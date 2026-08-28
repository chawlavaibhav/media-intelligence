# Task EVAL-035: Pilot video-route substrate

**TASK ID:** EVAL-035
**OBJECTIVE:** Implement one pilot-capable real video-provider route that can return and persist actual binary media bytes, while making zero paid/provider calls.
**WHY WE ARE DOING THIS:** The repository has live-generation machinery for the prior image experiment but no general video production route. PILOT-001 cannot exist until one video route can be dispatched safely and its returned media handled as bytes.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`.

## CONTEXT CONTRACT
**Inherits `shared/CONTEXT-SUFFICIENCY-POLICY.md`.**

### BASE STATE
- **BASE MAIN SHA:** 719c90f0900a2c3b925a6af8a8d538755d328467
- **ACCEPTED DEPENDENCIES:** EMP-001 dispatch/budget semantics; scientific Wave-1 roster; current pilot-priority Controller decision.

### REQUIRED ORIENTATION
Default bootstrap in `coordination/RUNBOOK.md`.

### TASK-SPECIFIC CONTEXT
- `eval/empirical-tranche-1/providers.py`
- `eval/empirical-tranche-1/budget_guard.py`
- `eval/empirical-tranche-1/atex/run_atex.py`
- `eval/v1/harness/harness.py`
- relevant Wave-1 video slot(s)
- latest committed route/price verification only as a planning reference; route identity/availability must be reverified before any later live execution

### BROAD READS
- `eval/v1/harness/**` — justified because the task must preserve trial/retry/provenance semantics while adding binary media support.

### EVIDENCE HANDLING LEVEL
`validator_summary`

**IN SCOPE:**
- select **one** serious video route compatible with the pilot's basic short-form video shape;
- implement provider-specific request/response handling behind an injected transport;
- support polling/download if the provider contract requires it;
- store returned media as binary bytes with SHA-256 and byte length;
- preserve one-call=one-trial, no silent retry, ambiguous-post-dispatch accounting, exact route/model/version recording and budget-gated live dispatch;
- add deterministic fake-transport tests for success, refusal, timeout/ambiguous dispatch and binary artifact persistence;
- expose a thin interface that PILOT-001 can call.

**OUT OF SCOPE:**
- any real provider call;
- evaluating output quality;
- multiple video providers;
- TTS/lipsync unless the selected route intrinsically includes audio and the contract requires handling it;
- Planner/routing logic;
- Registry writes;
- changing Stage-A thresholds.

**DELIVERABLES:**
- implementation under `eval/` in the narrowest appropriate runtime package;
- tests proving zero network access by default and correct binary handling;
- `eval/tasks/EVAL-035-CONTROLLER-BRIEF.md`

**AUTONOMY MODE:** autonomous

**RESOURCE BUDGET:**
- API spend: USD 0
- real generations: 0
- retries: 0
- providers implemented: exactly 1

**STOP CONDITIONS:**
- no current route can be verified to support the pilot shape without inventing provider behaviour;
- provider requires pre-funding or a paid call to discover the contract;
- implementation would require changing Resources-owned persistence contracts.

**HUMAN APPROVAL TRIGGERS:** any paid preflight/live call; any change to trial/cost semantics; adding a second provider.

**RESULT LOCATION:** `eval/tasks/EVAL-035-CONTROLLER-BRIEF.md`
