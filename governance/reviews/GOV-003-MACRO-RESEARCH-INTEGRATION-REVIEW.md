# GOV-003 — Macro research integration integrity review

**Task:** `governance/tasks/GOV-003.md`
**Reviewer:** Repository Governor · **Date:** 26 Aug 2026
**Branch:** `work/gov-003-macro-integration-review` · **Not merged**
**Spend:** ₹0. No model, generation or evaluator API call was made. No domain artifact was edited.

## Verdict

> # PASS WITH NON-BLOCKING NOTES

**What this verdict covers.** The three completed macro-research branches, the Controller's joint
integration decision, and the current-state documents that those two could have made stale.

**What this verdict means, and only means.** No repository-coherence defect was found that would
mislead a future zero-context session about live project state, corrupt or overwrite evidence, or
exceed an approved boundary. Seven coherence defects were found and are recorded in §7; each is
either corrected here inside the Governor's own files, or routed to its owner.

**What this verdict does not mean.** It is not a statement that CANON-009's request-space reading,
EVAL-007's capability audit or RES-003's topology proposal are scientifically or technically
correct, that their methods are sound, or that their conclusions would replicate. Those judgements
belong to the owning stream and the Controller, and this review must never be cited as though they
had been made (`governance/GOVERNOR-CONTRACT.md` §0 and §3).

### Merge-safety, per branch

| Branch | Coherence-safe to merge? | Basis |
|---|---|---|
| `work/canon-009-request-space` | **Yes** | Purely additive. No existing file touched. Its one machine-readable measurement reproduces byte-identically from the committed brief bank in this session. |
| `work/eval-007-capability-workflow` | **Yes** | Purely additive. No existing file touched. Both of its scripts were rerun here and reproduce their reported results. |
| `work/res-003-evidence-topology` | **Yes** | One existing file changed — `resources/HANDOFF.md`, which Resources owns. Its full validator suite was rerun here and passes end to end. |

All three merge cleanly into `main` at `2cd29037c713e2fb9c77551ddc40ada7cc62f50b`, individually and
all together. After a simulated three-way merge, every protected baseline artifact is
byte-unchanged and every validator in the repository still passes. **Merging is the Controller's
act, not the Governor's.**

---

## 1. What was reviewed, and against what

**Current `main` audited:** `2cd29037c713e2fb9c77551ddc40ada7cc62f50b`
("controller: assign macro integration integrity review", 26 Aug 2026).

**Common base of the three research branches:** `67b50fbc58309b3fd110b6afbc121256eb13bcea`
("controller: activate cloud macro research program", 26 Aug 2026). Confirmed present in the
repository and confirmed to be the merge base of all three branches.

| Branch | Head SHA | Commits since base | Files added | Files modified |
|---|---|---|---|---|
| `work/canon-009-request-space` | `3ca6e675dbbaa5359d0b67967a536e3c6ce01ead` | 1 | 9 | **0** |
| `work/eval-007-capability-workflow` | `714630419e2cf077189679f5f3e5c04be8b654ec` | 1 | 11 | **0** |
| `work/res-003-evidence-topology` | `2632016895ecd8a460eb4e23b43d8e24287de5ef` | 1 | 21 | **1** (`resources/HANDOFF.md`) |
| `work/eval-008-model-access` | `9e3d0080592403511003d03ae8809d23bdd0ad79` | 3 | 1 | 1 — **see §7 finding N-3** |

**Authoritative disposition used as the reference for what was accepted:**
`coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md`.

**None of the four branches is merged into `main`.** Verified by ancestry check, not by reading a
status line.

---

## 2. The central mechanical result

The strongest single check in this review is also the simplest one.

**Two of the three branches modify no pre-existing file at all, and the third modifies only its own
stream's handoff document.**

This matters because the most damaging thing a research branch can do is quietly change the
baseline it was supposed to be measuring — for example, editing a brief so the bank looks better
covered, or renaming a capability so a gap disappears. If a branch adds files and changes nothing,
that class of failure is impossible rather than merely absent. Here it is impossible for CANON-009
and EVAL-007, and confined to one Resources-owned file for RES-003.

Because that is a fact about the commit contents rather than about the prose, no amount of careful
or careless wording in the deliverables can contradict it.

