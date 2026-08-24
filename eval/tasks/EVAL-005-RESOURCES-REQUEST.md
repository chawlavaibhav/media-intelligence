# Cross-stream request to Resources — Hindi lexical items for EVAL-005

**From:** Eval / Capability Lab · **Task:** EVAL-005 · **Date:** 25 Aug 2026
**Status: REQUEST, not an approved task.** Only the Controller can open a Resources task. Eval has
**not** gone looking for material, and must not.
**Severity tag:** `CROSS_STREAM`.

---

## The ask, in order

> **Step 1 — a check, not an acquisition.** Resources checks its existing legitimate local corpus
> and distributor label files for additional **unique Hindi lexical strings already in hand**.
>
> **Step 2 — only if step 1 falls short.** If the existing material cannot supply the shortfall,
> report the gap and stop. **New acquisition needs separate Controller authorisation** and is not
> requested here.

The likely shortfall is **~31–37 additional distinct Hindi lexical items** — words as plain text,
not images and not new annotations.

---

## Why this is now a check rather than a hunt

Resources PR #5 is **merged**. Its records establish something Eval could not see before:

| Source | Crop images | Transcription-resolvable |
|---|---:|---:|
| IndicSTR12 | 2,711 | **2,711** (100%) |
| IIIT-ILST | 1,214 | **1,213** |
| **Total single-word crops** | 3,925 | **3,924** |

Two independent resolution routes exist — a distributor-shipped crop-level label file, and
coordinates encoded in the crop filename matching a line of the parent scene annotation.

**Be precise about what that establishes.** It establishes that **recoverable labels exist** for
3,924 single-word crops. The **raw lexical strings themselves may still live only in the
git-ignored Resources corpus** — merged git state contains the counts and the method, not the
words. Eval cannot read `resources/corpus/raw/`, so how many *distinct* Hindi words those 3,924
crops actually yield is **unknown**. They may repeat one another and they may repeat the 53 already
in use.

That is exactly why step 1 is a check. It may cost nothing and close the gap entirely.

---

## Why the current pool is insufficient — the arithmetic

The battery's sizing figure is computed over **hard opportunities**: items where a corrupted word is
*drawn* and the checker is asked about the *real* word. That is where a model's language prior pulls
it toward answering "yes, that matches" — the production failure.

Two structural rules fix how many opportunities a word list yields:

1. **Every mismatch item sits on a distinct base word.** Four perturbations of one word are not four
   separate chances to catch a checker out, so counting them as such would inflate the apparent
   sample. One word, one opportunity.
2. **70% of the mismatch stratum is built in the hard direction**, the rest being controls.

| Validated base words | Hard opportunities | iid reference upper bound, zero false passes |
|---:|---:|---:|
| **53 — everything the repository has today** | **37** | **7.8%** |
| 84 | 59 | 4.95% |
| 90 | 63 | 4.6% |

⚠ **Read that last column carefully.** It is a **reference calculation under an assumption EVAL-005
does not establish** — that a checker's outcomes on these opportunities behave like independent,
identically distributed coin flips. Distinct base words reduce within-word correlation; they do not
make the opportunities iid. Errors may remain correlated across words, diacritics, failure classes
and lexical patterns.

So **more words tighten a calculation; they do not supply the assumption.** 84–90 words is a
**planning target** for bringing that reference figure below 5%. It is not proof that a checker errs
on fewer than 5% of real cases, and it must never be reported as such. The actual qualification gate
is deterministic — *zero false passes* — and needs no probability model at all.

## What the repository actually holds — checked against merged `main`

| Source in merged `main` | Distinct Hindi strings | Usable as base words? |
|---|---:|---|
| `eval/calibration/devanagari-v0/candidate-manifest.jsonl` | **53** | yes — already in use |
| `eval/calibration/devanagari-v0/annotator-disagreement.json` | ~50 | **no** — see below |
| `resources/manifests/corpus-pilot-v0.jsonl` (34,786 records) | 0 | no — every record carries `source_labels_ref: null` |
| Merged Resources records from PR #5 | 1 (a worked example) | no — they carry counts and method, not the lexicon |
| Raw corpus / distributor label files | **unknown, and the point of step 1** | not visible to Eval — `resources/corpus/raw/` is git-ignored |

