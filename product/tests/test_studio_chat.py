"""The studio chat (founder 2026-09-24). A beta customer's 20-second Reel failed because the order form was left on
"Image 1:1". "No one fills a form like this." — "Let the user enter a prompt. The form was an internal instrument the
waiter fills for the kitchen." The customer's first message creates the job; the waiter fills the order from their
words and asks in the thread when something that matters is unclear; the job continues in the same thread. USD 0,
simulated, offline.

Kitchen v3 (2026-09-25): the film thread runs order -> recipe -> the dish (no pantry question, no look / first-shot
wait); a step error is shown with the chef's step. No test retired."""
import json
import re
import unittest
from unittest import mock

from product.stations import chef, waiter
from product.tests import fixtures_v2 as fx
from product.tests.support import Env
from product.tests.test_v2_customer import kitchen_words
from product.tests.test_web import Client
from product.web.app import App
from runtime.loop.synthetic import make_png

VAGUE = "an ad for my backpack"
REEL = ('A 20-second Reel for our Voyager 30L travel backpack by Acme, for young people who travel light. The words '
        '"Pack less. Go further." and "acme.in" must appear exactly.')
IMAGE_ORDER = "A calm launch poster for our navy travel backpack; the bag must be the first thing you see; no people."


class ChatBase(unittest.TestCase):
    def setUp(self):
        self.e = Env()
        self.app = App(self.e.s)
        self.c = Client(self.app)
        self.c.login("buyer@acme.test")

    def tearDown(self):
        self.e.close()

    def prompt(self, text, files=(), client=None):
        c = client or self.c
        r = c.req("POST", "/prompt", {"csrf": c.csrf("/"), "text": text}, files=[("photos", n, d, ct) for n, d, ct in files])
        self.assertTrue(r["status"].startswith("303"), (r["status"], r["body"][:300]))
        return dict(r["headers"])["Location"].split("/")[-1]

    def page(self, path, client=None):
        r = (client or self.c).req("GET", path)
        self.assertTrue(r["status"].startswith("200"), (path, r["status"], r["body"][:300]))
        return r["body"]

    def post(self, jid, action, form, files=None):
        r = self.c.req("POST", f"/jobs/{jid}/{action}", {"csrf": self.c.csrf(f"/jobs/{jid}"), **form}, files=files)
        self.assertTrue(r["status"].startswith("303"), (action, r["status"], r["body"][:300]))
        self.assertEqual(dict(r["headers"])["Location"], f"/jobs/{jid}")       # back to the same thread


