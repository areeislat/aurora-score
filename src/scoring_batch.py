"""
AURORA SCORE · Job de scoring por lotes (automatización Release 1).

1. Lee las solicitudes del día (CSV).
2. Aplica la misma preparación del entrenamiento y el modelo campeón (models/aurora_score_v1.joblib).
3. Aplica la política con supervisión humana: Aprobar / Revisión humana / Rechazar.
4. Genera los 3 principales motivos (SHAP) para cada rechazo o revisión (derecho a explicación).
5. Calcula el drift de cada variable (PSI) contra la referencia de entrenamiento y emite alerta si PSI > 0,25.

Uso:  python src/scoring_batch.py --entrada data/nuevas_solicitudes.csv --salida reports/
Se ejecuta automáticamente con GitHub Actions (.github/workflows/scoring_diario.yml).
"""
import argparse, json, sys
from datetime import date
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

ETIQ = {"max_dias_atraso_servicios": "atrasos en pago de servicios básicos", "pct_servicios_a_tiempo_12m": "puntualidad en servicios básicos",
        "antiguedad_linea_meses": "antigüedad de la línea móvil", "linea_nueva": "línea móvil muy reciente",
        "llenado_rapido": "formulario completado anormalmente rápido", "tiempo_llenado_seg": "tiempo de llenado del formulario",
        "reclamos_12m": "reclamos en comercio electrónico", "cambios_monto_solicitud": "cambios del monto solicitado",
        "tasa_devoluciones": "tasa de devoluciones", "pct_pagos_plan_a_tiempo": "puntualidad del plan móvil",
        "monto_credito_usd": "monto solicitado", "cuota_estimada_usd": "cuota estimada", "plazo_meses": "plazo",
        "meses_historial_servicios": "historial en servicios básicos", "transacciones_mes": "uso de billetera digital",
        "meses_actividad_billetera": "antigüedad en billetera digital", "sesiones_previas_app": "uso previo de la app",
        "tamano_red_contactos": "tamaño de red social (opt-in)", "antiguedad_cuenta_redes_meses": "antigüedad de cuenta en redes (opt-in)",
        "opt_in_redes_No": "sin autorización de redes sociales", "opt_in_redes_Sí": "autorización de redes sociales",
        "rezago_dato_servicios_h": "rezago del dato de servicios"}


def preparar(df):
    df = df.copy()
    df["tipo_plan"] = df["tipo_plan"].str.strip().str.lower().replace({"post-pago": "postpago"}).str.capitalize()
    df.loc[df["tiempo_llenado_seg"] > 3000, "tiempo_llenado_seg"] = np.nan
    df["llenado_rapido"] = (df["tiempo_llenado_seg"] < 110).astype(int)
    df["linea_nueva"] = (df["antiguedad_linea_meses"] < 6).astype(int)
    r = df["tasa_interes_mensual"]
    df["cuota_estimada_usd"] = (df["monto_credito_usd"] * r / (1 - (1 + r) ** -df["plazo_meses"])).round(1)
    return df


def psi(ref, act, bins=10):
    ref, act = ref.dropna(), act.dropna()
    cortes = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(cortes) < 3:
        return 0.0
    cortes[0], cortes[-1] = -np.inf, np.inf
    r = np.histogram(ref, cortes)[0] / len(ref) + 1e-4
    a = np.histogram(act, cortes)[0] / max(len(act), 1) + 1e-4
    return float(np.sum((a - r) * np.log(a / r)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default="data/nuevas_solicitudes.csv")
    ap.add_argument("--salida", default="reports/")
    ap.add_argument("--modelo", default="models/aurora_score_v1.joblib")
    a = ap.parse_args()
    art = joblib.load(a.modelo)
    modelo, cols, cortes = art["modelo"], art["columnas"], art["cortes"]
    sol = preparar(pd.read_csv(a.entrada))

    pd_ = modelo.predict_proba(sol[cols])[:, 1]
    decision = np.where(pd_ < cortes["aprobar"], "Aprobar", np.where(pd_ < cortes["rechazar"], "Revisión humana", "Rechazar"))

    motivos = ["—"] * len(sol)
    try:
        import shap
        prep, gb = modelo.named_steps["prep"], modelo.named_steps["modelo"]
        nombres = prep.get_feature_names_out()
        Xs = pd.DataFrame(prep.transform(sol[cols]), columns=nombres)
        exp = shap.LinearExplainer(gb, art["fondo_shap"]) if hasattr(gb, "coef_") else shap.TreeExplainer(gb)
        sv = np.asarray(exp.shap_values(Xs))
        for i in np.where(decision != "Aprobar")[0]:
            top = [j for j in np.argsort(-sv[i])[:3] if sv[i][j] > 0]
            motivos[i] = "; ".join(ETIQ.get(nombres[j].replace("missingindicator_", ""), nombres[j]) for j in top)
    except ImportError:
        print("Aviso: shap no instalado, se omiten motivos.", file=sys.stderr)

    out = Path(a.salida); out.mkdir(parents=True, exist_ok=True)
    hoy = date.today().strftime("%Y%m%d")
    res = pd.DataFrame({"id_solicitud": sol["id_solicitud"], "prob_incumplimiento": pd_.round(4),
                        "decision": decision, "motivos": motivos, "version_modelo": f'{art["nombre"]} v{art["version"]}'})
    res.to_csv(out / f"scoring_{hoy}.csv", index=False)

    ref = art["muestra_referencia"]
    psis = {c: round(psi(ref[c], sol[c]), 4) for c in ref.columns if c in sol.columns}
    alertas = {c: v for c, v in psis.items() if v > 0.25}
    reporte = {"fecha": hoy, "solicitudes": int(len(sol)),
               "decisiones": res["decision"].value_counts().to_dict(),
               "psi_max": max(psis.values()), "variables_en_alerta": alertas,
               "estado_drift": "ALERTA: reentrenar" if alertas else ("VIGILAR" if max(psis.values()) > 0.10 else "ESTABLE")}
    (out / "monitoreo_drift.json").write_text(json.dumps(reporte, indent=2, ensure_ascii=False))
    print(f"[AURORA] {len(sol)} solicitudes procesadas → {reporte['decisiones']} · drift: {reporte['estado_drift']} (PSI máx {reporte['psi_max']})")


if __name__ == "__main__":
    main()
