# Task EVAL-031: Local Stage-Q and Stage-A harness closure

**TASK ID:** EVAL-031  
**AUTONOMY MODE:** autonomous  
**RESOURCE BUDGET:** USD 0 / INR 0 external spend. No provider/model/evaluator API calls.

## Objective

Use only committed repository material and local deterministic execution to close as much of the Stage-Q/local-execution bottleneck as is scientifically honest.

This lane combines the two local/no-acquisition areas that share the same execution substrate:
1. Family-2 deterministic CV / geometry readiness and screening;
2. Q7 operational-logging verification plus Stage-A provider-agnostic harness rehearsal.

This task must produce executable evidence/readiness, not another broad design document.

## Read first

- PROJECT-MEMORY.md
- shared/COMMUNICATION-STANDARD.md
- coordination/PROJECT-CONTRACT.md
- coordination/CONTROL-STATE.md
- eval/v1/instruments/QUALIFICATION-MASTER-SPEC.md
- eval/v1/instruments/FAMILY-2-DETERMINISTIC-CV.md
- eval/pre-execution-integration/STAGED-EXECUTION-PLAN.yaml
- eval/v1/harness/**
- eval/registry/**

Newer durable Controller decisions govern over stale prose.

## Work

### A. Deterministic sub-instruments

Mechanically verify the file/metadata probes that the frozen instrument contract classifies as `deterministic`, including fail-closed behavior on corrupt/unparseable input.

Produce durable records showing exactly which capabilities/subchecks can legitimately carry `deterministic` instrument status without a learned detector.

Do not generalise deterministic status to detector-based counting/positioning.

### B. Geometry detector screening, not qualification

The 102-item CV fixture pack already exists.

- identify a small bounded set of local/open detector approaches suitable for the frozen geometry judgements;
- implement/configure them reproducibly;
- run **screening only** on the fixture pack;
- report count, position/relation, attribute-binding and negative-control behavior separately;
- record exact versions/configuration/confidence;
- characterise false-pass/fail-closed failures.

Also propose:
- one preferred detector/configuration for later qualification;
- a declared colour space and tolerance with rationale.

**Hard stop:** do not label any learned detector `qualified`. Controller approval of the final configuration/tolerance is required before qualification.

### C. Q7 operational logging + Stage-A harness rehearsal

Using only fake/local adapters:

- verify the operational-logging checks against real committed harness/run-record shapes;
- exercise the exact Stage-A 90-generation orchestration shape without external calls;
- verify per-slot repeat grouping, declared seed-policy plumbing, artifact lineage, cost refs, fail-closed error semantics, resume behavior and Registry admission guards;
- do not invent unverified provider adapters or prices;
- produce an exact adapter/configuration gap list for a live Stage-A run.

## Deliverables

Create:
- `eval/findings/EVAL-031-LOCAL-STAGE-Q-HARNESS-RESULT.md`
- machine-readable screening/verification evidence under `eval/runs/EVAL-031/`
- any narrow Eval-owned code/tests needed.

Return:
- deterministic sub-instruments verified;
- detector screening ranking and failures;
- proposed detector/config + colour tolerance (PROPOSED only);
- operational-logging result;
- Stage-A fake-live rehearsal result;
- exact remaining blockers to a live Stage-A run.

## Restrictions

No external calls. No spend. No Registry rows from synthetic/fake measurements. No detector qualification. No threshold promotion. No architecture changes. Do not edit Canon/Resources/coordination current-state files.

Commit and push to `work/eval-031-local-stage-q-harness`. Do not merge.