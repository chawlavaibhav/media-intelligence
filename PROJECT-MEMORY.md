# Project Memory

**The canonical entry point for this project.** Read this first, every session, before anything else.

**Maintained by:** the Repository Governor (see `governance/GOVERNOR-CONTRACT.md`).
**Last Governor reset:** 25 Aug 2026, task GOV-001, against `main` at `00ea9b067229cd992b77b7d6e0958df35178b01b`.

This document is a curated synthesis, not a diary. It tells you what is true now and points to the
committed evidence that proves it. Where it disagrees with the underlying artifact, **the artifact
wins and the disagreement is a governance defect** — report it.

**Provenance labels used below.** `[repo]` = mechanically verified from committed files during
GOV-001. `[decision]` = a Controller decision record exists in the repository. `[agent-reported]` =
a worker reported it and GOV-001 did not independently rerun it. `[external]` = external research
snapshot, not repository truth. `[unresolved]` = not established.

---

## 1. What this project is

An **API-native media production intelligence layer**. It is not a new foundation model. It sits
between what a customer asks for and the ecosystem of image/video/audio generation tools, and
continuously chooses the cheapest reliable path to a commercially acceptable result.

The long-term primary metric is **Cost per Accepted Outcome** — what it costs to reach an output a
customer will actually use — not cost per generation. A model that is cheap per image but needs six
retries is not cheap.

Full statement: `coordination/PROJECT-CONTRACT.md`.

## 2. How the work is divided

Three domain streams produce evidence, plus two control roles.

| Role | Owns | Explicitly does not own |
|---|---|---|
| **Canon** | Durable creative/production knowledge: what a good outcome must achieve, what techniques exist, what to inspect to judge fitness. | Which model is best today, prices, provider quirks. |
| **Eval / Capability Lab** | What to measure and how, then measuring it empirically. Produces the Capability Registry. | Inventing creative quality from first principles — Canon supplies the dimensions. |
| **Resources** | Independent media/data for testing: discovery, licensing, sampling, manifests, integrity. | Defining Canon truth; choosing examples that flatter a hypothesis. |
| **Controller** (human) | Product direction, architecture, task authorization, accept/reject, merges. | — |
| **Repository Governor** | Repository coherence, this document, integrity review, audits. | Project strategy; domain methodology. |

Charters: `canon/CHARTER.md`, `eval/CHARTER.md`, `resources/CHARTER.md`.
Governor role: `governance/GOVERNOR-CONTRACT.md`, approved design in
`docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md`.

## 3. Frozen decisions that constrain current work

These are not reopened without an approved integration task. Full list: `coordination/PROJECT-CONTRACT.md`
("Major separations"). The ones that most often trip up a new session:

1. **Creative IR ("what should exist") is separate from Production IR ("how today's tools make it").**
   Production IR **does not exist yet**. `[repo]`
2. **Book knowledge is never evidence about model capability.** The Capability Registry is empirical
   only, and **does not exist yet**. `[repo]`
3. **Public dataset labels are one source's observations, not our ground truth.** `[decision]`
4. **A worker's recommendation is not an approved decision.** Only a Controller-written task file or
   decision record makes something approved.
5. **Historical baselines are never rewritten to match current numbers.** Superseding is allowed;
   silent mutation is not.

## 4. Current state by stream

### Canon — 19 live accepted sources; historical CANON-003 baseline frozen at 16

Two numbers exist and must not be confused. `[repo]`

| Number | Value | Meaning |
|---|---|---|
| Historical CANON-003 / CANON-004 method-test corpus | **16** | Fixed forever. The frozen set the extraction batch closed on and the Audit Gate was tested against. |
| **Live accepted Canon** | **19** | What the Canon actually holds today. |

Verified mechanically by GOV-001: `canon/knowledge/current/` holds exactly 19 source directories,
`canon/audit/records/` holds exactly 19 audit records, and the two sets match one-for-one with no
orphans on either side. `canon/validation/validate_audit_gate_v02.py` reports 19 records and 0
errors. The historical instrument `canon/validation/validate_canon003_integrated.py` still reports
16 books / 505 source-knowledge objects / 54 concept systems / 417 ontology terms / 53 concepts /
111 bindings, 0 errors — unchanged, as intended.

