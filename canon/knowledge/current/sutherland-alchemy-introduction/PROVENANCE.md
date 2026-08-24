# Provenance record — Rory Sutherland, *Alchemy*, Introduction
**CANON-003 Lane C, book 15**

**Book:** Rory Sutherland, *Alchemy: The Dark Art and Curious Science of Creating Magic in Brands,
Business, and Life*. Local copy is an EPUB. Package metadata: title *Alchemy*, creator Rory
Sutherland, publisher HarperCollins, ISBN 9780062388438, date 2019-03-21.
**Section processed:** the complete Introduction, "Cracking the (Human) Code", comprising its ten
sub-sections from "What Sticks"-style opening through "Why We Should Ignore Our GPS".

## Why this section

The Introduction is the book's epistemic statement. It defines psycho-logic, argues the case against
requiring a rationale before trying anything, sets out the nonsense / non-sense distinction, states
the two-operating-systems model and the context argument, carries the author's own field experiment,
and names the framework the rest of the book uses. Parts 1–6 apply it. This is the section that
exposes the reasoning system.

**Stated scope limits:** the prologue ("Challenging Coca-Cola"), "Rory's Rules of Alchemy" and Parts
1–6 were **not** processed. The most consequential exclusion is that the book's named framework — the
Four S-es — is announced in this section and defined outside it.

## Identity and integrity

| Check | Result |
|---|---|
| Source form | EPUB, publisher-produced text, repackaged by Calibre 3.42.0 — no OCR in the chain |
| Text quality | 12,160 words across ten files. No garbled tokens, no interior capitals, no spliced sentences, no stray page-number artifacts. |
| Section structure | All ten sub-sections present in spine order, each opening with its own heading as real text |
| Footnotes | Held in separate files and resolved where they carry content. One is load-bearing and was retrieved — see below. |
| Comparison against a print edition | **not possible.** No print copy is available locally. |

### One integrity check worth reporting in full

The section headed **"The Four S-es"** says "There are **five** main reasons... and they conveniently
all begin with the letter S" and then lists **four** items — Signalling, Subconscious hacking,
Satisficing and Psychophysics. The heading, the count and the list do not agree.

A missing fifth item would look identical to a source error, so this was checked before anything was
recorded. The whole section is 78 words; it was read in the raw file; its single footnote was
resolved and reads *"Except for the one that begins with a P."* **Nothing is missing.** The
inconsistency is in the published text.

It has **not** been silently repaired. The object records the source's wording, the discrepancy, and
the fact that the extraction was verified complete.

## Visual evidence — inspected, and this is the lane's first source with a figure that argues

`visual_completeness: not_verified_page_layout`.

Both images in the section were opened and read against the surrounding text.

- **A two-axis chart** (credited to Greg Stevenson) running FAILS↔WORKS against MAKES SENSE↔SEEMS
  WEIRD, with roughly two dozen items placed in the quadrants. **This figure carries the book's
  thesis, and almost all of its content exists only in the picture.** The prose beside it names only
  the top-right quadrant and the bicycle. Everything else — Marxism, flossing, economies of scale and
  management consultancy in makes-sense-and-fails; placebos, marketing, heuristics, evolution and Red
  Bull in seems-weird-and-works — is readable only from the image. All placements are transcribed in
  `visual-evidence-ledger.yaml`.
- **A photograph** of the Clearwater, Florida traffic circle (credited to Ken Sides), whose caption
  carries a claim the body text does not: that a central decorative fountain worsened the original
  design and a later redesign cut the accident rate.

**Loss pattern: `named_loss_with_unstated_content`.** The prose points at the figure — "this graph",
"the top-right section of this graph" — so a text-only extractor would know a figure exists and would
not miss it silently. What it would produce is the claim without any of the specific placements that
make the claim contentful. The gap is visible, and one visual pass closes it entirely.

**Why not `verified_page_level`.** An EPUB reflows; there is no page and no printed page number.
Figures were checked and both recovered, but the claim "nothing was lost from the page" cannot
honestly be made about a file with no pages. As with book 14, **every object here locates itself by
section heading rather than by page range.**

Both images are greyscale in this file. Neither carries a colour argument. **NOT VERIFIED** whether
the printed edition is in colour.

## How this source's epistemic character was preserved

This book is deliberately a heuristic, anti-rational, commercial practitioner text. It describes
itself as "a provocation, and only accidentally a work of philosophy", and it argues that things can
work without a known reason and that demanding a rationale before trying something is itself a
failure mode. The extraction records that character rather than converting it:

- **The self-characterisation is the first object in the file** (`sk_sut_alc_0001`), so it frames
  everything read after it.
- **No claim has been recorded as an experimentally established rule.** Evidence characteristics are
  dominated by `practitioner_assertion`, `anecdotal` and `argued`. `controlled_comparison` and
  `empirical_within_source` appear only where the source reports its own test — chiefly the charity
  envelope experiment and the insurance letter.
- **No mechanism has been supplied where the source supplies none.**
- **`source_uncertainty` carries real values.** This is the first book in Lane C where it does so at
  scale — `source_concedes_difficulty`, `source_hedges`, `source_asks_open_question`. Sutherland says
  outright "I have no idea why this should be" about his own strongest result, and "We don't know
  yet" about his own worked example. Those concessions are recorded, not smoothed away.
- **The implied method is recorded as a system marked `extractor_synthesis`**, with the source's
  refusal to offer a recipe stated in the interpretation basis. A source like this invites being
  silently summarised as a set of rules; doing that would turn a book that declines to offer a method
  into one that does.

Recording the character faithfully also means recording where the source contradicts itself, and it
does so three times in the processed section — warning against reasoning from hindsight and then
doing it; arguing that universal claims about human affairs are doomed and then making two; and
rejecting self-report as evidence while explaining his own behaviour by introspection. All three are
recorded at object or system level.

## What was produced

32 SourceKnowledge objects · 3 SourceConceptSystems · 22 ontology terms (8 problems, 7 remedies,
7 properties) · 10 relationships including 1 `distinct_from` · 3 source-specific concepts ·
7 operational bindings, six of them governance or evaluation. All validate mechanically against
SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints, using the same validator that
passes on the five pre-parallel books and on this lane's books 13 and 14.

## Historical material

Searched **after** this book's fresh checkpoint, per the sealing rule. Result recorded in
`canon/findings/CANON-003-lane-C-issues.md`.

## Rights

Local EPUB carrying a 2019 HarperCollins publication record. Use here is read-only, local and
internal to this research task. No page render or extract of the book is committed. **NOT VERIFIED:**
the licence status of the local file — carried forward unresolved from the batch inventory, as a
Controller question.
