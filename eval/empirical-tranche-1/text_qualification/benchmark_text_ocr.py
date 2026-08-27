#!/usr/bin/env python3
"""EVAL-029 — benchmark-grade text OCR qualification. A second instrument, not a relaxed first one.

WHY THIS MODULE EXISTS SEPARATELY FROM `qualify_ocr.py`

    `qualify_ocr.py` implements the STRICT contract: zero mismatch false passes, progressive
    Devanagari-then-Latin, and a candidate is qualified or it is not. Every historical result was
    produced by it and must keep being reproducible by it.

    Adding a `if benchmark: threshold = 0.15` branch to that file would put the strict and the
    lenient gate one boolean apart, in one function, sharing one set of tests. The first time
    someone changed the shared code for one contract they would silently change the other, and the
    historical evidence would stop being reproducible without anyone noticing.

    So the benchmark gate is its own module with its own contract file and its own status vocabulary.
    What it deliberately SHARES is the part that must never diverge: the item loader, the image
    resolver, the frozen NFC + outer-whitespace comparison, and the OCR adapter. Those are imported.

WHAT `benchmark_qualified` DOES AND DOES NOT MEAN

    It means: this evaluator catches at least 85% of deliberate corruptions, wrongly rejects at most
    10% of correct text, is stable across repeats, and rarely fails to answer. That is enough to say
    generator A produces better text than generator B.

    It does NOT mean any individual output is exactly correct. Cloud Vision misses roughly one in
    eight adversarial corruptions. Every number this module emits carries that rate, and carries
    `strict_exactness_qualified: false`, so a downstream reader cannot mistake a ranking signal for
    a guarantee.
"""
from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
sys.path.insert(0, str(PACKAGE_ROOT))
sys.path.insert(0, str(HERE))

import qualify_ocr as QO  # noqa: E402
import qualify_text as QT  # noqa: E402

BENCHMARK_CONTRACT = HERE / "qualification-contract-benchmark-text-ocr-v1.yaml"
BENCHMARK_RESULT_FILENAME = "benchmark-text-ocr-qualification.json"

SCIENTIFIC_OUTCOMES = QO.SCIENTIFIC_OUTCOMES
INFRASTRUCTURE_OUTCOME = QO.INFRASTRUCTURE_OUTCOME


def benchmark_contract() -> dict:
    return yaml.safe_load(BENCHMARK_CONTRACT.read_text(encoding="utf-8"))


def benchmark_contract_sha256() -> str:
    return hashlib.sha256(BENCHMARK_CONTRACT.read_bytes()).hexdigest()


# ------------------------------------------------------------------------------- the gate
def benchmark_metrics(observations: list[dict]) -> dict:
    """Recompute every gate metric from raw per-call outcomes.

    Rates, not counts. `false_pass_rate` is over mismatch opportunities the evaluator actually
    read; `failure_rate` pools empty transcriptions, refusals and infrastructure failures over
    ALL executions, because from a benchmark user's point of view every one of them is the
    evaluator declining to answer.
    """
    total = len(observations)
    scientific = [o for o in observations if o["observed"] in SCIENTIFIC_OUTCOMES]
    infrastructure = [o for o in observations if o["observed"] == INFRASTRUCTURE_OUTCOME]
    empties = [o for o in scientific if o["observed"] == "empty_transcription"]
    refusals = [o for o in observations if o["observed"] == "refusal"]

    mismatches = [o for o in scientific if o["expected"] == "mismatch"]
    matches = [o for o in scientific if o["expected"] == "match"]
    readable_mismatches = [o for o in mismatches if o["observed"] != "empty_transcription"]
    readable_matches = [o for o in matches if o["observed"] != "empty_transcription"]

    false_passes = [o for o in mismatches if o["observed"] == "match"]
    false_fails = [o for o in matches if o["observed"] == "mismatch"]

    by_item: dict[str, set] = {}
    for o in scientific:
        if o["observed"] in ("match", "mismatch"):
            by_item.setdefault(o["item_id"], set()).add(o["observed"])
    consistency = (sum(1 for v in by_item.values() if len(v) == 1) / len(by_item)
                   if by_item else 0.0)

    failures = len(empties) + len(refusals) + len(infrastructure)

    return {
        "executions": total,
        "scientific_executions": len(scientific),
        "infrastructure_failures": len(infrastructure),
        "match_opportunities": len(matches),
        "mismatch_opportunities": len(mismatches),
        "false_passes": len(false_passes),
        "unique_false_pass_items": len({o["item_id"] for o in false_passes}),
        "false_pass_rate": (round(len(false_passes) / len(readable_mismatches), 4)
                            if readable_mismatches else 0.0),
        "false_fails": len(false_fails),
        "unique_false_fail_items": len({o["item_id"] for o in false_fails}),
        "match_false_fail_rate": (round(len(false_fails) / len(readable_matches), 4)
                                  if readable_matches else 0.0),
        "empty_transcriptions": len(empties),
        "refusals": len(refusals),
        "failure_rate": round(failures / total, 4) if total else 0.0,
        "repeat_consistency": round(consistency, 4),
    }


