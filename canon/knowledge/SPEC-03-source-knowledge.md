# Spec 03 — Source Knowledge v0

**Date:** 23 Aug 2026 · **Status:** new layer, built alongside SPEC-02 (superseded, retained)
**Supersedes conceptually:** SPEC-02's admission test, not its files.

## Why this layer exists

SPEC-02 admitted knowledge by asking:

> Does this inform a field in today's Creative IR?

The six-source probe showed that test is wrong in both directions. It **excluded** durable
knowledge that had no current consumer — *Light: Science & Magic*'s family of angles, the book's
central concept, was filed as a note. And it **admitted distortion**, because an extractor that
must find a binding will find one: `mb_004` ("bigger reads as stronger") was recorded as informing
`entities.role`, which is our product's word, not Molly Bang's idea.

The clearest evidence is internal. SPEC-02's own worked counter-example was
`pointed_shapes_read_as_threatening`, presented as knowledge that informs nothing and belongs in
human notes. The actual extraction made it `mb_011`, an atom informing `creative.visual_language`.
The same knowledge was unbindable in the specification and bound in practice, three days apart.
**`informs` is elastic. It cannot carry an admission decision.**

So this layer records what a source teaches. Whether today's product can use it is
[SPEC-04](SPEC-04-operational-bindings.md)'s question, and a Source Knowledge object with zero
bindings is a normal, healthy object.

## What this layer must never contain

- `informs` paths, or any reference to a Creative IR field
- registered product failure or repair terms
- a `status` that gates on product usefulness
- an uncalibrated decimal confidence
- our vocabulary inside a field claiming to be the source's

That last one is not theoretical. `mb_002`'s diagnostic currently reads *"Is the **rank-1 element**
at or near centre"* — SPEC-01 vocabulary embedded in an object that claims to be source-faithful.

---

## Object 1 — SourceKnowledge

```yaml
sk_id: sk_mb_0002
source_id: molly_bang_picture_this

# ── NAMING ──────────────────────────────────────────────────
source_terms:                    # the source's own words, verbatim where useful
  - "the center of the page is the most effective 'center of attention'"
concept_label: centre_as_strongest_attractor
label_origin: extractor_assigned    # extractor_assigned | source_verbatim

# ── THE CLAIM ───────────────────────────────────────────────
claim: >
  The centre of the frame is the strongest point of attraction. An element placed there
  holds the eye and resists the viewer moving away from it.

claim_type: explicit_source_claim   # explicit_source_claim | source_interpretation
interpretation_basis: null          # REQUIRED when claim_type is source_interpretation:
                                    # what we inferred it from, and why

mechanism:
  stated_by_source: true
  text: "The enclosing edges push attention inward; the centre both receives and radiates that force."

# ── SCOPE ───────────────────────────────────────────────────
scope:
  domain_discussed_by_source: [picture_book_illustration]   # what the SOURCE is about.
                                                            # NOT where we might apply it.
  conditions: "any framed composition"

caveats:
  - text: "square and circular frames intensify the effect"
    origin: source_stated          # source_stated | extractor_observed
  - text: "the source's demonstration also varies value contrast, so the variable is not isolated"
    origin: extractor_observed

# ── SOURCE'S OWN PROBLEM / REMEDY LANGUAGE ──────────────────
# Preserved in the source's frame. NOT product vocabulary. NOT registered anywhere.
source_stated_problems:
  - "the eye gets stuck and will not travel"
source_stated_remedies:
  - "keep the main emphasis away from the centre"

# ── EXAMPLES ────────────────────────────────────────────────
examples:
  positive:
    - {description: "red triangle centred in a white burst on black", figure_ref: p63}
  counter:
    - {description: "same burst displaced to upper left; the eye moves", figure_ref: p65}

# ── RELATIONS WITHIN THIS SOURCE ────────────────────────────
intra_source_relations:
  - {relation: trades_off_with, target: sk_mb_0003, note: "centring holds the eye; exploration requires releasing it"}
  # relation vocabulary: qualifies · qualified_by · trades_off_with · depends_on ·
  #                      generalises · specialises · contradicts · demonstrated_together_with
  - {relation: member_of_system, target: scs_mb_001}

# ── EVIDENCE ────────────────────────────────────────────────
evidence:
  characteristics:
    - explicitly_stated
    - visually_demonstrated
    - controlled_comparison        # minimal pair: one variable changed
  source_uncertainty: none         # none | source_hedges | source_asks_open_question |
                                   # source_states_it_as_tradition | source_concedes_difficulty
  extraction_uncertainty: none     # none | column_interleaving | figure_not_inspected |
                                   # ocr_degraded | inferred_from_layout | ambiguous_referent

# ── PROVENANCE ──────────────────────────────────────────────
provenance:
  chapter: null
  section: "Principle 5"
  page_start: 62
  page_end: 67
  figure_refs: [p63, p65]
  source_support: text_and_visual  # text | visual | text_and_visual
  inspected:
    text: true
    figures: [p63, p65]            # which figures a human or extractor actually looked at
```

