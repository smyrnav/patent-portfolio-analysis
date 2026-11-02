"""Chart each company's own sales and R&D growth, as commercial context rather than a ranking."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
ACCENT, LIGHT, INK, MUTED = "#124191", "#B8C2D0", "#1A1A1A", "#6B7686"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": INK, "ytick.color": INK})
with (ROOT / "data/processed/commercial_context.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
def name(r):
    if r["company"] != "Nokia":
        return f"{r['company']}, whole company"
    return "Nokia, whole group" if r["scope"].startswith("Whole") else "Nokia, Network Infrastructure"


labels = [f"{name(r)}\n{r['period']}" for r in rows]
sales = [(float(r["sales_m"]) / float(r["sales_prior_m"]) - 1) * 100 for r in rows]
rnd = [(float(r["rnd_m"]) / float(r["rnd_prior_m"]) - 1) * 100 for r in rows]
fig, ax = plt.subplots(figsize=(11, 6.6))
y = range(len(rows))
ax.barh([i - .19 for i in y], sales, height=.34, color=LIGHT, label="Sales growth")
ax.barh([i + .19 for i in y], rnd, height=.34, color=ACCENT, label="R&D growth")
for i in y:
    ax.text(sales[i] + .5, i - .19, f"+{sales[i]:.0f}%", va="center")
    ax.text(rnd[i] + .5, i + .19, f"+{rnd[i]:.0f}%", va="center", fontweight="bold")
ax.set_yticks(list(y), labels)
ax.invert_yaxis()
ax.xaxis.set_visible(False)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.set_xlim(0, 45)
ax.legend(frameon=False, loc="lower right")
ax.set_title("Commercial context only: these boundaries differ, so don't rank them", loc="left", fontweight="bold", fontsize=15, x=-.3)
fig.text(.02, .015, "Reporting periods and perimeters differ: Nokia segment/group vs peers' whole companies. Figures are context only, not evidence of underinvestment.\nEach bar is one company's growth against its own prior period. Total R&D isn't AI infrastructure R&D.\nNokia's two rows show how much the boundary alone changes.", color=MUTED, fontsize=10)
fig.tight_layout(rect=(0, .12, 1, 1))
fig.savefig(ROOT / "docs/img/commercial_context.png", dpi=150)
