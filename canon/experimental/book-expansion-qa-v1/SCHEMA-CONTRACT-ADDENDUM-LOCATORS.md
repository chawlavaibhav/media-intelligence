# Addendum to `SCHEMA-CONTRACT.md` — locators by source format

Added when the run expanded from 4 sources to the full local library. Everything in
`SCHEMA-CONTRACT.md` still applies unchanged; this only settles **how to cite** each format, because
the corpus now contains three different page situations and getting them confused would put invented
page numbers into the Q&A banks.

**The governing rule is unchanged and absolute: never invent a locator.**

---

## The three cases

### Case 1 — PDF with a verified authored folio

Your source text file begins with a line like:

```
PAGE MAPPING DETECTED: printed page = PDF page - 13 (folio agreement on 193 pages).
USE THE PRINTED NUMBER IN LOCATORS.
```

Markers look like `<<<PRINTED_PAGE 47 | PDF_PAGE 60>>>`.

- **Cite the printed number**: `printed p. 47`, or `printed pp. 47-49`.
- Set `provenance.page_start` / `page_end` to the **printed** numbers.
- The offset was *detected* from the folios actually present on the pages, not assumed. If you find
  a page where the printed folio disagrees with the marker, say so in `EXTRACTION-NOTES.md` and
  trust the folio you can see.

### Case 2 — PDF with NO verified folio

The header says `PAGE MAPPING: **NOT ESTABLISHED**` and markers look like `<<<PDF_PAGE 60>>>`.

- **Cite `PDF page 60`, explicitly using that phrase.** Never write `p. 60` — that would present a
  file offset as an authored page.
- Set `provenance.page_start` / `page_end` to `null` and put `PDF page 60` in `provenance.section`.
- Record the audit pattern `false_page_affordance` in `EXTRACTION-NOTES.md` if the file *looks* like
  it has authored pages and does not.

### Case 3 — EPUB (reflowable): there is no page at all

The header says `FORMAT: EPUB (reflowable). THERE ARE NO AUTHORED PAGE NUMBERS IN THIS FORMAT.`
Markers look like `<<<SPINE 12 | FILE OEBPS/ch04.xhtml | TITLE Applying the Theory>>>`.

- **Cite the chapter and section by name**, e.g.
  `Ch. 4 "Applying the Theory", section "Metal"` or `Ch. 2 "Breaking the Grid", opening argument`.
- You may add the spine marker as a secondary aid: `(spine 12)`. It is a file position, not a page.
- Set `provenance.page_start` / `page_end` to `null`; put the chapter/section in
  `provenance.chapter` / `provenance.section`.
- **Record the audit pattern `no_authored_page`** in `EXTRACTION-NOTES.md`. This is not a defect in
  the extraction — the format simply has no page, and it is unfixable in this copy. The Canon audit
  vocabulary already has a name for it.
- Where the book's own text cross-references a page number ("see page 143"), that reference is
  **unresolvable in this copy**. Do not resolve it by guessing. Note it.

### Case 4 — no pagination at all (web sources)

WCAG 2.2 and the Google ABCD pages. Cite the Success Criterion number, glossary term, or page plus
section heading. `page_start`/`page_end` are `null`.

---

## Consequence for the Q&A banks

`source_locator` must be **specific enough that a reader can find the supporting text**. A locator
of `Chapter 4` for a forty-page chapter is too coarse — name the section, the sub-heading, or the
worked example. If the source's own structure gives you nothing finer than a chapter, say the
chapter and add a short distinguishing phrase (e.g. `Ch. 7, the discussion of glass and liquids`).

The validator enforces:
- pageless sources must not carry `p.`-style page locators;
- page-bearing sources must have every cited page inside the book's real span;
- every locator is non-empty.

---

## Scope-extension sources — what is already live

Three lanes extend a work already in live Canon. **Do not re-extract the live span.** State
`scope_extension_of: <live source_id>` in `PROVENANCE.md`, and record that the extension is **not an
independent origin** against the live source — it is the same work.

| Lane | Live span (do NOT re-extract) | Your span |
|---|---|---|
| `hopkins-scientific-advertising-ch8-21` | ch. 1–7, printed pp. 1–24 | ch. 8–21, printed pp. 25–64 |
| `light-science-magic-beyond-ch3` | ch. 3 complete, "The Management of Reflection and the Family of Angles" | the chapters that **apply** that theory to specific surface classes and product cases |
| `samara-making-breaking-grid-ch2` | ch. 1 parts *Grid Basics* / *Building a Grid* / *Using a Grid*, printed pp. 20–76 | ch. 2 "Breaking the Grid" — the book's own counter-argument |

Where a later span **contradicts or qualifies** the live span, that is valuable and must be recorded
faithfully as the same author's own qualification of their own earlier claim. It is **not**
cross-source disagreement, and it must never be presented as two sources disagreeing.
