"""Check that the saved results agree with each other and with the figures in the docs."""
from common import config, rows

CFG = config()
FEES = CFG["us_fees_large_entity_usd"]


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
status_by_label = {r["status"]: r for r in status}
grant_status = status_by_label["Granted within 20 years"]
grant_evidence = int(grant_status["families"])
check("US families in status and office results match", int(grant_status["with_us_in_term"]), offices["US"])
check("no office has more families than the grant-evidence total", max(offices.values()) <= grant_evidence, True)

check("US kind codes match granted US applications, within 1", abs(sum(kinds.values()) - int(filings["US"]["granted_applications"])) <= 1, True)

total = {r["label"]: int(r["patents"]) for r in recount if r["row_type"] == "total"}
origin = {r["label"]: int(r["patents"]) for r in recount if r["row_type"] == "origin"}
names = sorted((int(r["patents"]) for r in recount if r["row_type"] == "name"), reverse=True)
check("unique US publications", total["Unique patents"], 36630)
check("owner-publication listings", total["Listings"], 37710)
check("summed origin counts", sum(origin.values()), 36866)
check("listings are at least unique patents", total["Listings"] >= total["Unique patents"], True)
# Origin rows overlap: a publication with multiple origins appears in each row.
# The distinct Alcatel/Lucent union cannot be recovered from this CSV and needs
# the corrected publication-level SQL in sql/08_recount_us_30y.sql to be rerun.
check("origin sum is at least the unique count", sum(origin.values()) >= total["Unique patents"], True)
check("each origin count is at most the unique count", all(v <= total["Unique patents"] for v in origin.values()), True)
check("Alcatel/Lucent diagnostic numerator does not exceed summed origins", origin["Alcatel and Alcatel-Lucent"] + origin["Lucent"] <= sum(origin.values()), True)
check("top 10 names' share of owner-publication listings, %", round(sum(names[:10]) / total["Listings"] * 100), 93)

check("break-even at 11.5 years and 10%, $", round(FEES["year_11_5"] / annuity(0.10, 20 - 4.05 - 11.5)), 2395)
check("break-even at 3.5 years and 10%, $", round(FEES["year_3_5"] / annuity(0.10, 4)), 678)
years = rows("data/processed/office_filings_by_year.csv")
check("new families by year add up to all families", sum(int(r["new_families"]) for r in years), int(table["families"]))
check("Japanese filings since 2010", sum(int(r["jp_applications"]) for r in years if int(r["year"]) >= 2010), 4376)
fin = rows("data/processed/nokia_financials_by_year.csv")
check("financial years covered", len(fin), 20)


def fee_spread(rates):
    alive, paid, spread = 1.0, 0, []
    for rate, fee in zip(rates, (FEES["year_3_5"], FEES["year_7_5"], FEES["year_11_5"])):
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
inv = {r["scope"][:5] + r["company"]: r for r in rows("data/processed/commercial_context.csv")}
net = inv["NetwoNokia"]
check("Nokia segment R&D share, %", round(float(net["rnd_m"]) / float(net["sales_m"]) * 100, 1), 18.4)
precision = {(r["pool"], r["company"]): r for r in rows("data/validation/results_precision.csv")}
for pool, matched in (("OPT", 73), ("IPR", 39), ("DCS", 21), ("DCS-H04L49", 42)):
    r = precision[(pool, "All")]
    check(f"{pool} claims match the class", (int(r["labelled"]), int(r["claims_match"])), (100, matched))
slots = rows("data/validation/validation_slots.csv")
check("test unique patents", len({s["publication_number"] for s in slots if s["stage"] == "test"}), 343)
check("pilot unique patents", len({s["publication_number"] for s in slots if s["stage"] == "pilot"}), 78)
check("slots in pilot and test", (sum(s["stage"] == "pilot" for s in slots), sum(s["stage"] == "test" for s in slots)), (90, 400))
assignee = {r["company"]: r for r in rows("data/validation/results_current_assignee.csv")}
check("Nokia other assignee", (int(assignee["Nokia"]["other_assignee"]), int(assignee["Nokia"]["unique_patents"])), (42, 179))
others = [r for c, r in assignee.items() if c != "Nokia"]
check("others' other assignee", (sum(int(r["other_assignee"]) for r in others), sum(int(r["unique_patents"]) for r in others)), (2, 242))
kept = {(r["pool"], r["company"]): int(r["est_families_mid"]) for r in rows("data/validation/results_estimates_current_assignee.csv")}
check("Nokia estimates without other assignees", (kept[("OPT", "Nokia")], kept[("IPR", "Nokia")], kept[("DCS-H04L49", "Nokia")]), (633, 202, 26))
check("agreement sheet patents", len(rows("data/validation/agreement_sheet.csv")), 60)
print("All checks passed.")
