"""Lane G, part A: the package renderer produces text the Canon gate parses without an
extraction error, and refuses (never pads or invents) when a prompt is unusable."""
from __future__ import annotations

import unittest

import test_g_support as G

from canon.gate import doctrine, package as gate_pkg, predispatch as gate_pre
from runtime.errors import Refusal
from runtime.loop import package, refusals

REGISTRY = doctrine.load_registry()


class RenderParses(unittest.TestCase):
    def setUp(self):
        self.spec = G.load_spec_dict(G.SPEC_OVERLAY)
        self.bp = G.blueprint_overlay()
        self.text = package.render_package(self.spec, self.bp)

    def test_headings_in_committed_order_and_known(self):
        headings = gate_pkg.section_headings(self.text)
        self.assertEqual(headings, list(package.SECTION_ORDER_STATIC))
        for h in headings:
            self.assertIn(h, gate_pkg.KNOWN_SECTION_HEADINGS)
        # nothing after the prompts that the corpus never places there
        opened = headings.index("GENERATION_PROMPTS")
        for h in headings[opened + 1:]:
            self.assertIn(h, gate_pkg.KNOWN_HEADINGS_AFTER_PROMPTS)

    def test_parses_as_v2_with_four_typed_subfields(self):
        pkg = gate_pkg.parse_package(self.text)
        self.assertEqual(pkg.schema, "v2")
        self.assertEqual(set(pkg.subfields), set(gate_pkg.TYPED_SUBFIELDS))
        for name in gate_pkg.TYPED_SUBFIELDS:
            self.assertTrue(pkg.subfields[name].strip(), name)

    def test_only_the_plate_prompt_is_extracted_under_code_composition(self):
        pkg = gate_pkg.parse_package(self.text)
        prompts = gate_pkg.extract_prompts(pkg)
        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0].text, self.bp["generation_prompts"]["textless_plate"])
        # C-6c: the in-scene main prompt belongs to a different route identity; it is not
        # in the package at all
        self.assertNotIn("दीपावली", self.text)

    def test_declared_aspect_matches_spec(self):
        pkg = gate_pkg.parse_package(self.text)
        self.assertEqual(gate_pkg.declared_aspect(pkg), "4:5")

    def test_exact_strings_listed_under_deterministic_elements(self):
        pkg = gate_pkg.parse_package(self.text)
        section = pkg.sections["DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS"]
        self.assertIn("मिठाई गिफ्ट बॉक्स ₹499", section)
        self.assertIn("HARD_CONSTRAINT_CHECK", pkg.sections)
        for line in self.spec["hard_constraints"]:
            self.assertIn(line, pkg.sections["HARD_CONSTRAINT_CHECK"])
        for req in self.spec["gate_requirements"]:
            self.assertIn(req, pkg.sections["FAILURE_PREVENTION"])

    def test_gate_pre_runs_without_extraction_error(self):
        """OBSERVED (2026-09-14): the frozen IMG-TEXT-01 plate prompt, copied verbatim, earns a
        LIMIT-TEXT FAIL at the gate — T3, 'poster' is a text-bearing-surface term and the first
        sentence carries no deferral/illegibility term. The blueprint's own header says the gate
        was never run on it. The renderer does not touch the prompt; the FAIL is the truth."""
        report = gate_pre.run_predispatch(
            self.text, None, {"generationConfig": {"imageConfig": {"aspectRatio": "4:5"}}},
            "static_image", True, REGISTRY)
        self.assertNotIn("ERROR", {r.status.name for r in report.results})
        limit = next(r for r in report.results if r.check_id == "LIMIT-TEXT")
        self.assertEqual(limit.status.name, "FAIL")
        self.assertIn("'poster'", limit.detail)

    def test_clean_plate_fixture_passes_limit_text(self):
        text = package.render_package(self.spec, G.blueprint_clean())
        report = gate_pre.run_predispatch(
            text, None, {"generationConfig": {"imageConfig": {"aspectRatio": "4:5"}}},
            "static_image", True, REGISTRY)
        by_id = {r.check_id: r for r in report.results}
        self.assertEqual(by_id["LIMIT-TEXT"].status.name, "PASS", by_id["LIMIT-TEXT"].detail)
        self.assertIn("explicit no-text clause present", by_id["LIMIT-TEXT"].detail)
        self.assertEqual(by_id["DISPATCH-ASPECT"].status.name, "PASS")
        self.assertEqual(report.verdict(), "PASS", report.render_text())

    def test_subfields_filled_from_case_values_not_invented(self):
        pkg = gate_pkg.parse_package(self.text)
        self.assertIn("1st read", pkg.subfields["attention_order"])
        self.assertIn("lower zone", pkg.subfields["placement_zone"])
        self.assertIn("matte", pkg.subfields["surface_finish_per_key_object"])
        self.assertIn("diya flames", pkg.subfields["implied_light_source"])

    def test_unstated_subfield_says_so(self):
        bp = G.blueprint_overlay()
        bp["case_values"] = {}
        text = package.render_package(self.spec, bp)
        pkg = gate_pkg.parse_package(text)
        for name in gate_pkg.TYPED_SUBFIELDS:
            self.assertEqual(pkg.subfields[name], package.NOT_STATED)

    def test_spec_composition_keys_take_precedence(self):
        spec = G.load_spec_dict(G.SPEC_OVERLAY)
        spec["composition"]["placement_zone"] = "lower-centre zone; the box sits low so the copy band stays clear"
        spec["materials_and_light"] = {"implied_light_source": "a single warm lamp from the upper left"}
        pkg = gate_pkg.parse_package(package.render_package(spec, self.bp))
        self.assertTrue(pkg.subfields["placement_zone"].startswith("lower-centre zone"))
        self.assertTrue(pkg.subfields["implied_light_source"].startswith("a single warm lamp"))


