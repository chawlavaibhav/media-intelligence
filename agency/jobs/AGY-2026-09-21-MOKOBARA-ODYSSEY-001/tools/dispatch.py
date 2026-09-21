#!/usr/bin/env python3
"""Paid dispatch for AGY-2026-09-21-MOKOBARA-ODYSSEY-001 — one job ledger, one cap (USD 12.00).

CREDITS ONLY (Google Gemini API key / Vertex service account). Routes in this file and nothing else
(cell status read from eval/capability-map/TAINT-REGISTER-v1.yaml on this base, price from the runtime PriceBook at call time):
  nano-banana-2          IMG-CORE/nano-banana-2              clean_observed  prod=True  7/8  USD 0.067 per image (gemini_api)
  veo-3.1-fast           VID-T2V/veo-3.1-fast                clean_observed  prod=True  4/8  USD 0.10 per second (vertex)
  veo-3.1-fast-i2v       VID-I2V/veo-3.1-fast-i2v            clean_observed  prod=True  5/8  USD 0.10 per second (vertex)
  veo-3.1-fast-ref2v     VID-REF/veo-3.1-fast-ref2v+native   clean_observed  prod=True  2/4  USD 0.10 per second (vertex)
  gemini-omni-1.1-flash  VID-T2V/gemini-omni-1.1-flash       clean_observed  prod=True  8/8  USD 0.10136 per second (gemini_api)
  lyria                  MUS/lyria+native                    clean_observed  prod=True  4/4  USD 0.06 per clip (vertex)
manual_only cells (veo extend chain, omni 10 s multi-shot, two-speaker) are NOT in this file.

Every paid call: (1) checks the cumulative RESERVED total in gen/LEDGER.jsonl against CAP_USD, (2) appends a reservation
line BEFORE the request leaves, (3) settles it after, failed calls included, (4) appends one attempt record to
gen/ATTEMPTS.jsonl. No hidden retry: a re-send is a new attempt with its own line. An unpriced route is refused.

PROVENANCE: tools/PROVENANCE.md (copied from the RENTOK-CREATIVE-QUALITY-001 treatments dispatch @ 41d97c6; t2v added from
eval/harness-v2/adapters/vertex_veo.py; lyria from Lane A @ 0405feb0). Run with /usr/bin/python3 after `source ~/.mi-keys`.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
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

LEDGER = JOB / "gen/LEDGER.jsonl"
ATTEMPTS = JOB / "gen/ATTEMPTS.jsonl"
CAP_USD = 12.0
CAP_STATED_BY = "human Controller, input/SPEND-AUTHORISATION.md recorded 2026-09-21T17:21:17Z: 'USD 12 (Recommended)'"
POOL_READING = "attested_by_human (2026-09-20; SPEND-AUTHORISATION.md: not machine-readable; reservations are upper bounds)"

# route_key -> (surface model id, provider surface, billing pool, cell, status, production_use_allowed, accepts)
ROUTES = {
    "nano-banana-2":         ("gemini-3.1-flash-image",     "gemini_api", "credits", "IMG-CORE/nano-banana-2",            "clean_observed", True, "7/8"),
    "veo-3.1-fast":          ("veo-3.1-fast-generate-001",  "vertex",     "credits", "VID-T2V/veo-3.1-fast",              "clean_observed", True, "4/8"),
    "veo-3.1-fast-i2v":      ("veo-3.1-fast-generate-001",  "vertex",     "credits", "VID-I2V/veo-3.1-fast-i2v",          "clean_observed", True, "5/8"),
    "veo-3.1-fast-ref2v":    ("veo-3.1-fast-generate-001",  "vertex",     "credits", "VID-REF/veo-3.1-fast-ref2v+native", "clean_observed", True, "2/4"),
    "gemini-omni-1.1-flash": ("gemini-omni-1.1-flash",      "gemini_api", "credits", "VID-T2V/gemini-omni-1.1-flash",     "clean_observed", True, "8/8"),
    "lyria":                 ("lyria-002",                  "vertex",     "credits", "MUS/lyria+native",                  "clean_observed", True, "4/4"),
}
# Stage 2 (c) IP list + (b) forbidden claims + the brand name (no in-model lettering; the wordmark is code-composited)
FORBIDDEN_PROMPT_WORDS = re.compile(
    r"\b(odyssey|odysseus|penelope|telemachus|ithaca|calypso|homer|nolan|universal|cast away|castaway|wilson|hanks|fedex|"
    r"robinson crusoe|matt damon|zendaya|lupita|holland|indestructible|waterproof|lifetime|guarantee|best-selling|mokobara)\b", re.I)
PROJECT = "vertexaiproject-507518"; REGION = "us-central1"
VEO_URL = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/publishers/google/models/veo-3.1-fast-generate-001"
OMNI_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
SA_FILE = "~/.aight-litellm-keys/vertex-sa.json"
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


def _ledger_lines():
    if not LEDGER.exists():
        return []
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]


def ledger_reserved() -> float:
    return sum(l.get("reserved_usd", 0) for l in _ledger_lines() if l.get("status") == "reserved")


def next_attempt_id() -> str:
    n = sum(1 for l in ATTEMPTS.read_text().splitlines() if l.strip()) if ATTEMPTS.exists() else 0
    return f"att-{n + 1:03d}"


def route_allowed(route_key: str):
    if route_key not in ROUTES:
        sys.exit(f"REFUSED: route {route_key!r} is not in this tool. Nothing sent.")
    ep, surface, pool, cell, status, allowed, acc = ROUTES[route_key]
    if allowed is not True or pool != "credits":
        sys.exit(f"REFUSED: route {route_key} is not production_use_allowed on credits. Nothing sent.")


def reserve(attempt_id: str, asset_id: str, route_key: str, q, is_repair: bool) -> float:
    if CAP_USD <= 0.0 or not CAP_STATED_BY:
        sys.exit("REFUSED: no written spend cap recorded. Nothing sent.")
    est = float(q.expected_cost_usd)
    cum = ledger_reserved() + est
    if cum > CAP_USD + 1e-9:
        sys.exit(f"REFUSED: cumulative reserved USD {cum:.4f} would exceed the job cap USD {CAP_USD:.2f}. HARD STOP; nothing sent.")
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps({"utc": now(), "attempt_id": attempt_id, "asset_id": asset_id, "route": route_key,
                            "quantity": str(q.quantity), "unit": q.unit, "unit_price_usd": str(q.unit_price),
                            "reserved_usd": round(est, 6), "cumulative_reserved_usd": round(cum, 6),
                            "cap_usd": CAP_USD, "cap_stated_by": CAP_STATED_BY, "pool_readings": POOL_READING,
                            "is_repair": is_repair, "status": "reserved"}) + "\n")
    print(f"[reserve] {attempt_id} {asset_id} {route_key} {q.quantity} {q.unit} x {q.unit_price} = USD {est:.4f}; job USD {cum:.4f} of {CAP_USD:.2f}")
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
    ep, surface, pool, cell, status, allowed, acc = ROUTES[route_key]
    return {"attempt_id": attempt_id, "asset_id": asset_id, "route_cell": route_key, "cell": cell,
            "evidence_status": status, "production_use_allowed": allowed, "accepts": acc, "endpoint": ep, "surface": surface,
            "pool": pool, "pool_readings": POOL_READING, "unit_price_usd": str(q.unit_price), "quantity": str(q.quantity),
            "quantity_unit": q.unit, "reserved_usd": round(float(q.expected_cost_usd), 6), "settled_usd": None, "prompt": prompt,
            "params": params, "start_utc": now(), "end": None, "latency_s": None, "status": None, "failure_basis": None,
            "artifact_path": str(out.resolve().relative_to(JOB)), "artifact_sha256": None, "verdict": "pending", "is_repair": is_repair}


def deck_strings() -> list[str]:
    p = JOB / "copy-deck.json"
    if not p.exists():
        return []
    d = json.load(open(p))
    return [v for k, v in d["strings"].items() if isinstance(v, str)]


def _prompt_guard(prompt: str, exact_strings: list[str]) -> None:
    """No IP/claim/brand word, no exact copy-deck string, and the no-lettering clause present (LIMIT-TEXT)."""
    hit = FORBIDDEN_PROMPT_WORDS.search(prompt)
    if hit:
        sys.exit(f"REFUSED: forbidden word {hit.group(0)!r} in the prompt. Nothing sent.")
    low = prompt.lower()
    for s in exact_strings:
        if s and len(s) > 3 and s.lower() in low:
            sys.exit(f"REFUSED: exact copy-deck string {s!r} appears in a generation prompt (text is code-set). Nothing sent.")
    if "no text" not in low and "no lettering" not in low and "textless" not in low:
        sys.exit("REFUSED: the prompt must state the no-lettering clause (LIMIT-TEXT). Nothing sent.")


def _confirm(args):
    if not getattr(args, "confirm_spend", False):
        sys.exit("REFUSED: pass --confirm-spend to send a paid request. Nothing was sent.")


# ── Nano Banana 2 on the Gemini API (credits) — stills ───────────────────────
def nb2(asset_id: str, prompt: str, out: Path, aspect: str, refs: list[Path] | None = None, is_repair=False) -> dict:
    route_key = "nano-banana-2"; route_allowed(route_key); ep = ROUTES[route_key][0]
    _prompt_guard(prompt, deck_strings())
    q = quote(route_key, {"params": {}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    parts = [{"text": prompt}]
    for rp in refs or []:
        b, mime = C.b64file(rp); parts.append({"inlineData": {"mimeType": mime, "data": b}})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": aspect}}}
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair,
                   {"aspect": aspect, "reference_images": [r.name for r in refs or []], "ref_sha256": [sha256(r) for r in refs or []]})
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


# ── Veo 3.1 fast on Vertex (credits) — t2v / i2v / ref2v ─────────────────────
def veo(asset_id: str, prompt: str, out: Path, workflow: str, duration_s: int, image: Path | None = None,
        refs: list[Path] | None = None, negative: str | None = None, aspect: str = "9:16", resolution: str = "720p",
        generate_audio: bool = True, is_repair=False) -> dict:
    """adapters/vertex_veo.py request shape. t2v: instances[0].prompt only; i2v: + image; ref2v: + referenceImages (<= 3, asset)."""
    route_key = {"t2v": "veo-3.1-fast", "i2v": "veo-3.1-fast-i2v", "ref2v": "veo-3.1-fast-ref2v"}[workflow]; route_allowed(route_key)
    _prompt_guard(prompt, deck_strings())
    if duration_s not in (4, 6, 8):
        sys.exit("REFUSED: Veo durations are 4, 6 or 8 s (pinned). Nothing sent.")
    if aspect not in ("16:9", "9:16") or resolution not in ("720p", "1080p"):
        sys.exit("REFUSED: aspect/resolution outside the pinned Veo enums. Nothing sent.")
    q = quote(route_key, {"params": {"duration_s": duration_s}})
    inst: dict = {"prompt": prompt}
    if workflow == "i2v":
        if not image:
            sys.exit("REFUSED: i2v needs --image. Nothing sent.")
        b, mime = C.b64file(image); inst["image"] = {"bytesBase64Encoded": b, "mimeType": mime}
    elif workflow == "ref2v":
        if not refs or len(refs) > 3:
            sys.exit("REFUSED: ref2v needs 1-3 --ref images (pinned: up to three asset references). Nothing sent.")
        inst["referenceImages"] = []
        for rp in refs:
            b, mime = C.b64file(rp); inst["referenceImages"].append({"image": {"bytesBase64Encoded": b, "mimeType": mime}, "referenceType": "asset"})
    params = {"sampleCount": 1, "durationSeconds": duration_s, "aspectRatio": aspect, "resolution": resolution, "generateAudio": generate_audio}
    if negative:
        params["negativePrompt"] = negative
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair,
                   {**params, "workflow": workflow, "image": image.name if image else None, "refs": [r.name for r in refs or []],
                    "image_sha256": sha256(image) if image else None, "ref_sha256": [sha256(r) for r in refs or []]})
    t0 = time.time()
    tok = C.gcloud_sa_token(SA_FILE); headers = {"Authorization": f"Bearer {tok}"}
    st, reply = C.http_json("POST", f"{VEO_URL}:predictLongRunning", headers, {"instances": [inst], "parameters": params}, timeout=300)
    if st != 200 or not isinstance(reply, dict) or not reply.get("name"):
        return failure(rec, http_status=st, message=str(reply), status=f"http_{st}")
    name = reply["name"]; rec["request_id"] = name

    def check():
        code, op = C.http_json("POST", f"{VEO_URL}:fetchPredictOperation", headers, {"operationName": name}, timeout=120)
        if code != 200 or not isinstance(op, dict):
            return True, {"$poll_error": code, "body": op}
        return bool(op.get("done")), op

    op = C.poll(check, interval_s=6.0, max_checks=120)
    if op.get("$timeout"):
        return failure(rec, message="poll timeout after 120 checks", timed_out=True, status="timeout")
    if op.get("$poll_error"):
        return failure(rec, http_status=op["$poll_error"], message=str(op.get("body")), status=f"poll_http_{op['$poll_error']}")
    if op.get("error"):
        return failure(rec, message=str(op["error"]), status="operation_error")
    resp = op.get("response") or {}
    vids = resp.get("videos") or []
    if not vids:
        if resp.get("raiMediaFilteredCount"):
            return failure(rec, message=f"safety_filtered: {resp.get('raiMediaFilteredReasons')}", status="refusal_or_empty")
        return failure(rec, message="done operation carried no videos", status="no_artifact")
    v0 = vids[0]
    if not v0.get("bytesBase64Encoded"):
        return failure(rec, message=f"artifact not inline: {v0.get('gcsUri')}", status="artifact_not_inline")
    data = base64.b64decode(v0["bytesBase64Encoded"])
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out), bytes=len(data),
               provider_meta={"operation": name, "raiMediaFilteredCount": resp.get("raiMediaFilteredCount")}); record(rec)
    settle(aid, "ok", f"{len(data)} bytes -> {out.name}", name); print(f"saved {out} ({len(data)} bytes) in {rec['latency_s']} s")
    return rec


# ── Gemini Omni 1.1 Flash on the Gemini API (credits) — t2v ──────────────────
def omni(asset_id: str, prompt: str, out: Path, duration_s: int, aspect: str = "9:16", resolution: str = "720p", is_repair=False) -> dict:
    route_key = "gemini-omni-1.1-flash"; route_allowed(route_key)
    _prompt_guard(prompt, deck_strings())
    if not (3 <= duration_s <= 10):
        sys.exit("REFUSED: Omni durations are 3-10 s (pinned). Nothing sent.")
    q = quote(route_key, {"params": {"duration_s": duration_s}})
    body = {"model": ROUTES[route_key][0], "input": [{"type": "text", "text": prompt}],
            "response_format": {"type": "video", "aspect_ratio": aspect, "resolution": resolution, "duration": f"{duration_s}s"},
            "generation_config": {"video_config": {"task": "text_to_video"}}}
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair, {"duration_s": duration_s, "aspect": aspect, "resolution": resolution, "task": "text_to_video"})
    t0 = time.time()
    st, reply = C.http_json("POST", OMNI_URL, {"x-goog-api-key": C.key("GOOGLE_API_KEY")}, body, timeout=900)
    iid = reply.get("id") if isinstance(reply, dict) else None; rec["request_id"] = iid
    if st != 200:
        return failure(rec, http_status=st, message=str(reply)[:600], status=f"http_{st}")
    if reply.get("status") not in ("completed", None):
        txt = str(reply.get("errors") or reply.get("error"))
        return failure(rec, message=f"interaction {reply.get('status')}: {txt}", status="refusal_or_empty" if any(w in txt.lower() for w in ("safety", "block", "policy", "prohibit", "violat")) else f"interaction_{reply.get('status')}")
    data = None
    for step in reply.get("steps") or []:
        if step.get("type") != "model_output":
            continue
        for c in step.get("content") or []:
            if c.get("type") == "video" and c.get("data"):
                data = base64.b64decode(c["data"]); break
        if data: break
    if not data:
        return failure(rec, message="completed interaction carried no inline video", status="no_artifact")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    rec.update(end=now(), latency_s=round(time.time() - t0, 1), status="ok", artifact_sha256=sha256(out), bytes=len(data),
               provider_meta={"interaction_id": iid, "usage": reply.get("usage")}); record(rec)
    settle(aid, "ok", f"{len(data)} bytes -> {out.name}", iid); print(f"saved {out} ({len(data)} bytes) in {rec['latency_s']} s")
    return rec


# ── Lyria on Vertex (credits) — one music bed ────────────────────────────────
def lyria(asset_id: str, prompt: str, out: Path, negative: str | None = None, is_repair=False) -> dict:
    """MUS/lyria+native, clean_observed 4/4, USD 0.06 per clip (≈ 32.8 s, trimmed by code). Lane A recipe @ 0405feb0."""
    route_key = "lyria"; route_allowed(route_key); ep = ROUTES[route_key][0]
    hit = FORBIDDEN_PROMPT_WORDS.search(prompt)
    if hit:
        sys.exit(f"REFUSED: forbidden word {hit.group(0)!r} in the music prompt. Nothing sent.")
    q = quote(route_key, {"params": {}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    url = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/publishers/google/models/{ep}:predict"
    inst = {"prompt": prompt}
    if negative:
        inst["negative_prompt"] = negative
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair, {"negative_prompt": negative, "sample_count": 1})
    t0 = time.time()
    st, reply = C.http_json("POST", url, {"Authorization": f"Bearer {C.gcloud_sa_token(SA_FILE)}"},
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
    print(f"cap USD {CAP_USD:.2f} ({CAP_STATED_BY}); reserved USD {ledger_reserved():.4f}; remaining USD {CAP_USD - ledger_reserved():.4f}")
    if ATTEMPTS.exists():
        for l in ATTEMPTS.read_text().splitlines():
            r = json.loads(l)
            print(f"  {r['attempt_id']} {r['asset_id']:<16} {r['route_cell']:<22} USD {r['reserved_usd']:<7} {r['status']:<14} {r.get('verdict')}  {r.get('artifact_path')}")


def quotes():
    for rk, facts in [("nano-banana-2", {"params": {}}), ("veo-3.1-fast", {"params": {"duration_s": 8}}), ("veo-3.1-fast-i2v", {"params": {"duration_s": 8}}),
                      ("veo-3.1-fast-ref2v", {"params": {"duration_s": 8}}), ("gemini-omni-1.1-flash", {"params": {"duration_s": 8}}), ("lyria", {"params": {}})]:
        q = pricebook().quote(rk, facts)
        print(rk, "priced" if q.priced else "UNPRICED", q.unit_price, q.unit, "x", q.quantity, q.quantity_unit, "=", q.expected_cost_usd, q.billing_pool, q.surface)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("summary"); sub.add_parser("quotes")
    for name in ("nb2", "veo", "omni", "lyria"):
        p = sub.add_parser(name)
        p.add_argument("--asset-id", required=True); p.add_argument("--prompt-file", required=True); p.add_argument("--out", required=True)
        p.add_argument("--repair", action="store_true"); p.add_argument("--confirm-spend", action="store_true")
        if name == "nb2":
            p.add_argument("--aspect", required=True); p.add_argument("--ref", action="append", default=[])
        if name == "veo":
            p.add_argument("--workflow", required=True, choices=["t2v", "i2v", "ref2v"]); p.add_argument("--duration", type=int, required=True)
            p.add_argument("--image"); p.add_argument("--ref", action="append", default=[]); p.add_argument("--negative-file")
            p.add_argument("--no-audio", action="store_true"); p.add_argument("--resolution", default="720p")
        if name == "omni":
            p.add_argument("--duration", type=int, required=True); p.add_argument("--resolution", default="720p")
        if name == "lyria":
            p.add_argument("--negative-file")
    a = ap.parse_args()
    if a.cmd == "summary":
        summary()
    elif a.cmd == "quotes":
        quotes()
    else:
        _confirm(a)
        prompt = Path(a.prompt_file).read_text().strip()
        out = Path(a.out)
        if a.cmd == "nb2":
            nb2(a.asset_id, prompt, out, a.aspect, [Path(r) for r in a.ref], a.repair)
        elif a.cmd == "veo":
            neg = Path(a.negative_file).read_text().strip() if a.negative_file else None
            veo(a.asset_id, prompt, out, a.workflow, a.duration, Path(a.image) if a.image else None,
                [Path(r) for r in a.ref], neg, resolution=a.resolution, generate_audio=not a.no_audio, is_repair=a.repair)
        elif a.cmd == "omni":
            omni(a.asset_id, prompt, out, a.duration, resolution=a.resolution, is_repair=a.repair)
        else:
            neg = Path(a.negative_file).read_text().strip() if a.negative_file else None
            lyria(a.asset_id, prompt, out, neg, a.repair)
