# EVAL-001 — Battery design findings

**Date:** 24 Aug 2026 · **Cost:** ₹0 · **Generations:** zero · **Models benchmarked:** none

What the published-benchmark review actually established, what it did not, and what auditing our
own material turned up. Per Controller clarification 12, nothing historical was modified to fit
the new design; problems are recorded here and the affected claims are downgraded in the drafts.

---

## 1 · Headline: there is no Devanagari text-rendering benchmark

`resources/corpus/CORPUS-SOURCING-PLAN.md` §D flagged this as a "critical unknown." **Answer as of
24 Aug 2026: no public text-rendering or text-editing benchmark covers Devanagari or Hindi.**

The 2025–26 literature is concentrated on English and Chinese. CVTG-2K probes multi-region English
rendering; ChineseWord targets Chinese characters; TextAtlasEval and LongText-Bench are English
and Chinese. None covers Indic scripts.

The nearest published work is **MULTITEXTEDIT** (May 2026), a controlled 3,600-instance benchmark
across 12 typologically diverse languages. Its full language list, read from the paper's Table 4:
English, Hebrew, Arabic, **Bengali**, Korean, Russian, Vietnamese, Yoruba, Japanese, Chinese,
Spanish, Dutch. **No Devanagari.**

**Bengali is the closest available proxy** — a Brahmic abugida with conjuncts and a headline
stroke, structurally the nearest thing to Devanagari in any published benchmark — and it is the
**third-worst-performing language in the study**, behind only Hebrew and Arabic:

| Language | ∆Sem vs English | ∆Text accuracy | ∆Script fidelity |
|---|---:|---:|---:|
| Hebrew | 0.856 | 1.168 | 1.551 |
| Arabic | 0.780 | 1.005 | 1.258 |
| **Bengali** | **0.697** | **0.960** | **1.172** |
| Korean | 0.543 | 0.717 | 0.911 |
| Chinese | 0.304 | 0.363 | — |
| Spanish | 0.184 | 0.234 | — |

**What this licenses.** Borrowing the *method*. **What it does not license:** inferring a
Devanagari number from a Bengali one. Bengali's poor showing is corroborating context for our own
observed Devanagari failures — not a substitute measurement, and not a Registry entry.

Two consequences. First, the Devanagari instrument must be calibrated locally against
native-speaker ground truth; there is nowhere to borrow it from. Second, the corpus plan's
judgement that this gap is "the single highest-value gap in this document" is **supported by the
review**, and the required string set (media requirement M1) currently has no owner.

---

## 2 · Convergent design: our checker protocol was independently reinvented

FINDINGS-01 designed its checker to **transcribe rather than confirm** — *"do not correct
spelling, do not guess what it was meant to say"* — reasoning that an agreeable model asked to
confirm will simply say yes.

MULTITEXTEDIT arrived at structurally the same protocol independently. Its language/script
fidelity metric is scored by a **two-stage protocol that first traces the edited target text and
then judges it in isolation**, and it reports a quadratic-weighted κ of **0.76** against
native-speaker annotators.

Two useful things follow. The trace-then-judge design is not an idiosyncratic choice of ours; it
is what a peer-reviewed team building the same instrument in the same year also concluded. And
their κ of 0.76 gives a published sanity anchor for what this class of instrument achieves —
**not** a threshold we may adopt, since theirs is a graded score across 12 languages and ours is a
binary gate on one script.

---

## 3 · Published methodology adopted, and where it was declined

