# Eval / Capability Lab — Handoff

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Plain English, minimum
sufficient wording, no invention, evidence separated from inference.

**PURPOSE:** Design measurement, calibrate evaluators, empirically test current model/workflow
capability, produce the Capability Registry.

**CURRENT STATE**

One completed calibration study (`findings/FINDINGS-01-can-we-check.md`): a Devanagari-text VLM
checker study on 14 samples. qwen3-vl-235b scored 14/14 correct verdicts; claude-sonnet-4.5
produced 6 false passes on the same material; Tesseract (Hindi) is reported as failing entirely.

⚠️ **Treat that study as preliminary, not settled.** FINDINGS-01 states its own limits and they
have not been resolved: the ground-truth labels were never confirmed by a Hindi first-language
reader; the 14 samples come from only **4 independent sources** (12 are correlated frames from 4
clips); each sample was run once, so checker consistency is unmeasured; and no artifact in this
repository supports the Tesseract 0/14 line. Detail in
`findings/EVAL-001-battery-design-findings.md` §5.

A V0 battery specification, Registry schema and instrument-calibration plan now exist **as drafts
pending Controller review** (EVAL-001). No battery is approved. No Capability Registry exists. No
provider benchmarking has run.

**CURRENT APPROVED DECISIONS:** Technical hard-fidelity and creative-fitness evaluation are
separate instruments. An evaluator must be calibrated against human judgement on the specific task
before being trusted. Capability claims must name the measuring instrument and conditions.

**LAST COMPLETED TASK:** EVAL-001 — battery design. Deliverables committed on `work/eval`;
Controller Brief at `tasks/EVAL-001-CONTROLLER-BRIEF.md`, status `needs_controller_review`.

**CURRENT TASK / QUEUE:** none approved beyond EVAL-001. Do not start EVAL-002.

**IMPORTANT OBSERVATIONS**

- A capability number without its instrument and calibration reference is not trustworthy.
- An instrument has two accuracies: **gate** (pass/fail, consumed by routing) and **diagnosis**
  (what broke, consumed by repair). Qwen3-VL's 14/14 is a gate score; the same finding records its
  diagnosis as incomplete. Do not cite a bare "14/14" as general accuracy.
- Cross-frame/shot failures require an explicit `observation_unit`. Vocabulary is already defined
  in `canon/knowledge/SPEC-04-operational-bindings.md` and must be adopted, not reinvented.
- Frames from one clip are **one trial**, never N. Report `n_items` alongside `n_trials`.
- **No public benchmark covers Devanagari text rendering** (EVAL-001 review, 24 Aug 2026). The
  instrument must be calibrated locally; there is nowhere to borrow it from.
- Human verification, not API spend, dominates run cost — roughly 25× generation in the worked
  example.
- Published benchmarks are methodology inputs, not our capability scores.
- `scripts/check-vlm.mjs` hardcodes a path that does not exist on this machine and cannot be run
  as committed. Fixing it is a prerequisite for any re-calibration.

**OPEN QUESTIONS:** which instruments can be calibrated cheaply enough for V0 beyond those already
specified; how Registry freshness should decay once drift has actually been observed (no formula
invented in V0, per Controller clarification 10).

**DEPENDENCIES:** EVAL-001 records five media requirements for Resources (battery draft §9); M1, a
native-speaker-verified Devanagari string set, cannot be acquired and must be built, and has no
owner. Capability Lab runs wait on Controller approval of the battery and on human calibration
time being budgeted.

**PROPOSED CROSS-STREAM CHANGES:** three identified in the EVAL-001 brief (to Canon, to Empirical
Memory/Planner, to Resources). **None filed as `PROPOSED-INTEGRATION-CHANGE` files** — awaiting
Controller direction on which to formalise.

**NEXT APPROVED TASK:** none. After Controller review of EVAL-001, stop; do not start benchmarking
or spend on generation without a new approved task.
