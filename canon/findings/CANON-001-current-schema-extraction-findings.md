# CANON-001 — First current-schema Canon extraction: findings

**Date:** 24 Aug 2026 · **Task:** `canon/tasks/CANON-001.md` · **Branch:** `work/canon`
**Source:** Molly Bang, *Picture This*, "The Principles" and "Some Remarks about Space", pp.42–91
**Pre-audit checkpoint commit:** `1383abe`

---

## What was produced

| Deliverable | Count |
|---|---|
| SourceKnowledge objects | 55 |
| SourceConceptSystem objects | 6 |
| Ontology terms (SPEC-05 Layer 1) | 26 — 6 problems, 10 remedies, 7 properties, 3 entities |
| Ontology relationships (Layer 2) | 9, all `related_to` |
| Ontology concepts (Layer 3) | 2, both `source_specific_concept` |
| Operational Bindings | 13 — 5 creative_ir, 4 evaluation, 1 benchmark, 2 governance, 1 production |

All 21 rendered figures were inspected before any claim was written. The extraction validates
against SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer constraints, checked by script.

**Method note.** Passes ran in the order: schema constraints → source segmentation → visual pass →
SourceKnowledge → SourceConceptSystems → ontology → bindings → validation → checkpoint commit →
historical comparison. SPEC-01 was opened only at the bindings pass. **Disclosed exception:**
SPEC-01's opening section and field names were read during the Phase 0 governance review, before
extraction began, while checking whether bindings were producible at all. The isolation intended by
"bindings last" is therefore partial rather than complete for this run.

---

## Extraction profile

```
source_support        text_and_visual 27 · text 28
extraction_uncertainty  none 35 · figure_not_inspected 11 · ocr_degraded 9
source_uncertainty      none 41 · source_hedges 7 · source_concedes_difficulty 5 ·
                        source_asks_open_question 2
mechanism.stated_by_source   true 27 · false 28
claim_type              explicit_source_claim 55 · source_interpretation 0
caveats                 source_stated 44 · extractor_observed 51 · objects with none 1
intra-source relations  94 across 8 relation types; 4 objects carry none
```

Half the objects rest on text alone, because ten of the pages carrying claims had no rendered
figure available. That is recorded per object rather than smoothed over.

---

## Findings

### 1. SPEC-03's own worked example misdescribes this source, and the error under-credits the author

This is the most consequential result and it is a defect in a **frozen** file.

SPEC-03 presents `scs_mb_001`'s whole-system claim with `origin: extractor_synthesis` and an
`interpretation_basis` reading, in part: *"The source never states this as a general claim."*

The source does state it, twice, in plain language. On page 58 it interrupts its own sequence of
principles to say the principles are used never one by one but always in combination and always in
some context, and that the addition of each new element can modify the effect of the other elements
or change them completely. On pages 58–60 it works a three-way example and concludes that the
principles work in conjunction with each other and are subservient to context and content.

The fresh extraction therefore records `scs_mb_c001_001.whole_system_claim.origin` as
**`source_explicit`** with a page reference, and carries the statements themselves as
`sk_mb_c001_0016` and `sk_mb_c001_0017` — two objects the historical work has no counterpart for.

Why it matters beyond one field: the origin-marking machinery exists to stop us claiming a source
said something it did not. This is the mirror failure — the spec attributes to the extractor
something the author stated outright, and does so in the example that teaches the distinction.
Anyone learning the convention from SPEC-03 learns it from a case that gets this source backwards.

**No edit was made to SPEC-03.** Recommended for Controller action.

### 2. The fresh pass independently avoided all four distortions the migration audit catalogued

Written blind, the extraction did not reproduce any of them.

