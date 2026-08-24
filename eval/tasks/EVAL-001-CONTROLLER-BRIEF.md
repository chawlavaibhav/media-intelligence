# Controller Brief — EVAL-001

**TASK:** EVAL-001 — Capability Lab V0 battery design
**STATUS:** needs_controller_review

**HUMAN SUMMARY**

No public benchmark covers Devanagari, so the Hindi text test cannot be borrowed and must be
calibrated locally against a native speaker. The closest published study covers Bengali — the
nearest script structurally — which came third worst of its twelve languages: corroboration for
our own Hindi failures, not a substitute for measuring them. Two outside teams independently
reached designs this project had already reached (transcribe-never-confirm checking, and
cost-per-success including human review). The second exposed a real gap in our cost model:
**human verification is roughly 25× generation cost**, so the budget question is people's hours,
not API spend. Nothing runs until you decide on ~11–14 hours of calibration time, 3–4 of them a
Hindi first-language reader.

**WHAT I DID**

Reviewed eight published benchmark methodologies plus one vendor pricing page, audited the
repository's own evidence against the underlying data files, and drafted the battery
specification, Registry schema and instrument-calibration plan. Zero generations, zero paid API
calls, ₹0 spent, no dataset acquired. All outputs are proposals per Controller clarification 1.

**OBSERVED** *(source-supported; sources tabulated in findings §7, detail in §1–§5)*

**From published sources:**
1. **No public benchmark covers Devanagari or Hindi text rendering.** MULTITEXTEDIT (May 2026)
   covers 12 languages including Bengali, not Devanagari; Bengali is its third worst
   (∆text-accuracy 0.960, ∆script-fidelity 1.172), behind Hebrew and Arabic. CVTG-2K, ChineseWord,
   TextAtlasEval, LongText-Bench, MARIO-Eval and AnyText are English/Chinese only.
2. MULTITEXTEDIT independently uses FINDINGS-01's two-stage trace-then-judge protocol (κ 0.76 vs
   native speakers). T2VTextBench (May 2025): all 10 video systems below 0.4 on on-screen text
   fidelity and temporal consistency. HYPE-EDIT-1 (Jan 2026) computes effective cost per success
   **including human review time**.
3. Instrument-choice evidence: DINO reaches 50.72% human alignment on concept preservation against
   83.31% for a structured multimodal judge (DreamBench++). GenEval reports 83% agreement against
   88% inter-annotator, with the detector confined to MS COCO's 80 classes.

**From this repository:**
4. Six provenance problems in our own material, itemised in findings §5: Devanagari ground truth
   unconfirmed by a native reader, with that caveat not carried into `eval/HANDOFF.md` or the V0
   plan; "14/14" is verdict accuracy while the same finding records diagnosis as incomplete; three
   files in `eval/runs/finding-01-devanagari-check/` are entirely API errors; the Tesseract 0/14
   claim has no artifact; `check-vlm.mjs` hardcodes a non-existent path; the 14 samples come from
   4 independent sources, not 14.
5. `media-factory/spike/out/scores.json` confirms the cited counts exactly — 64 records, 10
   failures, nano 7/32, seedream 3/32. Read read-only; not copied, not re-scored.

**INFERRED**

The Devanagari instrument cannot be borrowed and must be calibrated locally, which makes the
string set (media requirement M1) the highest-value unowned item in the plan. Human verification,
not API spend, is the binding cost constraint. The plan's "≈720 generations" is both over-counted
(operational behaviour generates nothing) and mis-specified (image and video workflows cannot be
crossed with the same dimensions).

**SURPRISES / BELIEF UPDATES**

- Two published sources converged on designs we derived locally. External convergence is stronger
  evidence for the trace-then-judge protocol and for cost-per-success than our own reasoning was.
- Cost intuition was wrong by an order of magnitude. Generation is 2–4% of a test cell; human
  checking is nearly all of it.
- **Do not take at face value:** "qwen3-vl-235b scored 14/14 correct verdicts." The phrasing is
  accurate, but it is a *verdict* score on labels no Hindi first-language reader has confirmed,
  from a sample of 4 independent sources. Downgraded to `provisional_uncalibrated` throughout.

**FAILURES / BLOCKERS**

None blocked EVAL-001. Four block a *run*: no native-speaker ground truth for the Devanagari
instrument; no frozen identity rubric or reference sets; ~11–14 hours of human calibration time
unbudgeted; `check-vlm.mjs` not runnable as committed.

**UNKNOWN / NOT VERIFIED**

- Whether Tesseract genuinely fails on Devanagari — the 0/14 claim has no artifact. Carried as
  unverified, and deliberately not used to justify the Hindi instrument's cost.