| Borrowed | From | Applied to |
|---|---|---|
| Object-detector + rule-based geometry for count and position | GenEval | D4 instrument |
| Detector confidence as a *recorded condition*, not a default | GenEval (0.3 general, 0.9 counting) | Registry `conditions.detector_confidence` |
| Instrument agreement reported against **inter-annotator** agreement | GenEval (83% vs 88%) | calibration rule "you cannot beat your ground truth" |
| Separating compositional capability into attribute binding / relationships / numeracy / complex | T2I-CompBench++ | splitting the plan's merged "composition placement and count" |
| Hierarchical, *disentangled* dimensions each with its own tailored prompts **and** its own evaluation method | VBench | the whole per-dimension structure of §6 |
| Human annotation collected **one dimension at a time**, annotator instructed to attend to that dimension only | VBench | calibration protocol |
| Per-language delta against a baseline language as the headline quantity | MULTITEXTEDIT | D2 Latin control |
| Two-stage trace-then-judge for script fidelity | MULTITEXTEDIT | D1 instrument (convergent, see §2) |
| Text fidelity **and** temporal consistency as separate results for on-screen text in video | T2VTextBench | D5's two independent results |
| pass@k, expected attempts under a retry cap, effective cost per success including human review | HYPE-EDIT-1 | cost model, and the missing cost fields |
| Public / private held-out task split | HYPE-EDIT-1 (50/50) | recorded as a **V1** candidate; we have too few items to split |

**Declined, with reasons:**

- **CLIPScore** — holistic; cannot say *which* constraint failed. GenEval's own motivation.
- **DINO / CLIP-I similarity for identity** — 50.72% human alignment on concept preservation
  (DreamBench++) against 83.31% for a structured multimodal judge, and the paper's conclusion that
  DINO "prioritize[s] overall shape and color over detailed features." Our invariants *are*
  detailed features.
- **TIFA's VQA question-generation** — genuinely good fit for later acceptance-contract checking,
  but the answering step is an uncalibrated model judgement. V1 candidate, not a V0 instrument.
- **VBench's aesthetic/imaging quality (LAION predictor, MUSIQ)** — B-side, deferred by
  clarification 2.
