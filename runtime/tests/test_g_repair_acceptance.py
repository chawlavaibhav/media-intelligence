"""Lane G, parts D and E: bounded repair (never "try again", never past the allowance) and the
human acceptance state machine (C-8: no autonomous delivery, no automated judge)."""
from __future__ import annotations

import unittest

import test_g_support as G

from runtime.errors import Refusal
from runtime.loop import acceptance, refusals, repair
from runtime.loop.refusals import RepairAllowanceExhausted

LETTERING = {"gate": "post_draw", "verdict": "FAIL", "blocking_failures": ["LIMIT-TEXT"],
             "rows": [{"check_id": "LIMIT-TEXT", "family": "limit", "status": "FAIL", "blocking": True,
                       "detail": "text detected ('40% 40%') per scripted"}],
             "report_sha256": "ab" * 32, "packs_selected": ["composition_and_attention"]}
ASPECT = dict(LETTERING, blocking_failures=["DISPATCH-ASPECT"],
              rows=[{"check_id": "DISPATCH-ASPECT", "family": "dispatch", "status": "FAIL", "blocking": True,
                     "detail": "artifact 64×80 (ratio 0.8000) is not 1:1"}])


class Repair(unittest.TestCase):
    def setUp(self):
        self.spec = G.load_spec_dict(G.SPEC_OVERLAY)
        self.profile = G.profile("alpha_human_release")   # repair_allowance 1

    def test_lettering_repair(self):
        r = repair.propose(LETTERING, self.spec, self.profile, 1, incremental_cost_usd="0.03")
        self.assertEqual(r["failure_category"], "baked_lettering")
        self.assertEqual(r["attempt_index"], 2)
        self.assertFalse(r["route_changed"])
        self.assertIn("re-draw the plate", r["what_changes"])
        self.assertIn("seed is not held", r["what_changes"])
        self.assertEqual(r["what_stays_invariant"], "acceptance contract, route, exact strings, aspect")
        self.assertEqual(r["incremental_cost_usd"], "0.03")
        self.assertEqual(len(r["repair_id"]), 64)
        self.assertIn("LIMIT-TEXT", r["failure_observed"])
        self.assertEqual(r["source"], "gate")

    def test_dispatch_repair_is_delivered_vs_declared(self):
        r = repair.propose(ASPECT, self.spec, self.profile, 1, incremental_cost_usd="0.03")
        self.assertEqual(r["failure_category"], "delivered_vs_declared")
        self.assertFalse(r["route_changed"])

    def test_human_rejection_quotes_the_failed_lines(self):
        verdict = G.load_json("human-reject.json")
        r = repair.propose(verdict, self.spec, self.profile, 1, incremental_cost_usd="0.03")
        self.assertEqual(r["failure_category"], "human_rejection")
        self.assertIn(verdict["contract_lines_failed"][0], r["what_changes"])
        self.assertEqual(r["source"], "human")

    def test_rejection_without_failed_lines_is_not_a_repair(self):
        verdict = dict(G.load_json("human-reject.json"), contract_lines_failed=[])
        with self.assertRaises(Refusal) as cm:
            repair.propose(verdict, self.spec, self.profile, 1, incremental_cost_usd="0.03")
        self.assertEqual(cm.exception.code, refusals.REPAIR_NOT_A_REPAIR)

    def test_fallback_trigger_changes_route(self):
        r = repair.propose(LETTERING, self.spec, self.profile, 1, incremental_cost_usd="0.05",
                           fallback_triggers=[{"condition": "LIMIT-TEXT"}], fallback_route="nano-banana-2")
        self.assertTrue(r["route_changed"])
        self.assertIn("nano-banana-2", r["what_changes"])
        self.assertNotIn("route", r["what_stays_invariant"].split(", "))

    def test_allowance_exhausted_on_the_second_repair(self):
        repair.propose(LETTERING, self.spec, self.profile, 1, incremental_cost_usd="0.03")
        with self.assertRaises(RepairAllowanceExhausted) as cm:
            repair.propose(LETTERING, self.spec, self.profile, 2, incremental_cost_usd="0.03")
        self.assertIsInstance(cm.exception, Refusal)
        self.assertEqual(cm.exception.code, refusals.REPAIR_ALLOWANCE_EXHAUSTED)
        self.assertEqual(cm.exception.context["repairs_proposed"], 1)
        self.assertEqual(cm.exception.context["repair_allowance"], 1)

    def test_allowance_is_read_from_the_profile_row(self):
        wider = G.profile("alpha_wider_example")   # repair_allowance 2
        r = repair.propose(LETTERING, self.spec, wider, 2, incremental_cost_usd="0.03")
        self.assertEqual(r["attempt_index"], 3)
        with self.assertRaises(RepairAllowanceExhausted):
            repair.propose(LETTERING, self.spec, wider, 3, incremental_cost_usd="0.03")

    def test_passing_outcome_is_not_a_failure(self):
        with self.assertRaises(Refusal) as cm:
            repair.propose(dict(LETTERING, verdict="PASS", blocking_failures=[]), self.spec, self.profile, 1,
                           incremental_cost_usd="0.03")
        self.assertEqual(cm.exception.code, refusals.REPAIR_NOT_A_REPAIR)

    def test_unrecognised_check_id_is_refused_not_retried(self):
        odd = dict(LETTERING, blocking_failures=["CA-D2-check"])
        with self.assertRaises(Refusal) as cm:
            repair.propose(odd, self.spec, self.profile, 1, incremental_cost_usd="0.03")
        self.assertEqual(cm.exception.code, refusals.REPAIR_FAILURE_UNRECOGNISED)

    def test_cost_is_never_computed_here(self):
        with self.assertRaises(TypeError):
            repair.propose(LETTERING, self.spec, self.profile, 1)   # incremental_cost_usd is required


