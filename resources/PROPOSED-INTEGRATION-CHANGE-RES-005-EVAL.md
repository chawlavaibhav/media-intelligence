# Proposed integration change — RES-005 → Eval

**Severity:** `CROSS_STREAM` · **Status:** PROPOSED, not actioned · **Date:** 28 Aug 2026
**Filed by:** Resources, task RES-005 · **Branch:** `work/res-005-mat-av-min-acquisition`

Resources proposes; it does not act. Nothing in Eval's tree was edited by this task.

---

## The finding in one sentence

Two frozen documents describe the material called **MAT-AV-MIN** differently, and under one of
them the twelve clips just acquired qualify, while under the other they do not exist at all.

## What the two documents say

**Eval — `eval/v1/instruments/FAMILY-4-TEMPORAL-VIDEO.md`:**

> "The base clips are the whole blocker. They need not be generated: **any rights-cleared clean
> footage with a person, a product and on-screen text would serve**, since we are testing the
> *instrument*, not a generator."

Under this reading the base is defined by **content and rights**. Any clean, cleared footage works.

**Resources — `eval/pre-execution-integration/EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml` and
`resources/pre-execution-freeze/CONTROLLED-PACK-REQUIREMENTS-v2.yaml`:**

```
MAT-AV-MIN:
  from_pack: PACK-AV-CLEAN
  minimum_for_stage_Q: "12 clean single-speaker clips"
```

and `PACK-AV-CLEAN` is `storage_class: B_controlled_permissioned` — controlled recording with
**separate written consent for likeness and for voice**, verified verbatim transcripts, and a
declared language balance. Its stated reason for self-supply is:

> "A perturbation base needs clips whose only defect is the one introduced. **A controlled
> recording satisfies that better than KoNViD-1k**, which was sampled for degradation variety."

Under this reading the base is defined by **capture control**, and it cannot be acquired at all
until the Controller approves a consent instrument — gate 2 of five in
`RIGHTS-ACQUISITION-PLAN.md`, still open.

## Why the difference is material rather than cosmetic

It is the difference between a lane that is **open today at zero cost** and a lane that is
**blocked on a legal decision that may need external counsel**.

- Under the Eval reading, `temporal_video` — **9 capabilities, the cheapest large unblock in the
  whole plan** — needs only rights-cleared clean footage, which RES-005 has now obtained for ₹0.
- Under the Resources reading, the same 9 capabilities sit behind the consent instrument, behind
  73 person-hours of AV acquisition effort, and behind transcription and turn-boundary annotation
  that the temporal family does not use at all.

The temporal family injects its own truth. It never reads a transcript, never attributes a turn,
and never needs a language balance. Those requirements exist for the **speech** capabilities that
share `PACK-AV-CLEAN`, not for the temporal ones.

## What RES-005 actually acquired, stated plainly

Twelve clips from twelve distinct works, every one under a licence a human can open and read:
Creative Commons Attribution, Attribution-ShareAlike, CC0, or US-Government public domain. No
CC-BY-NC. No YouTube ripping, no reposts, no social-media downloads, no request-corpus or
user-uploaded identity footage.

They satisfy the **Eval reading** and are measured against it.

They **do not** satisfy `PACK-AV-CLEAN`. They carry no consent instrument, no verified transcript,
no turn boundaries and no language balance, and they are not controlled captures. Resources
records them as a **distinct material set**, not as PACK-AV-CLEAN members, precisely so that
acquiring them cannot be mistaken later for partial satisfaction of the AV pack's obligations.

## What Resources proposes — and does not propose

**Proposes:** that Eval and the Controller record which of the two readings governs MAT-AV-MIN,
in one place, and that the losing wording be corrected rather than left standing.

If the Eval reading governs, the cleanest correction is to rename what RES-005 produced so it
stops borrowing the AV pack's name — for example `MAT-TEMPORAL-BASE` — and to change the stage
map's `from_pack: PACK-AV-CLEAN` to a supply route that does not imply consented capture.

If the Resources reading governs, RES-005's twelve clips are **not** the Stage-Q perturbation base,
the temporal lane returns to blocked-on-consent, and the clips should be held as an unqualified
internal set or discarded.

**Does not propose:** any change to `PACK-AV-CLEAN` itself. Its consent, transcript, turn-boundary
and language requirements are correct for the five speech capabilities that consume it, and
nothing here weakens them. The `>=6 clips at >=20 s continuous` evidence-driven requirement is
also untouched — RES-005's clips are 10 seconds and are not offered against it.

**Does not propose:** starting speech/audio evaluator qualification. That remains blocked and
RES-005 did not touch it.

## The narrower question underneath

Even if the Eval reading governs, one of Resources' stated reasons for controlled capture survives
and should not be lost: a perturbation base wants footage whose **only** defect is the injected
one. RES-005 therefore screens every clip mechanically for pre-existing freezes, black frames,
interlacing and near-static content, and reports the results per clip rather than asserting
cleanliness. That screen is evidence about **these** clips; it is not a claim that publicly
licensed footage is generally as clean as a controlled capture.

## Files

- `resources/pre-execution-freeze/mat-av-min/` — spec, acquisition record, measurements, manifests,
  lineage manifest, Controller Brief.
- `resources/scripts/acquire_mat_av_min.py`, `qualify_mat_av_min.py`,
  `build_mat_av_min_manifest.py`.

No file outside `resources/**` was modified.
