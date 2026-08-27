"""Frozen fal generation-route controls (EVAL-013 C).

IMG-01 and IMG-02 are frozen routes with frozen configuration. The risk this guards is a route
that quietly drifts — a different size, a different rendering speed, a seed appearing where the
experiment declared unseeded repeats — because then two halves of one comparison are no longer
comparable and nobody can tell from the result.

fal is never contacted. Every dispatch goes through an injected HTTP recorder, and every artifact
comes from an injected fetcher.
"""
import json
import socket

import pytest
import yaml

import providers as P
from pathlib import Path

CONFIG = yaml.safe_load(
    (Path(__file__).resolve().parents[1] / 'config.yaml').read_text(encoding='utf-8'))

PROMPT = 'A plain square poster. The only textual content is: शुभ दीपावली'


class RecordingHttp:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def __call__(self, url, headers, body, timeout_s):
        self.calls.append({'url': url, 'headers': dict(headers), 'body': body})
        return json.loads(json.dumps(self.response))


@pytest.fixture
def fal_key(monkeypatch):
    monkeypatch.setenv('FAL_KEY', 'fal-test-key-123')


def route(slot, http, **kw):
    return P.FalImageRoute(slot=slot, route=CONFIG['atex']['slots'][slot]['route'],
                           http=http, **kw)


