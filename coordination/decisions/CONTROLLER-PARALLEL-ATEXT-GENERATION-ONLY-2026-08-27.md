# Controller Parallel A-TEXT Generation-Only Authorisation — 2026-08-27

## Status

**AUTHORISED IN PARALLEL WITH EVALUATOR QUALIFICATION: GENERATE AND SEAL THE 16 FROZEN A-TEXT IMAGES NOW, BUT DO NOT SCORE THEM UNTIL A QUALIFIED EVALUATOR/HANDOFF EXISTS.**

This explicitly overrides the earlier EMP-001 ordering rule that generation waits for a qualified
text judge. It does NOT weaken the evaluator requirement for interpretation.

## Why

The old ordering saved generation spend if no judge qualified.

The user now prefers speed and has already approved a USD 10 EMP-001 consumed-API ceiling.
Current cumulative paid qualification spend is USD 1.3037905.

The frozen A-TEXT generation maximum is about USD 0.904 nominal, so generating the artifacts now
keeps the project comfortably inside the standing total ceiling while allowing evaluator work to
continue in parallel.

The scientific safeguard is:
**generate once now, seal the exact artifacts, and later evaluate those same bytes.**
No regeneration after seeing evaluator results.

## Frozen generation set

Strings:
1. `शुभ दीपावली`
2. `आज की डील`
3. `Aaj ki Deal`
4. `SAVE 20% • ₹999`

Routes:

### IMG-01
- fal route: `openai/gpt-image-2`
- 1024×1024
- medium
- 4 items × 2 repeats = 8 unseeded generations
- planning price USD 0.053/image
- nominal max USD 0.424

### IMG-02
- fal route: `fal-ai/ideogram/v3`
- quality/render mode: BALANCED
- 4 items × 2 repeats = 8 unseeded generations
- planning price USD 0.060/request
- nominal max USD 0.480

Total:
- 16 generations
- nominal max generation consumption USD 0.904

Retries: 0.

No sibling/model substitution.
No seed invention where route is unseeded.

## Required generation-only semantics

1. Do NOT call any evaluator.
2. Do NOT calculate pass/fail.
3. Do NOT populate Registry.
4. Do NOT open full Stage A.
5. Persist one trial/attempt per provider call.
6. Failed/refused/timed-out calls remain evidence.
7. Ambiguous post-dispatch failure retains conservative reservation and stops that route fail-closed.
8. Use the existing persistent EMP-001 run/spend ledger.
9. Before each dispatch mechanically enforce the USD 10 total ceiling.
10. If account funding/top-up above the standing ceiling is required, stop.

## Artifact sealing

For every successful generation persist:
- A-TEXT item id;
- exact requested string;
- script;
- route/model identity;
- exact request configuration;
- repeat index;
- trial/attempt id;
- provider request id if available;
- generation cost/cost_ref;
- raw returned artifact;
- SHA-256 of artifact bytes;
- dimensions/media metadata;
- completion status.

Create a generation-only manifest that binds:
- all 16 planned coordinates;
- every actual call record;
- artifact hashes;
- exact route/config identity;
- frozen A-TEXT input set;
- evidence fingerprint;
- `scored: false`;
- `sealed_for_later_evaluation: true`.

Later A-TEXT evaluation MUST consume these exact hashes. It may not regenerate failed-looking or
difficult outputs.

## Stop boundaries

If one route has an infrastructure ambiguity:
- persist it;
- retries 0;
- stop that route;
- the other route may proceed if budget remains safe.

If a normal provider refusal/error is scientifically/operationally settled:
- persist it as its trial;
- no retry.

Do not score any generated image in this task.

## Spend

Current cumulative paid qualification spend:
- USD 1.3037905.

Nominal A-TEXT generation max:
- USD 0.904.

Prospective combined consumed amount at nominal generation prices:
- USD 2.2077905.

This remains below the standing USD 10 EMP-001 total ceiling.

A-TEXT generation-only may run now.
A-TEXT **evaluation** remains blocked pending qualified evaluator coverage and Controller-approved
handoff.
