#!/usr/bin/env python3
"""EMP-001 A-TEXT generation-only: make the 16 frozen artifacts, seal them, score nothing.

WHY THIS EXISTS, AND WHY IT IS A SEPARATE PATH

    The Controller reversed the original ordering. Generation used to wait for a qualified text
    judge, which saved money if no judge qualified. The user now prefers speed and has already
    approved the USD 10 ceiling, so the artifacts are made NOW while evaluator qualification
    continues in parallel.

    The scientific safeguard that makes that safe is a seal, not a promise:

        generate once, hash every artifact, and later evaluate THOSE EXACT BYTES.

    No regeneration after seeing evaluator results. That is the whole guarantee, and it only holds
    if the bytes are pinned before anybody knows how they scored.

    This is a separate orchestrator rather than a flag on `run_atex.run()` because the honest
    property is not "we chose not to score" but "there is nothing here that can score". This module
    never imports a judge, never builds one, and never computes a comparison. A test greps this
    file for those names, so the property is checked rather than asserted.

WHAT IT REUSES

    The frozen fal adapters (`providers.FalImageRoute`), the persistent EMP-001 ledger
    (`spend_ledger`) and the frozen item manifest. There is no second provider integration.

WHAT IT REFUSES

    Any scoring field reaching the manifest — `write_manifest` raises rather than writes. A
    manifest that could carry a verdict would let a later reader believe these images had been
    judged before any evaluator was qualified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
REPO_ROOT = PACKAGE_ROOT.parent.parent

sys.path.insert(0, str(PACKAGE_ROOT))
sys.path.insert(0, str(HERE))

import yaml  # noqa: E402

import providers as P  # noqa: E402
import spend_ledger as SL  # noqa: E402
from budget_guard import load_authorisation  # noqa: E402

MANIFEST_FILENAME = "atex-generation-only-manifest.json"
SEALED_DIR_NAME = "sealed-generation-v1"
CONFIG = PACKAGE_ROOT / "config.yaml"
MANIFEST_ITEMS = HERE / "atex-items-v1.jsonl"

PLANNED_TOTAL = 16

# Nothing resembling a judgement may appear anywhere in a generation-only manifest.
FORBIDDEN_SCORING_KEYS = frozenset({
    "exact_match", "passed", "pass_rate", "verdict", "score", "scored_at", "transcription",
    "text_specific_stop_eligible", "qualified", "measurement", "measurements", "absent_reason",
})


class ScoringForbidden(RuntimeError):
    """A scoring field reached a generation-only artifact. It was not written."""


class ArtifactSealBroken(RuntimeError):
    """Sealed bytes no longer match the manifest that pinned them."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def items() -> list[dict]:
    return [json.loads(x) for x in MANIFEST_ITEMS.read_text(encoding="utf-8").splitlines()
            if x.strip()]


# ------------------------------------------------------------------------------ the plan
def planned_coordinates() -> list[dict]:
    """The 16 frozen coordinates, enumerated before anything is dispatched.

    Enumerating up front is what lets a missing coordinate be REPORTED as missing. If the plan were
    implicit in the loop, a call that never happened would simply be absent from the output and
    indistinguishable from one that was never intended.
    """
    cfg = config()
    coords: list[dict] = []
    for slot, meta in cfg["atex"]["slots"].items():
        for repeat_index in range(cfg["atex"]["repeats_per_item"]):
            for item in items():
                coordinate_id = f"{slot}:{item['item_id']}:r{repeat_index}"
                coords.append({
                    "coordinate_id": coordinate_id,
                    "slot": slot,
                    "route": meta["route"],
                    "provider_surface": meta["provider_surface"],
                    "item_id": item["item_id"],
                    "target_string": item["target_string"],
                    "script": item["script"],
                    "repeat_index": repeat_index,
                    "seed": None,
                    "seed_policy": "unseeded",
                    "trial_id": coordinate_id,
                    "attempt_id": coordinate_id,
                })
    if len(coords) != PLANNED_TOTAL:
        raise RuntimeError(
            f"planned {len(coords)} coordinates, expected exactly {PLANNED_TOTAL}. The frozen "
            f"shape is 4 items x 2 repeats x 2 routes and is not derivable any other way.")
    return coords


NOMINAL_PRICE_USD = {"IMG-01": Decimal("0.053"), "IMG-02": Decimal("0.060")}


