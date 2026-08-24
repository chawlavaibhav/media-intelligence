# Source record — IndicSTR12 - Devanagari subset

**source_id:** `src_indicstr12_devanagari`  
**status:** `partial_download`  
**assessed:** 2026-08-24 (RES-001, under Controller clarifications 6–7)

## Identity

- **Domain:** real_scene_text_devanagari
- **Origin:** CVIT, IIIT Hyderabad
- **Official URL:** https://cvit.iiit.ac.in/research/projects/cvit-projects/indicstr
- **Citation:** Lunia et al., IndicSTR12, ICDAR 2023 (arXiv:2403.08007)
- **Media type:** image
- **Claimed size:** >27,000 word images across 12 languages; real.zip = 1,382,967,649 bytes; synthetic companion 62,692,393,572 bytes NOT acquired

## Labels — source observations, never project ground truth

- **Provided labels:** TWO kinds of file, corrected 25 Aug 2026 - see supersedes_note. (a) 375 FULL SCENE PHOTOGRAPHS, each with a per-image *_gt.txt in tab-separated format: region index, 8 polygon coordinates, Unicode transcription - ONE LINE PER TEXT REGION. Photographs carry 1-98 annotated regions each (median 4, mean 7.2, 2,711 regions total). (b) 2,711 PRE-CROPPED single-word images under cropped_images/. These carry their OWN dedicated transcription file - verified_twice__<lang>__cropped_images__word_image_gt.txt, tab-separated crop-filename + transcription, 2,711 entries covering 100% of the crops. Independently, each crop filename also encodes its parent photo, region index and the same 8 polygon coordinates, which resolves to the same transcription via the parent's scene *_gt.txt. Both routes agree on all 2,711.
- **Annotation type:** manual annotation

## Rights — six separate facts

| Field | Finding |
|---|---|
| Code licence | not_stated |
| Dataset / annotation licence | not_stated |
| Underlying media rights | not_stated / not_verified. Photographs of real signage; no rights statement on the project page. |
| Redistribution status | not_stated - treat as NOT permitted |
| Access method | public direct download link on the CVIT project page, no login/form. Host honours HTTP 206. robots.txt disallows Joomla system paths but not /images/datasets/. |
| Commercial use (if explicit) | not_stated |

## Terms / access notes

Member-level range acquisition: transferred 112 MB of a 1.38 GB archive (8.1%); archive never staged on disk, so no full-archive hash is recorded. Selection = the distributor's hindi/ and marathi/ folders, the two Devanagari-script languages, plus their *_gt.txt files. The 62 GB synthetic companion was deliberately not acquired: RES-002 states clean synthetic text alone is insufficient for calibration.

## Determination

**`partial_download`** — Second Devanagari collection, independent of BSTD. NOT independent of IIIT-ILST: both are CVIT / IIIT Hyderabad releases and 173 files are byte-identical across the two (5.6% of this source, 12.4% of IIIT-ILST). Verified by SHA256, see the integrity report.

## Acquisition state

**Media acquired is not the same as usable annotated records — read this before sizing any task.**

- **Media files acquired:** 3086
- **Locally paired image + sidecar annotation records:** 375

MUTUALLY EXCLUSIVE MEDIA CATEGORIES, exhaustive over acquired media: 375 scene_photograph + 2,711 crop_image = 3,086 media files acquired. Asserted disjoint and exhaustive by resources/scripts/verify_devanagari_composition.py. A scene_photograph is a full photograph carrying its own region-level *_gt.txt (equivalently, a 'locally paired image + annotation record' in Eval's terms) - 375 of 3,086 = 12.2%. A crop_image is a single-word image under the distributor's cropped_images/ directory. Annotation files are NOT media and are counted separately (378 .txt files). SEPARATE STATISTIC, not a media category: 2,711 of 2,711 crop images (100%) resolve to a transcription, by either of two independent routes that agree completely.

| media category | count |
|---|---:|
| scene_photograph | 375 |
| crop_image | 2,711 |
| **total = media files acquired** | **3,086** |

These two categories are mutually exclusive and exhaustive over acquired media.
Annotation files are not media and are counted separately.

## Correction history

SUPERSEDED WORDING, preserved deliberately rather than erased. This record previously read: 'cropped word images with Unicode labels in per-image *_gt.txt'. That was wrong in a specific way: cropped word images do exist and are the majority of the files, but they are NOT the things the *_gt.txt files label. The *_gt.txt files describe the 375 full scene photographs, one line per region. Correction requested by Eval in eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md and independently reverified by Resources against the manifest and the files on disk. See resources/reports/RES-CORRECTION-01-indicstr12-composition.md.


COUNT CORRECTION, 25 Aug 2026. An earlier version of this record and its verifier reported 2,713 crop images, which did not reconcile with 3,086 acquired media (375+2,713=3,088). Root cause: the crop detector matched on filename pattern without filtering to media extensions, so it also counted two ANNOTATION files - verified_twice__hindi__cropped_images__word_image_gt.txt and the marathi equivalent. Those are the crop-level ground-truth files, not images. The true crop_image count is 2,711 and the partition now reconciles exactly. No media changed; only the classification of two text files.

- downloaded_item_count (media files): **3086**
- downloaded_bytes: **90,314,024**
- version/subset: Devanagari subset, 3,465 of 31,242 real members

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
