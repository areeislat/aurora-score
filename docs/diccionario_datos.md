# Diccionario de datos — AURORA SCORE (dataset sintético)

**Archivo:** `data/aurora_cartera_piloto.csv` · **Registros:** 12.060 (12.000 créditos + 60 duplicados de API) · **Columnas:** 34
**Generado con:** `src/generar_dataset.py` (semilla 2026, reproducible) · **Tasa de incumplimiento:** 10,6%

> Dataset **ficticio** construido por el equipo porque el caso no entrega datos. Replica la cartera piloto de la sección 9 del caso
> (12.000 créditos en Santiago y Lima), las fuentes de la sección 3, las condiciones de la Tabla 4 y los sesgos de las secciones 4 y 7.
> El riesgo real de incumplimiento **no depende** de género, edad ni zona; los grupos subrepresentados tienen menor huella digital, lo que
> genera discriminación indirecta vía variables proxy (hallazgo replicado para auditar y mitigar).

| Variable | Fuente | Descripción | Tipo | % nulos | Uso |
|---|---|---|---|---|---|
| `id_credito` | Identificación | Identificador único del crédito | categórica | 0.0% | — |
| `fecha_otorgamiento` | Identificación | Fecha de otorgamiento (mar–dic 2025) | categórica | 0.0% | — |
| `pais` | Identificación | País del piloto | categórica | 0.0% | Excluida del modelo |
| `ciudad_piloto` | Identificación | Ciudad del piloto (Santiago / Lima) | categórica | 0.0% | Excluida del modelo |
| `genero` | Sensible | Género declarado | categórica | 0.0% | Solo auditoría de equidad |
| `edad` | Sensible | Edad en años | numérica | 0.0% | Solo auditoría de equidad |
| `zona_residencia` | Sensible | Zona inferida por antena (urbana/periurbana/rural) | categórica | 0.0% | Solo auditoría de equidad |
| `sector_laboral` | Sensible | Formal / Independiente / Informal | categórica | 0.0% | Solo auditoría de equidad |
| `antiguedad_linea_meses` | Telco | Antigüedad de la línea móvil | numérica | 0.0% | Modelo |
| `tipo_plan` | Telco | Prepago / Postpago (etiquetas inconsistentes en origen) | categórica | 0.0% | Proxy: excluida en modelo mitigado |
| `recarga_prom_mensual_usd` | Telco | Recarga mensual promedio (solo prepago) | numérica | 26.4% | Proxy: excluida en modelo mitigado |
| `pct_pagos_plan_a_tiempo` | Telco | % de pagos del plan a tiempo (solo postpago) | numérica | 73.6% | Modelo |
| `gama_dispositivo` | Telco / App | Gama del teléfono (baja/media/alta) | categórica | 0.0% | Proxy: excluida en modelo mitigado |
| `antiguedad_dispositivo_meses` | Telco / App | Antigüedad del dispositivo | numérica | 1.8% | Proxy: excluida en modelo mitigado |
| `sistema_operativo` | App | Android / iOS | categórica | 0.0% | Proxy: excluida en modelo mitigado |
| `meses_historial_servicios` | Utilities | Meses de historial de pago de luz, agua o gas | numérica | 3.8% | Modelo |
| `pct_servicios_a_tiempo_12m` | Utilities | % de boletas pagadas a tiempo, últimos 12 meses | numérica | 7.6% | Modelo |
| `max_dias_atraso_servicios` | Utilities | Máximo de días de atraso en servicios | numérica | 0.0% | Modelo |
| `rezago_dato_servicios_h` | Utilities | Rezago del dato de la API (0/24/48/72 h) | numérica | 0.0% | Modelo / control de calidad |
| `meses_actividad_billetera` | Billetera / e-commerce | Meses de actividad en billetera digital | numérica | 0.0% | Modelo |
| `transacciones_mes` | Billetera / e-commerce | Transacciones mensuales promedio | numérica | 0.0% | Modelo |
| `ticket_promedio_usd` | Billetera / e-commerce | Ticket promedio de compra | numérica | 3.3% | Proxy: excluida en modelo mitigado |
| `tasa_devoluciones` | Billetera / e-commerce | Proporción de compras devueltas | numérica | 0.0% | Modelo |
| `reclamos_12m` | Billetera / e-commerce | Reclamos en marketplaces, 12 meses | numérica | 0.0% | Modelo |
| `tiempo_llenado_seg` | App VFG | Segundos en completar la solicitud (outliers 99999 = timeout) | numérica | 0.0% | Modelo |
| `cambios_monto_solicitud` | App VFG | Veces que modificó el monto solicitado | numérica | 0.0% | Modelo |
| `sesiones_previas_app` | App VFG | Sesiones previas en la app | numérica | 0.0% | Modelo |
| `opt_in_redes` | Redes (opt-in) | Autorizó uso de redes sociales (Sí/No) | categórica | 0.0% | Modelo |
| `antiguedad_cuenta_redes_meses` | Redes (opt-in) | Antigüedad de la cuenta (sin contenido de publicaciones) | numérica | 56.0% | Modelo |
| `tamano_red_contactos` | Redes (opt-in) | Tamaño de la red de contactos | numérica | 56.0% | Modelo |
| `monto_credito_usd` | Crédito | Monto otorgado (promedio USD 320, Tabla 4) | numérica | 0.0% | Modelo |
| `plazo_meses` | Crédito | Plazo en meses (3–6) | numérica | 0.0% | Modelo |
| `tasa_interes_mensual` | Crédito | Tasa mensual 3,2% (Tabla 4, Año 1) | numérica | 0.0% | Constante; usada para cuota |
| `incumplimiento` | Objetivo | 1 = mora ≥ 60 días | numérica | 0.0% | Variable dependiente |

## Archivo de solicitudes nuevas
`data/nuevas_solicitudes.csv`: 200 solicitudes del 20-11-2026 con las mismas variables (sin `incumplimiento`), usadas para las 5 predicciones y el job de scoring.

## Problemas de calidad incluidos a propósito
| Problema | Origen en el caso | Tratamiento |
|---|---|---|
| 60 registros duplicados | Reenvíos de APIs de terceros | `drop_duplicates()` |
| Etiquetas `PREPAGO `, `post-pago` | APIs heterogéneas entre operadoras | Normalización de texto |
| 25 tiempos de llenado = 99999 s | Timeouts de la app | Se convierten en faltantes |
| Nulos en servicios con rezago 72 h | Fuentes con rezago 24–72 h | Imputación por mediana + indicador de faltante |
| Nulos estructurales (prepago/postpago, sin opt-in) | Diseño de las fuentes | Indicador de faltante (información, no error) |
