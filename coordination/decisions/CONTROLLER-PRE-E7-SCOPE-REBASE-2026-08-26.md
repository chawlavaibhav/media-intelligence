# Controller Decision — Pre-E7 Scope Rebase

**Date:** 26 Aug 2026  
**Decision:** APPROVED AND IN FORCE

The Controller pauses paid Eval execution before E7 and adopts the design in:

`docs/superpowers/specs/2026-08-26-pre-e7-scope-rebase-design.md`

## Why

The accepted V1 capability map defines what can fail, but duration discussion exposed that important production conditions were not frozen. A capability result without its production envelope can become misleading when duration, shot count, workflow mode, reference quality, constraint load or composition strategy changes.

The second issue is outcome accounting: customers buy accepted media outcomes, while a single outcome may be assembled from multiple shots, transforms, repairs and API calls. CpAO must therefore be computable at outcome level without breaking the existing one-call-one-trial evidence model.

## Immediate effect

- E7 paid admission benchmarking: **BLOCKED pending rebase integration**.
- E8 deep qualification: **BLOCKED pending rebase integration**.
- Existing E7=204 / E8=520 output counts are retained as historical pre-rebase forecasts, not authorised budgets.
- Capability Registry remains at zero empirical current-model entries.
- The 36 capabilities are temporarily **open for bounded audit**, not discarded.
- The 100-item bank remains the baseline starting point, not automatically rebuilt.
- The 30 Canon customer briefs remain authoritative customer-intent audit material.
- `EVAL-006` remains PAUSED and is not revived.

## Frozen direction

Before paid benchmarking, the project must freeze four interfaces:

1. Production Requirement Profile;
2. Condition / Envelope Contract;
3. Outcome / Production Topology Contract;
4. Capability Contract v2 after auditing all 30 Canon briefs.

The benchmark must remain sparse/adaptive; do not enumerate the combinatorial space.

## Stream assignments

- Canon executes `canon/tasks/CANON-PRE-E7-SCOPE-AUDIT.md`.
- Eval executes `eval/tasks/EVAL-PRE-E7-SCOPE-REBASE.md`.
- Resources executes `resources/tasks/RESOURCES-PRE-E7-SCOPE-REBASE.md`.

Workers must use isolated branches and must not merge themselves. Controller performs final reconciliation and explicitly re-authorises E7 only if completion criteria pass.
