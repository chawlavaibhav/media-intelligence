"""Front of house — the waiter (kitchen v3, founder-approved 2026-09-25: the waiter takes the order and hands it to the
chef; the pantry checker is retired, so no order waits at a pantry). USD 0, no network."""
import hashlib
import json
import unittest

from product import rulebook
from product.tests import fixtures_v2 as fx
from product.tests.support import Env


def provider_attempts(e, jid):
    return [a for a in e.store.attempts(jid) if a["category"] == "provider"]


class TheWaiterHandsTheOrderToTheChef(unittest.TestCase):
    def setUp(self):
        self.e = Env()

    def tearDown(self):
        self.e.close()

    def test_the_backpack_order_goes_straight_to_the_plan_card_and_only_the_look_picture_is_bought(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")
        self.assertIsNone(e.store.artifact(jid, "feasibility"))
        path = [json.loads(x["data_json"]).get("to") for x in e.store.events(jid, ("state",))]
        self.assertNotIn("feasibility", path)
        self.assertNotIn("awaiting_customer_input", path)
        self.assertEqual({a["node_id"] for a in provider_attempts(e, jid)}, {"preview"})   # the look of the film, nothing else

    def test_the_waiter_labels_every_photo_and_flags_the_wrong_photo_note(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.drain()
        u = e.store.artifact(jid, "understanding")
        roles = {r["photo"]: r["role"] for r in u["photo_roles"]}
        self.assertEqual(roles, {1: "product_view", 2: "infographic", 3: "lifestyle"})
        self.assertTrue(any("photo 2" in m["where"] for m in u["mismatches"]), u["mismatches"])

    def test_a_job_left_in_the_retired_pantry_step_is_handed_to_the_chef(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.orch.step(jid)                                             # the waiter
        with e.store.tx() as c:                                      # an older job still sitting in `feasibility`
            c.execute("UPDATE jobs SET state='feasibility' WHERE id=?", (jid,))
        e.orch.step(jid)
        self.assertEqual(e.state(jid), "directing")


class CustomersExactWordsReachEveryAiCall(unittest.TestCase):
    """Spec §11 test 11 (front-of-house calls)."""

    def test_every_ai_call_carries_the_order_slip_words_byte_for_byte_and_records_its_card_version(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            e.drain()
            words = e.store.artifact(jid, "order_slip")["customer_exact_words"]
            self.assertEqual(words, fx.BACKPACK_FILM_ORDER)
            sha = hashlib.sha256(words.encode()).hexdigest()
            calls = e.store.llm_calls(jid)
            self.assertEqual({c["worker"] for c in calls}, {"waiter", "chef"})
            seeds = rulebook.seed_cards()
            for c in calls:
                self.assertEqual(c["exact_words_sha256"], sha)
                self.assertEqual(c["card_version"], int(seeds[c["worker"]]["version"]))
                self.assertIn("CUSTOMER_EXACT_WORDS", c["context_kinds"])
            self.assertEqual(e.store.artifact(jid, "understanding")["customer_exact_words"], words)
            for name in ("understanding", "recipe"):
                f = e.store.artifact(jid, name)
                self.assertEqual(f["rulebook_card_version"], int(seeds[f["written_by"]["worker"]]["version"]))
                self.assertTrue(f["written_by"]["model"])
        finally:
            e.close()


@unittest.skipUnless(fx.evidence_dir(), "the private evidence repository is not checked out next to this one")
class OnTheVerbatimEvidence(unittest.TestCase):
    def test_the_real_order_of_the_rejected_film_reaches_the_customers_plan_card_before_any_production_spend(self):
        ev = fx.evidence_film(fx.evidence_dir())
        e = Env()
        try:
            b = ev["brief"]
            ups = [{"role": r, "filename": p.name, "data": p.read_bytes()} for r, p in ev["uploads"]]
            jid = e.svc.submit(e.user, title="evidence film", media="video", text=b["text"], formats=b["formats"], duration_s=b["duration_s"],
                               exact_strings=b["exact_strings"], product=b["product"], brand_colours=b["brand_colours"], max_budget_usd="15",
                               allow_preview_spend=True, uploads=ups, references_note=b["references_note"])
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_approval")
            self.assertEqual({a["node_id"] for a in provider_attempts(e, jid)}, {"preview"})
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
