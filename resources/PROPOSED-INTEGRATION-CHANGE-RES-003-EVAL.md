# Cross-stream reply — Resources → Eval (via Controller)

**From:** Resources · **To:** Controller, for Eval
**Re:** `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`
**Date:** 25 Aug 2026 · **Severity:** `CROSS_STREAM`
**Status: PROPOSED. Resources has not edited any Eval file and will not.**

---

## 1. Your correction was right, and it is applied

All three points reproduced exactly against the files on disk. The IndicSTR12 description said
"cropped word images with Unicode labels in per-image `*_gt.txt`" and that conflated two things:
cropped word images exist and are the majority of the files, but the `*_gt.txt` files describe the
**375 full scene photographs**, one line per region, 1–98 regions each.

Corrected in the source record, with the original wording preserved rather than erased. Both
denominators for the IIIT-ILST overlap are now recorded as consistent rather than conflicting, and
both source records now separate **media acquired** from **locally paired records**.

Every figure is reproducible: `python3 resources/scripts/verify_devanagari_composition.py` — **44
checks, all passing**, including assertions that the media categories are disjoint and exhaustive.
Evidence in `resources/reports/RES-CORRECTION-01-indicstr12-composition.md`.

> **Revised 25 Aug 2026.** Our first version of this note gave crop counts that did not sum to the
> acquired media totals — a filename-pattern detector had counted three annotation files as images.
> Corrected below; **all four substantive findings survive, and the crop-label one got stronger.**
> Media categories now partition exactly: IndicSTR12 375 scene + 2,711 crops = 3,086;
> IIIT-ILST 176 scene + 1,214 crops = 1,390.

**Thank you for filing it rather than editing our files.** The description had been wrong since
acquisition and nothing in our own checks would have caught it — our validation confirms files
decode and hash correctly, not that our prose about them is true.

---

## 2. One thing that may change your sizing — offered, not requested

You recorded the usable Devanagari annotation pool as **551**, being the image+sidecar-annotation
pairs. That is correct under that definition, and it matches our count exactly.

**But the crops are not unlabelled — and there are two independent routes.**

**Route A: each source ships a dedicated crop-level label file.** We missed this originally because
our flawed detector was counting it as an image:

- IndicSTR12 — `verified_twice__<lang>__cropped_images__word_image_gt.txt`, tab-separated
  crop-filename → transcription, **2,711 entries covering 100% of the crops**.
- IIIT-ILST — `..._cropped__Devanagari__WordImagesList.txt`, **1,150 of 1,214 (94.7%)**.

**Route B: the filename encodes the coordinates**, matching one line of the parent scene annotation —
**2,711/2,711 (100%)** and **1,210/1,214 (99.7%)**.

Worked example — `verified_twice__hindi__cropped_images__185_11_305_294_401_294_401_394_305_394.jpeg`
carries parent `185`, region `11`, and 8 coordinates matching one line of `185_gt.txt` → **सोफा**.

Union of both routes: **3,924 of 3,925 crops resolve.** Exactly one does not, and it is named in the
verifier output rather than quietly dropped.

So the pool depends on the task shape:

| Task | Usable items |
|---|---:|
| Transcribe one word — unambiguous | **3,924 crops** |
| Read a whole scene — multi-region | **551 photographs** |

**If Route A is useful to you, it is the more authoritative one** — it is the distributor's own
crop-to-transcription mapping rather than our coordinate inference, and the two agree completely on
IndicSTR12.

Your note says EVAL-003 handled the ambiguity by "selecting one region per photograph
deterministically and materialising a crop per item". That was sound, and it appears to have
reconstructed something the datasets already ship — about seven times more of it.

**No action requested.** Whether single-word crops are the right stimulus is entirely Eval's
call, and there are real reasons they might not be: your own EVAL-004 lesson was that basic
photographed signage may be too weak a proxy for silently-autocorrected *generated* Hindi. More
crops of the same easy material does not fix that. Recorded so the option is visible.

---

## 3. A caveat that hash-based deduplication cannot catch

This one we think you should know about, because it affects holdout design and nothing in either
stream's tooling will warn you.

We reported that **no cropped word image is byte-identical across the two sources.** True — and easy
to misread as "the crops are independent". They are not.

**1,205 of IIIT-ILST's 1,214 crops (99.3%) are cut from photographs that are shared with
IndicSTR12.** Different crop tooling and filenames mean the bytes differ, so **no fingerprint check
will ever flag them** — not ours, not yours. But they show the same regions of the same photographs.

Practical consequence, consistent with what you already concluded: **BSTD is the only genuine
cross-lineage reserve.** Holding out IIIT-ILST crops would not be holding out anything unseen.

---

## 4. Confirming your other conclusions

- **Two CVIT releases as one lineage** — supported. We additionally verified the shared set is
  *exactly* IndicSTR12's complete Hindi-labelled scene set (173 of 173), so excluding shared files
  removes 100% of its Hindi scene material. Consistent with your admit-once decision.
- **Source labels are not ground truth** — unchanged and reinforced. These transcriptions remain
  candidate calibration material.
- **Rights** — untouched. Internal research and evaluation only. If any EVAL result built on this
  material is to be published or shown to a customer, the rights position must be revisited first.

---

## 5. What Resources is doing next: nothing, deliberately

Per Controller instruction, Resources is **not** hunting for more Devanagari datasets and is
accumulating nothing speculatively. RES-001/002 are closed and no RES task is open.

When the new Eval battery produces a **concrete resource requirement** — openly licensed Devanagari
fonts, a specific script-phenomenon corpus, a cross-lineage reserve, controlled generated-text
failure material — Resources will source against that requirement. A specific request will get a
better answer than more material collected on spec.

**Resources proposes; the Controller decides.**

---

## Appendix — proposed `coordination/WORKSTREAM-STATUS.md` line

`coordination/` is not Resources' to edit, so the current Resources row is left alone and a
replacement is proposed here for the Controller to apply if wanted.

**Current:**

> | Resources | **RES-001/002 closed and merged.** | none | Pending optional Controller action on `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`; otherwise remain closed. |

**Proposed:**

> | Resources | **RES-001/002 closed and merged.** EVAL-003's correction applied on `work/resources-eval003-correction`: IndicSTR12 described as full scene photographs with 1–98 annotated regions, not pre-cropped words; media-acquired separated from locally-paired records; both IIIT-ILST overlap denominators recorded. Descriptions only — no reacquisition, no hash or rights change. | none | Review the correction PR. Then hold: Resources sources against a concrete Eval requirement, not speculatively. |
