# CANON-003 Lane A — checkpoint

**Branch:** `work/canon-003-a` · **Updated:** 24 Aug 2026 (after book 7)
**Purpose:** durable lane state. The branch is memory; the chat is disposable. A fresh session can
resume from this file alone.

## Assignment

| Book | Title | Status |
|---|---|---|
| 6 | Timothy Samara — *Making and Breaking the Grid* | **complete** |
| 7 | Michael Freeman — *The Photographer's Eye: A Graphic Guide* | **complete** |
| 8 | John Alton — *Painting With Light* | not started |

## Completed

### Book 6 — Samara, *Making and Breaking the Grid*, 2nd edn (Rockport, 2017)

- **Section:** ch.1 "Making the Grid", instructional core, printed pp.20–76.
- **Directory:** `canon/knowledge/current/samara-making-breaking-grid-ch1/`
- **Fresh pre-history checkpoint:** `c8cb9d4` — pushed **before** any historical search.
- **Historical comparison:** **no historical comparator exists.** Searched after the checkpoint;
  the only repository mentions of Samara are in CANON-003 task and planning files. Nothing pending.
- **Counts:** 79 SourceKnowledge · 6 systems · 53 terms · 14 relations · 6 concepts · 12 bindings.
- **Validation:** passes SPEC-03 r1–7, SPEC-04 r1–9, SPEC-05 layer constraints.
- **Visual:** `partial_figures_only` — EPUB, figures fully inspectable in colour, printed page does
  not exist. 6 figures opened.
- **Findings:** `canon/findings/CANON-003-book06-samara-findings.md`

### Book 7 — Freeman, *The Photographer's Eye: A Graphic Guide* (Focal Press, 2013)

- **Section:** Parts 1–3 (*Framing*, *Placing*, *Dividing*), 24 cases, converted-PDF pages 12–70.
- **Directory:** `canon/knowledge/current/freeman-photographers-eye-graphic-guide/`
- **Fresh pre-history checkpoint:** `5f95755` — pushed **before** any historical search.
- **Historical comparison:** **no historical comparator exists.** No Freeman atom file, no Freeman
  migration audit. The only mentions are the CANON-003 planning files and a forward-looking entry in
  `CANON-CURRICULUM-V0.md`, which is a reading list, not an extraction. Nothing pending.
- **Counts:** 34 SourceKnowledge · 5 systems · 46 terms · 12 relations · 5 concepts · 8 bindings.
- **Validation:** passes SPEC-03 r1–7, SPEC-04 r1–9, SPEC-05 layer constraints.
- **Visual:** `partial_reflowed_layout` — calibre conversion, so the graphic deconstructions survive
  but the designed page does not. 5 pages inspected.
- **Findings:** `canon/findings/CANON-003-book07-freeman-findings.md`
- **Two inventory corrections recorded:** the book is *A Graphic Guide* (2013), not the 2007 *The
  Photographer's Eye* the inventory named; and the PDF is a calibre conversion, so the inventory's
  classification of it as page-renderable is wrong.

## Unresolved local issues

None blocking. Fifteen issues logged in `canon/findings/CANON-003-lane-A-issues.md` (LA-01 to
LA-15), all recorded rather than fixed, per the freeze rule.

Worth a second reader's attention before synthesis:

- **LA-01 is now resolved enough to state positively.** Books 6 and 7 have nearly identical section
  sizes (57 and 59 pages) and produced 79 and 34 objects. So source shape dominates and section size
  is a real but secondary confound. Raw counts are not comparable; the differences between books are
  not artefacts.
- **LA-13 is a recurrence of a CANON-002 carry-in hypothesis** — `creative.hierarchy` cannot express
  a traversal with a return. The batch design asked for this to be watched for, so finding it is the
  experiment working. Qualified: two of the three instances are cinema devices, so it may be a
  still-image schema meeting a moving-image idea.
- **LA-12 may be structural or may be particular.** `observation_unit` is indexed on how many assets
  you observe; Freeman states a condition about the *size* something is reproduced at. One instance
  is too thin to act on.
- **LA-11 should not be merged with LA-02.** "No page" (EPUB) and "false page" (converted PDF) are
  different problems and the second is the more dangerous.

**LA-08 carries a contamination disclosure** — the production-binding observation is not independent
of SPEC-04, which I had read and which contains the *Light: Science & Magic* case as a worked
example.

**A flag for the integrator, not acted on:** `CANON-CURRICULUM-V0.md` predicted Freeman as the source
that would yield the project's first `cross_source_concept` by agreeing with Molly Bang on visual
weight. This lane is isolated and did not test it. The opportunity now exists; note that the
curriculum entry describes the *other* Freeman book, so the prediction may not survive the identity
correction.

## Method integrity

- No SPEC-01/03/04/05 change. No granularity change. No ontology relation or term kind added.
  No visual-pass method change.
- Sealed-until-checkpoint held: the fresh extraction was committed and pushed before any historical
  material was opened, and no fresh object was altered afterwards.
- Isolation held: no other lane's CANON-003 findings were read; the batch issue ledger was not used
  as a checklist and its contents were not opened.
- Source-specific IDs throughout (`sk_sam_c003_*`, `scs_sam_c003_*`, `t_sam_c003_*`,
  `bnd_sam_c003_*`), so no lane merge can collide.

## Tooling note

Mechanical validation runs from a scratchpad script (not committed — it is session tooling, not a
deliverable). It implements exactly SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer
constraints, with nothing added. A stricter check that had crept in — requiring inspected figures
for `source_support: text_and_visual`, which SPEC-03 rule 4 binds only for `visual` — was downgraded
to a warning so the instrument stays frozen.

## Next action

Begin **book 8 — John Alton, *Painting With Light*** (EPUB, 329 figures per the inventory; a 1949
practitioner text on cinematography, and the oldest source in this lane by six decades).
