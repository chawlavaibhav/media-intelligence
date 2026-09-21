# Tool provenance — AGY-2026-09-21-MOKOBARA-ODYSSEY-001

Sources are read-only; copies live here. Nothing upstream was edited.

| Here | Source (path @ commit) | sha256 of source | Change made here |
|---|---|---|---|
| `tools/_common.py` | `media-intelligence-rentok-cq` `experiments/RENTOK-CREATIVE-QUALITY-001/treatments/tools/_common.py` @ `41d97c6` | `7971b67010a2425de762515db1120b6b9c893fda2b2c039022dcd2a0dbbae1c5` | header block only |
| `tools/dispatch.py` | same dir `dispatch.py` @ `41d97c6` | `64e5248b3e9be027f46f08fdd9b0f283178d201cdfa698c1ba7c48ec8006ce2d` | job paths/cap; treatment caps removed (one job ledger); `veo-3.1-fast` t2v added (request shape = i2v minus `image`, per `eval/harness-v2/adapters/vertex_veo.py` build_request); `lyria` recipe copied from Lane A `tools/dispatch.py` @ `0405feb0` lines 206–231; prompt guard word list = this job's IP/claim list (Stage 2); copy-deck path = this job's `copy-deck.json` |
| `tools/qa_checks.py` | `media-intelligence-rentok-v2` `agency/jobs/AGY-2026-09-21-RENTOK-GAME-V2-001/tools/qa_checks.py` @ `ffefe44b` | `8effc837ed6cfb30818c601df3c795d7e56ee85d0f7724f6df844b7b41fe54cf` | rewritten for a generated-footage film (container/duration/elst/faststart/loudness/atom-walk logic kept; the game-specific layout checks dropped; frame text hygiene + keyframes added) |
| loudness/mux flags | same job `tools/assemble_v2.py` @ `ffefe44b` | `580333d184aafd1d66df88058bb5c50242170b008ae92a88b88877aece9ba976` | two-pass loudnorm I=−14 TP=−4 + alimiter, `-use_editlist 0`, `+faststart+negative_cts_offsets` carried into `tools/assemble.py` |
| safe box, spec | Lane A `stages/02-STRUCTURE.md` @ `0405feb0` | — | numbers carried (Stage 2) |
