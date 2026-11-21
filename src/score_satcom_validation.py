"""Score a satcom validation cycle: join blind labels back to the slot list and report.

Inputs: a slots CSV (stage, company, period, pools_matched, matched_codes,
first_code), the blind key JSON from make_blind_sheet.py, and a first-pass
labels CSV (from review_workbench.py export or the assistant's blind pass).

Outputs, all under --out-prefix (default: the retest files):
    <prefix>_scored.csv             one row per blind entry, with the join
    <prefix>_results_precision.csv  precision with 95% Wilson ranges, for the
                                    combined pool and by pool-of-origin, company,
                                    period and code position
    <prefix>_results_confusion.csv  pool-of-origin tag x human label counts
    <prefix>_results_review.csv     share of entries still needing human review

Usage:
    python3 src/score_satcom_validation.py \
        --slots data/validation/satcom_retest_slots.csv \
        --stage satcom-retest \
        --key data/interim/claim_pages_retest/key_satcom-retest.json \
        --firstpass data/validation/satcom_retest_firstpass.csv

The defaults reproduce the 13 November 2026 re-test; a new validation cycle
passes its own --slots/--key/--firstpass and its own --out-prefix.
"""
import argparse
import collections
import json

from common import config, ROOT, rows, wilson, write_rows

CFG = config()
IN_POOL = set(CFG["scope"]["all_classes"]) - {"OTHER"}
BAR = CFG["validation"]["precision_bar"]
POOLS = CFG["retrieval_pools"]
SAT_PREFIXES = [p for k, v in POOLS.items() if not k.endswith(("_exclude", "_security")) for p in v]
SAT_EXCLUDE = POOLS.get("SAT_exclude", [])


def pool_code(code):
    """True if a CPC code is one of the satellite prefixes that define the pools."""
    return any(code.startswith(p) for p in SAT_PREFIXES) and not any(code.startswith(p) for p in SAT_EXCLUDE)


def load_join(slots_path, stage, key_path, firstpass_path):
    slots = {r["publication_number"]: r for r in rows(slots_path) if r["stage"] == stage}
    key = json.loads((ROOT / key_path).read_text())
    labels = {int(r["blind_number"]): r for r in rows(firstpass_path)}
    scored = []
    for number, label in sorted(labels.items()):
        publication = key[number - 1]
        slot = slots[publication]
        first_is_pool = pool_code(slot["first_code"])
        scored.append({
            "blind_number": number,
            "publication_number": publication,
            "company": slot["company"],
            "period": slot["period"],
            "pools_matched": slot["pools_matched"],
            "first_pass_label": label["first_pass_label"],
            "multi_components": label.get("multi_components", ""),
            "confidence": label.get("confidence", ""),
            "in_combined_pool": int(label["first_pass_label"] in IN_POOL),
            "code_position": "first-listed" if first_is_pool else "secondary",
            "reason": label.get("reason", ""),
        })
    return scored


def precision_rows(scored):
    out = []

    def add(segment, name, group):
        n = len(group)
        matches = sum(r["in_combined_pool"] for r in group)
        low, high = wilson(matches, n)
        out.append((segment, name, n, matches, round(matches / n, 3), round(low, 3), round(high, 3),
                    BAR, matches / n >= BAR))

    add("combined", "all pools (primary, per R2)", scored)
    for tag in sorted({r["pools_matched"] for r in scored}):
        add("pool_of_origin", tag, [r for r in scored if r["pools_matched"] == tag])
    for company in sorted({r["company"] for r in scored}):
        add("company", company, [r for r in scored if r["company"] == company])
    for period in sorted({r["period"] for r in scored}):
        add("period", period, [r for r in scored if r["period"] == period])
    for position in ["first-listed", "secondary"]:
        group = [r for r in scored if r["code_position"] == position]
        if group:
            add("code_position", position, group)
    return out


def confusion_rows(scored):
    classes = CFG["scope"]["all_classes"]
    out = []
    for tag in sorted({r["pools_matched"] for r in scored}):
        group = [r for r in scored if r["pools_matched"] == tag]
        out.append((tag, *[sum(r["first_pass_label"] == c for r in group) for c in classes], len(group)))
    return out, classes


def review_rows(scored):
    """Entries still needing a human eye: not-High confidence, or a boundary flag in the reason."""
    out = []

    def add(name, group):
        n = len(group)
        low_conf = sum(r["confidence"] != "High" for r in group)
        boundary = sum("boundary" in r["reason"].lower() or "RE-READ" in r["reason"] for r in group)
        out.append((name, n, low_conf, round(low_conf / n, 3), boundary, round(boundary / n, 3)))

    add("all", scored)
    for company in sorted({r["company"] for r in scored}):
        add(company, [r for r in scored if r["company"] == company])
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slots", default="data/validation/satcom_retest_slots.csv")
    parser.add_argument("--stage", default="satcom-retest")
    parser.add_argument("--key", default="data/interim/claim_pages_retest/key_satcom-retest.json")
    parser.add_argument("--firstpass", default="data/validation/satcom_retest_firstpass.csv")
    parser.add_argument("--out-prefix", default="data/validation/satcom_retest")
    args = parser.parse_args()

    scored = load_join(args.slots, args.stage, args.key, args.firstpass)
    write_rows(f"{args.out_prefix}_scored.csv",
               "blind_number publication_number company period pools_matched first_pass_label multi_components confidence in_combined_pool code_position reason".split(),
               [tuple(r.values()) for r in scored])
    write_rows(f"{args.out_prefix}_results_precision.csv",
               "segment name sampled matches precision low_95 high_95 bar passes_bar".split(),
               precision_rows(scored))
    confusion, classes = confusion_rows(scored)
    write_rows(f"{args.out_prefix}_results_confusion.csv", ["pools_matched", *classes, "labelled"], confusion)
    write_rows(f"{args.out_prefix}_results_review.csv",
               "name sampled not_high_confidence review_share boundary_flagged boundary_share".split(),
               review_rows(scored))

    combined = precision_rows(scored)[0]
    verdict = "PASSES" if combined[-1] else "FAILS"
    print(f"combined pool precision: {combined[3]}/{combined[2]} = {combined[4]} "
          f"(95% range {combined[5]}-{combined[6]}) — {verdict} the {BAR} bar")


if __name__ == "__main__":
    main()
