# Project Memory

**The canonical entry point for this project — a compact map to authority, not the authority
itself.** Read this first, every session; then `coordination/CONTROL-STATE.md` for what is currently
authorised.

**Maintained by:** the Repository Governor (`governance/GOVERNOR-CONTRACT.md`).
**Last refresh:** 1 Sep 2026 — REP-07 admission batch, EVAL-038 and CANON-SHAPE-v1 refresh. The
last full Governor reconciliation remains **GOV-006** against `main` at `91984f5`
(`governance/reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`, PASS WITH NON-BLOCKING NOTES);
CANON-014 received a bounded Level-1 review at
`governance/reviews/GOV-L1-CANON-014-FULL-CORPUS.md`. The text immediately before this refresh is
preserved byte-for-byte at `history/PROJECT-MEMORY-PRE-EVAL-038-REFRESH-2026-09-01.md`, and the
full pre-migration text at
`history/PROJECT-MEMORY-PRE-CONTEXT-MIGRATION-2026-08-28.md`; detailed narrative now lives under
`history/` (see §8).

## 1. What this project is

An **API-native media production intelligence layer**. Not a new foundation model: it sits between
what a customer asks for and the ecosystem of image/video/audio generation tools, and continuously
chooses the cheapest reliable path to a commercially acceptable result.

The long-term primary metric is **Cost per Accepted Outcome (CpAO)** — what it costs to reach an
output a customer will actually use, fully loaded (failed/refused calls, retries, evaluator calls,
repairs, required human review, rejected revisions in the same journey), not cost per generation. A
model that is cheap per image but needs six retries is not cheap. Full statement:
`coordination/PROJECT-CONTRACT.md`.

**The architectural flow:** customer input → Normalized Request → creative intelligence + Canon →
Creative IR → production planning/routing (consulting the Capability Registry) → generation tools →
evaluation → repair → accepted outcome → empirical memory.

**What exists vs what does not (verified at GOV-006):** the Normalized Request grammar, Creative IR
v0.1, accepted Canon knowledge, frozen measurement contracts and benchmark harnesses **exist**.
**Production IR, the Production Planner, routing, a request compiler, a repair runtime and any
customer-facing API do not exist.** The Capability Registry exists as a schema and validator with
**zero rows**.

## 2. Where truth comes from — typed authority

Different questions have different authorities. Never substitute one for another.
(Full policy: `shared/CONTEXT-SUFFICIENCY-POLICY.md`.)

| Question | Authority |
|---|---|
| What actually happened? (empirical fact) | **Committed evidence/artifacts** + deterministic validators over them (`verify/VALIDATOR-INDEX.yaml`) |
| What are we allowed to do? What governs? Is work cancelled/authorised? | **Explicit durable Controller decisions** — list `coordination/decisions/` directly; stream decision records also count. `coordination/DECISION-LOG.md` is a curated navigation index only |
| What is open/blocked/deferred right now? | **`coordination/CONTROL-STATE.md`** — the single primary current-state surface |
| What is this project; where is the authority? | **This document** — a map; it establishes nothing on its own |

**If this document conflicts with underlying evidence or decisions, they win and this document is
defective** — report the defect, don't argue from the map. **Newer durable Controller decisions
govern over stale prose**, including task files and handoffs. An empirical artifact never authorises
anything by itself (a 7/16 result cannot create a Registry row; only a Controller decision could,
and the Controller has ruled it does not).

## 3. Roles and stream boundaries

| Role | Owns | Explicitly does not own |
|---|---|---|
| **Canon** | Durable creative/production knowledge: what a good outcome must achieve, techniques, what to inspect. | Which model is best today, prices, provider quirks. |
| **Eval / Capability Lab** | What to measure and how; measuring it empirically; the Capability Registry. | Inventing creative quality from first principles — Canon supplies the dimensions. |
| **Resources** | Independent media/data for testing: discovery, licensing, sampling, manifests, integrity. | Defining Canon truth; choosing flattering examples. |
| **Controller** (human) | Product direction, architecture, task authorisation, accept/reject, merges. | — |
| **Repository Governor** | Repository coherence, this document, integrity review, audits. | Project strategy; domain methodology. |

