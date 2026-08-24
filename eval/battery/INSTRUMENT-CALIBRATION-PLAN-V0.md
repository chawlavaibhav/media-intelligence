# Instrument Calibration Plan V0 — DRAFT

**Task:** EVAL-001 · **Date:** 24 Aug 2026 · **Status: PROPOSAL. Not approved.**

**No calibration was performed in this task.** Per Controller clarification 4, EVAL-001 performs
no new human calibration; it specifies what would be required. Zero generations, zero API calls,
₹0 spent.

---

## 1 · Why this document exists before any measurement

The Charter states it as a rule: *"Any new evaluator/instrument before it is calibrated against
human judgement on the specific task (per Finding 01: an uncalibrated checker is worse than
none)"* requires Controller review.

The evidence behind that rule is worth restating precisely, because the asymmetry in it drives
every threshold below. In FINDINGS-01, one VLM returned `exact_match: true, edit_distance: 0` on
six frames that another VLM scored at edit distance 1–2 against the same target string. I
re-read the raw files at `eval/runs/finding-01-devanagari-check/` and confirm the pattern.

The failure was **not random**. A language model's prior pulls it toward the plausible word, so
as a spelling verifier it produces **false passes specifically**. Built on that checker, the
pipeline ships broken work *with a passing grade attached* — the silent failure the product
exists to eliminate, made worse by the appearance of verification.

**Consequence for every threshold in §4: false passes and false fails are not symmetric.** A
false fail costs a wasted regeneration. A false pass costs a customer relationship. Thresholds
are therefore set asymmetrically and stated as such.

---

## 2 · What calibration is, and what it is not

**Calibration** holds the material fixed with known ground truth and varies the *instrument*.
The question is "which checker is right." FINDINGS-01 is a calibration study.

**Capability measurement** holds the instrument fixed at a calibrated one and varies the *model*.
The question is "how often does this workflow succeed."

They produce different numbers and must never be run together or reported as one. A capability
score computed with an uncalibrated instrument is not a weak measurement — it is not a
measurement. Scored with Claude Sonnet 4.5, the Wan clip would have recorded **100% Devanagari
fidelity for a model that corrupts every frame.**

**Calibration is a gate that precedes measurement, and it expires** when the instrument's version
changes.

---

## 3 · Per-instrument calibration requirements

Each instrument below states: what it is, the ground truth it must be measured against, the
sample design, the acceptance thresholds, the human time required, and the re-calibration
triggers.

---

### 3.1 · I1 — Devanagari transcription VLM (D1, D5 level 2+)

**Instrument.** VLM instructed to transcribe without correcting, followed by deterministic NFC
normalisation and comparison. The transcription step is the entire uncertainty; the comparison
step is deterministic and needs no calibration.

**Current state: `provisional_uncalibrated`.** Per clarification 4, the existing result is
preliminary. Two reasons, both from FINDINGS-01's own "Limits of this result":

1. **Ground truth is unconfirmed by a native reader.** The finding states plainly: *"neither
   reader's first language is Hindi. A Hindi reader should confirm the labels before this is
   quoted."* No record of that confirmation exists in the repository.
2. **The sample is correlated.** 14 samples but **4 independent sources**; 12 are frames from 4
   clips.

Additionally, only one run per sample was made, so run-to-run consistency is unmeasured.

**Ground truth required.** A **Hindi first-language reader**, transcribing what is drawn — not
what it should say — blind to any model output and blind to the target string. Blindness to the
target matters: a reader shown "सुबह की पहली चाय" and asked "does this match?" is subject to the
same auto-correction pull that broke the model checker.

#### Reusable material — revised 24 Aug 2026 after Controller review

An earlier version of this plan assumed the whole calibration set had to be built. **That was
based on an over-broad claim, now corrected (findings §1).** Published Devanagari *recognition*
resources carry images with human ground-truth transcriptions, which is exactly what calibrating a
*reading* instrument needs. Candidates: the arXiv:2606.29213v1 release (stated as benchmark, code
and models released; arXiv page shows a CC BY 4.0 icon), the Bharat Scene Text Dataset, IIIT-ILST
and IndicSTR12.

**All reuse is conditional on Resources verifying licensing.** Eval has not verified any licence
and must not — per Project Contract separation 9 and RES-001's ownership, rights verification is
Resources' work. Until it clears, treat M1a as *candidate* material.

**What reuse does not cover.** These resources calibrate whether the checker can *read* Devanagari.
They cannot serve as capability items, which measure whether a generator can *draw* it. That set
(M1b) must still be built.

