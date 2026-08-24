# CANON-003 — Rebalance-lane issue file

**Lane:** rebalance worker, created by `canon/tasks/CANON-003-REBALANCE-01.md`
**Branch:** `work/canon-003-rebalance-d`, cut fresh from the common parallel base `4cbe257`
**Assigned books:** 8 — John Alton, *Painting With Light* · 11 — Christopher Kenworthy,
*Master Shots*

**What this file is.** New issues found by this lane during fresh extraction, in its own file
because the shared batch ledger is locked during parallel execution. It is **not** a synthesis and
does not count recurrence across lanes.

**Isolation statement, per the rebalance amendment.** No Lane A/B/C fresh findings, issue files or
checkpoints were read. The Lane D issue file and Lane D checkpoint were **not** opened or used as
extraction prompts for either of these books; they sit on a different branch which is not checked
out in this working tree. Shared starting material used: the communication standard, the CANON-003
task, the parallel-execution amendment, the rebalance amendment, the source inventory, the
pre-parallel handover checkpoint, and SPEC-01/03/04/05.

The amendment records that perfect cognitive erasure cannot be guaranteed where the same agent
identity is reused, and that the safeguard is procedural. Two things are worth stating plainly so a
reviewer can audit rather than trust: the sources were fixed before any lane result existed, and
each book's fresh extraction was committed and pushed before any historical or cross-book material
was opened. Where a finding below resembles something a reader may recognise from elsewhere, it was
reached from the source text and the reasoning is given so the derivation can be checked.

---

## R-01 — An EPUB can turn a book's heading hierarchy into pictures, and it survives inverted

**Status:** OBSERVED · **Layer:** source fidelity / visual completeness · **Books: 1**

**What it is.** In the *Painting With Light* EPUB, every chapter- and section-level heading is an
SVG file containing glyph outline paths — a drawing of the words — with an empty alt attribute. The
six section titles of chapter 2 exist nowhere in the text layer.

The chapter's *deeper* headings are ordinary text and extract cleanly. There are 39 of them.

**Why it matters.** The result is not a chapter that looks damaged. It is a chapter that looks
**flat**: 39 topics in a row, with no sign that thirteen of them belong inside one section called
"The Theory of Illumination". A text-only extractor would produce a coherent-looking, wrongly
structured reading of the chapter and have no reason to doubt it. Losing all the headings would have
been more honest than losing half of them from the top.

**Consequence if unchanged.** Any conversion that renders display type as vector art produces the
same effect, and the affected level is always the top of the hierarchy, because that is where
designed headings live. Structure recorded from such a file will be systematically too flat.

**How it was caught:** by listing image references during the visual pass and noticing that
subheadings sat under no heading. Rasterising the twenty SVGs recovered every section title.

**Proposed (not applied):** treat "headings present as images" as a checkable provenance condition
— compare the count of text headings against the count of image elements in heading positions —
and record the file's heading representation as provenance. Post-batch revision only.

---

## R-02 — A visually demonstrated claim can be under-determined *with* the figures in hand

**Status:** OBSERVED · **Layer:** visual completeness · **Books: 1**

**What it is.** Alton offers Figures 83 and 84 for the claim that "both are flat surfaces, yet one
gives a sensation of depth and the other does not". The text never says which one. Neither figure
carries a verdict label — unlike the Wrong/Right pair three pages earlier, which is labelled. Both
read as a tunnel.

**Why it matters.** The batch's working assumption about visual evidence is that inspecting the
figure recovers what the text lost. Here the figures were inspected and the claim is still not
settled, because the missing element is not the picture but the **pairing of picture to verdict**.
Recorded as `extraction_uncertainty: ambiguous_referent` rather than resolved by inference from the
neighbouring rule, which would have been a guess dressed as a reading.

**Consequence if unchanged.** Marking a source `verified` at figure level can overstate what was
recovered. A figure inspected is not the same as a claim resolved.

---

## R-03 — Three kinds of content with three different shelf lives, indistinguishable by claim type

**Status:** OBSERVED · **Layer:** evidence characteristics · **Books: 1**

**What it is.** Within a few pages, chapter 2 of *Painting With Light* states physical geometry that
does not date (one source renders a solid flat; matching tones lose their edge; an angle reveals
form), technology that has dated completely (the instrument catalogue; shiny props are wanted
*because of antihalo film*; every negative must be normally exposed), and one studio convention of
the period stated as technical fact (high reflectors are unfavourable to feminine faces).