class APromptStartsTheJob(ChatBase):
    def test_the_first_screen_is_a_greeting_and_one_prompt_box_with_a_paperclip(self):
        body = self.page("/")
        self.assertIn(b"What shall we make today?", body)
        self.assertIn(b'id="composer"', body)
        self.assertIn(b'action="/prompt"', body)
        self.assertIn(b'name="text"', body)
        self.assertIn(b'type="file"', body)
        for form_field in (b'name="media"', b'name="formats"', b"max_budget_usd", b'name="duration_s"', b"<table"):
            self.assertNotIn(form_field, body)                               # nothing to fill in, nothing to forget
        for path in ("/jobs/new", "/new"):
            self.assertEqual(dict(self.c.req("GET", path)["headers"])["Location"], "/")

    def test_the_first_message_creates_the_job_with_the_customers_words_and_photos_and_no_media_chosen(self):
        bag, logo = make_png(64, 64, seed=2), make_png(32, 16, seed=5)
        jid = self.prompt(REEL, files=[("bag.png", bag, "image/png"), ("logo.png", logo, "image/png")])
        brief = self.e.store.original_brief(jid)
        self.assertEqual(brief["text"], REEL)                                # verbatim: the kitchen's yardstick
        self.assertIsNone(brief["media"])                                    # the customer chose nothing
        self.assertEqual(brief["ordered_by"], "prompt")
        self.assertEqual(sorted(a["role"] for a in self.e.store.assets(jid, source="customer")), ["logo", "product"])
        self.assertEqual(self.e.store.job(jid)["budget_usd"], "3.000000")    # only the planning allowance is authorised
        page = self.page(f"/jobs/{jid}")
        self.assertIn(b"Reading your brief", page)
        self.assertIn(b"Pack less. Go further.", page)                       # their message, as the first bubble
        self.assertEqual(len(re.findall(rb'<img src="/assets/ast_\w+" alt="Your photo"', page)), 2)

    def test_the_waiter_fills_the_order_from_a_clear_prompt_and_records_it(self):
        jid = self.prompt(REEL, files=[("bag.png", make_png(64, 64, seed=2), "image/png")])
        self.e.drain()
        ch = self.e.store.artifact(jid, "order_change")
        self.assertEqual((ch["media"], ch["formats"], ch["duration_s"]), ("video", ["9:16"], 20.0))
        self.assertEqual(ch["exact_strings"], ["Pack less. Go further.", "acme.in"])
        self.assertFalse(ch["provisional"])
        self.assertEqual(ch["decided_by"], "waiter")
        slip = self.e.store.artifact(jid, "order_slip")
        self.assertEqual((slip["media"], slip["formats"], slip["duration_s"]), ("video", ["9:16"], 20.0))
        self.assertEqual(slip["customer_exact_words"], REEL)
        self.assertEqual(self.e.store.job(jid)["media"], "video")
        u = self.e.store.artifact(jid, "understanding")
        self.assertEqual(u["deliverable"]["media"], "video")
        self.assertNotIn(waiter.MEDIA_Q, [q["id"] for q in u["questions"]])   # clear words: nothing to ask
        self.assertNotEqual(self.e.state(jid), "needs_answers")
        self.assertIn(b"Instagram Reel", self.page(f"/jobs/{jid}"))

    def test_code_reads_the_words_even_when_the_model_guesses_otherwise(self):
        real = self.e.orch.sim.waiter__understanding

        def guesser(b, media):
            out = real(b, media)
            out["deliverable"] = {"media": "image", "formats": ["1:1"], "duration_s": None}
            return out
        with mock.patch.object(self.e.orch.sim, "waiter__understanding", guesser):
            jid = self.prompt(REEL)
            self.e.drain()
        self.assertEqual(self.e.store.job(jid)["media"], "video")
        self.assertEqual(self.e.store.artifact(jid, "understanding")["deliverable"]["media"], "video")

    def test_an_unclear_prompt_is_a_question_in_the_thread_and_the_reply_continues_the_job(self):
        jid = self.prompt(VAGUE)
        self.e.drain()
        self.assertEqual(self.e.state(jid), "needs_answers")
        self.assertTrue(self.e.store.artifact(jid, "order_change")["provisional"])
        qs = self.e.store.artifact(jid, "understanding")["questions"]
        self.assertEqual(qs[0]["id"], waiter.MEDIA_Q)
        page = self.page(f"/jobs/{jid}")
        self.assertIn(b"Should this be a Reel / short film, or a poster / image?", page)
        self.assertIn(b'action="/jobs/' + jid.encode() + b'/answer"', page)
        self.assertIn(b'name="reply"', page)
        self.assertEqual(kitchen_words(page), [])
        self.post(jid, "answer", {"reply": "A 15 second Reel, for young travellers"})
        self.assertEqual(self.e.store.artifact(jid, "answers")[waiter.MEDIA_Q], "A 15 second Reel, for young travellers")
        self.e.drain()
        ch = self.e.store.artifact(jid, "order_change")
        self.assertEqual((ch["media"], ch["duration_s"], ch["provisional"]), ("video", 15.0, False))
        self.assertNotIn(self.e.state(jid), ("needs_answers", "refused"))
        self.assertEqual(self.e.store.original_brief(jid)["text"], VAGUE)    # their words are never rewritten
        page = self.page(f"/jobs/{jid}")
        self.assertIn(b"A 15 second Reel, for young travellers", page)        # their reply, in the thread

    def test_a_poster_reply_makes_an_image_and_decide_for_me_uses_the_stated_default(self):
        jid = self.prompt(VAGUE)
        self.e.drain()
        self.post(jid, "answer", {"reply": "a poster please"})
        self.e.drain()
        self.assertEqual(self.e.store.job(jid)["media"], "image")
        jid2 = self.prompt(VAGUE)
        self.e.drain()
        self.post(jid2, "answer", {"delegate_all": "yes"})
        self.e.drain()
        ch = self.e.store.artifact(jid2, "order_change")
        self.assertEqual((ch["media"], ch["formats"], ch["provisional"]), ("image", ["1:1"], False))
        self.assertIn(b"Decide for me.", self.page(f"/jobs/{jid2}"))

    def test_an_empty_prompt_stays_on_the_first_screen(self):
        r = self.c.req("POST", "/prompt", {"csrf": self.c.csrf("/"), "text": "  "}, files=[])
        self.assertTrue(r["status"].startswith("400"))
        self.assertIn(b"What shall we make today?", r["body"])
        self.assertEqual(self.e.store.jobs_for_account(self.e.acct), [])

    def test_old_orders_are_untouched_by_prompt_orders(self):
        jid = self.e.submit("image", text=IMAGE_ORDER)
        self.e.drain()
        self.assertIsNone(self.e.store.artifact(jid, "order_change"))


