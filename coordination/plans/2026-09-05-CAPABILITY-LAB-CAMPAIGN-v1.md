# Capability Lab Campaign v1 — from Registry = 0 to evidence-backed conditional routing

**Status:** DRAFT — Writer Controller proposal, 2026-09-05. Pending the human Controller's
ratification. Nothing here authorises spend. Authority, once ratified:
`coordination/decisions/CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md`.
**Base `main`:** `599ff4af6a1f0684132303687e438877da47a004` (unchanged since PR #83, 31 Aug).
**Written against:** the Controller's 5 Sep direction — "move into extensive empirical
model/workflow testing … determine which current model/workflow works best for which use case
and under which conditions." Methodology is open; this is the recommended shape, not a constraint.

---

## A. Repository reality (5 Sep 2026, 01:10 IST)

### A.1 What is in flight and must not be disturbed

| Item | State |
|---|---|
| `main` | `599ff4a` — the last merge is PR #83 (31 Aug). No PR has merged since. |
| CANON-GATE-001 | Local branch `work/canon-gate-001` at `02e50fa`, **30 commits ahead of `main`, not pushed, no PR**. Ruling 9's structural fix has landed (`da9219d`, `02e50fa`). The bounded sixth checker pass and the merge commit named in `CONTROLLER-CANON-GATE-001-FIFTH-CHECK-DISPOSITION-2026-09-05.md` have **not yet happened**. A separate Writer Controller session owns that sequence; last activity 00:43 IST. |
| Consequence | `coordination/CONTROL-STATE.md` is **not** edited by this campaign until the gate merge lands. This plan and its decision live on `controller/capability-lab-direction-2026-09-05`, touching only `coordination/plans/`, `coordination/decisions/` and `eval/tasks/` — no overlap with the gate branch's files. |

### A.2 What exists and is reusable unchanged

| Asset | Where | Reuse verdict |
|---|---|---|
| Capability Contract v2 — 44 capabilities (43 active, 1 dormant), 7 evaluator families | `eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml` | **Reuse unchanged.** Capabilities are the columns of the routing map. |
| 13 condition families; 4 actively swept in Wave 1 (LOAD, CONSTRAINT, LANGUAGE, DELIVERY) | `eval/pre-execution-freeze/CONDITION-ENVELOPE-CONTRACT.yaml` | **Reuse; widen the swept set to 6** (add MOTION and REFERENCE — both are on the Controller's routing list). Still sparse, never cartesian. |
| 12 core + 2 reserve scientific slots, defined as *questions* with named candidates as *instruments* | `SCIENTIFIC-WAVE1-MODEL-ROSTER.md` | **Reuse the questions.** Refill every candidate (see C.3). One structural amendment: Stage A screens **several routes per question**, not one — the Controller's objective is *which route*, not *is this route viable*. |
| Stage Q → A → B → C, one call = one trial, repeat ≠ retry, generate once / score every eligible dimension, sparse adaptive sweeps | `eval/pre-execution-integration/STAGED-EXECUTION-PLAN.{md,yaml}` | **Reuse unchanged** as the execution grammar. Counts change; rules do not. |
| Evaluator Qualification Map: 8 capabilities deterministic, 4 qualifiable from material in repo, 7 blocked on qualification, 24 blocked on material + human reference | `EVALUATOR-QUALIFICATION-MAP.yaml` | **Reuse.** It is the basis of the three evidence tiers in §D. |
| Harness with nine fail-closed invariants; Registry writer accepts only `qualified`/`deterministic` instruments; Registry schema v1 (n_items, uncertainty, absence_reason mandatory) | `eval/v1/harness/`, `eval/registry/` | **Reuse unchanged.** Admission bar is not touched. |
| Spend ledger, budget guard, reservation-before-send, 0-retry, ambiguous-settlement semantics (EMP-001 machinery, EVAL-012…016) | `eval/empirical-tranche-1/` | **Reuse.** Proven on paid calls. |
| Direct Gemini video lifecycle (submit → poll → authenticated download), live-proven on `veo-3.1-lite` and `gemini-3.1-flash-image` | `eval/pilot-substrate/video_route.py`, `eval/experiments/EVAL-038/tools/generate_media.py` | **Reuse** for every Google route. |
| fal image route adapter (frozen to two A-TEXT routes), live-proven in EVAL-024 | `eval/empirical-tranche-1/providers.py` | **Extend** to fal video / audio / lipsync routes (zero-spend build). |
| Cloud Vision `TEXT_DETECTION` — benchmark-qualified on Devanagari and Latin; error rates known | `eval/empirical-tranche-1/evidence/EMP-001/text-ocr/` | **Reuse** as the benchmark-grade text instrument. Still not strict-exactness qualified; never a Registry input. |
| 96-item Devanagari battery, Latin pack, 102-item deterministic CV geometry fixtures (never run), 13 temporal perturbation types over 12 rights-cleared clips (3/3 ingested, no pass mark) | `eval/battery/`, `eval/v1/instruments/`, RES-005 | **Reuse** as Stage Q material. Q1 (geometry) is runnable today at USD 0. |
| EVAL-030 result: GPT Image 2 6/8 vs Ideogram v3 1/8 exact text (benchmark-grade, directional) | sealed | **A prior for IMG-02**: Ideogram is not refilled; the "text specialist vs generalist" question gets a new instrument. |
| EVAL-037/038 six briefs with sealed Sonnet production packages; CANON-011's 18 buyer cases (16 runnable); CANON-010's 30 briefs + 10 runnable RX items | `eval/experiments/EVAL-03[78]/`, `canon/research/marketplace-demand-v1/derived/`, `canon/experiments/` | **Reuse as the Stage C pool** (buyer-shaped; Eval authors no briefs). |
| Compiled packs (2/10) and the gate code (pending merge) | `canon/packs/`, `canon/gate/` | **Reuse as a zero-cost structural post-draw check on every trial** — observation only, no verdict on Canon. |
| Media Factory recovered evidence — 206-row manifest, routing prior, cost summary, findings | `~/Vaibhav_Personal_Projects/media-factory-controller-handoff.zip` (122 MB, on disk; **never imported** — `eval/historical-priors/` does not exist) | Import the four markdown files + manifest with hashes (compact EVAL-036). Do not copy media. |

### A.3 What is stale

| Stale item | Evidence | Consequence |
|---|---|---|
| Roster candidate identities (26 Aug) | fal catalogue, checked 5 Sep: MiniMax is now **H3 Max / H3 Max Turbo / Director**; **Seedance 2.5** (native audio, up to 50 reference inputs, 4–30 s, USD 0.473/s at 720p); **Wan 3.0 Prime** (USD 0.14/s 720p); **Gemini Omni Flash 1.1** (USD 0.10/s 720p, native audio); **FLUX 3** i2v; **Grok Imagine 1.5**; image side: **Nano Banana 2** (USD 0.08 on fal, USD 0.067 Google direct), **Qwen Image 3**, **Recraft V4**, **Meta Muse**. Veo 3.1 / Kling v3 / Seedream 5.0 Pro / GPT Image 2 / FLUX.2 Pro remain current. | Every named candidate is refilled in C.3; EVAL-039 pins each id + price with bytes and date before any paid call. |
| Prices | H3 Max is on a 75 % promotion **ending 7 Sep** (768p USD 0.02/s promo vs 0.08/s regular). fal Veo 3.1 Fast is USD 0.15/s with audio vs Google direct USD 0.10/s at 720p. | Pin regular rates, never promo rates, for anything that feeds CpAO. Route Google models direct (existing decision `CONTROLLER-DIRECT-GEMINI-T1-ROUTE-REVISION-2026-08-28.md` stands); everything else via fal. |
| Provider access | Keys on this machine: FAL, Google (Gemini + Cloud Vision), Anthropic. **None for Runway, Sarvam, OpenAI-direct.** ElevenLabs v3 is reachable via fal (USD 0.10/1k chars). | VID-04 (edit existing footage, Runway Aleph) cannot run without a Runway account → deferred to Stage B unless the Controller opens one. AUD-01 (Sarvam bulbul v3, ₹30/10k chars) needs a Sarvam key — **Controller action** (see memory: Vaibhav pre-creates accounts; ask before creating). |
| `SCIENTIFIC-WAVE1-MODEL-ROSTER` "one route per question" | The Controller's objective is conditional routing, which needs *within-lane comparison* | Amended in C.2. |
| Reset decision's immediate queue item 4 ("no new media before T2B") and its T5 scope ("refresh only what the winning workflow needs") | Controller has explicitly changed direction, 5 Sep | Superseded — see B.1. |
| Stage A price refresh (`STAGE-A-ROUTE-PRICE-REFRESH-2026-08-26.yaml`, ~USD 52) | Roster and prices changed | Input to EVAL-039, not a budget. |

### A.4 What is still missing

Registry rows (0); any qualified perceptual / temporal / speech evaluator; person/product reference packs with same-category decoys (Q4); any audio material (Q5); a concrete frozen Stage A item set — the 100-item bank holds prompt *specifications* ("Isolated probe for exact_text_latin at level 1"), not executable prompts, and the comparability core exists as a count (4 / 4 / 3 per lane), not as items; Production IR; Planner; repair runtime; HED-1 (which human time counts in fully-loaded CpAO).

---

## B. Recommended programme sequence

### B.1 Decisions that must be superseded or amended (nothing is erased)

| Prior decision | Disposition under the new direction |
|---|---|
| `CONTROLLER-PROGRAMME-RESET-MEDIA-FACTORY-PRIORS-2026-08-29.md` — immediate queue item 4 ("Do not generate any new media before T2B unless the user explicitly changes direction") | **Superseded** — the Controller has explicitly changed direction. T2B's question was answered for programme direction by `CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`. |
| Same decision — "The USD 25 T2 workflow/model screen remains declined and must not be revived under another name" | **Superseded explicitly.** The Stage A screen below is a differently designed experiment (route-comparison per scientific question, pre-registered elimination rules, tiered evidence), but the Controller is told plainly: this *is* a model screen, and the earlier refusal is reversed on purpose. |
| Same decision — T2A (EVAL-036) as a prerequisite; T3/T4 (Canon propagation / cost compression); T5 "refresh only what the winning workflow needs" | T2A: **re-scoped** to a compact import (four markdown files + manifest, hashed) folded into EVAL-039. T3/T4: **deferred, not cancelled** — Canon is now doctrine + gate + templates, and battery evidence decides which packs earn compilation. T5: **replaced** by this campaign (full Stage A/B/C rather than targeted freshness only). |
| Same decision — historical prior ≠ Registry row; no universal generate-vs-deterministic dogma; do not rediscover the seven settled priors | **Preserved verbatim.** The priors are freshness-tested inside Stage A where a current routing decision depends on them, never re-proven from zero. |
| `CONTROLLER-EVAL-037-CONCLUSION`, `CONTROLLER-EVAL-038-…`, `CONTROLLER-CANON-SHAPE-V1-DIRECTION` | **Untouched.** The Canon verdict stays reserved to the Controller; the substitution configuration stays closed; the consumption shape stands. |
| `CONTROLLER-STOP-TEMPORAL-PREP-PRIORITISE-PRODUCT-PILOT-2026-08-28.md` (EVAL-032/033 stopped "until automated temporal-evaluator qualification is again the objective") | The condition is met once Stage B needs temporal instruments → **reopen as a new task id** (EVAL-041), not by resurrecting EVAL-032/033. Not on the Stage A critical path. |
| `CONTROLLER-DIRECT-GEMINI-T1-ROUTE-REVISION-2026-08-28.md` (Google models via the direct Gemini API, no aggregator) | **Stands** for Google models. Non-Google routes go via fal. |
| `CONTROL-STATE.md` "Next gate is the gate build" | **Amended after the gate merge lands:** next gate = Capability Lab Tranche 1. |
| PILOT-001 closure, EMP-001 authority (spent), EVAL-038 authority (spent), Registry admission bar (`CONTROLLER-EVAL-030-…`) | **Untouched.** New spend needs its own authorisation record. |

### B.2 Sequence and dependencies

```
[now]  gate merge lands (other session) ──────────────────────────────┐
                                                                      ▼
T0  ZERO-SPEND PREPARATION  (EVAL-039, ~2–3 worker days, USD 0)
    ├─ roster + price + route-liveness refresh, pinned bytes/date      (no paid call)
    ├─ compact Media Factory prior import (hashes, 4 md + manifest)
    ├─ Stage A freeze package: items, acceptance contracts, seed policy,
    │    pre-registered elimination rules, evaluator plan, exact cost
    ├─ harness extension: fal video/audio/lipsync adapters; Google direct reuse
    ├─ Q1 deterministic-geometry qualification run (code only)
    ├─ deterministic instruments to build: format probe, masked-diff edit
    │    preservation, brand-colour distance, A/V offset, seeded-repeat hash
    └─ Controller actions: Sarvam key (AUD-01); Runway account (VID-04, optional)
                                                                      ▼
    Spend authorisation record (Controller) — exact models, call count, max cost
                                                                      ▼
T1  STAGE A — ROUTE ADMISSION SCREEN  (EVAL-040, paid, proposed cap USD 175)
    ├─ 1a  image lane + text-to-video lane + native-dialogue items        (~USD 60)
    └─ 1b  image-to-video, reference-to-video, multi-shot, TTS, lipsync   (~USD 115)
    → blind Controller acceptance (EVAL-038 pattern) + deterministic gates
    → first Registry rows (deterministic capabilities only)
    → Capability Map v0 (tiered)
                                                                      ▼
T2  STAGE B — SURVIVORS ONLY  (EVAL-04x, paid, proposed cap USD 250)
    ├─ ≤3 routes per question; atomic + compound items; sweeps on 6 condition families
    ├─ Q3 temporal + Q4 identity qualification using Stage A human labels + decoys
    └─ Registry rows widen to every newly qualified instrument
                                                                      ▼
T3  STAGE C — OUTCOMES + CpAO  (EVAL-04x, paid, proposed cap USD 150)
    ├─ 8 buyer-shaped briefs × 2 recipes × 2 repeats = 32 outcome attempts
    ├─ repair ladder: cheap route → gate/human reject → premium route
    └─ first CpAO; HED-1 must be decided before fully-loaded CpAO
                                                                      ▼
T4  RUNTIME v0 — Production IR extracted from accepted Stage C recipes;
    Planner v0 = deterministic Capability Map lookup (no LLM in the loop)
```

Tranche 1 can start the day the freeze package is accepted. Nothing in T0 needs a paid call.

---

## C. Battery design

### C.1 What we are trying to learn (the routing questions, mapped)

| Controller's routing question | Where it is answered |
|---|---|
| best commercial still without text | Image lane **comparability core** (4 text-free commercial stills: product hero, person lifestyle, Indian-market scene, flat-lay) — every image route runs it |
| best product-reference still / best person-reference still | IMG-04, split into `product` and `person` conditions (COND-REFERENCE) |
| best supplied-image edit / preservation route | IMG-03 (masked-diff preservation is deterministic → Registry-eligible) |
| best exact-text route; when text should be deterministic | IMG-01 / IMG-02 + TOPO-02 (generated vs composited; composite arm costs zero provider calls) |
| best image-to-video route | **VID-03a** (i2v from one shared accepted hero still — the historically proven plate) |
| best text-to-video route | VID-01 |
| best reference-conditioned video route | **VID-03b** (identity from references, camera free — distinct from i2v) |
| best multi-shot route | VID-02 |
| best high-motion / action route | COND-MOTION level in the video core (1 item) + Stage B sweep |
| best native dialogue / audio route | VID-01 with audio on = TOPO-01 arm A; Hindi dialogue item in the core |
| best Hindi / Hinglish route | COND-LANGUAGE: one Hindi item in every lane's core; Stage B sweep |
| best TTS route | AUD-01 (Sarvam bulbul v3) vs AUD-02 (ElevenLabs v3) |
| best lip-sync route | AUD-03 (sync-lipsync v3 + one second route) = TOPO-01 arm B |
| cheapest acceptable production plate; premium when cheap fails | VID-05 cost knee (Veo lite / fast / full; H3 Max 480p / 768p) in Stage A; **the accepted-outcome verdict only in Stage C** via the repair ladder |
| model-policy / refusal fallback | one policy-edge item per lane core (stylised emotional scene with a child-like character — the exact Media Factory Veo refusal shape); `latency_errors_refusals` is deterministic → Registry row from Stage A |
| behaviour under reference / constraint / language / motion / delivery load | Stage B sparse sweeps over 6 of 13 families |

### C.2 The one structural change to the August design

August: one candidate per slot, "equivalent fills" if unavailable → answers *is this route viable?*
Now: **several routes per question at Stage A, on the same frozen core items** → answers *which
route, under which condition, at what cost, and what is the fallback?* Stage A becomes a
route-comparison screen; Stage B keeps the August depth on ≤3 survivors per question.
Everything else — one call one trial, repeats of 2, unseeded inherent-variance repeats by default
(A-TEXT precedent), sparse sweeps, Registry only from qualified/deterministic — is unchanged.

### C.3 Refilled slate (September 2026) — every id and price to be pinned by EVAL-039

| Question | Routes screened at Stage A | Notes |
|---|---|---|
| Image core (all image questions share it) | `openai/gpt-image-2` (fal, ~0.053) · `gemini-3.1-flash-image` = Nano Banana 2 (direct, 0.067) · Nano Banana Pro (direct, 0.134) · `bytedance/seedream/v5/pro` (fal, ~0.0675) · `fal-ai/flux-2-pro` (fal, 0.03) · `alibaba/qwen-image-3` (fal, unpinned) | 6 routes × 4 items × 2 = 48 gens |
| IMG-01 / IMG-02 exact text (Devanagari + Latin) | GPT Image 2 · Nano Banana Pro · Seedream 5 Pro · Recraft V4 (vector, the repairability reserve IMG-06, promoted because Ideogram failed 1/8) | Scored by Cloud Vision (benchmark-grade); composite arm at USD 0 |
| IMG-03 edit preservation | `flux-2-pro/edit` · `nano-banana-pro/edit` · `seedream/v5/pro/edit` · `gpt-image-2/edit` | masked diff deterministic |
| IMG-04 reference (product; person) | same four edit/reference routes, with 1–3 refs | inputs + decoys double as the Q4 qualification pack |
| VID-01 text-to-video (with audio where native) | `veo-3.1-fast` (direct, 0.10/s 720p) · `fal-ai/kling-video/v3/pro` (0.112/s) · `minimax/h3-max` (0.08/s 768p regular) · `alibaba/wan-3.0-prime` (0.14/s) · `google/gemini-omni-flash/v1.1` (0.10/s) · `bytedance/seedance-2.5` (0.473/s, **premium — 4 gens not 8**) | 6 s, 720p, 9:16 |
| VID-03a image-to-video | Veo 3.1 fast i2v (direct) · Kling v3 pro i2v · H3 Max i2v · Wan 3.0 i2v · Seedance 2.5 i2v (4 gens) | from one shared hero still |
| VID-03b reference-to-video | Seedance 2.5 reference-to-video (4) · Veo 3.1 reference-to-video (direct, 4) · Kling v3 elements if pinned | identity refs, camera free |
| VID-02 multi-shot | Kling v3 (10 s multi-shot prompt, 4) · Seedance 2.5 (15 s, 2) · Omni Flash 1.1 (10 s, 4) | cross-cut continuity |
| VID-05 cost knee | Veo 3.1 lite (0.05/s) vs fast vs full (0.40/s, 2 gens); H3 Max 480p vs 768p | trial cost + reliability only; CpAO verdict in Stage C |
| VID-04 edit existing footage | Runway Aleph — **deferred** (no account) | Controller decides whether to open one |
| AUD-01 / AUD-02 TTS | Sarvam bulbul v3 (direct, needs key) · ElevenLabs eleven-v3 (fal, 0.10/1k chars) | 3 scripts (Hindi, Hinglish + brand names, English) × 2 |
| AUD-03 lip-sync | `fal-ai/sync-lipsync/v3` (USD 8/min) · one LatentSync-class or Kling lipsync route (pin) | drives = TTS outputs; plates = i2v outputs (no extra generation) |

### C.3a Provider surface rule — cloud credits first (Controller input, 5 Sep)

The Controller has AWS, GCP and Azure accounts with credits, plus fal, Gemini and Anthropic keys.
Rule for every route in C.3: **if the model is available on Bedrock / Vertex AI / Azure AI Foundry
and is billable against that cloud's credits, run it there; otherwise fal; Google models stay on
the direct Gemini API or Vertex (same models, credit-eligible on GCP).** A read-only availability
survey is being produced at `eval/empirical-planning/CLOUD-MODEL-AVAILABILITY-2026-09-05.md`; EVAL-039
records the chosen surface per route, its id on that surface, and whether it is credit-billed.
Consequences: (1) the cash budget in §E shrinks by whatever moves onto credits; the *call count*
does not change; (2) a model's price differs by surface and the Registry row records the surface
it was measured on; (3) marketplace listings that bill outside credits are treated as cash.

### C.3b Headline hypothesis — the cheap stack (Controller input, 5 Sep)

> "We eventually want a weaker LLM plus a weaker media model to beat the strongest media model
> plus strongest LLM combination. That's where the win is."

This is recorded as the campaign's headline **Stage C** hypothesis, **H-CHEAP**:

> A cheap stack (cheaper reasoning model + cheaper media routes + the intelligence layer:
> conditional routing, deterministic composition, mechanical gates, bounded repair) reaches an
> accepted-outcome rate at least equal to the frontier stack (strongest reasoning model + premium
> media routes, no intelligence layer) at lower CpAO.

How the stages serve it: Stage A/B find, per condition, the *cheapest route that is acceptable* and
the *premium route that fixes what cheap cannot*; Stage C then runs recipe 1 = cheap stack with
the intelligence layer vs recipe 2 = frontier stack, on the same buyer-shaped briefs, blind.
Boundary already on the record: EVAL-038 refuted "weak LLM + two packs ≈ strong LLM" at the
*reasoning-package* level with no gate/redraw loop and no deterministic composition. H-CHEAP is a
different claim (outcome level, with the full intelligence layer) and does not reopen EVAL-038.
No verdict on Canon is implied; the gate is one component of the layer under test.

**Specific cheap topology to test first (Controller's example):** exact text rendered by a cheap
image route that is good at text (candidates: Nano Banana 2 / Gemini Flash image tier; GPT Image 2
at USD 0.05; Qwen Image 3) into a hero still, then a cheap image-to-video route that holds that
text stable through motion — versus text generated natively by a premium video model, versus
deterministic composite. This is the TOPO-02 / TOPO-03 pair below and it is in Tranche 1a/1b, not
deferred to Stage C. (The Controller's phrase "via RGN" in the 5 Sep note is transcribed as given;
it is read here as "via one of the cheaper routes" — to be confirmed.)

| Topology | Arm A | Arm B | Arm C | Decides |
|---|---|---|---|---|
| TOPO-02 exact text in a still | cheap image route renders text | premium image route renders text | textless base + deterministic composite (USD 0) | when generated text is acceptable at all, and at which price tier |
| TOPO-03 exact text through motion | cheap still (with text) → cheap i2v | premium t2v renders text natively | textless still → i2v → tracked/static composite | whether the Media Factory "composite-always for video" prior has expired |

### C.4 What each stage establishes and what is eliminated when

**Stage A (Tranche 1)** establishes, per route × question: refusal/error/latency (deterministic), format compliance (deterministic), trial cost (deterministic), unseeded repeat variance (deterministic), text exactness (benchmark-grade), edit preservation (deterministic), and **blind human acceptance on the core** (product evidence). Pre-registered elimination rules, frozen before the first call:

- E1 — refusal or hard error on ≥ 3 of 8 core trials → eliminated for that question (recorded as refusal-prone; may still be a fallback elsewhere).
- E2 — blind acceptance ≤ 2 of 8 → eliminated for that question.
- E3 — among survivors, the top 3 by acceptance (tie-break: lower trial cost) advance to Stage B.
- E4 — elimination is per (route, question); a route dropped on one question can advance on another.
- E5 — deterministic failures (format, baked text on a no-text item) count as rejects, never as exclusions.

**Stage B (Tranche 2)** establishes capability × condition envelopes on survivors: atomic items for the slot's capabilities, compound scenarios, sweeps on LOAD / CONSTRAINT / LANGUAGE / DELIVERY / MOTION / REFERENCE with the inherited stop rule (two consecutive failing levels). A route leaves the map for a condition level when it fails twice consecutively there.

**Stage C (Tranche 3)** establishes accepted outcomes and CpAO on 8 buyer-shaped briefs × 2 recipes × 2 repeats. Recipe = production topology assembled from Stage B survivors (hero still → i2v → deterministic composite → TTS/lipsync where required), with a repair ladder (cheap first, premium on reject). Only here may "cheap vs premium" and "native vs composite" be concluded as *outcome* verdicts. Optional, Controller's call: make recipe 2 the CANON-SHAPE-v1 blueprint + gate path so Stage C doubles as the acceptance-rate measurement the Controller reserved — recorded as observation, verdict remains the Controller's.

---

## D. Measurement plan — three evidence tiers, kept separate

| Tier | Instruments | What it may claim | Registry? |
|---|---|---|---|
| **T-DET deterministic** | file/format probe; masked-diff edit preservation; brand-colour distance in a masked region; A/V offset (we supply both inputs); seeded/unseeded repeat hash + SSIM; ledger-derived latency, errors, refusals, trial cost; the compiled-doctrine gate's post-draw checks (structure only) | a capability score under recorded conditions | **Yes** — 8 capabilities: `delivery_format_compliance`, `edit_preservation`, `packaging_brand_colour_fidelity`, `audio_video_synchronisation`, `reliability_pass_at_k`, `cost_and_cpao` (trial cost; CpAO absent until Stage C), `latency_errors_refusals`, `reproducibility`. Q1 geometry (`object_count`, `spatial_relationship_2d`) joins after its USD-0 qualification run. |
| **T-BENCH benchmark-qualified** | Cloud Vision text OCR (error rates carried on every row); ASR against known scripts for `spoken_script_correctness` (script known by construction → qualifiable at Stage A from TTS outputs) | a bounded-error measurement | **No** (existing ruling: benchmark-grade text metrics do not populate the Registry). Lives in the Capability Map with its error rate. |
| **T-HUMAN blind acceptance** | Controller judges blinded artifacts against each item's frozen acceptance contract (EVAL-038 pattern: stripped packages, sealed commitments, keys off-repo, decision rule fixed first) | product evidence: "route X produced more customer-acceptable media than Y on these items" | **No.** Capability Map tier `human_blind_acceptance` with n. Also the human reference that later qualifies Q4/Q6 instruments. |
| **T-SCREEN unqualified machine** | VLM judges (Gemini / Claude vision) for failure-mode tagging and triage, labelled `screened_not_qualified` | nothing about capability; a hypothesis to check by hand | **Never.** Their agreement with T-HUMAN labels becomes qualification evidence for Q4. |
| **T-PRIOR historical** | Media Factory routing prior (July 2026), freshness-flagged | where to start; what not to rediscover | **Never.** Map tier `historical_prior`. |

Qualification path per family: Q1 geometry — run now (USD 0). Q2 text — done (benchmark). Q3 temporal — 12 clips + 13 perturbations exist; needs frozen pass marks before observation (EVAL-041, after Stage A). Q4 visual identity — Stage A's reference inputs + same-category decoys + Controller labels form the pack at zero extra spend. Q5 speech — Stage A TTS outputs with known scripts; pronunciation of brand names stays human (Controller is a first-language listener). Q6 creative/commercial — human only for this campaign.

The rule the Controller set is preserved exactly: an unqualified evaluator never blocks generation; it only blocks a Registry claim from that dimension.

---

## E. Cost / call plan (nominal, pre-pinning — EVAL-039 replaces every figure)

| Tranche | Generations | Evaluator calls | Human | Nominal | Proposed cap |
|---|---:|---:|---|---:|---:|
| T0 preparation | 0 | Q1 geometry: local code | Controller: Sarvam key; accept freeze package | USD 0 | 0 |
| **T1a** image core + text + edit + reference (112) · t2v incl. native dialogue (52) | 164 | Cloud Vision ~100, ASR ~20, VLM triage ~150 | ~1.5 h blind acceptance | ≈ USD 50 | **USD 60** |
| **T1b** i2v (36) · ref2v (12) · multi-shot (10) · TTS (12) · lipsync (12) | 82 | ASR ~24, A/V offset local, VLM triage ~60 | ~1 h | ≈ USD 90 | **USD 115** |
| T2 Stage B, ≤3 survivors/question, 6 sweep families | ≤ 200 | ≈ 1,000 | ~3 h | ≈ USD 180 | USD 250 |
| T3 Stage C, 32 outcome attempts + repair ladder | formula (≈ 100–150) | ≈ 400 | ~4 h + HED-1 decision | ≈ USD 110 | USD 150 |
| **Total ceiling, authorised one tranche at a time** | | | | | **≈ USD 575** |

**Credits change the cash line, not the call count.** Once the cloud-availability survey and
EVAL-039 settle which routes are credit-billed (Veo / Imagen / Gemini image on Vertex; Nova and any
Bedrock-native media on AWS; whatever Azure Foundry lists "direct from Azure"), the cash portion of
each tranche is re-stated as *cash* + *credits consumed*, and both are ledgered separately. The
proposed caps stay as spend ceilings in USD-equivalent regardless of which pool pays.

Video dominates: at 6 s, one trial costs USD 0.30 (Veo lite) to 2.84 (Seedance 2.5). Image trials are USD 0.03–0.13. Evaluator spend is small (Cloud Vision ≈ USD 1.5/1k images; VLM triage ≈ USD 0.01/call). The Controller's judging time is the scarce resource; blind acceptance is designed to take ≈ 20 s per artifact.

---

## F. Registry path — from 0 rows without weakening admission

1. **Stage A writes the first rows**, through the harness's existing Registry writer, only from `deterministic` instruments: for every route × question × core condition, rows for `latency_errors_refusals`, `delivery_format_compliance`, `cost_and_cpao` (trial cost; `absence_reason: not_applicable` for CpAO), `reproducibility` (unseeded variance, or held-seed where the route supports a seed), `reliability_pass_at_k` where a deterministic pass criterion exists; `edit_preservation` on IMG-03 items. Every row carries `n_items` (4 per core), `repeats_per_item: 2`, `uncertainty.status: computed` with `independence_status: NOT ESTABLISHED` (four core items share authorship) — so the interval is a sizing reference, as the schema demands.
2. **Stage B widens rows** to Q1 geometry capabilities and to any instrument that passes qualification between tranches (Q3 temporal with frozen pass marks; Q4 identity once the decoy pack + human labels qualify a VLM). Text exactness stays benchmark-grade and outside the Registry unless a strict-exactness instrument ever passes.
3. **Stage C adds `cost_and_cpao` rows with a real denominator** — the only place CpAO exists.
4. **The Capability Map is the product asset; the Registry is its strict subset.** `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml` holds every cell with its tier (`deterministic` / `benchmark` / `human_blind_acceptance` / `screened` / `historical_prior`), n, date, route id + version, price pin, failure modes, and fallback. A Planner may read all tiers; only Registry-tier cells may back a commitment.

---

## G. Runtime consequence — how this becomes routing and Production IR

- **Capability Map cell** = (required capabilities, condition levels) → ranked routes, each with: pass rate + tier, trial cost, refusal rate, failure modes to inspect, fallback route, evidence date.
- **Planner v0** is a deterministic lookup, no LLM: Normalized Request → required capability set + condition levels (already derivable from the CANON-010 grammar) → map lookup → topology (hero still → i2v → composite → TTS/lipsync as required) → cost estimate → fallback ladder. What a route may *promise* is bounded by the tier backing it.
- **Production IR v0** is extracted from Stage C's *accepted* recipes, not designed in the abstract: production units, per-step route id + pinned params, the gate checks applied, and the repair ladder that was actually used. This honours the frozen separation Creative IR ≠ Production IR and the reset's rule that Production IR is extracted from proven recipes.
- **Empirical memory** = accepted Stage C recipes become templates (CANON-SHAPE-v1 §4's last step) with their Map cells attached; the Map is re-dated as models drift, and the freshness rule (T-PRIOR) governs stale cells.

---

## H. Proposed Controller decisions and tasks — the minimum set

| Artifact | Purpose | Spend |
|---|---|---|
| `coordination/decisions/CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` | Records the direction change; supersedes / amends the items in B.1 explicitly; adopts this plan; defines the evidence tiers and the Capability Map; authorises T0 | USD 0 |
| `eval/tasks/EVAL-039-SEPT-2026-ROSTER-REFRESH-AND-STAGE-A-FREEZE.md` | Everything in T0 that a worker can do: pins, adapters, freeze package, compact prior import, Q1 run, deterministic instruments, exact Tranche 1 cost | USD 0 |
| `eval/tasks/EVAL-040-STAGE-A-ROUTE-ADMISSION-SCREEN.md` | Tranche 1 execution, split 1a / 1b; **status PENDING SPEND AUTHORISATION** until EVAL-039 names exact ids, counts and cost | proposed cap USD 175 |
| Spend authorisation record (Controller, after EVAL-039) | The reset's own rule: ask for spend only when the protocol names the exact model, call count and maximum cost | — |
| `CONTROL-STATE.md` amendment (after the gate merge lands) | next gate = Capability Lab Tranche 1; list superseded items | — |

Not proposed: a new governance layer, new charters, new schemas, further packs, Production IR before Stage C, any Canon verdict.
