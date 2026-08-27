# Controller Marketplace-Derived Benchmark Brief Preparation — 2026-08-27

## Status

**AUTHORISED ZERO-SPEND PREPARATION LANE.**

Use the user-supplied Upwork/Fiverr research now committed under:
- `canon/research/marketplace-demand-v1/sources/`

to prepare real-demand benchmark briefs and prompt-ready test cases in parallel with evaluator work.

No model/API calls are authorised by this decision.

## Why

The project already discovered that its original authored 30-brief bank under-covered important
real request operations. Marketplace research now supplies concrete commercial jobs with:
- supplied scripts and assets;
- product-video deliverables;
- Meta/social placements;
- aspect ratios and durations;
- recurring-character consistency;
- avatar/spokesperson requirements;
- batch/retainer structures;
- Hindi/Hinglish demand;
- commercial CTAs and brand inputs.

This is a better source for end-to-end benchmark briefs than inventing synthetic customer jobs.

## Provenance rule

### Upwork

Use individual Upwork buyer jobs as the primary source for customer intent.

Every derived case must retain:
- source file;
- source job title / stable internal source id;
- exact facts used;
- source date;
- whether each requirement was stated or inferred.

### Fiverr

Fiverr seller gigs are NOT customer briefs.

Use them only to inform:
- common input packages;
- common delivery shapes;
- commercial format conventions;
- package durations;
- aspect ratios;
- typical buyer-supplied assets;
- pronunciation/voice/brand-input conventions.

Do not convert seller claims into customer-stated requirements.

## Architecture rule

Do not collapse:
`marketplace job -> final provider prompt`.

Required derivation chain:

`source buyer job`
→ `source-faithful customer brief`
→ `Normalized Request`
→ `benchmark acceptance requirements`
→ `route-neutral generation brief`
→ later `Production IR / provider-specific prompt`

Production IR does not exist yet. Therefore this task may prepare prompt-ready envelopes and
route-neutral generation briefs, but must not invent a provider-specific optimal workflow and call it
the benchmark truth.

## Scope

Prepare a bounded bank of:
- 12–20 derived cases;
- at least 8 fully runnable without contacting the original buyer;
- a balanced mix across:
  - product/commercial video;
  - UGC/spokesperson;
  - supplied-script production;
  - supplied-asset product work;
  - recurring character/identity;
  - app/SaaS promo;
  - batch/series;
  - Hindi/Hinglish where supported by the source.

Prefer cases with explicit deliverables and acceptance constraints.

## Per-case artifacts

Each case must include:

1. **Source record**
   - marketplace;
   - source title/id;
   - source lineage;
   - source excerpt/facts used;
   - provenance.

2. **Customer brief**
   - minimal source-faithful rewrite;
   - no benchmark additions hidden as buyer intent.

3. **Normalized Request**
   - using the current Media Request Grammar;
   - every field labelled:
     - customer_stated;
     - customer_implied;
     - experiment_supplied_fixture;
     - system_derived;
     - absent / unresolved.

4. **Fixture requirements**
   - assets the original job requires;
   - assets the benchmark must supply;
   - source/rights requirement;
   - whether the case is runnable now.

5. **Acceptance contract**
   - objective hard constraints;
   - subjective/creative dimensions;
   - set-level vs per-output acceptance;
   - unresolved human-review needs.

6. **Route-neutral generation brief**
   - what must be produced;
   - no model/vendor assumptions;
   - no hidden production route.

7. **Prompt-ready envelope**
   - a neutral text instruction suitable for later adaptation;
   - model-specific prompt fields remain separate and may be null.

8. **Capability mapping**
   - current capability-contract dimensions exercised;
   - evaluator families required;
   - known qualification blockers.

9. **Stage fit**
   - Stage A atomic/compound: usually NO unless the case decomposes cleanly;
   - Stage C / Layer 4 end-to-end: primary intended destination;
   - may also be used as future compound-scenario source material.

## Selection priorities

Prioritise source jobs such as:
- Meta ad with avatar + product B-roll;
- e-commerce catalogue/product-video batch with explicit outputs;
- recurring-character SaaS series;
- supplied-PDF lecture video;
- mobile-app promo with supplied script;
- recurring/batch supplied-script production;
- persistent avatar/personality;
- Hindi/Hinglish commercial creative.

The source research found many productised jobs with explicit deliverables, and recurring-character /
product consistency is a major divider between simple pipeline work and custom creative. Preserve
that distinction rather than normalising it away.

## Output

Create:
- `canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml`
- `canon/research/marketplace-demand-v1/derived/marketplace-prompt-ready-bank-v1.yaml`
- `canon/research/marketplace-demand-v1/derived/COVERAGE-REPORT.md`
- deterministic validator(s).

No paid calls.
No model generation.
No Registry rows.
Do not replace the existing 30-brief bank.
This is an additional evidence-backed request source and a candidate Stage-C pool.
