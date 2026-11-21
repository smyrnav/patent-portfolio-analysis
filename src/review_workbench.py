"""Patent Review Workbench: walk a stratified sample and label patents one by one.

Closes the gap between make_blind_sheet.py (prints text) and the scored CSV
(needs labels): the reviewer sees each patent's own independent claims and
description paragraph with company names hidden, assigns a category, a
confidence, an evidence quote and a note; every decision is saved at once,
so the session can be stopped and resumed. The company and pool tags stay
hidden until the export step joins the answers back to the slot list.

Usage:
    python3 src/review_workbench.py review \
        --slots data/validation/satcom_retest_slots.csv \
        --stage satcom-retest \
        --pages data/interim/claim_pages_retest \
        --out data/validation/my_annotations.csv \
        --annotator seyrin

    python3 src/review_workbench.py export \
        --annotations data/validation/my_annotations.csv \
        --out data/validation/my_firstpass.csv

Commands inside the review:
    next            show the next unlabelled patent (default: just press enter)
    back            re-label the previous patent
    goto <n>        jump to entry number n
    skip            leave this one for the end
    skipped         show how many were skipped, then walk through them again
    status          how many done, skipped, remaining
    help            show the category meanings again
    quit            save and exit
"""
import argparse
import csv
import datetime
import json
import random
import re
import sys
import textwrap
from pathlib import Path

from common import DEPENDENT_RE, ROOT, rows, scrub

CATEGORIES = ["SAT", "ISL", "GRD", "NET", "SEC", "OTHER", "MULTI"]
CATEGORY_HELP = {
    "SAT": "satellite communications: payloads, beams, links, satellite radio technology",
    "ISL": "links between satellites, including free-space optical terminals (rule R4)",
    "GRD": "ground segment: gateways, ground stations, user terminals",
    "NET": "network integration: 5G/NTN procedures, handovers, timing, core network",
    "SEC": "security for satellite links: anti-jam, encryption, secure access",
    "OTHER": "does not belong to satellite communications at all",
    "MULTI": "genuinely spans several categories; you will name the components",
}
CONFIDENCE = {"h": "High", "m": "Medium", "l": "Low"}
FIELDS = ["blind_number", "annotator", "label", "multi_components", "confidence",
          "evidence", "reason", "status", "reviewed_at"]
EXPORT_FIELDS = ["blind_number", "first_pass_label", "multi_components", "confidence", "reason"]


def independent_claims(record):
    return [c for c in record.get("ind", []) if not DEPENDENT_RE.search(c[:250])]


