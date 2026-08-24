# CANON-003 book 11 — Master Shots, frame material and ch.8: extraction findings

**Date:** 24 Aug 2026 · **Lane:** rebalance · **Checkpoint:** `2d3da5d`
**Domain:** film directing / procedural recipe · **Section:** Introduction, How to Use this Book,
About the Images, Conclusion, and chapter 8 "Directing Attention" complete
**Visual completeness:** `verified_figure_level`
**Counts:** 20 SourceKnowledge objects · 3 SourceConceptSystems · 17 terms · 8 relations ·
3 concepts · 6 operational bindings, of which 2 are Creative IR

---

## 1. The finding: a technique whose own book cannot illustrate it

Technique 8.6 is called **Color Guides**. Its argument is that a character in a strikingly coloured
orange jacket remains identifiable while blurred and distant, because the rest of the frame is
graded almost entirely to blue — so the audience knows in a beat who is in the background.

Its illustration is greyscale. In it, the background figure is a small grey smudge on a grey beach:
**the outcome the technique says colour prevents.**

Colour saturation was measured across all 124 images in the package, roughly 2,000 samples each.
Zero coloured pixels in any of them.

**INFERRED, not verified: this is the printed book's own condition, not a digitisation artefact.**
Three things point that way. The book's diagram notation distinguishes camera movement from actor
movement by *white against black* — a choice only a monochrome book needs to make. "About the
Images" describes the frame grabs as enhanced "to greatly improve their clarity when printed" and
never mentions colour. And the greyscale is uniform across all 124 images rather than patchy.
Settling it would need a physical copy, which this task does not permit acquiring.

**Why this is a different kind of loss from the ones already in this batch.** Nothing here is
damaged. The text layer is clean, the image file is a legitimate greyscale photograph of a real
frame, and the extraction ran without difficulty. The loss exists only in the *relation* between
what a section claims and what its illustration can show — and it is visible only to someone reading
both. No mechanical check would find it, and no amount of care with the file would either.

## 2. The mirror image: the notation was designed for monochrome, and it survives everything

The same book, two pages earlier, defines its own diagram notation: white arrows for camera
movement, black arrows for actor movement. The overhead for technique 8.2 shows two black arrows
crossing — the two actors — and one white arrow leading away from the camera icon, which is the
backward dolly the text describes.

That notation is **tonal, not chromatic**, and it therefore survives greyscale reproduction, a
low-resolution EPUB image, and a reader with no colour vision. The whole mechanism of the technique
is legible in one picture.

So within one book: a visual convention deliberately built to survive monochrome, and a technique
whose argument monochrome destroys. Both were the same author's decisions. That pairing is more
informative than either half alone, because it shows the loss is not a property of the format or of
the digitisation — it is a property of the fit between an argument and its carrier.

## 3. This source states its own visual dependence, which is rare and useful

Most sources leave the extractor to judge how much of the argument lives in the pictures. This one
says so: readers are told to reconstruct each technique from the frame grabs and the overhead
diagrams **first**, and that practising that reconstruction matters more than watching the films the
examples come from.

It also states what each image type is *for*, which turns out to be necessary. Frame grabs show the
technique was used successfully before. Overhead diagrams carry the executable content — where the
camera and actors go. And the computer-graphics recreations are stated to be deliberately **not**
copies of the film frames: the differences exist to show that small changes of setup extend the
technique rather than break it.

Without that note, the renderings read as careless — the café technique is restaged on a rocky
hillside, the newsroom technique in an unrelated office. **The evidential status of a picture in this
book cannot be read off the picture.** It depends on a front-matter note, which is why the front
matter was processed as part of the section rather than skipped as preamble.

## 4. The most unusual thing in the source: it invites its own refutation

> "If, in any given chapter, I suggest that a long lens works better, try it, and then try it with a
> short lens and see whether you think I was right or not. What you learn from that is more
> important than anything I could put in words."

The author tells the reader, before making any of his hundred recommendations, to test them against
the opposite choice and decide whether he was right — and ranks the reader's own experiment above
his text.

