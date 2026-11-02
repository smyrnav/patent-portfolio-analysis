"""Sort the second query's names into company lineages and combine them with the first."""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/lineage_counts.csv"
OUT = ROOT / "data/interim/lineage_mapping.csv"
FIRST = ROOT / "data/interim/owner_mapping.csv"

UNRELATED = re.compile(r"MEDICAL|LUCENT SKY|TRANS ELECTRONIC|ADVANCED MAT|BIOSCIENCES|LUCENT OPTICS")
REVIEW = re.compile(r"LUCENT KK|^TRT ")


def company_lineage(name: str) -> str:
    upper = name.upper()
    if UNRELATED.search(upper):
        return "Not Nokia (unrelated Lucent names)"
    if REVIEW.search(upper):
        return "Needs review"
    if "INFINERA" in upper:
        return "Infinera"
    if upper.startswith("LUCENT"):
        return "Lucent"
    if "ALCATEL" in upper:
        return "Alcatel and Alcatel-Lucent"
    return "Unresolved"


def main() -> None:
    with RAW.open(newline="") as f:
        rows = [(r["owner"], int(r["granted_patents"])) for r in csv.DictReader(f)]
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["owner", "granted_patents", "company_lineage"])
        w.writerows((n, c, company_lineage(n)) for n, c in rows)

    combined, names = Counter(), Counter()
    for n, c in rows:
        lineage = company_lineage(n)
        combined[lineage] += c
        names[lineage] += 1
    with FIRST.open(newline="") as f:
        for r in csv.DictReader(f):
            combined[r["company_lineage"]] += int(r["granted_patents"])
            names[r["company_lineage"]] += 1
    kept = {k: v for k, v in combined.items() if not k.startswith("Not Nokia")}
    total = sum(kept.values())
    print(f"names={sum(names.values())} kept listings={total}")
    for k, v in sorted(combined.items(), key=lambda x: -x[1]):
        print(f"{k:38} names={names[k]:3} listings={v:6} share={v / total * 100:5.1f}%")
    print("Alcatel + Lucent listing share (origins overlap):", round((combined["Alcatel and Alcatel-Lucent"] + combined["Lucent"]) / total * 100, 1))


if __name__ == "__main__":
    main()
