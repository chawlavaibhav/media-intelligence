# SPEND RECORD — UPWORK-INTRO-V3-SHOWCASE (pilot `upwork-intro-video-2026-09-14`, pass v3)

**Written 2026-09-14 18:10 IST, BEFORE the first paid dispatch of this pass.**

**Authority.** Controller (Vaibhav) execution package "UPWORK INTRO V3", 14 Sep 2026, received in this session:
"Create a dedicated durable spend record before the first paid dispatch. Controller hard cap: INR 2,000. Expected spend
should be materially below the cap. The cap is not a target. Use cumulative ledger semantics and current pinned prices.
If the planned first pass exceeds INR 2,000: STOP BEFORE SPEND."

**Run class.** Paid commercial showcase / product-learning production. NOT Alpha-1 qualification evidence, NOT Capability
Registry evidence, NOT Stage-A evidence, NOT proof that Canon works. Nothing here is written to the Registry; no sealed
evidence is touched. This pass is separate from passes v1/v2 of the same pilot (their spend USD 8.082 = INR 771 under
the earlier INR 3,000 record `../plan/SHOT-MAP-AND-SPEND-RECORD.md`; that lineage is closed — this record has its own cap
and its own cumulative ledger, `gen/LEDGER.jsonl`).

**Hard cap.** INR 2,000 = USD 20.96 at the repo display rate 95.4211 INR/USD (COST-TABLE rules). Enforced cumulatively
against `gen/LEDGER.jsonl` at every dispatch by `tools/gen.py` (reservation written before the request leaves; a dispatch
whose estimate would carry the cumulative reserved total past the cap is refused).

**Pools.** fal cash (Kling v3 Pro i2v, Wan 3.0 Prime i2v, MiniMax H3 Max i2v, GPT Image 2, Seedream 5 Pro Edit, FLUX.2
Pro); Vertex credits (Lyria 2); Sarvam prepaid (bulbul:v3); Gemini API credits (Nano Banana 2 fallback only).
**fal cash balance at record time: USD 3.2315** (free read, `rest.alpha.fal.ai/billing/user_balance`, 18:05 IST). This
pool — not the INR 2,000 cap — is the binding constraint on the video slots; see "Planned first pass".

**Pinned prices used (USD; eval/empirical-planning/price-pins-2026-09 + ROSTER-REFRESH-2026-09.yaml, fetched 2026-09-04).**

| Route (surface id) | Unit price | Basis |
|---|---|---|
| GPT Image 2 — `openai/gpt-image-2` (fal), quality=medium | 0.053 / image at 1024x1024; token-metered, non-square sizes bill higher (est. 0.06–0.10) | fal page table; roster fallback row |
| Seedream 5 Pro Edit — `bytedance/seedream/v5/pro/edit` (fal) | 0.0675 / output image (≤ 1536x1536 area, 1 input image) | fal JSON (labelled Tentative) |
| FLUX.2 Pro — `fal-ai/flux-2-pro` (fal) | 0.03 / first megapixel | fal JSON |
| Kling v3 Pro i2v — `fal-ai/kling-video/v3/pro/image-to-video` (fal), generate_audio=false | 0.112 / second | fal pin |
| Wan 3.0 Prime i2v — `alibaba/wan-3.0-prime/image-to-video` (fal), 720p | 0.14 / second (5-s increments) | fal pin |
| MiniMax H3 Max i2v — `minimax/h3-max/image-to-video` (fal), 768P | 0.08 / second | fal pin |
| Nano Banana 2 — `gemini-3.1-flash-image` (Gemini API) | 0.067 / image | Gemini API pricing pin |
| Lyria 2 — `lyria-002` (Vertex us-central1) | 0.06 / ~32.8-s track | Vertex pricing pin |
| Sarvam bulbul:v3 — `api.sarvam.ai/text-to-speech`, speaker `aditya` | INR 3.00 / 1,000 chars | Sarvam pricing pin |

**Planned first pass (GENERATE 1 → JUDGE → REPAIR ONLY IF FAIL; no N=3 spray).**

| Slot | Route | Draws | Est. USD |
|---|---|---|---|
| A0 Aarohi packshot 4:5 | GPT Image 2 medium | 1 | 0.08 |
| Kora base 16:9 | GPT Image 2 medium | 1 | 0.08 |
| Brewa packshot 4:5 | GPT Image 2 medium | 1 | 0.08 |
| A1 / A2 / A3 Aarohi scenes | Seedream 5 Pro Edit | 3 | 0.2025 |
| B1 / B2 / B3 Brewa scenes | Seedream 5 Pro Edit | 3 | 0.2025 |
| Dhaba 47 flat-lay 4:5 | FLUX.2 Pro | 1 | 0.03 |
| Video A1 hero 5 s | Kling v3 Pro i2v | 1 | 0.56 |
| Video A2 4 s (static → motion beat) | Kling v3 Pro i2v | 1 | 0.448 |
| Video A3 4 s | Kling v3 Pro i2v | 1 | 0.448 |
| Video B1 4 s | Kling v3 Pro i2v | 1 | 0.448 |
| Music bed | Lyria 2 | 1 | 0.06 |
| Voice-over (~1,000 chars, 8 paragraph calls) | Sarvam bulbul:v3 `aditya` | 8 | ≈ INR 3.3 (USD 0.035) |
| **First pass** | | | **≈ USD 2.67 ≈ INR 255** |
| Reserve inside fal balance for ONE repair/fallback (Seedream repair 0.0675, GPT Image 2 → Nano Banana 2 fallback, or one Wan/H3 fallback ≤ 0.56) | | | ≤ 0.56 |
| **Planned ceiling this pass** | | | **≈ USD 3.2 ≈ INR 306 — cap USD 20.96 (INR 2,000)** |

**Slots the fal balance does NOT cover in this pass (recorded as deviations, not silently dropped):** Video B2, Video B3
(Brewa), Kora motion (optional in the frozen plan). Each is ≈ USD 0.34–0.56 on Kling at 3–5 s. They can be run as a
SPECIFIC REPAIR after a fal top-up; they stay inside the INR 2,000 cap (cumulative ≈ INR 450 with all of them).

**Stop rules.** Any refusal/HTTP error/timeout is a failed draw, recorded, never re-sent with the same prompt more than once.
Opening hero (Video A1): Kling primary; if rejected, ONE Wan 3.0 Prime fallback only if the fal balance covers it; if that
also fails, STOP and report the slot. Packshots: primary + 1 fallback (Nano Banana 2, credits). Scenes: 1 draw + at most
1 Seedream repair. No premium exception is used in this pass.

**Clock.** The customer-order timer starts when A0 is accepted (product photo accepted; Aarohi brand colours frozen; offer
frozen) and is written mechanically to `gen/CLOCK.json`; it stops when the Aarohi deliverable bundle (4 sizes, 6 hooks,
Hindi, 9:16 video ad) is complete. No elapsed time is ever typed by hand.

## Closeout (2026-09-14 ~19:05 IST)
Reserved at pinned prices: **USD 3.2836 = INR 313.3** (37 calls). fal balance 3.2315 → 0.2589 (USD 2.9726 billed on fal).
Lyria: 4 calls on credits (3 failed, billing unknown). Sarvam: 16 calls ≈ INR 4.3. One reserve call (B2, USD 0.448) was
spent after every first-pass slot had been judged; it was rejected. Cap never approached. Vendor statements not reconciled.
