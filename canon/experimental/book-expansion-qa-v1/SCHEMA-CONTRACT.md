# Shared schema contract — experimental book-expansion + Q&A lanes

**Every extraction lane MUST follow this file exactly.** It exists so that four parallel lanes
produce mechanically consolidatable output. A lane that invents a field, an enum value or a file
name breaks consolidation.

**This is experimental, non-live work.** Nothing here is accepted Canon. See `README.md`.

---

## 1. Files each source directory must contain

| File | Required | Contents |
|---|---|---|
| `PROVENANCE.md` | yes | source identity, edition, exact material available, span, local path/URL, fingerprint, overlap with live Canon, access basis |
| `source-knowledge.yaml` | yes | SPEC-03 SourceKnowledge objects |
| `source-concept-systems.yaml` | yes (may be an empty list) | SPEC-03 SourceConceptSystem objects — only where genuinely present |
| `operational-bindings.yaml` | yes (may be an empty list) | SPEC-04 bindings |
| `ontology-mappings.yaml` | yes | SPEC-05 terms / relationships / concepts |
| `qa-bank.yaml` | yes | the Q&A bank |
| `EXTRACTION-NOTES.md` | yes | method, hazards, what was deliberately not extracted, self-check results |

Write YAML, not JSON. Use 2-space indent. Every file starts with a `# comment` header naming the
source and stating `EXPERIMENTAL — NOT LIVE CANON`.

---

## 2. Identifier conventions

- `source_id` — the directory name, exactly (e.g. `hopkins-my-life-in-advertising`).
- `sk_id` — `sk_<short>_NNNN`, zero-padded 4, e.g. `sk_mla_0001`.
- `scs_id` — `scs_<short>_NNN`.
- `binding_id` — `bnd_<short>_NNN`.
- `term_id` — `t_<short>_NNNN`.
- `concept_id` — `sc_…` (source_specific), `cc_…` (canonical), `xs_…` (cross_source — **do not create
  any `xs_` concept in this task**; cross-source promotion is forbidden here).
- `qa_id` — `qa_<short>_NNNN`.

`<short>` per lane: `mla` (My Life in Advertising), `sa8` (Scientific Advertising ch8–21),
`wcag` (WCAG 2.2), `abcd` (Google ABCD).

IDs must be unique within the lane and must never collide across lanes (the `<short>` prefix
guarantees this).

---

## 3. SourceKnowledge — SPEC-03 shape (authoritative: `canon/knowledge/SPEC-03-source-knowledge.md`)

Required keys per object: `sk_id`, `source_id`, `source_terms`, `concept_label`, `label_origin`,
`claim`, `claim_type`, `interpretation_basis`, `mechanism`, `scope`, `caveats`,
`source_stated_problems`, `source_stated_remedies`, `examples`, `intra_source_relations`,
`evidence`, `provenance`.

```yaml
- sk_id: sk_mla_0001
  source_id: hopkins-my-life-in-advertising
  source_terms:                       # the SOURCE's own words. Short. Verbatim where useful.
    - "keyed advertisement"
  concept_label: some_snake_case_label
  label_origin: extractor_assigned    # extractor_assigned | source_verbatim
  claim: >
    What the source teaches, in our words, faithfully.
  claim_type: explicit_source_claim   # explicit_source_claim | source_interpretation
  interpretation_basis: null          # REQUIRED (non-null) when claim_type is source_interpretation
  mechanism:
    stated_by_source: true            # false is a normal, valid value
    text: "why the source says it works, or null"
  scope:
    domain_discussed_by_source: [mail_order_advertising]   # what the SOURCE is about, NOT where we might apply it
    conditions: "when the source says this holds"
  caveats:
    - text: "..."
      origin: source_stated           # source_stated | extractor_observed
  source_stated_problems: ["the source's own words for what goes wrong"]
  source_stated_remedies: ["the source's own words for the fix"]
  examples:
    positive: [{description: "...", figure_ref: null}]
    counter: []
  intra_source_relations:
    - {relation: qualifies, target: sk_mla_0002, note: "..."}
  evidence:
    characteristics: [explicitly_stated, practitioner_assertion]
    source_uncertainty: none
    extraction_uncertainty: none
  provenance:
    chapter: "Chapter Sixteen — Reasons for Success"
    section: null
    page_start: 167
    page_end: 170
    figure_refs: []
    source_support: text              # text | visual | text_and_visual
    inspected:
      text: true
      figures: []
```

