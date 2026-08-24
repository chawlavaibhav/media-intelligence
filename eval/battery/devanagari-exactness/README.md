# Devanagari exactness battery — design

**Status: PROPOSED DESIGN, revised after Controller review. Not approved, not run.**
**No paid checker call · no image/video model spend · no Capability Registry entry · no human time.**

Authoritative task file: [`eval/tasks/EVAL-005.md`](../../tasks/EVAL-005.md).

---

## The question

Not *"can a VLM read an easy Hindi sign?"* — the pilot that was stopped showed that is too weak a
proxy. The question that decides whether a checker is usable in production is:

> **Can an evaluator faithfully determine whether the visible Devanagari exactly matches the
> requested target, without silently autocorrecting plausible-looking errors?**

The dangerous answer is a **false pass**: the checker says "matches" when the text is wrong, and a
broken asset ships with a passing grade attached. We have watched this happen — one checker
reported `सुबह की पहली चाय — exact match` for six frames that visibly read `सुवह`.

---

## The move that makes this tractable

**We render the images ourselves.**

Every image is drawn locally from a string we chose, with a font file pinned by SHA-256, so what it
contains is known *by construction* — no annotator, no dataset label, no reader agreement, no
ambiguity. This is exactly what the photographed pack could not offer, and it is why the human
requirement drops from 3.5–4.5 hours across two readers to about **1.5 hours once**
(`NATIVE-VALIDATION.md`).

A mismatch item is built by rendering a **perturbed** string and asking about the **original word**.
The model sees malformed text and is handed a plausible real word: every pull of its language prior
says "yes, that's it". That is precisely where silent autocorrection lives.

---

## Four guards that make it a fair test

**1 · A difference must actually be on the page — checked on the pixels.** Different Unicode does
not guarantee different pixels, and neither does a different glyph sequence. Measured here:
precomposed क़ (U+0958) and क + nukta are canonically equal and render identically; and `सु‌बह`
(with a zero-width non-joiner) shapes to a **different glyph sequence** from `सुबह` yet produces a
**byte-identical PNG**. Every mismatch must therefore differ **after NFC** *and* **in its final
raster output**. Glyph comparison is kept as a diagnostic, not as the gate. Rejections are
recorded, not dropped.

**2 · The blind shape is actually blind.** Shape 1 (`transcribe`) never sees the target — it is
evaluator-side only, and a mechanical pre-run check refuses to write a payload containing any
target field or any Devanagari character at all. Shape 2 (`verdict`) does see the target, by
design. Comparing the two measures how much of a checker's false-pass behaviour is caused by
showing it the answer we hope for.

**3 · One hard opportunity per base word.** Every mismatch item sits on a distinct base word, so
the statistical bound is computed over opportunities that are genuinely separate rather than over
four deterministic perturbations of the same word. Class coverage is preserved by solving the
allocation as a bipartite matching, not by relaxing the rule.

**4 · Neither trivial strategy works.** The battery is **50/50 match/mismatch**, so "always match"
and "always mismatch" both score exactly 50%. Every base word appears in **both** strata, so word
identity carries no signal. And 32 items are **paired**: identical pixels, different target,
opposite expected answer — a checker cannot be right on both by looking only at the image, nor by
ignoring it.

---

## What is built

| File | What it is |
|---|---|
| `devtext.py` | shaping + rendering on one pinned font asset; the pixel-level validity screen |
| `perturb.py` | the failure taxonomy as deterministic operators, with cluster-plausibility tagging |
| `checker_input.py` | per-shape checker projections, frozen prompts, and the blind check |
| `build_items.py` | balanced, deterministic item construction and the opportunity model |
| `test_devanagari_exactness.py` | 121 checks across 37 tests, including five regressions for defects found while building |
| `FAILURE-TAXONOMY.md` | the exact taxonomy and the deterministic/generative boundary |
| `GENERATED-GLYPH-STRESS-LAYER.md` | Class B — what Unicode **cannot** fake, and how to test it later |
| `CHECKER-CONTRACT.md` | input/output contract, per shape, and the comparison predicate |
| `METRICS-AND-QUALIFICATION.md` | metrics, proposed gates, the opportunity model, cost |
| `NATIVE-VALIDATION.md` | exactly which cases need a Hindi speaker, and which no longer do |
| `native-validation/` | the prepared, **not executed**, validation sheets and plan |

