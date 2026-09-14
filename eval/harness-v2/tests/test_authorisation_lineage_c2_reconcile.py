"""Controller ruling C-2 (14 September 2026): the ledger governs caps; vendor billing is reconciliation.

Plain English. The ledger counts money the moment a request may have left the machine, so it is the number a
cap is enforced against at dispatch time - nobody waits for a bill before refusing a call. What the vendors
actually charged is a SEPARATE number, read once from their statements and written beside the ledger figure so
the real cost per accepted outcome can be computed. `coordination/audits/tools/reconcile_spend.py` now reads an
optional statements file for that column. Nobody has filed the four statements yet, so the file does not exist
in the repository; that absence must not block anything - the tool says "not reconciled" and exits 0.

Provenance: coordination/decisions/CONTROLLER-AUDIT-CLOSEOUT-CAP-CROSSINGS-AND-CALL-LIMIT-2026-09-14.md.
These tests read the sealed ledgers only, write statement files into a temp directory only, and never create the
real statements file.
"""
import contextlib
import importlib.util
import io
import unittest
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, hv2_paths  # noqa: F401

TOOL = hv2_paths.REPO_ROOT / "coordination" / "audits" / "tools" / "reconcile_spend.py"
REAL_STATEMENTS = hv2_paths.REPO_ROOT / "coordination" / "audits" / "vendor-statements" / "VENDOR-BILLED-2026-09.yaml"


def load_tool():
    spec = importlib.util.spec_from_file_location("reconcile_spend", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_tool(*argv) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = load_tool().main(list(argv))
    return code, out.getvalue()


def statement(**over) -> dict:
    base = {"provider": "fal", "statement_period": "2026-09-08/2026-09-10", "statement_ref": "fal usage export, September 2026",
            "billed_native": "8.96", "currency": "USD", "billed_usd_equiv": "8.96",
            "covers_run_ids": ["vid-wan2", "vid-wan2-smoke", "vid-wan2-i2v", "vid-wan2-i2v-smoke"],
            "reconciled_by": "test-fixture", "reconciled_utc": "2026-09-14T00:00:00Z"}
    base.update(over)
    return base


class ReconcileSpendC2Test(NoNetworkTestCase):
    def test_c2_tool_is_read_only_over_ledgers_and_opens_no_network(self):
        src = TOOL.read_text(encoding="utf-8")
        for needle in ("socket", "urllib", "requests", "http.client", "subprocess"):
            self.assertNotIn(f"import {needle}", src)
        self.assertFalse(REAL_STATEMENTS.exists(), "nobody has the statements; the real file must not exist (tests never create it)")
        mod = load_tool()
        self.assertEqual(Path(mod.DEFAULT_STATEMENTS).resolve(), REAL_STATEMENTS.resolve())
        self.assertIn("statement_ref", mod.__doc__)                  # the schema is documented in the tool's docstring
        self.assertIn("covers_run_ids", mod.__doc__)

    def test_c2_absent_statements_file_prints_not_reconciled_and_exits_0(self):
        code, out = run_tool("--vendor-statements", str(self.tmp / "absent.yaml"))
        self.assertEqual(code, 0)
        self.assertIn("not reconciled (no statement filed)", out)
        self.assertNotIn("stmt:", out)
        self.assertIn("vid-wan2 ", out)                              # the ledger table is still printed in full
        self.assertIn("ledger governs the cap", out)                 # C-2 stated in the output itself
        self.assertFalse((self.tmp / "absent.yaml").exists())       # the tool never creates the file
        self.assertFalse(REAL_STATEMENTS.exists())
        # the default path is the real (absent) file: same result, exit 0 - lack of statements blocks nothing
        code, out = run_tool()
        self.assertEqual(code, 0)
        self.assertIn("not reconciled (no statement filed)", out)

    def test_c2_a_filed_statement_is_read_and_compared_with_the_ledger(self):
        path = self.tmp / "VENDOR-BILLED-2026-09.yaml"
        path.write_text(yaml.safe_dump({"statements": [statement()]}, sort_keys=False))
        code, out = run_tool("--vendor-statements", str(path))
        self.assertEqual(code, 0)
        self.assertIn("stmt:fal", out)                               # the covered runs point at the statement
        self.assertIn("not reconciled (no statement filed)", out)   # every uncovered run still says so
        self.assertIn("VENDOR STATEMENTS", out)
        self.assertIn("11.840000", out)                              # ledger consumed over the four covered runs
        self.assertIn("8.96", out)                                   # what the statement says was billed
        self.assertIn("-2.880000", out)                              # billed minus ledger: the never-charged 422 draws
        self.assertIn("fal usage export, September 2026", out)
        self.assertNotIn("<<< CONSUMED ABOVE HIGHEST CAP" + " (vendor)", out)

    def test_c2_a_malformed_statement_refuses_rather_than_guessing(self):
        cases = {
            "missing field": {"statements": [{k: v for k, v in statement().items() if k != "reconciled_by"}]},
            "unknown run id": {"statements": [statement(covers_run_ids=["no-such-run"])]},
            "not a number": {"statements": [statement(billed_usd_equiv="eight")]},
            "account-number-like ref": {"statements": [statement(statement_ref="acct 1234567890123")]},
            "not a mapping": ["x"],
            "unknown field": {"statements": [statement(account_number="1")]},
        }
        for name, doc in cases.items():
            with self.subTest(case=name):
                path = self.tmp / f"bad-{name.replace(' ', '-')}.yaml"
                path.write_text(yaml.safe_dump(doc, sort_keys=False))
                code, out = run_tool("--vendor-statements", str(path))
                self.assertEqual(code, 2, out)
                self.assertIn("refus", out.lower())


if __name__ == "__main__":
    unittest.main()