### Fixed vocabularies (do not extend)

`evidence.characteristics` (≥1 required):
```
explicitly_stated  visually_demonstrated  controlled_comparison  argued
practitioner_assertion  anecdotal  outcome_claimed  empirical_within_source
repeated_within_source  mechanism_given  mechanism_absent
culturally_bounded  historical_claim
```

`source_uncertainty`: `none | source_hedges | source_asks_open_question |
source_states_it_as_tradition | source_concedes_difficulty`

`extraction_uncertainty`: `none | column_interleaving | figure_not_inspected | ocr_degraded |
inferred_from_layout | ambiguous_referent`

`intra_source_relations[].relation`: `qualifies | qualified_by | trades_off_with | depends_on |
generalises | specialises | contradicts | demonstrated_together_with | member_of_system`

`source_support`: `text | visual | text_and_visual`

### Hard prohibitions (SPEC-03 §"What this layer must never contain")

- No `informs` field, no Creative IR path, no `creative.*` / `entities.*` path anywhere.
- No product vocabulary inside a field claiming to be the source's (no "rank-1 element", no
  "Normalized Request", no "Capability Registry").
- No decimal confidence value anywhere.
- No `status` field that gates on product usefulness.
- **No cross-source claim.** A SourceKnowledge object cannot know it is corroborated.

---

## 4. SourceConceptSystem — SPEC-03 Object 2

Create one **only where the knowledge genuinely lives in the relationships**, not to look complete.
Zero systems is a valid outcome; a fabricated system is not.

```yaml
- scs_id: scs_mla_001
  source_id: hopkins-my-life-in-advertising
  label: some_label
  label_origin: extractor_assigned
  system_type: priority_order        # trade_off_set | priority_order | sequence |
                                     # decision_framework | causal_model | interacting_set |
                                     # mutual_qualification
  system_type_origin: extractor_inferred    # source_stated | extractor_inferred
  description: >
    ...
  whole_system_claim:
    text: >
      ...
    origin: extractor_synthesis      # source_explicit | extractor_synthesis
    interpretation_basis: >          # REQUIRED (non-null) when origin is extractor_synthesis
      ...
    source_ref: null                 # provenance when origin is source_explicit
  members:
    - {sk_ref: sk_mla_0004, role_in_system: step, order: 1, membership_origin: source_stated}
  internal_structure:
    ordering: {scheme: source_numbered, origin: source_stated}   # scheme: source_numbered | causal | procedural | none
    dependencies: []
    tradeoffs: []
    conflicts: []
  source_warns_against_isolated_use: false
  source_warning_ref: null
  evidence:
    characteristics: [explicitly_stated]
    source_uncertainty: none
    extraction_uncertainty: none
    system_level_uncertainty: >
      state plainly how much of this system is OURS rather than the source's
  provenance:
    chapter: "..."
    section: null
    page_start: 167
    page_end: 174
    source_support: text
```

**Origin marking is required at every structural level.** `extractor_synthesis` without a non-null
`interpretation_basis` is a validation failure.

---

## 5. OperationalBinding — SPEC-04

```yaml
- binding_id: bnd_mla_001
  source_knowledge_refs: [sk_mla_0004]      # or source_system_refs: [scs_mla_001]
  source_system_refs: []
  target_type: evaluation                   # creative_ir | evaluation | production | governance | benchmark
  target_path: null                         # REQUIRED non-null for creative_ir; null otherwise
  target_schema: null                       # 'SPEC-01' for creative_ir
  target_schema_version: null               # 'v0.1' for creative_ir
  role: [diagnoses]                         # fills | constrains | diagnoses | repairs | derives | flags | evaluates
  observation_unit: whole_asset             # REQUIRED for target_type: evaluation
                                            # frame | shot | shot_pair | sequence | whole_asset | asset_set_over_time
  governance_consumer: null                 # REQUIRED for target_type: governance, from the permitted list below
  rationale: >
    Our interpretation, recorded as ours. MUST NOT restate the source claim — reference it.
  applicability:
    when: "..."
    limits: >
      What the source actually covers vs where we would be applying it. Be honest.
  evidence_basis: derived_from_source       # derived_from_source | extractor_inference |
                                            # cross_source_supported | empirically_supported
  empirical_refs: []
  failure_ontology_refs: []                 # SPEC-05 identifiers from THIS lane's ontology-mappings.yaml
  repair_ontology_refs: []
  status: proposed                          # proposed | production_candidate
  status_reason: "experimental; not reviewed"
```

