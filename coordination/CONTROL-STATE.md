# Controller State

**The single primary operational current-state document.** It answers: what is active, authorised,
deferred, cancelled; the current empirical floor; Registry state; spend authority; blockers; and the
next Controller gate. It is a synthesis backed by the durable Controller decisions it links — where
it and any older prose disagree, the latest durable Controller decision governs.

**Updated:** 15 Sep 2026 — production-learning integration of the Upwork intro pilot (branch
`work/production-learning-upwork-intro-001`, **PR #98** open, not merged): see §1 "First accepted commercial
showcase asset" and §5 E. Previous refresh 14 Sep 2026 (second of the day) — **PR #95 and PR #96 merged to `main`** on the
Controller's instruction ("Merge #95 then #96"): `main` = `bf92c53` (PR #96's merge commit; PR #95's is
`191a224`). Earlier the same day: the full Governor refresh ordered by ruling C-6
(`coordination/decisions/CONTROLLER-GOVERNOR-REFRESH-ORDER-2026-09-14.md`) after the 10-Sep audit's
fifteen open items were ruled on and the derivative routing map and taint register were regenerated
under those rulings. The text immediately before the first refresh is preserved byte-for-byte at
`history/CONTROL-STATE-PRE-AUDIT-CLOSEOUT-REFRESH-2026-09-14.md` (earlier snapshots:
`history/CONTROL-STATE-PRE-CAPABILITY-LAB-2026-09-08.md`, `…-PRE-GATE-001-REFRESH-2026-09-07.md`,
`…-PRE-EVAL-038-REFRESH-2026-09-01.md`, `…-PRE-CONTEXT-MIGRATION-2026-08-28.md`).

