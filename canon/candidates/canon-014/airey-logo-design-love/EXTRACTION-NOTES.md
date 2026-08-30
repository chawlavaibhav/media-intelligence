# Extraction notes — David Airey, *Logo Design Love*

**EXPERIMENTAL — NOT LIVE CANON.** Lane `airey-logo-design-love` of the non-merge
`book-expansion-qa-v1` expansion. Nothing in this directory is accepted Canon, and nothing here may
be described as accepted, corroborated or admitted. No cross-source promotion was performed.

---

## 1. What was produced

| File | Count |
|---|---|
| `source-knowledge.yaml` | **50** SourceKnowledge objects (`sk_logo_0001`–`sk_logo_0050`) |
| `source-concept-systems.yaml` | **4** SourceConceptSystems |
| `operational-bindings.yaml` | **17** bindings — 10 `evaluation`, 2 `benchmark`, 3 `production`, 2 `governance`, **0** `creative_ir` |
| `ontology-mappings.yaml` | **45** terms · **30** relationships · **9** concepts |
| `qa-bank.yaml` | **57** Q&A items, **20** with `requires_application: true` (**35.1 %**) |

---

## 2. Method

1. Read the page-marked extraction end to end for printed 2–191 (the author's own text).
2. Refused Ch. 6 (*Pricing design*, printed 76–89) in full, and refused the business-of-design,
   self-promotion, portfolio, blogging, internship and employment material in Ch. 10. See §8.
3. Rendered **23 pages** with `pdftoppm` and looked at them, chosen as the pages where a claim
   depends on seeing the mark rather than on reading the sentence. Inventory in §5.
4. Wrote incrementally — the schema files were appended in chunks of ten to twelve objects and the
   Q&A bank in chunks of thirteen to fourteen items, after a note that an earlier attempt on this
   lane died mid-write on a single large write.
5. Ran the self-checks in §9 in code.

### Locator basis — Case 1, and independently re-verified

The supplied text declares `printed page = PDF page − 13 (folio agreement on 193 pages)`. This lane
did not take that on trust. Every one of the **23 rendered pages** carries a visible printed folio,
and all 23 agree with the stated offset:

| PDF | 20 | 28 | 36 | 37 | 38 | 39 | 40 | 42 | 43 | 44 | 45 | 46 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **folio read on the page** | 7 | 15 | 23 | 24 | 25 | 26 | 27 | 29 | 30 | 31 | 32 | 33 |

| PDF | 48 | 50 | 77 | 86 | 114 | 119 | 124 | 125 | 126 | 153 | 201 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **folio read on the page** | 35 | 37 | 64 | 73 | 101 | 106 | 111 | 112 | 113 | 140 | 188 |

**No disagreeing folio was found.** All locators cite printed numbers.

**Span used:** printed **2–191**. Printed 1 is a part title, printed 192–197 is the "Design
resources" appendix and printed 198–204 the index; nothing was extracted from any of them.
**Printed 99–100 carry no extractable text** — they are full-bleed images from the Tenth Church
project, and the page markers jump from 98 to 101 as a result. Seven further pages inside the span
(printed 16, 20, 40, 41, 95, 138, 142, 143) carry almost no text and are image or part-title pages.
Recorded rather than passed over silently.

---

## 3. The single largest hazard: this copy is not the English book

**The local file is a degraded, unattributed Spanish machine translation.** Its title page reads
*"Logo Design Love: Una Guía para crear identidades marca icónica"*; the bibliographic block (New
Riders, Berkeley; © 2010; David Airey) is intact, but no translator, translation copyright or
Spanish ISBN appears anywhere. The translation is visibly machine-produced: studio names are
translated as common nouns (**Bunch** → *"Manojo"*, **Someone** → *"Alguien"*, **UnderConsideration**
→ *"su examen en"*, **Moon Brand** → *"Marca Luna"*, **Lindon Leader** → *"el líder de Lindon"*,
**TIME** → *"HORA"*), ligature loss from the underlying text layer is carried through as word
breakage (*"de fi nitivamente"*, *"fl ujo"*), and the printed folio on page 65 is rendered as the
words *"sesenta y cinco"*.

**Consequence, and it is not cosmetic.** The brief asked for one thing verbatim: Airey's own
vocabulary for the *logo / identity / brand* distinction. **It cannot be supplied from this copy.**
`sk_logo_0034` records the SUBSTANCE of the three levels with an explicit caveat that the English
wording is unverifiable here; `scs_logo_004` repeats the caution at system level; `qa_logo_0001`
says so in its `support` field. Every `source_terms` entry in the lane is a back-translation into
English of the Spanish actually on the page, and **every term in `ontology-mappings.yaml` is marked
`verbatim: false`** — 45 of 45. Any downstream use that turns on Airey's phrasing must go to an
English edition.

The **figures are unaffected**: the logos, sketches and photographs are the original artwork.
One consequence of the translation does reach a figure, and it is recorded at `sk_logo_0049`: the
caption on printed 64 calls the redesigned Tropicana cartons the *"successfully renamed identity"*,
flatly contradicting the body text on the facing pages. That is a translation error in this copy,
not a claim of the book, and it is the kind of thing that would have been quoted straight if the
page had not been looked at.

---

## 4. Audit patterns observed

- **`figure_semantic_binding_lost`** — pervasive and central, exactly as anticipated. This is a book
  about marks; a large share of its argument is carried by a logo printed beside the paragraph.
  §5 gives the honest counts.
- **`in_figure_text_absent`** — the marks themselves carry lettering that the text layer does not
  contain (the FedEx, NHS, NMA, TalkMore, Tenth Church and Woodmere wordmarks are all artwork). Any
  claim about what a mark *says* required rendering the page.
- **A reverse case worth naming.** Printed 188, tip 19 *"Reverse it"*, prints the `amp` mark **black
  on white, not reversed**. The page does not demonstrate its own instruction. Found by rendering
  the page; recorded at `sk_logo_0010` and in `bnd_logo_003`, and it is the seed of `qa_logo_0041`.
- **`ocr_degraded`** — ligature loss in the underlying text layer, carried through the translation.
  Affects word forms, not page identity.
- **`false_page_affordance`** — **not present.** The folios are authored and were verified on 23
  rendered pages.
- **`no_authored_page`** — not applicable; this is a paginated PDF, Case 1.

---

## 5. Figure inspection — the honest counts

**23 pages rendered at 90 dpi and looked at**, out of roughly **81 pages in the span that carry a
figure credit caption** and 188 pages of author text present in the file. So **about 26 % of the
book's captioned figure pages were inspected**, chosen for claim-dependence rather than sampled.

Of the **50** SourceKnowledge objects:

| | count | share |
|---|---|---|
| rest at least partly on a figure that was **rendered and inspected** (`source_support: text_and_visual`) | **16** | 32 % |
| rest on **text alone** (`source_support: text`) | **34** | 68 % |
| carry `extraction_uncertainty: figure_not_inspected` | **7** | 14 % |

The seven flagged objects are `sk_logo_0021`, `0026`, `0036`, `0039`, `0040`, `0041`, `0048`. In
each, the visual claim is **not inferred from the text**: the object's `inspected.figures` field
names which pages were not rendered and states that no property of them is asserted. Two of the
seven (`0026`, `0049`-adjacent material) are mixed cases where one figure was inspected and another
was not, and the field says which.

`sk_logo_0021` is a special case worth naming: it is flagged `figure_not_inspected` because **there
is no figure to inspect**. Four of the five marks it turns on — BMW, Xerox, Virgin Atlantic, Tiger
Woods — are named in prose and printed nowhere in the book. The reader is being asked to recall
them. That observation became `qa_logo_0052`.

### What inspecting the pages actually bought

Not decoration. Six findings that a text-only pass would have got wrong or missed:

1. **Woodmere (printed 111–113)** is the strongest figure-verified claim in the lane. The text says
   an agency presents in black and white first. The pages show **thirty-two concepts across two
   spreads, every one in black, white and grey**, then the chosen mark in colour with three Pantone
   chips. The sequence is visibly what the pages do.
2. **Sugoi (printed 35)** is the book's only direct visual evidence for the small-size claim, and it
   does support it: the mark moulded into a metal zip pull and woven into a garment label.
3. **Bethnal Green (printed 15)** shows the star **engraved into a pint glass** — an application
   with no colour at all, where only form survives. That is a stronger versatility case than the
   text makes.
4. **French Property Exhibition (printed 37)** prints old and new side by side. The old mark is the
   book's clearest printed instance of the failure the one-thing rule targets; the text never says so.
5. **Yellow Pages (printed 140)** lays both concepts out on one page — the method being described is
   physically enacted on the page.
6. **Vanderbilt (printed 29)** is **not the mark in isolation**: it is a photograph of the identity
   realised as campus ironwork. The oak leaf is legible; the acorn the text names is **not
   resolvable** at the resolution rendered. `sk_logo_0023` says so rather than repeating the text.

### Where a text-only pass would still be trusted, and should not be

The Ecometrica and other mind-map spreads (printed 91–94), the sketch sheets (printed 96, 98,
103–105, 108), the Kerling mock-ups (printed 114–115), the CIGNA explorations (printed 70–71), the
New Mexico Heart Hospital marks (printed 57–58) and the HBD marks (printed 59–61) were **not
rendered**. Every claim resting on them is text-only and is flagged. In particular, `sk_logo_0041`
does **not** endorse the source's caption claim that the HBD mark "works equally well without the
accompanying company name" — that is a visual claim about a figure this lane did not look at.

---

## 6. Evidence posture: what this source is, and what it is not

**Survivorship is unmanaged and it is the defining weakness of the book.** Every exemplar is a
famous, surviving, commercially successful mark selected after the fact. There is **no unsuccessful
comparison set anywhere in the book** and **no controlled comparison of any kind**. The two
"failures" it does show — Tropicana and New Coke — are famous *reversals*, selected for the same
reason the successes were: everyone has heard of them. So the sample is selected on the outcome at
both ends. Nothing in this lane is evidence that the properties Airey names *cause* commercial
success, and `bnd_logo_016` exists specifically to make that handling rule explicit rather than
leaving each downstream reader to rediscover it.

**Evidence characteristics used, and why:**

- `practitioner_assertion` on 34 of 50 objects. This is the book's default register.
- `anecdotal` where a single narrated project is the whole support.
- `outcome_claimed` on every commercial figure: the Tropicana 20 % and $33 m, the 400,000 New Coke
  complaints, the 8.3 m Harry Potter copies in 24 hours, the NHS's "tens of millions of pounds".
  All are cited to trade press or asserted by a party to the project. None has controls.
- `empirical_within_source` is used **exactly once**, on `sk_logo_0033`, for the Landor/FedEx
  nine-month research study — the only place in the extracted span where a measurement is reported
  rather than an opinion offered. It is the honest use of that characteristic and it is not stretched.
- `historical_claim` on the era-bound material: 2010 print economics and printer pricing, desktop
  software, outdoor media, the second-hand trademark characterisation, the marks named as
  contemporary exemplars.
- `culturally_bounded` on the register examples (lawyer / crematorium / cancer charity are Western
  commercial category norms), on the Zia Pueblo case, and on the "symbols are recognisable
  regardless of culture" claim — which the book's own five-pointed-star rejection contradicts.
- `mechanism_absent` where the source asserts without arguing. This is common and is marked, not
  papered over.

**Two internal contradictions are recorded as the source's own and are not resolved:**

1. Tip 5 (printed 180) says a symbol "could prove restrictive" for a company expanding into other
   markets; Ch. 2 (printed 13) says symbols are precisely what let companies cross language barriers
   and compete globally. Same condition, opposite advice, 167 pages apart, neither cross-referencing
   the other. Recorded at `sk_logo_0035`/`sk_logo_0037` with `relation: contradicts`, in
   `scs_logo_004.internal_structure.conflicts`, and as `qa_logo_0020`.
2. Ch. 3 treats simple-and-relevant as the goal; Chermayeff at printed 145 declares them necessary
   but insufficient. Airey never carries the qualification back. `sk_logo_0025`, `qa_logo_0019`.

---

## 7. The checkable mark-quality tests — the point of this lane

The project's first pilot is a brand identity job and the Canon holds nothing about identity marks.
This is what the book supplies that can actually be checked against a rendered mark. **Ten checks**,
grouped by whether they have a determinate outcome. The grouping is **ours**, not the source's —
`scs_logo_002` says so at length.

**Determinate — a reduction, something survives or it does not:**

| Check | The source's target | Locator |
|---|---|---|
| Reduce to about one inch | "no loss of detail" | printed 34, restated 187 |
| Reduce to one colour | a one-colour version must exist and work | printed 186, tip 15 |
| Place on a dark ground | a version that works on dark backgrounds | printed 188, tip 19 |
| Rotate / invert | no unwanted reading from any angle | printed 188, tip 20 |
| Print a size-and-colour sweep and inspect the paper | clean · good contrast · not pixelated | printed 187, tip 18 |

**Judgement — needs a person; the source supplies no threshold for any of them:**

| Check | The source's target | Locator |
|---|---|---|
| Figure-ground **and** element-to-element contrast | "clearly identified" | printed 187, tip 16 |
| Silhouette recognition | "its shape or outline alone gives it away" | printed 30, restated 38 |
| One-phrase describability | distinctive marks are "almost always" describable easily | printed 31 |
| Single distinguishing feature — count the devices | "one. Not two, three, or four" | printed 36, tip 6 at 181 |
| Immediate legibility of lettering | "if most people can't read it straight away, don't use it" | printed 185, tip 12 |

**The two most valuable and least obvious of the ten**, because a competent designer would not
arrive at them by default:

- **Tip 16's *internal* contrast half.** Everyone checks the mark against its background. Almost
  nobody checks whether two elements *inside* the mark stay separable — and that is exactly what
  breaks when the mark moves to a dark ground or drops to one colour. It is the check that makes the
  other reductions diagnostic instead of merely descriptive.
- **The one-phrase description test.** Costs nothing, needs no rendering pipeline, and catches the
  failure the count-the-devices check argues for, from the opposite direction.

**The scoping clause worth more than most of the checks:** tip 12's *"especially when the brand
isn't well known"*. It concedes that recognition substitutes for reading — which means the
legibility gate binds hardest on exactly the case a new product is in, and loosens for the
established brands the book's examples are drawn from. That asymmetry is `qa_logo_0026` and
`qa_logo_0054`.

**Where the book stops, stated plainly so no one fills the gap and calls it Airey:** no numeric
contrast threshold; no test for whether a mark survives *reversal* at all (a mark whose meaning
lives in internal negative space can invert — the book prints several such marks and never raises
the possibility); nothing about screen rendering below one inch; no protocol for the outline test;
no population, exposure time or distance for the legibility gate. Every binding that touches these
says so in `applicability.limits`.

---

## 8. Deliberately refused

- **Ch. 6, *Pricing design*, printed 76–89, in full.** Fees, hourly versus fixed rates, rush
  mark-ups, print mark-ups, currency risk, deposits, spec work. Business-of-design, out of brief.
- **Self-promotion, portfolio and blogging guidance** (printed 162–167), internships (173–174),
  friends-and-family pricing (170–171), workload (176), employment contracts and ownership (177).
- **Tool recommendations as recommendations** (printed 175–176, tip 9 at 183). The *reasoning* about
  scalable vector artwork was extracted at `sk_logo_0039`; the brand names were not.
- **Agency-positioning tactics** in Ch. 8 — the four rules quoted from a consultant about reaching
  the decision-maker, including the scripted line to use when a contact resists. Business
  development, not design knowledge. The *design*-relevant residue of that chapter — the
  strategic-input / execution-freedom boundary, sell the idea not the details, and the
  build-it-and-compare repair — was extracted at `sk_logo_0050`.
- **Ch. 9 mostly refused.** Motivational prose and peer quotations. Four items kept: the Chermayeff
  qualification (145), step away from the computer (149), lateral-thinking manipulations (155), and
  Vit's "dozens of equally valid solutions" (153–154, folded into `sk_logo_0044`'s caveats).
