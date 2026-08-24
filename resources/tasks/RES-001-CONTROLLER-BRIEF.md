# Controller Brief — RES-001

**TASK:** RES-001
**STATUS:** needs_controller_review
**STAGE:** Phase 1 — source discovery, official-source verification and rights assessment complete
for 8 of 9 approved families. No media downloaded yet.
**Opened:** 24 Aug 2026 · **Last updated:** 24 Aug 2026

> **Working document.** Completed and finalised at the end of RES-001. Controller amendments are
> recorded here as they are issued, per Controller instruction of 24 Aug 2026.

---

## CONTROLLER AMENDMENTS

### Amendment 01 — RESOURCE BUDGET (storage) · issued 24 Aug 2026

Supersedes the storage line of the `RESOURCE BUDGET` section in `resources/tasks/RES-001.md`.

`RES-001.md` is deliberately left unedited. The task file is Controller-owned, and the RUNBOOK
warns against reopening a task with a materially different method under the same ID. The Controller
directed that this amendment be recorded in the Controller Brief, so the Brief is the authoritative
record of the amended budget. **Anyone reading `RES-001.md` alone will see the superseded figures.**

| Item | Original RES-001 | Amended (Amendment 01) |
|---|---|---|
| Target retained / downloaded corpus | 10–15 GB | **4–6 GB** |
| Hard stop | 20 GB | **8 GB** |
| Free local disk floor | not specified | **maintain 10–12 GB free at all times** |
| Pre-download headroom check | not specified | **mandatory — STOP before starting if it would be violated** |
| Source processing order | not specified | **sequential; no concurrent large-archive downloads** |
| Archive retention | not specified | **delete after successful extraction + validation, under five conditions below** |
| Cloud / object storage | not specified | **not to be introduced as part of RES-001** |

**Unchanged by this amendment:** diversity over volume; success condition remains at least three
meaningfully distinct usable source/domain families where legitimately accessible; ₹0 / $0 paid
APIs; do not chase item count; do not fill the storage budget for its own sake.

#### Archive deletion — pre-authorised only when all five hold

1. the official source remains reproducibly downloadable;
2. the exact source / version / URL is recorded;
3. the download script is saved;
4. the downloaded archive **or** the resulting files carry appropriate checksums;
5. extraction and validation completed successfully.

This is a Controller pre-authorisation of an action that would otherwise fire Autonomy Policy
trigger 7 (IRREVERSIBILITY). It is scoped to archives only.

**Explicitly still prohibited:** deleting validated media merely to make room without recording
what happened. Where a source requires retaining both archive and extracted media and doing so
would threaten the disk headroom, the correct responses are a smaller deterministic subset or
`too_large_for_pilot` — never exceeding the budget, and never a silent deletion.

#### Operating rules derived from Amendment 01

Recorded so the arithmetic is auditable rather than improvised mid-run.

- **Free-space floor read conservatively as 12 GB**, being the stricter end of the stated 10–12 GB
  range. Flagged to Controller; will be revised if 10 GB was intended.
- **Measured free space at time of amendment: 22 GB** on the single internal volume. No external
  volume and no cloud-sync mount exists on this machine.
- Therefore the **instantaneous on-disk ceiling for all RES-001 payload is ~10 GB** (22 − 12),
  against a retained hard stop of 8 GB. Transient headroom above retained is ~2 GB at the worst
  point, so permissible archive size shrinks as retained volume grows.
- **Gate evaluated before starting each source**, both conditions required:
  1. `retained_total + expected_extracted_size ≤ 8 GB`
  2. `free_space_now − (archive_size + expected_extracted_size) ≥ 12 GB`
  Failing either → subset deterministically, or mark `too_large_for_pilot`. Do not begin the
  download and hope.
- **Archive SHA256 is computed before deletion**, not after, so archive-level reproducibility
  remains verifiable once the file is gone.
- **Every archive deletion is logged** in `resources/reports/RES-001-integrity-report.md` with
  source_id, archive filename, bytes, SHA256, and confirmation of all five conditions.
- Free space is re-measured after each source, not assumed.

**Effect on Phase-0 blockers:** blocking question **B1 (storage) is resolved.** No disk cleanup is
required — 22 GB free supports the amended budget. B2–B5 remain open.

### Amendment 02 — RES-001 clarifications 1–5 · issued 24 Aug 2026

Received via the updated `resources/tasks/RES-001.md` (merged at `f41bebc`). These close all four
Phase-0 blocking questions. Recorded here so the Brief remains a complete record.

