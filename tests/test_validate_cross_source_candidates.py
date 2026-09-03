"""Tests for the REP-02 cross-source candidate-ledger validator.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

The committed ledger must pass; each negative fixture must fail with its named error; and a
handful of in-memory mutations pin the per-row rules the fixtures do not cover. Run with:
    python3 -m unittest tests.test_validate_cross_source_candidates
"""
import copy
import unittest
from pathlib import Path

import yaml

from canon.validation import validate_cross_source_candidates as validator

REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER = REPO_ROOT / "canon/candidates/ontology-join/cross-source-candidates-v0.yaml"
FIXTURES = REPO_ROOT / "canon/validation/fixtures/ontology-join"


def codes(errors):
    return {e.split(":", 1)[0] for e in errors}


class LedgerPassesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = yaml.safe_load(LEDGER.read_text())

    def test_committed_ledger_validates_clean(self):
        errors = validator.validate(self.ledger)
        self.assertEqual(errors, [])

    def test_every_row_is_proposed_with_grade_and_usable_flag(self):
        for row in self.ledger["records"]:
            self.assertEqual(row["status"], "proposed", row["record_id"])
            self.assertIn(row["confidence"], {"high", "medium", "low"}, row["record_id"])
            self.assertIn(row["usable"], {"accepted_only", "involves_hold", False}, row["record_id"])

    def test_sixteen_imported_rows_present_and_hold_flagged(self):
        imported = [r for r in self.ledger["records"] if r["kind"] == "imported_observation"]
        self.assertEqual(len(imported), 16)
        for row in imported:
            self.assertEqual(row["usable"], "involves_hold", row["record_id"])

    def test_duplicate_terms_each_have_one_adjudication(self):
        # Six duplicate terms at REP-02 authoring; the DN-06 admission batch (2026-09-01,
        # 24 -> 37 sources) created seven more exact-duplicate term strings, adjudicated
        # in ledger rows xj_0054-xj_0060.
        expected = {"darshan", "eye_trace", "jump_cut", "no_authored_page", "screen_direction",
                    "story", "blind_headline", "charging_for_the_sample", "irrelevant_brilliance",
                    "keyed_advertising", "noise", "substitution", "traced_returns"}
        self.assertEqual(validator.duplicate_term_strings(), expected)
        seen = [r["adjudicates_duplicate_term"]
                for r in self.ledger["records"] if r.get("adjudicates_duplicate_term")]
        self.assertEqual(sorted(seen), sorted(expected))


class NegativeFixtureTest(unittest.TestCase):
    def run_fixture(self, name):
        return validator.validate(yaml.safe_load((FIXTURES / name).read_text()))

    def test_positive_minimal_fixture_passes(self):
        self.assertEqual(self.run_fixture("positive_minimal.yaml"), [])

    def test_bad_relation_enum_fails_named(self):
        self.assertIn("E_RELATION_ENUM", codes(self.run_fixture("negative_bad_relation_enum.yaml")))

    def test_hold_id_on_accepted_row_fails_named(self):
        self.assertIn("E_HOLD_ID_ON_ACCEPTED_ROW",
                      codes(self.run_fixture("negative_hold_id_on_accepted_row.yaml")))

    def test_agreement_on_companion_pair_fails_named(self):
        found = codes(self.run_fixture("negative_agreement_on_companion_pair.yaml"))
        self.assertIn("E_AGREEMENT_WITHOUT_INDEPENDENT_ORIGINS", found)
        self.assertIn("E_ORIGIN_COUNT", found)


class MutationTest(unittest.TestCase):
    """Per-row rules pinned by mutating the committed ledger in memory."""

    @classmethod
    def setUpClass(cls):
        cls.base = yaml.safe_load(LEDGER.read_text())

    def mutate(self, fn):
        ledger = copy.deepcopy(self.base)
        fn(ledger)
        return codes(validator.validate(ledger))

    def row(self, ledger, record_id):
        return next(r for r in ledger["records"] if r["record_id"] == record_id)

    def test_status_not_proposed_is_refused(self):
        found = self.mutate(lambda l: self.row(l, "xj_0001").__setitem__("status", "accepted"))
        self.assertIn("E_STATUS", found)

    def test_missing_confidence_is_refused(self):
        found = self.mutate(lambda l: self.row(l, "xj_0001").pop("confidence"))
        self.assertIn("E_CONFIDENCE", found)

    def test_bad_usable_value_is_refused(self):
        found = self.mutate(lambda l: self.row(l, "xj_0001").__setitem__("usable", "yes"))
        self.assertIn("E_USABLE", found)

    def test_unresolved_id_is_refused(self):
        found = self.mutate(
            lambda l: self.row(l, "xj_0001")["members"][0].__setitem__("id", "t_zzz_9999"))
        self.assertIn("E_UNRESOLVED_ID", found)

    def test_misquoted_independence_is_refused(self):
        # xj_0002 quotes dwyer<->jain as cites_source; claiming no_known_relation must fail.
        def fn(ledger):
            self.row(ledger, "xj_0002")["independence"][0]["audit_relation"] = "no_known_relation"
        self.assertIn("E_INDEPENDENCE_MISMATCH", self.mutate(fn))

    def test_wrong_origin_count_is_refused(self):
        found = self.mutate(lambda l: self.row(l, "xj_0001").__setitem__("independent_origins", 2))
        self.assertIn("E_ORIGIN_COUNT", found)

    def test_tension_without_frame_note_is_refused(self):
        found = self.mutate(lambda l: self.row(l, "xj_0021").pop("frame_note"))
        self.assertIn("E_FRAME_NOTE", found)

    def test_dropped_import_is_refused(self):
        def fn(ledger):
            ledger["records"] = [r for r in ledger["records"] if r["record_id"] != "xj_0038"]
        self.assertIn("E_IMPORT_MISSING", self.mutate(fn))

    def test_second_adjudication_of_same_term_is_refused(self):
        def fn(ledger):
            self.row(ledger, "xj_0030")["adjudicates_duplicate_term"] = "darshan"
        found = self.mutate(fn)
        self.assertIn("E_DUPLICATE_ADJUDICATION", found)

    def test_shared_primary_informant_pair_cannot_carry_agreement(self):
        # Upgrading the murch/ondaatje dependent pair to same_mechanism must be refused: the
        # audit records say shared_primary_informant.
        def fn(ledger):
            self.row(ledger, "xj_0032")["relation"] = "same_mechanism"
        self.assertIn("E_AGREEMENT_WITHOUT_INDEPENDENT_ORIGINS", self.mutate(fn))


if __name__ == "__main__":
    unittest.main()
