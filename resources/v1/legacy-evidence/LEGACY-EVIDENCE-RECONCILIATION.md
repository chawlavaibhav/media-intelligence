# Legacy evidence reconciliation

**Task:** R2 / R8 legacy tranche of `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md`
**Date:** 26 Aug 2026 · **Branch:** `work/resources-v1-overnight`
**Register:** `legacy-evidence-register.csv` (10 pools, each ending in exactly one outcome)

---

## Why this exists

The handoff said, vaguely, that "two small internal pools also exist" and that a 64-image
human-scored set "remains in the `media-factory` repo". Vague is the problem: nobody could tell
whether that material was retrievable, partly retrievable, or gone. The runbook's rule is that every
known legacy pool must end in exactly one state — **`recovered`**, **`metadata_only`** or
**`unavailable`** — after a bounded, documented search. No "some old assets exist" may survive.

## Result in one table

| Outcome | pools | meaning |
|---|---:|---|
| `recovered` | **5** | Bytes accessible in this cloud session, hashes captured. |
| `metadata_only` | **2** | The record and evaluation survive; the media bytes do not. |
| `unavailable` | **1** | Concrete search performed; no retrievable artifact anywhere. |
| `unavailable_in_cloud_session` | **2** | Exists somewhere, but not reachable from GitHub in this session. |

**10 of 10 pools resolved. Zero vague states remain.**

## Where I searched, exactly

- `chawlavaibhav/media-factory` — cloned in full (6.0 MB), **all 6 remote branches**, and every commit
  reachable from any ref, enumerated by `git rev-list --all` + `git ls-tree -r`. That is the whole
  repository history, not just `main`.
- `chawlavaibhav/media-intelligence` — the working tree of `work/resources-v1-overnight`, plus the
  unmerged branches named by the GOV-001 audit.
- I did **not** search any laptop, local Downloads folder or local working directory. None is
  reachable from a cloud session and pretending otherwise would be fabrication.

## The find that matters: the 64-image scored set is half-recoverable

`media-factory` commit `57b2cca` ("spike: consistency + film-generation R&D harness") carries a
`spike/.gitignore` that excludes generated media with `out/*` — but then whitelists three exceptions:

```
out/*
!out/.gitkeep
!out/costs.jsonl
!out/scores.json
```

Whoever wrote that made a good call. It means the **judgements survived even though the images did
not.** So:

**`recovered` — the evaluation record.** `spike/out/scores.json`
(`sha256 8d928dac…`) holds all **64** human pass/fail judgements with a free-text note each. It
reconciles exactly with what `canon/findings/FINDINGS-11-empirical-knowledge-join.md` claims about it:
**64 items, 10 failures, nano-banana-pro 7 of 32, seedream 3 of 32** — an 84% pass rate. Structure:
2 image models × 8 scenes × 4 takes.

**`recovered` — the cost ledger.** `spike/out/costs.jsonl` (`sha256 645efb90…`), 129 lines,
**$35.28 total** across 11 model/step labels. This is the most directly useful legacy artifact the
project has for its primary metric, because it is a real prior example of **cost recorded per
attempt, next to the outputs** — which is precisely what Cost per Accepted Outcome needs and what
`EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` now formalises.

Two honesty notes on the ledger, both from the file and script themselves: the dollar figures are
**July-2026 fal.ai list prices hardcoded in `run.mjs`, not billed amounts**, and the script's own
comment says the ledger **over-counts failed round-1 video attempts**. It is a historical reference,
not a price list.

**`metadata_only` — the 64 images themselves.** They were never committed. The gitignore excluded
them and no branch or reachable commit contains them. Consequence, stated plainly: the project
**cannot re-annotate those failures for all visible defects**, which is what
`docs/superpowers/plans/2026-08-26-eval-capability-lab-v1-master-plan.md` R6 asks for, until someone
with access to the original machine makes the bytes available. The scores tell us *that* a face
drifted; without the image nobody can check *how badly*, or score it for the other defects present.

