# Provenance — Adam Connor & Aaron Irizarry, *Discussing Design*

**EXPERIMENTAL — NOT LIVE CANON.** A lane of the non-merge `book-expansion-qa-v1` expansion.
Nothing in this directory is accepted Canon and nothing here may be described as accepted.

## Source identity

| Field | Value |
|---|---|
| Title | *Discussing Design: Improving Communication and Collaboration through Critique* |
| Authors | Adam Connor and Aaron Irizarry |
| Publisher | O'Reilly Media |
| Year | 2015 |
| `source_id` | `connor-irizarry-discussing-design` |
| ID prefix | `disc` |
| Local original | `/Users/vaibhavchawla/Downloads/Books/Discussing Design.pdf` (205 PDF pages) |
| Page-marked text | `scratchpad/src/PDF-discussing-design.txt` |

Six named practitioners contribute signed sidebars inside the book: Kevin M. Hoffman with
Chris Cashdollar (printed pp. 31–32), Kim Goodwin (61–62), Veronica Erb (73–74),
Russ Unger (80–82), Jeff Gothelf (88–90) and Brad Nunnally (125–126). Where an object rests
on a sidebar rather than on the authors' own text, the object says so in a caveat and names
the contributor, because a sidebar is a *different practitioner's* assertion carried inside
this book, not the authors'.

## Locators — Case 1, PDF with a verified authored folio

The supplied text file declares:

```
PAGE MAPPING DETECTED: printed page = PDF page - 18 (folio agreement on 178 pages).
USE THE PRINTED NUMBER IN LOCATORS.
```

**Every locator in this extraction is a printed page number.** `provenance.page_start` and
`page_end` carry printed numbers.

**The offset was checked, not assumed.** Three pages were rendered from the original PDF and
the printed folio read directly off the page image:

| PDF page rendered | Folio visible on the page | Marker's printed number | Agree? |
|---|---|---|---|
| 24 | `6` | 6 | yes |
| 27 | `9` | 9 | yes |
| 138 | `120` | 120 | yes |
| 141 | `123` | 123 | yes |
| 170 | `152` | 152 | yes |
| 172 | `154` | 154 | yes |
| 173 | `155` | 155 | yes |
| 51 | `33` | 33 | yes |
| 77 | `59` | 59 | yes |
| 81 | `63` | 63 | yes |

Ten for ten. **No page where the folio disagrees with the marker was found.** The last
three were rendered in this pass, on pages carrying figures whose meaning the prose does not
fully carry (see `EXTRACTION-NOTES.md`, "Figures inspected"); reading the folio off them was
free, so it was done.

### The real printed span

Enumerated mechanically from the marker set in the source file:

- **Positive printed pages present: 1 – 187**, 182 of them.
- **Absent: 20, 76, 142, 174, 180.** These are the blank versos before chapter and section
  openings. They are not extraction failures; the pages carry no content and therefore no folio.
- Front matter is marked with negative numbers (`-17` to `-1`) because the folio there is roman
  (ix–xvi) and the detector could not express it. **Nothing in this extraction cites a negative
  or roman-numbered page.**

### The span actually used

| Range | Content | Cited here? |
|---|---|---|
| printed 1–19 | Ch. 1 Understanding Critique | yes |
| printed 21–46 | Ch. 2 What Critique Looks Like | yes |
| printed 47–75 | Ch. 3 Culture and Critique | yes |
| printed 77–108 | Ch. 4 Making Critique a Part of Your Process | yes |
| printed 109–141 | Ch. 5 Facilitating Critique | yes |
| printed 143–168 | Ch. 6 Critiquing with Difficult People and Challenging Situations | yes |
| printed 169–173 | Ch. 7 Summary | sparingly — it restates earlier chapters |
| printed 175–179 | Appendix A, The 10 Bad Habits That Hurt Critique | yes |
| printed 181–187 | Index | no |

**No locator in this extraction falls outside printed 1–179**, and none names one of the five
absent pages. Both facts were asserted mechanically; see `EXTRACTION-NOTES.md`.

## Access basis

The Controller authorised read-only use of a copy already present on this machine at
`~/Downloads/Books/Discussing Design.pdf`. The file was opened for reading only; nothing was
downloaded, purchased, decrypted or redistributed, and no long passage is reproduced in any
output file.

