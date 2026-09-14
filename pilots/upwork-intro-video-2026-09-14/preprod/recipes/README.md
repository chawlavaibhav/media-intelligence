# preprod/recipes — runnable, NOT RUN (2026-09-14)

Written by the production-capability analyst for the Upwork intro film. No script in this folder has made a paid call.
Every paid recipe refuses to send unless BOTH `--confirm-spend` and `--ledger <file>` are passed, and writes a
reservation line to that ledger before the request leaves. **No spend record exists for this pilot**; get one signed
before the first `--confirm-spend` (`coordination/CONTROL-STATE.md` §6: "Any paid tranche needs explicit Controller
approval in writing, before dispatch").

Run everything with `/opt/homebrew/bin/python3` (3.14) after `source ~/.mi-keys` (never print a value). The recipes are
stdlib-only because `requests` and `PIL` are not installed for that interpreter (PIL exists only under `/usr/bin/python3`
3.9.6). Local tools verified present: ffmpeg 8.1.2 (libx264, aac, xfade, acrossfade, loudnorm, overlay, drawbox; **no
drawtext / subtitles / ass**), ffprobe, hb-view + hb-shape (HarfBuzz 14.2.1), gcloud.

| Recipe | Does | Provenance | Paid? |
|---|---|---|---|
| `_common.py` | key-by-name, scrubbing, bounded poll, gcloud SA token in a throw-away config, spend guard + ledger | key rules from `eval/harness-v2/adapters/base.py`, token source from `eval/harness-v2/transports.py`; rest fresh | no |
| `fal_queue.py` | fal queue submit → poll → download; `balance` (free); Kling i2v (+audio, +elements), Kling t2v, H3 Max i2v, Wan 3.0 Prime i2v, FLUX.2 Pro plate | lifecycle + trust rules from `eval/harness-v2/adapters/fal_queue.py`; bodies = the Lab's ROUTE_PINS; `generate_audio=true` and `elements` on Kling i2v are UNTESTED additions present in the pinned OpenAPI | yes (guarded) |
| `google_video.py` | Veo 3.1 on Vertex (t2v / i2v / ref2v / extend; generateAudio); Omni on Vertex or Gemini API (t2v / i2v) | `adapters/vertex_veo.py`, `adapters/vertex_omni.py`, `adapters/gemini_api_omni.py` | yes (guarded) |
| `nano_banana_still.py` | Nano Banana 2 / Pro still on the Gemini API, optional inline reference images | `adapters/vertex_gemini_image.py` body (shared by `gemini_api_image.py`) | yes (guarded) |
| `lyria_track.py` | Lyria 2 (lyria-002) 32.8 s WAV on Vertex | `adapters/vertex_lyria.py` | yes (guarded) |
| `sarvam_tts.py` | bulbul:v3 speech, en-IN / hi-IN | `adapters/sarvam_tts.py` | yes (guarded) |
| `overlay_text_video.py` | hb-view text → PNG; static or animated overlay onto every frame via ffmpeg `overlay` (+ solid panel) | hb-view call from `eval/battery/devanagari-exactness/devtext.py`; compositing fresh (the Lab's `composite.py` does the same blend in pure Python) | **no** — tested locally on a synthetic clip 2026-09-14 |
| `assemble.sh` | conform → trim → cut/xfade → text → 60 s music loop → mix (sidechain duck + loudnorm −14 LUFS) → 1080p24 H.264 master | audio stack shape from `eval/harness-v2/stack_audio.py`; export flags from `instruments/imageio.py`; rest fresh | **no** — every function tested on synthetic media 2026-09-14 |

Dry runs (`--dry-run`) print the exact endpoint and body and exit before any socket opens; use them to review request
shapes with the Creative Director before the spend record is signed.
