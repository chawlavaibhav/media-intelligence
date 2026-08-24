# Provenance record — Painting With Light, chapter 2 (CANON-003 book 8, rebalance lane)

**Book:** John Alton, *Painting With Light*, first published 1949; this file is the University of
California Press edition (ISBN 9780520275843), which reprints the 1949 text with a new
introduction by Todd McCarthy.
**Section processed:** chapter 2, "Motion Picture Illumination", complete — six sections: The Set,
Props, People, Rigging for Illumination, Lighting Equipment, and The Theory of Illumination. About
8,100 words and 56 plates.

## Why this section
Chapter 2 is the book's systematic core. It defines what lighting acts on, gives the studio's
vocabulary of light functions, states the theory — why one source is not enough, what makes an angle
good, how depth is produced, what illumination is for — and then works a complete shooting day from
rigging to the take, followed by recipes for particular hours and situations. Chapter 3, "Mystery
Lighting", is the book's famous chapter but applies this system to one genre; chapter 2 is where the
reasoning system itself is set out.

## Identity and integrity
| Check | Result |
|---|---|
| Local file | `~/Downloads/Books/Painting With Light.epub` |
| `dc:title` · `dc:creator` · `dc:publisher` | Painting With Light · John Alton · Univ of California Press |
| Identifiers | ISBN 9780520275843 · ASIN B001NCDC0Y · Google v7MwDwAAQBAJ |
| Package | 4 HTML files, 329 JPEG plates, 146 SVG files |
| Navigation | 17 entries: introduction, filmography, preface, and 14 numbered chapters, matching the book's known structure |
| Body-text integrity | Continuous; no interleaving, no dropped passage. Across the 7,923 words of chapter 2, **zero** words came out without a vowel |
| Known OCR damage | Confined to display type and technical model names: the Molarc appears as "Dlolarc" and "Morinc", Duarcs as "Duares", and two all-caps subheadings are garbled — "TILE TAKE" for THE TAKE and "M( [OONLIGIIT AND WINDOWS" for MOONLIGHT AND WINDOWS |

**The damage that matters is where it falls.** The garbles are almost all in equipment names, which
is precisely the vocabulary an extraction would want verbatim. Every instrument name used in this
extraction was checked against the source's surrounding description rather than taken from the
damaged token, and the affected objects carry `extraction_uncertainty: ocr_degraded`.

**A provenance hazard specific to this file, and the reason no page numbers appear in this
extraction.** The file's internal anchors are named `pageNNNN` — chapter 2 opens at `page0123`,
chapter 3 at `page0184`, chapter 14 at `page0523`. These **cannot be printed pages**: the printed
book runs to well under two hundred pages, so an anchor numbered 523 is a file-internal position
marker inherited from the conversion. Citing them as pages would have produced a provenance record
that looks precise and is false. All provenance in this extraction therefore cites the chapter, the
section name, and the anchor id, with the section names recovered by the visual pass.

## Visual evidence — verified at figure level, and it changed the extraction twice
`visual_completeness: verified_figure_level`. Nothing committed; all renders ephemeral.

**1. The section headings are drawings, not text.** Every chapter- and section-level heading in this
EPUB is an SVG file containing glyph outline paths — a picture of the words. In the extracted text
they are `<img>` tags with empty alt attributes. All twenty SVGs in the chapter 2–3 range were
rasterised and read; that is the only reason this record can name the chapter's six sections.

**A text-only pass would have read this chapter as one undivided block** — and worse, it would have
looked structured, because the *deeper* headings (ARC LIGHTS, THE PURPOSE OF ILLUMINATION, DEPTH,
ROUGHING IN, DAWN, SUNRISE) are ordinary text and extract cleanly. There are 39 of them. The
hierarchy survives upside down: the leaves are present and the branches are missing.

**2. The source argues by photographic minimal pairs.** Fig. 75 and Fig. 76 are the same sphere
under one light and under four — flat white disc, then a solid modelled ball. Fig. 80 and Fig. 81
are labelled Wrong and Right and show tone-matched blocks losing their edges, then tone-opposed
blocks standing clear. These are controlled comparisons in the SPEC-03 sense: one variable changed.
They are also the entire argument for two of the chapter's central claims.

**3. One demonstration stays ambiguous even after inspection.** Fig. 83 and Fig. 84 are offered for
the claim that one gives a sensation of depth and the other does not — and the text never says
which, and neither figure carries a verdict label. Recorded as `ambiguous_referent` on the
corresponding object rather than resolved by guessing.

**4. The executable content of the recipes lives in the plans.** Fig. 90 is an overhead plan of the
dawn setup with instrument types, positions, beam paths and a legend. The prose says to crisscross
several well-diffused reflectors; the diagram says how many, of what, where, at what angle. A reader
with only the text could not rig the set.

Figure captions, unlike the headings, are ordinary text and survive — including the words "Wrong"
and "Right". A text-only reader of this chapter therefore knows a minimal pair was made and cannot
see it.

## What this book contributed
**A source in which the three kinds of content age at completely different rates, interleaved within
a few pages, and indistinguishable by claim type.** The geometry does not date: one source renders a
solid flat, matching tones lose their edge, an angle reveals form. The technology dates entirely:
the instrument catalogue, the antihalo-film justification for shiny props, the rule that every
negative must be normally exposed. And one claim is a studio convention of the period stated as
technical fact — that high reflectors are unfavourable to feminine faces. All three carry
`practitioner_assertion`; only reading tells them apart. `historical_claim` and `culturally_bounded`
were applied by hand.

## Historical material
Searched after this checkpoint. Result recorded in the rebalance-lane issue file and in the findings
document for this book.
