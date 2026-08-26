# EVAL-014 — EMP-001 Budget Continuity and Paid-Handoff Correction

**AUTONOMY:** autonomous  
**ENVIRONMENT:** Claude Code/cloud repository workspace  
**EXTERNAL SPEND:** **USD 0 / INR 0**  
**PROVIDER / MODEL / EVALUATOR CALLS:** **0**  
**BRANCH:** `work/eval-014-emp-001-budget-continuity`

## Objective

Close only the remaining spend-control and paid-stage-handoff defects identified in:

`coordination/decisions/CONTROLLER-EVAL-013-REVIEW-2026-08-27.md`

Preserve all valid EVAL-012/EVAL-013 implementation. This is not another research or architecture round.

The required end state is simple:

> after a future explicit user approval, qualification and A-TEXT can run in separate processes without ever resetting the approved USD 10 tranche spend, qualification can never consume more than its frozen USD 6 sub-cap, and a real qualified judge can be handed to A-TEXT without another code change.

## Read first

1. `PROJECT-MEMORY.md`
2. `shared/COMMUNICATION-STANDARD.md`
3. `coordination/CONTROL-STATE.md`
4. `coordination/decisions/CONTROLLER-EVAL-013-REVIEW-2026-08-27.md`
5. `coordination/decisions/CONTROLLER-FIRST-EMPIRICAL-TRANCHE-PREPARATION-2026-08-26.md`
6. `coordination/plans/2026-08-26-FIRST-EMPIRICAL-TRANCHE-PROPOSAL.md`
7. `eval/empirical-tranche-1/` from EVAL-013 returned head `2b83efd15c1f0fb26d6e7ca8bfbe542071abf577`
8. Resources topology / one-call-one-trial persistence contract already merged on main.

## Fixed Controller decisions — do not reopen

- EMP-001 total consumed-API ceiling remains **USD 10.00**.
- Text-judge qualification sub-cap remains **USD 6.00** inside that total.
- Retries remain **0**.
- No account pre-funding above the approved ceiling.
- Scientific roster, prompts, thresholds and routes remain unchanged.
- Qualification remains Devanagari first; Latin only for survivors.
- Latin human perceptibility review remains a required zero-spend prerequisite before the Latin paid leg.
- A-TEXT remains exactly four items × two repeats × two routes = **16 generations maximum**.
- IMG-01 remains fal `openai/gpt-image-2`, 1024×1024 medium.
- IMG-02 remains fal `fal-ai/ideogram/v3`, BALANCED.
- Primary A-TEXT exactness remains blind transcription + code equality.
- Customer-outcome CpAO remains forbidden here.
- No external call is authorised by this task.

## Required corrections

### E14-A — Persistent cumulative tranche budget

Replace process-local-only spend enforcement with a durable runtime spend state/ledger that survives separate qualification and A-TEXT invocations.

Requirements:
- runtime spend state is gitignored and never committed;
- every paid call reserves against both the persisted EMP-001 total and its applicable stage cap before dispatch;
- recorded actual/provisional billed amount is appended/committed atomically to the runtime spend ledger after the call;
- reopening a process reconstructs cumulative spend from the ledger/state rather than resetting to zero;
- no negative correction may manufacture headroom; corrections are additive ledger records with explicit type;
- concurrent/double-start behaviour must fail closed or lock safely; do not permit two processes to reserve the same remaining headroom;
- the total consumed ceiling can never exceed USD 10.00;
- qualification can never exceed USD 6.00 even when the authorisation file says USD 10.00;
- A-TEXT may consume only remaining tranche headroom after qualification.

Required positive/negative controls:
1. process A spends simulated USD 5.75 on qualification, closes; process B reopens and sees USD 4.25 total headroom, not USD 10;
2. qualification next-call reservation is refused at the USD 6 sub-cap even with total tranche headroom remaining;
3. A-TEXT next-call reservation is refused if qualification + A-TEXT would exceed USD 10;
4. deleting/replacing the authorisation file does not erase prior spend state for the same tranche/run id;
5. a second simultaneous writer cannot double-reserve remaining headroom;
6. malformed/corrupt spend state fails closed.

