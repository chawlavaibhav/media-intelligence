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

- **Provided labels:** per-image .xml annotations carrying bounding boxes and transcriptions
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

OVERLAPS IndicSTR12: 173 byte-identical files (12.4% of this source). Member-level range acquisition of the distributor's Devanagari/ folder plus README.txt. All 1,569 members verified present at their exact central-directory sizes with matching SHA256. NOTE: the recorded bytes_transferred_total for this source undercounts - a first attempt failed partway with HTTP/2 framing errors from this host and the rerun skipped members already on disk. The figure is left as measured rather than replaced with an estimate; see _transient_acquisition.json.

## Determination

**`partial_download`** — Third Devanagari collection, with a different annotation format (XML boxes+transcriptions). NOT independent of IndicSTR12: 173 of this source's 1,390 items (12.4%) are byte-identical to IndicSTR12 items. Both come from CVIT / IIIT Hyderabad. Independent of BSTD.

## Acquisition state

- downloaded_item_count: **1390**
- downloaded_bytes: **52,769,595**
- version/subset: Devanagari subset, 1,569 of 4,847 real members

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
