# Task EVAL-001: Capability Lab V0 battery design

**TASK ID:** EVAL-001
**OBJECTIVE:** Turn the existing Capability Lab research plan into a bounded, evidence-grounded V0 battery specification that is runnable later, without spending on model generations now.
**WHY WE ARE DOING THIS:** The Registry cannot exist until the battery defines what is measured, at what observation unit, with which instruments, and how each instrument is calibrated.

**INPUTS:**
- `coordination/PROJECT-CONTRACT.md`
- `eval/CHARTER.md`
- `eval/HANDOFF.md`
- `eval/battery/CAPABILITY-LAB-V0-PLAN.md`
- relevant Creative IR requirements from `canon/knowledge/SPEC-01-creative-ir.md`
- `eval/findings/FINDINGS-01-can-we-check.md`
- relevant real-failure findings already in repo, including observation-unit lessons
- public benchmark methodologies that can be researched without paid access (e.g. GenEval, T2I-CompBench, VBench and closely relevant peers)

**IN SCOPE:**
- review published benchmark taxonomies/methods and map what is reusable
- define V0 capability dimensions, difficulty levels, observation units, trial units, pass criteria and required instruments
- distinguish deterministic/hard-fidelity measures from model/human creative measures
- specify evaluator calibration requirements per dimension
- define registry fields needed to preserve instrument, conditions, freshness, cost and failure types
- produce a costed run plan, but do not run it
- identify which corpus/media inputs must come from Resources

**OUT OF SCOPE:**
- no paid generations
- no provider benchmarking
- no Capability Registry scores
- no new creative-quality principles
- no dataset acquisition/licensing
- no Canon-consumption experiment
- no post-hoc metric creation based on model outputs

**DELIVERABLES:**
- `eval/battery/CAPABILITY-BATTERY-V0-DRAFT.md`
- `eval/battery/CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml`
- `eval/battery/INSTRUMENT-CALIBRATION-PLAN-V0.md`
- `eval/findings/EVAL-001-battery-design-findings.md`
- `eval/tasks/EVAL-001-CONTROLLER-BRIEF.md`

**AUTONOMY MODE:** autonomous

**RESOURCE BUDGET:**
- sources/items: published benchmark docs/papers + repo evidence only
- storage: <250 MB
- API spend: ₹0 / $0 paid APIs
- generations/retries: zero model generations
- other: web/public research allowed; record exact source/version/date

**APPROVED DEPENDENCIES:** current Creative IR and Capability Lab research plan are inputs, not unquestionable truth.
**STOP CONDITIONS:** need for a new cross-stream architecture field; inability to calibrate a proposed instrument; legal/access gate; scope expansion into actual benchmarking; evidence that an existing central assumption is materially contradicted.
**HUMAN APPROVAL TRIGGERS:** any new battery dimension beyond what can be traced to published methodology, Creative IR requirements, or observed production failures; any paid test; any model/vendor list.
**RESULT LOCATION:** `eval/tasks/EVAL-001-CONTROLLER-BRIEF.md` plus the deliverables above.
