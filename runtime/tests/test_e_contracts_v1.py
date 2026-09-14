"""Lane E (14 Sep 2026): intake and the compiler run against the v1 contracts, and the spec they
emit is the one the router reads.

The defects these close were found by the lead and lane D, not by reading the contracts:

  D1  paths bound JOB_CONTRACT / SPEC_CONTRACT to the v0 files; consent keyed on role == 'person';
      the spec had no `schema` and no `policy_profile`, so runtime/route/spec.py refused it.
  D2  normalize._text_in_scene() hard-returned False; operation/modality were not checked against
      KIND-NR-BINDING.
  D3  the lettering prohibitions text_strategy computes were never written to route_exclusions.
  D4  exact_text_strategies_allowed and motion_requires_accepted_still were data nothing read.
  D5  canon.missing_domain was one string; v1 says missing_domains, a list.
  D6  no text_mechanism (C-6c vocabulary) on the spec.
"""
from __future__ import annotations

import copy
import unittest

from runtime import paths
from runtime.canon.normalize import normalize
from runtime.errors import Refusal
from runtime.policy import PolicyProfiles
from runtime.route.spec import Spec
from runtime.spec.compile import SpecCompiler, contract_view
from runtime.tests import support

FIXED = "2026-09-10T12:00:00Z"
BRIEFS = ("mustard-oil-tin", "showroom-photo-edit", "lipstick-packshot")


class Recorded:
    """A planner that answers ANY prompt with one recorded response. For tests that alter a fixture
    brief (so its prompt bytes have no recorded answer) and are about something other than the plan."""

    def __init__(self, name: str):
        import json

        from runtime.spec.planner_seam import validate_response

        path = paths.PLANNER_FIXTURES / f"{name}.response.json"
        self.response = validate_response(json.loads(path.read_text(encoding="utf-8")), source=str(path))

    def plan(self, prompt, *, job=None, nr=None) -> dict:
        return dict(self.response)


def person_asset(**over) -> dict:
    asset = {
        "asset_id": "ast_founder_portrait",
        "role": "person",
        "sha256": "aa" * 32,
        "content_type": "image/jpeg",
        "provenance": "customer_supplied",
        "depicts_identifiable_person": True,
    }
    asset.update(over)
    return asset


class D1ContractsAreV1(unittest.TestCase):
    def test_paths_bind_both_contracts_to_v1(self):
        self.assertTrue(str(paths.JOB_CONTRACT).endswith("PRODUCTION-JOB-v1.yaml"))
        self.assertTrue(str(paths.SPEC_CONTRACT).endswith("PRODUCTION-SPEC-v1.yaml"))

    def test_consent_keys_on_depiction_not_on_role(self):
        """The v0 hole: a `scene` photograph depicting a real member of staff passed the gate."""
        raw = copy.deepcopy(support.brief("showroom-photo-edit"))
        scene = [a for a in raw["reference_assets"] if a["role"] == "scene"][0]
        self.assertTrue(scene["depicts_identifiable_person"])
        del scene["consent_ref"]
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.CONSENT_MISSING)
        self.assertEqual(caught.exception.context["asset_id"], scene["asset_id"])
        self.assertEqual(caught.exception.context["role"], "scene")

    def test_a_person_role_asset_that_depicts_nobody_is_not_a_consent_case(self):
        """The field, not the label, decides: a `person` role with depicts false passes (v1 invariant)."""
        raw = copy.deepcopy(support.brief("lipstick-packshot"))
        raw["reference_assets"].append(person_asset(depicts_identifiable_person=False))
        job = support.intake().submit(raw).job
        self.assertEqual(len(job["reference_assets"]), 3)

    def test_depicts_identifiable_person_may_not_be_omitted(self):
        raw = copy.deepcopy(support.brief("lipstick-packshot"))
        asset = person_asset(consent_ref="CONSENT-X")
        del asset["depicts_identifiable_person"]
        raw["reference_assets"].append(asset)
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.SCHEMA_VIOLATION)
        self.assertIn("depicts_identifiable_person", caught.exception.context["field"])

    def test_the_spec_carries_schema_and_policy_profile_and_the_router_reads_it(self):
        for name in BRIEFS:
            job = support.submit(name)
            spec = SpecCompiler().compile(job, compiled_utc=FIXED).spec
            self.assertEqual(spec["schema"], "PRODUCTION-SPEC-v1")
            self.assertEqual(spec["policy_profile"], job["policy_profile"])
            loaded = Spec(path=paths.RUNTIME / f"{name}.yaml", data=spec)   # refuses on a v0-shaped spec
            self.assertEqual(loaded.kind, job["deliverable_request"]["kind"])
            self.assertEqual(loaded.spec_id, spec["spec_id"])

    def test_the_declared_part_still_validates_against_the_frozen_v1_contract(self):
        from runtime.contract_schema import Contract

        contract = Contract.load(paths.SPEC_CONTRACT)
        for name in BRIEFS:
            spec = SpecCompiler().compile(support.submit(name), compiled_utc=FIXED).spec
            contract.validate(contract_view(spec))


