"""Negative fixtures for the CANON_CONTEXT validator.

Each test mutates the committed worked example in one way and asserts the validator refuses it.
The point is that every rule in canon/context/CANON-CONTEXT-SPEC-v0.1.md is mechanically enforced
rather than merely written down — a spec whose rules only exist in prose is a convention.
"""
import hashlib
import tempfile
import unittest
from pathlib import Path

import yaml

from canon.validation import validate_canon_context as validator

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = REPO_ROOT / "canon/context/examples/B06-watch-hero.canon-context.yaml"


class CanonContextValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = validator.load_corpus()
        cls.example = yaml.safe_load(EXAMPLE.read_text())

    def check(self, ctx) -> list[str]:
        """Serialize a mutated context and run the validator over it."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.canon-context.yaml"
            path.write_text(yaml.safe_dump(ctx, sort_keys=False, allow_unicode=True))
            return validator.validate(path, self.corpus)

    def mutate(self):
        return yaml.safe_load(yaml.safe_dump(self.example))

    def assertRefused(self, errors, needle):
        self.assertTrue(errors, "expected the validator to refuse this context")
        joined = " | ".join(errors)
        self.assertIn(needle, joined)

    # ── the committed artifact ──────────────────────────────────────────
    def test_committed_example_passes_as_committed(self):
        self.assertEqual(validator.validate(EXAMPLE, self.corpus), [])

    def test_round_tripped_example_still_passes(self):
        self.assertEqual(self.check(self.mutate()), [])

    # ── R4: accepted Canon only ─────────────────────────────────────────
    def test_unknown_ref_is_refused(self):
        ctx = self.mutate()
        ctx["source_trace"][0]["ref"] = "sk_does_not_exist_0001"
        self.assertRefused(self.check(ctx), "not found in canon/knowledge/current")

    def test_hold_material_is_refused(self):
        """A candidate-source id resolves nowhere in accepted Canon, so it fails closed.

        The fixture must cite a source that is genuinely still held: the original one
        (google-abcd) was admitted to accepted Canon by DN-06 on 2026-09-01, which made its
        refs resolve and this test's premise false. airey-logo-design-love remains a HOLD
        candidate (REPLACEMENT-COPY blocked per DN-01), so its refs still resolve nowhere
        in canon/knowledge/current.
        """
        ctx = self.mutate()
        ctx["source_trace"].append({
            "ref": "sk_logo_0001", "kind": "source_knowledge",
            "source_dir": "airey-logo-design-love", "source_id": "airey-logo-design-love",
            "locator": "Logo Design Love", "audit_status": "complete"})
        self.assertRefused(self.check(ctx), "HOLD/candidate")

    def test_misdeclared_audit_status_is_refused(self):
        ctx = self.mutate()
        ctx["source_trace"][0]["audit_status"] = "provisional"
        self.assertRefused(self.check(ctx), "audit_status")

    def test_wrong_source_dir_is_refused(self):
        ctx = self.mutate()
        ctx["source_trace"][0]["source_dir"] = "vignelli-canon-intangibles"
        self.assertRefused(self.check(ctx), "corpus owner is")

    # ── R5: verbatim principles ─────────────────────────────────────────
    def test_paraphrased_principle_is_refused(self):
        ctx = self.mutate()
        ctx["key_guidance"][0]["principle"] = (
            "Put the light inside the family of angles to get a highlight on the case.")
        self.assertRefused(self.check(ctx), "not verbatim")

    def test_principle_improved_by_one_word_is_refused(self):
        ctx = self.mutate()
        ctx["key_guidance"][0]["principle"] += " This is always true."
        self.assertRefused(self.check(ctx), "not verbatim")

    def test_whitespace_only_difference_is_accepted(self):
        ctx = self.mutate()
        ctx["key_guidance"][0]["principle"] = \
            "\n  " + ctx["key_guidance"][0]["principle"] + "  \n"
        self.assertEqual(self.check(ctx), [])

    def test_condensed_principle_needs_review_and_digest(self):
        ctx = self.mutate()
        entry = ctx["key_guidance"][0]
        entry["render_mode"] = "condensed"
        entry["principle"] = "Light inside the family of angles produces a direct reflection."
        errors = self.check(ctx)
        self.assertRefused(errors, "condensed_review")
        self.assertRefused(errors, "source_digest")

    def test_condensed_principle_with_review_and_digest_is_accepted(self):
        ctx = self.mutate()
        entry = ctx["key_guidance"][0]
        ref = entry["rendered_from"]["ref"]
        kind, obj = self.corpus[0][ref]
        committed = validator.field_text(kind, obj, "claim")
        entry["render_mode"] = "condensed"
        entry["principle"] = "Light inside the family of angles produces a direct reflection."
        entry["rendered_from"]["condensed_review"] = "human"
        entry["rendered_from"]["source_digest"] = hashlib.sha256(
            validator.norm(committed).encode("utf-8")).hexdigest()
        self.assertEqual(self.check(ctx), [])

    # ── R1: budgets bite ────────────────────────────────────────────────
    def test_entry_budget_is_enforced(self):
        ctx = self.mutate()
        ctx["budget"]["max_guidance_entries"] = 2
        self.assertRefused(self.check(ctx), "max_guidance_entries")

    def test_byte_budget_is_enforced(self):
        ctx = self.mutate()
        ctx["budget"]["max_serialized_bytes"] = 1024
        self.assertRefused(self.check(ctx), "max_serialized_bytes")

    def test_principle_budget_is_enforced_separately(self):
        ctx = self.mutate()
        ctx["budget"]["max_principle_bytes"] = 512
        self.assertRefused(self.check(ctx), "max_principle_bytes")

    def test_budget_without_a_basis_is_refused(self):
        ctx = self.mutate()
        ctx["budget"]["basis"] = "  "
        self.assertRefused(self.check(ctx), "budget.basis is empty")

    # ── R2: questions and guidance answer each other ────────────────────
    def test_guidance_answering_no_question_is_refused(self):
        ctx = self.mutate()
        for question in ctx["production_questions"]:
            question["answered_by"] = [g for g in question["answered_by"] if g != "KG-03"]
        ctx["production_questions"] = [q for q in ctx["production_questions"] if q["answered_by"]]
        self.assertRefused(self.check(ctx), "KG-03: answers no production question")

    def test_question_with_no_answer_is_refused(self):
        ctx = self.mutate()
        ctx["production_questions"][0]["answered_by"] = []
        self.assertRefused(self.check(ctx), "answered_by is empty")

    def test_question_naming_a_missing_guidance_id_is_refused(self):
        ctx = self.mutate()
        ctx["production_questions"][0]["answered_by"] = ["KG-99"]
        self.assertRefused(self.check(ctx), "KG-99")

    # ── R3: nothing dangling ────────────────────────────────────────────
    def test_guidance_citing_an_untraced_ref_is_refused(self):
        ctx = self.mutate()
        ctx["source_trace"] = [t for t in ctx["source_trace"]
                               if t["ref"] != ctx["key_guidance"][1]["evidence"]["refs"][0]]
        self.assertRefused(self.check(ctx), "not in source_trace")

    # ── R6: uncertainty travels ─────────────────────────────────────────
    def test_empty_uncertainty_is_refused(self):
        ctx = self.mutate()
        ctx["key_guidance"][0]["uncertainty"] = ""
        self.assertRefused(self.check(ctx), "`uncertainty` is empty")

    def test_none_recorded_uncertainty_is_accepted(self):
        ctx = self.mutate()
        ctx["key_guidance"][0]["uncertainty"] = "none recorded"
        self.assertEqual(self.check(ctx), [])

    def test_every_mandatory_guidance_field_is_enforced(self):
        for field in ("principle", "applicability", "concrete_implication",
                      "failure_mode", "uncertainty"):
            with self.subTest(field=field):
                ctx = self.mutate()
                ctx["key_guidance"][0][field] = "   "
                self.assertRefused(self.check(ctx), f"`{field}` is empty")

    # ── R7: conflicts are surfaced with a rule ──────────────────────────
    def test_conflict_without_rule_or_unresolved_flag_is_refused(self):
        ctx = self.mutate()
        ctx["conflicts"][0]["resolution_rule"] = None
        ctx["conflicts"][0]["unresolved"] = False
        self.assertRefused(self.check(ctx), "needs a resolution_rule, or unresolved: true")

    def test_conflict_both_unresolved_and_resolved_is_refused(self):
        ctx = self.mutate()
        ctx["conflicts"][0]["unresolved"] = True
        self.assertRefused(self.check(ctx), "marked unresolved but also carries a resolution_rule")

    def test_honestly_unresolved_conflict_is_accepted(self):
        ctx = self.mutate()
        ctx["conflicts"][0]["resolution_rule"] = None
        ctx["conflicts"][0]["unresolved"] = True
        self.assertEqual(self.check(ctx), [])

    def test_one_sided_conflict_is_refused(self):
        ctx = self.mutate()
        ctx["conflicts"][0]["between"] = ctx["conflicts"][0]["between"][:1]
        self.assertRefused(self.check(ctx), "at least two distinct refs")

    def test_conflict_naming_an_untraced_ref_is_refused(self):
        ctx = self.mutate()
        ctx["conflicts"][0]["between"] = ["sk_lsm_c003_0004", "sk_vig_c003_0009"]
        self.assertRefused(self.check(ctx), "not in source_trace")

    # ── R8: limits are mandatory ────────────────────────────────────────
    def test_empty_do_not_overgeneralize_is_refused(self):
        ctx = self.mutate()
        ctx["do_not_overgeneralize"] = []
        self.assertRefused(self.check(ctx), "R8 requires at least one stated limit")

    def test_limit_pointing_at_a_missing_guidance_id_is_refused(self):
        ctx = self.mutate()
        ctx["do_not_overgeneralize"][0]["guidance_id"] = "KG-77"
        self.assertRefused(self.check(ctx), "KG-77")

    # ── structural ──────────────────────────────────────────────────────
    def test_missing_top_level_section_is_refused(self):
        for key in validator.TOP_LEVEL:
            with self.subTest(key=key):
                ctx = self.mutate()
                del ctx[key]
                self.assertRefused(self.check(ctx), f"missing required top-level key `{key}`")

    def test_wrong_version_is_refused(self):
        ctx = self.mutate()
        ctx["canon_context_version"] = "v0.2"
        self.assertRefused(self.check(ctx), "expected 'v0.1'")

    def test_duplicate_guidance_id_is_refused(self):
        ctx = self.mutate()
        ctx["key_guidance"][1]["guidance_id"] = ctx["key_guidance"][0]["guidance_id"]
        self.assertRefused(self.check(ctx), "duplicate guidance_id")


if __name__ == "__main__":
    unittest.main()
