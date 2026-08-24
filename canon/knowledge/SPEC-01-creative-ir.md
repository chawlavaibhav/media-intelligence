# Spec 01 — Creative IR v0.1
## Architecture locked for first experiment

**Date:** 23 Aug 2026 · **Supersedes:** v0, v0.1-draft
**Locked means:** we stop redesigning this intellectually and let real examples break it.
Not "final schema."

---

## Object boundaries

```
ARBITRARY INPUT
      ↓   parse only — never invent
NORMALIZED REQUEST          ← object 1, preserved forever
      ↓   creative reasoning + Canon
CREATIVE IR                 ← object 2, what we want to exist
      ↓   Capability Registry + Production Canon
PRODUCTION IR               ← object 3, how we intend to make it
      ↓
EXECUTE → EVALUATE → REPAIR
```

Objects 1 and 2 are kept side by side, never merged. "Did the parser misread the user, or did
creative reasoning decide badly?" has to stay answerable.

## The six operations

Every Creative IR field is the result of exactly one, and **records which**:

```
preserve   the user said it — carried through untouched
derive     logical consequence of what they said (Reel → vertical)
decide     judgment exercised (nothing said about lighting → choose)
delegate   marked free, generation may vary
ask        the answer matters and cannot be safely guessed
flag       the request contradicts itself; unresolvable until answered
```

Stored per field, so intervention level becomes measurable: how often we preserved, decided,
delegated, had to ask, or hit a conflict.

---

## Field annotation

```yaml
<field>:
  value:        <the thing>
  operation:    preserve | derive | decide | delegate | ask | flag
  provenance:   user | derived | system_decided | brand_policy |
                customer_memory | default
  strength:     hard | soft | free
  status:       resolved | unresolved | conflicted | blocked
  confidence:   0.0–1.0                        # derived / system_decided only
  evidence:     "launch our new sneaker"       # user / derived — what it came from
  rationale:    "..."                          # system_decided
  canon_refs:   [atom_ids]                     # knowledge used to reach the decision
```

**Provenance and strength are independent.** "Blue would be nice, but whatever works" is
`user / soft`. "Exactly this green" is `user / hard`. A system lighting choice can be
`system_decided / soft`.

**`canon` is not a provenance.** Molly Bang did not decide this customer's lighting — our
reasoning did, using Canon knowledge. So the value is `system_decided` and the Canon appears
in `canon_refs` as the evidence behind it. This matters the moment we try to measure *did the
Canon cause this decision*, which is the entire A/B/C experiment.

**There is no separate `constraints` section.** Hard/soft/free is a property of each field.
A compiled constraints view may be generated for convenience — derived, never authored.

---

## Object 1 — Normalized Request

What the customer actually said. Reading only. Absent means absent.

```yaml
raw_input:  "premium feel chahiye but bahut luxury wala nahi, young office crowd ke liye"
input_lang: hinglish

extracted:
  tone:      { value: premium_restrained, provenance: user, evidence: "premium... bahut luxury wala nahi" }
  audience:  { value: young_office, provenance: user, evidence: "young office crowd ke liye" }
  product:   { value: null }
  objective: { value: null }

internal_conflicts:
  - type: internal_request_conflict
    fields: [creative.composition, creative.density]
    statement: "minimal clean frame with lots of graphical elements everywhere"
    action: ask
```

`null` means the user did not say it. It does not mean they don't care — that judgment
belongs to object 2.

Internal conflicts are detected here, before the Canon participates. "Product dominant but
don't show it until the last frame" is the other canonical case. Own benchmark category.

---

## Object 2 — Creative IR

### assets — registry

Assets carry radically different meanings and must not be conflated. "I like the lighting in
this image" must never be read as "preserve this image's identity."

```yaml
assets:
  - asset_id: ref_001
    type: image | video | audio | vector | font
    role: identity_reference | style_reference | composition_reference |
          brand_asset | previous_campaign | character_sheet |
          location_reference | inspiration
    applies_to: entity.product_123        # required for identity_reference
```

### entities[] — subjects and their relationships

```yaml
entities:
  - entity_id: product_123
    type: product | mascot | person | character | venue | object
    role: hero | supporting | background | absent
    references: [ref_001]
    invariants:                      # these ARE the identity
      - silhouette
      - packaging_geometry
      - cap_colour
    allowed_variation:
      lighting: true
      viewing_angle: true
      label_design: false

  - entity_id: person_456
    type: person
    role: supporting
    invariants: [face_identity, wardrobe_colourway]

relationships:
  - { subject: person_456, relation: holding, object: product_123 }
  - { subject: person_456, relation: looking_at, object: product_123 }
```

