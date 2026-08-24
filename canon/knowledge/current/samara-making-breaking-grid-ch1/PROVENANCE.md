# Provenance record — Samara, *Making and Breaking the Grid* (CANON-003 book 6, Lane A)

**Book:** Timothy Samara, *Making and Breaking the Grid: A Graphic Design Layout Workshop*,
Second Edition, Updated and Expanded. Rockport Publishers, 2017. ISBN 9781631594090.
**Section processed:** Chapter 1, "Making the Grid" — the instructional core, printed pages 20–76:
*Grid Basics*, *Building a Grid*, *Using a Grid*.

## Why this section

Chapter 1 has four named parts. "Coming to Order" (pp.11–18) is a historical survey of the grid's
development, and "Exhibits" (pp.77–124) is a gallery of projects with short notes. Neither carries
the author's craft reasoning. The three middle parts do, and they are continuous: a taxonomy of
structures, then a method for deriving one, then the judgement needed to use it.

Taking only *Grid Basics* — one titled section, about 22 pages — would have produced a vocabulary
list with none of the reasoning that uses it. CANON-003 says to enlarge the section rather than
accept a count that fails to expose the author's reasoning system, so the section was enlarged.
Chapter 2, "Breaking the Grid", is the book's counter-argument and is a separate treatment.

**This is a larger section than the batch's earlier books.** 57 printed pages and 14,737 words of
running text and captions, against roughly 20 printed pages for *Grammar of the Shot* ch.4 and 13
spreads for *The Vignelli Canon* Part One. The consequence for object counts is discussed below and
recorded in the Lane A issue file.

## Identity and integrity

| Check | Result |
|---|---|
| Local file | `~/Downloads/Books/Making and Breaking the Grid_ A Graphic Design Layout Workshop.epub` |
| `dc:title` / `dc:creator` | "Making and Breaking the Grid" / "Timothy Samara" |
| `dc:publisher` / `dc:date` | Rockport Publishers / 2017 |
| `dc:identifier` | 9781631594090 |
| `dc:format` | "240 Pages" |
| `dcterms:modified` | 2017-07-14 |
| Edition confirmed by | the book's own contents page: "Making and Breaking the Grid, Second Edition, Updated and Expanded" |
| Source type | EPUB 3.0, publisher-produced, **not** a scan — real text, real fonts, 442 embedded images |
| Printed-page anchors | present throughout (`epub:type="pagebreak" id="page_N"`), 114 in chapter 1 |

**Every page number in this extraction is a printed page number taken from the publisher's own
anchors.** Nothing is inferred from position.

### Text integrity — clean

Measured over the 14,737-word section:

| Check | Result |
|---|---|
| Tokens mixing letters and digits (an OCR signature) | **0** |
| Tokens of irregular shape | 18 of 14,752 = **0.12%** |
| Lines lacking terminal punctuation | 214 of 461 — all of them designer credit lines, which is correct |

The 18 irregular tokens are proper nouns carrying the publisher's own small-caps markup
("VIgnellis", "TImothy") plus foreign-language names. There is **no** OCR damage and **no** column
interleaving of the kind that blocked Lupton. `extraction_uncertainty: none` on every object whose
only limitation is that its figure was not opened.

## Visual evidence — partial, and for a reason worth recording

`visual_completeness: partial_figures_only`. 120 figure references fall in pp.20–76; 6 figures were
opened and inspected. Colour is intact — 17 of 20 randomly sampled figures carry colour, up to
3,148 coloured pixels per 3,600 sampled — so this is a colour-bearing source, unlike the Albers
digitisation.

**What cannot be inspected is the page.** An EPUB reflows; there is no printed page to render. That
is not a defect in this file, it is what the format is. Three consequences, all recorded in
`visual-evidence-ledger.yaml`:

1. **The book's self-demonstration is gone.** This book argues for page structure and its own pages
   are built on a rigorous one — it says so twice, citing its own baselines and its own leading
   multiples, and one caption analyses one of its own spreads as a worked example. In the EPUB none
   of that exists. This is a **new loss mechanism** for this batch: not a bad scan (Albers) and not
   a bad text-layer order (Vignelli), but a delivery format that has no page. It is upstream of any
   extraction we perform and no extraction method can recover it.