**All three carry `practitioner_assertion`, and nothing in the schema distinguishes them.**

**Why it matters.** `historical_claim` was applied to 9 objects and `culturally_bounded` to 1, by
hand, by reading. Both fields exist and both did their job — but nothing *forced* the question, and
an extractor who did not ask it would produce a file in which a claim about optics and a claim about
1949 film stock are equally weighted and equally durable-looking.

**Consequence if unchanged.** Older technical sources will contribute claims whose validity expired
with their technology, indistinguishable from the ones that did not. The Canon is explicitly meant
to hold durable craft knowledge, and this is the failure mode that quietly fills it with the other
kind.

**Proposed (not applied):** nothing new in the vocabulary — `historical_claim` covers it. What may
be needed is a procedural step: for any source older than some threshold, require the extractor to
classify each object as technology-contingent or not, so the question is asked rather than left to
attentiveness.

---

## R-04 — Counter-evidence: figure-only visual evidence was sufficient for a diagram-argued book

**Status:** OBSERVED · **Layer:** visual completeness · **Evidence against an earlier concern** ·
**Books: 1**

**What it is.** The pre-parallel batch ledger left an explicit open question — opened here only
after this book's checkpoint was pushed — about whether figure-only visual evidence suffices for
non-layout books, noting that "a lighting diagram may survive perfectly well without its page".

For this book it does. Fig. 90 is a complete overhead lighting plan with instrument types,
positions, beam paths and a legend, fully legible with no notion of a page. The two minimal pairs
work exactly as printed. Nothing about the argument needed the page.

**Why it matters.** It bounds the earlier concern usefully: the risk in an EPUB is not "no page"
in general, it is "no page" *for a book that argues through page layout*. This book argues through
diagrams, and diagrams are self-contained. The loss that did occur here was structural — see R-01 —
and would not have been predicted by a rule about layout-argued books.

---

## R-05 — Counter-evidence: a source that polices its own vocabulary is the easy case for the ontology

**Status:** OBSERVED · **Layer:** ontology · **Evidence *for* the current design** · **Books: 1**

**What it is.** Alton writes "the key of the picture (not to be confused with keylight)". One term
is an instrument's role in a setup; the other is the lighting approach of an entire film. The
ontology records two terms joined by `distinct_from` with `confidence_basis: source_stated`.

**Why it matters.** SPEC-05 was built for near-synonyms across sources, and its worked precedent is
a source refusing an ambiguous term. Here a source pre-empts a collision **within itself**, and the
layer absorbed it with no adjustment. Recorded as a positive control: when a source does the work,
the schema simply records it, which is what should happen.

---

## R-06 — A source can pre-declare that its own claims are proposals for testing, and nothing marks it

**Status:** OBSERVED · **Layer:** source fidelity · **Books: 1**

**What it is.** Before making any of its hundred recommendations, *Master Shots* tells the reader to
test them against the opposite choice: "try it, and then try it with a short lens and see whether
you think I was right or not. What you learn from that is more important than anything I could put
in words."

**Why it matters.** That sentence changes what every later claim in the book *is*. They are
proposals offered for testing, not assertions insisted on — and the author says so first, in his own
voice, unprompted. Nothing in SPEC-03 records the difference: `claim_type` reads
`explicit_source_claim` for a claim its author has invited you to disprove exactly as it does for
one he insists on.

**What I did instead.** Recorded the stance as its own SourceKnowledge object and as an
`epistemic_stance` member of the method system, which preserves it. But a later reader has to notice
that one object among twenty to know that it conditions the other nineteen, and nothing links them.

**Consequence if unchanged.** Sources that are candid about their own confidence are recorded
identically to sources that are not, so the candour is lost precisely where it should count in the
source's favour.

**Proposed (not applied):** a source-level field for a declared epistemic stance, or a way for one
object to scope a qualification over others in the same source. Post-batch revision only.

---

## R-07 — A source can contain a claim its own production cannot illustrate, undetectably

**Status:** OBSERVED · **Layer:** visual completeness · **Books: 1**

