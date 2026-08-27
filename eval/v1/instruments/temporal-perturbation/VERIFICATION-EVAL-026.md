# EVAL-026 — verification record

**Date:** 28 Aug 2026 · **Branch:** `eval/eval-026-temporal-perturbation-qualification`
**Machine:** macOS (Darwin 23.6.0), arm64 · Python 3.14.6 · ffmpeg/ffprobe 8.1.2 (local, no account)
**pytest 9.1.1 in a throwaway virtualenv outside the repository**, matching the convention already
used for EMP-001.

**Model/evaluator/provider calls: 0 · External API calls: 0 · Consumed spend: USD 0 · Human labels: 0**

---

## What was verified, and what it does and does not prove

Every line below is something that was **run**, not something that was designed. None of it proves
that any checker can detect any of these defects — no checker has been run, and none can be until
the approved base clips exist. What it proves is that the machinery for asking that question is
correct, reproducible, honest about its own limits, and free.

---

## 1. Tests

```
$ python3 -m pytest -q eval/v1/instruments/temporal-perturbation/tests
153 passed in 15.90s
```

Grouped by what they defend:

| File | Tests | What would break if these were absent |
|---|---|---|
| `test_clipseq.py` | 15 | A clip could load partially, or a swapped frame could pass unnoticed. |
| `test_perturbations.py` | 68 | An "injected defect" could change nothing, land outside its recorded interval, differ between runs, or name a capability outside the frozen family. |
| `test_pack_build.py` | 17 | The pack could ship a duplicate fixture, a tampered fixture, an empty manifest, or silently lose coverage. |
| `test_qualify_temporal.py` | 23 | An incomplete run could be reported as a score; a blind spot could hide inside an average; frames could be counted as independent trials; the code could award a qualification. |
| `test_contract_alignment.py` | 8 | This package could drift away from the frozen capability list or acquire a threshold. |
| `test_ingest.py` | 15 | The real-clip path could be untested until the day the clips arrive. |
| `test_validate_package.py` | 7 | The zero-spend claim could be an assertion rather than a check. |

---

## 2. Pack build, on constructed stand-in material

```
$ python3 eval/v1/instruments/temporal-perturbation/build_perturbation_pack.py --build --rebuild-check
base clips              12
perturbed fixtures      146
clean controls          12
corrupt controls        7 (all refused, as required)
perturbation types      13
skipped (recorded)      10
material classes        constructed_stand_in
approved qualification pack: False
external calls 0 · human labels 0 · spend USD 0.0

manifest: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-026/eval/v1/instruments/temporal-perturbation/fixtures/pack/MANIFEST.json
fingerprint written to eval/v1/instruments/temporal-perturbation/STANDIN-PACK-FINGERPRINT.json
rebuild reproducibility: IDENTICAL
rebuild reproducibility: IDENTICAL
```

**Reading that in plain terms:** twelve clean stand-in clips produced 146 broken fixtures across 13
kinds of break, plus the same twelve clips untouched as clean controls, plus seven deliberately
unreadable artifacts that the loader refused — as it must. The rebuild produced hash-identical
output, so the pack is reproducible from committed code alone.

`approved qualification pack: False` is the lock working: this material is constructed, so nothing
built on it can be reported as a qualification.

---

## 3. Verification of the built pack

```
$ python3 eval/v1/instruments/temporal-perturbation/build_perturbation_pack.py --verify
PASS - every fixture present, hash-identical, and every corrupt control still refused.
```

`--verify` re-reads every frame of every fixture from disk, re-derives its hash, checks it against
the manifest, checks each perturbed fixture still differs from its source, checks the recorded
interval is inside the clip, and re-attempts every corrupt control to confirm it still fails to
load.

---

## 3b. Committed fingerprint

The built frames are git-ignored; `STANDIN-PACK-FINGERPRINT.json` is committed instead. A reviewer
on a fresh clone rebuilds and proves they got the same pack:

```
$ python3 .../build_perturbation_pack.py --build --check-fingerprint .../STANDIN-PACK-FINGERPRINT.json
committed fingerprint: MATCHES
```

Unlike the Devanagari battery, this carries **no rebuild risk**: nothing here depends on an
uncommitted font or any proprietary asset. The clips are drawn by committed, standard-library-only
code with integer arithmetic and no unseeded randomness.

---

## 4. Capability coverage on this build

| Frozen capability | Fixtures | Independent clips | Perturbation types |
|---|---:|---:|---|
| `action_adherence` | 24 | 12 | `frame_reversal`, `segment_reordering` |
| `camera_framing_fidelity` | 12 | 12 | `framing_discontinuity` |
| `motion_action_quality` | 48 | 12 | `frame_drop`, `frame_duplication`, `frame_freeze`, `frame_reversal` |
| `multi_shot_spatial_continuity` | 14 | 12 | `midclip_horizontal_flip`, `shot_horizontal_flip` |
| `person_stability_in_clip` | 12 | 12 | `identity_splice` |
| `product_stability_in_clip` | 12 | 12 | `product_region_substitution` |
| `sequence_state_continuity` | 12 | 12 | `segment_reordering` |
| `technical_visual_integrity` | 60 | 12 | `frame_drop`, `frame_duplication`, `frame_freeze`, `midclip_horizontal_flip`, `technical_corruption` |
| `text_logo_stability_in_clip` | 24 | 12 | `text_glyph_substitution`, `text_region_mutation` |

Coverage warnings on this build: **none**.

All nine frozen `temporal_video` capabilities have injected truth. Two of them
(`action_adherence`, `camera_framing_fidelity`) have it in the negative direction only — see
`PERTURBATION-SPEC.md` §7.

