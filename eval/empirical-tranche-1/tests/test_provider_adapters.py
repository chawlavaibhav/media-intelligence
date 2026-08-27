"""EMP-001 judge adapter controls. No provider is contacted by anything in this file.

Two things are being protected.

  1. BLINDNESS. The `transcribe` shape is the primary measurement, and it is only worth anything
     if the judge genuinely never saw the target. A leak through a field nobody anticipated turns
     the primary measurement into the secondary one, silently.

  2. FAIL-CLOSED DISPATCH. Nothing in this module may reach a network by accident: not at import,
     not at construction, not from a default argument. Money is spent only through an explicitly
     injected transport that has already been reserved against a budget guard.
"""
import json
import os
import socket
from decimal import Decimal

import pytest

import providers as P
from budget_guard import BudgetExceeded, BudgetGuard


TARGET_DEV = 'शुभ दीपावली'
TARGET_LAT = 'Flat 50% Off'
IMAGE = b'\x89PNG\r\n\x1a\n-not-a-real-image-'


# ------------------------------------------------------- nothing happens on construction
def test_constructors_make_no_network_call(monkeypatch):
    def explode(*a, **k):
        raise AssertionError('a judge constructor attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)

    P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='claude-sonnet-5')
    P.GeminiTextJudge(model_alias='gemini-3.5-flash-lite',
                      resolved_version='gemini-3.5-flash-lite-001')


def test_no_api_key_is_read_during_import_or_construction(monkeypatch):
    """A key read at construction time is a key that leaks into a dry run."""
    reads = []

    class Tracking(dict):
        def __getitem__(self, k):
            reads.append(k)
            return super().__getitem__(k)

        def get(self, k, default=None):
            reads.append(k)
            return super().get(k, default)

    monkeypatch.setattr(os, 'environ', Tracking(os.environ))

    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='x')
    j.build_transcribe_request(IMAGE)
    j.build_verdict_request(IMAGE, TARGET_DEV)

    assert not [r for r in reads if 'KEY' in r.upper() or 'TOKEN' in r.upper()], reads


# ------------------------------------------------------------------------ blindness
@pytest.mark.parametrize('judge_cls,alias', [
    (P.AnthropicTextJudge, 'claude-sonnet-5'),
    (P.GeminiTextJudge, 'gemini-3.5-flash-lite'),
])
@pytest.mark.parametrize('target', [TARGET_DEV, TARGET_LAT])
def test_transcribe_payload_never_contains_the_target(judge_cls, alias, target):
    j = judge_cls(model_alias=alias, resolved_version='v')
    blob = json.dumps(j.build_transcribe_request(IMAGE), ensure_ascii=False)
    assert target not in blob


def test_transcribe_payload_contains_no_devanagari_at_all():
    """The catch-all. Every Devanagari target is Devanagari, so any of it in a blind payload is
    decisive regardless of which field carried it."""
    for cls, alias in ((P.AnthropicTextJudge, 'claude-sonnet-5'),
                       (P.GeminiTextJudge, 'gemini-3.5-flash-lite')):
        blob = json.dumps(cls(model_alias=alias, resolved_version='v')
                          .build_transcribe_request(IMAGE), ensure_ascii=False)
        assert not any('ऀ' <= ch <= 'ॿ' for ch in blob)


def test_the_blind_check_actually_fires_on_a_leak():
    """NEGATIVE CONTROL. If this passes a leaking payload, every blindness test above is theatre."""
    leaking = {'model': 'x', 'input': [{'text': f'TARGET: {TARGET_DEV}'}]}
    violations = P.verify_blind_payload(leaking, shape='transcribe', target=TARGET_DEV)
    assert violations


def test_the_blind_check_passes_a_clean_payload():
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v')
    assert P.verify_blind_payload(j.build_transcribe_request(IMAGE),
                                  shape='transcribe', target=TARGET_DEV) == []


def test_building_a_transcribe_request_cannot_be_handed_a_target():
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v')
    with pytest.raises(TypeError):
        j.build_transcribe_request(IMAGE, TARGET_DEV)


# --------------------------------------------------------------- verdict is deliberately not blind
@pytest.mark.parametrize('judge_cls,alias', [
    (P.AnthropicTextJudge, 'claude-sonnet-5'),
    (P.GeminiTextJudge, 'gemini-3.5-flash-lite'),
])
def test_verdict_payload_carries_the_target_exactly_once(judge_cls, alias):
    j = judge_cls(model_alias=alias, resolved_version='v')
    blob = json.dumps(j.build_verdict_request(IMAGE, TARGET_DEV), ensure_ascii=False)
    assert blob.count(TARGET_DEV) == 1


