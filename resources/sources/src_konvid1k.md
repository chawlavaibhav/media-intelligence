# Source record — KoNViD-1k

**source_id:** `src_konvid1k`  
**status:** `downloaded`  
**assessed:** 2026-08-24 (RES-001, under Controller clarifications 6–7)

## Identity

- **Domain:** real_natural_video (Flickr/YFCC100M)
- **Origin:** MMSP / VQA Group, Universitat Konstanz
- **Official URL:** https://database.mmsp-kn.de/konvid-1k-database.html
- **Citation:** Hosu et al., QoMEX 2017
- **Media type:** video
- **Claimed size:** 1,200 videos, 8s each, ~2.3 GB

## Labels — source observations, never project ground truth

- **Provided labels:** subjective quality MOS + per-video blur/colourfulness/contrast/SI/TI/VNIQE (KoNViD_1k_attributes.csv, KoNViD_1k_mos.csv)
- **Annotation type:** crowdsourced subjective quality study

## Rights — six separate facts

| Field | Finding |
|---|---|
| Code licence | n/a |
| Dataset / annotation licence | not_stated |
| Underlying media rights | not_verified. Official page describes sources as Creative Commons video from YFCC100M but names no variant. The distributed metadata contains flickr_id but NO per-video licence field — checked directly. Per-item CC status therefore unresolved. |
| Redistribution status | not_stated - treat as NOT permitted |
| Access method | public direct download, ungated: https://datasets.vqa.mmsp-kn.de/archives/KoNViD_1k_videos.zip . No login/form/cookie. robots.txt absent on the file host; the database host does not disallow the KoNViD-1k page. |
| Commercial use (if explicit) | not_stated |

## Terms / access notes

Acquired under RES-001 clarification 6/7: public, ungated, no explicit term prohibiting download, internal research/evaluation only. flickr_id is present, so a future rights review could resolve per-video CC status against Flickr if a use beyond internal evaluation is ever proposed. PRIVACY NOTE: KoNViD_1k_subjective.csv ships crowdworker IP addresses, worker IDs and city/country - see Controller Brief.

## Determination

**`downloaded`** — Public, ungated, no explicit prohibition. Rights not_stated and recorded as such. Provides the only large real human-made media in the pilot.

## Acquisition state

- downloaded_item_count: **1200**
- downloaded_bytes: **2,412,945,110**
- version/subset: full public release

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
