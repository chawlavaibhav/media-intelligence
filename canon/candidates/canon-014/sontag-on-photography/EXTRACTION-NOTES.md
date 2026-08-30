# EXTRACTION NOTES — Susan Sontag, *On Photography*

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon and nothing here may
be described as accepted. This lane has no authority to admit anything and §11 below is a judgement
offered for the Controller, not a recommendation acted on.

---

## 1. Counts

| | |
|---|---|
| SourceKnowledge objects | **22** (19 `explicit_source_claim` · 3 `source_interpretation`) |
| SourceConceptSystems | **3** — all three with `whole_system_claim.origin: extractor_synthesis` |
| OperationalBindings | **3** (3 evaluation · 0 creative_ir · 0 production · 0 governance · 0 benchmark) |
| Ontology terms | **29** (14 problem · 13 property · **2 remedy**) |
| Ontology concepts | **6** (4 source_specific · 2 canonical) |
| Q&A items | **28** |
| Q&A with `requires_application: true` | **10 — 35.7%** |

Source size: **338,033 characters** across 12 spine documents. Six essays; **four extracted from,
two refused entire** (see §7).

**The ratio to look at is the remedy ratio: 14 problem terms, 2 remedy terms, and neither remedy is
performable.** That is the strongest single piece of evidence in this lane for the project's standing
warning, and §11 turns on it.

## 2. Method

Read the whole book once, including both refused essays and the endnotes. Then a second pass with
one question held against every candidate: **is this a claim about how photographs are read, or is
it a claim about how they should be made?** Only the first kind was extracted. The second kind does
not exist in this book, which is the finding rather than the obstacle.

The unit of extraction is a passage identified by its opening phrase. Sontag's essays have no
section headings, so the addendum's requirement — a locator fine enough that a reader can find the
supporting text — is met by naming the essay plus a distinguishing phrase.

## 3. Honouring the standing warning

`canon/experiments/CANON-COVERAGE-MAP-V0.md` records that **Berger and Sontag are "critique, not
craft"**. `canon/planning/CANON-V1-SOURCE-PORTFOLIO.md` adds that a source of this kind is *"a
reading method, not a production method, and admitting it risks importing analysis the product
cannot act on."*

The warning was treated as correct and binding. Three consequences shaped the whole lane:

1. **Nothing was extracted as instruction**, because there is none to extract.
2. **The binding count is three, all of one narrow kind**, and the empty categories are documented
   with reasons rather than filled (§8).
3. **`answer_type: source_position` and heavily qualified objects dominate**, because the honest
   record of an essayist's argument is a record of her position.

## 4. The load-bearing rule — no critical observation became production advice

This is the rule the brief named and the one most likely to be broken by a careless extraction, so
the enforcement is set out in full and the checks are reported.

**The two objects at risk, named.**

- `sk_snt_0011` — the medium beautifies whatever it records, including what is not beautiful.
- `sk_snt_0013` — aestheticisation neutralises the distress the image conveys.

The invented advice these would produce is easy to write and would be wrong: *avoid aestheticising
difficult subjects*, *do not beautify suffering*, *compose images of hardship plainly*. Sontag says
none of that, anywhere. She describes what the medium does to a viewer's relation to a subject and
stops.

**Five enforcement measures, all present in the files:**

1. **An explicit caveat on each at-risk object.** `sk_snt_0011` carries a caveat in capitals stating
   that it is not production advice and must not be read as any; `sk_snt_0013` carries one saying it
   is the object most likely to be misread that way and that anything of that form would be an
   invention of this lane's. `sk_snt_0020` carries the same on the photographic-seeing claim.
2. **Neither at-risk object is bound to anything.** They appear in no OperationalBinding. The
   header of `operational-bindings.yaml` names them and states why.
3. **Both ontology terms carry the warning inside the definition.** `t_snt_0020` and `t_snt_0023`
   say, in the `definition_in_origin_frame` itself, that this is a diagnosis of an effect on viewers
   and that no instruction is inferred — so the warning travels with the term wherever it is
   retrieved.
