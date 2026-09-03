# Controller State

**The single primary operational current-state document.** It answers: what is active, authorised,
deferred, cancelled; the current empirical floor; Registry state; spend authority; blockers; and the
next Controller gate. It is a synthesis backed by the durable Controller decisions it links — where
it and any older prose disagree, the latest durable Controller decision governs.

**Updated:** 1 Sep 2026 — REP-07 admission batch, EVAL-038 and CANON-SHAPE-v1 integrated on top of
the 31-Aug EVAL-037 conclusion and the 29-Aug Media Factory programme reset.
The current programme direction is governed by
`coordination/decisions/CONTROLLER-PROGRAMME-RESET-MEDIA-FACTORY-PRIORS-2026-08-29.md` and
`coordination/decisions/CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`, plus the newer 1-Sep trio:
`CONTROLLER-REP-07-ADMISSION-BATCH-2026-09-01.md`,
`CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md` and
`CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md`; CANON-014 integration remains recorded in
`coordination/decisions/CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md`. The text immediately before
this refresh is preserved byte-for-byte at
`history/CONTROL-STATE-PRE-EVAL-038-REFRESH-2026-09-01.md`, and the pre-migration full text at
`history/CONTROL-STATE-PRE-CONTEXT-MIGRATION-2026-08-28.md`; the last full Governor
reconciliation remains GOV-006 (`governance/reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`).

**Read `PROJECT-MEMORY.md` first.**

## Active / authorised

Four **zero-spend pre-pilot tasks are authorised in parallel**:

| Task | Purpose | Spend / generation authority |
|---|---|---|
| **CANON-012** | **Merged / closed.** Corrected Aight NR + Creative IR seed integrated; official Aight wordmark/master remains a PILOT-001 input gate | USD 0; 0 generations |
| **CANON-013** | **Merged / closed.** Feasibility triage integrated; proposed 8/8 development/holdout split remains **unfrozen** | USD 0; 0 generations |
| **EVAL-035** | **Merged / closed.** Direct Gemini/Veo pilot substrate integrated; merged RES-007 writer/validator integration and persistent PILOT-001 spend/cost_ref continuity proven | USD 0; **no real provider call** |
| **RES-007** | **Merged / closed.** Pilot outcome writer + final G12 enforcement integrated; Governor Level-1 PASS WITH NON-BLOCKING NOTES | USD 0; synthetic bytes only |

Authority: `coordination/decisions/CONTROLLER-REVISED-PROGRAM-AND-PREPILOT-TRANCHE-2026-08-28.md`.

The next integration target is **PILOT-001**: customer prompt → Normalized Request → Creative IR
→ frozen manual production recipe → real generation → deterministic brand/text composition →
explicit human inspection → bounded repair → candidate accepted outcome. It is product-learning only
— not Registry evidence, not Stage C.

**PILOT-001 brief / brand source / production recipe / acceptance contract are now frozen** under
`CONTROLLER-PILOT-001-AIGHT-FREEZE-2026-08-28.md`. The previous wordmark blocker is resolved by the
official Aight website-source definition. **Paid PILOT-001 execution is now authorised** under
`CONTROLLER-PILOT-001-SPEND-AUTHORISATION-2026-08-28.md` with a hard max consumed API spend of
**USD 2.00** and **0 retries**. Execution still requires a matching local runtime authorisation,
execution-time route/price verification, and `GEMINI_API_KEY` availability.

CANON-013 runs independently because its output gates the later architecture experiment, not the
Aight pilot.

## Stopped / deferred / cancelled

