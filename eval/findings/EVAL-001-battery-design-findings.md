# EVAL-001 — Battery design findings

**Date:** 24 Aug 2026 · **Cost:** ₹0 · **Generations:** zero · **Models benchmarked:** none

What the published-benchmark review actually established, what it did not, and what auditing our
own material turned up. Per Controller clarification 12, nothing historical was modified to fit
the new design; problems are recorded here and the affected claims are downgraded in the drafts.

---

## 1 · Headline: no benchmark measures *generative* Devanagari text rendering

**⚠️ This section was narrowed on 24 Aug 2026 after Controller review.** The first version of this
finding claimed "no public benchmark covers Devanagari or Hindi text rendering." **That claim was
too broad and is withdrawn.** Devanagari benchmarks exist; they measure a different task.

### 1.1 What exists — Devanagari *recognition*

Public Devanagari benchmarks exist and several are recent and substantial:

| Resource | Identifier | What it measures |
|---|---|---|
| **Can OCR-VLMs Read Devanagari? A Stress-Test Benchmark and Post-Correction Study** | arXiv:2606.29213v1, 28 Jun 2026, A. P. Singh | 10 OCR/VLM systems reading Devanagari; 4 synthetic degradation conditions + 300 real printed scans; chrF++ |
| Benchmarking Scene Text Recognition in Devanagari, Telugu and Malayalam (IIIT-ILST) | arXiv:2104.04437 | scene-text recognition, 3 Indic scripts |
| IndicSTR12 | CVIT IIIT-H, 2023 | Indic scene-text recognition, 12 scripts |
| Bharat Scene Text Dataset (BSTD) | arXiv:2511.23071 · IJDAR | >100K words, 11 Indian languages + English, 6,582 scene images |
| IndicVisionBench | arXiv:2511.04727 | OCR track: 876 document images, 10 Indic languages |
| MLT-17 / MLT-19 | ICDAR | multilingual scene text incl. Indic |
| DohaScript | arXiv:2602.18089 | continuous handwritten Hindi |

**All of these measure recognition: given an image containing Devanagari, read it correctly.**

### 1.2 The narrowed claim, re-checked and still supported

> **OBSERVED (as of 24 Aug 2026): no public benchmark measures whether a generative image or video
> model correctly renders Devanagari text it was instructed to produce.**

The generative text-rendering benchmarks are English and Chinese: CVTG-2K, MARIO-Eval, AnyText /
AnyWord-3M, TextAtlasEval, LongText-Bench, ChineseWord, and OneIG-Bench's Text Rendering dimension
(EN/ZH). MULTITEXTEDIT, the broadest multilingual text-in-image *editing* benchmark, covers 12
languages including Bengali but not Devanagari (§1.4).

**Why the distinction is load-bearing, not pedantic.** Reading and drawing are different
capabilities measured on different objects. An OCR benchmark tells you how well a model *reads*
Devanagari; it says nothing about whether a diffusion model can *draw* it. Our observed failures —
`still_seedream_headline` (gibberish), `frame_wan_*` (character substitution) — are drawing
failures. No public benchmark scores them.

**RESOLVED 24 Aug 2026 — OneIG-Bench does not affect the claim.** The earlier draft left this open.
Checked against the **released public dataset** rather than the paper prose:

| Evidence from the released files | Value |
|---|---|
| Configs published | exactly two: `OneIG-Bench` (English) and `OneIG-Bench-ZH` (Chinese) |
| Rows, English config | **1,120** — categories Anime_Stylization, Portrait, General Object, Text Rendering, Knowledge and Reasoning. **No Multilingualism category at all.** |
| Rows, Chinese config | **1,320** — the same five categories plus 200 rows in category `Multilingualism` |
| Sampled `Multilingualism` rows (6 inspected, offsets 1150–1155) | Simplified Chinese prompts about Chinese cultural subjects — the boxer Zou Shiming, actress Liu Shishi, magician Liu Qian, esports player Uzi, the Chinese women's curling team, actor Wallace Huo |

**"Multilingualism" in OneIG-Bench does not mean many scripts.** It is the Chinese-language,
Chinese-culture prompt set — consistent with the paper's own description of it as "100
culture-related prompts and 100 portrait-related prompts," and with its text-rendering score using
a constant φ defined only for English (100) and Chinese (50).

**What this establishes, and its limits.** The *structural* evidence is decisive: only two configs
exist, the category is absent from the English config entirely, and there is no config in any third
script. **No Devanagari, no Indic script.** The *content* evidence is a sample — 6 of 200 rows — so
I do not claim to have read every prompt, and nothing here is inferred beyond what the released
files show. The claim in §1.2 stands unchanged.

### 1.3 What the recognition benchmarks give us instead — and it is a lot

