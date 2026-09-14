# Project Memory

**The canonical entry point for this project — a compact map to authority, not the authority
itself.** Read this first, every session; then `coordination/CONTROL-STATE.md` for what is currently
authorised.

**Maintained by:** the Repository Governor (`governance/GOVERNOR-CONTRACT.md`).
**Last refresh:** 14 Sep 2026 — the audit-closeout refresh ordered by Controller ruling C-6
(`coordination/decisions/CONTROLLER-GOVERNOR-REFRESH-ORDER-2026-09-14.md`), after the two-day
Capability Lab run (8–10 Sep, EVAL-040…043), the two independent audits of 10 Sep, the Controller's
fifteen rulings of 14 Sep (C-1…C-11, six records dated 2026-09-14 under `coordination/decisions/`),
the regeneration of the routing map and taint register under those rulings, and the first runtime
lanes. The last full Governor reconciliation *review* remains **GOV-006**
(`governance/reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`); this refresh is a state-of-record
refresh, not a Governor review. The text immediately before it is preserved byte-for-byte at
`history/PROJECT-MEMORY-PRE-AUDIT-CLOSEOUT-REFRESH-2026-09-14.md` (earlier snapshots:
`…-PRE-GATE-001-REFRESH-2026-09-07.md`, `…-PRE-EVAL-038-REFRESH-2026-09-01.md`,
`…-PRE-CONTEXT-MIGRATION-2026-08-28.md`); detailed narrative lives under `history/` (see §8).

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

**What exists vs what does not (14 Sep 2026).** The Normalized Request grammar, Creative IR v0.1,
accepted Canon knowledge (37 sources, 2 of 10 compiled packs), the compiled-doctrine gate as code,
the frozen measurement contracts, the Stage-A execution harness with sealed evidence, **the Capability
Registry (575 deterministic rows)** and the tiered routing map with its taint register **exist**. On the
integration branch `work/audit-closeout-and-runtime-v0` a **production runtime exists as code**
(`runtime/`): four frozen contracts (PRODUCTION-JOB, PRODUCTION-SPEC, ROUTE-DECISION,
OUTCOME-EVENT), intake, a brief → Production Specification compiler with deterministic Canon lookup
(PC-03A), an evidence-aware router with declared fallback and live price pins (PC-03B), and policy
profiles carrying every operating limit as data. **PRODUCTION-SPEC-v1 is the Production IR; the router
is the Production Planner's first half.** What does **not** exist on that branch: an execution bridge
to a provider, post-draw checks on a real artifact, a repair loop, acceptance states, the
empirical-memory event writer, a customer-facing API — the child branch
`work/runtime-alpha-vertical-slice-v0` builds those at USD 0 in dry mode (see `runtime/ALPHA-1.md`).
**The runtime has never called a provider; every run to date is dry.**

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
   IR now exists as PRODUCTION-SPEC-v1 (`runtime/contracts/`), compiled from a job by code plus one
   recorded reasoning pass; it is still the "how, today" object and never the Creative IR.
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
numeric pass mark exists) · customer-outcome CpAO observations (Stage C only; not authorised) ·
**accepted-outcome-rate measurements** (no acceptance-rate run has ever been commissioned) ·
**8 of the 10 compiled packs** (and none is compiled without a real runtime failure — C-10) ·
**post-draw text detection on a real artifact** (the gate's Cloud Vision adapter is wired and has
never been invoked) · **any real, paid run of the production runtime** · **vendor-billed cost** (no
provider statement has been reconciled; the ledger figure is an upper bound).

**Four kinds of evidence, never mixed (the distinction every reader must keep):**

1. **Deterministic Registry evidence** — 575 rows, frozen instruments over sealed bytes; untouched by
   every 14-Sep ruling; never reads a human verdict; `independence NOT ESTABLISHED` on every row.
2. **Clean human-routing evidence** — 36 of the 61 routing-map cells are `clean_observed` in
   `eval/capability-map/TAINT-REGISTER-v1.yaml` (the literal frozen elimination rule reproduces the
   number, every named problem disposed of by a ruling, ≥ 4 settled draws); production use allowed on
   29; the Alpha-1 profile auto-routes 26. One judge, 4–8 draws — honest evidence, not proof.
3. **Directional / descriptive product evidence** — 25 cells `directional_only` (< 4 settled draws);
   the successful Wan 2.2 re-sends kept as `descriptive_resends` (C-6b: "do not delete them"); all
   EVAL-038 media; the Media Factory historical priors.
4. **Tainted / awaiting / eliminated** — 0 cells awaiting a ruling, 0 `method_tainted`; 17 cells
   eliminated on their question under the frozen rule (`production_use_allowed: false`), three of them
   needing a clean rerun before the route can be re-tested (`replacement_needed`).

