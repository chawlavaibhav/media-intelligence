# Audit Gate v0.2 — adopted Canon method

**Status: AUTHORITATIVE.** Adopted by the Controller on 25 Aug 2026
(`canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`) and applied by CANON-005.

This document is the normative procedure and schema for the Post-Extraction Audit Gate. It is a
**Canon method layer**, not a new authoritative spec — CANON-004 concluded that no `SPEC-06` was
required. The only authoritative spec change it carries is the independence rule in SPEC-05
Governance rule 5.

| | |
|---|---|
| Active records | `canon/audit/records/*.audit.yaml` — exactly one per accepted source |
| Validator | `canon/validation/validate_audit_gate_v02.py` |
| Tests | `tests/test_validate_audit_gate_v02.py` |
| Design evidence | `canon/findings/CANON-004-audit-gate-design.md` |
| Experiment history | `canon/experiments/audit-gate-v0.2/README.md` (pointer only — nothing active) |

Unchanged by adoption: SPEC-01, SPEC-03 and SPEC-04.

## The gate — required order

A source becomes **accepted downstream knowledge** only by passing through these steps in order.
This ordering is authoritative.

```
1. source extraction stabilises                       SPEC-03
2. source systems / ontology stabilise                SPEC-05
3. OperationalBindings stabilise                      SPEC-04
4. fresh checkpoint is committed
5. Audit Gate record is written against those exact bytes    ── this document
6. Audit Gate validator passes
   ─────────────────── THE GATE ───────────────────
7. only now may any of the following treat the source as accepted knowledge:
      · cross-source promotion (SPEC-05 cross_source_concept)
      · downstream product / application use
      · Canon-consumption / retrieval work
```

**An unaudited or stale source may remain in the repository as source evidence.** It is not
deleted, hidden or devalued. It simply may not pass the three gates in step 7. That distinction
matters: the gate governs *downstream consumption*, not whether knowledge is worth keeping.

**Bindings are still not mandatory.** Nothing in this order reintroduces the retired rule that every
object must name a Creative IR field. Step 3 stabilises whatever bindings exist, and zero is a
normal count.

The Audit Gate reads the frozen record and writes a **new, separate file**. It never writes into
`source-knowledge.yaml`, `source-concept-systems.yaml`, `ontology-mappings.yaml` or
`operational-bindings.yaml`. That separation is the whole design: CANON-003's central finding was
that mixing product questions into source extraction distorts the source, so the second look has to
happen in its own layer, after the first one is finished and sealed.

## Anti-score rule

The audit answers *what kind* of thing something is. It never answers *how good* it is.

The validator therefore rejects any record containing a key matching
`score`, `rank`, `rating`, `grade`, `quality`, `strength`, `weight`, `tier`, `confidence` or
`credibility`, at any depth. Categories are unordered sets. Where the model lists values, the list
order carries no meaning.

This is a mechanical guard against the failure the task names explicitly: a field that acts as a
hidden credibility score. It is not a complete guard — a reader can still count the members of a
category and treat the count as a ranking — and that residual risk is stated in the design document
rather than pretended away.

---

## The record

One file per accepted source, at `canon/audit/records/<knowledge-dir-name>.audit.yaml`.
Exactly one active record per accepted source; there is no second editable copy anywhere.

```yaml
audit_record_version: v0.2-experimental
audit_id: aud_<short_source_slug>
source_id: <the source_id used in the frozen source-knowledge.yaml>
knowledge_dir: canon/knowledge/current/<dir>
recorded_at_commit: <sha>          # INFORMATIONAL ONLY - not enforced. See below.
audit_status: complete | evidence_insufficient
source_snapshot:                   # ENFORCED. The single version mechanism.
  algorithm: sha256-of-sorted-path-and-content
  files:
    - path: ontology-mappings.yaml
      digest: <sha256 of the file's bytes>
    - path: operational-bindings.yaml
      digest: <sha256>
    - path: source-concept-systems.yaml
      digest: <sha256>
    - path: source-knowledge.yaml
      digest: <sha256>
    - path: visual-evidence-ledger.yaml
      digest: <sha256>
  combined_digest: <sha256 over the canonical join>
evidence_basis_for_this_audit: [<repository paths actually read>]
source_reopened: false            # true only if the original book had to be opened again
```

