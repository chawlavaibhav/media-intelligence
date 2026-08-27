#!/usr/bin/env python3
"""EMP-001 text-judge adapters. Request builders, response parsers, fail-closed dispatch.

NOTHING HERE CONTACTS A PROVIDER BY ITSELF.

    Importing this module makes no call. Constructing a judge makes no call and reads no API key.
    A judge with no injected transport REFUSES to dispatch, and a judge with a transport but no
    budget guard also refuses. The only way to spend money is to hand a judge both a live
    transport and a guard opened from an explicit authorisation file.

    `eval/v1/harness/adapters.py` stays synthetic-only. Live adapters live here, apart from it, so
    that the self-test can never accidentally acquire a network path.

THE TWO SHAPES ARE DIFFERENT EXPERIMENTS

    transcribe  image + a frozen transcription-only prompt. The target is EVALUATOR-SIDE ONLY.
                Our code does the comparison. This is the PRIMARY generated-output measurement.
    verdict     image + the target + a frozen exact-match prompt. Deliberately exposed: the
                plausible answer is sitting in the prompt.

    The prompts are imported read-only from the frozen Devanagari checker contract rather than
    retyped, so the Latin pack and the Devanagari battery are qualified with byte-identical
    wording. A second copy would drift, and a drifted prompt reported as the same run is an
    experiment mutation.

    `build_transcribe_request` takes NO target parameter. Blindness is enforced by the signature
    first and by `verify_blind_payload` second.

MODEL IDENTITY

    `model_alias` records the configured model label and `resolved_version` records the exact
    execution identifier. They may differ for providers that expose moving aliases, or be identical
    when the provider's canonical model ID is itself pinned (as with Anthropic
    `claude-sonnet-5`). Both are persisted on every call. A judge refuses to exist
    without a resolved version.

COST

    Providers do not always return a billed amount. When they do not, cost is computed from the
    published rate recorded in PRICE_BOOK and marked `provisional_published_rate`. It must be
    replaced with invoice/billing evidence before any cost claim is reported. A refused or errored
    call still consumes its trial and is still costed: EI-C6.

LIVE EXECUTION

    Dispatch is PER PROVIDER. Active EMP-001 judges use `AnthropicHttpTransport`
    (`x-api-key` + `anthropic-version`, model in the body) and `GeminiHttpTransport`
    (`x-goog-api-key`, model in the URL). The dormant OpenAI compatibility adapter remains
    available but is not on the active EMP-001 roster. There is no generic fallback
    transport, because a provider without an explicit auth contract must not inherit somebody
    else's — that is exactly the defect the EVAL-012 branch shipped.

    Every one of them reads its key from the environment at DISPATCH time only, and derives its
    endpoint from the exact resolved version rather than a floating alias. None has been run
    against a live provider; every exercise in this branch goes through an injected recorder.
    Treat the real path as unproven until the first authorised call.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
BATTERY = REPO_ROOT / "eval" / "battery" / "devanagari-exactness"

# Read-only import of the frozen prompts. Nothing is written to the battery.
sys.path.insert(0, str(BATTERY))
from checker_input import (  # noqa: E402
    PROMPT_TRANSCRIBE, PROMPT_VERDICT, prompt_sha256)

sys.path.insert(0, str(HERE))
from budget_guard import BudgetGuard  # noqa: E402

SHAPES = ("transcribe", "verdict")

# Environment variable names. Documented in README.md. Read at dispatch time only, never at
# import or construction, and never written to any committed file.
OPENAI_KEY_ENV = "OPENAI_API_KEY"  # dormant compatibility adapter; not active in EMP-001
ANTHROPIC_KEY_ENV = "ANTHROPIC_API_KEY"
GOOGLE_KEY_ENV = "GOOGLE_API_KEY"

# Published rates at planning time, USD per 1M tokens. Sources are recorded in
# coordination/plans/2026-08-26-FIRST-EMPIRICAL-TRANCHE-PROPOSAL.md. These produce a PROVISIONAL
# cost only; they are not invoice evidence and must not be reported as measured economics.
PRICE_BOOK = {
    "openai": {"input_per_1m": Decimal("0.75"), "output_per_1m": Decimal("4.50")},
    "anthropic": {"input_per_1m": Decimal("2.00"), "output_per_1m": Decimal("10.00")},
    "google": {"input_per_1m": Decimal("0.30"), "output_per_1m": Decimal("2.50")},
}

# Nominal per-generation prices for the two frozen fal routes, from the route price refresh.
# Provisional planning figures: they size a pre-call reservation and are NOT invoice evidence.
NOMINAL_FAL_PRICE_USD = {"IMG-01": Decimal("0.053"), "IMG-02": Decimal("0.060")}


class DispatchRefused(RuntimeError):
    """A paid call was attempted without the machinery that makes it legitimate."""


class ProviderResponseError(RuntimeError):
    """A provider response could not be parsed into the declared shape."""


class BlindnessViolation(RuntimeError):
    """A payload failed its shape's blind check. It was NOT sent."""


class PreDispatchRefusal(DispatchRefused):
    """PROVEN: no provider request left this process, so the reservation may be released.

    Only failures that happen strictly before the send may raise this — a missing key, a request
    the builder refused to construct, a blindness violation. If there is any doubt about whether
    bytes reached the provider, it is not this exception.
    """


