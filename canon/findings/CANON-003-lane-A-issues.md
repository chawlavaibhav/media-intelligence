# CANON-003 — Lane A issue file

**Lane A books:** 6 Samara *Making and Breaking the Grid* · 7 Freeman *The Photographer's Eye* ·
8 Alton *Painting With Light*
**Scope:** issues observed by Lane A only, under the frozen method. Not merged with the pre-parallel
batch ledger; the final integrator does that.
**Isolation:** no other lane's new findings were read. The pre-batch CANON-001/002 hypotheses that
CANON-003 explicitly inherits are used as carry-ins where relevant and are named as such.

**Counting rule:** "distinct books" counts books, not mentions. Repeated manifestations inside one
book are one book.

**Status vocabulary:** OBSERVED (directly seen) · INFERRED (reasoned from observations) ·
SUSPECTED (plausible, not established).

---

## LA-01 — Per-book object counts are not comparable, because "one representative section" is not a constant unit

**Plain English.** CANON-003 asks for a coherent representative section from each book. But sections
differ enormously in size, so the number of knowledge objects a book produces measures section
length at least as much as it measures the book. Book 6 produced **79 objects — more than the first
five books of the batch produced between them (90)** — from a 57-page section. *Grammar of the
Shot* ch.4 produced 17 from about 20 pages.

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.
**Layer:** granularity / batch method.
**New or recurrence:** new.

**What the evidence actually shows.** Normalising helps but does not remove it. Objects per printed
page is about 1.4 for Samara against 0.85 for *Grammar of the Shot* — genuinely denser, but ~1.6×
rather than the ~5× the raw counts suggest. Most of the gap is section size. The normalisation is
itself approximate: *The Vignelli Canon* is measured in two-page spreads, so its per-page figure
depends on which unit you pick.

**Consequence if unchanged.** Any end-of-batch analysis that compares object counts per book — to
judge which sources are rich, which schema areas are stressed, or how much a domain contributes —
will be partly measuring how long a chapter happened to be. A synthesis could conclude "procedural
manuals are five times denser" when the honest figure is under twice.

**Proposed only, not applied.** Record section size (printed pages and word count) alongside object
count for every book, and compare per-page. This is a reporting change, not a method change, and it
is a proposal for the synthesis to consider — CANON-003 forbids applying it during the batch.

---

## LA-02 — A delivery format with no page destroys a book that is evidence for itself, and no extraction method can recover it

**Plain English.** Some books demonstrate their argument through their own printed pages. Samara
argues for page structure and its own pages are built on a rigorous grid — the book says so twice,
citing its own baselines and its own leading measures, and one caption analyses one of its own
spreads as a worked example. In an EPUB there is no page: the format reflows. That evidence is not
degraded, it is absent.

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.
**Layer:** visual completeness.
**New or recurrence:** **new mechanism**; adjacent to the CANON-002 carry-in hypothesis that visual
evidence can disappear entirely in plain text, but distinct in cause and in what can be done about it.

**Why it is worth separating from the loss patterns already known.** The batch's earlier visual
losses were digitisation faults — a colour book scanned in greyscale, a text layer emitted out of
order. A better scan or a better extractor fixes either. **This is not a fault.** It is what the
publisher's own chosen format is. It sits upstream of every step we perform, and no change to
extraction, rendering or validation can recover it. The only remedy is a different physical copy,
which CANON-003 forbids acquiring.

**Consequence if unchanged.** For books in this class, `visual_completeness` will read
`partial_figures_only` forever, and any downstream process that treats that as "we did not look
hard enough" will be wrong. The limitation needs to be legible as permanent, not as pending work.

**Proposed only.** A visual-completeness value that distinguishes *not yet inspected* from
*structurally unavailable in this copy*. Not applied; the current vocabulary was used unchanged.

---

## LA-03 — Words typeset into artwork disappear with no signal in the text

**Plain English.** Diagram labels are often set inside the image file rather than as text. On p.28
of Samara the six worked examples of the book's modular-grid notation — 3×4, 3×6, 5×8, 5×12, 6×12,
9×14 — exist only as pixels. A text-only pass receives the notation rule stated abstractly and not
one instance of it, including the fact that its practical range runs from very coarse to very fine.

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.
**Layer:** visual completeness / source fidelity.
**New or recurrence:** new.

