# Provenance record — In the Blink of an Eye, pp.1–25 (CANON-003 book 10, Lane B)

**Book:** Walter Murch, *In the Blink of an Eye*, revised 2nd edition, Silman-James Press, 2001.
**Section processed:** printed pages 1–25, contiguous — seven consecutive named sections: *Cuts and
Shadow Cuts*, *Why Do Cuts Work?*, *"Cut Out the Bad Bits"*, *Most with the Least*, *The Rule of
Six*, *Misdirection*, *Seeing Around the Edge of the Frame*.

## Why this section

It is the book's theoretical opening, it runs unbroken, and it contains the Rule of Six in full —
the ranked framework that is this source's reason for selection into the batch. Nothing was taken
from elsewhere in the book.

**A boundary that is stated, not hidden.** On printed page 9 the source poses its central question —
"cuts do work. But the question still remains: Why?" — and answers it with "We will get back to this
mystery in a few moments". It actually returns to it on printed pages 58–64, via John Huston's
remark about blinking, which is the passage the book is named for and is thirty-three pages outside
this span. That question is recorded here as the **source's own open question**
(`source_uncertainty: source_asks_open_question`), not as an unanswered gap, and no part of the
later answer has been imported.

This is a property of the source's form. A transcribed lecture can raise a question, spend fifty
minutes elsewhere and return to it, so **any windowed extraction of a source shaped like this may
hold a question without its answer** — through no fault of the window.

## Identity and integrity

The PDF carries **no metadata at all** — no title, author, creator or producer — and its creation
date (2012) is eleven years after the edition. Identity was therefore established from the book's
own front matter, not from the file:

| Check | Result |
|---|---|
| Local file | `~/Downloads/Books/In the Blink of an Eye Revised 2nd Edition.pdf` |
| Copyright page | "Copyright 1995, 2001 by Walter Murch" |
| ISBN | 1-879505-62-2 |
| LoC control number | 2001042949 |
| Publisher | Silman-James Press, Beverly Hills |
| Stated origin | "a revised transcription of a lecture on film editing given by Walter Murch in the mixing theater at Spectrum Films, Sydney, Australia, in October 1988" |
| PDF pages | 81, each a **two-page spread**, 774 × 611.76 pts |
| Page mapping | printed page = 2×(spread) − 14 (left) and −13 (right); verified at four independent points |
| Source type | **Scanned**, with an OCR text layer — 81 pages, 81 full-page greyscale images |

## Source integrity — a structural hazard that was removable

**The hazard.** Because each PDF page is a two-page spread, naive full-page extraction reads lines
across *both* printed pages by vertical position. On spread 15 it produced: "and over here we have
the Mona Lisa, and, by the" (left page) → a line of "The Rule of Six" (right page) → "way, look at
these floor tiles" (left page again). Two unrelated arguments spliced into one stream. This is the
same failure mode that blocked the Lupton anchor.

**The resolution.** Each spread was cropped into its two halves before extraction — `-x 0 -W 387`
and `-x 387 -W 387` against a 774 pt page — and each half processed as its own page. Every half then
reads as continuous single-column prose.

**What that is and is not.** It is a mechanical extraction choice that respects the physical
geometry of the artifact, in the same class as decoding character entities before comparing text. It
is **not** reading through corruption: no character was altered, nothing was inferred, and both
extractions contain the same words — only the order differs.

**Scope.** Recorded strictly about this book. Whether any other blocked source in this batch would
respond to the same treatment has **not been checked by this lane and is not implied**. What this
case does establish is narrower and still useful: *interleaving can be a property of an extraction
as well as of a file, so "interleaved" is not by itself a verdict.*

