"""production-learning/: the case package validator and the pilot-ledger reconciliation.

Offline. The real pilot ref (work/pilot-upwork-intro-video-v4) is consulted only when it exists in the
local repository; every assertion that needs it is skipped otherwise, never faked.
"""
from __future__ import annotations

import copy
import hashlib
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


def _head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=B.ROOT, capture_output=True, text=True).stdout.strip()


def _write_case(files: dict) -> Path:
    """Materialise a case directory from {filename: dict|str}."""
    tmp = Path(tempfile.mkdtemp(prefix="pl-generic-")) / "CASE"
    tmp.mkdir()
    for name, body in files.items():
        (tmp / name).write_text(body if isinstance(body, str) else yaml.safe_dump(body, sort_keys=False, allow_unicode=True))
    return tmp


EVIDENCE_DIR = "production-learning/cases/UPWORK-INTRO-001"


def _blob_sha(commit: str, path: str) -> str:
    r = subprocess.run(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=B.ROOT, capture_output=True, check=True)
    return hashlib.sha256(r.stdout).hexdigest()


def _generic_accepted_case(head: str) -> dict:
    """A generic later job: met the baseline, mechanical TTAO only, generic cost, no reusable template,
    evidence under a job directory of its own (an existing repo path at HEAD stands in for it).
    The final asset's sha256 is the REAL hash of the blob it names, and the evidence map carries the same row."""
    sha = _blob_sha(head, f"{EVIDENCE_DIR}/README.md")
    return {
        "README.md": "# AGENCY-TEST-001 (fixture)\n",
        "OUTCOME.yaml": {
            "case_id": "AGENCY-TEST-001", "class": "customer_work", "schema": "PRODUCTION-LEARNING-CASE-v0",
            "final_outcome": "accepted", "accepted_version": "V1", "accepted_by": "human",
            "acceptance_evidence": "chat_only_human_evidence",
            "source_main_sha": head, "job_branch": "work/job-AGENCY-TEST-001", "job_commit": head,
            "evidence_source": {"ref": head, "dir": "production-learning/cases/UPWORK-INTRO-001"},
            "template_status": "none",
            "final_asset": {"path": "README.md", "commit": head, "sha256": sha},
            "not_evidence_for": ["Capability Registry", "Canon effectiveness"],
            "versions_produced": [{"version": "V1", "human_verdict": "accept"}],
            "two_conclusions": {"final_quality": "SUCCESS", "pipeline_efficiency_time_to_accepted_outcome": "MET_BASELINE",
                                "rule": "reported side by side, never blended"},
        },
        "REVISION-TRACE.yaml": {"case_id": "AGENCY-TEST-001", "versions": [
            {"version": "V1", "input_source": "brief", "generation_status": "ok", "assembly_status": "ok",
             "human_verdict": "accept", "defects": [], "repair_succeeded": None, "cost_usd": 0.1,
             "elapsed": {"value_hms": "0:20:00", "source": ["ledger_utc"]}}]},
        "HUMAN-VERDICTS.yaml": {"case_id": "AGENCY-TEST-001", "evidence_class": "chat_only_human_evidence",
                                "verdicts": [{"version": "V1", "verdict": "accept"}]},
        "ROUTE-OBSERVATIONS.yaml": {"case_id": "AGENCY-TEST-001", "observations": [
            {"id": "RO-01", "route": "flux-2-pro", "context": "one 4:5 textless plate", "n": 1, "accepted": 1,
             "observation": "clean plate", "evidence_class": "directional_production_observation", "routing_authority": "none"}]},
        "SYSTEM-DEFECTS.yaml": {"case_id": "AGENCY-TEST-001", "defects": []},
        "PROMOTION-QUEUE.yaml": {"case_id": "AGENCY-TEST-001", "promoted_now": [], "candidate_patterns": [],
                                 "directional_only": ["RO-01"], "not_promoted": ["taste"]},
        "TIME-AND-COST.yaml": {
            "case_id": "AGENCY-TEST-001",
            "time": {"time_to_accepted_outcome_mechanical": {"value_hms": "0:20:00", "from": "job_start_utc",
                                                             "to": "accepted_utc", "source": ["JOB.yaml ttao stamps"]}},
            "counts": {"human_review_cycles": 1, "versions_to_accept": 1, "paid_generation_attempts": 2, "failed_at_provider": 0},
            "cost": {"total_known_provider_cost_usd": 0.1,
                     "cost_per_accepted_outcome": {"media_cost_to_accepted_outcome_usd": 0.1, "numerator_complete": False,
                                                   "missing_components": ["vendor-billed reconciliation"]}},
            "product_conclusion": {"final_quality": "SUCCESS", "pipeline_efficiency": "MET_BASELINE"},
        },
        "EVIDENCE-MAP.md": f"| final asset | `README.md` @ `{head}` | `{sha}` |\n",
    }


