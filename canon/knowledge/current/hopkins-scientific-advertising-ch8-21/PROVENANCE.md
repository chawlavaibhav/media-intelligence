# Provenance — Claude C. Hopkins, *Scientific Advertising* (1923), chapters 8–21

**EXPERIMENTAL — NOT LIVE CANON.** Produced in the non-merge lane
`canon/experimental/book-expansion-qa-v1/`. Nothing in this directory is accepted Canon, has been
reviewed, or may be described as accepted.

---

## 1. Source identity

| Field | Value |
|---|---|
| `source_id` | `hopkins-scientific-advertising-ch8-21` |
| ID short prefix | `sa8` |
| Work | Claude C. Hopkins, *Scientific Advertising*, first published 1923 |
| Physical copy | Internet Archive scan of the 2009 Snowball Publishing / BN Publishing reprint, 88 PDF pages, 21 chapters |
| Local path | `/Users/vaibhavchawla/Downloads/Books/Scientific Advertising.pdf` |
| SHA-256 | `e081207466c2f8da334bf6bdeba8c454c17107e6ddfe90cbccc0d95e8531b6fc` (re-computed in this lane; matches the fingerprint supplied in the task) |
| Extracted text used | `scratchpad/src/SRC-sciadv-ch8-21.txt`, page-marked `<<<PRINTED_PAGE n \| PDF_PAGE m>>>` |
| Span processed | **Chapters 8–21, printed pages 25–64** (PDF pages 33–72) |
| Page mapping | printed page = PDF page − 8 |
| Extraction date | 2026-08-30 |

## 2. This is a scope extension, not an independent origin

```yaml
scope_extension_of: hopkins-scientific-advertising-ch1-7
independence: none — same work
```

Chapters 1–7 (printed pp. 1–24) are already **live accepted Canon** as
`hopkins-scientific-advertising-ch1-7`. This directory extends the same book into its unprocessed
remainder. **Same work, same author, same 1923 publication, same argument.**

Consequences that bind every object here:

- **No object in this directory may be counted as an independent origin against
  `hopkins_scientific_advertising_ch1_7`.** Under SPEC-05 §Governance 5 the dependence relation is
  stronger than `shared_author` — it is the *same volume*. Any future promotion attempt that treats
  ch1–7 and ch8–21 as two agreeing sources would report one author's single book as corroborated by
  itself.
- No `xs_` cross-source concept is created here. None is permitted in this task.
- Where chapters 8–21 restate a doctrine already captured from chapters 1–7, no duplicate object was
  created. Where a later chapter genuinely **extends, qualifies or supplies evidence for** a live
  object, the object was created and its `caveats` name the live `sk_` id it extends. Six objects
  carry such a caveat; they are listed in `EXTRACTION-NOTES.md` §5.

### The live gap this lane was built to close

The live `PROVENANCE.md` for chapters 1–7 records an explicit unresolved gap: chapter 15,
"Test Campaigns", was not processed, and whether it reports measurements chapters 1–7 do not was
recorded as **NOT VERIFIED**. Chapter 15 falls inside this span and has now been read in full.
The finding is stated in `EXTRACTION-NOTES.md` §3. It is a finding, not a promotion; the live
record is not touched.

## 3. Exact material available

Printed pages 25–64 are continuous body text, one column per page, running header and page-number
footer. Confirmed chapter starts, read off the text and cross-checked against the PDF rather than
taken from the task brief:

| Ch | Title | Printed pages |
|---|---|---|
| 8 | Tell Your Full Story | 25–27 |
| 9 | Art in Advertising | 28–30 |
| 10 | Things Too Costly | 31–33 |
| 11 | Information | 34–36 |
| 12 | Strategy | 37–39 |
| 13 | Use of Samples | 40–43 |
| 14 | Getting Distribution | 44–46 |
| 15 | Test Campaigns | 47–50 |
| 16 | Leaning on Dealers | 51–52 |
| 17 | Individuality | 53–54 |
| 18 | Negative Advertising | 55–56 |
| 19 | Letter Writing | 57–59 |
| 20 | A Name That Helps | 60–61 |
| 21 | Good Business | 62–64 |

Printed pages 65–66 are blank; 67 is the reprint publisher's "Recommended Readings" page (W. D. Gann
titles, Earl Nightingale, `snowballpublishing.com`) — **2009 reprint matter, not Hopkins, and not
extracted**; 68 is a blank verso whose text layer is scanner noise.

## 4. Integrity checks performed in this lane