### Evidence characteristics — the controlled vocabulary

Factual descriptions of how the source supports the claim. Multiple may apply. These replace the
decimal confidence field entirely.

```
explicitly_stated            the source says it in words
visually_demonstrated        the source shows it
controlled_comparison        minimal pair — one variable changed, others held
argued                       reasoned from stated premises
practitioner_assertion       asserted from professional experience
anecdotal                    supported by a specific recounted case
outcome_claimed              a result is claimed (sales, response) without controls
empirical_within_source      the source reports its own measurement
repeated_within_source       stated more than once, or restated in a summary
mechanism_given              the source explains why
mechanism_absent             the source states the effect but not the cause
culturally_bounded           the source scopes it to a culture or period
historical_claim             a claim about what was true when written
```

**No aggregation happens here.** Cross-source agreement is computed later from many
SourceKnowledge objects — never asserted inside one. A single object cannot know it is corroborated.

---

## Object 2 — SourceConceptSystem

Some knowledge only exists in the relationships between principles. Atomising it destroys it.

Molly Bang's book is the clear case: eight of the eighteen extracted atoms carry the same
emotional register, and two of them — centre-as-attractor and centre-avoidance — are a trade-off
pair that is incoherent when either is retrieved alone. `mb_008` even contains the relationship
inside its own principle text ("a horizontal placed across verticals restores order"), which is a
system leaking into an atom because there was nowhere else for it to go.

```yaml
scs_id: scs_mb_001
source_id: molly_bang_picture_this
label: emotional_register_of_pictorial_structure
label_origin: extractor_assigned

system_type: interacting_set
system_type_origin: extractor_inferred      # source_stated | extractor_inferred
# trade_off_set | priority_order | sequence | decision_framework |
# causal_model | interacting_set | mutual_qualification

description: >
  A set of structural choices — horizontal, vertical and diagonal emphasis, vertical half,
  shape contour, ground value, colour — that jointly determine a picture's emotional reading.

# ── WHOLE-SYSTEM CLAIM ──────────────────────────────────────
whole_system_claim:
  text: >
    The registers combine and can cancel. A horizontal placed across verticals restores
    stability; the same element against a different ground value changes register entirely.
    The emotional reading is a property of the combination.
  origin: extractor_synthesis                # source_explicit | extractor_synthesis
  interpretation_basis: >                    # REQUIRED when origin is extractor_synthesis
    The source never states this as a general claim. It is synthesised from the fact that the
    book builds one picture and changes one dimension at a time, and from mb_008's own text
    ("a horizontal placed across verticals restores order"), which states a cross-principle
    interaction inside a single principle.
  source_ref: null                           # provenance when origin is source_explicit

members:
  - {sk_ref: sk_mb_0007, role_in_system: dimension, order: 1, membership_origin: source_stated}
  - {sk_ref: sk_mb_0008, role_in_system: dimension, order: 2, membership_origin: source_stated}
  - {sk_ref: sk_mb_0009, role_in_system: dimension, order: 3, membership_origin: source_stated}
# membership_origin: source_stated | extractor_inferred
# "source_stated" means the source groups these together — here, by numbering them in one series.

internal_structure:
  ordering:
    scheme: source_numbered                  # source_numbered | causal | procedural | none
    origin: source_stated
  dependencies: []
  tradeoffs:
    - between: [sk_mb_0002, sk_mb_0003]
      nature: "holding the eye vs releasing it to explore"
      origin: source_stated
      source_ref: {section: "Principle 5 preamble", page_start: 62}
  conflicts: []

source_warns_against_isolated_use: false
source_warning_ref: null

evidence:
  characteristics: [explicitly_stated, visually_demonstrated, repeated_within_source]
  source_uncertainty: none
  extraction_uncertainty: none
  system_level_uncertainty: >                # distinct from member-level uncertainty
    Members are individually well supported. The claim that they form ONE system is ours.

provenance:
  section: "The Principles"
  page_start: 42
  page_end: 91
  source_support: text_and_visual
```

