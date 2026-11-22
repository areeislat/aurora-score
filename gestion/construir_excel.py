import sys; sys.path.insert(0, "gestion")
from datetime import date
import datos_gestion as g
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.comments import Comment

F = "Arial"; NAVY = "1F3864"
H = Font(name=F, bold=True, color="FFFFFF", size=10); B = Font(name=F, size=10); BB = Font(name=F, size=10, bold=True)
BLUE = Font(name=F, size=10, color="0000FF"); T = Font(name=F, size=14, bold=True, color=NAVY); ST = Font(name=F, size=10, italic=True, color="52514E")
HF = PatternFill("solid", fgColor=NAVY); YEL = PatternFill("solid", fgColor="FFFF00"); GRY = PatternFill("solid", fgColor="F2F2F2")
thin = Side(style="thin", color="BFBFBF"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WR = Alignment(wrap_text=True, vertical="top"); CEN = Alignment(horizontal="center", vertical="top", wrap_text=True)
EST = {"Completada": "C6EFCE", "En progreso": "FFEB9C", "Pendiente": "D9D9D9", "Bloqueada": "FFC7CE"}

wb = Workbook()
def hoja(nombre, titulo, sub, headers, widths):
    ws = wb.create_sheet(nombre)
    ws["A1"] = titulo; ws["A1"].font = T; ws["A2"] = sub; ws["A2"].font = ST
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        c = ws.cell(4, i, h); c.font = H; c.fill = HF; c.alignment = CEN; c.border = BOX
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A5"; ws.sheet_view.showGridLines = False
    return ws
def fila(ws, r, vals, fmt=None, font=B):
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.font = font; c.border = BOX; c.alignment = WR
        if fmt and i in fmt: c.number_format = fmt[i]
def d(s):
    return date(2026, int(s[3:5]), int(s[0:2])) if s else None

# 0. Índice
ws = wb.active; ws.title = "Indice"; ws.sheet_view.showGridLines = False
ws["A1"] = "AURORA SCORE — Seguimiento y control del proyecto"; ws["A1"].font = T
ws["A2"] = "Vertex Financial Group · Equipo: Areliz Isla y Daniela Montefinale · Corte de estado: viernes 20-11-2026 (semana 25 del proyecto)"; ws["A2"].font = ST
idx = [("Plan_LB_v2", "Línea base v2 por releases (CR-01) e hitos"), ("Seguimiento", "Tareas planificadas vs ejecutadas, responsables, fechas, dependencias y desviación en días"),
       ("Semana_simulada", "Semana 16–20 nov con eventos inesperados (Guía 3.2)"), ("Valor_ganado", "PV, EV, AC, SPI, CPI y proyección EAC de la Release 1"),
       ("Reporte_estado", "Reporte de estado para stakeholders (semáforo)"), ("Acciones_correctivas", "Acciones derivadas del análisis de desviaciones"),
       ("Control_cambios", "Registro de solicitudes de cambio"), ("Riesgos", "Actualización del registro de riesgos"),
       ("Flujo_caja", "Flujo de caja anual Año 0–5 (Alt. A) con fórmulas + sensibilidad"), ("Presupuesto_18m", "Presupuesto del horizonte de 18 meses cuadrado con el flujo de caja")]
for i, (h, dsc) in enumerate(idx, 4):
    ws.cell(i, 1, h).font = BB; ws.cell(i, 2, dsc).font = B
ws["A16"] = "Convención de colores: texto azul = dato de entrada; negro = fórmula; fondo amarillo = supuesto clave."; ws["A16"].font = ST
ws.column_dimensions["A"].width = 24; ws.column_dimensions["B"].width = 95

# 1. Plan LB v2
ws = hoja("Plan_LB_v2", "Línea base v2 del proyecto (aprobada por CR-01, 03-07-2026)",
          "El plan v1 ponía el go-live en el mes 18 mientras el flujo de caja suponía créditos desde el Año 1. La v2 entrega valor por releases.",
          ["Release", "Alcance", "Meses", "Inicio", "Término", "Financiamiento (flujo de caja)", "Estado al 20-11"], [9, 60, 10, 12, 12, 32, 18])
for r, v in enumerate(g.RELEASES, 5): fila(ws, r, v)
r0 = 11; ws.cell(r0 - 1, 1, "Hitos de la Release 1").font = BB
for i, h in enumerate(["Hito", "Descripción", "Fecha plan", "Fecha real / proyectada", "Estado"], 1):
    c = ws.cell(r0, i, h); c.font = H; c.fill = HF; c.border = BOX
for k, h in enumerate(g.HITOS, r0 + 1):
    fila(ws, k, [h[0], h[1], d(h[2]), h[3], h[4]], {3: "DD-MM-YYYY"})

# 2. Seguimiento
ws = hoja("Seguimiento", "Seguimiento de tareas: planificado vs ejecutado (Release 1)",
          "Fuente: tablero Trello del proyecto. Fechas en 2026. Desviación = fin real (o corte) − fin planificado, en días corridos.",
          ["ID", "Fase CRISP-DM", "Tarea", "Responsable", "Inicio plan", "Fin plan", "Inicio real", "Fin real", "% avance", "Estado",
           "Dependencias", "¿Planificada?", "Desviación (días)", "Partida presupuestaria"], [6, 18, 50, 16, 11, 11, 11, 11, 9, 12, 11, 11, 11, 30])
ws["P3"] = "Fecha de corte"; ws["P3"].font = BB; ws["Q3"] = date(2026, 11, 20); ws["Q3"].font = BLUE; ws["Q3"].number_format = "DD-MM-YYYY"
for r, t in enumerate(g.TAREAS, 5):
    resp = {"AI": "Areliz Isla", "DM": "Daniela Montefinale", "KA": "Kairos Analytics"}[t[3]]
    fila(ws, r, [t[0], t[1], t[2], resp, d(t[4]), d(t[5]), d(t[6]), d(t[7]), t[8], t[9], t[10], "Sí" if t[11] else "No (imprevisto)",
                 f'=IF(F{r}="","n/a",IF(H{r}<>"",H{r}-F{r},MAX(0,$Q$3-F{r})))', t[12]],
         {5: "DD-MM", 6: "DD-MM", 7: "DD-MM", 8: "DD-MM", 9: "0%"})
    ws.cell(r, 10).fill = PatternFill("solid", fgColor=EST[t[9]])
    if not t[11]: ws.cell(r, 12).fill = PatternFill("solid", fgColor="FCE4D6")
n = len(g.TAREAS) + 4
ws.conditional_formatting.add(f"M5:M{n}", CellIsRule(operator="greaterThan", formula=["0"], font=Font(name=F, color="C00000", bold=True)))
s = n + 2
ws.cell(s, 3, "Resumen").font = BB
res = [("Tareas totales", f"=COUNTA(A5:A{n})", "0"), ("Completadas", f'=COUNTIF(J5:J{n},"Completada")', "0"),
       ("En progreso", f'=COUNTIF(J5:J{n},"En progreso")', "0"), ("Pendientes", f'=COUNTIF(J5:J{n},"Pendiente")', "0"),
       ("No planificadas (imprevistos)", f'=COUNTIF(L5:L{n},"No*")', "0"), ("Avance promedio", f"=AVERAGE(I5:I{n})", "0%"),
       ("Tareas planificadas con atraso", f'=COUNTIF(M5:M{n},">0")', "0")]
for i, (a, f, fm) in enumerate(res, s + 1):
    ws.cell(i, 3, a).font = B; c = ws.cell(i, 4, f); c.font = BB; c.number_format = fm

# 3. Semana simulada
ws = hoja("Semana_simulada", "Simulación de una semana de avance con eventos inesperados (16 al 20 de noviembre de 2026)",
          "Guía 3.2: requerimientos recientes, nuevas tareas y cambio de alcance. Avance real y tareas no planificadas registradas en Seguimiento y Trello.",
          ["Día", "Tipo de evento", "Evento", "Impacto", "Respuesta / tarea", "Efecto en plan"], [12, 20, 48, 40, 42, 26])
for r, e in enumerate(g.EVENTOS, 5): fila(ws, r, e)
ws.cell(11, 1, "Avance real de la semana").font = BB
av = [("Planificadas para la semana", "T17, T18, T19 (3 tareas)"), ("Completadas", "T18 (job de scoring)"),
      ("En progreso", "T17 (70%), T19 (60%)"), ("No planificadas abiertas", "T21, T22, T23, T24, T25, T26 (6 tareas; 4 completadas)")]
for i, (a, b) in enumerate(av, 12): ws.cell(i, 1, a).font = B; ws.cell(i, 3, b).font = B

# 4. Valor ganado
ws = hoja("Valor_ganado", "Gestión del valor ganado (EVM) — Release 1 al 20-11-2026",
          "BAC = presupuesto de la inversión Año 0 de la Alternativa A (Tabla 1 del caso) sin contingencia. Cifras en USD.",
          ["Partida", "BAC", "PV (planificado)", "EV (ganado)", "AC (real)", "SV = EV−PV", "CV = EV−AC", "SPI", "CPI"], [46, 12, 15, 13, 12, 12, 12, 8, 8])
for r, e in enumerate(g.EVM, 5):
    fila(ws, r, [e[0], e[1], e[2], e[3], e[4], f"=D{r}-C{r}", f"=D{r}-E{r}", f"=IF(C{r}=0,\"-\",D{r}/C{r})", f"=IF(E{r}=0,\"-\",D{r}/E{r})"],
         {2: "#,##0", 3: "#,##0", 4: "#,##0", 5: "#,##0", 6: "#,##0;(#,##0);-", 7: "#,##0;(#,##0);-", 8: "0.00", 9: "0.00"})
    for col in (2, 3, 4, 5): ws.cell(r, col).font = BLUE
t = 5 + len(g.EVM)
fila(ws, t, ["TOTAL RELEASE 1"] + [f"=SUM({c}5:{c}{t-1})" for c in "BCDE"] + [f"=D{t}-C{t}", f"=D{t}-E{t}", f"=D{t}/C{t}", f"=D{t}/E{t}"],
     {2: "#,##0", 3: "#,##0", 4: "#,##0", 5: "#,##0", 6: "#,##0;(#,##0);-", 7: "#,##0;(#,##0);-", 8: "0.00", 9: "0.00"}, BB)
for c in range(1, 10): ws.cell(t, c).fill = GRY
k = t + 2
proj = [("Reserva de contingencia (10%, Tabla 1)", g.CONTINGENCIA, "#,##0", True),
        ("EAC = AC + (BAC − EV) / CPI", f"=E{t}+(B{t}-D{t})/I{t}", "#,##0", False),
        ("VAC = BAC − EAC", f"=B{t}-B{k+1}", "#,##0;(#,##0);-", False),
        ("% de la contingencia que se consumiría", f"=-B{k+2}/B{k}", "0%", False),
        ("Inversión total proyectada (Año 0)", f"=B{k+1}", "#,##0", False),
        ("Presupuesto Año 0 aprobado (con contingencia)", f"=B{t}+B{k}", "#,##0", False)]
for i, (a, f, fm, inp) in enumerate(proj, k):
    ws.cell(i, 1, a).font = B; c = ws.cell(i, 2, f); c.number_format = fm; c.font = BLUE if inp else BB
ws.cell(k + 7, 1, "Lectura: SPI y CPI < 1 → atraso y sobrecosto moderados; la proyección queda dentro de la reserva de contingencia (semáforo amarillo).").font = ST
ws.conditional_formatting.add(f"H5:I{t}", CellIsRule(operator="lessThan", formula=["1"], fill=PatternFill("solid", fgColor="FFEB9C")))

# 5. Reporte de estado
ws = wb.create_sheet("Reporte_estado"); ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 30; ws.column_dimensions["B"].width = 110
ws["A1"] = "Reporte de estado N°25 — semana del 16 al 20 de noviembre de 2026"; ws["A1"].font = T
ws["A2"] = "Para: Gerencia de Datos e IA (sponsor), Gerencia de Riesgo, Cumplimiento, Kairos Analytics · De: PM AURORA SCORE"; ws["A2"].font = ST
rep = [("Estado general", "AMARILLO — Release 1 con 87% de avance físico (valor ganado); atraso de 5 días hábiles en el Gate Go/No-Go y sobrecosto dentro de la contingencia."),
       ("Resumen ejecutivo", "El modelo de scoring v1 está entrenado, evaluado y automatizado. Reduce la mora en aprobados automáticos de 10,7% a 6,6% (−38%). La auditoría de equidad obligó a reemplazar el modelo original por una versión mitigada que cumple la regla 4/5 en todos los grupos. Gate R1 reprogramado del 27-11 al 04-12."),
       ("Indicadores", "Avance físico R1: 87,4% (EV/BAC) · SPI 0,95 · CPI 0,94 · EAC USD 390 mil vs BAC 365 mil (usa ~69% de la contingencia de USD 36,5 mil) · AUC 0,713 · Gini 0,43 · impacto dispar mínimo 0,82"),
       ("Logros de la semana", "1) Job de scoring diario con gate humano y motivos SHAP en producción de prueba (T18). 2) Modelo mitigado sin proxies (T22). 3) Rezago 72 h de utilities Perú resuelto con imputación + indicador (T21). 4) CR-03 evaluado y diferido, protegiendo el alcance."),
       ("Prioridades próxima semana", "1) Cerrar revisión de cumplimiento y reporte de equidad para el regulador (T17, T23). 2) Terminar monitoreo de drift PSI y alertas (T19). 3) Capacitar analistas de riesgo en la revisión humana (T20). 4) Bajar el costo cloud (T25)."),
       ("Riesgos y problemas", "R-03 regulatorio (activo), R-13 drift (PSI máx 0,23 = vigilar), R-09 sobrecosto cloud (materializado), R-14 renovación de contratos de datos > 24 meses (nuevo)."),
       ("Decisiones requeridas", "Sponsor: aprobar nueva fecha del Gate R1 (04-12) y uso de contingencia hasta USD 25 mil. Comercial: validar que microempresas entra en el backlog de R2.")]
for i, (a, b) in enumerate(rep, 4):
    ws.cell(i, 1, a).font = BB; c = ws.cell(i, 2, b); c.font = B; c.alignment = WR; ws.row_dimensions[i].height = 48
ws["B4"].fill = PatternFill("solid", fgColor="FFEB9C")

# 6. Acciones correctivas
ws = hoja("Acciones_correctivas", "Acciones correctivas", "Derivadas del análisis de desviaciones de cronograma, costo, calidad, datos y alcance.",
          ["ID", "Dimensión", "Desviación", "Acción correctiva", "Responsable", "Fecha"], [8, 14, 36, 70, 14, 12])
for r, a in enumerate(g.ACCIONES, 5):
    fila(ws, r, [a[0], a[1], a[2], a[3], {"AI": "Areliz Isla", "DM": "Daniela Montefinale", "KA": "Kairos Analytics"}[a[4]], a[5]])

# 7. Control de cambios
ws = hoja("Control_cambios", "Registro de control de cambios", "Todo cambio de alcance, plazo o costo pasa por solicitud formal.",
          ["ID", "Fecha", "Cambio solicitado", "Solicitante", "Decisión", "Impacto"], [8, 9, 60, 20, 26, 46])
for r, c in enumerate(g.CAMBIOS, 5): fila(ws, r, c)

# 8. Riesgos
ws = hoja("Riesgos", "Actualización del registro de riesgos (escala 1–5)", "Nivel = Probabilidad × Impacto. Crítico ≥ 17, Alto 10–16, Medio 5–9.",
          ["ID", "Categoría", "Riesgo", "P", "I", "Nivel", "Estado al 20-11", "Respuesta", "Dueño"], [7, 14, 46, 5, 5, 8, 26, 34, 18])
for r, x in enumerate(g.RIESGOS, 5):
    fila(ws, r, [x[0], x[1], x[2], x[3], x[4], f"=D{r}*E{r}", x[5], x[6], {"AI": "Areliz Isla", "DM": "Daniela Montefinale", "KA": "Kairos Analytics"}[x[7]]])
n = 4 + len(g.RIESGOS)
ws.conditional_formatting.add(f"F5:F{n}", CellIsRule(operator="greaterThanOrEqual", formula=["17"], fill=PatternFill("solid", fgColor="FFC7CE")))
ws.conditional_formatting.add(f"F5:F{n}", CellIsRule(operator="between", formula=["10", "16"], fill=PatternFill("solid", fgColor="FFEB9C")))

# 9. Flujo de caja
ws = wb.create_sheet("Flujo_caja"); ws.sheet_view.showGridLines = False
ws["A1"] = "Flujo de caja anual — Alternativa A (cloud), USD"; ws["A1"].font = T
ws["A2"] = "Supuestos de las Tablas 2, 4 y 5 del caso. Año 0 = construcción de la Release 1 (jun–nov 2026); Año 1 inicia con el go-live del MVP."; ws["A2"].font = ST
ws.column_dimensions["A"].width = 46
for c in "BCDEFG": ws.column_dimensions[c].width = 14
sup = [("Tasa de descuento", 0.15, "0.0%"), ("Impuesto a la renta", 0.27, "0.0%"), ("Valor terminal", 0, "#,##0")]
ws["A4"] = "Supuestos generales"; ws["A4"].font = BB
for i, (a, v, fm) in enumerate(sup, 5):
    ws.cell(i, 1, a).font = B; c = ws.cell(i, 2, v); c.font = BLUE; c.number_format = fm; c.fill = YEL
ws["C7"] = "Supuesto conservador: sin valor de continuidad después del Año 5"; ws["C7"].font = ST
hdr = ["Concepto", "Año 0", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
for i, h in enumerate(hdr, 1):
    c = ws.cell(9, i, h); c.font = H; c.fill = HF; c.alignment = CEN
inp = [("Créditos otorgados", [45000, 110000, 240000, 410000, 590000], "#,##0"), ("Monto promedio (USD)", [320, 340, 350, 370, 400], "#,##0"),
       ("Plazo promedio (meses)", [5, 5, 6, 6, 6], "0"), ("Tasa de interés mensual", [.032, .031, .030, .029, .028], "0.0%"),
       ("Comisión de originación", [.04, .04, .038, .038, .036], "0.0%"), ("Tasa de pérdida por mora", [.11, .09, .07, .055, .045], "0.0%")]
for i, (a, vals, fm) in enumerate(inp, 10):
    ws.cell(i, 1, a).font = B
    for j, v in enumerate(vals, 3): c = ws.cell(i, j, v); c.font = BLUE; c.number_format = fm
calc = [(16, "Monto colocado", "={c}10*{c}11"), (17, "Ingreso por intereses", "={c}16*{c}13*{c}12"), (18, "Ingreso por comisiones", "={c}16*{c}14"),
        (19, "Pérdida esperada por mora", "=-{c}16*{c}15"), (20, "Ingreso financiero neto", "=SUM({c}17:{c}19)")]
for r, a, f in calc:
    ws.cell(r, 1, a).font = BB if r == 20 else B
    for j in range(3, 8):
        col = get_column_letter(j); c = ws.cell(r, j, f.format(c=col)); c.number_format = "#,##0;(#,##0);-"; c.font = BB if r == 20 else B
opx = [("Infraestructura cloud", [180000, 260000, 340000, 410000, 470000]), ("Licencias de software", [95000, 110000, 125000, 140000, 150000]),
       ("Recursos humanos", [560000, 620000, 680000, 740000, 790000]), ("Agentes o servicios automáticos", [40000, 70000, 105000, 140000, 175000])]
for i, (a, vals) in enumerate(opx, 21):
    ws.cell(i, 1, a).font = B
    for j, v in enumerate(vals, 3): c = ws.cell(i, j, -v); c.font = BLUE; c.number_format = "#,##0;(#,##0);-"
rows2 = [(25, "Resultado antes de impuestos", "={c}20+SUM({c}21:{c}24)"), (26, "Impuesto (27%, solo si hay utilidad)", "=-MAX({c}25,0)*$B$6")]
for r, a, f in rows2:
    ws.cell(r, 1, a).font = B
    for j in range(3, 8):
        col = get_column_letter(j); c = ws.cell(r, j, f.format(c=col)); c.number_format = "#,##0;(#,##0);-"
ws.cell(27, 1, "Inversión inicial (Tabla 1, Alt. A)").font = B; c = ws.cell(27, 2, -401500); c.font = BLUE; c.number_format = "#,##0;(#,##0);-"
ws.cell(28, 1, "FLUJO DE CAJA NETO").font = BB
ws.cell(28, 2, "=B27").number_format = "#,##0;(#,##0);-"
for j in range(3, 8):
    col = get_column_letter(j); c = ws.cell(28, j, f"={col}25+{col}26+IF({j}=7,$B$7,0)"); c.number_format = "#,##0;(#,##0);-"; c.font = BB
for j in range(1, 8): ws.cell(28, j).fill = GRY
ws.cell(29, 1, "Flujo acumulado").font = B; ws.cell(29, 2, "=B28").number_format = "#,##0;(#,##0);-"
for j in range(3, 8):
    col, prev = get_column_letter(j), get_column_letter(j - 1); ws.cell(29, j, f"={prev}29+{col}28").number_format = "#,##0;(#,##0);-"
ind = [("VAN al 15%", "=B28+NPV(B5,C28:G28)", "#,##0"), ("TIR", "=IRR(B28:G28)", "0.0%"), ("ROI 5 años = (Σ flujos − inversión) / inversión", "=(SUM(C28:G28)+B28)/-B28", "0%")]
ws["A31"] = "Indicadores"; ws["A31"].font = BB
for i, (a, f, fm) in enumerate(ind, 32):
    ws.cell(i, 1, a).font = B; c = ws.cell(i, 2, f); c.number_format = fm; c.font = BB
ws["C34"] = "Nota crítica: el ROI es extremo porque el caso entrega ingresos netos sin restar el costo de fondear la cartera (USD 236 M colocados en el Año 5)."; ws["C34"].font = ST
# Sensibilidad
ws["A36"] = "Análisis de sensibilidad (VAN al 15%)"; ws["A36"].font = BB
for i, h in enumerate(["Escenario", "Factor mora", "Factor volumen", "VAN", "TIR"], 1):
    c = ws.cell(37, i, h); c.font = H; c.fill = HF
esc = [("Base (caso)", 1.0, 1.0), ("Mora +30%", 1.3, 1.0), ("Mora +50%", 1.5, 1.0), ("Volumen −30%", 1.0, 0.7),
       ("Pesimista: mora +50% y volumen −30%", 1.5, 0.7), ("Estrés: mora ×2 y volumen −50%", 2.0, 0.5)]
ws["H37"] = "Flujos por escenario (Año 0 a 5)"; ws["H37"].font = BB
for i, (a, fm_, fv) in enumerate(esc, 38):
    ws.cell(i, 1, a).font = B
    c = ws.cell(i, 2, fm_); c.font = BLUE; c.number_format = "0.0x"
    c = ws.cell(i, 3, fv); c.font = BLUE; c.number_format = "0.0x"
    ws.cell(i, 8, "=$B$27").number_format = "#,##0"
    for j, col in enumerate("CDEFG"):
        pre = f"(({col}17+{col}18)*$C{i}+{col}19*$C{i}*$B{i}+SUM({col}21:{col}24))"
        ws.cell(i, 9 + j, f"={pre}-MAX({pre},0)*$B$6").number_format = "#,##0;(#,##0);-"
    ws.cell(i, 4, f"=H{i}+NPV($B$5,I{i}:M{i})").number_format = "#,##0"
    ws.cell(i, 5, f"=IRR(H{i}:M{i})").number_format = "0.0%"
for col in "HIJKLM": ws.column_dimensions[col].width = 13

# 10. Presupuesto 18 meses
ws = hoja("Presupuesto_18m", "Presupuesto del horizonte de 18 meses (respuesta a la observación de la Evaluación 2)",
          "Plan v1: go-live en M18 sin presupuesto de construcción. Plan v2: Año 0 = 6 meses de construcción (inversión); Año 1 = 12 meses de operación y R2/R3.",
          ["Periodo", "Releases", "Concepto", "USD", "Fuente"], [16, 14, 52, 14, 34])
pres = [("M1–M6 (Año 0)", "R1", "Inversión inicial: conectores, plataforma, licencias, modelos, capacitación y contingencia", 401500, "Tabla 1 del caso, Alt. A"),
        ("M7–M18 (Año 1)", "R2 + R3", "Infraestructura cloud", 180000, "Tabla 2, Año 1"),
        ("M7–M18 (Año 1)", "R2 + R3", "Licencias de software", 95000, "Tabla 2, Año 1"),
        ("M7–M18 (Año 1)", "R2 + R3", "Recursos humanos (8 personas desde el go-live del MVP)", 560000, "Tabla 2, Año 1"),
        ("M7–M18 (Año 1)", "R2 + R3", "Agentes o servicios automáticos", 40000, "Tabla 2, Año 1")]
for r, p in enumerate(pres, 5):
    fila(ws, r, list(p), {4: "#,##0"}); ws.cell(r, 4).font = BLUE
fila(ws, 10, ["TOTAL 18 MESES", "", "Egresos del horizonte del plan", "=SUM(D5:D9)", ""], {4: "#,##0"}, BB)
fila(ws, 11, ["Ingreso neto Año 1", "", "Ingresos financieros netos del MVP en operación (M7–M18)", "=Flujo_caja!C20", "Hoja Flujo_caja"], {4: "#,##0"})
fila(ws, 12, ["Flujo acumulado al M18", "", "Ingresos − egresos − impuestos del Año 1", "=Flujo_caja!C29", "Hoja Flujo_caja"], {4: "#,##0;(#,##0);-"}, BB)
ws["A14"] = "Coherencia: el equipo de 8 personas y el costo cloud se pagan desde el go-live del MVP (M7), que es cuando el flujo de caja registra los 45.000 créditos del Año 1."; ws["A14"].font = ST
ws["A15"] = "Observación al caso: evaluar 4,8 M de personas en 18 meses con ~45.000 créditos en el Año 1 implica una tasa de aprobación < 1%; lo interpretamos como pre-scoring masivo de bases de operadoras, no como solicitudes."; ws["A15"].font = ST

wb.save("gestion/AURORA_SCORE_seguimiento_control.xlsx"); print("ok")
