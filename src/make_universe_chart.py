"""Draw how 72,207 families with a Nokia-lineage applicant sort into a candidate universe."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "docs/img"
ACCENT, MID, MUTED, LIGHT, INK = "#124191", "#5B7DB8", "#6B7686", "#C9D1DC", "#1A1A1A"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

with (ROOT / "data/processed/family_status.csv").open(newline="") as f:
    status = list(csv.DictReader(f))
order = ["Granted past 20 years", "Never granted older filing", "Sold-business names only", "Recent application may be pending", "Granted within 20 years"]
names = {"Granted past 20 years": "Grant evidence, past 20 years", "Never granted older filing": "No grant evidence, older",
         "Sold-business names only": "Sold-business names", "Recent application may be pending": "Recent application,\nno grant detected",
         "Granted within 20 years": "Grant evidence, within 20 years"}
counts = {r["status"]: int(r["families"]) for r in status}
fig, ax = plt.subplots(figsize=(11, 4.8))
remaining = sum(counts.values())
all_families = remaining
ax.barh(["All families"], [remaining], color=LIGHT, height=.62)
ax.text(remaining + 700, 0, f"{remaining:,}", va="center", fontweight="bold")
for k in order[:3]:
    remaining -= counts[k]
    ax.barh([names[k]], [counts[k]], left=[remaining], color=LIGHT, height=.62)
    ax.text(remaining - 700, list(order).index(k) + 1, f"−{counts[k]:,}", va="center", ha="right", fontweight="bold")
ax.barh([names[order[3]]], [counts[order[3]]], left=[counts[order[4]]], color=MID, height=.62)
ax.text(counts[order[4]] + counts[order[3]] + 700, 4, f"{counts[order[3]]:,}", va="center", fontweight="bold")
ax.barh([names[order[4]]], [counts[order[4]]], color=ACCENT, height=.62)
ax.text(counts[order[4]] + 700, 5, f"{counts[order[4]]:,}", va="center", fontweight="bold")
ax.invert_yaxis()
ax.set_xlim(0, 80000)
ax.xaxis.set_visible(False)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.set_title(f"From {all_families:,} families to a candidate universe, not a verified portfolio", loc="left", fontweight="bold", x=-.3, fontsize=15)
fig.tight_layout()
fig.savefig(IMG / "candidate_universe.png", dpi=150)
