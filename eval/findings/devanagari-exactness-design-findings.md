# Devanagari exactness battery — design findings

**Date:** 25 Aug 2026 · **Provisional task ID: EVAL-005 (Controller assigns)**
**API/model spend:** ₹0 · **Human specialist time:** 0 h · **Generators run:** 0 · **Registry entries:** 0

What was built, what was learned building it, and what remains uncertain.

---

## 1 · The reframing that makes this tractable

EVAL-004 was stopped because reading photographed signage is a weak proxy for the failure that
matters. The redesign changes the question:

> **Does the evaluator report a match when the visible text differs from the requested target?**

And it changes where ground truth comes from. Instead of *finding* images and trying to establish
what they say, we **construct** them: render a chosen string locally, and what the image contains
is known by construction.

**This dissolves the problem that stopped EVAL-004.** No annotator, no dataset label, no
reader-agreement reference, no adjudication. The human requirement falls from 3.5–4.5 hours across
two readers to **~1.5 hours once**, and none of it establishes ground truth (§6).

---

## 2 · Two different Unicode strings can produce identical pixels — measured

**OBSERVED.** On the rendering font, precomposed क़ (U+0958) and क + nukta (U+0915 U+093C) shape to
the **same glyph sequence**:

```
क़  (U+0958)        -> [uni0915093C=0+770]
क + nukta          -> [uni0915093C=0+770]
```

**Why it matters.** An item built from that pair would ask a checker to report a difference that is
not on the page, and mark it wrong for correctly describing what it saw. That measures Unicode
pedantry, not visual faithfulness — and it would have inflated any checker's apparent false-pass
rate with items no checker should pass.

**What was done.** Every mismatch must satisfy **both** conditions: the strings differ after NFC,
**and** the shaped glyphs differ. Rejections are recorded with their reason. On the current pool,
1,834 candidates pass and 2 are rejected — both this pair.

**A related detail that lines up.** NFC collapses the precomposed nukta letters onto their
decomposed forms, which is also what the renderer draws — so comparing in NFC **agrees with the
pixels**. The contract mandates NFC and nothing looser.

---

## 3 · Direction decides what is being measured

A mismatch can be built two ways, and they are not the same test:

| Direction | Construction | Autocorrect pressure |
|---|---|---|
| **`corrupt_image`** | render the perturbed string, ask about the **real word** | **high** — malformed text, plausible target; every pull of the prior says "yes" |
| `corrupt_target` | render the real word, ask about the perturbed string | low — clean image, odd target |

**INFERRED:** only the first reproduces the production failure. It is 70% of the mismatch stratum;
the second is retained as a control. They are reported separately, because a good score on the easy
direction would otherwise conceal blindness on the hard one.

---

## 4 · Neither trivial strategy survives

- **50/50 match/mismatch** — "always match" and "always mismatch" both score exactly 50%.
- **Base words appear in both strata** — 26 of 53 words back both a match and a mismatch item, so
  recognising the word does not reveal the answer.
- **27 paired items** — identical pixels, different target, **opposite** expected verdict. A checker
  cannot be right on both by judging the image alone, nor by ignoring it.

---

## 5 · Three defects found while building, all fixed

**5.1 · Duplicate images.** The first build cycled 53 words into 60 match slots, producing 25
byte-identical images — wasted budget and a repetition cue. The battery now caps at the number of
distinct words and **reports the cap** (120 requested, 106 built) rather than padding.

**5.2 · Implausible corruptions diluting the hard stratum.** Deleting the first letter of `तोड़ना`
gives `ोड़ना` — a word opening with a vowel sign. Visibly broken, trivially rejected, and it tests
nothing about autocorrection. Such items are now tagged and capped at 15%; plausible corruptions
sort first.

**5.3 · My own plausibility rule was wrong.** It flagged `तोड़ा` — an ordinary Hindi word — as
malformed, because it treated a vowel sign after a **nukta** as illegal. It is not: `ड़ा` is normal
Hindi. The rule would have discarded valid hard items. Corrected, and pinned by a regression test.

*(5.1 and 5.3 are both encoded as tests, so they cannot return unnoticed.)*

---

## 6 · The human requirement, and why it is small

**Not needed at all**, because ground truth is constructed: establishing what an image says,
resolving reader disagreement, adjudication, exact-agreement reference, the second reader.

**Still needed — ~1.5 hours, once:**

| Task | Time | Why |
|---|---|---|
| Validate the base word list | 45–75 min | autocorrection only happens *toward* a plausible word; if a base is not a real word, the item does not test what we think |
| Perceptibility sample (~25 pairs) | ~20 min | the shaper proves glyphs differ; it does not prove a person can **see** it at 40pt |
| Rendering sanity check | ~10 min | so we are not testing checkers against a broken font |

**One reader suffices**, and that is structural rather than a compromise: **none of these three
tasks produces ground truth.** A mistake degrades the battery; it cannot corrupt the answer key,
because the answer key does not come from a human. That is precisely what was not true before.

---

## 7 · What the battery can support statistically

| Stratum | n | 95% upper bound if zero false passes |
|---|---:|---:|
| All mismatches | 53 | 5.5% |
| **Hard stratum** (plausible + `corrupt_image`) | **35** | **8.2%** |
| Per failure class | ~2.6 mean | **not estimable** |

**The headline number is the wrong one to quote.** The stratum that matters is the hard one, and at
n=35 its bound is weak. **Per-class figures are diagnostic signals, never rates** — with two or
three items, one miss moves a "rate" by 30–50 points.

**The concrete ask:** ~85–90 validated base words instead of 53 moves the hard-stratum bound to
≤5%. Validating a longer list costs barely more than validating the current one, which makes it the
highest-value input available.

---

## 8 · What this battery cannot do — the boundary

A renderer always draws **well-formed** glyphs. No string will make it produce a half-formed
ligature, fused letters, a broken headline bar, or a stroke between two identities. Those are real
generator failures — one of ours is a sign whose misspelling **drifted between frames of a single
clip** — and no Unicode substitution reproduces them.

They are specified as **Class B** in `GENERATED-GLYPH-STRESS-LAYER.md`, with a recommended route
(deterministic corruption of clean renders, so the pixels stay known by construction) and an honest
note that programmatic damage is not the same distribution as a diffusion model's failures.

**Consequence for any result:** a checker that fails this battery cannot be trusted — it
autocorrects *well-formed* wrong text, the easier case. A checker that passes has cleared a
**necessary but not sufficient** bar, and that sentence must travel with the number.

---

## 9 · What remains uncertain

- **Whether the base words are all real, well-formed Hindi.** The single most important open
  question, and the reason for the word-list validation.
- **Whether every "visible" difference is perceptible** to a person at the rendered size.
- **Whether font choice changes results.** One font is used. A different face could make a
  difference easier or harder to see; unmeasured.
- **Whether checker shape matters** — transcribe-then-compare versus direct verdict. Both are
  specified and will be reported separately; which is more exposed to autocorrection is a
  hypothesis, not a finding.
- **Whether passing predicts anything about malformed generated glyphs.** Untested by construction.
- **Real per-call pricing.** The cost estimate rests on an old recorded figure that must be
  re-verified before any run.

---

## 10 · Scope and stop state

No paid checker call, no image or video model call, no network request to any model, no human time,
no Capability Registry entry, no BSTD use, no Marathi reserve use, and no change to any approved
EVAL-001/002/003 artifact.

EVAL-004 remains stopped: its Reader-A pilot is not promoted to ground truth, and no checker is
qualified, ranked or entered from it.
