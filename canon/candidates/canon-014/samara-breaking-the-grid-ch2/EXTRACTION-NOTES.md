# Extraction notes — Samara, *Making and Breaking the Grid*, Ch. 2 "Breaking the Grid"

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon and nothing here may
be described as accepted. Non-merge, exploratory work under
`canon/experimental/book-expansion-qa-v1/`.

`source_id: samara-breaking-the-grid-ch2` · prefix `sgb` ·
`scope_extension_of: samara-making-breaking-grid-ch1` · `independence: none — same work`

---

## 1. Method

The span is spine document 6, `ops/xhtml/ch02.xhtml`, read in full from the supplied text file
(`scratchpad/src/EPUB-Making_and_Breaking_the_Grid__A_.txt`, lines 1139–1827), plus one object
(`sk_sgb_0006`) taken from chapter 1's *Coming to Order* under the lane brief's allowance for
reasoning rather than chronology. Boundaries were confirmed directly in the file: spine 5 is
`TITLE 1 Making the Grid`, spine 6 is `TITLE 2 Breaking the Grid`, spine 7 is
`Directory of Contributors`.

Everything in the span was read: the untitled opening argument, *On the Other Hand* (the historical
survey), *Alternative Architectures* and all its sub-sections, *Considering the Practical in the
Impractical* and all its sub-sections, and the *Exhibits* commentaries.

Extraction proceeded section by section, taking a claim only where the text carried a mechanism, a
decision rule, a trade-off, a failure condition or a diagnostic cue. Where the source's exact
wording is the load-bearing part — "structurally antithetical", "chaotic randomness", "a necessary
level of practicality", "Limit the rules to two or three, total" — it is preserved verbatim in
`source_terms` and quoted short in `caveats`. The Q&A bank is paraphrase throughout.

**Written incrementally.** A previous attempt on this lane died mid-write on a single large write
call, leaving `source-knowledge.yaml` truncated at 17 objects. Those 17 were read, judged sound and
kept; numbering continued at `sk_sgb_0018`. The file was then extended in four appended chunks with
a YAML parse after each. The wrapped shape (`source_id:` + `source_knowledge:`) was added to match
the completed sibling lane `w3c-wcag22-text-legibility`.

---

## 2. The central hazard — `source_is_its_own_specimen`, and how much could not be verified

Audit pattern: **`no_authored_page`**. Caution name: **`figure_semantic_binding_lost`**.
Visual argument role: **`source_is_its_own_specimen`**.

This book argues through page layouts. Its claims are demonstrated by the arrangement of the page in
front of the reader, and the live chapter-1 audit already recorded it as
`inspected_no_page_available` with `no_authored_page` as an **unrecoverable** loss pattern in this
copy. That finding is honoured here rather than worked around.

**The proportion, stated plainly.** Counted mechanically:

| | Count |
|---|---|
| Distinct `<img>` references in the publisher's own `ops/xhtml/ch02.xhtml` | **205** (verified by opening the EPUB) |
| Figures inspected by this lane | **0** |
| Figures inspectable *as pages* in this copy | **0** — the page does not exist in a reflowable EPUB |
| Objects whose `source_support` is `text_and_visual` | **21 of 45 (47%)** |
| Objects carrying `extraction_uncertainty: figure_not_inspected` | **26 of 45 (58%)** |
| Objects carrying `visually_demonstrated` | **25 of 45 (56%)** |
| Positive examples recorded, every one with `figure_ref: null` | 59 |

So: **more than half of this extraction rests on claims the source demonstrates in images that were
not seen, and none of the 205 figures in the chapter was inspected.** The 24 text-only objects are
the ones where the reasoning is fully carried in prose — the opening argument, the practicality
obligation, the rule-count limit, the diagnostic questions, the chance-operation taxonomy — and they
are the sturdier half of the lane.

**What was NOT done.** No visual claim was inferred from a caption. Where a caption asserts a result
that only the image could establish, the object records the source's *stated reasoning* and stops.
Concretely:

- `sk_sgb_0020` records the vocabulary of bilateral, rotational and dual-axis symmetry because the
  words are the reusable part, and explicitly declines to infer anything further from the diagram
  that distinguishes them.
