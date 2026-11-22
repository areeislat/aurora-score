"""
Generador del dataset SINTÉTICO de la cartera piloto AURORA SCORE (Vertex Financial Group).

El caso de estudio (SCY1102) no entrega datos; se construye un dataset ficticio coherente con él:
- 12.000 créditos otorgados en el piloto controlado de Santiago (Chile) y Lima (Perú).
- Variables de fuentes alternativas descritas en el caso (telco, servicios básicos, billeteras,
  metadatos de la app, redes sociales con opt-in).
- Tasa de incumplimiento cercana al 11% (tasa de pérdida esperada del Año 1, Tabla 4 del caso).
- Sesgo histórico de la sección 4 y 7 del caso: sobrerrepresentación de hombres urbanos de 25-45 años,
  y variables proxy (gama del teléfono, tipo de plan) correlacionadas con nivel socioeconómico.
- Problemas de calidad reales: nulos, duplicados, outliers, etiquetas inconsistentes y rezago de 24-72 h.

Uso: python src/generar_dataset.py   (semilla fija = 2026 para reproducibilidad)
"""
import numpy as np
import pandas as pd
from pathlib import Path

SEED = 2026
N = 12_000
rng = np.random.default_rng(SEED)
OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)


def poblacion(n, rng):
    df = pd.DataFrame()
    df["pais"] = rng.choice(["Chile", "Perú"], n, p=[0.55, 0.45])
    df["ciudad_piloto"] = np.where(df["pais"] == "Chile", "Santiago", "Lima")
    # Sesgo histórico: base sobrerrepresenta hombres, 25-45 años, zona urbana
    df["genero"] = rng.choice(["Masculino", "Femenino"], n, p=[0.63, 0.37])
    tramo = rng.choice(["18-24", "25-45", "46-60", "60+"], n, p=[0.14, 0.62, 0.19, 0.05])
    lim = {"18-24": (18, 24), "25-45": (25, 45), "46-60": (46, 60), "60+": (61, 75)}
    df["edad"] = [rng.integers(lim[t][0], lim[t][1] + 1) for t in tramo]
    df["zona_residencia"] = rng.choice(["Urbana", "Periurbana", "Rural"], n, p=[0.74, 0.18, 0.08])
    p_inf = np.where(df["genero"] == "Femenino", 0.42, 0.30)
    df["sector_laboral"] = np.where(rng.random(n) < p_inf, "Informal",
                                    rng.choice(["Formal", "Independiente"], n, p=[0.7, 0.3]))
    return df


def comportamiento(df, rng):
    n = len(df)
    # Capacidad de pago latente: MISMA distribución para todos los grupos (el riesgo real no difiere)
    cap = rng.normal(0, 1, n)
    # "Brecha digital": desplaza la huella digital de grupos subrepresentados, sin relación con su riesgo real
    brecha = (np.where(df["zona_residencia"] == "Rural", 1.5, np.where(df["zona_residencia"] == "Periurbana", 0.5, 0))
              + np.where(df["edad"] > 60, 1.3, 0)
              + np.where((df["genero"] == "Femenino") & (df["sector_laboral"] == "Informal"), 1.0, 0))
    nivel_se = 0.9 * cap - 0.9 * brecha + rng.normal(0, 0.45, n)   # nivel socioeconómico observado vía proxies

    # --- Telecomunicaciones
    df["antiguedad_linea_meses"] = np.clip(rng.gamma(2.2, 18, n) * np.exp(0.15 * cap), 1, 240).round()
    p_post = 1 / (1 + np.exp(-(-0.9 + 0.9 * nivel_se)))
    df["tipo_plan"] = np.where(rng.random(n) < p_post, "Postpago", "Prepago")
    df["recarga_prom_mensual_usd"] = np.where(df["tipo_plan"] == "Prepago",
                                              np.clip(rng.lognormal(2.0 + 0.25 * nivel_se, 0.45), 2, 80), np.nan).round(1)
    df["pct_pagos_plan_a_tiempo"] = np.where(df["tipo_plan"] == "Postpago",
                                             np.clip(0.86 + 0.05 * cap + rng.normal(0, 0.09, n), 0.3, 1), np.nan).round(3)
    df["gama_dispositivo"] = pd.cut(nivel_se + rng.normal(0, 0.6, n), [-np.inf, -0.6, 0.7, np.inf],
                                    labels=["Baja", "Media", "Alta"]).astype(str)
    df["antiguedad_dispositivo_meses"] = np.clip(rng.gamma(2, 9, n) - 4 * nivel_se, 1, 96).round()
    df["sistema_operativo"] = np.where(rng.random(n) < 1 / (1 + np.exp(-(-1.6 + 1.1 * nivel_se))), "iOS", "Android")

    # --- Servicios básicos (utilities)
    df["meses_historial_servicios"] = np.clip(rng.gamma(3, 10, n) - 6 * brecha, 0, 120).round()
    df["pct_servicios_a_tiempo_12m"] = np.clip(0.84 + 0.06 * cap + rng.normal(0, 0.10, n), 0.2, 1).round(3)
    df["max_dias_atraso_servicios"] = np.clip(rng.gamma(1.4, 9, n) * np.exp(-0.55 * cap), 0, 180).round()
    df["rezago_dato_servicios_h"] = rng.choice([0, 24, 48, 72], n, p=[0.45, 0.30, 0.15, 0.10])

    # --- Billeteras digitales y e-commerce
    df["meses_actividad_billetera"] = np.clip(rng.gamma(2, 9, n) * np.exp(-0.45 * brecha), 0, 84).round()
    df["transacciones_mes"] = np.clip(rng.poisson(np.exp(2.3 + 0.35 * nivel_se)), 0, 300)
    df["ticket_promedio_usd"] = np.clip(rng.lognormal(3.0 + 0.3 * nivel_se, 0.5), 1, 900).round(1)
    df["tasa_devoluciones"] = np.clip(rng.beta(1.2, 18, n) * np.exp(-0.3 * cap), 0, 1).round(3)
    df["reclamos_12m"] = rng.poisson(np.exp(-0.6 - 0.45 * cap))

    # --- Metadatos de la app VFG
    df["tiempo_llenado_seg"] = np.clip(rng.lognormal(5.4, 0.45, n), 20, 3000).round()
    df["cambios_monto_solicitud"] = rng.poisson(np.exp(-0.3 - 0.35 * cap))
    df["sesiones_previas_app"] = rng.poisson(np.exp(1.2 + 0.2 * nivel_se))

    # --- Redes sociales (solo con opt-in)
    opt = rng.random(n) < 0.45
    df["opt_in_redes"] = np.where(opt, "Sí", "No")
    df["antiguedad_cuenta_redes_meses"] = np.where(opt, np.clip(rng.gamma(3, 25, n) - 15 * brecha, 1, 200).round(), np.nan)
    df["tamano_red_contactos"] = np.where(opt, np.clip(rng.lognormal(5.3 + 0.2 * nivel_se, 0.6), 5, 5000).round(), np.nan)

    # --- Condiciones del crédito (Tabla 4 del caso, Año 1)
    df["monto_credito_usd"] = np.clip(rng.normal(320, 85, n), 80, 700).round(-1)
    df["plazo_meses"] = rng.choice([3, 4, 5, 6], n, p=[0.15, 0.25, 0.40, 0.20])
    df["tasa_interes_mensual"] = 0.032

    # --- Variable objetivo: incumplimiento (mora >= 60 días). Depende de la capacidad real,
    #     del comportamiento de pago y de condiciones del crédito; NO del género, edad ni zona.
    z = (-2.75 - 0.85 * cap + 0.0016 * (df["monto_credito_usd"] - 320) + 0.08 * (df["plazo_meses"] - 5)
         + 0.55 * (df["tiempo_llenado_seg"] < 110)            # llenado anómalamente rápido (bots / fraude)
         + 0.75 * (df["max_dias_atraso_servicios"] > 40)      # umbral no lineal de atraso en servicios
         + 0.50 * (df["reclamos_12m"] >= 2)
         + 0.45 * (df["cambios_monto_solicitud"] >= 2)
         + 0.60 * (df["antiguedad_linea_meses"] < 6)          # líneas nuevas: posible fraude de identidad
         + rng.normal(0, 0.3, n))
    df["incumplimiento"] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    return df


