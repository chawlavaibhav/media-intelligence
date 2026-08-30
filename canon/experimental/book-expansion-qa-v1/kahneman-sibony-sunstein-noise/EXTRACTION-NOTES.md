# Extraction notes — Kahneman, Sibony & Sunstein, *Noise: A Flaw in Human Judgment*

**EXPERIMENTAL — NOT LIVE CANON.** A lane of the non-merge `book-expansion-qa-v1` expansion.
Nothing here is accepted Canon and nothing here may be described as accepted.

---

## 1. Method

The book was read in full through the extracted EPUB text, chapter by chapter, in the order of the
argument rather than the order of the spine — the taxonomy chapters first (Introduction, 2, 4, 5, 6,
7), then the mechanism chapters (8, 13, 14, 15, 16, 17), then the prediction chapters (9, 10, 11, 12),
then the remedy chapters (18–25) and the objections (26–28), and finally the Conclusion and the three
appendices.

Objects were written against the chapter text, not against the book's own end-of-chapter "Speaking
of…" summary boxes. Those boxes were used only to confirm that a claim had been read the way the
authors intended, and their phrasing appears in `source_stated_remedies` in a handful of places where
it is the crispest statement of the source's own instruction.

Twelve objects (`sk_nse_0001`–`sk_nse_0012`) survived from an earlier attempt that died mid-write.
They were re-read against the source before being kept. They were kept unchanged, and numbering
continued from `sk_nse_0013`. Their forward references to objects that did not yet exist —
`sk_nse_0013`, `sk_nse_0017`, `sk_nse_0035`, `sk_nse_0036`, `sk_nse_0044`, `scs_nse_001` — were
treated as constraints on the numbering plan and all now resolve.

Writing was incremental: source-knowledge in four appends of 10–12 objects, the Q&A bank in three
appends of 15–19 items, each append parse-checked before the next.

---

## 2. Self-check results

### 2.1 Every YAML parses

All five YAML files parse under `yaml.safe_load`. Two parse failures were introduced during writing
and fixed: a list item in `source_stated_remedies` with unquoted trailing prose after a quoted string
(`sk_nse_0035`), and the same pattern in `source_stated_problems` (`sk_nse_0040`, `sk_nse_0043`).
All three were malformed YAML, not malformed content, and were repaired by making each item a single
quoted scalar.

### 2.2 Locators — mechanical assertion

**Asserted mechanically across all five YAML files** that no `source_locator`, `provenance.chapter` or
`provenance.section` line matches `\b(p\.|pp\.|page[s]?\s+\d|printed p|PDF page)\b` (case-insensitive).

- **Hits: 0.**
- `page_start` and `page_end` are `null` in **50 of 50** SourceKnowledge objects and **3 of 3**
  SourceConceptSystem objects.
- All **57** Q&A `source_locator` values are non-empty.
- **Failures found: 0. Failures fixed: 0.**

Spot-checked by hand against the source text, well above the required 20: `sk_nse_0013`, `0014`,
`0015`, `0017`, `0022`, `0026`, `0031`, `0032`, `0033`, `0036`, `0037`, `0039`, `0040`, `0042`,
`0043`, `0044`, `0045`, `0048`, `0049`, `0050`, and Q&A items `qa_nse_0003`, `0012`, `0015`, `0029`,
`0034`, `0042`, `0047`, `0050`. Each names a chapter and a section that exists under that title in
the extracted text.

Audit pattern recorded: **`no_authored_page`**. This is not a defect in the extraction. The format
has no page and it is unfixable in this copy.

`false_page_affordance` was checked for and does **not** apply: the extraction header states plainly
that there are no authored page numbers, and the file does not look like it has them. The one place
page numbers do appear in this book is its **Notes**, where they are citations into *other people's*
works. None was used as a locator and the Notes were not extracted.

### 2.3 `empirical_within_source` count and justification

**Count: 9 of 50 objects.** Each is a study the authors themselves conducted.

| Object | Study | Whose |
|---|---|---|
| `sk_nse_0003` | The insurance company noise audit — median difference 55% underwriting, 43% claims | Authors' own consulting engagement |
| `sk_nse_0011` | The 20%-level / 80%-pattern split at that insurer; the 63/62/61% pattern share across three punitive-damages scales | Authors' own |
| `sk_nse_0013` | The insurance audit as the worked instance of the audit design | Authors' own |
| `sk_nse_0015` | The audit result plus the poll of 828 CEOs and senior executives (median expected difference 10%) | Authors' own |
| `sk_nse_0017` | The Gambardi case shown to 115 MBA students, estimates 10–95 | Authors' own demonstration |
| `sk_nse_0022` | Statistical juries (899 participants) versus deliberating juries (3,000+ citizens, 500+ six-person juries) | Authors' own experiments |
| `sk_nse_0026` | The outrage hypothesis: 0.98 correlation across 28 scenarios; the severe/mild harm manipulation | Authors' own (Kahneman, Schkade & Sunstein) |
| `sk_nse_0031` | The three-scale noise comparison, 51% / 71% / 94% | Authors' own |
| `sk_nse_0032` | The rank transformation, 94% → 49% | Authors' own |

