"""Draw the README charts from the corrected recount and the filings by office."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "docs/img"
ACCENT, MUTED, INK = "#124191", "#B8C2D0", "#1A1A1A"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def hide(ax):
    ax.xaxis.set_visible(False)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)


# Patents by origin
with (ROOT / "data/processed/us_30y_recount.csv").open(newline="") as f:
    origins = [r for r in csv.DictReader(f) if r["row_type"] == "origin"]
total = sum(int(r["patents"]) for r in origins)
labels = [r["label"] for r in origins]
values = [int(r["patents"]) for r in origins]
colors = [ACCENT if l in ("Alcatel and Alcatel-Lucent", "Lucent") else MUTED for l in labels]
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.barh(labels, values, color=colors, height=.62)
ax.invert_yaxis()
for i, v in enumerate(values):
    ax.text(v + 250, i, f"{v:,} ({v / total * 100:.0f}%)", va="center", fontsize=11)
ax.set_xlim(0, max(values) * 1.2)
hide(ax)
ax.set_title("46% of US patents filed since 1996 carry an Alcatel or Lucent name", loc="left", fontweight="bold", x=-.28)
fig.tight_layout()
fig.savefig(IMG / "origin_30y.png", dpi=160)

# Applications by patent office
with (ROOT / "data/raw/filings_by_country.csv").open(newline="") as f:
    offices = sorted(csv.DictReader(f), key=lambda r: -int(r["applications"]))[:9]
names = {"US": "United States", "EP": "European Patent Office", "WO": "International (WO), not yet a patent",
         "CN": "China", "DE": "Germany", "JP": "Japan", "AU": "Australia", "KR": "South Korea", "CA": "Canada"}
fig, ax = plt.subplots(figsize=(10, 4.6))
values = [int(r["applications"]) for r in offices]
colors = [ACCENT if r["country_code"] in ("US", "EP", "CN") else MUTED for r in offices]
ax.barh([names[r["country_code"]] for r in offices], values, color=colors, height=.62)
ax.invert_yaxis()
for i, v in enumerate(values):
    ax.text(v + 600, i, f"{v:,}", va="center", fontsize=11)
ax.set_xlim(0, max(values) * 1.12)
hide(ax)
ax.set_title("Europe is close behind the US", loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig(IMG / "offices.png", dpi=160)
