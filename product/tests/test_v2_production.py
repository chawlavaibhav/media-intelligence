"""P1 v2 phase 5 — the head cook, the tasters, the door guard. Spec §11 tests 5, 7, 8 (journey half), and the station
halves of tests 3 and 4 (only the founder can pick a take, override the big taster, or release — and, since amendment 1
§3, nothing ever waits for the founder to do so). USD 0, real ffmpeg."""
import hashlib
import json
import unittest
from pathlib import Path

from product import flow
from product.tests import fixtures_v2 as fx
from product.tests.support import Env


def paid(e, jid, prefix=None):
    return [a for a in e.store.attempts(jid) if a["category"] == "provider" and (prefix is None or (a["node_id"] or "").startswith(prefix))]


class ContinuityChain(unittest.TestCase):
    """Spec §11 test 5 — the production log proves every film shot starts from the master plate or the previous end."""

    def test_every_shot_is_built_from_the_master_plate_or_the_previous_shots_end_frame(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            self.assertEqual(fx.film_to_hold(e, jid), "ready_for_review")
            log = e.store.artifact(jid, "production_log")
            master = e.store.node(jid, "master")["selected_asset_id"]
            self.assertEqual(log["master_plate"]["asset_id"], master)
            self.assertEqual(log["master_plate"]["approved_by"], e.user["email"])
            frames = [x for x in log["entries"] if x["node"].startswith("frame_")]
            self.assertTrue(frames)
            for fr in frames:
                self.assertIn(fr["source_kind"], ("master_plate", "previous_shot_end"), fr)
                if fr["source_kind"] == "master_plate":
                    self.assertEqual(fr["source_image"], master)
                else:
                    prev = e.store.node(jid, fr["previous_shot"])["selected_asset_id"]
                    self.assertEqual(fr["source_image"], prev)        # the previous shot's clip, its end frame extracted
                    self.assertEqual(fr["attempts"], [])               # USD 0 — no picture was generated for it
            for x in log["entries"]:
                if x["node"].startswith("shot_"):
                    frame = e.store.node(jid, x["node"].replace("shot_", "frame_"))["selected_asset_id"]
                    self.assertEqual(x["source_image"], frame)
            # generated first frames were drawn WITH the master plate as a reference
            for a in e.store.assets(jid, source="generated"):
                if (a["node_id"] or "").startswith("frame_"):
                    self.assertIn("master plate", json.loads(a["meta_json"])["source_kind"])
            rows = {r["check_id"]: r for aid in e.orch.final_assets(jid) for r in e.store.checks(aid)}
            self.assertEqual(rows["process:continuity_chain"]["status"], "PASS")
            self.assertEqual(rows["process:riskiest_first"]["status"], "PASS")
        finally:
            e.close()


class RiskiestShotFirstAndOnlyTheFounderPicksATake(unittest.TestCase):
    """Checklist E4, E6 and the small-taster half of tests 3 and 4."""

    def test_a_risky_shot_rejected_twice_goes_to_the_chef_then_to_a_still_and_the_job_continues_without_the_founder(self):
        e = Env()
        try:
            orig = e.orch.sim.small_taster__ingredient_check

            def taster(b, media, **kw):
                out = orig(b, media, **kw)
                if kw.get("node_id") in ("frame_2", "shot_2"):
                    out.update(usable=False, product_identity_ok="no", notes="the bag's flap has changed shape", differences=["flap shape"])
                return out
            e.orch.sim.small_taster__ingredient_check = taster
            jid = fx.submit_backpack_film(e)
            fx.film_to_hold(e, jid)
            self.assertEqual(e.state(jid), "ready_for_review")                                          # amendment 1 §3
            self.assertEqual(flow.rounds_used(e.store, jid, "SB-TASTER-REPLAN", "shot2"), 1)          # the chef re-planned once
            self.assertEqual(e.store.artifact(jid, "recipe")["shots"][1]["route"], "FILM-A")            # ...to a still
            frame2 = [a for a in paid(e, jid, "frame_2")]
            self.assertLessEqual(len(frame2), 4)                                                         # 2 per plan, never a 3rd identical
            n = e.store.node(jid, "frame_2")
            self.assertEqual(n["status"], "done")
            self.assertIn("rejected", json.loads(n["spec_json"])["flagged"])                            # kept, flagged
            self.assertIn("shot 2", " ".join(e.store.artifact(jid, "customer_notes")["notes"]))         # ...and the customer is told
            self.assertFalse([x for x in e.store.nodes(jid) if x["status"] == "needs_founder"])
            take = n["selected_asset_id"]
            e.operator("ops@mi.test")
            for caller in ("w-123-abc", "operator:claude (builder, P1 validation)", e.session_of("ops@mi.test"), e.session_of("buyer@acme.test")):
                with self.assertRaises(PermissionError):                                                 # picking a take stays founder-only
                    e.orch.select_take(jid, session=caller, asset_id=take, reason="this take looks fine to me, use it")
            self.assertGreaterEqual(len(e.store.events(jid, ("override_refused",))), 4)
        finally:
            e.close()


class BigTasterSendBacks(unittest.TestCase):
    """Spec §11 test 7 and checklist E5 — plus the big-taster / release half of tests 3 and 4."""

    def test_fix_redoes_only_the_named_shot_and_a_second_fail_goes_to_the_customer_with_the_report(self):
        e = Env()
        try:
            orig = e.orch.sim.big_taster__final_review
            script = ["fix", "fail", "fail"]

            def big(b, media, **kw):
                out = orig(b, media, **kw)
                v = script.pop(0) if script else "pass"
                if v == "fix":
                    out.update(verdict="fix", defects=[{"id": "D1", "where": "shot 3", "severity": "major", "description": "the clothes morph",
                                                        "earliest_stage": "generation", "shot": 3, "repair": "redraw the clothes going in"}])
                elif v == "fail":
                    out.update(verdict="fail", defects=[{"id": "D2", "where": "whole film", "severity": "blocker",
                                                         "description": "the story never shows capacity", "earliest_stage": "plan",
                                                         "shot": None, "repair": "re-plan around the full bag"}])
                return out
            e.orch.sim.big_taster__final_review = big
            jid = fx.submit_backpack_film(e)
            fx.film_to_hold(e, jid)
            # fix → only shot 3 (and what is built from it) was redone; after the second pass the fail went to the chef
            fix = e.store.artifact(jid, "internal_repair")
            self.assertIn("shot_3", fix["nodes"])
            for x in ("master", "frame_1", "shot_1", "frame_2", "shot_2", "frame_3", "music"):
                self.assertNotIn(x, fix["nodes"], x)
            self.assertEqual(flow.rounds_used(e.store, jid, "SB-BIG-FIX"), 1)
            self.assertEqual(flow.rounds_used(e.store, jid, "SB-BIG-FAIL"), 1)
            # the re-planned recipe goes back to the customer's approval (no founder step)
            before = len(paid(e, jid))
            fx.film_to_hold(e, jid)
            self.assertEqual(e.state(jid), "ready_for_review")                   # the second fail: the CUSTOMER decides
            self.assertEqual(len(paid(e, jid)) - before, 0)                       # the unchanged recipe re-bought nothing
            self.assertIn("the story never shows capacity", " ".join(e.store.artifact(jid, "customer_notes")["notes"]))
            self.assertEqual(e.store.artifact(jid, "review_report")["verdict"], "fail")
            with self.assertRaises(PermissionError):                              # overriding the big taster stays founder-only
                e.orch.override_final_review(jid, session="operator:claude", reason="the film is good enough, ship it")
            e.orch.accept(jid, e.user["email"])                                   # the customer accepts it as is
            self.assertEqual(e.state(jid), "accepted")
            rows = {r["check_id"]: r for a in e.orch.final_assets(jid) for r in e.store.checks(a)}
            self.assertTrue(rows["independent_review"]["runner"].startswith("customer:"))
            self.assertIn("over our reviewer's objection", rows["independent_review"]["detail"])
            self.assertFalse([x for x in e.store.events(jid, ("state",)) if json.loads(x["data_json"]).get("to") in
                              ("paused_for_founder", "operator_hold")])
        finally:
            e.close()


class WriteOnceDeliverables(unittest.TestCase):
    """Spec §11 test 8 — v1 lost the first-cut posters when the recomposition wrote to the same path."""

    def test_a_recomposed_poster_is_a_new_file_and_the_first_cut_is_still_on_disk_unchanged(self):
        e = Env()
        try:
            jid = e.submit("image", text="A calm launch poster for our navy travel backpack; the bag must be the first thing you see; no people.")
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            e.drain()
            self.assertEqual(e.state(jid), "ready_for_review")
            first = {a: (e.store.asset(a)["path"], e.store.asset(a)["sha256"]) for a in e.orch.final_assets(jid)}
            e.orch.request_changes(jid, e.user["email"], [{"target": None, "text": "more space around the logo please"}])
            e.drain()
            second = e.orch.final_assets(jid)
            self.assertEqual(len(second), len(first))
            for a in second:
                self.assertNotIn(e.store.asset(a)["path"], [p for p, _ in first.values()])
            for aid, (path, sha) in first.items():
                self.assertTrue(Path(path).exists(), path)
                self.assertEqual(hashlib.sha256(Path(path).read_bytes()).hexdigest(), sha)
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
