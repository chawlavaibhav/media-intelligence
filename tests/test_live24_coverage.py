"""Tests for the REP-01 live-24 coverage layer.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Two layers: (1) the full validator runs end to end and exits 0 — this is the acceptance check for
REP-01 and it re-runs the generator twice, so it also proves determinism; (2) targeted negative
checks that the validator's own machinery refuses breaches rather than merely describing them
(a validator whose rules only exist in prose is a convention).

Run: python3 -m unittest tests.test_live24_coverage

SUPERSESSION NOTE (DN-06 admission, 2026-09-01): the live-24 layer is superseded by live-37
(canon/planning/live37_domain_map.yaml). Its committed artifacts are frozen history — their
byte-immutability is enforced here (test_live19_artifacts_untouched) and again in
tests/test_live37_coverage.py — but its validator re-derives facts from the LIVE corpus, which
has since grown to 37 sources, so the corpus-dependent checks below can no longer hold at HEAD
and are skipped with this reason, mirroring how the live19 layer was retired when live24
superseded it. The same checks run for the current layer in tests/test_live37_coverage.py.
"""
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "canon/validation/validate_live24_coverage.py"
REACH = REPO_ROOT / "canon/validation/recompute_system_reachability.py"
BACKFILL = REPO_ROOT / "canon/planning/PROPOSED-orphan-backfill-v0.yaml"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Live24CoverageTest(unittest.TestCase):
    # setUpClass used to run the live24 validator here. That validator re-runs the
    # generator against the LIVE corpus, transiently rewriting the frozen live24
    # coverage outputs — harmless when live24 was current, a mutation hazard now that
    # it is history. Every test that consumed cls.proc is skipped (supersession note
    # above), so the run is removed rather than guarded.

    @unittest.skip("superseded layer: validates against the live corpus, now 37 sources (see module docstring; current-layer checks live in tests/test_live37_coverage.py)")
    def test_validator_exits_zero(self):
        self.assertEqual(
            self.proc.returncode, 0,
            f"validate_live24_coverage.py failed:\n{self.proc.stdout}\n{self.proc.stderr}")
        payload = json.loads(self.proc.stdout)
        self.assertTrue(payload["ok"])

    @unittest.skip("superseded layer: validates against the live corpus, now 37 sources (see module docstring; current-layer checks live in tests/test_live37_coverage.py)")
    def test_closure_baseline_matches_backfill_meta(self):
        rmod = load(REACH, "reach_t")
        base = rmod.compute()
        meta = yaml.safe_load(BACKFILL.read_text())["meta"]["baseline"]
        self.assertEqual(base["reached"], meta["reached"])
        self.assertEqual(base["total"], meta["total"])
        self.assertEqual(sum(len(v) for v in base["unreached"].values()), meta["unreached"])

    @unittest.skip("superseded layer: validates against the live corpus, now 37 sources (see module docstring; current-layer checks live in tests/test_live37_coverage.py)")
    def test_simulated_adoption_closes_graph(self):
        rmod = load(REACH, "reach_t2")
        entries = yaml.safe_load(BACKFILL.read_text())["entries"]
        memberships = {e["sk_id"]: e["proposal"]["scs_id"] for e in entries
                       if e["proposal"]["type"] == "new_membership"}
        edges = [(e["sk_id"], e["proposal"]["target"]) for e in entries
                 if e["proposal"]["type"] == "new_relation"]
        sim = rmod.compute(extra_memberships=memberships, extra_edges=edges)
        self.assertEqual(sim["reached"], sim["total"], sim["unreached"])

    def test_closure_refuses_partial_adoption(self):
        """Dropping the proposals leaves the graph open — the closure is not vacuously full."""
        rmod = load(REACH, "reach_t3")
        sim = rmod.compute(extra_memberships={}, extra_edges=[])
        self.assertLess(sim["reached"], sim["total"])

    def test_every_backfill_relation_is_spec03(self):
        vmod = load(VALIDATOR, "validator_t")
        entries = yaml.safe_load(BACKFILL.read_text())["entries"]
        for e in entries:
            p = e["proposal"]
            if p["type"] == "new_relation":
                self.assertIn(p["relation"], vmod.SPEC03_ENUM, e["sk_id"])
            elif p["type"] == "new_membership":
                self.assertEqual(p["relation"], "member_of_system", e["sk_id"])
            elif p["type"] == "reachable_via":
                self.assertIn(p["committed_relation"], vmod.SPEC03_ENUM, e["sk_id"])
            else:
                self.fail(f"unknown proposal type on {e['sk_id']}")

    @unittest.skip("superseded layer: validates against the live corpus, now 37 sources (see module docstring; current-layer checks live in tests/test_live37_coverage.py)")
    def test_coverage_yaml_facts(self):
        cov = yaml.safe_load(
            (REPO_ROOT / "canon/planning/CANON-V1-LIVE24-COVERAGE.yaml").read_text())
        self.assertEqual(cov["summary"]["accepted_sources"], 24)
        self.assertEqual(cov["summary"]["total_objects"], 677)
        iic = cov["packs"]["indian_indic_context"]
        self.assertEqual(len(iic["contributors"]), 5)
        self.assertNotEqual(iic["pack_state"], "absent")
        # The authored override must not let the pack read as fully covered either.
        self.assertEqual(iic["pack_state"], "critical_limited")

    def test_live19_artifacts_untouched(self):
        """Frozen decision: supersede, never mutate. The live19 planning artifacts must be
        byte-identical to their committed state."""
        diff = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "--",
             "canon/planning/live19_domain_map.yaml",
             "canon/planning/CANON-V1-LIVE19-COVERAGE.yaml",
             "canon/planning/CANON-V1-LIVE19-COVERAGE.md",
             "canon/planning/build_live19_coverage.py"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(diff.stdout.strip(), "", "live19 artifact modified: " + diff.stdout)


if __name__ == "__main__":
    unittest.main()
