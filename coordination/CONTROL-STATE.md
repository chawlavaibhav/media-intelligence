# Control State

**Purpose:** enough to bootstrap a fresh Controller conversation without replaying history.  
**Not a diary** — see `coordination/DECISION-LOG.md` for history.  
**Snapshot refreshed:** 24 Aug 2026.

## Product thesis
An intelligence layer above image/video/audio models, optimizing Cost per Accepted Outcome by combining explicit creative knowledge (Canon) with empirically measured current capability (Capability Lab) to plan, route, generate, evaluate and repair.

## Current accepted architecture
Normalized Request → Creative IR (Canon-informed) → Production IR (does not exist yet) + Capability Registry (does not exist yet) → Planner → Execute → Evaluate (technical + creative) → Repair → Empirical Memory.

Object-level separations remain locked in `PROJECT-CONTRACT.md`. Canon-consumption / planning experiments remain paused unless the Controller explicitly reopens them.

## Workstream boundaries
Canon = durable creative expertise. Eval / Capability Lab = measurement design + empirical current-model behaviour. Resources = independent media/data. Full definitions: each stream's `CHARTER.md`.

## Current versions / approvals
- Creative IR: **SPEC-01 v0.1**, locked for the current phase.
- Source Knowledge: **SPEC-03 v0**.
- Operational Bindings: **SPEC-04 v0**.
- Knowledge Ontology: **SPEC-05 v0**.
- Capability Battery V0 specification: **Controller-approved under EVAL-001**; seven dimensions and instrument-calibration specification are approved as measurement design, not as empirical results.
- Identity rubric V0: frozen under EVAL-002 for later calibration; frozen does not mean calibrated.
- M1b Devanagari generation-item design V0: approved as a design only; no final linguistically validated item set exists.
- Capability Registry cross-stream schema: still proposed/deferred; **Registry does not exist yet**.
- Production IR: does not exist yet.

## Canon status — CANON-003 active in parallel
CANON-003 is the current Canon stress batch under the frozen SPEC-03/04/05 extraction method.

The authoritative pre-parallel checkpoint on `work/canon` records **5 usable books complete** with no partially extracted book: *Grammar of the Shot*, *Ogilvy on Advertising*, *Light: Science & Magic*, *Interaction of Color*, and *The Vignelli Canon*. *Thinking with Type* was blocked by source-structure corruption and is not counted.

Controller approved `canon/tasks/CANON-003-PARALLEL-EXECUTION.md` to finish the remaining fixed assignments through a preferred total of **18 usable books**. Four isolated branches exist: `work/canon-003-a`, `work/canon-003-b`, `work/canon-003-c`, and `work/canon-003-d`.