Everything else the book reports is somebody else's work, and is caveated as such with
`origin: extractor_observed` naming whose it was. The roster of third-party work that carries weight
in this extraction:

- **Sentencing** — the 1981 study of 208 federal judges, conducted as part of the sentencing-reform
  movement.
- **Bail** — Mullainathan and colleagues; the 173-judge, 141,833-case decomposition was a special
  analysis carried out **at the authors' request by the original researchers**. It is theirs, not the
  authors', and `sk_nse_0008` and `sk_nse_0011` say so explicitly. This is the single most tempting
  case to misfile and it was deliberately not filed as `empirical_within_source`.
- **Consistency without consensus** — Todorov and colleagues at Princeton, using paid online
  participants; the source itself notes their judgement quality is often lower than in professional
  settings.
- **Occasion noise** — Vul & Pashler (the crowd within), Herzog & Hertwig (dialectical bootstrapping),
  Forgas (mood), Kahana and colleagues (memory), the asylum-sequencing and opioid-prescribing
  analyses, the wine-competition re-tasting. **The authors report no occasion-noise measurement of
  their own.**
- **Groups** — Salganik and colleagues (music downloads and the inverted-ranking follow-up), Macy and
  colleagues (political positions), Muchnik and colleagues (the single artificial up-vote).
- **Models versus judges** — Meehl's 1954 review, the 2000 review of 136 studies, Goldberg's
  model-of-the-judge work, Dawes & Corrigan on equal weights, Yu & Kuncel's random-model study.
- **Forensics** — Dror and colleagues throughout, plus the FBI's own 2011 accuracy study and 2012
  re-test, and the 2016 PCAST report.
- **Forecasting** — Tetlock's expert political judgement work, the Good Judgment Project, and the BIN
  analysis by Satopää, Tetlock, Mellers & Salikhov.
- **Prediction ceilings** — the Fragile Families common-task challenge (McLanahan, Salganik and 160
  competing teams); the personnel-selection reviews; Mullainathan & Obermeyer on heart attacks.
- **Medicine and psychiatry** — Apgar, Centor, BI-RADS, and the psychiatric reliability literature
  from 1964 through the DSM-5 field trials.
- **Selection** — the GMA literature, the cognitive reflection test, the need-for-cognition scale,
  Baron's actively-open-minded-thinking scale, Haran/Ritov/Mellers.
- **Performance ratings** — the 360-degree variance decompositions, forced-ranking practice, and
  frame-of-reference training research, which the source itself notes has mostly been studied on
  students rather than working managers.

**Replication status is not verified by this extraction and is outside its scope.** Nothing above
asserts that any of it has since held up, and nothing asserts that it has not. This note exists to
mark *whose measurement it was*, which is a different question.

### 2.4 Nothing claims anything about model or AI evaluator behaviour

Checked object by object. **Confirmed: no SourceKnowledge object claims or implies anything about how
a model, an AI system or an automated evaluator behaves.**

Three objects discuss algorithms, and each reports only what the book says about *statistical models
and rule-based procedures as the book studied them*:

- `sk_nse_0033` — mechanical aggregation outperforming clinical judgement. This is about linear
  regression models, models of a judge, and randomly weighted linear models predicting human outcomes
  from scored predictors. It is not about generative or model-based evaluators, and the object's
  caveats record the source's own refusal to draw a replacement conclusion.
- `sk_nse_0034` — the broken-leg principle. A rule for when a *person* may override a mechanical
  output.
- `sk_nse_0045` — noiseless but biased algorithms. The book's own objection material, reporting
  third-party results and the book's careful "can, not will".

Nothing anywhere in this lane infers current model capability from this book. See §4 for the open
question that this constraint generated.

### 2.5 Application fraction — computed in code

Computed over `qa-bank.yaml`:

```
items = 57
requires_application: true = 22
fraction = 0.386
```

**0.386 ≥ 1/3.** Requirement met with margin. An earlier count of 17/52 = 0.327 was **below**
threshold and five further application items were written (`qa_nse_0053`–`0057`) rather than
reclassifying any existing item.

### 2.6 Other mechanical checks

