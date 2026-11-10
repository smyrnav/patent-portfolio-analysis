"""First-pass review of the satcom actor name census (query 23).

Reads data/raw/satcom_actor_names.csv and sorts every name variant into
keep / drop / review with a written reason, producing
data/interim/satcom_name_review.csv. It then emits
sql/24_satcom_peers_30y.sql built only from the names marked keep.

Design decision: names identify the corporate group (whole Thales group,
whole Airbus group), because division-level filtering by name is
unreliable. Relevance to satellite communications comes from the
technology-pool classification later, not from the name list.
"review" rows are excluded from the generated SQL until a human decides.
"""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/satcom_actor_names.csv"
OUT = ROOT / "data/interim/satcom_name_review.csv"
SQL = ROOT / "sql/24_satcom_peers_30y.sql"

EADS_WORD = re.compile(r"\bEADS\b")
EADS_SUBSTRING_JUNK = re.compile(r"LEAD|HEAD|READ|THREAD|SPREAD|BEAD|BEDSTEAD|MEAD|NEAD|KNEAD|DEADSHOT|ADS")
# Chinese "Thales" companies whose affiliation with the Thales group is unconfirmed.
THALES_UNCONFIRMED = re.compile(r"^(XIAMEN THALES|XIAN THALES|SHANGHAI THALES ELECTRON|SHANGHAI ELECTRICAL THALES)")


def classify(bucket: str, name: str):
    u = name.upper()
    if bucket == "ICEYE":
        if u.startswith("ICEYE OY") or u.startswith("ICEYE INC"):
            return "keep", "ICEYE", "ICEYE parent (Finland) or US subsidiary"
        if u.startswith("ICEYE POLSKA"):
            return "keep", "ICEYE", "Polish subsidiary, spelling variants"
        if "CHANGSHA" in u:
            return "review", "", "Chinese company sharing the name; no known ICEYE link"
        return "drop", "", "ICEYE is a substring of an unrelated name"
    if bucket == "Viasat":
        if "YINMARSAT" in u:
            return "drop", "", "name coincidence, not Inmarsat"
        if u.startswith("VIASAT"):
            return "keep", "Viasat", "Viasat entity or filing typo of one"
        if u.startswith("INMARSAT"):
            return "keep", "Viasat", "Inmarsat, merged into Viasat in 2023"
        return "review", "", "unclassified Viasat-bucket name"
    if bucket == "Eutelsat/OneWeb":
        if u.startswith("AIRBUS ONEWEB"):
            return "review", "", "Airbus OneWeb Satellites joint venture; belongs to both owners"
        if u.startswith(("EUTELSAT", "ORG EUROPEENNE TELECOMMUNICATIONS PAR SATELLITE")):
            return "keep", "Eutelsat/OneWeb", "Eutelsat entity"
        if u.startswith("WORLDVU"):
            return "keep", "Eutelsat/OneWeb", "WorldVu, original legal name of OneWeb"
        return "drop", "", '"ONE WEB" substring coincidence'
    if bucket == "Thales Alenia Space":
        if u.startswith("THALES ALENIA SPACE") or u.startswith("ALENIA SPAZIO") \
                or "ALCATEL ALENIA" in u or u.startswith("SELENIA SPAZIO"):
            return "keep", "Thales", "space joint venture lineage (Selenia Spazio -> Alenia Spazio -> Thales Alenia Space)"
        if u.startswith(("ALENIA AERMACCHI", "ALENIA AERONAUTICA", "ALENIA AERITALIA", "ALENIA MARCONI",
                         "ALENIA ELSAG", "ALENIA UN AZIENDA FINMECCANICA", "WHITEHEAD ALENIA")):
            return "drop", "", "Leonardo/Finmeccanica lineage, a different current company we do not track"
        if u.startswith(("SAMSUNG THALES", "HANWHA THALES", "SHANGHAI THALES SAIC")):
            return "keep", "Thales", "real Thales joint venture; group-level capture"
        if u.startswith("YTHALES"):
            return "review", "", "unclear entity, possibly Thales-linked investment vehicle"
        if THALES_UNCONFIRMED.search(u):
            return "review", "", 'Chinese company using "Thales" in its name; affiliation unconfirmed'
        if u.startswith("THALES"):
            return "keep", "Thales", "Thales group entity; pool classification filters relevance"
        return "drop", "", "THALES/ALENIA substring coincidence (person name or unrelated word)"
    if bucket == "Airbus Defence and Space":
        if "AIRBUS" in u or "ASTRIUM" in u or EADS_WORD.search(u) or "AEROSPATIALE" in u \
                or "EUROPEAN AERONAUTIC DEFENCE" in u or "DAIMLER BENZ AEROSPACE" in u \
                or "DEUTSCHE AEROSPACE" in u:
            return "keep", "Airbus", "Airbus group entity (current or heritage name)"
        if EADS_SUBSTRING_JUNK.search(u):
            return "drop", "", "EADS substring coincidence"
        return "review", "", "unclassified Airbus-bucket name"
    return "review", "", "unknown bucket"


