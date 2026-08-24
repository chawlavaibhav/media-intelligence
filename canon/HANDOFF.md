# Canon — Handoff

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Plain English, minimum
sufficient wording, no invention, evidence separated from inference.

**PURPOSE:** Build and test durable creative/media expertise consumable by a reasoning model.

**CURRENT STATE:** SPEC-01 (Creative IR) through SPEC-05 (Ontology) exist and are locked/frozen.
Six sources were partially processed as **representation-architecture probes** (not a Canon coverage
sample — see `findings/DIRECTION-RESET-01-CANON-ROLE.md`), then re-audited into the current schema
shape in `knowledge/migration/`. Original pre-SPEC-03 atom files remain at
`knowledge/atoms-v1-superseded/`.

**CANON-001 is complete and Controller-APPROVED (24 Aug 2026).** The first fresh end-to-end
extraction under SPEC-03/04/05 exists at `knowledge/current/molly-bang/` — 55 SourceKnowledge
objects, 6 SourceConceptSystems, 26 ontology terms, 13 bindings. It validates against SPEC-03
rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints. Not yet merged to `main`.

Canon-consumption experiments remain paused until the Controller explicitly reopens them.

**CURRENT APPROVED DECISIONS:** SPEC-01 v0.1 locked. SPEC-03/04/05 supersede SPEC-02 conceptually
(SPEC-02 retained as evidence). Direction reset restoring the Canon/Capability-Lab/Production
boundary accepted. CANON-001 Controller clarifications of 24 Aug 2026 (naming convention, task-scoped
IDs, source-local ontology scope, membership via `members[]` only, honest handling of missing figures
and OCR damage, audit blindness until checkpoint) applied in full.

**CANON-001 review decisions, 24 Aug 2026 — binding on the next extraction:**

1. **SPEC-03's Molly Bang worked example is confirmed incorrect.** The Controller will correct it.
   Canon does not edit it. Until it is corrected, do not treat SPEC-03's worked examples as verified
   against their sources.
2. **The missed page-87 figure-only claim stays out.** CANON-001 is preserved as evidence of the
   miss; a later visual-completeness task handles it explicitly. It is not an outstanding defect and
   must not be quietly patched.
3. **`distinct_from` is permitted in the SPEC-05 ontology layer**, since it is already part of that
   relation vocabulary. It is **not** permission to use it inside SPEC-03 `intra_source_relations`,
   which has its own separate closed vocabulary.
4. **V0 granularity rule — apply this to the next source.** Split into a separate SourceKnowledge
   object when a claim can meaningfully be **retrieved, supported, contradicted or qualified
   independently**. Do **not** split merely because the source offers another example, explanation or
   restatement. Do not target a particular object count in either direction.
5. **Bang's visual minimal-pair candidates may go to Eval's deferred creative-evaluation list**,
   marked as source-asserted expected readings, not validated human ground truth.

**LAST COMPLETED TASK:** `CANON-001` — substantive work approved 24 Aug 2026, all five review
questions closed, housekeeping corrections applied. Not yet merged to `main`.

- **`1383abe`** — the frozen pre-audit checkpoint. Stable reference. The four extraction files have
  been byte-identical since this commit and must stay that way.
- Later commits on `work/canon` carry the historical comparison, the Controller Brief, the approval
  record and housekeeping only. No SHA for these is quoted here, because it moves; read the tip of
  `work/canon`.

See `tasks/CANON-001-CONTROLLER-BRIEF.md` and
`findings/CANON-001-current-schema-extraction-findings.md`.

**CURRENT TASK / QUEUE:** None. CANON-001 is finished and no next task is approved. Do not
self-assign a second source or an experiment.

**IMPORTANT OBSERVATIONS:**
- **SPEC-03's `scs_mb_001` worked example is factually wrong about Molly Bang.** It states *"The
  source never states this as a general claim."* She states it on page 58 and again across pages
  58–60. CANON-001 records it as `source_explicit`. **The Controller has confirmed the error and
  approved the correction (decision 1); the Controller makes the edit, not Canon.** Until the edit
  lands, do not treat SPEC-03's worked examples as verified against their sources.
- **Granularity is now decided (decision 4), and its origin matters.** Two defensible conventions
  produced 19 objects (historical) and 55 objects (CANON-001) from the same fifty pages. The V0 rule
  exists because of that gap; apply it to the next source and report whether it holds.
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

**OPEN QUESTIONS:** All five CANON-001 review questions are **closed** (decisions 1–5 above).
Nothing below blocks the next task; these are forward-looking items.
- **Does the V0 granularity rule actually work?** Decision 4 directs that it be tested on the next
  source. NOT VERIFIED whether CANON-001's 55 objects satisfy it — the rule postdates the extraction
  and no re-audit was performed. Do not assume they do.
- **Optional, not blocking:** whether to write the two `distinct_from` relations decision 3 now
  permits — `space_reads_as_flat` vs `reads_as_floating`, and `monotony_of_relentless_repetition` vs
  `boring_and_heavy` (see `findings/CANON-001-...md` §8). Left unwritten because CANON-001 was
  already approved.
- Whether the thin ontology yield is a property of this source or of the ontology layer. One source
  cannot tell them apart.
- Runtime Canon consumption shape remains unresolved. No test may be run without a new approved task.

**DEPENDENCIES:** Ten pages of this source carry claims but have no rendered figure (53, 61, 72, 73,
82, 83, 85, 88, 89, 90). Half the CANON-001 extraction rests on text alone as a result. Routing work
remains downstream of Eval's future Capability Registry.

**CROSS-STREAM CHANGES:** `PROPOSED-INTEGRATION-CHANGE-CANON-001.md` — **APPROVED 24 Aug 2026**.
Four near-minimal picture pairs go to Eval's **deferred** creative-evaluation list, not to Capability
Battery V0 (EVAL-001 clarification §2 places creative judgement outside V0).

They are **candidate calibration stimuli, not calibration instruments. None is usable as-is.** The
expected readings are Molly Bang's assertions and must be independently validated against human
response data before any evaluator's answer can be scored right or wrong against them. Any use must
carry `expected reading: source-asserted by Molly Bang; NOT validated human ground truth`. The two
recorded isolation confounds travel with the pairs and are a separate defect from the validation gap.

**NEXT APPROVED TASK:** None. CANON-001 is approved and closed. Do not start CANON-002, do not touch
a second source, and do not run or extend an experiment without a new Controller-issued task file.
