"""P1 v2 phase 3 — front of house: the waiter, the pantry and oven checker, the equipment sheet seed.
Spec §11 tests 1 (pantry half; the recipe half is in test_v2_kitchen.py), 2 and 11 (waiter + pantry calls; every
worker is covered in test_v2_journeys.py). USD 0, no network."""
import json
import unittest

from product.tests import fixtures_v2 as fx
from product.tests.support import Env


def provider_attempts(e, jid):
    return [a for a in e.store.attempts(jid) if a["category"] == "provider"]


class BackpackOrderIsStoppedBeforeSpend(unittest.TestCase):
    """Spec §11 test 1 — the v1 film's order and photos."""

    def setUp(self):
        self.e = Env()

    def tearDown(self):
        self.e.close()

    def test_hands_zipping_the_bag_is_cannot_and_the_job_pauses_for_the_customer_with_an_alternative_at_usd_0(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_customer_input")
        f = e.store.artifact(jid, "feasibility")
        self.assertEqual(f["verdict"], "cannot_make")
        zips = [a for a in f["actions_needed"] if "zipped" in a["action"]]
        self.assertTrue(zips)
        for a in zips:
            self.assertEqual(a["action_class"], "hands_work_mechanism")
            self.assertEqual(a["best_verdict"], "cannot")
            rows = [v for v in f["route_verdicts"] if v["action_id"] == a["id"] and v["route"] == "FILM-C"]
            self.assertEqual((rows[0]["verdict"], rows[0]["equipment_row"]), ("cannot", "EQ-001"))
        self.assertTrue(any("zipped" in x["for_action"] for x in f["alternatives"]))
        self.assertTrue(all(x["alternative"] for x in f["alternatives"]))              # "cannot" always comes with an alternative
        self.assertEqual(provider_attempts(e, jid), [])                                # never reached a paid call
        self.assertIn(("SB-PANTRY-CANNOT"), [json.loads(x["data_json"])["rule"] for x in e.store.events(jid, ("send_back",))])

    def test_the_waiter_labels_every_photo_and_flags_the_wrong_photo_note(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.drain()
        u = e.store.artifact(jid, "understanding")
        roles = {r["photo"]: r["role"] for r in u["photo_roles"]}
        self.assertEqual(roles, {1: "product_view", 2: "infographic", 3: "lifestyle"})
        self.assertTrue(any("photo 2" in m["where"] for m in u["mismatches"]), u["mismatches"])
        f = e.store.artifact(jid, "feasibility")
        self.assertTrue(any(r["photo"] == 2 and r["equipment_row"] == "EQ-006" for r in f["reference_risks"]))

    def test_accepting_the_alternative_lets_the_order_through_to_the_chef_without_the_cannot_action(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.drain()
        f = e.store.artifact(jid, "feasibility")
        e.orch.provide_input(jid, by=e.user["email"],
                             accepted_alternatives=[{"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"}
                                                    for x in f["alternatives"]])
        e.orch.step(jid)          # waiter folds the answer in
        e.orch.step(jid)          # pantry re-checks
        f2 = e.store.artifact(jid, "feasibility")
        self.assertIn(f2["verdict"], ("go", "go_with_limits"))
        self.assertFalse([a for a in f2["actions_needed"] if a["best_verdict"] == "cannot"])
        self.assertEqual(e.state(jid), "directing")
        self.assertEqual(provider_attempts(e, jid), [])


class MissingProductTruthPausesTheJob(unittest.TestCase):
    """Spec §11 test 2."""

    def test_an_order_needing_the_front_pocket_open_with_no_photo_of_it_asks_the_customer_for_one(self):
        e = Env()
        try:
            photos = [fx.BACKPACK_PHOTOS[0]]
            text = ("A 15-second film for our backpack. The camera circles the bag, then shows the front pocket open "
                    "with the bright yellow lining. It must show the front pocket open. Calm and premium.")
            jid = fx.submit_backpack_film(e, text=text, photos=photos, note="")
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_customer_input")
            f = e.store.artifact(jid, "feasibility")
            self.assertEqual(f["verdict"], "need_input")
            t = [x for x in f["product_truth"] if "pocket open" in x["part_state"]]
            self.assertTrue(t and t[0]["source"] == "none" and t[0]["covered_by_photo"] == "no")
            self.assertTrue(any("photo" in a and "pocket open" in a for a in f["ask_customer"]))
            self.assertEqual(provider_attempts(e, jid), [])
            self.assertIn("pocket open", e.store.job(jid)["pause_reason"])
            # the customer sends the photo; the job moves on
            e.svc.add_upload(e.user, jid, role="product", filename="open.png", label="front pocket open",
                             data=fx.with_shows(fx.make_png(64, 64, seed=40), "the front pocket open, yellow lining visible, product only"))
            e.orch.provide_input(jid, by=e.user["email"], note="here is the open pocket")
            e.orch.step(jid)
            e.orch.step(jid)
            self.assertIn(e.store.artifact(jid, "feasibility")["verdict"], ("go", "go_with_limits"))
            self.assertEqual(len(e.store.artifact(jid, "order_slip")["photos"]), 2)
        finally:
            e.close()


class CustomersExactWordsReachEveryAiCall(unittest.TestCase):
    """Spec §11 test 11 (front-of-house calls)."""

    def test_every_ai_call_carries_the_order_slip_words_byte_for_byte_and_records_its_card_version(self):
        e = Env()
        try:
            jid = fx.submit_backpack_film(e)
            e.drain()
            words = e.store.artifact(jid, "order_slip")["customer_exact_words"]
            self.assertEqual(words, fx.BACKPACK_FILM_ORDER)
            import hashlib
            sha = hashlib.sha256(words.encode()).hexdigest()
            calls = e.store.llm_calls(jid)
            self.assertEqual({c["worker"] for c in calls}, {"waiter", "pantry_checker"})
            for c in calls:
                self.assertEqual(c["exact_words_sha256"], sha)
                self.assertEqual(c["card_version"], 1)
                self.assertIn("CUSTOMER_EXACT_WORDS", c["context_kinds"])
            self.assertEqual(e.store.artifact(jid, "understanding")["customer_exact_words"], words)
            for name in ("understanding", "feasibility"):
                f = e.store.artifact(jid, name)
                self.assertEqual(f["rulebook_card_version"], 1)
                self.assertTrue(f["written_by"]["model"])
                self.assertEqual(f["form_version"], 1)
        finally:
            e.close()


@unittest.skipUnless(fx.evidence_dir(), "the private evidence repository is not checked out next to this one")
class OnTheVerbatimEvidence(unittest.TestCase):
    def test_the_real_order_and_photos_of_the_rejected_film_pause_at_the_pantry_with_no_spend(self):
        ev = fx.evidence_film(fx.evidence_dir())
        e = Env()
        try:
            b = ev["brief"]
            ups = [{"role": r, "filename": p.name, "data": p.read_bytes()} for r, p in ev["uploads"]]
            jid = e.svc.submit(e.user, title="evidence film", media="video", text=b["text"], formats=b["formats"], duration_s=b["duration_s"],
                               exact_strings=b["exact_strings"], product=b["product"], brand_colours=b["brand_colours"], max_budget_usd="15",
                               allow_preview_spend=True, uploads=ups, references_note=b["references_note"])
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_customer_input")
            f = e.store.artifact(jid, "feasibility")
            self.assertIn(f["verdict"], ("cannot_make", "need_input"))
            self.assertTrue(any(a["action_class"] == "hands_work_mechanism" and a["best_verdict"] == "cannot" for a in f["actions_needed"]))
            self.assertEqual(provider_attempts(e, jid), [])
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
