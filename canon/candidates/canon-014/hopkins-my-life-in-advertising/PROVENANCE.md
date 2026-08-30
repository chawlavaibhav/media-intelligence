# PROVENANCE — Claude C. Hopkins, *My Life in Advertising* (1927)

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory has been reviewed, accepted, or
promoted. It is exploratory extraction produced under
`canon/experimental/book-expansion-qa-v1/SCHEMA-CONTRACT.md` and must never be described as
accepted Canon.

---

## 1. Source identity

| Field | Value |
|---|---|
| `source_id` | `hopkins-my-life-in-advertising` |
| ID prefix | `mla` |
| Author | Claude C. Hopkins (1866–1932) |
| Title | *My Life in Advertising* |
| Publisher | Harper & Brothers, New York |
| Year | 1927 |
| Edition | First edition |
| Local copy | Internet Archive scan, 232 PDF pages |
| Local path | `/Users/vaibhavchawla/Downloads/Books/My Life in Advertising.pdf` |
| SHA-256 | `7842a0944d315a37fcf8a054f6141a16935ee3322bbc062afbfba8d6fac53e5f` |
| Extracted text | `scratchpad/src/SRC-mylife.txt` (page markers `<<<PRINTED_PAGE n \| PDF_PAGE m>>>`) |

## 2. Access basis

The work was published in 1927 and is in the public domain in the United States; the US copyright
term for 1927 publications expired on 1 January 2023. Hopkins died in 1932, so the work is also
public domain in life-plus-70 jurisdictions. The local copy is an Internet Archive scan. No
licensed or restricted material is involved.

Notwithstanding public-domain status, this extraction is overwhelmingly paraphrase. Verbatim
strings are confined to short source terminology in `source_terms` and to phrases where the exact
wording is load-bearing.

## 3. Material available and span processed

**Whole book processed.** 19 chapters. Printed body pages 1–206; the text ends "THE END" on
printed p. 206, and printed pp. 207–210 are publisher advertisements for other Harper business
books (no Hopkins content). **No locator in this extraction cites a page above 206.**

Page mapping: **printed page = PDF page − 14.** All locators in every file in this directory use
**printed** page numbers.

| Ch | Title | Printed pp. | Extraction weight |
|---|---|---|---|
| 1 | Early Influences | 1–14 | light — mostly biography; 3 method items |
| 2 | Lessons in Advertising and Selling | 15–26 | medium — how he learned what he learned |
| 3 | My Start in Business | 27–36 | **none** — pure biography |
| 4 | How I Got My Start in Advertising | 37–49 | heavy — dealer-privilege mechanism |
| 5 | Larger Fields | 50–62 | light — one demonstration mechanism |
| 6 | Personal Salesmanship | 63–72 | heavy — service-not-selfishness doctrine |
| 7 | Medical Advertising | 73–85 | heavy — self-repudiation; Schlitz; guaranty |
| 8 | My Liquozone Experience | 86–95 | heavy — the one clean test-then-scale record |
| 9 | The Start of My Seventeen Years… | 96–108 | heavy — Van Camp; coupon distribution |
| 10 | Automobile Advertising | 109–122 | heavy — Mitchell failure; naming; crowd trend |
| 11 | Tire Advertising | 123–130 | heavy — naming; sell-twice doctrine |
| 12 | Early History of Palmolive | 131–142 | heavy — "We Will Buy" introduction |
| 13 | Puffed Grains and Quaker Oats | 143–150 | heavy — habit-change failure; sample pricing |
| 14 | Pepsodent | 151–156 | heavy — the free-offer boundary condition |
| 15 | Some Mail-Order Experiences | 157–166 | heavy — cost-per-reply figures; margin claim |
| 16 | Reasons for Success | 167–174 | heavy — explicit statement of method |
| 17 | Scientific Advertising | 175–188 | heaviest — the explicit principle inventory |
| 18 | My Great Mistake | 189–198 | heavy — account-loss dynamic; distribution |
| 19 | Some Things Personal | 199–206 | light — 1 scope claim; rest is biography |

## 4. Overlap with live Canon — **`shared_author` dependence**

`hopkins-scientific-advertising-ch1-7` is an **accepted live Canon source**. It is
*Scientific Advertising* (1923), chapters 1–7, by **the same author as this source**.

**This source is NOT an independent origin against `hopkins-scientific-advertising-ch1-7`.**

Under SPEC-05 §Governance rule 5 and the Audit Gate, `shared_author` is a **dependence relation**.
Two Hopkins books are one man's position stated twice, four years and one career apart. The
dependence is stronger than bibliography alone would suggest:

- **Chapter 17 of this book is literally about that book.** It opens by naming *Scientific
  Advertising* as the work through which his name became associated with the phrase (printed
  p. 175) and then restates its doctrine in condensed form across pp. 175–188.
- Hopkins states at printed p. 170 that Lasker paid him $10,000 for writing *Scientific
  Advertising*, and at p. 169 that he "wrote numerous books to set down the agency principles."
  The two works share not only an author but a single institutional programme.
- Load-bearing claims recur near-verbatim across the two works: keyed returns as the basis of
  principle, salesmanship-in-print, specific figures over superlatives, service over selfishness,
  and the treatment of mail order as the exact case.

**Consequences, binding on any downstream reader of this directory:**

1. Agreement between this source and `hopkins-scientific-advertising-ch1-7` is **not** cross-source
   convergence and must never be counted, displayed, or aggregated as such.
2. No `cross_source_concept` (`xs_…`) may be built from this pair. None is created here — no `xs_`
   identifier exists anywhere in this directory.
3. The pair carries `not_independent_of_named_sources` in spirit; a formal audit record is the
   Controller's to write, not this lane's.
4. Independence is pairwise. Nothing here says this source is non-independent of *other* corpus
   sources; that is a separate, unperformed determination.

A separate experimental lane is extracting *Scientific Advertising* chapters 8–21
(`hopkins-scientific-advertising-ch8-21`). **This lane did not coordinate with it and asserts no
agreement with it.** Since that source is also Hopkins, the same `shared_author` dependence applies
to that pair a fortiori. Neutral observations for later human review are recorded in
`EXTRACTION-NOTES.md` under "Observations for cross-source review (NOT promotions)".

## 5. Fingerprint of the working text

- `SRC-mylife.txt` — 9,006 lines, 288,156 bytes, 209 page markers.
- Spot-verified against the PDF with `pdftotext` at printed pp. 92, 93, 104, 147, 154, 158. All six
  matched the extracted text at the level of the figures and phrasing relied on. No OCR-induced
  numeric corruption was found in the figures this extraction cites.

## 6. Visual evidence

**The book contains no figures, plates, diagrams, or reproduced advertisements.** It argues
entirely in prose. Every SourceKnowledge object therefore carries `source_support: text`,
`figure_refs: []`, and `inspected.figures: []`. No claim anywhere in this directory is recorded as
`visually_demonstrated`. No `figure_semantic_binding_lost` caution arises.

## 7. What was deliberately not extracted

Biography, career narrative, family, religion, self-description of work habits, and motivational
prose — the majority of chapters 1, 3, 5, 18 and 19 by page count. See `EXTRACTION-NOTES.md` §3.