#### Three material corrections from arXiv:2606.29213v1

**1. Clean synthetic renders do not discriminate — this invalidates the original sample design.**
All ten systems in that study cluster within **chrF++ 91–98** on clean rendered Devanagari. A
calibration set of clean renders would make every candidate look equally good and would have told
us nothing. **The set must be stratified to include degraded and real-world material**, where the
same study finds nine of ten systems collapsing across a 76-point range.

**2. Do not choose the Devanagari checker on Latin performance.** The study states plainly that
strong English OCR does not predict Indic OCR — GPT-5.5 drops to 58.5 while Gemini 2.5 Flash
reaches 86.3. This independently supports our D2 Latin-control design, and forbids inferring I1's
quality from I2's.

**3. Screen for catastrophic outliers, not just mean agreement.** DeepSeek-OCR in that study
produced rare but catastrophic repetition failures — outputs reported up to 71× the reference
length — wrecking its corpus mean while its median was the best of any system. A checker with an
excellent median and a rare runaway failure is dangerous in a pipeline. **Add an explicit outlier
screen** (output length ratio, repetition detection) alongside the agreement thresholds.

⚠️ **Transfer is NOT VERIFIED.** Those figures come from printed scans and synthetic degradations.
Generated-image text is a third regime — often clean-looking but semantically wrong. Whether the
checker rankings transfer to our material is exactly what local calibration must establish, and no
external ranking may be adopted as ours.

**Sample design.**

| Property | Requirement | Reason |
|---|---|---|
| Independent items | ≥ 30 distinct strings × contexts | 4 independent sources is too few to estimate agreement |
| Correlated frames | at most 1 frame per clip counts as an item | §5.4 correlation rule |
| Broken:intact ratio | approximately 50:50 | an agreeable checker cannot pass by always saying "match" |
| Defect coverage | conjuncts, i/u matras, nukta, and the observed ब/व and य/थ pairs | the ब/व substitution is a single-character defect and is the hardest case we have actually seen |
| **Stratification** | **not all clean renders** — include degraded and real-world material, plus generated-image text | clean renders do not separate candidates (chrF++ 91–98 for all ten systems in arXiv:2606.29213v1) |
| Repeat runs | 3 runs per item on the leading candidate | consistency is currently unmeasured |
| Readers | 2 independent native readers on a ≥ 10-item overlap | inter-annotator agreement bounds achievable instrument agreement |

**Acceptance thresholds (proposed, asymmetric).**

| Measure | Threshold | Reasoning |
|---|---|---|
| **False-pass rate (gate)** | **0 in 30** | the disqualifying failure mode. Sonnet produced 6 in 13. Any false pass at this sample size is disqualifying, not a deduction. |
| False-fail rate (gate) | ≤ 10% | costs a regeneration, not a customer |
| Gate agreement with native reader | ≥ 0.90 | |
| Diagnostic agreement (character-level) | ≥ 0.75, **reported separately** | Qwen caught ब→व but silently corrected चाथ→चाय: gate right, diagnosis incomplete. A gate-qualified instrument may still be diagnosis-disqualified, and the Registry stores `instrument.role` for exactly this. |
| Run-to-run consistency | ≥ 0.95 identical verdicts across 3 runs | |
| **Catastrophic-outlier screen** | **no output exceeding 3× the reference length; no detected repetition loop** | DeepSeek-OCR's runaway outputs (up to 71× reference) wrecked its corpus mean despite the best median of any system. A rare runaway failure is disqualifying in a pipeline regardless of median quality. |
| Inter-reader agreement | reported, and the instrument threshold may not exceed it | GenEval's precedent: 83% instrument vs 88% inter-annotator — you cannot beat your ground truth |

**External reference point.** MULTITEXTEDIT reports a quadratic-weighted κ of **0.76** against
native-speaker annotators for its two-stage script-fidelity protocol. That is a published,
peer-reviewed bar for the same class of task in the same year, and a reasonable sanity anchor.
It is **not** our threshold — theirs is a graded score across 12 languages, ours is a binary gate
on one script, and clarification 4 forbids importing their result as ours.

**Human time estimate — revised.** Two cases, because M1a reuse changes the total:

- **If M1a reuse clears licensing:** existing resources supply images with ground truth, so
  native-reader time is needed mainly to verify M1b's reference renderings and to adjudicate a
  smaller local agreement check — **≈ 2–3 hours**.
- **If it does not clear:** the full set must be read from scratch — ~30 items × 2 readers × ~2 min
  plus a 10-item overlap and adjudication — **≈ 3–4 hours**, plus ~1 hour to build the strings.

