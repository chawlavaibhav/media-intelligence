# Provenance — Pandey, *Pandeymonium*

## Source identity

| | |
|---|---|
| Author | Piyush Pandey |
| Title | *Pandeymonium: Piyush Pandey on Advertising* |
| Foreword | Amitabh Bachchan (copyright © Amitabh Bachchan 2015) |
| Publisher | **Portfolio, Penguin Books India** — "First published in Portfolio by Penguin Books India 2015" |
| Print ISBN | 978-0-670-08859-1 |
| e-ISBN | 978-9-352-14004-6 |
| ISBN in OPF metadata | 9789352140046 — **matches the e-ISBN** |
| Cover design | Rajiv Rao (credited on the copyright page) |
| Format | EPUB, reflowable |
| Edition | **The publisher's digital edition, 2015.** Established from the book's own copyright page. |

**Note a filename error:** the supplied filename says "2016". The book's copyright page says 2015,
twice. The 2015 date is used throughout this record.

## A first reading that was wrong, and the check that corrected it

The EPUB's internal folders are named `GoogleDoc/`, and the spine files are
`GoogleDoc/Pandeymonium_split_NNN.xhtml`. On first inspection this suggested the file might be a
re-typeset copy rather than a publisher artefact, which would have been a serious provenance problem.

**That reading was wrong.** The check that settled it: the file carries Penguin's complete copyright
page — the imprint, the international office addresses, the first-publication statement, both
copyright lines, the cover-design credit, the publisher's liability disclaimer, the print ISBN, and a
separate digital-edition page whose e-ISBN **matches the ISBN declared in the OPF metadata**. A
re-typeset copy would not reproduce a matching e-ISBN. The folder name is a conversion-tool artefact.

This is recorded rather than quietly dropped because the corrected conclusion — that this is a
publisher file — is load-bearing for admission, and a reviewer should be able to re-run the check.

## The copy actually used

Supplied as an attachment to this Claude session by the Controller, who explicitly authorised its use
for CANON-014 and directed that acquisition legitimacy, filename and download origin were not to be
adjudicated. That instruction is followed. The filename carries a `libgen.li` marker; it is recorded
for completeness, was not treated as a reason to exclude the source, and no replacement was sought.

| | |
|---|---|
| File | `6ac60f43-Piyush_Pandey__Pandeymonium_2016_Penguin_UK__libgen.li.epub` |
| SHA-256 | `866597a98a429adf1ddd0130281d11b783b8d41673c969a5cd685b4ea90456fb` |
| Size | 1,046,663 bytes |
| Archive | 151 files, 138 spine items, 3 images |
| Extracted text | ~58,300 words |

**No book bytes and no page images are committed anywhere in this repository.**

## Span and completeness — checked, not assumed

The **whole book** is present and this was verified mechanically rather than eyeballed. Every one of
the 47 entries in the book's own table of contents was matched against the body text. All 47 resolve,
including chapter 8 "The Indian Advertising Business" and "Afterword: Why I Am Not Starting My Own
Agency". A first case-sensitive pass appeared to show eight absences; all eight turned out to be
formatting differences — part headings set in capitals without their "Part One:" prefix — not missing
content. All 138 spine items carry text and none is empty.

## Representation integrity

One real defect in this copy, established mechanically:

**Pull-quote flattening.** The printed book's pull-quotes have been flattened into the body text, so
each appears twice — once inside its paragraph and once standing alone. A scan for sentences over 90
characters occurring more than once returned **exactly 10, each occurring exactly twice**. The
consequence is specific: a naive extraction could read the pull-quote as a second, separate claim and
double-count it, and any word-frequency or emphasis analysis over this copy is corrupted. All ten were
identified, and where an extracted object quotes one, the duplication is noted on the object.

## Visual evidence — and why its absence is not a defect

The visual pass **ran and completed**. The archive holds three images: the cover, the publisher title
page, and one black-and-white photograph of the author's parents illustrating a memoir passage. Both
non-cover images were opened. None argues anything.

The book discusses campaigns whose evidence is visual — Fevicol, Cadbury Dairy Milk, the Vodafone
Zoozoos, Asian Paints — and reproduces none of them. **That is how the work was published, not a loss
in this copy.** The copyright page states:

> "All images and television commercials mentioned in this book are available for viewing on
> www.pandeymonium.in"

This is the Audit Gate's `source_evidence_never_printed` pattern in its defining form: a reader of the
printed 2015 edition was in exactly the position this extraction is. The named route **could not be
reached in this session** — no external network egress was available, and both a direct request and
the harness fetch tool were refused by the egress proxy for every external host tried — so the
evidence is named, located and unreachable here. No claim in this record rests on it.

**The bound this places on the record:** every claim here about a named campaign is a claim about what
Pandey *says* about it. Nothing in this record describes what any campaign looks like or asserts what
any campaign achieved.

## The author's evidence, and the survivorship structure

This is a practitioner memoir by India's best-known advertising creative director. Its characteristic
form is a story about his own career ending in a lesson, and **the cases are almost uniformly ones
that succeeded**. This is recorded on the objects rather than left for a reader to notice, because it
bounds everything the source can support:

- Campaign outcomes are asserted and never evidenced. No sales, share or tracking figure appears
  anywhere in the book.
- The argument against research procedures rests on named campaigns he says pre-testing *would have*
  killed — counterfactuals about tests that were never run, on work the book does not reproduce.
- The chapter on standing by one's convictions turns on a pitch that was won. Pandey supplies the
  counterfactual himself, noting he "could have been sacked" and that this would have ended his
  career — which is the one place the book counts the other branch.

The source can support statements about what an eminent practitioner believes and recommends, and
about the mechanisms he articulates. It cannot support a claim that a practice causes an outcome.

## Overlap with live Canon

**No work overlap, no author overlap, no publisher overlap** with any of the 19 accepted sources.

Relations recorded in the CANON-014 lineage matrix, none independence-defeating:

- Pandey is **named in passing** by `parameswaran-nawabs-nudes-noodles` as one of several writers who
  continued Hindi-originated copywriting. Under the Audit Gate that is incidental mention, **not**
  `shared_primary_informant`: no load-bearing claim in Parameswaran's book rests on Pandey's own
  account, and Pandey does not cite Parameswaran.
- Both books discuss the same Indian campaigns (Fevicol, Cadbury Dairy Milk, Asian Paints) because
  those campaigns are common property of the industry both worked in. **Shared subject matter is not
  shared origin.**
- The two agree on one point — that a celebrity should be cast as a character rather than presented
  as a star — on independent evidence. That is recorded in the lineage matrix as an **observed
  agreement** and is deliberately **not** promoted to a `cross_source_concept`; no cross-source
  promotion is authorised by CANON-014.

## Licence status

**Not independently verified**, and not adjudicated by this task under the Controller's explicit
instruction. Nothing was acquired, purchased, downloaded or redistributed by this worker. Internal
research use only.
