# Runbook

**Updated:** 28 Aug 2026, context-architecture migration (Controller-assigned cross-project task).
Previous update: 25 Aug 2026 by Repository Governor, task GOV-001.
**Read `PROJECT-MEMORY.md` first, then `coordination/CONTROL-STATE.md`.**

## Parallel work: one branch per task

Each task runs on its own branch named after the task, and the Controller merges it to `main` by PR.

```
main                                  Controller's view, merge target, the only source of truth
work/<task-id>                        e.g. work/canon-006-reserves, work/eval-005-review-packet
work/gov-<nnn>-<slug>                 Governor tasks
```

**A worker stays on its own branch for the whole session and never edits another stream's files.**
When a task is done the worker commits, pushes, and the Controller reviews the Controller Brief and
merges via PR.

**The control mechanism is three things together:** stream directory ownership (`canon/**`,
`eval/**`, `resources/**` each belong to one stream; `coordination/**` and `governance/**` belong to
the Controller and Governor), the approved scope of the assigned task, and PR review before merge.
A stream reaches another's territory only through a `PROPOSED-INTEGRATION-CHANGE-<ID>.md` file.

**Worktrees are optional execution convenience only.** Using `git worktree` to keep streams in
separate directories is fine and often handy. It enforces nothing, and no rule depends on it.

> **Correction notice.** This section previously described three long-lived per-stream worktrees
> (`work/canon`, `work/eval`, `work/resources`) checked out under a sibling
> `media-intelligence-worktrees/` directory, and called that arrangement the enforcement mechanism
> behind stream ownership. Actual practice moved to per-task branches from CANON-003 onward, and the
> three original branches are stale. **Worktrees never enforced anything** — directory ownership,
> approved task scope and PR review do.

**Branch hygiene.** Most `work/*` branches on the remote are historical: their content reached `main`
by squash merge, so `git branch --merged` reports them as unmerged and cannot be trusted to tell you
what is live. Treat a branch as live only if an open PR or an assigned task file names it.

## Communication check — mandatory

Every new worker session, and every active session after the communication standard changes, must read `shared/COMMUNICATION-STANDARD.md` and confirm once in chat:

> **Communication check:** I will explain technical ideas in plain English, including what they mean, why they matter, and their practical consequence; use minimum sufficient wording without sacrificing understandability; separate evidence from inference; and never invent facts. I have read `shared/COMMUNICATION-STANDARD.md`.

If the file cannot be found or read, STOP. Do not claim compliance.

This confirmation is a startup check, not something to repeat in every message.

## Starting a new worker session — default bootstrap (all streams)

Read, in order:

1. `PROJECT-MEMORY.md` — compact project map and authority map
2. `coordination/CONTROL-STATE.md` — what is currently authorised, active, blocked, cancelled
3. `coordination/PROJECT-CONTRACT.md`
4. `shared/COMMUNICATION-STANDARD.md`
5. `shared/CONTEXT-SUFFICIENCY-POLICY.md`
6. your own stream `CHARTER.md` (`canon/`, `eval/` or `resources/`)
7. the assigned task file
8. the task's named dependencies (its Context Contract)
9. **expand context whenever `shared/CONTEXT-SUFFICIENCY-POLICY.md` requires it** — and stop with
   `STOP — CONTEXT_INSUFFICIENT` rather than guess when sufficiency cannot be established.

**Stream `HANDOFF.md` files are NOT compulsory startup reading.** Read your stream's handoff only
when: the assigned task explicitly names it; recent technical continuity in that stream is relevant
to your task; necessary context cannot be obtained from current state plus the task's dependencies;
or an expansion trigger leads you into it. Handoffs are stream-owned working notes and may be
stale — `coordination/CONTROL-STATE.md` governs current state wherever they disagree.

Do not replay full project history. Historical narrative lives under `history/` and in decision
records; read it when an expansion trigger requires it, not by default.

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
Read `PROJECT-MEMORY.md` first, then `coordination/CONTROL-STATE.md`, then
`coordination/PROJECT-CONTRACT.md`, then `shared/COMMUNICATION-STANDARD.md`, then
`shared/CONTEXT-SUFFICIENCY-POLICY.md`. Discover decisions by listing `coordination/decisions/`
directly; `coordination/DECISION-LOG.md` is a curated historical/navigation index, not an
exhaustive post-26-Aug source.

## Controller sessions: one Writer, any number of Advisory

Parallel Controller chats are allowed, but **changes to the strategic control plane are
serialized**. Every Controller session operates in exactly one of two modes, declared at session
start:

**WRITER CONTROLLER** — at most **one at a time** across the whole project. Only a Writer may:
- create durable decisions (`coordination/decisions/`, decision records elsewhere);
- mutate `coordination/CONTROL-STATE.md` or other programme state;
- authorise, cancel or defer tasks;
- merge to `main`.

**ADVISORY CONTROLLER** — any number in parallel. An Advisory session may inspect GitHub, analyse,
challenge, critique, research, plan, and **draft** proposed decisions or tasks — but must **not**
mutate durable programme state. A draft becomes real only when a Writer Controller commits it.

Notes:
- This serializes only the strategic control plane. It does **not** serialize domain workers and
  does **not** prohibit multiple parallel analysis sessions.
- An Advisory session working from an older snapshot must re-check `CONTROL-STATE.md` and the
  newest decisions before its drafts are acted on — a parallel Writer may have moved the state.
- If two sessions have both been acting as Writer, stop: the later state wins only after an
  explicit reconciliation against `coordination/decisions/` — never assume.

## Governor review
Every meaningful task/PR gets a bounded integrity review by the Repository Governor before merge.
See `governance/GOVERNOR-CONTRACT.md`, including its three review modes: **Level 1** task/PR
integrity review (default, dependency-bounded), **Level 2** state reconciliation (after a batch of
integrated work, delta-bounded), **Level 3** deep audit (deliberately authorised broad inspection).
Its verdict is `PASS`, `PASS WITH NON-BLOCKING NOTES` or `BLOCK` with evidence. The Governor
advises; **the Controller merges.**

## Merging work safely
Each stream owns its directory tree exclusively. **The control mechanism is stream directory
ownership plus approved task scope plus PR review** — not tooling. A stream never edits another
stream's files or `coordination/` directly; it reaches them only via a
`PROPOSED-INTEGRATION-CHANGE` file the Controller actions.

## Recovering from a blocked task
Task stays `needs_controller_review`. Controller either unblocks (answers the question, approves
the budget, resolves the ambiguity) and the same task resumes, or explicitly closes it and opens a
new task ID reflecting the changed plan. Never silently reopen a task with a materially different
method under the same ID.
