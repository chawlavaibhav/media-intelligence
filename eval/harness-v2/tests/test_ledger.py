"""Battery ledger: EMP-001 semantics inherited, EVAL-040 caps over USD-equivalent across pools."""
import unittest
from decimal import Decimal
from pathlib import Path

from _support import NoNetworkTestCase, hv2_paths  # noqa: F401
import ledger as L
import spend_ledger as SL
from budget_guard import BudgetExceeded, NotAuthorised

CTX = dict(billing_pool="cash", currency="USD", amount_native=Decimal("0.053"), amount_usd_equiv=Decimal("0.053"))


class AuthorisationTest(NoNetworkTestCase):
    def test_m_no_live_ledger_from_the_committed_state(self):
        """Test (m): the committed example refuses, and no local file exists."""
        self.assertFalse(L.AUTH_LOCAL_PATH.exists(), "authorization.local.yaml must not exist in the committed state")
        with self.assertRaises(NotAuthorised):
            L.open_battery_ledger(root=self.tmp / "runs")
        with self.assertRaises(NotAuthorised):
            L.open_battery_ledger(root=self.tmp / "runs", authorisation_path=L.AUTH_EXAMPLE_PATH)
        st = L.authorisation_status(L.AUTH_EXAMPLE_PATH)
        self.assertFalse(st["paid_execution_permitted"])
        self.assertEqual(st["tranche_id"], "EVAL-040")

    def test_refusal_rules(self):
        p = self.tmp / "a.yaml"
        p.write_text("authorised: 'true'\ntranche_id: EVAL-040\nmax_consumed_api_spend_usd: 175\ntranche_caps_usd: {1a: 60, 1b: 115}\nretries_authorised: 0\n")
        self.assertTrue(any("boolean" in r for r in L.load_battery_authorisation(p).refusals))
        p.write_text("authorised: true\ntranche_id: EMP-001\nmax_consumed_api_spend_usd: 175\ntranche_caps_usd: {1a: 60, 1b: 115}\nretries_authorised: 0\n")
        self.assertTrue(any("tranche_id" in r for r in L.load_battery_authorisation(p).refusals))
        p.write_text("authorised: true\ntranche_id: EVAL-040\nmax_consumed_api_spend_usd: 176\ntranche_caps_usd: {1a: 60, 1b: 115}\nretries_authorised: 0\n")
        self.assertTrue(any("exceeds" in r for r in L.load_battery_authorisation(p).refusals))
        p.write_text("authorised: true\ntranche_id: EVAL-040\nmax_consumed_api_spend_usd: 175\ntranche_caps_usd: {1a: 60, 1b: 115}\nretries_authorised: 1\n")
        self.assertTrue(any("retries" in r for r in L.load_battery_authorisation(p).refusals))
        p.write_text("authorised: true\ntranche_id: EVAL-040\nmax_consumed_api_spend_usd: 175\ntranche_caps_usd: {1a: 60}\nretries_authorised: 0\n")
        self.assertTrue(any("exactly" in r for r in L.load_battery_authorisation(p).refusals))
        p.write_text("authorised: true\ntranche_id: EVAL-040\nmax_consumed_api_spend_usd: 175\ntranche_caps_usd: {1a: 60, 1b: 115}\nretries_authorised: 0\n")
        self.assertEqual(L.load_battery_authorisation(p).refusals, ())