def emit_sql(keeps) -> None:
    whens = []
    in_lists = {}
    for owner, name in sorted(keeps):
        esc = name.upper().replace("'", "''")
        whens.append(f"      WHEN '{esc}' THEN '{owner}'")
        in_lists.setdefault(owner, []).append(f"'{esc}'")
    in_all = ",\n      ".join(n for names in in_lists.values() for n in sorted(names))
    sql = f"""-- Peers table: satcom actors, filings since 1996 (mirrors 15_rivals_30y.sql).
-- Generated by src/review_satcom_names.py from data/interim/satcom_name_review.csv.
-- Only names marked "keep" in the review are included; "review" rows wait for a decision.
-- Name matching is exact (post-census), not regex: the census is what makes this safe.
CREATE OR REPLACE TABLE nokia_analytics.satcom_peers_30y AS
SELECT
  p.publication_number,
  p.application_number,
  p.family_id,
  p.country_code,
  p.kind_code,
  p.priority_date,
  p.filing_date,
  p.grant_date,
  ARRAY(
    SELECT DISTINCT CASE UPPER(a.name)
{chr(10).join(whens)}
    END
    FROM UNNEST(p.assignee_harmonized) AS a
    WHERE UPPER(a.name) IN (
      {in_all}
    )
  ) AS owners,
  ARRAY(SELECT c.code FROM UNNEST(p.cpc) AS c) AS cpc_codes,
  (SELECT t.text FROM UNNEST(p.title_localized) AS t WHERE t.language = 'en' LIMIT 1) AS title_en
FROM `patents-public-data.patents.publications` AS p
WHERE p.filing_date >= 19961101
  AND EXISTS (
    SELECT 1 FROM UNNEST(p.assignee_harmonized) AS a
    WHERE UPPER(a.name) IN (
      {in_all}
    )
  );
"""
    SQL.write_text(sql)


def main() -> None:
    with RAW.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["actor_bucket", "name", "publications", "decision", "owner", "reason"])
        keeps = []
        for r in rows:
            decision, owner, reason = classify(r["actor"], r["name"])
            w.writerow([r["actor"], r["name"], r["publications"], decision, owner, reason])
            if decision == "keep":
                keeps.append((owner, r["name"]))
    emit_sql(keeps)

    stats = Counter()
    pubs = Counter()
    for r in rows:
        decision, _, _ = classify(r["actor"], r["name"])
        stats[(r["actor"], decision)] += 1
        pubs[(r["actor"], decision)] += int(r["publications"])
    for bucket in sorted({r["actor"] for r in rows}):
        line = f"{bucket:24}"
        for d in ("keep", "drop", "review"):
            line += f" {d}={stats[(bucket, d)]:4} ({pubs[(bucket, d)]:6} pubs)"
        print(line)


if __name__ == "__main__":
    main()