| Item | Disposition | Authority (under `coordination/decisions/` unless noted) |
|---|---|---|
| EVAL-031 | **Stopped — do not start as written** | `CONTROLLER-PARALLEL-EMPIRICAL-UNBLOCK-CORRECTION-2026-08-28.md` |
| EVAL-032, EVAL-033 | **Stopped as immediate priorities**; valid future lab tasks only when automated temporal-evaluator qualification is again the objective | `CONTROLLER-STOP-TEMPORAL-PREP-PRIORITISE-PRODUCT-PILOT-2026-08-28.md` |
| EVAL-034 | **Cancelled** | `CONTROLLER-PARALLEL-EMPIRICAL-UNBLOCK-CORRECTION-2026-08-28.md` |
| RES-006 | **Deferred** | same |
| EVAL-028 | **Cancelled — must not be executed**; no mandatory human-in-the-loop step exists in the production API architecture | `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md` |
| EVAL-006 | **Paused — do not execute**; spend authority withdrawn | `CONTROLLER-PAUSE-EVAL-006-PENDING-MASTER-PLAN-2026-08-26.md` |
| GOV-007 | **Not authorised** | `CONTROLLER-STOP-TEMPORAL-PREP-PRIORITISE-PRODUCT-PILOT-2026-08-28.md` |
| Historical E7 paid admission / E8 deep qualification | Blocked | pre-execution decisions |
| Canon value gate / EVAL-037 | **Concluded for programme direction:** Canon helps; retrieval/consumption is not mature | `CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md` |
| EVAL-038 substitution configuration | **Closed — refuted 0/6; do not rerun to reconfirm.** The verdict on whether Canon works is **reserved to the Controller** | `CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md` |
| Forced-consumption receipt schema (`INJECTION-CONTRACT-v0.md`) | **Retired as a production mechanism**; the gate verifies mechanically instead | `CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md` |

**No worker may infer authorisation from an old task file.** A task file is not an authorisation;
where it disagrees with a newer Controller decision, the decision wins.

## Settled lanes — all merged, none active (do not restart, re-run or regenerate)

