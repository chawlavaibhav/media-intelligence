"""Provider adapters for the P1 routes — promoted once from the Mokobara job kit
(agency/jobs/AGY-2026-09-21-MOKOBARA-ODYSSEY-001/tools/dispatch.py + _common.py, which were copied
job to job from Cumin B → Lane A → CQ-001 → Mokobara). Request/response shapes are unchanged.

Routes (cells and evidence from eval/capability-map/TAINT-REGISTER-v1.yaml as recorded in that tool):
  nano-banana-2      IMG-CORE/nano-banana-2        gemini-3.1-flash-image     Gemini API   per image
  veo-3.1-fast-i2v   VID-I2V/veo-3.1-fast-i2v      veo-3.1-fast-generate-001  Vertex       per second
  lyria              MUS/lyria+native              lyria-002                  Vertex       per clip
The still-with-reference-photos use of nano-banana-2 is `manual_only`/unregistered in the taint
register (P1 assessment item 11); it is the method every accepted job used, and each beta job's
observations feed the register through the existing (human) promotion rule.

An adapter never touches money: dispatch.py reserves before `submit`, settles after.
Outcomes: ProviderResult(status ok|failed|pending, data, request_ref, http_status, message).
"""
from __future__ import annotations

import base64
import json
import math
import struct
import subprocess
import threading
import time
import urllib.error
import urllib.request
import wave
from dataclasses import dataclass, field
from pathlib import Path

from product.config import Settings, scrub

ROUTES = {
    "nano-banana-2": {"model": "gemini-3.1-flash-image", "surface": "gemini_api", "cell": "IMG-CORE/nano-banana-2",
                      "kind": "image", "evidence": "clean_observed 7/8; with reference photos: manual_only (unregistered)"},
    "veo-3.1-fast-i2v": {"model": "veo-3.1-fast-generate-001", "surface": "vertex", "cell": "VID-I2V/veo-3.1-fast-i2v",
                         "kind": "video", "evidence": "clean_observed 5/8"},
    "lyria": {"model": "lyria-002", "surface": "vertex", "cell": "MUS/lyria+native", "kind": "audio",
              "evidence": "clean_observed 4/4"},
}
VEO_DURATIONS = (4, 6, 8)


@dataclass
class ProviderResult:
    status: str                       # ok | failed | pending
    data: bytes | None = None
    content_type: str | None = None
    request_ref: str | None = None
    http_status: int | None = None
    message: str = ""
    timed_out: bool = False
    meta: dict = field(default_factory=dict)


def _http_json(method, url, headers, payload=None, timeout=300.0):
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"$unparseable_body": scrub(raw[:400])}
    except (TimeoutError, urllib.error.URLError) as e:
        return None, {"$error": scrub(str(e)), "$timeout": "timed out" in str(e).lower()}


# ── Vertex service-account token (JWT bearer grant; replaces the job kit's gcloud subprocess) ─────────
_TOKEN_LOCK = threading.Lock()
_TOKEN: dict = {}


def vertex_token(sa_json_path: str) -> str:
    with _TOKEN_LOCK:
        if _TOKEN.get("exp", 0) > time.time() + 120:
            return _TOKEN["tok"]
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        sa = json.loads(Path(sa_json_path).read_text())
        now = int(time.time())
        b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=")
        head = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
        claim = b64(json.dumps({"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/cloud-platform",
                                "aud": sa["token_uri"], "iat": now, "exp": now + 3600}).encode())
        key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
        sig = b64(key.sign(head + b"." + claim, padding.PKCS1v15(), hashes.SHA256()))
        assertion = (head + b"." + claim + b"." + sig).decode()
        data = f"grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion={assertion}".encode()
        req = urllib.request.Request(sa["token_uri"], data=data, method="POST",
                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req, timeout=60) as r:
            tok = json.loads(r.read().decode())
        _TOKEN.update(tok=tok["access_token"], exp=now + int(tok.get("expires_in", 3600)))
        return _TOKEN["tok"]


