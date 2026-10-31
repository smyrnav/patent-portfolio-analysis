"""Draw the licensing scale check and the portfolio filter charts."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "docs/img"
ACCENT, MID, MUTED, LIGHT, INK = "#124191", "#5B7DB8", "#6B7686", "#C9D1DC", "#1A1A1A"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

NINE_MONTHS_M = 1217
ANNUAL_M = NINE_MONTHS_M / 9 * 12
FAMILIES = 19873
PER_FAMILY = ANNUAL_M * 1e6 / FAMILIES


def money(v):
    return f"€{v / 1e6:.1f}M" if v >= 1e6 else f"€{v / 1e3:,.0f}k"


fig = plt.figure(figsize=(13, 6.9))
fig.text(.03, .94, "About €82k of licensing-unit sales per family, but the average hides most of the story", fontsize=17, fontweight="bold")
fig.text(.03, .895, "A scale check using Nokia's reported Technology Standards net sales, not a value per patent", fontsize=12, color=MUTED)

# How the figure is built
ax = fig.add_axes([.03, .13, .41, .69])
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")
steps = [("€1,217M", "Net sales, January–September 2026", LIGHT, INK),
         (f"≈ €{ANNUAL_M / 1000:.1f}B", "Per year, scaled up from 9 months", LIGHT, INK),
         (f"÷ {FAMILIES:,}", "Core families from my filter", LIGHT, INK),
         (f"≈ {money(PER_FAMILY)}", "Average sales per family, per year", ACCENT, "white")]
for i, (big, small, fill, ink) in enumerate(steps):
    y = 7.75 - i * 2.55
    ax.add_patch(plt.Rectangle((0, y), 10, 2.0, fc=fill, ec="none"))
    ax.text(.35, y + 1.0, big, fontsize=19, fontweight="bold", va="center", color=ink)
    ax.text(4.25, y + 1.0, small, fontsize=11, va="center", color=ink, wrap=True)
    if i < 3:
        ax.annotate("", xy=(5, y - .5), xytext=(5, y), arrowprops=dict(arrowstyle="-|>", color=INK))

# What the average would mean if income were concentrated
ax = fig.add_axes([.56, .2, .41, .56])
shares = [100, 50, 10, 1]
values = [ANNUAL_M * 1e6 / (FAMILIES * s / 100) for s in shares]
labels = [f"All families" if s == 100 else f"Top {s}%" for s in shares]
ax.barh(labels, values, color=[ACCENT, MID, MID, MID], height=.6)
ax.set_xscale("log")
ax.set_xlim(1e4, 2e8)
ax.invert_yaxis()
for i, v in enumerate(values):
    ax.text(v * 1.2, i, money(v), va="center", fontweight="bold")
ax.xaxis.set_visible(False)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.set_title("Same total, different reality", loc="left", fontweight="bold", pad=24)
ax.text(0, 1.03, "Sales per earning family if only this share earns it (log scale)", transform=ax.transAxes, fontsize=10.5, color=MUTED)
fig.text(.56, .13, "Illustrative only. Nokia doesn't publish how income is split\nacross families, so these aren't estimates of the real split.", fontsize=10.5, color=MUTED, va="top")
fig.text(.03, .05, "Sources: Nokia Q3 2026 report and my filter. Sales may include items beyond these families, and licensing sales can jump with catch-up payments.", fontsize=10, color=MUTED)
fig.savefig(IMG / "scale_check.png", dpi=150)

# Portfolio filter
with (ROOT / "data/processed/family_status.csv").open(newline="") as f:
    status = list(csv.DictReader(f))
order = ["Granted past 20 years", "Never granted older filing", "Sold-business names only", "Recent application may be pending", "Granted within 20 years"]
names = {"Granted past 20 years": "Granted, past 20 years", "Never granted older filing": "No grant detected, older",
         "Sold-business names only": "Sold-business names", "Recent application may be pending": "Possibly pending",
         "Granted within 20 years": "Core: granted, within 20 years"}
counts = {r["status"]: int(r["families"]) for r in status}
fig, ax = plt.subplots(figsize=(11, 4.8))
remaining = sum(counts.values())
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
ax.set_title("From 72,207 families to a workable portfolio", loc="left", fontweight="bold", x=-.3, fontsize=15)
fig.tight_layout()
fig.savefig(IMG / "portfolio_filter.png", dpi=150)
print(round(PER_FAMILY), [round(v) for v in values])
