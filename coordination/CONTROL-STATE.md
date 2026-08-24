# Control State

**Purpose:** enough to bootstrap a fresh Controller conversation without replaying history.
**Not a diary** — see `coordination/DECISION-LOG.md` for history.

## Product thesis
An intelligence layer above image/video/audio models, optimizing Cost per Accepted Outcome by
combining explicit creative knowledge (Canon) with empirically measured current capability
(Capability Lab) to plan, route, generate, evaluate and repair.

## Current accepted architecture
Normalized Request → Creative IR (Canon-informed) → Production IR (does not exist yet) + Capability
Registry (does not exist yet) → Planner → Execute → Evaluate (technical + creative) → Repair →
Empirical Memory. Object-level separations remain locked in `PROJECT-CONTRACT.md`.

## Workstream boundaries
Canon = durable creative expertise. Eval/Capability Lab = measurement design + empirical current-
model behaviour. Resources = independent media/data. Full definitions: each stream's `CHARTER.md`.

## Current versions
- Creative IR: **SPEC-01 v0.1**, locked for the current phase.
- Source Knowledge schema: **SPEC-03 v0** (SPEC-02 retained as historical evidence).
- Operational Bindings: **SPEC-04 v0**.
- Knowledge Ontology: **SPEC-05 v0**.
- Canon Coverage Map / Curriculum V0: planning documents, not a mandate to ingest everything.
- Capability Registry: not built.
- Eval Battery: not built; EVAL-001 is designing V0.
- External corpus: not yet acquired; RES-001 is now approved to acquire a bounded pilot.

## Canon status
Six sources were processed historically as representation-architecture probes and then re-audited
under the current split. No source has yet been freshly extracted end-to-end directly under
SPEC-03/04/05. `CANON-001` is approved to do exactly one such extraction from the existing Molly
Bang source, validate the shape, compare against the historical audit, and stop.

Canon-consumption / planning experiments are **paused by Controller direction for now**. Existing
experiment documents are retained as design/history, but no worker may run or extend them without a
new approved task.

## Eval status
One prior Devanagari checker-calibration study exists. No battery and no Capability Registry exist.
`EVAL-001` is approved to design a bounded Capability Battery V0 and instrument-calibration plan
using published benchmark methodology + Creative IR requirements + observed failures. It has zero
paid-generation budget and must stop before benchmarking providers.

## Resources status
No external dataset has been acquired yet. `RES-001` is approved as a bounded acquisition pilot:
verify official sources and rights, acquire legitimate media across multiple useful source families,
validate/checksum/manifest it, target 10–15 GB and hard-stop at 20 GB. Raw media is excluded from
git; manifests/reports/scripts remain versioned.

## Current approved tasks
- `canon/tasks/CANON-001.md`
- `eval/tasks/EVAL-001.md`
- `resources/tasks/RES-001.md`

Each worker must operate from its own worktree/branch, produce a Controller Brief, and stop at the
mandatory gates in `shared/AUTONOMY-POLICY.md`.

## Current central hypotheses
The assumptions register remains authoritative. Important unresolved items include whether the
Source Knowledge / Binding split earns its complexity over time, whether explicit Canon materially
improves planning/evaluation in useful settings, whether Canon-derived requirements improve routing
once a Registry exists, whether Empirical Memory predicts later failures, and whether CpAO is the
right operating objective. None should be promoted to fact without the register's evidence bar.

## Cross-stream dependencies
- CANON-001 validates the ingestion shape before scaling source processing.
- EVAL-001 defines what later Capability Lab runs need to measure and which media/instruments they
  require.
- RES-001 supplies independent media and rights/integrity metadata that later Eval/Canon work can
  use without circular selection.
- Routing remains blocked until a Capability Registry exists.

## Current integration checkpoint
Wait for the three Controller Briefs from CANON-001, EVAL-001 and RES-001. Review them together for
cross-stream implications before approving the next tasks. Do not allow a worker's recommended next
step to become automatic work.
