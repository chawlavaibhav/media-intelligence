# CANON-003 — Lane C checkpoint

**Lane:** C — advertising / persuasion · **Branch:** `work/canon-003-c` ·
**Worktree:** `media-intelligence-canon-c`
**Status:** **all three assigned books complete.** Lane stopped as instructed.
**Method:** frozen throughout. No schema, granularity rule, visual-pass method or ontology
vocabulary was changed. Shared CANON-003 ledger, synthesis, Controller Brief and `canon/HANDOFF.md`
were not touched.

---

## Status

| Book | Title | Section processed | State | Fresh checkpoint | Historical comparison |
|---|---|---|---|---|---|
| 13 | Claude C. Hopkins, *Scientific Advertising* | ch.1–7, printed pp.1–24 of 21 chapters | **complete** | `1222919` | **none exists** |
| 14 | Chip Heath & Dan Heath, *Made to Stick* | the complete Introduction, "What Sticks?" | **complete** | `a699a49` | **none exists**; one prior *prediction* was compared instead — see C-21 |
| 15 | Rory Sutherland, *Alchemy* | the complete Introduction, "Cracking the (Human) Code" | **complete** | `f992d69` | **none exists** |

**Books blocked:** none. **Partially extracted books:** none. Every book is finished, validated,
committed and pushed, and each fresh checkpoint was pushed **before** any historical material was
searched for.

## Commits on `work/canon-003-c`

| What | SHA |
|---|---|
| Book 13 fresh pre-history checkpoint | `1222919` |
| Book 13 historical search, lane issues, lane checkpoint | `df1a490` |
| Book 14 fresh pre-history checkpoint | `a699a49` |
| Book 14 historical search, lane issues, lane checkpoint | `31e3249` |
| Book 15 fresh pre-history checkpoint | `f992d69` |
| Book 15 historical search, lane issues, this final checkpoint | see `git log -1` |

## What the lane produced

Three directories under `canon/knowledge/current/`:
`hopkins-scientific-advertising-ch1-7`, `heath-made-to-stick-introduction`,
`sutherland-alchemy-introduction` — each with the five knowledge files and a `PROVENANCE.md`.

| | Objects | Systems | Terms | Relationships | Concepts | Bindings |
|---|---|---|---|---|---|---|
| Book 13 — Hopkins | 54 | 5 | 37 | 10 | 4 | 8 |
| Book 14 — Heath & Heath | 28 | 3 | 22 | 9 | 3 | 9 |
| Book 15 — Sutherland | 32 | 3 | 22 | 10 | 3 | 7 |
| **Total** | **114** | **11** | **81** | **29** | **10** | **24** |

**Mechanical validation:** all three pass SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer
constraints. The same validator was run against all five pre-parallel books and passes on each, so
this lane is being held to the same rules those were.

**Visual passes:** performed on all three, before any claim was written in each case.

- Book 13 — `verified_page_level`. 24 pages rendered and inspected; **zero** figures. Text
  extraction loses nothing. Load-bearing digits re-read from the page image against the text layer.
- Book 14 — `not_verified_page_layout`. Every image in the book enumerated and each distinct one
  opened; no figures anywhere. The section's own title exists only as an image of the word.
- Book 15 — `not_verified_page_layout`. Two figures, one of which carries the book's thesis and
  whose ~two dozen quadrant placements exist **only** in the image; transcribed in full in the ledger.

## Unresolved local issues

None blocking. Thirty issues are recorded in `canon/findings/CANON-003-lane-C-issues.md`, including
ten pieces of evidence *for* the frozen design. **Every proposed fix is a proposal. Nothing was
applied.**

### The finding this lane would put in front of the Controller first

**One SPEC-03 field broke in all three books, in three different ways.**
`empirical_within_source` is defined as "the source reports its **own** measurement", and the fixed
characteristic list has no neighbouring value for anything else.

- **Hopkins** claims measurement constantly — "we prove them by repeated tests", "never failed to
  prove out in any test we know" — and across seven chapters supplies three unattributed
  cost-per-reply figures, one before-and-after picture test, and a described record of ~2,000 keyed
  headlines from which no result is given.
- **Heath & Heath** report measurement constantly and almost none of it is theirs: Newton's 1990
  Stanford study, Best and Horiuchi's Halloween research, a 1999 Israeli advertising experiment.
- **Sutherland** does both inside one book — his own randomised envelope test alongside cited work
  from Duke, Trivers and Kurzban — so a single extraction contains the distinction the vocabulary
  cannot express.

All three were handled by writing the truth into `extractor_observed` caveats. That is faithful and
completely unaggregatable: nothing can later count how many sources claim an empirical basis, how
many supply one, and how many are relying on someone else's.

Whether this is general or an artefact of the advertising and persuasion domain is exactly what the
other three lanes settle. Lane C asserts the pattern within its own domain and asserts nothing
beyond it.

### Also worth the Controller's attention

- **C-15 — two governing documents disagree, and the conservative reading cost fidelity.** SPEC-05's
  governance section singles out only `same_failure_family` as needing review, which would permit
  `same_mechanism` and `broader_than`. The Canon charter lists exactly two relations a worker may set
  locally. The narrower reading was followed in all three books, so relations the sources state
  outright — one of them an identity Sutherland and the Heaths each assert directly — are recorded in
  the structured layer as unspecified connections. **The cheapest fix needs no schema change at all:
  a decision about which document governs.**
- **C-16 and C-26 are the counterweight**, and are the strongest positive evidence in this lane. Made
  to Stick's entire contribution lives above its individual claims — six commonsense rules at object
  level, one checklist explicitly not a formula aimed at one named obstacle at system level — and the
  system layer held all of it. Alchemy, an avowedly anti-rational provocation, went in with nothing
  excluded and nothing dressed up.
- **C-29 — every book in this lane contradicts itself inside the processed section**, eight instances
  across three books, all expressible with existing vocabulary. Evidence for the design, and a
  source-shape finding: a consumer retrieving two objects from the same commercial source cannot
  assume they are consistent.
- **All three Lane C books have no historical comparator.** The pre-parallel books 1–3 each had one
  and the comparison produced the batch's strongest signal to date. **Lane C contributes no evidence
  on that question at all, in either direction.** The integrator should not read Lane C's silence as
  agreement or disagreement.

## Open questions this lane cannot settle

- Whether the evidence-characteristic gap (C-01 / C-13 / C-23) is general or specific to sources that
  argue about persuasion. Three books, one domain.
- Whether the relation-type under-use (C-05a / C-15) is a genuine recurrence of a pre-parallel item
  or a separate observation of the same shape. This lane has not read the earlier books' working
  files and does not assert a count.
- Whether C-19 (a heading that exists only as an image) is a recurrence of the pre-parallel finding
  about a graphic disturbing a named section, or a separate pattern.
- Whether *Scientific Advertising* chapter 15, "Test Campaigns", supplies the measurement detail
  chapters 1–7 do not. Outside the processed section. **NOT VERIFIED.**
- Rights status of the local library files, carried forward unresolved from the batch inventory.

## Handover

Lane C is finished and does not merge itself, does not perform synthesis, and did not read any other
lane's fresh findings. The three book directories, the issue file and this checkpoint are the lane's
complete output and are pushed to `origin/work/canon-003-c`.

The integrator will need to combine this file's issue list with the other lanes and the preserved
pre-parallel batch ledger, count recurrence by **distinct books rather than by mentions**, and decide
the two questions this lane deliberately left open: whether C-05a/C-15 and C-19 are recurrences of
pre-parallel items or separate observations.
