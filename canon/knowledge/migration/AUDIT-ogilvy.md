# Migration audit — *Ogilvy on Advertising*, ch.2

**Source file (unchanged):** `canon/ogilvy-selling-atoms.yaml`
**Old shape:** 9 atoms, 5 human notes, 1 operational

**Evidence profile carries forward.** Practitioner assertion, anecdote and uncontrolled outcome
figures. Four objects take `mechanism_absent`. The decimal confidences (0.55–0.85) are **dropped**
and replaced by characteristics — they were never calibrated and were doing authority work they
had not earned.

| Old id | Concept | New | Systems | Bindings | Evidence characteristics |
|---|---|---|---|---|---|
| og_001 | positioning_is_what_it_does_and_who_it_is_for | B C D E | procedure | `intent.objective`, `audience.who`, `message.proposition` | explicitly_stated, mechanism_given |
| og_002 | proposition_grounded_in_specific_product_fact | B C D E | procedure, proposition | `message.proposition`, `message.support` | explicitly_stated, anecdotal, outcome_claimed |
| og_003 | audience_language_precedes_copy | B C D | procedure | `audience.who`, `audience.context` | practitioner_assertion, mechanism_absent |
| og_004 | every_asset_contributes_to_one_brand_image | B C D E | procedure | `brand.palette`, `brand.type`, `creative.visual_language` | practitioner_assertion, anecdotal |
| og_005 | production_quality_register_transfers_to_product | B D E | — | `creative.visual_language` | practitioner_assertion, culturally_bounded |
| og_006 | positively_good_beats_comparative_superiority | B C D | proposition | `message.proposition` | argued, mechanism_given, **attributed to a partner, not the author** |
| og_007 | make_the_product_the_hero | B D E | — | `entities`, `creative.hierarchy` | practitioner_assertion, mechanism_absent |
| og_008 | multiple_objectives_achieve_nothing | B D E | — | `intent.objective`, `message.proposition` | practitioner_assertion, mechanism_given |
| og_009 | big_idea_five_question_test | B C E | procedure | evaluation only | practitioner_assertion, source_concedes_difficulty |
| note | advertising_can_reduce_sales | **B** H | — | — | anecdotal, outcome_claimed — see below |
| note | style_as_added_value_for_parity_products | **B** D | proposition | `creative.visual_language` | was flagged for possible promotion; now simply bound |
| note | repeat_winners_moving_parade | **B** H | — | — | out of SPEC-01 scope (campaign, not asset) |
| note | committees_cannot_create | **B** H | — | — | organisational |
| note | big_ideas_from_the_informed_unconscious | **A** | — | — | advice on a human process |

## Systems

**scs_og_001 · the_working_procedure** — `sequence`
Members in the source's own order: og_002 (study the product) → og_003 (research the audience) →
og_001 (decide the position) → og_004 (decide the image) → og_009 (test the idea).

Ogilvy presents these as ordered steps under sequential headings. Under SPEC-02 they were five
unrelated atoms and the ordering — which is most of what the chapter teaches — was not recorded
anywhere.

**scs_og_002 · proposition_strategy_by_parity** — `trade_off_set`
Members: og_002, og_006, and the recovered `style_as_added_value`.
Conditional structure: where a differentiating fact exists, build on it (og_002). Where products
are genuine parity, do not claim superiority at all (og_006) and differentiate by style. The two
principles contradict without the parity condition selecting between them.

## The promotion defect, resolved structurally

FINDINGS-07 flagged that `og_009` reached `operational` — the weakest-evidenced object in the
entire batch — purely because it proposed no new vocabulary, while `og_001` (`established`) sat
pending because it proposed one term.

Under the new architecture there is **no `operational` status to misassign**. `og_009` is
SourceKnowledge with `practitioner_assertion` and `source_concedes_difficulty`, carrying one
evaluation binding whose `evidence_basis` is `derived_from_source`. Its weakness is now recorded
in the object rather than contradicted by its status.

## A source claim that argues against our own metric

`advertising_can_reduce_sales` was discarded as a note. It is a source claim and is now
SourceKnowledge — with no binding, because it fills no field.

It is also direct counter-evidence to assumption 13 in the falsification register: Ogilvy's
opening argument is that professionally admired advertising routinely fails to sell. Our entire
evaluation design rests on human acceptance. Under SPEC-02 this was thrown away; it is exactly the
kind of knowledge that should survive.

## Counts

```
OLD                          NEW
 9 atoms                     13 SourceKnowledge objects
 5 human notes                1 human-learning-only item
 1 operational                2 SourceConceptSystems
                             14 Creative IR bindings
                              7 evaluation bindings
                              0 governance · 0 production
                              3 objects with no binding
                              9 decimal confidences dropped
```