- `sk_sgb_0036` records that two annual-report spreads "manipulate imagery in different ways"; the
  ways are not named in the text and are **not guessed**.
- `sk_sgb_0034` records the rule for the entry point of type on a curve, and does not report what
  the paired before/after comparison shows.
- `sk_sgb_0044` and `sk_sgb_0045` are the two objects that would have been most valuable to verify
  and are the two least verifiable: both concern whether a layout *looks* controlled, and both are
  typed `source_interpretation` with an `interpretation_basis` saying so.
- The illustration for *Chance Operations — Random Physical Effect* is itself a chance operation
  performed on the page (a list of possibilities dropped onto the layout). That demonstration exists
  only as a designed surface; its absence is recorded in `sk_sgb_0028`'s caveats.
- The whole of *Pacing and Sequencing* concerns structure carried across a succession of spreads. A
  kinetic structure is unavailable to any single-surface inspection and doubly unavailable here.
  `sk_sgb_0043` records the principle and verifies no instance of it.

**No object carries `inferred_from_layout`,** and that is deliberate rather than an oversight: no
claim in this lane was arrived at by reasoning from a layout the extractor could not see. Where that
temptation arose it was refused (see §8).

**Unresolvable internal cross-references.** Chapter 2 contains a link reading `(see Coming to Order )`
whose target page cannot be resolved in this copy, and a caption reading `(see the detail images
immediately to the right)`, which is spatial deixis across a printed spread. Neither was guessed.

**A finding that must not be misread as permission.** The EPUB *file* does carry 110 publisher
`epub:type="pagebreak"` anchors in `ch02.xhtml` (verified). That is presumably how the live
chapter-1 extraction obtained printed page numbers. **The delivered text route for this lane strips
them**, and the locator addendum places this lane in Case 3. This lane therefore cites no pages
anywhere. The asymmetry with the live record is an artefact of the delivery route, not of the book,
and it is recorded here rather than resolved by inventing citations. It is also, incidentally, a
clean instance of `false_page_affordance` in reverse: the format looks pageless in one route and
paginated in another, and only one of those is authored.

---

## 3. Locators — Case 3

Per `SCHEMA-CONTRACT-ADDENDUM-LOCATORS.md` Case 3, every locator is **chapter + named section**,
with `(spine 6)` as a file-position aid. `page_start` and `page_end` are `null` on every object and
every system without exception. Locators name the sub-heading or the specific caption, not just the
chapter, because a chapter of ~20,800 words is far too coarse a locator to be useful.

---

## 4. What was deliberately NOT extracted

**Chapter 1's instructional core** — the grid taxonomy, the derivation method, the usage judgement of
*Using a Grid*. Already live; not re-extracted, and the diff in §6 confirms it.

**Chapter 1's *Coming to Order*** (historical survey). One object only (`sk_sgb_0006`, the
maximum-conformity / maximum-freedom framing, which is a design problem rather than a date).
Negative finding: the rest of that section is chronology — schools, names, decades — and carries no
reusable mechanism. Nothing else was taken from it.

**The whole of *On the Other Hand*, except its conclusions.** The historical survey in chapter 2 is
some 3,500 words of movements and biographies: Dada, the Cabaret Voltaire, Weingart at Basel, McCoy
at Cranbrook, Carson at *Beach Culture*. Three objects were taken from it — `sk_sgb_0003`
(structure is one system among many and context selects), `sk_sgb_0004` (deconstruction defined) and
`sk_sgb_0005` (a system defined by the consistent destruction of conformity) — because each is a
conclusion Samara draws rather than an event he reports. Everything else was refused as chronology.

**Gallery captions naming only a studio and a client.** The exhibits section carries 35 numbered
projects, each with a credit block. Credit blocks were refused outright. Exhibit *commentaries* were
mined only where they carry a mechanism; six objects came from them (`sk_sgb_0029`, `sk_sgb_0044`,
`sk_sgb_0045`, plus material folded into others), out of roughly 35 candidates.

**Contributor biographies** (spine 7, *Directory of Contributors*) — out of span and refused.

