"""Fuente única de verdad de la gestión del proyecto (alimenta Excel, Trello, informe y presentación)."""
from datetime import date
D = lambda s: date(2026, int(s[3:5]), int(s[0:2]))   # "dd-mm" -> 2026

INICIO, CORTE = date(2026, 6, 1), date(2026, 11, 20)
EQUIPO = {"AI": "Areliz Isla (PM / Data Scientist)", "DM": "Daniela Montefinale (Data Engineer / Compliance)",
          "KA": "Kairos Analytics (proveedor cloud)"}

RELEASES = [
    ("R1", "MVP scoring piloto Chile–Perú", "M1–M6", "01-06-2026", "30-11-2026", "Año 0 (inversión USD 401.500)", "En curso (87% avance físico)"),
    ("R2", "Escalamiento y MLOps: API < 8 s, score thin-file, agentes IA de atención y cobranza", "M7–M12", "01-12-2026", "31-05-2027", "Año 1 (OpEx USD 875.000, 12 meses)", "Planificada"),
    ("R3", "Expansión Colombia: conectores, residencia de datos, recalibración", "M13–M18", "01-06-2027", "30-11-2027", "Año 1 (incluido arriba)", "Planificada"),
    ("—", "México (Año 3 del flujo de caja) — fuera de los 18 meses", "Año 3", "2028", "2028", "Año 3", "Fuera de alcance"),
]

