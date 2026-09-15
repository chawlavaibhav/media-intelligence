"""Transient-error classification: an outage is not a bad draw.

WHY (production-learning UPWORK-INTRO-001, SD-09 / SD-10). Vertex Veo answered gRPC 14 UNAVAILABLE twice
and succeeded 100 s later; Lyria answered 503 / 500 / 500 on one prompt wording. The pilot ledger wrote
`failed_or_filtered` — a label that cannot tell an outage from a content refusal from a draw a person
rejected. This module gives a provider failure one of three names and NEVER the fourth:

  infrastructure_transient   outage, 5xx, 429, UNAVAILABLE / DEADLINE_EXCEEDED / RESOURCE_EXHAUSTED, timeout
  provider_refusal           the provider declined the request on content / policy / validation grounds
  unclassified               anything else — reported, not guessed

`model_quality_failure` exists here only as a constant to test against: it is assigned solely by a gate
row (LIMIT-TEXT, DISPATCH-*, INFRA-*) or a human verdict over an artifact that came back, never by this
classifier, because a call that returned nothing says nothing about the model's quality.

The attempt `status` vocabulary of OUTCOME-EVENT-v1 (ok | refusal | provider_error | timeout | local_fault
| dry_not_sent) is untouched; `failure_class` rides on the loop's attempt record beside it.
"""
from __future__ import annotations

import re

INFRASTRUCTURE_TRANSIENT = "infrastructure_transient"
PROVIDER_REFUSAL = "provider_refusal"
UNCLASSIFIED = "unclassified"
MODEL_QUALITY_FAILURE = "model_quality_failure"      # never returned by classify(); see the module docstring

TRANSIENT_HTTP = {408, 425, 429, 500, 502, 503, 504}
TRANSIENT_GRPC = {4: "DEADLINE_EXCEEDED", 8: "RESOURCE_EXHAUSTED", 13: "INTERNAL", 14: "UNAVAILABLE"}
TRANSIENT_WORDS = re.compile(r"\b(unavailable|deadline exceeded|resource exhausted|try again later|temporarily|"
                             r"overloaded|rate.?limit|service unavailable|gateway time.?out|internal error)\b", re.I)
REFUSAL_HTTP = {400, 403, 422}
REFUSAL_WORDS = re.compile(r"\b(content filter|safety|policy|blocked|moderat|prohibited|invalid argument|"
                           r"unsupported|validation)\w*", re.I)


def classify(*, http_status=None, grpc_code=None, message: str = "", timed_out: bool = False) -> dict:
    msg = str(message or "")
    basis = []
    if timed_out:
        basis.append("client timeout")
    if grpc_code is not None and int(grpc_code) in TRANSIENT_GRPC:
        basis.append(f"gRPC {int(grpc_code)} {TRANSIENT_GRPC[int(grpc_code)]}")
    if http_status is not None and int(http_status) in TRANSIENT_HTTP:
        basis.append(f"HTTP {int(http_status)}")
    if basis:
        return _result(INFRASTRUCTURE_TRANSIENT, basis, retry=True)
    if http_status is not None and int(http_status) in REFUSAL_HTTP:
        hit = REFUSAL_WORDS.search(msg)
        return _result(PROVIDER_REFUSAL, [f"HTTP {int(http_status)}" + (f" ({hit.group(0)})" if hit else "")], retry=False)
    if TRANSIENT_WORDS.search(msg) and http_status is None and grpc_code is None:
        return _result(INFRASTRUCTURE_TRANSIENT, [f"message: {TRANSIENT_WORDS.search(msg).group(0)!r}"], retry=True)
    if REFUSAL_WORDS.search(msg) and http_status is None and grpc_code is None:
        return _result(PROVIDER_REFUSAL, [f"message: {REFUSAL_WORDS.search(msg).group(0)!r}"], retry=False)
    return _result(UNCLASSIFIED, [f"http_status={http_status!r} grpc_code={grpc_code!r} message={msg[:80]!r}"], retry=False)


def _result(cls: str, basis: list, *, retry: bool) -> dict:
    return {
        "failure_class": cls,
        "counts_against_route_quality": False,       # a call that returned nothing says nothing about the model
        "retry_eligible": retry,
        "basis": "; ".join(basis),
        "note": ("retry only under a pre-declared allowance (UPWORK-INTRO-001 Addendum-1 pattern); never silently"
                 if retry else "not retried on the same route without a changed request"),
    }


def failure_record(attempt: dict, error_class: dict, *, reserved_usd="0", status: str = "provider_error") -> dict:
    """The attempt-record fragment the loop keeps for a call that returned no artifact: OUTCOME-EVENT-v1's
    own `status` vocabulary plus the failure class beside it. Money stays reserved and provisional until
    a vendor statement says otherwise — an outage may still bill."""
    if status not in ("provider_error", "timeout", "refusal", "local_fault"):
        raise ValueError(f"status {status!r} is not an OUTCOME-EVENT-v1 failure status")
    return {
        "attempt_id": attempt.get("attempt_id"),
        "route_key": attempt.get("route_key"),
        "status": status,
        "failure_class": error_class["failure_class"],
        "counts_against_route_quality": error_class["counts_against_route_quality"],
        "retry_eligible": error_class["retry_eligible"],
        "basis": error_class["basis"],
        "artifact_sha256": None,
        "artifact_origin": "none",
        "reserved_usd": str(reserved_usd),
        "settled_usd": "0",
        "billing_state": "unknown_provisional",
    }
