# CANON-003 book 18 — Building a StoryBrand ch.1–3: extraction findings

**Date:** 24 Aug 2026 · **Lane:** D · **Checkpoint:** `f0127e4` · **Domain:** commercial
communication / narrative framework
**Section:** Section 1 complete, chapters 1–3, ~8,900 words · **Visual completeness:**
`verified_figure_level`
**Counts:** 18 SourceKnowledge objects · 2 SourceConceptSystems · 22 terms · 8 relations ·
3 concepts · 7 operational bindings, of which **4 are Creative IR**

---

## 1. The headline: bindability and evidence quality moved in opposite directions

Books 16 and 17 produced **zero** Creative IR bindings between them. This one produced four — entity
roles, the message proposition, the call to action, and the emotional target — plus an evaluation
binding, a benchmark binding and a governance binding.

And it is the **weakest-evidenced source in the lane**. Its foundational mechanism, the claim that
attention is allocated by survival relevance and processing cost, is delivered as reported
conversation with a named friend on the author's back porch, resting partly on Maslow's hierarchy —
a mid-century model of motivation, not a finding about attention. Its results are revenue figures
with no controls and no failed cases: a client's course selling $25,000 and then $103,000 after a
rewrite, the author's own company doubling for four consecutive years. Its closing position is that
each module has set-in-stone rules that cannot be broken, and that successes which appear to break
them are using the formula invisibly — which, as stated, cannot be contradicted by any outcome.

**Why this matters more than either fact alone.** A system that ranked Canon knowledge by how well
it binds to the product schema would rank this book first in Lane D and *Light: Science & Magic* —
the most mechanism-bearing source in the batch — lower. Bindability measures how close a source's
subject is to our product's subject. It measures nothing about whether the source is right. Those
two things are recorded in different layers, which is exactly what the SPEC-03 / SPEC-04 split is
for, but nothing currently stops a later consumer from treating binding count as a quality signal.
Recorded as Lane D issue **D-13**.

## 2. The visual pass earned its keep, for the first time in this lane

Every figure in this book carries `alt="image"`. A text-only extraction recovers nothing from them.
Three things exist only in the pictures:

**The framework diagram forks, and the prose does not say so.** The text lists seven elements in
order, with "helps them avoid failure" sixth and "ends in a success" seventh. The diagram draws
them as two branches from a single junction — success rising, failure falling. They are alternative
outcomes of one decision point, not consecutive steps. A text-only reconstruction produces a
straight list of seven, and nothing in the text reveals the error.