| Distortion recorded in the audit | Fresh extraction |
|---|---|
| `entities.role` bound to size-as-strength | Size (`sk_mb_c001_0037`) feeds only a `creative.hierarchy` **diagnostic** binding. No role claim. |
| `relationships` bound to colour grouping and to overlap | Colour grouping binds to an **evaluation** binding with `target_path: null`. SPEC-01's `relationships` field is never touched. |
| Product vocabulary ("rank-1") inside source-faithful fields | Zero occurrences; checked mechanically across `claim`, `source_terms`, `mechanism`, `scope`, `concept_label` and the source problem/remedy fields. |
| `pointed_shapes_read_as_threatening` treated as unbindable, then bound | Extracted as `sk_mb_c001_0035` with a controlled comparison against `0036`. Under SPEC-03 there is no admission question to get wrong. |

This is the cleanest evidence available that the SPEC-03/04 split does what it was designed to do,
and it was obtained without sight of the audit.

### 3. The binding layer now behaves as SPEC-04 predicted, and the old layer did not

| | Historical audit | Fresh extraction |
|---|---|---|
| SourceKnowledge objects | 19 | 55 |
| Creative IR bindings | 21 | 5 |
| Objects with no direct binding | not reported | 30 of 55 (55%) |
| Objects in neither a binding nor a bound system | not reported | 13 |
| Governance bindings | 0 | 2 |
| Production candidates | 0 | 1 |
| Benchmark bindings | 0 | 1 |

Twenty-one Creative IR bindings against nineteen objects is effectively one binding per object —
the shape SPEC-02's coupled rule produced, carried forward through the migration. The fresh pass
produced five, each referencing several objects, and left more than half the corpus unbound.

SPEC-04 states that zero bindings is a normal, healthy state and information about the product
rather than the knowledge. This is the first run where that actually happened.

### 4. Three binding categories the historical work left empty are populated, and one is cross-stream

- **`rule_application` governance** (`bnd_mb_c001_0011`) — the page 58 statement is an author
  instructing readers on whether their own principles may be applied in isolation. A worked
  precedent for exactly the question that consumer exists to settle.
- **`evidence_interpretation` governance** (`bnd_mb_c001_0012`) — page 74 holds that colour
  symbolism rests on a generalisation that is *completely false* and that it *works very, very
  well*, without treating the falseness as a defect. A precedent for separating "is the mechanism
  true" from "does it predict response".
- **`benchmark`** (`bnd_mb_c001_0010`) — **tagged CROSS_STREAM.** The source constructs four
  near-minimal pairs with a stated expected reading: same triangle high vs low (p55/p57), same
  burst centred vs displaced (p63/p65), same silhouette pointed vs curved (p70/p71), same shape set
  in one colour vs two (p75/p77). That is the shape a creative-fitness benchmark item needs, and
  EVAL-001 is currently designing a Capability Battery V0. Two of the four pairs are **not**
  strictly isolated and the binding records which; the source's expected readings are its own
  judgements, not measured responses, so they are candidate expected answers requiring validation,
  never ground truth.

### 5. Granularity diverged by roughly 3× and most of the difference is real content, not splitting

All 18 historical atoms have a counterpart here. Seventeen map one-to-one or one-to-two (upper and
lower half, points and curves were each split into a matched pair). The remaining 37 objects have no
counterpart, and they are concentrated in material the historical pass barely touched:

- **pp.81–91, "Some Remarks about Space"** — 3 historical atoms, 10 fresh objects.
- **The interludes and worked examples** — pp.58–60 (combination and subservience to content),
  pp.62–64 (the radial force, the exploration goal, the centre remaining active), p67 (meditation
  centring, living elements escaping the principles), p73 (the association mechanism), p78 (the
  situation the author explicitly declines to name). None of these are numbered principles, and a
  one-object-per-numbered-principle convention would miss all of them.

The audit concluded the historical 18/18 conversion "was not wrong" because a numbered claim is
genuinely a knowledge object. That holds. What it did not surface is that **the numbered principles
are roughly a third of what this source teaches.**

### 6. One object the historical work recovered was missed here, and it is not being back-filled

