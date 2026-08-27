#!/usr/bin/env python3
"""EMP-001 OCR-FAMILY qualification runner. Transcription only, Devanagari first.

WHY A SECOND RUNNER RATHER THAN A FLAG ON `qualify_text.py`

    The VLM runner iterates two shapes and computes a primary/diagnostic split. An OCR candidate
    has one shape and no diagnostic contrast, so every one of those branches would be dead code
    guarded by `if family == "ocr"`. Dead branches guarded by a family flag are where a future
    change quietly applies VLM semantics to an OCR run.

    Both runners share the things that must not diverge: the item loader, the image resolver, the
    frozen normalisation and the exactness comparison. Those are imported, never copied.

WHAT THIS RUNNER WILL NOT DO

    Open A-TEXT. The OCR contract declares `atext_handoff.accepted_by_atext: false`, and the
    A-TEXT handoff independently refuses evidence produced under any contract but the current VLM
    one. Both are deliberate; either alone would be enough.

EVAL-022 MAKES ZERO EXTERNAL CALLS. Every path here is exercised through an injected recorder.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
sys.path.insert(0, str(PACKAGE_ROOT))

from budget_guard import BudgetGuard, BudgetExceeded, NotAuthorised, open_guard  # noqa: E402
from ocr_providers import (  # noqa: E402
    CLOUD_VISION_USD_PER_IMAGE,
    CloudVisionHttpTransport,
    CloudVisionTextDetection,
)
import qualify_text as QT  # noqa: E402

OCR_CONTRACT = HERE / "qualification-contract-ocr-v1.yaml"
OCR_QUALIFICATION_FILENAME = "ocr-qualification-result.json"
DEFAULT_OUT = HERE / "ocr-qualification-dryrun.json"

# One shape, 96 items, 3 repeats. The absent second shape is the point of this family.
OCR_SHAPE = "transcribe"
OCR_REPEATS = 3
OCR_ITEMS_PER_SCRIPT = 96
OCR_CALLS_PER_SCRIPT = OCR_ITEMS_PER_SCRIPT * OCR_REPEATS          # 288
OCR_MAX_CALLS_BOTH_SCRIPTS = OCR_CALLS_PER_SCRIPT * 2              # 576


def ocr_contract() -> dict:
    return yaml.safe_load(OCR_CONTRACT.read_text(encoding="utf-8"))


def ocr_contract_sha256() -> str:
    return hashlib.sha256(OCR_CONTRACT.read_bytes()).hexdigest()


# --------------------------------------------------------------------------------- budget proof
def ocr_budget_projection(prior_qualification_spend_usd: Decimal | str,
                          ceiling_usd: Decimal | str = "6.00") -> dict:
    """The maximum this family can cost, computed rather than asserted.

    Deliberately ignores Google's first-1,000-free tier. Whether that allowance is still available
    depends on what the rest of the account did this month, which this ledger cannot see. A budget
    proof that depends on an unverifiable external fact is not a proof.
    """
    prior = Decimal(str(prior_qualification_spend_usd))
    ceiling = Decimal(str(ceiling_usd))
    per_image = CLOUD_VISION_USD_PER_IMAGE
    devanagari_calls = OCR_CALLS_PER_SCRIPT
    latin_calls = OCR_CALLS_PER_SCRIPT
    max_calls = devanagari_calls + latin_calls
    max_reservation = per_image * max_calls
    prospective = prior + max_reservation
    return {
        "basis": "USD 1.50 per 1000 Cloud Vision TEXT_DETECTION images",
        "free_tier_relied_on": False,
        "usd_per_image": str(per_image),
        "devanagari_calls": devanagari_calls,
        "latin_calls": latin_calls,
        "max_calls": max_calls,
        "max_ocr_reservation_usd": str(max_reservation),
        "prior_qualification_spend_usd": str(prior),
        "prospective_cumulative_usd": str(prospective),
        "qualification_ceiling_usd": str(ceiling),
        "fits_ceiling": prospective <= ceiling,
    }


# ------------------------------------------------------------------------------------ candidates
class OcrCandidate:
    """One OCR engine plus the image resolver, scored against the frozen battery."""

    manages_own_budget = True

    def __init__(self, engine, images=None, name: str | None = None):
        self.engine = engine
        self.images = images or QT.ImageResolver()
        self.name = name or f"{engine.provider}:{engine.config_alias}"
        self.retries = 0

    def identity(self) -> dict:
        return self.engine.identity()

    def config_sha256(self) -> str:
        return self.engine.config_sha256()

    def call(self, script: str, item: dict, pass_index: int) -> dict:
        image_bytes = self.images.bytes_for(script, item["item_id"])
        image_sha = self.images.verify_bytes(script, item["item_id"], image_bytes)
        trial_id = (f"{script}:{item['item_id']}:{OCR_SHAPE}:p{pass_index}")
        self.engine.call_context = {
            "script": script, "item_id": item["item_id"],
            "shape": OCR_SHAPE, "pass_index": pass_index, "trial_id": trial_id,
        }
        # The target is passed for the BLINDNESS PROOF only. It never enters the payload.
        response = self.engine.transcribe(image_bytes, blind_check_target=item["target"])
        return {
            "text": response.text,
            "api_status": response.api_status,
            "error_class": response.error_class,
            "ambiguous_dispatch": response.ambiguous_dispatch,
            "cost": response.billed_usd,
            "call_record": {
                "trial_id": trial_id,
                "attempt_id": trial_id,
                "script": script,
                "item_id": item["item_id"],
                "shape": OCR_SHAPE,
                "pass_index": pass_index,
                "image_sha256": image_sha,
                "api_status": response.api_status,
                "error_class": response.error_class,
                "ambiguous_dispatch": response.ambiguous_dispatch,
                "billed_usd": str(response.billed_usd) if response.billed_usd is not None else None,
                "billing_state": response.billing_state,
                "cost_basis": response.cost_basis,
                "provider_request_id": response.provider_request_id,
                "retries": 0,
                "one_call_one_trial": True,
                "evidence_mode": "live",
                "synthetic": False,
                **self.engine.identity(),
            },
        }


class FakeOcrCandidate:
    """A deterministic synthetic OCR engine. Zero network, zero spend, perfect reader.

    A perfect reader is not a real one: this proves the harness executes end to end and says
    nothing whatever about any OCR service.
    """

    manages_own_budget = False

    def __init__(self, name: str = "fake-ocr", false_pass_items: set | None = None,
                 false_fail_items: set | None = None, empty_items: set | None = None,
                 infrastructure_items: set | None = None,
                 infrastructure_error_class: str = "provider_error_unavailable",
                 infrastructure_is_ambiguous: bool = False):
        self.name = name
        self.false_pass_items = false_pass_items or set()
        self.false_fail_items = false_fail_items or set()
        self.empty_items = empty_items or set()
        self.infrastructure_items = infrastructure_items or set()
        self.infrastructure_error_class = infrastructure_error_class
        self.infrastructure_is_ambiguous = infrastructure_is_ambiguous
        self.retries = 0
        self.calls = 0

    def identity(self) -> dict:
        return {"family": "ocr", "provider": "synthetic", "config_alias": self.name,
                "endpoint": None, "feature": "TEXT_DETECTION", "language_hints": [],
                "api_version": "synthetic", "config_pinned_at_execution": True}

    def config_sha256(self) -> str:
        return hashlib.sha256(
            json.dumps(self.identity(), sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    def call(self, script: str, item: dict, pass_index: int) -> dict:
        self.calls += 1
        trial_id = f"{script}:{item['item_id']}:{OCR_SHAPE}:p{pass_index}"

        ambiguous = False
        if item["item_id"] in self.infrastructure_items:
            text, status, err = "", "error", self.infrastructure_error_class
            ambiguous = self.infrastructure_is_ambiguous
        elif item["item_id"] in self.empty_items:
            text, status, err = "", "error", "empty_transcription"
        elif item["item_id"] in self.false_pass_items:
            # Reads the INTENDED word rather than the drawn one — the VLM failure mode, simulated.
            text, status, err = item["target"], "ok", None
        elif item["item_id"] in self.false_fail_items:
            text, status, err = item["drawn"] + "​", "ok", None
        else:
            text, status, err = item["drawn"], "ok", None

        return {
            "text": text, "api_status": status, "error_class": err,
            "ambiguous_dispatch": ambiguous, "cost": Decimal("0"),
            "call_record": {
                "trial_id": trial_id, "attempt_id": trial_id, "script": script,
                "item_id": item["item_id"], "shape": OCR_SHAPE, "pass_index": pass_index,
                "image_sha256": None, "api_status": status, "error_class": err,
                "ambiguous_dispatch": ambiguous, "billed_usd": "0",
                "billing_state": "unknown_provisional" if ambiguous else "reported",
                "cost_basis": "synthetic", "provider_request_id": None, "retries": 0,
                "one_call_one_trial": True, "evidence_mode": "fake_live", "synthetic": True,
                **self.identity(),
            },
        }


# --------------------------------------------------------------------------------- the scorer
# Outcomes a scientific metric may be computed from. Anything else is execution state.
SCIENTIFIC_OUTCOMES = ("match", "mismatch", "empty_transcription")
INFRASTRUCTURE_OUTCOME = "infrastructure_failure"


def _observed(item: dict, reply: dict) -> str:
    """What this execution established about the OCR engine — or that it established nothing.

    Three scientific outcomes and one non-outcome:

      match / mismatch        the service read the image; code decided exactness
      empty_transcription     the service ran and was billed, and could not read validated
                              visible text. A RESULT about the engine, and never coerced to
                              `match` — that is how an outage becomes a silent false pass.
      infrastructure_failure  the service did not usefully execute at all. Says nothing about
                              recognition quality and must not touch any gate.
    """
    if reply["api_status"] == "ok":
        if not reply["text"].strip():
            return "empty_transcription"
        return "match" if QT.transcription_matches(item["target"], reply["text"]) else "mismatch"

    # A successful-but-empty execution is reported by the adapter as an error carrying this
    # exact class. It is the one error that is scientific evidence.
    if reply.get("error_class") == "empty_transcription":
        return "empty_transcription"

    return INFRASTRUCTURE_OUTCOME


def _metrics(observations: list[dict]) -> dict:
    """Gate metrics, computed ONLY from scientifically interpretable executions.

    Infrastructure failures are filtered out before any denominator is formed. They are counted
    and reported, but a 429 must never be able to move a recognition-quality number.
    """
    scientific = [o for o in observations if o["observed"] in SCIENTIFIC_OUTCOMES]
    infrastructure = [o for o in observations if o["observed"] == INFRASTRUCTURE_OUTCOME]

    mismatches = [o for o in scientific if o["expected"] == "mismatch"]
    matches = [o for o in scientific if o["expected"] == "match"]
    empties = [o for o in scientific if o["observed"] == "empty_transcription"]

    false_passes = [o for o in mismatches if o["observed"] == "match"]
    false_fails = [o for o in matches if o["observed"] == "mismatch"]
    # An empty transcription is neither a pass nor a fail, so it leaves the false-fail
    # denominator: it is already counted, once, by its own gate.
    readable_matches = [o for o in matches if o["observed"] != "empty_transcription"]
    readable_mismatches = [o for o in mismatches if o["observed"] != "empty_transcription"]

    by_cell: dict[str, set] = {}
    for o in scientific:
        if o["observed"] in ("match", "mismatch"):
            by_cell.setdefault(o["item_id"], set()).add(o["observed"])
    consistency = (sum(1 for v in by_cell.values() if len(v) == 1) / len(by_cell)
                   if by_cell else 0.0)

    return {
        "calls": len(observations),
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
        "unique_empty_transcription_items": len({o["item_id"] for o in empties}),
        "empty_transcription_rate": (round(len(empties) / len(scientific), 4)
                                     if scientific else 0.0),
        "repeat_consistency": round(consistency, 4),
    }


def _score_script(candidate, script: str, guard: BudgetGuard, repeats: int) -> dict:
    """Every item x pass for the single OCR shape. Stops on a budget or dispatch refusal."""
    items = QT._script_items(script)
    observations: list[dict] = []
    call_records: list[dict] = []
    stopped_reason = None
    owns_budget = getattr(candidate, "manages_own_budget", False)

    for pass_index in range(repeats):
        for item in items:
            try:
                if not owns_budget:
                    guard.reserve(CLOUD_VISION_USD_PER_IMAGE)
                reply = candidate.call(script, item, pass_index)
                if not owns_budget:
                    guard.record(reply["cost"])
            except BudgetExceeded:
                stopped_reason = "budget_exhausted"
                break

            if reply.get("call_record"):
                call_records.append(reply["call_record"])

            observations.append({
                "item_id": item["item_id"],
                "shape": OCR_SHAPE,
                "pass": pass_index,
                "expected": item["expected"],
                "observed": _observed(item, reply),
                "api_status": reply["api_status"],
                "error_class": reply.get("error_class"),
                "target": item["target"],
                "rendered_string": item["drawn"],
                "ocr_transcription": reply["text"],
                "failure_class": item.get("failure_class"),
                "failure_group": item.get("failure_group"),
                "edit_detail": item.get("edit_detail"),
                "image_sha256": (reply.get("call_record") or {}).get("image_sha256"),
                "provider_request_id": (reply.get("call_record") or {}).get("provider_request_id"),
                "cost_basis": (reply.get("call_record") or {}).get("cost_basis"),
            })

            # An infrastructure failure is not a result. It stops the run fail-closed, with the
            # trial and its billing already persisted above, and no retry.
            if observations[-1]["observed"] == INFRASTRUCTURE_OUTCOME:
                stopped_reason = (reply.get("error_class")
                                  if not reply.get("ambiguous_dispatch") else "ambiguous_dispatch")
                break
        if stopped_reason:
            break

    c = ocr_contract()
    m = _metrics(observations)

    required = OCR_ITEMS_PER_SCRIPT * repeats
    scientifically_complete = (
        stopped_reason is None
        and m["infrastructure_failures"] == 0
        and m["scientific_executions"] == required)

    failed_gates = []
    if m["false_passes"] > c["mismatch_false_pass_max"]:
        failed_gates.append("mismatch_false_pass")
    if m["match_false_fail_rate"] > c["match_false_fail_rate_max"]:
        failed_gates.append("match_false_fail_rate")
    if m["empty_transcription_rate"] > c["empty_transcription_rate_max"]:
        failed_gates.append("empty_transcription_rate")
    if m["repeat_consistency"] < c["repeat_consistency_min"]:
        failed_gates.append("repeat_consistency")

    return {
        "script": script,
        "primary_shape": OCR_SHAPE,
        "total_dispatches": len(observations),
        "required_executions": required,
        "scientifically_complete": scientifically_complete,
        **m,
        "failed_gates": failed_gates if scientifically_complete else [],
        "gates_that_would_have_failed": failed_gates,
        # `None`, never a bool, when the screen did not finish. Reporting False would let a rate
        # limit read as a quality disqualification; True would promote an unfinished screen.
        "passed": (not failed_gates) if scientifically_complete else None,
        "stopped_reason": stopped_reason,
        "observations": observations,
        "call_records": call_records,
    }


def qualify_ocr_candidate(candidate, guard: BudgetGuard,
                          perceptibility_path: Path | str | None = None) -> dict:
    """Devanagari first. Latin only for survivors, and only after the human review is valid."""
    c = ocr_contract()
    repeats = c["repeats_per_shape"]

    dev = _score_script(candidate, "devanagari", guard, repeats)
    latin = None
    scope = []
    # `is True` deliberately: an INCOMPLETE script reports None, and `if None` would read the same
    # as a scientific failure. It is not the same, and the difference decides whether Latin runs.
    if dev["passed"] is True:
        scope.append("devanagari")
        review = QT.HR.review_status(perceptibility_path) if hasattr(QT, "HR") else {"ok": True}
        if review.get("ok", True):
            latin = _score_script(candidate, "latin", guard, repeats)
            if latin["passed"] is True:
                scope.append("latin")

    return {
        "candidate": candidate.name,
        "family": "ocr",
        "contract_version": c["contract_version"],
        "contract_status": c["status"],
        "identity": candidate.identity(),
        "config_sha256": candidate.config_sha256(),
        "devanagari": dev,
        "latin": latin,
        "scientifically_complete": {
            "devanagari": dev["scientifically_complete"],
            "latin": latin["scientifically_complete"] if latin else None,
        },
        "qualified_scope": scope,
        "qualified_scope_excludes": c["qualified_scope_excludes"],
        "stopped_after": "latin" if latin else "devanagari",
        "stopped_reason": (latin or dev)["stopped_reason"],
        "may_populate_registry": False,
        "may_open_atext": False,
        "atext_note": ("OCR-family evidence cannot open A-TEXT until a Controller decision "
                       "extends the handoff to this family."),
        "synthetic": getattr(candidate, "manages_own_budget", False) is False,
    }


# --------------------------------------------------------------------------------- fingerprint
OCR_FINGERPRINTED_FIELDS = ("run_id", "tranche_id", "mode", "synthetic", "family", "qualified",
                            "candidates", "call_records", "contract_sha256", "config_sha256")


def ocr_qualification_fingerprint(payload: dict) -> str:
    """SHA-256 over the claim AND the evidence that produced it, including the OCR config.

    The config is bound because 'Cloud Vision' is not one instrument: TEXT_DETECTION with no
    hints and TEXT_DETECTION with a Hindi hint are different measurements, and evidence that
    cannot say which it was is not reproducible.
    """
    material = {k: payload.get(k) for k in OCR_FINGERPRINTED_FIELDS}
    canonical = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                           default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_ocr_qualification_result(run, results: list[dict]) -> dict:
    """Assemble the persistable OCR-family qualification record for one EMP-001 run."""
    call_records = []
    for r in results:
        call_records.extend(r["devanagari"]["call_records"])
        if r["latin"]:
            call_records.extend(r["latin"]["call_records"])

    qualified = [{
        "candidate": r["candidate"],
        "family": "ocr",
        "identity": r["identity"],
        "config_sha256": r["config_sha256"],
        "qualified_scope": sorted(r["qualified_scope"]),
    } for r in results if r["qualified_scope"]]

    payload = {
        "record": "EMP-001-ocr-qualification-result",
        "run_id": getattr(run, "run_id", None),
        "tranche_id": "EMP-001",
        "family": "ocr",
        "mode": getattr(run, "mode", "fake_live"),
        "synthetic": getattr(run, "mode", "fake_live") not in ("live",),
        "qualified": qualified,
        "candidates": results,
        "call_records": call_records,
        "contract_version": ocr_contract()["contract_version"],
        "contract_status": ocr_contract()["status"],
        "contract_sha256": ocr_contract_sha256(),
        "config_sha256": results[0]["config_sha256"] if results else None,
        "may_open_atext": False,
        "atext_note": ("A-TEXT does not accept the OCR family. This record is prepared evidence, "
                       "not an authorisation."),
    }
    payload["evidence_fingerprint"] = ocr_qualification_fingerprint(payload)
    return payload


# ---------------------------------------------------------------------------------------- CLI
def persist_ocr_qualification(run, payload: dict) -> Path:
    """Write the canonical OCR qualification record into the run's evidence directory."""
    run.evidence_dir.mkdir(parents=True, exist_ok=True)
    path = run.evidence_dir / OCR_QUALIFICATION_FILENAME
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True,
                               default=str) + "\n", encoding="utf-8")
    return path


