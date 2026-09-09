"""THE ONLY module in eval/harness-v2 that may open a socket or run a network-capable subprocess.

    FalQueueTransport / VertexTransport / SarvamTransport /  urllib, called only from an adapter's
    ElevenLabsTransport                                      dispatch, never from construction
    GcloudServiceAccountTokenSource                          `gcloud auth activate-service-account`
                                                             + `gcloud auth print-access-token`
                                                             inside a throw-away CLOUDSDK_CONFIG,
                                                             at dispatch only; the token lives in
                                                             memory for one dispatch and is never
                                                             written, logged or put in a record
    FakeTransport / FakeTokenSource                          recorders for tests; open nothing

Every live class counts its calls so a silent retry would show. Construction opens nothing and
reads nothing. None of the live paths has been exercised against a provider - the zero-spend rule
forbids it tonight - so the real path is unproven until the first authorised call.

A grep for urllib / http.client / socket / subprocess over the package must hit this file only
(Tester check 2); the instruments run ffmpeg/ffprobe via subprocess for LOCAL decoding, which is
the one other permitted subprocess use and lives in instruments/imageio.py.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

import hv2_paths  # noqa: F401
from providers import PreDispatchRefusal  # noqa: E402


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """AF-7: a 3xx is returned as the provider's ANSWER; the request (and its Authorization header) is never
    replayed to the redirect target, so a credential can never be forwarded across hosts."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def nothing_left_the_machine(exc: BaseException) -> bool:
    """True only for a name-resolution failure: the socket was never connected, so no byte reached the provider.
    Lives here because it is the one exception classification that needs the network modules (hygiene rule:
    network symbols only in transports.py)."""
    import socket
    import urllib.error
    if isinstance(exc, socket.gaierror):
        return True
    if isinstance(exc, urllib.error.URLError) and isinstance(getattr(exc, "reason", None), socket.gaierror):
        return True
    return False


def build_opener():
    return urllib.request.build_opener(NoRedirectHandler)


class _UrllibTransport:
    """Four verbs. An HTTP error status (a 3xx included) is a provider ANSWER and is returned, not raised."""

    name = "urllib"

    def __init__(self, timeout_s: float = 120.0):
        self.timeout_s = timeout_s
        self.calls = 0
        self.opener = build_opener()

    def _open(self, req):
        self.calls += 1
        try:
            with self.opener.open(req, timeout=self.timeout_s) as resp:
                return resp.status, resp.read(), resp.headers.get("Content-Type")
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read(), exc.headers.get("Content-Type")

    def _open_with_headers(self, req):
        """Like _open, but also returns the response headers (lower-cased names) for providers that put the
        request / job id in a header instead of a JSON body (ElevenLabs: request-id, song-id)."""
        self.calls += 1
        try:
            with self.opener.open(req, timeout=self.timeout_s) as resp:
                return resp.status, resp.read(), resp.headers.get("Content-Type"), {k.lower(): v for k, v in resp.headers.items()}
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read(), exc.headers.get("Content-Type"), {k.lower(): v for k, v in exc.headers.items()}

    def post_json(self, url: str, headers: dict, payload: bytes) -> tuple[int, dict]:
        status, body, _ = self._open(urllib.request.Request(
            url, data=payload, method="POST",
            headers={"Content-Type": "application/json", **headers}))
        return status, _parse_json(body)

    def get_json(self, url: str, headers: dict) -> tuple[int, dict]:
        status, body, _ = self._open(urllib.request.Request(url, headers=headers, method="GET"))
        return status, _parse_json(body)

    def get_bytes(self, url: str, headers: dict) -> tuple[int, bytes, str | None]:
        return self._open(urllib.request.Request(url, headers=headers, method="GET"))

    def post_bytes(self, url: str, headers: dict, payload: bytes) -> tuple[int, bytes, str | None, dict]:
        """A JSON POST whose ANSWER is raw bytes (audio), not JSON: (status, body_bytes, content_type, response_headers).
        Exactly one request, like post_json; an error status comes back with the provider's error body bytes."""
        return self._open_with_headers(urllib.request.Request(
            url, data=payload, method="POST", headers={"Content-Type": "application/json", **headers}))


def _parse_json(body: bytes) -> dict:
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"$unparseable_body": True, "$bytes": len(body)}


class FalQueueTransport(_UrllibTransport):
    """queue.fal.run submit / status / response, then the CDN download. `Authorization: Key ...`."""
    name = "fal_queue"


class VertexTransport(_UrllibTransport):
    """Vertex AI REST with `Authorization: Bearer <access token>`."""
    name = "vertex"


class SarvamTransport(_UrllibTransport):
    """api.sarvam.ai with `api-subscription-key`."""
    name = "sarvam"


class ElevenLabsTransport(_UrllibTransport):
    """api.elevenlabs.io with `xi-api-key`; the answer is audio bytes (post_bytes), never a JSON envelope."""
    name = "elevenlabs"


