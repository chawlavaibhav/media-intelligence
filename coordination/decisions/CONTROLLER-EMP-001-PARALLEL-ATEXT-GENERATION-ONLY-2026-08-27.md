# Controller — Parallel A-TEXT Generation-Only Override — 2026-08-27

## Status

**AUTHORISED: GENERATE AND SEAL THE 16 FROZEN A-TEXT IMAGES IN PARALLEL WITH EVAL-023, BUT DO NOT SCORE, INTERPRET, PROMOTE OR OPEN DEEPER SPEND UNTIL A QUALIFIED EVALUATOR EXISTS.**

This is an explicit Controller override of the earlier EMP-001 ordering rule that required a qualified
text judge before any A-TEXT generation.

The scientific gate itself is NOT relaxed. Only the order of generation vs evaluator qualification
changes.

## Why this is scientifically safe

A-TEXT generation and evaluator qualification use independent materials.

Generating the model outputs before the evaluator qualifies does not change:
- the frozen A-TEXT prompts;
- model routes/versions;
- evaluator qualification battery;
- scoring rule;
- thresholds.

The generated artifacts must be sealed and later scored exactly as generated. They must NOT be
regenerated after seeing evaluator behaviour or qualification results.

Therefore this is a scheduling optimisation, not a change to the measurement claim.

## Frozen generation shape

A-TEXT:
- 4 frozen strings;
- 2 repeats;
- 2 routes;
- 16 generations maximum.

Strings:
- `शुभ दीपावली`
- `आज की डील`
- `Aaj ki Deal`
- `SAVE 20% • ₹999`

Routes:
- IMG-01: fal `openai/gpt-image-2`, 1024×1024, medium, 8 unseeded generations;
- IMG-02: fal `fal-ai/ideogram/v3`, BALANCED, 8 unseeded generations.

No prompt, route, size, quality, repeat count or seed policy may be changed.

## Spend

Planning prices remain:
- IMG-01: 8 × USD 0.053 = USD 0.424;
- IMG-02: 8 × USD 0.060 = USD 0.480;
- nominal maximum generation spend = **USD 0.904**.

Current cumulative qualification spend before this generation-only batch:
- USD 1.3037905.

Prospective cumulative EMP-001 spend after nominal A-TEXT generation:
- USD 2.2077905.

This remains below the user-approved USD 10 total EMP-001 consumed-API ceiling.

Retries remain 0.
No account prefunding above the approved ceiling.

## Required implementation

Add a bounded A-TEXT generation-only path rather than weakening the existing qualified-judge gate.

The generation-only path must:
1. run preflight and authorisation;
2. open the same persistent EMP-001 run/budget;
3. reserve generation cost before each provider call;
4. persist one Attempt/trial per generation;
5. persist failed/refused/ambiguous attempts;
6. preserve conservative ambiguous-dispatch billing;
7. never invoke an evaluator;
8. write the generated artifact plus immutable hashes and route/request identity;
9. mark every output `evidence_state: generated_unscored`;
10. mark `may_open_registry: false`, `may_open_atext_verdict: false`,
    `may_open_deeper_stage: false`;
11. write a manifest binding all 16 trial coordinates to artifact SHA/config/request;
12. refuse duplicate generation if a sealed trial for that coordinate already exists, unless a
    future Controller explicitly authorises replacement;
13. retries 0.

## Later scoring

When a text evaluator eventually qualifies for all required scripts/family handoff:
- score these exact stored artifacts;
- do not regenerate them;
- create evaluator trials linked to the existing generation attempts;
- only then may route-level A-TEXT pass/fail be computed.

If no evaluator ever qualifies, the 16 images remain unscored empirical artifacts and no model claim
is derived from them.

## Stop conditions

- any ambiguous generation dispatch: persist/count and stop generation-only batch, retries 0;
- any budget refusal: stop;
- any route/config mismatch: stop before dispatch;
- no evaluator calls;
- no Stage A 90-generation expansion;
- no Registry rows;
- no A-TEXT verdict yet.