# ------------------------------------------------------------------------------ generation
def generate_only(tranche_run, routes: dict, artifact_root: Path | str,
                  mode: str = "live") -> dict:
    """Dispatch the 16 frozen generations, seal what comes back, judge nothing.

    One provider call is one trial, including a call that refuses, errors or times out. Retries
    are 0: there is no path here that dispatches a coordinate twice.
    """
    artifact_root = Path(artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)
    stage = SL.TrancheBudget(tranche_run).stage("atex")

    call_records: list[dict] = []
    artifacts: list[dict] = []
    missing: list[dict] = []
    stopped_routes: dict[str, str] = {}

    for coord in planned_coordinates():
        slot = coord["slot"]
        if slot in stopped_routes:
            missing.append({**_coord_ref(coord), "reason": "route_stopped",
                            "detail": stopped_routes[slot]})
            continue

        price = NOMINAL_PRICE_USD[slot]
        stage.reserve(price, trial_id=coord["trial_id"], attempt_id=coord["attempt_id"],
                      stage="atex", coordinate_id=coord["coordinate_id"])

        request = {
            "route": coord["route"],
            "provider_surface": coord["provider_surface"],
            "item_id": coord["item_id"],
            "target_string": coord["target_string"],
            "prompt": _prompt_for(coord["item_id"]),
            "aspect_ratio": "1:1",
            "seed": None,
            "seed_policy": "unseeded",
        }

        ambiguous = None
        try:
            response = routes[slot](request)          # exactly one call. No loop. No retry.
        except P.PreDispatchRefusal:
            # PROVEN nothing was sent: release and re-raise. There is no attempt to persist.
            stage.release()
            raise
        except P.AmbiguousDispatch as exc:
            # fal may have received and billed this. Keep the money counted, keep the trial, and
            # stop this route fail-closed. The other route may continue if budget is safe.
            ambiguous = exc
            response = {"api_status": exc.api_status, "error_class": exc.error_class,
                        "provider_request_id": None, "artifact_url": None,
                        "fetch_artifact": None}

        cost_ref = stage.record(
            price, billing_state=("unknown_provisional" if ambiguous else "reported"),
            trial_id=coord["trial_id"], attempt_id=coord["attempt_id"], stage="atex",
            coordinate_id=coord["coordinate_id"])

        record = {
            **_coord_ref(coord),
            "route": coord["route"],
            "provider_surface": coord["provider_surface"],
            "target_string": coord["target_string"],
            "script": coord["script"],
            "repeat_index": coord["repeat_index"],
            "seed": None,
            "seed_policy": "unseeded",
            "request_config": _frozen_request_config(slot),
            "api_status": response["api_status"],
            "error_class": response.get("error_class"),
            "provider_request_id": response.get("provider_request_id"),
            "artifact_url": response.get("artifact_url"),
            "cost_ref": cost_ref,
            "cost_usd": str(price),
            "cost_basis": "provisional_planning_rate",
            "billing_state": "unknown_provisional" if ambiguous else "reported",
            "ambiguous_dispatch": bool(ambiguous),
            "retry_of_attempt_id": None,
            "requested_at": _now(),
            "mode": mode,
        }

        # The call record exists BEFORE anything asks whether an artifact came back, so a refusal
        # cannot silently vanish from the denominator.
        call_records.append(record)

        if ambiguous is not None:
            missing.append({**_coord_ref(coord), "reason": "ambiguous_dispatch",
                            "detail": ambiguous.error_class})
            stopped_routes[slot] = f"ambiguous_dispatch: {ambiguous.error_class}"
            continue

        if response["api_status"] != "ok" or not response.get("fetch_artifact"):
            missing.append({**_coord_ref(coord),
                            "reason": response["api_status"],
                            "detail": response.get("error_class") or "no artifact returned"})
            continue

        blob = response["fetch_artifact"]()
        relative = f"{coord['slot']}/{coord['item_id']}-r{coord['repeat_index']}.png"
        target = artifact_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)

        digest = hashlib.sha256(blob).hexdigest()
        record["artifact_sha256"] = digest
        artifacts.append({
            **_coord_ref(coord),
            "relative_path": relative,
            "sha256": digest,
            "bytes": len(blob),
            "media_type": _media_type(blob),
            "dimensions": _png_dimensions(blob),
            "artifact_url": response.get("artifact_url"),
            "provider_request_id": response.get("provider_request_id"),
            "cost_ref": cost_ref,
        })

    return {
        "record": "EMP-001-atex-generation-only",
        "mode": mode,
        "generations": len(call_records),
        "planned": PLANNED_TOTAL,
        "call_records": call_records,
        "artifacts": artifacts,
        "missing_coordinates": missing,
        "stopped_routes": stopped_routes,
        "retries": 0,
        "evaluator_calls": 0,
        "total_generation_cost_usd": str(sum(Decimal(c["cost_usd"]) for c in call_records)),
        "registry_rows_written": 0,
        "may_populate_registry": False,
        "scored": False,
    }


def _coord_ref(coord: dict) -> dict:
    return {"coordinate_id": coord["coordinate_id"], "slot": coord["slot"],
            "item_id": coord["item_id"], "trial_id": coord["trial_id"],
            "attempt_id": coord["attempt_id"]}


