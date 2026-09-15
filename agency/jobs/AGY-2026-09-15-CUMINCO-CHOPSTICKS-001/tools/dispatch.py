#!/usr/bin/env python3
"""Paid dispatch for AGY-2026-09-15-CUMINCO-CHOPSTICKS-001 — one job, one append-only ledger, one cap.

Every paid call: (1) checks the cumulative RESERVED total in gen/LEDGER.jsonl against the job cap (USD 8, stated by
the user in-session 2026-09-15T13:28:37Z, 0 retries), (2) appends a reservation line BEFORE the request leaves,
(3) settles the line after, failed calls included, (4) appends one attempt record to gen/ATTEMPTS.jsonl in the
JOB.yaml `spend.attempts[]` vocabulary (attempt_id, asset_id, route_cell, surface, pool, unit_price_usd, quantity,
reserved_usd, start/end UTC, latency_s, status, failure_basis, artifact_path, artifact_sha256). Failures are named by
runtime/execute/provider_errors.classify — an outage is infrastructure_transient, never a model failure. No hidden
retry: a re-send is a new attempt with its own line.

PROVENANCE: transport (submit → bounded poll → download, fal host trust, key-by-name, scrubbing) is the pilot's
preprod/recipes/_common.py + fal_queue.py and v3/tools/gen.py (origin/work/upwork-portfolio-samples-2026-09-15 @
b4b77fa) — production-proven on cases 001 and 002. Prices are re-read live from the runtime PriceBook at import.

Run with /opt/homebrew/bin/python3 after `source ~/.mi-keys` (values never printed).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
REPO = JOB.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))
import _common as C  # noqa: E402
from runtime.execute import provider_errors  # noqa: E402
from runtime.route.cli import build_router  # noqa: E402

GEN = JOB / "gen"
LEDGER = GEN / "LEDGER.jsonl"
ATTEMPTS = GEN / "ATTEMPTS.jsonl"
CAP_USD = 8.0                       # JOB.yaml spend.cap — stated by the user this session; hard stop
QUEUE = "https://queue.fal.run"

# route_key (runtime PriceBook / taint register cell) -> (fal endpoint id | provider surface, billing pool)
ROUTES = {
    "seedream-5-pro-edit": ("bytedance/seedream/v5/pro/edit", "fal", "cash"),
    "flux-2-pro-edit":     ("fal-ai/flux-2-pro/edit", "fal", "cash"),
    "kling-v3-pro-i2v":    ("fal-ai/kling-video/v3/pro/image-to-video", "fal", "cash"),
    "wan-3.0-prime-i2v":   ("alibaba/wan-3.0-prime/image-to-video", "fal", "cash"),
    "minimax-h3-max-i2v":  ("minimax/h3-max/image-to-video", "fal", "cash"),
    "sarvam-bulbul-v3":    ("https://api.sarvam.ai/text-to-speech", "sarvam_direct", "sarvam_credits"),
    "elevenlabs-v3-direct": ("https://api.elevenlabs.io/v1/text-to-speech", "elevenlabs_direct", "elevenlabs_credits"),
    "lyria":               ("lyria-002", "vertex", "credits"),
    "nano-banana-2":       ("gemini-3.1-flash-image", "gemini_api", "credits"),
    "veo-3.1-fast-i2v":    ("veo-3.1-fast-generate-001", "vertex", "credits"),
}
PROJECT = "vertexaiproject-507518"; REGION = "us-central1"
REGIONAL = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/publishers/google/models"
_PB = None


def pricebook():
    global _PB
    if _PB is None:
        _PB = build_router()[0].prices
    return _PB


def quote(route_key: str, facts: dict):
    q = pricebook().quote(route_key, facts)
    if not q.priced:
        sys.exit(f"REFUSED: route {route_key} is UNPRICED ({q.reason}); nothing sent")
    return q


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ledger_reserved() -> float:
    if not LEDGER.exists():
        return 0.0
    return sum(json.loads(l).get("reserved_usd", 0) for l in LEDGER.read_text().splitlines()
               if l.strip() and json.loads(l).get("status") == "reserved")


def next_attempt_id() -> str:
    n = 0
    if ATTEMPTS.exists():
        n = sum(1 for l in ATTEMPTS.read_text().splitlines() if l.strip())
    return f"att-{n + 1:03d}"


def reserve(attempt_id: str, asset_id: str, route_key: str, q, is_repair: bool) -> float:
    est = float(q.expected_cost_usd)
    cum = ledger_reserved() + est
    if cum > CAP_USD + 1e-9:
        sys.exit(f"REFUSED: cumulative reserved USD {cum:.4f} would exceed the job cap USD {CAP_USD:.2f}. Nothing sent. "
                 f"(reserved so far USD {ledger_reserved():.4f}; this attempt USD {est:.4f})")
    GEN.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps({"utc": now(), "attempt_id": attempt_id, "asset_id": asset_id, "route": route_key,
                            "quantity": str(q.quantity), "unit": q.unit, "unit_price_usd": str(q.unit_price),
                            "reserved_usd": round(est, 6), "cumulative_reserved_usd": round(cum, 6),
                            "cap_usd": CAP_USD, "is_repair": is_repair, "status": "reserved"}) + "\n")
    print(f"[reserve] {attempt_id} {asset_id} {route_key} {q.quantity} {q.unit} x {q.unit_price} = USD {est:.4f}; "
          f"cumulative USD {cum:.4f} of {CAP_USD:.2f}")
    return est


def settle(attempt_id: str, status: str, note: str = "", request_id=None):
    with LEDGER.open("a") as f:
        f.write(json.dumps({"utc": now(), "attempt_id": attempt_id, "request_id": request_id, "status": status,
                            "note": C.scrub(note)[:300]}) + "\n")


def record(rec: dict):
    with ATTEMPTS.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def failure(rec: dict, http_status=None, message="", timed_out=False, status="provider_error"):
    cls = provider_errors.classify(http_status=http_status, message=message, timed_out=timed_out)
    rec.update(end=now(), status=status, failure_class=cls.get("failure_class") or cls.get("class"),
               failure_basis=C.scrub(str(cls))[:300], error=C.scrub(message)[:300], verdict="failed")
    record(rec)
    settle(rec["attempt_id"], rec["status"], message, rec.get("request_id"))
    print("FAILED", rec["attempt_id"], rec["failure_class"], C.scrub(message)[:200])
    return rec


def base_rec(attempt_id, asset_id, route_key, q, prompt, out, is_repair, params):
    ep, surface, pool = ROUTES[route_key]
    return {"attempt_id": attempt_id, "asset_id": asset_id, "route_cell": route_key, "endpoint": ep, "surface": surface,
            "pool": pool, "unit_price_usd": str(q.unit_price), "quantity": str(q.quantity), "quantity_unit": q.unit,
            "reserved_usd": round(float(q.expected_cost_usd), 6), "settled_usd": None, "prompt": prompt,
            "params": params, "start_utc": now(), "end": None, "latency_s": None, "status": None, "failure_basis": None,
            "artifact_path": str(out.resolve().relative_to(JOB)), "artifact_sha256": None, "verdict": "pending", "is_repair": is_repair}


# ── fal queue ────────────────────────────────────────────────────────────────
def fal(asset_id: str, route_key: str, body: dict, facts: dict, out: Path, prompt: str, is_repair=False) -> dict:
    ep, surface, pool = ROUTES[route_key]
    q = quote(route_key, facts)
    aid = next_attempt_id()
    reserve(aid, asset_id, route_key, q, is_repair)
    shown = {k: v for k, v in body.items() if not (isinstance(v, str) and v.startswith("data:")) and k not in ("image_urls", "start_image_url", "image_url")}
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair, shown)
    t0 = time.time()
    hdr = {"Authorization": f"Key {C.key('FAL_KEY')}"}
    st, reply = C.http_json("POST", f"{QUEUE}/{ep}", hdr, body)
    if st != 200:
        return failure(rec, http_status=st, message=str(reply), status=f"submit_http_{st}")
    rid, surl, rurl = reply.get("request_id"), reply.get("status_url"), reply.get("response_url")
    if not (rid and _trusted(surl, "queue") and _trusted(rurl, "queue")):
        return failure(rec, message="malformed or off-host queue reply", status="local_fault")
    rec["request_id"] = rid
    print("request_id:", rid)

    def check():
        code, s = C.http_json("GET", surl, hdr)
        stt = s.get("status") if isinstance(s, dict) else None
        if code in (200, 202) and stt in ("IN_QUEUE", "IN_PROGRESS"):
            return False, s
        return True, (s if stt == "COMPLETED" else {"$error": code, "reply": s})

    fin = C.poll(check, interval_s=5.0, max_checks=144)
    if fin.get("$timeout"):
        return failure(rec, timed_out=True, message="poll timeout 720 s", status="timeout")
    if fin.get("$error"):
        return failure(rec, http_status=fin.get("$error"), message=str(fin.get("reply")), status="provider_error")
    code, res = C.http_json("GET", rurl, hdr)
    if code != 200 or res.get("error") or res.get("detail"):
        return failure(rec, http_status=code, message=str(res), status=f"result_http_{code}")
    url = None
    imgs = res.get("images")
    if isinstance(imgs, list) and imgs and imgs[0].get("url"):
        url = imgs[0]["url"]
    for k in ("video", "audio", "image"):
        v = res.get(k)
        if isinstance(v, dict) and v.get("url"):
            url = url or v["url"]
    if not url or not _trusted(url, "download"):
        return failure(rec, message=f"no trusted artifact url: {url}", status="local_fault")
    st2, data, ct = C.http("GET", url, {})
    if st2 != 200:
        return failure(rec, http_status=st2, message="artifact download failed", status=f"download_http_{st2}")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out),
               bytes=len(data), provider_meta={k: res.get(k) for k in ("seed", "timings", "has_nsfw_concepts") if k in res})
    record(rec); settle(aid, "ok", f"{ct} {len(data)} bytes -> {out.name}", rid)
    print(f"saved {out} ({len(data)} bytes) in {rec['latency_s']} s  sha256 {rec['artifact_sha256'][:16]}")
    return rec


def _trusted(url: str, kind: str) -> bool:
    import re
    m = re.match(r"^https://([A-Za-z0-9.-]+)(?::\d+)?(?:[/?#]|$)", url or "")
    if not m:
        return False
    h = m.group(1).lower()
    return h == "queue.fal.run" if kind == "queue" else (h == "queue.fal.run" or h.endswith(".fal.media") or h.endswith(".fal.run"))


def seedream_edit(asset_id, prompt, refs: list[Path], out: Path, width: int, height: int, is_repair=False):
    body = {"prompt": prompt, "image_urls": [C.data_uri(p) for p in refs], "num_images": 1,
            "image_size": {"width": width, "height": height}, "output_format": "png"}
    return fal(asset_id, "seedream-5-pro-edit", body, {"params": {}}, out, prompt, is_repair)


def kling_i2v(asset_id, prompt, still: Path, out: Path, duration: int = 5, negative: str | None = None, is_repair=False):
    body = {"prompt": prompt, "start_image_url": C.data_uri(still), "duration": str(duration), "generate_audio": False}
    if negative:
        body["negative_prompt"] = negative
    return fal(asset_id, "kling-v3-pro-i2v", body, {"params": {"duration_s": duration}}, out, prompt, is_repair)


def wan_i2v(asset_id, prompt, still: Path, out: Path, duration: int = 5, aspect: str = "9:16", is_repair=False):
    body = {"prompt": prompt, "start_image_url": C.data_uri(still), "resolution": "720p", "duration": int(duration),
            "audio": False, "aspect_ratio": aspect}
    return fal(asset_id, "wan-3.0-prime-i2v", body, {"params": {"duration_s": duration}}, out, prompt, is_repair)


def h3_i2v(asset_id, prompt, still: Path, out: Path, duration: int = 6, is_repair=False):
    body = {"prompt": prompt, "prompt_expansion_mode": "balanced", "image_url": C.data_uri(still), "resolution": "768P",
            "duration": int(duration)}
    return fal(asset_id, "minimax-h3-max-i2v", body, {"params": {"duration_s": duration}}, out, prompt, is_repair)


# ── Google credits surfaces (pilot recipes nano_banana_still.py / google_video.py, cases 001 + 002) ──
def nb2(asset_id: str, prompt: str, out: Path, aspect: str, refs: list[Path] | None = None, is_repair=False) -> dict:
    """Nano Banana 2 on the Gemini API with optional inline reference images (the pilot's nb2; RO-04 case 001, RO-04 case 002).
    NOTE: with reference images this is NOT a registered IMG-REF cell — used only under a micro-qualification with a human gate."""
    route_key = "nano-banana-2"; ep, surface, pool = ROUTES[route_key]
    q = quote(route_key, {"params": {}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    parts = [{"text": prompt}]
    for rp in refs or []:
        b, mime = C.b64file(rp); parts.append({"inlineData": {"mimeType": mime, "data": b}})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": aspect}}}
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair, {"aspect": aspect, "reference_images": [str(r.name) for r in refs or []]})
    t0 = time.time()
    st, reply = C.http_json("POST", f"https://generativelanguage.googleapis.com/v1beta/models/{ep}:generateContent",
                            {"x-goog-api-key": C.key("GOOGLE_API_KEY")}, body, timeout=300)
    rec["request_id"] = reply.get("responseId") if isinstance(reply, dict) else None
    if st != 200:
        return failure(rec, http_status=st, message=str(reply), status=f"http_{st}")
    data = None
    for cand in reply.get("candidates") or []:
        for part in (cand.get("content") or {}).get("parts") or []:
            if part.get("inlineData", {}).get("data"):
                data = base64.b64decode(part["inlineData"]["data"]); break
        if data: break
    if not data:
        fr = [c.get("finishReason") for c in reply.get("candidates") or []]
        return failure(rec, http_status=st, message=f"no image; finishReason={fr}; promptFeedback={reply.get('promptFeedback')}", status="refusal_or_empty")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out), bytes=len(data),
               provider_meta={"usage": reply.get("usageMetadata")}); record(rec)
    settle(aid, "ok", f"{len(data)} bytes -> {out.name}", rec["request_id"]); print(f"saved {out} ({len(data)} bytes) in {rec['latency_s']} s")
    return rec


def veo_i2v(asset_id: str, prompt: str, still: Path, out: Path, duration: int = 6, aspect: str = "9:16",
            resolution: str = "720p", negative: str | None = None, is_repair=False) -> dict:
    """Veo 3.1 Fast image-to-video on Vertex, silent — the exact configuration of the clean VID-I2V cell (720p, 9:16, generateAudio false)."""
    route_key = "veo-3.1-fast-i2v"; ep, surface, pool = ROUTES[route_key]
    if duration not in (4, 6, 8):
        sys.exit("Veo durations are 4, 6 or 8 s")
    q = quote(route_key, {"params": {"duration_s": duration}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    b, mime = C.b64file(still)
    inst = {"prompt": prompt, "image": {"bytesBase64Encoded": b, "mimeType": mime}}
    params = {"sampleCount": 1, "aspectRatio": aspect, "resolution": resolution, "durationSeconds": duration, "generateAudio": False}
    if negative:
        params["negativePrompt"] = negative
    body = {"instances": [inst], "parameters": params}
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair, params)
    t0 = time.time()
    hdr = {"Authorization": f"Bearer {C.gcloud_sa_token()}"}
    url_base = f"{REGIONAL}/{ep}"
    st, reply = C.http_json("POST", f"{url_base}:predictLongRunning", hdr, body)
    if st != 200:
        return failure(rec, http_status=st, message=str(reply), status=f"submit_http_{st}")
    name = reply.get("name"); rec["request_id"] = name; print("operation:", name)

    def check():
        code, op = C.http_json("POST", f"{url_base}:fetchPredictOperation", hdr, {"operationName": name})
        if code != 200:
            return True, {"$error": code, "reply": op}
        return bool(op.get("done")), op

    op = C.poll(check, 5.0, 120)
    if op.get("$timeout"):
        return failure(rec, timed_out=True, message="poll timeout 600 s", status="timeout")
    if op.get("$error") or op.get("error"):
        err = op.get("error") or op.get("reply")
        code = (err or {}).get("code") if isinstance(err, dict) else op.get("$error")
        return failure(rec, http_status=op.get("$error"), message=str(err), status="provider_error") if not isinstance(code, int) or code > 100 \
            else failure(rec, message=str(err), status="provider_error")
    resp = op.get("response") or {}
    vids = resp.get("videos") or []
    if not vids or not vids[0].get("bytesBase64Encoded"):
        return failure(rec, message=f"no video; raiMediaFilteredCount={resp.get('raiMediaFilteredCount')} reasons={resp.get('raiMediaFilteredReasons')}", status="refusal_or_empty")
    data = base64.b64decode(vids[0]["bytesBase64Encoded"])
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out), bytes=len(data)); record(rec)
    settle(aid, "ok", f"{vids[0].get('mimeType')} {len(data)} bytes -> {out.name}", name)
    print(f"saved {out} ({len(data)} bytes) in {rec['latency_s']} s")
    return rec


# ── voices ───────────────────────────────────────────────────────────────────
def sarvam(asset_id: str, text: str, out: Path, speaker: str, lang: str = "en-IN", pace: float | None = None, is_repair=False) -> dict:
    route_key = "sarvam-bulbul-v3"; ep, surface, pool = ROUTES[route_key]
    q = quote(route_key, {"params": {"chars": len(text)}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    body = {"text": text, "language_code": lang, "speaker": speaker, "model": "bulbul:v3"}
    if pace:
        body["pace"] = pace
    rec = base_rec(aid, asset_id, route_key, q, text, out, is_repair, {"language_code": lang, "speaker": speaker, "pace": pace})
    t0 = time.time()
    st, reply = C.http_json("POST", ep, {"api-subscription-key": C.key("SARVAM_API_KEY")}, body, timeout=120)
    rid = reply.get("request_id") if isinstance(reply, dict) else None
    rec["request_id"] = rid
    if st != 200 or not reply.get("audios"):
        return failure(rec, http_status=st, message=str(reply), status=f"http_{st}")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(base64.b64decode(reply["audios"][0]))
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out)); record(rec)
    settle(aid, "ok", f"-> {out.name}", rid); print(f"saved {out} in {rec['latency_s']} s")
    return rec


def elevenlabs(asset_id: str, text: str, out: Path, voice_id: str, is_repair=False, model_id: str = "eleven_v3", voice_settings: dict | None = None) -> dict:
    import re
    route_key = "elevenlabs-v3-direct"; ep, surface, pool = ROUTES[route_key]
    if not re.fullmatch(r"[A-Za-z0-9]+", voice_id):
        sys.exit("voice_id must be a plain identifier (it goes in a URL path)")
    q = quote(route_key, {"params": {"chars": len(text)}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    body = {"text": text, "model_id": model_id}
    if voice_settings:
        body["voice_settings"] = voice_settings
    rec = base_rec(aid, asset_id, route_key, q, text, out, is_repair, {"voice_id": voice_id, "model_id": model_id, "voice_settings": voice_settings})
    t0 = time.time()
    st, data, ct = C.http("POST", f"{ep}/{voice_id}?output_format=mp3_44100_128",
                          {"xi-api-key": C.key("ELEVENLABS_API_KEY"), "Content-Type": "application/json"},
                          json.dumps(body).encode(), timeout=120)
    if st != 200 or not data or (ct or "").startswith("application/json"):
        return failure(rec, http_status=st, message=data.decode("utf-8", "replace")[:300], status=f"http_{st}")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out)); record(rec)
    settle(aid, "ok", f"-> {out.name}"); print(f"saved {out} in {rec['latency_s']} s")
    return rec


# ── Gemini TTS (NO Registry cell; job-local price pin; micro-qualification only) ──
class _LocalQuote:
    """A job-local price pin for a route the roster does not carry. source/pins/gemini-api-pricing.html
    (sha256 18679848c2…, fetched 2026-09-15T14:06Z): gemini-3.1-flash-tts-preview USD 1.00 / 1M text tokens in,
    USD 20.00 / 1M audio tokens out. Audio tokens are not known before the call, so the reservation is an upper
    bound: 32 audio tokens per second of speech assumed at 15 s = 480 tokens -> USD 0.0096 + input; settled from usageMetadata."""
    def __init__(self, chars):
        self.priced = True; self.unit = "per_1M_audio_tokens_out (+ text in)"; self.unit_price = "20.00 out / 1.00 in"
        self.quantity = f"≤ 480 audio tokens + {chars} chars"; self.billing_pool = "credits"
        self.expected_cost_usd = round(480 / 1e6 * 20.0 + (chars / 4) / 1e6 * 1.0, 6)


def gemini_tts(asset_id: str, text: str, out: Path, voice: str, style: str, model: str = "gemini-3.1-flash-tts-preview", is_repair=False) -> dict:
    import struct, wave
    route_key = "gemini-tts"; ROUTES[route_key] = (model, "gemini_api", "credits")
    q = _LocalQuote(len(text))
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    body = {"contents": [{"parts": [{"text": f"{style}\n\n{text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    rec = base_rec(aid, asset_id, route_key, q, text, out, is_repair, {"voice": voice, "style": style, "model": model})
    t0 = time.time()
    st, reply = C.http_json("POST", f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                            {"x-goog-api-key": C.key("GOOGLE_API_KEY")}, body, timeout=180)
    if st != 200:
        return failure(rec, http_status=st, message=str(reply), status=f"http_{st}")
    data = None; mime = ""
    for cand in reply.get("candidates") or []:
        for part in (cand.get("content") or {}).get("parts") or []:
            if part.get("inlineData", {}).get("data"):
                data = base64.b64decode(part["inlineData"]["data"]); mime = part["inlineData"].get("mimeType", ""); break
        if data: break
    if not data:
        return failure(rec, message=f"no audio; {reply.get('promptFeedback')}", status="refusal_or_empty")
    out.parent.mkdir(parents=True, exist_ok=True)
    if "pcm" in mime.lower() or "l16" in mime.lower():
        rate = int(next((kv.split("=")[1] for kv in mime.split(";") if kv.strip().startswith("rate=")), "24000"))
        with wave.open(str(out), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(data)
    else:
        out.write_bytes(data)
    usage = reply.get("usageMetadata") or {}
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out), mime=mime,
               provider_meta={"usage": usage}, settled_usd=round((usage.get("candidatesTokenCount", 0) / 1e6) * 20.0 + (usage.get("promptTokenCount", 0) / 1e6) * 1.0, 6))
    record(rec); settle(aid, "ok", f"{mime} {len(data)} bytes -> {out.name}; usage {usage}"); print(f"saved {out} in {rec['latency_s']} s; usage {usage}")
    return rec


# ── music ────────────────────────────────────────────────────────────────────
def lyria(asset_id: str, prompt: str, out: Path, negative: str | None = None, is_repair=False) -> dict:
    route_key = "lyria"; ep, surface, pool = ROUTES[route_key]
    q = quote(route_key, {"params": {}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/vertexaiproject-507518/locations/us-central1/publishers/google/models/lyria-002:predict"
    inst = {"prompt": prompt}
    if negative:
        inst["negative_prompt"] = negative
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair, {"negative_prompt": negative, "sample_count": 1})
    t0 = time.time()
    st, reply = C.http_json("POST", url, {"Authorization": f"Bearer {C.gcloud_sa_token()}"},
                            {"instances": [inst], "parameters": {"sample_count": 1}}, timeout=300)
    preds = (reply.get("predictions") or []) if isinstance(reply, dict) else []
    p0 = preds[0] if preds else {}
    key = next((k for k in ("bytesBase64Encoded", "audioContent") if p0.get(k)), None)
    if st != 200 or not key:
        return failure(rec, http_status=st, message=str(reply), status=f"http_{st}")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(base64.b64decode(p0[key]))
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out)); record(rec)
    settle(aid, "ok", f"-> {out.name}"); print(f"saved {out} in {rec['latency_s']} s")
    return rec


def summary():
    print(f"reserved USD {ledger_reserved():.4f} of cap {CAP_USD:.2f}; remaining USD {CAP_USD - ledger_reserved():.4f}")
    if ATTEMPTS.exists():
        for l in ATTEMPTS.read_text().splitlines():
            r = json.loads(l)
            print(f"  {r['attempt_id']} {r['asset_id']:<14} {r['route_cell']:<22} USD {r['reserved_usd']:<7} {r['status']:<12} {r.get('verdict')}  {r.get('artifact_path')}")


def balance():
    st, txt, _ = C.http("GET", "https://rest.alpha.fal.ai/billing/user_balance", {"Authorization": f"Key {C.key('FAL_KEY')}"})
    print("fal balance HTTP", st, C.scrub(txt.decode("utf-8", "replace"))[:200])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["summary", "balance"])
    a = ap.parse_args()
    {"summary": summary, "balance": balance}[a.cmd]()
