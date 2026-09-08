# Task EVAL-039A: Stage A test-case package — customer-shaped cases, frozen Canon blueprints, acceptance contracts, coverage and cost

**TASK ID:** EVAL-039A (sub-task of EVAL-039, deliverable 6 — the Stage A freeze package)
**STATUS:** DRAFT — Planner output, 2026-09-05. Executable only after the human Controller reviews it (five-role pipeline, `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` §3a rule 11) and that decision is ratified. USD 0 provider spend in every case.
**OBJECTIVE:** Produce, at USD 0, the complete Stage A test-case package under `eval/empirical-planning/STAGE-A-FREEZE-2026-09/` — 35 customer-shaped cases with Normalized-Request mappings, one frozen Canon-shaped production blueprint per case, blind-judgeable acceptance contracts, per-route execution parameters, coverage matrix, elimination rules, seed policy, evaluator plan, irreducibility argument and a call-count/cost table split 1a/1b by billing pool — so the Controller can authorise Tranche 1 by naming exact routes, call counts and a hard cap.
**WHY WE ARE DOING THIS:** The Controller's direction is a conditional routing map ("which route, under which condition, at what cost"). The August bank holds prompt *specifications*, not executable customer requests; the comparability core exists only as counts. Before any money is spent, the cases must exist as a real Indian buyer would write them, mapped to the frozen request grammar, produced under one frozen Canon blueprint each so that a route comparison compares routes and nothing else. This package is what the spend record will name.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`; explain technical ideas in plain English, including what they mean, why they matter and their practical consequence; use minimum sufficient wording without sacrificing understandability; do not invent; separate evidence from inference.

## CONTEXT CONTRACT

**Inherits `shared/CONTEXT-SUFFICIENCY-POLICY.md`.** The worker owns context *sufficiency*, not just this checklist; expand context whenever the policy requires it, and stop with `STOP — CONTEXT_INSUFFICIENT` rather than guess.

### BASE STATE
- **BASE MAIN SHA:** `599ff4af6a1f0684132303687e438877da47a004`; work directly on `controller/capability-lab-direction-2026-09-05` in the worktree `media-intelligence-wt-controller` (which carries the plan, the direction decision and EVAL-039/039B/040); the Controller session commits. Re-base on the post-CANON-GATE-001 `main` when it lands; the gate is a read-only dependency.
- **ACCEPTED DEPENDENCY SHA(s):** none yet — the direction decision is DRAFT pending ratification.

### REQUIRED ORIENTATION
The default bootstrap in `coordination/RUNBOOK.md`, plus `coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md` §C.1–§C.4 and §D, and `coordination/decisions/CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` §3a and §7.

### TASK-SPECIFIC CONTEXT
- `eval/tasks/EVAL-039-SEPT-2026-ROSTER-REFRESH-AND-STAGE-A-FREEZE.md` — parent; this task owns its deliverable 6 only.
- `canon/CANON-SHAPE-v1.md` §4–§5 — the blueprint shape and the surviving rules (accepted Canon only; render by id, never paraphrase; guard closure; fail-closed on HOLD).
- `canon/packs/pack-triggers-v0.yaml` — deterministic NR → pack selection; the audio coverage-gap notice.
- `canon/compilation/PACK-product_appearance-v0.yaml` (PA-D1…PA-D10, `PA-Dn-check`) and `PACK-composition_and_attention-v0.yaml` (CA-D1…CA-D11, `CA-Dn-check`) — the only compiled doctrine; every blueprint decision cites these ids.
- `canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml` — NR fields (`requested_operation`, `supplied_assets[]`, `mutation_intents[]`, `deliverable_set`, `modality`, `entities[]`, `relationships[]`, `text_requirements[]`, `brand_requirements`, `language_topology`, `speaker_topology`, `temporal_structure`, `subject_motion`, `camera_motion`, `delivery`, `specification_provenance`, `ambiguity_markers[]`, `acceptance_intent`), the seven `requested_operation` values (`generate, edit, animate, restore, extend, compose, variants`) and the forbidden production-route values.
- Source pools (adapt from; never author from nothing): `canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml` (MKT-001…018; MKT-015/016 not runnable); `canon/experiments/v1/brief-bank/briefs.jsonl` (BR-F01…F10 × EN/HI/HG); `canon/experiments/pre-execution-freeze/REQUEST-COVERAGE-EXTENSION.jsonl` (RX-01…RX-10 runnable; RX-11 representation-only); `eval/experiments/EVAL-038/payloads/B01…B06.user.txt`.
- `eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml` (ids only; `repairability` is dormant), `CONDITION-ENVELOPE-CONTRACT.yaml` (13 families; `workflow_mode` ≠ `requested_operation`; seed fields), `EVALUATOR-QUALIFICATION-MAP.yaml` (the 8 `yes_deterministic` capabilities), `SCIENTIFIC-WAVE1-MODEL-ROSTER.md` (questions; TOPO-01/02).
- `eval/pre-execution-integration/STAGED-EXECUTION-PLAN.yaml` stage A block — repeats 2, never halved; seed policy declared before any repeat group; metrics permitted/forbidden.
- `eval/empirical-planning/CLOUD-MODEL-AVAILABILITY-2026-09-05.md` (surface per route; §6 table) and `STAGE-A-ROUTE-PRICE-REFRESH-2026-08-26.yaml` (August prices — stale, indicative only, never a pin).
- Historical priors, freshness-test only: `eval/historical-priors/media-factory-v1/MEDIA-FACTORY-ROUTING-PRIOR.md` once EVAL-039 deliverable 2 lands; until then the Controller-handoff copy the Planner read (`~/…/scratchpad/media-factory-controller-handoff/MEDIA-FACTORY-ROUTING-PRIOR.md`, five numbered freshness items).
- `eval/experiments/EVAL-038/JUDGING-PROTOCOL.md` — blind-judging pattern the acceptance contracts must fit.
- `canon/gate/run_gate.py` docstring (read-only; on the unmerged gate branch) — `pre` runs over a package at USD 0; a PASS establishes structure only.

