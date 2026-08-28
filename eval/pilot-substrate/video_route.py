#!/usr/bin/env python3
"""EVAL-035 (corrected): one pilot-capable video route. Direct Gemini Developer API, Veo 3.1 Fast.

ROUTE POLICY (Controller/user decision, 2026-08-28)

    `CONTROLLER-DIRECT-GEMINI-T1-ROUTE-REVISION-2026-08-28.md` supersedes the first-pass fal
    selection: for Google generation models this project talks to the DIRECT Gemini Developer
    API with `GEMINI_API_KEY` — no aggregator, no aggregator retry/fallback/auth layer. The
    temporary T1 executor is `veo-3.1-fast-generate-preview`, 720p, 9:16 for the Aight pilot.
    T1 plumbing only: not model qualification, not a Registry row, not a claim Veo is best.
    Veo's pilot role is the generative motion/visual plate; exact brand/text elements are
    composited deterministically later and are NOT this route's problem.

NOTHING HERE CONTACTS A PROVIDER BY ITSELF.

    Importing this module makes no call. Constructing a route makes no call and reads no API
    key. A route with no injected transport REFUSES to dispatch, and a route with a transport
    but no budget guard also refuses. The only way to spend money is to hand the route both a
    live transport (built explicitly via `LiveGeminiTransport`) and a guard opened from the
    machine-verifiable PILOT-001 authorisation chain (`pilot_authorisation.py`) — which the
    committed repository state cannot open today, by design.

THE PROVIDER CONTRACT (current official Google docs, fetched 2026-08-28)

    Source: ai.google.dev/gemini-api/docs/veo and .../docs/pricing.

      start      POST https://generativelanguage.googleapis.com/v1beta/models/
                     veo-3.1-fast-generate-preview:predictLongRunning
                 header `x-goog-api-key: $GEMINI_API_KEY`
                 body {"instances":[{"prompt": ...}],
                       "parameters":{"aspectRatio","resolution","durationSeconds"}}
                 -> {"name": "<operation name>"}
      poll       GET  https://generativelanguage.googleapis.com/v1beta/<operation name>
                 -> {"name", "done": bool, then "response" or "error"}
      result     response.generateVideoResponse.generatedSamples[0].video.uri
      download   GET <uri> with the same `x-goog-api-key` header; MP4; server retains the
                 file for 2 days only, so the local binary copy IS the artifact.

    Veo 3.1 Fast: durations 4|6|8 s; aspect 16:9|9:16; resolution 720p (1080p/4k need 8 s);
    audio is NATIVE — there is no audio request parameter, and none is sent (the pilot's
    audio treatment is deliberately not decided here). Google documents that safety filters
    sometimes block a generation and that blocked videos are not charged; blocked outcomes
    surface as an operation error or as a response with no generated samples (the
    `raiMediaFilteredCount`/`raiMediaFilteredReasons` fields Google documents on its Veo
    reference for the sibling Vertex surface are read here ONLY if present — their absence
    is never treated as meaning anything).

    Price (official Gemini API pricing page, fetched 2026-08-28): Veo 3.1 Fast 720p =
    USD 0.10 per generated second, audio included. Provisional planning rate for the
    pre-call reservation; NOT invoice evidence; re-verify at execution time.

THE TRIAL BOUNDARY, FOR A LONG-RUNNING OPERATION

    The GENERATION TRIAL IS THE predictLongRunning SUBMIT. Operation polls, the result read
    and the artifact download are lifecycle steps of that one trial: counted and recorded,
    never new attempts. One submit = one attempt = one trial, including a submit that
    refuses, errors, times out or becomes unresolvable mid-poll. There is no client retry
    path and no resubmission after ambiguity — a later authorised repair would be a NEW
    attempt owned by PILOT-001, not by this module.

AMBIGUITY, PRESERVED FROM EMP-001

    The exception vocabulary (`PreDispatchRefusal`, `AmbiguousDispatch`, `DispatchRefused`)
    and the transport-failure classifier are IMPORTED from
    eval/empirical-tranche-1/providers.py rather than re-declared — one source of truth for
    what "ambiguous" means. Applied here:

      before the submit send      provably pre-dispatch -> reservation released, nothing
                                  persisted (no attempt was made)
      submit send onwards         AMBIGUOUS on any failure -> settle the reservation
                                  conservatively, persist a real failed attempt, stop
      after the operation exists  a poll/result/download failure never releases money and
                                  never resubmits; recorded on the same attempt with
                                  `outcome_resolved: false` where the provider-side outcome
                                  is genuinely unknown.

    Google documents that safety-blocked videos are not charged; the ledger still settles
    refusals at the reserved estimate because a conservative overstatement can be corrected
    by billing evidence, while an optimistic release cannot be un-spent.

PROVENANCE

    Every attempt is recorded in the corrected-RES-007 vocabulary: provider / model_id /
    model_version / endpoint / workflow / prompt_hash / config_hash / config_location /
    reference_asset_hashes / requested_at / completed_at / lane / status / repeat & retry
    fields / storage_class. The full request configuration (model, endpoint, exact body
    including the prompt) is written to a JSON file next to the artifact BEFORE dispatch;
    `config_hash` is the SHA-256 of that file's bytes, so the exact request is recoverable
    and hash-bound. `res007_production_attempt()` emits the writer-ready handoff.

UNTESTED AGAINST A LIVE PROVIDER. Every exercise of this module goes through injected fake
transports. Treat the real path as unproven until the first authorised PILOT-001 call.
"""
from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
EVAL_ROOT = HERE.parent
EMP001 = EVAL_ROOT / "empirical-tranche-1"

