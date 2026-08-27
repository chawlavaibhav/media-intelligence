# Controller EVAL-020 — Primary-Shape Qualification and Evidence Persistence — 2026-08-27

## Status

**ZERO-SPEND INSTRUMENT CORRECTION PREPARED. DO NOT RUN PAID QUALIFICATION UNTIL FOCUSED TESTS PASS.**

## Finding

The post-two-candidate review established two defects in the v1 qualification instrument:

1. The contract declared blind `transcribe` as the primary measurement and target-aware `verdict`
   as diagnostic, but the scorer pooled both shapes into the pass/fail gates.

2. Per-call scoring observations were computed in memory and discarded, so the contract-mandated
   calibration review could not reconstruct shape-specific false passes, false fails, response text,
   failure classes, unique failing items or transcribe-vs-verdict disagreement.

A third handoff defect was found during this review:

3. Live qualification wrote the CLI output file but did not automatically persist the canonical
   fingerprint-bound `qualification-result.json` consumed by A-TEXT.

## Scientific disposition of prior runs

The old Haiku and corrected Sonnet-v2 complete screens remain valid historical evidence about the
**v1 pooled instrument**, but they cannot be treated as final qualification/disqualification under
the contract-corrected instrument.

Therefore:
- Haiku's prior "disqualified" status is downgraded to **failed pooled v1 provisional gate**.
- Sonnet v2 remains **failed pooled v1 provisional gate**.
- Neither old result may open A-TEXT under EVAL-020.
- No old evidence is deleted or rewritten.

## Contract v2

Create `qualification-contract-v2.yaml` and leave v1 untouched as history.

Numerical thresholds are unchanged:
- mismatch false pass max = 0;
- match false-fail rate max = 0.10;
- refusal rate max = 0.05;
- repeat consistency min = 0.95.

Semantic correction:
- `transcribe` is the only qualifying shape;
- `verdict` remains mandatory diagnostic coverage but its accuracy metrics cannot pass or fail the
  candidate;
- a complete run still executes both shapes unless stopped by an authorised fail-closed condition.

This is not threshold relaxation and is not chosen to make Sonnet pass.

## Evidence persistence

Every scored observation must be persisted with enough information to perform the review the
contract requires, including:
- item id;
- shape;
- repeat/pass;
- expected label;
- observed label;
- API status;
- target;
- rendered string;
- failure class/group/edit detail where present;
- evaluator response text.

The result must expose:
- primary-shape gate metrics;
- metrics by shape;
- pooled diagnostics;
- unique false-pass item count;
- raw observations.

## Handoff integrity

The qualification fingerprint must bind:
- qualified claim;
- candidate results including observations;
- provider call records;
- qualification contract hash.

A-TEXT must reject qualification evidence produced under a different contract version or hash.

Live qualification must automatically persist the canonical `qualification-result.json`.

## Next empirical run

After focused zero-spend verification is green, run **Sonnet 5 only** from Devanagari call 1 under
contract v2.

Use:
- `claude-sonnet-5`;
- `thinking: {"type":"disabled"}`;
- same batteries, images, prompts, repeats and numerical thresholds;
- retries 0;
- same persistent EMP-001 ledger;
- no Gemini or Haiku rerun.

Already-counted qualification spend: USD 0.3112678.

Conservative maximum reservation for a fresh two-script Sonnet run: USD 5.345280.

Cumulative worst case: **USD 5.6565478**, below the existing user-approved USD 6 qualification
sub-cap.

If Sonnet fails the v2 primary Devanagari gate, stop and return the evidence.
If it passes Devanagari, run Latin automatically.
If it passes both scripts, stop before A-TEXT and return to Controller.

No new user spend approval is required because the existing bounded approval still contains the
worst case.

## Verification required before paid rerun

Zero-spend only:
- text qualification tests;
- provider/live qualification tests touching the changed path;
- A-TEXT handoff tests;
- preflight;
- confirm no network/provider calls;
- confirm prior evidence files remain byte-identical.
