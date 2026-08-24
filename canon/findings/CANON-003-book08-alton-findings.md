# CANON-003 book 8 — Painting With Light ch.2: extraction findings

**Date:** 24 Aug 2026 · **Lane:** rebalance (Books 8 and 11) · **Checkpoint:** `ab2a833`
**Domain:** cinematography / lighting · **Section:** chapter 2 "Motion Picture Illumination",
complete · **Visual completeness:** `verified_figure_level`
**Counts:** 27 SourceKnowledge objects · 3 SourceConceptSystems · 22 terms · 9 relations ·
3 concepts · 6 operational bindings, of which 2 are Creative IR

---

## 1. The finding: the EPUB turned this book's headings into pictures, and the structure survived
## upside down

Every chapter- and section-level heading in this file is an SVG containing glyph outline paths — a
*drawing* of the words, with an empty alt attribute. Rasterising all twenty of them in the chapter
2–3 range is the only reason this extraction can name the chapter's six sections: The Set, Props,
People, Rigging for Illumination, Lighting Equipment, The Theory of Illumination.

What makes this worse than a plain loss is what *did* survive. The chapter's **deeper** headings —
ARC LIGHTS, DESIGNATIONS OF DIFFERENT TYPES OF LIGHTS, THE PURPOSE OF ILLUMINATION, ORIENTATION,
MOOD, DEPTH, KEY OF THE PICTURE, ROUGHING IN, REHEARSAL, DAWN, SUNRISE, SUNSET — are ordinary
all-caps text and extract cleanly. There are 39 of them.

**So a text-only pass sees the leaves and not the branches.** It does not read as damaged; it reads
as a flat chapter with 39 topics, when it is actually a six-part chapter whose sixth part contains
most of those topics. That is a different failure from the ones this batch has met so far, which
were either corruption you can see or absence you can suspect. This is a hierarchy that survives
inverted, and it is silent.

**How it was caught:** by the visual pass listing image references and finding that thirteen
all-caps subheadings sat under no heading at all. The navigation file would have recovered the
chapter title, but not one of the six section titles.

## 2. The pre-batch open question this book answers

The batch ledger, written before the parallel split, left an explicit open question about
EPUB-sourced books — I opened it only after this book's checkpoint was pushed:

> "Whether figure-only visual evidence is sufficient for *non*-layout books — a lighting diagram
> may survive perfectly well without its page — is **not yet established**. Watch across the batch."

**Answer, from this book: yes for the diagrams, and the question was aimed at the wrong risk.**

The figures survive perfectly. Fig. 90 is a complete overhead lighting plan with instrument types,
positions, beam paths and a legend, and it is fully legible without any notion of a page. The
sphere pair and the Wrong/Right pair work exactly as printed. For a book that argues through
diagrams rather than through page layout, figure-only evidence is sufficient.

The loss that actually occurred in this EPUB was **structural, not spatial** — the headings. That is
not what "EPUB + layout-argued book" predicted, and it would not have been caught by a rule about
layout-argued books, because this is not one.

## 3. What this source is: three kinds of content that age at three different rates

The chapter interleaves, within a few pages:

| Kind | Examples | Shelf life |
|---|---|---|
| **Geometry and perception** | one source renders a solid flat; matching tones lose their edge; an angle reveals form; a filler near the lens adds level without a second shadow | does not date |
| **Technology** | the instrument catalogue with amperages and beam angles; shiny props are wanted *because of antihalo film*; every negative must be normally exposed | dated completely |
| **Studio convention stated as technical fact** | high reflectors "exaggerate cheekbones, make deep-set eyes, none of which are favorable to feminine faces" | a period convention about how women were to be photographed |

**All three carry `practitioner_assertion` and are indistinguishable by claim type.** The separation
here was made by reading, and `historical_claim` (9 objects) and `culturally_bounded` (1) were
applied by hand. Nothing in the schema would have forced the question, and nothing mechanical would
catch an extractor who did not ask it.

