#!/usr/bin/env python3
"""Paid dispatch for UPWORK-INTRO-V3-SHOWCASE with a cumulative ledger + per-asset evidence record.

Every paid call: (1) checks the cumulative reserved total in gen/LEDGER.jsonl against the cap (INR 2,000 = USD 20.96),
(2) writes a reservation line BEFORE the request leaves, (3) settles the line, (4) appends one asset record to
gen/ASSETS.jsonl {asset_id, prompt, source, provider, model, surface, unit_price, quantity, est_usd, start, end,
latency_s, status, note}. Human verdicts are added later by `verdict`.

Transport code is the pilot's preprod recipes (stdlib urllib; keys read by NAME from the environment, never printed).
Run with /opt/homebrew/bin/python3 after `source ~/.mi-keys`.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
V3 = HERE.parent
RECIPES = V3.parent / "preprod" / "recipes"
V3_LEDGER = V3.parent / "v3" / "gen" / "LEDGER.jsonl"   # V4 continues V3's cumulative cap: carried forward, never reset
sys.path.insert(0, str(RECIPES))
import _common as C  # noqa: E402

GEN = V3 / "gen"
LEDGER = GEN / "LEDGER.jsonl"
ASSETS = GEN / "ASSETS.jsonl"
INR_PER_USD = 95.4211
CAP_INR = 2000.0
CAP_USD = CAP_INR / INR_PER_USD

PRICES = {  # USD, pinned 2026-09-04/09 (see plan/SPEND-AMENDMENT-V4.md)
    "veo-3.1-fast-generate-001/i2v/1080p": ("seconds", 0.12),
    "veo-3.1-fast-generate-001/i2v/720p": ("seconds", 0.10),
    "omni/vertex/image_to_video/720p": ("seconds", 0.10136),
    "openai/gpt-image-2": ("images", 0.053),
    "bytedance/seedream/v5/pro/edit": ("images", 0.0675),
    "fal-ai/flux-2-pro": ("images", 0.03),
    "fal-ai/kling-video/v3/pro/image-to-video": ("seconds", 0.112),
    "alibaba/wan-3.0-prime/image-to-video": ("seconds", 0.14),
    "minimax/h3-max/image-to-video": ("seconds", 0.08),
    "gemini-3.1-flash-image": ("images", 0.067),
    "lyria-002": ("tracks", 0.06),
    "sarvam/bulbul:v3": ("kchars", 3.0 / INR_PER_USD),
}
QUEUE = "https://queue.fal.run"
HOST_RE = re.compile(r"^https://([A-Za-z0-9.-]+)(?::\d+)?(?:[/?#]|$)")


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _reserved(path: Path) -> float:
    if not path.exists():
        return 0.0
    return sum(json.loads(l).get("est_usd", 0) for l in path.read_text().splitlines() if l.strip() and json.loads(l).get("status") == "reserved")


def ledger_total() -> float:
    """Cumulative reserved USD across V3 (carried) + V4."""
    return _reserved(V3_LEDGER) + _reserved(LEDGER)


def reserve(asset_id: str, route: str, qty: float, price: float) -> float:
    est = qty * price
    cum = ledger_total() + est
    if cum > CAP_USD:
        sys.exit(f"REFUSED: cumulative reserved USD {cum:.4f} would exceed the cap USD {CAP_USD:.2f} (INR {CAP_INR:.0f}). Nothing sent.")
    GEN.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps({"utc": now(), "asset_id": asset_id, "route": route, "quantity": qty, "unit": PRICES[route][0],
                            "unit_price_usd": price, "est_usd": round(est, 6), "cumulative_usd": round(cum, 6), "status": "reserved"}) + "\n")
    print(f"[reserve] {asset_id} {route} {qty} x {price} = USD {est:.4f}; cumulative USD {cum:.4f} of {CAP_USD:.2f}")
    return est


def settle(asset_id: str, status: str, note: str = "", request_id=None):
    with LEDGER.open("a") as f:
        f.write(json.dumps({"utc": now(), "asset_id": asset_id, "request_id": request_id, "status": status, "note": C.scrub(note)[:300]}) + "\n")


def record(rec: dict):
    with ASSETS.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def trusted(url: str, kind: str) -> bool:
    m = HOST_RE.match(url or "")
    if not m:
        return False
    h = m.group(1).lower()
    return h == "queue.fal.run" if kind == "queue" else (h == "queue.fal.run" or h.endswith(".fal.media") or h.endswith(".fal.run"))


def fal(asset_id: str, endpoint: str, body: dict, qty: float, out: Path, prompt: str, source: str, note: str = "") -> dict:
    unit, price = PRICES[endpoint]
    est = reserve(asset_id, endpoint, qty, price)
    rec = {"asset_id": asset_id, "prompt": prompt, "source": source, "provider": "fal", "model": endpoint, "surface": "fal queue",
           "unit_price_usd": price, "unit": unit, "quantity": qty, "est_usd": round(est, 6), "start": now(), "note": note,
           "params": {k: v for k, v in body.items() if not (isinstance(v, str) and v.startswith("data:")) and k not in ("image_urls",)}}
    t0 = time.time()
    hdr = {"Authorization": f"Key {C.key('FAL_KEY')}"}
    st, reply = C.http_json("POST", f"{QUEUE}/{endpoint}", hdr, body)
    if st != 200:
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status=f"submit_http_{st}", error=C.scrub(str(reply))[:300]); record(rec)
        settle(asset_id, f"submit_http_{st}", str(reply)); print("SUBMIT FAILED", st, C.scrub(str(reply))[:300]); return rec
    rid, surl, rurl = reply.get("request_id"), reply.get("status_url"), reply.get("response_url")
    if not (rid and trusted(surl, "queue") and trusted(rurl, "queue")):
        rec.update(end=now(), status="malformed_queue_reply"); record(rec); settle(asset_id, "malformed", str(reply)); return rec
    rec["request_id"] = rid
    print("request_id:", rid)

    def check():
        code, s = C.http_json("GET", surl, hdr)
        stt = s.get("status") if isinstance(s, dict) else None
        if code in (200, 202) and stt in ("IN_QUEUE", "IN_PROGRESS"):
            return False, s
        return True, (s if stt == "COMPLETED" else {"$error": code, "reply": s})

    fin = C.poll(check, interval_s=5.0, max_checks=144)
    if fin.get("$timeout") or fin.get("$error"):
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="poll_failed_or_timeout", error=C.scrub(str(fin))[:300]); record(rec)
        settle(asset_id, "poll_failed_or_timeout", str(fin), rid); print("POLL FAILED", C.scrub(str(fin))[:300]); return rec
    code, res = C.http_json("GET", rurl, hdr)
    if code != 200 or res.get("error") or res.get("detail"):
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status=f"result_http_{code}", error=C.scrub(str(res))[:300]); record(rec)
        settle(asset_id, f"result_http_{code}", str(res), rid); print("RESULT FAILED", C.scrub(str(res))[:300]); return rec
    url = None
    imgs = res.get("images")
    if isinstance(imgs, list) and imgs and imgs[0].get("url"):
        url = imgs[0]["url"]
    for k in ("video", "audio", "image"):
        v = res.get(k)
        if isinstance(v, dict) and v.get("url"):
            url = url or v["url"]
    if not url or not trusted(url, "download"):
        rec.update(end=now(), status="no_or_untrusted_artifact"); record(rec); settle(asset_id, "no_artifact", str(url), rid); return rec
    st2, data, ct = C.http("GET", url, {})
    if st2 != 200:
        rec.update(end=now(), status=f"download_http_{st2}"); record(rec); settle(asset_id, f"download_http_{st2}", "", rid); return rec
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", file=str(out.relative_to(V3)), bytes=len(data),
               provider_meta={k: res.get(k) for k in ("seed", "timings", "has_nsfw_concepts", "prompt") if k in res})
    record(rec); settle(asset_id, "ok", f"{ct} {len(data)} bytes -> {out.name}", rid)
    print(f"saved {out} ({len(data)} bytes) in {rec['latency_s']} s")
    return rec


def sarvam(asset_id: str, text: str, out: Path, lang: str = "en-IN", speaker: str = "aditya", pace: float | None = None) -> dict:
    route = "sarvam/bulbul:v3"; unit, price = PRICES[route]
    qty = len(text) / 1000.0
    est = reserve(asset_id, route, qty, price)
    body = {"text": text, "language_code": lang, "speaker": speaker, "model": "bulbul:v3"}
    if pace:
        body["pace"] = pace
    rec = {"asset_id": asset_id, "prompt": text, "source": "VO script (frozen)", "provider": "sarvam", "model": "bulbul:v3", "surface": "api.sarvam.ai/text-to-speech",
           "unit_price_usd": price, "unit": unit, "quantity": qty, "est_usd": round(est, 6), "start": now(), "params": {"language_code": lang, "speaker": speaker, "pace": pace}}
    t0 = time.time()
    st, reply = C.http_json("POST", "https://api.sarvam.ai/text-to-speech", {"api-subscription-key": C.key("SARVAM_API_KEY")}, body, timeout=120)
    rid = reply.get("request_id") if isinstance(reply, dict) else None
    if st != 200 or not reply.get("audios"):
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status=f"http_{st}", error=C.scrub(str(reply))[:300]); record(rec)
        settle(asset_id, f"http_{st}", str(reply), rid); print("SARVAM FAILED", st, C.scrub(str(reply))[:300]); return rec
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(base64.b64decode(reply["audios"][0]))
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", file=str(out.relative_to(V3)), request_id=rid); record(rec)
    settle(asset_id, "ok", f"-> {out.name}", rid); print(f"saved {out} in {rec['latency_s']} s")
    return rec


def lyria(asset_id: str, prompt: str, out: Path, negative: str | None = None) -> dict:
    route = "lyria-002"; unit, price = PRICES[route]
    est = reserve(asset_id, route, 1, price)
    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/vertexaiproject-507518/locations/us-central1/publishers/google/models/lyria-002:predict"
    inst = {"prompt": prompt}
    if negative:
        inst["negative_prompt"] = negative
    rec = {"asset_id": asset_id, "prompt": prompt, "source": "music prompt (frozen)", "provider": "google", "model": "lyria-002", "surface": "vertex us-central1",
           "unit_price_usd": price, "unit": unit, "quantity": 1, "est_usd": est, "start": now(), "params": {"negative_prompt": negative, "sample_count": 1}}
    t0 = time.time()
    st, reply = C.http_json("POST", url, {"Authorization": f"Bearer {C.gcloud_sa_token()}"}, {"instances": [inst], "parameters": {"sample_count": 1}}, timeout=300)
    preds = (reply.get("predictions") or []) if isinstance(reply, dict) else []
    p0 = preds[0] if preds else {}
    key = next((k for k in ("bytesBase64Encoded", "audioContent") if p0.get(k)), None)
    if st != 200 or not key:
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status=f"http_{st}_or_no_audio", error=C.scrub(str(reply))[:300]); record(rec)
        settle(asset_id, f"http_{st}", str(reply)); print("LYRIA FAILED", st, C.scrub(str(reply))[:300]); return rec
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(base64.b64decode(p0[key]))
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", file=str(out.relative_to(V3))); record(rec)
    settle(asset_id, "ok", f"-> {out.name}"); print(f"saved {out} in {rec['latency_s']} s")
    return rec


def nb2(asset_id: str, prompt: str, out: Path, aspect: str, source: str, refs: list[Path] | None = None) -> dict:
    route = "gemini-3.1-flash-image"; unit, price = PRICES[route]
    price_eff = price + 0.0011 * len(refs or [])
    est = reserve(asset_id, route, 1, price_eff)
    parts = [{"text": prompt}]
    for p in refs or []:
        b, mime = C.b64file(p); parts.append({"inlineData": {"mimeType": mime, "data": b}})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": aspect}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{route}:generateContent"
    rec = {"asset_id": asset_id, "prompt": prompt, "source": source, "provider": "google", "model": route, "surface": "gemini developer api",
           "unit_price_usd": price_eff, "unit": unit, "quantity": 1, "est_usd": est, "start": now(), "params": {"aspectRatio": aspect, "refs": len(refs or [])}}
    t0 = time.time()
    st, reply = C.http_json("POST", url, {"x-goog-api-key": C.key("GOOGLE_API_KEY")}, body)
    rid = reply.get("responseId") if isinstance(reply, dict) else None
    cands = (reply.get("candidates") or []) if isinstance(reply, dict) else []
    blob = None
    for part in ((cands[0].get("content") or {}).get("parts") or []) if cands else []:
        b = part.get("inlineData") or part.get("inline_data")
        if b and b.get("data"):
            blob = b
    if st != 200 or not blob:
        fr = cands[0].get("finishReason") if cands else reply.get("promptFeedback") if isinstance(reply, dict) else None
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status=f"http_{st}_{fr}", error=C.scrub(str(reply))[:300]); record(rec)
        settle(asset_id, f"http_{st}_{fr}", str(reply), rid); print("NB2 FAILED", st, fr); return rec
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(base64.b64decode(blob["data"]))
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", file=str(out.relative_to(V3)), request_id=rid); record(rec)
    settle(asset_id, "ok", f"-> {out.name}", rid); print(f"saved {out} in {rec['latency_s']} s")
    return rec


PROJECT = "vertexaiproject-507518"; REGION = "us-central1"
REGIONAL = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/publishers/google/models"
VERTEX_INTERACTIONS = f"https://aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/global/interactions"


def veo_i2v(asset_id: str, prompt: str, image: Path, out: Path, duration: int = 8, resolution: str = "1080p", audio: bool = True, aspect: str = "16:9") -> dict:
    """Veo 3.1 Fast image-to-video with native audio (Vertex predictLongRunning). PROVENANCE: preprod/recipes/google_video.py."""
    route = f"veo-3.1-fast-generate-001/i2v/{resolution}"; unit, price = PRICES[route]
    est = reserve(asset_id, route, duration, price)
    b, mime = C.b64file(image)
    body = {"instances": [{"prompt": prompt, "image": {"bytesBase64Encoded": b, "mimeType": mime}}],
            "parameters": {"sampleCount": 1, "aspectRatio": aspect, "resolution": resolution, "durationSeconds": duration, "generateAudio": audio}}
    rec = {"asset_id": asset_id, "prompt": prompt, "source": f"anchor still {image.name}", "provider": "google", "model": "veo-3.1-fast-generate-001", "surface": "vertex predictLongRunning",
           "unit_price_usd": price, "unit": unit, "quantity": duration, "est_usd": round(est, 6), "start": now(), "params": body["parameters"]}
    t0 = time.time(); hdr = {"Authorization": f"Bearer {C.gcloud_sa_token()}"}
    url = f"{REGIONAL}/veo-3.1-fast-generate-001"
    st, reply = C.http_json("POST", f"{url}:predictLongRunning", hdr, body)
    if st != 200:
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status=f"submit_http_{st}", error=C.scrub(str(reply))[:300]); record(rec); settle(asset_id, f"submit_http_{st}", str(reply)); print("VEO SUBMIT FAILED", st); return rec
    name = reply.get("name"); rec["request_id"] = name

    def check():
        code, op = C.http_json("POST", f"{url}:fetchPredictOperation", hdr, {"operationName": name})
        if code != 200:
            return True, {"$error": code, "reply": op}
        return bool(op.get("done")), op

    op = C.poll(check, 5.0, 120)
    resp = (op.get("response") or {}) if isinstance(op, dict) else {}
    vids = resp.get("videos") or []
    if op.get("$error") or op.get("$timeout") or op.get("error") or not vids or not vids[0].get("bytesBase64Encoded"):
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="failed_or_filtered", error=C.scrub(str(op))[:400]); record(rec)
        settle(asset_id, "failed_or_filtered", str(op), name); print("VEO FAILED", C.scrub(str(op))[:300]); return rec
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(base64.b64decode(vids[0]["bytesBase64Encoded"]))
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", file=str(out.relative_to(V3))); record(rec); settle(asset_id, "ok", f"-> {out.name}", name)
    print(f"saved {out} in {rec['latency_s']} s"); return rec


def omni_i2v(asset_id: str, prompt: str, image: Path, out: Path, duration: int = 10, resolution: str = "720p", aspect: str = "16:9") -> dict:
    """Gemini Omni 1.1 Flash image-to-video with native audio on Vertex interactions. PROVENANCE: preprod/recipes/google_video.py."""
    route = f"omni/vertex/image_to_video/{resolution}"; unit, price = PRICES[route]
    est = reserve(asset_id, route, duration, price)
    b, mime = C.b64file(image)
    body = {"model": "gemini-omni-1.1-flash-preview", "input": [{"type": "text", "text": prompt}, {"type": "image", "data": b, "mime_type": mime}],
            "response_format": [{"type": "video", "aspect_ratio": aspect, "resolution": resolution, "duration": f"{duration}s"}],
            "generation_config": {"video_config": {"task": "image_to_video"}}}
    rec = {"asset_id": asset_id, "prompt": prompt, "source": f"anchor still {image.name}", "provider": "google", "model": "gemini-omni-1.1-flash-preview", "surface": "vertex interactions",
           "unit_price_usd": price, "unit": unit, "quantity": duration, "est_usd": round(est, 6), "start": now(), "params": body["response_format"][0]}
    t0 = time.time(); hdr = {"Authorization": f"Bearer {C.gcloud_sa_token()}"}
    st, reply = C.http_json("POST", VERTEX_INTERACTIONS, hdr, body, timeout=600)
    iid = reply.get("id") if isinstance(reply, dict) else None
    data = None
    if st == 200 and isinstance(reply, dict):
        for step in reply.get("steps") or []:
            if step.get("type") != "model_output":
                continue
            for c in step.get("content") or []:
                if c.get("type") == "video" and c.get("data"):
                    data = base64.b64decode(c["data"])
    if data is None:
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status=f"http_{st}_no_video", error=C.scrub(str(reply))[:400]); record(rec)
        settle(asset_id, f"http_{st}_no_video", str(reply), iid); print("OMNI FAILED", st, C.scrub(str(reply))[:300]); return rec
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", file=str(out.relative_to(V3)), request_id=iid, provider_meta={"usage": reply.get("usage")}); record(rec)
    settle(asset_id, "ok", f"-> {out.name}", iid); print(f"saved {out} in {rec['latency_s']} s"); return rec


def verdict(asset_id: str, verdict_: str, reason: str = "", repair: str = ""):
    """Append a human verdict line for an asset (accept / reject) with the failure reason and repair/fallback taken."""
    record({"asset_id": asset_id, "verdict": verdict_, "reason": reason, "repair_or_fallback": repair, "utc": now()})
    print(f"[verdict] {asset_id}: {verdict_} {reason}")


def summary():
    tot = ledger_total()
    print(f"cumulative reserved USD {tot:.4f} = INR {tot * INR_PER_USD:.1f} of INR {CAP_INR:.0f}")
    by = {}
    for l in LEDGER.read_text().splitlines() if LEDGER.exists() else []:
        r = json.loads(l)
        if r.get("status") == "reserved":
            by.setdefault(r["route"], [0, 0.0]); by[r["route"]][0] += 1; by[r["route"]][1] += r["est_usd"]
    for k, (n, u) in sorted(by.items()):
        print(f"  {k:48s} {n:2d} calls  USD {u:.4f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["summary", "verdict"])
    ap.add_argument("--asset"); ap.add_argument("--verdict"); ap.add_argument("--reason", default=""); ap.add_argument("--repair", default="")
    a = ap.parse_args()
    if a.cmd == "summary":
        summary()
    else:
        verdict(a.asset, a.verdict, a.reason, a.repair)


def veo_t2v_extend(asset_id: str, prompt1: str, prompt2: str, out: Path, resolution: str = "720p", aspect: str = "9:16", audio: bool = True) -> dict:
    """Veo 3.1 Fast text-to-video 8 s + one 7-s extension (= 15 s). PROVENANCE: preprod/recipes/google_video.py extend mode; Lab VID-MS-01 chain 2/2."""
    route = f"veo-3.1-fast-generate-001/i2v/{resolution}"; unit, price = PRICES[route]   # same per-second pin as i2v (t2v/extend billed per second)
    est = reserve(asset_id, route, 15, price)
    params = {"sampleCount": 1, "aspectRatio": aspect, "resolution": resolution, "durationSeconds": 8, "generateAudio": audio}
    rec = {"asset_id": asset_id, "prompt": prompt1 + " || EXTEND: " + prompt2, "source": "text-to-video + extend", "provider": "google", "model": "veo-3.1-fast-generate-001",
           "surface": "vertex predictLongRunning (t2v + extend)", "unit_price_usd": price, "unit": unit, "quantity": 15, "est_usd": round(est, 6), "start": now(), "params": params}
    t0 = time.time(); hdr = {"Authorization": f"Bearer {C.gcloud_sa_token()}"}; url = f"{REGIONAL}/veo-3.1-fast-generate-001"

    def op(body):
        st, reply = C.http_json("POST", f"{url}:predictLongRunning", hdr, body)
        if st != 200:
            return None, f"submit_http_{st}: {C.scrub(str(reply))[:200]}"
        name = reply.get("name")
        def check():
            code, o = C.http_json("POST", f"{url}:fetchPredictOperation", hdr, {"operationName": name})
            if code != 200:
                return True, {"$error": code, "reply": o}
            return bool(o.get("done")), o
        o = C.poll(check, 5.0, 120); resp = (o.get("response") or {}) if isinstance(o, dict) else {}; vids = resp.get("videos") or []
        if o.get("$error") or o.get("$timeout") or o.get("error") or not vids or not vids[0].get("bytesBase64Encoded"):
            return None, C.scrub(str(o))[:300]
        return base64.b64decode(vids[0]["bytesBase64Encoded"]), name

    data, name1 = op({"instances": [{"prompt": prompt1}], "parameters": params})
    if data is None:
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="failed_call1", error=name1); record(rec); settle(asset_id, "failed_call1", name1); print("VEO T2V FAILED", name1); return rec
    out.parent.mkdir(parents=True, exist_ok=True); (out.with_suffix(".call1.mp4")).write_bytes(data)
    ext = {"instances": [{"prompt": prompt2, "video": {"bytesBase64Encoded": base64.b64encode(data).decode(), "mimeType": "video/mp4"}}],
           "parameters": {k: v for k, v in params.items() if k != "durationSeconds"}}
    data2, name2 = op(ext)
    if data2 is None:
        rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="failed_extend", error=name2, file=str(out.with_suffix(".call1.mp4").relative_to(V3))); record(rec); settle(asset_id, "failed_extend", name2, name1); print("VEO EXTEND FAILED", name2); return rec
    out.write_bytes(data2)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", file=str(out.relative_to(V3)), request_id=f"{name1} + {name2}"); record(rec); settle(asset_id, "ok", f"-> {out.name}", name2)
    print(f"saved {out} in {rec['latency_s']} s"); return rec