**Governing decisions of 14 Sep 2026** (all under `coordination/decisions/`; each quotes the
Controller's words verbatim and states what it does not authorise):

| Record | Rules on |
|---|---|
| `CONTROLLER-AUDIT-CLOSEOUT-CAP-CROSSINGS-AND-CALL-LIMIT-2026-09-14.md` | C-1 (two cap crossings accepted as recorded), C-5b (19-vs-16 call limit accepted as recorded), C-2 (caps enforced against the ledger at dispatch; vendor billing is a separate reconciliation field) |
| `CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS-2026-09-14.md` | C-3 (frozen elimination rule applied literally), C-4 (affected human cells are descriptive until recomputed or replaced), C-6b (strict: a failed draw stays a failure; RR-16 withdrawn), C-6c (two exact-text mechanisms, two route identities; RR-1 rewritten), C-6d (elimination per route and question) |
| `CONTROLLER-AUTHORISATION-LINEAGE-CUMULATIVE-BUDGET-2026-09-14.md` | C-6a (an amendment never resets consumed spend) |
| `CONTROLLER-GOVERNOR-REFRESH-ORDER-2026-09-14.md` | C-6 (this refresh) |
| `CONTROLLER-ALPHA-1-PRODUCT-FAMILY-AND-RELEASE-POLICY-2026-09-14.md` | C-7 (Alpha 1 frozen), C-8 (human approval before every external delivery), C-11 (twelve-condition public-release gate) |
| `CONTROLLER-CAPABILITY-LAB-STOP-WIDENING-AND-CANON-INJECTION-V1-2026-09-14.md` | C-9 (stop widening the Lab), C-10 (USD-0 Canon Injection v1 + template/empirical memory authorised; no further packs) |

The Controller's rider applies to every one of them: **adopting the Alpha policy is NOT spend
authorisation; no paid dispatch is authorised by any 14-Sep decision.** Earlier direction still in
force: `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` (as narrowed by C-9),
`CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md`, `CONTROLLER-EVAL-038-…-2026-09-01.md`,
`CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`, `CONTROLLER-PROGRAMME-RESET-MEDIA-FACTORY-PRIORS-2026-08-29.md`.

**Read `PROJECT-MEMORY.md` first.**

## 1. Where the work is (14 Sep 2026, after the merges)

- **`main` = `bf92c53`.** It carries everything from the 8–10 Sep Capability Lab run, the 10-Sep
  audit, the 14-Sep closeout (PR #95, merge `191a224`) and the 14-Sep runtime vertical slice (PR #96,
  merge `bf92c53`). Both integration branches are merged and finished; no branch of this tranche is
  outstanding.
- **The production runtime is on `main`** (`runtime/`): intake against PRODUCTION-JOB-v1; brief →
  PRODUCTION-SPEC-v1 with deterministic Canon lookup and a USD-0 reasoning pass (frozen Stage-A
  blueprint, recorded fixture, or promoted template); Canon Injection v1; the evidence-aware router;
  the execution bridge (`EXECUTION-MANIFEST-v0`, harness `dry_run()`, nothing sent); pre-dispatch and
  post-draw gates over `canon.gate`; bounded repair; human-acceptance states; the OUTCOME-EVENT-v1
  store; the template library; and the one-command chain `python3 -m runtime.alpha.cli`. **Every run to
  date is dry; the runtime has never called a provider.** Entry points for a new engineer:
  `runtime/ALPHA-1.md`, then `coordination/audits/HANDOFF-USD0-TRANCHE-2026-09-14.md` (refs, defects,
  the 14-run dry battery, blockers, the first-paid-tranche recommendation).
- PR #94 (`work/audit-brief-2026-09-10`, the audit brief itself) is still open and untouched.
- **First human-accepted real commercial showcase asset exists (14 Sep 2026).** The Upwork profile
  introduction film **V4.1** (`pilots/upwork-intro-video-2026-09-14/v4/assembly/v4.1/upwork-intro-v4.1.mp4`,
  sha256 `d1a5edf8…e008a`, 57.1 s, commit `f6ca66f` on `work/pilot-upwork-intro-video-v4`) was
  **ACCEPTED by the Controller** after V1 (specific repair) → V2 (rebuild) → V3 (reject) → V4 (specific
  repair). It was produced **outside the narrow Alpha-1 family** (speaking presenter, multi-shot) by pilot
  scripts, not by `runtime/alpha`, under the Controller's own pilot spend packages (INR 3,000 then INR
  2,000). Reconciled provider spend **USD 15.39318** (V1+V2 8.082 · V3 3.28358 · V4 4.0276 · V4.1 0; the
  "USD 7.31" in the final pilot report covers V3–V4.1 only). **TTAO ≈ 7–8 h (Controller estimate;
  mechanical lower bound 7 h 54 m from session start to the V4.1 file).** Two conclusions, never blended:
  **final quality succeeded; pipeline efficiency did not.** Durable record:
  `production-learning/cases/UPWORK-INTRO-001/` (outcome, human verdicts, revision trace, time + cost,
  system defects, route observations, accepted template, promotion queue, evidence map) and
  `coordination/audits/UPWORK-INTRO-PILOT-EVIDENCE-INVENTORY-2026-09-14.md`. **The raw pilot branch is
  on origin** (`origin/work/pilot-upwork-intro-video-v4` = `f6ca66f`, pushed 15 Sep unrewritten); it is
  never merged to `main`. **This does not prove commercial
  advantage** over a direct human + LLM workflow; it is the baseline the next real production is measured
  against.

## 2. Active / authorised