def _prompt_for(item_id: str) -> str:
    for item in items():
        if item["item_id"] == item_id:
            return item["prompt"]
    raise KeyError(item_id)


def _frozen_request_config(slot: str) -> dict:
    """The exact body configuration this route is frozen to, recorded with every call."""
    return {"route": P.FAL_ROUTES[slot]["route"], **P.FAL_ROUTES[slot]["body"]}


def _media_type(blob: bytes) -> str:
    return "image/png" if blob.startswith(b"\x89PNG\r\n\x1a\n") else "application/octet-stream"


def _png_dimensions(blob: bytes) -> dict | None:
    """Width/height straight out of the IHDR chunk. None when the bytes are not a PNG."""
    if not blob.startswith(b"\x89PNG\r\n\x1a\n") or len(blob) < 24:
        return None
    return {"width": int.from_bytes(blob[16:20], "big"),
            "height": int.from_bytes(blob[20:24], "big")}


# ------------------------------------------------------------------------------ the manifest
FINGERPRINTED_FIELDS = ("run_id", "tranche_id", "frozen_items", "routes", "planned_coordinates",
                        "call_records", "artifacts", "missing_coordinates", "scored",
                        "sealed_for_later_evaluation")


def manifest_fingerprint(manifest: dict) -> str:
    """SHA-256 over the plan, the calls, the artifact hashes and the route identity together.

    Binding all of them means a later reader cannot swap a route, a frozen string or an artifact
    hash and still present the manifest as the one that was produced.
    """
    material = {k: manifest.get(k) for k in FINGERPRINTED_FIELDS}
    canonical = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                           default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_manifest(tranche_run, result: dict, artifact_root: Path | str) -> dict:
    cfg = config()
    budget = SL.TrancheBudget(tranche_run)
    manifest = {
        "record": "EMP-001-atex-generation-only-manifest",
        "run_id": tranche_run.run_id,
        "tranche_id": "EMP-001",
        "mode": result["mode"],
        "created_at": _now(),
        "authority": ("coordination/decisions/"
                      "CONTROLLER-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md"),
        "frozen_items": [{"item_id": i["item_id"], "target_string": i["target_string"],
                          "script": i["script"]} for i in items()],
        "routes": {slot: {"route": meta["route"],
                          "provider_surface": meta["provider_surface"],
                          "generations": meta["generations"],
                          "request_config": _frozen_request_config(slot)}
                   for slot, meta in cfg["atex"]["slots"].items()},
        "planned_coordinates": [_coord_ref(c) for c in planned_coordinates()],
        "planned_total": PLANNED_TOTAL,
        "call_records": result["call_records"],
        "artifacts": result["artifacts"],
        "artifact_root": str(artifact_root),
        "missing_coordinates": result["missing_coordinates"],
        "stopped_routes": result["stopped_routes"],
        "generations": result["generations"],
        "retries": 0,
        "evaluator_calls": 0,
        "total_generation_cost_usd": result["total_generation_cost_usd"],
        "atex_stage_spend_usd": str(budget.stage_spent_usd("atex")),
        "cumulative_tranche_spend_usd": str(budget.spent_usd()),
        "tranche_ceiling_usd": str(SL.TOTAL_CEILING_USD),
        "registry_rows_written": 0,
        "may_populate_registry": False,
        "scored": False,
        "sealed_for_later_evaluation": True,
        "note": ("Generation-only. No evaluator was called and nothing here has been judged. "
                 "Later A-TEXT evaluation MUST verify these SHA-256 hashes and read these exact "
                 "bytes; it may not regenerate a coordinate that looks difficult or failed."),
    }
    manifest["evidence_fingerprint"] = manifest_fingerprint(manifest)
    return manifest


def _assert_unscored(manifest: dict) -> None:
    if manifest.get("scored") is not False:
        raise ScoringForbidden(
            "a generation-only manifest must declare scored: false. This task generates and "
            "seals; it does not judge, and no evaluator has been qualified to judge with.")
    if manifest.get("evaluator_calls") not in (0, None):
        raise ScoringForbidden("a generation-only manifest cannot record evaluator calls")

    def walk(node, path="") -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in FORBIDDEN_SCORING_KEYS:
                    raise ScoringForbidden(
                        f"scoring field {key!r} found at {path or '<root>'}. Generation-only "
                        f"evidence may not carry a judgement, not even a placeholder one.")
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for i, value in enumerate(node):
                walk(value, f"{path}[{i}]")

    walk({k: v for k, v in manifest.items() if k != "note"})


def write_manifest(manifest: dict, path: Path | str) -> Path:
    """Write the manifest, refusing outright if anything in it looks like a judgement."""
    _assert_unscored(manifest)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True,
                               default=str) + "\n", encoding="utf-8")
    return path