**Admission method: Post-Extraction Audit Gate v0.2**, authoritative since CANON-005. `[decision]`
It asks five questions per source after extraction — representation integrity, evidence origin,
application fit, pairwise source lineage, technology contingency — and `evidence_insufficient` is a
legitimate completed outcome, not a failure. Normative text: `canon/audit/AUDIT-GATE-v0.2.md`.
Decision: `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`.

**The gate governs use, not storage.** An unaudited or stale-audited source stays in the repository
as evidence but may not be used for cross-source promotion, downstream product use, or
Canon-consumption/retrieval.

How the Canon got from 16 to 19:
- **CANON-006** admitted the two deferred reserve sources, *Master Shots* (Kenworthy) and
  *The Conversations* (Ondaatje). 16 → 18. It also added the lineage relation
  `shared_primary_informant`, because *The Conversations* is substantially Walter Murch speaking and
  the corpus already held Murch's own *In the Blink of an Eye* — different author, publisher and
  year, same intellectual origin. The relation is **pairwise and symmetric**, and incidental
  quotation of the same person does not qualify. `[repo]` `[decision]`
- **CANON-007** admitted *Effectiveness in Context* (Binet & Field). 18 → 19. It added the
  representation-loss category `figure_semantic_binding_lost`, for material where a chart's text and
  numbers survive extraction but which number belongs to which category does not. `[repo]`
- **CANON-008 STOPPED at its acquisition gate and ingested nothing.** The official D'source/IDC
  record for Girish Dalvi's *Conceptual Model for Devanagari Typefaces* publishes only a 3-page
  abstract; the full thesis sits behind IIT Bombay authentication, which was not attempted. **This
  is the gate working, not a failure.** Live Canon stays 19. `[repo]`
  Brief: `canon/findings/CANON-008-CONTROLLER-BRIEF.md`.

**The Canon still has no accepted Devanagari-structure source.** *Thinking with Type* remains
blocked on structural column interleaving and is not in the 19.

Stream detail: `canon/HANDOFF.md`.

### Eval — battery built and human-validated; no checker has ever been run

**Nothing in this stream currently licenses trusting any evaluator's numbers.** No checker has been
qualified, no model benchmarked, no Capability Registry entry created, ₹0 API/generation spend. `[repo]`

**EVAL-005 is the live artifact: a Devanagari exactness battery.** It asks the question that costs
money — we ask a generator for a specific string, it produces something *subtly* wrong, and the
checker says "matches", shipping a defect with a passing grade. The battery removes the annotator
entirely by rendering its own images from strings we chose, so what each picture contains is known
by construction.

Two views exist and must not be confused: `[repo]`

| View | Contents | Status |
|---|---|---|
| Original build | 106 items — 53 match / 53 mismatch, 53 base words | **Historical source material.** What the reviewer actually saw. Unchanged. |
| **Validated view** | **96 items — 48 match / 48 mismatch, 48 accepted base words, 33 hard opportunities on 33 distinct base words, 20 failure classes / 5 groups** | **Authoritative for any checker run.** |

**Human validation is complete and the Controller chose PRUNE, DO NOT REBUILD.** `[decision]`
One Hindi-competent reviewer answered 98 of 98 questions, 0 unanswered, 0 unsure. Five of 53 base
words were rejected, excluding 10 items, which were **not replaced** — preserving the identity of
items already reviewed rather than opening a new human-validation surface.

GOV-001 verified this record mechanically: `human-validation/human-validation-v1.json` carries
status `FROZEN`, the 10 excluded item IDs, the expected validated state, and SHA-256 hashes for both
raw response artifacts — **both hashes recomputed and matched**.

**One reader is not independent-reader ground truth.** The record says so itself: it is
"PROVENANCE, NOT GROUND TRUTH", and no threshold, rate or checker claim may be derived from it.
Two items flagged in both the word and rendering questions are *within-reader* consistency, not a
second reader.