| Lane | One-line result | Spend | Authority (under `coordination/decisions/`) |
|---|---|---|---|
| **EVAL-038** | **Merged / closed.** Weak model + the two compiled packs vs a strong model alone, blind, extended to real media: substitution **refuted 0/6** (18/18 top-3 slots to the baseline), the cheap arm cost **more** per package. Media generated is **product learning only — never Registry evidence**. **Decision authority: the verdict on whether Canon works is reserved to the Controller; no worker concludes further.** `canon/findings/PROPOSED-EVAL-038-CONCLUSION.md` is a proposal, not an adopted finding | **USD 2.260122** of a USD 10.00 cap, 0 retries | `CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md` |
| **REP-07** | **Merged / closed.** 13 inspected candidates admitted; live accepted Canon **24 → 37 sources / 1,300 objects**; `google-abcd` marked `platform_contingent` and `sontag` `critique_context`; three same-work extensions admitted as scoped extensions, never independent origins; `ries` retired for Binet. HOLD now **5** | USD 0 | `CONTROLLER-REP-07-ADMISSION-BATCH-2026-09-01.md` |
| CANON-014 | **Merged / closed.** Full durable Canon reconciliation: 24 accepted sources total, 18 HOLD/candidate sources retained, 1,028 grounded/ungraded/uncalibrated Q&A items; candidate/Q&A retrieval is **not** enabled in ordinary runtime. *(Those two counts are the state as of 30 Aug 2026 and are preserved, not corrected — REP-07 has since taken live Canon to **37 accepted / 5 HOLD**.)* | USD 0 | `CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md` |
| CANON-011 | 18 marketplace-derived buyer cases (Upwork buyer postings only), 16 runnable; preferred real-demand pool for Stage-C; grammar **not** reopened (GG-01…GG-04 observations only); `MKT-015` blocked evidence only | USD 0 | `CONTROLLER-CANON-011-INTEGRATION-2026-08-28.md` |
| EVAL-024 | 16/16 A-TEXT coordinates generated and **sealed as committed bytes** — durable evidence, **do not regenerate** (manifest fingerprint `1e124343…`) | USD 0.904 | `CONTROLLER-EVAL-024-INTEGRATION-2026-08-28.md` |
| EVAL-029 | Cloud Vision `TEXT_DETECTION` (no language hints) **benchmark-qualified** on Devanagari and Latin; **strict-exactness disqualified**; evidence sealed, recomputable from a fresh clone | USD 0.4320 | `CONTROLLER-EVAL-029-REVIEW-SEAL-EVIDENCE-BEFORE-MERGE-2026-08-28.md` |
| EVAL-030 | The exact sealed images scored without regeneration: GPT Image 2 **6/8**, Ideogram v3 **1/8**, overall **7/16** — directional signal, not certification. **Registry stays 0** | USD 0.024 | `CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md` |
| EVAL-026 | Temporal qualification **machinery only**: 13 perturbation types over all 9 frozen `temporal_video` capabilities (7 full, 2 negative-direction-only). No evaluator qualified, no pass mark | USD 0 | `CONTROLLER-EVAL-026-INTEGRATION-2026-08-28.md` |
| RES-005 | 12 rights-cleared clips from 12 distinct works, 12/12 clean screen; **only 3/3 representative ingest** (not 12/12); role `MAT-TEMPORAL-BASE`, not `PACK-AV-CLEAN` | USD 0 | `CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md` |
| GOV-005 | Closed and merged (PR #48); do not reopen for parallel-lane drift | — | `CONTROLLER-GOV-005-CLOSURE-AND-GOV-006-TRIGGER-2026-08-28.md` |
| EVAL-012…016 (EMP-001 machinery) | Execution implementation accepted and integrated: persistent spend ledger, mechanical caps, ambiguous-dispatch semantics (pre-dispatch may release headroom; ambiguous post-dispatch must not, retries 0, fail-closed), fingerprint-bound qualification→A-TEXT handoff | USD 0 | `CONTROLLER-EVAL-012…016-REVIEW-*.md` |

## Current empirical floor

**Still zero:** qualified models/workflows · qualified subjective/perceptual evaluator families ·
strict-exactness-qualified text evaluators (5 tested, 5 disqualified, unrewritten) · qualified
temporal evaluators (pass mark `DOES_NOT_EXIST`) · **Capability Registry rows** (0 — deliberate;
verified: 0 data rows, validator passes) · customer-outcome CpAO observations · Production IR /
Planner · **the mechanical acceptance gate** (pre-dispatch and post-draw checks as code: designed
in `canon/CANON-SHAPE-v1.md` §4, **not built**) · **accepted-outcome-rate measurements** (none
commissioned) · **8 of the 10 compiled packs**.

**EVAL-038 moved none of those zeros.** It produced real media and the Controller judged it, but
that authority labelled media generation **product learning only — never Capability Registry
evidence**. EVAL-038 artifacts are not a qualified model, not a qualified evaluator, not a Registry
row, and not a customer-outcome CpAO observation.

**No longer zero:**

- **1 benchmark-qualified text evaluator** — Cloud Vision `TEXT_DETECTION`, no language hints,
  under `benchmark_text_ocr_v1`: Devanagari false-pass 0.1250 / false-fail 0.0208 / consistency
  1.0; Latin 0.1042 / 0.0000 / 1.0. Still `strict_exactness_qualified: false`. Benchmark
  qualification never certifies an individual output as exact.
- **16 A-TEXT generations**, sealed and scored **7/16 exact**.
- **12 real temporal base clips**, rights-cleared, 12/12 clean.
- **5 instrument configurations scientifically disqualified** under the strict standard, with the
  literalness mechanism finding attached (`history/EMP-001.md`).
- **EVAL-037 programme conclusion:** Canon is worth carrying forward, while the current retrieval / consumption protocol is not mature. This is a bounded programme-direction conclusion, not a universal quantified treatment effect and not Registry evidence. See `eval/experiments/EVAL-037/CONCLUSION.md`.
- **Canon corpus expanded (REP-07):** **37 live accepted sources · 1,300 SourceKnowledge objects ·
  132 concept systems · 291 bindings**, with **5 HOLD** (desai, airey, freeman-beyond, samara-ch2;
  ries retired). Recompute with `python3 canon/validation/validate_audit_gate_v02.py` — 37 records,
  0 errors. `google-abcd` carries a `platform_contingent` marker and `sontag` a `critique_context`
  marker; three same-work extensions are scoped extensions, never independent origins. **2 of 10
  compiled packs** exist. The 1,028 grounded, ungraded, uncalibrated Q&A items remain. The separate
  accepted/full/Q&A fingerprints are in
  `canon/knowledge/CANON-CORPUS-INDEX.yaml`. HOLD material remains non-accepted and ordinary
  runtime retrieval remains `canon/knowledge/current/**` only. **The live count is 37; the
  CANON-003 method-test corpus stays 16, fixed forever — never confuse the two.**
- **EVAL-038 evidence exists and the substitution question is answered:** 0/6, refuted, committed
  and never to be rewritten; the pack-guided image won the B06 pair; the compiled doctrine forbids
  both PILOT-001 candidates the Controller rejected. **Whether Canon works remains the Controller's
  call.** Evidence: `eval/experiments/EVAL-038/`.

**The Registry is empty deliberately.** `benchmark_qualified` is weaker than the Registry's
`qualified`/`deterministic` admission bar; **admission must not be weakened to create a first row**
(`coordination/decisions/CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md`).

**Important reset clarification (29 Aug): Registry = 0 does NOT mean empirical workflow memory = 0.**
The Controller has reviewed recovered Media Factory evidence containing dated historical workflow/model
observations (including a 64-item human-scored still set). These are to be imported as **historical
empirical priors**, not current Registry rows, under
`CONTROLLER-PROGRAMME-RESET-MEDIA-FACTORY-PRIORS-2026-08-29.md`.

**A-TEXT manual review is not project evidence.** Any human re-reading of the 16 images outside
GitHub must not be recorded or used for a Registry row without a new explicit Controller decision.
The accepted result is the OCR-observed 7/16.

## Spend authority

| Item | Figure | Authority |
|---|---|---|
| EMP-001 ceiling (user-approved, **covers EMP-001 only**) | **USD 10.00** total; USD 6.00 qualification sub-cap; 0 retries; no pre-funding above ceiling | `coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md` |
| Recorded cumulative through EVAL-024 | **USD 2.6397905** | sealed generation manifest + EVAL-024 decision |
| EVAL-030 evaluator stage | USD 0.024 | sealed scoring evidence + EVAL-030 decision |
| EVAL-038 (extended to media) ceiling — **spent, not renewed** | **USD 10.00** authorised; **USD 2.260122 consumed**, 0 retries, no cap breach (ledger conservatively 2.760122 with an annotated phantom entry) | `coordination/decisions/CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md` |
| Stage-A 90-generation planning estimate (~USD 52 + ₹4.50 Sarvam) | **Unapproved** | `CONTROLLER-VEO-PRICING-UNIT-CORRECTION-2026-08-26.md` (per-second Veo pricing) |

No committed artifact states a cumulative total including EVAL-030's USD 0.024 (GOV-006 **G6-02**,
routed). The mechanical ceiling and sub-cap are enforced by the live ledger, which stays local by
design. **Any tranche beyond EMP-001 needs explicit user approval.**