2. **Some words are pixels.** Diagram labels are typeset into the artwork. The six modular-grid
   notations on p.28 — 3×4 through 9×14 — exist only inside the image file. A text-only pass gets
   the notation rule stated abstractly and none of its worked instances, with nothing in the text
   signalling the loss.
3. **Caption coverage is uneven inside one book.** 11 of the 120 figure references carry no caption
   at all, counted mechanically. One of them, f0034-01, is the positive demonstration of the book's
   central image rule; the only caption on that page describes the error instead. Meanwhile p.24's
   caption is nearly a complete verbal description of its figure. Treating "captioned" as
   "recovered" would over-report completeness on this source.

A fourth observation **refines** rather than confirms an earlier concern: 14% of sentences carry
spatial deixis ("shown below", "at top", "diagrammed here"), but most still resolve, because the
EPUB keeps figures in reading order. What breaks is specifically deixis pointing *within* a single
composite figure ("Top / Middle / Bottom" on p.32) or *across a printed spread* ("the diagram
opposite"). That is narrower and more checkable than "spatially argued sources cannot be trusted in
text".

## What was produced

| File | Contents |
|---|---|
| `visual-evidence-ledger.yaml` | 5 demonstrations, 4 visual-only observations |
| `source-knowledge.yaml` | **79 objects** |
| `source-concept-systems.yaml` | 6 systems |
| `ontology-mappings.yaml` | 53 terms, 14 relationships, 6 concepts |
| `operational-bindings.yaml` | 12 bindings |

All validate against SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints.

### On the object count

**79 objects is more than the first five books of this batch produced between them (90).** No
granularity rule was changed. The V0 rule — split when a claim can be retrieved, supported,
contradicted or qualified independently; do not split for a further example, explanation or
restatement — was applied unchanged, and it decided every case without an invented exception.

Two things drive the count, and both are properties of the source:

- **It is a rule-dense procedural manual.** Most claims are imperative craft rules attached to a
  named element, each independently contradictable. Six of them are the "special cases" of text
  behaviour on p.37 alone.
- **The source itself separates them.** A large proportion of these rules are figure captions —
  one rule, one illustration, one caption. The splitting is the book's, not ours.

The section is also about three times the size of the batch's smaller sections. Objects per printed
page is roughly 1.4 here (79 over 57 pages), against 0.85 for *Grammar of the Shot* ch.4 (17 over
printed pp.93–112). *The Vignelli Canon* is 13 objects over 13 PDF spreads, so 1.0 per spread but
about 0.5 per printed page — the two units are not interchangeable and the comparison is only
approximate. Density here is genuinely higher, but by well under the raw count difference: most of
the gap is section size, not splitting.
This matters for the batch because it means **"one representative section" is not a constant unit
of work across sources**, and per-book counts are not comparable without normalising. Recorded in
the Lane A issue file rather than fixed.

### On the binding count

12 bindings against 79 objects. Most of the book is left unbound, which SPEC-04 says is normal.

Where it does bind, the fit is unusually direct — the best of any book in this batch so far.
`StaticCreativeExtension` names `typography_layout`, `spatial_hierarchy` and a `composition` field
covering depth and figure-ground, and this source is about exactly those three things. Two claims
turned out to be **mechanically checkable**, which is rare in this corpus: whether an element's
edges land on the structure's guides, and whether a line of continuous text runs 50–80 characters.

The largest single block of usable material — the whole derivation from type specimens to a locked
baseline grid — is parked as `production_candidate` and deliberately **not translated**. Every step
is exactly executable by a layout engine and none of it is a generation action. Asking a model to
"use a 5×12 modular grid with 12-point row gutters" is a different and unevidenced claim, and this
extraction does not make it.

## Historical material

**Searched after the fresh checkpoint commit, per CANON-003's sealed-until-checkpoint rule.**
Result recorded in `canon/findings/CANON-003-book06-samara-findings.md`.
