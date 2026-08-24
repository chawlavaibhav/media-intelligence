# Runbook

## Parallel work: worktrees, one per stream

Three worktrees exist so Canon, Eval and Resources can run simultaneously without one overwriting
another:

```
media-intelligence/                              main branch — Controller's view, merge target
media-intelligence-worktrees/canon/      work/canon branch — Canon sessions work here
media-intelligence-worktrees/eval/       work/eval branch — Eval sessions work here
media-intelligence-worktrees/resources/  work/resources branch — Resources sessions work here
```

**A worker session `cd`s into its own worktree directory and stays there for the whole session.**
It never edits files inside another stream's worktree. When a task is done, the worker commits on
its branch; the Controller reviews the Controller Brief and merges `work/<stream>` into `main`
(or opens a PR). This is the enforcement mechanism behind "a stream never edits another stream's
files" — separate working directories on separate branches, not just a convention.

## Communication check — mandatory

Every new worker session, and every active session after the communication standard changes, must read `shared/COMMUNICATION-STANDARD.md` and confirm once in chat:

> **Communication check:** I will explain technical ideas in plain English, including what they mean, why they matter, and their practical consequence; use minimum sufficient wording without sacrificing understandability; separate evidence from inference; and never invent facts. I have read `shared/COMMUNICATION-STANDARD.md`.

If the file cannot be found or read, STOP. Do not claim compliance.

This confirmation is a startup check, not something to repeat in every message.

## Starting a new Canon session
Read, in order: `coordination/PROJECT-CONTRACT.md` → `shared/COMMUNICATION-STANDARD.md` → `canon/CHARTER.md` → `canon/HANDOFF.md` → the assigned task file → only the source material the task names. Do not replay full project history.

## Starting a new Eval session
Read, in order: `coordination/PROJECT-CONTRACT.md` → `shared/COMMUNICATION-STANDARD.md` → `eval/CHARTER.md` → `eval/HANDOFF.md` → assigned task → named sources.

## Starting a new Resources session
Read, in order: `coordination/PROJECT-CONTRACT.md` → `shared/COMMUNICATION-STANDARD.md` → `resources/CHARTER.md` → `resources/HANDOFF.md` → assigned task → named sources.

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

## Controller-review checkpoints — chat for the human, GitHub for the record
A worker must report the same important checkpoint in **both places**:

1. **Chat:** explain in plain English what happened, what the important technical terms/numbers mean, why the result matters, what changed, what failed or surprised the worker, what remains uncertain, and what decisions/questions need attention. Do not reduce the chat response to only labels, task IDs, metrics, acronyms or commit SHAs.
2. **GitHub:** write the authoritative status, observations, questions, failures, surprises and decisions needed into the task's existing Controller Brief, or into `<stream>/tasks/<TASK-ID>-CHECKPOINT.md` if the Controller Brief does not yet exist.
3. Commit the checkpoint on `work/<stream>`.
4. Push `work/<stream>` to GitHub.
5. End the chat report with the task ID and commit SHA so the Controller can inspect the exact branch state.

The two surfaces have different purposes:
- **Chat is for immediate human understanding.** The human should understand the important learning and its consequence without opening GitHub or remembering internal jargon.
- **GitHub is the durable source of truth for Controller review.** The Controller reads the branch directly and should not rely on pasted chat text when the repository record is available.

The human operator therefore does not need to copy/paste normal worker reports between Claude and the Controller. They may simply tell the Controller to review `<TASK-ID>` on `work/<stream>`. The human may also open the same Controller Brief in GitHub whenever they want the full record.

A worker may update its own `HANDOFF.md` when useful, but the task checkpoint / Controller Brief is
the authoritative review surface. Do not use `HANDOFF.md` as a substitute for recording the actual
question and evidence.

## How the Controller reviews a Controller Brief
Read `OBSERVED` and `INFERRED` as separate claims — the first is evidence, the second is
interpretation. `RECOMMENDED NEXT STEP` is a suggestion only. Approve, amend, or reject; the
worker's suggestion becomes real only once written as a new task.

For meaningful tasks, the Controller should return two layers:
- **Founder view:** explain what worked, what failed, what surprised us, what changed our understanding, what the important technical result means in practice, and which evidence is worth the human inspecting personally. Internal labels should be translated into plain language rather than merely repeated.
- **Controller view:** scope compliance, evidence quality, technical correctness, merge recommendation, and proposed next task. Technical detail is welcome, but unfamiliar terms and consequential numbers must still be explained.

Both layers follow `shared/COMMUNICATION-STANDARD.md`: complete, explanatory and correct, but no longer than needed.
Routine mechanical details may stay in the Controller layer. Learning-bearing findings, belief changes, repeated failures and directional implications must be surfaced in the Founder view rather than silently converted into the next task.

## How cross-stream findings are escalated
Worker tags severity (`LOCAL` / `CROSS_STREAM` / `ARCHITECTURAL`) in its Controller Brief.
`CROSS_STREAM` → worker also files `<stream>/PROPOSED-INTEGRATION-CHANGE-<ID>.md`. `ARCHITECTURAL`
→ immediate stop, no further work in that task until Controller reviews.

## Starting a fresh Controller chat
Read `coordination/CONTROL-STATE.md` first, then `shared/COMMUNICATION-STANDARD.md`. Fall back to `coordination/DECISION-LOG.md` only if a CONTROL-STATE claim needs its history checked.

## Merging work safely
Each stream owns its directory tree exclusively (enforced by worktree, see below, or by
convention if worktrees aren't in use). A stream never edits another stream's files or
`coordination/` directly — only via a `PROPOSED-INTEGRATION-CHANGE` file the Controller merges in.

## Recovering from a blocked task
Task stays `needs_controller_review`. Controller either unblocks (answers the question, approves
the budget, resolves the ambiguity) and the same task resumes, or explicitly closes it and opens a
new task ID reflecting the changed plan. Never silently reopen a task with a materially different
method under the same ID.