class D2InSceneAndBinding(unittest.TestCase):
    def test_placement_in_scene_sets_the_facet(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "dry"
        raw["exact_text_strings"][1]["placement"] = "in_scene"
        nr = normalize(support.intake().submit(raw).job)
        self.assertTrue(nr.facets["text_in_scene"])
        self.assertEqual([t["placement"] for t in nr.text_requirements], ["overlay", "in_scene", "overlay"])

    def test_placement_defaults_to_overlay_and_the_facet_stays_false(self):
        nr = normalize(support.submit("mustard-oil-tin"))
        self.assertFalse(nr.facets["text_in_scene"])
        self.assertTrue(all(t["placement"] == "overlay" for t in nr.text_requirements))

    def test_operation_must_agree_with_the_binding_row(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["deliverable_request"]["operation"] = "edit"          # static_ad binds to generate
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.SCHEMA_VIOLATION)
        self.assertIn("KIND-NR-BINDING", caught.exception.message)
        self.assertIn("'edit'", caught.exception.message)
        self.assertIn("'generate'", caught.exception.message)

    def test_modality_must_agree_with_the_binding_row(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["deliverable_request"]["modality"] = "video"
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.SCHEMA_VIOLATION)
        self.assertEqual(caught.exception.context["field"], "deliverable_request.modality")

    def test_operation_and_modality_are_required_in_v1(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        del raw["deliverable_request"]["operation"]
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.SCHEMA_VIOLATION)


class D3RouteExclusionsCarryScope(unittest.TestCase):
    def test_a_lettering_prohibition_is_written_with_scope_generated_text_only(self):
        """RR-3 forbids three routes from DRAWING Devanagari. The mustard-oil job sets its Devanagari by
        code, so the same prohibition is carried with the narrow scope, never as a whole-route ban."""
        spec = SpecCompiler().compile(support.submit("mustard-oil-tin"), compiled_utc=FIXED).spec
        rows = spec["route_exclusions"]
        self.assertEqual(sorted(r["route_key"] for r in rows), ["flux-2-pro", "recraft-v4", "seedream-5-pro"])
        for row in rows:
            self.assertEqual(row["scope"], "generated_text_only", row)
            self.assertIn("RR-3", row["basis"])
            self.assertIn("IMG-", row["basis"])            # the map cells are named
            self.assertTrue(row["reason"])

    def test_no_exclusion_is_invented_where_no_rule_is_in_scope(self):
        spec = SpecCompiler().compile(support.submit("showroom-photo-edit"), compiled_utc=FIXED).spec
        self.assertEqual(spec["route_exclusions"], [])

    def test_the_router_reads_the_exclusions_it_is_given(self):
        spec = SpecCompiler().compile(support.submit("mustard-oil-tin"), compiled_utc=FIXED).spec
        loaded = Spec(path=paths.RUNTIME / "x.yaml", data=spec)
        self.assertEqual(sorted(e.route_key for e in loaded.exclusions()), ["flux-2-pro", "recraft-v4", "seedream-5-pro"])


class D4ProfileLimitsAreEnforced(unittest.TestCase):
    def test_a_strategy_outside_the_profile_list_is_a_refusal_naming_the_ruling(self):
        """alpha_human_release allows code_set_on_textless_plate only (C-7). An in-scene request under
        it is refused by name, with the profile's own note as the basis. Never a silent downgrade."""
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "alpha_human_release"
        raw["exact_text_strings"][1]["placement"] = "in_scene"
        for item in raw["exact_text_strings"]:
            item["may_reflow"] = True     # otherwise RR-1's contractual default wins over RR-2
        job = support.intake().submit(raw).job
        with self.assertRaises(Refusal) as caught:
            SpecCompiler().compile(job, compiled_utc=FIXED)
        self.assertEqual(caught.exception.code, Refusal.TEXT_STRATEGY_NOT_ALLOWED_BY_PROFILE)
        self.assertEqual(caught.exception.context["strategy"], "generated_in_scene")
        self.assertEqual(caught.exception.context["allowed"], ["code_set_on_textless_plate"])
        self.assertIn("C-7", caught.exception.context["basis"])

    def test_the_same_job_compiles_under_a_profile_that_allows_the_strategy(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "dry"
        raw["exact_text_strings"][1]["placement"] = "in_scene"
        for item in raw["exact_text_strings"]:
            item["may_reflow"] = True
        job = support.intake().submit(raw).job
        spec = SpecCompiler(planner=Recorded("mustard-oil-tin")).compile(job, compiled_utc=FIXED).spec
        self.assertEqual(spec["exact_text"]["strategy"], "generated_in_scene")
        self.assertEqual(spec["exact_text"]["text_mechanism"], "model_draws_text")
        # The scope is a property of the PROHIBITION, not of the strategy: RR-3 is about drawing
        # Devanagari, so it stays generated_text_only. Here the model draws the text, so the router
        # reading scope + text_mechanism drops these routes for this job; under code-set text the
        # same rows leave the plate route usable.
        rows = spec["route_exclusions"]
        self.assertEqual(sorted(r["route_key"] for r in rows), ["flux-2-pro", "recraft-v4", "seedream-5-pro"])
        self.assertTrue(all(r["scope"] == "generated_text_only" for r in rows))
        self.assertNotIn("flux-2-pro", spec["exact_text"]["strategy_basis"].split("map cells:")[1].split(";")[0])

    def test_the_allowed_list_is_read_from_the_profile_object_not_from_code(self):
        from runtime.policy.profiles import PolicyProfile

        seen = []
        original = PolicyProfile.limit

        def spy(self, limit_name):
            value = original(self, limit_name)
            seen.append(limit_name)
            return value

        PolicyProfile.limit = spy
        try:
            SpecCompiler().compile(support.submit("mustard-oil-tin"), compiled_utc=FIXED)
        finally:
            PolicyProfile.limit = original
        self.assertIn("exact_text_strategies_allowed", seen)

    def test_motion_without_depends_on_is_refused_where_the_profile_requires_the_accepted_still(self):
        raw = copy.deepcopy(support.brief("lipstick-packshot"))
        raw["policy_profile"] = "alpha_human_release"        # motion_requires_accepted_still: true
        self.assertNotIn("depends_on", raw["deliverable_request"]["motion"])
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.MOTION_DEPENDENCY_MISSING)
        self.assertIn("motion_requires_accepted_still", caught.exception.message)

    def test_motion_from_anything_but_the_accepted_still_is_refused_under_that_profile(self):
        raw = copy.deepcopy(support.brief("lipstick-packshot"))
        raw["policy_profile"] = "alpha_human_release"
        raw["deliverable_request"]["motion"]["from"] = "text_to_video"
        raw["deliverable_request"]["motion"]["depends_on"] = "still"
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.MOTION_DEPENDENCY_MISSING)

    def test_motion_naming_the_accepted_still_passes_and_reaches_the_spec(self):
        raw = copy.deepcopy(support.brief("lipstick-packshot"))
        raw["policy_profile"] = "alpha_human_release"
        raw["deliverable_request"]["motion"]["depends_on"] = "still"
        job = support.intake().submit(raw).job
        spec = SpecCompiler(planner=Recorded("lipstick-packshot")).compile(job, compiled_utc=FIXED).spec
        self.assertEqual(spec["deliverable"]["motion"]["depends_on"], "still")
        self.assertEqual(spec["deliverable"]["motion"]["from"], "accepted_still")

    def test_a_still_with_no_motion_block_is_not_asked_for_a_dependency(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "alpha_human_release"
        job = support.intake().submit(raw).job
        self.assertNotIn("motion", job["deliverable_request"])

    def test_the_dry_profile_does_not_require_the_dependency(self):
        profile = PolicyProfiles().profile("dry")
        self.assertFalse(profile.motion_requires_accepted_still)
        job = support.submit("lipstick-packshot")
        self.assertEqual(job["policy_profile"], "dry")
        self.assertNotIn("depends_on", job["deliverable_request"]["motion"])


class D5MissingDomainsIsAList(unittest.TestCase):
    def test_missing_domains_lists_each_absent_doctrine(self):
        spec = SpecCompiler().compile(support.submit("mustard-oil-tin"), compiled_utc=FIXED).spec
        self.assertNotIn("missing_domain", spec["canon"])
        self.assertIsInstance(spec["canon"]["missing_domains"], list)
        self.assertTrue(spec["canon"]["canon_gap"])
        self.assertIn("typography_and_copy", spec["canon"]["missing_domains"])
        self.assertEqual(spec["canon"]["missing_domains"], sorted(spec["canon"]["missing_domains"]))
        gap_lines = [g for g in spec["gate_requirements"] if g.startswith("canon gap:")]
        self.assertEqual(len(gap_lines), 1)
        self.assertIn("typography_and_copy", gap_lines[0])


class D6TextMechanism(unittest.TestCase):
    def test_code_set_maps_to_deterministic_text_composition(self):
        spec = SpecCompiler().compile(support.submit("mustard-oil-tin"), compiled_utc=FIXED).spec
        self.assertEqual(spec["exact_text"]["strategy"], "code_set_on_textless_plate")
        self.assertEqual(spec["exact_text"]["text_mechanism"], "deterministic_text_composition")
        self.assertTrue(all(s["placement"] == "overlay" for s in spec["exact_text"]["strings"]))

    def test_no_exact_text_maps_to_not_applicable(self):
        spec = SpecCompiler().compile(support.submit("showroom-photo-edit"), compiled_utc=FIXED).spec
        self.assertEqual(spec["exact_text"]["strategy"], "no_exact_text")
        self.assertEqual(spec["exact_text"]["text_mechanism"], "not_applicable")

    def test_the_mechanism_comes_from_the_facet_table_not_from_a_dict_in_code(self):
        from runtime.spec.compile import text_mechanism_for

        self.assertEqual(text_mechanism_for("code"), "deterministic_text_composition")
        self.assertEqual(text_mechanism_for("maker"), "model_draws_text")
        self.assertEqual(text_mechanism_for("none"), "not_applicable")
        with self.assertRaises(Refusal):
            text_mechanism_for("telepathy")


class BlueprintBlockOnRecordedFixtures(unittest.TestCase):
    def test_a_recorded_fixture_plan_yields_a_blueprint_block_that_says_so(self):
        spec = SpecCompiler().compile(support.submit("mustard-oil-tin"), compiled_utc=FIXED).spec
        bp = spec["blueprint"]
        self.assertEqual(bp["planner"], "recorded_fixture")
        self.assertIn("mustard-oil-tin.response.json", bp["source_ref"])
        self.assertEqual(set(bp["generation_prompts"]), {"main", "textless_plate", "motion"})
        self.assertIsInstance(bp["generation_prompts"]["main"], str)
        self.assertEqual(bp["case_values"], {})


if __name__ == "__main__":
    unittest.main()