**Statistical honesty is a hard-won rule here.** The qualification gate is deterministic — **zero
false passes** — and needs no probability model. The 8.68% figure attached to the validated view is
a `iid_reference_upper_bound_…` sizing calculation under an assumption the battery explicitly does
**not** establish (`independence_status: NOT ESTABLISHED`). It is never a checker's real error rate.

**EVAL-004 was stopped by the Controller, not completed.** `[decision]` One 54-item Reader-A pass
exists; a second person looked informally but did not perform the frozen blind protocol, so there is
**no Reader B and no two-reader reference**. Reader A is exploratory evidence only; no checker may be
qualified, ranked or entered in the Registry from it, and it must not be resumed.
`eval/decisions/EVAL-004-STOP-2026-08-24.md`.

**EVAL-003 remains closed and merged** — a 54-item Hindi-primary photographed-signage calibration
pack (173 eligible → 54 selected → 54 distinct hashes), untouched and available if that screen is
ever wanted.

**The founding result of the stream:** a capability number without its checker is not a measurement.
An early calibration study gave 14 Hindi images to three checkers; one AI vision model returned
**6 false passes** — it looked at visibly misspelled signs and called them correct. That study is
explicitly preliminary (14 images but only 4 independent sources; right answers never confirmed by a
first-language reader; each image checked once). `eval/findings/FINDINGS-01-can-we-check.md`.

Stream detail: `eval/HANDOFF.md`.

### Resources — corpus acquired and closed; no open task

**34,786 items / 5.70 GB across 8 acquired sources; 4 blocked.** `[repo]`
GOV-001 recomputed every headline figure directly from `resources/manifests/corpus-pilot-v0.jsonl`:
34,786 records, all `validation_status: ok`, 34,586 distinct SHA-256 hashes, 200 duplicates
(27 within a single source, 173 spanning two sources), 5,702,337,356 bytes. Every per-source count
matches the handoff table exactly.

**The most important Resources finding: two of the three Devanagari sources are not independent of
each other.** IndicSTR12 and IIIT-ILST are both CVIT / IIIT Hyderabad releases sharing 173
byte-identical files — 98.3% of IIIT-ILST's scene photographs. Treat them as **one source lineage**
for any holdout claim. **BSTD is the only genuine cross-lineage reserve and is held untouched.**

Two related traps recorded here, both real: hash-based deduplication cannot see content reuse
(1,205 of 1,214 IIIT-ILST crops derive from shared parent photographs while sharing no bytes), and
"media acquired" is not "usable annotated records" — 4,476 Devanagari images are 551 annotated
photographs plus 3,925 single-word crops, of which 3,924 resolve to a transcription.

**Rights posture: internal research and evaluation only.** If any result is ever published or shown
to a customer, the rights question must be reopened first.

Stream detail: `resources/HANDOFF.md`.

### Architecture objects — what does not exist yet

**Capability Registry, Production IR, the Production Planner, routing, and any Canon-consumption /
RAG / training experiment are unapproved and not implemented.** `[repo]` Do not assume otherwise
from a schema draft or a plan document; drafts exist, implementations do not.

## 5. Current gate — the project is under audit freeze

**All new domain work is frozen pending completion of the governance reset.** `[decision]`
(`governance/bootstrap/CONTROLLER-MIGRATION-SEED.md` §2, and `governance/README.md`.)

Do not start, and do not self-assign: CANON-009 or other Canon expansion; EVAL-006 or any
checker/model/API run; Resources expansion; acquisition work; Capability Registry work; Production
IR work.

**No task is currently open in any domain stream.** The next work in every stream is
Controller-assigned only.

The decisions genuinely waiting on the Controller, in rough order of what each unblocks:

1. **Canon:** what to do about CANON-008 — the Devanagari source slot is still empty and the task is
   stopped at `needs_controller_review`. Four options are set out in
   `canon/findings/CANON-008-CONTROLLER-BRIEF.md`.
2. **Eval:** approve a checker roster and API budget (order of ₹600–2,100 for a first run, on an old
   price that must be re-verified). This is the only thing blocking the first real measurement the
   project has ever taken.
3. **Eval:** approve or reject the proposed thresholds (0.95 repeat consistency, ≤10% false fail,
   ≤5% refusal). These are judgement calls with no empirical backing.
