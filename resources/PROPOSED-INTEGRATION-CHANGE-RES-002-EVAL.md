# Cross-stream note to Eval — Devanagari calibration material is now available

**From:** Resources (RES-002) · **To:** Eval · **Date:** 24 Aug 2026
**Status:** PROPOSED — a notification of available material, not a change to Eval's design.
Resources does not define what Eval measures.

## What changed for you

RES-001 explicitly could **not** unblock your Hindi-text checker: the corpus contained no Devanagari
material at all. That gap is now closed.

**29,722 real photographed Devanagari word/scene images with human transcriptions**, from three
independent collections:

| Source | Images | Ground truth | Why it is separate |
|---|---:|---|---|
| `src_bstd_devanagari` | 25,246 | JSON: filename → Unicode transcription | Largest; 2020s collection |
| `src_indicstr12_devanagari` | 3,086 | per-image `*_gt.txt` Unicode labels | Different collectors and conditions |
| `src_iiit_ilst_devanagari` | 1,390 | per-image XML: boxes + transcriptions | Oldest (2017); different annotation format |

All are photographs of real signage — genuinely degraded text with blur, angle, lighting variation
and occlusion — not clean synthetic renders. RES-002 specifically required this: published evidence
suggests clean synthetic text may not distinguish a strong reader from a weak one.

## What this material is for, and what it is not

**It tests whether a candidate evaluator can READ Devanagari at all.** That is a prerequisite
question. If a model cannot reliably read Devanagari from a photograph, its verdicts about generated
Hindi text are not worth anything, and no amount of careful rubric design fixes that.

**It is not a test of generated Hindi text.** These are photographs of real-world signs, not model
outputs. It answers "can this judge read the script?", not "did the generator render the script
correctly?".

**The transcriptions are candidate calibration material, not project ground truth.** They are other
people's annotations, made for their purposes. Standing rule from the Project Contract: external
labels are one source's observations. Treating them as truth needs your validation and, per RES-002,
a human Hindi reader — which Resources has explicitly not done.

## Two findings that affect how you use it

**1. Language labels are not script labels.** In BSTD, 5,109 images labelled `marathi` are written
in Devanagari, and a further 351 labelled as other languages also contain Devanagari text. Filtering
by language would have missed roughly a fifth of the usable material. **If you subset this pool,
filter on the script in the transcription, not on the language field.**

**2. Three collections, on purpose.** A checker evaluated against a single collection's photography
can look better than it is, because it has only met one set of cameras, fonts and lighting
conditions. Holding one collection back as an unseen test is possible with three, and was not with
one. How to use that is your call.

## Also newly available

`src_videogen_rewardbench` — 288 generated videos spanning **12 different text-to-video generators**,
with human pairwise preference labels. RES-001 marked this unobtainable; RES-002 acquired it. Useful
if you want to test whether an evaluator behaves consistently across generator styles rather than
being tuned to one model's look.

## Still missing

No Devanagari **generated** text, and no Devanagari text in **video**. Our own observed failure —
Devanagari corruption that drifts within a single clip — has no public counterpart in this material.
That would have to be produced, which means generation spend and is outside both RES-002 and
EVAL-001.

## Asked of Eval

Nothing is required. If this changes what EVAL-002 treats as blocked, say so and Resources will
record the dependency. **Resources proposes; the Controller decides.**