class AccountsAreSeparate(ChatBase):
    def test_a_customer_cannot_see_or_post_to_another_accounts_job(self):
        jid = self.prompt(VAGUE, files=[("bag.png", make_png(64, 64, seed=2), "image/png")])
        self.e.drain()
        other = self.e.store.create_account("Other Co", ceiling_usd="20")
        self.e.customer("spy@other.test", other)
        spy = Client(self.app)
        spy.login("spy@other.test")
        tok = spy.csrf("/")
        self.assertTrue(spy.req("GET", f"/jobs/{jid}")["status"].startswith("404"))
        self.assertTrue(spy.req("GET", f"/jobs/{jid}/status")["status"].startswith("404"))
        self.assertTrue(spy.req("POST", f"/jobs/{jid}/answer", {"csrf": tok, "reply": "make it pink"})["status"].startswith("404"))
        up = self.e.store.assets(jid, source="customer")[0]["id"]
        self.assertTrue(spy.req("GET", f"/assets/{up}")["status"].startswith("404"))
        self.assertNotIn(jid.encode(), self.page("/", client=spy))
        self.assertIsNone(self.e.store.artifact(jid, "answers"))
        self.assertTrue(self.c.req("POST", "/prompt", {"csrf": "forged", "text": "x"})["status"].startswith("403"))


