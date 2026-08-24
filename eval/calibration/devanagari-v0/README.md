# Devanagari checker calibration pack — V0

**Task:** EVAL-003 · **Status: READINESS ONLY.** Nothing here has been run against a model, no human
has been asked to do anything, and no capability result exists.

---

## What this is

A prepared package that would let us answer one question: **can a candidate AI checker actually read
Devanagari from a real photograph?**

That question comes first. If a checker cannot read the script reliably, its verdicts about generated
Hindi text are worthless no matter how good the rest of the design is. Our founding study showed one
checker reporting six visibly misspelled signs as correct — the specific way these tools fail is by
being agreeable, so this has to be measured rather than assumed.

**What it is not:** not a benchmark of any image generator, not a measurement of any checker, and not
project ground truth about what any sign says.

---

## Contents

| File | What it is |
|---|---|
| `build-candidate-pool.py` | deterministic selector — rebuilds the pool from the corpus |
| `materialise-crops.py` | produces one crop file per item, with a self-test that **proves** crop geometry before writing anything |
| `_png.py` | dependency-free PNG read/write, used only so crop geometry can be verified |
| `crops/` | the crop files. **Both the reviewer and the checker read these**, so the region judged is identical by construction. Git-ignored; regenerate with `materialise-crops.py` |
| `PROPOSED-V0-COMPOSITION.md` | **decision record** — why the pack is Hindi-primary. Decided 24 Aug 2026; retained as reasoning, not an open question |
| `candidate-manifest.jsonl` | the 54 selected items, full provenance. **Contains source transcriptions — not for reviewer eyes** |
| `candidate-manifest.csv` | same, **without** transcriptions, safe to open alongside review work |
| `selection-summary.json` | exactly how the sample was chosen, and the reserve attestation |
| `annotator-disagreement.json` | evidence about label reliability (see below) |
| `build-review-pack.py` | generates the blinded reviewer pack, with a blinding self-check |
| `review-pack/` | what the Hindi reader would actually use |
| `human-response-template.csv` | machine-readable response template |
| `HUMAN-REVIEW-GUIDE.md` | operator guide for the reader |
| `CALIBRATION-RUN-PLAN-V0.md` | the full run plan, costs, and what a clean result would and would not license |

## Reproducing the committed V0 pack

**These are the commands that regenerate what is committed.** The builder's own defaults are
generic and will produce a *different* pack — the Hindi-primary arguments below are required.

```
CORPUS=<path-to>/resources/corpus/raw

python3 build-candidate-pool.py --corpus-root "$CORPUS"         --overlap-policy admit-once --language-filter hindi --target-n 54

python3 materialise-crops.py    --corpus-root "$CORPUS"
python3 build-review-pack.py    --verify-blind
```

Expected result: **173 eligible Hindi photographs, 54 selected, 54 distinct image hashes, 54 Hindi.**
`selection-summary.json` records the configuration actually used, so a mismatch is visible.

⚠️ **Do not run `build-candidate-pool.py` without those arguments and expect the committed pack.**
The script's generic default is `--overlap-policy exclude` with no language filter, which excludes
every shared photograph — and since all 173 Hindi photographs are shared, that default produces a
pack with **no Hindi at all**. The default is retained as generic machinery, not as the V0
configuration.

### Self-tests, which touch no corpus

```
python3 build-candidate-pool.py --self-test   # adversarial one-to-one region matching
python3 materialise-crops.py    --self-test   # crop geometry, on a synthetic image
```

`materialise-crops.py` refuses to materialise anything if its geometry test fails.

The raw corpus is git-ignored and may sit in another worktree, so `--corpus-root` is explicit.
Selection uses stable sorting on SHA-256, not a random number generator: the same repository state
and the same arguments always produce a byte-identical manifest.

---

## How the 54 were chosen

Starting material: two CVIT / IIIT Hyderabad collections of photographed Indian signage.

**Committed configuration (Controller-approved, 24 Aug 2026):**
`--overlap-policy admit-once --language-filter hindi --target-n 54`