**Baselines confirmed unchanged, by content hash, on every branch and after a combined merge:**

| Artifact | What it is | Status |
|---|---|---|
| `canon/experiments/v1/brief-bank/briefs.jsonl` and `briefs-source.yaml` | the 30 authored commercial briefs | byte-identical |
| `eval/v1/capability-contract.yaml` and `CAPABILITY-CONTRACT.md` | the 36-capability contract | byte-identical |
| `eval/v1/bank/master-bank-v1.jsonl` and `MEASUREMENT-FANOUT.csv` | the 100-item Eval bank | byte-identical |
| `eval/registry/registry-v1.jsonl` | the empirical Capability Registry | byte-identical, still **0 data rows** |
| `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` | persistence contract v2.1 | byte-identical |
| `resources/manifests/corpus-pilot-v0.jsonl` | the acquired-corpus manifest | byte-identical |

---

## 3. Checks rerun in this session

Under the Governor contract, a result a worker reports stays labelled *agent-reported* until someone
else runs it. Everything in this table was **executed in this session**, so it is no longer merely
reported. Nothing was regenerated and committed; where a generator was run, the working tree was
confirmed clean afterwards (the regeneration rule, `GOVERNOR-CONTRACT.md` §2).

**Where these files live.** The three `*/research/` directories below exist **only on the unmerged
worker branches**. Every command was run with that branch checked out, and the last four rows were
also rerun on a simulated three-way merge of all three branches into `main`. If you are reading this
on `main` before the merge, those paths will not resolve — that is expected, not a broken reference.

| Check | Command | Result |
|---|---|---|
| CANON-009's 30-bank measurement | `canon/research/request-space-v1/audit_30_bank.py` | Regenerates the committed `30-bank-grammar-measurement.json` **byte-identically**; working tree clean |
| EVAL-007's research-output validator | `eval/research/pre-e7-macro/validate_research_outputs.py` | **PASS** — 9/9 deliverables, 10 sources, **36/36 capabilities**, **0 endpoints admitted**, 11 conditions |
| EVAL-007's cost forecast | `eval/research/pre-e7-macro/provisional_forecast.py` | Reproduces; **all nine price cells return `null`**, totals `null`, `authorises_spend: false` |
| RES-003's full suite | `resources/research/pre-e7-macro/validators/run_all_res003.sh` | **exit 0 — ALL RES-003 CHECKS PASSED** |
| — its source-register check | `check_source_register.py` | 13 sources, 11 lineage groups, 6/6 structural checks pass |
| — its corpus rebaseline | `resources/v1/validators/rebaseline_from_manifest.py` | **46 pass / 0 fail / 1 warn** (the warning is a pre-existing item — finding N-5) |
| — its CpAO controls | `run_cpao_controls.sh` | **9/9 as declared**: one fixture computes to 45.25 and eight refuse |
| — inherited v2.1 contract | `resources/v1/validators/run_all.sh` | exit 0, nothing regressed |
| Canon admission gate | `canon/validation/validate_audit_gate_v02.py` | 19 records, **0 errors** — live Canon still 19 |
| Canon historical baseline | `canon/validation/validate_canon003_integrated.py` | still 16 books / 505 / 54 / 417 / 53 / 111, 0 errors — **unchanged, as it must be** |
| Capability contract | `eval/v1/validate_capability_contract.py` | **PASS — 36/36 dimensions, scope unchanged** |
| Registry | `eval/registry/validate_registry.py` | **PASS — schema valid, registry empty** |

**Independent counts derived from the committed artifacts rather than read from prose:** 30 briefs
in the bank; 100 items in the Eval bank; 36 capability dimensions; 19 Canon source directories
matching 19 audit records one-for-one; 0 Registry rows.

**Two prose claims checked directly against the machine-readable contract, because they carry the
weight of EVAL-007's main structural argument:**

- *"13 capabilities at `frame`, 1 at `shot_pair`"* — **confirmed.** Counting the
  `observation_unit` field across all 36 dimensions gives frame 13, sequence 8, whole_asset 7,
  asset_set_over_time 7, shot_pair 1.