- **Tips 1, 3 and 23**, which restate process points already carried by other objects.
- **Client narratives whose only content is who the client was.** Where a narrative carries a
  reusable mechanism the mechanism is extracted and the narrative is not.

---

## 9. Self-check results

All run in code. Scripts: `scratchpad/selfcheck_logo.py`, `scratchpad/spotcheck_logo.py`.

**1. Every YAML parses.** All five YAML files load under `yaml.safe_load`. Cross-reference integrity
verified in code: 0 dangling `intra_source_relations` targets across 50 objects; 0 unresolved
`sk_ref` in 4 systems; 0 unresolved `source_knowledge_refs` / `source_system_refs` /
`failure_ontology_refs` / `repair_ontology_refs` across 17 bindings; 0 unresolved term ids across 30
relationships and 9 concepts; 0 duplicate ids in any file.

**2. Locator span assertion — PASS, mechanically.** Every number introduced by a `p.` or `pp.`
marker in every `source_locator` was parsed and tested against the real span. **90 page markers
parsed across 57 items, 74 distinct printed pages cited, range 8–190, all inside printed 2–191.
Zero failures.** The same assertion was run over `provenance.page_start` / `page_end` on all 50
SourceKnowledge objects and all 4 systems: zero outside the span, zero inverted ranges.

