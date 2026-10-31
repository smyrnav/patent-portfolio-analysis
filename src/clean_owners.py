"""Sort the raw owner names into company families and flag likely typos."""
import csv
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/owner_counts.csv"
OUT = ROOT / "data/processed/owner_mapping.csv"

NOT_NOKIA = re.compile(r"\bNOKIAN\b")
REVIEW = re.compile(
    r"TCL|VACUUM|OPTRONICS|KABEL|ALCATEL CABLE|FIBRES|ESPACE|TELSPACE|MOBILE COMM|"
    r"RADIOTELEPHONE|SUBMARCOM|TRANSP SOLUTION|ALSTHOM|ALSTHOLM|COMMISSARIAT|INRIA"
)
SIEMENS = re.compile(r"S[IE]{2}M[EA]NS")
BELL = re.compile(r"SHANGH[AI]{2} BELL")
TYPO_SIMILARITY = 0.88
ESTABLISHED_NAME = 20


def family(name: str) -> str:
    upper = name.upper()
    if NOT_NOKIA.search(upper):
        return "Not Nokia (Nokian Tyres)"
    if REVIEW.search(upper):
        return "Needs review"
    if BELL.search(upper):
        return "Shanghai Bell"
    if SIEMENS.search(upper):
        return "Nokia Siemens Networks"
    if "ALCATEL" in upper:
        return "Alcatel and Alcatel-Lucent"
    return "Nokia"


def main() -> None:
    with RAW.open(newline="") as f:
        rows = [(r["owner"], int(r["granted_patents"])) for r in csv.DictReader(f)]

    established = [n for n, c in rows if c >= ESTABLISHED_NAME]
    out = []
    for name, count in rows:
        match, score = "", 0.0
        if count < ESTABLISHED_NAME:
            for candidate in established:
                s = SequenceMatcher(None, name.upper(), candidate.upper()).ratio()
                if s > score:
                    match, score = candidate, s
        typo = score >= TYPO_SIMILARITY
        out.append((name, count, family(name), match if typo else "", round(score, 2) if typo else ""))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["owner", "granted_patents", "family", "likely_variant_of", "similarity"])
        w.writerows(out)

    names, listings = Counter(), Counter()
    for _, count, fam, *_ in out:
        names[fam] += 1
        listings[fam] += count
    print(f"{len(out)} names, {sum(listings.values())} listings")
    for fam, total in listings.most_common():
        print(f"{fam:30} names={names[fam]:3} listings={total}")
    print("likely variants:", sum(1 for r in out if r[3]), "covering", sum(r[1] for r in out if r[3]))
    groups = defaultdict(list)
    for r in out:
        groups[r[2]].append(r[0])
    print("Needs review:", groups["Needs review"])


if __name__ == "__main__":
    main()
