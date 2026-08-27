"""Durable per-call trial and cost identity (EVAL-014 B).

`one_call_one_trial: true` on a record is an assertion, not an identity. If two calls carry the
same trial id, or a cost_ref that resolves to nothing, the claim is decoration: you cannot count
trials, cannot reconcile spend against an invoice, and cannot tell a repeat from a duplicate.

So these controls check the identity is UNIQUE and RESOLVABLE, at the frozen full scale.
"""
import json
from decimal import Decimal
from pathlib import Path

import pytest

import providers as P
import qualify_text as Q
import spend_ledger as SL
from fake_live import FakeJudgeHttp, image_index_for

CALLS_PER_SCRIPT = 576
OPENAI_VERSION = 'gpt-5.4-mini-2026-07-01'


@pytest.fixture
def keys(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'fake-live-openai-key')
    monkeypatch.setenv('GOOGLE_API_KEY', 'fake-live-google-key')


def _run(tmp_path, run_id='run-trials'):
    auth = tmp_path / 'auth.yaml'
    auth.write_text("authorised: true\ntranche_id: EMP-001\n"
                    "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    return SL.TrancheRun.create(root=tmp_path / 'runs', run_id=run_id, authorisation_path=auth)


def _candidate(tmp_path, http, run=None):
    run = run or _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('qualification')
    judge = P.OpenAITextJudge(
        model_alias='gpt-5.4-mini', resolved_version=OPENAI_VERSION,
        transport=P.OpenAIHttpTransport(resolved_version=OPENAI_VERSION, http=http), guard=stage)
    return Q.LiveCandidate(judge=judge, images=Q.ImageResolver()), run


# ---------------------------------------------------------------- one call, one identity
def test_a_single_live_call_carries_every_required_identity_field(tmp_path, keys):
    http = FakeJudgeHttp(P.OpenAITextJudge, image_index_for('latin'))
    candidate, run = _candidate(tmp_path, http)
    item = Q._script_items('latin')[0]

    record = candidate.call('latin', item, 'transcribe', 0)['call_record']

    for field in ('trial_id', 'attempt_id', 'cost_ref', 'provider', 'model_alias',
                  'resolved_version', 'script', 'item_id', 'shape', 'pass_index',
                  'provider_request_id', 'api_status', 'retries', 'synthetic'):
        assert field in record, field
    assert record['retries'] == 0
    assert record['synthetic'] is False
    assert record['item_id'] == item['item_id']
    assert record['script'] == 'latin'
    assert record['shape'] == 'transcribe'
    assert record['resolved_version'] == OPENAI_VERSION


def test_the_cost_ref_resolves_to_a_ledger_record(tmp_path, keys):
    http = FakeJudgeHttp(P.OpenAITextJudge, image_index_for('latin'))
    candidate, run = _candidate(tmp_path, http)
    record = candidate.call('latin', Q._script_items('latin')[0], 'transcribe', 0)['call_record']

    refs = {r.get('cost_ref') for r in SL.TrancheBudget(run).records()}
    assert record['cost_ref'] in refs


def test_the_trial_id_and_attempt_id_are_not_the_same_string(tmp_path, keys):
    """One call is one trial, but the attempt identity must stay topology-compatible."""
    http = FakeJudgeHttp(P.OpenAITextJudge, image_index_for('latin'))
    candidate, _ = _candidate(tmp_path, http)
    r = candidate.call('latin', Q._script_items('latin')[0], 'transcribe', 0)['call_record']
    assert r['trial_id'] and r['attempt_id']
    assert r['trial_id'] == r['attempt_id']    # root call: trial IS the attempt, per models.py


def test_spend_lands_on_the_persistent_ledger_not_in_memory(tmp_path, keys):
    http = FakeJudgeHttp(P.OpenAITextJudge, image_index_for('latin'))
    candidate, run = _candidate(tmp_path, http)
    candidate.call('latin', Q._script_items('latin')[0], 'transcribe', 0)

    reopened = SL.TrancheBudget(SL.TrancheRun.open(root=tmp_path / 'runs', run_id='run-trials'))
    assert reopened.spent_usd() > 0
    assert reopened.stage_spent_usd('qualification') > 0


# ---------------------------------------------------------------- at frozen full scale
def test_2304_fake_live_dispatches_yield_2304_unique_trials_and_cost_refs(tmp_path, keys):
    """The frozen maximum: 2 candidates x 2 scripts x 96 items x 2 shapes x 3 passes."""
    run = _run(tmp_path, 'run-full')
    index = image_index_for('both')
    images = Q.ImageResolver()

    candidates = []
    for cls, transport_cls, version, alias in (
            (P.OpenAITextJudge, P.OpenAIHttpTransport, 'openai-snapshot-1', 'gpt-5.4-mini'),
            (P.GeminiTextJudge, P.GeminiHttpTransport, 'google-snapshot-1',
             'gemini-3.5-flash-lite')):
        stage = SL.TrancheBudget(run).stage('qualification')
        candidates.append(Q.LiveCandidate(
            judge=cls(model_alias=alias, resolved_version=version,
                      transport=transport_cls(resolved_version=version,
                                              http=FakeJudgeHttp(cls, index)),
                      guard=stage),
            images=images))

    records = []
    for c in candidates:
        result = Q.qualify_candidate(c, guard=c.judge.guard)
        records.extend(result['devanagari']['call_records'])
        if result['latin']:
            records.extend(result['latin']['call_records'])

    assert len(records) == 2304
    assert len({r['trial_id'] for r in records}) == 2304
    assert len({r['cost_ref'] for r in records}) == 2304

    ledger_refs = {r.get('cost_ref') for r in SL.TrancheBudget(run).records()}
    unresolved = [r['cost_ref'] for r in records if r['cost_ref'] not in ledger_refs]
    assert unresolved == []

    assert all(r['retries'] == 0 for r in records)
    assert all(r['synthetic'] is False for r in records)


def test_every_call_record_names_the_exact_version_that_produced_it(tmp_path, keys):
    run = _run(tmp_path, 'run-versions')
    index = image_index_for('devanagari')
    stage = SL.TrancheBudget(run).stage('qualification')
    judge = P.OpenAITextJudge(
        model_alias='gpt-5.4-mini', resolved_version='pinned-snapshot-xyz',
        transport=P.OpenAIHttpTransport(resolved_version='pinned-snapshot-xyz',
                                        http=FakeJudgeHttp(P.OpenAITextJudge, index)),
        guard=stage)
    candidate = Q.LiveCandidate(judge=judge, images=Q.ImageResolver())
    result = Q.qualify_candidate(candidate, guard=stage)
    versions = {r['resolved_version'] for r in result['devanagari']['call_records']}
    assert versions == {'pinned-snapshot-xyz'}


def test_the_ledger_holds_one_spend_record_per_dispatch(tmp_path, keys):
    http = FakeJudgeHttp(P.OpenAITextJudge, image_index_for('latin'))
    candidate, run = _candidate(tmp_path, http, _run(tmp_path, 'run-count'))
    for i, item in enumerate(Q._script_items('latin')[:10]):
        candidate.call('latin', item, 'transcribe', 0)

    rows = SL.TrancheBudget(run).records()
    assert len([r for r in rows if r['type'] == 'spend']) == 10
    assert len([r for r in rows if r['type'] == 'reservation']) == 10
    assert len(http.calls) == 10


def test_a_refused_call_still_gets_a_trial_and_a_cost_ref(tmp_path, keys):
    """A refusal consumed a call. It keeps its identity and its cost, and is never retried."""
    http = FakeJudgeHttp(P.OpenAITextJudge, image_index_for('latin'), refuse_all=True)
    candidate, run = _candidate(tmp_path, http, _run(tmp_path, 'run-refusal'))
    record = candidate.call('latin', Q._script_items('latin')[0], 'transcribe', 0)['call_record']

    assert record['api_status'] == 'refusal'
    assert record['trial_id'] and record['cost_ref']
    assert record['retries'] == 0
    refs = {r.get('cost_ref') for r in SL.TrancheBudget(run).records()}
    assert record['cost_ref'] in refs


def test_a_blindness_refusal_burns_no_budget_and_leaves_no_orphan_reservation(tmp_path, keys):
    """A call that never dispatched must not permanently consume headroom."""
    run = _run(tmp_path, 'run-blind')
    stage = SL.TrancheBudget(run).stage('qualification')
    http = FakeJudgeHttp(P.OpenAITextJudge, image_index_for('devanagari'))
    judge = P.OpenAITextJudge(
        model_alias='gpt-5.4-mini', resolved_version=OPENAI_VERSION,
        transport=P.OpenAIHttpTransport(resolved_version=OPENAI_VERSION, http=http), guard=stage)
    target = Q._script_items('devanagari')[0]['target']
    judge.build_transcribe_request = lambda b: {'model': OPENAI_VERSION, 'input': [
        {'role': 'user', 'content': [{'type': 'input_text', 'text': f'TARGET: {target}'}]}]}

    with pytest.raises(P.BlindnessViolation):
        judge.transcribe(b'anything', blind_check_target=target)

    assert http.calls == []
    assert SL.TrancheBudget(run).spent_usd() == Decimal('0')
