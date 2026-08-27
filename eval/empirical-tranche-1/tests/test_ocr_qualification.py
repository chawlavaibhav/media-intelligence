"""EMP-001 OCR-FAMILY controls. No provider is contacted by anything in this file.

Three things are being protected, and each has a negative twin that must fail.

  1. BLINDNESS. Cloud Vision receives an image and nothing else. There is no prompt for a target
     to leak through, which makes it tempting to assume the question is settled — so it is tested
     mechanically rather than assumed.

  2. NO SILENT MATCH. An OCR service that returns nothing has failed. The one thing that must
     never happen is an empty transcription being scored as agreement, because that converts a
     service outage into a false pass on the gate that exists to catch false passes.

  3. FAMILY ISOLATION. OCR evidence must not open A-TEXT, and the historical VLM contracts must
     not be touched by this family existing.
"""
import copy
import json
import os
import socket
from decimal import Decimal

import pytest

import ocr_providers as OCR
import qualify_ocr as QO
import qualify_text as QT
from budget_guard import BudgetExceeded, BudgetGuard

IMAGE = b'\x89PNG\r\n\x1a\n-not-a-real-image-'
TARGET_DEV = 'कण्डाघाट'


def _engine(http=None, guard=None):
    return OCR.CloudVisionTextDetection(
        transport=OCR.CloudVisionHttpTransport(http=http) if http is not None else None,
        guard=guard)


class RecordingHttp:
    """Stands exactly where the socket would be. Records URL, headers and body."""

    def __init__(self, fixture):
        self.fixture = fixture
        self.calls = []

    def __call__(self, url, headers, body, timeout_s):
        self.calls.append({"url": url, "headers": headers,
                           "body": json.loads(body.decode("utf-8"))})
        return copy.deepcopy(self.fixture)


# ------------------------------------------------------- nothing happens on construction
def test_constructing_the_ocr_engine_makes_no_network_call(monkeypatch):
    def explode(*a, **k):
        raise AssertionError('an OCR constructor attempted a network connection')

    monkeypatch.setattr(socket, 'socket', explode)
    engine = OCR.CloudVisionTextDetection()
    OCR.CloudVisionHttpTransport()
    assert engine.provider == 'google_cloud_vision'
    assert engine.identity()['feature'] == 'TEXT_DETECTION'


def test_the_first_candidate_is_pinned_to_no_language_hints():
    assert OCR.CloudVisionTextDetection().identity()['language_hints'] == []
    with pytest.raises(ValueError):
        OCR.CloudVisionTextDetection(language_hints=('hi',))


def test_the_request_is_text_detection_on_one_base64_image():
    body = OCR.CloudVisionTextDetection().build_request(IMAGE)
    assert list(body) == ['requests']
    assert len(body['requests']) == 1
    req = body['requests'][0]
    assert req['features'] == [{'type': 'TEXT_DETECTION', 'maxResults': 1}]
    import base64
    assert base64.b64decode(req['image']['content']) == IMAGE
    assert 'languageHints' not in json.dumps(body)


# ------------------------------------------------------------------------------ blindness
def test_the_target_can_never_reach_the_cloud_vision_request():
    engine = OCR.CloudVisionTextDetection()
    body = engine.build_request(IMAGE)
    blob = json.dumps(body, ensure_ascii=False)
    assert TARGET_DEV not in blob
    assert QT.normalise(TARGET_DEV) not in blob
    # And the mechanical checker agrees, using the same rule the VLM family is held to.
    assert OCR.verify_blind_payload(body, 'transcribe', TARGET_DEV) == []


def test_a_leaking_ocr_request_is_refused_before_dispatch(monkeypatch):
    http = RecordingHttp(OCR.CLOUD_VISION_OK_FIXTURE)
    engine = _engine(http=http, guard=BudgetGuard(authorised_usd=Decimal('1.00')))
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, 'not-a-real-key')

    # Simulate a future change that smuggles ground truth into the payload.
    monkeypatch.setattr(engine, 'build_request',
                        lambda image_bytes: {'requests': [{'target_string': TARGET_DEV}]})
    with pytest.raises(OCR.DispatchRefused):
        engine.transcribe(IMAGE, blind_check_target=TARGET_DEV)
    assert http.calls == []          # nothing was sent


