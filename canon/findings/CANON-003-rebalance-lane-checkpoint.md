# CANON-003 — Rebalance-lane checkpoint

**Branch:** `work/canon-003-rebalance-d` · cut fresh from the common parallel base `4cbe257`
**Amendment:** `canon/tasks/CANON-003-REBALANCE-01.md`, Controller-approved 24 Aug 2026
**Updated:** 24 Aug 2026, after book 11. **Both assigned books are complete. Lane stops here.**

**Communication check:** I will explain technical ideas in plain English, including what they mean,
why they matter, and their practical consequence; use minimum sufficient wording without sacrificing
understandability; separate evidence from inference; and never invent facts. I have read
`shared/COMMUNICATION-STANDARD.md`.

## Execution amendment, recorded here as the amendment requires

Books 8 and 11 were reassigned to this worker because Lane D finished its three books while other
lanes still had six outstanding. Both were fixed in `CANON-003-PARALLEL-EXECUTION.md` before any
parallel-lane result existed, and both were marked not started at the Controller audit, so no source
was chosen in the light of emerging findings.

The amendment notes that perfect cognitive erasure cannot be guaranteed when the same external agent
identity is reused, and that the safeguard is procedural and auditable. What was actually done:

- work is on a **fresh branch from the common base**, not a continuation of `work/canon-003-d`;
- the Lane D worktree is a separate directory, and its issue file and checkpoint were **not opened**
  during either extraction;
- no Lane A/B/C fresh findings, issue files or checkpoints were read at any point;
- each book's fresh extraction was committed **and pushed** before any historical, planning or
  cross-book material was opened;
- every finding below is written with its derivation from the source text, so a reviewer can check
  the reasoning rather than trust the isolation.

## Books — both complete

| # | Book | Section | Status | Fresh checkpoint | Historical |
|---|---|---|---|---|---|
| 8 | John Alton, *Painting With Light* (1949; UC Press ed.) | ch.2 "Motion Picture Illumination", complete | **complete, validated, pushed** | `ab2a833` | no extraction comparator; coverage-map confirmed on lighting and camera placement, contradicted on colour grading |
| 11 | Christopher Kenworthy, *Master Shots* vol.1, 2nd ed. | Introduction, How to Use this Book, About the Images, Conclusion + ch.8 "Directing Attention" complete | **complete, validated, pushed** | `2d3da5d` | no extraction comparator; coverage-map confirmed on shot grammar and camera movement, contradicted on composition; the ledger's EPUB concern refined |

Neither book was blocked. Both had usable text and usable figures.

## Totals

| | Book 8 | Book 11 | Lane |
|---|---|---|---|
| SourceKnowledge objects | 27 | 20 | **47** |
| SourceConceptSystems | 3 | 3 | **6** |
| Ontology terms | 22 | 17 | **39** |
| Relations | 9 | 8 | **17** |
| Concepts | 3 | 3 | **6** |
| Operational bindings | 6 | 6 | **12** |
| *of which Creative IR* | 2 | 2 | **4** |

Both directories pass mechanical validation against SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the
SPEC-05 layer constraints. The validator is an ephemeral scratchpad script, not committed,
consistent with earlier books in this batch.

## What this lane found, in plain English

**Two books about moving-image production, and the visual evidence failed in two completely
different ways — neither of them the way the batch expected.**

In *Painting With Light*, the EPUB turned every chapter and section heading into a vector drawing of
letters. The chapter's *deeper* headings are ordinary text and survive, so a text-only extraction
produces a chapter that looks flat and coherent — 39 topics in a row — instead of a six-part chapter,
with nothing to suggest anything is missing. **The hierarchy survives upside down.** Rasterising the
headings recovered all six section names. The figures, meanwhile, were perfect: a full overhead
lighting plan is entirely usable without a page around it.

In *Master Shots*, the file was fine and the book was the problem. A technique called "Color Guides"
argues that a strongly coloured jacket keeps a character identifiable at distance — and every one of
the book's 124 images is greyscale, so its illustration shows the background figure as an
unidentifiable smudge. Nothing is damaged; the loss exists only in the relation between what a
section claims and what its picture can show, and no check on the file, the text or the image would
find it.

**The same book contains the counter-example**, which is what makes the pair worth keeping together:
its diagram notation distinguishes camera movement from actor movement by *white against black*, a
tonal code that survives monochrome printing, low resolution and colour blindness perfectly. One
author, two decisions, opposite outcomes. So the lesson is not "EPUBs lose visual evidence" — it is
**ask what a source's argument depends on, not what its file format is.**

**Third finding, from Alton:** the same chapter states physical geometry that does not date, film
technology that has dated completely, and one studio convention of the period given as technical
fact. All three carry `practitioner_assertion` and nothing in the schema distinguishes them; the
separation was made by reading.

## Unresolved local issues

Nine entries in `canon/findings/CANON-003-rebalance-lane-issues.md`.

**Schema or method could not represent it cleanly — recorded as evidence, nothing applied:**
- **R-01** — an EPUB rendered a book's headings as images; the surviving hierarchy is inverted and
  looks intact.
- **R-03** — three kinds of content with three different shelf lives, indistinguishable by claim
  type.
- **R-06** — a source that pre-declares its claims as proposals for testing cannot be marked as
  such.
- **R-07** — a claim whose own illustration cannot discriminate it from its negation, undetectably.
- **R-02** — a visually demonstrated claim still under-determined after the figures were inspected.

**Counter-evidence and evidence for the current design:**
- **R-04** — figure-only visual evidence was sufficient for a diagram-argued book, which bounds an
  open question the batch recorded before the split.
- **R-05** — a source that polices its own vocabulary is the easy case for the ontology layer.
- **R-08** — a notation designed for its reproduction survives everything, which relocates the
  visual-loss problem from format to fit.
- **R-09** — two practitioner books in the same domain landed at opposite ends of several evidence
  fields with no adjustment to the method.

Nothing was applied. The method stayed frozen throughout.

## Method discipline

- Both fresh checkpoints were committed **and pushed** before any search for historical material.
- No historical extraction exists for either book. Pre-batch **planning** documents were found after
  the pushes; four judgements were confirmed, two contradicted, and one refined. All are recorded,
  and the contradictions are the more useful half.
- One entry in the locked batch issue ledger was **read** after a checkpoint, as post-hoc historical
  comparison. Nothing in it was edited.
- Locked shared files untouched: `CANON-003-batch-issue-ledger.md`,
  `CANON-003-multi-source-synthesis.md`, `CANON-003-CONTROLLER-BRIEF.md`, `canon/HANDOFF.md`.
  Lane A/B/C and Lane D files untouched — this branch contains none of them.
- No page images, figures or source text committed. All rendering and inspection ephemeral.
- No synthesis performed. Recurrence counts in the lane issue file are **within this lane only**.

## For the integrator

Three things this lane cannot settle alone:

1. **R-07** is the sharpest new question: a figure can be present, legible and inspected, and still
   be unable to support the claim it illustrates. Whether that has happened elsewhere in the batch
   is checkable only by re-reading each `visually_demonstrated` object against its figure.
2. **R-01** predicts that any conversion rendering display type as vector art will flatten a
   source's structure from the top down. Other EPUB-sourced books in the batch can be tested for it
   cheaply by comparing text headings against image elements in heading positions.
3. **R-03** and **R-06** are both about qualifications that scope over a whole source — a technology
   dependency and a declared epistemic stance — which SPEC-03 can only record object by object.
   Whether that shape recurs is a cross-lane question.

Both assigned books are complete, validated, historically reconciled, committed and pushed. Nothing
is in progress. Returning to Controller.
