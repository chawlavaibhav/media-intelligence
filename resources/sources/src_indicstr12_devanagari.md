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

- **Provided labels:** cropped word images with Unicode labels in per-image *_gt.txt
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

**`partial_download`** — Second independent Devanagari collection. Different collectors and conditions than BSTD, which matters because a checker that only sees one collection can look better than it is.

## Acquisition state

- downloaded_item_count: **3086**
- downloaded_bytes: **90,314,024**
- version/subset: Devanagari subset, 3,465 of 31,242 real members

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
