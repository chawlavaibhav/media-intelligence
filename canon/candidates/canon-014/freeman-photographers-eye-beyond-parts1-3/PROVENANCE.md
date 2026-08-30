# Provenance — Freeman, *The Photographer's Eye: A Graphic Guide*, Parts 4–10

**EXPERIMENTAL — NOT LIVE CANON.** Lane of `book-expansion-qa-v1`. Nothing in this directory is
accepted Canon and nothing here may be described as accepted.

---

## 1. Source identity

| Field | Value |
|---|---|
| `source_id` | `freeman-photographers-eye-beyond-parts1-3` |
| Author | Michael Freeman |
| Title | *The Photographer's Eye: A Graphic Guide* |
| Publisher | Focal Press (Taylor & Francis), first published USA 2013; conceived, designed and produced by Ilex Press Ltd |
| ISBN | 978-0-240-82426-0 (pbk) · 978-0-240-82460-4 (ebk) |
| Local copy | `/Users/vaibhavchawla/Downloads/Books/The Photographer’s Eye_ Graphic Guide_ Composition and Design for Better Digital Photos.pdf` |
| Extracted text | `scratchpad/src/PDF-photographers-eye.txt` |
| SHA-256 (PDF) | `a06d1dc36b12e5dddf4332cf8c7c97899dfc131a67bc76d7300065fdda527eaf` |
| Bytes | 13,124,759 |
| Delivery format | **converted PDF** — `/Creator` and `/Producer` both `calibre 3.40.1`, 214 uniform A4 pages |

---

## 2. Scope extension — this is NOT an independent origin

```yaml
scope_extension_of: freeman-photographers-eye-graphic-guide
independence: "none — same work"
```

The live Canon source `freeman-photographers-eye-graphic-guide` covers **Parts 1–3**
(*Framing*, *Placing*, *Dividing*), 24 cases plus three part introductions, converted-PDF
pages 12–70. **That span was not re-extracted here and is not the subject of any object or Q&A
item in this directory.**

This lane is the same book, the same author, the same edition and the same physical file.
It corroborates nothing. Where an object here relates to a live Part 1–3 claim, the relation is
**one author's book relating to itself**, never two sources agreeing.

---

## 3. What this lane covered, and what it did not

The book's own contents page names ten parts. Established from the file, not assumed:

| Part | Title | Converted-PDF pages | Cases | Status |
|---|---|---|---|---|
| I | Framing | 12–24 | 10 | **live Canon — not touched** |
| II | Placing | 31–47 | 8 | **live Canon — not touched** |
| III | Dividing | 55–70 | 6 | **live Canon — not touched** |
| IV | Graphics | 71–92 | 8 + intro | **covered, all 8 cases** |
| V | Viewpoint | 93–114 | 9 + intro | **covered, all 9 cases** |
| VI | Optics | 115–139 | 10 + intro | **covered, all 10 cases** |
| VII | Motion | 140–155 | 7 + intro | **covered, all 7 cases** |
| VIII | Color | 156–172 | 7 + intro | **covered, all 7 cases** |
| IX | Juxtaposing | 173–191 | 8 + intro | **covered, all 8 cases** |
| X | Combining | 192–207 | 7 + intro | **partially covered — see below** |
| — | Index | 208–214 | — | **not extracted; apparatus, and its page numbers are unusable (§4)** |

**Part 10 is the one part not fully mined, and deliberately.** Four of its seven cases
(COLLAGE, COMPOSITE, GRAPHIC COMPOSITE, PRACTICAL COMPOSITE) spend most of their words on
Photoshop layer operations — Multiply and Lighten blend modes, eraser-brush blending, cloning,
exploded layer stacks. Those are **software/post-processing steps and were refused** under the
lane's extraction stance. What was taken from Part 10 is only the transferable compositional
material: what holds a collage together, the vertical mountain-water form, why a sequence can
merge into one frame, why a body of work needs treatment variety, and Freeman's own
declared-versus-undeclared position on manipulation.

Also refused across the whole span, per the lane stance:

- **Camera-settings recipes with no stated reason** — bare ƒ-stop and shutter values were kept
  only where Freeman gives the reason (ƒ/32 in HORIZONTAL LINES and STACKING, both of which he
  argues for and both of which he says cost something).
- **Gear notes** — "my old 180mm lens," Panavision body, the ILM shoot's equipment.
- **Pure image description with no transferable principle** — location, date and travel anecdote
  (the Stonehenge helicopter permission, the Dinka cattle, the Burmese festival calendar).

---

## 4. The page-number problem — the governing hazard of this source

**The extracted text file's own header is wrong and must not be trusted.** It reads:

```
PAGE MAPPING DETECTED: printed page = PDF page - 0 (folio agreement on 302 pages).
USE THE PRINTED NUMBER IN LOCATORS.
```

That is a folio detector matching calibre's own injected page numbers against calibre's own
pagination and finding, unsurprisingly, perfect agreement. **There is no authored page here.**
The live audit record for this book states it directly: `delivery_format: converted_pdf`,
`page_addressability: converter_pages_not_authored`, loss pattern `false_page_affordance`.