**The gate, the Registry, the routing map and the runtime are no longer zero** — see "No longer
zero" below — but none of them moved the zeros above. **EVAL-038 did not move any of those zeros either.** It generated real media (2 images + 2 videos + a
replay pair) and the Controller judged it, but that authority labelled media generation **product
learning only — never Capability Registry evidence**. Do not read EVAL-038 artifacts as a qualified
model, a qualified evaluator, a Registry row, or a customer-outcome CpAO observation.

**No longer zero:**

- **The Capability Lab ran (EVAL-040…043, 8–10 Sep 2026).** 35/35 Stage-A cases dispatched and
  blind-judged; 311 sealed media files (re-hash exactly:
  `python3 coordination/audits/tools/verify_sealed_evidence.py`); **575 deterministic Registry rows**
  (`python3 eval/registry/validate_registry.py` — PASS); a 61-cell routing map with rules RR-1…RR-16
  regenerated 14 Sep under the Controller's rulings (**RR-16 withdrawn** as image-to-video routing
  truth; **RR-1 rewritten** to say code, not the image model, produced the accepted exact copy); ledger
  spend **USD 122.241262** counted against caps, two cap crossings and one call-limit breach **accepted
  as recorded** (C-1, C-5b), the mechanisms fixed (per-authorisation pooling; cumulative budget lineage
  under C-6a). The vision judge is **not qualified** (agreement 66 %, false-accept 22 %).
- **The production runtime exists as code (14 Sep 2026, integration branch)** — see §1. Adopted Alpha-1
  policy: **one static commercial ad with exact overlay copy, optionally one short motion version from
  the accepted still; human approval before every external delivery; no spend authority** (C-7, C-8;
  `runtime/contracts/POLICY-PROFILES.yaml`, `runtime/ALPHA-1.md`).
