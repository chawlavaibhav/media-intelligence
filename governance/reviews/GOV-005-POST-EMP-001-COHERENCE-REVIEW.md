# GOV-005 — Post-EMP-001 Repository Coherence Review and Project-Memory Refresh

**Date:** 28 August 2026
**Role:** Repository Governor (`governance/GOVERNOR-CONTRACT.md`)
**Audited `main`:** `0e24d6a1a4acce5e83b90fa7fe198db94a92dec5`
**Previous Governor review:** GOV-004, 26 Aug 2026, against `main` at `74d6b0d`
(`governance/reviews/GOV-004-FINAL-PRE-EXECUTION-REVIEW.md`)
**Range reviewed:** `74d6b0d..0e24d6a` — **188 commits**, **33 new Controller decision records**
(29 of them dated 27 Aug 2026).

**Communication check:** I will explain technical ideas in plain English, including what they mean,
why they matter, and their practical consequence; use minimum sufficient wording without sacrificing
understandability; separate evidence from inference; and never invent facts. I have read
`shared/COMMUNICATION-STANDARD.md`.

---

## Verdict

## **PASS WITH NON-BLOCKING NOTES**

**What that means, exactly.** No repository-coherence defect was found that would corrupt evidence
or that cannot be corrected or routed. Several documents had gone stale — badly enough that a fresh
session reading them would have believed paid execution had never been authorised — and those are
now corrected or routed below.

**What that does not mean.** This verdict says nothing about whether the exact-text qualification
programme is scientifically sound, whether the disqualification of five evaluator configurations was
correctly reasoned, whether the zero-false-pass gate is well chosen, or whether the human-confirmed
composite is the right next architecture. **Those are Eval's and the Controller's judgements and are
outside the Governor's authority** (`GOVERNOR-CONTRACT.md` §0). Nothing in this review may be cited
as scientific endorsement.

**One finding deserves the Controller's direct attention** and is the reason this review is worth
reading past the verdict: **the empirical evidence produced by the first paid tranche is not on
`main`.** See F-1. It is non-blocking only because nothing appears to have been lost or falsified —
but the project's founding invariant is currently not satisfied for its most expensive evidence.

---

## Assignment and scope

The Controller assigned a bounded post-EMP-001 coherence and project-memory refresh covering:

changes since GOV-004; the live EMP-001 qualification history; the EVAL-022 and EVAL-023
integrations; the currently active parallel lanes; the marketplace-demand source addition; stale
`PROJECT-MEMORY.md`; stale `coordination/WORKSTREAM-STATUS.md`; current authority links; the current
actual empirical floor; and stale statements claiming paid execution has not happened or has not
been authorised.

Explicit constraints carried into the work: evidence outranks validators, which outrank Controller
decisions, which outrank project memory; do not adjudicate scientific methodology; do not change
Eval, Canon or Resources domain artifacts; preserve historical claims as historical; update only
Governor-authorized current-state and entry-point material; open no domain task; merge no branch.

**Out of scope, deliberately:** the correctness of any qualification result, threshold or
disposition; the design of the proposed human-confirmed composite; the marketplace research's
methodology or its rights position; and any branch other than this one.

---

## 1. Mechanical checks rerun in this session

**Why this section comes first.** A number that appears only in prose is a claim. Where a figure can
be recomputed from a committed artifact, it was recomputed. Everything here was derived on the
audited `main`, not read from a summary.

