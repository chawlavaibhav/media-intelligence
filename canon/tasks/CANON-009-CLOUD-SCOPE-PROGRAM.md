# CANON-009 — Cloud Request-Space & Creative-Requirement Program

**AUTONOMY MODE:** autonomous  
**Environment:** Claude Web/cloud only  
**Branch:** `work/canon-009-request-space`  
**Budget:** ₹0  
**Shared program:** `coordination/plans/2026-08-26-CLOUD-MACRO-SCOPE-AND-READINESS-PROGRAM.md`

## Objective

Research the recurring structure of real media-generation requests and commercial creative use cases, then compare that discovered space with Creative IR, the current 30 synthetic briefs and Canon coverage.

This task does **not** define market demand from 30 authored briefs. It does **not** modify the Canon corpus or select models.

## Work packages — execute as one program

### C9-A — Request-source landscape

Build an evidence table of substantial real-user or usage-informed media-generation request sources across:

- text-to-image;
- image editing/reference-based image work;
- text-to-video;
- image-to-video;
- where credible, commercial/marketing creative requests and creator/agency use cases.

Seed sources to verify and extend:

- DiffusionDB — real-user T2I prompts;
- VidProM — real-user T2V prompts;
- TIP-I2V — real-user text+image I2V prompts;
- Arena Image / Arena-T2I-Hard;
- Artificial Analysis image benchmarking methodology/use-case taxonomy.

For each source record: population, modality, time period, interface/community bias, what fields are available, whether frequency/co-occurrence can actually be inferred, and access/rights facts visible publicly.

Do not treat any one corpus as a proxy for total market demand.

### C9-B — Media Request Grammar

Derive a **proposed** grammar of recurring request components. At minimum inspect:

- requested operation: generate/edit/transform/extend/compose/variant;
- media/output type;
- subject/entity types;
- references supplied and their role;
- entity relationships/actions;
- identity/preservation requirements;
- text/logo/brand requirements;
- visual/camera/style requirements;
- motion/temporal requirements;
- speech/audio requirements;
- delivery/platform/format requirements;
- number of outputs/variants/campaign-set requirements;
- customer-specified vs commonly omitted production decisions.

Prefer evidence-backed frequency/co-occurrence where sources support it. When only qualitative evidence exists, label it qualitative.

Do not collapse the grammar into one complexity score.

### C9-C — Pattern/co-occurrence analysis

Identify recurring combinations that matter for production, for example product+person+reference, exact text+commercial design, person+speech+video, edit+preservation, multi-shot+identity continuity.

The purpose is to discover which combinations deserve direct benchmark coverage later, not to enumerate the cartesian product.

Record source-specific bias: a Stable Diffusion gallery, video prompt gallery and commercial design arena represent different user populations.

### C9-D — Compare existing project scope

Compare the proposed request grammar against:

- `canon/knowledge/SPEC-01-creative-ir.md`;
- `canon/experiments/v1/brief-bank/briefs-source.yaml`;
- current Eval 36-capability contract only as a comparison surface, not a constraint;
- live Canon knowledge coverage.

Produce four lists:

1. well represented;
2. present but underrepresented;
3. absent from the 30-bank but supported by request evidence;
4. present in the 30-bank with weak/no external support as a recurring pattern.

Do not edit the 30-bank. Produce a rebalance proposal only.

### C9-E — Creative-IR / Canon implications

Identify where observed request structures cannot be represented cleanly by the existing Normalized Request / Creative IR without confusing customer intent with Planner decisions.

Any schema/architecture change is a **proposal**, not an edit to frozen specs.

Also identify high-recurrence creative/production areas where Canon knowledge is thin. Do not start source acquisition or ingestion.

### C9-F — Value-gate consequence

Assess whether the existing Canon value-gate bank remains a defensible test surface after the request-space findings. Recommend keep/rebalance/replace specific scenario coverage, but **do not run the value gate** and do not author Canon-naive controls.

## Required deliverables

Create under `canon/research/request-space-v1/`:

- `SOURCE-LANDSCAPE.md`
- `request-source-register.yaml`
- `MEDIA-REQUEST-GRAMMAR-v1-PROPOSAL.yaml`
- `COOCCURRENCE-AND-PATTERNS.md`
- `CURRENT-30-BANK-COVERAGE-AUDIT.md`
- `CREATIVE-IR-AND-CANON-GAPS.md`
- `CANON-009-CONTROLLER-BRIEF.md`

The Controller Brief must separate SOURCE-SUPPORTED / INFERRED / PROPOSED / UNKNOWN.

## Research standard

- Prefer papers, dataset/project pages, official methodology pages and first-party documentation.
- Cite every consequential quantitative claim.
- Do not infer frequency from example lists.
- Do not combine percentages across differently sampled corpora into a fake global prevalence number.
- Distinguish prompts written for model interfaces from commercial briefs requesting outcomes.
- Do not treat benchmark-authored prompts as evidence of user demand.

## Cloud rules

No laptop files, Downloads, local books or raw Resources corpus may be assumed. Public web research and GitHub evidence are sufficient for this task.

If a public dataset is huge, inspect its paper/documentation/metadata or a legitimately accessible small sample. Do not download large payloads merely to say they exist.

## Hard prohibitions

- no new Canon source ingestion;
- no model/provider selection;
- no Production IR;
- no paid or free generation/evaluator API calls;
- no merge;
- no editing another stream's files.

## Stop conditions

Stop only if the task would require an architecture decision to proceed, paid/gated access, material acquisition, or evidence is too unreliable to support the requested research. Otherwise continue independent work and document limitations.

## Completion

Commit and push the branch. Return a concise chat report explaining the discovered request structure, strongest evidence, important blind spots in the current 30-bank/Creative IR, and what the Controller must decide at integration.
