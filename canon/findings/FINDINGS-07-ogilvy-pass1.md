# Finding 07 — Ogilvy on Advertising, ch.2 (Pass 1)

**Date:** 23 Aug 2026 · **Source:** Vintage 1985 (text 1983), ch.2 "How to produce advertising that sells"
**Mode:** source-only Pass 1, isolated. EPUB single-column, extracted clean — no interleaving.

## Human learning notes

Ogilvy's chapter is a working procedure. Study the product until a specific fact surfaces. Find
out how the audience actually talks about the category and what would make them buy. Decide the
**position** — his definition is the two-part one: *what the product does, and who it is for*.
Decide the **image**, since every asset contributes to one accumulating personality and must stay
consistent for years. Then find a **big idea**, tested against five questions, the hardest being
"could it be used for thirty years?"

Two rules cut against each other productively. Where a real differentiating fact exists, build the
proposition on it. Where products are genuine parity, do not claim superiority at all — convince
the buyer your product is *positively good*, because certainty about one beats an unverifiable
comparison between two.

And: make the product the hero. Multiple objectives achieve nothing.

## Evidence profile — the important finding

Ogilvy's support is **practitioner assertion, anecdote, and uncontrolled outcome figures**. Sales
rose from 10,000 to 40,000; the campaign still runs 25 years later. No controls, no mechanism,
often no stated reason at all — four atoms below record `mechanism: "Not stated."` The source is
candid about this: it asks forgiveness for "the dogmatism of my style."

So this probe's atoms sit at `supported_extrapolation` and `hypothesis`, confidence 0.55–0.85.
The design sources in this batch sat at `established`, 0.7–0.95.

**Architectural implication.** The Canon will hold knowledge of radically different evidential
quality under one schema. SPEC-02 records `evidence_class` and `confidence`, but nothing in the
architecture yet *consumes* them — retrieval as designed would hand a 0.55 hypothesis to the
planner with the same authority as a demonstrated principle. Flagged, not acted on.

## Counts

```
14 candidate ideas
 9 atoms
   1 operational        (og_009)
   8 pending_vocabulary
 5 human_notes
```

## The promotion rule misfires here — flag

`og_009`, the five-question big-idea test, reached `operational`. It is the **weakest-evidenced
atom in the entire batch** — `evidence_class: hypothesis`, confidence 0.55, mechanism not stated,
and the source itself concedes that recognising a good idea is "horribly difficult."

It was promoted because it proposes no new failure or repair vocabulary. Meanwhile `og_001`
(positioning, `established`, 0.85) sits at `pending_vocabulary` because it proposed one term.

**Status is currently determined by vocabulary novelty, not by knowledge quality.** That is a
real defect in SPEC-02 rule 3 as written — it was designed to protect the taxonomy, and it is
being read as a quality gate it was never meant to be. Not fixed; SPEC-02 is frozen.

## IR-field coverage

| Field | Atoms |
|---|---:|
| `message.proposition` | 5 |
| `intent.objective` | 3 |
| `audience.who` | 2 |
| `creative.visual_language` | 2 |
| `brand.*` | 1 |
| `entities` | 1 |
| `creative.concept` | 1 |
| `creative.hierarchy` | 1 |
| `audience.context` | 1 |
| `message.support` | 1 |

First source in the batch to reach `intent`, `audience`, `message`, `brand` or `entities` at all.

**Still untouched across all five sources:** `delivery`, `acceptance`, `creative.hook`,
`video.dialogue_intent`.

## Proposed vocabulary

Failure modes (8): `advertiser_vocabulary_not_audience_vocabulary`,
`generic_claim_without_product_fact`, `image_quality_mismatch`, `inconsistent_brand_image`,
`objective_overload`, `position_unstated`, `product_not_hero`, `superiority_claim_on_parity_product`

Repairs (8): `align_to_established_brand_image`, `ground_proposition_in_product_fact`,
`promote_product_to_hero`, `raise_production_quality_register`, `reduce_to_single_objective`,
`restate_as_positive_claim`, `restate_in_audience_language`, `state_position_explicitly`

## Also flagged

**1. `og_007` confirms the `entities` schema independently.** "Make the product the hero" is
exactly `entities[].role: hero`, arrived at from a 1983 advertising text.

**2. Second source with genuine internal tension.** `og_002` (build on a differentiating fact)
and `og_006` (never claim superiority on parity products) contradict unless scoped by whether a
differentiating fact exists. Carried in `exceptions` on both atoms, cross-referencing each other.

**3. One human_note may deserve promotion.** `style_as_added_value_for_parity_products` — where
products are undifferentiated, the style of the advertising *is* the differentiation. Held out
because as stated it is an economic argument rather than a rule for an asset, but it plausibly
informs `creative.visual_language`. Judgment call, left for review.

## Visual-context status

None required. Advertisements appear as plates with captions; no atom depends on reading one.