They do not measure our generators. They **do** measure our *instrument*, because our instrument is
an OCR-VLM reading generated images. arXiv:2606.29213 is therefore directly useful, and it changes
the calibration design (see `INSTRUMENT-CALIBRATION-PLAN-V0.md` §3.1):

1. **Clean synthetic renders do not discriminate between checkers.** All ten systems cluster within
   **chrF++ 91–98** on clean rendered text. A calibration set built only from clean renders would
   make every candidate look equally good and tell us nothing. **This is a direct correction to our
   first calibration sample design.**
2. **Degraded and real material separates them sharply.** On real scans nine of ten systems
   collapse, across a **76-point range**: Gemini 2.5 Flash 86.3, Qwen3-VL-8B 75.2, GPT-5.5 58.5.
3. **"Strong English OCR does not predict Indic OCR."** Two consequences: it independently supports
   our D2 Latin-control design, and it forbids selecting the Devanagari checker on Latin
   performance.
4. **A named instrument failure mode.** DeepSeek-OCR produced rare but catastrophic repetition
   failures — outputs reported up to 71× the reference length — wrecking its corpus mean while its
   median was the best of any system. Our calibration must screen for catastrophic outliers, not
   only mean agreement.
5. **A graded diagnostic metric.** chrF++ alongside our binary gate, matching the gate-vs-diagnosis
   split we already require.

**Caveat on transferring finding 2 to us.** Those figures come from *printed scans* and synthetic
degradations. Generated-image text is a third regime: often clean-looking but semantically wrong.
Whether checker rankings transfer is **NOT VERIFIED** and is exactly what local calibration exists
to establish.

### 1.4 Bengali as the nearest published *generative* proxy

Within MULTITEXTEDIT (12 languages, text-in-image editing), Bengali — Brahmic, with conjuncts and a
headline stroke, structurally nearest to Devanagari — is the third-worst performer:

| Language | ∆Sem vs English | ∆Text accuracy | ∆Script fidelity |
|---|---:|---:|---:|
| Hebrew | 0.856 | 1.168 | 1.551 |
| Arabic | 0.780 | 1.005 | 1.258 |
| **Bengali** | **0.697** | **0.960** | **1.172** |
| Korean | 0.543 | 0.717 | 0.911 |
| Chinese | 0.304 | 0.363 | — |
| Spanish | 0.184 | 0.234 | — |

Corroborating context for our observed Devanagari failures. **Not** a substitute measurement, and
not a Registry entry.

### 1.5 Net effect on the plan

The gap is **narrower and cheaper to close** than the first version of this finding implied.

- **Instrument calibration material** can partly be reused from existing Devanagari OCR/scene-text
  resources, subject to Resources clearing the material for bounded internal evaluation under the
  current Resources policy.
- **Capability items** — prompt/target-string pairs to feed generators — still have to be built,
  because no public resource contains them.

Revised media requirement M1 is in the battery draft §9.

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

**Text instability in generated video is real, general and published.** **T2VTextBench
arXiv:2505.04946v1 (8 May 2025 — the only version; all figures below are v1 and none are mixed
with any other release).** It is dedicated to on-screen text fidelity *and* temporal consistency
in text-to-video: 73 prompts across six categories, 10 systems including Sora, Kling, Wan 2.1 and
Pika 2.2, three human annotators on a 0 / 0.25 / 0.5 / 1 scale. v1 states *"the highest average
score is reported for Sora, which is only 0.37"*, and concludes *"all models exhibit noticeable
failures in generating videos with textual content"* — i.e. **every evaluated model below 0.4**.
Our Wan clip's within-clip drift (सुवह की in frames 1–4, सुवह के in frames 5–6) is an instance of a
documented general failure, not a one-off artefact.

**Cost per accepted outcome has published precedent.** HYPE-EDIT-1 (Jan 2026) generates 10
independent outputs per task across 100 reference-based marketing/design edit tasks, judges binary
pass/fail, computes pass@k and expected attempts under a retry cap, and reports an effective cost
per success that combines model price **with human review time**. Its stated conclusion: models
with low per-image pricing are more expensive once retries and human review are counted.

This is independent external support for the project's primary metric — and a correction to our
own schema. **Their cost includes human review; ours did not.** ASSUMPTIONS §12 already recorded
that CpAO omits the intelligence layer's own cost.

**Supported conclusion:** human verification can materially dominate total cost and must be
included in the cost model.

⚠️ **The specific ratio is an illustrative scenario, not a finding.** Battery §8.3 works one
scenario in which generation is ~2–4% of a cell's cost. That arithmetic depends entirely on
assumptions **none of which is approved or measured**: a human verification rate of 20% of trials,
a human cost of $6.00 per verified trial (≈15 min at a nominal ₹2,000/hr), and a $0.03 image price.
Halve the verification rate or the hourly rate and the ratio changes by a factor of four. The
scenario shows the *shape* of the cost — that a term we had omitted can be the largest one — and
nothing more precise than that.

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

