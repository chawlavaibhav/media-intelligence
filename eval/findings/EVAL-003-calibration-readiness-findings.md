# EVAL-003 — Devanagari calibration readiness findings

**Date:** 24 Aug 2026 · **API spend:** ₹0 · **Human specialist time:** 0 hours
**External calls:** 0 · **Generators run:** 0 · **Capability results written:** 0

What the real Resources material turned out to be, what changed because of it, and what remains
uncertain.

---

## 1 · The two "independent" CVIT datasets are effectively one

**OBSERVED.** Resources reported 173 byte-identical files shared between IndicSTR12 and IIIT-ILST.
That is accurate, but the practical consequence is larger than the headline number suggests.

| | |
|---|---:|
| IIIT-ILST images carrying usable annotations | 176 |
| of those, byte-identical to an IndicSTR12 file | **173** |
| **unique labelled IIIT-ILST images** | **3** |

**INFERRED.** For calibration purposes the CVIT lineage is **one dataset, not two**. The selected
pool reflects this: 53 of 54 items come from IndicSTR12 and 1 from IIIT-ILST.

**What changes.** BSTD is not merely the *preferred* cross-source reserve — it is the **only** one.
Any later claim that a checker "transfers across sources" rests entirely on BSTD, and there is no
second opinion available if BSTD turns out to be unrepresentative.

---

## 2 · The two dataset releases disagree about a third of the time

> ### ⚠️ Correction — 24 Aug 2026, Controller review
>
> The first version of this section described this as **"two independent expert annotation teams"**
> disagreeing, and presented 67% as a **human-performance ceiling** that should bound any evaluator
> threshold. **Both claims are withdrawn.** They were not supported by anything in this repository.
>
> What the repository actually contains: two dataset releases from the **same source lineage**
> (CVIT / IIIT Hyderabad), each with manual annotations. There is **no provenance** establishing who
> produced them, whether the annotators were independent of one another, or whether the later release
> re-annotated or inherited from the earlier one. Two releases from one lab are not a controlled
> inter-annotator study.
>
> **Corrected description:** *cross-dataset annotation disagreement between two releases from the
> same source lineage.*
>
> **Consequences of the correction:** the figure is **not** a human-performance ceiling, and it
> **must not** be used to set an evaluator threshold. The original wording is preserved above so the
> correction is visible.

**Method (deterministic, no Hindi judgement made).** Regions matched geometrically at IoU ≥ 0.5,
**strictly one-to-one** — pairs sorted by descending IoU and accepted greedily, each region on either
side matching at most once. Transcriptions NFC-normalised and compared exactly.

**OBSERVED:**

| | |
|---|---:|
| Regions matched (one-to-one) | 1,082 |
| Identical transcription | **725 (67.0%)** |
| Different transcription | **357 (33.0%)** |

Examples, same photograph and same box: `सर्राफा`/`सरर्फि` · `मार्केट`/`माकेट` · `झेरोक्स`/`झारक्स`.

### 2.1 Matching-method audit

The first pass chose a best partner **independently for each region** of one dataset with **no
exclusivity**, so one region of the other dataset could in principle have been counted against
several. That was a genuine methodological flaw and the Controller was right to flag it.

**Recomputed strictly one-to-one, the figures are identical: 725/1082 either way.**

The reason is a property of this corpus, measured rather than assumed: **0 of 1,778** regions in the
other dataset were within threshold of more than one partner. The two releases' boxes are
near-identical rather than merely overlapping, so the flawed method had no opportunity to
double-count here.

**Both results are reported** in `annotator-disagreement.json` under `matching_method` and
`superseded_method`, so the correction is visible rather than silently overwritten. The flaw was
real; its effect on this data was nil. A different corpus could easily have differed.

### 2.2 The diacritic probe, renamed

The first version stripped virama, nukta, anusvara and chandrabindu and labelled the resulting
matches **"spelling convention only"**. **That interpretation is withdrawn** — a Unicode deletion
cannot establish a linguistic equivalence.

