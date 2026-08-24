# CANON-003 book 3 — Light: Science & Magic ch.3: extraction findings

**Date:** 24 Aug 2026 · **Checkpoint:** `d1eab97` · **Domain:** photography / lighting
**Section:** the complete chapter 3 · **Visual completeness:** `blocked_visual_validation`

---

## 1. A fourth knowledge shape, and the sharpest contrast in the batch

This chapter explains *why*. Ogilvy asserts *that*. Put side by side:

| | Ogilvy (book 2) | **Light: Science & Magic (book 3)** |
|---|---|---|
| Objects where the source states a mechanism | 12 of 22 | **14 of 20** |
| Objects resting on practitioner assertion | **20 of 22** | 3 of 20 |
| Objects that argue from stated premises | 11 of 22 | **17 of 20** |
| Anecdotal | 14 of 22 | 0 of 20 |
| Uncontrolled outcome claims | 5 of 22 | **0 of 20** |

Two books processed days apart under an unchanged method, with almost opposite evidence profiles.
**Neither required forcing, exclusion or invention.** That is direct evidence that the
evidence-characteristics vocabulary spans genuinely different kinds of craft knowledge — the design
that replaced the uncalibrated decimal confidences the historical passes used.

**Why it matters practically.** These two books would be weighted very differently by anything
reading the Canon. That difference is now recorded inside the objects rather than left to a reader's
impression of the author's authority.

## 2. What this source does that no earlier book did

**It gives a two-sided control.** Most craft rules in this batch tell you what to do. The family of
angles tells you both how to *produce* a direct reflection and how to *eliminate* it — put the light
inside the family, or place camera and light so it falls outside. Both moves are geometric and
calculable in advance.

**It ends a diagnostic ladder in a decisive physical test.** To tell polarized reflection from
ordinary direct reflection the source offers three tendencies — conductors versus insulators,
mirror-like appearance, a 40-to-50-degree viewing angle — each hedged as "likely". Then it names a
conclusive test: look through a polarizing filter. Elimination means polarized, no effect means
ordinary, partial dimming means mixed. No other source in the batch grades its own diagnostics this
way.

**It intervenes twice in its own field's vocabulary.** It refuses the word *specular* because
practitioners use it for at least three incompatible things, and it separates two senses of
*diffusion* because one describes the light and the other the surface. Both defend the same
distinction: the source determines the type of light, the surface determines the type of reflection.

## 3. Comparison with the sealed historical work

Opened only after checkpoint `d1eab97`. **Nothing altered afterwards.**

**Found by both — 9 of the historical 10**, including the family of angles, the distance-independence
of direct reflection brightness, and the refusal of *specular*.

**Found only by the fresh pass — 10 objects**, including the inverse square law, the jump-rope and
picket-fence explanation of polarization, the diffusion-confusion intervention, the three-tendency
diagnostic ladder, converting a reflection by polarizing the *source*, the open sky as a natural
polarized source, and the closing claim that the physics constrains the choice without making it.

**A divergence where the historical work used the schema better.** It made "lighting is primarily an
exercise in reflection management" the **whole-system claim** of its system object rather than a
standalone knowledge object. That is the more elegant reading: the sentence is a framing statement
about what all the other claims add up to, and SPEC-03 has a field built for exactly that. I made it
object `0001` and let the system claim restate it. Theirs fits the schema better.

### Where the historical work was better, for the fourth consecutive book

**It found a binding I did not, and it is a genuinely good one.** The audit binds
`material_class_determines_allowed_viewing_angle_variation` to SPEC-01's `entities.allowed_variation`
with `role: [constrains]` rather than `fills`.

The reasoning: whether a subject's appearance may legitimately vary with viewing angle is **a
physical property of its surface, not a free choice by whoever writes the spec**. So a Creative IR
declaring `viewing_angle: true` for polished metal is declaring something physically incoherent, and
this knowledge can be used to *validate* an existing hand-authored field.

I produced a nearby evaluation binding about when a surface's appearance is trustworthy evidence. I
never connected it to `entities.allowed_variation` and never framed it as validating an IR field.

**This is now four books out of four.** Williams, Grammar of the Shot, Ogilvy, Light: Science & Magic
— every book in this batch with a historical comparator shows the older pass catching a product-schema
fit point the fresh pass missed while holding identical evidence. See ledger B-14.

## 4. DISCLOSURE — one convergence was not independent

I extracted the *specular* refusal and bound it to `taxonomy_governance`. The historical audit
records the same binding and calls it "the batch's only governance binding", noting that SPEC-05's
near-synonym discipline was taken directly from it.

**That agreement is not evidence of anything.** I read SPEC-04 and SPEC-05 in full during CANON-001,
and both cite this exact example — SPEC-04's worked governance binding is literally this passage, and
SPEC-05's opening argument uses it as the precedent for refusing ambiguous terms. So when I reached
this chapter I already knew that this passage was considered a governance precedent and roughly what
consumer it was assigned to.

I am recording it as **contaminated convergence**, not as two passes independently agreeing. The
sealing rule in CANON-002 and CANON-003 covers a book's own historical extraction. It does not cover
the frozen schema documents, which quote several of the books this batch processes. That is a real
gap in the isolation design and is logged.

**What is not contaminated:** the other nineteen objects, all three systems, and the other four
bindings, none of which appear in the specs.

## 5. Recurrences after three books

- **Historical over-binding: 5 books.** LSM 11 Creative IR bindings for 10 objects. Fresh: 1 for 20.
- **Historical catches product-schema fit the fresh pass misses: 4 books, and 4 of 4 possible.**
- **Fresh method finds governance the historical passes missed: 3 books** — though LSM is the one book
  where the historical pass found governance too, and it found the same one I did.
- **Distinct visual-loss patterns: 5 books, 4 patterns.** LSM is *named* loss, like Grammar of the
  Shot: every figure numbered and captioned, so the reader knows precisely what they cannot see.

## 6. Uncertain / not verified

- Whether the three matched photographic pairs actually show what the source says. **Not verified** —
  the figures were unreachable. Three claims rest on the author's description of his own comparison.
- Whether the 40-to-50-degree polarization angle holds across materials. The source qualifies it as
  depending on the subject and gives no data.
- Whether any of this transfers to generated images. Outside Canon's remit and not asserted; this
  source is the Project Contract's own worked example of physical-production advice that must not be
  rewritten as generative instruction.
