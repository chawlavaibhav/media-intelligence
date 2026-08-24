# Controller Brief — RES-002

**TASK:** RES-002 · Devanagari calibration material + transient large-source acquisition
**STATUS:** completed · **Date:** 24 Aug 2026

---

## WHAT I DID

Two things. **First**, closed the Devanagari gap: acquired **29,722 real photographed Devanagari
images with human transcriptions** from three independent collections. RES-001 had none, which is
why Eval's Hindi-text checker was blocked.

**Second**, proved that a large public archive can be sampled without downloading it. RES-001 gave
up on VideoGen-RewardBench because its 13.42 GB arrives as a single zip. That was a wrong
conclusion, and this task overturns it: 288 videos across all 12 generators were acquired by
transferring **5.8% of the archive**, which was never written to disk.

Retained **1,170 MB** against a 2,048 MB budget. Free disk never fell below **14.5 GB** against a
12 GB floor. No account, no form, no terms accepted, no paid API.

## RES-001 FINALIZATION (all six items)

| Item | Done |
|---|---|
| 1. Duplicate claim | Corrected. The brief said "0 exact duplicates" — wrong, carried over from a KoNViD-only check. Real figure: **4,771 unique fingerprints across 4,776 items, 5 duplicate hashes**, all inside ImageRewardDB (same image under two filenames — expected where one image appears in several human comparisons). Retained and reported, not removed. |
| 2. Stale Handoff | Fixed. It claimed no external dataset had been downloaded. |
| 3. Eval-sufficiency claim | Narrowed everywhere. The corpus supports real-video judge calibration; it does **not** unblock the Hindi checker. |
| 4. VideoFeedback discrepancy | Left unexplained, as instructed. Card claims ~37.6k pairs / 8.81 GB; the exposed repo yielded 987 files / 0.18 GB. |
| 5. Privacy deletion | Done. Detail below. |
| 6. Merge + re-read standard | Done; communication check re-acknowledged after the standard changed. |

**The privacy deletion.** `KoNViD_1k_subjective.csv` held 98,384 individual rating rows (17.85 MB) —
and alongside each rating, the **IP address, worker ID and city/region/country of the crowdworker who
gave it**. Real people, paid a few cents years ago, whose identities this project has no use for.
Deleted; fingerprint recorded first; **no redacted copy kept**, since keeping one preserves exactly
the liability the deletion removes. The aggregate score file (`KoNViD_1k_mos.csv` — each video's
average rating) and the per-video technical measurements are retained and contain no personal data.
Practical cost: none for anything planned. What we can no longer do: study how much individual raters
disagreed with each other. Full reasoning in `resources/reports/RES-002-privacy-deletion-log.md`.

## OBSERVED

**Work Package A — Devanagari material acquired**

| source | images | ground truth | licence as found |
|---|---:|---|---|
| `src_bstd_devanagari` | 25,246 | JSON, filename → Unicode transcription | images cc-by-sa-4.0; annotations **not_stated** |
| `src_indicstr12_devanagari` | 3,086 | per-image `*_gt.txt` Unicode labels | **not_stated** |
| `src_iiit_ilst_devanagari` | 1,390 | per-image XML, boxes + transcriptions | **not_stated** |

All are photographs of real signage with genuine blur, angle and lighting variation — not clean
synthetic renders, which RES-002 required because published evidence suggests clean synthetic text
may not separate a strong reader from a weak one.

**Work Package B — transient acquisition**

| source | archive | transferred | % | retained |
|---|---:|---:|---:|---:|
| VideoGen-RewardBench | 13.42 GB | 0.78 GB | **5.8%** | 288 videos, 755 MB |
| IndicSTR12 | 1.38 GB | 0.11 GB | 8.1% | 96 MB |
| IIIT-ILST | 0.64 GB | undercounted, see report | — | 55 MB |
| BSTD | 0.83 GB | 0.83 GB (no usable range on Drive) | 100% | 263 MB |

**Reading the whole index of the 13.42 GB archive cost 0.5 MB in 4 range requests — 0.004% of the
file, about six seconds.**

**Validation:** 30,010 new items, **all decode cleanly, 0 defects.** Corpus-wide: 34,786 items,
5.70 GB, 5 duplicate hashes (all pre-existing, in ImageRewardDB).

## INFERRED

- RES-001's `too_large_for_pilot` verdict was a **method limitation, not a property of the source**.
  Nothing about VideoGen-RewardBench changed; only what we knew how to do. Worth remembering when
  future sources look unobtainable.