| Check | Result |
|---|---|
| SHA-256 of the PDF | Recomputed; matches the supplied fingerprint exactly. |
| Supplied text vs PDF | `pdftotext` re-run on PDF pages 39, 41, 49, 53, 57, 63, 64, 70 (printed 31, 33, 41, 45, 49, 55, 56, 62). Byte-for-byte agreement with the supplied extract on every one. |
| Page mapping | Verified at eight independent points across the span; printed = PDF − 8 holds throughout. |
| Chapter inventory | All 14 chapter headings for this span present, in order, none displaced. |
| OCR quality | Body text is clean. **No body-text corruption was found anywhere in printed pp. 25–64.** |
| Where OCR does fail | Italic page-number footers only, exactly as the live ch1–7 record found: `Pf` (p.27), `752]` (p.29), `2/7` (p.37), `28)` (p.53), `oo` (p.55), `nye` (p.57), `he` (p.59), and a stray `©` in the first line of p.28. None touches a word of Hopkins's text. |
| Numbers re-read from the PDF | $20–$25 per tooth-brush convert (p.31); one in a hundred / one in five (p.33); 50 cents, 15 cents, 40 cents to $1, 1,460,000 requests, one-fifth of coupons (p.41); 70 cents vs 18–22 cents, 70 per cent by telephone (p.42); $1,000 per test, 91 per cent, fifty plans in five years, 75 per cent (p.49); four to one (p.55); $700,000, 30 per cent vs 150 per cent (p.62). All match. |

`extraction_uncertainty: ocr_degraded` is therefore used on **zero** objects. This was verified, not
assumed.

## 5. Visual evidence

**There is none, and that is a finding rather than a gap in inspection.** Printed pages 25–64 contain
zero figures, illustrations, plates, tables, diagrams or reproduced advertisements. No object here is
recorded as `visually_demonstrated`; every `source_support` value is `text`; every
`provenance.inspected.figures` is empty.

The audit pattern the live record names **`source_evidence_never_printed` applies with full force to
this span** and is arguably worse here than in chapters 1–7. Hopkins argues from Arrow Collar
advertisements, Mead-style mail order advertisements, Puffed Grains pictures of the grains, the
incubator advertisement, Marmon's columns of copy, coupon advertisements carrying full-package
offers, "before and after taking" advertisements, and a positive/negative pair he says outpulls four
to one. **Not one is reproduced.** In chapter 9 he goes further and instructs the reader to *look at*
mail order advertisements to see how pictures are used — an instruction the book itself makes
impossible to follow.

This is not digitisation loss. A reader holding the 1923 first edition was in exactly the position we
are in. No better scan repairs it, and the caution name `figure_semantic_binding_lost` is **not**
applicable, because nothing was lost — nothing was ever printed.

## 6. Access basis

The underlying text is **Claude C. Hopkins, *Scientific Advertising*, published 1923**. Works
published in the United States in 1923 entered the US public domain on 1 January 2019. The 1923 text
— which is the only thing extracted here — is therefore public domain in the United States.

Recorded honestly, because the physical file does not say so on its face: **the local copy is a 2009
Snowball / BN Publishing reprint and carries its own "All rights reserved" notice.** That notice
attaches to whatever the reprint added — cover, typesetting, the publisher's "Recommended Readings"
page — and not to Hopkins's 1923 text. This lane extracted only Hopkins's text and deliberately
excluded the reprint's own matter (see §3). Use here is read-only, local and internal to a research
task; no page render and no source text is committed.

## 7. What was produced

48 SourceKnowledge objects · 4 SourceConceptSystems · 41 ontology terms · 14 relationships
(including 4 `distinct_from`) · 5 source-specific concepts · 1 canonical concept · 11 operational
bindings · 54 Q&A pairs.

All YAML parses. All bindings resolve inside this lane. Self-check results are in
`EXTRACTION-NOTES.md` §7.

## 8. Method note carried into every object

Identical in spirit to the live record, and repeated here because it governs how this whole
directory reads. The source describes itself as scientific, exact, proved and law-governed. Those
descriptions are recorded as **the source's claims**. Each object's `evidence.characteristics`
record what the source actually supplies for the claim in question.

- `empirical_within_source` is used **only** where Hopkins reports what a measurement returned.
- `outcome_claimed` is used where a result is asserted without controls.
- Where he asserts that measurement was performed and then withholds the return, the caveat says
  **"measurement asserted, result withheld"** in those words, with `origin: extractor_observed`.

Nothing was upgraded to look better and nothing was dismissed to look sceptical.
