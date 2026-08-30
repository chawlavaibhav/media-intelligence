# Provenance — Rama Bijapurkar, *We Are Like That Only: Understanding the Logic of Consumer India*

## Source identity

| | |
|---|---|
| Author | Rama Bijapurkar |
| Title | *We Are Like That Only: Understanding the Logic of Consumer India* |
| Edition | **Revised and updated** (the paperback edition) |
| Foreword | C. K. Prahalad |
| Afterword | N. R. Narayana Murthy |
| Publisher | **Portfolio / Penguin** (imprint page: "PORTFOLIO … Penguin Books is part of the Penguin Random House group of companies") |
| First published | "This collection published 2007" |
| Copyright | © Rama Bijapurkar **2007, 2009** |
| Print ISBN | 978-0-143-06597-5 |
| Digital edition | "This digital edition published in 2012." e-ISBN 978-8-184-75001-0 |
| Territory | "For sale in the Indian Subcontinent only" |
| Format | PDF, produced by **calibre 5.34.0** from an ebook |

**Three dates are in play and they are recorded rather than collapsed.** The supplied filename says
2009. The imprint page says the collection was published 2007 and the copyright is 2007, 2009 — the
second date being the revised and updated edition. The digital edition from which this PDF was
converted was published 2012. **The data in the book is 2008**, which the author states in her
Preface: "in this paperback edition … I have updated all the data to 2008." The 2012 digital edition
did not update the data further; nothing in the text refers to anything after 2009.

For the purposes of this record the source is treated as **the 2009 revised edition, with data to
2008**, and every numerical object carries that vintage.

## The copy actually used

Found on the Controller's machine at `~/Downloads/` and authorised by the Controller as a task input
for CANON-014, with an explicit instruction not to adjudicate acquisition provenance. That
instruction is followed. The filename carries a `libgen.li` marker; it is recorded as a fact about
the artefact, it was not treated as a reason to exclude the source, and no replacement copy was
sought.

| | |
|---|---|
| File | `Rama Bijapurkar - We are like that only_ Understanding the Logic of Consumer India (2009, Portfolio) - libgen.li.pdf` |
| SHA-256 | `8c480391db2f37a98802340acb9c253dcaff68b253bc4de116728100a4a53ca7` |
| Size | 3,847,876 bytes |
| Pages | 279 (conversion artefacts — see below) |
| Image objects | 46 |
| Extracted text | ~78,600 words |

**No book bytes and no page images are committed anywhere in this repository.**

## Representation integrity — the material issue

**The prose survived the conversion and the evidence did not.** This is the defining representation
fact about this source and it changes what a text-only extraction of it would have been worth.

The PDF was produced by calibre from an ebook. The running prose extracts cleanly and completely: a
duplicate-sentence scan over the whole text for sentences above 90 characters returned **zero**
duplicates, so there is no pull-quote flattening and no reading-order damage. The book is complete —
Foreword, Preface, all thirteen chapters, Afterword, Bibliography, Acknowledgements, endnotes and
copyright page all present and in order.

But **every table and figure in this copy is an embedded raster image**, and their content therefore
does not appear in the extracted text stream at all. The running text refers to them and reasons from
them without restating them: "Table 5.1 gives a stratification scheme (a special analysis done by
Hansa Research using IRS data)…", "as can be seen in Table 9.2", "Table 5.6 gives an idea of
consumption increase in rural India". A reader of the text alone would meet the assertions and never
meet the evidence, **and would see no sign of the loss**.

**All 30 data figures were therefore opened and read.** At least nine tables were found to carry
content that appears nowhere in the text — including the full urban and rural SEC classification
grids (Tables 7.1 and 7.2), the eight-layer consumption-intensity scheme (Table 5.2), the
liberalisation and values tables (9.1 and 9.2), and the youth-segment profile that substantiates the
book's sampling argument (Table 10.1). Four objects in this record rest partly on tables that could
not have been read from the text. Full detail, including the classification of all 46 image objects
and six claim checks against the tables, is in `visual-evidence-ledger.yaml`.

## Page addressability

**No authored page anywhere in this copy.** Established from the PDF metadata — Creator and Producer
both `calibre (5.34.0)`, page size US Letter (612×792 pt), which is a conversion default and not a
trade paperback trim — and from the text layer, which carries no running folios. The 279 pages are
conversion artefacts.

**No page number was interpolated.** Every locator in `source-knowledge.yaml` is a chapter number,
chapter title and section heading. This is workable for this source because the chapters are
numbered and titled in the book's own contents, the section headings are distinctive and set in
capitals, and no heading repeats. `page_start` and `page_end` are explicitly `null` throughout, which
is the honest representation rather than a gap.

This is the same handling already used on this branch for `desai-mother-pious-lady`,
`pandey-pandeymonium` and `parameswaran-nawabs-nudes-noodles`, all of which are reflowable with no
authored page. It differs from the other two sources added in this pass, both of which have real
printed folios.

## What kind of evidence this book contains — and why it must be sorted

This is the point at which this source is most likely to be mishandled, so it is set out explicitly.

**Bijapurkar draws on three quite different kinds of material and writes all three in the same
confident declarative voice.**

1. **Named third-party survey data**, with sources and years: NCAER's Market Information Survey of
   Households, the Indian Readership Survey via Hansa Research (an all-India sample of 242,118
   households in the 2008 round), the National Sample Survey, IIMS Dataworks, the Census of India,
   the World Bank, Goldman Sachs's BRIC report. This material is properly sourced and, where it
   appears in tables, was checked in this pass.
