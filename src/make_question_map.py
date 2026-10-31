"""Draw the business question map and the question-by-data matrix."""
from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

IMG = Path(__file__).resolve().parents[1] / "docs/img"
ACCENT, MID, MUTED, INK, CARD, EMPTY = "#124191", "#5B7DB8", "#6B7686", "#1A1A1A", "#F2F4F8", "#DDE2EA"

QUESTIONS = [
    ("Portfolio efficiency", "Which patents are worth maintaining, developing or reconsidering?",
     "Renewal history, remaining life, breadth, citations, overlap", "Add USPTO renewal records", "START HERE"),
    ("Competitive intelligence", "Where are competitors gaining technological advantages?",
     "Growth and share by technology and market, against rivals", "Add a rival table", "NEXT"),
    ("Technology strategy", "Where should Nokia invest in R&D?",
     "Refill rate, momentum, gaps against rivals", "Builds on competitive data", "THEN"),
    ("Commercial intelligence", "Which parts of the portfolio have licensing potential?",
     "Declared essential patents, citations by others, life left", "Add ETSI and citing patents", "THEN"),
    ("Market foresight", "Which emerging technologies could become commercially important?",
     "Fast growth from a small base, new entrants, standards work", "Add industry-wide data", "LAST"),
]
LIMITS = ["Market size or customer demand", "Revenue per patent or licence terms", "Nokia's real costs and strategy", "Recent inventions, due to publication delay"]

fig, ax = plt.subplots(figsize=(15, 9.1))
ax.set_xlim(0, 15)
ax.set_ylim(0, 9.1)
ax.axis("off")
ax.text(.15, 8.72, "Five business questions, and what each one needs", fontsize=21, fontweight="bold", color=INK)
ax.text(.15, 8.32, "Patent data gives signals to investigate. It doesn't give the final decision.", fontsize=13, color=MUTED)
H, GAP = 1.08, .12
for i, (t, q, sig, need, step) in enumerate(QUESTIONS):
    y = 7.05 - i * (H + GAP)
    color = ACCENT if i == 0 else MID
    ax.add_patch(FancyBboxPatch((.15, y), 14.7, H, boxstyle="round,pad=0,rounding_size=0.08", fc=CARD, ec="none"))
    ax.add_patch(FancyBboxPatch((.15, y), .08, H, boxstyle="square,pad=0", fc=color, ec="none"))
    ax.text(.4, y + H - .28, t, fontsize=14, fontweight="bold", color=INK, va="center")
    ax.text(.4, y + .34, "\n".join(wrap(q, 48)), fontsize=11, color=INK, va="center")
    ax.text(5.7, y + H - .25, "SIGNALS", fontsize=9, fontweight="bold", color=MUTED, va="center")
    ax.text(5.7, y + .4, "\n".join(wrap(sig, 42)), fontsize=11, color=INK, va="center")
    ax.text(10.1, y + H - .25, "NEEDS", fontsize=9, fontweight="bold", color=MUTED, va="center")
    ax.text(10.1, y + .4, need, fontsize=11, color=INK, va="center")
    ax.text(14.65, y + H / 2, step, fontsize=10.5, fontweight="bold", color=color, va="center", ha="right")
ax.text(.15, 1.0, "PATENT DATA CAN'T SHOW", fontsize=11.5, fontweight="bold", color=MUTED)
for i, t in enumerate(LIMITS):
    ax.text(.15 + (i % 2) * 5.4, .62 - (i // 2) * .36, "×  " + t, fontsize=12, color=INK)
fig.tight_layout(pad=.4)
fig.savefig(IMG / "question_map.png", dpi=150)

BLOCKS = ["Inventions", "Filing office", "Dates", "Technology", "Origin", "Renewals", "Fees", "Rival data", "Citing patents", "Standards", "Industry-wide"]
NEEDS = {
    "Portfolio efficiency": [0, 1, 2, 3, 5, 6, 8],
    "Competitive intelligence": [0, 1, 2, 3, 7],
    "Technology strategy": [0, 2, 3, 4, 7],
    "Commercial intelligence": [0, 1, 2, 3, 8, 9],
    "Market foresight": [0, 2, 3, 9, 10],
}
fig, ax = plt.subplots(figsize=(12, 4.3))
for r, need in enumerate(NEEDS.values()):
    for c in range(len(BLOCKS)):
        on = c in need
        ax.scatter(c, r, s=220 if on else 34, color=(MID if c >= 5 else ACCENT) if on else EMPTY, zorder=2)
ax.set_xticks(range(len(BLOCKS)), BLOCKS, rotation=35, ha="left", color=INK, fontsize=11)
ax.xaxis.tick_top()
ax.set_yticks(range(len(NEEDS)), list(NEEDS), color=INK, fontsize=12)
ax.axvline(4.5, color=MUTED, lw=1, ls=(0, (4, 4)))
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_ylim(5, -.6)
ax.text(2, 4.72, "In my table", ha="center", color=ACCENT, fontweight="bold", fontsize=11)
ax.text(7.5, 4.72, "Not collected yet", ha="center", color=MID, fontweight="bold", fontsize=11)
fig.tight_layout()
fig.savefig(IMG / "question_data_matrix.png", dpi=150)
