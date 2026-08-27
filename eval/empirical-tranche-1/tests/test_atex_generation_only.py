"""Generation-only A-TEXT controls (EVAL-024).

The Controller reversed the ordering: generate the 16 frozen artifacts NOW, seal them, and score
them later against those exact bytes. That makes two new things load-bearing.

First, this path must be genuinely evaluator-free. Not "we chose not to call the judge" but "there
is no judge here to call" — because a scoring side-effect that slipped in would spend evaluator
money nobody authorised and, worse, would score images before an evaluator is qualified.

Second, the seal has to actually bind. These artifacts are irreplaceable: no regeneration after
seeing results is permitted, so a manifest that could be edited to point at different bytes would
quietly destroy the one guarantee the parallel plan rests on.

fal is never contacted here. Every transport is injected.
"""
import hashlib
import json
from decimal import Decimal
from pathlib import Path

import pytest

import generate_atex as G
import providers as P
import spend_ledger as SL
from fake_live import FakeFalHttp

PKG = Path(__file__).resolve().parents[1]
REGISTRY = PKG.parents[1] / 'eval' / 'registry' / 'registry-v1.jsonl'

FROZEN = ['शुभ दीपावली', 'आज की डील', 'Aaj ki Deal', 'SAVE 20% • ₹999']


@pytest.fixture
def fal_key(monkeypatch):
    monkeypatch.setenv('FAL_KEY', 'REHEARSAL-NOT-A-REAL-KEY')


def _run(tmp_path, run_id='run-genonly', prior_qualification=None):
    auth = tmp_path / 'auth.yaml'
    auth.write_text("authorised: true\ntranche_id: EMP-001\n"
                    "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    run = SL.TrancheRun.create(root=tmp_path / 'runs', run_id=run_id,
                               authorisation_path=auth, mode='fake_live')
    if prior_qualification:
        SL.TrancheBudget(run).correct(stage='qualification', amount_usd=prior_qualification,
                                      reason='prior qualification spend for this test')
    return run


class Artifacts:
    """Injected artifact store. Deterministic bytes per url; opens no socket."""

    def __init__(self):
        self.fetched = []

    def __call__(self, url):
        self.fetched.append(url)
        return b'\x89PNG\r\n\x1a\n' + url.encode('utf-8')


def _generate(tmp_path, http=None, run=None, artifacts=None):
    run = run or _run(tmp_path)
    artifacts = artifacts if artifacts is not None else Artifacts()
    cfg = G.config()
    routes = {slot: P.fal_route_for(slot, cfg, http=http or FakeFalHttp(),
                                    artifact_fetch=artifacts)
              for slot in cfg['atex']['slots']}
    result = G.generate_only(run, routes=routes, artifact_root=tmp_path / 'sealed',
                             mode='fake_live')
    return result, run, artifacts


# ============================================================ the frozen plan
def test_exactly_sixteen_coordinates_are_planned():
    coords = G.planned_coordinates()
    assert len(coords) == 16
    assert len({(c['slot'], c['item_id'], c['repeat_index']) for c in coords}) == 16
    assert sorted({c['slot'] for c in coords}) == ['IMG-01', 'IMG-02']
    for slot in ('IMG-01', 'IMG-02'):
        assert sum(1 for c in coords if c['slot'] == slot) == 8


def test_the_frozen_strings_are_exactly_the_four():
    assert [i['target_string'] for i in G.items()] == FROZEN


def test_the_routes_are_the_frozen_ones():
    cfg = G.config()
    assert cfg['atex']['slots']['IMG-01']['route'] == 'openai/gpt-image-2'
    assert cfg['atex']['slots']['IMG-02']['route'] == 'fal-ai/ideogram/v3'


def test_every_coordinate_is_unseeded():
    assert all(c['seed'] is None and c['seed_policy'] == 'unseeded'
               for c in G.planned_coordinates())


# ============================================================ evaluator-free by construction
def test_a_full_generation_run_makes_zero_evaluator_calls(tmp_path, fal_key, monkeypatch):
    """Not 'we chose not to' — there is no judge here to call."""
    def explode(*a, **k):
        raise AssertionError('generation-only constructed a text judge')

    monkeypatch.setattr(P, 'OpenAITextJudge', explode)
    monkeypatch.setattr(P, 'GeminiTextJudge', explode)

    result, run, _ = _generate(tmp_path)

    assert result['evaluator_calls'] == 0
    assert result['generations'] == 16
    assert 'measurements' not in result