Renamed to `matches_after_selected_diacritic_removal`, with the four marks named explicitly
(U+094D, U+093C, U+0902, U+0901). **64 of 357** disagreements match after that removal.

**What that means:** those pairs become identical once those four marks are deleted from both. **What
it does not mean:** that they are semantically or orthographically equivalent, or represent the same
reading. Establishing that needs native-language evidence this project does not have.

### 2.3 What the finding does and does not support

**Supported, and it is the important part:** **source annotations are demonstrably unsafe to promote
directly to project ground truth.** Two releases from one lineage assign different transcriptions to
the same pixels often enough that adopting either arbitrarily would embed unexamined error. This is
why the protocol establishes its own reference, and why it now uses **two independent readers**
rather than one.

**Not supported:** any claim about human reading ability, any ceiling on achievable accuracy, and any
evaluator threshold derived from 67% or 73%.

**Limit.** Measured on the overlap set — images one release reused — which may not be representative.

## 3 · Annotation coverage is ~12%, not 100%

**OBSERVED.** Of 4,476 acquired CVIT images, **551 carry usable annotations** (375 IndicSTR12,
176 IIIT-ILST).

**Why.** Resources performed member-level partial acquisition — 8.1% of one archive — so label files
are sparse relative to images. Not an error; a consequence of a deliberate, budget-respecting
acquisition.

**What changes.** Nothing blocking. Under the committed V0 configuration **173 eligible Hindi
photographs** remain, ample for the 54-item pack. But any later plan assuming "4,476 labelled Devanagari images are available"
would be wrong by roughly eight-fold.

---

## 4 · What the material actually is — not cropped words

**OBSERVED.** Resources' note described IndicSTR12 as "cropped word images". On disk these are
**full scene photographs with multiple annotated text regions** — 1 to 98 regions per image, median
around 6, carrying bounding boxes and per-region transcriptions.

**What changes.** "Transcribe the Devanagari text in this image" is ambiguous when a photograph
contains 98 separate words. The pipeline therefore selects **one region per photograph**
deterministically (largest area, then position, then lexicographic) and records its box, so the task
put to both reader and checker is a single unambiguous word.

**Crops are materialised, with proven geometry** *(this paragraph previously said crops were
deliberately not materialised; that was true of the first pass and is no longer the current state —
see §11.7)*. `materialise-crops.py` writes one crop per item, and **the reviewer and the checker read
the same files**, verified by hash across all 54 items. Geometry is proven by a self-test on a
coordinate-encoded synthetic image, which also caught a real `sips` defect at the image origin.

---

## 5 · The candidate pool

**Deterministic and reproducible.** Selection uses stable sorting on SHA-256, not a random number
generator. Two consecutive runs produced byte-identical manifests (verified).

**Committed V0 configuration:** `--overlap-policy admit-once --language-filter hindi --target-n 54`.

| Step | Records |
|---|---:|
| Labelled source records | 551 |
| less second copies of the 173 shared hashes (**admit-once** keeps each photograph once) | −173 |
| less same-source duplicate records | −3 |
| less records outside the **hindi** language filter | −202 |
| **Eligible Hindi photographs** | **173** |
| **Selected** | **54** — all Hindi, 54 distinct hashes |

**Counts are records, not hashes.** Under the superseded `exclude` configuration each shared hash
removed **two** records (both copies), giving `551 − 346 − 3 = 202` eligible **and zero Hindi**. That
configuration is historical; do not present it as the current pool.

Spread across 12 strata (region size × scene clutter), 4–5 items each. Region area spans 528 px² to
388,480 px² — a 735× range — and regions occupy 0.21% to 65.7% of their frame.

**Devanagari was detected by script in the transcription, never by language label**, per Resources'
finding that ~5,100 Marathi-labelled images are written in Devanagari.

**Verified:** all 54 selected SHA-256 values are distinct — one photograph, one item. Under the
committed V0 configuration shared photographs are **admitted once** rather than excluded, which is
required because every Hindi-labelled photograph is a shared one; the guarantee enforced is that no
photograph can enter **twice**, not that shared photographs are absent.

