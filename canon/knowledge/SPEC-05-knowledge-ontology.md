# Spec 05 — Knowledge Ontology v0

**Date:** 23 Aug 2026 · **Depends on:** [SPEC-03](SPEC-03-source-knowledge.md), [SPEC-04](SPEC-04-operational-bindings.md)

## The problem this replaces

SPEC-02 required every atom to use registered failure and repair terms, with new terms held in a
pending lane. The six-source probe produced **42 failure terms and 47 repair terms with zero exact
reuse between any two sources**.

Under the old rule, seeding the registry from the first book would have forced five later sources
to distort into Molly Bang's language or fail validation. Under no rule at all,
`no_clear_entry_point`, `no_scan_entry_point` and `competing_focal_points` are three unrelated
strings and nothing ever aggregates.

Both options destroy information. So terminology is not normalised — it is **mapped**.

## The rule

**Source terminology is never overwritten.** Williams keeps `trapped_white_space`. Lupton keeps
`signal_overload`. Empirical Memory keeps whatever a model failure was actually called. A customer
rejection keeps the customer's words.

Canonical concepts sit **above** these as a navigational and aggregation layer, connected by typed
relationships. Nothing is merged. Nothing is renamed.

The precedent is in the corpus. *Light: Science & Magic* encountered exactly this: "specular" meant
direct reflection to some practitioners, small bright highlights to others, and hard light to
others again. Its resolution was not to pick a winner — it **refused the ambiguous term and named
the underlying concepts separately**, then said so explicitly in the text. That is the discipline
this spec adopts.

---

## Layer 1 — Terms (never altered)

```yaml
term_id: t_wil_0007
term: trapped_white_space
origin: source                       # source | empirical | customer | product
origin_ref: williams_non_designers_design_book
kind: problem                        # problem | remedy | property | entity
definition_in_origin_frame: >
  White space left between elements that belong together, which pushes them visually apart.
first_seen: 2026-08-23
verbatim: true                       # is this the origin's actual word, or our label for it
```

Terms from Empirical Memory and from customer rejections enter the same layer with
`origin: empirical` / `origin: customer`. **This is the join the whole architecture depends on** —
a book's predicted problem and a model's observed failure can only ever meet as two terms related
through this layer, never as one string that happens to match.

## Layer 2 — Relationships

```yaml
- {from: t_wil_0007, to: t_lup_0004, relation: potentially_equivalent_to, confidence_basis: extractor_judgement, note: "..."}
```

Relationship vocabulary:

```
maps_to                  asserted correspondence, reviewed
broader_than             the target is a special case of the source
narrower_than            inverse
related_to               connected, relationship unspecified
potentially_equivalent_to  may be the same; NOT reviewed; never treated as identity
distinct_from            explicitly checked and found different — records negative work
same_failure_family      groups under one canonical concept
same_mechanism           the underlying cause is the same
same_observed_effect     what a viewer sees is the same; mechanism may differ
uncertain                flagged, undecided
```

`same_mechanism` and `same_observed_effect` are deliberately separate. Two failures can look
identical and arise differently — which matters, because **the repair follows the mechanism, not
the appearance.**

`distinct_from` earns its place by recording that a similarity was examined and rejected. Without
it, the same false merge gets proposed every quarter. The first entry should be
`molly:flat_depth` vs `lsm:glossy_surface_reads_flat` — a string collision on "flat" with no
conceptual relationship.

## Layer 3 — Concepts, in three kinds

A concept sits above terms. Not every concept needs multiple sources — that requirement was too
blunt, and would have refused legitimate single-source generalisation.

| Kind | What it is | Independent origins required |
|---|---|---|
| `source_specific_concept` | One source's own generalisation over its own terms | **1** |
| `canonical_concept` | Our concept, used to organise and retrieve | **1** |
| `cross_source_concept` | A claim that several origins describe the same thing | **2 or more** |

### `source_specific_concept`

A source generalising its own vocabulary. *Grammar of the Shot* treats screen direction, the
180-degree rule and the 30-degree rule as one continuity geometry — that is the book's own
concept, valid with one origin, and it must not be presented as agreement between sources.

```yaml
concept_id: sc_gos_continuity_geometry
kind: source_specific_concept
origin_ref: grammar_of_the_shot
children_terms: [t_gos_0001, t_gos_0002, t_gos_0004, t_gos_0006]
origin: source_stated          # source_stated | extractor_inferred
```

### `canonical_concept`

**Ours**, created for retrieval and organisation. It makes no claim that anyone agrees. It may
group terms from one origin or several, and it is explicitly a working convenience — which is
exactly why it must be labelled as ours rather than dressed as consensus.

```yaml
concept_id: cc_focal_attention
kind: canonical_concept
label: focal_attention
purpose: retrieval_and_aggregation
created_by: extractor
asserts_equivalence: false     # a canonical concept NEVER asserts its children are the same
children_terms: [t_wil_0002, t_lup_0003, t_mb_0004]
```

`asserts_equivalence: false` is the whole point. Grouping `no_clear_entry_point`,
`no_scan_entry_point` and `competing_focal_points` under one retrieval label is useful. Claiming
they are the same failure is a different, stronger act — and that is a `cross_source_concept`.

### `cross_source_concept`

