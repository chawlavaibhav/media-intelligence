"""GateOutcome: the loop's JSON-friendly view of a canon.gate Report (WAVE2-INTERFACES §4).

    {gate, verdict: PASS|FAIL|NOT_RUN, blocking_failures: [check_id], rows: [{check_id, family,
     status, blocking, detail}], report_sha256, packs_selected, report_text}

The rows are the gate's rows, verbatim status and detail; `report_sha256` is over the rendered
report text (the same text the gate CLI prints), so an event can point at the exact report. The
loop may APPEND rows of family "runtime" (for example RUNTIME-PLATE-NO-LETTERING-INSTRUCTION); it
never edits, drops or reinterprets a gate row.
"""
from __future__ import annotations

import hashlib

from canon.gate.findings import Report, Status

PASS, FAIL, NOT_RUN = "PASS", "FAIL", "NOT_RUN"


def runtime_row(check_id: str, status: str, detail: str, *, blocking: bool = True) -> dict:
    if status not in {s.value for s in Status}:
        raise ValueError(f"unknown gate status {status!r}")
    if status != Status.PASS.value and not detail.strip():
        raise ValueError(f"{check_id}: a {status} row needs a reason")
    return {"check_id": check_id, "family": "runtime", "status": status, "blocking": blocking,
            "detail": detail}


def _row_failing(row: dict) -> bool:
    return row["status"] == Status.ERROR.value or (row["status"] == Status.FAIL.value and row["blocking"])


def _render_extra(rows) -> str:
    return "\n".join(f"{r['status']:<16}{r['check_id']:<16}{r['detail']}" for r in rows)


def from_report(report: Report, extra_rows=()) -> dict:
    rows = [{"check_id": r.check_id, "family": r.family, "status": r.status.value,
             "blocking": r.blocking, "detail": r.detail} for r in report.results]
    rows += list(extra_rows)
    blocking = [r["check_id"] for r in rows if _row_failing(r)]
    text = report.render_text()
    if extra_rows:
        text += "\nruntime\n" + _render_extra(extra_rows)
    return {
        "gate": report.gate,
        "verdict": FAIL if blocking else PASS,
        "blocking_failures": blocking,
        "rows": rows,
        "report_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "packs_selected": list(report.packs_selected),
        "report_text": text,
    }


def not_run(gate: str, check_ids, detail: str, *, packs_selected=()) -> dict:
    rows = [{"check_id": cid, "family": "runtime", "status": Status.NOT_RUN.value, "blocking": True,
             "detail": detail} for cid in check_ids]
    text = f"CANON GATE v0 — {gate} — NOT RUN — {detail}\n" + _render_extra(rows)
    return {"gate": gate, "verdict": NOT_RUN, "blocking_failures": [], "rows": rows,
            "report_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "packs_selected": list(packs_selected), "report_text": text}
