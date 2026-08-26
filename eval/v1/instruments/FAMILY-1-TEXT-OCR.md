# Family 1 — Text / OCR instruments

**Judges:** is the string in the picture exactly the string we asked for?
**Status: NOT QUALIFIED.** Pack exists and is frozen; no checker has run against it.

---

## What this family is for

Two different judgements share this family and **must not be confused**:

| Judgement | Question | Material |
|---|---|---|
| **Reading real text** | Can the checker read Hindi off a photograph of a sign? | Photographed signage |
| **Judging generated text** | Can the checker tell that generated text is subtly wrong? | Constructed renders |

They are different capabilities. A checker excellent at the first can be useless
at the second, because the second is adversarial: the wrong string is *designed*
to be plausible, and every pull of a language model's prior says "yes, that's
the word." The founding failure — six false passes on visibly misspelled signs —
was a failure of the second kind.

**The Registry must never cite a reading benchmark as evidence about the second
judgement.** Related and equally firm: a text-*recognition* benchmark is never
evidence about a *generator*. Reading and drawing are different capabilities.

---

## Devanagari — the pack is finished

**Authoritative pack:** `eval/battery/devanagari-exactness/`, validated view.

| | |
|---|---:|
| Items | **96** |
| Match / mismatch | **48 / 48** |
| Human-accepted base words | **48** |
| **Hard opportunities** | **33** (on 33 distinct base words) |
| Failure classes / groups | **20 / 5** |

**Why the ground truth needs no annotator.** The images are rendered from
strings *we chose*, so each item's match/mismatch label is **true by
construction**. No human decides whether a picture matches its target.

**This did not remove humans.** One Hindi-competent reviewer answered **98 of 98**
questions — 0 unanswered, 0 unsure — on three separate questions: is each base
word valid Hindi, is the rendered difference perceptible, and is the render
surface usable. Five of 53 base words were rejected, excluding 10 items, which
were **not replaced**. That preserves the identity of items already reviewed
rather than opening a fresh human-validation surface.

**One reader is provenance, not ground truth.** The record says so itself. Two
items flagged in both the word and rendering questions are *within-reader*
consistency, **not** a second reader. No threshold, rate or checker claim may be
derived from the human validation.

*Verified in this session: both frozen response-artifact SHA-256 hashes
recomputed and matched.*

### The gate

> **Rule 1 — zero false passes on every mismatch item. Disqualifying.**

One rule, not two. The hard stratum is a *subset* of all mismatches, so "zero
across all" already contains "zero on the hard subset". Presenting them as two
statistical gates would double-count one piece of evidence.

| Stratum | n | What a failure there means |
|---|---:|---|
| **Hard** — plausible corruption, real word as target | **33** | The production failure exactly: malformed text, plausible target, checker waves it through. **The checker autocorrects**, and an autocorrecting checker cannot be a gate however good its other numbers are. |
| **Control** — clean image, odd target | 15 | Not evidence about autocorrection. It means the checker **is not comparing against the target at all**. Also disqualifying, for a more basic reason. |

- **Rule 2 — usability.** False-fail ≤ 10% on the 48 clean match items; refusal ≤ 5%, reported separately, never folded into a verdict.
- **Rule 3 — stability.** Repeat consistency ≥ 0.95 across **≥3 full passes of the whole battery, in both shapes**.

⚠️ **0.95, 10% and 5% are judgement calls with no empirical backing in this
repository.** They require Controller approval before a run and should be
revisited once we have seen what real checkers actually do.

### Two shapes, receiving different inputs

- **`transcribe`** — checker never sees the target; our code does the comparison.
- **`verdict`** — checker sees the target.

Comparing them measures **how much of a checker's false-pass behaviour is caused
by showing it the answer we hope for.** The blind payload is verified
mechanically before any call: an allow-list that fails closed, plus a sweep for
any Devanagari character at all.

### What passing would and would not license

> Passing means the checker **did not autocorrect any of 33 distinct hard
> base-word opportunities on this battery's material.**
>
> Under an iid/exchangeable Bernoulli model **which this battery does not
> establish**, that corresponds to a 95% reference upper bound of **8.68%** — a
> sizing calculation, **not** the checker's real-world error rate.
>
> It does **not** mean the checker is accurate, and it says **nothing** about
> malformed *generated* glyphs, which this battery cannot produce.

**The gap that matters commercially:** this battery perturbs *real characters*.
A generator can emit shapes that are not characters at all. The Class B
generated-glyph stress layer is specified but **not built**, and needs
generation spend. Until it exists, a checker qualified here is qualified against
*correctly-formed wrong text*, not against *malformed glyphs*.

---

## Latin — the pack does not exist

**Must be built separately, and must NOT mutate the Devanagari pack** (it is
frozen; changing it would invalidate the human validation performed against it).

Recommended construction, mirroring what worked:
- deterministic render-target pairs, ground truth by construction, no annotator;
- perturbation classes suited to Latin: visually confusable pairs (rn/m, l/I/1,
  0/O, cl/d), case errors, doubled and dropped letters, transpositions,
  punctuation and digit errors — the last being commercially load-bearing
  because prices and claims are where an error is most expensive;
- **one mismatch item per base string**, so opportunities are counted, not items;
- both shapes, same blind verification;
- **no human validation needed for word validity** — English word validity can
  be settled against a dictionary, which is why this pack is much cheaper than
  the Devanagari one. Perceptibility still needs a human check.

**Estimated human cost: substantially below the Devanagari pack's ~1.5 hours**,
because the word-validity question is machine-answerable.

---

## Qualification inputs

| Need | State |
|---|---|
| Devanagari pack | ✅ exists, frozen, validated |
| Latin pack | ❌ not built |
| Generated-glyph stress layer | ❌ specified, not built, needs generation spend |
| Checker roster + API budget | ❌ not approved |
| Thresholds approved | ❌ proposed only |
| Photographed-signage pack (for the *reading* judgement) | ✅ 54-item pack exists, untouched — but its two-reader protocol was **stopped after Reader A**, so there is **no two-reader reference** and no checker may be qualified from it |
