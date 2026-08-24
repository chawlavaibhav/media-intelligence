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

Controller approved `canon/tasks/CANON-003-PARALLEL-EXECUTION.md` to finish the remaining fixed assignments through a preferred total of **18 usable books**. Four isolated branches exist:

- `work/canon-003-a`
- `work/canon-003-b`
- `work/canon-003-c`
- `work/canon-003-d`

Current branch audit: lanes A/B/C remain identical to the common parallel base. Lane D is **one commit ahead** with the six Book 16 (*Creativity, Inc.*, chapter 5) knowledge/provenance files. The content is provisionally architecture-disciplined: converted-EPUB provenance weakness is explicit; the no-evidentiary-figure result is recorded rather than invented around; synthesized source systems are marked as extractor synthesis; Creative IR is not forced; and Production IR implications are parked rather than translated.

**Book 16 is not yet counted as a completed usable post-split book.** The Lane D issue file and lane checkpoint required by the parallel contract are not present on GitHub yet. In addition, the provenance file says historical material was searched “after this checkpoint,” while the branch currently has only one reachable post-base commit. Until the lane preserves/reconciles the required fresh-before-historical checkpoint evidence, treat this as a provisional worker checkpoint, not an accepted completed book. Do not redo the extraction merely for cleanliness; record the method deviation if the sealed checkpoint was amended/squashed and enforce the rule on subsequent books.

Lanes must remain isolated during fresh extraction. Shared batch synthesis files are locked until one fresh integration session merges/reconciles the lanes and produces the end-of-batch synthesis. Parallel lanes do not change schemas or run Canon-consumption experiments.

## Eval status — EVAL-003 correction pass active
**EVAL-001 and EVAL-002 are closed and merged to `main`.**

EVAL-003 prepared a real Devanagari checker-calibration readiness package on `work/eval` at zero API/human spend. Useful parts include deterministic candidate selection, hash-based deduplication, an untouched BSTD reserve, per-item checker targets, and 27 historical regression cases with no judgement mismatch.

The first EVAL-003 return is **not approved for merge or human/API calibration yet**. Controller review found bounded validity/portability issues: cross-dataset annotation disagreement was over-interpreted as a human-performance ceiling; region matching was not one-to-one; a Unicode mark-removal heuristic was mislabelled as linguistic “convention”; candidate-count prose mixed hashes and source records; Hindi/Marathi composition was not measured; the human protocol depended on one reader; canonical crop materialisation was deferred; committed evidence contained machine-specific absolute paths; and a Resources cross-stream correction still needs to be filed.

`eval/tasks/EVAL-003-CORRECTION-PASS.md` is now the authoritative correction contract. It keeps the task as **EVAL-003**, requires **two independent blind readers in the future protocol**, requires crop identity to be solved before any human time is approved, and still authorizes **zero human/API/model spend**. The worker must return to Controller after the correction pass. **Do not start calibration or EVAL-004.**

## Resources status — RES-002 closed
**RES-001 and RES-002 are closed and merged to `main`.** No Resources task is currently active.

The repository now has a bounded external research/evaluation corpus plus provenance, integrity and acquisition records. Important standing constraints remain:

- source labels are observations, not automatic project ground truth;
- media rights remain **internal research and evaluation only** unless separately cleared;
- BSTD is the clean independent Devanagari lineage reserve relative to the two related CVIT / IIIT Hyderabad sources;
- transient/member-level acquisition is an approved storage method, not a rights grant.

Eval may propose cross-stream factual corrections through an Eval-owned `PROPOSED-INTEGRATION-CHANGE` file; Eval must not edit Resources-owned records directly.

## Current approved work
- `canon/tasks/CANON-003.md`
- `canon/tasks/CANON-003-PARALLEL-EXECUTION.md`
- `eval/tasks/EVAL-003.md`
- `eval/tasks/EVAL-003-CORRECTION-PASS.md`

There is **no active Resources task** and no approved EVAL-004.

## Current central hypotheses
The assumptions register remains authoritative. Important unresolved items still include whether the Source Knowledge / Binding split earns its complexity over time, whether explicit Canon materially improves planning/evaluation, whether Canon-derived requirements improve routing once a Registry exists, whether Empirical Memory predicts later failures, and whether CpAO is the right operating objective. None should be promoted to fact without the register's evidence bar.

## Current integration gates
1. **Canon:** audit each lane return against the frozen method as it lands. Lane D Book 16 is currently provisional for the checkpoint-integrity reason above. Do not merge/synthesise the parallel lanes until all usable assigned work is reviewed or a documented source block requires a Controller decision. Then use one fresh integration session for CANON-003 synthesis.
2. **Eval:** wait for the bounded EVAL-003 correction return. Do not approve human readers, checker roster, API spend, or calibration until the corrected package passes Controller review.
3. **Resources:** closed; only reopen if a Controller-approved cross-stream correction or new sourcing need warrants a new task.
4. **Architecture:** no Capability Registry, Production IR, routing system, or Canon-consumption experiment is authorized by the current work.