Permitted `governance_consumer` values (a binding that fits none of these **is not a governance
binding** — leave the knowledge unbound):
```
taxonomy_governance  retrieval_governance  conflict_resolution
evidence_interpretation  rule_application  cross_source_synthesis
```

### Binding rules that WILL be validated

1. `target_type: production` → `status: production_candidate` **and** `target_path: null`.
   Production IR does not exist. **Physical-production advice must not be rewritten as a
   generative-media instruction.** Record the source's action in the source's frame and mark it
   unbound.
2. `target_type: evaluation` → `observation_unit` present.
3. `target_type: creative_ir` → `target_path`, `target_schema`, `target_schema_version` all non-null.
4. `target_type: governance` → `governance_consumer` from the list above.
5. Every `source_knowledge_refs` / `source_system_refs` entry must resolve inside this lane.
6. Ontology refs must be SPEC-05 identifiers from this lane, never raw source strings.
7. `evidence_basis` present. Use `extractor_inference` honestly when you made a leap.
8. **Never** `cross_source_supported` or `empirically_supported` in this task — no cross-source
   promotion is authorised and there is no empirical evidence attached.
9. Zero bindings for a source is a legitimate outcome. Do not manufacture them.

---

## 6. Ontology mappings — SPEC-05

One file with three top-level keys: `terms`, `relationships`, `concepts`.

```yaml
terms:
  - term_id: t_mla_0001
    term: keyed_advertisement
    origin: source                  # source | empirical | customer | product  (use 'source' here)
    origin_ref: hopkins-my-life-in-advertising
    kind: property                  # problem | remedy | property | entity
    definition_in_origin_frame: >
      ...
    first_seen: 2026-08-30
    verbatim: true                  # is this the origin's actual word, or our label for it
    executable_by: null             # REQUIRED for kind: remedy —
                                    # physical_production | generative_respecification |
                                    # deterministic_composite | human_edit | unknown
relationships:
  - {from: t_mla_0001, to: t_sa8_0003, relation: related_to, confidence_basis: extractor_judgement, note: "..."}
concepts:
  - concept_id: sc_mla_something
    kind: source_specific_concept   # source_specific_concept | canonical_concept
    origin_ref: hopkins-my-life-in-advertising
    children_terms: [t_mla_0001]
    origin: source_stated           # source_stated | extractor_inferred
```

`relationships[].relation`: `maps_to | broader_than | narrower_than | related_to |
potentially_equivalent_to | distinct_from | same_failure_family | same_mechanism |
same_observed_effect | uncertain`

### Ontology rules that WILL be validated

1. **No `cross_source_concept` (`xs_…`) may be created in this task.** Cross-source promotion
   requires Controller review and Audit-Gate lineage records that do not exist here.
2. `same_failure_family` requires human review under SPEC-05 governance — **do not use it.**
3. A `canonical_concept` must carry `asserts_equivalence: false` and `purpose: retrieval_and_aggregation`.
4. A term is never edited to fit a concept. Concepts adapt to terms.
5. Record negative findings with `distinct_from` where you checked a resemblance and rejected it.
6. `kind: remedy` terms must carry `executable_by`. A remedy whose only value is
   `physical_production` is **not translated** into a generative instruction.
7. Cross-lane relationships (e.g. an `mla` term related to an `sa8` term) are permitted as
   `related_to` / `potentially_equivalent_to` / `distinct_from` only, and they are **observations**,
   not promotions. Anything stronger belongs in `CROSS-SOURCE-OBSERVATIONS.md` as prose.

---

## 7. Q&A bank — `qa-bank.yaml`

Top-level key `qa_items:`, a list. Every item carries exactly these keys:

```yaml
qa_items:
  - qa_id: qa_mla_0001
    source_id: hopkins-my-life-in-advertising
    source_title: "Claude C. Hopkins, My Life in Advertising (Harper & Brothers, 1927)"
    source_locator: "printed pp. 167-169 (Chapter Sixteen, 'Reasons for Success')"
    question: >
      ...
    answer: >
      ...
    answer_type: mechanism
    difficulty: medium
    knowledge_type: advertising
    requires_application: false
    support: >
      Concise paraphrase of the source claim(s) that support this answer, plus the locator.
      NOT a long quotation.
    confounders:
      - "a nearby idea a model could confuse with the correct answer"
```