**Licence status was not independently verified.** This lane has no way to check how the local
copy was obtained or whether its use here is within the terms under which it was supplied. No
claim of ownership, licence or fair use is made — the honest statement is that the file was
already on disk, the Controller authorised reading it, and its provenance was not established.
That is recorded here rather than quietly assumed.

## Overlap with live Canon

**None.** The nineteen live Canon sources are practitioner texts on design, photography,
film craft, typography and advertising, plus one standards document. **None of them is about
how judgement is conducted** — how a piece of work is assessed, by whom, against what, and what
makes an assessment usable. That is this book's whole subject.

### Observations for cross-source review (NOT promotions)

These are recorded as prose, here, and nowhere else. **No cross-source concept was created, no
cross-lane ontology relationship was written, and nothing below is asserted as agreement.**

1. **Nearest live neighbour: `catmull-creativity-inc-ch5`** (candour and feedback at Pixar).
   The two are adjacent but not equivalent, and it is worth naming exactly how.

   Connor & Irizarry are aware of Pixar and cite it once, at printed p. 83, describing Pixar's
   "Dailies" as a formal critique practice adapted from film review. **This is a one-directional
   citation and it defeats nothing**, but it does mean the two sources are not blind to one
   another and anyone assessing independence must look at it rather than assume it away.

   Both sources define a unit of usable feedback, and comparing the two definitions is the most
   informative thing a reviewer can do with this pair. The live Catmull object
   `sk_cat_c003_0015` records "the good note" by five properties: it states what is wrong,
   missing, unclear or senseless; it arrives early enough to be fixed; it makes no demand; any
   proposed fix illustrates rather than prescribes; and it is specific. Connor & Irizarry's three
   elements (printed p. 9) are: a specific aspect or decision; **related to an objective or best
   practice**; and how and why it does or does not serve that objective.

   Three of the five overlap in substance with the three — specificity, no demand, and (in
   Connor & Irizarry's timing material rather than in the three elements themselves) arriving
   early enough. **The middle element does not appear in Catmull's five at all.** Requiring the
   giver to name the objective the judgement is made against is this book's distinctive addition,
   and it is the element that makes a piece of feedback checkable by someone who was not in the
   room. That difference is recorded as an observation. It is **not** a claim that one source
   corrects the other, and neither is evidence for the other.

   The two also work at different levels: Catmull's chapter is largely about an institution — the
   Braintrust, its composition, and its lack of mandating power — while this book is largely
   about the sentence and the session. Nothing in this lane merges them.

2. **Against the ontology's own precedent.** SPEC-05 adopts the *Light: Science & Magic*
   discipline of refusing an ambiguous term rather than normalising it. This book does the
   opposite in one specific case, deliberately and with a stated reason: it declines to ban
   "I like" / "I don't like" from critique sessions (printed p. 116), because banning the phrase
   makes speakers flustered and costs more clarity than it buys, and it prescribes attaching a
   follow-up question instead. That is a *contrary* precedent on term governance, and it is
   recorded as such rather than smoothed over. It is not a disagreement between sources — the two
   are addressing different problems, one an ontology's admission rule and one a live
   conversation — and it is not presented as one.

3. **No independence claim is made.** This lane does not assert that this source is an
   independent origin against anything. Independence under SPEC-05 is established from Audit
   Gate lineage records, which do not exist for this source, and not from a count of
   `origin_ref` values. The Pixar citation at p. 83 is flagged above so that a later reviewer
   has it in hand.

## The extraction's central caution, restated

*Discussing Design* is a **practitioner methodology for human design teams**. Its subject is
synchronous conversation between people about interface and product work, and its remedies act on
**people** — how they ask, listen, frame, defer and follow up. It reports **no measurement of its
own**: not one study, experiment, count or controlled comparison of outcomes appears anywhere in
the book, and its single footnote is a dictionary definition of "collaborate" (printed p. 48).
Every claim is practitioner assertion, argument from stated premises, or recounted anecdote.

Applying any of it to an automated evaluation pipeline is **our** extrapolation. It appears only
inside OperationalBindings carrying `evidence_basis: extractor_inference`, with the gap stated in
each `applicability.limits`. It never appears inside a SourceKnowledge `claim`.

**Nothing here is evidence about what any generative model can do**, and no remedy in this lane
is translated into a generation instruction. Every `kind: remedy` term carries
`executable_by: human_edit` — because every remedy in this book is an act performed by a person
in a conversation — and none carries `generative_respecification`.
