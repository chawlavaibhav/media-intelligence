# CANON-003 — Parallel load rebalance 01

**Status:** Controller-approved execution amendment · 24 Aug 2026

This amendment changes only which worker handles two already-selected, not-yet-started books. It does **not** change the CANON-003 source set, book count, coverage goals, frozen extraction method, SPEC-01/03/04/05, visual-pass method, ontology vocabulary, evidence standards, or end-of-batch synthesis questions.

## Why this rebalance is approved

Lane D completed Books 16–18 while lanes A/B/C still have six fixed books remaining. Leaving an idle worker while preserving the same 18-book source set adds latency without improving experimental validity.

The source-selection decision remains fully precommitted: all books below were already fixed in `CANON-003-PARALLEL-EXECUTION.md` before any parallel-lane result was seen. This amendment therefore does not choose new sources based on emerging findings; it only redistributes execution of sources that were explicitly `not started` at the time of the Controller audit.

## Reassigned books

- **Book 8 — John Alton, _Painting With Light_** moves from Lane A to the rebalance worker.
- **Book 11 — Christopher Kenworthy, _Master Shots_** moves from Lane B to the rebalance worker.

Remaining ownership after this amendment:

- Lane A: Book 7 — Michael Freeman, _The Photographer's Eye_.
- Lane B: Book 10 — Walter Murch, _In the Blink of an Eye_; Book 12 — Michael Ondaatje, _The Conversations_.
- Lane C: Book 15 — Rory Sutherland, _Alchemy_.
- Rebalance worker: Books 8 and 11.
- Lane D's accepted Books 16–18 remain frozen and untouched.

## Why Book 12 is not moved

Lane D independently predicted that an interview-shaped source such as _The Conversations_ might expose its claim-attribution issue. Reassigning that specific book to the same worker after that prediction would make the fresh extraction less clean. Book 12 therefore remains with Lane B.

## Branch / isolation rule

Do **not** continue on `work/canon-003-d`; that branch is accepted evidence and remains untouched until integration.

Use a fresh branch from the common parallel base:

`work/canon-003-rebalance-d`

The rebalance worker may read only the same shared starting material allowed by the original parallel amendment plus its two assigned source files and its own new rebalance-lane files. It must not read Lane A/B/C fresh findings, issue files, or checkpoints before completing the relevant fresh checkpoint. It must also not use Lane D's accepted issue file as a checklist while extracting Books 8 or 11.

Because the human operator may reuse the same external agent identity, perfect cognitive erasure of prior Lane D work cannot be guaranteed. The safeguard is therefore procedural and auditable: fixed sources, fresh branch from the common base, no reading of other lanes' fresh work, no reading of Lane D issue/checkpoint files as extraction prompts, and book-specific fresh checkpoints before historical comparison. Record this execution amendment in the rebalance lane checkpoint.

## Per-book procedure

For Books 8 and 11, follow the unchanged CANON-003 procedure exactly:

1. verify source identity/provenance and integrity;
2. choose the coherent representative section;
3. run the frozen visual-evidence pass where matching visuals exist;
4. produce fresh SPEC-03 SourceKnowledge;
5. produce SourceConceptSystems and SPEC-05 mappings using only existing vocabulary;
6. produce SPEC-04 bindings after the source representation is stable;
7. mechanically validate;
8. commit and push a book-specific fresh checkpoint before opening historical extraction/audit material for that book;
9. only then compare historical material if any exists;
10. record issues in rebalance-owned files without changing the method.

Use source-specific knowledge directories. Create rebalance-owned findings/checkpoint files rather than editing Lane A/B/D files.

## Stop / handoff

After Books 8 and 11 are complete, validated, historically reconciled, committed and pushed, STOP and return to Controller. Do not merge into another lane, do not edit shared batch synthesis files, do not change schemas, and do not begin a 19th book.