## Frozen foundations (unchanged)

CANON-010 request contract · Capability Contract v2 (**44 = 43 active + 1 dormant**) · 13 condition
families · 12 core + 2 reserve scientific slots · Resources topology v3 / CpAO v3 / four
controlled-pack families · EVAL-011 staged design (Q=0, A=90, B≤404, C=32 outcome attempts) ·
EMP-001's frozen paid shape and its results (complete; **not** an authorisation to re-run —
`history/EMP-001.md`). Several merged contracts still carry stale `NOT IN FORCE` status headers;
this file governs.

## Still blocked / not authorised

- Mandatory human-in-the-loop exact-text review in the production API architecture (withdrawn
  28 Aug 2026);
- treating benchmark-grade OCR as a perfect exactness certifier;
- Registry population from text metrics — **decided: no** (see above);
- any temporal checker qualification run — requires all four: a selected checker; **full 12-clip
  ingest** under a recorded execution condition; Controller-approved numeric pass marks frozen
  **before** observations; preserved human adjudication wherever the frozen
  `EVALUATOR-QUALIFICATION-MAP.yaml` says `model_based_plus_human` (**five** capabilities);
- reopening the Media Request Grammar because CANON-011 observed GG-01…GG-04;
- regenerating any sealed A-TEXT artifact;
- importing the chat-only manual A-TEXT review as project truth;
- further Tesseract/OCR configuration sweeps without a new mechanism-level rationale
  (general-purpose multimodal LLMs stay frozen as the strict exact-text judge family);
