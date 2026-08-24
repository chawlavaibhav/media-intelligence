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

- **Provided labels:** TWO kinds of file, corrected 25 Aug 2026 - see supersedes_note. (a) 375 FULL SCENE PHOTOGRAPHS, each with a per-image *_gt.txt in tab-separated format: region index, 8 polygon coordinates, Unicode transcription - ONE LINE PER TEXT REGION. Photographs carry 1-98 annotated regions each (median 4, mean 7.2, 2,711 regions total). (b) 2,711 PRE-CROPPED single-word images under cropped_images/, whose filenames encode parent photo + region index + the same 8 polygon coordinates, so each crop resolves to exactly one transcription in its parent's *_gt.txt.
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

MEDIA ACQUIRED (3,086) is not the same as LOCALLY PAIRED IMAGE+ANNOTATION RECORDS (375, 12.2%). A 'paired record' means a photograph with its own sidecar *_gt.txt present and parsing to at least one region. The remaining 2,711 files are single-word crops with no sidecar file - but they are NOT unlabelled: 2,711 of 2,713 (99.9%) resolve to exactly one transcription by matching the polygon coordinates in their filename against their parent photograph's *_gt.txt. Resources verified this directly. So: 375 multi-region scene records, 2,711 single-word records, 4 unresolved.

## Correction history

SUPERSEDED WORDING, preserved deliberately rather than erased. This record previously read: 'cropped word images with Unicode labels in per-image *_gt.txt'. That was wrong in a specific way: cropped word images do exist and are the majority of the files, but they are NOT the things the *_gt.txt files label. The *_gt.txt files describe the 375 full scene photographs, one line per region. Correction requested by Eval in eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md and independently reverified by Resources against the manifest and the files on disk. See resources/reports/RES-CORRECTION-01-indicstr12-composition.md.

- downloaded_item_count (media files): **3086**
- downloaded_bytes: **90,314,024**
- version/subset: Devanagari subset, 3,465 of 31,242 real members

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
