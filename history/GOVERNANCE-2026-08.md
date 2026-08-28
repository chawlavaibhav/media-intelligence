# Governance and programme narrative — August 2026

**Status of this file:** historical chapter, moved out of `PROJECT-MEMORY.md` in the 2026-08-28
context migration. Current state lives in `coordination/CONTROL-STATE.md`; the named Controller
decisions and Governor reviews govern over this narrative. The original wording as GOV-006 left it
is preserved byte-for-byte in `history/PROJECT-MEMORY-PRE-CONTEXT-MIGRATION-2026-08-28.md`.

## The V1 architecture baseline — accepted 26 Aug

On the night of 25 Aug the three streams each produced a V1 design layer. The Controller reviewed
them, assigned correction passes, and accepted and merged all three
(`coordination/decisions/CONTROLLER-V1-OVERNIGHT-INTEGRATION-2026-08-26.md`). Four artifacts anchor
everything since — all design and measurement scaffolding, none of them empirical evidence about any
model:

| Artifact | What it is | Where |
|---|---|---|
| 30 authored commercial briefs | Hand-written customer briefs with objectives, audiences and acceptance criteria. A designed probe bank, never evidence of what customers actually ask for. | `canon/experiments/v1/brief-bank/` |
| 36-capability contract | The list of things a commercial media output can be measured on, with instrument and readiness per dimension. | `eval/v1/capability-contract.yaml` |
| 100-item Eval bank | Reusable test items designed so one generation can be measured many times. | `eval/v1/bank/` |
| Persistence contract v2.1 | How attempts, artifacts, measurements and cost are stored so a cost figure is always traceable to a real call. One provider/API/transform call = one trial. | `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` |

Also accepted: Creative IR v0.1, six evaluator families as a baseline, and the rules *repeat is not
retry* and *failed and refused attempts are kept individually, never collapsed into a counter*.
Verified mechanically during GOV-003: exactly 30 briefs, 36 dimensions, 100 items, 0 Registry rows.

## The 26 August macro reset

**What went wrong, in one sentence.** Before spending money on the first paid benchmark, the
Controller noticed that the 30 authored briefs and the 36-capability contract were starting to
*define* the product rather than *test* it — the benchmark was becoming the specification.
(`coordination/decisions/CONTROLLER-CLOUD-MACRO-RECALIBRATION-2026-08-26.md`.)

**The rule adopted instead:** research what customers actually request, independently research what
today's models can and cannot do, independently research what evidence and persistence the project
needs — and only then integrate the three and freeze the real empirical programme.

Three research programmes ran on that basis, each ₹0, no model or evaluator call, no Registry entry;
all three are merged into `main`:

| Programme | What it produced |
|---|---|
| CANON-009 | A map of real media-generation request patterns from 13 public sources, a proposed 14-part Media Request Grammar, and a measured audit of the 30-brief bank against it. |
| EVAL-007 | An external audit of the 36 capabilities, an evaluator/qualification landscape, a four-layer benchmark v2 proposal, and a cost forecast that refuses to produce a total. |
| RES-003 | Dataset rights and independence research, a corpus rebaseline, a leakage/protected-set proposal, and a proposed whole-outcome persistence topology with a working cost-recomputation engine. |

**The most consequential finding — a gap, not a result.** CANON-009 measured the 30-brief bank
against real request patterns and got an inversion: the two operations the world most demonstrably
asks for (edit a supplied asset — 82,976 real requests in one corpus; animate a supplied image —
1.70M+ requests) had **0** briefs, while exact text in the image (no real-user frequency figure
exists anywhere) had 28 of 30. This does not mean the bank is wrong and is not market-share evidence
— every corpus involved is a model-interface corpus. It means the bank is a narrow probe of a wide
space. Figures reproduced mechanically during GOV-003 by rerunning Canon's measurement script.

**What the Controller adopted** (authoritative record:
`coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md`): the requested
operation is an explicit field on the Normalized Request, separate from the production route; output
sets are first-class; multi-turn is recognised but not solved; the 30 briefs stay byte-identical
with a separate coverage extension; a requirement blocked by a failed prerequisite is never a pass
and never "not applicable"; every empirical result carries its conditions and there is no single
complexity score; fully-loaded Cost per Accepted Outcome is the primary business metric with shared
upstream costs counted once; a discovery corpus and a benchmark drawn from the same request pool are
not independent evidence; four controlled resource packs, no fifth.

## EVAL-008 — model selection first, sourcing second · superseded as supply evidence

