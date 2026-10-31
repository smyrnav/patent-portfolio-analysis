"""Draw the business question map and the question-by-data matrix."""
from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

IMG = Path(__file__).resolve().parents[1] / "docs/img"
ACCENT, MID, MUTED, INK, CARD, EMPTY = "#124191", "#5B7DB8", "#6B7686", "#1A1A1A", "#F2F4F8", "#DDE2EA"

NOW = [
    ("Refill rate", "Is new invention replacing what's about to expire?", "Where to invest in new patents"),
    ("Protection cliff", "How much protection could run out by 2036, by technology?", "What to renew or replace"),
    ("Geographic gaps", "Which key technologies lack cover in major markets?", "Where to file next"),
    ("Costly coverage", "Which areas are filed in many more offices than others?", "Where to file more narrowly"),
    ("Deal value", "What did each acquisition add that Nokia didn't already have?", "How to value future deals"),
    ("Dependency", "Which technologies rely on few countries or inventors?", "R&D site and talent risk"),
]
MORE = [
    ("Keep or drop", "Which patents do owners stop renewing, and which look next?", "Renewal records"),
    ("10-year budget", "What would keeping the portfolio cost, as a range?", "Renewal records, official fees"),
    ("Rival benchmark", "Where is Nokia ahead of or behind Ericsson and Huawei?", "Same table for rivals"),
    ("Standards exposure", "How much of the 5G cover expires, and how soon?", "ETSI declarations"),
]
NEVER = ["Revenue per patent", "Licensing terms", "Who holds a licence", "Nokia's real internal costs", "Why it decided anything"]


def card(ax, x, y, w, h, title, body, foot, color, width=54):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08", fc=CARD, ec="none"))
    ax.add_patch(FancyBboxPatch((x, y), .07, h, boxstyle="square,pad=0", fc=color, ec="none"))
    ax.text(x + .2, y + h - .24, title, fontsize=13, fontweight="bold", color=INK, va="center")
    ax.text(x + .2, y + h - .48, "\n".join(wrap(body, width)), fontsize=10.5, color=INK, va="top", linespacing=1.3)
    ax.text(x + .2, y + .16, foot, fontsize=9.5, color=MUTED, va="center")


fig, ax = plt.subplots(figsize=(15, 9.3))
ax.set_xlim(0, 15)
ax.set_ylim(0, 9.3)
ax.axis("off")
ax.text(.15, 8.95, "What this data can answer for the business", fontsize=21, fontweight="bold", color=INK)
ax.text(.15, 8.55, "Where is the portfolio strong, where is it exposed, and where might it cost more than it should?", fontsize=13, color=MUTED)
ax.text(.15, 8.08, "ANSWERABLE NOW, from my 30-year table", fontsize=11.5, fontweight="bold", color=ACCENT)
for i, (t, b, f) in enumerate(NOW):
    card(ax, .15 + (i % 2) * 4.45, 6.5 - (i // 2) * 1.68, 4.3, 1.48, t, b, "Decision: " + f, ACCENT)
ax.text(9.2, 8.08, "NEEDS MORE DATA", fontsize=11.5, fontweight="bold", color=MID)
for i, (t, b, f) in enumerate(MORE):
    card(ax, 9.2, 6.72 - i * 1.25, 5.65, 1.14, t, b, "Needs: " + f, MID, width=74)
ax.text(9.2, 2.72, "CAN'T BE ANSWERED FROM PUBLIC DATA", fontsize=11.5, fontweight="bold", color=MUTED)
for i, t in enumerate(NEVER):
    ax.text(9.2, 2.34 - i * .36, "×  " + t, fontsize=12, color=INK)
ax.text(.15, 2.72, "THE PATH", fontsize=11.5, fontweight="bold", color=INK)
STEPS = ["Clean owner\nnames", "Answer the\nsix questions", "Add renewals\nand fees", "One-page\ndecision brief"]
for i, t in enumerate(STEPS):
    x = .15 + i * 2.2
    ax.add_patch(FancyBboxPatch((x, 1.45), 1.85, 1.0, boxstyle="round,pad=0,rounding_size=0.08", fc=ACCENT, ec="none"))
    ax.text(x + .925, 1.95, t, ha="center", va="center", color="white", fontsize=11.5, fontweight="bold")
    if i < 3:
        ax.annotate("", xy=(x + 2.18, 1.95), xytext=(x + 1.87, 1.95), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5))
fig.tight_layout(pad=.4)
fig.savefig(IMG / "question_map.png", dpi=150)

# Which data each question needs
BLOCKS = ["Inventions", "Filing office", "Dates", "Technology", "Origin", "Inventors", "Renewals", "Fees", "Rival data", "Standards"]
NEEDS = {
    "Refill rate": "Inventions Dates Technology",
    "Protection cliff": "Inventions Dates Technology",
    "Geographic gaps": "Inventions Filing_office Technology",
    "Costly coverage": "Inventions Filing_office Technology",
    "Deal value": "Inventions Technology Origin",
    "Dependency": "Inventions Technology Inventors",
    "Keep or drop": "Inventions Dates Technology Renewals",
    "10-year budget": "Inventions Filing_office Dates Renewals Fees",
    "Rival benchmark": "Inventions Dates Technology Origin Rival_data",
    "Standards exposure": "Inventions Dates Standards",
}
fig, ax = plt.subplots(figsize=(12, 6.2))
for r, (q, need) in enumerate(NEEDS.items()):
    need = need.replace("_", " ")
    for c, b in enumerate(BLOCKS):
        on = b in need
        missing = c >= 6
        ax.scatter(c, r, s=210 if on else 34, color=(MID if missing else ACCENT) if on else EMPTY, zorder=2)
ax.set_xticks(range(len(BLOCKS)), BLOCKS, rotation=35, ha="left", color=INK, fontsize=11)
ax.xaxis.tick_top()
ax.set_yticks(range(len(NEEDS)), list(NEEDS), color=INK, fontsize=12)
ax.invert_yaxis()
ax.axvline(5.5, color=MUTED, lw=1, ls=(0, (4, 4)))
ax.axhline(5.5, color=MUTED, lw=1, ls=(0, (4, 4)))
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.text(2.5, 10.05, "In my table", ha="center", color=ACCENT, fontweight="bold", fontsize=11)
ax.text(7.5, 10.05, "Not collected yet", ha="center", color=MID, fontweight="bold", fontsize=11)
ax.set_ylim(10.3, -.6)
fig.tight_layout()
fig.savefig(IMG / "question_data_matrix.png", dpi=150)
