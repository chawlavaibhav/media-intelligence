# PROVENANCE — `ries-22-immutable-laws-branding`

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon. It has not been
reviewed by the Controller or passed any Audit Gate, and it must never be described as accepted.

---

## 1. Source identity

| Field | Value |
|---|---|
| `source_id` | `ries-22-immutable-laws-branding` |
| ID prefix | `r22` |
| Authors | Al Ries and Laura Ries |
| Title | *The 22 Immutable Laws of Branding* |
| Edition | HarperBusiness / PerfectBound e-book edition, copyright © 2002 Al Ries and Laura Ries. The copyright page states: "This edition combines *The 22 Immutable Laws of Branding* and *The 11 Immutable Laws of Internet Branding* with added illustrations and text." |
| Publisher | HarperCollins Publishers Inc., New York (PerfectBound imprint) |
| Local original | `/Users/vaibhavchawla/Downloads/Books/The 22 Immutable Laws of Branding.pdf` |
| File size | 1,002,744 bytes |
| SHA-256 | `9083461dc721ca4fff19b49aaf4d7ee76608162c2ee5a8ce741341761fc04ce2` |
| Page-marked text used | `scratchpad/src/PDF-22-laws-branding.txt` |
| PDF pages | 257 |

The original *22 Immutable Laws of Branding* was first published in 1998; the *11 Immutable Laws of
Internet Branding* in 2000. This 2002 combined edition is the copy inspected. The extraction does
not attempt to distinguish 1998 text from 2002 additions — the copy does not mark them.

---

## 2. Locator case and page mapping — Case 1 (PDF with verified authored folio)

The supplied source text header reads:

```
PAGE MAPPING DETECTED: printed page = PDF page - 17 (folio agreement on 229 pages).
USE THE PRINTED NUMBER IN LOCATORS.
```

**The mapping was verified independently by this lane**, not assumed:

| Check | PDF page | Expected printed | Folio actually seen |
|---|---|---|---|
| End of the 22 Laws span | 127 | 110 | `110` in the running head; the next page's head reads `Page 111` and opens "THE 11 IMMUTABLE LAWS OF INTERNET BRANDING" |
| Mid-book | 47 | 30 | `30` in the running head |
| Mid-book | 87 | 70 | `70` in the running head |
| Chapter opener | 30 | 13 | running head shows `3` (the **chapter number**), folio `13` printed at the foot of the page |
| Chapter opener | 66 | 49 | running head shows `10` (chapter number), folio `49` at the foot |
| Chapter opener | 100 | 83 | running head shows `16` (chapter number), folio `83` at the foot |

**All locators in this lane use the PRINTED page number.** Front matter carries roman folios
(`ix`–`xvi`); the marker file renders these as negative printed numbers (`-7` … `0`). Where this
lane cites front matter it writes the **roman folio** in `source_locator` (e.g. `printed p. ix`) and
sets `provenance.page_start` / `page_end` to `null` with the roman range recorded in
`provenance.section`, because a negative integer is not an authored page number.

**No folio disagreement was found.** The chapter-opening pages are not a disagreement: the number in
the head is the chapter number and the folio is printed at the foot, which is a normal design
convention. Reading the head as a folio on those pages would have produced badly wrong locators, so
three of them were checked deliberately.

**The offset was additionally re-verified mechanically across the whole file.** All 256
`<<<PRINTED_PAGE n | PDF_PAGE m>>>` markers were tested against `n = m - 17`: **zero violations**.
The positive printed folios present in the file run **1–240**, which is the real printed span of
this volume and the span every locator in this lane is asserted against. See `EXTRACTION-NOTES.md`
§5.2 for the assertion output.

---

## 3. Exact material extracted (span)

| | |
|---|---|
| **Span extracted** | Introduction (printed pp. **ix–xvi**) and *The 22 Immutable Laws of Branding*, chapters 1–22 (printed pp. **1–110**, chapter text pp. 3–110) |
| **Span NOT extracted** | *The 11 Immutable Laws of Internet Branding* (printed pp. **111–230**), About the Authors, Also-by list, Credits, copyright and publisher pages (pp. 231–240) |

The lane brief scopes this extraction to "the 22 named laws". The eleven Internet-branding laws are a
separate, later, and heavily period-bound work bound into the same volume; they are **deliberately
out of scope** and nothing in this directory draws on them. They are noted in `EXTRACTION-NOTES.md`
as available-but-unextracted material, not as a gap.

