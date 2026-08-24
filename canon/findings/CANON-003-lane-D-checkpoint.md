# CANON-003 — Lane D checkpoint

**Branch:** `work/canon-003-d` · **Lane:** D, storytelling / creative process
**Updated:** 24 Aug 2026, after book 17.

**Communication check:** I will explain technical ideas in plain English, including what they mean,
why they matter, and their practical consequence; use minimum sufficient wording without sacrificing
understandability; separate evidence from inference; and never invent facts. I have read
`shared/COMMUNICATION-STANDARD.md`.

## Books

| # | Book | Section | Status | Fresh checkpoint | Historical |
|---|---|---|---|---|---|
| 16 | Ed Catmull with Amy Wallace, *Creativity, Inc.* (2014) | ch.5 "Honesty and Candor", complete | **complete, validated, pushed** | `b7f0d47` | no extraction comparator; a pre-batch curriculum judgement exists and converged |
| 17 | David Bayles & Ted Orland, *Art & Fear* (1993) | Part I ch.I–II, printed pp.1–21 | **complete, validated, pushed** | `75e4da1` | no extraction comparator; same curriculum judgement, converged |
| 18 | Donald Miller, *Building a StoryBrand* | to be defined | not started | — | — |

## Outputs so far

`canon/knowledge/current/catmull-creativity-inc-ch5/` — 21 SourceKnowledge · 2 systems · 23 terms ·
10 relations · 3 concepts · 5 bindings (**0 Creative IR**) · PROVENANCE · visual ledger.
`canon/knowledge/current/bayles-orland-art-and-fear/` — 23 SourceKnowledge · 3 systems · 18 terms ·
9 relations · 3 concepts · 3 bindings (**0 Creative IR**) · PROVENANCE · visual ledger.

Findings: `CANON-003-book16-catmull-findings.md`, `CANON-003-book17-art-and-fear-findings.md`.

Both directories pass mechanical validation against SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the
SPEC-05 layer constraints. The validator is an ephemeral scratchpad script, not committed,
consistent with earlier books in this batch.

## What Lane D has found so far, in one paragraph

Two books whose subject is the *maker* rather than the *made thing*. Both produced substantial
usable knowledge and **neither produced a single Creative IR binding** — which is the correct
result, not a failure, and is the clearest evidence yet for splitting what a source teaches from
what our product can use. Two schema limitations recurred across both books: the repair vocabulary
has no value for a social action, and nothing records whether a claim is the author's own or one he
quotes approvingly. One new limitation appeared in book 17: a source may declare its foundations as
assumptions it chose rather than findings it reached, and the schema cannot mark that category.

## Unresolved local issues

Eleven entries in `canon/findings/CANON-003-lane-D-issues.md`.

**Schema could not represent it cleanly (recorded as evidence, nothing applied):**
- **D-01** — `executable_by` has no value for a remedy that is a social action. **2 of 2 books.**
- **D-02** — nothing distinguishes the author's own claim from one quoted approvingly from a named
  third party. **2 of 2 books**, heavier in book 17.
- **D-07** — a source declaring its premises as chosen working assumptions cannot be marked as such.
- **D-03** — the visual-completeness vocabulary has no value for "inspected; the source makes no
  visual argument".

**Method hazards found against my own work:**
- **D-09** — a title-string search missed a comparator over a comma. Corrected; both books
  re-searched on author surnames too.
- **D-08** — the most quotable line in book 17 was the one that bound least honestly. Refused and
  recorded.

**Counter-evidence and evidence for the current design:**
- **D-05** — zero Creative IR bindings arrived without any pressure to invent them.
- **D-10** — when a source really does declare a system, the origin fields say `source_explicit`;
  when it does not, they say `extractor_synthesis`. Two books, opposite readings, no adjustment.
- **D-06** — `broader_than` was usable where it fitted.
- **D-04**, **D-11** — process knowledge carries structure the source never made explicit; and the
  two books' evidence profiles are near-identical despite completely different material, which may
  mean profile tracks domain rather than author. Marked INFERRED — only the integrator can test it.

Nothing here was applied. The method stays frozen.

## Method discipline

- Both fresh checkpoints were committed **and pushed** before any search for historical material.
- The historical search found no earlier extraction for either book. It did find a pre-batch
  planning document, `canon/experiments/CANON-CURRICULUM-V0.md`, which excluded both books from the
  Canon curriculum as "aimed at our own judgement rather than at creative output" — the same
  conclusion both fresh extractions reached independently by producing zero Creative IR bindings.
  **Contamination check run:** the `canon/experiments/` documents were not read before or during
  either extraction. The convergence is genuine.
- No other lane's findings were read. The shared batch issue ledger was not opened.
- Locked shared files untouched: batch ledger, synthesis, Controller Brief, `canon/HANDOFF.md`.
- No page images or source text committed. All renders ephemeral.

## Next

Book 18, Donald Miller, *Building a StoryBrand*. EPUB. It is deliberately the opposite shape from
books 16 and 17: an explicit named framework applied commercially, which should bind to the product
schema far more readily than either. If it does not, that is a stronger result than if it does.
