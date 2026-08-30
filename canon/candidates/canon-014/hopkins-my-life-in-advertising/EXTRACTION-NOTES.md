# Extraction notes — Claude C. Hopkins, *My Life in Advertising* (Harper & Brothers, 1927)

**EXPERIMENTAL — NOT LIVE CANON.** Lane `hopkins-my-life-in-advertising`, run
`book-expansion-qa-v1`. Nothing in this directory has been reviewed, accepted or promoted, and
nothing here may be described as accepted Canon. Produced under `SCHEMA-CONTRACT.md` and
`SCHEMA-CONTRACT-ADDENDUM-LOCATORS.md` (Case 1 — PDF with a verified authored folio).

## Counts

| File | Objects |
|---|---|
| `source-knowledge.yaml` | **70** SourceKnowledge objects (`sk_mla_0001`–`sk_mla_0070`) |
| `source-concept-systems.yaml` | **5** SourceConceptSystems |
| `operational-bindings.yaml` | **15** OperationalBindings (5 production, 4 evaluation, 4 governance, 2 benchmark) |
| `ontology-mappings.yaml` | **40** terms, **22** relationships, **10** concepts |
| `qa-bank.yaml` | **80** Q&A items (`qa_mla_0001`–`qa_mla_0080`) |

`requires_application: true` — **32 of 80 = 0.400** (contract minimum 1/3 = 0.333). See
§"The application-ratio repair" for how it got there, because the number is the whole story of the
third pass.

Answer-type mix: mechanism 21 · application 19 · source_position 9 · comparison 8 ·
boundary_condition 7 · failure_diagnosis 7 · concept_definition 3 · repair 3 · tradeoff 2 ·
factual 1. Difficulty: 49 medium, 31 hard, **0 easy** — deliberate. An easy question about Hopkins
is a question a model answers from latent knowledge, because this is one of the most quoted
practitioners in advertising and his slogans circulate independently of his book.

Knowledge-type spread: persuasion 15 · testing_method 13 · advertising 11 · effectiveness 7 ·
concept_development 7 · copywriting 7 · creative_process 6 · brand_communication 6 ·
media_planning 4 · evaluation_diagnosis 3 · typography 1.

## Method, and the three passes

This lane was **interrupted twice by network failures and finished in three passes.** That is
recorded here because the file states in `qa-bank.yaml` are otherwise inexplicable, and because the
recovery procedure is the reason nothing was silently duplicated or renumbered.

1. **Pass 1** — read the whole book against the page-marked working text, chapter by chapter, and
   built `source-knowledge.yaml` (70 objects), `source-concept-systems.yaml`, and
   `operational-bindings.yaml`. Extraction was organised by mechanism rather than by narrative:
   Hopkins tells the same principle two or three times across different accounts, and taking the
   chapters in order would have produced near-duplicate objects. `intra_source_relations` were used
   to hold the restatements together instead.
2. **Pass 2** — built `ontology-mappings.yaml` and began `qa-bank.yaml`. This pass **died mid-write**
   on a large single write of the Q&A bank. The bank survived as a syntactically valid file with 56
   items and no truncation, which is why the repair was possible at all.
3. **Pass 3** (this one) — read the four completed files and the two contracts before touching
   anything, treated the existing 56 items as fixed, and appended 24 new application items in eight
   small writes rather than one large one. `EXTRACTION-NOTES.md` was written the same way. Two
   earlier attempts at this lane died on very large single writes, so **every write in pass 3 was
   deliberately kept small and the item count was re-parsed after each one.**

Nothing from passes 1 and 2 was rewritten. One `support` field on a new item was edited after a
spot-check (see §Self-check). No existing item was renumbered, relabelled, or reworded.

## Locators — Case 1, and the page span that is really the book

This source is **Case 1** under the locator addendum: a PDF with a verified authored folio. The
working text carries markers of the form `<<<PRINTED_PAGE n | PDF_PAGE m>>>` with a detected offset
of **printed = PDF − 14**, and every locator in every file in this directory cites the **printed**
number. `provenance.page_start` and `page_end` are printed numbers throughout. No `PDF page` phrasing
appears anywhere, because it would be wrong for this source.

**The authored span is printed pp. 1–206.** The text ends "THE END" on printed p. 206. Printed
pp. 207–210 are Harper & Brothers' own advertisements for other business books in their list. They
are typeset like the book, they are bound with the book, and they are inside the same PDF — which is
exactly what makes them a trap. **They are not Hopkins and nothing was extracted from them.** A
locator above 206 in this directory would be a validation failure, and there is none; the highest
page cited anywhere in the Q&A bank is 204.

