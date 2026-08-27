"""EVAL-025 controls for the two script-routed literal Tesseract legs. No paid API is contacted.

The only variable between these legs and the disqualified EVAL-023 candidate is which traineddata
model is loaded. Everything else — binary, OEM, PSM, all six DAWG flags, preprocessing, retries —
must be byte-for-byte the same, or the comparison against EVAL-023 measures two changes at once
and attributes both to script routing.

So the invariance is asserted explicitly, flag by flag, against the EVAL-023 constants.
"""
import copy
import json
import subprocess
from decimal import Decimal

import pytest

import qualify_ocr as QO
import qualify_text as QT
import tesseract_ocr as TESS
from budget_guard import BudgetGuard

IMAGE = b'\x89PNG\r\n\x1a\n-not-a-real-image-'
TARGET_DEV = 'कण्डाघाट'


class BatteryRunner:
    """Returns the string actually DRAWN, resolved by image bytes."""

    def __init__(self, scripts=('devanagari', 'latin')):
        import hashlib
        self.calls = []
        self._by_sha = {}
        images = QT.ImageResolver()
        for script in scripts:
            for item in QT._script_items(script):
                data = images.bytes_for(script, item['item_id'])
                self._by_sha[hashlib.sha256(data).hexdigest()] = (item['item_id'], item['drawn'])

    def __call__(self, cmd, env, timeout_s):
        import hashlib
        from pathlib import Path
        raw = Path(cmd[1]).read_bytes()
        item_id, drawn = self._by_sha[hashlib.sha256(raw).hexdigest()]
        self.calls.append({'item_id': item_id, 'cmd': list(cmd)})
        return 0, drawn + '\n', ''


# ------------------------------------------------------------------ frozen leg identities
def test_the_two_legs_are_exactly_what_the_decision_specifies():
    legs = TESS.SCRIPT_ROUTED_LEGS
    assert legs['devanagari'] == {'languages': 'hin',
                                  'alias': 'tesseract5-hin-literal-psm13-v1'}
    assert legs['latin'] == {'languages': 'eng',
                             'alias': 'tesseract5-eng-literal-psm13-v1'}


@pytest.mark.parametrize('script,lang,alias', [
    ('devanagari', 'hin', 'tesseract5-hin-literal-psm13-v1'),
    ('latin', 'eng', 'tesseract5-eng-literal-psm13-v1'),
])
def test_each_leg_loads_only_its_own_model(script, lang, alias):
    engine = TESS.TesseractLiteralOcr(config_alias=alias, languages=lang)
    cmd = ' '.join(engine.build_command('/tmp/x.png'))
    assert f'-l {lang}' in cmd
    other = 'eng' if lang == 'hin' else 'hin'
    assert f'-l {other}' not in cmd
    assert 'hin+eng' not in cmd
    assert engine.identity()['languages'] == lang
    assert engine.identity()['config_alias'] == alias
    # Only that leg's traineddata is hashed and bound.
    assert set(engine.identity()['traineddata_sha256']) == {f'{lang}.traineddata'}


@pytest.mark.parametrize('lang', ['hin', 'eng'])
def test_everything_except_the_model_is_unchanged_from_eval_023(lang):
    """The comparison is only valid if script routing is the ONE variable."""
    engine = TESS.TesseractLiteralOcr(languages=lang)
    ident = engine.identity()
    assert ident['oem'] == TESS.OEM == '1'
    assert ident['psm'] == TESS.PSM == '13'
    assert ident['dawg_flags'] == {k: v for k, v in TESS.DAWG_FLAGS}
    assert all(v == '0' for v in ident['dawg_flags'].values())
    assert len(ident['dawg_flags']) == 6
    assert ident['preprocessing'] == 'none'
    assert ident['user_words'] is None
    assert ident['one_process_per_trial'] is True
    assert ident['tessdata_tag'] == '4.1.0'
    assert ident['tessdata_commit'] == 'e2aad9b983032bb1beff9133104a67cdbb87ca4d'
    assert ident['tesseract_version'].startswith('tesseract 5')

    cmd = ' '.join(engine.build_command('/tmp/x.png'))
    for flag, _ in TESS.DAWG_FLAGS:
        assert f'{flag}=0' in cmd
    assert '--psm 13' in cmd and '--oem 1' in cmd


def test_the_two_legs_have_distinct_config_fingerprints():
    hin = TESS.TesseractLiteralOcr(config_alias='tesseract5-hin-literal-psm13-v1',
                                   languages='hin').config_sha256()
    eng = TESS.TesseractLiteralOcr(config_alias='tesseract5-eng-literal-psm13-v1',
                                   languages='eng').config_sha256()
    mixed = TESS.TesseractLiteralOcr().config_sha256()          # the EVAL-023 candidate
    assert len({hin, eng, mixed}) == 3


def test_the_pinned_traineddata_is_unchanged_from_eval_023():
    engine = TESS.TesseractLiteralOcr(languages='hin+eng')
    h = engine.traineddata_hashes()
    assert h['hin.traineddata'] == (
        'bd2e65a2184af08a167b0be2439e91fa5edbc4394399ca2f692b843ae26e78d6')
    assert h['eng.traineddata'] == (
        '8280aed0782fe27257a68ea10fe7ef324ca0f8d85bd2fd145d1c2b560bcb66ba')