**Gap: nukta coverage is effectively absent** — 1 item in 54, and 1 region in 1,629 across the whole
eligible pool. The check covers both the combining mark U+093C and the precomposed forms
U+0958–U+095F, so this is a corpus property, not a detection failure. If nukta handling matters, this
pool will not tell us about it.

**Not measured: blur and contrast.** Deterministic in principle but not computable without an image
library. Recorded as `null` with `pixel_metrics_state: not_computed_no_image_library` rather than
invented — the approved plan explicitly permits marking rather than guessing.

---

## 6 · BSTD remains untouched

**OBSERVED.** 25,252 files present; counted by directory traversal; **none opened, read, decoded,
inspected or selected.** The builder records this attestation in `selection-summary.json` on every
run, and the reserve directory is not referenced anywhere else in the pipeline.

Resources' warning is carried forward: **do not treat BSTD's published train/test split as an
independence guarantee** — two duplicate pairs cross it.

---

## 7 · Per-item targets, with judgement provably unchanged

**The limitation.** `check-vlm.mjs` assumed one target string for an entire run. Real calibration
items each say something different.

**What changed.** A second input mode, `--items <file.jsonl>`, where each record carries
`{id, image, target}`. The original single-target mode is preserved unchanged; the two are mutually
exclusive and combining them is rejected.

**What did not change.** Both modes normalise to one work list and pass through the *same*
`scoreTranscription(raw, target)` call. The predicate is identical — only where the target comes
from differs.

**Evidence, not assertion.** All **27 stored historical transcriptions** were re-scored through
**both** code paths and compared against the stored verdicts: **0 mismatches.** This is wired into
`node eval/harness/run-fixture.mjs --selftest` so a future change that breaks it fails loudly.

**Malformed input is rejected, not silently skipped** — a skipped item would quietly change what a
calibration run measured. Five fixtures cover it, each rejected with a named reason:

```
items-valid.jsonl                       -> accepted
items-malformed-missing-target.jsonl    -> rejected: record 2: missing required field 'target'
items-malformed-duplicate-id.jsonl      -> rejected: record 2: duplicate id 'fx-dup'
items-malformed-missing-image.jsonl     -> rejected: record 1 (id 'fx-noimg'): image not found
items-malformed-bad-json.jsonl          -> rejected: line 2 is not valid JSON
```

---

## 8 · Blinding is mechanically verified, not merely intended

The reviewer pack contains **only** item ID and a reference to the materialised crop file (name,
hash, dimensions). `--verify-blind` re-reads every generated file and fails if any Devanagari
character appears anywhere.

**Result: no Devanagari character exists anywhere in the generated pack.** Independently re-checked.

**Why it matters.** The auto-correction pull that made one AI checker report six misspelled signs as
correct acts on people too. A reader shown an expected answer and asked "does this match?" will tend
to see a match. The measured 33% cross-dataset annotation disagreement is a second reason: an
independent reading is only worth having if it was actually made independently.

**Canonical crop files are materialised locally**, and the reviewer interface and the checker input
both reference those same files — verified identical by hash across all 54 items. Equivalence is by
identity rather than by two computations agreeing. The crops are derived output: git-ignored, and
regenerated deterministically by `materialise-crops.py` from the manifest plus the verified crop
geometry. *(An earlier configuration displayed a browser-side crop of the original and copied no
images; that is superseded — see §11.7.)*

---

## 9 · What remains uncertain

- ~~Whether crops can be materialised correctly~~ — **RESOLVED.** Crop geometry is proven by
  self-test against a coordinate-encoded synthetic image, the reviewer and checker read byte-identical
  files, and the tool refuses to run if the geometry test fails. See §11.7.
- **How many of the 54 survive the reader.** The pool is oversized precisely because this is unknown.
  A high rejection rate is a fact about the material, to be reported rather than worked around.
- **Whether deterministic "broken" targets are genuinely broken.** A string edit can accidentally
  produce another real word, or the correct reading of an ambiguous crop. Confirming this is a
  Hindi-language judgement, deliberately deferred to a separate short pass **after** the blind pass
  is frozen.
