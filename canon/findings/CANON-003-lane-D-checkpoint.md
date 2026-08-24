# CANON-003 — Lane D checkpoint

**Branch:** `work/canon-003-d` · **Lane:** D, storytelling / creative process
**Updated:** 24 Aug 2026, after book 18. **Lane D assignment is complete.**

**Communication check:** I will explain technical ideas in plain English, including what they mean,
why they matter, and their practical consequence; use minimum sufficient wording without sacrificing
understandability; separate evidence from inference; and never invent facts. I have read
`shared/COMMUNICATION-STANDARD.md`.

## Books — all three complete

| # | Book | Section | Status | Fresh checkpoint | Historical |
|---|---|---|---|---|---|
| 16 | Ed Catmull with Amy Wallace, *Creativity, Inc.* (2014) | ch.5 "Honesty and Candor", complete | **complete, validated, pushed** | `b7f0d47` | no extraction comparator; pre-batch curriculum judgement converged |
| 17 | David Bayles & Ted Orland, *Art & Fear* (1993) | Part I ch.I–II, printed pp.1–21 | **complete, validated, pushed** | `75e4da1` | no extraction comparator; same curriculum judgement, converged |
| 18 | Donald Miller, *Building a StoryBrand* (2017) | Section 1, ch.1–3, complete | **complete, validated, pushed** | `f0127e4` | no extraction comparator; coverage-map judgement converged, inventory's "few figures" contradicted |

**No book in this lane was blocked.** All three sources had usable text; two are EPUBs and one is an
OCR'd scan whose damage is confined to page furniture.

## Totals

| | Book 16 | Book 17 | Book 18 | Lane D |
|---|---|---|---|---|
| SourceKnowledge objects | 21 | 23 | 18 | **62** |
| SourceConceptSystems | 2 | 3 | 2 | **7** |
| Ontology terms | 23 | 18 | 22 | **63** |
| Relations | 10 | 9 | 8 | **27** |
| Concepts | 3 | 3 | 3 | **9** |
| Operational bindings | 5 | 3 | 7 | **15** |
| *of which Creative IR* | 0 | 0 | 4 | **4** |

All three directories pass mechanical validation against SPEC-03 rules 1–7, SPEC-04 rules 1–9 and
the SPEC-05 layer constraints. The validator is an ephemeral scratchpad script, not committed,
consistent with earlier books in this batch.

## What Lane D found, in plain English

**Two books about the maker, one about the message.** *Creativity, Inc.* is about how a group
criticises work in progress; *Art & Fear* is about why makers stop making. Between them they
produced 44 knowledge objects and **not one Creative IR binding** — which is the correct result. The
Creative IR describes what a single asset contains, and neither book discusses that. Under the old
rule that every atom had to name a product field, these two chapters would have yielded either
nothing or forty invented bindings.

**Then the third book inverted it.** *Building a StoryBrand* produced four Creative IR bindings from
eighteen objects — and it is the weakest-evidenced source in the lane, with uncontrolled revenue
claims, a foundational mechanism delivered as reported conversation, and a closing position that
cannot be contradicted by any outcome. **The source that binds best is the source that supports
least.** That is issue D-13 and it is the most consequential thing this lane found.

**The visual pass mattered exactly once, and count did not predict when.** Books 16 and 18 have
almost the same number of images — 33 and 36. In book 16 not one supports a claim; its only
in-chapter image is a 525×1 pixel rule. In book 18 four do, and two carry content the text never
states: the framework diagram forks where the prose lists a sequence, and the output template holds
a field schema including an eighth element in a framework named for seven. What predicts visual loss
is whether the source teaches a **structure**, not how many pictures it has.

## Unresolved local issues

Fourteen entries in `canon/findings/CANON-003-lane-D-issues.md`.

**Schema could not represent it cleanly — recorded as evidence, nothing applied:**
- **D-01** — `executable_by` has no value for a remedy that changes how people work rather than what
  an asset contains. 2 of 3 books; book 18 bounded the problem usefully.
- **D-02** — nothing distinguishes the author's own claim from one quoted approvingly from a named
  third party. 2 of 3 books.
- **D-07** — a source declaring its premises as chosen working assumptions cannot be marked as such.
- **D-03** — the visual-completeness vocabulary has no value for "inspected; the source makes no
  visual argument", and the one value used covers two very different situations across this lane.

**Findings about the batch's own method:**
- **D-12** — figure count was the inventory's proxy for visual exposure and does not track it.
- **D-13** — bindability and evidence quality moved in opposite directions.
- **D-09** — a title-string search missed a comparator over a comma; corrected, and all three books
  re-searched on author surnames.
- **D-08** — the most quotable line in book 17 was the one that bound least honestly; refused and
  recorded.

**Counter-evidence and evidence for the current design:**
- **D-05** — zero Creative IR bindings arrived twice with no pressure to invent any.
- **D-10** — origin fields discriminate: `extractor_synthesis` where the source declares nothing,
  `source_explicit` where it does.
- **D-14** — a genuine term collision with our own vocabulary (`hero`) was held apart by the schema.
- **D-06** — `broader_than` and `narrower_than` were usable where they fitted.
- **D-04**, **D-11** — process knowledge carries structure the source never made explicit; evidence
  profile may track domain rather than author, and book 18 is consistent with that on a sample far
  too small to establish it.

Nothing was applied. The method stayed frozen throughout.

## Method discipline

- Every fresh checkpoint was committed **and pushed** before any search for historical material.
- No historical extraction exists for any of the three books. Pre-batch **planning** judgements were
  found in `canon/experiments/` after the checkpoints; two converged with the fresh results and one
  was contradicted. **Contamination check run:** those documents were not read before or during any
  extraction. The convergences are genuine and the contradiction is recorded as the more useful of
  the two.
- No other lane's findings were read at any point. The shared batch issue ledger was not opened.
- Locked shared files untouched: `CANON-003-batch-issue-ledger.md`,
  `CANON-003-multi-source-synthesis.md`, `CANON-003-CONTROLLER-BRIEF.md`, `canon/HANDOFF.md`.
- No page images, figures or source text committed. All renders ephemeral.
- No synthesis performed. Recurrence counts in the lane issue file are **within Lane D only**;
  combining them with other lanes is the integrator's job.

## For the integrator

Three things Lane D cannot settle alone and which the other lanes can test:

1. **D-01 and D-02** are schema gaps that should show up in any process-, interview- or
   reportage-shaped source. Lane B's *The Conversations* is an interview transcript and is the
   obvious place to check D-02.
2. **D-13** — whether bindability tracks subject-proximity rather than quality should be visible
   across all four lanes at once, by comparing binding counts against evidence profiles.
3. **D-11** — whether evidence profile tracks domain rather than author needs books classified by
   different extractors, which only the merge provides.

Lane D is finished. Nothing is in progress and nothing is half-extracted.
