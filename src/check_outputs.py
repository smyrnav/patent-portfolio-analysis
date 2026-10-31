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

check("break-even at 11.5 years and 10%, $", round(8280 / annuity(0.10, 5.5)), 2030)
check("break-even at 3.5 years and 10%, $", round(2150 / annuity(0.10, 4)), 678)
print("All checks passed.")
