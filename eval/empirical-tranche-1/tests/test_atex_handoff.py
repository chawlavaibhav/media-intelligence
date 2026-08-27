"""Qualification -> A-TEXT handoff controls (EVAL-014 C, D).

`run_atex.py --live` used to refuse unconditionally, so the paid stage could not start no matter
what was supplied. Making it start is only half the job: the other half is making sure it starts
for the RIGHT reasons. A judge that was never qualified, a qualification that was a rehearsal, a
JSON field edited by hand, a script nobody qualified for — each of those must still refuse.

Nothing here contacts a provider. Every transport is an injected recorder.
"""
import json
from decimal import Decimal
from pathlib import Path

import pytest

import providers as P
import qualify_text as Q
import run_atex as R
import human_review as HR
import spend_ledger as SL
from fake_live import FakeFalHttp, FakeJudgeHttp, image_index_for

PKG = Path(__file__).resolve().parents[1]
REGISTRY = PKG.parents[1] / 'eval' / 'registry' / 'registry-v1.jsonl'


@pytest.fixture
def keys(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'fake-anthropic')
    monkeypatch.setenv('GOOGLE_API_KEY', 'fake-google')
    monkeypatch.setenv('FAL_KEY', 'fake-fal')


def _auth(tmp_path):
    p = tmp_path / 'auth.yaml'
    p.write_text("authorised: true\ntranche_id: EMP-001\n"
                 "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    return p


def _run(tmp_path, mode='fake_live', run_id='run-handoff'):
    return SL.TrancheRun.create(root=tmp_path / 'runs', run_id=run_id,
                                authorisation_path=_auth(tmp_path), mode=mode)


def _resolved_perceptibility(tmp_path):
    """A structurally valid rehearsal-only sheet bound to the current frozen pack."""
    p = tmp_path / 'perceptibility-review-REHEARSAL-ONLY.csv'
    pack_sha = HR.pack_sha256()
    rows = ['item_id,visible_difference,usable_surface,reviewer_note']
    for item in Q.load_latin_items():
        visible = 'yes' if item['expected'] == 'mismatch' else ''
        note = f'REHEARSAL FIXTURE - NOT A HUMAN REVIEW; pack_sha256={pack_sha}'
        rows.append(f"{item['item_id']},{visible},yes,{note}")
    p.write_text('\n'.join(rows) + '\n')
    return p


def _qualify(tmp_path, run, scripts=('devanagari', 'latin')):
    """Run a real fake-live qualification for one candidate and persist its result."""
    stage = SL.TrancheBudget(run).stage('qualification')
    version = 'claude-sonnet-5'
    judge = P.AnthropicTextJudge(
        model_alias='claude-sonnet-5', resolved_version=version,
        transport=P.AnthropicHttpTransport(resolved_version=version,
                                        http=FakeJudgeHttp(P.AnthropicTextJudge,
                                                           image_index_for('both'))),
        guard=stage)
    candidate = Q.LiveCandidate(judge=judge, images=Q.ImageResolver())
    result = Q.qualify_candidate(candidate, guard=stage)
    payload = Q.build_qualification_result(run, [result], [candidate])
    return Q.persist_qualification(run, payload), payload


# ------------------------------------------------------------------ persistence + binding
def test_a_qualification_result_is_persisted_into_the_run(tmp_path, keys):
    run = _run(tmp_path)
    path, payload = _qualify(tmp_path, run)
    assert path.exists()
    on_disk = json.loads(path.read_text())
    assert on_disk['run_id'] == run.run_id
    assert on_disk['mode'] == 'fake_live'
    assert on_disk['evidence_fingerprint']


def test_qualification_fingerprint_binds_per_call_outcomes(tmp_path, keys):
    run = _run(tmp_path)
    path, _ = _qualify(tmp_path, run)
    doc = json.loads(path.read_text())
    assert doc['candidates'][0]['devanagari']['observations']
    doc['candidates'][0]['devanagari']['observations'][0]['observed'] = 'tampered'
    path.write_text(json.dumps(doc))

    with pytest.raises(R.GateClosed) as e:
        R.load_qualification(run, expected_mode='fake_live')
    assert 'fingerprint' in str(e.value).lower()


def test_old_contract_evidence_cannot_open_current_handoff(tmp_path, keys):
    run = _run(tmp_path)
    path, payload = _qualify(tmp_path, run)
    payload['contract_version'] = 1
    payload['evidence_fingerprint'] = Q.qualification_fingerprint(payload)
    path.write_text(json.dumps(payload))

    with pytest.raises(R.GateClosed) as e:
        R.load_qualification(run, expected_mode='fake_live')
    assert 'contract version' in str(e.value).lower()


def test_the_handoff_loads_the_persisted_qualification(tmp_path, keys):
    run = _run(tmp_path)
    _qualify(tmp_path, run)
    handoff = R.load_qualification(run, expected_mode='fake_live')
    assert handoff['qualified'][0]['resolved_version'] == 'claude-sonnet-5'
    assert set(handoff['qualified'][0]['qualified_scope']) == {'devanagari', 'latin'}


def test_hand_editing_the_qualified_field_does_not_open_atex(tmp_path, keys):
    """No manual edit of a 'qualified' field may be enough. The fingerprint binds the claim to
    the evidence that produced it."""
    run = _run(tmp_path)
    path, _ = _qualify(tmp_path, run)
    doc = json.loads(path.read_text())
    doc['qualified'][0]['qualified_scope'] = ['devanagari', 'latin', 'martian']
    path.write_text(json.dumps(doc))

    with pytest.raises(R.GateClosed) as e:
        R.load_qualification(run, expected_mode='fake_live')
    assert 'fingerprint' in str(e.value).lower()


def test_a_fabricated_qualification_file_is_rejected(tmp_path, keys):
    run = _run(tmp_path)
    fabricated = {
        'run_id': run.run_id, 'mode': 'live', 'tranche_id': 'EMP-001',
        'evidence_fingerprint': 'deadbeef' * 8,
        'qualified': [{'provider': 'anthropic', 'model_alias': 'claude-sonnet-5',
                       'resolved_version': 'whatever', 'qualified_scope': ['devanagari', 'latin']}],
        'call_records': [],
    }
    (run.evidence_dir / 'qualification-result.json').write_text(json.dumps(fabricated))
    with pytest.raises(R.GateClosed):
        R.load_qualification(run, expected_mode='live')


def test_a_missing_qualification_refuses(tmp_path, keys):
    with pytest.raises(R.GateClosed) as e:
        R.load_qualification(_run(tmp_path), expected_mode='fake_live')
    assert 'qualification' in str(e.value).lower()


# ------------------------------------------------------------------ mode discipline
def test_live_atex_refuses_fake_live_qualification_evidence(tmp_path, keys):
    """The control that stops a rehearsal opening a paid stage."""
    run = _run(tmp_path, mode='fake_live')
    _qualify(tmp_path, run)
    with pytest.raises(R.GateClosed) as e:
        R.load_qualification(run, expected_mode='live')
    assert 'fake_live' in str(e.value)


def test_live_atex_refuses_synthetic_dry_run_evidence(tmp_path, keys):
    run = _run(tmp_path, mode='dry_run')
    (run.evidence_dir / 'qualification-result.json').write_text(json.dumps({
        'run_id': run.run_id, 'mode': 'dry_run', 'tranche_id': 'EMP-001',
        'synthetic': True, 'evidence_fingerprint': 'x', 'qualified': [], 'call_records': []}))
    with pytest.raises(R.GateClosed):
        R.load_qualification(run, expected_mode='live')


# ------------------------------------------------------------------ scope + binding
def test_a_judge_qualified_only_on_devanagari_cannot_open_atex(tmp_path, keys):
    run = _run(tmp_path)
    path, payload = _qualify(tmp_path, run)
    # Re-derive honestly: narrow the scope AND re-fingerprint, as a real partial run would.
    payload['qualified'][0]['qualified_scope'] = ['devanagari']
    payload['evidence_fingerprint'] = Q.qualification_fingerprint(payload)
    path.write_text(json.dumps(payload))

    with pytest.raises(R.GateClosed) as e:
        R.select_judge_for_atex(R.load_qualification(run, expected_mode='fake_live'))
    assert 'latin' in str(e.value).lower()


def test_the_selected_judge_binds_to_the_exact_qualified_version(tmp_path, keys):
    run = _run(tmp_path)
    _qualify(tmp_path, run)
    chosen = R.select_judge_for_atex(R.load_qualification(run, expected_mode='fake_live'))
    assert chosen['provider'] == 'anthropic'
    assert chosen['resolved_version'] == 'claude-sonnet-5'
    assert chosen['model_alias'] == 'claude-sonnet-5'


def test_old_openai_qualification_cannot_open_atex_after_roster_switch(tmp_path, keys):
    run = _run(tmp_path)
    payload = {
        'run_id': run.run_id, 'mode': 'fake_live', 'tranche_id': 'EMP-001',
        'synthetic': False,
        'qualified': [{
            'candidate': 'openai:gpt-5.4-mini',
            'provider': 'openai',
            'model_alias': 'gpt-5.4-mini',
            'resolved_version': 'gpt-5.4-mini-2026-03-17',
            'qualified_scope': ['devanagari', 'latin'],
        }],
        'candidates': [],
        'call_records': [],
        'contract_version': Q.contract().get('contract_version'),
        'contract_sha256': __import__('hashlib').sha256(Q.CONTRACT.read_bytes()).hexdigest(),
    }
    payload['evidence_fingerprint'] = Q.qualification_fingerprint(payload)
    (run.evidence_dir / 'qualification-result.json').write_text(json.dumps(payload))

    loaded = R.load_qualification(run, expected_mode='fake_live')
    with pytest.raises(R.GateClosed):
        R.select_judge_for_atex(loaded)


def test_no_qualified_candidate_at_all_refuses(tmp_path, keys):
    run = _run(tmp_path)
    payload = {'run_id': run.run_id, 'mode': 'fake_live', 'tranche_id': 'EMP-001',
               'qualified': [], 'candidates': [], 'call_records': [], 'synthetic': False,
               'contract_version': Q.contract().get('contract_version'),
               'contract_sha256': __import__('hashlib').sha256(Q.CONTRACT.read_bytes()).hexdigest()}
    payload['evidence_fingerprint'] = Q.qualification_fingerprint(payload)
    (run.evidence_dir / 'qualification-result.json').write_text(json.dumps(payload))
    with pytest.raises(R.GateClosed):
        R.select_judge_for_atex(R.load_qualification(run, expected_mode='fake_live'))


# ------------------------------------------------------------------ Latin perceptibility gate
def test_the_committed_perceptibility_sheet_is_now_resolved():
    assert R.latin_perceptibility_resolved(
        PKG / 'text_qualification' / 'perceptibility-review.csv') is True


def test_atex_refuses_while_an_explicit_perceptibility_sheet_is_unresolved(tmp_path, keys):
    run = _run(tmp_path)
    _qualify(tmp_path, run)
    p = tmp_path / 'unresolved.csv'
    p.write_text('item_id,visible_difference,usable_surface,reviewer_note\n')
    with pytest.raises(R.GateClosed) as e:
        R.run_live(run, mode='fake_live', judge_http=FakeJudgeHttp(P.AnthropicTextJudge, {}),
                   fal_http=FakeFalHttp(), artifact_fetch=lambda u: b'x',
                   perceptibility_path=p)
    assert 'perceptibility' in str(e.value).lower()


def test_a_resolved_sheet_opens_the_gate(tmp_path, keys):
    assert R.latin_perceptibility_resolved(_resolved_perceptibility(tmp_path)) is True


def test_a_partially_filled_sheet_does_not_open_the_gate(tmp_path):
    p = tmp_path / 'partial.csv'
    p.write_text('item_id,visible_difference,usable_surface,reviewer_note\n'
                 'lx-0000,yes,yes,\nlx-0001,,,\n')
    assert R.latin_perceptibility_resolved(p) is False


# ------------------------------------------------------------------ the executable handoff
def test_the_full_fake_live_handoff_runs_atex_end_to_end(tmp_path, keys):
    run = _run(tmp_path)
    _qualify(tmp_path, run)
    fal_http = FakeFalHttp()
    judge_http = FakeJudgeHttp(P.AnthropicTextJudge, {})

    result = R.run_live(run, mode='fake_live', judge_http=judge_http, fal_http=fal_http,
                        artifact_fetch=lambda url: b'\x89PNG\r\n\x1a\n' + url.encode(),
                        perceptibility_path=_resolved_perceptibility(tmp_path))

    assert result['generations'] == 16
    assert result['per_route'] == {'IMG-01': 8, 'IMG-02': 8}
    assert len(fal_http.calls) == 16
    assert result['synthetic'] is False
    assert result['retries'] == 0
    assert result['registry_rows_written'] == 0
    assert result['evidence_class'] == 'partial_admission_screen_only'


def test_the_handoff_uses_the_same_persistent_tranche_budget(tmp_path, keys):
    run = _run(tmp_path)
    _qualify(tmp_path, run)
    qualification_spend = SL.TrancheBudget(run).stage_spent_usd('qualification')
    assert qualification_spend > 0

    R.run_live(run, mode='fake_live', judge_http=FakeJudgeHttp(P.AnthropicTextJudge, {}),
               fal_http=FakeFalHttp(), artifact_fetch=lambda u: b'\x89PNG\r\n\x1a\n' + u.encode(),
               perceptibility_path=_resolved_perceptibility(tmp_path))

    budget = SL.TrancheBudget(SL.TrancheRun.open(root=tmp_path / 'runs', run_id='run-handoff'))
    assert budget.stage_spent_usd('qualification') == qualification_spend  # unchanged
    assert budget.stage_spent_usd('atex') > 0
    assert budget.spent_usd() <= Decimal('10.00')


def test_generation_and_evaluator_calls_are_separately_costed(tmp_path, keys):
    run = _run(tmp_path)
    _qualify(tmp_path, run)
    result = R.run_live(run, mode='fake_live', judge_http=FakeJudgeHttp(P.AnthropicTextJudge, {}),
                        fal_http=FakeFalHttp(),
                        artifact_fetch=lambda u: b'\x89PNG\r\n\x1a\n' + u.encode(),
                        perceptibility_path=_resolved_perceptibility(tmp_path))

    gen_refs = {a['cost_ref'] for a in result['attempts']}
    eval_refs = {e['cost_ref'] for e in result['evaluator_calls']}
    assert len(gen_refs) == 16
    assert len(eval_refs) == 16
    assert not (gen_refs & eval_refs)          # never the same cost record
    ledger_refs = {r.get('cost_ref') for r in SL.TrancheBudget(run).records()}
    assert (gen_refs | eval_refs) <= ledger_refs


def test_atex_is_refused_when_the_tranche_headroom_is_gone(tmp_path, keys):
    run = _run(tmp_path)
    _qualify(tmp_path, run)
    # Burn the remaining tranche headroom on a correction, then try to generate.
    budget = SL.TrancheBudget(run)
    budget.correct(stage='atex', amount_usd=budget.remaining_usd(), reason='rehearsal burn')

    with pytest.raises(Exception) as e:
        R.run_live(run, mode='fake_live', judge_http=FakeJudgeHttp(P.AnthropicTextJudge, {}),
                   fal_http=FakeFalHttp(),
                   artifact_fetch=lambda u: b'\x89PNG\r\n\x1a\n' + u.encode(),
                   perceptibility_path=_resolved_perceptibility(tmp_path))
    assert 'ceiling' in str(e.value).lower() or 'exceed' in str(e.value).lower()


def test_the_registry_is_untouched_by_the_handoff(tmp_path, keys):
    before = REGISTRY.read_bytes()
    run = _run(tmp_path)
    _qualify(tmp_path, run)
    R.run_live(run, mode='fake_live', judge_http=FakeJudgeHttp(P.AnthropicTextJudge, {}),
               fal_http=FakeFalHttp(), artifact_fetch=lambda u: b'\x89PNG\r\n\x1a\n' + u.encode(),
               perceptibility_path=_resolved_perceptibility(tmp_path))
    assert REGISTRY.read_bytes() == before


# ------------------------------------------------------------------ E14-D blindness parity
def test_atex_passes_the_target_only_as_an_evaluator_side_blind_check(tmp_path, keys):
    """The target must reach the blind check and never the payload."""
    seen = {}

    class Recorder:
        provider, model_alias, resolved_version = 'openai', 'a', 'v'

        def transcribe(self, image_bytes, blind_check_target=''):
            seen['target'] = blind_check_target
            return P.EvaluatorResponse('x', 1, 1, Decimal('0.001'), 'r')

        def identity(self):
            return {'provider': 'anthropic', 'model_alias': 'a', 'resolved_version': 'v',
                    'version_pinned_at_execution': True}

        def call_record(self, response, shape):
            return {**self.identity(), 'shape': shape, 'api_status': response.api_status,
                    'error_class': None, 'provider_request_id': 'r', 'input_tokens': 1,
                    'output_tokens': 1, 'billed_usd': '0.001', 'cost_basis': 'x', 'retries': 0}

    item = R.items()[0]
    R._measure_artifact(Recorder(), b'img', item, 1, 'attempt-1')
    assert seen['target'] == item['target_string']


@pytest.mark.parametrize('item_index,script', [(0, 'devanagari'), (2, 'latin')])
def test_a_leaking_atex_transcribe_is_refused_for_both_scripts(tmp_path, keys, item_index, script):
    """E14-D negative control, on a Devanagari item AND a Latin one."""
    run = _run(tmp_path)
    stage = SL.TrancheBudget(run).stage('atex')
    item = R.items()[item_index]
    target = item['target_string']

    judge = P.AnthropicTextJudge(
        model_alias='a', resolved_version='v',
        transport=P.AnthropicHttpTransport(resolved_version='v',
                                        http=FakeJudgeHttp(P.AnthropicTextJudge, {})),
        guard=stage)
    judge.build_transcribe_request = lambda b: {'model': 'v', 'input': [
        {'role': 'user', 'content': [{'type': 'input_text', 'text': f'TARGET: {target}'}]}]}

    with pytest.raises(P.BlindnessViolation):
        R._measure_artifact(judge, b'img', item, 1, 'attempt-1')
