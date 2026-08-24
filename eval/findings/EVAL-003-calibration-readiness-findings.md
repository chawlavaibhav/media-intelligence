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

## 2 · Expert annotators disagree about a third of the time — the headline finding

The 173 shared files are the only place in this corpus where two independent expert teams
transcribed the *same pixels*. That makes them measurable.

**Method (deterministic, no Hindi judgement made).** Regions were matched geometrically at
IoU ≥ 0.5, so "the two teams annotated different words" is excluded; only same-region comparisons
count. Transcriptions were NFC-normalised and compared exactly.

**OBSERVED:**

| | |
|---|---:|
| Same-region comparisons | 1,082 |
| Identical transcription | **725 (67.0%)** |
| Different transcription | **357 (33.0%)** |

Decomposing the 357 using pure Unicode operations:

| Category | n | Share of disagreements |
|---|---:|---:|
| Identical once virama/nukta/anusvara/chandrabindu are removed — same letters, different convention | 64 | 17.9% |
| Differ by one character | 155 | 43.4% |
| Differ by two characters | 86 | 24.1% |
| Differ by three or more | 52 | 14.6% |

Examples, same photograph and same box (IoU 1.0):
`सर्राफा`/`सरर्फि` · `मार्केट`/`माकेट` · `झेरोक्स`/`झारक्स` · `रामनारायन`/`रामनारायण`

**Even treating every convention difference as agreement, agreement is ~73%.** Substantive
disagreement — actually different letters — is ~27% of same-region comparisons.

**INFERRED, and this is what matters:**

1. **"Source labels are not ground truth" is now measured, not asserted.** The Project Contract's
   standing rule has a number behind it for this material.
2. **Our Hindi reader's transcription will also be one reading.** The record must say "as read by X
   on date Y", not "this is what the sign says".
3. **There is a ceiling on any checker score.** Requiring a machine to agree with one reader more
   often than another qualified reader would is demanding something no human achieves here.

**This does not contradict the approved calibration plan** — it instantiates a rule that plan already
contains ("an instrument threshold may never exceed the measured inter-annotator agreement"). It
supplies the number.

**Limit.** The 33% is measured on the overlap set — images one lab chose to reuse — which may not be
representative of the wider pool. And whether any specific pair is a misreading or a legitimate
alternative reading is a Hindi-language judgement, deliberately **not** made here.

---

## 3 · Annotation coverage is ~12%, not 100%

**OBSERVED.** Of 4,476 acquired CVIT images, **551 carry usable annotations** (375 IndicSTR12,
176 IIIT-ILST).

**Why.** Resources performed member-level partial acquisition — 8.1% of one archive — so label files
are sparse relative to images. Not an error; a consequence of a deliberate, budget-respecting
acquisition.

**What changes.** Nothing blocking: after exclusions, **202 eligible independent photographs** remain,
ample for a 45–60 pool. But any later plan assuming "4,476 labelled Devanagari images are available"
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

**Deliberately not done: crops were not materialised.** The only image tool available here is macOS
`sips`, whose crop-offset semantics could not be verified without pixel inspection (no Pillow, no
numpy). Silently mis-cropping would mean a reader and a checker judging the wrong region — a
correctness failure invisible in every artifact. The manifest carries the box; the review pack
renders the crop in-browser from the untouched original; **materialising crops for the checker is
recorded as a prerequisite the approved run must implement and verify.**

---

## 5 · The candidate pool

**Deterministic and reproducible.** Selection uses stable sorting on SHA-256, not a random number
generator. Two consecutive runs produced byte-identical manifests (verified).

| Step | Count |
|---|---:|
| Labelled CVIT images | 551 |
| less byte-identical across the two datasets | −173 |
| less duplicate copies within one dataset | −3 |
| **Eligible independent photographs** | **202** |
| **Selected** | **54** |

Spread across 12 strata (region size × scene clutter), 4–5 items each. Region area spans 528 px² to
388,480 px² — a 735× range — and regions occupy 0.21% to 65.7% of their frame.

**Devanagari was detected by script in the transcription, never by language label**, per Resources'
finding that ~5,100 Marathi-labelled images are written in Devanagari.

**Verified:** no excluded overlap file entered the pool; all 54 selected SHA-256 values are distinct.

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

The reviewer pack contains **only** item ID, source image path and crop box. `--verify-blind`
re-reads every generated file and fails if any Devanagari character appears anywhere.

**Result: no Devanagari character exists anywhere in the generated pack.** Independently re-checked.

**Why it matters.** The auto-correction pull that made one AI checker report six misspelled signs as
correct acts on people too. A reader shown an expected answer and asked "does this match?" will tend
to see a match. The measured 33% annotator disagreement is a second reason: a third reading is only
worth having if it was made independently.

No images are copied or transformed — the viewer crops from the original at display time, so storage
cost is zero and there is no transformed-file provenance risk.

---

## 9 · What remains uncertain

- **Whether crops can be materialised correctly** for the checker stage. Unresolved by choice; the
  approved run must implement and verify it.
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

Specifically: the CVIT material **did** produce a varied independent pool (202 eligible, 54 selected
across 12 strata); the duplicate structure was as Resources reported, with the additional consequence
in §1 recorded rather than improvised around; source transcriptions joined to images cleanly through
the documented annotation formats, needing no new interpretation rule; per-item targets did **not**
change judgement semantics (§7, verified); no native-Hindi judgement was required or made — the one
place it would have been needed (§9, broken-target validity) was deferred rather than invented; no
new evaluator was needed; the approved calibration plan proved internally consistent against real
material, and §2 supplies a number for a rule it already contained; and no external call, paid step
or human work occurred.
