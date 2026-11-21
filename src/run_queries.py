"""Run a numbered sql/NN_*.sql query against BigQuery and save the result locally.

Closes the manual gap between BigQuery and the Python pipeline:
dry-run first (shows the bytes to be scanned), a billed-bytes cap on every
run, CSV output to the manifest-recorded path, and a sha256 fingerprint
appended to data/source_manifest.csv.

Usage:
    python3 src/run_queries.py 37                 dry-run, confirm, run, save, fingerprint
    python3 src/run_queries.py 37 --yes           skip the confirmation prompt
    python3 src/run_queries.py 37 --out data/raw/x.csv   override the output path
    python3 src/run_queries.py 37 --max-bytes 50000000000   raise the billed-bytes cap
    python3 src/run_queries.py --list             known queries and their output paths
    python3 src/run_queries.py --rebuild-sandbox  recreate expired sandbox tables (queries 06, 24)

Big queries stay on demand: nothing here runs all 36 queries, and the
billed-bytes cap refuses oversized scans unless explicitly raised.
"""
import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from build_manifest import fingerprint
from common import ROOT

DEFAULT_MAX_BILLED = 200 * 10**9  # 200 GB per query
GOOGLE_SOURCE = "patents-public-data.patents.publications"
SANDBOX_TABLES = ["portfolio_30y", "satcom_peers_30y"]
SANDBOX_BUILDERS = ["sql/06_create_portfolio_30y.sql", "sql/24_satcom_peers_30y.sql"]


def bq_bin():
    sdk_bin = Path.home() / "google-cloud-sdk" / "bin"
    # bq shells out to gcloud for authentication, so the SDK bin dir must be on PATH.
    os.environ["PATH"] = f"{sdk_bin}:{os.environ['PATH']}"
    found = shutil.which("bq")
    if found:
        return found
    if (sdk_bin / "bq").exists():
        return str(sdk_bin / "bq")
    raise SystemExit("bq not found on PATH or under ~/google-cloud-sdk/bin")


def query_file(number):
    matches = sorted((ROOT / "sql").glob(f"{int(number):02d}_*.sql"))
    if not matches:
        raise SystemExit(f"no sql/{int(number):02d}_*.sql found")
    return matches[0]


def clean_sql(path):
    """bq chokes on whole-line -- comments; strip them."""
    return "\n".join(line for line in path.read_text().splitlines() if not line.strip().startswith("--"))


def is_ddl(sql_text):
    return re.match(r"\s*(CREATE|DROP)\b", sql_text, re.I) is not None


def source_label(sql_text):
    if "patents-public-data" in sql_text:
        return GOOGLE_SOURCE
    if "nokia_analytics" in sql_text:
        return "nokia_analytics sandbox tables"
    return "unknown, check the query"


def manifest_output(query_path):
    """Output path recorded in the manifest for this query, else data/raw/<stem>.csv."""
    manifest = ROOT / "data" / "source_manifest.csv"
    if manifest.exists():
        for row in csv.DictReader(manifest.open(newline="", encoding="utf-8")):
            if row["produced_by"] == f"sql/{query_path.name}":
                return row["snapshot"]
    return f"data/raw/{query_path.stem}.csv"


