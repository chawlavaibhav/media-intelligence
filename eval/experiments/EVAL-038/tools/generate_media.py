#!/usr/bin/env python3
"""EVAL-038 media generation — product learning, NOT Capability Registry evidence.

Authority: DN-07. Executes a package's generation prompt into real media over the
cheapest verified route:

- image: `gemini-3.1-flash-image` (:generateContent, inline image bytes) — official
  price USD 0.067 per 1K-class image (standard tier), pinned in
  common/gemma-price-pin/gemini-api-pricing.html (sha256 47529589...); model id
  verified live (common/media-route-pin/flash-image-model.json).
- video: `veo-3.1-lite-generate-preview` (:predictLongRunning -> poll -> authenticated
  binary download; the merged EVAL-035 lifecycle) — official price USD 0.05 per
  generated second at 720p, same pinned page; model id verified live
  (common/media-route-pin/veo-lite-model.json). Provider charges only on successful
  generation.

Spend discipline: the shared EVAL-038 ledger (runs/spend-ledger.jsonl), reservation
before send, conservative ambiguous settlement, USD 10.00 hard cap, 0 retries.
The submit IS the trial; polls and the download never inflate the count.
Binary artifacts are committed bytes (EVAL-024 sealed pattern): media/ + manifest.

Usage:
  generate_media.py image --label <id> --prompt-file <p.txt> [--aspect 4:5]
  generate_media.py video --label <id> --prompt-file <p.txt> [--aspect 9:16]
                          [--seconds 8] [--resolution 720p]
"""
import argparse
import base64
import datetime
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.request

E38 = pathlib.Path(__file__).resolve().parents[1]
LEDGER = E38 / "runs/spend-ledger.jsonl"
MEDIA = E38 / "media"
HARD_CAP_USD = 10.00
BASE = "https://generativelanguage.googleapis.com/v1beta"

PRICE = {  # pinned: common/gemma-price-pin/gemini-api-pricing.html, 2026-09-01
    "image_usd_per_image_1k": 0.067,
    "video_usd_per_second_720p": 0.05,
}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def ledger_totals():
    committed = 0.0
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            rec = json.loads(line)
            if rec["entry"] in ("settle", "settle_ambiguous"):
                committed += rec["usd"]
    return committed

def ledger_append(rec):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")

