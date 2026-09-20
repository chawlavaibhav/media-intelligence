#!/usr/bin/env python3
"""Paid dispatch for AGY-2026-09-20-RENTOK-GAME-LANE-A-001 — one job, one append-only ledger, one cap.

CREDITS ONLY. Two routes exist in this file and nothing else can be sent from it:
  nano-banana-2  (gemini-3.1-flash-image on the Gemini API; Google credits)  — every generated still (sprites, plate)
  lyria          (lyria-002 on Vertex; Google credits)                       — the one music bed
The fal routes, the Veo/Omni video routes, Sarvam, ElevenLabs and Gemini TTS from the reference kit are REMOVED:
this plan animates by code and has no voice (Stage 3), so no other paid path may exist here by accident.

Every paid call: (1) checks the cumulative RESERVED total in gen/LEDGER.jsonl against CAP_USD, (2) appends a
reservation line BEFORE the request leaves, (3) settles the line after, failed calls included, (4) appends one
attempt record to gen/ATTEMPTS.jsonl in the JOB.yaml `spend.attempts[]` vocabulary. Failures are classified by
runtime/execute/provider_errors.classify — an outage is infrastructure_transient, never a model failure. No hidden
retry: a re-send is a new attempt with its own line.

CAP_USD was 0.0 until the Controller's written cap arrived (2026-09-21); it is now 10.0 with CAP_STATED_BY recorded.

PROVENANCE: transport (submit → bounded poll → download, key-by-name, scrubbing) is the reference kit
tools/reference-kit/dispatch.py (Cumin Job B @ 5c33173, itself from the pilot recipes production-proven on cases
001 and 002). Prices are re-read live from the runtime PriceBook at import.

Run with /usr/bin/python3 after `source ~/.mi-keys` (values never printed).
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

GEN = JOB / "gen"
LEDGER = GEN / "LEDGER.jsonl"
ATTEMPTS = GEN / "ATTEMPTS.jsonl"
CAP_USD = 10.0  # JOB.yaml spend.cap — USD 10.00 for this lane, credits only, no fal, 0 hidden retries, hard stop;
                # stated by the human Controller via the Controller session message 2026-09-20 (2026-09-20T18:44Z).
CAP_STATED_BY = "human Controller via Controller session message, 2026-09-20T18:44Z, 'USD 10 per lane (Recommended)'"

# route_key (runtime PriceBook / taint register cell) -> (model id, provider surface, billing pool)
ROUTES = {
    "nano-banana-2": ("gemini-3.1-flash-image", "gemini_api", "credits"),
    "lyria":         ("lyria-002", "vertex", "credits"),
}
FORBIDDEN_PROMPT_WORDS = re.compile(r"\b(mario|luigi|nintendo|goomba|koopa|bowser|peach|yoshi|mushroom kingdom|super star|fire flower|warp pipe)\b", re.I)
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
    if CAP_USD <= 0.0 or not CAP_STATED_BY:
        sys.exit("REFUSED: no written spend cap recorded (CAP_USD is 0.0 / CAP_STATED_BY unset). Nothing sent.")
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
                            "cap_usd": CAP_USD, "cap_stated_by": CAP_STATED_BY, "is_repair": is_repair, "status": "reserved"}) + "\n")
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


def _prompt_guard(prompt: str, exact_strings: list[str]) -> None:
    """Pre-dispatch A3 + Stage 2c: no critical string and no Nintendo name may reach a generation prompt."""
    hit = FORBIDDEN_PROMPT_WORDS.search(prompt)
    if hit:
        sys.exit(f"REFUSED: forbidden IP word {hit.group(0)!r} in the prompt. Nothing sent.")
    low = prompt.lower()
    for s in exact_strings:
        if s and len(s) > 3 and s.lower() in low:
            sys.exit(f"REFUSED: exact copy-deck string {s!r} appears in a generation prompt (mechanism B: text is code-set). Nothing sent.")
    if "no text" not in low and "no lettering" not in low and "textless" not in low:
        sys.exit("REFUSED: the plate/sprite prompt must state the no-lettering clause (LIMIT-TEXT). Nothing sent.")


def deck_strings() -> list[str]:
    """Critical strings that must never reach a generation prompt: every deck string except the HUD furniture
    (hud_whitelist_for_claim_scan — e.g. 'PG OWNER', which is also the natural description of the character)."""
    d = json.load(open(JOB / "copy-deck.json"))
    skip = set(d.get("hud_whitelist_for_claim_scan", []))
    return [v for k, v in d["strings"].items() if isinstance(v, str) and k not in skip]


# ── Nano Banana 2 on the Gemini API (credits) — stills only ──────────────────
def nb2(asset_id: str, prompt: str, out: Path, aspect: str, refs: list[Path] | None = None, is_repair=False) -> dict:
    """Nano Banana 2 (IMG-CORE/nano-banana-2, clean_observed 7/8, production_use_allowed True; the map lists the
    surface as vertex — this call uses the Gemini API endpoint as cases 001/002 did (RO-04 both), same credits pool).
    Reference images are optional and, when used, are a micro-qualification (no registered IMG-REF cell on this route)."""
    route_key = "nano-banana-2"; ep, surface, pool = ROUTES[route_key]
    _prompt_guard(prompt, deck_strings())
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


# ── Lyria 2 on Vertex (credits) — the music bed ──────────────────────────────
def lyria(asset_id: str, prompt: str, out: Path, negative: str | None = None, is_repair=False) -> dict:
    """MUS/lyria+native, clean_observed 4/4, production_use_allowed True, USD 0.06 per clip (≈ 32.8 s, trimmed by code).
    Known: 3 provider errors on a wording-heavy prompt in case 001 (RO-09 / SD-10) — keep the wording neutral."""
    route_key = "lyria"; ep, surface, pool = ROUTES[route_key]
    hit = FORBIDDEN_PROMPT_WORDS.search(prompt)
    if hit:
        sys.exit(f"REFUSED: forbidden IP word {hit.group(0)!r} in the music prompt. Nothing sent.")
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
    print(f"cap USD {CAP_USD:.2f} (stated by: {CAP_STATED_BY}); reserved USD {ledger_reserved():.4f}; remaining USD {CAP_USD - ledger_reserved():.4f}")
    if ATTEMPTS.exists():
        for l in ATTEMPTS.read_text().splitlines():
            r = json.loads(l)
            print(f"  {r['attempt_id']} {r['asset_id']:<16} {r['route_cell']:<14} USD {r['reserved_usd']:<7} {r['status']:<12} {r.get('verdict')}  {r.get('artifact_path')}")


def quotes():
    """USD-0: print the live quotes the plan is priced from."""
    for rk, facts in [("nano-banana-2", {"params": {}}), ("lyria", {"params": {}})]:
        q = pricebook().quote(rk, facts)
        print(rk, "priced" if q.priced else "UNPRICED", q.unit_price, q.unit, "x", q.quantity, q.quantity_unit, "=", q.expected_cost_usd, q.billing_pool)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["summary", "quotes"])
    a = ap.parse_args()
    {"summary": summary, "quotes": quotes}[a.cmd]()
