# Video piece 1 — text into motion (VID-TOPO3-01) — summary (judged 2026-09-09)

**Case** a Hindi Diwali sweets promo, 9:16, 6 s: three exact strings (greeting, "20% छूट" offer, shop name) must read
correctly on every frame. **Hypothesis under test (H-CHEAP)**: a cheap still plus a cheap animator beats the strongest
video model writing the text itself.

**Arms** (all customer-shaped prompts, Canon-backed blueprint):
- A — cheapest still model (Qwen Image 3, 9:16 plate; the Controller picked draw 2 after rejecting draw 1 as misspelled)
  → cheap image-to-video (MiniMax H3 Max, Wan 3.0 Prime), 2 repeats each.
- B — premium native text-to-video writing the Hindi itself (Veo 3.1 full, Kling v3 Pro), 2 repeats each.
- C — textless FLUX.2 Pro plate → MiniMax H3 Max image-to-video → the three strings set by code on every frame
  (`composite.py --video`, Kohinoor Devanagari Bold), 2 repeats.

**Spend** USD 10.22 (smoke 0.48 + lane 9.74; overlay USD 0) of the ₹950 cap. **Judge** the Controller, blind as to route
and arm (V01–V10; `judging-video/MAPPING.json`, `VERDICTS.yaml`; reveal in `RESULTS.yaml`).

## Result

| Arm | Route | Accepted | Controller's words |
|---|---|---|---|
| C | H3 Max + code overlay | **2 / 2** | "no mistakes", "correct" |
| A | H3 Max i2v | 0 / 2 | "same kali thing" (the plate's own 'कली'); r1 "different text altogether" (frames show the plate's lettering carried over) |
| A | Wan 3.0 Prime i2v | 0 / 2 | "same kali thing"; "kali mistake + chhoot has wrong spelling" |
| B | Veo 3.1 full | 0 / 2 | "some other text altogether" |
| B | Kling v3 Pro | 0 / 2 | "different texts altogether" |

Elimination: every arm except C is eliminated by E2. The Controller also noted V06–V10 looked visually better than
V01–V05 — a split that mixes all three arms, recorded as an observation, not a route effect.

## What this says

1. **The premium video models cannot write Devanagari.** Veo 3.1 full and Kling v3 Pro produced fluent-looking but
   fabricated script on all four draws, at USD 0.60–1.20 a clip. Arm B is the wrong way to put Hindi text in motion.
2. **Cheap animators preserve a plate's lettering exactly** — including its mistakes. H3 Max and Wan carried the Qwen
   plate's misspellings through six seconds without drift. The arm-A failure is upstream: the cheapest still model
   misspelled both 9:16 plates, where round one showed Nano Banana 2 and GPT Image 2 spelling Hindi 2/2.
3. **Code-set type on an animated textless plate is exact by construction and cost nothing beyond the plate and the
   animation** (≈ USD 0.03 plate + the i2v call). It is the only route that passed.

H-CHEAP is **supported in its strong form**: the cheap chain beat the strongest video models outright; the strongest
models scored zero. What is not yet shown is arm A with a text-capable plate (Nano Banana 2 / GPT Image 2) — offered
to the Controller (~USD 1.6), not authorised at the time of writing.

## Routing consequence (recorded in ROUTING-EVIDENCE-MAP-v0 as RR-6, RR-7)

- Exact Devanagari in motion → animate a textless plate and set the type by code; or carry a *correct* still into a
  cheap animator. Never ask the video model to write it.
- The plate that feeds an animator must come from a text-capable still route (RR-2), never the cheapest still model.

Deterministic Registry rows for the five video routes (format, cost, latency/errors, reliability, repeat consistency):
25 rows via `registry_rows.py`. No acceptance number above is a Registry row.
