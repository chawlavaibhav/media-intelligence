# Devanagari exactness battery — design

**Status: design approved and merged. Human validation COMPLETE.**
**Checker qualification has NOT started** — no checker selected, no checker/model/API call.
**No paid checker call · no image/video model spend · no Capability Registry entry.**

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

**1 · A difference must actually be on the page — checked on the decoded pixels.** Three candidate
tests exist and two of them are wrong, in opposite directions. Measured here:

- *Unicode difference is too weak* — precomposed क़ (U+0958) and क + nukta are canonically equal and
  draw the same picture.
- *Glyph-sequence difference is too weak* — `सु‌बह` (zero-width non-joiner) shapes to a **different
  glyph sequence** from `सुबह` and draws **identical pixels**.
- *Encoded PNG difference is too strong* — one picture written three ways (an `hb-view` render plus
  two re-encodings of its own pixels) gives **three different file hashes** and **one picture**.

So every mismatch must differ **after NFC** *and* **in its decoded raster** — dimensions plus RGBA8
pixel data. Glyph comparison is kept as a diagnostic. Two hashes are kept and named apart:
`image_file_sha256` is artifact identity, the pixel fingerprint is visual identity. Rejections are
recorded, not dropped.

**2 · The blind shape is actually blind.** Shape 1 (`transcribe`) never sees the target — it is
evaluator-side only, and a mechanical pre-run check refuses to write a payload containing any
target field or any Devanagari character at all. Shape 2 (`verdict`) does see the target, by
design. Comparing the two measures how much of a checker's false-pass behaviour is caused by
showing it the answer we hope for.

**3 · One hard opportunity per base word — and no overclaim about it.** Every mismatch item sits on
a distinct base word, so the sizing figure is computed over distinct base-word opportunities rather
than over four deterministic perturbations of the same word. Class coverage is preserved by solving
the allocation as a bipartite matching, not by relaxing the rule. **Distinct words are not iid
trials, and nothing here says they are:** the qualification gate is the deterministic *zero false
passes*, and the Clopper-Pearson figure is an explicitly labelled reference calculation for sizing.

**4 · Neither trivial strategy works.** The battery is **50/50 match/mismatch**, so "always match"
and "always mismatch" both score exactly 50%. Every base word appears in **both** strata, so word
identity carries no signal. And 32 items are **paired**: identical pixels, different target,
opposite expected answer — a checker cannot be right on both by looking only at the image, nor by
ignoring it.

---

## What is built

| File | What it is |
|---|---|
| `devtext.py` | shaping + rendering on one pinned font asset; the validity screen |
| `pngraster.py` | stdlib PNG decoder — pixel fingerprint (visual identity) vs file hash (artifact identity) |
| `perturb.py` | the failure taxonomy as deterministic operators, with cluster-plausibility tagging |
| `checker_input.py` | per-shape checker projections, frozen prompts, and the blind check |
| `build_items.py` | balanced, deterministic item construction and the opportunity model |
| `test_devanagari_exactness.py` | 149 checks across 41 tests, including regressions for every defect found while building |
| `FAILURE-TAXONOMY.md` | the exact taxonomy and the deterministic/generative boundary |
| `GENERATED-GLYPH-STRESS-LAYER.md` | Class B — what Unicode **cannot** fake, and how to test it later |
| `CHECKER-CONTRACT.md` | input/output contract, per shape, and the comparison predicate |
| `METRICS-AND-QUALIFICATION.md` | metrics, proposed gates, the opportunity model, cost |
| `NATIVE-VALIDATION.md` | exactly which cases need a Hindi speaker, and which no longer do |
| `native-validation/` | the validation sheets and plan |
| `human-validation/` | **the completed human validation** — frozen record, raw responses, exclusion decision |
| `apply_human_validation.py` | deterministic fail-closed filter producing the 96-item validated view |

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
| PNG decoding | `pngraster.py`, stdlib `zlib` only — no Pillow, no numpy, no image library |
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

> **Human validation is complete.** One reviewer rejected 5 of the 53 base words, excluding the 10
> items resting on them. The **authoritative battery for a checker run is the 96-item validated
> view** — see [`human-validation/HUMAN-VALIDATION-RECORD.md`](human-validation/HUMAN-VALIDATION-RECORD.md)
> and run `python3 apply_human_validation.py --from-build build`.
>
> **96 items · 48 match / 48 mismatch · 33 hard opportunities on 33 distinct base words · 48
> human-accepted base words · 20/20 classes · 5/5 groups · iid reference figure 8.68%.**
> Three classes rest on a single item (`NASAL_SUBSTITUTE`, `NUKTA_REMOVE`, `REPH_TO_FULL_RA`) —
> thin diagnostic coverage, not class loss.
>
> The 106-item build below is unchanged and remains the historical source material.

| | |
|---|---:|
| Items | **106** — 53 match, 53 mismatch |
| Distinct images | 90 (32 items share an image as deliberate pairs) |
| Base words | 53 |
| Failure classes represented | 20, across 5 groups |
| Mismatch items / distinct mismatch base words | **53 / 53** |
| **Hard opportunities / distinct hard base words** | **37 / 37** |
| Candidates screened | 1,834 valid; 2 rejected `canonical_equal`; 0 rejected `raster_identical` |
| Distinct image files / file hashes / **pixel fingerprints** | 90 / 90 / **90** |

### Two limits, stated plainly

**Size is capped by the word list.** Match items must be *distinct* words, and every mismatch must
sit on a *distinct* base word. So the battery caps at the number of validated base words. 120 was
requested; 106 was built, and the cap is recorded rather than padded.

**The sizing figure is weaker than the headline, and it is a sizing figure.** Under an iid /
exchangeable Bernoulli model — which **this battery does not establish** — zero false passes across
37 distinct hard opportunities corresponds to a one-sided 95% reference upper bound of **7.8%**. The
all-mismatch figure of 5.5% *contains* the hard stratum and is not separate evidence.

Bringing the reference figure below 5% needs **84–85 validated base words**; merged repo-local
material yields 53. See `METRICS-AND-QUALIFICATION.md` and
[`EVAL-005-RESOURCES-REQUEST.md`](../../tasks/EVAL-005-RESOURCES-REQUEST.md), whose first step is a
check of existing Resources material rather than any acquisition.

**More words tighten the calculation; they do not supply the assumption.** The figure is not a
universal checker error bound and not an estimate of real-world error at any word count. The actual
qualification gate is deterministic — *zero false passes* — and needs no probability model.

---

## What this battery cannot do

**It cannot test malformed glyphs.** A renderer always draws well-formed letters; it will never
produce a half-formed ligature, a fused pair, or a stroke between two identities. Those are real
generator failures and they are specified in `GENERATED-GLYPH-STRESS-LAYER.md`, which needs
generation spend that has not been authorised.

So: **a checker that fails this battery cannot be trusted** — it autocorrects well-formed wrong
text, the easier case. A checker that passes has cleared a necessary bar, **not a sufficient one**.
That sentence must accompany any result.