class AmbiguousDispatch(RuntimeError):
    """The request MAY have reached the provider. Billing state is unknown.

    Raised for anything that goes wrong once the send has begun: a read timeout, a connection
    reset, a remote disconnect, a TLS failure, or a reply we could not parse. The provider may
    have received and billed the request even though nothing usable came back.

    The correct response is conservative, and it is the whole point of EVAL-015: keep the money
    counted, keep the trial, do not retry, and stop.
    """

    def __init__(self, message: str, api_status: str, error_class: str, cause: BaseException):
        super().__init__(message)
        self.api_status = api_status
        self.error_class = error_class
        self.cause = cause


def classify_transport_failure(exc: BaseException) -> tuple[str, str]:
    """Map a post-send failure onto (api_status, error_class).

    `timeout` and `error` are kept apart because they are different facts about the provider, and
    the persistence vocabulary already distinguishes them. Everything here is ambiguous by
    construction: classification decides what to CALL it, never whether to charge for it.
    """
    import http.client
    import socket
    import ssl
    import urllib.error

    if isinstance(exc, (TimeoutError, socket.timeout)):
        return "timeout", "read_timeout"
    if isinstance(exc, ssl.SSLError):
        return "error", "tls_failure"
    if isinstance(exc, ConnectionResetError):
        return "error", "connection_reset"
    if isinstance(exc, http.client.RemoteDisconnected):
        return "error", "remote_disconnect"
    if isinstance(exc, ConnectionAbortedError):
        return "error", "connection_aborted"
    if isinstance(exc, urllib.error.HTTPError):
        return "error", f"http_{exc.code}"
    if isinstance(exc, (ConnectionError, OSError)):
        return "error", "network_failure"
    if isinstance(exc, ProviderResponseError):
        return "error", "malformed_response"
    return "error", "unknown_transport_failure"


@dataclass(frozen=True)
class EvaluatorResponse:
    """One provider call. One trial. Whatever happened to it."""

    text: str
    input_tokens: int | None
    output_tokens: int | None
    billed_usd: Decimal | None
    provider_request_id: str | None
    api_status: str = "ok"            # ok | error | refusal | timeout
    error_class: str | None = None
    cost_basis: str = "provisional_published_rate"
    raw_status_note: str = ""
    # `reported` when the provider told us; `unknown_provisional` when the call may have been
    # billed and we could not find out. Never silently zero.
    billing_state: str = "reported"
    ambiguous_dispatch: bool = False


# ------------------------------------------------------------------------------ transports
class FakeTransport:
    """Deterministic provider-shaped JSON. For tests. Counts its calls so a silent retry shows."""

    def __init__(self, fixture: dict):
        self.fixture = fixture
        self.calls = 0
        self.last_request: dict | None = None

    def __call__(self, request: dict) -> dict:
        self.calls += 1
        self.last_request = request
        return json.loads(json.dumps(self.fixture))


def _urllib_post(url: str, headers: dict, body: bytes, timeout_s: float) -> dict:
    """The only place in this package that opens a socket.

    It is injected as `http=` everywhere so that every test can stand exactly here and record the
    URL, headers and body without a network existing at all.
    """
    import urllib.request

    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8"))


class ProviderHttpTransport:
    """Base for a provider-specific dispatch path.

    WHY THIS IS NOT ONE GENERIC TRANSPORT

        The EVAL-012 branch sent `Authorization: Bearer <key>` to every provider. That is correct
        for OpenAI and simply wrong for the Gemini API-key route, which Google documents as
        `x-goog-api-key`. One generic transport was hiding two different contracts, and the first
        real Gemini call would have failed on authentication — after being counted as a trial and
        possibly billed. Auth is now per provider, and the emitted headers are tested.

        Constructing a transport opens no socket and reads no key. The key is read from the
        environment at DISPATCH time and never enters a request body or a persisted record.

    UNTESTED AGAINST A LIVE PROVIDER. Every exercise of this class in this branch goes through an
    injected recorder. Treat the real path as unproven until the first authorised call.
    """

    KEY_ENV = ""
    AUTH_HEADER = ""

    def __init__(self, resolved_version: str, http: Callable | None = None,
                 timeout_s: float = 60.0):
        if not resolved_version:
            raise ValueError(
                "resolved_version is required. The endpoint and the recorded provenance are both "
                "derived from the exact version, never from a floating alias.")
        self.resolved_version = resolved_version
        self.http = http or _urllib_post
        self.timeout_s = timeout_s
        self.calls = 0

    # -- provider-specific ------------------------------------------------------------------
    def endpoint(self) -> str:
        raise NotImplementedError

    def auth_headers(self, key: str) -> dict:
        raise NotImplementedError

    def outgoing_body(self, request: dict) -> dict:
        return request

    # -- dispatch ----------------------------------------------------------------------------
    def _read_key(self) -> str:
        import os

        key = os.environ.get(self.KEY_ENV)
        if not key:
            raise PreDispatchRefusal(
                f"{self.KEY_ENV} is not set. Keys are read from the environment at dispatch time "
                f"and are never committed, logged or persisted. Nothing was sent.")
        return key

    def __call__(self, request: dict) -> dict:
        """Exactly one dispatch. No loop, no retry — not even on an error response."""
        key = self._read_key()          # raises BEFORE anything is sent
        body = self.outgoing_body(request)
        headers = {"Content-Type": "application/json", **self.auth_headers(key)}

        # ---- THE DISPATCH BOUNDARY ----------------------------------------------------------
        # Everything above this line is provably pre-dispatch. Everything below may have reached
        # the provider, so every failure below is AMBIGUOUS and must never free the reservation.
        #
        # ensure_ascii=False, deliberately. With ASCII escaping a Devanagari target travels as
        # \uXXXX, and every leak check that scans for Devanagari characters goes blind in exactly
        # the place it is supposed to be watching.
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.calls += 1
        try:
            return self.http(self.endpoint(), headers, payload, self.timeout_s)
        except Exception as exc:
            api_status, error_class = classify_transport_failure(exc)
            raise AmbiguousDispatch(
                f"{type(exc).__name__} after dispatch to {self.endpoint()}: {exc}. The provider "
                f"may have received and billed this request; billing state is unknown.",
                api_status=api_status, error_class=error_class, cause=exc) from exc


