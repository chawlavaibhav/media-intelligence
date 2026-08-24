# Source record — ImageRewardDB

**source_id:** `src_imagerewarddb`  
**status:** `partial_download`  
**assessed:** 2026-08-24 (RES-001, under Controller clarifications 6–7)

## Identity

- **Domain:** generated_image_preference
- **Origin:** Zhipu/THUDM (ImageReward, NeurIPS 2023)
- **Official URL:** https://huggingface.co/datasets/zai-org/ImageRewardDB
- **Citation:** Xu et al., ImageReward, NeurIPS 2023
- **Media type:** image
- **Claimed size:** 137k expert comparisons; images/ tree = 23.7 GB (train 21.4, test 1.18, validation 1.13)

## Labels — source observations, never project ground truth

- **Provided labels:** expert pairwise comparisons; separate alignment / fidelity / harmlessness ratings
- **Annotation type:** expert human annotation

## Rights — six separate facts

| Field | Finding |
|---|---|
| Code licence | MIT (stated) |
| Dataset / annotation licence | apache-2.0 (stated on dataset card) |
| Underlying media rights | not_verified beyond the publisher's assertion. Images collected from DiffusionDB (Stable Diffusion generations). Publisher asserts apache-2.0 over the dataset. |
| Redistribution status | apache-2.0 permits redistribution; we do not redistribute |
| Access method | public HuggingFace, anonymous, ungated. NOTE: THUDM/ImageRewardDB now HTTP 307-redirects to zai-org/ImageRewardDB (org rename) - the URL printed in CORPUS-SOURCING-PLAN.md era references is stale. |
| Commercial use (if explicit) | not_stated explicitly; apache-2.0 imposes no use restriction |

## Terms / access notes

Subset rule is the distributor's own COMPLETE validation split, taken whole - so no selection judgement of ours enters the corpus at all. Full dataset far exceeds the RES-001 budget.

## Determination

**`partial_download`** — Apache-2.0, ungated. Only source separating evaluation dimensions, closest public analogue to our technical-vs-creative split.

## Acquisition state

- downloaded_item_count: **2584**
- downloaded_bytes: **1,125,610,808**
- version/subset: official validation split (validation_1.zip + validation_2.zip)

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