### `answer_type` — exactly one of
```
factual  concept_definition  mechanism  comparison  tradeoff
failure_diagnosis  repair  application  boundary_condition  source_position
```

### `difficulty` — exactly one of
```
easy  medium  hard
```
Difficulty reflects **reasoning required**, not obscure wording.

### `knowledge_type` — exactly one of this fixed controlled vocabulary
```
advertising          persuasion            copywriting          effectiveness
testing_method       media_planning        brand_communication  concept_development
short_form           creative_process      production_reasoning evaluation_diagnosis
typography           hierarchy             composition          colour
photography          lighting              product_photography
editing              continuity            shot_design
accessibility_legibility                   indian_context
```

### Hard Q&A rules

1. **`source_locator` must point at the smallest practical real location.** For the Hopkins books
   use **printed page numbers**, which are marked in the supplied source text as
   `<<<PRINTED_PAGE n | PDF_PAGE m>>>`. Use the PRINTED number. **Never invent a page number.** For
   WCAG use the Success Criterion number or glossary term; for Google ABCD use page + section
   heading. Those two sources have **no page numbers** — do not fabricate any.
2. **Answers are concise paraphrase.** Do not reproduce long copyrighted passages. Short source
   terminology may be quoted where the exact term matters. The bank must be overwhelmingly
   paraphrase.
3. **At least one third of the bank must have `requires_application: true`** — questions that make
   the reader apply a source principle to a described situation, with the answer still grounded in
   the source.
4. **No question answerable from generic common sense.** If a competent person with no exposure to
   this source would answer correctly by default, the question is worthless — cut it or make it
   specific to what this source actually claims.
5. **`confounders` are mandatory and non-empty.** List nearby ideas a model might confuse with the
   correct answer — including ideas from *other* sources, and including the plausible-but-wrong
   modern default.
6. **Never attribute to the source something it did not claim.** If you are extrapolating, the item
   does not belong in the bank.
7. **Preserve source position.** Where the source states a practitioner opinion, an
   outcome claim without controls, or a claim contingent on its own era's technology, the answer
   must say so — use `answer_type: source_position` where the item is about what this source
   holds rather than about how the world is.
8. No empty or placeholder answers. No `TODO`.
9. Target mix, approximately (do not force it if the source will not support it):
   definitions/facts ~20% · mechanisms ~25% · comparisons/trade-offs ~20% ·
   diagnosis/application ~20% · boundaries/exceptions ~15%.
10. **Prefer fewer strong questions over many trivial ones.** If a source supports 18 good
    questions, write 18.

---

## 8. Extraction stance — what to extract and what to refuse

**Extract:** mechanisms · decision rules · trade-offs · failure conditions · diagnostic cues ·
repair principles · interactions between principles · boundary conditions · examples that reveal a
general mechanism.

**Refuse:** generic advice · motivational prose · repetition · biography · decorative examples with
no reusable principle.

**Epistemic rules that apply to every lane:**

- Source claims remain source claims. Practitioner opinion must not become universal truth.
- Do not turn physical-production advice into generative-media instructions unless the source itself
  supports that translation.
- Record applicability and limits.
- Preserve disagreement between sources rather than resolving it artificially; **do not manufacture
  cross-source agreement**.
- Keep technology-contingent and historical-convention knowledge labelled as such — use the
  `historical_claim` and `culturally_bounded` evidence characteristics, and say so in caveats.
- **Never infer current model capability from a book.** Nothing here is evidence about what any
  generative model can do.
- Where a figure carries essential meaning that the text alone does not, say so explicitly and use
  the caution name `figure_semantic_binding_lost` in `EXTRACTION-NOTES.md`.

---

## 9. Absolute write boundary

A lane may write **only** inside its own directory:
`canon/experimental/book-expansion-qa-v1/<source-id>/`

A lane must **never** create, edit or delete anything under:
`canon/knowledge/current/**` · `canon/audit/records/**` · `canon/knowledge/SPEC-*` ·
`coordination/**` · `eval/**` · `resources/**` · `governance/**` · `PROJECT-MEMORY.md`

Nothing produced here is accepted Canon, and no lane may describe it as accepted.
