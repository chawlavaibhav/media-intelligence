# EVAL-026 — Stage-Q temporal-video evaluator qualification machinery

**Stream:** Eval / Capability Lab
**Date:** 28 Aug 2026
**Branch:** `eval/eval-026-temporal-perturbation-qualification`
**Base:** `origin/main` @ `0e24d6a1a4acce5e83b90fa7fe198db94a92dec5`
**Spend:** USD 0 · 0 model generations · 0 evaluator calls · 0 external API calls · 0 human labels
**Status: RETURNED FOR CONTROLLER REVIEW. NOT MERGED. NO INSTRUMENT IS QUALIFIED.**

---

## Why this was worth doing now

`EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml` names the temporal family the **cheapest large unblock
available to the project**: nine capabilities from twelve clean clips, with zero human labels,
because the truth is *injected* rather than annotated. Everything about that route was decided and
frozen. What did not exist was the code.

This task builds it, and builds it in a way that can be proven today, before the clips exist —
so that when Resources delivers, the only remaining step is pointing the builder at the files.

## What "truth by injection" means, plainly

Take a clean clip. Break it on purpose at a known moment, in a known way — hold one frame still
for half a second, splice in four frames of a different person, mirror one shot, alter the caption
from frame 30 onward. Because we performed the break, we already know exactly what is wrong and
exactly where. Nobody has to watch anything and write down an opinion.

The checker being tested is then asked two questions, and both matter:

- can it find the break we know is there? (**recall**)
- does it report a break in the clip we did *not* touch? (**false alarms**)

A checker that scores well on the first and badly on the second is useless, which is why the pack
includes every clip untouched as well as broken.

## Scope taken, and scope deliberately not taken

**Built:** thirteen deterministic perturbations covering all nine frozen `temporal_video`
capabilities; a hashable clip container that fails closed; local ffmpeg ingest for real footage;
the injected-truth manifest; clean and corrupt controls; the scoring harness; a static zero-spend
check; twelve constructed stand-in clips; 153 tests.

**Not built, deliberately:**

- **Audio/video synchronisation.** The family-4 document lists it, but the frozen qualification
  map files it under evaluator family 5, and the project holds no audio at all. Implementing it
  now would produce machinery with nothing to run on and would overstate this task's coverage.
- **Any pass mark.** No number in the frozen contracts says what recall is good enough for this
  family. None was invented. The harness returns `gate_verdict: undetermined`, and a static check
  fails the package if a threshold constant ever appears in the code.
- **Any capability.** Zero added, zero redefined. A test reads the frozen map directly and fails
  on drift in either direction.

## The two locks against overclaiming

1. **Constructed stand-in material can never produce a qualification.** The scoring harness returns
   `unmeasurable` whenever the pack is not built purely from supplied clips, no matter how good the
   answers are. The frozen family-4 condition is real footage, and a qualification does not
   transfer from coloured shapes on flat backgrounds to a real face.
2. **This code cannot emit `qualified` at all.** It raises if it tries. Promotion is a Controller
   decision against an approved pass mark that does not yet exist.

## Result

| | |
|---|---|
| Machinery builds, verifies, rebuilds identically | **OBSERVED** |
| Real-clip path works end to end on a locally encoded video | **OBSERVED** |
| Seven of nine temporal capabilities fully runnable once 12 clips land | **INFERRED** from coverage, verified on stand-ins |
| Two capabilities (`action_adherence`, `camera_framing_fidelity`) runnable in the negative direction only | **OBSERVED** limitation, recorded in the contract |
| Any instrument detects any of these defects | **UNKNOWN** — no instrument has been run |
| Temporal family qualified | **NO. Not claimed anywhere.** |

## Decisions this task did NOT make, and which need the Controller

1. **The family-4 pass mark.** Recall per type, false-alarm rate, and localisation are computed;
   what counts as passing is not decided and was not invented.
2. **Whether Resources declares regions and shot boundaries** with the twelve clips. Ingest works
   without them — it defaults boxes from frame geometry and records that weaker basis — but a
   defaulted box that lands on a featureless area cannot carry a text or product perturbation at
   all, and the pack records that as lost coverage rather than inventing a fixture. Declared boxes
   are geometry, not defect labels, so asking for them does not reintroduce human labelling.
3. **Whether the ingest frame-rate normalisation is acceptable as a stated condition** of any
   qualification earned on this pack.

## Artifacts

- `eval/v1/instruments/temporal-perturbation/` — the package, its spec, its contract and its tests
- `eval/v1/instruments/temporal-perturbation/README.md` — plain-English overview
- `eval/v1/instruments/temporal-perturbation/PERTURBATION-SPEC.md` — the protocol and its limits
- `eval/v1/instruments/temporal-perturbation/perturbation-contract.yaml` — machine-readable mapping
- `eval/v1/instruments/temporal-perturbation/STANDIN-PACK-FINGERPRINT.json` — committed proof of a
  reproducible build; the frames themselves are git-ignored and rebuild byte-identically
- `eval/v1/instruments/temporal-perturbation/clips.example.json` — the one file Resources' delivery
  needs alongside it
- `eval/v1/instruments/temporal-perturbation/VERIFICATION-EVAL-026.md` — the run record
