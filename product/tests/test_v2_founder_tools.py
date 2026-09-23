"""P1 v2 phase 7 — the cost report, the judges' qualification harness (simulated) and the founder's pages.
Spec §11 test 15; checklist H1–H4, I1–I4, B9, E8–E9 through the web app. USD 0."""
import json
import os
import re
import unittest
from decimal import Decimal

from product import cost
from product.qualification import judges
from product.tests import fixtures_v2 as fx
from product.tests.support import Env
from product.tests.test_web import Client
from product.web.app import App


class CostReport(unittest.TestCase):
    """Spec §11 test 15 — a simulated film job reports its estimated reasoning cost per worker against the §9.4 budget."""

    def test_a_simulated_film_job_reports_estimated_reasoning_cost_per_worker_and_flags_it_against_the_budget(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            self.assertEqual(fx.film_to_hold(e, jid), "ready_for_review")
            q = e.store.artifact(jid, "quote")
            self.assertGreater(Decimal(q["reasoning_line_usd"]), 0)                 # the quote shows the reasoning line
            r = cost.reasoning_report(e.orch, jid, e.store.artifact(jid, "recipe"))
            self.assertEqual(r["budget_usd"], "0.30")
            self.assertEqual(r["targets"], {"film": "0.30", "image": "0.08"})           # amendment 1 §1: both targets shown
            self.assertEqual(r["mode"], "simulated")
            workers = set(r["per_worker"])
            self.assertTrue({"waiter", "pantry_checker", "chef", "recipe_checker", "small_taster", "big_taster", "diary_writer"} <= workers)
            total = sum(Decimal(x["estimated_usd"]) + Decimal(x["expected_usd"]) for x in r["per_worker"].values())
            self.assertEqual(Decimal(r["estimated_total_usd"]), total.quantize(Decimal("0.0001")))
            self.assertEqual(r["within_budget"], total <= Decimal("0.30"))            # honest: reported either way
            self.assertLess(total, Decimal("2.33") / 3)                               # v1 actual: USD 2.33 per film
            for c in e.store.llm_calls(jid):
                self.assertGreater(Decimal(c["est_cost_usd"]), 0)
                self.assertEqual(Decimal(c["est_cost_usd"]),
                                 e.orch.workers.estimate(c["worker"] if c["model"] != "gemini-3.1-pro-preview" or c["worker"] != "small_taster"
                                                         else "small_taster_escalation", c["est_in_tokens"])[1])
            self.assertEqual(r["per_worker"]["chef"]["model"], "azure_openai:gpt-5.6-sol")
        finally:
            e.close()

    def test_models_are_configuration_the_chef_and_judges_must_be_different_companies_and_a_decision_slot_exists(self):
        from product import config
        os.environ["MI_MODEL_RECIPE_CHECKER"] = "azure_openai:gpt-5.6-terra"
        try:
            with self.assertRaises(ValueError):
                config.check_independence(config.worker_models())
        finally:
            os.environ.pop("MI_MODEL_RECIPE_CHECKER")
        os.environ["MI_MODEL_DECISION"] = "decision:jev-1"
        try:
            self.assertEqual(config.worker_models()["decision"], "decision:jev-1")
        finally:
            os.environ.pop("MI_MODEL_DECISION")
        self.assertNotIn("decision", config.worker_models())
        from pathlib import Path
        src = "".join(Path(p).read_text() for p in ("product/stations/chef.py", "product/stations/waiter.py", "product/stations/pantry.py",
                                               "product/stations/tasters.py", "product/stations/head_cook.py"))
        for model in ("gpt-5", "gemini-3", "claude-"):
            self.assertNotIn(model, src)


class JudgesQualification(unittest.TestCase):
    def test_the_harness_scores_every_judge_on_known_verdicts_and_a_simulated_run_can_never_qualify(self):
        rep = judges.run(out=None)
        self.assertEqual(rep["spent_usd"], "0.000000")
        self.assertEqual(set(rep["judges"]), {"recipe_checker", "small_taster", "big_taster"})
        for j, r in rep["judges"].items():
            self.assertFalse(r["qualified"], j)
            self.assertIn("simulated", r["why_not_qualified"])
            self.assertEqual(r["available"] + r["unavailable"], len(r["cases"]))
        if fx.evidence_dir():
            st = rep["judges"]["small_taster"]
            self.assertEqual(st["available"], 9)
            self.assertIsNotNone(st["known_bad_caught"])
        self.assertEqual(len(rep["judges"]["big_taster"]["cases"]), 3 + 14 + 62)          # amendment 1 §2: the old jobs too
        self.assertEqual(len(rep["judges"]["recipe_checker"]["cases"]), 2 + 6)
        self.assertEqual([m["case"] for m in rep["recipe_checker_missing"]], ["UPWORK-PORTFOLIO-002"])

    def test_a_live_run_is_refused_without_the_founders_own_session(self):
        with self.assertRaises(SystemExit):
            judges.run(live=True)
        e = Env()
        try:
            e.operator("ops@mi.test")
            with self.assertRaises(PermissionError):
                judges.run(live=True, founder_session=e.session_of("ops@mi.test"), product_data=str(e.dir))
        finally:
            e.close()

    def test_until_qualified_a_judges_no_blocks_and_its_yes_goes_to_the_customers_preview(self):
        e = Env()
        try:
            self.assertEqual(e.s.qualified_judges, ())
            jid = e.submit("image", text="A calm launch poster for our navy travel backpack; the bag must be the first thing you see; no people.")
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_approval")                      # amendment 1 §3: straight to the customer
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            e.drain()
            self.assertEqual(e.state(jid), "ready_for_review")
            results = e.store.artifact(jid, "gateway_report")["results"]
            open_ = {b["check_id"] for r in results for b in r["judgement_open"]}
            self.assertTrue({"small_taster_confirmed", "independent_review", "product_fidelity"} <= open_, open_)
            self.assertTrue(all(r["presentable"] and not r["ready"] for r in results))   # shown, not yet verified
        finally:
            e.close()


class FounderPages(unittest.TestCase):
    def setUp(self):
        self.e = Env()
        self.app = App(self.e.s)
        self.e.founder_session()
        self.e.operator("ops@mi.test")
        self.f = Client(self.app); self.f.login("founder@mi.test")
        self.ops = Client(self.app); self.ops.login("ops@mi.test")

    def tearDown(self):
        self.e.close()

    def test_an_operator_is_refused_every_decision_the_founder_decides_with_a_reason_and_pages_render(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.drain()
        f = e.store.artifact(jid, "feasibility")
        e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=[
            {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")                      # no founder wait (amendment 1 §3)
        page = self.ops.req("GET", f"/ops/jobs/{jid}")["body"]
        self.assertIn(b"You can view and pause", page)
        tok = self.ops.csrf(f"/ops/jobs/{jid}")
        r = self.ops.req("POST", f"/ops/jobs/{jid}/pause", {"csrf": tok, "reason": "the customer phoned; hold it"})
        self.assertTrue(r["status"].startswith("303"), r["status"])             # anyone on the team may pause (an intervention)
        self.assertEqual(e.state(jid), "paused_operator")
        tok = self.ops.csrf(f"/ops/jobs/{jid}")
        r = self.ops.req("POST", f"/ops/jobs/{jid}/resume", {"csrf": tok, "reason": "looks fine to me, operator here"})
        self.assertTrue(r["status"].startswith("403"), r["status"])
        self.assertEqual(e.state(jid), "paused_operator")
        tok = self.f.csrf(f"/ops/jobs/{jid}")
        r = self.f.req("POST", f"/ops/jobs/{jid}/resume", {"csrf": tok, "reason": "Spoke to the customer: zips as stills is fine."})
        self.assertTrue(r["status"].startswith("303"), r["body"][:300])
        self.assertEqual(e.state(jid), "awaiting_approval")
        page = self.f.req("GET", f"/ops/jobs/{jid}")["body"]
        self.assertIn(b"Founder overrides on this job", page)
        self.assertIn(b"zips as stills", page)
        self.assertIn(b"AI reasoning cost", page)
        for path in ("/ops/rulebook", "/ops/library", "/ops/lessons", "/ops/digest", "/ops"):
            r = self.ops.req("GET", path)
            self.assertTrue(r["status"].startswith("200"), path)
        self.assertIn(b"EQ-001", self.f.req("GET", "/ops/library")["body"])
        self.assertIn(b"KRA", self.f.req("GET", "/ops/rulebook")["body"])

    def test_the_founder_undoes_an_applied_lesson_and_decides_a_money_lesson_in_the_web_app_and_an_operator_cannot(self):
        e = self.e
        jid = e.submit("image", text="A calm launch poster for our navy travel backpack; the bag must be the first thing you see; no people.")
        e.drain()
        e.orch.abandon(jid, e.user["email"], "closing to test the lessons")
        applied = [r for r in e.orch.lessons.all(jid) if r["status"] == "applied" and r["target"] == "recipe_library"]
        self.assertTrue(applied)
        lid = applied[0]["id"]
        rid = json.loads(applied[0]["applied_json"])["id"]
        self.assertIn(lid.encode(), self.ops.req("GET", "/ops/digest")["body"])
        tok = self.ops.csrf("/ops/digest")
        r = self.ops.req("POST", f"/ops/lessons/{lid}/undo", {"csrf": tok, "note": "operator trying to undo this one"})
        self.assertTrue(r["status"].startswith("403"))
        self.assertEqual(e.orch.lessons.lesson(lid)["status"], "applied")
        tok = self.f.csrf("/ops/digest")
        r = self.f.req("POST", f"/ops/lessons/{lid}/undo", {"csrf": tok, "note": "A closed test job is not a recipe worth keeping."})
        self.assertTrue(r["status"].startswith("303"), r["body"][:300])
        self.assertEqual(e.orch.lessons.lesson(lid)["status"], "undone")
        self.assertEqual(e.orch.lessons.lesson(lid)["undone_by"], "founder:founder@mi.test")
        self.assertIsNone(e.store.q1("SELECT id FROM recipe_library WHERE id=?", (rid,)))
        # a money lesson waits for the founder, who may approve it with an edit
        [money] = e.orch.lessons.enqueue(jid, {"per_worker": [{"worker": "chef", "evidence_refs": ["test"], "proposed_change": {
            "target": "rulebook_card", "why": "cheaper plans", "diff": {"worker": "chef", "changes": {"kra_add": "Keep each plan under USD 0.10."}}}}]})
        self.assertEqual(e.orch.lessons.lesson(money)["status"], "founder_only")
        tok = self.ops.csrf("/ops/lessons")
        r = self.ops.req("POST", f"/ops/lessons/{money}", {"csrf": tok, "decision": "approve", "note": "operator trying to approve this"})
        self.assertTrue(r["status"].startswith("403"))
        tok = self.f.csrf("/ops/lessons")
        edited = {"worker": "chef", "changes": {"kra_add": "Edited by the founder: keep plans short."}}
        r = self.f.req("POST", f"/ops/lessons/{money}", {"csrf": tok, "decision": "edit", "note": "Keep it, but with my wording, no numbers.",
                                                         "edited": json.dumps(edited)})
        self.assertTrue(r["status"].startswith("303"), r["body"][:300])
        self.assertEqual(e.orch.lessons.lesson(money)["status"], "approved_edited")
        self.assertIn("Edited by the founder: keep plans short.", e.orch.rulebook.card("chef")["kra"])

    def test_the_customer_answers_the_pantry_checker_approves_the_master_plate_and_manages_the_shelf_in_the_web_app(self):
        e = self.e
        c = Client(self.app); c.login("buyer@acme.test")
        jid = fx.submit_backpack_film(e)
        e.drain()
        page = c.req("GET", f"/jobs/{jid}")["body"]
        self.assertIn(b"we need something from you", page)
        self.assertIn(b"Nothing has been spent on production yet", page)
        n = len(e.store.artifact(jid, "feasibility")["alternatives"])
        tok = c.csrf(f"/jobs/{jid}")
        r = c.req("POST", f"/jobs/{jid}/input", {"csrf": tok, **{f"alt_{i}": "yes" for i in range(n)}, "note": "fine"}, files=[])
        self.assertTrue(r["status"].startswith("303"), r["body"][:300])
        e.drain()
        tok = c.csrf(f"/jobs/{jid}")
        page = c.req("GET", f"/jobs/{jid}")["body"]
        self.assertIn(b"Planning and checking (AI reasoning, estimated)", page)
        c.req("POST", f"/jobs/{jid}/approve", {"csrf": tok, "budget_usd": "15"})
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_master_approval")
        page = c.req("GET", f"/jobs/{jid}")["body"]
        self.assertIn(b"Approve the look of your film", page)
        master = re.search(rb'/assets/(ast_\w+)" alt="The master', page).group(1).decode()
        self.assertTrue(c.req("GET", f"/assets/{master}")["status"].startswith("200"))
        tok = c.csrf(f"/jobs/{jid}")
        c.req("POST", f"/jobs/{jid}/master", {"csrf": tok})
        self.assertEqual(e.state(jid), "producing")
        shelf = c.req("GET", "/shelf")["body"]
        self.assertIn(b"master plate", shelf)
        spy_acct = e.store.create_account("Rival", ceiling_usd="10")
        e.customer("spy@rival.test", spy_acct)
        spy = Client(self.app); spy.login("spy@rival.test")
        self.assertNotIn(b"master plate", spy.req("GET", "/shelf")["body"])
        sid = e.orch.shelf.items(e.acct)[0]["id"]
        tok = spy.csrf("/shelf")
        self.assertTrue(spy.req("POST", f"/shelf/{sid}", {"csrf": tok, "decision": "reject"})["status"].startswith("404"))


if __name__ == "__main__":
    unittest.main()
