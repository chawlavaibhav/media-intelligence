# Task CANON-003: Broad multi-book Canon stress batch

**TASK ID:** CANON-003

**OBJECTIVE:** Stress-test the current Canon extraction method across a genuinely broad set of distinct books before making another schema or method change. Complete **at least 15 usable distinct books**, target **18**, and allow **up to 20** when suitable already-available sources exist. Accumulate failures first; revise rules only after the batch is complete.

**WHY WE ARE DOING THIS:** CANON-001 and CANON-002 each surfaced a different issue. A loop of one book → one problem → one rule change risks fitting the Canon method to the last book seen. Four more books is still too thin to distinguish recurring structural failures from source-specific quirks. The human has therefore explicitly broadened the experiment: hold the method fixed across a much larger and more varied sample, then revise once from the pattern.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`. Explain what each issue means, why it matters, whether it repeats across sources, what changes because of it, and what remains uncertain. Do not bury important failures in YAML-only notes.

## CORE EXPERIMENT RULE — FREEZE, OBSERVE, THEN SYNTHESIZE

For this task, the current CANON-002-era extraction method and SPEC-03/04/05 schemas are a **frozen test instrument**.

During the whole batch:
- do **not** change the granularity rule;
- do **not** change the visual-pass method;
- do **not** change SPEC-01, SPEC-03, SPEC-04 or SPEC-05;
- do **not** add ontology relation types or term kinds;
- do **not** repair the method after one source reveals a problem and then continue as though all books were processed under the same method;
- do **not** silently back-fill omissions discovered after comparison with historical work;
- do **not** choose later books merely because they are likely to confirm an issue already seen.

Instead, log every mismatch, omission, ambiguity, schema limitation, visual-loss problem, source-shape mismatch, provenance problem or useful counterexample in one batch issue ledger.

The question is not “can we fix this book?” It is “what breaks repeatedly across materially different books?”

## PRE-START: PRESERVE CANON-002 AS EVIDENCE

CANON-002 remains evidence for this batch. Preserve its frozen checkpoint and its identified issues, including:
- visual evidence can disappear entirely in plain text;
- a change can be both an experimental confound and a source-authored claim;
- the all-caps passage may contain separable claims;
- `creative.hierarchy` may not express a definite traversal/end;
- three source claims were missed because of classification.

Do **not** resolve these before the batch. Enter them in the batch ledger as hypotheses to watch for recurrence.

Administrative cleanup is allowed: fetch/merge latest `origin/main` if clean and adopt the current communication standard. Do not rewrite CANON-001/002 substantive extraction artifacts merely to prepare CANON-003.

## PHASE 0 — INVENTORY AND SOURCE SELECTION

Before extraction, inventory the **already-available local/repository book library**. Do not acquire new copyrighted books for this task.

Create `canon/findings/CANON-003-source-inventory-and-selection.md` containing:
- distinct book title / author / edition where verifiable;
- local/repo location;
- whether usable text exists;
- whether matching visuals/pages are locally available and provenance-verifiable;
- likely domain/source shape;
- known integrity limitations;
- selected / reserve / blocked status and reason.

### Batch size

- **Minimum success:** 15 usable distinct books completed under the frozen method.
- **Target:** 18 distinct books.
- **Maximum without another Controller approval:** 20 distinct books.
- A book blocked before faithful extraction does **not** count toward the 15. Replace it from the already-available inventory where possible.
- If fewer than 15 usable distinct books are actually available locally under the task rules, document the exact inventory shortfall and stop for Controller review rather than acquiring new books.

### What counts as one book

A “book” means a distinct source title, not another chapter from the same title.

For each selected book, process a **coherent representative section large enough to expose the author’s reasoning system**, normally one substantial chapter or a tightly connected multi-chapter span. Do not cherry-pick isolated quotes merely to reach the source count. Full cover-to-cover extraction is not required in this stress batch unless the book is short and doing so is practical.

### Coverage requirement

Selection must be driven by **domain/source-shape diversity**, not by current Canon issues. Across the first 15 usable books, aim for at least:

- **3 static visual-design / typography / composition books**;
- **3 photography / lighting / image-making books**;
- **3 filmmaking / cinematography / editing / continuity books**;
- **3 advertising / commercial-communication / persuasion books**;
- **3 storytelling / animation / motion / creative-process books**.

If the actual local library cannot satisfy a quota, do not invent a source. Use the nearest legitimate available domain, document the gap, and preserve the overall goal of materially different source shapes.

For books 16–20, prioritise the weakest remaining coverage or a genuinely different knowledge shape: mechanism-heavy, remedy-heavy, procedural, physical/causal, sequence-level, empirical, practitioner heuristic, trade-off driven, or visually demonstrated.

## ANCHOR SOURCES — MUST BE INCLUDED IF USABLE

The four already-planned probes remain mandatory anchors unless source integrity blocks them:

1. **Ellen Lupton — hierarchy / typography material** — `canon/sources/lupton_split001.txt`. Known risk: prior column/interleaving corruption; do not guess through garbled text.
2. **Grammar of the Shot — continuity chapter** — `canon/sources/gos-ch4-continuity-p93-112.txt`.
3. **Ogilvy — advertising that sells** — `canon/sources/ogilvy-ch2-advertising-that-sells.txt`.
4. **Light: Science & Magic — reflection chapter** — `canon/sources/lsm-ch3-reflection.txt`.

The remaining books are selected autonomously from the verified already-available inventory under the coverage rules above. This broadening is human-approved; selecting a book within those rules does **not** require returning for Controller approval.

## VISUAL EVIDENCE POLICY

Use matching local page images/PDFs where already available and provenance-verifiable. Render ephemerally only; do not commit copyrighted page images.

If a source is visually argued and no matching visual source is available locally:
- do not abandon the whole batch;
- mark that source’s visual completeness `not_verified` / `blocked_visual_validation`;
- continue source-faithful text extraction only where the text itself supports the claim;
- do not claim visual completeness;
- record the limitation in the batch ledger.

If the text itself is corrupt enough that claims cannot be extracted faithfully, block that book as `blocked_source_integrity`, record why, and replace it from the local reserve where possible. Do not guess through corruption.

## PER-BOOK PROCEDURE

For every selected book, independently:

1. Verify source identity/provenance and text integrity as far as available evidence permits.
2. Define the coherent section being processed and why it is representative enough for this stress test.
3. Perform the same CANON-002-era independent visual-evidence pass where matching visuals are available.
4. Produce a fresh SPEC-03 source representation using the existing V0 granularity rule.
5. Produce SourceConceptSystems and SPEC-05 ontology mappings using only existing relation types.
6. Produce SPEC-04 operational bindings only after source representation is stable. Zero bindings is acceptable.
7. Mechanically validate.
8. Commit a **book-specific fresh checkpoint** before opening any historical extraction/audit/summary for that same book.
9. If historical material exists, compare after the checkpoint and record disagreements/misses. If none exists, record `no historical comparator` rather than manufacturing one.
10. Add all relevant issues/counterevidence to the batch ledger. Do not alter the frozen method.

Use separate task-scoped IDs/directories per book.

## HISTORICAL MATERIAL

Historical work for a book is sealed until that book’s fresh checkpoint exists. Historical comparison is a post-hoc diagnostic, never training material for the fresh pass.

Known historical anchors include:
- `canon/findings/FINDINGS-05-lupton-hierarchy-pass1.md`
- `canon/findings/FINDINGS-06-gos-continuity-pass1.md`
- `canon/findings/FINDINGS-07-ogilvy-pass1.md`
- `canon/findings/FINDINGS-08-lsm-reflection-pass1.md`

Treat corresponding migration audits / superseded atoms as sealed in the same way. For newly selected books, search for historical repo material only **after** that book’s fresh checkpoint.

## BATCH ISSUE LEDGER

Create `canon/findings/CANON-003-batch-issue-ledger.md`.

Every issue must record:
- plain-English issue;
- book(s) where observed;
- OBSERVED / INFERRED / SUSPECTED status;
- affected layer: source fidelity, granularity, systems, ontology, bindings, visual completeness, provenance, Creative IR fit, or other;
- whether it is new, a recurrence of CANON-001/002, a recurrence first seen inside this batch, or evidence against an earlier concern;
- number of **distinct books** showing it;
- practical consequence if unchanged;
- proposed fix only as a proposal, not applied during CANON-003.

Do not count repeated manifestations inside one book as independent cross-source evidence.

## PROGRESS CHECKPOINTS — LEARNING WITHOUT RULE CHANGES

After approximately books 5, 10 and 15, update the Controller Brief/Handoff and explain in chat:
- what kinds of sources have been processed;
- recurring issues so far;
- issues that have failed to recur;
- surprising new source shapes;
- blocked books and why;
- whether the remaining selection still gives broad coverage.

These are learning checkpoints, **not approval gates**. Continue autonomously unless a whole-task stop condition fires. Do not change the method at a checkpoint.

After 15 usable books, continue toward the target of 18 when suitable already-available sources remain. Going from 18 to 20 is optional and should add real diversity, not volume for its own sake.

## END-OF-BATCH SYNTHESIS

Only after at least 15 usable distinct books are complete — preferably 18 — produce `canon/findings/CANON-003-multi-source-synthesis.md` answering:

1. Which CANON-001/002 issues recurred, across how many distinct books and domains?
2. Which earlier issues did not recur despite many opportunities?
3. What new failure modes appeared repeatedly?
4. Which schema/method changes now have broad evidence behind them?
5. Which proposed changes still look source-specific or like overfitting?
6. Did the V0 granularity rule remain usable across the different source shapes?
7. Did the SourceKnowledge / SourceConceptSystem / ontology / binding separation continue to hold?
8. What source shapes produce different knowledge profiles — mechanism-heavy, remedy-heavy, procedural, physical/causal, sequence-level, commercial heuristic, empirical, etc.?
9. Which useful source knowledge repeatedly fails to bind to current product schemas, and is that a Canon problem or a product-schema limitation?
10. What visual information is repeatedly lost in text extraction, and in what source classes?
11. Which apparently important issues are actually isolated to one or two books?
12. What should be changed **once**, after this batch, before broad ingestion?
13. What should deliberately remain unchanged because evidence is still weak?
14. Based on this larger sample, is another stress batch needed before method revision, or is the evidence broad enough to consolidate?

The synthesis may recommend one consolidated schema/method revision task. It may **not perform that revision**.

## IN SCOPE

- 15–20 distinct already-available books under one frozen method;
- a coherent representative section from each book;
- source inventory and coverage-driven selection;
- visual passes where provenance-verifiable local visuals exist;
- source-integrity blocking/replacement when necessary;
- fresh SourceKnowledge, SourceConceptSystems, ontology mappings and operational bindings;
- per-book fresh checkpoints;
- post-checkpoint historical comparison where such material exists;
- batch issue ledger;
- progress learning checkpoints;
- multi-book synthesis;
- clearly marked cross-stream proposals where warranted.

## OUT OF SCOPE

- no schema or extraction-method changes during the batch;
- no new copyrighted-book acquisition;
- no more than 20 distinct books without Controller approval;
- no Canon-consumption/RAG experiment;
- no evaluator/model benchmarking;
- no provider/model selection;
- no committing copyrighted page renders;
- no rewriting historical evidence;
- no retrospective cleanup of CANON-001/002 knowledge objects as part of this task.

## DELIVERABLES

Batch-level:
- `canon/findings/CANON-003-source-inventory-and-selection.md`
- `canon/findings/CANON-003-batch-issue-ledger.md`
- `canon/findings/CANON-003-multi-source-synthesis.md`
- `canon/tasks/CANON-003-CONTROLLER-BRIEF.md`
- updated `canon/HANDOFF.md`

Per usable book:
- fresh current-schema knowledge files under `canon/knowledge/current/<source>/`;
- source-specific findings/provenance record;
- fresh checkpoint before historical comparison.

**AUTONOMY MODE:** autonomous inside the frozen method. The worker may inventory, select and process up to 20 already-available books without returning for approval between books, subject to the selection and stop rules above.

## RESOURCE BUDGET

- usable books: minimum 15; target 18; maximum 20;
- source acquisition: **none** — already-available local/repository material only;
- paid APIs: ₹0 / $0;
- page rendering: ephemeral local only;
- committed storage: text/YAML/Markdown only; no full copyrighted page images or source books committed.

## STOP CONDITIONS

Stop the whole task only for:
- fewer than 15 usable distinct books are available locally under these rules;
- need to change schema/method to continue a substantial fraction of remaining books;
- need for a new ontology relation/type to represent multiple materially different books honestly;
- project-wide provenance/legal problem;
- source integrity problem affecting the library broadly rather than one book;
- architecture conflict that makes continued extraction misleading rather than merely imperfect.

A problem isolated to one book should normally block/log/replace that book and continue.

## HUMAN APPROVAL TRIGGERS

- any schema/method change during the batch;
- any new source acquisition;
- any new ontology relation/type;
- exceeding 20 distinct books;
- changing the coverage-selection policy materially;
- any attempt to convert a recurring issue into a project rule before the end-of-batch synthesis.

**RESULT LOCATION:** `canon/tasks/CANON-003-CONTROLLER-BRIEF.md` plus the batch deliverables above.