def run_live_ocr(guard, http=None, run=None) -> dict:
    """The real Cloud Vision path. Exactly one candidate, exactly the frozen configuration.

    The plan is checked against the frozen protocol BEFORE anything is constructed. A run that
    could dispatch more than 576 images, or reserve more than USD 0.864, is refused here rather
    than discovered halfway through a paid screen.
    """
    max_reservation = CLOUD_VISION_USD_PER_IMAGE * OCR_MAX_CALLS_BOTH_SCRIPTS
    if max_reservation > Decimal("0.864"):
        raise NotAuthorised(
            f"the frozen OCR protocol would reserve {max_reservation}, above the authorised "
            f"USD 0.864. The protocol is frozen; this is a configuration error, not a budget "
            f"question.")

    engine = CloudVisionTextDetection(
        transport=CloudVisionHttpTransport(http=http),
        guard=guard)
    candidate = OcrCandidate(engine, name="google_cloud_vision:cloud-vision-text-detection-v1")

    result = qualify_ocr_candidate(candidate, guard)
    payload = build_ocr_qualification_result(run, [result])
    payload["dispatches"] = sum(
        len((result.get(s) or {}).get("call_records", [])) for s in ("devanagari", "latin"))
    payload["max_authorised_calls"] = OCR_MAX_CALLS_BOTH_SCRIPTS
    payload["max_authorised_reservation_usd"] = str(max_reservation)

    if payload["dispatches"] > OCR_MAX_CALLS_BOTH_SCRIPTS:
        raise NotAuthorised(
            f"{payload['dispatches']} dispatches exceeds the frozen maximum of "
            f"{OCR_MAX_CALLS_BOTH_SCRIPTS}.")

    if run is not None:
        payload["canonical_path"] = str(persist_ocr_qualification(run, payload))
    return payload