class GenericCases(unittest.TestCase):
    """The validator checks STRUCTURE and HONESTY of any production-learning case, never the pilot's outcome."""

    def test_generic_accepted_job_passes(self):
        head = _head()
        case = _write_case(_generic_accepted_case(head))
        notes: list = []
        problems = check_case.run(case, source_ref=head, source_dir="production-learning/cases/UPWORK-INTRO-001", notes=notes)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_rejected_job_without_accepted_asset_passes(self):
        head = _head()
        files = _generic_accepted_case(head)
        o = files["OUTCOME.yaml"]
        o.update({"final_outcome": "rejected", "final_outcome_reason": "human rejected V1: product drift",
                  "two_conclusions": {"final_quality": "REJECTED", "pipeline_efficiency_time_to_accepted_outcome": "NOT_APPLICABLE"}})
        for k in ("accepted_version", "accepted_by", "final_asset"):
            del o[k]
        o["versions_produced"] = [{"version": "V1", "human_verdict": "reject"}]
        files["REVISION-TRACE.yaml"]["versions"][0]["human_verdict"] = "reject"
        files["HUMAN-VERDICTS.yaml"]["verdicts"][0]["verdict"] = "reject"
        tc = files["TIME-AND-COST.yaml"]
        tc["time"] = {"time_to_outcome_mechanical": {"value_hms": "0:20:00", "from": "job_start_utc", "to": "rejected_utc",
                                                     "source": ["JOB.yaml ttao stamps"]}}
        tc["cost"] = {"total_known_provider_cost_usd": 0.1,
                      "cost_per_accepted_outcome": {"value": None, "reason": "no accepted outcome"}}
        tc["product_conclusion"] = {"final_quality": "REJECTED", "pipeline_efficiency": "NOT_APPLICABLE"}
        case = _write_case(files)
        problems = check_case.run(case, source_ref=head, source_dir="production-learning/cases/UPWORK-INTRO-001")
        self.assertEqual(problems, [], "\n".join(problems))

    def test_abandoned_job_passes_and_cost_null_needs_a_reason(self):
        head = _head()
        files = _generic_accepted_case(head)
        o = files["OUTCOME.yaml"]
        o.update({"final_outcome": "abandoned", "final_outcome_reason": "repair allowance exhausted"})
        for k in ("accepted_version", "accepted_by", "final_asset"):
            del o[k]
        tc = files["TIME-AND-COST.yaml"]
        tc["time"] = {"time_to_outcome_mechanical": {"value": None, "reason": "no accept timestamp; job abandoned at QA",
                                                     "source": []}}
        tc["cost"] = {"total_known_provider_cost_usd": {"value": None}}      # null WITHOUT a reason -> refused
        del tc["product_conclusion"]["pipeline_efficiency"]
        case = _write_case(files)
        problems = check_case.run(case)
        self.assertTrue(any("total_known_provider_cost_usd" in p and "reason" in p for p in problems), problems)
        self.assertTrue(any("pipeline_efficiency" in p for p in problems), problems)
        tc["cost"] = {"total_known_provider_cost_usd": {"value": None, "reason": "ledger lost; provider statement pending"}}
        tc["product_conclusion"]["pipeline_efficiency"] = "NOT_APPLICABLE"
        case = _write_case(files)
        problems = check_case.run(case)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_accepted_job_must_declare_template_status_when_no_template_file(self):
        head = _head()
        files = _generic_accepted_case(head)
        del files["OUTCOME.yaml"]["template_status"]
        problems = check_case.run(_write_case(files))
        self.assertTrue(any("template_status" in p for p in problems), problems)
        files["OUTCOME.yaml"]["template_status"] = "reusable_candidate"       # claims a template but ships none
        problems = check_case.run(_write_case(files))
        self.assertTrue(any("ACCEPTED-TEMPLATE.yaml" in p for p in problems), problems)

    def test_false_or_missing_provenance_fails(self):
        head = _head()
        files = _generic_accepted_case(head)
        files["OUTCOME.yaml"]["final_asset"]["sha256"] = "MOCK"              # not a sha256
        problems = check_case.run(_write_case(files))
        self.assertTrue(any("sha256" in p for p in problems), problems)
        files = _generic_accepted_case(head)
        files["EVIDENCE-MAP.md"] = f"| `does-not-exist.png` @ `{head}` | invented |\n"
        problems = check_case.run(_write_case(files), source_ref=head, source_dir="production-learning/cases/UPWORK-INTRO-001")
        self.assertTrue(any("does not resolve" in p for p in problems), problems)
        files = _generic_accepted_case(head)
        files["EVIDENCE-MAP.md"] = f"| `README.md` @ `{head}` | `{'b' * 64}` |\n"
        files["OUTCOME.yaml"]["final_asset"]["sha256"] = "b" * 64
        problems = check_case.run(_write_case(files), source_ref=head, source_dir="production-learning/cases/UPWORK-INTRO-001")
        self.assertTrue(any("sha256" in p and "!=" in p for p in problems), problems)

    def test_legacy_pilot_aliases_still_work(self):
        outcome = yaml.safe_load((CASE / "OUTCOME.yaml").read_text())
        problems = check_case.run(CASE, pilot_ref=outcome["final_asset"]["commit"])
        self.assertEqual(problems, [], "\n".join(problems))


