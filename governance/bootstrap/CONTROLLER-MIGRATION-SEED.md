> # HISTORICAL / SUPERSEDED FOR BOOTSTRAP
>
> **Do not bootstrap a session from this file.** Reconciled and superseded by GOV-001 on
> 25 Aug 2026 against `main` at `00ea9b067229cd992b77b7d6e0958df35178b01b`.
>
> **Current project memory is `PROJECT-MEMORY.md`.** This file is retained unedited below as
> forensic evidence of the migration boundary — the point at which the project stopped depending on
> chat context. **It was never authoritative and is not authoritative now.**
>
> Claim-by-claim reconciliation is in
> `governance/audits/2026-08-25-initial-repository-hygiene-audit.md` §6. Summary: every material
> Canon, Eval, Resources and freeze claim in this seed was **confirmed** against committed evidence,
> several with mechanical verification. Nothing material was contradicted by the repository.
>
> **One unresolved migration dependency remains.** Of the four external research artifacts named in
> §6, two — `creative_production_canon_expansion_report (1).docx` and
> `creative_production_canon_candidate_universe (1).xlsx` — were located and inspected, and are
> recorded as an external research snapshot whose central arithmetic is now **stale** (they state
> live Canon 16; it is 19). The other two — `WAVE-1-ACQUISITION-REPORT.md` and
> `ACQUISITION-MANIFEST.xlsx` — **were not found and were not inspected**. Any acquisition claim
> resting on them is **unverified**, and the §6 Wave-1 status leads should be treated as unresolved
> until the Controller either supplies those artifacts or accepts their content into GitHub.

---

# Controller Migration Seed

**Date:** 2026-08-25
**Status:** ONE-TIME MIGRATION INPUT — NOT FINAL AUTHORITY
**Purpose:** Preserve important pre-Governor project context that may exist across prior Controller sessions and external research artifacts so GOV-001 can reconcile it into GitHub-native project memory.

## How GOV-001 must use this file

This file is **not** a substitute for repository evidence and must not be copied wholesale into `PROJECT-MEMORY.md`.

Evidence order for GOV-001:

1. committed GitHub artifacts on the audited `main`;
2. committed decision/task/findings records and reproducible outputs;
3. this migration seed, only as a lead/context preservation layer;
4. external research artifacts explicitly named below;
5. no prior chat history.

For every material claim below, the Governor must either:

- confirm it against committed GitHub evidence;
- preserve it with an explicit weaker provenance label if it is accepted context but not independently provable from GitHub;
- mark it unresolved/contradicted/superseded;
- or omit it from canonical project memory if it has no durable support and no continuing project value.

Do not promote a Controller recollection or external research snapshot into hard project truth merely because it appears here.

---

## 1. Product thesis / architecture context to reconcile

The project is building an **API-native media production intelligence layer** between customer intent and image/video/audio generation tools. The long-term primary metric is **Cost per Accepted Outcome**, not cost per generation.

The architecture currently separates:

- **Canon** — durable creative/production knowledge;
- **Eval / Capability Lab** — empirical measurement of what current models/workflows can actually do;
- **Resources** — independent evaluation media/data;
- **Controller** — strategic/architectural authority;
- **Repository Governor** — newly approved fifth role for repository coherence and long-term project memory.

Important separations believed to remain frozen include Normalized Request vs Creative IR, Creative IR vs Production IR, Source Knowledge vs current operational bindings, Canon knowledge vs empirical capability, and public dataset labels vs project ground truth. Verify against `coordination/PROJECT-CONTRACT.md` and relevant specs.

Production IR and the Capability Registry are not believed to be implemented yet. Verify before preserving this as current state.

---

## 2. Current global operating state

At the time of this seed, the Controller intentionally placed **all new domain work on audit freeze** pending GOV-001.

Do not authorize or start:

- CANON-009 or other Canon expansion;
- EVAL-006 or checker/model/API execution beyond already-completed EVAL-005 work;
- new Resources expansion;
- new acquisition work;
- Capability Registry work;
- Production IR work;
- other newer architecture/product work.

This freeze was chosen so the project can establish a clean GitHub-native source of truth before continuing.

---

## 3. Canon state/history leads

These are migration leads and must be checked against `canon/**`, task records, audit records, PR history, validators, and handoffs.

### Historical CANON-003 baseline

The Controller believes CANON-003 established a frozen historical baseline of **16 accepted sources**. Later live-Canon growth must not rewrite that historical measurement.

Historical accepted set believed to be:

1. Grammar of the Shot
2. Ogilvy on Advertising
3. Light: Science & Magic
4. Interaction of Color
5. The Vignelli Canon
6. Making and Breaking the Grid
7. The Photographer’s Eye: A Graphic Guide
8. Painting With Light
9. Grammar of the Edit
10. In the Blink of an Eye
11. Scientific Advertising
12. Made to Stick
13. Alchemy
14. Creativity, Inc.
15. Art & Fear
16. Building a StoryBrand

