"""Controller ruling C-6a (14 September 2026): an amendment does NOT create a fresh budget.

Plain English. The Controller's signed authorisation file is edited in place when a cap is raised. Before this
change the ledger pooled spend by the file's byte fingerprint (`authorisation_sha256`), so raising a cap changed the
fingerprint and quietly handed the runs a brand-new, empty budget: the Wan 2 round spent USD 8.48 under the first
version of its file and USD 3.36 more under the amended version, USD 11.84 in all against a final cap of USD 11.53,
and the repaired ledger could only ever have stopped the first half. Now a file may carry a stable `budget_id` and
declare which earlier file bytes it `amends`; every run charged to any version in that lineage is one cumulative pool,
the cap checked is the CURRENT file's, and an undeclared (silent) edit is refused rather than trusted.

Ruling text and provenance: coordination/decisions/CONTROLLER-AUTHORISATION-LINEAGE-CUMULATIVE-BUDGET-2026-09-14.md
and coordination/decisions/CONTROLLER-AUDIT-CLOSEOUT-CAP-CROSSINGS-AND-CALL-LIMIT-2026-09-14.md (C-1 / C-5b: history
is preserved, nothing annulled).

Every file here is a throw-away temp file. The replay test READS the sealed Wan 2 ledgers and proves it left them
byte-identical. No network, no key, USD 0.
"""
import hashlib
import json
import shutil
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, hv2_paths  # noqa: F401
import ledger as L
from budget_guard import BudgetExceeded, NotAuthorised

BUDGET = "EVAL-040-TRANCHE-1/lineage-test"


def cash(amount) -> dict:
    amount = Decimal(str(amount))
    return dict(billing_pool="cash", currency="USD", amount_native=amount, amount_usd_equiv=amount)


class LineageLoaderTest(NoNetworkTestCase):
    def test_c6a_budget_id_and_amends_are_optional_signed_fields(self):
        self.assertIn("budget_id", L.OPTIONAL_AUTH_FIELDS)
        self.assertIn("amends", L.OPTIONAL_AUTH_FIELDS)
        self.assertNotIn("budget_id", L.AUTH_FIELDS)              # optional: the signed 13 are untouched
        self.assertNotIn("amends", L.AUTH_FIELDS)
        plain = L.load_battery_authorisation(self.write_auth(name="plain.yaml"))
        self.assertEqual(plain.refusals, ())
        self.assertIsNone(plain.budget_id)
        self.assertEqual(plain.amends, ())
        self.assertEqual(plain.lineage_sha256s, (plain.sha256,))    # a file with no amends is a lineage of one
        prev = "a" * 64
        older = "b" * 64
        auth = L.load_battery_authorisation(self.write_auth(name="lineage.yaml", budget_id=BUDGET, amends=[prev, older]))
        self.assertEqual(auth.refusals, ())
        self.assertEqual(auth.budget_id, BUDGET)
        self.assertEqual(auth.amends, (prev, older))
        self.assertEqual(auth.lineage_sha256s, (auth.sha256, prev, older))
        single = L.load_battery_authorisation(self.write_auth(name="single.yaml", budget_id=BUDGET, amends=prev))
        self.assertEqual(single.amends, (prev,))                     # one prior sha may be written as a bare string
        # the committed example documents both fields
        example = L.AUTH_EXAMPLE_PATH.read_text()
        self.assertIn("budget_id", example)
        self.assertIn("amends", example)

    def test_c6a_malformed_budget_id_or_amends_is_refused(self):
        for bad in ("", "   ", 5, "has space", None):
            with self.subTest(budget_id=bad):
                a = L.load_battery_authorisation(self.write_auth(name="bad-bid.yaml", budget_id=bad))
                self.assertTrue(any("budget_id" in r for r in a.refusals), a.refusals)
        for bad in ("abc", [], ["zz" * 32], ["a" * 64, "a" * 64], [5], None, "A" * 64):
            with self.subTest(amends=bad):
                a = L.load_battery_authorisation(self.write_auth(name="bad-amends.yaml", amends=bad))
                self.assertTrue(any("amends" in r for r in a.refusals), a.refusals)
        # a file cannot amend itself: the sha it names must not be its own (impossible to satisfy honestly)
        # and the unknown-field discipline still holds for anything else
        a = L.load_battery_authorisation(self.write_auth(name="unknown.yaml", lineage="x"))
        self.assertTrue(any("unknown fields" in r for r in a.refusals), a.refusals)


