# RES-001 — Integrity report

**Date:** 24 Aug 2026 · **Method:** deterministic only. SHA256 over every retained file, plus
`ffprobe` decode of every item. No model is involved and nothing is judged on content.

## Totals

| | |
|---|---|
| Retained items | **34,786** |
| Retained bytes | **5.70 GB** |
| Budget target | 4–6 GB |
| Budget hard stop | 8 GB |
| Free disk floor | 12 GB |

## Per source

| source_id | items | bytes | validated ok | problems |
|---|---:|---:|---:|---:|
| `src_bstd_devanagari` | 25,246 | 0.20 GB | 25,246 | 0 |
| `src_iiit_ilst_devanagari` | 1,390 | 0.05 GB | 1,390 | 0 |
| `src_imagerewarddb` | 2,584 | 1.13 GB | 2,584 | 0 |
| `src_indicstr12_devanagari` | 3,086 | 0.09 GB | 3,086 | 0 |
| `src_konvid1k` | 1,200 | 2.41 GB | 1,200 | 0 |
| `src_videofeedback` | 987 | 0.18 GB | 987 | 0 |
| `src_videogen_rewardbench` | 288 | 0.78 GB | 288 | 0 |
| `src_youtube_ugc` | 5 | 0.86 GB | 5 | 0 |

## Decode validation

- Items decoding cleanly: **34,786 / 34,786**
- Zero-byte files: **0**
- Undecodable files: **0**

## Exact duplicates

- Unique SHA256: **34,586** across **34,786** items
- Exact duplicate hashes: **200**

Duplicates are **reported, never silently removed** (RES-001 in-scope rule). Perceptual-duplicate
detection was not run: it is optional in RES-001 and the required libraries are not installed.

| sha256 | copies |
|---|---:|
| `5c01966a04b1a4cc…` | 2 |
| `f7038f723a4dd5ee…` | 2 |
| `b5e76762d2b4c166…` | 2 |
| `a94307e9c4706c53…` | 2 |
| `5d0a56f28f7c64ed…` | 2 |
| `e8581b07284bdc5c…` | 2 |
| `d3827b63df32e8aa…` | 2 |
| `9a415931348e094a…` | 2 |
| `3d46b8090fc31630…` | 2 |
| `2d51286b95346e61…` | 2 |
| `44f464a1acbaa16a…` | 2 |
| `771838ff843f7473…` | 2 |
| `e79c1ab67d821232…` | 2 |
| `b2f9b55803e6945d…` | 2 |
| `236e4b16cb59a09f…` | 2 |
| `0e49534be46e8c89…` | 2 |
| `15b39c9321f56b2f…` | 2 |
| `7417de2fc2394e63…` | 2 |
| `e6c6d31ef4022f78…` | 2 |
| `459b233c32f830de…` | 2 |

## Archive deletions (Amendment 01 / RES-001 budget rule)

Archives were deleted only after all five conditions held. Every archive was fingerprinted
**before** deletion so a future re-download can still be verified against it.

| source | archive | bytes | sha256 |
|---|---|---:|---|
| `src_bstd_devanagari` | `recognition.zip` |  | `159fb044fba701f87e41a98b…` |
| `src_imagerewarddb` | `validation_1.zip` |  | `8eb57656d6c424b9451240d5…` |
| `src_imagerewarddb` | `validation_2.zip` |  | `5349f894b1b1571fbe1aed6a…` |
| `src_konvid1k` | `KoNViD_1k_videos.zip` |  | `3528bf99b4d8bad23ced543a…` |
| `src_konvid1k` | `KoNViD_1k_metadata.zip` |  | `13af8b028536bf1864361396…` |

Full fingerprints are retained in `resources/corpus/raw/<source_id>/_archive.sha256`.

### Media removed

One file, `src_youtube_ugc/Animation_360P-188f.mkv` (207,046,293 bytes, sha256
`33998201f2b31c9c1faa786ceccb083ab8a5948e5cd23dab6bc766c10eda47e6`), was removed. It was fetched
under a first-pass selection rule that took the two lexicographically first 360P clips, both from
the same category. The rule was then revised to one clip per category for better coverage. The
file was removed so that re-running `fetch-youtube-ugc.sh` reproduces the corpus exactly. This was
a reproducibility correction, not a space-saving deletion.
