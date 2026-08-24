import tempfile
import unittest
from pathlib import Path

import yaml

from canon.validation import validate_audit_gate_v02 as validator

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _make_frozen_book(root: Path, name: str, source_id: str, *, empirical: bool = False) -> str:
    """Minimal frozen SPEC-03/04 pair for an audit record to point at."""
    book = root / "canon" / "knowledge" / "current" / name
    characteristics = ["explicitly_stated"]
    if empirical:
        characteristics.append("empirical_within_source")
    _write_yaml(book / "source-knowledge.yaml", {
        "source_id": source_id,
        "source_knowledge": [
            {"sk_id": "sk_fx_0001", "evidence": {"characteristics": characteristics}},
            {"sk_id": "sk_fx_0002", "evidence": {"characteristics": ["explicitly_stated"]}},
        ],
    })
    _write_yaml(book / "operational-bindings.yaml", {
        "source_id": source_id,
        "operational_bindings": [{"binding_id": "bnd_fx_0001", "target_type": "governance"}],
    })
    return f"canon/knowledge/current/{name}"


def _minimal_record(source_id: str, knowledge_dir: str, audit_id: str) -> dict:
    return {
        "audit_record_version": "v0.2-experimental",
        "audit_id": audit_id,
        "source_id": source_id,
        "knowledge_dir": knowledge_dir,
        "audit_status": "complete",
        "representation_integrity": {
            "delivery_format": "publisher_epub",
            "page_addressability": "no_pages_reflowable",
            "inspection_state": "inspected_figure_level",
            "visual_argument_role": "no_visual_argument",
            "observed_loss_patterns": [{
                "pattern": "no_loss_detected",
                "affects": "nothing",
                "detectability": "detected_by_independent_check",
                "recoverability": "not_applicable",
                "evidence": "all images measured; none argues a claim",
            }],
            "claim_resolution_after_inspection": "not_applicable",
        },
        "evidence_origin": {
            "audit_scope": "all_objects",
            "categories": [{
                "category": "source_author_assertion",
                "sk_refs": ["sk_fx_0002"],
                "evidence": "the author speaks in their own voice",
            }],
        },
        "application_fit": {
            "audited": True,
            "findings": [
                {"consumer": c, "outcome": "no_current_binding"}
                for c in validator.APPLICATION_CONSUMERS
            ],
        },
        "lineage": {
            "authors": ["A Person"],
            "related_sources_in_corpus": [],
            "independence_verdict": "independent_origin",
            "independence_basis": "no shared authorship with any corpus source",
            "extractor_exposure": {
                "spec_contains_examples_from_this_source": False,
                "evidence": "not quoted in the specs",
            },
        },
        "technology_contingency": {
            "applicable": False,
            "applicability_basis": "a current source with no technology dependency",
            "assessed": False,
            "classes": [],
        },
    }


class AuditGateRecordTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.knowledge_dir = _make_frozen_book(self.root, "fixture-book", "fixture_source")
        self.record = _minimal_record("fixture_source", self.knowledge_dir, "aud_fixture")

    def tearDown(self):
        self._tmp.cleanup()

    def test_minimal_valid_record_has_no_errors(self):
        self.assertEqual(validator.validate_record(self.record, self.root), [])

    def test_unresolved_sk_ref_is_reported(self):
        self.record["evidence_origin"]["categories"][0]["sk_refs"] = ["sk_does_not_exist"]
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("unresolved sk_ref sk_does_not_exist" in e for e in errors), errors)

    def test_source_id_mismatch_is_reported(self):
        self.record["source_id"] = "some_other_source"
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("does not match frozen record" in e for e in errors), errors)

    # ── the anti-score rule ─────────────────────────────────────────────────────────────────
    def test_score_like_key_is_refused_at_any_depth(self):
        self.record["representation_integrity"]["visual_risk_score"] = 3
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("forbidden score-like key" in e for e in errors), errors)

    def test_credibility_key_is_refused_even_when_nested_deeply(self):
        self.record["evidence_origin"]["categories"][0]["credibility"] = "high"
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("forbidden score-like key" in e for e in errors), errors)

    # ── no_current_binding must not collapse into not_audited ───────────────────────────────
    def test_not_audited_requires_a_reason_and_forbids_findings(self):
        self.record["application_fit"] = {"audited": False, "findings": [
            {"consumer": "creative_ir", "outcome": "no_current_binding"}]}
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("requires not_audited_reason" in e for e in errors), errors)
        self.assertTrue(any("must not carry findings" in e for e in errors), errors)

    def test_not_audited_with_reason_is_valid_and_distinct_from_no_binding(self):
        self.record["application_fit"] = {
            "audited": False,
            "not_audited_reason": "the frozen record does not say which consumers were considered",
        }
        self.assertEqual(validator.validate_record(self.record, self.root), [])

    def test_audited_must_cover_every_consumer(self):
        self.record["application_fit"]["findings"] = [
            {"consumer": "creative_ir", "outcome": "no_current_binding"}]
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("does not cover consumers" in e for e in errors), errors)

    def test_binding_exists_requires_a_binding_reference(self):
        self.record["application_fit"]["findings"][0] = {
            "consumer": "creative_ir", "outcome": "binding_exists"}
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("binding_exists with no existing_binding_refs" in e for e in errors), errors)

    # ── evidence origin must agree with the frozen SPEC-03 characteristic ───────────────────
    def test_own_measurement_claim_requires_empirical_within_source(self):
        self.record["evidence_origin"]["categories"] = [{
            "category": "source_own_measurement_reported",
            "sk_refs": ["sk_fx_0002"],
            "evidence": "claimed as the source's own measurement",
        }]
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(
            any("does not carry empirical_within_source" in e for e in errors), errors
        )

    def test_third_party_measurement_must_not_carry_empirical_within_source(self):
        _make_frozen_book(self.root, "empirical-book", "empirical_source", empirical=True)
        record = _minimal_record(
            "empirical_source", "canon/knowledge/current/empirical-book", "aud_empirical")
        record["evidence_origin"]["categories"] = [{
            "category": "third_party_measurement_reported",
            "sk_refs": ["sk_fx_0001"],
            "evidence": "a named outside study",
        }]
        errors = validator.validate_record(record, self.root)
        self.assertTrue(any("but the frozen record carries" in e for e in errors), errors)

    # ── technology contingency ──────────────────────────────────────────────────────────────
    def test_applicable_contingency_must_be_assessed_with_classes(self):
        self.record["technology_contingency"] = {
            "applicable": True,
            "applicability_basis": "first published 1949",
            "assessed": True,
            "classes": [],
        }
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("assessed with no classes recorded" in e for e in errors), errors)

    def test_loss_patterns_cannot_be_empty(self):
        self.record["representation_integrity"]["observed_loss_patterns"] = []
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("observed_loss_patterns is empty" in e for e in errors), errors)


class IndependenceRuleTests(unittest.TestCase):
    """The promotion rule: a source id count must not stand in for independent origins."""

    def _records(self, *specs) -> dict:
        out = {}
        for name, source_id, related in specs:
            record = {
                "audit_id": f"aud_{name}",
                "source_id": source_id,
                "lineage": {
                    "independence_verdict": "not_independent" if related and any(
                        r["relation"] in validator.DEPENDENT_RELATIONS for r in related
                    ) else "independent_origin",
                    "related_sources_in_corpus": related,
                },
            }
            out[f"{name}.audit.yaml"] = record
        return out

    def test_same_author_companion_books_are_not_independent_origins(self):
        records = self._records(
            ("a", "book_a", [{"source_id": "book_b", "relation": "companion_volume"}]),
            ("b", "book_b", [{"source_id": "book_a", "relation": "companion_volume"}]),
        )
        ok, reason = validator.independent_origins_ok("book_a", "book_b", records)
        self.assertFalse(ok)
        self.assertIn("companion_volume", reason)

    def test_dependence_declared_on_only_one_side_still_blocks_promotion(self):
        records = self._records(
            ("a", "book_a", [{"source_id": "book_b", "relation": "shared_author"}]),
            ("b", "book_b", []),
        )
        ok, _ = validator.independent_origins_ok("book_a", "book_b", records)
        self.assertFalse(ok)

    def test_shared_publisher_alone_does_not_defeat_independence(self):
        records = self._records(
            ("a", "book_a", [{"source_id": "book_b", "relation": "shares_publisher_only"}]),
            ("b", "book_b", [{"source_id": "book_a", "relation": "shares_publisher_only"}]),
        )
        ok, _ = validator.independent_origins_ok("book_a", "book_b", records)
        self.assertTrue(ok)

    def test_citation_alone_does_not_defeat_independence(self):
        records = self._records(
            ("a", "book_a", [{"source_id": "book_b", "relation": "cites_source"}]),
            ("b", "book_b", []),
        )
        ok, _ = validator.independent_origins_ok("book_a", "book_b", records)
        self.assertTrue(ok)

    def test_unestablished_independence_blocks_rather_than_passes(self):
        records = self._records(("a", "book_a", []), ("b", "book_b", []))
        records["a.audit.yaml"]["lineage"]["independence_verdict"] = "independence_not_established"
        ok, reason = validator.independent_origins_ok("book_a", "book_b", records)
        self.assertFalse(ok)
        self.assertIn("independence_not_established", reason)

    def test_missing_audit_record_blocks_promotion(self):
        records = self._records(("a", "book_a", []))
        ok, reason = validator.independent_origins_ok("book_a", "book_absent", records)
        self.assertFalse(ok)
        self.assertIn("no audit record", reason)

    def test_one_sided_dependence_is_reported_by_the_record_set_check(self):
        records = self._records(
            ("a", "book_a", [{"source_id": "book_b", "relation": "companion_volume"}]),
            ("b", "book_b", []),
        )
        errors = validator.validate_record_set(records)
        self.assertTrue(any("declared from both sides" in e for e in errors), errors)