| Check | Result | Source of truth |
|---|---|---|
| Canon audit records | **19 records, 0 errors** | `canon/validation/validate_audit_gate_v02.py` |
| Live Canon source directories | **19** | `canon/knowledge/current/` |
| Historical CANON-003 instrument | **16 books · 505 source-knowledge objects · 54 concept systems · 417 ontology terms · 53 concepts · 111 bindings, 0 errors** — unchanged, as intended | `canon/validation/validate_canon003_integrated.py` |
| Capability Registry | **0 rows**; validator `PASS` | `eval/registry/registry-v1.jsonl`, `validate_registry.py` |
| V1 capability contract | **36** | `eval/v1/capability-contract.yaml` |
| V1 Eval bank | **100 items** | `eval/v1/bank/master-bank-v1.jsonl` |
| Authored brief bank | **30 briefs** | `canon/experiments/v1/brief-bank/briefs.jsonl` |
| Latin exact-text pack | **96 items = 48 match + 48 mismatch**; SHA-256 recomputed as `320323ff84dd9c0d3ea3e9110eead1a3b789516de43c5f31c4f414fa022f1fcb`, matching both the committed `.sha256` file and `CONTROL-STATE.md` | `eval/empirical-tranche-1/text_qualification/latin-pack-v1.jsonl` |
| Devanagari validated view | **96 items · 48 distinct base words · 33 hard opportunities**; record status `FROZEN`; reviewer count 1 | `eval/battery/devanagari-exactness/human-validation/human-validation-v1.json` |
| Latin human perceptibility review | **96/96 usable · 48/48 mismatch visible · 96 bound rows**, fingerprint-bound to the pack SHA above | `eval/empirical-tranche-1/text_qualification/perceptibility-mechanical.json` |
| Resources corpus | **34,786 records, all `validation_status: ok` · 34,586 distinct SHA-256 · 5,702,337,356 bytes** | `resources/manifests/corpus-pilot-v0.jsonl` |

**Every figure above matches what `PROJECT-MEMORY.md` and `CONTROL-STATE.md` claim.** No headline
count has drifted.

### What could not be checked mechanically, and why

**Every live EMP-001 qualification number.** False-pass counts, false-fail rates, repeat
consistency, call counts and cumulative spend could not be recomputed, because the artifacts that
produced them are not in the repository. See F-1. In this review they are labelled **Controller
decision on record**, carrying **worker-reported** measurements — never `[repo]`.

---

## 2. What happened since GOV-004, in plain English

At GOV-004 the project had four specification packages awaiting merge and had never spent money on a
model. Since then it merged them, built the execution machinery, obtained an explicit spend approval
from the user, and **ran the first real paid experiment in the project's history**.

The experiment asked one narrow question: **can any available system reliably tell whether the text
drawn in an image is exactly the text that was requested?** Five distinct instrument configurations
were run against the frozen 96-item Devanagari battery, and **all five failed**, all in the same
way — they silently repaired corrupted words instead of reading what was actually drawn.

That failure mode is the expensive one. A checker that quietly corrects a misspelling reports a
defective image as correct, so a defect ships with a passing grade.

**This is a real empirical result, not an absence of one.** The project still has zero qualified
evaluators — but it now knows something it did not know two days ago about *why*, across two
different technology families, and it paid about USD 1.30 to learn it.

### The qualification history, as the Controller decisions record it

Every row below is **Controller decision on record**, carrying **worker-reported** live measurement.
None of it was independently reproduced in this review.

| Order | Candidate configuration | Devanagari result | Disposition |
|---|---|---|---|
| 1 | Anthropic `claude-haiku-4-5-20251001` | 576 calls; 43 false passes; 118 false fails; match false-fail rate 0.4097; repeat consistency 0.9271 | Disqualified (pooled v1 gate) |
| 2 | Google `gemini-3.5-flash-lite`, first attempt | stopped at 17 calls on HTTP 429 | **Not a scientific verdict** — ambiguous post-dispatch failure, preserved, not retried |
| 3 | Anthropic `claude-sonnet-5`, corrected | 576 calls; 29 false passes; 6 false fails; match false-fail rate 0.0208; repeat consistency 0.9843 | Triggered the contract-v1 calibration review |
| 4 | Anthropic `claude-sonnet-5` under contract v2 | primary blind transcribe 288 calls; **20 false passes across 7 unique items**; false-fail rate 0.0278; repeat consistency 0.9792 | **Disqualified** |
| 5 | Google `gemini-3.5-flash-lite` under contract v2 (7-second pacing) | primary 288/288; **18 false passes across 7 unique items**; false-fail rate 0.1111; repeat consistency 0.9375; a later diagnostic call hit 429 at dispatch 486/576 | **Disqualified** |
| 6 | Google `gemini-3.5-flash-lite` repeat, no pacing | 576/576, zero errors, zero 429s; primary **16 false passes across 8 unique items**; repeat consistency 0.9167 | **Disqualified**, reinforced by a second complete screen; the pacing requirement was withdrawn |
| 7 | Google Cloud Vision `TEXT_DETECTION`, no language hints | 288/288; **18 false passes across 6 unique items**; false-fail rate 0.0208; repeat consistency **1.0**; zero infrastructure failures | **Disqualified** — best operational stability tested, still fails the safety gate |
| 8 | Tesseract 5.5.3 `hin+eng`, all six lexical dictionaries disabled (USD 0) | 288/288; **3 false passes across 1 unique item**; match false-fail rate **0.6667**; repeat consistency 1.0 | **Disqualified** |
| 9 | Tesseract `hin` script-routed leg (USD 0) | 3 false passes / 1 unique; false-fail rate 0.6042; consistency 1.0 | **Disqualified** |
| 10 | Tesseract `eng` script-routed leg (USD 0) | 12 false passes / 4 unique; false-fail rate 0.5000; consistency 1.0 | **Disqualified** |