- *"22 official provider domains probed, 0 yielding a price"* — **confirmed** from
  `CURRENT-WORKFLOW-INVENTORY-2026-08-26.yaml`: 22 candidate rows, `rows_resolved: 0`,
  `endpoints_admitted: 0`, `api_calls_made: 0`, and a programmatic scan finds **zero non-null price
  or cost fields anywhere in the file**.

**Path resolution.** Every repository path written as a code reference in the 41 new files across
the three branches was checked against that branch's file tree. **Zero unresolved paths.** The
task, plan and decision files the three briefs cite all exist on `main`.

---

## 4. Common checks

### Stream ownership — held

| Branch | Wrote only inside | Verdict |
|---|---|---|
| CANON-009 | `canon/research/request-space-v1/` | inside Canon |
| EVAL-007 | `eval/research/pre-e7-macro/` | inside Eval |
| RES-003 | `resources/research/pre-e7-macro/` plus `resources/HANDOFF.md` | inside Resources |

No branch wrote into another stream's directory, into `coordination/`, or into `governance/`.

### Proposals still read as proposals — held

This is the check that most often fails in practice: a worker's recommendation quietly acquires the
grammar of a decision, and three weeks later someone builds on it believing the Controller approved
it. It did not fail here.

- CANON-009's grammar carries `status: PROPOSED_NOT_APPROVED` in the machine-readable file and
  "STATUS: PROPOSAL. Nothing here is an approved schema" in its header. Its five Creative IR items
  are written as proposals, and the brief says explicitly *"This is an architecture decision and is
  flagged, not made."*
- EVAL-007's benchmark document is titled *"Benchmark v2 proposal (PROPOSED, NOT FROZEN)"*; its
  capability audit opens with *"This task does NOT modify the authoritative capability contract"*
  and states of its six candidate capabilities: *"None is proposed for adoption in this task."*
- RES-003's topology carries `status: PROPOSED_NOT_AUTHORITATIVE` and
  `authoritative_until_controller_integration: v2.1`.

A text scan across all three branches for language that would assert Controller approval, frozen
status or an approved budget returned **no matches**.

### No historical baseline mutated — held

Established two ways: by content hash (§2) and by rerunning the historical instruments (§3). The
CANON-003 validator still reports its frozen 16-book figures, which is the correct outcome — that
instrument is historical and its meaning must not move even though live Canon is 19.

### Worker-reported versus independently verified — corrected where possible

Every mechanical claim in the three briefs that could be rerun from committed files **was** rerun
here (§3). Claims that could not be rerun in this environment remain agent-reported, and the
briefs themselves say so. The largest such category is external: all three workers had outbound web
fetching blocked, all three recorded it, and none upgraded a search result into a verified reading.

### Execution posture — no accidental authorisation anywhere

| Question | Evidence |
|---|---|
| Did any branch freeze a paid model roster? | **No.** `eval/model-access/2026-08-26/` — where EVAL-008's roster is required to live — **does not exist on any branch.** |
| Did any branch admit a provider endpoint or price? | **No.** `endpoints_admitted: 0`; all nine forecast price cells `null`. |
| Did any unqualified instrument become evidence? | **No.** EVAL-007 states *"No instrument is declared qualified by this document"* and *"No instrument is qualified. No threshold is proposed."* |
| Did any benchmark score reach the Registry? | **No.** `registry-v1.jsonl` is byte-identical to base and holds 0 data rows. |
| Was any money spent? | **No.** `api_calls_made: 0`, `spend: 0` in the machine-readable inventory; ₹0 asserted in all three briefs. |

`coordination/CONTROL-STATE.md` on `main` separates the four categories the task asks about
correctly: it states the research is complete, names the decision record as authoritative, says in
terms that the worker branches are **not yet merged**, and keeps a "Still blocked / not authorised"
section listing zero qualified evaluators, zero Registry rows, no approved paid budget and
EVAL-006 paused. Each of those was checked against the underlying artifact and each holds.

---

## 5. Branch-specific checks

### CANON-009 — request space