| Item | What is authorised | Spend authority |
|---|---|---|
| **Alpha 1 product family** (C-7) | One static commercial ad with exact **overlay** copy (text composed by code onto a textless plate — exact-text mechanism B), optionally followed by one short motion version derived **only** from the accepted still. Supplied-photo work is conditional behind the identifiable-person / consent gate. Excluded: talking heads, lip-sync, native speech, multi-shot stories, generated in-scene exact text. Encoded as data in `runtime/contracts/POLICY-PROFILES.yaml` (`alpha_human_release`, `adopted: true`); described for a new engineer in `runtime/ALPHA-1.md` | **None.** `spend_authority.status: none` on every profile. Adoption is a policy agreement, not money |
| **Human release** (C-8) | Every Alpha-1 output needs human approval before external delivery; no autonomous external delivery; the automated judge is out of the release path (agreement 66 %, false-accept 22 %) | — |
| **Public-release gate** (C-11) | Auditor A's twelve T8 conditions adopted as the bar for public delivery; held as data on the alpha profile. **None of the twelve is met today** | — |
| **Canon Injection v1 + template / empirical-memory integration** (C-10) | USD-0 implementation only, following `canon/CANON-SHAPE-v1.md` §4: deterministic pack lookup, accepted Canon only, stable cached prefix, no compliance receipts, mechanical gates, accepted blueprint → reusable template. **The remaining eight packs are not compiled** unless a real runtime failure demands one | USD 0; no tokens, no model, no provider call to "prove" it |
| **Runtime engineering at USD 0** | Everything now on `main` under `runtime/`: contracts, intake, spec compiler, router, dry execution, gates, repair/acceptance states, memory event, CLI, dry battery. The `dry` operating profile sends nothing | USD 0 |
| **Capability Lab** (C-9) | **Stopped widening.** No generic model battery, no premium-model sweep, no expansion to make tables prettier. New evidence work only when the production runtime exposes a launch-critical hole. The 8-Sep direction stands only as narrowed here | **Not authorised** — every Group-3 item (C-12 cheapest-tier round, C-13 Gemini API smoke, C-14 judge v2, C-15 clean reruns, C-16 still round two, C-17 Stage B, C-18 Stage C) needs its own signed spend record; none exists |

Merged and closed earlier (unchanged): CANON-012, CANON-013, EVAL-035, RES-007, PILOT-001 freeze
and its USD 2.00 authorisation (never executed under the runtime; the PILOT-001 recipe is superseded
in practice by the Alpha-1 family but its record is not withdrawn).

## 3. Stopped / deferred / cancelled

| Item | Disposition | Authority (under `coordination/decisions/` unless noted) |
|---|---|---|
| Capability Lab widening (further battery rounds, premium sweep, "prettier tables") | **Stopped** | `CONTROLLER-CAPABILITY-LAB-STOP-WIDENING-AND-CANON-INJECTION-V1-2026-09-14.md` (C-9) |
| The "next gates" listed on 10 Sep (cheapest Wan/Kling floor round, Seedance on the bottle briefs, judge v2, still round two, Gemini API adapter smoke) | **Not gates any more.** Recorded as Group-3 items C-12…C-18; each is authorised only by its own future spend record, and only where the runtime exposes a launch-critical hole | same |
| Compiling the remaining eight Canon packs | **Not authorised** unless a real runtime failure demands one | same (C-10) |
| EVAL-031 | Stopped — do not start as written | `CONTROLLER-PARALLEL-EMPIRICAL-UNBLOCK-CORRECTION-2026-08-28.md` |
| EVAL-032, EVAL-033 | Stopped as immediate priorities | `CONTROLLER-STOP-TEMPORAL-PREP-PRIORITISE-PRODUCT-PILOT-2026-08-28.md` |
| EVAL-034 | Cancelled | `CONTROLLER-PARALLEL-EMPIRICAL-UNBLOCK-CORRECTION-2026-08-28.md` |
| RES-006 | Deferred | same |
| EVAL-028 | Cancelled — must not be executed | `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md` |
| EVAL-006 | Paused; spend authority withdrawn | `CONTROLLER-PAUSE-EVAL-006-PENDING-MASTER-PLAN-2026-08-26.md` |
| GOV-007 | Not authorised | `CONTROLLER-STOP-TEMPORAL-PREP-PRIORITISE-PRODUCT-PILOT-2026-08-28.md` |
| EVAL-038 substitution configuration | Closed — refuted 0/6; the verdict on whether Canon works stays reserved to the Controller | `CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md` |
| Forced-consumption receipt schema (`INJECTION-CONTRACT-v0.md` §1) | Retired as a production mechanism; the gate verifies mechanically | `CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md` |

