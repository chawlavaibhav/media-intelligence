# Existing-resource Eval views

**Task:** R5 of `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md` · **Date:** 26 Aug 2026
**Built by:** `../validators/build_views.py` — executed in this cloud session, exit 0

## What a view is

A **selection over committed item ids, not a copy of media.** Each `.jsonl` line references an
`item_id` and `sha256` from `resources/manifests/corpus-pilot-v0.jsonl` and adds the three lineage
keys plus descriptive attributes. No media byte is copied, moved or relabelled. Nine views, 39,262
line-references over 34,786 distinct items (the Devanagari items appear in more than one view
because a view is a lens, not a partition).

**Every record carries `payload_availability_in_this_session: not_present_git_ignored`,** because the
raw media is not in GitHub. A manifest implying otherwise would be exactly the "description does not
match the files" defect this stream has already been caught by once.

**Every record carries `protected_role: unassigned_pending_eval_experiment_split`.** Resources does
not assign roles; Eval's experiment does.

## The views

| View | Items | Content groups | Valid uses | Invalid uses |
|---|---:|---:|---|---|
| `deva_bstd_full` | 25,246 | 25,227 | Devanagari **reading** calibration; the only genuine cross-lineage reserve candidate | Not a test of Devanagari **rendering**. Do not filter by `language == hindi` — that drops 5,109 Marathi images written in the same script. Do not treat the distributor's train/test split as a holdout boundary; 2 duplicate pairs cross it. |
| `deva_cvit_lineage_full` | 4,476 | **376** | Devanagari reading development/calibration **as one pool in one role** | Never split across roles. 4,476 items are 376 independent scenes. |
| `deva_cvit_scene_photographs` | 551 | 375 | Multi-region photographs with their own annotation file | 173 of the 176 IIIT-ILST photographs are byte-identical to IndicSTR12 items |
| `deva_cvit_word_crops` | 3,925 | 376 | Single-word items; 3,924 of 3,925 resolve to a transcription (previously committed) | 1,205 of IIIT-ILST's 1,214 crops derive from photographs shared with IndicSTR12 |
| `imagepref_imagerewarddb` | 2,584 | 2,579 | Image-preference evaluator **development**; separates alignment / fidelity / harmlessness | Not evidence about current models — DiffusionDB-era Stable Diffusion |
| `realvideo_konvid1k` | 1,200 | 1,200 | Real filmed video; candidate perturbation base clips (160.0 min total) | Sampled for **degradation** variety, not creative merit. Base-clip cleanliness unscreened. |
| `genvideo_videofeedback` | 987 | 987 | Generated-video multi-aspect scores, esp. temporal consistency (49.4 min, all exactly 3.00 s) | The publisher **names neither its generators nor its real-world portion** |
| `genvideo_videogen_rewardbench` | 288 | 288 | Cross-generator evaluator behaviour: **24 clips × 12 named generators** | Not a current-model benchmark |
| `realugc_youtube_ugc` | 5 | 5 | Best-documented rights position in the corpus (CC BY 4.0, per-item attribution) | 5 clips is not a population — and **the audio is removed** |

## Label provenance, stated once

Every label in every view is **the distributor's observation**, not project ground truth:
BSTD/CVIT human transcriptions, ImageRewardDB expert comparisons, KoNViD crowdsourced MOS,
VideoFeedback multi-aspect human ratings, VideoGen-RewardBench expert pairwise preferences. None has
been validated by this project. Whether the Devanagari transcriptions survive checking by a Hindi
reader remains **untested**.

## Rights, stated once

All eight sources are **internal research and evaluation only**. Two are `not_stated / not_verified`
(both CVIT sources), one asserts `cc-by-sa-4.0` for images with annotation terms unstated (BSTD), one
is `not_stated` with no per-item licence field in the distributed metadata (KoNViD-1k), three assert
`apache-2.0` by the publisher over material whose upstream rights are not independently verified, and
one is explicitly and verifiably **CC BY 4.0** (YouTube-UGC). **If any result is ever published or
shown to a customer, the rights question must be reopened first.**

## A note on size, and why these are committed anyway

The nine views total about 31 MB, and they are **derived** — every field comes from the committed
manifest plus committed lineage rules. They are committed rather than generated on demand for two
reasons. First, a view Eval can read directly is more useful than one that requires running a script.
Second, and more importantly: this project has twice been bitten by artifacts that turned out not to
be reconstructible (the EVAL-005 `build/` items, which need an uncommitted proprietary font, and the
legacy spike's generated media, gitignored as "regenerable from the scripts here" when it was not).

The distinguishing test is whether an artifact depends on anything outside git. **These do not** —
`build_views.py` needs only `corpus-pilot-v0.jsonl` and `lineage_keys.py`, both committed. They are
genuinely regenerable, and committing them costs 31 MB in a repository that already commits a 21 MB
manifest. No media byte is duplicated: the raw corpus is untouched and absent.

## Rebuilding

`python3 resources/v1/validators/build_views.py` — fail-closed. Every view declares an expected
count; a view that selects zero items, or a count that disagrees with its expectation, aborts the
whole build and writes nothing.
