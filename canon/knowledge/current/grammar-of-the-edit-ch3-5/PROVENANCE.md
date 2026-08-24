# Provenance record — Grammar of the Edit, ch.3–5 (CANON-003 book 9, Lane B)

**Book:** Roy Thompson & Christopher J. Bowen, *Grammar of the Edit*, **Second Edition**, Focal
Press / Elsevier, 2009.
**Section processed:** Chapters Three, Four and Five, complete — printed pages 55–109.

## Why this section

Three chapters taken as one span, which CANON-003 permits as "a tightly connected multi-chapter
span". The connection is the source's own, not a convenience:

- **Chapter Three** introduces six factors that make a transition a good edit.
- **Chapter Four** opens by saying it will analyse each transition against "the six elements of
  information, motivation, composition, camera angle, continuity, and sound" — and then does so,
  four times, before defining five categories of edit type. It is not readable without Chapter
  Three.
- **Chapter Five** states the seven general practices that govern both, and carries the section's
  strongest visual evidence — the matched correct/incorrect line-crossing pair.

Chapter Two covers shot types and footage properties; Chapter Six is workflow procedure. Both are
different material and are excluded.

**Object count is scope, not a method change.** This span is 55 printed pages against roughly 20 for
the earlier books in the batch, and the source is unusually enumerative. It produced 60
SourceKnowledge objects — about 1.1 per printed page, against 0.85 per page for book 1. The V0
granularity rule was applied unchanged; the count follows from section size and source shape.

## Identity and integrity

| Check | Result |
|---|---|
| Local file | `~/Downloads/Books/Grammar of the Edit, .pdf` |
| `/Title` | "Grammar of the Edit, Second Edition" |
| `/Author` | "Roy Thompson and Christopher J. Bowen" |
| `/Creator` · `/Producer` | Adobe Acrobat 7.0 · Acrobat Distiller 7.0, created 6 Feb 2009 |
| Page count | 225 |
| Page offset | PDF page = printed page + 13 |
| Chapter span | printed 55–109 = PDF 68–122 |
| Boundaries confirmed | PDF 68 begins "Chapter Three"; PDF 110 begins "Chapter Five"; PDF 124 begins Chapter Six |
| Source type | **Native digital PDF**, not a scan — real text layer, no OCR |
| Words extracted | 15,755 |
| Garbling | **none detected** |

**Character-level artifacts, both reversible and neither blocking.** 129 words (0.81%) carry `ﬁ` or
`ﬂ` typographic ligatures emitted as single Unicode characters, and two instances of `=` are emitted
as `⫽` (U+2AFD). Meaning is unaffected. Recorded because the batch has already seen a text-extraction
artifact imitate a provenance failure once — a naive verbatim match against an ASCII transcript would
miss every ligature word and could be read as an edition mismatch.

**Section completeness check.** Every section named in the book's contents page for these three
chapters was searched for in the extracted text. All present. This is the contents-page control that
caught a buried section in book 5; here it returned clean.

## Visual evidence — VERIFIED

`visual_completeness: verified_page_level`. All 55 pages rendered ephemerally at 105 dpi (plus two
crops at 200 dpi) into the session scratchpad and inspected; **no page images committed**.

The section contains 23 figures and 90 embedded images. All 23 captions survived text extraction;
none of the 90 images did.

**Colour control — this source is natively monochrome.** Of 291 embedded images in the whole book,
276 are single-separation and 11 greyscale; exactly one is RGB, and it is the cover on PDF page 1.
Across the extracted span every image is single-separation. This is a black-and-white printed book,
not a colour book stripped in digitisation — the distinction that made book 4 (Albers) dangerous.
Nothing in the section's argument depends on hue.

## What this book contributed

**1. A genuine controlled comparison across two pages, invisible in text.** Figure 5.4 and Figure
5.5 photograph the same two actors, in the same wardrobe, at the same location, at the same framing
scale. Figure 5.5 reuses Figure 5.4's first two frames unchanged and replaces only the third — the
same actor, moved to the opposite side of frame, looking the opposite way. One variable changed, the
rest held. In plain text this reduces to two nearly identical caption sentences and a scatter of the
letters A to F, with no signal that the two figures are the same setup photographed twice.

