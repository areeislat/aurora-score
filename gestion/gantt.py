"""Carta Gantt de la Release 1: plan (línea base v2) vs real, con hitos y fecha de corte."""
import sys; sys.path.insert(0, "gestion")
from datetime import date, timedelta
import matplotlib.pyplot as plt, matplotlib.dates as mdates
import datos_gestion as g
D = lambda s: date(2026, int(s[3:5]), int(s[:2])) if s else None
CORTE = date(2026, 11, 20)
PLAN, REAL, IMPREV, CURSO, TINTA, GRIS = "#b9c7dd", "#2a78d6", "#eb6834", "#eda100", "#0b0b0b", "#52514e"
T = g.TAREAS
fig, ax = plt.subplots(figsize=(13, 9.2))
for i, t in enumerate(T):
    tid, fase, nom, resp, ip, fp, ir, fr, av, est, dep, plan, part = t
    y = len(T) - i
    if plan: ax.barh(y + 0.18, (D(fp) - D(ip)).days + 1, left=D(ip), height=0.32, color=PLAN, edgecolor="none")
    if ir:
        fin = D(fr) if fr else CORTE
        col = REAL if plan else IMPREV
        if not fr: col = CURSO
        ax.barh(y - 0.18, (fin - D(ir)).days + 1, left=D(ir), height=0.32, color=col, edgecolor="none")
    etiqueta = f"{tid}  {nom[:52]}{'…' if len(nom) > 52 else ''}"
    ax.text(date(2026, 5, 29), y, etiqueta, ha="right", va="center", fontsize=8.2, color=TINTA if plan else IMPREV)
for h in g.HITOS:
    hp = D(h[2]); hr = D(h[3][:5])
    ax.plot(hp, len(T) + 1.2, marker="D", color=GRIS, ms=7); ax.plot(hr, len(T) + 1.2, marker="D", color=REAL if hr <= CORTE else CURSO, ms=7)
    ax.text(hr + timedelta(days=(-3 if h[0]=="H5" else 3 if h[0]=="H6" else 0)), len(T) + 1.75, h[0], ha={"H5":"right","H6":"left"}.get(h[0],"center"), fontsize=8, color=TINTA)
ax.axvline(CORTE, color="#e34948", ls="--", lw=1.2); ax.text(CORTE, 0.2, " corte 20-11", color="#e34948", fontsize=8, va="bottom")
ax.set_ylim(0.3, len(T) + 2.4); ax.set_yticks([])
ax.set_xlim(date(2026, 5, 30), date(2026, 12, 12))
ax.xaxis.set_major_locator(mdates.MonthLocator()); MES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{MES[mdates.num2date(v).month]} 2026"))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0)); ax.grid(axis="x", which="minor", color="#f0efec", lw=0.6); ax.grid(axis="x", which="major", color="#dcdcd6", lw=0.8)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.tick_params(axis="x", colors=GRIS, labelsize=9)
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
ax.legend(handles=[Patch(color=PLAN, label="Plan (línea base v2)"), Patch(color=REAL, label="Real"), Patch(color=CURSO, label="En curso al corte"),
                   Patch(color=IMPREV, label="Tarea no planificada (imprevisto)"), Line2D([], [], marker="D", color=GRIS, ls="", label="Hito plan"),
                   Line2D([], [], marker="D", color=REAL, ls="", label="Hito real / proyectado")],
          loc="lower left", ncol=3, frameon=False, fontsize=8.5, bbox_to_anchor=(0, -0.11))
ax.set_title("Carta Gantt Release 1 — planificado vs. ejecutado (corte 20-11-2026)", fontsize=12, fontweight="bold", loc="left", x=-0.42)
plt.subplots_adjust(left=0.33, right=0.98, top=0.95, bottom=0.1)
plt.savefig("reports/figures/fig10_gantt_plan_vs_real.png", dpi=160, facecolor="white")
print("ok")