class LineagePoolingTest(NoNetworkTestCase):
    """The regression the ruling exists for: an in-place amendment cannot reset consumed spend."""

    def budget(self, auth, run_id, root=None):
        root = self.tmp / "runs" if root is None else root
        return L.BatteryBudget(L.BatteryRun.create(root, run_id, auth, mode="fake_live"))

    def auth(self, name, ceiling, **kw):
        return L.load_battery_authorisation(self.write_auth(ceiling, (ceiling, ceiling), name=name, **kw))

    def spend_like_wan2_first_half(self, b) -> Decimal:
        """15 x 0.48 + 0.64 = 7.84: the first half of the real Wan 2 round, then the 0.64 call that made 8.48."""
        for _ in range(15):
            b.tranche("1a").record(Decimal("0.48"), **cash("0.48"))
        b.tranche("1a").record(Decimal("0.64"), **cash("0.64"))
        self.assertEqual(b.spent_usd(), Decimal("7.84"))
        return b.spent_usd()

    def test_c6a_i_and_ii_an_amendment_raises_the_cap_but_never_resets_what_was_spent(self):
        # (i) file v1: cap 8.39, budget_id. Run A spends 7.84; the 0.64 call that would make 8.48 is refused.
        v1 = self.auth("wan2.yaml", "8.39", budget_id=BUDGET)
        a = self.budget(v1, "run-a")
        self.spend_like_wan2_first_half(a)
        with self.assertRaises(BudgetExceeded) as cm:
            a.tranche("1a").reserve(Decimal("0.64"), **cash("0.64"))
        self.assertIn("8.48", str(cm.exception))
        self.assertEqual(a.run.record["budget_id"], BUDGET)          # a new run writes its budget into run.json
        # (ii) the Controller amends the SAME file in place: cap 11.53, same budget_id, declares amends: [sha(v1)]
        v2 = self.auth("wan2.yaml", "11.53", budget_id=BUDGET, amends=[v1.sha256])
        self.assertNotEqual(v1.sha256, v2.sha256)                    # the fingerprint moved...
        self.assertEqual(v2.lineage_sha256s, (v2.sha256, v1.sha256))
        b = self.budget(v2, "run-b")                                 # ...but run B opens INSIDE the same budget
        self.assertEqual(b.sibling_run_ids(), ("run-a",))
        self.assertEqual(b.sibling_spent_usd(), Decimal("7.84"))
        self.assertEqual(b.combined_spent_usd(), Decimal("7.84"))
        self.assertEqual(b.remaining_usd(), Decimal("3.69"))          # 11.53 - 7.84: the raise buys 3.69, not 11.53
        self.assertEqual(json.loads(b.run.run_json_path.read_text())["authorisation_amends"], [v1.sha256])
        for _ in range(7):
            b.tranche("1b").record(Decimal("0.48"), **cash("0.48"))    # 3.36 -> cumulative 11.20
        self.assertEqual(b.combined_spent_usd(), Decimal("11.20"))
        with self.assertRaises(BudgetExceeded) as cm:
            b.tranche("1b").reserve(Decimal("0.48"), **cash("0.48"))   # 11.68 would cross 11.53
        self.assertIn("11.68", str(cm.exception))
        self.assertIn("run-a", str(cm.exception))
        # the pool is live both ways: run A, re-opened under the amended file, sees run B's spend
        a2 = L.BatteryBudget(L.BatteryRun.open(self.tmp / "runs", "run-a", v2))
        self.assertEqual(a2.sibling_run_ids(), ("run-b",))
        self.assertEqual(a2.combined_spent_usd(), Decimal("11.20"))
        # and a third run under the same lineage sees BOTH
        c = self.budget(v2, "run-c")
        self.assertEqual(set(c.sibling_run_ids()), {"run-a", "run-b"})
        self.assertEqual(c.remaining_usd(), Decimal("0.33"))

    def test_c6a_iii_a_silent_in_place_edit_is_refused_as_an_undeclared_amendment(self):
        v1 = self.auth("wan2.yaml", "8.39", budget_id=BUDGET)
        a = self.budget(v1, "run-a")
        a.tranche("1a").record(Decimal("0.48"), **cash("0.48"))
        # the cap is raised in place, same budget_id, but nobody wrote `amends`
        silent = self.auth("wan2.yaml", "11.53", budget_id=BUDGET)
        self.assertEqual(silent.refusals, ())                        # the file alone looks fine...
        with self.assertRaises(NotAuthorised) as cm:                 # ...the pool refuses it
            L.BatteryRun.create(self.tmp / "runs", "run-b", silent, mode="fake_live")
        msg = str(cm.exception)
        self.assertIn("declare the amendment", msg)
        self.assertIn("amends", msg)
        self.assertIn(BUDGET, msg)
        self.assertIn(v1.sha256[:12], msg)
        self.assertFalse((self.tmp / "runs" / "run-b").exists())     # refused before a folder exists
        with self.assertRaises(NotAuthorised):                       # re-opening run A under the silent edit is refused too
            L.BatteryRun.open(self.tmp / "runs", "run-a", silent)
        # dropping the budget_id from the same file is not an escape hatch either
        stripped = self.auth("wan2.yaml", "11.53")
        with self.assertRaises(NotAuthorised) as cm2:
            L.BatteryRun.create(self.tmp / "runs", "run-b", stripped, mode="fake_live")
        self.assertIn(BUDGET, str(cm2.exception))
        # declaring the amendment is what makes the same bytes acceptable
        declared = self.auth("wan2.yaml", "11.53", budget_id=BUDGET, amends=[v1.sha256])
        b = self.budget(declared, "run-b")
        self.assertEqual(b.sibling_spent_usd(), Decimal("0.48"))

    def test_c6a_iii_legacy_files_with_neither_field_keep_todays_behaviour(self):
        # PRESERVED HISTORY (C-1): a file with no budget_id and no amends pools by fingerprint only, exactly as
        # the 10 September repair left it. Historical pools are therefore not silently rewritten.
        v1 = self.auth("legacy.yaml", "1.00")
        a = self.budget(v1, "run-a")
        a.tranche("1a").record(Decimal("0.90"), **cash("0.90"))
        v2 = self.auth("legacy.yaml", "2.00")                        # silent in-place raise, legacy style
        b = self.budget(v2, "run-b")
        self.assertEqual(b.sibling_run_ids(), ())                    # a fresh pool: today's behaviour, unchanged
        self.assertEqual(b.remaining_usd(), Decimal("2.00"))
        # `amends` alone (no budget_id) is enough to join the lineage
        v3 = self.auth("legacy.yaml", "2.00", amends=[v1.sha256, v2.sha256])
        c = self.budget(v3, "run-c")
        self.assertEqual(set(c.sibling_run_ids()), {"run-a", "run-b"})
        self.assertEqual(c.sibling_spent_usd(), Decimal("0.90"))

    def test_c6a_iv_two_different_budget_ids_do_not_pool(self):
        one = self.auth("one.yaml", "1.00", budget_id="EVAL-040-TRANCHE-1/one")
        two = self.auth("two.yaml", "1.00", budget_id="EVAL-040-TRANCHE-1/two")
        a = self.budget(one, "run-a")
        a.tranche("1a").record(Decimal("0.90"), **cash("0.90"))
        b = self.budget(two, "run-b")
        self.assertEqual(b.sibling_run_ids(), ())
        self.assertEqual(b.remaining_usd(), Decimal("1.00"))
        # a sibling whose run.json names a DIFFERENT budget is never pooled, even in the same run root
        self.assertEqual(a.sibling_run_ids(), ())
        # an amendment may not rename a budget: lineage says "I amend one.yaml's bytes" but names budget two
        renamed = self.auth("two.yaml", "1.00", budget_id="EVAL-040-TRANCHE-1/two", amends=[one.sha256])
        with self.assertRaises(NotAuthorised) as cm:
            L.BatteryRun.create(self.tmp / "runs", "run-c", renamed, mode="fake_live")
        self.assertIn("one", str(cm.exception))
        # a run created under budget one cannot be opened with budget two's file
        with self.assertRaises(NotAuthorised):
            L.BatteryRun.open(self.tmp / "runs", "run-a", two)

    def test_c6a_v_max_paid_calls_is_cumulative_across_the_lineage(self):
        v1 = self.auth("calls.yaml", "1.00", budget_id=BUDGET, max_paid_calls=3)
        a = self.budget(v1, "run-a")
        a.tranche("1a").record(Decimal("0.01"), **cash("0.01"))
        a.tranche("1a").record(Decimal("0.01"), **cash("0.01"))
        v2 = self.auth("calls.yaml", "1.00", budget_id=BUDGET, max_paid_calls=4, amends=[v1.sha256])
        b = self.budget(v2, "run-b")
        self.assertEqual(b.combined_paid_calls(), 2)                 # run A's two calls count against the raised limit
        b.tranche("1a").record(Decimal("0.01"), **cash("0.01"))
        b.tranche("1a").record(Decimal("0.01"), **cash("0.01"))
        with self.assertRaises(BudgetExceeded) as cm:
            b.tranche("1a").reserve(Decimal("0.01"), **cash("0.01"))   # the fifth call: 4 is the CURRENT file's limit
        self.assertIn("max_paid_calls", str(cm.exception))
        self.assertIn("run-a", str(cm.exception))
        with self.assertRaises(BudgetExceeded):
            L.BatteryRun.create(self.tmp / "runs", "run-c", v2, mode="fake_live")

    def test_c6a_status_names_the_budget_the_lineage_the_pooled_runs_and_the_consumption(self):
        v1 = self.auth("st.yaml", "8.39", budget_id=BUDGET)
        a = self.budget(v1, "run-a")
        a.tranche("1a").record(Decimal("0.48"), **cash("0.48"))
        path = self.write_auth("11.53", ("11.53", "11.53"), name="st.yaml", budget_id=BUDGET, amends=[v1.sha256])
        st = L.authorisation_status(path, root=self.tmp / "runs")
        self.assertEqual(st["budget_id"], BUDGET)
        self.assertEqual(st["lineage_sha256s_short"], [L.load_battery_authorisation(path).sha256[:12], v1.sha256[:12]])
        self.assertEqual(st["pooled_run_ids"], ["run-a"])
        self.assertEqual(st["pooled_consumed_usd_equiv"], "0.48")
        self.assertIn("0.48", st["budget_summary"])
        self.assertIn("11.53", st["budget_summary"])
        self.assertIn("run-a", st["budget_summary"])
        self.assertIn(BUDGET, st["budget_summary"])
        plain = L.authorisation_status(self.write_auth(name="plain.yaml"))
        self.assertIsNone(plain["budget_id"])
        self.assertIn("no budget_id", plain["budget_summary"])
        self.assertIn("no run root", plain["budget_summary"])


