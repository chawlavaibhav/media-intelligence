# Proposed method change — a home and a vocabulary for the cross-source layer

**STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.**

**From:** Canon worker, REP-02 (tranche A) · **To:** Controller · **Date:** 31 Aug 2026
**Severity:** `LOCAL-PLUS` — a SPEC-05 addendum (no redesign): one file location, two relation
values, two row fields, one compile invariant.
**Status of this document:** proposal only. Nothing below is in force. Adoption is a Controller
decision; until it is taken, no cross-source record may live anywhere but a candidates lane, and
nothing may treat one as doctrine.

---

## 1. What is missing, measured

SPEC-05 already defines the hard parts of cross-source work correctly: the `cross_source_concept`
shape (`independent_origins`, `children_are_authoritative`, `mechanisms_differ`, `status`), the
pairwise independence rule with its mechanical form `independent_origins_ok()` in
`canon/validation/validate_audit_gate_v02.py`, and `distinct_from` for recorded negative work.
Four things are absent, and their absence is measurable from committed bytes:

1. **No home file.** Every committed `ontology-mappings.yaml` is per-source; 18 of the 24 headers
   say "source-local". `find canon/knowledge -maxdepth 2 -name '*cross*'` returns nothing.
   `murch-blink-p1-25/ontology-mappings.yaml:468-479` defers a verified cross-source candidate to
   "the integrator's work" — an artifact that does not exist. Four cross-source findings live only
   in YAML comments, machine-invisible.
2. **No cross-source contradiction or tension relation.** The Layer-2 vocabulary (SPEC-05 lines
   60-73) is: `maps_to`, `broader_than`, `narrower_than`, `related_to`,
   `potentially_equivalent_to`, `distinct_from`, `same_failure_family`, `same_mechanism`,
   `same_observed_effect`, `uncertain`. `contradicts` exists only in SPEC-03's
   *intra*-source vocabulary. The most valuable join content — two accepted sources disagreeing —
   is currently inexpressible at Layer 2.
3. **No confidence grade.** Rows carry `confidence_basis` (provenance of the judgement) but no
   grade of how strongly the evidence supports the proposed relation.
4. **No usability flag.** Nothing marks a record as involving HOLD material, so nothing
   mechanically stops HOLD-involving content from reaching a compiled artifact.

Observed Layer-2 relation census over the 24 committed
`canon/knowledge/current/*/ontology-mappings.yaml` files (recompute: load every file's
`relationships` list and count by `relation`; total 189):

| relation | count |
|---|---|
| related_to | 103 |
| distinct_from | 50 |
| narrower_than | 9 |
| broader_than | 7 |
| same_mechanism | 11 |
| same_observed_effect | 4 |
| maps_to | 3 |
| potentially_equivalent_to | 1 |
| same_failure_family | 1 |

## 2. Proposed changes

### 2.1 Home file

Adopt `canon/knowledge/current/cross-source/` as the committed home for Layer-2 rows whose two
ends live in different sources, and for `cross_source_concept` records. Per-source files stay
source-local, as their headers promise. Until adoption, candidate records live in
`canon/candidates/ontology-join/` (seeded by REP-02 as
`cross-source-candidates-v0.yaml`, every row `status: proposed`).

### 2.2 Two relation values added to the Layer-2 vocabulary

```
contradicts_across_sources   two accepted sources make opposed claims about the same decision;
                             symmetric; both claims are kept and co-delivered
in_tension_with              opposed only under a shared frame that may not hold; symmetric;
                             REQUIRES frame_note stating the frame under which the tension
                             resolves (phase, artifact class, level of address, era)
```

`in_tension_with` without a `frame_note` is invalid — a tension you cannot frame is a
contradiction you have not finished analysing, and should be recorded as `uncertain` until it is.

The full closed enum after adoption (12 values, declared symmetry/direction):

| relation | symmetry |
|---|---|
| maps_to | symmetric |
| broader_than | directed (from is broader) |
| narrower_than | directed (from is narrower) |
| related_to | symmetric |
| potentially_equivalent_to | symmetric |
| distinct_from | symmetric |
| same_failure_family | symmetric |
| same_mechanism | symmetric |
| same_observed_effect | symmetric |
| uncertain | symmetric |
| contradicts_across_sources | symmetric |
| in_tension_with | symmetric |

The enum is **closed**: a validator refuses any value outside it. `contradicts` (bare) remains
SPEC-03 intra-source vocabulary and is invalid at Layer 2, which keeps the two layers'
disagreement machinery from being conflated.

### 2.3 Confidence grade

Every cross-source row carries `confidence: high | medium | low` alongside the existing
`confidence_basis`. Grade is about evidential support for the stated relation (both definitions
read, independence recomputed = `high`; one side thin or the frame arguable = `medium`;
inference from summaries = `low`). Basis remains about who judged.

### 2.4 Usability flag

Every cross-source row carries `usable`:

```
accepted_only    every id resolves in canon/knowledge/current; eligible for Controller
                 promotion review and, after review, for compilation
involves_hold    at least one end lives under canon/candidates/ (HOLD lane); usable only for
                 admission planning; NEVER content in a compiled/production artifact
false            not usable for anything until a stated precondition is met (e.g. a source
                 admission, a re-derivation)
```

A validator enforces: an id that resolves only under `canon/candidates/` is legal **only** on a
row whose `usable` is not `accepted_only`.

### 2.5 Compile invariant — tensions travel with doctrine

Any compiled pack that states doctrine derived from an object X must carry the tension and
contradiction records touching X (`contradicts_across_sources`, `in_tension_with`, and SPEC-03
intra-source `contradicts`/`qualified_by` partners). Rationale, recomputable: 462 of 677 objects
(68.2%) are entangled in guard edges (`contradicts`/`qualifies`/`qualified_by`/
`trades_off_with`/`depends_on` over the 1280 committed `intra_source_relations`; recompute by
walking every `source-knowledge.yaml`), so per-object selection without partner co-delivery ships
rules without their exceptions at corpus scale.

## 3. What this proposal does not do

It does not admit any source, promote any candidate, create any `cross_source_concept`, or touch
SPEC-05's independence rule, which is correct as adopted (CANON-004/CANON-006). Promotion of any
candidate to `cross_source_concept` or `same_failure_family` remains a Controller (human) review
under Governance rules 2 and 5.

## 4. Mechanical form

`canon/validation/validate_cross_source_candidates.py` (shipped with REP-02) enforces the closed
enum, the usability rule, the confidence grade, the `frame_note` requirement, and — for any row
asserting agreement (`maps_to`, `same_mechanism`, `same_observed_effect`,
`same_failure_family`) — at least two pairwise-independent origins recomputed from
`canon/audit/records/*.audit.yaml` `lineage.related_sources_in_corpus`, mirroring
`independent_origins_ok()`. Negative fixtures under
`canon/validation/fixtures/ontology-join/` pin each refusal.

**Adoption is a Controller decision.** This file proposes; `coordination/CONTROL-STATE.md`
governs.
