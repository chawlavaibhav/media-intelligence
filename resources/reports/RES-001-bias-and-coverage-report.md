# RES-001 — Bias and coverage report

**Date:** 24 Aug 2026 · **Descriptive only.** These axes describe what the corpus contains. They
are deliberately *not* Canon-derived: no axis here encodes a creative principle under test, because
stratifying evaluation media by the theory being tested is the circularity this stream exists to
prevent (Project Contract, separation 9).

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

| Vertical resolution | items |
|---|---:|
| <=1080p | 549 |
| <=360p | 29,033 |
| <=540p | 3,497 |
| <=720p | 1,665 |
| >1080p | 42 |

## Real vs generated — the axis that changed

- **Real human-made media:** 5 sources — `src_konvid1k`, `src_youtube_ugc`, `src_bstd_devanagari`, `src_indicstr12_devanagari`, `src_iiit_ilst_devanagari`
- **AI-generated media:** 3 sources — `src_imagerewarddb`, `src_videofeedback`, `src_videogen_rewardbench`

Under the previous rights policy this pilot could acquire **no real human-made media at all**. The
licence-silence change reversed that: the corpus is now majority real media by item count.

## Known skews — state these before anyone designs an experiment on this corpus

| Skew | Detail |
|---|---|
| **Quality-assessment bias** | Both real-video sources were built to study *technical* quality — compression, blur, camera shake. Their populations were sampled for degradation variety, not for creative merit. |
| **No commercial creative** | Zero advertising, zero professional brand work. Pitt Ads was the only route and stays gated. |
| **No real photography** | AVA was the only route and is blocked by explicit site terms. |
| **Language / script** | Not measured. No Devanagari or Indic-script content is known to be present. Unchanged from the sourcing plan's gap table. |
| **Geography** | Not stated by any source. Assume Anglosphere-weighted; not verified. |
| **Generator era** | ImageRewardDB images are DiffusionDB-era Stable Diffusion. VideoFeedback does not name its generators. Neither reflects current frontier models. |
| **Generator diversity lost** | VideoGen-RewardBench (12 generators) is `too_large_for_pilot` — its distribution is one 13.42 GB archive with no addressable per-item path. That diversity exists nowhere else in the corpus. |
| **Audio** | YouTube-UGC clips are audio-removed excerpts. The corpus supports no audio work. |
| **Sample size, YouTube-UGC** | 5 clips. Enough to prove the acquisition path and the rights position; not a population. |

## What this corpus can and cannot support

**Can support:** evaluator/instrument calibration on real video; technical-quality measurement;
cross-frame temporal work (KoNViD-1k and VideoFeedback both carry relevant labels); comparing how
judges behave on real versus generated material — which is newly possible and was not before.

**Cannot support:** any claim requiring comparison against real professional or commercial creative;
any Indic-script or Indian-market work; any audio work; any claim about current frontier generators.

## Blocked sources — evidence, not failure

| source | status | blocker |
|---|---|---|
| `src_pvp` | `blocked_access` | Gated (login + terms acceptance). |
| `src_ava` | `blocked_license` | Explicit site terms prohibit robots, reproduction and aggregation; photographers' copyright expressly reserved. |
| `src_pitt_ads` | `blocked_access` | Email/manual-approval gate; clarification 7 keeps this blocked absent separate Controller authorisation. |
| `src_lsvq` | `blocked_access` | Form/manual-approval gate; clarification 7 keeps this blocked absent separate Controller authorisation. |

Note the shape: after the policy change, **not one source is blocked for licence silence.** The
remaining blockers are access gates (login, email, form) and one explicit terms prohibition — exactly
the categories the policy still treats as hard limits.
