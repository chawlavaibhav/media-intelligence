# Ledger summary — RENTOK-CREATIVE-QUALITY-001 Phase 2 (Treatments B, C, D)

Written 2026-09-21 from `treatments/LEDGER.jsonl` (reservation-before-request, settle-after) and `treatments/ATTEMPTS.jsonl` (one line per attempt). Cap USD 6.00 (`SPEND-AUTHORISATION.md`, human Controller). Pool: Google Vertex/Gemini credits, `pool_readings: attested_by_human` (2026-09-20T18:44Z; not machine-readable). Every reservation is an upper bound at pinned prices; vendor statements unreconciled.

| Attempt | Treatment | Asset | Route (cell · status · use · accepts) | Surface | USD reserved | Status | Verdict |
|---|---|---|---|---|---|---|---|
| att-001 | B | B-A1_owner_sheet | nano-banana-2 (IMG-CORE · clean_observed · True · 7/8) | gemini_api | 0.067 | ok | accepted |
| att-002 | B | B-A1_owner_sheet | nano-banana-2 (IMG-CORE · clean_observed · True · 7/8) | gemini_api | 0.067 | ok | not_selected |
| att-003 | B | B-A7_plate | nano-banana-2 (IMG-CORE · clean_observed · True · 7/8) | gemini_api | 0.067 | ok | accepted |
| att-004 | B | B-A6_swarm | nano-banana-2 (IMG-CORE · clean_observed · True · 7/8) | gemini_api | 0.067 | ok | accepted |
| att-005 | B | B-A2_wall | nano-banana-2 (IMG-CORE · clean_observed · True · 7/8) | gemini_api | 0.067 | ok | accepted |
| att-006 | C | C-A1_pose_sheet | nano-banana-2 (IMG-CORE · clean_observed · True · 7/8) | gemini_api | 0.067 | ok | accepted |
| att-007 | D | D1-microqual | veo-3.1-fast-i2v (VID-I2V · clean_observed · True · 5/8) | vertex | 0.800 | ok | not_selected |
| att-008 | D | D1-take2 | veo-3.1-fast-i2v (VID-I2V · clean_observed · True · 5/8) | vertex | 0.800 | ok | not_selected |
| att-009 | D | D1-take3 | veo-3.1-fast-i2v (VID-I2V · clean_observed · True · 5/8) | vertex | 0.800 | ok | accepted |

## Totals

| Treatment | Attempts | ok | failed / refused | USD reserved | Planned max | Unspent |
|---|---|---|---|---|---|---|
| B | 5 | 5 | 0 | 0.335 | 0.402 | 0.067 |
| C | 1 | 1 | 0 | 0.067 | 0.335 | 0.268 |
| D | 3 | 3 | 0 | 2.400 | 4.811 | 2.411 |
| **All** | **9** | **9** | **0** | **2.802** | 5.548 | — |

**Experiment: USD 2.802 reserved of the USD 6.00 cap (46.7 %); remaining USD 3.198.** 9 paid calls, 9 ok, 0 failed, 0 refused, 0 infrastructure re-sends, 0 hidden retries. Ledger lines: 9 reservations, 9 settlements (every reservation settled).

Not spent: B's second plate-or-obstacle repair (0.067); C's sheet repair (0.067), optional second plate (0.067) and Pro fallback (0.134); D's two probes (`veo-3.1-fast-ref2v` 0.80, `gemini-omni-1.1-flash` t2v 0.811) — conditional on D1 failing identity or the world, which it did not — and one D1 attempt (0.80). Nothing transferred between treatments. No fal, no cash pool, no route outside `production_use_allowed: true`; `veo-3.1-fast-extend` (manual_only) was never in the tool.

## Verdicts (producer's, per treatment record)

- att-001 **accepted** (B owner sheet; used) · att-002 **not_selected** (repair draw: run poses less distinct, splitter gaps still merged; a counted attempt) · att-003/004/005 **accepted** (B plate, swarm, wall).
- att-006 **accepted** (C 2×4 pose sheet; no repair needed).
- att-007 **not_selected** (D micro-qualification: PASSED the identity + aesthetic gate; not composited — duplicate book, fire flash, wall visible from the start, street drift) · att-008 **not_selected** (take 2: swarm crumbles before the power) · att-009 **accepted** (take 3: composited).

## Directional model observations (routing_authority: none)

- `nano-banana-2` sprite sheets: 3/3 draws usable on identity, props and no-lettering; 2/2 attempts to get two *distinct* run-leg phases from text failed (near-identical poses; Lane B saw the same) — n = 2 here.
- `nano-banana-2` 2×4 pose grid with expressions: 1/1 first draw usable, all eight poses present, identity held against a separately drawn base sheet.
- `veo-3.1-fast-i2v` from a composed pixel-art world frame: 3/3 ok, 0 refusals, identity of the character held in all three, camera locked side-on in all three (the negative prompt + locked-camera clause), the requested event chain in order in all three; in all three the scenery drifts to different buildings after ≈ 5 s, effects are painted rather than pixelated and the character softens after heavy effects; one or two unrequested elements per draw (duplicate book 2/3, fire/sparks 2/3, obstacle self-destructing 1/3, a marked plaque 1/3). Native audio produced 3/3, content not ear-checked.

## Blindness limitations to declare with the packet

- Clips A and B carry byte-identical audio (B re-used the baseline mix by design); an evaluator may notice two clips sound the same.
- One clip keeps a video model's own soundtrack; the README says so without saying which.
- Packet clip sizes differ (7.4–9.1 MB); only the picture and sound are to be judged.

## Provenance of the dispatch tool

`tools/_common.py` — copied from Lane A `tools/_common.py` @ 7dab37a (original sha256 `22cdc2f6…`; header edited only). `tools/dispatch.py` — ledger/cap/attempt/failure logic and the Nano Banana 2 recipe from Lane A `tools/dispatch.py` @ 7dab37a; Veo i2v/ref2v request and poll shape from `eval/harness-v2/adapters/vertex_veo.py`; Omni t2v shape from `eval/harness-v2/adapters/gemini_api_omni.py` + `vertex_omni.py`; prices live from the runtime PriceBook (a route whose quote is not `priced` is refused); `CAP_USD = 6.0`; per-treatment maxima enforced; `--confirm-spend` required. Refusal paths tested at USD 0 before the first paid call (no confirm flag; an IP word).
