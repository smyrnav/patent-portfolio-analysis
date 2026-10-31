"""Chart 20 years of reported finances against the patent data."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

ROOT = Path(__file__).resolve().parents[1]
ACCENT, MID, MUTED, LIGHT, INK = "#124191", "#5B7DB8", "#6B7686", "#C9D1DC", "#1A1A1A"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def rows(p):
    with (ROOT / p).open(newline="") as f:
        return list(csv.DictReader(f))


fin = rows("data/processed/nokia_financials_by_year.csv")
off = rows("data/processed/office_filings_by_year.csv")


def series(data, key, field):
    return [(int(r[key]), float(r[field])) for r in data if r[field]]


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:,.0f}")
    ax.xaxis.set_major_locator(MultipleLocator(3))
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}")
    ax.grid(axis="y", color="#E6EAF0", lw=.8)
    ax.set_axisbelow(True)


fig, axes = plt.subplots(2, 2, figsize=(14.5, 9.2))
fig.suptitle("Twenty years of Nokia's patents and money", x=.04, ha="left", fontsize=20, fontweight="bold")

ax = axes[0, 0]
x, y = zip(*series(fin, "fiscal_year", "reported_portfolio_families"))
ax.step(x, y, where="mid", color=ACCENT, lw=2.5)
ax.scatter(x, y, color=ACCENT, s=22, zorder=3)
ax.set_ylim(0, 31000)
ax.set_title("Reported portfolio: the Alcatel jump, then 20,000, then 26,000+", loc="left", fontweight="bold")
ax.annotate("Alcatel-Lucent\n26,000+", (2016, 26000), (2010.5, 27300), arrowprops=dict(arrowstyle="-", color=INK))
ax.annotate("26,000+\nFY2025", (2025, 26000), (2022.3, 27300), arrowprops=dict(arrowstyle="-", color=INK))
ax.text(2006, 2000, "Figures before 2016 cover different parts of the group. FY2024 not found.", color=MUTED, fontsize=10)
clean(ax)

ax = axes[0, 1]
x, y = zip(*series(fin, "fiscal_year", "licensing_unit_net_sales_eur_m"))
ax.bar(x, y, color=[ACCENT if v in (2017, 2024) else MID for v in x], width=.72)
ax.set_title("Licensing-unit net sales, €M: it moves with renewal cycles", loc="left", fontweight="bold")
ax.annotate("Catch-up\nabout €300M", (2017, 1654), (2013.2, 1760), arrowprops=dict(arrowstyle="-", color=INK))
ax.annotate("Renewal cycle:\n€1,085M, then €1,928M", (2024, 1928), (2018.2, 2010), arrowprops=dict(arrowstyle="-", color=INK))
ax.set_ylim(0, 2300)
clean(ax)

ax = axes[1, 0]
x, y = zip(*[(int(r["year"]), int(r["new_families"])) for r in off if 2006 <= int(r["year"]) <= 2024])
ax.plot(x, y, color=ACCENT, lw=2.5, label="New families in my data")
x2, y2 = zip(*series(fin, "fiscal_year", "reported_new_inventions"))
ax.scatter(x2, y2, color=INK, s=48, zorder=3, label='Nokia\'s reported "new inventions"')
ax.axvspan(2023, 2024, color=LIGHT, alpha=.4, lw=0)
ax.text(2023.5, 3150, "Provisional", ha="center", color=MUTED, fontsize=10)
ax.set_ylim(0, 3500)
ax.legend(frameon=False, loc="lower left")
ax.set_title("My data follows Nokia's own reported figures", loc="left", fontweight="bold")
clean(ax)

ax = axes[1, 1]
years = [int(r["year"]) for r in off if 2006 <= int(r["year"]) <= 2024]
pick = [r for r in off if 2006 <= int(r["year"]) <= 2024]
for key, label, color, ls in (("us_applications", "US", ACCENT, "-"), ("ep_applications", "Europe (EPO)", MID, "-"), ("cn_applications", "China", INK, "-"), ("jp_applications", "Japan", MUTED, "-")):
    vals = [int(r[key]) for r in pick]
    ax.plot(years, vals, color=color, lw=2.3, ls=ls)
    ax.text(2024.2, vals[-1], label, color=color, va="center", fontweight="bold")
ax.set_xlim(2006, 2027.5)
ax.axvspan(2023, 2024, color=LIGHT, alpha=.4, lw=0)
ax.set_title("Filings by office: China passes the US in 2024, provisionally", loc="left", fontweight="bold")
clean(ax)

fig.text(.04, .012, "Sources: Nokia 20-F reports and Google Patents data. Group changes break comparability in 2013 and 2016. Recent patent years are incomplete because of publication delay.", color=MUTED, fontsize=10)
fig.tight_layout(rect=(0, .035, 1, .95))
fig.savefig(ROOT / "docs/img/twenty_years.png", dpi=150)
