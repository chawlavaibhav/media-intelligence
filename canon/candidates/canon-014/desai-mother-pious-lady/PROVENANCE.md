# Provenance — Desai, *Mother Pious Lady*

## Source identity

| | |
|---|---|
| Author | Santosh Desai |
| Title | *Mother Pious Lady: Making Sense of Everyday India* |
| Publisher (from the book's own title page) | HarperCollins Publishers India |
| Publisher (from the file's OPF metadata) | **`GAPPAA.ORG` — the real publisher has been overwritten by a redistributor** |
| Date in file | `dc:date opf:event="modification"` 2015-03-08 — a modification date, not a publication date |
| ISBN in file | **none** |
| Format | EPUB, reflowable |
| Edition | **Not established, and not establishable from this copy.** |

The title page image inside the book still reads "HarperCollins Publishers India", and the running
head throughout is "Mother Pious Lady", so the work's identity is not in doubt. What is not
recoverable from this copy is *which edition* it is: the metadata that would say so has been
replaced, there is no ISBN, and the only date is a file modification date.

Because the format is reflowable and every locator in this extraction is an **essay title**, the
missing edition does not affect a single locator. The essays are individually titled, no title
repeats, and the table of contents matches the essays present.

## The copy actually used

Supplied as an attachment to this Claude session by the Controller, who explicitly authorised its
use for CANON-014 and directed that acquisition legitimacy, filename and download origin were not to
be adjudicated. That instruction is followed. The filename carries a `libgen.li` marker and the
metadata carries a different redistributor's mark; both are recorded as facts about the artefact,
neither was treated as a reason to exclude the source, and no replacement copy was sought.

| | |
|---|---|
| File | `8d18d4df-Santosh_Desai__Mother_Pious_Lady__Making_Sense_of_Everyday_India_2015_Harpercollins__libgen.li.epub` |
| SHA-256 | `b0a2fb33bde95c44018e5558c80129d74e4c9b13288be356c29c940fa2e2e305` |
| Size | 532,237 bytes |
| Archive | 177 files, 137 spine items, 33 images |
| Extracted text | ~96,000 words |

**No book bytes and no page images are committed anywhere in this repository.**

## Representation integrity — the material issue

This copy **has been modified by a redistributor**, and the modification reaches inside the author's
prose. Two distinct effects, both established mechanically:

1. **Metadata overwritten.** `dc:publisher` is `GAPPAA.ORG`, and the identifier scheme is
   `GAPPAA.ORG`. The real publisher survives only inside a title-page image.
2. **Text injected.** The string `GAPPAA.ORG` appears at 11 positions. Ten stand alone in front
   matter, the dedication, the contents, section openers and chapter heads, where they are
   obviously not authorial. **One is a complete sentence inside an authorial paragraph of the
   Introduction**, carrying no distinguishing markup and reading as prose:

   > "My effort in this book has been to examine Middle India from within. *This book has been
   > downloaded from gappaa dot org.* I have grown up in a middle class family; …"

All 11 positions were located by string search and enumerated in `visual-evidence-ledger.yaml`. The
injected text was excluded from extraction, and no extracted claim contains redistributor text.

**The residual risk is not the injections that were found.** It is that a redistributor demonstrably
willing to insert a sentence into the author's prose may have made other changes carrying no marker,
which would be undetectable in this copy. That risk is silent and unbounded. It is the reason **no
object in this record rests on a single verbatim sentence**: every object is supported by an argument
Desai develops across a whole essay, which no plausible injection would fabricate.

Apart from the injections, the text is clean. A duplicate-sentence scan over the whole book found no
duplicated sentence above 90 characters, so there is no pull-quote flattening or reading-order
damage, and the prose extracts in order across all 137 spine items.

## Span and completeness

The **whole book** is present: acknowledgements, introduction, all three sections and their nine
chapters, and the essays within them. All 137 spine items were extracted. The essays read as
independently published newspaper columns, which the author's "patchwork quilt" description
corroborates, and each stands alone.

## Page addressability

**No authored page anywhere.** Reflowable EPUB, no page map, no folio. Every locator is an essay
title. **No page number was interpolated.**

## Visual evidence

The visual pass **ran and completed**, and found that there is nothing to inspect: 30 of the 33
images are 700–1,840-byte decorative ornaments repeated at essay openings, and the remaining three
are the cover and two front-matter marks. The book argues about objects — a scooter, a thali, a
matrimonial column — entirely in prose and never reproduces or points at an image of any of them.
No sentence in the book directs the reader to look at anything.

A text-only representation therefore loses **nothing** of this argument. That is a real result and
is recorded as `visual_argument_role: no_visual_argument` with `inspection_state:
inspected_figure_level` — we looked, and there was nothing to see.

## The author's evidence, and its one measurement

Desai is a former advertising agency head and a newspaper columnist writing about a class he belongs
to. Sixteen of the seventeen objects in this record are interpretation, and are typed as
`source_interpretation` where the reading is his rather than the observation.

The **one** exception is a thirty-year content analysis of matrimonial advertisements which he says
he was involved in (`sk_dmpl_0020`, `empirical_within_source`). It is reported with **no** sample
size, sampling frame, publication list, coding scheme, date range, inter-coder check or single
number — every finding is directional. Its most valuable result is a null one: the proportion of
advertisements mentioning caste origin did not change across the window, which runs against the
book's general modernisation narrative.

## Overlap with live Canon

**No work overlap, no author overlap, no publisher overlap** with any of the 19 accepted sources.
This is the corpus's first source on Indian everyday material culture.

Relations recorded in the CANON-014 lineage matrix, none independence-defeating:

- Desai and Parameswaran (`parameswaran-nawabs-nudes-noodles`) both cite Malcolm Gladwell's *Blink*.
  Two sources citing the same third work is not a dependence between them.
- Both write about Indian consumer culture in the same period and both are advertising
  practitioners. That is **subject adjacency, not shared origin**: different works, different
  authors, different publishers, no shared informant, and neither cites the other.
- Desai's descriptor-inflation mechanism and Parameswaran's censorship-driven word substitution look
  superficially similar and are **deliberately not merged**: they run in opposite directions. See
  the caveat on `sk_dmpl_0022`.

## Licence status

**Not independently verified**, and not adjudicated by this task under the Controller's explicit
instruction. Nothing was acquired, purchased, downloaded or redistributed by this worker. Internal
research use only.
