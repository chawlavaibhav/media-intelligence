# CANON-007 — Controller brief

**Task:** CANON-007, Wave 1 pilot — *Effectiveness in Context*
**Date:** 25 Aug 2026 · **Branch:** `work/canon-007-effectiveness-context` · **Task-base:** `main` at `161a14a`
**Status:** ingestion complete, source accepted · **needs_controller_review**
**Severity:** `LOCAL`. No stop condition fired. No spec changed.

---

## Bottom line

**Accepted. Live Canon moves from 18 to 19.**

The first genuinely new source since the method was frozen went through the full sequence —
extraction → systems/ontology → bindings → fresh checkpoint → Audit Gate → validators — and passed
without needing any method change. Historical CANON-003/004 remain fixed at 16.

The pilot's real result is that **the gate caught things a text-only ingestion would have shipped
wrong.** Two representation findings and one evidence-origin correction are described below; each
was found by looking rather than by parsing, and one was forced by the validator.

---

## 1. Source identity — fingerprint matched exactly

Downloaded from the official route named in the task. The Thinkbox landing page links directly to
the PDF on Thinkbox's own Contentful asset host. **No mirror or substitute was sought.**

| Check | Expected (Work) | Actual | |
|---|---|---|---|
| File size | 24,726,437 bytes | 24,726,437 bytes | ✅ |
| SHA-256 | `e589a422…0ae91e` | `e589a4222f5ce06db52384c5cc002dbd4e96f4156530be60d19bdf73e70ae91e` | ✅ |
| Pages | 139 | 139 | ✅ |
| PDF version / encryption | 1.6, unencrypted | 1.6, unencrypted | ✅ |

Both matched on the first download, so no version-identity question arose and the
stop-and-return-before-extraction condition never fired. Native Adobe InDesign 14.0, no OCR layer.

**One dating detail, recorded rather than smoothed:** the report is an EffWeek **2018** publication
and the PDF file was produced in **October 2019**. Nothing in the document identifies a revision, so
this reads as a later production of the same report — but the file date is not the publication date
and the two are kept separate.

**Nothing copyrighted was committed.** The PDF, six ephemeral page renders and all extracted text
lived only in a workspace outside the repository.

## 2. Slug, scope and counts

**Slug:** `binet-field-effectiveness-in-context-ch1`
**Source id:** `binet_field_effectiveness_in_context_ch1_consideration`

**Scope:** Section 1, Chapter 1.0 "How people choose brands" (printed pp.9–25) complete, plus the
Introduction (pp.6–8), *In a nutshell* (p.5) and the **Appendix: Metrics and methodology**
(pp.132–134).

Chapter 1.0 is the report's own stated foundation — *"in many ways this is the most important
chapter"* — and it establishes the consideration framework the report says it returns to throughout.
**The Appendix was included because the evidence-origin audit is not possible without it:** every
percentage in the chapter is a proportion of case-author self-gradings from a declaredly biased
sample, and extracting the claims without the apparatus that produced them would have made them look
like measurements they are not.

Unprocessed material — chapters 2.0–6.0, Sections 2 and 3, the two case vignettes — is named in
`PROVENANCE.md` rather than implied.

| Layer | Count |
|---|---|
| SourceKnowledge | **28** |
| SourceConceptSystems | **3** |
| Ontology terms | **20** |
| Ontology relationships | **7** |
| Concepts | **3** (2 source-specific, 1 canonical, 0 cross-source) |
| OperationalBindings | **4** |

Mechanical validation against current SPEC-03/04/05: **0 errors**.

## 3. The systems and claims that matter

**Three systems.** The report's own consideration framework (a decision framework on two dimensions,
level and nature, which jointly set which marketing task is hard); the brand-and-activation causal
model; and — marked `extractor_synthesis` — the **evidence apparatus**, which assembles the four
methodology facts the source states separately and never states together.

That third system is the one worth your attention. Its `interpretation_basis` says exactly why it
exists: the source states each fact plainly and never assembles them, so the assembly is mine, and
it is recorded as a system rather than folded into individual claims so that no single object is
made to carry an argument the source did not make.

**The consequential claims**, in summary rather than source prose: consideration level and type
govern which of brand building and activation is the harder job; penetration effects exceed loyalty
effects in every cell examined; the optimum budget split moves toward brand as consideration rises
and as decisions become more rational; and in high-online-research categories the derived optimum is
74:26 brand-to-activation while actual practice runs roughly the reverse.

## 4. Where the extraction refused to follow the source

The report states findings in stronger language than its charts carry. Three were recorded at the
strength of the evidence with the source's framing marked as framing:

- **Figure 13 is titled "Brand building boosts short-term effects."** The chart shows that campaigns
  reporting more very-large brand effects also report very-large activation effects more often —
  17%, 36%, 42%. That is co-occurrence between two self-gradings *of the same campaign by the same
  person*. The association is recorded; the causal direction is not.
