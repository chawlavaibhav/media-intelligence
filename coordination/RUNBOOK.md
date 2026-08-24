# Runbook

## Starting a new Canon session
Read, in order: `coordination/PROJECT-CONTRACT.md` → `canon/CHARTER.md` → `canon/HANDOFF.md` →
the assigned task file → only the source material the task names. Do not replay full project
history.

## Starting a new Eval session
Same pattern: `coordination/PROJECT-CONTRACT.md` → `eval/CHARTER.md` → `eval/HANDOFF.md` →
assigned task → named sources.

## Starting a new Resources session
`coordination/PROJECT-CONTRACT.md` → `resources/CHARTER.md` → `resources/HANDOFF.md` → assigned
task → named sources.

## Approving a task
Controller writes/fills `shared/templates/TASK-TEMPLATE.md`, assigns an ID (`CANON-NNN` /
`EVAL-NNN` / `RES-NNN` / `INT-NNN`), sets `AUTONOMY MODE`, and places it in the stream's `tasks/`.
A task is not approved until it exists as a file with a Controller-set ID.

## Marking a task autonomous
Set `AUTONOMY MODE: autonomous` only when method is frozen, inputs are named, and budget/stop
conditions are explicit. See `shared/AUTONOMY-POLICY.md`.

## Building an autonomous queue
A numbered sequence of pre-approved tasks (e.g. `CANON-030`…`CANON-033`) where each one's inputs
don't depend on human judgement about the *previous* one's output. If task N's next step needs a
decision, the queue ends at N — do not pre-approve N+1 blind.

## When a worker must stop
Any of the 8 triggers in `shared/AUTONOMY-POLICY.md`. On a stop: freeze evidence, write a
Controller Brief with `STATUS: needs_controller_review`, do not attempt to resolve the trigger and
continue.

## How the Controller reviews a Controller Brief
Read `OBSERVED` and `INFERRED` as separate claims — the first is evidence, the second is
interpretation. `RECOMMENDED NEXT STEP` is a suggestion only. Approve, amend, or reject; the
worker's suggestion becomes real only once written as a new task.

## How cross-stream findings are escalated
Worker tags severity (`LOCAL` / `CROSS_STREAM` / `ARCHITECTURAL`) in its Controller Brief.
`CROSS_STREAM` → worker also files `<stream>/PROPOSED-INTEGRATION-CHANGE-<ID>.md`. `ARCHITECTURAL`
→ immediate stop, no further work in that task until Controller reviews.

## Starting a fresh Controller chat
Read `coordination/CONTROL-STATE.md` first — it's built to be sufficient alone. Fall back to
`coordination/DECISION-LOG.md` only if a CONTROL-STATE claim needs its history checked.

## Merging work safely
Each stream owns its directory tree exclusively (enforced by worktree, see below, or by
convention if worktrees aren't in use). A stream never edits another stream's files or
`coordination/` directly — only via a `PROPOSED-INTEGRATION-CHANGE` file the Controller merges in.

## Recovering from a blocked task
Task stays `needs_controller_review`. Controller either unblocks (answers the question, approves
the budget, resolves the ambiguity) and the same task resumes, or explicitly closes it and opens a
new task ID reflecting the changed plan. Never silently reopen a task with a materially different
method under the same ID.
