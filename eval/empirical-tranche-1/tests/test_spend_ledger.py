"""Persistent cumulative tranche budget controls (EVAL-014 A).

The defect this closes: `BudgetGuard.spent_usd` lived in memory. Qualification could spend most of
the tranche, exit, and A-TEXT could reopen the SAME authorisation file with `spent_usd = 0`. The
USD 10 ceiling was a per-process ceiling wearing a tranche ceiling's clothes, and nothing in the
suite noticed because every test ran in one process.

So every control here is about what survives a process boundary, and the caps are asserted against
a ledger reconstructed from disk rather than against an object that was never closed.
"""
import json
import os
from decimal import Decimal
from pathlib import Path

import pytest

import spend_ledger as SL
from budget_guard import BudgetExceeded

TOTAL = Decimal('10.00')
QUAL_CAP = Decimal('6.00')


def _auth(tmp_path, name='authorization.local.yaml'):
    p = tmp_path / name
    p.write_text("authorised: true\ntranche_id: EMP-001\n"
                 "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    return p


def _run(tmp_path, run_id='run-0001'):
    return SL.TrancheRun.create(root=tmp_path / 'runs', run_id=run_id,
                                authorisation_path=_auth(tmp_path))


# ------------------------------------------------------------------ frozen constants
def test_the_frozen_ceilings_are_what_the_controller_froze():
    assert SL.TOTAL_CEILING_USD == Decimal('10.00')
    assert SL.STAGE_CAPS['qualification'] == Decimal('6.00')
    assert SL.STAGE_CAPS['atex'] is None          # remaining headroom only
    assert SL.RETRIES_AUTHORISED == 0


# ------------------------------------------------------------------ persistence
def test_a_new_run_starts_at_zero(tmp_path):
    b = SL.TrancheBudget(_run(tmp_path))
    assert b.spent_usd() == Decimal('0')
    assert b.remaining_usd() == TOTAL


def test_spend_survives_closing_and_reopening_the_run(tmp_path):
    """CONTROL 1. Process A spends 5.75 and exits; process B must see 4.25, not 10."""
    run = _run(tmp_path)
    a = SL.TrancheBudget(run).stage('qualification')
    a.reserve(Decimal('5.75'))
    a.record(Decimal('5.75'))
    del a, run

    reopened = SL.TrancheBudget(SL.TrancheRun.open(root=tmp_path / 'runs', run_id='run-0001'))
    assert reopened.spent_usd() == Decimal('5.75')
    assert reopened.remaining_usd() == Decimal('4.25')


def test_reopening_cannot_reset_spend_by_constructing_a_fresh_budget(tmp_path):
    run = _run(tmp_path)
    s = SL.TrancheBudget(run).stage('qualification')
    s.reserve(Decimal('3.00'))
    s.record(Decimal('3.00'))

    for _ in range(3):
        again = SL.TrancheBudget(SL.TrancheRun.open(root=tmp_path / 'runs', run_id='run-0001'))
        assert again.spent_usd() == Decimal('3.00')


def test_deleting_the_authorisation_file_does_not_erase_spend(tmp_path):
    """CONTROL 4. Spend is a property of the RUN, not of the file that authorised it."""
    auth = _auth(tmp_path)
    run = SL.TrancheRun.create(root=tmp_path / 'runs', run_id='run-0001',
                               authorisation_path=auth)
    s = SL.TrancheBudget(run).stage('qualification')
    s.reserve(Decimal('4.00'))
    s.record(Decimal('4.00'))

    auth.unlink()
    _auth(tmp_path)          # a brand new authorisation file, same tranche and run

    reopened = SL.TrancheBudget(SL.TrancheRun.open(root=tmp_path / 'runs', run_id='run-0001'))
    assert reopened.spent_usd() == Decimal('4.00')
    assert reopened.remaining_usd() == Decimal('6.00')


def test_the_ledger_is_append_only_and_never_rewritten(tmp_path):
    run = _run(tmp_path)
    s = SL.TrancheBudget(run).stage('qualification')
    for _ in range(5):
        s.reserve(Decimal('0.10'))
        s.record(Decimal('0.10'))
    lines = run.ledger_path.read_text().strip().split('\n')
    assert len(lines) == 10                       # 5 reservations + 5 spends
    assert [json.loads(x)['seq'] for x in lines] == list(range(1, 11))


# ------------------------------------------------------------------ the caps
def test_qualification_is_refused_at_its_six_dollar_sub_cap(tmp_path):
    """CONTROL 2. Total headroom remains, and the stage cap still refuses."""
    run = _run(tmp_path)
    s = SL.TrancheBudget(run).stage('qualification')
    s.reserve(Decimal('5.99'))
    s.record(Decimal('5.99'))

    assert SL.TrancheBudget(run).remaining_usd() == Decimal('4.01')   # tranche has room
    with pytest.raises(BudgetExceeded) as e:
        s.reserve(Decimal('0.02'))                                    # the STAGE does not
    assert '6' in str(e.value)


def test_the_qualification_cap_holds_even_when_the_authorisation_says_ten(tmp_path):
    run = _run(tmp_path)                       # authorisation file says 10.00
    s = SL.TrancheBudget(run).stage('qualification')
    with pytest.raises(BudgetExceeded):
        s.reserve(Decimal('6.01'))


def test_atex_is_refused_when_it_would_break_the_ten_dollar_total(tmp_path):
    """CONTROL 3."""
    run = _run(tmp_path)
    q = SL.TrancheBudget(run).stage('qualification')
    q.reserve(Decimal('6.00'))
    q.record(Decimal('6.00'))

    a = SL.TrancheBudget(SL.TrancheRun.open(root=tmp_path / 'runs',
                                            run_id='run-0001')).stage('atex')
    a.reserve(Decimal('4.00'))                 # exactly the remaining headroom is fine
    a.record(Decimal('4.00'))
    with pytest.raises(BudgetExceeded):
        a.reserve(Decimal('0.01'))


def test_atex_receives_only_the_headroom_qualification_left(tmp_path):
    run = _run(tmp_path)
    q = SL.TrancheBudget(run).stage('qualification')
    q.reserve(Decimal('5.50'))
    q.record(Decimal('5.50'))
    a = SL.TrancheBudget(run).stage('atex')
    assert a.remaining_usd() == Decimal('4.50')


def test_the_total_ceiling_is_absolute_across_stages(tmp_path):
    run = _run(tmp_path)
    q = SL.TrancheBudget(run).stage('qualification')
    q.reserve(Decimal('6.00')); q.record(Decimal('6.00'))
    a = SL.TrancheBudget(run).stage('atex')
    a.reserve(Decimal('4.00')); a.record(Decimal('4.00'))
    assert SL.TrancheBudget(run).spent_usd() == TOTAL
    with pytest.raises(BudgetExceeded):
        SL.TrancheBudget(run).stage('atex').reserve(Decimal('0.01'))


# ------------------------------------------------------------------ concurrency
def test_an_outstanding_reservation_blocks_a_second_writer(tmp_path):
    """CONTROL 5. Two processes must not reserve the same remaining headroom."""
    run = _run(tmp_path)
    a = SL.TrancheBudget(run).stage('qualification')
    a.reserve(Decimal('6.00'))               # reserved, not yet settled

    b = SL.TrancheBudget(SL.TrancheRun.open(root=tmp_path / 'runs',
                                            run_id='run-0001')).stage('qualification')
    with pytest.raises(BudgetExceeded):
        b.reserve(Decimal('0.50'))           # the pending reservation already counts


def test_a_released_reservation_returns_its_headroom(tmp_path):
    """A dispatch that never happened must not permanently burn budget."""
    run = _run(tmp_path)
    s = SL.TrancheBudget(run).stage('qualification')
    s.reserve(Decimal('5.00'))
    s.release()
    assert SL.TrancheBudget(run).spent_usd() == Decimal('0')
    s.reserve(Decimal('5.00'))               # available again


def test_pending_reservations_count_toward_spend_until_settled(tmp_path):
    run = _run(tmp_path)
    s = SL.TrancheBudget(run).stage('qualification')
    s.reserve(Decimal('2.00'))
    b = SL.TrancheBudget(run)
    assert b.pending_usd() == Decimal('2.00')
    assert b.committed_usd() == Decimal('0')
    assert b.spent_usd() == Decimal('2.00')


def test_the_lock_is_held_per_run_and_serialises_writers(tmp_path):
    run = _run(tmp_path)
    b = SL.TrancheBudget(run)
    with b._locked():
        assert run.lock_path.exists()


# ------------------------------------------------------------------ corrections
def test_a_negative_correction_cannot_manufacture_headroom(tmp_path):
    run = _run(tmp_path)
    s = SL.TrancheBudget(run).stage('qualification')
    s.reserve(Decimal('5.00')); s.record(Decimal('5.00'))
    with pytest.raises(ValueError):
        SL.TrancheBudget(run).correct(stage='qualification', amount_usd=Decimal('-2.00'),
                                      reason='wishful thinking')
    assert SL.TrancheBudget(run).spent_usd() == Decimal('5.00')


def test_a_correction_is_an_additive_record_with_an_explicit_type(tmp_path):
    run = _run(tmp_path)
    SL.TrancheBudget(run).correct(stage='qualification', amount_usd=Decimal('0.25'),
                                  reason='invoice reconciliation')
    rows = [json.loads(x) for x in run.ledger_path.read_text().strip().split('\n')]
    assert rows[-1]['type'] == 'correction'
    assert rows[-1]['reason'] == 'invoice reconciliation'
    assert SL.TrancheBudget(run).spent_usd() == Decimal('0.25')


def test_a_correction_cannot_break_the_total_ceiling(tmp_path):
    run = _run(tmp_path)
    s = SL.TrancheBudget(run).stage('qualification')
    s.reserve(Decimal('6.00')); s.record(Decimal('6.00'))
    with pytest.raises(BudgetExceeded):
        SL.TrancheBudget(run).correct(stage='atex', amount_usd=Decimal('5.00'),
                                      reason='late invoice')


# ------------------------------------------------------------------ fail closed
def test_a_corrupt_ledger_line_fails_closed(tmp_path):
    """CONTROL 6."""
    run = _run(tmp_path)
    s = SL.TrancheBudget(run).stage('qualification')
    s.reserve(Decimal('1.00')); s.record(Decimal('1.00'))
    with run.ledger_path.open('a') as fh:
        fh.write('{not json at all\n')
    with pytest.raises(SL.LedgerCorrupt):
        SL.TrancheBudget(run).spent_usd()


def test_a_ledger_with_a_missing_amount_fails_closed(tmp_path):
    run = _run(tmp_path)
    with run.ledger_path.open('a') as fh:
        fh.write(json.dumps({'seq': 1, 'type': 'spend', 'stage': 'qualification'}) + '\n')
    with pytest.raises(SL.LedgerCorrupt):
        SL.TrancheBudget(run).spent_usd()


def test_a_ledger_with_a_sequence_gap_fails_closed(tmp_path):
    """A gap means a record was lost. Guessing what it was is how a ceiling springs a leak."""
    run = _run(tmp_path)
    with run.ledger_path.open('a') as fh:
        fh.write(json.dumps({'seq': 7, 'type': 'spend', 'stage': 'qualification',
                             'amount_usd': '1.00', 'cost_ref': 'c'}) + '\n')
    with pytest.raises(SL.LedgerCorrupt):
        SL.TrancheBudget(run).spent_usd()


def test_an_unknown_record_type_fails_closed(tmp_path):
    run = _run(tmp_path)
    with run.ledger_path.open('a') as fh:
        fh.write(json.dumps({'seq': 1, 'type': 'refund', 'stage': 'qualification',
                             'amount_usd': '5.00'}) + '\n')
    with pytest.raises(SL.LedgerCorrupt):
        SL.TrancheBudget(run).spent_usd()


def test_a_missing_run_record_fails_closed(tmp_path):
    run = _run(tmp_path)
    run.run_json_path.unlink()
    with pytest.raises(SL.LedgerCorrupt):
        SL.TrancheRun.open(root=tmp_path / 'runs', run_id='run-0001')


def test_an_unknown_stage_is_refused(tmp_path):
    with pytest.raises(ValueError):
        SL.TrancheBudget(_run(tmp_path)).stage('some-other-stage')


def test_float_amounts_are_refused(tmp_path):
    s = SL.TrancheBudget(_run(tmp_path)).stage('qualification')
    with pytest.raises(TypeError):
        s.reserve(0.10)


# ------------------------------------------------------------------ gitignored
def test_the_runtime_run_root_is_gitignored():
    root = Path(__file__).resolve().parents[3]
    assert 'eval/runs/' in (root / '.gitignore').read_text()
