"""Lane G, parts F and G: the four loop paths end to end (all dry, all synthetic), and the
OUTCOME-EVENT-v1 store's invariants."""
from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import test_g_support as G

from canon.gate import textscan
from runtime.errors import Refusal
from runtime.loop import driver, memory, refusals, synthetic
from runtime.util import sha256_obj

NOW = "2026-09-14T13:00:00Z"


def manifest_for(spec: dict, n_attempts: int = 2, *, fallback_second: bool = False) -> dict:
    """A minimal EXECUTION-MANIFEST-v0 per WAVE2-INTERFACES §3 (lane F's object, hand-made here)."""
    attempts = []
    for i in range(1, n_attempts + 1):
        slot = "fallback" if (fallback_second and i == 2) else "primary"
        attempts.append({
            "attempt_id": f"att-{spec['spec_id']}-{i}", "slot": slot, "draw_index": i,
            "route_key": "nano-banana-2" if slot == "fallback" else "imagen-4-fast+code_overlay",
            "surface": "gcp-vertex", "adapter_family": "vertex_images",
            "surface_model_id": "imagen-4.0-fast-generate-001",
            "request": {"method": "POST", "url": "dry://not-sent", "body_sha256": "00" * 32,
                        "body": {"generationConfig": {"imageConfig": {"aspectRatio": spec["deliverable"]["aspect"]}}},
                        "rendered_by": "harness adapter dry_run"},
            "price": {"unit_price": "0.03", "unit": "image", "quantity": 1, "expected_cost_usd": "0.03",
                      "billing_pool": "gcp_credits", "price_pin_ref": "pins/gcp-imagen-2026-09-10.yaml",
                      "pin_indexes": [0]},
            "evidence": {"cells": ["IMG-TEXT/imagen-4-fast+code_overlay"], "status": "clean_observed",
                         "text_mechanism": "deterministic_text_composition"},
            "would_dispatch": False, "refusal_reason": None,
            "ceiling": {"job_ceiling_usd": "5.00", "reserved_before_this_usd": "0", "this_attempt_usd": "0", "within": True},
        })
    return {
        "schema": "EXECUTION-MANIFEST-v0", "manifest_id": f"man-{spec['spec_id']}", "job_id": spec["job_id"],
        "spec_id": spec["spec_id"], "decision_id": f"rd-{spec['spec_id']}", "policy_profile": "alpha_human_release",
        "dispatch_mode": "dry", "blocked": None, "attempts": attempts,
        "fallback_triggers": [{"condition": "LIMIT-TEXT", "note": "baked lettering on the plate"}],
        "self_composed": [{"capability": "exact_text_composition", "cell": "code_overlay",
                           "text_mechanism": "deterministic_text_composition", "note": "runtime composes the strings"}],
        "provenance": {"spec_sha256": sha256_obj(spec), "decision_sha256": "11" * 32,
                       "routing_evidence_map_sha256": "22" * 32, "taint_register_sha256": "33" * 32,
                       "roster_sha256": "44" * 32, "policy_profile": "alpha_human_release",
                       "policy_profile_adopted": True, "spend_authority_status": "none",
                       "harness_modules": [], "dispatched": False, "network": "none"},
        "built_utc": NOW,
    }


def detector(name: str):
    return textscan.ScriptedDetector.from_json(G.load_json(name))


class CountingProvider:
    """Synthetic PNGs of the spec's aspect, seed = draw index (distinct digests per draw)."""
    def __init__(self, spec, kind="png"):
        self.spec, self.calls, self.kind = spec, 0, kind

    def __call__(self, attempt):
        self.calls += 1
        if self.kind is None:
            return None
        return synthetic.png_for_aspect(self.spec["deliverable"]["aspect"], seed=attempt["draw_index"])


