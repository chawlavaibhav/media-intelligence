"""production-learning/: the case package validator and the pilot-ledger reconciliation.

Offline. The real pilot ref (work/pilot-upwork-intro-video-v4) is consulted only when it exists in the
local repository; every assertion that needs it is skipped otherwise, never faked.
"""
from __future__ import annotations

import copy
import shutil
import subprocess
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

import _bootstrap as B

import importlib.util


def _load(name: str):
    """production-learning/ is a data tree with a hyphen in its name, so its tools are loaded by path."""
    path = B.ROOT / "production-learning" / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"production_learning_tools.{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


check_case = _load("check_case")
reconcile_pilot_ledgers = _load("reconcile_pilot_ledgers")

CASE = B.ROOT / "production-learning" / "cases" / "UPWORK-INTRO-001"
PILOT_REF = "work/pilot-upwork-intro-video-v4"
PILOT_DIR = "pilots/upwork-intro-video-2026-09-14"


def _ref_exists() -> bool:
    r = subprocess.run(["git", "rev-parse", "--verify", "--quiet", PILOT_REF + "^{commit}"],
                       cwd=B.ROOT, capture_output=True, text=True)
    return r.returncode == 0


class CasePackage(unittest.TestCase):
    def test_the_case_validates(self):
        problems = check_case.run(CASE)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_accepted_outcome_needs_final_asset_sha(self):
        tmp = Path(tempfile.mkdtemp(prefix="pl-case-"))
        shutil.copytree(CASE, tmp / "CASE")
        outcome = yaml.safe_load((tmp / "CASE" / "OUTCOME.yaml").read_text())
        del outcome["final_asset"]["sha256"]
        (tmp / "CASE" / "OUTCOME.yaml").write_text(yaml.safe_dump(outcome, sort_keys=False))
        problems = check_case.run(tmp / "CASE")
        self.assertTrue(any("final_asset.sha256" in p for p in problems), problems)

    def test_unknown_root_cause_class_is_refused(self):
        tmp = Path(tempfile.mkdtemp(prefix="pl-case-"))
        shutil.copytree(CASE, tmp / "CASE")
        trace = yaml.safe_load((tmp / "CASE" / "REVISION-TRACE.yaml").read_text())
        trace["versions"][0]["defects"][0]["root_cause_class"] = "vibes"
        (tmp / "CASE" / "REVISION-TRACE.yaml").write_text(yaml.safe_dump(trace, sort_keys=False))
        problems = check_case.run(tmp / "CASE")
        self.assertTrue(any("root_cause_class" in p and "vibes" in p for p in problems), problems)

    def test_route_observations_carry_no_routing_authority(self):
        obs = yaml.safe_load((CASE / "ROUTE-OBSERVATIONS.yaml").read_text())
        for o in obs["observations"]:
            self.assertEqual(o["evidence_class"], "directional_production_observation", o)
            self.assertEqual(o["routing_authority"], "none", o)
            self.assertIsInstance(o["n"], int)

    def test_template_pacing_values_are_scoped(self):
        tmp = Path(tempfile.mkdtemp(prefix="pl-case-"))
        shutil.copytree(CASE, tmp / "CASE")
        t = yaml.safe_load((tmp / "CASE" / "ACCEPTED-TEMPLATE.yaml").read_text())
        del t["observed_pacing"][0]["evidence_scope"]
        (tmp / "CASE" / "ACCEPTED-TEMPLATE.yaml").write_text(yaml.safe_dump(t, sort_keys=False))
        problems = check_case.run(tmp / "CASE")
        self.assertTrue(any("evidence_scope" in p for p in problems), problems)

    @unittest.skipUnless(_ref_exists(), "raw pilot ref not present locally")
    def test_evidence_map_paths_resolve_against_the_pilot_ref(self):
        problems = check_case.run(CASE, pilot_ref=PILOT_REF)
        self.assertEqual(problems, [], "\n".join(problems))


class LedgerReconciliation(unittest.TestCase):
    SAMPLE = [
        {"utc": "2026-09-14T10:00:00Z", "route": "r1", "est_usd": 0.5, "status": "reserved"},
        {"utc": "2026-09-14T10:00:05Z", "status": "ok"},
        {"utc": "2026-09-14T10:01:00Z", "route": "r2", "est_usd": 1.25, "status": "reserved"},
        {"utc": "2026-09-14T10:02:00Z", "status": "http_503"},
        {"utc": "2026-09-14T10:03:00Z", "route": "r2", "est_usd": 1.25, "status": "reserved"},
        {"utc": "2026-09-14T10:04:00Z", "status": "ok"},
    ]

    def test_totals_sum_every_reserved_line_including_failed_calls(self):
        t = reconcile_pilot_ledgers.totals(self.SAMPLE)
        self.assertEqual(t["reserved_usd"], Decimal("3.00"))
        self.assertEqual(t["dispatches"], 3)
        self.assertEqual(t["returned_ok"], 2)
        self.assertEqual(t["failed"], 1)
        self.assertEqual(t["first_utc"], "2026-09-14T10:00:00Z")
        self.assertEqual(t["last_utc"], "2026-09-14T10:04:00Z")
        self.assertEqual(t["by_route"], {"r1": {"calls": 1, "usd": Decimal("0.5")},
                                         "r2": {"calls": 2, "usd": Decimal("2.50")}})

    @unittest.skipUnless(_ref_exists(), "raw pilot ref not present locally")
    def test_the_real_ledgers_reconcile_to_the_recorded_figures(self):
        figures = reconcile_pilot_ledgers.pilot_totals(B.ROOT, PILOT_REF, PILOT_DIR)
        self.assertEqual(figures["v1_v2"]["reserved_usd"], Decimal("8.082"))
        self.assertEqual(figures["v3"]["reserved_usd"], Decimal("3.28358"))
        self.assertEqual(figures["v4"]["reserved_usd"], Decimal("4.0276"))
        self.assertEqual(figures["all"]["reserved_usd"], Decimal("15.39318"))
        self.assertEqual(figures["all"]["dispatches"], 54)
        self.assertEqual(figures["all"]["failed"], 5)
        tc = yaml.safe_load((CASE / "TIME-AND-COST.yaml").read_text())
        self.assertEqual(Decimal(str(tc["cost"]["verified_pilot_provider_cost_usd"]["value"])),
                         figures["all"]["reserved_usd"])
        self.assertEqual(Decimal(str(tc["cost"]["known_v3_to_v4_1_provider_cost_usd"]["value"])),
                         figures["v3"]["reserved_usd"] + figures["v4"]["reserved_usd"])


if __name__ == "__main__":
    unittest.main()