**Why the disagreement file cannot be used**, even though it superficially looks like ~50 free
words: its strings are *specifically the contested ones* — regions where two dataset releases
assigned different transcriptions. At least one member of every pair is wrong by construction
(`सर्राफा` / `सरर्फि`, `शक्ति` / `शकती`), and several are Marathi rather than Hindi (`पोलीस`,
`ठाणे`). Using them would put non-words at the base of items whose whole premise is that the base is
a plausible real word.

---

## What Eval needs, precisely

| Requirement | Specification |
|---|---|
| **Quantity** | 31–37 additional items minimum; 40–50 preferred, because some will be rejected during reader validation |
| **Form** | **plain text strings**, one lexical item per record. Not images. Not crops. Not new annotations. |
| **Script** | Devanagari, in Unicode. Any encoding is fine; Eval normalises to NFC. |
| **Language** | **Hindi.** Marathi is a separate reserve and must not be substituted to make up the count. |
| **Word form** | single orthographic words preferred; short two-word phrases acceptable. No sentences, no punctuation-heavy strings, no numerals-only strings. |
| **Length** | 3–12 Devanagari characters. Shorter gives the perturbation operators too little to work on; longer makes a single-line render unwieldy. |
| **Distinctness** | distinct from each other **and** from the 53 already in use, after NFC. Duplicates add no opportunity. |
| **Feature coverage** *(desirable, not required)* | the battery covers 20 failure classes and the scarcest need specific features. Items containing **a nukta**, **a visarga (ः)**, **a chandrabindu (ँ)**, **a reph (र् before a consonant)** or **a rakar (्र)** are worth more than generic words, because those classes currently rest on 1–2 items each. |
| **Provenance** | each item carries its source and access date, per normal Resources bookkeeping. Eval records provenance per base word in the build manifest. |
| **Rights** | public and ungated is sufficient. `not_stated` / `not_verified` is acceptable under the existing Resources policy: the words are used **internally only**, never redistributed, not training data, not shipped to a customer. That judgement is Resources' to record, not Eval's. |

## Two hard constraints

**Do not treat the 3,924 recoverable crop labels as validated Hindi words.** They are *candidate*
lexical items with exactly the same status as the 53 already in use: one annotation team's
observation, reused as a lexicon rather than as ground truth about a photograph. Every candidate
still has to pass the planned Hindi lexical validation — *"is this a real, well-formed Hindi word as
written?"* — before it enters the battery. EVAL-003's finding that these annotations are unsafe as
ground truth stands, and a misread annotation may be a non-word.

**Do not use BSTD or the Marathi reserve to hit the count.** BSTD remains the only genuine
cross-lineage reserve — IndicSTR12 and IIIT-ILST are one evaluation lineage, confirmed twice over by
Resources (byte-level overlap among scene photographs, content-level overlap among crops: 1,205 of
1,214 IIIT-ILST crops come from photographs shared with IndicSTR12). Spending BSTD on a word list
would burn the only unseen source we have, to save a calculation that is a planning aid rather than
a result.

## What Eval does NOT need

- No images, crops or bounding boxes — the battery renders its own.
- No human transcriptions of photographs — what is on the page is known by construction.
- No agreement between annotators — irrelevant here.
- **No new download.** Step 1 is a check of what already exists.

---

## What this unblocks, and what it does not

**Unblocks:** a tighter reference calculation — 7.8% → below 5%.

**Does not unblock:** the run itself. A run at 53 words is possible; it simply reports the figure at
37 opportunities, honestly labelled.

**Does not change:** what the figure means. It is a sizing calculation under an assumption this
battery does not establish, at any word count.

---

## Suggested handling

Eval proposes the Controller ask Resources for **step 1 only** — a check of existing local material.
That may be cheap and may close the gap. If it does not, the shortfall is a separate Controller
decision about acquisition, and Eval has no view on whether it is worth Resources' time. Eval has
deliberately not gone looking for the material itself.