class GcloudServiceAccountTokenSource:
    """An access token from a service-account key file, via the gcloud CLI, at dispatch only.

    No pure-Python JWT signing: no crypto library is importable on this machine and hand-written
    RSA is forbidden. The gcloud config directory is a fresh temporary directory that is deleted
    afterwards, so the machine's default gcloud configuration (a Wherehouse account) is never
    read or written (EVAL-039B practice).
    """

    def __init__(self, credential_file: Path | str, gcloud_bin: str = "gcloud", runner=None,
                 timeout_s: float = 60.0):
        self.credential_file = Path(credential_file).expanduser()
        self.credential_file_name = str(credential_file)          # NAME is recorded, never contents
        self.gcloud_bin = gcloud_bin
        self.runner = runner or subprocess.run
        self.timeout_s = timeout_s
        self.calls = 0

    def token(self) -> str:
        if not self.credential_file.exists():
            raise PreDispatchRefusal(
                f"credential file {self.credential_file_name} does not exist; nothing was sent")
        self.calls += 1
        tmp = tempfile.mkdtemp(prefix="hv2-gcloud-")
        env = {**os.environ, "CLOUDSDK_CONFIG": tmp, "CLOUDSDK_CORE_DISABLE_PROMPTS": "1"}
        try:
            r = self.runner([self.gcloud_bin, "auth", "activate-service-account", "--key-file",
                             str(self.credential_file)], env=env, capture_output=True, text=True,
                            timeout=self.timeout_s)
            if r.returncode != 0:
                raise PreDispatchRefusal(
                    f"gcloud auth activate-service-account failed (exit {r.returncode}); nothing was sent")
            r = self.runner([self.gcloud_bin, "auth", "print-access-token"], env=env,
                            capture_output=True, text=True, timeout=self.timeout_s)
            if r.returncode != 0 or not (r.stdout or "").strip():
                raise PreDispatchRefusal(
                    f"gcloud auth print-access-token failed (exit {r.returncode}); nothing was sent")
            return r.stdout.strip()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
            if os.path.exists(tmp):                                   # AF-13: a leftover throw-away config is named, never silent
                raise RuntimeError(f"throw-away gcloud config directory {tmp} could not be removed; delete it by hand")


# ------------------------------------------------------------------------------- fakes
class FakeTokenSource:
    def __init__(self, credential_file_name: str = "FAKE-credential-file.json", token: str = "FAKE-TOKEN-NOT-A-CREDENTIAL"):
        self.credential_file_name = credential_file_name
        self._token = token
        self.calls = 0

    def token(self) -> str:
        self.calls += 1
        return self._token


class FakeTransport:
    """Scripted provider-shaped answers. Opens nothing. Records every call.

    `posts`, `gets`, `downloads` are lists consumed in order; an item that is an Exception
    instance is RAISED at that step (where a real socket failure would surface). When a list
    runs out the last item is replayed, so a bounded poll loop can be exhausted by design.
    `on_call(kind, url)` is an optional hook a test uses to assert ledger state at send time.
    """

    name = "fake"

    def __init__(self, posts=None, gets=None, downloads=None, on_call=None):
        self.posts = list(posts or [])
        self.gets = list(gets or [])
        self.downloads = list(downloads or [])
        self.on_call = on_call
        self.calls: list[dict] = []
        self._pi = self._gi = self._di = 0

    @property
    def submits(self) -> int:
        return sum(1 for c in self.calls if c["kind"] == "post")

    def _next(self, items, idx_name):
        idx = getattr(self, idx_name)
        if not items:
            raise AssertionError("FakeTransport has no scripted answer for this step")
        step = items[min(idx, len(items) - 1)]
        setattr(self, idx_name, idx + 1)
        if isinstance(step, BaseException):
            raise step
        return step

    def _record(self, kind, url, headers, payload=None):
        self.calls.append({"kind": kind, "url": url, "headers": dict(headers or {}), "payload": payload})
        if self.on_call:
            self.on_call(kind, url)

    def post_json(self, url, headers, payload):
        self._record("post", url, headers, payload)
        return self._next(self.posts, "_pi")

    def get_json(self, url, headers):
        self._record("get", url, headers)
        return self._next(self.gets, "_gi")

    def get_bytes(self, url, headers):
        self._record("download", url, headers)
        return self._next(self.downloads, "_di")

    def post_bytes(self, url, headers, payload):
        """Scripted from the same `posts` list (it is a submit and counts as one): each item is
        (status, body_bytes, content_type, response_headers) or an Exception to raise."""
        self._record("post", url, headers, payload)
        return self._next(self.posts, "_pi")


FakeQueueTransport = FakeTransport
FakeVertexTransport = FakeTransport
FakeSarvamTransport = FakeTransport
FakeElevenLabsTransport = FakeTransport


# ------------------------------------------------------------------------------- Gemini Developer API (2026-09-09)
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"


def gemini_generate_content_url(model: str) -> str:
    """`models/{model}:generateContent` on the Gemini Developer API. The model id is the caller's config, not a claim."""
    if not model or "/" in model or ":" in model or any(ch.isspace() for ch in model):
        raise PreDispatchRefusal(f"gemini model id {model!r} is not a bare model name; nothing was sent")
    return f"{GEMINI_API_BASE}/models/{model}:generateContent"


class GeminiApiTransport(_UrllibTransport):
    """generativelanguage.googleapis.com with `x-goog-api-key`; JSON in, JSON out (Controller decision
    CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09: Gemini-named models run on the key NAMED GOOGLE_API_KEY, never
    Vertex). One `generate_content` = one POST through `post_json`, so `FakeTransport` (which scripts `post_json`)
    stands in for it unchanged: the instrument calls `transport.post_json(url, headers, payload)` and nothing else.
    The key value travels in the header of that one request; it is never in the URL, the body, a log or a record."""
    name = "gemini_api"

    def generate_content(self, model: str, body: dict, api_key: str) -> tuple[int, dict]:
        return self.post_json(gemini_generate_content_url(model), {"x-goog-api-key": api_key},
                              json.dumps(body, ensure_ascii=False).encode("utf-8"))


FakeGeminiApiTransport = FakeTransport
