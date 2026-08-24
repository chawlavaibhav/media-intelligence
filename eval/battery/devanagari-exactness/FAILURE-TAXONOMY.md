# Failure taxonomy — Devanagari exactness battery

**Status: PROPOSED design. Not approved, not run. No model has been called.**

---

## What the taxonomy is for

The battery asks one question:

> **Does the evaluator report a match when the visible text differs from the requested target?**

To answer it we need mismatches that resemble the mistakes a *generator* makes — a dropped vowel
sign, a broken conjunct, a letter that looks like its neighbour — and that remain plausible enough
that a model reading toward the nearest real word will wave them through. A taxonomy of obviously
broken strings would measure OCR competence, not resistance to autocorrection.

Every class below is implemented as a deterministic operator in `perturb.py` and is exercised by
`test_devanagari_exactness.py`.

---

## The dividing line that matters

**Class A — representable as a different Unicode string.** Render a different string and the
difference is really on the page. Ground truth is exact and free.

**Class B — NOT representable that way.** A renderer always draws *well-formed* glyphs. It cannot
produce a half-formed ligature, a smeared stroke, or a letter that sits between two identities.
Those are real and common generator failures, but no choice of Unicode string will produce them.

**Pretending Class B is covered by Class A would be the central dishonesty available in this
design.** It is not covered. Class B is specified separately in
`GENERATED-GLYPH-STRESS-LAYER.md` and requires generated images, which requires spend the
Controller has not authorised.

---

## Class A — deterministic, implemented now

### A1 · Vowel signs (matras) — group `vowel_signs`

| Class | What changes | Why it belongs |
|---|---|---|
| `MATRA_SUBSTITUTE` | one vowel sign becomes a visually similar one (ि↔ी, ु↔ू, े↔ै, ो↔ौ) | differs by one stroke or stroke-count; the most autocorrect-prone error in the set |
| `MATRA_DELETE` | a vowel sign is dropped | consonants survive, the word changes |
| `MATRA_INSERT` | a vowel sign is added to a bare consonant | |
| `MATRA_REPOSITION` | the same vowel sign attaches to a different consonant | same character inventory, different word — invisible to any bag-of-characters comparison |
| `INDEP_VOWEL_SUBSTITUTE` | an independent vowel letter becomes another (अ→आ) | whole-letter vowel error |

### A2 · Letters — group `letters`

| Class | What changes |
|---|---|
| `CONSONANT_SUBSTITUTE` | a consonant becomes a **visually confusable** one: ब/व, भ/म, घ/ध, ङ/ड, थ/य, ट/ठ, प/ष, ख/रव, ऋ/ॠ, द/ढ |
| `CHAR_DELETE` | a consonant is dropped |
| `CHAR_INSERT` | a consonant is duplicated |
| `CHAR_TRANSPOSE` | two adjacent letters swap |

**ब/व and य/थ are not hypothetical.** Both appear in this project's own recorded generator
failures: `सुबह` rendered as `सुवह`, and `चाय` as `चाथ`.

### A3 · Conjuncts and half-forms — group `conjuncts`

| Class | What changes |
|---|---|
| `CONJUNCT_SPLIT` | a virama is removed, so a fused ligature becomes two separate letters |
| `CONJUNCT_FORM` | a virama is inserted, fusing two letters into a ligature |

Visually large and mechanically verifiable: क्ष shapes to a **single** glyph `uni0915094D0937`;
कष shapes to **two**. A generator that fails to form a ligature produces exactly this.

### A4 · Dots and marks — group `dots_marks`

| Class | What changes |
|---|---|
| `NUKTA_ADD` / `NUKTA_REMOVE` | the subscript dot that changes a consonant's identity |
| `NASAL_SUBSTITUTE` | anusvara ं ↔ chandrabindu ँ — a dot versus a dot with a crescent |
| `NASAL_DELETE` / `NASAL_INSERT` | nasal mark dropped or added |
| `VISARGA_ADD` / `VISARGA_REMOVE` | the two-dot visarga ः |

⚠️ **Nukta carries a trap, and it is screened.** Precomposed क़ (U+0958) and क + nukta
(U+0915 U+093C) are different Unicode strings that shape to **byte-identical glyphs**. An item
built on that pair would mark a checker wrong for correctly reporting what it saw. See §Validity.

### A5 · The two positional forms of र — group `ra_forms`

| Class | What changes |
|---|---|
| `REPH_TO_FULL_RA` | reph (र् drawn as a hook above the next letter) becomes a full र |
| `RAKAR_TO_FULL_RA` | rakar (्र drawn as a subscript stroke) becomes a full र |
| `FULL_RA_TO_REPH` | a full र becomes a reph |

र is written three different ways depending on position. A generator that picks the wrong
positional form produces a visibly different word from the same underlying letters.

---

## Validity: two conditions, both required

A candidate becomes an item **only if**:

1. **the normalised strings differ** (NFC) — it is a real textual difference; and
2. **the shaped glyph sequences differ** (HarfBuzz) — the difference is actually drawn.

Rejection reasons are recorded in `build/rejected-candidates.jsonl`, never silently dropped.

| Reason | Meaning |
|---|---|
| `normalised_equal` | not a textual difference at all after NFC |
| `glyphs_identical` | a textual difference the renderer does not draw — asking a checker to see it would penalise correct observation |

On the current base pool, 1,834 candidates pass and **2 are rejected as `normalised_equal`** — both
the nukta pair above.

---

## Plausibility: a difficulty axis, not a filter

Some perturbations produce strings that are *visibly broken* rather than plausibly misspelled — a
word opening with a vowel sign, or ending on a bare virama. These are kept, but tagged and capped
at **15%** of the mismatch stratum, because:

- a checker that misses them is unusable, so they are a useful floor; but
- rejecting them demonstrates nothing about resisting autocorrection, so they must not dilute the
  stratum that does.

Results are reported split by plausibility.

*(The plausibility rule initially mis-flagged `तोड़ा` — an ordinary Hindi word — because it treated
a vowel sign after a nukta as illegal. Corrected, and pinned by a regression test.)*

---

## Direction: the axis that decides what is being measured

| Direction | Construction | What it measures |
|---|---|---|
| **`corrupt_image`** | render the **perturbed** string, ask about the **real word** | The model sees malformed text and is handed a plausible word. Every pull of its language prior says "yes, that's it." **This is where silent autocorrection happens** — the primary stratum, 70% of mismatches. |
| `corrupt_target` | render the **real word**, ask about the **perturbed** string | Clean image, odd target. Much easier. A control: failing here is failing basic comparison. |

Reported separately. Collapsing them would let a good score on the easy direction conceal
blindness on the hard one.
