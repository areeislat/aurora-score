# AURORA SCORE — Scoring crediticio alternativo (Release 1: MVP piloto Chile–Perú)

**Vertex Financial Group · Gestión de Proyectos de Datos (SCY1102) · Evaluación Parcial 3**
Equipo: **Areliz Isla** (PM / Data Scientist) · **Daniela Montefinale** (Data Engineer / Compliance)

Implementación técnica del proyecto AURORA SCORE siguiendo CRISP-DM y gestionada con Trello + valor ganado (PMBOK).
El modelo estima la probabilidad de incumplimiento de solicitantes sin historial bancario usando datos alternativos
(telecomunicaciones, servicios básicos, billeteras digitales y metadatos de la app), con auditoría de equidad,
explicabilidad SHAP y un job automatizado de scoring con supervisión humana.

## Resultados clave (test, 3.000 créditos)
| Métrica | Valor |
|---|---|
| Modelo campeón | Gradient boosting mitigado (sin variables proxy + re-ponderación) |
| AUC / Gini / KS | 0,713 / 0,43 / 0,31 |
| Mora en aprobados automáticos | 6,6% vs 10,7% de la cartera piloto (−38%) |
| Impacto dispar mínimo (regla 4/5) | 0,82 (modelo original: 0,73 → no apto) |
| Automatización | Job diario (GitHub Actions) con gate humano, motivos de rechazo y control de drift PSI |

## Estructura
```
data/            aurora_cartera_piloto.csv (12.000 créditos + 60 duplicados) · nuevas_solicitudes.csv (200)
docs/            diccionario_datos.md
notebooks/       AURORA_SCORE_modelo_v1.ipynb  ← 8 pasos de la Guía 3.1 (ejecutable en Google Colab)
src/             generar_dataset.py · scoring_batch.py
models/          aurora_score_v1.joblib (modelo campeón + cortes de decisión + referencia de drift)
reports/         figuras, métricas, salida del scoring diario y monitoreo de drift
gestion/         AURORA_SCORE_seguimiento_control.xlsx (seguimiento, valor ganado, reporte de estado, flujo de caja)
.github/workflows/scoring_diario.yml   automatización programada (08:00 Chile)
```

## Cómo ejecutar
**Google Colab:** abrir el enlace de Colab de abajo y ejecutar todo (Entorno de ejecución → Ejecutar todas).

**Local:**
```bash
pip install -r requirements.txt
python src/generar_dataset.py                       # regenera el dataset (semilla 2026)
jupyter notebook notebooks/AURORA_SCORE_modelo_v1.ipynb
python src/scoring_batch.py --entrada data/nuevas_solicitudes.csv --salida reports/
```

## Nota sobre los datos
El caso de estudio no entrega datos. El dataset es **sintético**, generado por el equipo con `src/generar_dataset.py`
para replicar la cartera piloto, las fuentes, las tasas y los sesgos descritos en el caso. No contiene datos de personas reales.

## Enlaces
- Tablero de gestión (Trello): https://trello.com/b/sd2LHARo
- Notebook en Colab: https://colab.research.google.com/github/areeislat/aurora-score/blob/main/notebooks/AURORA_SCORE_modelo_v1.ipynb
