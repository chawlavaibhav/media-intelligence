# Initial Repository Hygiene and State-Reconstruction Audit

**Task:** GOV-001 · **Role:** Repository Governor (fifth, independent) · **Date:** 25 Aug 2026
**Audited baseline:** `main` at **`00ea9b067229cd992b77b7d6e0958df35178b01b`**
("Merge governance migration seed", 25 Aug 2026 21:35 +0530)
**Branch:** `work/gov-001-initial-repository-hygiene`
**Scope:** governance/control plane. Canon, Eval and Resources artifacts were **read-only evidence**.

**Governor verdict: PASS WITH NON-BLOCKING NOTES.**

The domain evidence layer is in good order and survived every mechanical check run against it. The
**control plane had drifted badly** — the two documents a fresh Controller session is told to read
first described a project state roughly five merged tasks out of date. That is corrected here.
Fourteen issues are routed to their owning streams; none blocks merge of this task.

---

## 1. Method

Audited from a fresh clone of `main`, with no reliance on chat history.

Evidence priority, as required by the task: committed domain artifacts first; committed
decision/task/findings records second; the one-time Controller migration seed only as a
reconciliation lead; external research artifacts only with explicit external provenance; chat never.

**Numbers were derived from underlying artifacts, not read from Markdown.** Where a document stated
a count, that count was recomputed from the manifest, the directory tree, or the validator that owns
it. Three headline figures — live Canon sources, the EVAL-005 validated battery, and the Resources
corpus — were each independently reconstructed before any prose was trusted.

Repository shape at the baseline: **429 tracked files**, 187 Markdown files totalling **32,478
lines**, 14 merged PRs, 23 remote branches, 0 open PRs.

---

## 2. Reconstructed current state

Established from committed evidence alone. Full narrative: `PROJECT-MEMORY.md`.

**The project** is an API-native media production intelligence layer that routes a customer's intent
across image/video/audio tools, optimising **Cost per Accepted Outcome**. Three evidence streams
(Canon, Eval, Resources), a human Controller, and now a Governor.

**Canon — 19 live accepted sources; historical CANON-003 baseline frozen at 16.** Both numbers are
real and must stay distinct. Admission runs through Audit Gate v0.2, authoritative since CANON-005.
CANON-006 took 16 → 18 by admitting the two former deferred reserves; CANON-007 took 18 → 19;
CANON-008 stopped at its acquisition gate and ingested nothing. **The Canon still has no accepted
Devanagari-structure source.**

**Eval — battery built and human-validated; no checker has ever been run.** The authoritative
artifact is the **96-item validated view** of the Devanagari exactness battery; the 106-item build is
historical source material. Human validation is complete (98/98, one reviewer) and the Controller
decided **PRUNE, DO NOT REBUILD**. No checker qualified, no model benchmarked, no Registry entry,
₹0 API and generation spend. EVAL-004 remains stopped with no Reader B.

**Resources — closed, 34,786 items / 5.70 GB across 8 sources, 4 blocked.** IndicSTR12 and IIIT-ILST
are one source lineage, not two independent sources; BSTD is the only genuine cross-lineage reserve
and is untouched.

**Not built:** Capability Registry, Production IR, Production Planner, routing, any
Canon-consumption/RAG experiment.

**Global posture:** audit freeze on all new domain work. No task open in any stream.

---

## 3. Mechanical verification of the three headline facts

These were the facts most likely to have drifted, so each was reconstructed from the artifact rather
than read from prose.

### 3.1 Live Canon = 19 — CONFIRMED

| Check | Result |
|---|---|
| Directories under `canon/knowledge/current/` | **19** |
| Records in `canon/audit/records/*.audit.yaml` | **19** |
| Set difference in either direction | **0** — perfect one-to-one match, no orphan record, no unaudited directory |
| `validate_audit_gate_v02.py` | `record_count: 19`, `error_count: 0`, exit 0 |

The 19 are exactly the historical 16, plus `kenworthy-master-shots-ch8` and
`ondaatje-conversations-ch3` (CANON-006), plus `binet-field-effectiveness-in-context-ch1`
(CANON-007). **The arithmetic 16 → 18 → 19 is fully accounted for.**

### 3.2 Historical CANON-003 baseline = 16 — CONFIRMED AND UNMUTATED

`validate_canon003_integrated.py` reports **16 books, 505 source-knowledge objects, 54 concept
systems, 417 ontology terms, 53 concepts, 111 operational bindings, 0 errors**, exit 0 — byte-for-byte
the figures `canon/HANDOFF.md` has always claimed. **The historical instrument was not mutated as
live Canon grew.** This is the single most important non-regression in the repository and it holds.

### 3.3 EVAL-005 validated battery = 96 items — CONFIRMED

`human-validation-v1.json` is the machine-readable authority. It carries `status: FROZEN —
Controller-accepted adjudication; PRUNE, DO NOT REBUILD`, and states 98/98 answered, 0 unanswered,
0 unsure, 5 rejected base words, 10 excluded item IDs, and an expected validated state of 96 items /
48 match / 48 mismatch / 33 hard opportunities / 48 base words / 20 classes / 5 groups.

**Both raw response artifacts were re-hashed and matched their recorded SHA-256 exactly**
(`word-validation-sheet.completed.csv` → `b3dcebb9…`, `eval-005-review-results.completed.json` →
`4f52f930…`). The provenance chain from reviewer answers to frozen decision is intact.

### 3.4 Resources corpus — CONFIRMED

Recomputed directly from `resources/manifests/corpus-pilot-v0.jsonl`:

| Claim | Recomputed | Match |
|---|---|---|
| 34,786 items | 34,786 records | ✔ |
| all decode-validated, 0 defects | all 34,786 `validation_status: ok` | ✔ |
| 34,586 distinct files | 34,586 distinct SHA-256 | ✔ |
| 200 duplicates — 27 within a source, 173 across two | 27 / 173 | ✔ |
| 5.70 GB | 5,702,337,356 bytes | ✔ |
| every per-source count in the handoff table | all 8 match exactly | ✔ |
| 173 files shared between the two CVIT releases | 173 hashes spanning >1 source | ✔ |

---

## 4. Findings

Severity is judged by **what a fresh zero-context session would wrongly believe**, not by untidiness.

### HIGH — corrected within the governance write boundary

**H1 · `coordination/CONTROL-STATE.md` described a project roughly five merged tasks in the past.**
It stated "Canon status — CANON-003 active", "Controller-accepted usable books: **13 / 18**", lane and
branch assignments for books 8–12, and "EVAL-004 and Registry work remain unopened". By the audited
baseline, CANON-003 had closed at 16 and been superseded by CANON-004 through CANON-008, and EVAL-004
had been opened, run and stopped. **This is the file the runbook told a fresh Controller to read
first.** A new session would have restarted finished work and would have believed live Canon was 13.
*Evidence:* the file versus `canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md`, the 19 audit
records, and `eval/decisions/EVAL-004-STOP-2026-08-24.md`.
**Resolution: corrected.** Rewritten as genuinely current, with a correction notice naming what it
used to say and where that history is preserved.

**H2 · `coordination/WORKSTREAM-STATUS.md` still described Books 11–12 as deferred reserves outside
the synthesis set.** CANON-006 admitted both. The file also stopped at the EVAL-004 stop and had no
knowledge of EVAL-005 or the 96-item validated battery. Its "Current Controller posture" section
would have actively misdirected a session.
**Resolution: corrected**, with the legitimately historical CANON-003 record retained intact and
labelled as history rather than deleted.

**H3 · A Canon-filed request to correct the control plane had gone unactioned.**
`canon/PROPOSED-INTEGRATION-CHANGE-CANON-005-COORDINATION.md` (25 Aug) listed the exact stale lines
in both coordination files, correctly declining to edit them because `coordination/` is not Canon's
to write. Nothing consumed it. **The routing mechanism worked; the receiving end had no owner.**
That gap is precisely what the Governor role now fills.
**Resolution: corrected** — its proposed replacement facts are applied where still true. Note that
the proposal is itself now partly superseded: it says the two reserves remain outside the live Canon,
which CANON-006 changed the same day.

**H4 · `coordination/DECISION-LOG.md` ended on 23 Aug and indexed none of the later decisions.**
Every Controller decision from 24–25 Aug lives in a stream folder (`canon/decisions/`,
`eval/decisions/`) or inside a Controller Brief. The runbook directs a fresh Controller to fall back
to this log to check history, and that fallback silently returned nothing for the entire operating
period of the project.
**Resolution: corrected** — a 13-row index of later decisions with their evidence paths and record
types was added. **No decision was invented; only decisions with committed evidence are indexed.**

### MEDIUM — corrected within the governance write boundary

