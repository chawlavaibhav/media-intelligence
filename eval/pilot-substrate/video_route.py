#!/usr/bin/env python3
"""EVAL-035: one pilot-capable video generation route. fal queue surface, Veo 3.1.

NOTHING HERE CONTACTS A PROVIDER BY ITSELF.

    Importing this module makes no call. Constructing a route makes no call and reads no API
    key. A route with no injected transport REFUSES to dispatch, and a route with a transport
    but no budget guard also refuses. The only way to spend money is to hand the route both a
    live transport (built explicitly via `LiveQueueTransport`) and a guard opened from an
    explicit PILOT-001 authorisation — which does not exist yet (`pilot_authorisation.py`).

ONE ROUTE, FROZEN

    `fal-ai/veo3.1` — Google Veo 3.1, text-to-video, native audio, version pinned in the
    endpoint path. Identity evidence: fal's own SDK enumeration
    (eval/pre-execution-freeze/model-supply/FAL-VERIFIED-ROUTES.yaml). Selected for the Aight
    short-form commercial pilot because it is the Wave-1 VID-01 candidate family (rendered
    text/logo stability + native audio in ONE call — the smallest operationally sufficient
    topology; a composite TTS+lipsync route would be three routes, not one), and because the
    fal surface reuses the exact auth contract EMP-001 already exercised with real money.
    This selection is INFRASTRUCTURE, not model qualification — no quality claim is made.

THE TRIAL BOUNDARY, FOR AN ASYNC PROVIDER

    fal runs video jobs through a queue: submit -> request_id -> status polling -> completed
    result -> artifact URL. The GENERATION TRIAL IS THE SUBMIT. Status polls, the result
    fetch and the artifact download are lifecycle steps of that one trial: they are counted
    and recorded, but they are never new attempts and never inflate the generation count.
    One submit = one attempt = one trial, including a submit that refuses, errors, times out
    or vanishes into an unresolvable network failure mid-poll.

ZERO RETRIES, INCLUDING THE PROVIDER'S OWN

    fal's platform automatically retries queued requests up to 10 times on server errors,
    timeouts, connection failures and rate limits unless the caller sends `X-Fal-No-Retry`
    (fal reliability docs, fetched 2026-08-28). Without that header, one submit could
    quietly become several platform-side generation runs — a silent retry outside our
    process. Every submit here therefore carries `X-Fal-No-Retry: 1`, and the tests assert
    the header's presence rather than trusting this paragraph.

NO SILENT PROMPT SUBSTITUTION

    The veo3.1 endpoint's `auto_fix` parameter defaults to TRUE and rewrites prompts that
    fail content policy. A rewritten prompt is a different generation than the one recorded,
    which breaks provenance in exactly the way a floating model alias would. `auto_fix` is
    pinned FALSE in the frozen body and the caller cannot turn it on. A policy block comes
    back as an honest refusal instead.

AMBIGUITY, PRESERVED FROM EMP-001

    The exception vocabulary (`PreDispatchRefusal`, `AmbiguousDispatch`, `DispatchRefused`)
    and the transport-failure classifier are IMPORTED from
    eval/empirical-tranche-1/providers.py rather than re-declared. A second copy would
    drift, and drifting ambiguity semantics is how a hard spend ceiling becomes soft.

    Applied to the queue lifecycle:

      before the submit send      provably pre-dispatch -> reservation released, nothing
                                  persisted (no attempt was made)
      submit send onwards         AMBIGUOUS on any failure -> settle the reservation
                                  conservatively, persist a real failed attempt, stop
      after submit succeeded      the job EXISTS at the provider and will be billed if it
                                  completes. A poll/result/download failure never releases
                                  money and never re-submits; it is recorded on the same
                                  attempt with `outcome_resolved: false` where the final
                                  provider-side outcome is genuinely unknown.

COST

    fal returns no billed amount. Cost is reserved and settled from the committed provisional
    planning rate — USD 0.40 per generated second with audio at 720p/1080p, per
    coordination/decisions/CONTROLLER-VEO-PRICING-UNIT-CORRECTION-2026-08-26.md — and marked
    `provisional_published_rate`. It must be replaced by execution-time price verification
    and billing evidence before any cost claim is reported.

UNTESTED AGAINST A LIVE PROVIDER. Every exercise of this module goes through injected fake
transports. Treat the real path as unproven until the first authorised PILOT-001 call.
"""
from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
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

