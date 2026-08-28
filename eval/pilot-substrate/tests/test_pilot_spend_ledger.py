"""Persistent PILOT-001 spend: durable reservations, restart continuity, fail-closed reads.

The lesson under test is EMP-001's, applied to the pilot: a tranche ceiling is a property
of the TRANCHE, so spend history must live on disk against a run id — not in a Python
object. Restart continuity is proven with a REAL second process (subprocess), never with
two references to the same in-memory object.
"""
import json
import socket
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest

import pilot_spend_ledger as SL
from budget_guard import BudgetExceeded, NotAuthorised
from conftest import FakeGeminiTransport, make_pilot_authority
from video_route import GeminiVeoRoute


def runtime(tmp_path, run_id="run-1", cap="5.00"):
    local, decisions = make_pilot_authority(tmp_path, cap=cap)
    return SL.open_pilot_runtime(tmp_path / "runs", run_id,
                                 authorisation_path=local, decisions_dir=decisions)


# ------------------------------------------------------------------ reserve / settle
def test_reservation_is_persisted_to_disk_before_any_dispatch(tmp_path):
    budget = runtime(tmp_path)
    budget.reserve(Decimal("0.80"))
    lines = [json.loads(x) for x in
             budget.run.ledger_path.read_text().splitlines()]
    assert len(lines) == 1
    assert lines[0]["type"] == "reservation"
    assert lines[0]["amount_usd"] == "0.80"
    assert lines[0]["cost_ref"].startswith("pilot-cost-res-")


def test_pending_reservation_counts_against_the_cap(tmp_path):
    budget = runtime(tmp_path, cap="1.00")
    budget.reserve(Decimal("0.80"))            # pending, not settled
    fresh = SL.PilotBudget(SL.PilotRun.open(tmp_path / "runs", "run-1"))
    with pytest.raises(BudgetExceeded, match="pending"):
        fresh.reserve(Decimal("0.40"))         # 0.80 pending + 0.40 > 1.00


def test_committed_plus_pending_cannot_exceed_cap(tmp_path):
    budget = runtime(tmp_path, cap="2.00")
    budget.reserve(Decimal("0.80"))
    budget.record(Decimal("0.80"))             # committed 0.80
    budget.reserve(Decimal("0.80"))            # pending 0.80
    with pytest.raises(BudgetExceeded):
        budget.reserve(Decimal("0.80"))        # 0.80 + 0.80 + 0.80 > 2.00


def test_same_cost_ref_survives_reservation_to_settlement(tmp_path):
    budget = runtime(tmp_path)
    budget.reserve(Decimal("0.80"))
    ref_at_reserve = budget.cost_ref
    settled_ref = budget.record(Decimal("0.80"))
    assert settled_ref == ref_at_reserve       # one stable identity, start to finish
    rows = [json.loads(x) for x in budget.run.ledger_path.read_text().splitlines()]
    assert [r["type"] for r in rows] == ["reservation", "spend"]
    assert rows[0]["cost_ref"] == rows[1]["cost_ref"] == settled_ref
    assert rows[0]["reservation_id"] == rows[1]["reservation_id"]


def test_release_restores_only_its_own_reservation(tmp_path):
    budget = runtime(tmp_path)
    budget.reserve(Decimal("0.80"))
    budget.record(Decimal("0.80"))             # settled: stays counted forever
    budget.reserve(Decimal("0.40"))
    budget.release()                           # provably pre-dispatch: given back
    assert budget.committed_usd() == Decimal("0.80")
    assert budget.pending_usd() == Decimal("0")
    assert budget.remaining_usd() == Decimal("4.20")
    rows = [json.loads(x) for x in budget.run.ledger_path.read_text().splitlines()]
    assert rows[-1]["type"] == "release"
    assert rows[-1]["reservation_id"] == rows[-2]["reservation_id"]