class OpenAIHttpTransport(ProviderHttpTransport):
    """OpenAI Responses API. Bearer token; the exact model version travels in the body."""

    KEY_ENV = OPENAI_KEY_ENV
    ENDPOINT = "https://api.openai.com/v1/responses"

    def endpoint(self) -> str:
        return self.ENDPOINT

    def auth_headers(self, key: str) -> dict:
        return {"Authorization": f"Bearer {key}"}


class AnthropicHttpTransport(ProviderHttpTransport):
    """Anthropic Messages API. x-api-key + anthropic-version; model remains in the body."""

    KEY_ENV = ANTHROPIC_KEY_ENV
    ENDPOINT = "https://api.anthropic.com/v1/messages"

    def endpoint(self) -> str:
        return self.ENDPOINT

    def auth_headers(self, key: str) -> dict:
        return {"x-api-key": key, "anthropic-version": "2023-06-01"}


class GeminiHttpTransport(ProviderHttpTransport):
    """Gemini REST generateContent. API-key header, and the model lives in the URL.

    `x-goog-api-key`, not `Authorization: Bearer`. The model path segment is built from this
    transport's own `resolved_version`, and a request body naming a different model is REFUSED
    rather than silently dispatched to the URL's version — two disagreeing model names in one
    call is a run nobody can reproduce.
    """

    KEY_ENV = GOOGLE_KEY_ENV
    BASE = "https://generativelanguage.googleapis.com/v1beta/models"

    def endpoint(self) -> str:
        return f"{self.BASE}/{self.resolved_version}:generateContent"

    def auth_headers(self, key: str) -> dict:
        return {"x-goog-api-key": key}

    def outgoing_body(self, request: dict) -> dict:
        declared = request.get("model")
        if declared and declared != self.resolved_version:
            raise PreDispatchRefusal(
                f"request body names model {declared!r} but this transport is pinned to "
                f"{self.resolved_version!r}. Refusing rather than dispatching a call whose two "
                f"model names disagree. Nothing was sent.")
        # The REST route names the model in the URL; repeating it in the body is duplicate truth.
        return {k: v for k, v in request.items() if k != "model"}


def transport_for(provider: str, resolved_version: str, http: Callable | None = None,
                  timeout_s: float = 60.0) -> ProviderHttpTransport:
    """Pick the provider-correct transport. There is no generic fallback, by design."""
    if provider == "openai":
        return OpenAIHttpTransport(resolved_version, http=http, timeout_s=timeout_s)
    if provider == "anthropic":
        return AnthropicHttpTransport(resolved_version, http=http, timeout_s=timeout_s)
    if provider == "google":
        return GeminiHttpTransport(resolved_version, http=http, timeout_s=timeout_s)
    raise ValueError(
        f"no transport is defined for provider {provider!r}. A provider without an explicit "
        f"auth contract must not inherit somebody else's.")


# ------------------------------------------------------------------------------ blind check
GROUND_TRUTH_KEYS = frozenset({
    "target", "target_string", "expected", "expected_verdict", "failure_class", "edit_detail",
    "rendered_string", "base_string", "scoring_key",
})


