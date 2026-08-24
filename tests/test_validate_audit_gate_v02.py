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
    """Minimal frozen source representation for an audit record to point at.

    Writes every file the snapshot covers, so a fixture book is snapshot-complete.
    """
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
    _write_yaml(book / "source-concept-systems.yaml", {
        "source_id": source_id, "source_concept_systems": []})
    _write_yaml(book / "ontology-mappings.yaml", {
        "source_id": source_id, "terms": [], "relationships": [], "concepts": []})
    _write_yaml(book / "visual-evidence-ledger.yaml", {
        "source_id": source_id, "pass": "performed", "visual_completeness": "fixture"})
    return f"canon/knowledge/current/{name}"


def _minimal_record(source_id: str, knowledge_dir: str, audit_id: str, root: Path) -> dict:
    snapshot = validator.compute_source_snapshot(root, knowledge_dir)
    return {
        "audit_record_version": validator.AUDIT_RECORD_VERSION,
        "audit_id": audit_id,
        "source_id": source_id,
        "knowledge_dir": knowledge_dir,
        "recorded_at_commit": "0" * 40,
        "audit_status": "complete",
        "source_snapshot": {
            "algorithm": snapshot["algorithm"],
            "files": snapshot["files"],
            "combined_digest": snapshot["combined_digest"],
        },
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
        self.record = _minimal_record(
            "fixture_source", self.knowledge_dir, "aud_fixture", self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_minimal_valid_record_has_no_errors(self):
        self.assertEqual(validator.validate_record(self.record, self.root), [])

    # ── the single adopted record version ───────────────────────────────────────────────────
    def test_adopted_version_record_passes(self):
        self.assertEqual(self.record["audit_record_version"], "v0.2")
        self.assertEqual(validator.validate_record(self.record, self.root), [])

    def test_pre_adoption_experimental_version_is_refused(self):
        self.record["audit_record_version"] = "v0.2-experimental"
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(
            any("unsupported audit_record_version 'v0.2-experimental'" in e for e in errors),
            errors,
        )

    def test_arbitrary_unsupported_version_is_refused(self):
        for bad in ("v0.1", "v0.3", "latest", "2", ""):
            with self.subTest(version=bad):
                self.record["audit_record_version"] = bad
                errors = validator.validate_record(self.record, self.root)
                self.assertTrue(errors, f"version {bad!r} was accepted")

    def test_missing_version_still_fails(self):
        del self.record["audit_record_version"]
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(
            any("missing required field audit_record_version" in e for e in errors), errors
        )

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
            "empirical_source", "canon/knowledge/current/empirical-book", "aud_empirical",
            self.root)
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

    # ── the CANON-007 loss-pattern addition ─────────────────────────────────────────────────
    def test_figure_semantic_binding_lost_is_accepted(self):
        self.record["representation_integrity"]["observed_loss_patterns"] = [{
            "pattern": "figure_semantic_binding_lost",
            "affects": "every quantitative claim",
            "detectability": "silent",
            "recoverability": "recovered_in_this_copy",
            "evidence": "labels and values survive; their correspondence does not",
        }]
        self.assertEqual(validator.validate_record(self.record, self.root), [])

    def test_an_unknown_loss_pattern_still_fails_closed(self):
        for bad in ("figure_semantics_lost", "chart_binding_broken", "", "in_figure_text_missing"):
            with self.subTest(pattern=bad):
                self.record["representation_integrity"]["observed_loss_patterns"] = [{
                    "pattern": bad, "affects": "x", "detectability": "silent",
                    "recoverability": "not_applicable", "evidence": "y",
                }]
                errors = validator.validate_record(self.record, self.root)
                self.assertTrue(
                    any("invalid loss pattern" in e for e in errors),
                    f"pattern {bad!r} was accepted: {errors}",
                )

    def test_loss_patterns_cannot_be_empty(self):
        self.record["representation_integrity"]["observed_loss_patterns"] = []
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("observed_loss_patterns is empty" in e for e in errors), errors)