**No worker may infer authorisation from an old task file.** Where a task file, handoff or summary
disagrees with a newer Controller decision, the decision wins.

## 4. Settled lanes — all merged, none active (do not restart, re-run or regenerate)

| Lane | One-line result | Spend | Authority |
|---|---|---|---|
| **EVAL-040…043 (the two-day Capability Lab run, 8–10 Sep)** | 35/35 Stage-A package cases run and judged; 311 sealed media re-hash exactly; **575 deterministic Registry rows** (validator PASS); routing map 61 cells + RR-1…RR-16, **regenerated 14 Sep under the rulings** (see §5); vision judge screened, **not qualified** (kappa 0.33, false-accept 22 %) | ledger **USD 122.241262** counted against caps (see §6) | PRs #90–#93; spend records `CONTROLLER-SPEND-AUTHORISATION-*-2026-09-0[89].md`, `…-WAN2-CONTENDER-ROUND-2026-09-10.md` |
| **Audit of 10 Sep 2026** | Two independent audits; nine zero-spend repairs; four re-runnable tools (`coordination/audits/tools/`: `reconcile_spend.py`, `recompute_elimination.py`, `verify_price_pins.py`, `build_taint_register.py`) plus `verify_sealed_evidence.py` (14 Sep); fifteen open items → **all ruled 14 Sep** | USD 0 | `coordination/audits/HANDOFF-TO-CONTROLLER-2026-09-10.md` (corrected 14 Sep) and the six 14-Sep records |
| CANON-GATE-001 | Compiled-doctrine gate as code (`canon/gate/`); 21 check lines by id; blocking set = baked-text guard, delivered-vs-declared, named-ratio, integrity, extraction errors; a PASS is structure, never quality | USD 0 | `CONTROLLER-CANON-GATE-001-MERGE-2026-09-07.md` |
| EVAL-038 | Weak model + two packs vs strong model alone: refuted 0/6; media is product learning only | USD 2.260122 | `CONTROLLER-EVAL-038-…-2026-09-01.md` |
| REP-07 | Live accepted Canon 24 → **37 sources / 1,300 objects**; HOLD 5 | USD 0 | `CONTROLLER-REP-07-ADMISSION-BATCH-2026-09-01.md` |
| CANON-014, CANON-011, EVAL-024, EVAL-029, EVAL-030, EVAL-026, RES-005, GOV-005, EVAL-012…016 | unchanged from the 9-Sep state; see `history/CONTROL-STATE-PRE-AUDIT-CLOSEOUT-REFRESH-2026-09-14.md` §"Settled lanes" for the one-line results | as recorded there | as recorded there |

## 5. Current empirical floor — four kinds of evidence, never mixed

**A. Deterministic Registry evidence (unchanged by every 14-Sep ruling).** `eval/registry/registry-v1.jsonl`:
**575 rows over 61 cells**, every row `evidence_tier: deterministic` under the frozen criteria
(`CONTROLLER-INSTRUMENT-THRESHOLDS-FROZEN-2026-09-09.md`); five capabilities only
(delivery_format_compliance, reliability_pass_at_k, latency_errors_refusals, cost_and_cpao,
reproducibility); every row `independence NOT ESTABLISHED` — reference calculations, not statistics;
524 of 575 rest on a single base item. The rows record the failures the run files excluded (they never
read a human verdict), and where a trial identity was sent twice the Registry holds two rows,
distinguishable by `run_ids`, which must never be added together. Recompute:
`python3 eval/registry/validate_registry.py`. **Human acceptance never enters the Registry.**

**B. Clean human-routing evidence.** `eval/capability-map/TAINT-REGISTER-v1.yaml` (regenerated 14 Sep
under C-3/C-4/C-6b/C-6c/C-6d; `build_taint_register.py --check` = UNCHANGED): **36 of 61 cells
`clean_observed`** (the literal frozen rule reproduces the number from sealed files, every named
problem disposed of by a listed ruling, ≥ 4 settled draws). **Production use allowed on 29 cells**; the
runtime's `alpha_human_release` profile auto-routes **26 of 61** (the 29 minus the three audio cells the
router cannot price by duration). Every `clean_observed` number is 4–8 draws judged by one person —
honest evidence, not proof, and never a launch clearance.