# --------------------------------------------------------------- restart continuity
def _reopen_in_subprocess(tmp_path, run_id="run-1"):
    """Open the SAME run from a genuinely fresh process and report what it sees."""
    local = tmp_path / "authorization.pilot.local.yaml"
    decisions = tmp_path / "decisions"
    script = (
        "import json, sys\n"
        f"sys.path.insert(0, {str(Path(__file__).resolve().parent.parent)!r})\n"
        "import pilot_spend_ledger as SL\n"
        f"b = SL.open_pilot_runtime({str(tmp_path / 'runs')!r}, {run_id!r},\n"
        f"                          authorisation_path={str(local)!r},\n"
        f"                          decisions_dir=__import__('pathlib').Path({str(decisions)!r}))\n"
        "print(json.dumps({'committed': str(b.committed_usd()),\n"
        "                  'pending': str(b.pending_usd()),\n"
        "                  'spent': str(b.spent_usd),\n"
        "                  'remaining': str(b.remaining_usd())}))\n")
    proc = subprocess.run([sys.executable, "-c", script],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout.strip().splitlines()[-1])


def test_settled_spend_survives_a_real_process_restart(tmp_path):
    budget = runtime(tmp_path)
    budget.reserve(Decimal("0.80"))
    budget.record(Decimal("0.80"))
    seen = _reopen_in_subprocess(tmp_path)
    assert seen == {"committed": "0.80", "pending": "0",
                    "spent": "0.80", "remaining": "4.20"}   # NOT reset to zero


def test_pending_reservation_visible_to_a_second_process(tmp_path):
    budget = runtime(tmp_path)
    budget.reserve(Decimal("0.80"))            # left pending, as after a crash mid-call
    seen = _reopen_in_subprocess(tmp_path)
    assert seen["pending"] == "0.80"
    assert seen["spent"] == "0.80"             # pending counts, deliberately
    assert seen["remaining"] == "4.20"


# --------------------------------------------------- ambiguity via the actual route
def test_ambiguous_dispatch_settles_conservatively_and_keeps_headroom_consumed(
        tmp_path, gemini_key):
    budget = runtime(tmp_path)
    transport = FakeGeminiTransport(submit=socket.timeout("read timed out"))
    route = GeminiVeoRoute(transport=transport, guard=budget)
    outcome = route.generate("p", 8, "9:16", tmp_path / "out")
    assert outcome["attempt"]["billing_state"] == "unknown_provisional"
    assert outcome["attempt"]["cost_ref"]                     # durable, non-null
    assert budget.committed_usd() == Decimal("0.80")          # settled, not released
    assert budget.remaining_usd() == Decimal("4.20")
    # and a fresh process sees the same consumed headroom
    assert _reopen_in_subprocess(tmp_path)["committed"] == "0.80"


def test_route_success_yields_stable_nonnull_cost_ref_from_persistent_ledger(
        tmp_path, gemini_key):
    budget = runtime(tmp_path)
    route = GeminiVeoRoute(transport=FakeGeminiTransport(), guard=budget)
    outcome = route.generate("p", 8, "9:16", tmp_path / "out")
    ref = outcome["attempt"]["cost_ref"]
    assert ref and ref.startswith("pilot-cost-res-")
    assert outcome["cost_record"]["ledger_entry_id"] == ref
    rows = [json.loads(x) for x in budget.run.ledger_path.read_text().splitlines()]
    assert {r["cost_ref"] for r in rows} == {ref}


def test_predispatch_refusal_releases_the_persisted_reservation(tmp_path):
    # No GEMINI_API_KEY in the environment (conftest strips it).
    budget = runtime(tmp_path)
    route = GeminiVeoRoute(transport=FakeGeminiTransport(), guard=budget)
    from providers import PreDispatchRefusal

    with pytest.raises(PreDispatchRefusal):
        route.generate("p", 8, "9:16", tmp_path / "out")
    assert budget.pending_usd() == Decimal("0")
    assert budget.remaining_usd() == Decimal("5.00")
    types = [json.loads(x)["type"] for x in
             budget.run.ledger_path.read_text().splitlines()]
    assert types == ["reservation", "release"]   # history kept, additively


