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

**AUTONOMY MODE:** interactive

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

## Controller clarification — 24 Aug 2026

These clarifications resolve Phase-0 ambiguities and are part of the approved task.

1. **Governance / autonomy.** Battery design is not worker-autonomous under the Charter and Autonomy Policy. `AUTONOMY MODE` is therefore `interactive`. The worker may research and draft the specified artifacts after Controller approval, but all outputs remain proposals until Controller review. Do not silently promote draft decisions into shared truth.

2. **V0 scope.** EVAL-001 should deliberately focus the first Capability Battery on hard-fidelity and operational capabilities. Creative-judgement evaluation is not part of EVAL-001; it will be designed separately once the relevant Canon/evaluation work is ready. Still document which future creative dimensions are intentionally deferred so absence is not mistaken for irrelevance.

3. **No invented two-source admission rule.** A dimension does not need two independent justifications to enter the draft. It may be included when traceable to any approved evidence class: published benchmark methodology, a current Creative IR requirement, or an observed production failure. Record the provenance and strength of the justification. Do not create a new admission policy without Controller approval.

4. **Devanagari calibration.** Do not perform new human calibration in EVAL-001. Treat the existing Devanagari checker result as preliminary because native-speaker confirmation is unresolved and the sample contains correlated frames. The calibration plan must specify what native-speaker/human validation is required before the instrument is trusted for Registry scoring, including an estimated human-time requirement. Do not quote historical 14/14 or Tesseract 0/14 claims as settled ground truth where supporting evidence is incomplete.

5. **Costed plan without an approved model list.** Build a parameterised cost model first. You may use workflows already named in `CAPABILITY-LAB-V0-PLAN.md` only as clearly labelled budgeting examples, not as an approved benchmark roster. Treat Wan and Veo as separate workflows/models; never collapse them into one Registry entry. Exact future model/vendor selection remains a Controller decision.

6. **Existing production failures.** Do not copy the external `media-factory` 64-image set into this repository during EVAL-001 and do not re-score it. Reference available findings/metadata as historical evidence and record the inaccessible underlying media as a dependency for a later Resources/integration task. Re-annotation/re-scoring is separate work.

7. **Registry draft fields.** The draft may propose fields needed to represent evidence correctly, including multiple defects per output/trial, evaluator/checking cost, repair/retry cost where measurable, and an explicit state for `required_but_no_calibrated_instrument`. Mark such additions as proposed. If a proposed field changes cross-stream architecture or routing semantics, raise it as a cross-stream proposal rather than treating it as accepted.

8. **Field references.** Use exact SPEC-01 paths where they are actually defined. Where the current plan uses shorthand or points at the wrong field, cite the relevant SPEC-01 section/path and flag the mismatch. Do not invent a temporary naming convention.

9. **Cost per success.** `usd_per_pass` / cost per successful outcome is an important Registry metric, but is not approved as the sole or universal primary sort key. Preserve component costs so later routing can trade off quality, reliability, latency and repairability rather than collapsing them prematurely.

10. **Freshness.** Do not invent a mathematical decay function in V0. Represent freshness explicitly using tested date, exact model/version, and a discrete status such as current/ageing/stale plus retest triggers. A decay formula can be proposed later from observed model drift.

11. **Source record.** Maintain a complete research source list for benchmark methodologies reviewed, with title, official URL, version/date accessed, and what specific method/taxonomy was borrowed or rejected.

12. **Experiment integrity.** Do not modify existing historical findings, scripts or result files to make them fit the new design. Record broken paths, unsupported claims, correlated samples and other provenance issues in EVAL-001 findings. If a historical claim lacks sufficient evidence, downgrade it in the new draft rather than silently repairing history.
