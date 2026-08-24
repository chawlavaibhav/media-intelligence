# Failure taxonomy — Devanagari exactness battery

**Status: PROPOSED design, revised after Controller review. Not approved.**
**No checker/model/API qualification run and no human validation have occurred** — only
deterministic local construction, rendering and test verification. No model has been called.

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

## Validity: the difference must be textual AND actually drawn

A candidate becomes an item **only if** it clears three gates, in order:

| # | Gate | Rejection reason if it fails |
|---|---|---|
| 1 | the **NFC-canonical strings differ** — it is a real textual difference | `canonical_equal` |
| 2 | shaping and rasterising both succeed — the pair can be judged at all | `rendering_error` |
| 3 | the **decoded pixels differ** — the difference is actually on the page | `raster_identical` |

Rejection reasons are recorded in `build/rejected-candidates.jsonl`, never silently dropped.

### Why gate 3 is the decoded pixels — and neither of the two obvious alternatives

Gate 3 compares **decoded rasters**: image dimensions plus RGBA8 pixel data, fingerprinted with
SHA-256. Both of the tempting shortcuts are wrong, in opposite directions.

**Too weak — HarfBuzz glyph sequences.** A different glyph sequence is good *evidence* that two
strings look different, but it is not the same claim. Measured on the pinned font:

```
सुबह        -> [uni0938=0+680|uni0941=0+0|uni092C=2+567|uni0939=3+507]
सु‌बह  (ZWNJ) -> [uni0938=0+680|uni0941=0+0|space=2+0|uni092C=3+567|uni0939=4+507]
```

Different strings after NFC. **Different glyph sequences** — there is an extra zero-advance glyph.
**Identical pixels.** A glyph-only gate would have admitted this as a valid mismatch and then scored
a checker wrong for correctly reporting that the two pictures are the same.

**Too strong — encoded PNG bytes.** A file hash answers "is this the same file", not "is this the
same picture". PNG is a container: the same raster can be written as many byte streams — a different
zlib level, a different chunk split, an extra ancillary chunk. Measured, from a real battery render:
an `hb-view` PNG and two re-encodings of its own decoded pixels give **three different file hashes**
and **one pixel fingerprint**. A file-hash gate would call visually identical images different, and
mark a checker wrong for correctly saying they match.

So two hashes are kept and they answer different questions: `image_file_sha256` is **artifact**
identity (did a checker read the file we shipped?), and the pixel fingerprint is **visual** identity.
Only the second decides `raster_identical`.

The glyph comparison is retained as a diagnostic and recorded on every rejection, so we can see when
the two disagree. On the current 53-word pool they never did: 1,834 candidates pass, 2 are rejected
as `canonical_equal` (both the nukta pair below), and **0** as `raster_identical`. Switching from
file bytes to decoded pixels also changed **no item** — every image in the battery has a distinct
picture as well as distinct bytes. The gate is nonetheless the decoded raster, because that is the
claim the battery actually makes.

## Plausibility: what may enter the hard stratum

Some perturbations produce strings that are *visibly broken* rather than plausibly misspelled.
Silent autocorrection happens only when corrupted text still looks like it could be a word — a
model cannot read toward a plausible reading that is not there. A checker that rejects an obviously
broken string has demonstrated nothing about resisting autocorrection.

**Plausibility is decided by two rules, and the shaper has the final word.**

1. **A string rule** — no cluster may open with a vowel sign or other combining mark; a virama
   must sit *between* two consonants; a nukta must follow a consonant.
2. **The shaper** — any string HarfBuzz draws with a **dotted circle (U+25CC)** is visibly broken.
   That glyph is the writing system's own "this cluster is invalid" marker and is unmistakable on
   the page.

The second rule caught two items the first had let into the hard stratum. Deleting the first
consonant of `इंग्लीश` leaves `इं्लीश`, whose virama hangs off an anusvara; deleting the first
consonant of `बॉम्बे` leaves `ॉम्बे`, which opens with U+0949 — a vowel sign the string rule's list
did not contain. Both shape with a dotted circle. Asking the shaper what it actually drew is a
better test than asking us what we think is legal, and it is now the authoritative one.

*(The string rule also once mis-flagged `तोड़ा` — an ordinary Hindi word — because it treated a
vowel sign after a nukta as illegal. Corrected, and pinned by a regression test. Widening the
vowel-sign set to catch `ॉम्बे` briefly reintroduced that same bug, because U+093C NUKTA sits
inside the numeric run of vowel signs; the regression test caught it immediately.)*

⚠️ **What "plausible" does and does not mean here.** Both rules test whether the string is a
**well-formed Devanagari cluster** — something the script permits and the shaper draws cleanly.
Neither tests whether it is a *lexically* likely misspelling. `ककालका` (a doubled initial
consonant, from `कालका`) is well-formed and passes, though no Hindi word looks like that. That is
defensible for this battery — duplicated letters are a real generator failure, and the checker is
being asked about *drawing*, not about the lexicon — but it means the hard stratum is "well-formed
and visually subtle", not "a mistake a human would plausibly make". The perceptibility sample in
`NATIVE-VALIDATION.md` is where a reader can tell us if any of them are too easy.

**Visibly-broken strings are kept, but never in the hard stratum.** They are capped at 15% of the
mismatch stratum and are always assigned the `corrupt_target` direction, so the malformation sits
in the *string we ask about* and never in the image. On the current build 2 of 53 mismatches are
of this kind, and the hard stratum of 37 is entirely plausible with clean shaping.

## Direction: the axis that decides what is being measured

| Direction | Construction | What it measures |
|---|---|---|
| **`corrupt_image`** | render the **perturbed** string, ask about the **real word** | The model sees malformed text and is handed a plausible word. Every pull of its language prior says "yes, that's it." **This is where silent autocorrection happens** — the primary stratum, 70% of mismatches (37 of 53 on the current build), and the only stratum the iid reference figure is quoted on. |
| `corrupt_target` | render the **real word**, ask about the **perturbed** string | Clean image, odd target. Much easier. A control: failing here is failing basic comparison. |

Reported separately. Collapsing them would let a good score on the easy direction conceal
blindness on the hard one.
