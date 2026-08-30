# PROVENANCE — `ogilvy-beyond-ch2`

**EXPERIMENTAL — NOT LIVE CANON.** Lane of the non-merge run `book-expansion-qa-v1`. Nothing in
this directory is accepted Canon and nothing here may be described as accepted.

---

## 1. Source identity

| Field | Value |
|---|---|
| Work | David Ogilvy, *Ogilvy on Advertising* |
| First published | 1983 (Pan Books Ltd. and Orbis Publishing Ltd., United Kingdom; Crown Publishers, United States) |
| Copy used | Vintage Books ebook, first Vintage edition March 1985; text copyright 1983 David Ogilvy, compilation copyright 1983 Multimedia Books Ltd. |
| ISBN of the copy | print 0-394-72903-X; eBook 978-0-8041-7005-5 |
| Format | **EPUB, reflowable** |
| `source_id` | `ogilvy-beyond-ch2` |
| ID prefix | `ogx` |

Original file: `/Users/vaibhavchawla/Downloads/Books/Ogilvy on Advertising.epub`
Working text extract used for this lane:
`.../scratchpad/src/EPUB-ogilvy-on-advertising.txt` — 26 spine documents carrying text,
415,904 characters, header stating `FORMAT: EPUB (reflowable). THERE ARE NO AUTHORED PAGE NUMBERS
IN THIS FORMAT.`

---

## 2. Scope extension — this is the same work as a live Canon source

```
scope_extension_of: ogilvy-ch2-advertising-that-sells
independence: none — same work
```

Chapter 2, "How to produce advertising that sells", is already live accepted Canon as
`ogilvy-ch2-advertising-that-sells` (source_id `ogilvy_on_advertising_ch2`, 22 SourceKnowledge
objects, audit record `aud_ogilvy_ch2`, `audit_status: complete`).

**This lane is NOT an independent origin against it.** It is the rest of the same book by the same
author in the same year. No `cross_source_concept` is created here, and no relation in this lane
may be read as two sources agreeing. Where a later chapter qualifies or contradicts a chapter-2
claim, that is recorded as **the same author qualifying his own earlier statement** and is labelled
as such in the object's caveats.

Chapter 2 was **not re-extracted**. Its live `source-knowledge.yaml` was read in full before
extraction began, and eight objects in this lane name a live chapter-2 object explicitly where they
extend, qualify or repeat it:

| This lane | Relation to the live chapter-2 object |
|---|---|
| `sk_ogx_0003` | extends `sk_ogl_c003_0019` — supplies a mechanism (no retrieval + turnover) for the field's failure to codify |
| `sk_ogx_0012` | ch2 records Rudolph's story-appeal finding only inside a caveat on `sk_ogl_c003_0019` as abandoned research; ch7 states it as an operative craft rule with a dose-response form |
| `sk_ogx_0044` | qualifies `sk_ogl_c003_0007` — names what image consistency has to consist of, and its failure mode |
| `sk_ogx_0049` | supplies the reason behind `sk_ogl_c003_0020` — attributability, a property of the distribution channel |
| `sk_ogx_0056` | **qualifies `sk_ogl_c003_0017`** — see §6 |
| `sk_ogx_0059` | qualifies `sk_ogl_c003_0007` — names the external cost of consistency (predictability) |
| `sk_ogx_0063` | gives the operational stopping rule for `sk_ogl_c003_0017` |
| `sk_ogx_0065` | repeats the limit already in `sk_ogl_c003_0012` — research cannot predict a campaign's long-run value |

A mechanical concept-label diff against the live file returned **zero exact collisions** and, on
inspection, **zero conceptual duplicates**. The highest string-similarity pairs are artefacts of
long snake_case labels sharing function words, not shared claims. See `EXTRACTION-NOTES.md` §5.

---

## 3. Span covered — and what was not covered

The book's own contents page gives **20 chapters** plus a reading list, index, picture credits and
an appendix. That list was taken from the book, not assumed.

### Chapters READ IN FULL and extracted

| Ch. | Title | Objects |
|---|---|---|
| 1 | Overture | 2 |
| 7 | Wanted: a renaissance in print advertising | 27 |
| 8 | How to make TV commercials that sell | 13 |
| 9 | Advertising corporations | 1 |
| 10 | How to advertise foreign travel | 1 |
| 11 | The secrets of success in business-to-business advertising | 3 |
| 12 | Direct mail, my first love and secret weapon | 8 |
| 13 | Advertising for good causes | 1 |
| 14 | Competing with Procter & Gamble | 2 |
| 15 | 18 Miracles of research | 6 |
| 16 | What little I know about marketing | 2 |
| 17 | Is America still top nation? | 1 |
| 19 | What's wrong with advertising? | 1 |
| 20 | I predict 13 changes | 0 — read, nothing extracted (see below) |

### Chapters READ IN PART

| Ch. | Title | What was read | Objects |
|---|---|---|---|
| 3 | Jobs in advertising – and how to get them | section headings enumerated; the sections *Copywriters*, *Art directors*, *Account executives*, *Researchers*, *Media*, *Women in advertising*, *Firing and hiring*, *Education for advertising*, *Social status* read in full | 1 |
| 4 | How to run an advertising agency | section headings enumerated; *Written principles*, *Profit and all that*, *How to get paid*, *What to do with your profits* read in full | 0 |
| 5 | How to get clients | section headings enumerated; *Five tips* read in full | 0 |
| 18 | Lasker, Resor, Rubicam, Burnett, Hopkins and Bernbach | searched exhaustively for reasoning about the work rather than biography; the Hopkins section read in full | 1 |

### Chapter READ IN FULL and deliberately not extracted from

| Ch. | Title | Reason |
|---|---|---|
| 6 | Open letter to a client in search of an agency | Entirely business-of-agency: how to pick an agency, what to pay it, contract length, conflict policy. Refused under the lane's brief. |

