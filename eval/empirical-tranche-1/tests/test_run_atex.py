"""Gate-order controls on the A-TEXT runner.

Five gates stand between this code and a paid image generation. Each test below opens exactly one
of them and confirms that no generator adapter is invoked — measured by a call counter on a fake
adapter, not by reading the code.

The 16-generation ceiling is likewise proved by counting, and the runner is checked for the thing
it must NOT contain: a retry path.
"""
import json
from decimal import Decimal
from pathlib import Path

import pytest

import run_atex as R
from budget_guard import BudgetExceeded, BudgetGuard

PKG = Path(__file__).resolve().parents[1]
REGISTRY = PKG.parents[1] / 'eval' / 'registry' / 'registry-v1.jsonl'

QUALIFIED_JUDGE = {'candidate': 'fake-judge', 'qualified_scope': ['devanagari', 'latin'],
                   'synthetic': True}
UNQUALIFIED_JUDGE = {'candidate': 'fake-judge', 'qualified_scope': [], 'synthetic': True}


def _guard():
    return BudgetGuard(authorised_usd=Decimal('10.00'))


# ------------------------------------------------------------------ gate 1: authorisation
def test_missing_authorisation_invokes_no_generator(tmp_path):
    gen = R.FakeGenerator()
    with pytest.raises(R.GateClosed) as e:
        R.run(authorisation_path=tmp_path / 'nope.yaml', judge=QUALIFIED_JUDGE,
              generator=gen, preflight_green=True, guard=_guard())
    assert gen.calls == 0
    assert 'authorisation' in str(e.value).lower()


def test_false_authorisation_invokes_no_generator():
    gen = R.FakeGenerator()
    with pytest.raises(R.GateClosed):
        R.run(authorisation_path=R.AUTHORISATION_EXAMPLE_PATH, judge=QUALIFIED_JUDGE,
              generator=gen, preflight_green=True, guard=_guard())
    assert gen.calls == 0


# ------------------------------------------------------------------ gate 2: qualified judge
def test_no_qualified_judge_invokes_no_generator():
    gen = R.FakeGenerator()
    with pytest.raises(R.GateClosed) as e:
        R.run(judge=UNQUALIFIED_JUDGE, generator=gen, preflight_green=True,
              guard=_guard(), dry_run=True)
    assert gen.calls == 0
    assert 'judge' in str(e.value).lower()


def test_a_judge_qualified_only_on_devanagari_still_gates_latin_items():
    """A partially qualified judge cannot score the Hinglish/Latin items."""
    partial = {'candidate': 'fake', 'qualified_scope': ['devanagari'], 'synthetic': True}
    gen = R.FakeGenerator()
    with pytest.raises(R.GateClosed):
        R.run(judge=partial, generator=gen, preflight_green=True, guard=_guard(), dry_run=True)
    assert gen.calls == 0


# ------------------------------------------------------------------ gate 3: preflight
def test_a_red_preflight_invokes_no_generator():
    gen = R.FakeGenerator()
    with pytest.raises(R.GateClosed) as e:
        R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=False,
              guard=_guard(), dry_run=True)
    assert gen.calls == 0
    assert 'preflight' in str(e.value).lower()


# ------------------------------------------------------------------ gate 4: budget
def test_a_guard_that_cannot_reserve_invokes_no_generator():
    gen = R.FakeGenerator()
    exhausted = BudgetGuard(authorised_usd=Decimal('0.001'), spent_usd=Decimal('0.001'))
    with pytest.raises(BudgetExceeded):
        R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
              guard=exhausted, dry_run=True)
    assert gen.calls == 0


def test_the_budget_stops_the_run_partway_without_raising_the_ceiling():
    gen = R.FakeGenerator()
    small = BudgetGuard(authorised_usd=Decimal('0.20'))
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=small, dry_run=True, stop_on_budget=True)
    assert result['stopped_reason'] == 'budget_exhausted'
    assert gen.calls < 16
    assert small.spent_usd <= small.authorised_usd


# ------------------------------------------------------------------ gate 5: route ceiling
def test_a_route_may_not_exceed_its_declared_eight_generations():
    gen = R.FakeGenerator()
    with pytest.raises(R.GateClosed) as e:
        R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True, guard=_guard(),
              dry_run=True, repeats_override=3)
    assert gen.calls == 0
    assert '8' in str(e.value)


# ------------------------------------------------------------------ the ceiling, counted
def test_a_full_dry_run_makes_exactly_sixteen_generation_calls():
    gen = R.FakeGenerator()
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=_guard(), dry_run=True)
    assert gen.calls == 16
    assert result['generations'] == 16
    assert result['per_route'] == {'IMG-01': 8, 'IMG-02': 8}


