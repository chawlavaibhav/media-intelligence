# Family 4 — Temporal / video instruments

**Judges:** drift, continuity, motion, stability — defects that exist *between* frames.
**Status: NOT QUALIFIED. Pack does not exist — but it needs NO human labels and should be built early.**

**Unblocks 5 capabilities.**

---

## Why this family exists at all

A misspelling that **changes partway through a clip** does not exist in any
single frame. Look at one frame and you cannot see it, however good your checker
is. The same is true of identity drift, product morphing and screen-direction
violations across a cut.

These are not "harder" versions of image defects. They are **structurally
invisible at frame level**. That is why the observation unit is part of every
measurement, and why this family cannot be replaced by running family 3 on
sampled frames.

---

## The key insight: this pack is nearly free

Truth can be **constructed by perturbation** rather than annotated. Take a clean
clip and inject a defect at a known frame. The answer is then exact, and no
human labelled anything:

| Injected perturbation | Creates known | Tests |
|---|---|---|
| Freeze N frames | frame freeze at known index | stutter/freeze detection |
| Splice in frames from another clip | identity swap at known index | `person_stability_in_clip` |
| Substitute a different product region | product swap at known index | `product_stability_in_clip` |
| Alter rendered text from frame k onward | text mutation at known index | `text_logo_stability_in_clip` |
| Reverse a frame run | direction reversal | `motion_action_quality` |
| Flip one shot horizontally | screen-direction violation | `multi_shot_spatial_continuity` |
| Shift audio by known ms | known A/V offset | `audio_video_synchronisation` |

This is exactly the trick that made the Devanagari battery cheap. **Combined
with family 2, these are the two packs that need no human time — which is why
they should be built before the ones that do.**

## Gate — recall on known perturbations, and the sampling caveat

- **Detection recall** on injected defects, reported **per perturbation type**, never as one average. An instrument that catches freezes and misses text mutation is not "80% accurate"; it is blind to the failure that costs us most.
- **False-positive rate** on the unperturbed clean clips. A detector that flags drift in a perfectly stable clip is unusable.
- **Localisation accuracy** — does it report the defect near the frame where it was injected? Detection without localisation cannot drive repair.

⚠️ **The sample rate is part of the measurement.** A defect between two sampled
frames is invisible. Every result records `sampled_frames`, and an instrument's
qualification is valid only at or above the sample rate it was qualified at.

⚠️ **Frames from one clip are ONE trial.** Sampling 12 frames does not create 12
independent tests. Report independent clips alongside frame counts, always.

## Qualification inputs

| Need | State |
|---|---|
| Clean base clips to perturb | ❌ not held — the only real dependency |
| Perturbation code | ❌ not written (deterministic, straightforward) |
| Human labels | ✅ **none required** |
| Spend | ✅ **none** — perturbation and detection run locally |

**The base clips are the whole blocker.** They need not be generated: any
rights-cleared clean footage with a person, a product and on-screen text would
serve, since we are testing the *instrument*, not a generator.
