# CANON-010 — Normalized Request delta (C10-B) and multi-turn boundary (C10-C)

**Task:** CANON-010 · **Date:** 26 Aug 2026 · **Branch:** `work/canon-010-request-freeze`
**Status: PROPOSAL PREPARED FOR CONTROLLER FREEZE. No frozen spec was edited.**
**Authority:** `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md` §2

---

## 1. The smallest change that does the job

Six additions to the **Normalized Request** — object 1, the conservative record of what the customer
said, preserved forever. **No change to Creative IR is proposed.**

| # | Field | Why here and not in Creative IR |
|---|---|---|
| **N1** | `requested_operation` | It is something the customer *said*, not something we decided |
| **N2** | `supplied_assets[]` | Ditto — the customer handed us these |
| **N3** | `mutation_intents[]` | What the customer wants changed and kept |
| **N4** | `deliverable_set` | One artefact or a set, and how acceptance works |
| **N5** | `motion_intent` | Camera and subject motion, kept separate |
| **N6** | `specification_provenance` | Who said what — the audit trail |

**Why the Normalized Request rather than Creative IR.** SPEC-01 keeps the two objects side by side
so that *"did the parser misread the user, or did creative reasoning decide badly?"* stays
answerable. All six additions are facts about **the ask**. Putting them in Creative IR would mean the
system's own decisions and the customer's words share one object, and that question stops being
answerable.

**Why not Production IR.** Production IR does not exist and is not designed here. Nothing below says
*how* anything is made.

---

## 2. The field specifications

### N1 · `requested_operation` — the load-bearing addition

```yaml
requested_operation:
  value:       generate | edit | animate | restore | extend | compose | variants
  operation:   preserve
  provenance:  user | derived
  evidence:    "remove the guy in the background"
```

| Property | Value |
|---|---|
| **Type** | enum, `vocabularies.requested_operation` in `MEDIA-REQUEST-GRAMMAR-v1.yaml` |
| **Required** | yes |
| **Operation** | `preserve` when stated; `derive` when a direct consequence |
| **Provenance** | `user` or `derived` only — **never `system_decided`** |

**Why `system_decided` is forbidden.** If the system decided what operation the customer wanted, the
system misread the request. There is no legitimate case where an operation appears from nothing the
customer said. Making that structurally impossible is cheaper than catching it later.

**What must NOT be inferred.**

> **A supplied asset does not imply `edit`.**

This is the error the field exists to prevent, and it is easy to make:

| Customer says | Operation | Because |
|---|---|---|
| *"Change the background of this photo"* | **edit** | They asked us to alter that artefact |
| *"Here's our product shot — make a Diwali creative"* | **generate** | The photo is an `identity_reference`; the deliverable is new |

Both requests arrive with an image attached. **They have different preservation semantics**, and
getting it wrong means either destroying something the customer wanted kept, or refusing to change
something they wanted changed.

**Relationship to workflow mode.** None, and the separation is deliberate. Requested operation is
what the customer asked. Workflow mode is the route the Planner picks — inpainting, img2img,
segment-and-composite. Both may appear in an Eval condition row; the Controller decision requires
provenance to keep one from substituting for the other.

**Values `inpaint`, `img2img`, `outpaint`, `controlnet`, `upscale` are forbidden** and the validator
fails on them. Every one is a technique, not a request.

### N2 · `supplied_assets[]`

```yaml
supplied_assets:
  - asset_id:   ref_001
    media_type: image | video | audio | vector | font | document
    role:       subject_of_operation | identity_reference | style_reference |
                composition_reference | brand_asset | previous_campaign |
                character_sheet | location_reference | inspiration
    applies_to: entity.product_123     # required for identity_reference and subject_of_operation
    operation:  preserve
    provenance: user
```

**One new role: `subject_of_operation`.** SPEC-01's existing roles all describe a reference that
*informs* a new artefact. An edit request supplies something categorically different — the artefact
the operation acts **on**. SPEC-01's own comment warns that *"assets carry radically different
meanings and must not be conflated"*, and this is precisely such a case.

