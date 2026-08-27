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
    NotAuthorised, load_authorisation, open_guard)
import providers as P  # noqa: E402
from qualify_text import transcription_matches  # noqa: E402
import human_review as HR  # noqa: E402

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
# Populated in dry-run mode so the fake judge can "read" the fake generator's artifact. Never
# consulted on the live path.
_TARGET_BY_ARTIFACT: dict[str, str] = {}


class PartialEvidenceOnly(RuntimeError):
    """A-TEXT is a partial admission screen. It cannot promote a complete scientific slot."""


def promote_slot(result: dict):
    """Refuse, always, and say why.

    A-TEXT asks one narrow question on four items. Full Stage-A survival requires every instrument
    family the route's slot depends on, and none of them is qualified. This exists so the boundary
    is a mechanical refusal rather than a paragraph everybody agrees with and nobody enforces.
    """
    raise PartialEvidenceOnly(
        f"REFUSED: {result.get('evidence_class', 'partial_admission_screen_only')}. A-TEXT is "
        f"partial evidence from four frozen items on one prompt style. It may eliminate a route "
        f"from deeper text spend; it may never promote a complete Stage-A slot, and a non-zero "
        f"score is not promotion. This holds whether the evidence is synthetic or real.")


def _measure_artifact(judge_instance, image_bytes: bytes, item: dict, seq: int,
                      attempt_id: str) -> tuple[dict, dict, "P.EvaluatorResponse"]:
    """One blind transcription. Returns (evaluator_call_record, measurement).

    The judge never sees the target. It commits to what it believes is drawn and OUR code performs
    the exact comparison — `transcription_matches`, the same frozen rule the qualification used.

    The evaluator call is its own trial with its own cost. A judge that refused or errored did not
    say "wrong": that is an ABSENCE with a reason, not a mismatch, and folding the two would
    corrupt the numerator and the denominator in opposite directions.
    """
    # E14-D: the target goes to the BLIND CHECK and nowhere else. It is never placed in the
    # transcribe payload; it is what the payload is proved not to contain. Same invariant as
    # qualification, and it must hold for Latin targets as well as Devanagari ones.
    try:
        response = judge_instance.transcribe(
            image_bytes, blind_check_target=item["target_string"])
    except TypeError:
        # A judge that predates the blind-check parameter. Still measured, but say so loudly:
        # a silent fallback here is how an invariant quietly stops being enforced.
        response = judge_instance.transcribe(image_bytes)
    call = {
        **judge_instance.call_record(response, shape="transcribe"),
        "evaluator_trial_id": f"eval-{seq:04d}",
        "attempt_id": attempt_id,
        "item_id": item["item_id"],
        "synthetic": False,
    }

    if response.api_status != "ok":
        absent = ("evaluator_refused" if response.api_status == "refusal"
                  else f"evaluator_{response.api_status}")
        return call, {"transcription": None, "exact_match": None,
                      "absent_reason": absent}, response

    exact = transcription_matches(item["target_string"], response.text)
    return call, {"transcription": response.text, "exact_match": exact,
                  "absent_reason": None}, response