# Same-package import via the sys.path convention this repo already uses for hyphenated
# package directories (see eval/empirical-tranche-1/tests/conftest.py).
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import artifact_store  # noqa: E402

FAL_KEY_ENV = "FAL_KEY"

# ------------------------------------------------------------------ the one frozen route
# Changing anything in this table is a Controller decision, not a runtime option.
#
# Contract provenance is recorded in README.md. `duration` and `aspect_ratio` are the only
# caller-selectable parameters, restricted to the provider's own enums; everything else is
# pinned. No seed is ever sent (`seed_policy: unseeded`) and `auto_fix` is pinned off so the
# prompt that runs is byte-identical to the prompt recorded.
VIDEO_ROUTES = {
    "VID-PILOT-01": {
        "route": "fal-ai/veo3.1",
        "provider_surface": "fal",
        "model_family": "veo-3.1",
        "workflow_mode": "t2v",
        "queue_base": "https://queue.fal.run",
        "allowed_durations_s": (4, 6, 8),
        "allowed_aspect_ratios": ("16:9", "9:16"),
        "pinned_body": {
            "resolution": "720p",
            "generate_audio": True,
            "auto_fix": False,
        },
        # USD per generated second, with audio, 720p — provisional planning rate from
        # CONTROLLER-VEO-PRICING-UNIT-CORRECTION-2026-08-26.md. NOT invoice evidence.
        "provisional_usd_per_second": Decimal("0.40"),
        "billing_unit": "per_generated_second",
    },
}

TERMINAL_STATUS = "COMPLETED"
IN_FLIGHT_STATUSES = ("IN_QUEUE", "IN_PROGRESS")

# fal signals a content-policy block as a 422 with this type, and documents it as
# non-retryable. A block is a REFUSAL — the provider understood and declined — which is a
# different fact about the prompt than an infrastructure ERROR is about the provider.
CONTENT_POLICY_TYPES = ("content_policy_violation", "moderation_block", "safety")


class LifecycleContractBreach(RuntimeError):
    """The provider's queue reply did not match its documented contract."""


