# CANON-011 — Marketplace-Derived Benchmark Brief & Prompt-Ready Bank

**Owner:** Canon worker  
**Authority:** `coordination/decisions/CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PREP-2026-08-27.md`  
**Spend:** USD 0  
**External calls:** 0

## Objective

Turn the committed Upwork/Fiverr marketplace research into a bounded, provenance-preserving bank of
real-demand benchmark briefs and route-neutral prompt-ready cases.

Do not invent synthetic demand where the source already provides a real buyer job.

## Read first

- `canon/research/marketplace-demand-v1/README.md`
- all three files under `canon/research/marketplace-demand-v1/sources/`
- `canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml`
- `eval/pre-execution-freeze/BENCHMARK-v2-WAVE1.md`
- current Capability Contract / Stage map needed for mapping only

## Source discipline

- Upwork individual jobs = customer-intent source candidates.
- Fiverr gigs = commercial/package/input conventions only.
- Raw Fiverr capture = provenance/supporting record.
- If raw and cleaned reports disagree, record the discrepancy.
- Do not browse marketplaces again.
- Do not contact buyers/sellers.

## Build 12–20 cases

At least 8 must be runnable without contacting the source buyer.

Target mix:
- product/commercial video;
- UGC/spokesperson;
- supplied-script production;
- supplied-product-assets;
- recurring-character/identity;
- app/SaaS promo;
- batch/series;
- Hindi/Hinglish where source-supported.

Prefer explicit jobs over vague roles.

## Required per-case schema

Every case must carry:

`case_id`
`source_marketplace`
`source_record_id`
`source_title`
`source_file`
`source_facts_used[]`
`customer_brief`
`normalized_request`
`fixture_requirements[]`
`runnable_now`
`acceptance_contract`
`route_neutral_generation_brief`
`prompt_ready_envelope`
`capability_mappings[]`
`evaluator_dependencies[]`
`stage_fit`
`open_questions[]`

For each Normalized Request field include provenance:
- `customer_stated`
- `customer_implied`
- `experiment_supplied_fixture`
- `system_derived`
- `absent`

Never hide an experiment-supplied fixture as customer intent.

## Prompt-ready envelope rule

The prompt-ready envelope should be usable later by a model adapter, but must remain route-neutral.

It may contain:
- objective;
- deliverable;
- duration;
- aspect ratio;
- entities;
- product/person consistency requirements;
- text/script requirements;
- language;
- beats;
- CTA;
- brand constraints;
- supplied asset references;
- prohibited failure modes.

It must NOT contain:
- a model/vendor name unless the buyer explicitly required one and that fact is retained separately;
- an invented camera recipe;
- a specific image-to-video chain;
- LoRA/ControlNet/inpainting/etc. as customer intent;
- model-specific prompt hacks.

## Coverage report

Report:
- source jobs considered;
- selected cases;
- reason selected/rejected;
- requested-operation distribution;
- modality distribution;
- language distribution;
- supplied-asset distribution;
- character/product consistency coverage;
- exact-text coverage;
- batch/set-level acceptance coverage;
- evaluator dependencies;
- how these cases complement the existing 30-brief bank;
- which cases are strongest Stage-C candidates.

Explicitly call out where marketplace evidence corrects known gaps in the original authored bank.

## Validation

Add deterministic checks that:
- every case has source lineage;
- every Normalized Request field has provenance;
- no Fiverr seller gig is labelled as a buyer brief;
- no provider-specific route appears in route-neutral prompt fields unless it is quoted source metadata;
- runnable cases have all benchmark-supplied fixtures identified;
- ids unique;
- source file paths resolve.

## Output

Create:
- `canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml`
- `canon/research/marketplace-demand-v1/derived/marketplace-prompt-ready-bank-v1.yaml`
- `canon/research/marketplace-demand-v1/derived/COVERAGE-REPORT.md`
- validator(s)

Do not modify the historical 30-brief bank.
Do not run models.
Do not spend.
Push branch; do not merge.
Return to Controller.
