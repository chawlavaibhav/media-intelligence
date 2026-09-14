#!/usr/bin/env python3
"""Google video: Veo 3.1 on Vertex (t2v / i2v / ref2v / extend) and Gemini Omni 1.1 Flash (Vertex or Gemini API).

PROVENANCE
  Veo body + operation lifecycle: copied from eval/harness-v2/adapters/vertex_veo.py
      POST {regional}/publishers/google/models/<id>:predictLongRunning  {"instances":[...],"parameters":{...}}
      POST {regional}/.../<id>:fetchPredictOperation {"operationName": name}  until done -> response.videos[0].bytesBase64Encoded
      durations 4|6|8 (extend adds a fixed 7 s: 8+7=15); aspect 16:9|9:16; resolution 720p|1080p; generateAudio bool.
  Omni on Vertex (the surface the Lab actually paid on, 8/8 + 2/2 + 2/2): eval/harness-v2/adapters/vertex_omni.py
      POST https://aiplatform.googleapis.com/v1beta1/projects/<p>/locations/global/interactions
      model gemini-omni-1.1-flash-preview; response_format is a LIST on Vertex.
  Omni on the Gemini Developer API (key GOOGLE_API_KEY; surface NEVER paid on for video - C-13 'untested pricing
      surface'): eval/harness-v2/adapters/gemini_api_omni.py
      POST https://generativelanguage.googleapis.com/v1beta/interactions   header x-goog-api-key
      model gemini-omni-1.1-flash; response_format is a DICT on this surface. Synchronous: one POST is the trial.
  Token for Vertex: gcloud with the SA file inside a throw-away config (transports.py). Project vertexaiproject-507518.
  UNTESTED COMBINATIONS this pilot needs: Veo i2v WITH generateAudio=true (presenter speaks from an accepted still);
  Veo ref2v WITH generateAudio=true on a person; Omni image_to_video. The Lab never sent any of these.
NEVER RUN.

USAGE (source ~/.mi-keys first for the Gemini API surface)
  python3 google_video.py veo --mode i2v --image portrait.png --prompt "..." --duration 8 --resolution 1080p --audio --out take1.mp4 --dry-run
  python3 google_video.py veo --mode ref2v --refs a.png b.png c.png --prompt "..." --duration 8 --audio --out t.mp4 ...
  python3 google_video.py veo --mode extend --prompt "..." --out t15.mp4 ...          # 8 s generate + 7 s extend, one recipe run
  python3 google_video.py veo --mode t2v --model veo-3.1-generate-001 --prompt "..." --duration 6 --out hero.mp4 ...
  python3 google_video.py omni --surface vertex --prompt "..." --duration 10 --resolution 720p --out s.mp4 ...
  python3 google_video.py omni --surface gemini_api --image plate.png --prompt "..." --duration 6 --out b.mp4 ...
"""
from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _common as C  # noqa: E402

PROJECT = "vertexaiproject-507518"; REGION = "us-central1"
REGIONAL = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/publishers/google/models"
VERTEX_INTERACTIONS = f"https://aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/global/interactions"
GEMINI_INTERACTIONS = "https://generativelanguage.googleapis.com/v1beta/interactions"

# USD per second, pinned (vertex-shared/vertex-generative-ai-pricing.html 2026-09-04; gemini-api-judge/gemini-api-pricing.html 2026-09-09)
VEO_PRICE = {"veo-3.1-fast-generate-001": {"720p": 0.10, "1080p": 0.12},
             "veo-3.1-generate-001":      {"720p": 0.40, "1080p": 0.40},
             "veo-3.1-lite-generate-001": {"720p": 0.05, "1080p": 0.08}}
OMNI_PRICE_720P = 0.10136       # 17.50 USD/1M tokens x 5,792 tokens/s; 1080p token rate NOT pinned -> priced as unknown


