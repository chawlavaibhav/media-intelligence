"""POSITIVE fake-live A-TEXT controls (EVAL-013 C, D + E).

EVAL-012 shipped a real defect here, not merely a gap: `run_atex.run` called `_fake_transcribe`
and stamped `synthetic: true` regardless of `dry_run`. A genuinely paid run would therefore have
been scored by a stub that reads its own generator's payload, and then filed as synthetic — spend
with no measurement, mislabelled so nobody could tell.

These tests drive the real fal route adapters and the real judge through injected recorders, and
they assert on the thing that was wrong: that non-dry-run evidence is measured by the qualified
blind judge and is NOT labelled synthetic.
"""
import json
from decimal import Decimal
from pathlib import Path

import pytest

import providers as P
import run_atex as R
from budget_guard import BudgetExceeded, BudgetGuard
from fake_live import FakeFalHttp

PKG = Path(__file__).resolve().parents[1]
REGISTRY = PKG.parents[1] / 'eval' / 'registry' / 'registry-v1.jsonl'

QUALIFIED = {'candidate': 'fake-live-judge', 'qualified_scope': ['devanagari', 'latin'],
             'synthetic': False}


@pytest.fixture
def fal_key(monkeypatch):
    monkeypatch.setenv('FAL_KEY', 'fal-test-key-123')


@pytest.fixture
def auth(tmp_path):
    """A VALID authorisation. Supplying one is part of the positive control: the live path must
    demand it, and these tests must therefore satisfy it rather than route around it."""
    p = tmp_path / 'authorization.local.yaml'
    p.write_text("authorised: true\ntranche_id: EMP-001\n"
                 "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n"
                 "approved_by: eval-013-test\napproved_at: '2026-08-26'\n")
    return p


class FakeArtifacts:
    """Injected artifact store. Maps a url to deterministic bytes; opens no socket."""

    def __init__(self):
        self.fetched = []

    def __call__(self, url):
        self.fetched.append(url)
        return b'\x89PNG\r\n\x1a\n' + url.encode('utf-8')


class ScriptedJudge:
    """A stand-in for a QUALIFIED judge. Records every dispatch; never loops."""

    provider = 'openai'
    model_alias = 'gpt-5.4-mini'
    resolved_version = 'gpt-5.4-mini-2026-07-01'

    def __init__(self, reply_for=None, refuse_every=0, error_every=0):
        self.reply_for = reply_for or (lambda img: '')
        self.refuse_every = refuse_every
        self.error_every = error_every
        self.transcribe_calls = 0
        self.verdict_calls = 0

    def _resp(self, text, status='ok', error_class=None):
        return P.EvaluatorResponse(text=text, input_tokens=800, output_tokens=6,
                                   billed_usd=Decimal('0.0021'),
                                   provider_request_id=f'judge-{self.transcribe_calls:04d}',
                                   api_status=status, error_class=error_class)

    def transcribe(self, image_bytes):
        self.transcribe_calls += 1
        n = self.transcribe_calls
        if self.refuse_every and n % self.refuse_every == 0:
            return self._resp('', 'refusal', 'moderation_block')
        if self.error_every and n % self.error_every == 0:
            return self._resp('', 'error', 'internal_error')
        return self._resp(self.reply_for(image_bytes))

    def verdict(self, image_bytes, target):
        self.verdict_calls += 1
        return self._resp('MATCH')

    def identity(self):
        return {'provider': self.provider, 'model_alias': self.model_alias,
                'resolved_version': self.resolved_version, 'version_pinned_at_execution': True}

    def call_record(self, response, shape):
        return {**self.identity(), 'shape': shape, 'api_status': response.api_status,
                'error_class': response.error_class,
                'provider_request_id': response.provider_request_id,
                'input_tokens': response.input_tokens, 'output_tokens': response.output_tokens,
                'billed_usd': str(response.billed_usd), 'cost_basis': response.cost_basis,
                'retries': 0, 'one_call_one_trial': True}


def _routes(http, artifacts):
    cfg = R.config()
    return {slot: P.fal_route_for(slot, cfg, http=http, artifact_fetch=artifacts)
            for slot in cfg['atex']['slots']}


def _perfect_judge():
    """Reads back exactly the target the generator was asked for — a perfect reader."""
    targets = {i['item_id']: i['target_string'] for i in R.items()}

    def reply(image_bytes):
        url = image_bytes.split(b'\x1a\n', 1)[1].decode('utf-8')
        return R._TARGET_BY_ARTIFACT.get(url, '')

    return ScriptedJudge(reply_for=reply), targets