**C. Directional / descriptive product evidence.** **25 cells `directional_only`** (fewer than four
settled draws; a person routes them — `production_use_allowed: manual_only`, 15 cells — or they are
eliminated). Plus the **descriptive re-sends** retained under C-4/C-6b: the six successful Wan 2.2 A14B
image-to-video re-sends (5 of 6 accepted) live in the map cell as `descriptive_resends`, labelled "not
counted", never deleted. Plus every EVAL-038 artifact and the 64-item Media Factory prior
(`eval/historical-priors/media-factory-v1/`): product learning, never Registry evidence.

**D. Tainted / awaiting / eliminated.** **0 cells awaiting a Controller ruling; 0 `method_tainted`.**
**17 cells are eliminated on their question under the frozen rule** (`production_use_allowed: false`),
including VID-I2V/`wan-2.2-a14b-i2v` (2/8 with six HTTP-422 failures counted — E1 and E2),
VID-T2V/`kling-v3-pro-audio` (2/8, E2) and VID-2SPK/`kling-v3-pro-audio+A_native` (0/2 with two
failures, E1 and E2). **`replacement_needed: true` on exactly those three**: their elimination rests on
failures the run classified as infrastructure or request-shape faults; no ruling can re-test them —
only a clean rerun (Group-3 item C-15, not authorised).

**Routing rules after the rulings.** **RR-16 is withdrawn** as Stage-A image-to-video routing truth
(`status: withdrawn_as_stage_a_i2v_routing_truth (C-6b)`); Wan 3.0 Prime remains the Wan tier for
image-to-video (RR-8). **RR-1 now says what was accepted:** a FLUX.2 Pro textless plate onto which
deterministic code composed the exact strings, 4/4 — the image model did not render the accepted copy;
the same plates judged bare were 1/4 (eliminated). The two IMG-TEXT cells carry distinct route identities
(`flux-2-pro` mechanism `model_draws_text`; `flux-2-pro+code_overlay` mechanism
`deterministic_text_composition`) and every map cell carries `text_mechanism`. RR-15's fractions are the
literal ones (2/8, 5/8, 4/8); its advice is unchanged. RR-11/RR-12 keep their per-case advice; the
routes are kept on their questions (C-6d). Regenerate: the commands in
`coordination/audits/AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` §Addendum.

**Still zero:** qualified models/workflows · qualified subjective/perceptual evaluator families ·
strict-exactness-qualified text evaluators (5 tested, 5 disqualified) · qualified temporal evaluators
(pass mark `DOES_NOT_EXIST`) · customer-outcome CpAO observations · **accepted-outcome-rate
measurements** (none commissioned) · **8 of the 10 compiled packs** (and none will be compiled without a
real runtime failure — C-10) · post-draw text detection on a real artifact (Cloud Vision adapter wired,
never invoked) · any real (non-dry) run of the production runtime · vendor-billed cost (§6).

**No longer zero (unchanged from 9 Sep unless marked):** 1 benchmark-qualified text evaluator (Cloud
Vision `TEXT_DETECTION`, `benchmark_text_ocr_v1`; still not strict-exactness qualified) · 16 sealed
A-TEXT images scored 7/16 · 12 rights-cleared temporal base clips · EVAL-037 programme conclusion
("Canon helps; retrieval/consumption not mature") · 37 accepted Canon sources / 1,300 objects / 2 of
10 compiled packs · the compiled-doctrine gate as code · EVAL-038's committed negative result · **the
575 deterministic Registry rows and the 61-cell routing map (9–10 Sep)** · **a production runtime that
exists as code on the integration branch (14 Sep): intake, brief → Production Specification with
deterministic Canon lookup, evidence-aware router with declared fallback and price pins; every run to
date is dry — no provider has ever been called by the runtime.**

