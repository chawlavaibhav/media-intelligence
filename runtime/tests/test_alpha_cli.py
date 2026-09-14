"""The one-command dry Alpha-1 chain (runtime/alpha): end to end, offline, reproducible, refusing precisely.

Every test here runs the real modules the lanes built (intake, compiler, router, execution bridge,
gates, loop, outcome store, template library) over committed briefs; nothing is mocked except the
network, which is made to explode so any attempt to open a socket fails the test.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import _bootstrap as B  # noqa: F401  (puts the checkout root on sys.path)

from runtime.alpha import battery as battery_module
from runtime.alpha.run import AlphaRunner

ROOT = B.ROOT
BRIEFS = ROOT / "runtime" / "fixtures" / "alpha-briefs"
AT = "2026-09-14T12:00:00Z"

STUB = textwrap.dedent('''
    import http.client, socket, ssl, sys, urllib.request
    from pathlib import Path
    def boom(*a, **k):
        raise AssertionError("the dry chain tried to open a connection")
    class ExplodingSocket:
        def __init__(self, *a, **k):
            boom()
    socket.socket = ExplodingSocket
    socket.create_connection = boom
    socket.getaddrinfo = boom
    ssl.SSLContext.wrap_socket = boom
    http.client.HTTPConnection.__init__ = boom
    http.client.HTTPSConnection.__init__ = boom
    urllib.request.urlopen = boom
    root = Path(sys.argv[1]); store = sys.argv[2]
    sys.path.insert(0, str(root))
    from runtime.alpha.run import AlphaRunner
    r = AlphaRunner(root=root)
    res = r.run(root / "runtime/fixtures/alpha-briefs/img-text-02-conformant.json", store_root=store,
                human_verdict="accept", post_draw="clean", at="2026-09-14T12:00:00Z")
    assert res.final_state == "accepted", res.summary()
    assert res.objects["template"]["template_id"].startswith("tpl-")
    print("OK", res.objects["event"]["event_id"])
''')


class OneCommandChain(unittest.TestCase):
    def setUp(self):
        self.runner = AlphaRunner(root=ROOT)
        self.store = Path(tempfile.mkdtemp(prefix="alpha-test-"))

    def run_brief(self, name, **kw):
        return self.runner.run(BRIEFS / f"{name}.json", store_root=self.store, at=AT, **kw)

    def test_the_happy_path_reaches_an_accepted_event_and_a_template_with_no_hand_authored_object(self):
        res = self.run_brief("img-text-02-conformant", human_verdict="accept")
        self.assertEqual(res.final_state, "accepted", res.summary())
        stages = {s.stage: s.status for s in res.stages}
        self.assertEqual(stages, {"intake": "ok", "spec": "ok", "canon": "ok", "route": "ok", "manifest": "ok",
                                  "dry_execution": "ok", "loop": "ok", "outcome_event": "ok", "template": "ok"})
        spec = res.objects["spec"]
        self.assertEqual(spec["exact_text"]["text_mechanism"], "deterministic_text_composition")
        decision = res.objects["decision"]
        self.assertFalse(decision["manual_route_required"])
        self.assertIsNotNone(decision["fallback"])
        composed = [r for r in decision["selection_basis"]["self_composed_requirements"]]
        self.assertEqual(composed[0]["cell_selected"], "IMG-TEXT/flux-2-pro+code_overlay")
        manifest = res.objects["manifest"]
        self.assertEqual(manifest["dispatch_mode"], "dry")
        self.assertTrue(all(a["price"]["price_pin_ref"] for a in manifest["attempts"]))
        self.assertEqual(res.objects["execution"]["status"], "dry_complete")
        event = res.objects["event"]
        self.assertTrue(event["dry_run"])
        self.assertEqual(event["acceptance"]["decision"], "accepted")
        self.assertEqual(event["acceptance"]["authority"], "human")
        self.assertEqual(event["route"]["text_mechanism"], "deterministic_text_composition")
        self.assertEqual(res.objects["template"]["status"], "reusable_dry_only")
        # the run wrote every object it produced
        for name in ("01-job.json", "02-spec.json", "04-route-decision.json", "05-execution-manifest.json",
                     "07-package.txt", "08-gate-pre.json", "09-loop.json", "10-outcome-event.json", "11-template.json"):
            self.assertTrue((Path(res.run_dir) / name).exists(), name)

    def test_a_repeat_job_is_served_from_the_template_without_a_reasoning_pass(self):
        first = self.run_brief("img-text-02-conformant", human_verdict="accept")
        raw = json.loads((BRIEFS / "img-text-02-conformant.json").read_text(encoding="utf-8"))
        raw["job_id"] = "alpha-dry-img-text-02-repeat-test"
        raw.pop("_provenance", None)
        path = self.store / "repeat.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        again = self.runner.run(path, store_root=self.store, at="2026-09-14T13:00:00Z", human_verdict="accept")
        self.assertEqual(again.final_state, "accepted", again.summary())
        self.assertEqual(again.objects["spec"]["blueprint"]["planner"], f"template:{first.objects['template']['template_id']}")

    def test_the_bounded_repair_path_and_its_exhaustion(self):
        res = self.run_brief("img-text-02-conformant", human_verdict="accept", post_draw="lettering_then_clean")
        self.assertEqual(res.final_state, "accepted")
        loop = res.objects["loop"]
        self.assertEqual((len(loop.attempts), len(loop.repairs)), (2, 1))
        self.assertEqual(loop.attempts[1]["is_repair_of"], loop.attempts[0]["attempt_id"])
        store2 = Path(tempfile.mkdtemp(prefix="alpha-test-"))
        res2 = self.runner.run(BRIEFS / "img-text-02-conformant.json", store_root=store2, at=AT,
                               human_verdict="accept", post_draw="lettering_always")
        self.assertEqual(res2.final_state, "abandoned")
        self.assertEqual(res2.objects["loop"].refusal, "REPAIR_ALLOWANCE_EXHAUSTED")
        self.assertEqual(len(res2.objects["loop"].attempts), 2)      # the profile's draws; no hidden retry

    def test_precise_refusals(self):
        consent = self.run_brief("img-edit-01")
        self.assertEqual((consent.final_state, consent.refusal["code"]), ("refused_at_intake", "CONSENT_MISSING"))
        with_consent = self.run_brief("img-edit-01", consent_ref="CONSENT-TEST")
        self.assertEqual((with_consent.final_state, with_consent.refusal["code"]),
                         ("manual_route_required", "MANUAL_ROUTE_REQUIRED"))
        self.assertIn("fallback_required", with_consent.refusal["message"])
        kind = self.run_brief("vid-topo3-01")
        self.assertEqual((kind.final_state, kind.refusal["code"]), ("refused_at_intake", "KIND_NOT_IN_PROFILE"))
        mkt = self.run_brief("mkt-001")
        self.assertEqual(mkt.refusal["code"], "KIND_NOT_IN_PROFILE")
        frozen = self.run_brief("img-text-02", human_verdict="accept")
        self.assertEqual(frozen.refusal["code"], "PRE_DISPATCH_GATE_FAIL")
        self.assertIn("LIMIT-TEXT", frozen.refusal["message"])

    def test_the_cost_ceiling_propagates_and_hands_to_a_person_before_dispatch(self):
        raw = json.loads((BRIEFS / "img-text-02-conformant.json").read_text(encoding="utf-8"))
        raw["job_id"] = "alpha-dry-ceiling-test"
        raw["cost_ceiling_usd"] = "0.02"
        path = self.store / "ceiling.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        res = self.runner.run(path, store_root=self.store, at=AT)
        self.assertEqual(res.refusal["code"], "MANUAL_ROUTE_REQUIRED")
        self.assertIn("cost_envelope_exceeded", res.refusal["message"])
        self.assertIsNone(res.objects.get("manifest"))       # nothing rendered, nothing sent

    def test_the_same_brief_at_the_same_time_gives_the_same_ids(self):
        a = self.run_brief("img-text-02-conformant", human_verdict="accept")
        b = self.runner.run(BRIEFS / "img-text-02-conformant.json",
                            store_root=Path(tempfile.mkdtemp(prefix="alpha-test-")), at=AT, human_verdict="accept")
        for key in ("spec", "decision", "manifest", "event"):
            ida = a.objects[key].get("spec_id") or a.objects[key].get("decision_id") or a.objects[key].get("manifest_id") or a.objects[key].get("event_id")
            idb = b.objects[key].get("spec_id") or b.objects[key].get("decision_id") or b.objects[key].get("manifest_id") or b.objects[key].get("event_id")
            self.assertEqual(ida, idb, key)


class BatteryManifest(unittest.TestCase):
    def test_every_battery_brief_exists_and_the_manifest_names_the_profile_and_time(self):
        import yaml
        m = yaml.safe_load((ROOT / "runtime/battery/DRY-ALPHA-BATTERY-2026-09-14.yaml").read_text(encoding="utf-8"))
        self.assertEqual(m["profile"], "dry")
        self.assertEqual(m["at"], AT)
        self.assertGreaterEqual(len(m["runs"]), 10)
        for entry in m["runs"]:
            self.assertTrue((ROOT / entry["brief"]).exists(), entry["brief"])
            self.assertIn(entry.get("post_draw") or "clean", ("clean", "lettering_then_clean", "lettering_always", "no_artifact"))

    def test_the_committed_results_match_a_fresh_run_of_the_manifest(self):
        """The committed SUMMARY.yaml is regenerated into a temp dir and compared field by field on
        the observed outcomes (states, refusal codes, routes, gate verdicts, counts). Ids are
        deterministic at the fixed timestamp, so they are compared too."""
        import yaml
        committed = yaml.safe_load((ROOT / "runtime/battery/results/2026-09-14/SUMMARY.yaml").read_text(encoding="utf-8"))
        out = Path(tempfile.mkdtemp(prefix="alpha-battery-out-"))
        fresh = battery_module.run_battery(ROOT / "runtime/battery/DRY-ALPHA-BATTERY-2026-09-14.yaml", out,
                                           Path(tempfile.mkdtemp(prefix="alpha-battery-store-")))
        self.assertEqual([r["id"] for r in fresh["runs"]], [r["id"] for r in committed["runs"]])
        for got, want in zip(fresh["runs"], committed["runs"]):
            self.assertEqual(got["observed"], want["observed"], got["id"])


class NoSocketEver(unittest.TestCase):
    def test_the_whole_chain_runs_under_an_exploding_socket_in_a_fresh_interpreter(self):
        store = tempfile.mkdtemp(prefix="alpha-nosock-")
        proc = subprocess.run([sys.executable, "-c", STUB, str(ROOT), store], capture_output=True, text=True, timeout=600)
        self.assertEqual(proc.returncode, 0, proc.stderr[-3000:])
        self.assertTrue(proc.stdout.startswith("OK oe-"), proc.stdout)


if __name__ == "__main__":
    unittest.main()
