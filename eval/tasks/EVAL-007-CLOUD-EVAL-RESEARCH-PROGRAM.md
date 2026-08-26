# EVAL-007 — Cloud Capability, Evaluator & Workflow Research Program

**AUTONOMY MODE:** autonomous  
**Environment:** Claude Web/cloud only  
**Branch:** `work/eval-007-capability-workflow`  
**Budget:** ₹0  
**Shared program:** `coordination/plans/2026-08-26-CLOUD-MACRO-SCOPE-AND-READINESS-PROGRAM.md`

## Objective

Independently research the modern capability/failure/evaluator/workflow space for image, video and audio generation so the Controller can refreeze Eval after request-space and Resources evidence return.

This task treats the current 36 capabilities, six evaluator families and 100-item bank as useful baselines, not as proof that scope is complete.

## Work packages — execute as one program

### E7-A — Modern benchmark and failure landscape

Review current, high-quality evaluation work across image/video/audio where relevant. Seed families include:

- GenEval and GenEval 2;
- T2I-CompBench and related compositional benchmarks;
- VBench and later video-evaluation work;
- Arena-T2I-Hard / real-user hard-prompt evaluation;
- human-alignment / evaluator-calibration work relevant to image/video quality;
- speech/lip-sync/audio evaluation where it maps to our product.

For each, record:

- what capability/failure dimension it actually tests;
- observation unit;
- evaluator/judge method;
- whether the benchmark is atomic, compositional, preference-based or end-to-end;
- known limitations, judge drift, contamination or human-alignment concerns;
- what lesson transfers to our system and what does not.

Do not copy an external benchmark taxonomy wholesale.

### E7-B — Current production workflow/API inventory

Complete and broaden E2 using **official current provider documentation only** for model identity, availability, limits and price.

Research credible current candidates across:

- image generation/editing;
- general video generation;
- native audio-video;
- lip-sync / digital-human transforms;
- TTS / voice;
- useful direct vs aggregator access where materially different.

For every evidenced workflow/endpoint record, capture where officially exposed:

- provider, exact model/API id/version;
- current availability/access path and relevant region limits;
- direct vs aggregator;
- billing unit and current price with source URL/read date;
- native duration range;
- T2V/I2V/edit/extension support;
- first/last-frame controls;
- reference support type/count;
- mask/edit controls;
- character/product conditioning;
- native audio support;
- supported aspect ratios/resolutions;
- camera/motion controls;
- seed/reproducibility controls;
- version pinning or lack of it;
- concurrency/rate constraints relevant to production.

If an official page is inaccessible or ambiguous, mark the row unresolved. Do not fill from memory, reseller blogs or secondary price calculators.

No API calls are allowed.

### E7-C — External audit of the current 36 capabilities

Map every current capability against external benchmark/failure evidence and our product boundary.

Classify each as one of:

- externally supported and well scoped;
- supported but definition/observation unit may need refinement;
- likely a condition rather than a capability;
- overlaps another capability;
- product-important but weakly evidenced externally;
- candidate missing capability.

Explicitly inspect, without presuming the answer:

- exact spoken-script/content fidelity;
- camera/framing instruction fidelity;
- cross-shot / cross-asset identity consistency;
- sequence/state continuity beyond left-right spatial continuity;
- technical visual integrity such as flicker, transient corruption, warping or sudden softness;
- pronunciation/intelligibility/voice consistency;
- style-reference fidelity;
- campaign/variant consistency.

Do not target a preselected capability count and do not modify the authoritative capability contract in this task.

### E7-D — Condition / production-envelope evidence map

Research operating conditions that materially change model/workflow behaviour or interpretation of a score.

At minimum inspect evidence for:

- duration;
- shot count / sequence structure;
- reference type/count/quality;
- resolution/aspect ratio;
- people/product/entity counts;
- action and camera-motion complexity;
- constraint/exactness load;
- language/script/speaker topology;
- workflow mode (T2V/I2V/extension/edit/ref-conditioned/composite);
- input quality;
- single asset vs variant/campaign scale.