class WanTwoReplayTest(NoNetworkTestCase):
    """Replay the REAL sealed Wan 2 ledgers through the cumulative pooling arithmetic under a synthetic lineage.

    The sealed run.json files record two authorisation fingerprints: v1 (`e54512d2...`, cap 8.39, runs
    vid-wan2-smoke + vid-wan2) and v2 (`062ab2f0...`, cap 11.53, runs vid-wan2-i2v-smoke + vid-wan2-i2v). The
    fingerprints are enough to name the lineage; the file bytes themselves are not in the repository and are never
    read. The sealed trees are read, copied to a temp directory, and proven byte-identical afterwards.
    """

    RUNS = hv2_paths.REPO_ROOT / "eval" / "experiments" / "EVAL-040" / "runs"
    ORDER = ("vid-wan2-smoke", "vid-wan2", "vid-wan2-i2v-smoke", "vid-wan2-i2v")

    def sealed(self, run_id: str) -> Path:
        return self.RUNS / run_id / "ledger" / run_id

    def tree_digest(self) -> str:
        h = hashlib.sha256()
        for run_id in self.ORDER:
            for name in ("run.json", "spend-ledger.jsonl"):
                h.update((self.sealed(run_id) / name).read_bytes())
        return h.hexdigest()

    def copy_run(self, root: Path, run_id: str, keep_rows: int | None = None) -> None:
        """Copy one sealed run into the replay root, optionally only its first `keep_rows` ledger lines."""
        dst = root / run_id
        dst.mkdir(parents=True)
        shutil.copyfile(self.sealed(run_id) / "run.json", dst / "run.json")
        lines = (self.sealed(run_id) / "spend-ledger.jsonl").read_text(encoding="utf-8").splitlines()
        if keep_rows is not None:
            lines = lines[:keep_rows]
        (dst / "spend-ledger.jsonl").write_text("".join(line + "\n" for line in lines), encoding="utf-8")

    def spends(self, run_id: str) -> list[Decimal]:
        rows = [json.loads(l) for l in (self.sealed(run_id) / "spend-ledger.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        return [Decimal(r["amount_usd_equiv"]) for r in rows if r["type"] == "spend"]

    def setUp(self):
        super().setUp()
        for run_id in self.ORDER:
            self.assertTrue((self.sealed(run_id) / "run.json").exists(), f"sealed ledger missing for {run_id}")
        self.before = self.tree_digest()

    def tearDown(self):
        self.assertEqual(self.tree_digest(), self.before, "the sealed Wan 2 ledgers must be byte-identical after the replay")
        super().tearDown()

    def test_replay_the_sealed_ledgers_identify_two_file_versions_and_the_recorded_figures(self):
        rec = {r: json.loads((self.sealed(r) / "run.json").read_text()) for r in self.ORDER}
        v1 = rec["vid-wan2"]["authorisation_sha256"]
        v2 = rec["vid-wan2-i2v"]["authorisation_sha256"]
        self.assertNotEqual(v1, v2)
        self.assertEqual(rec["vid-wan2-smoke"]["authorisation_sha256"], v1)
        self.assertEqual(rec["vid-wan2-i2v-smoke"]["authorisation_sha256"], v2)
        self.assertEqual(rec["vid-wan2"]["total_ceiling_usd"], "8.39")
        self.assertEqual(rec["vid-wan2-i2v"]["total_ceiling_usd"], "11.53")
        for r in self.ORDER:
            self.assertNotIn("budget_id", rec[r])                    # the historical runs predate budget_id: legacy
        # the figures the audit recorded: 8.480 under v1 against 8.39; 11.840 in all against the final 11.53
        first_half = sum(self.spends("vid-wan2-smoke")) + sum(self.spends("vid-wan2"))
        total = first_half + sum(self.spends("vid-wan2-i2v-smoke")) + sum(self.spends("vid-wan2-i2v"))
        self.assertEqual(first_half, Decimal("8.480000"))
        self.assertEqual(total, Decimal("11.840000"))
        self.assertEqual(self.spends("vid-wan2")[-1], Decimal("0.640000"))       # the call that made 8.48
        self.assertEqual(self.spends("vid-wan2-i2v")[-1], Decimal("0.480000"))   # the call that made 11.84

    def test_replay_first_half_the_call_that_made_8_48_is_refused_under_the_v1_cap(self):
        v1_sha = json.loads((self.sealed("vid-wan2") / "run.json").read_text())["authorisation_sha256"]
        root = self.tmp / "replay-v1"
        self.copy_run(root, "vid-wan2-smoke")                        # 0.48, complete
        self.copy_run(root, "vid-wan2", keep_rows=30)                # 15 reservation+spend pairs = 7.36 of its 8.00
        auth = L.load_battery_authorisation(self.write_auth("8.39", ("8.39", "8.39"), name="wan2-v1-replay.yaml",
                                                            budget_id="EVAL-040-TRANCHE-1/wan2-replay", amends=[v1_sha]))
        b = L.BatteryBudget(L.BatteryRun.open(root, "vid-wan2", auth))
        self.assertEqual(b.sibling_run_ids(), ("vid-wan2-smoke",))
        self.assertEqual(b.combined_spent_usd(), Decimal("7.84"))
        with self.assertRaises(BudgetExceeded) as cm:
            b.tranche("1a").reserve(Decimal("0.64"), **cash("0.64"))   # the 17th recorded call
        self.assertIn("8.48", str(cm.exception))
        self.assertIn("8.39", str(cm.exception))

    def test_replay_cumulative_lineage_refuses_the_call_that_crossed_11_53(self):
        rec = {r: json.loads((self.sealed(r) / "run.json").read_text()) for r in self.ORDER}
        v1_sha, v2_sha = rec["vid-wan2"]["authorisation_sha256"], rec["vid-wan2-i2v"]["authorisation_sha256"]
        root = self.tmp / "replay-v2"
        self.copy_run(root, "vid-wan2-smoke")                        # 0.48 (v1)
        self.copy_run(root, "vid-wan2")                              # 8.00 (v1), the crossing included: history as recorded
        self.copy_run(root, "vid-wan2-i2v-smoke")                    # 0.48 (v2)
        self.copy_run(root, "vid-wan2-i2v", keep_rows=10)            # 5 of its 6 calls = 2.40 (v2)
        # the current file: cap 11.53 (the final amended cap), declaring the whole lineage v2 <- v1
        lineage = L.load_battery_authorisation(self.write_auth("11.53", ("11.53", "11.53"), name="wan2-lineage-replay.yaml",
                                                               budget_id="EVAL-040-TRANCHE-1/wan2-replay", amends=[v2_sha, v1_sha]))
        self.assertEqual(lineage.refusals, ())
        b = L.BatteryBudget(L.BatteryRun.open(root, "vid-wan2-i2v", lineage))
        self.assertEqual(set(b.sibling_run_ids()), {"vid-wan2-smoke", "vid-wan2", "vid-wan2-i2v-smoke"})
        self.assertEqual(b.sibling_spent_usd(), Decimal("8.96"))
        self.assertEqual(b.spent_usd(), Decimal("2.40"))
        self.assertEqual(b.combined_spent_usd(), Decimal("11.36"))   # what the round had consumed before its last call
        self.assertEqual(b.remaining_usd(), Decimal("0.17"))
        with self.assertRaises(BudgetExceeded) as cm:
            b.tranche("1b").reserve(Decimal("0.48"), **cash("0.48"))   # the 24th recorded call: 11.36 + 0.48 = 11.84
        self.assertIn("11.84", str(cm.exception))
        self.assertIn("11.53", str(cm.exception))
        self.assertIn("vid-wan2", str(cm.exception))
        # the previous call (the 23rd, 10.88 -> 11.36) was within the cap and stays permitted
        root5 = self.tmp / "replay-v2-before"
        for r in ("vid-wan2-smoke", "vid-wan2", "vid-wan2-i2v-smoke"):
            self.copy_run(root5, r)
        self.copy_run(root5, "vid-wan2-i2v", keep_rows=8)
        b5 = L.BatteryBudget(L.BatteryRun.open(root5, "vid-wan2-i2v", lineage))
        self.assertEqual(b5.combined_spent_usd(), Decimal("10.88"))
        b5.tranche("1b").reserve(Decimal("0.48"), **cash("0.48"))
        self.assertEqual(b5.combined_spent_usd(), Decimal("11.36"))

    def test_replay_without_the_declared_lineage_the_gap_the_audit_found_remains(self):
        # CONTRAST, documented not desired: a file that only names v2 (today's fingerprint pooling) never sees the
        # 8.48 spent under v1, so the crossing call is allowed. This is exactly the half-caught Wan 2 gap in
        # AUDIT-2026-09-10-CONTROLLER-DECISIONS.md C-6a. Legacy runs with a non-matching sha are NOT pooled
        # (preserved history); only a declared `amends` joins them.
        rec = {r: json.loads((self.sealed(r) / "run.json").read_text()) for r in self.ORDER}
        v2_sha = rec["vid-wan2-i2v"]["authorisation_sha256"]
        root = self.tmp / "replay-v2-only"
        for r in ("vid-wan2-smoke", "vid-wan2", "vid-wan2-i2v-smoke"):
            self.copy_run(root, r)
        self.copy_run(root, "vid-wan2-i2v", keep_rows=10)
        v2_only = L.load_battery_authorisation(self.write_auth("11.53", ("11.53", "11.53"), name="wan2-v2-only.yaml",
                                                               budget_id="EVAL-040-TRANCHE-1/wan2-replay", amends=[v2_sha]))
        b = L.BatteryBudget(L.BatteryRun.open(root, "vid-wan2-i2v", v2_only))
        self.assertEqual(b.sibling_run_ids(), ("vid-wan2-i2v-smoke",))
        self.assertEqual(b.combined_spent_usd(), Decimal("2.88"))
        b.tranche("1b").reserve(Decimal("0.48"), **cash("0.48"))       # allowed: the gap
        self.assertEqual(b.combined_spent_usd(), Decimal("3.36"))


if __name__ == "__main__":
    unittest.main()
