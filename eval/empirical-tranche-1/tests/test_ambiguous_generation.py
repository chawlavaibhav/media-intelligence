"""Ambiguous fal generation accounting (EVAL-015 C).

B12: A-TEXT reserved generation spend and then called the fal route. If the route raised, the
runner exited before creating the Attempt — fail-closed for budget, because the reservation stayed
pending, but the provider attempt itself was never persisted as a trial. An image generation that
may have been billed simply had no record at all.

So an ambiguous generation failure must now: persist the Attempt, carry timeout/error with an
explicit class, keep a resolvable cost_ref, keep the spend counted, make NO evaluator call because
there is no artifact, never retry, and stop the run.

fal is never contacted. Every failure is injected.
"""
import http.client
import socket
import ssl
from decimal import Decimal
from pathlib import Path

import pytest

import providers as P
import run_atex as R
import spend_ledger as SL

PKG = Path(__file__).resolve().parents[1]
REGISTRY = PKG.parents[1] / 'eval' / 'registry' / 'registry-v1.jsonl'


@pytest.fixture
def fal_key(monkeypatch):
    monkeypatch.setenv('FAL_KEY', 'REHEARSAL-NOT-A-REAL-KEY')


def _run(tmp_path, run_id='run-gen-ambiguous'):
    auth = tmp_path / 'auth.yaml'
    auth.write_text("authorised: true\ntranche_id: EMP-001\n"
                    "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    return SL.TrancheRun.create(root=tmp_path / 'runs', run_id=run_id, authorisation_path=auth,
                                mode='fake_live')


class ExplodingFal:
    def __init__(self, exc, fail_on_call=1):
        self.exc = exc
        self.fail_on_call = fail_on_call
        self.calls = 0

    def __call__(self, url, headers, body, timeout_s):
        self.calls += 1
        if self.calls >= self.fail_on_call:
            raise self.exc
        return {'request_id': f'fal-{self.calls:04d}',
                'images': [{'url': f'https://fal.media/fake/{self.calls}.png'}]}


class CountingJudge:
    """Records whether A-TEXT ever asked it to look at anything."""

    provider, model_alias, resolved_version = 'openai', 'a', 'v'

    def __init__(self):
        self.transcribe_calls = 0

    def transcribe(self, image_bytes, blind_check_target=''):
        self.transcribe_calls += 1
        return P.EvaluatorResponse('x', 1, 1, Decimal('0.001'), 'r')

    def identity(self):
        return {'provider': 'openai', 'model_alias': 'a', 'resolved_version': 'v',
                'version_pinned_at_execution': True}

    def call_record(self, response, shape):
        return {**self.identity(), 'shape': shape, 'api_status': response.api_status,
                'error_class': None, 'provider_request_id': 'r', 'input_tokens': 1,
                'output_tokens': 1, 'billed_usd': '0.001', 'cost_basis': 'x',
                'billing_state': response.billing_state, 'retries': 0}


AMBIGUOUS = [
    pytest.param(TimeoutError('read timed out'), 'timeout', id='timeout'),
    pytest.param(ConnectionResetError(54, 'reset'), 'error', id='conn-reset'),
    pytest.param(http.client.RemoteDisconnected('closed'), 'error', id='remote-disconnect'),
    pytest.param(ssl.SSLError('tls'), 'error', id='tls'),
]

QUALIFIED = {'candidate': 'j', 'qualified_scope': ['devanagari', 'latin'], 'synthetic': False}


def _routes(http, artifacts=None):
    cfg = R.config()
    return {slot: P.fal_route_for(slot, cfg, http=http,
                                  artifact_fetch=artifacts or (lambda u: b'\x89PNG\r\n\x1a\n' + u.encode()))
            for slot in cfg['atex']['slots']}


def _atex(tmp_path, http, judge=None, run=None):
    run = run or _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('atex')
    return R.run(judge=QUALIFIED, judge_instance=judge or CountingJudge(),
                 routes=_routes(http), preflight_green=True, guard=stage,
                 dry_run=False, authorisation_path=Path(run.record['authorisation_path'])), run