**Two text standards** still exist and every text result must name its standard (strict exactness
certification — nothing has passed; benchmark-grade OCR — Cloud Vision passes). Exact-text imperfection
is not a programme-wide blocker; under Alpha 1 exact copy is composed by code (mechanism B), which is
exact by construction and does not depend on any text evaluator.

**E. Production learning (new, 15 Sep 2026) — never Registry, never Canon.** `production-learning/cases/`
holds real productions' records. UPWORK-INTRO-001: the accepted V4.1 asset; **zero media-model failures
reached the Controller — every defect he named was compositor, orchestration, creative direction, QA
timing or a route choice** (`SYSTEM-DEFECTS.yaml`). Model observations from the job (Veo 3.1 Fast
speaker 1/1 accepted after two transient UNAVAILABLE failures; Gemini Omni 1.1 Flash speaker 0/1, inserted
a word, synthetic timbre; Nano Banana 2 drew paper-like text once; Kling sharpened blurred signage into
letters once; Lyria refused one wording three times) are **directional only** (`ROUTE-OBSERVATIONS.yaml`,
`routing_authority: none`); **no Registry row was created or changed (575), no Canon pack compiled or
edited** — no new Canon source or domain was proven necessary by the pilot. **Deterministic gates
promoted into the runtime from this evidence:** text bounds, contrast with opaque-backing rule,
contain/native/declared-cover fit, one design-token source, critical-region disjointness
(`runtime/compositor/`); video-frame text hygiene — a video's text verdict comes only from sampled frames,
no frames → NOT_RUN never PASS (`runtime/loop/frame_hygiene.py`, wired into the loop and the dry battery);
provider-pool liquidity on the execution manifest (`runtime/execute/pools.py`, additive fields on
EXECUTION-MANIFEST-v0; **fail closed** — an attempt is dispatchable only when its pool is positively known
to fund it, the pool-agnostic answer is `would_dispatch_if_funded`); transient-error classification that can never yield `model_quality_failure`
(`runtime/execute/provider_errors.py`). **Candidate patterns, not policy:** speaker micro-qualification
(test the unresolved speaker route first → human gate → freeze → build), the accepted
`service_intro_with_portfolio_proof` template (pacing values scoped to that one accepted instance), and
**TTAO as a primary production KPI alongside CpAO — ADOPTED by the Controller (PR #98 audit comment,
14 Sep 19:19Z)**; speaker micro-qualification stays a candidate; COMPLEX-PRODUCTION-EVENT deferred until
after the second complex real production.
OUTCOME-EVENT-v1 is **not** mutated — it cannot represent a five-version, nine-route, assembly-repaired
production honestly; a COMPLEX-PRODUCTION-EVENT is a design candidate after a second complex run.
**Next real productions measure TTAO from the first production input and record the ACCEPT timestamp.**

## 6. Spend authority and spend of record