**5.4 · The Tesseract claim has no artifact — and the external picture is now more nuanced.**
FINDINGS-01 reports `tesseract (hin) 0/14 — unreadable output`. No supporting file exists in the
repository, so the claim is **not reproducible from committed evidence** and is carried as
*unverified*.

Published evidence does not straightforwardly endorse it either. arXiv:2606.29213v1 includes
EasyOCR — a classical OCR engine, not a VLM — among ten systems, and reports **all ten clustering
at chrF++ 91–98 on clean rendered Devanagari**. That does not vindicate Tesseract specifically
(different engine, different material, and our samples were generated-image text rather than clean
renders), but it does mean "classical OCR simply cannot read Devanagari" is **too strong a
generalisation to carry forward unexamined**. What the published data does support is that
performance collapses on degraded and real-world material.

Practical consequence: the possibility of a cheap deterministic second opinion for Devanagari
should be **re-tested**, not written off on an unreproducible line. Recorded as an open check;
I1's cost is not justified by this claim either way.

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

**5.9 · V0 calibration sample sizes cannot support error-rate claims.** Added 24 Aug 2026 at
Controller direction. The thresholds first drafted ("0 false passes in 30", "≤5% false-pass for
identity") read as error-rate statements but are qualification gates. A false pass can only occur on
an item whose ground truth is broken, so the denominator is the broken half: 30 items at 50:50 gives
**~15 opportunities**, and zero observed there is consistent with a true rate **up to ~18%** (95%
one-sided bound, `1 − 0.05^(1/n)`). For identity at ~20 items and ~50% drift there are ~10
opportunities, so a **≤5% threshold is not estimable at all** — the finest observable resolution is
10% — and zero observed is consistent with **up to ~26%**. Supporting a genuine ≤5% claim needs 59
opportunities; ≤1% needs ~299. Restated as gates with published bounds in
`INSTRUMENT-CALIBRATION-PLAN-V0.md` §2b, §3.1 and §3.3. **No Registry entry may describe an
instrument as low-error on V0 evidence.**

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
| 6 | "Composition placement and count" merges two dimensions with two ladders | **Applied 24 Aug 2026 at Controller direction:** split into `object_count` (D4) and `spatial_relationship` (D4b). Both GenEval and T2I-CompBench++ separate them; they fail independently; and they need **different detector confidence settings** (0.9 counting, 0.3 relations), so one dimension could not carry one honest `conditions` block. Shared detector, separate capability results. Image run-shape rises from 12 cells to 15 |
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
| **T2VTextBench** | arXiv:2505.04946**v1** · 8 May 2025 · only version published | **v1 — all figures cited are v1; no cross-version mixing** | text fidelity and temporal consistency as separate results (73 prompts, 6 categories, 10 systems, 3 annotators, 0/0.25/0.5/1 scale; v1: "the highest average score is reported for Sora, which is only 0.37", all models <0.4) | its Chinese-only multilingual category |
| **HYPE-EDIT-1** | arXiv:2602.00105 · 25 Jan 2026 · Chan & Allen | v1 | pass@k with retry cap; effective cost per success including human review time; 10 outputs per task; binary pass/fail; 50 public / 50 private split (noted as V1) | its task set (marketing edits, but not our constraints) |
| **Can OCR-VLMs Read Devanagari? A Stress-Test Benchmark and Post-Correction Study** | arXiv:2606.29213v1 · 28 Jun 2026 · A. P. Singh | v1 | calibration-set design (clean synthetic renders do not discriminate: all 10 systems chrF++ 91–98; real scans spread 76 points); instrument evidence (Gemini 2.5 Flash 86.3, Qwen3-VL-8B 75.2, GPT-5.5 58.5); "strong English OCR does not predict Indic OCR"; catastrophic-repetition screening; chrF++ as graded diagnostic | its scores as our capability numbers — it measures *reading*, not *generation*; licence not verified by Eval |
| **OneIG-Bench released dataset** | HF `OneIG-Bench/OneIG-Bench`, configs `OneIG-Bench` / `OneIG-Bench-ZH` · NeurIPS 2025 D&B (arXiv:2506.07977) | released files as published, accessed 24 Aug 2026 | resolved the open Multilingualism question from the files themselves: two configs only (EN 1,120 rows, ZH 1,320), `Multilingualism` present only in ZH and Chinese in content (§1.2) | its text-rendering dimension as Devanagari evidence — EN/ZH only |
| Devanagari recognition resources surveyed | IIIT-ILST arXiv:2104.04437 · IndicSTR12 (CVIT 2023) · BSTD arXiv:2511.23071 · IndicVisionBench arXiv:2511.04727 · MLT-17/19 · DohaScript arXiv:2602.18089 | as cited | candidate reusable calibration material for the *reading* instrument, pending Resources clearing the material for bounded internal evaluation under the current Resources policy | as generative-rendering evidence — none measures it |
| **fal.ai public pricing page** | https://fal.ai/pricing | accessed 24 Aug 2026 | Seedream V4 $0.03/image; Nano Banana $0.0398/image; Wan 2.5 $0.05/s; Veo 3 $0.40/s, normalised to 1MP | ⚠️ Nano Banana **Pro** priced separately and **not confirmed** on the vendor page; the plan's observed ~$0.15 corresponds to the Pro variant |

Generative text-rendering benchmarks surveyed and found not to cover Devanagari: CVTG-2K,
ChineseWord, TextAtlasEval, LongText-Bench, MARIO-Eval, AnyText / AnyWord-3M, and OneIG-Bench's
Text Rendering dimension (EN/ZH). **OneIG-Bench's 200-prompt Multilingualism set: language list
NOT VERIFIED** — README does not enumerate it, OpenReview PDF blocked by browser verification.

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

---

## 10 · Revision history

Kept here so the Controller Brief stays short and the audit trail stays complete. **No revision
deleted an earlier claim; withdrawn claims are marked as withdrawn in place.**

### Revision 1 — 24 Aug 2026
Initial deliverables: battery draft, Registry schema, calibration plan, these findings, Controller
Brief.

### Revision 2 — 24 Aug 2026, after first Controller review
Three evidence corrections plus a version pin.

| # | Change | Files |
|---|---|---|
| 1 | **"No public benchmark covers Devanagari" withdrawn as too broad.** Devanagari recognition benchmarks exist and are numerous. Narrowed to: no benchmark measures *generative* Devanagari rendering | findings §1; battery §7.1 |
| 2 | **M1 reassessed and split** into M1a (reusable recognition material) and M1b (capability items). Three design corrections followed from arXiv:2606.29213v1 | battery §9/§9.1; calibration §3.1 |
| 3 | **Cost ratio demoted** from finding to illustrative scenario with its unapproved assumptions named | battery §8.3; findings §4 |
| 4 | **T2VTextBench pinned to arXiv:2505.04946v1**, the only published version; no cross-version mixing | findings §4, §7; battery §6.5 |
| 5 | D2 and D5 recorded as `controller_approved_v0` | battery §6.2, §6.5, §12 |
| 6 | Corrected an inaccurate claim of my own: `eval/HANDOFF.md` does **not** drop the "correct verdicts" qualifier | findings §5.1–5.2; battery §5.2 |

### Revision 3 — 24 Aug 2026, after second Controller review

| # | Change | Files |
|---|---|---|
| 1 | **`object_count_and_spatial_placement` split** into D4 `object_count` and D4b `spatial_relationship`. They fail independently and need different detector confidences (0.9 vs 0.3). Run-shape: image workflows rise from 12 cells / 288 trials to **15 cells / 360 trials** | battery §6.4, new §6.4b, §8.4; findings §6 row 6 |
| 2 | **Calibration thresholds relabelled as qualification gates** with published 95% bounds (~18% text, ~26% identity). **The ≤5% identity threshold is withdrawn as not estimable** at ~10 drifted items | calibration new §2b, §3.1, §3.3; findings new §5.9 |
| 3 | **M1a reuse re-conditioned** on Resources *clearing* material for bounded internal evaluation under `resources/CHARTER.md`; licence silence alone is no longer an automatic block | battery §9/§9.1; calibration §3.1 |
| 4 | **Human hours made consistent** at **≈ 11–15.5 h total, 2–4 h native reader** across calibration §4, battery §9.1 and §12, Handoff and Brief. I4 raised to 2–2.5 h for the two predicates; M1b assembly added at 1–1.5 h | all four files |
| 5 | **M1b narrowed:** the *item set* must be built, but target strings may be sourced from existing permissible Hindi text rather than authored | battery §9/§9.1; calibration §3.1 |
| 6 | **OneIG-Bench resolved from its released dataset** rather than left open. Two configs only; `Multilingualism` exists only in the Chinese config and is Chinese in content. Structural evidence decisive; content evidence is a 6-of-200 sample, not extrapolated | findings §1.2, §7 |
| 7 | D2 and D5 remain approved. Workflow roster, human-time budget and Registry cross-stream architecture remain unapproved/deferred | battery §12; Brief |

**Standing across all revisions:** no benchmark run, no generation call, no money spent, no dataset
acquired, and no historical finding, script or result file altered.
