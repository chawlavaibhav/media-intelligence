# RES-001 — Source assessment (Phase 1: discovery, verification, rights)

**Date:** 24 Aug 2026 · **Status:** Phase 1 complete for 8 of 9 approved families. No media downloaded yet.
**Method:** each candidate was resolved to its official distribution point, and the page and any readme
were read directly. Rights were recorded as six separate fields. Nothing below is inferred from the
`CORPUS-SOURCING-PLAN.md`, which is a candidate pool, not evidence.

---

## Headline finding

**Every media type we can legitimately obtain is AI-generated. Every source of real, human-made
media is blocked.**

This was not the expected shape. `CORPUS-SOURCING-PLAN.md` named real advertising as the one thing
we cannot substitute. It is the one thing this pilot cannot get.

| | Families | Outcome |
|---|---|---|
| **Generated media** | 3 of 3 assessed | All three open, Apache-2.0, ungated |
| **Real / human-made media** | 4 assessed, 1 not assessed | All four blocked, each for a different reason |

The four real-media blocks are independent, which is what makes the pattern worth reporting — it is
not one bad link or one awkward licence.

| Source | Blocker | Type of blocker |
|---|---|---|
| Pitt Image and Video Ads | "To obtain the dataset for research purposes, please email us." | Human permission decision |
| AVA | Authors distribute image lists only; media obtainable only by scraping dpchallenge.com or via torrent | Distribution method we may not use |
| LSVQ | Download form must be completed | Human permission decision |
| KoNViD-1k | Files are directly downloadable, but no licence is stated anywhere | Rights ambiguity |

---

## Approved for download (3 families)

All three state Apache-2.0 on their official pages and showed no login, agreement or access-request
gate. Apache-2.0 clearly permits the internal research and evaluation use RES-001 authorises.

| source_id | What it is | Media | Size | Pilot plan |
|---|---|---|---|---|
| `src_imagerewarddb` | Expert preference over generated images, with alignment / fidelity / harmlessness scored separately | Generated images (from DiffusionDB) | 1K-scale subset = 2.7 GB | Take 1K-scale whole |
| `src_videofeedback` | Generated video scored on 5 aspects incl. temporal consistency | Generated video | 8.81 GB total | Bounded deterministic subset |
| `src_videogen_rewardbench` | Pairwise preference over video from **12 different generators** | Generated video | 13.4 GB total | Bounded deterministic subset |

**Why these three and not more of the same.** `src_imagerewarddb` is the only one that separates
evaluation dimensions, which is the closest public analogue to our own split between technical
fidelity and creative fitness. `src_videogen_rewardbench` is the only one with wide generator
diversity, so evaluator behaviour can be tested across model styles rather than one house look.

**One honest caveat on all three.** The publishers assert Apache-2.0 over media that are outputs of
third-party commercial generators (Kling, Luma, Gen3, Minimax and others). Whether a dataset
publisher can license those outputs is not something we verified independently. For internal
research and evaluation this is the normal position and the stated terms cover our use. It would
need a real answer before any use beyond that.

---

## Blocked, with reasons

### `src_pitt_ads` — blocked_access
Two independent blockers, either sufficient. First, images are obtained by emailing the authors —
a human permission decision that RES-001 clarification 4 forbids crossing. Second, even with URLs
in hand the media sit on third-party sites, so acquisition would be scraping. Videos are supplied
as an ID list, not media. No licence statement exists on the official page or in the readme, and the
media are advertisements under brand copyright.

**This is the loss that matters.** It was the sourcing plan's first priority and the only proposed
source of real commercial creative with intent annotations.

### `src_ava` — blocked_access
The official package contains image lists and annotations only. The authors do not distribute the
photographs at all. The two available routes — scripted scraping of dpchallenge.com, or an academic
torrent — are both explicitly prohibited by RES-001. Rights over the contest photographs are also
unstated.

### `src_lsvq` — blocked_access
Free to the research community but behind a download form. The associated repository also notes the
automatic form reply has been broken and that some videos may no longer be retrievable from their
original sites, so the practical state of the distribution is uncertain even for someone who does
complete the form.

### `src_pvp` — blocked_license
Repository code is MIT. The **dataset** licence is not stated. The paper describes images as partly
DALL-E generated and partly sourced through Google Image Search; the web-sourced portion carries
third-party copyright with no stated clearance.

**Recorded because it is the exact trap this project warns about:** a web search summary asserted the
dataset is "available under the MIT license." That is a paraphrase of the *code* licence. Media
rights are not inferred from a code licence, so the claim was not accepted.

### `src_konvid1k` — blocked_license, and the one worth a Controller decision
This is the only real-media candidate that is both openly downloadable and budget-compatible:
1,200 videos, 2.3 GB, a direct zip link, no login, no form.

**It is blocked on rights, not access.** No licence appears on the database page or the site root;
the footer carries only a copyright notice. The official page describes the source videos as
Creative Commons sequences drawn from YFCC100M, but does not identify which CC variant applies to
which video. YFCC100M mixes commercially-usable CC licences with NonCommercial ones, and we are a
commercial entity — so "CC" alone does not answer our question.

Under RES-001 clarification 3 this is ambiguous, and ambiguous means stop. Flagged rather than
resolved, because resolving it is a legal judgement reserved to the Controller.

### `src_youtube_ugc` — candidate_not_downloaded, **not assessed**
No verification was performed. Recorded as unassessed rather than unavailable. No claim is made
about its status either way.

---

## What this means for the corpus

**Coverage we will have:** generated images and generated video, with three different human
annotation styles (expert dimensional ratings, multi-aspect scores, pairwise preference) across
roughly 13+ distinct generative models.

**Coverage we will not have:** any real photography, any real advertising, any human-made video, any
commercial creative, and — unchanged from the sourcing plan's own gap table — anything Indic-script,
Indian-market, or short-form feed-native.

**The consequence, stated plainly:** this pilot can support work on *how AI-generated media fails and
how evaluators judge it*. It cannot support any claim that involves comparison against real
professional creative work. That is a real limit on what the corpus can be used to test, and it
should be recorded before anyone designs an experiment assuming otherwise.

Whether this changes the project's plan is a Controller decision. It is reported here, not acted on.
