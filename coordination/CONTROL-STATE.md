# Controller State

**Updated:** 24 Aug 2026

## Architecture state

- Source Knowledge: **SPEC-03 v0**.
- Operational Bindings: **SPEC-04 v0**.
- Knowledge Ontology: **SPEC-05 v0**.
- Capability Battery V0: Controller-approved under EVAL-001 as measurement design, not empirical capability data.
- Identity rubric V0: frozen under EVAL-002 for later calibration; frozen does not mean calibrated.
- M1b Devanagari generation-item design V0: approved design only; no final linguistically validated generation-item set exists.
- Capability Registry cross-stream schema remains proposed/deferred; **Registry does not exist yet**.
- Production IR does not exist yet.

## Canon status — CANON-003 active

CANON-003 remains a frozen-method 18-usable-book stress batch. The fixed source set has not changed.

**Controller-accepted usable books: 13 / 18.**

- Five pre-parallel usable books: *Grammar of the Shot*, *Ogilvy on Advertising*, *Light: Science & Magic*, *Interaction of Color*, *The Vignelli Canon*.
- Lane A accepted: Book 6 *Making and Breaking the Grid*; Book 7 Michael Freeman, *The Photographer's Eye: A Graphic Guide* (2013). The inventory had misidentified the preselected local artifact as the 2007 *The Photographer's Eye*; final integration must preserve the corrected identity.
- Lane C accepted: Book 13 *Scientific Advertising*; Book 14 *Made to Stick*; Book 15 *Alchemy*.
- Original Lane D accepted: Books 16–18 — *Creativity, Inc.*, *Art & Fear*, *Building a StoryBrand*.
- *Thinking with Type* was blocked by structural text corruption and does not count as usable.

Execution rebalance remains in force without changing the selected 18-book set:

- Lane A is stopped; Book 8 *Painting With Light* moved to `work/canon-003-rebalance-d`.
- Lane C is stopped.
- Lane B owns Books 9, 10 and 12; Book 11 *Master Shots* moved to `work/canon-003-rebalance-d`. Latest worker checkpoint reports Books 9 and 10 complete and Book 12 in progress; those books are not yet Controller-accepted.
- Rebalance worker owns Books 8 and 11.
- Accepted A/C/D branches remain untouched until the dedicated final integration session.

No schema, granularity, visual-pass, ontology-vocabulary, or Canon-consumption change is permitted during the batch. Final integration must independently revalidate every per-book output before CANON-003 closes.

Durable A/C review: `coordination/CANON-003-LANE-A-C-AUDIT.md`.

## Eval status — EVAL-003 readiness merged

**EVAL-001, EVAL-002 and EVAL-003 readiness are merged to `main`.** EVAL-003 merged through PR #3 on 24 Aug 2026 after Controller audit and final documentation cleanup.

Authoritative EVAL-003 state:

- Primary V0 is Hindi-focused: **173 eligible Hindi-labelled unique photographs → 54 selected → 54 distinct photograph hashes**.
- Shared CVIT photographs are admitted once, never counted twice. The two CVIT releases are one source lineage for independence claims.
- Dataset transcriptions are evidence/provenance, **not project ground truth**. On 1,082 one-to-one matched regions the two releases agree 725 times and disagree 357 times; this is cross-dataset disagreement, not human-performance evidence and not an evaluator threshold.
- Canonical crops are materialised; human reviewers and future checkers reference the same crop bytes/hashes.
- Reference construction uses **two independent blind Hindi-competent readers**. Exact agreement forms the strict reference. After references are frozen, either reader may perform the separate altered-target validity check; that check cannot change the reference.
- Agent verification recorded 27/27 historical checker cases re-scored with 0 judgement mismatches; matcher adversarial self-test, crop geometry, crop identity, blinding and local harness checks passed before merge.
- BSTD remains untouched as the independent Devanagari lineage reserve.
- No human review, checker API/model run, generator run, capability result, Registry entry, EVAL-004 work or new acquisition was performed by EVAL-003 readiness.

The active findings file is now an authoritative current-state summary; superseded zero-Hindi, single-reader and browser-crop states survive only in Git history.

**Next Eval gate is not more readiness cleanup.** It is a Controller decision whether to authorize approximately **3.5–4.5 hours across two Hindi-competent readers**. Checker roster/API spend remains a separate later approval. EVAL-004 and Registry work remain unopened.

## Resources status — RES-002 closed

RES-001/002 are closed and merged. The corpus remains internal research/evaluation material unless separately cleared.

EVAL-003 produced `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`, containing factual downstream corrections about:

1. IndicSTR12 being full scene photographs with multiple annotated regions rather than pre-cropped word images;
2. 375 IndicSTR12 + 176 IIIT-ILST locally paired image+annotation records versus total media acquired;
3. the distinction between 173/1,390 full-source overlap and 173/176 overlap within the locally paired IIIT subset.

Eval did not edit Resources-owned evidence. Controller may action or reject that proposal separately.

## Current integration gates

1. **Canon:** finish and audit B plus the rebalance worker, then run one fresh CANON-003 integration/synthesis session. No schema revision or Canon-consumption experiment before that synthesis.
2. **Eval:** EVAL-003 readiness is complete and merged. Human calibration remains **not started** pending explicit authorization of two Hindi-competent readers. Checker roster/API spend is separately gated.
3. **Resources:** closed unless the Controller actions the pending EVAL-003 factual correction proposal or opens a new sourcing task.
4. **Architecture:** Capability Registry, Production IR, routing system and Canon-consumption/training experiments remain unapproved/not implemented.
