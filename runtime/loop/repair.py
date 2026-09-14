"""Bounded repair: what failed, what changes, what stays the same — or a refusal by name.

WHY THIS SHAPE. OUTCOME-EVENT-v0 says it plainly: "'Try again' is not a repair and must be rejected
by the schema check." A RepairRequest therefore cannot exist without `what_changes` and
`what_stays_invariant`, and both are derived from the failure's category, never typed by a caller.
A failure the table does not recognise is a refusal (REPAIR_FAILURE_UNRECOGNISED), not a generic
retry; a human rejection that names no failed contract line is a refusal (REPAIR_NOT_A_REPAIR).

THE BOUND. `repair_allowance` is read from the policy profile row (`profile.limit`), never a
constant. Repairs proposed so far = attempts_so_far - 1 (the first attempt is not a repair). The
(repair_allowance + 1)th repair raises RepairAllowanceExhausted, a Refusal carrying the count; the
caller records it and stops — nothing here retries.

COST. `incremental_cost_usd` is the expected cost of one more draw, PASSED IN by the caller (lane
F's manifest prices attempts); this module never reads a price or a pin.

FALLBACK. When the caller supplies the manifest's fallback_triggers and a fallback route, a failing
check id that matches a trigger makes `route_changed` True and names the route in what_changes;
"route" then leaves what_stays_invariant. Otherwise the route is invariant.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from runtime.errors import Refusal
from runtime.loop import refusals
from runtime.loop.refusals import RepairAllowanceExhausted
from runtime.util import sha256_obj

INVARIANT_WITH_ROUTE = "acceptance contract, route, exact strings, aspect"
INVARIANT_ROUTE_CHANGED = "acceptance contract, exact strings, aspect"

# check-id prefix -> (category, what_changes). Order is precedence when several ids fail.
GATE_CATEGORIES = (
    ("LIMIT-TEXT", "baked_lettering",
     "re-draw the plate; the plate prompt's no-lettering instruction is repeated verbatim and the "
     "draw seed is not held"),
    ("DISPATCH-", "delivered_vs_declared",
     "re-draw with the dispatch parameters re-derived from the spec's declared aspect and duration; "
     "the artifact must probe to what was declared"),
    ("INFRA-", "artifact_container",
     "re-draw; the returned container must probe as a complete file of the dispatched kind"),
    ("RUNTIME-PLATE-NO-LETTERING-INSTRUCTION", "plate_prompt_missing_instruction",
     "the planner supplies a plate prompt that carries an explicit no-lettering instruction; the "
     "runtime adds no words to a prompt"),
)


def _money(value) -> str:
    try:
        return format(Decimal(str(value)), "f")
    except (InvalidOperation, ValueError):
        raise Refusal(refusals.REPAIR_NOT_A_REPAIR, "incremental_cost_usd must be a decimal amount",
                      got=repr(value)) from None


def _matches_trigger(check_id: str, trigger) -> bool:
    if isinstance(trigger, str):
        key = trigger
    elif isinstance(trigger, dict):
        key = trigger.get("check_id") or trigger.get("condition") or trigger.get("trigger") or ""
    else:
        return False
    key = str(key)
    return key == check_id or (key.endswith("*") and check_id.startswith(key[:-1]))


def _categorise_gate(failure: dict):
    ids = list(failure.get("blocking_failures") or [])
    if failure.get("verdict") != "FAIL" or not ids:
        raise Refusal(refusals.REPAIR_NOT_A_REPAIR,
                      "a gate outcome with no blocking failure names nothing to repair",
                      verdict=failure.get("verdict"), gate=failure.get("gate"))
    for prefix, category, what_changes in GATE_CATEGORIES:
        hit = [i for i in ids if i.startswith(prefix)]
        if hit:
            details = {r["check_id"]: r.get("detail", "") for r in failure.get("rows") or []}
            observed = "; ".join(f"{i}: {details.get(i, '')}".rstrip(": ") for i in ids)
            return category, what_changes, observed, ids
    raise Refusal(refusals.REPAIR_FAILURE_UNRECOGNISED,
                  "the failing check ids match no repair category; a repair the table cannot name "
                  "is not proposed (it would be 'try again')", failing=ids)


def _categorise_human(verdict: dict):
    decision = verdict.get("decision")
    if decision not in ("rejected", "repair_requested"):
        raise Refusal(refusals.REPAIR_NOT_A_REPAIR,
                      "only a human rejection or repair request can seed a repair", decision=decision)
    lines = [str(l) for l in (verdict.get("contract_lines_failed") or []) if str(l).strip()]
    if not lines:
        raise Refusal(refusals.REPAIR_NOT_A_REPAIR,
                      "the human decision names no failed acceptance-contract line, so nothing is "
                      "known to change — 'try again' is not a repair", decision=decision)
    quoted = "; ".join(f'"{l}"' for l in lines)
    what_changes = f"re-draw against the failed acceptance lines, which the next draw must satisfy: {quoted}"
    observed = f"human {decision} by {verdict.get('by')}: {verdict.get('note') or ''}".rstrip(": ")
    return "human_rejection", what_changes, observed, lines


def propose(failure: dict, spec: dict, profile, attempts_so_far: int, *, incremental_cost_usd,
            fallback_triggers=None, fallback_route=None) -> dict:
    allowance = int(profile.limit("repair_allowance"))
    proposed = max(0, int(attempts_so_far) - 1)
    if proposed >= allowance:
        raise RepairAllowanceExhausted(
            f"{proposed} repair(s) already proposed under profile {getattr(profile, 'name', '?')!r} "
            f"whose repair_allowance is {allowance}; the next repair would be number {proposed + 1} "
            f"and is refused — no retry is hidden here",
            repairs_proposed=proposed, repair_allowance=allowance, attempts_so_far=int(attempts_so_far))

    if "decision" in failure:
        source = "human"
        category, what_changes, observed, ids = _categorise_human(failure)
    elif "gate" in failure:
        source = "gate"
        category, what_changes, observed, ids = _categorise_gate(failure)
    else:
        raise Refusal(refusals.REPAIR_FAILURE_UNRECOGNISED,
                      "the failure is neither a GateOutcome nor a HumanVerdict", keys=sorted(failure))

    route_changed = False
    if fallback_route and fallback_triggers:
        matched = [i for i in ids for t in fallback_triggers if _matches_trigger(i, t)]
        if matched:
            route_changed = True
            what_changes += (f"; the route changes to the fallback {fallback_route} (manifest fallback "
                             f"trigger matched {', '.join(dict.fromkeys(matched))})")

    request = {
        "attempt_index": int(attempts_so_far) + 1,
        "source": source,
        "failure_observed": observed,
        "failure_category": category,
        "what_changes": what_changes,
        "what_stays_invariant": INVARIANT_ROUTE_CHANGED if route_changed else INVARIANT_WITH_ROUTE,
        "route_changed": route_changed,
        "fallback_route": fallback_route if route_changed else None,
        "incremental_cost_usd": _money(incremental_cost_usd),
        "failing_ids": ids,
    }
    request["repair_id"] = sha256_obj({"spec_id": spec.get("spec_id"), **{k: request[k] for k in (
        "attempt_index", "failure_category", "what_changes", "failure_observed")}})
    return request