**This changes what the rest of the book's claims are.** They are proposals for testing rather than
assertions of fact, and the source says so first. Nothing in SPEC-03 marks that: `claim_type` reads
`explicit_source_claim` for a claim the author has pre-declared as testable, exactly as it would for
one he insists on. The stance is recorded as its own object and as an `epistemic_stance` member of
the method system, which preserves it — but a later reader has to notice the object to know that it
conditions every other claim in the book.

Recorded as rebalance-lane issue **R-06**.

## 5. Where the schema fitted this source better than anything else in this lane

**The recipe form is nearly the shape of a specification field.** Each technique has a start state,
a trigger, a duration or timing constraint, a stated failure condition, and named variations. That
maps onto `VideoCreativeExtension.temporal_structure` more directly than anything else assigned to
this lane — and it exposes a real gap in SPEC-01, which currently treats a shot as an indivisible
unit with one subject. This source's whole chapter is about a shot whose subject changes without a
cut.

**Three `source_interpretation` objects, and they are the honest ones.** The chapter has no stated
thesis; each technique stands alone under its own number. Reading them as seven answers to one
question, collecting the shared success criterion, and identifying the film citation as the book's
evidential basis are all mine, and each carries an `interpretation_basis` saying so. This is the
first book in this lane to need that claim type at all — the other, Alton, states everything it
means directly and produced 27 objects with zero interpretations.

## 6. Evidence profile, next to book 8

| Characteristic | Book 8 — Alton (27) | **Book 11 — Kenworthy (20)** |
|---|---|---|
| `explicitly_stated` | 27 | 20 |
| `practitioner_assertion` | 27 | 20 |
| `mechanism_absent` | 14 | 12 |
| `mechanism_given` | 13 | 8 |
| `visually_demonstrated` | 12 | 8 |
| `argued` | 10 | **3** |
| `repeated_within_source` | 1 | **4** |
| `historical_claim` | 9 | 0 |
| `controlled_comparison` | **2** | 0 |
| `culturally_bounded` | 1 | 0 |
| `claim_type: source_interpretation` | 0 | **3** |

**Plain-English reading.** Alton explains and demonstrates; Kenworthy instructs and repeats. Only
three of Kenworthy's twenty objects argue from stated premises, and none is a controlled comparison —
what stands behind each technique is a named film in which it was used, and nothing else. That is
not a weakness the source hides: it is exactly what the front matter says the frame grabs are for.

The four `repeated_within_source` marks are the same standard restated across techniques — motivate
the move, do not let the audience notice it — which is what a recipe book does instead of arguing.

## 7. Historical comparison

**No historical extraction comparator exists.** Searched after checkpoint `2d3da5d` was committed
and pushed, on author surname and title.

Three pre-batch judgements exist, all read only after the push.

**Confirmed.** `CANON-COVERAGE-MAP-V0.md` assigns this book to "Shot grammar & shot types" and
"Camera placement & movement", both marked strong. The extraction's largest cluster is exactly that,
and its principal Creative IR binding is to a video shot's temporal structure. The parallel-execution
amendment describes it as a "procedural recipe" source shape; that is precisely what it is.

**Partially contradicted.** The same coverage map also lists it under "Composition & framing —
strong". This chapter contributes almost nothing about framing as such. It is about where attention
goes and what carries it there; the one framing instruction in seven techniques is that the start
and end of a move should each be composed as a finished shot, and the source declines to give any
rule for how.

**Refined.** The pre-parallel batch ledger recorded an issue about EPUB-sourced books losing visual
evidence, and named this book among those affected. For this book the EPUB was not the problem: the
diagrams survive intact and the notation was built to survive exactly this kind of reproduction. The
loss that did occur is (inferred) in the printed book itself, and it is chromatic rather than
spatial. Same book, listed under the right concern, for the wrong reason.

**Contamination check:** `canon/experiments/`, the batch issue ledger and all other lanes' material
were not opened before or during this extraction. The batch ledger line was read only after the
checkpoint was pushed, and only the entry the search matched.
