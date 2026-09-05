"""Battery ledger after Auditor AF-1 / AF-2: every number comes from the authorisation file (the signed record's
machine_authorisation block); no ceiling constant exists in code; BatteryRun.open re-validates against the file
and never takes a ceiling from run.json; an INR sub-cap applies natively to the Sarvam pool."""
import hashlib
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, hv2_paths  # noqa: F401
import ledger as L
import spend_ledger as SL
from budget_guard import BudgetExceeded, NotAuthorised

CTX = dict(billing_pool="cash", currency="USD", amount_native=Decimal("0.053"), amount_usd_equiv=Decimal("0.053"))
FIELDS = ("tranche_id", "authorised", "item_basis_commit", "price_basis_roster_sha256", "max_consumed_usd_equivalent",
          "cap_1a_usd", "cap_1b_usd", "sarvam_cap_inr", "retries_authorised", "execution_time_route_price_verification",
          "images_before_video", "approved_by", "approved_at")


class AuthorisationTest(NoNetworkTestCase):
    def test_m_no_live_ledger_from_the_committed_state(self):
        self.assertFalse(L.AUTH_LOCAL_PATH.exists(), "authorization.local.yaml must not exist in the committed state")
        with self.assertRaises(NotAuthorised):
            L.open_battery_ledger(root=self.tmp / "runs")
        with self.assertRaises(NotAuthorised):
            L.open_battery_ledger(root=self.tmp / "runs", authorisation_path=L.AUTH_EXAMPLE_PATH)
        st = L.authorisation_status(L.AUTH_EXAMPLE_PATH)
        self.assertFalse(st["paid_execution_permitted"])
        ex = yaml.safe_load(L.AUTH_EXAMPLE_PATH.read_text())["machine_authorisation"]
        self.assertEqual(tuple(ex), FIELDS, "the example file carries exactly the signed record's field names, in order")
        self.assertIs(ex["authorised"], False)

    def test_af1_no_hard_coded_ceiling_anywhere(self):
        src = Path(L.__file__).read_text()
        self.assertFalse(hasattr(L, "MAX_PROPOSED_CEILING_USD"))
        self.assertIsNone(re.search(r'Decimal\("(1[0-9]{2}|[2-9][0-9]{2})(\.[0-9]+)?"\)', src), "no USD ceiling literal in ledger.py")
        self.assertEqual(L.AUTH_FIELDS, FIELDS)

    def test_af1_refusal_rules(self):
        good = self.write_auth()
        self.assertEqual(L.load_battery_authorisation(good).refusals, ())
        cases = {
            "authorised": ("true", "boolean"), "tranche_id": ("EVAL-040", "tranche_id"), "approved_by": ("", "approved_by"),
            "approved_at": (None, "approved_at"), "price_basis_roster_sha256": ("0" * 64, "roster"),
            "retries_authorised": (1, "retries"), "max_consumed_usd_equivalent": (None, "max_consumed"),
            "cap_1a_usd": ("500.00", "cap_1a"), "cap_1b_usd": (None, "cap_1b"), "sarvam_cap_inr": ("-1", "sarvam_cap_inr"),
            "execution_time_route_price_verification": ("optional", "execution_time"), "item_basis_commit": ("", "item_basis"),
            "images_before_video": ("yes", "images_before_video"),
        }
        for field, (bad, needle) in cases.items():
            with self.subTest(field=field):
                p = self.write_auth(name=f"bad-{field}.yaml", **{field: bad})
                refusals = L.load_battery_authorisation(p).refusals
                self.assertTrue(any(needle in r for r in refusals), (field, refusals))
        # a flat file without the machine_authorisation block is refused too
        flat = self.tmp / "flat.yaml"
        flat.write_text("authorised: true\n")
        self.assertTrue(L.load_battery_authorisation(flat).refusals)

    def test_af1_roster_sha_is_checked_against_the_roster_on_disk(self):
        p = self.write_auth(price_basis_roster_sha256="99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46")
        auth = L.load_battery_authorisation(p)
        on_disk = hashlib.sha256(Path(hv2_paths.ROSTER).read_bytes()).hexdigest()
        self.assertEqual(auth.refusals == (), on_disk == "99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46")
        self.assertEqual(auth.roster_sha256_on_disk, on_disk)