def update_manifest(query_path, snapshot, source):
    manifest = ROOT / "data" / "source_manifest.csv"
    rows = list(csv.DictReader(manifest.open(newline="", encoding="utf-8"))) if manifest.exists() else []
    entry = {
        "produced_by": f"sql/{query_path.name}",
        "snapshot": snapshot,
        "source": source,
        "sha256": fingerprint(snapshot),
    }
    key = entry["produced_by"]
    if any(r["produced_by"] == key for r in rows):
        rows = [entry if r["produced_by"] == key else r for r in rows]
    else:
        rows.append(entry)
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["produced_by", "snapshot", "source", "sha256"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def dry_run_bytes(bq, sql_text):
    proc = subprocess.run([bq, "query", "--dry_run", "--use_legacy_sql=false", sql_text],
                          capture_output=True, text=True)
    message = proc.stdout + proc.stderr
    if proc.returncode != 0:
        raise SystemExit(f"dry-run failed:\n{message}")
    match = re.search(r"process (\d+) bytes", message)
    return int(match.group(1)) if match else None


def run_query(number, out, max_bytes, assume_yes):
    path = query_file(number)
    sql_text = clean_sql(path)
    snapshot = out or manifest_output(path)
    bq = bq_bin()

    scanned = dry_run_bytes(bq, sql_text)
    human = f"{scanned / 10**9:.1f} GB" if scanned is not None else "unknown size"
    print(f"query:  sql/{path.name}")
    print(f"scan:   {human} (cap {max_bytes / 10**9:.0f} GB)")
    if scanned is not None and scanned > max_bytes:
        raise SystemExit("dry-run exceeds the billed-bytes cap; raise it with --max-bytes if you mean it")
    if is_ddl(sql_text):
        print("type:   table builder (no CSV output)")
    else:
        print(f"output: {snapshot}")
    if not assume_yes and input("run it? [y/N] ").strip().lower() != "y":
        raise SystemExit("aborted, nothing was billed")

    if is_ddl(sql_text):
        subprocess.run([bq, "query", "--use_legacy_sql=false", sql_text], check=True)
        print("table rebuilt.")
        return

    with (ROOT / snapshot).open("w", encoding="utf-8") as f:
        subprocess.run([bq, "query", "--use_legacy_sql=false", "--format=csv",
                        f"--maximum_bytes_billed={max_bytes}", "--max_rows=100000", sql_text],
                       check=True, stdout=f)
    update_manifest(path, snapshot, source_label(sql_text))
    print(f"saved {snapshot} and fingerprinted it in data/source_manifest.csv")


def rebuild_sandbox(max_bytes, assume_yes):
    bq = bq_bin()
    for table in SANDBOX_TABLES:
        alive = subprocess.run([bq, "show", f"nokia_analytics.{table}"],
                               capture_output=True).returncode == 0
        print(f"nokia_analytics.{table}: {'exists' if alive else 'MISSING'}")
    for builder in SANDBOX_BUILDERS:
        path = ROOT / builder
        sql_text = clean_sql(path)
        scanned = dry_run_bytes(bq, sql_text)
        human = f"{scanned / 10**9:.1f} GB" if scanned is not None else "unknown size"
        print(f"build {builder}: will scan {human}")
        if scanned is not None and scanned > max_bytes:
            print(f"  skipped: exceeds the {max_bytes / 10**9:.0f} GB cap, raise with --max-bytes")
            continue
        if assume_yes or input("  run it? [y/N] ").strip().lower() == "y":
            subprocess.run([bq, "query", "--use_legacy_sql=false", sql_text], check=True)
            print(f"  {builder} done")
        else:
            print("  skipped by user")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("number", nargs="?", help="query number to run, e.g. 37")
    parser.add_argument("--out", help="override the output CSV path")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BILLED,
                        help=f"billed-bytes cap per query (default {DEFAULT_MAX_BILLED // 10**9} GB)")
    parser.add_argument("--yes", action="store_true", help="skip confirmation prompts")
    parser.add_argument("--list", action="store_true", help="list queries and their output paths")
    parser.add_argument("--rebuild-sandbox", action="store_true",
                        help="check and recreate the sandbox tables (queries 06 and 24)")
    args = parser.parse_args()

    if args.list:
        for path in sorted((ROOT / "sql").glob("[0-9]*_*.sql")):
            print(f"{path.stem.split('_')[0]}  sql/{path.name}  ->  {manifest_output(path)}")
        return
    if args.rebuild_sandbox:
        rebuild_sandbox(args.max_bytes, args.yes)
        return
    if args.number is None:
        parser.error("give a query number, --list or --rebuild-sandbox")
    run_query(args.number, args.out, args.max_bytes, args.yes)


if __name__ == "__main__":
    main()
