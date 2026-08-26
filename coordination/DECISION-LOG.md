# Decision Log

**Updated:** 26 Aug 2026 — current Controller decision index.

> **Scope notice.** The two narrative entries below are the project's **23 Aug 2026 architectural
> decisions** and remain accurate as history. They are **not** a complete decision register: from
> 24 Aug 2026 onward, Controller decisions were recorded inside the owning stream's folder or in
> dedicated Controller records.
>
> The index below links those committed decisions. It records only decisions with committed evidence;
> it creates none.

## Decision index — 24 Aug 2026 onward

| Date | Decision | Where the record lives | Record type |
|---|---|---|---|
| 24 Aug 2026 | Resources may treat **transient acquisition** as the default for large, reliably re-acquirable public archives; licence silence is not a block for public, ungated, internal-only material, but access gates and explicit terms still are | `resources/CHARTER.md`, `resources/tasks/RES-002-CONTROLLER-BRIEF.md` | charter + brief |
| 24 Aug 2026 | **EVAL-003 pack is Hindi-primary**, and shared photographs are admitted **once** | `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md` | Controller brief |
| 24 Aug 2026 | **CANON-003 extraction stops at 16** accepted usable books — above the minimum of 15, below the 18 target | `canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md` | **decision record** |
| 24 Aug 2026 | **EVAL-004 stopped** before its second reader; Reader A is exploratory evidence only and may not qualify any checker | `eval/decisions/EVAL-004-STOP-2026-08-24.md` | **decision record** |
| 24 Aug 2026 | Identity rubric V0 **frozen** for later calibration; frozen does not mean validated | `eval/tasks/EVAL-002-CONTROLLER-BRIEF.md` | Controller brief |
| 25 Aug 2026 | **Adopt Post-Extraction Audit Gate v0.2** as the Canon admission method | `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md` | **decision record** |
| 25 Aug 2026 | Audit Gate made **authoritative**; SPEC-05 Governance rule 5 amended so independence comes from lineage records, not a count of distinct source ids | `canon/tasks/CANON-005.md`, `canon/findings/CANON-005-CONTROLLER-BRIEF.md` | task + brief |
| 25 Aug 2026 | Approve the lineage relation **`shared_primary_informant`**, applied pairwise and symmetrically; incidental quotation does not qualify. Both reserve sources admitted — live Canon 16 → 18 | `canon/PROPOSED-METHOD-CHANGE-CANON-006-LINEAGE.md`, `canon/findings/CANON-006-CONTROLLER-BRIEF.md` | approved proposal + brief |
| 25 Aug 2026 | Approve the representation-loss category **`figure_semantic_binding_lost`**; *Effectiveness in Context* admitted — live Canon 18 → 19 | `canon/findings/CANON-007-CONTROLLER-BRIEF.md` | Controller brief |
| 25 Aug 2026 | **EVAL-005 human validation: PRUNE, DO NOT REBUILD.** 5 base words rejected, 10 items excluded and not replaced; authoritative battery is the 96-item validated view | `eval/battery/devanagari-exactness/human-validation/human-validation-v1.json` (status `FROZEN`), `.../HUMAN-VALIDATION-RECORD.md` | **machine-readable frozen record** |
| 25 Aug 2026 | **CANON-008 stops at its acquisition gate**; no source ingested, live Canon stays 19 | `canon/findings/CANON-008-CONTROLLER-BRIEF.md` | Controller brief |
| 25 Aug 2026 | **Approve the Repository Governor design** and fifth-agent role | `docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md` | approved spec |
| 25 Aug 2026 | **Audit freeze** on new domain work pending governance reset | `governance/bootstrap/CONTROLLER-MIGRATION-SEED.md`, `governance/README.md` | historical bootstrap decision |
| 25 Aug 2026 | **Post-audit unblock:** close CANON-008 as legitimate blocked-source adjudication; accept Resources correction; provisionally approve EVAL-005 checker gates/Registry schema; open EVAL-006 | `coordination/decisions/CONTROLLER-POST-AUDIT-UNBLOCK-2026-08-25.md` | **decision record** |
| 25 Aug 2026 | **Authorize EVAL-006** under a ₹16,000 cap | `eval/tasks/EVAL-006.md` | approved task, later paused |
| 26 Aug 2026 | **Three-stream overnight program** authorised to build V1 Canon/Eval/Resources architecture in parallel | `coordination/decisions/CONTROLLER-THREE-STREAM-OVERNIGHT-PROGRAM-2026-08-26.md` | **decision record** |
| 26 Aug 2026 | **V1 overnight integration accepted:** Creative IR/30-bank, 36-capability/100-item Eval baseline and Resources V2.1 architecture accepted; paid model evidence still absent | `coordination/decisions/CONTROLLER-V1-OVERNIGHT-INTEGRATION-2026-08-26.md` | **decision record** |
| 26 Aug 2026 | **EVAL-006 paused and spend authority withdrawn** pending master-plan re-scope | `coordination/decisions/CONTROLLER-PAUSE-EVAL-006-PENDING-MASTER-PLAN-2026-08-26.md`, `eval/tasks/EVAL-006.md` | **decision record + paused task** |
| 26 Aug 2026 | **Pre-E7 scope rebase:** native model duration is a production constraint rather than a product limit; explicit conditions/outcome topology required; historical E7/E8 counts no longer authorised | `coordination/decisions/CONTROLLER-PRE-E7-SCOPE-REBASE-2026-08-26.md` | **decision record** |
| 26 Aug 2026 | **Cloud macro recalibration:** replace synthetic-brief-first discovery with independent request-space, capability/workflow and evidence/topology research; E7 remains blocked | `coordination/decisions/CONTROLLER-CLOUD-MACRO-RECALIBRATION-2026-08-26.md` | **decision record** |
| 26 Aug 2026 | **Macro research integration accepted with corrections:** explicit requested operation, Capability-v2 direction, dependency-aware scoring, topology-v3 direction, whole-outcome CpAO and request-lineage rules adopted for specification work | `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md` | **decision record** |
| 26 Aug 2026 | **Final pre-execution freeze tranche authorised:** CANON-010, EVAL-009, RES-004 and EVAL-010 run in parallel; EVAL-008 is candidate-universe research, not a paid roster; scientific model selection remains independent of sourcing | `coordination/decisions/CONTROLLER-FINAL-PRE-EXECUTION-FREEZE-2026-08-26.md` | **decision record** |
| 26 Aug 2026 | **Pre-execution freeze integration accepted with one bounded Eval correction:** seven-value requested-operation vocabulary, Capability Contract v2 at 44 (43 active + 1 dormant), dependency-aware scoring, 13 condition families, 12 core + 2 reserve scientific slots, outcome topology v3 and CpAO v3, four controlled packs. 494 generations / 5,515 evaluator calls / 188 human review units and 173 pack-acquisition hours are **explicitly not authorised** as a paid tranche | `coordination/decisions/CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md` | **decision record** |

