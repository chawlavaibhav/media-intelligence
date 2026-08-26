# EVAL-012 — EMP-001 Zero-Spend Implementation and Preflight

**AUTONOMY:** autonomous  
**ENVIRONMENT:** Claude Code/cloud repository workspace  
**EXTERNAL SPEND:** **USD 0 / INR 0**  
**PROVIDER / MODEL / EVALUATOR CALLS:** **0**  
**BRANCH:** `work/eval-012-emp-001-zero-spend`

## Objective

Implement and execute the **zero-spend portion of EMP-001** so that the next Controller decision is about whether to authorise actual empirical calls, not whether the harness is ready.

This is implementation/preflight, **not another research round**.

The authoritative proposal and implementation plan already exist:

- `coordination/decisions/CONTROLLER-FIRST-EMPIRICAL-TRANCHE-PREPARATION-2026-08-26.md`
- `coordination/plans/2026-08-26-FIRST-EMPIRICAL-TRANCHE-PROPOSAL.md`
- `docs/superpowers/plans/2026-08-26-first-empirical-tranche.md`

Execute only the plan steps that can be completed with **zero external spend and zero provider/evaluator/model calls**.

## Read first

1. `PROJECT-MEMORY.md`
2. `shared/COMMUNICATION-STANDARD.md`
3. `coordination/CONTROL-STATE.md`
4. `coordination/decisions/CONTROLLER-PRE-EXECUTION-CLOSURE-2026-08-26.md`
5. `coordination/decisions/CONTROLLER-FIRST-EMPIRICAL-TRANCHE-PREPARATION-2026-08-26.md`
6. `coordination/plans/2026-08-26-FIRST-EMPIRICAL-TRANCHE-PROPOSAL.md`
7. `docs/superpowers/plans/2026-08-26-first-empirical-tranche.md`
8. `eval/pre-execution-integration/STAGED-EXECUTION-PLAN.yaml`
9. existing V1 harness / persistence contracts under `eval/v1/harness/`

## Fixed Controller decisions — do not reopen

- EMP-001 is text-first and gated; it is **not** the full 90-generation Stage A.
- Stage-Q model generations remain exactly **0**.
- No external call of any kind is authorised by this task.
- Proposed later consumed-API ceiling remains **USD 10**, but this task does not authorise it.
- Retries authorised: **0**.
- Frozen Devanagari 96-item validated battery remains untouched.
- New Latin qualification material must be a separate 96-item pack: 48 match + 48 controlled mismatch.
- `transcribe` and `verdict` remain separate evaluator shapes.
- A-TEXT items are frozen to:
  1. `शुभ दीपावली`
  2. `आज की डील`
  3. `Aaj ki Deal`
  4. `SAVE 20% • ₹999`
- Future A-TEXT generation ceiling remains 16 total: 8 IMG-01 + 8 IMG-02.
- Synthetic/dry-run evidence must never populate the empirical Registry.
- One provider/API call = one trial.
- No customer-outcome CpAO may be reported here.

## Required execution

Follow `docs/superpowers/plans/2026-08-26-first-empirical-tranche.md` using test-first implementation. Complete all zero-spend prerequisites that can be honestly executed in the repository environment.

### E12-A — Authorisation and budget guard

Implement the EMP-001 configuration, disabled authorisation example, and fail-closed budget guard exactly as specified by the implementation plan.

Required negative controls:
- missing/false authorisation cannot make a paid call;
- zero/negative authorised ceiling is rejected;
- a next-call reserve that could exceed the ceiling is rejected before network dispatch;
- recorded spend can never silently exceed the ceiling;
- retries remain zero.

No secrets may be committed.

### E12-B — Separate Latin qualification pack

Build and freeze the separate 96-item Latin exact-text pack required by EMP-001.

Requirements:
- exactly 48 match + 48 mismatch;
- exactly one controlled mismatch opportunity per base string;
- controlled failure classes only;
- truth known by construction;
- deterministic serialization and SHA-256 fingerprint;
- a perceptibility sanity record;
- no write to or mutation of the frozen Devanagari battery.

If an actual human perceptibility review cannot be honestly performed in the worker environment, do **not** fabricate one. Produce the pack and mark that review as a precise remaining zero-spend human prerequisite.

### E12-C — Q1/Q7 / persistence preflight

Execute the existing harness self-tests and cross-branch validation called for by the implementation plan.

Then implement/run the EMP-001 preflight with network disabled.

It must prove at minimum:
- geometry fixture count = 102;
- existing persistence/harness checks are green;
- Capability Registry empirical row count remains 0;
- one-call-one-trial invariant is preserved;
- retries authorised = 0;
- no external network access is required for `--dry-run`;
- disabled/missing authorisation blocks any real adapter path.

Record exact commands, exit codes and test counts. Do not summarize a test as passing unless it was actually executed in this branch.

### E12-D — Provider adapter scaffolding, no calls

Implement the provider-adapter/request-builder scaffolding from the implementation plan **without invoking any external provider**.

Use fake/injected transports for tests.

Required checks:
- constructors make no network calls;
- blind `transcribe` payload does not contain the target string;
- target-visible `verdict` payload contains the target only where specified;
- model alias and exact resolved version fields are separate;
- provider request id/token/cost/refusal/error fields can be persisted;
- no API key is read during dry-run/import tests.

Do not claim current provider availability from this implementation task; current public-source planning evidence remains in the EMP-001 planning artifacts until real execution pins the exact version.

### E12-E — Freeze A-TEXT local manifest and dry-run

Materialise the four frozen A-TEXT items locally and implement the gated runner in dry-run/fake-transport mode.

The dry run must demonstrate:
- 4 items × 2 repeats × 2 routes = 16 maximum future generations;
- no seed is supplied for these unseeded repeats;
- no retry path exists;
- output attempt/artifact/measurement shapes can be persisted;
- fake/synthetic results cannot enter Registry;
- if no qualified text judge exists, the real-generation gate remains closed.

### E12-F — Readiness return

Create:

`eval/empirical-tranche-1/EVAL-012-ZERO-SPEND-READINESS.md`

Return an evidence-backed verdict exactly:

`READY_FOR_SPEND_APPROVAL | BLOCKED`

If READY, state precisely what remains before the first call:
- explicit user approval of the USD 10 consumed-API ceiling;
- runtime secrets/accounts;
- exact provider/model snapshot pinning at execution;
- any zero-spend human perceptibility item still outstanding.

If BLOCKED, identify the exact failing test/invariant/material and the smallest correction required. Do not broaden the task.

## Verification before return

Run the full relevant test suite from the implementation plan, not only the newest tests. At minimum:

- existing V1 harness self-test;
- existing cross-branch validation;
- all new `eval/empirical-tranche-1/tests/` tests;
- dry-run preflight with network disabled;
- a final check that `eval/registry/registry-v1.jsonl` has no empirical rows;
- a final check that frozen V1/Devanagari baselines were not modified.

Commit and push all work to:

`work/eval-012-emp-001-zero-spend`

Do not merge it.

## Return to Controller

Return only:

1. verdict;
2. commit SHA;
3. exact tests/commands run and results;
4. zero-spend artifacts built;
5. remaining blockers/prerequisites;
6. confirmation that external calls = 0 and spend = 0;
7. whether the repository is ready for explicit EMP-001 spend approval.
