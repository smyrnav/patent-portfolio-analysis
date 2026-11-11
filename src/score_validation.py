"""Score the labelled samples: precision, confusion, review share, period balance, assignee check and agreement.

Input: data/validation/manual_labels.csv, validation_slots.csv, agreement_sheet.csv and codebook_sample.csv.
Output: data/validation/results_*.csv. Pool sizes for the H04L49-only pool come from codebook_sample_h04l49.csv.
"""
import collections
import re

from common import cohen_kappa, config, rows, wilson, write_rows

CFG = config()
labels = {r["publication_number"]: r for r in rows("data/validation/manual_labels.csv")}
slots = rows("data/validation/validation_slots.csv")
test = [s for s in slots if s["stage"] == "test"]
pool_size = {(r["pool"], r["company"]): int(r["pool_size"]) for r in rows("data/validation/codebook_sample.csv")}
pool_size.update({("DCS-H04L49", r["company"]): int(r["pool_size"]) for r in rows("data/validation/codebook_sample_h04l49.csv")})
target = {"OPT": "OPT", "IPR": "IPR", "DCS": "DCS", "DCS-H04L49": "DCS"}


def match(slot):
    return labels[slot["publication_number"]]["primary_class"] == target[slot["pool"]]


def other_assignee(publication):
    r = labels[publication]
    return not re.search(CFG["lineage_names"][r["company"]], r["google_patents_current_assignee"], re.I)


# Precision and estimated families, by pool and company
precision = []
pools = sorted({s["pool"] for s in test})
for pool in pools:
    in_pool = [s for s in test if s["pool"] == pool]
    for company in ["All"] + sorted({s["company"] for s in in_pool}):
        group = in_pool if company == "All" else [s for s in in_pool if s["company"] == company]
        m, n = sum(map(match, group)), len(group)
        low, high = wilson(m, n)
        size = pool_size.get((pool, company))
        est = (round(size * low), round(size * m / n), round(size * high)) if size else ("", "", "")
        precision.append((pool, company, size or "", n, m, round(m / n, 3), round(low, 3), round(high, 3), *est))
write_rows("data/validation/results_precision.csv",
           "pool company pool_size_us_families labelled claims_match precision low_95 high_95 est_families_low est_families_mid est_families_high".split(),
           precision)

# Confusion between classes: which class the claims earned, by retrieval pool
classes = CFG["pre_pivot"]["all_classes"]
write_rows("data/validation/results_confusion.csv", ["pool", *classes, "labelled"],
           [(pool, *[sum(labels[s["publication_number"]]["primary_class"] == c for s in test if s["pool"] == pool) for c in classes],
             sum(s["pool"] == pool for s in test)) for pool in pools])

# Share of records needing review, per stage, on unique patents
review = []
for stage in ("pilot", "test"):
    ids = {s["publication_number"] for s in slots if s["stage"] == stage}
    total = len(ids)
    for name, test_fn in (("MULTI", lambda r: r["primary_class"] == "MULTI"), ("Low confidence", lambda r: r["confidence"] == "Low"),
                          ("MULTI or low confidence", lambda r: r["primary_class"] == "MULTI" or r["confidence"] == "Low"),
                          ("Status pending", lambda r: r["review_status"] == "pending")):
        count = sum(test_fn(labels[i]) for i in ids)
        review.append((stage, name, count, total, round(count / total, 3)))
write_rows("data/validation/results_review_share.csv", "stage measure patents unique_patents share".split(), review)


# Period balance: the sample wasn't stratified by priority date, so show what it contains
def period(date):
    for low, high, name in CFG["validation"]["priority_periods"]:
        if low <= int(date) <= high:
            return name


names = [p[2] for p in CFG["validation"]["priority_periods"]]
balance = []
for pool in pools:
    for name in names:
        group = [s for s in test if s["pool"] == pool and period(labels[s["publication_number"]]["priority_date"]) == name]
        m = sum(map(match, group))
        balance.append((pool, name, len(group), m, round(m / len(group), 3) if group else ""))
write_rows("data/validation/results_period_balance.csv", "pool priority_period labelled claims_match precision".split(), balance)

# Current assignee on Google Patents, on unique patents across pilot and test
assignee = []
for company in sorted({r["company"] for r in labels.values()}):
    ids = [i for i, r in labels.items() if r["company"] == company]
    other = [i for i in ids if other_assignee(i)]
    top = collections.Counter(labels[i]["google_patents_current_assignee"] for i in other).most_common(3)
    assignee.append((company, len(ids), len(other), round(len(other) / len(ids), 3), "; ".join(f"{k} {v}" for k, v in top)))
write_rows("data/validation/results_current_assignee.csv", "company unique_patents other_assignee share largest".split(), assignee)

# Estimates limited to patents still showing a lineage name as current assignee
kept = []
for pool in ("OPT", "IPR", "DCS-H04L49"):
    for company in sorted({s["company"] for s in test}):
        group = [s for s in test if s["pool"] == pool and s["company"] == company]
        m = sum(match(s) and not other_assignee(s["publication_number"]) for s in group)
        kept.append((pool, company, pool_size[(pool, company)], len(group), m, round(pool_size[(pool, company)] * m / len(group))))
write_rows("data/validation/results_estimates_current_assignee.csv", "pool company pool_size_us_families labelled claims_match_and_lineage_assignee est_families_mid".split(), kept)

# Agreement between the first pass and the human labels
sheet = [r for r in rows("data/validation/agreement_sheet.csv") if r["my_label"].strip()]
pairs = [(labels[r["publication_number"]]["primary_class"], r["my_label"].strip().upper().replace("REVIEW", "MULTI")) for r in sheet]
result = (len(pairs), round(cohen_kappa(pairs), 3), "pass" if cohen_kappa(pairs) >= CFG["validation"]["kappa_bar"] else "fail") if len(pairs) == 60 else (len(pairs), "", "pending")
write_rows("data/validation/results_agreement.csv", "labelled_by_human kappa status".split(), [result])

print("Scored", len(test), "test slots on", len({s["publication_number"] for s in test}), "patents. Agreement:", result[2])
