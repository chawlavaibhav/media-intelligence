# Provenance — Light: Science & Magic, 5th ed., the chapters BEYOND chapter 3

**EXPERIMENTAL — NOT LIVE CANON.** Lane of `book-expansion-qa-v1`. Non-merge, exploratory. Nothing
in this directory is accepted Canon and nothing here may be described as accepted.

`source_id: light-science-magic-beyond-ch3` · ID prefix `lsmx`

---

## 1. Source identity

| Field | Value |
|---|---|
| Authors | Fil Hunter, Steven Biver, Paul Fuqua |
| Title | *Light: Science & Magic — An Introduction to Photographic Lighting* |
| Edition | **Fifth Edition** |
| Publisher | Focal Press (named on the copyright page of this copy) |
| Format | **EPUB, reflowable** |
| Local copy | `~/Downloads/Books/Light Science & Magic, 5th Edition.epub`, 9,692,005 bytes |
| Processed text | `scratchpad/src/EPUB-Light_Science___Magic__5th_Editi.txt`, 468,886 bytes, 20 spine documents carrying text |
| Images | extracted from the same EPUB to `scratchpad/epub/OEBPS/Images/` |

**Access basis.** The Controller authorised read-only use of this already-present local copy.
**Licence status has not been independently verified** and no claim about redistribution rights is
made here. The extraction reproduces short source terminology only; the banks are paraphrase.

---

## 2. THIS IS A SCOPE EXTENSION, NOT AN INDEPENDENT ORIGIN

```
scope_extension_of: light-science-magic-ch3
independence: none — same work
```

Chapter 3, *The Management of Reflection and the Family of Angles*, is already live Canon as
`light-science-magic-ch3` (`canon/knowledge/current/light-science-magic-ch3/`, 20 objects,
`source_id: light_science_and_magic_ch3`). **This lane is the same book by the same authors.**

Consequences, applied throughout:

- Nothing here corroborates the live chapter-3 knowledge. Agreement between this lane and
  `light-science-magic-ch3` is *one author team repeating itself*, not convergence.
- The chapter-3 theory is **not re-extracted**: the three reflection types, the angle-independence
  of diffuse reflection, the mirror-image property of direct reflection, the inverse-square
  behaviour of each, the polarization mechanism, and the definition of the family of angles are
  all live and are referenced, never restated as new knowledge. Where an object here depends on one
  of them, a caveat names the live object it builds on (by `sk_lsm_c003_*` id).
- Where a later chapter **qualifies** a chapter-3 claim — and three do — it is recorded as
  **the same authors qualifying their own earlier statement**, with `origin: source_stated` and an
  explicit note. It is never presented as two sources disagreeing. The three are listed in
  `EXTRACTION-NOTES.md` §4.

---

## 3. Span covered — chapters established by me, not by the spine markers

The `<<<SPINE n | FILE .. | TITLE ..>>>` markers in the processed text are **unreliable as chapter
titles**: the extractor took each document's *last* heading, so spine 13 (`13_Chapter04.xhtml`) is
labelled "Complex Surfaces", which is the closing section of chapter 4, not its title. The file
numbering (`NN_ChapterMM.xhtml`) is reliable and agrees with the Table of Contents at spine 7.
Chapter identity below was established from the Table of Contents and confirmed against the
chapter-opening numeral in each document.

