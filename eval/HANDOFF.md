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

A V0 battery specification, Registry schema and instrument-calibration plan exist **as drafts
pending final Controller review** (EVAL-001, revision 3). Seven dimensions are defined.
`exact_text_latin` and `text_stability_across_frames` are Controller-approved for V0 (24 Aug 2026);
`object_count` and `spatial_relationship` were split apart at Controller direction. The battery as a
whole, the workflow roster, the human-time budget and the Registry cross-stream fields remain
**unapproved**. No Capability Registry exists. No provider benchmarking has run.

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
- **Devanagari OCR / scene-text benchmarks exist and are numerous.** What does not exist, as far as
  the EVAL-001 review could establish (24 Aug 2026), is any benchmark measuring whether a
  *generative* model correctly renders Devanagari it was told to produce. Reading and drawing are
  different capabilities — do not cite an OCR benchmark as evidence about a generator.
  Those recognition resources are, however, candidate material for calibrating our *reading*
  instrument, conditional on Resources verifying licensing.
- **Clean synthetic Devanagari renders do not discriminate between checkers** (all ten systems in
  arXiv:2606.29213v1 cluster at chrF++ 91–98). Any calibration set must include degraded and real
  material.
- **Human verification can materially dominate run cost and must be in the cost model.** The
  specific ratio in battery §8.3 is an illustrative scenario under unapproved assumptions, not a
  measured finding.
- **V0 calibration thresholds are qualification gates, not error rates.** "Zero false passes" on a
  V0-sized set is consistent with a true rate of ~18% (text) or ~26% (identity). Never describe an
  instrument as low-error on V0 evidence — see `battery/INSTRUMENT-CALIBRATION-PLAN-V0.md` §2b.
- **Counting and spatial placement are separate capabilities.** They share a detector but need
  different confidence settings and produce separate Registry entries.
- Published benchmarks are methodology inputs, not our capability scores.
- `scripts/check-vlm.mjs` hardcodes a path that does not exist on this machine and cannot be run
  as committed. Fixing it is a prerequisite for any re-calibration.

**OPEN QUESTIONS:** which instruments can be calibrated cheaply enough for V0 beyond those already
specified; how Registry freshness should decay once drift has actually been observed (no formula
invented in V0, per Controller clarification 10).

**DEPENDENCIES:** EVAL-001 records media requirements for Resources (battery draft §9). M1 is split:
**M1a** — published Devanagari recognition material, reusable for instrument calibration *if
Resources clears it for bounded internal evaluation under `resources/CHARTER.md`* (licence silence
alone is no longer a block); **M1b** — the capability item set, which must be built, though its
target strings may be sourced from existing permissible Hindi text rather than authored. Neither has
an owner. Capability Lab runs wait on Controller approval of the roster and on human calibration
time being budgeted: **≈ 11–15.5 hours, of which 2–4 must be a Hindi first-language reader**.

**PROPOSED CROSS-STREAM CHANGES:** three identified in the EVAL-001 brief (to Canon, to Empirical
Memory/Planner, to Resources). **None filed as `PROPOSED-INTEGRATION-CHANGE` files** — awaiting
Controller direction on which to formalise.

**NEXT APPROVED TASK:** none. After Controller review of EVAL-001, stop; do not start benchmarking
or spend on generation without a new approved task.