# ------------------------------------------------------------------ nothing on construction
def test_construction_opens_no_socket_and_reads_no_key(monkeypatch):
    def explode(*a, **k):
        raise AssertionError('a fal route constructor attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)
    monkeypatch.delenv('FAL_KEY', raising=False)

    route('IMG-01', RecordingHttp(P.FAL_OK_FIXTURE))
    route('IMG-02', RecordingHttp(P.FAL_OK_FIXTURE))


def test_a_missing_fal_key_refuses_before_any_dispatch(monkeypatch):
    monkeypatch.delenv('FAL_KEY', raising=False)
    http = RecordingHttp(P.FAL_OK_FIXTURE)
    with pytest.raises(P.DispatchRefused) as e:
        route('IMG-01', http)({'prompt': PROMPT})
    assert http.calls == []
    assert 'FAL_KEY' in str(e.value)


# ------------------------------------------------------------------------------ frozen routes
def test_img01_posts_to_the_frozen_gpt_image_2_route(fal_key):
    http = RecordingHttp(P.FAL_OK_FIXTURE)
    route('IMG-01', http)({'prompt': PROMPT})
    assert http.calls[0]['url'] == 'https://fal.run/openai/gpt-image-2'


def test_img02_posts_to_the_frozen_ideogram_v3_route(fal_key):
    http = RecordingHttp(P.FAL_OK_FIXTURE)
    route('IMG-02', http)({'prompt': PROMPT})
    assert http.calls[0]['url'] == 'https://fal.run/fal-ai/ideogram/v3'


def test_fal_uses_key_authorization_not_bearer(fal_key):
    http = RecordingHttp(P.FAL_OK_FIXTURE)
    route('IMG-01', http)({'prompt': PROMPT})
    assert http.calls[0]['headers']['Authorization'] == 'Key fal-test-key-123'


def test_img01_body_is_frozen_at_1024x1024_medium(fal_key):
    http = RecordingHttp(P.FAL_OK_FIXTURE)
    route('IMG-01', http)({'prompt': PROMPT})
    body = json.loads(http.calls[0]['body'])
    assert body['prompt'] == PROMPT
    assert body['image_size'] == {'width': 1024, 'height': 1024}
    assert body['quality'] == 'medium'
    assert body['num_images'] == 1


def test_img02_body_is_frozen_at_balanced(fal_key):
    http = RecordingHttp(P.FAL_OK_FIXTURE)
    route('IMG-02', http)({'prompt': PROMPT})
    body = json.loads(http.calls[0]['body'])
    assert body['prompt'] == PROMPT
    assert body['rendering_speed'] == 'BALANCED'
    assert body['num_images'] == 1


def test_no_seed_is_ever_sent_on_either_route(fal_key):
    """A-TEXT repeats are unseeded on BOTH routes, even where a route exposes a seed."""
    for slot in ('IMG-01', 'IMG-02'):
        http = RecordingHttp(P.FAL_OK_FIXTURE)
        route(slot, http)({'prompt': PROMPT, 'seed': 12345, 'seed_policy': 'unseeded'})
        assert 'seed' not in json.loads(http.calls[0]['body'])


def test_an_unknown_slot_is_refused():
    with pytest.raises(ValueError):
        P.FalImageRoute(slot='IMG-99', route='whatever/route')


def test_a_route_that_disagrees_with_the_frozen_config_is_refused():
    with pytest.raises(ValueError):
        P.FalImageRoute(slot='IMG-01', route='fal-ai/some-other-model')


def test_the_key_never_reaches_the_request_body(fal_key):
    http = RecordingHttp(P.FAL_OK_FIXTURE)
    route('IMG-01', http)({'prompt': PROMPT})
    assert 'fal-test-key-123' not in http.calls[0]['body'].decode('utf-8')


# ------------------------------------------------------------------------------ responses
def test_an_ok_response_yields_a_persistable_record(fal_key):
    r = route('IMG-01', RecordingHttp(P.FAL_OK_FIXTURE))({'prompt': PROMPT})
    assert r['api_status'] == 'ok'
    assert r['artifact_url']
    assert r['provider_request_id'] == 'fal-req-001'
    assert r['error_class'] is None


def test_a_content_policy_response_is_a_refusal_not_an_error(fal_key):
    r = route('IMG-01', RecordingHttp(P.FAL_REFUSAL_FIXTURE))({'prompt': PROMPT})
    assert r['api_status'] == 'refusal'
    assert r['error_class'] == 'moderation_block'
    assert r['artifact_url'] is None


def test_an_error_response_is_recorded_as_an_error(fal_key):
    r = route('IMG-02', RecordingHttp(P.FAL_ERROR_FIXTURE))({'prompt': PROMPT})
    assert r['api_status'] == 'error'
    assert r['error_class']
    assert r['artifact_url'] is None


def test_one_attempt_is_exactly_one_dispatch_even_on_error(fal_key):
    for fixture in (P.FAL_OK_FIXTURE, P.FAL_REFUSAL_FIXTURE, P.FAL_ERROR_FIXTURE):
        http = RecordingHttp(fixture)
        route('IMG-01', http)({'prompt': PROMPT})
        assert len(http.calls) == 1


# ------------------------------------------------------------------------------ artifacts
def test_an_artifact_is_fetched_through_the_injected_layer(fal_key):
    fetched = []

    def fake_fetch(url):
        fetched.append(url)
        return b'\x89PNG\r\n\x1a\nFAKE'

    r = route('IMG-01', RecordingHttp(P.FAL_OK_FIXTURE), artifact_fetch=fake_fetch)(
        {'prompt': PROMPT})
    data = r['fetch_artifact']()
    assert data.startswith(b'\x89PNG')
    assert fetched == [r['artifact_url']]


def test_no_artifact_fetch_happens_when_the_call_refused(fal_key):
    fetched = []
    r = route('IMG-01', RecordingHttp(P.FAL_REFUSAL_FIXTURE),
              artifact_fetch=lambda u: fetched.append(u))({'prompt': PROMPT})
    assert r['fetch_artifact'] is None
    assert fetched == []


def test_the_route_records_its_identity_for_persistence(fal_key):
    r = route('IMG-01', RecordingHttp(P.FAL_OK_FIXTURE))({'prompt': PROMPT})
    assert r['slot'] == 'IMG-01'
    assert r['route'] == 'openai/gpt-image-2'
    assert r['provider_surface'] == 'fal'
    assert json.dumps({k: v for k, v in r.items() if k != 'fetch_artifact'})
