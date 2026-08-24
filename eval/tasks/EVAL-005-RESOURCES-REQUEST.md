# Cross-stream request to Resources — Hindi lexical items for EVAL-005

**From:** Eval / Capability Lab · **Task:** EVAL-005 · **Date:** 25 Aug 2026
**Status: REQUEST, not an approved task.** Only the Controller can open a Resources task. Eval has
**not** gone looking for material, and must not.
**Severity tag:** `CROSS_STREAM`.

---

## The one-line ask

> **~31–37 additional distinct Hindi lexical items — words, not images, not transcriptions of
> photographs — so the Devanagari exactness battery can support a ≤5% qualification bound instead
> of 7.8%.**

Nothing else is requested. No new images. No new annotations. No new corpus.

---

## Why the current pool is insufficient — the arithmetic

The battery's qualification bound is computed over **hard opportunities**: items where a corrupted
word is *drawn* and the checker is asked about the *real* word. That is the case where a model's
language prior pulls it toward answering "yes, that matches", which is the production failure.

Two structural rules fix how many opportunities a word list yields:

1. **Every mismatch item sits on a distinct base word.** Four perturbations of one word are not
   four independent chances to catch a checker out, so counting them as such would inflate the
   apparent sample. One word, one opportunity.
2. **70% of the mismatch stratum is built in the hard direction**, the rest being controls.

That gives:

| Validated base words | Hard opportunities | 95% upper bound with zero false passes |
|---:|---:|---:|
| **53 — everything the repository has today** | **37** | **7.8%** |
| 84 | 59 | 4.95% |
| 90 | 63 | 4.6% |

**In plain English:** at 53 words, a checker that never once waved a broken image through could
still be wrong roughly 8 times in 100 on this material without us seeing it. Getting that ceiling
below 5 in 100 needs 59 distinct hard opportunities, which needs about 84–90 words.

## What the repository actually holds — checked, not assumed

| Source, in merged `main` | Distinct Hindi strings | Usable as base words? |
|---|---:|---|
| `eval/calibration/devanagari-v0/candidate-manifest.jsonl` | **53** | yes — already in use |
| `eval/calibration/devanagari-v0/annotator-disagreement.json` | ~50 | **no** |
| `resources/manifests/corpus-pilot-v0.jsonl` (34,786 records) | 0 | no — every record carries `source_labels_ref: null`; the manifest holds no transcriptions |
| Raw corpus label files (`*_gt.txt`) | unknown | not available — `resources/corpus/raw/` is git-ignored and absent from merged state |
| Everything else committed | <15 across scattered docs | no — illustrative examples in prose, not a lexicon |

**Why the disagreement file cannot be used**, even though it superficially looks like ~50 free
words: its strings are *specifically the contested ones* — the regions where two dataset releases
assigned different transcriptions. At least one member of every pair is wrong by construction
(`सर्राफा` / `सरर्फि`, `शक्ति` / `शकती`), and several are Marathi rather than Hindi (`पोलीस`,
`ठाणे`). Using them would put non-words at the base of items whose whole premise is that the base
is a plausible real word. It is the worst available source, not a convenient one.

**So the gap is real: 53 available, 84–90 needed, ~31–37 short.**

---

## What Eval needs, precisely

| Requirement | Specification |
|---|---|
| **Quantity** | 31–37 additional items minimum; 40–50 preferred, because some will be rejected during reader validation |
| **Form** | **plain text strings**, one lexical item per record. Not images. Not image-region transcriptions. |
| **Script** | Devanagari, in Unicode. Any encoding is fine; Eval normalises to NFC. |
| **Language** | **Hindi.** Marathi is a separate reserve and must not be substituted to make up the count. |
| **Word form** | single orthographic words preferred; short two-word phrases acceptable. No sentences, no punctuation-heavy strings, no numerals-only strings. |
| **Length** | 3–12 Devanagari characters. Shorter gives the perturbation operators too little to work on; longer makes a single-line render unwieldy. |
| **Feature coverage** *(desirable, not required)* | the battery covers 20 failure classes, and the scarcest need specific features. Items containing **a nukta**, **a visarga (ः)**, **a chandrabindu (ँ)**, **a reph (र् before a consonant)** or **a rakar (्र)** are worth more than generic words, because those classes currently rest on 1–2 items each. |
| **Provenance** | each item must carry its source and access date, per normal Resources bookkeeping. Eval records provenance per base word in the build manifest. |
| **Rights** | public and ungated is sufficient. `not_stated` / `not_verified` is acceptable under the existing Resources policy: the words are used **internally only**, are never redistributed, are not training data, and are not shipped to a customer. A word list is also not a creative work being reproduced — but that is Resources' judgement to record, not Eval's. |
| **What must NOT be used** | **BSTD** (held as the only genuinely independent source lineage — do not spend it on a word list) and the **Marathi reserve**. |

## What Eval does NOT need

- No images, crops or bounding boxes — the battery renders its own.
- No human transcriptions — the words are used as *lexical items*, and what is on the page is known
  by construction.
- No agreement between annotators — irrelevant here.
- No new download of the CVIT corpus if a cheaper route exists.

## A cheaper route that may already exist

**INFERRED, not verified by Eval.** The EVAL-003 pool builder reads Hindi transcriptions out of
per-image `*_gt.txt` files under `resources/corpus/raw/`, and selected 54 items out of **173
eligible Hindi-labelled photographs**. The transcriptions of the other **119** were enumerated
during that build but never committed — only the 54 selected records were.

If those label files are still on the Resources machine, some or all of the gap may already be in
hand and need only be extracted into a plain word list, with **no new acquisition at all**. How
many *distinct* words those 119 photographs yield is **unknown**: they may repeat each other and
they may repeat the 53 already in use. Eval cannot check, because `resources/corpus/raw/` is
git-ignored and absent from merged state. This is Resources' to verify first, before any download
is considered.

**Open dependency:** Resources PR #5 concerns IndicSTR12 / IIIT-ILST composition and *recoverable
crop transcriptions*. It was **open, not merged**, when this request was written, so nothing here
depends on it. If it has merged by the time this is read, its records may already answer the
question above and should be checked first.

---

## What this unblocks, and what it does not

**Unblocks:** a ≤5% qualification bound instead of 7.8%.

**Does not unblock:** the run itself. A run at 53 words is perfectly possible — it simply carries a
weaker bound, and the bound must be quoted honestly either way.

**Does not change:** the epistemic limit. Even at 90 words this is a binomial bound over
opportunities *this battery constructs*, conditional on its word list, operators and font. It is
never an estimate of a checker's universal true error rate, and more words do not make it one.

---

## Suggested handling

Eval proposes the Controller convert this into a Resources task only if the ≤5% bound is wanted.
It is genuinely optional: the alternative is to run at 53 words and report 7.8%. Eval has no view
on which is the better use of Resources' time, and has deliberately not gone looking for the
material itself.