### BROAD READS
`canon/compilation/PACK-*.yaml` in full — BROAD READ JUSTIFICATION: blueprints must cite decision and check ids verbatim, so the Executor must read every decision, its `default`, `limits` and `check` once.

### EXPANSION TRIGGERS
(a) a source pool item's language, operation or supplied-asset list is ambiguous → read the whole source record; (b) a route in plan §C.3 has no surface row in the cloud survey → record `surface: unresolved`, do not choose; (c) CANON-GATE-001 merges during the task → re-read `canon/gate/run_gate.py` and run `pre` on every blueprint.

### EVIDENCE HANDLING LEVEL
`aggregated_evidence` — committed contracts, packs and source pools; no run evidence is opened. Never open sealed A-TEXT or EVAL-038 media.

### CONTEXT INSUFFICIENCY
If a case cannot be mapped to the grammar without inventing a customer statement, or a route's surface cannot be chosen from the survey, stop and route with `STOP — CONTEXT_INSUFFICIENT`; record the case as `status: blocked` rather than guessing.

**INPUTS:** the files above; nothing else is read for authoring. No provider, API, OCR or LLM call of any kind.

**IN SCOPE:** everything under `eval/empirical-planning/STAGE-A-FREEZE-2026-09/` as specified in §A–§D below.
**OUT OF SCOPE:** price pinning and fetched bytes (EVAL-039 deliverable 1 — this task *references* pins by route id and marks `unpinned` where none exists); harness adapters and instruments (deliverables 3–4); Q1 run; the Controller Brief for EVAL-039; Stage B/C items; any generation, evaluator call, or "liveness ping"; any edit to `coordination/`, `canon/`, `resources/`, committed evidence, or any existing file; any Registry row; any verdict on Canon.

**DELIVERABLES** (all under `eval/empirical-planning/STAGE-A-FREEZE-2026-09/`): `README.md`, `TEST-CASES.yaml`, `test-cases/<CASE-ID>.md`, `BLUEPRINTS/<CASE-ID>.blueprint.md`, `COVERAGE-MATRIX.md`, `ACCEPTANCE-CONTRACTS.md`, `ELIMINATION-RULES.md`, `SEED-POLICY.yaml`, `EVALUATOR-PLAN.yaml`, `COST-TABLE.yaml`, `IRREDUCIBILITY.md`.

**AUTONOMY MODE:** autonomous — method frozen below; the Controller is unavailable for the authoring window; every question is recorded in `README.md` §Open questions, never asked.

**RESOURCE BUDGET:**
- sources/items: 35 cases, 35 blueprints; source pools above only.
- storage: text and YAML only; no media, no fetched HTML (≤ 1 MB total).
- API spend: **USD 0**. Provider, evaluator, OCR and LLM API calls: 0. Network: none required.
- generations/retries: 0 / 0.
- other: no sub-agents (8 GB machine); no git commit or push by the Executor beyond its own work branch; nothing deleted or overwritten.

