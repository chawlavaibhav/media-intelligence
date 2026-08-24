# CANON-003 — Handover checkpoint

**Written:** 24 Aug 2026 · **Branch:** `work/canon` · **Reason:** task moving to parallel execution.
**State:** paused cleanly. No book is half-extracted.

---

## 1. Books completely finished — 5 of a required 15

Each has all five knowledge files, a provenance record, mechanical validation passing, and a frozen
checkpoint commit.

| # | Book | Section | Domain | Objects | Visual | Historical comparison |
|---|---|---|---|---|---|---|
| 1 | *Grammar of the Shot*, 2nd ed. | ch.4, printed pp.93–112 | filmmaking / continuity | 17 | verified page-level | **done** — audit opened after `b9f18be` |
| 2 | *Ogilvy on Advertising* | ch.2, complete | advertising | 22 | blocked (access) | **done** — audit opened after `b904278` |
| 3 | *Light: Science & Magic*, 5th ed. | ch.3, complete | photography / lighting | 20 | blocked (access) | **done** — audit opened after `d1eab97` |
| 4 | *Interaction of Color* (Albers) | ch.I–V | colour / design education | 18 | blocked (greyscale) | **n/a** — no historical comparator exists |
| 5 | *The Vignelli Canon* | Part One, complete | design values | 13 | verified page-level | **n/a** — no historical comparator exists |

Books 4 and 5 have no historical material in this repository. That was verified by search, recorded
as `no historical comparator`, and no comparator was manufactured.

**Totals across the five:** 90 SourceKnowledge objects · 13 SourceConceptSystems · 81 ontology terms ·
35 relations · 11 source-specific concepts · 27 operational bindings. All validate against SPEC-03
rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints.

## 2. Book currently partial

**None.** Book 5 was the operation in progress and has been completed rather than left open. Every
file listed below exists, validates, and is committed.

The next book that *would* have been started is **Making and Breaking the Grid** (Samara), from the
static-design quota. Nothing for it has been created — no directory, no files, no provenance work.

## 3. Files belonging to the most recently completed book

`canon/knowledge/current/vignelli-canon-intangibles/`

| File | Status |
|---|---|
| `visual-evidence-ledger.yaml` | complete, 1 demonstration, 2 visual-only observations |
| `source-knowledge.yaml` | complete, 13 objects |
| `source-concept-systems.yaml` | complete, 2 systems |
| `ontology-mappings.yaml` | complete, 17 terms, 6 relations, 2 concepts |
| `operational-bindings.yaml` | complete, 4 bindings |
| `PROVENANCE.md` | complete |

Batch-level files, all current as of this checkpoint:
`canon/findings/CANON-003-source-inventory-and-selection.md`,
`canon/findings/CANON-003-batch-issue-ledger.md`,
`canon/findings/CANON-003-book01-grammar-of-the-shot-findings.md`,
`canon/findings/CANON-003-book02-ogilvy-findings.md`,
`canon/findings/CANON-003-book03-lsm-findings.md`.

**Not yet written:** per-book findings documents for books 4 and 5. Their substantive findings are
recorded in their `PROVENANCE.md` files and in the batch issue ledger, so nothing is lost, but the
two standalone findings files that books 1–3 have do not yet exist for Albers and Vignelli.

**Not yet written:** `CANON-003-multi-source-synthesis.md` and `CANON-003-CONTROLLER-BRIEF.md`. Both
are end-of-batch deliverables requiring at least 15 books, so they are correctly absent.

## 4. Historical-comparison state

Sealed-until-checkpoint discipline held throughout. For each of books 1–3 the fresh extraction was
committed *before* any historical material was opened, and no fresh object was altered afterwards —
verified by diff in each case.

- **Book 1** — compared. 11 of 13 historical objects found, 5 fresh objects with no counterpart.
- **Book 2** — compared. 12 of 13 found, 10 fresh with no counterpart.
- **Book 3** — compared. 9 of 10 found, 10 fresh with no counterpart.
- **Books 4 and 5** — no comparator exists. Nothing pending.

