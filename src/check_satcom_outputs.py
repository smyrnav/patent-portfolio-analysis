"""Check that the satcom validation outputs agree with each other and with the rules.

Reads the files written by score_satcom_validation.py (defaults: the retest
cycle) and fails loudly if the join, the precision table, the confusion
matrix or the review-share table drift apart or break the codebook rules.
"""
from common import config, rows

CFG = config()
CLASSES = set(CFG["scope"]["all_classes"])
CONFIDENCE = set(CFG["validation"]["confidence_levels"]) | {"Med"}
BAR = CFG["validation"]["precision_bar"]

scored = rows("data/validation/satcom_retest_scored.csv")
slots = {r["publication_number"]: r for r in rows("data/validation/satcom_retest_slots.csv") if r["stage"] == "satcom-retest"}
precision = rows("data/validation/satcom_retest_results_precision.csv")
confusion = rows("data/validation/satcom_retest_results_confusion.csv")
review = rows("data/validation/satcom_retest_results_review.csv")


def check(label, actual, expected):
    if actual != expected:
        raise SystemExit(f"FAILED {label}: got {actual}, expected {expected}")
    print(f"ok  {label}: {actual}")


check("every scored publication exists in the slot list",
      all(r["publication_number"] in slots for r in scored), True)
check("blind numbers are 1..n with no gaps",
      sorted(int(r["blind_number"]) for r in scored), list(range(1, len(scored) + 1)))
check("every label is a codebook class", {r["first_pass_label"] for r in scored} <= CLASSES, True)
check("every confidence level is allowed", {r["confidence"] for r in scored} <= CONFIDENCE, True)

combined = next(r for r in precision if r["segment"] == "combined")
check("combined row counts the scored file", int(combined["sampled"]), len(scored))
check("combined matches recount in-pool flags", int(combined["matches"]), sum(int(r["in_combined_pool"]) for r in scored))
check("combined precision equals matches over sampled",
      float(combined["precision"]), round(int(combined["matches"]) / int(combined["sampled"]), 3))
check("passes_bar agrees with the bar", combined["passes_bar"] == "True", float(combined["precision"]) >= BAR)

for row in [r for r in precision if r["segment"] in ("company", "period", "pool_of_origin")]:
    group = [s for s in scored if s[row["segment"] if row["segment"] != "pool_of_origin" else "pools_matched"] == row["name"]]
    check(f"{row['segment']} {row['name']}: sampled", int(row["sampled"]), len(group))
    check(f"{row['segment']} {row['name']}: matches", int(row["matches"]), sum(int(s["in_combined_pool"]) for s in group))

check("confusion rows add up to their labelled totals",
      all(sum(int(r[c]) for c in CLASSES) == int(r["labelled"]) for r in confusion), True)
check("confusion labelled totals equal the precision samples",
      sorted(int(r["labelled"]) for r in confusion),
      sorted(int(r["sampled"]) for r in precision if r["segment"] == "pool_of_origin"))

total = next(r for r in review if r["name"] == "all")
check("review table counts the scored file", int(total["sampled"]), len(scored))
check("review share never exceeds 100%", all(0 <= float(r["review_share"]) <= 1 for r in review), True)
check("per-company review samples add up to the total",
      sum(int(r["sampled"]) for r in review if r["name"] != "all"), int(total["sampled"]))

print("All satcom validation outputs agree.")
