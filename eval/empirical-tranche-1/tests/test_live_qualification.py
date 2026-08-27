"""POSITIVE fake-live qualification controls (EVAL-013 A + E).

EVAL-012 proved refusal exhaustively and never proved the inverse. `qualify_text.py --live`
opened a valid guard and then unconditionally raised, so the real judges never participated in
the protocol at all — only `FakeCandidate` did.

These tests drive the REAL `AnthropicTextJudge` / `GeminiTextJudge` through the REAL transports and
the REAL scoring path. The only thing replaced is the socket: an injected recorder stands exactly
where the network would be, decodes the base64 image out of the request body, and answers from a
lookup table built from the real rendered pack — which is what a judge does, minus the model.

Every test here FAILS if the live branch refuses. That is the point: a positive control that would
still pass against an unconditional refusal is not a control.
"""
import json
from types import SimpleNamespace
from decimal import Decimal
from pathlib import Path

import pytest

import providers as P
import qualify_text as Q
from budget_guard import BudgetExceeded, BudgetGuard, NotAuthorised
from fake_live import FakeJudgeHttp, image_index_for

PKG = Path(__file__).resolve().parents[1]

ANTHROPIC_VERSION = 'claude-sonnet-5'
GEMINI_VERSION = 'gemini-3.5-flash-lite-001'

CALLS_PER_SCRIPT = 576          # 96 items x 2 shapes x 3 passes


@pytest.fixture
def keys(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-ant-test-key')
    monkeypatch.setenv('GOOGLE_API_KEY', 'AIza-test-google-key')


def _authorisation(tmp_path):
    p = tmp_path / 'authorization.local.yaml'
    p.write_text("authorised: true\ntranche_id: EMP-001\n"
                 "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n"
                 "approved_by: controller-test\napproved_at: '2026-08-26'\n")
    return p


def _anthropic_judge(http, guard):
    return P.AnthropicTextJudge(
        model_alias='claude-sonnet-5', resolved_version=ANTHROPIC_VERSION,
        transport=P.AnthropicHttpTransport(resolved_version=ANTHROPIC_VERSION, http=http), guard=guard)


def _gemini_judge(http, guard):
    return P.GeminiTextJudge(
        model_alias='gemini-3.5-flash-lite', resolved_version=GEMINI_VERSION,
        transport=P.GeminiHttpTransport(resolved_version=GEMINI_VERSION, http=http), guard=guard)


# --------------------------------------------------------- images resolve from the real packs
def test_the_resolver_supplies_real_rendered_bytes_for_both_scripts():
    r = Q.ImageResolver()
    dev = Q.load_devanagari_items()[0]
    lat = Q.load_latin_items()[0]
    assert r.bytes_for('devanagari', dev['item_id']).startswith(b'\x89PNG')
    assert r.bytes_for('latin', lat['item_id']).startswith(b'\x89PNG')


def test_the_resolver_verifies_the_committed_image_hash():
    """The checker contract says: resolve the path, read the file, confirm the hash before
    sending anything. A judge scored against different bytes than we think we sent is worthless."""
    r = Q.ImageResolver()
    dev = Q.load_devanagari_items()[0]
    assert r.verified('devanagari', dev['item_id']) is True


def test_the_resolver_refuses_bytes_whose_hash_does_not_match(tmp_path):
    r = Q.ImageResolver()
    with pytest.raises(Q.ImageIntegrityError):
        r.verify_bytes('devanagari', Q.load_devanagari_items()[0]['item_id'], b'not-the-image')


# ------------------------------------------------- POSITIVE CONTROL 1: exactly one dispatch
def test_one_live_evaluator_call_dispatches_exactly_once_and_is_not_synthetic(keys):
    """E13-E(1). Valid budget + fake live transport -> one dispatch, non-synthetic record."""
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('latin'))
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    candidate = Q.LiveCandidate(judge=_anthropic_judge(http, guard), images=Q.ImageResolver())

    item = Q._script_items('latin')[0]
    reply = candidate.call('latin', item, 'transcribe', 0)

    assert len(http.calls) == 1
    assert reply['api_status'] == 'ok'
    assert reply['call_record']['synthetic'] is False
    assert reply['call_record']['model_alias'] == 'claude-sonnet-5'
    assert reply['call_record']['resolved_version'] == ANTHROPIC_VERSION
    assert guard.spent_usd > 0


def test_the_live_candidate_declares_itself_not_synthetic(keys):
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('latin'))
    c = Q.LiveCandidate(judge=_anthropic_judge(http, BudgetGuard(authorised_usd=Decimal('10.00'))),
                        images=Q.ImageResolver())
    assert c.synthetic is False