| Required check | Result |
|---|---|
| 30-brief bank not modified | **Held.** `briefs-source.yaml` and `briefs.jsonl` byte-identical. The brief's own claim *"`briefs-source.yaml` is byte-identical"* is now independently confirmed. |
| Live 19-source Canon not changed | **Held.** 19 directories, 19 audit records, validator reports 19 records / 0 errors. No knowledge or audit file was added, changed or removed. |
| External evidence carries evidence labels | **Held.** The register defines four evidence classes and applies one to every row; the grammar labels each of its 14 components; the brief sorts every claim into source-supported (quantitative or qualitative), inferred, proposed or unknown. |
| Search-only limitation stays visible | **Held, and prominently.** The register's header states once, for every row, that page fetching was blocked and that figures are `search_verified`, not `primary_read`. The brief repeats it under its own heading and adds the memorable rule: *"good enough to plan with and not good enough to spend on."* |
| No silent edit to Creative IR or Normalized Request | **Held.** No spec file exists in the diff. All five IR items are proposals in a research document. |

**Quantified prose agrees with the machine-readable measurement.** Rerunning `audit_30_bank.py`
reproduces the committed JSON exactly, and every number the audit document and the brief assert
matches it: 0 edit briefs, 0 animate briefs, 0 multi-turn, 0 variant-set, 28/30 exact text,
12/30 speech, 18/30 duration specified, 19/30 people present, 13/30 product hero, 10/30 identity
continuity, 9 underspecified, 8 contradictory, 30/30 objective present, 12 static / 18 video.

**The honesty of the finding is worth recording.** The audit does not claim its own gaps are proof
that the bank is wrong. It separates what is measured from what is judged in its first section, and
its "List 4" records the two heaviest-covered requirements — exact text at 93% and speech at 40% —
as scope assumptions with weak or no external support, rather than quietly dropping them. That is
the behaviour the evidence rules are meant to produce.

### EVAL-007 — capability and workflow

| Required check | Result |
|---|---|
| 36-capability contract not silently modified | **Held.** Byte-identical; validator reports 36/36, scope unchanged. |
| 100-item bank not silently modified | **Held.** Byte-identical, 100 lines. |
| No unqualified instrument became evidence | **Held.** Stated explicitly in the deliverable and confirmed by the empty Registry. |
| No benchmark score written into Registry evidence | **Held.** Registry byte-identical, 0 rows. |
| Provider, model and price facts left unresolved rather than guessed | **Held, and mechanically enforced.** The inventory records status `BLOCKED_NO_OFFICIAL_EVIDENCE_OBTAINABLE`, 22 probed, 0 resolved. The forecast prints an explicit `unresolved_price_cells` list of all nine and refuses to produce a total. It is blocked by a named blocker id, `E7B-BLOCK-01`. |
| Proposal language distinct from Controller adoption | **Held.** See §4. |

**One point of nuance the Controller should be aware of, recorded as fact rather than as a
complaint.** The 36-capability contract that everyone — this task included — refers to as
*authoritative* carries `status: PROPOSED_FOR_CONTROLLER_REVIEW` inside its own file. EVAL-007 did
not change that and does not misrepresent it. It is noted here only because the word "authoritative"
and the word "proposed" are both attached to the same artifact, and a future session will meet
both. Routed as finding N-6.

### RES-003 — evidence topology

| Required check | Result |
|---|---|
| Persistence v2.1 remains authoritative in the worker branch | **Held, in three places.** The schema file is byte-identical; the topology proposal declares `authoritative_until_controller_integration: v2.1`; the brief and the recomputation document both say v2.1 remains authoritative. |
| v3 topology not silently installed as authoritative | **Held.** `status: PROPOSED_NOT_AUTHORITATIVE`, and it lives under `resources/research/`, not under `resources/v1/`. |
| One call = one trial intact | **Held.** It is the first entry in the proposal's own `preserved_invariants` list: *"One provider/API/transform CALL = one trial. Local steps and composition create no trials."* The point that could have broken this rule — local deterministic transforms producing artifacts — is handled by giving those steps a recipe and no trial, rather than by inventing a trial. |
| No claim of revalidating unavailable raw media | **Held, carefully.** The rebaseline prints *"SCOPE: committed manifest + registry metadata only. No media file was opened."* and the brief marks the decode result **PREVIOUSLY-COMMITTED**, not re-run. |
| CpAO fixtures, validators and documented behaviour agree | **Held.** Rerun here: the happy-path fixture computes to 45.25 as documented, and all eight negative-control fixtures refuse as declared. 9/9. |
| No historical evidence backfilled with invented context | **Held.** Legacy records are to be marked `legacy_v2_1_no_outcome_context` rather than given provenance they never had — the correct treatment under the project's own supersede-don't-rewrite rule. |

