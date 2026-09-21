# Stage 4 — Production plan (gate: riskiest element first; every route priced live; reuse records before use)

Job `AGY-2026-09-21-RENTOK-GAME-V2-001`. Prices: live PriceBook quotes read 2026-09-21 by `tools/dispatch.py quotes` — `nano-banana-2` USD 0.067 per image, `lyria` USD 0.06 per clip, both pool `credits`. Cap **USD 3.00** (`input/SPEND-AUTHORISATION.md`), written into `tools/dispatch.py` (`CAP_USD = 3.0`, `CAP_STATED_BY` = the authorisation). Pool: Google credits, human-attested 2026-09-20 (Lane A `spend.pool_readings`; the authorisation says the attestation stands; not machine-readable).

## 4.0 Approach

The Video-4 way: the whole 30 s is code-rendered by `tools/render_v2.py` from BOARD-v2 (Stage 3). Generative models supply only textless stills — and this job needs exactly **one** new still: an 8-pose sheet for the poses the direction calls for that no accepted asset carries. Everything else is reused from accepted work with a reuse record below. No video model (Stage 1 V2-D3).

## 4.1 Risk order

| Rank | Item | Risk | Test |
|---|---|---|---|
| 1 | V2-S1 pose sheet (8 poses, 2×4, 16:9) | identity drift vs the two accepted sheets (a third text-prompted sheet of the same man); lettering (RO-04); pixel density differing from the base sheet (C sheet was ≈ 60 % of the base density — OBSERVED in CQ-001) | one draw → `tools/inspect_sheet.py` consistency card (keyable ≥ 98 %, 8 cells, red book + gold keys per cell, review strip against Lane A idle + C brace, judged by eye) → freeze by sha256 → then the final render; one repair draw allowed |
| 2 | Feel across 30 s (pacing of five pushes) | a pipeline risk, not generative | the USD-0 animatic v2 (Stage 3 Part E) — judged and passed before this spend |
| 3 | Audio per beat (ducks, low-pass, semitone lift over a 30-s bed) | processing artefacts at the concat point | measured on the encoded file (loudness, true peak), ear check |

## 4.2 Assets — reuse records (DESIGN_REUSE_PROVENANCE) and the one new draw

