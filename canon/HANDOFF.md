# Canon — Handoff

**PURPOSE:** Build and test durable creative/media expertise consumable by a reasoning model.

**CURRENT STATE:** SPEC-01 (Creative IR) through SPEC-05 (Ontology) exist and are locked/frozen.
CANON-003 closed at **16 Controller-accepted books** and was merged to `main` via PR #4 — 505
SourceKnowledge objects, 54 SourceConceptSystems, 417 ontology terms, 53 concepts, 111 operational
bindings, under `knowledge/current/`. Its conclusion was that the three-layer architecture
(SourceKnowledge → source systems/ontology → OperationalBindings) should be **retained**, and that the
next revision should be one consolidated post-extraction Audit Gate.

CANON-004 designed and tested that gate against the 16-book corpus. **The Controller ADOPTED it on
25 Aug 2026** (`decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`, PR #6), and **CANON-005 has made
it authoritative**. Canon-consumption / RAG experiments remain paused until the Controller reopens
them.

**Audit Gate v0.2 — the active method and its paths:**

| What | Where |
|---|---|
| Normative procedure and schema | `canon/audit/AUDIT-GATE-v0.2.md` |
| Active records — exactly one per source directory | `canon/audit/records/*.audit.yaml` (19), all `audit_record_version: v0.2` |
| Validator | `canon/validation/validate_audit_gate_v02.py` |
| Tests | `tests/test_validate_audit_gate_v02.py` |
| Experiment history — pointer only, nothing active | `canon/experiments/audit-gate-v0.2/README.md` |

**The gate blocks downstream consumption, not storage.** A source becomes accepted downstream
knowledge only after its extraction, systems/ontology and bindings are stable, its fresh checkpoint
is committed, its Audit Gate record is written against those exact bytes, and the Audit Gate
validator passes. **Until then — and again if its audit goes stale — it may not be used for
cross-source promotion, downstream product/application use, or Canon-consumption/retrieval.** It
remains in the repository as source evidence throughout; the gate governs use, not worth.

**Live corpus after CANON-007: 19 source directories, all 19 accepted, 19 active audit records.**

Two numbers that used to coincide are now distinct and must not be confused:

| Number | Value |
|---|---|
| CANON-003 accepted books / CANON-004 method-test corpus | **16 — fixed forever** |
| Live accepted Canon | **19** |

`canon/validation/validate_canon003_integrated.py` remains a **historical** instrument for the frozen
16 and its meaning must never change. The live invariant is simple and needs no registry: **every
source directory holds exactly one active Audit Gate record.** A source whose audit cannot be
completed says so in the record itself, via `audit_status: evidence_insufficient`.

**CANON-006's durable finding: different bibliographic authorship does not prove independent
intellectual origin.** *The Conversations* is Michael Ondaatje's book substantially recording Walter
Murch, and the corpus already held Murch's own *In the Blink of an Eye*. Different author, publisher
and year, and the same load-bearing claims in both — the Egyptian-painting argument and `planarity`.
That pair would pass any check built on bibliographic metadata. The Controller therefore approved a
new dependence relation, `shared_primary_informant`, now applied. Both sources are accepted, and the
pair is blocked from counting as independent convergence with each other only.

**One adopted record version: `v0.2`.** The validator fails closed on anything else, including the
pre-adoption `v0.2-experimental`. There is no migration or version-negotiation machinery, and adding
a second version is a Controller decision, not something to build in advance.

**CURRENT APPROVED DECISIONS:** Audit Gate v0.2 adopted 25 Aug 2026 and authoritative; the only
authoritative spec it changed is SPEC-05 Governance rule 5. `deterministic_composition` and
`human_workflow` remain **audit application-fit vocabulary only** — neither is a SPEC-04 target type
or executor unless a later task separately establishes one. SPEC-01 v0.1 locked. SPEC-03/04/05 supersede SPEC-02 conceptually
(SPEC-02 retained as evidence). Direction reset restoring the Canon / Capability-Lab / Production
boundary accepted. CANON-003 stopped at 16 books by Controller decision
(`decisions/CANON-003-STOP-AT-16-2026-08-24.md`); Books 11 (*Master Shots*) and 12 (*The
Conversations*) are deferred reserves, not failures. *Thinking with Type* remains blocked on
structural column interleaving.

**LAST COMPLETED TASK:** `tasks/CANON-007.md` — Wave 1 pilot, one source. Ingested Binet & Field,
*Effectiveness in Context* (Chapter 1.0 plus Introduction and the methodology Appendix) from the
official Thinkbox route; both the file size and SHA-256 matched the Work acquisition fingerprint
exactly. Accepted through the full sequence with no stop condition. Live Canon 18 → 19.
No SPEC changed; one minimal Controller-approved Audit Gate v0.2 vocabulary addition was made,
`figure_semantic_binding_lost`, with no new Audit Gate version and no migration machinery.

Preceding: `tasks/CANON-006.md` — adjudicated the two deferred reserves under the
authoritative gate. *Master Shots* recovered from `work/canon-003-rebalance-d` and *The
Conversations* from `work/canon-003-b`; both **accepted**. The Controller approved and this task
applied one new lineage dependence relation, `shared_primary_informant`, amending SPEC-05 Governance
rule 5's dependence list from four relations to five. No legacy branch merged, no source re-opened,
no new source ingested, and the historical 16-source validator left byte-identical.

Preceding: `tasks/CANON-005.md` — applied the adopted Audit Gate. Amended SPEC-05
Governance rule 5 so independence for a `cross_source_concept` comes from the Audit Gate lineage
records rather than a count of distinct source ids; promoted the schema and the 16 records out of
`experiments/` into `canon/audit/`; documented the gate order authoritatively; repointed the
validator and tests. SPEC-01, SPEC-03 and SPEC-04 unchanged.

Preceding: `tasks/CANON-004.md` — designed and tested the gate, plus a Controller correction pass on
25 Aug (retain `deterministic_composition`; close the stale-audit hole with an enforced
`source_snapshot` content fingerprint; correct the independence test fixtures).

**CANON-008 STOPPED AT ITS ACQUISITION GATE, 25 Aug 2026.** The official D'source/IDC record for
Girish Dalvi's *Conceptual Model for Devanagari Typefaces* (id=1275) exposes only a **3-page
abstract** — `idc-girish-pdh-abstract.pdf`, 50,197 bytes, SHA-256 `e9baa76c…d92d2cf7`, PDF title
metadata `Abstract.xps`. The full thesis sits behind IITB SSO, which was not attempted. Neighbouring
IDC records publish full theses under `-thesis` / `-report` names, so the archive distinguishes the
two and holds only the abstract for this one. No extraction was performed and no source directory
was created; live Canon stays at 19. Details and four Controller options in
`findings/CANON-008-CONTROLLER-BRIEF.md`. **The Canon still has no accepted Devanagari-structure
source.**

**CURRENT TASK / QUEUE:** none. CANON-008 is `needs_controller_review`, stopped at its acquisition
gate. The rest of the Wave 1 portfolio is **not** started and must not be self-assigned. **Next work is
Controller-assigned only** — do not self-assign reserve-book integration, Canon expansion,
cross-source promotion, RAG/retrieval or Production IR.

**IMPORTANT OBSERVATIONS:**
- The old admission rule ("no IR consumer → discard") caused exclusion and distortion. Do not
  reintroduce that coupling. 44 objects across *Creativity, Inc.* and *Art & Fear* have zero Creative
  IR bindings and that is correct.
- Current source knowledge must stay source-faithful; product bindings are separate and optional.
- **Bindability is not evidence quality.** The corpus's best-binding source (*Building a StoryBrand*,
  4 Creative IR bindings from 18 objects) has its weakest support. Never rank by binding count.
