# CANON-004 — Post-Extraction Audit Gate v0.2: design and test evidence

**Date:** 25 Aug 2026 · **Branch:** `work/canon-004` · **Status:** design/test complete, awaiting
Controller decision. SPEC-03, SPEC-04 and SPEC-05 are unchanged.

---

## 1. What was built, and what it costs

CANON-003 concluded that the Canon's three-layer architecture works and its *procedure* stopped
asking five useful questions. This task turned that into one concrete thing and tested it.

**The Audit Gate is a second file per book, written after the source record is frozen.** It reads
the frozen record and never writes to it. It answers five questions: what the copy hid, whose
evidence this is, what the product can use, whether two sources are really two, and whether an old
technical claim is still true.

All 16 accepted books now have one. The candidate schema, the 16 records, a validator and 32 tests
are committed on this branch.

**The headline result:** the gate catches every one of the four recurring CANON-003 failures, and it
needs **one** authoritative rule change to do it — a single addition to SPEC-05's governance
section. Everything else is additive: new files, new directory, no edit to any existing schema and
no edit to any accepted source claim.

**What it costs.** An audit record averages **154 lines** against an average `source-knowledge.yaml`
of 1,590 — roughly a **10 per cent** addition to a book's committed record, and slightly less than
the existing `visual-evidence-ledger.yaml` at 158 lines. Writing all 16 required no source book to
be re-opened; every record was built from committed repository evidence.

---

## 2. The four audits, and whether each one earned its place

### A. Representation integrity — **earned, and it fixes a field that was actively misleading**

CANON-003 recorded one value per book, `visual_completeness`. Sixteen lanes invented **seven
different values** for it, with no controlled vocabulary anywhere in SPEC-03/04/05 and no validator
check of any kind. That field was doing two unrelated jobs at once:

- how far did the inspection get?
- how much was there to inspect?

Lane D caught it doing so. `verified_figure_level` on *Creativity, Inc.* means "we measured all 33
images and none of them argues anything". The same value on *Building a StoryBrand* means "we opened
the figures and found a field schema the prose never states, including an eighth element in a
framework named for seven". **One recorded value, opposite meanings.**

The candidate splits the axes. `inspection_state` says how far we got; `visual_argument_role` says
what the source needed. Across the corpus:

| inspection_state | books | | visual_argument_role | books |
|---|---|---|---|---|
| `inspected_page_level` | 7 | | `figure_carries_content` | 8 |
| `inspected_figure_level` | 5 | | `no_visual_argument` | 5 |
| `not_inspected_access_blocked` | 2 | | `page_layout_is_the_argument` | 1 |
| `inspected_no_page_available` | 1 | | `source_is_its_own_specimen` | 1 |
| `inspected_but_required_dimension_destroyed` | 1 | | `illustrative_only` | 1 |

The split also separates two things CANON-003 recorded identically as
`blocked_visual_validation`. *Ogilvy* was unreachable because macOS privacy protection had locked
the library — a permission, later granted. *Interaction of Color* opened perfectly, rendered every
page, and its digitisation is greyscale for a book about colour: zero coloured pixels in 4,800
sampled per page, on every page tested. One was fixed by a click. The other is permanent.
`recoverability` now records that distinction directly.

**Fourteen loss patterns, from the corpus, not invented:**

| Pattern | Books | Pattern | Books |
|---|---|---|---|
| `no_authored_page` | 5 | `required_visual_dimension_destroyed` | 1 |
| `no_loss_detected` | 3 | `figure_inspected_claim_underdetermined` | 1 |
| `in_figure_text_absent` | 3 | `false_page_affordance` | 1 |
| `text_layer_order_damage` | 3 | `demonstration_performs_the_claim` | 1 |
| `named_loss_with_unstated_content` | 3 | `source_evidence_never_printed` | 1 |
| `heading_carried_as_image` | 2 | `announced_loss_placeholder` | 1 |
| `display_type_ocr_damage` | 2 | `caption_coverage_uneven` | 1 |

Four of these recur across three or more distinct books, which is the threshold CANON-003 set for a
structural finding. The singletons are kept because each names a mechanism no other value covers,
and a pattern list is cheap in a way that a schema field is not.

Two patterns are worth naming for the reader:

