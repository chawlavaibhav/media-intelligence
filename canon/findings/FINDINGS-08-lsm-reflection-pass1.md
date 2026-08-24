# Finding 08 — Light: Science & Magic, ch.3 (Pass 1)

**Date:** 23 Aug 2026 · **Source:** Hunter, Biver, Fuqua & Reid, 5th ed., ch.3
**Mode:** source-only Pass 1, isolated. EPUB single-column, extracted clean.

## Human learning notes

The chapter's claim is that photographic lighting is **reflection management**. Light reaching a
subject is transmitted, absorbed, or reflected, and reflection is the visible one.

Reflection comes in three kinds. **Diffuse** reflection is the same brightness from every angle,
because the surface scatters equally — white paper approximates it. **Direct** reflection is a
mirror image of the source, visible from exactly one angle where incidence equals reflectance —
polished metal, glass and water approximate it. **Polarised direct** reflection, or glare, looks
like direct reflection but dimmer, and shows most on black or transparent subjects.

The idea worth carrying: **material identity is a reflection mixture.** Three objects of identical
colour and identical absorption — thick grey paper, grey pewter, grey glazed tile — are instantly
distinguishable, and the only difference is the proportion of the three reflection types.

The **family of angles** is the book's central tool: every point on a surface is viewed at a
slightly different angle, and together those angles define where a source must sit to produce a
direct reflection. Put the source inside the family and a mirror-like subject lights up; put it
outside and, as far as the camera is concerned, it does not light the subject at all.

## The finding — highest content, lowest yield

This was the **densest chapter processed in this batch and produced the fewest atoms.**

```
10 candidate ideas
 6 atoms
   1 operational        (lsm_002)
   5 pending_vocabulary
 4 human_notes
```

That is not a failure of extraction. Most of the chapter is **physical mechanism** (inverse
square law, polarisation, angle of incidence) and **lighting technique** (where to put a source).
In this architecture both are Production IR, which does not exist yet. Only the parts describing
what a surface will *look like* — as opposed to how to make it look that way — can inform a
Creative IR.

The family of angles, the book's most important concept, is in `human_notes` for exactly this
reason. It is a rule about where to place a physical light.

## The repair vocabulary does not transfer — flag

Every repair this source implies is a **physical camera action**: enlarge the source, move the
light out of the family of angles, raise or lower the camera, add a polariser, use dulling spray.

None is executable against a generative model, where the only available repair is to respecify
and regenerate. So this probe proposes almost no repair terms, and the one it does
(`respecify_source_size`) is already stated in generative terms rather than the source's.

**The terms were deliberately not translated.** Converting "move the light outside the family of
angles" into a generative instruction is a `generative_media_hypothesis` and belongs to Pass 2.
Doing it here would have been exactly the drift the two-pass rule exists to prevent — and it
would have been very easy, which is the point.

This is the first source in the batch where the **failure modes transfer but the repairs do not.**

## IR-field coverage

| Field | Atoms |
|---|---:|
| `entities` | 5 |
| `creative.visual_language` | 5 |

Nothing else. But `entities` is now well covered, and specifically `entities.allowed_variation`:
`lsm_004` says whether a subject's appearance may vary with viewing angle is **a property of its
surface, not a free choice.** SPEC-01's worked example had `allowed_variation: {viewing_angle:
true}` set by hand — this says that value is materially determined and can be wrong.

## Proposed vocabulary

Failure modes (5): `glossy_surface_reads_flat`, `implausible_material_behaviour_across_angles`,
`inconsistent_lighting_evidence`, `material_reads_as_wrong_substance`, `unintended_glare`

Repairs (1): `respecify_source_size`

## Flagged for human review

**1. The source solves our registry problem, in 1990, and shows its working.**
It refuses to use the word "specular" anywhere in the book — because practitioners use it to mean
at least three different things, and because "specular light" has drifted to describe the source
rather than the reflection. Its resolution is to **refuse the ambiguous term and name the two
concepts separately.**

That is precisely the near-synonym problem the Canon registry faces, handled by a technical field
that had the same problem. Recorded in `human_notes` because it informs no IR field, but it is
arguably the most useful thing this probe found.

**2. `lsm_005` is a consistency check, not just a description.**
Hard shadows and a small highlight are *both* evidence of a small source. They must agree. A
generated image showing soft shadows with a pinpoint highlight is internally contradictory in a
way that is mechanically checkable — a rare thing among the atoms in this batch.

**3. `entities.allowed_variation` may need validation, not just declaration.**
Per `lsm_004`, a spec that declares `viewing_angle: true` for a polished metal product is
declaring something physically incoherent. Whether the IR should validate that field against
material type is a judgment call.

## Visual-context status

None unresolved. Diagrams are ray-path schematics whose geometry is stated in the prose. No atom
rests on a figure.