**The handoff edit is in scope and accurate.** `resources/HANDOFF.md` is a Resources-owned file. The
change adds RES-003 as the latest work, demotes the previous entry to "PRIOR WORK" rather than
deleting it, and states inside the new text that **v2.1 remains authoritative** and the branch is
**not merged**. It does not overstate.

**One item deserves the Controller's attention as a matter of practice, not as a defect.** RES-003
reports that its cost engine's first run disagreed with the worker's hand-computed fixture, that the
engine was right and the hand arithmetic wrong, and that the fixture was corrected — recorded
openly rather than quietly fixed. The +13.3% double-counting figure it quantifies (a shared logo
visited twice by a naive walk) is the kind of error that would otherwise make the project's primary
business metric look better than reality.

---

## 6. Fourth lane — EVAL-008, from GitHub evidence only

**Status: assigned and active. No deliverable exists.**

| Question | GitHub evidence |
|---|---|
| Is the task assigned? | Yes. `eval/tasks/EVAL-008-CLOUD-MODEL-ACCESS-RESEARCH.md` is on `main`, and `coordination/CONTROL-STATE.md` lists it as the single active assignment. |
| Has any deliverable been produced? | **No.** The task requires nine files under `eval/model-access/2026-08-26/`. That directory **does not exist on `main`, on `work/eval-008-model-access`, or on any other branch.** **0 of 9 delivered.** |
| Does the branch contain research work? | **No.** Its three commits are all Controller/task-authoring commits. It contains no research output. |
| Is a paid model roster frozen anywhere? | **No.** No roster file exists. No branch names a selected model set. |

**The model-selection-before-sourcing rule is intact in the task text** on both `main` and the
branch: select models independently first, then check Frontier Clouds, then fal, then direct or
other providers, and the Controller Brief must prove sourcing did not drive selection.

**GOV-003 has not frozen, implied or pre-empted any model roster.** This review makes no statement
about which models should be tested.

One divergence between the two copies of the EVAL-008 task file is recorded as finding N-3.

---

## 7. Findings

All seven are non-blocking. Severity follows the contract's test: *what would a future zero-context
session wrongly believe?* — not how untidy the file looks.

| ID | Finding | Severity | Owner | Status |
|---|---|---|---|---|
| N-1 | `coordination/WORKSTREAM-STATUS.md` still describes a total audit freeze with no task open in any stream | **Medium** (High before the memory refresh in this task) | Controller | routed — mitigated |
| N-2 | `coordination/DECISION-LOG.md` indexes none of the six 26 Aug Controller decisions | **Medium** | Controller | routed |
| N-3 | Two different versions of the EVAL-008 task file exist on `main` and on `work/eval-008-model-access` | **Medium** | Controller | routed |
| N-4 | GOV-002 was assigned but never executed; its premise has since been overtaken | **Low** | Governor | **corrected here** |
| N-5 | Pre-existing BSTD 351-vs-364 documentation discrepancy still open | **Low** | Resources | routed — already visible |
| N-6 | The "authoritative" 36-capability contract is internally labelled `PROPOSED_FOR_CONTROLLER_REVIEW` | **Low** | Eval / Controller | routed |
| N-7 | `PROJECT-MEMORY.md` never described the accepted V1 architecture baseline at all | **Medium** | Governor | **corrected here** |

### N-1 — the stale workstream status document · Medium · Controller

**File:** `coordination/WORKSTREAM-STATUS.md`, last updated 25 Aug 2026 by GOV-001.

**What it says.** *"Audit freeze — all new domain work is frozen. No task is open in any stream.
Next work in every stream is Controller-assigned only."* Its Eval row gives the next gate as
*"Approve a checker roster and API budget (order ₹600–2,100, price needs re-verification)"*, and all
three stream rows say current approved work: **none**.

