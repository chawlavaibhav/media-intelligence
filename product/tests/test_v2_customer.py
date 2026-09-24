"""The customer's experience (founder, 2026-09-23): "we don't show them the kitchen, but we keep them engaged" — and the
model trial for the judges ("the kitchen is independent of the models"). USD 0, simulated."""
import json
import re
import unittest
from unittest import mock

from product import customer
from product.qualification import judges
from product.tests import fixtures_v2 as fx
from product.tests.support import Env
from product.tests.test_web import Client
from product.web.app import App

# Words that belong to the kitchen, never to the customer's page.
KITCHEN = re.compile(r"\b(taster|chef|recipe checker|pantry|head cook|door guard|FILM-[ABC]|check_id|process:|SB-[A-Z]|"
                     r"gemini|gpt-|veo|nano-banana|haiku|EQ-\d|R[1-5]:|node_|frame_\d|shot_\d|llm|simulated reviewer)", re.I)


def kitchen_words(page: bytes) -> list:
    body = page.decode("utf-8", "replace")
    body = re.sub(r"<style>.*?</style>", "", body, flags=re.S)
    return sorted({m.group(0) for m in KITCHEN.finditer(re.sub(r"<[^>]+>", " ", body))})


class KeepTheCustomerEngaged(unittest.TestCase):
    def setUp(self):
        self.e = Env()
        self.app = App(self.e.s)
        self.c = Client(self.app)
        self.c.login("buyer@acme.test")

    def tearDown(self):
        self.e.close()

    def page(self, jid):
        return self.c.req("GET", f"/jobs/{jid}")["body"]

    def test_the_customer_sees_the_order_the_progress_and_the_plan_but_never_the_kitchen_at_any_step(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        seen = {}
        e.drain()
        seen["input"] = self.page(jid)
        f = e.store.artifact(jid, "feasibility")
        e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=[
            {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")
        seen["plan"] = self.page(jid)
        e.orch.approve(jid, by=e.user["email"], budget_usd="15")
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_master_approval")
        seen["look"] = self.page(jid)
        e.orch.approve_master(jid, by=e.user["email"])
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_taste")
        seen["taste"] = self.page(jid)
        e.orch.approve_taste(jid, by=e.user["email"])
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")
        seen["ready"] = self.page(jid)
        for step, page in seen.items():
            self.assertEqual(kitchen_words(page), [], step)
            self.assertIn(b"Progress", page, step)
            self.assertIn(b"Your order", page, step)
        self.assertIn(fx.BACKPACK_FILM_ORDER[:40].encode(), seen["plan"])          # the order, as the customer wrote it
        self.assertIn(b"Scene by scene", seen["plan"])
        self.assertIn(b"Recommended budget", seen["plan"])
        self.assertIn(b"What we checked", seen["ready"])
        steps = [p["text"] for p in customer.progress(e.store, jid)]
        for words in ("We've received your order.", "Our creative team is writing your plan.", "The look of your film is ready.",
                      "Giving everything a final check.", "It's ready for you."):
            self.assertIn(words, steps)
        self.assertTrue(any(re.match(r"Shot \d+ of \d+ is made\.", s) for s in steps))
        self.assertEqual([s for s in steps if KITCHEN.search(s)], [])

    def test_the_hardest_shot_is_tasted_before_the_rest_is_made_and_a_change_redoes_only_that_shot(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        e.drain()
        f = e.store.artifact(jid, "feasibility")
        e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=[
            {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
        e.drain()
        e.orch.approve(jid, by=e.user["email"], budget_usd="15")
        e.drain()
        e.orch.approve_master(jid, by=e.user["email"])
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_taste")
        from product.stations.head_cook import taste_nodes
        tasted = taste_nodes(e.orch, jid)
        self.assertTrue(tasted)
        risky = [n["node_id"] for n in e.store.nodes(jid) if n["kind"] == "shot" and json.loads(n["spec_json"]).get("risky")]
        self.assertEqual(tasted, sorted(risky) or tasted)
        others = [n["node_id"] for n in e.store.nodes(jid) if n["kind"] == "shot" and n["node_id"] not in tasted]
        paid = {a["node_id"] for a in e.store.attempts(jid) if a["category"] == "provider"}
        self.assertFalse(paid & set(others))                                        # nothing else bought before the taste
        before = e.store.node(jid, tasted[0])["selected_asset_id"]
        with self.assertRaises(ValueError):
            e.orch.change_taste(jid, by=e.user["email"], text="")
        e.orch.change_taste(jid, by=e.user["email"], text="make the laptop slide in more slowly")
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_taste")                            # a new version to taste
        self.assertNotEqual(e.store.node(jid, tasted[0])["selected_asset_id"], before)
        self.assertIn("more slowly", json.loads(e.store.node(jid, tasted[0])["spec_json"])["revision_note"])
        paid = {a["node_id"] for a in e.store.attempts(jid) if a["category"] == "provider"}
        self.assertFalse(paid & set(others))
        e.orch.approve_taste(jid, by=e.user["email"])
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")
        self.assertLessEqual(e.store.committed_usd(jid), __import__("decimal").Decimal("15"))

    def test_image_orders_have_no_taste_step(self):
        e = self.e
        jid = e.submit("image", text="A calm launch poster for our navy travel backpack; the bag must be the first thing you see.")
        e.drain()
        e.orch.approve(jid, by=e.user["email"], budget_usd="10")
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")

    def test_the_customer_is_told_every_time_it_is_their_turn_on_the_page_and_by_email_when_configured(self):
        e = self.e
        sent = []

        class FakeSMTP:
            def __init__(self, *a, **k): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def starttls(self): pass
            def login(self, *a): pass
            def send_message(self, msg): sent.append((msg["To"], msg["Subject"], msg.get_content()))

        with mock.patch.dict("os.environ", {"MI_SMTP_HOST": "smtp.test"}), mock.patch("smtplib.SMTP", FakeSMTP):
            jid = e.submit("image", text="A calm launch poster for our navy travel backpack; the bag must be the first thing you see.")
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="10")
            e.drain()
        states = [json.loads(x["data_json"])["state"] for x in e.store.events(jid, ("customer_notified",))]
        self.assertEqual(states, ["awaiting_approval", "ready_for_review"])
        self.assertEqual([t for t, _, _ in sent], ["buyer@acme.test", "buyer@acme.test"])
        self.assertIn("Your plan and a first look are ready", sent[0][1])
        self.assertIn(f"/jobs/{jid}", sent[0][2])
        self.assertEqual([m for m in sent if KITCHEN.search(m[1] + m[2])], [])
        # without a mail server: still recorded, never an error
        jid2 = e.submit("image", text="A calm launch poster for our navy travel backpack; the bag must be the first thing you see.")
        e.drain()
        last = json.loads(e.store.events(jid2, ("customer_notified",))[-1]["data_json"])
        self.assertFalse(last["emailed"])

    def test_the_reviewers_objections_and_a_failed_measurement_reach_the_customer_in_plain_words(self):
        from product.stations.chef import plain_objections
        rc = {"issues": [], "add_steps": [], "code_findings": [
            {"rule": "R1:cannot_on_route", "where": "shot 2 (FILM-C): The hands pull the zips", "finding": "hands_work_mechanism is CANNOT on FILM-C (EQ-001)"},
            {"rule": "R5:exact_copy_missing", "where": "copy deck", "finding": "the exact string 'Room' is missing"}]}
        words = plain_objections(rc)
        self.assertEqual(words, ["Shot 2 asks for something our video tools can't do reliably yet.", "Your exact words are missing from the plan."])
        self.assertEqual(customer.problem_words("exact_copy_match"), "This did not hold: your exact words appear exactly as you wrote them.")
        self.assertNotIn("process", customer.problem_words("process:paid_preflight"))


class ModelTrial(unittest.TestCase):
    """Founder 2026-09-23: judges are independent of the model — try several (cheap, open, strong) on the old cases."""

    def test_an_estimate_costs_nothing_and_prices_every_candidate_model_for_every_judge(self):
        rep = judges.trial(estimate_only=True, judges=("recipe_checker",))
        self.assertEqual(rep["spent_usd"], "0.000000")
        per = rep["judges"]["recipe_checker"]
        self.assertEqual(set(per), set(judges.TRIAL_MODELS["recipe_checker"]))
        for spec, r in per.items():
            self.assertGreater(float(r["estimated_usd"]), 0, spec)
            self.assertFalse(r["qualified"])

    def test_a_paid_trial_needs_the_founders_approval_on_record_and_skips_models_without_keys(self):
        with self.assertRaises(SystemExit):
            judges.trial(max_usd="5")
        with mock.patch.dict("os.environ", {}, clear=False):
            import os
            for kk in ("AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "GOOGLE_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY"):
                os.environ.pop(kk, None)
            rep = judges.trial(max_usd="5", approved_by="founder in chat, test", judges=("recipe_checker",))
        self.assertEqual(rep["spent_usd"], "0.000000")
        self.assertTrue(all("missing" in r["skipped"] for r in rep["judges"]["recipe_checker"].values()))


if __name__ == "__main__":
    unittest.main()
