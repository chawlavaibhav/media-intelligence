# Controller Brief — EVAL-001

**TASK:** EVAL-001 — Capability Lab V0 battery design
**STATUS:** needs_controller_review

**WHAT I DID:** Reviewed eight published benchmark methodologies plus the fal.ai public pricing
page, audited the repository's own evidence against the underlying artifacts, and drafted a V0
battery specification, a Registry schema, and an instrument-calibration plan. Zero generations,
zero paid API calls, ₹0 spent, no dataset acquired, no historical file modified. All outputs are
proposals per Controller clarification 1.

---

**OBSERVED**

1. **No public benchmark covers Devanagari or Hindi text rendering.** The nearest published work,
   MULTITEXTEDIT (May 2026, 12 languages), covers Bengali but not Devanagari. Bengali is its
   third-worst-performing language (∆text-accuracy 0.960, ∆script-fidelity 1.172), behind only
   Hebrew and Arabic. CVTG-2K, ChineseWord, TextAtlasEval, LongText-Bench, MARIO-Eval and AnyText
   are English/Chinese only.
2. **MULTITEXTEDIT independently arrived at FINDINGS-01's checker protocol** — a two-stage
   trace-then-judge design — reporting κ 0.76 against native-speaker annotators.
3. **T2VTextBench (May 2025) measures on-screen text fidelity and temporal consistency in video.**
   All 10 systems evaluated scored below 0.4 on a 0–1 scale; best 0.37.
4. **HYPE-EDIT-1 (Jan 2026) computes effective cost per success including human review time**, and
   reports that low per-image pricing becomes expensive once retries and review are counted.
5. **DreamBench++ reports DINO at 50.72% human alignment on concept preservation** against 83.31%
   for a structured multimodal judge, concluding DINO prioritises shape and colour over detailed
   features.
6. **GenEval reports 83% instrument agreement against 88% inter-annotator agreement**, and its
   authors record that the detector is confined to MS COCO's 80 classes and degrades
   out-of-distribution.
7. **Auditing our own material** (detail in findings §5): Devanagari ground truth is unconfirmed by
   a native reader and is quoted as settled in `eval/HANDOFF.md`; "14/14" is a *verdict* score and
   the same finding records the diagnosis as incomplete; three files in
   `eval/runs/finding-01-devanagari-check/` are entirely API errors; the Tesseract 0/14 claim has no
   supporting artifact; `eval/scripts/check-vlm.mjs` hardcodes a path that does not exist;
   FINDINGS-01's 14 samples come from 4 independent sources.
8. **`media-factory/spike/out/scores.json` confirms the cited counts exactly** — 64 records, 10
   failures, nano 7/32, seedream 3/32. Read read-only; not copied, not re-scored.

**INFERRED**

- The Devanagari instrument cannot be borrowed and must be calibrated locally against
  native-speaker ground truth. This makes the M1 string set the highest-value item in the plan and
  it currently has no owner.
- Bengali's poor showing is corroborating context for our observed Devanagari failures, not a
  substitute measurement.
- Human verification, not API spend, is the binding cost constraint: generation is 2–4% of a cell's
  cost in the worked example.
- The plan's `≈720 generations` figure is both over-counted (operational behaviour generates
  nothing) and mis-specified (image and video workflows cannot be crossed with the same dimensions).

**SURPRISES**

Two published sources independently reached conclusions this project had derived locally: the
trace-then-judge checker protocol, and cost-per-success including human review. Convergence from
outside is stronger evidence for both than our own reasoning was.

**FAILURES / BLOCKERS**

None blocked EVAL-001. Four items block a *run*: no native-speaker ground truth for the Devanagari
instrument; no frozen identity rubric or reference sets; ~11–14 hours of human calibration time
unbudgeted; and `check-vlm.mjs` not runnable as committed.

**ASSUMPTIONS CHALLENGED**