Keep three things separate:

1. **capability** — what can succeed/fail;
2. **condition** — under what circumstances it was measured;
3. **Planner decision** — a production choice that may be absent from the customer request.

Do not collapse conditions into one complexity score.

### E7-E — Evaluator/instrument landscape and qualification proposal

Reassess the six evaluator-family baseline:

1. text/OCR;
2. deterministic/CV geometry;
3. structured visual VLM;
4. temporal/video;
5. speech/audio/AV;
6. creative/commercial.

For each family, determine:

- what can genuinely be deterministic;
- what requires a learned/model judge;
- what qualification/reference material is needed;
- what human role remains necessary;
- important false-pass risks;
- what evidence would qualify it for a hard gate vs descriptive diagnosis;
- known modern evaluator-drift/human-alignment issues.

No checker/evaluator API calls. Do not declare an instrument qualified.

### E7-F — Benchmark v2 proposal and provisional economics

Using only this stream's evidence, propose — do not freeze — a benchmark architecture that the Controller can later integrate with Canon request-space findings and Resources constraints.

Principles:

- request/use-case coverage and technical capability coverage are separate axes;
- generate once / measure many remains;
- keep atomic probes for causal isolation;
- use compound scenarios for realistic co-occurrence;
- add sparse/adaptive production-envelope sweeps instead of a cartesian product;
- compare materially different workflow topologies for the same outcome;
- reserve end-to-end customer-outcome tests for an integration-defined bank;
- include benchmark-refresh/audit triggers because models and evaluators drift.

Treat the existing 100-item bank as a baseline. Recommend exact changes only where evidence shows a concrete gap.

Build a **provisional** call/cost forecast from the current officially evidenced workflow roster. Unresolved prices remain null and must prevent a falsely complete total.

## Required deliverables

Create under `eval/research/pre-e7-macro/`:

- `BENCHMARK-LANDSCAPE.md`
- `benchmark-source-register.yaml`
- `CURRENT-WORKFLOW-INVENTORY-2026-08-26.yaml`
- `CAPABILITY-36-EXTERNAL-AUDIT.md`
- `CONDITION-EVIDENCE-MAP.yaml`
- `EVALUATOR-LANDSCAPE-AND-QUALIFICATION.md`
- `BENCHMARK-v2-PROPOSAL.md`
- `COST-FORECAST-PROVISIONAL.md`
- `EVAL-007-CONTROLLER-BRIEF.md`

The Controller Brief must separate SOURCE-SUPPORTED / INFERRED / PROPOSED / UNKNOWN.

## Research standard

- Current provider identity/access/pricing/features: official provider docs only.
- Benchmark/failure claims: prefer original papers/project pages and first-party repositories.
- Cite consequential claims and dates.
- Do not treat leaderboard scores from different benchmarks as directly comparable unless methodology supports it.
- Do not treat a benchmark dimension as market demand.
- Do not infer capability from provider marketing language without empirical evidence; provider docs establish interfaces/limits, not quality.

## Cloud rules

Assume no laptop API keys, local media or prior chat context. Public web + GitHub are the working surfaces.

If code execution exists, validators/parsers may be written and run on committed/synthetic data. If it does not, record `runtime_verification_blocked_no_runner` and do not claim execution.

## Hard prohibitions

- no generation API calls;
- no evaluator/checker calls;
- no Registry population;
- no paid spend;
- no Production IR or Planner implementation;
- no authoritative capability/schema rewrite;
- no merge;
- no editing another stream's files.

## Stop conditions

Do not stop merely because one provider's official page is inaccessible; mark that row unresolved and continue independent candidates. Stop and escalate only if the task requires an architecture decision, material scope expansion, paid/gated access, or unreliable evidence would contaminate the program.

## Completion

Commit and push the branch. Return a concise chat report explaining what the modern evaluation/workflow landscape changes in our thinking, which current capability assumptions look strong/weak, which conditions clearly matter, what remains unresolved, and what the Controller must decide at integration.