4. **Eval → Resources:** whether to ask Resources to check material it already holds for ~36–42 more
   Hindi words. Optional; it tightens a reference figure and blocks nothing.
   `eval/tasks/EVAL-005-RESOURCES-REQUEST.md` is a request, not an approved task.
5. **Resources:** whether to action `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`.

## 6. Lessons already paid for — do not rediscover these

- **A validator that aborts a unit on a parse error under-reports, and the shortfall is invisible in
  its own output.** This hid 10 real errors until CANON-004 found them.
- **An audit record is only valid for the exact bytes it audited.** Any change to a source's
  machine-consumed artifacts fails its audit as stale. There is deliberately no refresh shortcut.
- **Different authorship is not independent origin.** Companion volumes and shared informants both
  defeat any independence check built on bibliographic metadata.
- **Bindability is not evidence quality.** The source with the most product bindings has the weakest
  support. Never rank sources by binding count.
- **Test tooling with deliberately broken inputs, not only correct ones.** Negative-control fixtures
  immediately exposed three real defects in the Eval harness, including a run that raised integrity
  errors and still exited successfully. **None was visible from reading the code.**
- **An empty check is not a passing check.** A suite with nothing in it must fail, not report
  success.
- **A statistical bound over correlated items is not a bound**, and de-correlating items does not
  make them independent. Count opportunities, not items — and say `independence_status: NOT
  ESTABLISHED` out loud.
- **Descriptions can be wrong for months while every integrity check passes.** Hash and decode checks
  prove files are intact; they prove nothing about whether the prose describes them.
- **Do not infer media rights from a code licence.** A repository's MIT licence says nothing about
  the dataset it ships.

## 7. Known limitations and unresolved questions

- **The Canon has no accepted Devanagari-structure source.** `[repo]`
- **No checker is qualified; the project has taken no empirical capability measurement.** `[repo]`
- **The EVAL-005 battery is not reproducible from GitHub alone.** Its built items live under a
  git-ignored `build/` directory and the pinned font is a proprietary system asset that is not
  committed (provenance is recorded instead). The committed record fingerprints the build by SHA-256
  so a rebuild can be checked, but a fresh clone on a machine without that font cannot reconstruct
  it. `[repo]`
- **The Resources composition verifier cannot run from a fresh clone** — it reads the git-ignored raw
  corpus. `[repo]`
- **Whether the Devanagari transcriptions survive checking by a Hindi reader is untested.** `[unresolved]`
- **CANON-001 and CANON-002 outputs are not on `main`.** Their briefs, findings and two extracted
  knowledge directories exist only on unmerged branches, although `canon/tasks/CANON-003.md` cites
  them as evidence. Routed to Canon/Controller by GOV-001. `[repo]`
- **The EVAL-004 Reader-A freeze and attestation are not on `main`** — only on `work/eval-004`,
  although the merged stop decision refers to retaining that evidence. Routed to Eval/Controller. `[repo]`
- **How a Registry entry should lose confidence as it ages has deliberately not been decided.**
  Inventing a decay formula now would encode a guess as a finding. `[unresolved]`

## 8. External research — context, not authority

Source-discovery and acquisition work was performed outside GitHub. It is an **external research
snapshot** and never competes with repository truth.

GOV-001 inspected two of the four named artifacts, both dated 24 Aug 2026, in the operator's local
Downloads folder: `creative_production_canon_expansion_report (1).docx` and
`creative_production_canon_candidate_universe (1).xlsx`. `[external]`

**Both are now contradicted by the repository on their central arithmetic.** They state "Current live
Canon on main: 16" and that *Master Shots* and *The Conversations* are "absent from main and not
Controller-accepted live". CANON-006 admitted both on 25 Aug and live Canon is 19. The workbook
anticipated exactly this and recorded the rule — raise the live baseline when a deferred branch is
accepted — but was never updated. **Its 22-source portfolio and its projected total of 38 rest on
the stale base of 16 and must be recomputed before use.**

