"""The reasoning pass at USD 0: a Stage-A-derived brief is planned from its frozen blueprint, parsed.

Nothing here calls a model. The blueprint bytes are read-only Lab material; the planner turns them
into the planner response shape deterministically, the compiler's own StyleGuard judges the
acceptance lines, and CanonCorpus — not the blueprint — computes the packs. The last test checks
the two agree for every case in use; a disagreement would be reported, not papered over.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

from runtime import paths
from runtime.errors import Refusal
from runtime.intake import Intake, JobStore
from runtime.canon.normalize import normalize
from runtime.canon.packs import CanonCorpus
from runtime.spec.blueprint_planner import BlueprintPlanner, first_sentence, parse_blueprint
from runtime.spec.compile import SpecCompiler
from runtime.spec.planner_seam import PlannerPrompt
from runtime.tests import support

FIXED = "2026-09-14T12:00:00Z"
CASES_IN_USE = ("img-text-02", "img-text-01", "img-core-01", "vid-i2v-01", "img-edit-01", "img-ref-02", "vid-topo3-01")


def alpha_brief(name: str, *, consent: bool = False) -> dict:
    raw = json.loads((paths.ALPHA_BRIEFS / f"{name}.json").read_text(encoding="utf-8"))
    if consent:
        for asset in raw.get("reference_assets") or []:
            if asset["depicts_identifiable_person"]:
                asset["consent_ref"] = "CONSENT-TEST-STAND-IN"
    return raw


def submit(name: str, **kw):
    return Intake(store=JobStore(tempfile.mkdtemp(prefix="runtime-e-"))).submit(alpha_brief(name, **kw))


def blueprint_text(case_id: str) -> str:
    return (paths.STAGE_A_BLUEPRINTS / f"{case_id}.blueprint.md").read_text(encoding="utf-8")


class ParseTest(unittest.TestCase):
    def test_img_text_02_parses_into_every_slot(self):
        parsed = parse_blueprint(blueprint_text("IMG-TEXT-02"))
        self.assertEqual(parsed["case_id"], "IMG-TEXT-02")
        self.assertEqual([p["pack_id"] for p in parsed["packs_selected"]][:3],
                         ["concept_and_distinctiveness", "critique_and_effectiveness", "composition_and_attention"])
        self.assertTrue(parsed["case_values"]["CA-D1"].startswith('1st read: "FLAT 40% OFF"'))
        self.assertIn("upper-left zone", parsed["case_values"]["CA-D2"])
        self.assertEqual(parsed["dispatch_parameters"]["aspect"], "1:1")
        self.assertEqual(parsed["dispatch_parameters"]["resolution"], "~1 MP")
        self.assertEqual(parsed["brief_only_parameters"]["light/mood"],
                         ["(scene mood) Key set by genre: high-contrast, hard-edged; mood from contrast, not from brightness."])
        prompts = parsed["generation_prompts"]
        self.assertTrue(prompts["main"].startswith("Bold square social-media poster for a gym offer."))
        self.assertTrue(prompts["textless_plate"].startswith("Bold square social-media poster background."))
        self.assertIn("No text, no letters, no numerals", prompts["textless_plate"])
        self.assertIsNone(prompts["motion"])

    def test_img_core_01_has_no_textless_plate_and_reads_the_pa_decisions(self):
        parsed = parse_blueprint(blueprint_text("IMG-CORE-01"))
        self.assertIsNone(parsed["generation_prompts"]["textless_plate"])
        self.assertIn("juice_bottle body: direct (glossy) glass", parsed["case_values"]["PA-D1"])
        self.assertIn("north-facing window camera-left", parsed["case_values"]["PA-D4"])
        self.assertEqual(parsed["text_handling"], ["mode: `none`"])

    def test_the_prompts_are_exactly_what_the_harness_casebook_extracts(self):
        """Same parser, imported: the runtime and the Lab can never disagree on prompt bytes."""
        hv2 = str(paths.HARNESS_V2)
        if hv2 not in sys.path:
            sys.path.insert(0, hv2)
        import hv2_paths  # noqa: F401
        import casebook

        for case_id in ("IMG-TEXT-02", "IMG-CORE-01", "VID-I2V-01", "VID-TOPO3-01"):
            text = blueprint_text(case_id)
            parsed = parse_blueprint(text)
            self.assertEqual(parsed["generation_prompts"]["main"], casebook.extract_prompt(text))
        text = blueprint_text("IMG-TEXT-02")
        self.assertEqual(parse_blueprint(text)["generation_prompts"]["textless_plate"],
                         casebook.extract_prompt(text, "C_composite_textless_base"))
        text = blueprint_text("VID-TOPO3-01")
        self.assertEqual(parse_blueprint(text)["generation_prompts"]["motion"],
                         casebook.extract_prompt(text, "A_cheap_still_to_cheap_i2v"))
        self.assertEqual(parse_blueprint(text)["generation_prompts"]["textless_plate"],
                         casebook.extract_prompt(text, "C_plate_9x16"))

    def test_a_blueprint_missing_a_section_is_refused_not_guessed(self):
        text = blueprint_text("IMG-TEXT-02").replace("## 4. dispatch_parameters", "## 4. something_else")
        with self.assertRaises(Refusal) as caught:
            parse_blueprint(text)
        self.assertEqual(caught.exception.code, Refusal.BLUEPRINT_UNPARSEABLE)
        self.assertEqual(caught.exception.context["section"], "dispatch_parameters")

    def test_first_sentence_is_the_customers_own_words(self):
        self.assertEqual(first_sentence("Hi team, we need an Instagram post for our New Year offer. It has to say"),
                         "Hi team, we need an Instagram post for our New Year offer.")
        self.assertEqual(first_sentence("दीपावली के लिए एक poster चाहिए। ऊपर लिखा हो"), "दीपावली के लिए एक poster चाहिए।")
        self.assertEqual(first_sentence("no terminator here"), "no terminator here")


class PlanTest(unittest.TestCase):
    def test_img_text_02_plans_from_its_blueprint_with_nothing_invented(self):
        result = submit("img-text-02")
        planner = BlueprintPlanner(provenance=result.provenance)
        plan = planner.plan(PlannerPrompt(system="", user=""), job=result.job, nr=normalize(result.job))
        self.assertEqual(plan["planner"], "stage_a_blueprint_fixture")
        self.assertTrue(plan["source_ref"].startswith("eval/empirical-planning/STAGE-A-FREEZE-2026-09/BLUEPRINTS/IMG-TEXT-02.blueprint.md sha256:"))
        self.assertIn(result.provenance["blueprint_sha256"], plan["source_ref"])
        self.assertEqual(plan["objective"],
                         'Produce one static_ad at 1:1 that answers the customer\'s request: '
                         '"Hi team, we need an Instagram post for our New Year offer."')
        self.assertEqual(plan["hard_constraints"],
                         ["three exact strings", "date communicated", "no human figures", "brand colours", "clean corner"])
        self.assertEqual(len(plan["acceptance_statements"]), 5)
        self.assertTrue(plan["acceptance_statements"][0].startswith('ACCEPT only if the lettering reads exactly "FLAT 40% OFF"'))
        self.assertEqual(set(plan["composition"]), {"attention_order", "placement_zone", "edge_treatment", "balance", "aspect_justification"})
        self.assertEqual(plan["materials_and_light"]["implied_light_source"],
                         "(scene mood) Key set by genre: high-contrast, hard-edged; mood from contrast, not from brightness.")
        self.assertEqual(plan["resolution_class"], "~1 MP")
        self.assertEqual(set(plan["case_values"]), {"CA-D1", "CA-D2", "CA-D3", "CA-D4", "CA-D5", "CA-D6"})

    def test_the_spec_blueprint_block_is_filled_from_the_frozen_bytes(self):
        result = submit("img-text-02")
        spec = SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=result.provenance).spec
        bp = spec["blueprint"]
        self.assertEqual(bp["planner"], "stage_a_blueprint_fixture")
        self.assertTrue(bp["generation_prompts"]["main"].startswith("Bold square social-media poster for a gym offer."))
        self.assertTrue(bp["generation_prompts"]["textless_plate"])
        self.assertIsNone(bp["generation_prompts"]["motion"])
        self.assertEqual(bp["case_values"]["CA-D4"], "None used.")
        self.assertEqual(bp["production_parameters"]["dispatch_parameters"]["aspect"], "1:1")
        self.assertIn("composite arm: font Inter Black", " ".join(bp["production_parameters"]["text_handling"]))
        # what the spec says about the job comes from the job, not from the blueprint
        self.assertEqual(spec["deliverable"]["aspect"], "1:1")
        self.assertEqual(spec["exact_text"]["strategy"], "code_set_on_textless_plate")
        self.assertEqual(spec["exact_text"]["text_mechanism"], "deterministic_text_composition")
        self.assertEqual(spec["policy_profile"], "dry")

    def test_the_same_brief_compiles_to_the_same_spec_twice(self):
        from runtime.util import canonical_json

        result = submit("img-text-02")
        first = SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=result.provenance).spec
        second = SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=result.provenance).spec
        self.assertEqual(canonical_json(first), canonical_json(second))

    def test_derived_acceptance_lines_hold_only_the_contractual_strings_exact(self):
        """IMG-TEXT-02's fourth string may re-flow ('readable in some wording'); the derived exact-read
        statement must not demand it character-exact, or it would contradict the case's own line."""
        result = submit("img-text-02")
        spec = SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=result.provenance).spec
        exact = [s for s in spec["acceptance_contract"] if s.startswith("ACCEPT only if the lettering reads exactly")]
        self.assertTrue(exact)
        self.assertNotIn("Offer ends 15 January", exact[0])
        self.assertIn("AlphaFit", exact[0])
        self.assertIn("ACCEPT only if the 15 January end date is readable in some wording.", spec["acceptance_contract"])

    def test_a_blueprint_whose_bytes_changed_is_a_refusal_not_a_replan(self):
        result = submit("img-text-02")
        prov = dict(result.provenance, blueprint_sha256="0" * 64)
        with self.assertRaises(Refusal) as caught:
            SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=prov)
        self.assertEqual(caught.exception.code, Refusal.BLUEPRINT_UNPARSEABLE)
        self.assertEqual(caught.exception.context["expected_sha256"], "0" * 64)

    def test_a_case_the_freeze_does_not_have_refuses_by_name(self):
        result = submit("img-text-02")
        prov = dict(result.provenance, case_id="IMG-TEXT-99", blueprint_ref=None)
        with self.assertRaises(Refusal) as caught:
            SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=prov)
        self.assertEqual(caught.exception.code, Refusal.PLANNER_FIXTURE_MISSING)
        self.assertEqual(caught.exception.context["case_id"], "IMG-TEXT-99")

    def test_a_case_line_that_fails_the_style_guard_is_a_refusal_naming_the_line_not_an_edit(self):
        """IMG-REF-02 and VID-TOPO3-01 open a line 'ACCEPT only if, ...' (comma). The runtime guard
        requires 'ACCEPT only if ' (space). The Stage-A build guard did not check openings. Reported."""
        for name in ("img-ref-02", "vid-topo3-01"):
            result = submit(name, consent=True)
            with self.assertRaises(Refusal) as caught:
                SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=result.provenance)
            self.assertEqual(caught.exception.code, Refusal.ACCEPTANCE_STYLE_VIOLATION, name)
            self.assertTrue(caught.exception.context["statement"].startswith("ACCEPT only if,"), name)

    def test_without_provenance_the_same_job_falls_back_to_the_recorded_fixture_planner(self):
        result = submit("img-text-02")
        with self.assertRaises(Refusal) as caught:
            SpecCompiler(planner=_NoFixtures()).compile(result.job, compiled_utc=FIXED)   # no provenance
        self.assertEqual(caught.exception.code, Refusal.PLANNER_FIXTURE_MISSING)

    def test_the_template_hook_is_offered_the_job_first(self):
        result = submit("img-text-02")
        offered = []

        def template_planner(prompt, *, job, nr):
            offered.append(job["job_id"])
            return None      # no template: fall through to the blueprint

        spec = SpecCompiler(template_planner=template_planner).compile(
            result.job, compiled_utc=FIXED, provenance=result.provenance).spec
        self.assertEqual(offered, ["alpha-dry-img-text-02"])
        self.assertEqual(spec["blueprint"]["planner"], "stage_a_blueprint_fixture")