| Check | Result |
|---|---|
| SourceKnowledge objects | 50 (target 30–50) |
| All 18 required SPEC-03 keys present on every object | pass |
| `evidence.characteristics` within fixed vocabulary | pass |
| `intra_source_relations[].relation` within fixed vocabulary | pass |
| All `sk_` relation targets resolve inside the lane | pass, 0 dangling |
| All `scs_` relation targets resolve | pass (`scs_nse_001/002/003` all exist) |
| Q&A items | 57 (target 40–60) |
| Q&A key set exactly the 12 contract keys, no extras, no omissions | pass |
| `answer_type`, `difficulty`, `knowledge_type` within fixed vocabularies | pass |
| `confounders` non-empty on every item | pass |
| No empty or placeholder answers, no `TODO` | pass |
| Bindings: `governance` → permitted `governance_consumer` | pass |
| Bindings: `evaluation` → `observation_unit` present and valid | pass |
| Bindings: no `creative_ir`, no `production` | pass |
| Bindings: `evidence_basis` never `cross_source_supported` or `empirically_supported` | pass |
| Bindings: all ontology refs resolve to this lane's SPEC-05 identifiers | pass |
| Ontology: every `kind: remedy` term carries `executable_by` | pass |
| Ontology: `executable_by` only ever `human_edit` or `unknown` | pass |
| Ontology: no `xs_` concept created | pass |
| Ontology: `same_failure_family` not used | pass |

Q&A mix against the contract's approximate target: definitions/facts 6 (11%), mechanisms 11 (19%),
comparisons/trade-offs 8 (14%), diagnosis/application/repair 21 (37%), boundaries/exceptions +
source-position 11 (19%). The bank is heavier on application and lighter on definitions than the
target mix. That is deliberate and it follows the source: this book's transferable content is
procedural, and the definitional surface is small — the noise taxonomy is eight terms, and once they
are defined the remaining value is in applying them.

---

## 3. What was deliberately not extracted, and why

- **Ch. 1 in full, and the sentencing-reform history.** Case material. The general mechanisms it
  introduces are carried by Ch. 2, 6 and 17 objects.
- **The extended insurance, medical, forensic and forecasting narratives.** Extracted only where a
  case reveals a general mechanism: the audit design (Ch. 2, Appendix A), the
  verification-independence failure (Ch. 20), the guideline mechanism and its psychiatric limit
  (Ch. 22), the aggregation arithmetic (Ch. 21), the scale results (Ch. 15, 23).
- **The statistical appendices' derivations** and the correlation/percent-concordant conversion
  table. `sk_nse_0029` records Appendix C's correction procedure as a procedure, without reproducing
  the arithmetic apparatus.
- **Organisational politics** — resistance to mechanical prediction, the performance-management
  fashion cycle, professional bodies' reactions. Recorded only where the source's own concession
  about a remedy's adoption cost bears on whether the remedy is usable, in which case it appears as a
  caveat on the remedy's object (e.g. `sk_nse_0040` on frame-of-reference training, `sk_nse_0039` on
  people disliking structured interviews).
- **The Notes, Acknowledgments and back matter.**

No attempt was made to pad the count by drifting into parts of the book with nothing to do with
judging outputs. Where the material ran out, the extraction stopped.

---

## 4. Open question — recorded here and nowhere else

**Does anything in an automated evaluator correspond to occasion noise, level noise or pattern
noise?**

This thought formed repeatedly while reading Ch. 6, 7 and 16, and it is recorded here as an
explicitly-labelled open question because it does not belong in a SourceKnowledge object or in a
binding's `rationale`. The book says **nothing** about machine evaluators. Whether a model-based
evaluator scoring the same asset twice, or scoring the same asset under different sampling
parameters, exhibits anything *analogous* to occasion noise is **unknown and outside this source**.
The vocabulary is tempting precisely because it fits so neatly — which is the reason to be careful
with it, not the reason to use it.

Specifically, four things were **not** asserted anywhere in this lane:

1. That an automated evaluator has a "level" — a general severity — comparable to a human judge's.
2. That an automated evaluator has "pattern noise" — an idiosyncratic sensitivity to particular
   assets that another evaluator would not share.
3. That re-scoring the same asset measures anything analogous to occasion noise, or that a stable
   re-score means anything analogous to reliability in this book's sense.
4. That the book's finding on the relative *sizes* of the three components transfers in any way.

The related methodological question — whether a noise audit's design transfers to auditing an
automated evaluator — is likewise unanswered here. `bnd_nse_001` binds the audit design to auditing
**our human adjudicators**, and says explicitly that transfer to people judging generated media is
untested. It makes no claim about auditing a model.

Two smaller open questions, also recorded rather than answered:

- **Does a model-produced score bias a human reviewer the way a colleague's verdict does?**
  `bnd_nse_004` assumes it might and marks the assumption `extractor_inference`. The book's evidence
  is human examiners exposed to human-supplied context. The extension is plausible and untested.
- **Are this project's acceptance judgements predictive or evaluative?** `sk_nse_0018` makes the
  distinction load-bearing — the book's whole quantitative apparatus applies only to the first — and
  `bnd_nse_012` proposes declaring it per rubric dimension. This extraction cannot answer it, and the
  answer changes which parts of this book apply.