# ------------------------------------------------------------------------- key and dispatch
def test_a_missing_key_refuses_before_any_dispatch(monkeypatch):
    monkeypatch.delenv(OCR.CLOUD_VISION_KEY_ENV, raising=False)
    http = RecordingHttp(OCR.CLOUD_VISION_OK_FIXTURE)
    engine = _engine(http=http, guard=BudgetGuard(authorised_usd=Decimal('1.00')))
    with pytest.raises(OCR.PreDispatchRefusal):
        engine.transcribe(IMAGE, blind_check_target=TARGET_DEV)
    assert http.calls == []


def test_the_key_travels_in_the_url_and_never_in_the_body(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, 'secret-key-value')
    http = RecordingHttp(OCR.CLOUD_VISION_OK_FIXTURE)
    engine = _engine(http=http, guard=BudgetGuard(authorised_usd=Decimal('1.00')))
    engine.transcribe(IMAGE, blind_check_target=TARGET_DEV)

    sent = http.calls[0]
    assert sent['url'].startswith(OCR.CLOUD_VISION_ENDPOINT)
    assert 'secret-key-value' not in json.dumps(sent['body'])
    assert 'secret-key-value' not in json.dumps(sent['headers'])
    # And the transport's own recorded URL is redacted.
    assert 'secret-key-value' not in engine.transport.last_url


def test_one_call_produces_exactly_one_dispatch_and_no_retry(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, 'k')
    http = RecordingHttp(OCR.CLOUD_VISION_RESPONSE_ERROR_FIXTURE)
    engine = _engine(http=http, guard=BudgetGuard(authorised_usd=Decimal('1.00')))
    r = engine.transcribe(IMAGE, blind_check_target=TARGET_DEV)
    assert len(http.calls) == 1                     # an error response is NOT retried
    assert r.api_status == 'error'


# -------------------------------------------------------------------------------- parsing
def test_a_clean_response_parses_to_the_transcription():
    r = OCR.CloudVisionTextDetection().parse(OCR.CLOUD_VISION_OK_FIXTURE)
    assert r.api_status == 'ok'
    assert r.text == 'कण्डाघाट'
    assert r.provider_request_id == 'cv-req-ok'
    assert r.billed_usd == OCR.CLOUD_VISION_USD_PER_IMAGE


def test_empty_ocr_output_is_an_evaluator_failure_never_a_match():
    r = OCR.CloudVisionTextDetection().parse(OCR.CLOUD_VISION_EMPTY_FIXTURE)
    assert r.api_status == 'error'
    assert r.error_class == 'empty_transcription'
    assert r.text == ''
    assert r.billed_usd == OCR.CLOUD_VISION_USD_PER_IMAGE   # an empty answer is still billed


def test_a_documented_provider_error_is_well_formed_not_ambiguous():
    r = OCR.CloudVisionTextDetection().parse(OCR.CLOUD_VISION_RESPONSE_ERROR_FIXTURE)
    assert r.api_status == 'error'
    assert r.error_class == 'provider_error_permission_denied'
    assert r.ambiguous_dispatch is False

    top = OCR.CloudVisionTextDetection().parse(OCR.CLOUD_VISION_TOP_LEVEL_ERROR_FIXTURE)
    assert top.error_class == 'provider_error_resource_exhausted'
    assert top.ambiguous_dispatch is False


def test_a_malformed_response_fails_closed():
    with pytest.raises(OCR.ProviderResponseError):
        OCR.CloudVisionTextDetection().parse(OCR.CLOUD_VISION_MALFORMED_FIXTURE)
    with pytest.raises(OCR.ProviderResponseError):
        OCR.CloudVisionTextDetection().parse({'responseId': 'x'})


def test_a_malformed_reply_is_charged_and_stops_the_run(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, 'k')
    guard = BudgetGuard(authorised_usd=Decimal('1.00'))
    http = RecordingHttp(OCR.CLOUD_VISION_MALFORMED_FIXTURE)
    engine = _engine(http=http, guard=guard)
    r = engine.transcribe(IMAGE, blind_check_target=TARGET_DEV)
    assert r.api_status == 'error'
    assert r.error_class == 'malformed_response'
    assert r.ambiguous_dispatch is True
    assert r.billing_state == 'unknown_provisional'
    assert guard.spent_usd == OCR.CLOUD_VISION_USD_PER_IMAGE   # never free


