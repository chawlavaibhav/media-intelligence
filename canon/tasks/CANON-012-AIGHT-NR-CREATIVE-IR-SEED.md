# Task CANON-012: Aight Normalized Request + Creative IR seed

**TASK ID:** CANON-012
**OBJECTIVE:** Create the first real, auditable Normalized Request and Creative IR instance for the Aight pilot without inventing customer intent or production-routing decisions.
**WHY WE ARE DOING THIS:** The project has specifications for Normalized Request and Creative IR but no real executable/product instance. Before automating the interpreter, we need one real commercial brief to expose what the schemas can and cannot express.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`.

## CONTEXT CONTRACT
**Inherits `shared/CONTEXT-SUFFICIENCY-POLICY.md`.**

### BASE STATE
- **BASE MAIN SHA:** 719c90f0900a2c3b925a6af8a8d538755d328467
- **ACCEPTED DEPENDENCY:** `coordination/decisions/CONTROLLER-REVISED-PROGRAM-AND-PREPILOT-TRANCHE-2026-08-28.md`

### REQUIRED ORIENTATION
Default bootstrap in `coordination/RUNBOOK.md`.

### TASK-SPECIFIC CONTEXT
- `canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml`
- `canon/knowledge/SPEC-01-creative-ir.md`
- `coordination/PROJECT-CONTRACT.md` sections defining Normalized Request vs Creative IR
- relevant accepted Canon files **only if needed to understand field semantics; Canon knowledge must not be used to improve the pilot Creative IR in this task**

### EXPANSION TRIGGERS
- if the Aight brief cannot be represented without changing a frozen vocabulary;
- if a requested field would require production-route knowledge;
- if a customer statement and an experiment-supplied fixture cannot be separated cleanly.

### EVIDENCE HANDLING LEVEL
`state_only`

### CONTEXT INSUFFICIENCY
Stop with `STOP — CONTEXT_INSUFFICIENT` rather than inventing a missing customer fact.

**INPUT BRIEF — Controller-supplied product-learning brief:**
Create a short premium festive promotional video for **aight / getaight.ai**, positioning the product as an outcome API. The commercial claims that must remain exact are **“Image ₹9”** and **“Video ₹99”**. The work should feel modern and premium for the Indian festive context rather than gaudy. Where the aight logo/wordmark appears, it must remain exact. A 12-second duration and 9:16 delivery may be used as **experiment-supplied fixtures**, not customer-stated facts, unless a newer Controller-supplied brief says otherwise.

**IN SCOPE:**
- create one Normalized Request instance;
- create one Creative IR instance;
- explicitly label every fact as customer-stated, customer-implied, system-derived, experiment-supplied fixture, absent, or ambiguous as the governing grammar requires;
- write an acceptance contract separating hard intent from subjective creative criteria;
- identify schema friction/gaps observed while instantiating the brief;
- list required external assets by role, without fabricating them.

**OUT OF SCOPE:**
- Canon retrieval or Canon-enhanced planning;
- model/provider selection;
- Production IR or production recipe;
- generation;
- changing the request grammar or Creative IR spec;
- inventing brand assets.

**DELIVERABLES:**
- `canon/experiments/pilot-001/aight-normalized-request.yaml`
- `canon/experiments/pilot-001/aight-creative-ir.yaml`
- `canon/experiments/pilot-001/CANON-012-CONTROLLER-BRIEF.md`

**AUTONOMY MODE:** autonomous

**RESOURCE BUDGET:**
- API spend: USD 0
- generations/retries: 0
- external research: 0 unless a context-insufficiency trigger requires a Controller decision

**STOP CONDITIONS:**
- any need to mutate a frozen cross-stream contract;
- exact current brand asset cannot be found — record it as required input, do not invent it;
- the brief requires a production decision to fill a Creative IR field.

**HUMAN APPROVAL TRIGGERS:** any proposed schema/architecture change.

**RESULT LOCATION:** `canon/experiments/pilot-001/CANON-012-CONTROLLER-BRIEF.md`