**The output template carries a field schema the prose never states.** Under the problem: villain,
internal, external, philosophical. Under the guide: empathy, authority. Under the plan: process,
agreement. Under the call to action: direct, transitional. Plus an eighth box — Character
Transformation, with a from and a to — in a framework named for seven elements. The chapters mention
several of these pairs as forward references ("in the fourth part we'll look at two kinds of
plans"); the picture is what shows them as named slots in a form. This is the most operationally
useful content in the section, and it is the content plain text loses completely.

**The three-level problem taxonomy is demonstrated only in figures.** Chapter 3 states that
customers face external, internal and philosophical problems and gives not one example. The worked
instances — Star Wars: defeat the Empire / is he a Jedi / good versus evil — sit in a chapter 2
diagram the text never points to.

**One figure was checked and found redundant**: the nesting diagram showing one brand script above
divisions above products says exactly what the prose says. Worth recording because it shows the
loss is not uniform across a source's figures, so "this book has figures" is not by itself a measure
of exposure.

## 3. The pre-batch inventory called this book "few figures", and that was the wrong question

The source inventory, written before the batch, classified this book as EPUB with "few figures".
Numerically that is right — 36 images, against 442 in *Making and Breaking the Grid*. It is also a
poor guide to what happened here, because **figure count does not predict visual load**:

| Book | Images in file | Figures carrying an argument |
|---|---|---|
| 16 — *Creativity, Inc.* | 33 | **0** |
| 18 — *Building a StoryBrand* | 36 | **4**, two of them carrying content absent from the text |

Nearly the same count, opposite exposure. What predicts the loss is not how many pictures a book
has but **whether what it teaches is a structure** — a form with named slots, an order, a branch.
Prose is a poor container for those, so an author with a framework draws it, whatever their
discipline. Recorded as Lane D issue **D-12**.

## 4. What the framework contributed to our own schema, as a question

Two of the bindings raise questions about SPEC-01 rather than only consuming it.

**`copy.cta` may be one field where two are needed.** SPEC-01 holds a single call to action. This
source treats two as normally present and doing different jobs: a direct ask for the purchase, and a
transitional ask that continues the relationship without requesting the sale. That is a candidate
structural gap in our schema, surfaced by a source rather than by us.

**`entities.role` already has `hero`, and the two heroes are not the same thing.** SPEC-01's `hero`
marks the primary visual subject of an asset. This source's hero is the protagonist of a narrative
the customer is living. A product can be the visual subject of a shot in which the customer is
still the protagonist, so the binding constrains the *message* and must not be read as forbidding
product-led imagery. The binding's `limits` field says so explicitly. This is the closest a source
in Lane D has come to a term collision with our own vocabulary, and the schema handled it by
forcing the distinction into a field rather than letting the word carry it.

## 5. Where the source contradicts itself, and the schema held it

Three tensions, all the source's own, none resolved by it:

- The elements are "set-in-stone rules you cannot break" — stated two pages after the source says
  the elements should not be used evenly, and after conceding that some stories omit the guide.
- Stakes must be present or nothing is at issue, and stakes must be dosed like salt or the message
  is ruined, with no way given to judge the dose.
- The one technology company used as the central illustration is conceded in the same passage to be
  arguably not the maker of the best products, then used as the illustration anyway.

Recorded as a `contradicts` relation and a `conflicts` entry on the framework system. The extraction
did not tidy any of them up.

## 6. Evidence profile — and the first real departure in Lane D

| Characteristic | Book 16 (21) | Book 17 (23) | **Book 18 (18)** |
|---|---|---|---|
| `explicitly_stated` | 21 | 23 | 18 |
| `practitioner_assertion` | 21 | 23 | 18 |
| `mechanism_given` | 13 | 14 | 11 |
| `argued` | 9 | 13 | **6** |
| `anecdotal` | 4 | 6 | 3 |
| `outcome_claimed` | **0** | **0** | **4** |
| `visually_demonstrated` | **0** | **0** | **3** |
| `repeated_within_source` | 2 | 2 | **5** |
| `historical_claim` | 2 | 2 | 4 |
| `controlled_comparison` | 0 | 0 | 0 |

**Plain-English reading.** The two creative-process books argued; this one asserts and repeats. It
is the only book in the lane that claims commercial outcomes — four objects — and the only one that
demonstrates anything visually. `repeated_within_source` more than doubles, which fits a book whose
core claims are restated as slogans ("if you confuse, you'll lose") and printed as numbered
principles.

This matters for the tentative pattern noted after book 17 — that evidence profile might track
domain rather than author. **Lane D's third book breaks the similarity**, and it comes from a
different domain, which is consistent with the pattern rather than against it. Still one lane and
three books, all classified by the same extractor. Marked INFERRED and left for the integrator.

## 7. Historical comparison

**No historical extraction comparator exists.** Searched after the checkpoint `f0127e4` was
committed and pushed, on title, author surname and framework terms.

Two pre-batch planning judgements exist and both converged with the fresh result.
`CANON-COVERAGE-MAP-V0.md`, dated 23 August 2026, lists this book under **"Proposition &
positioning"** and **"CTA & response"**. The fresh extraction, which had not read that file,
produced bindings to `message.proposition` and `copy.cta` — the same two, arrived at from the text.

The same document's companion, the source inventory, called the book "few figures", which the visual
pass contradicted. Both the agreement and the disagreement are recorded; the disagreement is the
more useful one, and it is issue **D-12**.

**Contamination check:** the `canon/experiments/` documents were not read before or during any Lane
D extraction, and were found only by post-checkpoint search. The convergences are genuine.
