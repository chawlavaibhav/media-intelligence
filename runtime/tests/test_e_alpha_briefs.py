"""The alpha briefs: derived from frozen cases by a tool, committed, regenerable byte for byte, and —
for the one that matters most — carried through intake, compile, the spec file on disk, the router's
loader and the router's plan, offline, under the dry profile.

The lanes never connected before this: intake produced a v0-shaped spec and runtime/route/spec.py
refused it. The end-to-end test below is the proof that they connect now.
"""
from __future__ import annotations

import contextlib
import io
import json
import socket
import ssl
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

try:
    import _bootstrap as B                       # unittest discover -s runtime/tests
except ImportError:                              # python3 -m unittest runtime.tests.test_e_alpha_briefs
    from runtime.tests import _bootstrap as B

from runtime import cli, paths
from runtime.errors import Refusal
from runtime.intake import Intake, JobStore
from runtime.route.spec import load_spec
from runtime.spec.compile import SpecCompiler
from runtime.tools import brief_from_marketplace_case, brief_from_stage_a_case
from runtime.util import canonical_json

FIXED = "2026-09-14T12:00:00Z"
GENERATED = {
    "img-text-02": ("IMG-TEXT-02", {}),
    "img-text-01": ("IMG-TEXT-01", {}),
    "img-core-01": ("IMG-CORE-01", {}),
    "vid-i2v-01": ("VID-I2V-01", {"depends_on": "alpha-dry-img-core-01"}),
    "img-edit-01": ("IMG-EDIT-01", {}),
    "img-ref-02": ("IMG-REF-02", {}),
    "vid-topo3-01": ("VID-TOPO3-01", {"depends_on": "alpha-dry-img-text-01"}),
}


def committed(name: str) -> dict:
    return json.loads((paths.ALPHA_BRIEFS / f"{name}.json").read_text(encoding="utf-8"))


def fresh_intake() -> Intake:
    return Intake(store=JobStore(tempfile.mkdtemp(prefix="runtime-e-")))


class ToolDeterminismTest(unittest.TestCase):
    def test_every_committed_brief_regenerates_byte_for_byte(self):
        for name, (case_id, kw) in GENERATED.items():
            regenerated = brief_from_stage_a_case.derive(case_id, **kw)
            self.assertEqual(canonical_json(regenerated), canonical_json(committed(name)), name)
        self.assertEqual(canonical_json(brief_from_marketplace_case.derive("MKT-001")), canonical_json(committed("mkt-001")))

    def test_the_customers_words_are_verbatim_and_nothing_is_inferred_about_placement(self):
        import yaml

        cases = {c["case_id"]: c for c in yaml.safe_load(paths.STAGE_A_TEST_CASES.read_text(encoding="utf-8"))["cases"]}
        for name, (case_id, _) in GENERATED.items():
            brief = committed(name)
            self.assertEqual(brief["brief"]["text"], cases[case_id]["customer_request"]["text"], name)
            self.assertEqual(brief["_provenance"]["source_pool"], "stage_a_case")
            for item in brief.get("exact_text_strings") or []:
                self.assertEqual(item["placement"], "overlay", name)
            self.assertEqual(brief["_provenance"]["placement_default"], bool(brief.get("exact_text_strings")), name)
            self.assertEqual(brief["job_id"], f"alpha-dry-{case_id.lower()}")
            self.assertEqual(brief["policy_profile"], "dry")
            self.assertNotIn("delete_after_days", brief["retention"])      # the profile fills it at intake

    def test_an_unmapped_family_is_refused_not_guessed(self):
        with self.assertRaises(Refusal) as caught:
            brief_from_stage_a_case.derive("VID-REF-01")
        self.assertEqual(caught.exception.context["family"], "VID-REF")

    def test_approximate_strings_may_reflow_exact_ones_may_not(self):
        strings = {s["value"]: s["may_reflow"] for s in committed("img-text-02")["exact_text_strings"]}
        self.assertFalse(strings["FLAT 40% OFF"])
        self.assertTrue(strings["Offer ends 15 January"])


class ConsentGateOnDerivedBriefsTest(unittest.TestCase):
    def test_img_edit_01_refuses_without_consent_because_the_photo_depicts_the_staff_member(self):
        raw = committed("img-edit-01")
        asset = raw["reference_assets"][0]
        self.assertEqual(asset["role"], "scene")
        self.assertTrue(asset["depicts_identifiable_person"])
        self.assertNotIn("consent_ref", asset)
        self.assertIn("staff_member", raw["_provenance"]["depicts_basis"]["showroom_sofa_01"])
        with self.assertRaises(Refusal) as caught:
            fresh_intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.CONSENT_MISSING)
        self.assertEqual(caught.exception.context["asset_id"], "showroom_sofa_01")
        self.assertEqual(caught.exception.context["role"], "scene")

    def test_img_edit_01_is_accepted_and_compiles_with_a_consent_ref(self):
        raw = brief_from_stage_a_case.derive("IMG-EDIT-01", consent_ref="CONSENT-2026-09-14-TEST-01")
        self.assertEqual(raw["reference_assets"][0]["consent_ref"], "CONSENT-2026-09-14-TEST-01")
        self.assertTrue(raw["_provenance"]["consent_ref_added"])
        result = fresh_intake().submit(raw)
        self.assertTrue(result.created)
        spec = SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=result.provenance).spec
        self.assertEqual(spec["deliverable"]["kind"], "static_ad_from_supplied_photo")
        self.assertEqual(spec["deliverable"]["aspect"], "as_supplied")
        self.assertEqual(spec["exact_text"]["text_mechanism"], "not_applicable")
        self.assertEqual(spec["blueprint"]["planner"], "stage_a_blueprint_fixture")
        self.assertIn("REJECT if any person, or part of a person, remains anywhere in the image.", spec["acceptance_contract"])

    def test_img_ref_02_refuses_for_the_same_reason_on_a_person_reference(self):
        with self.assertRaises(Refusal) as caught:
            fresh_intake().submit(committed("img-ref-02"))
        self.assertEqual(caught.exception.code, Refusal.CONSENT_MISSING)
        self.assertEqual(caught.exception.context["role"], "person")