| Question | Controller answer | Effect on the work |
|---|---|---|
| B2 — which source list governs | `RES-001.md` governs. `CORPUS-SOURCING-PLAN.md` is a candidate pool, not a second approval list. | A plan dataset is usable only if it clearly sits inside an approved family. |
| B3 — what is PVP | **Personalized Visual Persuasion.** Use only that expansion; if no official distribution verifies, record unavailable rather than guess at a similar name. | Resolved and assessed. |
| B4 — licence bar | **Internal research and evaluation only.** A `research-only` label is not automatically sufficient. Non-commercial-only, academic-only, entity-excluding or ambiguous terms → `blocked_license` / `metadata_only`, no download. | This is a strict bar and it is what blocked KoNViD-1k and PVP. |
| B5 — access gates | Do not cross any account/terms/API-key/institutional gate. Record `blocked_access`, continue to the next approved candidate. Escalate the whole task only if the success criterion becomes unreachable, a human permission decision is needed, or ambiguity affects already-downloaded material. | Pitt Ads and LSVQ skipped without escalation; success criterion still met. |

Also confirmed in the amended task file: disk floor is **12 GB** (resolving the 10–12 GB range in
Amendment 01 in favour of the stricter figure, matching the conservative reading already adopted),
and archive deletion now explicitly requires the archive to be **fingerprinted before deletion**.

Clarification 5 is load-bearing for how Phase 1 should be read: *"Known blocked candidates are
evidence, not failure... Do not weaken the rights bar merely to reach three families or a byte
target."* No source below was admitted by relaxing the bar.

---

## WHAT I DID

**Phase 0.** Bootstrapped the Resources worktree on `work/resources`, fast-forwarded to `origin/main`,
read the governing documents, verified tooling and storage locally, and reported four blocking
questions without starting work.

**Phase 1.** After the Controller answered all four and issued Amendments 01–02, merged `origin/main`
(`f41bebc`), acknowledged `shared/COMMUNICATION-STANDARD.md`, then resolved 8 of the 9 approved
source families to their official distribution points and read the licence, terms and access
conditions directly from those pages. Recorded rights as six separate fields per source. Downloaded
no media.

## OBSERVED

*Directly read from the named official pages on 24 Aug 2026.*

**Open and licence-clear (Apache-2.0 stated, no gate seen):**
- `THUDM/ImageRewardDB` — licence `apache-2.0`, code MIT. Subsets 1K/2K/4K/8K at 2.7 / 5.5 / 10.8 / 20.9 GB. Images collected from DiffusionDB.
- `TIGER-Lab/VideoFeedback` — licence `apache-2.0`; annotation rows only. Media are in a separate repo, `hexuan21/VideoFeedback-videos-mp4`, licence `apache-2.0`, 8.81 GB, 37,662 rows.
- `KwaiVGI/VideoGen-RewardBench` — licence `apache-2.0`, 13.4 GB, 25,234 rows, actual `.mp4` files, videos from 12 named T2V models.

**Blocked:**
- Pitt Ads `readme_images.txt` states: *"To obtain the dataset for research purposes, please email us."* Videos supplied as `final_video_id_list.csv`, not media. No licence statement on the page or readme.
- AVA — official package is image lists and annotations only; media obtainable only by scraping dpchallenge.com or via an academic torrent.
- LSVQ — free to researchers but a download form must be completed; repo notes the automatic form reply was broken and some videos may no longer be retrievable.
- PVP — repository LICENSE is MIT (code). Dataset licence **not stated**. Paper describes images as partly DALL-E generated, partly sourced via Google Image Search.
- KoNViD-1k — direct zip at `datasets.vqa.mmsp-kn.de`, 2.3 GB, 1,200 videos, **no login or form**. No licence stated on the database page or site root; footer is a copyright notice only. Page describes sources as Creative Commons sequences from YFCC100M without identifying the variant per video.

**Not assessed:** YouTube-UGC. No verification performed; no claim made.

**Storage:** 22 GB free before any download. Amended budget is 4–6 GB target / 8 GB stop / 12 GB floor.

## INFERRED

*Interpretation, not measurement.*

- The blocked/open split falls almost exactly along generated-vs-real media. Four real-media sources are blocked for four different reasons, which suggests a structural pattern rather than four coincidences: media that humans own tends to be gated, un-relicensable, or distributed only as links.
- KoNViD-1k is the highest-value unblock available. It is the only real-media candidate that is ungated, budget-sized and one decision away from usable.
- Because ImageRewardDB's images come from DiffusionDB (Stable Diffusion era) while the video sets come from 2024–2025 generators, the corpus will skew old on the image side and current on the video side. Relevant to any later claim about "current" model behaviour.
- The publishers of all three open sets assert Apache-2.0 over outputs of third-party commercial generators. For internal evaluation the stated terms cover us; the publishers' authority to grant that is unverified and would matter for any wider use.

## SURPRISES