def test_the_module_never_imports_a_judge_or_a_scorer():
    source = (PKG / 'atex' / 'generate_atex.py').read_text(encoding='utf-8')
    for forbidden in ('TextJudge', 'transcribe(', 'qualify_text', 'load_qualification',
                      'select_judge_for_atex', 'transcription_matches'):
        assert forbidden not in source, forbidden


def test_no_evaluator_spend_lands_on_the_ledger(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    stages = {r.get('stage') for r in SL.TrancheBudget(run).records()}
    assert stages == {'atex'}


# ============================================================ scoring is impossible
def _all_keys(node):
    """Every dict KEY at any depth. Checked as keys, not as substrings.

    An earlier version of this grepped the serialised manifest for 'score', which the legitimate
    field `scored: false` contains. A control that fires on the manifest correctly declaring
    itself unscored is worse than no control.
    """
    if isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from _all_keys(v)
    elif isinstance(node, list):
        for v in node:
            yield from _all_keys(v)


@pytest.mark.parametrize('field', ['exact_match', 'passed', 'pass_rate', 'verdict', 'score',
                                   'transcription', 'text_specific_stop_eligible'])
def test_a_scoring_field_cannot_enter_the_manifest(tmp_path, fal_key, field):
    result, run, _ = _generate(tmp_path)
    manifest = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    assert field not in set(_all_keys(manifest))


def test_the_manifest_declares_itself_unscored_and_sealed(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    assert m['scored'] is False
    assert m['sealed_for_later_evaluation'] is True
    assert m['may_populate_registry'] is False
    assert m['evaluator_calls'] == 0


def test_writing_a_scoring_field_is_refused_outright(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    m['scored'] = True
    with pytest.raises(G.ScoringForbidden):
        G.write_manifest(m, tmp_path / 'manifest.json')


def test_an_injected_pass_fail_field_is_refused(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    m['artifacts'][0]['exact_match'] = True
    with pytest.raises(G.ScoringForbidden):
        G.write_manifest(m, tmp_path / 'manifest.json')


# ============================================================ the seal
def test_every_successful_artifact_is_sealed_by_sha256(tmp_path, fal_key):
    result, run, artifacts = _generate(tmp_path)
    assert len(result['artifacts']) == 16
    for a in result['artifacts']:
        blob = (tmp_path / 'sealed' / a['relative_path']).read_bytes()
        assert hashlib.sha256(blob).hexdigest() == a['sha256']
        assert a['bytes'] == len(blob)


def test_the_seal_detects_a_swapped_artifact(tmp_path, fal_key):
    """The guarantee the whole parallel plan rests on: later scoring reads THESE bytes."""
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    G.write_manifest(m, tmp_path / 'manifest.json')

    victim = tmp_path / 'sealed' / m['artifacts'][0]['relative_path']
    victim.write_bytes(b'\x89PNG\r\n\x1a\n-a-different-image-entirely-')

    report = G.verify_sealed_artifacts(m, artifact_root=tmp_path / 'sealed')
    assert report['ok'] is False
    assert m['artifacts'][0]['coordinate_id'] in report['hash_mismatches']


def test_the_seal_detects_a_deleted_artifact(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    (tmp_path / 'sealed' / m['artifacts'][0]['relative_path']).unlink()
    report = G.verify_sealed_artifacts(m, artifact_root=tmp_path / 'sealed')
    assert report['ok'] is False
    assert report['missing']


def test_an_intact_seal_verifies(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    report = G.verify_sealed_artifacts(m, artifact_root=tmp_path / 'sealed')
    assert report['ok'] is True
    assert report['verified'] == 16


def test_the_manifest_fingerprint_detects_tampering(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    recorded = m['evidence_fingerprint']

    tampered = json.loads(json.dumps(m))
    tampered['artifacts'][0]['sha256'] = '0' * 64
    assert G.manifest_fingerprint(tampered) != recorded


def test_the_fingerprint_covers_the_route_identity(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    tampered = json.loads(json.dumps(m))
    tampered['routes']['IMG-01']['route'] = 'some-other/model'
    assert G.manifest_fingerprint(tampered) != m['evidence_fingerprint']


def test_the_fingerprint_covers_the_frozen_input_set(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    tampered = json.loads(json.dumps(m))
    tampered['frozen_items'][0]['target_string'] = 'something else'
    assert G.manifest_fingerprint(tampered) != m['evidence_fingerprint']


# ============================================================ trials, budget, retries
def test_one_call_is_one_trial_with_a_resolvable_cost_ref(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    assert len({c['trial_id'] for c in result['call_records']}) == 16
    ledger_refs = {r.get('cost_ref') for r in SL.TrancheBudget(run).records()}
    assert {c['cost_ref'] for c in result['call_records']} <= ledger_refs


def test_retries_are_zero_and_no_attempt_carries_a_retry_reference(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    assert result['retries'] == 0
    assert all(c['retry_of_attempt_id'] is None for c in result['call_records'])


def test_the_persistent_tranche_budget_is_used(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    reopened = SL.TrancheBudget(SL.TrancheRun.open(tmp_path / 'runs', 'run-genonly'))
    assert reopened.stage_spent_usd('atex') > 0
    assert reopened.spent_usd() == reopened.stage_spent_usd('atex')


def test_prior_qualification_spend_is_preserved_and_added_to(tmp_path, fal_key):
    """Historical evidence preserved: generation must not disturb what qualification recorded."""
    run = _run(tmp_path, prior_qualification=Decimal('1.3037905'))
    before = SL.TrancheBudget(run).records()
    result, _, _ = _generate(tmp_path, run=run)

    budget = SL.TrancheBudget(run)
    assert budget.stage_spent_usd('qualification') == Decimal('1.3037905')
    assert budget.stage_spent_usd('atex') > 0
    assert budget.spent_usd() == Decimal('1.3037905') + budget.stage_spent_usd('atex')
    after = budget.records()
    assert after[:len(before)] == before          # append-only; nothing rewritten


def test_generation_is_refused_when_it_would_break_the_ten_dollar_ceiling(tmp_path, fal_key):
    """Spread across both stages, because qualification has its own USD 6 sub-cap."""
    run = _run(tmp_path, prior_qualification=Decimal('5.95'))
    SL.TrancheBudget(run).correct(stage='atex', amount_usd=Decimal('4.00'),
                                  reason='prior A-TEXT spend for this test')
    assert SL.TrancheBudget(run).remaining_usd() == Decimal('0.05')

    from budget_guard import BudgetExceeded
    http = FakeFalHttp()
    with pytest.raises(BudgetExceeded):
        _generate(tmp_path, http=http, run=run)
    assert len(http.calls) == 0        # refused before dispatch


def test_the_nominal_cost_matches_the_frozen_planning_prices(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    expected = Decimal('0.053') * 8 + Decimal('0.060') * 8
    assert Decimal(result['total_generation_cost_usd']) == expected
    assert expected == Decimal('0.904')


# ============================================================ failures stay evidence
def test_an_ambiguous_failure_persists_and_stops_that_route(tmp_path, fal_key):
    class Exploding:
        def __init__(self): self.calls = 0
        def __call__(self, url, headers, body, timeout_s):
            self.calls += 1
            raise TimeoutError('read timed out')

    result, run, _ = _generate(tmp_path, http=Exploding())

    ambiguous = [c for c in result['call_records'] if c.get('ambiguous_dispatch')]
    assert ambiguous
    assert ambiguous[0]['api_status'] == 'timeout'
    assert ambiguous[0]['cost_ref']
    assert ambiguous[0]['billing_state'] == 'unknown_provisional'
    assert result['retries'] == 0
    assert SL.TrancheBudget(run).spent_usd() > 0       # conservatively counted
    assert result['missing_coordinates']


def test_a_refusal_is_persisted_as_its_trial_with_no_artifact(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path, http=FakeFalHttp(refuse_every=4))
    refusals = [c for c in result['call_records'] if c['api_status'] == 'refusal']
    assert refusals
    assert all(c['cost_ref'] for c in refusals)
    sealed = {a['coordinate_id'] for a in result['artifacts']}
    assert all(c['coordinate_id'] not in sealed for c in refusals)
    assert len(result['artifacts']) + len(result['missing_coordinates']) == result['generations']


def test_a_missing_coordinate_is_recorded_rather_than_silently_dropped(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path, http=FakeFalHttp(refuse_every=4))
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    assert m['missing_coordinates']
    for miss in m['missing_coordinates']:
        assert miss['reason']
        assert miss['coordinate_id']


# ============================================================ Registry untouched
def test_the_registry_is_untouched(tmp_path, fal_key):
    before = REGISTRY.read_bytes()
    _generate(tmp_path)
    assert REGISTRY.read_bytes() == before


def test_the_result_cannot_populate_the_registry(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path)
    assert result['may_populate_registry'] is False
    assert result['registry_rows_written'] == 0


# ============================================================ live requires real authorisation
def test_live_mode_refuses_without_a_valid_authorisation(tmp_path, monkeypatch):
    monkeypatch.delenv('FAL_KEY', raising=False)
    assert G.main(['--live', '--run-root', str(tmp_path / 'runs'),
                   '--run-id', 'nope']) != 0


# ============================================================ media type honesty (EVAL-024 cleanup)
"""The filename must not claim PNG when fal returned something else.

An extension is a claim about bytes. If a `.png` path holds JPEG bytes, every later reader — the
evaluator, a human opening the folder, any tooling that dispatches on extension — is misled by
evidence we sealed ourselves. Detect from the bytes, name accordingly, and never transcode: the
sealed hash must be over exactly what the provider returned.
"""

PNG_1x1 = (b'\x89PNG\r\n\x1a\n' + b'\x00\x00\x00\rIHDR'
           + (1).to_bytes(4, 'big') + (1).to_bytes(4, 'big') + b'\x08\x06\x00\x00\x00'
           + b'\x00' * 20)

# JPEG: SOI, APP0, then SOF0 declaring 40 high x 30 wide.
JPEG_30x40 = (b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
              + b'\xff\xc0\x00\x11\x08' + (40).to_bytes(2, 'big') + (30).to_bytes(2, 'big')
              + b'\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01' + b'\xff\xd9')

# WebP (lossy VP8): RIFF container, VP8 chunk with a 16x8 frame header.
_VP8 = (b'\x9d\x01\x2a' + (16).to_bytes(2, 'little') + (8).to_bytes(2, 'little'))
WEBP_16x8 = (b'RIFF' + (4 + 8 + len(_VP8) + 3).to_bytes(4, 'little') + b'WEBP'
             + b'VP8 ' + (len(_VP8) + 3).to_bytes(4, 'little') + b'\x00\x00\x00' + _VP8)


def test_png_bytes_are_detected_with_dimensions():
    media, ext, dims = G.detect_media(PNG_1x1)
    assert media == 'image/png' and ext == '.png'
    assert dims == {'width': 1, 'height': 1}


def test_jpeg_bytes_are_detected_with_dimensions():
    media, ext, dims = G.detect_media(JPEG_30x40)
    assert media == 'image/jpeg' and ext == '.jpg'
    assert dims == {'width': 30, 'height': 40}


def test_webp_bytes_are_detected_with_dimensions():
    media, ext, dims = G.detect_media(WEBP_16x8)
    assert media == 'image/webp' and ext == '.webp'
    assert dims == {'width': 16, 'height': 8}


def test_unknown_bytes_get_a_content_neutral_name_and_no_invented_dimensions():
    media, ext, dims = G.detect_media(b'not an image at all')
    assert media == 'application/octet-stream'
    assert ext == '.bin'
    assert dims is None


def test_truncated_bytes_do_not_produce_guessed_dimensions():
    """Better to record no dimensions than a number nobody can trust."""
    media, ext, dims = G.detect_media(b'\x89PNG\r\n\x1a\n')
    assert media == 'image/png'
    assert dims is None


@pytest.mark.parametrize('blob,expected_ext,expected_media', [
    (PNG_1x1, '.png', 'image/png'),
    (JPEG_30x40, '.jpg', 'image/jpeg'),
    (WEBP_16x8, '.webp', 'image/webp'),
    (b'mystery bytes', '.bin', 'application/octet-stream'),
])
def test_the_sealed_filename_matches_the_actual_bytes(tmp_path, fal_key, blob, expected_ext,
                                                      expected_media):
    """The regression the Controller flagged: a .png path holding non-PNG bytes."""
    result, run, _ = _generate(tmp_path, artifacts=lambda url: blob)

    a = result['artifacts'][0]
    assert a['relative_path'].endswith(expected_ext)
    assert a['media_type'] == expected_media

    on_disk = (tmp_path / 'sealed' / a['relative_path']).read_bytes()
    assert on_disk == blob                      # byte-identical: nothing was transcoded
    assert a['sha256'] == hashlib.sha256(blob).hexdigest()
    assert a['bytes'] == len(blob)


def test_jpeg_returned_by_fal_is_never_written_to_a_png_path(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path, artifacts=lambda url: JPEG_30x40)
    assert not any(a['relative_path'].endswith('.png') for a in result['artifacts'])
    assert all(a['media_type'] == 'image/jpeg' for a in result['artifacts'])


def test_the_seal_still_verifies_for_non_png_media(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path, artifacts=lambda url: WEBP_16x8)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    report = G.verify_sealed_artifacts(m, artifact_root=tmp_path / 'sealed')
    assert report['ok'] is True and report['verified'] == 16


def test_media_type_and_dimensions_reach_the_manifest(tmp_path, fal_key):
    result, run, _ = _generate(tmp_path, artifacts=lambda url: JPEG_30x40)
    m = G.build_manifest(run, result, artifact_root=tmp_path / 'sealed')
    for a in m['artifacts']:
        assert a['media_type'] == 'image/jpeg'
        assert a['dimensions'] == {'width': 30, 'height': 40}