---

## 5. Figures — `figure_semantic_binding_lost` assessment

The book contains numbered figures; the extracted spans reference Figures 3 through 19. **None was
inspected.** The extracted text carries captions and surrounding prose.

**Assessment: `figure_semantic_binding_lost` does NOT apply to this source in the strong sense.**
In every case where a figure carries quantitative content, the prose states the numbers explicitly —
the three noise equations, the 51/71/94 percentages, the 94%→49% rank transformation, the
20%/80% insurance split, the 26%/7% bail-judge split. The figures render the argument; they do not
carry meaning the text withholds.

Where a figure is nonetheless doing visual work the extraction cannot see — the two-panel comparison
of halving bias against halving noise (`sk_nse_0006`), the Pythagorean rendering of the
decompositions (`sk_nse_0005`, `sk_nse_0010`), the variance breakdowns (`sk_nse_0031`, `sk_nse_0032`),
and the side-by-side of a behaviourally anchored scale against a case scale (`sk_nse_0040`) — the
object carries `extraction_uncertainty: figure_not_inspected` and a caveat naming the figure. Seven
objects carry that marking. Everything else carries `none`.

---

## 6. Judgement calls a reviewer should check

These are the places where a different extractor could reasonably have gone another way.

1. **Nine `empirical_within_source` markings, not more and not fewer.** The hardest exclusion was the
   bail-judge decomposition, which was run at the authors' request but by the original researchers on
   their own data with their own models. It was excluded. The hardest inclusion was `sk_nse_0017`,
   which rests on the Gambardi demonstration — the authors' own, but a classroom demonstration
   designed to produce the effect it illustrates rather than a controlled study. It is marked
   `empirical_within_source` **and** carries a caveat saying exactly that.

2. **Three concept systems, not one and not six.** The noise taxonomy is unambiguously a system: the
   source states it as three nested equations and the nesting does real work. The decision hygiene
   principles are enumerated by the source as a set, and its own objections chapter turns on the set
   being the unit of reasoning — but the *dependency and trade-off structure* recorded in
   `scs_nse_002` is partly ours, and `whole_system_claim.origin` is `extractor_synthesis` with a
   non-null `interpretation_basis` saying so. The seven objections are enumerated and answered as a
   set by the source; the compression of seven objections into four member objects is an extraction
   decision and is stated in `system_level_uncertainty`, as is our inference that the
   rules-versus-standards framework resolves the set (marked `extractor_inferred` in the membership).
   No fourth system was manufactured.

3. **`knowledge_type` is overwhelmingly `evaluation_diagnosis` (48 of 57).** The controlled
   vocabulary has no value for "how human judgement behaves". `evaluation_diagnosis` is the honest
   nearest fit; `testing_method` was used for the six audit-design and measurement items, and
   `effectiveness` for the three items about whether noise reduction pays. Forcing variety by
   assigning `creative_process` or `production_reasoning` would have been a misfiling, so it was not
   done. A consolidator may want to note that this source strains the vocabulary.

4. **Fourteen bindings, and a list of what was left unbound.** The unbound list is written into the
   header of `operational-bindings.yaml` so the omissions are visible: the error equation and its MSE
   arithmetic (our acceptance judgements are largely evaluative and the source rules the equation out
   for those); objective ignorance (binding it would require a claim about the ceiling on this
   project's prediction tasks that we cannot support); rules-versus-standards and the dignity
   objection (institutional and legal, with no permitted consumer here); and all the case material.
   Zero bindings would have been a legitimate outcome; so is fourteen. None was manufactured to look
   complete.

5. **`observation_unit` is `asset_set_over_time` on all four evaluation bindings, never
   `whole_asset`.** Noise is a property of a set of judgements. A single asset judged once cannot
   carry it, and each of those bindings says so in `applicability.limits` rather than relying on the
   enum value to make the point.

6. **The `governance_consumer` restriction.** Only `evidence_interpretation`, `conflict_resolution`
   and `rule_application` were used. Candidates that fitted none of the six permitted consumers —
   principally the material on institutional design and on who should be trusted with discretion —
   were left unbound rather than forced into `taxonomy_governance` or `retrieval_governance`.

7. **The book's hedges were preserved, not smoothed.** Where the source marks a conclusion tentative
   it is marked tentative here: `sk_nse_0011` carries `source_uncertainty: source_hedges` and quotes
   the authors' own warning against overgeneralising from a limited selection of examples;
   `sk_nse_0043` carries `source_concedes_difficulty` for the psychiatric case; `sk_nse_0021` carries
   it for singular decisions. The tempting move — presenting "stable pattern noise is the largest
   component" as a finding — was not made, and every downstream object and binding that depends on it
   inherits the hedge.