**Decorative description.** Much of the exhibit commentary is appreciation: "a kinetic experience
that is both filmic and reminiscent of tattered street posters". Where a passage names no mechanism
and yields no reusable rule, it was left.

**Anything about generative models.** Nothing in this book is evidence about what any model can do,
and no object or binding says or implies otherwise.

---

## 5. Interactions with the live chapter 1 — the same author qualifying himself

This is a **scope extension of a work already in live Canon, not an independent origin**. Same
author, same book, same edition, same file. **Nothing here corroborates the live extraction, and no
aggregation may count this lane as a second source agreeing with it.** `bnd_sgb_007` exists to flag
exactly that to any later conflict-resolution step.

Chapter 2 qualifies chapter 1 in five substantive places. Each is recorded as **one author
qualifying his own earlier statement across a chapter boundary within a single work** — never as
cross-source disagreement, and never presented as two sources disagreeing.

1. **Assess the content before building the structure.** The live object
   `the_grid_is_a_closed_system_so_content_must_be_assessed_first` makes this the first step of a
   reliable grid. Chapter 2's *Universal/Unique* exhibit (`sk_sgb_0029`) commends a book in which
   "the grid forces the deconstruction because its structure is created before assessing the
   material it governs". Both stand. The chapter-2 context is an exhibition brief that *required*
   predetermined kernel elements, which is why the object's scope says so and its caveats warn
   against generalising it.

2. **Whether a grid enables or impedes variation.** Chapter 1 treats the grid as a system whose rules
   exist to allow a range of expression. Chapter 2 (`sk_sgb_0038`) says grid-based thinking "tends to
   engender systems that are characteristically consistent and programmatic" and that "expressing
   variation is more difficult". Cooler, from the same pen.

3. **Fragmenting running text.** Chapter 1 holds a set of interacting readability measures sensitive
   to small shifts. Chapter 2 concedes that fragmenting text "would generally interfere with
   reading" (`sk_sgb_0016`), states in a caption that "the visual clarity is decreased"
   (`sk_sgb_0018`), and then suggests it "might even improve readability" under a redefinition of
   readability as engagement (`sk_sgb_0017`). The redefinition is what makes those compatible, and
   the objects say so rather than smoothing it over.

4. **Symmetry.** Chapter 1 reads symmetry connotatively — authoritative, classical. Chapter 2
   (`sk_sgb_0019`, `sk_sgb_0021`) treats it structurally: antithetical to grid logic, unforgiving,
   and liable to let the viewer rest too soon. Different questions about the same device, not a
   reversal.

5. **Violating a structure.** Chapter 1's `violation_works_by_scarcity_and_can_be_designed_into_the_structure`
   makes the violation effective through contrast with surrounding rigour. Chapter 2's `sk_sgb_0013`
   is the inverse case: a structure so thoroughly broken that only a vestige survives, and the
   vestige is what preserves navigation. The two are complementary, and neither was folded into the
   other.

Ontology note: these relationships are recorded **in prose here and not as SPEC-05 relationships**,
because expressing them in the ontology would make one work look like two vocabularies meeting.

---

## 6. Self-check results

**(1) Every YAML parses.** All five YAML files load under `yaml.safe_load`. Every enumerated value
was checked against the schema contract's fixed vocabularies in code:
`evidence.characteristics`, `source_uncertainty`, `extraction_uncertainty`,
`intra_source_relations[].relation`, `source_support`, `answer_type`, `difficulty`,
`knowledge_type`, SPEC-05 `relation`, `executable_by`, `governance_consumer`, `evidence_basis`.
Two `intra_source_relations` initially used `related_to`, which is a SPEC-05 relation and **not** a
SPEC-03 one; both were caught by the check and corrected (to `trades_off_with` and
`demonstrated_together_with`). No `same_failure_family`, no `xs_` concept, no decimal confidence
value, no `informs` field, no `creative.*` path.

Reference integrity: all 45 `sk_id` unique; **0** dangling `intra_source_relations` targets; all
`scs.members[].sk_ref`, all `source_knowledge_refs`, all `source_system_refs`, all
`failure_ontology_refs` / `repair_ontology_refs` and all `concepts[].children_terms` resolve inside
this lane. Every `source_interpretation` object carries a non-null `interpretation_basis` (3 of 3).
Every `extractor_synthesis` whole-system claim carries one (4 of 4). Every `kind: remedy` term
carries `executable_by` (16 of 16).