# ------------------------------------------------------------------------------ blindness
@pytest.mark.parametrize('lang', ['hin', 'eng'])
def test_the_target_cannot_reach_a_routed_leg(lang):
    calls = []

    def runner(cmd, env, timeout_s):
        calls.append({'cmd': list(cmd), 'env': dict(env)})
        return 0, 'x', ''

    TESS.TesseractLiteralOcr(languages=lang, runner=runner).transcribe(
        IMAGE, blind_check_target=TARGET_DEV, trial_id='devanagari:dx-0013:transcribe:p0')
    blob = json.dumps(calls[0], ensure_ascii=False)
    assert TARGET_DEV not in blob
    assert set(calls[0]['env']) == {'PATH', 'TESSDATA_PREFIX', 'LC_ALL', 'LANG'}


# ------------------------------------------------------------- independence and execution
def test_both_legs_run_regardless_of_the_other_and_are_not_gated():
    runner = BatteryRunner()
    payload = QO.run_script_routed_tesseract(runner=runner)

    assert set(payload['legs']) == {'devanagari', 'latin'}
    for script in ('devanagari', 'latin'):
        leg = payload['legs'][script]
        assert leg['result']['calls'] == 288
        assert leg['result']['scientifically_complete'] is True
    assert payload['local_executions'] == 576
    assert len(runner.calls) == 576
    assert payload['api_calls'] == 0
    assert payload['api_spend_usd'] == '0'


def test_a_failing_devanagari_leg_does_not_stop_the_latin_leg():
    """The EVAL-023 progressive stop must NOT apply across two separate candidates."""
    class HalfBadRunner(BatteryRunner):
        def __call__(self, cmd, env, timeout_s):
            code, out, err = super().__call__(cmd, env, timeout_s)
            # Corrupt every Devanagari read so that leg fails outright.
            item = self.calls[-1]['item_id']
            if item.startswith('dx-'):
                return 0, 'ZZZ\n', ''
            return code, out, err

    payload = QO.run_script_routed_tesseract(runner=HalfBadRunner())
    assert payload['legs']['devanagari']['result']['passed'] is False
    assert payload['legs']['latin']['result']['calls'] == 288      # ran anyway
    assert payload['legs']['latin']['result']['passed'] is True


def test_the_legs_are_not_a_composite_evaluator_and_cannot_open_atext():
    payload = QO.run_script_routed_tesseract(runner=BatteryRunner())
    assert payload['is_composite_evaluator'] is False
    assert payload['may_open_atext'] is False
    assert payload['may_populate_registry'] is False


def test_the_leg_evidence_fingerprint_detects_tampering():
    payload = QO.run_script_routed_tesseract(runner=BatteryRunner(scripts=('devanagari',
                                                                          'latin')))
    base = payload['evidence_fingerprint']
    for mutate in (
        lambda p: p['legs']['devanagari']['result']['observations'].__setitem__(
            0, {**p['legs']['devanagari']['result']['observations'][0], 'observed': 'match'}),
        lambda p: p['legs']['latin'].__setitem__('config_sha256', 'a' * 64),
        lambda p: p.__setitem__('contract_sha256', 'b' * 64),
    ):
        import hashlib
        t = copy.deepcopy(payload)
        mutate(t)
        other = hashlib.sha256(json.dumps(
            {k: t.get(k) for k in ('record', 'tranche_id', 'family', 'legs', 'contract_sha256')},
            sort_keys=True, separators=(',', ':'), ensure_ascii=False,
            default=str).encode()).hexdigest()
        assert other != base


def test_no_paid_provider_transport_is_constructed(monkeypatch):
    import ocr_providers as OCR

    def explode(*a, **k):
        raise AssertionError('a paid Cloud Vision transport was constructed during EVAL-025')

    monkeypatch.setattr(OCR, 'CloudVisionHttpTransport', explode)
    payload = QO.run_script_routed_tesseract(runner=BatteryRunner())
    assert payload['api_calls'] == 0


def test_gates_and_normalisation_are_unchanged():
    c = QO.ocr_contract()
    assert c['mismatch_false_pass_max'] == 0
    assert c['match_false_fail_rate_max'] == 0.10
    assert c['empty_transcription_rate_max'] == 0.05
    assert c['repeat_consistency_min'] == 0.95
    assert c['repeats_per_shape'] == 3
    assert QT.normalise('  abc  ') == 'abc'
    assert QT.transcription_matches('abc', ' abc ') is True
    assert QT.transcription_matches('abc', 'abc.') is False       # not loosened


def test_the_registry_is_untouched():
    registry = QT.REPO_ROOT / 'eval' / 'registry' / 'registry-v1.jsonl'
    rows = [x for x in registry.read_text(encoding='utf-8').splitlines()
            if x.strip() and not x.startswith('#')]
    assert rows == []
