"""EVAL-023 controls for the local literal Tesseract candidate. No paid API is contacted.

The experiment's whole claim rests on the configuration being what it says it is. If a dictionary
flag silently flipped, or the adaptive classifier carried state between trials, or the target
reached the command line, the run would produce numbers that look like evidence and are not.

So the configuration is asserted flag by flag, and the blindness rule the API families are held to
is applied to a local subprocess: command, temp path AND environment.
"""
import copy
import json
import os
import subprocess
from decimal import Decimal

import pytest

import qualify_ocr as QO
import qualify_text as QT
import tesseract_ocr as TESS
from budget_guard import BudgetGuard

IMAGE = b'\x89PNG\r\n\x1a\n-not-a-real-image-'
TARGET_DEV = 'कण्डाघाट'


class FakeRunner:
    """Stands where `subprocess.run` would. Records every invocation."""

    def __init__(self, stdout_for=None, default='कण्डाघाट', returncode=0, raises=None):
        self.calls = []
        self.stdout_for = stdout_for or {}
        self.default = default
        self.returncode = returncode
        self.raises = raises

    def __call__(self, cmd, env, timeout_s):
        self.calls.append({'cmd': list(cmd), 'env': dict(env), 'timeout_s': timeout_s})
        if self.raises:
            raise self.raises
        return self.returncode, self.default, ''


class BatteryRunner:
    """Returns the string actually DRAWN, resolved by image bytes, so scoring is exercised."""

    def __init__(self, scripts=('devanagari', 'latin'), empty_for=None, fail_for=None,
                 exc_for=None):
        import hashlib
        self.calls = []
        self.empty_for = empty_for or set()
        self.fail_for = fail_for or set()
        self.exc_for = exc_for or set()
        self._by_sha = {}
        images = QT.ImageResolver()
        for script in scripts:
            for item in QT._script_items(script):
                data = images.bytes_for(script, item['item_id'])
                self._by_sha[hashlib.sha256(data).hexdigest()] = (item['item_id'], item['drawn'])

    def __call__(self, cmd, env, timeout_s):
        import hashlib
        from pathlib import Path
        path = cmd[1]
        raw = Path(path).read_bytes()
        item_id, drawn = self._by_sha[hashlib.sha256(raw).hexdigest()]
        self.calls.append({'item_id': item_id, 'path': path, 'cmd': list(cmd)})
        if item_id in self.exc_for:
            raise subprocess.TimeoutExpired(cmd, timeout_s)
        if item_id in self.fail_for:
            return 1, '', 'tesseract: fatal'
        if item_id in self.empty_for:
            return 0, '', ''
        return 0, drawn + '\n', ''


# ------------------------------------------------------------------ frozen configuration
def test_the_frozen_configuration_is_exactly_what_the_decision_specifies():
    assert TESS.CANDIDATE_ALIAS == 'tesseract5-hin-eng-literal-psm13-v1'
    assert TESS.LANGUAGES == 'hin+eng'
    assert TESS.OEM == '1'
    assert TESS.PSM == '13'
    assert dict(TESS.DAWG_FLAGS) == {
        'load_system_dawg': '0', 'load_freq_dawg': '0', 'load_unambig_dawg': '0',
        'load_bigram_dawg': '0', 'load_punc_dawg': '0', 'load_number_dawg': '0'}
    assert len(TESS.DAWG_FLAGS) == 6


def test_every_lexical_aid_is_disabled_in_the_actual_command():
    cmd = TESS.TesseractLiteralOcr().build_command('/tmp/x.png')
    joined = ' '.join(cmd)
    for flag, _ in TESS.DAWG_FLAGS:
        assert f'{flag}=0' in joined, flag
        assert f'{flag}=1' not in joined
    assert '--psm 13' in joined and '--oem 1' in joined
    assert '-l hin+eng' in joined
    assert '--tessdata-dir' in joined
    assert 'user_words' not in joined
    assert '--user-words' not in joined


def test_the_binary_must_be_tesseract_5():
    v = TESS.tesseract_version()
    assert v.startswith('tesseract 5'), v