The third row is recorded as the source states it, with a caveat naming it as a convention of the
period rather than repeated as a general rule. That is the honest handling: the claim is part of
what this book teaches and part of why it needs reading with care.

## 4. Where the schema fitted this source unusually well

**Two genuine controlled comparisons.** `controlled_comparison` has been a rare characteristic in
this batch. Alton uses it twice in one chapter: the same sphere under one light and under four, and
tone-matched versus tone-opposed blocks labelled Wrong and Right. One variable changed, everything
else held. These are the strongest single pieces of visual evidence assigned to this lane.

**A term collision the source guards itself.** Alton writes "the key of the picture (not to be
confused with keylight)" — one is an instrument's role in a setup, the other the lighting approach
of a whole film. The ontology layer records them as two terms with `distinct_from` and
`confidence_basis: source_stated`. A source that polices its own vocabulary is the easiest possible
case for this layer, and worth recording as the positive control against the harder cases.

**Two contradictions the source does not notice, and the schema held both.** The chapter requires
the key light to appear to come from an established source, then exempts musical comedy entirely —
"light sources and logic in lighting mean nothing". And it gives two depth rules in one section: a
symmetrical one (separate foreground from background in tone, either direction) and a directional
one (the most distant spot should be the lightest). A dark distant background satisfies the first
and violates the second. Both are recorded as `conflicts` on the concept system with
`origin: extractor_inferred`, because noticing them is ours.

## 5. One demonstration is under-determined even after inspecting it

Figures 83 and 84 are offered for the claim that "both are flat surfaces, yet one gives a sensation
of depth and the other does not". The text never says which. Neither figure carries a verdict label,
unlike the Wrong/Right pair three pages earlier. Both read as a tunnel.

Recorded as `extraction_uncertainty: ambiguous_referent` rather than resolved by inference. Worth
recording as a class: a visually-argued claim can be under-determined **with** the figures in hand,
not only without them. Inspecting the picture is not automatically the same as recovering the claim.

## 6. Evidence profile

| Characteristic | Objects (of 27) |
|---|---|
| `explicitly_stated` | 27 |
| `practitioner_assertion` | 27 |
| `mechanism_absent` | 14 |
| `mechanism_given` | 13 |
| `visually_demonstrated` | **12** |
| `argued` | 10 |
| `historical_claim` | **9** |
| `controlled_comparison` | **2** |
| `repeated_within_source` | 1 |
| `culturally_bounded` | 1 |
| `outcome_claimed` · `anecdotal` · `empirical_within_source` | 0 |

Source uncertainty is `none` on all 27 — Alton never hedges. Extraction uncertainty is `none` on 23,
`ocr_degraded` on 2 (objects resting on damaged equipment names) and `ambiguous_referent` on 2.

**Plain-English reading.** A practitioner stating things flatly, with about half his claims explained
and nearly half shown. The 12 visual demonstrations and 2 controlled comparisons make this the most
*shown* source in the lane; the 9 historical claims make it the most time-bound. Neither fact is
visible from the claim types, which is the point of section 3.

## 7. Historical comparison

**No historical extraction comparator exists.** Searched after checkpoint `ab2a833` was committed
and pushed, on author surname and title.

Two pre-batch **planning** judgements exist, in `CANON-COVERAGE-MAP-V0.md` dated 23 August 2026,
which assign this book to "Lighting" (strong coverage) and "Camera placement & movement" (strong).
Both are borne out: the chapter's largest object clusters are the light-function vocabulary and the
lighting recipes, and its stated criterion for camera position — the angle that reveals the most
surfaces — is one of only two Creative IR bindings this book produced. The same document also lists
it under "Colour grading — weak, partial via Painting With Light", which this chapter does not
support at all: it is a monochrome chapter whose only colour discussion is what colour to *paint a
set* so that faces separate in black and white.

**Contamination check:** the `canon/experiments/` documents and the batch issue ledger were not
opened before or during this extraction. Both were read only after the checkpoint was pushed. The
agreement on lighting and camera placement is therefore genuine, and so is the disagreement on
colour grading.
