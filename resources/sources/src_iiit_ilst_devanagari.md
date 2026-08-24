# Source record — IIIT-ILST - Devanagari subset

**source_id:** `src_iiit_ilst_devanagari`  
**status:** `partial_download`  
**assessed:** 2026-08-24 (RES-001, under Controller clarifications 6–7)

## Identity

- **Domain:** real_scene_text_devanagari
- **Origin:** CVIT, IIIT Hyderabad
- **Official URL:** https://cvit.iiit.ac.in/research/projects/cvit-projects/iiit-ilst
- **Citation:** Mathew, Jain, Jawahar, ICDAR MOCR Workshop 2017 (arXiv:2104.04437)
- **Media type:** image
- **Claimed size:** ~1,000 real images per script across Devanagari/Telugu/Malayalam; IIIT-ILST.zip = 638,566,321 bytes

## Labels — source observations, never project ground truth

- **Provided labels:** Same two-part structure as IndicSTR12. (a) 176 FULL SCENE PHOTOGRAPHS with a per-image PASCAL-VOC style .xml carrying one <object> per text region - bounding box plus Unicode transcription. 1-64 regions each (median 8, 1,788 regions total). (b) 1,214 pre-cropped single-word images. A distributor-supplied list, IIIT-ILST__Devanagari__cropped__Devanagari__WordImagesList.txt, maps 1,150 of them to a transcription; independently, 1,210 resolve by matching the bounding box in the crop filename against the parent scene XML. The union covers 1,213 of 1,214 (99.9%); exactly one crop resolves by neither route and is named in the verifier output. The original wording 'bounding boxes and transcriptions' was accurate but did not distinguish scene photographs from crops.
- **Annotation type:** manual annotation

## Rights — six separate facts

| Field | Finding |
|---|---|
| Code licence | not_stated |
| Dataset / annotation licence | not_stated |
| Underlying media rights | not_stated / not_verified. Photographs of real signage; no rights statement on the project page. |
| Redistribution status | not_stated - treat as NOT permitted |
| Access method | public direct download link on the CVIT project page, no login/form. Host honours HTTP 206. |
| Commercial use (if explicit) | not_stated |

## Terms / access notes

OVERLAPS IndicSTR12 - TWO VALID DENOMINATORS, both true, same numerator: (1) 173 of 1,390 ACQUIRED images = 12.4%, the correct figure for the source as a whole; (2) 173 of 176 LOCALLY PAIRED records = 98.3%, the figure a consumer actually feels, because only paired records can be scored. Only 3 paired records are genuinely unique to this source. The overlap sits ENTIRELY in the annotated scene photographs - no cropped word image is byte-identical across the two sources. Further, all 173 shared photographs are exactly IndicSTR12's complete Hindi-labelled scene set (173 of 173), so the smaller dataset's Devanagari scene folder is effectively the larger dataset's Hindi scene folder. CONTENT-LEVEL CAVEAT verified by Resources: 1,205 of this source's 1,214 crops (99.3%) are derived from photographs shared with IndicSTR12. They are not byte-identical, so hash-based deduplication does NOT flag them, but they depict the same regions of the same photographs - relevant to any holdout that assumes crop-level independence. Member-level range acquisition of the distributor's Devanagari/ folder plus README.txt. All 1,569 members verified present at their exact central-directory sizes with matching SHA256. NOTE: the recorded bytes_transferred_total for this source undercounts - a first attempt failed partway with HTTP/2 framing errors from this host and the rerun skipped members already on disk. The figure is left as measured rather than replaced with an estimate; see _transient_acquisition.json.

## Determination

**`partial_download`** — Third Devanagari collection, with a different annotation format (XML boxes+transcriptions). NOT independent of IndicSTR12: 173 of this source's 1,390 items (12.4%) are byte-identical to IndicSTR12 items. Both come from CVIT / IIIT Hyderabad. Independent of BSTD.

## Acquisition state

**Media acquired is not the same as usable annotated records — read this before sizing any task.**

- **Media files acquired:** 1390
- **Locally paired image + sidecar annotation records:** 176

MUTUALLY EXCLUSIVE MEDIA CATEGORIES, exhaustive over acquired media: 176 scene_photograph + 1,214 crop_image = 1,390 media files acquired. Asserted disjoint and exhaustive by resources/scripts/verify_devanagari_composition.py. A scene_photograph is a full photograph with its own PASCAL-VOC .xml (equivalently a 'locally paired image + annotation record') - 176 of 1,390 = 12.7%. Annotation files are NOT media and are counted separately (176 .xml). SEPARATE STATISTIC, not a media category: 1,213 of 1,214 crop images (99.9%) resolve to a transcription; 1 resolves by neither available route.

| media category | count |
|---|---:|
| scene_photograph | 176 |
| crop_image | 1,214 |
| **total = media files acquired** | **1,390** |

These two categories are mutually exclusive and exhaustive over acquired media.
Annotation files are not media and are counted separately.


COUNT CORRECTION, 25 Aug 2026. An earlier version reported 1,215 crop images, which did not reconcile with 1,390 acquired media (176+1,215=1,391). Root cause: the crop detector matched on filename pattern without filtering to media extensions, so it also counted the annotation file IIIT-ILST__Devanagari__cropped__Devanagari__WordImagesList.txt. The true crop_image count is 1,214 and the partition now reconciles exactly. No media changed; only the classification of one text file.

- downloaded_item_count (media files): **1390**
- downloaded_bytes: **52,769,595**
- version/subset: Devanagari subset, 1,569 of 4,847 real members

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
