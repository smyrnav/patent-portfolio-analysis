"""Sort the second query's names into families and combine them with the first."""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/lineage_counts.csv"
OUT = ROOT / "data/processed/lineage_mapping.csv"
FIRST = ROOT / "data/processed/owner_mapping.csv"

UNRELATED = re.compile(r"MEDICAL|LUCENT SKY|TRANS ELECTRONIC|ADVANCED MAT|BIOSCIENCES|LUCENT OPTICS")
REVIEW = re.compile(r"LUCENT KK|^TRT ")


def family(name: str) -> str:
    upper = name.upper()
    if UNRELATED.search(upper):
        return "Not Nokia (unrelated Lucent names)"
    if REVIEW.search(upper):
        return "Needs review"
    if "INFINERA" in upper:
        return "Infinera"
    if upper.startswith("LUCENT"):
        return "Lucent"
    return "Alcatel and Alcatel-Lucent"


def main() -> None:
    with RAW.open(newline="") as f:
        rows = [(r["owner"], int(r["granted_patents"])) for r in csv.DictReader(f)]
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["owner", "granted_patents", "family"])
        w.writerows((n, c, family(n)) for n, c in rows)

    combined, names = Counter(), Counter()
    for n, c in rows:
        combined[family(n)] += c
        names[family(n)] += 1
    with FIRST.open(newline="") as f:
        for r in csv.DictReader(f):
            combined[r["family"]] += int(r["granted_patents"])
            names[r["family"]] += 1
    kept = {k: v for k, v in combined.items() if not k.startswith("Not Nokia")}
    total = sum(kept.values())
    print(f"names={sum(names.values())} kept listings={total}")
    for k, v in sorted(combined.items(), key=lambda x: -x[1]):
        print(f"{k:38} names={names[k]:3} listings={v:6} share={v / total * 100:5.1f}%")
    print("Alcatel + Lucent share:", round((combined["Alcatel and Alcatel-Lucent"] + combined["Lucent"]) / total * 100, 1))


if __name__ == "__main__":
    main()
