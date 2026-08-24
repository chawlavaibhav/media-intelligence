# Bias and coverage report — full corpus

**Generated from the manifest and registry. Do not hand-edit — rerun `resources/scripts/build_reports.py`.**

**Descriptive only.** These axes describe what the corpus contains. They are deliberately *not*
Canon-derived: no axis encodes a creative principle under test, because stratifying evaluation
media by the theory being tested is the circularity this stream exists to prevent (Project
Contract, separation 9).

## What is in the corpus

| Media type | items |
|---|---:|
| image | 32,306 |
| video | 2,480 |

| Domain family | items |
|---|---:|
| real_scene_text_devanagari | 29,722 |
| generated_image_preference | 2,584 |
| real_natural_video (Flickr/YFCC100M) | 1,200 |
| generated_video_human_scores | 987 |
| generated_video_pairwise_preference | 288 |
| real_ugc_video (YouTube creators) | 5 |

## Real vs generated media

- **Real human-made:** 5 sources, 30,927 items — `src_konvid1k`, `src_youtube_ugc`, `src_bstd_devanagari`, `src_indicstr12_devanagari`, `src_iiit_ilst_devanagari`
- **AI-generated:** 3 sources, 3,859 items — `src_imagerewarddb`, `src_videofeedback`, `src_videogen_rewardbench`

## What this corpus can and cannot support

*Derived from the domains actually present in the registry — not written by hand.*

| Capability | Status |
|---|---|
| Calibrating a judge against real filmed video | **supported** |
| Devanagari / Indic script reading (real photographed text) | **supported** |
| Evaluator behaviour across multiple AI video generators | **supported** |
| Generated-image preference / dimensional rating work | **supported** |
| Comparison against real professional or commercial creative | gap — not in the corpus |
| Real photography aesthetics | gap — not in the corpus |
| Audio work | gap — not in the corpus |
| Devanagari in GENERATED output (our actual failure mode) | gap — not in the corpus |

**Open gaps:** Comparison against real professional or commercial creative; Real photography aesthetics; Audio work; Devanagari in GENERATED output (our actual failure mode)

## Known skews — state these before designing an experiment on this corpus

| Skew | Detail |
|---|---|
| **Quality-assessment bias** | The real-video sources were built to study *technical* quality — compression, blur, camera shake. Their populations were sampled for degradation variety, not creative merit. |
| **Devanagari is photographed, not generated** | The Devanagari material is real signage. It tests whether a judge can *read* the script. It does not test whether a generator *renders* it correctly. |
| **Two Devanagari sources share a lab** | IndicSTR12 and IIIT-ILST are both CVIT / IIIT Hyderabad releases and share byte-identical files (see the integrity report). Treat them as related, not independent. |
| **Geography** | Not stated by any source. The Devanagari material is Indian by construction; the rest should be assumed Anglosphere-weighted, unverified. |
| **Generator era** | ImageRewardDB images are DiffusionDB-era Stable Diffusion; VideoFeedback does not name its generators. Neither reflects current frontier models. |
| **Audio** | The YouTube-UGC clips are audio-removed excerpts. |
| **Sample size, YouTube-UGC** | 5 clips. Enough to prove the acquisition path and the rights position; not a population. |

## Blocked sources — evidence, not failure

| source | status | blocker |
|---|---|---|
| `src_pvp` | `blocked_access` | Gated (login + terms acceptance). |
| `src_ava` | `blocked_license` | Explicit site terms prohibit robots, reproduction and aggregation; photographers' copyright expressly reserved. |
| `src_pitt_ads` | `blocked_access` | Email/manual-approval gate; clarification 7 keeps this blocked absent separate Controller authorisation. |
| `src_lsvq` | `blocked_access` | Form/manual-approval gate; clarification 7 keeps this blocked absent separate Controller authorisation. |

**4 of 12 candidate sources are blocked.** Not one is blocked for licence
silence; the blockers are access gates and one explicit terms prohibition — the categories current
policy still treats as hard limits.
