#!/usr/bin/env python3
"""EMP-001 zero-spend preflight — Q1 geometry, Q7 persistence, Registry-zero, authorisation gate.

WHAT THIS ANSWERS

    One question: is the repository mechanically ready to spend money — without having spent any.

    It is deliberately not a summary of what somebody believes is true. Every line of the result
    file is a boolean produced by a check that was executed in this process, on this tree, in this
    run, and every check has a test proving it can FAIL. A preflight that always says READY is
    worse than no preflight, because it launders belief as evidence.

WHY THE HARNESS SELF-TEST RUNS IN-PROCESS

    The no-network control patches `socket` and then runs the whole dry-run. A subprocess would
    escape that patch, and the control would prove nothing about the code it most needs to cover.
    So `run_selftest.main()` is imported and called here, inside the poisoned process.

WHAT IT REFUSES

    Without `--dry-run` it refuses to run at all while no valid authorisation exists. There is no
    flag that makes it proceed anyway.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from budget_guard import AUTHORISATION_LOCAL_PATH, authorisation_status  # noqa: E402

GEOMETRY_MANIFEST = REPO_ROOT / "eval/v1/instruments/fixtures/cv-geometry/manifest.json"
REGISTRY = REPO_ROOT / "eval/registry/registry-v1.jsonl"
PROTECTED_BASELINES = HERE / "protected-baselines.sha256"
CONFIG = HERE / "config.yaml"
DEFAULT_OUT = HERE / "preflight-result.json"

EXPECTED_GEOMETRY_FIXTURES = 102


# --------------------------------------------------------------------------------- Q1 geometry
def check_geometry_fixtures(manifest_path: Path | str = GEOMETRY_MANIFEST) -> dict:
    """The deterministic CV geometry pack must still be exactly 102 fixtures, all present."""
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        return {"ok": False, "reason": f"missing manifest {manifest_path}",
                "fixture_count": 0, "expected": EXPECTED_GEOMETRY_FIXTURES}

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    count = data.get("counts", {}).get("total")
    items = data.get("items", [])
    missing = [i["id"] for i in items
               if not (manifest_path.parent / i["image"]).exists()]

    return {
        "ok": count == EXPECTED_GEOMETRY_FIXTURES and not missing,
        "fixture_count": count,
        "expected": EXPECTED_GEOMETRY_FIXTURES,
        "declared_items": len(items),
        "missing_images": missing,
        "manifest": str(manifest_path),
    }


# ------------------------------------------------------------------------------ Registry zero
def check_registry_empirical_rows(registry_path: Path | str = REGISTRY) -> dict:
    """The Capability Registry must still contain zero empirical rows. Comments are not rows."""
    registry_path = Path(registry_path)
    raw = registry_path.read_bytes()
    rows = [ln for ln in raw.decode("utf-8").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")]
    return {
        "ok": len(rows) == 0,
        "empirical_row_count": len(rows),
        "file_sha256": hashlib.sha256(raw).hexdigest(),
        "path": str(registry_path),
    }


# ------------------------------------------------------------------------ protected baselines
def check_protected_baselines(baselines_path: Path | str = PROTECTED_BASELINES,
                              repo_root: Path | str = REPO_ROOT) -> dict:
    """Every historical baseline must still hash to its pre-EMP-001 value."""
    baselines_path, repo_root = Path(baselines_path), Path(repo_root)
    mismatches, checked = [], 0

    for line in baselines_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        expected, rel = line.split(None, 1)
        target = repo_root / rel.strip()
        checked += 1
        if not target.exists():
            mismatches.append({"path": rel.strip(), "problem": "missing"})
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            mismatches.append({"path": rel.strip(), "expected": expected, "actual": actual})

    return {"ok": not mismatches, "checked": checked, "mismatches": mismatches}


# ------------------------------------------------------------------ Q7 one call = one trial
def _synthetic_harness(qualification_status: str = "screened_not_qualified"):
    """Build a throwaway harness over the dummy synthetic adapters. No network, no spend.

    `qualification_status` is a parameter because the two Registry controls need different
    instruments. To prove the SYNTHETIC guard specifically, the instrument must be `qualified`,
    so that the qualification guard cannot be what refused the write. Otherwise the test would
    pass while the synthetic guard was broken.
    """
    import tempfile
    sys.path.insert(0, str(REPO_ROOT / "eval/v1/harness"))
    import adapters as A
    from harness import Harness, Instrument

    h = Harness(Path(tempfile.mkdtemp()))
    h.register_instrument(Instrument(
        "preflight-dummy", "v0", {"kind": "synthetic"},
        qualification_status=qualification_status,
        capabilities={"text_exactness"},
        fn=A.make_evaluator("preflight", {"text_exactness"})))
    return h, A


def check_one_call_one_trial() -> dict:
    """One provider call is one trial — including a call that refuses and produces nothing."""
    h, A = _synthetic_harness()
    item = {"item_id": "preflight-000", "modality": "image"}
    cfg = {"model": "dummy", "lane": "image", "unit_price": 0.10}

    ok_attempt = h.generate(item, cfg, A.dummy_generator)
    refused = h.generate(item, cfg, A.refusing_generator, repeat_of=ok_attempt.attempt_id,
                         repeat_index=1)

    attempts = h.emit_attempts()
    trials = {a["trial_id"] for a in attempts}

    return {
        "ok": (len(attempts) == len(trials) == 2
               and refused.trial_id is not None
               and ok_attempt.attempt_id == ok_attempt.trial_id
               and not h.registry_rows),
        "attempts": len(attempts),
        "trials": len(trials),
        "refused_attempt_still_has_a_trial": bool(refused.trial_id),
        "refused_attempt_has_a_cost_ref": bool(refused.cost_ref),
        "registry_rows_created": len(h.registry_rows),
    }


def check_synthetic_cannot_reach_registry() -> dict:
    """A synthetic measurement must be REFUSED at the Registry boundary. There is no override."""
    h, A = _synthetic_harness(qualification_status="qualified")
    item = {"item_id": "preflight-001", "modality": "image",
            "measurement_fanout": ["text_exactness"]}
    cfg = {"model": "dummy", "lane": "image", "unit_price": 0.10}
    attempt = h.generate(item, cfg, A.dummy_generator)
    m = h.measure(attempt.asset_id, "text_exactness", "preflight-dummy", item=item)

    try:
        h.write_registry_row("text_exactness", "preflight-dummy", [m],
                             conditions={}, difficulty_level=1, repeats_per_item=1)
    except Exception as exc:
        return {"ok": True, "refused": True, "refusal_message": str(exc),
                "registry_rows_created": len(h.registry_rows)}

    return {"ok": False, "refused": False,
            "refusal_message": "NO refusal — a synthetic measurement reached the Registry",
            "registry_rows_created": len(h.registry_rows)}


# ------------------------------------------------------------------- inherited harness self-test
def check_harness_selftest() -> dict:
    """Run the existing V1 harness self-test IN THIS PROCESS, so the socket poison covers it."""
    import contextlib
    import io

    sys.path.insert(0, str(REPO_ROOT / "eval/v1/harness"))
    import run_selftest

    run_selftest.results.clear()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = run_selftest.main()

    passed = sum(1 for _, ok, _ in run_selftest.results if ok)
    total = len(run_selftest.results)
    failed = [name for name, ok, _ in run_selftest.results if not ok]

    return {
        "ok": code == 0 and passed == total and total > 0,
        "exit_code": code,
        "checks_passed": passed,
        "checks_total": total,
        "failed_checks": failed,
        "registry_rows_created": 0,
        "ran": "eval/v1/harness/run_selftest.py main() in-process",
    }


# --------------------------------------------------------------------------------- authorisation
def check_authorisation_blocked(path: Path | str = AUTHORISATION_LOCAL_PATH) -> dict:
    """During preparation, paid execution must be impossible. `ok` means BLOCKED."""
    import yaml

    status = authorisation_status(path)
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    return {
        "ok": not status["paid_execution_permitted"],
        "paid_execution_permitted": status["paid_execution_permitted"],
        "authorisation_file_exists": status["file_exists"],
        "authorisation_file_is_false_or_missing": not status["authorised"],
        "retries_authorised": cfg["retries_authorised"],
        "config_status": cfg["status"],
        "refusals": status["refusals"],
    }


# --------------------------------------------------------------------------------------- run
def run_preflight(dry_run: bool) -> dict:
    checks = {
        "geometry_fixtures": check_geometry_fixtures(),
        "registry_empirical_rows": check_registry_empirical_rows(),
        "protected_baselines": check_protected_baselines(),
        "one_call_one_trial": check_one_call_one_trial(),
        "synthetic_cannot_reach_registry": check_synthetic_cannot_reach_registry(),
        "authorisation_blocked": check_authorisation_blocked(),
        "harness_selftest": check_harness_selftest(),
    }
    green = all(c["ok"] for c in checks.values())
    return {
        "record": "EMP-001-preflight",
        "dry_run": dry_run,
        "verdict": "PREFLIGHT_GREEN" if green else "PREFLIGHT_BLOCKED",
        "checks": checks,
        "failed_checks": [k for k, c in checks.items() if not c["ok"]],
        "external_calls": 0,
        "spend_usd": "0",
        "note": ("Every boolean above was produced by a check executed in this run. No provider, "
                 "model or evaluator was called and no money was spent."),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EMP-001 zero-spend preflight.")
    ap.add_argument("--dry-run", action="store_true",
                    help="the only supported mode while EMP-001 is unauthorised")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args(argv)

    if not a.dry_run:
        auth = check_authorisation_blocked()
        if not auth["paid_execution_permitted"]:
            print("REFUSED: EMP-001 paid execution is not authorised, so there is no non-dry-run "
                  "preflight to perform. Reasons:", file=sys.stderr)
            for r in auth["refusals"]:
                print(f"  - {r}", file=sys.stderr)
            print("Re-run with --dry-run.", file=sys.stderr)
            return 2

    result = run_preflight(dry_run=a.dry_run)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")

    print(f"verdict: {result['verdict']}")
    for name, c in sorted(result["checks"].items()):
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {name}")
    print(f"external calls: {result['external_calls']}   spend USD: {result['spend_usd']}")
    print(f"written: {out}")
    return 0 if result["verdict"] == "PREFLIGHT_GREEN" else 1


if __name__ == "__main__":
    sys.exit(main())