| Item | Figure | Authority |
|---|---|---|
| **All Capability Lab spend, 8–10 Sep 2026** (ledger consumed, conservative, USD-equivalent across pools) | **USD 119.085109** across the run ledgers (cash USD 77.5235 on fal; cloud credits USD 41.5522; Sarvam ₹0.894; 1,198 ElevenLabs plan credits) **+ USD 3.156153** vision judge outside every run ledger **= USD 122.241262 counted against caps.** USD 108.9706 produced a sealed artifact; USD 10.1145 produced nothing (the upper bound on money vendors may never have billed) | `python3 coordination/audits/tools/reconcile_spend.py`; `AUDIT-2026-09-10-SPEND-RECONCILIATION.md` (+ 14-Sep addendum) |
| **Two cap crossings** — video piece 1 USD 10.364 vs 9.96; Wan 2 round USD 11.840 vs its final 11.53 | **Accepted as recorded (C-1).** History preserved; nothing annulled. Mechanism fixed: the ledger pools spend per authorisation and, since 14 Sep, per **budget lineage** (`budget_id` / `amends`) so an in-place cap amendment can never reset consumed spend (C-6a; replay test shows the 11.53 crossing would now be refused) | `CONTROLLER-AUDIT-CLOSEOUT-CAP-CROSSINGS-AND-CALL-LIMIT-2026-09-14.md`; `…-AUTHORISATION-LINEAGE-CUMULATIVE-BUDGET-2026-09-14.md`; `eval/harness-v2/ledger.py` |
| **19 paid calls against a "≤ 16" record** (stand-in picture run) | **Accepted as recorded (C-5b).** `max_paid_calls` is now enforced across the pooled runs | same record |
| **Vendor-billed cost** | **Not reconciled.** No statement is filed; `reconcile_spend.py` prints the column as "not reconciled" and exits 0. Caps are enforced against the ledger, never against a bill (C-2). The four statements (fal, Google Cloud, Sarvam, ElevenLabs) still need one reading; who reads them is not settled | C-2 record |
| EMP-001 (Aug) | USD 2.6397905 through EVAL-024 + USD 0.024 EVAL-030 under a USD 10.00 ceiling | `CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md` |
| EVAL-038 | USD 2.260122 of USD 10.00; spent, not renewed | `CONTROLLER-EVAL-038-…-2026-09-01.md` |
| **Upwork intro showcase pilot (14 Sep 2026, outside the Lab and the runtime)** | **USD 15.39318 reserved at pinned prices across three pilot ledgers** (V1+V2 USD 8.082 under the INR 3,000 record; V3 3.28358 + V4 4.0276 under the INR 2,000 record; V4.1 0). Pools: Vertex/Gemini credits 11.8696, fal cash 3.479, Sarvam ₹4.3. Five provider failures (Lyria ×3, Veo UNAVAILABLE ×2) reserved conservatively; vendor statements not reconciled | Controller pilot packages recorded in `plan/SHOT-MAP-AND-SPEND-RECORD.md`, `v3/plan/SPEND-RECORD-V3.md`, `v4/plan/SPEND-AMENDMENT-V4.md` on the pilot branch; reconciled by `production-learning/tools/reconcile_pilot_ledgers.py` |
| **Any new paid dispatch** — Lab or runtime | **Not authorised.** The runtime's every profile carries `spend_authority.status: none`; the Lab's `authorization.local.yaml` authorises nothing without a new signed record | Controller rider of 14 Sep |

Mechanical enforcement stays local by design (the live ledger and the local authorisation file are
never committed). **Any paid tranche needs explicit Controller approval in writing, before dispatch.**

## 7. Frozen foundations (unchanged)

CANON-010 request contract · Capability Contract v2 (44 = 43 active + 1 dormant) · 13 condition
families · 12 core + 2 reserve scientific slots · Resources topology v3 / CpAO v3 / four
controlled-pack families · EVAL-011 staged design (Q=0, A=90, B≤404, C=32) · the Stage-A frozen package
(`eval/empirical-planning/STAGE-A-FREEZE-2026-09/`: 35 cases, 35 blueprints, **ELIMINATION-RULES.md
applied literally — C-3**) · the six frozen deterministic-instrument criteria · EMP-001's frozen paid
shape. Several merged contracts still carry stale `NOT IN FORCE` status headers; this file governs.
**Sealed evidence is never edited**: `python3 coordination/audits/tools/verify_sealed_evidence.py
--against origin/main` proves the 311 media re-hash and the sealed trees are unchanged.

## 8. Still blocked / not authorised

- **any paid or network provider call by the runtime** — every profile has `spend_authority: none`; a
  signed runtime spend record does not exist and is not created by any 14-Sep decision;
- **any Group-3 item** (C-12…C-18) until its own spend record exists — and, under C-9, only where the
  runtime exposes a launch-critical hole;
- compiling any of the remaining eight Canon packs (C-10);
- **generated in-scene exact text, talking heads, lip-sync, native speech, multi-shot stories** inside
  Alpha 1 (C-7) — RR-2's evidence for in-scene text exists and is untouched; it is out by ruling;