A fourth lane ran alongside: `eval/tasks/EVAL-008-CLOUD-MODEL-ACCESS-RESEARCH.md`. Which models to
test is decided independently of where credits happen to be available; the ordering was honoured
provably in git and verified in GOV-003. All nine deliverables exist under
`eval/model-access/2026-08-26/` on branch `claude/eval-008-cloud-model-access-i3fl86`, unmerged,
draft PR #21. **Read it as a candidate universe, not as supply truth** — EVAL-010 has since rejected
eight of its claims, and where the two disagree, EVAL-010 governs. Nothing in EVAL-008 is
authorised.

## The final pre-execution freeze — four packages, merged and in force

After the macro reset, one more ₹0 tranche turned the adopted directions into contracts precise
enough to price. GOV-004 reviewed the four packages; the Controller merged them on 26 Aug 2026
(`coordination/decisions/CONTROLLER-PRE-EXECUTION-CLOSURE-2026-08-26.md`):

| Package | What it froze |
|---|---|
| CANON-010 | The request contract: seven-value operation vocabulary (`generate · edit · animate · restore · extend · compose · variants`), the Normalized Request delta, an 11-item coverage extension. Production-route values are forbidden as operation values and a validator rejects them. |
| EVAL-011 (corrects EVAL-009) | Capability Contract v2 (44 = 43 active + 1 dormant, `repairability` dormant), the 13-family condition contract, dependency scoring, the 12-core + 2-reserve scientific roster, and the staged execution plan (Q=0, A=90, B≤404, C=32 outcome attempts). |
| RES-004 | Outcome topology v3 (`job → outcome → sequence_or_asset_set → production_unit → production_step → attempt → artifact`), the CpAO v3 accounting contract, four controlled-pack requirements. |
| EVAL-010 | Verified model identities, routes and prices — deliberately partial: of 26 candidate rows, 2 execution-ready, 19 identity/route-verified with no verified price. |

`work/eval-009-measurement-freeze` is historical: EVAL-009 shipped an internal contradiction (13
declared condition families vs 12 in prose, making a derived figure 4,096 instead of 8,192); the
Controller ordered one bounded correction and EVAL-011 is the corrected live proposal. No family was
removed to recover the old number; the count was the error.

