# Source record — Bharat Scene Text Dataset - Devanagari subset

**source_id:** `src_bstd_devanagari`  
**status:** `partial_download`  
**assessed:** 2026-08-24 (RES-001, under Controller clarifications 6–7)

## Identity

- **Domain:** real_scene_text_devanagari
- **Origin:** Bhashini / IIT Jodhpur
- **Official URL:** https://github.com/Bhashini-IITJ/BharatSceneTextDataset
- **Citation:** arXiv:2511.23071
- **Media type:** image
- **Claimed size:** 6,582 scene images / 126,292 words across 12 languages; recognition.zip = 829,120,510 bytes

## Labels — source observations, never project ground truth

- **Provided labels:** per-image ground-truth transcription (Unicode) + language label, in train/test_recognition_data.json
- **Annotation type:** manual annotation - polygon boxes, transcription, script

## Rights — six separate facts

| Field | Finding |
|---|---|
| Code licence | not_stated |
| Dataset / annotation licence | not_stated for annotations |
| Underlying media rights | repo states images are under Creative Commons cc-by-sa-4.0. Annotation/transcription licence not stated -> not_verified. |
| Redistribution status | cc-by-sa-4.0 permits redistribution with share-alike for the images; annotation terms unstated; we do not redistribute |
| Access method | public creator-published Google Drive link, no login. Anonymous requests get Google's standard large-file 'Virus scan warning' interstitial, which asks for no credential/account/agreement - JUDGEMENT CALL flagged in the Controller Brief. |
| Commercial use (if explicit) | cc-by-sa-4.0 does not restrict commercial use for the images; annotations not_stated |

## Terms / access notes

TRANSIENT acquisition: the 0.83 GB archive was downloaded to temporary staging, only Devanagari members extracted, archive deleted after validation (sha256 159fb044fba701f87e41a98b679a5da8c4dadd07727a2a5de72bb9d4f2c13036 recorded first). Selection rule = UNION of (a) language label == hindi and (b) transcription contains a Devanagari codepoint. Rule (b) matters: Marathi is written in Devanagari and a language filter alone would have missed ~5,100 target-script images. 351 further images labelled as other languages also carry Devanagari text - the language label is NOT a reliable proxy for script.

## Determination

**`partial_download`** — Largest Devanagari pool acquired: real photographed signage with human transcriptions, which is what checker calibration needs.

## Acquisition state

- downloaded_item_count (media files): **25246**
- downloaded_bytes: **201,386,592**
- version/subset: Devanagari subset, 25,246 of 106,490 archive members

## Permitted use

Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not
training data, not customer-deliverable, not production-cleared. Rights recorded above as
found; nothing inferred.