def test_every_generation_is_its_own_trial():
    gen = R.FakeGenerator()
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=_guard(), dry_run=True)
    assert result['trials'] == 16
    assert len({a['attempt_id'] for a in result['attempts']}) == 16
    assert len({a['trial_id'] for a in result['attempts']}) == 16


def test_a_refusal_is_persisted_and_never_retried():
    gen = R.FakeGenerator(refuse_every=4)
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=_guard(), dry_run=True)
    assert gen.calls == 16          # not one more
    assert result['retries'] == 0
    refusals = [a for a in result['attempts'] if a['api_status'] == 'refusal']
    assert refusals
    assert all(a['error_class'] for a in refusals)
    assert all(a['cost_ref'] for a in refusals)   # a refused call still costs its trial


def test_a_run_where_every_call_refuses_still_dispatches_exactly_sixteen():
    """The real no-retry control.

    An earlier version of this test grepped the source for 'retry_of' — which is wrong twice
    over: the persistence contract REQUIRES a retry_of_attempt_id field (pinned to None), and a
    grep would have been satisfied by a comment. What matters is behavioural: when every single
    call fails, the runner must not dispatch a seventeenth.
    """
    gen = R.FakeGenerator(refuse_every=1)
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=_guard(), dry_run=True)
    assert gen.calls == 16
    assert result['generations'] == 16
    assert result['retries'] == 0
    assert all(a['api_status'] == 'refusal' for a in result['attempts'])
    assert all(a['retry_of_attempt_id'] is None for a in result['attempts'])


def test_no_attempt_ever_carries_a_retry_reference():
    for gen in (R.FakeGenerator(), R.FakeGenerator(refuse_every=3)):
        result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                       guard=_guard(), dry_run=True)
        assert all(a['retry_of_attempt_id'] is None for a in result['attempts'])


# ------------------------------------------------------------------ seeds
def test_no_seed_is_supplied_for_these_unseeded_repeats():
    gen = R.FakeGenerator()
    R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
          guard=_guard(), dry_run=True)
    assert all(req.get('seed') is None for req in gen.requests)
    assert all(req.get('seed_policy') == 'unseeded' for req in gen.requests)


def test_repeats_are_recorded_as_repeats_not_retries():
    gen = R.FakeGenerator()
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=_guard(), dry_run=True)
    repeats = [a for a in result['attempts'] if a['repeat_index'] == 1]
    assert len(repeats) == 8
    assert all(a['retry_of_attempt_id'] is None for a in result['attempts'])


# ------------------------------------------------------------------ persistence shape
def test_output_records_carry_the_shapes_persistence_needs():
    gen = R.FakeGenerator()
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=_guard(), dry_run=True)
    a = result['attempts'][0]
    for key in ('attempt_id', 'trial_id', 'item_id', 'route', 'provider_surface', 'api_status',
                'seed', 'seed_policy', 'repeat_index', 'retry_of_attempt_id', 'cost_ref'):
        assert key in a, key
    m = result['measurements'][0]
    for key in ('measurement_id', 'attempt_id', 'item_id', 'shape', 'exact_match', 'synthetic'):
        assert key in m, key
    assert json.dumps(result['attempts'])


def test_the_primary_measurement_is_blind_transcription():
    gen = R.FakeGenerator()
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=_guard(), dry_run=True)
    primary = [m for m in result['measurements'] if m['role'] == 'primary']
    assert primary and all(m['shape'] == 'transcribe' for m in primary)


# ------------------------------------------------------------------ Registry isolation
def test_dry_run_results_cannot_enter_the_registry():
    gen = R.FakeGenerator()
    result = R.run(judge=QUALIFIED_JUDGE, generator=gen, preflight_green=True,
                   guard=_guard(), dry_run=True)
    assert result['synthetic'] is True
    assert result['registry_rows_written'] == 0
    assert all(m['synthetic'] is True for m in result['measurements'])


def test_the_harness_refuses_a_dry_run_measurement_at_the_registry_boundary():
    """NEGATIVE CONTROL against the real harness, not against a promise in a docstring."""
    r = R.attempt_registry_write_with_dry_run_evidence()
    assert r['refused'] is True
    assert 'synthetic' in r['message'].lower()


def test_cli_dry_run_leaves_the_registry_byte_identical(tmp_path):
    before = REGISTRY.read_bytes()
    out = tmp_path / 'atex-dryrun.json'
    assert R.main(['--dry-run', '--out', str(out)]) == 0
    assert REGISTRY.read_bytes() == before
    r = json.loads(out.read_text())
    assert r['external_calls'] == 0
    assert r['spend_usd'] == '0'
    assert r['maximum_future_generations'] == 16


def test_cli_refuses_live_without_authorisation():
    assert R.main(['--live']) != 0
