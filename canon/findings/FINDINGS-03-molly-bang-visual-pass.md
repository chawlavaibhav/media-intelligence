# Finding 03 — Molly Bang visual-context pass

**Date:** 23 Aug 2026 · **Cost:** ₹0 (local render) · **Inputs:** 21 pages rendered at 80dpi, 17 inspected
**Scope:** resolve the 15 atoms flagged `visual_context_required: true`. No vocabulary promotion, no Pass 2.

## Method finding — the source argues in minimal pairs

Four of Bang's demonstrations are **controlled single-variable comparisons**:

| Pair | Held constant | Varied |
|---|---|---|
| p55 / p57 | same red triangle, same ground | vertical position only |
| p63 / p65 | same burst, same colours | centred vs off-centre |
| p70 / p71 | dark mass on white, same area | jagged contour vs curved contour |
| p75 / p77 | same six shapes, same positions | colour uniform vs colour varied |

This matters for how much these atoms can be trusted. They are not assertions with a decorative
illustration — the confound is held constant and the reader sees the isolated effect. Confidence
raised on `mb_001` and `mb_010` (0.85 → 0.9) and `mb_016` (0.75 → 0.8) on that basis.

## Atoms revised

**`mb_013` colour_association_dominates_shape_association — principle sharpened.**
The pair shows more than the prose does. p75 is six shapes all in red: grouping falls back to
shape. p77 is the same six shapes in red and black: colour grouping overrides shape entirely.
So the operative rule is not "colour beats shape" but **colour dominates when colour varies;
shape grouping is what remains available when colour is uniform.** That is directly usable —
it says a uniform palette makes shape a controllable grouping cue, and a varied one does not.

**`mb_011` point_versus_curve_register — scope widened.**
Both figures are a dark landmass against white sky. The effect is demonstrated on **the dominant
contour of a mass**, not on individual pointed objects, and value is held constant across the pair.
Principle updated to say so.

## Atoms weakened

**`mb_007` horizontal_reads_as_calm — confidence 0.85 → 0.7.**
p43 divides the frame into a white field over a black band. That demonstration is not a clean
isolation of horizontality: it also carries strong light/dark value contrast, which `mb_012`
independently claims is an emotional cue. Two principles are doing work in one figure. Exception
recorded.

**`mb_017` isolation_by_surrounding_space — confidence 0.75 → 0.6.**
Two problems. The isolated triangle in p84 also sits **higher in the frame** than the cluster, so
the demonstration confounds isolation with vertical position (`mb_001`). And Bang does not assert
the principle — her caption asks an open question about whether differing shape, size or colour
would make the figure feel *more* isolated. The atom as written was firmer than the source.
Both recorded as exceptions.

## Confirmed unchanged

`mb_002` (p63 centre), `mb_005` (p80 — four contrast panels, explicitly a combination of the
others), `mb_006` (p69 red on black; p91 Sue Jensen), `mb_009` (p51 floating diagonal, no
baseline), `mb_015` (p87 base-height progression), `mb_016` (p86 overlap joining two triangles
into one range), `mb_018` (p66 — circle inside, red square breaking the frame edge).

## Unresolved — internal inconsistency in Pass 1

Three atoms are marked `visual_context_required: true` but carry **empty `figure_refs`**:

```
mb_004  size_as_strength
mb_008  vertical_reads_as_energy
mb_012  ground_value_safety_register
```

They could not be resolved by this pass because they name no figures to inspect. Either the
extractor should have cited pages, or the flag should have been false. Left as-is — the fix is
a judgment call about extractor behaviour, not a mechanical correction.

## Candidate observation — not written as an atom

p87 contains a cue the prose does not mention: a full-height black band running off the right
frame edge, with no visible base, reads as the **nearest** element. Depth from base-height
progression is what the text describes; depth from an element that exceeds the frame is visible
in the figure only.

Not written as an atom. It would be my inference from a picture rather than something the source
states, and promoting it would be exactly the drift the two-pass rule exists to prevent.
Recorded here for human review.

## Net effect

```
18 atoms
 4 revised (2 sharpened, 2 weakened)
 7 confirmed unchanged
 3 unresolvable — no figure references
 4 not requiring visual context
 1 candidate observation held for review
```

No atom moved from `pending_vocabulary` to `operational`. Vocabulary remains unpromoted.
