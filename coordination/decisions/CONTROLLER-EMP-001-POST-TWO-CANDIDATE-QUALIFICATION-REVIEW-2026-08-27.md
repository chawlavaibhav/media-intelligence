# Controller EMP-001 Post-Two-Candidate Qualification Review — 2026-08-27

## Status
PROVISIONAL V1 GATE REVIEW TRIGGERED. A-TEXT REMAINS BLOCKED. NO NEW PAID CALLS AUTHORISED.

The qualification contract says its thresholds are PROVISIONAL_FIRST_RUN_GATE and must be revisited after the first two candidates complete full screens. That trigger is now met.

## Accepted complete-screen evidence

Haiku 4.5:
- 576 Devanagari calls
- 43 false passes
- 118 false fails
- match false-fail rate 0.4097
- repeat consistency 0.9271
- failed provisional v1 gate

Corrected Sonnet 5:
- 576 Devanagari calls
- 29 false passes
- 6 false fails
- match false-fail rate 0.0208
- refusal rate 0
- repeat consistency 0.9843
- zero errors / zero ambiguous dispatches
- failed only mismatch_false_pass under provisional v1 gate

Latin was not run. A-TEXT was not run.
Cumulative qualification spend: USD 0.3112678.

## Controller disposition

Sonnet has failed the provisional v1 gate, but is not permanently rejected until the contract's required calibration review is complete.

The contract states transcribe is the blind primary shape and verdict is target-aware diagnostic. The current scorer pools both shapes when computing the gate metrics. Before changing any threshold, we must determine whether the 29 Sonnet false passes come from the primary transcribe shape, the diagnostic verdict shape, or both.

## Zero-spend review required

Using only persisted evidence for Haiku and corrected Sonnet:
- split false passes, false fails, refusals and repeat consistency by transcribe vs verdict;
- enumerate false-pass item IDs, passes and failure classes;
- compute unique-item false-pass rate as well as call-level count;
- build transcribe-vs-verdict disagreement counts for the same item/pass;
- assess whether pooling the diagnostic verdict shape into the qualification gate is consistent with the contract semantics.

Do not change thresholds during this analysis.
Make zero provider/model/evaluator calls and spend USD 0.

Until Controller review:
- Sonnet not qualified;
- Latin blocked;
- A-TEXT blocked;
- Gemini unresolved;
- Registry unchanged.
