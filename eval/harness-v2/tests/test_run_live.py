"""EVAL-040 live runner (run_live.py) - fake transports and fake token sources only.

Every test runs under NoNetworkTestCase: sockets and urlopen raise, every key name is stripped from the
environment, the key loader points at a throw-away file, and the authorisation is a TEST fixture at a
temp path (never eval/harness-v2/authorization.local.yaml).
"""
import base64
import hashlib
import json
import os
import re
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, fixed_clock, hv2_paths
import run_live as RL
import store as S
import surfaces
import transports as T
from adapters import adapter_for
from budget_guard import NotAuthorised
from instruments import imageio as IO

SIX_CASES = ["IMG-CORE-01", "IMG-CORE-02", "IMG-CORE-03", "IMG-CORE-04", "IMG-TEXT-01", "IMG-TEXT-02"]
SIX_ROUTES = {"gpt-image-2", "nano-banana-2", "nano-banana-pro", "seedream-5-pro", "flux-2-pro", "qwen-image-3", "recraft-v4"}
CANARY = "CANARY-fal-key-value-0f9e8d7c6b5a"


def png_bytes(w: int = 32, h: int = 40, rgb=(200, 120, 40)) -> bytes:
    return IO.encode_png([bytes(rgb) * w for _ in range(h)], w, h, 3)


def fal_transport(png: bytes, outcome: str = "ok") -> T.FakeTransport:
    if outcome == "error":
        gets = [(200, {"status": "COMPLETED"}), (200, {"error": {"type": "internal_server_error", "message": "upstream"}})]
    elif outcome == "refusal":
        gets = [(200, {"status": "COMPLETED"}), (200, {"detail": "content policy violation: blocked"})]
    else:
        gets = [(200, {"status": "IN_QUEUE"}), (200, {"status": "COMPLETED"}),
                (200, {"images": [{"url": "https://v3.fal.media/files/fake/out.png", "content_type": "image/png"}]})]
    return T.FakeTransport(
        posts=[(200, {"request_id": "req-1", "status_url": "https://queue.fal.run/x/requests/req-1/status",
                      "response_url": "https://queue.fal.run/x/requests/req-1", "status": "IN_QUEUE"})],
        gets=gets, downloads=[(200, png, "image/png")])


def vertex_transport(png: bytes, outcome: str = "ok") -> T.FakeTransport:
    if outcome == "error":
        return T.FakeTransport(posts=[(400, {"error": {"code": 400, "status": "INVALID_ARGUMENT", "message": "bad"}})])
    if outcome == "refusal":
        return T.FakeTransport(posts=[(200, {"responseId": "r", "candidates": []})])
    body = {"responseId": "resp-1", "candidates": [{"finishReason": "STOP", "content": {"parts": [
        {"inlineData": {"mimeType": "image/png", "data": base64.b64encode(png).decode("ascii")}}]}}]}
    return T.FakeTransport(posts=[(200, body)])


class FakeFactory:
    """transport_factory(entry, trial): a fresh scripted transport per trial; records every transport built."""

    def __init__(self, outcome_for=None):
        self.transports: list = []
        self.outcome_for = outcome_for or (lambda trial: "ok")

    def __call__(self, entry, trial):
        rgb = (10 * trial["repeat_index"] + 50, 90, 200 - 20 * trial["repeat_index"])
        png = png_bytes(rgb=rgb)
        t = (fal_transport if entry.surface == "fal" else vertex_transport)(png, self.outcome_for(trial))
        self.transports.append(t)
        return t

    @property
    def submits(self) -> int:
        return sum(t.submits for t in self.transports)