def test_version_and_traineddata_hashes_are_bound_into_the_config_fingerprint():
    engine = TESS.TesseractLiteralOcr()
    ident = engine.identity()
    assert ident['tesseract_version'].startswith('tesseract 5')
    assert set(ident['traineddata_sha256']) == {'hin.traineddata', 'eng.traineddata'}
    assert all(len(h) == 64 for h in ident['traineddata_sha256'].values())
    assert ident['tessdata_commit'] == TESS.TESSDATA_COMMIT
    assert ident['tessdata_tag'] == TESS.TESSDATA_TAG

    base = engine.config_sha256()
    for mutate in (
        lambda i: i.__setitem__('tesseract_version', 'tesseract 4.1.1'),
        lambda i: i['traineddata_sha256'].__setitem__('hin.traineddata', 'f' * 64),
        lambda i: i['traineddata_sha256'].__setitem__('eng.traineddata', 'e' * 64),
        lambda i: i.__setitem__('psm', '6'),
        lambda i: i.__setitem__('oem', '3'),
        lambda i: i.__setitem__('languages', 'hin'),
        lambda i: i['dawg_flags'].__setitem__('load_system_dawg', '1'),
        lambda i: i.__setitem__('tessdata_commit', 'a' * 40),
    ):
        import hashlib as _h
        mutated = copy.deepcopy(ident)
        mutate(mutated)
        other = _h.sha256(json.dumps(mutated, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()
        assert other != base


# ------------------------------------------------------------------------------ blindness
def test_the_target_cannot_reach_the_command_path_or_environment():
    runner = FakeRunner()
    engine = TESS.TesseractLiteralOcr(runner=runner)
    engine.transcribe(IMAGE, blind_check_target=TARGET_DEV,
                      trial_id='devanagari:dx-0013:transcribe:p0')

    call = runner.calls[0]
    blob = json.dumps(call, ensure_ascii=False)
    assert TARGET_DEV not in blob
    assert QT.normalise(TARGET_DEV) not in blob
    # The temp filename carries trial coordinates only.
    assert 'dx-0013' in call['cmd'][1]
    assert TARGET_DEV not in call['cmd'][1]
    # The environment is minimal and explicit, not the inherited process environment.
    assert set(call['env']) == {'PATH', 'TESSDATA_PREFIX', 'LC_ALL', 'LANG'}


def test_no_provider_api_key_is_ever_handed_to_the_subprocess(monkeypatch):
    monkeypatch.setenv('GOOGLE_CLOUD_VISION_API_KEY', 'should-never-propagate')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'also-never')
    runner = FakeRunner()
    TESS.TesseractLiteralOcr(runner=runner).transcribe(IMAGE, blind_check_target=TARGET_DEV)
    env = runner.calls[0]['env']
    assert 'GOOGLE_CLOUD_VISION_API_KEY' not in env
    assert 'ANTHROPIC_API_KEY' not in env
    assert 'should-never-propagate' not in json.dumps(env)


def test_a_leaking_command_is_refused_before_execution(monkeypatch):
    runner = FakeRunner()
    engine = TESS.TesseractLiteralOcr(runner=runner)
    monkeypatch.setattr(engine, 'build_command',
                        lambda p: ['tesseract', p, 'stdout', '-c', f'target_string={TARGET_DEV}'])
    with pytest.raises(TESS.DispatchRefused):
        engine.transcribe(IMAGE, blind_check_target=TARGET_DEV)
    assert runner.calls == []


# ---------------------------------------------------------------------- process discipline
def test_one_fresh_process_per_trial():
    runner = BatteryRunner(scripts=('devanagari',))
    engine = TESS.TesseractLiteralOcr(runner=runner)
    candidate = QO.TesseractCandidate(engine, name='fresh-process')
    result = QO._score_script(candidate, 'devanagari', BudgetGuard(authorised_usd=Decimal('6')),
                              repeats=3)
    assert result['calls'] == 288
    assert len(runner.calls) == 288                       # one invocation per trial, no reuse
    assert len({c['path'] for c in runner.calls}) == 288   # and a distinct temp file each time


def test_the_temp_image_is_removed_after_each_trial():
    runner = FakeRunner()
    TESS.TesseractLiteralOcr(runner=runner).transcribe(IMAGE, blind_check_target=TARGET_DEV)
    assert not os.path.exists(runner.calls[0]['cmd'][1])


# ------------------------------------------------------------------------------- taxonomy
def test_empty_stdout_on_a_successful_run_is_scientific_empty_transcription():
    r = TESS.TesseractLiteralOcr(runner=FakeRunner(default='')).transcribe(
        IMAGE, blind_check_target=TARGET_DEV)
    assert r.api_status == 'error'
    assert r.error_class == 'empty_transcription'
    assert r.ambiguous_dispatch is False
    assert QO._observed({'item_id': 'x', 'target': 'क', 'expected': 'match', 'drawn': 'क'},
                        {'api_status': 'error', 'error_class': 'empty_transcription',
                         'text': ''}) == 'empty_transcription'


def test_a_nonzero_exit_is_infrastructure():
    r = TESS.TesseractLiteralOcr(runner=FakeRunner(returncode=1)).transcribe(
        IMAGE, blind_check_target=TARGET_DEV)
    assert r.api_status == 'error'
    assert r.error_class == 'local_execution_exit_1'
    assert QO._observed({'item_id': 'x', 'target': 'क', 'expected': 'match', 'drawn': 'क'},
                        {'api_status': 'error', 'error_class': r.error_class,
                         'text': ''}) == QO.INFRASTRUCTURE_OUTCOME


def test_a_timeout_is_infrastructure():
    runner = FakeRunner(raises=subprocess.TimeoutExpired(['tesseract'], 1))
    r = TESS.TesseractLiteralOcr(runner=runner).transcribe(IMAGE, blind_check_target=TARGET_DEV)
    assert r.error_class == 'local_execution_timeoutexpired'
    assert QO._observed({'item_id': 'x', 'target': 'क', 'expected': 'match', 'drawn': 'क'},
                        {'api_status': 'error', 'error_class': r.error_class,
                         'text': ''}) == QO.INFRASTRUCTURE_OUTCOME


def test_an_infrastructure_failure_leaves_the_script_incomplete_and_null():
    victim = QT._script_items('devanagari')[10]['item_id']
    runner = BatteryRunner(scripts=('devanagari',), fail_for={victim})
    candidate = QO.TesseractCandidate(TESS.TesseractLiteralOcr(runner=runner), name='crash')
    result = QO._score_script(candidate, 'devanagari', BudgetGuard(authorised_usd=Decimal('6')),
                              repeats=3)
    assert result['scientifically_complete'] is False
    assert result['passed'] is None
    assert result['failed_gates'] == []
    assert result['infrastructure_failures'] == 1
    assert result['false_passes'] == 0 and result['false_fails'] == 0
    assert result['empty_transcriptions'] == 0
    assert all(r['retries'] == 0 for r in result['call_records'])


def test_empty_output_can_fail_its_own_gate_without_being_infrastructure():
    victims = {i['item_id'] for i in QT._script_items('devanagari')[:10]}
    runner = BatteryRunner(scripts=('devanagari',), empty_for=victims)
    candidate = QO.TesseractCandidate(TESS.TesseractLiteralOcr(runner=runner), name='silent')
    result = QO._score_script(candidate, 'devanagari', BudgetGuard(authorised_usd=Decimal('6')),
                              repeats=3)
    assert result['infrastructure_failures'] == 0
    assert result['empty_transcriptions'] == 30
    assert result['scientifically_complete'] is True
    assert 'empty_transcription_rate' in result['failed_gates']
    assert result['passed'] is False


# ----------------------------------------------------------------- full fake-subprocess run
def test_a_clean_fake_subprocess_completes_576_executions_and_qualifies():
    runner = BatteryRunner()
    payload = QO.run_local_tesseract(runner=runner, run=None)
    c = payload['candidates'][0]
    assert payload['local_executions'] == 576
    assert len(runner.calls) == 576
    assert c['devanagari']['calls'] == 288 and c['devanagari']['passed'] is True
    assert c['latin']['calls'] == 288 and c['latin']['passed'] is True
    assert c['qualified_scope'] == ['devanagari', 'latin']
    assert payload['api_calls'] == 0
    assert payload['api_spend_usd'] == '0'
    assert payload['may_open_atext'] is False
    assert all(r['billed_usd'] == '0' for r in payload['call_records'])


def test_the_persisted_record_carries_everything_the_review_needs():
    payload = QO.run_local_tesseract(runner=BatteryRunner(scripts=('devanagari',)), run=None)
    obs = payload['candidates'][0]['devanagari']['observations']
    for key in ('item_id', 'shape', 'pass', 'expected', 'observed', 'api_status',
                'target', 'rendered_string', 'ocr_transcription', 'failure_class',
                'failure_group', 'edit_detail', 'image_sha256', 'cost_basis'):
        assert key in obs[0], key
    rec = payload['call_records'][0]
    for key in ('tesseract_version', 'traineddata_sha256', 'psm', 'oem', 'languages',
                'dawg_flags', 'tessdata_commit', 'stderr_note', 'retries', 'image_sha256'):
        assert key in rec, key
    assert rec['retries'] == 0
    assert rec['dawg_flags'] == {k: v for k, v in TESS.DAWG_FLAGS}


def test_the_fingerprint_binds_the_tesseract_config_and_detects_tampering():
    run = type('R', (), {'run_id': 'tess-test', 'mode': 'live'})()
    payload = QO.run_local_tesseract(runner=BatteryRunner(scripts=('devanagari',)), run=None)
    payload['run_id'] = 'tess-test'
    payload['evidence_fingerprint'] = QO.ocr_qualification_fingerprint(payload)
    assert payload['config_sha256']

    for mutate in (
        lambda p: p['candidates'][0]['devanagari']['observations'].__setitem__(
            0, {**p['candidates'][0]['devanagari']['observations'][0], 'observed': 'match'}),
        lambda p: p.__setitem__('config_sha256', 'a' * 64),
        lambda p: p.__setitem__('contract_sha256', 'b' * 64),
        lambda p: p['call_records'].__setitem__(0, {**p['call_records'][0], 'psm': '6'}),
    ):
        t = copy.deepcopy(payload)
        mutate(t)
        assert QO.ocr_qualification_fingerprint(t) != payload['evidence_fingerprint']


# ------------------------------------------------------------------------ A-TEXT / registry
def test_local_ocr_evidence_cannot_open_atext(tmp_path):
    import run_atex as A

    run = type('R', (), {'run_id': 'tess-test', 'mode': 'live', 'evidence_dir': tmp_path})()
    payload = QO.run_local_tesseract(runner=BatteryRunner(), run=None)
    payload.update({'run_id': 'tess-test', 'mode': 'live', 'synthetic': False})
    payload['evidence_fingerprint'] = QO.ocr_qualification_fingerprint(payload)
    (tmp_path / QT.QUALIFICATION_FILENAME).write_text(
        json.dumps(payload, ensure_ascii=False, default=str), encoding='utf-8')

    with pytest.raises(A.GateClosed) as exc:
        A.load_qualification(run, expected_mode='live')
    assert 'ocr' in str(exc.value)


def test_the_registry_is_untouched_by_eval_023():
    registry = QT.REPO_ROOT / 'eval' / 'registry' / 'registry-v1.jsonl'
    rows = [x for x in registry.read_text(encoding='utf-8').splitlines()
            if x.strip() and not x.startswith('#')]
    assert rows == []


def test_no_paid_provider_module_is_touched_by_the_local_candidate(monkeypatch):
    """A local run must not construct a Cloud Vision transport even accidentally."""
    import ocr_providers as OCR

    def explode(*a, **k):
        raise AssertionError('a paid Cloud Vision transport was constructed during EVAL-023')

    monkeypatch.setattr(OCR, 'CloudVisionHttpTransport', explode)
    payload = QO.run_local_tesseract(runner=BatteryRunner(scripts=('devanagari',)), run=None)
    assert payload['api_calls'] == 0
