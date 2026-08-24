# Privacy deletion log — KoNViD-1k crowdworker data

**Date:** 24 Aug 2026 · **Authority:** Controller approval, recorded in `resources/tasks/RES-002.md`
(REQUIRED PRE-START RES-001 FINALIZATION, item 5). This is the *only* destructive action approved
outside the transient-payload rules.

## What was deleted, and why it mattered

**File:** `resources/corpus/raw/src_konvid1k/KoNViD_1k_subjective.csv`

This was the per-rating file from KoNViD-1k's crowdsourced video-quality study. Each row was one
person's individual quality rating. The problem was not the ratings — it was what the distributor
shipped alongside them: **columns identifying the individual crowdworkers who did the rating work**,
including their IP address, worker ID, and city/region/country.

Those are real people, they were paid a few cents for a rating task years ago, and this project has
no use whatsoever for their identities. Holding third-party personal data with no purpose is a
liability with no offsetting benefit, so it is gone.

| | |
|---|---|
| Bytes | 17852162 |
| Rating rows | 98384 |
| SHA256 (recorded before deletion) | `7c0a0d412451a4eb365682ea4c7bd0bf7ff8331f9fd7810302a891c279f025e3` |
| Identifying columns | `x_ip`, `x_worker_id`, `x_country`, `x_region`, `x_city`, `x_trust`, `x_channel` |

## What was preserved, and why that is enough

`KoNViD_1k_mos.csv` is retained. "MOS" means **Mean Opinion Score** — the average quality rating each
video received across all the people who rated it. It has two columns: the video's Flickr ID and its
average score. No individual, no location, no network address.

This is the file that actually carries the research value. The scientific content of the study is
"how good did people think this video looked", and the aggregate answers that. The per-person file
only added *who* said it, which we never needed.

`KoNViD_1k_attributes.csv` is also retained: per-video MOS plus technical measurements (blur,
colourfulness, contrast, spatial/temporal information). No personal data.

**Practical consequence:** none for any planned use. Nothing we intend to do with this corpus
required per-rater rows.

**What we can no longer do:** any analysis needing rater-level variation — for example, measuring how
much individual raters disagreed with each other, or modelling rater reliability. If a future task
genuinely needs that, the file is reacquirable from the official source
(`https://datasets.vqa.mmsp-kn.de/archives/KoNViD_1k_metadata.zip`), and the rights question would
have to be revisited then rather than assumed.

**No redacted copy was kept.** RES-002 instructed not to retain one absent a concrete purpose, and
there is none. Keeping a stripped copy "just in case" would preserve exactly the liability the
deletion removes.

## Reproduction

The metadata archive remains publicly downloadable at the URL above. Re-running
`resources/scripts/fetch-konvid1k.sh` restores the video corpus; the metadata archive would need to
be re-fetched separately, and this file would then reappear and should be deleted again.
