# Finding 05 — Ellen Lupton, "Hierarchy" (Pass 1)

**Date:** 23 Aug 2026 · **Source:** Thinking with Type, 2nd ed., TEXT part, pp.131–133
**Mode:** source-only Pass 1, isolated.

## Extraction-quality warning — read before trusting these atoms

The source is set in **two columns**, and the EPUB extraction **interleaves them sentence by
sentence**. Raw output looks like this:

> "A typographic hierarchy expresses the organization Emphasizing a word or phrase within a body
> of of content, emphasizing some elements and text usually requires only one signal."

Two unrelated sentences woven together. Every atom below required de-interleaving, which is an
**inference step, not a reading step** — the extractor decided which clause belonged to which
column. Confidence is capped at 0.8 throughout and no atom should be promoted before someone
checks it against the printed page.

This is a finding about method, not just this book: **EPUB sources with multi-column print layouts
are not safely machine-readable by text extraction alone.** Two more EPUBs are queued in this
batch. The same check applies to them.

## Human learning notes

Lupton's hierarchy is **relational** — a level exists only relative to other levels, never in
isolation. Its purpose is scanning: letting a reader enter, exit, and pick among the content
rather than reading it through.

The operational core is a cue economy. Cues divide into **spatial** (indent, line spacing,
placement) and **graphic** (size, style, colour). Each level is marked by one or more cues,
applied consistently. Inline emphasis needs only one signal — italic being the default. Structural
breaks may carry deliberate redundancy, a paragraph traditionally taking both a line break and an
indent so each backs the other up. The ceiling is three cues per level; past that the source
labels the result "too many signals."

The best idea in the section is demonstrated rather than argued: one identical logical hierarchy
rendered four different ways, all correct. **The ranking belongs to the content; the cue set is a
separate choice.**

## Counts

```
11 candidate ideas
 9 atoms
   3 operational       (lu_004, lu_006, lu_008 — propose no new vocabulary)
   6 pending_vocabulary
 2 human_notes
```

First atoms in this batch to reach `operational`. They did so purely because they propose no new
failure or repair terms — not because they are better knowledge.

## IR-field coverage

| Field | Atoms |
|---|---:|
| `static.typography_layout` | 7 |
| `creative.hierarchy` | 5 |
| `copy.body` | 1 |

**Untouched:** `intent`, `audience`, `message`, `entities`, `relationships`, `brand`, `delivery`,
`acceptance`, `creative.concept`, `creative.hook`, `creative.visual_language`, `static.composition`,
and the entire video extension.

## Proposed vocabulary

Failure modes (6): `hierarchy_contradicts_content_structure`, `inconsistent_level_cueing`,
`mismatched_x_heights`, `no_scan_entry_point`, `signal_overload`

Repairs (5): `align_x_heights`, `normalise_level_cues`, `reduce_cue_count`,
`reduce_to_single_signal`, `restate_level_cues`, `strengthen_level_contrast`

## Flagged for human review

**1. The source contains its own apparent contradiction, and the schema absorbed it.**
`lu_005` says inline emphasis needs only one signal. `lu_006` says redundancy is acceptable and
even recommended. Both are Lupton's. They reconcile by scope — inline emphasis versus structural
break — and are bounded by the three-cue ceiling in `lu_007`. This was carried in the `exceptions`
field rather than by dropping either atom. It is the first case where SPEC-02's exceptions
mechanism did real work, and worth checking whether a human agrees with how it was resolved.

**2. `lu_008` is architectural evidence, not just a principle.**
"One hierarchy, many valid encodings" says the ranking is a property of the content while the cue
set is a design choice. That is the Creative IR / Production IR boundary, stated by a typographer
in 2010 about print. Recorded as an atom; noted because it independently supports a split we made
on other grounds.

**3. `lu_004` is a taxonomy, not a rule.**
It lists what cues exist rather than prescribing anything, and has `role: [fills]` only, with no
diagnostic teeth. It passes validation. Whether a pure taxonomy should be an atom or reference
data is a granularity question for review.

## Visual-context status

One unresolved: `lu_008` is marked `visual_context_required: true`. Its evidence is a four-column
table whose entire point is the typographic difference between columns, and that difference does
not survive text extraction. The atom rests on the caption and surrounding prose. Resolvable only
by rendering the printed page.
