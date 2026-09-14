#!/usr/bin/env python3
"""Sarvam bulbul:v3 text-to-speech, direct REST. aud-tts-sarvam 6/6 accepted with speaker `aditya` (male), INR 3.00 per
1,000 characters (pinned 2026-09-04). Output: WAV 22.05 kHz mono (measured on the sealed files). ~1-2 s latency.

PROVENANCE: copied from eval/harness-v2/adapters/sarvam_tts.py.
  POST https://api.sarvam.ai/text-to-speech   header api-subscription-key
  {"text", "language_code": "en-IN" | "hi-IN", "speaker": <lowercase id>, "model": "bulbul:v3"}  -> {"request_id", "audios":[<b64 wav>]}
  <= 2500 characters per call (adapter limit). Indian-English voice-over: language_code en-IN. Speakers pinned in
  eval/empirical-planning/price-pins-2026-09/sarvam-bulbul-v3/SPEAKERS-PIN.yaml (shubh default, aditya, ritu, priya, ...).
  Key validity checked 2026-09-14 with an empty-body probe (HTTP 400 invalid_request_error = key accepted, nothing generated).
NEVER RUN for this pilot.

USAGE
  source ~/.mi-keys
  python3 sarvam_tts.py --text "Hi, I'm ..." --lang en-IN --speaker aditya --out vo_01.wav --dry-run
"""
from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _common as C  # noqa: E402

URL = "https://api.sarvam.ai/text-to-speech"
INR_PER_1000 = 3.00; INR_PER_USD = 95.4211      # repo display rate (COST-TABLE rules), display only


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--text", required=True); ap.add_argument("--lang", default="en-IN"); ap.add_argument("--speaker", default="aditya")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--confirm-spend", action="store_true"); ap.add_argument("--ledger")
    a = ap.parse_args(argv)
    if len(a.text) > 2500:
        sys.exit("bulbul:v3 accepts at most 2500 characters per call; split the script")
    body = {"text": a.text, "language_code": a.lang, "speaker": a.speaker, "model": "bulbul:v3"}
    print("endpoint:", URL); print("body:", body); print(f"INR {len(a.text) / 1000 * INR_PER_1000:.3f} for {len(a.text)} chars")
    ledger = C.spend_guard(a, "sarvam-bulbul-v3", len(a.text) / 1000, "kchars", INR_PER_1000 / INR_PER_USD, "sarvam_tts")
    st, reply = C.http_json("POST", URL, {"api-subscription-key": C.key("SARVAM_API_KEY")}, body, timeout=60)
    rid = reply.get("request_id") if isinstance(reply, dict) else None
    if st != 200:
        C.settle(ledger, rid, f"http_{st}", str(reply)); sys.exit(f"HTTP {st}: {C.scrub(str(reply))[:300]}")
    audios = reply.get("audios") or []
    if not audios:
        C.settle(ledger, rid, "no_audio"); sys.exit("no audio in reply")
    C.save(a.out, base64.b64decode(audios[0])); C.settle(ledger, rid, "ok")


if __name__ == "__main__":
    main()