**What the stronger evidence says.** `coordination/CONTROL-STATE.md` on the same `main`, updated
26 Aug, records that four domain tasks were assigned and that three of them have returned; that
EVAL-008 is the current active assignment; and that the historical spend figures are superseded
calculations rather than budgets. The Controller's own decision records
(`CONTROLLER-POST-AUDIT-UNBLOCK-2026-08-25.md` §6 and the 26 Aug records) re-scoped that freeze
twice.

**Why it matters.** A fresh session that reads this file and stops there would believe no domain
work is authorised and that the next Eval step is a small checker-roster budget. Both are false.

**Why it is not blocking, and what closes it.** Three things already stand between that file and a
wrong action, and this task adds the third:

1. The file's own third line says **"Read `PROJECT-MEMORY.md` first."**
2. `CONTROL-STATE.md` states that where older wording conflicts, the decision records and that file
   govern.
3. `PROJECT-MEMORY.md` is corrected in this task and now marks this file as stale **at the point in
   the authority map where a reader would go looking for it.**

That makes the misleading path closed for anyone following the documented bootstrap, which is why
the severity is Medium rather than High. It is a mitigation, not a repair.

**Why the Governor did not simply fix it.** Writing factual current-state corrections into
`coordination/**` requires an approved governance task that includes that scope
(`GOVERNOR-CONTRACT.md` §2). GOV-003 grants Governor-owned status documentation and a
`PROJECT-MEMORY.md` refresh; it does not grant `coordination/**` write scope. **The Governor asks
the Controller either to refresh that file or to grant the scope in a future governance task.**

### N-2 — the decision index does not index the current decisions · Medium · Controller

**File:** `coordination/DECISION-LOG.md`, last updated 25 Aug 2026.

**What is missing.** Six Controller decision records exist under `coordination/decisions/`. The
index links **one** of them. Not indexed:

- `CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md` — **the decision this whole review is
  measured against**
- `CONTROLLER-CLOUD-MACRO-RECALIBRATION-2026-08-26.md`
- `CONTROLLER-PAUSE-EVAL-006-PENDING-MASTER-PLAN-2026-08-26.md`
- `CONTROLLER-PRE-E7-SCOPE-REBASE-2026-08-26.md`
- `CONTROLLER-THREE-STREAM-OVERNIGHT-PROGRAM-2026-08-26.md`
- `CONTROLLER-V1-OVERNIGHT-INTEGRATION-2026-08-26.md`

**Why it matters.** `PROJECT-MEMORY.md` tells every reader that this file *"is the index for
discovering"* Controller decisions. A reader who trusts that instruction will not find the decision
that currently governs the project. The index is not wrong about anything it contains; it is
incomplete about the period that matters most.

**The one part that could have been worse, and is not.** The index's last entry authorises EVAL-006
with a ₹16,000 API cap. That authority was withdrawn on 26 Aug. But the entry links to
`eval/tasks/EVAL-006.md`, and that file's first line is **"PAUSED — DO NOT EXECUTE"**. Under the
contract's severity test this is self-correcting on contact with the underlying artifact, so it is
Low on its own; the missing index rows are what make the finding Medium.

**Routed to the Controller.** The index is a `coordination/**` file and is outside this task's
Governor write scope. `PROJECT-MEMORY.md` now names the decisions directory alongside the index so
a reader has a second route.

### N-3 — two versions of the EVAL-008 task file · Medium · Controller

**Evidence.** `main` and `work/eval-008-model-access` diverged at commit `7508ded`. The same
intended edit was then committed twice, 38 seconds apart:

| Ref | Commit | Time | Anti-bias requirement reads |
|---|---|---|---|
| `main` | `db13e4e` | 13:35:19 | "**timestamp/order or** artifact structure showing `MODEL-ROSTER-FIRST.md` was completed before provider-route recommendations" |
| `work/eval-008-model-access` | `9e3d008` | 13:35:57 | "artifact structure showing `MODEL-ROSTER-FIRST.md` was completed before provider-route recommendations" |

**Why it matters, in plain terms.** This clause is the check that stops available credits from
deciding which models the project studies — the task's stated purpose. The branch copy is the later
one and asks for slightly less proof. An EVAL-008 agent working on the branch would follow a
different, weaker requirement than one reading `main`, and neither copy signals that the other
exists.

