# CANON-010 — Request Contract & Coverage Freeze

**AUTONOMY:** autonomous  
**ENVIRONMENT:** Claude Web/cloud; GitHub + public web as needed  
**BUDGET:** ₹0 external spend  
**BRANCH:** `work/canon-010-request-freeze`

## Objective

Convert CANON-009 request-space research plus the Controller integration decision into a **request-side package ready for Controller freeze**.

This task owns customer-request representation and controlled request coverage. It does not own model selection, provider routing, Eval thresholds or Production IR.

## Read first

1. `PROJECT-MEMORY.md`
2. `coordination/CONTROL-STATE.md`
3. `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md`
4. `coordination/decisions/CONTROLLER-FINAL-PRE-EXECUTION-FREEZE-2026-08-26.md`
5. `coordination/plans/2026-08-26-FINAL-PRE-EXECUTION-FREEZE-PROGRAM.md`
6. CANON-009 research under `canon/research/request-space-v1/`
7. current Creative IR spec and 30-brief bank

## Work packages

### C10-A — Media Request Grammar v1

Produce a versioned, machine-readable proposal for recurring request structure.

At minimum represent:
- requested operation: generate / edit / animate / restore / extend / compose / variants, with room for future controlled extension;
- supplied asset roles;
- mutation intent: preserve / change / remove / add / transform;
- modality and deliverable-set/cardinality semantics;
- subject/entity/reference requirements;
- text/brand/language/script/speaker requirements;
- temporal/shot structure;
- camera motion separately from subject motion;
- customer-specified versus omitted/derived fields;
- ambiguity/contradiction markers;
- acceptance intent that is visible from the request without inventing Eval thresholds.

Requested operation is customer intent and must never become workflow mode.

### C10-B — Normalized Request additions

Specify the smallest exact additions needed upstream of Creative IR.

For every proposed field provide:
- field id/type;
- preserve/derive/ask/flag semantics;
- source/provenance;
- examples;
- what must **not** be inferred;
- relationship to existing Creative IR fields.

Do not implement Production IR or provider decisions.

### C10-C — Multi-turn boundary

Define the minimum representation boundary that prevents architecture lock-in while keeping multi-turn out of first paid execution.

Do not design a full conversation/session system.

State exactly what is deferred and what current structures must not preclude.

### C10-D — Request-coverage extension bank

Keep the original 30 briefs byte-identical.

Author a separate extension bank that covers at minimum:
- edit a supplied asset;
- animate a supplied image;
- variants/campaign-set deliverables.

Add only as many items as coverage requires. Do not force a symmetric count or arbitrary target.

Use English/Hindi/Hinglish where language materially changes requirements. Do not duplicate prompts merely to balance languages.

A multi-turn representation probe may be included but must be marked `representation_only` / not runnable in Wave 1.

Each extension item must include:
- request text;
- requested operation;
- supplied inputs;
- exact hard/soft/free constraints;
- required preservation/change semantics;
- output cardinality/set semantics;
- acceptance-relevant requirements;
- grammar features covered;
- whether runnable in Wave 1.

### C10-E — Combined coverage audit

Measure the original 30 + extension bank against Media Request Grammar v1.

Report:
- request operations covered/not covered;
- important feature/co-occurrence patterns covered/not covered;
- customer-specified vs omitted production decisions;
- first-product gaps intentionally deferred;
- any existing Creative IR field that cannot represent a required creative outcome.

Do not report corpus frequency as market share.

## Deliverables

Under `canon/experiments/pre-execution-freeze/` create at minimum:
- `MEDIA-REQUEST-GRAMMAR-v1.yaml`
- `NORMALIZED-REQUEST-DELTA.md`
- `REQUEST-COVERAGE-EXTENSION.jsonl`
- `REQUEST-COVERAGE-EXTENSION.md`
- `COMBINED-COVERAGE-REPORT.md`
- `validate_request_freeze.py`
- `CANON-010-CONTROLLER-BRIEF.md`

## Mechanical gates

Validator must fail if:
- original 30-bank bytes changed;
- an extension item lacks requested operation or input/output cardinality semantics;
- workflow/provider/model appears as the resolution of customer requested operation;
- customer-specified provenance is assigned to something the customer did not say;
- a runnable Wave-1 multi-turn item is created without a frozen history contract;
- language variants are exact duplicates with no language-dependent requirement;
- a grammar field has no provenance/operation rule.

## Stop conditions

Stop and report rather than decide if:
- fulfilling request representation requires changing the fundamental Creative IR separation;
- a field is inherently a Production IR/provider decision;
- external evidence is needed to claim market prevalence rather than structural coverage.

## Restrictions

No source ingestion. No paid calls. No model/provider selection. No Eval thresholds. No Production IR. No merge.

Commit and push the branch. Return the Controller brief and commit SHA only after the whole program is complete.
