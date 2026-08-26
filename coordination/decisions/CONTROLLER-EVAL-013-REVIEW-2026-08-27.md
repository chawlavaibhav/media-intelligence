# Controller Review — EVAL-013 EMP-001 live-path correction

**Date:** 27 Aug 2026  
**Returned branch:** `work/eval-013-emp-001-live-path-correction`  
**Returned head:** `2b83efd15c1f0fb26d6e7ca8bfbe542071abf577`  
**Worker verdict:** `READY_FOR_SPEND_APPROVAL`  
**Controller verdict:** **BLOCKED — bounded budget-continuity / paid-handoff correction only**

## Accepted work

EVAL-013 successfully closes the five defects identified in the EVAL-012 Controller review:

1. real qualification orchestration now exists behind injectable transports;
2. OpenAI and Gemini transport/auth semantics are provider-specific;
3. frozen fal IMG-01 / IMG-02 route adapters exist;
4. non-dry-run A-TEXT uses a supplied qualified judge rather than `_fake_transcribe`, and synthetic labelling is no longer hard-coded true;
5. positive fake-live controls now exercise dispatch rather than only refusal paths.

Additional corrections discovered by EVAL-013 are accepted:
- live blind-check enforcement before evaluator dispatch;
- UTF-8 request serialisation so Devanagari leak checks are meaningful;
- corrected verdict-shape blindness rule.

Worker-reported fresh evidence is accepted as worker evidence, not independently rerun by Controller:
- 247 EMP-001 tests passed;
- V1 harness 107/107 passed;
- Resources cross-branch validation passed;
- positive fake-live qualification traversed 2,304 recorded dispatches with zero network calls;
- positive fake-live A-TEXT traversed 16 generation + 16 evaluator dispatches with zero network calls;
- Registry remained empty;
- 13 protected baselines remained byte-identical;
- external spend/calls remained zero.

Current official fal documentation independently confirms the implemented key convention: `FAL_KEY` and `Authorization: Key <key>` for Model API calls.

## Why READY_FOR_SPEND_APPROVAL is still rejected

The remaining defects are not scientific. They are spend-control and executable handoff defects.

### B6 — tranche spend is not cumulative across processes

`BudgetGuard.spent_usd` is in-memory. `qualify_text.py --live` opens a guard from the USD 10 authorisation, spends within that process, then exits. A later A-TEXT process can reopen the same authorisation with `spent_usd = 0`.

Therefore the nominal **USD 10 EMP-001 consumed-API ceiling is not mechanically cumulative across stages/processes**. Two individually compliant processes could consume more than the user-approved tranche ceiling.

The approved ceiling must be enforced against a persistent tranche spend ledger/state carried across qualification and A-TEXT.

### B7 — the frozen USD 6 evaluator sub-cap is not mechanically enforced

The EMP-001 freeze gives text-judge qualification a **hard USD 6.00 consumption cap inside the USD 10 tranche**.

`qualify_text.py --live` currently opens the general USD 10 authorisation guard. It does not impose the USD 6 qualification sub-cap. This violates the frozen tranche allocation even if the total USD 10 ceiling happened not to be crossed.

Both total and stage sub-cap must fail closed before dispatch.

### B8 — A-TEXT paid CLI handoff is still not executable

`run_atex.py --live` still unconditionally refuses. It has no CLI/runtime handoff that consumes a real, non-synthetic qualified-judge result, reconstructs/pins that same judge identity/version, opens the remaining persistent tranche budget, constructs the frozen fal routes, and runs the screen.

The underlying `run(...)` function is improved, but a user-approved execution still needs another code change/orchestrator before A-TEXT can actually run.

### B9 — evaluator qualification calls need durable per-call trial/cost identity

Live qualification currently records provider/model/item/script/pass/shape and `one_call_one_trial: true`, but the per-call record does not itself carry a durable unique trial id/cost reference suitable for the Resources one-call-one-trial evidence contract.

Before spend, every real evaluator call must be individually identifiable and cumulatively costed; an assertion flag is not a substitute for trial identity.

### B10 — A-TEXT primary live transcription should pass the target into the evaluator-side blind check

`TextJudge.transcribe` supports `blind_check_target`; qualification uses it. A-TEXT `_measure_artifact` currently calls `transcribe(image_bytes)` without the target. The request builder is structurally target-free, so this is defense-in-depth rather than evidence of an existing leak, but the same live blindness invariant should be enforced in both paths.

## Controller disposition

Do **not** merge EVAL-013 as execution-ready and do **not** request spend approval yet.

Preserve the EVAL-013 implementation and open exactly one correction lane, EVAL-014, based on its returned head.

EVAL-014 may only:
- persist cumulative tranche spend across processes/stages;
- enforce both the USD 10 tranche ceiling and USD 6 qualification sub-cap;
- implement the qualified-judge → A-TEXT paid CLI/orchestrator handoff;
- give every evaluator call durable unique trial/cost identity;
- make A-TEXT use the same target-aware blind pre-dispatch check;
- prove the above with zero-network positive/negative controls.

No scientific question, candidate, prompt, threshold, price assumption, route, repeat count, retry policy, A-TEXT item or budget may change.

The Latin human perceptibility review remains an outstanding zero-spend prerequisite for the Latin leg and is not to be fabricated.

## Spend posture

Still **not authorised**:
- any provider/model/evaluator call;
- any account funding;
- EMP-001 USD 10 spend;
- full Stage A or later stages.

External spend authorised for EVAL-014: **USD 0 / INR 0**.