The live extraction proved it on Parts 1–3 using five internal cross-references. **This lane
found eight more in Parts 4–10, and every one of them is also wrong in this copy:**

| Where | What the text says | Where that case actually is |
|---|---|---|
| CIRCLES | "implied triangles (see pages 72–73)" | TRIANGLES is at converted-PDF page 84 |
| RHYTHM | "a shift lens, also—see pages 92–93" | SHIFT is at converted-PDF page 133 |
| DISTANT | "one of them is on pages 162–163" | the telephoto-distance case (STACKING) is at converted-PDF page 181 |
| COUNTER FOCUS | "Selective and Color-wash earlier, on pages 106–111" | SELECTIVE 121, COLOR-WASH BACKGROUND 123, COLOR-WASH FOREGROUND 125 |
| MUTED | "the Shakers, last visited on pages 60–61" | the Shaker plate is at converted-PDF page 70 |
| THEME | "the 'looking through' shot on pages 90–91" | LOOKING THROUGH is at converted-PDF page 104 |
| CONTRAST | "a color theme, as on pages 146–147" | THEME is at converted-PDF page 165 |
| LAYERING | "focus blending (pages 104–105)" | IMPOSSIBLY DEEP is at converted-PDF page 119 |
| PRACTICAL COMPOSITE | "see Frame Break, pages 18–19" | FRAME BREAK is in the live Part 1 span, not at 18–19 of this file |

Nine for nine. The book's own index (converted-PDF pages 208–214) fails the same way — it lists
"-wash (background) 108–109" where COLOR-WASH BACKGROUND is at converted-PDF page 123.

**Consequences applied throughout this directory:**

1. Every page citation is written **`converted-PDF page N`**, using exactly that phrasing.
   The strings `p. N`, `pp. N`, `printed p. N` and `page N` appear nowhere as a locator.
2. `provenance.page_start` and `provenance.page_end` are `null` in **every** object.
3. The **case title is the primary locator**. These are the source's own hyphenated headings
   (HORIZONTAL LINES, COUNTER FOCUS, ACTION COINCIDES). A case title plus a converted-PDF page
   is the strongest locator this copy can carry, and it is what every `source_locator` uses.
4. **No cross-reference in the book's text was resolved and no number from one was repeated as
   if valid.** Where an object or Q&A item needs to point at another case, it points at the
   case *title* — because the book's title-level references are correct even though its
   page-level references are not. MID-AIR's "In Chapter 2 there was a special kind of framing
   that I called 'Just'" is right; JUST is in Part II. Only the numbers are broken.

---

## 5. Text integrity

Measured over converted-PDF pages 71–207: **14,177 words**. Twenty-two tokens mix letters and
digits and twenty-one of them are legitimate — focal lengths (`65mm`, `400mm`, `21mm`), a film
size (`4x5-inch`), an aperture (`ƒ/32`), an aircraft designation (`SR-71`). The twenty-second,
`tw0-dimensional` on converted-PDF page 189, is a real defect but it is a **typesetting error in
the source**, not conversion damage — it appears in the rendered page as printed. No column
interleaving, no OCR degradation. Eight pages in the whole book carry no text and all eight are
part titles or dividers.

`extraction_uncertainty: ocr_degraded` is therefore used nowhere in this lane.

---

## 6. Visual loss — `figure_semantic_binding_lost`

The author declares in his introduction that the words are deliberately insufficient: *"Words to
a necessary minimum, with visuals carrying the story."* Anything taken from text alone in this
book is known in advance to be partial.

The conversion destroyed the designed spread. Rendering any case page shows a single A4 column
of running text with the photographs and analytic diagrams dropped in beneath at unrelated
sizes — not the facing-page composition of photograph, deconstruction and caption that the
argument actually is. **Sixteen pages were rendered at 100 dpi and looked at** for this lane;
what they support and what they do not is set out in `EXTRACTION-NOTES.md` §4, with the honest
unverified fraction.

One case makes the hazard explicit from inside the source. In TILT, Freeman writes that the
principle *"becomes difficult to describe in words, so I'll let the illustrations tell the
story."* That sentence is recorded as its own object.

---

## 7. Access basis and licence

The Controller authorised **read-only** use of a copy already present on this machine at the
path above. No copy was made, moved or redistributed; no long passage is reproduced in any file
in this directory. **Licence status is not independently verified** — this lane did not and
cannot confirm how the local copy was obtained or what rights attach to it. The extraction is
paraphrase with short terminology quotation only.

---

## 8. What was produced

| File | Contents |
|---|---|
| `source-knowledge.yaml` | 53 SourceKnowledge objects |
| `source-concept-systems.yaml` | 5 SourceConceptSystem objects |
| `operational-bindings.yaml` | 12 bindings |
| `ontology-mappings.yaml` | 58 terms, 16 relationships, 6 concepts |
| `qa-bank.yaml` | 58 Q&A items |
| `EXTRACTION-NOTES.md` | method, hazards, refusals, self-check results |