# ------------------------------------------------ POSITIVE CONTROL 3: full fake-live A-TEXT
def test_a_fake_live_run_makes_exactly_sixteen_generations_and_is_not_synthetic(fal_key, auth):
    """E13-E(3)."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    guard = BudgetGuard(authorised_usd=Decimal('10.00'))

    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=guard, dry_run=False, authorisation_path=auth)

    assert len(http.calls) == 16
    assert result['generations'] == 16
    assert result['per_route'] == {'IMG-01': 8, 'IMG-02': 8}
    assert result['synthetic'] is False
    assert result['retries'] == 0
    assert all(a['synthetic'] is False for a in result['attempts'])
    assert all(m['synthetic'] is False for m in result['measurements'])


def test_a_fake_live_run_is_measured_by_the_judge_not_by_a_stub(fal_key, auth):
    """The B3 defect, asserted directly."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()

    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)

    assert judge.transcribe_calls == 16
    assert artifacts.fetched and len(artifacts.fetched) == 16
    assert all(m['shape'] == 'transcribe' and m['role'] == 'primary'
               for m in result['measurements'])


def test_a_perfect_reader_scores_every_frozen_item_as_an_exact_match(fal_key, auth):
    """If the code comparison were broken, a perfect reader would still not score 16."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)
    assert result['exact_matches'] == 16
    assert result['scoreable_opportunities'] == 16


def test_a_judge_that_misreads_scores_zero_and_the_stop_rule_becomes_eligible(fal_key, auth):
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge = ScriptedJudge(reply_for=lambda b: 'completely different text')
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)
    assert result['exact_matches'] == 0
    assert result['text_specific_stop_eligible'] is True


def test_the_stop_rule_is_not_eligible_when_anything_matched(fal_key, auth):
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)
    assert result['text_specific_stop_eligible'] is False


# --------------------------------------------------- generation and evaluator trials stay apart
def test_a_refused_generation_persists_with_no_evaluator_call(fal_key, auth):
    http, artifacts = FakeFalHttp(refuse_every=4), FakeArtifacts()
    judge, _ = _perfect_judge()
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)

    refused = [a for a in result['attempts'] if a['api_status'] == 'refusal']
    assert len(refused) == 4
    assert all(a['cost_ref'] for a in refused)
    assert result['generations'] == 16
    assert judge.transcribe_calls == 12          # no artifact, no evaluator call
    absent = [m for m in result['measurements'] if m['absent_reason'] == 'no_artifact_produced']
    assert len(absent) == 4


def test_an_evaluator_refusal_preserves_both_trials_separately(fal_key, auth):
    """E13-D: generation succeeded and the judge declined. Two trials, two costs, one absence."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge = ScriptedJudge(reply_for=lambda b: 'x', refuse_every=4)
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)

    assert result['generations'] == 16
    assert len(result['evaluator_calls']) == 16
    refused_eval = [e for e in result['evaluator_calls'] if e['api_status'] == 'refusal']
    assert len(refused_eval) == 4
    assert all(e['billed_usd'] for e in refused_eval)
    absent = [m for m in result['measurements'] if m['absent_reason'] == 'evaluator_refused']
    assert len(absent) == 4
    assert result['scoreable_opportunities'] == 12


def test_an_evaluator_error_is_not_scored_as_a_mismatch(fal_key, auth):
    """A judge that failed to answer did not say 'wrong'. Folding them corrupts the numerator."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge = ScriptedJudge(reply_for=lambda b: 'x', error_every=4)
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)
    absent = [m for m in result['measurements'] if m['absent_reason'] == 'evaluator_error']
    assert len(absent) == 4
    assert all(m['exact_match'] is None for m in absent)


def test_every_generation_and_every_evaluator_call_is_its_own_trial(fal_key, auth):
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)
    assert len({a['trial_id'] for a in result['attempts']}) == 16
    assert len({e['evaluator_trial_id'] for e in result['evaluator_calls']}) == 16
    gen_trials = {a['trial_id'] for a in result['attempts']}
    eval_trials = {e['evaluator_trial_id'] for e in result['evaluator_calls']}
    assert not (gen_trials & eval_trials)        # an evaluator call is not a generation trial


# ----------------------------------------------------------------- verdict is diagnostic only
def test_verdict_is_not_run_unless_explicitly_budgeted(fal_key, auth):
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
          preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
          dry_run=False, authorisation_path=auth)
    assert judge.verdict_calls == 0


def test_a_verdict_may_never_overturn_a_primary_transcription_mismatch(fal_key, auth):
    """The judge is shown the answer and agrees. The primary measurement must not move."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge = ScriptedJudge(reply_for=lambda b: 'not the target at all')   # verdict() says MATCH
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, run_verdict_diagnostic=True, authorisation_path=auth)

    assert judge.verdict_calls == 16
    assert result['exact_matches'] == 0
    primary = [m for m in result['measurements'] if m['role'] == 'primary']
    assert all(m['exact_match'] is False for m in primary)
    diagnostic = [m for m in result['measurements'] if m['role'] == 'diagnostic']
    assert diagnostic and all(m['may_override_primary'] is False for m in diagnostic)


