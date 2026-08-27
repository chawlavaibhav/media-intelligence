# Controller — GOV-006 Start Authorisation — 2026-08-28

## Status

**GOV-006 AUTHORISED AND MAY START NOW.**

The deferred trigger from
`coordination/decisions/CONTROLLER-GOV-005-CLOSURE-AND-GOV-006-TRIGGER-2026-08-28.md`
is satisfied: the active parallel lanes have settled enough for a meaningful current-`main` reconciliation.

The last returning material lane, RES-005, is accepted and merged, including the Controller's cross-stream temporal material-contract reconciliation.

## Scope

GOV-006 is a bounded Repository Governor coherence audit only.

Authority and task:
- `governance/tasks/GOV-006.md`

It must reconcile current-state documentation to the already-merged evidence and Controller decisions through the current settled tree, including:
- CANON-011;
- EVAL-024;
- EVAL-029;
- EVAL-026;
- EVAL-030;
- RES-005 and its temporal cross-stream corrections;
- GOV-005 closure.

It must verify durable empirical evidence persistence and authority-chain navigability, close stale active-lane wording, and route remaining coherence defects.

## Boundaries

GOV-006 must not:
- reopen GOV-005;
- redesign any domain methodology or architecture;
- edit stream-owned domain artifacts;
- change Registry admission semantics;
- add Registry rows;
- invent a temporal checker, threshold, qualification or result;
- import chat-only A-TEXT manual review into durable project truth;
- run any model/evaluator/provider API or spend money;
- build Production IR or a Planner.

## Execution branch

Use:

`work/gov-006-post-parallel-reconciliation`

The Governor records the exact `main` SHA it audits at worker start and returns to the Controller. The Governor does not merge.