4. **A Q&A item that tests the misreading directly.** `qa_snt_0028` asks whether someone may cite
   Sontag to argue a photograph should have been composed differently so as not to aestheticise its
   subject. The answer is no, and it gives her reason rather than a preference: a tendency that
   survives the intention to defeat it, and survives accurate captioning, cannot ground a
   recommendation about composing. Its confounders name both the standard misuse and the opposite
   over-correction — concluding she thinks such images should not be made, which she also never says.
5. **The three bindings are restricted to the unit and conditions of observation.** Each says in its
   `applicability.limits` that it generates no instruction about making anything. `bnd_snt_002`
   states it twice, because the attrition material is where "so vary your creative" would be
   smuggled in.

**The mechanical check, and its result.** All five YAML files were scanned in code for prescriptive
production phrasing — *you should*, *you must*, *make sure*, *be sure to*, *avoid using/showing*,
*do not use/show/shoot/frame/crop*, *shoot…*, *compose the…*, *crop the…*, *frame the subject so…*,
*choose a lens*, *use a…*, *set the…*, *prefer a…*. **Result: 0 hits across all five files.**

That check is a floor, not a proof — it catches phrasing, not intent — so it is reported alongside
the five structural measures rather than in place of them.

## 5. `interpretation_basis` — where it was needed and what it says

The brief expected `source_interpretation` to be needed often, because Sontag argues by accumulation
and allusion rather than by stating propositions. In the event **three of 22 objects** are typed
`source_interpretation`, and each carries a non-null `interpretation_basis` that names exactly what
is hers and what is ours:

- **`sk_snt_0002`** — both halves are hers (photographers always impose standards; photographs carry
  a presumption of veracity). The joining into one claim *about concealment* is ours, justified by
  the passage's structure and recorded as ours.
- **`sk_snt_0005`** — the retouching fact is hers and the desire for the idealised image is hers, in
  adjacent paragraphs. She never connects them. The causal joining is ours, and the basis is
  adjacency, which is weaker than an argument and is said to be.
- **`sk_snt_0017`** — three passages from two essays, unified by a variable (who controls the
  duration of looking) that Sontag never names. The unification is ours.

The remaining 19 are `explicit_source_claim` because she does state them, often quotably. That is
worth saying plainly rather than treating as a lucky outcome: *On Photography* reads as allusive but
is full of flat declarative sentences, and most of this bank is those sentences.

**A second correction went the same way.** A first draft attributed 22 stated mechanisms to her.
Re-checked object by object, **six** were the extractor's reconstruction of her reasoning rather
than reasoning she gives. All six now carry `mechanism.stated_by_source: false` and a
`mechanism.text` that opens with **"EXTRACTOR'S RECONSTRUCTION, NOT THE SOURCE'S"**, and
`mechanism_given` was removed from the evidence characteristics where it no longer applied. Final
count: **16 of 22 with a stated mechanism.**

## 6. Historical contingency — the rule and one worked example

Two rules, neither relaxed: **no claim was updated or modernised**, and **this lane does not assert
what has changed since**.

Nineteen of 22 objects carry `historical_claim` and nineteen carry `culturally_bounded`. Where a
premise is visibly of 1977, the caveat says *what she assumes* and stops there.

The worked example is `sk_snt_0003`, the trace, which is also the most tempting place to editorialise
in a lane inside a project that generates synthetic imagery. Its caveat reads: the whole claim is
conditional on the viewer believing in the causal link; Sontag does not examine that condition,
because in 1977 an image that looked photographic had one; the premise is recorded as she relies on
it, and this lane asserts nothing about whether it holds now. **The obvious modern observation is
not made.** The same restraint is applied on `sk_snt_0001`, `sk_snt_0014` (the circulation regime),
`sk_snt_0017` (broadcast television), `sk_snt_0018` (the still photograph as a physical object) and
`sk_snt_0022` (the ratio of images to occasions).

## 7. What was deliberately not extracted

**Two of six essays refused entire**, both read in full before refusing:

- ***America, Seen Through Photographs, Darkly*** — a literary argument about American cultural
  self-understanding conducted through Whitman, Walker Evans and Diane Arbus. Excluded by the brief
  and the exclusion is correct: its content is a reading of American letters.