The audit records `sk_mb_0019 · depth_from_frame_exceeding_element` — an element running off the
frame edge with no visible base reads as nearest — as *visible in the p87 figure but not stated in
the prose*, and cites it as the case SPEC-03's `source_interpretation` machinery exists for.

The fresh extraction did not produce it. **`claim_type` is `explicit_source_claim` for all 55
objects; `source_interpretation` count is zero.**

Re-inspecting p87 after the comparison: the dark field occupying the right of the frame does run off
both the top and bottom edges, has no visible base, and does read as nearer than the three bars. The
audit's observation is defensible from the figure.

**It has not been added.** Adding it would be converging on the audit rather than comparing with it,
and it would destroy the more useful signal — which is that this extraction pass used figures to
*verify* text-derived claims and never as independent evidence in their own right. That is a method
limitation worth knowing about before the same method is applied to ten more books, and patching the
one known instance would hide it. Controller direction is requested; the correction is cheap.

### 7. The source-vocabulary layer is thin because this source is not a source of that kind

SPEC-05 Layer 1 admits terms of kind `problem`, `remedy`, `property` or `entity`. There is no kind
for a *principle*, and this source is almost entirely principles. Six problems and ten remedies came
out of 50 dense pages, against 55 claims.

Nine of the twenty-six terms are the author's own coinages and are preserved verbatim —
`pictorial_weight`, `natural_constants`, `noncolors`, `picture_world`, `radial_force`,
`center_of_attention`, `invisible_emotional_horizon_line`, `islands_of_calm`,
`emotions_attached_to_remembered_experiences`. Those are where this source's real vocabulary lives,
and they sit in the `property`/`entity` kinds rather than the failure/repair spine that Layer 2 and
Layer 3 are built around.

Consequence for the join: SPEC-05 describes the term layer as the join between a book's predicted
problems and a model's observed failures. On this source that join has six problem terms to work
with. The prediction the ontology is meant to carry is mostly sitting in the SourceKnowledge claims,
which the ontology does not index.

### 8. Layer 2 is nearly vacuous for a first source, as anticipated

Nine relationships, all `related_to`, all internal to one source. Zero
`potentially_equivalent_to` — within a single book the author does not use two different terms for
one thing often enough to justify one, and manufacturing one would assert a similarity nobody
established. Recorded as genuinely empty rather than padded.

**Negative findings not written, for want of authority.** `canon/CHARTER.md` grants this worker
`related_to` and `potentially_equivalent_to` as local decisions. `distinct_from` is not on that list,
so two candidates were left unwritten:

- `t_mb_c001_0011 space_reads_as_flat` vs `t_mb_c001_0012 reads_as_floating` — both are depth
  failures and both were written as such, but the mechanisms are unrelated (a picture with no
  frame-crossing element vs a shape with no baseline).
- `monotony_of_relentless_repetition` vs `boring_and_heavy` — recorded here as `related_to`, but a
  reviewer may judge them distinct, since one is about perfect regularity and the other about
  equal-sized parallel shapes.

Requesting a ruling on whether `distinct_from` is a local decision.

---

## Schema and repository inconsistencies encountered

Recorded per Controller ruling 8. **No file outside `canon/knowledge/current/molly-bang/` and
`canon/findings/` was edited.**

**A. SPEC-03's worked example uses a relation absent from its own vocabulary.** SPEC-03 lists the
`intra_source_relations` vocabulary as `qualifies · qualified_by · trades_off_with · depends_on ·
generalises · specialises · contradicts · demonstrated_together_with` (lines 95–96), then the very
next line uses `{relation: member_of_system, target: scs_mb_001}`. Per Controller ruling 4,
membership is carried by `SourceConceptSystem.members[]` only and `member_of_system` was not used.