`audit_status: evidence_insufficient` is a legitimate completed outcome. It means the committed
repository record does not settle the audit's questions and the original book would have to be
re-opened. It is **not** the same as an unwritten audit, and the validator requires an explicit
reason for it.

### The source snapshot — proving the audit is not stale

An audit record describes a source representation **at one moment**. If that representation later
changes, the audit is stale. Because this gate blocks cross-source promotion and downstream product
use, a stale record that keeps validating is worse than no gate at all: a consumer would be told the
source had been audited when the thing audited no longer exists.

`source_snapshot` closes that. It is a deterministic content fingerprint of the frozen artifacts the
audit was written against. The validator recomputes it from the files on disk and fails if anything
has moved.

**How it is computed.** For each covered file, the SHA-256 of its raw bytes. Paths are relative to
`knowledge_dir` and are processed in **lexicographic order**, so the result depends only on file
contents — never on filesystem ordering, clock, locale or git state. The `combined_digest` is the
SHA-256 of the UTF-8 encoding of `"{path}:{digest}\n"` joined over those sorted entries.

Per-file digests are recorded alongside the combined one so the validator can name *which* artifact
moved rather than only reporting that something did.

**What is covered, and why each file is in.** A file belongs in the snapshot when a change to it
would falsify something the audit asserts. Not for completeness.

| File | Why the audit depends on it |
|---|---|
| `source-knowledge.yaml` | `sk_refs` resolve into it; `evidence_origin` is cross-checked against its `empirical_within_source` characteristics; `source_id` must match it |
| `operational-bindings.yaml` | `application_fit` findings cite its `binding_id`s |
| `source-concept-systems.yaml` | bindings resolve `source_system_refs` into it, and audit prose cites system-level fields such as `source_warns_against_isolated_use` and `priority_order` |
| `ontology-mappings.yaml` | the layer whose `cross_source_concept` promotion the lineage audit governs; audit prose also cites remedy `executable_by` values from it |
| `visual-evidence-ledger.yaml` | `representation_integrity` is derived from it, and nothing else would detect a change to Area A |

**Explicitly excluded: `PROVENANCE.md`.** It is narrative prose, not a machine-consumed
representation, and the factual content the audit takes from it — delivery format, page
addressability, the evidence for each — is restated inside the audit's own fields, where it is
visible and reviewable. It stays in `evidence_basis_for_this_audit` as informational provenance.

**One version mechanism, not two.** `recorded_at_commit` is informational provenance: it says which
repository state a human was looking at. The validator **does not read it**, and a test asserts that
changing it has no effect. `source_snapshot` is the only enforced check. Git history is deliberately
not the mechanism — a content fingerprint survives rebases, squashes, cherry-picks and worktree
moves, all of which change a commit SHA without changing a single byte of the audited source.

**There is deliberately no snapshot-refresh tool.** Refreshing a snapshot against changed content
without re-examining the source would rubber-stamp exactly the staleness this field exists to catch.
When a source legitimately changes, the correct response is to re-run the Audit Gate for that book,
which produces a new snapshot as a by-product. `compute_source_snapshot()` is exposed as a function
for that purpose and for the tests.

---

## A. Representation integrity

> What did the copy we actually had make unavailable, misleading or impossible to check?

```yaml
representation_integrity:
  delivery_format: <enum>
  page_addressability: <enum>
  page_addressability_evidence: >
  inspection_state: <enum>
  visual_argument_role: <enum>
  observed_loss_patterns:
    - pattern: <enum>
      affects: >
      detectability: <enum>
      recoverability: <enum>
      evidence: >
  claim_resolution_after_inspection: all_resolved | some_underdetermined | not_applicable
  consequence: >
```

### `delivery_format`