**The mechanism the Controller recorded**, stated plainly: modern text recognisers — both
general-purpose vision-language models and purpose-built OCR — use language and dictionary priors
that repair broken words. Turning those priors off (the Tesseract legs) removed most of the silent
repair, but left the recogniser too inaccurate on ordinary correct text to be usable: it started
failing valid words instead. Routing by script removed wrong-script mistakes but did not reduce the
false passes.

**Consequence.** Single-configuration OCR search is closed. The next direction is a fail-closed
composite in which an automated stage can only *reject*, and anything it would pass must be
confirmed by two independent blind human readers. That is **EVAL-028, preparation only** — no human
time and no API call is authorised by it.

**Spend, as recorded:** cumulative EMP-001 paid qualification spend **USD 1.3037905**, against a
USD 6 qualification sub-cap and a USD 10 total ceiling. **Zero image generations have occurred** and
fal spend is USD 0.

---

## 3. The current authorisation picture

`coordination/CONTROL-STATE.md` is authoritative and was found **coherent with the decision records
behind it**. Summarised for navigation only:

**Three lanes are authorised and open.** EVAL-028 (zero-spend preparation of the human-confirmed
composite), EVAL-024 (generate and seal the 16 frozen A-TEXT images, **do not score them**), and
CANON-011 (zero-spend preparation of a marketplace-derived brief and prompt bank).

**Still blocked:** A-TEXT scoring, Registry population, further paid text-judge sweeps without a new
decision, the full 90-generation Stage A, Stages B and C, broad pack acquisition, and any Production
IR or Planner work.

**Lane branch state on the remote**, checked in this session:

| Lane | Branch | State |
|---|---|---|
| EVAL-024 | `origin/work/eval-024-parallel-atext-generation-only` @ `e4e4d39` | 1 commit ahead of `main`, 5 behind. Adds a generation-only orchestrator and tests. **No generation results are committed**, so no image has demonstrably been produced. |
| CANON-011 | `canon/canon-011-marketplace-brief-bank` | Local branch only, not pushed, no commits beyond `main`. **Nothing derived is committed.** Untracked working-tree output was present partway through this review and had been removed by its end — the local clone is shared with at least one active worker session, so working-tree observations here are point-in-time only. Nothing untracked was committed, moved or deleted by the Governor. |
| EVAL-028 | — | Task file merged; no worker branch exists yet. |

---

## 4. The marketplace-demand source addition

**What it is.** Three user-supplied research files were committed under
`canon/research/marketplace-demand-v1/sources/`: a read-only Upwork job-market sweep (11 queries,
114 unique job postings, 4 detail pages), a read-only Fiverr demand and competition sweep (10
listing pages, 42 gig pages), and the raw capture notes behind the Fiverr sweep. A provenance README
records the origin, the evidence hierarchy and the interpretation boundary.

**Why it matters.** This is the first material in the repository that records **what real buyers
actually asked to have made**, rather than what the project authored as a probe. CANON-009 measured
that gap and found the 30-brief bank tests almost none of what real requests most demonstrably ask
for.