**A second, larger consequence of the same divergence.** The branch is missing two commits that are
on `main`: the macro-research integration decision and the GOV-003 task. **A zero-context EVAL-008
agent that bootstraps from its own branch would never see the Controller decision that currently
governs the project**, and would read a `CONTROL-STATE.md` that predates the integration.

**Recommended, and for the Controller to do, not the Governor:** bring `work/eval-008-model-access`
up to date with `main`, and decide which wording of the anti-bias clause stands. Neither is a
Governor call — the task file is Eval-owned and the wording is a Controller decision.

### N-4 — GOV-002 was assigned but never run · Low · Governor · **corrected in this task**

**Evidence.** `governance/tasks/GOV-002.md` exists and is written as an assigned task. Its required
deliverable, `governance/reviews/GOV-002-POST-AUDIT-UNBLOCK-REVIEW.md`, **exists on no branch in
the repository.** `PROJECT-MEMORY.md` still carried "Last Governor reset: 25 Aug 2026, task
GOV-001", confirming no GOV-002 refresh ever landed. Separately, `governance/README.md` stated
*"GOV-002 has not been assigned and must not be self-started"* — which the presence of the task file
contradicts.

**Why the task is now unrunnable as written.** GOV-002 asks the Governor to reconcile memory with a
state that says *"the Controller has ... opened EVAL-006"*. EVAL-006 was paused on 26 Aug and its
spend authority withdrawn. Executing GOV-002 literally would now write a false current state into
`PROJECT-MEMORY.md`.

**Corrected here**, inside Governor-owned files only:

- `governance/status/2026-08-26-GOV-002-SUPERSEDED.md` — a supersession note recording that GOV-002
  was never executed, why its premise no longer holds, and that its memory-refresh purpose is
  discharged by GOV-003.
- `governance/README.md` — the false "GOV-002 has not been assigned" line and the stale audit-freeze
  paragraph are corrected, and the new `reviews/` and `status/` directories are listed.

**The GOV-002 task file itself was not edited.** Governor task files are Controller-assigned; the
supersession is recorded alongside it rather than written over it.

### N-7 — the project's entry point never learned about the V1 baseline · Medium · Governor · **corrected in this task**

**What was missing.** Before this task, `PROJECT-MEMORY.md` did not mention the 30-brief bank, the
36-capability contract, the 100-item Eval bank, persistence contract v2.1 or Creative IR v0.1
**anywhere**. A word-level search of the file found no reference to any of them.

**Why that happened.** All four landed on `main` on the evening of 25 Aug, **after** GOV-001 wrote
the memory reset. GOV-002 was assigned to close exactly this kind of gap and never ran (finding
N-4), so the gap persisted for a day across two Controller decisions.

**Why it matters more than it sounds.** These four artifacts are what the macro reset re-examined.
A zero-context agent reading the entry point could not have understood what "the 30-brief bank has
zero edit briefs" or "the current 36 remain the baseline" referred to, because the entry point had
never said the 30 briefs or the 36 capabilities existed. The Controller accepted and merged them in
`coordination/decisions/CONTROLLER-V1-OVERNIGHT-INTEGRATION-2026-08-26.md`, so this was a gap in the
map, not in the evidence.

**Corrected here.** `PROJECT-MEMORY.md` §4 now opens with a compact table of the four artifacts,
what each is in plain terms, where it lives, and the explicit statement that **none of them is
empirical evidence about any model**. Each count in it was verified mechanically in this session.

**Related, and worth the Controller knowing:** the current `coordination/CONTROL-STATE.md` also
dropped the "What remains accepted from V1" inventory that its predecessor at the research base
carried. No harm follows now that memory carries it, and the V1 integration decision remains the
owning record either way.

### N-5 — BSTD 351 vs 364 · Low · Resources · already visible, not introduced here

RES-003's rebaseline emits one warning: the corpus manifest records **364** "other language" BSTD
items where committed prose says **351**, a difference of 13. This is a pre-existing discrepancy,
not something RES-003 created, and RES-003 explicitly declines to silently correct it in either
direction because resolving it needs raw annotation files that no cloud session can reach. **That is
the correct behaviour** and the finding is recorded here only so it stays visible after merge. It
does not affect any headline corpus figure — item count, distinct hashes, duplicates and total bytes
all reconcile exactly.