class RealCorpusTests(unittest.TestCase):
    """Exercise the rule against the committed 16-record corpus, not a fixture."""

    @classmethod
    def setUpClass(cls):
        cls.records = {}
        for path in sorted((REPO_ROOT / validator.RECORDS_SUBPATH).glob("*.audit.yaml")):
            cls.records[path.name] = yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_all_sixteen_accepted_books_have_a_record(self):
        self.assertEqual(len(self.records), 16)

    def test_committed_corpus_validates_clean(self):
        report = validator.validate_repository(REPO_ROOT)
        self.assertEqual(report["errors"], [])

    def test_the_two_grammar_books_cannot_count_as_independent_convergence(self):
        ok, reason = validator.independent_origins_ok(
            "grammar_of_the_shot_ch4_continuity",
            "grammar_of_the_edit_ch3_5_editing_decisions",
            self.records,
        )
        self.assertFalse(ok, "same-author companion volumes must not pass the promotion rule")
        self.assertIn("companion_volume", reason)

    def test_murch_and_grammar_of_the_edit_are_a_genuine_convergence(self):
        # Independence is a property of a PAIR. Grammar of the Edit is not an independent origin
        # against its companion volume, and is a perfectly good one against Murch - a different
        # author, publisher and decade writing on the same subject. A rule that blocked this
        # would lose the corpus's clearest real convergence in order to catch its one false one.
        ok, _ = validator.independent_origins_ok(
            "murch_blink_p1_25_editing_decisions",
            "grammar_of_the_edit_ch3_5_editing_decisions",
            self.records,
        )
        self.assertTrue(ok)

    def test_a_source_blocked_against_its_companion_is_still_usable_elsewhere(self):
        blocked, _ = validator.independent_origins_ok(
            "grammar_of_the_shot_ch4_continuity",
            "grammar_of_the_edit_ch3_5_editing_decisions",
            self.records,
        )
        allowed, _ = validator.independent_origins_ok(
            "grammar_of_the_shot_ch4_continuity",
            "murch_blink_p1_25_editing_decisions",
            self.records,
        )
        self.assertFalse(blocked)
        self.assertTrue(allowed)

    def test_two_unrelated_sources_pass_the_promotion_rule(self):
        ok, _ = validator.independent_origins_ok(
            "murch_blink_p1_25_editing_decisions",
            "samara_making_breaking_grid_ch1",
            self.records,
        )
        self.assertTrue(ok)

    def test_shared_publisher_pair_in_the_real_corpus_stays_promotable(self):
        ok, _ = validator.independent_origins_ok(
            "freeman_photographers_eye_graphic_guide_parts1_3",
            "grammar_of_the_shot_ch4_continuity",
            self.records,
        )
        self.assertTrue(ok, "Focal Press alone must not defeat independence")


if __name__ == "__main__":
    unittest.main()