**The coherence points worth recording**, all of which the source README states itself and this
review confirms it states:

- Upwork buyer jobs may be used as customer-intent source briefs; **Fiverr seller gigs may not** —
  a seller's package description is not a customer's request.
- Volume and market-size figures in the sweep are **research estimates from one capture**, not
  market-share facts.
- The material is **user-supplied external research**, not repository-derived evidence, and carries
  an explicit no-redistribution-without-rights-review boundary.

**Governor position.** The provenance boundary is stated clearly and correctly, and the derived work
is not yet committed. Whether the derived brief bank honours the boundary is a question for the
Controller's CANON-011 review, **not for this review** — the Governor does not adjudicate whether a
derivation is methodologically sound.

---

## 5. Findings

Severity is judged by **what a zero-context session would wrongly believe** — not by how untidy a
file looks.

### F-1 — The first paid tranche's evidence is not in the repository · **High** · Eval + Controller · **routed, unresolved**

**What I found.** `eval/runs/` is git-ignored. No per-trial outcome record, no spend ledger, no
`qualification-result.json` and no run manifest from any live EMP-001 execution is committed to
`main`. I searched the tracked tree for the reported cumulative-spend values and every hit was
either Controller decision prose or a task file quoting it.

**Why it matters.** The project's founding invariant — stated in `GOVERNOR-CONTRACT.md` §1 and in
`PROJECT-MEMORY.md` — is that a fresh competent agent with no conversation history can reconstruct
authoritative project state from GitHub **by reading the evidence**. For the most expensive evidence
the project has ever produced, it currently cannot. Every qualification number exists only as prose
inside a decision record. Nobody can recompute a false-pass rate, re-derive the cumulative spend,
check a reported figure against the trials that produced it, or re-analyse the false-pass items
under a different question.

The `.gitignore` comment explains the intent — "machine-local runtime state about money;
reconstructed from the ledger on every read and never committed" — and that is a defensible rule for
a *live mutable ledger*. It is a different thing from the **sealed, immutable result of a completed
experiment**, which is exactly what the project's persistence contract exists to preserve.

**Concretely at risk.** The Controller's own EVAL-025 disposition reasons about a specific item,
`dx-0013`, appearing among the false passes of several independent candidates. That
cross-candidate item-level comparison is load-bearing for the decision to stop searching
configurations — and it cannot be reproduced or extended by anyone reading `main`.

**What I did not do.** I did not commit any run artifact, change `.gitignore`, or open a task. All
three are outside Governor authority.

**Routed question for the Controller:** should completed EMP-001 qualification results be sealed
into `main` as immutable evidence, separately from the live ledger?

### F-2 — `eval/HANDOFF.md` still says no model or API call has ever occurred · **High** · Eval · **routed**

**Evidence.** `eval/HANDOFF.md:33` states `**Authorised spend** | **₹0 API/model · ₹0 generation ·
0 Registry entries**` and that "a checker roster and API budget in particular are **not** approved".
Line 131 states "No checker/model/API call has occurred and no checker has been selected."

**The stronger evidence that contradicts it.**
`coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md` records the user's
explicit approval of a USD 10 ceiling, and eight subsequent decision records report completed live
screens totalling **USD 1.3037905** of consumed API spend.

**What a fresh session would wrongly believe.** That EMP-001 is still unfunded and that no evaluator
has ever been tried — which would invite re-proposing exactly the work that has already been done
and paid for.

**Why I did not fix it.** Stream handoffs are stream-owned (`GOVERNOR-CONTRACT.md` §2). The Governor
routes; it does not edit them. The `0 Registry entries` half of the claim remains true and
mechanically verified.

### F-3 — `coordination/WORKSTREAM-STATUS.md` described a state two days and one paid tranche out of date · **High** · Governor · **corrected**

The file opened with "26 Aug 2026 — EMP-001 prepared; explicit spend approval pending" and "**No
paid model/evaluator call is authorised yet.**" Both were false on the audited `main`.