**M1 · `coordination/AUTOMATION-ROADMAP.md` claimed one working script existed.** It stated
`eval/scripts/check-vlm.mjs` was "the one working script in the repo" and "everything else in
`*/scripts/` is empty", and pointed at `canon/scripts/`, **which does not exist**. The repository
actually holds two Canon validators with 65 tests plus 93 subtests, an Eval harness with a passing
self-test, a 43-test battery suite, and 14 Resources scripts.
**Resolution: corrected**, including the two genuine reproducibility limits recorded in F2 below.

**M2 · Three broken internal links in `coordination/`.** `DECISION-LOG.md` linked
`ASSUMPTIONS-AND-FALSIFICATION.md` (the file is `ASSUMPTIONS.md`); `ASSUMPTIONS.md` linked
`CANON-EXPERIMENT-V0.md` and `CAPABILITY-LAB-V0-PLAN.md` as if they were siblings when they live
under `canon/experiments/` and `eval/battery/`.
**Resolution: corrected** — all three repointed to the real paths.

**M3 · `coordination/RUNBOOK.md` documented an obsolete branching model.** It described three
long-lived per-stream worktrees as "the enforcement mechanism" behind stream ownership. Actual
practice moved to per-task branches from CANON-003 onward; the three original branches are stale.
The bootstrap order also predated `PROJECT-MEMORY.md` and contained no Governor step.
**Resolution: corrected**, including a branch-hygiene warning (see M5).

**M4 · The two CANON-003 Controller audits in `coordination/` read as live.** Both describe active
worker branches and books "subject to" a future integration requirement, in the present tense, with
no status header.
**Resolution: marked HISTORICAL.** Content untouched and explicitly affirmed as still evidentially
valid for CANON-003.

**M5 · Branch state is misleading and cannot be read mechanically.** 23 remote branches exist. 17
report as **unmerged** against `main` because their content arrived by squash merge, so
`git branch --merged` gives the wrong answer for almost every branch in the repository. A future
session cannot tell live work from finished work.
**Resolution: corrected in documentation** — the runbook now states the rule (treat a branch as live
only if an open PR or an assigned task file names it). **Deleting branches was deliberately not done:**
the task forbids large deletions for tidiness, and two branches hold genuinely unmerged evidence (R1,
R2 below).

**M6 · `coordination/PROJECT-CONTRACT.md` did not mention the Governor.** Its Authority section listed
only Controller and Workers, so a zero-context agent reading the contract would not learn that a
fifth role exists or what it may write.
**Resolution: corrected** — an additive Authority entry recording the already-approved role and its
write boundary. **No product, architecture or separation content was altered.**

### FINDINGS ABOUT THE REPOSITORY AS A WHOLE

**F1 · `resources/scripts/build_reports.py` is not fail-closed, and the handoff invites running it.**
Run from a fresh clone (no raw corpus, which is correctly git-ignored), it **regenerated
`RES-001-integrity-report.md` with every folder-byte figure zeroed and the entire archive-hash table
deleted — and exited 0.** `resources/HANDOFF.md` tells the reader "Rerun the script rather than
editing them." Anyone following that instruction on a clean machine would silently destroy committed
integrity evidence and see a success exit code.
This is the same defect class Eval already found and fixed in its own harness — "a run that raised
integrity errors still exited successfully". **Severity: HIGH for the Resources stream, but
domain-owned.**
**Resolution: routed** to Resources/Controller (R3). The Governor **reverted the regenerated file**
and committed nothing from it, per the regeneration rule now written into the Governor contract.

**F2 · Two authoritative artifacts cannot be reconstructed from GitHub alone.** Both are deliberate
consequences of keeping large or proprietary payloads out of Git, and neither is a defect — but
neither was written down, which made them invisible failure modes.
1. The **EVAL-005 battery items** live under a git-ignored `build/` directory, and the pinned font is
   a proprietary system asset that is not committed. The committed record fingerprints the 106-item
   build by SHA-256 so a rebuild can be *checked*, but on a machine without that font it cannot be
   *produced*. GOV-001's own 43-test battery run passed **only because the audit machine happens to
   be macOS and carries Kohinoor Devanagari as a system font.**
2. The **Resources composition verifier** reads the git-ignored raw corpus and cannot run from a
   clone.
**Resolution: corrected in documentation** — both are now recorded as named limitations in
`PROJECT-MEMORY.md` §7 and `coordination/AUTOMATION-ROADMAP.md`.

**F3 · `verify_devanagari_composition.py` reports vacuous passes on empty input.** With no corpus
present it prints `[PASS] categories are pairwise DISJOINT (0 shared files)` and `[PASS] categories
sum to acquired media (EXHAUSTIVE)` over empty sets, before dying on an unhandled
`ValueError: min() iterable argument is empty`. The exit code is correctly 1, so the failure is not
silent — but "an empty check must not read as success" is a rule this project has already learned
once. **Domain-owned. Resolution: routed** (R4).

**F4 · Context burden is high but not yet unmanageable.** 32,478 lines of Markdown across 187 files.
A worker following the runbook reads roughly 750–850 lines before touching its task
(`PROJECT-MEMORY.md` + contract + standard + charter + handoff). `eval/HANDOFF.md` alone is 495
lines and is the strongest candidate for future compression, though its content is dense rather than
padded. **No action taken** — compression is a judgement call better made after the next merged task,
and the handoff is stream-owned. **Recorded for the next periodic audit.**

**F5 · No evidence of unauthorized methodology change was found.** Every SPEC amendment traces to a
Controller-approved task, both new controlled-vocabulary terms
(`shared_primary_informant`, `figure_semantic_binding_lost`) appear in the normative gate document,
the validator, the test suite and at least one audit record, and `canon/experiments/audit-gate-v0.2/`
was correctly emptied to a pointer with a test asserting no duplicate copy reappears. **This is good
hygiene and is recorded as a positive finding.**

### ROUTED — domain-owned, not fixed by the Governor

The Governor may not edit stream handoffs, task files or Controller Briefs. Each of these is real,
evidence-backed, and returned to its owner.

