"""Ambiguous-dispatch accounting (EVAL-015 A, B).

The defect EVAL-014 shipped: `_dispatch` caught EVERY transport exception and called `release()`,
on the assumption that an exception proves the provider never saw the request. It does not.

A socket timeout, a connection reset, a TLS failure or a malformed response can all happen AFTER
the provider received and billed the request. Releasing there does two bad things at once: the
ledger says USD 0 for a call the provider may have charged for, weakening a user-approved hard
ceiling; and the attempted call vanishes from the evidence instead of persisting as a trial.

So the rule these controls enforce is asymmetric on purpose:

    release only when it is PROVABLE nothing was sent.
    otherwise keep the money counted and keep the trial.

No provider is contacted. Every failure below is injected.
"""
import http.client
import json
import socket
import ssl
from decimal import Decimal
from pathlib import Path

import pytest

import providers as P
import qualify_text as Q
import spend_ledger as SL
from budget_guard import BudgetGuard

OPENAI_VERSION = 'gpt-5.4-mini-2026-07-01'
GEMINI_VERSION = 'gemini-3.5-flash-lite-001'
IMAGE = b'\x89PNG\r\n\x1a\n-not-a-real-image-'


@pytest.fixture
def keys(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'REHEARSAL-NOT-A-REAL-KEY')
    monkeypatch.setenv('GOOGLE_API_KEY', 'REHEARSAL-NOT-A-REAL-KEY')
    monkeypatch.setenv('FAL_KEY', 'REHEARSAL-NOT-A-REAL-KEY')