**A trap that outlived the merge:** several of these artifacts still carry
`status: PROPOSED_FOR_CONTROLLER_FREEZE_NOT_IN_FORCE` in their own headers. That status field is
stale, not authoritative — the generator that emits it was not rerun after the merge.
`coordination/CONTROL-STATE.md` governs. (GOV-005 finding F-6; same class as CANON-011's G6-03.)

Layers 1–3 (494 generations design ceiling) may not report customer-outcome CpAO — no accepted
customer outcomes exist there. The premium-versus-fast cost-knee verdict is a Stage C output only.

## Numbers that are NOT approved budgets

- 494 generations · 5,515 evaluator calls · 188 human review units — the Layers-1–3 *design
  ceiling* and its forecast, not a tranche;
- 173 person-hours of pack acquisition — a provisional plan, explicitly not a prerequisite to the
  first paid model call;
- provisional controlled-pack entity totals — labelled provisional;
- every price in the repository — 0 of 4 stages is price-complete; no missing price has been
  guessed;
- the full 90-generation Stage-A planning estimate (~USD 52.01 + up to ₹4.50 Sarvam) — unapproved;
  the USD 10 approval covered EMP-001 only.

## Governor history — GOV-001 through GOV-006

- **GOV-001** (25 Aug, `main` @ `00ea9b0`): Governor role established; reset audit
  (`governance/audits/2026-08-25-initial-repository-hygiene-audit.md`); mechanical verification of
  Canon 19/19, battery hashes, corpus manifest.
- **GOV-002**: assigned but never executed; superseded
  (`governance/status/2026-08-26-GOV-002-SUPERSEDED.md`).
- **GOV-003** (26 Aug): coherence review of the three macro-research branches — PASS with
  non-blocking notes (`governance/reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md`).
- **GOV-004** (26 Aug, @ `74d6b0d`): final pre-execution coherence review — PASS with non-blocking
  notes (`governance/reviews/GOV-004-FINAL-PRE-EXECUTION-REVIEW.md`).
- **GOV-005** (28 Aug, audit @ `0e24d6a`, refresh @ `8990a7a`): post-EMP-001 coherence review —
  PASS with non-blocking notes. Its High finding F-1 (live evidence existed only as prose because
  `eval/runs/` is git-ignored) drove the evidence sealing. Closed and merged (PR #48, `c794694`);
  do not reopen it (`governance/reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md`,
  `coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md`).
- **GOV-006** (28 Aug, audited @ `91984f5`): post-parallel reconciliation — **PASS WITH
  NON-BLOCKING NOTES**; sealed evidence, artifact hashes and all headline arithmetic independently
  re-derived; seven findings routed (G6-01…G6-07)
  (`governance/reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`). GOV-007 is not authorised.

## The five parallel lanes after GOV-005 — all settled and merged

| Lane | Outcome | Spend | Authority (under `coordination/decisions/`) |
|---|---|---|---|
| CANON-011 | 18 marketplace-derived buyer cases from Upwork buyer postings only, 16 runnable without buyer contact; Media Request Grammar **not** reopened (GG-01…GG-04 recorded as observations, no change made); `MKT-015` retained only as blocked market evidence. Now the preferred real-demand pool for Stage-C selection and compound-scenario sourcing. Not a Canon source; live Canon stays 19. | USD 0 | `CONTROLLER-CANON-011-INTEGRATION-2026-08-28.md` (PR #49, merge `610d69f`) |
| EVAL-024 | 16 A-TEXT images generated and sealed as committed bytes. | USD 0.904 | `CONTROLLER-EVAL-024-INTEGRATION-2026-08-28.md` (PR #50, merge `eadad54`) |
| EVAL-029 | Cloud Vision benchmark-qualified on both scripts, strict-disqualified; evidence sealed into Git. | USD 0.4320 | `CONTROLLER-EVAL-029-REVIEW-SEAL-EVIDENCE-BEFORE-MERGE-2026-08-28.md` (merge `10b237f`) |
| EVAL-030 | The 16 sealed images scored without regeneration: 7/16. Registry stays 0. | USD 0.024 | `CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md` (PR #53, merge `13fe76f`) |
| EVAL-026 | Temporal qualification machinery only: 13 deterministic perturbation types covering all 9 frozen `temporal_video` capabilities (7 full injected-truth, 2 negative-direction-only: `action_adherence`, `camera_framing_fidelity`). No evaluator qualified, no pass mark. 153 package tests pass. | USD 0 | `CONTROLLER-EVAL-026-INTEGRATION-2026-08-28.md` (PR #52, merge `2af1dbd`) |
| RES-005 | 12 rights-cleared temporal base clips from 12 distinct works (CC BY / CC BY-SA / CC0 / US-Gov PD), 12/12 clean; only a representative 3/3 passed EVAL-026 ingest (full 12-clip ingest exhausted local disk). Material role `MAT-TEMPORAL-BASE`, not `PACK-AV-CLEAN`. Content requirement resolved at pack level. | USD 0 | `CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md` (PR #54, merge `3a49464`) |

Temporal opportunity counts (coverage counts, never statistical-precision claims): general
freeze/reversal base 12, multi-shot 6, on-screen text 6, product region 5, rendered-character
identity 4, photographed-face identity 3. The two identity populations are separate and must not be
pooled. Three commits on `main` carry the pack-level reconciliation across streams (`c049cfe`,
`68667c5`, `88b5a1b`), all verified present at GOV-006.

## Post-GOV-006 authorisation sequence (28 Aug 2026)

1. `CONTROLLER-PARALLEL-EMPIRICAL-UNBLOCK-2026-08-28.md` authorised five lanes
   (EVAL-031…034, RES-006) outside GOV-006's audit snapshot.
2. `CONTROLLER-PARALLEL-EMPIRICAL-UNBLOCK-CORRECTION-2026-08-28.md` narrowed them: EVAL-031 do not
   start as written; EVAL-032/033 continue narrowed; EVAL-034 cancelled; RES-006 deferred.
3. `CONTROLLER-STOP-TEMPORAL-PREP-PRIORITISE-PRODUCT-PILOT-2026-08-28.md` — **the currently
   governing disposition**: EVAL-032 and EVAL-033 stopped as immediate work (valid future lab tasks
   only when automated temporal-evaluator qualification is again the objective); the next Controller
   priority is a real customer vertical-slice pilot (product-learning, not Registry evidence, not
   Stage C).

## External research — context, not authority

Source-discovery/acquisition work done outside GitHub is an external research snapshot and never
competes with repository truth. GOV-001 inspected two artifacts dated 24 Aug 2026 in the operator's
local Downloads folder (a Canon expansion report and a candidate-universe workbook); both are
contradicted by the repository on their central arithmetic (they state live Canon is 16; CANON-006/7
took it to 19) and must be recomputed before use. Two further named artifacts were not found and not
inspected. Everything external in the 26 Aug macro research is search-verified, not read (outbound
page fetching was blocked in all three cloud sessions); the Controller separately verified the
load-bearing figures before deciding. The 26 Aug Upwork/Fiverr marketplace research **is** committed
(`canon/research/marketplace-demand-v1/`) with a provenance README; it is not a Canon source and its
volume figures are one capture's research estimates. One qualitative Canon-vs-not advertising
comparison was judged informally by the operator to favour the Canon arm; it is anecdotal, outside
the Eval system, and licenses no capability claim and no Registry entry.
