"""Fetch all Prozorro tender search results for a text query (default: Starlink).

The portal search endpoint is POST https://prozorro.gov.ua/api/search/tenders
with query parameters. It caps any search at 1,000 results (page > 50 is
rejected and per_page is fixed at 20), so a broad query cannot be paged
directly. This script works around the cap by splitting the notice-date range
into shards small enough that each stays under 1,000 hits, paging each shard,
and deduplicating by tenderID.

Usage:
    python3 src/fetch_prozorro_tenders.py                 # text=Starlink
    python3 src/fetch_prozorro_tenders.py --text "супутниковий інтернет"

Output: data/raw/prozorro_<slug>_tenders.csv (flat table) and
data/raw/prozorro_<slug>_tenders.json (raw items as returned), plus a printed
shard summary. Stdlib only. Be polite: the script sleeps between requests.
"""
import argparse
import datetime
import json
import re
import time
import urllib.parse
import urllib.request

from common import ROOT, write_rows

API = "https://prozorro.gov.ua/api/search/tenders"
TENDER_PAGE = "https://prozorro.gov.ua/tender/"
MAX_TOTAL = 1000          # server-side cap per search
PAUSE = 1.0               # seconds between requests
FIELDS = "tenderID title buyer status amount currency vat_included notice_start enquiry_end tender_end link".split()


def fetch(text, page, start=None, end=None):
    params = {"text": text, "page": page}
    if start:
        params["date[notice][start]"] = start.isoformat()
        params["date[notice][end]"] = end.isoformat()
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, method="POST", data=b"",
                                 headers={"User-Agent": "research-project (patent-portfolio-analysis)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def shard(text, start, end, depth=0):
    """Yield (start, end) ranges whose totals fit under the cap."""
    total = fetch(text, 1, start, end).get("total", 0)
    print(f"{'  ' * depth}{start} .. {end}: {total}")
    time.sleep(PAUSE)
    if total == 0:
        return
    if total < MAX_TOTAL:
        yield start, end, total
        return
    mid = start + (end - start) / 2
    if (end - start).days < 2:  # single day over the cap: take the first 1,000 and flag it
        print(f"{'  ' * depth}WARNING: {start} alone has {total}+ results; only the first {MAX_TOTAL} are retrievable")
        yield start, end, total
        return
    yield from shard(text, start, mid, depth + 1)
    yield from shard(text, mid + datetime.timedelta(days=1), end, depth + 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--text", default="Starlink")
    parser.add_argument("--since", default="2021-01-01", help="earliest notice date, YYYY-MM-DD")
    parser.add_argument("--until", default=datetime.date.today().isoformat())
    args = parser.parse_args()

    start = datetime.date.fromisoformat(args.since)
    end = datetime.date.fromisoformat(args.until)

    found = {}
    raw = {}
    capped_shards = 0
    for s, e, total in shard(text=args.text, start=start, end=end):
        if total >= MAX_TOTAL:
            capped_shards += 1
        for page in range(1, 51):
            data = fetch(args.text, page, s, e).get("data", [])
            time.sleep(PAUSE)
            for t in data:
                tid = t.get("tenderID")
                if tid in found:
                    continue
                raw[tid] = t
                found[tid] = (
                    tid,
                    (t.get("title") or "").replace("\n", " "),
                    (t.get("procuringEntity") or {}).get("name", ""),
                    t.get("status", ""),
                    (t.get("value") or {}).get("amount", ""),
                    (t.get("value") or {}).get("currency", ""),
                    (t.get("value") or {}).get("valueAddedTaxIncluded", ""),
                    (t.get("enquiryPeriod") or {}).get("startDate", ""),
                    (t.get("enquiryPeriod") or {}).get("endDate", ""),
                    (t.get("tenderPeriod") or {}).get("endDate", ""),
                    TENDER_PAGE + tid,
                )
            if len(data) < 20:
                break

    slug = re.sub(r"[^a-z0-9]+", "_", args.text.lower()).strip("_")
    out = f"data/raw/prozorro_{slug}_tenders.csv"
    out_json = f"data/raw/prozorro_{slug}_tenders.json"
    write_rows(ROOT / out, FIELDS, sorted(found.values()))
    (ROOT / out_json).write_text(json.dumps(list(raw.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(found)} unique tenders -> {out} (+ raw JSON {out_json})")
    if capped_shards:
        print(f"WARNING: {capped_shards} single-day shard(s) hit the {MAX_TOTAL}-result cap; some tenders may be missing")


if __name__ == "__main__":
    main()