Charters: `canon/CHARTER.md`, `eval/CHARTER.md`, `resources/CHARTER.md`. Streams own their
directories exclusively; cross-stream change goes through `PROPOSED-INTEGRATION-CHANGE-<ID>.md`
files. Parallel Controller sessions follow the **Writer/Advisory convention** in
`coordination/RUNBOOK.md` — one Writer Controller at a time may mutate programme state.

## 4. Frozen decisions that constrain current work

Not reopened without an approved integration task. Full list:
`coordination/PROJECT-CONTRACT.md` ("Major separations"). The ones that most often trip a fresh
session:

1. **Creative IR ("what should exist") ≠ Production IR ("how today's tools make it").** Production
   IR does not exist yet.
2. **Book knowledge is never evidence about model capability.** The Registry is empirical only, and
   admits only `qualified`/`deterministic` instruments — **admission must not be weakened to create
   a first row** (`coordination/decisions/CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md`).
3. **Public dataset labels are one source's observations, not our ground truth.**
4. **A worker's recommendation is not an approved decision** — only a Controller disposition makes
   it one.
5. **Historical baselines are never rewritten to match current numbers.** Supersede; never mutate.
6. Frozen measurement foundations: CANON-010 request contract (seven operation values; production
   routes forbidden as operations); Capability Contract v2 (**44 = 43 active + 1 dormant**); 13
   condition families (no cartesian sweep; no single complexity score); 12 core + 2 reserve
   scientific slots; Resources outcome topology v3 / CpAO v3 / four controlled packs, no fifth;
   staged plan Q=0 · A=90 · B≤404 · C=32 outcome attempts. **Several merged contracts still say
   `NOT IN FORCE` in their own status headers — that wording is stale; `CONTROL-STATE.md` governs.**
7. **One provider/API/transform call = one trial**; repeat is not retry; failed/refused attempts are
   kept individually; a requirement blocked by a failed prerequisite is **never** a pass and never
   "not applicable".

## 5. Current empirical floor and headline results

Current authorisation state always comes from `coordination/CONTROL-STATE.md`. The stable picture:

**Still zero (mechanically verified where possible):** qualified models/workflows · qualified
subjective/perceptual evaluator families · strict-exactness-qualified text evaluators (five
configurations tested, five disqualified, unrewritten) · qualified temporal-video evaluators (no
numeric pass mark exists) · **Capability Registry rows — a deliberate decision, not an absence** ·
customer-outcome CpAO observations (Stage C
only; not authorised) · Production IR / Planner · **the mechanical acceptance gate** (pre-dispatch
and post-draw checks as code — designed in `canon/CANON-SHAPE-v1.md` §4, **not built**) ·
**accepted-outcome-rate measurements** (no acceptance-rate run has ever been commissioned) ·
**8 of the 10 compiled packs**.

**EVAL-038 did not move any of those zeros.** It generated real media (2 images + 2 videos + a
replay pair) and the Controller judged it, but that authority labelled media generation **product
learning only — never Capability Registry evidence**. Do not read EVAL-038 artifacts as a qualified
model, a qualified evaluator, a Registry row, or a customer-outcome CpAO observation.

**No longer zero:**

- **Paid execution happened.** The user approved EMP-001 at **USD 10 total / USD 6 qualification
  sub-cap / 0 retries** (`coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md`).
  Recorded spend: **USD 2.6397905** cumulative through EVAL-024, plus **USD 0.024** for EVAL-030 (no
  committed artifact states a consolidated total including it — GOV-006 G6-02).
- **1 benchmark-qualified text evaluator:** Google Cloud Vision `TEXT_DETECTION`, no language hints
  — benchmark-qualified on Devanagari (false-pass 0.1250, false-fail 0.0208, consistency 1.0) and
  Latin (0.1042 / 0.0000 / 1.0) under `benchmark_text_ocr_v1`; still **not** strict-exactness
  qualified. Evidence sealed and recomputable:
  `eval/empirical-tranche-1/evidence/EMP-001/text-ocr/`.