class LedgerTest(NoNetworkTestCase):
    def test_subclasses_not_copies(self):
        self.assertTrue(issubclass(L.BatteryRun, SL.TrancheRun))
        self.assertTrue(issubclass(L.BatteryBudget, SL.TrancheBudget))
        self.assertTrue(issubclass(L.PoolStageBudget, SL.StageBudget))
        self.assertIs(L.BatteryBudget.records, SL.TrancheBudget.records)
        self.assertIs(L.BatteryBudget._append, SL.TrancheBudget._append)
        self.assertIs(L.BatteryBudget.correct, SL.TrancheBudget.correct)
        self.assertIs(L.PoolStageBudget.release, SL.StageBudget.release)

    def test_run_record_carries_eval_040_identity_and_caps(self):
        b = self.make_ledger()
        self.assertEqual(b.run.record["tranche_id"], "EVAL-040")
        self.assertEqual(b.run.ceiling_usd, Decimal("175.00"))
        self.assertEqual(b.run.tranche_caps, {"1a": Decimal("60.00"), "1b": Decimal("115.00")})
        with self.assertRaises(SL.LedgerCorrupt):
            SL.TrancheRun.open(self.tmp / "runs", "run-test")          # EMP-001 refuses it, correctly
        reopened = L.BatteryRun.open(self.tmp / "runs", "run-test")
        self.assertEqual(reopened.ceiling_usd, Decimal("175.00"))

    def test_reserve_then_record_with_pool_fields(self):
        b = self.make_ledger()
        t = b.tranche("1a")
        rid = t.reserve(Decimal("0.053"), case_id="IMG-CORE-01", **CTX)
        self.assertTrue(rid.startswith("res-"))
        self.assertEqual(b.pending_usd(), Decimal("0.053"))
        ref = t.record(Decimal("0.053"), billing_state="reported", **CTX)
        self.assertTrue(ref.startswith("cost-"))
        self.assertEqual(b.committed_usd(), Decimal("0.053"))
        self.assertEqual(b.pending_usd(), Decimal("0"))
        rows = b.records()
        self.assertEqual([r["type"] for r in rows], ["reservation", "spend"])
        for r in rows:
            self.assertEqual(r["billing_pool"], "cash")
            self.assertEqual(r["currency"], "USD")

    def test_every_row_needs_pool_and_currency(self):
        t = self.make_ledger().tranche("1a")
        with self.assertRaises(ValueError):
            t.reserve(Decimal("0.05"))
        with self.assertRaises(ValueError):
            t.reserve(Decimal("0.05"), billing_pool="crypto", currency="USD", amount_native="0.05", amount_usd_equiv="0.05")
        with self.assertRaises(ValueError):
            t.reserve(Decimal("0.05"), billing_pool="cash", currency="USD", amount_native="0.05", amount_usd_equiv="0.04")

    def test_inr_reservation_counts_against_the_usd_cap(self):
        b = self.make_ledger(ceiling="1.00", caps=("0.50", "0.50"))
        t = b.tranche("1b")
        inr = Decimal("0.063")
        usd = (inr / Decimal("95.4211")).quantize(Decimal("0.000001"))
        t.reserve(usd, billing_pool="sarvam_credits", currency="INR", amount_native=inr, amount_usd_equiv=usd)
        pools = b.totals_by_pool()
        self.assertEqual(pools["sarvam_credits"]["native"], inr)
        self.assertEqual(pools["sarvam_credits"]["usd_equiv"], usd)
        self.assertEqual(b.spent_usd(), usd)
        # a huge INR reservation cannot slip past the USD-equivalent cap
        big_inr = Decimal("95.4211") * 2
        with self.assertRaises(BudgetExceeded):
            t.reserve(Decimal("2.000000"), billing_pool="sarvam_credits", currency="INR", amount_native=big_inr, amount_usd_equiv=Decimal("2.000000"))

    def test_ceiling_and_tranche_caps(self):
        b = self.make_ledger(ceiling="1.00", caps=("0.30", "0.90"))
        with self.assertRaises(BudgetExceeded):
            b.tranche("1a").reserve(Decimal("0.31"), billing_pool="cash", currency="USD", amount_native="0.31", amount_usd_equiv="0.31")
        b.tranche("1a").reserve(Decimal("0.30"), billing_pool="cash", currency="USD", amount_native="0.30", amount_usd_equiv="0.30")
        with self.assertRaises(BudgetExceeded):
            b.tranche("1b").reserve(Decimal("0.71"), billing_pool="credits", currency="USD", amount_native="0.71", amount_usd_equiv="0.71")
        self.assertEqual(b.tranche("1b").remaining_usd(), Decimal("0.70"))
        with self.assertRaises(ValueError):
            b.tranche("qualification")

    def test_release_and_corrupt_ledger_are_inherited(self):
        b = self.make_ledger()
        t = b.tranche("1a")
        t.reserve(Decimal("0.05"), billing_pool="cash", currency="USD", amount_native="0.05", amount_usd_equiv="0.05")
        t.release()
        self.assertEqual(b.spent_usd(), Decimal("0"))
        with b.run.ledger_path.open("a") as fh:
            fh.write("not json\n")
        with self.assertRaises(SL.LedgerCorrupt):
            L.BatteryBudget(L.BatteryRun.open(self.tmp / "runs", "run-test")).records()

    def test_correction_is_additive_and_never_negative(self):
        b = self.make_ledger()
        with self.assertRaises(ValueError):
            b.correct("1a", Decimal("-1"), "no")
        b.correct("1a", Decimal("0.10"), "billing evidence")
        self.assertEqual(b.committed_usd(), Decimal("0.10"))


if __name__ == "__main__":
    unittest.main()