**What must NOT be inferred:** when the role is not stated and cannot be derived, the correct
operation is **`ask`**, not `decide`. Guessing that an attached image is the subject rather than a
reference is guessing at the whole shape of the job.

### N3 · `mutation_intents[]`

```yaml
mutation_intents:
  preservation_default: implicit_everything_not_named
  intents:
    - target:    "person in background"
      intent:    remove
      operation: preserve
      provenance: user
```

**Required when** `requested_operation ∈ {edit, restore, extend, compose}`.

**The rule that matters — do not enumerate implicit preservation.** An edit request states what
should change; everything else is implicitly preserved. It is tempting to expand that into an
explicit `preserve` entry for every element in the image. **Don't.** Those entries would be recorded
as things the customer said, and the customer said none of them. `preservation_default` records the
implicit background honestly, in one field, without manufacturing customer statements.

### N4 · `deliverable_set`

```yaml
deliverable_set:
  cardinality:       1
  variation_axis:    none | market | placement | format | message | language | audience
  acceptance_basis:  per_deliverable | set_level | best_n_of_m
  best_n:            3          # required when acceptance_basis == best_n_of_m
  operation:         preserve | derive
  provenance:        user | derived
```

**Default when the customer says nothing:** cardinality 1, axis none, acceptance per-deliverable,
provenance `derived`. A safe default, explicitly recorded as derived rather than pretended to be
stated.

**Why this is not `delivery.aspect_ratios[]`.** That is *one artefact delivered several ways*. This
is *several artefacts*. The distinction is economic: **the product's primary metric is Cost per
Accepted Outcome**, and twelve variants where three must be accepted is a different object from one
deliverable that must be accepted. Without this field we cannot express the difference, so we cannot
price it.

### N5 · `motion_intent` — two fields, deliberately

```yaml
motion_intent:
  subject_motion:
    - entity_ref:  entity.person_456
      motion_type: locomotion | gesture | micro_expression | object_motion | state_change
      operation:   preserve
      provenance:  user
  camera_motion:
    motion_type:   static | pan | tilt | zoom | dolly | orbit | handheld | crane
    operation:     preserve | derive | decide | delegate
    provenance:    user | derived | system_decided
```

**They must not be merged**, per the Controller decision. CANON-009 found the reason in TIP-I2V's
real requests: users ask for **"zoom"** (camera), **"walk"** (locomotion) and **"blink"**
(micro-expression). Three different production problems, three different failure modes. A system
that models "motion" as one thing cannot tell which one failed.

**Asymmetry worth noting:** camera motion may legitimately be `system_decided` — a customer who says
nothing about the camera has delegated it. Subject motion may not: a customer who says nothing about
what the subject does has usually not asked for motion at all.

### N6 · `specification_provenance`

```yaml
specification_provenance:
  customer_specified: [requested_operation, text_requirements.headline]
  customer_omitted:   [camera_motion, delivery.resolution]
  derived:
    - field:     modality
      from:      "post it on Reels"
      rationale: "Reels implies vertical video"
  operation:  derive
  provenance: system_decided
```

This field is *about* provenance, so it is itself system-derived. That is not circular — it is a
record of who said what, not a claim about the deliverable.

**The rule the validator checks hardest:** a field is `customer_specified` **only if the customer
said it**. Assigning customer provenance to a system decision is how a bad plan later gets scored as
a misread request — it corrupts the one distinction the two-object architecture exists to preserve.

**External corroboration:** CANON-009 found PSR's *creativity level* dimension — over 82,976 real
requests — measuring how much latitude the requester granted. A coarse, one-dimensional version of
SPEC-01's six operations, arrived at independently.

---

## 3. What is explicitly NOT proposed

