"""Fetch Prozorro portal search results: tenders, plans and contracts.

The portal search endpoints are POST https://prozorro.gov.ua/api/search/<kind>
with query parameters, no login needed. They cap any search at 1,000 results
(page > 50 is rejected and per_page is fixed at 20), so broad queries cannot be
paged directly. This module works around the cap:

- tenders and plans: split the date range (date[notice] / date[plan]) into
  shards small enough to stay under 1,000 hits, page each shard, deduplicate.
- contracts: the contracts endpoint accepts no working date filter, so instead
  every known tenderID is queried as the search text — contract IDs are the
  tender ID plus a suffix, so text=<tenderID> returns exactly that tender's
  contracts. Scope limit: only contracts of tenders in the given list.

Usage:
    python3 src/prozorro_extractor.py                          # tenders, text=Starlink
    python3 src/prozorro_extractor.py --kind plans
    python3 src/prozorro_extractor.py --kind contracts --from-tenders data/raw/prozorro_starlink_tenders.csv

Output per run: data/raw/prozorro_<slug>_<kind>.csv (flat table) and .json
(raw items as returned), plus a printed summary. Stdlib only. Be polite: the
script sleeps between requests.
"""
import argparse
import datetime
import json
import re
import time
import urllib.parse
import urllib.request

from common import ROOT, rows, write_rows

API = "https://prozorro.gov.ua/api/search"
PAGE = "https://prozorro.gov.ua"
MAX_TOTAL = 1000          # server-side cap per search
PAUSE = 1.0               # seconds between requests

KINDS = {
    "tenders": {
        "date_dim": "notice",
        "fields": "tenderID title buyer status amount currency vat_included notice_start enquiry_end tender_end link".split(),
    },
    "plans": {
        "date_dim": "plan",
        "fields": "planID description buyer status amount currency plan_start link".split(),
    },
    "contracts": {
        "date_dim": None,  # no working date filter; extraction goes per tenderID
        "fields": "contractID tenderID buyer suppliers status amount currency vat_included link".split(),
    },
}