| Step | Records |
|---|---:|
| Labelled source records | 551 |
| minus second copies of the 173 shared hashes (**admit-once**: each shared photograph is kept once) | −173 |
| minus same-source duplicate records | −3 |
| minus records outside the **hindi** language filter | −202 |
| **Eligible Hindi photographs** | **173** |
| **Selected** | **54** — all Hindi, 54 distinct hashes |

**Note the arithmetic.** Counts are **records**, not hashes. Under the earlier `exclude` policy each
shared hash removed **two** records (both copies), giving `551 − 346 − 3 = 202` — and zero Hindi.
Under `admit-once` each shared hash removes only the second copy.
| Selected across 12 difficulty strata | **54** |

**Only ~12% of the acquired images carry annotations at all** (551 of 4,476). That is a consequence
of Resources acquiring a partial slice of each archive, not an error. **173 eligible Hindi
photographs** is ample for a 54-item pack.

**Why the 173 shared photographs are admitted *once*.** They are literally the same photograph
distributed in both datasets, so admitting each twice would count one picture as two independent
tests. Admitting each **once** avoids that while keeping the material: the photograph is attributed
deterministically to one source record for provenance, and the two dataset names are **not** treated
as independent evidence about it.

This matters because **every Hindi-labelled photograph is a shared one** — all 173 of them. Excluding
shared files entirely, as the earlier configuration did, removes 100% of the Hindi.

**Independence is by file hash**, not by filename: one photograph, one item.

**Devanagari is detected by script in the transcription, never by language label.** Resources found
that ~5,100 images labelled `marathi` are written in Devanagari; filtering on language would have
discarded a fifth of the usable material.

The committed V0 pack then applies a **language filter on top of the script test**: all 54 items are
Hindi-labelled. Marathi-labelled material remains in the corpus and is eligible under a different
configuration, but it is **not** part of the primary V0 pack.

---

## The difficulty spread, and what it is not

The approved calibration plan says a set of clean, tidy examples is useless — if every candidate
checker scores the same, the test has separated nothing. So the pool is spread across 12 buckets
combining **region size** (tiny → large) and **scene clutter** (isolated → cluttered), 4–5 items each.

**Measured on the committed 54-Hindi pack** (recomputed, not carried over from the earlier pack):

| Property | Range across the 54 |
|---|---|
| Region area | 864 px² → 182,700 px² (a 211× spread; median 9,372) |
| Region share of frame | 0.11% → 37.1% (median 3.5%) |
| Regions in the source photo | 1 → 28 (median 3) |
| Transcription length | 3 → 12 characters (median 6) |
| Containing a conjunct | 20 of 54 |
| Containing a vowel sign | 53 of 54 |
| Containing a nukta | **1 of 54** |

**This is a spread, not a validated difficulty scale.** The buckets are convenience proxies chosen
because they are deterministic; nobody has shown that "small area" means "hard to read".

### What we could not measure

**Blur and contrast are not computed.** They are deterministic in principle, but this environment has
no image library (no Pillow, no numpy), so per-pixel statistics could not be calculated. They are
recorded as `null` with `pixel_metrics_state: not_computed_no_image_library` rather than guessed.

**Nukta coverage is effectively absent** — 1 item in 54, and only 1 region in 1,629 across the whole
eligible pool. This is a property of the corpus, not a bug: the check covers both the combining mark
and the precomposed forms. If nukta behaviour matters, this pool will not tell us about it.

**The pool is effectively single-source, and unavoidably so.** All 54 items are attributed to
IndicSTR12 — but every one of them is a photograph that appears in *both* CVIT releases. The
attribution is a deterministic provenance choice, **not** evidence that the item came from one
dataset rather than the other, and the two dataset names must not be counted as two sources. BSTD
remains the only genuinely independent lineage, and it is untouched.

---

## Two findings that change how the results must be read

### 1 · The two "independent" CVIT datasets are effectively one

173 files are byte-identical across them — and those 173 are **98% of everything IIIT-ILST has
labelled**. Only 3 labelled IIIT-ILST images are unique.

So the development material is one lineage, and **BSTD is the only genuine cross-source check we
have.** That is why it is held back untouched.

### 2 · The two dataset releases disagree with each other about a third of the time