# --------------------------------------------------------------------------------- scoring
def test_an_empty_transcription_is_its_own_scientific_outcome_not_a_match():
    item = {'item_id': 'x', 'target': 'क', 'expected': 'match', 'drawn': 'क'}
    assert QO._observed(item, {'api_status': 'error', 'error_class': 'empty_transcription',
                               'text': ''}) == 'empty_transcription'
    assert QO._observed(item, {'api_status': 'ok', 'text': '   '}) == 'empty_transcription'


def test_infrastructure_errors_are_not_scientific_outcomes():
    item = {'item_id': 'x', 'target': 'क', 'expected': 'match', 'drawn': 'क'}
    for err in ('provider_error_resource_exhausted', 'provider_error_unavailable',
                'malformed_response', 'http_429', 'timeout'):
        assert QO._observed(item, {'api_status': 'error', 'error_class': err,
                                   'text': ''}) == QO.INFRASTRUCTURE_OUTCOME
    assert QO.SCIENTIFIC_OUTCOMES == ('match', 'mismatch', 'empty_transcription')


def test_exactness_uses_the_frozen_shared_normalisation():
    item = {'item_id': 'x', 'target': 'कण्डाघाट', 'expected': 'match', 'drawn': 'कण्डाघाट'}
    assert QO._observed(item, {'api_status': 'ok', 'text': '  कण्डाघाट  '}) == 'match'
    assert QO._observed(item, {'api_status': 'ok', 'text': 'कण्ङाघाट'}) == 'mismatch'


# ----------------------------------------------------------------- fake-live positive control
def test_a_clean_synthetic_ocr_candidate_completes_both_scripts_at_zero_spend():
    candidate = QO.FakeOcrCandidate(name='clean')
    guard = BudgetGuard(authorised_usd=Decimal('6.00'))
    result = QO.qualify_ocr_candidate(candidate, guard)

    assert result['devanagari']['calls'] == QO.OCR_CALLS_PER_SCRIPT == 288
    assert result['latin']['calls'] == 288
    assert candidate.calls == QO.OCR_MAX_CALLS_BOTH_SCRIPTS == 576
    assert result['qualified_scope'] == ['devanagari', 'latin']
    assert guard.spent_usd == Decimal('0')
    assert result['may_open_atext'] is False