- **16 A-TEXT images** — sealed committed bytes, scored **7/16 exact** (GPT Image 2 **6/8**,
  Ideogram v3 **1/8**): the project's first empirical model comparison. A **directional signal**
  with the evaluator's error rate carried on every row — not a certification, not a population rate.
  Evidence: `eval/empirical-tranche-1/atex/sealed-generation-v1/` (do not regenerate) and
  `eval/empirical-tranche-1/evidence/EMP-001/atex-scoring/`.
- **The mechanism finding:** modern recognisers (VLM and OCR alike) repair misspelled words on
  purpose — accuracy and literalness are opposite virtues for an exactness checker. Turning off
  dictionaries cut false passes to 3 but pushed false-fails to 0.67. Details: `history/EMP-001.md`.
- **Temporal machinery + material, nothing qualified:** EVAL-026 shipped 13 deterministic
  perturbation types covering all 9 frozen `temporal_video` capabilities (7 full injected-truth, 2
  negative-direction-only); RES-005 acquired 12 rights-cleared base clips (12/12 clean; only a
  representative **3/3** passed ingest — **not** 12/12; role `MAT-TEMPORAL-BASE`, not
  `PACK-AV-CLEAN`; content requirement is pack-level).
- **EVAL-037:** the Controller accepts the bounded programme conclusion **Canon helps, but current retrieval/consumption is not mature**. This is enough to carry Canon forward, but not a universal treatment-effect estimate or a production retrieval design. See `eval/experiments/EVAL-037/CONCLUSION.md` and `coordination/decisions/CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`.
- **EVAL-038 — a committed negative result, and the verdict is reserved.** Weak model + the two
  compiled packs did not match a strong model alone on any of six briefs: **0/6**, all 18 top-3
  slots to the Sonnet NO_CANON baseline, judged blind against a decision rule fixed before
  execution. The cheap arm also cost **more** per package (USD 0.072 vs 0.063). **The tested
  substitution configuration is closed — do not rerun it.** Spend: **USD 2.260122** of a USD 10.00
  cap, 0 retries. Media generated here is **product learning only, never Registry evidence**.
  Observations recorded without verdict: the compiled doctrine forbids both PILOT-001 candidates
  the Controller rejected, on the Controller's own grounds; the pack-guided image won the B06 pair;
  both videos failed on baked-in text, the exact defect the packs guard against. **Whether Canon
  works is the Controller's call and is explicitly reserved** —
  `canon/findings/PROPOSED-EVAL-038-CONCLUSION.md` is a worker proposal, not an adopted finding.
  Evidence `eval/experiments/EVAL-038/`; authority
  `coordination/decisions/CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`.
- **Canon:** **37 live accepted sources** · **1,300 SourceKnowledge objects** · 132 concept
  systems · 291 bindings, with **5 HOLD** (desai, airey, freeman-beyond, samara-ch2; ries retired).
  Grew 24 → 37 under the REP-07 admission batch
  (`coordination/decisions/CONTROLLER-REP-07-ADMISSION-BATCH-2026-09-01.md`); `google-abcd` carries
  a `platform_contingent` marker and `sontag` a `critique_context` marker, and three same-work
  extensions entered as scoped extensions, never independent origins. Recompute the count with
  `python3 canon/validation/validate_audit_gate_v02.py` (37 records, 0 errors). **Two numbers that
  must never be confused:** live accepted Canon = **37**; the CANON-003 method-test corpus =
  **16, fixed forever**. **2 of 10 compiled packs** exist (`product_appearance`,
  `composition_and_attention`). CANON-014 also
  preserves **1,028 grounded, ungraded, uncalibrated Q&A items** across 23 banks. HOLD material is
  not accepted Canon and current runtime retrieval still reads `canon/knowledge/current/**` only.
  The corpus index and separate accepted/full/Q&A fingerprints are under
  `canon/knowledge/CANON-CORPUS-INDEX.yaml`. **CANON-011:** 18 marketplace-derived buyer cases
  from Upwork buyer postings, 16 runnable — the preferred real-demand pool for Stage-C selection;
  not a Canon source; the Media Request Grammar was **not** reopened (GG-01…GG-04 are recorded
  observations only).
