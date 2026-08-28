# Controller — Context Architecture Migration Integration — 2026-08-28

## Status

**ACCEPTED AND MERGED.**

Integration:
- PR #56
- merge commit `cb53d1405d6aebbe07b4d48e36780abc6cd55e08`

This decision records the durable Controller disposition for the cross-project context-architecture migration that was assigned directly by the user/Controller and implemented on branch `claude/os-migration-impl-exe9d6`.

## Objective

Reduce unnecessary agent context/time growth **without reducing correctness, scientific rigor, evidence integrity, or fresh-agent reconstructability**.

The governing principle is:

> Use the smallest context sufficient to act correctly, and expand context whenever authority, dependency, evidence, ambiguity or integrity requires it. Correctness always outranks context efficiency.

## Accepted operating model

### Typed authority

Different questions retain different authorities:

- empirical/factual claims → committed evidence/artifacts and deterministic checks over them;
- strategic/authorisation claims → durable Controller decisions;
- current operational synthesis → `coordination/CONTROL-STATE.md`;
- navigation/bootstrap → `PROJECT-MEMORY.md`.

No single linear precedence rule replaces this typed model.

### Progressive retrieval

All roles inherit `shared/CONTEXT-SUFFICIENCY-POLICY.md`.

Workers start from bounded context and MUST expand when the policy's triggers fire. If sufficient authority cannot be established, they stop with `STOP — CONTEXT_INSUFFICIENT` rather than guess.

### Startup

Default worker bootstrap is now:
1. `PROJECT-MEMORY.md`;
2. `coordination/CONTROL-STATE.md`;
3. `coordination/PROJECT-CONTRACT.md`;
4. `shared/COMMUNICATION-STANDARD.md`;
5. `shared/CONTEXT-SUFFICIENCY-POLICY.md`;
6. stream charter;
7. assigned task;
8. task Context Contract dependencies;
9. expansion as required.

Stream `HANDOFF.md` files are no longer mandatory startup reading.

### Project memory/state

- `PROJECT-MEMORY.md` remains the canonical entry map, but is compact rather than an historical diary.
- `CONTROL-STATE.md` is the primary current operational-state synthesis.
- pre-migration versions of both are preserved byte-for-byte under `history/`.
- `history/**` is Governor-maintained **project-wide derived narrative only**; it never owns domain evidence.
- `WORKSTREAM-STATUS.md` remains a derived convenience view and is not mandatory startup reading.

### Task context contract

`shared/templates/TASK-TEMPLATE.md` now requires:
- base state;
- required orientation;
- task-specific context;
- justified broad reads;
- expansion triggers;
- evidence handling level;
- explicit context-insufficiency behavior.

Broad reads remain allowed when genuinely required; they are not forbidden.

### Evidence handling

The accepted rule is **compute first, load second**:
- use deterministic validators/calculations for small invariants from large evidence;
- load raw evidence when the task actually requires the observations, an integrity issue exists, a relevant dependency changed, or a deep audit is running.

Raw evidence remains authoritative.

### Verification

Routine verification is dependency-triggered.

Previously accepted evidence does not need full recomputation when evidence bytes, governing contract, validator/scorer and relevant interpretation are unchanged.

Full recomputation is required when those dependencies change, integrity fails, a result is disputed, or a Level-3 audit is deliberately invoked.

### Governor modes

The Governor now has:
- **Level 1** — task/PR integrity review, dependency-bounded;
- **Level 2** — state reconciliation, previous accepted Governor SHA → current main delta;
- **Level 3** — deliberate deep audit with broad independent recomputation.

GOV-006-style work remains available but is no longer the implied default for ordinary reviews.

### Parallel Controller sessions

Controller sessions operate as:
- **WRITER** — may mutate durable programme state, authorise/cancel/defer tasks and merge;
- **ADVISORY** — may inspect, challenge, research, plan and draft, but does not mutate durable programme state.

Only one Writer Controller should operate at a time. This serialises strategic-state mutation, not domain execution.

## Quality gate

Worker-reported migration checks:
- genuinely fresh zero-context reconstruction test: **22/22 correct**;
- only 3 context expansions;
- no historical narrative required;
- deliberate stale-defect fixture was blocked by a routine Level-1 review;
- listed validators/tests green.

Controller independently verified:
- archived pre-migration `PROJECT-MEMORY.md` is byte-for-byte identical in content to the prior main version;
- archived pre-migration `CONTROL-STATE.md` is byte-for-byte identical in content to the prior main version;
- no Canon/Eval/Resources scientific artifact or empirical result was modified by the migration diff;
- key quality-critical facts remain navigable from the compact bootstrap;
- the branch was based on unchanged current main before merge.

Measured generic bootstrap reduction before task-specific context:
- Eval: ~151,015 chars → ~51,049 chars (**66.2% reduction**);
- Canon: ~130,821 → ~51,381 (**60.7% reduction**);
- Resources: ~138,930 → ~53,873 (**61.2% reduction**).

These are context-size measurements, not hard future caps. Correctness remains the gate.

## Controller corrections made before merge

1. Defined ownership of top-level `history/**` so the new archive has a maintainable owner without becoming domain authority.
2. Restored an explicit compact-map statement that exact-text imperfection is **not a programme-wide blocker**.
3. Strengthened `verify/verify_sealed_evidence.py` so A-TEXT scoring must match the exact sealed generation coordinate set, artifact hashes, byte lengths, relative paths and generation fingerprint, in addition to headline arithmetic.

## Boundaries preserved

This migration does **not** change:
- product definition or CpAO;
- Normalized Request / Creative IR / Production IR separation;
- scientific or empirical results;
- Capability Registry admission semantics;
- model/evaluator results;
- spend authority;
- current task dispositions;
- Stage-A/B/C scientific design;
- Production IR / Planner status.

## Follow-up posture

Do not immediately perform another large documentation cleanup.

Use the new operating model on real tasks and measure:
- generic bootstrap/context size;
- context expansions and why;
- task wall time;
- missed dependencies or stale-state incidents;
- Governor review cost.

If quality degrades, expand the default context or fix navigation. Token reduction is not success unless integrity remains intact.

No GOV-007 is authorised by this decision.
