# Source record — VideoFeedback (VideoScore)

**source_id:** `src_videofeedback`  
**status:** `candidate_approved_for_download`  
**assessed:** 2026-08-24 (RES-001 Phase 1)

## Identity

- **Domain:** generated_video_human_scores
- **Origin:** TIGER-Lab
- **Official URL:** https://huggingface.co/datasets/TIGER-Lab/VideoFeedback
- **Citation:** VideoScore / VideoFeedback, TIGER-Lab
- **Media type:** video
- **Claimed size:** 37.6k text-to-video pairs; media repo 8.81 GB / 37,662 rows

## Labels (source observations, never project ground truth)

- **Provided labels:** visual quality, temporal consistency, dynamic degree, text-to-video alignment, factual consistency (1-4)
- **Annotation type:** human raters, multi-aspect

## Rights — recorded as six separate facts

| Field | Finding |
|---|---|
| Code licence | not_stated |
| Dataset / annotation licence | Apache-2.0 (stated on both annotation and media repos) |
| Underlying media rights | AI-generated video from multiple text-to-video models, plus some real-world video as augmentation. Source models not listed on the dataset page. Publisher asserts Apache-2.0. |
| Redistribution status | Apache-2.0 permits redistribution; we do not plan to redistribute |
| Access method | public direct download (HuggingFace, no login observed). Annotations and media are in SEPARATE repos. |
| Commercial use (if explicit) | not_stated explicitly; Apache-2.0 does not restrict use |

## Terms / access notes

Media files live at hexuan21/VideoFeedback-videos-mp4 (apache-2.0, 8.81 GB, README empty). Real-world-video augmentation portion is undocumented and needs checking before those items are used.

## Determination

**`candidate_approved_for_download`** — Licence clearly permits internal research/evaluation use; ungated; requires bounded subset.

## Acquisition state

- downloaded_item_count: 0
- downloaded_bytes: 0
- version/subset: bounded deterministic subset required (8.81 GB exceeds 8 GB cap)