Corrected in this task under the Controller-approved scope, which named this file explicitly. The
correction states current authorisation, the current lanes, the qualification history in one line,
and the empirical floor. **The historical Veo pricing-unit correction and the unapproved
90-generation planning figure were preserved**, because they are still true and still relevant.
GOV-004 corrected this same file for the same reason; F-6 records why that keeps recurring.

### F-4 — Two authorising decisions and two task files exist for EVAL-024, and for CANON-011, with no supersession marker · **Medium** · Controller · **routed**

**Evidence.**

| Lane | Record | Created |
|---|---|---|
| A-TEXT generation-only | `coordination/decisions/CONTROLLER-EMP-001-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md` | commit `540c172` |
| A-TEXT generation-only | `coordination/decisions/CONTROLLER-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md` | commit `1660c74` |
| A-TEXT generation-only | `eval/tasks/EVAL-024-ATEXT-GENERATION-ONLY.md` | commit `0fbc1ae` |
| A-TEXT generation-only | `eval/tasks/EVAL-024-PARALLEL-ATEXT-GENERATION-ONLY.md` | commit `5a3ce50` |
| Marketplace brief bank | `coordination/decisions/CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PROMPT-PREP-2026-08-27.md` | commit `23a7cbb` |
| Marketplace brief bank | `coordination/decisions/CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PREP-2026-08-27.md` | commit `2ab85f7` |
| Marketplace brief bank | `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-PROMPT-BANK.md` | commit `827801a` |
| Marketplace brief bank | `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-BANK.md` | commit `57da7c9` |

The two task files in each pair are **different documents**, cite **different authorising
decisions**, and **neither pair carries a supersession marker**. Neither of the two later decisions
mentions the earlier one.

**What a fresh session would wrongly believe.** It would pick one file, follow it, and have no way
to know the other exists or which governs. For EVAL-024 that matters more than usual, because the
lane spends real money against the EMP-001 ceiling.

**Why I did not fix it.** Deciding which authorisation governs is a **Controller decision**, not a
Governor determination, and the task files are stream-owned. The Governor may place a supersession
marker only for a supersession the Controller has actually made. Recorded here and in
`PROJECT-MEMORY.md` as an open ambiguity.

### F-5 — The decision index stops at 26 August and misses 32 Controller decision records · **Medium** · Controller · **coverage notice added by Governor; full re-index routed**

`coordination/DECISION-LOG.md` describes itself as "the index for discovering" durable Controller
decisions, and `PROJECT-MEMORY.md` §10 points at it for "What has the Controller actually decided?".
Its index ends at the 26 Aug pre-execution closure. I checked every file under
`coordination/decisions/` against the index: **32 of the 42 decision records are not referenced by
it** — 29 dated 27 Aug 2026, plus three from 26 Aug (`CONTROLLER-EVAL-012-REVIEW`,
`CONTROLLER-FIRST-EMPIRICAL-TRANCHE-PREPARATION`, `CONTROLLER-VEO-PRICING-UNIT-CORRECTION`).
Every decision that authorised spending money, switched the judge roster, disqualified a candidate
or opened a current lane is **absent from it**.

**What a fresh session would wrongly believe.** That the last decision the Controller made was to
close the pre-execution freeze — the exact belief that produced F-2 and F-3.

**What I did.** Added a dated coverage notice stating precisely where the index ends, that 32
unindexed records exist under `coordination/decisions/`, and that `CONTROL-STATE.md` governs current
authorisation. **I did not author index rows**, because summarising a decision into
one line is a characterisation of what was decided, and that is the Controller's to write, not the
Governor's. Full re-indexing is routed.

### F-6 — Frozen v2 contracts still say `NOT IN FORCE` in their own status fields · **Medium** · Eval · **routed**

**Evidence.** `eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml` carries
`status: PROPOSED_FOR_CONTROLLER_FREEZE_NOT_IN_FORCE`. So do `CONDITION-ENVELOPE-CONTRACT.yaml`,
`DEPENDENCY-SCORING-CONTRACT.yaml`, `PRODUCTION-REQUIREMENT-PROFILE-v1.yaml`,
`SCIENTIFIC-WAVE1-MODEL-ROSTER.yaml`, `BENCHMARK-v2-WAVE1.yaml`,
`EVALUATOR-QUALIFICATION-MAP.yaml` and `CAPABILITY-V1-V2-MAPPING.md`.