**Lane D is Controller-audited complete and contributes three usable books: Books 16–18.** The branch is six commits ahead of the common parallel base and contains the required lane checkpoint/issues records plus complete source representations for *Creativity, Inc.* ch.5, *Art & Fear* pp.1–21, and *Building a StoryBrand* ch.1–3. That brings the currently Controller-confirmed usable count to **8** (the five pre-parallel books plus Lane D's three), pending the other lanes and final integration validation.

The earlier Book 16 checkpoint-integrity concern is resolved by durable Git history, not by retrospective prose alone. The fresh Book 16 checkpoint `b7f0d47` is exactly one commit after the common base and contains only Book 16 source-representation files. Book 17's fresh checkpoint is `75e4da1`, with the Book 16 findings/history record landing between those checkpoints; Book 18's fresh checkpoint is `f0127e4`, with Book 17 findings/history landing before it; Book 18 findings/history land only after `f0127e4`. This satisfies the frozen per-book rule: fresh extraction was committed and pushed before historical comparison for that book. **No method deviation is required.**

Lane D stayed within its ownership boundary: compare-to-base shows only Lane D findings/checkpoint files and source-specific knowledge directories; the locked shared batch ledger, synthesis, Controller Brief and Canon handoff were not changed. The returned content is architecture-disciplined: process/organisational knowledge is not forced into Creative IR, extractor-synthesised systems remain marked as synthesis, visual evidence is explicitly inspected, source/evidence weaknesses are retained, and proposed schema implications are recorded without changing the frozen method.

Lanes A/B/C remain under separate audit as they return. Lanes must remain isolated during fresh extraction. Shared batch synthesis files stay locked until one fresh integration session merges/reconciles the reviewed lanes and produces the end-of-batch synthesis. Parallel lanes do not change schemas or run Canon-consumption experiments.

## Eval status — EVAL-003 finalization pass active
**EVAL-001 and EVAL-002 are closed and merged to `main`.**

EVAL-003's first correction return fixed the major validity problems from the first review. The returned package now correctly treats the 67% figure as **cross-dataset annotation disagreement**, not human performance; uses one-to-one matching; labels the mark-removal diagnostic mechanically; reconciles candidate arithmetic; uses two blind readers in the reference design; materialises canonical hashed crops for both humans and future checkers; removes committed machine-specific paths; and preserves the 27-case checker-regression result.

The correction return also exposed a consequential composition fact: under the original cross-dataset-overlap exclusion rule, the selected 54-item pack contains **53 Marathi, 1 language-unstated item, and 0 Hindi**, because all 173 Hindi-labelled IndicSTR12 records are in the shared-image overlap. The checker and observed production failure are Hindi-facing, so spending the first human calibration budget on a zero-Hindi pack would create an avoidable transfer assumption.

Controller therefore opened `eval/tasks/EVAL-003-FINALIZATION-PASS.md`. **Primary V0 decision: use a Hindi-focused qualification pack, target 54 Hindi-labelled unique photographs, admitting a shared photograph once rather than treating the two dataset copies as independent.** Source labels remain provenance/selection metadata only; the later reference still comes from two independent blind Hindi-competent readers. Marathi stress testing is deferred and must be reported separately if later opened. BSTD remains untouched as the independent lineage reserve.

The return is **not yet merge-ready and human/API calibration remains unapproved** because final bounded defects remain:
- `work/eval` did not merge current `main` before its correction work and must synchronize normally without rewriting history;
- the production matcher is one-to-one, but the required fabricated adversarial regression proving one B region cannot be reused is missing;
- the returned altered-target confirmation rule is impossible with only the two readers because both establish every agreed reference; finalization fixes this by freezing the reference first, then allowing either reader to perform the non-reference-changing validity check;
- current EVAL-003 prose still contains stale pre-correction statements about crop materialisation and must be made internally consistent;
- the Eval→Resources proposal covers the scene-photo discrepancy but still needs the locally paired 375/176 counts and the denominator-specific 173/176 overlap clarification.

The finalization pass authorizes **zero human/API/model/generation spend**. It must return to Controller after a bounded verification suite. **Do not start readers, checker APIs, EVAL-004, BSTD selection, Registry work, or capability runs.**

## Resources status — RES-002 closed
**RES-001 and RES-002 are closed and merged to `main`.** No Resources task is currently active.

The repository has a bounded external research/evaluation corpus plus provenance, integrity and acquisition records. Standing constraints remain:
- source labels are observations, not automatic project ground truth;
- media rights remain **internal research and evaluation only** unless separately cleared;
- BSTD is the independent Devanagari lineage reserve relative to the two related CVIT / IIIT Hyderabad sources;
- transient/member-level acquisition is an approved storage method, not a rights grant.

Eval may propose factual corrections through an Eval-owned `PROPOSED-INTEGRATION-CHANGE` file; Eval must not edit Resources-owned records directly.

## Current approved work
- `canon/tasks/CANON-003.md`
- `canon/tasks/CANON-003-PARALLEL-EXECUTION.md`
- `eval/tasks/EVAL-003.md`
- `eval/tasks/EVAL-003-CORRECTION-PASS.md`
- `eval/tasks/EVAL-003-FINALIZATION-PASS.md`

There is **no active Resources task** and no approved EVAL-004.

## Current central hypotheses
The assumptions register remains authoritative. Important unresolved items still include whether the Source Knowledge / Binding split earns its complexity over time, whether explicit Canon materially improves planning/evaluation, whether Canon-derived requirements improve routing once a Registry exists, whether Empirical Memory predicts later failures, and whether CpAO is the right operating objective. None should be promoted to fact without the register's evidence bar.

## Current integration gates
1. **Canon:** Lane D is reviewed and accepted as three usable books; keep it isolated and unmerged until the other lane returns are reviewed. Audit A/B/C against the same frozen method, then use one fresh Canon integration session to merge/reconcile, mechanically validate all outputs, count recurrence and synthesize. No schema changes or Canon-consumption experiments during the batch.
2. **Eval:** wait for the EVAL-003 finalization return. Human readers, checker roster, API spend and calibration remain blocked. The primary V0 calibration pack is Controller-directed to be Hindi-focused with unique photograph hashes.
3. **Resources:** closed; act only on a Controller-approved cross-stream correction or a new sourcing task.
4. **Architecture:** no Capability Registry, Production IR, routing system, or Canon-consumption experiment is authorized by the current work.
