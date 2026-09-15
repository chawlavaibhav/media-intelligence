# EVIDENCE MAP — case UPWORK-INTRO-001

Raw media is **not** duplicated here. Every claim in this case points at a file on the raw pilot branch
`work/pilot-upwork-intro-video-v4` (directory `pilots/upwork-intro-video-2026-09-14/`), identified by path,
commit and sha256 (full for the films, 16-hex prefix for records). `production-learning/tools/check_case.py
--pilot-ref work/pilot-upwork-intro-video-v4` verifies that every `path @ commit` below resolves.
Inventory with classification: `coordination/audits/UPWORK-INTRO-PILOT-EVIDENCE-INVENTORY-2026-09-14.md`.

## Films

| Version | path @ commit | sha256 |
|---|---|---|
| V1 | `assembly/v1/upwork-intro-first-pass.mp4` @ `7629894` | `c073e9ab0cf67f5754be0fba6505483d375ea314353e4d691e31e468fda8f4bd` |
| V2 | `assembly/v2/upwork-intro-v2.mp4` @ `7b39aeb` | `bdd4566eee1b494e802b055a212e6026c664761dad243f43fa01eb37d34915d5` |
| V3 | `v3/assembly/v3/upwork-intro-v3.mp4` @ `70f687e` | `ea81264d4103faa346b8937b50da4f785d5351f08aefc1e9bceb8d5df0052e51` |
| V4 | `v4/assembly/v4/upwork-intro-v4.mp4` @ `11d3e59` | `09ed32c54d601f68bd31733dfc1749326d89c9e40a43ba89fc0e6a14d60a29fc` |
| **V4.1 (accepted)** | `v4/assembly/v4.1/upwork-intro-v4.1.mp4` @ `f6ca66f` | `d1a5edf8836936eb7e27cec4350f4cce6f21f1d966778f7241544a2ad07e008a` |

## Records (sha256 prefix)

| Claim in this case | path @ commit | sha256 |
|---|---|---|
| V1+V2 spend USD 8.082, 12 dispatches | `gen/LEDGER.jsonl` @ `7b39aeb` | `da7ac16a97e12155` |
| V1+V2 per-route table, pools | `gen/LEDGER-SUMMARY.md` @ `7b39aeb` | — |
| V3 spend USD 3.2836, 36 dispatches, 3 Lyria failures | `v3/gen/LEDGER.jsonl` @ `70f687e` | `39004445f97a0b0e` |
| V3 per-asset timings, verdicts, failure reasons | `v3/gen/ASSETS.jsonl` @ `70f687e` | `a129cacc7120544b` |
| V3 sample-order clock 1,612 s | `v3/gen/CLOCK.json` @ `70f687e` | `e922e75d257c6904` |
| V3 spend record (cap, pools, fal balance 3.2315) | `v3/plan/SPEND-RECORD-V3.md` @ `70f687e` | — |
| V4 spend USD 4.0276, 6 dispatches, 2 Veo UNAVAILABLE | `v4/gen/LEDGER.jsonl` @ `11d3e59` | `f8c1e4b81f59529a` |
| V4 per-asset timings, verdicts | `v4/gen/ASSETS.jsonl` @ `11d3e59` | `44477a6e9190408b` |
| V4 spend amendment + Addendum 1 (outage) + V4.1 USD 0 | `v4/plan/SPEND-AMENDMENT-V4.md` @ `f6ca66f` | — |
| Speaker micro-qualification scores 53/60 vs 45/60 | `v4/qa/speaker/SPEAKER-QUALIFICATION.md` @ `11d3e59` | `e437642c782fa3bb` |
| Omni transcript (inserted word) / Veo transcript (verbatim) | `v4/qa/speaker/omni-r1-transcript.json` @ `11d3e59`, `v4/qa/speaker/veo-r3-transcript.json` @ `11d3e59` | — |
| V4.1 layout gate (29 boxes inside safe area, radii [26]) | `v4/qa/layout-report.json` @ `f6ca66f` | `1c78e06da48f6b58` |
| V4.1 contrast gate (all pass, min 5.67:1) | `v4/qa/contrast-report.json` @ `f6ca66f` | `84009f2313a4bcb3` |
| V4.1 crop gate (23 placements, 0 unintended) | `v4/qa/crop-report.json` @ `f6ca66f` | `652631cf32919877` |
| V4.1 beat starts (ACCEPTED-TEMPLATE structure) | `v4/assembly/v4.1/timeline.json` @ `f6ca66f` | `57fdaaec36df2ec0` |
| V4 route plan / execution manifest | `v4/plan/ROUTE-PLAN-V4.yaml`, `v4/plan/EXECUTION-MANIFEST-V4.json` @ `11d3e59` | `b8b4b616d89ff144`, `852725b41044d263` |
| V3 asset reuse decisions for V4 | `v4/plan/V3-ASSET-INVENTORY.md` @ `11d3e59` | — |
| V4 gates as code (the source the runtime gates were ported from) | `v4/tools/design4.py`, `v4/tools/film4.py` @ `f6ca66f` | — |
| Accepted speaker clip / rejected Omni clip / accepted still | `v4/gen/speaker/veo-r3.mp4` @ `11d3e59`, `v4/gen/speaker/omni-r1.mp4` @ `11d3e59`, `v4/gen/speaker/still-r2.png` @ `11d3e59` | `72a16bd735372f33`, `1d6d6e5cd503e96c`, `e85e2ea171d43d93` |
| V1/V2 learning, V3 learning, V4/V4.1 learning | `learning/PRODUCTION-MAP-AND-LEARNING.md` @ `7629894`; `v3/learning/PRODUCT-LEARNING-V3.md` @ `70f687e`; `v4/learning/PRODUCT-LEARNING-V4.md` @ `f6ca66f` | — |
| Controller verdicts V1–V4.1 | **chat only** — `HUMAN-VERDICTS.yaml` in this case is the transcription | — |
| Session start/end times | Claude desktop session metadata (`local_40723378…`, `local_b73a9a32…`) — outside the repo | — |