- autonomous external delivery of anything (C-8);
- treating any `clean_observed` cell as a launch clearance, a statistic, or a production SLA;
- adding the two Registry rows of a twice-sent trial identity together;
- rewriting any sealed results file to match the literal rule (the correction lives in the map and
  register); correcting `redo_of: null` in the three undeclared re-do runs (OPEN-2 closed by the
  sealed-evidence rule);
- mandatory human-in-the-loop *exact-text review* in the production API architecture (withdrawn
  28 Aug) — **distinct from C-8**, which is human approval of the finished output before external
  delivery; the two coexist;
- treating benchmark-grade OCR as an exactness certifier; Registry population from text metrics;
- any temporal checker qualification run without all four preconditions (checker, full 12-clip
  ingest, frozen numeric pass marks, preserved human adjudication);
- regenerating any sealed A-TEXT artifact; importing the chat-only manual A-TEXT review;
- rerunning the refuted EVAL-038 configuration; any worker verdict on whether Canon works;
- invoking the gate's Cloud Vision text detector or any paid post-draw scan;
- any CANON-GATE-002 item; any acceptance-rate / accepted-outcome measurement run (not commissioned);
- HED-1 stays undecided and blocks fully loaded CpAO.

### Temporal material contract (resolved, pack-level) — unchanged

Pack-level content requirement; opportunity counts base 12 · multi-shot 6 · on-screen text 6 · product
region 5 · rendered-character identity 4 · photographed-face identity 3; identity populations never
pooled. `CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md`.

## 9. Next gate

**Both branches are merged (14 Sep 2026). The next Controller gate is the first paid Alpha-1 run**,
which needs three things that do not exist today: (1) a decision on whether the Alpha-1 plan comes from
a recorded fixture (as in battery run B01) or a paid reasoning pass; (2) the live transport wired behind
`ExecutionBridge.run()` (deliberately unbuilt; `dispatch_mode: live` refuses); (3) a new signed runtime
spend record naming the profile, the job ceiling, the routes it may call, 0 retries and the human
approver — the object `spend_authority.record` would point at (shape proposed in
`runtime/execute/authorisation.py`). Until that record exists the runtime is dry-only by construction.

In the Controller's order (nothing here is authorised by this file):

1. **First paid Alpha-1 vertical-slice run** — one static overlay ad through the whole chain
   (intake → spec → route → dispatch → gates → human acceptance → outcome event); the smallest
   paid experiment now justified by the runtime. Size: single-digit USD.
2. **C-13 Gemini API smoke** — the two recommended still routes are priced on a surface that has
   never carried a call (`NOTE-UNTESTED-PRICING-SURFACE`); ~USD 1.
3. **C-15 clean reruns** only for the three `replacement_needed` cells, and only if Alpha traffic
   needs them (Alpha 1 does not use image-to-video Wan 2.2, Kling audio or two-speaker routes).
4. Stage B / Stage C (C-17 / C-18) — only after the runtime and baseline are frozen; HED-1 first.

**Open Controller decisions from the Upwork intro integration (15 Sep 2026; none decided by this file):**
(a) ~~push the raw pilot branch~~ (done 15 Sep); (b) adopt **TTAO** formally as a primary production KPI alongside CpAO (recommended YES);
(c) when to promote **speaker micro-qualification** from candidate pattern to standard workflow
(proposed: after two more real productions); (d) when enough complex runs exist to justify
**COMPLEX-PRODUCTION-EVENT / OUTCOME-EVENT-v2** (proposed: after the second); (e) merge **PR #98**
"Production learning: ingest accepted Upwork intro pilot and harden runtime QA".

**Routed, not fixed (Governor):** `canon/HANDOFF.md` and `canon/CANON-SHAPE-v1.md` §7 carry 14-Sep
status notes but remain Canon-stream-owned; `eval/HANDOFF.md` predates the Capability Lab entirely and
needs the eval stream's rewrite; `coordination/WORKSTREAM-STATUS.md` is a derived view and is stale
where it says the Registry is empty or that Production IR/Planner do not exist — this file governs.