**What it is.** Technique 8.6 of *Master Shots*, "Color Guides", argues that a strongly coloured
jacket keeps a character identifiable when blurred and distant, in a frame graded almost entirely to
one other hue. Its illustration is greyscale, and in it the background figure is a grey smudge — the
outcome the technique says colour prevents. Measurement: all 124 images in the package, roughly
2,000 samples each, **zero coloured pixels**.

INFERRED, not verified: this is the printed book's own condition rather than a digitisation
artefact. The book's diagram notation distinguishes camera from actor by white against black, which
only a monochrome book needs; "About the Images" speaks of clarity "when printed" and never mentions
colour; and the greyscale is uniform rather than patchy.

**Why it matters, and why it is not the same as the greyscale problems already known.** Nothing here
is damaged. The text is clean, the image is a legitimate greyscale photograph, and the extraction
ran without difficulty. **The loss exists only in the relation between what the section claims and
what its illustration can show.** It is invisible to any check on the file, on the text, or on the
image — it is visible only to a reader holding both at once and asking whether the picture supports
the sentence. That question is not part of the frozen visual-pass method; it happened here because
the technique's title made the mismatch conspicuous.

**Consequence if unchanged.** Claims will be recorded as `visually_demonstrated` on the strength of
a figure existing and being legible, when the figure cannot in fact carry the claim. The evidence
characteristic then overstates the support in exactly the direction that matters.

**Proposed (not applied):** during the visual pass, for each figure, ask not only "is it legible"
but "could this figure, as reproduced, discriminate the claim it illustrates from its negation".
Post-batch only.

---

## R-08 — Counter-evidence: a notation designed for the reproduction survives everything

**Status:** OBSERVED · **Layer:** visual completeness · **Evidence *for* careful source design** ·
**Books: 1**

**What it is.** The same book that contains R-07 defines its diagram notation as white arrows for
camera movement and black arrows for actor movement. Because the distinction is tonal rather than
chromatic, it survives greyscale printing, low-resolution reproduction in an EPUB, and a reader with
no colour vision. The overhead for technique 8.2 carries the entire mechanism — two crossing actor
paths and one retreating camera — in a single legible picture.

**Why it matters.** Within one book, a visual convention built to survive monochrome sits a few
pages from a technique monochrome destroys. Both were the same author's choices. **The loss is
therefore not a property of the format or of the digitisation, but of the fit between an argument
and its carrier** — which is a sharper statement than "EPUB loses visual evidence", and it points at
a different remedy: ask what a source's argument depends on, not what its file format is.

---

## R-09 — Two sources at the extremes of the same schema field, days apart

**Status:** INFERRED · **Layer:** other (evidence characteristics) · **Books: 2**

**What it is.** The two books in this lane sit at opposite ends of several fields without any
adjustment to the method:

| | Book 8 — Alton | Book 11 — Kenworthy |
|---|---|---|
| Objects | 27 | 20 |
| `argued` | 10 | **3** |
| `controlled_comparison` | **2** | 0 |
| `historical_claim` | **9** | 0 |
| `claim_type: source_interpretation` | **0** | **3** |

Alton explains and demonstrates, sometimes with genuine minimal pairs, and is heavily time-bound.
Kenworthy instructs and repeats, warrants each technique by naming a released film, and states no
thesis at all — which is why reading his chapter as a system required three interpretation objects
where Alton required none.

**Why it matters.** Both are practitioner craft books about moving-image production, written for
directors, and the schema separated them cleanly on the fields that matter without either being
forced. That is evidence the evidence-characteristics vocabulary discriminates within a domain and
not only across domains.

**Status is INFERRED deliberately.** Two books, one extractor, one day. The pattern is what the
fields are supposed to do; whether they do it consistently across extractors is the integrator's
question.

---

## Book status — rebalance lane

| Book | Status | Fresh checkpoint | Historical comparator |
|---|---|---|---|
| 8 — Alton, *Painting With Light* ch.2 | **complete, validated, pushed** | `ab2a833` | no extraction comparator; two pre-batch coverage-map judgements confirmed, one contradicted |
| 11 — Kenworthy, *Master Shots* frame + ch.8 | **complete, validated, pushed** | `2d3da5d` | no extraction comparator; coverage-map judgements confirmed on shot grammar and camera movement, contradicted on composition, and the ledger's EPUB concern refined — see R-08 |
