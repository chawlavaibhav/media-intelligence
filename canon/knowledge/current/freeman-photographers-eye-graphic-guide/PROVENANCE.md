# Provenance record — Freeman, *The Photographer's Eye: A Graphic Guide* (CANON-003 book 7, Lane A)

**Book:** Michael Freeman, *The Photographer's Eye: A Graphic Guide*. Focal Press (imprint of
Taylor & Francis), first published USA 2013; conceived, designed and produced by Ilex Press Ltd.
ISBN 978-0-240-82426-0 (pbk), 978-0-240-82460-4 (ebk).
**Section processed:** Parts 1–3 — *Framing*, *Placing*, *Dividing*. 24 cases plus three part
introductions, converted-PDF pages 12–70.

---

## 1. Two corrections to the batch inventory

Both are recorded here rather than fixed silently, because the inventory is a deliverable and a
later reader would otherwise inherit the errors.

### 1a. This is not the book the inventory selected

The file is named `The Photographer's Eye_ Graphic Guide_ Composition and Design for Better Digital
Photos.pdf`, and `CANON-003-source-inventory-and-selection.md` lists it as **"*The Photographer's
Eye*"** with the note "Composition for photography; overlaps Bang's territory from a different
craft."

Its own title page, metadata and imprint page all say otherwise:

| Evidence | Value |
|---|---|
| PDF `Title` | The Photographer's Eye: Graphic Guide (100 Cases) |
| Title page | MICHAEL FREEMAN / THE PHOTOGRAPHER'S EYE: A GRAPHIC GUIDE |
| Imprint | First published in the USA 2013 by Focal Press; © 2013 The Ilex Press Ltd |

And the book states the distinction itself, in its first sentence: *"This book takes as it's
starting point my earlier The Photographer's Eye"*. It is a later, different title by the same
author revisiting the same theme.

**Consequence:** the *selection* still stands — the photography quota asked for composition for
photography, and that is what this is. The *identification* was wrong. Corrected.

### 1b. This PDF is a calibre conversion, so it has no printed page

`/Creator` and `/Producer` are both `calibre 3.40.1`, created 2019. All 214 pages are A4. The
inventory classed this source in the group where "a visual pass can recover the actual printed page:
layout, spacing, position, before/after pairs as the reader saw them."

**It cannot.** Rendering a page here shows calibre's single-column A4 reflow — running text with the
photographs dropped in beneath at whatever size the converter chose — not Freeman's designed spread.

This was proved rather than assumed, using the book's own cross-references. The section contains
five, and **every one points somewhere else in this copy**:

| The text says | Where that case actually is | What is on the cited page |
|---|---|---|
| "square format (page 22)" | SQUARE is at page 29 | FRAME-FIT |
| "Symmetrical on page_52" | SYMMETRICAL is at page 61 | FIGURE IN A LANDSCAPE |
| "opened the last chapter (page 30)" | OFF-CENTER is at page 38 | part of SQUARE |
| "Four-square on pages 82–83" | FOUR-SQUARE is at page 95 | — |

One of the five, `page_52`, is a broken hyperlink anchor left in the running text as a literal
string with its underscore intact.

**Consequence:** the numbers on these pages are the converted file's pagination. Citing them as
printed pages would be a fabrication. **Every object in this extraction therefore carries
`page_start: null` and a locator of the form "converted-PDF page NN, CASE NAME".**

---

## 2. Text integrity — clean

