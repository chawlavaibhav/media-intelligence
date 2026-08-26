# CANON-010 — combined coverage report (C10-E)

**Task:** CANON-010 / C10-E · **Date:** 26 Aug 2026
**Measurement:** `combined-coverage-measurement.json`, computed by `combined_coverage.py`
**Structural coverage only. No frequency and no market-share claim is made anywhere in this report.**

---

## 1. Headline

| | Original 30 | Extension | Combined |
|---|---|---|---|
| Items | 30 | 11 | **41** |
| Runnable in Wave 1 | 30 | 10 | **40** |
| Representation only | 0 | 1 | 1 |
| **Request operations covered** | **1 of 7** | 6 of 7 | **7 of 7** |

**All seven grammar operations are now covered. Before the extension, one was.**

## 2. Operations

| Operation | Original 30 | Extension | Combined |
|---|---|---|---|
| generate | **30** | 0 | 30 |
| edit | **0** | 4 | 4 |
| animate | **0** | 2 | 2 |
| variants | **0** | 2 | 2 |
| restore | **0** | 1 | 1 |
| extend | **0** | 1 | 1 |
| compose | **0** | 1 | 1 |

**Not covered: none.**

Read the counts correctly. The 30:11 ratio is **not** a statement that generation is thirty times
more common than editing — CANON-009 found the opposite is plausible. It is an artefact of build
order: the 30 were authored from first-product scope before the request space was mapped, and the
Controller decided to freeze them rather than rebalance. **Neither bank is demand evidence.**

## 3. Grammar features

| Feature | Original 30 | Combined | Note |
|---|---|---|---|
| Supplied asset as **subject of operation** | **0** | **8** | The whole point of the extension |
| Reference supplied (informing a new artefact) | 30 | 33 | Already strong |
| Exact text requirement | 28 | 33 | Still the most-exercised requirement |
| Speech / spoken script | 12 | **12** | **Extension adds none** — see §5 |
| **Camera motion declared** | **0** | **2** | New capability |
| **Camera and subject motion separated** | **0** | **2** | RX-05 and RX-06, in both directions |
| **Cardinality > 1** | **0** | **2** | New capability |
| **Set-level acceptance** | **0** | **1** | RX-10 |
| Ambiguity markers (contradiction / underspecification) | 17 | **17** | **Extension adds none** — see §5 |
| Objective present | 30 | 41 | 100%, and still what no public corpus has |

## 4. Co-occurrences the extension adds

Each was absent from the combined bank before:

- `edit_plus_preservation` · `edit_plus_exact_text_survival` · `edit_plus_exact_text_change` ·
  `edit_plus_script_switch`
- `restore_plus_identity_preservation`
- `animate_plus_identity_preservation` · `animate_plus_text_stability` ·
  `animate_plus_identity_continuity`
- `camera_motion_without_subject_motion` · `subject_motion_without_camera_motion`
- `extend_plus_element_preservation` · `extend_plus_delivery_constraint`
- `compose_plus_dual_identity` · `compose_plus_new_relationship` ·
  `product_plus_person_plus_reference`
- `variant_set_plus_cross_deliverable_invariant` · `variant_set_plus_multiscript` ·
  `campaign_set_plus_cross_modality` · `set_level_acceptance`
- `multi_turn_inheritance` *(representation only)*

**`product_plus_person_plus_reference` is worth naming.** CANON-009 listed it as central to the first
product but **inferred, not measured** — each part attested, the combination not. RX-08 now exercises
it directly.

## 5. Deliberate non-additions — and why

Two features the extension **does not** touch. Both are deliberate.

### 5.1 Speech — stays at 12, all from the original 30

CANON-009 found **no corpus covering speech, voiceover or dialogue requests at all.** The original 30
already carry 12 speech briefs, derived from first-product scope.

Adding more would have increased a count with **no external structural support** while the
best-evidenced operations were still uncovered. The right move was to spend the extension on what the
evidence pointed at. Speech coverage is adequate for Wave 1 and is labelled scope-derived, not
evidence-derived.

### 5.2 Ambiguity markers — stay at 17, all from the original 30