**3. Spot-checks against the cited page — 51 checks across 45 of the 57 items (79 %), all passed on
the first run, zero fixes required.** Each check pulls the text of the cited *printed* page out of
the page-marked extraction by its own marker and asserts that a distinctive Spanish string the
answer relies on is actually present there — e.g. `qa_logo_0002` → printed 34 contains *"un mínimo
de alrededor de una pulgada"*; `qa_logo_0012` → printed 65 contains *"20 por ciento"*;
`qa_logo_0046` → printed 54 contains *"900 nombres de empresas"*; `qa_logo_0040` → printed 39
contains *"las reglas están hechas para romperse"*. Accent- and case-insensitive matching.

**4. Application fraction — computed in code: 20 of 57 = 35.09 %.** Above the required one third.
This required adding three items late; the honest note is that the first pass came in at 31.5 % and
the fix was to **write three more application items** (`qa_logo_0055`–`0057`), not to relabel
existing ones.

**5. Figure inspection — reported in §5.** 16 of 50 objects (32 %) rest partly on an inspected
figure; 34 (68 %) on text alone; 7 carry `figure_not_inspected`.

**6. Vocabulary conformance.** Every `evidence.characteristics` value, `source_uncertainty`,
`extraction_uncertainty`, `intra_source_relations[].relation`, `source_support`, `target_type`,
`observation_unit`, `governance_consumer`, `evidence_basis`, `answer_type`, `difficulty`,
`knowledge_type` and SPEC-05 `relation` checked against the contract's fixed lists in code. Zero
out-of-vocabulary values. No `xs_` concept, no `same_failure_family`, no `cross_source_supported`,
no `empirically_supported`, no decimal confidence, no `informs` field, no Creative IR path, no
product vocabulary.

