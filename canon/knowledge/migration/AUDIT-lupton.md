# Migration audit — Ellen Lupton, *Thinking with Type*, Hierarchy

**Source file (unchanged):** `canon/lupton-hierarchy-atoms.yaml`
**Old shape:** 9 atoms, 2 human notes, 3 operational

**Extraction uncertainty carries forward on every object below.** The EPUB interleaves two print
columns sentence by sentence; every claim required de-interleaving, which is inference. All
objects take `extraction_uncertainty: column_interleaving` and none may be treated as settled
until checked against the printed page.

| Old id | Concept | New | Systems | Bindings | Note |
|---|---|---|---|---|---|
| lu_001 | hierarchy_expresses_content_organisation | B D | — | `creative.hierarchy` | |
| lu_002 | hierarchy_supports_scanning_entry_and_exit | B D E | — | `creative.hierarchy` | converges with rw_003 |
| lu_003 | level_cues_must_be_applied_consistently | B C D E | cue economy | `static.typography_layout`, `creative.hierarchy` | |
| lu_004 | hierarchy_cues_are_spatial_or_graphic | B D | cue economy | `static.typography_layout` | taxonomy; was `operational` |
| lu_005 | inline_emphasis_needs_only_one_signal | B C D E | cue economy | `static.typography_layout`, `copy.body` | contradicts lu_006 alone |
| lu_006 | limited_redundancy_reinforces_a_break | B C D | cue economy | `static.typography_layout` | contradicts lu_005 alone; was `operational` |
| lu_007 | three_cue_ceiling_per_level | B C D E | cue economy | `static.typography_layout`, `creative.hierarchy` | the bound that reconciles lu_005/lu_006 |
| lu_008 | one_hierarchy_has_many_valid_encodings | B D | — | `creative.hierarchy` | was `operational`; architectural evidence |
| lu_009 | align_x_heights_when_mixing_families | B D | — | `static.typography_layout` | `mechanism_absent` |
| note | common_typographic_diseases | **A** | — | — | specimen text and humour; genuinely human-learning only |
| note | named_family_recommendations | **A** | — | — | dated product recommendations |

Two notes stay human-learning only. They are the batch's clearest examples of material that is
correctly *not* knowledge — which matters, because it shows the new architecture is not simply
promoting everything.

## System

**scs_lup_001 · hierarchy_cue_economy** — `mutual_qualification`
Members: lu_003, lu_005, lu_006, lu_007.

The strongest system found in the batch, because its members are **individually contradictory**.
lu_005 says inline emphasis takes one signal. lu_006 says redundancy is recommended. Retrieved
separately they conflict. Retrieved together with lu_007's three-cue ceiling and lu_003's
consistency requirement, they form a coherent economy: one signal inline, deliberate redundancy at
structural breaks, never more than three, applied identically at every occurrence.

Under SPEC-02 this was handled by writing cross-references into each atom's `exceptions` field —
which worked, but only because a human noticed. Nothing structural required them to travel together.

## Architectural evidence, not a governance binding

`lu_008` — one logical hierarchy has endlessly many valid visual encodings — says the ranking
belongs to the content while the cue set is a separate design choice. That is the Creative IR /
Production IR boundary, stated by a typographer about print in 2010.

It is recorded as a Creative IR binding (`fills`), and noted in FINDINGS-10 as independent support
for a split we made on other grounds. It is **not** made a governance binding: it has no named
governance consumer, and dressing evidence up as a rule would be exactly the junk drawer SPEC-04
guards against.

## Counts

```
OLD                          NEW
 9 atoms                      9 SourceKnowledge objects
 2 human notes                2 human-learning-only items
 3 operational                1 SourceConceptSystem
                             12 Creative IR bindings
                              5 evaluation bindings
                              0 governance · 0 production
                              0 objects with no binding
                              9 objects flagged column_interleaving
```
