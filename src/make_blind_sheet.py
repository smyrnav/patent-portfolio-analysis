"""Print a blind labelling sheet: claims only, shuffled, with company, pool, title and codes hidden.

Usage: python src/make_blind_sheet.py <stage> [first_claim_chars] [other_claim_chars] [folder] [slots_csv]
"""
import json
import random
import re
import sys
from pathlib import Path

from common import ROOT, rows

stage = sys.argv[1]
first_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 700
other_chars = int(sys.argv[3]) if len(sys.argv) > 3 else 150
folder = Path(sys.argv[4]) if len(sys.argv) > 4 else ROOT / "data/interim/claim_pages"
slots = sys.argv[5] if len(sys.argv) > 5 else "data/validation/validation_slots.csv"
parsed = json.loads((folder / "parsed.json").read_text())
ids = sorted({s["publication_number"] for s in rows(slots) if s["stage"] == stage})
missing = [i for i in ids if i not in parsed or not parsed[i]["ind"]]
if missing:
    print(f"Skipped {len(missing)} publications with no readable claims: {missing}", file=sys.stderr)
ids = [i for i in ids if i not in missing]
random.Random(f"blind-{stage}").shuffle(ids)
dependent = re.compile(r"\b(of|to|in|by|with|from|under|per)\s+(any\s+(one\s+)?of\s+)?(the\s+)?(preceding\s+)?claims?\s+\d+", re.I)
companies = re.compile(r"\b(nokia|alcatel|lucent|infinera|airbus|astrium|thales|viasat|inmarsat|eutelsat|oneweb|one\s*web|worldvu|iceye|spacex|space\s*x|starlink|boeing|qualcomm|globalstar)\b", re.I)


def scrub(text):
    return companies.sub("[company]", text)


for number, publication in enumerate(ids, 1):
    claims = [c for c in parsed[publication]["ind"] if not dependent.search(c[:250])]
    first = re.sub(r"^\d+\s*\.\s*", "", claims[0]) if claims else ""
    shown = first if len(first) <= first_chars else f"{first[:int(first_chars * .6)]} [...] {first[-int(first_chars * .4):]}"
    print(f"#{number} {scrub(shown)}")
    for claim in claims[1:3]:
        print(f"  +{scrub(re.sub(r'^[0-9]+ *[.] *', '', claim)[:other_chars])}")
    desc = parsed[publication].get("desc", "")
    if desc:
        print(f"  ~{scrub(desc[:400])}")
(folder / f"key_{stage}.json").write_text(json.dumps(ids))