def fetch(kind, text, page, start=None, end=None, date_dim=None):
    params = {"text": text, "page": page}
    if start and date_dim:
        params[f"date[{date_dim}][start]"] = start.isoformat()
        params[f"date[{date_dim}][end]"] = end.isoformat()
    url = f"{API}/{kind}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, method="POST", data=b"",
                                 headers={"User-Agent": "research-project (patent-portfolio-analysis)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def shard(kind, text, start, end, date_dim, depth=0):
    """Yield (start, end, total) ranges whose totals fit under the cap."""
    total = fetch(kind, text, 1, start, end, date_dim).get("total", 0)
    print(f"{'  ' * depth}{start} .. {end}: {total}")
    time.sleep(PAUSE)
    if total == 0:
        return
    if total < MAX_TOTAL:
        yield start, end, total
        return
    mid = start + (end - start) / 2
    if start == end:  # single day over the cap: take the first 1,000 and flag it
        print(f"{'  ' * depth}WARNING: {start} alone has {total}+ results; only the first {MAX_TOTAL} are retrievable")
        yield start, end, total
        return
    yield from shard(kind, text, start, mid, date_dim, depth + 1)
    yield from shard(kind, text, mid + datetime.timedelta(days=1), end, date_dim, depth + 1)


def row_from(kind, item, parent_tender_id=None):
    """Flatten one search-result item into a CSV row matching KINDS[kind]['fields']."""
    if kind == "tenders":
        tid = item.get("tenderID", "")
        return (tid,
                (item.get("title") or "").replace("\n", " "),
                (item.get("procuringEntity") or {}).get("name", ""),
                item.get("status", ""),
                (item.get("value") or {}).get("amount", ""),
                (item.get("value") or {}).get("currency", ""),
                (item.get("value") or {}).get("valueAddedTaxIncluded", ""),
                (item.get("enquiryPeriod") or {}).get("startDate", ""),
                (item.get("enquiryPeriod") or {}).get("endDate", ""),
                (item.get("tenderPeriod") or {}).get("endDate", ""),
                f"{PAGE}/tender/{tid}")
    if kind == "plans":
        pid = item.get("planID", "")
        return (pid,
                ((item.get("budget") or {}).get("description") or "").replace("\n", " "),
                (item.get("procuringEntity") or {}).get("name", ""),
                item.get("status", ""),
                (item.get("budget") or {}).get("amount", ""),
                (item.get("budget") or {}).get("currency", ""),
                (item.get("tender") or {}).get("tenderPeriod", {}).get("startDate", ""),
                f"{PAGE}/plan/{pid}")
    if kind == "contracts":
        cid = item.get("contractID", "")
        suppliers = "; ".join(s.get("name", "") for s in item.get("suppliers") or [])
        return (cid,
                parent_tender_id or "",
                (item.get("buyer") or {}).get("name", ""),
                suppliers,
                item.get("status", ""),
                (item.get("value") or {}).get("amount", ""),
                (item.get("value") or {}).get("currency", ""),
                (item.get("value") or {}).get("valueAddedTaxIncluded", ""),
                f"{PAGE}/contract/{cid}")
    raise ValueError(kind)


def extract(kind, text, start, end):
    """Fetch every search result for text between the dates start and end.

    Returns (rows, raw_items, capped_shards): unique flattened rows sorted by
    ID, the raw items keyed the same way, and the number of single-day shards
    that still exceeded the server cap (those days may be incomplete).
    """
    date_dim = KINDS[kind]["date_dim"]
    if not date_dim:
        raise ValueError(f"{kind} has no date filter; use extract_contracts_for_tenders")
    found = {}
    raw = {}
    capped_shards = 0
    for s, e, total in shard(kind, text, start, end, date_dim):
        if total >= MAX_TOTAL:
            capped_shards += 1
        for page in range(1, 51):
            data = fetch(kind, text, page, s, e, date_dim).get("data", [])
            time.sleep(PAUSE)
            for item in data:
                row = row_from(kind, item)
                if row[0] and row[0] not in found:
                    found[row[0]] = row
                    raw[row[0]] = item
            if len(data) < 20:
                break
    return sorted(found.values()), raw, capped_shards


def extract_contracts_for_tenders(tender_ids):
    """Fetch contracts for each known tenderID (see module docstring for why).

    Returns (rows, raw_items): unique contracts sorted by contractID and the
    raw items.
    """
    found = {}
    raw = {}
    for i, tid in enumerate(tender_ids, 1):
        page = 1
        while True:
            data = fetch("contracts", tid, page).get("data", [])
            time.sleep(PAUSE)
            for item in data:
                row = row_from("contracts", item, parent_tender_id=tid)
                if row[0] and row[0] not in found:
                    found[row[0]] = row
                    raw[row[0]] = item
            if len(data) < 20:
                break
            page += 1
        if i % 100 == 0:
            print(f"{i}/{len(tender_ids)} tenders checked, {len(found)} contracts so far")
    return sorted(found.values()), raw


CONTRACT_DETAIL_FIELDS = ("contractID tenderID status contractNumber dateSigned period_start period_end "
                          "amount amountNet currency buyer_name buyer_edrpou supplier_names supplier_edrpous "
                          "items_count items_summary cpv_codes delivery_regions documents link").split()


def fetch_contract_detail(contract_id):
    """Full contract record as the contract page itself loads it."""
    url = f"{API}/contracts/{urllib.parse.quote(contract_id)}"
    req = urllib.request.Request(url, headers={"User-Agent": "research-project (patent-portfolio-analysis)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def contract_detail_row(d):
    """Flatten one full contract record into a row matching CONTRACT_DETAIL_FIELDS."""
    items = d.get("items") or []
    suppliers = d.get("suppliers") or []
    period = d.get("period") or {}
    value = d.get("value") or {}

    def cpv_of(item):
        m = re.search(r"\d{8}-\d", (item.get("classification") or {}).get("description", ""))
        return m.group(0) if m else ""

    def item_text(item):
        unit = (item.get("unit") or {}).get("name", "")
        desc = (item.get("description") or "").replace("\n", " ")
        return f"{item.get('quantity', '')} {unit} — {desc}".strip()

    return (d.get("contractID", ""),
            d.get("tenderID", ""),
            d.get("status", ""),
            d.get("contractNumber") or "",
            d.get("dateSigned") or "",
            period.get("startDate", ""),
            period.get("endDate", ""),
            value.get("amount", ""),
            value.get("amountNet", ""),
            value.get("currency", ""),
            (d.get("buyer") or {}).get("name", ""),
            ((d.get("buyer") or {}).get("identifier") or {}).get("id", ""),
            "; ".join(s.get("name", "") for s in suppliers),
            "; ".join((s.get("identifier") or {}).get("id", "") for s in suppliers),
            len(items),
            " | ".join(item_text(i) for i in items),
            "; ".join(sorted({c for c in (cpv_of(i) for i in items) if c})),
            "; ".join(sorted({r for r in ((i.get("deliveryAddress") or {}).get("region", "") for i in items) if r})),
            len(d.get("publicDocuments") or []),
            f"{PAGE}/contract/{d.get('contractID', '')}")


def extract_contract_details(contract_ids):
    """Fetch the full record for every contractID. Returns (rows, raw_items)."""
    found = []
    raw = {}
    for i, cid in enumerate(contract_ids, 1):
        d = fetch_contract_detail(cid)
        time.sleep(PAUSE)
        found.append(contract_detail_row(d))
        raw[d.get("contractID", cid)] = d
        if i % 100 == 0:
            print(f"{i}/{len(contract_ids)} contract details fetched")
    return found, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind", choices=[*sorted(KINDS), "contract-details"], default="tenders")
    parser.add_argument("--text", default="Starlink")
    parser.add_argument("--since", default="2021-01-01", help="earliest date, YYYY-MM-DD")
    parser.add_argument("--until", default=datetime.date.today().isoformat())
    parser.add_argument("--from-tenders", help="contracts only: CSV with a tenderID column to extract contracts for")
    parser.add_argument("--from-contracts", help="contract-details only: CSV with a contractID column to fetch full records for")
    args = parser.parse_args()

    slug = re.sub(r"[^a-z0-9]+", "_", args.text.lower()).strip("_")
    out = f"data/raw/prozorro_{slug}_{args.kind.replace('-', '_')}.csv"
    out_json = f"data/raw/prozorro_{slug}_{args.kind.replace('-', '_')}.json"

    if args.kind == "contract-details":
        if not args.from_contracts:
            raise SystemExit("contract-details need --from-contracts <csv> with a contractID column")
        contract_ids = [r["contractID"] for r in rows(args.from_contracts)]
        print(f"fetching full records for {len(contract_ids)} contracts")
        rows_found, raw = extract_contract_details(contract_ids)
        write_rows(ROOT / out, CONTRACT_DETAIL_FIELDS, rows_found)
        (ROOT / out_json).write_text(json.dumps(raw, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n{len(rows_found)} contract details -> {out} (+ raw JSON {out_json})")
        return

    if args.kind == "contracts":
        if not args.from_tenders:
            raise SystemExit("contracts need --from-tenders <csv>: the contracts endpoint has no working date filter")
        tender_ids = [r["tenderID"] for r in rows(args.from_tenders)]
        print(f"extracting contracts for {len(tender_ids)} tenders")
        rows_found, raw = extract_contracts_for_tenders(tender_ids)
        capped_shards = 0
    else:
        rows_found, raw, capped_shards = extract(args.kind, args.text,
                                                 datetime.date.fromisoformat(args.since),
                                                 datetime.date.fromisoformat(args.until))

    write_rows(ROOT / out, KINDS[args.kind]["fields"], rows_found)
    (ROOT / out_json).write_text(json.dumps(list(raw.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(rows_found)} unique {args.kind} -> {out} (+ raw JSON {out_json})")
    if capped_shards:
        print(f"WARNING: {capped_shards} single-day shard(s) hit the {MAX_TOTAL}-result cap; some results may be missing")


if __name__ == "__main__":
    main()