- **"Loyalty-first approaches are doomed to fail"** is a recommendation. What the data shows is six
  cells in which penetration exceeds loyalty.
- **"Only emotional campaigns can create competitive advantage in this environment"** sits beside two
  bars differing by **0.06** (0.67 against 0.73). The prose's own word is "slightly", which is
  proportionate; the assertion is not.

Where the data undercuts the source's own hedge, that is recorded too: the loyalty series behind the
"loyalty matters more when consideration is low" qualification is **not monotonic** — 15, 12, 17 and
10, 15, 16 — so the qualification is weaker than a trend, and the extraction says so.

The source's own refusal to be read as universal rules is preserved as a first-class object and
carries a governance binding.

## 5. Representation integrity — two findings, both found by looking

`native_digital_pdf` · `authored_pages` · `inspected_page_level` · `figure_carries_content`.

**The chart values survive and their bindings do not.** This inverts the usual case. Chart text is
*not* missing: axis labels, series names, category names and every printed value extract cleanly.
What linearised text destroys is which number belongs to which category in which series. A text-only
pass on Figure 03 receives eleven numbers and six category names with nothing connecting them, would
bind them by guess, and nothing would signal uncertainty. On printed page 15 a chart axis value,
`1.5`, appears mid-sentence inside the extracted prose.

**Consequence: all 34 numeric values in this extraction were read from renders. None from the text
layer.** Seven claim-bearing figures were rendered and read; seven more that support only
directional claims were not, and that limit is stated in the ledger rather than glossed.

**The forewords contain phantom text.** The text layer of printed pages 1–3 carries sentences
printed *nowhere on those pages* — they belong to *In a nutshell* on page 5 — interleaved line by
line with the real foreword text. Rendering page 3 and reading it confirms the visible page carries
only Janet Hull's foreword and a photograph. A text-only pass would have a named third party
appearing to say things the report says elsewhere.

**A vocabulary mismatch, recorded and not stretched.** Every loss pattern in the adopted vocabulary
describes information *lost* from a page. Here information is *added* to the text layer that the
page does not show. I recorded it under `text_layer_order_damage` as the closest available value
**and said in the record, the ledger and PROVENANCE that it is not exact.** No method change is
proposed, because the phantom text is confined to printed pages 1–3 — verified by scanning all 139
pages for the marker phrases — no page in the processed span is affected, and no object is drawn
from the forewords. **If a later task processes those pages, the gap becomes live and should be
raised then.**

## 6. Evidence origin — four parties in the chain

The task warned against calling everything the authors' own measurement because Binet and Field
wrote the report. That warning is well aimed.

- **The analysis is theirs.** They cut the IPA Databank, fit the curves, report results found
  nowhere else.
- **The measurements are not.** Case-study authors grade their own campaign's outcomes on a
  four-point scale; only top-box "very large" grades are counted. **Every percentage in the report
  is a proportion of other people's self-assessments**, not an independently measured effect size.
- **One classification is a fourth party's** — the TNS Consumer Barometer.

Recorded as `mixed_own_and_third_party` at source level, with `source_own_measurement_reported` for
analyses that exist only here, `source_author_assertion` for the recommendations, and
`measurement_claimed_result_not_supplied` for the one prevalence claim made with no prevalence
given.

**Two declared biases are extracted as first-class objects rather than left as caveats**, because
they qualify everything: the sample is drawn from awards entries and is biased toward successful
campaigns, and **activation spend is under-reported in the direction that flatters the report's own
headline budget conclusion.** The source states both openly; neither is quantified. A third object
records that every published optimum is read off a fitted curve **after excluding** rational
product-benefit brand campaigns.

**The validator forced a correction here, and it was right to.** I had initially listed the
405-case online-research object under `third_party_measurement_reported` because the TNS Barometer
is third-party. The consistency check refused it: the object carries `empirical_within_source` in
the frozen record. The distinction it forced is real — *a third-party measurement used as a
covariate is not a third-party measurement reported as evidence*. The source never reports a
Barometer result; it reports its own overlay. The category now carries no `sk_refs` and explains
why, and the outside dependency is recorded where it actually bites: in technology contingency.

## 7. Application fit — a governance source

| Consumer | Outcome |
|---|---|
| governance | **binding_exists** (2) — `rule_application` and `evidence_interpretation` |
| evaluation | **binding_exists** (1) — `observation_unit: asset_set_over_time` |
| benchmark | **binding_exists** (1) — `evidence_basis: extractor_inference` |
| creative_ir | no_current_binding |
| production_ir | no_current_binding |
| deterministic_composition | no_current_binding |
| human_workflow | **candidate_no_binding_made** |

**Zero Creative IR bindings from 28 objects, and that is correct.** Nothing here describes the
contents of a generated asset; the rational/emotional distinction is about how a category is bought.
Turning it into a message-field value would be precisely the forced binding SPEC-04 exists to
prevent.

