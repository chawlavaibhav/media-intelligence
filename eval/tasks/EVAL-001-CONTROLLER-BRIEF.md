# Controller Brief — EVAL-001

**TASK:** EVAL-001 — Capability Lab V0 battery design
**STATUS:** needs_controller_review — **revision 2, 24 Aug 2026.** Three evidence corrections
applied after Controller review; D2 and D5 approved for V0.

**HUMAN SUMMARY**

My earlier claim that "no Devanagari benchmark exists" was **too broad and is withdrawn**.
Devanagari benchmarks do exist — they measure *reading* text, not *drawing* it. The narrowed claim
survives re-checking: nothing public measures whether a generative model correctly renders
Devanagari it was told to produce. That is better news than the original claim, because those
reading benchmarks can calibrate our *checker*, so the material we must build shrinks. It also
forced a real design fix: one study finds all ten systems it tested scoring within a 7-point band on
clean text, so a calibration set of clean renders would have separated nothing. Nothing runs until
you decide on ~10–14 hours of calibration time, 2–4 of them a Hindi first-language reader, and
until Resources checks whether the reusable material is licensed for our use.

**WHAT I DID**

Reviewed eight published benchmark methodologies plus one vendor pricing page, audited the
repository's own evidence against the underlying data files, and drafted the battery
specification, Registry schema and instrument-calibration plan. Zero generations, zero paid API
calls, ₹0 spent, no dataset acquired. All outputs are proposals per Controller clarification 1.

**OBSERVED** *(sources tabulated in findings §7; repository evidence in §5)*

1. **Devanagari *recognition* benchmarks exist and are numerous** — arXiv:2606.29213v1 (Jun 2026),
   IIIT-ILST, IndicSTR12, Bharat Scene Text Dataset, IndicVisionBench, MLT-17/19, DohaScript
   (findings §1.1). **Generative text-rendering benchmarks do not cover Devanagari** — CVTG-2K,
   ChineseWord, TextAtlasEval, LongText-Bench, MARIO-Eval, AnyText, OneIG-Bench are EN/ZH;
   MULTITEXTEDIT covers Bengali (third worst of twelve), not Devanagari.
2. **arXiv:2606.29213v1:** all ten systems cluster at chrF++ 91–98 on clean rendered Devanagari; on
   real scans nine of ten collapse across a 76-point range; "strong English OCR does not predict
   Indic OCR"; DeepSeek-OCR showed rare catastrophic repetition failures despite the best median
   (findings §1.3).
3. **T2VTextBench arXiv:2505.04946v1** (8 May 2025, only version): *"the highest average score is
   reported for Sora, which is only 0.37"* — all ten systems below 0.4 on a 0/0.25/0.5/1 scale.
4. Method/instrument evidence: MULTITEXTEDIT independently uses FINDINGS-01's trace-then-judge
   protocol (κ 0.76 vs native speakers); HYPE-EDIT-1 (Jan 2026) computes cost per success
   **including human review time**; DreamBench++ reports DINO at 50.72% human alignment vs 83.31%
   for a structured multimodal judge; GenEval 83% vs 88% inter-annotator, detector confined to MS
   COCO's 80 classes.
5. **Six provenance problems in our own material** (findings §5): unconfirmed Devanagari ground
   truth, with that caveat absent from `eval/HANDOFF.md` and the V0 plan; "14/14" is verdict not
   diagnostic accuracy; three run files are entirely API errors; the Tesseract 0/14 claim has no
   artifact; `check-vlm.mjs` hardcodes a non-existent path; 14 samples come from 4 independent
   sources.
6. `media-factory/spike/out/scores.json` confirms the cited counts exactly — 64 records, 10
   failures, nano 7/32, seedream 3/32. Read read-only; not copied, not re-scored.

**INFERRED**

The Devanagari instrument must still be calibrated locally — nothing public scores Devanagari
*generation* — but the calibration material is now partly reusable, so the build shrinks to M1b
(prompt/target-string pairs) with M1a reuse conditional on Resources verifying licensing. Human
verification can materially dominate run cost and must be in the cost model. The plan's
"≈720 generations" is both over-counted (operational behaviour generates nothing) and mis-specified
(image and video workflows cannot be crossed with the same dimensions).

**SURPRISES / BELIEF UPDATES**

- **My own claim was too broad and Controller review caught it.** I had collapsed reading and
  drawing into one capability.
- **A clean-render calibration set would have separated nothing** (all ten systems within a 7-point
  band). The original sample design was wrong and is corrected.
- Our cost model omitted human verification. **Supported conclusion: it can materially dominate and
  must be included.** The "2–4%" figure is an illustrative scenario, not a finding.
- Two published teams independently reached designs we had already reached — stronger evidence than
  our own reasoning was.
- **Do not take at face value:** "qwen3-vl-235b scored 14/14 correct verdicts." Accurate phrasing,
  but a *verdict* score on labels no Hindi first-language reader has confirmed, from 4 independent
  sources.

**FAILURES / BLOCKERS**

None blocked EVAL-001. Four block a *run*: no native-speaker ground truth for the Devanagari
instrument; no frozen identity rubric or reference sets; ~11–14 hours of human calibration time
unbudgeted; `check-vlm.mjs` not runnable as committed.

**UNKNOWN / NOT VERIFIED**