### N-6 — "authoritative" versus "proposed" on the capability contract · Low · Eval / Controller

`eval/v1/capability-contract.yaml` carries `status: PROPOSED_FOR_CONTROLLER_REVIEW` while
`CONTROL-STATE.md`, the Controller decision and GOV-003's own task text all treat the 36 as the
**baseline** the v2 work starts from. Both readings are defensible — it is a baseline in practice
and a proposal by its own label — and no document misstates the other. It is recorded so that the
v2 specification work resolves the label rather than inheriting the ambiguity.

**An adjacent note for whoever merges.** After merge the repository will hold two session-scoped
readings of the same external source: CANON-009 records Arena-T2I-Hard as **unresolved** ("search
did not return a first-party page ... in this session"), while EVAL-007 describes it as 310 real
arena prompts with a dependency-aware checklist and RES-003 registers it as sharing the LMArena
lineage. Neither is a false claim — CANON-009 is honest that its statement is about its own
session's reach — and the Controller decision, which independently verified the 310-prompt figure,
governs. No action is required; it is flagged so nobody later reads the Canon row as the project's
current position.

---

## 8. What this review did not check

Stated plainly, because a review's silence is otherwise read as approval.

- **Whether any domain method is correct.** Not the Governor's judgement to make. This review does
  not evaluate whether the request grammar is the right grammar, whether the proposed capability
  splits are the right splits, or whether the outcome topology is the right shape.
- **Any external claim.** Every figure drawn from outside the repository — PSR's 82,976, TIP-I2V's
  1.70M, VBench-2.0's dimensions, the licence status of any dataset — was checked only for
  **internal consistency and honest labelling**. None was verified against its primary source here.
  All three workers had web fetching blocked and said so; the Controller decision records a separate
  independent verification pass, and that is the Controller's evidence, not the Governor's.
- **Anything requiring the raw corpus.** The 5.70 GB media corpus is git-ignored and absent. No
  media file was opened. Decode results remain previously-committed observations.
- **The domain content of files this review did not need to open.** The review was bounded to the
  three branches, the integration decision, and the current-state documents they could have made
  stale — not a full repository audit. The next periodic health audit is due under
  `GOVERNOR-CONTRACT.md` §4.

---

## 9. Project memory

`PROJECT-MEMORY.md` **was updated** in this task. It was materially stale: it described a total
audit freeze, no open task in any stream, and a next Eval gate of a ₹600–2,100 checker roster —
all superseded by the 25 and 26 August Controller decisions.

The update is narrow and keeps the document a bootstrap rather than a transcript — it is organised
by state and decision, not by task sequence. It adds: the V1 architecture baseline (finding N-7),
why the macro reset happened, the fact that the three programmes completed and are **awaiting merge
as of this review**, the Controller-adopted integration direction, EVAL-008's status as observed on
GitHub, and a rewritten current-gate section replacing the superseded audit-freeze text. It marks
`coordination/WORKSTREAM-STATUS.md` and `coordination/DECISION-LOG.md` as stale **at the point in the
authority map where a reader would otherwise trust them**, and points at `coordination/decisions/`
as the working route to Controller decisions.

To keep the context cost from growing, the Eval stream narrative and the external-research section
were compressed — meaning and links preserved, repetition removed — as the contract's maintenance
rule requires. Net growth is about 200 lines, all of it current state that the document did not
previously carry.

**A note on how it should be read after a merge.** The memory's stream sections say the three
branches were unmerged **as of 26 Aug 2026 at `main` `2cd29037`**. If the Controller merges them,
that sentence becomes historical and the Governor should refresh it. It is written with the SHA
attached so the staleness is self-evident rather than silent.

---

## 10. Deliverables of this task

| File | What it is |
|---|---|
| `governance/reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` | this review |
| `governance/status/2026-08-26-GOV-002-SUPERSEDED.md` | Governor-owned supersession note for GOV-002 |
| `governance/README.md` | corrected: stale freeze paragraph, false GOV-002 line, missing directories |
| `PROJECT-MEMORY.md` | narrow current-state refresh |

**Nothing outside `PROJECT-MEMORY.md` and `governance/**` was written.** No domain artifact was
edited. No generator output was committed. No task was opened. Nothing was merged.
