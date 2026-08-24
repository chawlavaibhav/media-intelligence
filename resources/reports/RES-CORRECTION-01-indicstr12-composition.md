# Correction 01 — what the Devanagari scene-text sources actually contain

**Date:** 25 Aug 2026 · **Trigger:** `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`,
treated as Controller-approved for correction.
**Scope:** descriptions only. **No file was reacquired, no hash recomputed, no integrity or rights
conclusion changed.**
**Reproduce every number below:** `python3 resources/scripts/verify_devanagari_composition.py`
(20 checks, all passing, reads only files already on disk).

---

## What was wrong

`resources/sources/src_indicstr12_devanagari.md` described the acquired material as:

> **Provided labels:** cropped word images with Unicode labels in per-image `*_gt.txt`

**That conflated two different things.** Cropped word images do exist — they are in fact the
*majority* of the files — but they are **not** what the `*_gt.txt` files label. Those files describe
full scene photographs, one line per text region.

**The original wording is preserved** in the source record under *Correction history*, and in this
report, rather than being quietly overwritten. Anyone who sized a task off the old description can
see exactly what changed and why.

## What the material actually is

Both Devanagari scene-text sources ship the **same two-part structure**: a set of full scene
photographs with region-level annotations, plus a much larger set of single-word crops cut from those
same photographs.

| | IndicSTR12 | IIIT-ILST |
|---|---:|---:|
| **Full scene photographs** (own annotation file) | 375 | 176 |
| — median size | 700×488 | 640×480 |
| — regions per photo | 1–98 (median 4, mean 7.2) | 1–64 (median 8) |
| — total annotated regions | 2,711 | 1,788 |
| **Single-word crops** | 2,713 | 1,215 |
| — median size | 68×41 | 65×44 |
| **Total media acquired** | **3,086** | **1,390** |

Annotation formats differ. IndicSTR12's `*_gt.txt` is tab-separated: region index, 8 polygon
coordinates, transcription. IIIT-ILST's `.xml` is PASCAL-VOC style with one `<object>` per region
carrying a bounding box and transcription.

## Why the distinction changes the work

**A cropped word and a scene photograph are different evaluation tasks.**

Given a crop, *"transcribe the text"* has one correct answer. Given a photograph containing up to 98
separate words, the same instruction has **no well-defined answer** unless you also say which region
and in what order. Eval reports hitting exactly this and working around it by selecting one region per
photograph and materialising a crop. That workaround was sound — and, as it turns out, was
reconstructing something the dataset already ships.

## Media acquired ≠ locally paired records

`downloaded_item_count` has always meant *media files*, and that is what it says. But
"3,086 images with Unicode labels in per-image `*_gt.txt`" could reasonably be read as "3,086 images
that have labels", which would oversize a task roughly eightfold. Both source records now state the
two counts separately.

| | IndicSTR12 | IIIT-ILST | Total |
|---|---:|---:|---:|
| Media files acquired | 3,086 | 1,390 | 4,476 |
| **Locally paired image + sidecar annotation** | **375** | **176** | **551** |
| Share | 12.2% | 12.7% | 12.3% |

A *paired record* means the photograph and its own annotation file are both present and the
annotation parses to at least one region. These figures reproduce Eval's exactly.

### But the crops are not unlabelled — and this matters for sizing

**A crop's filename encodes its parent photograph and its coordinates**, which map to exactly one
line of the parent's annotation.

- IndicSTR12: **2,711 of 2,713 crops (99.9%)** resolve to a transcription by polygon match.
- IIIT-ILST: **1,210 of 1,215 crops (99.6%)** resolve by bounding-box match.

Worked example — crop `verified_twice__hindi__cropped_images__185_11_305_294_401_294_401_394_305_394.jpeg`
carries parent `185`, region `11`, and 8 coordinates that match one line of `185_gt.txt` → `सोफा`.

**So "usable pool = 551" understates it, and the right number depends on the task:**

| Task shape | Usable items |
|---|---:|
| Transcribe one word (unambiguous) | **3,921 crops** |
| Read a whole scene (multi-region) | **551 photographs** |

For checker calibration — *can this model read Devanagari at all* — the crops are the more directly
usable form, and there are seven times as many. **This is an observation for Eval to act on or not.
Resources does not decide what Eval measures.**

## Overlap — two denominators, both correct

Same numerator, different denominators. Neither figure is wrong and they do not conflict.

| Denominator | Overlap | Share |
|---|---:|---:|
| All acquired IIIT-ILST images (1,390) | 173 | **12.4%** |
| Locally paired IIIT-ILST records (176) | 173 | **98.3%** |

**Why the first is right for the source:** 1,390 files were acquired and 173 of them are byte-identical
to IndicSTR12 files. As a statement about what is on disk, 12.4% is correct.

**Why the second is what a consumer feels:** a holdout can only contain records that can actually be
scored, which means paired ones. In that subset **only 3 records are genuinely unique to IIIT-ILST**.
For evaluation purposes the two CVIT releases are effectively one source.

Two further facts, both verified here:

1. **The 173 shared photographs are exactly IndicSTR12's complete Hindi-labelled scene set** — all
   173 of 173. The smaller dataset's Devanagari scene folder *is* the larger dataset's Hindi scene
   folder. Excluding shared files therefore removes 100% of IndicSTR12's Hindi scene material.
2. **No cropped word image is byte-identical across the two sources.**

### A caveat hash-based deduplication cannot catch

Point 2 above is easy to misread as "the crops are independent". They are not.

**1,205 of IIIT-ILST's 1,214 crops (99.3%) are cut from photographs that are shared with
IndicSTR12.** They are not byte-identical — different crop tooling, different filenames — so **no
fingerprint check will ever flag them**, including ours. But they depict the same regions of the same
photographs.

Anything treating IIIT-ILST crops as unseen material would be wrong, and the duplicate report would
not warn you. **BSTD remains the only genuine cross-lineage reserve.**

## Unchanged

Hashes, duplicate counts, integrity conclusions, rights, statuses, budgets, manifests and acquisition
method are all untouched. Rights remain **internal research and evaluation only**.