**Why it matters.** This is silent loss. Nothing in the extracted text is missing, malformed, or out
of order, so no integrity check catches it. It is detectable only by opening the figures — which
means the visual pass is not only recovering pictures, it is recovering *text*.

**Consequence if unchanged.** A source can appear to have been fully extracted while a named
convention, a numeric range, or a labelled taxonomy is entirely absent from the record.

**Proposed only.** None yet — one book is too thin. Watch for recurrence in books 7 and 8, both of
which are figure-led.

---

## LA-04 — Caption coverage is uneven *inside* one book, so "has a caption" is not "recovered"

**Plain English.** 11 of the 120 figure references in the Samara section carry no caption at all
(counted mechanically). One of them, f0034-01, is the positive demonstration of the book's central
image rule; the only caption on that page describes the *error* instead. Two pages earlier, p.24's
caption is nearly a complete verbal description of its figure.

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.
**Layer:** visual completeness.
**New or recurrence:** new.

**Consequence if unchanged.** An extraction that reports completeness by counting captions will
over-report on sources like this, and the figures it misses are not randomly distributed — the
uncaptioned ones here include the single most load-bearing demonstration in the section.

**Proposed only.** None. Recorded as a caution about how visual completeness is reported.

---

## LA-05 — Spatial language mostly SURVIVES reflow; the failure is narrower than expected

**Plain English.** This is evidence that **narrows** an earlier concern rather than confirming it.
14% of sentences in the Samara section (78 of 544) contain spatial references — "shown below", "the
example at top", "diagrammed here", "opposite". CANON-002 would predict a reflowed source breaks
all of it. Most of it still resolves, because the EPUB keeps figures in reading order, so "below"
reliably means "the next image".