- **Whether reading ability predicts judging generated text.** It does not follow. Generated text
  fails differently — often clean-looking but semantically wrong. This screen is necessary, not
  sufficient.
- **Whether the difficulty strata mean anything.** They are deterministic proxies, not a validated
  scale.
- **Whether the 33% disagreement generalises** beyond the overlap set.

---

## 10 · Stop conditions — none fired

No EVAL-003 or `shared/AUTONOMY-POLICY.md` stop condition triggered.

Specifically: the CVIT material **did** produce a varied independent pool (173 eligible Hindi
photographs, 54 selected across 12 strata); the duplicate structure was as Resources reported, with the additional consequence
in §1 recorded rather than improvised around; source transcriptions joined to images cleanly through
the documented annotation formats, needing no new interpretation rule; per-item targets did **not**
change judgement semantics (§7, verified); no native-Hindi judgement was required or made — the one
place it would have been needed (§9, broken-target validity) was deferred rather than invented; no
new evaluator was needed; the approved calibration plan proved internally consistent against real
material, and §2 supplies a number for a rule it already contained; and no external call, paid step
or human work occurred.

---

## 11 · Correction pass — 24 Aug 2026, after Controller review

Ten corrections. Two were substantive overclaims of mine; one exposed a real defect in an
external tool; the rest tighten accuracy.

**11.1 · Overclaim withdrawn — "expert teams" and the "ceiling".** §2. I described two dataset
releases as independent expert annotation teams and turned their disagreement into a human-performance
ceiling for evaluator thresholds. Nothing in the repository supports either. Corrected throughout,
with the supported conclusion — source annotations are unsafe to adopt as ground truth — retained.

**11.2 · Matching audited and corrected.** §2.1. Strict one-to-one matching implemented; both old and
new results reported. Figures unchanged here (725/1082), because 0 of 1,778 regions were contested —
the flaw was real, its effect on this corpus nil.

**11.3 · "Convention only" renamed.** §2.2 → `matches_after_selected_diacritic_removal`, marks named.

**11.4 · Candidate arithmetic fixed.** §5 — stated in records rather than hashes. *(The figure at
that time was `551 − 346 − 3 = 202` under the then-current `exclude` configuration; the committed V0
arithmetic is in §12.)*

**11.5 · Language composition measured, and it is a problem.** The pool is **53 Marathi, 1 unlabelled,
0 Hindi** — because **all 173 Hindi-labelled records sit inside the excluded overlap**. The smaller
dataset's Devanagari folder *is* the larger one's Hindi folder, so deduplication removes every Hindi
photograph.

This matters because the defect we are hunting is a **language-prior** failure: a model reads toward
the plausible *word*, which is how one checker passed six misspelled Hindi signs. A model's Hindi
prior is generally stronger than its Marathi prior, so a Marathi-only pool may **under-detect the
exact failure we care about** — while our production failure is Hindi and the checker prompt says
"Devanagari (Hindi) text". *(That the prior differs is a reasonable expectation, not something
measured here.)*

Options in `PROPOSED-V0-COMPOSITION.md`, including an implemented `--overlap-policy admit-once` that
yields **19 Hindi / 35 Marathi** while keeping one photograph to one item (verified: 54 items, 54
distinct hashes). **Default unchanged pending a Controller decision.**

**11.6 · Human protocol now uses two independent readers.** The single-reader design would have made
one person's transcription the answer key, with no way to distinguish a confident misreading from a
correct one — every checker that read such an item correctly would have been scored wrong. Now: two
blind readers; exact agreement becomes reference material; disagreements are excluded from the hard
gate or adjudicated and **reported**; neither reader alone is ground truth; and the later
broken-target confirmation may not be done by the reader who established that item's reading.
**Cost roughly doubles to ≈ 3.5–4.5 hours.**

**11.7 · Crop materialisation solved, and it caught a real defect.** `materialise-crops.py` writes one
crop per item; **the reviewer and the checker now read the same files**, verified by hash across all
54 — equivalence by identity rather than by two computations agreeing.