# id, fase CRISP-DM, tarea, resp, ini_plan, fin_plan, ini_real, fin_real, avance, estado, deps, planificada, partida EVM
TAREAS = [
 ("T01","Gestión","Kickoff y Project Charter v2","AI","01-06","12-06","01-06","12-06",1.0,"Completada","—",True,"Capacitación y gestión del cambio"),
 ("T02","Gestión","CR-01: re-línea base por releases y presupuesto 18 meses","AI","15-06","30-06","15-06","03-07",1.0,"Completada","T01",True,"Capacitación y gestión del cambio"),
 ("T03","Infraestructura","Provisionar cloud (IAM, VPC, lakehouse, residencia CL/PE)","KA","15-06","17-07","15-06","17-07",1.0,"Completada","T01",True,"Plataforma de datos"),
 ("T04","Infraestructura","Pipeline MLOps base (registro de modelos, CI/CD)","KA","20-07","14-08","20-07","21-08",1.0,"Completada","T03",True,"Plataforma de datos"),
 ("T05","Business Understanding","Acuerdos de datos y consentimiento granular (telco, utilities, billeteras)","DM","08-06","10-07","08-06","10-07",1.0,"Completada","T01",True,"Conectores e integración"),
 ("T06","Data Understanding","Conectores de ingesta (3 telcos, utilities CL/PE, marketplace)","DM","13-07","14-08","13-07","21-08",1.0,"Completada","T03, T05",True,"Conectores e integración"),
 ("T07","Data Understanding","Extracción cartera piloto (12.000 créditos) y diccionario de datos","DM","03-08","14-08","10-08","21-08",1.0,"Completada","T06",True,"Conectores e integración"),
 ("T08","Data Understanding","EDA y reporte de calidad de datos","AI","17-08","31-08","24-08","04-09",1.0,"Completada","T07",True,"Desarrollo de modelos ML"),
 ("T09","Data Preparation","Limpieza: duplicados, etiquetas, outliers, nulos","DM","01-09","11-09","07-09","18-09",1.0,"Completada","T08",True,"Desarrollo de modelos ML"),
 ("T10","Data Preparation","Ingeniería de variables y feature store v1","DM","14-09","25-09","21-09","02-10",1.0,"Completada","T09",True,"Desarrollo de modelos ML"),
 ("T11","Data Preparation","Auditoría de representatividad y detección de proxies","AI","21-09","02-10","21-09","02-10",1.0,"Completada","T08",True,"Desarrollo de modelos ML"),
 ("T12","Modeling","Baseline: regresión logística","AI","05-10","09-10","05-10","14-10",1.0,"Completada","T10",True,"Desarrollo de modelos ML"),
 ("T13","Modeling","Gradient boosting + ajuste de hiperparámetros (CV 5 pliegues)","AI","12-10","23-10","15-10","28-10",1.0,"Completada","T12",True,"Desarrollo de modelos ML"),
 ("T14","Modeling","Explicabilidad SHAP y motivos de rechazo","AI","19-10","30-10","26-10","04-11",1.0,"Completada","T13",True,"Desarrollo de modelos ML"),
 ("T15","Evaluation","Evaluación técnica (AUC, Gini, KS) y de negocio (mora aprobados)","AI","02-11","06-11","02-11","06-11",1.0,"Completada","T13",True,"Desarrollo de modelos ML"),
 ("T16","Evaluation","Auditoría de equidad (regla 4/5)","DM","09-11","13-11","09-11","13-11",1.0,"Completada","T15",True,"Desarrollo de modelos ML"),
 ("T17","Evaluation","Revisión de cumplimiento (DPIA, derecho a explicación)","DM","09-11","20-11","09-11","",0.7,"En progreso","T14",True,"Desarrollo de modelos ML"),
 ("T18","Deployment","Job de scoring por lotes con gate humano","AI","16-11","20-11","16-11","20-11",1.0,"Completada","T15",True,"Plataforma de datos"),
 ("T19","Deployment","Monitoreo de drift (PSI) y alertas","AI","16-11","24-11","18-11","",0.6,"En progreso","T18",True,"Plataforma de datos"),
 ("T20","Deployment","Capacitación a analistas de riesgo y gestión del cambio","DM","23-11","27-11","","",0.0,"Pendiente","T18",True,"Capacitación y gestión del cambio"),
 ("T21","Data Preparation","Tratar rezago 72 h de utilities Perú (imputación + indicador)","DM","","","16-11","17-11",1.0,"Completada","T09",False,"Conectores e integración"),
 ("T22","Modeling","Mitigación de sesgo: modelo sin proxies + re-ponderación","AI","","","18-11","19-11",1.0,"Completada","T16",False,"Desarrollo de modelos ML"),
 ("T23","Evaluation","CR-02: reporte de equidad por grupo para el regulador","DM","","","17-11","",0.5,"En progreso","T16",False,"Desarrollo de modelos ML"),
 ("T24","Gestión","CR-03: evaluar segmento microempresas (diferido a R2)","AI","","","19-11","19-11",1.0,"Completada","—",False,"Capacitación y gestión del cambio"),
 ("T25","Infraestructura","Optimizar costo cloud (límites de presupuesto, instancias spot)","KA","","","20-11","",0.3,"En progreso","T13",False,"Plataforma de datos"),
 ("T26","Gestión","Reporte de estado semana 25 a stakeholders","AI","","","20-11","20-11",1.0,"Completada","—",False,"Capacitación y gestión del cambio"),
]
HITOS = [
 ("H1","Charter y línea base v2 aprobados (CR-01)","30-06","03-07","Cumplido con atraso de 3 días"),
 ("H2","Data Readiness Review","31-08","04-09","Cumplido con atraso de 4 días"),
 ("H3","Dataset analítico validado","02-10","02-10","Cumplido en plazo"),
 ("H4","Modelo campeón v1 seleccionado","30-10","04-11","Cumplido con atraso de 5 días"),
 ("H5","Gate Go/No-Go R1","27-11","04-12 (reprogramado)","En riesgo: +5 días hábiles"),
 ("H6","Go-live MVP piloto Chile–Perú","30-11","07-12 (reprogramado)","En riesgo: +5 días hábiles"),
]
EVENTOS = [
 ("Lun 16-11","Imprevisto de datos","La utility de Perú entrega el 18% de los registros con rezago de 72 h","El job de scoring no puede usar puntualidad en servicios para esos casos","T21 (no planificada): imputación + indicador de faltante","+1 día en T18"),
 ("Mar 17-11","Nuevo requerimiento","Cumplimiento (por consulta del regulador peruano) pide reporte de equidad por género, edad y zona","Nueva tarea y entregable para el Gate R1","CR-02 aprobado → T23","+3 días en T17"),
 ("Mié 18-11","Hallazgo de calidad del modelo","La auditoría de equidad (T16) muestra impacto dispar 0,73 (rural) y 0,77 (60+) < 0,80","El modelo original NO puede pasar el Gate","T22: retirar proxies + re-ponderar; nuevo campeón con mínimo 0,82","+2 días; Gate R1 se mueve"),
 ("Jue 19-11","Cambio de alcance","Gerencia Comercial pide incluir microempresas en R1","Aumentaría alcance ~30% (nuevas fuentes y variables)","CR-03 rechazado para R1, diferido a backlog R2","Sin impacto (alcance protegido)"),
 ("Vie 20-11","Desviación de costo","Factura cloud del mes +18% por reentrenamientos repetidos (grid search)","CPI cae a 0,93","T25: límites de presupuesto, instancias spot, grid acotado","USD 4.500 sobre lo previsto en el mes"),
]
# partida EVM: BAC, PV, EV, AC (USD) al corte 20-11-2026
EVM = [
 ("Conectores e integración", 95000, 95000, 95000, 104000),
 ("Plataforma de datos (configuración y puesta en marcha)", 120000, 112000, 100000, 103000),
 ("Licencias y setup fees", 45000, 45000, 45000, 45000),
 ("Desarrollo de modelos ML", 80000, 80000, 74000, 84000),
 ("Capacitación y gestión del cambio", 25000, 5000, 5000, 5000),
]
CONTINGENCIA = 36500
CAMBIOS = [
 ("CR-01","15-06","Re-línea base: plan por releases (R1 MVP M1–6, R2 M7–12, R3 M13–18) y presupuesto de 18 meses cuadrado con el flujo de caja","PMO / Directorio","Aprobado 03-07","Corrige la incoherencia del plan v1: go-live en M18 vs ingresos desde el Año 1"),
 ("CR-02","17-11","Reporte de equidad por grupo exigido por Cumplimiento","Gerencia de Riesgo","Aprobado 17-11","+3 días en revisión de cumplimiento"),
 ("CR-03","19-11","Incluir microempresas en el MVP","Gerencia Comercial","Rechazado para R1 / diferido a R2 19-11","Protege la fecha del Gate R1"),
]
ACCIONES = [
 ("AC-01","Cronograma","Gate R1 +5 días hábiles (SPI 0,95)","Fast-tracking: capacitación (T20) en paralelo con monitoreo (T19); daily de 15 min hasta el Gate","AI","27-11"),
 ("AC-02","Costo","CPI 0,93; costo cloud +18% en el mes","Límites de presupuesto con alertas al 80%, instancias spot para entrenamiento, grid de hiperparámetros acotado","KA","25-11"),
 ("AC-03","Calidad / ética","Impacto dispar < 0,80 en rural y 60+","Modelo mitigado como campeón; auditoría de equidad obligatoria en cada reentrenamiento (criterio de aceptación)","AI","19-11 (hecho)"),
 ("AC-04","Datos","Rezago 72 h utilities Perú","SLA con penalidad en contrato; indicador de faltante en producción; alerta de rezago en el job","DM","30-11"),
 ("AC-05","Alcance","Presión por ampliar alcance (microempresas)","Control de cambios formal; backlog priorizado de R2 revisado con Comercial","AI","04-12"),
]
RIESGOS = [
 ("R-01","Datos","Calidad y rezago de fuentes de terceros",4,4,"Materializado (16-11)","AC-04, T21","DM"),
 ("R-04","Ético","Sesgo algorítmico contra grupos subrepresentados",4,5,"Materializado y mitigado (18-11)","AC-03, T22","AI"),
 ("R-03","Regulatorio","Exigencias de explicabilidad y equidad del regulador",3,5,"Activo","CR-02, T23","DM"),
 ("R-09","Presupuesto","Sobrecosto cloud",3,3,"Materializado (20-11)","AC-02, T25","KA"),
 ("R-05","Organizacional","Scope creep",3,4,"Activo (CR-03)","AC-05","AI"),
 ("R-13","Técnico","Drift de datos en producción (PSI máx 0,23 = vigilar)",3,4,"Nuevo","T19","AI"),
 ("R-14","Contractual","Contratos de datos sin renovación garantizada > 24 meses",2,5,"Nuevo","Cláusulas de renovación y fuentes alternativas en R2","DM"),
]
