#!/usr/bin/env python3
"""Cross-process EMP-001 lifecycle rehearsal. Zero network, zero spend (EVAL-014 E).

WHY REAL SUBPROCESSES

    The defect this whole task exists to close was invisible to a suite that ran everything in one
    process. `BudgetGuard.spent_usd` was in memory, so a test could never catch that a second
    stage reopened the tranche from zero — there never WAS a second process.

    So this rehearsal spawns actual `python` processes. Qualification runs, exits, and its memory
    is gone. A-TEXT is a fresh interpreter that knows nothing except what is on disk. If spend did
    not survive that boundary, the numbers below would show it.

WHAT IS FAKE, AND WHAT IS NOT

    Fake: the socket. Both stages use injected recorders, and a PERFECT reader.
    Real: the orchestration, request builders, provider-specific auth, parsers, the blind check,
          the code-level exactness comparison, the persistent ledger, both ceilings, the
          fingerprint-bound handoff and every gate.

    The committed Latin perceptibility sheet is now a completed real human review. The rehearsal
    also writes an explicitly unresolved temporary fixture first, solely to prove the fail-closed
    gate still refuses before exercising the positive path with the committed review.

    Nothing produced here may reach the Capability Registry.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "text_qualification"))

TOTAL_CEILING = Decimal("10.00")
QUALIFICATION_CAP = Decimal("6.00")


def _step(n: int, title: str) -> None:
    print(f"\n[{n}] {title}")


def _run_process(argv: list[str], env: dict) -> subprocess.CompletedProcess:
    """A genuinely separate interpreter. Its memory dies with it."""
    return subprocess.run([sys.executable, *argv], capture_output=True, text=True,
                          cwd=str(REPO_ROOT), env=env)


def rehearse(work_dir: Path) -> dict:
    import spend_ledger as SL

    run_root = work_dir / "runs"
    run_id = "rehearsal-run"
    env = {
        **os.environ,
        # Obvious non-secrets. No real key is used anywhere in this rehearsal.
        "OPENAI_API_KEY": "REHEARSAL-NOT-A-REAL-KEY",
        "GOOGLE_API_KEY": "REHEARSAL-NOT-A-REAL-KEY",
        "FAL_KEY": "REHEARSAL-NOT-A-REAL-KEY",
    }
    findings: dict = {"steps": [], "checks": {}}

    # ---------------------------------------------------------------- 1. authorisation
    _step(1, "create a valid fake authorisation")
    auth = work_dir / "authorization.local.yaml"
    auth.write_text("authorised: true\ntranche_id: EMP-001\n"
                    "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n"
                    "approved_by: rehearsal\napproved_at: '2026-08-27'\n")
    print(f"    {auth}")

    # ---------------------------------------------------------------- 2. initialise the run
    _step(2, "initialise the persistent run and spend state")
    run = SL.TrancheRun.create(root=run_root, run_id=run_id, authorisation_path=auth,
                               mode="fake_live")
    print(f"    run {run.run_id}  ledger {run.ledger_path.relative_to(work_dir)}")
    assert SL.TrancheBudget(run).spent_usd() == Decimal("0")

    # ---------------------------------------------------------------- 3. qualification process
    _step(3, "PROCESS A — fake-live qualification (separate interpreter)")
    proc_a = _run_process([
        "eval/empirical-tranche-1/text_qualification/qualify_text.py",
        "--fake-live", "--authorisation", str(auth),
        "--run-root", str(run_root), "--run-id", run_id,
        "--out", str(work_dir / "qualification.json"),
    ], env)
    print("   ", (proc_a.stdout.strip().splitlines() or ["<no output>"])[0])
    if proc_a.returncode != 0:
        raise SystemExit(f"qualification failed:\n{proc_a.stdout}\n{proc_a.stderr}")
    findings["steps"].append({"step": "qualification", "pid_exit": proc_a.returncode})

    # ---------------------------------------------------------------- 4. close, then reopen
    _step(4, "PROCESS A exits — reopen the budget from disk only")
    after_qualification = SL.TrancheBudget(SL.TrancheRun.open(run_root, run_id))
    qual_spend = after_qualification.stage_spent_usd("qualification")
    total_after_qual = after_qualification.spent_usd()
    print(f"    qualification spend reconstructed from the ledger: USD {qual_spend}")
    print(f"    tranche total so far:                              USD {total_after_qual}")
    findings["checks"]["qualification_spend_usd"] = str(qual_spend)
    findings["checks"]["spend_survived_process_boundary"] = qual_spend > 0

    # ---------------------------------------------------------------- 5. the handoff
    _step(5, "the persisted qualification handoff")
    qualification_doc = json.loads(
        (run.evidence_dir / "qualification-result.json").read_text(encoding="utf-8"))
    qualified = qualification_doc["qualified"]
    print(f"    qualified candidates: {[c['candidate'] for c in qualified]}")
    print(f"    fingerprint: {qualification_doc['evidence_fingerprint'][:32]}…")
    findings["checks"]["qualified_candidates"] = len(qualified)

    # Negative control: an explicitly unresolved temp sheet must close the gate.
    _step(6, "PROCESS B — A-TEXT with an explicitly UNRESOLVED Latin review fixture")
    unresolved = work_dir / "perceptibility-review-UNRESOLVED.csv"
    unresolved.write_text("item_id,visible_difference,usable_surface,reviewer_note\n")
    proc_blocked = _run_process([
        "eval/empirical-tranche-1/atex/run_atex.py",
        "--fake-live", "--run-root", str(run_root), "--run-id", run_id,
        "--perceptibility-review", str(unresolved),
        "--out", str(work_dir / "atex-blocked.json"),
    ], env)
    print(f"    exit {proc_blocked.returncode}: "
          f"{(proc_blocked.stderr.strip().splitlines() or [''])[0][:100]}")
    findings["checks"]["atex_blocked_by_perceptibility_gate"] = proc_blocked.returncode != 0

    # Positive control: use the committed real human review, which is bound to the frozen pack.
    _step(7, "PROCESS C — A-TEXT with the completed committed perceptibility review")
    proc_c = _run_process([
        "eval/empirical-tranche-1/atex/run_atex.py",
        "--fake-live", "--run-root", str(run_root), "--run-id", run_id,
        "--out", str(work_dir / "atex.json"),
    ], env)
    for line in proc_c.stdout.strip().splitlines():
        print(f"    {line}")
    if proc_c.returncode != 0:
        raise SystemExit(f"A-TEXT failed:\n{proc_c.stdout}\n{proc_c.stderr}")

    atex = json.loads((work_dir / "atex.json").read_text())

    # ---------------------------------------------------------------- 8. the invariants
    _step(8, "verify the invariants against the reconstructed ledger")
    final = SL.TrancheBudget(SL.TrancheRun.open(run_root, run_id))
    total = final.spent_usd()
    qual = final.stage_spent_usd("qualification")
    atex_spend = final.stage_spent_usd("atex")

    records = final.records()
    cost_refs = [r["cost_ref"] for r in records if r["type"] == "spend"]
    trial_ids = [r["trial_id"] for r in records if r["type"] == "spend" and "trial_id" in r]

    checks = {
        "cumulative_spend_did_not_reset": qual > 0 and atex_spend > 0 and total == qual + atex_spend,
        "total_within_10": total <= TOTAL_CEILING,
        "qualification_within_6": qual <= QUALIFICATION_CAP,
        "retries_zero": atex["retries"] == 0,
        "generations_sixteen": atex["generations"] == 16,
        "per_route_eight_each": atex["per_route"] == {"IMG-01": 8, "IMG-02": 8},
        "cost_refs_unique": len(cost_refs) == len(set(cost_refs)),
        "trial_ids_unique": len(trial_ids) == len(set(trial_ids)),
        "generation_and_evaluator_costed_separately": (
            len({a["cost_ref"] for a in atex["attempts"]}
                & {e["cost_ref"] for e in atex["evaluator_calls"]}) == 0),
        "atex_not_synthetic": atex["synthetic"] is False,
        "registry_rows_written": atex["registry_rows_written"] == 0,
        "not_promotable": atex["evidence_class"] == "partial_admission_screen_only",
    }
    for name, ok in checks.items():
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

    print(f"\n    qualification USD {qual}  +  A-TEXT USD {atex_spend}  =  USD {total} "
          f"of {TOTAL_CEILING}")
    print(f"    spend records {len(cost_refs)}, all cost refs unique: {checks['cost_refs_unique']}")

    findings["checks"].update({k: bool(v) for k, v in checks.items()})
    findings["totals"] = {"qualification_usd": str(qual), "atex_usd": str(atex_spend),
                          "total_usd": str(total), "ceiling_usd": str(TOTAL_CEILING),
                          "qualification_cap_usd": str(QUALIFICATION_CAP)}
    findings["spend_records"] = len(cost_refs)
    findings["external_calls"] = 0
    findings["spend_usd"] = "0"
    findings["all_passed"] = all(checks.values())
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EMP-001 cross-process fake-live rehearsal.")
    ap.add_argument("--work-dir", default=None,
                    help="defaults to a temporary directory that is discarded")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)

    print("EMP-001 cross-process rehearsal — fake-live, zero network, zero spend")
    if a.work_dir:
        work_dir = Path(a.work_dir)
        work_dir.mkdir(parents=True, exist_ok=True)
        findings = rehearse(work_dir)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            findings = rehearse(Path(tmp))

    print(f"\nRESULT: {'PASS' if findings['all_passed'] else 'FAIL'}   "
          f"external calls {findings['external_calls']}   spend USD {findings['spend_usd']}")

    if a.out:
        Path(a.out).write_text(json.dumps(findings, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
        print(f"written: {a.out}")
    return 0 if findings["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
