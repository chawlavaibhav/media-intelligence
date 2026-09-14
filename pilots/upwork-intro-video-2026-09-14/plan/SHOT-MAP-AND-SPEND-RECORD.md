# Shot map, routes, fallbacks and SPEND RECORD — pilot `upwork-intro-video-2026-09-14`

**Authority.** Controller (Vaibhav) instruction of 14 Sep 2026 in the production session: "This is intentionally a
paid product-learning run… Recommended Controller ceiling: INR 3,000. Treat this as a HARD CAP… One bounded normal
repair cycle is authorised inside the INR 3,000 cap." Plus his rulings the same day: fully AI-made, no footage of him,
Upwork "video of you" rule risk accepted by him, Ledge design direction, sealed lab media may be reused.
This pilot is **separate from Alpha-1** (C-7) and does not widen it. Nothing here touches sealed evidence.

**Hard cap:** INR 3,000 = USD 31.44 at the repo rate 95.4211. Pools: `credits` (Vertex + Gemini API) first; `cash`
(fal, USD 3.35 available) only for the one cheap plate animation; `sarvam_credits` unused unless a fallback fires.
**Ledger:** `gen/LEDGER.jsonl`, one line per dispatch, written before the request leaves; totals in `gen/LEDGER-SUMMARY.md`.

## Production units → routes

| # | Unit | What it must do | Route (surface) | Evidence basis | Fallback | Planned draws | USD |
|---|---|---|---|---|---|---|---|
| P0 | Presenter portrait still, 16:9 | One accepted face/room/light to anchor every take | Nano Banana 2 `gemini-3.1-flash-image` (Gemini API, credits) | CLEAN for stills (img-r1 11/12; EVAL-038 live surface) | NB Pro (same surface) | 3 | 0.20 |
| P1 | **Smoke**: T1 as i2v + native speech from P0, 8 s 1080p | Prove identity+lips+no lettering on the primary route | Veo 3.1 fast i2v `generateAudio:true` (Vertex, credits) | i2v CLEAN 5/8; native speech DIRECTIONAL 2/2 (RR-14); the combination UNTESTED | Omni 1.1 Flash i2v (Vertex, 0.81); Kling i2v audio (fal, 1.34) | 1 (+1 fallback) | 0.96 (+0.81) |
| P2 | T2 take 8 s | same | same as the route P1 proves | as P1 | as P1 | 1 | 0.96 |
| P3 | T3 take 8 s | same | same | as P1 | as P1 | 1 | 0.96 |
| A0 | Aarohi serum plate, 4:5, textless | The Ledge plate (bottle base at 3/5 height, window light left, empty lower third) | Nano Banana 2 (Gemini API, credits) | CLEAN (RR-1/RR-7 textless plate route) | FLUX.2 Pro (fal, 0.03) | 2 | 0.13 |
| A1 | Aarohi text-in-motion clip: plate → i2v 6 s, then code overlay per frame | The sold "offer as animated text in motion" deliverable | MiniMax H3 Max i2v (fal, cash) | CLEAN: arm C 2/2 (RR-6), H3 Max i2v 7/8 | Kling v3 Pro i2v (fal) / Veo fast silent (credits) | 1 | 0.30 |
| L1 | Diwali sweets text-in-motion | code-set Devanagari in motion | **sealed** `topo3-video …C_textless_plate_i2v_composite__r1.composite.mp4` | CLEAN, accepted | r2 composite | 0 | 0 |
| L2 | Juice macro + code-set offer | premium product clip with exact text | **sealed** `vid-t2v VID-T2V-04 gemini-omni r1` + overlay by code | CLEAN accepted clip; overlay = RR-6 mechanism | Veo fast r1 | 0 | 0 |
| M1 | Music bed 57 s | quiet, inert under speech | **sealed** Lyria `MUS-01 r1` (32.8 s) looped with a crossfade by ffmpeg | CLEAN accepted | MUS-02 | 0 | 0 |
| C* | Cards, build, sizes, hooks, check, supers, end card | every critical string exact | code (hb-view + Pillow + ffmpeg) | deterministic | — | 0 | 0 |
| **First pass total** | | | | | | | **≈ 3.5 + 1.3 stills = 4.8 USD ≈ ₹460** |
| Bounded repair reserve | one presenter redraw + one plate redraw + fallback route smoke | | | | | | ≤ 3.0 USD |
| **Planned ceiling for this run** | | | | | | | **USD 8 (₹765) — cap USD 31.44 (₹3,000)** |

Stop rules: any refusal/lock counts as a failed draw and is recorded; no draw is re-sent with the same prompt more than
once; if the P1 smoke fails on all three routes, the film switches to the silent-presenter + Sarvam voice fallback
(U1-alt) and returns to the Controller before further spend; if cumulative spend would pass USD 12 (₹1,145) the run
pauses and reports.

## Exact-text discipline
No model is asked to write any word. Plates and the portrait carry the instruction "no text, captions, subtitles,
logos, labels or lettering anywhere in any frame". Every string on screen comes from `plan/COPY-DECK.yaml` v4 and the
D3 check asserts it.