**APPROVED DEPENDENCIES:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` (ratification pending — this task is authored ahead of it, per §7 overnight mode, and executes only after it); CANON-010 grammar, Capability Contract v2, Condition Envelope Contract (in force per `CONTROL-STATE.md` despite stale headers).

---

## A. Deliverable structure and the case record

### A.1 `TEST-CASES.yaml` — one record per case; every field mandatory unless marked optional

| Field | Content and rule |
|---|---|
| `case_id` | `<LANE>-<KIND>-<NN>`; unique; lanes `IMG`, `VID`, `AUD`, `MUS`. Fixed ids in §B.1. |
| `lane`, `question_served` | plan §C.1 row(s) and roster question ids (e.g. `IMG-03`), plus `TOPO-01/02/03` arm(s) and any §C.3d addition served. |
| `customer_request` | verbatim, as the customer would write it to a studio on WhatsApp/email: `channel`, `register` (whatsapp/email), `language` (en/hi/hg), `text` (with the customer's own constraints, typos tolerated, no benchmark vocabulary), `attachments_named[]` (what the customer says they are sending). |
| `source` | `{pool, id, adaptation}` — `pool` ∈ marketplace/brief_bank/rx/eval038; `id` the real record; `adaptation` states every change made (e.g. `text_requirement_dropped_for_core`, `duration_set_to_6s`) or `fixture` with a reason. |
| `nr` | the Normalized Request: `requested_operation` (one of the seven), `modality`, `supplied_assets[]`, `mutation_intents[]` (when required by the grammar), `entities[]` with `product_or_packshot_present: bool`, `text_requirements[]` (exact strings, script), `language_topology`, `speaker_topology`, `temporal_structure`, `delivery` (aspect, duration_s, resolution, platform), `acceptance_intent`, `provenance` per field (`customer_stated / customer_implied / system_derived / absent`). No production-route value anywhere. |
| `capabilities` | `primary` (one contract-v2 id) and `exercised[]` (all ids); no dormant id as primary. |
| `conditions` | family → level for all 13 families (`not_applicable` where the family does not apply); `COND-WORKFLOW.workflow_mode` per route arm, `who_chose_workflow_mode: benchmark_fixed`. |
| `reference_assets[]` | optional; each: `role` (identity_product / identity_person / supplied_subject / style / decoy), `description`, `rights_rule` (Controller-owned photo, Resources item with explicit `underlying_media_rights`, or constructed synthetic), `decoys_required: true` for identity refs, `status: specified` (bytes are not produced by this task). |
| `acceptance_contract` | 3–6 observable accept/reject statements (§A.3). |
| `blueprint_ref` | path under `BLUEPRINTS/`; `blueprint_author: executor_agent`; `blueprint_sha256`. |
| `routes[]` | per route: `route_id` (plan §C.3 id), `surface` (vertex/azure/bedrock/fal/direct — from the survey §6), `billing_pool: credits|cash`, `route_status: pinned|unpinned|needs_controller_enablement|no_access`, `arm` (cheap/premium/composite/native/chain), `params` (aspect, duration_s, resolution, audio on/off, refs count, seed field per `SEED-POLICY.yaml`), `repeats: 2` (or the stated exception with reason), `tranche: 1a|1b`. **Interlock with EVAL-039B:** each record also carries `item_id` (= `case_id`) and each route carries the billing quantity `seconds` (video), `chars` (TTS) or `minutes` (lipsync) so `eval/empirical-planning/project_costs.py --test-cases TEST-CASES.yaml` (EVAL-039B) can regenerate the projection from this file. |
| `downstream_reuse` | what this case's accepted outputs feed (hero still → i2v plate; clip → lipsync plate; TTS → lipsync drive) and what it consumes. |
| `cut_order_rank`, `irreducibility_ref` | integer rank (1 = cut first) and the §C paragraph id. |

### A.2 `test-cases/<CASE-ID>.md`
Human-readable twin of the record: the request as the customer sent it (Hindi in Devanagari where the customer would write Devanagari; Hinglish in Latin as customers actually type), the NR table, the acceptance contract, and one paragraph "why this shape is real demand" citing the source id.

### A.3 `ACCEPTANCE-CONTRACTS.md` — judgeable blind
Each contract is 3–6 statements a first-language Indian judge can decide from the artifact alone (no prompt, no route name), each phrased `ACCEPT only if …` / `REJECT if …`, e.g. *"REJECT if any lettering appears anywhere in the image"* (no-text core), *"ACCEPT only if the bottle's label wording reads exactly 'शुद्ध सरसों तेल'"*, *"REJECT if the second speaker's lips move while the first line is spoken"*. Forbidden: rubric scores, adjectives without an observable ("premium", "good"), anything referencing the route, the arm, or Canon. Every contract ends with the deterministic pre-checks that count as rejects (E5): format probe, baked-text scan on no-text items, duration/aspect mismatch.

### A.4 `BLUEPRINTS/<CASE-ID>.blueprint.md` — one frozen production spec per case
Authored by the Executor agent from the compiled packs (no LLM API call); `author: executor_agent` recorded. Structure: (1) `packs_selected[]` from the trigger table with the triggering NR field named; compiled packs injected by id, uncompiled packs listed as `selected_uncompiled` (no doctrine drawn from them); audio cells carry the coverage-gap notice verbatim and attribute nothing to Canon; (2) `decisions[]` — each cites a `PA-Dn` / `CA-Dn` id and states the case-specific value (declared finish per named object, one implied light source, the single dominant element and attention order, frame choice, shot length / motion motivation for video), rendered from the pack's `default` text by id — never paraphrased doctrine, never HOLD material; (3) `text_handling` — `none` (no lettering anywhere), `generated` (arm A/B, exact string + script), or `composite` (textless plate + deterministic overlay, font/position/colour named); (4) `dispatch_parameters` — aspect, duration_s, resolution (720p video / ~1 MP image), audio flag, reference slots; (5) `pre_dispatch_checks[]` — the `PA-Dn-check` / `CA-Dn-check` lines that apply, plus the no-in-image-text line for no-text cases; (6) `held_constant_across_routes: true` and the single `generation_prompt` text every route receives (route-specific parameter mapping only, no prompt rewording). If `canon/gate/run_gate.py` is on the Executor's base, run `pre` on each blueprint at USD 0 and record `gate_pre: PASS|FAIL + report path`; otherwise `gate_pre: not_available_on_base` — never copy gate code into the deliverable.

### A.5 Package-level files
- `ELIMINATION-RULES.md`: E1–E5 **verbatim** from plan §C.4, the survivor cap of 3 per question, and the note that Seedance 2.5 items with fewer core trials are eliminated on the same *proportions* (E1 ≥ 3/8 → ≥ 37.5 %; E2 ≤ 2/8 → ≤ 25 %), stated before any call.
- `SEED-POLICY.yaml`: per route `seed_support: exposed|absent_in_api|undocumented` (from EVAL-010 / pins; `undocumented` where unpinned) and `seed_policy: unset` default (inherent variance, A-TEXT precedent); `held` only where the Executor records a reason; never pooled.
- `EVALUATOR-PLAN.yaml`: per case the fan-out by tier — T-DET (format probe, latency/error/refusal, trial cost, unseeded repeat hash+SSIM; masked-diff on edit cases; brand-colour distance where a packaging colour is fixed; A/V offset on lipsync), T-BENCH (Cloud Vision on every text case; ASR-vs-script on TTS and dialogue), T-HUMAN (blind Controller acceptance on every case), T-SCREEN (VLM failure tagging, `screened_not_qualified`), plus `run_gate.py post` structure-only on every artifact; language never pooled across en/hi.
- `COST-TABLE.yaml`: §D.
- `IRREDUCIBILITY.md`: §C.
- `README.md`: package map, counts, language mix, 4K deferral statement, open questions for the Controller (morning decisions), and the contradictions the Executor met.

---

## B. Coverage requirements (fixed counts)

### B.1 The 35 cases
**Image lane — 12.** Comparability core (exactly 4, all no-lettering by doctrine; 6 routes: `openai/gpt-image-2` [Azure if deployed, else fal cash], `gemini-3.1-flash-image` Nano Banana 2 [Vertex credits], `gemini-3-pro-image` Nano Banana Pro [Vertex credits], `bytedance/seedream/v5/pro` [fal], `FLUX.2-pro` [Azure if deployed, else fal], `alibaba/qwen-image-3` [fal, unpinned]; conditional credit-only extras `stability.sd3-5-large-v1:0` [Bedrock us-west-2] and `MAI-Image-2.6` [Azure, price unpublished] recorded as `needs_controller_enablement`):
`IMG-CORE-01` product hero, EN (source B06 or BR-F02-EN); `IMG-CORE-02` person lifestyle, **Hinglish** (BR-F03-HG with `text_requirement_dropped_for_core`); `IMG-CORE-03` flat-lay, EN/HG (BR-F04-HG or `fixture`); `IMG-CORE-04` **policy-edge**: stylised emotional scene with a child-like character in an Indian setting, Hindi (the Media Factory Veo-refusal shape; `fixture` permitted with that reason).
Exact text = TOPO-02, three arms each: `IMG-TEXT-01` Devanagari headline, HI (BR-F01-HI); `IMG-TEXT-02` Latin + brand name, EN (BR-F01-EN). Arm A cheap: NB2, Qwen Image 3, GPT Image 2; arm B premium: NB Pro, Seedream 5 Pro, Recraft V4 (`fal`, pin); arm C composite: one textless base draw ×2 on the cheapest pinned image route, overlay by code at USD 0.
Edit/reference on the four edit routes (`flux-2-pro/edit`, `nano-banana-pro/edit`, `seedream/v5/pro/edit`, `gpt-image-2/edit`; edit prices unpinned in August): `IMG-EDIT-01` remove a person, EN (RX-01); `IMG-EDIT-02` background to white preserving pack text, **HI** (RX-02); `IMG-EXT-01` extend to 9:16, EN (RX-07); `IMG-COMP-01` compose portrait + packshot, HG (RX-08); `IMG-REF-01` product identity from 1–3 refs + same-category decoys (BR-F02-HI or B06); `IMG-REF-02` person identity from refs + decoys (MKT-009 or BR-F04-HI).
**Text-to-video lane — 6.** Core (exactly 4; 6 s, 720p, 9:16 unless the customer's platform implies otherwise; routes `veo-3.1-fast-generate-001` [Vertex], `fal-ai/kling-video/v3/pro` [fal], `minimax/h3-max` 768p [fal], `alibaba/wan-3.0-prime` [fal], `gemini-omni-1.1-flash-preview` [Vertex], `bytedance/seedance-2.5` [fal, premium]; conditional `sora-2` [Azure, needs deployment]): `VID-T2V-01` single-speaker **Hindi** talking to camera, native audio = TOPO-01 arm A (BR-F07-HI); `VID-T2V-02` **high-motion** action, EN (BR-F06-EN or MKT-011); `VID-T2V-03` **policy-edge** stylised emotional scene with a child-like character, HI/HG (`fixture` reason as above); `VID-T2V-04` product commercial, EN (MKT-012 or B01). Seedance 2.5 runs `VID-T2V-01` and `VID-T2V-02` only, repeats 2 (breadth deferred, repeats never halved — see contradiction 2). Added scope: `VID-2SPK-01` **two-speaker Hindi dialogue, ≤ 2 turns** (BR-F08-HI) on Veo 3.1 fast, Kling v3, Omni Flash 1.1, Seedance 2.5 (native, arm A) *and* on the chain (arm B: TTS both lines on both TTS routes → lipsync on a two-person plate drawn once on the cheapest pinned image route ×2 then i2v ×2) — capability `two_speaker_turn_assignment_and_lip_sync`; freshness test for prior item 4. Cost knee `VID-KNEE-01` = `VID-T2V-04`'s request on Veo 3.1 lite ×2, Veo 3.1 full ×2, H3 Max 480p ×2 (fast and 768p come from the core).
**TOPO-03 — 1.** `VID-TOPO3-01` exact Devanagari text through motion (same brief as IMG-TEXT-01): arm A cheap still with text (IMG-TEXT-01 arm A accepted draw) → cheap i2v on H3 Max, Wan 3.0, Veo 3.1 lite ×2; arm B premium native t2v on Veo 3.1 full and Kling v3 ×2 (tranche 1a); arm C textless plate (IMG-TEXT-01 arm C base) → i2v on the cheapest pinned i2v route ×2 + tracked/static composite by code. Freshness test for prior item 3.
**Image-to-video lane — 4** (plates = Controller-accepted stills from 1a; routes Veo 3.1 fast i2v [Vertex], Kling v3 i2v, H3 Max i2v, Wan 3.0 i2v, Seedance 2.5 i2v on two items only): `VID-I2V-01` slow orbit on the product still, EN (RX-05; plate IMG-CORE-01); `VID-I2V-02` **Hindi** animate person, static camera (RX-06; plate IMG-CORE-02); `VID-I2V-03` **high-motion** on the person still, EN/HG (adapted BR-F06-EN/HG); `VID-I2V-04` **policy-edge** animate of the child-like stylised still, HI (plate IMG-CORE-04; freshness test for prior item 1). Seedance runs 02 and 03.
**Reference-to-video — 2** (Seedance 2.5 ref2v, `veo-3.1` reference-to-video [Vertex], Kling v3 elements if pinned): `VID-REF-01` product identity from refs, EN (MKT-014 or MKT-012); `VID-REF-02` person identity from refs + decoys, EN (MKT-009).
**Multi-shot — 2:** `VID-MS-01` **15-second** multi-shot, HG (BR-F10-HG) on Kling v3 15 s, Seedance 2.5 15 s, Omni Flash 1.1 (longest supported ≤ 15 s), Veo 3.1 fast + extend — this is the §C.3d 15-s item; `VID-MS-02` 10 s, EN (BR-F10-EN, `duration_set_to_10s`) on Kling v3 and Omni Flash 1.1.
**TTS — 3** (Sarvam `bulbul:v3` direct [Sarvam credits, key is a morning decision]; ElevenLabs `eleven_v3` via fal [cash]; conditional credit-only Hindi extras Chirp 3 HD hi-IN / Azure Neural TTS hi-IN, unpinned): `AUD-TTS-01` **Hindi** (BR-F05-HI); `AUD-TTS-02` **Hinglish + Indian brand names** (BR-F07-HG); `AUD-TTS-03` Indian-English (BR-F05-EN). ≤ 250 characters each.
**Lip-sync — 3** (`fal-ai/sync-lipsync/v3` + one LatentSync-class or Kling lipsync route, pin; freshness test for prior item 5): `AUD-LIP-01` **Hindi** = TOPO-01 arm B (plate VID-I2V-02 accepted clip, drive AUD-TTS-01); `AUD-LIP-02` Hinglish (drive AUD-TTS-02); `AUD-LIP-03` English (drive AUD-TTS-03). Drive selection rule frozen in the package: repeat 1 of ElevenLabs v3 unless the Controller chooses Sarvam in the morning; the drive is held constant across lipsync routes.
**Music — 2** (Lyria on Vertex — the survey observed `lyria-002` GA, not "Lyria 3"; ElevenLabs music on fal, unpinned): `MUS-01` Hindi kitchen ad bed (BR-F06-HI); `MUS-02` runner ambient + music, EN (BR-F06-EN).
**4K:** not a case. `README.md` and `COVERAGE-MATRIX.md` state: *4K recorded as a Stage B COND-DELIVERY level only; round one runs 720p.*

### B.2 Checks the Tester runs on `COVERAGE-MATRIX.md`
1. Every plan §C.1 routing-question row lists ≥ 1 case id (VID-04 Runway row shows `deferred_no_account`).
2. §C.3d: exactly one 15-s item (VID-MS-01); one two-speaker Hindi dialogue (VID-2SPK-01) with native and chain arms; music lane 2 briefs × 2 routes × 2; 4K deferral sentence present.
3. Core counts exactly: image 4, t2v 4, i2v 4, TTS 3, lipsync 3; each core has ≥ 1 Hindi/Hinglish item and 1 policy-edge item (TTS/lipsync: policy-edge waived, stated); video cores each have 1 high-motion item.
4. TOPO-02 (both text cases) and TOPO-03 list arms A, B, C with routes and call counts.
5. Media Factory freshness items 1–5 each map to ≥ 1 case (1 → VID-I2V-04 / VID-T2V-03; 2 → every Seedance line; 3 → VID-TOPO3-01; 4 → VID-2SPK-01; 5 → AUD-LIP-*).
6. `requested_operation` coverage: generate, edit, animate, extend, compose covered; `restore` and `variants` **omitted with stated reasons** (no restore route in the §C.3 slate; variant-set acceptance is outcome-level → Stage C; Tamil/Bengali scripts have no benchmark-grade instrument).
7. Language mix stated as counts by en/hi/hg per lane; Hindi/Hinglish ≥ 40 % of cases overall.
8. No `customer_request.text` contains benchmark vocabulary (grep: `probe`, `capability`, `benchmark`, `isolated`, `level 1`, `condition`); the Auditor reads every request for register.

---

## C. Irreducibility and cut order (`IRREDUCIBILITY.md`)
One short paragraph per case: which routing question would go unanswered if it were dropped, and why it cannot merge with its nearest neighbour (e.g. VID-I2V-04 vs VID-T2V-03: same policy shape, different workflow mode — the historical refusal was on i2v). Then the **cut order if money is short**, fixed here and copied verbatim: (1) Seedance 2.5 on VID-MS-01 (15 s premium); (2) Seedance 2.5 on VID-REF-01/02; (3) Wan 3.0 on VID-I2V-*; (4) VID-MS-02; (5) VID-REF-02 Kling-elements arm; (6) Seedance 2.5 on i2v items; (7) VID-2SPK-01 chain arm; (8) MUS-02; (9) VID-KNEE-01 Veo full tier; (10) Wan 3.0 on VID-T2V-*. Never cut: repeats, any core item, any Hindi item, TOPO-02/03 arms A and C.

## D. Cost and call count (`COST-TABLE.yaml`)
Rows = route × case × arm with `calls = items × repeats`, `unit_price`, `price_status: pinned|unpinned|plan_indicative`, `price_ref` (EVAL-039 pin path or `STAGE-A-ROUTE-PRICE-REFRESH-2026-08-26.yaml` marked stale), `billing_pool`, `tranche`. Pools: Google routes → Vertex credits; gpt-image-2 / FLUX.2 Pro / Sora 2 / MAI → Azure credits **only if the Controller deploys them**, else fal cash (gpt-image-2, FLUX.2 Pro) or excluded (Sora 2, MAI); SD3.5 → Bedrock credits; fal-only routes → cash; Sarvam → Sarvam credits; ElevenLabs → cash. Totals: calls and USD per tranche per pool; unpinned lines summed separately and excluded from the proposed cap; evaluator lines (Cloud Vision ≈ per-image, ASR, VLM triage) as separate rows; Controller judging time in minutes. Fixed call counts: **1a = 186** (image 124 + t2v core 44 + 2SPK native 8 + TOPO3-B 4 + knee 6), **1b = 112** (i2v 36 + TOPO3 A/C 8 + ref2v 8 + multi-shot 12 + TTS 20 incl. 2SPK drives + lipsync 12 + 2SPK chain 8 + music 8), **total 298**, plus 32 conditional calls listed but not in the cap (credit-only: SD3.5 8, MAI-Image-2.6 8, Sora 2 8, Chirp 3 HD / Azure Neural TTS on the Hindi script 2 + 2; cash-if-pinned: Kling v3 elements on VID-REF-* 4). Any deviation from these counts is written in `README.md` with the reason. INFERRED planning figure from plan §C.3 prices, to be replaced by pins: ≈ USD 150–165 nominal, of which ≈ USD 45–55 credit-eligible; above the plan's 1a ≈ 60 line — the Controller decides between the cut order and a higher 1a cap.

## E. Rules the Executor must obey
1. USD 0: no generation, no evaluator, no OCR, no LLM API call; blueprints and requests are authored by the Executor agent itself; `blueprint_author: executor_agent`.
2. Canon by id only: every blueprint decision cites `PA-Dn`/`CA-Dn` and every pre-dispatch line cites `*-check`; no paraphrased doctrine; accepted Canon only; no HOLD ids; nothing attributed to uncompiled packs or to audio.
3. No invented prices, ids or surfaces: `unpinned` / `needs_controller_enablement` / `no_access` are the only honest alternatives.
4. Every `customer_request` cites its real-demand source id and lists every adaptation, or is `fixture` with a reason; no request is benchmark-phrased; Hindi/Hinglish as the market dictates, never "because the client is Indian" (marketplace bank rule).
5. The Normalized Request records only what the customer said or what follows directly; production choices carry `system_derived` with a rationale; `requested_operation` never takes a route value.
6. One blueprint per case, held byte-identical across routes; route differences live in `routes[].params` only.
7. Write nothing outside `eval/empirical-planning/STAGE-A-FREEZE-2026-09/`; never touch `coordination/`, `canon/`, `resources/`, sealed evidence, or any existing file.
8. Reference/supplied assets are specified, not fetched or generated; rights rule recorded per asset.
9. No sub-agents; no git commit by the Executor (the Controller session commits); no force-push; no deletion.

## F. Acceptance criteria
**Tester (mechanical; all must pass):**
1. `TEST-CASES.yaml`, `SEED-POLICY.yaml`, `EVALUATOR-PLAN.yaml`, `COST-TABLE.yaml` parse with `python3 -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1]))'`.
2. 35 `case_id`s, unique, matching §B.1 exactly; every case has every §A.1 field; every `blueprint_ref` and `test-cases/` file exists and `blueprint_sha256` matches.
3. `nr.requested_operation` ∈ the seven values; no forbidden route value in any NR field; `capabilities.primary` ∈ contract-v2 active ids; `repairability` never primary; all 13 condition families present per case.
4. Coverage checks B.2 items 1–8 pass (8 via grep list).
5. Every `route_id` in `COST-TABLE.yaml` appears in plan §C.3/§C.3c/§C.3d or is marked conditional; every surface matches the survey §6; every row has `billing_pool` and `price_status`; call totals equal 186 / 112 / 298 (+32 conditional) or `README.md` explains the delta.
6. Every cited source id exists (`MKT-nnn` in the marketplace bank; `BR-Fnn-XX` in `briefs.jsonl`; `RX-nn` in the extension; `B0n` under EVAL-038 payloads); no `MKT-015`, `MKT-016`, `RX-11`.
7. Every blueprint cites only ids present in the two compiled packs; grep finds no HOLD source id (desai, airey, freeman-beyond, samara-ch2, ries) and no uncompiled pack quoted as doctrine.
8. `ELIMINATION-RULES.md` contains E1–E5 byte-identical to plan §C.4 plus the survivor cap.
9. `git diff --stat` touches only the deliverable directory; no file deleted or modified elsewhere.