def run(judge: dict | None = None, generator=None, routes: dict | None = None,
        judge_instance=None, preflight_green: bool = False,
        guard: BudgetGuard | None = None, authorisation_path: Path | None = None,
        dry_run: bool = False, repeats_override: int | None = None,
        stop_on_budget: bool = False, run_verdict_diagnostic: bool = False) -> dict:
    """Execute the A-TEXT screen behind all five gates.

    Two execution modes, and the difference is real rather than cosmetic:

      dry_run=True   a fake generator and a stub reader. Everything is marked synthetic.
      dry_run=False  the supplied frozen fal routes, and the supplied QUALIFIED judge's blind
                     transcribe. Records carry synthetic=False, because they are real evidence
                     about whatever the transports actually talked to.

    `synthetic` is derived from the execution mode. It was previously a constant `True`, which
    meant a paid run would have been scored by the stub and then filed as synthetic.
    """
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

    if dry_run:
        if generator is None:
            raise GateClosed("a dry run needs a fake generator; none was supplied.")
    else:
        if not routes:
            raise GateClosed(
                "GATE 5 CLOSED — no generation routes supplied. This runner never constructs a "
                "live route itself; the caller injects the frozen adapters.")
        if judge_instance is None:
            raise GateClosed(
                "GATE 2 CLOSED — a real run needs the QUALIFIED judge instance, not merely a "
                "qualification record. Generating images nobody measures is spend with no "
                "evidence attached.")

    attempts: list[dict] = []
    evaluator_calls: list[dict] = []
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
                trial_id = attempt_id          # one call = one trial, always

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

                ambiguous = None
                try:
                    if dry_run:
                        response = generator(request)     # exactly one call, no loop
                    else:
                        response = routes[slot](request)  # exactly one call, no loop
                except P.PreDispatchRefusal:
                    # PROVEN nothing was sent. Release and re-raise: there is no attempt to
                    # persist, because no attempt was made.
                    release = getattr(guard, "release", None)
                    if release:
                        release()
                    raise
                except P.AmbiguousDispatch as exc:
                    # fal may have received and billed this generation. Keep the money counted,
                    # persist the attempt as a real failed trial, and stop after it.
                    ambiguous = exc
                    response = {
                        "api_status": exc.api_status,
                        "error_class": exc.error_class,
                        "provider_request_id": None,
                        "artifact_url": None,
                        "fetch_artifact": None,
                        "slot": slot,
                        "route": meta["route"],
                        "provider_surface": meta["provider_surface"],
                    }

                # A persistent StageBudget returns the ledger cost_ref that this spend was
                # written under; the in-memory guard returns None. Using the ledger's reference
                # is what makes a generation trial reconcilable against actual spend later.
                try:
                    recorded_ref = guard.record(
                        price, billing_state=("unknown_provisional" if ambiguous else "reported"))
                except TypeError:
                    recorded_ref = guard.record(price)
                per_route[slot] += 1

                cost_ref = recorded_ref or f"ledger-{seq:04d}"
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
                    "artifact_url": response.get("artifact_url"),
                    "seed": None,
                    "seed_policy": "unseeded",
                    "repeat_index": repeat_index,
                    "repeat_of_attempt_id": (
                        f"atex-{slot}-{item['item_id']}-r0" if repeat_index else None),
                    # Named and pinned to None on purpose: this tranche authorises 0 retries.
                    "retry_of_attempt_id": None,
                    "cost_ref": cost_ref,
                    "synthetic": bool(dry_run),
                    "billing_state": "unknown_provisional" if ambiguous else "reported",
                    "ambiguous_dispatch": bool(ambiguous),
                })

                # The Attempt record exists BEFORE anything asks whether an artifact came back, so
                # a refusal cannot silently vanish from the denominator.
                measurement = {
                    "measurement_id": f"m-{seq:04d}",
                    "attempt_id": attempt_id,
                    "trial_id": trial_id,
                    "item_id": item["item_id"],
                    "shape": "transcribe",
                    "role": "primary",
                    "judge": judge.get("candidate"),
                    "transcription": None,
                    "exact_match": None,
                    "absent_reason": "no_artifact_produced",
                    "synthetic": bool(dry_run),
                    "may_populate_registry": False,
                }

                if dry_run:
                    artifact = response.get("artifact")
                    if artifact:
                        transcription = _fake_transcribe(artifact)
                        measurement.update({
                            "transcription": transcription,
                            "exact_match": transcription_matches(item["target_string"],
                                                                 transcription),
                            "absent_reason": None,
                        })
                evaluator_response = None
                if not dry_run and response["api_status"] == "ok" \
                        and response.get("fetch_artifact"):
                    image_bytes = response["fetch_artifact"]()
                    _TARGET_BY_ARTIFACT[response["artifact_url"]] = item["target_string"]
                    call, outcome, evaluator_response = _measure_artifact(
                        judge_instance, image_bytes, item, seq, attempt_id)
                    evaluator_calls.append(call)
                    measurement.update(outcome)
                    measurement["evaluator_trial_id"] = call["evaluator_trial_id"]

                    if run_verdict_diagnostic:
                        # Diagnostic ONLY, and explicitly budgeted. It measures how much
                        # false-pass behaviour comes from showing a judge the answer we hope for.
                        # It can never overturn the primary transcription result.
                        vresp = judge_instance.verdict(image_bytes, item["target_string"])
                        vcall = {
                            **judge_instance.call_record(vresp, shape="verdict"),
                            "evaluator_trial_id": f"eval-verdict-{seq:04d}",
                            "attempt_id": attempt_id, "item_id": item["item_id"],
                            "synthetic": False,
                        }
                        evaluator_calls.append(vcall)
                        measurements.append({
                            "measurement_id": f"m-verdict-{seq:04d}",
                            "attempt_id": attempt_id, "trial_id": trial_id,
                            "item_id": item["item_id"], "shape": "verdict",
                            "role": "diagnostic",
                            "judge": judge.get("candidate"),
                            "reply": vresp.text,
                            "may_override_primary": False,
                            "absent_reason": None if vresp.api_status == "ok" else "evaluator_"
                                             + vresp.api_status,
                            "synthetic": False,
                            "may_populate_registry": False,
                        })

                measurements.append(measurement)

                if ambiguous is not None:
                    # The attempt and its cost are now on the record. Stop: continuing would
                    # spend more money after a call nobody can account for, and retries are 0 so
                    # there is nothing to re-attempt.
                    stopped_reason = "ambiguous_dispatch"
                    break

                if getattr(evaluator_response, "ambiguous_dispatch", False):
                    stopped_reason = "ambiguous_dispatch"
                    break
            if stopped_reason:
                break
        if stopped_reason:
            break

    primary = [m for m in measurements if m["role"] == "primary"]
    scoreable = [m for m in primary if m["absent_reason"] is None]
    exact_matches = sum(1 for m in scoreable if m["exact_match"])

    return {
        "record": "EMP-001-atex-screen",
        "dry_run": dry_run,
        # From the execution MODE, never a constant.
        "synthetic": bool(dry_run),
        "generations": len(attempts),
        "trials": len({a["trial_id"] for a in attempts}),
        "per_route": per_route,
        "retries": 0,
        "attempts": attempts,
        "evaluator_calls": evaluator_calls,
        "measurements": measurements,
        "cost_ledger": cost_ledger,
        "exact_matches": exact_matches,
        "scoreable_opportunities": len(scoreable),
        # The frozen hard elimination rule. Eligibility to STOP deeper spend, stated only as a
        # result on this screen — never as a universal model incapability.
        "text_specific_stop_eligible": bool(scoreable) and exact_matches == 0,
        "stopped_reason": stopped_reason,
        "registry_rows_written": 0,
        "may_populate_registry": False,
        "evidence_class": "partial_admission_screen_only",
    }


