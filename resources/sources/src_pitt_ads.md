# Source record — Pitt Image and Video Ads

**source_id:** `src_pitt_ads`  
**status:** `blocked_access`  
**assessed:** 2026-08-24 (RES-001 Phase 1)

## Identity

- **Domain:** real_advertising
- **Origin:** Univ. of Pittsburgh, Kovashka group
- **Official URL:** https://people.cs.pitt.edu/~kovashka/ads/
- **Citation:** Hussain et al., CVPR 2017
- **Media type:** image + video
- **Claimed size:** 64,832 image ads; 3,477 video ads

## Labels (source observations, never project ground truth)

- **Provided labels:** topic, sentiment, action-reason Q/A, strategy, symbolism bounding boxes
- **Annotation type:** crowdworker (Amazon Mechanical Turk)

## Rights — recorded as six separate facts

| Field | Finding |
|---|---|
| Code licence | not_stated |
| Dataset / annotation licence | not_stated (annotation zips are directly downloadable but carry no licence text) |
| Underlying media rights | UNCLEAR. Media are advertisements collected from the web; third-party brand copyright almost certainly applies. No rights statement anywhere on the official page or readme. |
| Redistribution status | not_stated |
| Access method | EMAIL REQUEST GATE for image data. readme_images.txt: 'To obtain the dataset for research purposes, please email us.' Image URLs are also supplied by email. Video data is supplied as a video ID list (final_video_id_list.csv), not media. |
| Commercial use (if explicit) | not_stated. Access phrased as 'for research purposes'. |

## Terms / access notes

Two independent blockers: (1) obtaining images requires emailing the authors = a human permission decision, not crossable per RES-001 clarification 4; (2) even with URLs, acquiring the media means fetching from arbitrary third-party sites, which RES-001 prohibits as scraping. Video acquisition would mean pulling from the hosting platform by ID.

## Determination

**`blocked_access`** — Email request gate; plus no licence stated and underlying media rights unclear. Highest-priority source in CORPUS-SOURCING-PLAN.md, not obtainable within RES-001 rules.

## Acquisition state

- downloaded_item_count: 0
- downloaded_bytes: 0
- version/subset: n/a
