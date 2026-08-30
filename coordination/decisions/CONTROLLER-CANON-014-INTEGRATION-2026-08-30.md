# Controller Decision — CANON-014 Integration — 2026-08-30

**Status:** ACCEPTED FOR MERGE  
**Role:** Writer Controller  
**Target:** PR #68, `work/canon-014-final-full-canon`

## Decision

CANON-014 is accepted as the project's full durable Canon reconciliation and is authorised for
merge to `main`, subject to the bounded Level-1 Governor review recorded at
`governance/reviews/GOV-L1-CANON-014-FULL-CORPUS.md`.

This decision is independent of the upcoming reasoning-model experiment. Merging Canon does not
authorise any model/provider call and does not itself define the T2B treatment.

## Integrated state

- **24 accepted/live Canon sources** total: the previous 19 plus five newly admitted Indian-context
  sources.
- **18 durable HOLD/candidate sources** retained under `canon/candidates/canon-014/`; structural
  validity does not convert them into accepted knowledge.
- **1,028 grounded, ungraded, uncalibrated Q&A items** retained under `canon/qa/canon-014/`.
- The corpus index at `canon/knowledge/CANON-CORPUS-INDEX.yaml` records separate fingerprints for
  accepted Canon, the full knowledge corpus, and the Q&A corpus.
- PR #68 supersedes PR #66 and PR #67 for integration purposes; those donor PRs must not be merged.

## Retrieval boundary

This merge does **not** enable HOLD/candidate retrieval in ordinary runtime. Runtime continues to
read `canon/knowledge/current/**` unless a later, explicitly frozen experiment/runtime change says
otherwise.

A future experiment may deliberately expose the full status-aware corpus and Q&A, but must record the
exact fingerprints used and preserve `source_status` so HOLD material cannot masquerade as accepted.

## Known issues carried, not repaired here

- Three pre-existing schema defects remain in accepted
  `sutherland-alchemy-introduction` (missing concept-system provenance).
- `tests/test_request_freeze_gates.py` has the pre-existing CANON-010 collection defect documented
  by CANON-014; the full pytest suite therefore still requires a separate owning fix.
- Devanagari/Indic typography remains an open Canon coverage gap.
- Several held sources still require source/visual inspection before any admission decision.

## Not authorised by this decision

- no model/provider call;
- no paid experiment;
- no Capability Registry row;
- no visual-pass programme over the 18 HOLD sources;
- no Production IR / Planner implementation;
- no runtime candidate-retrieval change.
