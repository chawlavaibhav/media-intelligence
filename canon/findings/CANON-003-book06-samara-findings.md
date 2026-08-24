# CANON-003 book 6 — Timothy Samara, *Making and Breaking the Grid*

**Lane:** A · **Fresh checkpoint:** `c8cb9d4` · **Date:** 24 Aug 2026
**Section:** chapter 1 "Making the Grid", instructional core, printed pp.20–76
**Method:** CANON-002-era frozen instrument. No schema, granularity, ontology or visual-pass
change was made or needed.

---

## 1. What this book is, and why it was worth processing

A layout manual. It teaches what a grid is made of, how to derive one from the actual content of a
project, and how to use one without producing dull work. It is the third static-design book in the
batch and the first that is primarily **procedural** — it gives step-by-step methods with
arithmetic in them, which none of the earlier books did.

Plain-English summary of what it teaches: a page has an underlying skeleton of columns and
horizontal bands; that skeleton should be worked out from the material you actually have rather
than picked in advance; and once you have it, the danger is obeying it too well.

## 2. Result

79 SourceKnowledge objects · 6 SourceConceptSystems · 53 terms · 14 relations · 6 concepts ·
12 operational bindings. All validate mechanically.

**No historical comparator exists.** Searched after the checkpoint commit. The only mentions of
Samara anywhere in the repository are in the CANON-003 task and planning files. Recorded as
`no historical comparator` rather than manufacturing one. This is the third such book in the batch,
after Albers and Vignelli.

## 3. The object count, and what it means for the batch

**This one book produced 79 objects. The first five books of the batch produced 90 between them.**

That is not a method change. The V0 granularity rule was applied unchanged and decided every case
without an invented exception. Two things explain it, and both are properties of the source:

- **It is a rule-dense procedural manual.** Most claims are imperative rules attached to a named
  element — set the gutter from the running text, hang bullets outside the alignment, add columns
  rather than move the image. Each is independently contradictable, which is exactly the test the
  V0 rule applies.
- **The source itself does the splitting.** A large share of these rules are figure captions: one
  rule, one illustration, one caption. Page 37 alone carries six separate text-setting exceptions,
  each with its own picture. Merging them would have been our decision, not the book's.

Section size is the other half. This section is 57 printed pages against roughly 20 for *Grammar of
the Shot* ch.4. Per printed page the density is about 1.4 objects against 0.85 — genuinely higher,
but by far less than the raw counts suggest.

**Why this matters beyond this book.** It means per-book object counts across CANON-003 are not
comparable without knowing the section size, and "one coherent representative section" is not a
constant unit of work. Any later synthesis that counts objects per book as a measure of anything
will be measuring section length as much as source richness. Logged as a batch issue; nothing was
changed to compensate.

## 4. A new kind of visual loss: the format has no page

CANON-002 established that plain text can destroy a spatially-argued source. This batch has since
seen two mechanisms: Albers, where a colour book was digitised in greyscale, and Vignelli, where a
full-page graphic pushed a whole named section out of order in the text layer.

This book adds a third, and it is different in kind from both.

**The book argues for page structure, and its own pages are evidence for its argument.** It says so
directly, twice, citing itself — "the baselines of text positioned in adjacent columns should align
horizontally with each other (as they do in this book)" and "the leading measures of the text
styles used in this book are multiples of 2.1". One caption on p.21 analyses one of the book's own
spreads as a worked example.

In the EPUB, none of that is inspectable. An EPUB reflows: there is no page. The self-demonstration
is not degraded — it is absent.

**Why this is worth separating from the other two.** Albers and Vignelli were digitisation faults;
a better scan or a better text extractor would have fixed either. This is not a fault at all. It is
what the publisher's own chosen delivery format is, it is upstream of every extraction step we
perform, and **no extraction method can recover it.** The only remedy would be a different physical
copy, which CANON-003 forbids acquiring.

### Two further visual findings

