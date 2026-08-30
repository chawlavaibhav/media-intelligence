# PROVENANCE — Seth Godin, *This Is Marketing*

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon, and nothing here
may be described as accepted. This is exploratory, non-merge extraction under
`canon/experimental/book-expansion-qa-v1/`.

---

## 1. Source identity

| Field | Value |
|---|---|
| `source_id` | `godin-this-is-marketing` |
| ID prefix | `god` |
| Author | Seth Godin |
| Title | *This Is Marketing: You Can't Be Seen Until You Learn to See* |
| Publisher | Portfolio / Penguin (Penguin Random House LLC), New York |
| Copyright | © 2018 by Seth Godin |
| LCCN | 2018041567 (print) · 2018042423 (ebook) |
| ISBN | 9780525540847 (ebook) · 9780525540830 (hardcover) |
| Edition used | EPUB ebook edition (the ISBN present in the file's copyright page is the ebook one) |

## 2. Format and pagination — Case 3 (addendum)

**EPUB, reflowable. There are no authored page numbers in this format.**

The extraction text carries the header
`FORMAT: EPUB (reflowable). THERE ARE NO AUTHORED PAGE NUMBERS IN THIS FORMAT.` and locator markers
of the form `<<<SPINE n | FILE OEBPS/xhtml/… | TITLE …>>>`.

Consequences, applied throughout this lane:

- Every locator names the **chapter number and title**, plus the **section heading** Godin himself
  prints in bold within the chapter (e.g. `Ch. 4 "The Smallest Viable Market", section "Forcing a
  focus"`). Godin's section headings are dense — usually one every few hundred words — so they give
  a genuinely fine locator without any page.
- `provenance.page_start` and `provenance.page_end` are **`null`** on every object.
- Spine numbers appear only as a secondary aid, in parentheses (`spine 11`). They are file
  positions, not pages.
- Audit pattern recorded: **`no_authored_page`**. See `EXTRACTION-NOTES.md`.
- **No page number has been invented anywhere in this lane.**

The book contains no internal "see page N" cross-references that would need resolving. It does
contain several references to figures/graphs (the Rogers curve, the long tail, the status quadrant
grids, the customer-contribution bar chart, the Gartner Hype Cycle). Those images are **not present
as inspectable images** in the extracted text — only their captions and the surrounding prose.
Every object in this lane therefore carries `source_support: text` and
`inspected: {text: true, figures: []}`. Where a diagram carries meaning the text alone does not,
this is recorded in `EXTRACTION-NOTES.md` under `figure_semantic_binding_lost`.

## 3. Material available and span extracted

| Item | Value |
|---|---|
| Extraction text | `scratchpad/src/EPUB-This_Is_Marketing.epub.txt` |
| SHA-256 (text) | `dd2f1569ec7a717139776ce3a6337ce0d62a0f163fedf7acc30cbac421beda2e` |
| Original file | `/Users/vaibhavchawla/Downloads/Books/This Is Marketing.epub` |
| SHA-256 (epub) | `c8f464e184f1903923462c5a0820f031d83d87f9ba9fb7f54ce67146e7303c1b` |
| Size (epub) | 2,377,250 bytes |
| Spine documents carrying text | 34 · total ~328,396 characters |

**Span read:** the whole book — Author's Note through Chapter Twenty-Three, plus
"A Simple Marketing Worksheet". Front matter, the reading list, acknowledgments, index and
"About the Author" were skimmed for identity only and not extracted from.

**Span extracted from:** Author's Note and Chapters One to Nineteen, plus the worksheet.

Two later chapters contributed to objects whose primary anchor is earlier in the book, and are
listed here so the span is not overstated. **Chapter Twenty** ("Organizing and Leading a Tribe")
supplies the half-life claim about unmaintained tribal behaviour and the Ziglar case of crossing a
local chasm by persistence, both of which support `sk_god_0025`. **Chapter Twenty-One** ("Some Case
Studies Using the Method") supplies the Tesla case, which supports `sk_god_0021`, and the NRA case,
which supports `sk_god_0003`; in both instances the case is used as evidence for a claim stated
elsewhere and no object is anchored there. **Chapters Twenty-Two and Twenty-Three** yielded nothing
extractable. See `EXTRACTION-NOTES.md` §"What was deliberately not extracted".

## 4. Overlap with live Canon

**None.** `godin-this-is-marketing` does not appear in `canon/knowledge/current/`, and no live
source in that directory is this work, an edition of it, or a scope-extension of it. This is an
**independent origin** in the bibliographic sense, and it is **not** a `scope_extension_of` any
live source.

**Nearest live neighbour, read before extracting:**
`canon/knowledge/current/miller-storybrand-sb7/source-knowledge.yaml` — Donald Miller,
*Building a StoryBrand*, ch. 1–3. Both are 2010s US trade-press positioning frameworks. The live
Miller extraction holds message-**structure** knowledge (survival relevance, processing cost, the
seven-element framework, hero/guide, the grunt test, the BrandScript). Godin's transferable core is
audience **selection and exclusion**, and the status/affiliation machinery underneath choice.

Reading the neighbour changed this extraction in two ways, both recorded in `EXTRACTION-NOTES.md`:
material that would merely have restated Miller in Godin's words was refused, and **no
relationship, equivalence or agreement between the two is asserted anywhere in this lane's YAML.**
Cross-source promotion is forbidden in this task; the comparison lives in prose only, and is an
observation about what to extract, not a claim about the world.

## 5. Access basis and licence

The Controller authorised **read-only** use of an **already-present local copy** of this EPUB at
`/Users/vaibhavchawla/Downloads/Books/This Is Marketing.epub`. Nothing was acquired, downloaded or
redistributed for this task, and no part of the work is reproduced here beyond short terminology
quotations where the exact wording is load-bearing.

**Licence status was not independently verified.** This lane makes no claim about the provenance,
licence or redistribution rights of the local copy. That question is out of scope for the
extraction and is left to the Controller.

## 6. Files in this directory

`PROVENANCE.md` · `source-knowledge.yaml` · `source-concept-systems.yaml` ·
`operational-bindings.yaml` · `ontology-mappings.yaml` · `qa-bank.yaml` · `EXTRACTION-NOTES.md`

Nothing was written outside this directory.