# ============================================================ pre-dispatch may release
def test_a_missing_fal_key_dispatches_nothing_and_frees_the_reservation(tmp_path, monkeypatch):
    monkeypatch.delenv('FAL_KEY', raising=False)
    run = _run(tmp_path)
    http = ExplodingFal(AssertionError('must never be reached'))
    with pytest.raises(P.DispatchRefused):
        _atex(tmp_path, http, run=run)
    assert http.calls == 0
    assert SL.TrancheBudget(run).spent_usd() == Decimal('0')


def test_a_pre_dispatch_fal_refusal_is_the_provable_subtype(tmp_path, monkeypatch):
    monkeypatch.delenv('FAL_KEY', raising=False)
    route = P.FalImageRoute(slot='IMG-01', route='openai/gpt-image-2',
                            http=ExplodingFal(RuntimeError()))
    with pytest.raises(P.PreDispatchRefusal):
        route({'prompt': 'x'})


# ============================================================ ambiguous keeps everything
@pytest.mark.parametrize('exc,expected_status', AMBIGUOUS)
def test_an_ambiguous_generation_persists_its_attempt(tmp_path, fal_key, exc, expected_status):
    http = ExplodingFal(exc, fail_on_call=1)
    result, run = _atex(tmp_path, http)

    assert http.calls == 1
    assert result['stopped_reason'] == 'ambiguous_dispatch'
    assert len(result['attempts']) == 1
    attempt = result['attempts'][0]
    assert attempt['api_status'] == expected_status
    assert attempt['error_class']
    assert attempt['cost_ref']
    assert attempt['trial_id'] and attempt['attempt_id']
    assert attempt['route'] and attempt['slot'] and attempt['provider_surface'] == 'fal'
    assert attempt['retry_of_attempt_id'] is None
    assert attempt['billing_state'] == 'unknown_provisional'


@pytest.mark.parametrize('exc,expected_status', AMBIGUOUS)
def test_an_ambiguous_generation_keeps_the_spend_counted(tmp_path, fal_key, exc, expected_status):
    result, run = _atex(tmp_path, ExplodingFal(exc))
    spent = SL.TrancheBudget(run).spent_usd()
    assert spent > Decimal('0')
    assert SL.TrancheBudget(run).stage_spent_usd('atex') == spent


def test_the_generation_cost_ref_resolves_to_the_ledger(tmp_path, fal_key):
    result, run = _atex(tmp_path, ExplodingFal(TimeoutError('t')))
    refs = {r.get('cost_ref') for r in SL.TrancheBudget(run).records()}
    assert result['attempts'][0]['cost_ref'] in refs


def test_no_evaluator_call_happens_when_no_artifact_exists(tmp_path, fal_key):
    judge = CountingJudge()
    http = ExplodingFal(TimeoutError('t'))
    _atex(tmp_path, http, judge=judge)
    assert judge.transcribe_calls == 0
    assert http.calls == 1


def test_an_ambiguous_generation_is_never_retried(tmp_path, fal_key):
    http = ExplodingFal(ConnectionResetError(54, 'reset'))
    result, _ = _atex(tmp_path, http)
    assert http.calls == 1
    assert result['retries'] == 0


def test_the_run_stops_rather_than_continuing_to_the_remaining_generations(tmp_path, fal_key):
    """Without the stop, 15 more paid calls would follow a call nobody can account for."""
    http = ExplodingFal(TimeoutError('t'), fail_on_call=3)
    result, _ = _atex(tmp_path, http)
    assert http.calls == 3
    assert result['generations'] == 3
    assert result['generations'] < 16
    assert result['stopped_reason'] == 'ambiguous_dispatch'


def test_the_measurement_for_an_ambiguous_generation_is_an_absence_not_a_mismatch(tmp_path,
                                                                                  fal_key):
    """A generation that may not have happened did not produce wrong text."""
    result, _ = _atex(tmp_path, ExplodingFal(TimeoutError('t')))
    m = [x for x in result['measurements'] if x['role'] == 'primary'][0]
    assert m['exact_match'] is None
    assert m['absent_reason'] == 'no_artifact_produced'
    assert result['scoreable_opportunities'] == 0


def test_an_ambiguous_generation_does_not_make_the_stop_rule_eligible(tmp_path, fal_key):
    """Zero exact matches out of zero scoreable opportunities is not evidence of failure."""
    result, _ = _atex(tmp_path, ExplodingFal(TimeoutError('t')))
    assert result['exact_matches'] == 0
    assert result['text_specific_stop_eligible'] is False


