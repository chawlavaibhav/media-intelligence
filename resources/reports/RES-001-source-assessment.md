# RES-001 — Source assessment

**Date:** 24 Aug 2026 · **Status:** all 9 approved families assessed; 4 acquired.
**Method:** each candidate resolved to its official distribution point; licence, terms, `robots.txt`
and access conditions read directly from that source. Rights recorded as six separate fields.
Nothing is inferred from `CORPUS-SOURCING-PLAN.md`, which is a candidate pool, not evidence.

> **This report was rewritten after Controller clarifications 6–7.** Its earlier conclusion —
> *"every media type we can legitimately obtain is AI-generated; every source of real human-made
> media is blocked"* — was **correct under the previous rights policy and is now superseded.**
> The change is recorded rather than erased, because the reversal is itself the finding.

---

## The finding

**The binding constraint was the rights policy, not availability.** Not one source changed. Under the
old rule the pilot could acquire no real human-made media at all. Under the new one, real media is
the majority of the corpus by item count.

But the reversal is partial, and the part that survived matters:

| Blocker type | Survived the policy change? |
|---|---|
| Licence not stated | **No** — no source is now blocked for this |
| Login / email / form gate | **Yes** — 3 sources |
| Explicit terms prohibition | **Yes** — 1 source |
| Distribution format | **Yes** — 1 source |

Every hard blocker still sits on real human-made media. That pattern was not an artefact of the old
rule; it is a property of how media that people own is distributed.

---

## Acquired

| source_id | Domain | Items | Bytes | Rights as found |
|---|---|---:|---:|---|
| `src_konvid1k` | Real natural video | 1,200 | 2.41 GB | **not_stated** |
| `src_youtube_ugc` | Real UGC video | 5 | 0.86 GB | **explicit CC BY 4.0** |
| `src_imagerewarddb` | Generated images + expert preference | 2,584 | 1.13 GB | apache-2.0 stated |
| `src_videofeedback` | Generated video + 5-aspect scores | 987 | 0.18 GB | apache-2.0 stated |

**KoNViD-1k** — 1,200 real 8-second clips. Ungated direct zip; `robots.txt` absent on the file host
and the database host does not disallow the dataset page. No licence anywhere. The official page
describes the videos as Creative Commons from YFCC100M but names no variant, and the distributed
metadata carries `flickr_id` but **no licence field** — checked directly, not assumed. Acquired under
clarification 6 with rights recorded `not_stated`/`not_verified`. The `flickr_id` means a future
rights review could resolve per-video status if a use beyond internal evaluation is proposed.

**YouTube-UGC** — the best-documented source in the pilot, and the one Phase 1 never assessed.
Distributed by Google from a public GCS bucket (`ugc-dataset`), anonymous, ungated. **No YouTube
endpoint is touched**, so YouTube's `robots.txt` restrictions on `/get_video` are not engaged. The
bucket carries an explicit `LICENSE` (Creative Commons Public License) and an `ATTRIBUTION` file
naming each clip's original work, author, and "licensed under CC BY 4.0". Only 5 clips because the
originals are pre-transcode files of 0.06–5 GB each; selection is the first 360P clip of each
distributor-defined category, in sorted order.

**ImageRewardDB** — the distributor's **complete validation split**, taken whole, so no selection
judgement of ours enters the corpus. The only source that scores alignment, fidelity and quality
separately — the closest public analogue to our own technical-versus-creative split.

**VideoFeedback** — every addressable file on the media repo's main revision. Carries
temporal-consistency labels, the axis relevant to the cross-frame observation-unit problem.

---

## Blocked

**`src_pvp` — `blocked_access`.** HuggingFace reports `gated: auto` on `holi-lab/PVP`: automatic
approval, but still login plus terms acceptance. Clarification 6 does not waive gates. Separately
checked the ungated `holi-lab/visual_persuasion` — it holds only annotations and training JSON, **no
images**, so it is not the PVP media and was not substituted (clarification 2).

*Recorded because it is the exact trap this project warns about:* a web search asserted the PVP
dataset is "available under the MIT license." That is the repository **code** licence. Media rights
are never inferred from a code licence, so the claim was not accepted.

**`src_ava` — `blocked_license`, on stronger grounds than before.** Reassessed expecting the
licence-silence rule to unblock it. Instead, `dpchallenge.com/terms.php` explicitly prohibits: *"use
a robot, spider or other device or process to monitor the activity on or copy pages from the
DPChallenge.com Web Site"*, and *"You may not reproduce or distribute any information available from
the Website... You shall not store or aggregate such information in any manner."* The site also
states *"All digital photo copyrights belong to the photographers and may not be used without
permission."* `robots.txt` does not blanket-disallow — the `User-agent: *` block is commented out —
but the terms of service do, and terms control.

**`src_pitt_ads` / `src_lsvq` — `blocked_access`.** Email request and download form respectively;
both are human permission decisions, and clarification 7 keeps them blocked absent separate
authorisation.

**`src_videogen_rewardbench` — `too_large_for_pilot`. A format block, not a rights block.**
Apache-2.0 and ungated, but the media ship as one 13.42 GB `videos.zip` with no addressable per-item
path. A bounded subset would require partial-archive range techniques the pilot should not depend on;
peak need would be ~26.8 GB against an 8 GB cap. Its 12-generator diversity exists nowhere else in
the corpus and is the strongest candidate for a later, larger acquisition.

---

## Two things that do not fit the rights fields

**Personal data.** `KoNViD_1k_subjective.csv` ships crowdworker **IP addresses, worker IDs and
city/country**. Nothing in the six rights fields would have caught this. Flagged for Controller
decision; nothing deleted.

**Stale identifiers.** `THUDM/ImageRewardDB` now 307-redirects to `zai-org/...`, and
`KwaiVGI/VideoGen-RewardBench` to `KlingTeam/...`. Any older reference to those paths is stale.

**One unreconciled discrepancy.** VideoFeedback's dataset card claims 37.6k pairs / 8.81 GB; its
media repo's main revision exposes 987 files / 0.18 GB. Recorded as observed, not explained.
