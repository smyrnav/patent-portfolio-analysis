"""Draw the satcom validation re-test: precision vs the 85% bar, with 95% Wilson ranges.

Reads data/validation/satcom_retest_results_precision.csv (written by
score_satcom_validation.py) and saves docs/img/satcom_validation_precision.png.
"""
from pathlib import Path

import matplotlib.pyplot as plt

from common import ROOT, config, rows

OUT = ROOT / "docs/img/satcom_validation_precision.png"
BAR = config()["validation"]["precision_bar"]
ACCENT, PASS, FAIL, INK, MUTED = "#124191", "#2E7D32", "#C62828", "#1A1A1A", "#6B7686"

precision = rows("data/validation/satcom_retest_results_precision.csv")


def take(segment, names):
    out = []
    for r in precision:
        if r["segment"] == segment and (names is None or r["name"] in names):
            out.append((r["name"], float(r["precision"]), float(r["low_95"]), float(r["high_95"]), int(r["sampled"])))
    return out


panels = [
    "By pool of origin",
    [take("combined", None)[0]] + take("pool_of_origin", {"SAT", "NET", "SAT,NET", "ISL"}),
    "By company",
    take("company", {"Nokia (lineage)", "Thales", "Airbus", "Viasat", "Eutelsat/OneWeb"}),
    "By code position",
    take("code_position", None),
]

fig, axes = plt.subplots(1, 3, figsize=(15, 5.2), sharex=True)
for ax, title, data in zip(axes, panels[0::2], panels[1::2]):
    labels = [d[0].replace(" (lineage)", "") for d in data]
    values = [d[1] for d in data]
    errors = [[v - lo for _, v, lo, _, _ in data], [hi - v for _, v, _, hi, _ in data]]
    colors = [PASS if v >= BAR else FAIL for _, v, _, _, _ in data]
    y = range(len(data))
    ax.barh(y, values, xerr=errors, color=colors, alpha=.85, height=.62,
            error_kw={"ecolor": MUTED, "capsize": 4, "lw": 1.2})
    ax.axvline(BAR, color=INK, ls="--", lw=1.2)
    ax.set_yticks(list(y), [f"{l}  (n={n})" for l, (_, _, _, _, n) in zip(labels, data)], fontsize=10)
    for yi, v in enumerate(values):
        ax.text(min(v + .015, 1.0), yi, f"{v:.0%}", va="center", fontsize=10, fontweight="bold", color=INK)
    ax.set_xlim(0, 1.05)
    ax.set_title(title, fontsize=13, fontweight="bold", color=INK, pad=10)
    ax.invert_yaxis()
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel("share of sampled patents that are genuinely satcom", fontsize=9.5, color=MUTED)

fig.suptitle("Re-test, 13 Nov 2026: the combined pool fails the 85% bar — so no company comparison may graduate yet",
             fontsize=14.5, fontweight="bold", color=INK, y=1.0)
axes[1].text(BAR + .01, -.62, f"bar = {BAR:.0%}", fontsize=9.5, color=INK)
fig.tight_layout(rect=[0, 0, 1, .94])
fig.savefig(OUT, dpi=150, bbox_inches="tight")
print(f"saved {OUT}")
