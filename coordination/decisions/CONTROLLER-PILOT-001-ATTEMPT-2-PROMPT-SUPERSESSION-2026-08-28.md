# Controller — PILOT-001 Attempt 2 Prompt Supersession — 2026-08-28

## Status
**THE SEGMENTED REPAIR PROMPT IS WITHDRAWN BEFORE DISPATCH. A SIMPLER SINGLE-SCENE PROMPT IS NOW
THE FROZEN ATTEMPT 2 PROMPT.**

Writer Controller decision, made on direct instruction from the user (customer proxy and
acceptance authority for PILOT-001) received in chat on 2026-08-28 and made durable here.

## What is superseded

The "Frozen repair prompt" section of
`coordination/decisions/CONTROLLER-PILOT-001-CANDIDATE-1-REJECTION-AND-REPAIR-2026-08-28.md`
— the prompt split into timed phases (0–2.5s source / 2.5–4.5s transformation / 4.5–8s settle,
"two blank frameless media panels").

That prompt was **never dispatched**. No spend was consumed on it. Everything else in the
rejection-and-repair decision remains in force unchanged: the Candidate 1 rejection (H1/H4/H6
FAIL), the classification of the defect as provider-origin, the allocation of the single repair
to one final provider generation, the spend arithmetic, and the evidence rules.

## Why

1. **The acceptance authority pre-declared it non-credible.** The user reviewed the segmented
   prompt and judged that its timed multi-phase choreography and abstract "media panels" idea
   read as incoherent — the same failure family as Candidate 1. Spending the last authorised
   provider call on a prompt the final reviewer already expects to fail is irrational.
2. **Mechanism.** Short video generation models follow one coherent scene with a simple camera
   instruction far more reliably than second-by-second stage directions. Candidate 1 failed on
   "not premium / does not hold / makes no sense"; the highest-probability fix is a single real,
   held, premium scene — not more choreography.

Durable production-intelligence lesson (extends the Candidate 1 lesson): *style adjectives are
not a substitute for a visual idea, and timed multi-phase choreography is not a reliable way to
give an 8-second video model one.* Prefer one concrete scene, one camera move, explicit holds.

## Frozen Attempt 2 prompt

Use semantically as written. Minor punctuation changes for API encoding allowed; no creative
rewriting after seeing the result.

> An 8-second vertical premium commercial shot for a modern Indian brand during the festive
> season. One single continuous scene, photoreal luxury advertising cinematography: a refined
> unbranded gift box on a dark ink-navy studio tabletop, warm amber practical light, subtle
> brass and silk textures, a few scattered marigold petals, soft out-of-focus warm festive
> lights in the background. One slow, smooth camera movement that gently eases into a
> near-still hold on the composed scene. Restrained, minimal, expensive and calm, with
> generous clean negative space through the middle and lower frame. Absolutely no text,
> typography, logos, letters, numbers, signage, icons, UI elements, people, faces, dialogue,
> voiceover or lyrics. No named festival, no religious symbols, no abstract sculptures, no
> floating objects, no morphing, no visual clutter, no gaudy saturation.

The palette and register are the official Aight website brand tokens from the PILOT-001 freeze
(ink navy `#141f31` ground, warm restraint, stamp red only as deterministic accent later) —
the provider cannot be given the website itself as a reference, so its aesthetic is carried by
these terms.

## What does not change

- provider/route/model: direct Gemini Developer API, `veo-3.1-fast-generate-preview`, 8s,
  9:16, 720p;
- the model renders **no** text, logo, or numbers — all claims (`Image ₹9`, `Video ₹99`) and
  the `Aight.` endcard (`Outcome API`, `getaight.ai`) remain deterministic, reusing the exact
  accepted Candidate 1 layer;
- spend: USD 2.00 hard cap, USD 0.80 reservation for Attempt 2, 0 retries, no third call;
- Attempt 2 remains the final repair; after Candidate 2 there is no repair left;
- acceptance: final human H1–H6 review by the user; no acceptance row before that review;
- all evidence/immutability rules of the rejection-and-repair decision.

## Execution pointer

`coordination/plans/2026-08-28-PILOT-001-ATTEMPT-2-EXECUTION-ADDENDUM.md` is updated to point
at this prompt. The user confirms the prompt wording at dispatch time in the key-holding
environment; any wording change before dispatch requires one further supersession decision,
not ad-hoc editing.