None promoted or demoted — no experiment was run. Three informed (findings §8): **§12** gains
external support for CpAO's shape and independent confirmation of its stated weakness, the missing
intelligence-layer cost; **§4**'s observation-unit channel gains a second instance; **§15** remains
blocked and stays untestable after V0, since V0 is A-side only.

**LOCAL IMPLICATIONS**

Four V0 dimensions traceable to the existing plan (Devanagari exact text, person identity across
prompts, object count and spatial placement, operational behaviour), plus two flagged
`proposed_addition` requiring your decision. D4 is restricted to COCO-representable objects; brand
marks are deferred with no calibratable instrument.

**CROSS-STREAM IMPLICATIONS** — proposed, not acted on. No `PROPOSED-INTEGRATION-CHANGE` filed
pending your direction on which of these you want formalised.

- **CROSS_STREAM → Canon.** SPEC-01 open question 1 (element-reference naming) is unresolved, so
  the battery cannot cite IR paths mechanically. Separately, `CAPABILITY-LAB-V0-PLAN.md` uses
  `static.*` and `video.*` shorthands that are not SPEC-01 paths, and cites `audience.language` for
  on-screen Devanagari where the correct fields are `audience.language.on_screen_copy` and
  `copy.script_system`. Flagged, not invented around.
- **CROSS_STREAM → Empirical Memory / Planner.** Registry fields `observation_unit`,
  `failed_trials[].defects[]`, `calibration_status: required_but_no_calibrated_instrument`, and
  `usd_per_repair_attempt` touch routing or memory semantics. Marked `PROPOSED · CROSS_STREAM` in
  the schema rather than treated as accepted.
- **CROSS_STREAM → Resources.** Five media requirements (battery §9). M1 — a native-speaker-verified
  Devanagari string set — cannot be acquired and must be built. M5 — access to the media-factory
  spike outputs — is a recorded dependency for a later integration task.

**ARCHITECTURAL IMPLICATIONS**

None requiring an immediate stop. The Registry schema gaps were representable as proposed fields
rather than as an inability of the architecture to hold the evidence.

**DECISIONS NEEDED FROM CONTROLLER**

1. Approve or hold the two `proposed_addition` dimensions: `exact_text_latin` (control, without
   which a Devanagari failure rate is uninterpretable) and `text_stability_across_frames`.
2. The workflow roster. Battery §8.3 is an illustrative example only.
3. Human calibration budget: ~11–14 hours, of which 3–4 must be a Hindi first-language reader.
4. Owner for M1, the Devanagari string set.
5. Which cross-stream items above to formalise as `PROPOSED-INTEGRATION-CHANGE` files.
6. Whether `eval/HANDOFF.md` should be corrected — it currently carries "qwen3-vl-235b scored
   14/14" without the verdict-vs-diagnosis qualifier, and the next Eval session will inherit it.
   **I did not edit it**, since doing so would promote an EVAL-001 conclusion into stream state
   before your review.

**FILES CREATED / MODIFIED**

Created — `eval/battery/CAPABILITY-BATTERY-V0-DRAFT.md`,
`eval/battery/CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml`,
`eval/battery/INSTRUMENT-CALIBRATION-PLAN-V0.md`,
`eval/findings/EVAL-001-battery-design-findings.md`, this brief.
**Modified — none.** No historical finding, script or result file was altered (clarification 12).

**RECOMMENDED NEXT STEP** *(a recommendation, not an action taken)*

Resolve decisions 1–4, then open a separate task to build M1 and run the I1 and I2 calibrations —
before any capability run. Calibration is a gate that precedes measurement, and a capability score
from an uncalibrated instrument is not a weak measurement but a false one.

**CONFIRMATION**

No unapproved next strategic step was started. No model was benchmarked, no generation call made,
no money spent, no dataset acquired, no shared architecture changed, and no draft decision promoted
into shared truth. EVAL-002 was not started.
