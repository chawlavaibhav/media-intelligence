# Task <STREAM>-<NNN>: <short title>

**TASK ID:** <STREAM>-<NNN>
**OBJECTIVE:** one sentence — the finish line, not "continue researching X"
**WHY WE ARE DOING THIS:** explain the project question this task answers and why the answer matters

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`; explain technical ideas in plain English, including what they mean, why they matter and their practical consequence; use minimum sufficient wording without sacrificing understandability; do not invent; separate evidence from inference.

## CONTEXT CONTRACT

**Inherits `shared/CONTEXT-SUFFICIENCY-POLICY.md`.** The worker owns context *sufficiency*, not just
this checklist; expand context whenever the policy requires it, and stop with
`STOP — CONTEXT_INSUFFICIENT` rather than guess.

### BASE STATE
- **BASE MAIN SHA:** <exact `main` commit this task was authored against>
- **ACCEPTED DEPENDENCY SHA(s):** <optional — commits/fingerprints of accepted artifacts this task builds on>

### REQUIRED ORIENTATION
Normally just: *the default bootstrap in `coordination/RUNBOOK.md`.* Add extra orientation files
only when this task genuinely needs them; do not repeat the standard list.

### TASK-SPECIFIC CONTEXT
Exact files this task must read. Prefer exact sections, capability ids or document headings over
whole large files when practical (e.g. name the three capability ids rather than the whole
capability contract) — but do not create fragile line-number dependencies.

### BROAD READS
Broad globs (e.g. `eval/v1/harness/**`) or complete large frozen contracts are allowed when
genuinely required. Each one needs a one-line reason:
`BROAD READ JUSTIFICATION: ...`

### EXPANSION TRIGGERS
Task-specific additions to the global triggers in `shared/CONTEXT-SUFFICIENCY-POLICY.md`
(the global triggers always apply and cannot be removed here).

### EVIDENCE HANDLING LEVEL
One of (defined in `shared/CONTEXT-SUFFICIENCY-POLICY.md`):
`state_only` | `validator_summary` | `aggregated_evidence` | `row_level_evidence` | `full_raw_evidence`
Compute first, load second: prefer the deterministic validators in `verify/VALIDATOR-INDEX.yaml`
over loading raw evidence, unless a trigger demands the rows.

### CONTEXT INSUFFICIENCY
If a required dependency, authority or input cannot be determined without guessing:
**stop and route** (`STOP — CONTEXT_INSUFFICIENT`), reporting what is missing, why it matters, what
authority/file is needed, and whether completed work remains valid. Never guess to save tokens.

**INPUTS:** exact files/sources this task reads (summarised from the Context Contract above)
**IN SCOPE:**
**OUT OF SCOPE:**
**DELIVERABLES:** exact file(s)/location this task must produce

**AUTONOMY MODE:** interactive | autonomous | autonomous_queue

**RESOURCE BUDGET:**
- sources/items:
- storage:
- API spend:
- generations/retries:
- other:

**APPROVED DEPENDENCIES:** tasks/decisions this one relies on already being approved
**STOP CONDITIONS:** see AUTONOMY-POLICY.md — list the specific ones relevant here
**HUMAN APPROVAL TRIGGERS:** state the decision the human would need to make and why it matters
**RESULT LOCATION:** exact path the Controller Brief and artifacts will be found at