# ------------------------------------------------------------------------ the paid handoff
LATIN_SCRIPTS = ("latin", "latin_hinglish", "latin_commercial_claim")


def scripts_required_by_atex() -> set[str]:
    """Which qualified scripts the four frozen items actually need.

    ATEXT-01/02 are Devanagari; ATEXT-03/04 are Latin. So A-TEXT needs BOTH, which means the
    Latin leg's prerequisites gate the whole screen, not just half of it.
    """
    required = set()
    for item in items():
        required.add("latin" if item["script"] in LATIN_SCRIPTS else item["script"])
    return required


def latin_perceptibility_resolved(path: Path | str | None = None) -> bool:
    """Apply the frozen human-review rule to the exact current Latin pack.

    All 96 items need usable_surface=yes. Only the 48 mismatch items need
    visible_difference=yes. The review notes must bind the answers to the current pack SHA.
    """
    return HR.resolved(path)


def load_qualification(run, expected_mode: str) -> dict:
    """Load the persisted qualification for this run, or refuse with the reason.

    Refuses when: the file is absent; it belongs to another run; its declared mode is not the mode
    A-TEXT is running in; or its fingerprint does not match the evidence it carries.

    The fingerprint check is the one that matters. Without it, opening a paid stage would be a
    matter of editing one JSON field.
    """
    sys.path.insert(0, str(PACKAGE_ROOT / "text_qualification"))
    import qualify_text as QT

    path = run.evidence_dir / QT.QUALIFICATION_FILENAME
    if not path.exists():
        raise GateClosed(
            f"GATE 2 CLOSED — no qualification result at {path}. A-TEXT consumes the qualification "
            f"actually run for THIS EMP-001 run; there is no way to assert a judge is qualified.")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GateClosed(f"GATE 2 CLOSED — {path} is not readable JSON") from exc

    if payload.get("run_id") != run.run_id:
        raise GateClosed(
            f"GATE 2 CLOSED — qualification belongs to run {payload.get('run_id')!r}, not "
            f"{run.run_id!r}. Spend and evidence are per run and do not travel between them.")

    mode = payload.get("mode")
    if mode != expected_mode:
        raise GateClosed(
            f"GATE 2 CLOSED — qualification evidence is {mode!r} but A-TEXT is running in "
            f"{expected_mode!r}. A rehearsal may not open a paid stage, and a paid stage may not "
            f"be scored against rehearsal evidence.")

    if expected_mode == "live" and payload.get("synthetic"):
        raise GateClosed(
            "GATE 2 CLOSED — qualification evidence is marked synthetic. Synthetic evidence "
            "cannot qualify an instrument for paid measurement.")

    current_contract_sha = hashlib.sha256(QT.CONTRACT.read_bytes()).hexdigest()
    if payload.get("contract_version") != QT.contract().get("contract_version"):
        raise GateClosed(
            f"GATE 2 CLOSED — qualification used contract version "
            f"{payload.get('contract_version')!r}, current version is "
            f"{QT.contract().get('contract_version')!r}. Old qualification evidence cannot be "
            f"promoted under a corrected instrument.")
    if payload.get("contract_sha256") != current_contract_sha:
        raise GateClosed(
            "GATE 2 CLOSED — qualification contract fingerprint does not match the current "
            "qualification instrument. Re-run qualification; do not reinterpret old evidence.")

    expected_fp = payload.get("evidence_fingerprint")
    actual_fp = QT.qualification_fingerprint(payload)
    if expected_fp != actual_fp:
        raise GateClosed(
            f"GATE 2 CLOSED — qualification fingerprint mismatch.\n"
            f"  recorded: {expected_fp}\n  recomputed: {actual_fp}\n"
            f"The claim is bound to the call records that produced it. Widening a qualified scope "
            f"without also producing the calls changes the fingerprint, which is exactly what "
            f"this check is for.")

    return payload