# Read-only import of the frozen EMP-001 dispatch semantics. One source of truth for what
# "ambiguous" means; a re-declaration here would drift.
if str(EMP001) not in sys.path:
    sys.path.insert(0, str(EMP001))
from providers import (  # noqa: E402
    AmbiguousDispatch, DispatchRefused, PreDispatchRefusal, classify_transport_failure)

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import artifact_store  # noqa: E402

GEMINI_KEY_ENV = "GEMINI_API_KEY"

# ------------------------------------------------------------------ the one frozen route
# Changing anything in this table is a Controller decision, not a runtime option.
# `model_id` IS the exact versioned identifier Google exposes; there is no separate stable
# alias to drift from, which is why model_version records the same string explicitly rather
# than a friendly family name.
VIDEO_ROUTES = {
    "VID-PILOT-01": {
        "provider": "google",
        "provider_surface": "gemini-developer-api",
        "model_id": "veo-3.1-fast-generate-preview",
        "model_version": "veo-3.1-fast-generate-preview",
        "api_base": "https://generativelanguage.googleapis.com/v1beta",
        "workflow": "t2v",
        "lane": "native_av",           # Veo 3.1 output is video with native audio
        "allowed_durations_s": (4, 6, 8),
        "allowed_aspect_ratios": ("16:9", "9:16"),
        "pinned_parameters": {
            "resolution": "720p",
        },
        # USD per generated second, 720p, audio included — official Gemini API pricing page,
        # fetched 2026-08-28. Provisional planning rate; NOT invoice evidence.
        "provisional_usd_per_second": Decimal("0.10"),
        "billing_unit": "per_generated_second",
    },
}

STORAGE_CLASS = "C_irreproducible_empirical"


class LifecycleContractBreach(RuntimeError):
    """The provider's reply did not match its documented contract."""


# --------------------------------------------------------------------------- transports
class LiveGeminiTransport:
    """The ONLY class in this package that can open a socket — and only when called.

    Construction opens nothing and reads no key. The route's default transport is None, so
    reaching Google requires someone to build one of these and inject it, which is the
    correct difficulty for a paid path.
    """

    def __init__(self, timeout_s: float = 60.0):
        self.timeout_s = timeout_s
        self.calls = 0

    def _open(self, req):
        import urllib.error
        import urllib.request

        self.calls += 1
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                return resp.status, resp.read(), resp.headers.get("Content-Type")
        except urllib.error.HTTPError as exc:
            # An HTTP error status is still a provider ANSWER; return it for classification
            # rather than burying the body (which carries the error detail).
            return exc.code, exc.read(), exc.headers.get("Content-Type")

    def post_json(self, url: str, headers: dict, payload: bytes) -> tuple[int, dict]:
        import urllib.request

        status, body, _ = self._open(urllib.request.Request(
            url, data=payload, headers={"Content-Type": "application/json", **headers}))
        return status, json.loads(body.decode("utf-8"))

    def get_json(self, url: str, headers: dict) -> tuple[int, dict]:
        import urllib.request

        status, body, _ = self._open(urllib.request.Request(url, headers=headers))
        return status, json.loads(body.decode("utf-8"))

    def get_bytes(self, url: str, headers: dict) -> tuple[int, bytes, str | None]:
        import urllib.request

        return self._open(urllib.request.Request(url, headers=headers))