class ProvenanceSidecarTest(unittest.TestCase):
    def test_provenance_is_stripped_from_the_job_and_kept_beside_it(self):
        store = JobStore(tempfile.mkdtemp(prefix="runtime-e-"))
        result = Intake(store=store).submit(committed("img-text-02"))
        self.assertNotIn("_provenance", result.job)
        self.assertEqual(result.provenance["case_id"], "IMG-TEXT-02")
        self.assertTrue(store.provenance_path_for(result.job_id).exists())
        # a repeat submission returns the same job AND the same provenance, and validates nothing
        again = Intake(store=store, profiles=None).submit(committed("img-text-02"))
        self.assertFalse(again.created)
        self.assertEqual(again.provenance, result.provenance)
        self.assertEqual(again.job_sha256, result.job_sha256)

    def test_a_malformed_provenance_block_is_refused(self):
        raw = committed("img-text-02")
        raw["_provenance"] = "IMG-TEXT-02"
        with self.assertRaises(Refusal) as caught:
            fresh_intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.PROVENANCE_MALFORMED)


class MarketplaceRefusalTest(unittest.TestCase):
    def test_mkt_001_names_the_kind_the_buyer_asked_for_and_intake_refuses_it_precisely(self):
        raw = committed("mkt-001")
        self.assertEqual(raw["deliverable_request"]["kind"], "talking_head_ad")
        self.assertEqual(raw["deliverable_request"]["motion"]["seconds"], 40)
        with self.assertRaises(Refusal) as caught:
            fresh_intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.KIND_NOT_IN_REGISTRY)
        self.assertEqual(caught.exception.context["kind"], "talking_head_ad")
        self.assertIn("DELIVERABLE-KINDS.yaml", caught.exception.context["registry"])
        self.assertNotIn("talking_head_ad", caught.exception.context["known"])

    def test_under_the_alpha_profile_the_refusal_is_the_profile_list(self):
        raw = brief_from_marketplace_case.derive("MKT-001", profile="alpha_human_release")
        with self.assertRaises(Refusal) as caught:
            fresh_intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.KIND_NOT_IN_PROFILE)
        self.assertEqual(caught.exception.context["profile"], "alpha_human_release")
        self.assertEqual(sorted(caught.exception.context["allowed"]),
                         ["short_motion_from_accepted_still", "static_ad", "static_ad_from_supplied_photo"])