- ***Photographic Evangels*** — the essay on whether photography is an art, conducted through what
  Stieglitz, Weston, Strand, Adams and Callahan said about themselves. Its substance is the
  art-status debate and aesthetic judgement of named photographers. It contains sentences that would
  look extractable in isolation — on originality, on self-expression, on the machine used
  "unmechanically" — but each is a report of a photographer's self-description inside an argument
  about status, and lifting them would produce objects about what practitioners claimed for
  themselves rather than about how images are read.

***A Brief Anthology of Quotations*** was also refused: it is other people's sentences assembled
without commentary, and extracting from it would attribute their claims to this source.

**Refused within the four extracted essays:**

- **The art-historical survey.** The nineteenth-century material on Fox Talbot, Daguerre, Hill,
  Cameron, Nadar; the Surrealism argument that occupies most of *Melancholy Objects*; the
  Bauhaus/Cubism influence discussion. Only two things were taken from *Melancholy Objects* at all,
  and neither is its Surrealism thesis.
- **Biography and aesthetic judgement of named photographers.** Sander, Atget, Arbus, Weston,
  Strand, Riis, Hine, Lartigue, Vroman, Laughlin, Abbott, Lesy, Adelman. Where a photographer's work
  is the vehicle for a general claim, the claim is recorded and the photographer is not named — the
  examples throughout this lane are described rather than attributed.
- **The China essay-within-an-essay.** A large part of *The Image-World* is an extended contrast
  with Chinese image practice as reported in the early 1970s, built on the official criticism of one
  documentary film. It is period political argument of a specific moment and reads as such. Only the
  general mechanism it frames — recycling and "the interesting" — was extracted, and `sk_snt_0021`
  carries a caveat saying the surrounding contrast was refused.
- **The camera-as-gun material.** The predation metaphor, *Peeping Tom*, the photographic safari,
  "a sublimated murder". It is argument by metaphor, and although "photographing is essentially an
  act of non-intervention" is recorded as an ontology term (`t_snt_0028`), no object was built on
  the metaphor.
- **The family-album and memento mori material as an object.** `all photographs are memento mori` is
  recorded as a term (`t_snt_0016`) because it names something real in her frame, but no object was
  built on it: the surrounding argument is about the nuclear family in industrialising Europe and
  America, and extracting it would import a sociological claim about 1970s family structure that
  this project has no use for and no way to assess.
- **The Plato framing and the closing "ecology of images".** The first is a literary conceit; the
  second is recorded as a remedy term with `executable_by: [unknown]` precisely because it names a
  remedy with no method.

**Not one section of the four extracted essays was found to yield nothing** — but two of six essays
did, and that is the answer to the brief's instruction to say so where a section yields nothing this
project could ever use.

## 8. Bindings — three, all of one kind, and four categories refused

Three evaluation bindings, each doing one narrow job: **fixing the unit and conditions of
observation under which an image is read**. None says anything about making anything.

- `bnd_snt_001` — image and its accompanying text are one artefact for assessment (`whole_asset`).
- `bnd_snt_002` — attrition effects are properties of a set over time, not of any asset
  (`asset_set_over_time`). This is the only binding in the lane whose unit is larger than one asset.
- `bnd_snt_003` — two preconditions on the assessor: identification of the subject, and the frame
  the audience already holds (`whole_asset`).

**Refused, with reasons, each recorded in the file's header:**

- **`creative_ir`** — not attempted; forbidden; nothing here is a field.
- **`production`** — the load-bearing refusal. See §4.
- **`benchmark`** — she generates no test case and no comparison. Her comparisons are between
  historical episodes read differently by different publics, which are not minimal pairs and could
  not be constructed as any.
- **`governance`** — two candidates examined and both refused. `sk_snt_0007` (a photograph's meaning
  is its use) resembles `retrieval_governance` until you notice its subject is how *photographs*
  behave when separated from context, not how this project's knowledge behaves. `sk_snt_0003` and
  `sk_snt_0004` resemble `evidence_interpretation` until you notice they govern how a *viewer*
  weighs a photograph, not how this project weighs a source. Under SPEC-04's guard, a candidate
  fitting none of the six permitted consumers is not a governance binding, so both are unbound.