**No book is awaiting a comparison.**

## 5. Batch issues discovered so far

Twenty issues logged, plus five hypotheses carried in from CANON-001/002. Full detail in
`CANON-003-batch-issue-ledger.md`. The ones that matter:

**Recurring across books — the strongest signals**

- **B-14 — the older extractions keep catching product-schema fit the fresh ones miss. Four books out
  of four possible.** In every book with a historical comparator, the old pass noticed something about
  how the knowledge meets the Creative IR that the fresh pass walked past while holding identical
  evidence. Inferred cause: the old rule *required* every atom to name a Creative IR field, which
  forced the question every time. Removing it removed the distortion and the attention together. If
  that is right this is a trade-off SPEC-03 introduced, not a defect in it, and the fix is a separate
  pass rather than a change to extraction.
- **B-07 — the historical binding layer over-binds. Five books.** Roughly one Creative IR binding per
  object every time; the fresh passes produce a fraction of that and leave most objects unbound, which
  is what SPEC-04 says should happen.
- **B-15 / B-18 — visual loss comes in five distinct patterns and severity tracks detectability, not
  amount.** Only two of the five produce confident wrong extraction. Albers's greyscale digitisation
  of a colour book is the worst, because it survives a visual pass.

**Method-integrity problems found against my own work**

- **B-17 — the isolation rule has a hole.** SPEC-04 and SPEC-05 quote several books this batch
  processes. My governance binding for the Light: Science & Magic *specular* refusal appeared to
  converge with the historical audit; it did not, because I had read that exact example in the specs
  during CANON-001. Struck from the convergence column. Bang and Williams are suspected of the same
  contamination.
- **B-11 — a worker may use fewer relation types than the schema defines.** Two relations wanted
  `broader_than` / `narrower_than`; both were downgraded to `related_to` with the intended reading in
  the note rather than assuming authority.

**Blocking and provenance**

- **B-13 — the library became unreachable mid-batch**, then was restored. Diagnosed as macOS privacy
  protection rather than the Claude Code sandbox, and fixed by the user granting access and restarting.
  Books 2 and 3 were extracted text-only during the outage and are marked `blocked_visual_validation`.
- **B-03 — Lupton is blocked** on column interleaving baked into the source file. It is a mandatory
  anchor and cannot be extracted without fabricating sentences.
- **B-20 — OCR damage has two kinds and only one blocks a book.** Albers at 0.2% garbled words was
  usable; Lupton was not. The difference is character-level versus structural, not severity.
- **B-19 — a full-page graphic buried a whole named section** in the Vignelli text layer. Caught by
  checking the contents page against the extracted sections.

**Evidence *for* the current design**

- The schema absorbed two opposite evidence profiles days apart without modification: Ogilvy at 20/22
  practitioner assertion and 0/22 controlled comparison, Light: Science & Magic at 14/20
  mechanism-given and 0/20 anecdotal. Nothing was forced or excluded in either.
- The V0 granularity rule has held across five materially different source shapes without a single
  invented exception. Ambiguous cases were recorded, not resolved by new policy.
- Williams's silent visual loss has **not** recurred in four subsequent books.

## 6. Remaining work

10 books to reach the minimum of 15; 13 to reach the target of 18. All are selected and
provenance-checked in `CANON-003-source-inventory-and-selection.md`, with reserves listed. Then the
per-book findings for books 4–5, the multi-source synthesis, and the Controller Brief.

**Nothing was started for book 6.** A parallel worker can pick up from the inventory without needing
to inspect or undo anything.

## 7. Commit

**Latest SHA: recorded in the commit that adds this file — see `git log -1` on `work/canon`.**
Book checkpoints: `b9f18be` (book 1), `b904278` (book 2), `d1eab97` (book 3), `08ed2b3` (book 4),
`22c5c8c` (book 5).