class RunnerBase(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        os.environ["FAL_KEY"] = CANARY
        self.out = self.tmp / "runs" / "run-x"
        self.auth = self.write_auth()
        self.factory = FakeFactory()
        self.adapter_kwargs = {"token_source": T.FakeTokenSource(), "sleep": lambda s: None, "clock": fixed_clock()}
        self.gate_script = self.tmp / "no-such-gate.py"

    def plan(self, cases=("IMG-CORE-01",), routes=("gpt-image-2", "nano-banana-2"), run_id="run-x", out=None, **kw):
        return RL.build_plan(out or self.out, run_id, cases=list(cases), routes=list(routes) if routes else None,
                             tranche="1a", auth_path=self.auth, **kw)

    def runner(self, run_id="run-x", out=None, auth=None, factory=None, **kw):
        return RL.LiveRunner(out or self.out, run_id, auth_path=auth or self.auth, transport_factory=factory or self.factory,
                             adapter_kwargs=self.adapter_kwargs, gate_script=self.gate_script, **kw)


# ====================================================================== plan
class PlanTest(RunnerBase):
    """The 76-trial plan is built once per process (a plan is never overwritten) in its own throw-away directory."""
    _full = None
    _cache_dir = None

    @classmethod
    def setUpClass(cls):
        import tempfile
        cls._cache_dir = Path(tempfile.mkdtemp(prefix="hv2-plan-cache-"))

    @classmethod
    def tearDownClass(cls):
        import shutil
        shutil.rmtree(cls._cache_dir, ignore_errors=True)

    def full_plan(self):
        if PlanTest._full is None:
            PlanTest._full = RL.build_plan(self.full_out, "run-full", cases=SIX_CASES, routes=None, tranche="1a", auth_path=self.auth)
        return PlanTest._full

    @property
    def full_out(self):
        return PlanTest._cache_dir / "run-full"

    def test_plan_is_the_authorised_image_round(self):
        plan = self.full_plan()
        trials = plan["trials"]
        self.assertEqual(len(trials), 76, "IMG-CORE-01..04 + IMG-TEXT-01/02, six routes + recraft on the text cases")
        self.assertEqual({t["route_key"] for t in trials}, SIX_ROUTES)
        self.assertTrue(all(t["tranche"] == "1a" for t in trials))
        total = sum(Decimal(t["estimated_usd_equiv"]) for t in trials)
        self.assertLessEqual(abs(total - Decimal("4.858")), Decimal("0.01"), total)
        excluded = {(e["case_id"], e["route_key"]) for e in plan["excluded"]}
        self.assertIn(("IMG-CORE-01", "sd3.5-large"), excluded)
        self.assertIn(("IMG-CORE-01", "mai-image-2.6"), excluded)
        self.assertTrue(all(e["reason"] for e in plan["excluded"]))
        self.assertEqual(plan["header"]["roster_sha256"], "99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46")
        self.assertEqual(plan["header"]["item_basis_commit"], "0596aa2")
        self.assertEqual(plan["header"]["tranche_id"], "EVAL-040-TRANCHE-1")
        self.assertTrue(plan["header"]["freeze_matches_item_basis"])

    def test_plan_ordering_repeat_major_all_repeat_1_then_all_repeat_2(self):
        # Controller change before the first lane (8 Sep 2026): identical unseeded bodies must not reach a
        # provider seconds apart, so the WHOLE lane's repeat 1 runs before any repeat 2.
        trials = self.full_plan()["trials"]
        self.assertEqual([t["seq"] for t in trials], list(range(1, 77)))
        reps = [t["repeat_index"] for t in trials]
        n = len(reps) // 2
        self.assertEqual(reps, [1] * n + [2] * n, "every repeat 1 in the lane before any repeat 2")
        for rep in (1, 2):
            block = [t for t in trials if t["repeat_index"] == rep]
            cases_in_order = []
            for t in block:
                if not cases_in_order or cases_in_order[-1] != t["case_id"]:
                    cases_in_order.append(t["case_id"])
            self.assertEqual(cases_in_order, SIX_CASES, f"repeat {rep}: cases contiguous, in the requested order")
        r1 = [(t["case_id"], t["route_key"], t["arm"]) for t in trials if t["repeat_index"] == 1]
        r2 = [(t["case_id"], t["route_key"], t["arm"]) for t in trials if t["repeat_index"] == 2]
        self.assertEqual(r1, r2, "the repeat-2 block mirrors the repeat-1 block exactly")

    def test_plan_files_and_no_key_value(self):
        self.full_plan()
        out = self.full_out
        self.assertTrue((out / "PLAN.yaml").exists() and (out / "PLAN.sha256").exists())
        self.assertEqual((out / "PLAN.sha256").read_text().split()[0], hashlib.sha256((out / "PLAN.yaml").read_bytes()).hexdigest())
        text = (out / "PLAN.yaml").read_text()
        self.assertNotIn(CANARY, text)
        self.assertIn("<KEY:FAL_KEY>", text) if "headers" in text else None
        self.assertNotIn("Key fal_", text)
        loaded = yaml.safe_load(text)
        self.assertEqual(loaded["header"]["run_id"], "run-full")
        self.assertEqual({t["trial_id"] for t in loaded["trials"]}, {t["trial_id"] for t in self.full_plan()["trials"]})

    def test_plan_route_and_tranche_filters(self):
        plan = self.plan(cases=("IMG-CORE-02",), routes=("gpt-image-2", "flux-2-pro"))
        self.assertEqual([(t["route_key"], t["repeat_index"]) for t in plan["trials"]],
                         [("gpt-image-2", 1), ("flux-2-pro", 1), ("gpt-image-2", 2), ("flux-2-pro", 2)])
        with self.assertRaises(RL.PlanRefused):
            RL.build_plan(self.tmp / "p2", "p2", cases=["IMG-CORE-01"], routes=["gpt-image-2"], tranche="1b", auth_path=self.auth)
        with self.assertRaises(RL.PlanRefused):
            RL.build_plan(self.tmp / "p3", "p3", cases=["NO-SUCH-CASE"], routes=None, tranche="1a", auth_path=self.auth)
        with self.assertRaises(RL.PlanRefused):
            RL.build_plan(self.tmp / "p4", "p4", cases=["IMG-CORE-01"], routes=["sd3.5-large"], tranche="1a", auth_path=self.auth)

    def test_plan_needs_a_permitted_authorisation(self):
        with self.assertRaises(NotAuthorised):
            RL.build_plan(self.tmp / "p5", "p5", cases=["IMG-CORE-01"], routes=["gpt-image-2"], tranche="1a", auth_path=self.tmp / "absent.yaml")

    def test_plan_refuses_to_overwrite(self):
        self.plan(out=self.tmp / "p6", run_id="p6")
        with self.assertRaises(RL.PlanRefused):
            self.plan(out=self.tmp / "p6", run_id="p6")


# ====================================================================== execute
class ExecuteTest(RunnerBase):
    def test_refuses_without_authorisation_file(self):
        self.plan()
        r = self.runner(auth=self.tmp / "absent.yaml")
        with self.assertRaises(NotAuthorised):
            r.execute()
        self.assertEqual(self.factory.submits, 0)
        self.assertFalse((self.out / "ledger").exists())

    def test_refuses_without_plan_or_with_a_changed_plan(self):
        with self.assertRaises(RL.PlanRefused):
            self.runner().execute()
        self.plan()
        p = self.out / "PLAN.yaml"
        p.write_text(p.read_text().replace("gpt-image-2", "seedream-5-pro"))
        with self.assertRaises(RL.PlanRefused):
            self.runner().execute()
        self.assertEqual(self.factory.submits, 0)

    def test_runs_the_plan_in_order_and_persists_everything(self):
        plan = self.plan()
        seen = []
        orig = RL.adapter_for

        def spy(entry, **kw):
            seen.append(kw)
            return orig(entry, **kw)
        r = self.runner(adapter_for=spy)
        summary = r.execute()
        self.assertEqual(summary["status"], "completed")
        self.assertEqual(summary["dispatched"], 4)
        self.assertEqual(self.factory.submits, 4)
        self.assertTrue(all(kw["allow_default_token_source"] is True for kw in seen), "the live runner is the only place the flag is set")
        store = S.SealedStore(self.out / "artifacts")
        for t in plan["trials"]:
            a = json.loads(store.attempt_path(t["trial_id"]).read_text())
            self.assertEqual(a["status"], "ok", t["trial_id"])
            self.assertTrue(store.request_path(t["trial_id"]).exists())
            self.assertTrue(store.verify(a["artifact"] | {"relative_path": a["artifact"]["relative_path"]}))
        order = [json.loads(l)["trial_id"] for l in (self.out / "RUN-LOG.jsonl").read_text().splitlines() if '"dispatched"' in l]
        self.assertEqual(order, [t["trial_id"] for t in plan["trials"]])
        rows = [json.loads(l) for l in (self.out / "ledger" / "run-x" / "spend-ledger.jsonl").read_text().splitlines()]
        self.assertEqual([x["type"] for x in rows], ["reservation", "spend"] * 4)
        self.assertEqual({x["billing_pool"] for x in rows}, {"cash", "credits"})

    def test_smoke_performs_exactly_one_submit(self):
        summary = RL.smoke(self.out, "run-x", case_id="IMG-CORE-01", route_key="nano-banana-2", auth_path=self.auth,
                           transport_factory=self.factory, adapter_kwargs=self.adapter_kwargs, gate_script=self.gate_script)
        self.assertEqual(self.factory.submits, 1)
        self.assertEqual(summary["dispatched"], 1)
        plan = yaml.safe_load((self.out / "PLAN.yaml").read_text())
        self.assertEqual(plan["header"]["mode"], "smoke")
        self.assertEqual(len(plan["trials"]), 1)
        self.assertEqual(plan["trials"][0]["repeat_index"], 1)
        r = self.runner()
        again = r.execute()          # the smoke plan is complete; a second execute dispatches nothing
        self.assertEqual((again["dispatched"], self.factory.submits), (0, 1))

    def test_cap_breach_stops_cleanly_and_persists_state(self):
        auth = self.write_auth(ceiling="0.06", caps=("0.06", "0.06"), name="tiny.yaml")
        self.plan(routes=("gpt-image-2", "flux-2-pro"))            # 0.053 then 0.03: the second breaches 0.06
        r = self.runner(auth=auth)
        summary = r.execute()
        self.assertEqual(summary["status"], "stopped_cap_reached")
        self.assertEqual(self.factory.submits, 1)
        self.assertEqual(summary["dispatched"], 1)
        state = json.loads((self.out / "RUN-STATE.json").read_text())
        self.assertEqual(state["status"], "stopped_cap_reached")
        self.assertIn("BudgetExceeded", state["stop_reason"])
        rows = [json.loads(l) for l in (self.out / "ledger" / "run-x" / "spend-ledger.jsonl").read_text().splitlines()]
        self.assertEqual([x["type"] for x in rows], ["reservation", "spend"])
        st = RL.status(self.out, "run-x", auth_path=auth)
        self.assertEqual((st["done"], st["remaining"]), (1, 3))

    def test_provider_error_persists_an_attempt_and_the_run_continues(self):
        self.plan(routes=("gpt-image-2", "nano-banana-2"))
        self.factory = FakeFactory(outcome_for=lambda t: "error" if t["seq"] == 1 else ("refusal" if t["seq"] == 2 else "ok"))
        summary = self.runner().execute()
        self.assertEqual(summary["status"], "completed")
        self.assertEqual(self.factory.submits, 4)
        store = S.SealedStore(self.out / "artifacts")
        statuses = [json.loads(store.attempt_path(t).read_text())["status"] for t in summary["trial_order"]]
        self.assertEqual(statuses, ["error", "refusal", "ok", "ok"])
        self.assertEqual(summary["errors"][0]["trial_id"], summary["trial_order"][0])
        rows = [json.loads(l) for l in (self.out / "ledger" / "run-x" / "spend-ledger.jsonl").read_text().splitlines()]
        self.assertEqual([x["type"] for x in rows], ["reservation", "spend"] * 4, "a failed call is a trial and is settled")

    def test_pre_dispatch_refusal_is_recorded_and_the_run_continues(self):
        os.environ.pop("FAL_KEY", None)                              # fal routes: key missing -> PreDispatchRefusal, nothing sent
        self.plan(routes=("gpt-image-2", "nano-banana-2"))
        summary = self.runner().execute()
        self.assertEqual(summary["status"], "completed")
        self.assertEqual(self.factory.submits, 2, "only the two vertex trials were sent")
        refusals = sorted(p.name for p in (self.out / "trials").glob("*.pre_dispatch_refusal.json"))
        self.assertEqual(len(refusals), 2)
        rec = json.loads((self.out / "trials" / refusals[0]).read_text())
        self.assertIn("FAL_KEY", rec["reason"])
        self.assertNotIn(CANARY, json.dumps(rec))
        rows = [json.loads(l) for l in (self.out / "ledger" / "run-x" / "spend-ledger.jsonl").read_text().splitlines()]
        self.assertEqual(rows.count and [x["type"] for x in rows].count("release"), 2, "a refusal before the send releases its reservation")
        again = self.runner().execute()
        self.assertEqual(again["dispatched"], 0, "a refused trial id is terminal in this run (its request is sealed); a new run id re-plans it")

    def test_harness_exception_on_one_trial_is_recorded_and_the_run_continues(self):
        self.plan(routes=("gpt-image-2", "nano-banana-2"))

        def boom(entry, trial):
            if trial["seq"] == 1:
                raise RuntimeError("factory exploded on purpose")
            return self.factory(entry, trial)
        summary = self.runner(factory=boom).execute()
        self.assertEqual(summary["status"], "completed")
        self.assertEqual(self.factory.submits, 3)
        errs = list((self.out / "trials").glob("*.harness_error.json"))
        self.assertEqual(len(errs), 1)
        self.assertIn("factory exploded", json.loads(errs[0].read_text())["error"])

    def test_resume_skips_completed_trials(self):
        plan = self.plan()
        first = self.runner().execute(max_dispatches=2)
        self.assertEqual((first["dispatched"], first["status"]), (2, "paused_max_dispatches"))
        second = self.runner().execute()
        self.assertEqual((second["skipped"], second["dispatched"], second["status"]), (2, 2, "completed"))
        self.assertEqual(self.factory.submits, 4)
        third = self.runner().execute()
        self.assertEqual((third["skipped"], third["dispatched"]), (4, 0))
        self.assertEqual(self.factory.submits, 4)
        store = S.SealedStore(self.out / "artifacts")
        self.assertEqual(len(store.manifest()), 4)
        self.assertEqual(sorted(a["trial_id"] for a in store.manifest()), sorted(t["trial_id"] for t in plan["trials"]))

    def test_instruments_run_after_each_artifact_and_never_block(self):
        gate = self.tmp / "fake_gate.py"
        gate.write_text("import json,sys\nargs=sys.argv\nout=args[args.index('--json')+1]\n"
                        "json.dump({'gate':'fake','verdict':'PASS','artifact':args[args.index('--artifact')+1]}, open(out,'w'))\n")
        self.gate_script = gate
        plan = self.plan(routes=("gpt-image-2",))
        r = self.runner()
        summary = r.execute()
        self.assertEqual(summary["status"], "completed")
        t1, t2 = plan["trials"][0]["trial_id"], plan["trials"][1]["trial_id"]
        i1 = json.loads((self.out / "instruments" / f"{t1}.json").read_text())
        i2 = json.loads((self.out / "instruments" / f"{t2}.json").read_text())
        self.assertEqual(i1["format_probe"]["verdict"], "absent")                 # criterion_not_frozen (MD-C1): observation only
        self.assertEqual(i1["format_probe"]["note"], "criterion_not_frozen")
        self.assertTrue(i1["format_probe"]["measurement"]["probe"]["width"])
        self.assertEqual(i1["gate_post"]["status"], "ran")
        self.assertEqual(i1["gate_post"]["report"]["verdict"], "PASS")
        self.assertTrue(i1["gate_post"]["json_path"].startswith(str(self.out / "instruments")))
        self.assertIsNone(i1["repeat_consistency"])
        self.assertEqual(i2["repeat_consistency"]["note"], "criterion_not_frozen")
        self.assertEqual(i2["repeat_consistency"]["measurement"]["group"], "unseeded")
        self.assertGreater(i2["repeat_consistency"]["measurement"]["dhash_hamming_max"], -1)

    def test_instrument_crash_never_blocks_the_run(self):
        self.plan(routes=("gpt-image-2",))
        import instruments.format_probe as FP
        saved = FP.evaluate
        FP.evaluate = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("probe exploded"))
        try:
            summary = self.runner().execute()
        finally:
            FP.evaluate = saved
        self.assertEqual((summary["status"], summary["dispatched"]), ("completed", 2))
        i = json.loads((self.out / "instruments" / f"{summary['trial_order'][0]}.json").read_text())
        self.assertIn("probe exploded", i["errors"][0])
        self.assertEqual(i["gate_post"]["status"], "not_available_on_base")

    def test_no_key_value_anywhere_under_out(self):
        self.plan(routes=("gpt-image-2", "nano-banana-2"))
        self.runner().execute()
        for p in self.out.rglob("*"):
            if p.is_file():
                self.assertNotIn(CANARY.encode(), p.read_bytes(), str(p))
                self.assertNotIn(b"FAKE-TOKEN-NOT-A-CREDENTIAL", p.read_bytes(), str(p))

    def test_everything_is_written_under_out(self):
        self.out.parent.mkdir(parents=True, exist_ok=True)      # the run directory's parent is the caller's
        before = {p for p in self.tmp.rglob("*")}
        self.plan(routes=("gpt-image-2",))
        self.runner().execute()
        new = {p for p in self.tmp.rglob("*")} - before
        outside = [str(p) for p in new if self.out not in p.parents and p != self.out]
        self.assertEqual(outside, [])

    def test_status_reports_counts_cost_and_headroom(self):
        self.plan(routes=("gpt-image-2", "nano-banana-2"))
        self.runner().execute(max_dispatches=3)
        st = RL.status(self.out, "run-x", auth_path=self.auth)
        self.assertEqual((st["planned"], st["done"], st["remaining"]), (4, 3, 1))
        self.assertEqual(st["settled_by_pool"]["cash"]["usd_equiv"], "0.106000")     # gpt r1 + gpt r2
        self.assertEqual(st["settled_by_pool"]["credits"]["usd_equiv"], "0.067000")  # nano r1
        self.assertEqual(Decimal(st["remaining_headroom_usd_equiv"]), Decimal("200.00") - Decimal("0.173"))
        self.assertEqual(st["errors"], [])