def test_verdict_payload_carries_the_target_inside_the_prompt():
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v')
    req = j.build_verdict_request(IMAGE, TARGET_DEV)
    assert TARGET_DEV in P.prompt_text_of(req)


def test_verdict_blind_check_rejects_a_payload_that_lost_its_target():
    stripped = {'model': 'x', 'input': [{'text': 'Does the text match?'}]}
    assert P.verify_blind_payload(stripped, shape='verdict', target=TARGET_DEV)


# ---------------------------------------------------------------- alias vs resolved version
def test_anthropic_canonical_model_id_is_itself_a_pinned_resolved_version():
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5',
                             resolved_version='claude-sonnet-5')
    ident = j.identity()
    assert ident['model_alias'] == 'claude-sonnet-5'
    assert ident['resolved_version'] == 'claude-sonnet-5'
    assert ident['version_pinned_at_execution'] is True


def test_a_judge_without_a_resolved_version_refuses_to_exist():
    """An alias alone is not a pinned model. A run that cannot name the exact version it called
    cannot be reproduced or compared."""
    with pytest.raises(ValueError):
        P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='')


# -------------------------------------------------------------------- fail-closed dispatch
def test_a_judge_with_no_transport_refuses_to_dispatch():
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v')
    with pytest.raises(P.DispatchRefused):
        j.transcribe(IMAGE)


def test_dispatch_requires_a_budget_guard():
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v',
                          transport=P.FakeTransport(P.ANTHROPIC_OK_FIXTURE))
    with pytest.raises(P.DispatchRefused):
        j.transcribe(IMAGE)


def test_dispatch_is_refused_when_the_guard_cannot_reserve():
    guard = BudgetGuard(authorised_usd=Decimal('0.01'), spent_usd=Decimal('0.01'))
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v',
                          transport=P.FakeTransport(P.ANTHROPIC_OK_FIXTURE), guard=guard)
    with pytest.raises(BudgetExceeded):
        j.transcribe(IMAGE)


def test_a_refused_reservation_dispatches_nothing():
    guard = BudgetGuard(authorised_usd=Decimal('0.01'), spent_usd=Decimal('0.01'))
    transport = P.FakeTransport(P.ANTHROPIC_OK_FIXTURE)
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v',
                          transport=transport, guard=guard)
    with pytest.raises(BudgetExceeded):
        j.transcribe(IMAGE)
    assert transport.calls == 0


# ------------------------------------------------------------------ fake-transport parsing
def _judge(cls, fixture, alias):
    return cls(model_alias=alias, resolved_version='v',
               transport=P.FakeTransport(fixture),
               guard=BudgetGuard(authorised_usd=Decimal('10.00')))


def test_anthropic_response_preserves_request_id_tokens_and_cost():
    j = _judge(P.AnthropicTextJudge, P.ANTHROPIC_OK_FIXTURE, 'claude-sonnet-5')
    r = j.transcribe(IMAGE)
    assert r.text == 'Flat 50% Off'
    assert r.provider_request_id == 'msg_fake_abc123'
    assert r.input_tokens == 812 and r.output_tokens == 7
    assert r.billed_usd is not None and r.billed_usd > 0
    assert r.api_status == 'ok'


def test_gemini_response_preserves_request_id_tokens_and_cost():
    j = _judge(P.GeminiTextJudge, P.GEMINI_OK_FIXTURE, 'gemini-3.5-flash-lite')
    r = j.transcribe(IMAGE)
    assert r.text == 'Flat 50% Off'
    assert r.provider_request_id == 'gen-req-99'
    assert r.input_tokens == 640 and r.output_tokens == 6
    assert r.billed_usd is not None and r.billed_usd > 0


def test_a_refusal_is_recorded_as_a_refusal_not_a_transcription():
    j = _judge(P.AnthropicTextJudge, P.ANTHROPIC_REFUSAL_FIXTURE, 'claude-sonnet-5')
    r = j.transcribe(IMAGE)
    assert r.api_status == 'refusal'
    assert r.error_class == 'moderation_block'
    assert r.text == ''


def test_an_error_is_recorded_as_an_error_and_still_consumes_its_trial():
    j = _judge(P.AnthropicTextJudge, P.ANTHROPIC_ERROR_FIXTURE, 'claude-sonnet-5')
    r = j.transcribe(IMAGE)
    assert r.api_status == 'error'
    assert r.error_class
    assert r.billed_usd is not None  # a failed call still costs a trial


def test_spend_is_recorded_against_the_guard_after_every_call():
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v',
                          transport=P.FakeTransport(P.ANTHROPIC_OK_FIXTURE), guard=guard)
    j.transcribe(IMAGE)
    assert guard.spent_usd > 0


