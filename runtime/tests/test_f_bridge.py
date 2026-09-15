"""The execution bridge (runtime/execute): a ROUTE-DECISION becomes rendered, priced, unsent attempts.

Every test here runs at USD 0. The attempts are rendered through the Lab harness's own adapter
dry_run(), which reads no key and opens no socket (the fresh-interpreter proof is test_f_no_socket.py).
"""
from __future__ import annotations

import copy
import re
import shutil
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

import _bootstrap as B
from runtime.execute import manifest as M
from runtime.execute.authorisation import AuthorisationRefused, check_live_authorisation, load_authorisation
from runtime.execute.bridge import ExecutionBridge
from runtime.route.decision import ExecuteRefused
from runtime.route.profile import PolicyProfile
from runtime.route.spec import Spec

PROMPT = ("A centred gift box of Indian mithai on a warm, softly lit Diwali table; textless plate with a calm "
          "lower third kept clear; no lettering anywhere.")
CUSTOMER = "acct-test"


def _bridge(ev=None):
    ev = ev or B.evidence_base()
    pb = B.price_book(ev)
    r = B.router(ev, pb)
    return ExecutionBridge(evidence=ev, prices=pb, identities=r.identities), r, ev


def _build(spec_path, profile_name="dry", *, prompt=PROMPT, inputs=None, mutate=None, request_ceiling=None):
    bridge, r, ev = _bridge()
    spec = B.spec(spec_path)
    if mutate:
        data = copy.deepcopy(spec.data)
        mutate(data)
        spec = Spec(path=spec.path, data=data)
    prof = B.profile(profile_name, ev)
    decision = r.plan(spec, prof, customer_ref=CUSTOMER)
    manifest = bridge.build(spec, decision, prof, prompt_text=prompt, inputs=inputs, customer_ref=CUSTOMER,
                            request_ceiling_usd=request_ceiling)
    return bridge, spec, decision, prof, manifest


