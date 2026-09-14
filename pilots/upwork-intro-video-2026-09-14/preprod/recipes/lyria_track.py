#!/usr/bin/env python3
"""Lyria 2 (lyria-002) music track on Vertex, us-central1. One call = one ~32.8 s WAV (48 kHz stereo; measured on the
Lab's 4 sealed tracks: 32.768 s each). USD 0.06 per track (Vertex pricing page pin, 2026-09-04). aud-music-lyria 4/4 accepted.

PROVENANCE: copied from eval/harness-v2/adapters/vertex_lyria.py.
  POST {regional}/publishers/google/models/lyria-002:predict  {"instances":[{"prompt": <en-US>, "negative_prompt"?}], "parameters":{"sample_count":1}}
  -> predictions[0].bytesBase64Encoded  (the live key; the pinned page says audioContent - both accepted)
  `seed` cannot be used with sample_count, so two calls with the same prompt are two DIFFERENT pieces.
  For a 60 s bed: generate ONE track, then loop it with an audio crossfade (see assemble.sh, 'music60'); a second
  generation as a B-section is the fallback when the loop seam is audible.
NEVER RUN.

USAGE
  python3 lyria_track.py --prompt "warm, understated acoustic guitar and soft piano, 90 bpm, no vocals, ..." --out music_A.wav --dry-run
  python3 lyria_track.py --prompt "..." --negative "vocals, drums, distortion" --out music_A.wav --confirm-spend --ledger ...
"""
from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _common as C  # noqa: E402

URL = "https://us-central1-aiplatform.googleapis.com/v1/projects/vertexaiproject-507518/locations/us-central1/publishers/google/models/lyria-002:predict"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompt", required=True); ap.add_argument("--negative"); ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--confirm-spend", action="store_true"); ap.add_argument("--ledger")
    a = ap.parse_args(argv)
    inst = {"prompt": a.prompt}
    if a.negative:
        inst["negative_prompt"] = a.negative
    body = {"instances": [inst], "parameters": {"sample_count": 1}}
    print("endpoint:", URL); print("body:", body)
    ledger = C.spend_guard(a, "lyria-002", 1, "tracks", 0.06, "lyria_track")
    st, reply = C.http_json("POST", URL, {"Authorization": f"Bearer {C.gcloud_sa_token()}"}, body, timeout=300)
    if st != 200:
        C.settle(ledger, None, f"http_{st}", str(reply)); sys.exit(f"HTTP {st}: {C.scrub(str(reply))[:400]}")
    preds = reply.get("predictions") or []
    p0 = preds[0] if preds else {}
    key = next((k for k in ("bytesBase64Encoded", "audioContent") if p0.get(k)), None)
    if not key:
        C.settle(ledger, None, "no_audio", str(sorted(p0.keys()))); sys.exit(f"no audio; prediction keys {sorted(p0.keys())}")
    C.save(a.out, base64.b64decode(p0[key])); C.settle(ledger, reply.get("deployedModelId"), "ok", f"key={key}")


if __name__ == "__main__":
    main()