`Thinking with Type` was historically blocked in CANON-003 because of representation/column-interleaving issues and was not counted in that baseline.

### Audit Gate

The Controller believes Audit Gate v0.2 became the authoritative Canon admission method in CANON-005, including representation integrity, evidence origin, application fit, pairwise source lineage, technology contingency, and the legitimate completed outcome `evidence_insufficient`.

### CANON-006

The Controller believes two reserve sources were later admitted:

- *Master Shots*, chapter 8, Christopher Kenworthy;
- *The Conversations*, chapter 3, Michael Ondaatje / substantial Walter Murch speaking voice.

For this pair, `shared_primary_informant` was approved as a pairwise symmetric lineage dependency because the same practitioner's own claims materially inform both works. Incidental quotation alone was explicitly not enough.

If supported, this moved live Canon from 16 to 18 while leaving the CANON-003 baseline at 16.

### CANON-007

The Controller believes *Effectiveness in Context* was admitted as one bounded source, taking live Canon from 18 to 19. A new representation-loss category `figure_semantic_binding_lost` was approved for cases where textual/numeric elements survive but spatial/structural mapping to categories/series/panels/labels is lost.

### CANON-008

The Controller believes CANON-008 attempted to replace an earlier bad Wave-1 Devanagari source identity with Girish Dalvi's 2010 IIT Bombay thesis *Conceptual Model for Devanagari Typefaces*.

The task **stopped at the acquisition gate** because the official Dsource/IDC route exposed only an abstract/3-page artifact and the full thesis required IIT Bombay authentication. No ingestion should have occurred and live Canon should therefore remain **19**, not 20.

Verify all of the above from current `main` and PR/task history.

---

## 4. Eval state/history leads

These must be checked against `eval/**`, task records, battery materialization, human-validation records, PR history, and tests.

### Earlier work

The Controller believes EVAL-003 produced a 54-item Hindi-primary Devanagari crop pack. EVAL-004 was exploratory reader work and was stopped rather than treated as a benchmark result.

### EVAL-005 design

The Controller believes EVAL-005 established a qualification battery for exact Devanagari rendering/checking with these important design constraints:

- image-only transcription target hidden from checker;
- verdict uses image + target;
- pinned Kohinoor rendering path with no silent fallback;
- malformed/dotted-circle items excluded from hard stratum;
- one mismatch per distinct base word;
- multiple failure classes/groups;
- decoded-pixel visibility screening;
- fail-closed narrow PNG handling;
- encoded SHA artifact identity;
- qualification gate of zero false passes, with additional false-fail/refusal/repeat-consistency thresholds;
- probabilistic/iid calculations used only as reference/planning, not as truth of deterministic item construction.

Original battery believed to have been **106 items = 53 match + 53 mismatch**.

### Human validation and prune decision

A human review packet was completed **98/98** by one reviewer. Controller accepted five rejected base-word items and two broken sanity renders.

Controller decision was explicitly:

**PRUNE, DO NOT REBUILD.**

The intent was to preserve already-reviewed item identities and avoid introducing a new human-validation surface.

The exact excluded item IDs believed to be:

Mismatch:
- `dx-0000`
- `dx-0003`
- `dx-0005`
- `dx-0020`
- `dx-0039`

Match:
- `dx-0053`
- `dx-0056`
- `dx-0058`
- `dx-0073`
- `dx-0092`

Resulting validated view believed to be:

- 96 total items;
- 48 match / 48 mismatch;
- 48 human-accepted base words;
- 33 hard distinct-base mismatch opportunities;
- 20 failure classes / 5 groups.

The original 106-item battery should remain preserved/reproducible rather than mutated into the 96-item view.

### Eval PR #12

The Controller believes the final EVAL-005 human-validation freeze PR corrected two important integrity issues before merge:

1. derived validated checker payload paths were rebased to `../images/...` while validated `items.jsonl` remained byte-identical to the intended derived view;
2. stale live Eval documentation was updated from pre-human-validation state to the post-validation 96-item/48-word state.

The Controller could inspect the committed implementation but could not independently rerun the full test suite because of environment/network limitations. Any quoted full test counts from the worker should therefore remain labelled **agent-reported verification** unless GOV-001 can rerun them.

Verify current committed state rather than trusting these numbers.

---

## 5. Resources state/history leads

The Controller believes current Resources work established that IndicSTR12 and IIIT-ILST are heavily overlapping/derived and should be treated as one lineage rather than independent evidence.

Migration leads to verify:

- IndicSTR12: 375 scene images + 2,711 crops = 3,086 media;
- IIIT-ILST: 176 scene images + 1,214 crops = 1,390 media;
- 3,924 resolvable crop labels total;
- 173/176 IIIT scenes shared with IndicSTR12;
- 1,205/1,214 IIIT crops derive from shared parents;
- crops may be scoreable but independence is broken;
- BSTD was identified as a genuine cross-lineage reserve.