Two further reconciliations: *Effectiveness in Context*, listed there as Wave 1 candidate 5, **has
since been ingested** as CANON-007 and is no longer a candidate. Wave 1 candidate 7 was still the
superseded "Devanagari Type Design" identity; that slot was redirected to the Dalvi thesis, which
CANON-008 then stopped on.

`WAVE-1-ACQUISITION-REPORT.md` and `ACQUISITION-MANIFEST.xlsx` were **not found and were not
inspected**. Any claim resting on them is unverified. `[unresolved]`

**One qualitative experiment is recorded for completeness and is not a benchmark.** A small informal
comparison of advertising concepts, one arm using Canon-derived principles and one not, was judged by
the operator to favour the Canon arm. It is anecdotal, was run outside the Eval system, and licenses
no capability claim and no Registry entry. `[external]`

## 9. Milestones

| Date | Milestone | Evidence |
|---|---|---|
| 23 Aug 2026 | SPEC-02's single-atom schema split into source knowledge / bindings / ontology; Canon scope restored after a category-error finding | `coordination/DECISION-LOG.md` |
| 24 Aug 2026 | Three workstreams started; RES-001/002 corpus acquired and closed | `resources/tasks/`, PR #2 |
| 24 Aug 2026 | CANON-003 extraction stopped at 16 accepted books, then integrated | `canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md`, PR #4 |
| 24 Aug 2026 | EVAL-003 calibration pack merged; EVAL-004 stopped after Reader A | PR #3, `eval/decisions/EVAL-004-STOP-2026-08-24.md` |
| 25 Aug 2026 | Audit Gate v0.2 designed, adopted and made authoritative | `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`, PRs #6/#7 |
| 25 Aug 2026 | CANON-006/007 take live Canon 16 → 18 → 19 | PRs #9, #10 |
| 25 Aug 2026 | EVAL-005 human validation frozen; battery pruned to the 96-item view | PR #12 |
| 25 Aug 2026 | CANON-008 stopped at the acquisition gate | PR #13 |
| 25 Aug 2026 | Repository Governor approved; GOV-001 reset audit | PR #14, `governance/audits/2026-08-25-initial-repository-hygiene-audit.md` |

## 10. Authority map — which file proves what

| Question | Authoritative file |
|---|---|
| What is the product and what are the frozen separations? | `coordination/PROJECT-CONTRACT.md` |
| How must every worker communicate? | `shared/COMMUNICATION-STANDARD.md` |
| What is live in each stream right now? | `coordination/CONTROL-STATE.md`, then this document |
| Per-stream status and next gate | `coordination/WORKSTREAM-STATUS.md` |
| How do I start a session, approve a task, escalate? | `coordination/RUNBOOK.md` |
| When may a worker run unattended? | `shared/AUTONOMY-POLICY.md` |
| What has the Controller actually decided? | `coordination/DECISION-LOG.md` and the stream decision records it indexes |
| What is believed but untested? | `coordination/ASSUMPTIONS.md` |
| How is a Canon source admitted? | `canon/audit/AUDIT-GATE-v0.2.md` |
| Which Canon sources are live? | `canon/audit/records/` + `canon/knowledge/current/` (one record per directory) |
| What is the authoritative Eval battery? | `eval/battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md` and `human-validation-v1.json` |
| What media do we hold? | `resources/manifests/corpus-pilot-v0.jsonl` and `source-registry-v0.csv` |
| What does the Governor do? | `governance/GOVERNOR-CONTRACT.md` |
| What did the first repository audit find? | `governance/audits/2026-08-25-initial-repository-hygiene-audit.md` |

## 11. How to start a session

**Every role:** this document → `coordination/PROJECT-CONTRACT.md` → `shared/COMMUNICATION-STANDARD.md`.

Then:
- **Controller:** `coordination/CONTROL-STATE.md`, then the decision records it links.
- **Worker:** your stream `CHARTER.md` → your stream `HANDOFF.md` → your assigned task file → only
  the sources that task names. Do not replay full project history.
- **Governor:** `governance/GOVERNOR-CONTRACT.md` → current `main` → the task/PR under review.

**A session may persist for convenience, but no important project fact may depend on it.** If you
learn something that matters, it belongs in GitHub before the session ends.