`authored_print_scan` · `publisher_epub` · `native_digital_pdf` · `converted_pdf` ·
`repository_text_extract` · `unknown`

### `page_addressability`

`authored_pages` · `no_pages_reflowable` · `converter_pages_not_authored` · `pages_unknown`

**Why this is separate from format.** Book 7 (*The Photographer's Eye*) is a PDF whose 214 A4 pages
were made by calibre out of an ebook. It renders. It has page numbers. Every one of them is the
converter's invention, and the book's own five internal cross-references all point to the wrong
place in it — the check that established the fact (LA-11). A file type cannot tell you whether a
page is the author's. Recording those as two fields is what makes "there is no page" (book 6)
distinguishable from "there is a page and it is a lie" (book 7).

### `inspection_state` and `visual_argument_role` — the two-axis fix

`inspection_state`: `inspected_page_level` · `inspected_figure_level` · `inspected_no_page_available`
· `inspected_but_required_dimension_destroyed` · `not_inspected_access_blocked`

`visual_argument_role`: `no_visual_argument` · `illustrative_only` · `figure_carries_content` ·
`page_layout_is_the_argument` · `source_is_its_own_specimen`

CANON-003 used a single field, `visual_completeness`, and the 16 lanes invented **seven different
values** for it with no controlled vocabulary and no validator check:

```
verified_page_level (6) · verified_figure_level (3) · blocked_visual_validation (3)
not_verified_page_layout (2) · partial_figures_only (1) · partial_reflowed_layout (1)
```

That one field was carrying two unrelated questions at once — *how far did the inspection get* and
*how much was there to inspect* — and Lane D caught it doing so. `verified_figure_level` on book 16
(*Creativity, Inc.*) means "we measured all 33 images and none of them argues anything"; the same
value on book 18 (*Building a StoryBrand*) means "we opened the figures and they contained a field
schema the prose never states" (D-03, D-12). Same recorded value, opposite meanings.

Splitting the axes fixes it without inventing a risk number:

| Source | inspection_state | visual_argument_role |
|---|---|---|
| *Creativity, Inc.* | `inspected_figure_level` | `no_visual_argument` |
| *Building a StoryBrand* | `inspected_figure_level` | `figure_carries_content` |
| *Making and Breaking the Grid* | `inspected_no_page_available` | `source_is_its_own_specimen` |
| *Interaction of Color* | `inspected_but_required_dimension_destroyed` | `figure_carries_content` |
| *Ogilvy on Advertising* | `not_inspected_access_blocked` | `figure_carries_content` |

The last two rows are the reason `blocked_visual_validation` had to be split: Albers's file opened
perfectly and every page rendered, but the digitisation is greyscale and the book is about colour;
Ogilvy's file was simply unreachable. Both were recorded as the same value in CANON-003 and they are
not the same problem — one is permanent damage inside the artifact, the other was fixed by a macOS
permission (B-13).

### `observed_loss_patterns[].pattern`

Each value below was observed in at least one accepted book. This is a list of **shapes**, not
severities. There is deliberately no aggregate risk value.

| Pattern | Books | What it is |
|---|---|---|
| `no_authored_page` | 5 | the format has no page at all; not a fault, and unfixable in this copy |
| `no_loss_detected` | 3 | the pass ran and found nothing missing |
| `in_figure_text_absent` | 3 | words typeset inside a figure are missing from the text layer |
| `text_layer_order_damage` | 3 | reading order disturbed, from cosmetic to a buried section |
| `named_loss_with_unstated_content` | 3 | the text points at a figure whose content it never states |
| `heading_carried_as_image` | 2 | section titles exist only as artwork, flattening the structure |
| `display_type_ocr_damage` | 2 | OCR errors confined to running heads, drop caps and logotypes |
| `required_visual_dimension_destroyed` | 1 | the figure survives; the property the argument needs does not |
| `figure_inspected_claim_underdetermined` | 1 | the figure was looked at and the claim still is not settled |
| `false_page_affordance` | 1 | a converter's pages look addressable and are not the author's |
| `demonstration_performs_the_claim` | 1 | the evidence is the reader's own act of looking |
| `source_evidence_never_printed` | 1 | the evidence was absent from the original book |
| `announced_loss_placeholder` | 1 | the file contains literal placeholders where evidence was |
| `caption_coverage_uneven` | 1 | captions exist for some figures, and the uncaptioned ones are not random |

Counts are distinct books out of 16, from the committed records. They are an inventory, not a
severity ordering.

`source_evidence_never_printed` earns its place by being the one pattern that is **not** our problem.
Hopkins argues from advertisements the 1923 book never reproduced. A 1923 reader was in exactly the
same position as we are. Filing that with digitisation losses would misattribute the gap.

### `detectability` and `recoverability`

`detectability`: `silent` · `named_by_text` · `announced_by_placeholder` · `detected_by_independent_check`

`recoverability`: `recovered_in_this_copy` · `recoverable_not_attempted` · `unrecoverable_in_this_copy`
· `not_applicable`

Ledger issue B-15/B-18 established that **severity tracks detectability, not amount**. Announced and
named losses are recoverable in principle because you know exactly what to go and find. Silent loss
is the dangerous kind, and the two silent cases in this corpus — Samara's in-figure notation and
Grammar of the Edit's diagram labels — were each found only by the visual pass itself.

`recoverability` records something the CANON-003 vocabulary could not say at all (LA-02): the
difference between *we have not looked hard enough yet* and *this copy will never contain it*.
Samara's missing page is `unrecoverable_in_this_copy` forever, and any downstream process treating
that as pending work is wrong.

---

## B. Evidence and claim origin

> Whose evidence is this, and did the source actually supply it?

```yaml
evidence_origin:
  audit_scope: all_objects | notable_objects_only | evidence_insufficient
  audit_scope_note: >
  categories:
    - category: <enum>
      sk_refs: [sk_...]
      evidence: >
  relation_to_evidence_characteristics: >
```

### Categories

| Category | Means |
|---|---|
| `source_own_measurement_reported` | the source measured something and tells you what it got |
| `measurement_claimed_result_not_supplied` | the source says a test happened and never says what it returned |
| `third_party_measurement_reported` | a named outside study, reported by the source |
| `mixed_own_and_third_party` | both, inside one object's evidence |
| `source_author_assertion` | the author says it in their own voice |
| `source_quotes_named_third_party` | the author quotes an identified person, approvingly |
| `source_quotes_unnamed_third_party` | "research shows", with no researcher named |
| `origin_unresolved` | the source does not permit a stronger statement |

### Why this is not a duplicate of `evidence.characteristics`

SPEC-03 has one relevant characteristic, `empirical_within_source`, defined as *"the source reports
its own measurement"*. That single slot is asked to answer two questions at once, and Lane C broke it
in three different directions across three books (C-01, C-13, C-23):

| Book | What the source does | What the one characteristic can record |
|---|---|---|
| Hopkins | claims tests constantly, reports almost no result | applying it credits evidence never supplied; withholding it loses the fact that the source *claims* an empirical basis |
| Heath & Heath | reports measurement constantly, almost none of it their own | cannot credit evidence that genuinely was supplied |
| Sutherland | his own field experiment *and* cited Duke research, in one section | needs two values in one source and has one |

Lane D found the adjacent case from the other side (D-02): a claim Catmull quotes from Andrew
Stanton, or that *Art & Fear* quotes from Joan Didion, is neither the author's own assertion nor a
third-party measurement, and has nowhere to live. In every one of these books the extractor did the
right thing — recorded the truth in an `extractor_observed` caveat — and the truth ended up in prose
that nothing can count.

The audit layer does not change `evidence.characteristics`. It records the origin question separately
and **cross-checks against** the frozen field. The validator enforces one consistency rule:

> every `sk_id` listed under `source_own_measurement_reported` must carry `empirical_within_source`
> in the frozen source record, and no `sk_id` listed under `third_party_measurement_reported` or
> `measurement_claimed_result_not_supplied` may carry it.

That rule is what makes the two layers agree instead of drifting. It reads the frozen file and never
writes to it.

---

## C. Application fit

> Now that source truth is settled, can anything we are building actually use this?

```yaml
application_fit:
  audited: true | false
  not_audited_reason: >            # required when audited is false
  findings:
    - consumer: <enum>
      outcome: <enum>
      existing_binding_refs: [bnd_...]
      note: >
  unbound_knowledge_of_note:
    - sk_refs: [sk_...]
      observation: >
  conclusion: >
```

`consumer`: `creative_ir` · `production_ir` · `evaluation` · `governance` · `benchmark` ·
`deterministic_composition` · `human_workflow`

`outcome`: `binding_exists` · `candidate_no_binding_made` · `no_current_binding` ·
`blocked_target_schema_absent`

**Every consumer in the list must appear exactly once when `audited: true`.** That is the mechanism
that restores the attention the old mandatory-binding rule used to force, without restoring the rule
itself. The old method made you name a Creative IR field for every atom, which guaranteed the
question was asked and guaranteed the answer was often a distortion (B-07, B-09, B-14). This asks the
question once per source per consumer, after the source is frozen, and accepts `no_current_binding`
as a full answer.

`no_current_binding` versus `not audited` is structural, not a convention: `audited: false` has no
`findings` at all and requires `not_audited_reason`.

Two consumers in this list are deliberately **not** SPEC-04 `target_type` values.
`deterministic_composition` and `human_workflow` exist here because CANON-003 found knowledge that
fits neither a generative product nor a physical production step — Samara's exactly executable layout
geometry (LA-08), and remedies that act on a person rather than on material (D-01, LB-11). Naming a
fit in the audit is **not** creating a binding. Nothing in this layer adds a SPEC-04 target type, and
no binding may be written from an audit finding without going through SPEC-04 as it stands.

---

## D. Lineage and independence

> Are two sources that agree actually two sources?

```yaml
lineage:
  authors: [<name>]
  publisher: <string or null>
  series: <string or null>
  first_published: <year or null>
  copy_edition: <string or null>
  related_sources_in_corpus:
    - source_id: <other source_id>
      relation: <enum>
      evidence: >
  independence_verdict: <enum>
  independence_basis: >
  extractor_exposure:
    spec_contains_examples_from_this_source: true | false | unknown
    evidence: >
```

`relation`: `shared_author` · `same_series` · `companion_volume` · `derivative_of` · `cites_source` ·
`shares_publisher_only` · `no_known_relation`

`independence_verdict`: `independent_origin` · `not_independent_of_named_sources` ·
`independence_not_established`

### The promotion rule

SPEC-05's `cross_source_concept` is the only concept kind that makes a claim about the world, and its
only guard is that two or more `independent_origins` are listed. `independent_origins` holds source
identifiers. **Two source identifiers can share an author, a publisher, a series and a decade**
(LB-09). *Grammar of the Shot* and *Grammar of the Edit* are Thompson & Bowen, Focal Press, same
series, a year apart, each citing the other. They share four near-identical terms — `axis_of_action`,
`screen_direction`, `jump_cut`, `eye_line_match`. A promotion counting distinct source ids would read
that as two sources agreeing. It is one authorial position stated twice.

The candidate rule, mechanically checkable from the audit records alone:

> Two sources count as independent origins for a `cross_source_concept` **only if** neither one's
> audit record declares the other with relation `shared_author`, `same_series`, `companion_volume`
> or `derivative_of`.
>
> `shares_publisher_only` and `cites_source` do **not** by themselves defeat independence.
> `independence_not_established` blocks promotion against everything until resolved; it does not
> silently pass.

**Independence is a property of a pair, not of a source.** The first draft of this rule also
consulted a source-level `not_independent` verdict, and the corpus test immediately showed why that
is wrong: *Grammar of the Shot* is not an independent origin against its companion volume and is a
perfectly good one against *The Photographer's Eye*, Murch, Samara and every other source here. A
global flag would have thrown away fifteen usable pairings to catch one bad one. The source-level
verdict is therefore `not_independent_of_named_sources`, which points at the pairwise entries and
does not block on its own.

`cites_source` is deliberately not disqualifying. Book 9 citing book 1 is evidence of the same
authorship, but a source citing an unrelated source is normal scholarly behaviour and does not make
the two one origin.

The validator implements this as a function over the record set, and the test suite exercises it on
the real Grammar pair.

### `extractor_exposure`

Issue B-17 recorded a hole in the isolation rule: SPEC-04 and SPEC-05 themselves quote books this
batch processed — the *Light: Science & Magic* "specular" refusal appears as a worked example in both
specs. An extractor who has read the specs already knows that finding, so apparent convergence
between the fresh pass and the historical audit was not independent and had to be struck. Recording
it per source keeps that fact attached to the evidence instead of to a worker's memory.

---

## E. Technology contingency

> Is this claim still true, or did it expire with its technology?

```yaml
technology_contingency:
  applicable: true | false
  applicability_basis: >
  assessed: true | false
  classes:
    - class: durable_mechanism | technology_contingent | historical_convention | uncertain
      sk_refs: [sk_...]
      evidence: >
  existing_characteristics_relied_on: [historical_claim, culturally_bounded]
```

**No new vocabulary.** R-03 established that SPEC-03's existing `historical_claim` and
`culturally_bounded` characteristics can already express this, and that both were used correctly on
*Painting With Light* — 9 objects and 1 object respectively. What was missing was not a field, it was
a **step**: nothing forced the extractor to ask. Within a few pages Alton states optical geometry
that has not dated, film-stock practice that has dated completely, and a 1949 studio convention about
lighting women's faces stated as technical fact. All three carry `practitioner_assertion` and nothing
separates them.

So this section adds a required question, not a required word. `applicable: false` is a normal answer
and needs a basis; `applicable: true` with `assessed: true` requires at least one class entry.

---

## Validation rules

Implemented in `canon/validation/validate_audit_gate_v02.py`.

**Per record**

1. `audit_record_version`, `audit_id`, `source_id`, `knowledge_dir`, `audit_status` present.
2. `source_id` matches the `source_id` in the referenced `source-knowledge.yaml`.
2a. `source_snapshot` present, using the declared algorithm, covering exactly the five files above,
    with every declared digest matching the file on disk and the `combined_digest` internally
    consistent. A missing covered artifact is reported as such, not skipped.
3. Every `sk_ref` anywhere in the record resolves to an `sk_id` in that frozen file.
4. Every `bnd_` reference resolves to a `binding_id` in that book's `operational-bindings.yaml`.
5. All enum values drawn from the fixed lists above.
6. No forbidden score-like key at any depth (the anti-score rule).
7. `audit_status: evidence_insufficient` requires a non-empty reason.
8. `application_fit.audited: true` covers every consumer exactly once;
   `audited: false` requires `not_audited_reason` and forbids `findings`.
9. `evidence_origin` consistency against the frozen `empirical_within_source` characteristic.
10. `technology_contingency.applicable: true` + `assessed: true` requires at least one class.
11. `representation_integrity` requires `delivery_format`, `page_addressability`,
    `inspection_state`, `visual_argument_role` and at least one loss-pattern entry
    (`no_loss_detected` is a legitimate entry).

**Across the record set**

12. `audit_id` and `source_id` unique.
13. **Dependence** relations are symmetric: if A declares `shared_author`, `same_series`,
    `companion_volume` or `derivative_of` with B, B must declare a dependence back. Relations that
    do not defeat independence are deliberately not symmetric - `shares_publisher_only` is
    uninformative to mirror and `cites_source` is genuinely one-directional.
14. `independent_origins_ok(a, b)` implements the promotion rule and is exposed for use by any later
    cross-source promotion check. It **fails closed**: an `independence_verdict` outside the
    controlled vocabulary is refused rather than passed through, so a malformed record cannot
    silently qualify for promotion.