class StaleAuditTests(unittest.TestCase):
    """An audit describes a source at one moment. If the source moves, the audit must stop passing.

    This gate blocks cross-source promotion and product use, so a stale pass is worse than no gate.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.knowledge_dir = _make_frozen_book(self.root, "fixture-book", "fixture_source")
        self.book = self.root / self.knowledge_dir
        self.record = _minimal_record(
            "fixture_source", self.knowledge_dir, "aud_fixture", self.root)

    def tearDown(self):
        self._tmp.cleanup()

    # 1. unchanged source snapshot -> audit passes
    def test_unchanged_source_snapshot_passes(self):
        self.assertEqual(validator.validate_record(self.record, self.root), [])

    # 2. mutate a frozen source artifact after the audit -> audit fails as stale
    def test_mutating_source_knowledge_after_the_audit_fails_as_stale(self):
        path = self.book / "source-knowledge.yaml"
        path.write_text(path.read_text() + "\n# edited after the audit was written\n", encoding="utf-8")
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("STALE AUDIT" in e and "source-knowledge.yaml" in e for e in errors), errors)

    def test_mutating_any_covered_artifact_is_detected(self):
        for name in validator.SNAPSHOT_FILES:
            with self.subTest(artifact=name):
                path = self.book / name
                original = path.read_text()
                path.write_text(original + "\n# probe\n", encoding="utf-8")
                errors = validator.validate_record(self.record, self.root)
                path.write_text(original, encoding="utf-8")
                self.assertTrue(
                    any("STALE AUDIT" in e and name in e for e in errors),
                    f"a change to {name} was not detected: {errors}",
                )

    # 3. regenerate the audit snapshot against the changed artifact -> it can pass again
    def test_regenerating_the_snapshot_after_a_legitimate_change_passes_again(self):
        path = self.book / "ontology-mappings.yaml"
        path.write_text(path.read_text() + "\n# a legitimate later correction\n", encoding="utf-8")
        self.assertTrue(any("STALE AUDIT" in e for e in validator.validate_record(self.record, self.root)))

        refreshed = validator.compute_source_snapshot(self.root, self.knowledge_dir)
        self.record["source_snapshot"] = {
            "algorithm": refreshed["algorithm"],
            "files": refreshed["files"],
            "combined_digest": refreshed["combined_digest"],
        }
        self.assertEqual(validator.validate_record(self.record, self.root), [])

    # 4. missing fingerprint/snapshot metadata -> fails
    def test_missing_snapshot_fails(self):
        del self.record["source_snapshot"]
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("source_snapshot missing" in e for e in errors), errors)

    def test_snapshot_that_omits_a_required_artifact_fails(self):
        self.record["source_snapshot"]["files"] = [
            f for f in self.record["source_snapshot"]["files"]
            if f["path"] != "operational-bindings.yaml"
        ]
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(
            any("does not cover required artifact operational-bindings.yaml" in e for e in errors),
            errors,
        )

    def test_deleting_a_snapshot_artifact_fails_clearly(self):
        (self.book / "visual-evidence-ledger.yaml").unlink()
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(
            any("snapshot artifact visual-evidence-ledger.yaml is missing" in e for e in errors),
            errors,
        )

    def test_wrong_algorithm_is_refused(self):
        self.record["source_snapshot"]["algorithm"] = "md5-of-something"
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("is not 'sha256-of-sorted-path-and-content'" in e for e in errors), errors)

    def test_tampered_combined_digest_is_refused(self):
        self.record["source_snapshot"]["combined_digest"] = "0" * 64
        errors = validator.validate_record(self.record, self.root)
        self.assertTrue(any("internally inconsistent" in e for e in errors), errors)

    # There must be exactly ONE enforced version mechanism.
    def test_recorded_at_commit_is_informational_and_not_enforced(self):
        self.record["recorded_at_commit"] = "deadbeef" * 5
        self.assertEqual(
            validator.validate_record(self.record, self.root), [],
            "recorded_at_commit must be informational provenance; the snapshot is the enforced check",
        )

    def test_snapshot_is_deterministic_and_content_addressed(self):
        first = validator.compute_source_snapshot(self.root, self.knowledge_dir)
        second = validator.compute_source_snapshot(self.root, self.knowledge_dir)
        self.assertEqual(first, second)
        self.assertEqual([f["path"] for f in first["files"]], sorted(validator.SNAPSHOT_FILES))

    def test_computing_a_snapshot_does_not_modify_the_source(self):
        before = {
            name: (self.book / name).read_bytes() for name in validator.SNAPSHOT_FILES
        }
        validator.compute_source_snapshot(self.root, self.knowledge_dir)
        validator.validate_record(self.record, self.root)
        after = {name: (self.book / name).read_bytes() for name in validator.SNAPSHOT_FILES}
        self.assertEqual(before, after)


class IndependenceRuleTests(unittest.TestCase):
    """The promotion rule: a source id count must not stand in for independent origins."""

    def _records(self, *specs) -> dict:
        out = {}
        for name, source_id, related in specs:
            record = {
                "audit_id": f"aud_{name}",
                "source_id": source_id,
                "lineage": {
                    "independence_verdict": "not_independent_of_named_sources" if related and any(
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

    def test_unrecognised_verdict_fails_closed(self):
        records = self._records(("a", "book_a", []), ("b", "book_b", []))
        records["a.audit.yaml"]["lineage"]["independence_verdict"] = "probably_fine"
        ok, reason = validator.independent_origins_ok("book_a", "book_b", records)
        self.assertFalse(ok, "a verdict outside the controlled vocabulary must not pass")
        self.assertIn("unrecognised independence_verdict", reason)

    def test_fixtures_use_the_real_controlled_vocabulary(self):
        records = self._records(
            ("a", "book_a", [{"source_id": "book_b", "relation": "companion_volume"}]),
            ("b", "book_b", [{"source_id": "book_a", "relation": "companion_volume"}]),
        )
        for record in records.values():
            self.assertIn(
                record["lineage"]["independence_verdict"], validator.INDEPENDENCE_VERDICTS
            )

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

    def test_every_source_directory_has_exactly_one_record(self):
        # The invariant is derived from what is actually in the repository, never hard-coded. The
        # historical 16 belongs to the CANON-003/004 instrumentation alone; the live corpus is
        # whatever currently exists, and each source directory holds exactly one active record.
        on_disk = sorted(
            p.name for p in (REPO_ROOT / "canon" / "knowledge" / "current").iterdir() if p.is_dir())
        audited = sorted(Path(r["knowledge_dir"]).name for r in self.records.values())
        self.assertEqual(audited, on_disk)
        self.assertEqual(len(self.records), len(on_disk))

    def test_committed_corpus_validates_clean(self):
        report = validator.validate_repository(REPO_ROOT)
        self.assertEqual(report["errors"], [])

    # ── CANON-005 promotion: one authoritative home, no second active copy ───────────────────
    def test_every_committed_record_declares_the_adopted_version(self):
        self.assertTrue(self.records)
        for name, record in self.records.items():
            with self.subTest(record=name):
                self.assertEqual(
                    record.get("audit_record_version"), validator.AUDIT_RECORD_VERSION,
                    f"{name} does not declare the adopted authoritative version",
                )

    def test_no_active_record_still_calls_itself_experimental(self):
        for name, record in self.records.items():
            with self.subTest(record=name):
                self.assertNotIn(
                    "experimental", str(record.get("audit_record_version")),
                    "an authoritative record must not self-identify as experimental",
                )

    def test_active_records_live_at_the_authoritative_path(self):
        self.assertEqual(validator.RECORDS_SUBPATH, Path("canon/audit/records"))
        self.assertTrue((REPO_ROOT / validator.RECORDS_SUBPATH).is_dir())

    def test_no_duplicate_active_records_under_the_retired_experimental_path(self):
        retired = REPO_ROOT / validator.RETIRED_RECORDS_SUBPATH
        leftovers = sorted(p.name for p in retired.glob("*.audit.yaml")) if retired.is_dir() else []
        self.assertEqual(
            leftovers, [],
            "audit records must exist in exactly one active location; downstream tooling cannot "
            "have two independently editable copies",
        )

    def test_a_reappearing_duplicate_copy_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active = root / validator.RECORDS_SUBPATH
            active.mkdir(parents=True)
            retired = root / validator.RETIRED_RECORDS_SUBPATH
            retired.mkdir(parents=True)
            (retired / "stray.audit.yaml").write_text("audit_id: aud_stray\n", encoding="utf-8")
            report = validator.validate_repository(root)
            self.assertTrue(
                any("duplicate active records" in e for e in report["errors"]), report["errors"]
            )

    def test_the_adopted_method_document_exists_and_is_authoritative(self):
        doc = REPO_ROOT / "canon" / "audit" / "AUDIT-GATE-v0.2.md"
        self.assertTrue(doc.is_file())
        text = doc.read_text(encoding="utf-8")
        self.assertIn("Status: AUTHORITATIVE", text)

    def test_every_record_still_carries_a_snapshot_after_promotion(self):
        for name, record in self.records.items():
            with self.subTest(record=name):
                snapshot = record.get("source_snapshot")
                self.assertIsInstance(snapshot, dict, f"{name} lost its source_snapshot")
                self.assertEqual(snapshot.get("algorithm"), validator.SNAPSHOT_ALGORITHM)
                self.assertEqual(
                    sorted(f["path"] for f in snapshot["files"]),
                    sorted(validator.SNAPSHOT_FILES),
                    f"{name} does not cover the adopted artifact set",
                )

    def test_all_seven_application_fit_consumers_survive_promotion(self):
        self.assertIn("deterministic_composition", validator.APPLICATION_CONSUMERS)
        self.assertIn("human_workflow", validator.APPLICATION_CONSUMERS)
        self.assertEqual(len(validator.APPLICATION_CONSUMERS), 7)
        for name, record in self.records.items():
            with self.subTest(record=name):
                covered = [f["consumer"] for f in record["application_fit"]["findings"]]
                self.assertEqual(sorted(covered), sorted(validator.APPLICATION_CONSUMERS))

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

    # ── shared_primary_informant: bibliographic authorship is not intellectual origin ────────
    def test_murch_and_the_conversations_cannot_be_two_independent_origins(self):
        ok, reason = validator.independent_origins_ok(
            "murch_blink_p1_25_editing_decisions",
            "ondaatje_conversations_third_conversation",
            self.records,
        )
        self.assertFalse(
            ok,
            "one practitioner recorded in two works must not count as independent convergence",
        )
        self.assertIn("shared_primary_informant", reason)

    def test_the_informant_dependence_is_declared_from_both_sides(self):
        def relation(a, b):
            record = next(r for r in self.records.values() if r["source_id"] == a)
            entry = next(
                e for e in record["lineage"]["related_sources_in_corpus"] if e["source_id"] == b)
            return entry["relation"]

        self.assertEqual(
            relation("murch_blink_p1_25_editing_decisions",
                     "ondaatje_conversations_third_conversation"),
            "shared_primary_informant")
        self.assertEqual(
            relation("ondaatje_conversations_third_conversation",
                     "murch_blink_p1_25_editing_decisions"),
            "shared_primary_informant")

    def test_murch_remains_an_independent_origin_against_unrelated_sources(self):
        # The dependence is pairwise. Blocking it globally would throw away the corpus's clearest
        # genuine convergence in order to catch one false one.
        for other in ("grammar_of_the_edit_ch3_5_editing_decisions",
                      "samara_making_breaking_grid_ch1",
                      "albers_interaction_of_color_ch1_5"):
            with self.subTest(other=other):
                ok, _ = validator.independent_origins_ok(
                    "murch_blink_p1_25_editing_decisions", other, self.records)
                self.assertTrue(ok)

    def test_the_conversations_remains_an_independent_origin_against_unrelated_sources(self):
        ok, _ = validator.independent_origins_ok(
            "ondaatje_conversations_third_conversation",
            "samara_making_breaking_grid_ch1",
            self.records,
        )
        self.assertTrue(ok)

    def test_shared_primary_informant_is_a_dependence_relation(self):
        self.assertIn("shared_primary_informant", validator.LINEAGE_RELATIONS)
        self.assertIn("shared_primary_informant", validator.DEPENDENT_RELATIONS)

    def test_shared_publisher_pair_in_the_real_corpus_stays_promotable(self):
        ok, _ = validator.independent_origins_ok(
            "freeman_photographers_eye_graphic_guide_parts1_3",
            "grammar_of_the_shot_ch4_continuity",
            self.records,
        )
        self.assertTrue(ok, "Focal Press alone must not defeat independence")


if __name__ == "__main__":
    unittest.main()
