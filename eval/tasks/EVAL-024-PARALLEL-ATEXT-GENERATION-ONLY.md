# EVAL-024 — Parallel A-TEXT Generation-Only

**Owner:** Eval worker  
**Authority:** `coordination/decisions/CONTROLLER-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md`  
**External spend:** bounded by existing EMP-001 USD 10 total ceiling  
**Evaluation:** NOT authorised in this task

## Objective

Generate and seal the frozen 16 A-TEXT image artifacts now, while evaluator qualification continues
in parallel.

Do not score them.

## Frozen inputs

Strings:
- `शुभ दीपावली`
- `आज की डील`
- `Aaj ki Deal`
- `SAVE 20% • ₹999`

Routes:

IMG-01:
- fal `openai/gpt-image-2`
- 1024×1024
- medium
- 2 repeats per string
- 8 total
- unseeded
- planning price USD 0.053/image

IMG-02:
- fal `fal-ai/ideogram/v3`
- BALANCED
- 2 repeats per string
- 8 total
- unseeded
- planning price USD 0.060/request

Max planned:
- 16 generation calls
- nominal USD 0.904
- retries 0

## Implementation

Prefer reusing the existing A-TEXT generation adapters/persistence code rather than creating a
second provider integration.

Add a generation-only orchestration mode/path that:
1. does not load evaluator qualification;
2. does not construct/call a text judge;
3. still uses existing EMP-001 authorisation, `TrancheRun`, total-stage budget and persistent ledger;
4. persists each generation attempt under one-call-one-trial semantics;
5. preserves ambiguous-dispatch accounting;
6. writes successful artifacts to a dedicated sealed generation-only directory;
7. writes a fingerprint-bound generation manifest;
8. cannot populate Registry;
9. cannot mark A-TEXT pass/fail.

## Manifest

The generation-only manifest must include:
- run/tranche id;
- exact frozen item set;
- route configs + identity;
- 16 planned coordinates;
- call records;
- successful artifact paths;
- SHA-256 of every successful artifact;
- missing/failed coordinates;
- provider request ids if available;
- per-call cost refs;
- total consumed generation cost;
- `scored: false`;
- `sealed_for_later_evaluation: true`;
- evidence fingerprint.

Later scoring must verify artifact hashes against this manifest before reading them.

## Zero-spend tests before dispatch

Prove with injected transports:
- exactly 16 planned calls;
- zero evaluator calls;
- retries 0;
- persistent total EMP-001 budget is used;
- missing/ambiguous generation persists correctly;
- manifest fingerprint tamper detection;
- scoring fields cannot be written;
- Registry untouched;
- historical evidence preserved.

Run affected tests + preflight before network.

If anything fails, stop before spend.

## Live execution

If zero-spend checks are green:
- run from exact tested/pushed head;
- use existing `FAL_KEY`;
- no evaluator/API judge calls;
- no model substitution;
- no retries;
- max nominal generation spend USD 0.904;
- preserve all artifacts exactly.

## Return

Report:
- branch/head;
- test/preflight results;
- exact route identities;
- 16 coordinate disposition;
- artifact hashes;
- failures/ambiguities;
- incremental generation spend;
- cumulative EMP-001 spend;
- manifest path/fingerprint;
- proof evaluator calls = 0;
- proof Registry unchanged;
- proof prior evidence preserved.

Do not merge.
Do not score.