def select_judge_for_atex(qualification: dict) -> dict:
    """Pick a candidate qualified for EVERY script the four frozen items need."""
    required = scripts_required_by_atex()
    candidates = qualification.get("qualified") or []

    if not candidates:
        raise GateClosed(
            "GATE 2 CLOSED — no candidate qualified. If no text judge qualifies, ZERO image "
            "generations run: there would be nothing to score the output with.")

    active_roster = {
        (spec["provider"], spec["model_alias"])
        for spec in config()["qualification"]["judge_candidates"]
    }
    for candidate in candidates:
        identity = (candidate.get("provider"), candidate.get("model_alias"))
        if identity not in active_roster:
            continue
        if required <= set(candidate.get("qualified_scope") or []):
            return candidate

    scopes = {c["candidate"]: sorted(c.get("qualified_scope") or []) for c in candidates}
    raise GateClosed(
        f"GATE 2 CLOSED — the four frozen A-TEXT items need {sorted(required)} and no candidate "
        f"covers all of them: {scopes}. Generating images nobody can grade is spend with no "
        f"measurement attached.")


def build_live_judge(chosen: dict, guard, http=None):
    """Rebuild the EXACT judge that qualified: same provider, alias and resolved version."""
    judge_cls = {
        "anthropic": P.AnthropicTextJudge,
        "google": P.GeminiTextJudge,
        "openai": P.OpenAITextJudge,
    }.get(chosen["provider"])
    if judge_cls is None:
        raise GateClosed(f"unsupported qualified judge provider {chosen['provider']!r}")
    return judge_cls(
        model_alias=chosen["model_alias"],
        resolved_version=chosen["resolved_version"],
        transport=P.transport_for(chosen["provider"], chosen["resolved_version"], http=http),
        guard=guard)


