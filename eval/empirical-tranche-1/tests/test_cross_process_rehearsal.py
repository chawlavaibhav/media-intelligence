"""Cross-process EMP-001 lifecycle rehearsal (EVAL-014 E).

This is the control the whole task exists for. The budget defect was invisible to a suite that ran
everything in one process — there never WAS a second process for spend to fail to survive.

So this spawns real interpreters via `rehearse_cross_process`. Qualification runs and exits; its
memory is gone. A-TEXT is a fresh process that knows only what is on disk.
"""
import json
from decimal import Decimal
from pathlib import Path

import pytest

import rehearse_cross_process as RH
import spend_ledger as SL

PKG = Path(__file__).resolve().parents[1]
REGISTRY = PKG.parents[1] / 'eval' / 'registry' / 'registry-v1.jsonl'


@pytest.fixture(scope='module')
def rehearsal(tmp_path_factory):
    """One full lifecycle, shared by the assertions below. Spawns real subprocesses."""
    work = tmp_path_factory.mktemp('rehearsal')
    registry_before = REGISTRY.read_bytes()
    findings = RH.rehearse(work)
    return findings, work, registry_before


def test_the_whole_lifecycle_passes(rehearsal):
    findings, _, _ = rehearsal
    assert findings['all_passed'] is True, findings['checks']


def test_spend_survived_the_process_boundary(rehearsal):
    """The defect, stated as a test: a second process must not see a fresh USD 10."""
    findings, _, _ = rehearsal
    assert findings['checks']['spend_survived_process_boundary'] is True
    assert findings['checks']['cumulative_spend_did_not_reset'] is True
    assert Decimal(findings['totals']['qualification_usd']) > 0
    assert Decimal(findings['totals']['atex_usd']) > 0
    assert (Decimal(findings['totals']['total_usd'])
            == Decimal(findings['totals']['qualification_usd'])
            + Decimal(findings['totals']['atex_usd']))


def test_both_ceilings_held(rehearsal):
    findings, _, _ = rehearsal
    assert Decimal(findings['totals']['total_usd']) <= Decimal('10.00')
    assert Decimal(findings['totals']['qualification_usd']) <= Decimal('6.00')
    assert findings['checks']['total_within_10'] is True
    assert findings['checks']['qualification_within_6'] is True


def test_the_perceptibility_gate_actually_blocked_a_process(rehearsal):
    """Step 6 ran A-TEXT with the committed, unfilled sheet. It must have refused."""
    findings, _, _ = rehearsal
    assert findings['checks']['atex_blocked_by_perceptibility_gate'] is True


def test_the_frozen_atex_shape_held(rehearsal):
    findings, _, _ = rehearsal
    assert findings['checks']['generations_sixteen'] is True
    assert findings['checks']['per_route_eight_each'] is True
    assert findings['checks']['retries_zero'] is True


def test_every_trial_and_cost_reference_is_unique(rehearsal):
    findings, _, _ = rehearsal
    assert findings['checks']['cost_refs_unique'] is True
    assert findings['checks']['trial_ids_unique'] is True
    assert findings['checks']['generation_and_evaluator_costed_separately'] is True
    # 2,304 qualification dispatches + 16 generations + 16 evaluator calls.
    assert findings['spend_records'] == 2336


def test_the_registry_was_not_touched_by_the_whole_lifecycle(rehearsal):
    _, _, registry_before = rehearsal
    assert REGISTRY.read_bytes() == registry_before


def test_fake_live_evidence_remains_non_promotable(rehearsal):
    findings, work, _ = rehearsal
    assert findings['checks']['not_promotable'] is True
    atex = json.loads((work / 'atex.json').read_text())
    assert atex['may_populate_registry'] is False
    assert atex['registry_rows_written'] == 0
    assert atex['evidence_class'] == 'partial_admission_screen_only'


def test_the_rehearsal_made_no_external_call_and_spent_nothing(rehearsal):
    findings, _, _ = rehearsal
    assert findings['external_calls'] == 0
    assert findings['spend_usd'] == '0'


def test_the_rehearsal_preserves_the_completed_committed_human_review(rehearsal):
    import human_review as HR

    committed = PKG / 'text_qualification' / 'perceptibility-review.csv'
    status = HR.review_status(committed)
    assert status['ok'] is True
    assert status['usable_yes'] == 96
    assert status['mismatch_visible_yes'] == 48
    assert status['bound_rows'] == 96


def test_a_reopened_ledger_reports_the_same_totals(rehearsal):
    """Reconstructed from disk a second time, by yet another reader."""
    findings, work, _ = rehearsal
    budget = SL.TrancheBudget(SL.TrancheRun.open(work / 'runs', 'rehearsal-run'))
    assert str(budget.spent_usd()) == findings['totals']['total_usd']
    assert str(budget.stage_spent_usd('qualification')) == findings['totals']['qualification_usd']
    assert str(budget.stage_spent_usd('atex')) == findings['totals']['atex_usd']
