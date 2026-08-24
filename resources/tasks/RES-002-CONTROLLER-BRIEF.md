# Controller Brief — RES-002

**TASK:** RES-002 · Devanagari calibration material + transient large-source acquisition
**STATUS:** **CONTROLLER-APPROVED — CLOSED** · **Date:** 24 Aug 2026
**Closed:** 24 Aug 2026 by Controller sign-off. Substantive work and the consistency cleanup are
approved. All three decisions below are resolved; none remains open.

> **Standing rights limitation, carried past closure.** Everything acquired under RES-001 and
> RES-002 is for **internal research and evaluation only**. It may **not** be redistributed, used as
> training data, delivered to customers, or treated as production-cleared. Closing this task does not
> relax that. If results built on this material are ever to be published or shown outside the
> company, **the rights position must be revisited first** — several sources state no licence at all,
> and were acquired under the licence-silence policy precisely on the basis that use stays internal.

---

## WHAT I DID

Two things. **First**, closed the Devanagari gap: acquired **29,722 real photographed Devanagari
images with human transcriptions** from three collections (two independent lineages — see the
duplicates section). RES-001 had none, which is why Eval's Hindi-text checker was blocked.

**Second**, proved that a large public archive can be sampled without downloading it. RES-001 gave
up on VideoGen-RewardBench because its 13.42 GB arrives as a single zip. That was a wrong
conclusion, and this task overturns it: 288 videos across all 12 generators were acquired by
transferring **5.8% of the archive**, which was never written to disk.

Retained **1,170 MB** against a 2,048 MB budget. Free disk never fell below **14.5 GB** against a
12 GB floor. No account, no form, no terms accepted, no paid API.

## RES-001 FINALIZATION (all six items)

| Item | Done |
|---|---|
| 1. Duplicate claim | Corrected twice — see the dedicated section below. For the RES-001 corpus alone the figure is 5 duplicate hashes; for the **full corpus after RES-002 it is 200**, and the RES-002 additions turned out to carry a finding worth more than the number. |
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
34,586 distinct files, 5.70 GB of media.

## DUPLICATES — the figure changed, and the reason matters more than the figure

**Mechanically verified across the full corpus: 200 duplicate hashes among 34,786 items.** The
earlier "5" was correct for the RES-001 corpus of 4,776 items; RES-002 added 30,010 items and the
number moved with them. Nothing was recounted differently — the corpus grew.

| kind | hashes | what it is |
|---|---:|---|
| Within a single source | **27** | a source containing the same file twice |
| **Spanning two sources** | **173** | the same file present in two supposedly separate datasets |

| source | within-source | involved in cross-source | source items |
|---|---:|---:|---:|
| `src_bstd_devanagari` | 19 | 0 | 25,246 |
| `src_indicstr12_devanagari` | 3 | 173 | 3,086 |
| `src_iiit_ilst_devanagari` | 0 | 173 | 1,390 |
| `src_imagerewarddb` | 5 | 0 | 2,584 |

### The finding: two of my "independent" Devanagari sources are not independent

**173 files are byte-identical between IndicSTR12 and IIIT-ILST** — 12.4% of IIIT-ILST, 5.6% of
IndicSTR12. Both are releases from the same lab (CVIT, IIIT Hyderabad), so the newer dataset appears
to reuse images from the older one.

**This contradicts something I told you and told Eval.** I described three *independent* collections.
That is wrong: BSTD is genuinely independent, but IndicSTR12 and IIIT-ILST are related. Corrected in
the registry, both source records, the integrity report and the note to Eval.

**Why it matters practically.** The reason for wanting three collections was to allow one to be held
back as genuinely unseen test material — a checker measured only on photography it has already met
looks better than it is. If Eval holds back IIIT-ILST, **roughly one in eight of those images is not
unseen at all**; it is literally the same file that appeared in IndicSTR12. BSTD remains a clean
holdout candidate.

### A second, smaller finding

Two of BSTD's 19 within-source duplicate pairs **span its own train and test splits** — the same
image file appears on both sides of the distributor's own division. Small, but anyone using BSTD's
published splits as-is should know they are not perfectly disjoint.

**Nothing was deleted.** Removing the 173 overlaps would have improved the duplicate count and
erased the finding.

## RETAINED SIZE — three figures, all correct

Different numbers appear for the same source depending on what is being counted. None is wrong;
quoting one without saying which is what causes confusion.

| | BSTD | whole corpus |
|---|---:|---:|
| **Media bytes** (manifest — the evaluation payload) | 201.4 MB | 5.70 GB |
| **Folder bytes** (media + retained transcriptions, licences, member lists) | 224.3 MB | 5.74 GB |
| **Disk usage** (`du` — allocated filesystem blocks) | 263.9 MB | — |

