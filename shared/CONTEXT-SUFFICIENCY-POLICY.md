# Context Sufficiency / Progressive Retrieval Policy

**Applies to every worker, every stream, the Controller and the Governor.**
Adopted 2026-08-28 as part of the context-architecture migration. This policy governs *how agents
obtain context*; it changes no scientific result, no task authorisation and no project decision.

## The principle

> **Use the smallest context sufficient to act correctly, and expand context whenever authority,
> dependency, evidence, ambiguity or integrity requires it. Correctness always outranks context
> efficiency.**

Context begins deliberately bounded: the default bootstrap in `coordination/RUNBOOK.md` plus the
assigned task's Context Contract. It does not stay bounded when correctness needs more.

**Priority order, explicit:**

> Correctness → authority completeness → evidence integrity → context efficiency.

A smaller context that produces worse work is a failure. A larger context that is genuinely required
for correctness is correct behaviour, not a violation of this policy.

## Responsibility

A worker is responsible for **context sufficiency**, not merely for reading a checklist. Having read
every file the task names does not discharge this responsibility; the worker must judge whether what
it has read is sufficient to act correctly, and expand when it is not. "The task didn't tell me to
read it" is never a defence for acting on incomplete authority.

## Typed authority — which kind of source answers which kind of question

Different authority types answer different questions. Do not substitute one for another.

| Question | Authority |
|---|---|
| **What actually happened?** (factual/empirical claims) | Committed evidence/artifacts, and deterministic validators/calculations over that evidence. |
| **What are we allowed to do? What decision governs? Is a task cancelled, deferred or authorised?** | Explicit durable Controller decisions (discovered under `coordination/decisions/` and stream decision records). |
| **What work is open, blocked, deferred now? What is the next gate?** | `coordination/CONTROL-STATE.md` — a synthesis/navigation surface backed by Controller decisions. |
| **What is this project and where do I find the authority?** | `PROJECT-MEMORY.md` — a map to authority, not a replacement for it. |

Two consequences worth spelling out:

- An empirical artifact cannot authorise anything. A 7/16 scoring result is established by its
  sealed evidence; whether that result may populate the Registry is established only by a Controller
  decision — and the Controller has ruled it may not.
- A synthesis document (`CONTROL-STATE.md`, `PROJECT-MEMORY.md`, `WORKSTREAM-STATUS.md`) never
  outranks the evidence or decisions it summarises. If they disagree, the underlying authority wins
  and the synthesis is defective — report it, do not argue from it.
- **Newer durable Controller decisions govern over stale prose**, including task files, handoffs and
  older decisions they supersede.

## Mandatory expansion triggers

The worker MUST read beyond its initial context when any of the following holds:

1. an authoritative artifact references another dependency needed to interpret it correctly;
2. a frozen contract or schema is involved in the work;
3. a referenced decision may have been superseded by a newer one;
4. evidence conflicts with prose;
5. two current-state documents disagree;
6. a cross-stream dependency matters to the task;
7. a historical baseline could be modified by the work;
8. a validator or check fails;
9. a relevant upstream dependency changed since the accepted base the task names;
10. authorisation is unclear — including whether the task itself is still authorised;
11. execution would otherwise require guessing;
12. the task crosses an ownership boundary;
13. a scientific conclusion depends on underlying row-level/raw evidence rather than only a stored
    aggregate.

A task's Context Contract may add task-specific triggers; it can never remove these.

## Insufficient context — stop and route, never guess

If, after expanding, context sufficiency still cannot be established, stop with:

```
STOP — CONTEXT_INSUFFICIENT
```

and return:

- **what is missing**;
- **why it matters** for this task;
- **what authority/file is needed** to resolve it;
- **whether work completed so far remains valid**.

Never guess to preserve a context budget. Never treat "I could not find the authority" as "no
authority exists."

## Large evidence: COMPUTE FIRST, LOAD SECOND

When a task needs a small invariant from large machine-readable evidence, do **not** load the entire
evidence file into model context by default. Run the deterministic validator or a small
deterministic calculation over it first, and reason over the result (counts, rates, hashes) with the
source path and hash named. `verify/VALIDATOR-INDEX.yaml` maps important evidence families to their
verification commands.

**Raw evidence remains authoritative.** This is context reduction through computation, not evidence
replacement. Load the raw evidence when:

- the task concerns the actual observations themselves;
- the result is disputed;
- a validator fails;
- evidence integrity is under audit;
- the scorer, contract or evidence changed;
- a deep audit is running;
- qualitative failure analysis requires specific rows.

## Evidence handling levels

Tasks declare how deep into evidence they must go (see the Context Contract in
`shared/templates/TASK-TEMPLATE.md`):

| Level | Meaning |
|---|---|
| `state_only` | Current-state documents and decision records suffice; no evidence file is opened. |
| `validator_summary` | Run the named deterministic validators; reason over their output. |
| `aggregated_evidence` | Read committed aggregate/summary artifacts (manifests, result summaries), not row-level records. |
| `row_level_evidence` | Read specific row-level records the task or a finding requires. |
| `full_raw_evidence` | Load complete raw evidence — audits, disputes, integrity incidents, qualitative failure analysis. |

The declared level is a starting point, not a ceiling: any mandatory expansion trigger above moves
the worker to a deeper level. It is a ceiling in one direction only — do not load deeper evidence
than the task needs without a trigger.

## Verification is dependency-triggered, not ritual

For previously accepted empirical evidence, routine work does **not** recompute the entire
experiment when ALL of these are unchanged since acceptance:

- the evidence bytes;
- the governing contract;
- the validator/scorer;
- the interpretation relevant to the current task.

In that case, verify the authority/fingerprint chain (hashes match, the decision record exists and
is not superseded) and proceed.

Fully recompute the affected evidence when any of these holds:

- evidence bytes changed;
- the validator/scorer changed;
- the contract changed;
- a threshold changed;
- the interpretation changed;
- integrity verification fails;
- the result is disputed;
- a deep audit is deliberately invoked.

Random spot-checking is not the primary verification rule; changed dependencies are.

## What this policy must never cause

This policy is not a licence to miss things. The migration that introduced it is unacceptable if it
causes agents to miss: frozen contracts; Controller decisions; supersession; upstream dependencies;
schema changes; evidence needed for a scientific claim; historical baselines that must not be
mutated; cross-stream boundaries; spend/authorisation boundaries; cancelled work; or Registry
admission constraints. Every one of those is covered by a mandatory expansion trigger above — when
in doubt, expand; when still in doubt, stop and route.