# ------------------------------------------------------------------------------ the route
@dataclass
class GeminiVeoRoute:
    """The frozen pilot video route behind an injected transport and a budget guard.

    `transport` must expose post_json / get_json / get_bytes as in LiveGeminiTransport.
    `guard` must expose reserve / record (and optionally release), as EMP-001's guards do.
    `sleep` and `clock` are injected so tests never wait and timestamps are deterministic.
    """

    slot: str = "VID-PILOT-01"
    transport: Any = None
    guard: Any = None
    sleep: Callable[[float], None] | None = None
    clock: Callable[[], str] | None = None
    poll_interval_s: float = 10.0
    max_status_checks: int = 90
    # Set by the caller before a call so ledger rows and records share trial identity.
    call_context: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        frozen = VIDEO_ROUTES.get(self.slot)
        if frozen is None:
            raise ValueError(
                f"unknown pilot video slot {self.slot!r}. The frozen slots are "
                f"{sorted(VIDEO_ROUTES)}; adding one is a Controller decision.")
        self.frozen = frozen
        self.submits = 0          # generation trials — the only count that may reach 1
        self.status_checks = 0    # lifecycle steps, never trials

    # -- identity ---------------------------------------------------------------------
    def identity(self) -> dict:
        return {
            "slot": self.slot,
            "provider": self.frozen["provider"],
            "provider_surface": self.frozen["provider_surface"],
            "model_id": self.frozen["model_id"],
            "model_version": self.frozen["model_version"],
            "endpoint": self.submit_url(),
            "workflow": self.frozen["workflow"],
            "lane": self.frozen["lane"],
        }

    # -- request construction (no dispatch) -------------------------------------------
    def build_body(self, prompt: str, duration_s: int, aspect_ratio: str) -> dict:
        """The documented predictLongRunning body, frozen pins applied. Nothing else enters.

        Built from the frozen table, NOT from a caller dict: a seed, a resolution change or
        an undocumented parameter cannot reach Google merely by being passed in. No audio
        parameter exists on this surface and none is invented; no personGeneration policy is
        decided here.
        """
        if not prompt or not prompt.strip():
            raise ValueError("a generation request needs a non-empty prompt")
        if duration_s not in self.frozen["allowed_durations_s"]:
            raise ValueError(
                f"duration_s {duration_s!r} is not in the provider enum "
                f"{self.frozen['allowed_durations_s']}. The contract exposes discrete "
                f"durations; anything else would be a guess about provider behaviour.")
        if aspect_ratio not in self.frozen["allowed_aspect_ratios"]:
            raise ValueError(
                f"aspect_ratio {aspect_ratio!r} is not in the provider enum "
                f"{self.frozen['allowed_aspect_ratios']}")
        return {
            "instances": [{"prompt": prompt}],
            "parameters": {
                "aspectRatio": aspect_ratio,
                "durationSeconds": duration_s,
                **self.frozen["pinned_parameters"],
            },
        }

    def submit_url(self) -> str:
        return (f"{self.frozen['api_base']}/models/"
                f"{self.frozen['model_id']}:predictLongRunning")

    def operation_url(self, operation_name: str) -> str:
        # The operation name arrives fully qualified (e.g. "models/.../operations/<id>").
        return f"{self.frozen['api_base']}/{operation_name}"

    def estimate_usd(self, duration_s: int) -> Decimal:
        return self.frozen["provisional_usd_per_second"] * Decimal(duration_s)

    def _read_key(self) -> str:
        import os

        key = os.environ.get(GEMINI_KEY_ENV)
        if not key:
            raise PreDispatchRefusal(
                f"{GEMINI_KEY_ENV} is not set. Keys are read from the environment at "
                f"dispatch time and are never committed, logged or persisted. Nothing "
                f"was sent.")
        return key

    def _headers(self, key: str) -> dict:
        return {"x-goog-api-key": key}

    def _now(self) -> str:
        if self.clock:
            return self.clock()
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # -- budget plumbing (EMP-001 tolerant pattern: persistent StageBudget takes context,
    #    the in-memory BudgetGuard does not; both must still be charged) -----------------
    def _reserve(self, estimated_usd: Decimal) -> None:
        try:
            self.guard.reserve(estimated_usd, **(self.call_context or {}))
        except TypeError:
            self.guard.reserve(estimated_usd)

    def _settle(self, amount: Decimal, **extra) -> str | None:
        try:
            return self.guard.record(amount, **{**(self.call_context or {}), **extra})
        except TypeError:
            return self.guard.record(amount)

    def _release(self) -> None:
        release = getattr(self.guard, "release", None)
        if release:
            release()

    # -- the full lifecycle, once -------------------------------------------------------
    def generate(self, prompt: str, duration_s: int, aspect_ratio: str,
                 out_dir: Path) -> dict:
        """One generation trial: submit, poll the operation, fetch, download, persist.

        Returns {"attempt": ..., "artifact": ... | None}. Every path that reaches the
        dispatch boundary returns a persisted attempt; only provably-pre-dispatch failures
        raise instead (after releasing the reservation), because no attempt was made.
        """
        if self.transport is None:
            raise DispatchRefused(
                "no transport injected. This route cannot reach a provider, which is the "
                "correct state until PILOT-001 is authorised.")
        if self.guard is None:
            raise DispatchRefused(
                "no budget guard. A paid call must be reserved against an explicit "
                "authorised ceiling before it is dispatched.")

        body = self.build_body(prompt, duration_s, aspect_ratio)   # refuses bad params first
        estimate = self.estimate_usd(duration_s)
        self._reserve(estimate)                                    # raises BEFORE any send

        try:
            key = self._read_key()
        except PreDispatchRefusal:
            # PROVEN nothing was sent. Only here may the headroom go back.
            self._release()
            raise

        headers = self._headers(key)
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        out_dir = Path(out_dir)
        attempt = self._base_attempt(body, out_dir)

        # ---- THE DISPATCH BOUNDARY ------------------------------------------------------
        # Everything below may have reached Google. Every failure below is AMBIGUOUS: the
        # money stays counted, the attempt is persisted, and nothing is retried.
        attempt["requested_at"] = self._now()
        self.submits += 1
        try:
            status_code, reply = self.transport.post_json(self.submit_url(), headers, payload)
        except Exception as exc:
            api_status, error_class = classify_transport_failure(exc)
            return self._settle_failed(attempt, estimate, api_status, error_class,
                                       note=f"{type(exc).__name__} after dispatch to "
                                            f"{self.submit_url()}: {exc}",
                                       ambiguous=True, outcome_resolved=False)

        if status_code != 200:
            err = (reply or {}).get("error") or {}
            return self._settle_failed(
                attempt, estimate, "error",
                str(err.get("status") or err.get("code") or f"http_{status_code}"),
                note=str(reply)[:300], ambiguous=False, outcome_resolved=True)

        operation_name = (reply or {}).get("name")
        if not operation_name:
            exc = LifecycleContractBreach(
                "predictLongRunning returned 200 with no operation name — the documented "
                "contract returns one, and without it the job cannot be tracked or "
                "accounted for")
            return self._settle_failed(attempt, estimate, "error", "malformed_response",
                                       note=str(exc), ambiguous=True, outcome_resolved=False)

        attempt["operation_name"] = operation_name

        # ---- polling: lifecycle steps of the SAME trial ---------------------------------
        operation = None
        for _ in range(self.max_status_checks):
            if self.status_checks and self.sleep:
                self.sleep(self.poll_interval_s)
            self.status_checks += 1
            attempt["status_checks"] += 1
            try:
                code, op = self.transport.get_json(
                    self.operation_url(operation_name), headers)
            except Exception as exc:
                # The operation exists at Google and may complete and bill. Unresolvable.
                api_status, error_class = classify_transport_failure(exc)
                return self._settle_failed(
                    attempt, estimate, api_status, f"poll_{error_class}",
                    note=f"operation poll failed after submit succeeded; "
                         f"{operation_name} may still complete and bill: {exc}",
                    ambiguous=True, outcome_resolved=False)

            if code != 200:
                return self._settle_failed(
                    attempt, estimate, "error", f"poll_http_{code}",
                    note=f"operation poll answered {code} for {operation_name}; final "
                         f"provider outcome unknown", ambiguous=True,
                    outcome_resolved=False)

            if not isinstance(op, dict) or ("done" not in op and "name" not in op):
                exc = LifecycleContractBreach(
                    f"operation poll returned an undocumented shape for {operation_name}; "
                    f"refusing to guess what it means for billing")
                return self._settle_failed(attempt, estimate, "error", "malformed_response",
                                           note=str(exc), ambiguous=True,
                                           outcome_resolved=False)
            if op.get("done") is True:
                operation = op
                break
        else:
            return self._settle_failed(
                attempt, estimate, "timeout", "poll_budget_exhausted",
                note=f"{operation_name} not done after {self.max_status_checks} status "
                     f"checks; it may still complete and bill. No re-submit.",
                ambiguous=True, outcome_resolved=False)

        attempt["completed_at"] = self._now()

        # ---- terminal operation: error, refusal, or a result ----------------------------
        if operation.get("error"):
            err = operation["error"]
            return self._settle_failed(
                attempt, estimate, "error",
                str(err.get("status") or err.get("code") or "operation_error"),
                note=str(err)[:300], ambiguous=False, outcome_resolved=True)

        gv = ((operation.get("response") or {}).get("generateVideoResponse") or {})
        samples = gv.get("generatedSamples") or []
        if not samples or not ((samples[0].get("video") or {}).get("uri")):
            # Google documents that safety filters sometimes block a generation. The
            # rai* fields are read only if present; an absent field is never interpreted.
            filtered = gv.get("raiMediaFilteredCount")
            if filtered:
                return self._settle_failed(
                    attempt, estimate, "refusal", "safety_filtered",
                    note=str(gv.get("raiMediaFilteredReasons"))[:300],
                    ambiguous=False, outcome_resolved=True)
            return self._settle_failed(
                attempt, estimate, "error", "no_artifact_returned",
                note="done operation carried no generated video uri", ambiguous=False,
                outcome_resolved=True)

        artifact_uri = samples[0]["video"]["uri"]

        # ---- binary artifact download (server retains the file 2 days only) -------------
        try:
            code, data, served_type = self.transport.get_bytes(artifact_uri, headers)
        except Exception as exc:
            return self._settle_failed(
                attempt, estimate, "error", "artifact_download_failed",
                note=f"generation completed (billable) but the artifact download failed: "
                     f"{exc}. The provider URI is recorded for a later, separately "
                     f"authorised fetch — never an automatic one.",
                ambiguous=False, outcome_resolved=True, artifact_uri=artifact_uri)
        if code != 200 or not isinstance(data, (bytes, bytearray)) or not data:
            return self._settle_failed(
                attempt, estimate, "error", "artifact_download_failed",
                note=f"artifact URI answered {code} with "
                     f"{'no' if not data else 'non-byte'} content",
                ambiguous=False, outcome_resolved=True, artifact_uri=artifact_uri)

        artifact = artifact_store.persist_video_bytes(
            bytes(data), out_dir=out_dir,
            attempt_id=attempt["attempt_id"],
            trial_id=attempt["trial_id"],
            identity=self.identity(),
            provider_request_id=operation_name,
            content_type=served_type,
            declared_file_size=None,      # the operation response declares no size
            source_url=artifact_uri)

        cost_ref = self._settle(estimate, billing_state="reported")
        attempt.update({
            "status": "ok",
            "error_class": None,
            "artifact_uri": artifact_uri,
            "artifact_id": artifact["artifact_id"],
            "billing_state": "reported",
            "cost_basis": "provisional_published_rate",
            "cost_ref": cost_ref or getattr(self.guard, "cost_ref", None),
            "ambiguous_dispatch": False,
            "outcome_resolved": True,
        })
        return {"attempt": attempt, "artifact": artifact}

    # -- record shaping ---------------------------------------------------------------
    def _base_attempt(self, body: dict, out_dir: Path) -> dict:
        """The attempt skeleton, in the corrected-RES-007 provenance vocabulary.

        The full request configuration is written to a JSON file BEFORE dispatch so the
        exact request is recoverable; config_hash binds the attempt to those bytes.
        """
        prompt = body["instances"][0]["prompt"]
        config = {
            "record": "EVAL-035-request-config",
            "provider": self.frozen["provider"],
            "provider_surface": self.frozen["provider_surface"],
            "model_id": self.frozen["model_id"],
            "model_version": self.frozen["model_version"],
            "endpoint": self.submit_url(),
            "api_version": "v1beta",
            "workflow": self.frozen["workflow"],
            "request_body": body,
            "billing_unit": self.frozen["billing_unit"],
            "provisional_usd_per_second": str(self.frozen["provisional_usd_per_second"]),
        }
        config_bytes = json.dumps(config, ensure_ascii=False, indent=2,
                                  sort_keys=True).encode("utf-8")
        config_hash = hashlib.sha256(config_bytes).hexdigest()

        attempt_id = self.call_context.get("attempt_id") or f"pilot-{config_hash[:12]}"
        out_dir.mkdir(parents=True, exist_ok=True)
        config_path = out_dir / f"{attempt_id}-request-config.json"
        config_path.write_bytes(config_bytes)

        return {
            **self.identity(),
            "attempt_id": attempt_id,
            "trial_id": attempt_id,                 # one call = one trial, by construction
            "prompt_hash": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "config_hash": config_hash,
            "config_location": str(config_path),
            "reference_asset_hashes": [],           # t2v: no reference assets supplied
            "request_parameters": dict(body["parameters"]),
            "seed": None,
            "seed_policy": "unseeded",
            "billing_unit": self.frozen["billing_unit"],
            "reserved_usd": str(self.estimate_usd(body["parameters"]["durationSeconds"])),
            "operation_name": None,
            "artifact_uri": None,
            "artifact_id": None,
            "status_checks": 0,
            "requested_at": None,
            "completed_at": None,
            "status": None,
            "error_class": None,
            "raw_status_note": "",
            "retries": 0,
            "repeat_index": 0,
            "repeat_of_attempt_id": None,
            "retry_of_attempt_id": None,            # pinned; no code path sets it
            "retry_reason": None,
            "storage_class": STORAGE_CLASS,
            "one_call_one_trial": True,
            "synthetic": False,
        }

    def _settle_failed(self, attempt: dict, estimate: Decimal, status: str,
                       error_class: str, note: str, ambiguous: bool,
                       outcome_resolved: bool, artifact_uri: str | None = None) -> dict:
        """Settle conservatively and describe the failed trial honestly. Never retried."""
        billing_state = "unknown_provisional" if ambiguous or not outcome_resolved \
            else "reported"
        cost_ref = self._settle(estimate, billing_state=billing_state)
        if attempt["completed_at"] is None and outcome_resolved:
            attempt["completed_at"] = self._now()
        attempt.update({
            "status": status,
            "error_class": error_class,
            "raw_status_note": note[:300],
            "artifact_uri": artifact_uri,
            "billing_state": billing_state,
            "cost_basis": ("conservative_reserved_estimate_billing_unknown"
                           if billing_state == "unknown_provisional"
                           else "provisional_published_rate"),
            "cost_ref": cost_ref or getattr(self.guard, "cost_ref", None),
            "ambiguous_dispatch": bool(ambiguous),
            "outcome_resolved": bool(outcome_resolved),
        })
        return {"attempt": attempt, "artifact": None}