`coordination/CONTROL-STATE.md` lists Capability Contract v2 (44 = 43 active + 1 dormant), the 13
condition families and the 12 core + 2 reserve slots among the project's **frozen foundations**, on
the authority of `CONTROLLER-PRE-EXECUTION-CLOSURE-2026-08-26.md`.

**Note this was correct when GOV-004 wrote it.** GOV-004 cited these same status fields as evidence
that worker proposals were properly distinguished from Controller decisions. The merge is what made
them stale. **This is not a regression by any worker.**

**Why it is only Medium.** A reader who follows the authority chain reaches `CONTROL-STATE.md` and
gets the right answer. A reader who opens the YAML first gets the wrong one.

**Why I did not fix it.** Two reasons, and the second is the binding one. These are Eval-owned
artifacts; and they are **generated** — `build_capability_v2.py` and `build_wave1.py` emit the
status string, so editing the YAML by hand would be undone by the next regeneration and would
violate the regeneration rule in `GOVERNOR-CONTRACT.md` §2.

### F-7 — `preflight-result.json` is committed containing absolute paths from one machine · **Low** · Eval · **routed**

`eval/empirical-tranche-1/preflight-result.json` on `main` records paths such as
`/Users/…/media-intelligence-worktrees/eval-015/eval/registry/registry-v1.jsonl`. The EVAL-024
branch changes the same lines only to say `eval-024`. The file therefore produces a spurious diff in
every worktree and cannot be reproduced on another machine, which weakens it as evidence that
preflight was green. The **substantive** contents — `empirical_row_count: 0`, the registry file
hash, the fixture counts — are machine-independent and unchanged.

### F-8 — `qualify_ocr.py` has a hand-maintained prior-spend default that has drifted · **Low** · Eval · **routed**

`eval/empirical-tranche-1/text_qualification/qualify_ocr.py:733` defaults `--prior-spend` to
`0.6712415`. Cumulative qualification spend is now `1.3037905`.

