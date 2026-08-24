# Task CANON-003: Multi-source Canon stress batch

**TASK ID:** CANON-003

**OBJECTIVE:** Stress-test the current Canon extraction method across several materially different sources before making another schema or method change. Accumulate failures first; revise rules only after the batch is complete.

**WHY WE ARE DOING THIS:** CANON-001 and CANON-002 each surfaced a different method/schema issue. Reviewing one source, changing the method, then reviewing one more source risks overfitting the extraction system to the last book seen. The human has explicitly changed direction: consume a broader batch first, record where the frozen method succeeds or breaks, then make one evidence-based revision from the pattern across sources.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`. Explain what each issue means, why it matters, whether it repeats across sources, and what remains uncertain. Do not bury important method failures in YAML-only notes.

## CORE EXPERIMENT RULE — FREEZE, OBSERVE, THEN SYNTHESIZE

For this task, the current CANON-002-era extraction method and SPEC-03/04/05 schemas are a **frozen test instrument**.

During the batch:
- do **not** change the granularity rule;
- do **not** change the visual-pass method;
- do **not** change SPEC-03, SPEC-04, SPEC-05, or SPEC-01;
- do **not** add ontology relation types or term kinds;
- do **not** repair the method after the first source reveals a problem and then continue as though all sources were processed under one method;
- do **not** silently back-fill omissions discovered by comparison with historical work.

Instead, log every mismatch, omission, ambiguity, schema limitation, visual-loss problem, source-shape mismatch, or provenance problem in a **batch issue ledger** with the source(s) that triggered it.

The point is to learn which failures are isolated and which recur.

## PRE-START: CLOSE CANON-002 AS EVIDENCE, NOT AS A NEW RULE

CANON-002's substantive extraction remains evidence for this batch. Preserve its frozen checkpoint and its identified issues, including:
- visual evidence can disappear entirely in plain text;
- a change can be both an experimental confound and a source-authored claim;
- the all-caps passage may contain separable claims;
- `creative.hierarchy` may not express a definite traversal/end;
- three source claims were missed because of classification.

Do **not** resolve these by changing the method before the batch. Record them as starting hypotheses/issues to test for recurrence.

Administrative cleanup is allowed: fetch/merge latest `origin/main` if clean and adopt the current communication standard. No substantive CANON-002 extraction artifact may be rewritten merely to prepare CANON-003.

## BATCH SOURCES

Process these four existing source probes using the same frozen method:

1. **Ellen Lupton — hierarchy / typography material**
   - repo source: `canon/sources/lupton_split001.txt`
   - historical probe exists and must remain sealed until that source's fresh checkpoint.
   - known risk: earlier extraction noted possible column/interleaving corruption. Treat source integrity as evidence; do not silently repair or guess through garbled text.

2. **Grammar of the Shot — continuity chapter**
   - repo source: `canon/sources/gos-ch4-continuity-p93-112.txt`
   - tests sequence/shot-pair knowledge rather than static composition.

3. **Ogilvy — advertising that sells**
   - repo source: `canon/sources/ogilvy-ch2-advertising-that-sells.txt`
   - tests commercial/advertising guidance, claims, heuristics and practitioner rules.

4. **Light: Science & Magic — reflection chapter**
   - repo source: `canon/sources/lsm-ch3-reflection.txt`
   - tests physical/causal photographic knowledge and whether production-oriented source actions remain representable without premature translation into generator instructions.

These four were chosen because they span typography, moving-image continuity, advertising, and photographic physics. Do not substitute a different source without Controller approval.

## VISUAL EVIDENCE POLICY FOR THIS BATCH

Use matching local page images/PDFs where already available and provenance-verifiable. Render ephemerally only; do not commit copyrighted page images.

If a source is visually argued and no matching visual source is available locally:
- do **not** abandon the whole batch;
- mark that source's visual completeness as `not_verified` / `blocked_visual_validation`;
- continue source-faithful text extraction only where the text itself supports the claim;
- do not assert visual completeness;
- record the limitation in the batch issue ledger.

If the text itself is corrupt/garbled enough that claims cannot be extracted faithfully, stop that **source**, record `blocked_source_integrity`, and continue the remaining batch sources. Do not guess through corrupted source text.

## PER-SOURCE PROCEDURE

For each of the four sources, independently:

1. Verify text provenance/integrity as far as available evidence permits.
2. Perform the same CANON-002-style independent visual-evidence pass where matching visuals are available.
3. Produce a fresh SPEC-03 source representation using the existing V0 granularity rule.
4. Produce SourceConceptSystems and SPEC-05 ontology mappings using only existing relation types.
5. Produce SPEC-04 bindings only after source representation is stable.
6. Mechanically validate.
7. Commit a **source-specific pre-history checkpoint** before opening that source's historical probe/audit/atoms.
8. Compare with the sealed historical work for that source.
9. Record disagreements and misses; do not alter the frozen method.

Use task-scoped IDs and separate directories for each source.

## SEALED HISTORICAL MATERIAL

For each source, its old finding/audit/atoms remain sealed until that source's fresh checkpoint exists. Historical comparison is a diagnostic after the fresh pass, not training material.

Known historical findings include:
- `canon/findings/FINDINGS-05-lupton-hierarchy-pass1.md`
- `canon/findings/FINDINGS-06-gos-continuity-pass1.md`
- `canon/findings/FINDINGS-07-ogilvy-pass1.md`
- `canon/findings/FINDINGS-08-lsm-reflection-pass1.md`

Also treat any corresponding migration audits / superseded atoms as sealed for that source until its checkpoint.

## BATCH ISSUE LEDGER

Create `canon/findings/CANON-003-batch-issue-ledger.md`.

Every issue must record:
- plain-English issue;
- source(s) where observed;
- whether directly observed, inferred, or only suspected;
- whether it affects source fidelity, granularity, systems, ontology, bindings, visual completeness, provenance, or Creative IR fit;
- whether it is new, a recurrence of CANON-001/002, or contradicts an earlier concern;
- practical consequence if left unchanged;
- proposed fix **only as a proposal**, not applied during the batch.

Do not count repeated manifestations in one source as independent evidence unless they genuinely are independent cases.

## END-OF-BATCH SYNTHESIS

Only after all four sources are completed or source-blocked, produce `canon/findings/CANON-003-multi-source-synthesis.md` answering:

1. Which CANON-001/002 issues recurred, and in how many materially different sources?
2. Which earlier issues did **not** recur?
3. What new failure modes appeared?
4. Which schema/method changes now have multi-source evidence behind them?
5. Which proposed changes still look like one-book overfitting?
6. Did the V0 granularity rule remain usable across all usable sources?
7. Did the SourceKnowledge / SourceConceptSystem / ontology / binding separation continue to hold?
8. What source shapes produce different knowledge profiles (mechanism-heavy, remedy-heavy, procedural, physical/causal, sequence-level, commercial heuristic)?
9. What should be changed once, after the batch, before broad ingestion?
10. What should deliberately remain unchanged because evidence is still weak?

The synthesis may recommend a consolidated schema/method revision task. It may **not perform that revision**.

## IN SCOPE

- four fresh source extractions under one frozen method
- visual passes where provenance-verifiable local visuals exist
- source-integrity blocking when necessary
- fresh SourceKnowledge, SourceConceptSystems, ontology mappings and operational bindings
- source-specific frozen checkpoints
- post-checkpoint comparison with historical material
- batch issue ledger
- multi-source synthesis
- cross-stream proposals where findings genuinely affect Eval/Production, clearly marked proposed

## OUT OF SCOPE

- no schema or method changes during the batch
- no broad ingestion beyond the four named sources
- no fifth source
- no Canon-consumption experiment
- no evaluator/model benchmarking
- no provider/model selection
- no new copyrighted-source acquisition
- no committing page renders
- no rewriting historical evidence
- no retrospective cleanup of CANON-001/002 knowledge objects as part of this task

## DELIVERABLES

For each source:
- fresh current-schema knowledge files under `canon/knowledge/current/<source>/`
- source-specific findings file
- source-specific pre-history checkpoint

Batch-level:
- `canon/findings/CANON-003-batch-issue-ledger.md`
- `canon/findings/CANON-003-multi-source-synthesis.md`
- `canon/tasks/CANON-003-CONTROLLER-BRIEF.md`
- updated `canon/HANDOFF.md`

**AUTONOMY MODE:** autonomous inside the frozen method. The worker may process all four sources sequentially without returning for approval between books unless a project-wide stop condition occurs.

## RESOURCE BUDGET

- sources: exactly four named existing repo sources
- new source acquisition: none
- paid APIs: ₹0 / $0
- page rendering: ephemeral local only
- storage: text/YAML/Markdown plus temporary renders; no full copyrighted page images committed

## STOP CONDITIONS

Stop the whole task only for:
- need to change schema/method to continue **all** remaining sources;
- need for a new ontology relation/type to represent multiple sources honestly;
- project-wide provenance/legal problem;
- source material integrity issue affecting more than the one source;
- architecture conflict that makes continued extraction misleading rather than merely imperfect.

A problem isolated to one source should normally block/log that source and continue the other three.

## HUMAN APPROVAL TRIGGERS

- any schema/method change during the batch;
- any new source acquisition or substitution;
- any new ontology relation/type;
- broadening beyond the four-source batch;
- any attempt to convert a recurring issue into a project rule before the end-of-batch synthesis.

**RESULT LOCATION:** `canon/tasks/CANON-003-CONTROLLER-BRIEF.md` plus the batch deliverables above.