# --------------------------------------------------------- RES-007 production handoff
# The corrected v3 writer (RES-007, gate G12) mechanically requires the inherited v2.1 call
# provenance on every production attempt and FORBIDS eval_item_id on production attempts.
# This adapter emits exactly the writer-ready field set, losslessly, so PILOT-001 needs no
# ad-hoc translation after the call. It is a handoff shape, not a second persistence
# architecture: nothing is written anywhere by this function.
RES007_REQUIRED_FIELDS = (
    "attempt_id", "trial_id", "provider", "model_id", "model_version", "endpoint",
    "workflow", "prompt_hash", "config_hash", "config_location",
    "reference_asset_hashes", "requested_at", "completed_at", "lane", "repeat_index",
    "repeat_of_attempt_id", "retry_of_attempt_id", "retry_reason", "status", "cost_ref",
    "storage_class",
)


def res007_production_attempt(outcome: dict) -> dict:
    """Map one route outcome onto the corrected-RES-007 production-attempt handoff.

    Returns {"writer_fields": ..., "provider_extras": ...}:

      writer_fields     exactly the named arguments OutcomeWriter.record_attempt requires
                        for a production attempt (minus step_id, which belongs to the
                        journey, and plus storage_class for the artifact side). No
                        eval_item_id — a production attempt serves a brief, not a
                        benchmark item, and fabricating the link is invented provenance.
      provider_extras   provider-specific evidence (operation name, raw status note,
                        artifact URI, poll count, billing state) that the journey persists
                        alongside, kept OUT of writer_fields because the corrected writer
                        refuses unknown fields.
    """
    a = outcome["attempt"]
    writer_fields = {
        "attempt_id": a["attempt_id"],
        "trial_id": a["trial_id"],
        "attempt_kind": "production",
        "status": a["status"],
        "lane": a["lane"],
        "cost_ref": a.get("cost_ref"),
        "provider": a["provider"],
        "model_id": a["model_id"],
        "model_version": a["model_version"],
        "endpoint": a["endpoint"],
        "workflow": a["workflow"],
        "prompt_hash": a["prompt_hash"],
        "config_hash": a["config_hash"],
        "config_location": a["config_location"],
        "reference_asset_hashes": list(a["reference_asset_hashes"]),
        "requested_at": a["requested_at"],
        "completed_at": a["completed_at"],       # None only if the call never resolved
        "repeat_index": a["repeat_index"],
        "repeat_of_attempt_id": a["repeat_of_attempt_id"],
        "retry_of_attempt_id": a["retry_of_attempt_id"],
        "retry_reason": a["retry_reason"],
        "error_detail": (None if a["status"] == "ok"
                         else f"{a['error_class']}: {a['raw_status_note']}"[:300]),
        "storage_class": a["storage_class"],
    }
    provider_extras = {
        "provider_surface": a["provider_surface"],
        "operation_name": a["operation_name"],
        "artifact_uri": a["artifact_uri"],
        "artifact_id": a["artifact_id"],
        "status_checks": a["status_checks"],
        "request_parameters": a["request_parameters"],
        "seed_policy": a["seed_policy"],
        "billing_unit": a["billing_unit"],
        "reserved_usd": a["reserved_usd"],
        "billing_state": a["billing_state"],
        "cost_basis": a["cost_basis"],
        "ambiguous_dispatch": a["ambiguous_dispatch"],
        "outcome_resolved": a["outcome_resolved"],
    }
    return {"writer_fields": writer_fields, "provider_extras": provider_extras}


# ------------------------------------------------------------------- the PILOT-001 seam
def generate_pilot_video(prompt: str, duration_s: int, aspect_ratio: str, out_dir: Path,
                         guard, transport, sleep=None, clock=None,
                         call_context: dict | None = None,
                         slot: str = "VID-PILOT-01") -> dict:
    """The thin interface PILOT-001 calls: one route, one trial, one persisted outcome.

    The caller supplies the guard (opened from the machine-verifiable PILOT-001
    authorisation chain — see pilot_authorisation.open_pilot_guard, which the committed
    state cannot open today) and the transport (LiveGeminiTransport for a real call; a fake
    in every test). This function adds nothing else on purpose: no routing, no planning, no
    repair, no retry.
    """
    route = GeminiVeoRoute(slot=slot, transport=transport, guard=guard, sleep=sleep,
                           clock=clock, call_context=call_context or {})
    return route.generate(prompt, duration_s, aspect_ratio, Path(out_dir))
