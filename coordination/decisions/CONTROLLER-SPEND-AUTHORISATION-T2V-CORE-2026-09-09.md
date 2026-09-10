# Controller — Spend Authorisation: text-to-video core, cheap-first — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.
**Parent rules:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` §3/§3a; hard limits as in
`CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md` §4.

## 1. Authority — the Controller's words

The cheap-first cap for the text-to-video core (₹3,550, Seedance 2.5 left out) was quoted on 2026-09-09 and recommended
first; after the day-2 close the Writer Controller named it as the one unrun piece. The Controller:

> **"cool text to video it is. you can run other pieces without spend ones too in parallel."**

## 2. Scope — `VID-T2V-01..04` (four ordinary customer briefs, 6 s, 9:16, audio on where native), cheap-first

| Route | Surface / pool | Cost per 6-s clip | Trials | Cost |
|---|---|---|---|---|
| veo-3.1-fast | Vertex, credits | USD 0.60 | 8 | USD 4.80 |
| gemini-omni-1.1-flash | Vertex, credits | USD 0.61 | 8 | USD 4.87 |
| minimax-h3-max | fal, cash | USD 0.48 | 8 | USD 3.84 |
| wan-3.0-prime | fal, cash | USD 0.84 | 8 | USD 6.72 |
| kling-v3-pro-audio | fal, cash | USD 1.01 | 8 | USD 8.06 |
| sora-2 | conditional in the package | — | — | dispatched only if the planner admits it |
| seedance-2.5 | — | — | — | left out ("leave seedance 2.5 for now") |
| | | | **40** | **USD 28.29 + one smoke (H3 Max, USD 0.48)** |

The fal balance (about USD 16 after the two-speaker Kling draws) may not cover all 24 fal trials (USD 18.62); a
balance refusal is recorded as infrastructure and the affected draws run under this record after a top-up.

## 3. Cap and hard limits

Cap **₹3,550 = USD 37.20** (`max_consumed_usd_equivalent`; `cap_1a_usd` = `cap_1b_usd` = 37.20; Sarvam 0; ElevenLabs 0).
Retries 0; price verified before every paid call; sealed evidence write-once; keys by name only; blind judging by the
Controller; Registry rows only from the deterministic instruments. Run ids `vid-t2v(-smoke)`; authorisation file
`eval/harness-v2/authorization.t2v.local.yaml` (gitignored); item basis commit 0ba06b92ee27 (package unchanged).

## 4. In parallel, no spend (the Controller's "other pieces without spend")

Pin the two unpinned routes (Kling Elements, sync-lipsync v3) from their vendor pages; build the vision-model
screening instrument for the `screened_not_qualified` tier and its qualification runner against the Controller's
verdicts — **offline only; no model call until a record authorises the qualification run**; size round two of stills.

## 5. Not authorised

Seedance 2.5; any model call for instrument qualification; anything beyond the rows above.