**B. SPEC-03 has no relation for "adjacent but not logically related".** Thirteen intra-source
relations were drafted, caught by the validator as outside the listed vocabulary, and **removed**
rather than forced into a wrong type. Examples: the two floating-reading claims (`0019` circular
frames, `0010` absent baseline) describe the same reading from unrelated causes; `0044`
(regularity/confusion extremes) and `0052` (wide/narrow gap extremes) are structurally analogous
claims about opposite extremes of one variable. SPEC-05 provides `related_to` for exactly this at
the *term* layer; SPEC-03 provides nothing equivalent at the *claim* layer. Four objects now carry
`intra_source_relations: []` as a result. This is reported, not repaired.

**C. SPEC-04's worked examples use ontology identifiers SPEC-05 does not define.** SPEC-04 shows
`failure_ontology_refs: [fo_focal_attention.contested]` and
`repair_ontology_refs: [ro_position.alter_centre_offset]`. SPEC-05's Layer-1 identifier form is
`t_...`. This file uses `t_` identifiers, since SPEC-05 is the ontology specification, but SPEC-04
rule 8 requires "SPEC-05 identifiers" while illustrating a different scheme.

**D. `CANON-CURRICULUM-V0.md` marks this section done.** It records "Molly Bang, *Picture This* ✓
*The Principles* (pp.42–91) — done". Two representations of these pages now exist. The ✓ will
mislead a future session unless it is qualified.

**E. Broken link in `coordination/DECISION-LOG.md`.** It links `ASSUMPTIONS-AND-FALSIFICATION.md`;
the file is `coordination/ASSUMPTIONS.md`.

---

## Post-comparison changes to the fresh extraction

**None.** No object, system, term, relation or binding was altered, added or removed after
`AUDIT-molly-bang.md` was opened. The pre-audit checkpoint `1383abe` and the final state of the four
YAML files are identical.

---

## Bearing on the assumptions register

Reported as evidence, not as resolution. None of these should be promoted without the register's bar.

- **1b — the Source/Binding separation is the right response.** *Supporting, weakly.* Its stated
  falsifier is "after fifty bindings, if none is ever revised while its source knowledge holds
  constant, the separation is paying for nothing." Thirteen bindings exist and none has been
  revised, so the falsifier is untouched. What this run adds is the first evidence of the intended
  *shape*: 55% of objects unbound, bindings referencing several objects each, and three category
  types populated that a Creative-IR-only rule could not have reached.
- **2 — atoms are sufficient.** *Further weakened.* `sk_mb_c001_0003` is a relationship between two
  principles that had to become its own object; the audit flagged the same content as a "system
  leak" inside `mb_008` and left it there.
- **3 — SourceConceptSystems are required.** *Its review trigger has fired.* The trigger is "after
  five systems exist"; six now do, from one source. Its falsifier — that every system turns out
  reconstructible from its members' `intra_source_relations` — is now testable, and finding B above
  bears directly on it, since the relation vocabulary could not carry thirteen of the connections
  that were drafted.
- **14 — corpus representativeness.** Untouched. One source says nothing about a forty-book library.

---

## Recommendations

Recommendations only. None has been acted on.

1. **Correct SPEC-03's `scs_mb_001` worked example** so it does not teach the convention from a case
   that reverses this source. Controller-only; a Canon worker may not edit a frozen spec.
2. **Rule on the missed `source_interpretation` object** (finding 6) — add it under a follow-up task,
   or leave it out and keep the method signal.
3. **Rule on `distinct_from` authority** (finding 8).
4. **Route the benchmark binding to EVAL-001** as cross-stream input, with its two recorded confounds
   and the caveat that the expected readings are the author's judgements rather than measurements.
5. **Decide the granularity convention before the next source.** Two defensible conventions produced
   19 objects and 55 objects from the same 50 pages. Whichever is chosen should be written down
   before a second source is extracted, for the same reason SPEC-05 wanted the naming convention
   settled before seeding.
6. **Render the ten missing figure pages** (53, 61, 72, 73, 82, 83, 85, 88, 89, 90) before this
   source is considered complete. Half the extraction currently rests on text alone, and the source's
   entire closing section on space is unverified visually.
