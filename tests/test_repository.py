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
        for r in self.labels:
            self.assertIn(r["primary_class"], CFG["scope"]["all_classes"])
            self.assertIn(r["review_status"], v["review_statuses"])
            self.assertIn(r["confidence"], v["confidence_levels"])
            self.assertEqual(r["codebook_version"], v["codebook_version"])
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


if __name__ == "__main__":
    unittest.main()
