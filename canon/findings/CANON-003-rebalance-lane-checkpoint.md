# CANON-003 — Rebalance-lane checkpoint

**Branch:** `work/canon-003-rebalance-d` · cut fresh from the common parallel base `4cbe257`
**Amendment:** `canon/tasks/CANON-003-REBALANCE-01.md`, Controller-approved 24 Aug 2026
**Updated:** 24 Aug 2026, after book 8.

**Communication check:** I will explain technical ideas in plain English, including what they mean,
why they matter, and their practical consequence; use minimum sufficient wording without sacrificing
understandability; separate evidence from inference; and never invent facts. I have read
`shared/COMMUNICATION-STANDARD.md`.

## Execution amendment, recorded here as the amendment requires

Books 8 and 11 were reassigned to this worker because Lane D finished its three books while other
lanes still had six outstanding. Both books were fixed in `CANON-003-PARALLEL-EXECUTION.md` before
any parallel-lane result existed, and both were marked not started at the time of the Controller
audit, so no source was chosen in the light of emerging findings.

The amendment notes that perfect cognitive erasure cannot be guaranteed when the same external agent
identity is reused, and that the safeguard is procedural and auditable. What was actually done:

- work is on a **fresh branch from the common base**, not a continuation of `work/canon-003-d`;
- the Lane D worktree is a different directory and its issue file and checkpoint were **not opened**
  during either extraction;
- no Lane A/B/C fresh findings, issue files or checkpoints were read;
- each book's fresh extraction was committed **and pushed** before any historical, planning or
  cross-book material was opened;
- where a finding resembles something a reviewer may recognise from elsewhere, the derivation from
  the source text is written out so it can be checked rather than trusted.

## Books

| # | Book | Section | Status | Fresh checkpoint | Historical |
|---|---|---|---|---|---|
| 8 | John Alton, *Painting With Light* (1949; UC Press ed.) | ch.2 "Motion Picture Illumination", complete | **complete, validated, pushed** | `ab2a833` | no extraction comparator; coverage-map judgements confirmed on lighting and camera placement, contradicted on colour grading |
| 11 | Christopher Kenworthy, *Master Shots* | to be defined | not started | — | — |

## Book 8 outputs

`canon/knowledge/current/alton-painting-with-light-ch2/` — `visual-evidence-ledger.yaml`,
`source-knowledge.yaml` (27 objects), `source-concept-systems.yaml` (3 systems),
`ontology-mappings.yaml` (22 terms, 9 relations, 3 concepts), `operational-bindings.yaml`
(6 bindings, 2 Creative IR), `PROVENANCE.md`.
Findings: `canon/findings/CANON-003-book08-alton-findings.md`.

Mechanical validation passes SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer
constraints. The validator is an ephemeral scratchpad script, not committed, consistent with earlier
books in this batch.

## What book 8 found, in plain English

**The file format turned the book's headings into pictures.** Every chapter and section title in
this EPUB is a vector drawing of letters, not text. The chapter's *deeper* headings are ordinary
text and survive. So a text-only extraction produces a chapter that looks flat and coherent — 39
topics in a row — instead of a six-part chapter, with no sign anything is missing. Rasterising the
headings recovered all six section names, and every section cited in this extraction came from that
render.

**The figures, by contrast, survived perfectly**, which answers an open question the batch recorded
before the split: for a book that argues through diagrams rather than page layout, figure-only
evidence is enough. A full overhead lighting plan is just as usable without a page around it.

**The harder issue is that this source ages at three different rates at once** — physical geometry
that does not date, film technology that has dated completely, and one studio convention of the
period stated as technical fact. All three look identical in the schema; only reading separates
them.

## Unresolved local issues

Five entries in `canon/findings/CANON-003-rebalance-lane-issues.md`: R-01 headings as images with an
inverted surviving hierarchy; R-02 a visually demonstrated claim still under-determined after the
figures were inspected; R-03 three shelf lives indistinguishable by claim type; R-04 counter-evidence
that figure-only evidence sufficed for a diagram-argued book; R-05 counter-evidence that a source
policing its own vocabulary is the easy case for the ontology layer.

Nothing applied. The method stays frozen.

## Method discipline

- Fresh checkpoint committed and pushed before any historical search.
- Locked shared files untouched: `CANON-003-batch-issue-ledger.md`,
  `CANON-003-multi-source-synthesis.md`, `CANON-003-CONTROLLER-BRIEF.md`, `canon/HANDOFF.md`.
  One issue in the batch ledger was **read** after the checkpoint, as post-hoc historical
  comparison; nothing in it was edited.
- No page images, figures or source text committed. All renders ephemeral.
- No synthesis performed.

## Next

Book 11, Christopher Kenworthy, *Master Shots*. EPUB. The inventory describes it as procedural
recipes, which is a different knowledge shape from anything in this lane so far.
