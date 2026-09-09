# EVAL-040 Image Round 1 — summary after the blind reveal (2026-09-08)

**Product evidence, not Registry evidence.** Verdicts are the Controller's blind accept/reject against each case's
acceptance contract (75 pictures, J01–J75, judge copies re-encoded metadata-free; reveal verified against the
committed commitment). Registry rows are NOT written: every deterministic instrument still reports
`criterion_not_frozen` until the Controller freezes `eval/harness-v2/instruments/PASS-CRITERIA-v0.yaml` (MD-C1).

## Spend

| Run | Calls | Cash (fal) | GCP credits | Total USD |
|---|---:|---:|---:|---:|
| smoke | 1 | — | 0.067 | 0.067 |
| img-r1 | 76 | 2.446 | 2.211 | 4.657 |
| img-r1-redo (8 trials that never reached a provider during the 12:42–14:07 IST network outage) | 8 | 0.244 | 0.268 | 0.512 |
| **Total** | **85** | **2.690** | **2.546** | **5.236 ≈ ₹500 of the ₹1,200 cap** |

## Results per route (accepted / trials; cost per accepted picture)

| Route | Core stills (4 cases × 2) | Exact text (2 cases × 2) | All | USD per accepted |
|---|---|---|---|---:|
| gpt-image-2 (fal, cash) | 7/8 | 4/4 (Hindi 2/2, English 2/2) | 11/12 | 0.058 |
| nano-banana-2 (Vertex, credits) | 7/8 | 4/4 (Hindi 2/2, English 2/2) | 11/12 | 0.073 |
| qwen-image-3 (fal, cash) | 7/8 | 2/4 (Hindi 1/2; English 1/2 — one moderation refusal on the gym offer) | 9/12 | 0.053 |
| nano-banana-pro (Vertex, credits) | 4/8 | 4/4 | 8/12 | 0.201 |
| seedream-5-pro (fal, cash) | 6/8 | 2/4 (Hindi 0/2, English 2/2) | 8/12 | 0.101 |
| flux-2-pro (fal, cash) | 5/8 | 1/4 (Hindi 0/2, English 1/2) — see caveat 1 | 6/12 | 0.060 |
| recraft-v4 (fal, cash; text cases only) | — | 2/4 (Hindi 0/2, English 2/2) | 2/4 | 0.080 |

E1/E2 (8-trial and 4-trial denominators, ELIMINATION-RULES.md): every route survives the core; flux-2-pro is
below E2 on the text question (caveat 1 applies).

## What the pictures say

1. **Cheap exact text is real for stills.** GPT Image 2 and Nano Banana 2 rendered the Devanagari Diwali poster and the
   English gym offer correctly on both tries, at USD 0.05–0.07 a picture. Nano Banana Pro did the same at three times the
   price. Seedream 5 Pro, Recraft V4 and FLUX.2 Pro all failed Devanagari on both tries ("wrong spelling"); Qwen got it
   once. The "cheap text" half of the Controller's hypothesis is supported for still images.
2. **The expensive Google model was the worst value on plain stills.** Nano Banana Pro put a white label on the juice
   bottle both times (contract: label blank) and cropped the biryani salad both times. Fine at text, poor at restraint.
3. **The biryani flat-lay exposed a composition failure most routes share:** the salad bowl or raita cut off at the frame
   edge (rejected on gpt-image-2 r1, nano-banana-2 r1, nano-banana-pro ×2, qwen r2, seedream ×2). FLUX was the only
   route that kept everything in frame both times. This is a CA-D3 (edge treatment / tangency) failure the gate cannot
   yet mechanise; it is exactly the kind of check worth building next.
4. **The child-at-the-window scene** (policy-edge case) was refused by nobody; FLUX was rejected twice on staging
   ("looks water will come in", "sitting outside window"), every other route accepted twice.
5. **One moderation refusal**: Qwen Image 3 refused the "FLAT 40% OFF / First 100 members only" gym poster once.

## Caveats the Controller should know

1. **The composite arm was not actually tested.** The plan's "C_composite_textless_base" rows for FLUX.2 Pro were
   dispatched with the same text-bearing blueprint prompt as arms A/B (one blueprint per case, byte-identical across
   routes — the package's own rule). FLUX therefore ran as a cheap *text-generating* route and is scored as such
   above. The textless plate + code overlay arm needs its own prompt variant and the overlay step; it is a package
   defect to fix before the composite question is answered. The overlay tool itself is not built yet.
2. **Two verdicts came after the sheet** (J16 accept, J34 reject) in chat, once the blank entries were pointed out;
   recorded in VERDICTS.yaml with a note.
3. **Repeat consistency** was measured on every second draw but carries no verdict (threshold not frozen).
4. **fal 202 misread and the outage** cost nothing extra: five written-off jobs were recovered by request id without
   re-submission; eight never-sent trials were redone under `img-r1-redo`; one submitted job whose request id was lost
   (IMG-CORE-03 gpt-image-2 r1) was redone and may have been billed twice (≈ USD 0.05).

## Routing table v0 for still images (product evidence, this round only)

| Job | Use | Fallback | Why |
|---|---|---|---|
| Plain commercial still, no text | nano-banana-2 (credits) or gpt-image-2 | qwen-image-3 | 7/8 each; cheapest accepted |
| Exact Devanagari text on a still | nano-banana-2 or gpt-image-2 | nano-banana-pro (3× price) | 2/2 each; every other route failed Hindi |
| Exact English text on a still | gpt-image-2 / nano-banana-2 | seedream-5-pro, recraft-v4 | 2/2 each |
| Food flat-lay with several elements | flux-2-pro | gpt-image-2 (1/2) | only route that kept the frame intact twice |
| Blank label / packaging restraint | avoid nano-banana-pro | — | white label both tries |

## Next

- Freeze the instrument thresholds (MD-C1) so the first Registry rows (format, latency, refusal, repeat consistency)
  can be written from this round's records.
- Fix the composite arm (textless prompt variant + overlay tool) — a small package rebuild, then 4 cheap calls.
- Image half two (edit, extend, compose, reference cases) needs the Controller's photos or constructed inputs.

## Addendum (2026-09-09) — the composite arm, tested properly

Caveat 1 above is closed. Four FLUX.2 Pro plates generated with the blueprints' textless prompt (USD 0.12), the exact
strings set by code with pinned system fonts (Kohinoor Devanagari Bold, Helvetica Neue Bold; USD 0), judged by the
Controller against the same contracts: **4/4 accepted** ("all accepted"). Cost per accepted picture ≈ USD 0.03, the
cheapest of any route, and exact by construction. It could not be blind as to arm.

Routing consequence for stills with exact text: generated text on Nano Banana 2 / GPT Image 2 (2/2 each, ≈ USD 0.06)
and code-set text on a cheap plate (4/4, ≈ USD 0.03) are both acceptable. Code-set text is the default where exactness
is contractual (prices, legal lines, brand names) or where a re-render must be free; generated text where the type must
sit inside the scene (on a pack, a sign, a surface). Evidence: `eval/experiments/EVAL-040/runs/img-r1-composite/`.
