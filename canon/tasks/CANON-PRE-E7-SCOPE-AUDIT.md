# CANON — Pre-E7 Customer-to-Requirement Scope Audit

**Owner:** Canon  
**Controller decision:** `coordination/decisions/CONTROLLER-PRE-E7-SCOPE-REBASE-2026-08-26.md`  
**Design:** `docs/superpowers/specs/2026-08-26-pre-e7-scope-rebase-design.md`

## Goal

Audit all 30 accepted customer briefs from the customer's wording outward and prove that every meaningful requirement can be represented by the re-scoped architecture without inventing production methods or model capabilities.

## Read first

- `canon/experiments/v1/brief-bank/briefs-source.yaml`
- `canon/knowledge/SPEC-01-creative-ir.md`
- `eval/v1/capability-contract.yaml`
- Pre-E7 design above

## Deliverables

Create under `canon/experiments/pre-e7-scope-audit/`:

1. `requirement-ledger.jsonl` — one row per meaningful requirement found in the 30 briefs.
2. `AUDIT-REPORT.md` — findings and proposed cross-stream changes.
3. `validate_requirement_ledger.py` — fail-closed validator.

Each requirement row must include:

- `brief_id`
- `requirement_id`
- exact supporting customer text or authoritative-intent field
- `classification`: `existing_capability | condition | planner_decision | acceptance_constraint | operational_variable | genuine_gap`
- `mapped_id_or_proposed_name`
- `source_operation`: `preserve | derive | decide | delegate | ask | flag`
- `strength`: `hard | soft | free`
- `scope`: entity / asset / shot / sequence / outcome / campaign-set as applicable
- plain-English reason

## Rules

- Do not change the customer briefs.
- Do not author Production IR or choose a provider/model/workflow.
- Do not manufacture requirements from general knowledge; every row must be grounded in the brief or an unavoidable acceptance expectation explicitly justified as implicit.
- For implicit acceptance requirements, mark `source_operation: derive` and explain why rejection is reasonably expected even though the customer did not state it.
- Do not propose a new capability if an existing capability plus an explicit condition represents the requirement honestly.
- Candidate gaps from the Controller design are questions, not instructions to add dimensions.

## Mechanical gates

Validator must fail if:

- any of 30 brief ids is absent;
- a row has no grounding/evidence;
- `genuine_gap` has no explanation of why existing capability + condition is insufficient;
- a requirement is simultaneously classified into multiple buckets;
- a Planner decision is presented as customer-specified;
- an Eval model/provider/workflow name appears as the answer to a requirement.

## Controller brief

Conclude with:

- total requirements classified;
- counts per classification bucket;
- exact list of genuine gaps, if any;
- condition concepts repeatedly appearing in customer briefs;
- production decisions customers commonly omit;
- whether the 30-brief bank exposes any important creation family not representable by the proposed interfaces.

No merge. Commit and push the isolated branch for Controller review.
