# Class B — failures that cannot be faked with Unicode

**Status: SPECIFICATION ONLY. No image was generated. This layer requires model spend the
Controller has not authorised, and none was incurred.**

---

## The boundary, stated plainly

The deterministic battery renders a *different string* to create a mismatch. That works because a
renderer draws exactly what the string says.

It also bounds what the battery can test. **A renderer always produces well-formed glyphs.** Give
it any string at all and it will draw clean, correctly-shaped letters. It will never draw:

- a ligature that half-formed and then gave up;
- two letters bleeding into one another;
- a stroke that belongs to no character;
- a headline bar (शिरोरेखा) that breaks in the middle of a word.

Those are not exotic. They are what generated Devanagari actually looks like when it fails — our
own recorded failures include a sign whose misspelling *drifted between frames of one clip*, which
no string substitution can reproduce.

**So the deterministic battery tests whether a checker autocorrects a well-formed wrong word. It
does not test whether a checker autocorrects malformed glyphs.** Those are different questions and
the second may well be harder. Claiming the first covers the second would be the central
dishonesty available here.

---

## Class B taxonomy

| # | Class | What it looks like | Why Unicode cannot produce it |
|---|---|---|---|
| B1 | **Malformed glyph topology** | a shape with roughly the right silhouette but wrong internal structure | no codepoint denotes "a broken ka" |
| B2 | **Fused characters** | adjacent letters merged into one blob | the renderer separates glyphs by design |
| B3 | **Broken / partial characters** | missing strokes, a letter drawn half-height | every glyph is drawn complete |
| B4 | **Shirorekha discontinuity** | the horizontal bar breaks mid-word, or runs on past the word | shaping joins the bar correctly by construction |
| B5 | **Visually ambiguous strokes** | a form genuinely between ब and व | Unicode forces a discrete choice |
| B6 | **Diacritic collision** | a matra overlapping the letter or another mark | positioning is handled correctly by the shaper |
| B7 | **Inconsistent baseline / scale** | one letter larger or offset within a word | a single text run is laid out uniformly |
| B8 | **Wrong contextual form** | a positional variant used in the wrong place, beyond the reph/rakar cases | the shaper picks the correct form |
| B9 | **Within-clip drift** *(video)* | the same sign reading differently across frames | a still image cannot express it |

**B9 is ours.** It is recorded in this repository: a generated clip whose Devanagari sign read
`सुवह की` in frames 1–4 and `सुवह के` in frames 5–6. No public benchmark we found covers it.

---

## How a later layer should test these

**Do not build this until the Controller authorises generation spend.** Specified now so the
boundary is explicit and the design is ready.

### Sourcing

Three routes, in decreasing order of ground-truth strength:

1. **Real generator output** — prompt an image model for known Hindi text and keep what it
   produces. Highest external validity; **ground truth is unknown** until a human reads it, so it
   inherits the whole EVAL-003 reference problem.
2. **Controlled glyph corruption** — render cleanly, then apply a deterministic, recorded image
   transform (stroke erosion, local warp, clipping) to a *known* region. Ground truth is
   "corrupted at this location by this operation"; **the pixels are known by construction**, which
   is the property that makes this layer tractable at all. Recommended starting point.
3. **Hand-authored** — a designer draws specific malformations. Highest control, lowest volume,
   needs skilled time.

**Route 2 is recommended first**, for the same reason the deterministic battery works: the answer
is known without asking anyone. The corruption is applied by us, so "does this still match the
target?" has a defensible answer even when no reader has seen it.

### The honest limit of route 2

A programmatic warp is not the same distribution as a diffusion model's failures. It tests whether
a checker notices *damage*; it does not prove the checker notices *the damage generators actually
produce*. Route 1 is the only thing that proves that, and route 1 needs human reference.

### Required properties for a Class B layer

- **Balance** — same 50/50 discipline, so "always fail" is not a strategy.
- **Severity ladder** — corruption strength varied and recorded, because the interesting result is
  the threshold at which a checker stops noticing, not a single pass rate.
- **Localisation** — record *where* the corruption is, so per-region sensitivity is measurable.
- **A clean-control arm** — uncorrupted renders in the same pipeline, to separate "notices damage"
  from "rejects everything".
- **Human confirmation on a sample only** — see `NATIVE-VALIDATION.md`. Route 2 needs a human to
  confirm the corruption is *perceptible*, not to establish what the text says.

### What it would cost

Generation spend, unlike the deterministic battery which costs nothing to build. A first pass at
~50 corrupted items plus ~50 clean controls is small, but it is **not ₹0** and requires a separate
Controller authorisation with a named model roster.

---

## What the deterministic battery may and may not claim

**May claim:** a checker that fails the deterministic battery cannot be trusted to verify generated
Devanagari. Failing on *well-formed* wrong text is disqualifying on its own — the easier case.

**May not claim:** that a checker which passes will catch malformed generated glyphs. That is
untested until Class B is built, and it must be stated wherever a deterministic result is reported.