## What counts as a durable Controller decision

**This repository has never used dedicated decision files exclusively, and this index does not
pretend otherwise.** A durable Controller decision may currently be recorded in any of:

- a **dedicated decision record** (`canon/decisions/`, `eval/decisions/`, or Controller-owned decision records);
- an **approved task file or spec**;
- a **Controller Brief carrying an explicit Controller disposition**;
- an **approved proposal**;
- a **frozen machine-readable decision artifact** (e.g. `human-validation-v1.json`, status `FROZEN`).

**This log is the index for discovering them**, and the "Record type" column above says which form
each decision takes so its provenance is visible rather than assumed.

**What does not change.** A worker's recommendation, an inference, or a proposal with no Controller
disposition **is not a decision**, whichever file it sits in. The form of the record varies; the
requirement that a Controller disposition exists does not.

**Known variation in provenance strength.** Some decisions have dedicated records; others are
carried by a brief, task file, approved proposal or frozen artifact. A brief mixes decision with
worker narrative, which is weaker provenance than a dedicated record even when the disposition is
explicit. Normalising these into dedicated decision records is a routed improvement, not a current
requirement. It must not be done retroactively in a way that rewrites what was actually decided at
the time.

---

## 2026-08-23 · SPEC-02 superseded conceptually by SPEC-03/04/05

**Decision:** Split the single Canon Atom into three layers — durable source knowledge, replaceable
product bindings, and a terminology ontology. Retain SPEC-02 and all six probe outputs unchanged as
experimental evidence.

**The assumption that failed:**

> Current product consumption is not a valid admission criterion for durable source knowledge.

SPEC-02 rule 1 read *"No consumer, no atom."* Every piece of book knowledge had to name a Creative
IR path or be demoted to human notes.

**Why it failed — evidence from the six-source probe:**

1. **It excluded durable knowledge.** *Light: Science & Magic*'s family of angles, the organising
   concept of the book, was filed as a note because it describes where to place a physical light
   and Production IR does not exist. Nineteen items were discarded this way.

2. **It admitted distortion.** An extractor required to find a binding finds one. Molly Bang's
   "larger reads as stronger" was recorded as informing `entities.role`; her colour-grouping
   principle as informing `relationships`, which in SPEC-01 means entity-to-entity relations.
   Neither is her claim. Product vocabulary also leaked into source fields — `mb_002`'s diagnostic
   read *"Is the rank-1 element at or near centre."*