class LiveProviders:
    def __init__(self, settings: Settings):
        self.s = settings

    def _vertex_headers(self):
        sa = self.s.secret("MI_VERTEX_SA_JSON")
        if not sa or not self.s.vertex_project:
            raise RuntimeError("Vertex is not configured (MI_VERTEX_SA_JSON / MI_VERTEX_PROJECT)")
        return {"Authorization": f"Bearer {vertex_token(sa)}"}

    def _vertex_url(self, model: str, method: str) -> str:
        r, p = self.s.vertex_region, self.s.vertex_project
        return f"https://{r}-aiplatform.googleapis.com/v1/projects/{p}/locations/{r}/publishers/google/models/{model}:{method}"

    # Stills — nano-banana-2 on the Gemini API (with reference photos as inline parts)
    def image(self, prompt: str, aspect: str, refs: list[tuple[str, bytes]], on_ref=None) -> ProviderResult:
        key = self.s.secret("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError("GOOGLE_API_KEY is not configured")
        parts = [{"text": prompt}] + [{"inlineData": {"mimeType": m, "data": base64.b64encode(d).decode()}} for m, d in refs]
        body = {"contents": [{"role": "user", "parts": parts}],
                "generationConfig": {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": aspect}}}
        st, reply = _http_json("POST", f"https://generativelanguage.googleapis.com/v1beta/models/{ROUTES['nano-banana-2']['model']}:generateContent",
                               {"x-goog-api-key": key}, body, timeout=300)
        rid = reply.get("responseId") if isinstance(reply, dict) else None
        if st != 200:
            return ProviderResult("failed", http_status=st, message=scrub(str(reply))[:600], request_ref=rid,
                                  timed_out=bool(reply.get("$timeout")))
        for cand in reply.get("candidates") or []:
            for part in (cand.get("content") or {}).get("parts") or []:
                d = (part.get("inlineData") or {}).get("data")
                if d:
                    return ProviderResult("ok", base64.b64decode(d), (part["inlineData"].get("mimeType") or "image/png"),
                                          request_ref=rid, meta={"usage": reply.get("usageMetadata")})
        fr = [c.get("finishReason") for c in reply.get("candidates") or []]
        return ProviderResult("failed", http_status=200, message=f"refusal_or_empty: finishReason={fr}; "
                              f"promptFeedback={reply.get('promptFeedback')}", request_ref=rid)

    # Clips — Veo 3.1 fast i2v on Vertex. Submission returns an operation name; the caller records it
    # BEFORE polling so an interrupted worker resumes the poll instead of paying for a second clip.
    def video_submit(self, prompt: str, image: tuple[str, bytes], duration_s: int, aspect: str,
                     negative: str | None, resolution: str = "720p", generate_audio: bool = True) -> ProviderResult:
        if duration_s not in VEO_DURATIONS or aspect not in ("16:9", "9:16"):
            return ProviderResult("failed", message=f"refused locally: Veo needs duration in {VEO_DURATIONS} and 16:9/9:16")
        inst = {"prompt": prompt, "image": {"bytesBase64Encoded": base64.b64encode(image[1]).decode(), "mimeType": image[0]}}
        params = {"sampleCount": 1, "durationSeconds": duration_s, "aspectRatio": aspect, "resolution": resolution,
                  "generateAudio": generate_audio}
        if negative:
            params["negativePrompt"] = negative
        st, reply = _http_json("POST", self._vertex_url(ROUTES["veo-3.1-fast-i2v"]["model"], "predictLongRunning"),
                               self._vertex_headers(), {"instances": [inst], "parameters": params}, timeout=300)
        if st != 200 or not isinstance(reply, dict) or not reply.get("name"):
            return ProviderResult("failed", http_status=st, message=scrub(str(reply))[:600], timed_out=bool((reply or {}).get("$timeout")))
        return ProviderResult("pending", request_ref=reply["name"])

    def video_poll(self, operation: str, max_wait_s: int = 720) -> ProviderResult:
        url = self._vertex_url(ROUTES["veo-3.1-fast-i2v"]["model"], "fetchPredictOperation")
        deadline = time.time() + max_wait_s
        while time.time() < deadline:
            code, op = _http_json("POST", url, self._vertex_headers(), {"operationName": operation}, timeout=120)
            if code != 200 or not isinstance(op, dict):
                return ProviderResult("failed", http_status=code, request_ref=operation, message=f"poll: {scrub(str(op))[:300]}")
            if op.get("done"):
                if op.get("error"):
                    return ProviderResult("failed", request_ref=operation, message=f"operation_error: {op['error']}")
                resp = op.get("response") or {}
                vids = resp.get("videos") or []
                if not vids:
                    why = "safety_filtered" if resp.get("raiMediaFilteredCount") else "no_artifact"
                    return ProviderResult("failed", request_ref=operation, message=f"{why}: {resp.get('raiMediaFilteredReasons')}")
                b = vids[0].get("bytesBase64Encoded")
                if not b:
                    return ProviderResult("failed", request_ref=operation, message=f"artifact not inline: {vids[0].get('gcsUri')}")
                return ProviderResult("ok", base64.b64decode(b), "video/mp4", request_ref=operation)
            time.sleep(6)
        return ProviderResult("failed", request_ref=operation, timed_out=True, message=f"poll timeout after {max_wait_s} s")

    # Music — Lyria on Vertex
    def music(self, prompt: str, negative: str | None) -> ProviderResult:
        inst = {"prompt": prompt}
        if negative:
            inst["negative_prompt"] = negative
        st, reply = _http_json("POST", self._vertex_url(ROUTES["lyria"]["model"], "predict"), self._vertex_headers(),
                               {"instances": [inst], "parameters": {"sample_count": 1}}, timeout=300)
        preds = (reply.get("predictions") or []) if isinstance(reply, dict) else []
        p0 = preds[0] if preds else {}
        k = next((k for k in ("bytesBase64Encoded", "audioContent") if p0.get(k)), None)
        if st != 200 or not k:
            return ProviderResult("failed", http_status=st, message=scrub(str(reply))[:600])
        return ProviderResult("ok", base64.b64decode(p0[k]), "audio/wav")


# ── Simulated providers: real files, no network, USD 0 ──────────────────────────────────────────
def _png(w: int, h: int, seed: int) -> bytes:
    from runtime.loop.synthetic import make_png
    return make_png(w, h, seed=seed)


def _wav(seconds: float, freq: float = 220.0) -> bytes:
    import io
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(22050)
        frames = b"".join(struct.pack("<h", int(3000 * math.sin(2 * math.pi * freq * i / 22050)))
                          for i in range(int(seconds * 22050)))
        w.writeframes(frames)
    return buf.getvalue()


ASPECT_PX = {"1:1": (1024, 1024), "4:5": (896, 1120), "9:16": (720, 1280), "16:9": (1280, 720)}


class SimulatedProviders:
    """Deterministic stand-ins. Faults can be injected per call kind: {"image": [503], "video": ["timeout"]}."""

    def __init__(self, settings: Settings):
        self.s = settings
        self._n = 0
        self._ops: dict = {}

    def _fault(self, kind: str):
        q = self.s.fault_injection.get(kind) or []
        if q:
            f = q.pop(0)
            if f == "timeout":
                return ProviderResult("failed", timed_out=True, message="simulated timeout")
            if f == "crash":
                raise KeyboardInterrupt("simulated worker crash during provider call")
            return ProviderResult("failed", http_status=int(f), message=f"simulated HTTP {f}")
        return None

    def image(self, prompt, aspect, refs, on_ref=None):
        f = self._fault("image")
        if f:
            return f
        self._n += 1
        w, h = ASPECT_PX.get(aspect, (1024, 1024))
        from product import media
        data = media.sim_image(w, h, seed=self._n, label=prompt[:40]) or _png(w // 4, h // 4, self._n)
        return ProviderResult("ok", data, "image/png", request_ref=f"sim-img-{self._n}")

    def video_submit(self, prompt, image, duration_s, aspect, negative, resolution="720p", generate_audio=True):
        f = self._fault("video")
        if f:
            return f
        self._n += 1
        op = f"sim-op-{self._n}"
        self._ops[op] = (duration_s, aspect)
        return ProviderResult("pending", request_ref=op)

    def video_poll(self, operation, max_wait_s=720):
        f = self._fault("video_poll")
        if f:
            return f
        duration_s, aspect = self._ops.get(operation, (4, "9:16"))
        from product import media
        data = media.sim_video(duration_s, aspect, seed=len(operation))
        if data is None:
            from runtime.loop.synthetic import make_mp4_stub
            w, h = ASPECT_PX.get(aspect, (720, 1280))
            data = make_mp4_stub(w, h, duration_s=duration_s)
        return ProviderResult("ok", data, "video/mp4", request_ref=operation)

    def music(self, prompt, negative):
        f = self._fault("music")
        if f:
            return f
        return ProviderResult("ok", _wav(32.0), "audio/wav", request_ref="sim-music")


def providers_for(settings: Settings):
    return LiveProviders(settings) if settings.provider_mode == "live" else SimulatedProviders(settings)
