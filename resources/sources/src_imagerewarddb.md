# Source record — ImageRewardDB

**source_id:** `src_imagerewarddb`  
**status:** `candidate_approved_for_download`  
**assessed:** 2026-08-24 (RES-001 Phase 1)

## Identity

- **Domain:** generated_image_preference
- **Origin:** THUDM / Tsinghua (ImageReward, NeurIPS 2023)
- **Official URL:** https://huggingface.co/datasets/THUDM/ImageRewardDB
- **Citation:** Xu et al., ImageReward, 2023
- **Media type:** image
- **Claimed size:** 137k expert comparisons; 8K-scale=20.9GB, 1K-scale=2.7GB

## Labels (source observations, never project ground truth)

- **Provided labels:** expert pairwise comparisons; alignment / fidelity / harmlessness ratings
- **Annotation type:** expert human annotation

## Rights — recorded as six separate facts

| Field | Finding |
|---|---|
| Code licence | MIT (stated) |
| Dataset / annotation licence | Apache-2.0 (stated on dataset page) |
| Underlying media rights | Images sourced from DiffusionDB (Stable Diffusion generations). Publisher asserts Apache-2.0 over the dataset. Not independently verified beyond the publisher's statement. |
| Redistribution status | Apache-2.0 permits redistribution; we do not plan to redistribute |
| Access method | public direct download (HuggingFace, no login observed) |
| Commercial use (if explicit) | not_stated explicitly; Apache-2.0 does not restrict use |

## Terms / access notes

Dataset card states license apache-2.0; code MIT. No gate observed on the dataset page.

## Determination

**`candidate_approved_for_download`** — Licence clearly permits internal research/evaluation use; ungated; 1K-scale subset fits budget.

## Acquisition state

- downloaded_item_count: 0
- downloaded_bytes: 0
- version/subset: 1K-scale subset selected for pilot
