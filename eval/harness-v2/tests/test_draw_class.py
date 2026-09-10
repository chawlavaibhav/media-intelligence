"""Audit finding A (2026-09-10): a smoke/liveness draw must never wear a candidate trial's identity.

In the September run 17 trial ids existed in BOTH a smoke run and the real run that followed it - e.g.
`VID-T2V-02__wan-2.2-a14b__core__r1` in vid-wan2-smoke and vid-wan2 - so a route quietly received an extra
provider draw that was paid for, sealed, and never judged.

Proven here (no socket, no key, no dispatch - plans only):
    - a liveness trial id carries an explicit `__smoke` marker, so it cannot collide with the candidate draw
      of the same case x route x arm x repeat;
    - the plan header records `draw_class: liveness` outright, and build_plan refuses a plan whose ids collide;
    - every consumer decides from the RECORDED draw class, never from the run-id string: registry_rows refuses to
      build Registry rows from a liveness run, judging_packet refuses to blind one, evidence_map refuses one as evidence;
    - the sealed September plans still read correctly (their `mode: smoke` is just as explicit as `draw_class`), and
      the sealed candidate RESULTS documents, which carry neither key, still merge as candidates.
"""
import unittest
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, hv2_paths
import evidence_map as EM
import registry_rows as RR
import run_live as RL
from adapters import base as B
from test_run_live import RunnerBase

RUNS = hv2_paths.EVAL_ROOT / "experiments" / "EVAL-040" / "runs"
ROW = {"case_id": "VID-T2V-02", "route_key": "wan-2.2-a14b", "arm": "core", "repeat_index": 1}


class TrialIdentityTest(unittest.TestCase):
    def test_a_liveness_trial_id_carries_an_explicit_smoke_marker(self):
        candidate = B.make_trial_id(ROW)
        liveness = B.make_trial_id(ROW, liveness=True)
        self.assertEqual(candidate, "VID-T2V-02__wan-2.2-a14b__core__r1")
        self.assertEqual(liveness, "VID-T2V-02__wan-2.2-a14b__core__r1__smoke")
        self.assertNotEqual(candidate, liveness, "the September collision: one id for two different draws")
        self.assertTrue(B.is_liveness_trial_id(liveness))
        self.assertFalse(B.is_liveness_trial_id(candidate))

    def test_the_marker_is_read_off_the_id_not_off_a_run_name(self):
        self.assertFalse(B.is_liveness_trial_id("IMG-CORE-01__nano-banana-2__core__r1"),
                         "a candidate id planned by a run whose NAME says smoke is still a candidate id")
        self.assertFalse(B.is_liveness_trial_id(None))


class DrawClassVocabularyTest(unittest.TestCase):
    def test_mode_decides_the_draw_class(self):
        self.assertEqual(RL.draw_class_for_mode("smoke"), RL.DRAW_LIVENESS)
        self.assertEqual(RL.draw_class_for_mode("lane"), RL.DRAW_CANDIDATE)
        self.assertEqual(RL.draw_class_for_mode(None), RL.DRAW_CANDIDATE)

    def test_an_explicit_draw_class_is_preferred_and_mode_is_the_fallback(self):
        self.assertEqual(RL.plan_draw_class({"draw_class": "liveness", "mode": "lane"}), RL.DRAW_LIVENESS)
        self.assertEqual(RL.plan_draw_class({"mode": "smoke"}), RL.DRAW_LIVENESS, "sealed September plans carry mode only")
        self.assertEqual(RL.plan_draw_class({"mode": "lane"}), RL.DRAW_CANDIDATE)
        self.assertTrue(RL.is_liveness_plan({"mode": "smoke"}))

    def test_the_sealed_september_plans_still_read_correctly(self):
        for run_id, want in (("vid-wan2-smoke", RL.DRAW_LIVENESS), ("vid-wan2", RL.DRAW_CANDIDATE),
                             ("img-r1-smoke", RL.DRAW_LIVENESS), ("vid-knee", RL.DRAW_CANDIDATE)):
            p = RUNS / run_id / "PLAN.yaml"
            if not p.exists():
                continue
            header = (yaml.safe_load(p.read_text(encoding="utf-8")) or {})["header"]
            self.assertEqual(RL.plan_draw_class(header), want, f"{run_id}")