def veo(args):
    model = args.model
    if args.mode == "extend":
        dur = 8
    else:
        dur = args.duration
        if dur not in (4, 6, 8):
            sys.exit("Veo durations are 4, 6 or 8 s (pinned t2v guide); use --mode extend for 15 s")
    if args.mode == "ref2v" and dur != 8:
        sys.exit("Vertex ref2v accepted only 8 s in the Lab (6 s refused; DAY-2 summary)")
    inst = {"prompt": args.prompt}
    if args.mode in ("i2v", "extend") and args.image:
        b, mime = C.b64file(args.image); inst["image"] = {"bytesBase64Encoded": b, "mimeType": mime}
    elif args.mode == "ref2v":
        if not args.refs or len(args.refs) > 3:
            sys.exit("ref2v takes 1-3 --refs (asset references)")
        inst["referenceImages"] = [{"image": dict(zip(("bytesBase64Encoded", "mimeType"), C.b64file(p))), "referenceType": "asset"} for p in args.refs]
    params = {"sampleCount": 1, "aspectRatio": args.aspect, "resolution": args.resolution, "durationSeconds": dur, "generateAudio": bool(args.audio)}
    body = {"instances": [inst], "parameters": params}
    billed = ((0 if args.from_video else 8) + 7 * len(args.extend_prompt or [args.prompt])) if args.mode == "extend" else dur
    price = VEO_PRICE[model][args.resolution]
    shown = {"instances": [{k: (v if k == "prompt" else "<bytes>") for k, v in inst.items()}], "parameters": params}
    print("endpoint:", f"{REGIONAL}/{model}:predictLongRunning"); print("body:", shown)
    ledger = C.spend_guard(args, f"{model}/{args.mode}/{args.resolution}", billed, "seconds", price, "google_video.veo")
    tok = C.gcloud_sa_token(); hdr = {"Authorization": f"Bearer {tok}"}
    if args.mode == "extend" and args.from_video:
        data, mime, name = Path(args.from_video).read_bytes(), "video/mp4", f"from:{args.from_video}"
    else:
        data, mime, name = _veo_op(f"{REGIONAL}/{model}", hdr, body, ledger)
    if args.mode == "extend":
        prompts = args.extend_prompt or [args.prompt]
        for k, ep in enumerate(prompts, start=1):
            ext = {"instances": [{"prompt": ep, "video": {"bytesBase64Encoded": base64.b64encode(data).decode(), "mimeType": mime}}],
                   "parameters": {kk: v for kk, v in params.items() if kk != "durationSeconds"}}
            C.save(str(args.out).replace(".mp4", f".call{k}.mp4"), data)
            data, mime, name2 = _veo_op(f"{REGIONAL}/{model}", hdr, ext, ledger)
            name = f"{name} + {name2}"
    C.save(args.out, data); C.settle(ledger, name, "ok", f"{mime} -> {args.out}")


def _veo_op(url_base, hdr, body, ledger):
    st, reply = C.http_json("POST", f"{url_base}:predictLongRunning", hdr, body)
    if st != 200:
        C.settle(ledger, None, f"submit_http_{st}", str(reply)); sys.exit(f"Veo submit HTTP {st}: {C.scrub(str(reply))[:300]}")
    name = reply.get("name"); print("operation:", name)

    def check():
        code, op = C.http_json("POST", f"{url_base}:fetchPredictOperation", hdr, {"operationName": name})
        if code != 200:
            return True, {"$error": code, "reply": op}
        return bool(op.get("done")), op

    op = C.poll(check, 5.0, 120)
    if op.get("$error") or op.get("$timeout") or op.get("error"):
        C.settle(ledger, name, "operation_failed", str(op)); sys.exit(f"Veo operation failed: {C.scrub(str(op))[:300]}")
    resp = op.get("response") or {}
    vids = resp.get("videos") or []
    if not vids:
        C.settle(ledger, name, "refusal_or_empty", str(resp.get("raiMediaFilteredReasons"))); sys.exit(f"no video (raiMediaFilteredCount={resp.get('raiMediaFilteredCount')}): {resp.get('raiMediaFilteredReasons')}")
    v0 = vids[0]
    if not v0.get("bytesBase64Encoded"):
        C.settle(ledger, name, "not_inline", str(v0.get("gcsUri"))); sys.exit("video not inline")
    return base64.b64decode(v0["bytesBase64Encoded"]), v0.get("mimeType") or "video/mp4", name