def apply_benchmark_gate(observations: list[dict], required_executions: int | None = None) -> dict:
    """Apply the benchmark thresholds mechanically. Returns metrics plus a disposition."""
    c = benchmark_contract()
    required = required_executions or c["scientific_completeness"]["required_executions_per_script"]
    m = benchmark_metrics(observations)

    complete = (m["infrastructure_failures"] == 0
                and m["scientific_executions"] == required)

    failed = []
    if m["false_pass_rate"] > c["mismatch_false_pass_rate_max"]:
        failed.append("mismatch_false_pass_rate")
    if m["match_false_fail_rate"] > c["match_false_fail_rate_max"]:
        failed.append("match_false_fail_rate")
    if m["repeat_consistency"] < c["repeat_consistency_min"]:
        failed.append("repeat_consistency")
    if m["failure_rate"] > c["failure_rate_max"]:
        failed.append("failure_rate")

    return {
        **m,
        "required_executions": required,
        "scientifically_complete": complete,
        "failed_gates": failed if complete else [],
        "gates_that_would_have_failed": failed,
        # None, never a bool, on an incomplete screen: an infrastructure stop says nothing about
        # the evaluator's accuracy, and `false` would read as a quality judgement.
        "benchmark_qualified": (not failed) if complete else None,
        "strict_exactness_qualified": False,
        "strict_note": ("Under the strict zero-false-pass OCR contract this candidate failed. "
                        "That finding is preserved and is not altered by benchmark qualification."),
    }


# ----------------------------------------------------------- recompute historical evidence
def recompute_from_stored_evidence(path: Path | str, script: str) -> dict:
    """Recompute a stored strict-contract result against the benchmark gate.

    Reads the persisted per-call observations and recomputes from scratch. The prose numbers in a
    decision document are not evidence; the observations are. This function exists so the
    benchmark disposition can be checked against the raw record rather than inherited from a
    summary that might have drifted.
    """
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    candidates = payload.get("candidates") or []
    if not candidates:
        raise ValueError(f"{path} carries no candidates to recompute")

    leg = candidates[0].get(script)
    if not leg:
        raise ValueError(f"{path} carries no {script!r} screen")

    observations = leg.get("observations")
    if not observations:
        raise ValueError(
            f"{path} carries no per-call observations for {script!r}; a benchmark disposition "
            f"cannot be recomputed from summary metrics alone.")

    gate = apply_benchmark_gate(observations)
    return {
        "source_evidence": str(path),
        "source_evidence_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "source_contract_version": payload.get("contract_version"),
        "source_config_sha256": payload.get("config_sha256"),
        "script": script,
        "recomputed": gate,
        "stored_summary": {k: leg.get(k) for k in
                           ("false_passes", "false_pass_rate", "false_fails",
                            "match_false_fail_rate", "empty_transcriptions",
                            "infrastructure_failures", "repeat_consistency", "calls")},
    }