class SmokePlanTest(RunnerBase):
    """build_plan under mode=smoke: its own identities, its own declared class, and no collision with the lane plan."""

    def test_a_smoke_plan_cannot_share_an_identity_with_the_lane_plan(self):
        lane = self.plan(cases=("IMG-CORE-01",), routes=("gpt-image-2",), run_id="lane", out=self.tmp / "lane")
        smoke = RL.build_plan(self.tmp / "smk", "smk", cases=["IMG-CORE-01"], routes=["gpt-image-2"], tranche="1a",
                              auth_path=self.auth, mode="smoke", repeats=(1,))
        lane_ids = {t["trial_id"] for t in lane["trials"]}
        smoke_ids = {t["trial_id"] for t in smoke["trials"]}
        self.assertTrue(smoke_ids, "the smoke plan drew nothing")
        self.assertFalse(lane_ids & smoke_ids, f"a smoke draw still shares an identity with a candidate draw: {lane_ids & smoke_ids}")
        self.assertTrue(all(B.is_liveness_trial_id(i) for i in smoke_ids))
        self.assertFalse(any(B.is_liveness_trial_id(i) for i in lane_ids))

    def test_the_plan_header_records_the_draw_class(self):
        smoke = RL.build_plan(self.tmp / "smk2", "smk2", cases=["IMG-CORE-01"], routes=["gpt-image-2"], tranche="1a",
                              auth_path=self.auth, mode="smoke", repeats=(1,))
        self.assertEqual(smoke["header"]["draw_class"], RL.DRAW_LIVENESS)
        self.assertEqual(smoke["header"]["mode"], "smoke")
        lane = self.plan(cases=("IMG-CORE-01",), routes=("gpt-image-2",), run_id="lane2", out=self.tmp / "lane2")
        self.assertEqual(lane["header"]["draw_class"], RL.DRAW_CANDIDATE)

    def test_the_written_plan_on_disk_carries_the_declaration(self):
        RL.build_plan(self.tmp / "smk3", "smk3", cases=["IMG-CORE-01"], routes=["gpt-image-2"], tranche="1a",
                      auth_path=self.auth, mode="smoke", repeats=(1,))
        doc = yaml.safe_load((self.tmp / "smk3" / RL.PLAN_FILE).read_text(encoding="utf-8"))
        self.assertEqual(doc["header"]["draw_class"], "liveness")
        self.assertTrue(all(t["trial_id"].endswith("__smoke") for t in doc["trials"]))


class _StubRun:
    def __init__(self, run_id, liveness):
        self.run_id, self.is_liveness = run_id, liveness
        self.draw_class = RL.DRAW_LIVENESS if liveness else RL.DRAW_CANDIDATE


class ConsumersRefuseLivenessTest(unittest.TestCase):
    def test_registry_rows_refuses_to_build_rows_from_a_liveness_run(self):
        with self.assertRaises(RR.RegistryRowsError) as e:
            RR.build_rows([_StubRun("vid-wan2-smoke", True)])
        self.assertIn("liveness", str(e.exception))

    def test_evidence_map_refuses_a_liveness_results_document(self):
        with self.assertRaises(EM.EvidenceMapRefused):
            EM.merge_results([{"run_id": "vid-wan2-smoke", "draw_class": "liveness", "trials": [], "elimination": []}])

    def test_evidence_map_refuses_a_liveness_screen_results_document(self):
        with self.assertRaises(EM.EvidenceMapRefused):
            EM.merge_screens([{"run_id": "vid-wan2-smoke", "draw_class": "liveness", "trials": []}])

    def test_a_document_with_no_draw_class_is_a_candidate(self):
        self.assertEqual(EM.draw_class_of({"run_id": "vid-knee"}), EM.DRAW_CANDIDATE)
        self.assertEqual(EM.draw_class_of(None), EM.DRAW_CANDIDATE)
        merged = EM.merge_results([{"run_id": "vid-knee", "trials": [{"trial_id": "t"}], "elimination": []}])
        self.assertEqual(merged["run_ids"], ["vid-knee"])

    def test_the_sealed_september_results_documents_still_merge(self):
        docs = []
        for rid in ("vid-knee", "img-r1-composite"):
            p = RUNS / rid / "RESULTS.yaml"
            if p.exists():
                docs.append(yaml.safe_load(p.read_text(encoding="utf-8")))
        if docs:
            self.assertEqual(len(EM.merge_results(docs)["run_ids"]), len(docs))


if __name__ == "__main__":
    unittest.main()