def api(path, body=None, raw=False):
    key = os.environ["GOOGLE_API_KEY"]
    req = urllib.request.Request(
        BASE + path if path.startswith("/") else path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    return data if raw else json.loads(data)

def reserve_or_stop(trial_id, reservation):
    committed = ledger_totals()
    if committed + reservation > HARD_CAP_USD:
        ledger_append({"entry": "refuse", "trial_id": trial_id, "at": now(),
                       "reason": f"cap: committed {committed:.6f} + reservation "
                                 f"{reservation:.6f} > {HARD_CAP_USD}"})
        sys.exit(f"HARD STOP — cap would be exceeded ({committed:.6f} committed)")
    ledger_append({"entry": "reserve", "trial_id": trial_id, "usd": round(reservation, 6),
                   "at": now(), "committed_before": round(committed, 6)})

def persist(trial_id, media_bytes, media_kind, ext, request_body, provider_meta, cost):
    MEDIA.mkdir(parents=True, exist_ok=True)
    out = MEDIA / f"{trial_id}{ext}"
    out.write_bytes(media_bytes)
    rec = {
        "trial_id": trial_id, "media_kind": media_kind,
        "relative_path": f"media/{trial_id}{ext}",
        "bytes": len(media_bytes), "sha256": sha256(media_bytes),
        "request_body_sha256": sha256(json.dumps(request_body, sort_keys=True).encode()),
        "provider": provider_meta, "consumed_usd": round(cost, 6), "at": now(),
        "purpose": "product learning under DN-07 — NOT Capability Registry evidence",
    }
    (MEDIA / f"{trial_id}.request.json").write_text(
        json.dumps(request_body, indent=1, sort_keys=True))
    (MEDIA / f"{trial_id}.record.json").write_text(
        json.dumps(rec, indent=1, sort_keys=True))
    ledger_append({"entry": "settle", "trial_id": trial_id, "usd": round(cost, 6),
                   "at": now(), "artifact_sha256": rec["sha256"],
                   "artifact_bytes": rec["bytes"]})
    print(json.dumps(rec, indent=1, sort_keys=True))

def gen_image(args):
    trial_id = f"E038-media-{args.label}"
    prompt = pathlib.Path(args.prompt_file).read_text().strip()
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": args.aspect}}}
    cost = PRICE["image_usd_per_image_1k"]
    reserve_or_stop(trial_id, cost * 1.5)
    t0 = now()
    try:
        resp = api("/models/gemini-3.1-flash-image:generateContent", body)
    except Exception as e:
        ledger_append({"entry": "settle_ambiguous", "trial_id": trial_id,
                       "usd": round(cost * 1.5, 6), "at": now(),
                       "failure_class": type(e).__name__, "detail": str(e)[:500]})
        sys.exit(f"image generation failed (0 retries): {e}")
    img = None
    mime = None
    for part in resp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        blob = part.get("inlineData") or part.get("inline_data")
        if blob:
            img = base64.b64decode(blob["data"])
            mime = blob.get("mimeType") or blob.get("mime_type")
    if not img:
        ledger_append({"entry": "settle_ambiguous", "trial_id": trial_id,
                       "usd": round(cost * 1.5, 6), "at": now(),
                       "failure_class": "no_image_in_response",
                       "detail": json.dumps(resp)[:800]})
        sys.exit("no image bytes in response (0 retries)")
    ext = ".png" if (mime or "").endswith("png") else ".jpg"
    usage = resp.get("usageMetadata", {})
    persist(trial_id, img, "image", ext, body,
            {"model": "gemini-3.1-flash-image", "mime": mime,
             "usage": usage, "submitted_at": t0,
             "model_version": resp.get("modelVersion"),
             "response_id": resp.get("responseId")}, cost)

def gen_video(args):
    trial_id = f"E038-media-{args.label}"
    prompt = pathlib.Path(args.prompt_file).read_text().strip()
    model = "veo-3.1-lite-generate-preview"
    body = {"instances": [{"prompt": prompt}],
            "parameters": {"aspectRatio": args.aspect,
                           "durationSeconds": args.seconds,
                           "resolution": args.resolution}}
    cost = PRICE["video_usd_per_second_720p"] * args.seconds
    reserve_or_stop(trial_id, cost * 1.25)
    t0 = now()
    try:
        op = api(f"/models/{model}:predictLongRunning", body)
    except Exception as e:
        # submit failed before generation: provider charges only on success, but
        # after-send is ambiguous by discipline — settle conservatively.
        ledger_append({"entry": "settle_ambiguous", "trial_id": trial_id,
                       "usd": round(cost * 1.25, 6), "at": now(),
                       "failure_class": type(e).__name__, "detail": str(e)[:500]})
        sys.exit(f"video submit failed (0 retries): {e}")
    op_name = op.get("name")
    print(f"operation: {op_name}")
    deadline = time.time() + 15 * 60
    while time.time() < deadline:
        st = api(f"/{op_name}")
        if st.get("done"):
            break
        time.sleep(15)
    else:
        ledger_append({"entry": "settle_ambiguous", "trial_id": trial_id,
                       "usd": round(cost * 1.25, 6), "at": now(),
                       "failure_class": "poll_timeout", "operation": op_name})
        sys.exit("poll timeout (0 retries); operation name recorded")
    if st.get("error"):
        ledger_append({"entry": "settle_ambiguous", "trial_id": trial_id,
                       "usd": round(cost * 1.25, 6), "at": now(),
                       "failure_class": "operation_error",
                       "detail": json.dumps(st["error"])[:800]})
        sys.exit(f"operation error (0 retries): {st['error']}")
    resp = st.get("response", {})
    vids = (resp.get("generateVideoResponse", {}) or {}).get("generatedSamples") or []
    uri = None
    if vids:
        uri = (vids[0].get("video") or {}).get("uri")
    if not uri:
        # alternate response shape
        for v in (resp.get("generatedVideos") or []):
            uri = (v.get("video") or {}).get("uri")
            break
    if not uri:
        ledger_append({"entry": "settle_ambiguous", "trial_id": trial_id,
                       "usd": round(cost * 1.25, 6), "at": now(),
                       "failure_class": "no_video_uri",
                       "detail": json.dumps(st)[:800]})
        sys.exit("no video uri in finished operation (0 retries)")
    media_bytes = api(uri if uri.startswith("http") else "/" + uri, raw=True)
    if not isinstance(media_bytes, bytes) or len(media_bytes) < 1000:
        ledger_append({"entry": "settle_ambiguous", "trial_id": trial_id,
                       "usd": round(cost * 1.25, 6), "at": now(),
                       "failure_class": "download_invalid"})
        sys.exit("download returned no plausible binary (0 retries)")
    persist(trial_id, media_bytes, "video", ".mp4", body,
            {"model": model, "operation": op_name, "video_uri": uri,
             "submitted_at": t0, "seconds": args.seconds,
             "aspect": args.aspect, "resolution": args.resolution}, cost)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="kind", required=True)
    im = sub.add_parser("image")
    im.add_argument("--label", required=True)
    im.add_argument("--prompt-file", required=True)
    im.add_argument("--aspect", default="4:5")
    vi = sub.add_parser("video")
    vi.add_argument("--label", required=True)
    vi.add_argument("--prompt-file", required=True)
    vi.add_argument("--aspect", default="9:16")
    vi.add_argument("--seconds", type=int, default=8)
    vi.add_argument("--resolution", default="720p")
    args = ap.parse_args()
    if (MEDIA / f"E038-media-{args.label}.record.json").exists():
        sys.exit(f"refusing regeneration: E038-media-{args.label} already sealed")
    if args.kind == "image":
        gen_image(args)
    else:
        gen_video(args)

if __name__ == "__main__":
    main()