**Auditor (adversarial; report, do not fix):**
1. Read every request as a studio would receive it: is it genuinely how a buyer writes, in the right language for that buyer, with attachments named? Flag any request a benchmark author would recognise as theirs.
2. Can each acceptance contract be decided from the artifact alone by a blind judge, consistently, with no route/arm/Canon leakage and no hidden rubric?
3. Is every blueprint decision doctrine-by-id with the case-specific value filled, and is the same generation prompt truly reusable across all listed routes (no route-specific wording hidden in the prompt)?
4. Is anything mislabelled as Registry-eligible? Only the 8 deterministic capabilities may appear as T-DET; text, identity, dialogue, music and acceptance must sit in T-BENCH/T-HUMAN/T-SCREEN.
5. Could any case be dropped or merged without losing a §C.1 answer? Is any Media Factory prior being re-proved from zero rather than freshness-tested where a routing decision depends on it?
6. Are the "fixture" cases the minimum, each with a reason no source pool could supply?
7. Does the NR anywhere attribute a system choice to the customer (grammar provenance rule)?
8. Are unpinned prices excluded from the proposed cap, and are credit-pool routes correctly conditional on Controller enablement?

**STOP CONDITIONS:** any action that would bill a provider or call an LLM API; a case that cannot be mapped to the grammar without inventing a customer statement (record `blocked`, continue others, stop if > 3); a route whose surface is not in the survey; any need to edit a file outside the deliverable directory; a compiled pack failing `python3 canon/validation/validate_compiled_pack.py` (integrity — stop and report); ARCHITECTURE / SCOPE / EXPERIMENT-MUTATION triggers of `shared/AUTONOMY-POLICY.md`.

