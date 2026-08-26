#!/usr/bin/env python3
"""EMP-001 authorisation gate and fail-closed cumulative spend guard.

WHY THIS FILE EXISTS

    Every other protection in this tranche is a matter of discipline. This one is mechanical.
    The tranche may consume at most USD 10.00 of API spend, and only after a human has said so in
    an explicit file that names the tranche and the exact ceiling. Nothing here infers approval
    from "continue", from an existing account balance, from prior research budgets or from
    provider credits already sitting in an account.

    The guard fails CLOSED in every direction:

      * no authorisation file            -> NotAuthorised
      * `authorised: false`              -> NotAuthorised
      * `authorised: "true"` (a string)  -> NotAuthorised, because a string is not a decision
      * a ceiling of zero or below       -> NotAuthorised
      * a ceiling above the proposal     -> NotAuthorised, because the runner may not raise it
      * a different tranche id           -> NotAuthorised
      * any authorised retry             -> NotAuthorised; EMP-001 authorises 0

    `reserve()` is the call that must happen BEFORE network dispatch. `record()` is the call that
    happens after, with the actual billed amount. Both refuse rather than truncate: a run that
    stops with an incomplete result is recoverable, a run that silently spent more than it was
    given is not.

    Money is Decimal, never float. `record(0.11)` is refused with TypeError rather than quietly
    accumulating binary rounding error into a ceiling comparison.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parent
AUTHORISATION_EXAMPLE_PATH = PACKAGE_ROOT / "authorization.example.yaml"
AUTHORISATION_LOCAL_PATH = PACKAGE_ROOT / "authorization.local.yaml"

TRANCHE_ID = "EMP-001"

# The proposed ceiling. This is the MAXIMUM a local authorisation file may name; it is not itself
# an authorisation. Controller reference:
# coordination/plans/2026-08-26-FIRST-EMPIRICAL-TRANCHE-PROPOSAL.md
MAX_PROPOSED_CEILING_USD = Decimal("10.00")
RETRIES_AUTHORISED = 0


class BudgetExceeded(RuntimeError):
    """The next or recorded amount would take cumulative spend past the ceiling."""


class NotAuthorised(RuntimeError):
    """No valid explicit authorisation exists for a paid EMP-001 call."""


@dataclass
class BudgetGuard:
    """Cumulative spend guard for one authorised tranche.

    `authorised_usd` is the ceiling. `spent_usd` is cumulative recorded consumption.
    """

    authorised_usd: Decimal
    spent_usd: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        for name in ("authorised_usd", "spent_usd"):
            _require_decimal(getattr(self, name), name)
        if self.authorised_usd <= 0:
            raise ValueError("positive explicit authorisation required")
        if self.spent_usd < 0:
            raise ValueError("spent_usd cannot be negative")

    @property
    def remaining_usd(self) -> Decimal:
        return self.authorised_usd - self.spent_usd

    def reserve(self, estimated_usd: Decimal) -> None:
        """Called BEFORE dispatching a paid call. Raises rather than letting the call go out."""
        _require_decimal(estimated_usd, "estimated_usd")
        if estimated_usd < 0:
            raise ValueError("a reservation cannot be negative")
        if self.spent_usd + estimated_usd > self.authorised_usd:
            raise BudgetExceeded(
                f"next call could exceed authorised ceiling: "
                f"spent {self.spent_usd} + estimated {estimated_usd} > {self.authorised_usd}")

    def record(self, actual_usd: Decimal) -> None:
        """Called AFTER a paid call with the actual billed amount."""
        _require_decimal(actual_usd, "actual_usd")
        if actual_usd < 0:
            raise ValueError(
                "a negative spend record would manufacture headroom; a correction is a new "
                "ledger entry, never a subtraction here")
        if self.spent_usd + actual_usd > self.authorised_usd:
            raise BudgetExceeded(
                f"recorded spend exceeds authorised ceiling: "
                f"spent {self.spent_usd} + actual {actual_usd} > {self.authorised_usd}")
        self.spent_usd += actual_usd


def _require_decimal(value: Any, name: str) -> None:
    if not isinstance(value, Decimal):
        raise TypeError(
            f"{name} must be a Decimal, got {type(value).__name__}. Money is never a float here: "
            f"binary rounding inside a ceiling comparison is how a hard limit becomes a soft one.")


@dataclass(frozen=True)
class Authorisation:
    """A parsed authorisation file. Parsing it is not the same as accepting it."""

    authorised: bool
    tranche_id: str | None
    max_consumed_api_spend_usd: Decimal
    retries_authorised: int
    approved_by: str | None = None
    approved_at: str | None = None
    source_path: str = ""
    refusals: tuple[str, ...] = field(default_factory=tuple)


def load_authorisation(path: Path | str) -> Authorisation:
    """Read an authorisation file and list every reason it would be refused.

    Never raises on a merely disabled file — a disabled file is the expected committed state.
    Raises only when the bytes cannot be read as the declared shape at all.
    """
    import yaml

    path = Path(path)
    if not path.exists():
        return Authorisation(
            authorised=False, tranche_id=None, max_consumed_api_spend_usd=Decimal("0"),
            retries_authorised=0, source_path=str(path),
            refusals=("no authorisation file exists at that path",))

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise NotAuthorised(f"{path}: authorisation file is not a mapping")

    raw_authorised = data.get("authorised", False)
    raw_ceiling = data.get("max_consumed_api_spend_usd", 0)
    raw_retries = data.get("retries_authorised", 0)

    refusals: list[str] = []

    # `is True`, not truthiness. The string "true", the integer 1 and the list [1] are all truthy
    # and none of them is a person approving a spend.
    if raw_authorised is not True:
        refusals.append(f"authorised is {raw_authorised!r}, not the boolean true")

    tranche_id = data.get("tranche_id")
    if tranche_id != TRANCHE_ID:
        refusals.append(f"tranche_id is {tranche_id!r}, expected {TRANCHE_ID!r}")

    try:
        ceiling = Decimal(str(raw_ceiling))
    except Exception:
        ceiling = Decimal("0")
        refusals.append(f"max_consumed_api_spend_usd {raw_ceiling!r} is not a number")
    else:
        if ceiling <= 0:
            refusals.append(f"max_consumed_api_spend_usd is {ceiling}, which authorises nothing")
        elif ceiling > MAX_PROPOSED_CEILING_USD:
            refusals.append(
                f"max_consumed_api_spend_usd {ceiling} exceeds the proposed EMP-001 ceiling "
                f"{MAX_PROPOSED_CEILING_USD}; raising it is a separate Controller/user decision")

    if raw_retries != RETRIES_AUTHORISED:
        refusals.append(
            f"retries_authorised is {raw_retries!r}; EMP-001 authorises exactly "
            f"{RETRIES_AUTHORISED}. One provider call is one trial, even when it refuses.")

    return Authorisation(
        authorised=raw_authorised is True,
        tranche_id=tranche_id,
        max_consumed_api_spend_usd=ceiling,
        retries_authorised=raw_retries if isinstance(raw_retries, int) else 0,
        approved_by=data.get("approved_by"),
        approved_at=data.get("approved_at"),
        source_path=str(path),
        refusals=tuple(refusals),
    )


def open_guard(path: Path | str = AUTHORISATION_LOCAL_PATH) -> BudgetGuard:
    """Return a live BudgetGuard, or raise NotAuthorised with every reason it refused.

    This is the ONLY supported way for a runner to obtain a guard for paid execution.
    """
    auth = load_authorisation(path)
    if auth.refusals:
        raise NotAuthorised(
            f"EMP-001 paid execution is not authorised ({auth.source_path}):\n  - "
            + "\n  - ".join(auth.refusals))
    return BudgetGuard(authorised_usd=auth.max_consumed_api_spend_usd)


def authorisation_status(path: Path | str = AUTHORISATION_LOCAL_PATH) -> dict:
    """Machine-readable status for the preflight record. Makes no call and opens no guard."""
    auth = load_authorisation(path)
    return {
        "path": auth.source_path,
        "file_exists": Path(auth.source_path).exists(),
        "authorised": auth.authorised,
        "tranche_id": auth.tranche_id,
        "max_consumed_api_spend_usd": str(auth.max_consumed_api_spend_usd),
        "retries_authorised": auth.retries_authorised,
        "refusals": list(auth.refusals),
        "paid_execution_permitted": not auth.refusals,
    }
