# Task RES-007: Pilot outcome writer

**TASK ID:** RES-007
**OBJECTIVE:** Implement the minimal writer that can persist a real PILOT-001 job/outcome using the accepted v3 topology and CpAO contracts, with binary artifact lineage and immutable cost references.
**WHY WE ARE DOING THIS:** The v3 outcome/CpAO schemas and validators exist, but nothing writes a real production journey into them. The first pilot must be recorded rather than reconstructed from chat or logs afterwards.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`.

## CONTEXT CONTRACT
**Inherits `shared/CONTEXT-SUFFICIENCY-POLICY.md`.**

### BASE STATE
- **BASE MAIN SHA:** 719c90f0900a2c3b925a6af8a8d538755d328467
- **ACCEPTED DEPENDENCIES:** Resources topology v3, CpAO v3, historical v2.1 compatibility rules.

### REQUIRED ORIENTATION
Default bootstrap in `coordination/RUNBOOK.md`.

### TASK-SPECIFIC CONTEXT
- `resources/pre-execution-freeze/OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml`
- `resources/pre-execution-freeze/CPAO-CONTRACT-v3.md`
- `resources/pre-execution-freeze/validators/validate_topology_v3.py`
- `resources/pre-execution-freeze/validators/recompute_cpao_v3.py`
- v2.1 manifest schema only where inherited fields are required

### EVIDENCE HANDLING LEVEL
`validator_summary`

**IN SCOPE:**
- implement a small writer/API for job → outcome → set → production unit → production step → attempt/artifact → acceptance;
- support provider-call, local deterministic and human steps without manufacturing attempts for non-provider work;
- support actual binary artifact metadata: path/location, SHA-256, byte count, media kind, ordered parent lineage;
- support immutable cost references and failed/refused/timeout attempts;
- create synthetic tests for a short multi-step video outcome including one provider artifact, one local assembly/overlay step and one human review;
- prove produced records pass the existing topology validator and recompute CpAO correctly.

**OUT OF SCOPE:**
- changing topology/CpAO contracts;
- deciding HED-1;
- generating media;
- provider integration;
- evaluator measurements beyond storing already-supplied measurement references;
- customer API.

**DELIVERABLES:**
- writer implementation and tests under `resources/`;
- synthetic example output produced by tests;
- `resources/tasks/RES-007-CONTROLLER-BRIEF.md`

**AUTONOMY MODE:** autonomous

**RESOURCE BUDGET:**
- API spend: USD 0
- generations/retries: 0
- storage: synthetic test bytes only

**STOP CONDITIONS:**
- accepted v3 schema cannot represent the pilot journey without a contract change;
- CpAO recomputation disagrees with an independently known synthetic total;
- work would require Eval-owned measurement semantic changes.

**HUMAN APPROVAL TRIGGERS:** any proposed topology/CpAO change; any HED-1 decision.

**RESULT LOCATION:** `resources/tasks/RES-007-CONTROLLER-BRIEF.md`
