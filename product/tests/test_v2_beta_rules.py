"""Beta rules (founder decisions 2026-09-24, ~50 files for friends as customers). USD 0, simulated.

1. The founder is never inside a running job: every wait the system itself creates is a customer's (or automatic). A step
   error retries twice by itself, then the customer chooses try again / stop. Founder overrides stay, never required.
2. The customer owns the money decision: no account ceiling in beta (MI_ENFORCE_ACCOUNT_CEILING, default off)."""
import json
import os
import unittest
from decimal import Decimal
from unittest import mock

from product import config, flow
from product.orchestrator import Orchestrator
from product.reasoning import ReasoningFailed
from product.service import Invalid
from product.stations import chef, head_cook, pantry, tasters, waiter
from product.tests import fixtures_v2 as fx
from product.tests.support import Env

IMAGE_ORDER = "A calm launch poster for our navy travel backpack; the bag must be the first thing you see; no people."
FOUNDER_ONLY = set(flow.FOUNDER_ONLY_FROM) | {"operator_hold"}


def states_of(e, jid):
    return [json.loads(x["data_json"]).get("to") for x in e.store.events(jid, ("state",))]


def paid(e, jid):
    return [a for a in e.store.attempts(jid) if a["category"] == "provider"]


def failing(fn, times, exc=None):
    """`fn`, but its first `times` calls raise (a model that returned junk, a file that would not compose ...)."""
    left = [times]

    def f(*a, **kw):
        if left[0] > 0:
            left[0] -= 1
            raise exc or ReasoningFailed("the model's answer failed its schema")
        return fn(*a, **kw)
    return f