**HUMAN APPROVAL TRIGGERS (recorded in `README.md` as morning decisions, never attempted):** (1) ratify this task and the counts (35 cases / 298 + 32 conditional calls) or apply the cut order; (2) Sarvam key present? (else AUD-TTS-* run on ElevenLabs only and TOPO-01 arm B loses its Indic voice); (3) Azure deployments for gpt-image-2 / FLUX.2 Pro (credits) and whether Sora 2 / MAI-Image-2.6 join; (4) Bedrock access for SD3.5 Large; (5) Runway account for VID-04 (else stays deferred); (6) Controller-supplied photos for IMG-EDIT-01/02, IMG-EXT-01, IMG-COMP-01, IMG-REF-*, VID-REF-* (or accept constructed/Resources items with the stated rights rule); (7) Seedance 2.5 policy: 2 items × 2 repeats (this task) vs the plan's 4 single draws; (8) 1a cap: raise above ≈ USD 60 or cut; (9) lipsync drive route (ElevenLabs default vs Sarvam); (10) Lyria id (`lyria-002` observed vs "Lyria 3" in the plan); (11) whether the image core's fourth slot is the policy-edge scene (this task) or the plan's flat-lay + Indian-market scene (contradiction 3).

**RESULT LOCATION:** `eval/empirical-planning/STAGE-A-FREEZE-2026-09/` on branch `controller/capability-lab-direction-2026-09-05` in the worktree `media-intelligence-wt-controller` (same convention as the sibling EVAL-039B: the Controller session commits, the Executor does not — this supersedes rule E.9 wording about a work branch; price references point at EVAL-039B's `ROSTER-REFRESH-2026-09.yaml` / `price-pins-2026-09/` once they exist, else `unpinned`); Executor report at `eval/tasks/EVAL-039A-EXECUTOR-REPORT.md`; Tester and Auditor reports at `eval/tasks/EVAL-039A-TESTER-REPORT.md` and `EVAL-039A-AUDITOR-REPORT.md`; Approver verdict appended to the Controller Brief of EVAL-039.

---

## Planner notes — contradictions observed in the repository against the plan (OBSERVED unless marked)
1. Plan §C.3d names "Lyria 3 on Vertex"; the survey observed only `lyria-002` GA on the publisher endpoint. Music routes carry `unpinned` until EVAL-039 resolves the id.
2. Plan §C.3 gives Seedance 2.5 "4 gens not 8" on a 4-item core (one draw per item); `STAGED-EXECUTION-PLAN.yaml` stage A says repeats stay at 2 and breadth is deferred instead. This task follows the frozen rule (2 items × 2). Controller decision 7.
3. Plan §C.1 lists four image-core shapes (product hero, person lifestyle, Indian-market scene, flat-lay) *and* one policy-edge item per lane core — five shapes for four slots. This task folds the Indian-market scene into the Hindi policy-edge item. Controller decision 11.
4. Plan §C.1 says the composite arm "costs zero provider calls"; a textless base plate still needs a draw. This task charges 2 base draws per text case to arm C and keeps the compositing step at USD 0.
5. The marketplace bank has no runnable Hindi/Hinglish case (MKT-015 blocked, MKT-016 not runnable); Hindi/Hinglish demand shapes come from the 30-bank and RX items, so the language-mix target rests on those pools. INFERRED: adequate, since the 30-bank is 10/10/10 by language.
6. `pack-triggers-v0.yaml` gives audio zero Canon coverage; "all productions use Canon" is satisfied for TTS/music/lipsync by the mandatory coverage-gap notice, not by doctrine. The Auditor must accept that as the honest state, not a defect.
7. EVAL-040 estimates ≈ 246 generations; this package fixes 298 (+ 32 conditional). The added §C.3d scope (+ 25–30 USD in the plan's own estimate) and the extend/compose/two-speaker-chain items account for the difference.
8. EVAL-039 says "video core 4 incl. one Hindi dialogue item" while §C.3d adds "one two-speaker Hindi dialogue item"; this task keeps both (single-speaker in the core for a clean TOPO-01 comparison; two-speaker as the added-scope item).
9. `CANON-SHAPE-v1.md` §4 has "a reasoning model" write the blueprint; rule 13 of the direction allows "model or agent". At USD 0 the Executor agent authors and is recorded as author; a model-authored blueprint would be a separate, spend-bearing task.
10. `CONTROL-STATE.md` (1 Sep) still says "no new paid tranche is authorised" and "next gate is the gate build"; the 5 Sep direction is DRAFT. Nothing in this task spends, so no conflict is created, but the Executor must not read this task as evidence that the direction is ratified.
