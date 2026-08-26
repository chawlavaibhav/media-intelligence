# EVAL-008 — Cloud Model Roster & Access Research

**AUTONOMY MODE:** autonomous  
**Environment:** Claude Web/cloud only  
**Branch:** `work/eval-008-model-access`  
**Budget:** ₹0  
**Relationship to EVAL-007:** parallel and independent. EVAL-007 studies capability/evaluator/workflow semantics; EVAL-008 studies the actual model/provider supply universe and access requirements. Neither finalizes the paid benchmark roster.

## Objective

Build a current, evidence-backed candidate universe of image/video/audio generation models and the routes through which we can access them, so the Controller can later choose a compact paid benchmark roster after CANON-009 / EVAL-007 / RES-003 integration.

The task must answer:

1. Which model families are serious candidates for our commercial-media product?
2. Which production lanes does each support: image generation/editing/reference work, T2V, I2V, V2V/edit/extend, native AV, TTS, lip-sync/avatars, upscaling where materially relevant?
3. Where can each model be called: direct vendor API, fal, Runway API/router, Google/OpenAI/Alibaba/etc., or another legitimate production API?
4. Where the same underlying model exists through multiple providers, are the routes materially equivalent or should they become separate workflow evidence?
5. Which accounts/credits/API approvals would the user need before empirical testing?

## Important user-reported access

- User reports existing access to **fal**.
- User reports access to **“Frontier clouds”**; exact provider identity is not established in repository evidence. Record this as `user_reported_access_unverified_provider_identity` unless the worker can unambiguously identify the service from public evidence. Do not guess.
- Do not inspect or assume laptop credentials/API keys.

## Research principles

- Use **official provider documentation** for current model identity, API availability, supported operations, limits and direct-provider pricing.
- fal/Runway/other aggregators may be authoritative for what they themselves expose and charge through their route.
- Do not treat aggregator marketing copy as proof of an underlying vendor capability when the vendor docs disagree or are silent.
- Capture exact date and model/version/endpoint where exposed. Avoid generic “latest”.
- Do not benchmark or call any paid API.
- Do not propose testing every model available on an aggregator.

## Candidate-selection philosophy

The deliverable should produce a **compact proposed research roster**, not a catalog dump.

For each production lane, seek a mix of:

1. **frontier/generalist candidates** — strongest current broad models likely to matter commercially;
2. **specialists** — models with materially distinctive strengths such as typography, design/vector output, identity/reference conditioning, native audio, multi-shot control, lip-sync, etc.;
3. **cost/latency baselines** — materially cheaper models that could win on Cost per Accepted Outcome even if raw quality is lower;
4. **open/self-hostable baselines** where realistically production-relevant;
5. **workflow alternatives**, not duplicates for their own sake.

A candidate earns a slot because it represents a plausible production choice or a distinct capability/cost frontier, not because it is famous.

## Work packages

### E8-A — Provider/access landscape

Research at minimum:

- fal;
- OpenAI direct;
- Google Gemini / Vertex AI direct;
- Runway API;
- Black Forest Labs / FLUX direct where relevant;
- Ideogram direct where relevant;
- Recraft direct where relevant;
- ByteDance/Seedance access routes;
- Kling access routes;
- MiniMax/Hailuo access routes;
- Alibaba Model Studio / Wan;
- Luma;
- ElevenLabs or equivalent TTS/voice where relevant;
- Sync Labs or equivalent lip-sync where relevant;
- any clearly stronger/current provider discovered during research.

For each provider record:

- account/signup route;
- API availability;
- billing model/minimum top-up if stated;
- geographic/business-access restrictions if stated;
- exact models/operations relevant to us;
- whether user likely needs a separate account given fal access;
- whether direct access offers a materially different workflow/control/version pinning than fal.

### E8-B — Model/workflow matrix

Create one normalized row per **underlying model family × materially distinct access/workflow route**.

Fields should include where available:

- vendor;
- model family;
- exact model/version/endpoint;
- provider/access route;
- direct vs aggregator;
- image/video/audio modality;
- supported operations;
- input types and reference controls;
- native duration/output limits;
- resolution/aspect ratios;
- native audio;
- text/dialogue/voice features;
- first/last-frame or multi-reference controls;
- edit/mask/extend/V2V capability;
- seed/reproducibility/version pinning;
- pricing unit/current price;
- known rate/concurrency restrictions;
- commercial-use/API status as stated by provider;
- source URL and checked date.

Do not collapse two materially different routes into one row.

### E8-C — Deduplication and route analysis

For models available through fal, Runway and/or direct vendor APIs, identify:

- same underlying model, likely equivalent route;
- same family but different version;
- aggregator wrapper adds/removes controls;
- pricing difference;
- version-pinning difference;
- rate-limit/latency/availability difference;
- terms/commercial-access difference.

Recommend when only one route needs initial testing and when route itself is a variable worth measuring.

### E8-D — Proposed compact candidate roster

Propose candidates by lane, with rationale and **priority tiers**, not final authorization:

- image: text-to-image / commercial creative;
- image: editing/reference/identity/product work;
- image: typography/design/vector specialist if distinct;
- video: T2V;
- video: I2V/reference-conditioned;
- video: edit/V2V/extension/multi-shot;
- native audio video;
- speech/TTS;
- lip-sync/avatar where it is a separate production step.

For each proposed candidate explain which different hypothesis it lets us test. If two candidates answer essentially the same question, prefer the stronger/cheaper one and mark the other reserve.

### E8-E — User account/action checklist

Create `ACCOUNT-ACTIONS.md` with three buckets:

1. **Already likely covered by fal** — no new signup unless direct route is experimentally necessary.
2. **Worth opening now** — direct accounts that unlock models/controls not adequately represented through fal or provide needed exact-version evidence.
3. **Wait until roster freeze** — accounts that add little before Controller integration.

For every action state:

- exact service;
- why we need it;
- whether free signup is enough for research;
- whether payment/credits are needed only later;
- whether any manual approval/business verification is known;
- what not to buy yet.

Do not ask the user to prepay anything in this task.

## Deliverables

Create under `eval/model-access/2026-08-26/`:

1. `PROVIDER-ACCESS-LANDSCAPE.md`
2. `model-workflow-matrix.yaml` or `.jsonl`
3. `ROUTE-DEDUPLICATION.md`
4. `PROPOSED-CANDIDATE-ROSTER.md`
5. `ACCOUNT-ACTIONS.md`
6. `EVAL-008-CONTROLLER-BRIEF.md`

## Stop / escalation

Stop and report rather than deciding if:

- a provider requires accepting nonstandard terms or business verification to inspect API access;
- a model cannot be identified/versioned well enough to make evidence interpretable;
- the candidate universe becomes so large that a new selection methodology is required;
- completing the research would require paid calls or account credentials;
- evidence materially contradicts current Controller architecture.

Otherwise continue through all work packages autonomously.

## Completion standard

The Controller should be able to read the output and answer, without more discovery work:

- the serious model families worth considering;
- the minimum set of distinct access providers needed;
- which models can be covered through fal alone;
- which direct APIs are still strategically useful;
- what accounts the user should create before paid benchmarking;
- what remains uncertain until EVAL-007/request-space integration.

No paid calls. No benchmark execution. No Registry rows. No merge.