**2. Text baked into artwork is lost silently.** The labels `WRONG SIDE OF LINE` (Figure 5.5) and
`THE LINE` (Figure 5.3) are typeset inside the diagrams. Neither string occurs anywhere in the
extracted text of the section, or of the whole book. The first is what marks which diagram is the
error case. Unlike book 5's buried section, which a contents page revealed, **there is no cheap
independent index that would flag missing in-graphic text.** It was found only by rendering and
reading the pages.

**3. A source-internal error only a visual pass can catch.** On printed page 61 the text reads
"(see Figure 3.4E and F)". Figure 3.4 is on page 64 and has three panels, A to C, showing camera
angles. The train-whistle sound bridge the sentence is about is Figure 3.2E and F, on the same page
as the sentence. A text-only extractor would have no way to know the pointer is broken and could
attach the claim to the wrong demonstration. The extraction cites what the source actually shows and
records the misdirection as an extractor-observed caveat.

**4. A counter-case: one figure is fully recoverable from text.** Figure 5.2 illustrates the
shot-length method, and the prose enumerates every element of the picture — house, chimney smoke,
walking man, setting sun — because the method being taught *is* describing the shot aloud. Visual
loss is not uniform across a figure-bearing source, and where a figure survives, the reason can be
stated.

**5. The named framework and the applied framework differ.** The source calls its checklist "the six
elements" and applies a different subset seven times: six to the cut, six-with-time-replacing-
continuity to the dissolve, four to the fade, two explicitly waived for the wipe, all six waived for
the concept edit. Three of the seven departures are the source's own words; the other four are
silent. Recorded as `scs_gote_c003_002` with the counts checkable against named pages.

## Schema observation — recorded, not acted on

Thirteen intra-source connections were **dropped** rather than expressed, because SPEC-03's
`intra_source_relations` vocabulary has no relation that fits them honestly. The vocabulary offers
`qualifies`, `qualified_by`, `trades_off_with`, `depends_on`, `generalises`, `specialises`,
`contradicts`, `demonstrated_together_with` and `member_of_system` — all hierarchical, causal or
oppositional. It has no way to say *these two are siblings*, *these are alternatives for the same
decision*, or *these are orthogonal classifications of the same event*.

The most consequential loss is between `sk_gote_c003_0039` (the five edit categories) and
`sk_gote_c003_0024` (the four transitions). These are two independent classifications of one event —
the categories describe the relation between two shots, the transitions describe the mechanics of
joining them, and the source's own review confirms it ("the combined edit is still just a cut,
dissolve, or wipe at one transition"). Neither generalises the other and they do not conflict. The
relation is stated in prose inside both objects' caveats and is **not** machine-readable.

No relation type was invented, and SPEC-05's `related_to` was not borrowed into the SPEC-03 layer —
that mistake was made during drafting and caught by mechanical validation, which is how it came to
be recorded here. Full list in the lane issue file.

## Mechanical validation

All five files pass SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints:
60 SourceKnowledge objects · 5 SourceConceptSystems · 48 ontology terms · 15 relationships ·
6 concepts (4 source-specific, 2 canonical, 0 cross-source — correct for a single-source file) ·
11 operational bindings.

## Isolation

**No Canon knowledge file for *Grammar of the Shot* was opened at any point during this
extraction**, although the two books share authors, publisher, series and subject, and *Grammar of
the Shot* ch.4 is book 1 of this same batch. Everything above was read off this source. Whether the
two books produce overlapping knowledge is a question for the post-checkpoint comparison and was not
an input to it.

## Historical material

Sealed until this book's fresh checkpoint commit exists. Not opened during extraction. Whether any
historical *Grammar of the Edit* material exists in this repository has **not been checked** — that
search happens after the checkpoint, per CANON-003.
