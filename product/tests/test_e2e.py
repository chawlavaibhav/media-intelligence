"""Dry end-to-end: the whole product path at USD 0 (simulated providers and reasoning).

What this proves: states, persistence, ledger, graph scheduling, pauses, recovery, gateway, revision and
learning capture work together. What it does NOT prove: media quality, provider behaviour, reasoning quality.
"""
import json
import unittest
from decimal import Decimal

from product.reasoning import ReasoningFailed
from product.tests.support import Env


class FilmJourney(unittest.TestCase):
    def setUp(self):
        self.e = Env()

    def tearDown(self):
        self.e.close()

    def test_submit_direct_approve_produce_hold_release_revise_accept_download(self):
        e = self.e
        jid = e.submit("video")
        e.to_review(jid)
        self.assertEqual(e.state(jid), "ready_for_review")
        nodes = {n["node_id"]: n for n in e.store.nodes(jid)}
        self.assertTrue(nodes["clip_b1"]["draws"] >= 1)
        # the riskiest beat's clip is a dependency of every other clip (qualification first)
        risky = [k for k, n in nodes.items() if n["kind"] == "clip" and json.loads(n["spec_json"]).get("qualify")]
        self.assertEqual(len(risky), 1)
        for k, n in nodes.items():
            if n["kind"] == "clip" and k != risky[0]:
                self.assertIn(risky[0], json.loads(n["deps_json"]))
        cut1 = e.orch._final_assets(jid)
        before = {k: n["selected_asset_id"] for k, n in nodes.items()}
        e.orch.request_changes(jid, e.user["email"], [{"target": "beat:2", "text": "slower reveal"}])
        e.drain()
        self.assertEqual(e.state(jid), "operator_hold")
        after = {n["node_id"]: n["selected_asset_id"] for n in e.store.nodes(jid)}
        changed = sorted(k for k in after if after[k] != before[k])
        self.assertIn("clip_b2", changed)
        self.assertIn("film", changed)
        self.assertNotIn("clip_b1", changed)
        self.assertNotIn("still_b2", changed)                      # a clip change keeps the approved first frame
        self.assertNotIn("music", changed)
        e.waive_all(jid)
        e.orch.release_hold(jid, "operator:test")
        e.orch.accept(jid, e.user["email"])
        self.assertEqual(e.state(jid), "accepted")
        d = e.store.deliveries(jid)
        self.assertEqual(len(d), 1)
        self.assertNotEqual(d[0]["asset_id"], cut1[0])
        self.assertEqual(d[0]["asset_sha256"], e.store.asset(d[0]["asset_id"])["sha256"])
        led = e.store.ledger_summary(jid)
        self.assertLessEqual(Decimal(led["committed_usd"]), Decimal(e.store.job(jid)["budget_usd"]))
        self.assertEqual(led["uncertain"], 0)

    def test_copy_change_rerenders_only_text_bearing_nodes(self):
        e = self.e
        jid = e.submit("video")
        e.to_review(jid)
        before = {n["node_id"]: n["selected_asset_id"] for n in e.store.nodes(jid)}
        copy_id = e.store.artifact(jid, "direction")["copy_deck"][0]["id"]
        e.orch.request_changes(jid, e.user["email"], [{"target": f"copy:{copy_id}", "text": 'text to "Pack less. Travel further."'}])
        n_attempts = len([a for a in e.store.attempts(jid) if a["category"] == "provider"])
        e.drain()
        after = {n["node_id"]: n["selected_asset_id"] for n in e.store.nodes(jid)}
        changed = sorted(k for k in after if after[k] != before[k])
        self.assertTrue(set(changed) <= {"end_card", "film"} | {k for k in after if k.startswith("super_")}, changed)
        self.assertEqual(len([a for a in e.store.attempts(jid) if a["category"] == "provider"]), n_attempts)   # no paid redraw
        self.assertIn("Pack less. Travel further.", [c["text"] for c in e.store.artifact(jid, "direction")["copy_deck"]])
        self.assertEqual(e.orch.exact_strings(jid), ["Pack less. Travel further."])

    def test_concept_change_goes_back_to_direction_for_a_new_quote(self):
        e = self.e
        jid = e.submit("video")
        e.to_review(jid)
        e.orch.request_changes(jid, e.user["email"], [{"target": None, "text": "we want a different concept entirely — start over"}])
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")
        self.assertEqual(len(e.store.artifact_versions(jid, "direction")), 2)


class ImageJourney(unittest.TestCase):
    def test_two_formats_each_get_their_own_plate_and_composition(self):
        e = Env()
        try:
            jid = e.submit("image", formats=["1:1", "4:5"])
            e.to_review(jid)
            kinds = sorted((n["kind"], json.loads(n["spec_json"])["aspect"]) for n in e.store.nodes(jid))
            self.assertEqual(kinds, [("compose_still", "1:1"), ("compose_still", "4:5"), ("plate", "1:1"), ("plate", "4:5")])
            e.orch.accept(jid, e.user["email"])
            self.assertEqual(len(e.store.deliveries(jid)), 2)
        finally:
            e.close()


