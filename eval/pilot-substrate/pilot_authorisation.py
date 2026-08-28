#!/usr/bin/env python3
"""EVAL-035: fail-closed spend authority for the future PILOT-001 tranche.

NO PILOT SPEND AUTHORITY EXISTS TODAY. CONTROL-STATE is explicit: PILOT-001 paid execution
waits for Controller review of the pre-pilot tasks, execution-time route verification, and
the user's explicit approval of a pilot spend cap. This module therefore refuses, always,
until a human materialises `authorization.pilot.local.yaml` (git-ignored) AFTER those gates
open.

The mechanical guard itself is EMP-001's `BudgetGuard`, imported unchanged — Decimal money,
reserve-before-dispatch, record-after, fail closed in every direction. What is new here is
only the PILOT-001 acceptance rule for the authorisation file:

    * `authorised` must be the boolean true (not "true", not 1);
    * `tranche_id` must be exactly "PILOT-001";
    * `max_consumed_api_spend_usd` must be a positive number;
    * `retries_authorised` must be exactly 0 — one provider call is one trial, always;
    * `approved_by` and `approved_at` must be present — an anonymous approval is not one;
    * `decision_ref` must name a Controller decision file that actually exists under
      coordination/decisions/. A ceiling with no decision behind it is a fabrication, and
      this check makes fabricating one require inventing a committed repository path too.

Existence of the referenced decision file is necessary, not sufficient: the runner at pilot
time must still verify the decision's content actually approves the named cap.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
EMP001 = HERE.parent / "empirical-tranche-1"
if str(EMP001) not in sys.path:
    sys.path.insert(0, str(EMP001))

from budget_guard import BudgetGuard, NotAuthorised  # noqa: E402

PILOT_TRANCHE_ID = "PILOT-001"
PILOT_AUTHORISATION_PATH = HERE / "authorization.pilot.local.yaml"
DECISIONS_DIR = REPO_ROOT / "coordination" / "decisions"
RETRIES_AUTHORISED = 0


def load_pilot_authorisation(path: Path | str = PILOT_AUTHORISATION_PATH) -> dict:
    """Read a pilot authorisation file and list every reason it would be refused.

    Never raises on a merely absent/disabled file — absence is the expected committed state.
    """
    import yaml

    path = Path(path)
    if not path.exists():
        return {"source_path": str(path), "authorised": False,
                "max_consumed_api_spend_usd": Decimal("0"),
                "refusals": ["no PILOT-001 authorisation file exists at that path — "
                             "PILOT-001 spend has not been approved"]}

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise NotAuthorised(f"{path}: authorisation file is not a mapping")

    refusals: list[str] = []

    if data.get("authorised") is not True:
        refusals.append(f"authorised is {data.get('authorised')!r}, not the boolean true")
    if data.get("tranche_id") != PILOT_TRANCHE_ID:
        refusals.append(f"tranche_id is {data.get('tranche_id')!r}, "
                        f"expected {PILOT_TRANCHE_ID!r}")

    try:
        ceiling = Decimal(str(data.get("max_consumed_api_spend_usd", 0)))
    except Exception:
        ceiling = Decimal("0")
        refusals.append(f"max_consumed_api_spend_usd "
                        f"{data.get('max_consumed_api_spend_usd')!r} is not a number")
    else:
        if ceiling <= 0:
            refusals.append(f"max_consumed_api_spend_usd is {ceiling}, "
                            f"which authorises nothing")

    if data.get("retries_authorised") != RETRIES_AUTHORISED:
        refusals.append(f"retries_authorised is {data.get('retries_authorised')!r}; "
                        f"PILOT-001 authorises exactly {RETRIES_AUTHORISED}. One provider "
                        f"call is one trial, even when it refuses.")

    for required in ("approved_by", "approved_at"):
        if not data.get(required):
            refusals.append(f"{required} is missing — an anonymous or undated approval "
                            f"is not an approval")

    decision_ref = data.get("decision_ref")
    if not decision_ref:
        refusals.append("decision_ref is missing — a spend cap must name the Controller "
                        "decision that approved it")
    else:
        decision_path = (REPO_ROOT / decision_ref if not Path(decision_ref).is_absolute()
                         else Path(decision_ref))
        try:
            inside = decision_path.resolve().is_relative_to(DECISIONS_DIR.resolve())
        except AttributeError:      # pragma: no cover — Python < 3.9 has no is_relative_to
            inside = str(decision_path.resolve()).startswith(str(DECISIONS_DIR.resolve()))
        if not inside:
            refusals.append(f"decision_ref {decision_ref!r} is not under "
                            f"coordination/decisions/")
        elif not decision_path.exists():
            refusals.append(f"decision_ref {decision_ref!r} names a decision file that "
                            f"does not exist in this repository")

    return {"source_path": str(path), "authorised": data.get("authorised") is True,
            "tranche_id": data.get("tranche_id"),
            "max_consumed_api_spend_usd": ceiling,
            "retries_authorised": data.get("retries_authorised"),
            "approved_by": data.get("approved_by"), "approved_at": data.get("approved_at"),
            "decision_ref": decision_ref, "refusals": refusals}


def open_pilot_guard(path: Path | str = PILOT_AUTHORISATION_PATH) -> BudgetGuard:
    """Return a live guard for PILOT-001, or raise NotAuthorised with every refusal reason.

    This is the ONLY supported way for a pilot runner to obtain a guard for paid dispatch.
    """
    auth = load_pilot_authorisation(path)
    if auth["refusals"]:
        raise NotAuthorised(
            f"PILOT-001 paid execution is not authorised ({auth['source_path']}):\n  - "
            + "\n  - ".join(auth["refusals"]))
    return BudgetGuard(authorised_usd=auth["max_consumed_api_spend_usd"])
