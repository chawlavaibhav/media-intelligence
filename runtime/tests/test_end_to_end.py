"""One command, three real Indian commercial briefs, three complete specs.

No hand-editing anywhere between the brief and the spec: the whole path is intake -> Normalized
Request -> Canon lookup -> text-strategy rule -> one recorded reasoning pass -> spec.
"""
from __future__ import annotations

import json
import unittest

from runtime import paths
from runtime.canon.normalize import normalize
from runtime.tests import support
from runtime.util import canonical_json

FIXED = "2026-09-10T12:00:00Z"


class MustardOilTest(unittest.TestCase):
    """A Kanpur mill's mustard-oil tin with an exact Hindi price line."""

    @classmethod
    def setUpClass(cls):
        cls.job = support.submit("mustard-oil-tin")
        cls.compiled = support.compiler().compile(cls.job, compiled_utc=FIXED)
        cls.spec = cls.compiled.spec

    def test_the_price_line_is_set_by_code_because_exactness_is_contractual(self):
        self.assertEqual(self.spec["exact_text"]["strategy"], "code_set_on_textless_plate")
        self.assertIn("RR-1", self.spec["exact_text"]["strategy_basis"])

    def test_the_price_survives_verbatim_into_the_spec(self):
        values = [s["content"] for s in self.spec["exact_text"]["strings"]]
        self.assertIn("₹185 प्रति लीटर", values)
        self.assertTrue(all(s["exactness"] == "contractual" for s in self.spec["exact_text"]["strings"]))

    def test_the_customers_own_words_reach_the_hard_constraints(self):
        joined = " ".join(self.spec["hard_constraints"])
        self.assertIn("No people in the picture", joined)
        self.assertIn("bilkul same rehna chahiye", joined)

    def test_the_product_pack_fires_because_a_product_photo_was_supplied(self):
        rows = {r["pack_id"]: r for r in self.spec["canon"]["packs_selected"]}
        self.assertTrue(rows["product_appearance"]["compiled"])
        self.assertIn("product_or_packshot_entity_present", rows["product_appearance"]["trigger"])

    def test_the_gate_carries_the_devanagari_limit_the_packs_state(self):
        joined = " ".join(self.spec["gate_requirements"])
        self.assertIn("never generate Devanagari glyphs", joined)


class ShowroomEditTest(unittest.TestCase):
    """A Rajkot furniture showroom photograph with a staff member to remove."""

    @classmethod
    def setUpClass(cls):
        cls.job = support.submit("showroom-photo-edit")
        cls.spec = support.compiler().compile(cls.job, compiled_utc=FIXED).spec

    def test_it_is_an_edit_on_a_supplied_photograph(self):
        nr = normalize(self.job)
        self.assertEqual(nr.requested_operation, "edit")
        self.assertEqual(nr.specification_provenance["requested_operation"], "customer_stated")

    def test_no_lettering_strategy_is_chosen_because_no_string_was_named(self):
        self.assertEqual(self.spec["exact_text"]["strategy"], "no_exact_text")
        self.assertEqual(self.spec["exact_text"]["strings"], [])

    def test_the_baked_text_scan_is_the_deterministic_check_not_a_string_probe(self):
        joined = " ".join(self.spec["deterministic_checks"])
        self.assertIn("baked-text scan", joined)
        self.assertNotIn("required string absent", joined)

    def test_the_sofas_identity_must_survive(self):
        self.assertIn("product", self.spec["identity_requirements"]["preserve"])
        self.assertTrue(self.spec["identity_requirements"]["decoy_check"])

    def test_the_person_removal_is_decidable_from_the_artifact(self):
        joined = " ".join(self.spec["acceptance_contract"])
        self.assertIn("person", joined)


class LipstickPackshotTest(unittest.TestCase):
    """A Mumbai cosmetics launch: a packshot with a Hindi headline and a silent 6 s version."""

    @classmethod
    def setUpClass(cls):
        cls.job = support.submit("lipstick-packshot")
        cls.spec = support.compiler().compile(cls.job, compiled_utc=FIXED).spec

    def test_the_motion_request_reaches_the_deliverable_and_the_capabilities(self):
        self.assertEqual(self.spec["deliverable"]["motion"]["seconds"], 6)
        capabilities = {r["capability"] for r in self.spec["capability_requirements"]}
        self.assertIn("image_to_video", capabilities)
        self.assertNotIn("native_audio", capabilities)

    def test_text_that_must_move_is_never_drawn_by_the_maker(self):
        self.assertEqual(self.spec["exact_text"]["strategy"], "code_set_on_textless_plate")
        self.assertIn("RR-6", self.spec["exact_text"]["strategy_basis"])

    def test_an_uncertain_modality_widened_the_pack_set_rather_than_guessing(self):
        triggers = {r["pack_id"]: r["trigger"] for r in self.spec["canon"]["packs_selected"]}
        self.assertIn("uncertainty_rule", triggers["composition_and_attention"])
        self.assertIn("editing_pacing_and_short_form", triggers)

    def test_the_limits_come_from_the_profile_the_job_named(self):
        self.assertEqual(self.job["policy_profile"], "dry")
        self.assertEqual(self.spec["budget"]["max_provider_draws"], 0)
        self.assertEqual(self.spec["budget"]["repair_allowance"], 0)


class NoHandAuthoringTest(unittest.TestCase):
    def test_a_brief_on_disk_produces_a_complete_spec_with_no_step_in_between(self):
        for name in ("mustard-oil-tin", "showroom-photo-edit", "lipstick-packshot"):
            with open(paths.BRIEF_FIXTURES / f"{name}.json", "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            result = support.intake().submit(raw)
            compiled = support.compiler().compile(result.job, compiled_utc=FIXED)
            self.assertTrue(compiled.spec["objective"])
            self.assertTrue(compiled.spec["acceptance_contract"])
            self.assertTrue(compiled.canon_payload)
            self.assertEqual(
                compiled.spec["canon"]["injected_context_sha256"],
                support.compiler().compile(result.job, compiled_utc=FIXED).spec["canon"]["injected_context_sha256"],
            )

    def test_the_three_briefs_compile_to_three_stable_specs(self):
        seen = {}
        for name in ("mustard-oil-tin", "showroom-photo-edit", "lipstick-packshot"):
            job = support.submit(name)
            seen[name] = canonical_json(support.compiler().compile(job, compiled_utc=FIXED).spec)
        for name, blob in seen.items():
            job = support.submit(name)
            self.assertEqual(blob, canonical_json(support.compiler().compile(job, compiled_utc=FIXED).spec), name)


if __name__ == "__main__":
    unittest.main()
