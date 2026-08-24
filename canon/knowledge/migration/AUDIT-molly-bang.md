# Migration audit — Molly Bang, *Picture This*

**Source file (unchanged):** `canon/molly-bang-principles-atoms.yaml`
**Old shape:** 18 atoms, 0 human notes, 2 operational, 16 pending_vocabulary

## Disposition

Legend: **B** SourceKnowledge · **C** system member · **D** Creative IR binding · **E** evaluation binding · **F** governance · **G** production · **H** currently unbound · **A** human learning only

| Old id | Concept | New | Systems | Bindings proposed | Note |
|---|---|---|---|---|---|
| mb_001 | pictorial_weight_of_vertical_position | B C D E | attention | `creative.hierarchy`, `static.spatial_hierarchy` | diagnostic used product vocabulary — rewritten |
| mb_002 | centre_as_strongest_attractor | B C D E | attention | `creative.hierarchy`, `static.composition` | **diagnostic said "rank-1 element"** — SPEC-01 term inside a source object |
| mb_003 | centre_avoidance_for_exploration | B C D | attention | `static.composition` | trade-off partner of mb_002; incoherent alone |
| mb_004 | size_as_strength | B C D E | attention | `creative.hierarchy` | **`entities.role` dropped** — see distortions |
| mb_005 | contrast_enables_perception | B C D E | attention | `creative.hierarchy`, `static.composition` | was `operational` |
| mb_006 | value_contrast_against_ground | B C D E | attention | `creative.visual_language`, `static.composition` | |
| mb_007 | horizontal_reads_as_calm | B C D | register | `creative.visual_language` | source demo not isolated (visual pass) |
| mb_008 | vertical_reads_as_energy | B C D | register | `creative.visual_language` | **principle text contains a cross-principle relation** — system leak |
| mb_009 | diagonal_reads_as_motion_or_tension | B C D | register | `creative.visual_language` | |
| mb_010 | vertical_half_emotional_register | B C D | register | `creative.visual_language` | |
| mb_011 | point_versus_curve_register | B C D | register | `creative.visual_language` | **SPEC-02's own "unbindable" example** — see distortions |
| mb_012 | ground_value_safety_register | B C D | register | `creative.visual_language` | |
| mb_013 | colour_association_dominates_shape_association | B C D E | register | `static.composition` | **`relationships` dropped** — see distortions |
| mb_014 | colour_carries_borrowed_qualities | B C D | register | `creative.visual_language`; `message.emotional_target` *(extractor_inference)* | |
| mb_015 | depth_via_size_and_base_height_progression | B C D | space | `static.composition` | |
| mb_016 | overlap_joins_elements_into_a_unit | B C D | space | `static.composition` | **`relationships` dropped** |
| mb_017 | isolation_by_surrounding_space | B C D E | attention, space | `static.composition`, `creative.hierarchy` | source asks an open question; weakened in visual pass |
| mb_018 | proximity_to_edge_or_centre_raises_tension | B C D | register, space | `static.composition` | |
| **new** | sk_mb_0019 depth_from_frame_exceeding_element | B H | space | — | **recovered** — see below |

## Systems

**scs_mb_001 · emotional_register_of_pictorial_structure** — `interacting_set`
Members: mb_007, mb_008, mb_009, mb_010, mb_011, mb_012, mb_014, mb_018.
Whole-system claim: the registers combine and can cancel; the emotional reading is a property of
the combination, not of any single dimension.

**scs_mb_002 · attention_and_dominance** — `trade_off_set`
Members: mb_001, mb_002, mb_003, mb_004, mb_005, mb_006, mb_017.
Internal trade-off: mb_002 ↔ mb_003, holding the eye versus releasing it to explore.

**scs_mb_003 · pictorial_space** — `interacting_set`
Members: mb_015, mb_016, mb_017, mb_018, sk_mb_0019.

mb_017 and mb_018 are members of two systems each. Permitted, and true to the source.

## Distortions caused by the old `informs` filter

**1. `entities.role` on mb_004.** Bang says a larger element reads as stronger and more capable.
`entities.role` is our schema's hero/supporting slot. Mapping one to the other is a product
interpretation that was recorded as if it were part of her claim. Now a binding — or rather, not
even that: the binding drops it, because "big reads strong" does not assert which entity should be
the hero.

**2. `relationships` on mb_013 and mb_016.** SPEC-01's `relationships` means physical or semantic
relations between entities — a person *holding* a product. Bang is describing **perceptual
grouping**: which elements a viewer reads as belonging together. Two different concepts sharing an
English word, joined because a binding had to be found.

**3. Product vocabulary inside source objects.** mb_002's diagnostic read *"Is the rank-1 element
at or near centre"*. mb_001 and mb_017 also used "intended priority order" and "rank-1". `rank-1`
is SPEC-01's word. It appeared inside the field that claimed to record what Molly Bang teaches.

**4. SPEC-02's own counter-example was extracted as a bound atom.** The spec presented
`pointed_shapes_read_as_threatening` as knowledge informing nothing, destined for human notes. The
extraction three days later produced `mb_011`, informing `creative.visual_language`. Same
knowledge, opposite verdicts, from the same rule. This is the clearest available evidence that
`informs` cannot carry an admission decision.

## The 18/18 conversion

Molly Bang produced 18 atoms and rejected nothing. Every other source rejected 2–5. Re-audited,
**the conversion itself was not wrong** — the "Principles" section is a numbered sequence of
compositional claims, and a numbered claim is genuinely a knowledge object. What was wrong was
the reason it looked suspicious: the old schema had exactly two outcomes, bound or discarded, so
the extractor's choice was to bind everything or throw away Molly Bang.

Under SPEC-03 the same 18 remain, plus one recovered, and **three of them now carry no Creative IR
binding for `entities.role`/`relationships` that they never should have had.** The distortion was
never in the count. It was in what the atoms claimed.

## Recovered knowledge

`sk_mb_0019 · depth_from_frame_exceeding_element` — an element running off the frame edge with no
visible base reads as nearest. Visible in the p87 figure; **not stated in the prose**. FINDINGS-03
recorded it as a candidate and deliberately refused to write it, because SPEC-02 had no way to
mark "seen in a figure, not claimed by the author."

SPEC-03 does: `claim_type: source_interpretation`, `interpretation_basis: "observed in figure
p87; the surrounding text describes only base-height progression"`, `source_support: visual`.
It has no binding and needs none.

## Preserved as-is

All 7 source failure terms and all 13 repair terms enter SPEC-05 Layer 1 unchanged, with
`origin: source`. Visual-pass revisions to mb_007, mb_011, mb_013 and mb_017 carry forward,
including the two recorded confounds.

## Counts

```
OLD                          NEW
18 atoms                     19 SourceKnowledge objects
 0 human notes                3 SourceConceptSystems
 2 operational               21 Creative IR bindings   (2 dropped as distortions)
16 pending_vocabulary         8 evaluation bindings
                              0 governance · 0 production
                              1 object with no binding (recovered)
```