Real media is product + person, two people + product, car + driver + location. A single
`subject` could not express any of them. Relationships also feed prompt construction and
become checkable claims ("is the person actually holding it?").

The point is never "preserve identity" but **which dimensions constitute identity** — that
is what a checker can test and a repair can target.

### intent

```yaml
objective:
  class: awareness | consideration | conversion | retention | explain |
         demonstrate | train | recruit | announce | entertain | educate |
         engage | offer | brand_film | other
  description: "drive trial of the new SKU"        # open text, always
desired_action:
success_criteria:                                   # what the USER said they care about
```

`class` normalizes where it fits; `description` stays open. An early marketing funnel taxonomy
must not become the ceiling of a general commercial-media API.

### audience

```yaml
who:
context:
language:
  spoken:          hi
  on_screen_copy:  en
  subtitles:       none
  viewer:          hi-IN
```

Four separate languages. Hindi dialogue with an English CTA and no subtitles is an ordinary
Indian brief, and language becomes a hard router constraint later.

### message
`proposition` · `support[]` · `emotional_target`

### creative

```yaml
concept:
hook:
hierarchy:                       # global — what the creative prioritises overall
  - { rank: 1, element_ref: entity.product_123, reason: primary commercial subject }
  - { rank: 2, element_ref: copy.headline }
  - { rank: 3, element_ref: brand.logo }
visual_language:                 # palette, lighting, texture, genre
```

Element references resolve against `entities[]`, `copy`, and `brand`, so hierarchy is
machine-comparable rather than free text.

### copy

```yaml
headline:
  value: "30% OFF"
  exactness: exact | approximate | free
body:
cta:
script_system: devanagari | latin | ...
```

No `render_method`. Whether that headline is generated, composited, or drawn as SVG is a
Production IR decision that changes as models improve — keeping it here would bake today's
model limitations into the permanent specification.

### brand
`logo` (asset, placement, exactness) · `palette`/`type` with tolerance ·
`mandatories[]` (legal, disclaimers, price) · `prohibitions[]`

### delivery
`platform` · `aspect_ratios[]` · `duration` · `resolution`

### StaticCreativeExtension
`composition` (framing, depth, figure-ground) · `spatial_hierarchy` · `typography_layout`

### VideoCreativeExtension

```yaml
temporal_structure:
  - { beat: hook,    start: 0s, end: 2s, purpose: ... }
  - { beat: demo,    start: 2s, end: 5s }
  - { beat: endcard, start: 5s, end: 8s }

temporal_hierarchy:
  hook:    [entity.person_456, entity.product_123]
  demo:    [entity.product_123, benefit_demo]
  endcard: [brand.logo, copy.cta]

dialogue_intent:
continuity_requirements:
```

Global hierarchy says what the creative prioritises; temporal hierarchy says how that priority
moves. Video is not a poster with a duration field, and the filmmaking and editing books will
land almost entirely here.

---

## Authority and conflict

"The user is never overridden" fails on *"remove the mandatory disclaimer."* Authority and
constraint strength are separate axes.

**Authority tiers** — a lower tier never silently overrides a higher one:

```
1  legal_mandatory      disclosures, disclaimers, regulated claims
2  brand_policy(hard)   logo colourways, prohibited treatments
3  user explicit
4  customer_memory
5  task objective
6  canon heuristic
7  default
```

| Situation | Action |
|---|---|
| Canon (soft) vs user, any strength | advisory only — value unchanged |
| Lower tier vs higher tier, both soft | higher tier wins, recorded |
| User (hard) vs brand_policy (hard) | `ask` — neither side silently wins |
| Anything vs legal_mandatory | `reject` — not negotiable |
| Internal user contradiction | `ask`, before the Canon participates |

```yaml
conflicts:
  - field: brand.logo.colour
    source_a: { value: fluorescent_green, provenance: user,         strength: hard }
    source_b: { value: black_or_white,    provenance: brand_policy, strength: hard }
    resolution: { action: ask }

advisories:
  - field: creative.hierarchy
    canon_view: "product should lead within first 2s for a launch objective"
    user_value: "product held back until 5.5s"
    action: none
    severity: low
```

