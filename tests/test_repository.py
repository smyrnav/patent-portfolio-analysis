"""Keep the repository coherent: links, shared wording, label files and snapshot fingerprints."""
import re
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from build_manifest import fingerprint  # noqa: E402
from common import config, rows  # noqa: E402

CFG = config()
DOCS = [ROOT / "README.md", ROOT / "sql/README.md", *sorted((ROOT / "docs").rglob("*.md"))]
LOGS = {"learning-log.md", "research-log.md", "questions.md"}
RETIRED = ["workable portfolio", "core dataset", "core famil", "granted families", "does nokia own", "nokia actually own", "actually own", "investment position",
           "draft 0.1 |", "](strategy.md", "](competitors.md", "portfolio-filter.md", "data-trust.md", "](principles.md", "how-i-got-here", "approach-changes",
           "roughly 1%", "1% of nokia", "per family, but", "scale_check", "portfolio_filter.png", "investment_position"]


def slug(heading):
    text = re.sub(r"[`*]|\[|\]\([^)]*\)", "", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(path):
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
    return {slug(h) for h in re.findall(r"^#{1,6} (.+)$", text, re.M)}


class Links(unittest.TestCase):
    def test_every_relative_link_resolves(self):
        broken = []
        for doc in DOCS:
            text = re.sub(r"```.*?```", "", doc.read_text(), flags=re.S)
            for target in re.findall(r"\]\(([^)\s]+)\)", text):
                if re.match(r"https?:|mailto:", target):
                    continue
                file_part, _, anchor = target.partition("#")
                path = (doc.parent / file_part).resolve() if file_part else doc
                if not path.exists():
                    broken.append(f"{doc.name}: {target}")
                elif anchor and path.suffix == ".md" and anchor not in anchors(path):
                    broken.append(f"{doc.name}: {target} (anchor)")
        self.assertEqual(broken, [])


class Wording(unittest.TestCase):
    def test_central_question_is_identical_everywhere(self):
        central = CFG["question"]["central"]
        for doc in DOCS:
            if doc.name in LOGS:  # logs quote superseded wording as dated history
                continue
            for found in re.findall(r"How should Nokia prioriti[sz]e[^?*]*\?", doc.read_text()):
                self.assertEqual(found, central, doc.name)
        self.assertIn(central, (ROOT / "README.md").read_text())
        self.assertIn(central, (ROOT / "docs/01-research-design/research-design.md").read_text())

    def test_retired_terms_stay_out_of_current_documents(self):
        hits = []
        for doc in DOCS:
            if doc.name in LOGS:
                continue
            text = doc.read_text().lower()
            hits += [f"{doc.name}: {term}" for term in RETIRED if term in text]
        self.assertEqual(hits, [])

    def test_scope_is_named_consistently(self):
        scope = (ROOT / "docs/01-research-design/scope.md").read_text()
        for name in [*CFG["scope"]["labels"], *CFG["scope"]["core_peers"], CFG["scope"]["global_reference"]]:
            self.assertIn(name, scope)
        codebook = (ROOT / "docs/02-methodology/classification-codebook.md").read_text()
        for name in CFG["scope"]["all_classes"]:
            self.assertIn(f"**{name}", codebook)


class LabelFile(unittest.TestCase):
    def setUp(self):
        self.labels = rows("data/validation/manual_labels.csv")

    def test_fields_and_values(self):
        required = "simple_family_id publication_number applicant priority_date primary_class dc_context optical_medium ai_cloud_relevance claim_evidence review_status annotator confidence codebook_version".split()
        self.assertEqual(list(self.labels[0])[:len(required)], required)
        v = CFG["validation"]
        for r in self.labels:  # archived pre-pivot record, checked against the archived values
            self.assertIn(r["primary_class"], CFG["pre_pivot"]["all_classes"])
            self.assertIn(r["review_status"], v["review_statuses"])
            self.assertIn(r["confidence"], v["confidence_levels"])
            self.assertEqual(r["codebook_version"], CFG["pre_pivot"]["codebook_version"])
            self.assertTrue(r["simple_family_id"] and r["priority_date"] and r["applicant"])

    def test_one_row_per_patent(self):
        ids = [r["publication_number"] for r in self.labels]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {s["publication_number"] for s in rows("data/validation/validation_slots.csv")})

    def test_nothing_is_marked_reviewed_before_a_person_reviews_it(self):
        if not any(r["my_label"].strip() for r in rows("data/validation/agreement_sheet.csv")):
            self.assertEqual({r["review_status"] for r in self.labels}, {"pending"})
            self.assertEqual({r["annotator"] for r in self.labels}, {"claude_first_pass"})

    def test_agreement_sheet_hides_the_labels(self):
        self.assertEqual(list(rows("data/validation/agreement_sheet.csv")[0]), "number publication_number link my_label confidence note".split())