class LedgerTest(NoNetworkTestCase):
    def test_subclasses_not_copies(self):
        self.assertTrue(issubclass(L.BatteryRun, SL.TrancheRun))
        self.assertTrue(issubclass(L.BatteryBudget, SL.TrancheBudget))
        self.assertTrue(issubclass(L.PoolStageBudget, SL.StageBudget))
        self.assertIs(L.BatteryBudget.records, SL.TrancheBudget.records)
        self.assertIs(L.BatteryBudget._append, SL.TrancheBudget._append)
        self.assertIs(L.BatteryBudget.correct, SL.TrancheBudget.correct)
        self.assertIs(L.PoolStageBudget.release, SL.StageBudget.release)

    def test_run_carries_the_files_numbers(self):
        b = self.make_ledger()
        self.assertEqual(b.run.record["tranche_id"], "EVAL-040-TRANCHE-1")
        self.assertEqual(b.run.ceiling_usd, Decimal("200.00"))
        self.assertEqual(b.run.tranche_caps, {"1a": Decimal("85.00"), "1b": Decimal("115.00")})
        self.assertEqual(b.run.sarvam_cap_inr, Decimal("5.00"))
        with self.assertRaises(SL.LedgerCorrupt):
            SL.TrancheRun.open(self.tmp / "runs", "run-test")

    def test_af2_open_revalidates_and_never_trusts_run_json(self):
        b = self.make_ledger()
        auth = L.load_battery_authorisation(self.tmp / "auth.yaml")
        with self.assertRaises(TypeError):
            L.BatteryRun.open(self.tmp / "runs", "run-test")                    # an authorisation is mandatory
        rj = b.run.run_json_path
        rec = json.loads(rj.read_text())
        rec["total_ceiling_usd"] = "9999"
        rj.write_text(json.dumps(rec))
        with self.assertRaises(NotAuthorised):
            L.BatteryRun.open(self.tmp / "runs", "run-test", auth)               # recorded ceiling above the file's
        rec["total_ceiling_usd"] = "50"
        rec["tranche_caps_usd"] = {"1a": "1", "1b": "1"}
        rj.write_text(json.dumps(rec))
        run = L.BatteryRun.open(self.tmp / "runs", "run-test", auth)
        self.assertEqual(run.ceiling_usd, Decimal("200.00"))                    # from the file, not run.json
        self.assertEqual(run.tranche_caps["1a"], Decimal("85.00"))
        refused = L.load_battery_authorisation(self.write_auth(name="off.yaml", authorised=False))
        with self.assertRaises(NotAuthorised):
            L.BatteryRun.open(self.tmp / "runs", "run-test", refused)
        (self.tmp / "auth.yaml").unlink()
        with self.assertRaises(NotAuthorised):
            L.open_battery_ledger(root=self.tmp / "runs", run_id="run-test", authorisation_path=self.tmp / "auth.yaml")

    def test_reserve_then_record_with_pool_fields(self):
        b = self.make_ledger()
        t = b.tranche("1a")
        rid = t.reserve(Decimal("0.053"), case_id="IMG-CORE-01", **CTX)
        self.assertTrue(rid.startswith("res-"))
        self.assertEqual(b.pending_usd(), Decimal("0.053"))
        ref = t.record(Decimal("0.053"), billing_state="reported", **CTX)
        self.assertTrue(ref.startswith("cost-"))
        self.assertEqual(b.committed_usd(), Decimal("0.053"))
        for r in b.records():
            self.assertEqual((r["billing_pool"], r["currency"]), ("cash", "USD"))

    def test_every_row_needs_pool_and_currency(self):
        t = self.make_ledger().tranche("1a")
        with self.assertRaises(ValueError):
            t.reserve(Decimal("0.05"))
        with self.assertRaises(ValueError):
            t.reserve(Decimal("0.05"), billing_pool="crypto", currency="USD", amount_native="0.05", amount_usd_equiv="0.05")
        with self.assertRaises(ValueError):
            t.reserve(Decimal("0.05"), billing_pool="cash", currency="USD", amount_native="0.05", amount_usd_equiv="0.04")

    def test_inr_counts_against_the_usd_cap_and_the_inr_sub_cap(self):
        b = self.make_ledger(ceiling="1.00", caps=("0.50", "0.50"), inr_cap="0.50")
        t = b.tranche("1b")
        inr = Decimal("0.42")
        usd = (inr / Decimal("95.4211")).quantize(Decimal("0.000001"))
        t.reserve(usd, billing_pool="sarvam_credits", currency="INR", amount_native=inr, amount_usd_equiv=usd)
        self.assertEqual(b.totals_by_pool()["sarvam_credits"]["native"], inr)
        with self.assertRaises(BudgetExceeded):                                 # INR 0.42 + 0.20 > the INR sub-cap 0.50
            t.reserve(Decimal("0.002096"), billing_pool="sarvam_credits", currency="INR", amount_native=Decimal("0.20"), amount_usd_equiv=Decimal("0.002096"))
        with self.assertRaises(BudgetExceeded):                                 # a huge INR amount cannot slip past the USD cap either
            t.reserve(Decimal("2.000000"), billing_pool="sarvam_credits", currency="INR", amount_native=Decimal("190.8422"), amount_usd_equiv=Decimal("2.000000"))

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
        auth = L.load_battery_authorisation(self.tmp / "auth.yaml")
        with self.assertRaises(SL.LedgerCorrupt):
            L.BatteryBudget(L.BatteryRun.open(self.tmp / "runs", "run-test", auth)).records()

    def test_correction_is_additive_and_never_negative(self):
        b = self.make_ledger()
        with self.assertRaises(ValueError):
            b.correct("1a", Decimal("-1"), "no")
        b.correct("1a", Decimal("0.10"), "billing evidence")
        self.assertEqual(b.committed_usd(), Decimal("0.10"))


if __name__ == "__main__":
    unittest.main()