def _walk_keys(obj: Any):
    """Every dict KEY in a payload, at any depth."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _walk_keys(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _walk_keys(v)


def _walk_strings(obj: Any):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _walk_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _walk_strings(v)


def verify_blind_payload(payload: dict, shape: str, target: str) -> list[str]:
    """Return every reason this payload violates its shape. An empty list is the only pass.

    For `transcribe`: the target must be absent, no ground-truth key may appear, and no
    Devanagari character may appear anywhere — the catch-all that finds a leak arriving through
    a field nobody anticipated.

    For `verdict`: the target must be present exactly once, and it must be in the prompt.
    """
    if shape not in SHAPES:
        raise ValueError(f"unknown shape {shape!r}")

    blob = json.dumps(payload, ensure_ascii=False)
    violations: list[str] = []

    # Ground-truth keys are forbidden in BOTH shapes. The target legitimately reaches a verdict
    # payload through the PROMPT and through nothing else; a dedicated field carrying it is how a
    # blind item quietly becomes a sighted one.
    for key in _walk_keys(payload):
        if key in GROUND_TRUTH_KEYS:
            violations.append(f"{shape} payload carries ground-truth key {key!r}")

    prompt = prompt_text_of(payload) or ""

    if shape == "transcribe":
        if target and target in blob:
            violations.append("transcribe payload contains the target string")
        if any("ऀ" <= ch <= "ॿ" for ch in blob):
            violations.append(
                "transcribe payload contains Devanagari text — every target in this battery is "
                "Devanagari, so its presence is decisive regardless of the field name")
    else:
        # PRESENCE in the prompt, which is the rule the Devanagari checker contract already
        # settled on. An earlier version here also demanded the target appear exactly once across
        # the whole serialised body; that is not an invariant. Short targets occur incidentally in
        # ordinary prompt prose, in structural enum values like "input_text", and inside base64
        # image data, so the stricter rule refused perfectly good payloads. A control that cries
        # wolf is a control that gets switched off.
        if not target:
            violations.append("verdict blind check needs the target to check against")
        elif target not in prompt:
            violations.append("verdict payload does not carry the target inside its prompt")

    return sorted(set(violations))


def prompt_text_of(payload: dict) -> str:
    """Concatenate every prompt-bearing text field of a provider request."""
    parts = []
    for block in payload.get("input", []) or []:
        for chunk in (block.get("content") or [block]):
            if isinstance(chunk, dict) and isinstance(chunk.get("text"), str):
                parts.append(chunk["text"])
    for c in payload.get("contents", []) or []:
        for part in c.get("parts", []) or []:
            if isinstance(part.get("text"), str):
                parts.append(part["text"])
    for message in payload.get("messages", []) or []:
        for part in message.get("content", []) or []:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                parts.append(part["text"])
    return "\n".join(parts)


# --------------------------------------------------------------------------------- base judge
@dataclass
class TextJudge:
    """One judge candidate, at one exact resolved version, behind one injected transport."""

    model_alias: str
    resolved_version: str
    transport: Callable[[dict], dict] | None = None
    guard: BudgetGuard | None = None
    provider: str = field(init=False, default="")
    # Set by the caller immediately before a call so the ledger row and the call record carry the
    # same trial identity. Never part of any request payload.
    call_context: dict = field(default_factory=dict)
    _last_cost_ref: str | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        if not self.model_alias:
            raise ValueError("model_alias is required")
        if not self.resolved_version:
            raise ValueError(
                "resolved_version is required. An alias silently repoints; a run that cannot name "
                "the exact version it called cannot be reproduced or compared.")

    # -- identity ------------------------------------------------------------------------
    def identity(self) -> dict:
        return {
            "provider": self.provider,
            "model_alias": self.model_alias,
            "resolved_version": self.resolved_version,
            "version_pinned_at_execution": True,
        }

    # -- request building (no dispatch) ----------------------------------------------------
    def build_transcribe_request(self, image_bytes: bytes) -> dict:
        """Blind. Takes no target: blindness is enforced by the signature before anything else."""
        raise NotImplementedError

    def build_verdict_request(self, image_bytes: bytes, target: str) -> dict:
        raise NotImplementedError

    def parse(self, raw: dict) -> EvaluatorResponse:
        raise NotImplementedError

    # -- dispatch ---------------------------------------------------------------------------
    def _reserve(self, estimated_usd: Decimal):
        """Reserve against whichever guard we were given.

        A persistent `StageBudget` accepts call context and writes it onto the ledger row; the
        in-memory `BudgetGuard` does not. Both are supported, because the dry-run path still uses
        the simple one and there is no reason to make it durable.
        """
        try:
            self.guard.reserve(estimated_usd, **(self.call_context or {}))
        except TypeError:
            self.guard.reserve(estimated_usd)
        self._last_cost_ref = getattr(self.guard, "cost_ref", None)

    def _settle(self, billed: Decimal, **extra) -> None:
        try:
            self.guard.record(billed, **{**(self.call_context or {}), **extra})
        except TypeError:
            # The in-memory BudgetGuard takes no context. It must still be CHARGED: an ambiguous
            # call that silently skipped settlement would be exactly the free call this correction
            # exists to prevent.
            self.guard.record(billed)

    def _dispatch(self, request: dict, estimated_usd: Decimal) -> EvaluatorResponse:
        """One call. One trial. No loop, no retry, no second chance — by construction."""
        if self.transport is None:
            raise DispatchRefused(
                "no transport injected. This judge cannot reach a provider, which is the correct "
                "state until EMP-001 is authorised.")
        if self.guard is None:
            raise DispatchRefused(
                "no budget guard. A paid call must be reserved against an explicit authorised "
                "ceiling before it is dispatched.")

        self._reserve(estimated_usd)               # raises BEFORE anything is sent

        try:
            raw = self.transport(request)          # exactly one call. No loop. No retry.
        except PreDispatchRefusal:
            # PROVEN nothing was sent. Only here may the headroom go back: a reservation that
            # outlives a call that never happened is budget nobody can ever spend.
            self._release()
            raise
        except AmbiguousDispatch as exc:
            # The provider may have received and billed this. Releasing would let the ledger claim
            # USD 0 for a call that cost money, which quietly weakens a user-approved hard ceiling
            # — and would erase the attempt from the evidence entirely.
            #
            # So: settle at the reserved estimate, mark the billing state unknown, and hand back a
            # response the caller must persist as ONE failed trial before stopping.
            return self._ambiguous_response(exc, estimated_usd)

        try:
            response = self.parse(raw)
        except ProviderResponseError as exc:
            # The request WAS sent. That the reply was unusable does not make the call free.
            ambiguous = AmbiguousDispatch(
                f"unparseable provider response: {exc}", api_status="error",
                error_class="malformed_response", cause=exc)
            return self._ambiguous_response(ambiguous, estimated_usd)

        self._settle(response.billed_usd if response.billed_usd is not None else Decimal("0"))
        return response

    def _release(self) -> None:
        release = getattr(self.guard, "release", None)
        if release:
            release()

    def _ambiguous_response(self, exc: AmbiguousDispatch,
                            estimated_usd: Decimal) -> EvaluatorResponse:
        """Settle conservatively and describe the call honestly. Never retried, never free."""
        self._settle(estimated_usd, billing_state="unknown_provisional")
        return EvaluatorResponse(
            text="",
            input_tokens=None,
            output_tokens=None,
            billed_usd=estimated_usd,
            provider_request_id=None,        # unavailable; identity lives on the trial record
            api_status=exc.api_status,
            error_class=exc.error_class,
            cost_basis="conservative_reserved_estimate_billing_unknown",
            raw_status_note=str(exc)[:300],
            billing_state="unknown_provisional",
            ambiguous_dispatch=True,
        )

    def _check_shape(self, request: dict, shape: str, target: str) -> None:
        """Run the blind check and REFUSE rather than dispatch.

        The checker contract requires this before any call is made, and it has to be enforced
        here rather than in a test: a target that reaches the wire has already destroyed the
        measurement, and no later assertion can undo it. Refusing costs nothing, because nothing
        was reserved or sent.
        """
        violations = verify_blind_payload(request, shape=shape, target=target)
        if violations:
            raise BlindnessViolation(
                f"{shape} payload refused before dispatch — nothing was sent:\n  - "
                + "\n  - ".join(violations))

    def transcribe(self, image_bytes: bytes, blind_check_target: str = "") -> EvaluatorResponse:
        """Blind. `blind_check_target` is EVALUATOR-SIDE ONLY: it is never put in the payload,
        it is used to prove the payload does not contain it."""
        request = self.build_transcribe_request(image_bytes)
        self._check_shape(request, "transcribe", blind_check_target)
        return self._dispatch(request, self._estimate())

    def verdict(self, image_bytes: bytes, target: str) -> EvaluatorResponse:
        request = self.build_verdict_request(image_bytes, target)
        self._check_shape(request, "verdict", target)
        return self._dispatch(request, self._estimate())

    def _estimate(self) -> Decimal:
        """Conservative pre-call reservation from the published rate."""
        rates = PRICE_BOOK[self.provider]
        return (rates["input_per_1m"] * Decimal("2000") / Decimal("1000000")
                + rates["output_per_1m"] * Decimal("64") / Decimal("1000000"))

    def provisional_cost(self, input_tokens: int | None, output_tokens: int | None) -> Decimal:
        rates = PRICE_BOOK[self.provider]
        return (rates["input_per_1m"] * Decimal(input_tokens or 0) / Decimal("1000000")
                + rates["output_per_1m"] * Decimal(output_tokens or 0) / Decimal("1000000"))

    # -- persistence -------------------------------------------------------------------------
    def call_record(self, response: EvaluatorResponse, shape: str) -> dict:
        """The persistable shape of one call. A transcribe record never carries the target."""
        if shape not in SHAPES:
            raise ValueError(f"unknown shape {shape!r}")
        return {
            **self.identity(),
            **{k: v for k, v in (self.call_context or {}).items()},
            "cost_ref": self._last_cost_ref,
            "shape": shape,
            "api_status": response.api_status,
            "error_class": response.error_class,
            "provider_request_id": response.provider_request_id,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "billed_usd": str(response.billed_usd) if response.billed_usd is not None else None,
            "cost_basis": response.cost_basis,
            "billing_state": response.billing_state,
            "ambiguous_dispatch": response.ambiguous_dispatch,
            "retries": 0,
            "prompt_sha256": prompt_sha256(
                PROMPT_TRANSCRIBE if shape == "transcribe" else PROMPT_VERDICT),
            "one_call_one_trial": True,
        }


# ------------------------------------------------------------------------------- OpenAI
class OpenAITextJudge(TextJudge):
    provider = "openai"

    def __post_init__(self) -> None:
        super().__post_init__()
        self.provider = "openai"

    def _image_part(self, image_bytes: bytes) -> dict:
        b64 = base64.b64encode(image_bytes).decode("ascii")
        return {"type": "input_image", "image_url": f"data:image/png;base64,{b64}"}

    def build_transcribe_request(self, image_bytes: bytes) -> dict:
        return {
            "model": self.resolved_version,
            "input": [{"role": "user", "content": [
                {"type": "input_text", "text": PROMPT_TRANSCRIBE},
                self._image_part(image_bytes)]}],
            "max_output_tokens": 128,
        }

    def build_verdict_request(self, image_bytes: bytes, target: str) -> dict:
        return {
            "model": self.resolved_version,
            "input": [{"role": "user", "content": [
                {"type": "input_text", "text": PROMPT_VERDICT.format(target=target)},
                self._image_part(image_bytes)]}],
            "max_output_tokens": 16,
        }

    def parse(self, raw: dict) -> EvaluatorResponse:
        usage = raw.get("usage") or {}
        in_tok = usage.get("input_tokens")
        out_tok = usage.get("output_tokens")
        cost = self.provisional_cost(in_tok, out_tok)
        req_id = raw.get("id")

        if raw.get("error"):
            err = raw["error"]
            return EvaluatorResponse("", in_tok, out_tok, cost, req_id, "error",
                                     err.get("code") or err.get("type") or "provider_error",
                                     raw_status_note=str(err)[:200])

        text_parts, refusal = [], None
        for block in raw.get("output", []) or []:
            for chunk in block.get("content", []) or []:
                if chunk.get("type") == "refusal":
                    refusal = chunk.get("refusal") or "refused"
                elif isinstance(chunk.get("text"), str):
                    text_parts.append(chunk["text"])

        if refusal is not None:
            return EvaluatorResponse("", in_tok, out_tok, cost, req_id, "refusal",
                                     "moderation_block", raw_status_note=refusal[:200])
        if not text_parts:
            raise ProviderResponseError("no text and no refusal in an ok-looking response")
        return EvaluatorResponse("".join(text_parts), in_tok, out_tok, cost, req_id, "ok")


# ----------------------------------------------------------------------------- Anthropic
class AnthropicTextJudge(TextJudge):
    provider = "anthropic"

    def __post_init__(self) -> None:
        super().__post_init__()
        self.provider = "anthropic"

    def _image_part(self, image_bytes: bytes) -> dict:
        return {"type": "image", "source": {
            "type": "base64", "media_type": "image/png",
            "data": base64.b64encode(image_bytes).decode("ascii")}}

    def build_transcribe_request(self, image_bytes: bytes) -> dict:
        return {
            "model": self.resolved_version,
            "max_tokens": 128,
            "messages": [{"role": "user", "content": [
                self._image_part(image_bytes),
                {"type": "text", "text": PROMPT_TRANSCRIBE}]}],
        }

    def build_verdict_request(self, image_bytes: bytes, target: str) -> dict:
        return {
            "model": self.resolved_version,
            "max_tokens": 16,
            "messages": [{"role": "user", "content": [
                self._image_part(image_bytes),
                {"type": "text", "text": PROMPT_VERDICT.format(target=target)}]}],
        }

    def parse(self, raw: dict) -> EvaluatorResponse:
        usage = raw.get("usage") or {}
        in_tok = usage.get("input_tokens")
        out_tok = usage.get("output_tokens")
        cost = self.provisional_cost(in_tok, out_tok)
        req_id = raw.get("id")

        if raw.get("error"):
            err = raw["error"]
            return EvaluatorResponse("", in_tok, out_tok, cost, req_id, "error",
                                     err.get("type") or "provider_error",
                                     raw_status_note=str(err)[:200])

        if raw.get("stop_reason") == "refusal":
            detail = raw.get("stop_details") or {}
            return EvaluatorResponse("", in_tok, out_tok, cost, req_id, "refusal",
                                     "moderation_block",
                                     raw_status_note=str(detail)[:200])

        text_parts = [b.get("text", "") for b in (raw.get("content") or [])
                      if b.get("type") == "text" and isinstance(b.get("text"), str)]
        if not any(text_parts):
            raise ProviderResponseError("no text and no refusal in an ok-looking Anthropic response")
        return EvaluatorResponse("".join(text_parts), in_tok, out_tok, cost, req_id, "ok")


# ------------------------------------------------------------------------------- Gemini
class GeminiTextJudge(TextJudge):
    provider = "google"

    def __post_init__(self) -> None:
        super().__post_init__()
        self.provider = "google"

    def _image_part(self, image_bytes: bytes) -> dict:
        return {"inline_data": {"mime_type": "image/png",
                                "data": base64.b64encode(image_bytes).decode("ascii")}}

    def build_transcribe_request(self, image_bytes: bytes) -> dict:
        return {
            "model": self.resolved_version,
            "contents": [{"role": "user", "parts": [
                {"text": PROMPT_TRANSCRIBE}, self._image_part(image_bytes)]}],
            "generationConfig": {"maxOutputTokens": 128, "temperature": 0},
        }

    def build_verdict_request(self, image_bytes: bytes, target: str) -> dict:
        return {
            "model": self.resolved_version,
            "contents": [{"role": "user", "parts": [
                {"text": PROMPT_VERDICT.format(target=target)}, self._image_part(image_bytes)]}],
            "generationConfig": {"maxOutputTokens": 16, "temperature": 0},
        }

    def parse(self, raw: dict) -> EvaluatorResponse:
        usage = raw.get("usageMetadata") or {}
        in_tok = usage.get("promptTokenCount")
        out_tok = usage.get("candidatesTokenCount")
        cost = self.provisional_cost(in_tok, out_tok)
        req_id = raw.get("responseId")

        if raw.get("error"):
            err = raw["error"]
            return EvaluatorResponse("", in_tok, out_tok, cost, req_id, "error",
                                     err.get("status") or "provider_error",
                                     raw_status_note=str(err)[:200])

        candidates = raw.get("candidates") or []
        if not candidates:
            return EvaluatorResponse("", in_tok, out_tok, cost, req_id, "refusal",
                                     "moderation_block",
                                     raw_status_note=str(raw.get("promptFeedback", ""))[:200])

        c0 = candidates[0]
        if c0.get("finishReason") in ("SAFETY", "BLOCKLIST", "PROHIBITED_CONTENT"):
            return EvaluatorResponse("", in_tok, out_tok, cost, req_id, "refusal",
                                     "moderation_block", raw_status_note=c0["finishReason"])

        parts = [p.get("text", "") for p in (c0.get("content", {}).get("parts") or [])]
        if not any(parts):
            raise ProviderResponseError("no text and no refusal in an ok-looking response")
        return EvaluatorResponse("".join(parts), in_tok, out_tok, cost, req_id, "ok")


# --------------------------------------------------------------------------- fal image routes
FAL_KEY_ENV = "FAL_KEY"

# The two frozen A-TEXT routes and their frozen request configuration. These are Controller
# decisions (config.yaml, CONTROL-STATE); they are not tunable at runtime, and a route that
# disagrees with the frozen config is refused rather than dispatched.
#
# NOTE ON SEEDS: neither body carries a seed, deliberately, even where a route exposes one.
# A-TEXT repeats are UNSEEDED on both routes so the first comparison is an inherent-variance
# comparison. A seed leaking in would silently make the two halves incomparable.
FAL_ROUTES = {
    "IMG-01": {
        "route": "openai/gpt-image-2",
        "body": {"image_size": {"width": 1024, "height": 1024},
                 "quality": "medium", "num_images": 1},
    },
    "IMG-02": {
        "route": "fal-ai/ideogram/v3",
        "body": {"rendering_speed": "BALANCED", "num_images": 1},
    },
}


def _urllib_get_bytes(url: str, timeout_s: float = 60.0) -> bytes:
    """The only artifact fetch that touches a network. Injected everywhere as `artifact_fetch`."""
    import urllib.request

    with urllib.request.urlopen(url, timeout=timeout_s) as resp:
        return resp.read()


class FalImageRoute:
    """One frozen fal generation route. Reaching fal is an injected concern, never a default.

    Construction opens no socket and reads no key. `FAL_KEY` is read at DISPATCH time only and
    never enters a request body or a persisted record.

    One attempt is exactly one dispatch — including an attempt that refuses or errors. There is no
    retry path, and `num_images` is pinned to 1 so one call can never quietly become several
    trials' worth of evidence.

    UNTESTED AGAINST fal. Every exercise in this branch goes through an injected recorder.
    """

    ENDPOINT_BASE = "https://fal.run"

    def __init__(self, slot: str, route: str, http: Callable | None = None,
                 artifact_fetch: Callable | None = None, timeout_s: float = 120.0):
        frozen = FAL_ROUTES.get(slot)
        if frozen is None:
            raise ValueError(
                f"unknown A-TEXT slot {slot!r}. The frozen slots are {sorted(FAL_ROUTES)}.")
        if route != frozen["route"]:
            raise ValueError(
                f"slot {slot} is frozen to route {frozen['route']!r}, not {route!r}. The route is "
                f"a Controller decision and is not changeable at runtime.")
        self.slot = slot
        self.route = route
        self.http = http or _urllib_post
        self.artifact_fetch = artifact_fetch or _urllib_get_bytes
        self.timeout_s = timeout_s
        self.calls = 0

    def endpoint(self) -> str:
        return f"{self.ENDPOINT_BASE}/{self.route}"

    def _read_key(self) -> str:
        import os

        key = os.environ.get(FAL_KEY_ENV)
        if not key:
            raise PreDispatchRefusal(
                f"{FAL_KEY_ENV} is not set. Keys are read from the environment at dispatch time "
                f"and are never committed, logged or persisted. Nothing was sent.")
        return key

    def build_body(self, request: dict) -> dict:
        """Frozen configuration plus the prompt. Nothing the caller passes can widen it."""
        if not request.get("prompt"):
            raise ValueError("a generation request needs a prompt")
        # Built from the frozen table, NOT from the caller's dict: an unexpected key — a seed, a
        # different size — cannot reach fal merely by being passed in.
        return {"prompt": request["prompt"], **FAL_ROUTES[self.slot]["body"]}

    def __call__(self, request: dict) -> dict:
        key = self._read_key()          # raises BEFORE anything is sent
        body = self.build_body(request)
        headers = {"Content-Type": "application/json", "Authorization": f"Key {key}"}
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")

        # ---- THE DISPATCH BOUNDARY ----------------------------------------------------------
        # Below this line fal may have received and billed the request, so every failure is
        # AMBIGUOUS. An image generation is the most expensive call in this tranche; letting one
        # disappear because the socket broke is exactly the accounting hole EVAL-015 closes.
        self.calls += 1                 # exactly one, no loop
        try:
            raw = self.http(self.endpoint(), headers, payload, self.timeout_s)
        except Exception as exc:
            api_status, error_class = classify_transport_failure(exc)
            raise AmbiguousDispatch(
                f"{type(exc).__name__} after dispatch to {self.endpoint()}: {exc}. fal may have "
                f"received and billed this generation; billing state is unknown.",
                api_status=api_status, error_class=error_class, cause=exc) from exc

        try:
            return self.parse(raw)
        except Exception as exc:
            raise AmbiguousDispatch(
                f"unparseable fal response: {exc}. The request was sent.",
                api_status="error", error_class="malformed_response", cause=exc) from exc

    def parse(self, raw: dict) -> dict:
        """Map a fal response onto the persistence vocabulary. A refusal is not an error."""
        base = {
            "slot": self.slot,
            "route": self.route,
            "provider_surface": "fal",
            "provider_request_id": raw.get("request_id"),
            "artifact_url": None,
            "fetch_artifact": None,
            "error_class": None,
            "cost_usd": str(NOMINAL_FAL_PRICE_USD[self.slot]),
            "cost_basis": "provisional_planning_rate",
        }

        if raw.get("error"):
            err = raw["error"]
            code = err.get("type") or err.get("code") or "provider_error"
            # A content-policy block is a REFUSAL: the provider understood and declined. An
            # infrastructure failure is an ERROR. Both consume their trial; only one is about the
            # prompt, and folding them together would corrupt both numbers.
            refusal = code in ("content_policy_violation", "moderation_block", "safety")
            return {**base, "api_status": "refusal" if refusal else "error",
                    "error_class": "moderation_block" if refusal else code,
                    "raw_note": str(err)[:200]}

        images = raw.get("images") or []
        if not images or not images[0].get("url"):
            return {**base, "api_status": "error", "error_class": "no_artifact_returned",
                    "raw_note": "ok-looking response carried no image url"}

        url = images[0]["url"]
        return {**base, "api_status": "ok", "artifact_url": url,
                "fetch_artifact": lambda: self.artifact_fetch(url)}


def fal_route_for(slot: str, config: dict, http: Callable | None = None,
                  artifact_fetch: Callable | None = None) -> FalImageRoute:
    """Build the frozen route for a slot straight from config.yaml."""
    return FalImageRoute(slot=slot, route=config["atex"]["slots"][slot]["route"],
                         http=http, artifact_fetch=artifact_fetch)


# ------------------------------------------------------------------------------- fixtures
# Deterministic provider-SHAPED JSON for tests. Not captured from any provider; no call was made
# to produce them, and they are not evidence about any provider's behaviour.
OPENAI_OK_FIXTURE = {
    "id": "resp_abc123",
    "output": [{"content": [{"type": "output_text", "text": "Flat 50% Off"}]}],
    "usage": {"input_tokens": 812, "output_tokens": 7},
}
OPENAI_REFUSAL_FIXTURE = {
    "id": "resp_ref456",
    "output": [{"content": [{"type": "refusal", "refusal": "I can't help with that."}]}],
    "usage": {"input_tokens": 800, "output_tokens": 2},
}
OPENAI_ERROR_FIXTURE = {
    "id": "resp_err789",
    "error": {"type": "server_error", "code": "internal_error"},
    "usage": {"input_tokens": 790, "output_tokens": 0},
}
ANTHROPIC_OK_FIXTURE = {
    "id": "msg_fake_abc123", "type": "message", "role": "assistant",
    "content": [{"type": "text", "text": "Flat 50% Off"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 812, "output_tokens": 7},
}
ANTHROPIC_REFUSAL_FIXTURE = {
    "id": "msg_fake_ref456", "type": "message", "role": "assistant",
    "content": [], "stop_reason": "refusal",
    "stop_details": {"type": "refusal", "category": "general_harms"},
    "usage": {"input_tokens": 800, "output_tokens": 2},
}
ANTHROPIC_ERROR_FIXTURE = {
    "id": "msg_fake_err789",
    "error": {"type": "api_error", "message": "backend unavailable"},
    "usage": {"input_tokens": 790, "output_tokens": 0},
}

GEMINI_OK_FIXTURE = {
    "responseId": "gen-req-99",
    "candidates": [{"content": {"parts": [{"text": "Flat 50% Off"}]}, "finishReason": "STOP"}],
    "usageMetadata": {"promptTokenCount": 640, "candidatesTokenCount": 6},
}
GEMINI_REFUSAL_FIXTURE = {
    "responseId": "gen-req-100",
    "candidates": [{"content": {"parts": []}, "finishReason": "SAFETY"}],
    "usageMetadata": {"promptTokenCount": 640, "candidatesTokenCount": 0},
}
GEMINI_ERROR_FIXTURE = {
    "responseId": "gen-req-101",
    "error": {"status": "UNAVAILABLE", "message": "backend overloaded"},
    "usageMetadata": {"promptTokenCount": 630, "candidatesTokenCount": 0},
}

# fal-shaped fixtures. Not captured from fal; no call was made to produce them, and they are not
# evidence about fal or about either route's behaviour.
FAL_OK_FIXTURE = {
    "request_id": "fal-req-001",
    "images": [{"url": "https://fal.media/files/fake/atex-0001.png",
                "width": 1024, "height": 1024, "content_type": "image/png"}],
}
FAL_REFUSAL_FIXTURE = {
    "request_id": "fal-req-002",
    "error": {"type": "content_policy_violation", "message": "blocked by content policy"},
}
FAL_ERROR_FIXTURE = {
    "request_id": "fal-req-003",
    "error": {"type": "internal_server_error", "message": "upstream failure"},
}
