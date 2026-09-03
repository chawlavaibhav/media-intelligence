# PROVENANCE — Susan Sontag, *On Photography*

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon and nothing here may
be described as accepted. This is exploratory, non-merge extraction under
`canon/experimental/book-expansion-qa-v1/`.

---

## 1. Source identity

| Field | Value |
|---|---|
| `source_id` | `sontag-on-photography` |
| ID prefix | `snt` |
| Author | Susan Sontag |
| Title | *On Photography* |
| Copyright | © 1973, 1974, 1977 by Susan Sontag |
| First US publication | Farrar, Straus and Giroux |
| Imprint in this copy | Picador (used by FSG under licence from Pan Books Limited) |
| ISBN (print, as printed in the file) | 0-312-42009-9 · eISBN 9781429957113 |
| Edition used | Picador ebook edition, first eBook edition June 2011 |
| Prior publication | Earlier versions of the essays appeared in *The New York Review of Books* between October 1973 and June 1977 |

**Date matters more for this source than for any other in this run.** The book is of 1973–77. Every
premise it rests on is a premise of that moment, and §6 states what this lane does and does not say
about that.

## 2. Format and pagination — Case 3 (addendum)

**EPUB, reflowable. There are no authored page numbers in this format.**

The extraction text carries the header
`FORMAT: EPUB (reflowable). THERE ARE NO AUTHORED PAGE NUMBERS IN THIS FORMAT.` and locator markers
of the form `<<<SPINE n | FILE OEBPS/… | TITLE …>>>`.

Applied throughout this lane:

- Every locator names the **essay by title** and, because Sontag's essays have no section headings,
  a **short distinguishing phrase** identifying the passage — e.g. `"In Plato's Cave", the passage
  on photographs furnishing evidence`. The addendum requires this: a bare essay title would be too
  coarse for a forty-page essay.
- `provenance.page_start` and `provenance.page_end` are **`null`** on every object.
- Spine numbers appear only as a secondary aid, in parentheses (`spine 5`).
- Audit pattern recorded: **`no_authored_page`**. See `EXTRACTION-NOTES.md`.
- **No page number has been invented anywhere in this lane.**

The book contains no internal "see page N" cross-references, so nothing was left unresolved. Its
endnotes are numbered and were read; where a note carries content it is cited by its number.

## 3. Material available and span extracted

| Item | Value |
|---|---|
| Extraction text | `scratchpad/src/EPUB-On_Photography.epub.txt` |
| SHA-256 (text) | `fa143e43b78c23195bf0eca43ec73b88f42d8fae8f312854344fd7f410d4d8d9` |
| Original file | `/Users/vaibhavchawla/Downloads/Books/On Photography.epub` |
| SHA-256 (epub) | `edd6d37e3f765f5d2892a93c9f9069c0db4c0edf75a82a02b6fa15975298db57` |
| Size (epub) | 210,160 bytes |
| Spine documents carrying text | 12 · total ~338,033 characters |

**Structure.** Six essays plus an anthology of quotations:
*In Plato's Cave* · *America, Seen Through Photographs, Darkly* · *Melancholy Objects* ·
*The Heroism of Vision* · *Photographic Evangels* · *The Image-World* ·
*A Brief Anthology of Quotations*.

**Span read:** the whole book, plus the endnotes and the copyright page.

**Span extracted from:** four essays — *In Plato's Cave*, *Melancholy Objects*,
*The Heroism of Vision* and *The Image-World*.

**Span deliberately not extracted from, and why:**

- ***America, Seen Through Photographs, Darkly*** — refused entire. It is the Whitman essay: a
  literary argument about American cultural self-understanding conducted through Whitman, Walker
  Evans and Diane Arbus. The brief for this lane excludes it and the exclusion is correct — its
  content is a reading of American letters, not of how images are read.
