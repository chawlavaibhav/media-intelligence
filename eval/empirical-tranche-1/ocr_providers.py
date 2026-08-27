#!/usr/bin/env python3
"""OCR-FAMILY evaluator adapters for EMP-001. First candidate: Google Cloud Vision TEXT_DETECTION.

WHY THIS IS A SEPARATE MODULE FROM `providers.py`

    `providers.py` holds the general-VLM judge family: models that take a prompt, can be shown a
    target, and answer in prose. An OCR service shares none of that. It has no prompt, no verdict
    shape, no token accounting and a per-image price rather than a per-token one.

    Folding Cloud Vision into the VLM judge base would mean carrying fields that have no meaning
    for it — `output_tokens`, `verdict`, `resolved_version` as a model snapshot — and every one of
    those would be a place for a plausible-looking zero to hide. A separate adapter says what is
    actually true about this family.

WHAT IS DELIBERATELY REUSED

    The blindness checker, the exceptions, and the dispatch discipline. Those are properties of
    the EXPERIMENT, not of the provider, and a second copy of them would drift.

UNTESTED AGAINST A LIVE PROVIDER. Every exercise of this module goes through an injected
recorder. EVAL-022 makes zero Cloud Vision calls; treat the real path as unproven until the first
authorised call.
"""
from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Callable

from budget_guard import BudgetGuard
from providers import (
    AmbiguousDispatch,
    DispatchRefused,
    EvaluatorResponse,
    PreDispatchRefusal,
    ProviderResponseError,
    _urllib_post,
    verify_blind_payload,
)

CLOUD_VISION_KEY_ENV = "GOOGLE_CLOUD_VISION_API_KEY"
CLOUD_VISION_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"

# Conservative PAID basis. Google documents the first 1,000 Text Detection units per month as
# free, and this deliberately does not use that: a free-tier assumption is an assumption about
# what the rest of the account did this month, which the ledger cannot verify and must not
# silently depend on. USD 1.50 / 1000 images.
CLOUD_VISION_USD_PER_1000_IMAGES = Decimal("1.50")
CLOUD_VISION_USD_PER_IMAGE = CLOUD_VISION_USD_PER_1000_IMAGES / Decimal("1000")  # 0.0015


class OcrEngine:
    """One OCR candidate, at one exact provider configuration, behind one injected transport."""

    family = "ocr"
    provider = ""

    def identity(self) -> dict:
        raise NotImplementedError

    def build_request(self, image_bytes: bytes) -> dict:
        raise NotImplementedError

    def parse(self, raw: dict) -> EvaluatorResponse:
        raise NotImplementedError


class CloudVisionHttpTransport:
    """Cloud Vision REST dispatch. API key travels as a query parameter, per Google's docs.

    Constructing this opens no socket and reads no key. The key is read from the environment at
    DISPATCH time only, and never enters a request body, a log line or a persisted record.
    """

    KEY_ENV = CLOUD_VISION_KEY_ENV
    ENDPOINT = CLOUD_VISION_ENDPOINT

    def __init__(self, http: Callable | None = None, timeout_s: float = 60.0):
        self.http = http or _urllib_post
        self.timeout_s = timeout_s
        self.calls = 0
        self.last_request: dict | None = None
        self.last_url: str | None = None

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
        key = self._read_key()                      # raises BEFORE anything is sent
        url = f"{self.ENDPOINT}?key={key}"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        body = json.dumps(request, ensure_ascii=False).encode("utf-8")

        # ---- THE DISPATCH BOUNDARY -------------------------------------------------------
        # Everything above is provably pre-dispatch. Everything below may have reached Google.
        self.calls += 1
        self.last_request = request
        # The URL carries the key, so the RECORDED url is the redacted one. A persisted record
        # that leaks a credential is a worse failure than a lost debugging aid.
        self.last_url = f"{self.ENDPOINT}?key=<redacted>"
        try:
            return self.http(url, headers, body, self.timeout_s)
        except Exception as exc:                    # noqa: BLE001 - classified by the caller
            raise AmbiguousDispatch(
                f"Cloud Vision dispatch failed after the send boundary: {type(exc).__name__}: "
                f"{exc}. It cannot be proven the request was not received and billed.",
                api_status="error", error_class="transport_failure", cause=exc) from exc


