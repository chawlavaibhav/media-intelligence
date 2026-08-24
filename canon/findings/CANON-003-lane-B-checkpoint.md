# CANON-003 Lane B — checkpoint

**Branch:** `work/canon-003-b` · **Lane:** film / editing / unusual source form
**Updated:** 24 Aug 2026, after book 9.

## Completed books

| # | Book | Section | Objects | Systems | Terms | Bindings | Visual | Validated | Historical |
|---|---|---|---|---|---|---|---|---|---|
| 9 | *Grammar of the Edit*, 2nd ed. | ch.3–5, printed pp.55–109 | 60 | 5 | 48 | 11 | verified page-level | pass | **done** — `no historical comparator`; companion-volume comparison run |
| 10 | Murch, *In the Blink of an Eye* | printed pp.1–25 | 39 | 4 | 23 | 8 | verified page-level (0 figures) | pass | **done** — `no historical comparator` |

## Remaining assignments

| # | Book | Status |
|---|---|---|
| 11 | Christopher Kenworthy — *Master Shots* | **reassigned out of Lane B** — moved to `work/canon-003-rebalance-d` by Controller update, 24 Aug 2026. Not started here; no artifact of any kind was created for it in this branch. |
| 12 | Michael Ondaatje — *The Conversations* | in progress |

**Lane B's assignment is now three books, not four.** Book 11 was reassigned to
`work/canon-003-rebalance-d` by Controller update on 24 Aug 2026. Nothing had been created for it on
this branch — no directory, no files, no provenance work — so there is nothing for the receiving lane
to reconcile or undo. Lane B did open the Master Shots EPUB to read its front matter before the
reassignment arrived; no claim was extracted and no file was written.

Nothing has been created for book 12 yet. A fresh session can pick up from this checkpoint without
inspecting or undoing anything.

## Latest SHA

Recorded in the commit that adds this file — see `git log -1` on `work/canon-003-b`.

Book checkpoints: **`ddef98d`** (book 9) · **`72a6b31`** (book 10). Each is the fresh pre-history
checkpoint for its book; post-checkpoint comparison and findings follow in the next commit each time.

## Unresolved local issues

- **Book 9 is closed.** Fresh checkpoint `ddef98d` pushed, then the repository searched: no
  historical *Grammar of the Edit* material exists, recorded as `no historical comparator`. The
  companion-volume comparison against book 1 was run afterwards and produced LB-09.
- **LB-09 is open and rests on one pair.** Two books by the same authors are not two independent
  origins, and SPEC-05's `cross_source_concept` guard counts source ids. No cross-source promotion
  has been attempted yet, so the failure is predicted rather than observed.
- **Book 10 is closed.** Fresh checkpoint `72a6b31` pushed, then searched: no historical Murch
  material exists, recorded as `no historical comparator` — the fourth such book in the batch.
- **LB-01 is open and single-source.** SPEC-03's intra-source relation vocabulary could not express
  thirteen connections in book 9. Murch did not stress the same area, so it has not recurred.
- **LB-10 is open and single-source, and it is the one the operator asked about.** SPEC-03's
  `priority_order` carries Murch's rank order faithfully and cannot carry his weights. Not fixed;
  recorded with the numbers preserved verbatim on the member objects.
- **LB-14 is a live hazard for book 12.** A transcribed lecture deferred its central question 33
  pages. *The Conversations* is an interview transcript and is likely to be less locally complete
  still.
- **A cross-source concept candidate is flagged for the integrator**, not created: Murch's
  `eye_trace` and *Grammar of the Edit*'s `eye trace` are genuinely independent origins.
- **Book 11 is out of scope for this lane** as of the Controller update. Lane B's usable-book
  contribution to the batch is therefore three, not four.
- No blocked books. No stop condition fired.

## Isolation state

No other lane's new CANON-003 findings have been read. The shared batch issue ledger has not been
opened. No shared file has been edited — the batch ledger, the synthesis, the Controller Brief and
`canon/HANDOFF.md` are untouched by this lane.

For book 9 specifically: no Canon knowledge file for *Grammar of the Shot* was opened during
extraction, despite the two books sharing authors, publisher, series and subject.

## Method state

Frozen instrument held. No schema, granularity rule, visual-pass method or ontology vocabulary was
changed. One drafting error — thirteen relations written with a relation type SPEC-03 does not define
— was caught by mechanical validation and resolved by remapping five and deleting eight, without
inventing a relation type. Recorded in the lane issue file rather than quietly fixed.