- **OneIG-Bench's Multilingualism set — language list NOT VERIFIED** (README silent, OpenReview PDF
  blocked). If it includes Devanagari, finding §1.2 narrows further.
- **M1a licence status.** arXiv:2606.29213 states its release and shows a CC BY 4.0 icon; **Eval has
  not verified it and must not** — Resources' work.
- Whether checker rankings from printed-scan benchmarks transfer to generated-image text, a
  different regime. This is what local calibration must settle.
- Whether Tesseract genuinely fails on Devanagari — published data makes the blanket claim doubtful.
  Re-test rather than write off.
- Devanagari ground-truth labels; checker run-to-run consistency; Nano Banana **Pro** pricing.
- Whether the six V0 dimensions are the *right* six. Coverage is not claimed.

**ASSUMPTIONS CHALLENGED**

None promoted or demoted — no experiment was run. Three informed (findings §8): **§12** gains
external support for CpAO's shape and independent confirmation of its stated weakness (missing
intelligence-layer cost); **§4**'s observation-unit channel gains a second instance; **§15** stays
blocked and remains untestable after V0, since V0 is A-side only.

**LOCAL IMPLICATIONS**

Six V0 dimensions, all Controller-approved (D2 and D5 approved 24 Aug 2026). D4 restricted to
COCO-representable objects; brand marks deferred with no calibratable instrument.

**CROSS-STREAM IMPLICATIONS** — proposed, not acted on. No `PROPOSED-INTEGRATION-CHANGE` filed
pending your direction on which to formalise.

- **→ Canon.** SPEC-01 open question 1 (element-reference naming) is unresolved, so the battery
  cannot cite IR paths mechanically. Nine path mismatches tabulated in battery §7.2, including one
  substantive error: on-screen Devanagari cited against `audience.language` rather than
  `audience.language.on_screen_copy` + `copy.script_system`.
- **→ Empirical Memory / Planner.** Four Registry fields touch routing or memory semantics; marked
  `PROPOSED · CROSS_STREAM` in the schema rather than assumed.
- **→ Resources.** Media requirements in battery §9. **M1a licence verification is now the gating
  question** — it determines both how much of M1 must be built and the human-hour estimate.

**ARCHITECTURAL IMPLICATIONS**

None requiring a stop. Schema gaps were representable as proposed fields, not an inability of the
architecture to hold the evidence.

**DECISIONS NEEDED FROM CONTROLLER**

1. ~~D2 and D5~~ — **RESOLVED 24 Aug 2026: both approved for V0.** Recorded as
   `controller_approved_v0` in battery §6.2 and §6.5.
2. **The workflow roster.** Costing cannot be finalised without it; battery §8.3 is illustrative.
3. **Human calibration budget:** ~10–14 hours, 2–4 of them a Hindi first-language reader. The range
   depends on decision 4. Gates every Devanagari Registry entry.
4. **M1, now split (battery §9.1).** **M1a** — ask Resources to verify licensing on published
   Devanagari recognition resources so their images and ground truth can calibrate our checker.
   **M1b** — assign an owner for the prompt/target-string set, which must still be built. Nobody
   owns either today.
5. **Which cross-stream items to formalise** as `PROPOSED-INTEGRATION-CHANGE` files.

**EVIDENCE WORTH HUMAN INSPECTION**

- `eval/findings/EVAL-001-battery-design-findings.md` §1 — the narrowed Devanagari claim and what
  the reading benchmarks do and do not give us. The section that changed most in revision 2.
- `INSTRUMENT-CALIBRATION-PLAN-V0.md` §3.1 — the three design corrections the new evidence forced.

**FILES CREATED / MODIFIED**

Created (rev 1): the battery draft, Registry schema, calibration plan, findings and this brief,
all under `eval/`.
Modified (rev 2): battery draft §6.2, §6.5, §7.1, §8.3, §8.4, §9/§9.1, §12; calibration plan §3.1,
§3.2, §4, §5; findings §1, §4, §5.4, §7; this brief; `eval/HANDOFF.md`.
**No historical finding, script or result file has been altered at any point** (clarification 12).

**RECOMMENDED NEXT STEP** *(recommendation, not an action taken)*

Resolve decisions 2–4. Ask Resources to verify M1a licensing first, since it determines both the
human-hour estimate and how much of M1 must be built. Then open a separate task to build M1b and run
the I1/I2 calibrations — before any capability run. Calibration is a gate that precedes measurement:
a score from an uncalibrated instrument is not a weak measurement but a false one.

**EPISTEMIC CHECK**

Every figure is read from a named published source or a file in this repository, attributable via
findings §7 or §5. Interpretations are confined to INFERRED, unknowns are listed rather than filled,
and nothing is presented as approved beyond D2 and D5.

**Revision 2 specifically:** the over-broad Devanagari claim is marked withdrawn in place rather
than quietly deleted; the cost ratio is demoted to an illustrative scenario with its assumptions
named; all T2VTextBench figures are pinned to v1 with no cross-version mixing; and every proposed
reuse of external material is marked conditional on Resources verifying licensing.

**CONFIRMATION**

No unapproved next strategic step was started. No model benchmarked, no generation call made, no
money spent, no dataset acquired, no shared architecture changed. EVAL-002 not started.