class LoopPaths(unittest.TestCase):
    def setUp(self):
        self.spec = G.load_spec_dict(G.SPEC_OVERLAY)
        self.bp = G.blueprint_clean()
        self.profile = G.profile("alpha_human_release")   # repair_allowance 1, max draws 2
        self.tmp = tempfile.mkdtemp(prefix="g-loop-")

    def run_loop(self, det, verdicts, *, spec=None, bp=None, manifest=None, provider=None, write=False):
        spec = spec or self.spec
        provider = provider or CountingProvider(spec)
        res = driver.run_loop(spec, bp or self.bp, manifest or manifest_for(spec), self.profile,
                              artifact_provider=provider, detector=det, human_verdicts=verdicts,
                              product_entity=True, write=write, store=memory.OutcomeStore(self.tmp), now_utc=NOW)
        return res, provider

    def test_happy_path(self):
        res, provider = self.run_loop(detector("detector-no-text.json"), [G.load_json("human-accept.json")], write=True)
        self.assertEqual(res.state, driver.TERMINAL)
        self.assertEqual(res.acceptance_state, "accepted")
        self.assertEqual(provider.calls, 1)
        self.assertEqual(res.repairs, [])
        ev = res.event
        self.assertEqual(ev["schema"] if "schema" in ev else "OUTCOME-EVENT-v1", "OUTCOME-EVENT-v1")
        self.assertTrue(ev["dry_run"])
        self.assertEqual(ev["acceptance"]["decision"], "accepted")
        self.assertEqual(ev["acceptance"]["decided_by"], "controller")
        self.assertTrue(ev["template_candidate"]["eligible"])
        self.assertIn("dry_run", ev["template_candidate"]["reason"])
        self.assertEqual(len(ev["attempts"]), 1)
        a = ev["attempts"][0]
        self.assertEqual(a["status"], "dry_not_sent")
        self.assertEqual(a["billing_state"], "not_dispatched")
        self.assertEqual(a["artifact_origin"], "synthetic")
        self.assertEqual(a["settled_usd"], "0")
        self.assertEqual(a["gate_post_verdict"], "PASS")
        self.assertEqual(ev["route"]["text_mechanism"], "deterministic_text_composition")
        self.assertEqual(ev["route"]["cell_key"], "IMG-TEXT/imagen-4-fast+code_overlay")
        self.assertEqual(ev["cost"], {"provider_usd_total": "0", "by_pool": {"gcp_credits": "0"}, "draws": 1,
                                      "draws_per_accepted_outcome": 1})
        self.assertTrue(ev["event_id"].startswith("oe-"))
        self.assertTrue(Path(res.written_path).exists())
        self.assertEqual(json.loads(Path(res.written_path).read_text())["event_id"], ev["event_id"])
        self.assertEqual({d["check"]: d["status"] for d in ev["deterministic_checks"]},
                         {"format_probe": "PASS", "baked_text_scan": "PASS", "aspect_check": "PASS"})

    def test_repair_path(self):
        res, provider = self.run_loop(detector("detector-lettering-then-clean.json"), [G.load_json("human-accept.json")])
        self.assertEqual(res.acceptance_state, "accepted")
        self.assertEqual(provider.calls, 2)
        self.assertEqual(len(res.repairs), 1)
        ev = res.event
        self.assertEqual(ev["repairs"][0]["failure_category"], "baked_lettering")
        self.assertEqual(ev["repairs"][0]["attempt_index"], 2)
        self.assertEqual(ev["repairs"][0]["incremental_cost_usd"], "0.03")
        self.assertEqual(ev["attempts"][0]["gate_post_verdict"], "FAIL")
        self.assertEqual(ev["attempts"][1]["gate_post_verdict"], "PASS")
        self.assertEqual(ev["attempts"][1]["is_repair_of"], ev["attempts"][0]["attempt_id"])
        self.assertEqual(ev["attempts"][1]["repair_id"], ev["repairs"][0]["repair_id"])
        self.assertIsNone(ev["attempts"][0].get("is_repair_of"))
        self.assertEqual(ev["cost"]["draws"], 2)
        self.assertEqual(ev["cost"]["draws_per_accepted_outcome"], 2)

    def test_exhaustion_path(self):
        res, provider = self.run_loop(detector("detector-lettering.json"), [G.load_json("human-accept.json")])
        self.assertEqual(res.state, driver.TERMINAL)
        self.assertEqual(res.acceptance_state, "abandoned")
        self.assertEqual(res.refusal, refusals.REPAIR_ALLOWANCE_EXHAUSTED)
        self.assertEqual(provider.calls, 2)              # no hidden retry
        self.assertEqual(len(res.repairs), 1)            # allowance 1: one repair, the second refused
        ev = res.event
        self.assertEqual(ev["acceptance"]["decision"], "abandoned")
        self.assertIn("REPAIR_ALLOWANCE_EXHAUSTED", ev["acceptance"]["note"])
        self.assertFalse(ev["template_candidate"]["eligible"])
        self.assertNotIn("decided_by", ev["acceptance"])
        self.assertEqual([a["gate_post_verdict"] for a in ev["attempts"]], ["FAIL", "FAIL"])
        self.assertEqual(ev["gate"]["blocking_failures"], ["LIMIT-TEXT"])
        self.assertNotIn("draws_per_accepted_outcome", ev["cost"])

    def test_reject_path(self):
        res, provider = self.run_loop(detector("detector-no-text.json"), [G.load_json("human-reject.json")])
        self.assertEqual(res.acceptance_state, "rejected")
        self.assertEqual(provider.calls, 1)
        ev = res.event
        self.assertEqual(ev["acceptance"]["decision"], "rejected")
        self.assertEqual(ev["acceptance"]["contract_lines_failed"], G.load_json("human-reject.json")["contract_lines_failed"])
        self.assertFalse(ev["template_candidate"]["eligible"])

    def test_human_repair_request_path(self):
        verdicts = [G.load_json("human-repair-request.json"), G.load_json("human-accept.json")]
        res, provider = self.run_loop(detector("detector-no-text.json"), verdicts)
        self.assertEqual(res.acceptance_state, "accepted")
        self.assertEqual(provider.calls, 2)
        self.assertEqual(res.repairs[0]["failure_category"], "human_rejection")
        self.assertEqual(res.repairs[0]["source"], "human")
        self.assertIn("mithai", res.repairs[0]["what_changes"])
        self.assertEqual(res.event["attempts"][1]["is_repair_of"], res.event["attempts"][0]["attempt_id"])
        # the transcript shows repair_requested -> pending_human -> accepted
        self.assertEqual([t["to"] for t in res.acceptance.transcript], ["repair_requested", "pending_human", "accepted"])

    def test_fallback_slot_changes_route_on_repair(self):
        man = manifest_for(self.spec, 2, fallback_second=True)
        res, _ = self.run_loop(detector("detector-lettering-then-clean.json"), [G.load_json("human-accept.json")], manifest=man)
        self.assertTrue(res.repairs[0]["route_changed"])
        self.assertEqual(res.repairs[0]["fallback_route"], "nano-banana-2")
        self.assertEqual(res.event["attempts"][1]["slot"], "fallback")

    def test_pre_dispatch_block_draws_nothing(self):
        res, provider = self.run_loop(detector("detector-no-text.json"), [G.load_json("human-accept.json")],
                                      bp=G.blueprint_overlay())    # IMG-TEXT-01 plate: LIMIT-TEXT FAIL
        self.assertEqual(res.state, driver.BLOCKED_PRE)
        self.assertEqual(provider.calls, 0)
        self.assertEqual(res.acceptance_state, "abandoned")
        self.assertEqual(res.event["attempts"], [])
        self.assertEqual(res.event["cost"]["draws"], 0)
        self.assertIn("LIMIT-TEXT", res.event["acceptance"]["note"])

    def test_dry_none_artifacts_never_pass(self):
        provider = CountingProvider(self.spec, kind=None)
        res, provider = self.run_loop(detector("detector-no-text.json"), [G.load_json("human-accept.json")], provider=provider)
        self.assertEqual(provider.calls, 2)
        self.assertEqual(res.acceptance_state, "abandoned")
        self.assertEqual([a["gate_post_verdict"] for a in res.event["attempts"]], ["NOT_RUN", "NOT_RUN"])
        self.assertEqual([a["artifact_origin"] for a in res.event["attempts"]], ["none", "none"])
        self.assertEqual(res.repairs, [])

    def test_no_verdict_left_means_pending_and_no_event(self):
        res, _ = self.run_loop(detector("detector-no-text.json"), [])
        self.assertEqual(res.state, driver.PENDING)
        self.assertIsNone(res.event)
        self.assertEqual(res.acceptance_state, "pending_human")

    def test_motion_path_without_sampled_frames_cannot_be_accepted(self):
        # Promoted from UPWORK-INTRO-001 (SD-06): a video nobody sampled frames from is NOT_RUN at the
        # post-draw gate — never PASS-by-omission — so no person is asked to accept it.
        spec = G.load_spec_dict(G.SPEC_MOTION)
        man = manifest_for(spec, 1)
        man["attempts"][0]["request"]["body"] = {"parameters": {"aspectRatio": "9:16", "durationSeconds": 6}}
        provider = lambda a: synthetic.mp4_for_spec(spec, seed=a["draw_index"])
        res = driver.run_loop(spec, G.blueprint_motion(), man, self.profile, artifact_provider=provider,
                              detector=None, human_verdicts=[G.load_json("human-accept.json")], now_utc=NOW)
        self.assertEqual(res.event["attempts"][0]["gate_post_verdict"], "NOT_RUN")
        self.assertEqual(res.acceptance_state, "abandoned")

    def test_motion_path_with_mp4_stub_and_sampled_frames(self):
        spec = G.load_spec_dict(G.SPEC_MOTION)
        man = manifest_for(spec, 1)
        man["attempts"][0]["request"]["body"] = {"parameters": {"aspectRatio": "9:16", "durationSeconds": 6}}
        provider = lambda a: synthetic.mp4_for_spec(spec, seed=a["draw_index"])
        sampler = lambda a, b: synthetic.frames_for_spec(spec, seed=a["draw_index"])
        script = {hashlib.sha256(f).hexdigest(): {"status": "no_text", "transcript": ""}
                  for f in synthetic.frames_for_spec(spec, seed=1)}
        res = driver.run_loop(spec, G.blueprint_motion(), man, self.profile, artifact_provider=provider,
                              detector=textscan.ScriptedDetector.from_json(script), frame_sampler=sampler,
                              human_verdicts=[G.load_json("human-accept.json")], now_utc=NOW)
        # LIMIT-TEXT ran over the three sampled frames; geometry/duration/track rows pass; the person decides
        self.assertEqual(res.event["attempts"][0]["gate_post_verdict"], "PASS")
        self.assertEqual(res.acceptance_state, "accepted")
        checks = {d["check"]: d["status"] for d in res.event["deterministic_checks"]}
        self.assertEqual(checks["duration_probe"], "PASS")
        self.assertEqual(checks["aspect_check"], "PASS")
        rows = {r["check_id"]: r["status"] for r in res.event["gate"]["post_draw"]}
        self.assertEqual(rows["LIMIT-TEXT"], "PASS")
        self.assertEqual(rows["RUNTIME-VIDEO-FRAME-TEXT"], "PASS")


