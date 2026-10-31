"""Chart how sales and R&D growth compare across Nokia and its rivals."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
ACCENT, LIGHT, INK, MUTED = "#124191", "#B8C2D0", "#1A1A1A", "#6B7686"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": INK, "ytick.color": INK})
with (ROOT / "data/processed/investment_position.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
rows = [r for r in rows if r["scope"] != "Whole group (reported)"]
labels = [("Nokia Network\nInfrastructure" if r["company"] == "Nokia" else r["company"]) + f"\n{r['period']}" for r in rows]
sales = [(float(r["sales_m"]) / float(r["sales_prior_m"]) - 1) * 100 for r in rows]
rnd = [(float(r["rnd_m"]) / float(r["rnd_prior_m"]) - 1) * 100 for r in rows]
fig, ax = plt.subplots(figsize=(11, 5.6))
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
ax.set_title("Sales are growing faster than R&D at all four", loc="left", fontweight="bold", fontsize=15)
fig.text(.02, .015, "Periods and scope differ. Nokia's row is one segment with comparable R&D, and the others are whole companies with GAAP R&D.", color=MUTED, fontsize=10)
fig.tight_layout(rect=(0, .05, 1, 1))
fig.savefig(ROOT / "docs/img/investment_position.png", dpi=150)
