# Eval / Capability Lab — Handoff

**PURPOSE:** Design measurement, calibrate evaluators, empirically test current model/workflow
capability, produce the Capability Registry.

**CURRENT STATE:** One completed calibration study exists
(`findings/FINDINGS-01-can-we-check.md`): a Devanagari-text VLM checker study. qwen3-vl-235b scored
14/14 correct verdicts; claude-sonnet-4.5 produced 6 false passes on the same 14 samples. Tesseract
(Hindi) failed completely. No Eval Battery exists. No Capability Registry exists. No provider
benchmarking beyond that calibration has run.

**CURRENT APPROVED DECISIONS:** Technical hard-fidelity and creative-fitness evaluation are
separate instruments. An evaluator must be calibrated against human judgement on the specific
task before being trusted. Capability claims must name the measuring instrument and conditions.

**LAST COMPLETED TASK:** the Devanagari checker calibration (pre-dates this operating structure).

**CURRENT TASK / QUEUE:** `tasks/EVAL-001.md` — turn the current Capability Lab research plan into
a bounded V0 battery specification and instrument-calibration plan. No paid generations or model
benchmarking in this task.

**IMPORTANT OBSERVATIONS:**
- A capability number without its instrument and calibration reference is not trustworthy.
- Cross-frame/shot failures require an explicit `observation_unit` concept.
- Published benchmarks are methodology inputs, not our capability scores.
- Do not add metrics after seeing model outputs; there are no model outputs in EVAL-001.

**OPEN QUESTIONS:** which published benchmark taxonomies should be adopted/adapted; which
instruments can be calibrated cheaply enough for V0; how Registry freshness should later decay.

**DEPENDENCIES:** EVAL-001 may identify media requirements for Resources. Actual Capability Lab
runs wait on Controller approval of the battery and on suitable corpus inputs.

**PROPOSED CROSS-STREAM CHANGES:** none filed yet.

**NEXT APPROVED TASK:** `EVAL-001` only. After the battery draft and Controller Brief, stop; do not
start benchmarking or spend on generation without a new approved task.
