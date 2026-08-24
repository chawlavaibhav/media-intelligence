# Eval / Capability Lab — Handoff

**PURPOSE:** Design measurement, calibrate evaluators, empirically test current model/workflow
capability, produce the Capability Registry.

**CURRENT STATE:** One completed calibration study exists
(`findings/FINDINGS-01-can-we-check.md`): a Devanagari-text VLM checker study. qwen3-vl-235b scored
14/14 correct verdicts; claude-sonnet-4.5 produced 6 false passes on the same 14 samples, reporting
"exact match" on visibly misspelled text. Tesseract (Hindi) failed completely (0/14, matching
published research on Devanagari OCR). No Eval Battery exists. No Capability Registry exists. No
model benchmarking beyond this one calibration test has run.

**CURRENT APPROVED DECISIONS:** Technical (hard-fidelity) and creative (fitness) evaluation are
separate instruments and must not be collapsed onto one evaluator. An evaluator must be calibrated
against human judgement **on the specific task** before being trusted — a confident wrong checker
is worse than none.

**LAST COMPLETED TASK:** the Devanagari checker calibration (pre-dates this operating structure).

**CURRENT TASK / QUEUE:** none — a Capability Lab V0 plan exists
(`battery/CAPABILITY-LAB-V0-PLAN.md`) but is a research plan, not an approved task. Battery design
has not started.

**IMPORTANT OBSERVATIONS:**
- A capability number is meaningless without naming its measuring instrument — the Registry schema
  in the V0 plan carries `instrument` and `instrument_calibration_ref` for this reason.
- Cross-shot/cross-frame failures exist that a frame-level evaluator cannot see (observed via
  Canon's `Grammar of the Shot` probe, applied to a real video failure: Devanagari misspelling
  *changed* mid-clip). Battery design should include an `observation_unit` concept
  (frame/shot/shot_pair/sequence) from the start.
- 64 already-scored generations exist in the `media-factory` repo (`spike/out/scores.json`, not
  yet copied into this repo) — real material, already graded, before any new spend.

**OPEN QUESTIONS:** which published benchmark taxonomies (T2I-CompBench, VBench, GenEval, etc.) to
adopt methodology from — see `resources/corpus/CORPUS-SOURCING-PLAN.md`. Whether a Devanagari
text-rendering benchmark exists publicly (currently believed: no) — if confirmed absent, one must
be built.

**DEPENDENCIES:** needs Resources for corpus/evaluation media. Canon needs Eval's Registry before
hypothesis 15 (routing) is testable.

**PROPOSED CROSS-STREAM CHANGES:** none filed yet.

**NEXT APPROVED TASK:** none — do not self-assign. Suggested candidate (not started): EVAL-001,
verify whether a public Devanagari text-rendering benchmark exists.
