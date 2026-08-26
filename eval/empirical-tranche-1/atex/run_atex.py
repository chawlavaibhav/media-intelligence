#!/usr/bin/env python3
"""Gated A-TEXT runner for IMG-01 and IMG-02. Maximum 16 generations, no retries, ever.

FIVE GATES STAND BETWEEN THIS FILE AND A PAID GENERATION

    1. an explicit authorisation file naming EMP-001 and its exact ceiling;
    2. a text judge qualified on BOTH scripts the four items span;
    3. a green preflight;
    4. a budget guard that can reserve the next call before it is dispatched;
    5. a per-route ceiling of 8 generations that cannot be argued up at runtime.

    Each gate is tested by COUNTING CALLS on a fake generator. "No generator was invoked" is a
    measurement here, not a claim.

WHY A PARTIALLY QUALIFIED JUDGE IS NOT ENOUGH

    The four items span Devanagari and Latin/Hinglish. A judge qualified only on Devanagari cannot
    score ATEXT-03 or ATEXT-04, and running the generations anyway would produce images nobody can
    grade — spend with no measurement attached. So the gate requires the judge's qualified scope to
    cover every script in the manifest.

THERE IS NO RETRY PATH

    Not a disabled one. Not a configurable one. `retry_of_attempt_id` exists on every attempt
    record because the persistence contract requires the field, and it is pinned to None on every
    single row — there is no code path that sets it. The control is behavioural and it is tested
    by counting: when every one of the sixteen calls refuses, the runner dispatches a seventeenth
    exactly zero times.

    One provider call is one trial, including a call that refuses, errors or times out; those are
    persisted with their reason and their cost, and the run moves on.

    Repeats are NOT retries. A repeat is decided before the run to measure inherent variance and
    carries `repeat_index`; a retry is decided after seeing a failure and belongs to a production
    chain this tranche does not have. Conflating them corrupts reliability and cost at once.

DRY RUN

    `--dry-run` executes the whole protocol against a deterministic fake generator and a fake
    judge. Zero network calls, zero spend, and every measurement marked `synthetic: true`. The
    Capability Registry is never written to, and `attempt_registry_write_with_dry_run_evidence`
    proves the real harness refuses this evidence rather than trusting that it would.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
REPO_ROOT = PACKAGE_ROOT.parent.parent

sys.path.insert(0, str(PACKAGE_ROOT))
sys.path.insert(0, str(PACKAGE_ROOT / "text_qualification"))

import yaml  # noqa: E402

from budget_guard import (  # noqa: E402
    AUTHORISATION_EXAMPLE_PATH, AUTHORISATION_LOCAL_PATH, BudgetExceeded, BudgetGuard,
    NotAuthorised, load_authorisation)
from qualify_text import transcription_matches  # noqa: E402

MANIFEST = HERE / "atex-items-v1.jsonl"
CONFIG = PACKAGE_ROOT / "config.yaml"
DEFAULT_OUT = HERE / "atex-dryrun.json"

# Planning-time nominal per-generation prices. Provisional, from the route price refresh; they
# size the pre-call reservation and are not invoice evidence.
NOMINAL_PRICE_USD = {"IMG-01": Decimal("0.053"), "IMG-02": Decimal("0.060")}


class GateClosed(RuntimeError):
    """A gate that must be open before a paid generation is not open."""


def config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def items() -> list[dict]:
    return [json.loads(x) for x in MANIFEST.read_text(encoding="utf-8").splitlines() if x.strip()]


# ------------------------------------------------------------------------------ fake generator
class FakeGenerator:
    """Deterministic stand-in for a route. Makes no network call and counts everything."""

    def __init__(self, refuse_every: int = 0):
        self.calls = 0
        self.refuse_every = refuse_every
        self.requests: list[dict] = []

    def __call__(self, request: dict) -> dict:
        self.calls += 1
        self.requests.append(request)
        if self.refuse_every and self.calls % self.refuse_every == 0:
            return {"api_status": "refusal", "error_class": "moderation_block",
                    "artifact": None, "provider_request_id": f"fake-{self.calls}"}
        # A synthetic "image" whose payload encodes the target, so the fake judge has something
        # deterministic to transcribe. It is not an image and must never be treated as evidence.
        return {"api_status": "ok", "error_class": None,
                "artifact": f"SYNTHETIC_ATEXT::{request['target_string']}",
                "provider_request_id": f"fake-{self.calls}"}


def _fake_transcribe(artifact: str | None) -> str:
    """The fake judge. Reads back exactly what the fake generator drew."""
    if not artifact:
        return ""
    return artifact.split("::", 1)[1] if "::" in artifact else ""


# ------------------------------------------------------------------------------------- gates
def _check_authorisation(authorisation_path: Path | None, dry_run: bool) -> None:
    if dry_run:
        return
    path = authorisation_path or AUTHORISATION_LOCAL_PATH
    auth = load_authorisation(path)
    if auth.refusals:
        raise GateClosed(
            "GATE 1 CLOSED — authorisation. No paid A-TEXT generation may run:\n  - "
            + "\n  - ".join(auth.refusals))


def _check_judge(judge: dict | None) -> None:
    if not judge:
        raise GateClosed("GATE 2 CLOSED — no text judge record was supplied.")
    scope = set(judge.get("qualified_scope") or [])
    if not scope:
        raise GateClosed(
            "GATE 2 CLOSED — no qualified text judge. If no judge qualifies, ZERO image "
            "generations run: there would be nothing to score the output with.")
    required = {"devanagari", "latin"}
    missing = required - scope
    if missing:
        raise GateClosed(
            f"GATE 2 CLOSED — the judge is qualified on {sorted(scope)} but the four frozen items "
            f"span {sorted(required)}. Missing: {sorted(missing)}. Generating images nobody can "
            f"grade is spend with no measurement attached.")


def _check_preflight(preflight_green: bool) -> None:
    if not preflight_green:
        raise GateClosed("GATE 3 CLOSED — preflight is not green.")


def _check_route_ceiling(n_items: int, repeats: int, cfg: dict) -> None:
    for slot, meta in cfg["atex"]["slots"].items():
        planned = n_items * repeats
        if planned > meta["generations"]:
            raise GateClosed(
                f"GATE 5 CLOSED — route {slot} would run {planned} generations but its frozen "
                f"ceiling is {meta['generations']}. The ceiling is a Controller decision and is "
                f"not raisable at runtime.")


# --------------------------------------------------------------------------------------- run
def run(judge: dict | None = None, generator=None, preflight_green: bool = False,
        guard: BudgetGuard | None = None, authorisation_path: Path | None = None,
        dry_run: bool = False, repeats_override: int | None = None,
        stop_on_budget: bool = False) -> dict:
    """Execute the A-TEXT screen behind all five gates. Returns persistable records."""
    cfg = config()
    manifest = items()
    repeats = repeats_override or cfg["atex"]["repeats_per_item"]

    # Gate order is deliberate: the cheapest, most decisive refusals happen first.
    _check_authorisation(authorisation_path, dry_run)
    _check_judge(judge)
    _check_preflight(preflight_green)
    _check_route_ceiling(len(manifest), repeats, cfg)

    if guard is None:
        raise GateClosed("GATE 4 CLOSED — no budget guard.")
    if generator is None:
        raise GateClosed("no generator supplied; this runner never constructs a live one itself.")

    attempts: list[dict] = []
    measurements: list[dict] = []
    cost_ledger: list[dict] = []
    per_route = {slot: 0 for slot in cfg["atex"]["slots"]}
    stopped_reason = None
    seq = 0

    for slot, meta in cfg["atex"]["slots"].items():
        price = NOMINAL_PRICE_USD[slot]
        for repeat_index in range(repeats):
            for item in manifest:
                try:
                    guard.reserve(price)
                except BudgetExceeded:
                    if not stop_on_budget:
                        raise
                    stopped_reason = "budget_exhausted"
                    break

                seq += 1
                attempt_id = f"atex-{slot}-{item['item_id']}-r{repeat_index}"
                # One call = one trial. trial_id equals attempt_id for a root call, always.
                trial_id = attempt_id

                request = {
                    "route": meta["route"],
                    "provider_surface": meta["provider_surface"],
                    "item_id": item["item_id"],
                    "target_string": item["target_string"],
                    "prompt": item["prompt"],
                    "aspect_ratio": item["aspect_ratio"],
                    "seed": None,                    # unseeded, deliberately
                    "seed_policy": "unseeded",
                }
                response = generator(request)        # exactly one call, no loop
                guard.record(price)
                per_route[slot] += 1

                cost_ref = f"ledger-{seq:04d}"
                cost_ledger.append({
                    "cost_ref": cost_ref, "attempt_id": attempt_id, "kind": "generation",
                    "amount_usd": str(price), "basis": "provisional_planning_rate",
                    "synthetic": bool(dry_run), "immutable": True,
                })

                attempts.append({
                    "attempt_id": attempt_id,
                    "trial_id": trial_id,
                    "item_id": item["item_id"],
                    "slot": slot,
                    "route": meta["route"],
                    "provider_surface": meta["provider_surface"],
                    "api_status": response["api_status"],
                    "error_class": response.get("error_class"),
                    "provider_request_id": response.get("provider_request_id"),
                    "seed": None,
                    "seed_policy": "unseeded",
                    "repeat_index": repeat_index,
                    "repeat_of_attempt_id": (
                        f"atex-{slot}-{item['item_id']}-r0" if repeat_index else None),
                    # Named and pinned to None on purpose: this tranche authorises 0 retries.
                    "retry_of_attempt_id": None,
                    "cost_ref": cost_ref,
                    "synthetic": bool(dry_run),
                })

                # The Attempt record exists BEFORE anything asks whether an artifact came back,
                # so a refusal cannot silently vanish from the denominator.
                artifact = response.get("artifact")
                transcription = _fake_transcribe(artifact)
                exact = bool(artifact) and transcription_matches(
                    item["target_string"], transcription)

                measurements.append({
                    "measurement_id": f"m-{seq:04d}",
                    "attempt_id": attempt_id,
                    "trial_id": trial_id,
                    "item_id": item["item_id"],
                    "shape": "transcribe",
                    "role": "primary",
                    "judge": judge.get("candidate"),
                    "transcription": transcription,
                    "exact_match": exact,
                    "absent_reason": None if artifact else "no_artifact_produced",
                    "synthetic": True,
                    "may_populate_registry": False,
                })
            if stopped_reason:
                break
        if stopped_reason:
            break

    scoreable = [m for m in measurements if m["absent_reason"] is None]
    return {
        "record": "EMP-001-atex-screen",
        "dry_run": dry_run,
        "synthetic": True,
        "generations": len(attempts),
        "trials": len({a["trial_id"] for a in attempts}),
        "per_route": per_route,
        "retries": 0,
        "attempts": attempts,
        "measurements": measurements,
        "cost_ledger": cost_ledger,
        "exact_matches": sum(1 for m in scoreable if m["exact_match"]),
        "scoreable_opportunities": len(scoreable),
        "stopped_reason": stopped_reason,
        "registry_rows_written": 0,
        "may_populate_registry": False,
        "evidence_class": "partial_admission_screen_only",
    }


# ---------------------------------------------------- the Registry boundary, actually tested
def attempt_registry_write_with_dry_run_evidence() -> dict:
    """Hand dry-run evidence to the REAL harness and confirm it refuses.

    A docstring promising that synthetic evidence cannot be promoted is worth nothing. This
    exercises the actual boundary in eval/v1/harness/harness.py.
    """
    import tempfile

    sys.path.insert(0, str(REPO_ROOT / "eval/v1/harness"))
    import adapters as A
    from harness import Harness, Instrument

    h = Harness(Path(tempfile.mkdtemp()))
    h.register_instrument(Instrument(
        "atex-dryrun-judge", "v0", {"kind": "synthetic"},
        qualification_status="qualified",          # so only the SYNTHETIC guard can refuse
        capabilities={"text_exactness"},
        fn=A.make_evaluator("atex", {"text_exactness"})))

    item = {"item_id": "ATEXT-01", "modality": "image",
            "measurement_fanout": ["text_exactness"]}
    attempt = h.generate(item, {"model": "dummy", "lane": "image", "unit_price": 0.05},
                         A.dummy_generator)
    m = h.measure(attempt.asset_id, "text_exactness", "atex-dryrun-judge", item=item)

    try:
        h.write_registry_row("text_exactness", "atex-dryrun-judge", [m],
                             conditions={}, difficulty_level=1, repeats_per_item=2)
    except Exception as exc:
        return {"refused": True, "message": str(exc), "registry_rows": len(h.registry_rows)}
    return {"refused": False, "message": "NO refusal — dry-run evidence reached the Registry",
            "registry_rows": len(h.registry_rows)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EMP-001 gated A-TEXT screen.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args(argv)

    if a.live:
        auth = load_authorisation(AUTHORISATION_LOCAL_PATH)
        print("REFUSED: EMP-001 paid A-TEXT generation is not authorised.", file=sys.stderr)
        for r in auth.refusals:
            print(f"  - {r}", file=sys.stderr)
        return 2

    gen = FakeGenerator()
    result = run(judge={"candidate": "dry-run-fake-judge",
                        "qualified_scope": ["devanagari", "latin"], "synthetic": True},
                 generator=gen, preflight_green=True,
                 guard=BudgetGuard(authorised_usd=Decimal("10.00")), dry_run=True)

    registry_boundary = attempt_registry_write_with_dry_run_evidence()
    cfg = config()

    payload = {
        **result,
        "maximum_future_generations": (len(items()) * cfg["atex"]["repeats_per_item"]
                                       * len(cfg["atex"]["slots"])),
        "external_calls": 0,
        "spend_usd": "0",
        "simulated_spend_usd": str(sum(Decimal(c["amount_usd"]) for c in result["cost_ledger"])),
        "registry_boundary_check": registry_boundary,
        "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "note": ("Fake generator, fake judge. This proves the gate order, the 16-call ceiling and "
                 "the Registry refusal. It is not evidence about IMG-01, IMG-02 or any model."),
    }
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")

    print(f"generations: {payload['generations']}  per route: {payload['per_route']}  "
          f"retries: {payload['retries']}")
    print(f"registry rows written: {payload['registry_rows_written']}  "
          f"boundary refused synthetic evidence: {registry_boundary['refused']}")
    print(f"external calls: {payload['external_calls']}   spend USD: {payload['spend_usd']}")
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
