# CANON-003 Lane B — checkpoint (FINAL)

**Branch:** `work/canon-003-b` · **Lane:** film / editing / unusual source form
**Updated:** 24 Aug 2026, after book 12. **Lane B's assigned work is complete.**

## Completed books — 3 of 3 assigned

| # | Book | Section | Objects | Systems | Terms | Bindings | Visual | Validated | Historical |
|---|---|---|---|---|---|---|---|---|---|
| 9 | *Grammar of the Edit*, 2nd ed. | ch.3–5, printed pp.55–109 | 60 | 5 | 48 | 11 | verified page-level | pass | **done** — `no historical comparator`; companion-volume comparison run |
| 10 | Murch, *In the Blink of an Eye* | printed pp.1–25 | 39 | 4 | 23 | 8 | verified page-level (0 figures) | pass | **done** — `no historical comparator` |
| 12 | Ondaatje, *The Conversations* | Third Conversation, complete | 27 | 3 | 16 | 6 | not_verified_page_level (EPUB) | pass | **done** — `no historical comparator` |

**Lane totals:** 126 SourceKnowledge objects · 12 SourceConceptSystems · 87 ontology terms ·
32 relationships · 12 concepts · 25 operational bindings. Every file validates against SPEC-03
rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints.

**No book was blocked.** No CANON-003 stop condition fired.

## Reassignment

| # | Book | Status |
|---|---|---|
| 11 | Christopher Kenworthy — *Master Shots* | **reassigned out of Lane B** to `work/canon-003-rebalance-d` by Controller update, 24 Aug 2026. Nothing was created for it on this branch — no directory, no files, no provenance work — so there is nothing for the receiving lane to reconcile or undo. Lane B opened the EPUB front matter only; no claim extracted, no file written. |

## Book checkpoints

| Book | Fresh pre-history checkpoint | Comparison + findings |
|---|---|---|
| 9 | `ddef98d` | `26788fc` |
| 10 | `72a6b31` | `7a0f140` |
| 12 | `9e6f716` | `7760953` |

Sealed-until-checkpoint discipline held for all three. In each case the fresh extraction was
committed **and pushed** before any historical or comparison material was opened, and no fresh object
was altered afterwards.

## Issues recorded — LB-01 to LB-20

In `canon/findings/CANON-003-lane-B-issues.md`. The ones that matter most:

**Schema insufficiencies, each recorded and none fixed**
- **LB-01** — SPEC-03's intra-source relation vocabulary cannot express *sibling*, *alternative* or
  *orthogonal classification*. Thirteen connections in book 9 were dropped rather than forced. Did
  not recur in books 10 or 12.
- **LB-10** — `priority_order` carries Murch's rank and **not his weights**. 51/23/10/7/5/4 says
  emotion outweighs the other five combined; `order: 1..6` says six things in sequence. **This is the
  case the operator asked to be tested.** Represented with the existing type, insufficiency recorded,
  numbers preserved verbatim on the member objects.
- **LB-15** — no field for **who said it**. A four-voice interview stores an interviewer's proposal
  identically to a practitioner's assertion, including one case where the speaker *declines* the
  framing and the correction is the claim.
- **LB-11** — a remedy acting on a *person* (send the director to the Alps for two weeks) has no
  `executable_by` value; `unknown` is honest and flattens a real distinction.

**Visual loss — four distinct mechanisms in three books**
- **LB-03** — text baked into artwork lost **silently**, with no cheap index to detect it (book 9).
- **LB-16** — caption and image both survive; the **binding between them** does not (book 12). Unlike
  LB-03, this one has a cheap detector.
- **LB-17** — a figure can survive extraction and still be **too small to carry its evidence**.
- **LB-13 / LB-05** — visual dependence follows the author's mode of argument, not the domain: 23
  figures and total loss in book 9, **zero figures** in book 10, same subject. And one figure in book
  9 is fully text-recoverable *for a statable reason*.

**Independence — the lane's strongest cross-cutting result**
- **LB-09** — same authors, publisher and series would pass a naive check and should not.
- **LB-20** — same speaking voice with a **different author field** would pass any metadata check at
  all. Contamination disclosed: the second extraction was done by someone who had read the first.
- Against one genuinely independent pair that correctly passes. Two false positives, one true
  positive, three books, one lane.

**Source shape**
- **LB-18 / LB-19** — textbook, lecture and interview produce different object densities, different
  term counts, different system counts, and different binding profiles. Book 9 states *properties* →
  evaluation. Book 10 states *priorities* → governance. Book 12 states *testimony* → mostly nothing,
  correctly.
- **LB-12** — spread interleaving in a scanned PDF was **removable** by respecting page geometry.
  Scoped strictly to book 10; this lane did **not** examine Lupton and makes no claim about it.
- **LB-14** — a transcribed lecture deferred its central question 33 pages past any reasonable window.

## What this lane did NOT do

- No shared file was edited. `CANON-003-batch-issue-ledger.md`, `CANON-003-multi-source-synthesis.md`,
  `CANON-003-CONTROLLER-BRIEF.md` and `canon/HANDOFF.md` are untouched.
- No other lane's new CANON-003 findings were read. The existing batch issue ledger was never opened
  or used as a checklist.
- **No cross-source concept was created**, though three candidate pairs were identified. Cross-source
  aggregation is the integrator's work.
- No final synthesis. No method or schema change. No new relation type, term kind or ontology value.
- For book 9 specifically: no *Grammar of the Shot* knowledge file was opened during extraction,
  despite shared authors, publisher, series and subject.

## Open items for the integrator

1. **Three independence cases** need a decision before any `cross_source_concept` is promoted —
   two that must not count as independent origins, one that may.
2. **LB-10 and LB-15 both want a field the schema does not have** (a member weight; a speaker). Each
   rests on one book. Neither should drive a change alone.
3. **Five of the batch's books now have no historical comparator, including all three of Lane B's.**
   The batch's strongest recurring signal is untestable on this lane, and the miss rate for books 9,
   10 and 12 is unknown rather than zero.
4. **Lane B contributes three usable books, not four**, following the book 11 reassignment.

## Method state

The frozen instrument held across four materially different source shapes. One drafting error — in
book 9, thirteen relations written with a relation type SPEC-03 does not define — was caught by
mechanical validation before the checkpoint and resolved by remapping five and deleting eight,
without inventing a relation type. Recorded in the lane issue file rather than quietly fixed.
