# Provenance — W3C, Web Content Accessibility Guidelines (WCAG) 2.2

**EXPERIMENTAL — NOT LIVE CANON.** Lane 3 of the non-merge `book-expansion-qa-v1` expansion.
Nothing in this directory is accepted Canon and nothing here may be described as accepted.

## Source identity

| Field | Value |
|---|---|
| Title | Web Content Accessibility Guidelines (WCAG) 2.2 |
| Publisher / body | World Wide Web Consortium (W3C), Accessibility Guidelines Working Group |
| Status of the main document | **W3C Recommendation** (normative) |
| Canonical URL | https://www.w3.org/TR/WCAG22/ |
| Companion material | "Understanding WCAG 2.2" — https://www.w3.org/WAI/WCAG22/Understanding/ |
| Status of the companion | **W3C Working Group Note — non-normative** |
| Republication noted in source | 2024-12-12 republication of WCAG 2.2, incorporating errata (Change Log, section A) |
| `source_id` | `w3c-wcag22-text-legibility` |
| ID prefix | `wcag` |
| Local source text | `scratchpad/src/SRC-wcag22.txt` (3,055 lines) |

## Exact material available and processed

The supplied file is in three explicitly labelled parts:

1. **Part 1 — normative Success Criteria, Guideline 1.4 (Distinguishable).** SC 1.4.1 through
   SC 1.4.13 as published, including their normative notes and exception clauses. Guideline 2.1
   begins immediately after and is out of scope.
2. **Part 2 — the WCAG 2.2 glossary, in full.** Normative. Includes all six notes on
   `contrast ratio`, all six notes on `relative luminance`, all five notes on `large scale (text)`,
   and the definitions of `text`, `image of text`, `pure decoration`, `essential`,
   `user interface component`, `normative` and `informative`.
3. **Part 3 — seven "Understanding" documents, non-normative.** SC 1.4.1, 1.4.3, 1.4.4, 1.4.5,
   1.4.8, 1.4.11, 1.4.12.

**Span processed for this extraction.** Guideline 1.4 criteria on contrast, text presentation and
images of text (1.4.1, 1.4.3, 1.4.4, 1.4.5, 1.4.6, 1.4.8, 1.4.9, 1.4.10, 1.4.11, 1.4.12); the
glossary definitions those criteria depend on; and the corresponding Understanding notes.

**Deliberately not processed.** SC 1.4.2 (Audio Control), SC 1.4.7 (Low or No Background Audio) and
SC 1.4.13 (Content on Hover or Focus) — audio and pointer-interaction criteria outside the brief.
The glossary's non-visual entries, the Input Purposes list (section 7), the Change Log (A) and the
Acknowledgments (B) were read for context and not extracted.

## Locators — there are no page numbers

This source has **no pagination of any kind**. Every locator in this extraction is one of:

- a Success Criterion number and title, e.g. `SC 1.4.3 Contrast (Minimum)`
- a glossary term, e.g. `Glossary: contrast ratio, Note 3`
- an Understanding document and section heading, e.g.
  `Understanding SC 1.4.3, Rationale for the Ratios Chosen`

`provenance.page_start` and `provenance.page_end` are `null` in every SourceKnowledge object, and
the real locator is carried in `provenance.section`. **No page number was invented anywhere.**

## Normative status — tracked per object

Every SourceKnowledge object carries a caveat with `origin: source_stated` naming its authority
level, using the source's own vocabulary from `Glossary: normative` ("required for conformance")
and `Glossary: informative` ("for information purposes and not required for conformance").

- Objects `sk_wcag_0001`–`sk_wcag_0029` are supported by the Success Criteria or the glossary:
  **normative**.
- Objects `sk_wcag_0030`–`sk_wcag_0038` are supported only by Understanding documents:
  **non-normative W3C Working Group Notes**.

Every Q&A item repeats this in its `support` field. No answer grounded only in an Understanding
note is presented as a conformance requirement.

## Visual material

The Understanding documents reference 48 numbered figures. **None was inspected** — the supplied
file carries only the figures' text captions and the surrounding prose, which in this source state
the colour values and contrast ratios explicitly (e.g. `#767676` on white, `2.7:1`). Where an
object rests on a figure caption, `provenance.source_support` is `text` and
`evidence.extraction_uncertainty` is `figure_not_inspected`. See EXTRACTION-NOTES.md for the
`figure_semantic_binding_lost` assessment.

## Access basis

**W3C Document Licence.** An openly published international standard. No paywall, no
authentication, no circumvention. The Understanding notes are published by W3C/WAI on the same
open basis. Fully legitimate.

## Overlap with live Canon

**None found.** All nineteen live Canon sources are books or practitioner texts — design,
photography, film-craft and advertising. None is a standards document, none states a numeric
acceptance threshold, and none is authored by a standards body.

The nearest adjacencies, recorded as adjacencies and **not** as agreement:

- Albers (*Interaction of Color*) treats colour as relational and unmeasurable by name; WCAG
  treats one colour property — relative luminance contrast — as a computable number. These are
  neither compatible nor incompatible; they answer different questions. No cross-source claim of
  any kind is made in this lane.
- Live Canon typography sources address a held page or print surface. WCAG addresses web content
  rendered by a user agent under user control. The difference in surface is recorded in every
  binding's `applicability.limits`.

Per the schema contract §6, **no `xs_` cross-source concept was created**, and no cross-lane
ontology relationship was written (the parallel lanes' term IDs are not resolvable from here).

## The extraction's central caution, restated

WCAG 2.2 is an **accessibility conformance standard for web content**. Its thresholds are chosen
to serve users with low vision and colour-vision deficiency, as its own rationale states. The
source makes **no claim** that meeting 4.5:1 makes a piece of communication effective,
attention-getting or attractive, and no claim that failing it makes creative work bad. Applying
these numbers to a video thumbnail, a packshot or a feed creative is **our** extrapolation; it
appears only inside OperationalBindings marked `evidence_basis: extractor_inference`, never inside
a SourceKnowledge `claim`.