def omni(args):
    if not (3 <= args.duration <= 10):
        sys.exit("Omni clips are 3-10 s")
    inputs = [{"type": "text", "text": args.prompt}]
    if args.image:
        b, mime = C.b64file(args.image); inputs.append({"type": "image", "data": b, "mime_type": mime})
    fmt = {"type": "video", "aspect_ratio": args.aspect, "resolution": args.resolution, "duration": f"{args.duration}s"}
    task = "image_to_video" if args.image else "text_to_video"
    if args.surface == "vertex":
        url, model, rf = VERTEX_INTERACTIONS, "gemini-omni-1.1-flash-preview", [fmt]
    else:
        url, model, rf = GEMINI_INTERACTIONS, "gemini-omni-1.1-flash", fmt
    body = {"model": model, "input": inputs, "response_format": rf, "generation_config": {"video_config": {"task": task}}}
    price = OMNI_PRICE_720P if args.resolution == "720p" else float("nan")
    if args.resolution != "720p":
        print("WARNING: only the 720p token rate is pinned; 1080p cost is NOT pinned (priced as NaN, guard will still require confirm)")
    print("endpoint:", url); print("body:", {**body, "input": [i if i["type"] == "text" else {"type": "image", "data": "<b64>"} for i in inputs]})
    ledger = C.spend_guard(args, f"omni/{args.surface}/{task}/{args.resolution}", args.duration, "seconds", price if price == price else 0.0, "google_video.omni")
    if args.surface == "vertex":
        hdr = {"Authorization": f"Bearer {C.gcloud_sa_token()}"}
    else:
        hdr = {"x-goog-api-key": C.key("GOOGLE_API_KEY")}
    st, reply = C.http_json("POST", url, hdr, body, timeout=600)
    iid = reply.get("id") if isinstance(reply, dict) else None
    if st != 200 or reply.get("status") not in ("completed", None):
        C.settle(ledger, iid, f"http_{st}_{reply.get('status') if isinstance(reply, dict) else ''}", str(reply)); sys.exit(f"Omni failed HTTP {st}: {C.scrub(str(reply))[:400]}")
    for step in reply.get("steps") or []:
        if step.get("type") != "model_output":
            continue
        for c in step.get("content") or []:
            if c.get("type") == "video" and c.get("data"):
                C.save(args.out, base64.b64decode(c["data"])); C.settle(ledger, iid, "ok", str(reply.get("usage"))); return
    C.settle(ledger, iid, "no_video", str(reply)[:300]); sys.exit("completed interaction carried no video")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("family", choices=["veo", "omni"])
    ap.add_argument("--mode", choices=["t2v", "i2v", "ref2v", "extend"], default="t2v")
    ap.add_argument("--model", default="veo-3.1-fast-generate-001")
    ap.add_argument("--surface", choices=["vertex", "gemini_api"], default="vertex")
    ap.add_argument("--prompt", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--image"); ap.add_argument("--refs", nargs="*")
    ap.add_argument("--from-video", help="extend mode: skip the first generation and extend this existing clip")
    ap.add_argument("--extend-prompt", nargs="*", help="extend mode: one prompt per 7 s extension, in order (defaults to --prompt once)")
    ap.add_argument("--duration", type=int, default=8); ap.add_argument("--aspect", default="16:9"); ap.add_argument("--resolution", default="720p")
    ap.add_argument("--audio", action="store_true")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--confirm-spend", action="store_true"); ap.add_argument("--ledger")
    a = ap.parse_args(argv)
    (veo if a.family == "veo" else omni)(a)


if __name__ == "__main__":
    main()
