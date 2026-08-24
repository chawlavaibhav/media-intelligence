# Provenance record — The Conversations, Third Conversation (CANON-003 book 12, Lane B)

**Book:** Michael Ondaatje, *The Conversations: Walter Murch and the Art of Editing Film*, Knopf,
2002.
**Section processed:** the Third Conversation, complete — seven named sections, from *Editing The
Conversation* through *The Most Characteristic Angle*.

## Why this section

One complete conversation, which is **the source's own unit**. Each chapter is a single meeting, in
a single place, on a single day; this one is New York in December 2000, in a SoHo loft where the
steam pipes kept startling the participants. It is contiguous, self-contained, and the smallest
complete unit the source itself defines.

Nothing was taken from elsewhere in the book. The Introduction — which is Ondaatje's own essay
rather than conversation — was read **only** to establish the source's identity and form, and no
claim was drawn from it.

## Identity and integrity

| Check | Result |
|---|---|
| Local file | `~/Downloads/Books/The Conversations_ Walter Murch and the Art of Editing Film.epub` |
| `dc:title` · `dc:creator` | "The Conversations" · Michael Ondaatje (`opf:role="aut"`) |
| `dc:publisher` · `dc:rights` | Knopf Doubleday · "Copyright © 2002 by Michael Ondaatje" |
| ISBN | 978-0-307-51817-0 |
| Conversion | calibre 0.9.12, January 2013 |
| Stated origin | "talks that took place during our meetings over the next year, starting in July 2000" |
| Words in chapter | 13,774 |
| Replacement characters | **0** — and 0 across all five conversations plus the introduction (92,199 words) |
| Garbling | none detected |

Encoding is intact and positively verified rather than merely un-flagged: 155 em-dashes, 45 pairs of
curly quotes, 23 ellipses, and correctly decoded accents in *Almásy*, *fêted* and *d'échafaud*.

