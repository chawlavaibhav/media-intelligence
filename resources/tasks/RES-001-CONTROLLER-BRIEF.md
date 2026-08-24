# Controller Brief — RES-001

**TASK:** RES-001 · Evaluation corpus acquisition pilot
**STATUS:** completed
**Opened:** 24 Aug 2026 · **Last updated:** 24 Aug 2026

---

## WHAT I DID

Verified all nine approved source families at their official distribution points, recorded rights as
six separate fields each, and acquired four of them: **4,776 items, 4.58 GB**, inside the 4–6 GB
target, under the 8 GB stop, with 16 GB free against a 12 GB floor. Every file is checksummed and
decode-validated. No account was created, no terms accepted, no gate crossed, no paid API called.

The task ran across three Controller amendments. The third — licence silence is not an automatic
block for public, ungated data used internally — **reversed the pilot's main finding**, so both the
old and new results are recorded below.

## CONTROLLER AMENDMENTS

**Amendment 01 (storage).** Target 10–15 GB → **4–6 GB**; hard stop 20 GB → **8 GB**; new **12 GB
free-disk floor**; sequential processing; conditional archive deletion; no cloud storage. Raised
because the machine had only 22 GB free against a 20 GB cap.

**Amendment 02 (clarifications 1–5).** Closed all four Phase-0 blocking questions: the task file
governs the source list; PVP = Personalized Visual Persuasion; use is internal research/evaluation
only; access gates are not to be crossed.

**Amendment 03 (clarifications 6–7).** Absence of a stated licence is no longer an automatic block
for public, ungated sources used internally. Public scraping permitted, rate-limited, without
evading controls. Explicit restrictions, gates and paywalls remain hard blocks.

## OBSERVED

**Acquired — 4,776 items, 4.58 GB**

| source | what | items | bytes | rights as found |
|---|---|---:|---:|---|
| `src_konvid1k` | Real natural video, 8s clips | 1,200 | 2.41 GB | **not_stated.** Page says CC from YFCC100M, names no variant. Distributed metadata has `flickr_id` but **no licence field** — checked directly |
| `src_youtube_ugc` | Real UGC video, one per category | 5 | 0.86 GB | **explicit CC BY 4.0.** `LICENSE` + per-clip `ATTRIBUTION` in the bucket |
| `src_imagerewarddb` | Generated images, expert preference | 2,584 | 1.13 GB | apache-2.0 stated |
| `src_videofeedback` | Generated video, 5-aspect human scores | 987 | 0.18 GB | apache-2.0 stated |

Validation: **4,776 / 4,776 decode cleanly. 0 zero-byte, 0 undecodable.**

**Duplicates — correcting an error in the original version of this brief.** It previously said "0
exact duplicates". That was wrong: it carried forward a figure measured on KoNViD-1k alone before
the other sources were added. The correct figure, which the auto-generated integrity report had
right all along, is **4,771 unique file fingerprints across 4,776 items — 5 hashes appear twice, so
5 items are byte-identical copies of another item.**

All five pairs are inside ImageRewardDB: the same generated image stored under two different
filenames. That is expected in a preference dataset, where one image can appear in more than one
human comparison. **The duplicates are retained, not removed** — RES-001 requires reporting them,
and how often a source reuses an image is itself information Eval may need when sampling.

**Blocked — five, none of them for licence silence**

| source | status | blocker |
|---|---|---|
| `src_pvp` | `blocked_access` | HuggingFace reports `gated: auto` — login + terms acceptance |
| `src_ava` | `blocked_license` | dpchallenge.com terms explicitly prohibit robots, reproduction and aggregation |
| `src_pitt_ads` | `blocked_access` | "please email us" — human permission decision |
| `src_lsvq` | `blocked_access` | download form |
| `src_videogen_rewardbench` | `too_large_for_pilot` | rights are fine; ships as one 13.42 GB archive with no per-item path |

**Other observations**
- `THUDM/ImageRewardDB` now 307-redirects to `zai-org/...`; `KwaiVGI/VideoGen-RewardBench` to `KlingTeam/...`. Older references are stale.
- VideoFeedback's card claims 37.6k pairs / 8.81 GB; its media repo's main revision exposes **987 files / 0.18 GB**. Discrepancy unexplained; recorded as observed, not reconciled.
- `holi-lab/visual_persuasion` is ungated but contains only annotations and training JSON — **no images**. Not substituted for PVP.
- **`KoNViD_1k_subjective.csv` contains crowdworker IP addresses, worker IDs, and city/country.** Third-party personal data, shipped by the distributor.

## INFERRED

- The policy change was the binding constraint, not availability. Under the old rule the pilot could
  acquire **zero real human-made media**; under the new one, real media is the **majority of the
  corpus by item count**. Nothing about the sources changed in between.
