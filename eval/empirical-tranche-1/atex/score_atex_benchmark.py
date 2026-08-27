#!/usr/bin/env python3
"""EVAL-030 — score the 16 sealed EVAL-024 A-TEXT artifacts with the EVAL-029 benchmark evaluator.

WHAT THIS MODULE CANNOT DO, BY CONSTRUCTION

    It cannot generate an image. It never imports `generate_atex`, never constructs a fal route,
    never reads `FAL_KEY`, and has no code path that produces bytes. The only bytes it handles are
    read from disk and hash-verified first.

    That is deliberate and it is stronger than a promise not to regenerate. If an artifact is
    missing or its hash does not match the sealed manifest, the honest outcome is a refusal, and
    the only alternative this module has is to stop — it has no way to manufacture a replacement.

VERIFY BEFORE DISPATCH, NOT AFTER

    Every artifact's SHA-256 is checked against the merged EVAL-024 manifest BEFORE a single byte
    is sent to Cloud Vision. Scoring an unverified file would attribute a measurement to a
    generator that may not have produced it, and an evaluator call already spent is not
    recoverable — so the check has to come first, not as a later assertion.

WHAT THE RESULT IS AND IS NOT

    It is a BENCHMARK measurement carrying declared evaluator error. Cloud Vision misses roughly
    12.5% of adversarial Devanagari corruptions and 10.4% of Latin ones, so an "exact match" here
    means "the evaluator read it as matching", not "this image is provably correct".

    The raw observed rate is reported. It is NOT adjusted upward or downward for evaluator error:
    no method for doing so has been justified, and an unexplained correction would look like a
    measurement while being an assumption.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
REPO_ROOT = PACKAGE_ROOT.parent.parent
sys.path.insert(0, str(PACKAGE_ROOT))
sys.path.insert(0, str(PACKAGE_ROOT / "text_qualification"))

from budget_guard import BudgetGuard  # noqa: E402
import ocr_providers as OCR  # noqa: E402
import qualify_text as QT  # noqa: E402
import benchmark_text_ocr as B  # noqa: E402

SEALED_ROOT = HERE / "sealed-generation-v1"
SEALED_MANIFEST = SEALED_ROOT / "atex-generation-only-manifest.json"
BENCHMARK_EVIDENCE = (PACKAGE_ROOT / "evidence" / "EMP-001" / "text-ocr"
                      / "benchmark-text-ocr-qualification.json")
SCORING_FILENAME = "atex-benchmark-scoring-v1.json"

MAX_ARTIFACTS = 16
USD_PER_EVALUATION = OCR.CLOUD_VISION_USD_PER_IMAGE          # 0.0015
MAX_EVALUATOR_SPEND = USD_PER_EVALUATION * MAX_ARTIFACTS      # 0.024


class ArtifactRefused(RuntimeError):
    """A sealed artifact is missing or its bytes do not match the manifest. Never substituted."""


def sealed_manifest() -> dict:
    return json.loads(SEALED_MANIFEST.read_text(encoding="utf-8"))


def evaluator_qualification() -> dict:
    """The EVAL-029 measured error rates, per script, carried onto every scored row."""
    b = json.loads(BENCHMARK_EVIDENCE.read_text(encoding="utf-8"))
    return {
        "contract_id": b["contract_id"],
        "contract_sha256": b["contract_sha256"],
        "benchmark_qualified": b["benchmark_qualified"],
        "strict_exactness_qualified": b["strict_exactness_qualified"],
        "by_script": {s: {"false_pass_rate": v["false_pass_rate"],
                          "match_false_fail_rate": v["match_false_fail_rate"],
                          "repeat_consistency": v["repeat_consistency"]}
                      for s, v in b["scripts"].items()},
        "evaluator_identity": b["evaluator"],
    }


def _qual_script(script: str) -> str:
    """Map an A-TEXT item script onto the script the evaluator was qualified on.

    The battery qualified `devanagari` and `latin`. A-TEXT items are labelled more finely —
    `latin_hinglish` and `latin_commercial_claim` — but both are Latin glyphs, so the Latin
    qualification rates are the ones that describe the measurement error. The finer label is kept
    on the row so the breakdown stays reportable.
    """
    return "devanagari" if script == "devanagari" else "latin"


def verify_artifact(entry: dict, root: Path = SEALED_ROOT) -> bytes:
    """Read the sealed bytes and prove they are the ones EVAL-024 sealed. Refuses otherwise."""
    path = root / entry["relative_path"]
    if not path.exists():
        raise ArtifactRefused(
            f"{entry['coordinate_id']}: sealed artifact missing at {path}. Refusing — this "
            f"module cannot and must not produce a replacement.")
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != entry["sha256"]:
        raise ArtifactRefused(
            f"{entry['coordinate_id']}: sha256 mismatch.\n  sealed:   {entry['sha256']}\n"
            f"  on disk:  {actual}\nRefusing to score bytes that are not the sealed artifact.")
    if len(data) != entry["bytes"]:
        raise ArtifactRefused(
            f"{entry['coordinate_id']}: byte length {len(data)} != sealed {entry['bytes']}.")
    return data


def score_sealed_atex(http=None, run=None, guard=None) -> dict:
    """Score every sealed coordinate exactly once. Verify-then-dispatch, retries 0, fail-closed."""
    manifest = sealed_manifest()
    qual = evaluator_qualification()
    items = {i["item_id"]: i for i in manifest["frozen_items"]}
    routes = manifest["routes"]
    artifacts = manifest["artifacts"]

    if len(artifacts) != MAX_ARTIFACTS:
        raise ArtifactRefused(
            f"manifest declares {len(artifacts)} artifacts; EVAL-030 is authorised for exactly "
            f"{MAX_ARTIFACTS}. Refusing rather than scoring an unexpected set.")

    guard = guard or BudgetGuard(authorised_usd=MAX_EVALUATOR_SPEND)
    engine = OCR.CloudVisionTextDetection(
        transport=OCR.CloudVisionHttpTransport(http=http), guard=guard)

    rows: list[dict] = []
    stopped_reason = None
    seen: set[str] = set()

    for entry in artifacts:
        cid = entry["coordinate_id"]
        if cid in seen:
            raise ArtifactRefused(f"{cid} appears twice; each artifact is scored exactly once.")
        seen.add(cid)

        # GATE: verify BEFORE any evaluator dispatch. A refusal here stops the run.
        data = verify_artifact(entry)

        item = items[entry["item_id"]]
        script = item["script"]
        qscript = _qual_script(script)
        route = routes[entry["slot"]]

        engine.call_context = {"script": qscript, "item_id": entry["item_id"],
                               "shape": "transcribe", "pass_index": _repeat_index(cid),
                               "trial_id": f"atex-score:{cid}"}
        # The target is handed in ONLY so the blindness checker can prove it is absent from the
        # payload. It never reaches Cloud Vision.
        response = engine.transcribe(data, blind_check_target=item["target_string"])

        transcription = response.text
        # An EMPTY transcription is a legitimate generator outcome here — unlike qualification,
        # where the image is a known-good render, an A-TEXT image may genuinely carry no legible
        # text. That is the generator failing, and it scores as a non-match.
        #
        # A provider/transport/malformed error is NOT a generator outcome. The artifact simply was
        # not measured, so it must not be counted against the route.
        evaluator_failed = response.api_status != "ok" and response.error_class != "empty_transcription"
        exact = (not evaluator_failed
                 and QT.transcription_matches(item["target_string"], transcription))

        rows.append({
            "coordinate_id": cid,
            "slot": entry["slot"],
            "generator_route": route["route"],
            "generator_provider_surface": route["provider_surface"],
            "generator_request_config": route["request_config"],
            "item_id": entry["item_id"],
            "script": script,
            "qualification_script": qscript,
            "target_string": item["target_string"],
            "repeat_index": _repeat_index(cid),
            "artifact_relative_path": entry["relative_path"],
            "artifact_sha256": entry["sha256"],
            "artifact_sha256_verified": True,
            "artifact_bytes": entry["bytes"],
            "generation_cost_ref": entry["cost_ref"],
            "evaluator_identity": qual["evaluator_identity"],
            "evaluator_contract_id": qual["contract_id"],
            "evaluator_contract_sha256": qual["contract_sha256"],
            "ocr_transcription": transcription,
            "ocr_api_status": response.api_status,
            "ocr_error_class": response.error_class,
            "ambiguous_dispatch": response.ambiguous_dispatch,
            "exact_match": exact,
            "evaluator_failed": evaluator_failed,
            "counts_toward_generator_score": not evaluator_failed,
            "evaluator_cost_ref": getattr(guard, "cost_ref", None),
            "evaluator_billed_usd": str(response.billed_usd),
            "evaluator_billing_state": response.billing_state,
            "evaluator_provider_request_id": response.provider_request_id,
            "retries": 0,
            "evaluator_false_pass_rate": qual["by_script"][qscript]["false_pass_rate"],
            "evaluator_false_fail_rate": qual["by_script"][qscript]["match_false_fail_rate"],
            "evaluator_repeat_consistency": qual["by_script"][qscript]["repeat_consistency"],
            "benchmark_qualified": True,
            "strict_exactness_qualified": False,
            "measurement_has_known_error": True,
        })

        if evaluator_failed:
            # The artifact was not measured. Cost is already conservatively settled by the
            # adapter, the trial is persisted above, and the run stops rather than continuing to
            # spend against an evaluator that is not answering. Retries remain 0.
            stopped_reason = ("ambiguous_dispatch" if response.ambiguous_dispatch
                              else response.error_class)
            break

    return _assemble(manifest, qual, rows, stopped_reason, guard)


def _repeat_index(coordinate_id: str) -> int:
    return int(coordinate_id.rsplit(":r", 1)[1])


def _rate(n: int, d: int) -> float:
    return round(n / d, 4) if d else 0.0


def _assemble(manifest: dict, qual: dict, rows: list[dict],
              stopped_reason: str | None, guard) -> dict:
    # Only MEASURED artifacts inform the generator score. An artifact the evaluator failed on is
    # reported, but attributing it to the generator would manufacture a miss out of an outage.
    scored = [r for r in rows if r["counts_toward_generator_score"]]
    unmeasured = [r for r in rows if not r["counts_toward_generator_score"]]
    matches = [r for r in scored if r["exact_match"]]

    by_route: dict[str, dict] = defaultdict(lambda: {"attempts": 0, "exact": 0, "coordinates": []})
    by_script: dict[str, dict] = defaultdict(lambda: {"attempts": 0, "exact": 0})
    by_item: dict[str, dict] = defaultdict(lambda: {"attempts": 0, "exact": 0, "by_route": {}})

    for r in scored:
        rt = by_route[r["generator_route"]]
        rt["attempts"] += 1
        rt["exact"] += bool(r["exact_match"])
        rt["coordinates"].append(r["coordinate_id"])
        sc = by_script[r["script"]]
        sc["attempts"] += 1
        sc["exact"] += bool(r["exact_match"])
        it = by_item[r["item_id"]]
        it["attempts"] += 1
        it["exact"] += bool(r["exact_match"])
        it["by_route"].setdefault(r["generator_route"], {"attempts": 0, "exact": 0})
        it["by_route"][r["generator_route"]]["attempts"] += 1
        it["by_route"][r["generator_route"]]["exact"] += bool(r["exact_match"])

    for agg in (by_route, by_script, by_item):
        for v in agg.values():
            v["observed_exact_match_rate"] = _rate(v["exact"], v["attempts"])
            for sub in v.get("by_route", {}).values():
                sub["observed_exact_match_rate"] = _rate(sub["exact"], sub["attempts"])

    # Repeat consistency: for each (route, item) pair, did both repeats agree?
    cells: dict[tuple, set] = defaultdict(set)
    for r in scored:
        cells[(r["generator_route"], r["item_id"])].add(bool(r["exact_match"]))
    consistent = sum(1 for v in cells.values() if len(v) == 1)
    repeat_consistency = _rate(consistent, len(cells))

    evaluator_spend = sum((Decimal(r["evaluator_billed_usd"]) for r in rows), Decimal("0"))
    generation_spend = Decimal(str(manifest["total_generation_cost_usd"]))

    payload = {
        "record": "EMP-001-atex-benchmark-scoring",
        "tranche_id": "EMP-001",
        "run_id": manifest["run_id"],
        "authority": "CONTROLLER-EVAL-030-ATEXT-BENCHMARK-SCORING-2026-08-28",
        "measurement_class": "benchmark",
        "not_a_certification": ("Exact-match here means the benchmark evaluator read the rendered "
                                "text as matching the target. It is not proof the image is "
                                "correct: the evaluator's own miss rate is carried on every row."),
        "generation": {
            "regenerated_anything": False,
            "generator_invoked": False,
            "sealed_manifest_fingerprint": manifest["evidence_fingerprint"],
            "artifacts_declared": len(manifest["artifacts"]),
            "artifacts_verified": sum(1 for r in rows if r["artifact_sha256_verified"]),
            "generation_spend_usd": str(generation_spend),
            "routes": {s: v["route"] for s, v in manifest["routes"].items()},
        },
        "evaluator": {
            **qual,
            "feature": "TEXT_DETECTION",
            "language_hints": [],
            "target_sent_to_provider": False,
            "retries": 0,
            "human_review": False,
        },
        "scoring": {
            "artifacts_dispatched": len(rows),
            "attempts": len(scored),
            "measured": len(scored),
            "unmeasured_evaluator_failures": len(unmeasured),
            "exact_matches": len(matches),
            "observed_exact_match_rate": _rate(len(matches), len(scored)),
            "repeat_consistency": repeat_consistency,
            "repeat_cells": len(cells),
            "stopped_reason": stopped_reason,
            "complete": stopped_reason is None and len(rows) == MAX_ARTIFACTS,
        },
        "by_generator_route": dict(by_route),
        "by_script": dict(by_script),
        "by_item": dict(by_item),
        "spend": {
            "evaluator_usd": str(evaluator_spend),
            "evaluator_max_authorised_usd": str(MAX_EVALUATOR_SPEND),
            "generation_usd": str(generation_spend),
            "atex_total_generation_plus_evaluation_usd": str(generation_spend + evaluator_spend),
        },
        "benchmark_qualified": True,
        "strict_exactness_qualified": False,
        "measurement_has_known_error": True,
        "may_populate_registry": False,
        "registry_rows_written": 0,
        "rows": rows,
    }
    payload["evidence_fingerprint"] = scoring_fingerprint(payload)
    return payload


SCORING_FINGERPRINTED_FIELDS = ("record", "tranche_id", "run_id", "generation", "evaluator",
                                "scoring", "by_generator_route", "by_script", "rows")


def scoring_fingerprint(payload: dict) -> str:
    material = {k: payload.get(k) for k in SCORING_FINGERPRINTED_FIELDS}
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, default=str).encode("utf-8")).hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EVAL-030 A-TEXT benchmark scoring.")
    ap.add_argument("--live", action="store_true", help="dispatch Cloud Vision for real")
    ap.add_argument("--run-root", default=None)
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--out", default=str(HERE / SCORING_FILENAME))
    a = ap.parse_args(argv)

    if not a.live:
        ap.error("EVAL-030 scores sealed artifacts against a live evaluator; pass --live.")

    guard = None
    run = None
    if a.run_root and a.run_id:
        import spend_ledger as SL
        run = SL.TrancheRun.open(Path(a.run_root), a.run_id)
        guard = SL.TrancheBudget(run).stage("qualification")

    payload = score_sealed_atex(http=None, run=run, guard=guard)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True,
                              default=str) + "\n", encoding="utf-8")
    s = payload["scoring"]
    print(f"scored {s['attempts']}/{MAX_ARTIFACTS}  exact {s['exact_matches']}  "
          f"rate {s['observed_exact_match_rate']}  complete={s['complete']}")
    for route, v in payload["by_generator_route"].items():
        print(f"  {route:24} {v['exact']}/{v['attempts']}  rate {v['observed_exact_match_rate']}")
    print(f"evaluator spend USD {payload['spend']['evaluator_usd']}")
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