# ----------------------------------------------------------------- gates still closed
def test_a_live_run_without_a_judge_instance_is_refused(fal_key, auth):
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    with pytest.raises(R.GateClosed):
        R.run(judge=QUALIFIED, judge_instance=None, routes=_routes(http, artifacts),
              preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
              dry_run=False, authorisation_path=auth)
    assert http.calls == []


def test_an_unqualified_judge_dispatches_nothing_even_on_the_live_path(fal_key, auth):
    """E13-E(4)."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    with pytest.raises(R.GateClosed):
        R.run(judge={'candidate': 'x', 'qualified_scope': []}, judge_instance=judge,
              routes=_routes(http, artifacts), preflight_green=True,
              guard=BudgetGuard(authorised_usd=Decimal('10.00')), dry_run=False, authorisation_path=auth)
    assert http.calls == []
    assert judge.transcribe_calls == 0


def test_budget_exhaustion_stops_the_live_run_with_no_further_generation(fal_key, auth):
    """E13-E(5)."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    small = BudgetGuard(authorised_usd=Decimal('0.20'))
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=small, dry_run=False, stop_on_budget=True, authorisation_path=auth)
    assert result['stopped_reason'] == 'budget_exhausted'
    assert len(http.calls) < 16
    assert small.spent_usd <= small.authorised_usd


# ----------------------------------------------------------------- promotion boundary
def test_real_atex_evidence_still_cannot_promote_a_complete_slot(fal_key, auth):
    """E13-E(7). Non-synthetic evidence, and promotion is STILL refused."""
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)

    assert result['synthetic'] is False          # real evidence...
    assert result['may_populate_registry'] is False
    assert result['evidence_class'] == 'partial_admission_screen_only'
    with pytest.raises(R.PartialEvidenceOnly) as e:   # ...and promotion still refused
        R.promote_slot(result)
    assert 'partial' in str(e.value).lower()


def test_a_live_run_writes_no_registry_row(fal_key, auth):
    before = REGISTRY.read_bytes()
    http, artifacts = FakeFalHttp(), FakeArtifacts()
    judge, _ = _perfect_judge()
    result = R.run(judge=QUALIFIED, judge_instance=judge, routes=_routes(http, artifacts),
                   preflight_green=True, guard=BudgetGuard(authorised_usd=Decimal('10.00')),
                   dry_run=False, authorisation_path=auth)
    assert result['registry_rows_written'] == 0
    assert REGISTRY.read_bytes() == before


# ----------------------------------------------------------------- dry run unchanged
def test_the_dry_run_is_still_synthetic_and_still_uses_the_fake_path():
    gen = R.FakeGenerator()
    result = R.run(judge={'candidate': 'dry', 'qualified_scope': ['devanagari', 'latin']},
                   generator=gen, preflight_green=True,
                   guard=BudgetGuard(authorised_usd=Decimal('10.00')), dry_run=True)
    assert result['synthetic'] is True
    assert all(m['synthetic'] is True for m in result['measurements'])
    assert gen.calls == 16


def test_cli_fake_live_runs_the_real_measurement_path(monkeypatch, tmp_path, fal_key):
    import socket

    def explode(*a, **k):
        raise AssertionError('fake-live A-TEXT attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)

    auth = tmp_path / 'auth.yaml'
    auth.write_text("authorised: true\ntranche_id: EMP-001\n"
                    "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    out = tmp_path / 'atex-fake-live.json'
    assert R.main(['--fake-live', '--authorisation', str(auth), '--out', str(out)]) == 0

    r = json.loads(out.read_text())
    assert r['mode'] == 'fake_live'
    assert r['synthetic'] is False
    assert r['generations'] == 16
    assert r['external_calls'] == 0
    assert r['spend_usd'] == '0'
    assert r['registry_rows_written'] == 0