- Devanagari ground-truth labels — never confirmed by a Hindi first-language reader.
- Checker run-to-run consistency — one run per sample, never measured.
- Nano Banana **Pro** pricing — not confirmed on the vendor page. The plan's observed ~$0.15 is
  consistent with it, but only the base Nano Banana ($0.0398) appears on fal.ai's public page.
- Whether the four V0 dimensions are the *right* four. They are the traceable, affordable four.
  Coverage is not claimed.

**ASSUMPTIONS CHALLENGED**

None promoted or demoted — no experiment was run. Three informed (findings §8): **§12** gains
external support for CpAO's shape and independent confirmation of its stated weakness (missing
intelligence-layer cost); **§4**'s observation-unit channel gains a second instance; **§15** stays
blocked and remains untestable after V0, since V0 is A-side only.

**LOCAL IMPLICATIONS**

Four V0 dimensions traceable to the existing plan, plus two flagged `proposed_addition` needing
your decision. D4 restricted to COCO-representable objects; brand marks deferred with no
calibratable instrument.

**CROSS-STREAM IMPLICATIONS** — proposed, not acted on. No `PROPOSED-INTEGRATION-CHANGE` filed
pending your direction on which to formalise.

- **CROSS_STREAM → Canon.** SPEC-01 open question 1 (element-reference naming) is unresolved, so
  the battery cannot cite IR paths mechanically. Nine path mismatches in
  `CAPABILITY-LAB-V0-PLAN.md` are tabulated in battery §7.2 — including one substantive error:
  on-screen Devanagari is cited against `audience.language` rather than
  `audience.language.on_screen_copy` + `copy.script_system`.
- **CROSS_STREAM → Empirical Memory / Planner.** Four Registry fields touch routing or memory
  semantics; marked `PROPOSED · CROSS_STREAM` in the schema rather than assumed.
- **CROSS_STREAM → Resources.** Five media requirements (battery §9). M1 cannot be acquired and
  must be built; M5 (media-factory spike outputs) is a dependency for a later integration task.

**ARCHITECTURAL IMPLICATIONS**

None requiring a stop. Schema gaps were representable as proposed fields, not an inability of the
architecture to hold the evidence.

**DECISIONS NEEDED FROM CONTROLLER**

1. **The two `proposed_addition` dimensions — approve or hold.** `exact_text_latin` is a control:
   without it a Devanagari failure rate cannot distinguish "bad at text" from "bad at Devanagari",
   and that distinction changes routing. `text_stability_across_frames` is our most distinctive
   measurement.
2. **The workflow roster.** Costing cannot be finalised without it; battery §8.3 is illustrative.
3. **Human calibration budget:** ~11–14 hours, 3–4 of them a Hindi first-language reader. Gates
   every Devanagari Registry entry.
4. **Owner for M1**, the Devanagari string set. Nobody owns it.
5. **Which cross-stream items to formalise** as `PROPOSED-INTEGRATION-CHANGE` files.

**EVIDENCE WORTH HUMAN INSPECTION**

- `eval/findings/EVAL-001-battery-design-findings.md` §1 — the Devanagari gap and the Bengali
  proxy table. This is the finding that shapes the roadmap.
- Battery draft §8.3 — the cost arithmetic showing human verification dominating.

**FILES CREATED / MODIFIED**

Created: `eval/battery/CAPABILITY-BATTERY-V0-DRAFT.md`,
`eval/battery/CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml`,
`eval/battery/INSTRUMENT-CALIBRATION-PLAN-V0.md`,
`eval/findings/EVAL-001-battery-design-findings.md`, this brief.
Modified: `eval/HANDOFF.md` — added FINDINGS-01's own preliminary-ground-truth caveat, which the
handoff did not carry forward, and recorded EVAL-001's outputs as drafts pending review. Done under
the Runbook's provision that a worker may update its own handoff. No historical finding, script or
result file was altered (clarification 12).

**RECOMMENDED NEXT STEP** *(recommendation, not an action taken)*

Resolve decisions 1–4, then open a separate task to build M1 and run the I1/I2 calibrations before
any capability run. Calibration is a gate that precedes measurement: a score from an uncalibrated
instrument is not a weak measurement but a false one.

**EPISTEMIC CHECK**

Every figure is read from a named published source or a file in this repository, attributable via
findings §7 (sources) or §5 (repository evidence). Interpretations are confined to INFERRED,
unknowns are listed rather than filled, and no draft dimension, schema field or threshold is
presented as approved.

**CONFIRMATION**

No unapproved next strategic step was started. No model benchmarked, no generation call made, no
money spent, no dataset acquired, no shared architecture changed. EVAL-002 not started.