- Having three independent Devanagari collections rather than one materially changes what Eval can
  claim. A checker measured against a single collection's photography may simply have learned that
  collection's cameras and fonts. Whether to hold one back as unseen is Eval's call, not mine.

## SURPRISES

**1. Language labels are not script labels — and this nearly cost a fifth of the material.** My first
BSTD selection filtered on `language == hindi`. But **Marathi is also written in Devanagari**: 5,109
images. A further 351 images labelled Punjabi, Bengali, Telugu, English and others also carry
Devanagari text. Switching to "does the transcription contain a Devanagari character" took the pool
from 19,773 to 25,246. **Flagged to Eval** — anyone subsetting this material should filter on script,
not language.

**2. Reading a 13 GB archive's index costs half a megabyte.** The asymmetry is larger than expected
and is what makes the method worth generalising.

**3. A rights-clear source was previously lost to packaging alone.** VideoGen-RewardBench was
Apache-2.0 and ungated the whole time. Only the container defeated us.

## FAILURES / BLOCKERS

- **IIIT-ILST first attempt failed** with HTTP/2 framing errors under concurrent range requests.
  Fixed by forcing HTTP/1.1, lowering concurrency to 2, and retrying — not by hammering the host. A
  side effect is that the transfer counter for that source undercounts; **left as measured rather
  than replaced with an estimate**, and labelled as such.
- **A slow first implementation.** My initial VideoGen-RewardBench fetch let Python's zip library do
  the reading, which issued dozens of tiny range requests per file: 41 files in 10 minutes. Rewritten
  to fetch each member in one request from its byte offset.

## DECISIONS NEEDED FROM CONTROLLER

**1. One judgement call I made, for review.** BSTD's creators publish their data via Google Drive.
An anonymous request gets Google's standard large-file **"Virus scan warning"** page. I treated that
as *not* an access gate and proceeded, because it asks for no account, no credential and no
agreement, and any anonymous visitor can continue past it — unlike a login or a terms checkbox.
**If you read that differently, say so and I will mark BSTD `blocked_access` and remove it.** It is
21% of the retained RES-002 material and the largest Devanagari pool.

**2. Rights on the Devanagari material are thin, and that limits use.** BSTD's *images* are
cc-by-sa-4.0 but its *annotations* say nothing; IndicSTR12 and IIIT-ILST state nothing at all. All
were acquired under the licence-silence policy for internal research and evaluation only. **They may
not be redistributed, used as training data, shipped to customers, or treated as production-cleared.**
If Eval's calibration results are ever to be published or shown to a customer, the rights question
must be reopened first.

**3. Should the transient method become standard?** It worked on three of four sources and reduces
both bandwidth and storage substantially. Making it the default for large public archives is a
Resources-policy change, so it is yours to make, not mine.

## CROSS-STREAM — `CROSS_STREAM`, proposed only

`resources/PROPOSED-INTEGRATION-CHANGE-RES-002-EVAL.md` filed. It tells Eval what is available, what
it does and does not test, and the language-vs-script trap. **Still missing:** no Devanagari
*generated* text and none in video — our actual observed failure has no public counterpart here, and
producing one needs generation spend, outside both RES-002 and EVAL-001.

## FILES

`resources/tasks/RES-002-CONTROLLER-BRIEF.md` · `resources/reports/RES-002-transient-acquisition.md`
· `resources/reports/RES-002-privacy-deletion-log.md` · `resources/PROPOSED-INTEGRATION-CHANGE-RES-002-EVAL.md`
· 3 new source records + updated `src_videogen_rewardbench.md` · updated registry and manifests
· `resources/scripts/remote_zip.py` + 3 fetch scripts · updated `resources/HANDOFF.md`

Raw media git-ignored throughout.

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.* Answer decision 1 first, since it determines whether 21% of
this material stays. Then let Eval consume the Devanagari pool under EVAL-001/002. Do **not** treat
the transcriptions as ground truth until a human Hindi reader has checked a sample — RES-002 kept
Resources out of that deliberately.

## CONFIRMATION

No benchmark or holdout built, no calibration run, no creative labelling, no generation, no new
source family, no gate crossed, no explicit restriction overridden, no disk-floor relaxation. The
only destructive actions were the explicitly approved KoNViD privacy deletion and transient-payload
deletion. RES-003 not started.
