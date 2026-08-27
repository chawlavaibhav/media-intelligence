# Controller — Marketplace-Derived Brief and Prompt Preparation — 2026-08-27

## Status

**AUTHORISED IN PARALLEL AT ZERO API SPEND.**

Use the user's 26 Aug 2026 Upwork and Fiverr research as market-demand evidence to prepare a
marketplace-derived benchmark brief bank and frozen prompt packages.

This work may run in parallel with EVAL-023 and EVAL-024.

## Purpose

The project needs realistic prompts for later model tests, but the prompt must not become the source
of truth.

Use three separate layers:

1. **source brief evidence** — what the marketplace buyer/post actually asked for;
2. **Normalized Request** — the request represented under Media Request Grammar v1, preserving
   stated / implied / absent / experiment-supplied provenance;
3. **benchmark prompt package** — a frozen executable brief derived from the Normalized Request for
   testing models/workflows.

The marketplace post is demand evidence, not capability evidence.
A generated prompt/result does not retroactively change what the buyer asked for.

## Source roles

### Upwork

Use as the primary source of buyer-shaped briefs because the research captured actual job requests.

The source report contains 114 unique postings, 67 classified addressable, including tightly
specified single ads, product catalogue work, batch scripted work, recurring-character series and
high-volume production contracts.

### Fiverr

Use mainly as evidence about:
- common deliverable shapes;
- buyer intake fields;
- package durations;
- aspect/delivery expectations;
- market language/format categories.

Fiverr gig listings are seller offers, not buyer requests. They must not be represented as though
a customer directly asked for every package field.

## Seed marketplace cases

Prepare at least these eight source-derived candidates, preserving the source-post facts and marking
unknowns as unknown:

1. **UP-008 — Meta ad: talking head + product B-roll**
   - 40-second Meta ad;
   - men's dog-care supplement;
   - AI avatar + AI product B-roll;
   - one deliverable.

2. **UP-074 — E-commerce product catalogue / Knox Deco**
   - 15–30 seconds per video;
   - 1080×1080 master;
   - up to two revisions;
   - no watermark;
   - optional 9:16 and 16:9 exports;
   - paid test, then substantial product catalogue.

3. **UP-021 — recurring-character SaaS series**
   - 10-video series;
   - recurring named characters Thomas and Anna;
   - visual and vocal consistency;
   - integrate live SaaS dashboard footage;
   - subtle comedy;
   - avoid generic AI-avatar look;
   - reusable character style guide requested.

4. **UP-063 — lecture videos from supplied documents**
   - source material supplied as PDF;
   - 6 courses × 8 weeks;
   - batch/series delivery;
   - narration/assessment context.

5. **UP-mobile-promo — 35-second mobile-app promo**
   - 35-second promo;
   - script and full instructions supplied in the job;
   - treat unavailable detail text as missing until sourced, do not invent it.

6. **UP-036 — short cinematic product ad**
   - 10–20 seconds;
   - product-commercial format;
   - cinematic intent.

7. **UP-069 — persistent AI influencer / football performance lab**
   - ultra-realistic avatar/influencer;
   - persistent brand personality;
   - consistency is a first-class requirement.

8. **UP-031 — scripted batch assembly**
   - 10 videos;
   - scripts supplied;
   - approximately 3 minutes each according to the research summary;
   - assembly/polish workflow rather than free-form ideation.

Reserve additional candidates from:
- AI UGC sock-brand ad;
- two-videos-per-week AI UGC work;
- B2B/SaaS product ads;
- mobile-app marketing;
- short-form product ads;
- long-form recurring-character story video;
- product/dealership batch work.

Do not use client budget or proposal count as a creative requirement. Keep those only as demand
priority metadata.

## Representation rules

For every brief candidate record:

### Source facts

Persist:
- source platform;
- research date;
- source row/job id where available;
- title;
- only the deliverable facts actually captured;
- source confidence/detail level;
- recurring/batch signal;
- market priority metadata.

Do not reproduce unnecessary client-identifying metadata in the benchmark.

### Normalized Request

Map against current Media Request Grammar v1:
- requested_operation;
- supplied_assets and roles;
- mutation intent if applicable;
- deliverable_set;
- modality;
- entities + identity invariants;
- relationships;
- text requirements;
- brand requirements;
- language topology;
- speaker topology;
- temporal structure;
- subject motion;
- camera motion;
- delivery;
- ambiguity/underspecification markers.

Every field needs provenance:
- `customer_stated`;
- `customer_implied`;
- `system_derived`;
- `absent`;
- or a new benchmark-only provenance `experiment_supplied_fixture` that MUST NOT be mistaken for
  customer intent.

Do not fill absent marketplace details from Fiverr norms and label them customer-stated.

### Benchmark prompt package

Produce:
1. `canonical_generation_brief` — provider-neutral;
2. `asset_manifest` — exact fixture inputs required;
3. `acceptance_requirements` — only requirements traceable to the source/fixture;
4. `prompt_template` — model-neutral semantic prompt;
5. `provider_adapter_fields` — API syntax only, not provider-specific creative optimisation;
6. `evaluation_capabilities_required` — links to Capability Contract v2;
7. `unscorable_without_instrument` — explicit list.

## Prompt fairness rule

The prompt bank must be frozen before any comparative model run.

Do not hand-tune a prompt for one model after seeing its output while leaving another model on the
original prompt.

Allowed differences between provider prompt packages:
- API-required syntax;
- supported input modality packaging;
- documented parameter translation.

Disallowed:
- adding/removing creative constraints for a specific model;
- model-specific rescue wording discovered after a failure;
- changing assets or acceptance criteria.

A future separate experiment may compare prompt strategies, but it must not be mixed into model
capability comparison.

## How this relates to benchmark stages

- **A-TEXT:** unchanged; marketplace briefs do not replace its four frozen text items.
- **Stage A 90-generation admission:** do not rewrite the frozen comparability core now.
- **Stage B compound testing:** marketplace-derived cases may later replace/supplement synthetic
  compound scenarios through an explicit integration decision.
- **Stage C / Layer 4:** this is the strongest immediate destination. Layer 4 requires customer
  briefs, and these are real marketplace-request-derived candidates.

Prepare the bank now so later model execution is not blocked on prompt authoring.

## Fiverr-derived benchmark fixture template

Use Fiverr patterns only as optional experiment-fixture scaffolding:
- product images/clips;
- script or idea;
- logo;
- brand colours/guidelines;
- product link/description;
- target audience;
- offer/CTA;
- reference examples;
- voice/presenter preference;
- pronunciation guidance where language requires it.

If a marketplace source did not state one of these, it must be:
- absent; or
- explicitly `experiment_supplied_fixture`.

Never silently upgrade a common seller intake field into a customer requirement.

## Deliverables

Create a zero-spend package under a new marketplace-demand experiment directory containing:
- source-evidence register;
- normalized-request bank;
- prompt-package bank;
- capability-coverage report;
- ambiguity/missing-input report;
- candidate Stage-C shortlist;
- validator proving provenance separation and prompt freeze.

Target:
- 12–20 high-quality marketplace-derived candidates;
- at least 8 runnable once experiment fixtures are attached;
- broad coverage of product ad, UGC/spokesperson, recurring character, SaaS/product demo,
  document-to-video, catalogue/batch, mobile-app promo and cinematic product work.

No model/evaluator/API calls.
No Stage A spend.
No Registry rows.