def ensuciar(df, rng):
    """Problemas de calidad típicos de APIs heterogéneas de terceros."""
    n = len(df)
    for col, p in [("meses_historial_servicios", 0.04), ("ticket_promedio_usd", 0.03),
                   ("antiguedad_dispositivo_meses", 0.02), ("pct_servicios_a_tiempo_12m", 0.025)]:
        df.loc[rng.random(n) < p, col] = np.nan
    # Rezago de 72 h: el dato de servicios aún no llega
    df.loc[(df["rezago_dato_servicios_h"] == 72) & (rng.random(n) < 0.5), "pct_servicios_a_tiempo_12m"] = np.nan
    # Etiquetas inconsistentes entre operadoras
    idx = rng.choice(n, 140, replace=False)
    df.loc[idx, "tipo_plan"] = df.loc[idx, "tipo_plan"].map({"Prepago": "PREPAGO ", "Postpago": "post-pago"})
    # Outliers de captura en la app (timeouts y autocompletado)
    df.loc[rng.choice(n, 25, replace=False), "tiempo_llenado_seg"] = 99999
    return df


def main():
    df = poblacion(N, rng)
    df = comportamiento(df, rng)
    fechas = pd.to_datetime("2025-03-01") + pd.to_timedelta(rng.integers(0, 275, N), unit="D")
    df.insert(0, "fecha_otorgamiento", fechas.strftime("%Y-%m-%d"))
    df.insert(0, "id_credito", [f"AUR-{i:05d}" for i in range(1, N + 1)])
    df = ensuciar(df, rng)
    # 60 registros duplicados por reenvío de la API de la operadora
    dup = df.sample(60, random_state=SEED)
    df = pd.concat([df, dup]).sample(frac=1, random_state=SEED).reset_index(drop=True)
    df.to_csv(OUT / "aurora_cartera_piloto.csv", index=False)

    # Nuevas solicitudes (sin variable objetivo) para predicción / scoring automatizado
    rng2 = np.random.default_rng(SEED + 1)
    nuevas = comportamiento(poblacion(200, rng2), rng2).drop(columns="incumplimiento")
    nuevas.insert(0, "fecha_solicitud", "2026-11-20")
    nuevas.insert(0, "id_solicitud", [f"SOL-{i:04d}" for i in range(1, 201)])
    nuevas.to_csv(OUT / "nuevas_solicitudes.csv", index=False)
    print(df.shape, "tasa incumplimiento:", round(df["incumplimiento"].mean(), 4))
    print(df.groupby("zona_residencia")["incumplimiento"].mean().round(3).to_dict())
    print(df.groupby("genero")["incumplimiento"].mean().round(3).to_dict())


if __name__ == "__main__":
    main()