## Reproducing

```
cd eval/battery/devanagari-exactness
python3 build_items.py --total 120        # builds 106; see the size cap below
python3 test_devanagari_exactness.py
```

Deterministic **for a given environment**: the same repository state, the same font file and the
same HarfBuzz build produce a byte-identical `items.jsonl`.

### ⚠ Portability, stated accurately

This battery is **not portable as-is**, and the previous draft overstated that it was. It requires:

| Requirement | Value used for the recorded build |
|---|---|
| `hb-shape` and `hb-view` | HarfBuzz 14.2.1 |
| Font **file** (not a family name) | `/System/Library/Fonts/Kohinoor.ttc`, face index 0 |
| Font SHA-256 | `8b508b160d4573963c064e951af48c33c6381901253ec6ae0feb86d80fde1f31` |
| Point size / margin | 40 / 24 |

The font is a proprietary macOS system asset. **It is deliberately not committed** — redistributing
it is a licence question we have no basis to answer. Its identity is pinned by SHA-256 instead, and
recorded in `build-summary.json` with the tool versions, so a future run can *prove* it used the
same bytes or discover that it did not.

If the font file is absent, the build raises `FontMissing` and stops. It does not fall back to
another face — silently drawing through a different font would invalidate every visibility
decision the battery has made, invisibly. Running on a machine without this exact asset means
rebuilding the battery and recording the new provenance, and results across the two are not
directly comparable.

**No network, no model, no spend.** A test asserts that no module in this directory references a
network client, a URL or an API key.

---

## Current build

| | |
|---|---:|
| Items | **106** — 53 match, 53 mismatch |
| Distinct images | 90 (32 items share an image as deliberate pairs) |
| Base words | 53 |
| Failure classes represented | 20, across 5 groups |
| Mismatch items / distinct mismatch base words | **53 / 53** |
| **Hard opportunities / distinct hard base words** | **37 / 37** |
| Candidates screened | 1,834 valid; 2 rejected `canonical_equal`; 0 rejected `raster_identical` |

### Two limits, stated plainly

**Size is capped by the word list.** Match items must be *distinct* words, and every mismatch must
sit on a *distinct* base word. So the battery caps at the number of validated base words. 120 was
requested; 106 was built, and the cap is recorded rather than padded.

**The bound that matters is weaker than the headline.** Zero false passes across all 53 mismatches
gives a 95% upper bound of 5.5% — but that figure *contains* the hard stratum and is not separate
evidence. On the 37 distinct hard opportunities the bound is **7.8%**. Reaching ≤5% there needs
**84–85 validated base words**, which the repository cannot currently supply: merged repo-local
material yields 53. See `METRICS-AND-QUALIFICATION.md` and
[`EVAL-005-RESOURCES-REQUEST.md`](../../tasks/EVAL-005-RESOURCES-REQUEST.md).

And whatever the size: the bound is conditional on this battery's words, operators and font. It is
**not** an estimate of a checker's universal true error rate.

---

## What this battery cannot do

**It cannot test malformed glyphs.** A renderer always draws well-formed letters; it will never
produce a half-formed ligature, a fused pair, or a stroke between two identities. Those are real
generator failures and they are specified in `GENERATED-GLYPH-STRESS-LAYER.md`, which needs
generation spend that has not been authorised.

So: **a checker that fails this battery cannot be trusted** — it autocorrects well-formed wrong
text, the easier case. A checker that passes has cleared a necessary bar, **not a sufficient one**.
That sentence must accompany any result.
