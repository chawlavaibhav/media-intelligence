# Autonomy Policy

**Principle: bounded autonomy, not unrestricted autonomy.**

## When a worker may run unattended

All of these must hold:
- objective is approved (a real task ID exists)
- method/protocol is frozen enough not to require judgement calls mid-run
- inputs are approved
- resource budget is explicit in the task
- stop conditions are explicit
- architecture does not need to change to complete it

## Mandatory STOP / escalation triggers

1. **ARCHITECTURE** — the existing schema/architecture appears unable to represent the evidence.
2. **SCOPE** — the task would require material expansion beyond what was approved.
3. **MONEY / RESOURCE** — the budget in the task will be exceeded.
4. **ACCESS / LEGAL** — authentication, payment, licence ambiguity, terms acceptance, or a human
   permission decision is needed.
5. **DATA INTEGRITY** — source, media, evaluator, or data quality is unreliable enough to
   contaminate results.
6. **CENTRAL ASSUMPTION** — the result materially contradicts an entry in `coordination/ASSUMPTIONS.md`.
7. **IRREVERSIBILITY** — a destructive or irreversible action would be required.
8. **EXPERIMENT MUTATION** — the benchmark, evaluator, or protocol would need to change after
   seeing results.

**On any of these: STOP. Freeze evidence in place. Write a Controller Brief marking
`needs_controller_review`. Do not solve the problem and continue — that silently promotes a
worker's judgement call into an architecture decision.**

### Pre-approved blocked-candidate handling

A multi-candidate discovery/acquisition task may explicitly authorize a narrower behaviour for an
individual candidate: record it as blocked/unavailable and continue to the next already-approved
candidate **without crossing the gate**. This is allowed only when the task file defines the status,
the candidate is optional, no terms are accepted, no authentication/payment/manual permission is
attempted, and no ambiguous material has already been acquired.

This does **not** waive the ACCESS / LEGAL stop gate. The worker must still stop the whole task if
resolving the gate is necessary to meet the task objective, if a human legal/permission judgement is
needed to proceed, or if ambiguity affects material already downloaded/used. The exception exists so
a pre-approved corpus survey does not halt merely because one optional candidate is gated.

## Autonomous queues

`mode: autonomous_queue` lets a worker continue through a pre-approved sequence — e.g.
`CANON-030` → `CANON-031` → `CANON-032` — **only if**: every task in the queue was pre-approved,
the previous task completed normally, no stop gate fired, and cumulative resource budget across
the whole queue still holds.

**If a gate fires partway through a queue, the whole queue stops.** Do not skip the failed item
and continue to the next one — a later task may depend on what the failed one was supposed to
establish.

## What is Level B (worker-autonomous) once frozen

- Canon: consuming approved book/chapter batches into Source Knowledge, provenance checks, coverage
  updates, validation against frozen schemas.
- Eval: running approved model tests, capturing outputs, executing fixed checkers/evaluators,
  logging cost/latency/versions, aggregating results.
- Resources: approved downloads, checksums, manifests, deterministic sampling, duplicate detection,
  distribution reports.

## What is never worker-autonomous, in any stream

Expanding a curriculum or battery. Redefining Canon, Creative IR, or the knowledge architecture.
Adding or removing evaluation metrics post hoc. Changing an evaluator prompt and reporting the
rerun as the original experiment. Merging ontology terms. Choosing a new consumption architecture
because one run happened to look better. Materially increasing spend.