@dataclass
class CloudVisionTextDetection(OcrEngine):
    """Google Cloud Vision `TEXT_DETECTION` as an exact-text checker.

    NO LANGUAGE HINTS, DELIBERATELY

        Google documents that omitting `languageHints` generally gives the best result and lets
        automatic detection work. A Hindi hint is a DIFFERENT candidate configuration with
        different behaviour, and it would be dishonest to introduce it as a silent runtime tweak
        after seeing a disappointing score. If it is ever tried it gets its own configuration
        identity and its own screen.

    TEXT_DETECTION RATHER THAN DOCUMENT_TEXT_DETECTION

        The battery is single words and short lines. Google documents TEXT_DETECTION as optimised
        for sparse text in images and DOCUMENT_TEXT_DETECTION for dense documents. The battery is
        the former.
    """

    config_alias: str = "cloud-vision-text-detection-v1"
    feature: str = "TEXT_DETECTION"
    language_hints: tuple[str, ...] = ()
    transport: Callable[[dict], dict] | None = None
    guard: BudgetGuard | None = None
    provider: str = field(init=False, default="google_cloud_vision")
    # Set immediately before a call so the ledger row and the call record carry the same trial
    # identity. Never part of any request payload.
    call_context: dict = field(default_factory=dict)
    _last_cost_ref: str | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        if self.language_hints:
            raise ValueError(
                "the first Cloud Vision candidate is pinned to NO languageHints. A hinted "
                "configuration is a separate candidate with its own identity, not a variant of "
                "this one.")

    # -- identity ---------------------------------------------------------------------------
    def identity(self) -> dict:
        return {
            "family": self.family,
            "provider": self.provider,
            "config_alias": self.config_alias,
            "endpoint": CLOUD_VISION_ENDPOINT,
            "feature": self.feature,
            "language_hints": list(self.language_hints),
            "api_version": "v1",
            "config_pinned_at_execution": True,
        }

    def config_sha256(self) -> str:
        """A configuration fingerprint, so 'which Cloud Vision was this' is answerable later."""
        return hashlib.sha256(
            json.dumps(self.identity(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    # -- request building (no dispatch) -----------------------------------------------------
    def build_request(self, image_bytes: bytes) -> dict:
        """Blind by construction: the signature takes an image and nothing else."""
        return {
            "requests": [{
                "image": {"content": base64.b64encode(image_bytes).decode("ascii")},
                "features": [{"type": self.feature, "maxResults": 1}],
            }]
        }

    # -- parsing ----------------------------------------------------------------------------
    def parse(self, raw: dict) -> EvaluatorResponse:
        """Deterministic. Every branch is a documented Cloud Vision response shape."""
        cost = CLOUD_VISION_USD_PER_IMAGE
        req_id = raw.get("responseId")

        # Top-level transport/quota error object.
        if raw.get("error"):
            err = raw["error"]
            return EvaluatorResponse(
                "", None, None, cost, req_id, "error",
                _classify_error(err), cost_basis="published_per_image_rate",
                raw_status_note=str(err)[:200])

        responses = raw.get("responses")
        if not isinstance(responses, list) or not responses:
            raise ProviderResponseError(
                "Cloud Vision reply had no `responses` array. Nothing usable, and no documented "
                "status to classify it by.")

        r0 = responses[0]
        if not isinstance(r0, dict):
            raise ProviderResponseError("Cloud Vision `responses[0]` was not an object.")

        # Per-response error object — documented, so it is a well-formed evaluator failure.
        if r0.get("error"):
            err = r0["error"]
            return EvaluatorResponse(
                "", None, None, cost, req_id, "error",
                _classify_error(err), cost_basis="published_per_image_rate",
                raw_status_note=str(err)[:200])

        text = _extract_text(r0)
        if text is None:
            raise ProviderResponseError(
                "Cloud Vision response carried neither an error, a fullTextAnnotation nor a "
                "textAnnotations array. The shape is undocumented, so it fails closed.")

        if not text.strip():
            # THE OCR-FAMILY RULE. Every battery image is a human-reviewed rendering of visible
            # text. No transcription is a service failure, never a match — coercing it to match
            # would manufacture a false pass out of an outage.
            return EvaluatorResponse(
                "", None, None, cost, req_id, "error", "empty_transcription",
                cost_basis="published_per_image_rate",
                raw_status_note="no text returned for a known-visible-text image")

        return EvaluatorResponse(text, None, None, cost, req_id, "ok",
                                 cost_basis="published_per_image_rate")

    # -- dispatch ---------------------------------------------------------------------------
    def estimate_usd(self) -> Decimal:
        """Conservative pre-call reservation. Per IMAGE, not per token — this is not an LLM."""
        return CLOUD_VISION_USD_PER_IMAGE

    def _reserve(self, estimated_usd: Decimal) -> None:
        try:
            self.guard.reserve(estimated_usd, **(self.call_context or {}))
        except TypeError:
            self.guard.reserve(estimated_usd)
        self._last_cost_ref = getattr(self.guard, "cost_ref", None)

    def _settle(self, billed: Decimal, **extra) -> None:
        try:
            self.guard.record(billed, **{**(self.call_context or {}), **extra})
        except TypeError:
            self.guard.record(billed)

    def _release(self) -> None:
        release = getattr(self.guard, "release", None)
        if release is not None:
            try:
                release(**(self.call_context or {}))
            except TypeError:
                release()

    def transcribe(self, image_bytes: bytes, blind_check_target: str = "") -> EvaluatorResponse:
        """One image in, one transcription out. One call, one trial.

        `blind_check_target` is EVALUATOR-SIDE ONLY: it is never put in the payload, it is used to
        prove the payload does not contain it.
        """
        request = self.build_request(image_bytes)

        violations = verify_blind_payload(request, "transcribe", blind_check_target)
        if violations:
            raise DispatchRefused(
                "BLINDNESS VIOLATION — refusing to dispatch: " + "; ".join(violations)
                + ". A target that reaches the wire has already destroyed the measurement, and no "
                  "later assertion can undo it.")

        if self.transport is None:
            raise DispatchRefused(
                "no transport injected. This engine cannot reach a provider, which is the correct "
                "state until an OCR-family run is authorised.")
        if self.guard is None:
            raise DispatchRefused(
                "no budget guard. A paid call must be reserved against an explicit authorised "
                "ceiling before it is dispatched.")

        estimated = self.estimate_usd()
        self._reserve(estimated)                    # raises BEFORE anything is sent

        try:
            raw = self.transport(request)           # exactly one call. No loop. No retry.
        except PreDispatchRefusal:
            # PROVEN nothing was sent. Only here may the headroom go back.
            self._release()
            raise
        except AmbiguousDispatch as exc:
            return self._ambiguous(exc, estimated)

        try:
            response = self.parse(raw)
        except ProviderResponseError as exc:
            # The request WAS sent. An unusable reply does not make the call free.
            return self._ambiguous(
                AmbiguousDispatch(f"unparseable Cloud Vision reply: {exc}",
                                  api_status="error", error_class="malformed_response",
                                  cause=exc),
                estimated, error_class="malformed_response")

        # `EvaluatorResponse` is frozen on purpose: a settled trial record is evidence, and
        # evidence that can be edited after the fact is not evidence. `parse` already priced the
        # call at the published per-image rate, so settlement reads it rather than rewriting it.
        billed = response.billed_usd if response.billed_usd is not None else estimated
        self._settle(billed, billing_state=response.billing_state)
        return response

    def _ambiguous(self, exc: AmbiguousDispatch, estimated: Decimal,
                   error_class: str = "ambiguous_dispatch") -> EvaluatorResponse:
        """Settle at the reserved estimate, mark the billing unknown, hand back one failed trial.

        Releasing here would let the ledger claim USD 0 for a call that may have cost money, and
        would erase the attempt from the evidence entirely.
        """
        self._settle(estimated, billing_state="unknown_provisional")
        return EvaluatorResponse(
            "", None, None, estimated, None, "error", error_class,
            cost_basis="published_per_image_rate",
            raw_status_note=str(exc)[:200],
            billing_state="unknown_provisional", ambiguous_dispatch=True)


def _classify_error(err: Any) -> str:
    """Map a documented Cloud Vision error object onto a stable, greppable class."""
    if isinstance(err, dict):
        status = err.get("status")
        code = err.get("code")
        if status:
            return f"provider_error_{str(status).lower()}"
        if code:
            return f"provider_error_http_{code}"
    return "provider_error"


def _extract_text(response_0: dict) -> str | None:
    """Cloud Vision exposes the full transcription two documented ways. Prefer the explicit one.

    Returns None when NEITHER documented carrier is present — an undocumented shape, which the
    caller turns into a fail-closed malformed response rather than an empty string.
    """
    full = response_0.get("fullTextAnnotation")
    if isinstance(full, dict) and "text" in full:
        return full.get("text") or ""

    annotations = response_0.get("textAnnotations")
    if isinstance(annotations, list):
        if not annotations:
            return ""                                # documented "nothing found" shape
        first = annotations[0]
        if isinstance(first, dict):
            return first.get("description") or ""

    return None


# ------------------------------------------------------------------ zero-network test fixtures
CLOUD_VISION_OK_FIXTURE = {
    "responseId": "cv-req-ok",
    "responses": [{
        "textAnnotations": [{"description": "कण्डाघाट"}],
        "fullTextAnnotation": {"text": "कण्डाघाट"},
    }],
}

CLOUD_VISION_EMPTY_FIXTURE = {
    "responseId": "cv-req-empty",
    "responses": [{"textAnnotations": []}],
}

CLOUD_VISION_RESPONSE_ERROR_FIXTURE = {
    "responseId": "cv-req-err",
    "responses": [{"error": {"code": 7, "status": "PERMISSION_DENIED",
                             "message": "Cloud Vision API has not been used in project"}}],
}

CLOUD_VISION_TOP_LEVEL_ERROR_FIXTURE = {
    "error": {"code": 429, "status": "RESOURCE_EXHAUSTED", "message": "Quota exceeded"},
}

CLOUD_VISION_MALFORMED_FIXTURE = {
    "responseId": "cv-req-malformed",
    "responses": [{"somethingUndocumented": True}],
}