def test_the_devanagari_screen_has_the_expected_opportunity_split():
    result = QO.qualify_ocr_candidate(QO.FakeOcrCandidate(name='clean'),
                                      guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    dev = result['devanagari']
    assert dev['match_opportunities'] == 144
    assert dev['mismatch_opportunities'] == 144
    assert dev['primary_shape'] == 'transcribe'
    assert dev['total_dispatches'] == 288


# ------------------------------------------------------------------------ negative controls
def test_a_single_false_pass_fails_the_gate_and_blocks_latin():
    candidate = QO.FakeOcrCandidate(name='one-false-pass', false_pass_items={'dx-0002'})
    result = QO.qualify_ocr_candidate(candidate, guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    dev = result['devanagari']
    assert dev['false_passes'] >= 1
    assert 'mismatch_false_pass' in dev['failed_gates']
    assert dev['passed'] is False
    assert result['latin'] is None                  # progressive stop
    assert result['qualified_scope'] == []


def test_widespread_false_fails_trip_the_false_fail_gate():
    # Select REAL match items rather than guessing an id range: the validated view's ids are
    # sparse, so a range guess silently lands under the threshold and the control proves nothing.
    match_items = [i['item_id'] for i in QT._script_items('devanagari')
                   if i['expected'] == 'match']
    assert len(match_items) == 48
    victims = set(match_items[:20])                  # 20/48 -> 0.4167, comfortably over 0.10

    result = QO.qualify_ocr_candidate(
        QO.FakeOcrCandidate(name='over-strict', false_fail_items=victims),
        guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    dev = result['devanagari']
    assert dev['false_fails'] == 60                  # 20 items x 3 repeats
    assert dev['match_false_fail_rate'] > 0.10
    assert 'match_false_fail_rate' in dev['failed_gates']
    assert dev['false_passes'] == 0                  # over-strict is not unsafe, only costly
    assert dev['passed'] is False


def test_empty_transcriptions_can_fail_their_own_gate_and_never_score_as_match():
    """CORRECTION CONTROL 1: an empty successful OCR response is scientific evidence."""
    all_items = [i['item_id'] for i in QT._script_items('devanagari')]
    victims = set(all_items[:10])                    # 10/96 items -> 30/288 = 0.1042 > 0.05

    result = QO.qualify_ocr_candidate(
        QO.FakeOcrCandidate(name='silent', empty_items=victims),
        guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    dev = result['devanagari']

    assert dev['empty_transcriptions'] == 30
    assert dev['unique_empty_transcription_items'] == 10
    assert dev['empty_transcription_rate'] > 0.05
    assert 'empty_transcription_rate' in dev['failed_gates']
    assert dev['false_passes'] == 0                  # silence never became agreement
    assert dev['false_fails'] == 0                   # nor disagreement
    assert dev['infrastructure_failures'] == 0       # it is NOT infrastructure
    assert dev['scientifically_complete'] is True    # the screen DID finish
    assert dev['passed'] is False                    # and it scientifically failed
    assert result['latin'] is None


def test_a_few_empty_transcriptions_stay_under_the_gate():
    all_items = [i['item_id'] for i in QT._script_items('devanagari')]
    result = QO.qualify_ocr_candidate(
        QO.FakeOcrCandidate(name='mostly-fine', empty_items=set(all_items[:4])),
        guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    dev = result['devanagari']
    assert dev['empty_transcriptions'] == 12         # 12/288 = 0.0417
    assert dev['empty_transcription_rate'] <= 0.05
    assert dev['failed_gates'] == []
    assert dev['passed'] is True


def test_a_backend_or_quota_error_stops_scientifically_incomplete():
    """CORRECTION CONTROL 2: infrastructure failure is execution state, not a verdict."""
    result = QO.qualify_ocr_candidate(
        QO.FakeOcrCandidate(name='throttled', infrastructure_items={'dx-0011'},
                            infrastructure_error_class='provider_error_resource_exhausted'),
        guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    dev = result['devanagari']

    assert dev['stopped_reason'] == 'provider_error_resource_exhausted'
    assert dev['infrastructure_failures'] == 1
    assert dev['scientifically_complete'] is False
    assert dev['passed'] is None                     # NOT False
    assert dev['failed_gates'] == []                 # an unfinished screen fails no gate
    assert dev['false_passes'] == 0
    assert dev['false_fails'] == 0
    assert dev['empty_transcriptions'] == 0
    assert dev['empty_transcription_rate'] == 0.0
    assert result['latin'] is None                   # incomplete does not advance
    assert result['qualified_scope'] == []           # nor qualify


def test_an_ambiguous_post_dispatch_failure_stops_incomplete_with_conservative_billing():
    """CORRECTION CONTROL 3."""
    result = QO.qualify_ocr_candidate(
        QO.FakeOcrCandidate(name='reset', infrastructure_items={'dx-0011'},
                            infrastructure_error_class='malformed_response',
                            infrastructure_is_ambiguous=True),
        guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    dev = result['devanagari']

    assert dev['stopped_reason'] == 'ambiguous_dispatch'
    assert dev['scientifically_complete'] is False
    assert dev['passed'] is None
    bad = [r for r in dev['call_records'] if r['ambiguous_dispatch']]
    assert len(bad) == 1
    assert bad[0]['billing_state'] == 'unknown_provisional'
    assert bad[0]['retries'] == 0


def test_no_infrastructure_failure_can_produce_a_scientific_pass_or_fail():
    """CORRECTION CONTROL 5, across every infrastructure class."""
    for err, ambiguous in (('provider_error_resource_exhausted', False),
                           ('provider_error_unavailable', False),
                           ('http_429', False),
                           ('timeout', False),
                           ('malformed_response', True)):
        result = QO.qualify_ocr_candidate(
            QO.FakeOcrCandidate(name=f'infra-{err}', infrastructure_items={'dx-0011'},
                                infrastructure_error_class=err,
                                infrastructure_is_ambiguous=ambiguous),
            guard=BudgetGuard(authorised_usd=Decimal('6.00')))
        dev = result['devanagari']
        assert dev['passed'] is None, err
        assert dev['passed'] is not True and dev['passed'] is not False, err
        assert dev['scientifically_complete'] is False, err


def test_budget_exhaustion_stops_the_ocr_run_incomplete(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, 'k')
    tiny = BudgetGuard(authorised_usd=Decimal('0.0030'))     # two images
    engine = _engine(http=RecordingHttp(OCR.CLOUD_VISION_OK_FIXTURE), guard=tiny)
    candidate = QO.OcrCandidate(engine, name='tiny-budget')
    result = QO._score_script(candidate, 'devanagari', tiny, repeats=3)
    assert result['stopped_reason'] == 'budget_exhausted'
    assert result['scientifically_complete'] is False
    assert result['passed'] is None                  # a budget stop is not a quality verdict
    assert tiny.spent_usd <= tiny.authorised_usd


def test_retries_remain_zero_across_every_persisted_ocr_record():
    result = QO.qualify_ocr_candidate(QO.FakeOcrCandidate(name='clean'),
                                      guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    for script in ('devanagari', 'latin'):
        assert all(r['retries'] == 0 for r in result[script]['call_records'])


# ---------------------------------------------------------------------------- evidence shape
def test_every_field_the_calibration_review_needs_is_persisted():
    result = QO.qualify_ocr_candidate(QO.FakeOcrCandidate(name='clean'),
                                      guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    obs = result['devanagari']['observations']
    assert len(obs) == 288
    for key in ('item_id', 'shape', 'pass', 'expected', 'observed', 'api_status',
                'target', 'rendered_string', 'ocr_transcription', 'failure_class',
                'failure_group', 'edit_detail', 'image_sha256', 'provider_request_id',
                'cost_basis'):
        assert key in obs[0], key


def test_the_ocr_fingerprint_binds_contract_config_outcomes_and_call_records():
    run = type('R', (), {'run_id': 'ocr-test', 'mode': 'fake_live'})()
    result = QO.qualify_ocr_candidate(QO.FakeOcrCandidate(name='clean'),
                                      guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    payload = QO.build_ocr_qualification_result(run, [result])

    assert payload['contract_version'] == 'ocr-1'
    assert payload['contract_sha256'] == QO.ocr_contract_sha256()
    assert payload['config_sha256']
    assert payload['evidence_fingerprint'] == QO.ocr_qualification_fingerprint(payload)

    for mutate in (
        lambda p: p['candidates'][0]['devanagari']['observations'].__setitem__(
            0, {**p['candidates'][0]['devanagari']['observations'][0], 'observed': 'match'}),
        lambda p: p['call_records'].__setitem__(
            0, {**p['call_records'][0], 'item_id': 'tampered'}),
        lambda p: p.__setitem__('contract_sha256', 'a' * 64),
        lambda p: p.__setitem__('config_sha256', 'b' * 64),
        lambda p: p.__setitem__('qualified', [{'candidate': 'invented'}]),
    ):
        tampered = copy.deepcopy(payload)
        mutate(tampered)
        assert QO.ocr_qualification_fingerprint(tampered) != payload['evidence_fingerprint']


# ----------------------------------------------------------------------------- budget proof
def test_the_conservative_paid_maximum_fits_the_qualification_cap():
    proof = QO.ocr_budget_projection('0.6712415')
    assert proof['usd_per_image'] == '0.0015'
    assert proof['devanagari_calls'] == 288
    assert proof['latin_calls'] == 288
    assert proof['max_calls'] == 576
    assert Decimal(proof['max_ocr_reservation_usd']) == Decimal('0.864')
    assert Decimal(proof['prospective_cumulative_usd']) == Decimal('1.5352415')
    assert Decimal(proof['prospective_cumulative_usd']) <= Decimal('6.00')
    assert proof['free_tier_relied_on'] is False


def test_the_free_tier_is_not_used_in_the_mechanical_budget():
    # 576 images at the PAID rate. If the first 1000 were assumed free this would be zero.
    assert OCR.CLOUD_VISION_USD_PER_IMAGE * 576 == Decimal('0.864')


# ----------------------------------------------------------------------- contract isolation
def test_the_historical_vlm_contracts_are_untouched_by_this_family():
    v1 = QT.HERE / 'qualification-contract-v1.yaml'
    v2 = QT.HERE / 'qualification-contract-v2.yaml'
    assert v1.exists() and v2.exists()
    assert QT.contract()['contract_version'] == 2          # the VLM runner still loads v2
    assert QO.ocr_contract()['contract_version'] == 'ocr-1'
    assert QO.ocr_contract()['contract_family'] == 'ocr'


def test_the_ocr_contract_keeps_the_numerical_thresholds_and_adds_no_verdict_shape():
    c = QO.ocr_contract()
    assert c['mismatch_false_pass_max'] == 0
    assert c['match_false_fail_rate_max'] == 0.10
    assert c['empty_transcription_rate_max'] == 0.05
    assert c['repeat_consistency_min'] == 0.95
    assert 'refusal_rate_max' not in c              # replaced by the scientific gate
    assert c['repeats_per_shape'] == 3
    assert c['gate_scope']['qualifying_shape'] == 'transcribe'
    assert c['gate_scope']['diagnostic_shapes'] == []
    assert list(c['shapes']) == ['transcribe']
    assert c['empty_transcription_is_failure'] is True
    assert c['progressive_stop']['order'] == ['devanagari', 'latin']
    assert c['retries_authorised'] == 0


# -------------------------------------------------------------------------- A-TEXT boundary
def test_ocr_evidence_cannot_open_atex(tmp_path):
    """Feed a PERFECT OCR record straight into the A-TEXT handoff. It must still refuse."""
    import run_atex as A

    run = type('R', (), {'run_id': 'ocr-test', 'mode': 'live', 'evidence_dir': tmp_path})()
    result = QO.qualify_ocr_candidate(QO.FakeOcrCandidate(name='clean'),
                                      guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    payload = QO.build_ocr_qualification_result(run, [result])
    # Dress it up as convincingly as a forger could: live mode, not synthetic, fingerprint valid.
    payload['mode'] = 'live'
    payload['synthetic'] = False
    payload['evidence_fingerprint'] = QO.ocr_qualification_fingerprint(payload)
    (tmp_path / QT.QUALIFICATION_FILENAME).write_text(
        json.dumps(payload, ensure_ascii=False, default=str), encoding='utf-8')

    with pytest.raises(A.GateClosed) as exc:
        A.load_qualification(run, expected_mode='live')
    assert 'ocr' in str(exc.value)
    assert A.ACCEPTED_QUALIFICATION_FAMILY == 'vlm'


def test_the_family_gate_fires_before_the_version_gate(tmp_path):
    """The refusal must name the family, not merely trip over a version string.

    If a future OCR contract ever chose `contract_version: 2`, the version check would pass and
    the only thing standing between OCR evidence and a paid stage would be this gate.
    """
    import run_atex as A

    run = type('R', (), {'run_id': 'ocr-test', 'mode': 'live', 'evidence_dir': tmp_path})()
    result = QO.qualify_ocr_candidate(QO.FakeOcrCandidate(name='clean'),
                                      guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    payload = QO.build_ocr_qualification_result(run, [result])
    payload['mode'] = 'live'
    payload['synthetic'] = False
    payload['contract_version'] = QT.contract()['contract_version']          # forged to match
    payload['contract_sha256'] = __import__('hashlib').sha256(
        QT.CONTRACT.read_bytes()).hexdigest()                                # forged to match
    payload['evidence_fingerprint'] = QO.ocr_qualification_fingerprint(payload)
    (tmp_path / QT.QUALIFICATION_FILENAME).write_text(
        json.dumps(payload, ensure_ascii=False, default=str), encoding='utf-8')

    with pytest.raises(A.GateClosed) as exc:
        A.load_qualification(run, expected_mode='live')
    assert 'ocr' in str(exc.value)


def test_the_ocr_contract_declares_itself_unaccepted_by_atext():
    assert QO.ocr_contract()['atext_handoff']['accepted_by_atext'] is False


def test_a_qualified_ocr_result_still_refuses_to_open_atext():
    result = QO.qualify_ocr_candidate(QO.FakeOcrCandidate(name='clean'),
                                      guard=BudgetGuard(authorised_usd=Decimal('6.00')))
    assert result['qualified_scope'] == ['devanagari', 'latin']   # a perfect candidate
    assert result['may_open_atext'] is False                      # and still no A-TEXT
    assert result['may_populate_registry'] is False


# ---------------------------------------------------------------------------------- registry
def test_the_registry_is_untouched_by_ocr_readiness():
    registry = QT.REPO_ROOT / 'eval' / 'registry' / 'registry-v1.jsonl'
    rows = [x for x in registry.read_text(encoding='utf-8').splitlines()
            if x.strip() and not x.startswith('#')]
    assert rows == []