- broad Stage-B/C execution without their own instrument readiness;
- broad controlled-pack acquisition;
- Production IR / Planner implementation before sufficient empirical capability evidence exists;
- **rerunning the refuted EVAL-038 substitution configuration** to reconfirm it;
- **any worker conclusion on whether Canon works** — that verdict is reserved to the Controller;
- **building the gate, injection v1, the template library, or any further pack** — the shape
  document's open-work list is a queue, not an authorisation;
- **any acceptance-rate / accepted-outcome measurement run** — not yet commissioned;
- **further paid execution under the EVAL-038 authority** — it is spent and not renewed.

### Temporal material contract (resolved, pack-level)

The family-4 content requirement is **pack-level** — an individual clip needs only the feature its
perturbation requires. Opportunity counts (coverage counts, never precision claims): base 12,
multi-shot 6, on-screen text 6, product region 5, rendered-character identity 4, photographed-face
identity 3 — **the two identity populations must not be pooled**.
Authority: `coordination/decisions/CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md`.

## Next gate

**The next gate is the gate build:** derive the pre-dispatch and post-draw checks as code from
PA-D1..D10 and CA-D1..D11, baked-text scan first (`canon/CANON-SHAPE-v1.md` §7 item 1). This is the
next build **when the Controller directs it** — nothing in this file or in the shape document
authorises it yet.

**`canon/CANON-SHAPE-v1.md` is the governing consumption shape** for Canon, adopted by the
Controller under `CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md`. It settles what Canon is,
what it is for, and how it is consumed. It carries **no verdict on whether Canon works**, and
adoption adds none.

1. **EVAL-037 / T2B is concluded for programme direction.** Canon remains in the product thesis; the current retrieval / consumption mechanism is explicitly not accepted as production-ready.
2. **EVAL-038 is settled.** The substitution question is closed for the configuration tested. The
   verdict on Canon is the Controller's, to be measured rather than argued; the cheapest decisive
   measurement available is an acceptance-rate run (many draws per arm, blind accept/reject), which
   the Controller may commission and which is **not** authorised here.
3. **Return to Controller planning mode before authorising more execution.** Rebase the T3-T8 path around the shortest route to a working end-to-end accepted-outcome system, rather than another broad research tranche.
4. **No new paid execution, media propagation, retrieval experiment, Production IR implementation, or Planner implementation is authorised by the EVAL-037 conclusion, the EVAL-038 disposition, or the adoption of CANON-SHAPE-v1.**
5. **EVAL-036 / T2A remains an authorised USD-0 historical-prior import, but it is no longer an automatic prerequisite to every next product step.** Its place in the rebased programme must be decided for outcome value, not because an older sequence says so.
6. **The next programme plan must preserve the final product chain:** customer request -> intelligence/Canon -> production specification -> route selection -> execution -> evaluation -> bounded repair -> accepted outcome -> empirical memory.
7. **Primary decision metrics remain accepted-outcome rate, CpAO, repeatability, and incremental value over the strongest simpler baseline.**
8. HED-1 remains undecided and must be resolved before fully-loaded holdout/Stage-C CpAO scoring.
