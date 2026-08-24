# Finding 04 — Robin Williams, "Proximity" (Pass 1)

**Date:** 23 Aug 2026 · **Source:** The Non-Designer's Design Book, 4th ed., ch.2, book pp.15–32
**Mode:** source-only Pass 1, isolated. No vocabulary or atoms from any other source were consulted.

## Human learning notes

The chapter argues one idea: **physical closeness implies relationship**, and the rule runs both
ways — related things must be moved together *and* unrelated things must be moved apart. Williams
teaches it through before/after redesigns of ordinary commercial artefacts: a business card, a
newsletter flag, a dance postcard, a restaurant menu, a web page.

The mental model worth keeping is that **spacing is a signal, and relative spacing is the whole
signal**. Equal space between everything communicates that everything is a peer, which is almost
never true. Her diagnostic is unusually concrete: squint, count the number of times your eye
stops, and if that count is above three to five, the frame needs grouping.

Her second recurring idea is that a composition owes the viewer a **beginning and an end** — not
just an order, but a terminating point, so the reader knows they are finished rather than
scanning the corners for something missed.

## Structural finding — the source authors its own failure and repair lists

Every principle chapter closes with four named sections: *Summary*, *The basic purpose*,
*How to get it*, *What to avoid*.

`What to avoid` is a failure-mode list. `How to get it` is a diagnostic plus a repair list.
Both are written by Williams, not inferred by us.

This is the first evidence that **schema fit depends on how a source is written, not only on what
it knows**. Molly Bang required us to derive failure modes from principles; Williams hands them
over. Sources that already think in failures and repairs will populate SPEC-02 almost directly;
sources that think only in principles will need inference, and inference is where drift enters.
Worth tracking across the remaining probes.

## Counts

```
14 candidate ideas
 9 atoms      (all pending_vocabulary — registry is empty)
 5 human_notes
 0 operational
```

Nothing was promoted. Every atom proposes at least one new vocabulary term, so SPEC-02 rule 3
holds all nine at `pending_vocabulary`.

## IR-field coverage

| Field | Atoms |
|---|---:|
| `static.composition` | 5 |
| `static.typography_layout` | 3 |
| `creative.hierarchy` | 3 |
| `creative.concept` | 1 |
| `creative.visual_language` | 1 |
| `copy.headline` | 1 |

**Untouched:** everything in `intent`, `audience`, `message`, `entities`, `relationships`,
`brand`, `delivery`, `acceptance`, and the entire video extension.

`static.typography_layout` is newly covered — Molly Bang did not reach it.

## Proposed vocabulary

Failure modes (10): `ambiguous_element_association`, `competing_entry_points`,
`decoration_obscures_information`, `excessive_separate_elements`, `false_grouping_by_proximity`,
`illegible_all_caps`, `no_clear_entry_point`, `no_clear_exit_point`, `space_filling_placement`,
`trapped_white_space`

Repairs (10): `convert_caps_to_mixed_case`, `demote_competing_emphasis`,
`establish_single_entry_point`, `group_related_elements`, `increase_space_between_groups`,
`reduce_element_count`, `reduce_space_within_group`, `remove_corner_filling`,
`separate_unrelated_elements`, `subordinate_theme_to_clarity`

Proposed independently, without reference to any other source's terms.

## Flagged for human review

**1. Possible IR gap — hierarchy as a path, not a rank.**
`rw_003` says a composition must have a definite beginning *and a definite end*, and that the
viewer must know when they are finished. SPEC-01's `creative.hierarchy` is a rank-ordered list
of elements. A rank list can express "the product is noticed first" but cannot express "and the
viewer knows they have finished reading." These may be different things. Not acted on — SPEC-01
is frozen and this is a judgment call.

**2. `rw_009` may be governance rather than creative knowledge.**
"Clarity outranks thematic expression" reads less like a compositional principle and more like a
precedence rule of the kind SPEC-01 encodes in its authority ladder. Written as an atom informing
`creative.concept`, but flagged.

**3. A human_notes item describes our own pipeline.**
`group_information_before_designing` — write out which pieces of information belong together
before attempting layout. That is producing a specification before execution. It is a statement
about how the system should be built rather than knowledge the system consumes.

**4. First item that clearly belongs to Production IR.**
`reversed_type_needs_a_robust_face` is a render-method-dependent constraint. It has no home in
the Creative IR and correctly should not have one — the first extracted item where the
Creative/Production split visibly did its job rather than merely being asserted.

## Visual-context status

No unresolved items. The before/after pairs survive text extraction well enough to judge, with
one exception: the dance-postcard example (p24) relies on scattered rotated text that flattens
into unreadable order when extracted, so it was treated as text-only evidence and `rw_009` rests
on Williams's prose rather than on the figure.
