# Provenance — Samara, *Making and Breaking the Grid*, Chapter 2 "Breaking the Grid"

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon and nothing here may
be described as accepted. This is exploratory, non-merge work under
`canon/experimental/book-expansion-qa-v1/`.

`source_id: samara-breaking-the-grid-ch2` · ID prefix `sgb`

---

## 1. Source identity

| Field | Value |
|---|---|
| Author | Timothy Samara |
| Title | *Making and Breaking the Grid: A Graphic Design Layout Workshop* |
| Edition | Second Edition, Updated and Expanded |
| Publisher / year | Rockport Publishers, 2017 |
| ISBN (`dc:identifier` in the EPUB) | 9781631594090 |
| Format | EPUB 3.0, publisher-produced, reflowable. Not a scan. |
| First edition | 2003 (the chapter refers to it explicitly) |

## 2. Span processed

**Chapter 2, "Breaking the Grid"** — spine document 6, `ops/xhtml/ch02.xhtml`, in its entirety:

- the untitled chapter-opening argument
- *On the Other Hand — A Historical Survey of Non-Structural Design Tendencies*
- *Alternative Architectures — Intuitive, Relational, and Conceptual* (all sub-sections)
- *Considering the Practical in the Impractical* (all sub-sections)
- *Exhibits — Design Projects Without Grids* (exhibits 01–35)

Plus **one object** from chapter 1's *Coming to Order* (`sk_sgb_0006`), taken under the lane brief's
allowance to extract from that part where it carries reasoning rather than chronology. Nothing else
was taken from chapter 1. See `EXTRACTION-NOTES.md` §4 for the negative finding on that part.

**Boundaries confirmed directly.** In the supplied text file, spine 5 is `TITLE 1 Making the Grid`
and spine 6 is `TITLE 2 Breaking the Grid`; spine 7 is `Directory of Contributors`. Chapter 2 runs
from the spine-6 marker to the spine-7 marker and is **20,766 words** of running text and captions.

## 3. Material available and how it was read

| Item | Value |
|---|---|
| Primary text | `scratchpad/src/EPUB-Making_and_Breaking_the_Grid__A_.txt` |
| sha256 of that file | `d52616e0eca30d5691a3c0acb0fef64281fedb6bfe489ca151d33f4d10def1fa` |
| Original | `~/Downloads/Books/Making and Breaking the Grid_ A Graphic Design Layout Workshop.epub` (30,988,392 bytes) |
| Figure references in chapter 2 | **202 distinct**, in the EPUB's own `ch02.xhtml` |
| Figures inspected | **0** |
| Text integrity | clean; no OCR signature, no column interleaving. Four typographical errors in the publisher's own text were observed (`rcetangular`, `esnure`, `shcool`, `disection`) and are the publisher's, not damage. |

## 4. Locators — Case 3, EPUB, **no page numbers**

The supplied text file's own header states:

> `FORMAT: EPUB (reflowable). THERE ARE NO AUTHORED PAGE NUMBERS IN THIS FORMAT.`

Per `SCHEMA-CONTRACT-ADDENDUM-LOCATORS.md` **Case 3**, every locator in this lane is
**chapter + section by name**, optionally with `(spine 6)` as a file-position aid.
`page_start` and `page_end` are `null` on every object without exception. The audit pattern
**`no_authored_page`** is recorded in `EXTRACTION-NOTES.md`.

**No page number appears anywhere in this lane.** One in-text cross-reference in chapter 2 —
`(see Coming to Order )` — is a link whose target page is unresolvable in this copy; it was not
guessed. A second, `(see the detail images immediately to the right)`, is spatial deixis across a
printed spread and is likewise unresolvable here.

**A finding that must not be misread as permission.** The EPUB *file* does carry publisher
`epub:type="pagebreak"` anchors (110 in `ch02.xhtml`), which is how the live chapter-1 lane obtained
printed pages. The **delivered extraction route for this lane strips them**, and the binding
addendum places this lane in Case 3. This lane therefore cites no pages. The asymmetry with the live
record is an artefact of the delivery route, not of the book, and is recorded in
`EXTRACTION-NOTES.md` §3 rather than resolved by inventing citations.

## 5. Relationship to live Canon — a scope extension, **not** an independent origin

```
scope_extension_of: samara-making-breaking-grid-ch1
independence: none — same work
```

The live extraction `canon/knowledge/current/samara-making-breaking-grid-ch1` holds chapter 1's
instructional core (*Grid Basics*, *Building a Grid*, *Using a Grid*), 79 objects. Its own
`PROVENANCE.md` states that chapter 2 "is the book's counter-argument and is a separate treatment."
That is this lane's span.

**Same author, same work, same edition, same file.** Nothing here corroborates the live extraction
and nothing here may be counted as a second source agreeing with it. Where chapter 2 qualifies,
complicates or inverts a chapter-1 claim, that is recorded as **the same author qualifying his own
earlier statement** — never as two sources disagreeing. The five substantive qualifications are
listed in `EXTRACTION-NOTES.md` §5.

Chapter 1 material already live was **not re-extracted**: the grid taxonomy, the derivation method,
and the usage judgement of *Using a Grid*. The one live object closest to this lane —
`violation_works_by_scarcity_and_can_be_designed_into_the_structure` — was diffed against every
object here; see `EXTRACTION-NOTES.md` §6 for the near-duplicate check and its result.

## 6. Access basis

The Controller authorised **read-only** use of a copy already present on this machine. The file was
read; nothing was written to it, copied out of it, or redistributed. **Licence status was not
independently verified** — no rights check was performed on this copy, and this lane makes no claim
that its use is licensed beyond the Controller's instruction. Quotation in
`source-knowledge.yaml` is confined to short terminology and single sentences carrying the exact
wording of a rule; the Q&A bank is paraphrase throughout.

## 7. What was produced

| File | Contents |
|---|---|
| `source-knowledge.yaml` | 45 SourceKnowledge objects |
| `source-concept-systems.yaml` | 5 SourceConceptSystems |
| `operational-bindings.yaml` | 7 bindings (5 evaluation, 2 governance; **no** `creative_ir`, **no** `production`) |
| `ontology-mappings.yaml` | 38 terms, 16 relationships, 7 concepts |
| `qa-bank.yaml` | 46 Q&A items |
| `EXTRACTION-NOTES.md` | method, hazards, refusals, self-check results |

## 8. The central hazard, stated up front

`visual_argument_role: source_is_its_own_specimen`. This book argues through page layouts; its
claims are demonstrated by the arrangement of the page in front of the reader. **In an EPUB the page
does not exist**, and in this lane's text route the figures are not even named. 202 figure
references in chapter 2; zero inspected; zero inspectable as pages.

The live chapter-1 audit already recorded this book as `inspected_no_page_available` with
`no_authored_page` as an unrecoverable loss pattern. This lane honours that finding rather than
working around it. Fourteen objects carry `extraction_uncertainty: figure_not_inspected` and two
carry `inferred_from_layout`; several claims that the text gestures at were **left unextracted**
because they exist only in an image. See `EXTRACTION-NOTES.md` §2.