class HumanAcceptance(unittest.TestCase):
    def setUp(self):
        self.profile = G.profile("alpha_human_release")
        self.acc = acceptance.Acceptance(self.profile)

    def test_initial_state(self):
        self.assertEqual(self.acc.state, "pending_human")
        self.assertEqual(self.acc.authority, "human")

    def test_accept_from_fixture(self):
        v = G.load_json("human-accept.json")
        self.acc.record(v["decision"], v["by"], v["note"], v["utc"])
        self.assertEqual(self.acc.state, "accepted")
        ev = self.acc.to_event()
        self.assertEqual(ev["decision"], "accepted")
        self.assertEqual(ev["decided_by"], "controller")
        self.assertEqual(ev["authority"], "human")
        self.assertEqual(len(ev["transcript_sha256"]), 64)
        self.assertEqual(len(self.acc.transcript), 1)
        self.assertEqual(self.acc.transcript[0]["from"], "pending_human")

    def test_reject_from_fixture(self):
        v = G.load_json("human-reject.json")
        self.acc.record(v["decision"], v["by"], v["note"], v["utc"], contract_lines_failed=v["contract_lines_failed"])
        self.assertEqual(self.acc.state, "rejected")
        self.assertEqual(self.acc.to_event()["contract_lines_failed"], v["contract_lines_failed"])

    def test_repair_requested_then_reopened(self):
        v = G.load_json("human-repair-request.json")
        self.acc.record(v["decision"], v["by"], v["note"], v["utc"], contract_lines_failed=v["contract_lines_failed"])
        self.assertEqual(self.acc.state, "repair_requested")
        self.acc.reopen("2026-09-14T12:11:00Z", "repair draw 2 rendered")
        self.assertEqual(self.acc.state, "pending_human")

    def test_automated_judge_refused_as_by(self):
        for by in ("judge:sonnet-4.5", "model:gemini-2.5", "", None, {"name": "x"}):
            with self.assertRaises(Refusal, msg=repr(by)) as cm:
                self.acc.record("accepted", by, "n", "2026-09-14T12:00:00Z")
            self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_AUTOMATED_JUDGE)
        self.assertEqual(self.acc.state, "pending_human")

    def test_unknown_decision_refused_including_delivered(self):
        for decision in ("delivered", "approved", "maybe"):
            with self.assertRaises(Refusal) as cm:
                self.acc.record(decision, "controller", "n", "2026-09-14T12:00:00Z")
            self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_DECISION_UNKNOWN)

    def test_terminal_states_take_no_second_decision(self):
        self.acc.record("accepted", "controller", "n", "2026-09-14T12:00:00Z")
        with self.assertRaises(Refusal) as cm:
            self.acc.record("rejected", "controller", "n", "2026-09-14T12:01:00Z")
        self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_INVALID_TRANSITION)

    def test_release_requires_accepted_and_a_human(self):
        with self.assertRaises(Refusal) as cm:
            self.acc.release("controller", "2026-09-14T12:00:00Z", artifact_sha256="ab" * 32, content_type="image/png")
        self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_INVALID_TRANSITION)
        self.acc.record("accepted", "controller", "n", "2026-09-14T12:00:00Z")
        with self.assertRaises(Refusal) as cm:
            self.acc.release("judge:auto", "2026-09-14T12:01:00Z", artifact_sha256="ab" * 32, content_type="image/png")
        self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_AUTOMATED_JUDGE)
        rec = self.acc.release("controller", "2026-09-14T12:02:00Z", artifact_sha256="ab" * 32, content_type="image/png")
        self.assertEqual(self.acc.state, "delivered")
        self.assertEqual(rec["released_by"], "controller")
        self.assertEqual(rec["delivered_utc"], "2026-09-14T12:02:00Z")
        # a delivered job still reports its acceptance decision as accepted
        self.assertEqual(self.acc.to_event()["decision"], "accepted")

    def test_no_transition_reaches_delivered_without_release(self):
        self.assertNotIn("delivered", {t for targets in acceptance.TRANSITIONS.values() for t in targets})

    def test_profile_with_non_human_authority_cannot_record(self):
        dry = G.profile("dry_permissive")   # acceptance_authority: none (the lane-development row)
        acc = acceptance.Acceptance(dry)
        with self.assertRaises(Refusal) as cm:
            acc.record("accepted", "controller", "n", "2026-09-14T12:00:00Z")
        self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_AUTHORITY_MISMATCH)

    def test_automated_judge_flag_is_read_and_asserted_false(self):
        class Judgey:
            name = "judgey"
            def limit(self, key):
                return {"acceptance_authority": "human", "automated_judge_in_release_path": True,
                        "autonomous_external_delivery": False,
                        "human_approval_required_before_external_delivery": True}[key]
        acc = acceptance.Acceptance(Judgey())
        with self.assertRaises(Refusal) as cm:
            acc.record("accepted", "controller", "n", "2026-09-14T12:00:00Z")
        self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_AUTOMATED_JUDGE)

    def test_autonomous_delivery_flag_true_refuses_release(self):
        class Auto:
            name = "auto"
            def limit(self, key):
                return {"acceptance_authority": "human", "automated_judge_in_release_path": False,
                        "autonomous_external_delivery": True,
                        "human_approval_required_before_external_delivery": False}[key]
        acc = acceptance.Acceptance(Auto())
        acc.record("accepted", "controller", "n", "2026-09-14T12:00:00Z")
        with self.assertRaises(Refusal) as cm:
            acc.release("controller", "2026-09-14T12:01:00Z", artifact_sha256="ab" * 32, content_type="image/png")
        self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_NO_AUTONOMOUS_DELIVERY)

    def test_abandon_records_the_runtime_reason(self):
        self.acc.abandon("2026-09-14T12:00:00Z", "REPAIR_ALLOWANCE_EXHAUSTED: 1 repair proposed, allowance 1")
        self.assertEqual(self.acc.state, "abandoned")
        ev = self.acc.to_event()
        self.assertEqual(ev["decision"], "abandoned")
        self.assertNotIn("decided_by", ev)

    def test_pending_is_not_an_event(self):
        with self.assertRaises(Refusal) as cm:
            self.acc.to_event()
        self.assertEqual(cm.exception.code, refusals.ACCEPTANCE_INVALID_TRANSITION)

    def test_transcript_is_json_with_utc(self):
        import json
        self.acc.record("accepted", "controller", "n", "2026-09-14T12:00:00Z")
        doc = json.loads(self.acc.transcript_json())
        self.assertEqual(doc[0]["utc"], "2026-09-14T12:00:00Z")
        self.assertEqual(doc[0]["to"], "accepted")


if __name__ == "__main__":
    unittest.main()
