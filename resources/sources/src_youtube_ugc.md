# Source record — YouTube-UGC

**source_id:** `src_youtube_ugc`  
**status:** `partial_download`  
**assessed:** 2026-08-24 (RES-001, under Controller clarifications 6–7)

## Identity

- **Domain:** real_ugc_video (YouTube creators)
- **Origin:** Google / YouTube Media Algorithms
- **Official URL:** https://media.withyoutube.com/
- **Citation:** Wang, Inguva, Adsumilli, MMSP 2019 (arXiv:1904.06457)
- **Media type:** video
- **Claimed size:** ~1,500 clips; bucket holds 1,070 video keys / 4,922 objects

## Labels — source observations, never project ground truth

- **Provided labels:** no-reference quality metrics published separately (Noise, Banding, SLEEQ); subjective MOS in follow-up work
- **Annotation type:** subjective quality study (separate release)

## Rights — six separate facts

| Field | Finding |
|---|---|
| Code licence | n/a |
| Dataset / annotation licence | see media licence |
| Underlying media rights | EXPLICIT AND VERIFIED. gs://ugc-dataset/LICENSE is a Creative Commons Public License. gs://ugc-dataset/ATTRIBUTION names each clip's original work, author and states 'licensed under CC BY 4.0'. Clips are audio-removed excerpts of CC BY 4.0 YouTube videos. |
| Redistribution status | CC BY 4.0 permits redistribution with attribution; we do not redistribute |
| Access method | public Google Cloud Storage bucket `ugc-dataset`, anonymous HTTP, ungated. Anonymous XML listing returns HTTP 200. NOT retrieved from youtube.com - no YouTube endpoint touched, so YouTube's robots.txt/ToS restrictions on /get_video are not engaged. |
| Commercial use (if explicit) | CC BY 4.0 does not restrict commercial use (licence text read directly) |

## Terms / access notes

Best-documented source in the pilot: explicit licence AND per-item attribution. LICENSE and ATTRIBUTION retained alongside the media. Selection is deterministic and content-blind: within the 360P tier, the first clip of each distributor-defined category in sorted order, until the source byte budget. Rate-limited, sequential, 1s delay.

## Determination

**`partial_download`** — Explicitly CC BY 4.0, ungated, official Google distribution. Bounded sample only because original pre-transcode files are 0.06-5 GB each.

## Acquisition state

- downloaded_item_count: **5**
- downloaded_bytes: **855,146,670**
- version/subset: 360P tier, one clip per category, bounded sample

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
