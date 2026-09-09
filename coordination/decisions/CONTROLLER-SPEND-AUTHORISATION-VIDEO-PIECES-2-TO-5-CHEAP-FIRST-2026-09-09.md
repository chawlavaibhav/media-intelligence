# Controller — Spend Authorisation: video pieces 2–5, cheap-first (no Seedance 2.5) — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.
**Parent rules:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` §3/§3a; hard limits as in
`CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md` §4.

## 1. Authority — the Controller's words

The Writer Controller put the per-piece caps (full and cheap-first, i.e. without Seedance 2.5) to the Controller, with the
recommendation to run cheap-first. The Controller:

> **"for videos- image to video, multi-shot and long clips, reference, knee proceed with them first. leave seedance 2.5 for now."**

## 2. Scope — four pieces, each its own run and cap (frozen package at commit 9adc4035d089, 2 repeats per route)

| Piece | Cases | Routes (Seedance 2.5 rows excluded by `--routes`) | Estimate | Cap |
|---|---|---|---|---|
| 2 — knee | VID-KNEE-01 | veo-3.1-lite, veo-3.1-full, minimax-h3-max-480p | USD 6.00 | **₹700 = USD 7.34** |
| 3 — multi-shot / long | VID-MS-01, VID-MS-02 | kling-v3-pro-15s, veo-3.1-fast-extend (2 calls/trial), kling-v3-pro-10s, gemini-omni-1.1-flash-10s (gemini-omni-1.1-flash-long refused by the planner: the pinned Omni page caps a clip at 10 s, the case row asks 15 — recorded, not run) | USD 10.63 | **₹1,600 = USD 16.77** |
| 4 — image-to-video | VID-I2V-01..04 | veo-3.1-fast-i2v, kling-v3-pro-i2v, minimax-h3-max-i2v, wan-3.0-prime-i2v | USD 20.74 | **₹2,250 = USD 23.58** |
| 5 — reference-to-video | VID-REF-01, VID-REF-02 | veo-3.1-fast-ref2v (kling-v3-elements is unpinned → excluded) | USD 2.40 | **₹300 = USD 3.14** |
| | | | **USD 39.77** | **₹4,850 = USD 50.83** |

Each cap covers that piece's lane plus one smoke call. Inputs: piece 4 animates the Controller-accepted round-one
stills (Nano Banana 2 draws of IMG-CORE-01 r1, IMG-CORE-02 r1, IMG-CORE-04 r2 — the accepted draws on the cheapest
text-capable route); piece 5 uses the half-two stand-in references (tin front/side/top; host portraits 1–3) and the
same decoys at judging. Blind judging by the Controller per piece; reveal after all verdicts; Registry rows only from
the deterministic instruments.

## 3. Hard limits

Per-piece ceilings above (`max_consumed_usd_equivalent`; `cap_1a_usd` = `cap_1b_usd` = the piece cap; Sarvam 0;
retries 0; price verified before every paid call; sealed evidence write-once; keys never printed). Run ids:
`vid-knee`, `vid-ms`, `vid-i2v`, `vid-ref` (+ `-smoke`). Authorisation files `eval/harness-v2/authorization.{knee,ms,i2v,ref}.local.yaml`
(gitignored), materialised from this record.

## 4. Not authorised

Seedance 2.5 on any case ("leave seedance 2.5 for now"); text-to-video core, two speakers, music, speech/lipsync
(caps quoted, not approved); anything beyond the rows above.

## 6. Addendum — reference-to-video duration and cap (Writer Controller, 2026-09-09)

The reference piece's smoke call was refused by Vertex: *"Unsupported output video duration 6 seconds, supported
durations are [8] for feature reference_to_video."* The frozen rows asked 6 s. Correction under the Controller's
"proceed with them first": `veo-3.1-fast-ref2v` rows on VID-REF-01/02 move to **8 s** (USD 0.80 a clip; 4 clips
USD 3.20 + the refused smoke USD 0.60 already charged + one new smoke USD 0.80 = USD 4.60), so the piece-5 cap is
raised from ₹300 to **₹450 = USD 4.72**. Nothing else changes; the same blind judging and decoy line-ups apply.