| id | Asset | Method | Reuse record | Price | Draws |
|---|---|---|---|---|---|
| R1 | PG-owner base sheet: `gen/assets/owner_{idle,runA,runB,jump}.png` (from `gen/raw/A1_owner_sheet_att001.png`) | reuse | `source_asset`: Lane A att-001 @ sha256 `f1706052…` (PROVENANCE.md) · `source_verdict`: accepted (film ACCEPT 2026-09-20; checker PASS on all five sheet criteria, CHECK-STAGE-5 §4) · `reuse_status`: **accepted_in_context** (same character, same film, same pixel style; the context here is the same story at 300 px instead of 260 px → `fresh_qa_required: true` — the DET suite runs on the new file) | 0 | 0 |
| R2 | Obstacles 1–5: `gen/assets/obst_1..5.png` | reuse | Lane A att-002..006 · accepted · **accepted_in_context** (same obstacles, same plate; sizes ×1.0–1.15 by code; fresh QA on the film) | 0 | 0 |
| R3 | Plate: `gen/assets/plate.png` | reuse | Lane A att-007 · accepted · **accepted_in_context**; the plate is fitted 1080×1920 and the code lane (Lane A D-7) fills the frame to the bottom at every zoom (the 1.6× crop shows world y 256–1456: plate + lane; OBSERVED on the animatic) → **no new plate needed** (the optional ≤ 1 draw is not spent) | 0 | 0 |
| R4 | C expression sheet: `gen/assets/c_{hurt,cornered,cornered_up,catch,powered,windup,fire,brace}.png` (from `gen/raw/C-A1_pose_sheet_att-006.png`) | reuse | CQ-001 Treatment C att-006 @ sha256 `0abda641…` · `source_verdict`: accepted in the blind evaluation as part of clip 4 (customer rank 2 of 4, "better pixelated"; evaluator 25/40; "not accepted as-is" for the CLIP, the sheet itself passed identity) · `reuse_status`: **accepted_in_context** (same man, same film context) · pixel density: cells are ≈ 60 % of the base sheet's density; at 300 px (scale 300/344 = 0.87 vs the base 300/561 = 0.53) the C poses' pixels are ≈ 1.6× coarser than the run poses — visible on a large screen at pose swaps, INFERRED not visible at phone size (C's finding); accepted, recorded as an LJ item | 0 | 0 |
| **N1** | **V2-S1 pose sheet — 8 poses no accepted asset carries**: (1) look-back, (2) reach, (3) trip (sprawled), (4) cover (arms over head), (5) running-fire, (6) cheer, (7) dazed, (8) land | AI still → `inspect_sheet.py` cut-out | new; prompt `gen/prompts/V2-S1_pose_sheet.txt` (the C prompt's proven structure and style block; 377 words; Canon pre-gate PASS `V2-S1_pose_sheet.gate.json`; prompt guard PASS) | 0.067 | 1 (+1 repair) |
| N2 | second sheet | not needed — the direction's pose list is covered by R1 + R4 + N1 (18 + 2 run + jump poses); reserved only if N1's repair still misses a pose that matters | 0.067 | 0 (reserve) |
| R5 | Music bed: `gen/raw/A10_music_att-008.wav` (Lyria, ≈ 32.8 s) | reuse | Lane A att-008 · accepted · **accepted_in_context** — **decision: no new Lyria draw.** The per-beat audio (ducks at each hit, cut for the hit-stops, low-pass + −7 dB from the swarm hit to the flash, −24 dB for 0.3 s before it, one semitone up after) is PROCESSING of the bed, not a different tempo; the C clip did exactly this on the same bed and was accepted; a second draw would be USD 0.06 for an unheard bed with no evidence it fits better | 0 | 0 |
| R6 | Wordmark raster `source/rentok-brand/rentok-new-logo.webp` @ `1ff7dcf5…` | reuse | the brand's own file (Stage 2d) | 0 | 0 |
| C1 | SFX (`tools/sfx_v2.py`: Lane A cues + C cues at every board audio entry) · assembly (`tools/assemble_v2.py`: C's bed processing generalised to 30 s + Lane A loudnorm/mux) · render · QA | code | — | 0 | — |

Obstacle "after" states and props: none drawn — every payoff is code (debris, paper sheets, coin fountain, ledger tag + tick, dashboard card, red→green flip) as the Lane A board specified and C's primitives execute.

## 4.3 Expected spend vs the cap

| Line | Draws | USD |
|---|---|---|
| N1 sheet | 1 × 0.067 | 0.067 |
| N1 repair (if the card fails) | 1 × 0.067 | 0.067 |
| N2 second sheet (reserve, only on a second miss) | 1 × 0.067 | 0.067 |
| Music (reuse) | 0 | 0 |
| **Expected** | 1 call | **0.067** |
| **Planned ceiling** | 3 calls | **0.201** (6.7 % of USD 3.00) |

0 hidden retries; a provider refusal/outage is `infrastructure_transient`, counted at full price, re-sent only as a new counted attempt inside the ceiling.

## 4.4 Consistency card for N1 (the acceptance test before any dependent work)

1. Border keyable ≥ 98 % (`key_out`) and exactly 8 cells in 2 rows.
2. Same man in all 8: face, spectacles, hair, checked shirt, dark trousers, sandals — judged by eye on the review strip beside the Lane A idle and the C brace.
3. Keys + red book present in every cell except the trip (book skidding ahead, still in the cell) — red-pixel and gold-pixel counts per cell (≥ 300 red = book present, as calibrated on the C sheet: absent cells score < 200).
4. No lettering anywhere (eye; the phone is not in this sheet).
5. Not a Nintendo cue (Stage 2c table).
6. Pixel density vs the base sheet recorded (cell height of the standing 'dazed' pose).
Verdict → freeze (sha256 in JOB.yaml `plan.micro_qualifications`) → `--poses sheet` final render.

## 4.5 Order of work

1. USD 0: animatic v2 — done (Stage 3 Part E), 26 gates PASS.
2. USD 0: pre-dispatch checks — Canon pre-gate PASS; prompt guard PASS; cap written; pool attested; consent n-a.
3. Paid: N1 → consistency card → freeze.
4. USD 0: SFX stem, final render (`--poses sheet`), assembly, DET suite, contact sheet, keyframes, one bounded repair round on the producer's own findings.

Not a verdict. Written by the producer session.