**Scope of the consequence, stated precisely because it matters.** I traced the flag: it feeds only
`ocr_budget_projection` behind `--budget-proof`, which prints a planning projection. It does **not**
feed the live budget guard, which reads the persistent ledger. So the drift produces a stale
printed forecast, **not** a wrong spend gate. Reported as Low for that reason — but it is exactly
the hand-maintained-number-drifts-from-derived-number pattern the project has already paid to learn
once (EVAL-009's 12-versus-13 condition families).

### F-9 — The EVAL-024 branch re-serialises a completed human-review artifact · **Low** · Eval · **noted for merge, no action needed**

`origin/work/eval-024-parallel-atext-generation-only` rewrites
`eval/empirical-tranche-1/text_qualification/perceptibility-mechanical.json`. I diffed it against
`main`: **the change is key reordering only — every value is identical**, including
`status: COMPLETE_HUMAN_REVIEW`, `usable_yes: 96`, `mismatch_visible_yes: 48` and the bound pack
SHA-256. No human-review evidence was mutated. Recorded so the Controller can confirm the same at
merge rather than having to re-derive it.

### F-10 — Task-file numbering has gaps, and five completed steps have no task file · **Low** · Controller · **noted only**

EVAL-017 through EVAL-021 were run and dispositioned entirely through Controller decision records
with no file under `eval/tasks/`. EVAL-026 and EVAL-027 are unused identifiers — no file, no
reference anywhere in the tracked tree.

**This is not a defect.** The repository has never required a task file per step, and
`DECISION-LOG.md` explicitly says decisions live in several valid forms. It is recorded so a fresh
session does not waste time hunting for files that were never written, or assume work is missing.

---

## 6. What this review deliberately did not check

Stated explicitly, because an unstated gap reads as a pass.

- **No live evidence was reproduced.** Nothing could be: see F-1.
- **No test suite was run.** The reported counts (366 tests under EVAL-016, 363 under EVAL-015, 436
  under EVAL-022, preflight `PREFLIGHT_GREEN` 8/8) remain **worker-reported** and are labelled that
  way in `PROJECT-MEMORY.md`.
- **No provider price, model identity or route was re-verified.** The 27 Aug verification is the
  Controller's, on the Controller's evidence.
- **No scientific judgement was formed** about any threshold, gate, disqualification or the proposed
  composite architecture.
- **No branch other than this one was merged, rebased or modified**, and the untracked CANON-011
  working-tree output was left exactly as found.
- **The Devanagari battery and Latin pack images were not rebuilt.** Both are git-ignored build
  products; the committed SHA-256 fingerprints were checked where the input is committed, which is
  the strongest check available from a fresh clone.

---

## 7. Current-state documents updated in this task

All four are within Governor write authority (`GOVERNOR-CONTRACT.md` §2) and within the scope the
Controller approved for this task.

| File | Change |
|---|---|
| `PROJECT-MEMORY.md` | Refreshed against `0e24d6a`. Rewrote the current-state, gate, milestone and authority sections; added the EMP-001 qualification history and the corrected empirical floor; corrected every statement claiming paid execution had not been authorised or had not happened; re-pointed authority links that named unmerged branches. Historical claims preserved as historical. |
| `coordination/WORKSTREAM-STATUS.md` | Rewritten to current state (F-3). Historical pricing correction and unapproved planning figures preserved. |
| `governance/README.md` | Corrected the execution-posture paragraph, which said paid empirical execution remains blocked; added GOV-004 and GOV-005 to the task history. |
| `coordination/DECISION-LOG.md` | Added a dated coverage notice recording where the index ends and where the unindexed 27–28 Aug decisions live (F-5). No index rows authored. |

**Nothing else was written.** No Canon, Eval or Resources artifact, no stream `CHARTER.md` or
`HANDOFF.md`, no task file, no `.gitignore`, no domain code, and no generated artifact was
regenerated or committed.

---

## 8. Routing summary

| # | Finding | Severity | Owner | Status |
|---|---|---|---|---|
| F-1 | Live EMP-001 evidence is not on `main` | High | Eval + Controller | routed, unresolved |
| F-2 | `eval/HANDOFF.md` says no API call has ever occurred | High | Eval | routed |
| F-3 | `WORKSTREAM-STATUS.md` two days and one tranche stale | High | Governor | corrected |
| F-4 | Duplicate EVAL-024 and CANON-011 authorities, no supersession | Medium | Controller | routed |
| F-5 | Decision index misses 32 of 42 decision records | Medium | Controller | coverage notice added; re-index routed |
| F-6 | Frozen v2 contracts say `NOT IN FORCE` | Medium | Eval | routed |
| F-7 | `preflight-result.json` holds machine-absolute paths | Low | Eval | routed |
| F-8 | `qualify_ocr.py` prior-spend default has drifted | Low | Eval | routed |
| F-9 | EVAL-024 branch re-serialises the human-review artifact (values identical) | Low | Eval | noted for merge |
| F-10 | Task-file numbering gaps | Low | Controller | noted only |

**No finding blocks any authorised lane.** EVAL-028, EVAL-024 and CANON-011 may continue.

---

## 9. What the Controller may want to decide next

Offered as options, not recommendations promoted into decisions.

1. **F-1 — whether completed qualification results get sealed into `main`.** This is the only
   finding that touches the project's founding invariant, and the cost of deciding it later grows
   with every run.
2. **F-4 — which EVAL-024 and CANON-011 authorisation governs**, so both lanes have one unambiguous
   authority.
3. **F-2 — refreshing `eval/HANDOFF.md`**, which is the first file an Eval worker reads and
   currently tells them the opposite of the truth about spend.
4. **F-5/F-6 — whether to normalise the decision index and re-emit the frozen v2 status fields**, or
   to accept `CONTROL-STATE.md` as the single current-state authority and leave both as they are.

---

**Verdict recorded: PASS WITH NON-BLOCKING NOTES.** This is a claim about repository coherence only.
The Governor merges nothing; this branch returns to the Controller.