def test_reopening_the_run_cannot_reclaim_the_generation_headroom(tmp_path, fal_key):
    result, run = _atex(tmp_path, ExplodingFal(TimeoutError('t')))
    spent = SL.TrancheBudget(run).spent_usd()
    reopened = SL.TrancheBudget(SL.TrancheRun.open(tmp_path / 'runs', 'run-gen-ambiguous'))
    assert reopened.spent_usd() == spent > Decimal('0')


def test_the_registry_is_untouched_by_an_ambiguous_generation(tmp_path, fal_key):
    before = REGISTRY.read_bytes()
    _atex(tmp_path, ExplodingFal(TimeoutError('t')))
    assert REGISTRY.read_bytes() == before


def test_an_ambiguous_generation_result_is_still_non_promotable(tmp_path, fal_key):
    result, _ = _atex(tmp_path, ExplodingFal(TimeoutError('t')))
    assert result['may_populate_registry'] is False
    assert result['registry_rows_written'] == 0
    with pytest.raises(R.PartialEvidenceOnly):
        R.promote_slot(result)


def test_a_successful_run_is_unaffected_by_the_new_semantics(tmp_path, fal_key):
    """No-regression: a clean fake-live A-TEXT still does all 16."""
    from fake_live import FakeFalHttp
    result, run = _atex(tmp_path, FakeFalHttp())
    assert result['generations'] == 16
    assert result['stopped_reason'] is None
    assert result['per_route'] == {'IMG-01': 8, 'IMG-02': 8}


# ============================================================ ambiguity on the EVALUATOR side
class AmbiguousJudge:
    """Generation succeeded; the judge call is the one whose outcome is unknown."""

    provider, model_alias, resolved_version = 'openai', 'a', 'v'

    def __init__(self):
        self.transcribe_calls = 0

    def transcribe(self, image_bytes, blind_check_target=''):
        self.transcribe_calls += 1
        return P.EvaluatorResponse(
            '', None, None, Decimal('0.0018'), None, api_status='timeout',
            error_class='read_timeout', billing_state='unknown_provisional',
            ambiguous_dispatch=True)

    def identity(self):
        return {'provider': 'openai', 'model_alias': 'a', 'resolved_version': 'v',
                'version_pinned_at_execution': True}

    def call_record(self, response, shape):
        return {**self.identity(), 'shape': shape, 'api_status': response.api_status,
                'error_class': response.error_class, 'provider_request_id': None,
                'input_tokens': None, 'output_tokens': None,
                'billed_usd': str(response.billed_usd), 'cost_basis': response.cost_basis,
                'billing_state': response.billing_state, 'retries': 0,
                'cost_ref': 'cost-eval-ambiguous'}


def test_an_ambiguous_evaluator_call_inside_atex_stops_the_run(tmp_path, fal_key):
    """The generation was fine; the measurement is what we cannot account for. Stop anyway."""
    from fake_live import FakeFalHttp

    judge = AmbiguousJudge()
    fal = FakeFalHttp()
    result, run = _atex(tmp_path, fal, judge=judge)

    assert result['stopped_reason'] == 'ambiguous_dispatch'
    assert judge.transcribe_calls == 1          # no retry, and no second item attempted
    assert len(fal.calls) == 1
    assert result['generations'] == 1


def test_both_trials_are_preserved_when_the_evaluator_is_ambiguous(tmp_path, fal_key):
    """One generation trial that succeeded, one evaluator trial that may have been billed."""
    from fake_live import FakeFalHttp

    result, run = _atex(tmp_path, FakeFalHttp(), judge=AmbiguousJudge())

    assert len(result['attempts']) == 1
    assert result['attempts'][0]['api_status'] == 'ok'
    assert len(result['evaluator_calls']) == 1
    assert result['evaluator_calls'][0]['api_status'] == 'timeout'
    assert result['evaluator_calls'][0]['billing_state'] == 'unknown_provisional'

    m = [x for x in result['measurements'] if x['role'] == 'primary'][0]
    assert m['absent_reason'] == 'evaluator_timeout'
    assert m['exact_match'] is None