3. **The rule contradicted itself.** SPEC-02's own counter-example,
   `pointed_shapes_read_as_threatening`, was presented as unbindable. The extraction produced
   `mb_011`, bound to `creative.visual_language`. Same rule, opposite verdicts, three days apart.

**Two further assumptions failed alongside it:**

- *A single shared string vocabulary can be seeded from early sources.* Six sources produced 42
  failure terms and 47 repair terms with **zero exact reuse**. Seeding from book one would have
  forced five later sources to distort or fail. Replaced by SPEC-05's mapping layer.
- *Atoms alone are sufficient.* Three systems carry claims no member states; `mb_008` contains a
  cross-principle relationship inside its own principle text because there was nowhere else for it
  to go. SPEC-03 adds SourceConceptSystem.

**What changes**

- Source knowledge is durable and has no admission test. Zero bindings is a normal state.
- Bindings are ours, versioned against SPEC-01, and cheap to discard.
- Terminology is mapped, never merged. Canonical concepts are optional and their children stay
  authoritative for repair selection.
- Evidence is recorded as factual characteristics. Uncalibrated decimal confidence is removed.
- Physical-production repairs are preserved untranslated. Translation is Pass 2.

**What is explicitly unchanged**

SPEC-01 Creative IR v0.1. SPEC-02 and all six probe atom files. The two-pass extraction discipline,
page-and-figure provenance, and the observation-not-instrument rule for diagnostics all carry
forward.

**Cost of being wrong:** one extra layer and an indirection. Recorded as assumption 1 in
[ASSUMPTIONS.md](ASSUMPTIONS.md), with a falsifier: if after
fifty bindings none is ever revised while its source knowledge holds constant, the separation is
paying for nothing.

**Next review trigger:** first SPEC-01 revision after bindings exist.

---

## 2026-08-23 · Direction reset — Canon scope restored

**Decision:** Restore the original separation of responsibilities between the Creative Canon, the
Capability Lab, the Production Planner, Empirical Memory and Evaluation. No architecture is
reopened; no prior work is deleted.

**What went wrong.** Recent work began judging the Canon against responsibilities it never had.
FINDINGS-11 reported that 35% of a twenty-failure sample had "no useful Canon relationship" and
that routing showed "no evidence." Both were true of what was measured, and both were measured
against the wrong subsystem — seven of the twenty failures were server restarts, storage paths,
provider API drift and a platform message limit, and several more were diffusion artefacts. A
category error was published as a finding.

**The restored boundary:**

- **Canon** — durable creative and media expertise. What a good outcome must accomplish, what
  techniques and trade-offs exist, how to turn an incomplete instruction into a plan without
  overriding intent, what to inspect to judge fitness for objective, what is wrong at craft level.
  Cookbook, culinary school, tasting expertise. It does not know which oven works today.
- **Capability Lab** — what current models actually do, measured. Produces the Registry.
- **Production Planner** — chooses today's execution path from IR requirements plus Registry.
- **Empirical Memory** — what happened on real runs, in the observer's words.
- **Evaluation** — two instruments: technical hard-fidelity, and creative fitness. Canon serves
  the second and is largely irrelevant to the first.

**Routing, stated correctly:** the Canon helps define **which capabilities a job requires**. It
must never claim to know **which current model has them**.

**Conclusions corrected** (originals retained on disk): FINDINGS-11's results table and routing
verdict; FINDINGS-09/10's "fields never covered"; FINDINGS-08's "lowest yield" framing; assumption
14's "weakened" verdict.

**Standing rule adopted:** a missing relationship in processed material means *"not found in the
currently processed material."* It never means *"the Canon cannot know this."* Any future finding
reporting a Canon limitation must first state which subsystem owns the failure.

**Register changes:** entry 4 restated with three connection channels and a scope warning; entry 6
split into 6a planning and 6b evaluation; entry 14's weakening withdrawn as out of scope; entries
15 (routing via requirements plus Registry) and 16 (curriculum breadth) added. All remain
hypotheses.

**Work commissioned:** Coverage Map (52 domains), Canon V0 curriculum (11 sources with a
dimensional stopping criterion), Experiment A and B designs, Capability Lab V0 plan and Registry
schema, evaluation corpus research.

**Not done, deliberately:** no book ingested, no vector database, no fine-tuning, no full
Production IR, no schema expansion, no A/B/C run.

**Next review trigger:** approval of the Coverage Map and Curriculum before any source ingestion.