class OneCommandToARoutedPlanTest(unittest.TestCase):
    """python3 -m runtime.cli <brief> --store <dir> -> a v1 spec on disk that the router loads and plans."""

    @classmethod
    def setUpClass(cls):
        cls.store = Path(tempfile.mkdtemp(prefix="runtime-e-store-"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            cls.exit_code = cli.main([str(paths.ALPHA_BRIEFS / "img-text-02.json"), "--store", str(cls.store), "--at", FIXED])
        cls.stdout = out.getvalue()
        cls.spec_path = cls.store / "specs" / "alpha-dry-img-text-02.spec.yaml"

    def test_the_command_succeeds_and_writes_the_spec_yaml(self):
        self.assertEqual(self.exit_code, 0, self.stdout)
        self.assertTrue(self.spec_path.exists())
        self.assertIn("PRODUCTION-SPEC-v1", self.stdout)
        self.assertIn("stage_a_blueprint_fixture", self.stdout)
        self.assertTrue((self.store / "jobs" / "alpha-dry-img-text-02.json").exists())
        self.assertTrue((self.store / "jobs" / "alpha-dry-img-text-02.provenance.json").exists())

    def test_the_router_loads_the_spec_and_plans_it_under_the_dry_profile(self):
        spec = load_spec(self.spec_path)
        self.assertEqual(spec.kind, "static_ad")
        self.assertEqual([r.capability for r in spec.requirements()], ["exact_text_composition", "image_generation"])
        self.assertEqual([r.level for r in spec.requirements() if r.capability == "exact_text_composition"],
                         ["code_set_on_textless_plate"])
        ev = B.evidence_base()
        decision = B.router(ev).plan(spec, B.profile("dry", ev), already_committed_usd=Decimal("0"), customer_ref="acct-stage-a-img")
        self.assertEqual(decision["schema"], "ROUTE-DECISION-v0")
        self.assertFalse(decision["manual_route_required"], decision["manual_route_reason"])
        self.assertIsNotNone(decision["primary"])
        self.assertTrue(decision["primary"]["route_key"])
        composed = [r for r in decision["selection_basis"]["self_composed_requirements"] if r["capability"] == "exact_text_composition"]
        self.assertEqual(len(composed), 1)
        self.assertEqual(composed[0]["cell_selected"], "IMG-TEXT/flux-2-pro+code_overlay")
        self.assertEqual(composed[0]["text_mechanism"], "deterministic_text_composition")
        self.assertFalse(decision["provenance"]["dispatched"])
        self.assertEqual(decision["exclusions_applied"], [])     # Latin text: RR-3 is out of scope, nothing excluded

    def test_the_spec_on_disk_carries_every_interface_field(self):
        import yaml

        data = yaml.safe_load(self.spec_path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], "PRODUCTION-SPEC-v1")
        self.assertEqual(data["policy_profile"], "dry")
        self.assertIsInstance(data["route_exclusions"], list)
        self.assertIsInstance(data["canon"]["missing_domains"], list)
        self.assertEqual(data["exact_text"]["text_mechanism"], "deterministic_text_composition")
        self.assertTrue(all("placement" in s for s in data["exact_text"]["strings"]))
        self.assertEqual(set(data["blueprint"]), {"generation_prompts", "planner", "source_ref", "case_values", "production_parameters"})
        self.assertEqual(data["budget"]["max_provider_draws"], 0)


class RouterScopeDefectTracker(unittest.TestCase):
    """KNOWN DEFECT, owned by lane F (the router), recorded here so it cannot be forgotten.

    PRODUCTION-SPEC-v1.route_exclusions[].scope exists precisely so that RR-3's "do not DRAW Devanagari
    on these routes" does not delete RR-1's cheapest exact-text path, in which the same route makes a
    TEXTLESS PLATE and code sets the copy. The compiler writes scope `generated_text_only` and
    text_mechanism `deterministic_text_composition`. The router ignores scope:
      runtime/route/spec.py:40-44   Exclusion(route_key, reason, basis) — no scope field;
      runtime/route/spec.py:115-120 exclusions() never reads e["scope"];
      runtime/route/decision.py:243-249 stage 1 drops the WHOLE candidate for any excluded route_key.
    Effect today (IMG-TEXT-01, Devanagari overlay, dry profile): IMG-CORE/flux-2-pro and
    IMG-CORE/seedream-5-pro are dropped at hard_requirements as plate routes although nothing is drawn.
    """

    @unittest.expectedFailure
    def test_a_generated_text_only_exclusion_leaves_the_plate_route_usable_under_code_composed_text(self):
        raw = committed("img-text-01")
        result = fresh_intake().submit(raw)
        compiled = SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=result.provenance)
        self.assertEqual({r["scope"] for r in compiled.spec["route_exclusions"]}, {"generated_text_only"})
        self.assertEqual(compiled.spec["exact_text"]["text_mechanism"], "deterministic_text_composition")
        path = Path(tempfile.mkdtemp(prefix="runtime-e-")) / "spec.yaml"
        cli.write_spec(compiled.spec, path)
        ev = B.evidence_base()
        decision = B.router(ev).plan(load_spec(path), B.profile("dry", ev), already_committed_usd=Decimal("0"), customer_ref="acct-test")
        dropped_plates = [e["would_have_supplied"] for e in decision["exclusions_applied"]]
        self.assertEqual(dropped_plates, [])   # fails today: ['IMG-CORE/flux-2-pro', 'IMG-CORE/seedream-5-pro']


class ZeroSpendOnTheAlphaFlowTest(unittest.TestCase):
    def test_intake_compile_and_plan_open_no_socket(self):
        def boom(*a, **k):
            raise AssertionError("the alpha flow tried to open a connection")

        class ExplodingSocket:
            def __init__(self, *a, **k):
                boom()

        patched = [(socket, "socket", ExplodingSocket), (socket, "create_connection", boom),
                   (socket, "socketpair", boom), (socket, "getaddrinfo", boom), (ssl.SSLContext, "wrap_socket", boom)]
        saved = [(m, n, getattr(m, n)) for m, n, _ in patched]
        for m, n, v in patched:
            setattr(m, n, v)
        try:
            result = fresh_intake().submit(committed("img-text-02"))
            compiled = SpecCompiler().compile(result.job, compiled_utc=FIXED, provenance=result.provenance)
            path = Path(tempfile.mkdtemp(prefix="runtime-e-")) / "spec.yaml"
            cli.write_spec(compiled.spec, path)
            ev = B.evidence_base()
            decision = B.router(ev).plan(load_spec(path), B.profile("dry", ev), already_committed_usd=Decimal("0"), customer_ref="acct-test")
            self.assertFalse(decision["manual_route_required"])
        finally:
            for m, n, v in saved:
                setattr(m, n, v)


if __name__ == "__main__":
    unittest.main()
