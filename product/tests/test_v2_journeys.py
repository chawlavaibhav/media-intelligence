"""P1 v2 phase 8 — full simulated journeys through the web app (spec §13 step 8; checklist J3), and spec §11 test 11 across
every AI worker. Only HTTP requests by the customer and by the founder, plus the worker process; USD 0, real ffmpeg."""
import hashlib
import re
import unittest

from product import verify
from product.tests import fixtures_v2 as fx
from product.tests.support import Env
from product.tests.test_web import Client
from product.web.app import App
from runtime.loop.synthetic import make_png

ALL_AI_WORKERS = {"waiter", "pantry_checker", "chef", "recipe_checker", "small_taster", "big_taster", "diary_writer"}


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

    def founder_at_the_door(self, jid):
        """The founder, on the job page: confirm each person-check and waive what a simulation cannot verify, then release."""
        page = f"/ops/jobs/{jid}"
        g = self.e.store.artifact(jid, "gateway_report")
        for res in g["results"]:
            for b in res["blocking"]:
                if verify.attestable(b["check_id"]):
                    self.post(self.f, f"/ops/jobs/{jid}/attest", page, {"asset_id": res["asset_id"], "check_id": b["check_id"],
                                                                         "note": "DRY RUN — looked at the stand-in file; simulated media",
                                                                         "outcome": "PASS"})
                else:
                    self.post(self.f, f"/ops/jobs/{jid}/waive", page, {"asset_id": res["asset_id"], "check_id": b["check_id"],
                                                                        "reason": "DRY RUN — a simulation cannot verify this"})
        self.post(self.f, f"/ops/jobs/{jid}/release", page, {})

    def test_the_rejected_films_order_becomes_an_accepted_film_through_the_web_app_with_lessons_for_the_founder(self):
        e = self.e
        ups = [("product_photos", name, fx.with_shows(make_png(64, 64, seed=10 + i), shows), "image/png")
               for i, (name, shows) in enumerate(fx.BACKPACK_PHOTOS)] + [("logo", "logo.png", make_png(32, 16, seed=5), "image/png")]
        tok = self.c.csrf("/jobs/new")
        r = self.c.req("POST", "/jobs", {"csrf": tok, "brief": fx.BACKPACK_FILM_ORDER, "media": "video", "formats": ["9:16"],
                                         "duration_s": "30", "product_name": "Transit Backpack 30L", "brand": "Mokobara",
                                         "category": "backpack", "exact_text": "\n".join(fx.BACKPACK_EXACT), "brand_colours": "#101820",
                                         "max_budget_usd": "15", "allow_preview": "yes", "references_note": fx.BACKPACK_NOTE}, files=ups)
        jid = dict(r["headers"])["Location"].split("/")[-1]
        e.drain()
        page = self.c.req("GET", f"/jobs/{jid}")["body"]
        self.assertIn(b"We can&#39;t film", page)                                    # hands zipping the bag: cannot, with an alternative
        n = len(e.store.artifact(jid, "feasibility")["alternatives"])
        self.post(self.c, f"/jobs/{jid}/input", f"/jobs/{jid}", {**{f"alt_{i}": "yes" for i in range(n)}}, files=[])
        e.drain()
        self.assertEqual(e.state(jid), "paused_for_founder")                       # the recipe checker is not qualified
        self.post(self.f, f"/ops/jobs/{jid}/confirm_recipe", f"/ops/jobs/{jid}", {"reason": "Plan read: zips as stills; slides first."})
        self.assertEqual(e.state(jid), "awaiting_approval")
        self.post(self.c, f"/jobs/{jid}/approve", f"/jobs/{jid}", {"budget_usd": "15"})
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_master_approval")
        self.post(self.c, f"/jobs/{jid}/master", f"/jobs/{jid}", {})
        e.drain()
        self.assertEqual(e.state(jid), "operator_hold")
        self.founder_at_the_door(jid)
        self.assertEqual(e.state(jid), "ready_for_review")
        self.post(self.c, f"/jobs/{jid}/changes", f"/jobs/{jid}", {"target_1": "shot:2", "change_1": "a slower slide"})
        e.drain()
        self.assertEqual(e.state(jid), "operator_hold")
        self.founder_at_the_door(jid)
        self.post(self.c, f"/jobs/{jid}/accept", f"/jobs/{jid}", {})
        self.assertEqual(e.state(jid), "accepted")
        final = e.store.deliveries(jid)[0]["asset_id"]
        dl = self.c.req("GET", f"/assets/{final}/download")
        self.assertTrue(dl["status"].startswith("200"))
        self.assertEqual(hashlib.sha256(dl["body"]).hexdigest(), e.store.deliveries(jid)[0]["asset_sha256"])
        # the founder sees the lessons, the shelf proposals reach the customer
        self.assertIn(jid.encode(), self.f.req("GET", "/ops/lessons")["body"])
        self.assertIn(b"Approve", self.c.req("GET", "/shelf")["body"])
        # spec §11 test 11: every AI worker carried the order slip's words byte for byte
        sha = hashlib.sha256(fx.BACKPACK_FILM_ORDER.encode()).hexdigest()
        calls = e.store.llm_calls(jid)
        self.assertEqual({c["worker"] for c in calls}, ALL_AI_WORKERS)
        for c in calls:
            self.assertEqual(c["exact_words_sha256"], sha, c["worker"])
            self.assertIn("CUSTOMER_EXACT_WORDS", c["context_kinds"].split(","))
        # nothing reached the customer without the founder at the door, and no builder or script decided anything
        actors = {x["actor"] for x in e.store.events(jid) if x["kind"] == "founder_override"}
        self.assertEqual(actors, {"founder:founder@mi.test"})
        for w in e.store.q("SELECT by_user FROM waivers WHERE job_id=?", (jid,)):
            self.assertEqual(e.store.user(w["by_user"])["role"], "founder")

    def test_an_image_order_is_accepted_through_the_web_app(self):
        e = self.e
        tok = self.c.csrf("/jobs/new")
        r = self.c.req("POST", "/jobs", {"csrf": tok, "brief": "A calm launch poster for our navy travel backpack; the bag must be the "
                                                              "first thing you see; no people.", "media": "image", "formats": ["1:1", "4:5"],
                                         "product_name": "Transit Backpack 30L", "brand": "Mokobara", "category": "backpack",
                                         "exact_text": "Room for the long way home.", "brand_colours": "#101820", "max_budget_usd": "10",
                                         "allow_preview": "yes"},
                       files=[("product_photos", "front.png", fx.with_shows(make_png(64, 64, seed=3), fx.BACKPACK_PHOTOS[0][1]), "image/png"),
                              ("logo", "logo.png", make_png(32, 16, seed=5), "image/png")])
        jid = dict(r["headers"])["Location"].split("/")[-1]
        e.drain()
        self.post(self.f, f"/ops/jobs/{jid}/confirm_recipe", f"/ops/jobs/{jid}", {"reason": "Plan read: one clean picture per format."})
        page = self.c.req("GET", f"/jobs/{jid}")["body"]
        self.assertIn(b"Approve direction", page)
        prev = re.search(rb'/assets/(ast_\w+)"', page).group(1).decode()
        self.assertTrue(self.c.req("GET", f"/assets/{prev}")["status"].startswith("200"))
        self.post(self.c, f"/jobs/{jid}/approve", f"/jobs/{jid}", {"budget_usd": "10"})
        e.drain()
        self.assertEqual(e.state(jid), "operator_hold")
        self.founder_at_the_door(jid)
        self.post(self.c, f"/jobs/{jid}/accept", f"/jobs/{jid}", {})
        self.assertEqual(e.state(jid), "accepted")
        self.assertEqual(len(e.store.deliveries(jid)), 2)
        self.assertTrue(e.store.artifact(jid, "lessons"))


if __name__ == "__main__":
    unittest.main()