def verify_sealed_artifacts(manifest: dict, artifact_root: Path | str) -> dict:
    """Re-hash every sealed artifact. Later scoring MUST call this before reading any bytes."""
    artifact_root = Path(artifact_root)
    missing, mismatches, verified = [], [], 0

    for a in manifest.get("artifacts", []):
        path = artifact_root / a["relative_path"]
        if not path.exists():
            missing.append(a["coordinate_id"])
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != a["sha256"]:
            mismatches.append(a["coordinate_id"])
            continue
        verified += 1

    return {
        "ok": not missing and not mismatches,
        "verified": verified,
        "missing": missing,
        "hash_mismatches": mismatches,
        "fingerprint_matches": manifest.get("evidence_fingerprint")
                               == manifest_fingerprint(manifest),
    }


# --------------------------------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="EMP-001 A-TEXT generation-only. Generates and seals; never scores.")
    ap.add_argument("--live", action="store_true", help="real fal dispatch; spends money")
    ap.add_argument("--fake-live", action="store_true",
                    help="the same orchestration behind injected recorders; zero network")
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--authorisation", default=None)
    ap.add_argument("--artifact-root", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)

    if not (a.live or a.fake_live):
        print("REFUSED: choose --fake-live (zero network) or --live (spends money).",
              file=sys.stderr)
        return 2

    mode = "live" if a.live else "fake_live"

    try:
        tranche_run = SL.TrancheRun.open(Path(a.run_root), a.run_id)
    except SL.LedgerCorrupt as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

    auth_path = Path(a.authorisation or tranche_run.record["authorisation_path"])
    if not auth_path.is_absolute():
        auth_path = REPO_ROOT / auth_path
    auth = load_authorisation(auth_path)
    if auth.refusals:
        print("REFUSED: EMP-001 authorisation:", file=sys.stderr)
        for r in auth.refusals:
            print(f"  - {r}", file=sys.stderr)
        return 2

    budget = SL.TrancheBudget(tranche_run)
    nominal = sum(NOMINAL_PRICE_USD[c["slot"]] for c in planned_coordinates())
    if budget.remaining_usd() < nominal:
        print(f"REFUSED: remaining tranche headroom USD {budget.remaining_usd()} is below the "
              f"nominal generation cost USD {nominal}.", file=sys.stderr)
        return 2

    fal_http = artifact_fetch = None
    if mode == "fake_live":
        import os

        sys.path.insert(0, str(PACKAGE_ROOT / "text_qualification"))
        from fake_live import FakeFalHttp

        # An obvious non-secret. The route still reads a key at dispatch time — that behaviour is
        # the live contract and must not be special-cased away — so the rehearsal supplies a
        # placeholder rather than weakening the check it is meant to exercise.
        os.environ.setdefault("FAL_KEY", "REHEARSAL-NOT-A-REAL-KEY")
        fal_http = FakeFalHttp()

        def artifact_fetch(url):
            return b"\x89PNG\r\n\x1a\n" + url.encode("utf-8")

    cfg = config()
    routes = {slot: P.fal_route_for(slot, cfg, http=fal_http, artifact_fetch=artifact_fetch)
              for slot in cfg["atex"]["slots"]}

    artifact_root = Path(a.artifact_root) if a.artifact_root else (
        tranche_run.evidence_dir / SEALED_DIR_NAME)

    print(f"EMP-001 A-TEXT generation-only — mode {mode}")
    print(f"  run            : {tranche_run.run_id}")
    print(f"  spent so far   : USD {budget.spent_usd()} of {SL.TOTAL_CEILING_USD}")
    print(f"  nominal cost   : USD {nominal} for {PLANNED_TOTAL} generations")

    result = generate_only(tranche_run, routes=routes, artifact_root=artifact_root, mode=mode)
    manifest = build_manifest(tranche_run, result, artifact_root=artifact_root)
    out = Path(a.out) if a.out else (artifact_root / MANIFEST_FILENAME)
    write_manifest(manifest, out)

    seal = verify_sealed_artifacts(manifest, artifact_root)
    final = SL.TrancheBudget(tranche_run)

    print(f"  generations    : {result['generations']}/{PLANNED_TOTAL}")
    print(f"  sealed         : {len(result['artifacts'])} artifacts, seal ok {seal['ok']}")
    print(f"  missing        : {len(result['missing_coordinates'])}")
    print(f"  evaluator calls: {result['evaluator_calls']}   retries: {result['retries']}")
    print(f"  generation cost: USD {result['total_generation_cost_usd']}")
    print(f"  cumulative     : USD {final.spent_usd()} of {SL.TOTAL_CEILING_USD}")
    print(f"  fingerprint    : {manifest['evidence_fingerprint']}")
    print(f"  manifest       : {out}")
    return 0 if seal["ok"] and result["generations"] == PLANNED_TOTAL else 1


if __name__ == "__main__":
    sys.exit(main())
