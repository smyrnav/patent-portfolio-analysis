"""Config-driven Prozorro research pipeline: many search queries in, one database out.

Reads config/prozorro_categories.yaml (categories x queries), runs every query
through prozorro_extractor's verified date-sharding search, deduplicates
globally by tenderID while keeping every matching category and query, then
fetches contracts, full contract records and tender summaries — each exactly
once. Every phase checkpoints to disk, so an interrupted run resumes where it
stopped and never redoes finished work.

    python3 src/prozorro_pipeline.py                     # full run
    python3 src/prozorro_pipeline.py --config my.yaml    # other taxonomy

Outputs (data/processed/prozorro_satellite_*):
    tenders.csv             one row per unique tender, with all matching categories/queries
    matches.csv             one row per ID x category x query match (tenders and contracts)
    contracts.csv           one row per unique contract: buyer, suppliers, value, status,
                            parent tender (derived from the contract ID), matching categories
    quality.csv             per-query shard/page/duplicate counts and incompleteness flags
    prozorro_satellite_research.xlsx   the same plus a market overview, one workbook
Stages: the default bulk run (stage 1) fetches everything via search only.
`--stage select` filters the contract base (config: selection) down to a
shortlist, and `--stage details` opens only those contracts one by one —
full records, items and EDRPOU codes, written to contract_details.csv and
tech_requirements.csv.
Raw API items accumulate as JSONL under data/raw/prozorro_pipeline/ for
reproducibility; checkpoints live in data/interim/prozorro_pipeline/.

Depends on PyYAML (config) and openpyxl (workbook); everything else is stdlib.
"""
import argparse
import datetime
import json
import sys
import time
import urllib.error

import prozorro_extractor as pe
from common import ROOT, rows, write_rows

STATE_DIR = ROOT / "data/interim/prozorro_pipeline"
RAW_DIR = ROOT / "data/raw/prozorro_pipeline"
OUT_PREFIX = "data/processed/prozorro_satellite"
CHECKPOINT = STATE_DIR / "checkpoint.json"

TENDER_FIELDS = ("tenderID title buyer status amount currency notice_start tender_end "
                 "categories queries n_contracts link").split()
MATCH_FIELDS = "kind id category query".split()
CONTRACT_FIELDS = [*pe.KINDS["contracts"]["fields"], "categories", "queries"]
SELECTED_FIELDS = "contractID tenderID buyer suppliers status amount currency categories queries link".split()
TECH_FIELDS = ("contractID tenderID buyer supplier item_description quantity unit cpv_code "
               "delivery_region amount currency link").split()
QUALITY_FIELDS = "phase key items pages shards capped_shards duplicates errors flag".split()

BACKOFF = (5, 20, 60)


def log(msg):
    print(msg, flush=True)


_REAL_FETCH = pe.fetch  # captured once; search_phase swaps pe.fetch for fetch_retry


def fetch_retry(kind, text, page, start=None, end=None, date_dim=None):
    """pe.fetch with retries and backoff; raises after the last attempt.

    Calls the captured original, never pe.fetch itself: search_phase points
    pe.fetch at this function so pe.shard gets retries too, and a lookup
    through pe.fetch here would recurse forever.
    """
    for attempt, wait in enumerate([0, *BACKOFF]):
        if wait:
            log(f"    retry in {wait}s ({kind} p{page})")
            time.sleep(wait)
        try:
            return _REAL_FETCH(kind, text, page, start, end, date_dim)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt == len(BACKOFF):
                raise
    raise AssertionError("unreachable")


def with_retries(fn, label):
    """Run fn() with the same backoff as fetch_retry; raises after the last attempt."""
    for attempt, wait in enumerate([0, *BACKOFF]):
        if wait:
            log(f"    retry in {wait}s ({label})")
            time.sleep(wait)
        try:
            return fn()
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt == len(BACKOFF):
                raise
    raise AssertionError("unreachable")


