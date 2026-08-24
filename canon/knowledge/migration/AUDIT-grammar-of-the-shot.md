# Migration audit — *Grammar of the Shot*, ch.4

**Source file (unchanged):** `canon/gos-continuity-atoms.yaml`
**Old shape:** 10 atoms, 3 human notes, 2 operational

| Old id | Concept | New | Systems | Bindings | Note |
|---|---|---|---|---|---|
| gos_001 | frame_edges_are_directional_references | B C D | geometry | `video.continuity_requirements`, `static.composition` | foundation of the chain; was `operational` |
| gos_002 | continuity_of_screen_direction | B C D E | geometry | `video.continuity_requirements`, `video.temporal_structure` | `observation_unit: shot_pair` |
| gos_003 | lines_of_attention_establish_spatial_relations | B C D E | geometry | `relationships`, `video.continuity_requirements` | genuine `relationships` binding — see below |
| gos_004 | axis_of_action_180_degree_rule | B C D E | geometry | `video.continuity_requirements` | `observation_unit: sequence` |
| gos_005 | line_violation_is_invisible_until_assembly | B C E | geometry | evaluation only | **shapes the evaluator** — see below |
| gos_006 | thirty_degree_rule | B C D E | geometry | `video.temporal_structure` | `observation_unit: shot_pair` |
| gos_007 | reciprocating_imagery | B C D E | matching | `video.continuity_requirements` | `observation_unit: shot_pair` |
| gos_008 | outside_in_shot_progression | B C D | matching | `video.temporal_structure`, `video.temporal_hierarchy` | source calls it tradition; was `operational` |
| gos_009 | eyeline_match_setup_and_payoff | B C D E | matching | `video.temporal_structure`, `relationships` | `observation_unit: shot_pair` |
| gos_010 | continuity_of_action_across_takes | B D E | — | `video.continuity_requirements` | |
| note | shoot_coverage_to_give_the_editor_choices | **B** G | — | production_candidate | was discarded |
| note | minimise_take_count_for_cost | **B** G | — | production_candidate | was discarded; cost modelling |
| note | shot_type_information_roles | **B** H | — | — | was discarded; restated from ch.1, attribution incomplete |

## Systems

**scs_gos_001 · continuity_geometry** — `causal_model`
Members, in dependency order: gos_001 → gos_003 → gos_004 → gos_002 → gos_006, with gos_005 as
the detection property of the whole.

This system has genuine **dependencies**, not just interaction. Frame edges supply the directional
frame. Sight lines create the axis. The axis constrains camera placement. Screen direction is what
that constraint preserves. The 30-degree rule operates inside the arc the axis defines. Retrieved
alone, "stay within 180 degrees" is a rule with no stated referent — the line it refers to is
defined two atoms upstream.

**scs_gos_002 · shot_matching_for_the_edit** — `interacting_set`
Members: gos_007, gos_008, gos_009.

## Evaluation is where this source pays

Six of ten objects carry evaluation bindings, and **every one of them requires more than one
shot**. `gos_005` states it outright: a crossed action line is invisible within any single shot and
appears only on assembly.

Under SPEC-02 this was an atom whose `informs` was `video.continuity_requirements` — a Creative IR
field — even though what it actually constrains is **the shape of the evaluator**. SPEC-04's
`observation_unit` field exists because of this source:

```
gos_002  shot_pair      gos_004  sequence
gos_006  shot_pair      gos_007  shot_pair
gos_009  shot_pair      gos_005  shot_pair
```

Six evaluation bindings, zero at frame level. An evaluator built to score frames independently —
the obvious first design, and the one Finding 01 exercised — is structurally unable to detect any
of them.

## A genuine `relationships` binding

`gos_003` and `gos_009` bind to SPEC-01's `relationships` and **should**. Sight lines are
attention directed from one entity to another — exactly `{subject, relation: looking_at, object}`,
which was SPEC-01's own worked example.

Worth stating alongside the Molly Bang audit, where the same field was bound wrongly. `relationships`
means entity-to-entity relations. Bang's colour grouping is perceptual grouping and is not that.
The field is fine; the earlier binding was not.

## Counts

```
OLD                          NEW
10 atoms                     13 SourceKnowledge objects
 3 human notes                2 SourceConceptSystems
 2 operational               13 Creative IR bindings
                              7 evaluation bindings (0 at frame level)
                              0 governance
                              2 production candidates
                              1 object with no binding
```