- ***Photographic Evangels*** — refused entire. It is the essay on whether photography is an art,
  conducted through what Stieglitz, Weston, Strand, Adams and Callahan said about themselves. Its
  substance is aesthetic judgement of named photographers and the art-status debate, both of which
  this lane refuses. Read in full before refusing; see `EXTRACTION-NOTES.md`.
- ***A Brief Anthology of Quotations*** — refused. It is an anthology of other people's sentences,
  assembled without commentary. Extracting from it would attribute other authors' claims to this
  source.

**No photograph is reproduced anywhere in this book.** *On Photography* is a book about photographs
that contains none. Every object therefore carries `source_support: text` and
`inspected: {text: true, figures: []}`, and unlike the other sources in this run there is no
`figure_semantic_binding_lost` hazard at all — not because the extraction route recovered the
figures, but because there are none to lose.

## 4. Overlap with live Canon

**None.** `sontag-on-photography` does not appear in `canon/knowledge/current/`, and no live source
in that directory is this work, an edition of it, or a scope extension of it. This is an
**independent origin** and it is **not** a `scope_extension_of` any live source.

**No live neighbour was named for this lane**, and after reading, that is right: nothing in
`canon/knowledge/current/` does what this book does. The photography sources in live Canon
(`freeman-photographers-eye-graphic-guide`, `light-science-magic-ch3`, `alton-painting-with-light-ch2`)
are all about making photographs. This one is about how photographs are read, and it argues that the
two questions are related only distantly.

## 5. Extracted under a standing project warning

This source was extracted under a warning the project had already recorded about it, and the warning
is repeated here rather than paraphrased away.

`canon/experiments/CANON-COVERAGE-MAP-V0.md` records that **Berger and Sontag are "critique, not
craft"**. `canon/planning/CANON-V1-SOURCE-PORTFOLIO.md` extends the same caution to sources of this
kind: *"This is a reading method, not a production method, and admitting it risks importing analysis
the product cannot act on."*

The warning was honoured, not worked around. What that meant in practice is set out in
`EXTRACTION-NOTES.md` §4, and the load-bearing rule was this: **no critical observation in this lane
was converted into production advice.** Sontag's claim that photography beautifies whatever it
records is not guidance to avoid a composition, and it is not recorded as any kind of guidance. The
enforcement is described and the checks are reported.

`EXTRACTION-NOTES.md` §11 gives this lane's own judgement on whether the source earns a place in a
media-production Canon at all. That judgement is not a recommendation and this lane has no authority
to admit anything.

## 6. Historical contingency — what this lane says and does not say

Almost every claim in this book rests on premises of 1977: film, the material scarcity of images,
the family album, the picture magazine, the news photograph as the principal route by which
distant events reached people, and an explicitly Western — mostly American and European — image
culture that the book treats as its subject.

**Two rules were applied and neither was relaxed:**

1. **No claim was updated or modernised.** Every object records what Sontag says, in her frame, at
   her date.
2. **This lane does not assert what has changed since.** Where a premise she relies on is stated,
   the premise is recorded as she states it and the contingency is noted in a caveat carrying
   `origin: extractor_observed`. Those caveats say *what she assumes*; they do not say what is now
   true instead, because this lane has no source for that.

Almost every object accordingly carries `historical_claim`, `culturally_bounded`, or both.

## 7. Access basis and licence

The Controller authorised **read-only** use of an **already-present local copy** of this EPUB at
`/Users/vaibhavchawla/Downloads/Books/On Photography.epub`. Nothing was acquired, downloaded or
redistributed for this task, and no part of the work is reproduced here beyond short quotations
where the exact wording is load-bearing.

**Licence status was not independently verified.** This lane makes no claim about the provenance,
licence or redistribution rights of the local copy. That question is out of scope for the extraction
and is left to the Controller.

## 8. Files in this directory

`PROVENANCE.md` · `source-knowledge.yaml` · `source-concept-systems.yaml` ·
`operational-bindings.yaml` · `ontology-mappings.yaml` · `qa-bank.yaml` · `EXTRACTION-NOTES.md`

Nothing was written outside this directory.