class RenderMotion(unittest.TestCase):
    def setUp(self):
        self.spec = G.load_spec_dict(G.SPEC_MOTION)
        self.bp = G.blueprint_motion()
        self.text = package.render_package(self.spec, self.bp)

    def test_deliverable_declares_aspect_duration_and_one_shot(self):
        pkg = gate_pkg.parse_package(self.text)
        self.assertEqual(gate_pkg.declared_aspect(pkg), "9:16")
        self.assertEqual(gate_pkg.declared_duration_s(pkg), 6.0)
        shots = gate_pkg.extract_shots(pkg)
        self.assertEqual(len(shots), 1)
        self.assertEqual(shots[0].duration_s_max, 6.0)

    def test_gate_pre_video_no_extraction_error(self):
        report = gate_pre.run_predispatch(
            self.text, None, {"parameters": {"aspectRatio": "9:16", "durationSeconds": 6}},
            "video", False, REGISTRY)
        by_id = {r.check_id: r for r in report.results}
        self.assertEqual(by_id["LIMIT-TEXT"].status.name, "PASS", by_id["LIMIT-TEXT"].detail)
        self.assertEqual(by_id["DISPATCH-ASPECT"].status.name, "PASS")
        self.assertEqual(by_id["DISPATCH-SHOT-SUM"].status.name, "PASS", by_id["DISPATCH-SHOT-SUM"].detail)


class RenderRefusals(unittest.TestCase):
    def setUp(self):
        self.spec = G.load_spec_dict(G.SPEC_OVERLAY)

    def test_short_prompt_is_a_refusal_not_padding(self):
        bp = G.blueprint_overlay()
        bp["generation_prompts"]["textless_plate"] = "A maroon plate with sweets, no text."
        with self.assertRaises(Refusal) as cm:
            package.render_package(self.spec, bp)
        self.assertEqual(cm.exception.code, refusals.PACKAGE_PROMPT_BELOW_FLOOR)
        self.assertEqual(cm.exception.context["floor"], gate_pkg.PROMPT_MIN_CHARS)

    def test_curly_quote_in_prompt_is_a_refusal(self):
        bp = G.blueprint_overlay()
        bp["generation_prompts"]["textless_plate"] = bp["generation_prompts"]["textless_plate"].replace(
            "Diwali festive", "Diwali “festive”")
        with self.assertRaises(Refusal) as cm:
            package.render_package(self.spec, bp)
        self.assertEqual(cm.exception.code, refusals.PACKAGE_CURLY_QUOTE)

    def test_missing_plate_prompt_under_code_composition_is_a_refusal(self):
        bp = G.blueprint_overlay()
        bp["generation_prompts"]["textless_plate"] = None
        with self.assertRaises(Refusal) as cm:
            package.render_package(self.spec, bp)
        self.assertEqual(cm.exception.code, refusals.PACKAGE_PROMPT_MISSING)

    def test_spec_value_that_would_read_as_a_heading_is_refused(self):
        spec = G.load_spec_dict(G.SPEC_OVERLAY)
        spec["hard_constraints"] = list(spec["hard_constraints"]) + ["IMPORTANT"]
        # rendered as a bullet, a bare ALL-CAPS constraint cannot open a section
        text = package.render_package(spec, G.blueprint_overlay())
        self.assertEqual(gate_pkg.section_headings(text), list(package.SECTION_ORDER_STATIC))

    def test_unknown_text_mechanism_is_a_refusal(self):
        spec = G.load_spec_dict(G.SPEC_OVERLAY)
        spec["exact_text"]["text_mechanism"] = "telepathy"
        with self.assertRaises(Refusal) as cm:
            package.render_package(spec, G.blueprint_overlay())
        self.assertEqual(cm.exception.code, refusals.PACKAGE_TEXT_MECHANISM_UNKNOWN)

    def test_dispatched_prompt_helper(self):
        self.assertEqual(package.dispatched_prompt_slot(self.spec), "textless_plate")
        spec = G.load_spec_dict(G.SPEC_IN_SCENE)
        self.assertEqual(package.dispatched_prompt_slot(spec), "main")
        self.assertEqual(package.dispatched_prompt_slot(G.load_spec_dict(G.SPEC_MOTION)), "motion")


if __name__ == "__main__":
    unittest.main()