Advisories exist so the Canon's characteristic harm — quietly overriding someone who knew what
they wanted — becomes a counted failure rather than an anecdote.

### The clarification response

`ask` resolves to an intermediate API result, not a dead end:

```yaml
status: needs_clarification
request_id: req_123
clarifications:
  - field: audience.who
    reason: required_to_resolve_objective
    question: "Who is the primary audience?"
    blocking: true
```

The caller answers and resubmits, decides the value itself, or handles it however its UX
chooses. Non-interactive callers set a policy up front:

```yaml
clarification_policy: return_questions | fail_if_blocking | autonomously_resolve_when_safe
```

Legal conflicts still reject. Brand-versus-user conflicts return clarification.

---

## Acceptance contract

Two sources, kept apart.

**User success criteria** — what they explicitly said they care about. Often empty.

**System acceptance contract** — generated from the completed spec. Every `strength: hard`
field and every `exactness: exact` field must produce an entry, or the spec is incomplete
by construction.

```yaml
acceptance_contract:
  - requirement: copy.headline matches "30% OFF" exactly
    derived_from: copy.headline.exactness = exact
    verification: { required: true, mode: machine }

  - requirement: product identity holds on [silhouette, cap_colour]
    derived_from: entities.product_123.invariants
    verification: { required: true, mode: hybrid }

  - requirement: product reads as aspirational but attainable
    derived_from: message.emotional_target
    verification: { required: true, mode: unresolved }
```

`mode: machine | human | hybrid | unresolved`. A requirement can be legitimate and currently
unverifiable — that is a known state, not a schema failure.

The contract states **what must be observed, never how to observe it.** Instrument selection
lives in Production IR and comes from the Capability Registry. "Ask a VLM what it noticed
first" is a hypothesis about an instrument, and Finding 01 is exactly why we don't assume it.

---

## Readiness

Each field resolves to one of:

```
known             the user said it
derivable         follows from what they said
safe_to_decide    system can choose without risk
deliberately_free delegated to generation
blocking_unknown  matters, cannot be guessed, must be asked
```

Only `blocking_unknown` reduces readiness.

```yaml
information_coverage:    0.42     # how much came from the user — drives intervention level
specification_readiness: 0.96     # no blocking unknowns remain
```

**The concepts are locked; the scoring formula is not.** Equal weighting is certainly wrong —
a missing CTA wording is trivial, a missing SKU is fatal. Weights come from real examples,
not from us guessing now.

This is *specification* readiness. Whether any model can actually produce it is a Production
IR question against the Capability Registry, one stage later.

---

## Object 3 — Production IR (stub, not drafted)

Named here only so nothing leaks back into object 2:

```
asset decomposition · generate/reuse/transform/render decisions ·
model + workflow selection · reference-conditioning strategy ·
render_method per element · known_risks from empirical memory ·
checker assignment per dimension · repair options · cost + latency estimate
```

---

## Prompt-invariance metrics

Across N phrasings of one underlying intent:

**Must be invariant** — explicit constraints, entity identity and invariants, exact copy,
objective class, supplied assets and their roles, prohibitions, delivery requirements.

**May legitimately differ** — system decisions, free fields, some derived detail.

**Must be semantically equivalent** — derived facts.

Three measures:

| Metric | Question |
|---|---|
| **Explicit Intent Preservation** | Of everything the user stated, how much survived intact? |
| **Explicit Intent Mutation** | Did a surviving field change meaning? ("premium but not luxury" → "ultra-luxury editorial") |
| **Incorrect Autonomous Decision** | Two counted cases only — see below |

Mutation is the subtle one: the field is present, provenance still reads `user`, and the value
has drifted. Preservation rate alone would score that as a pass.

Filling gaps is the product's job, so raw invention count would penalise it for working. Only
two things count as incorrect autonomous decisions:

1. A `system_decided` value recorded with `provenance: user` — always a bug.
2. A value decided where the correct operation was `ask` — a judgment error, gradable.

All three are text-only. The whole invariance grid runs without generating an image.

---

## Open questions

1. `hierarchy` element references need a naming scheme that survives compilation.
2. Multi-asset jobs (a campaign, not an asset) — out of scope for v0.1.
3. Whether `visual_language` belongs in Core or splits across both extensions.
4. Readiness weighting — deliberately deferred to real examples.

## Next

Atom Schema v0 derives from this file. An atom earns its place by naming the IR decisions it
improves — `informs:` must point at real IR field paths. No consumer, no atom.