- **Resources corpus:** 34,786 items / 5.70 GB across 8 sources; IndicSTR12 and IIIT-ILST are one
  source lineage (173 shared files); BSTD is the only genuine cross-lineage reserve, held untouched.
  Rights: internal research/evaluation only.

**Exact-text imperfection is not a programme-wide blocker.** It may block a job that requires certified exact text, but it does not stall unrelated image/video/audio work.

**Two text standards exist and every text result must name its standard:** *strict exactness
certification* (zero false passes — nothing has ever passed) vs *benchmark-grade OCR*
(`benchmark_text_ocr_v1`, bounded error — Cloud Vision passes). Both true simultaneously; neither
was rewritten (`coordination/decisions/CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md`).

## 6. Current direction and blockers

**Read `coordination/CONTROL-STATE.md` for the live version.**

- **EVAL-037 / T2B is concluded for programme direction:** Canon helps; the current retrieval / consumption interface is not mature.
- **EVAL-038 is a settled lane.** The substitution question is closed for the configuration tested
  (0/6, refuted). **The verdict on whether Canon works is reserved to the Controller** and is not to
  be concluded further by any worker.
- **`canon/CANON-SHAPE-v1.md` is the governing consumption shape for Canon** — adopted by the
  Controller ("Let's stick with that") under
  `coordination/decisions/CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md`. It settles what Canon
  is, what it is for, and how it is consumed: packs injected unconditionally as a cached prefix, no
  forced-consumption receipts, mechanical gates in code, blueprints amortised over cheap redraws.
  **Adopting the shape authorises no build.**
- **The next gate is the gate build** — pre-dispatch and post-draw checks derived as code from
  PA-D1..D10 / CA-D1..D11, baked-text scan first (`canon/CANON-SHAPE-v1.md` §7 item 1). It is the
  next build **when the Controller directs it**; it is not yet authorised.
- **The programme is back in Controller planning mode.** The next move is not another broad Canon-value experiment; it is a rebase of T3-T8 around the shortest route to an end-to-end accepted-outcome product.
- **EVAL-036 remains authorised at USD 0** as a historical-prior import, but its sequencing must now be justified by outcome value rather than treated as an automatic gate.
- **No new paid tranche is currently authorised.**
- **Production IR, Planner, routing runtime, repair runtime and customer-facing API still do not exist.** They should be extracted/implemented from proven outcome-producing workflows, not designed abstractly first.
- Persistent blockers include HED-1 for fully loaded CpAO and the empty Capability Registry by deliberate admission policy.

## 7. Critical traps for a fresh session

1. **Do not conclude paid execution is unauthorised or nothing was generated** because a task file
   or handoff says so — `eval/HANDOFF.md` still claims ₹0 spend. `CONTROL-STATE.md` governs.
2. **Do not treat settled lanes as open work.** CANON-011, EVAL-024, EVAL-029, EVAL-026, EVAL-030,
   RES-005, REP-07 and **EVAL-038** are merged and closed; a task file is never an authorisation.
3. **Do not regenerate the 16 sealed A-TEXT images.** They are durable evidence, verified by hash.
4. **Do not add a Registry row from the 7/16 result or weaken admission to allow one.**
5. **Always name the standard a text result was measured against** (strict vs benchmark); never
   present benchmark-grade OCR as an exactness guarantee.
6. **Do not claim 12/12 temporal ingest or any qualified temporal evaluator**, and never invent a
   pass mark to let a run conclude.
7. **Do not read a `NOT IN FORCE` / `PROPOSED_…_NOT_FROZEN` status header as truth** — several
   merged artifacts carry stale generator-emitted statuses (GOV-005 F-6, GOV-006 G6-03).
