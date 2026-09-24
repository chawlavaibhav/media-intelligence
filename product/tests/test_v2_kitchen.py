"""P1 v2 phase 4 — the chef, the librarian and the recipe checker: trays, binding send-back.
Spec §11 test 1 (recipe half) and test 12. USD 0, no network."""
import json
import unittest

from product import flow
from product.library.librarian import CAPS
from product.tests import fixtures_v2 as fx
from product.tests.support import Env


def provider_attempts(e, jid):
    return [a for a in e.store.attempts(jid) if a["category"] == "provider"]


def to_directing(e, jid):
    """Accept the pantry checker's alternatives so the order reaches the chef."""
    e.drain()
    f = e.store.artifact(jid, "feasibility")
    if e.state(jid) == "awaiting_customer_input":
        e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=[
            {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
        e.orch.step(jid)
        e.orch.step(jid)
    assert e.state(jid) == "directing", e.state(jid)


class TheV1RecipeIsSentBackBeforeSpend(unittest.TestCase):
    """Spec §11 test 1 — the chef cannot plan hands working zips or folding the flap."""

    def test_the_rejected_films_recipe_is_sent_back_by_code_for_every_mechanism_shot_and_no_paid_call_is_made(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            to_directing(e, jid)
            u, f = e.store.artifact(jid, "understanding"), e.store.artifact(jid, "feasibility")
            e.orch.sim.chef__recipe = lambda b, media: fx.v1_recipe(u, f)            # the chef insists on the v1 recipe
            e.orch.step(jid)
            # 2 send-back rounds, then the SYSTEM applies the safest alternative (amendment 1 §3) — never the founder
            self.assertEqual(flow.rounds_used(e.store, jid, "SB-RECIPE"), 2)
            self.assertEqual(len(e.store.artifact_versions(jid, "recipe")), 4)        # 3 by the chef + the system's safe re-plan
            rc = e.store.artifact(jid, "recipe_check", 3)                            # the third check of the chef's v1 recipe
            self.assertEqual(rc["verdict_after_code"], "send_back")
            cannot = {x["where"].split(" ")[1] for x in rc["code_findings"] if x["rule"] == "R1:cannot_on_route"}
            for n in ("2", "3", "5", "6", "7"):                                   # zips pulled, flap folded/raised, zips closed
                self.assertIn(n, cannot, rc["code_findings"])
            self.assertTrue(any("EQ-001" in x["finding"] for x in rc["code_findings"]))
            self.assertTrue(any(x["rule"] == "R3:risky_not_limited" for x in rc["code_findings"]))   # the laptop slide, the lift
            self.assertEqual([a for a in provider_attempts(e, jid) if a["node_id"] != "preview"], [])   # no production spend
            v1 = e.store.artifact(jid, "recipe", 3)
            self.assertTrue(all(s["route"] == "FILM-C" for s in v1["shots"] if s["route"] != "END-CARD"))
            safe = e.store.artifact(jid, "recipe")
            for n in (2, 3, 5, 6, 7):                                             # the mechanism shots are stills now
                self.assertEqual(next(s for s in safe["shots"] if s["n"] == n)["route"], "FILM-A")
            self.assertEqual(e.state(jid), "awaiting_approval")
        finally:
            e.close()

    def test_the_recipe_checkers_model_cannot_approve_a_cannot_action_even_if_it_says_approve(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            to_directing(e, jid)
            u, f = e.store.artifact(jid, "understanding"), e.store.artifact(jid, "feasibility")
            r = fx.v1_recipe(u, f)
            from product.stations import recipe_check
            tray = e.orch.librarian.tray(jid, "recipe_checker", query="x", media="video", account_id=e.acct,
                                         action_classes=["hands_work_mechanism"], routes=["FILM-C"])
            orig = e.orch.sim.recipe_checker__recipe_check
            e.orch.sim.recipe_checker__recipe_check = lambda b, m: {**orig(b, m), "verdict": "approve", "predicted_acceptance": "likely"}
            rc = recipe_check.check(e.orch, jid, r, tray)
            self.assertEqual(rc["verdict"], "approve")
            self.assertEqual(rc["verdict_after_code"], "send_back")
        finally:
            e.close()


class RecipeRoundsAndTheCustomer(unittest.TestCase):
    def test_a_good_recipe_goes_straight_to_the_customer_as_our_reviewer_found_no_problems(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            to_directing(e, jid)
            e.orch.step(jid)
            self.assertEqual(e.state(jid), "awaiting_approval")                  # amendment 1 §3: no founder confirmation
            self.assertEqual(e.store.artifact(jid, "recipe_check")["verdict_after_code"], "approve")
            self.assertEqual(e.store.artifact(jid, "plan_note")["text"], "Our reviewer found no problems with this plan.")
            q = e.store.artifact(jid, "quote")
            self.assertIn("reasoning_line_usd", q)
            self.assertTrue(e.store.assets(jid, role="preview"))                  # the sample picture (the master plate draft)
            recipe = e.store.artifact(jid, "recipe")
            self.assertFalse([s for s in recipe["shots"] if s["action_class"] == "hands_work_mechanism"])
            self.assertTrue(all(s["starts_from"] == "master_plate" for s in recipe["shots"] if s["route"] in ("FILM-B", "FILM-C")))
        finally:
            e.close()

    def test_the_founder_may_still_override_the_reviewers_objections_but_never_has_to_and_the_reason_is_kept(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            to_directing(e, jid)
            orig = e.orch.sim.recipe_checker__recipe_check
            e.orch.sim.recipe_checker__recipe_check = lambda b, m: {**orig(b, m), "verdict": "send_back"}
            e.orch.step(jid)
            self.assertEqual(e.state(jid), "awaiting_approval")                  # objections go to the customer
            self.assertTrue(e.store.artifact(jid, "plan_objections"))
            with self.assertRaises(PermissionError):
                e.orch.override_recipe(jid, session=e.session_of("buyer@acme.test"), reason="customer wants it anyway, push it")
            e.orch.override_recipe(jid, session=e.founder_session(), reason="Testing the override path; this recipe must not ship.")
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")             # no need to accept objections once overridden
            self.assertEqual(e.state(jid), "planning")
            o = e.store.overrides(jid, "recipe_send_back")[0]
            self.assertEqual(o["founder_email"], "founder@mi.test")
            self.assertIn("must not ship", o["reason"])
        finally:
            e.close()


class TraysAreCappedLoggedAndCarryMatchingFailures(unittest.TestCase):
    """Spec §11 test 12."""

    def test_the_chef_gets_a_capped_tray_with_the_failures_for_its_action_classes_and_the_ids_are_logged(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            to_directing(e, jid)
            e.orch.step(jid)
            tray = e.store.artifact(jid, "tray:chef")
            self.assertLessEqual(tray["tokens"], CAPS["chef"])
            self.assertEqual(tray["cap_tokens"], 6000)
            ids = [i["id"] for i in tray["items"]]
            sections = {i["section"] for i in tray["items"]}
            self.assertTrue({"cookbook", "failure_diary", "recipe_library"} <= sections, sections)
            self.assertLessEqual(len([i for i in tray["items"] if i["section"] == "cookbook"]), 6)
            self.assertLessEqual(len([i for i in tray["items"] if i["section"] == "recipe_library"]), 3)
            self.assertIn("FD-0923-02", ids)                   # continuity drift: matches the planned insert action class
            self.assertIn("RL-0923-FILM", ids)                 # the similar past recipe, with its outcome (rejected)
            self.assertIn("insert_object_into_container", tray["filters"]["action_classes"])
            chef_call = [c for c in e.store.llm_calls(jid) if c["worker"] == "chef"][-1]
            self.assertEqual(json.loads(chef_call["tray_ids"]), ids)
            # the whole Canon is ~25,000 tokens; the chef's tray is a fraction of it
            self.assertLess(tray["tokens"], 25000 / 4)
            rt = e.store.artifact(jid, "tray:recipe_checker")
            self.assertLessEqual(rt["tokens"], CAPS["recipe_checker"])
            self.assertTrue(any(i["section"] == "equipment_sheet" for i in rt["items"]))
            pt = e.store.artifact(jid, "tray:pantry_checker")
            self.assertLessEqual(pt["tokens"], CAPS["pantry_checker"])
            self.assertIn("EQ-001", [i["id"] for i in pt["items"]])
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