| Spine | File | Chapter | Title | In scope |
|---|---|---|---|---|
| 10 | `10_Chapter01.xhtml` | 1 | Light: the Beginning | no — front matter, gear, "what camera do I need" |
| 11 | `11_Chapter02.xhtml` | 2 | Light: the Raw Material of Photography | no — precedes the live span; transmission/absorption/reflection basics |
| 12 | `12_Chapter03.xhtml` | 3 | The Management of Reflection and the Family of Angles | **NO — live Canon** |
| 13 | `13_Chapter04.xhtml` | 4 | **Surface Appearances** | **YES — fully** |
| 14 | `14_Chapter05.xhtml` | 5 | **Revealing Shape and Contour** | **YES — fully** |
| 15 | `15_Chapter06.xhtml` | 6 | **Metal** | **YES — fully** |
| 16 | `16_Chapter07.xhtml` | 7 | **The Case of the Disappearing Glass** | **YES — fully** |
| 17 | `17_Chapter08.xhtml` | 8 | **Making Portraits** | **partially** — only where a general optical mechanism is stated (eyeglasses and the family of angles; dark skin and direct reflection; skin's own direct reflection). Posing, styling, key/mood taxonomy and the light-by-light catalogue were refused. |
| 18 | `18_Chapter09.xhtml` | 9 | **The Extremes** (white-on-white, black-on-black) | **YES — fully**; the characteristic-curve and histogram material is labelled `technology_contingent`/`historical_claim` where it is about film or a particular sensor generation |
| 19 | `19_Chapter10.xhtml` | 10 | **Traveling Light** | **partially** — the colour-of-light mechanism (mixed vs unmixed colour, filtering the window, highlight colour after global correction) and the flash/ambient duration mechanism. The flash and LED hardware survey was refused. |
| 20 | `20_Chapter11.xhtml` | 11 | Setting Up Your First Studio | **no** — studio-space logistics and equipment shopping, refused per the extraction stance |
| 21 | `21_Appendix01.xhtml` | — | Appendix: Reliable Suppliers | **no** — supplier list, refused |

Chapters 1, 2 and 11 and the appendix were read only far enough to confirm they are out of scope.

---

## 4. Locators — Case 3 of the addendum: **there is no page**

`FORMAT: EPUB (reflowable). THERE ARE NO AUTHORED PAGE NUMBERS IN THIS FORMAT.`

- `provenance.page_start` and `provenance.page_end` are **`null` in every object in this lane**, and
  every `qa_bank` `source_locator` is chapter-plus-section. No page number is invented anywhere.
- The real locator lives in `provenance.chapter` (e.g. `6 — Metal`) and `provenance.section`
  (e.g. `Keeping the Metal Bright`), plus a `locator` string matching the live chapter-3 record's
  shape. Spine numbers are given in `EXTRACTION-NOTES.md` as a file-position aid only.
- Audit pattern recorded: **`no_authored_page`**, `recoverability: unrecoverable_in_this_copy`.
- The book cross-references its own figures by number ("look back at Figure 6.30") and, in one
  place, its own chapters by number. Figure references resolve in this copy. **No page
  cross-reference was found in the in-scope chapters**, so no unresolvable page pointer had to be
  guessed at; had one appeared it would have been noted rather than resolved.

---

## 5. Visual evidence — inspected, unlike the live chapter-3 pass

The live chapter-3 record carries `blocked_visual_validation`: the macOS privacy protection over
`~/Downloads` made the EPUB unreadable during CANON-003, and all fourteen of its figures went
unseen. **That block is gone.** The EPUB opened, and the figure images are present as
`OEBPS/Images/figN_M.jpg`.

I inspected **34 figures** from chapters 4, 6, 7 and 9 as nine labelled contact sheets, chosen to
cover every matched pair on which a claim in this lane depends. What that changes, and what it does
not, is set out in `EXTRACTION-NOTES.md` §3, including the count of objects that still carry
`extraction_uncertainty: figure_not_inspected`.

This asymmetry must be carried forward: **the live chapter-3 objects and this lane's objects do not
have the same evidential standing**, and a reader comparing them should not read
`visually_demonstrated` here as a sign that this lane was done more carefully — it is a sign that
the file opened.

---

## 6. Integrity

| Check | Result |
|---|---|
| Processed text parses, 20 spine documents | yes |
| Chapter boundaries confirmed against the Table of Contents | yes, 11 chapters + appendix |
| Figure images present for every figure cited in an object | yes, checked by filename for all cited `figN_M` |
| Sentence-level verification against the EPUB | **not repeated** — the live chapter-3 record verified 200/200 sentences against this same EPUB earlier in the project; the processed text used here is a fresh extraction from the same file, and quotations in `source_terms` were checked individually against it |

No historical Light: Science & Magic material was opened during this extraction.