The 30 carry 9 underspecified and 8 contradictory briefs — deliberate probes for a specific failure
mode. The extension items are mostly **clear**, and intentionally so: an extension item exists to
exercise an *operation*, and confounding a new operation with a planted contradiction would make a
failure impossible to attribute.

RX-11 is the exception, and its ambiguity is intrinsic rather than planted — it is the multi-turn
inheritance problem itself.

## 6. Customer-specified vs omitted production decisions

Across the combined 41, the pattern the grammar's `specification_provenance` exists to record:

| Typically **customer-specified** | Typically **omitted** and derived or delegated |
|---|---|
| Requested operation | Camera motion (where not the point of the request) |
| Exact copy and its script | Lighting and background treatment |
| Identity invariants when the customer names them | How a vacated area is filled after a removal |
| Deliverable count when a set is wanted | Composition and framing |
| Hard brand constraints | Shot pacing within a stated duration |

**The asymmetry is the finding.** Customers reliably specify *what must be true* and reliably omit
*how it should look*. That is the space Canon exists to fill — and it is why `specification_provenance`
is a required field rather than a nicety: it makes intervention level measurable.

Note the one direction that must never reverse: **a field is `customer_specified` only if the
customer said it.** The validator enforces this with evidence quotes.

## 7. What the combined bank still does not cover

Stated plainly, because each is a deliberate deferral rather than an oversight.

| Gap | Status | Why |
|---|---|---|
| **Multi-turn as a runnable request** | **Deferred by Controller decision** | No request-history contract is frozen. RX-11 probes representation only |
| **Speech in non-generate operations** | Not covered | No corpus evidence; would compound two under-supported dimensions |
| **Audio-only deliverables** | Not covered | Outside first-product scope as currently framed |
| **`best_n_of_m` acceptance** | Vocabulary exists, no item uses it | RX-09 and RX-10 cover the two bases that change cost most. A third would add an item without adding a distinct production problem |
| **Edit + variants combined** | Not covered | Plausible and untested. Flagged for a later wave rather than added speculatively |
| **India-specific request evidence** | **Structurally unavailable** | CANON-009 found no India/Hinglish/Devanagari request corpus. Our language coverage is scope-derived and cannot currently be validated externally |

## 8. Creative IR fields that cannot represent a required outcome

The C10-E question: does any *existing* Creative IR field fail to represent something the combined
bank requires?

**No existing field fails.** Three things are **absent** rather than broken, and all three are
addressed by the Normalized Request delta rather than by changing Creative IR:

| Requirement | Status | Where addressed |
|---|---|---|
| Which operation the customer asked for | **No field exists** | `N1 requested_operation` — Normalized Request |
| One deliverable versus a set, and its acceptance basis | **No field exists**; `delivery.aspect_ratios[]` is one artefact delivered several ways | `N4 deliverable_set` |
| Camera motion separable from subject motion | Camera motion has no explicit home; it would land in `visual_language` or a beat's free-text `purpose` | `N5 motion_intent` |

**No stop condition was triggered.** None of the three requires changing the Creative IR / Normalized
Request separation — all three *strengthen* it by putting customer-stated facts in the object that
preserves customer-stated facts.

One item, **`subject_of_operation`**, extends an existing Creative IR vocabulary (`assets[].role`)
rather than adding a field. SPEC-01's own comment warns that conflating asset meanings is the failure
to avoid, and this is exactly such a case: an artefact being *acted on* is not a reference *informing*
a new artefact.

## 9. Verification

| Check | Result |
|---|---|
| Original 30 byte-identical | **PASS** — SHA-256 verified on both files, 30 briefs present |
| All 7 mechanical gates | **PASS**, and each proven to fire against a deliberate violation |
| Extension items complete | 11/11 carry operation, inputs, constraints, cardinality, acceptance basis, grammar features, Wave-1 flag |
| Grammar fields have provenance and operation rules | 18/18 |
| No workflow or provider token anywhere in the bank | **PASS** |
| Multi-turn not runnable | **PASS** — 1 item, `representation_only`, validator rejects any change |
