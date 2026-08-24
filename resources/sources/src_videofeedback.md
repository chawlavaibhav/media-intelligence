# Source record — VideoFeedback (VideoScore)

**source_id:** `src_videofeedback`  
**status:** `downloaded`  
**assessed:** 2026-08-24 (RES-001, under Controller clarifications 6–7)

## Identity

- **Domain:** generated_video_human_scores
- **Origin:** TIGER-Lab
- **Official URL:** https://huggingface.co/datasets/TIGER-Lab/VideoFeedback
- **Citation:** VideoScore / VideoFeedback, TIGER-Lab
- **Media type:** video
- **Claimed size:** card claims 37.6k pairs / 8.81 GB; the media repo's main revision exposes 987 mp4 files totalling 0.18 GB - the discrepancy is unexplained and recorded as observed

## Labels — source observations, never project ground truth

- **Provided labels:** visual quality, temporal consistency, dynamic degree, text-to-video alignment, factual consistency (1-4)
- **Annotation type:** human raters, multi-aspect

## Rights — six separate facts

| Field | Finding |
|---|---|
| Code licence | not_stated |
| Dataset / annotation licence | apache-2.0 (stated on both repos) |
| Underlying media rights | not_verified beyond the publisher's assertion. AI-generated video from multiple text-to-video models plus some real-world video as augmentation; the card names neither the source models nor which items are the real-world portion. |
| Redistribution status | apache-2.0 permits redistribution; we do not redistribute |
| Access method | public HuggingFace, anonymous, ungated. Annotations at TIGER-Lab/VideoFeedback; media at hexuan21/VideoFeedback-videos-mp4. |
| Commercial use (if explicit) | not_stated explicitly; apache-2.0 imposes no use restriction |

## Terms / access notes

No subset rule needed: every mp4 addressable on the media repo's main revision was taken. Temporal-consistency labels are the relevant axis for the cross-frame observation-unit problem.

## Determination

**`downloaded`** — Apache-2.0, ungated, fits budget whole.

## Acquisition state

- downloaded_item_count (media files): **987**
- downloaded_bytes: **181,560,342**
- version/subset: all mp4 on main revision

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
