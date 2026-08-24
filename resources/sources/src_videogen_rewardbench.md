# Source record — VideoGen-RewardBench

**source_id:** `src_videogen_rewardbench`  
**status:** `candidate_approved_for_download`  
**assessed:** 2026-08-24 (RES-001 Phase 1)

## Identity

- **Domain:** generated_video_pairwise_preference
- **Origin:** KwaiVGI / Kling team
- **Official URL:** https://huggingface.co/datasets/KwaiVGI/VideoGen-RewardBench
- **Citation:** VideoAlign / Improving Video Generation with Human Feedback, NeurIPS 2025
- **Media type:** video
- **Claimed size:** 25,234 rows / 26.5k triplets; 13.4 GB

## Labels (source observations, never project ground truth)

- **Provided labels:** pairwise preference: visual quality, motion quality, temporal alignment, overall
- **Annotation type:** expert annotators, pairwise

## Rights — recorded as six separate facts

| Field | Finding |
|---|---|
| Code licence | not_stated |
| Dataset / annotation licence | Apache-2.0 (stated on dataset page) |
| Underlying media rights | AI-generated video from 12 named commercial and open T2V models (CogVideoX, kling, kling1.5, qingying, gen3, minimax, vidu, tongyi, luma, luma1.6, opensora1.2, easyanimatev4). Publisher asserts Apache-2.0 over outputs of third-party commercial generators; that authority is NOT independently verified. |
| Redistribution status | Apache-2.0 permits redistribution; we do not plan to redistribute |
| Access method | public direct download (HuggingFace, no login observed) |
| Commercial use (if explicit) | not_stated explicitly; Apache-2.0 does not restrict use |

## Terms / access notes

Mirrored at KlingTeam/VideoGen-RewardBench. Generator diversity (12 models) is the main value here.

## Determination

**`candidate_approved_for_download`** — Licence clearly permits internal research/evaluation use; ungated; requires bounded subset.

## Acquisition state

- downloaded_item_count: 0
- downloaded_bytes: 0
- version/subset: bounded deterministic subset required (13.4 GB exceeds 8 GB cap)