class StoreInvariants(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="g-store-")
        self.store = memory.OutcomeStore(self.tmp)
        spec = G.load_spec_dict(G.SPEC_OVERLAY)
        res = driver.run_loop(spec, G.blueprint_clean(), manifest_for(spec), G.profile(),
                              artifact_provider=CountingProvider(spec), detector=detector("detector-no-text.json"),
                              human_verdicts=[G.load_json("human-accept.json")], product_entity=True, now_utc=NOW)
        self.event = res.event

    def test_validates_against_v1_contract(self):
        memory.contract().validate(self.event)
        self.assertEqual(memory.contract().schema, "OUTCOME-EVENT-v1")

    def test_event_id_is_sha_of_content_without_written_utc(self):
        body = {k: v for k, v in self.event.items() if k not in ("event_id", "written_utc")}
        self.assertEqual(self.event["event_id"], "oe-" + sha256_obj(body))
        later = dict(self.event, written_utc="2026-09-15T00:00:00Z")
        self.assertEqual(memory.event_id_for(later), self.event["event_id"])

    def test_write_then_refuse_overwrite(self):
        path = self.store.write(self.event)
        self.assertTrue(path.exists())
        with self.assertRaises(Refusal) as cm:
            self.store.write(self.event)
        self.assertEqual(cm.exception.code, refusals.OUTCOME_IMMUTABLE)
        self.assertEqual(self.store.read(self.event["event_id"])["event_id"], self.event["event_id"])

    def test_tampered_content_is_refused(self):
        ev = copy.deepcopy(self.event)
        ev["cost"]["draws"] = 7
        with self.assertRaises(Refusal) as cm:
            self.store.write(ev)
        self.assertEqual(cm.exception.code, refusals.OUTCOME_EVENT_ID_MISMATCH)

    def test_authority_must_match_profile(self):
        ev = copy.deepcopy(self.event)
        ev["acceptance"]["authority"] = "judge"
        ev = memory.finalize(ev, ev["written_utc"])
        with self.assertRaises(Refusal) as cm:
            self.store.write(ev)
        self.assertEqual(cm.exception.code, refusals.OUTCOME_AUTHORITY_MISMATCH)

    def test_accepted_without_human_is_refused(self):
        for tamper in ({"decided_by": None}, {"decided_by": "judge:sonnet"}, {"decided_by": "model:gemini"}):
            ev = copy.deepcopy(self.event)
            ev["acceptance"].update(tamper)
            ev["acceptance"] = {k: v for k, v in ev["acceptance"].items() if v is not None}
            ev = memory.finalize(ev, ev["written_utc"])
            with self.assertRaises(Refusal, msg=repr(tamper)) as cm:
                self.store.write(ev)
            self.assertEqual(cm.exception.code, refusals.OUTCOME_ACCEPTED_WITHOUT_HUMAN)

    def test_try_again_repair_is_a_schema_violation(self):
        ev = copy.deepcopy(self.event)
        ev["repairs"] = [{"repair_id": "x", "attempt_index": 2, "source": "gate", "failure_observed": "LIMIT-TEXT",
                          "failure_category": "baked_lettering", "what_changes": "try again",
                          "route_changed": False, "incremental_cost_usd": "0.03"}]   # no what_stays_invariant
        with self.assertRaises(Refusal) as cm:
            memory.finalize(ev, ev["written_utc"])
        self.assertEqual(cm.exception.code, Refusal.SCHEMA_VIOLATION)
        self.assertIn("what_stays_invariant", str(cm.exception))

    def test_undeclared_key_is_a_schema_violation(self):
        ev = copy.deepcopy(self.event)
        ev["surprise"] = 1
        with self.assertRaises(Refusal):
            memory.finalize(ev, ev["written_utc"])

    def test_v0_contract_untouched(self):
        v0 = (memory.paths.CONTRACTS / "OUTCOME-EVENT-v0.yaml").read_text(encoding="utf-8")
        self.assertIn("schema: OUTCOME-EVENT-v0", v0)
        self.assertNotIn("dry_run", v0)

    def test_placeholder_fingerprint_is_refused(self):
        spec = G.load_spec_dict(G.SPEC_OVERLAY)
        spec["job_sha256"] = 0    # what YAML makes of the fixture's unquoted zeros
        with self.assertRaises(Refusal) as cm:
            driver.run_loop(spec, G.blueprint_clean(), manifest_for(spec), G.profile(),
                            artifact_provider=CountingProvider(spec), detector=detector("detector-no-text.json"),
                            human_verdicts=[G.load_json("human-accept.json")], product_entity=True, now_utc=NOW)
        self.assertEqual(cm.exception.code, refusals.FINGERPRINT_INVALID)

    def test_dry_flag_is_true_and_said_so(self):
        self.assertTrue(self.event["dry_run"])
        self.assertIn("dry_run", (memory.CONTRACT_PATH).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()


class NoSocketDuringLoop(unittest.TestCase):
    """ZERO SPEND, proved: the whole loop — render, both gates, repair, acceptance, store — runs
    with every way out of the process replaced by a stub that raises (the pattern of
    test_route_offline.py)."""

    def test_loop_opens_nothing(self):
        import http.client
        import socket
        import ssl
        import urllib.request

        def boom(*a, **k):
            raise AssertionError("the loop tried to open a connection")

        class ExplodingSocket:
            def __init__(self, *a, **k):
                boom()

        patched = [(socket, "socket", ExplodingSocket), (socket, "create_connection", boom),
                   (socket, "socketpair", boom), (socket, "getaddrinfo", boom),
                   (ssl.SSLContext, "wrap_socket", boom),
                   (http.client.HTTPConnection, "__init__", boom),
                   (http.client.HTTPSConnection, "__init__", boom),
                   (urllib.request, "urlopen", boom)]
        saved = [(m, n, getattr(m, n)) for m, n, _ in patched]
        for m, n, v in patched:
            setattr(m, n, v)
        try:
            tmp = tempfile.mkdtemp(prefix="g-offline-")
            spec = G.load_spec_dict(G.SPEC_OVERLAY)
            res = driver.run_loop(spec, G.blueprint_clean(), manifest_for(spec), G.profile(),
                                  artifact_provider=CountingProvider(spec),
                                  detector=detector("detector-lettering-then-clean.json"),
                                  human_verdicts=[G.load_json("human-accept.json")], product_entity=True,
                                  write=True, store=memory.OutcomeStore(tmp), now_utc=NOW)
            self.assertEqual(res.acceptance_state, "accepted")
            self.assertTrue(res.event["dry_run"])
            self.assertEqual(res.event["cost"]["provider_usd_total"], "0")
        finally:
            for m, n, v in saved:
                setattr(m, n, v)