Public labels are not automatically validated Hindi-word ground truth.

Resources should remain idle during the GOV-001 freeze unless the audit finds a concrete integrity issue to route.

---

## 6. External source-discovery / acquisition context

This work was performed outside GitHub in ChatGPT Work and should be treated as **external research snapshot**, not competing repository authority.

Known external artifacts in the user's file/library environment were believed to include:

- `creative_production_canon_expansion_report (1).docx`
- `creative_production_canon_candidate_universe (1).xlsx`
- `WAVE-1-ACQUISITION-REPORT.md`
- `ACQUISITION-MANIFEST.xlsx`

The source-discovery portfolio proposed approximately 22 additions to the historical 16-source Canon, but some workbook counts are known to have become stale as live Canon later moved beyond 16.

Wave-1 research leads included:

- Product Photography Courses / Visual Education;
- Animation Bootcamp;
- Thinking with Type, 3e;
- Brand New reviewed identity critiques;
- Effectiveness in Context;
- The Advertising Concept Book;
- a Devanagari source slot later redirected to Dalvi's IIT Bombay thesis.

Known status leads to reconcile only if durable evidence is available:

- *Effectiveness in Context* was later ingested via Canon and is no longer merely an acquisition candidate;
- Visual Education/Product Photography appeared to be streaming-access only, requiring a legal/operational capability check before purchase/use;
- Animation Bootcamp terms reportedly included a restriction affecting AI-model enhancement/use, so no purchase was authorized;
- *Thinking with Type* 3e was reportedly available through VitalSource/DRM and required operational-access assessment before purchase;
- Brand New reviewed critiques appeared accessible as authenticated web content, but corpus-freeze mechanics were unresolved;
- *The Advertising Concept Book* physical/library/fixed-layout access was still being investigated;
- the earlier “Fiona Ross / Devanagari Type Design” candidate identity was considered wrong for the intended slot and was superseded by the Dalvi attempt.

If the Governor cannot access the external artifacts, it should record only that external research exists and route the unresolved migration dependency rather than inventing detail.

---

## 7. Qualitative experiment lead

A small qualitative comparison was run outside the formal Eval system using Aight advertising concepts: one arm used Canon-derived creative principles and another was more vanilla. The Controller/user judged the Canon arm materially better in cleanliness, premium feel, alignment, control, and trustworthiness.

This is **qualitative anecdotal evidence only**, not a benchmark result and not a Capability Registry entry. Preserve it only if useful as a historical experiment note and label it accordingly.

---

## 8. Known coordination/control-plane drift leads

Controller's pre-Governor read-only audit found material staleness in operational documents. GOV-001 must independently verify and broaden this list.

Known leads include:

- `coordination/CONTROL-STATE.md` appearing to describe much older Canon/Eval states;
- `coordination/WORKSTREAM-STATUS.md` appearing stale relative to CANON-006/007/008 and EVAL-005;
- `coordination/DECISION-LOG.md` potentially ending before several later Controller decisions;
- `coordination/RUNBOOK.md` potentially containing obsolete startup/branch conventions;
- `coordination/AUTOMATION-ROADMAP.md` appearing historical rather than current;
- stream handoffs mixing useful present state with accumulated historical narrative;
- some Eval operational docs having previously contradicted completed human validation;
- external acquisition work lacking a clear durable authority boundary in GitHub.

These are leads, not findings. GOV-001 must classify every operational/state document independently.

---

## 9. Important Controller decisions/context believed not to be safely recoverable from one current status file

Reconcile and persist only if supported or still strategically material:

- historical CANON-003 count remains frozen even as live Canon grows;
- Audit Gate v0.2 is the current Canon admission method;
- CANON-006 `shared_primary_informant` relationship applies pairwise/symmetrically to the identified reserve pair, not as a generic excuse for dependence;
- CANON-008 is a legitimate STOP, not a failed ingestion to work around with unauthorized access;
- EVAL-005 human adjudication chose **PRUNE, DO NOT REBUILD**;
- one-reader human validation is not independent-reader ground truth and should be represented honestly;
- worker-reported test counts remain agent-reported unless independently rerun;
- current project work is frozen until the governance reset is complete;
- source discovery/acquisition work can inform decisions but is external research until accepted into GitHub;
- future sessions should bootstrap from GitHub rather than pasted chat summaries.

---

## 10. Migration success condition

GOV-001 should make this file unnecessary for normal future operation.

After the first canonical `PROJECT-MEMORY.md` and Governor audit are accepted, this seed should be marked **HISTORICAL / SUPERSEDED FOR BOOTSTRAP** and retained only as forensic evidence of the migration boundary.

The target post-reset invariant is:

> A fresh competent agent with zero prior chat history can reconstruct the project's authoritative current state, important decisions, provenance/verification limitations, and next gates from GitHub alone.
