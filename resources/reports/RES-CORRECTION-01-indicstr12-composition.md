# Correction 01 — what the Devanagari scene-text sources actually contain

**Date:** 25 Aug 2026 · **Trigger:** `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`,
treated as Controller-approved for correction.
**Scope:** metadata/documentation plus a reproducible verifier. **No file was reacquired, no hash
recomputed, no integrity or rights conclusion changed.**
**Reproduce every number below:** `python3 resources/scripts/verify_devanagari_composition.py`
(44 checks, all passing, reads only files already on disk).

> **Revision 2, 25 Aug 2026 — count correction.** Revision 1 of this report gave crop counts that did
> not add up to the acquired media totals. Root cause and fix are in *"A second defect: the categories
> did not add up"* below. The substantive findings are unchanged; one of them got stronger.

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
| **Single-word crops** | 2,711 | 1,214 |
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

There are **two independent routes** to a crop's transcription.

**Route A — the distributor ships a crop-level label file.** This was missed in revision 1 precisely
because the flawed detector counted it as an image:

- IndicSTR12: `verified_twice__<lang>__cropped_images__word_image_gt.txt`, tab-separated
  crop-filename → transcription. **2,711 entries covering 100% of the 2,711 crops.**
- IIIT-ILST: `...__cropped__Devanagari__WordImagesList.txt`. **1,150 of 1,214 crops (94.7%).**

**Route B — the filename encodes the coordinates.** A crop filename carries its parent photograph,
region index and coordinates, which match exactly one line of the parent's scene annotation.

- IndicSTR12: **2,711 of 2,711 (100%)** by polygon match.
- IIIT-ILST: **1,210 of 1,214 (99.7%)** by bounding-box match.

Worked example — `verified_twice__hindi__cropped_images__185_11_305_294_401_294_401_394_305_394.jpeg`
carries parent `185`, region `11`, and 8 coordinates matching one line of `185_gt.txt` → `सोफा`.

**Union of both routes:**

| | crops | resolvable | unresolved |
|---|---:|---:|---:|
| IndicSTR12 | 2,711 | **2,711 (100%)** | 0 |
| IIIT-ILST | 1,214 | **1,213 (99.9%)** | 1 |
| **Total** | **3,925** | **3,924** | **1** |

The single unresolved file is named in the verifier output
(`IIIT-ILST__..._178_1_1_154_132_207_167.jpg`); its filename carries an extra token, so neither route
parses it. It is **reported, not hidden and not quietly reclassified.**

**So "usable pool = 551" understates it, and the right number depends on the task:**

| Task shape | Usable items |
|---|---:|
| Transcribe one word (unambiguous) | **3,924 crops** |
| Read a whole scene (multi-region) | **551 photographs** |

For checker calibration — *can this model read Devanagari at all* — the crops are the more directly
usable form, and there are seven times as many. **This is an observation for Eval to act on or not.
Resources does not decide what Eval measures.**

## A second defect: the categories did not add up

**Revision 1 of this report reported counts that could not all be true at once.** It gave IndicSTR12
as 375 scene photographs and 2,713 crop images, against 3,086 acquired media files — but
375 + 2,713 = **3,088**. IIIT-ILST had the same shape of error: 176 + 1,215 = **1,391** against 1,390
acquired.

**Root cause.** The crop detector matched on filename pattern alone, with no filter on file type. The
distributor stores each source's crop-level ground-truth file *inside the crop directory*, so those
annotation files matched the pattern and were counted as crop images:

| Source | Files wrongly counted as crop images | Bytes |
|---|---|---:|
| IndicSTR12 | `verified_twice__hindi__cropped_images__word_image_gt.txt` | 61,457 |
| IndicSTR12 | `verified_twice__marathi__cropped_images__word_image_gt.txt` | 98,590 |
| IIIT-ILST | `..._cropped__Devanagari__WordImagesList.txt` | 45,478 |

Two extra for IndicSTR12, one for IIIT-ILST — matching the discrepancies exactly.

**No media file was miscounted, gained or lost.** Three text files were misclassified as images. The
acquired-media totals of 3,086 and 1,390 were correct throughout and are unchanged.

**Why revision 1's verifier did not catch it.** It checked each count against an expected value, and
each count was individually defensible. Nothing checked that the categories formed a *partition* — that
they were disjoint and summed to the whole. The verifier now asserts exactly that, per source:

```
scene photographs + crop images == media files acquired    (exhaustive)
scene photographs & crop images == empty                   (disjoint)
every media file lands in exactly one category             (total)
```

**Resolvability is now reported separately and is explicitly not a media category.** "How many crops
exist" and "how many crops can be tied to a transcription" are different questions; collapsing them is
what produced the defect. They differ by exactly one file.

**The silver lining.** Chasing the two extra IndicSTR12 files is what surfaced the dedicated
crop-level label files — which turn out to be a cleaner and more authoritative route to crop
transcriptions than the coordinate inference of revision 1.

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