**Some of the words are pixels.** Diagram labels are typeset into the artwork. The six modular-grid
notations on p.28 — 3×4, 3×6, 5×8, 5×12, 6×12, 9×14 — exist only inside the image file. A text-only
pass receives the notation rule stated abstractly and not one of its worked instances, including
the fact that the notation's practical range runs from very coarse to very fine. Nothing in the
text signals that anything is missing. It is detectable only by opening the figures.

**Caption coverage is uneven inside one book.** Counted mechanically: 11 of the 120 figure
references in this section are followed by no prose at all. One of them is f0034-01 — the positive
demonstration of the book's central image rule, showing twenty image blocks all on their guides
while overlapping, crossing the gutter and bleeding off the page. The only caption on that page
describes the *error* instead. Two pages earlier, p.24's caption is nearly a complete verbal
description of its figure.

So the amount of a figure recoverable from text varies figure by figure **within one source**. An
extraction that treated "has a caption" as "recovered" would over-report completeness here.

### One earlier concern refined rather than confirmed

14% of sentences in the section (78 of 544) carry spatial deixis — "shown below", "the example at
top", "diagrammed here", "opposite". The expectation from CANON-002 would be that a reflowed source
breaks all of it.

It does not. Most still resolves, because the EPUB keeps figures in reading order, so "below"
reliably means "the next image". What actually breaks is narrower: deixis pointing **within a
single composite figure** ("Top / Middle / Bottom" on p.32, naming three rows inside one image) and
deixis pointing **across a printed spread** ("the page structure diagram opposite" on p.22).

That is a more useful and more checkable statement than "spatially-argued sources cannot be trusted
in text", and it is evidence that partially narrows an earlier worry rather than confirming it.

## 5. Product-schema fit — the best in the batch so far, and still mostly unbound

12 bindings against 79 objects. Most of the book does not reach a product field, which SPEC-04 says
is the normal state.

Where it does reach one, the fit is unusually direct. SPEC-01's `StaticCreativeExtension` names
three things — `typography_layout`, `spatial_hierarchy`, and a `composition` field covering depth
and figure-ground — and this book is about exactly those three. It supplies a closed vocabulary for
the first (columns, gutters, flowlines, rows, modules, zones, markers), the construction and
purpose of the second (spatial zones with assigned roles), and for the third something the field
otherwise has no vocabulary for: a set of **structural** determinants of apparent depth in a flat
typographic composition, rather than pictorial ones.

**Two claims are mechanically checkable, which is rare in this corpus.**

- Whether an element's edges land on the structure's guides is measurable, given the grid.
- Whether a line of continuous text runs 50–80 characters is countable.

Both come with real limits, recorded in the bindings. The alignment check is decidable only if the
grid is supplied — inferring it from the layout is the source's own method for *deriving* a grid
and is not reliable in reverse. And the bare rule would flag as failures at least four things the
source explicitly permits. The character count is scoped by the source's own footnote to English,
and the number is asserted with no derivation and no study.

**The largest usable block is deliberately not translated.** The derivation from type specimens to a
locked baseline grid — universal width increment, gutter from running text, margins as remainder,
leading forced onto a common divisor, row depth from where baselines meet, baseline grid reconciled
by arithmetic — is the single most substantial and most exactly executable thing in the book. Every
step is a deterministic layout operation and none is a generation action. Production IR does not
exist, so it is parked as `production_candidate` in the source's own frame. Asking a model to "use
a 5×12 modular grid with 12-point row gutters" is a different and unevidenced claim and this
extraction does not make it.

## 6. A repair profile the batch has not seen, absorbed without schema change

*Light: Science & Magic* produced repairs that were all physical camera and light actions —
`executable_by: [physical_production]` — and therefore untranslatable.

This source produces the opposite extreme. Nine of its fourteen repair terms are geometric
operations on a structure: add a subdivision, hang a character, set a measure, multiply a base
column. They carry `executable_by: [deterministic_composite]` — a layout engine could execute them
exactly, with no model and no judgement.

**The existing SPEC-05 vocabulary covered this without addition.** That is evidence *for* the
current design, and it is worth stating positively: the `executable_by` field was introduced to
make the physical/generative gap visible, and it turned out to also express a third profile it was
not designed for.

## 7. Internal contradictions found in the source, recorded rather than resolved

