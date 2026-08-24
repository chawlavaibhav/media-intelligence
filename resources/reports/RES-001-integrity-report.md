# RES-001 — Integrity report

**Date:** 24 Aug 2026 · **Method:** deterministic only. SHA256 over every retained file, plus
`ffprobe` decode of every item. No model is involved and nothing is judged on content.

## Totals

| | |
|---|---|
| Retained items | **4,776** |
| Retained bytes | **4.58 GB** |
| Budget target | 4–6 GB |
| Budget hard stop | 8 GB |
| Free disk floor | 12 GB |

## Per source

| source_id | items | bytes | validated ok | problems |
|---|---:|---:|---:|---:|
| `src_imagerewarddb` | 2,584 | 1.13 GB | 2,584 | 0 |
| `src_konvid1k` | 1,200 | 2.41 GB | 1,200 | 0 |
| `src_videofeedback` | 987 | 0.18 GB | 987 | 0 |
| `src_youtube_ugc` | 5 | 0.86 GB | 5 | 0 |

## Decode validation

- Items decoding cleanly: **4,776 / 4,776**
- Zero-byte files: **0**
- Undecodable files: **0**

## Exact duplicates

- Unique SHA256: **4,771** across **4,776** items
- Exact duplicate hashes: **5**

Duplicates are **reported, never silently removed** (RES-001 in-scope rule). Perceptual-duplicate
detection was not run: it is optional in RES-001 and the required libraries are not installed.

| sha256 | copies |
|---|---:|
| `16ea0d43bbe30ab2…` | 2 |
| `eb8243615cb5cf9c…` | 2 |
| `74d70092e5fdd153…` | 2 |
| `e8745c8785fb88f9…` | 2 |
| `d3450431e56b36d9…` | 2 |

## Archive deletions (Amendment 01 / RES-001 budget rule)

Archives were deleted only after all five conditions held. Every archive was fingerprinted
**before** deletion so a future re-download can still be verified against it.

| source | archive | bytes | sha256 |
|---|---|---:|---|
| `src_imagerewarddb` | `validation_1.zip` |  | `8eb57656d6c424b9451240d5…` |
| `src_imagerewarddb` | `validation_2.zip` |  | `5349f894b1b1571fbe1aed6a…` |
| `src_konvid1k` | `KoNViD_1k_videos.zip` |  | `3528bf99b4d8bad23ced543a…` |
| `src_konvid1k` | `KoNViD_1k_metadata.zip` |  | `13af8b028536bf1864361396…` |

Full fingerprints are retained in `resources/corpus/raw/<source_id>/_archive.sha256`.

### Non-media file removed — approved privacy deletion

`src_konvid1k/KoNViD_1k_subjective.csv` (17,852,162 bytes, 98,384 rating rows, sha256
`7c0a0d412451a4eb365682ea4c7bd0bf7ff8331f9fd7810302a891c279f025e3`) was deleted on 24 Aug 2026 under
explicit Controller approval. It contained crowdworker IP addresses, worker IDs and city/region/
country — third-party personal data this project has no use for. The aggregate mean-opinion-score
file and per-video technical attributes are retained and contain no personal data. Full reasoning:
`resources/reports/RES-002-privacy-deletion-log.md`.

### Media removed

One file, `src_youtube_ugc/Animation_360P-188f.mkv` (207,046,293 bytes, sha256
`33998201f2b31c9c1faa786ceccb083ab8a5948e5cd23dab6bc766c10eda47e6`), was removed. It was fetched
under a first-pass selection rule that took the two lexicographically first 360P clips, both from
the same category. The rule was then revised to one clip per category for better coverage. The
file was removed so that re-running `fetch-youtube-ugc.sh` reproduces the corpus exactly. This was
a reproducibility correction, not a space-saving deletion.
