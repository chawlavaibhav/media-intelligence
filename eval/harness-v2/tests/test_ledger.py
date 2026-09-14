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


def cash(amount: Decimal) -> dict:
    """The pool fields every row needs, for a plain USD cash amount."""
    return dict(billing_pool="cash", currency="USD", amount_native=amount, amount_usd_equiv=amount)
FIELDS = ("tranche_id", "authorised", "item_basis_commit", "price_basis_roster_sha256", "max_consumed_usd_equivalent",
          "cap_1a_usd", "cap_1b_usd", "sarvam_cap_inr", "retries_authorised", "execution_time_route_price_verification",
          "images_before_video", "approved_by", "approved_at")


class AuthorisationTest(NoNetworkTestCase):
    def test_m_no_live_ledger_from_the_committed_state(self):
        # The committed state carries no authorisation file (it is gitignored). On a machine where the
        # Controller has materialised one from a signed record, that file is legitimately present, so the
        # "committed state" is modelled by a path that does not exist — never by the live file.
        self.assertTrue(any(line.strip() == "eval/harness-v2/authorization.local.yaml"
                            for line in (L.hv2_paths.REPO_ROOT / ".gitignore").read_text().splitlines()),
                        "authorization.local.yaml must be gitignored")
        with self.assertRaises(NotAuthorised):
            L.open_battery_ledger(root=self.tmp / "runs", authorisation_path=self.tmp / "absent-authorization.local.yaml")
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
        p = self.write_auth(price_basis_roster_sha256="311f663159a01bc587f1b0c65c65e721d6f46937a5b7d8188ccdb3090a9ccd4c")
        auth = L.load_battery_authorisation(p)
        on_disk = hashlib.sha256(Path(hv2_paths.ROSTER).read_bytes()).hexdigest()
        self.assertEqual(auth.refusals == (), on_disk == "311f663159a01bc587f1b0c65c65e721d6f46937a5b7d8188ccdb3090a9ccd4c")
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

    def test_zero_cap_is_a_valid_signed_statement_that_forbids_the_tranche(self):
        # Image Round 1 signs cap_1b_usd: 0.00 and sarvam_cap_inr: 0.00 — "nothing in 1b, no Sarvam call".
        # The loader accepts 0 (only missing or negative is malformed) and the budget refuses every
        # positive reservation against it; a negative cap is still refused by the loader.
        good = self.write_auth(name="zero-1b.yaml", cap_1b_usd="0.00", sarvam_cap_inr="0.00")
        auth = L.load_battery_authorisation(good)
        self.assertEqual(auth.refusals, ())
        self.assertEqual(auth.caps_usd["1b"], Decimal("0"))
        bad = self.write_auth(name="neg-1b.yaml", cap_1b_usd="-0.01")
        self.assertTrue(any("cap_1b" in r for r in L.load_battery_authorisation(bad).refusals))
        b = self.make_ledger(ceiling="12.58", caps=("12.58", "0.00"))
        with self.assertRaises(BudgetExceeded):
            b.tranche("1b").reserve(Decimal("0.01"), billing_pool="credits", currency="USD", amount_native="0.01", amount_usd_equiv="0.01")
        self.assertEqual(b.tranche("1b").remaining_usd(), Decimal("0"))
        b.tranche("1a").reserve(Decimal("0.067"), billing_pool="credits", currency="USD", amount_native="0.067", amount_usd_equiv="0.067")

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