class Manifest(unittest.TestCase):
    def test_snapshots_match_their_fingerprints(self):
        for r in rows("data/source_manifest.csv"):
            self.assertEqual(fingerprint(r["snapshot"]), r["sha256"], r["snapshot"])


class Config(unittest.TestCase):
    def test_config_parses(self):
        with (ROOT / "config/research_parameters.toml").open("rb") as f:
            self.assertIn("scope", tomllib.load(f))


class RunQueries(unittest.TestCase):
    def test_comment_lines_are_stripped(self):
        from run_queries import clean_sql, query_file
        sql_text = clean_sql(query_file(35))
        self.assertFalse(any(line.strip().startswith("--") for line in sql_text.splitlines()))

    def test_ddl_detection(self):
        from run_queries import clean_sql, is_ddl, query_file
        self.assertTrue(is_ddl(clean_sql(query_file(6))))
        self.assertFalse(is_ddl(clean_sql(query_file(35))))

    def test_manifest_output_paths(self):
        from run_queries import manifest_output, query_file
        self.assertEqual(manifest_output(query_file(35)), "data/raw/35_iceye_name_variants.csv")
        self.assertEqual(manifest_output(query_file(34)), "data/validation/satcom_retest_slots.csv")


RETEST_PAGES = ROOT / "data/interim/claim_pages_retest"  # gitignored: local claim text and labelling key
needs_retest_pages = unittest.skipUnless(
    (RETEST_PAGES / "parsed.json").exists() and (RETEST_PAGES / "key_satcom-retest.json").exists(),
    "local claim-review pages not in git; regenerate via src/fetch_claims.py to run")


class ReviewWorkbench(unittest.TestCase):
    def session(self, out="/tmp/test_wb_annotations.csv"):
        from review_workbench import Session
        return Session("data/validation/satcom_retest_slots.csv", "satcom-retest",
                       "data/interim/claim_pages_retest", out, "test")

    @needs_retest_pages
    def test_order_matches_the_blind_sheet_key(self):
        import json
        key = json.loads((ROOT / "data/interim/claim_pages_retest/key_satcom-retest.json").read_text())
        self.assertEqual(self.session().ids, key)

    @needs_retest_pages
    def test_record_and_resume(self):
        import os
        out = "/tmp/test_wb_annotations.csv"
        if os.path.exists(out):
            os.remove(out)
        first = self.session(out)
        first.record(1, "SAT", "", "High", "quote", "reason")
        resumed = self.session(out)
        self.assertEqual(resumed.next_open(), 2)
        self.assertEqual(resumed.counts(), (1, 0, len(resumed.ids) - 1))
        os.remove(out)

    def test_scrub_hides_company_names(self):
        from common import scrub
        self.assertNotIn("Nokia", scrub("Nokia and ICEYE filed this"))
        self.assertIn("[company]", scrub("Nokia filed this"))