### Origin marking is required at every structural level

A system asserts more than its members do, and most of what it asserts is usually **ours**. Every
structural element therefore carries an origin:

| Element | Field | Values |
|---|---|---|
| System type | `system_type_origin` | `source_stated` · `extractor_inferred` |
| Whole-system claim | `whole_system_claim.origin` | `source_explicit` · `extractor_synthesis` |
| Membership | `members[].membership_origin` | `source_stated` · `extractor_inferred` |
| Ordering | `internal_structure.ordering.origin` | `source_stated` · `extractor_inferred` |
| Dependencies | `dependencies[].origin` | `source_stated` · `extractor_inferred` |
| Trade-offs | `tradeoffs[].origin` | `source_stated` · `extractor_inferred` |
| Conflicts | `conflicts[].origin` | `source_stated` · `extractor_inferred` |

`extractor_synthesis` on a whole-system claim **requires** `interpretation_basis`. Without it the
system is asserting something no one said and nothing records who said it.

The distinction is not cosmetic. Ogilvy's working procedure is `source_stated` ordering — he
numbers the steps under sequential headings. Molly Bang's emotional-register system is
`extractor_inferred` grouping over `source_stated` numbering: she numbers her principles, but the
claim that eight of them constitute one interacting register is ours. Lupton's cue economy sits
between: the three-cue ceiling and the one-signal rule are both hers, but the observation that
they **reconcile each other** is synthesis.

A system may be entirely `extractor_inferred`. That is legitimate and must be visible, because a
fully inferred system is a hypothesis about a source, not a report of one.

A system may reference members that have no bindings of their own. A system may itself have
bindings ([SPEC-04](SPEC-04-operational-bindings.md)) that none of its members has.

---

## Validation rules

Mechanical, and deliberately fewer than SPEC-02 had:

1. `claim_type` present. If `source_interpretation`, `interpretation_basis` is non-empty.
2. `evidence.characteristics` non-empty, drawn from the fixed list.
3. `provenance` resolves to a page range or an equivalent locator, and names `source_support`.
4. `provenance.inspected.figures` lists what was actually looked at — empty is legitimate and
   informative, but `source_support: visual` with no inspected figures is a validation failure.
5. `mechanism.stated_by_source` present. `false` is a normal value, not a defect.
6. No field may contain a Creative IR path, a registered product term, or product vocabulary.
7. `caveats[].origin` distinguishes what the source limited from what we noticed.

There is deliberately **no rule about usefulness**. A SourceKnowledge object is valid if it
faithfully records what a source teaches.

## What this changes for extraction

Pass 1 no longer has to find a consumer. It records the claim, how the source supports it, what
the source itself calls the problem and the remedy, and how the claim relates to its neighbours
in the same book. That is a smaller and more honest job, and it removes the pressure that
produced eighteen atoms and zero rejections from the first book we tried.
