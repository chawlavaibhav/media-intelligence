"""Progressive text-qualification controls.

The expensive mistake this guards against is paying twice to learn the same thing. A candidate
that already false-passed on Devanagari must NOT go on to demonstrate that it also fails English —
that is another 576 calls for no new information. So the stop is tested by counting calls, not by
reading the code and believing it.

Every "call" here goes to a fake candidate. No provider is contacted.
"""
import json
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

import qualify_text as Q
from budget_guard import BudgetExceeded, BudgetGuard

PKG = Path(__file__).resolve().parents[1]
CONTRACT = PKG / 'text_qualification' / 'qualification-contract-v2.yaml'

# 96 items x 2 shapes x 3 passes
CALLS_PER_SCRIPT = 576


# --------------------------------------------------------------- the frozen contract
def test_contract_thresholds_are_frozen():
    c = yaml.safe_load(CONTRACT.read_text(encoding='utf-8'))
    assert c['repeats_per_shape'] == 3
    assert c['mismatch_false_pass_max'] == 0
    assert c['match_false_fail_rate_max'] == 0.10
    assert c['refusal_rate_max'] == 0.05
    assert c['repeat_consistency_min'] == 0.95
    assert c['primary_generated_output_shape'] == 'transcribe'
    assert c['contract_version'] == 2
    assert c['gate_scope']['qualifying_shape'] == 'transcribe'
    assert c['gate_scope']['diagnostic_shapes'] == ['verdict']
    assert c['gate_scope']['diagnostic_shapes_may_fail_qualification'] is False
    assert 'malformed_generated_glyphs' in c['qualified_scope_excludes']


def test_every_threshold_is_marked_provisional_not_universal_truth():
    c = yaml.safe_load(CONTRACT.read_text(encoding='utf-8'))
    assert c['status'] == 'PROVISIONAL_PRIMARY_GATE_V2'
    for name, meta in c['thresholds'].items():
        assert meta['status'] == 'PROVISIONAL_PRIMARY_GATE_V2', name


# ------------------------------------------------------------------- the scorer
def test_exactness_is_decided_by_code_not_by_the_judge():
    assert Q.transcription_matches('शुभ दीपावली', 'शुभ दीपावली') is True
    assert Q.transcription_matches('शुभ दीपावली', 'शुब दीपावली') is False


def test_only_the_frozen_normalisation_is_applied():
    """NFC and surrounding-whitespace trimming. Nothing else: no case folding, no de-accenting."""
    assert Q.transcription_matches('Flat 50% Off', '  Flat 50% Off  ') is True
    assert Q.transcription_matches('Flat 50% Off', 'flat 50% off') is False
    assert Q.transcription_matches('Café Mocha', 'Cafe Mocha') is False


def test_nfc_equivalent_encodings_are_the_same_string():
    composed, decomposed = 'é', 'é'
    assert Q.transcription_matches(composed, decomposed) is True


def test_a_verdict_reply_is_parsed_but_never_decides_exactness():
    assert Q.parse_verdict_reply('MATCH') == 'match'
    assert Q.parse_verdict_reply('mismatch') == 'mismatch'
    assert Q.parse_verdict_reply('probably fine') == 'unparseable'


class VerdictOnlyFalsePassCandidate(Q.FakeCandidate):
    """Primary transcription is perfect; target-aware verdict agrees with wrong targets."""

    def call(self, script, item, shape, pass_index):
        reply = super().call(script, item, shape, pass_index)
        if shape == 'verdict' and item['expected'] == 'mismatch' and reply['api_status'] == 'ok':
            return {**reply, 'text': 'MATCH'}
        return reply


def test_diagnostic_verdict_false_passes_do_not_fail_the_primary_gate():
    candidate = VerdictOnlyFalsePassCandidate(name='diagnostic-sycophant')
    result = Q.qualify_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('10.00')))

    dev = result['devanagari']
    assert dev['primary_shape'] == 'transcribe'
    assert dev['metrics_by_shape']['transcribe']['false_passes'] == 0
    assert dev['metrics_by_shape']['verdict']['false_passes'] == 144
    assert dev['false_passes'] == 0
    assert 'mismatch_false_pass' not in dev['failed_gates']
    assert dev['passed'] is True
    assert result['latin'] is not None


def test_outcomes_needed_for_calibration_are_persisted_in_script_result():
    result = Q.qualify_candidate(
        Q.FakeCandidate(name='clean'),
        guard=BudgetGuard(authorised_usd=Decimal('10.00')))
    obs = result['devanagari']['observations']
    assert len(obs) == CALLS_PER_SCRIPT
    assert {o['shape'] for o in obs} == {'transcribe', 'verdict'}
    for key in ('item_id', 'shape', 'pass', 'expected', 'observed', 'api_status',
                'target', 'rendered_string', 'failure_class', 'evaluator_response'):
        assert key in obs[0], key


