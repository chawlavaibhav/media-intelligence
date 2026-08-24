# CANON-003 — Lane D checkpoint

**Branch:** `work/canon-003-d` · **Lane:** D, storytelling / creative process
**Updated:** 24 Aug 2026, after book 16.

**Communication check:** I will explain technical ideas in plain English, including what they mean,
why they matter, and their practical consequence; use minimum sufficient wording without sacrificing
understandability; separate evidence from inference; and never invent facts. I have read
`shared/COMMUNICATION-STANDARD.md`.

## Books

| # | Book | Section | Status | Fresh checkpoint | Historical |
|---|---|---|---|---|---|
| 16 | Ed Catmull with Amy Wallace, *Creativity, Inc.* (2014) | ch.5 "Honesty and Candor", complete | **complete, validated, pushed** | `b7f0d47` | no comparator exists — searched after checkpoint |
| 17 | David Bayles & Ted Orland, *Art & Fear* | to be defined | not started | — | — |
| 18 | Donald Miller, *Building a StoryBrand* | to be defined | not started | — | — |

## Book 16 outputs

`canon/knowledge/current/catmull-creativity-inc-ch5/` — `visual-evidence-ledger.yaml`,
`source-knowledge.yaml` (21 objects), `source-concept-systems.yaml` (2 systems),
`ontology-mappings.yaml` (23 terms, 10 relations, 3 concepts), `operational-bindings.yaml`
(5 bindings, **0 Creative IR**), `PROVENANCE.md`.
Findings: `canon/findings/CANON-003-book16-catmull-findings.md`.

Mechanical validation passes SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer
constraints. The validator is an ephemeral scratchpad script, not committed, consistent with
earlier books in this batch.

## Unresolved local issues

Six entries in `canon/findings/CANON-003-lane-D-issues.md`. Two are limitations of the current
schemas that Lane D could not represent cleanly and recorded as evidence instead of working around:

- **D-01** — `executable_by` has no value for a remedy that is a social action, so nine remedies
  read `unknown` when they are in fact well understood.
- **D-02** — nothing distinguishes a claim the book's author makes from one he quotes approvingly
  from a named colleague.

Two more record the visual pass returning nothing (**D-03**), and process knowledge whose structure
the source never made explicit anywhere (**D-04**). Two are counter-evidence: zero Creative IR
bindings arrived without any pressure to invent them (**D-05**), and `broader_than` was usable
(**D-06**).

Nothing here was applied. The method stays frozen.

## Method discipline

- The fresh checkpoint for book 16 was committed and pushed **before** any search for historical
  material. The search then found none, which is recorded rather than filled.
- No other lane's findings were read. The shared batch issue ledger was not opened.
- Locked shared files untouched: batch ledger, synthesis, Controller Brief, `canon/HANDOFF.md`.

## Next

Book 17, *Art & Fear*. It is a **PDF with page renders available**, so unlike book 16 it can carry a
real page-level visual pass. Section to be chosen after the integrity check.
