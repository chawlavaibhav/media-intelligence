#!/usr/bin/env python3
"""fal queue: submit one job, poll, download the artifact. Generic over any fal endpoint id.

PROVENANCE: lifecycle and URL-trust rules copied from eval/harness-v2/adapters/fal_queue.py (submit POST
https://queue.fal.run/<endpoint> -> {request_id,status_url,response_url}; GET status_url until COMPLETED, HTTP 200/202
both pollable; GET response_url -> images[0].url | video.url | audio.url; download from *.fal.media / *.fal.run only).
Body shapes below are the ROUTE_PINS the Lab actually sent (kling-v3-pro-i2v, minimax-h3-max-i2v, wan-3.0-prime-i2v,
kling-v3-pro t2v, flux-2-pro) plus TWO UNTESTED variants for this pilot: Kling i2v with generate_audio=true (English
presenter speech) and Kling i2v with `elements` (identity reference). Those two fields exist in the pinned OpenAPI
(eval/harness-v2/schemas/fal/fal-ai_kling-video_v3_pro_image-to-video.json) but were never dispatched by the Lab.
NEVER RUN. Balance check is free: `python3 fal_queue.py balance`.

USAGE
  source ~/.mi-keys
  python3 fal_queue.py balance
  python3 fal_queue.py kling-i2v --image still.png --prompt "..." --duration 8 --audio --out take1.mp4 --dry-run
  python3 fal_queue.py kling-i2v --image still.png --prompt "..." --duration 8 --audio --out take1.mp4 --confirm-spend --ledger ../../gen/ledger.jsonl
  python3 fal_queue.py h3-i2v   --image plate.png --prompt "..." --duration 6 --out b1.mp4 ...
  python3 fal_queue.py wan-i2v  --image plate.png --prompt "..." --duration 6 --aspect 16:9 --out b2.mp4 ...
  python3 fal_queue.py kling-t2v --prompt "..." --duration 15 --aspect 16:9 [--audio] --out story.mp4 ...
  python3 fal_queue.py flux-plate --prompt "..." --aspect 16:9 --out plate.png ...
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _common as C  # noqa: E402

QUEUE = "https://queue.fal.run"
HOST_RE = re.compile(r"^https://([A-Za-z0-9.-]+)(?::\d+)?(?:[/?#]|$)")

# pinned prices, USD (eval/empirical-planning/price-pins-2026-09/PIN-INDEX.yaml, fetched 2026-09-04; fal quotes)
PRICES = {
    "fal-ai/kling-video/v3/pro/image-to-video": {"silent": 0.112, "audio": 0.168, "unit": "seconds"},
    "fal-ai/kling-video/v3/pro/text-to-video":  {"silent": 0.112, "audio": 0.168, "unit": "seconds"},
    "minimax/h3-max/image-to-video":            {"silent": 0.08, "audio": 0.08, "unit": "seconds"},   # 768P; 480P = 0.05
    "alibaba/wan-3.0-prime/image-to-video":     {"silent": 0.14, "audio": 0.14, "unit": "seconds"},   # 720p; 1080p = 0.28
    "fal-ai/flux-2-pro":                        {"silent": 0.03, "audio": 0.03, "unit": "images"},    # first megapixel
}
SIZE_16_9 = {"width": 1280, "height": 720}        # SIZE_A policy, harness fal_queue.py: <= 1 MP keeps the 0.03 price


def trusted(url: str, kind: str) -> bool:
    m = HOST_RE.match(url or "")
    if not m:
        return False
    h = m.group(1).lower()
    return h == "queue.fal.run" if kind == "queue" else (h == "queue.fal.run" or h.endswith(".fal.media") or h.endswith(".fal.run"))


def balance() -> None:
    """Free read. Observed 2026-09-14: HTTP 200, USD 3.3515175 (the dashboard's user_balance endpoint)."""
    st, txt, _ = C.http("GET", "https://rest.alpha.fal.ai/billing/user_balance", {"Authorization": f"Key {C.key('FAL_KEY')}"})
    print("fal balance HTTP", st, C.scrub(txt.decode("utf-8", "replace"))[:200])


def body_for(args) -> tuple[str, dict, float, float]:
    """(endpoint_id, body, quantity, unit_price)"""
    if args.cmd == "kling-i2v":
        ep = "fal-ai/kling-video/v3/pro/image-to-video"
        body = {"prompt": args.prompt, "start_image_url": C.data_uri(args.image), "duration": str(args.duration),
                "generate_audio": bool(args.audio)}
        if args.elements:                                         # UNTESTED: identity reference set(s)
            body["elements"] = [{"frontal_image_url": C.data_uri(args.elements[0]),
                                 "reference_image_urls": [C.data_uri(p) for p in args.elements[1:]]}]
        if args.negative:
            body["negative_prompt"] = args.negative
        price = PRICES[ep]["audio" if args.audio else "silent"]; qty = args.duration
    elif args.cmd == "kling-t2v":
        ep = "fal-ai/kling-video/v3/pro/text-to-video"
        body = {"prompt": args.prompt, "aspect_ratio": args.aspect, "duration": str(args.duration), "generate_audio": bool(args.audio)}
        price = PRICES[ep]["audio" if args.audio else "silent"]; qty = args.duration
    elif args.cmd == "h3-i2v":
        ep = "minimax/h3-max/image-to-video"
        body = {"prompt": args.prompt, "prompt_expansion_mode": "balanced", "image_url": C.data_uri(args.image),
                "resolution": "768P", "duration": int(args.duration)}       # 5..15; aspect follows the image
        price = PRICES[ep]["silent"]; qty = args.duration
    elif args.cmd == "wan-i2v":
        ep = "alibaba/wan-3.0-prime/image-to-video"
        body = {"prompt": args.prompt, "start_image_url": C.data_uri(args.image), "resolution": "720p",
                "duration": int(args.duration), "audio": bool(args.audio), "aspect_ratio": args.aspect}  # send the aspect, never 'adaptive'
        price = PRICES[ep]["silent"]; qty = args.duration
    elif args.cmd == "flux-plate":
        ep = "fal-ai/flux-2-pro"
        body = {"prompt": args.prompt, "image_size": SIZE_16_9 if args.aspect == "16:9" else {"width": 1024, "height": 1024}}
        price = PRICES[ep]["silent"]; qty = 1
    else:
        sys.exit(f"unknown command {args.cmd}")
    return ep, body, qty, price


def run(args) -> None:
    ep, body, qty, price = body_for(args)
    shown = {k: (v if not (isinstance(v, str) and v.startswith("data:")) else "<data-uri>") for k, v in body.items()}
    print("endpoint:", f"{QUEUE}/{ep}"); print("body:", shown)
    ledger = C.spend_guard(args, ep, qty, PRICES[ep]["unit"], price, "fal_queue")
    hdr = {"Authorization": f"Key {C.key('FAL_KEY')}"}
    st, reply = C.http_json("POST", f"{QUEUE}/{ep}", hdr, body)
    if st != 200:
        C.settle(ledger, None, f"submit_http_{st}", str(reply)); sys.exit(f"submit failed HTTP {st}: {C.scrub(str(reply))[:300]}")
    rid, surl, rurl = reply.get("request_id"), reply.get("status_url"), reply.get("response_url")
    if not (rid and trusted(surl, "queue") and trusted(rurl, "queue")):
        C.settle(ledger, rid, "untrusted_or_malformed", str(reply)); sys.exit("queue reply malformed or off-host; key not sent further")
    print("request_id:", rid)

    def check():
        code, st_ = C.http_json("GET", surl, hdr)
        s = st_.get("status") if isinstance(st_, dict) else None
        if code in (200, 202) and s in ("IN_QUEUE", "IN_PROGRESS"):
            return False, st_
        return True, (st_ if s == "COMPLETED" else {"$error": code, "reply": st_})

    fin = C.poll(check, interval_s=5.0, max_checks=120)
    if fin.get("$timeout") or fin.get("$error"):
        C.settle(ledger, rid, "poll_failed_or_timeout", str(fin)); sys.exit(f"poll ended without COMPLETED: {C.scrub(str(fin))[:300]}")
    code, out = C.http_json("GET", rurl, hdr)
    if code != 200 or out.get("error") or out.get("detail"):
        C.settle(ledger, rid, f"result_http_{code}", str(out)); sys.exit(f"result read failed: {C.scrub(str(out))[:300]}")
    url = None
    for k in ("images",):
        v = out.get(k)
        if isinstance(v, list) and v and v[0].get("url"):
            url = v[0]["url"]
    for k in ("video", "audio", "image"):
        v = out.get(k)
        if isinstance(v, dict) and v.get("url"):
            url = url or v["url"]
    if not url or not trusted(url, "download"):
        C.settle(ledger, rid, "no_or_untrusted_artifact", str(url)); sys.exit(f"no trusted artifact url: {url}")
    st, data, ct = C.http("GET", url, {})
    if st != 200:
        C.settle(ledger, rid, f"download_http_{st}"); sys.exit(f"download failed {st}")
    C.save(args.out, data); C.settle(ledger, rid, "ok", f"{ct} {len(data)} bytes -> {args.out}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["balance", "kling-i2v", "kling-t2v", "h3-i2v", "wan-i2v", "flux-plate"])
    ap.add_argument("--prompt"); ap.add_argument("--image"); ap.add_argument("--out")
    ap.add_argument("--duration", type=int, default=6); ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--audio", action="store_true"); ap.add_argument("--negative")
    ap.add_argument("--elements", nargs="*", help="UNTESTED Kling identity reference: frontal image then extra reference images")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--confirm-spend", action="store_true"); ap.add_argument("--ledger")
    a = ap.parse_args(argv)
    if a.cmd == "balance":
        return balance()
    if not a.out or not a.prompt:
        sys.exit("--prompt and --out are required")
    run(a)


if __name__ == "__main__":
    main()