> ⚠️ **Corrected 24 Aug 2026.** An earlier version of this section called this "expert annotators
> disagreeing" and treated 67% as a **human-performance ceiling**. **Both claims are withdrawn.**
> The repository holds no provenance showing who produced these annotations or whether the two sets
> were made independently. What is measured is *cross-dataset annotation disagreement between two
> releases from the same source lineage* — nothing about human reading ability, and nothing that may
> be used to set an evaluator threshold.

On the 173 shared photographs we compared the two releases' transcriptions of the **same physical
region**, matched **strictly one-to-one** (each region on either side matches at most once, pairs
accepted in descending IoU order, threshold 0.5):

| | |
|---|---:|
| Regions matched | 1,082 |
| Identical transcription | **725 (67.0%)** |
| Different transcription | **357 (33.0%)** |
| — identical after removing virama, nukta, anusvara, chandrabindu | 64 (18%) |
| — still different after that removal | 293 (82%) |

Same sign, same box: one release reads `मार्केट`, the other `माकेट`.

**On the diacritic figure.** Deleting those four marks is a mechanical Unicode operation. It does
**not** establish that such pairs are semantically or orthographically equivalent, or that they
represent the same reading — that needs native-language evidence this project does not have. The
field is named `matches_after_selected_diacritic_removal` so it cannot be read as more than it is.

**Matching-method audit.** The first pass chose a best partner independently for each region of one
dataset, without enforcing exclusivity, so one region could in principle have been counted against
several. That was a real methodological flaw. Recomputed strictly one-to-one, the figures are
**unchanged (725/1082 either way)** — because in this corpus the two releases' boxes are near-
identical rather than overlapping, and **0 of 1,778** regions were contested by more than one
partner. Both results are reported in `annotator-disagreement.json`.

**What this supports:**

**Source annotations are demonstrably unsafe to promote directly to project ground truth.** Two
releases from one lineage assign different transcriptions to the same pixels often enough that
adopting either arbitrarily would embed unexamined error. That is why the protocol establishes its
own reference with two independent readers.

**What this does not support:** any claim about human reading ability, any ceiling on achievable
accuracy, and any evaluator threshold.

The 173 overlap files are **excluded from the candidate pool** by default. They are kept as evidence
in `annotator-disagreement.json`.

**Caveat:** measured on the overlap set — the images one release reused — which may not be
representative of the wider pool.

### 3 · Every Hindi photograph is a shared photograph — and the pack is now Hindi-primary

**100% of Hindi-labelled records sit inside the cross-dataset overlap** (173 of 173). The smaller
dataset's Devanagari folder *is* the larger dataset's Hindi folder. So an `exclude` policy removes
every Hindi photograph. *(Historical, superseded: the pre-finalization `exclude` configuration
produced a pack of 53 Marathi + 1 unlabelled with no Hindi at all. That configuration is **not** the
committed V0 and must not be rebuilt as if it were.)*

**Controller decision, 24 Aug 2026: the primary V0 pack is Hindi-focused.** Shared photographs are
admitted **once** — one photograph, one item, never counted twice — and only Hindi-labelled items are
selected. The committed pack is **54 Hindi of 173 eligible Hindi candidates**.

The reason is that the checker prompt and our observed production failure are both Hindi-facing.
Spending the first human budget on a pack with no Hindi would have bought an avoidable transfer
assumption.

A result from this pack speaks to **reading Hindi from photographed signage**. It does **not**
automatically transfer to Marathi or to Devanagari-language use in general. The Marathi stress subset
is **deferred, not rejected** — see `PROPOSED-V0-COMPOSITION.md`, which is now a record of the
decision taken rather than an open question.

## What is deliberately held back

**BSTD (25,246 images) has never been opened.** This script counted its files by directory traversal
and read none of them. It is the unseen reserve for checking whether a checker transfers to a
genuinely different lineage.

Do not use BSTD's published train/test split as an independence guarantee — Resources found two
duplicate pairs crossing it.

**This is not the final benchmark split.** It is the V0 readiness structure.

---

## Status

Prepared, not performed. No human has transcribed anything, no checker has been run, no API call has
been made, and no Registry entry exists. Running it requires Controller approval of human time and
API spend — see `CALIBRATION-RUN-PLAN-V0.md` §5.
