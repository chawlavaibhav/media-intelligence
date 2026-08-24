# Resources — Handoff

**PURPOSE:** Discover, licence-check, sample and validate independent media/data, keeping
evaluation media separate from the knowledge being tested.

**CURRENT STATE:** No dataset downloaded. A research plan exists listing candidate external
datasets (`corpus/CORPUS-SOURCING-PLAN.md`) — Pitt Ads, Pick-a-Pic, HPD v2, ImageRewardDB, AVA,
T2I-CompBench, GenEval, VBench and others — **every entry marked licence-unverified**, none
accessed. Two small internal pools exist: `corpus/finding-01-samples/` (14 images used in the
Devanagari checker calibration) and a larger 64-image human-scored set that remains in the
`media-factory` repo (`spike/out/`), not yet copied here.

**CURRENT APPROVED DECISIONS:** External dataset labels are not ground truth for Canon or Eval —
they're one source's observations under one rubric. Where a dimension matters, fresh blind human
annotation against our own rubric is required. Evaluation media must stay independent of the
knowledge under test — do not select "hierarchy" examples because a book about hierarchy exists.

**LAST COMPLETED TASK:** none — this stream has not executed yet, only been planned.

**CURRENT TASK / QUEUE:** none.

**IMPORTANT OBSERVATIONS:**
- The most valuable public gap found in planning: **no public Devanagari text-rendering benchmark
  appears to exist.** If confirmed, this becomes a build-it-ourselves item — small, cheap, and
  genuinely proprietary.
- Four domains have no adequate public corpus at all: Devanagari rendering, Indian commercial
  creative with intent labels, short-form feed-native assets with performance data, and any
  creative-to-commercial-outcome linkage. All four likely require building rather than sourcing.

**OPEN QUESTIONS:** licence terms for every listed dataset (nothing verified). Whether Pitt Ads
media may be used beyond internal research. Storage/budget ceiling for any download.

**DEPENDENCIES:** Eval needs a battery designed before Resources knows exactly what corpus
properties matter most. Canon's curriculum gaps (Indian context, Devanagari) point directly at
what Resources should prioritise sourcing or building.

**PROPOSED CROSS-STREAM CHANGES:** none filed yet.

**NEXT APPROVED TASK:** none — do not self-assign. Suggested candidate (not started): RES-001,
verify licence terms for Pitt Ads Dataset and the Devanagari-benchmark question, before any
download.
