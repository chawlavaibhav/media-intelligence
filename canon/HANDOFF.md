# Canon — Handoff

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Plain English, minimum
sufficient wording, no invention, evidence separated from inference.

**PURPOSE:** Build and test durable creative/media expertise consumable by a reasoning model.

**CURRENT STATE:** SPEC-01 (Creative IR) through SPEC-05 (Ontology) exist and are locked/frozen.
Six sources were partially processed as **representation-architecture probes** (not a Canon coverage
sample — see `findings/DIRECTION-RESET-01-CANON-ROLE.md`), then re-audited into the current schema
shape in `knowledge/migration/`. Original pre-SPEC-03 atom files remain at
`knowledge/atoms-v1-superseded/`.

**CANON-001 is complete.** The first fresh end-to-end extraction under SPEC-03/04/05 now exists at
`knowledge/current/molly-bang/` — 55 SourceKnowledge objects, 6 SourceConceptSystems, 26 ontology
terms, 13 bindings. It validates against SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer
constraints. Awaiting Controller review; not yet merged to `main`.

Canon-consumption experiments remain paused until the Controller explicitly reopens them.

**CURRENT APPROVED DECISIONS:** SPEC-01 v0.1 locked. SPEC-03/04/05 supersede SPEC-02 conceptually
(SPEC-02 retained as evidence). Direction reset restoring the Canon/Capability-Lab/Production
boundary accepted. CANON-001 Controller clarifications of 24 Aug 2026 (naming convention, task-scoped
IDs, source-local ontology scope, membership via `members[]` only, honest handling of missing figures
and OCR damage, audit blindness until checkpoint) applied in full.

**LAST COMPLETED TASK:** `CANON-001`. Checkpoint `1383abe` (pre-audit, frozen), completion `21f6e79`.
See `tasks/CANON-001-CONTROLLER-BRIEF.md` and
`findings/CANON-001-current-schema-extraction-findings.md`.

**CURRENT TASK / QUEUE:** None. CANON-001 is finished and no next task is approved. Do not
self-assign a second source or an experiment.

**IMPORTANT OBSERVATIONS:**
- **SPEC-03's `scs_mb_001` worked example is factually wrong about Molly Bang.** It states *"The
  source never states this as a general claim."* She states it on page 58 and again across pages
  58–60. CANON-001 records it as `source_explicit`. The spec has **not** been edited — Controller
  decision pending. Do not treat SPEC-03's worked examples as verified against their sources.
- **Granularity is unsettled and it matters.** Two defensible conventions produced 19 objects
  (historical) and 55 objects (CANON-001) from the same fifty pages. Settle this before a second
  source.
- **SPEC-03 has no relation type for claims that are adjacent but not logically related.** 13
  drafted relations were removed rather than forced into a wrong type; four objects carry empty
  relation lists as a result. SPEC-05 covers this at the term layer with `related_to`; SPEC-03 does
  not cover it at the claim layer.
- **SPEC-05 Layer 1 has no term kind for a principle**, and this source is almost entirely
  principles. Its real vocabulary sits in `property`/`entity` terms, outside the failure/repair spine
  the book-to-failure join depends on.
- The old admission rule ("no IR consumer → discard") caused exclusion and distortion. Do not
  reintroduce that coupling. CANON-001's 55%-unbound profile is the intended behaviour.
- Lupton's EPUB extraction has column interleaving and must not be trusted without visual recovery.
- Source knowledge must stay source-faithful; product bindings are separate and optional.
- Missing coverage in processed material is never a claim about what Canon can never know.

**OPEN QUESTIONS:**
- Granularity convention (Controller decision 4 in the CANON-001 brief).
- Whether `distinct_from` is within a worker's local authority. Two negative findings are unwritten.
- Whether to add the one figure-only object the historical audit recovered and CANON-001 missed.
- Whether the thin ontology yield is a property of this source or of the ontology layer. One source
  cannot tell them apart.
- Runtime Canon consumption shape remains unresolved. No test may be run without a new approved task.

**DEPENDENCIES:** Ten pages of this source carry claims but have no rendered figure (53, 61, 72, 73,
82, 83, 85, 88, 89, 90). Half the CANON-001 extraction rests on text alone as a result. Routing work
remains downstream of Eval's future Capability Registry.

**PROPOSED CROSS-STREAM CHANGES:** `PROPOSED-INTEGRATION-CHANGE-CANON-001.md` — four near-minimal
picture pairs offered to Eval for its **deferred** creative-fitness list, explicitly not for
Capability Battery V0 (EVAL-001 clarification §2 places creative judgement outside V0). Proposed, not
accepted.

**NEXT APPROVED TASK:** None. Wait for Controller review of CANON-001.
