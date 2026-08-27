# Does Eval's existing temporal tooling actually accept these clips?

**Task:** RES-005 · **Date:** 28 Aug 2026 · **Spend: ₹0 / USD 0, entirely local**

EVAL-026 landed on `main` while this acquisition was running. It ships the perturbation
machinery and, importantly, a **real-clip ingest contract**:
`eval/v1/instruments/temporal-perturbation/ingest_clips.py`. Until now it has only been exercised
against stand-in clips its own `build_dummy_clips.py` generates.

So rather than *assert* that this material is usable, RES-005 ran Eval's own ingest against it.

## Result — 3 of 3 accepted, fail-closed checks passed

```
mavm-03  240 frames @ 24fps  10.0s  motion_load=0.011613  shots=4  (auto_detected)
mavm-06  240 frames @ 24fps  10.0s  motion_load=0.011035  shots=12 (auto_detected)
mavm-12  240 frames @ 24fps  10.0s  motion_load=0.023155  shots=1  (single_shot_assumed)
```

A representative subset was used deliberately: `MAVM-03` is the only clip with a photographed face
and a held object, `MAVM-06` carries the densest burnt-in text and a hard cut, `MAVM-12` is a
single-shot product study with photographed rather than rendered signage.

All three normalised to the contract's declared 24 fps without error. Nothing was skipped, and none
of the fail-closed conditions (missing tool, non-zero exit, truncated buffer, zero-frame decode,
under-length clip) fired.

**This is an acceptance check on the material, not evaluator qualification.** No perturbation pack
was built, no instrument was scored, and no Registry row exists or is proposed.

## Two things Eval should know before it runs the full pack

**1. Shot counts are threshold-dependent, and the two tools disagree.**
RES-005 measured `MAVM-06` at **2** shots; Eval's ingest auto-detected **12**. Neither is wrong —
RES-005 uses ffmpeg scene detection at 0.30, Eval uses mean absolute inter-frame change at 0.08,
and the clip contains a graphics-heavy sequence that crosses the lower threshold repeatedly.
**Eval's detector governs**, because the perturbation pack is built from Eval's shot boundaries.
The manifest's `shot_count_measured` should be read as *RES-005's screen for "does this clip cut at
all"*, not as the boundary list the pack will use.

**2. Ingest is disk-expensive, and it is easy to underestimate.**
Ingest expands every clip into per-frame PNGs. **Three 10-second clips produced 941 MB.** A first
attempt to ingest all twelve at once **exhausted the disk and failed mid-write** — the 3840×2160
clip alone is a large multiple of the others. Extrapolating, the full twelve need several
gigabytes, and the frames are a rebuildable intermediate, not evidence.

Practical consequence for whoever runs the qualification: ingest in batches, or downscale before
ingest, and check free space first. This is an operational warning from a real failure, not a
prediction.

## Reproducing this check

```
python3 eval/v1/instruments/temporal-perturbation/ingest_clips.py \
    --config <config listing the clips> --out-dir <scratch>
```

The config is built from `MAT-AV-MIN-MANIFEST.csv`, carrying each clip's `rights_ref` through, since
ingest refuses a clip with no rights record. `pack_ref` is deliberately recorded as
`MAT-AV-MIN (RES-005) - NOT PACK-AV-CLEAN`, because these clips are not members of that pack and
must never be counted against its consent, transcript or turn-boundary obligations.
