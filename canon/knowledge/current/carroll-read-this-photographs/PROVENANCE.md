# PROVENANCE — Henry Carroll, *Read This If You Want to Take Great Photographs*

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon and nothing here may
be described as accepted. This is exploratory, non-merge extraction under
`canon/experimental/book-expansion-qa-v1/`.

---

## 1. Source identity

| Field | Value |
|---|---|
| `source_id` | `carroll-read-this-photographs` |
| ID prefix | `crl` |
| Author | Henry Carroll |
| Title | *Read This If You Want to Take Great Photographs* |
| Publisher | Laurence King Publishing Ltd, London |
| First published | 2014 · © text 2014 Henry Carroll |
| ISBN (print, as printed in the file) | 978-1-78067-335-6 |
| Design / picture research | The Urban Ant (design) · Peter Kent (picture research) |
| Edition used | EPUB, derived from the 2014 Laurence King edition |

## 2. Format and pagination — Case 3 (addendum)

**EPUB, reflowable. There are no authored page numbers in this format.**

The extraction text carries the header
`FORMAT: EPUB (reflowable). THERE ARE NO AUTHORED PAGE NUMBERS IN THIS FORMAT.` and locator markers
of the form `<<<SPINE n | FILE OEBPS/… | TITLE …>>>`.

Applied throughout this lane:

- Every locator names the **spread title** Carroll gives the section (e.g. `Ch. "Shallow depth of
  field"`), plus the sub-heading he prints under it (e.g. `sub-heading "Stand out by being
  shallow"`). The book is built as sixty-one short titled spreads, so this is a genuinely fine
  locator without any page.
- `provenance.page_start` and `provenance.page_end` are **`null`** on every object.
- Spine numbers appear only as a secondary aid, in parentheses (`spine 26`). They are file
  positions, not pages.
- Audit pattern recorded: **`no_authored_page`**. See `EXTRACTION-NOTES.md`.
- **No page number has been invented anywhere in this lane.**

### A live trap in this particular file: `false_page_affordance`

This EPUB **does** contain page numbers — but they are the *print* edition's, and they cannot be
resolved to any location in this reflowable copy:

- Every spread carries a "For other examples:" list of the form `Alkan Hassan p. 21`.
- Body text cross-references pages directly: *"Look at the Ansel Adams image on page 8"*,
  *"turn back to pages 10, 16 and 22"*, *"see p. 32"*, *"increasing your ISO (p. 50–4)"*.
- The Index and the Credits list printed page numbers throughout.

None of these is usable. The EPUB has no page anchors, so `p. 21` names a page that does not exist
in the copy read. **Every one of these references was left unresolved and none was used as a
locator.** This is recorded in `EXTRACTION-NOTES.md` as `false_page_affordance` alongside
`no_authored_page`, because a file that *looks* paginated is exactly the condition under which an
extractor invents a page.

## 3. Material available and span extracted

| Item | Value |
|---|---|
| Extraction text | `scratchpad/src/EPUB-Read_This_If_You_Want_to_Take_Gr.txt` |
| SHA-256 (text) | `9238f191aec5ab1b752b6623e3b71c803e448007dd37d4e70af021dc655e5ca0` |
| Original file | `/Users/vaibhavchawla/Downloads/Books/Read This If You Want to Take Great Photographs.epub` |
| SHA-256 (epub) | `c0a69021c14f2852c0235851ff7b45cf15676d25e6237144627f6e1936faa60a` |
| Size (epub) | 5,142,000 bytes |
| Spine documents carrying text | 66 · **total 92,763 characters** |

**Span read:** the whole book — Contents through the Index and Credits. Every one of the sixty-one
titled spreads was read in full, plus the Introduction, the five section openers
(Composition · Exposure · Light · Lenses · Seeing) and the Troubleshooting appendix.

**Span extracted from:** the sixty-one spreads, the section openers and Troubleshooting.
Copyright page, Contents, Index, Credits and Acknowledgements were read for identity only.

**This is a very small book.** 92,763 characters of text — roughly a quarter the length of the other
two sources in this lane group, and the text is subordinate to the photographs. Thirty
SourceKnowledge objects were taken from sixty-one spreads: an extraction rate of under one object
per two spreads, which is the honest rate for a book whose method is *show a famous photograph,
explain what the photographer did*. See `EXTRACTION-NOTES.md` §"What was deliberately not
extracted" for the spreads that yielded nothing.

## 4. Overlap with live Canon

**None in the bibliographic sense.** `carroll-read-this-photographs` does not appear in
`canon/knowledge/current/`, and no live source in that directory is this work, an edition of it, or
a scope extension of it. This is an **independent origin**, and it is **not** a `scope_extension_of`
any live source.

**Nearest live neighbour, read before extracting:**
`canon/knowledge/current/freeman-photographers-eye-graphic-guide/source-knowledge.yaml` — Michael
Freeman, *The Photographer's Eye*. Freeman occupies the same territory: the frame and its edges,
subject placement, division, symmetry, tonal weight, frame proportion.

Reading the neighbour changed this extraction in two concrete ways, and both are recorded in
`EXTRACTION-NOTES.md` §"Genuine addition versus restatement":

1. **One candidate was refused as restatement.** Carroll's "Landscape or portrait" spread — match
   the format of the picture to the dominant lines of the subject — is a single-sentence rule with
   an asserted eye-movement mechanism. The live Freeman extraction already holds frame shape and
   proportion in far more differentiated form. Recording Carroll's version would have added a
   thinner statement of material the corpus already has, so it was not extracted.
2. **Several were kept precisely because they are *not* Freeman.** Carroll's contribution is the
   *decision under time pressure* — what the photographer must have settled before the moment
   arrives, and how to judge the result afterwards — plus exposure and light as expressive choices,
   which Freeman's graphic-guide material does not cover in the live span.

**No relationship, equivalence or agreement between Carroll and Freeman is asserted anywhere in this
lane's YAML.** Cross-source promotion is forbidden in this task. The comparison above lives in prose
only, it is an **observation about what to extract**, and it is not a claim about the world.

## 5. Access basis and licence

The Controller authorised **read-only** use of an **already-present local copy** of this EPUB at
`/Users/vaibhavchawla/Downloads/Books/Read This If You Want to Take Great Photographs.epub`. Nothing
was acquired, downloaded or redistributed for this task, and no part of the work is reproduced here
beyond short terminology quotations where the exact wording is load-bearing.

**Licence status was not independently verified.** This lane makes no claim about the provenance,
licence or redistribution rights of the local copy. That question is out of scope for the extraction
and is left to the Controller.

## 6. The photographs

The book reproduces about fifty photographs by fifty named photographers, and they are the book's
argument. **None was inspected.** The extraction route is text only: the EPUB text stream carries
the captions (title, photographer, year) and the prose, and no image was opened, decoded or
described. Every object therefore carries `source_support: text` and
`inspected: {text: true, figures: []}`.

Where a claim's only support in the book is a reproduced photograph, the object carries
`extraction_uncertainty: figure_not_inspected` and **the visual claim was not reconstructed from the
text**. The proportion is reported in `EXTRACTION-NOTES.md` under the caution name
`figure_semantic_binding_lost`.

## 7. Files in this directory

`PROVENANCE.md` · `source-knowledge.yaml` · `source-concept-systems.yaml` ·
`operational-bindings.yaml` · `ontology-mappings.yaml` · `qa-bank.yaml` · `EXTRACTION-NOTES.md`

Nothing was written outside this directory.