| Not proposed | Why |
|---|---|
| Any change to Creative IR | The six additions are facts about the ask; Creative IR describes what should exist |
| Any Production IR field | Does not exist, not designed here, out of scope |
| Workflow mode anywhere | Eval's condition contract owns it; it is not customer intent |
| Evaluator thresholds | Acceptance *intent* is Canon's; acceptance *measurement* is Eval's |
| Style / prompt-folklore fields | Controller decision §2.5. CANON-009 found "trending on artstation" went from top-prominent in 2022 to outside the top 10 by 2023 — model-contingent vocabulary with a one-year shelf life |
| A multi-turn schema | §4 |

---

## 4. Multi-turn boundary (C10-C)

**Status: DEFERRED BY CONTROLLER DECISION. No schema is proposed and none should be.**

### What the evidence says

CANON-009 found **95,000 multi-turn editing sequences of up to five rounds** in SEED-Data-Edit
part 3. Real requests often arrive as a conversation, not a specification. This is a genuine request
shape and not an edge case.

### Why it is not solved here

The Controller decision is explicit: multi-turn is *"recognised as a real request shape but NOT
solved in this integration"*, no schema is frozen, and it must not block the first paid benchmark.

There is also a Canon-side reason to refuse. The problem is genuinely hard in a way that is easy to
under-estimate:

> **Round three of a conversation is not a new request. It inherits everything unstated from rounds
> one and two.**

Modelling each round as an independent Normalized Request **loses the inheritance**. Modelling it as
a mutation of the first **breaks the "preserved forever, never overwritten" rule** that makes the
object trustworthy. Neither is acceptable, and choosing between them is an architecture decision.

The Canon charter's mandatory stop conditions cover exactly this: a request appearing to require an
IR field that does not exist is an **ARCHITECTURE** matter — stop, do not add the field yourself.
**So this is flagged, not designed.**

### The minimum boundary: three things current structures must not preclude

This is the whole of C10-C. Not a design — three constraints that keep the door open.

**B1 · The Normalized Request must remain append-only and addressable.**
Each request record needs a stable identity that a later record could reference. It does *not* need
a `previous_request_id` field now — it needs to not be structured in a way that makes adding one
impossible. Today's structure already satisfies this; the constraint is *do not break it*.

**B2 · Nothing may assume a request is complete at first receipt.**
Any component that treats "the request" as final and total will need rewriting when rounds arrive.
Specifically: acceptance evaluation must be able to attach to a *deliverable*, not to "the one and
only request". `deliverable_set` (N4) already works this way.

**B3 · `specification_provenance` must be able to record inherited provenance later.**
A field specified in round one and unmentioned in round three is still `customer_specified` — but
by an *earlier* round. The provenance record needs room for that eventually. It does not need the
field now.

### Exactly what is deferred

| Deferred | Status |
|---|---|
| Request-history schema / linkage | **Not designed.** Architecture decision for the Controller |
| Inheritance semantics across rounds | **Not designed.** The hard part |
| Whether a revision creates a new outcome boundary | Partially settled by the Resources disposition — a *material* brief change creates a new outcome/revision boundary. What counts as material is undecided |
| Multi-turn acceptance semantics | **Not designed** |
| Multi-turn in a paid benchmark | **Excluded from Wave 1** by Controller decision |

### What CANON-010 does provide

One extension item, **`RX-11`**, marked **`representation_only`** and **`runnable_wave1: false`**.
It exists to test whether the *representation* can hold a multi-turn request at all — not to be
executed. The validator fails the build if any multi-turn item is ever marked runnable without a
frozen history contract, so this cannot drift into the benchmark by accident.

---

## 5. Stop conditions — checked, none triggered

| Stop condition | Assessment |
|---|---|
| Requires changing the fundamental Creative IR separation | **No.** All six additions sit in the Normalized Request, which *strengthens* the separation rather than blurring it |
| A field is inherently a Production IR / provider decision | **No.** Production-route values are explicitly forbidden from `requested_operation` and the validator enforces it |
| External evidence needed to claim market prevalence | **No** — because no prevalence claim is made anywhere. Every field is justified by structural recurrence or by stated first-product scope, and the two are labelled differently |

**One item was flagged rather than decided** — multi-turn history — which is the correct handling
under the charter, not a stop.