class PooledAuthorisationTest(NoNetworkTestCase):
    """Auditor AF-4 / AF-5 (2026-09-10): one signed authorisation is ONE cap however many runs use it, and a
    record that names `max_paid_calls` caps the NUMBER of paid calls over that same set of runs.

    Before this, a cap was enforced inside one run directory only: `topo3-plates` + `topo3-smoke` + `topo3-video`
    each got the whole USD 9.96 record and together spent USD 10.364.
    """

    def budget(self, auth, run_id, root=None):
        root = self.tmp / "runs" if root is None else root
        return L.BatteryBudget(L.BatteryRun.create(root, run_id, auth, mode="fake_live"))

    def auth(self, name="pool.yaml", ceiling="1.00", caps=("1.00", "1.00"), **kw):
        return L.load_battery_authorisation(self.write_auth(ceiling, caps, name=name, **kw))

    # -- AF-4: the money cap -------------------------------------------------------------------
    def test_af4_sibling_runs_under_one_authorisation_share_one_cap(self):
        auth = self.auth()
        a = self.budget(auth, "run-a")
        a.tranche("1a").record(Decimal("0.60"), **cash(Decimal("0.60")))
        b = self.budget(auth, "run-b")
        self.assertEqual(b.sibling_run_ids(), ("run-a",))
        self.assertEqual(b.spent_usd(), Decimal("0"))                    # per-run accounting is still visible
        self.assertEqual(b.sibling_spent_usd(), Decimal("0.60"))         # and so is the pooled number
        self.assertEqual(b.combined_spent_usd(), Decimal("0.60"))
        self.assertEqual(b.remaining_usd(), Decimal("0.40"))
        self.assertEqual(b.tranche("1a").remaining_usd(), Decimal("0.40"))
        b.tranche("1a").reserve(Decimal("0.40"), **cash(Decimal("0.40")))   # exactly the headroom the pool has left
        with self.assertRaises(BudgetExceeded) as cm:
            b.tranche("1a").reserve(Decimal("0.01"), **cash(Decimal("0.01")))
        self.assertIn("run-a", str(cm.exception))
        self.assertIn("pool.yaml", str(cm.exception))
        self.assertEqual(b.spent_usd(), Decimal("0.40"))
        self.assertEqual(b.combined_spent_usd(), Decimal("1.00"))
        # the pool is shared both ways, and live: run-a, opened before run-b existed, now sees run-b's spend
        self.assertEqual(a.sibling_run_ids(), ("run-b",))
        self.assertEqual(a.sibling_spent_usd(), Decimal("0.40"))
        self.assertEqual(a.combined_spent_usd(), Decimal("1.00"))
        with self.assertRaises(BudgetExceeded):
            a.tranche("1a").reserve(Decimal("0.05"), **cash(Decimal("0.05")))

    def test_af4_the_tranche_caps_are_pooled_too(self):
        auth = self.auth(name="tranche-pool.yaml", ceiling="2.00", caps=("0.50", "1.50"))
        a = self.budget(auth, "run-a")
        a.tranche("1a").record(Decimal("0.50"), **cash(Decimal("0.50")))
        b = self.budget(auth, "run-b")
        self.assertEqual(b.tranche("1a").remaining_usd(), Decimal("0"))   # 1a is spent, by a DIFFERENT run
        with self.assertRaises(BudgetExceeded) as cm:
            b.tranche("1a").reserve(Decimal("0.01"), **cash(Decimal("0.01")))
        self.assertIn("tranche 1a cap", str(cm.exception))
        b.tranche("1b").reserve(Decimal("1.00"), **cash(Decimal("1.00")))  # 1b is untouched and still spendable

    def test_af4_pooling_spans_the_sibling_out_directories_ledger_roots(self):
        # the runners give every run its own --out and keep the ledger in <out>/ledger/<run_id>/
        auth = self.auth(name="outs.yaml")
        a = self.budget(auth, "run-a", root=self.tmp / "outs" / "run-a" / "ledger")
        a.tranche("1a").record(Decimal("0.90"), **cash(Decimal("0.90")))
        b = self.budget(auth, "run-b", root=self.tmp / "outs" / "run-b" / "ledger")
        self.assertEqual(b.sibling_run_ids(), ("run-a",))
        self.assertEqual(b.remaining_usd(), Decimal("0.10"))
        with self.assertRaises(BudgetExceeded):
            b.tranche("1a").reserve(Decimal("0.11"), **cash(Decimal("0.11")))

    def test_af4_a_different_authorisation_sha_does_not_pool(self):
        one = self.auth(name="one.yaml")
        two = self.auth(name="two.yaml", approved_by="a-different-signature")
        self.assertNotEqual(one.sha256, two.sha256)
        a = self.budget(one, "run-a")
        a.tranche("1a").record(Decimal("0.90"), **cash(Decimal("0.90")))
        b = self.budget(two, "run-b")
        self.assertEqual(b.sibling_run_ids(), ())                        # another signed record, another cap
        self.assertEqual(b.sibling_spent_usd(), Decimal("0"))
        self.assertEqual(b.remaining_usd(), Decimal("1.00"))
        b.tranche("1a").reserve(Decimal("0.90"), **cash(Decimal("0.90")))

    def test_af4_a_second_run_refuses_before_dispatch_when_the_first_consumed_the_cap(self):
        auth = self.auth(name="consumed.yaml", ceiling="0.50", caps=("0.50", "0.50"))
        a = self.budget(auth, "run-a")
        a.tranche("1a").record(Decimal("0.50"), **cash(Decimal("0.50")))
        with self.assertRaises(BudgetExceeded) as cm:
            L.BatteryRun.create(self.tmp / "runs", "run-b", auth, mode="fake_live")
        self.assertIn("run-a", str(cm.exception))
        self.assertIn("0.50", str(cm.exception))
        self.assertIn("consumed.yaml", str(cm.exception))
        self.assertFalse((self.tmp / "runs" / "run-b").exists())         # refused before the run directory exists

    def test_af4_an_unreadable_sibling_refuses_rather_than_counting_zero(self):
        auth = self.auth(name="unreadable.yaml")
        a = self.budget(auth, "run-a")
        a.tranche("1a").record(Decimal("0.10"), **cash(Decimal("0.10")))
        self.budget(auth, "run-c")                                        # opened again below
        (self.tmp / "runs" / "run-a" / "run.json").write_text("{ not json")
        with self.assertRaises(SL.LedgerCorrupt):
            L.BatteryRun.create(self.tmp / "runs", "run-b", auth, mode="fake_live")
        with self.assertRaises(SL.LedgerCorrupt):
            L.BatteryRun.open(self.tmp / "runs", "run-c", auth)
        # a directory that records spend but has no run record at all is refused for the same reason
        (self.tmp / "runs" / "run-a" / "run.json").unlink()
        with self.assertRaises(SL.LedgerCorrupt):
            L.BatteryRun.create(self.tmp / "runs", "run-d", auth, mode="fake_live")

    # -- AF-5: the call limit ------------------------------------------------------------------
    def test_af5_max_paid_calls_absent_means_no_call_limit(self):
        path = self.write_auth("1.00", ("1.00", "1.00"), name="nolimit.yaml")
        auth = L.load_battery_authorisation(path)
        self.assertEqual(auth.refusals, ())
        self.assertIsNone(auth.max_paid_calls)
        st = L.authorisation_status(path)
        self.assertIsNone(st["max_paid_calls"])
        self.assertIn("NO limit", st["paid_call_limit"])
        b = self.budget(auth, "run-a")
        self.assertIsNone(b.run.max_paid_calls)
        for _ in range(9):
            b.tranche("1a").record(Decimal("0.01"), **cash(Decimal("0.01")))
        self.assertEqual(b.paid_calls(), 9)                               # nine calls, no limit to refuse them
        self.assertEqual(b.combined_paid_calls(), 9)
        t = b.tranche("1a")
        t.reserve(Decimal("0.01"), **cash(Decimal("0.01")))
        t.release()
        self.assertEqual(b.paid_calls(), 9)                               # a released reservation never became a call

    def test_af5_max_paid_calls_is_read_from_the_file_and_refuses_a_bad_value(self):
        auth = L.load_battery_authorisation(self.write_auth("1.00", ("1.00", "1.00"), name="limit.yaml", max_paid_calls=16))
        self.assertEqual(auth.refusals, ())
        self.assertEqual(auth.max_paid_calls, 16)
        st = L.authorisation_status(self.write_auth("1.00", ("1.00", "1.00"), name="limit-st.yaml", max_paid_calls=16))
        self.assertEqual(st["max_paid_calls"], "16")
        self.assertIn("pooled", st["paid_call_limit"])
        for bad in ("-1", "2.5", "sixteen"):
            with self.subTest(bad=bad):
                a = L.load_battery_authorisation(self.write_auth("1.00", ("1.00", "1.00"), name=f"bad-calls-{bad}.yaml", max_paid_calls=bad))
                self.assertTrue(any("max_paid_calls" in r for r in a.refusals), a.refusals)
        self.assertIn("max_paid_calls", L.OPTIONAL_AUTH_FIELDS)
        self.assertNotIn("max_paid_calls", L.AUTH_FIELDS)                 # optional: it is not one of the signed 13

    def test_af5_the_call_that_would_exceed_max_paid_calls_is_refused_before_dispatch(self):
        auth = self.auth(name="calls.yaml", max_paid_calls=3)
        a = self.budget(auth, "run-a")
        a.tranche("1a").record(Decimal("0.01"), **cash(Decimal("0.01")))
        a.tranche("1a").record(Decimal("0.01"), **cash(Decimal("0.01")))
        self.assertEqual(a.run.record["max_paid_calls"], "3")
        b = self.budget(auth, "run-b")
        self.assertEqual(b.combined_paid_calls(), 2)                      # the two calls the SIBLING made
        b.tranche("1a").reserve(Decimal("0.01"), **cash(Decimal("0.01")))  # the third call is authorised
        before = len(b.records())
        with self.assertRaises(BudgetExceeded) as cm:
            b.tranche("1b").reserve(Decimal("0.01"), **cash(Decimal("0.01")))
        self.assertIn("max_paid_calls", str(cm.exception))
        self.assertIn("run-a", str(cm.exception))
        self.assertEqual(len(b.records()), before)                        # nothing was written, so nothing was dispatched
        self.assertEqual(b.remaining_usd(), Decimal("0.97"))              # money was left; the CALL limit is what refused
        # and a further run cannot start at all once the pool has used every authorised call
        self.assertEqual(b.combined_paid_calls(), 3)
        with self.assertRaises(BudgetExceeded) as cm2:
            L.BatteryRun.create(self.tmp / "runs", "run-c", auth, mode="fake_live")
        self.assertIn("max_paid_calls", str(cm2.exception))


if __name__ == "__main__":
    unittest.main()