## The negative result worth as much as the find

`spike/guddu/` holds **19 committed images**, and before opening them they were the most plausible
candidate in the whole project for a ready-made person-reference pack — 19 images, apparently one
production, `REQ-CAP-11` needs 32.

**They are not a person pack.** I opened them. They are **AI-generated illustrated narrative frames**
— storyboard stills from a short story film ("Pixels to Dawn"), used as start frames for
image-to-video. There is no photographed person, no identifiable individual and therefore no
identity to reference. `spike/film.mjs` confirms the use: each frame is an input still with a motion
prompt.

This matters because it is exactly the mistake this reconciliation was meant to prevent. "19 images
of a character" reads like supply in a spreadsheet. It is not supply. `PACK-PERSON-REF` remains
completely empty, and the person pack still requires consented capture. Recorded as `recovered`
(the bytes are real and hashed) with `valid_v1_use` explicitly excluding identity reference.

A related point about the spike's own character: `spike/brand.json` defines it as a *"Pixar-style 3D
animated character"* described entirely in prose. The legacy project's own identity work used a
**described fictional character, not a real person**. That is a genuinely relevant precedent for R4's
person-pack routes and is carried into that document.

## Three first-party brand marks are real supply

`spike/refs/` holds three committed logo assets, and visual inspection confirms `aight_logo.png` is
the project's **own** "Aight" wordmark — a first-party demo brand, so there is **no third-party
trademark exposure**. That makes them the only material in the entire project that legitimately
serves `REQ-CAP-09` `logo_wordmark_fidelity` today.

The limit is resolution, not rights: 680×240, 237×74 and 204×33 pixels. Two of the three are under
240 px wide, which is thin for fidelity testing. So: **3 of ≥12 marks, usable, small.** `REQ-CAP-09`
is `partial` rather than `missing` because of these three files.

## What is gone, and what is merely out of reach

- **`unavailable`** — `spike/guddu/_contact.jpg`, excluded by gitignore line 7, never committed,
  absent from every branch and reachable commit.
- **`unavailable_in_cloud_session`** — `spike/refs/Fraunces.ttf` (the pinned display font) and the
  EVAL-005 `build/` items. Both are the *same failure shape*: **a build that depends on an
  uncommitted font asset cannot be reconstructed from GitHub alone.** The project already knows this
  about EVAL-005; it is now recorded that the legacy spike has the identical hole. I took no action
  on the EVAL-005 item — it is Eval-owned and listed only so the pattern is visible in one place.

## Two observations routed, not acted on

While enumerating history I checked the two "evidence not on `main`" items the GOV-001 audit raised
as High. Both are **cloud-accessible on their unmerged branches**:

| GOV-001 row | Artifact | Confirmed present on |
|---|---|---|
| R1 | `canon/findings/CANON-001-…`, `CANON-002-…`, and the `molly-bang` knowledge directory | `origin/work/canon-003-a` |
| R2 | `READER-A-FREEZE.md`, `READER-ATTESTATION.md` | `origin/work/eval-004` |

**This is good news and it is not mine to act on.** The evidence is not lost, only unmerged. Those
are Canon and Eval files; Resources may not edit another stream's outputs. Routed to the Controller
as an observation only.

## What this reconciliation does not claim

- It does **not** claim the recovered bytes are fit for any V1 purpose. `valid_v1_use` and
  `invalid_use` are recorded per pool in the register, and most rows are historical evidence only.
- It does **not** promote any historical human judgement to current ground truth. The 64 pass/fail
  calls are one unblinded rater, no protocol, no repeats, no second reader. They are a **vocabulary
  of failures this project actually hit**, and a candidate regression list — nothing more. Eval, not
  Resources, decides what a failure label means.
- It does **not** search exhaustively. The rule is a bounded search with documented locations, and
  the locations are named above.