def run_to_end(e, jid, budget="15"):
    """The customer's side of a journey, whatever the system asks: alternatives, plan (objections accepted), look, taste,
    try again after an error, final acceptance. Returns the last state."""
    for _ in range(40):
        e.drain()
        s = e.state(jid)
        if s == "awaiting_customer_input":
            f = e.store.artifact(jid, "feasibility")
            e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=[
                {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
        elif s == "awaiting_approval":
            e.orch.approve(jid, by=e.user["email"], budget_usd=budget, accept_objections=True)
        elif s == "awaiting_master_approval":
            e.orch.approve_master(jid, by=e.user["email"])
        elif s == "awaiting_taste":
            e.orch.approve_taste(jid, by=e.user["email"])
        elif s == "needs_retry_decision":
            e.orch.decide(jid, by=e.user["email"], choice="try_again")
        elif s == "ready_for_review":
            e.orch.accept(jid, e.user["email"])
        else:
            return s
    return e.state(jid)


class TheFounderIsNeverInsideARunningJob(unittest.TestCase):
    def assert_no_founder_state(self, e, jid):
        self.assertFalse([s for s in states_of(e, jid) if s in FOUNDER_ONLY], states_of(e, jid))
        self.assertIsNone(e.store.artifact(jid, "founder_decision"))

    def test_no_state_the_system_works_in_can_even_lead_to_a_founder_only_state(self):
        # the table itself: from every state the system acts in, the only founder-ish exits are a PERSON's pause
        # (paused_operator) and the founder's own optional hold before the preview (operator_hold, off by default)
        for s in flow.WORKER_STATES + flow.CUSTOMER_STATES:
            self.assertFalse(flow.ALLOWED[s] & {"paused_for_founder", "failed"}, s)
        for s in flow.WORKER_STATES:
            self.assertFalse(flow.ALLOWED[s] & FOUNDER_ONLY - {"paused_operator", "operator_hold"}, s)
        self.assertFalse(config.Settings.hold_before_preview)                  # the founder's optional hold: off
        self.assertEqual(flow.STATES["needs_retry_decision"][2], "customer")
        for gone in ("to_founder", "select_take"):                 # the founder-wait machinery is gone, not just unused
            self.assertFalse(hasattr(Orchestrator, gone), gone)
        self.assertFalse(hasattr(head_cook, "NeedsFounder"))
        self.assertFalse(hasattr(head_cook, "founder_select_take"))
        for s, (_, words, _) in flow.STATES.items():                # nothing tells the customer "our team is reviewing"
            self.assertNotIn("reviewing", words.lower(), s)

    def test_every_hostile_journey_ends_with_the_system_or_the_customer(self):
        """Walk what the system does on its own: the recipe checker never approves, the small taster rejects every take, the
        big taster fails every cut, a measured check fails, and a step errors in every station. No founder, ever."""
        from product import verify
        cases = {
            "recipe checker never approves": lambda e: mock.patch.object(
                e.orch.sim, "recipe_checker__recipe_check",
                lambda b, m, _o=e.orch.sim.recipe_checker__recipe_check: {**_o(b, m), "verdict": "send_back",
                                                                          "issues": [{"severity": "major", "where": "shot 2",
                                                                                      "issue": "flat", "fix": "surprise"}]}),
            "small taster rejects everything": lambda e: mock.patch.object(
                e.orch.sim, "small_taster__ingredient_check",
                lambda b, m, _o=e.orch.sim.small_taster__ingredient_check, **kw: {**_o(b, m, **kw), "usable": False, "notes": "no"}),
            "big taster fails every cut": lambda e: mock.patch.object(
                e.orch.sim, "big_taster__final_review",
                lambda b, m, _o=e.orch.sim.big_taster__final_review, **kw: {**_o(b, m, **kw), "verdict": "fail", "defects": [
                    {"id": "D", "where": "whole", "severity": "blocker", "description": "flat", "earliest_stage": "plan", "shot": None,
                     "repair": "re-plan"}]}),
            "a measured check fails": lambda e: mock.patch.object(verify, "exact_copy_match", side_effect=lambda *a, **k: {
                "check_id": "exact_copy_match", "control": "EXACT_COPY_MATCH", "status": "FAIL", "detail": "a letter is missing"}),
        }
        for (mod, fn) in ((waiter, "understand"), (pantry, "check"), (chef, "direct"), (head_cook, "plan"), (head_cook, "produce"),
                          (tasters, "check_cut")):
            cases[f"{fn} errors three times"] = (lambda mod, fn: lambda e: mock.patch.object(mod, fn, failing(getattr(mod, fn), 3)))(mod, fn)
        cases["produce crashes three times"] = lambda e: mock.patch.object(head_cook, "produce", failing(head_cook.produce, 3, KeyError("x")))
        for name, patch in cases.items():
            for media in ("image", "video"):
                if media == "video" and "errors" in name and "produce" not in name:
                    continue                                          # the film adds nothing to a plain step error
                with self.subTest(name, media=media):
                    e = Env()
                    try:
                        with patch(e):
                            jid = e.submit("image", text=IMAGE_ORDER) if media == "image" else fx.submit_backpack_film(e)
                            end = run_to_end(e, jid)
                            if end == "needs_customer_decision":        # a measured FAIL: the customer stops
                                e.orch.decide(jid, by=e.user["email"], choice="stop")
                        self.assertIn(e.state(jid), flow.TERMINAL, (name, states_of(e, jid)))
                        self.assert_no_founder_state(e, jid)
                    finally:
                        e.close()

    def test_a_send_back_limit_that_reaches_the_kitchen_goes_to_the_customer_with_the_objections(self):
        """Even when every recipe round and the system's safe re-plan were already used in this plan cycle (a retried step),
        the limit ends with the customer, never the founder."""
        e = Env()
        try:
            orig = e.orch.sim.recipe_checker__recipe_check
            e.orch.sim.recipe_checker__recipe_check = lambda b, m: {**orig(b, m), "verdict": "send_back", "issues": [
                {"severity": "major", "where": "the plan", "issue": "the idea is flat", "fix": "find a surprise"}]}
            jid = e.submit("image", text=IMAGE_ORDER)
            for rule in ("SB-RECIPE", "SB-RECIPE", "SB-RECIPE-SAFE"):
                e.store.event(jid, "system", "send_back", {"rule": rule, "key": "cycle1", "why": "an earlier attempt of this step"})
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_approval")
            self.assertIn("the idea is flat", " ".join(e.store.artifact(jid, "plan_objections")["plain_words"]))
            self.assertEqual(paid(e, jid), [])
            self.assert_no_founder_state(e, jid)
        finally:
            e.close()


class AStepErrorRetriesThenAsksTheCustomer(unittest.TestCase):
    def setUp(self):
        self.e = Env()

    def tearDown(self):
        self.e.close()

    def test_two_automatic_retries_then_the_customer_is_asked_to_try_again_or_stop(self):
        e = self.e
        with mock.patch.object(pantry, "check", failing(pantry.check, 99)):
            jid = e.submit("image", text=IMAGE_ORDER)
            e.drain()
        self.assertEqual(e.state(jid), "needs_retry_decision")
        self.assertEqual(e.store.job(jid)["resume_state"], "feasibility")
        retries = [json.loads(x["data_json"]) for x in e.store.events(jid, ("step_retry",))]
        self.assertEqual([(r["state"], r["retry"]) for r in retries], [("feasibility", 1), ("feasibility", 2)])
        self.assertEqual(len(e.store.events(jid, ("step_failed",))), 3)              # the first try and two retries
        self.assertIn("try again", e.store.job(jid)["pause_reason"].lower())
        self.assertTrue(flow.label("needs_retry_decision").startswith("Something went wrong on our side"))
        turn = [json.loads(x["data_json"]) for x in e.store.events(jid, ("customer_notified",))]
        self.assertTrue(any(t.get("state") == "needs_retry_decision" for t in turn), turn)

    def test_two_errors_are_absorbed_by_the_retries_and_the_customer_never_hears_of_them(self):
        e = self.e
        with mock.patch.object(pantry, "check", failing(pantry.check, 2)):
            jid = e.submit("image", text=IMAGE_ORDER)
            e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")
        self.assertEqual(len(e.store.events(jid, ("step_retry",))), 2)
        self.assertNotIn("needs_retry_decision", states_of(e, jid))

    def test_try_again_resumes_the_same_step_with_fresh_retries(self):
        e = self.e
        with mock.patch.object(pantry, "check", failing(pantry.check, 3)):
            jid = e.submit("image", text=IMAGE_ORDER)
            e.drain()
            self.assertEqual(e.state(jid), "needs_retry_decision")
            e.orch.decide(jid, by=e.user["email"], choice="try_again")
            self.assertEqual(e.state(jid), "feasibility")
            self.assertTrue(e.store.events(jid, ("customer_retry",)))
            e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")
        e.orch.approve(jid, by=e.user["email"], budget_usd="10")
        with mock.patch.object(head_cook, "produce", failing(head_cook.produce, 3, RuntimeError("disk full"))):
            e.drain()                                                                 # a crash mid-production: same rule
            self.assertEqual(e.state(jid), "needs_retry_decision")
            self.assertEqual(e.store.job(jid)["resume_state"], "producing")
            self.assertTrue(e.store.events(jid, ("step_crashed",)))
            e.orch.decide(jid, by=e.user["email"], choice="try_again")
            e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")
        self.assertFalse([s for s in states_of(e, jid) if s in FOUNDER_ONLY])

    def test_stop_ends_the_job_and_nothing_more_is_spent(self):
        e = self.e
        jid = e.submit("image", text=IMAGE_ORDER)
        e.drain()
        e.orch.approve(jid, by=e.user["email"], budget_usd="10")
        with mock.patch.object(tasters, "check_cut", failing(tasters.check_cut, 99)):
            e.drain()
        self.assertEqual(e.state(jid), "needs_retry_decision")
        spent, n = e.store.committed_usd(jid), len(paid(e, jid))
        with self.assertRaises(ValueError):
            e.orch.decide(jid, by=e.user["email"], choice="rework")                  # only try again or stop
        e.orch.decide(jid, by=e.user["email"], choice="stop", note="never mind")
        self.assertEqual(e.state(jid), "abandoned")
        self.assertEqual(e.store.job(jid)["outcome"], "abandoned")
        e.drain()
        self.assertEqual(e.store.committed_usd(jid), spent)
        self.assertEqual(len(paid(e, jid)), n)
        with self.assertRaises(ValueError):
            e.orch.decide(jid, by=e.user["email"], choice="try_again")


class NoAccountCeilingInBeta(unittest.TestCase):
    def test_the_setting_is_off_by_default_and_read_from_the_environment(self):
        e = Env()
        try:
            self.assertFalse(e.s.account_ceiling_enforced)
            os.environ["MI_ENFORCE_ACCOUNT_CEILING"] = "1"
            try:
                self.assertTrue(config.load(e.dir).account_ceiling_enforced)
            finally:
                os.environ.pop("MI_ENFORCE_ACCOUNT_CEILING")
        finally:
            e.close()

    def test_a_budget_above_the_old_ceiling_is_accepted_when_off(self):
        e = Env()                                                             # the account's old ceiling: USD 40
        try:
            jid = e.submit("image", text=IMAGE_ORDER, budget="100")
            self.assertEqual(Decimal(e.orch.brief(jid)["max_budget_usd"]), Decimal("100"))
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="75")
            self.assertEqual(Decimal(e.store.job(jid)["budget_usd"]), Decimal("75"))
            e.svc.raise_budget(e.user, jid, "90")
            self.assertEqual(Decimal(e.store.job(jid)["budget_usd"]), Decimal("90"))
            with self.assertRaises(Invalid) as cm:
                e.submit("image", text=IMAGE_ORDER, budget="0.5")                   # a minimum of USD 1 stays
            self.assertNotIn("account limit", str(cm.exception))
        finally:
            e.close()

    def test_the_old_ceiling_is_refused_when_switched_on(self):
        e = Env(account_ceiling_enforced=True)
        try:
            with self.assertRaises(Invalid):
                e.submit("image", text=IMAGE_ORDER, budget="100")
            jid = e.submit("image", text=IMAGE_ORDER, budget="20")
            e.drain()
            with self.assertRaises(PermissionError):
                e.orch.approve(jid, by=e.user["email"], budget_usd="75")
            e.orch.approve(jid, by=e.user["email"], budget_usd="10")
            with self.assertRaises(Invalid):
                e.svc.raise_budget(e.user, jid, "90")
        finally:
            e.close()

    def test_a_paid_rework_above_the_old_ceiling_is_the_customers_call_when_off(self):
        from product import verify
        for enforced in (False, True):
            e = Env(account_ceiling_enforced=enforced)
            try:
                with mock.patch.object(verify, "exact_copy_match", side_effect=lambda *a, **k: {
                        "check_id": "exact_copy_match", "control": "EXACT_COPY_MATCH", "status": "FAIL", "detail": "a letter is missing"}):
                    jid = e.submit("image", text=IMAGE_ORDER)
                    e.drain()
                    e.orch.approve(jid, by=e.user["email"], budget_usd="10")
                    e.drain()
                self.assertEqual(e.state(jid), "needs_customer_decision")
                if enforced:
                    with self.assertRaises(PermissionError):
                        e.orch.decide(jid, by=e.user["email"], choice="rework", budget_usd="60")
                else:
                    e.orch.decide(jid, by=e.user["email"], choice="rework", budget_usd="60")
                    self.assertEqual(Decimal(e.store.job(jid)["budget_usd"]), Decimal("60"))
            finally:
                e.close()

    def test_the_needs_more_budget_question_still_goes_to_the_customer(self):
        e = Env()
        try:
            jid = e.submit("image", text=IMAGE_ORDER)
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="0.01")
            e.drain()
            self.assertEqual(e.state(jid), "paused_budget")
            self.assertIn("more", e.store.job(jid)["pause_reason"])
            e.svc.raise_budget(e.user, jid, "100")                                   # above the old ceiling: the customer's call
            e.drain()
            self.assertEqual(e.state(jid), "ready_for_review")
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