# --------------------------------------------------------------------------- transports
class LiveQueueTransport:
    """The ONLY class in this package that can open a socket — and only when called.

    Construction opens nothing and reads no key. Kept deliberately explicit: the route's
    default transport is None, so reaching fal requires someone to build one of these and
    inject it, which is the correct difficulty for a paid path.
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
                return resp.status, resp.read()
        except urllib.error.HTTPError as exc:
            # An HTTP error status is still a provider ANSWER; return it for classification
            # rather than burying the body (which carries the refusal/error detail).
            return exc.code, exc.read()

    def post_json(self, url: str, headers: dict, payload: bytes) -> tuple[int, dict]:
        import urllib.request

        status, body = self._open(urllib.request.Request(
            url, data=payload, headers={"Content-Type": "application/json", **headers}))
        return status, json.loads(body.decode("utf-8"))

    def get_json(self, url: str, headers: dict) -> tuple[int, dict]:
        import urllib.request

        status, body = self._open(urllib.request.Request(url, headers=headers))
        return status, json.loads(body.decode("utf-8"))

    def get_bytes(self, url: str, headers: dict) -> tuple[int, bytes]:
        import urllib.request

        return self._open(urllib.request.Request(url, headers=headers))


# ------------------------------------------------------------------------------ the route
@dataclass
class PilotVideoRoute:
    """The frozen pilot video route behind an injected transport and a budget guard.

    `transport` must expose post_json / get_json / get_bytes as in LiveQueueTransport.
    `guard` must expose reserve / record (and optionally release), as EMP-001's guards do.
    `sleep` is injected so tests never wait and the poll cadence is visible in the record.
    """

    slot: str = "VID-PILOT-01"
    transport: Any = None
    guard: Any = None
    sleep: Callable[[float], None] | None = None
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
            "route": self.frozen["route"],
            "provider_surface": self.frozen["provider_surface"],
            "model_family": self.frozen["model_family"],
            "workflow_mode": self.frozen["workflow_mode"],
            "route_version_pinned_in_path": True,
        }

    # -- request construction (no dispatch) -------------------------------------------
    def build_body(self, prompt: str, duration_s: int, aspect_ratio: str) -> dict:
        """Frozen configuration plus the caller's three parameters. Nothing else can enter.

        Built from the frozen table, NOT from a caller dict: a seed, a resolution change or
        auto_fix cannot reach fal merely by being passed in.
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
            "prompt": prompt,
            "duration": f"{duration_s}s",
            "aspect_ratio": aspect_ratio,
            **self.frozen["pinned_body"],
        }

    def submit_url(self) -> str:
        return f"{self.frozen['queue_base']}/{self.frozen['route']}"

    def request_url(self, request_id: str, suffix: str = "") -> str:
        return (f"{self.frozen['queue_base']}/{self.frozen['route']}/requests/"
                f"{request_id}{suffix}")

    def estimate_usd(self, duration_s: int) -> Decimal:
        return self.frozen["provisional_usd_per_second"] * Decimal(duration_s)

    def _read_key(self) -> str:
        import os

        key = os.environ.get(FAL_KEY_ENV)
        if not key:
            raise PreDispatchRefusal(
                f"{FAL_KEY_ENV} is not set. Keys are read from the environment at dispatch "
                f"time and are never committed, logged or persisted. Nothing was sent.")
        return key

    def _headers(self, key: str) -> dict:
        # X-Fal-No-Retry: without it fal re-runs failed queue jobs up to 10 times, and one
        # submit silently becomes several platform-side generation attempts.
        return {"Authorization": f"Key {key}", "X-Fal-No-Retry": "1"}

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
        """One generation trial: submit, poll, fetch, download, persist. No second chance.

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
        attempt = self._base_attempt(body, duration_s, aspect_ratio, estimate)

        # ---- THE DISPATCH BOUNDARY ------------------------------------------------------
        # Everything below may have reached fal. Every failure below is AMBIGUOUS: the money
        # stays counted, the attempt is persisted, and nothing is retried.
        self.submits += 1
        try:
            status_code, reply = self.transport.post_json(self.submit_url(), headers, payload)
        except Exception as exc:
            api_status, error_class = classify_transport_failure(exc)
            return self._settle_failed(attempt, estimate, api_status, error_class,
                                       note=f"{type(exc).__name__} after dispatch to "
                                            f"{self.submit_url()}: {exc}",
                                       ambiguous=True, outcome_resolved=False)

        if status_code == 422:
            err_type = _error_type_of(reply)
            if err_type in CONTENT_POLICY_TYPES:
                return self._settle_failed(attempt, estimate, "refusal", "moderation_block",
                                           note=str(reply)[:300], ambiguous=False,
                                           outcome_resolved=True)
            return self._settle_failed(attempt, estimate, "error",
                                       err_type or "validation_error",
                                       note=str(reply)[:300], ambiguous=False,
                                       outcome_resolved=True)
        if status_code != 200:
            # The request reached fal and was answered with an error status. Conservative:
            # counted, persisted, not retried — fal's own retry is disabled by header.
            return self._settle_failed(attempt, estimate, "error",
                                       _error_type_of(reply) or f"http_{status_code}",
                                       note=str(reply)[:300], ambiguous=False,
                                       outcome_resolved=True)

        request_id = reply.get("request_id")
        if not request_id:
            exc = LifecycleContractBreach(
                "submit returned 200 with no request_id — the documented queue contract "
                "requires one, and without it the job cannot be tracked or accounted for")
            return self._settle_failed(attempt, estimate, "error", "malformed_response",
                                       note=str(exc), ambiguous=True, outcome_resolved=False)

        attempt["provider_request_id"] = request_id

        # ---- polling: lifecycle steps of the SAME trial ---------------------------------
        final_status_reply = None
        for _ in range(self.max_status_checks):
            if self.status_checks and self.sleep:
                self.sleep(self.poll_interval_s)
            self.status_checks += 1
            attempt["status_checks"] += 1
            try:
                code, status_reply = self.transport.get_json(
                    self.request_url(request_id, "/status"), headers)
            except Exception as exc:
                # The job exists at fal and may complete and bill. Unresolvable from here.
                api_status, error_class = classify_transport_failure(exc)
                return self._settle_failed(
                    attempt, estimate, api_status, f"poll_{error_class}",
                    note=f"status poll failed after submit succeeded; job {request_id} may "
                         f"still complete and bill: {exc}",
                    ambiguous=True, outcome_resolved=False)

            if code != 200:
                return self._settle_failed(
                    attempt, estimate, "error", f"poll_http_{code}",
                    note=f"status poll answered {code} for job {request_id}; final provider "
                         f"outcome unknown", ambiguous=True, outcome_resolved=False)

            state = status_reply.get("status")
            if state == TERMINAL_STATUS:
                final_status_reply = status_reply
                break
            if state not in IN_FLIGHT_STATUSES:
                exc = LifecycleContractBreach(
                    f"undocumented queue status {state!r} — the documented values are "
                    f"{IN_FLIGHT_STATUSES + (TERMINAL_STATUS,)}. Refusing to guess what it "
                    f"means for billing.")
                return self._settle_failed(attempt, estimate, "error", "malformed_response",
                                           note=str(exc), ambiguous=True,
                                           outcome_resolved=False)
        else:
            return self._settle_failed(
                attempt, estimate, "timeout", "poll_budget_exhausted",
                note=f"job {request_id} not terminal after {self.max_status_checks} status "
                     f"checks; it may still complete and bill. No re-submit.",
                ambiguous=True, outcome_resolved=False)

        # COMPLETED can still carry a job-level error (documented optional error fields).
        job_error_type = _error_type_of(final_status_reply)
        if final_status_reply.get("error") or job_error_type:
            refusal = job_error_type in CONTENT_POLICY_TYPES
            return self._settle_failed(
                attempt, estimate,
                "refusal" if refusal else "error",
                "moderation_block" if refusal else (job_error_type or "provider_error"),
                note=str(final_status_reply.get("error"))[:300],
                ambiguous=False, outcome_resolved=True)

        # ---- result fetch ---------------------------------------------------------------
        try:
            code, result = self.transport.get_json(self.request_url(request_id), headers)
        except Exception as exc:
            api_status, error_class = classify_transport_failure(exc)
            return self._settle_failed(
                attempt, estimate, api_status, f"result_fetch_{error_class}",
                note=f"job {request_id} COMPLETED but the result fetch failed; the "
                     f"generation happened and is billable: {exc}",
                ambiguous=True, outcome_resolved=False)
        if code != 200:
            return self._settle_failed(
                attempt, estimate, "error", f"result_fetch_http_{code}",
                note=f"job {request_id} COMPLETED but the result endpoint answered {code}",
                ambiguous=True, outcome_resolved=False)

        video = (result or {}).get("video") or {}
        artifact_url = video.get("url")
        if not artifact_url:
            return self._settle_failed(
                attempt, estimate, "error", "no_artifact_returned",
                note="COMPLETED result carried no video.url", ambiguous=False,
                outcome_resolved=True)

        # ---- binary artifact download -----------------------------------------------------
        try:
            code, data = self.transport.get_bytes(artifact_url, {})
        except Exception as exc:
            return self._settle_failed(
                attempt, estimate, "error", "artifact_download_failed",
                note=f"generation completed (billable) but the artifact download failed: "
                     f"{exc}. The provider URL is recorded for a later, separately "
                     f"authorised fetch — never an automatic one.",
                ambiguous=False, outcome_resolved=True, artifact_url=artifact_url)
        if code != 200 or not isinstance(data, (bytes, bytearray)) or not data:
            return self._settle_failed(
                attempt, estimate, "error", "artifact_download_failed",
                note=f"artifact URL answered {code} with "
                     f"{'no' if not data else 'non-byte'} content",
                ambiguous=False, outcome_resolved=True, artifact_url=artifact_url)

        artifact = artifact_store.persist_video_bytes(
            bytes(data), out_dir=Path(out_dir),
            attempt_id=attempt["attempt_id"],
            trial_id=attempt["trial_id"],
            identity=self.identity(),
            provider_request_id=request_id,
            content_type=video.get("content_type"),
            declared_file_size=video.get("file_size"),
            source_url=artifact_url)

        cost_ref = self._settle(estimate, billing_state="reported")
        attempt.update({
            "api_status": "ok",
            "error_class": None,
            "artifact_url": artifact_url,
            "artifact_id": artifact["artifact_id"],
            "billing_state": "reported",
            "cost_basis": "provisional_published_rate",
            "cost_ref": cost_ref or getattr(self.guard, "cost_ref", None),
            "ambiguous_dispatch": False,
            "outcome_resolved": True,
        })
        return {"attempt": attempt, "artifact": artifact}

    # -- record shaping ---------------------------------------------------------------
    def _base_attempt(self, body: dict, duration_s: int, aspect_ratio: str,
                      estimate: Decimal) -> dict:
        attempt_id = self.call_context.get("attempt_id") or (
            f"pilot-{self.slot}-{hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:12]}")
        return {
            **self.identity(),
            "attempt_id": attempt_id,
            "trial_id": attempt_id,                 # one call = one trial, by construction
            "prompt_sha256": hashlib.sha256(body["prompt"].encode("utf-8")).hexdigest(),
            "request_parameters": {
                "duration": f"{duration_s}s",
                "aspect_ratio": aspect_ratio,
                **self.frozen["pinned_body"],
            },
            "seed": None,
            "seed_policy": "unseeded",
            "billing_unit": self.frozen["billing_unit"],
            "reserved_usd": str(estimate),
            "provider_request_id": None,
            "artifact_url": None,
            "artifact_id": None,
            "status_checks": 0,
            "api_status": None,
            "error_class": None,
            "raw_status_note": "",
            "retries": 0,
            "retry_of_attempt_id": None,            # pinned; no code path sets it
            "platform_auto_retry_disabled": True,   # X-Fal-No-Retry sent on the submit
            "one_call_one_trial": True,
            "synthetic": False,
        }

    def _settle_failed(self, attempt: dict, estimate: Decimal, api_status: str,
                       error_class: str, note: str, ambiguous: bool,
                       outcome_resolved: bool, artifact_url: str | None = None) -> dict:
        """Settle conservatively and describe the failed trial honestly. Never retried."""
        billing_state = "unknown_provisional" if ambiguous or not outcome_resolved \
            else "reported"
        cost_ref = self._settle(estimate, billing_state=billing_state)
        attempt.update({
            "api_status": api_status,
            "error_class": error_class,
            "raw_status_note": note[:300],
            "artifact_url": artifact_url,
            "billing_state": billing_state,
            "cost_basis": ("conservative_reserved_estimate_billing_unknown"
                           if billing_state == "unknown_provisional"
                           else "provisional_published_rate"),
            "cost_ref": cost_ref or getattr(self.guard, "cost_ref", None),
            "ambiguous_dispatch": bool(ambiguous),
            "outcome_resolved": bool(outcome_resolved),
        })
        return {"attempt": attempt, "artifact": None}


def _error_type_of(reply: Any) -> str | None:
    """Pull the provider's error type out of the documented shapes without guessing."""
    if not isinstance(reply, dict):
        return None
    if reply.get("error_type"):
        return str(reply["error_type"])
    err = reply.get("error")
    if isinstance(err, dict):
        return err.get("type") or err.get("code")
    detail = reply.get("detail")
    if isinstance(detail, list):
        for entry in detail:
            if isinstance(entry, dict) and entry.get("type"):
                return str(entry["type"])
    return None


# ------------------------------------------------------------------- the PILOT-001 seam
def generate_pilot_video(prompt: str, duration_s: int, aspect_ratio: str, out_dir: Path,
                         guard, transport, sleep=None, call_context: dict | None = None,
                         slot: str = "VID-PILOT-01") -> dict:
    """The thin interface PILOT-001 calls: one route, one trial, one persisted outcome.

    The caller supplies the guard (opened from an explicit PILOT-001 authorisation — see
    pilot_authorisation.open_pilot_guard, which fails closed today) and the transport
    (LiveQueueTransport for a real call; a fake in every test). This function adds nothing
    else on purpose: no routing, no planning, no repair, no retry.
    """
    route = PilotVideoRoute(slot=slot, transport=transport, guard=guard, sleep=sleep,
                            call_context=call_context or {})
    return route.generate(prompt, duration_s, aspect_ratio, Path(out_dir))
