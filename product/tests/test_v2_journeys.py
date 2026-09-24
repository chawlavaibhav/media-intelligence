"""P1 v2 phase 8 — full simulated journeys through the web app (spec §13 step 8; checklist J3), and spec §11 test 11 across
every AI worker. Only HTTP requests by the customer and by the founder, plus the worker process; USD 0, real ffmpeg.

Kitchen v3 (2026-09-25): the film journey follows the v3 line — no pantry question, no look / first-shot wait; the
AI workers are the waiter, the chef, the head cook, the gatekeeper and the diary writer. No test retired."""
import hashlib
import json
import re
import unittest

from product.tests import fixtures_v2 as fx
from product.tests.support import Env
from product.tests.test_web import Client
from product.web.app import App
from runtime.loop.synthetic import make_png

from product import rulebook

ALL_AI_WORKERS = set(rulebook.AI_WORKERS)


class WebJourneys(unittest.TestCase):
    def setUp(self):
        self.e = Env()
        self.app = App(self.e.s)
        self.e.founder_session()
        self.c = Client(self.app); self.c.login("buyer@acme.test")
        self.f = Client(self.app); self.f.login("founder@mi.test")

    def tearDown(self):
        self.e.close()

    def post(self, client, path, page, form, files=None):
        tok = client.csrf(page)
        r = client.req("POST", path, {"csrf": tok, **form}, files=files)
        self.assertTrue(r["status"].startswith("303"), (path, r["status"], r["body"][:400]))
        return r

    def test_the_rejected_films_order_becomes_an_accepted_film_through_the_web_app_with_lessons_for_the_founder(self):
        """Kitchen v3: nobody waits for the founder — the customer approves the recipe and receives the dish."""
        e = self.e
        ups = [("product_photos", name, fx.with_shows(make_png(64, 64, seed=10 + i), shows), "image/png")
               for i, (name, shows) in enumerate(fx.BACKPACK_PHOTOS)] + [("logo", "logo.png", make_png(32, 16, seed=5), "image/png")]
        tok = self.c.csrf("/jobs/new/form")
        r = self.c.req("POST", "/jobs", {"csrf": tok, "brief": fx.BACKPACK_FILM_ORDER, "media": "video", "formats": ["9:16"],
                                         "duration_s": "30", "product_name": "Transit Backpack 30L", "brand": "Mokobara",
                                         "category": "backpack", "exact_text": "\n".join(fx.BACKPACK_EXACT), "brand_colours": "#101820",
                                         "max_budget_usd": "15", "allow_preview": "yes", "references_note": fx.BACKPACK_NOTE}, files=ups)
        jid = dict(r["headers"])["Location"].split("/")[-1]
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")                        # waiter -> chef -> the customer
        page = self.c.req("GET", f"/jobs/{jid}/details")["body"]
        self.assertIn(b"Approve direction", page)
        self.post(self.c, f"/jobs/{jid}/approve", f"/jobs/{jid}", {"budget_usd": "15"})
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")
        self.assertIn(b"your look is the final check", self.c.req("GET", f"/jobs/{jid}/details")["body"])
        self.post(self.c, f"/jobs/{jid}/changes", f"/jobs/{jid}", {"target_1": "shot:1", "change_1": "a slower slide"})
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")
        self.post(self.c, f"/jobs/{jid}/accept", f"/jobs/{jid}", {})
        self.assertEqual(e.state(jid), "accepted")
        final = e.store.deliveries(jid)[0]["asset_id"]
        dl = self.c.req("GET", f"/assets/{final}/download")
        self.assertTrue(dl["status"].startswith("200"))
        self.assertEqual(hashlib.sha256(dl["body"]).hexdigest(), e.store.deliveries(jid)[0]["asset_sha256"])
        # the founder sees what was learned (applied automatically, undoable), the shelf proposals reach the customer
        self.assertIn(jid.encode(), self.f.req("GET", "/ops/digest")["body"])
        self.assertIn(b"Approve", self.c.req("GET", "/shelf")["body"])
        # spec §11 test 11: every AI worker carried the order slip's words byte for byte
        sha = hashlib.sha256(fx.BACKPACK_FILM_ORDER.encode()).hexdigest()
        calls = e.store.llm_calls(jid)
        self.assertEqual({c["worker"] for c in calls}, ALL_AI_WORKERS)
        for c in calls:
            self.assertEqual(c["exact_words_sha256"], sha, c["worker"])
            self.assertIn("CUSTOMER_EXACT_WORDS", c["context_kinds"].split(","))
        # nobody waited for the founder, no builder or script decided anything, and the customer's acceptance is recorded
        # against every judgement check the unqualified judges could not settle
        self.assertFalse([x for x in e.store.events(jid, ("state",)) if json.loads(x["data_json"]).get("to") in
                          ("paused_for_founder", "operator_hold")])
        self.assertEqual(e.store.overrides(jid), [])
        self.assertEqual(e.store.q("SELECT * FROM waivers WHERE job_id=?", (jid,)), [])
        rows = {r["check_id"]: r for r in e.store.checks(final)}
        for cid in ("independent_review", "audio_heard_by_person"):
            self.assertEqual(rows[cid]["runner"], "customer:buyer@acme.test", cid)

    def test_an_image_order_is_accepted_through_the_web_app(self):
        e = self.e
        tok = self.c.csrf("/jobs/new/form")
        r = self.c.req("POST", "/jobs", {"csrf": tok, "brief": "A calm launch poster for our navy travel backpack; the bag must be the "
                                                              "first thing you see; no people.", "media": "image", "formats": ["1:1", "4:5"],
                                         "product_name": "Transit Backpack 30L", "brand": "Mokobara", "category": "backpack",
                                         "exact_text": "Room for the long way home.", "brand_colours": "#101820", "max_budget_usd": "10",
                                         "allow_preview": "yes"},
                       files=[("product_photos", "front.png", fx.with_shows(make_png(64, 64, seed=3), fx.BACKPACK_PHOTOS[0][1]), "image/png"),
                              ("logo", "logo.png", make_png(32, 16, seed=5), "image/png")])
        jid = dict(r["headers"])["Location"].split("/")[-1]
        e.drain()
        page = self.c.req("GET", f"/jobs/{jid}/details")["body"]
        self.assertIn(b"Approve direction", page)
        prev = re.search(rb'/assets/(ast_\w+)"', page).group(1).decode()
        self.assertTrue(self.c.req("GET", f"/assets/{prev}")["status"].startswith("200"))
        self.post(self.c, f"/jobs/{jid}/approve", f"/jobs/{jid}", {"budget_usd": "10"})
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")
        self.post(self.c, f"/jobs/{jid}/accept", f"/jobs/{jid}", {})
        self.assertEqual(e.state(jid), "accepted")
        self.assertEqual(len(e.store.deliveries(jid)), 2)
        self.assertTrue(e.store.artifact(jid, "lessons"))


if __name__ == "__main__":
    unittest.main()
