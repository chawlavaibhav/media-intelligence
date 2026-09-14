"""One refusal type. A refusal carries a machine code, a human sentence and context.

Nothing in this lane returns a degraded result: it either produces the object or refuses
by name. Silence and defaults are the two failure modes the contracts exist to prevent.
"""
from __future__ import annotations

from typing import Any


class Refusal(Exception):
    # Intake
    MALFORMED_REQUEST = "MALFORMED_REQUEST"
    SCHEMA_VIOLATION = "SCHEMA_VIOLATION"
    CONSENT_MISSING = "CONSENT_MISSING"
    POLICY_PROFILE_UNKNOWN = "POLICY_PROFILE_UNKNOWN"
    POLICY_LIMIT_MISSING = "POLICY_LIMIT_MISSING"
    KIND_NOT_IN_PROFILE = "KIND_NOT_IN_PROFILE"
    KIND_NOT_IN_REGISTRY = "KIND_NOT_IN_REGISTRY"
    JOB_IMMUTABLE = "JOB_IMMUTABLE"
    # 14 Sep 2026 (lane E): the two Alpha-1 profile limits the compiler and intake now enforce, plus
    # the provenance block a brief may carry outside the contract object.
    MOTION_DEPENDENCY_MISSING = "MOTION_DEPENDENCY_MISSING"
    PROVENANCE_MALFORMED = "PROVENANCE_MALFORMED"
    # Canon
    CANON_BUDGET_EXCEEDED = "CANON_BUDGET_EXCEEDED"
    CANON_TRIGGER_TABLE_HOLE = "CANON_TRIGGER_TABLE_HOLE"
    # Spec
    NR_BINDING_MISSING = "NR_BINDING_MISSING"
    TEXT_STRATEGY_UNDECIDABLE = "TEXT_STRATEGY_UNDECIDABLE"
    ACCEPTANCE_STYLE_VIOLATION = "ACCEPTANCE_STYLE_VIOLATION"
    ACCEPTANCE_COUNT_OUT_OF_RANGE = "ACCEPTANCE_COUNT_OUT_OF_RANGE"
    PLANNER_FIXTURE_MISSING = "PLANNER_FIXTURE_MISSING"
    PLANNER_RESPONSE_INVALID = "PLANNER_RESPONSE_INVALID"
    TEXT_STRATEGY_NOT_ALLOWED_BY_PROFILE = "TEXT_STRATEGY_NOT_ALLOWED_BY_PROFILE"
    BLUEPRINT_UNPARSEABLE = "BLUEPRINT_UNPARSEABLE"
    NO_DISPATCH_ALLOWED = "NO_DISPATCH_ALLOWED"

    def __init__(self, code: str, message: str, **context: Any) -> None:
        self.code = code
        self.message = message
        self.context = context
        detail = "; ".join(f"{k}={v!r}" for k, v in sorted(context.items()))
        super().__init__(f"{code}: {message}" + (f" [{detail}]" if detail else ""))