- **AVA / Pick-a-Pic / HPDv2** — B-side; and per the corpus plan, contest and preference
  aesthetics are not commercial effectiveness (Ogilvy's opening argument, and ASSUMPTIONS §13).
- **VBench's `subject_consistency`** — implemented as DINO across frames, inheriting the same
  limitation.

---

## 4 · Published support for two things we had only observed locally

**Text instability in generated video is real, general and published.** T2VTextBench (May 2025) is
dedicated to on-screen text fidelity *and temporal consistency* in text-to-video. Across 10
systems including Sora, Kling, Wan 2.1 and Pika 2.2, **every model scored below 0.4** on a 0–1
scale, best 0.37, with the authors reporting substantial gaps in temporal text consistency. Our
Wan clip's within-clip drift (सुवह की in frames 1–4, सुवह के in frames 5–6) is an instance of a
documented general failure, not a one-off artefact.

**Cost per accepted outcome has published precedent.** HYPE-EDIT-1 (Jan 2026) generates 10
independent outputs per task across 100 reference-based marketing/design edit tasks, judges binary
pass/fail, computes pass@k and expected attempts under a retry cap, and reports an effective cost
per success that combines model price **with human review time**. Its stated conclusion: models
with low per-image pricing are more expensive once retries and human review are counted.

This is independent external support for the project's primary metric — and a correction to our
own schema. **Their cost includes human review; ours did not.** ASSUMPTIONS §12 already recorded
that CpAO omits the intelligence layer's own cost. The battery's §8.3 arithmetic makes the size of
the omission concrete: at realistic verification rates, **generation is 2–4% of a cell's cost and
human verification is the overwhelming majority.**

---

## 5 · Provenance and integrity problems in our own material

Recorded here per clarification 12. **Nothing was modified.** Affected claims are downgraded in
the drafts rather than repaired in place.

**5.1 · Devanagari ground truth is unconfirmed.** FINDINGS-01 states it directly: *"neither
reader's first language is Hindi. A Hindi reader should confirm the labels before this is
quoted."* `eval/HANDOFF.md` reports the result correctly qualified as "14/14 correct verdicts", but
neither it nor `CAPABILITY-LAB-V0-PLAN.md` carries forward the caveat that the labels are
unconfirmed, and both rely on the result. No record of confirmation exists.
**Downgraded** to `provisional_uncalibrated` throughout the drafts.

**5.2 · "14/14" conflates two accuracies.** FINDINGS-01 is precise — *"14/14 correct verdicts"* —
and records in the same file that Qwen *"caught सुबह→सुवह but silently corrected चाथ→चाय. Verdict
right, diagnosis incomplete."* The risk is that the two get conflated downstream, since a bare
"14/14" reads as a general accuracy claim. Verified against the
raw run file: Qwen's transcription of `frame_wan_1`–`4` is सुवह की पहली चा**य** (edit distance 1),
while FINDINGS-01's stated ground truth is सुवह की पहली चा**थ** — two substitutions, one caught.
**Consequence:** the Registry schema now carries `instrument.role: gate | diagnosis` so the two
are stored separately.

**5.3 · Three run artifacts are entirely API errors.** In
`eval/runs/finding-01-devanagari-check/`: `vlm_google-gemini-2-5-pro.json` is 14/14 HTTP 422
("requires reasoning to be enabled"); `vlm_openai-gpt-5-chat.json` is 14/14 HTTP 400/404 ("no
endpoints found"); `vlm-transcriptions.json` is 14/14 HTTP 422 (invalid model literal). FINDINGS-01
correctly reports a three-checker study and does not claim these. **No correction to the finding is
needed** — but the directory contains five result files, and a reader could reasonably infer a
larger comparison than took place. Recorded, not deleted.

**5.4 · The Tesseract claim has no artifact.** FINDINGS-01 reports `tesseract (hin) 0/14 —
unreadable output`. No supporting file exists in the repository. The claim is consistent with the
published difficulty of Devanagari OCR and with §1's finding that no Devanagari benchmark exists,
but it is **not currently reproducible from committed evidence**. Carried as *unverified* in the
calibration plan, and explicitly not used to justify I1's cost.

**5.5 · The one working script cannot be run as committed.** `eval/scripts/check-vlm.mjs` hardcodes
`ROOT = "/Users/vaibhavchawla/Vaibhav_Personal_Projects/aight-eval"`, which does not exist on this
machine; the samples now live at `resources/corpus/finding-01-samples/`. FINDINGS-01 requires a
checker to be re-measured when its version changes — as committed, that re-measurement is
impossible without editing the instrument, and editing the instrument breaks comparability with the
original calibration. **Not fixed here** (clarification 12); recorded as a prerequisite for any
approved run.

**5.6 · Sample correlation.** 14 samples, **4 independent sources**, 12 correlated frames from 4
clips. FINDINGS-01 states this under its own limits. Any arithmetic treating frames as independent
trials overstates confidence roughly threefold. **Consequence:** the battery defines item / trial /
repeat / observation (§5.4) and the Registry requires `n_items` alongside `trials`.

**5.7 · Broken internal references.** `CAPABILITY-LAB-V0-PLAN.md` links `EVAL-CORPUS-PLAN.md`,
which does not exist; the document it means is `resources/corpus/CORPUS-SOURCING-PLAN.md`, now
owned by Resources. `coordination/ASSUMPTIONS.md` links `CANON-EXPERIMENT-V0.md` and
`CAPABILITY-LAB-V0-PLAN.md` as if siblings in `coordination/`. `coordination/DECISION-LOG.md` cites
`ASSUMPTIONS-AND-FALSIFICATION.md`, since renamed. Cosmetic individually; collectively they are the
citation trail under the falsification register. **Not edited** — outside Eval's ownership.

**5.8 · Regression corpus is out of reach and single-labelled.**
`CAPABILITY-LAB-V0-PLAN.md` cites `spike/out/scores.json`; no such path exists in this repository.
It exists in the separate `media-factory` project, and reading it read-only confirms the cited
counts exactly: 64 records, 10 failures, nano 7/32, seedream 3/32. Per clarification 6 it was
**not copied and not re-scored**. Two dependencies recorded: the media is unreachable from where
the battery lives, and every record carries a single free-text label, which FINDINGS-11
§Co-occurrence already proved lossy (`seedream_sign_t1` carries a second, unrecorded defect).
**Consequence:** Registry `result.failed_trials` permits multiple defects per trial, per Project
Contract separation 13.

---

## 6 · Design corrections to `CAPABILITY-LAB-V0-PLAN.md`

Proposed, not applied to that file.

| # | Issue | Proposed correction |
|---|---|---|
| 1 | `3 × 4 × 3 × 20 ≈ 720` treats operational behaviour as a generating dimension | D6 is a by-product; costs zero additional generations |
| 2 | The same figure assumes full crossing | Image workflows cannot exhibit within-clip drift; video workflows cannot be tested on across-prompt identity. The design is ragged, not a cube |
| 3 | "Wan / Veo" as one workflow row | Separate entries. The Registry keys on vendor+model+version (clarification 5) |
| 4 | "20 trials" undefined | item / trial / repeat / observation defined; correlation rule binding |
| 5 | Difficulty levels named but not defined | Level N+1 = level N plus exactly one named, independently observable stressor |
| 6 | "Composition placement and count" merges two dimensions with two ladders | Both GenEval and T2I-CompBench++ separate them, and they need different instruments |
| 7 | Identity ladder cites `invariants` only | `allowed_variation` is mandatory, or the criterion is undecidable |
| 8 | `audience.language` cited for on-screen Devanagari | Wrong field. SPEC-01 splits language four ways; on-screen script is `audience.language.on_screen_copy` + `copy.script_system`. `spoken` is a different capability |
| 9 | `static.*` / `video.*` path shorthands | Not SPEC-01 paths. Correct references are `StaticCreativeExtension.*` / `VideoCreativeExtension.*` |
| 10 | `usd_per_pass` undefined at zero passes | `null` + `usd_per_pass_lower_bound`; never infinity |
| 11 | `failure_types: [{term, n}]` cannot express co-occurrence | `failed_trials[].defects[]`; counts become a derived view |
| 12 | No cost of evaluation or repair | `usd_per_evaluation`, `usd_human_verification_per_trial`, `usd_per_repair_attempt` |
| 13 | No state for "matters, cannot measure" | `required_but_no_calibrated_instrument`, mirroring SPEC-01's `verification.mode: unresolved` |

---

## 7 · Source record

Per clarification 11. All accessed **24 Aug 2026**. No paid access was used.

| Source | Identifier / venue | Version | Borrowed | Rejected |
|---|---|---|---|---|
| **GenEval: An Object-Focused Framework for Evaluating Text-to-Image Alignment** | arXiv:2310.11513 · NeurIPS 2023 D&B | published | 6-task taxonomy (single object 80 / two object 99 / counting 80 / colors 94 / position 100 / attribute binding 100 = 553 prompts, 4 images each); Mask2Former Swin-S COCO detector, conf 0.3 and 0.9 for counting; CLIP ViT-L/14 colour classifier; 83% vs 88% inter-annotator, 91% unanimous | its 80-class COCO ceiling for brand marks |
| **T2I-CompBench++** | arXiv:2307.06350 · TPAMI 2025 | ++ | 4 groups / 8 sub-categories (attribute binding: colour, shape, texture; relationships: 2D/3D-spatial, non-spatial; numeracy; complex) | MLLM-as-metric (GPT-4V / ShareGPT4V) — uncalibrated model judgement for V0 |
| **VBench / VBench++** | arXiv:2311.17982 · CVPR 2024 / arXiv:2411.13503 | v1 / ++ | disentangled per-dimension design; per-dimension instruments (DINO, CLIP, MAE, AMT, RAFT, LAION aesthetic, MUSIQ, GRiT, UMT, Tag2Text, ViCLIP); ~100 prompts/dimension, 800 across 8 content categories; single-dimension pairwise human annotation, 5 groups of 4 videos per prompt | aesthetic/imaging quality (B-side); `subject_consistency` (DINO-based) |
| **TIFA** | arXiv:2303.11897 · ICCV 2023 | v1.0 | question-generation-from-prompt as a later acceptance-contract method (4,081 inputs, 25,829 QA pairs, 12 categories) | VQA answering as a V0 instrument — uncalibrated |
| **DreamBench++** | arXiv:2406.16855 | v2 | structured per-attribute multimodal judging for identity (150 concepts, 1,350 prompts, 0–4 scale); alignment evidence: concept preservation GPT 83.31% vs DINO 50.72%; prompt following GPT 98.17% vs CLIP-T 61.48% | DINO / CLIP-I as identity instruments |
| **MULTITEXTEDIT** | arXiv:2605.08163v2 · 18 May 2026 | v2 | two-stage trace-then-judge script-fidelity protocol; κ 0.76 vs native speakers; per-language delta-vs-English design; 12-language coverage table | its scores; Bengali as a Devanagari proxy |
| **T2VTextBench** | arXiv:2505.04946 · 8 May 2025 | v1 | text fidelity and temporal consistency as separate results (73 prompts, 6 categories, 10 systems, 3 annotators, 0/0.25/0.5/1 scale; all models <0.4, best 0.37) | its Chinese-only multilingual category |
| **HYPE-EDIT-1** | arXiv:2602.00105 · 25 Jan 2026 · Chan & Allen | v1 | pass@k with retry cap; effective cost per success including human review time; 10 outputs per task; binary pass/fail; 50 public / 50 private split (noted as V1) | its task set (marketing edits, but not our constraints) |
| **fal.ai public pricing page** | https://fal.ai/pricing | accessed 24 Aug 2026 | Seedream V4 $0.03/image; Nano Banana $0.0398/image; Wan 2.5 $0.05/s; Veo 3 $0.40/s, normalised to 1MP | ⚠️ Nano Banana **Pro** priced separately and **not confirmed** on the vendor page; the plan's observed ~$0.15 corresponds to the Pro variant |

Also surveyed and found not to cover Devanagari: CVTG-2K, ChineseWord, TextAtlasEval,
LongText-Bench, MARIO-Eval, AnyText / AnyWord-3M.

---

## 8 · Assumptions touched

No assumption was promoted or demoted; EVAL-001 produced no experimental result. Three are
**informed** and their register entries may warrant a Controller-made note.

- **§12 (CpAO adequacy).** Independent external support from HYPE-EDIT-1 for the *shape* of the
  metric, and independent confirmation of the register's own stated weakness — the intelligence
  layer's cost was missing. The battery quantifies it: human verification dominates generation
  cost by more than an order of magnitude.
- **§4 (book knowledge ↔ empirical failure).** The observation-unit channel held up under a
  second, external test: T2VTextBench independently measures the temporal text consistency that
  `gos_005` predicted an evaluator would need. Book knowledge shaped the instrument; a published
  benchmark independently built that instrument. Not a new result — a second instance of the one
  FINDINGS-11 already recorded.
- **§15 (Canon-derived requirements improve routing).** Still blocked on a Registry, and V0 as
  scoped is A-side only, so it stays untestable after this battery runs. Stated so the block is
  not mistaken for progress.

---

## 9 · What this task did not establish

- No capability of any model was measured. Zero generations.
- No instrument was calibrated. The Devanagari checker remains preliminary.
- No Registry entry exists.
- Nothing about creative fitness. V0 is A-side by decision, not by finding.
- Nothing about whether the four V0 dimensions are the *right* four. They are the traceable,
  affordable four. Coverage is not claimed.
