# Task EVAL-039: September-2026 roster refresh and Stage A freeze package

**TASK ID:** EVAL-039
**STATUS:** DRAFT — authorised only when `coordination/decisions/CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` is ratified and merged.
**OBJECTIVE:** Produce a price-pinned, route-verified, item-frozen Stage A package such that the Controller can authorise Tranche 1 by naming exact models, call counts and a hard cap — with zero paid calls spent getting there.
**WHY WE ARE DOING THIS:** The programme's most commercially useful missing asset is a current, conditional model/workflow routing map. The August roster is stale (candidate identities, prices, promotions, provider access). Stage A cannot be authorised until every figure is current and every elimination rule is pre-registered.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`.

## CONTEXT CONTRACT

**Inherits `shared/CONTEXT-SUFFICIENCY-POLICY.md`.**

### BASE STATE
- **BASE MAIN SHA:** `599ff4af6a1f0684132303687e438877da47a004` (re-base on the post-CANON-GATE-001 `main` when it lands; the gate is a read-only dependency).

### REQUIRED ORIENTATION
The default bootstrap in `coordination/RUNBOOK.md`, plus `coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md` §C–§E.

### TASK-SPECIFIC CONTEXT
- `eval/pre-execution-freeze/SCIENTIFIC-WAVE1-MODEL-ROSTER.{md,yaml}` — the questions; candidates are stale.
- `eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml` — capability ids only (no whole-file read needed beyond ids and `registry_conditions` of the capabilities named in the plan).
- `eval/pre-execution-freeze/CONDITION-ENVELOPE-CONTRACT.yaml` — the 13 families; `actively_swept_in_wave1`.
- `eval/pre-execution-freeze/EVALUATOR-QUALIFICATION-MAP.yaml` — the 8 `yes_deterministic` capabilities and Q1 material.
- `eval/pre-execution-integration/STAGED-EXECUTION-PLAN.yaml` — Stage A rules (repeats 2, seed policy requirement, metrics permitted/forbidden).
- `eval/empirical-planning/STAGE-A-ROUTE-PRICE-REFRESH-2026-08-26.yaml` — the August pins to supersede (format precedent).
- `eval/pre-execution-freeze/model-supply/PRICE-VERIFICATION.yaml` — pinning format precedent.
- `eval/experiments/EVAL-038/common/` — the bytes+sha+date price-pin pattern.
- `eval/empirical-tranche-1/providers.py`, `eval/pilot-substrate/video_route.py`, `eval/experiments/EVAL-038/tools/generate_media.py` — the live-proven adapters to extend, not replace.
- `eval/v1/instruments/FAMILY-2-DETERMINISTIC-CV.md`, `eval/v1/instruments/fixtures/cv-geometry/` — Q1.
- `~/Vaibhav_Personal_Projects/media-factory-controller-handoff.zip` — the four markdown files and `EVIDENCE-MANIFEST.json` only.
- `eval/tasks/EVAL-036-MEDIA-FACTORY-HISTORICAL-PRIORS.md` — the original (larger) import spec; this task executes its compact form.

### BROAD READS
`eval/v1/harness/**` — BROAD READ JUSTIFICATION: the Registry writer and instrument model must be reused exactly; the adapters plug into it.

### EXPANSION TRIGGERS
Any route whose pricing unit is ambiguous (per second vs per video vs tokens) → read the vendor page in full and record the unit verbatim; never normalise silently.

### EVIDENCE HANDLING LEVEL
`validator_summary` for repository state; `full_raw_evidence` only for the vendor pages being pinned.

### CONTEXT INSUFFICIENCY
If a route's exact id, version or price cannot be established from a primary vendor/aggregator page, record it as `unpinned` and exclude it from the Tranche 1 cost; do not guess.

**INPUTS:** as above.

**IN SCOPE (deliverables, all USD 0):**
1. `eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml` — for every route in plan §C.3: exact route id, model version string, **provider surface chosen under the cloud-credits-first rule** (Bedrock / Vertex / Azure Foundry / Google direct / fal), the model id on that surface, `billing_pool: credits | cash`, billing unit verbatim, regular price, any promotion (recorded, flagged, not used), supported durations/resolutions/refs/audio, seed support, key availability on this machine (name only, never value), `route_status: pinned | unpinned | no_access`. Input: `eval/empirical-planning/CLOUD-MODEL-AVAILABILITY-2026-09-05.md`. Never enable, deploy or subscribe to a cloud model — that is a Controller action; record `needs_controller_enablement` instead.
   1a. The TOPO-02 / TOPO-03 cheap exact-text topologies (plan §C.3b) are itemised in the freeze package with their three arms and the cheap-route candidates (Nano Banana 2 / Gemini Flash image tier, GPT Image 2, Qwen Image 3) named explicitly. Each price pinned with fetched bytes + sha256 + UTC timestamp under `eval/empirical-planning/price-pins-2026-09/`.