**7. Write boundary.** Only the seven files in this lane directory were written. Nothing under
`canon/knowledge/current/**`, `canon/audit/**`, `coordination/**`, `governance/**` or any SPEC file
was created, edited or read-modified. Nothing was committed.

---

## 10. Where I was tempted to over-claim and did not

Recorded because the temptations were real and the restraint is the substance of the lane.

1. **The verbatim vocabulary.** The brief asked for Airey's logo/identity/brand words *verbatim*.
   Producing a confident-sounding English quotation from the Spanish would have satisfied the brief
   on its face and been unverifiable. Recorded the substance, flagged the impossibility in three
   places, and marked all 45 terms `verbatim: false`.
2. **A numeric contrast threshold.** Tip 16 names two contrast relationships and gives no number.
   It would have been easy and useful to attach 4.5:1 — and it would have attributed to a 2010
   design book a value from a web accessibility standard it has never heard of. `bnd_logo_003` says
   the source supplies no threshold and can therefore report merging, not a pass. It appears as a
   confounder on three Q&A items.
3. **A "logo quality score".** Ten checkable properties is exactly the material from which someone
   builds a composite score. The source supplies pass conditions for five of the ten and none at all
   for the other five. `scs_logo_002` splits them for that reason and states that a checker running
   only the automatable half will pass marks the source would reject.