class Session:
    """Which entries exist, which are labelled, and where the answers live."""

    def __init__(self, slots_path, stage, pages_folder, out_path, annotator):
        self.pages = json.loads((ROOT / pages_folder / "parsed.json").read_text())
        slots = rows(slots_path)
        # Same ordering as make_blind_sheet.py: blind numbers match the printed
        # sheet and the key_<stage>.json file, so exports join cleanly.
        ids = sorted({s["publication_number"] for s in slots if s["stage"] == stage})
        ids = [i for i in ids if i in self.pages and independent_claims(self.pages[i])]
        random.Random(f"blind-{stage}").shuffle(ids)
        self.ids = ids
        self.out = ROOT / out_path
        self.annotator = annotator
        self.annotations = {}
        if self.out.exists():
            for row in csv.DictReader(self.out.open(newline="", encoding="utf-8")):
                self.annotations[row["blind_number"]] = row

    def state(self, number):
        row = self.annotations.get(str(number))
        return row["status"] if row else "open"

    def next_open(self, start=1, status="open"):
        for n in range(max(1, start), len(self.ids) + 1):
            if self.state(n) == status:
                return n
        return None

    def record(self, number, label, multi, confidence, evidence, reason):
        row = {
            "blind_number": str(number),
            "annotator": self.annotator,
            "label": label,
            "multi_components": multi,
            "confidence": confidence,
            "evidence": evidence,
            "reason": reason,
            "status": "done",
            "reviewed_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self.annotations[str(number)] = row
        with self.out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            for n in range(1, len(self.ids) + 1):
                if str(n) in self.annotations:
                    writer.writerow(self.annotations[str(n)])

    def mark_skipped(self, number):
        self.record(number, "", "", "", "", "")
        self.annotations[str(number)]["status"] = "skipped"
        self._rewrite()

    def _rewrite(self):
        with self.out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            for n in range(1, len(self.ids) + 1):
                if str(n) in self.annotations:
                    writer.writerow(self.annotations[str(n)])

    def counts(self):
        done = sum(1 for n in range(1, len(self.ids) + 1) if self.state(n) == "done")
        skipped = sum(1 for n in range(1, len(self.ids) + 1) if self.state(n) == "skipped")
        return done, skipped, len(self.ids) - done - skipped


def show(session, number):
    record = session.pages[session.ids[number - 1]]
    print(f"\n{'=' * 100}\nentry #{number} of {len(session.ids)}  (company hidden)")
    for i, claim in enumerate(independent_claims(record), 1):
        print(f"\n-- independent claim {i} " + "-" * 60)
        print(textwrap.fill(scrub(re.sub(r"^\d+\s*\.\s*", "", claim)), 100))
    desc = record.get("desc", "")
    if desc:
        print("\n-- description, first paragraph " + "-" * 48)
        print(textwrap.fill(scrub(desc), 100))
    print("-" * 100)


def ask_category():
    print("\ncategories:")
    for c in CATEGORIES:
        print(f"  {c:6s} {CATEGORY_HELP[c]}")
    while True:
        label = input("category (or skip/back/goto/quit): ").strip().upper()
        if label in ("SKIP", "BACK", "QUIT", "STATUS", "HELP", "SKIPPED") or label.startswith("GOTO"):
            return label, ""
        if label in CATEGORIES:
            multi = ""
            if label == "MULTI":
                parts = input("components, comma-separated (SAT/ISL/GRD/NET/SEC): ").strip().upper()
                multi = "+".join(p.strip() for p in parts.split(",") if p.strip() in CATEGORIES[:-2])
            return label, multi
        print("  not a category; type HELP to see them again")


def review(args):
    session = Session(args.slots, args.stage, args.pages, args.out, args.annotator)
    done, skipped, remaining = session.counts()
    print(f"{len(session.ids)} entries in the sample; {done} labelled, {skipped} skipped, {remaining} open.")
    current = session.next_open()
    revisit = False
    while current is not None:
        show(session, current)
        label, multi = ask_category()
        if label == "QUIT":
            break
        if label == "STATUS":
            print("done / skipped / open:", session.counts())
            continue
        if label == "HELP":
            continue
        if label.startswith("GOTO"):
            try:
                current = max(1, min(len(session.ids), int(label.split()[1])))
            except (IndexError, ValueError):
                print("  goto needs a number, e.g. goto 42")
            continue
        if label == "BACK":
            current = max(1, current - 1)
            continue
        if label == "SKIP":
            session.mark_skipped(current)
        else:
            confidence = ""
            while confidence not in CONFIDENCE:
                confidence = input("confidence h/m/l: ").strip().lower()
            evidence = input("evidence: paste the phrase from the patent that decided it: ").strip()
            reason = input("one-line reason, or a boundary question for the log: ").strip()
            session.record(current, label, multi, CONFIDENCE[confidence], evidence, reason)
            print("  saved.")
        nxt = session.next_open(current + 1)
        if nxt is None and not revisit:
            nxt = session.next_open(0, "skipped")
            if nxt is not None:
                print("\nEnd of the open entries. Now the ones you skipped.")
                revisit = True
        current = nxt
    done, skipped, remaining = session.counts()
    print(f"\nsession saved to {args.out}: {done} labelled, {skipped} skipped, {remaining} open.")


def export(args):
    annotations = list(csv.DictReader((ROOT / args.annotations).open(newline="", encoding="utf-8")))
    with (ROOT / args.out).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPORT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in sorted(annotations, key=lambda r: int(r["blind_number"])):
            if row["status"] == "done":
                writer.writerow({"blind_number": row["blind_number"],
                                 "first_pass_label": row["label"],
                                 "multi_components": row["multi_components"],
                                 "confidence": row["confidence"],
                                 "reason": row["reason"]})
    print(f"exported the labelled entries to {args.out} in the first-pass format used by the scoring step")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    rev = sub.add_parser("review", help="interactive labelling session")
    rev.add_argument("--slots", required=True, help="slot list CSV, e.g. data/validation/satcom_retest_slots.csv")
    rev.add_argument("--stage", required=True, help="stage name in the slots file, e.g. satcom-retest")
    rev.add_argument("--pages", required=True, help="folder with parsed.json from fetch_claims.py")
    rev.add_argument("--out", required=True, help="annotations CSV, created or resumed")
    rev.add_argument("--annotator", required=True, help="your name, stored with every decision")
    rev.set_defaults(func=review)
    exp = sub.add_parser("export", help="write the first-pass CSV used by the scoring step")
    exp.add_argument("--annotations", required=True)
    exp.add_argument("--out", required=True)
    exp.set_defaults(func=export)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