- My earlier "generated vs real" pattern was partly an artefact of the rule, but not entirely: the
  hardest blockers (email gate, form gate, explicit terms) still sit on real media, and all four
  survive the new policy.
- KoNViD-1k and YouTube-UGC are the same *domain* (natural video sampled for technical quality
  variety), so the corpus has two real-video sources but arguably one real-video domain.

## SURPRISES

1. **YouTube-UGC was the best-documented source in the pilot, and I had assumed it would be the
   worst.** I deprioritised it in Phase 1 expecting a YouTube scraping problem. Google distributes
   the actual files from a public GCS bucket with an explicit `LICENSE` and per-clip `ATTRIBUTION`
   naming each original author under CC BY 4.0. No YouTube endpoint is involved. It is the only
   source in the corpus with verified, item-level rights.
2. **AVA's block got stronger, not weaker.** Reassessed expecting the licence-silence rule to unblock
   it; instead the site's terms turned out to prohibit robots and reproduction explicitly.
3. **A rights-clear source was defeated by packaging.** VideoGen-RewardBench is Apache-2.0 and
   ungated, and still unusable here purely because 13.42 GB arrives as one archive.
4. **A dataset shipping personal data.** Not something the rights fields were designed to catch.

## FAILURES / BLOCKERS

None outstanding. One process defect worth recording: my first YouTube-UGC selection rule took the
two lexicographically-first 360P clips, both from the same category — content-blind but poor
coverage. I revised it to one clip per distributor-defined category and removed the stray file so
the corpus reproduces exactly from the script. Logged in the integrity report.

## ASSUMPTIONS CHALLENGED

None. Nothing here bears on `coordination/ASSUMPTIONS.md`.

## LOCAL IMPLICATIONS

Every subset rule is content-blind and recorded: ImageRewardDB uses the distributor's **complete
validation split** (no selection of ours at all); YouTube-UGC takes the first 360P clip per
distributor-defined category; VideoFeedback takes every addressable file; KoNViD-1k is whole.

## CROSS-STREAM IMPLICATIONS — `CROSS_STREAM`, proposed only

The corpus supports **some** of Eval's work and explicitly not all of it.

**It does unblock:** calibrating a judge against real video — checking whether an automated evaluator
agrees with humans on material that was filmed rather than generated. That was impossible before this
task.

**It does not unblock the Hindi-text checker.** The corpus contains **no known Devanagari or Indic
material at all.** Devanagari text rendering is recorded elsewhere in this project as our worst
observed failure area, so this is a live gap, not a theoretical one. Anyone reading "the corpus
supports evaluator calibration" should not conclude Hindi-text evaluation is covered — it is not.
(RES-002 exists to close this.)

**It also does not support:** comparison against real professional or commercial creative, or any
audio work.

## ARCHITECTURAL IMPLICATIONS

None.

## DECISIONS NEEDED FROM CONTROLLER

1. **Personal data in KoNViD-1k.** `KoNViD_1k_subjective.csv` carries crowdworker IPs and locations.
   It is git-ignored and never leaves the machine, but retaining third-party personal data we do not
   need is a choice you should make, not me. Options: keep, drop the file (MOS scores survive in
   `KoNViD_1k_mos.csv`), or drop just the identifying columns. **I have not deleted anything.**
2. **VideoGen-RewardBench.** 12-generator diversity exists nowhere else. Needs either a larger
   budget (~27 GB peak) or approval to range-fetch individual members from the remote archive.
3. **Pitt Ads / LSVQ.** Still the only routes to real advertising and large-scale social video. Both
   need a human to complete a request. Do you want to?
4. **A second real-media *domain*.** Both real sources study technical quality. If the corpus should
   contain real media chosen for creative merit, that is a new source family and needs approval.

## FILES CREATED / MODIFIED

`resources/manifests/corpus-pilot-v0.{jsonl,csv}` (4,776 items) · `source-registry-v0.csv` (9
sources, 23 fields) · `resources/sources/*.md` (9 records) · `resources/reports/RES-001-{source-
assessment,integrity-report,bias-and-coverage-report}.md` · `resources/scripts/` (guard, 4 fetch
scripts, validator, registry builder, report builder) · `resources/HANDOFF.md` · this brief.

Raw media in `resources/corpus/raw/` — git-ignored, never committed.

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.* Answer decision 1 first — it is the only one with a
personal-data dimension. Then treat this corpus as sufficient for the **real-video** part of
EVAL-001's instrument-calibration work only — it does **not** cover Hindi/Devanagari checking, which
needs separate material. Open a separate task if a real *creative* media family is wanted, since
that is a new source family rather than more of this one.

## CONFIRMATION

No unapproved strategic step was started. No benchmark or holdout was constructed, no creative
labels were created, no Canon-derived strata were used, no external label was promoted to project
ground truth. All acquired media is marked internal research and evaluation only: not
redistributable, not training data, not customer-deliverable, not production-cleared.