class Provenance(unittest.TestCase):
    """An accepted asset is byte-verified; an explicit source ref fails closed."""

    def test_A_real_accepted_asset_sha_passes(self):
        head = _head()
        notes: list = []
        problems = check_case.run(_write_case(_generic_accepted_case(head)), source_ref=head, source_dir=EVIDENCE_DIR, notes=notes)
        self.assertEqual(problems, [], "\n".join(problems))
        self.assertTrue(any("byte-verified" in n for n in notes), notes)

    def test_B_fake_64hex_sha_on_the_same_path_and_commit_fails(self):
        head = _head()
        files = _generic_accepted_case(head)
        fake = "f" * 64
        files["OUTCOME.yaml"]["final_asset"]["sha256"] = fake
        files["EVIDENCE-MAP.md"] = f"| final asset | `README.md` @ `{head}` | `{fake}` |\n"
        problems = check_case.run(_write_case(files), source_ref=head, source_dir=EVIDENCE_DIR)
        self.assertTrue(any("final_asset" in p and "sha256" in p and "!=" in p for p in problems), problems)

    def test_B2_accepted_asset_without_a_matching_hashed_evidence_row_fails(self):
        head = _head()
        files = _generic_accepted_case(head)
        files["EVIDENCE-MAP.md"] = f"| `README.md` @ `{head}` | no hash column |\n"
        problems = check_case.run(_write_case(files), source_ref=head, source_dir=EVIDENCE_DIR)
        self.assertTrue(any("EVIDENCE-MAP.md" in p and "final_asset" in p for p in problems), problems)

    def test_B3_repo_root_path_form_is_byte_verified_too(self):
        head = _head()
        files = _generic_accepted_case(head)
        files["OUTCOME.yaml"]["final_asset"]["path"] = f"{EVIDENCE_DIR}/README.md"      # the pilot's shape
        problems = check_case.run(_write_case(files), source_ref=head, source_dir=EVIDENCE_DIR)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_C_explicit_nonexistent_source_ref_fails(self):
        head = _head()
        problems = check_case.run(_write_case(_generic_accepted_case(head)), source_ref="no-such-ref-xyz", source_dir=EVIDENCE_DIR)
        self.assertTrue(any("source ref" in p and "no-such-ref-xyz" in p for p in problems), problems)
        problems = check_case.run(CASE, pilot_ref="no-such-ref-xyz")
        self.assertTrue(any("source ref" in p and "no-such-ref-xyz" in p for p in problems), problems)

    def test_D_no_source_ref_is_structural_only_with_a_note(self):
        head = _head()
        notes: list = []
        problems = check_case.run(_write_case(_generic_accepted_case(head)), notes=notes)
        self.assertEqual(problems, [], "\n".join(problems))
        self.assertTrue(any("skipped" in n for n in notes), notes)
        self.assertTrue(any("not byte-verified" in n for n in notes), notes)

    @unittest.skipUnless(_ref_exists(), "raw pilot ref not present locally")
    def test_E_upwork_intro_001_is_byte_verified_and_unchanged(self):
        outcome = yaml.safe_load((CASE / "OUTCOME.yaml").read_text())
        commit = outcome["final_asset"]["commit"]
        notes: list = []
        problems = check_case.run(CASE, source_ref=commit, source_dir=PILOT_DIR, notes=notes)
        self.assertEqual(problems, [], "\n".join(problems))
        self.assertTrue(any("byte-verified" in n and outcome["final_asset"]["sha256"][:12] in n for n in notes), notes)
        # the case directory itself is byte-identical to main
        r = subprocess.run(["git", "diff", "--quiet", "main", "--", str(CASE.relative_to(B.ROOT))], cwd=B.ROOT)
        self.assertEqual(r.returncode, 0, "UPWORK-INTRO-001 differs from main")


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
        # The case's figures are the identity of the ACCEPTED commit (OUTCOME.final_asset.commit). The pilot
        # branch kept moving after V4.1 (portfolio work on 15 Sep appended ledger lines), so reconciling
        # against the branch tip would compare a later ledger with the recorded case; the commit is pinned.
        outcome = yaml.safe_load((CASE / "OUTCOME.yaml").read_text())
        accepted_commit = outcome["final_asset"]["commit"]
        figures = reconcile_pilot_ledgers.pilot_totals(B.ROOT, accepted_commit, PILOT_DIR)
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
