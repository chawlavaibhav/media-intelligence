import threading
import unittest
from decimal import Decimal

from product.store import BudgetExhausted, StaleState
from product.tests.support import Env


class ConcurrentReservation(unittest.TestCase):
    """MOKOBARA-ODYSSEY-007:LG-1 — att-020 was issued twice because ids were counted from a file appended at settle."""

    def setUp(self):
        self.e = Env()
        self.jid = self.e.submit()
        self.e.store.set_job(self.jid, budget_usd="1.000000", budget_authorised_by="test")

    def tearDown(self):
        self.e.close()

    def test_forty_concurrent_reservations_mint_unique_ids_and_never_cross_the_cap(self):
        ok, refused = [], []

        def go():
            try:
                ok.append(self.e.store.reserve(self.jid, route="nano-banana-2", category="provider", amount_usd="0.067"))
            except BudgetExhausted:
                refused.append(1)

        ts = [threading.Thread(target=go) for _ in range(40)]
        [t.start() for t in ts]
        [t.join() for t in ts]
        self.assertEqual(len(ok), len(set(ok)))
        self.assertEqual(len(ok), 14)                       # floor(1.00 / 0.067)
        self.assertEqual(len(refused), 26)
        self.assertLessEqual(self.e.store.committed_usd(self.jid), Decimal("1.00"))
        seqs = [r["seq"] for r in self.e.store.attempts(self.jid)]
        self.assertEqual(seqs, list(range(1, 15)))

    def test_failed_and_uncertain_attempts_stay_in_the_committed_total(self):
        a = self.e.store.reserve(self.jid, route="veo-3.1-fast-i2v", category="provider", amount_usd="0.40")
        self.e.store.settle(a, status="failed", settled_usd="0.40", failure_class="infrastructure_transient")
        b = self.e.store.reserve(self.jid, route="nano-banana-2", category="provider", amount_usd="0.067")
        self.e.store.settle(b, status="uncertain", settled_usd="0.067")
        self.assertEqual(self.e.store.committed_usd(self.jid), Decimal("0.467"))
        with self.assertRaises(StaleState):
            self.e.store.settle(a, status="ok", settled_usd="0.40")


class NoSpendWithoutAuthorisation(unittest.TestCase):
    def test_provider_reservation_needs_a_recorded_budget_authorisation(self):
        e = Env()
        try:
            jid = e.submit()
            e.store.set_job(jid, budget_authorised_by=None)
            with self.assertRaises(PermissionError):
                e.store.reserve(jid, route="nano-banana-2", category="provider", amount_usd="0.067")
            self.assertEqual(e.store.attempts(jid), [])
        finally:
            e.close()


class Transitions(unittest.TestCase):
    def test_compare_and_set_and_illegal_moves(self):
        e = Env()
        try:
            jid = e.submit()
            with self.assertRaises(StaleState):
                e.store.transition(jid, "producing", "checking", actor="t")      # not in producing
            with self.assertRaises(StaleState):
                e.store.transition(jid, "submitted", "accepted", actor="t")      # not a permitted move
            e.store.transition(jid, "submitted", "understanding", actor="t")
            self.assertEqual(e.state(jid), "understanding")
        finally:
            e.close()

    def test_the_original_brief_is_frozen_and_fingerprinted(self):
        e = Env()
        try:
            jid = e.submit()
            b = e.store.original_brief(jid)
            self.assertIn("backpack", b["text"])
            with e.store.tx() as c:
                c.execute("UPDATE jobs SET brief_json=replace(brief_json, 'backpack', 'suitcase') WHERE id=?", (jid,))
            with self.assertRaises(RuntimeError):
                e.store.original_brief(jid)
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
