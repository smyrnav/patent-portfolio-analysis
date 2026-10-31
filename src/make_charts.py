"""Draw the README charts from data/processed/owner_mapping.csv."""
import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "docs/img"
ACCENT, MUTED, INK = "#124191", "#B8C2D0", "#1A1A1A"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

with (ROOT / "data/processed/owner_mapping.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
counts = sorted((int(r["granted_patents"]) for r in rows), reverse=True)
total = sum(counts)

listings, names = Counter(), Counter()
for r in rows:
    listings[r["family"]] += int(r["granted_patents"])
    names[r["family"]] += 1

# Listings per family
order = [f for f, _ in listings.most_common()]
fig, ax = plt.subplots(figsize=(10, 4.2))
colors = [MUTED if f.startswith("Not Nokia") or f == "Needs review" else ACCENT for f in order]
ax.barh(order, [listings[f] for f in order], color=colors, height=.62)
ax.invert_yaxis()
for i, f in enumerate(order):
    ax.text(listings[f] + 250, i, f"{listings[f]:,} listings, {names[f]} names", va="center", fontsize=11)
ax.set_xlim(0, max(listings.values()) * 1.42)
ax.xaxis.set_visible(False)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.set_title("187 owner names fall into a handful of company families", loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig(IMG / "families.png", dpi=160)

# Concentration of listings across names
cumulative, running = [], 0
for c in counts:
    running += c
    cumulative.append(running / total * 100)
ones = sum(1 for c in counts if c == 1)
fig, ax = plt.subplots(figsize=(10, 4.2))
x = range(1, len(counts) + 1)
ax.plot(x, cumulative, color=ACCENT, lw=2.5)
ax.scatter([10], [cumulative[9]], color=ACCENT, s=60, zorder=3)
ax.annotate(f"Top 10 names: {cumulative[9]:.0f}% of listings", (10, cumulative[9]), xytext=(28, cumulative[9] - 14),
            arrowprops=dict(arrowstyle="-", color=INK))
ax.axvspan(len(counts) - ones + 1, len(counts), color=MUTED, alpha=.35, lw=0)
ax.text(len(counts) - ones / 2, 60, f"{ones} names appear\non only one patent", ha="center")
ax.set_xlabel("Owner names, largest first")
ax.set_ylabel("Share of all listings (%)")
ax.set_ylim(0, 104)
ax.set_xlim(1, len(counts))
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_title("A few names hold almost everything, and the rest is a long messy tail", loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig(IMG / "concentration.png", dpi=160)
print(f"total={total} top3={cumulative[2]:.1f} top10={cumulative[9]:.1f} ones={ones}")

# Listings by origin, across both queries
lineage = Counter(listings)
with (ROOT / "data/processed/lineage_mapping.csv").open(newline="") as f:
    for r in csv.DictReader(f):
        lineage[r["family"]] += int(r["granted_patents"])
groups = ["Nokia", "Alcatel and Alcatel-Lucent", "Lucent", "Nokia Siemens Networks", "Infinera", "Shanghai Bell"]
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.barh(groups, [lineage[g] for g in groups], color=[MUTED, ACCENT, ACCENT, MUTED, MUTED, MUTED], height=.62)
ax.invert_yaxis()
kept = sum(v for k, v in lineage.items() if not k.startswith("Not Nokia"))
for i, g in enumerate(groups):
    ax.text(lineage[g] + 250, i, f"{lineage[g]:,} ({lineage[g] / kept * 100:.0f}%)", va="center", fontsize=11)
ax.set_xlim(0, max(lineage.values()) * 1.2)
ax.xaxis.set_visible(False)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.set_title("About 4 in 10 listings trace back to Alcatel-Lucent", loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig(IMG / "lineage.png", dpi=160)