class _NoFixtures:
    def plan(self, prompt, *, job=None, nr=None):
        raise Refusal(Refusal.PLANNER_FIXTURE_MISSING, "no fixture", prompt_sha256=prompt.sha256)


class PacksAgreeWithTheBlueprintTest(unittest.TestCase):
    def test_canon_corpus_selects_exactly_the_packs_the_frozen_blueprint_lists(self):
        """canon.packs_selected is COMPUTED by CanonCorpus from the job; §1 of the blueprint was computed
        by the Lab from the same Normalized Request. Every case in use agrees, id by id, in order, with
        the same compiled/uncompiled status. If this ever fails, report the discrepancy — do not read §1."""
        corpus = CanonCorpus()
        for name in CASES_IN_USE:
            result = submit(name, consent=True)
            ours = [(s.pack_id, s.status == "compiled_accepted") for s in corpus.select(normalize(result.job))]
            parsed = parse_blueprint((paths.STAGE_A_FREEZE / result.provenance["blueprint_ref"]).read_text(encoding="utf-8"))
            theirs = [(p["pack_id"], p["compiled"]) for p in parsed["packs_selected"]]
            self.assertEqual(ours, theirs, name)

    def test_the_blueprint_sha_in_the_brief_matches_the_bytes_on_disk_and_test_cases(self):
        import yaml

        doc = yaml.safe_load(paths.STAGE_A_TEST_CASES.read_text(encoding="utf-8"))
        recorded = {c["case_id"]: c.get("blueprint_sha256") for c in doc["cases"]}
        for name in CASES_IN_USE:
            prov = alpha_brief(name)["_provenance"]
            on_disk = hashlib.sha256((paths.STAGE_A_FREEZE / prov["blueprint_ref"]).read_bytes()).hexdigest()
            self.assertEqual(prov["blueprint_sha256"], on_disk, name)
            self.assertEqual(prov["blueprint_sha256"], recorded[prov["case_id"]], name)


if __name__ == "__main__":
    unittest.main()