---

## 5. Scoring harness, exercised without any checker

The harness was run against fabricated answers with a deliberate flaw, to show the report catching
it. These answers come from no instrument and mean nothing about any instrument.

```
$ python3 .../qualify_temporal.py --manifest .../MANIFEST.json --selftest-profile blind_to_text
status                 unmeasurable
registry_use_permitted False
reason                 The protocol ran, but against material class ['constructed_stand_in']. ...
opportunities (clips)  12
false passes (missed)  24 of 146 perturbed fixtures
false fails (clean)    0 of 12 clean controls

recall per perturbation type (never averaged):
  frame_drop                      12/12  clips 12/12
  frame_duplication               12/12  clips 12/12
  frame_freeze                    12/12  clips 12/12
  frame_reversal                  12/12  clips 12/12
  framing_discontinuity           12/12  clips 12/12
  identity_splice                 12/12  clips 12/12
  midclip_horizontal_flip         12/12  clips 12/12
  product_region_substitution     12/12  clips 12/12
  segment_reordering              12/12  clips 12/12
  shot_horizontal_flip             2/2   clips 2/2
  technical_corruption            12/12  clips 12/12
  text_glyph_substitution          0/12  clips 0/12   <-- the planted blind spot
  text_region_mutation             0/12  clips 0/12   <-- the planted blind spot
```

**Why this matters:** a checker with that profile would score 12/13 defect types perfectly. Averaged,
it would look excellent. Reported per type — as the frozen gate requires — the blind spot is the
first thing you see, and it happens to be the failure this project cares about most.

Status is `unmeasurable`, and stays `unmeasurable` even when told there are five repeats and an
approved pass mark, because the material is constructed.

---

## 6. Zero-spend check

```
$ python3 eval/v1/instruments/temporal-perturbation/validate_package.py
PASS - 15 files scanned: no network or provider import anywhere, subprocess only for local ffmpeg/ffprobe, no invented pass mark in any module.
```

This is a static check on our own code: no HTTP client, socket, or provider SDK is imported
anywhere in the package including its tests; the only external binaries it may invoke are local
ffmpeg and ffprobe; and no numeric pass-mark constant appears in any module.

---

## 7. The real-clip path, proven today

No real footage exists yet, so `tests/test_ingest.py` encodes video locally with the same ffmpeg the
ingest uses, then ingests it back. That covers:

- decode to frames, and normalisation to a declared integer frame rate;
- both hashes recorded, and their difference (the delivered file's bytes vs the normalised frames);
- determinism — the same file ingested twice gives the same sequence hash;
- a different target frame rate correctly produces a different material identity;
- region defaulting, and the `geometric_default` marker that records the weaker basis;
- deterministic shot-cut detection on a constructed cut;
- fail-closed on a missing file, an empty file, a non-video file, a too-short clip, a too-long clip
  and an empty config;
- **a full build from ingested clips**, which reports `is_approved_qualification_pack: true`, drops
  the stand-in caveat, records `text_glyph_substitution` as unavailable on footage we did not
  render, and — because these test videos have a featureless default text box — records the text
  mutation as **skipped with a reason** and raises a coverage warning rather than inventing a
  fixture.

That last point is the machinery refusing to fake a defect, on a real container, today.

---

## 7b. Fresh-clone reproducibility

The strongest form of the reproducibility claim: clone the pushed branch into an empty directory
and rebuild from nothing.

```
$ git clone --depth 1 --branch eval/eval-026-temporal-perturbation-qualification <repo> freshclone
$ cd freshclone && git rev-parse HEAD
960b2a771eb796e50157be2b2ede03f17d3592e0

$ python3 eval/v1/instruments/temporal-perturbation/validate_package.py
PASS - 15 files scanned: ...

$ python3 -m pytest -q eval/v1/instruments/temporal-perturbation/tests
153 passed in 9.14s

$ python3 .../build_perturbation_pack.py --build --check-fingerprint .../STANDIN-PACK-FINGERPRINT.json
committed fingerprint: MATCHES
```

**What this establishes:** a reviewer who has never seen this working directory can reproduce the
whole pack, hash for hash, from committed code alone. No font, no downloaded asset, no third-party
Python package, no network. This is the property the Devanagari battery could not offer, and it is
why the built frames are git-ignored without loss.

---

## 8. Timings, for anyone re-running this

| Command | Wall clock on this machine |
|---|---|
| `--build` (12 stand-in clips, 146 fixtures) | 220s (measured; an earlier run of the same build took 63s, so treat this as 1-4 minutes depending on machine load) |
| `--build --rebuild-check` | roughly twice a build, since it builds the whole pack a second time into a scratch directory |
| `--verify` | 3.7s |
| full test suite | 16.3s |

The perturbations are pure-Python pixel loops, which is why the build is measured in minutes rather
than seconds. That was a deliberate trade: no numpy, no OpenCV, no Pillow, nothing to install, and
therefore nothing that can drift between machines.

---

## 9. What remains unverified

| | |
|---|---|
| Any checker's ability to detect any of these defects | **UNKNOWN** — none has been run |
| Behaviour on real footage's noise, grain, compression and lighting | **NOT VERIFIED** — no real clips held |
| Whether the twelve delivered clips will carry declared regions and shot boundaries | **UNKNOWN** — a Resources/Controller decision |
| The family-4 pass mark | **DOES NOT EXIST** — a Controller decision, deliberately not invented |
| The temporal evaluator family's qualification | **NOT QUALIFIED. Not claimed.** |