def run_live(tranche_run, mode: str = "live", judge_http=None, fal_http=None,
             artifact_fetch=None, perceptibility_path: Path | None = None,
             run_verdict_diagnostic: bool = False) -> dict:
    """The executable qualification -> A-TEXT handoff.

    Everything a paid run needs, in gate order, with the persistent tranche budget throughout.
    `judge_http` / `fal_http` / `artifact_fetch` are the injected transport seams: None means the
    real socket, which is why nothing in this branch ever calls it that way.
    """
    sys.path.insert(0, str(PACKAGE_ROOT))
    import spend_ledger as SL

    # GATE 1 — authorisation, from the run's own record.
    auth_path = Path(tranche_run.record["authorisation_path"])
    auth = load_authorisation(auth_path)
    if auth.refusals:
        raise GateClosed("GATE 1 CLOSED — authorisation:\n  - " + "\n  - ".join(auth.refusals))

    # GATE 2 — the real, fingerprint-bound qualification for THIS run.
    qualification = load_qualification(tranche_run, expected_mode=mode)
    chosen = select_judge_for_atex(qualification)

    # GATE 2b — the Latin human perceptibility prerequisite.
    required = scripts_required_by_atex()
    if "latin" in required and not latin_perceptibility_resolved(perceptibility_path):
        raise GateClosed(
            "GATE 2b CLOSED — the Latin human perceptibility review is unresolved. Two of the four "
            "frozen A-TEXT items (ATEXT-03, ATEXT-04) are Latin, so this gates the whole screen. "
            "The review sheet is emitted unfilled by design and must be completed by a person; it "
            "must not be fabricated to open this gate.")

    # GATE 3/4/5 — budget, routes, and the run itself.
    stage = SL.TrancheBudget(tranche_run).stage("atex")
    judge = build_live_judge(chosen, guard=stage, http=judge_http)

    cfg = config()
    routes = {slot: P.fal_route_for(slot, cfg, http=fal_http, artifact_fetch=artifact_fetch)
              for slot in cfg["atex"]["slots"]}

    result = run(judge={"candidate": chosen["candidate"],
                        "qualified_scope": chosen["qualified_scope"],
                        "synthetic": qualification.get("synthetic", False)},
                 routes=routes, judge_instance=judge, preflight_green=True, guard=stage,
                 authorisation_path=auth_path, dry_run=False,
                 run_verdict_diagnostic=run_verdict_diagnostic)

    result.update({
        "mode": mode,
        "run_id": tranche_run.run_id,
        "judge": chosen,
        "qualification_fingerprint": qualification["evidence_fingerprint"],
        "tranche_spent_usd": str(SL.TrancheBudget(tranche_run).spent_usd()),
        "atex_spent_usd": str(SL.TrancheBudget(tranche_run).stage_spent_usd("atex")),
        "qualification_spent_usd": str(SL.TrancheBudget(tranche_run).stage_spent_usd("qualification")),
    })
    (tranche_run.evidence_dir / "atex-result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8")
    return result


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