**No model capability is inferred from this source anywhere.**

## 9. The concept systems are hypotheses, and say so

All three carry `system_type_origin: extractor_inferred` and
`whole_system_claim.origin: extractor_synthesis` with a non-null `interpretation_basis`. This book
contains no framework, no numbered set and no stated structure, and the characteristic way of
getting an essayist wrong is to build her one because she returns to the same themes.

Each system's `system_level_uncertainty` says how much is ours, and each carries a recorded
objection rather than a smoothed surface:

- `scs_snt_001` — the acquisition material can be read as an independent argument owing nothing to
  the trace, and she herself asserts that photographs are as much an interpretation as paintings are,
  which sits awkwardly with a system organised around what makes them different in kind.
- `scs_snt_002` — one member is itself typed `source_interpretation`, so a hypothesis sits inside a
  hypothesis.
- `scs_snt_003` — **the source directly resists this system's whole-system claim.** Sontag says
  familiarity does not entirely explain which conventions of beauty get used up, and that the
  attrition is moral as well as perceptual — which is a statement that the single route the system
  proposes is insufficient. The system is kept because the members genuinely cluster; the objection
  is kept with it, as a `conflicts` entry.

## 10. Tensions preserved, not resolved

1. **Innocent relation versus imposed standards.** Both within a few sentences of each other in *In
   Plato's Cave*. Recorded as a `conflicts` entry in `scs_snt_001`, as a `distinct_from` relationship
   between `t_snt_0002` and `t_snt_0026`, and as a Q&A item (`qa_snt_0027`) that asks the reader to
   say what the tension implies about using the source.
2. **The still's force versus the still's cost.** Its stasis keeps a moment open for scrutiny and
   removes the duration understanding needs. Recorded as a `tradeoffs` entry in `scs_snt_002` and as
   a `distinct_from` relationship.
3. **Photographs cannot create a moral position — and one photograph probably did more than a
   hundred hours of television.** Both hers, in the same essay, unreconciled by her and unreconciled
   here. Recorded as a `source_stated` caveat on `sk_snt_0016` and in `bnd_snt_003`'s limits.
4. **Two attritions that look like one.** Recorded as a `distinct_from` relationship, as a
   `conflicts` entry, and as the Q&A item `qa_snt_0026`, which asks the reader to catch the collapse.

## 11. Does this source earn a place in a media-production Canon? — this lane's judgement

The brief asked for an honest verdict either way. Here it is, with the reasoning, offered to the
Controller and binding on nothing.

**Verdict: qualified yes, on a strictly limited basis — and the project's warning is right about
almost all of it.**

**The case against, which is strong and mostly correct.** The remedy ratio is the evidence: 14
problem terms, 2 remedy terms, and neither remedy performable — one is another writer's proposal
that Sontag reports in order to refute, and the other is the last sentence of the book, a
conservationist gesture with no method, no agent and no procedure. A source that diagnoses
continuously and prescribes nothing is a source a production system cannot act on, which is exactly
what "critique, not craft" says. Three bindings from twenty-two objects, none of them touching
production, is the same fact stated in the binding layer. And this material carries a specific
hazard the other two sources in this run do not: the at-risk objects read like advice, so admitting
them raises the standing risk that someone downstream converts *photography aestheticises suffering*
into a composition rule and attributes it to her. Five separate measures were needed in this lane to
prevent that, which is a cost the source imposes on everyone who handles it.

**The case for, which is narrower than it looks but is real.** Four things here are not available
anywhere in live Canon and are not craft advice in disguise:

1. **`sk_snt_0016` — an image lands inside a frame of understanding it cannot itself supply.** The
   contribution of photography follows the naming of the event; without a relevant prior
   consciousness the image reads as unreal. This is a limit on what any image can accomplish, and a
   project that produces images to change what an audience believes has no other source stating it.
2. **`sk_snt_0007` and `sk_snt_0008` — meaning is use, and the caption both dominates and fails to
   secure.** The image-plus-text unit of assessment falls out of this directly, which is
   `bnd_snt_001` and is the most immediately usable thing in the lane.
