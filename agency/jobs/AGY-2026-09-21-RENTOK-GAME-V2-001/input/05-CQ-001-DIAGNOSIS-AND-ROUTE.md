# RENTOK-CREATIVE-QUALITY-001 — diagnosis and proposed route (written after both blind verdicts; seal opened 2026-09-21)

Labels: OBSERVED (files, ledgers, recorded verdicts) · INFERRED · UNKNOWN. One brief, one beat (≈ 6.85 s), one customer, one independent evaluator: the diagnosis is evidence-backed for this job and directional beyond it.

## 1. The seal, opened after both verdicts were committed

| Packet label | Treatment | What changed vs the accepted film | Spend |
|---|---|---|---|
| clip-3 | **A — baseline** | nothing (stream copy of the accepted Lane A film, 14.0–20.8 s) | 0 |
| clip-2 | **B — asset prompts only** | four Nano Banana 2 prompts rewritten; renderer, board, timing, audio frozen | USD 0.335 (5 draws) |
| clip-4 | **C — creative direction + renderer, same topology** | per-beat feeling, framing, impact and effects specified; ≈ 20 new renderer primitives; one 8-pose expression sheet | USD 0.067 (1 draw) + code |
| clip-1 | **D — production-method change** | C's direction sent to Veo 3.1 Fast image-to-video (8 s, native audio), HUD/text composited by code | USD 2.40 (3 draws, take 3 used) |

Seal sha256 `c496d004…` (unchanged); mapping `treatments/PACKET-MAPPING.sealed.json`.

## 2. The two blind verdicts (OBSERVED, verbatim in `evaluation/`)

- **Customer:** "video 1 is good in drama. video 2,3,4 are better pixelated. video 1 looses quality towards the end" · rank "1,4,2,3 in decreasing order of acceptance" → **D > C > B > A**.
- **Independent evaluator (blind, media only):** creative-quality totals over eight 1–5 dimensions — **D 29 · C 25 · B 18 · A 18**; rank D, C, B, A on both creative quality and "would a polished-platform-game customer accept this beat"; "neither [D nor C] would be accepted as-is"; B and A tied on every dimension; clips 2/3 (B/A) "power is a thin cyan outline and a fingernail-sized ✓ … invisible at phone width, so the paper wall appears to dissolve on its own"; clip 1 (D) "soft painterly character and effects under a crisp pixel HUD read as two styles composited"; clip 1 true-peaks at −0.2 dBTP (over the −1 dBTP limit).

The two judges agree on the order without contact. The customer's two qualitative notes map exactly onto the producer's own pre-verdict observations for D (style softening after the burst; the street drifting to different buildings after ≈ 5 s).

## 3. Diagnosis by candidate cause

