"""ledger_metrics -> latency_errors_refusals, cost_and_cpao: what the attempt records and the ledger say.

    latency  = completed_at - requested_at (seconds); p50 / p95 per cell by nearest rank
    status counts by status and by error_class; refusal rate = refusals / attempts
    trial cost = the settled `spend` ledger row for the attempt's reservation (never the estimate)
    CpAO      = always absent / not_applicable at Stage A (no accepted-outcome chain exists yet)
Verdict rules (proposed, PASS-CRITERIA-v0.yaml#ledger_metrics): latency_errors_refusals pass = status ok;
cost_and_cpao pass = settled <= reserved. An attempt with no settled row is a parse_failure, never a pass.
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from . import common as C
from . import metrics as MX

INSTRUMENT_ID = "ledger_metrics"
VERSION = "0.1.0"
CAPABILITIES = ("latency_errors_refusals", "cost_and_cpao")


def _ts(s) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None


def latency_s(attempt: dict) -> float | None:
    a, b = _ts(attempt.get("requested_at")), _ts(attempt.get("completed_at"))
    if a is None or b is None:
        return None
    return (b - a).total_seconds()


def settled_row(attempt: dict, ledger_rows: list) -> dict | None:
    rid = attempt.get("reservation_id")
    cref = attempt.get("cost_ref")
    for r in ledger_rows:
        if r.get("type") != "spend":
            continue
        if (rid and r.get("reservation_id") == rid) or (cref and r.get("cost_ref") == cref):
            return r
    return None


def cell_metrics(attempts: list, ledger_rows: list) -> dict:
    lats = [v for v in (latency_s(a) for a in attempts) if v is not None]
    status_counts: dict = {}
    err_counts: dict = {}
    for a in attempts:
        status_counts[a.get("status")] = status_counts.get(a.get("status"), 0) + 1
        if a.get("error_class"):
            err_counts[a["error_class"]] = err_counts.get(a["error_class"], 0) + 1
    settled = Decimal("0")
    n_settled = 0
    for a in attempts:
        r = settled_row(a, ledger_rows)
        if r is not None:
            try:
                settled += Decimal(str(r.get("amount_usd")))
                n_settled += 1
            except InvalidOperation:
                pass
    n = len(attempts)
    return {
        "n_attempts": n, "status_counts": status_counts, "error_class_counts": err_counts,
        "refusal_rate": (status_counts.get("refusal", 0) / n) if n else None,
        "error_rate": ((status_counts.get("error", 0) + status_counts.get("timeout", 0)) / n) if n else None,
        "latency_s": {"p50": MX.percentile_nearest_rank(lats, 0.5), "p95": MX.percentile_nearest_rank(lats, 0.95), "n": len(lats),
                      "method": "nearest_rank"},
        "settled_total_usd_equiv": str(settled.quantize(Decimal("0.000001"))), "n_settled": n_settled,
        "cpao": {"verdict": "absent", "absence_reason": "not_applicable", "note": "no accepted-outcome chain at Stage A"},
    }


def evaluate(attempt: dict, ledger_rows: list, capability: str, criteria_path: Path | str | None = None) -> dict:
    if capability not in CAPABILITIES:
        raise ValueError(f"{INSTRUMENT_ID} is not specified for capability {capability!r}")
    crit = C.criterion(INSTRUMENT_ID, criteria_path)
    if not isinstance(attempt, dict) or not attempt.get("status"):
        return C.parse_failure("attempt record has no status")
    row = settled_row(attempt, ledger_rows or [])
    if capability == "latency_errors_refusals":
        m = {"status": attempt.get("status"), "error_class": attempt.get("error_class"), "latency_s": latency_s(attempt),
             "requested_at": attempt.get("requested_at"), "completed_at": attempt.get("completed_at"),
             "billing_state": attempt.get("billing_state"), "ambiguous_dispatch": attempt.get("ambiguous_dispatch"),
             "settled_row_present": row is not None}
        ok = attempt.get("status") == "ok"
        return C.gate(crit, ok, m, [] if ok else [{"term": f"attempt status {attempt.get('status')} ({attempt.get('error_class')})"}])
    if row is None:
        return C.parse_failure("no settled spend row for this attempt in the ledger; a trial cost cannot be read from an estimate")
    try:
        settled = Decimal(str(row.get("amount_usd")))
        reserved = Decimal(str(attempt.get("reserved_amount_usd_equiv")))
    except (InvalidOperation, TypeError):
        return C.parse_failure("settled or reserved amount is not a decimal")
    m = {"settled_usd_equiv": str(settled.quantize(Decimal("0.000001"))), "reserved_usd_equiv": str(reserved.quantize(Decimal("0.000001"))),
         "cost_ref": row.get("cost_ref"), "billing_state": attempt.get("billing_state"),
         "cpao": {"verdict": "absent", "absence_reason": "not_applicable"}}
    ok = settled <= reserved
    return C.gate(crit, ok, m, [] if ok else [{"term": f"settled {settled} > reserved {reserved}"}])


def instrument(criteria_path: Path | str | None = None):
    def fn(path, item, capability):
        ins = C.inputs_of(item)
        if not ins.get("attempt"):
            return C.parse_failure("ledger metrics need instrument_inputs.attempt (the persisted attempt record) and .ledger_rows")
        return evaluate(ins["attempt"], ins.get("ledger_rows") or [], capability, criteria_path)
    return C.build_instrument(INSTRUMENT_ID, VERSION, CAPABILITIES, fn, criteria_path, observation_unit="trial")