3. **`sk_snt_0014` and `sk_snt_0012` — the two attritions.** A rising threshold driven by the supply
   of images, and conventions of beauty exhausted by the images that established them. Stated in
   1977 about a far smaller supply of images than any project now handles. This lane records what
   she says and refuses to extend it — but the shape of the claim is the reason someone would want
   this source at all.
4. **`sk_snt_0003` and `sk_snt_0004` — the trace, and what falsifying a photograph falsifies.** For
   a project generating synthetic imagery this is the most consequential material in the book, and
   the reason is precisely that Sontag did not write it about synthetic imagery: she identifies the
   authority as causal rather than evidential, on a premise she never had to examine. Whether that
   premise survives is not this lane's question and is not answered here.

**Where the line should fall.** The honest recommendation is not "admit" or "refuse" but *admit as a
reading source with production bindings prohibited by rule*. This lane is already built that way,
and if the material is ever consolidated the prohibition should be attached to the source rather
than left to each future extractor's care — because the caveats in this directory protect these
objects only for as long as someone reads them.

**One point against my own verdict, stated because it is the strongest one.** Almost everything
above is a limit on what images do, not a capability. A Canon full of limits and empty of methods
would be a Canon that explains failures well and produces nothing, and this source pulls in that
direction. The four items listed are worth the cost; the other eighteen objects in this lane are, on
this lane's own assessment, closer to the coverage map's warning than to its exceptions.

## 12. Self-check results

1. **All five YAML files parse** under `yaml.safe_load`.
2. **No page number anywhere.** 22/22 objects have `page_start` and `page_end` null; 28/28 Q&A
   locators contain no `p.`/`pp.`/`page N` construction; asserted in code by regex over every
   locator string. 0 failures, 0 fixes required. Audit pattern **`no_authored_page`** recorded. No
   `false_page_affordance`: this book contains no internal page cross-references.
3. **No production advice.** Enforced by five structural measures and checked mechanically over all
   five files for prescriptive production phrasing: **0 hits.** Full account in §4.
4. **`requires_application` = 10/28 = 35.7%**, computed in code. Required minimum one third:
   **met.** The first draft came in at 25.0%, below the floor. It was corrected by **rewriting three
   question stems into genuinely applied form** — judging an unidentifiable crop, diagnosing which
   of the two decays an archive image has undergone, and reading an image reused in an unrelated
   advertisement — not by relabelling recall questions, and not by deleting content to move the
   denominator. Every applied item applies a way of **reading** an image; none applies a way of
   making one.
5. **Every reference resolves.** All `source_knowledge_refs`, `source_system_refs`,
   `failure_ontology_refs`, `repair_ontology_refs`, `members[].sk_ref`, `children_terms`,
   `relationships[].from/to` and every `intra_source_relations[].target` checked in code. 0 dangling.
6. **Every `source_interpretation` carries a non-null `interpretation_basis`** — 3 of 3, checked in
   code. Every `extractor_synthesis` whole-system claim carries one — 3 of 3, checked in code.
7. **Every `kind: remedy` term carries `executable_by`** — 2 of 2. Neither carries
   `generative_respecification`.
8. **No `xs_` concept and no `same_failure_family` relation** created.
9. **No `empirical_within_source`** on any object — 0 of 22, checked in code. There was no
   candidate: this book contains no measurement of any kind.
10. **`source_support: text` on all 22 objects**, with `inspected: {text: true, figures: []}`. The
    book reproduces no photographs, so there is no `figure_semantic_binding_lost` hazard here — not
    because the route recovered figures, but because there are none.
11. **Honest count, not target count.** The range was 15–28 objects and 18–30 Q&A. This lane sits at
    22 and 28, from a book of 338,033 characters of which two of six essays were refused entire.

## 13. Write boundary

Every file written by this lane is inside
`canon/experimental/book-expansion-qa-v1/sontag-on-photography/`. Nothing under
`canon/knowledge/current/**`, `canon/audit/**`, `coordination/**` or any SPEC file was created,
edited or deleted. Nothing was committed.