### E14-B — Durable evaluator trial/cost identity

Every live qualification evaluator dispatch must produce a durable unique trial identity and cost reference consistent with one-call-one-trial.

At minimum each call record must carry:
- `trial_id` unique within the EMP-001 run;
- `attempt_id` or equivalent topology-compatible attempt identifier;
- candidate provider/model alias/resolved version;
- script, item id, shape, pass/repeat index;
- provider request id when returned;
- API status / refusal / error;
- cost reference resolving to the persistent tranche spend ledger;
- retries = 0;
- evidence/synthetic mode.

Tests must prove 2,304 fake-live qualification dispatches yield 2,304 unique trial ids and 2,304 resolvable cost references when both fake candidates survive.

### E14-C — Executable paid qualification → A-TEXT handoff

`run_atex.py --live` must no longer unconditionally refuse when all legitimate inputs are supplied.

Implement a fail-closed CLI/orchestrator that:
1. consumes the actual persisted qualification result from the same EMP-001 run;
2. rejects dry-run/fake-live/synthetic qualification records;
3. requires a judge qualified for every script used by the four A-TEXT items;
4. reconstructs the exact same provider + alias + resolved version used in qualification;
5. opens that judge with provider-correct live transport and the persistent tranche budget;
6. constructs only the two frozen fal generation routes;
7. runs the existing A-TEXT live path;
8. writes evidence into the same run root/spend ledger;
9. keeps generation and evaluator calls as separate trials/cost records;
10. refuses if the Latin perceptibility gate is unresolved when Latin qualification/A-TEXT requires it.

No manual editing of a “qualified” JSON field may be enough to open A-TEXT. Bind the handoff to the real qualification run identity/fingerprint and its evidence records.

### E14-D — Same blind invariant in A-TEXT

When A-TEXT calls the primary judge, pass `item['target_string']` only as `blind_check_target` to the evaluator-side pre-dispatch check. It must never enter the transcribe payload.

Add a negative control for a Latin target leak as well as Devanagari.

### E14-E — Cross-process positive fake-live rehearsal

Add a zero-network rehearsal that runs the future lifecycle as separate invocations/process-equivalent steps:

1. create valid fake authorisation;
2. initialise persistent run/spend state;
3. fake-live qualification using the real orchestration and injected transports;
4. close/reopen budget state;
5. consume the persisted qualified-judge handoff;
6. fake-live A-TEXT using frozen fal route adapters + real judge orchestration behind injected transports;
7. verify cumulative spend did not reset;
8. verify total <= USD 10 and qualification <= USD 6;
9. verify 0 retries;
10. verify Registry remains unchanged;
11. verify every generation/evaluator call has unique trial/cost identity;
12. verify fake-live evidence remains explicitly non-promotable.

The rehearsal may use smaller fixture counts for a focused unit test, but the full fake-live controls for the frozen 2,304 qualification / 16 A-TEXT maxima must continue to pass.

## Verification before return

Freshly run and record:
- all `eval/empirical-tranche-1/tests/` tests;
- V1 harness self-test;
- Resources cross-branch validation;
- dry-run preflight;
- positive fake-live qualification;
- positive fake-live A-TEXT;
- new cross-process budget/handoff rehearsal;
- Registry zero check;
- protected-baseline SHA check.

No provider key may be used; no network/provider/model/evaluator call may occur.

## Required return

Create:

`eval/empirical-tranche-1/EVAL-014-BUDGET-HANDOFF-READINESS.md`

Return exactly:
1. verdict: `READY_FOR_SPEND_APPROVAL | BLOCKED`;
2. commit SHA;
3. exact tests/commands and results;
4. evidence that USD 10 total + USD 6 qualification sub-cap persist across separate processes;
5. evidence that paid qualification → paid A-TEXT handoff is executable without another code change;
6. remaining non-code prerequisites, including Latin human perceptibility review;
7. confirmation external calls = 0 and spend = 0.

Do not merge.