- The single most important source in `CORPUS-SOURCING-PLAN.md` (Pitt Ads, "the one thing we cannot substitute") is unobtainable under RES-001's rules — and would have been even without the rights question, because the images are distributed as URLs to third-party sites.
- KoNViD-1k publishes a completely open download link while stating no licence at all. Open access and clear rights turned out to be independent properties.
- A web search summary confidently asserted the PVP *dataset* is MIT-licensed. It is the repository code that is MIT. This is the precise error `resources/HANDOFF.md` warns against, appearing unprompted in a search result.

## FAILURES / BLOCKERS

None that stop the task. Five candidates are blocked and recorded as evidence per clarification 5.
The success criterion — at least three distinct usable source families — is met without weakening
the rights bar. One Controller decision (KoNViD-1k) could materially improve corpus coverage.

## ASSUMPTIONS CHALLENGED

None yet. Nothing in Phase 0 bears on `coordination/ASSUMPTIONS.md`.

## LOCAL IMPLICATIONS

Planned acquisition, ~5.7 GB, inside the 4–6 GB target:

| Source | Plan | Approx |
|---|---|---|
| `src_imagerewarddb` | 1K-scale subset whole | 2.7 GB |
| `src_videofeedback` | bounded deterministic subset | ~1.5 GB |
| `src_videogen_rewardbench` | bounded deterministic subset | ~1.5 GB |

Two of three need a subset rule, which is the point in this task closest to the selection bias the
Resources charter exists to prevent. The rule will be content-blind and deterministic — the official
split where one exists, otherwise a fixed selection over sorted item IDs, with the rule and seed
recorded in the manifest. Never a content-aware choice.

## CROSS-STREAM IMPLICATIONS

Tagged **`CROSS_STREAM`**, proposed only, not acted on.

The corpus this pilot can legitimately build contains **no real human-made media at all**. Eval work
that assumes access to real professional creative for comparison would be planning against media we
do not have and currently cannot get through open channels. `EVAL-001` is designing the battery now,
so the constraint is worth knowing before it hardens into a design.

No `PROPOSED-INTEGRATION-CHANGE` filed yet — filing one is proposed, pending the Controller's view
on whether this rises above information-sharing.

## ARCHITECTURAL IMPLICATIONS

None. No schema or architecture change is implied, and none would be made without a stop.

## DECISIONS NEEDED FROM CONTROLLER

**All Phase-0 blockers closed.** B1 by Amendment 01; B2–B5 by Amendment 02. Acquisition is not
blocked and proceeds under the amended budget.

**One decision worth making, not blocking:**

- **D1 — KoNViD-1k.** 1,200 real videos, 2.3 GB, direct download, no login or form. No licence is
  stated; the official page describes the videos as Creative Commons from YFCC100M without naming
  the variant per video, and YFCC100M mixes commercially-usable and NonCommercial licences. Under
  clarification 3 this is ambiguous, so it is blocked and untouched.
  **This is the only route to real human-made media found in the entire approved list.** Options are
  (a) leave blocked; (b) authorise checking whether the distributed metadata identifies per-video CC
  licences, and if so acquire only the commercially-usable ones as a documented deterministic subset;
  (c) treat the paper's CC provenance as sufficient. (b) is the only one that resolves the ambiguity
  with evidence rather than assumption; it is proposed, not assumed.

- **D2 — YouTube-UGC.** Not assessed. Assess it, or close it as out of pilot scope?

**Non-blocking, proceeding on stated defaults unless corrected:** subset rule as described under
LOCAL IMPLICATIONS; raw media into the git-ignored `resources/corpus/raw/<source_id>/`; descriptive
bias axes only; no holdout or strata built in RES-001.

## FILES CREATED / MODIFIED

- `resources/tasks/RES-001-CONTROLLER-BRIEF.md` — this file
- `resources/HANDOFF.md` — budget line updated for Amendment 01
- `resources/manifests/source-registry-v0.csv` — 9 sources, all 23 required fields
- `resources/sources/*.md` — 9 per-source rights records
- `resources/reports/RES-001-source-assessment.md` — Phase 1 findings
- created empty: `resources/scripts/`, `resources/corpus/raw/` (git-ignored)

No media downloaded. No account created, no terms accepted, no gate crossed, no paid API called.
Public dataset pages and readmes were read; that is the source verification RES-001 puts in scope.

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.* Proceed to Phase 2 — acquire the three approved sources
(~5.7 GB), checksum, validate, manifest and report — which is already authorised under the amended
task and needs no further approval. Separately, answer D1, because the corpus's single largest gap
(no real human-made media) hangs on that one rights question and it is cheap to resolve.

## CONFIRMATION

No unapproved next strategic step was started. No external research, dataset access, terms
acceptance, download, paid API call, benchmark construction or creative labelling has occurred.