class OverlayManifestUnderDry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bridge, cls.spec, cls.decision, cls.prof, cls.m = _build(B.SPEC_STATIC_OVERLAY)

    def test_the_manifest_has_the_contract_shape(self):
        m = self.m
        self.assertEqual(m["schema"], "EXECUTION-MANIFEST-v0")
        self.assertTrue(m["manifest_id"].startswith("em-"))
        self.assertEqual(m["job_id"], "job-fixture-A")
        self.assertEqual(m["spec_id"], self.spec.spec_id)
        self.assertEqual(m["decision_id"], self.decision["decision_id"])
        self.assertEqual(m["policy_profile"], "dry")
        self.assertEqual(m["dispatch_mode"], "dry")
        self.assertIsNone(m["blocked"])
        for key in ("attempts", "fallback_triggers", "self_composed", "surface_preference", "ceiling",
                    "provenance", "built_utc"):
            self.assertIn(key, m)

    def test_one_attempt_per_allowed_draw_for_primary_and_for_fallback(self):
        draws = self.prof.max_provider_draws
        self.assertEqual(draws, 2)
        primary = [a for a in self.m["attempts"] if a["slot"] == "primary"]
        fallback = [a for a in self.m["attempts"] if a["slot"] == "fallback"]
        self.assertEqual(len(primary), draws)
        self.assertEqual(len(fallback), draws)
        self.assertEqual([a["draw_index"] for a in primary], [1, 2])
        self.assertEqual({a["route_key"] for a in primary}, {self.decision["primary"]["route_key"]})
        self.assertEqual({a["route_key"] for a in fallback}, {self.decision["fallback"]["route_key"]})

    def test_the_primary_is_the_cheap_textless_plate_and_would_dispatch(self):
        primary = [a for a in self.m["attempts"] if a["slot"] == "primary"]
        for a in primary:
            self.assertEqual(a["route_key"], "flux-2-pro")
            self.assertEqual(a["price"]["expected_cost_usd"], "0.030000")
            # pool-agnostic answer (harness shape, price, ceiling) is yes; the real answer is no until a
            # pool reading positively funds it (Controller audit on PR #98, blocker 3: fail closed)
            self.assertTrue(a["would_dispatch_if_funded"], a["refusal_reason"])
            self.assertFalse(a["would_dispatch"])
            self.assertEqual(a["pool_liquidity"]["status"], "not_read")
            self.assertIn("pool_liquidity_unknown", a["refusal_reason"])
            self.assertNotIn("harness:", a["refusal_reason"])
            self.assertEqual(a["request"]["method"], "POST")
            self.assertTrue(a["request"]["url"].startswith("https://queue.fal.run/"))
            self.assertRegex(a["request"]["body_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(a["request"]["rendered_by"], "harness adapter dry_run")
            self.assertEqual(a["request"]["body"]["prompt"], PROMPT)
            self.assertEqual(a["request"]["body"]["image_size"], {"width": 816, "height": 1024})   # 4:5, SIZE_A

    def test_every_attempt_carries_its_price_pin_and_evidence_cell(self):
        for a in self.m["attempts"]:
            self.assertTrue(a["price"]["price_pin_ref"])
            self.assertTrue(a["price"]["pin_indexes"])
            self.assertTrue(a["evidence"]["cells"])
            self.assertEqual(a["evidence"]["status"], "clean_observed")
            self.assertEqual(a["evidence"]["text_mechanism"], "deterministic_text_composition")
            self.assertTrue(a["price"]["price_agrees_with_harness"], a["price"])

    def test_attempt_ids_are_customer_namespace_and_match_the_decision(self):
        ids = [a["attempt_id"] for a in self.m["attempts"]]
        self.assertEqual(len(set(ids)), len(ids))
        for i in ids:
            self.assertTrue(i.startswith("cust:acct-test:job-fixture-A:"))
        primary_ids = [a["attempt_id"] for a in self.m["attempts"] if a["slot"] == "primary"]
        self.assertEqual(primary_ids, self.decision["primary"]["attempt_ids_if_dispatched"])

    def test_fallback_attempts_are_conditional_on_named_triggers(self):
        for a in (x for x in self.m["attempts"] if x["slot"] == "fallback"):
            self.assertFalse(a["would_dispatch"])
            self.assertEqual(a["conditional_on"], self.m["fallback_triggers"])
            self.assertEqual(set(a["conditional_on"]),
                             {"provider_refusal", "timeout", "gate_fail", "capability_unsupported"})
            self.assertTrue(a["if_triggered_would_dispatch_if_funded"], a["refusal_reason"])
            self.assertFalse(a["if_triggered_would_dispatch"])          # no pool reading: fail closed
            self.assertIn("never as a retry", a["conditional_note"])

    def test_the_ceiling_propagates_per_attempt_in_reservation_order(self):
        c = self.m["ceiling"]
        self.assertEqual(Decimal(c["job_ceiling_usd"]), Decimal("5.00"))
        self.assertEqual(c["attempts_blocked_by_ceiling"], 0)
        running = Decimal("0")
        for a in self.m["attempts"]:
            ce = a["ceiling"]
            self.assertEqual(Decimal(ce["reserved_before_this_usd"]), running)
            running += Decimal(ce["this_attempt_usd"])
            self.assertTrue(ce["within"])
            self.assertFalse(a["blocked_by_ceiling"])
        self.assertEqual(Decimal(c["reserved_total_usd"]), running)
        self.assertEqual(running, Decimal("0.140000"))     # 2 x 0.03 + 2 x 0.04

    def test_self_composed_text_is_recorded_as_the_runtime_s_own_work(self):
        sc = self.m["self_composed"]
        self.assertEqual(len(sc), 1)
        self.assertEqual(sc[0]["capability"], "exact_text_composition")
        self.assertEqual(sc[0]["cell"], "IMG-TEXT/flux-2-pro+code_overlay")
        self.assertEqual(sc[0]["text_mechanism"], "deterministic_text_composition")

    def test_provenance_pins_every_input_and_says_nothing_was_sent(self):
        pv = self.m["provenance"]
        for key in ("spec_sha256", "decision_sha256", "routing_evidence_map_sha256", "taint_register_sha256", "roster_sha256"):
            self.assertRegex(pv[key], r"^[0-9a-f]{64}$", key)
        self.assertEqual(pv["decision_sha256"], M.sha256_of(self.decision))
        self.assertEqual(pv["policy_profile"], "dry")
        self.assertIs(pv["policy_profile_adopted"], True)
        self.assertEqual(pv["spend_authority_status"], "none")
        self.assertFalse(pv["may_spend"])
        self.assertTrue(pv["harness_modules"])
        self.assertIs(pv["dispatched"], False)
        self.assertEqual(pv["network"], "none")

    def test_no_key_value_anywhere_in_the_manifest(self):
        """Credentials appear as NAMES only; a header template says <KEY:NAME>, never a value."""
        blob = M.canonical_json(self.m).decode("utf-8")
        self.assertNotIn("Key ", blob.replace("Key $", ""))      # a fal 'Authorization: Key <value>' shape
        self.assertNotRegex(blob, r"(?i)(sk|key)-[A-Za-z0-9]{20,}")
        for a in self.m["attempts"]:
            self.assertEqual(a["request"]["credential_name"], "FAL_KEY")

    def test_surface_preference_is_recorded_honestly_not_invented(self):
        sp = self.m["surface_preference"]
        self.assertEqual(sp["rule"], "same_model_prefers_gcp")
        self.assertFalse(sp["applied"])
        self.assertEqual(sp["primary_surface"], "fal")
        # flux-2-pro's roster record is azure_foundry (needs_controller_enablement) with a fal fallback: no GCP surface
        self.assertEqual(sorted(o["surface"] for o in sp["roster_surfaces_for_model"]), ["azure_foundry", "fal"])
        self.assertIn("neither pair is fal + GCP", sp["reason"])

    def test_dry_run_returns_dry_complete_with_nothing_sent_and_nothing_reserved(self):
        res = self.bridge.run(self.m, self.prof)
        self.assertEqual(res["status"], "dry_complete")
        self.assertEqual(len(res["attempts"]), len(self.m["attempts"]))
        for a in res["attempts"]:
            self.assertEqual(a["status"], "dry_not_sent")
            self.assertIsNone(a["artifact_sha256"])
            self.assertEqual(a["settled_usd"], "0")
            self.assertEqual(a["reserved_usd"], "0")
        self.assertEqual(res["network"], "none")
        self.assertIs(res["dispatched"], False)

    def test_the_rendering_names_the_essentials(self):
        text = M.render(self.m, self.bridge.run(self.m, self.prof))
        self.assertIn("EXECUTION-MANIFEST", text)
        self.assertIn("flux-2-pro on fal", text)
        self.assertIn("CONDITIONAL", text)
        self.assertIn("dry_complete", text)
        self.assertIn("network none", text)


class BlockedManifests(unittest.TestCase):
    def test_the_supplied_photo_edit_is_blocked_manual_route_required(self):
        bridge, spec, decision, prof, m = _build(B.SPEC_EDIT_PHOTO)
        self.assertTrue(decision["manual_route_required"])
        self.assertEqual(m["blocked"]["reason_code"], "manual_route_required")
        self.assertIn("fallback_required", m["blocked"]["reason"])
        self.assertEqual(m["attempts"], [])
        res = bridge.run(m, prof)
        self.assertEqual(res["status"], "refused")
        self.assertEqual(res["refusal"]["reason_code"], "manual_route_required")
        self.assertEqual(res["attempts"], [])

    def test_a_decision_whose_envelope_is_exceeded_is_blocked(self):
        bridge, r, ev = _bridge()
        spec = B.spec(B.SPEC_MOTION)
        prof = B.profile("dry", ev)
        decision = r.plan(spec, prof, already_committed_usd=Decimal("4.90"), customer_ref=CUSTOMER)
        m = bridge.build(spec, decision, prof, prompt_text=PROMPT, customer_ref=CUSTOMER)
        self.assertIsNotNone(m["blocked"])
        # the router already turned the exceeded envelope into manual_route_required; the bridge reports that first
        self.assertIn(m["blocked"]["reason_code"], ("manual_route_required", "cost_envelope_exceeded"))
        self.assertIn("cost_envelope_exceeded", m["blocked"]["reason"])

    def test_fallback_required_with_no_fallback_is_blocked_by_the_bridge_itself(self):
        """Defence in depth: hand the bridge a decision with the fallback removed."""
        bridge, spec, decision, prof, _ = _build(B.SPEC_STATIC_OVERLAY)
        d = copy.deepcopy(decision)
        d["fallback"] = None
        d["manual_route_required"] = False
        m = bridge.build(spec, d, prof, prompt_text=PROMPT, customer_ref=CUSTOMER)
        self.assertEqual(m["blocked"]["reason_code"], "fallback_required_missing")
        self.assertEqual(m["attempts"], [])

    def test_no_primary_is_blocked(self):
        bridge, spec, decision, prof, _ = _build(B.SPEC_STATIC_OVERLAY)
        d = copy.deepcopy(decision)
        d["primary"] = None
        d["manual_route_required"] = False
        m = bridge.build(spec, d, prof, prompt_text=PROMPT, customer_ref=CUSTOMER)
        self.assertEqual(m["blocked"]["reason_code"], "no_primary")


class CeilingPerAttempt(unittest.TestCase):
    def test_attempts_past_the_ceiling_are_blocked_not_trimmed(self):
        """A request ceiling below the spec's: the effective ceiling is the lower one, attempts that
        would cross it are blocked_by_ceiling and stay on the manifest."""
        bridge, spec, decision, prof, m = _build(B.SPEC_STATIC_OVERLAY, request_ceiling="0.07")
        c = m["ceiling"]
        self.assertEqual(c["request_ceiling_usd"], "0.07")
        self.assertEqual(c["effective_ceiling_usd"], "0.07")
        self.assertEqual(len(m["attempts"]), 4)                     # nothing trimmed
        flags = [a["blocked_by_ceiling"] for a in m["attempts"]]
        self.assertEqual(flags, [False, False, True, True])         # 0.03 + 0.03 fit; the 0.04 fallbacks do not
        self.assertEqual(c["attempts_blocked_by_ceiling"], 2)
        for a in m["attempts"][2:]:
            self.assertFalse(a["would_dispatch"])
            self.assertFalse(a["if_triggered_would_dispatch"])
            self.assertFalse(a["would_dispatch_if_funded"] or a["if_triggered_would_dispatch_if_funded"])  # the ceiling, not the pool
            self.assertIn("blocked_by_ceiling", a["refusal_reason"])
        self.assertEqual(c["reserved_total_usd"], "0.060000")

    def test_already_committed_money_counts_against_the_ceiling(self):
        bridge, r, ev = _bridge()
        spec = B.spec(B.SPEC_STATIC_OVERLAY)
        prof = B.profile("dry", ev)
        decision = r.plan(spec, prof, already_committed_usd=Decimal("4.90"), customer_ref=CUSTOMER)
        self.assertFalse(decision["manual_route_required"])         # 4.90 + 2 x 0.04 worst case fits 5.00
        m = bridge.build(spec, decision, prof, prompt_text=PROMPT, customer_ref=CUSTOMER)
        self.assertEqual(m["ceiling"]["already_committed_usd"], "4.90")
        self.assertEqual(Decimal(m["attempts"][0]["ceiling"]["reserved_before_this_usd"]), Decimal("4.90"))
        # 4.90 + 0.03 + 0.03 = 4.96; + 0.04 = 5.00 fits; + 0.04 = 5.04 does not
        self.assertEqual([a["blocked_by_ceiling"] for a in m["attempts"]], [False, False, False, True])


class HarnessRefusalsAreKeptVerbatim(unittest.TestCase):
    def test_a_motion_attempt_without_the_accepted_still_would_not_dispatch_with_the_harness_reason(self):
        bridge, spec, decision, prof, m = _build(B.SPEC_MOTION)
        self.assertIsNone(m["blocked"])
        for a in m["attempts"]:
            self.assertFalse(a["would_dispatch"])
            self.assertFalse(a["would_dispatch_if_funded"])            # the harness reason, not the pool
            self.assertIn("harness: input_unresolved:plate_accepted_draw", a["refusal_reason"])
            self.assertTrue(a["request"]["body_sha256"])            # the body is rendered with a placeholder, and refused
            self.assertEqual(a["evidence"]["text_mechanism"], "not_applicable")

    def test_supplying_the_accepted_still_as_an_input_resolves_the_body(self):
        still = {"image_url": "sealed://accepted-still/job-fixture-A/sha256/0000"}
        bridge, spec, decision, prof, m = _build(B.SPEC_MOTION, inputs=still)
        primary = [a for a in m["attempts"] if a["slot"] == "primary"]
        for a in primary:
            self.assertTrue(a["would_dispatch_if_funded"], a["refusal_reason"])
            self.assertEqual(a["request"]["body"]["image_url"], still["image_url"])
            self.assertEqual(a["request"]["body"]["duration"], 6)
            self.assertEqual(a["price"]["expected_cost_usd"], "0.480000")

    def test_a_caller_parameter_that_is_not_an_input_role_is_refused_by_the_harness_not_patched(self):
        bridge, spec, decision, prof, m = _build(B.SPEC_STATIC_OVERLAY, inputs={"seed": 7})
        for a in m["attempts"]:
            self.assertFalse(a["would_dispatch"])
            self.assertFalse(a["would_dispatch_if_funded"])
            self.assertIn("PreDispatchRefusal", a["refusal_reason"])


class PromptIsPartOfTheRequest(unittest.TestCase):
    def test_no_prompt_refuses_before_anything_is_rendered(self):
        bridge, r, ev = _bridge()
        spec = B.spec(B.SPEC_STATIC_OVERLAY)
        prof = B.profile("dry", ev)
        decision = r.plan(spec, prof, customer_ref=CUSTOMER)
        for bad in (None, "", "   "):
            with self.assertRaises(ExecuteRefused) as ctx:
                bridge.build(spec, decision, prof, prompt_text=bad, customer_ref=CUSTOMER)
            self.assertIn("never invents one", " ".join(ctx.exception.reasons))


class LiveRefuses(unittest.TestCase):
    def test_live_run_refuses_naming_spend_authority(self):
        bridge, spec, decision, prof, m = _build(B.SPEC_STATIC_OVERLAY, "alpha_human_release")
        self.assertEqual(m["dispatch_mode"], "live")
        self.assertIsNone(m["blocked"])
        for a in m["attempts"]:
            self.assertIsNone(a["request"]["body"])                 # a live manifest carries the body hash only
            self.assertTrue(a["request"]["body_sha256"])
        with self.assertRaises(ExecuteRefused) as ctx:
            bridge.run(m, prof)
        joined = " ".join(ctx.exception.reasons)
        self.assertIn("spend_authority", joined)
        self.assertIn("before any transport was considered", joined)

    def test_a_manifest_built_dry_cannot_be_run_live(self):
        bridge, spec, decision, prof, m = _build(B.SPEC_STATIC_OVERLAY, "dry")
        live = B.profile("alpha_human_release")
        with self.assertRaises(ExecuteRefused):
            bridge.run(m, live)

    def test_even_a_signed_record_does_not_dispatch_because_nothing_is_wired(self):
        """The positive parse of an authorisation, on a throwaway file, and the refusal that follows it."""
        tmp = Path(tempfile.mkdtemp(prefix="runtime-auth-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        record = tmp / "RUNTIME-SPEND-AUTHORISATION-TEST.yaml"
        record.write_text(yaml.safe_dump({
            "authorised": True, "approved_by": "test-only approver", "approved_at": "2026-09-14T00:00:00Z",
            "job_ceiling_usd": 5.00, "profile": "in_memory_live", "routes_allowed": ["flux-2-pro", "qwen-image-3"],
        }), encoding="utf-8")
        auth = load_authorisation(str(record))
        self.assertTrue(auth.authorised)
        self.assertEqual(auth.approved_by, "test-only approver")
        self.assertEqual(auth.job_ceiling_usd, Decimal("5.0"))

        bridge, r, ev = _bridge()
        row = dict(B.profile("alpha_human_release", ev).row)
        row["spend_authority"] = {"status": "signed", "record": str(record), "note": "TEST ROW - in memory only"}
        prof = PolicyProfile(name="in_memory_live", row=row, path=Path("in-memory"))
        self.assertTrue(prof.may_spend()[0])
        spec = B.spec(B.SPEC_STATIC_OVERLAY)
        decision = r.plan(spec, prof, customer_ref=CUSTOMER)
        m = bridge.build(spec, decision, prof, prompt_text=PROMPT, customer_ref=CUSTOMER)
        self.assertEqual(m["dispatch_mode"], "live")
        check_live_authorisation(prof, ev.root, job_ceiling_usd=Decimal("5.00"),
                                 routes=[a["route_key"] for a in m["attempts"]])   # passes
        with self.assertRaises(ExecuteRefused) as ctx:
            bridge.run(m, prof)
        self.assertIn("live dispatch is not wired in this tranche", " ".join(ctx.exception.reasons))

    def test_the_authorisation_check_names_each_defect(self):
        tmp = Path(tempfile.mkdtemp(prefix="runtime-auth-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        with self.assertRaises(AuthorisationRefused) as ctx:
            load_authorisation(str(tmp / "missing.yaml"))
        self.assertIn("does not exist", ctx.exception.reasons[0])
        bad = tmp / "bad.yaml"
        bad.write_text(yaml.safe_dump({"authorised": False, "approved_by": "", "approved_at": "x",
                                       "job_ceiling_usd": 1, "profile": "p", "routes_allowed": []}), encoding="utf-8")
        with self.assertRaises(AuthorisationRefused) as ctx:
            load_authorisation(str(bad))
        joined = " ".join(ctx.exception.reasons)
        for phrase in ("authorised: False", "no approver", "allows no routes"):
            self.assertIn(phrase, joined)
        with self.assertRaises(AuthorisationRefused) as ctx:
            load_authorisation(None)
        self.assertIn("names no signed spend authorisation record", ctx.exception.reasons[0])

    def test_no_profile_row_on_disk_names_a_record(self):
        for name in ("alpha_human_release", "alpha_wider_example", "dry", "dry_permissive"):
            prof = B.profile(name)
            self.assertEqual(prof.spend_authority["status"], "none")
            self.assertIsNone(prof.spend_authority["record"])


class CaseRowShape(unittest.TestCase):
    def test_the_case_row_is_built_from_the_spec_and_decision_only(self):
        spec = B.spec(B.SPEC_MOTION)
        d = B.plan(B.SPEC_MOTION, "dry")
        row = ExecutionBridge.case_row(spec, d, d["primary"], PROMPT, 2)
        self.assertEqual(row["case_id"], "job-fixture-C")
        self.assertEqual(row["item_id"], "spec-fixture-C-sweetshop-reel")
        self.assertEqual(row["route_key"], d["primary"]["route_key"])
        self.assertEqual(row["params"], {"aspect": "9:16", "duration_s": 6, "audio": "off"})
        self.assertEqual(row["repeat_index"], 2)
        self.assertEqual(row["tranche"], "alpha")
        self.assertEqual(row["billing_pool"], d["primary"]["billing_pool"])
        self.assertEqual(row["price_status"], "pinned")
        self.assertFalse(row["conditional"])


if __name__ == "__main__":
    unittest.main()
