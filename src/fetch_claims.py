"""Download Google Patents pages for the validation sample and extract independent claims.

Usage: python src/fetch_claims.py [folder] [slots_csv]. Pages and the parsed file stay local,
in data/interim/claim_pages by default; slots default to data/validation/validation_slots.csv.
"""
import concurrent.futures as cf
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

from common import ROOT, rows

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/interim/claim_pages"
PAGES = OUT / "html"


def urls(publication):
    bare = publication.replace("-", "")
    yield bare
    country, number, _kind = publication.split("-", 2)
    if country == "US" and number[:4].isdigit() and int(number[:4]) >= 2001:
        yield f"US{number[:4]}{number[4:].zfill(7)}{_kind}"


def get(publication):
    path = PAGES / f"{publication}.html"
    if path.exists() and path.stat().st_size > 5000:
        return None
    for candidate in urls(publication):
        url = f"https://patents.google.com/patent/{candidate}/en"
        for _ in range(3):
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                path.write_text(urllib.request.urlopen(request, timeout=60).read().decode("utf8", "ignore"))
                time.sleep(0.5)
                return None
            except OSError:
                time.sleep(3)
    return publication


def parse(page):
    first = [html.unescape(x).strip() for x in re.findall(r'itemprop="assigneeOriginal"[^>]*>([^<]*)', page)]
    current = [html.unescape(x).strip() for x in re.findall(r'itemprop="assigneeCurrent"[^>]*>\s*([^<]*)', page)]
    section = re.search(r'<section itemprop="claims".*?</section>', page, re.S)
    independent = []
    if section:
        for m in re.finditer(r'<div[^>]*class="claim(-dependent)?"[^>]*>(.*?)(?=<div[^>]*class="claim(?:-dependent)?"|</section>)', section.group(0), re.S):
            text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
            if not m.group(1) and len(text) > 20:
                independent.append(text)
        if not independent:
            for m in re.finditer(r'<claim\b[^>]*>(.*?)</claim>', section.group(0), re.S):
                text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip()
                if len(text) > 20:
                    independent.append(text)
    desc = ""
    dsec = re.search(r'<section itemprop="description".*?</section>', page, re.S)
    if dsec:
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", dsec.group(0)))).strip()
        desc = re.sub(r"^(description|technical field|field of the invention|background)[:\s]*", "", text, flags=re.I)[:800]
    return {"orig": first, "cur": current, "ind": independent, "desc": desc}


if __name__ == "__main__":
    PAGES.mkdir(parents=True, exist_ok=True)
    slots = sys.argv[2] if len(sys.argv) > 2 else "data/validation/validation_slots.csv"
    ids = sorted({s["publication_number"] for s in rows(slots)})
    with cf.ThreadPoolExecutor(4) as pool:
        failed = [x for x in pool.map(get, ids) if x]
    parsed = {p: parse((PAGES / f"{p}.html").read_text()) for p in ids if (PAGES / f"{p}.html").exists()}
    (OUT / "parsed.json").write_text(json.dumps(parsed, ensure_ascii=False))
    print(f"Parsed {len(parsed)} of {len(ids)} pages. Failed: {failed}")
