"""Negative fixtures for the domain-vocabulary validator.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Each test mutates the committed PROPOSED-domain-vocabulary-v1.yaml in one way and asserts the
validator refuses it; the committed file itself must pass, and pass identically twice
(determinism). The acceptance-critical fixture is the label mapped to two medium terms.

Run: python3 -m unittest tests.test_domain_vocabulary -v
"""
import copy
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from canon.validation import validate_domain_vocabulary as validator  # noqa: E402

ARTIFACT = REPO_ROOT / "canon/ontology/PROPOSED-domain-vocabulary-v1.yaml"


class DomainVocabularyValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counts, cls.dirs, cls.n_files = validator.recompute_census()
        cls.doc = yaml.safe_load(ARTIFACT.read_text())

    def check(self, doc) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.yaml"
            path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
            return validator.validate(path, self.counts, self.dirs)

    def mutate(self):
        return copy.deepcopy(self.doc)

    def assertRefused(self, errors, needle):
        self.assertTrue(errors, "expected the validator to refuse this fixture")
        self.assertIn(needle, " | ".join(errors))

    # ── the committed artifact ──────────────────────────────────────────
    def test_committed_artifact_passes(self):
        self.assertEqual(validator.validate(ARTIFACT, self.counts, self.dirs), [])

    def test_round_tripped_artifact_still_passes(self):
        self.assertEqual(self.check(self.mutate()), [])

    def test_census_totals_match_brief_figures(self):
        self.assertEqual(sum(self.counts.values()), 1335)
        self.assertEqual(len(self.counts), 331)
        self.assertEqual(sum(1 for v in self.counts.values() if v == 1), 197)

    def test_coverage_target_met(self):
        covered = sum(self.counts[l] for l in self.doc["mapping"])
        self.assertGreaterEqual(len(self.doc["mapping"]), 205)
        self.assertGreaterEqual(covered / sum(self.counts.values()), 0.90)

    def test_validator_is_deterministic_across_two_runs(self):
        runs = []
        for _ in range(2):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = validator.main(["validate_domain_vocabulary.py", str(ARTIFACT)])
            runs.append((rc, buf.getvalue()))
        self.assertEqual(runs[0], runs[1])
        self.assertEqual(runs[0][0], 0)

    def test_cli_exits_zero_on_committed_artifact(self):
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "canon/validation/validate_domain_vocabulary.py")],
            capture_output=True, text=True, cwd=REPO_ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    # ── acceptance-critical negative fixture ────────────────────────────
    def test_label_mapped_to_two_medium_terms_is_refused(self):
        doc = self.mutate()
        doc["mapping"]["film_editing"]["terms"] = [
            "m_moving_image_editing", "m_moving_image_production"]
        self.assertRefused(self.check(doc), "at most one term per axis")

    def test_label_mapped_to_two_subject_terms_is_refused(self):
        doc = self.mutate()
        doc["mapping"]["advertising"]["terms"] = [
            "s_advertising_craft", "s_advertising_effectiveness"]
        self.assertRefused(self.check(doc), "at most one term per axis")

    # ── partition: never both, never neither ────────────────────────────
    def test_silently_dropped_label_is_refused(self):
        doc = self.mutate()
        del doc["mapping"]["film_editing"]
        self.assertRefused(self.check(doc), "silent drop")

    def test_label_in_both_mapping_and_queue_is_refused(self):
        doc = self.mutate()
        row = doc["mapping"]["film_editing"]
        doc["review_queue"].append({"label": "film_editing", "count": row["count"],
                                    "source_dirs": [], "reason": "duplicate"})
        self.assertRefused(self.check(doc), "BOTH mapping and review_queue")

    def test_phantom_label_is_refused(self):
        doc = self.mutate()
        doc["mapping"]["label_that_no_source_carries"] = {
            "count": 1, "terms": ["s_advertising_craft"]}
        self.assertRefused(self.check(doc), "phantom row")

    # ── recomputation beats recorded figures ────────────────────────────
    def test_wrong_recorded_census_is_refused(self):
        doc = self.mutate()
        doc["census"]["accepted"]["mentions"] = 9999
        self.assertRefused(self.check(doc), "recomputed value is 1335")

    def test_wrong_per_label_count_is_refused(self):
        doc = self.mutate()
        doc["mapping"]["film_editing"]["count"] = 1
        self.assertRefused(self.check(doc), "recomputed count is 125")

    def test_wrong_recorded_coverage_is_refused(self):
        doc = self.mutate()
        doc["coverage"]["mapped_mentions"] = 1335
        self.assertRefused(self.check(doc), "coverage.mapped_mentions")

    # ── closed enum and reserved term ───────────────────────────────────
    def test_term_outside_closed_enum_is_refused(self):
        doc = self.mutate()
        doc["mapping"]["film_editing"]["terms"] = ["m_invented_term"]
        self.assertRefused(self.check(doc), "not in the closed 22-term enum")

    def test_reserved_term_with_a_member_is_refused(self):
        doc = self.mutate()
        doc["mapping"]["film_editing"]["terms"] = ["m_short_form_feed_video"]
        self.assertRefused(self.check(doc), "zero members")

    def test_reserved_term_without_rationale_is_refused(self):
        doc = self.mutate()
        for row in doc["vocabulary"]["medium"]:
            if row["term"] == "m_short_form_feed_video":
                row["rationale"] = ""
        self.assertRefused(self.check(doc), "non-empty rationale")

    def test_queue_row_without_reason_is_refused(self):
        doc = self.mutate()
        doc["review_queue"][0]["reason"] = ""
        self.assertRefused(self.check(doc), "non-empty reason")


if __name__ == "__main__":
    unittest.main()
