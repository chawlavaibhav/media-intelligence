# Migration audit — Robin Williams, *The Non-Designer's Design Book*, ch.2

**Source file (unchanged):** `canon/williams-proximity-atoms.yaml`
**Old shape:** 9 atoms, 5 human notes, 0 operational

| Old id | Concept | New | Systems | Bindings | Note |
|---|---|---|---|---|---|
| rw_001 | proximity_implies_relationship | B C D E | spacing | `static.composition`, `creative.hierarchy` | |
| rw_002 | eye_stop_count_threshold | B D E | — | `static.composition` | source-authored diagnostic with a threshold |
| rw_003 | reading_path_requires_definite_start_and_end | B D E | — | `creative.hierarchy` | **hierarchy as path, not rank** — see below |
| rw_004 | competing_emphasis_destroys_entry_point | B D E | — | `creative.hierarchy` | |
| rw_005 | trapped_white_space_separates_related_elements | B C D E | spacing | `static.typography_layout`, `static.composition` | |
| rw_006 | equal_spacing_signals_equal_relationship | B C D E | spacing | `static.typography_layout` | |
| rw_007 | do_not_fill_space_for_its_own_sake | B C D | spacing | `static.composition` | |
| rw_008 | all_caps_reduces_legibility | B D E | — | `static.typography_layout`, `copy.headline` | `mechanism_absent` |
| rw_009 | clarity_outranks_thematic_expression | B D | — | `creative.concept` | governance considered and **rejected** — see below |
| note | organisation_increases_readership_and_recall | **B** H | — | — | was discarded; `outcome_claimed`, `mechanism_absent` |
| note | group_information_before_designing | **B** H | — | — | was discarded; see below |
| note | overlap_graphic_past_the_edge | **B** H | — | — | was discarded; single instance, `mechanism_absent` |
| note | straight_corners_read_stronger_than_rounded | **B** H | — | — | was discarded; single instance |
| note | reversed_type_needs_a_robust_face | **B** G | — | production_candidate | was discarded; first parked production item |

**All five discarded notes are now first-class Source Knowledge.** None has a Creative IR binding
and none needs one.

## System

**scs_wil_001 · relative_spacing_as_the_grouping_signal** — `mutual_qualification`
Members: rw_001, rw_005, rw_006, rw_007.
Whole-system claim: spacing signals grouping **only relatively**. rw_005 and rw_006 are the same
mechanism seen from opposite ends — space inside a group pushes apart, equal space everywhere
removes the signal entirely. rw_007 is the failure that follows when placement is driven by
vacancy rather than relationship. Retrieved singly, rw_005 reads as "use less space," which
inverts the actual rule.

**scs_wil_002 · the_four_principles** — `interacting_set`, **STUB**
Williams presents proximity, alignment, repetition and contrast as one framework and repeatedly
solves examples in this chapter using the other three. Only proximity was processed. Recorded as a
stub so the incompleteness is visible rather than implied.

## Governance considered and rejected

`rw_009` — clarity outranks thematic expression — was flagged in FINDINGS-04 as possibly
governance. Under SPEC-04 a governance binding requires a **named consumer** from the permitted
list. This has none: it is a precedence rule about creative concepts, not about how the system
handles knowledge. It binds to `creative.concept` as `constrains`.

Recording the rejection so it is not re-proposed.

`group_information_before_designing` — write out what belongs together *before* laying anything
out — is genuinely a statement about our pipeline: produce a specification before execution. But
it also has no named governance consumer. It stays Source Knowledge with **no binding**, which is
the honest outcome and was impossible before.

## Open observation carried forward

`rw_003` requires a composition to have a definite beginning **and a definite end** — the viewer
must know when they are finished. SPEC-01's `creative.hierarchy` is a rank-ordered list, which can
express "noticed first" but not "finished." Lupton's `lu_002` independently says the same thing
about entry and exit.

Two sources, unaware of each other, describing hierarchy as a **traversal** rather than a ranking.
Recorded; SPEC-01 not modified.

## Counts

```
OLD                          NEW
 9 atoms                     14 SourceKnowledge objects
 5 human notes                1 SourceConceptSystem + 1 stub
 0 operational               12 Creative IR bindings
                              7 evaluation bindings
                              0 governance (1 considered, rejected)
                              1 production candidate
                              5 objects with no binding
```