def load_checkpoint():
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())
    return {"queries": {}, "contracts": [], "details": [], "summaries": []}


def save_checkpoint(cp):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(json.dumps(cp, ensure_ascii=False, indent=1))


def append_jsonl(path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def read_jsonl(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def slugify(text):
    import re
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def query_key(category, query):
    return f"{category}|{query}"


def add_match(db, matches, category, query, item):
    """Merge one search item into the global dedup table. Returns True if new."""
    row = pe.row_from("tenders", item)
    tid = row[0]
    if not tid:
        return False
    matches.append(("tender", tid, category, query))
    if tid in db:
        entry = db[tid]
        entry["categories"].add(category)
        entry["queries"].add(query)
        return False
    db[tid] = {"row": row, "categories": {category}, "queries": {query}}
    return True


def search_phase(cfg, cp, quality):
    """Run every category query through the sharded search, checkpointing per query."""
    real_fetch = pe.fetch
    pe.fetch = fetch_retry  # sharding uses the module-level fetch; give it retries
    try:
        db, matches = {}, []
        start = datetime.date.fromisoformat(cfg["project"]["date_from"])
        end = datetime.date.fromisoformat(cfg["project"]["date_to"] or datetime.date.today().isoformat())
        for category, body in cfg["categories"].items():
            for query in body["queries"]:
                key = query_key(category, query)
                raw_path = RAW_DIR / f"tenders__{category}__{slugify(query)}.jsonl"
                if key in cp["queries"]:
                    log(f"skip (done): {key}")
                    items = read_jsonl(raw_path)
                    q = cp["queries"][key]
                    q["reused"] = True
                else:
                    log(f"search: {key}")
                    items, pages, shards, capped, errors = [], 0, 0, 0, 0
                    try:
                        for s, e, total in pe.shard("tenders", query, start, end, "notice"):
                            shards += 1
                            if total >= pe.MAX_TOTAL:
                                capped += 1
                            for page in range(1, 51):
                                data = fetch_retry("tenders", query, page, s, e, "notice").get("data", [])
                                pages += 1
                                time.sleep(pe.PAUSE)
                                items.extend(data)
                                if len(data) < 20:
                                    break
                    except Exception as exc:  # recorded, flagged, not hidden
                        errors = 1
                        log(f"  ERROR: {exc}")
                    append_jsonl(raw_path, items)
                    q = {"items": len(items), "pages": pages, "shards": shards,
                         "capped_shards": capped, "errors": errors}
                    if not errors:  # failed queries are NOT checkpointed: the next run retries them
                        cp["queries"][key] = q
                        save_checkpoint(cp)
                before = len(db)
                for item in items:
                    add_match(db, matches, category, query, item)
                quality.append(("search", key, len(items), q.get("pages"), q.get("shards"),
                                q.get("capped_shards"), len(items) - (len(db) - before),
                                q.get("errors"), "INCOMPLETE" if q.get("errors") or q.get("capped_shards") else ""))
        return db, matches
    finally:
        pe.fetch = real_fetch


def contracts_phase(cfg, cp, quality):
    """Bulk contract search per category query; dedup by contractID, keep every match.

    The contracts endpoint has no working date filter, so there is no sharding
    here: any query hitting the 1,000-result cap is flagged INCOMPLETE in the
    quality report instead of being silently treated as complete. The parent
    tender ID is derived from the contract ID (it is the tender ID plus a
    suffix), so no per-tender lookups are needed.
    """
    done_q = cp.setdefault("contract_queries", {})
    db, matches = {}, []
    for category, body in cfg["categories"].items():
        for query in body["queries"]:
            key = query_key(category, query)
            raw_path = RAW_DIR / f"contracts__{category}__{slugify(query)}.jsonl"
            if key in done_q:
                log(f"skip (done): contracts {key}")
                items = read_jsonl(raw_path)
                q = done_q[key]
            else:
                log(f"contracts search: {key}")
                items, pages, capped, errors = [], 0, 0, 0
                try:
                    page = 1
                    while True:
                        resp = fetch_retry("contracts", query, page)
                        data = resp.get("data", [])
                        total = resp.get("total", 0)
                        pages += 1
                        time.sleep(pe.PAUSE)
                        items.extend(data)
                        if len(data) < 20:
                            break
                    capped = 1 if total >= pe.MAX_TOTAL else 0
                except Exception as exc:
                    errors = 1
                    log(f"  ERROR: {exc}")
                append_jsonl(raw_path, items)
                q = {"items": len(items), "pages": pages, "capped": capped, "errors": errors}
                if not errors:  # failed queries are NOT checkpointed: the next run retries them
                    done_q[key] = q
                    save_checkpoint(cp)
            new = 0
            for item in items:
                cid = item.get("contractID")
                if not cid:
                    continue
                matches.append(("contract", cid, category, query))
                if cid in db:
                    db[cid]["categories"].add(category)
                    db[cid]["queries"].add(query)
                else:
                    db[cid] = {"item": item, "categories": {category}, "queries": {query}}
                    new += 1
            flag = "INCOMPLETE: over the 1,000-result cap" if q.get("capped") else ("INCOMPLETE: request failed" if q.get("errors") else "")
            quality.append(("contracts", key, len(items), q.get("pages"), "", q.get("capped", 0),
                            len(items) - new, q.get("errors"), flag))
    return db, matches


def details_phase(contract_ids, cp, quality):
    """Fetch the full record of every contract once; checkpoint per contract.

    Not part of the default pipeline run (per-record fetching was descoped);
    kept for targeted use: extract_contract_details in prozorro_extractor.
    """
    done = set(cp["details"])
    raw_path = RAW_DIR / "contract_details.jsonl"
    raw = {d["contractID"]: d for d in read_jsonl(raw_path)}
    errors = 0
    todo = [c for c in contract_ids if c not in done]
    for i, cid in enumerate(todo, 1):
        try:
            d = with_retries(lambda: pe.fetch_contract_detail(cid), cid)
            time.sleep(pe.PAUSE)
            append_jsonl(raw_path, [d])
            raw[d["contractID"]] = d
            done.add(cid)
        except Exception as exc:
            errors += 1
            log(f"  ERROR detail {cid}: {exc}")
        if i % 100 == 0:
            cp["details"] = sorted(done)
            save_checkpoint(cp)
            log(f"  details: {i}/{len(todo)}")
    cp["details"] = sorted(done)
    save_checkpoint(cp)
    quality.append(("details", "full contract records", len(raw), "", "", "", "", errors,
                    f"INCOMPLETE: {errors} record(s) failed" if errors else ""))
    return raw


def select_phase(cfg, quality):
    """Stage 2: filter the bulk contract base down to contracts worth opening.

    Reads the exported contracts.csv, keeps contracts matching the selection
    rules in the config (status, minimum amount), ranks by value and writes the
    shortlist that stage 3 opens one by one.
    """
    sel = cfg.get("selection", {})
    statuses = set(sel.get("contract_statuses", ["active", "terminated"]))
    min_amount = float(sel.get("min_amount", 0))
    top_n = int(sel.get("top_n", 50))

    kept = []
    for r in rows(f"{OUT_PREFIX}_contracts.csv"):
        if r["status"] not in statuses:
            continue
        try:
            amount = float(r["amount"])
        except (ValueError, TypeError):
            continue
        if amount < min_amount:
            continue
        kept.append((amount, r))
    kept.sort(key=lambda t: t[0], reverse=True)
    selected = kept[:top_n]
    write_rows(ROOT / f"{OUT_PREFIX}_selected.csv", SELECTED_FIELDS,
               [(r["contractID"], r["tenderID"], r["buyer"], r["suppliers"], r["status"],
                 r["amount"], r["currency"], r["categories"], r["queries"], r["link"]) for _, r in selected])
    quality.append(("select", f"statuses {sorted(statuses)}, top {top_n} by value",
                    len(kept), "", "", "", len(kept) - len(selected), 0, ""))
    log(f"stage 2: {len(kept)} contracts pass the filter, {len(selected)} shortlisted")
    return [r["contractID"] for _, r in selected]


def tech_rows_from(details):
    """One row per contracted item from full contract records (stage 3 output)."""
    tech_rows = []
    for d in details.values():
        suppliers = "; ".join(s.get("name", "") for s in d.get("suppliers") or [])
        for item in d.get("items") or []:
            m = pe.re.search(r"\d{8}-\d", (item.get("classification") or {}).get("description", ""))
            tech_rows.append((d.get("contractID", ""), d.get("tenderID", ""),
                              (d.get("buyer") or {}).get("name", ""), suppliers,
                              (item.get("description") or "").replace("\n", " "),
                              item.get("quantity", ""), (item.get("unit") or {}).get("name", ""),
                              m.group(0) if m else "",
                              (item.get("deliveryAddress") or {}).get("region", ""),
                              (d.get("value") or {}).get("amount", ""),
                              (d.get("value") or {}).get("currency", ""),
                              f"{pe.PAGE}/contract/{d.get('contractID', '')}"))
    return tech_rows


def summaries_phase(tender_ids, cp, quality):
    """Fetch the tender summary card once per tender; checkpoint per tender."""
    done = set(cp["summaries"])
    raw_path = RAW_DIR / "tender_summaries.jsonl"
    raw = {d["tenderID"]: d for d in read_jsonl(raw_path)}
    errors = 0
    todo = [t for t in tender_ids if t not in done]
    for i, tid in enumerate(todo, 1):
        try:
            def get_summary():
                url = f"{pe.API}/tenders/{tid}/summary"
                req = pe.urllib.request.Request(url, headers={"User-Agent": "research-project (patent-portfolio-analysis)"})
                with pe.urllib.request.urlopen(req, timeout=60) as r:
                    return json.load(r)
            d = with_retries(get_summary, tid)
            time.sleep(pe.PAUSE)
            append_jsonl(raw_path, [d])
            raw[d["tenderID"]] = d
            done.add(tid)
        except Exception as exc:
            errors += 1
            log(f"  ERROR summary {tid}: {exc}")
        if i % 100 == 0:
            cp["summaries"] = sorted(done)
            save_checkpoint(cp)
            log(f"  summaries: {i}/{len(todo)}")
    cp["summaries"] = sorted(done)
    save_checkpoint(cp)
    quality.append(("summaries", "tender cards", len(raw), "", "", "", "", errors,
                    f"INCOMPLETE: {errors} card(s) failed" if errors else ""))
    return raw


def export(db, matches, contracts_db, quality):
    import collections
    parent_of = {cid: pe.re.sub(r"-[a-z]\d+$", "", cid) for cid in contracts_db}
    n_by_tender = collections.Counter(parent_of.values())

    tender_rows = []
    for tid in sorted(db):
        e = db[tid]
        r = e["row"]
        tender_rows.append((tid, r[1], r[2], r[3], r[4], r[5], r[7], r[9],
                            "; ".join(sorted(e["categories"])), "; ".join(sorted(e["queries"])),
                            n_by_tender.get(tid, 0), r[10]))
    write_rows(ROOT / f"{OUT_PREFIX}_tenders.csv", TENDER_FIELDS, tender_rows)
    write_rows(ROOT / f"{OUT_PREFIX}_matches.csv", MATCH_FIELDS, sorted(set(matches)))

    contract_rows = []
    for cid in sorted(contracts_db):
        e = contracts_db[cid]
        base = pe.row_from("contracts", e["item"], parent_tender_id=parent_of[cid])
        contract_rows.append((*base, "; ".join(sorted(e["categories"])), "; ".join(sorted(e["queries"]))))
    write_rows(ROOT / f"{OUT_PREFIX}_contracts.csv", CONTRACT_FIELDS, contract_rows)

    write_rows(ROOT / f"{OUT_PREFIX}_quality.csv", QUALITY_FIELDS, quality)
    return tender_rows, contract_rows


def export_xlsx(tender_rows, matches, contract_rows, quality):
    """One workbook with the result sheets; skipped with a warning if openpyxl is missing."""
    try:
        import collections

        from openpyxl import Workbook
    except ImportError:
        log("openpyxl not installed; skipping the workbook (CSVs are complete)")
        return
    wb = Workbook()
    wb.remove(wb.active)

    def sheet(name, fields, rows_):
        ws = wb.create_sheet(name)
        ws.append(list(fields))
        for row in rows_:
            ws.append([str(v) for v in row])

    sheet("All Tenders", TENDER_FIELDS, tender_rows)
    sheet("Contracts", CONTRACT_FIELDS, contract_rows)
    sheet("Search Matches", MATCH_FIELDS, sorted(set(matches)))

    years = collections.Counter((r[0][3:7] or "unknown") for r in tender_rows)
    cats = collections.Counter()
    for r in tender_rows:
        for c in r[8].split("; "):
            if c:
                cats[c] += 1
    ws = wb.create_sheet("Market Overview")
    ws.append(["tenders by year (from tenderID)", "count"])
    for y, n in sorted(years.items()):
        ws.append([y, n])
    ws.append([])
    ws.append(["tenders by category", "count"])
    for c, n in cats.most_common():
        ws.append([c, n])

    sheet("Extraction Quality", QUALITY_FIELDS, quality)
    out = ROOT / f"{OUT_PREFIX}_research.xlsx"
    wb.save(out)
    log(f"workbook -> {out}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", default="config/prozorro_categories.yaml")
    parser.add_argument("--no-xlsx", action="store_true")
    parser.add_argument("--stage", choices=["pipeline", "select", "details", "all"], default="all",
                        help="pipeline = bulk search + exports; select = stage-2 filter; "
                             "details = stage-3 full records for the shortlist; all = everything")
    args = parser.parse_args()

    import yaml  # lazy: the rest of the repo is stdlib-only
    cfg = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8"))

    cp = load_checkpoint()
    quality = []

    if args.stage in ("pipeline", "all"):
        db, matches = search_phase(cfg, cp, quality)
        log(f"unique tenders: {len(db)} (matches: {len(matches)})")

        contracts_db, cmatches = contracts_phase(cfg, cp, quality)
        matches += cmatches
        log(f"unique contracts: {len(contracts_db)}")

        summaries_phase(sorted(db), cp, quality)

        tender_rows, contract_rows = export(db, matches, contracts_db, quality)
        if not args.no_xlsx:
            export_xlsx(tender_rows, matches, contract_rows, quality)
        print(f"\nstage 1 DONE: {len(db)} tenders, {len(contracts_db)} contracts")

    if args.stage in ("select", "all"):
        selected = select_phase(cfg, quality)
    else:
        selected = [r["contractID"] for r in rows(f"{OUT_PREFIX}_selected.csv")] if args.stage == "details" else []

    if args.stage in ("details", "all") and selected:
        details = details_phase(selected, cp, quality)
        write_rows(ROOT / f"{OUT_PREFIX}_contract_details.csv", pe.CONTRACT_DETAIL_FIELDS,
                   [pe.contract_detail_row(d) for d in details.values()])
        write_rows(ROOT / f"{OUT_PREFIX}_tech_requirements.csv", TECH_FIELDS, tech_rows_from(details))
        print(f"stage 3 DONE: {len(details)} contract detail records")

    write_rows(ROOT / f"{OUT_PREFIX}_quality.csv", QUALITY_FIELDS, quality)
    flagged = [q for q in quality if q[-1]]
    if flagged:
        print("INCOMPLETE segments (see quality.csv):")
        for q in flagged:
            print(f"  {q[1]}: {q[-1]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
