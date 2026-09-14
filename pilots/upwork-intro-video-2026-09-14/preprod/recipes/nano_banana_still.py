#!/usr/bin/env python3
"""Nano Banana 2 (gemini-3.1-flash-image) still on the Gemini Developer API, key GOOGLE_API_KEY.

PROVENANCE: body copied from eval/harness-v2/adapters/vertex_gemini_image.py _build_body (shared byte-for-byte by
gemini_api_image.py); this surface is live-proven for image generation by EVAL-038 (2026-09-01). The Lab's Nano Banana 2
stills (IMG-CORE 7/8, IMG-TEXT 4/4, topo3 plate 1/2) were made on Vertex with the same body.
  POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent   header x-goog-api-key
  {"contents":[{"role":"user","parts":[{"text":prompt}, {"inlineData":{...}}...]}],
   "generationConfig":{"responseModalities":["IMAGE"],"candidateCount":1,"imageConfig":{"aspectRatio":"16:9"}}}
  1K output by default (no imageSize sent) -> USD 0.067 per image (pinned Gemini API pricing page 2026-09-09).
  Reference images (for a consistent presenter across stills) go inline as extra parts (edit form); then the model
  follows them. Nano Banana Pro = model gemini-3-pro-image, USD 0.134.
NEVER RUN.

USAGE
  source ~/.mi-keys
  python3 nano_banana_still.py --prompt "..." --aspect 16:9 --out portrait.png --dry-run
  python3 nano_banana_still.py --prompt "..." --ref portrait.png --aspect 16:9 --out portrait_v2.png --confirm-spend --ledger ...
"""
from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _common as C  # noqa: E402

MODELS = {"nb2": ("gemini-3.1-flash-image", 0.067), "nbpro": ("gemini-3-pro-image", 0.134)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompt", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--model", choices=list(MODELS), default="nb2")
    ap.add_argument("--aspect", default="16:9"); ap.add_argument("--ref", nargs="*", help="inline reference image(s)")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--confirm-spend", action="store_true"); ap.add_argument("--ledger")
    a = ap.parse_args(argv)
    model, price = MODELS[a.model]
    parts = [{"text": a.prompt}]
    for p in a.ref or []:
        b, mime = C.b64file(p); parts.append({"inlineData": {"mimeType": mime, "data": b}})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": a.aspect}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    print("endpoint:", url); print("parts:", [p if "text" in p else "<inlineData>" for p in parts], "generationConfig:", body["generationConfig"])
    ledger = C.spend_guard(a, model, 1, "images", price + 0.0011 * len(a.ref or []), "nano_banana_still")
    st, reply = C.http_json("POST", url, {"x-goog-api-key": C.key("GOOGLE_API_KEY")}, body)
    rid = reply.get("responseId") if isinstance(reply, dict) else None
    if st != 200:
        C.settle(ledger, rid, f"http_{st}", str(reply)); sys.exit(f"HTTP {st}: {C.scrub(str(reply))[:400]}")
    cands = reply.get("candidates") or []
    if not cands:
        C.settle(ledger, rid, "refusal", str(reply.get("promptFeedback"))); sys.exit(f"blocked: {reply.get('promptFeedback')}")
    c0 = cands[0]
    if c0.get("finishReason") in ("SAFETY", "BLOCKLIST", "PROHIBITED_CONTENT", "IMAGE_SAFETY"):
        C.settle(ledger, rid, "refusal", c0.get("finishReason")); sys.exit(f"refused: {c0.get('finishReason')}")
    for part in (c0.get("content") or {}).get("parts") or []:
        blob = part.get("inlineData") or part.get("inline_data")
        if blob and blob.get("data"):
            C.save(a.out, base64.b64decode(blob["data"])); C.settle(ledger, rid, "ok", blob.get("mimeType", "")); return
    C.settle(ledger, rid, "no_image", str(reply)[:300]); sys.exit("no image part in the reply")


if __name__ == "__main__":
    main()
