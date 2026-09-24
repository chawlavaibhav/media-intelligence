"""P1 v2 amendment 1 (coordination/p1-v2/P1-V2-AMENDMENT-1.md, founder decisions 2026-09-23). USD 0, simulated.

§1 image cost target + image chef · §2 judges tested on old jobs · §3 nobody waits for the founder · §4 learning automated ·
§6 founder account note in the runbook."""
import json
import os
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

import yaml

from product import cost, flow, rulebook
from product.config import REPO
from product.qualification import judges
from product.store import utc_now
from product.tests import fixtures_v2 as fx
from product.tests.support import Env

IMAGE_ORDER = "A calm launch poster for our navy travel backpack; the bag must be the first thing you see; no people."
FOUNDER_WAITS = ("paused_for_founder", "operator_hold")


def states_of(e, jid):
    return [json.loads(x["data_json"]).get("to") for x in e.store.events(jid, ("state",))]


def no_founder_wait(test, e, jid):
    test.assertFalse([s for s in states_of(e, jid) if s in FOUNDER_WAITS], states_of(e, jid))


def accept_alternatives(e, jid):
    e.drain()
    if e.state(jid) == "awaiting_customer_input":
        f = e.store.artifact(jid, "feasibility")
        e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=[
            {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
        e.drain()


# ── §1 cost ────────────────────────────────────────────────────────────────────────────────────────────────────────────
class ImageCost(unittest.TestCase):
    def test_image_jobs_use_the_image_chef_and_films_the_strongest_both_configurable_and_independent_of_the_judges(self):
        e = Env()
        try:
            img = e.submit("image", text=IMAGE_ORDER)
            e.drain()
            film = fx.submit_backpack_film(e)
            accept_alternatives(e, film)
            self.assertEqual(e.store.artifact(img, "recipe")["written_by"]["model"], "azure_openai:gpt-5.6-terra")
            self.assertEqual(e.store.artifact(film, "recipe")["written_by"]["model"], "azure_openai:gpt-5.6-sol")
            est = {j: sum(Decimal(c["est_cost_usd"]) for c in e.store.llm_calls(j) if c["worker"] == "chef") for j in (img, film)}
            self.assertLess(est[img], est[film])                          # priced at the cheaper chef's list price
            from product import config
            self.assertEqual(config.worker_models()["chef_image"], "azure_openai:gpt-5.6-terra")
            os.environ["MI_MODEL_CHEF_IMAGE"] = "gemini:gemini-3.1-pro-preview"
            try:
                with self.assertRaises(ValueError):                    # same company as the judges: refused
                    config.check_independence(config.worker_models())
            finally:
                os.environ.pop("MI_MODEL_CHEF_IMAGE")
        finally:
            e.close()

    def test_the_report_shows_both_targets_and_the_quote_shares_reasoning_across_the_image_set(self):
        e = Env()
        try:
            jid = e.submit("image", text=IMAGE_ORDER, formats=["1:1", "4:5", "9:16"])
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_approval")
            r = cost.reasoning_report(e.orch, jid, e.store.artifact(jid, "recipe"), stage="quote")
            self.assertEqual(r["targets"], {"film": "0.30", "image": "0.08"})
            self.assertEqual(r["images_in_set"], 3)
            self.assertEqual(Decimal(r["per_image_usd"]), (Decimal(r["estimated_total_usd"]) / 3).quantize(Decimal("0.0001")))
            self.assertEqual(r["within_budget"], Decimal(r["per_image_usd"]) <= Decimal("0.08"))
            q = e.store.artifact(jid, "quote")
            self.assertEqual(q["images_in_set"], 3)
            self.assertIn("reasoning_per_image_usd", q)
        finally:
            e.close()


# ── §2 judges on old jobs ──────────────────────────────────────────────────────────────────────────────────────────────
class JudgesOnOldJobs(unittest.TestCase):
    def test_the_big_taster_set_holds_the_14_films_and_62_images_with_the_verdict_mapping_and_pass_marks_are_confirmed(self):
        cases = yaml.safe_load((REPO / "product/qualification/JUDGE-CASES.yaml").read_text())
        hist = [c for c in cases["big_taster"] if c["id"].startswith("BT-H-")]
        self.assertEqual(len([c for c in hist if c["media"] == "film"]), 14)
        self.assertEqual(len([c for c in hist if c["media"] == "image"]), 62)
        mapping = {"accept": "pass", "specific_repair": "fix", "rebuild_direction": "fail", "reject": "fail"}
        for c in hist:
            self.assertEqual(c["known_judge_verdict"], mapping[c["founder_verdict"]])
            self.assertEqual(len(c["evidence"]["sha256"]), 64)
        rc = {c["id"] for c in cases["recipe_checker"]}
        self.assertTrue({"RC-H-MOKOBARA-ODYSSEY-007", "RC-H-RENTOK-GAME-A-004", "RC-H-RENTOK-GAME-B-005", "RC-H-RENTOK-GAME-V2-006",
                         "RC-H-UPWORK-INTRO-001", "RC-H-CUMINCO-CHOPSTICKS-003"} <= rc)
        self.assertTrue(cases["recipe_checker_missing"])                     # jobs whose plan is not on a job branch are listed
        marks = yaml.safe_load((REPO / "product/qualification/PASS-MARKS.yaml").read_text())
        self.assertEqual(str(marks["confirmed_by_founder"]), "2026-09-23")

    @unittest.skipUnless(fx.evidence_dir() and (fx.evidence_dir() / "historical/CASES.yaml").exists(), "historical cases not on this host")
    def test_the_harness_scores_accepted_and_not_accepted_separately_verifies_hashes_and_still_never_qualifies_simulated(self):
        rep = judges.run(judges=("big_taster", "recipe_checker"))
        bt = rep["judges"]["big_taster"]
        self.assertGreaterEqual(bt["available"], 79)
        for key in ("agreement_accepted", "agreement_not_accepted", "agreement_balanced"):
            self.assertIn(key, bt)
        self.assertFalse(bt["qualified"])
        self.assertIn("simulated", bt["why_not_qualified"])
        self.assertIn("agreement_balanced", rep["judges"]["recipe_checker"])
        self.assertEqual(rep["spent_usd"], "0.000000")

    def test_a_file_whose_hash_does_not_match_is_unavailable_never_judged(self):
        with mock.patch.object(judges, "sha256_file", return_value="0" * 64):
            ev = judges.Evidence(fx.evidence_dir())
            if ev.root and (ev.root / "historical/CASES.yaml").exists():
                c = next(c for c in yaml.safe_load((REPO / "product/qualification/JUDGE-CASES.yaml").read_text())["big_taster"]
                         if c["id"].startswith("BT-H-"))
                self.assertIsNone(ev.historical(c["evidence"]))


# ── §3 nobody waits for the founder ────────────────────────────────────────────────────────────────────────────────────
class NobodyWaitsForTheFounder(unittest.TestCase):
    def setUp(self):
        self.e = Env()

    def tearDown(self):
        self.e.close()

    def test_an_unqualified_recipe_checkers_approve_goes_straight_to_the_customer_as_our_reviewer_found_no_problems(self):
        e = self.e
        jid = e.submit("image", text=IMAGE_ORDER)
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")
        self.assertIn("found no problems", e.store.artifact(jid, "plan_note")["text"])
        e.orch.approve(jid, by=e.user["email"], budget_usd="10")
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")                  # the customer's preview is the final check
        no_founder_wait(self, e, jid)
        e.orch.accept(jid, e.user["email"])
        rows = {r["check_id"]: r for a in e.orch.final_assets(jid) for r in e.store.checks(a)}
        self.assertTrue(rows["independent_review"]["runner"].startswith("customer:"))
        self.assertEqual(e.state(jid), "accepted")

    def test_after_two_send_backs_the_system_replans_with_safe_alternatives_and_the_customer_decides_if_it_still_fails(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.orch.sim.chef__recipe = lambda b, media: fx.v1_recipe(e.store.artifact(jid, "understanding"), e.store.artifact(jid, "feasibility"))
        accept_alternatives(e, jid)
        self.assertEqual(e.state(jid), "awaiting_approval")                  # the system's safe re-plan passed the checker
        self.assertEqual(flow.rounds_used(e.store, jid, "SB-RECIPE"), 2)
        rep = e.store.artifact(jid, "system_replan")
        self.assertTrue(rep["shots"])
        self.assertEqual(e.store.artifact(jid, "recipe_check")["verdict_after_code"], "approve")
        r = e.store.artifact(jid, "recipe")
        for s in r["shots"]:
            if "zip" in s["action"].lower() or s["n"] in [x["shot"] for x in rep["shots"]]:
                self.assertEqual(s["route"], "FILM-A")
        self.assertNotIn("objections", json.dumps(e.store.artifact(jid, "plan_note")).lower().replace('"objections": false', ""))
        no_founder_wait(self, e, jid)
        # if the checker still objects, the customer sees the objections and chooses: go ahead, change the brief, or stop
        e2 = Env()
        try:
            jid2 = fx.submit_backpack_film(e2)
            orig = e2.orch.sim.recipe_checker__recipe_check
            e2.orch.sim.recipe_checker__recipe_check = lambda b, m: {**orig(b, m), "verdict": "send_back",
                                                                      "issues": [{"severity": "major", "where": "shot 2", "issue": "the idea is flat",
                                                                                  "fix": "find a surprise"}]}
            accept_alternatives(e2, jid2)
            self.assertEqual(e2.state(jid2), "awaiting_approval")
            self.assertEqual([x["shot"] for x in e2.store.artifact(jid2, "system_replan")["shots"]], [2])
            obj = e2.store.artifact(jid2, "plan_objections")
            self.assertIn("the idea is flat", " ".join(obj["plain_words"]))
            self.assertEqual([a for a in e2.store.attempts(jid2) if a["category"] == "provider"], [])      # USD 0 so far
            with self.assertRaises(PermissionError):
                e2.orch.approve(jid2, by=e2.user["email"], budget_usd="15")                 # must acknowledge the objections
            e2.orch.approve(jid2, by=e2.user["email"], budget_usd="15", accept_objections=True)
            self.assertEqual(e2.state(jid2), "planning")
            self.assertTrue(e2.store.events(jid2, ("customer_accepted_objections",)))
            no_founder_wait(self, e2, jid2)
        finally:
            e2.close()

    def test_a_risky_shot_that_fails_after_its_replan_becomes_a_still_with_code_motion_and_the_preview_says_so(self):
        e = self.e
        orig = e.orch.sim.small_taster__ingredient_check

        def taster(b, media, **kw):
            out = orig(b, media, **kw)
            if kw.get("node_id") in ("frame_2", "shot_2"):
                out.update(usable=False, notes="the laptop passes through the bag wall")
            return out
        e.orch.sim.small_taster__ingredient_check = taster
        jid = fx.submit_backpack_film(e)
        accept_alternatives(e, jid)
        e.orch.approve(jid, by=e.user["email"], budget_usd="15")
        e.produce(jid)
        self.assertEqual(e.state(jid), "ready_for_review")
        self.assertEqual(e.store.artifact(jid, "recipe")["shots"][1]["route"], "FILM-A")
        notes = " ".join(e.store.artifact(jid, "customer_notes")["notes"])
        self.assertIn("shot 2", notes)
        no_founder_wait(self, e, jid)

    def test_big_taster_fix_repairs_automatically_within_the_approved_budget_and_never_spends_beyond_it(self):
        e = self.e
        orig = e.orch.sim.big_taster__final_review

        def big(b, media, **kw):
            out = orig(b, media, **kw)
            out.update(verdict="fix", defects=[{"id": "D1", "where": "shot 2", "severity": "major", "description": "the laptop morphs",
                                                "earliest_stage": "generation", "shot": 2, "repair": "redraw the slide"}])
            return out
        e.orch.sim.big_taster__final_review = big
        spent_at_first_look = []
        orig_big = big

        def big(b, media, **kw):
            spent_at_first_look.append(e.store.committed_usd(jid))
            return orig_big(b, media, **kw)
        e.orch.sim.big_taster__final_review = big
        jid = fx.submit_backpack_film(e)
        accept_alternatives(e, jid)
        e.orch.approve(jid, by=e.user["email"], budget_usd="15")
        e.produce(jid)
        self.assertEqual(len(e.store.artifact_versions(jid, "internal_repair")), 2)       # 2 automatic rounds, named shots only
        for v in e.store.artifact_versions(jid, "internal_repair"):
            rep = e.store.artifact(jid, "internal_repair", v["version"])
            self.assertNotIn("master", rep["nodes"])
            self.assertNotIn("shot_1", rep["nodes"])
        self.assertEqual(e.state(jid), "ready_for_review")                                # repairs used up: the customer decides
        self.assertLessEqual(e.store.committed_usd(jid), Decimal("15"))
        self.assertGreater(spent_at_first_look[1], spent_at_first_look[0])            # the repair did buy new takes
        no_founder_wait(self, e, jid)
        # the same job with a budget that only just covers the first cut: the repair stops at the cap and asks the customer
        e2 = Env()
        try:
            e2.orch.sim.big_taster__final_review = orig_big
            jid2 = fx.submit_backpack_film(e2)
            accept_alternatives(e2, jid2)
            cap = spent_at_first_look[0] + Decimal("0.01")
            e2.orch.approve(jid2, by=e2.user["email"], budget_usd=str(cap))
            e2.produce(jid2)
            self.assertEqual(e2.state(jid2), "paused_budget")                        # the customer decides; nothing over the cap
            self.assertLessEqual(e2.store.committed_usd(jid2), cap)
            self.assertEqual(len(e2.store.artifact_versions(jid2, "internal_repair")), 1)
            no_founder_wait(self, e2, jid2)
        finally:
            e2.close()

    def test_a_big_taster_fail_after_its_round_goes_to_the_customer_who_may_accept_as_is(self):
        e = self.e
        orig = e.orch.sim.big_taster__final_review

        def big(b, media, **kw):
            out = orig(b, media, **kw)
            out.update(verdict="fail", defects=[{"id": "D2", "where": "whole", "severity": "blocker", "description": "the story is flat",
                                                 "earliest_stage": "plan", "shot": None, "repair": "re-plan"}])
            return out
        e.orch.sim.big_taster__final_review = big
        jid = e.submit("image", text=IMAGE_ORDER)
        e.drain()
        e.orch.approve(jid, by=e.user["email"], budget_usd="10")
        e.drain()                                                                  # fail #1 → the chef → a new plan for the customer
        self.assertEqual(e.state(jid), "awaiting_approval")
        e.orch.approve(jid, by=e.user["email"], budget_usd="10")
        e.drain()                                                                  # fail #2 → the customer sees it
        self.assertEqual(e.state(jid), "ready_for_review")
        self.assertIn("the story is flat", json.dumps(e.store.artifact(jid, "customer_notes")))
        e.orch.accept(jid, e.user["email"])
        self.assertEqual(e.state(jid), "accepted")
        no_founder_wait(self, e, jid)

    def test_a_measured_fail_never_ships_it_goes_to_repair_then_the_customer_chooses_to_stop_or_pay_for_a_rework(self):
        e = self.e
        from product import verify

        def bad_copy(*a, **k):
            return {"check_id": "exact_copy_match", "control": "EXACT_COPY_MATCH", "status": "FAIL", "detail": "a letter is missing"}
        with mock.patch.object(verify, "exact_copy_match", side_effect=bad_copy):
            jid = e.submit("image", text=IMAGE_ORDER)
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="10")
            e.drain()
        self.assertEqual(e.state(jid), "needs_customer_decision")
        d = e.store.artifact(jid, "customer_decision")
        self.assertIn("exact_copy_match", json.dumps(d))
        self.assertEqual(sorted(d["options"]), ["rework", "stop"])
        with self.assertRaises(Exception):
            e.orch.accept(jid, e.user["email"])
        paid = len([a for a in e.store.attempts(jid) if a["category"] == "provider"])
        budget = Decimal(e.store.job(jid)["budget_usd"])
        with mock.patch.object(verify, "exact_copy_match", side_effect=bad_copy):
            e.orch.decide(jid, by=e.user["email"], choice="rework", note="try once more")      # a paid rework: new pictures
            self.assertEqual(e.state(jid), "producing")
            e.drain()
        self.assertGreater(len([a for a in e.store.attempts(jid) if a["category"] == "provider"]), paid)
        self.assertTrue(e.store.events(jid, ("customer_rework",)))
        self.assertGreaterEqual(Decimal(e.store.job(jid)["budget_usd"]), budget)
        self.assertEqual(e.state(jid), "needs_customer_decision")                       # still failing: never shipped
        e.orch.decide(jid, by=e.user["email"], choice="stop", note="not worth more money")
        self.assertEqual(e.state(jid), "abandoned")
        no_founder_wait(self, e, jid)

    def test_no_simulated_journey_ever_enters_a_founder_only_wait(self):
        e = self.e
        for jid in (e.submit("image", text=IMAGE_ORDER), fx.submit_backpack_film(e)):
            accept_alternatives(e, jid)
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            e.produce(jid)
            e.orch.accept(jid, e.user["email"])
            self.assertEqual(e.state(jid), "accepted")
            no_founder_wait(self, e, jid)


# ── §4 learning is automated ───────────────────────────────────────────────────────────────────────────────────────────
def closed_job(e, outcome, *, card=None, when=None):
    jid = e.store.create_job(account_id=e.acct, user_id=e.user["id"], title="t", media="image", brief={"text": "x"}, budget_usd="1")
    e.store.set_job(jid, outcome=outcome, state=outcome, closed_at=when or utc_now())
    if card:
        e.store.llm_start(jid, role="chef:recipe", provider="simulated", model="simulated", isolated=False, input_sha256="0",
                          context_kinds=[], worker="chef", form="recipe", card_version=card)
    return jid


def lesson(worker, target, diff, why="evidence"):
    return {"outcome": "accepted", "what_the_customer_said": "", "per_worker": [
        {"worker": worker, "what_went_right": "", "what_went_wrong": "", "evidence_refs": ["x"],
         "proposed_change": {"target": target, "diff": diff, "why": why}}]}


class LearningIsAutomated(unittest.TestCase):
    def setUp(self):
        self.e = Env()
        self.q = self.e.orch.lessons

    def tearDown(self):
        self.e.close()

    def test_a_more_careful_lesson_applies_immediately_and_the_founder_can_undo_it_exactly(self):
        e, q = self.e, self.q
        jid = closed_job(e, "rejected")
        before = e.orch.equipment.verdict("lift_closed_product", "FILM-C")
        [lid] = q.enqueue(jid, lesson("small_taster", "equipment_sheet", {"id": "EQ-003", "action_class": "lift_closed_product",
                                                                          "verdict": "cannot", "sample_count": 4}))
        self.assertEqual(q.lesson(lid)["status"], "applied")
        self.assertEqual(e.orch.equipment.verdict("lift_closed_product", "FILM-C")["verdict"], "cannot")
        applied = json.loads(q.lesson(lid)["applied_json"])
        self.assertEqual(applied["before"]["verdict"], "risky")
        self.assertEqual(applied["after"]["verdict"], "cannot")
        with self.assertRaises(PermissionError):
            q.undo(lid, founder="operator:claude", note="undo it please, builder")
        q.undo(lid, founder=e.founder(), note="The lift was fine on the next brand; restore.")
        self.assertEqual(e.orch.equipment.verdict("lift_closed_product", "FILM-C"), before)
        self.assertEqual(q.lesson(lid)["status"], "undone")

    def test_a_bolder_lesson_waits_for_two_accepted_jobs(self):
        e, q = self.e, self.q
        diff = {"action_class": "lift_closed_product", "verdict": "reliable", "routes": ["FILM-C"]}
        [a] = q.enqueue(closed_job(e, "accepted"), lesson("small_taster", "equipment_sheet", diff))
        [b] = q.enqueue(closed_job(e, "rejected"), lesson("small_taster", "equipment_sheet", diff))
        self.assertEqual(q.lesson(a)["status"], "waiting_support")
        self.assertEqual(q.lesson(b)["status"], "waiting_support")
        self.assertEqual(e.orch.equipment.verdict("lift_closed_product", "FILM-C")["verdict"], "risky")
        [c] = q.enqueue(closed_job(e, "accepted"), lesson("small_taster", "equipment_sheet", diff))
        self.assertEqual(q.lesson(c)["status"], "applied")
        self.assertEqual(q.lesson(a)["status"], "applied_with_support")
        self.assertEqual(e.orch.equipment.verdict("lift_closed_product", "FILM-C")["verdict"], "reliable")

    def test_a_change_to_a_judges_card_may_relax_a_check_so_it_waits_for_the_founders_review(self):
        # reviewer 2026-09-24 (founder: "do both the fixes"): was ≥ 2 accepted jobs then auto; now always the founder's review
        e, q = self.e, self.q
        diff = {"worker": "small_taster", "changes": {"kra_add": "A slightly soft edge on the product is acceptable."}}
        for _ in range(3):
            [a] = q.enqueue(closed_job(e, "accepted"), lesson("small_taster", "rulebook_card", diff))
            self.assertEqual((q.lesson(a)["kind"], q.lesson(a)["status"]), ("founder_only", "founder_only"))
        self.assertEqual(e.orch.rulebook.version("small_taster"), 1)

    def test_one_customers_taste_goes_on_that_customers_shelf_only(self):
        e, q = self.e, self.q
        other = e.store.create_account("Rival", ceiling_usd="5")
        [lid] = q.enqueue(closed_job(e, "accepted"), lesson("waiter", "customer_shelf",
                                                            {"kind": "tone_note", "key": "no pastels", "data": {"note": "never pastel colours"}}))
        self.assertEqual(q.lesson(lid)["status"], "applied")
        self.assertEqual([r["key"] for r in e.orch.shelf.approved(e.acct, "tone_note")], ["no pastels"])
        self.assertEqual(e.orch.shelf.approved(other, "tone_note"), [])

    def test_a_rulebook_change_applies_is_watched_for_five_jobs_and_rolls_back_on_a_drop(self):
        e, q = self.e, self.q
        for _ in range(5):
            closed_job(e, "accepted", card=1)
        [lid] = q.enqueue(closed_job(e, "accepted", card=1), lesson("chef", "rulebook_card",
                                                                    {"worker": "chef", "changes": {"kra_add": "Always open on a close-up."}}))
        self.assertEqual(q.lesson(lid)["status"], "applied")
        v1_kra = rulebook.seed_cards()["chef"]["kra"]
        self.assertEqual(e.orch.rulebook.version("chef"), 2)
        for _ in range(4):
            closed_job(e, "rejected", card=2)
        self.assertEqual(q.review_watches(), [])                                    # only 4 watched jobs so far
        closed_job(e, "rejected", card=2)
        rolled = q.review_watches()
        self.assertEqual(rolled, [lid])
        self.assertEqual(e.orch.rulebook.card("chef")["kra"], v1_kra)
        self.assertEqual(e.orch.rulebook.version("chef"), 3)
        self.assertEqual(q.lesson(lid)["status"], "rolled_back")
        self.assertIn("rolled back", e.orch.rulebook.history("chef")[-1]["reason"])

    def test_a_money_or_override_lesson_is_never_applied_automatically(self):
        e, q = self.e, self.q
        v = e.orch.rulebook.version("chef")
        [a] = q.enqueue(closed_job(e, "accepted"), lesson("chef", "rulebook_card",
                                                          {"worker": "chef", "changes": {"kra_add": "Raise the budget cap to USD 50 when needed."}}))
        [b] = q.enqueue(closed_job(e, "accepted"), lesson("recipe_checker", "rulebook_card",
                                                          {"worker": "recipe_checker", "changes": {"kra_add": "The customer may override a check."}}))
        for lid in (a, b):
            self.assertEqual(q.lesson(lid)["status"], "founder_only")
        self.assertEqual(e.orch.rulebook.version("chef"), v)

    def test_the_weekly_digest_lists_what_was_learned_from_which_job_with_an_undo_button(self):
        e, q = self.e, self.q
        jid = closed_job(e, "rejected")
        q.enqueue(jid, lesson("big_taster", "failure_diary", {"text": "a new failure", "failure_mode": "generation",
                                                              "action_classes": ["lift_closed_product"], "routes": ["FILM-C"]}))
        from product.tests.test_web import Client
        from product.web.app import App
        app = App(e.s)
        e.founder_session()
        c = Client(app)
        c.login("founder@mi.test")
        page = c.req("GET", "/ops/digest")["body"]
        self.assertIn(jid.encode(), page)
        self.assertIn(b"a new failure", page)
        self.assertIn(b"Undo", page)


class RunbookFounderAccount(unittest.TestCase):
    def test_the_runbook_says_only_the_founder_creates_and_holds_the_founder_account(self):
        text = (REPO / "deploy/RUNBOOK-P1.md").read_text()
        self.assertIn("init-founder", text)
        self.assertIn("never", text.lower())
        self.assertIn("builder", text.lower())


if __name__ == "__main__":
    unittest.main()