**(2) No locator contains a page number; every `page_start`/`page_end` is null.** Asserted
mechanically over **95 locators** — 45 SourceKnowledge, 4 SourceConceptSystem, 46 Q&A — with a regex
for `p.`/`pp.`/`page N`/`printed p`/`PDF page N`/`folio N`. **Violations: 0. Non-null page fields: 0.**
A whole-file scan of every `.yaml` and `.md` in the lane produced two hits, both inspected by hand
and both prose rather than citation ("exists only as a printed page"; "how the live chapter-1 lane
obtained printed pages"). Far more than the 15 items required were checked — all 95 were, in code —
and **nothing needed fixing.**

**(3) No chapter-1 duplication.** All 45 `concept_label`s were diffed against the 79 live labels in
`canon/knowledge/current/samara-making-breaking-grid-ch1/source-knowledge.yaml`, using exact match,
token-set Jaccard and character-sequence ratio. **Exact collisions: 0. Near-duplicates above
threshold (Jaccard ≥ 0.30 or ratio ≥ 0.62): 0.** Lowering the threshold to 0.18 produced a single
hit, `fragmenting_running_text_interferes_with_reading_and_is_conditionally_warranted` against the
live `gutter_from_running_text_margins_from_the_remainder`, which shares only the words "running
text" and is not a semantic near-duplicate.

Five pairs were then checked by hand because a token diff would not catch a semantic overlap; **all
five were kept, with reasons** (they are the five qualifications listed in §5). The short version:
in each case chapter 2 asks a different question about the same device, and collapsing the pair
would lose the qualification, which is the most valuable thing this span contains.

**(4) Application fraction.** Computed in code over `qa-bank.yaml`:
**17 of 46 items carry `requires_application: true` = 36.96%**, above the required 1/3. Answer-type
mix: application 9, source_position 7, mechanism 7, boundary_condition 5, failure_diagnosis 4,
comparison 4, repair 4, concept_definition 3, factual 2, tradeoff 1. Difficulty: 19 hard, 25 medium,
2 easy. Every item has non-empty `confounders`; no placeholders; no `TODO`.

---

## 7. Bindings — what was written, what was refused

Seven bindings: **five `evaluation`, two `governance`. No `creative_ir`, no `production`, no
`benchmark`.**

- **No `creative_ir`.** SPEC-01 was not supplied to this lane. A `creative_ir` binding requires a
  non-null `target_path`, `target_schema` and `target_schema_version`, and there is no honest way to
  produce them. Guessing a path would be worse than leaving the knowledge unbound.
- **No `production`.** Nothing here is a physical-production act in the SPEC-04 sense. The one
  physically executed remedy in the chapter — flinging paint, or dropping cropped images over a
  format, as a random physical chance operation — is a studio process for generating a layout. It is
  recorded in the source's own frame (`t_sgb_0028`, `executable_by: physical_production`) and
  **not** rewritten as a generative-media instruction.
- **No `benchmark`.** There is not a single measured quantity in this chapter.
- **Every `evaluation` binding carries `observation_unit`**: four `whole_asset`, one
  `asset_set_over_time` (the systematising-the-organic checks, which are only meaningful across a
  series).
- `evidence_basis` is `derived_from_source` for six and `extractor_inference` for one
  (`bnd_sgb_004`, which merges a rule shape the source states three times in three unrelated places
  and never joins). Neither `cross_source_supported` nor `empirically_supported` appears anywhere.

**`deterministic_composition` — an audit-level observation, not a binding.** Several of this
chapter's remedies are exactly executable geometry that a layout engine could perform without
judgement: the splitting/splicing/shifting operations (`t_sgb_0005`), column and row deformation
(`t_sgb_0007`), interval progressions including Fibonacci and A/B/A alternation (`t_sgb_0020`), the
programmatic chance procedures (`t_sgb_0029` — dissect on a formula, multiply successive point
sizes, overprint and delete overlaps), and recasting a data shape (`t_sgb_0037`). **SPEC-04 has no
target type for a deterministic executor.** The live chapter-1 audit already recorded that gap for
this same book. This lane records the fit and **does not invent a target type**; those five terms
carry `executable_by: deterministic_composite` in the ontology and are otherwise unbound. Noting it
here is the whole of the action taken.

**Print-medium contingency.** Much of this chapter assumes a printed page and a reader holding it.
Nine objects carry `historical_claim` and six carry `culturally_bounded`. The screen material
(`sk_sgb_0041`, `sk_sgb_0042`) is scoped to 2017 desktop browsers with mouseover and flyout
navigation and to the phones of that moment, and says so. **Nothing print-scoped was silently
transposed to a screen or a feed**, and `bnd_sgb_001`'s `applicability.limits` states outright that
Samara wrote nothing about a feed, a thumbnail, a five-second view or an autoplaying frame.

---

## 8. Where I was tempted to over-claim, and did not

1. **A test for intentional versus incompetent disorder.** This was the brief's highest-value ask and
   the chapter does not contain one. What it contains is a recurring contrast in the exhibit
   commentaries — "rhythmic cohesion instead of chaotic randomness", "carefully randomized",
   "decisively located", "a rigorously controlled network of geometric axes" — plus a rule-count
   limit stated for systems. It would have been easy to write a clean diagnostic and attribute it to
   Samara. Instead `sk_sgb_0044` and `sk_sgb_0045` are typed `source_interpretation`, their
   `interpretation_basis` states that the generalisation is the extractor's, and `scs_sgb_004`'s
   `system_level_uncertainty` says most of that system is ours. The chapter also offers **no negative
   control** — it never shows a project where apparent randomness turned out to be carelessness —
   and that absence is recorded rather than papered over.

2. **Claiming a viewer can tell the difference.** Samara asserts throughout that a viewer glosses
   over symmetrical work, that immediacy is "inviting", that disorder reads as crafted. There is no
   reader evidence anywhere in the chapter. Every such object carries `practitioner_assertion`
   (44 of 45 do) and a caveat naming the absence.

3. **Resolving the small-screen question.** `sk_sgb_0042` reports two open questions Samara asks and
   stops. He gives no answer and neither does this lane; `source_uncertainty:
   source_asks_open_question`.

4. **Choosing between "imagery governs the layout" and "the environment governs the image".** Two
   sections of the chapter push opposite ways and Samara never sets them side by side. The conflict
   is recorded in `scs_sgb_002.internal_structure.conflicts` and in `qa_sgb_0018`, whose answer says
   plainly that he offers nothing for choosing.

5. **Reading the *Universal/Unique* exhibit as a general method.** It would have made a striking
   claim — build the grid blind and let the content break it. It is one exhibit under an artificial
   brief, and `sk_sgb_0029`'s caveats say so twice.

6. **Inferring what a caption's figure shows.** Several captions are one clause short of a complete
   claim: "manipulate imagery in different ways", "compare the readability of the top configuration
   to the altered version". In each case the object stops where the text stops. This is why **no
   object carries `inferred_from_layout`** — the temptation was live and was declined rather than
   labelled.

7. **Treating Samara's screen usability list as a standard.** It reads like one. It is a designer's
   list in a 2017 layout book, overlapping accessibility requirements without being one, and
   `bnd_sgb_005`'s limits say so.

8. **Rounding the concept systems to five.** The pre-existing plan for this lane anticipated five.
   Four were written. A fifth would have been a re-slicing of material already in `scs_sgb_001` and
   `scs_sgb_003`, and a fabricated system is worse than a missing one under SPEC-03.

---

## 9. Source-text observations

The publisher's text contains four typographical errors — `rcetangular`, `esnure`, `shcool`,
`disection` — reproduced faithfully in the source and not evidence of OCR damage. This is a
publisher-produced EPUB, not a scan: no OCR signature, no column interleaving, no character
substitution. `extraction_uncertainty: ocr_degraded` and `column_interleaving` appear nowhere in
this lane, correctly.

The chapter is approximately 20,800 words of running text and captions.
