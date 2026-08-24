# CANON-003 — Parallel execution amendment

**Status:** Controller-approved execution amendment · 24 Aug 2026

This amendment changes only how CANON-003 is executed. The extraction method, SPEC-01/03/04/05 schemas, granularity rule, visual-pass method, ontology vocabulary, evidence standards, source-selection principles, and end-of-batch synthesis questions remain frozen exactly as defined in `canon/tasks/CANON-003.md`.

## Why parallel execution is approved

The sequential Canon session approached its context-window limit after five completed books. CANON-003 is specifically designed so each book is a fresh extraction under one frozen method, followed by a later cross-book synthesis. Parallelising the remaining independent book extractions therefore improves speed and reduces context pressure without changing the experiment, provided workers remain isolated from each other's new findings.

## Authoritative pre-parallel checkpoint

The latest `origin/work/canon` checkpoint must contain `canon/findings/CANON-003-HANDOVER-CHECKPOINT.md` and report:

- 5 usable books complete: Grammar of the Shot, Ogilvy on Advertising, Light: Science & Magic, Interaction of Color, The Vignelli Canon;
- no partially extracted book;
- Lupton / Thinking with Type blocked on structural column-interleaving corruption and not counted as usable;
- no extraction started for Making and Breaking the Grid.

The setup session must resolve the exact checkpoint SHA from `origin/work/canon` after fetching; do not hard-code a SHA from chat.

## Parallel-base rule

Create one new branch from the exact `origin/work/canon` checkpoint tip, then merge current `origin/main` into that new branch. Do not rewrite the old `work/canon` branch merely to prepare parallelism.

Recommended base branch: `work/canon-003-parallel-base`.

All four worker branches/worktrees must start from the same final parallel-base SHA.

## Isolation rule

The first five completed books and CANON-001/002 pre-batch hypotheses are shared starting evidence. New CANON-003 findings produced after the parallel split are not training material for another lane's fresh extraction.

A lane may read:

- `shared/COMMUNICATION-STANDARD.md`;
- `canon/tasks/CANON-003.md`;
- this amendment;
- `canon/findings/CANON-003-source-inventory-and-selection.md`;
- the pre-parallel handover checkpoint;
- CANON-001/002 decisions needed to understand the frozen method;
- its assigned source material and its own lane files.

During fresh extraction it must not read another lane's new per-book findings or lane issue file. It must also avoid using the existing batch issue ledger as a checklist of what to find; the ledger already contains findings from the first five books and is preserved as evidence for later integration.

## Shared files locked during parallel extraction

Parallel lanes must not edit:

- `canon/findings/CANON-003-batch-issue-ledger.md`
- `canon/findings/CANON-003-multi-source-synthesis.md`
- `canon/tasks/CANON-003-CONTROLLER-BRIEF.md`
- `canon/HANDOFF.md`

Each lane records new issues in its own lane file:

- Lane A: `canon/findings/CANON-003-lane-A-issues.md`
- Lane B: `canon/findings/CANON-003-lane-B-issues.md`
- Lane C: `canon/findings/CANON-003-lane-C-issues.md`
- Lane D: `canon/findings/CANON-003-lane-D-issues.md`

Each lane also maintains a small lane checkpoint with completed books, latest SHA, unresolved local issues, and remaining assignments.

## Fixed remaining-book assignments

The first five usable books are already complete. The following thirteen slots are fixed so the batch reaches the preferred target of 18 usable books without workers choosing sources after seeing emerging results.

### Lane A — visual design / photography

- **Book 6:** Timothy Samara — *Making and Breaking the Grid*
- **Book 7:** Michael Freeman — *The Photographer's Eye*
- **Book 8:** John Alton — *Painting With Light*

### Lane B — film / editing / unusual source form

- **Book 9:** *Grammar of the Edit*
- **Book 10:** Walter Murch — *In the Blink of an Eye*
- **Book 11:** Christopher Kenworthy — *Master Shots*
- **Book 12:** Michael Ondaatje — *The Conversations*

### Lane C — advertising / persuasion

- **Book 13:** Claude Hopkins — *Scientific Advertising*
- **Book 14:** Chip Heath & Dan Heath — *Made to Stick*
- **Book 15:** Rory Sutherland — *Alchemy*

### Lane D — storytelling / creative process

- **Book 16:** Ed Catmull — *Creativity, Inc.*
- **Book 17:** David Bayles & Ted Orland — *Art & Fear*
- **Book 18:** Donald Miller — *Building a StoryBrand*

These assignments include three reserve selections beyond the original first-15 usable core because the human preference is at least 15 and preferably higher. The added books deliberately broaden source shape: procedural recipe (`Master Shots`), interview transcript (`The Conversations`), and anti-rational/practitioner heuristic (`Alchemy`).

If one assigned book is blocked by source integrity, do not substitute autonomously across lanes. Record the block and stop that book. The final integrator decides whether a replacement is needed to preserve 18 usable books. Other assigned books in the same lane may continue unless a CANON-003 whole-task stop condition fires.

## Per-book procedure remains unchanged

For every assigned book:

1. verify source identity/provenance and text integrity;
2. define the coherent representative section;
3. run the frozen visual-evidence pass where matching visuals are available;
4. produce fresh SPEC-03 SourceKnowledge;
5. produce SourceConceptSystems and existing SPEC-05 ontology mappings;
6. produce SPEC-04 bindings only after source representation is stable;
7. mechanically validate;
8. commit and push a book-specific fresh checkpoint **before** opening historical extraction/audit material for that book;
9. only then compare historical material if any exists;
10. record issues in the lane issue file without changing the method.

Use source-specific IDs/directories so lane merges cannot collide. Never create generic IDs whose uniqueness depends only on a global book number.

## Context-window rule

The branch is durable memory; the chat is disposable.

After every completed book, each lane must validate, commit, push, and update its lane checkpoint. If the Claude context is becoming crowded, stop at a book boundary and continue later in a fresh Claude session on the same branch/worktree. Do not force several books through a degraded context merely to finish a lane in one conversation.

## Final integration

Parallel lanes do not merge themselves together and do not perform final synthesis.

After Controller review of all lane branches, one fresh Canon integration session will:

1. merge/reconcile the lane branches;
2. validate all per-book outputs;
3. combine the four lane issue files with the preserved pre-parallel batch ledger;
4. count recurrence by distinct books, not mentions;
5. distinguish recurring, isolated, contradicted, and source-shape-specific issues;
6. write the missing standalone findings for pre-parallel books 4–5 if still required;
7. confirm domain/source-shape coverage and actual usable-book count;
8. produce `CANON-003-multi-source-synthesis.md` and the Controller Brief;
9. recommend one consolidated post-batch revision task if evidence supports it;
10. **not** implement any method/schema revision and **not** run Canon-consumption experiments.

## No other change

Parallelisation is an execution optimization, not permission to change Canon architecture or research rules. All original CANON-003 stop conditions and human-approval triggers continue to apply.