4. **The Tropicana causal claim.** 20 % in two months and $33 m is the most quotable thing in the
   book. It is trade-press-sourced, uncontrolled, and Airey himself floats an alternative reading
   (deliberate alignment with store-brand packaging) and notes most redesigns do not go this way.
   `bnd_logo_016` exists to stop the figure being laundered into evidence.
5. **A fifth concept system.** A "redesign decision framework" out of Ch. 5 was drafted and
   **dropped**: re-reading, the chapter is narrated cases, not interacting principles, and
   everything it teaches is already carried by `sk_logo_0049`. The drop is recorded in the header of
   `source-concept-systems.yaml` rather than silently made.
6. **`creative_ir` bindings.** Zero written. SPEC-01 was not in this lane's read set, so a target
   path would have been guessed — and more fundamentally, Airey's knowledge is about a static
   artefact's reproduction behaviour, not about specifying a generated asset. Stated in the file
   header rather than left as an apparent omission.
7. **The acorn.** The text says the Vanderbilt mark integrates an oak leaf *and an acorn*. I
   rendered the page; the acorn is not resolvable. The object says the leaf is legible and the acorn
   is not, instead of repeating the caption.
8. **The Tenth Church tension.** Airey's one-thing rule and his praise of a wordmark carrying five
   conceptual themes are in tension. The tempting move was to resolve it silently by reading "one
   thing" as "one device". Instead the tension is recorded as the source's own in `sk_logo_0017`'s
   caveats and in `bnd_logo_007`'s limits, and the device-versus-meaning reading appears in
   `qa_logo_0027` **explicitly labelled as a reading Airey does not draw**.