| # | Issue | Path | Severity | Owner |
|---|---|---|---|---|
| **R1** | **CANON-001 and CANON-002 outputs are not on `main`.** Their Controller Briefs, findings, and two extracted knowledge directories (`molly-bang`, `robin-williams-proximity`) exist only on unmerged branches — yet `canon/tasks/CANON-003.md` cites both tasks as the evidence that motivated the batch. The evidence chain has a hole. | `work/canon-003-*` branches | **High** | Canon / Controller |
| **R2** | **EVAL-004's Reader-A freeze and attestation are not on `main`** (`READER-A-FREEZE.md`, `READER-ATTESTATION.md`), although the merged stop decision says the Reader-A pass "may be retained as exploratory pilot evidence". The decision refers to evidence `main` does not hold. | `work/eval-004` | **High** | Eval / Controller |
| **R3** | `build_reports.py` silently degrades and exits 0 when the corpus is absent; the handoff instructs rerunning it. | `resources/scripts/build_reports.py`, `resources/HANDOFF.md` | **High** | Resources |
| **R4** | `verify_devanagari_composition.py` emits vacuous `[PASS]` lines on empty input and dies on an unhandled `ValueError`. | `resources/scripts/verify_devanagari_composition.py` | Medium | Resources |
| **R5** | `canon/tasks/CANON-007.md` still reads `Status: OPEN — Controller-assigned`. CANON-007 completed and merged (PR #10). | `canon/tasks/CANON-007.md` | Medium | Canon |
| **R6** | `canon/tasks/CANON-008.md` still reads `Status: OPEN`. It is stopped at the acquisition gate and `needs_controller_review`. | `canon/tasks/CANON-008.md` | Medium | Canon |
| **R7** | `canon/HANDOFF.md` ends with "**Wait for the Controller's CANON-004 decision**" — that decision was made on 25 Aug and applied by CANON-005. It contradicts the same file's own current and accurate summary. | `canon/HANDOFF.md` | Medium | Canon |
| **R8** | `eval/HANDOFF.md` "CURRENT TASK / QUEUE" says EVAL-005 is "awaiting Controller review on `work/eval-005-controller-review`". That branch merged (PR #8), as did two later EVAL-005 PRs. Contradicts the same file's own "NEXT APPROVED TASK: None". | `eval/HANDOFF.md` | Medium | Eval |
| **R9** | `eval/tasks/EVAL-005-CONTROLLER-BRIEF.md` reads "complete; **awaiting Controller review** … no human validation ha[s] occurred" with **no supersession banner**, while its sibling `EVAL-005.md` correctly carries one. Human validation is complete and frozen. | `eval/tasks/EVAL-005-CONTROLLER-BRIEF.md` | Medium | Eval |
| **R10** | `resources/HANDOFF.md` says the EVAL-003 correction is "awaiting PR review". It merged as PR #5. | `resources/HANDOFF.md` | Medium | Resources |
| **R11** | `resources/PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md` proposes a replacement Resources row for `coordination/WORKSTREAM-STATUS.md` and remains unactioned. GOV-001 corrected that row from primary evidence rather than by adopting the proposal, so the proposal still needs a Controller disposition. | `resources/PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md` | Low | Controller |
| **R12** | Three broken internal links in domain files: `canon/experiments/CANON-EXPERIMENT-V0.md` and `eval/battery/CAPABILITY-LAB-V0-PLAN.md` both link `EVAL-CORPUS-PLAN.md`, **which exists nowhere in the repository**; `canon/knowledge/SPEC-02-atom-schema.md` links `FINDINGS-10-…` as a sibling when it lives in `canon/findings/`. | as listed | Low | Canon / Eval |
| **R13** | **Only 4 of 13 recorded Controller decisions have a dedicated decision record**; the rest are evidenced inside a Controller Brief, task file or approved proposal, which mixes decision with worker narrative. Whether to normalise this is a Controller call. | `coordination/DECISION-LOG.md` index | Low | Controller |
| **R14** | `eval/rubrics/IDENTITY-CONSISTENCY-RUBRIC-V0-DRAFT.md` is frozen V0 but keeps `-DRAFT` in its filename. The file explains why (the approved task names that exact path) and states that the status inside governs. **Recorded as understood, not as a defect.** | as listed | Low | Eval |

---

## 5. Operational-document classification inventory

Every document that functions as current state, workstream status, handoff, task queue, decision
register, runbook, roadmap, charter, spec, resource request, or audit/current-state summary.

**Scope: 188 documents** — all 187 tracked Markdown files except the 6 raw source texts under
`canon/sources/` (which are source material, not operational documents), plus the 19 per-source
`PROVENANCE.md` files and the 5 SPEC files, plus one machine-readable state artifact
(`human-validation-v1.json`) that functions as a decision record, plus the 3 documents GOV-001
created. **Each document carries exactly one primary class.** The full row-by-row inventory is
Appendix A.

Classes: `CURRENT_AUTHORITY` (defines live truth for its area) · `SUPPORTING_CURRENT` (live and
useful, subordinate) · `HISTORICAL` (accurate about a finished period) · `SUPERSEDED` (replaced;
retained for comparison) · `REQUIRES_CORRECTION` (asserts a live state contradicted by evidence).

### Summary

| Class | Count |
|---|---|
| `CURRENT_AUTHORITY` | 38 |
| `SUPPORTING_CURRENT` | 43 |
| `HISTORICAL` | 91 |
| `SUPERSEDED` | 4 |
| `REQUIRES_CORRECTION` | 12 |
| **Total** | **188** |

**All 12 `REQUIRES_CORRECTION` documents are accounted for**: **6 corrected** by GOV-001, all in
`coordination/` (`CONTROL-STATE`, `WORKSTREAM-STATUS`, `DECISION-LOG`, `RUNBOOK`,
`AUTOMATION-ROADMAP`, `ASSUMPTIONS`); **6 routed** to their owning stream (`canon/HANDOFF.md`,
`canon/tasks/CANON-007.md`, `canon/tasks/CANON-008.md`, `eval/HANDOFF.md`,
`eval/tasks/EVAL-005-CONTROLLER-BRIEF.md`, `resources/HANDOFF.md`) as R5–R10.

Two further files were **corrected additively without being stale about live state**, so they remain
`CURRENT_AUTHORITY` rather than `REQUIRES_CORRECTION`: `coordination/PROJECT-CONTRACT.md` (Governor
role added) and `governance/README.md` (rewritten now that `PROJECT-MEMORY.md` exists).

The 4 `SUPERSEDED` documents are `governance/bootstrap/CONTROLLER-MIGRATION-SEED.md` (marked by this
task), `canon/knowledge/SPEC-02-atom-schema.md` (superseded conceptually by SPEC-03/04/05, retained
as evidence by explicit decision), `canon/PROPOSED-INTEGRATION-CHANGE-CANON-005-COORDINATION.md`
(actioned here), and `eval/tasks/PROPOSED-EVAL-005-CONTROLLER-BRIEF.md` (already self-marked).

The 91 `HISTORICAL` documents are overwhelmingly per-book findings, lane checkpoints, closed task
files and dated reports — forensic evidence of finished work. **None was edited.**

### Control plane — `coordination/`, `shared/`, `governance/`, root

| Document | Class | Note |
|---|---|---|
| `PROJECT-MEMORY.md` | `CURRENT_AUTHORITY` | Created by GOV-001. Canonical entry point. |
| `governance/GOVERNOR-CONTRACT.md` | `CURRENT_AUTHORITY` | Created by GOV-001. |
| `governance/audits/2026-08-25-…-audit.md` | `CURRENT_AUTHORITY` | This file. |
| `governance/README.md` | `CURRENT_AUTHORITY` | Corrected — previously said `PROJECT-MEMORY.md` "will be created". |
| `governance/tasks/GOV-001.md` | `CURRENT_AUTHORITY` | The task under execution. |
| `governance/bootstrap/CONTROLLER-MIGRATION-SEED.md` | `SUPERSEDED` | Marked **HISTORICAL / SUPERSEDED FOR BOOTSTRAP**. Retained unedited as forensic evidence of the migration boundary. |
| `coordination/PROJECT-CONTRACT.md` | `CURRENT_AUTHORITY` | Corrected: Governor role added; bootstrap order updated. Product/architecture content untouched. |
| `coordination/CONTROL-STATE.md` | `REQUIRES_CORRECTION` → corrected | H1. |
| `coordination/WORKSTREAM-STATUS.md` | `REQUIRES_CORRECTION` → corrected | H2. |
| `coordination/DECISION-LOG.md` | `REQUIRES_CORRECTION` → corrected | H4. Historical entries preserved verbatim. |
| `coordination/RUNBOOK.md` | `REQUIRES_CORRECTION` → corrected | M3. |
| `coordination/AUTOMATION-ROADMAP.md` | `REQUIRES_CORRECTION` → corrected | M1. Level A–D policy unchanged. |
| `coordination/ASSUMPTIONS.md` | `REQUIRES_CORRECTION` → corrected | M2, links only. **No entry status changed** — promoting an entry requires running its falsifier, which is a domain judgement. |
| `coordination/CANON-003-LANE-A-C-AUDIT.md` | `HISTORICAL` | M4, marked. |
| `coordination/CANON-003-BOOKS-08-10-AUDIT.md` | `HISTORICAL` | M4, marked. |
| `shared/COMMUNICATION-STANDARD.md` | `CURRENT_AUTHORITY` | Live, no drift. |
| `shared/AUTONOMY-POLICY.md` | `CURRENT_AUTHORITY` | Live, no drift. |
| `shared/templates/*.md` (4) | `SUPPORTING_CURRENT` | Live templates. |
| `docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md` | `CURRENT_AUTHORITY` | Approved design behind this task. |
| `docs/superpowers/plans/2026-08-25-governor-reset-cleanup-plan.md` | `SUPPORTING_CURRENT` | Plan for this task. |
| `docs/superpowers/plans/2026-08-24-canon-003-integration-16.md` | `HISTORICAL` | Executed and merged. |

### Canon

| Document(s) | Class | Note |
|---|---|---|
| `canon/CHARTER.md` | `CURRENT_AUTHORITY` | Boundary document, no drift. |
| `canon/audit/AUDIT-GATE-v0.2.md` | `CURRENT_AUTHORITY` | The live admission method. |
| `canon/decisions/*.md` (2) | `CURRENT_AUTHORITY` | Durable Controller decisions. |
| `canon/HANDOFF.md` | `REQUIRES_CORRECTION` → routed | R7. **Substantially accurate** on all counts and states; one stale closing line. |
| `canon/tasks/CANON-007.md`, `CANON-008.md` | `REQUIRES_CORRECTION` → routed | R5, R6 — stale `OPEN` status. |
| `canon/tasks/CANON-001…006`, `CANON-003-PARALLEL-EXECUTION`, `CANON-003-REBALANCE-01` (8) | `HISTORICAL` | Completed/closed tasks. |
| `canon/findings/CANON-008-CONTROLLER-BRIEF.md` | `SUPPORTING_CURRENT` | Live decision input — `needs_controller_review`. |
| `canon/findings/CANON-003…007 briefs, lane checkpoints, issues, per-book findings, synthesis` (34) | `HISTORICAL` | Forensic evidence of finished work. |
| `canon/findings/FINDINGS-02…11`, `DIRECTION-RESET-01` (11) | `HISTORICAL` | Pre-batch probe evidence; FINDINGS-08/09/10/11 conclusions corrected in `DECISION-LOG.md` with originals retained. |
| `canon/PROPOSED-INTEGRATION-CHANGE-CANON-005-COORDINATION.md` | `SUPERSEDED` | H3 — actioned by GOV-001 and itself partly overtaken by CANON-006. |
| `canon/PROPOSED-METHOD-CHANGE-CANON-006-LINEAGE.md` | `SUPPORTING_CURRENT` | Approved; carries the decision text for `shared_primary_informant`. |
| `canon/experiments/audit-gate-v0.2/README.md` | `HISTORICAL` | Exemplary pointer-only marker (F5). |
| `canon/experiments/CANON-COVERAGE-MAP-V0`, `CANON-CURRICULUM-V0`, `CANON-EXPERIMENT-V0` | `HISTORICAL` | Pre-batch planning; CANON-EXPERIMENT-V0 also R12. |

### Eval

| Document(s) | Class | Note |
|---|---|---|
| `eval/CHARTER.md` | `CURRENT_AUTHORITY` | No drift. |
| `eval/battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md` | `CURRENT_AUTHORITY` | The authoritative battery state. |
| `…/human-validation/human-validation-v1.json` | `CURRENT_AUTHORITY` | Machine-readable frozen decision; **hashes verified**. |
| `…/CHECKER-CONTRACT.md`, `METRICS-AND-QUALIFICATION.md`, `NATIVE-VALIDATION.md`, `FAILURE-TAXONOMY.md`, `README.md` | `CURRENT_AUTHORITY` | All five correctly banner the 96-vs-106 distinction. **Good hygiene.** |
| `eval/decisions/EVAL-004-STOP-2026-08-24.md` | `CURRENT_AUTHORITY` | Binding stop decision. |
| `eval/HANDOFF.md` | `REQUIRES_CORRECTION` → routed | R8. Otherwise current and accurate. |
| `eval/tasks/EVAL-005-CONTROLLER-BRIEF.md` | `REQUIRES_CORRECTION` → routed | R9 — missing supersession banner. |
| `eval/tasks/EVAL-005.md` | `HISTORICAL` | Correctly bannered as superseded on current state. |
| `eval/tasks/PROPOSED-EVAL-005-CONTROLLER-BRIEF.md` | `SUPERSEDED` | Already carries an explicit banner naming what it supersedes. |
| `eval/tasks/EVAL-005-RESOURCES-REQUEST.md` | `SUPPORTING_CURRENT` | Live request, explicitly **not** an approved task. |
| `eval/tasks/EVAL-001…004` and their briefs, `EVAL-003-*-PASS` (10) | `HISTORICAL` | Closed tasks. |
| `eval/battery/CAPABILITY-BATTERY-V0-DRAFT.md`, `CAPABILITY-LAB-V0-PLAN.md`, `INSTRUMENT-CALIBRATION-PLAN-V0.md`, `M1B-…-V0.md`, `GENERATED-GLYPH-STRESS-LAYER.md`, `PROPOSED-TASK-SPEC.md` | `SUPPORTING_CURRENT` | Approved designs, none implemented or run. `CAPABILITY-LAB-V0-PLAN.md` also R12. |
| `eval/rubrics/IDENTITY-CONSISTENCY-RUBRIC-V0-DRAFT.md` | `SUPPORTING_CURRENT` | Frozen V0, not validated, never used. R14. |
| `eval/calibration/devanagari-v0/*.md` (4), `eval/harness/README.md`, `…/native-validation/README.md` | `SUPPORTING_CURRENT` | Live descriptions of untouched, available material. |
| `eval/findings/*.md` (5) | `HISTORICAL` | Dated findings; FINDINGS-01 correctly self-labels as preliminary. |
| `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md` | `SUPPORTING_CURRENT` | Open cross-stream proposal. |

### Resources

| Document(s) | Class | Note |
|---|---|---|
| `resources/CHARTER.md` | `CURRENT_AUTHORITY` | Includes the approved transient-acquisition policy. |
| `resources/HANDOFF.md` | `REQUIRES_CORRECTION` → routed | R10 (stale "awaiting PR review") and R3 (the rerun instruction). All corpus figures verified correct. |
| `resources/reports/RES-001-integrity-report.md`, `RES-001-bias-and-coverage-report.md` | `CURRENT_AUTHORITY` | Generated from the manifest. **Committed versions are correct**; see F1 before regenerating. |
| `resources/sources/src_*.md` (12) | `CURRENT_AUTHORITY` | Per-source rights and access records. |
| `resources/reports/RES-001-source-assessment.md`, `RES-002-transient-acquisition.md`, `RES-002-privacy-deletion-log.md`, `RES-CORRECTION-01-…md` | `HISTORICAL` | Dated task reports; the privacy deletion log is a permanent compliance record. |
| `resources/tasks/RES-001*, RES-002*` (4) | `HISTORICAL` | Closed and merged. |
| `resources/corpus/CORPUS-SOURCING-PLAN.md` | `HISTORICAL` | Pre-acquisition plan. |
| `resources/PROPOSED-INTEGRATION-CHANGE-RES-002-EVAL.md` | `SUPPORTING_CURRENT` | Tells Eval what the corpus does and does not test. |
| `resources/PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md` | `SUPPORTING_CURRENT` | R11 — awaiting Controller disposition. |

---

## 6. Migration-seed reconciliation

Required by GOV-001. Every material claim in `governance/bootstrap/CONTROLLER-MIGRATION-SEED.md`,
checked against committed evidence.

| Seed § | Claim | Status | Evidence |
|---|---|---|---|
| 1 | Product thesis, four-role architecture, frozen separations | **CONFIRMED** | `coordination/PROJECT-CONTRACT.md` |
| 1 | Production IR and Capability Registry not implemented | **CONFIRMED** | No such artifact anywhere in the tree |
| 2 | Audit freeze on all new domain work | **CONFIRMED** | Seed §2 + `governance/README.md`; no open task in any stream |
| 3 | CANON-003 historical baseline = 16, with the exact 16 titles listed | **CONFIRMED — mechanically** | `validate_canon003_integrated.py` → 16 books, 0 errors; all 16 titles map to `knowledge/current` directories |
| 3 | *Thinking with Type* historically blocked, not counted | **CONFIRMED** | Absent from `knowledge/current`; source text present in `canon/sources/` |
| 3 | Audit Gate v0.2 authoritative from CANON-005, incl. `evidence_insufficient` | **CONFIRMED** | `canon/audit/AUDIT-GATE-v0.2.md`, `canon/decisions/CANON-004-…md`, validator |
| 3 | CANON-006 admitted *Master Shots* + *The Conversations*; `shared_primary_informant` approved as a pairwise symmetric dependency; incidental quotation insufficient; 16 → 18 | **CONFIRMED** | Both audit records + knowledge dirs present; relation in gate doc, validator, tests, and `ondaatje-conversations-ch3.audit.yaml` |
| 3 | CANON-007 admitted *Effectiveness in Context*; `figure_semantic_binding_lost` added; 18 → 19 | **CONFIRMED** | `binet-field-…` record + directory; term in gate doc, validator, tests, record |
| 3 | CANON-008 stopped at the acquisition gate; live Canon stays **19, not 20** | **CONFIRMED** | `canon/findings/CANON-008-CONTROLLER-BRIEF.md`; **19** directories and **19** records at baseline |
| 4 | EVAL-003 produced a 54-item Hindi-primary pack; EVAL-004 exploratory and stopped | **CONFIRMED** | `eval/calibration/devanagari-v0/`, `eval/decisions/EVAL-004-STOP-2026-08-24.md` |
| 4 | EVAL-005 design constraints (blind transcribe payload, pinned font, decoded-pixel visibility, deterministic zero-false-pass gate, iid figure as reference only) | **CONFIRMED** | Battery docs, `checker_input.py`, `pngraster.py`, 43 passing tests |
| 4 | Original battery = **106 items = 53 match + 53 mismatch** | **CONFIRMED** | Battery README/CONTROLLER-BRIEF; recorded `items_jsonl_sha256` |
| 4 | Human packet completed **98/98** by one reviewer; 5 base words and 2 broken renders accepted | **CONFIRMED — mechanically** | `human-validation-v1.json`: 53+25+20 = 98 answered, 0 unsure; both response hashes recomputed and matched |
| 4 | Controller decision **PRUNE, DO NOT REBUILD** | **CONFIRMED** | `human-validation-v1.json` `status` and `replacement_policy: NONE` |
| 4 | The 10 excluded item IDs, exactly as listed | **CONFIRMED — exact match** | `decisions.excluded_item_ids` = `dx-0000, 0003, 0005, 0020, 0039, 0053, 0056, 0058, 0073, 0092` |
| 4 | Validated view = 96 / 48 / 48 / 48 words / 33 hard / 20 classes / 5 groups | **CONFIRMED — exact match** | `expected_validated_state` |
| 4 | 106-item build preserved, not mutated | **CONFIRMED** | Explicit in the record and in five battery documents |
| 4 | PR #12 rebased derived checker payload paths to `../images/…` | **CONFIRMED** | Implemented and explained in `apply_human_validation.py` |
| 4 | PR #12 updated stale live Eval docs to the post-validation state | **CONFIRMED** | All five live battery docs carry the 96-vs-106 banner |
| 4 | Worker test counts should stay **agent-reported** unless rerun | **SUPERSEDED — now independently verified.** GOV-001 reran them; see §7. Note the environment qualifier in F2. | this audit |
| 5 | IndicSTR12 375 + 2,711 = 3,086; IIIT-ILST 176 + 1,214 = 1,390 | **CONFIRMED — mechanically** | Manifest: 3,086 and 1,390 exactly |
| 5 | 173/176 IIIT scenes shared; 1,205/1,214 crops derive from shared parents; 3,924 resolvable crop labels | **PARTIALLY CONFIRMED.** 173 cross-source byte-identical files confirmed from the manifest. The 1,205 and 3,924 figures depend on the **git-ignored corpus** and could not be recomputed — retained with the handoff/report as their provenance. | manifest + `resources/HANDOFF.md` |
| 5 | BSTD is a genuine cross-lineage reserve, untouched | **CONFIRMED** | Registry + manifest; no Eval task consumes it |
| 6 | Four external artifacts named | **PARTIALLY RESOLVED** — two found and inspected, two **not found**. See below. | §8 |
| 6 | Workbook counts "known to have become stale" as live Canon moved past 16 | **CONFIRMED — and stronger than stated.** Both inspected artifacts assert "Current live Canon on main: **16**" and that both reserve titles are "absent from main". Both statements are now false. | §8 |
| 6 | *Effectiveness in Context* since ingested, no longer a candidate | **CONFIRMED** | It is Wave-1 candidate 5 in the workbook and is live Canon source 19 |
| 6 | The Devanagari slot was redirected from a "Fiona Ross / Devanagari Type Design" identity to the Dalvi thesis | **CONFIRMED** | Workbook still lists the superseded identity; `CANON-008-CONTROLLER-BRIEF.md` names the supersession |
| 6 | Wave-1 access/licensing status leads (streaming-only, AI-use restriction, DRM, corpus-freeze mechanics) | **UNRESOLVED** | No committed evidence; the two artifacts that would carry it were not found |
| 7 | Qualitative Canon-vs-vanilla advertising comparison favoured the Canon arm | **RETAINED WITH WEAKER PROVENANCE** — recorded in `PROJECT-MEMORY.md` §8 as anecdotal external evidence licensing no capability claim | seed only |
| 8 | Control-plane drift leads (CONTROL-STATE, WORKSTREAM-STATUS, DECISION-LOG, RUNBOOK, AUTOMATION-ROADMAP, handoffs, Eval docs, acquisition boundary) | **CONFIRMED, and broadened.** All six named files were genuinely stale. GOV-001 additionally found H3, M2, M5, M6, F1–F4 and R1–R14. **The Eval-docs lead was the one exception** — those were already corrected by PR #12 before this audit. | §4 |
| 9 | Nine "not safely recoverable" Controller decisions | **ALL CONFIRMED** and carried into `PROJECT-MEMORY.md` and the `DECISION-LOG.md` index | §4 H4 |

**Disposition.** Every material seed claim was confirmed, or explicitly downgraded above. **Nothing
in the seed was contradicted by the repository.** The seed is marked
**HISTORICAL / SUPERSEDED FOR BOOTSTRAP** and retained unedited as forensic evidence.

**One unresolved migration dependency remains:** `WAVE-1-ACQUISITION-REPORT.md` and
`ACQUISITION-MANIFEST.xlsx` were not found and were not inspected. The seed §6 Wave-1 access and
licensing statuses rest on them and are recorded as **unverified**. This does not block GOV-001, but
the Controller should either supply those artifacts or accept their content into GitHub before any
acquisition decision relies on them.

---

## 7. Verification performed

All commands run from a fresh clone of the audited baseline on macOS (Darwin 23.6.0), Python 3.14.6
in a local `.venv` with `pyyaml 6.0.3` and `pytest 9.1.1`, Node v25.9.0.

| # | Command | Result |
|---|---|---|
| 1 | `python -m pytest tests/ -q` | **65 passed, 93 subtests passed** in 1.75s. Exit 0. |
| 2 | `python canon/validation/validate_audit_gate_v02.py` | **`record_count: 19`, `error_count: 0`, `errors: []`.** Exit 0. |
| 3 | `python canon/validation/validate_canon003_integrated.py` | **16 books, 505 source-knowledge, 54 systems, 417 terms, 53 concepts, 111 bindings, `error_count: 0`.** Exit 0. |
| 4 | `node eval/harness/run-fixture.mjs --selftest` | **SELFTEST OK — all groups passed**, incl. 27 stored transcriptions re-scored via both code paths with 0 mismatches. Exit 0. |
| 5 | `python -m pytest eval/battery/devanagari-exactness/test_devanagari_exactness.py -q` | **43 passed** in 92.2s. Exit 0. **Qualifier: passed only because the audit machine carries the pinned font as a macOS system asset (F2).** |
| 6 | `python resources/scripts/verify_devanagari_composition.py` | **NOT VERIFIED — could not run.** Requires the git-ignored raw corpus. Exit 1 with `[FAIL]` lines and an unhandled `ValueError`. **Recorded as unrun, not as a pass** (F3/R4). |
| 7 | `python resources/scripts/build_reports.py` | **Ran, exit 0, but produced a degraded artifact** — regenerated `RES-001-integrity-report.md` with zeroed folder bytes and the archive-hash table removed. **Working tree reverted; nothing committed.** (F1/R3). |
| 8 | Manifest reconstruction from `corpus-pilot-v0.jsonl` | All seven Resources headline figures match exactly (§3.4). |
| 9 | SHA-256 recomputation of both EVAL-005 human-validation response artifacts | **Both match** their recorded hashes (§3.3). |
| 10 | Repository-wide relative Markdown link check (187 files) | 6 broken links at baseline. **3 corrected** (M2), **3 routed** (R12). **0 broken links introduced by GOV-001** — re-run clean over all files this task added or edited. |
| 11 | Branch/merge reconstruction across 23 remote branches | 17 report unmerged due to squash merges; 2 hold genuinely absent evidence (R1, R2). |
| 12 | Diff review against the audited baseline | See §9. |

### What could not be verified

- **The Resources composition verifier (#6) and any figure derived from the raw corpus** —
  specifically the 1,205/1,214 crop-derivation figure and the 3,924 resolvable crop labels. The
  corpus is deliberately git-ignored. **Unverified, not failed.**
- **The EVAL-005 battery cannot be rebuilt on a machine without the pinned proprietary font.** Test
  run #5 is a pass *on this machine*; it is not evidence that a fresh clone reproduces the battery.
- **No checker, model or API was called**, per the task's boundaries and the standing ₹0 spend
  constraint. Nothing here speaks to any model's ability.
- **Two external research artifacts were not found** (§6).

---

## 8. External research artifacts

Inspected with explicit external-research provenance. **Neither competes with repository truth.**

Located in the operator's local `~/Downloads`, both dated 24 Aug 2026:
`creative_production_canon_expansion_report (1).docx` (183 paragraphs, 2 tables) and
`creative_production_canon_candidate_universe (1).xlsx` (7 sheets; 96-row candidate universe,
22-row exact portfolio).

**Both are now contradicted by the repository on their central arithmetic.** The workbook's "Canon
state" sheet records `Current live Canon on main = 16` and the report states "Master Shots and The
Conversations: substantial branch work exists, but neither is on main or Controller-accepted live."
CANON-006 admitted both on 25 Aug; live Canon is 19.

The workbook anticipated exactly this and wrote the rule down — *"If either deferred branch is
separately audited and accepted before this portfolio executes, the Controller should raise the live
baseline at that moment"* — but was never updated. **Its 22-source portfolio and its projected total
of 38 live sources rest on the stale base of 16 and must be recomputed before use.**

Two further reconciliations: Wave-1 candidate 5, *Effectiveness in Context*, **has since been
ingested** as CANON-007 and is no longer a candidate. Wave-1 candidate 7 still carries the superseded
"Devanagari Type Design" identity that CANON-008 replaced with the Dalvi thesis.

`WAVE-1-ACQUISITION-REPORT.md` and `ACQUISITION-MANIFEST.xlsx` **were not found**.

**Status recorded in `PROJECT-MEMORY.md`: external research snapshot, materially stale on live Canon
state, with two artifacts unverified.**

---

## 9. Diff review against the audited baseline

Every file GOV-001 changed, and why it is inside the write boundary.

**Created (3):** `PROJECT-MEMORY.md`, `governance/GOVERNOR-CONTRACT.md`, this audit.

**Modified (11):** `governance/README.md`, `governance/bootstrap/CONTROLLER-MIGRATION-SEED.md`
(banner only, body unedited), and nine files in `coordination/` — `PROJECT-CONTRACT.md`,
`CONTROL-STATE.md`, `WORKSTREAM-STATUS.md`, `DECISION-LOG.md`, `RUNBOOK.md`,
`AUTOMATION-ROADMAP.md`, `ASSUMPTIONS.md`, `CANON-003-LANE-A-C-AUDIT.md` and
`CANON-003-BOOKS-08-10-AUDIT.md`.

**Total: 14 files changed, +1,751 / −130 lines.** All 130 deleted lines are control-plane lines,
preserved in Git history: `WORKSTREAM-STATUS.md` 52, `CONTROL-STATE.md` 49, `RUNBOOK.md` 16
(the obsolete worktree block), `AUTOMATION-ROADMAP.md` 5, `governance/README.md` 3,
`PROJECT-CONTRACT.md` 2, `ASSUMPTIONS.md` 2 (link targets), `DECISION-LOG.md` 1 (link target).
**Zero deletions in any domain directory.**

**Confirmed unchanged:**

- **Zero files under `canon/`, `eval/`, `resources/`, `tests/`, `shared/` or `docs/`.**
- No Canon source knowledge, audit record, spec, validator or test.
- No Eval battery, threshold, result, task, brief or finding.
- No Resources dataset, manifest, report, source record or script — including the report GOV-001
  regenerated during verification and then reverted.
- No historical baseline was mutated. `validate_canon003_integrated.py` and its 16-book result are
  byte-identical to the baseline.
- No methodology, schema or benchmark design was altered.
- No task was opened, authorized or started.

**On historical numbers.** Where a document legitimately recorded a past measurement — the 13/18 in
`CANON-003-BOOKS-08-10-AUDIT.md`, the 16-book CANON-003 record, the 106-item build — the number was
**preserved and labelled**, never replaced with the current figure. Only claims asserting a *live*
state that evidence contradicts were rewritten.

---

## 10. Zero-chat bootstrap test

Performed as required: assume no conversation exists; using only `PROJECT-MEMORY.md` and the files it
links, answer each question.

| Question | Answerable? | From |
|---|---|---|
| What is the product and what is success? | **Yes** | §1 + `PROJECT-CONTRACT.md` |
| What has actually been built? | **Yes** | §4 — 19 Canon sources, a 96-item validated battery, a 34,786-item corpus |
| What is live versus historical? | **Yes** | §4 tables state both numbers side by side with their meanings |
| What is frozen and may not be reopened? | **Yes** | §3 + `PROJECT-CONTRACT.md` |
| What is unresolved or unverified? | **Yes** | §7, including the two reproducibility limits and the routed evidence gaps |
| What may happen next, and who decides? | **Yes** | §5 — the freeze, and five named Controller decisions |
| Which file proves any given claim? | **Yes** | §10 authority map |
| How do I start a session in my role? | **Yes** | §11 |

**No answer depended on remembered chat.** Two answers depend on files GOV-001 created, which is the
intended design.

**Residual bootstrap risk, stated honestly.** A zero-context agent can fully understand the project
and its state, but **cannot reproduce two artifacts**: the EVAL-005 battery build (needs a
proprietary font) and any corpus-derived Resources figure (needs the git-ignored media). Both are
now named limitations rather than silent traps. That is a genuine, bounded gap in "GitHub alone is
sufficient" — the *knowledge* is complete; the *reproduction* is not.

---

## 11. Verdict

**PASS WITH NON-BLOCKING NOTES.**

**Why not a clean PASS:** fourteen routed issues remain open, two of which (R1, R2) mean committed
decisions on `main` refer to evidence `main` does not hold, and one of which (R3) is a script that
can destroy committed evidence while reporting success. None is the Governor's to fix, and none
blocks this task.

**Why not BLOCK:** every high-severity control-plane contradiction found is corrected here; no domain
evidence was altered; no historical baseline was mutated; every mechanically checkable fact that
could be checked, was, and passed.

**The strongest positive finding** is that the domain streams' own discipline held. Historical and
live Canon counts were kept distinct by the workers themselves; the 96-vs-106 battery distinction is
correctly bannered in all five live Eval documents; the audit-gate experiment directory was emptied to
a pointer with a test guarding against a duplicate reappearing; and the human-validation decision is
recorded in machine-readable form with verifiable hashes. **The drift was concentrated almost entirely
in the control plane — the layer that had no owner until now.**

**Recommended next steps for the Controller** (recommendations, not decisions, and explicitly **not**
authorizations):

1. Merge GOV-001 and lift or re-scope the audit freeze.
2. Dispose of R1 and R2 — merge the stranded evidence, or record a decision that it is abandoned.
   Leaving decisions pointing at absent evidence is the worst of the three options.
3. Route R3 to Resources as a small bounded fix; it is the only finding that can actively destroy
   evidence.
4. Decide the routed stale statuses R5–R10 as a single small hygiene pass in each stream.
5. Supply or formally set aside the two missing external acquisition artifacts before any acquisition
   decision relies on them.

**GOV-002 has not been started, no domain task was opened, and nothing was merged.**

---

## Appendix A — full classification inventory

Derived mechanically at the audited baseline plus GOV-001's own additions. One primary class per document.

| # | Class | Document |
|---:|---|---|
| 1 | `CURRENT_AUTHORITY` | `canon/CHARTER.md` |
| 2 | `REQUIRES_CORRECTION` | `canon/HANDOFF.md` |
| 3 | `SUPERSEDED` | `canon/PROPOSED-INTEGRATION-CHANGE-CANON-005-COORDINATION.md` |
| 4 | `SUPPORTING_CURRENT` | `canon/PROPOSED-METHOD-CHANGE-CANON-006-LINEAGE.md` |
| 5 | `CURRENT_AUTHORITY` | `canon/audit/AUDIT-GATE-v0.2.md` |
| 6 | `CURRENT_AUTHORITY` | `canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md` |
| 7 | `CURRENT_AUTHORITY` | `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md` |
| 8 | `HISTORICAL` | `canon/experiments/CANON-COVERAGE-MAP-V0.md` |
| 9 | `HISTORICAL` | `canon/experiments/CANON-CURRICULUM-V0.md` |
| 10 | `HISTORICAL` | `canon/experiments/CANON-EXPERIMENT-V0.md` |
| 11 | `HISTORICAL` | `canon/experiments/audit-gate-v0.2/README.md` |
| 12 | `HISTORICAL` | `canon/findings/CANON-003-CONTROLLER-BRIEF.md` |
| 13 | `HISTORICAL` | `canon/findings/CANON-003-HANDOVER-CHECKPOINT.md` |
| 14 | `HISTORICAL` | `canon/findings/CANON-003-INTEGRATION-VALIDATION.md` |
| 15 | `HISTORICAL` | `canon/findings/CANON-003-batch-issue-ledger.md` |
| 16 | `HISTORICAL` | `canon/findings/CANON-003-book01-grammar-of-the-shot-findings.md` |
| 17 | `HISTORICAL` | `canon/findings/CANON-003-book02-ogilvy-findings.md` |
| 18 | `HISTORICAL` | `canon/findings/CANON-003-book03-lsm-findings.md` |
| 19 | `HISTORICAL` | `canon/findings/CANON-003-book06-samara-findings.md` |
| 20 | `HISTORICAL` | `canon/findings/CANON-003-book07-freeman-findings.md` |
| 21 | `HISTORICAL` | `canon/findings/CANON-003-book08-alton-findings.md` |
| 22 | `HISTORICAL` | `canon/findings/CANON-003-book09-grammar-of-the-edit-findings.md` |
| 23 | `HISTORICAL` | `canon/findings/CANON-003-book10-murch-blink-findings.md` |
| 24 | `HISTORICAL` | `canon/findings/CANON-003-book11-master-shots-findings.md` |
| 25 | `HISTORICAL` | `canon/findings/CANON-003-book12-conversations-findings.md` |
| 26 | `HISTORICAL` | `canon/findings/CANON-003-book16-catmull-findings.md` |
| 27 | `HISTORICAL` | `canon/findings/CANON-003-book17-art-and-fear-findings.md` |
| 28 | `HISTORICAL` | `canon/findings/CANON-003-book18-storybrand-findings.md` |
| 29 | `HISTORICAL` | `canon/findings/CANON-003-lane-A-checkpoint.md` |
| 30 | `HISTORICAL` | `canon/findings/CANON-003-lane-A-issues.md` |
| 31 | `HISTORICAL` | `canon/findings/CANON-003-lane-B-checkpoint.md` |
| 32 | `HISTORICAL` | `canon/findings/CANON-003-lane-B-issues.md` |
| 33 | `HISTORICAL` | `canon/findings/CANON-003-lane-C-checkpoint.md` |
| 34 | `HISTORICAL` | `canon/findings/CANON-003-lane-C-issues.md` |
| 35 | `HISTORICAL` | `canon/findings/CANON-003-lane-D-checkpoint.md` |
| 36 | `HISTORICAL` | `canon/findings/CANON-003-lane-D-issues.md` |
| 37 | `HISTORICAL` | `canon/findings/CANON-003-multi-source-synthesis.md` |
| 38 | `HISTORICAL` | `canon/findings/CANON-003-rebalance-lane-checkpoint.md` |
| 39 | `HISTORICAL` | `canon/findings/CANON-003-rebalance-lane-issues.md` |
| 40 | `HISTORICAL` | `canon/findings/CANON-003-source-inventory-and-selection.md` |
| 41 | `HISTORICAL` | `canon/findings/CANON-004-CONTROLLER-BRIEF.md` |
| 42 | `HISTORICAL` | `canon/findings/CANON-004-audit-gate-design.md` |
| 43 | `HISTORICAL` | `canon/findings/CANON-005-CONTROLLER-BRIEF.md` |
| 44 | `HISTORICAL` | `canon/findings/CANON-006-CONTROLLER-BRIEF.md` |
| 45 | `HISTORICAL` | `canon/findings/CANON-007-CONTROLLER-BRIEF.md` |
| 46 | `SUPPORTING_CURRENT` | `canon/findings/CANON-008-CONTROLLER-BRIEF.md` |
| 47 | `HISTORICAL` | `canon/findings/DIRECTION-RESET-01-CANON-ROLE.md` |
| 48 | `HISTORICAL` | `canon/findings/FINDINGS-02-molly-bang-pass1.md` |
| 49 | `HISTORICAL` | `canon/findings/FINDINGS-03-molly-bang-visual-pass.md` |
| 50 | `HISTORICAL` | `canon/findings/FINDINGS-04-williams-proximity-pass1.md` |
| 51 | `HISTORICAL` | `canon/findings/FINDINGS-05-lupton-hierarchy-pass1.md` |
| 52 | `HISTORICAL` | `canon/findings/FINDINGS-06-gos-continuity-pass1.md` |
| 53 | `HISTORICAL` | `canon/findings/FINDINGS-07-ogilvy-pass1.md` |
| 54 | `HISTORICAL` | `canon/findings/FINDINGS-08-lsm-reflection-pass1.md` |
| 55 | `HISTORICAL` | `canon/findings/FINDINGS-09-aggregate-six-probes.md` |
| 56 | `HISTORICAL` | `canon/findings/FINDINGS-10-source-vs-binding-reaudit.md` |
| 57 | `HISTORICAL` | `canon/findings/FINDINGS-11-empirical-knowledge-join.md` |
| 58 | `CURRENT_AUTHORITY` | `canon/knowledge/SPEC-01-creative-ir.md` |
| 59 | `SUPERSEDED` | `canon/knowledge/SPEC-02-atom-schema.md` |
| 60 | `CURRENT_AUTHORITY` | `canon/knowledge/SPEC-03-source-knowledge.md` |
| 61 | `CURRENT_AUTHORITY` | `canon/knowledge/SPEC-04-operational-bindings.md` |
| 62 | `CURRENT_AUTHORITY` | `canon/knowledge/SPEC-05-knowledge-ontology.md` |
| 63 | `SUPPORTING_CURRENT` | `canon/knowledge/current/albers-interaction-of-color/PROVENANCE.md` |
| 64 | `SUPPORTING_CURRENT` | `canon/knowledge/current/alton-painting-with-light-ch2/PROVENANCE.md` |
| 65 | `SUPPORTING_CURRENT` | `canon/knowledge/current/bayles-orland-art-and-fear/PROVENANCE.md` |
| 66 | `SUPPORTING_CURRENT` | `canon/knowledge/current/binet-field-effectiveness-in-context-ch1/PROVENANCE.md` |
| 67 | `SUPPORTING_CURRENT` | `canon/knowledge/current/catmull-creativity-inc-ch5/PROVENANCE.md` |
| 68 | `SUPPORTING_CURRENT` | `canon/knowledge/current/freeman-photographers-eye-graphic-guide/PROVENANCE.md` |
| 69 | `SUPPORTING_CURRENT` | `canon/knowledge/current/grammar-of-the-edit-ch3-5/PROVENANCE.md` |
| 70 | `SUPPORTING_CURRENT` | `canon/knowledge/current/grammar-of-the-shot-ch4/PROVENANCE.md` |
| 71 | `SUPPORTING_CURRENT` | `canon/knowledge/current/heath-made-to-stick-introduction/PROVENANCE.md` |
| 72 | `SUPPORTING_CURRENT` | `canon/knowledge/current/hopkins-scientific-advertising-ch1-7/PROVENANCE.md` |
| 73 | `SUPPORTING_CURRENT` | `canon/knowledge/current/kenworthy-master-shots-ch8/PROVENANCE.md` |
| 74 | `SUPPORTING_CURRENT` | `canon/knowledge/current/light-science-magic-ch3/PROVENANCE.md` |
| 75 | `SUPPORTING_CURRENT` | `canon/knowledge/current/miller-storybrand-sb7/PROVENANCE.md` |
| 76 | `SUPPORTING_CURRENT` | `canon/knowledge/current/murch-blink-p1-25/PROVENANCE.md` |
| 77 | `SUPPORTING_CURRENT` | `canon/knowledge/current/ogilvy-ch2-advertising-that-sells/PROVENANCE.md` |
| 78 | `SUPPORTING_CURRENT` | `canon/knowledge/current/ondaatje-conversations-ch3/PROVENANCE.md` |
| 79 | `SUPPORTING_CURRENT` | `canon/knowledge/current/samara-making-breaking-grid-ch1/PROVENANCE.md` |
| 80 | `SUPPORTING_CURRENT` | `canon/knowledge/current/sutherland-alchemy-introduction/PROVENANCE.md` |
| 81 | `SUPPORTING_CURRENT` | `canon/knowledge/current/vignelli-canon-intangibles/PROVENANCE.md` |
| 82 | `HISTORICAL` | `canon/knowledge/migration/AUDIT-grammar-of-the-shot.md` |
| 83 | `HISTORICAL` | `canon/knowledge/migration/AUDIT-light-science-and-magic.md` |
| 84 | `HISTORICAL` | `canon/knowledge/migration/AUDIT-lupton.md` |
| 85 | `HISTORICAL` | `canon/knowledge/migration/AUDIT-molly-bang.md` |
| 86 | `HISTORICAL` | `canon/knowledge/migration/AUDIT-ogilvy.md` |
| 87 | `HISTORICAL` | `canon/knowledge/migration/AUDIT-williams.md` |
| 88 | `HISTORICAL` | `canon/tasks/CANON-001.md` |
| 89 | `HISTORICAL` | `canon/tasks/CANON-002.md` |
| 90 | `HISTORICAL` | `canon/tasks/CANON-003-PARALLEL-EXECUTION.md` |
| 91 | `HISTORICAL` | `canon/tasks/CANON-003-REBALANCE-01.md` |
| 92 | `HISTORICAL` | `canon/tasks/CANON-003.md` |
| 93 | `HISTORICAL` | `canon/tasks/CANON-004.md` |
| 94 | `HISTORICAL` | `canon/tasks/CANON-005.md` |
| 95 | `HISTORICAL` | `canon/tasks/CANON-006.md` |
| 96 | `REQUIRES_CORRECTION` | `canon/tasks/CANON-007.md` |
| 97 | `REQUIRES_CORRECTION` | `canon/tasks/CANON-008.md` |
| 98 | `REQUIRES_CORRECTION` | `coordination/ASSUMPTIONS.md` |
| 99 | `REQUIRES_CORRECTION` | `coordination/AUTOMATION-ROADMAP.md` |
| 100 | `HISTORICAL` | `coordination/CANON-003-BOOKS-08-10-AUDIT.md` |
| 101 | `HISTORICAL` | `coordination/CANON-003-LANE-A-C-AUDIT.md` |
| 102 | `REQUIRES_CORRECTION` | `coordination/CONTROL-STATE.md` |
| 103 | `REQUIRES_CORRECTION` | `coordination/DECISION-LOG.md` |
| 104 | `CURRENT_AUTHORITY` | `coordination/PROJECT-CONTRACT.md` |
| 105 | `REQUIRES_CORRECTION` | `coordination/RUNBOOK.md` |
| 106 | `REQUIRES_CORRECTION` | `coordination/WORKSTREAM-STATUS.md` |
| 107 | `HISTORICAL` | `docs/superpowers/plans/2026-08-24-canon-003-integration-16.md` |
| 108 | `SUPPORTING_CURRENT` | `docs/superpowers/plans/2026-08-25-governor-reset-cleanup-plan.md` |
| 109 | `CURRENT_AUTHORITY` | `docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md` |
| 110 | `CURRENT_AUTHORITY` | `eval/CHARTER.md` |
| 111 | `REQUIRES_CORRECTION` | `eval/HANDOFF.md` |
| 112 | `SUPPORTING_CURRENT` | `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md` |
| 113 | `SUPPORTING_CURRENT` | `eval/battery/CAPABILITY-BATTERY-V0-DRAFT.md` |
| 114 | `SUPPORTING_CURRENT` | `eval/battery/CAPABILITY-LAB-V0-PLAN.md` |
| 115 | `SUPPORTING_CURRENT` | `eval/battery/INSTRUMENT-CALIBRATION-PLAN-V0.md` |
| 116 | `SUPPORTING_CURRENT` | `eval/battery/M1B-DEVANAGARI-GENERATION-ITEM-DESIGN-V0.md` |
| 117 | `CURRENT_AUTHORITY` | `eval/battery/devanagari-exactness/CHECKER-CONTRACT.md` |
| 118 | `CURRENT_AUTHORITY` | `eval/battery/devanagari-exactness/FAILURE-TAXONOMY.md` |
| 119 | `SUPPORTING_CURRENT` | `eval/battery/devanagari-exactness/GENERATED-GLYPH-STRESS-LAYER.md` |
| 120 | `CURRENT_AUTHORITY` | `eval/battery/devanagari-exactness/METRICS-AND-QUALIFICATION.md` |
| 121 | `CURRENT_AUTHORITY` | `eval/battery/devanagari-exactness/NATIVE-VALIDATION.md` |
| 122 | `SUPPORTING_CURRENT` | `eval/battery/devanagari-exactness/PROPOSED-TASK-SPEC.md` |
| 123 | `CURRENT_AUTHORITY` | `eval/battery/devanagari-exactness/README.md` |
| 124 | `CURRENT_AUTHORITY` | `eval/battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md` |
| 125 | `CURRENT_AUTHORITY` | `eval/battery/devanagari-exactness/human-validation/human-validation-v1.json` |
| 126 | `SUPPORTING_CURRENT` | `eval/battery/devanagari-exactness/native-validation/README.md` |
| 127 | `SUPPORTING_CURRENT` | `eval/calibration/devanagari-v0/CALIBRATION-RUN-PLAN-V0.md` |
| 128 | `SUPPORTING_CURRENT` | `eval/calibration/devanagari-v0/HUMAN-REVIEW-GUIDE.md` |
| 129 | `SUPPORTING_CURRENT` | `eval/calibration/devanagari-v0/PROPOSED-V0-COMPOSITION.md` |
| 130 | `SUPPORTING_CURRENT` | `eval/calibration/devanagari-v0/README.md` |
| 131 | `CURRENT_AUTHORITY` | `eval/decisions/EVAL-004-STOP-2026-08-24.md` |
| 132 | `HISTORICAL` | `eval/findings/EVAL-001-battery-design-findings.md` |
| 133 | `HISTORICAL` | `eval/findings/EVAL-002-readiness-findings.md` |
| 134 | `HISTORICAL` | `eval/findings/EVAL-003-calibration-readiness-findings.md` |
| 135 | `HISTORICAL` | `eval/findings/FINDINGS-01-can-we-check.md` |
| 136 | `HISTORICAL` | `eval/findings/devanagari-exactness-design-findings.md` |
| 137 | `SUPPORTING_CURRENT` | `eval/harness/README.md` |
| 138 | `SUPPORTING_CURRENT` | `eval/rubrics/IDENTITY-CONSISTENCY-RUBRIC-V0-DRAFT.md` |
| 139 | `HISTORICAL` | `eval/tasks/EVAL-001-CONTROLLER-BRIEF.md` |
| 140 | `HISTORICAL` | `eval/tasks/EVAL-001.md` |
| 141 | `HISTORICAL` | `eval/tasks/EVAL-002-CONTROLLER-BRIEF.md` |
| 142 | `HISTORICAL` | `eval/tasks/EVAL-002.md` |
| 143 | `HISTORICAL` | `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md` |
| 144 | `HISTORICAL` | `eval/tasks/EVAL-003-CORRECTION-PASS.md` |
| 145 | `HISTORICAL` | `eval/tasks/EVAL-003-DOC-CONSISTENCY-CLEANUP.md` |
| 146 | `HISTORICAL` | `eval/tasks/EVAL-003-FINALIZATION-PASS.md` |
| 147 | `HISTORICAL` | `eval/tasks/EVAL-003.md` |
| 148 | `HISTORICAL` | `eval/tasks/EVAL-004-HUMAN-REFERENCE.md` |
| 149 | `REQUIRES_CORRECTION` | `eval/tasks/EVAL-005-CONTROLLER-BRIEF.md` |
| 150 | `SUPPORTING_CURRENT` | `eval/tasks/EVAL-005-RESOURCES-REQUEST.md` |
| 151 | `HISTORICAL` | `eval/tasks/EVAL-005.md` |
| 152 | `SUPERSEDED` | `eval/tasks/PROPOSED-EVAL-005-CONTROLLER-BRIEF.md` |
| 153 | `CURRENT_AUTHORITY` | `governance/README.md` |
| 154 | `SUPERSEDED` | `governance/bootstrap/CONTROLLER-MIGRATION-SEED.md` |
| 155 | `CURRENT_AUTHORITY` | `governance/tasks/GOV-001.md` |
| 156 | `CURRENT_AUTHORITY` | `resources/CHARTER.md` |
| 157 | `REQUIRES_CORRECTION` | `resources/HANDOFF.md` |
| 158 | `SUPPORTING_CURRENT` | `resources/PROPOSED-INTEGRATION-CHANGE-RES-002-EVAL.md` |
| 159 | `SUPPORTING_CURRENT` | `resources/PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md` |
| 160 | `HISTORICAL` | `resources/corpus/CORPUS-SOURCING-PLAN.md` |
| 161 | `CURRENT_AUTHORITY` | `resources/reports/RES-001-bias-and-coverage-report.md` |
| 162 | `CURRENT_AUTHORITY` | `resources/reports/RES-001-integrity-report.md` |
| 163 | `HISTORICAL` | `resources/reports/RES-001-source-assessment.md` |
| 164 | `HISTORICAL` | `resources/reports/RES-002-privacy-deletion-log.md` |
| 165 | `HISTORICAL` | `resources/reports/RES-002-transient-acquisition.md` |
| 166 | `HISTORICAL` | `resources/reports/RES-CORRECTION-01-indicstr12-composition.md` |
| 167 | `CURRENT_AUTHORITY` | `resources/sources/src_ava.md` |
| 168 | `CURRENT_AUTHORITY` | `resources/sources/src_bstd_devanagari.md` |
| 169 | `CURRENT_AUTHORITY` | `resources/sources/src_iiit_ilst_devanagari.md` |
| 170 | `CURRENT_AUTHORITY` | `resources/sources/src_imagerewarddb.md` |
| 171 | `CURRENT_AUTHORITY` | `resources/sources/src_indicstr12_devanagari.md` |
| 172 | `CURRENT_AUTHORITY` | `resources/sources/src_konvid1k.md` |
| 173 | `CURRENT_AUTHORITY` | `resources/sources/src_lsvq.md` |
| 174 | `CURRENT_AUTHORITY` | `resources/sources/src_pitt_ads.md` |
| 175 | `CURRENT_AUTHORITY` | `resources/sources/src_pvp.md` |
| 176 | `CURRENT_AUTHORITY` | `resources/sources/src_videofeedback.md` |
| 177 | `CURRENT_AUTHORITY` | `resources/sources/src_videogen_rewardbench.md` |
| 178 | `CURRENT_AUTHORITY` | `resources/sources/src_youtube_ugc.md` |
| 179 | `HISTORICAL` | `resources/tasks/RES-001-CONTROLLER-BRIEF.md` |
| 180 | `HISTORICAL` | `resources/tasks/RES-001.md` |
| 181 | `HISTORICAL` | `resources/tasks/RES-002-CONTROLLER-BRIEF.md` |
| 182 | `HISTORICAL` | `resources/tasks/RES-002.md` |
| 183 | `CURRENT_AUTHORITY` | `shared/AUTONOMY-POLICY.md` |
| 184 | `CURRENT_AUTHORITY` | `shared/COMMUNICATION-STANDARD.md` |
| 185 | `SUPPORTING_CURRENT` | `shared/templates/CONTROLLER-BRIEF-TEMPLATE.md` |
| 186 | `SUPPORTING_CURRENT` | `shared/templates/EXPERIMENT-RUN-TEMPLATE.md` |
| 187 | `SUPPORTING_CURRENT` | `shared/templates/HANDOFF-TEMPLATE.md` |
| 188 | `SUPPORTING_CURRENT` | `shared/templates/TASK-TEMPLATE.md` |
