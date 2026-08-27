# EVAL-024 — Parallel A-TEXT Generation-Only

**Authority:** `coordination/decisions/CONTROLLER-EMP-001-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md`  
**Max nominal generation spend:** USD 0.904  
**Retries:** 0

## Objective

Generate and seal the frozen 16 A-TEXT images now, in parallel with evaluator qualification, without
scoring or interpreting them.

Do not weaken the existing scored A-TEXT handoff. Add a separate `generation-only` path.

## Required zero-spend verification first

- existing EMP-001 tests stay green;
- generation-only path refuses config drift;
- no evaluator can be constructed/called from generation-only mode;
- duplicate sealed trial coordinates refuse regeneration;
- ambiguous dispatch persists an Attempt and conservative spend;
- successful fake-live makes 16 generation attempts and 0 evaluator attempts;
- manifest/artifact tampering is detectable;
- Registry remains empty.

If green, run live using the existing persistent EMP-001 authorisation/ledger.

## Frozen live shape

4 strings × 2 repeats × 2 routes = 16 max.

IMG-01:
- fal `openai/gpt-image-2`
- 1024×1024
- medium
- 8 unseeded
- USD 0.053/image planning price

IMG-02:
- fal `fal-ai/ideogram/v3`
- BALANCED
- 8 unseeded
- USD 0.060/request

No retries. No evaluator. No scoring.

Persist:
- generation attempt/trial;
- provider request identity;
- exact prompt/string;
- route config/version;
- artifact;
- artifact SHA;
- billing state/cost;
- trial coordinate;
- `generated_unscored` state;
- sealed generation-only manifest.

Stop after generation. Return exact evidence paths, artifact hashes, spend and ledger delta.
Do not merge automatically.
