# Existing-resource Eval views

**Task:** R5 of `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md` · **Date:** 26 Aug 2026
**Built by:** `../validators/build_views.py` — executed in this cloud session, exit 0

## What a view is

A **selection over committed item ids, not a copy of media.** Each record references an `item_id` and
`sha256` from `resources/manifests/corpus-pilot-v0.jsonl` and adds the three lineage keys plus
descriptive attributes. No media byte is copied, moved or relabelled.

**The views are build products and are not committed (R-C3).** They are regenerated into
`resources/v1/build/views/` by `../validators/build_views.py`. What *is* committed:

| File | What it is |
|---|---|
| `view-fingerprints.json` | Per-view item count, content-group count and SHA-256, plus a combined fingerprint. |
| `SAMPLE-RECORDS.jsonl` | One representative record per view, showing the exact record shape. |
| `VIEWS.md` | This document: valid uses, invalid uses, label provenance, rights. |

Nine views, 39,262 line-references over 34,786 distinct items (the Devanagari items appear in more
than one view because a view is a lens, not a partition). Carrying them in git cost ~31 MB of
rebuildable JSONL; the fingerprints cost 2 KB and prove the same thing.

**This is not the reproducibility hole the project has been bitten by twice.** The EVAL-005 `build/`
items and the legacy spike's generated media were irreproducible because they depended on assets
outside git — a proprietary font, raw media. These views depend only on `corpus-pilot-v0.jsonl` and
`lineage_keys.py`, both committed. The distinguishing test is whether an artifact needs anything git
does not hold, and this one does not. **Irreplaceable class-C model outputs are explicitly not
covered by this rule and must never be git-ignored.**

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

## Rebuilding

```bash
python3 resources/v1/validators/build_views.py                       # build + verify fingerprints
python3 resources/v1/validators/build_views.py --update-fingerprints # rewrite the committed fingerprints
```

Fail-closed. Every view declares an expected count; a view that selects zero items, or a count that
disagrees with its expectation, aborts the whole build and writes nothing. Without
`--update-fingerprints` the rebuild is compared against the committed fingerprints and a mismatch is
exit 1 — verified by tampering with a fingerprint and confirming the check fails.
