import unittest

from product.dispatch import DispatchFailed, GuardRefused
from product.providers import SimulatedProviders
from product.tests.support import Env

GUARD = {"exact_strings": ["Pack less. Go further."], "forbidden_words": ["Acme"]}


class GuardBeforeReserve(unittest.TestCase):
    """RENTOK-GAME-B-005:T1 / VALIDATE_BEFORE_RESERVE: a refused request costs nothing and leaves no attempt."""

    def setUp(self):
        self.e = Env()
        self.jid = self.e.submit()

    def tearDown(self):
        self.e.close()

    def _img(self, prompt):
        return self.e.orch.dispatch.image(self.jid, "n1", prompt=prompt, aspect="1:1", refs=[], guard=GUARD)

    def test_brand_word_exact_copy_and_missing_no_lettering_clause_are_refused_before_reserve(self):
        for p in ("An Acme backpack on a rock. No text.", "A backpack. Pack less. Go further. No text.", "A backpack on a rock."):
            with self.assertRaises(GuardRefused):
                self._img(p)
        self.assertEqual(self.e.store.attempts(self.jid), [])

    def test_a_clean_prompt_reserves_settles_and_registers_the_asset(self):
        aid = self._img("A navy backpack on a rock at dawn. No text, no lettering.")
        a = self.e.store.attempts(self.jid)
        self.assertEqual([(x["status"], x["route"]) for x in a], [("ok", "nano-banana-2")])
        self.assertEqual(self.e.store.asset(aid)["attempt_id"], a[0]["id"])


class FailureClassification(unittest.TestCase):
    """UPWORK-INTRO-001:SD-09/SD-10, MOKOBARA-ODYSSEY-007:DF-5: an outage is not a bad draw."""

    def test_503_is_transient_charged_and_retryable_400_is_refusal_not_charged(self):
        e = Env(fault_injection={"image": [503, 400]})
        try:
            jid = e.submit()
            for want_retry in (True, False):
                with self.assertRaises(DispatchFailed) as cm:
                    e.orch.dispatch.image(jid, "n1", prompt="A bag. No text.", aspect="1:1", refs=[], guard=GUARD)
                self.assertEqual(cm.exception.retryable, want_retry)
            rows = e.store.attempts(jid)
            self.assertEqual([r["failure_class"] for r in rows], ["infrastructure_transient", "provider_refusal"])
            self.assertEqual([r["settled_usd"] for r in rows], ["0.067000", "0.000000"])
            self.assertTrue(all(r["counts_against_route"] == 0 for r in rows))
        finally:
            e.close()


class Recovery(unittest.TestCase):
    """A worker that died between reserve and settle: resume a known operation, never silently re-send."""

    def test_a_clip_with_an_operation_id_is_recovered_by_polling_and_a_still_without_one_is_uncertain(self):
        e = Env()
        try:
            jid = e.submit()
            p: SimulatedProviders = e.orch.dispatch.p
            a1 = e.store.reserve(jid, route="veo-3.1-fast-i2v", category="provider", amount_usd="0.60", node_id="clip_b1")
            op = p.video_submit("x", ("image/png", b""), 6, "9:16", None).request_ref
            e.store.mark_request(a1, op)
            a2 = e.store.reserve(jid, route="nano-banana-2", category="provider", amount_usd="0.067", node_id="still_b2")
            out = dict((a, o) for a, o, _ in e.orch.dispatch.recover(jid))
            self.assertEqual(out, {a1: "recovered", a2: "uncertain"})
            rows = {r["id"]: r for r in e.store.attempts(jid)}
            self.assertEqual(rows[a2]["status"], "uncertain")
            self.assertEqual(e.store.committed_usd(jid), __import__("decimal").Decimal("0.667"))
            self.assertEqual(len(e.store.attempts(jid)), 2)                      # nothing re-sent
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
