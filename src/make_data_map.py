"""Draw the map of what the publications table contains."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "docs/img/data_map.png"
ACCENT, MUTED, INK, CARD = "#124191", "#6B7686", "#1A1A1A", "#F2F4F8"
USED = {"publication_number", "application_number", "country_code", "kind_code", "filing_date",
        "family_id", "grant_date", "assignee_harmonized"}
CARDS = [
    ("Identity", "Which patent, which office, which type?",
     ["publication_number", "application_number", "country_code", "kind_code", "application_kind",
      "application_number_formatted", "pct_number", "family_id", "spif_publication_number",
      "spif_application_number"]),
    ("Dates", "When was it filed and granted?",
     ["priority_date", "filing_date", "publication_date", "grant_date"]),
    ("People and owners", "Who invented it, and whose name is on it?",
     ["assignee", "assignee_harmonized", "inventor", "inventor_harmonized", "examiner"]),
    ("Technology codes", "What kind of technology is it?",
     ["cpc", "ipc", "uspc", "fi", "fterm", "locarno"]),
    ("Written content", "What does it actually say?",
     ["title_localized", "abstract_localized", "claims_localized", "claims_localized_html",
      "description_localized", "description_localized_html"]),
    ("Links", "What is it connected to?",
     ["citation", "priority_claim", "parent", "child"]),
    ("Office details", "How did the patent office handle it?",
     ["entity_status", "art_unit"]),
]
W, H, GAP = 3.35, 3.6, .2
fig, ax = plt.subplots(figsize=(14.4, 8.3))
ax.set_xlim(0, 4 * W + 3 * GAP)
ax.set_ylim(0, 2 * H + GAP + 1.05)
ax.axis("off")
ax.text(0, 2 * H + GAP + .72, "What the Google patents table contains", fontsize=20, fontweight="bold", color=INK)
ax.text(0, 2 * H + GAP + .3, "37 fields in 7 groups. Blue, bold fields are the 8 I have analysed so far.", fontsize=13, color=MUTED)
for i, (title, question, fields) in enumerate(CARDS):
    x = (i % 4) * (W + GAP)
    y = H + GAP if i < 4 else 0
    ax.add_patch(FancyBboxPatch((x + .05, y + .05), W - .1, H - .1, boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc=CARD, ec="none"))
    ax.text(x + .2, y + H - .32, title, fontsize=14, fontweight="bold", color=INK)
    ax.text(x + .2, y + H - .62, question, fontsize=10, color=MUTED)
    for j, f in enumerate(fields):
        used = f in USED
        ax.text(x + .2, y + H - 1.0 - j * .255, f, fontsize=10.5, family="DejaVu Sans Mono",
                color=ACCENT if used else INK, fontweight="bold" if used else "normal")
x = 3 * (W + GAP)
ax.text(x + .05, H - .32, "Not in this table", fontsize=14, fontweight="bold", color=INK)
for j, t in enumerate(["Revenue or licence deals", "Nokia's internal costs", "Renewal payments",
                       "Whether a patent is still alive", "The current owner, reliably",
                       "Whether it's essential to 5G"]):
    ax.text(x + .05, H - .78 - j * .36, "×  " + t, fontsize=11.5, color=INK)
fig.tight_layout(pad=.6)
fig.savefig(OUT, dpi=150)