class TheJobIsAConversation(ChatBase):
    def forms(self, page, jid):
        return set(re.findall(rb'action="/jobs/' + jid.encode() + rb'/([\w-]+)"', page))

    def check(self, jid, *actions, words=()):
        page = self.page(f"/jobs/{jid}")
        self.assertEqual(kitchen_words(page), [], self.e.state(jid))
        self.assertNotIn(self.e.state(jid).encode(), page)                    # never a state name
        for a in actions:
            self.assertIn(a.encode(), self.forms(page, jid), (self.e.state(jid), a))
        for w in words:
            self.assertIn(w.encode(), page, (self.e.state(jid), w))
        return page

    def test_a_film_job_from_the_first_question_to_delivery_in_one_thread(self):
        e = self.e
        jid = fx.submit_backpack_film(e)
        page = self.check(jid, words=("Reading your brief",))
        self.assertIn(b'data-poll="/jobs/' + jid.encode() + b'/status"', page)          # refreshes itself while we work
        st = json.loads(self.c.req("GET", f"/jobs/{jid}/status")["body"])
        self.assertEqual((st["state"], st["line"]), ("submitted", "Reading your brief…"))
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")
        page = self.check(jid, "approve", "direction-change", "abandon", words=("Approve and start",))
        self.assertNotIn(b"data-poll", page)                                           # the customer's turn: no refreshing
        q = e.store.artifact(jid, "quote")
        self.assertIn(f'name="budget_usd" value="{q["recommended_budget_usd"]}"'.encode(), page)   # the exact price
        self.assertRegex(page, rb"about <strong>\$\d+\.\d\d</strong>")
        self.post(jid, "approve", {"budget_usd": q["recommended_budget_usd"]})
        self.assertEqual(e.store.job(jid)["budget_usd"][:4], q["recommended_budget_usd"][:4])
        self.assertIn(b"Approved", self.page(f"/jobs/{jid}"))
        e.drain()
        if e.state(jid) == "paused_budget":                                  # the exact price was a little short
            self.check(jid, "budget")
            e.svc.raise_budget(e.user, jid, "30")
            e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")                  # v3: no look / first-shot wait in between
        page = self.check(jid, "accept", "changes", "reject")
        self.assertIn(b"<video", page)
        self.post(jid, "accept", {})
        page = self.check(jid, words=("Download", "Delivered"))

    def test_an_image_job_shows_the_finished_pictures_large_and_takes_changes_by_reply(self):
        e = self.e
        jid = e.submit("image", text=IMAGE_ORDER)
        e.drain()
        e.orch.approve(jid, by=e.user["email"], budget_usd="10")
        e.drain()
        self.assertEqual(e.state(jid), "ready_for_review")
        page = self.check(jid, "accept", "changes", "reject", words=("Request changes",))
        for a in e.orch._final_assets(jid):
            self.assertIn(f'<img src="/assets/{a}" alt="Your finished ad"'.encode(), page)
        self.assertIn(b'name="change_1"', page)
        self.post(jid, "changes", {"change_1": "make the background a little warmer"})
        self.assertIn(b"make the background a little warmer", self.page(f"/jobs/{jid}"))

    def test_something_went_wrong_asks_try_again_or_stop(self):
        e = self.e
        from product.tests.test_v2_beta_rules import failing
        with mock.patch.object(chef, "direct", failing(chef.direct, 99)):
            jid = e.submit("image", text=IMAGE_ORDER)
            e.drain()
        self.assertEqual(e.state(jid), "needs_retry_decision")
        page = self.check(jid, "decide", words=("Try again", "Stop here"))
        self.assertIn(b'value="try_again"', page)
        self.assertIn(b'value="stop"', page)

    def test_a_failed_check_asks_the_customer(self):
        e = self.e
        from product import verify
        with mock.patch.object(verify, "exact_copy_match", side_effect=lambda *a, **k: {
                "check_id": "exact_copy_match", "control": "EXACT_COPY_MATCH", "status": "FAIL", "detail": "a letter is missing"}):
            jid = e.submit("image", text=IMAGE_ORDER)
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="10")
            e.drain()
        self.assertEqual(e.state(jid), "needs_customer_decision")
        page = self.check(jid, "decide", words=("Try once more",))
        self.assertIn(b'value="rework"', page)

    def test_needs_more_money_asks_to_continue(self):
        e = self.e
        jid = e.submit("image", text=IMAGE_ORDER)
        e.drain()
        e.orch.approve(jid, by=e.user["email"], budget_usd="0.01")
        e.drain()
        self.assertEqual(e.state(jid), "paused_budget")
        page = self.check(jid, "budget", words=("more", "Continue"))
        m = re.search(rb'name="budget_usd" value="([\d.]+)"', page)
        self.assertGreater(float(m.group(1)), 0.01)
        self.post(jid, "budget", {"budget_usd": m.group(1).decode()})
        self.assertNotEqual(e.state(jid), "paused_budget")

    def test_the_old_job_page_stays_at_details_and_the_old_form_at_new_form(self):
        e = self.e
        jid = e.submit("image", text=IMAGE_ORDER)
        self.assertIn(b"Progress", self.page(f"/jobs/{jid}/details"))
        for path in ("/jobs/new/form", "/new/form"):
            self.assertIn(b"What should we make?", self.page(path))
        tok = self.c.csrf("/jobs/new/form")
        r = self.c.req("POST", "/jobs", {"csrf": tok, "brief": "a poster", "media": "image", "max_budget_usd": "5", "allow_preview": "yes"},
                       files=[])
        self.assertTrue(r["status"].startswith("303"))


class HomeListsTheAds(ChatBase):
    def test_the_customers_ads_in_plain_words_under_the_prompt_box(self):
        jid = self.prompt(VAGUE)
        page = self.page("/")
        self.assertIn(f"/jobs/{jid}".encode(), page)
        self.assertIn(b"working on it", page)
        self.e.drain()
        self.assertIn(b"Waiting for your reply", self.page("/"))
        self.assertEqual(kitchen_words(self.page("/")), [])

    def test_operators_still_go_to_ops_and_see_the_full_page(self):
        jid = self.prompt(VAGUE)
        self.e.operator()
        op = Client(self.app)
        op.login("ops@mi.test")
        self.assertEqual(dict(op.req("GET", "/")["headers"])["Location"], "/ops")
        self.assertIn(b"Progress", self.page(f"/jobs/{jid}", client=op))

    def test_the_chat_script_is_served_from_our_own_site(self):
        r = self.c.req("GET", "/static/chat.js")
        self.assertTrue(r["status"].startswith("200"))
        self.assertIn("javascript", dict(r["headers"])["Content-Type"])
        csp = dict(self.c.req("GET", "/")["headers"])["Content-Security-Policy"]
        self.assertIn("script-src 'self'", csp)


if __name__ == "__main__":
    unittest.main()