# ====================================================================== hygiene + CLI
class HygieneTest(NoNetworkTestCase):
    def test_only_the_live_runner_sets_allow_default_token_source(self):
        hits = []
        for p in hv2_paths.HERE.rglob("*.py"):
            if "tests" in p.parts or "__pycache__" in p.parts:
                continue
            if re.search(r"allow_default_token_source\s*=\s*True", p.read_text(encoding="utf-8")):
                hits.append(p.name)
        self.assertEqual(hits, ["run_live.py"])

    def test_runner_imports_no_network_module(self):
        src = (hv2_paths.HERE / "run_live.py").read_text()
        for mod in ("url" + "lib", "http\\." + "client", "sock" + "et", "requ" + "ests"):
            self.assertIsNone(re.search(r"^\s*(import|from)\s+" + mod + r"\b", src, re.M), mod)


class CliTest(RunnerBase):
    def test_plan_and_status_via_main(self):
        out = self.tmp / "cli-run"
        rc = RL.main(["plan", "--run-id", "cli-run", "--cases", "IMG-CORE-03", "--routes", "gpt-image-2,qwen-image-3",
                      "--tranche", "1a", "--out", str(out), "--auth", str(self.auth)])
        self.assertEqual(rc, 0)
        self.assertTrue((out / "PLAN.yaml").exists())
        rc = RL.main(["status", "--run-id", "cli-run", "--out", str(out), "--auth", str(self.auth)])
        self.assertEqual(rc, 0)

    def test_execute_via_main_refuses_without_authorisation_and_sends_nothing(self):
        out = self.tmp / "cli-run2"
        RL.main(["plan", "--run-id", "cli-run2", "--cases", "IMG-CORE-03", "--routes", "gpt-image-2", "--out", str(out), "--auth", str(self.auth)])
        rc = RL.main(["execute", "--run-id", "cli-run2", "--out", str(out), "--auth", str(self.tmp / "absent.yaml")])
        self.assertNotEqual(rc, 0)
        self.assertFalse((out / "ledger").exists())


if __name__ == "__main__":
    unittest.main()
