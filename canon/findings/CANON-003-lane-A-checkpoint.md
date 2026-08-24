# CANON-003 Lane A — checkpoint

**Branch:** `work/canon-003-a` · **Updated:** 24 Aug 2026
**Purpose:** durable lane state. The branch is memory; the chat is disposable. A fresh session can
resume from this file alone.

## Assignment

| Book | Title | Status |
|---|---|---|
| 6 | Timothy Samara — *Making and Breaking the Grid* | **complete** |
| 7 | Michael Freeman — *The Photographer's Eye* | not started |
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

## Unresolved local issues

None blocking. Ten issues logged in `canon/findings/CANON-003-lane-A-issues.md` (LA-01 to LA-10),
all recorded rather than fixed, per the freeze rule.

One is worth a second reader's attention before synthesis: **LA-01**, that per-book object counts
are not comparable across books because section sizes differ by roughly 3×. Book 6 alone produced
more objects than the batch's first five books combined, and most of that gap is section length
rather than source density.

**LA-08 carries a contamination disclosure** — the production-binding observation is not independent
of SPEC-04, which I had read and which contains the *Light: Science & Magic* case as a worked
example.

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

Begin **book 7 — Michael Freeman, *The Photographer's Eye*** (PDF, printed pages available, so a
page-level visual pass should be possible for the first time in this lane).