class ProzorroExtractor(unittest.TestCase):
    """Sharding logic only; no network. fetch() is replaced with canned totals."""

    def setUp(self):
        import prozorro_extractor as pe
        self.pe = pe
        self.real_fetch, self.real_pause = pe.fetch, pe.PAUSE
        pe.PAUSE = 0

    def tearDown(self):
        self.pe.fetch, self.pe.PAUSE = self.real_fetch, self.real_pause

    def fake_totals(self, totals):
        def fake(kind, text, page, start=None, end=None, date_dim=None):
            return {"total": totals.get((start, end), 5), "data": []}
        self.pe.fetch = fake

    def test_oversized_range_splits_until_each_shard_fits(self):
        import datetime
        pe = self.pe
        start, end = datetime.date(2026, 1, 1), datetime.date(2026, 1, 8)

        def fake(kind, text, page, start=None, end=None, date_dim=None):
            # any range longer than a day is over the cap; a single day fits
            return {"total": 1500 if (end - start).days >= 1 else 300, "data": []}
        pe.fetch = fake
        shards = list(pe.shard("tenders", "x", start, end, "notice"))
        self.assertTrue(shards)
        for s, e, total in shards:
            self.assertLess(total, pe.MAX_TOTAL)
            self.assertEqual(s, e)  # split down to single days
        days = {s for s, _, _ in shards}
        self.assertEqual(len(days), 8)  # every day covered exactly once

    def test_empty_range_yields_nothing(self):
        import datetime
        pe = self.pe
        self.fake_totals({(datetime.date(2022, 1, 1), datetime.date(2022, 12, 31)): 0})
        self.assertEqual(list(pe.shard("tenders", "x", datetime.date(2022, 1, 1), datetime.date(2022, 12, 31), "notice")), [])

    def test_row_from_contract_links_parent_tender(self):
        item = {"contractID": "UA-2024-01-01-000001-a-c1", "status": "terminated",
                "buyer": {"name": "Buyer"}, "suppliers": [{"name": "Seller"}],
                "value": {"amount": 100, "currency": "UAH", "valueAddedTaxIncluded": True}}
        row = self.pe.row_from("contracts", item, parent_tender_id="UA-2024-01-01-000001-a")
        self.assertEqual(row[0], "UA-2024-01-01-000001-a-c1")
        self.assertEqual(row[1], "UA-2024-01-01-000001-a")
        self.assertEqual(row[3], "Seller")


class ProzorroPipeline(unittest.TestCase):
    """Dedup/merge logic; no network, no YAML."""

    def item(self, tid, title="t"):
        return {"tenderID": tid, "title": title, "status": "complete",
                "procuringEntity": {"name": "B"}, "value": {"amount": 1, "currency": "UAH"}}

    def test_one_tender_keeps_every_matching_category_and_query(self):
        import prozorro_pipeline as pp
        db, matches = {}, []
        pp.add_match(db, matches, "starlink", "Starlink", self.item("UA-1"))
        pp.add_match(db, matches, "satellite_hardware", "супутниковий модем", self.item("UA-1"))
        pp.add_match(db, matches, "satellite_hardware", "супутниковий термінал", self.item("UA-1"))
        pp.add_match(db, matches, "starlink", "Starlink", self.item("UA-2"))
        self.assertEqual(len(db), 2)  # one tender = one record
        self.assertEqual(db["UA-1"]["categories"], {"starlink", "satellite_hardware"})
        self.assertEqual(db["UA-1"]["queries"], {"Starlink", "супутниковий модем", "супутниковий термінал"})
        self.assertEqual(len(matches), 4)  # every match preserved as a relation

    def test_resume_skips_completed_queries(self):
        import prozorro_pipeline as pp
        cp = {"queries": {"starlink|Starlink": {"items": 5}}, "contracts": [], "details": [], "summaries": []}
        cfg = {"project": {"date_from": "2024-01-01", "date_to": "2024-12-31"},
               "categories": {"starlink": {"queries": ["Starlink"]}}}
        done = []
        real_read = pp.read_jsonl
        pp.read_jsonl = lambda path: []
        try:
            db, matches = pp.search_phase(cfg, cp, done)
        finally:
            pp.read_jsonl = real_read
        self.assertIn("starlink|Starlink", cp["queries"])
        self.assertEqual(db, {})  # no network calls happened; checkpoint said done

    def test_fetch_retry_calls_the_original_fetch_not_the_patched_one(self):
        import prozorro_pipeline as pp
        calls = []
        real = pp._REAL_FETCH
        pp._REAL_FETCH = lambda *a, **k: calls.append(a) or {"total": 0, "data": []}
        try:
            pe_fetch_before = pp.pe.fetch
            pp.pe.fetch = pp.fetch_retry  # what search_phase does
            result = pp.fetch_retry("tenders", "x", 1)
        finally:
            pp._REAL_FETCH = real
            pp.pe.fetch = pe_fetch_before
        self.assertEqual(result, {"total": 0, "data": []})
        self.assertEqual(len(calls), 1)  # exactly one call, no recursion


if __name__ == "__main__":
    unittest.main()