Six places where the book states two things that cannot both hold. None was repaired; all are
recorded as caveats on the objects and as `conflicts` in the systems.

| The source says | And also says |
|---|---|
| The grid is a **closed system** once developed (p.42) | If a misaligned image looks better, **add columns or rows** so the position becomes an alignment (p.34) |
| Lateral margins are **whatever remains** after the columns are fitted (p.48) | The margin should be about **twice the gutter** (p.50) |
| …and margins are a **remainder** | Folios and runners **usually force the margin measure to increase** (p.40) |
| Paragraph breaks **need not** land on row guidelines (p.37) | The baseline grid must lock all text to an increment landing on **every** row and row-gutter guide (p.51) |
| Open, unfilled space must be **maintained for visual rest** (p.64) | An **awkwardly empty** negative space should be activated with a dot (p.41) |
| Violation works because it is **occasional and surprising** (p.72) | A structure can be designed for **constant** transgression (p.73) |

The schema held all six without strain. Each sits as an `extractor_observed` caveat on the object
and, where it spans a system, as an `origin: extractor_inferred` conflict — visibly ours, not
presented as something the source noticed.

**One conflict is the source's own and is recorded as `source_stated`:** forcing every text style's
leading onto a common divisor changes the interline spacing the book has just established as
optimal for reading. The book concedes it in a footnote and does not say which requirement wins.

## 8. Two evidence profiles interleaved with nothing marking the join

Most of this book is geometric and checkable — a measure, a count, an alignment. Scattered through
it are claims about what audiences will infer:

- a manuscript grid reads as historical, authoritative, institutional or formal;
- a modular grid signifies Bauhaus and Swiss rationalism, and is sometimes chosen for that on
  projects whose content does not need one;
- symmetry reads classical and authoritative, asymmetry modern and casual — with a one-sentence
  historical derivation compressing premise, causal step and conclusion into a figure caption;
- structure itself can be a message, read culturally, historically and associationally.

**Not one reports any audience evidence**, and they are typographically indistinguishable from the
checkable claims surrounding them. The general principle is stated only in the last of the four
places, three sections *after* the book has twice relied on it.

Weighing a source that mixes the two is a different problem from weighing one that is uniformly
assertion (Ogilvy) or uniformly mechanism (*Light: Science & Magic*). Recorded as a governance
binding against `evidence_interpretation`. Separating them here required reading every claim; no
rule would have done it.

## 9. Evidence *for* the current design

- The **V0 granularity rule held again**, on a source shape it has not met: a manual whose rules
  arrive as captions rather than prose. No invented exception; ambiguous cases were recorded, not
  resolved by new policy.
- **The evidence-characteristics vocabulary absorbed a third profile** without addition, alongside
  Ogilvy's practitioner assertion and LSM's stated mechanism.
- **`executable_by` expressed a repair class it was not designed for**, as above.
- **The source/binding separation earned its keep visibly here.** 79 objects of durable layout
  knowledge, only 12 of which today's product can use. Under SPEC-02's rule — every atom must name
  a Creative IR field — either the count would have collapsed or 67 bindings would have been
  invented. Neither happened.
- **`distinct_from` did real work.** Three negative findings were recorded: hierarchic against
  modular grid, preserved negative space against awkward emptiness, and the eye escaping sideways
  against the eye re-reading a line. All three are string-similar or concept-adjacent pairs that a
  later merge would plausibly propose.

## 10. What remains uncertain

- Whether the object-count disparity is a source-shape effect or partly an artefact of a larger
  section. Measured per printed page it shrinks from ~5× to ~1.6×, but one comparison book is
  measured in spreads and one in pages, so the normalisation is itself approximate.
- Whether "the delivery format has no page" recurs. It will apply to every EPUB in the batch, but
  it only *matters* where the book's own layout is evidence for its claims. That is true of this
  book and of Lupton; it is probably not true of a prose-led source.
- Whether the two mechanically checkable claims survive review. Both are asserted without study.
  Countability is not the same as correctness, and this extraction records only that they can be
  checked, not that checking them is worth doing.
