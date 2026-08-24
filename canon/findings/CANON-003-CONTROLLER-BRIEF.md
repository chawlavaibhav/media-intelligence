# CANON-003 — Controller brief

**Date:** 24 Aug 2026  
**Decision status:** final synthesis decision for the 16-book batch; pending integration PR verification/merge.

## Bottom line

CANON-003 succeeded at its real purpose: it stressed the current Canon method across enough different source shapes to distinguish architectural strengths from method weaknesses.

**Controller decision:** retain the current three-layer Canon architecture. Do not collapse SourceKnowledge into product bindings and do not redesign the schema around isolated edge cases.

The next Canon revision should be one coordinated **Post-Extraction Audit Gate** that runs after source truth is frozen and before cross-source promotion or product use.

## Evidence base

The integrated accepted set contains 16 books and, at the last complete strict integration run, 505 SourceKnowledge objects, 54 SourceConceptSystems, 417 ontology terms, 53 concepts and 111 operational bindings.

Books 11 (*Master Shots*) and 12 (*The Conversations*) were deliberately deferred once the batch exceeded its required minimum of 15 usable books. They remain reserve stress-test sources, not failures.

Only books 1–3 had historical extraction comparators. Conclusions based on old-vs-new extraction therefore apply to that subset, not automatically to all 16.

## What is now well-supported

1. **Source truth must stay separate from current product use.** Legitimate zero-Creative-IR-binding sources occurred, while more bindable material was not necessarily better evidenced.
2. **The systems layer is useful.** It handled sequence, priority, checklist, interacting-set, design and creative-process structures without a batch-time vocabulary change.
3. **Visual risk is representation-dependent.** No-page EPUBs, false/reflowed pages, image-only headings/text, destroyed colour information and underdetermined figure pairings are different failure mechanisms. Raw image count is a bad proxy.
4. **Evidence origin needs better structure.** Own measurement, third-party studies, claimed measurement without supplied result and mixed evidence currently collapse into caveats that cannot be aggregated reliably.
5. **Source id is not independence.** Companion books by the same authors must not count as independent convergence merely because their source ids differ.
6. **The old mandatory-binding process asked one useful question in the wrong place.** Product-fit attention should return as a post-source audit, not as a requirement to bind every source object.
7. **Committed mechanical validation is required.** Lane-local ephemeral validators missed 24 defects that the integration validator found.

## One revision to make next

### CANON Method v0.2 — Post-Extraction Audit Gate

After SourceKnowledge/systems/ontology are stable and before cross-source promotion or downstream use, require four explicit audits:

- source/visual integrity;
- evidence and claim origin;
- current application/product fit, where `no current binding` is valid;
- source lineage and independence.

As part of the same revision, require an explicit technology-contingency check for older technical sources and use the committed validator as the mechanical acceptance instrument.

The follow-on task should propose the **minimum** schema changes needed for evidence origin and source lineage, test them against the existing 16-book corpus, and avoid unrelated schema expansion.

## What not to change yet

Do not let single/few-source issues drive the revision: Murch's weighted priorities, traversal-with-return hierarchy, long-range transcript dependencies, human/organisational executability, or additional ontology relation types. Keep them logged and wait for recurrence or downstream empirical pressure.

Do not translate physical-production remedies into generative prompts without evidence. Do not force a binding merely to make knowledge look product-relevant. Do not treat object count, image count, or number of agreeing source ids as evidence strength.

## Integration note

The final strict run, after correcting an over-strict validator assumption, left exactly 24 data errors in three directories: one malformed YAML scalar in *Made to Stick* and 23 remedy terms lacking SPEC-05's required `executable_by` field across *Scientific Advertising* and *Alchemy*.

Integration repaired only those mechanical defects. The YAML scalar was re-quoted without changing meaning. The 23 remedies were assigned `executable_by: [unknown]`, the conservative allowed value, rather than inventing a generative or deterministic executor. Original lane checkpoint history remains untouched.

The temporary auto-running GitHub Actions workflow used during validator development was removed after it produced noisy failure notifications. The validator and regression tests remain committed; the workflow does not.

## Next sequence

1. Complete controlled integration verification and merge PR #4.
2. Open the follow-on CANON Method v0.2 task for the Audit Gate; do not modify SPEC-03/04/05 inside CANON-003.
3. After the method revision is tested against the integrated corpus, resume Canon-consumption/RAG experiments so they consume the hardened representation rather than the pre-synthesis method.
