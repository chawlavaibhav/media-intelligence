# EVAL-030 — A-TEXT Benchmark Scoring

**Owner:** Eval worker  
**Authority:** `coordination/decisions/CONTROLLER-EVAL-030-ATEXT-BENCHMARK-SCORING-2026-08-28.md`  
**Max external spend:** USD 0.024  
**Retries:** 0

## Objective

Score the exact 16 merged EVAL-024 A-TEXT artifacts using the merged EVAL-029 benchmark-grade Cloud Vision OCR evaluator.

Do not generate anything.

## Read first

- `PROJECT-MEMORY.md`
- `coordination/PROJECT-CONTRACT.md`
- `shared/COMMUNICATION-STANDARD.md`
- `coordination/CONTROL-STATE.md`
- `coordination/decisions/CONTROLLER-EVAL-030-ATEXT-BENCHMARK-SCORING-2026-08-28.md`
- `eval/empirical-tranche-1/atex/sealed-generation-v1/atex-generation-only-manifest.json`
- `eval/empirical-tranche-1/evidence/EMP-001/text-ocr/EVIDENCE-MANIFEST.json`
- `eval/empirical-tranche-1/ATEXT-BENCHMARK-SCORING-HANDOFF.md`

## Required execution

1. Verify all 16 artifact hashes against the merged EVAL-024 manifest before scoring.
2. Score each artifact once with Cloud Vision `TEXT_DETECTION`, no language hints.
3. Target text must never be sent to the evaluator.
4. Retries 0.
5. Compare OCR output to the frozen target with NFC + outer-whitespace trim and exact equality.
6. Use the existing persistent EMP-001 ledger.
7. Persist all per-artifact results and the bounded cost/evaluator evidence needed for a fresh clone to recompute aggregates.
8. Aggregate by route and script.
9. Carry evaluator qualification error rates/statuses with every reported metric.

## Stop/refuse

- any artifact hash mismatch;
- missing artifact;
- config/evaluator identity drift;
- budget refusal;
- ambiguous post-dispatch failure: persist/count conservatively and stop fail-closed;
- any attempt to regenerate or substitute.

## Forbidden

- human review;
- image regeneration;
- prompt changes;
- new OCR qualification;
- Registry population;
- full Stage-A expansion.

## Return

Report:
- branch/head;
- tests/preflight;
- 16 coordinate dispositions;
- per-route exact-match counts/rates;
- per-script breakdown;
- OCR transcriptions;
- evaluator spend;
- A-TEXT generation+evaluation spend;
- evidence paths/hashes/fingerprint;
- proof no generation call;
- proof Registry unchanged;
- git status.

Push, do not merge.
Return to Controller.