def test_one_call_is_one_trial_and_there_is_no_retry_path():
    """No adapter method may loop. A refusal returns a record, it does not try again."""
    transport = P.FakeTransport(P.ANTHROPIC_REFUSAL_FIXTURE)
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v',
                          transport=transport, guard=BudgetGuard(authorised_usd=Decimal('10.00')))
    j.transcribe(IMAGE)
    assert transport.calls == 1
    assert not any('retry' in name for name in dir(j))


def test_full_sonnet_plus_gemini_reservation_exceeds_six_dollar_cap():
    calls_per_candidate = 96 * 2 * 3 * 2  # 96 items × 2 shapes × 3 passes × 2 scripts
    anthropic = P.AnthropicTextJudge(
        model_alias='claude-sonnet-5',
        resolved_version='claude-sonnet-5')
    gemini = P.GeminiTextJudge(
        model_alias='gemini-3.5-flash-lite',
        resolved_version='gemini-3.5-flash-lite')
    worst_case = (anthropic._estimate() + gemini._estimate()) * calls_per_candidate
    assert worst_case == Decimal('6.220800')
    # Full Sonnet + Gemini cannot both be re-run under the frozen $6 cap.
    # EMP-001 therefore authorises Sonnet-only continuation after the first run.
    assert worst_case > Decimal('6.00')


def test_sonnet_only_continuation_with_first_run_spend_fits_six_dollar_cap():
    calls = 96 * 2 * 3 * 2
    sonnet = P.AnthropicTextJudge(
        model_alias='claude-sonnet-5', resolved_version='claude-sonnet-5')
    first_run_counted = Decimal('0.0854218')
    cumulative_worst_case = first_run_counted + sonnet._estimate() * calls
    assert cumulative_worst_case == Decimal('5.4307018')
    assert cumulative_worst_case <= Decimal('6.00')


# ------------------------------------------------------------------ persistence shape
def test_a_response_can_be_persisted_with_every_field_the_contract_needs():
    j = _judge(P.AnthropicTextJudge, P.ANTHROPIC_OK_FIXTURE, 'claude-sonnet-5')
    row = j.call_record(j.transcribe(IMAGE), shape='transcribe')
    for key in ('provider', 'model_alias', 'resolved_version', 'shape', 'api_status',
                'error_class', 'provider_request_id', 'input_tokens', 'output_tokens',
                'billed_usd', 'cost_basis', 'retries', 'prompt_sha256'):
        assert key in row, key
    assert row['retries'] == 0
    assert json.dumps(row)  # must be JSON-serialisable for the harness handoff


def test_a_persisted_transcribe_record_does_not_leak_the_target():
    j = _judge(P.AnthropicTextJudge, P.ANTHROPIC_OK_FIXTURE, 'claude-sonnet-5')
    row = j.call_record(j.transcribe(IMAGE), shape='transcribe')
    assert 'target' not in json.dumps(row).lower()


def test_provisional_cost_is_labelled_provisional_not_invoiced():
    j = _judge(P.AnthropicTextJudge, P.ANTHROPIC_OK_FIXTURE, 'claude-sonnet-5')
    row = j.call_record(j.transcribe(IMAGE), shape='transcribe')
    assert row['cost_basis'] == 'provisional_published_rate'


# ------------------------------------------- the blind check must not misfire on short targets
def test_a_short_verdict_target_is_not_falsely_flagged():
    """REGRESSION. The check once counted raw substring hits across the whole serialised body, so
    a one-character target matched inside ordinary structural words like "text" and "type" and a
    perfectly good payload was refused. A control that cries wolf on a short target is a control
    that will be switched off."""
    j = P.AnthropicTextJudge(model_alias='claude-sonnet-5', resolved_version='v')
    for target in ('t', 'A', '20%', 'Aaj ki Deal'):
        assert P.verify_blind_payload(j.build_verdict_request(IMAGE, target),
                                      shape='verdict', target=target) == [], target


def test_a_verdict_payload_carrying_ground_truth_in_a_field_is_flagged():
    """The realistic smuggling vector: the target reaches a verdict payload through the PROMPT and
    through nothing else. A dedicated ground-truth field is how a blind item becomes a sighted
    one, and it is caught by key name rather than by scanning prose."""
    smuggled = {'model': 'x', 'expected_verdict': 'match',
                'input': [{'content': [{'text': 'TARGET: शुभ दीपावली'}]}]}
    assert P.verify_blind_payload(smuggled, shape='verdict', target='शुभ दीपावली')


def test_a_transcribe_payload_carrying_ground_truth_in_a_field_is_flagged():
    smuggled = {'model': 'x', 'rendered_string': 'Flat 5O% Off',
                'input': [{'content': [{'text': 'Transcribe.'}]}]}
    assert P.verify_blind_payload(smuggled, shape='transcribe', target='Flat 50% Off')
