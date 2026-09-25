"""P1 v2 phase 4 — the chef, the librarian and the recipe checker: trays, binding send-back.
Spec §11 test 1 (recipe half) and test 12. USD 0, no network."""
import json
import unittest

from product import flow
from product.library.librarian import CAPS
from product.library import stats
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


# Kitchen v3 (founder-approved 2026-09-25): the recipe checker is retired — the customer checks the recipe. The tests that
# asserted its send-backs, its code rules R1-R6 and the system's safe re-plan were removed with it; the new line is tested
# in test_v3_kitchen.py.


def seen(e, items):
    from product import library
    rows = {r["id"]: r for r in library.FailureDiary(e.store).all(None)}
    return [(rows[i["id"]]["times_seen"], rows[i["id"]]["jobs_on_record"]) for i in items]


class TraysAreCappedLoggedAndCarryMatchingFailures(unittest.TestCase):
    """Spec §11 test 12."""

    def test_the_chef_gets_a_capped_tray_with_the_failures_for_its_action_classes_and_the_ids_are_logged(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            e.drain()                                  # kitchen v3: waiter -> chef -> the customer's plan card
            tray = e.store.artifact(jid, "tray:chef")
            self.assertLessEqual(tray["tokens"], CAPS["chef"])
            self.assertEqual(tray["cap_tokens"], 8000)
            ids = [i["id"] for i in tray["items"]]
            sections = {i["section"] for i in tray["items"]}
            # the books (Canon) and the cheat sheet (the tools' track record) are the chef's reading, as the founder asked
            self.assertTrue({"cookbook", "equipment_sheet", "recipe_library"} <= sections, sections)
            self.assertEqual(tray["items"][0]["section"], "cookbook")                 # the books come first
            self.assertLessEqual(len([i for i in tray["items"] if i["section"] == "cookbook"]), 6)
            self.assertLessEqual(len([i for i in tray["items"] if i["section"] == "recipe_library"]), 3)
            # founder 2026-09-24: only failure kinds that recur significantly for the sample size reach a tray, one per kind, few
            fails = [i for i in tray["items"] if i["section"] == "failure_diary"]
            self.assertLessEqual(len(fails), 3)
            self.assertTrue(all(stats.recurs_significantly(k, n) for k, n in seen(e, fails)), seen(e, fails))
            self.assertNotIn("FD-0923-03", ids)                # character drift: 3 of 23 jobs — not distinguishable from a one-off
            self.assertNotIn("FD-0923-02", ids)                # continuity drift: 2 of 23 jobs
            self.assertNotIn("FD-0923-07", ids)                # a one-off
            self.assertIn("RL-0923-FILM", ids)                 # the similar past recipe, with its outcome (rejected)
            self.assertIn("person_performance", tray["filters"]["action_classes"])
            chef_call = [c for c in e.store.llm_calls(jid) if c["worker"] == "chef"][-1]
            self.assertEqual(json.loads(chef_call["tray_ids"]), ids)
            # the whole Canon is ~25,000 tokens; the chef's tray is a fraction of it
            self.assertLess(tray["tokens"], 25000 / 4)
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