Geometry is proven by self-test: a synthetic image where every pixel encodes its own coordinates is
cropped and decoded with a dependency-free PNG reader written for the purpose. **That test found that
`sips --cropOffset 0 0` is silently treated as "no offset" and returns a CENTRE crop** — so any region
at the exact image origin would have been wrong, invisibly. A flip-crop-flip workaround handles it and
the self-test covers it. The script refuses to run if the self-test fails.

**11.8 · Machine-specific paths removed.** Generated metadata now records repo-relative paths.

**11.9 · Cross-stream correction filed, not applied.**
`eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md` — the IndicSTR12 record describes "cropped
word images"; the acquired files are full scene photographs with 1–98 annotated regions each. **No
Resources file was edited.**

**11.10 · A defect this pass introduced and caught.** While restructuring the builder, a block
replacement silently deleted the manifest and report writes, leaving stale pre-correction outputs on
disk while the script still appeared to succeed. Caught by checking the generated files for the new
field names rather than trusting the run. Restored and re-verified. Recorded because the same class
of error — a program that reports success while writing nothing — is exactly what the harness
integrity checks exist to catch elsewhere.

---

## 12 · Finalization pass — 24 Aug 2026

**Controller decision: the primary V0 pack is Hindi-focused.** The correction pass established that
the `exclude` policy produced a pack with **no Hindi at all**, because all 173 Hindi-labelled records
are shared photographs. The Controller approved admitting shared photographs **once** and selecting
Hindi-labelled items only.

**Result — no shortfall:** **173 eligible Hindi photographs, 54 selected, 54 distinct hashes, 54
Hindi.** A shortfall guard exits non-zero rather than substituting Marathi; it did not fire.
Arithmetic: `551 − 173 (admit-once) − 3 (same-source dupes) − 202 (language filter) = 173`.

Every Hindi photograph is a shared photograph, so nothing here claims two independent sources for
these items. The Marathi stress subset is **deferred, not rejected**, and would need Marathi-competent
readers and a separately reported result.

**Adversarial matching regression added.** §2.1 previously leaned on the real-corpus observation that
no partners were contested. That is not evidence the matcher is correct — it is evidence this corpus
never exercised the bug. `build-candidate-pool.py --self-test` now constructs the case the corpus
lacks: two A-regions both above threshold against, and both preferring, the same B-region. The
superseded rule matches both; the corrected rule uses that B-region once. Ten assertions, all passing.
The `0 of 1,778` figure is now computed by `count_contested_partners` and recorded in
`annotator-disagreement.json`, with an explicit note that zero contested partners is a property of
this data and not a validation of the superseded rule.

**Stage-4 protocol corrected.** The rule "not checked by the reader who established that item's
reading" was **impossible**: both readers read every item, so nobody was eligible, and satisfying it
would have required a third specialist. Withdrawn. **Either reader may perform the altered-target
check**, because by then the reference is frozen and the check cannot edit or replace it. Doubt drops
the item; the checker's identity is recorded. No third reader, no extra budget.

**Human time under the two-reader protocol: ≈ 3.5–4.5 hours**, readers **Hindi-competent**.

**Stale current-state prose removed.** Corrected in place: crops-not-materialised in §4; the
one-reader protocol; the impossible stage-4 rule; "the pool contains no Hindi" as current state; and
wording implying Hindi competence covers Marathi. Correction history is retained in marked sections
so the trace survives without leaving a followable obsolete instruction.

**Resources proposal completed** with all three required points, including the locally-paired-record
counts (551 of 4,476) and the two valid overlap denominators (12.4% of the full source, 98.3% of the
locally paired subset — consistent, not contradictory). No Resources file was edited.

**Verification:** builder determinism, 54/54 distinct hashes, 54 Hindi, adversarial regression 10/10,
crop geometry 8/8, crop-hash identity across reviewer and checker 54/54, blind-pack scan clean,
**27/27 historical checker cases with 0 judgement mismatches**, harness suites green, no absolute
paths, BSTD untouched at 25,252 files, and no human/API/model/generator work.
