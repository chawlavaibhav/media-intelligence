# Task CANON-013: Marketplace architecture-experiment feasibility triage

**TASK ID:** CANON-013
**OBJECTIVE:** Determine which of the 16 runnable marketplace-derived buyer cases are operationally suitable for the architecture experiment, and propose a balanced 8-development / 8-holdout split without generating media.
**WHY WE ARE DOING THIS:** “Runnable” currently means missing inputs can be constructed without contacting the buyer. It does not mean the case is cheap, short, fixture-ready or suitable for a controlled architecture comparison.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`.

## CONTEXT CONTRACT
**Inherits `shared/CONTEXT-SUFFICIENCY-POLICY.md`.**

### BASE STATE
- **BASE MAIN SHA:** 719c90f0900a2c3b925a6af8a8d538755d328467
- **ACCEPTED DEPENDENCY:** CANON-011 marketplace brief bank

### REQUIRED ORIENTATION
Default bootstrap in `coordination/RUNBOOK.md`.

### TASK-SPECIFIC CONTEXT
- `canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml`
- CANON-011 Controller integration decision
- frozen scientific model roster only for capability/route vocabulary; do not infer model capability from it

### EVIDENCE HANDLING LEVEL
`aggregated_evidence`

**IN SCOPE:**
For each of the 16 `runnable_now: true` cases, record:
- deliverable count and duration/load;
- modality and speech/audio need;
- person/product/reference-identity need;
- fixture assets required and whether currently present vs constructible;
- whether the case can be reduced to one representative deliverable without changing the buyer's core job;
- major production-route prerequisites;
- major acceptance requirements;
- estimated experimental burden class: low / medium / high, with a concrete reason.

Then propose:
- **8 development briefs** spanning materially different commercial shapes while remaining feasible;
- **8 holdout briefs** of comparable breadth, not selected merely because they are hard.

**OUT OF SCOPE:**
- generation;
- route/model selection;
- changing buyer facts;
- creating fixtures;
- scoring model quality;
- revealing the proposed holdout set to later implementation workers except through Controller-approved context.

**DELIVERABLES:**
- `canon/experiments/architecture-outcome-v1/marketplace-feasibility-triage.yaml`
- `canon/experiments/architecture-outcome-v1/proposed-brief-split.yaml`
- `canon/experiments/architecture-outcome-v1/CANON-013-CONTROLLER-BRIEF.md`

**AUTONOMY MODE:** autonomous

**RESOURCE BUDGET:**
- API spend: USD 0
- generations/retries: 0
- sources: existing committed marketplace bank only

**STOP CONDITIONS:**
- fewer than 16 cases can be triaged from committed evidence without inventing missing facts;
- an 8/8 split would require changing buyer intent rather than supplying fixtures.

**HUMAN APPROVAL TRIGGERS:** Controller freezes the final split; worker only proposes it.

**RESULT LOCATION:** `canon/experiments/architecture-outcome-v1/CANON-013-CONTROLLER-BRIEF.md`