Measured over the 5,748-word section: **0** tokens mixing letters and digits, **0.07%** tokens of
irregular shape (all of them the source's own hyphenated case titles). Eight pages in the whole book
carry no text, and all eight are part titles or dividers. No OCR damage; no interleaving.

---

## 3. Why this book is the batch's sharpest test of visual loss

The author states his method in the introduction, and it is a method designed to defeat text:

> "often it would have been simpler … to have bypassed words and instead relied more on a purely
> visual explanation. That's the premise here. Words to a necessary minimum, with visuals carrying
> the story."

So this is not a source where visual loss has to be inferred by comparing figures against captions.
**The author declares in advance that the words are deliberately insufficient.** Anything extracted
from text alone is known to be partial before it is written.

`visual_completeness: partial_reflowed_layout`. The good news is that the graphic deconstructions —
the diagrams that are the book's whole method — **survive in this copy**. That was the real risk and
it did not happen. What is lost is the page: photograph, analysis and caption are stacked down an
A4 column at unrelated sizes instead of composed together. Resolution is modest too, 222–975 px
wide, median 500; a 225 px analytic diagram is at the edge of legibility.

**Three findings from the pass**, in `visual-evidence-ledger.yaml`:

1. **A diagram that measures what the text only asserts.** The prose says the three placement zones
   are "approximate" and that any rule of thirds "can only be approximate". The diagram draws all
   three zones with soft gradient edges wide enough that adjacent zones visibly overlap. The word
   is an adjective; the picture is a quantity. Text keeps the claim and loses the only thing that
   makes it usable.
2. **A counterfactual the text reduces to a conclusion.** For the classical-division case the source
   manipulated its own photograph so the tonal boundaries fell on the Golden Section, showed that it
   fails, then showed the tone-equalised version that would work — plus an exploded rendering
   separating the frame's three depth planes. In text this survives as one sentence: "It doesn't
   work well, and the bright sky over-dominates." That is the conclusion with the experiment removed.
3. **A demonstration that performs itself.** The reveal case claims "it takes the eye a moment to
   slip down to the corner to notice it". Looking at the photograph, that is what happens. The
   evidence is the delay in the viewer's own looking. Text can report that the effect exists; it
   cannot produce it. This is a different loss from the others in this batch, which were losses of
   information.

A fourth observation is about triage rather than this book: **text density is a poor proxy for
content here.** Case pages carry 150–280 words; the pages after them carry 4–65 and are almost
entirely image. A pipeline that sampled or weighted by text volume would discard exactly the pages
this book puts its argument on.

---

## 4. What was produced

| File | Contents |
|---|---|
| `visual-evidence-ledger.yaml` | 4 demonstrations, 4 visual-only observations |
| `source-knowledge.yaml` | **34 objects** |
| `source-concept-systems.yaml` | 5 systems |
| `ontology-mappings.yaml` | 46 terms, 12 relationships, 5 concepts |
| `operational-bindings.yaml` | 8 bindings |

All validate against SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints.

### The object count is the useful number here

**34 objects from 59 pages, against 79 objects from 57 pages for the layout manual processed
immediately before it in this lane.** Same lane, same method, same week, almost the same section
size — and 2.3× fewer objects.

That is a clean test of the concern this lane raised after book 6, that per-book object counts might
be measuring chapter length. Here section size is held nearly constant and the counts still differ by
more than double, so **source shape is genuinely the dominant term, and section size is a real but
secondary confound.** Books cannot be compared on raw counts, but the differences are not artefacts.

The V0 granularity rule was applied unchanged and decided every case.

### The binding count and what did not fit

8 bindings against 34 objects. Most of this book has no product consumer, because most of it is
about what a photographer does with a camera before the exposure. That block is parked as
`production_candidate` and **explicitly not translated** into generative control.

Two bindings are worth flagging:

- **`bnd_fre_c003_0005` records a schema gap rather than a use.** Three of this source's claims
  describe a *traversal* of attention — the two shot where "the attention plays ping-pong between
  the two subjects" and returns, the reveal where the eye lands, lingers, wanders and discovers, the
  eccentric division that sends the eye from a sharp element to the real subject. `creative.hierarchy`
  is a ranked list. It can say the actor outranks the actress; it cannot say the eye is meant to go
  there and come back. Nothing was added; the gap is recorded.
- **`bnd_fre_c003_0004` records that `observation_unit` cannot express its own condition.** The
  source says whether a scale figure registers depends on the **print size** — one version "works
  under one condition: It has to be printed big." Every available observation_unit value describes
  how many assets are observed, not at what size. `whole_asset` is recorded as the nearest available
  value and is marked as inaccurate.

---

## 5. Historical material

**Searched after the fresh checkpoint commit**, per CANON-003's sealed-until-checkpoint rule.
Result recorded in `canon/findings/CANON-003-book07-freeman-findings.md`.
