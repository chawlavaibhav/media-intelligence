# Devanagari exactness battery — design

**Status: PROPOSED DESIGN. Not approved, not run.**
**No paid checker call · no image/video model spend · no Capability Registry entry · no human time.**

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

Every image is drawn locally from a string we chose, so what it contains is known *by construction* —
no annotator, no dataset label, no reader agreement, no ambiguity. This is exactly what the
photographed pack could not offer, and it is why the human requirement drops from 3.5–4.5 hours
across two readers to about **1.5 hours once** (`NATIVE-VALIDATION.md`).

A mismatch item is built by rendering a **perturbed** string and asking about the **original word**.
The model sees malformed text and is handed a plausible real word: every pull of its language prior
says "yes, that's it". That is precisely where silent autocorrection lives.

---

## Two guards that make it a fair test

**1 · A difference must actually be on the page.** Different Unicode does not guarantee different
pixels. Measured here: precomposed क़ (U+0958) and क + nukta shape to **byte-identical glyphs**. An
item built on that pair would score a checker wrong for correctly reporting what it saw. Every
mismatch must therefore differ **after NFC** *and* **in its shaped glyphs**; rejections are recorded,
not dropped.

**2 · Neither trivial strategy works.** The battery is **50/50 match/mismatch**, so "always match"
and "always mismatch" both score 50%. Base words appear in **both** strata, so word identity carries
no signal. And 27 items are **paired**: identical pixels, different target, opposite expected
answer — a checker cannot be right on both by looking only at the image, nor by ignoring it.

---

## What is built

| File | What it is |
|---|---|
| `devtext.py` | shaping + rendering; the visible-difference validity screen |
| `perturb.py` | the failure taxonomy as deterministic operators, with cluster-plausibility tagging |
| `build_items.py` | balanced, deterministic item construction |
| `test_devanagari_exactness.py` | construction tests, incl. two regressions for defects found while building |
| `FAILURE-TAXONOMY.md` | the exact taxonomy and the deterministic/generative boundary |
| `GENERATED-GLYPH-STRESS-LAYER.md` | Class B — what Unicode **cannot** fake, and how to test it later |
| `CHECKER-CONTRACT.md` | input/output contract for a checker run |
| `METRICS-AND-QUALIFICATION.md` | metrics, proposed gates, statistical bounds, cost |
| `NATIVE-VALIDATION.md` | exactly which cases need a Hindi speaker, and which no longer do |

## Reproducing

```
cd eval/battery/devanagari-exactness
python3 build_items.py --total 120        # builds 106; see the size cap below
python3 test_devanagari_exactness.py
```

Deterministic: the same repository state and seed produce a byte-identical `items.jsonl`.
Requires local `hb-shape` and `pango-view` (HarfBuzz/Pango). **No network, no model, no spend.**

---

## Current build

| | |
|---|---:|
| Items | **106** — 53 match, 53 mismatch |
| Distinct images | 90 (27 items share an image as deliberate pairs) |
| Base words | 53 |
| Failure classes represented | 20, across 5 groups |
| Hard stratum (plausible + `corrupt_image`) | **35** |
| Candidates screened | 1,834 valid, 2 rejected as invisible |

### Two limits, stated plainly

**Size is capped by the word list.** Match items must be *distinct* words — repeating one would
produce duplicate images and hand a checker a repetition cue. So the battery caps at the number of
validated base words. 120 was requested; 106 was built, and the cap is recorded rather than padded.

**The bound that matters is weaker than the headline.** Zero false passes across all 53 mismatches
gives a 95% upper bound of 5.5% — but on the hard stratum (n=35) it is only **8.2%**. Reaching ≤5%
there needs ~85–90 validated base words. That is the single highest-value input, and validating a
longer word list costs barely more than validating the current one.

---

## What this battery cannot do

**It cannot test malformed glyphs.** A renderer always draws well-formed letters; it will never
produce a half-formed ligature, a fused pair, or a stroke between two identities. Those are real
generator failures and they are specified in `GENERATED-GLYPH-STRESS-LAYER.md`, which needs
generation spend that has not been authorised.

So: **a checker that fails this battery cannot be trusted** — it autocorrects well-formed wrong
text, the easier case. A checker that passes has cleared a necessary bar, **not a sufficient one**.
That sentence must accompany any result.