# ------------------------------------------------------------------- fail closed
def test_malformed_ledger_line_fails_closed(tmp_path):
    budget = runtime(tmp_path)
    budget.reserve(Decimal("0.80"))
    budget.record(Decimal("0.80"))
    with budget.run.ledger_path.open("a") as fh:
        fh.write("this is not json\n")
    fresh = SL.PilotBudget(SL.PilotRun.open(tmp_path / "runs", "run-1"))
    with pytest.raises(SL.LedgerCorrupt, match="not valid JSON"):
        fresh.spent_usd


def test_sequence_gap_fails_closed(tmp_path):
    budget = runtime(tmp_path)
    for _ in range(3):
        budget.reserve(Decimal("0.10"))
        budget.record(Decimal("0.10"))
    lines = budget.run.ledger_path.read_text().splitlines()
    budget.run.ledger_path.write_text("\n".join(lines[:2] + lines[3:]) + "\n")
    fresh = SL.PilotBudget(SL.PilotRun.open(tmp_path / "runs", "run-1"))
    with pytest.raises(SL.LedgerCorrupt, match="expected seq"):
        fresh.spent_usd


def test_in_process_truncation_fails_closed(tmp_path):
    budget = runtime(tmp_path)
    budget.reserve(Decimal("0.80"))
    budget.record(Decimal("0.80"))
    assert budget.spent_usd == Decimal("0.80")     # parse and cache
    lines = budget.run.ledger_path.read_text().splitlines()
    budget.run.ledger_path.write_text(lines[0] + "\n")   # history rewritten shorter
    with pytest.raises(SL.LedgerCorrupt, match="shrank"):
        budget.spent_usd


def test_unknown_record_type_fails_closed(tmp_path):
    budget = runtime(tmp_path)
    with budget.run.ledger_path.open("a") as fh:
        fh.write(json.dumps({"seq": 1, "type": "adjustment",
                             "amount_usd": "9.99"}) + "\n")
    fresh = SL.PilotBudget(SL.PilotRun.open(tmp_path / "runs", "run-1"))
    with pytest.raises(SL.LedgerCorrupt, match="unknown record type"):
        fresh.spent_usd


def test_missing_run_record_fails_closed(tmp_path):
    with pytest.raises(SL.LedgerCorrupt, match="no run record"):
        SL.PilotRun.open(tmp_path / "runs", "never-created")


def test_ceiling_drift_between_run_and_authority_fails_closed(tmp_path):
    runtime(tmp_path, cap="5.00")                  # creates run at 5.00
    local, decisions = make_pilot_authority(tmp_path, cap="3.00")   # authority now 3.00
    with pytest.raises(SL.LedgerCorrupt, match="ceiling"):
        SL.open_pilot_runtime(tmp_path / "runs", "run-1",
                              authorisation_path=local, decisions_dir=decisions)


# ------------------------------------------------------------- authority still gates
def test_current_repository_state_cannot_open_a_live_runtime(tmp_path):
    """The decisive gate: even a perfect local file cannot open the persistent runtime
    against the REAL decisions directory, because no committed authorising decision
    exists. A local YAML alone manufactures nothing."""
    local, _ = make_pilot_authority(tmp_path)
    with pytest.raises(NotAuthorised):
        SL.open_pilot_runtime(tmp_path / "runs", "run-x", authorisation_path=local)
    assert not (tmp_path / "runs" / "run-x").exists()     # nothing was even created


def test_no_local_file_cannot_open_a_live_runtime(tmp_path):
    with pytest.raises(NotAuthorised):
        SL.open_pilot_runtime(tmp_path / "runs", "run-x",
                              authorisation_path=tmp_path / "absent.yaml")
