"""Provider-specific transport and authentication controls (EVAL-013 B5).

The EVAL-012 branch sent `Authorization: Bearer <key>` to every provider. For the Gemini API-key
route that is simply the wrong header — Google documents `x-goog-api-key` — so the first real
Gemini call would have failed on authentication, after being counted as a trial and possibly
billed. One generic transport was hiding two different contracts.

Everything below is inspected through an injected HTTP recorder. No request leaves the process:
the recorder IS the network boundary, and it never opens a socket.
"""
import json
import os
import socket

import pytest

import providers as P


OPENAI_VERSION = 'gpt-5.4-mini-2026-07-01'
GEMINI_VERSION = 'gemini-3.5-flash-lite-001'
IMAGE = b'\x89PNG\r\n\x1a\n-not-a-real-image-'


class RecordingHttp:
    """Stands exactly where the socket would be. Records the call and returns a fixture."""

    def __init__(self, response: dict):
        self.response = response
        self.calls = []

    def __call__(self, url, headers, body, timeout_s):
        self.calls.append({'url': url, 'headers': dict(headers), 'body': body,
                           'timeout_s': timeout_s})
        return json.loads(json.dumps(self.response))


@pytest.fixture
def openai_key(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'sk-test-openai-key')


@pytest.fixture
def google_key(monkeypatch):
    monkeypatch.setenv('GOOGLE_API_KEY', 'AIza-test-google-key')


# ------------------------------------------------------------------ no network on construction
def test_constructing_a_transport_opens_no_socket(monkeypatch):
    def explode(*a, **k):
        raise AssertionError('a transport constructor attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)

    P.OpenAIHttpTransport(resolved_version=OPENAI_VERSION)
    P.GeminiHttpTransport(resolved_version=GEMINI_VERSION)


def test_constructing_a_transport_reads_no_key():
    reads = []

    class Tracking(dict):
        def get(self, k, default=None):
            reads.append(k)
            return super().get(k, default)

    real = os.environ
    try:
        os.environ = Tracking(real)  # noqa: B003
        P.OpenAIHttpTransport(resolved_version=OPENAI_VERSION)
        P.GeminiHttpTransport(resolved_version=GEMINI_VERSION)
    finally:
        os.environ = real  # noqa: B003
    assert not [r for r in reads if 'KEY' in r.upper()], reads


# ------------------------------------------------------------------------------ OpenAI auth
def test_openai_sends_a_bearer_authorization_header(openai_key):
    http = RecordingHttp(P.OPENAI_OK_FIXTURE)
    t = P.OpenAIHttpTransport(resolved_version=OPENAI_VERSION, http=http)
    t({'model': OPENAI_VERSION, 'input': []})

    headers = http.calls[0]['headers']
    assert headers['Authorization'] == 'Bearer sk-test-openai-key'
    assert headers['Content-Type'] == 'application/json'
    assert 'x-goog-api-key' not in {k.lower() for k in headers}


def test_openai_posts_to_the_responses_endpoint(openai_key):
    http = RecordingHttp(P.OPENAI_OK_FIXTURE)
    P.OpenAIHttpTransport(resolved_version=OPENAI_VERSION, http=http)({'model': OPENAI_VERSION})
    assert http.calls[0]['url'] == 'https://api.openai.com/v1/responses'


def test_openai_carries_the_exact_resolved_version_in_the_body(openai_key):
    http = RecordingHttp(P.OPENAI_OK_FIXTURE)
    P.OpenAIHttpTransport(resolved_version=OPENAI_VERSION, http=http)({'model': OPENAI_VERSION})
    assert json.loads(http.calls[0]['body'])['model'] == OPENAI_VERSION


# ------------------------------------------------------------------------------ Gemini auth
def test_gemini_sends_x_goog_api_key_and_never_a_bearer_header(google_key):
    """The whole point of B5."""
    http = RecordingHttp(P.GEMINI_OK_FIXTURE)
    t = P.GeminiHttpTransport(resolved_version=GEMINI_VERSION, http=http)
    t({'model': GEMINI_VERSION, 'contents': []})

    headers = http.calls[0]['headers']
    assert headers['x-goog-api-key'] == 'AIza-test-google-key'
    assert 'Authorization' not in headers
    assert not any(str(v).startswith('Bearer') for v in headers.values())


def test_gemini_url_is_derived_from_the_exact_resolved_version(google_key):
    http = RecordingHttp(P.GEMINI_OK_FIXTURE)
    P.GeminiHttpTransport(resolved_version=GEMINI_VERSION, http=http)({'model': GEMINI_VERSION})
    assert http.calls[0]['url'] == (
        f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_VERSION}'
        ':generateContent')