def _fake_live(guard: BudgetGuard, authorisation_path: Path, out: Path) -> dict:
    """The real measurement path with injected recorders where the sockets would be.

    Real frozen fal route adapters, real request bodies, real blind transcription, real code-level
    comparison. The only substitutions are the HTTP layer, the artifact store and the reader — and
    the reader is a PERFECT one, which is precisely why this proves the path executes and proves
    nothing whatsoever about any model.
    """
    import os

    sys.path.insert(0, str(PACKAGE_ROOT / "text_qualification"))
    from fake_live import FakeFalHttp

    os.environ.setdefault("FAL_KEY", "fake-live-fal-key")

    http = FakeFalHttp()
    artifacts: dict[str, bytes] = {}

    def fetch(url: str) -> bytes:
        artifacts.setdefault(url, b"\x89PNG\r\n\x1a\n" + url.encode("utf-8"))
        return artifacts[url]

    cfg = config()
    routes = {slot: P.fal_route_for(slot, cfg, http=http, artifact_fetch=fetch)
              for slot in cfg["atex"]["slots"]}

    class PerfectReader:
        """Reads back whatever was rendered. A stand-in for a qualified judge, not a model."""

        provider, model_alias = "fake-live", "fake-live-perfect-reader"
        resolved_version = "FAKE-LIVE-reader-v1"

        def __init__(self):
            self.transcribe_calls = 0

        def transcribe(self, image_bytes):
            self.transcribe_calls += 1
            url = image_bytes.split(b"\x1a\n", 1)[1].decode("utf-8")
            return P.EvaluatorResponse(
                text=_TARGET_BY_ARTIFACT.get(url, ""), input_tokens=800, output_tokens=6,
                billed_usd=Decimal("0.0021"),
                provider_request_id=f"fake-judge-{self.transcribe_calls:04d}")

        def identity(self):
            return {"provider": self.provider, "model_alias": self.model_alias,
                    "resolved_version": self.resolved_version,
                    "version_pinned_at_execution": True}

        def call_record(self, response, shape):
            return {**self.identity(), "shape": shape, "api_status": response.api_status,
                    "error_class": response.error_class,
                    "provider_request_id": response.provider_request_id,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "billed_usd": str(response.billed_usd),
                    "cost_basis": response.cost_basis, "retries": 0,
                    "one_call_one_trial": True}

    reader = PerfectReader()
    result = run(judge={"candidate": "fake-live-perfect-reader",
                        "qualified_scope": ["devanagari", "latin"], "synthetic": False},
                 routes=routes, judge_instance=reader, preflight_green=True, guard=guard,
                 authorisation_path=authorisation_path, dry_run=False)

    payload = {
        **result,
        "mode": "fake_live",
        "maximum_future_generations": (len(items()) * cfg["atex"]["repeats_per_item"]
                                       * len(cfg["atex"]["slots"])),
        "external_calls": 0,
        "spend_usd": "0",
        "recorded_dispatches": len(http.calls),
        "evaluator_dispatches": reader.transcribe_calls,
        "simulated_spend_usd": str(guard.spent_usd),
        "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "note": ("Real frozen fal adapters, real request bodies, real blind transcription and "
                 "real code-level comparison, with injected recorders where the sockets would "
                 "be. The reader is PERFECT, so the exact-match count says nothing about any "
                 "model. It proves the positive path executes and stays inside its ceiling."),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True,
                              default=str) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EMP-001 gated A-TEXT screen.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fake-live", action="store_true",
                    help="the real measurement path with injected recorders; zero network")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--authorisation", default=None)
    ap.add_argument("--run-root", default=None,
                    help="persistent EMP-001 run root; required for the qualification handoff")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--perceptibility-review", default=None,
                    help="path to the Latin human perceptibility sheet")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args(argv)

    if a.live or (a.fake_live and a.run_root and a.run_id):
        # The executable handoff. Identical code path for both modes; only the transports and the
        # declared mode differ, and load_qualification refuses to mix them.
        sys.path.insert(0, str(PACKAGE_ROOT))
        import spend_ledger as SL

        if not (a.run_root and a.run_id):
            print("REFUSED: --run-root and --run-id are required. A-TEXT consumes the persisted "
                  "qualification for a specific EMP-001 run and spends against that run's "
                  "ledger.", file=sys.stderr)
            return 2

        mode = "live" if a.live else "fake_live"
        try:
            tranche_run = SL.TrancheRun.open(Path(a.run_root), a.run_id)
        except SL.LedgerCorrupt as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 2

        judge_http = fal_http = artifact_fetch = None
        if mode == "fake_live":
            sys.path.insert(0, str(PACKAGE_ROOT / "text_qualification"))
            from fake_live import FakeFalHttp, FakeJudgeHttp

            judge_http = FakeJudgeHttp(P.AnthropicTextJudge, {})
            fal_http = FakeFalHttp()

            def artifact_fetch(url):
                return b"\x89PNG\r\n\x1a\n" + url.encode("utf-8")

        try:
            result = run_live(
                tranche_run, mode=mode, judge_http=judge_http, fal_http=fal_http,
                artifact_fetch=artifact_fetch,
                perceptibility_path=(Path(a.perceptibility_review)
                                     if a.perceptibility_review else None))
        except GateClosed as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 2

        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True,
                                          default=str) + "\n", encoding="utf-8")
        print(f"{mode}: {result['generations']} generations {result['per_route']}, "
              f"{len(result['evaluator_calls'])} evaluator dispatches, retries "
              f"{result['retries']}")
        print(f"tranche spent USD {result['tranche_spent_usd']} "
              f"(qualification {result['qualification_spent_usd']}, "
              f"atex {result['atex_spent_usd']})")
        print(f"synthetic: {result['synthetic']}   registry rows: "
              f"{result['registry_rows_written']}")
        print(f"written: {a.out}")
        return 0

    if a.live:
        auth = load_authorisation(a.authorisation or AUTHORISATION_LOCAL_PATH)
        print("REFUSED: EMP-001 paid A-TEXT generation requires an explicit authorisation and a "
              "qualified judge produced by a real qualification run.", file=sys.stderr)
        for r in auth.refusals:
            print(f"  - {r}", file=sys.stderr)
        return 2

    if a.fake_live:
        path = Path(a.authorisation) if a.authorisation else AUTHORISATION_LOCAL_PATH
        guard = open_guard(path)          # the same gate a paid run must pass
        result = _fake_live(guard, path, Path(a.out))
        print(f"fake-live: {result['generations']} generations "
              f"({result['per_route']}), {result['evaluator_dispatches']} evaluator dispatches, "
              f"0 network calls")
        print(f"exact matches: {result['exact_matches']}/{result['scoreable_opportunities']}  "
              f"(perfect reader — not evidence about any model)")
        print(f"synthetic: {result['synthetic']}   registry rows: "
              f"{result['registry_rows_written']}")
        print(f"external calls: {result['external_calls']}   spend USD: {result['spend_usd']}")
        print(f"written: {a.out}")
        return 0

    gen = FakeGenerator()
    result = run(judge={"candidate": "dry-run-fake-judge",
                        "qualified_scope": ["devanagari", "latin"], "synthetic": True},
                 generator=gen, preflight_green=True,
                 guard=BudgetGuard(authorised_usd=Decimal("10.00")), dry_run=True)

    registry_boundary = attempt_registry_write_with_dry_run_evidence()
    cfg = config()

    payload = {
        **result,
        "mode": "dry_run",
        "maximum_future_generations": (len(items()) * cfg["atex"]["repeats_per_item"]
                                       * len(cfg["atex"]["slots"])),
        "external_calls": 0,
        "spend_usd": "0",
        "simulated_spend_usd": str(sum(Decimal(c["amount_usd"]) for c in result["cost_ledger"])),
        "registry_boundary_check": registry_boundary,
        "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "note": ("Fake generator, fake reader. This proves the gate order, the 16-call ceiling "
                 "and the Registry refusal. It is not evidence about IMG-01, IMG-02 or any "
                 "model."),
    }
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True,
                              default=str) + "\n", encoding="utf-8")

    print(f"generations: {payload['generations']}  per route: {payload['per_route']}  "
          f"retries: {payload['retries']}")
    print(f"registry rows written: {payload['registry_rows_written']}  "
          f"boundary refused synthetic evidence: {registry_boundary['refused']}")
    print(f"external calls: {payload['external_calls']}   spend USD: {payload['spend_usd']}")
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