What actually breaks is specific: references pointing **within one composite figure** ("Top /
Middle / Bottom" naming three rows inside a single image) and references pointing **across a printed
spread** ("the page structure diagram opposite").

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.
**Layer:** source fidelity.
**New or recurrence:** **evidence against a broad reading** of the CANON-002 carry-in concern about
spatially-argued sources; it does not contradict the concern, it bounds it.

**Consequence if unchanged.** A rule that treats spatial deixis as an automatic extraction risk
would flag most of this book unnecessarily. The checkable version is far cheaper: flag only deixis
whose referent is a position inside one figure or on a printed spread.

**Proposed only.** None during the batch. Offered to the synthesis as a candidate refinement.

---

## LA-06 — A source can contradict itself repeatedly, and the schema records it only in scattered pieces

**Plain English.** Six places in the Samara section state two things that cannot both hold — for
example that the grid is a closed system once built, and that a misaligned image should be fixed by
adding columns during layout; or that margins are whatever is left after the columns are fitted,
and that margins should be twice the gutter.

The schema held every one of them without strain. But the record of them is distributed: each sits
as an `extractor_observed` caveat on an individual object, and where a contradiction spans a system,
as an `origin: extractor_inferred` conflict. **There is no place that says "this source is
internally inconsistent, six times, and here is the list."**

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.
**Layer:** source fidelity / Creative IR fit.
**New or recurrence:** new.

**Consequence if unchanged.** Retrieval that returns one side of a contradiction without the other
returns advice the source itself overrides elsewhere. A reader assembling the objects one at a time
would not discover that the book disagrees with itself.

**Proposed only.** None. Note that this is arguably correct behaviour — SPEC-03 records what a
source teaches, and a contradiction is a property of the whole book rather than of any object. Two
of the six were also caught only because one section was read against another 30 pages away, which
a per-object process would not do.

---

## LA-07 — Two evidence profiles interleaved in one text with nothing marking the join

**Plain English.** Most of Samara is geometric and checkable — a measure, a count, an alignment.
Scattered through it are claims about what audiences will *infer*: that a manuscript grid reads as
authoritative, that a modular grid signifies rationalism, that symmetry reads classical and
asymmetry modern. Not one reports any audience evidence, and they are typographically
indistinguishable from the checkable claims around them. The general principle behind them is stated
only in the last of the four places, three sections after the book has twice relied on it.

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.
**Layer:** ontology / evidence interpretation.
**New or recurrence:** new. Distinct from the profiles seen earlier in the batch, which were
*uniform* per book — Ogilvy near-uniformly practitioner assertion, *Light: Science & Magic*
near-uniformly stated mechanism. Here the two sit side by side inside one text.

**Consequence if unchanged.** Weighting a source at the book level is unsafe for sources of this
kind. A rule of the form "this book is well-evidenced" or "this book is assertion" would be wrong
about half of it either way.

**Proposed only.** None. Recorded as a governance binding against `evidence_interpretation`.
Separating the two profiles here required reading every claim; no mechanical rule would have done it.

---

## LA-08 — The most exactly executable knowledge in the book is the least bindable

**Plain English.** The single largest and most precisely specified block in Samara is the derivation
that turns type specimens into a locked layout structure: find a shared width increment, take the
gutter from the running text, take margins as the remainder, force the leading measures onto a
common divisor, take row depth from where most baselines meet, then reconcile the baseline grid by
arithmetic. Every step is exactly executable. **None of it binds to anything**, because Production
IR does not exist. It is parked as `production_candidate`, untranslated.

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.
**Layer:** bindings.
**New or recurrence:** structurally the same situation SPEC-04 already documents for *Light: Science
& Magic* — knowledge whose repairs are real actions with no consumer.

**CONTAMINATION DISCLOSURE.** I have read SPEC-04, which contains the LSM production-candidate
example as a worked case. This observation is therefore **not independent convergence** with that
earlier finding; I knew the pattern before extracting. What is independent is the *cause*: LSM's
repairs are unbindable because they are physical camera and light actions, and Samara's are
unbindable because they are deterministic layout operations. Those are different reasons reaching
the same parking place.

**Consequence if unchanged.** Repeatedly, the best-specified knowledge in a source is the knowledge
today's product can do least with. If that holds across the batch it is a statement about the
product's shape, not about the Canon's.

**Proposed only.** None. Explicitly **not** translated to generative control — asking a model to
"use a 5×12 modular grid with 12-point row gutters" is a different and unevidenced claim, and this
extraction does not make it.

---

## LA-09 — Evidence FOR the frozen design (recorded so the batch is not only a fault list)

**Books:** 6 (Samara). **Status:** OBSERVED. **Distinct books:** 1.

- **The V0 granularity rule held on a source shape it had not met** — a manual whose rules arrive
  as figure captions rather than prose, one rule per illustration. It decided every case without an
  invented exception; ambiguous cases were recorded, not resolved by new policy.
- **`executable_by` expressed a repair class it was not designed for.** It exists to make the
  physical-versus-generative gap visible. Nine of this book's fourteen repairs are neither: they are
  deterministic layout operations a layout engine could execute exactly. The existing vocabulary
  covered them without addition.
- **The source/binding separation earned its keep visibly.** 79 objects of durable layout knowledge,
  12 of which today's product can use. Under SPEC-02's rule that every atom must name a Creative IR
  field, either the count would have collapsed or 67 bindings would have been invented. Neither
  happened.
- **`distinct_from` did real work.** Three negative findings recorded: hierarchic against modular
  grid; preserved negative space against awkward emptiness; the eye escaping sideways against the
  eye re-reading a line. All three are pairs a later merge would plausibly propose.
- **The evidence-characteristics vocabulary absorbed a third profile** — mixed checkable-and-inferred
  within one source — without modification.

---

## LA-10 — Most of this batch will have no historical comparator

**Plain English.** The repository's historical extraction work covers only the six original probes
(Molly Bang, Williams, Lupton, *Grammar of the Shot*, Ogilvy, *Light: Science & Magic*). Every book
selected beyond those has nothing to compare against. Samara is the third book in the batch with
`no historical comparator`, after Albers and Vignelli, and Lane A's remaining two books are
unlikely to differ.

**Books:** 6 (Samara), and by inspection of the repository the same will hold for 7 and 8.
**Status:** OBSERVED for book 6; INFERRED for the rest.
**Distinct books:** 1 confirmed.
**Layer:** batch method.
**New or recurrence:** recurrence first seen inside this batch (Albers, Vignelli).

**Consequence if unchanged.** Historical comparison is one of CANON-003's diagnostics, and it will
be available for at most six of eighteen books. Any pattern drawn from it — for instance about what
older passes catch that fresh ones miss — rests on that minority and cannot be generalised to the
batch.

**Proposed only.** None. Recorded so the synthesis does not read absence of comparison as absence
of disagreement.
