# Spec 04 — Operational Bindings v0

**Date:** 23 Aug 2026 · **Depends on:** [SPEC-03](SPEC-03-source-knowledge.md)

## What a binding is

A binding answers one question:

> How can today's system use this piece of source knowledge?

It is **our interpretation**, recorded as ours. It is derived from Source Knowledge and is never
part of the source's claim.

```
SOURCE KNOWLEDGE                     OPERATIONAL BINDING
Molly Bang says relative scale       We think this can fill creative.hierarchy,
affects perceived dominance.         diagnose an incorrect focal priority,
                                     and suggest altering relative scale.
```

The second sentence must never be presented as though Molly Bang specified our Creative IR. Under
SPEC-02 it effectively was: the `informs` field sat inside the atom, at the same level as the
principle, with nothing marking it as ours.

## Consequences of the split

- **Bindings are versioned against the product.** When SPEC-01 changes, bindings are re-derived.
  Source Knowledge is untouched.
- **Zero bindings is a normal state.** It means today's product has no use for durable knowledge,
  which is information about the product, not about the knowledge.
- **One SourceKnowledge object may have many bindings**, across different targets.
- **A binding may reference several SourceKnowledge objects**, or a SourceConceptSystem.
- **Deleting a binding costs nothing.** Deleting Source Knowledge loses a book.

---

## The object

```yaml
binding_id: bnd_0041
source_knowledge_refs: [sk_mb_0002]
# or: source_system_refs: [scs_mb_001]

target_type: creative_ir
# creative_ir | evaluation | production | governance | benchmark

target_path: creative.hierarchy      # required for creative_ir; null for others
target_schema: SPEC-01
target_schema_version: v0.1          # what this binding was derived against

role: [fills, diagnoses]
# fills · constrains · diagnoses · repairs · derives · flags · evaluates

rationale: >
  Centre placement is one of the strongest determinants of which element is noticed first,
  so a specified rank-1 element and a centred element that disagree is a detectable conflict.

applicability:
  when: "the composition has a specified hierarchy and a clearly centred element"
  limits: >
    The source discusses picture-book illustration. Whether the effect holds at the scale,
    crop and viewing duration of a social-feed creative is untested.

evidence_basis: derived_from_source   # derived_from_source | extractor_inference |
                                      # cross_source_supported | empirically_supported
                                      # (the last requires Empirical Memory refs)
empirical_refs: []

failure_ontology_refs: [fo_focal_attention.contested]   # SPEC-05 identifiers, not raw strings
repair_ontology_refs: [ro_position.alter_centre_offset]

status: proposed
# proposed | accepted | production_candidate | deprecated | rejected
status_reason: "not reviewed"
```

### On `evidence_basis`

`derived_from_source` means the binding follows closely from what the source says.
`extractor_inference` means we made a leap. The distinction matters because a binding is where
leaps happen, and this is the field that records one honestly.

A binding whose `evidence_basis` is `extractor_inference` and whose SourceKnowledge has
`evidence.characteristics: [practitioner_assertion, outcome_claimed]` is two inferential steps
from anything demonstrated. Nothing currently reads that chain — but it can now be read, which
was impossible under SPEC-02.

---

## Target types

### `creative_ir`
Binds to a SPEC-01 path. Requires `target_path` and `target_schema_version`.

### `evaluation`
The knowledge supports checking an output. `target_path` names an acceptance dimension where one
exists, otherwise null.

Note from the probes: several failure modes are **between-shot properties** — a crossed action
line, reversed screen direction, a jump cut, mismatched reciprocal framing. An evaluator scoring
frames independently cannot detect any of them. Evaluation bindings should record the **unit of
observation** they require:

```yaml
observation_unit: frame | shot | shot_pair | sequence | whole_asset | asset_set_over_time
```

### `production`
How something is made or executed. **Production IR does not exist yet**, so these bindings carry
`status: production_candidate` and `target_path: null`. They are parked, not translated.

**Physical production actions must not be rewritten as generation actions.** "Move the light
outside the family of angles" does not become "regenerate with a different lighting prompt." That
translation is a generative-media hypothesis and belongs to Pass 2. The binding records the
source's action in the source's frame and marks it unbound.

### `governance`
Only where there is a **named consumer**. Permitted consumers:

```
taxonomy_governance       how the ontology admits, splits or refuses terms
retrieval_governance      what may be retrieved together, and what must not be split
conflict_resolution       how contradictions between knowledge are settled
evidence_interpretation   how evidence characteristics are weighted
rule_application          whether a principle may be applied in isolation
cross_source_synthesis    when sources may be combined into a canonical concept
```

If a candidate governance binding does not name one of these, it is not a governance binding —
it stays as Source Knowledge with no binding. This list is the guard against a junk drawer.

### `benchmark`
The knowledge generates a test case, a brief category, or a minimal-pair comparison.

---

## Worked examples from the six probes

**A governance binding with a real consumer.** *Light: Science & Magic* refuses the word
"specular" because practitioners use it for three different things, and names the two concepts
separately instead.

```yaml
binding_id: bnd_gov_001
source_knowledge_refs: [sk_lsm_0009]
target_type: governance
target_path: null
role: [constrains]
rationale: >
  A worked precedent for the ontology's core problem: a technical field encountering a term with
  divergent practitioner meanings, and resolving it by refusing the term rather than normalising
  it. Directly applicable to SPEC-05's treatment of near-synonyms.
governance_consumer: taxonomy_governance
evidence_basis: derived_from_source
status: proposed
```

**A production candidate, deliberately untranslated.**

```yaml
binding_id: bnd_prod_004
source_knowledge_refs: [sk_lsm_0007]     # the family of angles
target_type: production
target_path: null
target_schema: null
role: [derives]
rationale: >
  Determines where a physical source must sit to produce or avoid a direct reflection.
  No generative equivalent is asserted here.
applicability:
  limits: "Physical camera and light. Not translated to generative control. Pass 2 required."
evidence_basis: derived_from_source
status: production_candidate
```

**An evaluation binding that names its observation unit.**

```yaml
binding_id: bnd_eval_012
source_knowledge_refs: [sk_gos_0004, sk_gos_0005]
target_type: evaluation
role: [diagnoses]
observation_unit: shot_pair
rationale: >
  A crossed action line is invisible within any single shot; it exists only as a relation
  between two. Any evaluator for this must receive both shots together.
evidence_basis: derived_from_source
status: proposed
```

---

## Validation rules

1. `source_knowledge_refs` or `source_system_refs` non-empty and resolving.
2. `target_type` from the fixed list.
3. `creative_ir` bindings carry `target_path`, `target_schema`, `target_schema_version`.
4. `governance` bindings carry a `governance_consumer` from the permitted list.
5. `production` bindings carry `status: production_candidate` while Production IR does not exist.
6. `evaluation` bindings carry `observation_unit`.
7. `evidence_basis` present.
8. Ontology references use SPEC-05 identifiers, never raw source strings.
9. A binding may not restate the source claim — it references it.

## What bindings are not

They are not truth about the world, not the source's opinion, and not stable. They are the
current, revisable answer to "what can we do with this," recorded separately so that when the
answer changes, the knowledge survives.
