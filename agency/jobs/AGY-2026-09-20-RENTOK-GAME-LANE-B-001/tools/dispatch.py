#!/usr/bin/env python3
"""Paid dispatch for AGY-2026-09-20-RENTOK-GAME-LANE-B-001 (lane B) — one job, one append-only ledger, one cap.

ADAPTED from tools/reference-kit/dispatch.py (the Cumin Job B tool, production-proven on cases 001/002):
  * job paths point at THIS job (gen/LEDGER.jsonl, gen/ATTEMPTS.jsonl under agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-B-001);
  * CAP_USD = 10.0 — the Controller's written cap (JOB.yaml spend.cap; recorded 2026-09-20). Before that message it was 0.0 and
    every reserve() refused;
  * every fal route (seedream / flux / kling / wan / minimax / fal balance) is REMOVED — this job uses no fal and no cash surface;
  * the remaining routes are the credit pools the Controller allowed: nano-banana-2 and nano-banana-pro (Gemini API, credits),
    Lyria (Vertex, credits), Sarvam bulbul:v3 (Sarvam credits), ElevenLabs v3 direct (plan credits). Veo/Omni video routes are
    not in this job's plan (Stage 4) and are deliberately not wired here — adding one is a plan change, not a tool tweak.

Every paid call: (1) checks the cumulative RESERVED total in gen/LEDGER.jsonl against CAP_USD, (2) appends a reservation line
BEFORE the request leaves, (3) settles the line after, failed calls included, (4) appends one attempt record to
gen/ATTEMPTS.jsonl in the JOB.yaml `spend.attempts[]` vocabulary. Failures are classified by runtime/execute/provider_errors
(an outage is infrastructure_transient, never a model failure). No hidden retry: a re-send is a new attempt with its own line.
Prices are re-read live from the runtime PriceBook at import. Keys by name from `source ~/.mi-keys`; never printed.

Run with /usr/bin/python3 (yaml, Pillow, numpy present) after `source ~/.mi-keys`.
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
CAP_USD = 10.0  # JOB.yaml spend.cap — Controller session message 2026-09-20, human answer "USD 10 per lane (Recommended)": USD 10.00, credits only (Google Vertex/Gemini, ElevenLabs plan, Sarvam), no fal, 0 hidden retries, hard stop.

# route_key (runtime PriceBook / taint-register cell) -> (provider model id, surface, billing pool)
ROUTES = {
    "nano-banana-2":        ("gemini-3.1-flash-image", "gemini_api", "credits"),      # IMG-CORE clean 7/8, use=True
    "nano-banana-pro":      ("gemini-3-pro-image", "gemini_api", "credits"),          # IMG-CORE clean 4/8, use=True (declared fallback only)
    "lyria":                ("lyria-002", "vertex", "credits"),                       # MUS clean 4/4, use=True
    "sarvam-bulbul-v3":     ("https://api.sarvam.ai/text-to-speech", "sarvam_direct", "sarvam_credits"),   # AUD-TTS clean 6/6
    "elevenlabs-v3-direct": ("https://api.elevenlabs.io/v1/text-to-speech", "elevenlabs_direct", "elevenlabs_credits"),  # AUD-TTS clean 4/6
}
PROJECT = "vertexaiproject-507518"; REGION = "us-central1"
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
    if CAP_USD <= 0.0:
        sys.exit("REFUSED: CAP_USD is 0.0 — no confirmed spend cap has been recorded for this job. Nothing sent. "
                 "(Set CAP_USD from the Controller's written cap and record it in JOB.yaml spend.cap first.)")
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


FORBIDDEN_PROMPT_WORDS = ("mario", "nintendo", "luigi", "bowser", "koopa", "goomba", "mushroom kingdom", "super mario", "peach")   # checker NOTE 4: "peach" added; the standalone "Super" rule is NOT applied here (it would block the brand tagline "superapp"); "super mario" covers the IP case


def guard_prompt(prompt: str) -> None:
    """Stage 2 §2.5 DET rule: no Nintendo name in any generation prompt; refuse before reserving."""
    low = prompt.lower()
    hits = [w for w in FORBIDDEN_PROMPT_WORDS if w in low]
    if hits:
        sys.exit(f"REFUSED: prompt contains forbidden IP word(s) {hits}; nothing sent")


# ── Google credits: Nano Banana stills on the Gemini API (pilot recipe; RO-04 case 001, RO-04 case 002) ──
def nb(asset_id: str, prompt: str, out: Path, aspect: str, route_key: str = "nano-banana-2", is_repair=False) -> dict:
    """Text-to-image, NO reference images (a referenced draw would not be a registered IMG-REF cell for this route; this job
    keeps consistency INSIDE one draw — sprite sheets / two-panel obstacles — instead)."""
    guard_prompt(prompt)
    ep, surface, pool = ROUTES[route_key]
    q = quote(route_key, {"params": {}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": aspect}}}
    rec = base_rec(aid, asset_id, route_key, q, prompt, out, is_repair, {"aspect": aspect})
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


# ── music ────────────────────────────────────────────────────────────────────
def lyria(asset_id: str, prompt: str, out: Path, negative: str | None = None, is_repair=False) -> dict:
    guard_prompt(prompt)
    route_key = "lyria"; ep, surface, pool = ROUTES[route_key]
    q = quote(route_key, {"params": {}})
    aid = next_attempt_id(); reserve(aid, asset_id, route_key, q, is_repair)
    url = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/publishers/google/models/{ep}:predict"
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
    print(f"CAP_USD {CAP_USD:.2f}; reserved USD {ledger_reserved():.4f}; remaining USD {CAP_USD - ledger_reserved():.4f}")
    if ATTEMPTS.exists():
        for l in ATTEMPTS.read_text().splitlines():
            r = json.loads(l)
            print(f"  {r['attempt_id']} {r['asset_id']:<14} {r['route_cell']:<22} USD {r['reserved_usd']:<7} {r['status']:<12} {r.get('verdict')}  {r.get('artifact_path')}")


def quotes():
    """USD 0: print the live PriceBook quote for every route in ROUTES (the Stage 4 spend table is built from these)."""
    for rk, facts in [("nano-banana-2", {"params": {}}), ("nano-banana-pro", {"params": {}}), ("lyria", {"params": {}}),
                      ("sarvam-bulbul-v3", {"params": {"chars": 72}}), ("elevenlabs-v3-direct", {"params": {"chars": 72}})]:
        q = pricebook().quote(rk, facts)
        print(rk.ljust(22), "priced" if q.priced else "UNPRICED", q.unit_price, q.unit, "x", q.quantity, q.quantity_unit, "=", q.expected_cost_usd, q.billing_pool)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["summary", "quotes"])
    a = ap.parse_args()
    {"summary": summary, "quotes": quotes}[a.cmd]()
