# Migration audit — *Light: Science & Magic*, ch.3

**Source file (unchanged):** `canon/lsm-reflection-atoms.yaml`
**Old shape:** 6 atoms, 4 human notes, 1 operational

This source is where SPEC-02 failed hardest. It was the densest chapter processed and produced the
fewest atoms — **not because it teaches less, but because the admission test only admitted
knowledge with a current Creative IR consumer.** Its central concept was filed as a note.

| Old id | Concept | New | Systems | Bindings | Note |
|---|---|---|---|---|---|
| lsm_001 | surface_identity_is_a_reflection_mixture | B C D E | reflection | `entities`, `creative.visual_language` | controlled_comparison (three-object thought experiment) |
| lsm_002 | diffuse_reflection_is_viewpoint_independent | B C D | reflection | `entities`, `creative.visual_language` | was `operational` |
| lsm_003 | direct_reflection_is_viewpoint_dependent | B C D E | reflection | `entities`, `creative.visual_language` | |
| lsm_004 | material_class_determines_allowed_viewing_angle_variation | B C D E | reflection | `entities.allowed_variation` | **validation candidate** — see below |
| lsm_005 | source_size_governs_shadow_and_highlight_extent | B C D E | reflection | `creative.visual_language` | internal-consistency check |
| lsm_006 | glare_is_strongest_on_dark_and_transparent_subjects | B C D E | reflection | `entities`, `creative.visual_language` | |
| note | **the_family_of_angles** | **B** C G | reflection | production_candidate | **the book's central concept** — recovered |
| note | direct_reflection_brightness_ignores_distance | **B** C H | reflection | — | physical mechanism |
| note | lighting_is_reflection_management | **C** | reflection | — | becomes the system's whole-system claim |
| note | source_refuses_an_ambiguous_term | **B** F | — | governance: taxonomy_governance | **the batch's only governance binding** |

## System

**scs_lsm_001 · reflection_management** — `causal_model`
Members: lsm_001–lsm_006, the family of angles, and the inverse-square behaviour.

**Whole-system claim:** *photographic lighting is primarily an exercise in reflection management;
understanding and managing reflection for the result you want is what constitutes good lighting.*

That sentence was an orphaned human note under SPEC-02 — a framing statement with no field to
fill. It is not an atom at all. It is **what the system as a whole asserts**, and SPEC-03 has a
field for exactly that. The three reflection types, the family of angles and the material
consequences are its members.

This is the clearest demonstration in the batch that some knowledge is systems-level and was being
destroyed by atomisation.

## The recovered central concept

`the_family_of_angles` — every point on a surface is seen at a slightly different angle; together
those angles determine where a source must sit to produce or avoid a direct reflection.

It was a note because it informs no Creative IR field. It informs no Creative IR field because it
is a rule about **where to put a physical light** — Production IR, which does not exist. Under
SPEC-03 it is ordinary Source Knowledge with `claim_type: explicit_source_claim`,
`evidence.characteristics: [explicitly_stated, visually_demonstrated, mechanism_given]`, and one
production binding at `status: production_candidate`.

**Deliberately not translated.** "Move the source outside the family of angles" is not rewritten
as "regenerate with a different lighting prompt." SPEC-05 marks its repair
`executable_by: [physical_production]` so the gap stays visible.

## The governance binding

`source_refuses_an_ambiguous_term` is the only binding in the batch with a named governance
consumer. The source refuses to use "specular" anywhere, because practitioners use it for direct
reflection, for small bright highlights, and for hard light — and says so explicitly rather than
picking a winner.

```yaml
target_type: governance
governance_consumer: taxonomy_governance
role: [constrains]
```

SPEC-05's near-synonym discipline — refuse the ambiguous term, name the concepts separately,
record the reason — is taken directly from it. Under SPEC-02 this was a note with `informs: []`.

## A validation candidate, not a fill

`lsm_004` says whether a subject's appearance may vary with viewing angle is **a property of its
surface, not a free choice**. SPEC-01's `entities.allowed_variation` is currently authored by hand.

So this binds with `role: [constrains]`, not `fills`: it says a spec declaring
`viewing_angle: true` for polished metal is declaring something physically incoherent. Whether the
IR should validate that field is left open — SPEC-01 is untouched.

## Repairs did not transfer, and that is now recorded

Six objects, one repair term. Every repair the source implies is a physical camera action.
SPEC-05's `executable_by` field exists because of this probe. The terms are preserved in the
source's frame and marked, rather than silently bridged.

## Counts

```
OLD                          NEW
 6 atoms                     10 SourceKnowledge objects  (9 + 1 as system claim)
 4 human notes                1 SourceConceptSystem
 1 operational               11 Creative IR bindings
                              5 evaluation bindings
                              1 governance binding
                              1 production candidate
                              1 object with no binding
```