Either way this remains the most load-bearing human requirement in V0, and **no one currently
owns it**. The licence question is Resources' and gates which estimate applies.

**Re-calibration triggers.** Instrument version change (FINDINGS-01: *"re-measured when its
version changes"*); provider serving-stack change; any script or font family not in the
calibration set; the target string set being extended.

**Blocking rule.** Until this passes, `instrument_state` remains `provisional_uncalibrated` and
**no D1 or D5-level-2+ Registry entry may be written.** The battery may be *designed* around it,
which is what EVAL-001 has done.

---

### 3.2 · I2 — Latin transcription (D2, D5 level 1)

**Instrument.** Same two-stage protocol, Latin script.

**Materially cheaper than I1**, for two reasons: ground truth needs no specialist reader, and a
**second independent instrument exists** — conventional OCR is viable for Latin. Where two
mechanically independent instruments agree, human verification can be sampled rather than
exhaustive.

⚠️ **State the reason for the asymmetry honestly.** FINDINGS-01 records `tesseract (hin) 0/14 —
unreadable output`, and **no supporting artifact for that run exists in the repository** (findings
§5.4), so it is carried as *unverified*. Nor does published work straightforwardly endorse it:
arXiv:2606.29213v1 reports EasyOCR — a classical engine — clustering with nine other systems at
chrF++ 91–98 on clean rendered Devanagari, collapsing only on degraded and real material.
**Whether a cheap deterministic second opinion exists for Devanagari should be re-tested rather
than assumed absent**, and I1's cost is not justified by an unreproducible number either way.

**Sample design.** ≥ 30 independent items, ~50:50 broken:intact, matched to M1 on word and
character count so the D1↔D2 delta is interpretable.

**Thresholds.** As §3.1, except diagnostic agreement ≥ 0.85 (Latin character confusions are
easier) and false-pass 0 in 30 (unchanged — the asymmetry argument does not depend on script).

**Human time estimate.** ≈ 1–1.5 hours, non-specialist.

---

### 3.3 · I3 — Identity judge (D3)

**Instrument.** VLM judging **each declared invariant separately** against the reference set,
returning a per-invariant verdict — not a holistic similarity score.

**Why embedding similarity is rejected.** DreamBench++ reports concept-preservation human
alignment of **50.72% for DINO** against **83.31%** for a structured multimodal-LLM evaluator, and
concludes DINO-based ratings *"prioritize overall shape and color over detailed features, making
them suboptimal for evaluating personalized image generation."* Our invariants are exactly
detailed features — a hair streak's position, a wardrobe colourway. An embedding metric would
have scored `nano_chai_t3` ("face drift — younger, streak moved") as a pass.

**Ground truth required.** Human judgement, per invariant, against the reference set. No
specialist qualification, but the rubric must be written before any judging begins and frozen.

**Sample design.**

| Property | Requirement |
|---|---|
| Independent items | ≥ 20 reference-set + prompt-set combinations |
| Observation unit | `asset_set_over_time` — the judge sees the **whole set**, never one image |
| Invariant declaration | every item declares both `invariants` **and** `allowed_variation` before generation |
| Drift:hold ratio | approximately 50:50, using known-drifted sets where available |
| Annotators | 2 independent, ≥ 10-item overlap |

**The `allowed_variation` requirement is load-bearing, not bookkeeping.** Without it, "the blazer
changed colour" and "the lighting changed the apparent shade" are the same observation, and both
the human and the instrument are being asked an undecidable question. SPEC-01 defines both fields;
`CAPABILITY-LAB-V0-PLAN.md`'s ladder referenced only the first.

**Acceptance thresholds (proposed).**

| Measure | Threshold |
|---|---|
| False-pass rate (identity drifted, judged held) | ≤ 5% |
| False-fail rate | ≤ 15% |
| Per-invariant agreement with human | ≥ 0.80 |
| Inter-annotator agreement | reported; instrument threshold may not exceed it |

DreamBench++'s 83.31% is the reference point for what is achievable with a well-structured
multimodal judge on this exact task class. Ours is a stricter per-invariant binary rather than
their graded 0–4 scale, so the numbers are not directly comparable and theirs is not adopted.

**Human time estimate.** ~20 items × 2 annotators × ~5 min (a set, not an image), plus rubric
drafting and adjudication: **≈ 5–6 hours**. The largest human cost in V0.

**Re-calibration triggers.** Instrument version change; a new entity type (product vs person are
different problems); a new invariant vocabulary term.

---

### 3.4 · I4 — Object detector (D4)

**Instrument.** Object detector plus rule-based geometric predicates — the GenEval protocol.

**Current state: `published_calibration_only`.** GenEval reports **83% agreement with annotators
against 88% inter-annotator agreement**, rising to **91% on images annotators unanimously agree
on**, using Mask2Former (Swin-S, COCO instance segmentation) at confidence 0.3, and 0.9 for
counting.

**Why that is not sufficient on its own.** Those figures were measured on *their* material.
GenEval's authors record that the detector is confined to MS COCO's 80 classes, produces merged
bounding boxes for overlapping same-class objects, mis-segments objects with holes, and degrades
on out-of-distribution imagery such as clip art. Commercial creative — studio lighting, shallow
depth of field, branded packaging, graphic overlays — is closer to that out-of-distribution
regime than to COCO photographs.

**Local confirmation required (cheap).** ~20 items from our own material, hand-labelled for count
and spatial relation, agreement measured against the detector. Threshold: **≥ 0.80 agreement**;
below that, D4 is restricted further or moved to `required_but_no_calibrated_instrument`.

**Scope restriction already applied in the battery.** V0 D4 covers only COCO-representable
generic objects. Brand marks are deferred — reporting a COCO-class result as covering wordmarks
would be precisely the over-claim this plan exists to prevent.

**Human time estimate.** ≈ 1.5–2 hours, non-specialist.

**Re-calibration triggers.** Detector or threshold change; a new object class outside COCO; a
visual style materially unlike the confirmation set.

---

### 3.5 · I5 — Operational logging (D6)

**Instrument.** Deterministic capture of latency, HTTP status class, moderation response, posted
price on the run date, and repeat agreement.

**Calibration:** none required — `deterministic`.

**One requirement that is not automatic.** Price must be read from the provider's page **on the
run date** and stored with the entry (`cost.price_source`, `cost.price_read_date`). Provider
prices move, and a cost-per-pass computed against a stale rate is wrong in a way nothing
downstream can detect.

---

## 4 · Threshold summary

| Instrument | Dimension | State today | False-pass bar | Human hours |
|---|---|---|---|---:|
| I1 Devanagari transcription | D1, D5 L2+ | `provisional_uncalibrated` | **0 in 30** + outlier screen | 2–4 (native reader) — depends on M1a licensing |
| I2 Latin transcription | D2, D5 L1 | `requires_calibration` | 0 in 30 | 1–1.5 |
| I3 Identity judge | D3 | `requires_calibration` | ≤ 5% | 5–6 |
| I4 Object detector | D4 | `published_calibration_only` | — (≥0.80 agreement) | 1.5–2 |
| I5 Operational logging | D6 | `deterministic` | n/a | 0 |
| *(none)* | logo fidelity, human-object interaction | `required_but_no_calibrated_instrument` | n/a | n/a |

**Total human calibration time: ≈ 11–14 hours**, of which **3–4 must be a Hindi first-language
reader**. This is one-off setup, not per-run.

---

## 5 · What blocks a run today

1. **I1 has no native-speaker ground truth.** D1 and D5 levels 2+ cannot produce Registry entries.
   Requires a Hindi first-language reader plus M1b (must be built) and, ideally, M1a (reusable only
   once Resources verifies licensing).
2. **I3 has no frozen rubric and no reference sets.** M3 needs rights clearance from Resources.
3. **Human calibration time is unbudgeted.** ~11–14 hours is not currently approved anywhere.
4. **I4's local confirmation set does not exist.** Cheapest of the four to unblock.

**None of these blocked EVAL-001**, because EVAL-001's deliverable is the specification. They
block the *run*, which is a separate approval.

---

## 6 · Standing rules

1. **Calibrate before measuring.** No Registry entry from an instrument whose
   `calibration_status` is `provisional_uncalibrated` or
   `required_but_no_calibrated_instrument`.
2. **Re-calibrate on version change.** A changed instrument is a new instrument.
3. **Never change an evaluator prompt and report the rerun as the same experiment.** Autonomy
   Policy stop condition 8. If the prompt changes, the run is frozen as evidence and a new run
   record is opened.
4. **Store gate and diagnostic accuracy separately.** They are different capabilities of the
   instrument and serve different consumers.
5. **You cannot beat your ground truth.** An instrument threshold may never exceed the measured
   inter-annotator agreement on the same material.
6. **Blind the human.** Ground-truth readers see the image and not the target string. The
   auto-correction pull that broke the model checker acts on people too.