**Cause B — creative information lost between plan and model-facing prompt: REFUTED as the primary cause (this job).** Evidence: the Phase-1 trace found 1 of 16 decisions lost at the prompt step (`02-LOSS-OF-INTENT-TRACE.md`); Treatment B, which changed only the asset prompts and produced visibly richer stills (expression on the owner's face, shop fronts, wires, laundry, a diving swarm — OBSERVED on the frames), scored **identical to the baseline** with the evaluator (18 = 18) and ranked one place above it with the customer. Better pictures did not move the beat because the beat is made of motion, timing and impact, none of which a still prompt can carry. INFERRED: the customer's hypothesis located the loss one step too late in the chain.

**Cause A — creative direction under-specified: CONFIRMED, and it is the cheapest lever.** The plan never stated a feeling per beat, a framing target, or impact language (2 decisions never specified, 4 simplified in the trace); the renderer it fed had a vocabulary of slide / flash / offset (3 decisions lost in animation). Treatment C — direction written per beat, then the renderer given anticipation, hit-stop, shake, easing, expression swap, camera push, particles, grade change, per-beat audio — moved the evaluator score by **+7 for USD 0.067 and code**, and moved the customer from last to second, while keeping the pixel-art style the customer said he preferred ("2,3,4 are better pixelated"). INFERRED: on this topology, the quality was not blocked by the method; it was never asked for and the renderer had no way to say it.

**Cause C — production method: PARTIALLY CONFIRMED, as a trade.** Treatment D produced the strongest drama (customer's word; evaluator +11 over baseline, best on character expressiveness, motion, gameplay readability, audiovisual impact) — the video model supplies continuous deformation, impact and secondary motion that the still+code renderer cannot. It bought that with the losses both judges saw: style softening from pixel art to painterly after the burst, the street drifting to other buildings after ≈ 5 s, one or two unrequested elements per draw (duplicate book 2/3, spark flash 2/3), the HUD reading as a second style, true peak over limit. Cost 36× a still per attempt (USD 0.80 vs 0.067), 3 attempts to reach a usable take. INFERRED: the method change is a real gain in motion quality and a real loss in control and style fidelity; neither judge accepted it as-is.

**Overall: D (combination), with a clear order of leverage —** (1) direction that names feel, framing and impact per beat; (2) a renderer that can execute it; (3) a video model for the beats where continuous motion matters more than style precision. The prompt layer was never the bottleneck.

## 4. What Media Factory had that the current pipeline lacked — and which of it mattered here (OBSERVED in `03-MEDIA-FACTORY-EVIDENCE.md`; effect INFERRED from Phase 2)

| Practice (historical source) | Applied in | Effect seen |
|---|---|---|
| Intended feeling stated per beat before any prompt (`rentok-ad/assets/brief.md`) | C | the single change that turned "slide, flash" into a beat with a low point and a lift |
| Character with personality/expression (`brand.json`) | B, C | B: expression on stills, no motion gain; C: eight drawn states used by the renderer |
| Several takes compared, one change-set per take (MF `scores.json`) | D | take 3 of 3 selected; each take's change recorded |
| Five-part shot description (shot → subject → action start/end → camera cause → light/sound) | D's Veo prompt | 3/3 draws held identity, side-on camera and the full event order |

## 5. Proposed route for the full 30-s advertisement (PROPOSED — not authorised by this file)

**Backbone: Treatment C's topology** (AI stills + the upgraded renderer) for the whole film — it keeps the style the customer prefers, exact text by code, deterministic timing and safe zones, USD ≈ 0.5–1.0 in stills, and every primitive built in C is reusable across all five obstacle beats. Required first: rewrite the Stage 3 board schema to carry, per beat, `feeling`, `framing` (owner ≥ 25 % of frame height at the beat's focus), `impact` (anticipation / hit-stop / shake / particle / audio sting) — the fields C wrote by hand.

**Hero beats on the video model, optionally:** the power-up transformation and the flag/victory — the two moments where continuous motion earns its cost — as Veo 3.1 Fast i2v clips of ≤ 6 s from a C-rendered start frame, one change-set per take, ≤ 3 takes each, composited under the code HUD. Mitigations for what both judges saw: shorter clips (drift set in after ≈ 5 s), a style-lock line and a pixel-art negative-space reference, true-peak limiting in the mix, an ear check of native audio, and a style-consistency gate (compare the clip's last frame to the C frame it must cut back to). If the style seam stays visible, drop the hero-beat clips and ship C alone.

**Cost (PriceBook pins):** C-only ≈ USD 1.0; with two hero beats ≈ USD 1.0 + 2 × 3 × 0.60 ≈ 4.6; recommended cap USD 6.

**Capability risks, honest:** no evidence that Veo holds pixel-art style beyond ≈ 5 s (n = 3, all drifted); unrequested elements in 2/3 draws; native audio unheard by any ear; the renderer's remaining gaps (secondary motion, true contact, squash-and-stretch on pixel art) are documented in `TREATMENT-C.md` and do not go away; a strong 7-s beat does not guarantee a strong 30-s film — the 30-s cut has five obstacle beats and the same customer will judge pacing across all of them.

## 6. The smallest consequential change

Add three fields to the creative board — feeling, framing, impact per beat — and keep the C renderer primitives. That is the change that moved the customer's rank from last to second at USD 0.07, holds the style he wants, and is repeatable on the next job without a new model, a new Canon source or a new workstream. The video-model route is a second, optional step for one or two beats, worth its cost only if the style seam can be hidden.
