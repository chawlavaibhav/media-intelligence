# Controller Brief — RES-001

**TASK:** RES-001
**STATUS:** needs_controller_review
**STAGE:** Phase 0 — bootstrap and comprehension complete. Acquisition not started.
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

---

## WHAT I DID

Phase 0 only. Bootstrapped the Resources worktree, confirmed branch `work/resources`, fetched
origin, and fast-forwarded cleanly from `0a831ca` to `b891fc3` (9 commits, no conflicts, tree clean
before and after). Read the Project Contract, Control State, Autonomy Policy, Runbook, Resources
Charter, Resources Handoff, RES-001 and the Corpus Sourcing Plan, plus `.gitignore`, the Assumptions
register, Workstream Status and the Capability Lab V0 plan. Verified local tooling and storage
without contacting any external service. Produced a comprehension report and a blocking-question
list for the Controller.

## OBSERVED

- Worktree, branch and fast-forward as above; no local commits, no dirty state, no force operations.
- `.gitignore` ignores `resources/corpus/raw/`, `staging/` and `tmp/` only — confirmed by
  `git check-ignore`. `resources/corpus/finding-01-samples/` is **committed raw media** and is not
  ignored, so path-based protection is narrow rather than blanket.
- Single internal volume, 228 GB, **22 GB free (89% full)**. No external volume, no Google Drive
  desktop mount, no other cloud-sync mount.
- Tooling present: `curl`, `ffmpeg`, `ffprobe`, `shasum`, `tar`, `unzip`, `python3` 3.14.6.
  Absent: `git-lfs`, `wget`, `aria2c`, `jq`, and the Python libraries `requests`, `PIL`,
  `huggingface_hub`, `datasets`, `numpy`.
- `RES-001` approves nine candidate families. Three — KoNViD-1k, LSVQ, YouTube-UGC — appear in no
  other project document. Approximately ten datasets discussed at length in
  `CORPUS-SOURCING-PLAN.md` do not appear in RES-001's approved list.
- The token `PVP` appears exactly once in the repository, in RES-001, and is defined nowhere.
- `CORPUS-SOURCING-PLAN.md` states its own provenance is prior knowledge with a May 2026 cutoff and
  marks every licence *unverified*.
- The plan names Pitt Ads as the highest-priority source and simultaneously records its media as
  scraped advertising where third-party copyright almost certainly applies.
- Broken cross-references: `eval/battery/CAPABILITY-LAB-V0-PLAN.md` links a non-existent
  `EVAL-CORPUS-PLAN.md`; `coordination/ASSUMPTIONS.md` links `CANON-EXPERIMENT-V0.md` and
  `CAPABILITY-LAB-V0-PLAN.md` as if they were siblings. Both are outside Resources' write scope.

## INFERRED

*Interpretation, not measurement.*

- A material share of the approved candidate list is likely to return `blocked_access` or
  `blocked_license` rather than media, given how much of this ecosystem sits behind account,
  token or click-through gates that RES-001 defines as stop conditions.
- YouTube-UGC in particular looks self-contradicting as specified: approved "if legitimately
  accessible" while scraping is prohibited, and such datasets typically distribute links rather
  than media.
- The KoNViD-1k / LSVQ / YouTube-UGC group is natural-video *technical quality* material, a
  different research purpose from the sourcing plan's generated-video and creative-preference
  framing. Their inclusion may be deliberate and undocumented, or may be an error.
- The absent `git-lfs` may block several sources outright, since it is the standard transport for
  large dataset repositories.

## SURPRISES

- Disk headroom (22 GB) was smaller than the original 20 GB hard stop assumed. No project document
  recorded a storage assumption of any kind. Now resolved by Amendment 01.
- The repository already contains committed raw media, which sits in tension with the instruction
  that raw payloads must not be committed.

## FAILURES / BLOCKERS

Four blocking questions remain open (see DECISIONS NEEDED). No acquisition has begun.

## ASSUMPTIONS CHALLENGED

None yet. Nothing in Phase 0 bears on `coordination/ASSUMPTIONS.md`.

## LOCAL IMPLICATIONS

Under the amended budget the pilot is firmly a breadth exercise: roughly 1.5–2 GB per family across
three families. Large video datasets are effectively excluded except as deterministic subsets, and
subset selection rules become load-bearing — they are the point in this task nearest to the
selection bias the Resources charter exists to prevent.

## CROSS-STREAM IMPLICATIONS

None to propose. Tagged `LOCAL`. The broken cross-references above are documentation hygiene in
other streams' directories; raised here rather than edited.

## ARCHITECTURAL IMPLICATIONS

None. No schema or architecture change is implied, and none would be made without a stop.

## DECISIONS NEEDED FROM CONTROLLER

**Resolved:** B1 storage — closed by Amendment 01.

**Open, blocking:**
- **B2** — Does the RES-001 candidate list replace `CORPUS-SOURCING-PLAN.md` or select from it?
  Are Pick-a-Pic, HPD v2, Persuasion Strategies, VBench, T2VQA-DB, MARIO-Eval and AnyText inside
  the approved envelope? What is the rationale for KoNViD-1k / LSVQ / YouTube-UGC?
- **B3** — What dataset does `PVP` refer to?
- **B4** — Rights assessed against internal-research-only use, or use that may support commercial
  product development? This determines whether "research use only" passes or blocks.
- **B5** — Confirm that any free-account, credential or terms-acceptance gate is an automatic stop.

**Open, non-blocking:** priority order; storage path; deterministic subset rule; local tooling
installation; bias/coverage axes; confirmation that no holdout or strata are built in RES-001.

## FILES CREATED / MODIFIED

- `resources/tasks/RES-001-CONTROLLER-BRIEF.md` — created (this file)
- `resources/HANDOFF.md` — budget line updated to reflect Amendment 01

No other file created or modified. No network access. No downloads. No terms accepted. No accounts
created.

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.* Answer B2–B5, then authorise Phase 1 (source discovery and
official-source verification, no downloads) so that rights assessment can complete before any
acquisition decision is made.

## CONFIRMATION

No unapproved next strategic step was started. No external research, dataset access, terms
acceptance, download, paid API call, benchmark construction or creative labelling has occurred.