The only kind that requires **two or more independent origins**, because it is the only kind
making a claim about the world: that several sources, or a source and an observation, are
describing one thing.

```yaml
concept_id: xs_unintended_relationship_inference
kind: cross_source_concept
label: unintended_relationship_inference
definition: >
  The viewer infers a relationship between elements that the creative did not intend.

parameter: cue
children:
  - {param_value: colour,    terms: [t_mb_0011],  origin_ref: molly_bang_picture_this}
  - {param_value: proximity, terms: [t_wil_0005], origin_ref: williams_non_designers_design_book}
  - {param_value: spacing,   terms: [t_wil_0001], origin_ref: williams_non_designers_design_book}
  - {param_value: gaze,      terms: [t_gos_0002], origin_ref: grammar_of_the_shot}

independent_origins: [molly_bang_picture_this, williams_non_designers_design_book, grammar_of_the_shot]
children_are_authoritative: true
relation_types_supporting: [same_observed_effect]
mechanisms_differ: true
reviewed_by: null
status: proposed
```

Note `mechanisms_differ: true` alongside `same_observed_effect`. The four children look the same
to a viewer and arise differently. **`children_are_authoritative` is load-bearing** — aggregate
counts at the parent, but never select a repair there. Breaking a colour association and
separating two objects are not interchangeable.

An **empirical origin counts as an independent origin.** A book term and an observed model failure
related by `same_observed_effect` form a legitimate two-origin `cross_source_concept`. That is the
join the Canon and Empirical Memory are supposed to make.

### Parameterisation is permitted, not required

Some clusters parameterise cleanly. Others do not — the too-many-signals cluster spans typographic
cues, page elements and campaign objectives, and forcing a shared parameter would assert an
equivalence nobody established. A cluster with no clean parameter stays a `canonical_concept` with
`asserts_equivalence: false`, which is a normal outcome rather than an unfinished one.

## Governance

Adapted from the *Light: Science & Magic* precedent.

1. **A term is never edited to fit a concept.** Concepts adapt to terms.
2. **`potentially_equivalent_to` is not identity** and may not be used for aggregation. Promotion
   to `same_failure_family` requires human review.
3. **Refusal is a valid outcome.** Where a proposed canonical term would be ambiguous across
   communities, refuse it and keep the children — with a recorded reason, as the source did.
4. **Negative findings are recorded.** `distinct_from` is written down, not discarded.
5. **Only a `cross_source_concept` requires two or more independent origins.** A source
   generalising its own vocabulary is a `source_specific_concept`; a grouping we create for
   retrieval is a `canonical_concept` with `asserts_equivalence: false`. Neither may be presented
   as agreement between sources.

   **Independence is established from the active Audit Gate lineage records, never from a count of
   distinct `origin_ref` values.** Two source identifiers can share an author, a publisher, a
   series and a decade — *Grammar of the Shot* and *Grammar of the Edit* are Thompson & Bowen,
   Focal Press, same series, a year apart, each citing the other — so counting ids would report one
   authorial position stated twice as two sources agreeing.

   Two origins may be counted as independent only when:

   - neither source's audit record declares the other with a **dependence relation**:
     `shared_author`, `same_series`, `companion_volume` or `derivative_of`; and
   - neither carries `independence_not_established`, which blocks promotion until resolved rather
     than silently passing.

   A shared publisher (`shares_publisher_only`) or a citation (`cites_source`) **does not** by
   itself defeat independence. A source citing an unrelated source is ordinary scholarly behaviour,
   and treating a shared imprint as shared origin would refuse legitimate convergence.

   **Independence is pairwise, not a permanent global property of a source.** A source may be
   non-independent of one corpus source and a perfectly good independent origin against every
   other. A record therefore carries `not_independent_of_named_sources`, which points at the
   pairwise entries; it does not block that source everywhere.

   The mechanical form of this rule is `independent_origins_ok()` in
   `canon/validation/validate_audit_gate_v02.py`, which fails closed on an unrecognised verdict.
   The audit record schema is `canon/audit/AUDIT-GATE-v0.2.md`. Adopted by
   `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`; applied by CANON-005.
6. **Naming convention, to be decided before seeding:** the probes produced noun phrases
   (`trapped_white_space`, `jump_cut`) and sentences (`glossy_surface_reads_flat`,
   `advertiser_vocabulary_not_audience_vocabulary`) side by side. Repairs were consistently
   verb-first. Recorded as an open decision — deciding it after fifty terms sets a bad precedent
   for the next five hundred.

## Repairs use the same three layers

With one addition. The *Light: Science & Magic* probe proposed one repair term against six atoms,
because every repair it implies is a physical camera action — enlarge the source, move the light,
raise the camera, add a polariser. None is executable against a generative model.

So every repair term carries:

```yaml
executable_by: [physical_production]
# physical_production | generative_respecification | deterministic_composite |
# human_edit | unknown
```

Repairs whose only value is `physical_production` are **not translated**. Producing a generative
equivalent is a Pass 2 hypothesis and is not performed here. The field exists so the gap is
visible rather than silently bridged.

---

## What this layer does not do

It does not decide which term is right, produce one vocabulary, merge on string similarity,
delete duplicates, or compute cross-source agreement automatically. Agreement is a claim about
the world and needs review; the ontology only makes it expressible.