8. **The chat-only human re-reading of the A-TEXT images is not project evidence** and must not be
   imported. No mandatory human-in-the-loop step exists in the production API architecture.
9. **Cancelled work stays cancelled** (EVAL-028, EVAL-034; EVAL-006 paused) unless a **newer**
   Controller decision reopens it.
10. **Do not conclude EVAL-038 any further, and do not rerun the refuted configuration.** The
    Controller has reserved the judgment of whether Canon works. Record observations; never issue a
    verdict. `canon/findings/PROPOSED-EVAL-038-CONCLUSION.md` is a proposal, not a finding.
11. **Do not read EVAL-038 media as capability evidence.** It was authorised as product learning
    only. No Registry row and no qualification claim comes from it.
12. **Do not treat HOLD/candidate material as accepted Canon merely because it is durable.**
    Runtime retrieval remains accepted-only unless a separately frozen experiment explicitly exposes
    the status-carrying full corpus. After the REP-07 admission batch, **HOLD is 5, not 18** — 13 of
    the former candidates were admitted; `ries` is retired and must never be put to the Audit Gate.
13. Longer lessons list (paid for, do not rediscover): `history/EMP-001.md` §Lessons and
    `history/PROJECT-MEMORY-PRE-CONTEXT-MIGRATION-2026-08-28.md` §6.

## 8. History — where the narrative went

Detailed chronology moved out of this file on 28 Aug 2026 (nothing was lost):

- `history/EMP-001.md` — the full first-paid-tranche story: qualification table, mechanism finding,
  spend, evidence sealing, EVAL-029/024/030.
- `history/GOVERNANCE-2026-08.md` — V1 baseline, macro reset, pre-execution freeze, EVAL-008,
  GOV-001…GOV-006, post-GOV-006 authorisation sequence, external-research posture.
- `history/PROJECT-MILESTONES.md` — dated milestone table with evidence pointers.
- `history/PROJECT-MEMORY-PRE-CONTEXT-MIGRATION-2026-08-28.md` — byte-for-byte pre-migration
  snapshot (the completeness guarantee).
- `history/PROJECT-MEMORY-PRE-EVAL-038-REFRESH-2026-09-01.md` and
  `history/CONTROL-STATE-PRE-EVAL-038-REFRESH-2026-09-01.md` — byte-for-byte snapshots of both
  current-state documents immediately before the 1 Sep 2026 refresh.

## 9. Authority map — which file proves what