9. **The `empirical_within_source` characteristic.** Applied once, to the FedEx research study.
   Several other passages report numbers and none of them is a measurement made by the source.

---

## 11. Observations for cross-source review (NOT promotions)

**These are observations only.** No ontology relationship, no `cross_source_supported` evidence
basis, no `xs_` concept and no claim inside any SourceKnowledge object encodes any of this. Nothing
below is corroboration, and none of it may be treated as such without Controller review and
Audit-Gate lineage that do not exist here.

### `vignelli-canon-intangibles` (live) — genuinely adjacent, and the differences matter more

Skimmed specifically to separate agreement from restatement.

- **Apparent agreement on simplicity, timelessness and the designer's authority.** The apparent
  agreement is shallower than it looks, and the *grounds* diverge sharply. Vignelli's discipline is
  argued from **intellectual elegance and semantic responsibility** — simplicity as a discipline the
  designer owes the work. Airey's is argued from **reproduction economics and viewer processing
  cost**: it survives the zip pull, it survives one-colour print, the viewer only gets a glance.
  Two arguments arriving near the same instruction from different premises is **not** two sources
  corroborating each other, and would be a mistake to record as such.
- **A real and instructive divergence on the client.** Vignelli's position on the designer's
  authority is close to absolute. Airey's is transactional and he is explicit about it: swallow your
  pride, listen, build the client's idea and show the comparison — and he narrates a case
  (`sk_logo_0050`, Berthier) in which the client was right and he was wrong. On the same question
  they are not aligned, and preserving that is more valuable than harmonising it.
- **A cheap resemblance CHECKED AND REJECTED.** Both books say something that reads as "colour is
  secondary". They do not mean the same thing. Airey's claim (printed 30) is a **working-method**
  claim about which channel carries distinctiveness during generation. Reading it as a general
  aesthetic position on colour would misrepresent him, and any future mapping should record this as
  `distinct_from` rather than as agreement.

### `miller-storybrand-sb7` (live) — adjacent on one line, and the word does not mean the same thing

Airey's chapter 2 is titled *"It's the stories we tell"* and tells the designer their job is to find
the story and tell it wisely (printed 8). The verbal overlap with a narrative-framework source is
obvious and **it is a false friend**. Airey means the *provenance* narrative behind a mark — the
Zia symbol's history, the seven-pointed star's origin, the oak leaf's association — used mainly as
**presentation rationale to a client**. He does not mean a customer-as-hero message structure, and
nothing in his book is about message architecture at all. Recording these as related would import a
resemblance that exists only in the English word "story", which — given that this copy is a
translation — is not even demonstrably his word.

### No cross-lane ontology relationships were written

The parallel lanes' term ids are not resolvable from here. An unresolvable reference is worse than
a missing observation, so none was created.