**A method note worth recording.** A first sweep for section headings used a plain uppercase pattern
and found five of the seven, silently missing the two whose titles contain an apostrophe or a
quotation mark (*What's Under the Hands?* and *"Night Was Night": Re-editing Touch of Evil*). Both
were found by reading the chapter. A completeness check built on a naive pattern can under-report
and still look like it passed.

## Visual evidence — `not_verified_page_level`

This is an EPUB, so **there is no page to inspect**. That matters more than usual here, because this
is a *plate book*: a print volume whose photographs were grouped across facing pages, with captions
written to address several plates at once by position. Reflowing destroyed the arrangement the
captions describe.

Recorded as `not_verified_page_level` rather than `blocked_visual_validation` — the images are
present and were inspected. What cannot be verified is how they were **organised**.

### The finding: caption and image both survive, and the binding between them does not

Four caption blocks in this chapter use print-relative position words — *"Overleaf:"*, *"Above:"*,
*"Right:"*, *"center"*, *"far right"* — to say which plate each clause describes. In a reflowable
EPUB those words point at nothing.

The worked case: one caption names **three** films. The image beside it (076), inspected, contains
**two** of them — *In the Mood for Love* across the top, *Rear Window* at the lower right — plus a
**black rectangle** where a third plate sat in the printed book. The film named by "Overleaf" is not
in that image at all.

This is the **third distinct visual-loss mechanism** this lane has met, and it is unlike the others.
Book 9 lost pictures, and lost text drawn inside pictures. Book 10 lost typographic emphasis on words
that survived. Here nothing is missing — caption and image both survive — and what is lost is the
**correspondence**. A text-only extractor sees complete, confident, well-formed captions with no
signal that they have been detached from their referents.

Unlike book 9's in-graphic text loss, this one has a **cheap detector**: search captions for
print-relative position words. Four hits in this chapter, all true positives.

### Two further visual observations

- **A primary document reproduced as a photograph.** Image 084 is page 1 of Welles's fifty-eight-page
  memo — roughly 200 words of legible typescript. The text layer carries only the caption. The
  conversation quotes one fragment ("I assume the opening music is temporary") and paraphrases the
  topic, so recovery is partial: the opening clause survives, ~190 words do not. A second memo page
  (087) has nothing of its content quoted anywhere.
- **A figure can survive extraction and still not carry its evidence.** Image 090 illustrates the
  claim that there is "a chemistry between each actor and a certain lens" — a claim about the
  planarity of a face under a given lens. It is reproduced at 207 × 158 pixels, which cannot support
  inspection of that property. Availability is necessary and not sufficient; **resolution belongs in
  the same assessment.**

All 20 images in the chapter are greyscale, and no claim in the chapter refers to colour. Unlike the
Albers hazard, there is nothing here for a greyscale reproduction to destroy.

## The source's form — four registers, recorded before extraction

This chapter interleaves four kinds of text carrying different evidential weight:

1. **Ondaatje's third-person editorial frame**, setting the scene — authorial writing.
2. **The transcribed dialogue**, marked `O:` and `M:`.
3. **An inset first-person contribution from a third party** — the producer Rick Schmidlin's ~400-word
   account, *"As if Orson was sending us notes"*.
4. **Photograph captions**, some carrying substantive content.

The register determines who is making a claim, and this source has no single voice. A statement can
be Murch asserting; Ondaatje proposing and Murch assenting ("Mm-hm", "Right"); Ondaatje asserting
unchallenged; or a third party recalling. Those are different evidential situations.

**SPEC-03 has no field for a speaker.** `source_id` names the work. Every object below therefore
names its speaker in the claim text and quotes with the source's own `O:`/`M:` markers in
`source_terms`. Recorded as **LB-15**, not solved by adding a field.

## This source does not teach the way a textbook teaches, and was not made to

Nothing here is numbered, ranked, defined or summarised. Three consequences, all deliberate:

- **Many passages yield no object at all.** Long stretches are film history, biography, production
  gossip and literary comparison. Where Murch describes what he did on one film without asserting it
  generalises, the act is recorded as an **example** inside an object whose claim the source actually
  makes — never promoted into a principle he did not state.
- **Only three SourceConceptSystems**, against five and four for books 9 and 10. A speaker answering
  questions does not construct taxonomies; he returns to preoccupations. Two of the three are marked
  largely `extractor_inferred` and labelled as hypotheses about the source.
- **Hedges and abandonments are preserved.** "I don't know whether love is the right word."
  "Curiously, I wasn't consciously aware of this when I was working on the film." "It is and it
  isn't." In a transcript the hedge is often the most accurate part of the claim.

## Disclosed contamination

`sk_conv_c003_0027` records the Egyptian-painting argument. **I recognised it on sight**, because I
had extracted a compressed version of the same argument from *In the Blink of an Eye* earlier in this
lane, where it appears as a footnote.

Nothing was imported — the object is written from the wording in front of me, which is substantially
longer and differently developed. But an extraction cannot claim an independence it does not have,
so the recognition is disclosed on the object itself and discussed in the findings. This is the same
class of problem the batch already logged when specs were found to quote books the batch processes:
**extracting two books by or about the same person in one lane means the second extraction is
performed by someone who has read the first.**

## Mechanical validation

All five files pass SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints:
27 SourceKnowledge objects · 3 SourceConceptSystems · 16 ontology terms · 8 relationships ·
3 concepts (2 source-specific, 1 canonical, 0 cross-source — correct for a single-source file) ·
6 operational bindings.

Sixteen terms against book 9's 48 is the source shape, not thin work: a textbook names things because
naming is how it teaches; a conversation reaches for a figure of speech instead. Six bindings against
27 objects is likewise expected — much of this chapter is testimony about one film under one set of
constraints, true and well evidenced as testimony, and never a claim about films in general.

## Historical material

Sealed until this book's fresh checkpoint commit exists. Not opened during extraction. Whether any
historical Ondaatje or *Conversations* material exists in this repository has **not been checked** —
that search happens after the checkpoint, per CANON-003.