2. `eval/historical-priors/media-factory-v1/` — copies of `MEDIA-FACTORY-ROUTING-PRIOR.md`, `MEDIA-FACTORY-EMPIRICAL-FINDINGS.md`, `COST-SUMMARY.md`, `PROMPT-ENRICHMENT-EVIDENCE.md`, `EVIDENCE-MANIFEST.json`, each with sha256 recorded in `PRIOR-INDEX.yaml`; every row marked `tier: historical_prior`, `freshness_required: true`. No media copied. No Registry rows.
3. Harness adapters: fal video (t2v, i2v, reference-to-video), fal TTS, fal lipsync; reuse of the Google direct lifecycle for Veo (t2v, i2v, reference) and Gemini image. Each adapter: construction opens no socket; key read at dispatch only; `num_outputs` pinned to 1; 0 retries; reservation-before-send through the existing ledger. Tests with injected transports only (`python3 -m unittest`).
4. Deterministic instruments as code with tests: delivery-format probe; masked-diff edit preservation; brand-colour distance in a masked region; A/V offset for lipsync (we supply both inputs); seeded/unseeded repeat hash + SSIM; ledger-derived latency/error/refusal/cost. Each registered in the harness with `qualification_status: deterministic` and a `pass_criterion_ref`.
5. **Q1 run:** deterministic CV geometry qualification over the 102-item fixture pack, with `R_q` declared before running; result file under `eval/v1/instruments/qualification-records/`. No provider call.
6. **Stage A freeze package** `eval/empirical-planning/STAGE-A-FREEZE-2026-09/`:
   - concrete executable prompts for every core item (image core 4, video core 4 incl. one Hindi dialogue item, one high-motion item, one policy-edge item; TTS 3 scripts; lipsync 3), each with a written acceptance contract the Controller will judge against blind;
   - reference inputs for IMG-04 / VID-03b (product and person) **with same-category decoys** — sourced from Resources' rights-cleared corpus or constructed; provenance recorded;
   - the shared hero still for VID-03a (chosen from the image core after the Controller's blind acceptance of Tranche 1a — so 1b depends on 1a);
   - seed policy per route (`seed_supported`, `policy: unseeded_inherent_variance` default);
   - pre-registered elimination rules E1–E5 exactly as in the plan §C.4, plus the survivor cap of 3 per question;
   - evaluator plan per item (which T-DET / T-BENCH / T-HUMAN / T-SCREEN instruments fan out);
   - blind-judging protocol (EVAL-038 pattern: strip, commit, keys off-repo);
   - **exact Tranche 1 cost table** by route × item × repeat, split 1a / 1b, with evaluator lines, and the proposed hard caps.
7. Controller Brief `eval/tasks/EVAL-039-CONTROLLER-BRIEF.md` with OBSERVED / INFERRED separated, listing every `unpinned` and `no_access` route and what the Controller must decide.

**OUT OF SCOPE:** any paid call (generation, evaluator, or "liveness ping" that bills); any Registry row; Stage B/C item authoring; Canon pack work; edits under `coordination/`, `canon/`, `resources/`.

**AUTONOMY MODE:** autonomous — method frozen above; stop conditions explicit.

**RESOURCE BUDGET:**
- API spend: **USD 0** (network fetches for price pinning are authorised; nothing that bills).
- generations/retries: 0 / 0.
- storage: price-pin HTML ≤ 5 MB total; no media.

**APPROVED DEPENDENCIES:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` (ratified); CANON-GATE-001 merged (read-only use of `canon/gate/run_gate.py post` as a structural check in the evaluator plan).

**STOP CONDITIONS:** any action that would bill a provider; a route whose billing unit cannot be read verbatim; a reference input whose rights are unclear; any temptation to author Stage C briefs (Eval authors no customer briefs — the pool is CANON-011 / CANON-010 / EVAL-037).

**ADDED SCOPE (Controller, 5 Sep):** the freeze package must also itemise: one 15-second item (routes that support it); one two-speaker Hindi dialogue item on native-audio routes and on the TTS + lip-sync chain; a small music lane (Lyria 3 on Vertex vs ElevenLabs music on fal, 2 briefs × 2); 4K recorded as a Stage B delivery level only. See plan §C.3d.

**PROVIDER SURFACE FACTS TO CARRY (from the 5 Sep survey):** Google routes on Vertex (`vertexaiproject-507518`) against credits; GPT Image 2 and FLUX.2 Pro on Azure only after the Controller deploys them (`gpt-image-2` needs a resource in eastus2 / swedencentral / westus3 / uaenorth / polandcentral); Imagen 4 and Nova are dropped (retired / end of life); Sora 2 preview and MAI-Image-2.6 added as Azure candidates; SD3.5 Large added as a Bedrock candidate (us-west-2 only); every Azure command must pass `--subscription b832f4a1…` and the adapter must refuse otherwise; Sarvam runs direct against Sarvam credits with `SARVAM_API_KEY` from `~/.mi-keys` (Controller holds the key; never printed).

**HUMAN APPROVAL TRIGGERS:** Runway account (VID-04) — ask, never create; Azure deployments of gpt-image-2 / FLUX.2 Pro; Bedrock model access; credit balances on the three clouds; acceptance of the freeze package; the spend authorisation itself.

**RESULT LOCATION:** `eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml`, `eval/empirical-planning/STAGE-A-FREEZE-2026-09/`, `eval/historical-priors/media-factory-v1/`, `eval/tasks/EVAL-039-CONTROLLER-BRIEF.md`, branch `work/eval-039-roster-refresh`.