**Chapter 20** was read in full and produced nothing. It is thirteen one-line predictions for the
future of the advertising business. One of them — that better research would generate a bigger
corpus of knowledge, which creative people would learn to exploit — is a real causal statement, but
extracting a 1983 prediction as knowledge would be recording a forecast as a finding. It is named
here so the omission is visible rather than silent.

**I did not read chapters 4 and 5 in full**, and I read only part of chapter 3. Those three
chapters are the running of an agency, the winning of clients and the getting of jobs. The lane's
brief instructs refusal of business-of-agency material, so I enumerated their section headings,
read the sections that could plausibly contain reasoning about the work, and stopped. One object
came out of chapter 3 (`sk_ogx_0003`, the loss of research findings). **If genuine craft reasoning
is buried in the unread portions of chapters 3, 4 and 5, this lane has missed it.** That is a
partial extraction and it is recorded as partial.

Front and back matter — copyright page, contents, reading list, index, picture credits — were
consulted for provenance and not extracted from.

---

## 4. Locators — Case 3, EPUB with no authored page

Per `SCHEMA-CONTRACT-ADDENDUM-LOCATORS.md` **Case 3**:

- **There are no authored page numbers in this format and none is invented anywhere in this lane.**
- Every `provenance.page_start` and `provenance.page_end` is `null`, in `source-knowledge.yaml`
  and in `source-concept-systems.yaml`. Asserted mechanically: **0 violations across 70
  SourceKnowledge objects and 3 concept systems.**
- Every `source_locator` in `qa-bank.yaml` is chapter number + chapter title + the book's own
  section heading, with the spine marker as a file-position aid. Asserted mechanically against
  `\bpp?\.\s*\d`: **0 page-style locators across 76 Q&A items.**
- Audit pattern recorded: **`no_authored_page`**.
- The book's own text cross-references pages ("see this page") in several places. In this copy
  those references are **unresolvable** — the ebook renders them as the words "this page" with no
  target. They were not resolved by guessing. Noted in `EXTRACTION-NOTES.md`.

---

## 5. Verification of the extract against the source

All 70 SourceKnowledge objects were checked mechanically: for each object, at least one entry in
`source_terms` was located verbatim (after Unicode and punctuation normalisation) **inside the
chapter the object cites**. **70 of 70 passed. 0 failures, 0 corrections required.** This is a
stronger check than the required spot-check of 25, and it was run over the whole set rather than a
sample because it could be automated.

---

## 6. Where a later chapter qualifies chapter 2 — the load-bearing case

The most consequential is `sk_ogx_0056` against the live `sk_ogl_c003_0017`.

- **Chapter 2 (live Canon):** research shows readership does not decline across at least four
  repetitions in the same magazine; the audience is a moving parade, not a standing army; repeat a
  winning advertisement until it stops selling.
- **Chapter 12 (this lane):** "When you advertise repeatedly in the same magazine, response rates
  almost always drop." Some magazines support six profitable insertions a year, others twelve.

These are **not two sources disagreeing.** They are one author, in one book, reporting two
different measures — readership in the first case, orders in the second — and he never places them
side by side. The reconciliation is available in his own material and he does not make it. The
object records the qualification and states explicitly that it must not be presented as
cross-source disagreement. The Q&A bank tests exactly this at `qa_ogx_0047`.

Three further qualifications of chapter 2 are recorded the same way: the external cost of
consistency (`sk_ogx_0059`), what consistency must consist of to be recognisable
(`sk_ogx_0044`), and the operational stopping rule for a repeated campaign (`sk_ogx_0063`).

---

## 7. Visual evidence — figures not inspected

The book reproduces advertisements that carry its argument. In this copy those reproductions are
absent and replaced by **39 literal placeholders** reading "Click here for hi-res image" or "Click
here for hi-res image and text" — 6 of them in the print chapter, 1 in the television chapter.

**A finding that qualifies the live chapter-2 audit.** That audit recorded the loss pattern as
`announced_loss_placeholder` with `recoverability: recoverable_not_attempted`. This lane found that
the book's own **Appendix** (spine 30, "Hi-res images and related text") carries roughly 300 lines
of recovered advertisement **text**, with 40 "Click here to return to the text" links back into the
chapters. So the **copy of many of the reproduced advertisements is recoverable inside this same
file**; the **layout, typography and image are not**. The distinction matters for a book whose print
chapter argues from layout and typography specifically. It is recorded here and in
`EXTRACTION-NOTES.md`; the live audit record was **not modified**, this lane being read-only against
`canon/audit/**`.

No figure was inspected. Fourteen objects carry `extraction_uncertainty: figure_not_inspected`. No
visual claim is reconstructed from text anywhere in this lane. See `EXTRACTION-NOTES.md` §4 for the
caution name `figure_semantic_binding_lost` and the specific claims it affects.

---

## 8. Access basis and licence

- The Controller authorised read-only use of an **already-present local copy** of this book for
  extraction in this run.
- **Licence status has not been independently verified by this lane.** The copy is a commercial
  ebook in the user's own downloads. No claim is made here about the terms under which it was
  obtained or may be used, and no part of the book is reproduced at length: `source_terms` entries
  are short verbatim fragments used to anchor claims, and every Q&A answer is paraphrase.
- No content was redistributed and nothing was published.

---

## 9. Write boundary

This lane wrote **only** inside
`canon/experimental/book-expansion-qa-v1/ogilvy-beyond-ch2/`.

`canon/knowledge/current/ogilvy-ch2-advertising-that-sells/` and
`canon/audit/records/ogilvy-ch2-advertising-that-sells.audit.yaml` were **read only** and are
unmodified. Nothing was committed.