Both text and the book's structural apparatus (chapter titles, the epigram under each chapter title,
numbered lists) were inspected. **The volume's "added illustrations" do not appear as extractable
figures in this PDF's text layer, and no figure was inspected.** No object in this lane claims
`source_support: visual` or `text_and_visual`; every object is `text`. Where the book's argument is
visual in character (the Law of Shape's logotype proportion, the Law of Color's colour choices) the
argument is nonetheless carried entirely by prose in this copy, and the caution
`figure_semantic_binding_lost` is recorded in `EXTRACTION-NOTES.md`.

---

## 4. Access basis

The Controller authorised **read-only** use of this already-present local copy for extraction.
The copy is a commercial DRM-era e-book conversion; its copyright page asserts that access was
granted "by payment of the required fees" and restricts reproduction.

**Licence status was not independently verified by this lane.** No attempt was made to establish
whether this particular file is a licensed copy. The extraction therefore treats the text as
copyright-restricted throughout: the Q&A bank is overwhelmingly paraphrase, `source_terms` are kept
to short verbatim phrases where the exact wording is load-bearing (chiefly the twenty-two law names
and epigrams, which are the source's own terminology), and no long passage is reproduced anywhere in
this directory.

---

## 5. Overlap with live Canon

**None. This is an independent origin against all nineteen live sources.**

- No live source directory names Ries, Ries & Ries, Trout, *Positioning*, or any of the 22 laws.
- This is **not** a scope extension. There is no `scope_extension_of`.
- The nearest live source by subject is `binet-field-effectiveness-in-context-ch1`, which is a
  different work by different authors from a different tradition and reaches materially different
  conclusions. That is **disagreement between independent sources**, not overlap, and it is recorded
  as an unadjudicated observation in `EXTRACTION-NOTES.md` under
  *"Observations for cross-source review (NOT promotions)"*. **No cross-source concept was created.
  Nothing was resolved.**

---

## 6. Evidential character of this source — read this before using anything here

This is the single most important paragraph in this file.

*The 22 Immutable Laws of Branding* asserts lawlike, universal status for claims that are supported
in this text **almost entirely by selected corporate anecdote**. The authors are practising
consultants writing in their own frame about their own clients and about companies whose outcomes
were already known when the book was written.

Specifically:

1. **"Immutable law" is rhetoric, not a finding.** The word "law" in this book carries no evidential
   weight beyond the authors' assertion. Every object in this lane that reproduces a law is tagged
   `practitioner_assertion`, and most are tagged `anecdotal` and `outcome_claimed`. Nothing in this
   lane should be read as though "law" implied replication, measurement, or generalisation.
2. **The book contradicts its own immutability claim.** Chapter 20 states plainly that nothing in
   branding is absolute, that there are exceptions to every rule, and that the Law of Change is the
   biggest exception to the laws of branding (printed p. 101). Chapter 21 concedes that while the
   laws are immutable, brands are not (printed p. 105). Chapter 15 concedes that the laws "seem to
   suggest" single-brand concentration and then licenses a second brand (printed p. 77). This is
   captured as its own SourceKnowledge object (`sk_r22_0049`).
3. **Survivorship and hindsight are unmanaged.** Cases are chosen after outcomes were known.
   Successes (Starbucks, Subway, Toys "R" Us, FedEx, Volvo, Absolut, DeWalt, L'eggs, Olive Garden)
   are presented as consequences of following the laws; failures (Chevrolet, American Express, Levi
   Strauss, Crest, Miller Regular, Bayer Select, Arch Deluxe, Holiday Inn Crowne Plaza, Boston
   Market, Atari, Newton) as consequences of breaking them. **Counter-examples are largely absent**:
   the book does not present focused brands that failed, or extended brands that succeeded and kept
   succeeding, except where it can immediately re-label them (Diet Coke is explained away by
   competitor weakness, printed p. 7; Vaseline Intensive Care by customer misreading of the name,
   printed p. 66; General Electric by all its competitors being equally weak, printed p. 36). The
   base rate is never given: the reader is never told how many focused brands were launched, or how
   many extensions were launched, or what proportion of each survived. **No causal claim in this
   book is supported by a controlled comparison.**
4. **`empirical_within_source` count: ZERO.** See §7.
5. **The examples are of their period.** Every company case is pre-2002 and many of these companies'
   fates have since changed. Objects carrying period-bound examples are tagged `historical_claim`.
   **This lane has deliberately not updated any example with what happened afterwards** — there is no
   source for that here and doing so would be invention.
6. **The book is about brands and markets.** It contains nothing about generative media and no
   inference about any model's capability has been drawn from it. No `creative_ir` binding exists in
   this lane (SPEC-01 was not supplied to it) and no advice in the source has been rewritten as a
   model instruction.

---

## 7. `empirical_within_source` — zero, and why

**No object in `source-knowledge.yaml` carries `empirical_within_source`.** The characteristic is
reserved for a measurement the source itself made and reported. Every quantitative statement in this
span falls into one of four categories, none of which qualifies:

| Kind | Examples | Why it is not `empirical_within_source` |
|---|---|---|
| Reported third-party figures | Kroger scanner data on 23,000 store items (printed p. 49); U.S. vs Japanese top-100 profit margins (p. 47); an unnamed "widely publicized study" of 25 leading brands from 1923 (p. 32); Consumer Reports rankings (p. 35) | Someone else's data, reported second-hand, method and provenance unstated |
| Market-share before/after pairs | American Express 27%→18%, Levi's 31%→19%, Crest 36%→25% (pp. 4–5) | Two numbers with no comparison group, no time alignment, and no test of the asserted cause |
| Asserted research with nothing behind it | "Our research indicates that 50 percent is about the upper limit" (p. 60); "Years of observation have led us to this conclusion" on quality and sales (p. 35) | Research is invoked, not reported. No method, no sample, no data |
| Illustrative counts | 45% of national flags dominated by red (p. 86); 90% of new grocery products are line extensions (p. 49) | Descriptive figures cited without source, used to decorate an argument they do not test |

The nearest miss is the Consumer Reports small-car comparison (printed p. 35), where the authors
themselves line up quality rank against sales rank and report three pairs. This lane **rejected** it
as `empirical_within_source` because: the ranking is undated and unnamed beyond "recent"; the sales
ranking's source is not given; only three of the sixteen ranked brands are reported, and they are
the three that make the point; and no statistic is computed. It is recorded as
`outcome_claimed` + `anecdotal` with an `extractor_observed` caveat saying exactly this.

**Zero is a finding, not a gap.** It is the honest characterisation of a book that calls its content
immutable law.

---

## 8. Files in this directory

| File | Contents |
|---|---|
| `PROVENANCE.md` | this file |
| `source-knowledge.yaml` | 49 SPEC-03 SourceKnowledge objects |
| `source-concept-systems.yaml` | 3 SPEC-03 SourceConceptSystem objects |
| `operational-bindings.yaml` | 9 SPEC-04 bindings (3 benchmark, 3 evaluation, 3 governance) |
| `ontology-mappings.yaml` | SPEC-05 ontology — 61 terms, 20 relationships, 9 source-specific concepts |
| `qa-bank.yaml` | 50 Q&A items, 19 of them `requires_application` (0.38) |
| `EXTRACTION-NOTES.md` | method, hazards, refusals, cross-source observations, self-check results |

All counts above were written before the files existed, as targets, and all four were met exactly.

---

## 9. Self-check outcome (summary; full results in `EXTRACTION-NOTES.md` §5)

- Every YAML file parses, and every controlled vocabulary, required key and internal reference was
  checked in code. Zero errors, zero dangling references across all five files.
- **Locators: 87 page numerals across the 50 Q&A items, every one inside the real printed span
  1–240 and inside this lane's extracted span 3–110. Zero failures, zero corrections.** Thirty-four
  items were spot-checked against the actual page text (the brief required twenty); the single flag
  was a false positive on a passage that spans a page break, investigated and confirmed correct.
- **`empirical_within_source`: ZERO.** See §7 above.
- **Application fraction: 19/50 = 0.38**, against a required minimum of one third.
- No cross-source concept, term relationship or binding was created. The disagreements with
  `binet-field-effectiveness-in-context-ch1` are recorded as unadjudicated prose observations in
  `EXTRACTION-NOTES.md` §6 and nowhere else.