2. **One original analysis she co-authored**: "Solving the Income Data Puzzle" with Laveesh Bhandari
   (*Businessworld Marketing White Book*, 2006), linking survey income distributions to GDP.
3. **Consulting anecdotes from her own assignments**, told without client name, date, sample size, or
   outcome — the two-wheeler company, the bicycle company, the tractor company, the paint company,
   the gaming company, the glucometer company, the polyurethane manufacturer, the hotel chain.

**The book does not mark the difference. This record does, on every object.** An object resting on
named survey data carries `empirical_within_source` and names the source and year; an object resting
on a consulting story carries `anecdotal` and says so; objects resting on both say which part is
which. The sorting is gathered as `scs_rbwl_003` so that the mixed character of the source is visible
as a whole and not only object by object.

**A consequence worth stating plainly**: several of the book's most quoted arguments rest entirely on
category (3). The change-confluence framework (`sk_rbwl_0110`) is illustrated by two undated,
unattributed cases with no outcomes. The no-frills failure argument (`sk_rbwl_0150`) names no failed
product at all. These are recorded because the mechanisms are clear and useful, and they are caveated
because the evidence is not there.

## The freshness problem

**This is India before the smartphone.** The data are 2008 and earlier. Since publication the market
has acquired mass mobile internet, UPI, and consumer e-commerce at scale — none of which this book
could anticipate, and any of which would change the numbers materially. Several of the business-model
instances the book celebrates were artefacts of a cost structure that has since disappeared: STD/ISD
booths, cyber cafés, community television.

**The author says this herself**, twice, and it is extracted as `sk_rbwl_0180`. In her Preface she
records exactly what she updated; in chapter 5 she raises the objection against herself — "Is a
detailed tour of methodology and numbers from various sources really necessary, particularly if the
data will be outdated as soon as the book is published?" — and answers that the durable contribution
is the framework for reasoning about the numbers, not the numbers.

**This extraction is built on that instruction.** The bindings in `operational-bindings.yaml` bind
reasoning errors and nothing else: no binding carries a number, a segment size, a threshold or a
market fact. Every numerical object is grouped under `scs_rbwl_002` with the author's own vintage
statement, so that no figure can be retrieved without it.

## Two things to be careful about

**The culturalist framing is separable from the mechanism, and the record separates them.** The "this
as well as that" observation (`sk_rbwl_0120`) contains a clean and general account of hybrid
adoption — a bundled practice is adopted by outsourcing the disliked component and retaining the
valued one, which is why the successful entrant unbundles rather than substitutes. It is wrapped in a
framing that treats this as an Indian cultural "DNA" with "high tolerance of ambiguity", evidenced by
avatars in the Hindu pantheon and by Brahmins in Bengal being permitted fish. That framing is
essentialist, is not evidenced, and does no work the mechanism does not already do. The object says
so, and Table 9.2, which sets the framing out as a two-column list of asserted binary contrasts with
no source, is recorded in the visual ledger as the author's summary of her own position rather than
as a finding.

**The author has an interest and the book does not disclose it.** Bijapurkar is a market strategy
consultant, and the book's central argument is that firms need customized market strategy for India.
That is not a disqualification — her disclosure of her own role in creating the middle-class myth she
now attacks is unusually candid, and is recorded as strengthening `sk_rbwl_0040` — but the interest
is real and is noted on `sk_rbwl_0010`.

## Overlap with live Canon

**No work overlap, no author overlap and no publisher overlap** with any of the 19 accepted live
Canon sources.

There is, however, a **real and directional relation with a source already extracted on this
branch**, and it is the clearest inter-candidate relation in the CANON-014 batch:

- Bijapurkar **cites Santosh Desai by name and repeatedly**, and thanks him in her Acknowledgements:
  "Santosh Desai (now managing director of Future Brands, formerly president of McCann Erickson) has
  added a significant dimension to my understanding of changing consumer values and attitudes and
  **has been quoted quite a bit in this book**." Santosh Desai is the author of
  `desai-mother-pious-lady`, already extracted on this branch.
- The specific attributions observed are enumerated in `ontology-mappings.yaml` under
  `t_rbwl_0060`, recorded as an **attribution record rather than as a concept** precisely because the
  party attributed is a separate CANON-014 candidate.
- **The date order matters and is recorded.** This book's first edition is 2007 and this revision
  2009; *Mother Pious Lady* is a 2010 collection of Desai's newspaper columns. Bijapurkar is
  therefore citing Desai's columns and conversations, **not this book** — she cannot be citing a book
  that did not yet exist. The two records share an intellectual source, in one direction, on a subset
  of cultural-observation material.

**No `cross_source_concept` was created and no concept was merged.** The relation is recorded pairwise,
with its direction and its date order, in `canon/findings/CANON-014-CANDIDATE-LINEAGE-MATRIX.yaml`,
where the Controller can weigh it. The extraction's own view, recorded there, is that this is a
**partial, directional dependence on a subset of objects** — Bijapurkar's cultural-observation
material in chapters 8 and 9 — and not a dependence of the book's structural or quantitative
arguments, which come from survey data Desai has no part in.

A second, weaker relation is recorded there too: Bijapurkar and Parameswaran
(`parameswaran-nawabs-nudes-noodles`) both write about Indian consumer culture of overlapping decades
from adjacent professional positions, and both cite C. K. Prahalad. Neither cites the other.

## Licence status

**Not independently verified**, and not adjudicated by this task under the Controller's explicit
instruction. Nothing was acquired, purchased, downloaded or redistributed by this worker. Internal
research use only.