Note the shape of this: unlike the pageless sources in this run, **this source really does have
authored pages.** The `false_page_affordance` audit pattern does **not** apply here — the folios are
real, printed on the pages, and agree with the marker offset everywhere the extraction checked. The
only affordance problem is the publisher tail, and the fix for that is a span bound, not a change of
citation style.

No page was found where the printed folio disagreed with the marker.

## The OCR hazard, and how it was handled

The local copy is an older Internet Archive scan and the working text warns about it in its own
header. Three distinct failure modes appeared:

1. **Running heads interleaved into body text.** `MY LIFE IN ADVERTISING` and the chapter title
   appear mid-paragraph on nearly every page, sometimes with the folio attached
   (`AUTOMOBILE ADVERTISING 119g`). Harmless once expected, but it breaks naive sentence splitting
   and it puts stray digits next to real prose — which is why the locator self-check extracts page
   numbers only from `p.`/`pp.` markers in the locator field rather than by scanning text for
   numbers.
2. **Display type is damaged.** Chapter openings are scrambled (`Chapter MY Eighteen GREAT MISTAKE`,
   `CriaupE C. Hopkins`, `vettising`), and so are headlines quoted inside the body — the most
   consequential instance being on printed p. 134, discussed below.
3. **Ordinary body text is mostly clean** but carries scattered character errors (`ad.-writer`
   rendered variously, `insiduous` for insidious, `stoty` for story, `Sarah Bernhardt` intact but
   `Bissell` occasionally not). Figures — the part that matters most here — were clean everywhere
   they were checked.

Handling, in order of strength:

- **Paraphrase throughout.** No long string is quoted anywhere in this directory. Short source
  terminology is quoted only where the exact term is the point (`No-Rim-Cut`, `All-Weather`,
  `We Will Buy`, `Try Our Rivals, Too`, `salesmanship-in-print`), and each of those was confirmed
  clean in the scan.
- **Every load-bearing figure was re-read on its page** before being used. The figures relied on in
  the Q&A bank — 18 cents per Liquozone inquiry, the $700 Benton Harbor test, 1,460,000 coupons and
  $146,000 redeemed, $175,000 total, 97 per cent distribution, $250 dealer minimum and ~30,000
  dealers, $1.25 per case, 25 cents versus $1.25 per inquiry, 85 cents / $2.50 / $14.20 / 42 cents
  per reply, $1.78 average sale, under $5,000 / $750 / $20,000 on a test campaign, 8-point and
  6-point type, $13,000 / $200,000 / $500,000 on Pepsodent — were each verified against the page.
  None was OCR-corrupted.
- **One string could not be recovered and is flagged in the bank itself.** On printed p. 134 Hopkins
  calls the headline `"We Will Buy"` much better than the free-sample headline he names beside it —
  an assertion, not a reported test result. `"We Will Buy"` is
  clean; the rejected headline is set in damaged display type and reads as
  `‘“‘1o-Cent Cake Prec-«` in both the working text and in a fresh `pdftotext` pass on the PDF, so
  the scan itself is the limit and not the extraction. The reading *ten-cent cake free* is what the
  surrounding argument requires — the whole passage contrasts buying the article for the reader
  against giving it away — but it is a **reconstruction**, and `qa_mla_0065` says so in its `support`
  field and paraphrases rather than quotes. This is the only place in the lane where a load-bearing
  string could not be confirmed character-for-character.

No SourceKnowledge object carries `extraction_uncertainty: ocr_degraded`, and that is a deliberate
judgement rather than an oversight: in every case where OCR damage touched a claim, the claim was
either re-read cleanly on the page or confirmed from a restatement elsewhere in the book. Where
neither was possible, the material was left out.

## Deliberately not extracted

The book is an autobiography that happens to contain a method. Most of it by page count is not the
method, and refusing it was the main editorial act of pass 1.