def test_gemini_url_never_silently_uses_a_floating_alias(google_key):
    """An alias in the URL is a different experiment every time the vendor repoints it."""
    http = RecordingHttp(P.GEMINI_OK_FIXTURE)
    P.GeminiHttpTransport(resolved_version=GEMINI_VERSION, http=http)({'model': GEMINI_VERSION})
    assert 'gemini-3.5-flash-lite:' not in http.calls[0]['url']


def test_gemini_refuses_a_body_naming_a_different_model(google_key):
    http = RecordingHttp(P.GEMINI_OK_FIXTURE)
    t = P.GeminiHttpTransport(resolved_version=GEMINI_VERSION, http=http)
    with pytest.raises(P.DispatchRefused):
        t({'model': 'some-other-version', 'contents': []})
    assert http.calls == []


def test_gemini_does_not_repeat_the_model_in_the_body(google_key):
    """The REST route names the model in the URL; leaving it in the body is duplicate truth."""
    http = RecordingHttp(P.GEMINI_OK_FIXTURE)
    P.GeminiHttpTransport(resolved_version=GEMINI_VERSION, http=http)(
        {'model': GEMINI_VERSION, 'contents': [{'parts': []}]})
    assert 'model' not in json.loads(http.calls[0]['body'])


# ---------------------------------------------------------------- secrets discipline
@pytest.mark.parametrize('cls,env,version', [
    (P.OpenAIHttpTransport, 'OPENAI_API_KEY', OPENAI_VERSION),
    (P.GeminiHttpTransport, 'GOOGLE_API_KEY', GEMINI_VERSION),
])
def test_a_missing_key_refuses_before_any_dispatch(monkeypatch, cls, env, version):
    monkeypatch.delenv(env, raising=False)
    http = RecordingHttp({})
    with pytest.raises(P.DispatchRefused) as e:
        cls(resolved_version=version, http=http)({'model': version})
    assert http.calls == []
    assert env in str(e.value)


@pytest.mark.parametrize('cls,version,fixture', [
    (P.OpenAIHttpTransport, OPENAI_VERSION, P.OPENAI_OK_FIXTURE),
    (P.GeminiHttpTransport, GEMINI_VERSION, P.GEMINI_OK_FIXTURE),
])
def test_the_key_never_appears_in_the_request_body(openai_key, google_key, cls, version, fixture):
    http = RecordingHttp(fixture)
    cls(resolved_version=version, http=http)({'model': version, 'contents': [], 'input': []})
    body = http.calls[0]['body'].decode('utf-8')
    assert 'sk-test-openai-key' not in body
    assert 'AIza-test-google-key' not in body


@pytest.mark.parametrize('cls,version,fixture', [
    (P.OpenAIHttpTransport, OPENAI_VERSION, P.OPENAI_OK_FIXTURE),
    (P.GeminiHttpTransport, GEMINI_VERSION, P.GEMINI_OK_FIXTURE),
])
def test_no_key_reaches_a_persisted_call_record(openai_key, google_key, cls, version, fixture):
    judge_cls = P.OpenAITextJudge if cls is P.OpenAIHttpTransport else P.GeminiTextJudge
    from decimal import Decimal
    from budget_guard import BudgetGuard
    j = judge_cls(model_alias='alias', resolved_version=version,
                  transport=cls(resolved_version=version, http=RecordingHttp(fixture)),
                  guard=BudgetGuard(authorised_usd=Decimal('10.00')))
    blob = json.dumps(j.call_record(j.transcribe(IMAGE), shape='transcribe'))
    assert 'sk-test-openai-key' not in blob and 'AIza-test-google-key' not in blob


# ---------------------------------------------------------------- one dispatch, no retry
@pytest.mark.parametrize('cls,version,fixture', [
    (P.OpenAIHttpTransport, OPENAI_VERSION, P.OPENAI_OK_FIXTURE),
    (P.GeminiHttpTransport, GEMINI_VERSION, P.GEMINI_OK_FIXTURE),
])
def test_one_call_produces_exactly_one_http_dispatch(openai_key, google_key, cls, version,
                                                     fixture):
    http = RecordingHttp(fixture)
    cls(resolved_version=version, http=http)({'model': version, 'contents': [], 'input': []})
    assert len(http.calls) == 1


@pytest.mark.parametrize('cls,version,fixture', [
    (P.OpenAIHttpTransport, OPENAI_VERSION, P.OPENAI_ERROR_FIXTURE),
    (P.GeminiHttpTransport, GEMINI_VERSION, P.GEMINI_ERROR_FIXTURE),
])
def test_an_error_response_is_not_retried(openai_key, google_key, cls, version, fixture):
    http = RecordingHttp(fixture)
    cls(resolved_version=version, http=http)({'model': version, 'contents': [], 'input': []})
    assert len(http.calls) == 1


def test_a_transport_requires_a_resolved_version():
    with pytest.raises(ValueError):
        P.GeminiHttpTransport(resolved_version='')