class Clarification(unittest.TestCase):
    def test_a_one_line_idea_pauses_for_questions_before_any_spend_and_answers_resume_it(self):
        e = Env()
        try:
            jid = e.submit("image", text="Poster for our oil tin.")
            e.drain()
            self.assertEqual(e.state(jid), "needs_answers")
            self.assertEqual([a for a in e.store.attempts(jid) if a["category"] == "provider"], [])
            e.orch.answer(jid, {"Q1": "Kanpur families buying for Diwali"}, e.user["email"])
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_approval")
            self.assertEqual(e.store.artifact(jid, "intent")["audience"], "Kanpur families buying for Diwali")
        finally:
            e.close()


class Refusal(unittest.TestCase):
    def test_a_talking_head_voice_over_brief_is_refused_at_intake_with_zero_production_spend(self):
        e = Env()
        try:
            jid = e.submit("video", text="A talking head explainer with a voice-over narrating our app features for 20 seconds.")
            e.drain()
            self.assertEqual(e.state(jid), "refused")
            self.assertEqual([a for a in e.store.attempts(jid) if a["category"] == "provider"], [])
            self.assertIn("voice-over", e.store.artifact(jid, "intent")["refusal_reason"])
        finally:
            e.close()


class BudgetExhaustion(unittest.TestCase):
    def test_a_low_budget_pauses_without_crossing_the_cap_and_a_raise_resumes_to_completion(self):
        e = Env()
        try:
            jid = e.submit("video")
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="1.20")
            e.drain()
            j = e.store.job(jid)
            self.assertEqual(j["state"], "paused_budget")
            self.assertEqual(j["resume_state"], "producing")
            self.assertLessEqual(e.store.committed_usd(jid), Decimal("1.20"))
            self.assertIn("more", j["pause_reason"])
            e.svc.raise_budget(e.user, jid, "15")
            e.drain()
            self.assertEqual(e.state(jid), "operator_hold")
            self.assertLessEqual(e.store.committed_usd(jid), Decimal("15"))
        finally:
            e.close()


class ProviderFailureInjection(unittest.TestCase):
    def test_injected_503s_are_counted_attempts_and_the_job_continues_without_a_person(self):
        e = Env(fault_injection={"video": [503]})
        try:
            jid = e.submit("video")
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            e.drain()
            self.assertEqual(e.state(jid), "operator_hold")
            failed = [a for a in e.store.attempts(jid) if a["status"] == "failed"]
            self.assertEqual([(a["route"], a["failure_class"]) for a in failed], [("veo-3.1-fast-i2v", "infrastructure_transient")])
        finally:
            e.close()

    def test_a_persistent_outage_pauses_the_job_as_provider_paused_then_it_resumes(self):
        e = Env(fault_injection={"music": [503, 503, 503]})
        try:
            jid = e.submit("video")
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            e.worker.run_once()          # planning
            e.worker.run_once()          # producing → music fails 3x
            self.assertEqual(e.state(jid), "paused_provider")
            e.drain()                    # retry window 0 s in tests; the fault queue is empty now
            self.assertEqual(e.state(jid), "operator_hold")
        finally:
            e.close()


class WorkerCrash(unittest.TestCase):
    def test_a_worker_killed_mid_production_resumes_with_no_duplicate_ids_and_nothing_resent(self):
        e = Env(fault_injection={"video_poll": ["crash"]})
        try:
            jid = e.submit("video")
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            e.worker.run_once()          # planning
            with self.assertRaises(KeyboardInterrupt):
                e.worker.run_once()      # dies while polling a paid clip
            self.assertEqual(e.state(jid), "producing")
            held = [a for a in e.store.attempts(jid) if a["status"] == "reserved"]
            self.assertTrue(held)
            from product.worker import Worker
            w2 = Worker(e.s, e.store, e.orch)
            w2.drain()
            self.assertEqual(e.state(jid), "operator_hold")
            rows = e.store.attempts(jid)
            self.assertEqual(len({r["id"] for r in rows}), len(rows))
            self.assertEqual([r for r in rows if r["status"] == "reserved"], [])
            recovered = e.store.events(jid, ("recovered_in_flight",))
            self.assertTrue(recovered)
            used = e.store.events(jid, ("recovered_take_used",))
            self.assertTrue(used, "the clip paid for before the crash must be used, not re-bought")
        finally:
            e.close()


class Isolation(unittest.TestCase):
    def test_reviewer_roles_refuse_producer_context_by_construction(self):
        e = Env()
        try:
            jid = e.submit()
            with self.assertRaises(ReasoningFailed):
                e.orch.llm.call(jid, "reviewer", {"BRIEF": "x", "PRODUCER_NOTES": "the director thinks beat 3 is great"})
            with self.assertRaises(ReasoningFailed):
                e.orch.llm.call(jid, "inspector", {"INSTRUCTION": "x"}, knowledge="packs")
        finally:
            e.close()


class Learning(unittest.TestCase):
    def test_an_accepted_job_writes_a_case_that_passes_check_case(self):
        import subprocess
        import sys
        from product.config import REPO
        e = Env()
        try:
            jid = e.submit("image")
            e.to_review(jid)
            e.orch.accept(jid, e.user["email"])
            case = e.dir / "cases" / jid
            r = subprocess.run([sys.executable, str(REPO / "production-learning/tools/check_case.py"), "--case", str(case)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            from product import learning
            m = learning.metrics(e.store, jid)
            self.assertIsNotNone(m["first_cut_latency_s"])
            self.assertLessEqual(m["active_elapsed_s"], m["active_accumulated_s"] + 1e-6)
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
