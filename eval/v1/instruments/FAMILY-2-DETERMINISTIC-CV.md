# Family 2 — Deterministic CV / geometry instruments

**Judges:** counts, positions, colours, file properties — things with a right answer computable from the image itself.
**Status: NOT QUALIFIED — but its qualification pack was CONSTRUCTED IN THIS SESSION.**

---

## Why this family is the cheapest to qualify, and should go first

Everything here has a **right answer we can generate ourselves**. If we draw
three squares at coordinates we chose, we know there are three squares and where
they are. No human is needed to say so. That makes the qualification pack
**free** in human time — the single largest cost in every other family.

Two of the six families have this property (this one and temporal/video). They
should be qualified first for that reason alone.

**The important caveat:** "deterministic family" does not mean "deterministic
instrument". A *file probe* is deterministic. An *object detector* is a model
with error modes, and calling its output "deterministic" would repeat exactly
the error this project already paid for. The family splits in two:

| Sub-type | Needs qualification? |
|---|---|
| **File/metadata probing** — duration, aspect, resolution, fps, audio presence | No. Registry status `deterministic`. Must still **fail closed** on an unparseable file. |
| **Geometry over detected regions** — counting, positions, colour sampling | **Yes.** The detector is a model. |

---

## The pack — 100 synthetic known-answer fixtures

Built in this session: `eval/v1/instruments/fixtures/cv-geometry/`

Each fixture is a PNG drawn by code from a specification we chose, so its
answer is exact and its provenance is a seed, not a label. Ground truth ships
alongside as JSON.

| Category | Fixtures | What it tests |
|---|---:|---|
| Count | 30 | Exact cardinality, 1–8 objects, with and without overlap |
| Relative position | 25 | left/right/above/below between two named shapes |
| Absolute placement | 15 | Quadrant placement within the frame |
| Attribute binding | 15 | Which colour is on which shape — including deliberate swaps |
| Size / aspect | 15 | Relative size ordering and frame aspect ratio |

**Deliberately included, because a pack of only-correct examples cannot catch a
permissive instrument:**
- **overlapping objects**, where a naive detector merges or double-counts;
- **shadow-like grey duplicates**, which is the recorded trap — *counting and
  locating need different detector confidence settings; high when counting, so
  shadows are not counted as extra objects, lower when locating*;
- **same-colour distractors** of a different shape;
- **negative controls**: a blank image (answer: zero objects), and a corrupt
  file (correct behaviour: **fail closed**, not "0 objects found").

That last one matters. *An empty check is not a passing check* — an instrument
that reports "0 objects, all good" on a file it could not decode has failed, not
passed, and only a deliberately broken fixture catches it.

### Gate

- **Exact agreement on every count and relation fixture.** No tolerance — the answers are integers and directions, not estimates.
- **Colour within a declared tolerance in a declared colour space.** ⚠️ The tolerance is a judgement call, must be declared and approved **before** the run, and changing it afterwards is an experiment-mutation stop.
- **Fails closed on the corrupt fixture.** Non-negotiable.
- **Detector confidence recorded** as a condition on every result. The same detector at two settings is two instruments.

### Reporting rule

**Counting and positioning are separate results even when they share software.**
A model can place a cup correctly beside a laptop and still draw two laptops.
Shared instrument, separate Registry rows.

---

## Qualification inputs

| Need | State |
|---|---|
| Synthetic fixture pack | ✅ **built in this session, 100 fixtures + negative controls** |
| Fixture generator reproducible from a seed | ✅ deterministic, re-runnable |
| Detector software choice | ❌ not selected |
| Colour tolerance approved | ❌ judgement call, needs Controller approval |
| Human time | ✅ **none required** |
| Spend | ✅ **none required** — runs locally |