def _fake_live(out: Path, run=None) -> dict:
    """The positive control: a clean synthetic OCR candidate across BOTH scripts, zero network."""
    guard = BudgetGuard(authorised_usd=Decimal("6.00"))
    candidate = FakeOcrCandidate(name="clean-synthetic-ocr")
    result = qualify_ocr_candidate(candidate, guard)
    payload = build_ocr_qualification_result(
        run or type("R", (), {"run_id": "ocr-fake-live", "mode": "fake_live"})(), [result])
    payload["external_calls"] = 0
    payload["spend_usd"] = "0"
    payload["dispatches"] = candidate.calls
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True,
                              default=str) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EMP-001 OCR-family qualification (readiness).")
    ap.add_argument("--fake-live", action="store_true",
                    help="clean synthetic OCR candidate, both scripts, zero network, zero spend")
    ap.add_argument("--live", action="store_true",
                    help="real paid Cloud Vision execution; requires explicit authorisation")
    ap.add_argument("--authorisation", default=None)
    ap.add_argument("--run-root", default=None,
                    help="persistent EMP-001 run root; enables the durable tranche ledger")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--budget-proof", action="store_true",
                    help="print the conservative maximum paid cost for a full OCR screen")
    ap.add_argument("--prior-spend", default="0.6712415")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args(argv)

    if a.budget_proof:
        print(json.dumps(ocr_budget_projection(a.prior_spend), indent=2, sort_keys=True))
        return 0

    if a.live:
        # GATE 1. Fails closed on a missing, disabled or over-wide authorisation file, exactly as
        # the VLM runner does. There is no separate OCR authorisation: this is the same tranche.
        authorisation = open_guard(a.authorisation) if a.authorisation else open_guard()

        run = None
        guard = authorisation
        if a.run_root and a.run_id:
            import spend_ledger as SL

            root = Path(a.run_root)
            try:
                run = SL.TrancheRun.open(root, a.run_id)
            except SL.LedgerCorrupt:
                run = SL.TrancheRun.create(root, a.run_id,
                                           authorisation_path=a.authorisation or "", mode="live")
            # The SAME qualification stage the VLM runs used, so prior qualification spend is
            # already inside this ceiling rather than starting a fresh USD 6.
            guard = SL.TrancheBudget(run).stage("qualification")

        payload = run_live_ocr(guard, http=None, run=run)
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True,
                                  default=str) + "\n", encoding="utf-8")
        c = payload["candidates"][0]
        dev, latin = c["devanagari"], c["latin"]
        print(f"ocr live: {payload['dispatches']} dispatches")
        print(f"  devanagari calls={dev['calls']} complete={dev['scientifically_complete']} "
              f"passed={dev['passed']} gates={dev['failed_gates']}")
        latin_line = ("not run" if not latin
                      else f"calls={latin['calls']} complete={latin['scientifically_complete']} "
                           f"passed={latin['passed']} gates={latin['failed_gates']}")
        print(f"  latin      {latin_line}")
        print(f"  qualified_scope={c['qualified_scope']}  may_open_atext={payload['may_open_atext']}")
        print(f"written: {out}")
        if payload.get("canonical_path"):
            print(f"canonical: {payload['canonical_path']}")
        return 0

    if a.fake_live:
        payload = _fake_live(Path(a.out))
        dev = payload["candidates"][0]["devanagari"]
        latin = payload["candidates"][0]["latin"]
        print(f"ocr fake-live: {payload['dispatches']} dispatches, 0 network calls")
        print(f"  devanagari calls={dev['calls']} passed={dev['passed']}")
        print(f"  latin      calls={latin['calls'] if latin else 0} "
              f"passed={latin['passed'] if latin else None}")
        print(f"  qualified_scope={payload['candidates'][0]['qualified_scope']}")
        print(f"  may_open_atext={payload['may_open_atext']}")
        print(f"external calls: {payload['external_calls']}   spend USD: {payload['spend_usd']}")
        print(f"written: {a.out}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