| Question | Authoritative file |
|---|---|
| Product definition and frozen separations | `coordination/PROJECT-CONTRACT.md` |
| What is currently authorised, blocked, active | `coordination/CONTROL-STATE.md` — **the most important file after this one** |
| What has the Controller decided | list `coordination/decisions/` directly (+ stream decision records); `coordination/DECISION-LOG.md` is a curated index only |
| How to start a session / approve a task / escalate | `coordination/RUNBOOK.md` |
| How to communicate | `shared/COMMUNICATION-STANDARD.md` |
| When to read more / when to stop | `shared/CONTEXT-SUFFICIENCY-POLICY.md` |
| When a worker may run unattended | `shared/AUTONOMY-POLICY.md` |
| Which validator verifies which artifact family | `verify/VALIDATOR-INDEX.yaml` |
| Per-stream status convenience view | `coordination/WORKSTREAM-STATUS.md` — derived; `CONTROL-STATE.md` governs |
| Current exact-text posture | `coordination/decisions/CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md` |
| Why the Registry is empty despite a benchmark result | `coordination/decisions/CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md` |
| The 16 A-TEXT images + hashes | `eval/empirical-tranche-1/atex/sealed-generation-v1/atex-generation-only-manifest.json` |
| What they scored | `eval/empirical-tranche-1/evidence/EMP-001/atex-scoring/atex-benchmark-scoring-v1.json` |
| Sealed text-OCR evidence | `eval/empirical-tranche-1/evidence/EMP-001/text-ocr/` |
| Approved spend and by whom | `coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md` |
| Temporal material contract (pack-level; `MAT-TEMPORAL-BASE`) | `coordination/decisions/CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md` |
| Is any temporal evaluator qualified — **no** | `eval/v1/instruments/temporal-perturbation/perturbation-contract.yaml` (pass mark `DOES_NOT_EXIST`) |
| Is EVAL-028 running — **no, cancelled** | `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md` |
| v2 contracts (request, capability, condition, topology, CpAO) | `canon/experiments/pre-execution-freeze/`, `eval/pre-execution-freeze/`, `eval/pre-execution-integration/`, `resources/pre-execution-freeze/` — merged and in force despite stale status headers |
| The 36 capabilities, 100-item bank, 30 briefs, persistence contract (V1 historical baselines) | `eval/v1/capability-contract.yaml`, `eval/v1/bank/`, `canon/experiments/v1/brief-bank/`, `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` |
| Canon admission method | `canon/audit/AUDIT-GATE-v0.2.md` |
| Which Canon sources are live (**37**) | `canon/audit/records/` + `canon/knowledge/current/`; recompute with `canon/validation/validate_audit_gate_v02.py` |
| What Canon is, what it is for, and how it is consumed | `canon/CANON-SHAPE-v1.md` — the governing shape |
| Which Canon sources were admitted, and on what markers | `coordination/decisions/CONTROLLER-REP-07-ADMISSION-BATCH-2026-09-01.md` |
| What EVAL-038 established, and who owns the verdict | `coordination/decisions/CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`; evidence `eval/experiments/EVAL-038/` |
| Why CANON-SHAPE-v1 governs and what it does not authorise | `coordination/decisions/CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md` |
| Full Canon map, HOLD candidates and corpus fingerprints | `canon/knowledge/CANON-CORPUS-INDEX.yaml` + `canon/candidates/canon-014/` |
| CANON-014 grounded Q&A corpus | `canon/qa/canon-014/` |
| The authoritative Eval battery (96-item validated view) | `eval/battery/devanagari-exactness/human-validation/` |
| Real customer demand evidence (external, not a Canon source) | `canon/research/marketplace-demand-v1/`; derived bank under its `derived/` |
| What media we hold | `resources/manifests/corpus-pilot-v0.jsonl`, `source-registry-v0.csv` |
| Governor role and review modes | `governance/GOVERNOR-CONTRACT.md` |
| Current Governor review | `governance/reviews/GOV-L1-CANON-014-FULL-CORPUS.md` (Level-1, CANON-014; last full reconciliation remains `GOV-006-POST-PARALLEL-RECONCILIATION.md`) |
| What is believed but untested | `coordination/ASSUMPTIONS.md` |
| Known limitations / unresolved questions | preserved in `history/PROJECT-MEMORY-PRE-CONTEXT-MIGRATION-2026-08-28.md` §7; live blockers in `CONTROL-STATE.md` |

## 10. How to start a session

Follow the default bootstrap in `coordination/RUNBOOK.md`:

1. this document → 2. `coordination/CONTROL-STATE.md` → 3. `coordination/PROJECT-CONTRACT.md` →
4. `shared/COMMUNICATION-STANDARD.md` → 5. `shared/CONTEXT-SUFFICIENCY-POLICY.md` → 6. your stream
`CHARTER.md` → 7. your assigned task → 8. the task's named dependencies → then **expand context
whenever the policy requires it**, and stop (`STOP — CONTEXT_INSUFFICIENT`) rather than guess.

Stream `HANDOFF.md` files, full history and broad evidence are **not** default reading — they are
expansion targets. Controller sessions declare Writer or Advisory mode (`coordination/RUNBOOK.md`).
Governor sessions: `governance/GOVERNOR-CONTRACT.md`.

**Before acting on any authorisation, check `coordination/CONTROL-STATE.md`.** A task file is not an
authorisation. A session may persist for convenience, but no important project fact may depend on
it — if you learn something that matters, it belongs in GitHub before the session ends.