BSTD shows the spread most sharply for two reasons. Its 17.1 MB of JSON transcriptions and 5.8 MB of
member lists are retained deliberately — **those transcriptions are what make it calibration material
rather than a pile of pictures.** And it holds 25,252 very small files, so filesystem block
allocation adds 23.3% on top of the actual bytes. KoNViD-1k, made of 1,203 large videos, shows ~0.1%
overhead by comparison.

My earlier chat figure of "263 MB" for BSTD was the `du` number. Against the 2,048 MB RES-002 budget
the relevant measure is retained bytes, and by either byte measure the task finished well inside it.

## INFERRED

- RES-001's `too_large_for_pilot` verdict was a **method limitation, not a property of the source**.
  Nothing about VideoGen-RewardBench changed; only what we knew how to do. Worth remembering when
  future sources look unobtainable.
- Having more than one Devanagari collection still materially changes what Eval can claim — a checker
  measured against a single collection's photography may simply have learned that collection's
  cameras and fonts. But it is **two** independent lineages, not three: BSTD on one side, and the two
  CVIT datasets on the other. Whether to hold one back as unseen is Eval's call; if they do, BSTD is
  the clean choice.

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

## DECISIONS — ALL RESOLVED AT CLOSURE

**1. BSTD's Google Drive interstitial — RESOLVED: accepted. BSTD remains.**

I had flagged a judgement call: BSTD's creators publish via Google Drive, and an anonymous request
gets Google's standard large-file **"Virus scan warning"** page. I treated that as *not* an access
gate and proceeded, because it asks for no account, no credential and no agreement, and any anonymous
visitor can continue past it — unlike a login or a terms checkbox.

**The Controller accepted that reading.** The interstitial is an **advisory on an anonymous download,
not an access gate** under current policy. BSTD stays in the corpus: 25,246 images, the largest
Devanagari pool, and the only Devanagari source independent of the other two.

*Scope of this ruling:* it covers an advisory interstitial that any anonymous visitor can pass. It
does **not** extend to logins, account creation, click-through terms, request forms or API keys —
those remain hard blocks, and are why `src_pvp`, `src_pitt_ads` and `src_lsvq` are still blocked.

**2. Rights on the Devanagari material — RESOLVED: limitation stands, unchanged.**

BSTD's *images* are cc-by-sa-4.0 but its *annotations* say nothing; IndicSTR12 and IIIT-ILST state
nothing at all. All were acquired under the licence-silence policy, which permits exactly one thing:
**internal research and evaluation.**

**This limitation is not lifted by closing the task.** The material may not be redistributed, used as
training data, shipped to customers, or treated as production-cleared. If Eval's calibration results
are ever to be published or shown to a customer, **the rights question must be reopened before that
happens, not after.** Closure records the work as complete; it does not grant any wider permission.

**3. Transient acquisition as the default — RESOLVED: approved and codified.**

The Controller approved making it the default for large, reliably reacquirable public archives. It is
now written into `resources/CHARTER.md` under *"Large public archives — transient acquisition is the
default"*: prefer range/member/stream access, **verify a real HTTP 206 before relying on it** (a host
that ignores Range replies 200 with the entire file, which defeats the purpose and can breach the
disk floor), retain the bounded subset plus reproduction metadata, do not keep the full archive once
extraction and validation succeed, and **never record a hash for an archive that was never
downloaded.**

That Charter section states explicitly that it changes **storage method only** and grants nothing
about rights — decision 2 above continues to govern.

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

*A recommendation, not an action taken. Decisions 1–3 are resolved; nothing here is blocking.*

Let Eval consume the Devanagari pool under EVAL-001/002. Two carry-forwards that closure does not
settle:

- **Do not treat the transcriptions as ground truth until a human Hindi reader has checked a sample.**
  RES-002 kept Resources out of that deliberately — they are other people's annotations, made for
  other purposes, and remain candidate calibration material until validated.
- **If a held-out Devanagari set is wanted, use BSTD.** IndicSTR12 and IIIT-ILST share 173
  byte-identical files, so holding out IIIT-ILST would leave roughly one image in eight not actually
  unseen.

Both are Eval's calls to make, not Resources'.

## CONFIRMATION

No benchmark or holdout built, no calibration run, no creative labelling, no generation, no new
source family, no gate crossed, no explicit restriction overridden, no disk-floor relaxation. The
only destructive actions were the explicitly approved KoNViD privacy deletion and transient-payload
deletion. RES-003 not started.