def _run(tmp_path, run_id='run-ambiguous'):
    auth = tmp_path / 'auth.yaml'
    auth.write_text("authorised: true\ntranche_id: EMP-001\n"
                    "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    return SL.TrancheRun.create(root=tmp_path / 'runs', run_id=run_id, authorisation_path=auth)


class Exploding:
    """An injected HTTP layer that fails the way a real network fails. Counts its attempts."""

    def __init__(self, exc):
        self.exc = exc
        self.calls = 0

    def __call__(self, url, headers, body, timeout_s):
        self.calls += 1
        raise self.exc


class Garbage:
    """Dispatched fine, then returned something unparseable."""

    def __init__(self):
        self.calls = 0

    def __call__(self, url, headers, body, timeout_s):
        self.calls += 1
        return {'unexpected': 'shape', 'no': 'output field'}


AMBIGUOUS_FAILURES = [
    pytest.param(TimeoutError('read timed out'), 'timeout', id='read-timeout'),
    pytest.param(socket.timeout('timed out'), 'timeout', id='socket-timeout'),
    pytest.param(ConnectionResetError(54, 'Connection reset by peer'), 'error', id='conn-reset'),
    pytest.param(http.client.RemoteDisconnected('remote end closed'), 'error', id='remote-disc'),
    pytest.param(ssl.SSLError('tls handshake failure'), 'error', id='tls-error'),
    pytest.param(ConnectionAbortedError('aborted'), 'error', id='conn-aborted'),
]


def _judge(guard, http, version=OPENAI_VERSION):
    return P.OpenAITextJudge(
        model_alias='gpt-5.4-mini', resolved_version=version,
        transport=P.OpenAIHttpTransport(resolved_version=version, http=http), guard=guard)


# ============================================================ proven pre-dispatch may release
def test_a_missing_key_dispatches_nothing_and_frees_the_reservation(tmp_path, monkeypatch):
    """Provably pre-dispatch: the key is read before a socket is touched."""
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    http = Exploding(AssertionError('must never be reached'))

    with pytest.raises(P.DispatchRefused):
        _judge(stage, http).transcribe(IMAGE)

    assert http.calls == 0
    assert SL.TrancheBudget(run).spent_usd() == Decimal('0')


def test_a_pre_dispatch_refusal_is_not_classified_as_ambiguous(tmp_path, monkeypatch):
    monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
    t = P.GeminiHttpTransport(resolved_version=GEMINI_VERSION, http=Exploding(RuntimeError()))
    with pytest.raises(P.DispatchRefused) as e:
        t({'model': GEMINI_VERSION})
    assert not isinstance(e.value, P.AmbiguousDispatch)


def test_a_model_mismatch_refusal_frees_the_reservation(tmp_path, keys):
    """Body construction refused before send: nothing left the process."""
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    http = Exploding(AssertionError('must never be reached'))
    judge = P.GeminiTextJudge(
        model_alias='gemini-3.5-flash-lite', resolved_version=GEMINI_VERSION,
        transport=P.GeminiHttpTransport(resolved_version=GEMINI_VERSION, http=http), guard=stage)
    judge.build_transcribe_request = lambda b: {'model': 'a-different-version', 'contents': []}

    with pytest.raises(P.DispatchRefused):
        judge.transcribe(IMAGE)
    assert http.calls == 0
    assert SL.TrancheBudget(run).spent_usd() == Decimal('0')


def test_a_blindness_refusal_never_reserves_at_all(tmp_path, keys):
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    http = Exploding(AssertionError('must never be reached'))
    judge = _judge(stage, http)
    judge.build_transcribe_request = lambda b: {'model': OPENAI_VERSION, 'input': [
        {'role': 'user', 'content': [{'type': 'input_text', 'text': 'TARGET: शुभ दीपावली'}]}]}

    with pytest.raises(P.BlindnessViolation):
        judge.transcribe(IMAGE, blind_check_target='शुभ दीपावली')
    assert http.calls == 0
    assert SL.TrancheBudget(run).spent_usd() == Decimal('0')


# ============================================================ ambiguous must NOT release
@pytest.mark.parametrize('exc,expected_status', AMBIGUOUS_FAILURES)
def test_an_ambiguous_failure_keeps_the_spend_counted(tmp_path, keys, exc, expected_status):
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    http = Exploding(exc)

    response = _judge(stage, http).transcribe(IMAGE)

    assert http.calls == 1
    assert response.ambiguous_dispatch is True
    assert response.api_status == expected_status
    assert response.error_class
    assert response.billing_state == 'unknown_provisional'
    # The money stays counted. This is the whole correction.
    assert SL.TrancheBudget(run).spent_usd() > Decimal('0')


@pytest.mark.parametrize('exc,expected_status', AMBIGUOUS_FAILURES)
def test_an_ambiguous_failure_is_never_retried(tmp_path, keys, exc, expected_status):
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    http = Exploding(exc)
    _judge(stage, http).transcribe(IMAGE)
    assert http.calls == 1            # not one more


def test_a_malformed_response_after_send_is_ambiguous_not_free(tmp_path, keys):
    """The request WAS sent. That the reply was gibberish does not make the call free."""
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    http = Garbage()

    response = _judge(stage, http).transcribe(IMAGE)

    assert http.calls == 1
    assert response.ambiguous_dispatch is True
    assert response.error_class == 'malformed_response'
    assert SL.TrancheBudget(run).spent_usd() > Decimal('0')


def test_an_ambiguous_call_persists_one_trial_with_full_identity(tmp_path, keys):
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    judge = _judge(stage, Exploding(TimeoutError('read timed out')))
    judge.call_context = {'trial_id': 't-1', 'attempt_id': 't-1', 'script': 'devanagari',
                          'item_id': 'dx-0001', 'shape': 'transcribe', 'pass_index': 0,
                          'stage': 'qualification'}

    response = judge.transcribe(IMAGE)
    record = judge.call_record(response, shape='transcribe')

    assert record['trial_id'] == 't-1' and record['attempt_id'] == 't-1'
    assert record['cost_ref']
    assert record['provider'] == 'openai'
    assert record['model_alias'] == 'gpt-5.4-mini'
    assert record['resolved_version'] == OPENAI_VERSION
    assert record['api_status'] == 'timeout'
    assert record['error_class']
    assert record['retries'] == 0
    assert record['billing_state'] == 'unknown_provisional'
    assert record['provider_request_id'] is None      # unavailable, but identity still exists

    refs = {r.get('cost_ref') for r in SL.TrancheBudget(run).records()}
    assert record['cost_ref'] in refs


def test_reopening_the_run_cannot_reclaim_ambiguous_headroom(tmp_path, keys):
    """The control the Controller asked for by name."""
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    _judge(stage, Exploding(ConnectionResetError(54, 'reset'))).transcribe(IMAGE)
    spent = SL.TrancheBudget(run).spent_usd()
    assert spent > 0

    reopened = SL.TrancheBudget(SL.TrancheRun.open(tmp_path / 'runs', 'run-ambiguous'))
    assert reopened.spent_usd() == spent
    assert reopened.stage_spent_usd('qualification') == spent


def test_the_ledger_marks_the_billing_state_unknown(tmp_path, keys):
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    _judge(stage, Exploding(TimeoutError('t'))).transcribe(IMAGE)
    spends = [r for r in SL.TrancheBudget(run).records() if r['type'] == 'spend']
    assert len(spends) == 1
    assert spends[0]['billing_state'] == 'unknown_provisional'


def test_the_conservative_charge_is_the_reserved_estimate(tmp_path, keys):
    """We do not know what it cost. Counting zero is the one answer that can overspend."""
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    judge = _judge(stage, Exploding(TimeoutError('t')))
    estimate = judge._estimate()
    judge.transcribe(IMAGE)
    assert SL.TrancheBudget(run).spent_usd() == estimate


def test_ambiguity_still_respects_the_ceiling(tmp_path, keys):
    """An ambiguous call cannot push the tranche past USD 10 either."""
    run = _run(tmp_path)
    budget = SL.TrancheBudget(run)
    budget.correct(stage='qualification', amount_usd=Decimal('6.00'), reason='rehearsal burn')
    stage = budget.stage('qualification')
    http = Exploding(TimeoutError('t'))
    from budget_guard import BudgetExceeded
    with pytest.raises(BudgetExceeded):
        _judge(stage, http).transcribe(IMAGE)
    assert http.calls == 0            # refused before dispatch, so nothing was sent


def test_classification_is_explicit_and_covers_the_named_cases():
    for exc, expected in ((TimeoutError('x'), 'timeout'),
                          (socket.timeout('x'), 'timeout'),
                          (ConnectionResetError(54, 'x'), 'error'),
                          (http.client.RemoteDisconnected('x'), 'error'),
                          (ssl.SSLError('x'), 'error')):
        status, error_class = P.classify_transport_failure(exc)
        assert status == expected
        assert error_class


def test_an_in_memory_guard_also_keeps_ambiguous_spend(tmp_path, keys):
    """The dry-run guard has no release(); it must still settle rather than silently skip."""
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    judge = _judge(guard, Exploding(TimeoutError('t')))
    response = judge.transcribe(IMAGE)
    assert response.ambiguous_dispatch is True
    assert guard.spent_usd > 0


# ============================================================ the run stops, it does not limp on
def test_qualification_stops_after_an_ambiguous_dispatch(tmp_path, keys):
    """Stop the tranche rather than carry on as if nothing happened."""
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    http = Exploding(TimeoutError('read timed out'))
    candidate = Q.LiveCandidate(judge=_judge(stage, http), images=Q.ImageResolver())

    result = Q.qualify_candidate(candidate, guard=stage)

    assert result['stopped_reason'] == 'ambiguous_dispatch'
    assert result['qualified_scope'] == []
    assert result['latin'] is None
    assert http.calls == 1                       # stopped on the first one, no retry
    assert len(result['devanagari']['call_records']) == 1
    assert result['devanagari']['call_records'][0]['api_status'] == 'timeout'


def test_the_stopped_qualification_still_persists_its_one_trial(tmp_path, keys):
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    candidate = Q.LiveCandidate(judge=_judge(stage, Exploding(ConnectionResetError(54, 'x'))),
                                images=Q.ImageResolver())
    result = Q.qualify_candidate(candidate, guard=stage)

    record = result['devanagari']['call_records'][0]
    assert record['trial_id'] and record['cost_ref']
    assert record['retries'] == 0
    assert SL.TrancheBudget(run).spent_usd() > 0
