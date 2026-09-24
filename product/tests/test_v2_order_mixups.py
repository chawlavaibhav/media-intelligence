"""Founder 2026-09-24: a beta customer's 20-s Reel was ordered with the form on "Image 1:1" and the waiter refused it.
A mix-up or an unsupported ask becomes one question to the customer; refused only if the answer still cannot be made."""
from __future__ import annotations

import unittest

from product.stations import waiter
from product.tests.support import Env

REEL = "A 20-second Instagram Reel for our backpack: a hand packs it, then the end card. Calm, premium."


class OrderMixups(unittest.TestCase):
    def setUp(self):
        self.e = Env()

    def tearDown(self):
        self.e.close()

    def test_a_reel_ordered_as_an_image_asks_the_customer_and_becomes_a_film(self):
        e = self.e
        jid = e.submit("image", text=REEL)
        e.drain()
        self.assertEqual(e.state(jid), "needs_answers")
        qs = e.store.artifact(jid, "understanding")["questions"]
        self.assertEqual(qs[0]["id"], waiter.MEDIA_Q)
        e.orch.answer(jid, {waiter.MEDIA_Q: "video, 9:16, 20 seconds"}, by=e.user["email"])
        e.drain()
        self.assertEqual(e.orch.order_slip(jid)["media"], "video")
        self.assertEqual(e.store.job(jid)["media"], "video")
        self.assertEqual(e.store.original_brief(jid)["text"], REEL)            # the customer's words stay as written
        self.assertNotEqual(e.state(jid), "refused")

    def test_an_unsupported_ask_is_offered_the_alternative_before_any_refusal(self):
        e = self.e
        jid = e.submit("video", text="A 20-second film where our founder speaks to camera with a voice-over and lip sync.")
        e.drain()
        self.assertEqual(e.state(jid), "needs_answers")
        self.assertEqual(e.store.artifact(jid, "understanding")["questions"][0]["id"], waiter.ALT_Q)

    def test_a_matching_order_asks_nothing_extra(self):
        e = self.e
        self.assertIsNone(waiter.media_mismatch({"media": "video", "formats": ["9:16"]}, REEL))
        self.assertIsNone(waiter.media_mismatch({"media": "image", "formats": ["1:1"]}, "A launch poster for our backpack"))


if __name__ == "__main__":
    unittest.main()
