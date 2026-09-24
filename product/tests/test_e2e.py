"""Dry end-to-end: the whole product path at USD 0 (simulated providers and reasoning).

What this proves: states, persistence, ledger, graph scheduling, pauses, recovery, gateway, revision and
learning capture work together. What it does NOT prove: media quality, provider behaviour, reasoning quality.

v3 (kitchen v3, 2026-09-25): these tests keep their purpose; their steps follow the v3 line — waiter -> chef -> the
customer approves the recipe -> head cook (cooks, tastes, repairs) -> gatekeeper -> customer, with no wait in between.
Film tests use the backpack order so the recipe has shots on the video model.

Retired in v3:
  - WorldTruthBeforeSpend.test_an_unsourced_product_claim_stops_the_job_before_spend_and_approve_refuses_it — it guarded
    the recipe checker's objections and the founder's override_recipe; both are retired (the customer approves the recipe).
"""
import json
import unittest
from decimal import Decimal

from product.reasoning import ReasoningFailed
from product.tests import fixtures_v2 as fx
from product.tests.support import Env


def film(e, **kw):
    return fx.submit_backpack_film(e, **kw)


class FilmJourney(unittest.TestCase):
    def setUp(self):
        self.e = Env()

    def tearDown(self):
        self.e.close()

    def test_submit_direct_approve_produce_hold_release_revise_accept_download(self):
        e = self.e
        jid = film(e)
        e.to_review(jid)
        self.assertEqual(e.state(jid), "ready_for_review")
        nodes = {n["node_id"]: n for n in e.store.nodes(jid)}
        moving = [k for k, n in nodes.items() if n["kind"] == "shot" and json.loads(n["spec_json"]).get("tool") == "video"]
        self.assertTrue(moving)                                    # the chef's moving moment is made on the video model
        self.assertTrue(all(nodes[k]["draws"] >= 1 for k in moving))
        cut1 = e.orch._final_assets(jid)
        before = {k: n["selected_asset_id"] for k, n in nodes.items()}
        shot = moving[0]
        e.orch.request_changes(jid, e.user["email"], [{"target": shot.replace("_", ":"), "text": "slower slide"}])
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")                  # amendment 1 §3: no founder hold by default
        after = {n["node_id"]: n["selected_asset_id"] for n in e.store.nodes(jid)}
        changed = sorted(k for k in after if after[k] != before[k])
        self.assertIn(shot, changed)
        self.assertIn("film", changed)
        self.assertNotIn(shot.replace("shot_", "frame_"), changed)  # a clip change keeps the approved first frame
        self.assertNotIn("music", changed)
        self.assertNotIn("master", changed)
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
        jid = film(e)
        e.to_review(jid)
        before = {n["node_id"]: n["selected_asset_id"] for n in e.store.nodes(jid)}
        copy_id = e.store.artifact(jid, "recipe")["copy_deck"][0]["id"]
        e.orch.request_changes(jid, e.user["email"], [{"target": f"copy:{copy_id}", "text": 'text to "Pack less. Travel further."'}])
        n_attempts = len([a for a in e.store.attempts(jid) if a["category"] == "provider"])
        e.drain()
        after = {n["node_id"]: n["selected_asset_id"] for n in e.store.nodes(jid)}
        changed = sorted(k for k in after if after[k] != before[k])
        self.assertTrue(set(changed) <= {"end_card", "film"} | {k for k in after if k.startswith("super_")}, changed)
        self.assertEqual(len([a for a in e.store.attempts(jid) if a["category"] == "provider"]), n_attempts)   # no paid redraw
        self.assertIn("Pack less. Travel further.", [c["text"] for c in e.store.artifact(jid, "recipe")["copy_deck"]])
        self.assertEqual(e.orch.exact_strings(jid), ["Pack less. Travel further.", "mokobara.com"])

    def test_concept_change_goes_back_to_direction_for_a_new_quote(self):
        e = self.e
        jid = film(e)
        e.to_review(jid)
        e.orch.request_changes(jid, e.user["email"], [{"target": None, "text": "we want a different concept entirely — start over"}])
        self.assertEqual(e.front(jid), "awaiting_approval")                 # the chef writes a new recipe and a new quote
        self.assertEqual(len(e.store.artifact_versions(jid, "recipe")), 2)
        self.assertEqual(len(e.store.artifact_versions(jid, "quote")), 2)


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
            self.assertEqual(e.front(jid), "awaiting_approval")
            self.assertEqual(e.store.artifact(jid, "understanding")["audience"], "Kanpur families buying for Diwali")
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
            self.assertIn("talking heads", e.store.artifact(jid, "understanding")["refusal_reason"])   # v3: a voice-over alone is allowed
        finally:
            e.close()


class BudgetExhaustion(unittest.TestCase):
    def test_a_low_budget_pauses_without_crossing_the_cap_and_a_raise_resumes_to_completion(self):
        e = Env()
        try:
            jid = film(e)
            e.front(jid)
            e.orch.approve(jid, by=e.user["email"], budget_usd="0.60")
            e.produce(jid)
            j = e.store.job(jid)
            self.assertEqual(j["state"], "paused_budget")
            self.assertEqual(j["resume_state"], "producing")
            self.assertLessEqual(e.store.committed_usd(jid), Decimal("0.60"))
            self.assertIn("more", j["pause_reason"])
            e.svc.raise_budget(e.user, jid, "15")
            self.assertEqual(e.produce(jid), "ready_for_review")
            self.assertLessEqual(e.store.committed_usd(jid), Decimal("15"))
        finally:
            e.close()


