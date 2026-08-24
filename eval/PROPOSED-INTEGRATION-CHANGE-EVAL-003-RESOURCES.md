# Cross-stream correction proposal — Eval → Resources

**From:** Eval / Capability Lab (EVAL-003 correction pass) · **To:** Controller, for Resources
**Date:** 24 Aug 2026 · **Severity:** CROSS_STREAM
**Status: PROPOSED. Eval has not edited any Resources file and will not.**

---

## What this is

While building the Devanagari calibration pack, Eval found that one description in a Resources
source record does not match the files that were actually acquired. Under the Runbook a stream never
edits another stream's evidence, so this is filed for the Controller to action rather than fixed in
place.

**Nothing about the acquisition itself is in question.** The files are present, validated and
correctly hashed. This is a description that will mislead the next reader.

---

## Point 1 — the discrepancy

**File:** `resources/sources/src_indicstr12_devanagari.md`

**Currently states:**

> **Provided labels:** cropped word images with Unicode labels in per-image *_gt.txt

**What the acquired files actually are:** full **scene photographs**, each carrying **multiple**
annotated text regions, with per-image `*_gt.txt` files in a tab-separated format of
`index, 8 polygon coordinates, transcription` — one line per region.

**Evidence, reproducible from the repository:**

- Annotated images carry **1 to 98 regions each**, median around 6.
- Example — `verified_twice__hindi__100_gt.txt` contains 6 regions with polygon coordinates and 6
  distinct transcriptions, for a single photograph of a shopfront.
- Image dimensions in the Resources manifest are full-scene (e.g. 465×617, 1659×1656), not
  word-crop dimensions.

The same applies to `src_iiit_ilst_devanagari`, whose per-image `.xml` files are PASCAL-VOC style
with multiple `<object>` entries per photograph. That record says "bounding boxes and
transcriptions", which is accurate — no correction proposed there.

---

## Why it matters to a consumer

**"Cropped word images" and "scene photographs with many regions" are different evaluation tasks.**

Given a cropped word, "transcribe the text" is unambiguous. Given a photograph containing 98 separate
words, it is not — there is no defined answer without also specifying *which* region and in what
order. A consumer who trusted the current description would design a task with no well-defined
correct answer, and would probably not discover this until results looked strange.

EVAL-003 handled it by selecting one region per photograph deterministically and materialising a
crop per item, but that only works because the discrepancy was noticed.

---

## Proposed correction *(Controller to apply, or direct Resources to)*

Amend the **Provided labels** line of `src_indicstr12_devanagari.md` to something like:

> **Provided labels:** full scene images with per-image `*_gt.txt` files carrying one line per text
> region — index, 8 polygon coordinates, Unicode transcription. Images contain 1–98 annotated
> regions each (median ~6). Not pre-cropped word images.

**Preserve the original line** rather than overwriting it, consistent with how this project has
handled other corrections, so anyone who relied on the earlier description can see what changed.

---

## Point 2 — distinguish acquired media from locally usable image+annotation pairs

**Observed.** Of the media acquired, only a minority carries an annotation file that can be paired
with an image locally:

| Source | Images acquired | **Locally paired image + annotation records** | Share |
|---|---:|---:|---:|
| `src_indicstr12_devanagari` | 3,086 | **375** | 12.2% |
| `src_iiit_ilst_devanagari` | 1,390 | **176** | 12.7% |
| **Total** | 4,476 | **551** | 12.3% |

A pairing is counted only where the image file and its annotation file are both present and the
annotation actually parses into at least one region — `<name>_gt.txt` beside `<name>.jpeg` for
IndicSTR12, `<name>.xml` beside `<name>.jpg` for IIIT-ILST.

**Why this is worth recording.** Nothing in the Resources records is incorrect — `downloaded_item_count`
is the count of media files, and that is exactly what it says. But a reader planning work that needs
transcriptions could reasonably read "3,086 images with Unicode labels in per-image `*_gt.txt`" as
"3,086 images that have labels", and size a task eightfold too large. EVAL-003 hit precisely this: the
usable Devanagari annotation pool is 551, not 4,476.

**Requested:** where the wording could imply that all acquired media carries a locally usable
transcription, distinguish **media acquired** from **locally paired image+annotation records**. The
partial member-level acquisition that produced this is already documented and is not in question.

## Point 3 — the overlap figure has two valid denominators

**Observed.** Of the **176 locally paired IIIT-ILST records**, **173 are byte-identical** to an
IndicSTR12 file — leaving **3 unique** in that subset (98.3%).

**This is not a contradiction of Resources' figure.** Resources reports 173 of 1,390 acquired
IIIT-ILST images = **12.4%**, which is correct for the full acquired source. The two numbers share a
numerator and differ in denominator:

| Denominator | Overlap | Share |
|---|---:|---:|
| All acquired IIIT-ILST images (1,390) — **Resources' figure** | 173 | **12.4%** |
| Locally paired IIIT-ILST records (176) — **the figure a consumer feels** | 173 | **98.3%** |

**Why the second one matters downstream.** A consumer holding out IIIT-ILST as unseen material can
only hold out records it can actually score, which means paired ones. In that subset the overlap is
near-total: **only 3 records are genuinely unique.** For calibration purposes the two CVIT releases
are effectively one source, which is why EVAL-003 treats BSTD as the only real cross-lineage reserve.

**Requested:** record both denominators explicitly, stating that they are consistent rather than
conflicting. No change to Resources' existing 12.4% figure is sought.

---

## What Eval is NOT asking for

- **No re-acquisition.** The material is exactly what calibration needs.
- **No rights reinterpretation.** Untouched and not in question.
- **No change to the overlap, duplicate or integrity findings**, all of which Eval independently
  reproduced and confirmed.
- **No change to Resources' conclusions.** Only this one description line.

## Related observation, offered without a request attached

EVAL-003 also found that **all 173 shared files are exactly the Hindi-labelled subset** — the smaller
dataset's Devanagari folder appears to *be* the larger dataset's Hindi folder. Resources correctly
reported the overlap; this is a consequence of it worth knowing, because it means the two collections
are far less independent than their separate names suggest.

It also has a concrete effect on Eval: excluding shared files removes **100% of Hindi-labelled
material**. The Controller has therefore approved admitting shared photographs **once** for the
Hindi-primary V0 calibration pack, so one photograph is one item and never two.

Eval has recorded the consequence for its own purposes in
`eval/calibration/devanagari-v0/PROPOSED-V0-COMPOSITION.md`. **Resources proposes; the Controller
decides** — and the same applies here in reverse.