def reconciles_with_stored_summary(recomputation: dict, tolerance: float = 0.0005) -> dict:
    """Does the recomputation agree with what the accepted record claims?

    A material disagreement means the stored summary and the stored observations describe
    different runs, which would make every downstream number untrustworthy — so the caller is
    expected to stop rather than proceed to a paid call.
    """
    r, s = recomputation["recomputed"], recomputation["stored_summary"]
    checks = {
        "false_passes": (r["false_passes"], s.get("false_passes"), 0),
        "false_fails": (r["false_fails"], s.get("false_fails"), 0),
        "empty_transcriptions": (r["empty_transcriptions"], s.get("empty_transcriptions"), 0),
        "infrastructure_failures": (r["infrastructure_failures"],
                                    s.get("infrastructure_failures"), 0),
        "repeat_consistency": (r["repeat_consistency"], s.get("repeat_consistency"), tolerance),
        "false_pass_rate": (r["false_pass_rate"], s.get("false_pass_rate"), tolerance),
        "match_false_fail_rate": (r["match_false_fail_rate"],
                                  s.get("match_false_fail_rate"), tolerance),
    }
    mismatches = {}
    for name, (got, stored, tol) in checks.items():
        if stored is None:
            continue
        if abs(float(got) - float(stored)) > tol:
            mismatches[name] = {"recomputed": got, "stored": stored}
    return {"reconciles": not mismatches, "mismatches": mismatches, "compared": list(checks)}


# ------------------------------------------------------------------- live single-script screen
def run_benchmark_script(candidate, script: str, guard) -> dict:
    """Run ONE script under the benchmark contract. No progressive stop, by design.

    Scripts qualify independently here: Latin coverage does not depend on Devanagari, which is
    precisely why Cloud Vision's Latin screen was never run under the strict progressive gate.
    """
    c = benchmark_contract()
    scored = QO._score_script(candidate, script, guard, c["repeats_per_shape"])
    gate = apply_benchmark_gate(scored["observations"])
    return {
        "script": script,
        "candidate": candidate.name,
        "identity": candidate.identity(),
        "config_sha256": candidate.config_sha256(),
        "contract_id": c["contract_id"],
        "contract_sha256": benchmark_contract_sha256(),
        "benchmark": gate,
        "stopped_reason": scored["stopped_reason"],
        "observations": scored["observations"],
        "call_records": scored["call_records"],
    }


BENCHMARK_FINGERPRINTED_FIELDS = (
    "record", "tranche_id", "family", "contract_id", "contract_sha256",
    "evaluator", "scripts", "call_records")


def benchmark_fingerprint(payload: dict) -> str:
    material = {k: payload.get(k) for k in BENCHMARK_FINGERPRINTED_FIELDS}
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, default=str).encode("utf-8")).hexdigest()


def build_benchmark_result(evaluator_identity: dict, scripts: dict,
                           call_records: list[dict]) -> dict:
    """Assemble the benchmark qualification record, with BOTH statuses on every script."""
    c = benchmark_contract()
    coverage = sorted(s for s, v in scripts.items() if v.get("benchmark_qualified") is True)

    payload = {
        "record": "EMP-001-benchmark-text-ocr-qualification",
        "tranche_id": "EMP-001",
        "family": "ocr",
        "contract_id": c["contract_id"],
        "contract_version": c["contract_version"],
        "contract_sha256": benchmark_contract_sha256(),
        "contract_class": c["contract_class"],
        "evaluator": evaluator_identity,
        "scripts": scripts,
        "script_coverage": coverage,
        "benchmark_qualified": bool(coverage),
        "benchmark_qualified_scripts": coverage,
        "strict_exactness_qualified": False,
        "strict_exactness_note": (
            "Every candidate tested under the strict zero-false-pass OCR contract failed it, "
            "Cloud Vision included. That result is preserved unchanged. Benchmark qualification "
            "answers a different question and does not overturn it."),
        "measurement_has_known_error": True,
        "call_records": call_records,
        "human_review_required": False,
    }
    payload["evidence_fingerprint"] = benchmark_fingerprint(payload)
    return payload