class ProviderFailureInjection(unittest.TestCase):
    def test_injected_503s_are_counted_attempts_and_the_job_continues_without_a_person(self):
        e = Env(fault_injection={"video": [503]})
        try:
            jid = film(e)
            e.front(jid)
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            self.assertEqual(e.produce(jid), "ready_for_review")
            failed = [a for a in e.store.attempts(jid) if a["status"] == "failed"]
            self.assertEqual([(a["route"], a["failure_class"]) for a in failed], [("veo-3.1-fast-i2v", "infrastructure_transient")])
        finally:
            e.close()

    def test_a_persistent_outage_pauses_the_job_as_provider_paused_then_it_resumes(self):
        e = Env(fault_injection={"music": [503, 503, 503]})
        try:
            jid = film(e)
            e.front(jid)
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            for _ in range(10):          # planning, then producing until the music fails 3x
                e.worker.run_once()
                if e.state(jid) not in ("planning", "producing"):
                    break
            self.assertEqual(e.state(jid), "paused_provider")
            self.assertEqual(e.produce(jid), "ready_for_review")   # retry window 0 s in tests; the fault queue is empty now
        finally:
            e.close()


class WorkerCrash(unittest.TestCase):
    def test_a_worker_killed_mid_production_resumes_with_no_duplicate_ids_and_nothing_resent(self):
        e = Env(fault_injection={"video_poll": ["crash"]})
        try:
            jid = film(e)
            e.front(jid)
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            with self.assertRaises(KeyboardInterrupt):
                for _ in range(10):      # planning, then producing: it dies while polling a paid clip
                    e.worker.run_once()
            self.assertEqual(e.state(jid), "producing")
            held = [a for a in e.store.attempts(jid) if a["status"] == "reserved"]
            self.assertTrue(held)
            from product.worker import Worker
            w2 = Worker(e.s, e.store, e.orch)
            w2.drain()
            while e.state(jid) == "awaiting_taste":                 # the customer tastes the hardest shot
                e.orch.approve_taste(jid, by=e.user["email"])
                w2.drain()
            self.assertEqual(e.state(jid), "ready_for_review", e.store.job(jid)["pause_reason"])
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




V3_NOT_REQUIRED = {"AD_STRUCTURE_MINIMUM"}


class EveryApplicableControlRunsOnTheProductionPath(unittest.TestCase):
    """Controller review of PR #108, concern 2: a control mapped in YAML is not a control unless the real production
    path writes its result onto the delivered file."""

    def test_image_and_film_jobs_record_every_applicable_control_on_their_deliverables(self):
        import json
        from product import verify
        e = Env()
        try:
            for kind in ("image", "video"):
                jid = e.submit(kind) if kind == "image" else film(e)
                e.front(jid)
                e.orch.approve(jid, by=e.user["email"], budget_usd="15")
                e.produce(jid)
                applies = ("any", kind, "text") + (("audio",) if kind == "video" else ())
                # kitchen v3 no longer requires AD_STRUCTURE_MINIMUM (verify.required_checks: the gatekeeper checks the
                # dish against the order; a film ordered without a logo failed it on 2026-09-24)
                want = {c["id"] for c in verify.controls().values()
                        if c["status"] in ("enforced", "reviewer_obligation") and c["applies"].split()[0] in applies} - V3_NOT_REQUIRED
                for aid in e.orch._final_assets(jid):
                    seen = set()
                    for r in e.store.checks(aid):
                        c = r["control_ids"]
                        seen.update(json.loads(c) if c.startswith("[") else [c])
                    self.assertEqual(sorted(want - seen), [], f"{kind} {aid}")
        finally:
            e.close()



class TheTasterRejectsEverything(unittest.TestCase):
    """Live 2026-09-23: an unqualified inspector rejected four draws, three of them faithful, and the job failed; v1 then
    let 'a person' (in practice the builder) pick takes. Kitchen v3: the head cook tastes; when its takes are used up the
    best take is kept, flagged and noted on the customer's preview — nobody waits for the founder."""

    def test_all_attempts_rejected_keeps_the_best_take_flagged_and_the_customer_is_told(self):
        e = Env()
        try:
            orig = e.orch.sim.head_cook__ingredient_check

            def taster(b, media, **kw):
                out = orig(b, media, **kw)
                out.update(usable=False, notes="the flap sticks out horizontally")
                return out
            e.orch.sim.head_cook__ingredient_check = taster
            jid = e.submit("image")
            e.front(jid)
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            e.drain()
            self.assertEqual(e.state(jid), "ready_for_review")
            flagged = [n for n in e.store.nodes(jid) if json.loads(n["spec_json"]).get("flagged")]
            self.assertTrue(flagged)
            self.assertFalse([n for n in e.store.nodes(jid) if n["status"] == "needs_founder"])
            for n in flagged:
                self.assertLessEqual(len([a for a in e.store.attempts(jid) if a["category"] == "provider" and a["node_id"] == n["node_id"]]),
                                     n["max_draws"])                             # never a third identical request
            self.assertIn("flap sticks out", " ".join(e.store.artifact(jid, "customer_notes")["notes"]))
            self.assertTrue(e.store.events(jid, ("take_kept_flagged",)))
            self.assertFalse([x for x in e.store.events(jid, ("state",)) if json.loads(x["data_json"]).get("to") == "paused_for_founder"])
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