- **Biography and career narrative.** Chapter Three (*My Start in Business*, printed pp. 27–36) is
  pure biography and produced **zero** objects. Chapter Five (*Larger Fields*, printed pp. 50–62)
  produced no object of its own and appears only as a restatement locus on `sk_mla_0004`. Chapters
  One, Six, Eighteen and Nineteen produced between one and four objects each across their
  page counts. The mother, the Scotch ancestry, the Baptist upbringing and
  the lay-preaching, the health collapse in Paris, the yacht, the country place, the two marriages,
  the relationship with Lasker as a personal matter — all read, none extracted, except where a
  passage does double duty as a stated method (the childhood silver-polish demonstration at
  pp. 17–18; the Pinkerton book refused by the mayor at pp. 19–21; the Bissell conversation at
  p. 189 as the frame of Chapter Eighteen's argument).
- **Motivational prose.** Long stretches of "the road to success lies through ordinary people",
  "I abhor drones", exhortations to young men, and the general 1920s self-made-man register. It
  argues nothing that can be applied or falsified.
- **Campaign anecdote with no mechanism.** This is the largest and least obvious category. Hopkins
  narrates dozens of accounts. Many end in a claimed result with no statement of *why* the thing
  worked — the sales went up, the brand led its field, the campaign was a sensation. Where a story
  supplies only an outcome, it was left out; where it supplies an outcome **and** a stated mechanism,
  it became an object. That is why 64 of 70 objects carry `mechanism_given` and 69 of 70 have
  `mechanism.stated_by_source: true` — not because the book is unusually rigorous, but because
  mechanism was the admission criterion.
- **Self-assessment and reputation-management.** The passages weighing his own credit against the
  agency's, disclaiming personal credit, and rebutting the head of the agency's remark that they
  never succeeded for anybody who could not have succeeded without them (p. 136). Interesting as
  evidence about the narrator; not knowledge.
- **The publisher tail at printed pp. 207–210**, as above.
- **His accounts of other people's businesses** where the advertising is incidental — the incubator
  man, the friends he financed, the Curtis anecdote about ordering a bottle of Schlitz on a train
  (p. 82). Charming, no reusable principle. The Curtis anecdote in particular *looks* like evidence
  for the Schlitz campaign and is a single reader's reaction.

## Evidence origin — how this source actually knows things

This is the most important thing an extraction of Hopkins can get wrong, so it is stated in numbers.

**`empirical_within_source` is on 11 of the 70 objects (15.7%).** The other 59 are not empirical
within the source. For comparison, all 70 carry `practitioner_assertion` and all 70 carry
`explicitly_stated`; 47 carry `outcome_claimed`, 46 carry `anecdotal`, and only **3** carry
`controlled_comparison`.

**The gap between 70 practitioner assertions and 11 empirical objects is the finding.** Hopkins
claims measurement constantly. Chapter Seventeen opens by grounding his whole authority in
thirty-six years of traced advertising, campaigns on some hundreds of lines, and keyed-return
comparisons of thousands of pieces of copy, and he states a refusal rule — an untraced success is
not evidence about the advertising that accompanied it. He then, across 206 pages, **reports the
actual numbers about a dozen times.** The rest of the time the sentence has the grammar of a result
and the content of a recollection: "results were immediate and enormous", "it worked like magic",
"the campaign from the start was a sensational success", "I have multiplied results by eight or ten
by a simple change in headline" — with no line, no date, no volume and never the losing version.

The eleven that earned `empirical_within_source`, and why:

| Object | pp. | What is actually reported |
|---|---|---|
| `sk_mla_0013` | 92–95 | successive guaranty forms with the Liquozone conversion economics attached |
| `sk_mla_0020` | 92–94 | **the cleanest record in the book**: a dozen Illinois test cities, inquiries at 18 cents each, a stated waiting period, then the same measure reproduced at national scale |
| `sk_mla_0025` | 103–105 | 97% distribution in three weeks; 1,460,000 coupons; $146,000 redeemed; $175,000 total; payback inside nine months |
| `sk_mla_0039` | 135 | the repeat-purchase criterion with the Benton Harbor $700 test and repeat sales paying the advertising before the bills fell due |
| `sk_mla_0041` | 140–142 | wants collected by interviewing buyers by the hundreds, then figures commissioned against those wants |
| `sk_mla_0044` | 146–147 | free inquiries ≈25 cents against ≥$1.25 when ten cents is charged — a stated cost comparison, not an impression |
| `sk_mla_0045` | 149–150 | a reformulated product tried in a few towns on existing users and **rejected on the result**, against everyone's expectation |
| `sk_mla_0050` | 154 | the free-offer reversal: readership multiplied on food, results divided by four on a hygiene product |
| `sk_mla_0054` | 158–159 | 85c/$2.50 baseline, $14.20 per reply on the attractive advertisement, 42c on the plain one, held for years across 250,000 replies |
| `sk_mla_0056` | 197 | $1.78 average sale against 50c / 35c / 10c single-product categories |
| `sk_mla_0057` | 163–165 | ≈25c per inquiry and ≥35c per colour catalogue, with the resulting decision |

**Justification of the count.** The bar applied was: *the source states a quantity or a directional
comparison it says it obtained, on this page, such that the claim could have come out the other
way.* Everything below that bar was refused, including three tempting categories:

1. **"Countless tests have proved…"** — pp. 178 (coupons multiply returns), 181 (oversize type does
   not pay), 187 (keyed headline tests). These *describe* a method and assert its verdict without
   producing it. They earn `explicitly_stated` and `practitioner_assertion`; they do not earn
   `empirical_within_source`, and treating them as empirical would convert the book's rhetoric into
   its evidence.
2. **Large claimed outcomes.** Schlitz from fifth place to neck-and-neck with first in a very few
   months (p. 81), Palmolive to the world's leading toilet soap, $40,000 to nearly $2,000,000 on
   Goodyear (p. 127). These are business outcomes with no counterfactual and no attribution
   argument, and Hopkins's own refusal rule at pp. 175–176 disqualifies them.
3. **The book's own headline figures about itself** — thirty-six years, hundreds of lines, thousands
   of pieces of copy (pp. 175–177). This is a claim about a body of evidence, not the evidence.
   `sk_mla_0061` records it as the source's stated epistemology and `sk_mla_0062` records the refusal
   rule; neither is marked empirical, which is the correct and slightly uncomfortable outcome, since
   it means the book's foundational claim about its own rigour is itself unevidenced within the book.

Three objects carry `controlled_comparison`: `sk_mla_0045` (the two-minute oats tried on existing
users), `sk_mla_0050` (the same free device on two categories), `sk_mla_0054` (two advertisements for
the same article, cost per reply held over years). Even these are single-arm-at-a-time field
comparisons reported from memory a decade or more later, with no sample sizes and no intervals.

`source_uncertainty` breakdown: 63 `none`, 5 `source_hedges`, 1 `source_asks_open_question`
(art and colour, pp. 182–183 — the one place he says the question is open and he has no proof), 1
`source_concedes_difficulty`. **Hopkins hedges almost never**, and that near-absence of hedging is
itself recorded, because a downstream reader that treats confident phrasing as a confidence signal
will read this source catastrophically.

## The application-ratio repair

**The bank stood at 8 application items out of 56 = 14.3%, against a contract floor (§7 rule 3) of
one third. That is a hard failure and it was the primary reason for pass 3.**

**24 new items were added, `qa_mla_0057`–`qa_mla_0080`, all `requires_application: true`.** Final
state: **32 of 80 = 0.400.**

The repair was made by **writing new items, not by relabelling existing ones.** Relabelling was the
obvious shortcut and it would have been a lie: a recall question does not become an application
question because a boolean changed, and the resulting bank would have reported a ratio it did not
have. The eight original application items are untouched, as are the other 48.

Construction rules used for the 24:

- **Each is built on a SourceKnowledge object from this lane**, so every answer traces to a claim, a
  mechanism and a page range that already survived pass 1's admission criteria. The locator was then
  narrowed from the object's range to the page or pair of pages that actually carries the answer —
  e.g. `sk_mla_0008` spans pp. 41–44 and `qa_mla_0057` cites pp. 42–44, where the
  privilege-not-inducement formulation and the order figures sit.
- **Each puts a described situation first and requires the principle to be applied to it** — a
  manufacturer refusing to fund samples, a designer asking for large display type, a client with
  weak distribution and no salesforce, a team proposing a sequenced three-advertisement campaign.
  None is of the form "what did Hopkins say about X".
- **Each is answerable only from this source.** Several deliberately name the plausible modern
  default in the confounders and then have the answer contradict it: free-with-purchase drives trial
  (p. 146 says it is simply a price reduction and it failed), bigger type is more readable
  (pp. 181–182 argues from habituation and cost to the opposite), reach at low cost per thousand is
  efficient (pp. 145–146 measures against affordability instead), sequenced messaging (p. 183 denies
  the premise that anyone reads in series).
- **Spread across the book rather than mined from two chapters.** The 24 draw on thirteen of the
  nineteen chapters: Two (1), Four (2), Six (1), Seven (1), Nine (2), Ten (1), Eleven (2),
  Twelve (1), Thirteen (3), Fifteen (1), Sixteen (1), Seventeen (5), Eighteen (3). Chapter Seventeen
  takes five because it is the fourteen-page principle inventory and the densest material in the
  book.
- **Chapter Eighteen, *My Great Mistake*, was worked hard as instructed** — the richest failure
  account in the book. It now carries `qa_mla_0018`, `0029`, `0030` from pass 2 and `qa_mla_0064`
  (partly), `0076`, `0077`, `0078` from pass 3: the account-loss dynamic diagnosed as a structure
  rather than a misfortune; the auxiliaries economics with its unaudited self-reported figures; the
  never-sell-twice doctrine restated with the trade's demands attached; and the closing hedge in
  which Hopkins explicitly withdraws his own late-career move as advice to the majority.
- **No item modernises a claim.** Every one that touches a mechanism era-bound to redeemable paper
  coupons, independent grocers, general-circulation print without targeting, or publisher-paid agency
  commissions says so in the answer or in the confounders. Several confounders exist specifically to
  block a digital-media transfer that a model would otherwise make (`qa_mla_0061`, `qa_mla_0063`,
  `qa_mla_0067`, `qa_mla_0069`, `qa_mla_0072`).
- **Where the claim rests on assertion, the answer says so.** `qa_mla_0073` is the clearest case: it
  asks where the leverage is, gives Hopkins's eight-or-ten multiplication and 25-versus-50-per-cent
  contrast, and then states plainly that he supplies no campaign, no date, no volume and never the
  losing headline. `qa_mla_0066`, `qa_mla_0069`, `qa_mla_0070`, `qa_mla_0071`, `qa_mla_0079` and
  `qa_mla_0080` each carry the same correction.

Effect on the mix: `application` as an `answer_type` went from 1 to 19, and the diagnosis/application
share of the bank now sits close to the contract's ~20% target rather than far below it. Definitions
and facts remain slightly under target (4 of 80) — a deliberate choice, since a definitional question
about Hopkins is exactly the kind a model answers from circulating summary rather than from the book.

## Ethically dated material — recorded, never as guidance

Two categories, handled the same way: as source position and historical record, with
`culturally_bounded` and `historical_claim` on the objects and `source_position` on the Q&A items
that are about what this source holds.

- **Patent medicine.** Chapter Seven recounts the medicine campaigns that made his reputation, and
  it opens with Hopkins disowning the whole class: he no longer approves of medicine advertising,
  has not advertised one except for simple ailments in seventeen years or more, and would not under
  any circumstances. `sk_mla_0014` and `qa_mla_0015` record the repudiation as the frame. The
  mechanisms recovered from those chapters — the locally-signed guaranty, risk transfer, the free
  trial bottle — are extracted as mechanisms, with the product class named every time. None is
  presented as guidance, and Liquozone in particular is recorded as what it was.
- **1927 attitudes to women and class.** They are pervasive and they are load-bearing: the
  class/mass distinction that decides his media argument at pp. 145–146, "the girl who should
  economize" at pp. 173–174, the repeated framing of the housewife as the object of study, and the
  disclosure of one woman's credit record to another business at pp. 161–162 with no consent step
  anywhere in the account. Extracted where a mechanism sits inside them, with the framing named as
  the source's. `qa_mla_0075` states the absence of any consent consideration explicitly and calls it
  part of the historical record rather than a gap in the extraction.

## Observations for cross-source review (NOT promotions)

**Nothing in this section is a promotion, a merge, or a claim of agreement.** No `xs_` concept
exists anywhere in this directory, no `same_failure_family` relation is used, no binding carries
`cross_source_supported`, and no cross-lane ontology relationship was written (the sibling lanes'
term ids are not resolvable from here). These are notes for a human reviewer who will have the
authority this lane does not.

### 1. The `shared_author` dependence with live Canon — the binding one

`hopkins-scientific-advertising-ch1-7` is **accepted live Canon**. It is *Scientific Advertising*
(1923), chapters 1–7, by **the same author as this source**.

**These two are not independent origins, and agreement between them must never be counted as
cross-source convergence.** It is one man's position stated twice, four years and one career apart.
The dependence here is stronger than bibliography alone would suggest, and the book itself supplies
the proof:

- **Chapter Seventeen of this book is literally about that book.** It opens by naming *Scientific
  Advertising* as the work through which his name became attached to the phrase (printed p. 175),
  and then restates its doctrine in condensed form across pp. 175–188. Nine of the seventy
  SourceKnowledge objects here come from that chapter. An aggregator that treats them as a second
  witness to the live source is counting a summary of a document as corroboration of the document.
- **He was paid to write it, by the man who employed him for both.** Printed p. 170: Lasker gave him
  a $10,000 cheque for writing *Scientific Advertising*. Printed p. 169: he wrote numerous books to
  set down the agency's principles. Same author, same agency, same institutional programme, same
  commercial interest in the principles being true.
- **Load-bearing claims recur near-verbatim across the two works** — keyed returns as the basis of
  principle, salesmanship-in-print, definite figures over superlatives, service over selfishness,
  and mail order treated as the exact case.

Consequences a downstream reader is bound by: agreement between this source and
`hopkins-scientific-advertising-ch1-7` is **not** convergence and must not be counted, displayed or
aggregated as such; no `cross_source_concept` may be built from the pair; and independence is
**pairwise** — nothing here says this source is independent of any *other* corpus source, which is a
separate and unperformed determination. A formal audit record of the dependence is the Controller's
to write, not this lane's. The same statement appears in `PROVENANCE.md` §4.

### 2. The `hopkins-scientific-advertising-ch8-21` lane — observation only

A separate experimental lane in this run extracted *Scientific Advertising* chapters 8–21
(48 SourceKnowledge objects, printed pp. 25–64). **This lane did not coordinate with it, asserts no
agreement with it, and read it only after its own extraction was complete** — specifically to write
this section. Since that source is also Hopkins, and is in fact the same *volume* as the live ch1–7
source, the `shared_author` dependence applies to that pair **a fortiori**: any triangle drawn
between this book, ch1–7 and ch8–21 has one author and two books at its corners, not three sources.

Recurrences noticed, offered as leads for a reviewer and nothing more. In each case the two lanes
were written independently and arrived at the same doctrine because the same man wrote both books:

| This lane | ch8–21 lane | Note |
|---|---|---|
| `sk_mla_0030` every advertisement carries the whole case (p. 183) | `sk_sa8_0001` one reading decides | Same argument, same premise about serial reading |
| `sk_mla_0053` the headline is the selector (pp. 186–187) | `sk_sa8_0002`, `sk_sa8_0014` | Both derive the featured claim from reachable share |
| `sk_mla_0062` an untraced success is not evidence (pp. 175–176) | `sk_sa8_0004` evidence from anyone who does not know his returns is inadmissible | The refusal rule, stated in both books |
| `sk_mla_0044` charging for a trial multiplies acquisition cost (pp. 146–147) | `sk_sa8_0024` free multiplies readers, any charge costs more | **Worth a reviewer's attention:** the 1923 statement is unconditional; this 1927 book reports at p. 154 that the same device *divided results by four* on a hygiene product. That is the same author qualifying his own earlier claim, not two sources disagreeing, and it must be presented that way |
| `sk_mla_0025`, `sk_mla_0036` pre-announced coupon; naming stocking dealers | `sk_sa8_0030`, `sk_sa8_0031` | Two mechanisms for distribution without salesmen, in both books |
| `sk_mla_0045` a product change tested on existing users and reversed | `sk_sa8_0035` a decision everyone was certain of, reversed by a thousand-dollar test | **Probably the same episode told twice.** A reviewer should establish that before either is treated as a second instance |
| `sk_mla_0049` reward not prevention (pp. 152–153) | `sk_sa8_0013`, `sk_sa8_0042` | Same rule, and both add the never-picture-the-defect corollary |
| `sk_mla_0058` colour and expensive art unresolved (pp. 182–183) | `sk_sa8_0008` colour does not generally pay | The 1927 statement is the more cautious of the two — it records an open question |
| `sk_mla_0068` repeat frequency sets what may be spent (pp. 191–192) | `sk_sa8_0012` feasibility as lifetime revenue against acquisition cost | Same economics |
| `sk_mla_0016` be first to state the commonplace facts (pp. 79–82) | `sk_sa8_0022` a parity product must be given a seeming advantage | Same move; "seeming advantage" is his phrase in both |
| `sk_mla_0021` a cheap local test predicts the national market | `sk_sa8_0034` small-scale averages asserted always to hold at scale | **The load-bearing unexamined assumption of both books.** Neither supplies evidence for it |
| `sk_mla_0032` the name should carry the claim (pp. 125–126) | `sk_sa8_0046`, `sk_sa8_0047` | The ch8–21 lane has the fuller taxonomy of how a name fails |

One consolidation note, offered neutrally because it will matter mechanically and is nobody's error:
the two lanes serialise `source-knowledge.yaml` differently — this lane writes a **bare list** of
objects, the ch8–21 lane wraps its objects under a `source_knowledge:` key with a `source_id`
sibling. Both are valid YAML and both satisfy the contract's field requirements; a consolidator will
need to handle both shapes.

### 3. What is **not** claimed here

- No relationship to any non-Hopkins source in the run was assessed. The resemblances a reader might
  expect — Ries on differentiation, Godin on permission, Sullivan on craft — were not examined, and
  their absence from this file is not a finding about them.
- No claim that Hopkins is corroborated by anything. Within this directory he is corroborated by
  nothing, including himself.

## Where I was tempted to over-claim, and did not

1. **The application ratio itself.** The fastest repair available was to flip
   `requires_application` to `true` on eighteen existing recall items. Several of them *look* close —
   they describe a case and ask what Hopkins concluded. They are not application items: the reader
   recalls rather than applies, and the ratio would have been a fiction reported as a fact. Twenty-
   four new items were written instead, and the existing eight are still the only pass-2 application
   items.

2. **"He tested it" as "it is established."** This is the standing temptation with this source and
   it is strongest exactly where the material is most useful. `qa_mla_0073` asks where the leverage
   in a campaign is, and the honest answer includes that Hopkins gives an eight-or-ten multiplication
   from a headline change and never once gives the pair of headlines, the line, the date or the
   volume. Same for coupons multiplying returns (p. 178), oversize type not paying (p. 181), and
   thousands of tests proving the space-economy principle (p. 158). Each is written as a claim about
   what he asserts, and the withheld result is named. `empirical_within_source` stayed at 11.

3. **The Schlitz result.** Fifth place to neck-and-neck with first in a very few months is the most
   quotable outcome in the book and the one a corpus most wants. It is an unattributed business
   outcome with no counterfactual, and Hopkins's own refusal rule disqualifies it. `sk_mla_0016` and
   `qa_mla_0033` carry the *mechanism* — telling the untold commonplace facts — and treat the
   market-share movement as an outcome claimed rather than as evidence that the mechanism worked.

4. **Transposing a mechanism to digital media.** Almost every strong item here had an obvious modern
   restatement waiting: the pre-announced coupon as a launch-day promo code, the dealer-naming
   campaign as a store locator, the earned sample as a gated download, the headline test as an A/B
   test. Writing any of them would have been a claim about a medium Hopkins never saw. Where the
   parallel is close enough to be dangerous, the modern reading is written into the confounders as
   the wrong answer — `qa_mla_0061`, `qa_mla_0063`, `qa_mla_0067`, `qa_mla_0069`, `qa_mla_0072` all
   do this explicitly.

5. **The pre-testing method at p. 174.** He says he does not consult managers and boards and submits
   campaigns to the ordinary people around his country place. It reads like a research protocol and
   it is not one: it is a handful of neighbours and employees on his own property, chosen by him,
   with no count, no protocol and no recorded result. `qa_mla_0056` says so. It was tempting to
   build a second application item on it as though it were a method; it is a habit.

6. **Chapter Eighteen's title.** "My Great Mistake" reads like a failure post-mortem of a campaign
   and a corpus would like it to be one. It is not: the mistake is his 1887 decision to stay an
   employee. The genuine campaign-failure material in that chapter is the account-loss dynamic and
   the abandoned cosmetic line, and `qa_mla_0078` exists partly to block the misreading.

7. **A `cross_source_concept`, and cross-lane ontology relationships.** Both were live temptations
   given how closely the ch8–21 lane's objects track this book's. Both are forbidden here, and the
   agreement would have been worthless anyway — see the section above. Zero `xs_` identifiers, zero
   cross-lane relationships, and the observations live in prose where a human can weigh them.

8. **`empirically_supported` / `cross_source_supported` on bindings.** Eleven objects report real
   figures, which briefly looks like grounds for `empirically_supported`. It is forbidden in this
   task and would be wrong regardless: there is no Empirical Memory reference behind any of them, and
   a 1927 recollection of a 1911 test is not an empirical record. All 15 bindings are
   `derived_from_source` (12) or `extractor_inference` (3).

9. **Turning his physical-production advice into generative instructions.** The book is full of
   instructions about objects — build sweepers in twelve woods, print the pie card in twelve stone
   passes, put signs on both sides of the boxcars, set the coupon in 6-point. Five bindings carry
   `target_type: production` with `status: production_candidate` and `target_path: null`, recording
   the action in the source's own frame and leaving it unbound, exactly as §5 rule 1 requires.

## Self-check results

All checks were run as code against the written files, not by eye.

1. **`qa-bank.yaml` parses and the item count is correct.**
   `python3 -c "import yaml; d=yaml.safe_load(open('qa-bank.yaml')); print(len(d['qa_items']))"`
   → **80**. Re-run after every one of the eight appends.

2. **Every locator page is inside printed 1–206.** Checked mechanically, extracting only digit runs
   introduced by a `p.` / `pp.` marker (ranges and comma/and lists included), then range-testing each.
   Result: **80 of 80 items carry at least one page locator; every extracted page falls in 1–206;
   the cited range is 1–204; zero out-of-range, zero missing.** A stricter second pass then required
   every digit run *anywhere* in a locator to fall inside a `p.`/`pp.` group, to catch a page number
   written without its marker. One anomaly surfaced and is not one: `qa_mla_0010` contains the phrase
   "the 52-countries claim", where 52 is part of a claim description and not a page. No page number
   above 206 appears anywhere in the file.

3. **Application count and fraction, verified with code, not by eye.**
   **32 of 80 = 0.400.** Exact-fraction test `Fraction(32,80) >= Fraction(1,3)` → **True**. Before
   pass 3 it was **8 of 56 = 0.143**, a failure. **24 items added, all application.**

4. **Spot-checks against the cited pages.** **All 24 new items** were checked — more than the 15
   required — by asserting between three and seven distinct substrings per item against the exact
   printed pages named in that item's locator, in the page-marked working text. First run: 18 items
   clean, 6 items with one failing substring each. **All six were failures of my check strings, not
   of the items:** four were phrases split across a page boundary inside the cited range
   (`privilege, not an in-|ducement` across pp. 43–44; `good | at any store for a ten-cent can` across
   pp. 103–104; `15 per | cent` across pp. 171–172; `never tried to sell things without demonstra-`
   ending p. 17), and two were my own paraphrase drift in the check string (`gave` for `had given`;
   a doubled quote mark in `the ‘free’ offer cheapens a product`). Re-run against the full cited
   span: **24 of 24 pass, 0 misses.**
   **Substantive corrections required: zero.** One `support` field was nevertheless amended —
   `qa_mla_0065`, to record that the losing headline on printed p. 134 is OCR-damaged and that
   *ten-cent cake free* is a reconstruction rather than a reading. That is an added disclosure, not a
   correction of a wrong claim. The p. 134 damage was additionally confirmed against the PDF itself
   with `pdftotext -f 148 -l 148`, so it is the scan and not the working text.

5. **Identifiers and required fields.**
   - `qa_id`s unique: **yes** (80 distinct), and contiguous `qa_mla_0001`–`qa_mla_0080`.
   - Every `source_id` is `hopkins-my-life-in-advertising`: **yes**, 80 of 80.
   - No empty `answer`, `support`, `confounders`, `question`, `source_locator` or `source_title`:
     **zero empties**, 80 of 80. No `TODO` or placeholder text anywhere in the file.
   - Key set identical across all 80 items: **yes** — the twelve keys §7 specifies, no more and no
     fewer.
   - `answer_type`, `difficulty` and `knowledge_type` all drawn from their fixed vocabularies:
     **yes**, 80 of 80 on each.
   - `confounders` non-empty on every item, and every new item's confounder list names the plausible
     modern default as well as an adjacent Hopkins idea.

Not re-verified in pass 3, because the files were fixed on arrival and pass 3 had no authority to
change them: the internal schema conformance of `source-knowledge.yaml`,
`source-concept-systems.yaml`, `operational-bindings.yaml` and `ontology-mappings.yaml`. Their counts
and enum distributions were read for this file (and are reported above), and nothing anomalous
surfaced — 15 bindings all carrying `derived_from_source` or `extractor_inference`, no `xs_`
identifier, no `same_failure_family` relation, no cross-lane relationship — but that is an
observation, not a validation run.

## Write boundary

This pass wrote **only** inside
`canon/experimental/book-expansion-qa-v1/hopkins-my-life-in-advertising/`, and only two files:
`qa-bank.yaml` (appended) and `EXTRACTION-NOTES.md` (created). Nothing under
`canon/knowledge/current/**`, `canon/audit/**`, `coordination/**` or any SPEC file was created,
edited or deleted. Nothing was committed.
