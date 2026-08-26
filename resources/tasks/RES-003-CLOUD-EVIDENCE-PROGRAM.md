# RES-003 — Cloud Evidence, Independence & Outcome-Persistence Program

**AUTONOMY MODE:** autonomous  
**Environment:** Claude Web/cloud only  
**Branch:** `work/res-003-evidence-topology`  
**Budget:** ₹0  
**Shared program:** `coordination/plans/2026-08-26-CLOUD-MACRO-SCOPE-AND-READINESS-PROGRAM.md`

## Objective

Prepare the evidence side of the next empirical program: verify source/access/rights/provenance for request and evaluation data, reassess resource fit from committed evidence, design protected-set/leakage rules, and propose whole-outcome/multi-parent persistence for CpAO.

Resources does not define customer demand, creative quality or Eval metrics.

## Work packages — execute as one program

### R3-A — Request/evaluation source access & rights map

Research the public evidence sources likely to matter to Canon/Eval's macro work, including where relevant:

- DiffusionDB;
- VidProM;
- TIP-I2V;
- Arena Image / Arena-T2I-Hard data or methodology artifacts;
- benchmark datasets/resources used by modern image/video/audio evaluation work;
- controlled-product/person/AV/commercial-creative candidate routes already identified in Resources V1.

For each, record separately:

- publisher/creator/distributor;
- access route;
- authentication or terms gate;
- dataset/annotation licence;
- underlying-media rights where stated;
- redistribution status;
- internal research/evaluation suitability;
- whether prompt/request text can be accessed or only aggregate methodology;
- source lineage / known derivation relationships;
- approximate scale from source-supported documentation.

No acquisition beyond small public documentation/metadata inspection.

### R3-B — Existing resource fit rebaseline from committed evidence

Reassess what the existing 34,786-item / 5.70GB historical corpus and V1 resource design can support under the widened scope.

This is a **metadata/evidence rebaseline only**. The raw git-ignored corpus is not available in cloud and must not be described as re-opened, re-decoded or re-hashed.

Map existing material against likely needs for:

- exact/brand text;
- product identity/reference conditioning;
- person identity/reference conditioning;
- temporal/multi-shot consistency;
- speech/audio/AV;
- creative/commercial judgement;
- longer/composed video outcomes;
- campaign/variant consistency;
- evaluator qualification.

Distinguish prior committed observation from fresh cloud verification.

### R3-C — Discovery/calibration/benchmark/holdout separation

Propose a protected-set and leakage model for the next program.

Explicitly separate roles for:

1. request-space **discovery** data used to learn the taxonomy;
2. benchmark-construction/training examples used to author or tune tasks;
3. evaluator **calibration/qualification** material;
4. active benchmark material;
5. untouched final holdout/regression reserves.

Address both byte-level and semantic/source-lineage leakage. Reuse the accepted Resources principle that hash independence does not prove content/source independence.

Prevent circularity such as deriving a request pattern from one source and then claiming generalization by testing on rephrases or descendants of that same source.

### R3-D — Outcome / production topology proposal

Extend the accepted V2.1 persistence architecture conceptually so it can represent one customer outcome assembled from many steps.

The proposal must support:

`job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact`

Preserve:

- one provider/API/transform call = one trial;
- failed/refused attempts persist;
- repeat != retry;
- measurements remain Eval-owned;
- costs use immutable provenance.

Add/propose:

- outcome-level acceptance distinct from diagnostic trial/unit acceptance;
- multi-parent artifact lineage for composition/assembly/mix/overlay;
- deterministic/local production steps that may create artifacts without provider attempts;
- ordered parents where sequence order matters;
- recoverable transformation/config provenance;
- backward-compatible legacy states rather than pretending old archives had outcome metadata.

This task proposes the contract and validators/fixtures. Do not rewrite the authoritative V2.1 schema as final cross-stream architecture without Controller integration.

### R3-E — Whole-outcome CpAO recomputation

Design a fail-closed recomputation contract for total cost of an accepted outcome.

It must include, where the project cost definition later chooses to count them:

- all paid generation attempts, including failed/retried attempts contributing to the outcome;
- paid transforms;
- evaluator/checker costs;
- human verification/review cost;
- material local/deterministic production cost when recorded;
- repair attempts.

Prevent double counting when one intermediate artifact/cost feeds several downstream steps.

Provide known-answer synthetic fixtures and negative cases if a runner exists; otherwise specify exact expected results.

### R3-F — Controlled-pack supply routes and scope delta

Revisit the four accepted V1 pack families:

- product references;
- person references;
- AV/speaker material;
- commercial creative.

Research legitimate creator/publisher/institution/public routes without acquiring them.

Check whether the widened request/workflow scope creates a concrete need to change:

- number/quality tiers of product/person reference views;
- cross-shot/cross-asset identity material;
- AV duration, speaker and pronunciation coverage;
- commercial sequence/video-duration examples;
- campaign/variant sets;
- protected reserve sizes.

Prefer richer metadata/usage of existing pack families over inventing new pack families. Any increase must name the specific consumer need it would serve.

## Required deliverables

Create under `resources/research/pre-e7-macro/`:

- `REQUEST-AND-EVAL-SOURCE-ACCESS-REGISTER.yaml`
- `SOURCE-ACCESS-RIGHTS-REPORT.md`
- `EXISTING-RESOURCE-FIT-REBASELINE.md`
- `PROTECTED-SETS-AND-LEAKAGE-PROPOSAL.md`
- `OUTCOME-PRODUCTION-TOPOLOGY-PROPOSAL.yaml`
- `OUTCOME-CPAO-RECOMPUTATION.md`
- `CONTROLLED-PACK-ROUTES-AND-DELTA.md`
- `RES-003-CONTROLLER-BRIEF.md`

The Controller Brief must separate OBSERVED/PREVIOUSLY-COMMITTED / SOURCE-SUPPORTED / INFERRED / PROPOSED / UNKNOWN.

## Evidence standard

- Rights/access facts come from creator/publisher/dataset/provider documentation where possible.
- Do not infer underlying-media rights from a code licence.
- Unknown lineage stays indeterminate.
- Do not report historical decode/hash observations as freshly rerun.
- No creative labels or Eval thresholds.
- A source useful for discovery is not automatically suitable for calibration or holdout.

## Cloud rules

Assume no raw git-ignored corpus, local media, Downloads or laptop credentials. Use committed manifests/reports/source records and public web evidence.

If code execution exists, run only validators/fixtures on committed/synthetic material. Never run raw-corpus-dependent scripts in a way that could overwrite degraded reports.

## Hard prohibitions

- no materially new dataset/media acquisition;
- no login/account creation/click-through terms/payment;
- no generation/evaluator API calls;
- no creative-quality labels;
- no Eval threshold decisions;
- no merge;
- no editing another stream's files.

## Stop conditions

An optional gated source may be recorded as blocked/unavailable and research may continue to other pre-approved candidates. Stop and escalate if resolving a gate is necessary to complete the objective, a legal/permission decision is required, architecture must be changed to proceed, or unreliable evidence would contaminate conclusions.

## Completion

Commit and push the branch. Return a concise chat report explaining what evidence we can actually obtain independently, where leakage/rights risks are, whether the current four-pack plan survives, what outcome-level persistence must change, and what the Controller must decide at integration.