# ----------------------------------------------------------- progressive stop
def test_a_devanagari_false_pass_costs_576_calls_and_zero_latin_calls():
    """The whole point of the progressive gate, measured in calls."""
    candidate = Q.FakeCandidate(name='leaky', false_pass_on_first_mismatch=True)
    result = Q.qualify_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('10.00')))

    assert result['devanagari']['calls'] == CALLS_PER_SCRIPT
    assert result['latin'] is None
    assert candidate.calls_by_script['latin'] == 0
    assert result['qualified_scope'] == []
    assert result['stopped_after'] == 'devanagari'


def test_a_clean_candidate_reaches_latin_and_spends_576_more():
    candidate = Q.FakeCandidate(name='clean')
    result = Q.qualify_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('10.00')))

    assert result['devanagari']['calls'] == CALLS_PER_SCRIPT
    assert result['latin']['calls'] == CALLS_PER_SCRIPT
    assert candidate.calls_by_script['latin'] == CALLS_PER_SCRIPT
    assert result['qualified_scope'] == ['devanagari', 'latin']


def test_an_unresolved_human_review_stops_before_any_latin_call(tmp_path):
    candidate = Q.FakeCandidate(name='clean')
    p = tmp_path / 'unresolved.csv'
    p.write_text('item_id,visible_difference,usable_surface,reviewer_note\n')
    result = Q.qualify_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                                 perceptibility_path=p)

    assert result['devanagari']['calls'] == CALLS_PER_SCRIPT
    assert result['latin'] is None
    assert candidate.calls_by_script['latin'] == 0
    assert result['stopped_reason'] == 'latin_human_perceptibility_unresolved'


def test_a_high_false_fail_rate_also_stops_before_latin():
    candidate = Q.FakeCandidate(name='trigger-happy', false_fail_rate=0.5)
    result = Q.qualify_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('10.00')))
    assert result['latin'] is None
    assert 'match_false_fail_rate' in result['devanagari']['failed_gates']


def test_a_refusing_candidate_stops_before_latin():
    candidate = Q.FakeCandidate(name='refuser', refusal_rate=0.5)
    result = Q.qualify_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('10.00')))
    assert result['latin'] is None
    assert 'refusal_rate' in result['devanagari']['failed_gates']


def test_an_inconsistent_candidate_stops_before_latin():
    candidate = Q.FakeCandidate(name='flaky', inconsistent=True)
    result = Q.qualify_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('10.00')))
    assert result['latin'] is None
    assert 'repeat_consistency' in result['devanagari']['failed_gates']


# ------------------------------------------------------------------- budget stop
def test_a_budget_refusal_stops_before_the_next_call():
    """A ceiling that runs out mid-run returns an incomplete result. It never raises the ceiling."""
    candidate = Q.FakeCandidate(name='clean')
    tiny = BudgetGuard(authorised_usd=Decimal('0.001'))
    result = Q.qualify_candidate(candidate, guard=tiny)

    assert result['stopped_reason'] == 'budget_exhausted'
    assert result['qualified_scope'] == []
    assert candidate.calls < CALLS_PER_SCRIPT
    assert tiny.spent_usd <= tiny.authorised_usd


def test_the_run_never_retries_a_refusal():
    candidate = Q.FakeCandidate(name='refuser', refusal_rate=1.0)
    Q.qualify_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('10.00')))
    assert candidate.calls == CALLS_PER_SCRIPT  # not one call more
    assert candidate.retries == 0


# ------------------------------------------------------------------- materials
def test_both_scripts_supply_exactly_96_items():
    assert len(Q.load_devanagari_items()) == 96
    assert len(Q.load_latin_items()) == 96


def test_the_devanagari_view_matches_the_frozen_battery_identity():
    """Fail closed if the materialised view is not the one the human actually validated."""
    assert Q.verify_devanagari_identity()['ok'] is True


def test_live_qualification_is_refused_without_authorisation():
    with pytest.raises(Q.NotAuthorised):
        Q.main(['--live'])


# ------------------------------------------------------------------- dry run
def test_dry_run_makes_no_network_call_and_writes_no_registry_row(monkeypatch, tmp_path):
    import socket

    def explode(*a, **k):
        raise AssertionError('qualification dry-run attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)

    registry = PKG.parents[1] / 'eval' / 'registry' / 'registry-v1.jsonl'
    before = registry.read_bytes()
    out = tmp_path / 'qualification-dryrun.json'
    assert Q.main(['--dry-run', '--out', str(out)]) == 0
    assert registry.read_bytes() == before

    r = json.loads(out.read_text())
    assert r['dry_run'] is True
    assert r['external_calls'] == 0
    assert r['spend_usd'] == '0'
    assert r['registry_rows_written'] == 0
    assert r['synthetic'] is True


def test_dry_run_simulates_both_candidates_and_the_full_call_ceiling(tmp_path):
    out = tmp_path / 'q.json'
    Q.main(['--dry-run', '--out', str(out)])
    r = json.loads(out.read_text())
    assert len(r['candidates']) == 2
    assert r['maximum_evaluator_calls_if_all_survive'] == 2304


def test_dry_run_results_are_marked_unpromotable():
    result = Q.qualify_candidate(Q.FakeCandidate(name='clean'),
                                 guard=BudgetGuard(authorised_usd=Decimal('10.00')))
    assert result['synthetic'] is True
    assert result['may_populate_registry'] is False