- **`false_page_affordance`** (*The Photographer's Eye*). A calibre-converted PDF with 214 A4 pages
  that render on demand. Every page number is the converter's. The book's own five internal
  cross-references all point to the wrong place — SQUARE cited as page 22 and found at page 29 —
  and one survives in the running text as the literal string `page_52`, underscore intact. A visual
  pass reasoning "this is a PDF, so I can inspect the page" would record verified page-level
  completeness for a layout that never existed. **File type cannot tell you whether a page is the
  author's.**
- **`source_evidence_never_printed`** (*Scientific Advertising*). Hopkins argues throughout from
  specific advertisements and the 1923 book reproduces not one of them. A reader in 1923 was in
  exactly our position. Filing this beside our digitisation losses would misattribute the gap and,
  worse, imply a remedy — find a better copy — that does not exist.

### B. Evidence and claim origin — **earned; strongest recurrence in the corpus**

SPEC-03 has one relevant characteristic, `empirical_within_source`: *"the source reports its own
measurement."* One slot, two questions. Lane C broke it in three directions across three books, and
Lane D broke it from a fourth:

| Source | What it does | What the one field can record |
|---|---|---|
| Hopkins | claims tests constantly, reports almost no result | applying it credits evidence never supplied; withholding it loses the fact that the source *claims* an empirical basis |
| Heath & Heath | reports measurement constantly, almost none of it theirs | cannot credit evidence that genuinely was supplied |
| Sutherland | his own field experiment *and* cited Duke research, one section | needs two values in one source and has one |
| Catmull / *Art & Fear* | quote named colleagues and endorse them | says nothing about voice at all |

In every case the extractor did the right thing and wrote the truth into an `extractor_observed`
caveat, where nothing can count it. The practical result, stated in *Made to Stick*'s own file
header: `sk_hea_mts_0023`, resting on Elizabeth Newton's controlled Stanford study — 120 songs, 3
identified, 2.5 per cent actual against 50 per cent predicted — and `sk_hea_mts_0017`, resting on
"it's difficult... but it's easier", are not cleanly separable by anything a machine reads.

Eight origin categories, applied across the corpus:

| Category | Books |
|---|---|
| `source_author_assertion` | 16 |
| `source_own_measurement_reported` | 7 |
| `source_quotes_named_third_party` | 3 |
| `measurement_claimed_result_not_supplied` | 3 |
| `third_party_measurement_reported` | 2 |
| `source_quotes_unnamed_third_party` | 1 |
| `mixed_own_and_third_party` | 1 |
| `origin_unresolved` | 0 |

**How this avoids duplicating `evidence.characteristics`.** It answers a different question, and the
validator forces the two layers to agree rather than drift:

> every `sk_id` listed under `source_own_measurement_reported` must carry `empirical_within_source`
> in the frozen record, and no `sk_id` under `third_party_measurement_reported` or
> `measurement_claimed_result_not_supplied` may carry it.

That rule reads the frozen file and never writes to it. It fires on the real corpus: Hopkins's four
reported-measurement objects all carry the characteristic and its seven claimed-without-result
objects all correctly lack it; *Made to Stick*'s four named third-party studies all correctly lack
it. Nine books needed no category beyond plain authorial assertion, which is the correct behaviour
for a mandatory step — the burden falls only where the evidence is genuinely mixed.

**A limit worth stating.** `outcome_claimed` already exists in SPEC-03 and overlaps this audit,
most visibly on *Building a StoryBrand*, whose four uncontrolled client-outcome claims carry both.
The two are adjacent, not identical: `outcome_claimed` says a result was asserted without controls;
the origin category says whose result it was and whether one was supplied at all. Hopkins is where
they come apart most sharply, and *StoryBrand* is where they nearly coincide.

### C. Application fit — **earned, and it recovers what the old rule got right**

CANON-003's clearest historical finding (B-14, four of four books with a comparator) was that the
old extraction kept noticing product-schema fit the fresh pass walked past, because the old rule
*forced* the question by requiring every atom to name a Creative IR field. The old answer was
usually wrong; the question was useful.

The gate asks the question once per source per consumer, after freeze, and accepts `no current
binding` as a full answer. Every one of seven consumers must appear exactly once. Results:

| Consumer | binding_exists | candidate_no_binding_made | no_current_binding |
|---|---|---|---|
| governance | 16 | — | — |
| evaluation | 15 | — | 1 |
| creative_ir | 14 | — | 2 |
| benchmark | 12 | — | 4 |
| production_ir | 7 | — | 9 |
| human_workflow | — | 7 | 9 |
| deterministic_composition | — | 1 | 15 |

`no_current_binding` is structurally distinct from `not audited`: `audited: false` carries no
findings at all and requires an explicit reason. The validator enforces both directions.

**Two consumers here are deliberately not SPEC-04 target types**, and naming a fit is not creating a
binding:

- **`human_workflow`** fired as a candidate in **7 of 16** books. The clearest is the Braintrust:
  a meeting format with preconditions, failure modes and a defined unit of feedback, the single most
  operational thing in *Creativity, Inc.*, acting entirely on people. SPEC-05's `executable_by`
  offers `physical_production`, `generative_respecification`, `deterministic_composite`,
  `human_edit` and `unknown`, and none of them is "change how a group talks to each other" (D-01,
  LB-11). Seven of sixteen is a real recurrence.
- **`deterministic_composition`** fired **once**, on Samara: nine of fourteen remedies are geometric
  operations a layout engine could execute exactly — add a column, hang a character, set a measure —
  and none is a generative control (LA-08). One in sixteen is weak, and it is kept only because that
  one hit is precisely the finding, not because the vocabulary needs symmetry. **This is the
  candidate's weakest component and the first thing to cut under ADOPT WITH REDUCTION.**

**The audit's most important negative result.** Lane D's D-13, confirmed here from the committed
bindings: *Creativity, Inc.* produced 21 objects and 0 Creative IR bindings; *Art & Fear* 23 objects
and 0; *Building a StoryBrand* 18 objects and 4 — on four uncontrolled outcome claims and a closing
position the extraction records as unfalsifiable as stated. **The source that binds best to the
product schema has the weakest support in the corpus.** Anything that later retrieves by
product-schema fit will surface that book and bury the mechanism-bearing ones, with nothing in the
system being wrong. This is why the application audit must never be read as a quality signal, and
why the anti-score rule below is mechanical rather than advisory.

### D. Lineage and independence — **earned; it is the only audit that changes a rule**

SPEC-05's `cross_source_concept` is the only concept kind that makes a claim about the world, and
its only guard is that two or more `independent_origins` are listed. That field holds source
identifiers. **Two source identifiers can share an author, a publisher, a series and a decade.**

*Grammar of the Shot* and *Grammar of the Edit* are Thompson & Bowen, Focal Press, same series, a
year apart, each citing the other. Four terms exist in both files with near-identical meaning —
`axis_of_action`, `screen_direction`, `jump_cut`, `eye_line_match`. Both books independently state
that their rules are defeasible by creative intent. Under a count of distinct `origin_ref`s that is
two sources agreeing. It is one authorial position stated twice.

The candidate rule:

> Two sources are independent origins **only if** neither audit record declares the other with
> relation `shared_author`, `same_series`, `companion_volume` or `derivative_of`.
> `shares_publisher_only` and `cites_source` do not defeat independence.
> `independence_not_established` blocks until resolved.

Tested against the committed records, not a fixture:

- the real Grammar pair is **rejected**, citing `companion_volume`;
- Murch against *Grammar of the Edit* — different author, publisher and decade, same subject — is
  **accepted**, which is the convergence the architecture exists to support;
- *The Photographer's Eye* against *Grammar of the Shot*, both Focal Press, is **accepted**;
- *StoryBrand* against *Alchemy*, both HarperCollins and actively disagreeing, is **accepted**.

**`cites_source` is deliberately not disqualifying.** A source citing an unrelated source is normal
scholarly behaviour. Book 9 citing book 1 is evidence of shared authorship, and shared authorship is
what the rule catches.

The record also carries `extractor_exposure`, for issue B-17. SPEC-04's worked governance example
*is* the *Light: Science & Magic* "specular" refusal, quoted in full, and SPEC-05 opens its rule
section with the same case. An extractor who read the specs already knew that finding, so the fresh
pass's apparent convergence with the historical audit was not independent and was struck. Two of
sixteen sources are flagged: *Light: Science & Magic* and *Grammar of the Shot*.

### E. Technology contingency — **earned, and it needs no new vocabulary**

R-03 is the cleanest single-source finding in CANON-003. Within a few pages, *Painting With Light*
states optical geometry that has not dated, film-stock practice that has dated completely — shiny
props wanted *because of antihalo film* — and a 1949 studio convention about lighting women's faces
stated as technical fact. **All three carry `practitioner_assertion` and nothing separates them.**

`historical_claim` and `culturally_bounded` already exist and both were applied correctly, by hand,
by reading. What was missing was not a field but a **step**: nothing forced the extractor to ask.

Three of sixteen sources were assessed as applicable — Alton (1949), Hopkins (1923), Ogilvy (1983).
Thirteen were marked not applicable with a stated basis. The contrast that shows the question is
real: Albers (1963) and Alton (1949) are both mid-century, and only one has technology-dependent
content, because Albers's subject is the eye and Alton's is equipment.

---

## 3. The anti-score rule

The task named a specific failure mode: a proposed field acting as a hidden credibility score. The
guard is mechanical. The validator refuses any record containing a key matching `score`, `rank`,
`rating`, `grade`, `quality`, `strength`, `weight`, `tier`, `confidence` or `credibility`, at any
depth, and two tests exercise it.

**It is not a complete guard, and pretending otherwise would be worse than admitting it.** A reader
can still count the members of an origin category, or count bound consumers, and treat the count as
a ranking. The D-13 result above is exactly what that misreading would produce. The mitigation is
partly structural — categories are unordered sets, list order carries no meaning — and partly a rule
for whoever consumes the Canon later: never rank by binding count, and carry the evidence profile
alongside any retrieved binding. That is a consumption-layer rule and belongs in the consumption
task, not here.

---

## 4. Two revisions forced by the corpus

Both were caught by applying the candidate to all 16 books rather than by inspection, which is the
argument for testing a method design against a whole corpus instead of a worked example.

**1. Symmetry only for dependence.** The first rule required every declared lineage relation to be
mirrored. Applied to the corpus it produced pure bookkeeping: `shares_publisher_only` is
uninformative to mirror, and `cites_source` is genuinely one-directional. Symmetry is now required
only for the four relations that defeat independence — where one-sided declaration would be a real
safety hole, because a promotion check reading only the other record would miss it.

**2. Independence is a property of a pair, not of a source.** The first rule also consulted a
source-level `not_independent` verdict. The corpus test failed immediately: that would block
*Grammar of the Shot* against Freeman, Murch, Samara and every other source in order to catch its one
real dependence on *Grammar of the Edit* — fifteen usable pairings thrown away to catch one bad one.
The verdict is now `not_independent_of_named_sources`, which points at the pairwise entries and does
not block on its own.

---

## 5. A defect found in the inherited corpus

The committed integration validator was **red on `main`** before this task made any change: 10
errors, all `t_hea_mts_0008` through `t_hea_mts_0017` in *Made to Stick*, lacking SPEC-05's required
`executable_by` on remedy terms.

This is not a new defect and not a contradiction of the integration record, which states plainly that
the full validator was never re-executed on the final head after the noisy GitHub Actions workflow
was removed. The mechanism is visible in the validator itself: it returns early on a YAML parse
failure. *Made to Stick*'s parse failure was one of the 24 catalogued defects, so that book's
term-level checks never ran in the run that produced the inventory. Repairing the quoting made the
file parseable and unmasked ten checks that had been skipped, and nothing re-ran to see them.

Repaired on this branch in its own commit (`00dd64b`), using the repair already precedented and
Controller-accepted for the same defect class: `executable_by: [unknown]`, exactly as applied to 16
Hopkins and 7 Sutherland remedies during integration. Additive only — 10 lines, no id, reference,
count, claim, concept, binding or relationship changed, term total unchanged at 417. The integration
validator now reports **0 errors** across 16 books, 505 objects, 54 systems, 417 terms, 53 concepts
and 111 bindings.

**The transferable lesson is about the instrument, not the data:** a validator that aborts a unit on
a parse error will under-report, and the shortfall is invisible in its own output. Proposed, not
applied: on a parse failure, report the file as unchecked rather than merely reporting the parse
error, so a later reader can tell "clean" from "not examined".

---

## 6. Exact proposed authoritative changes

### One change to an authoritative spec

**SPEC-05, Governance, rule 5.** Current text:

> **Only a `cross_source_concept` requires two or more independent origins.**

Proposed addition:

> Independence is established from the Audit Gate lineage records, not from a count of distinct
> `origin_ref` values. Two origins may be counted as independent only when neither source's audit
> record declares the other with relation `shared_author`, `same_series`, `companion_volume` or
> `derivative_of`, and neither carries `independence_not_established`. A shared publisher or a
> citation does not by itself defeat independence.

That is the whole authoritative surface. It is one rule because it is the only place where the audit
changes what the system is *permitted to do*, rather than what it records.

### One change to the extraction procedure (not a spec file)

Add a step between the fresh checkpoint and any cross-source or product work:

> After a book's source knowledge, systems and ontology are stable and its fresh checkpoint is
> committed, write its Audit Gate record and validate it. Cross-source promotion and downstream
> product use may not consume an unaudited source.

### Nothing else

- **SPEC-03: no change.** No new evidence characteristic, no new field. The origin question is
  answered in the audit layer and cross-checked against `empirical_within_source`.
- **SPEC-04: no change.** `human_workflow` and `deterministic_composition` are audit vocabulary
  only. No new target type, no new binding, no new executor value.
- **SPEC-01 / Creative IR: no change.** Never in scope.
- **No new ontology relation or term kind.**
- **No GitHub Actions workflow.** The validator and its 32 tests are committed and run on demand.

---

## 7. Rejected changes, and why

| Proposed in CANON-003 | Verdict | Reason |
|---|---|---|
| New SPEC-03 evidence characteristics for claimed-measurement and third-party research (C-01, C-13, C-23) | **Reject** | Real problem, wrong layer. Adding characteristics means migrating 16 frozen corpora and re-deciding 505 objects. The audit answers it additively with zero migration, and the validator keeps the layers honest. |
| A numeric visual-risk or completeness score | **Reject** | Three independent findings say count-based proxies fail. D-12: *Creativity, Inc.* 33 images, none argues; *StoryBrand* 36, four argue and two are load-bearing. LA-04: 11 uncaptioned figures, and the uncaptioned ones include the section's most load-bearing demonstration. B-15/B-18: severity tracks detectability, not amount. |
| New SPEC-04 target types for human workflow and deterministic composition | **Reject for now** | A target type means bindings, and no executor exists for either. Parking the fit in the audit is honest; inventing a binding is not. Revisit if a deterministic composition executor is actually built. |
| New ontology relation types (C-15, B-11) | **Reject** | CANON-003 diagnosed this as two governing documents disagreeing about a worker's authority — a governance clarification, not a schema defect. |
| Three-valued `source_warns_against_isolated_use` (C-14) | **Reject** | One book. Recorded in `system_level_uncertainty` and in a governance binding. |
| Weighted `priority_order` for Murch's Rule of Six (LB-10) | **Reject** | One book. Recorded as an audit observation on the Murch record. |
| A scale axis for `observation_unit` (LA-12) | **Reject** | One book, one claim, possibly specific to print-reproduced photography. Recorded in the Freeman record and in the binding's own limits. |
| Restoring mandatory Creative IR bindings | **Reject** | 44 objects across two books with zero Creative IR bindings, correctly. The old rule would have produced 44 distortions. |
| An auto-running CI workflow | **Reject** | Explicitly out of scope, and it produced noisy failures last time. |

---

## 8. Migration consequence for the existing 16-book corpus

**If ADOPTED: none.** That is the point of testing against the whole corpus rather than a sample —
the backfill is already done. All 16 records exist and validate.

- **Zero edits** to any `source-knowledge.yaml`, `source-concept-systems.yaml` or
  `operational-bindings.yaml`. No accepted claim was reinterpreted or rewritten.
- **One repair** to an `ontology-mappings.yaml`, described in §5, completing an integration that was
  already intended.
- **`visual-evidence-ledger.yaml` stays as it is.** It has no schema in any spec and 16 lanes gave
  it 16 different key sets; the audit record's `representation_integrity` is the machine-readable
  successor to the part that needs to be machine-readable. Retiring or specifying the ledger is a
  separate decision and is not proposed here.
- **Three records carry an unresolved element** — Alton and Hopkins each have objects classed
  `uncertain` for technology contingency, and Ogilvy's `measurement_claimed_result_not_supplied`
  category is present with no `sk_refs` because assigning it would need the chapter re-read. Three
  of sixteen, none escalating to `evidence_insufficient`, which is well inside the task's stop
  condition of "more than a small minority requiring the original books re-opened".

---

## 9. Unresolved questions

1. **Drift between the two files.** The audit is a second record that can fall out of step with the
   frozen one. The validator enforces consistency for `empirical_within_source` only. Nothing yet
   detects an audit written against an older version of a source record — `audited_against_commit`
   is recorded but not checked.
2. **The anti-score rule is partial.** It blocks a field named like a score. It cannot block a
   reader counting categories. §3 states the residual risk; the consumption-layer rule that would
   close it is out of scope here.
3. **Evidence lineage versus source lineage.** *Made to Stick*'s evidence is largely third-party. If
   a later cross-source concept rested on the Newton study reported there *and* on the same study
   reported elsewhere, that would be one evidential event counted twice, even though the two sources
   are independent. The candidate keeps source lineage and evidence origin as separate questions and
   deliberately does not merge them. Whether they need joining is a real open question and one book
   is not enough to answer it.
4. **`deterministic_composition` fired once in sixteen.** Kept because the single hit is exactly the
   LA-08 finding, but it is the weakest component and the obvious first cut.
5. **Who runs the gate.** These 16 records were written by one worker reading committed evidence. It
   is untested whether a different worker, or the book's own extractor, produces the same record. The
   isolation question CANON-003 raised for extraction applies here too and has not been examined.
6. **The gate has not been exercised on a promotion.** The rule is tested against the corpus and no
   `cross_source_concept` has ever been created. The failure it prevents is predicted, and the
   prediction is now mechanically checkable, which is a step short of observed.