# ------------------------------------------------- POSITIVE CONTROL 2: Gemini header + dispatch
def test_a_live_gemini_call_uses_x_goog_api_key_and_dispatches_once(keys):
    """E13-E(2)."""
    http = FakeJudgeHttp(P.GeminiTextJudge, image_index_for('latin'))
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    candidate = Q.LiveCandidate(judge=_gemini_judge(http, guard), images=Q.ImageResolver())

    candidate.call('latin', Q._script_items('latin')[0], 'transcribe', 0)

    assert len(http.calls) == 1
    assert http.calls[0]['headers']['x-goog-api-key'] == 'AIza-test-google-key'
    assert 'Authorization' not in http.calls[0]['headers']


# ------------------------------------------------- the blind payload survives the live path
def _all_strings(obj):
    """Every string in a parsed body, so an escaped leak cannot hide from the scan."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _all_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _all_strings(v)


def test_a_live_transcribe_dispatch_carries_no_devanagari_in_its_body(keys):
    """Blindness must survive all the way to the wire, not just to the request builder.

    Scanned on the PARSED body, not the raw bytes. An earlier version of this test scanned the raw
    text while the transport was serialising with ensure_ascii=True, so a leaked Devanagari target
    would have travelled as \\uXXXX and the check would have passed while blind. The transport now
    emits real UTF-8 and the scan parses first; between them a leak has nowhere to hide.
    """
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('devanagari'))
    candidate = Q.LiveCandidate(
        judge=_anthropic_judge(http, BudgetGuard(authorised_usd=Decimal('10.00'))),
        images=Q.ImageResolver())
    item = Q._script_items('devanagari')[0]
    candidate.call('devanagari', item, 'transcribe', 0)

    parsed = json.loads(http.calls[0]['body'].decode('utf-8'))
    for value in _all_strings(parsed):
        assert not any('ऀ' <= ch <= 'ॿ' for ch in value)
        assert item['target'] not in value


def test_the_wire_body_is_utf8_not_ascii_escaped(keys):
    """The property the blind scan depends on. If this regresses, blindness goes unwatched."""
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('devanagari'))
    candidate = Q.LiveCandidate(
        judge=_anthropic_judge(http, BudgetGuard(authorised_usd=Decimal('10.00'))),
        images=Q.ImageResolver())
    item = Q._script_items('devanagari')[0]
    candidate.call('devanagari', item, 'verdict', 0)
    assert item['target'].encode('utf-8') in http.calls[0]['body']


def test_the_blind_scan_would_catch_an_escaped_leak():
    """NEGATIVE CONTROL on the control itself.

    Feed verify_blind_payload a payload whose target arrived ASCII-escaped. If the checker only
    looked at raw serialised text it would miss this, and every blindness claim in the suite would
    be worthless.
    """
    target = 'शुभ दीपावली'
    leaking = json.loads(json.dumps({'model': 'x', 'input': [{'text': f'TARGET: {target}'}]},
                                    ensure_ascii=True))
    assert P.verify_blind_payload(leaking, shape='transcribe', target=target)


def test_a_live_verdict_dispatch_does_carry_the_target(keys):
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('devanagari'))
    candidate = Q.LiveCandidate(
        judge=_anthropic_judge(http, BudgetGuard(authorised_usd=Decimal('10.00'))),
        images=Q.ImageResolver())
    item = Q._script_items('devanagari')[0]
    candidate.call('devanagari', item, 'verdict', 0)
    assert item['target'] in http.calls[0]['body'].decode('utf-8')


# ------------------------------------------------- POSITIVE CONTROL: the whole protocol runs
def test_a_faithful_fake_live_candidate_completes_both_scripts(keys):
    """The full progressive protocol, driven through the real judge, transport and scorer."""
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('both'))
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    candidate = Q.LiveCandidate(judge=_anthropic_judge(http, guard), images=Q.ImageResolver())

    result = Q.qualify_candidate(candidate, guard=guard)

    assert result['devanagari']['calls'] == CALLS_PER_SCRIPT
    assert result['latin']['calls'] == CALLS_PER_SCRIPT
    assert len(http.calls) == 2 * CALLS_PER_SCRIPT
    assert result['qualified_scope'] == ['devanagari', 'latin']
    assert result['synthetic'] is False
    assert result['may_populate_registry'] is False


def test_a_live_candidate_that_false_passes_stops_before_latin(keys):
    """The progressive stop must hold on the LIVE path too, not only for FakeCandidate."""
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('both'), false_pass_on_first_mismatch=True)
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    candidate = Q.LiveCandidate(judge=_anthropic_judge(http, guard), images=Q.ImageResolver())

    result = Q.qualify_candidate(candidate, guard=guard)

    assert result['devanagari']['calls'] == CALLS_PER_SCRIPT
    assert result['latin'] is None
    assert len(http.calls) == CALLS_PER_SCRIPT      # zero Latin dispatches
    assert result['synthetic'] is False


def test_every_live_call_record_pins_alias_and_resolved_version(keys):
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('both'))
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    candidate = Q.LiveCandidate(judge=_anthropic_judge(http, guard), images=Q.ImageResolver())
    result = Q.qualify_candidate(candidate, guard=guard)

    records = result['devanagari']['call_records']
    assert len(records) == CALLS_PER_SCRIPT
    assert {r['resolved_version'] for r in records} == {ANTHROPIC_VERSION}
    assert {r['model_alias'] for r in records} == {'claude-sonnet-5'}
    assert all(r['retries'] == 0 for r in records)
    assert all(r['synthetic'] is False for r in records)


# ------------------------------------------------- NEGATIVE TWINS
def test_budget_exhaustion_stops_the_live_run_with_zero_further_dispatches(keys):
    """E13-E(5)."""
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('both'))
    tiny = BudgetGuard(authorised_usd=Decimal('0.02'))
    candidate = Q.LiveCandidate(judge=_anthropic_judge(http, tiny), images=Q.ImageResolver())

    result = Q.qualify_candidate(candidate, guard=tiny)

    assert result['stopped_reason'] == 'budget_exhausted'
    assert result['qualified_scope'] == []
    assert len(http.calls) < CALLS_PER_SCRIPT
    assert tiny.spent_usd <= tiny.authorised_usd
    dispatched = len(http.calls)
    with pytest.raises(BudgetExceeded):
        tiny.reserve(Decimal('1.00'))
    assert len(http.calls) == dispatched          # the refusal dispatched nothing


def test_a_refusing_live_judge_is_never_retried(keys):
    """E13-E(8)."""
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('devanagari'), refuse_all=True)
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    candidate = Q.LiveCandidate(judge=_anthropic_judge(http, guard), images=Q.ImageResolver())

    result = Q.qualify_candidate(candidate, guard=guard)

    assert len(http.calls) == CALLS_PER_SCRIPT    # not one more
    assert result['devanagari']['refusals'] == CALLS_PER_SCRIPT
    assert 'refusal_rate' in result['devanagari']['failed_gates']
    assert result['latin'] is None
    assert all(r['retries'] == 0 for r in result['devanagari']['call_records'])


def test_a_refusal_still_costs_its_trial(keys):
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('latin'), refuse_all=True)
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    candidate = Q.LiveCandidate(judge=_anthropic_judge(http, guard), images=Q.ImageResolver())
    reply = candidate.call('latin', Q._script_items('latin')[0], 'transcribe', 0)

    assert reply['api_status'] == 'refusal'
    assert guard.spent_usd > 0
    assert reply['call_record']['billed_usd'] is not None


def test_run_live_persists_canonical_fingerprint_bound_qualification(tmp_path, keys):
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('both'))
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    run = SimpleNamespace(run_id='canonical-live-test', mode='live', evidence_dir=tmp_path)

    result = Q.run_live(
        guard,
        http=http,
        resolved_versions={'anthropic': ANTHROPIC_VERSION},
        only_provider='anthropic',
        run=run)

    path = tmp_path / Q.QUALIFICATION_FILENAME
    assert path.exists()
    payload = json.loads(path.read_text())
    assert payload['contract_version'] == 2
    assert payload['contract_sha256']
    assert payload['candidates'][0]['devanagari']['observations']
    assert payload['qualified'][0]['qualified_scope'] == ['devanagari', 'latin']
    assert payload['evidence_fingerprint'] == Q.qualification_fingerprint(payload)
    assert result['qualified_candidates'] == [f'anthropic:{ANTHROPIC_VERSION}']


# ------------------------------------------------- CLI still fails closed
def test_cli_live_refuses_without_authorisation():
    with pytest.raises(NotAuthorised):
        Q.main(['--live'])


def test_cli_live_refuses_a_ceiling_above_the_proposal(tmp_path):
    p = tmp_path / 'auth.yaml'
    p.write_text("authorised: true\ntranche_id: EMP-001\n"
                 "max_consumed_api_spend_usd: 999\nretries_authorised: 0\n")
    with pytest.raises(NotAuthorised):
        Q.main(['--live', '--authorisation', str(p)])


def test_cli_fake_live_runs_the_real_orchestration_without_a_network(monkeypatch, tmp_path, keys):
    """The runnable proof: same orchestration, injected recorder instead of a socket."""
    import socket

    def explode(*a, **k):
        raise AssertionError('fake-live qualification attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)

    out = tmp_path / 'fake-live.json'
    assert Q.main(['--fake-live', '--authorisation', str(_authorisation(tmp_path)),
                   '--out', str(out)]) == 0

    r = json.loads(out.read_text())
    assert r['mode'] == 'fake_live'
    assert r['external_calls'] == 0
    assert r['spend_usd'] == '0'
    assert r['synthetic'] is False
    assert r['registry_rows_written'] == 0
    assert r['dispatches'] > 0
    assert r['candidates'][0]['devanagari']['calls'] == CALLS_PER_SCRIPT


def test_cli_fake_live_honors_anthropic_only_provider(monkeypatch, tmp_path, keys):
    import socket

    def explode(*a, **k):
        raise AssertionError('fake-live qualification attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)

    out = tmp_path / 'fake-live-anthropic-only.json'
    assert Q.main(['--fake-live', '--only-provider', 'anthropic',
                   '--authorisation', str(_authorisation(tmp_path)),
                   '--out', str(out)]) == 0

    r = json.loads(out.read_text())
    assert r['selected_providers'] == ['anthropic']
    assert len(r['candidates']) == 1
    assert r['candidates'][0]['candidate'].startswith('anthropic:')
    assert r['dispatches'] == 2 * CALLS_PER_SCRIPT
    assert r['maximum_evaluator_calls_if_all_survive'] == 2 * CALLS_PER_SCRIPT


def test_fake_live_records_are_not_labeled_synthetic(tmp_path, keys):
    """E13-E(6). Real/non-dry-run evidence must never be labeled synthetic."""
    out = tmp_path / 'fake-live.json'
    Q.main(['--fake-live', '--authorisation', str(_authorisation(tmp_path)), '--out', str(out)])
    r = json.loads(out.read_text())
    assert all(c['synthetic'] is False for c in r['candidates'])


def test_dry_run_is_still_synthetic_and_untouched(tmp_path):
    out = tmp_path / 'dry.json'
    Q.main(['--dry-run', '--out', str(out)])
    r = json.loads(out.read_text())
    assert r['synthetic'] is True
    assert all(c['synthetic'] is True for c in r['candidates'])


# ------------------------------------------- the blind check runs BEFORE the wire, every time
def test_a_leaking_transcribe_request_is_refused_before_dispatch(keys):
    """The checker contract says the blind check must run and return no violations before ANY
    call is made. On the live path it must therefore be enforced in the code, not only asserted
    in a test — a leak that reaches the wire has already destroyed the measurement.
    """
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('devanagari'))
    judge = _anthropic_judge(http, BudgetGuard(authorised_usd=Decimal('10.00')))
    target = Q._script_items('devanagari')[0]['target']

    # Simulate the leak this guard exists to catch: a builder that appends the target.
    def leaking(image_bytes):
        return {'model': ANTHROPIC_VERSION,
                'input': [{'role': 'user', 'content': [
                    {'type': 'input_text', 'text': f'Transcribe. TARGET: {target}'}]}]}

    judge.build_transcribe_request = leaking

    with pytest.raises(P.BlindnessViolation) as e:
        judge.transcribe(b'anything')

    assert http.calls == []               # nothing reached the wire
    assert 'devanagari' in str(e.value).lower() or 'target' in str(e.value).lower()


def test_a_leaking_request_costs_nothing_because_it_never_dispatched(keys):
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('devanagari'))
    judge = _anthropic_judge(http, guard)
    target = Q._script_items('devanagari')[0]['target']
    judge.build_transcribe_request = lambda b: {'model': ANTHROPIC_VERSION, 'input': [
        {'role': 'user', 'content': [{'type': 'input_text', 'text': target}]}]}

    with pytest.raises(P.BlindnessViolation):
        judge.transcribe(b'anything')
    assert guard.spent_usd == Decimal('0')


def test_a_verdict_request_that_lost_its_target_is_also_refused(keys):
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('devanagari'))
    judge = _anthropic_judge(http, BudgetGuard(authorised_usd=Decimal('10.00')))
    judge.build_verdict_request = lambda b, t: {'model': ANTHROPIC_VERSION, 'input': [
        {'role': 'user', 'content': [{'type': 'input_text', 'text': 'Does it match?'}]}]}

    with pytest.raises(P.BlindnessViolation):
        judge.verdict(b'anything', 'शुभ दीपावली')
    assert http.calls == []


def test_the_ordinary_live_path_passes_the_blind_check_every_call(keys):
    """The guard must not be so strict that the real path cannot run."""
    http = FakeJudgeHttp(P.AnthropicTextJudge, image_index_for('both'))
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))
    candidate = Q.LiveCandidate(judge=_anthropic_judge(http, guard), images=Q.ImageResolver())
    result = Q.qualify_candidate(candidate, guard=guard)
    assert result['devanagari']['calls'] == CALLS_PER_SCRIPT
    assert result['latin']['calls'] == CALLS_PER_SCRIPT