- **Chart text can survive extraction while its meaning does not.** *Effectiveness in Context*
  extracts every axis label, series name and printed value cleanly, and loses which number belongs
  to which category. A text-only pass would bind them by guess with nothing signalling doubt. Every
  numeric value from that source was read from a page render.
- **A text layer can contain text the page does not show.** That report's three foreword pages carry
  sentences printed nowhere on them. The loss-pattern vocabulary has no value for *added* text, only
  for lost text; the mismatch is recorded rather than papered over, and becomes live if those pages
  are ever processed.
- **Do not treat an authored empirical report as its own measurement.** Its percentages are
  proportions of case-author self-gradings from a declaredly biased sample, with activation spend
  self-declared as under-reported in the direction that flatters its headline conclusion. Recorded
  as `mixed_own_and_third_party`.
- **A different author field is not independence either.** *The Conversations* and *In the Blink of
  an Eye* have different authors, publishers and years, and are the same practitioner speaking. No
  metadata field records that. Now expressed by `shared_primary_informant`; incidental quotation of
  the same person does not qualify. This is the sharper sibling of the finding below.
- **A source id is not an independent origin.** *Grammar of the Shot* and *Grammar of the Edit* are
  companion volumes by the same authors and must not count as convergence. This is now enforced by
  SPEC-05 Governance rule 5 and by `independent_origins_ok()`, which fails closed. Independence is
  **pairwise** — a source blocked against its companion is still a good origin against everything
  else.
- **Validate with a committed instrument, not a session script.** The integration validator returns
  early on a YAML parse failure, which under-reported one book's term checks; that gap surfaced as 10
  real errors on `main` and was repaired in CANON-004.
- **An audit record is only valid for the exact bytes it audited.** If any of a book's five
  machine-consumed artifacts changes, that book's Audit Gate record fails as stale and must be
  re-run. There is deliberately no snapshot-refresh shortcut.
- **PyYAML is not installed system-wide on this machine.** Create a local `.venv` (self-ignoring) with
  `pyyaml` and `pytest` before running either validator.

**SERIES DEPENDENCY TO DECLARE LATER.** *Effectiveness in Context* is Part 2 of a series and builds
on the authors' own *The Long and the Short of It* and *Media in Focus*. If either is ever ingested,
that pair is `shared_author` and `same_series` and must be declared at ingestion rather than
discovered afterwards.

**DEFERRED RESERVE SOURCES — resolved by CANON-006.** Both remain **outside** the frozen 16-book
CANON-003/004 method-test set, which is a historical fact and does not change. Both now hold active
audit records and are live accepted knowledge, taking the live Canon to 18.

**OPEN QUESTIONS:** Ontology naming convention. Runtime Canon consumption shape. Whether evidence
lineage and source lineage need joining (one source is not enough to say). Whether a different worker
writing an audit record produces the same record.

**DEPENDENCIES:** None. Routing work remains downstream of Eval's future Capability Registry.

**PROPOSED CROSS-STREAM CHANGES:** none filed. One observation the Controller may wish to forward to
Eval: a validator that aborts a unit on a parse error under-reports, and the shortfall is invisible in
its own output.

**NEXT APPROVED TASK:** none. Do not self-assign a source, an experiment or a spec edit. Wait for the
Controller's CANON-004 decision.