**OCR damage: usable.** 6,493 words in the span; 2 letter-digit confusions (0.03%); no vowel-less
words; one non-ASCII character. Remaining artifacts are em-dashes rendered as hyphens, a stray
capital `I` on p.17 from the drop-cap `T` being read twice, two words clipped on p.1
(`Apocal'se Now`, `-ualifies`), and two slips on pp.21 and 23 (`undOing`, `may to forcing`). Every
damaged instance is locally obvious. **None falls inside a claim this extraction records**, with one
exception, marked: `sk_murch_c003_0036` carries `extraction_uncertainty: ocr_degraded` because the
sentence about a shot's cost is missing a word. Its reading was confirmed against the rendered page.

Comparable to Albers (usable) rather than Lupton (blocked). The load-bearing content — the Rule of
Six list, its six percentages, the sacrifice rule, both footnotes — extracts cleanly and was checked
against the rendered page.

**Section completeness check.** All seven section titles listed in the contents page for pp.1–25 are
present in the extracted text, each starting on the printed page the contents page names.

## Visual evidence — VERIFIED, and there is nothing to lose

`visual_completeness: verified_page_level`. Thirteen spreads rendered ephemerally at 100 dpi, three
inspected closely including both spreads carrying the Rule of Six; none committed.

**The section contains zero figures.** Twenty-five printed pages of continuous prose and footnotes.
The only non-prose typography is the Rule of Six list itself, which is set as *text* and therefore
extracts intact — numbers, order and all.

This is worth stating as a result rather than an absence: **a source can be fully visually verified
and contribute no visual evidence.** It is the opposite pole from book 9 in this same lane, which
carries 23 figures across 55 pages and loses every one of them to text extraction. Two books, one
domain, one batch — total visual-loss risk in one, zero in the other. Domain does not predict visual
dependence; the author's mode of argument does.

What *is* lost is a third kind: **typographic emphasis**. On printed page 19 four conjunctions are
italicised to mark a cumulative tally of satisfied criteria ("...gives the right emotion *and* moves
the story forward, *and* is rhythmically satisfying, *and* respects eye-trace and planarity, *but* it
fails..."). Every word survives; the weighting does not. A plain-text extractor sees all the words
and cannot see which ones the author leaned on.

## The Rule of Six and the schema — the operator's question, answered

The ranked list is represented with SPEC-03's **existing** `priority_order` system type
(`scs_murch_c003_001`). No structure was invented. What that type carries, it carries faithfully:
six members with `order` 1–6, `ordering.scheme: source_numbered`, `origin: source_stated`, the
sacrifice procedure, and the two worked trade-offs.

**What it cannot carry is the interval.** Murch's percentages — 51, 23, 10, 7, 5, 4 — are not
decoration. They say emotion outweighs the other five *combined*, and that the gap between rank 2
and rank 3 is wider than the entire spread from rank 3 to rank 6. Read as a bare ordinal list, the
Rule of Six looks like six roughly comparable considerations in a preferred sequence, which is close
to the opposite of what the source argues.

SPEC-03 has no field for a member weight. The numbers are therefore preserved **verbatim** inside
`sk_murch_c003_0020`–`0025` and `sk_murch_c003_0029`, readable by a human and not by a machine, and
the insufficiency is recorded as evidence in the lane issue file as **LB-10**. A second thing the
type cannot hold: the ordering is claimed to be *perceptual* as well as preferential — higher items
mask failures of lower ones — which is carried as an ordinary member because `ordering` has only
`scheme` and `origin`.

Two markings the source puts on its own framework are preserved and flagged, because both are
routinely dropped when this list is quoted elsewhere: the weights are "slightly tongue-in-cheek, but
not completely", and the whole list is scoped as "An ideal cut **(for me)**".

## Mechanical validation

All five files pass SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints:
39 SourceKnowledge objects · 4 SourceConceptSystems · 23 ontology terms · 9 relationships ·
3 concepts (2 source-specific, 1 canonical, 0 cross-source — correct for a single-source file) ·
8 operational bindings.

## Historical material

Sealed until this book's fresh checkpoint commit exists. Not opened during extraction. Whether any
historical Murch material exists in this repository has **not been checked** — that search happens
after the checkpoint, per CANON-003.