- **Paid execution happened (EMP-001, Aug 2026).** The user approved EMP-001 at **USD 10 total / USD 6 qualification
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
- **CANON-GATE-001 — the compiled-doctrine gate exists as code** (`canon/gate/`, merged 7 Sep
  2026 via PR #88; `coordination/decisions/CONTROLLER-CANON-GATE-001-MERGE-2026-09-07.md`). It
  reads the 21 check lines from the two compiled packs by id, runs a pre-dispatch inspection over a
  production package and its generation prompts and a post-draw inspection over artifact bytes,
  and prints every one of the 21 lines on every run with a status and a reason. **Honest scope:**
  10 lines are mechanised partially (a literal clause each), 11 not at all; the blocking set is the
  baked-text guard, delivered-vs-declared (aspect, dimensions, duration, shot sum), the named-ratio
  prohibition, the integrity rows and any extraction error; declaration-presence partials report
  but do not block. On the committed fixtures it fails both EVAL-038 video packages on the exact
  sentences that produced the baked-text defects, passes the accepted image, and flags the image
  delivered below its declared size. Built maker/checker over nine bounded checker passes; USD 0;
  the extractor fails closed on every quoted-content path a checker could name (274 tests, a
  172-row intended-vs-observed battery, a no-silent-discard invariant). **A gate PASS establishes
  structure over the submitted bytes — never doctrine satisfaction, quality, outcomes or
  adoption — and bears nothing on whether Canon works.** Run: `python3 canon/gate/run_gate.py`.
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

- **The programme changed mode on 14 Sep 2026: from widening the Capability Lab to building the
  smallest complete production path.** C-9 stops Lab widening (no generic battery, no premium sweep,
  no prettier tables; new evidence only where the runtime exposes a launch-critical hole). C-7 freezes
  Alpha 1. C-10 authorises Canon Injection v1 and template/empirical-memory integration at USD 0 and
  forbids compiling the remaining eight packs without a real runtime failure. C-11 adopts the
  twelve-condition public-release gate; none of the twelve is met.
- **Nothing paid is authorised.** Every runtime profile carries `spend_authority.status: none`; every
  Group-3 Lab item (C-12…C-18) needs its own signed record. The first paid act the runtime justifies is
  one Alpha-1 vertical-slice run (single-digit USD) — a recommendation, not an authorisation.
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
- **The gate is built and merged (CANON-GATE-001).** Of `canon/CANON-SHAPE-v1.md` §7's open items,
  **injection v1 and the template library are now authorised at USD 0 (C-10, 14 Sep 2026)** and are
  built on the runtime child branch; the remaining packs are not; the acceptance-rate run (the cheapest
  decisive measurement of the reserved question) is **not** commissioned. The **CANON-GATE-002
  register** is opened by the merge decision and is **not** a task.
- **EVAL-036 remains authorised at USD 0** as a historical-prior import, but its sequencing must now be justified by outcome value rather than treated as an automatic gate.
- **Production IR (PRODUCTION-SPEC-v1), intake, the spec compiler and the router exist on the
  integration branch; the execution bridge, gates, repair, acceptance states and memory event are
  being built dry on the child branch.** A customer-facing API does not exist. Nothing has been run for
  money.
- Persistent blockers: HED-1 for fully loaded CpAO; the four provider statements are unreconciled
  (upper-bound costs only); the two recommended still routes are priced on the Gemini Developer API,
  a surface that has never carried a paid call (C-13 would close it).

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
13. **Do not read gate output as a verdict on Canon.** A gate PASS means no mechanised check
    failed over the submitted bytes; 11 of 21 doctrine lines are never mechanised and are printed
    as such. The gate is Canon's *consumption*, not its *evaluation*. The verdict stays reserved.
14. **The CANON-GATE-002 register is a list of recorded limitations, not an authorisation.** Each
    item needs its own Controller decision. Its root-cause entry — the gate extracts prompts from
    free prose — is the reason nine checker passes were needed; do not patch a tenth edge without
    reading the merge decision first.
15. Longer lessons list (paid for, do not rediscover): `history/EMP-001.md` §Lessons and
    `history/PROJECT-MEMORY-PRE-CONTEXT-MIGRATION-2026-08-28.md` §6.
16. **Do not read a `clean_observed` cell as a launch clearance, a statistic or an SLA.** It means the
    literal frozen rule reproduces a 4–8 draw number judged by one person, with every named problem
    disposed of by a ruling. The runtime's policy profile, not the register, decides what may be
    auto-routed (`eval/capability-map/TAINT-REGISTER-v1.yaml` header).
17. **Do not read RR-1's 4/4 as "the image model wrote the text".** Code composed the exact strings onto
    a textless plate (mechanism B, cell `IMG-TEXT/flux-2-pro+code_overlay`); the same plates judged bare
    were 1/4 (C-6c). And **do not read RR-16 as routing truth** — Wan 2.2 A14B is eliminated from
    image-to-video under the frozen rule; its successful re-sends are descriptive only (C-6b).
18. **Do not treat `adopted: true` on a policy profile as permission to spend.** Adoption is a policy
    agreement (C-7/C-8); `spend_authority` is money, and it is `none` everywhere (Controller rider,
    14 Sep 2026). **No 14-Sep decision authorises a paid dispatch.**
19. **Do not edit a sealed results file to match the literal rule.** The correction lives in the
    regenerated map and register and in the recompute tool (C-3, C-6d; OPEN-2 closed by this rule).
20. **Do not widen the Capability Lab** — no new battery round, premium sweep or "tidier" two-draw cell
    without a launch-critical hole exposed by the runtime and a signed spend record (C-9).

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
- `history/PROJECT-MEMORY-PRE-GATE-001-REFRESH-2026-09-07.md` and
  `history/CONTROL-STATE-PRE-GATE-001-REFRESH-2026-09-07.md` — the same, immediately before the
  7 Sep 2026 post-gate refresh.

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
| Why the Registry held 0 rows until 9 Sep 2026 despite a benchmark result | `coordination/decisions/CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md` |
| The Registry's 575 deterministic rows and their admission criteria | `eval/registry/registry-v1.jsonl`, `eval/registry/validate_registry.py`, `coordination/decisions/CONTROLLER-INSTRUMENT-THRESHOLDS-FROZEN-2026-09-09.md` |
| The routing map (61 cells, RR-1…RR-16) and what each number is worth | `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml` (generated), `eval/capability-map/TAINT-REGISTER-v1.yaml` (generated); regenerate per `coordination/audits/AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` §Addendum |
| What the 10-Sep audits found and how every item was ruled | `coordination/audits/HANDOFF-TO-CONTROLLER-2026-09-10.md`, `AUDIT-2026-09-10-CONTROLLER-DECISIONS.md` (dispositions), the six `CONTROLLER-*-2026-09-14.md` records |
| Spend of record, cap crossings, budget lineage | `coordination/audits/AUDIT-2026-09-10-SPEND-RECONCILIATION.md`; `python3 coordination/audits/tools/reconcile_spend.py`; `eval/harness-v2/ledger.py` |
| Sealed evidence intact | `python3 coordination/audits/tools/verify_sealed_evidence.py --against origin/main` |
| What Alpha 1 is, and the difference between adopted and spend-authorised | `runtime/ALPHA-1.md`; `runtime/contracts/POLICY-PROFILES.yaml`; `coordination/decisions/CONTROLLER-ALPHA-1-PRODUCT-FAMILY-AND-RELEASE-POLICY-2026-09-14.md` |
| The production runtime's contracts and what building them found | `runtime/contracts/README.md`, `runtime/contracts/CHANGES-v0-to-v1.md`; tests `python3 -m unittest discover -s runtime/tests -p 'test_*.py'` |
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
| The compiled-doctrine gate: code, CLI, what it mechanises and what it does not | `canon/gate/` (`run_gate.py`, `GATE-BUILD-PLAN-v0.md` §A derivation table); tests `tests/test_gate_*.py`; `python3 -m tests.test_gate_regression_battery --table` |
| Why the gate merged, its guarantee in one sentence, and the CANON-GATE-002 register | `coordination/decisions/CONTROLLER-CANON-GATE-001-MERGE-2026-09-07.md` (Ruling 13; Rulings 1–12 are the `CONTROLLER-CANON-GATE-001-*` records beside it) |
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