The evaluation binding's observation unit is set by the source's own measurement window, not by
judgement: business effects are measured over at least a year and ESOV Efficiency is annualised, so
**no single asset can be scored against any metric in this report.**

`human_workflow` is the largest unbound block and the most operational — how a team divides a budget,
and how to read the report at all. It acts on how an organisation decides, not on material.

This is the corpus's first source whose centre of gravity is **governance**. Reading that as a weak
source would be the D-13 error in reverse.

## 8. Lineage — `independent_origin`

No shared author, series, publisher or derivation with any live source. The IPA appears nowhere
else, so not even `shares_publisher_only` applies. Three domain-adjacent sources were checked
individually and recorded as `no_known_relation`: Hopkins, Ogilvy and Heath.

**The `shared_primary_informant` test was applied and does not fire.** It requires the same
practitioner's own claims to be a primary knowledge source in both works. Binet and Field appear in
no other corpus source, and the processed span quotes no practitioner whose own book the corpus
holds. Ehrenberg, Sharp and Kahneman are named in passing — incidental quotation, which the adopted
definition explicitly excludes.

**One dependence exists and is flagged for the future.** This report is Part 2 of a series and
repeatedly builds on the authors' own earlier reports, *The Long and the Short of It* and *Media in
Focus*. Some claims are carried forward rather than newly established here. **If either earlier
report is ever ingested, that pair is `shared_author` and `same_series` and must be declared at
ingestion, not discovered later.**

## 9. Technology contingency — `applicable: true`

A 2018 report whose data window closes in 2016, read in 2026, about an environment that changes fast.

- **durable_mechanism** — claims about attention and memory: rational thought makes brand
  perceptions harder to shift, emotional engagement is the route to a price premium, memory
  structures and immediate triggers are complementary. Claims about people, not about a media market.
- **technology_contingent** — the entire online-research block, which rests on a pre-2016
  classification and on the search and aggregator economics of that period; and the optimum splits,
  which the source itself frames as evolving and which are measured through a spend-reporting
  structure that has continued to change.
- **historical_convention** — claims describing the state of the evidence base rather than a
  mechanism, which would need re-establishing against a later Databank.
- **uncertain** — the core consideration findings. The mechanism is plausibly durable; every
  magnitude was measured on 1998–2016 UK awards entries, and the report gives no basis for deciding
  whether the magnitudes travel or only the directions. Recorded as uncertain rather than assigned,
  because deciding would need evidence this source does not contain and the task forbids acquiring
  another.

## 10. Verification — fresh from the final branch head

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `python canon/validation/validate_canon003_integrated.py --root .` | **0** | `error_count = 0` · **16 books**, 505 objects, 54 systems, 417 terms, 53 concepts, 111 bindings — *identical to `main`* |
| 2 | `python canon/validation/validate_audit_gate_v02.py --root .` | **0** | `error_count = 0` · **`record_count = 19`** over 19 source directories |
| 3 | `python -m pytest tests/ -q` | **0** | **63 passed, 89 subtests passed** |

| Confirmation | Result |
|---|---|
| new source's five snapshot artifacts match its audit snapshot | ✅ recomputed clean; all 19 snapshots valid |
| no id collision across the enlarged live corpus | ✅ 0 across 580 / 63 / 470 / 62 / 127 |
| SPEC-01, SPEC-03, SPEC-04 unchanged from task base | ✅ `git diff --stat` empty |
| SPEC-05 unchanged | ✅ no stop condition fired |
| no historical CANON-003/004 decision or synthesis rewritten | ✅ none touched |
| no source PDF, page render or image committed | ✅ every changed path is `.md` or `.yaml` |
| no `.github` workflow | ✅ no `.github` directory |
| no model/API spend | ✅ none |

## 11. Counts after this task

| Number | Value |
|---|---|
| CANON-003 accepted / CANON-004 method-test corpus | **16 — fixed forever** |
| Source directories | **19** |
| **Live accepted Canon** | **19** |
| Active v0.2 audit records | **19** |

## 12. Unresolved and worth your attention

1. **The loss-pattern vocabulary has no value for added text**, only for lost text. Recorded, not
   stretched; no change proposed because no extracted claim is affected. Live if the forewords are
   ever processed.
2. **Seven figures supporting directional claims were not rendered.** `sk_eic_0013` carries
   `extraction_uncertainty: figure_not_inspected` for exactly this. A bounded, stated limit of the
   pilot, not a completeness claim.
3. **The series dependency** on *The Long and the Short of It* and *Media in Focus* — flagged above,
   must be declared if either is ingested.
4. **Scope is one chapter of a 139-page report.** The remaining chapters are not in the Canon and
   nothing here should be read as covering them.

No stop condition fired. Not started or self-assigned: any other Wave-1 source, RAG/retrieval,
cross-source concepts, Production IR, model or API work.
