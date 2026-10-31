"""Download Nokia's annual 20-F reports and structured financial data from SEC EDGAR."""
import argparse
import csv
import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path

CIK = "0000924613"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/raw/annual_reports"
MANIFEST = ROOT / "data/raw/annual_reports_manifest.csv"
AGENT = os.environ.get("SEC_USER_AGENT")


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    time.sleep(0.2)  # SEC asks for no more than 10 requests per second
    return data


def filings():
    base = "https://data.sec.gov/submissions/"
    index = json.loads(fetch(f"{base}CIK{CIK}.json"))
    pages = [index["filings"]["recent"]]
    pages += [json.loads(fetch(base + f["name"])) for f in index["filings"].get("files", [])]
    for page in pages:
        for row in zip(page["form"], page["filingDate"], page["reportDate"], page["accessionNumber"], page["primaryDocument"]):
            yield row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=20, help="number of annual reports, newest first")
    args = parser.parse_args()
    if not AGENT:
        raise SystemExit('The SEC requires a contact. Run: SEC_USER_AGENT="Your Name you@example.com" python3 src/download_annual_reports.py')
    OUT.mkdir(parents=True, exist_ok=True)

    reports = sorted((f for f in filings() if f[0] == "20-F"), key=lambda f: f[1], reverse=True)[: args.count]
    rows = []
    for form, filed, period, accession, document in reports:
        if not document:  # very old filings can lack a listed main document
            document = f"{accession}.txt"
        url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{accession.replace('-', '')}/{document}"
        path = OUT / f"nokia_20f_filed{filed[:4]}{Path(document).suffix}"
        data = fetch(url)
        path.write_bytes(data)
        rows.append([period[:4] or filed[:4], period, filed, accession, url, path.name, len(data), hashlib.sha256(data).hexdigest()])
        print(f"Period {period or 'unlisted'}  filed {filed}  {len(data) / 1e6:.1f} MB  {path.name}")

    facts = fetch(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json")
    (OUT / "nokia_companyfacts.json").write_bytes(facts)
    print(f"Company facts  {len(facts) / 1e6:.1f} MB")

    with MANIFEST.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fiscal_year", "period_end", "filed", "accession", "url", "file", "bytes", "sha256"])
        writer.writerows(rows)


if __name__ == "__main__":
    main()
