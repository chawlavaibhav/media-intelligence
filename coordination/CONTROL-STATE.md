# Controller State

**The single primary operational current-state document.** It answers: what is active, authorised,
deferred, cancelled; the current empirical floor; Registry state; spend authority; blockers; and the
next Controller gate. It is a synthesis backed by the durable Controller decisions it links — where
it and any older prose disagree, the latest durable Controller decision governs.

**Updated:** 28 Aug 2026 — post context-architecture migration, with the revised outcome-first
programme and zero-spend pre-pilot tranche authorised by
`CONTROLLER-REVISED-PROGRAM-AND-PREPILOT-TRANCHE-2026-08-28.md`. The previous full text is preserved
at `history/CONTROL-STATE-PRE-CONTEXT-MIGRATION-2026-08-28.md`; the last Governor reconciliation
was GOV-006 (`governance/reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`).

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
| Canon value gate | Unrun | — |

**No worker may infer authorisation from an old task file.** A task file is not an authorisation;
where it disagrees with a newer Controller decision, the decision wins.

## Settled lanes — all merged, none active (do not restart, re-run or regenerate)

| Lane | One-line result | Spend | Authority (under `coordination/decisions/`) |
|---|---|---|---|
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
verified: 0 data rows, validator passes) · accepted Canon-improves-outcomes evidence ·
customer-outcome CpAO observations · Production IR / Planner.

**No longer zero:**

- **1 benchmark-qualified text evaluator** — Cloud Vision `TEXT_DETECTION`, no language hints,
  under `benchmark_text_ocr_v1`: Devanagari false-pass 0.1250 / false-fail 0.0208 / consistency
  1.0; Latin 0.1042 / 0.0000 / 1.0. Still `strict_exactness_qualified: false`. Benchmark
  qualification never certifies an individual output as exact.
- **16 A-TEXT generations**, sealed and scored **7/16 exact**.
- **12 real temporal base clips**, rights-cleared, 12/12 clean.
- **5 instrument configurations scientifically disqualified** under the strict standard, with the
  literalness mechanism finding attached (`history/EMP-001.md`).

**The Registry is empty deliberately.** `benchmark_qualified` is weaker than the Registry's
`qualified`/`deterministic` admission bar; **admission must not be weakened to create a first row**
(`coordination/decisions/CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md`).

**A-TEXT manual review is not project evidence.** Any human re-reading of the 16 images outside
GitHub must not be recorded or used for a Registry row without a new explicit Controller decision.
The accepted result is the OCR-observed 7/16.

## Spend authority

| Item | Figure | Authority |
|---|---|---|
| EMP-001 ceiling (user-approved, **covers EMP-001 only**) | **USD 10.00** total; USD 6.00 qualification sub-cap; 0 retries; no pre-funding above ceiling | `coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md` |
| Recorded cumulative through EVAL-024 | **USD 2.6397905** | sealed generation manifest + EVAL-024 decision |
| EVAL-030 evaluator stage | USD 0.024 | sealed scoring evidence + EVAL-030 decision |
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
- Production IR / Planner implementation before sufficient empirical capability evidence exists.

### Temporal material contract (resolved, pack-level)

The family-4 content requirement is **pack-level** — an individual clip needs only the feature its
perturbation requires. Opportunity counts (coverage counts, never precision claims): base 12,
multi-shot 6, on-screen text 6, product region 5, rendered-character identity 4, photographed-face
identity 3 — **the two identity populations must not be pooled**.
Authority: `coordination/decisions/CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md`.

## Next gate

1. **PILOT-001 Candidate 1 is human-rejected**: deterministic text/brand passed, but H1/H4/H6 failed
   because the Veo plate was not premium, did not hold, and had no coherent visual meaning.
2. **The single authorised repair is now allocated to one final provider regeneration** under
   `CONTROLLER-PILOT-001-CANDIDATE-1-REJECTION-AND-REPAIR-2026-08-28.md`. Attempt 2 may consume
   another provisional USD 0.80 within the existing USD 2.00 cap. 0 retries; no third provider call.
   **The segmented repair prompt in that decision was withdrawn before dispatch**; the current
   frozen Attempt 2 prompt is the single-scene prompt in
   `CONTROLLER-PILOT-001-ATTEMPT-2-PROMPT-SUPERSESSION-2026-08-28.md`, with the execution packet at
   `coordination/plans/2026-08-28-PILOT-001-ATTEMPT-2-EXECUTION-ADDENDUM.md`.
3. **After Candidate 2, no repair remains.** Human-review it once; PASS closes T1 with an accepted
   outcome, FAIL closes T1 as a bounded product/integration failure.
4. **Before architecture-test media exists**, freeze the representative-deliverable policy,
   development/holdout split and decision protocol. CANON-013's merged 8/8 split remains only a proposal.
5. **Registry text rows stay blocked**; admission semantics stay as they are.
6. **Temporal/identity/speech evaluator qualification remains deferred** until a real product or
   Registry decision depends on those automated measurements.
7. **Prices remain incomplete** — execution-time route/price verification is required before each
   paid tranche; no broad price-refresh task is authorised.
8. **HED-1 remains undecided** and must be resolved before fully-loaded Stage-C CpAO is scored.
9. **Stream-owned staleness** routed by GOV-006 remains non-blocking; this file governs where stale
   handoffs/spec prose disagree with current decisions.
