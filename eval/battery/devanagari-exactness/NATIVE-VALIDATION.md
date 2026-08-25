# Which cases actually need a Hindi speaker — and which do not

**Status: COMPLETE.** One Hindi-competent reviewer worked through the packet with fingerprint
`e1cedf564603a94d` and answered **98 of 98** — 53/53 words, 25/25 perceptibility, 20/20 rendering,
**0 unanswered, 0 UNSURE**.

**Outcome: 5 of 53 base words rejected. Controller decision — PRUNE, DO NOT REBUILD.** 10 items
excluded and not replaced; the authoritative battery is now **96 items · 48 match / 48 mismatch ·
33 hard opportunities on 33 distinct base words · 48 accepted base words · 20/20 classes · 5/5
groups**. The frozen record, raw responses and exclusion decision are in
[`human-validation/`](human-validation/).

This document remains the specification of *what was asked and why*. It is no longer a plan.

---

## The short answer

**One task, roughly 45–75 minutes, once: validate the base word list.**

Not a second 54-item transcription exercise. Not two independent readers. Not 3.5–4.5 hours.

The reason is structural, and it is the main thing this design buys.

---

## Why almost all of the human requirement disappeared

EVAL-003/004 needed readers because it started from **photographs**: someone had to establish what
was in the picture, and dataset labels could not be trusted — the two CVIT releases disagree on 33%
of the same regions.

This battery **renders the images itself**. We choose the string, the renderer draws it, and the
shaper confirms mechanically that what was drawn differs from what we ask about. What the image
says is therefore **known by construction**.

That removes, entirely:

- establishing what each image says;
- resolving reader disagreement;
- adjudication;
- exact-agreement reference construction;
- the second reader.

None of that is a shortcut. There is nothing left for those steps to do.

---

## What still genuinely needs a Hindi speaker

### 1 · Validate the base word list · **required · ~45–75 min once**

The 53 base strings are reused as **lexical items** from EVAL-003's Hindi pack transcriptions. That
reuse is sound for a reason worth being precise about: those annotations were unreliable as claims
about *what a photograph showed*, which is irrelevant here because we render the string ourselves.
What they are being used for is only "is this a real Hindi word".

But that residual question is real. If an annotation was itself a misreading, the "word" may be a
non-word — and **the whole autocorrection hypothesis depends on the base being a plausible real
word**. A model only autocorrects *toward* something.

The reader is asked, per word, one question:

> Is this a real, well-formed Hindi word as written? **yes / no / unsure**

No transcription. No images. A flat list — `native-validation/word-validation-sheet.csv`, with a
stable `word_id` per row.

**What actually happened, and the rule that now governs:** 48 words were accepted, 5 rejected, none
marked unsure. Rejected words do **not** cause a rebuild. The Controller decided **PRUNE, DO NOT
REBUILD**: the 106-item build stays as it is — it is what the reviewer saw — and the 10 items
resting on rejected words are filtered out by `apply_human_validation.py`, which fails closed if the
battery is not the one that was adjudicated. Rebuilding would produce a different allocation nobody
has reviewed, while borrowing the authority of a validation performed on something else.

**This is also the moment to expand the list.** `METRICS-AND-QUALIFICATION.md` shows the hard
stratum needs **84–90 words** to bring the iid reference calculation below 5%. After validation the
pool stands at **48 accepted words**, so that target is further away, not closer. It is a planning
target for a sizing figure, not a threshold that would demonstrate anything about a checker's real
error rate. It was recomputed
after the corrected one-item-per-base-word construction, not carried over from the earlier draft.
Validating ~90 words costs barely more than validating 53, and it is the single highest-value
input to the battery.

⚠️ **The repository cannot currently supply them.** Merged repo-local material yields **53**
distinct Hindi lexical items — **48 after human validation**. Closing the gap needs roughly
**36–42 more**, which is a request to
Resources rather than something Eval should go and find:
[`eval/tasks/EVAL-005-RESOURCES-REQUEST.md`](../../tasks/EVAL-005-RESOURCES-REQUEST.md). Sheet ids
are stable across pool changes, so validation done now is not wasted when the list grows.

### 2 · Confirm perceptibility on a sample · **recommended · ~20 min once**

The shaper proves two strings produce different glyphs. It does **not** prove a human can *see* the
difference at the rendered size — a nukta dot or an anusvara at 40pt is small.

The reader is shown ~25 rendered image pairs — `native-validation/perceptibility-sheet.csv`,
sampled deterministically round-robin across the five failure groups, hard opportunities first —
and asked:

> Can you see a difference between these two images? **yes / no / only when I look closely**

This is a **perceptibility** check, not a reading task. It calibrates whether "visibly different"
means what we think. A class where humans routinely answer "no" should be reported separately or
dropped, because scoring a checker on a difference people cannot see would be unfair in the same
way the invisible-nukta item would have been.

⚠️ **This is not a checker qualification and produces no ground truth.** It tunes item difficulty.

### 3 · Sanity-check the rendering · **required · ~10 min once**

`native-validation/rendering-sanity-sheet.csv`, 20 clean renders. Confirm the sample shows
well-formed Devanagari — no tofu boxes, no broken
conjuncts, no missing marks — so we are not testing checkers against a broken font. Purely a
"does this look like normal Hindi text?" pass.

### 4 · The Class B generated-glyph layer · **not now**

Malformed glyphs genuinely need human judgement, because there is no ground-truth string. That is
specified in `GENERATED-GLYPH-STRESS-LAYER.md` and is **not part of this battery** and not part of
this human ask.

---

## Total

| Task | Time | Kind |
|---|---|---|
| Validate (and ideally expand) the base word list | 45–75 min | lexical judgement |
| Perceptibility sample | ~20 min | visual judgement |
| Rendering sanity check | ~10 min | visual judgement |
| **Total** | **~1.5 hours, once** | |

Against 3.5–4.5 hours across two readers for the abandoned protocol — and unlike that protocol,
**none of this is on the critical path for ground truth**, so a delay in scheduling does not block
building or testing the battery. It only gates *running* it.

---

## What one reader is sufficient for, and why

The abandoned protocol needed **two** readers because a single reader's transcription would have
silently become the answer key, with no way to tell a confident misreading from a correct one.

Here, none of the three tasks establishes ground truth:

- word validation **filters** a pool; a wrong `no` costs one word, not a wrong answer key;
- perceptibility **tunes difficulty**; a wrong answer changes an item's stratum, not its verdict;
- rendering sanity **checks the tool**.

**A mistake in any of them degrades the battery. None of them can corrupt the ground truth, because
the ground truth does not come from a human at all.** That is why one competent reader is enough,
and it is the direct consequence of constructing the images rather than finding them.

If the Controller prefers two readers on the word list for robustness, that is a reasonable
belt-and-braces choice — but it is optional here, where it was structural before.
