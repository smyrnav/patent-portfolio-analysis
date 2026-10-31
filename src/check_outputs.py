"""Check that the saved results agree with each other and with the figures in the docs."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with (ROOT / path).open(newline="") as f:
        return list(csv.DictReader(f))


def annuity(rate, years):
    return (1 - (1 + rate) ** -years) / rate


def check(label, actual, expected):
    if actual != expected:
        raise SystemExit(f"FAILED {label}: got {actual}, expected {expected}")
    print(f"ok  {label}: {actual}")


table = rows("data/raw/portfolio_30y_check.csv")[0]
status = rows("data/processed/family_status.csv")
offices = {r["country_code"]: int(r["families"]) for r in rows("data/processed/in_term_by_office.csv")}
recount = rows("data/processed/us_30y_recount.csv")
kinds = {r["kind"]: int(r["patents"]) for r in rows("data/raw/us_kind_codes.csv")}
filings = {r["country_code"]: r for r in rows("data/raw/filings_by_country.csv")}

check("statuses add up to all families", sum(int(r["families"]) for r in status), int(table["families"]))
core = int(status[0]["families"])
check("US families in status and office results match", int(status[0]["with_us_in_term"]), offices["US"])
check("no office has more families than the core", max(offices.values()) <= core, True)

check("US kind codes match granted US applications, within 1", abs(sum(kinds.values()) - int(filings["US"]["granted_applications"])) <= 1, True)

total = {r["label"]: int(r["patents"]) for r in recount if r["row_type"] == "total"}
origin = {r["label"]: int(r["patents"]) for r in recount if r["row_type"] == "origin"}
names = sorted((int(r["patents"]) for r in recount if r["row_type"] == "name"), reverse=True)
check("listings are at least unique patents", total["Listings"] >= total["Unique patents"], True)
check("Alcatel and Lucent share, %", round((origin["Alcatel and Alcatel-Lucent"] + origin["Lucent"]) / sum(origin.values()) * 100), 46)
check("top 10 names' share of listings, %", round(sum(names[:10]) / total["Listings"] * 100), 93)

check("break-even at 11.5 years and 10%, $", round(8280 / annuity(0.10, 20 - 4.05 - 11.5)), 2395)
check("break-even at 3.5 years and 10%, $", round(2150 / annuity(0.10, 4)), 678)
check("sales per core family, €k", round(1217e6 / 9 * 12 / core / 1000), 82)
years = rows("data/processed/office_filings_by_year.csv")
check("new families by year add up to all families", sum(int(r["new_families"]) for r in years), int(table["families"]))
check("Japanese filings since 2010", sum(int(r["jp_applications"]) for r in years if int(r["year"]) >= 2010), 4376)
fin = rows("data/processed/nokia_financials_by_year.csv")
check("financial years covered", len(fin), 20)


def fee_spread(rates):
    alive, paid, spread = 1.0, 0, []
    for rate, fee in zip(rates, (2150, 4040, 8280)):
        spread.append((paid, alive * (1 - rate)))
        alive *= rate
        paid += fee
    spread.append((paid, alive))
    mean = sum(cost * share for cost, share in spread)
    running = 0
    for cost, share in spread:
        running += share
        if running >= 0.5:
            return round(mean), cost


check("mean and median fees at high renewal", fee_spread((0.9, 0.8, 0.7)), (9017, 14470))
check("mean and median fees at low renewal", fee_spread((0.8, 0.6, 0.4)), (5249, 2150))
inv = {r["scope"][:5] + r["company"]: r for r in rows("data/processed/investment_position.csv")}
net = inv["NetwoNokia"]
check("Nokia segment R&D share, %", round(float(net["rnd_m"]) / float(net["sales_m"]) * 100, 1), 18.4)
print("All checks passed.")
