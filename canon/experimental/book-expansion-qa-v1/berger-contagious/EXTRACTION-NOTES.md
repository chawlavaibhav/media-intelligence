# Extraction notes — Jonah Berger, *Contagious: Why Things Catch On*

**EXPERIMENTAL — NOT LIVE CANON.** `book-expansion-qa-v1`, non-merge, exploratory lane. Nothing here
is accepted Canon and nothing here may be described as accepted.

`source_id: berger-contagious` · ID prefix `ctg`

---

## 1. Method

The whole book was read: Introduction, chapters 1–6, Epilogue, both long author footnotes, and the
back-matter interview. The Notes section was read separately and **used only for attribution** —
it is the only place in the book that establishes, study by study, whose research each finding is,
and that distinction is what this lane was constituted to get right.

Order of work: read the binding contracts and the SPEC files; read the completed
`connor-irizarry-discussing-design` lane for shape and the live
`canon/knowledge/current/heath-made-to-stick-introduction` extraction for the neighbouring case;
read the book; build the own-versus-third-party ledger from the Notes **before** assigning any
evidence characteristic; then write.

Files were appended in chunks and re-parsed after every chunk. Earlier runs of this task died on
single large writes; nothing here was written in one call.

## 2. Locators — audit pattern `no_authored_page`

This is an EPUB. The supplied text file's own header states it: `FORMAT: EPUB (reflowable). THERE
ARE NO AUTHORED PAGE NUMBERS IN THIS FORMAT.`

- Every locator is **chapter plus named section**, with the spine document number carried as a
  secondary file-position aid. `Ch. 3 "Emotion", section "Exercise Makes People Share" (spine 8)`.
- `provenance.page_start` and `page_end` are `null` in all 54 SourceKnowledge objects and all 5
  SourceConceptSystems.
- **Audit pattern recorded: `no_authored_page`.** Per the addendum this is a property of the format,
  not a defect in the extraction, and it is unfixable in this copy.

**The page-number trap in this book, and how it was handled.** The Notes section is dense with page
numbers — `Journal of Marketing Research 49, no. 2, 192–205`, `Marketing Science 29, no. 5, 815–27`,
`Psychological Science 22, no. 7, 891–93`. Every one is a page range inside a **different work**.
None is a locator into *Contagious*. No number from the Notes appears as a locator anywhere in this
extraction. The book's body text contains no internal "see page N" cross-reference, so no
unresolvable internal reference had to be recorded.

`false_page_affordance` is **not** recorded: this file does not look like it has authored pages.

## 3. Section names used as locators

The book's own section headings, used verbatim. Introduction: *Why Do Products, Ideas, and Behaviors
Catch On?* · *Generating Word of Mouth* · *Are Some Things Just Born Word-of-Mouth Worthy?* ·
*Studying Social Influence* · *Six Principles of Contagiousness*, plus two author footnotes. Ch. 1:
*Minting a New Type of Currency* · *Inner Remarkability* · *Leverage Game Mechanics* (with *Building
a Good Game*) · *Make People Feel Like Insiders* · *A Brief Note on Motivation*, plus a footnote.
Ch. 2: *Buzzing for BzzAgent* · *Why Do People Buzz About Some Products More Than Others?* · *The
Difference Between Immediate and Ongoing Word of Mouth* · *From Mars Bars to Voting* · *Searching
for "Friday" on . . . Friday* · *Triggered to Talk* · *Kit Kat and Coffee: Growing the Habitat* ·
*What Makes for an Effective Trigger?* · *Consider the Context* · *Why Cheerios Gets More Word of
Mouth Than Disney World*. Ch. 3: *Most E-Mailed Lists and the Importance of Sharing* ·
*Systematically Analyzing the Most E-Mailed List* · *The Power of Awe* · *Does Any Emotion Boost
Sharing?* · *Kindling the Fire: The Science of Physiological Arousal* · *Focus on Feelings* ·
*Kindling the Fire with High-Arousal Emotions* · *Babywearing, Boycotts, and Blunting Bad Buzz* ·
*Exercise Makes People Share*. Ch. 4: *The Psychology of Imitation* · *The Power of Observability* ·
*Making the Private Public . . . with Moustaches* · *Advertising Itself: Sharing Hotmail with the
World* · *Livestrong Wristbands as Behavioral Residue* · *Anti-Drug Commercials?*, plus a footnote.
Ch. 5: *Saving a Couple of Bucks* · *The Psychology of Deals* · *Highlighting Incredible Value*
(with *The Rule of 100*) · *More Than Money* · *A Note on Truth*. Ch. 6: *Stories as Vessels* ·
*Learning Through Stories* · *Build a Trojan Horse* · *Making Virality Valuable*.

---

## 4. THE OWN-VERSUS-THIRD-PARTY LEDGER

This is the disciplinary core of the lane and it was built before any evidence field was written.
SPEC-03 defines `empirical_within_source` as "the source reports its own measurement" and has **no
characteristic for third-party research**, so `empirical_within_source` was applied only where the
measurement is Berger's, and every third-party study was recorded instead in a caveat marked
`extractor_observed`, **naming whose study it is**, with its design and figures.

### 4a. BERGER'S OWN — formal studies (14). These carry `empirical_within_source`.

| # | Study | Reported result | Where |
|---|---|---|---|
| 1 | Berger & Iyengar, 6,500 products and brands scored for remarkability against discussion frequency | remarkable brands discussed almost twice as often | `sk_ctg_0011` |
| 2 | Berger & Schwartz, several hundred BzzAgent campaigns, interest/novelty/surprise against word of mouth | **no relationship** overall; interest predicts immediate, not ongoing | `sk_ctg_0018` |
| 3 | Berger & Schwartz, same data, trigger frequency | +15%, and on **both** immediate and ongoing | `sk_ctg_0019` |
| 4 | Berger & Schwartz with BzzAgent, Boston Market habitat experiment, six weeks, dinner-pairing vs generic message | +20% word of mouth **among a subgroup** | `sk_ctg_0023` |
| 5 | Berger & Fitzsimons, dining-hall tray slogan experiment, two-week food diary | tray slogan rated <half as attractive, self-predicted to fail, +25% fruit and vegetable intake | `sk_ctg_0021` |
| 6 | Berger & Fitzsimons, Halloween orange-product accessibility | thoughts of orange products far higher the day before than a week after | `sk_ctg_0026` |
| 7 | Berger, Meredith & Wheeler, every Arizona polling place, 2000 general election | >10,000 more votes for school funding at school polling places; survives controls and a matched comparison | `sk_ctg_0022` |
| 8 | Berger, Sorensen & Rasmussen, hundreds of NYT book reviews | negative reviews hurt known books; **+45%** for new or unknown authors | `sk_ctg_0027` |
| 9 | Berger & Milkman, ~7,000 NYT articles over six months, web crawler | interesting +25%, useful +30%, awe +30%, sad −16%, positive +13%, anger and anxiety up (no figure) | `sk_ctg_0029`, `sk_ctg_0030` |
| 10 | Berger & Milkman, arousal manipulation — same story made angrier | more sharing (no figure) | `sk_ctg_0031` |
| 11 | Berger & Milkman, arousal manipulation — same ad made funnier | more sharing (no figure) | `sk_ctg_0031` |
| 12 | Berger, jogging vs sitting for 60 seconds, then an unrelated article | 75% of joggers shared, >2× the relaxed group | `sk_ctg_0032` |
| 13 | McShane, Bradlow & Berger, 1.5 million car sales | ~1 in 8 cars attributable to social influence; effect larger where cars are more visible | `sk_ctg_0036` |
| 14 | Berger's administration of two Thaler-derived scenario pairs, 100 people per cell | grill 75% vs 22%; clock radio/television 17% vs 87% | `sk_ctg_0042`, `sk_ctg_0043` |

Also his own, cited only in the Notes and never described in the body text: **Akpinar & Berger,
'Valuable Virality'** (Wharton working paper), which underlies chapter 6's central claim. It is
recorded in a caveat on `sk_ctg_0052` and carries **no** evidence characteristic, because the book
reports its conclusion without any design.

### 4b. BERGER'S OWN — informal demonstrations (3). These also carry `empirical_within_source`, and each carries an `extractor_observed` caveat saying it is informal.

| Demonstration | Reported | Where |
|---|---|---|
| Classroom poll on the share of word of mouth that is online | audiences average ~50% against a claimed 7% | `sk_ctg_0001` |
| The minivan / Mohawk identity-inference game, "hundreds of people" | 100% said the minivan driver had children; almost all named soccer | `sk_ctg_0009` |
| Annual split-question MBA cohort exercise, anonymous and blinded | <20% pre-programme wanted banking or consulting; >2/3 do a year in | `sk_ctg_0035` |

They **are** his own reported measurements, so applying the characteristic is factually correct.
None is a study: no control, no sampling frame, no dispersion, and the MBA exercise is recall-based
on one side. **This is the boundary at which the extraction was most at risk of over-claiming, and
it is flagged rather than smoothed.** A reviewer who wanted a stricter rule could drop these three,
leaving 16 objects carrying `empirical_within_source`.

### 4c. THIRD-PARTY STUDIES — recorded in `extractor_observed` caveats, naming the researcher. **None contributes any evidence characteristic.** (21)

Keller Fay Group, the 7% online figure · Tamir & Mitchell (2012, PNAS), self-disclosure reward and
the 25% pay cut · Dunbar, Marriott & Duncan (1997), the 40% conversation figure · Naaman, Boase &
Lai (2010), self-focused tweets · a University of Illinois group, the cockroach retelling
experiment · an unnamed Harvard $50,000/$100,000 relative-income study (Berger cites no source at
all for this one) · North, Hargreaves & McKendrick (1997, Nature), French/German supermarket music
and wine · Cialdini et al. (2005), the poison-parasite strategy · Cialdini et al. (2006), the
Petrified Forest sign comparison · Cialdini (2001), the Michelob slogan history and the term "social
proof" · Keltner & Haidt, the definition of awe · Pennebaker's textual analysis program (an
instrument, not a study) · Juanjuan Zhang (2010, Marketing Science), the kidney list · Hornik et al.
(2008, AJPH), the anti-drug campaign evaluation · Schroeder & Prentice (1998), pluralistic ignorance
and campus drinking · Sam Gosling, the term "behavioural residue" · Anderson & Simester (2001,
Marketing Science), the catalogue sale-sign experiment · Inman, Peter & Raghubir (1997), quantity
limits · Schindler (1998), restricted access · Chen, Monroe & Lou (1998), the discount-framing
finding behind the "Rule of 100" · Kahneman & Tversky and Thaler, prospect theory and the scenarios
· Allport & Postman (1947), the rumour transmission chains · Bakshy et al. (2011) and Watts & Dodds
(2007), the influentials evidence · Goel, Watts & Goldstein (2012), diffusion chain length · Duncan
Watts, the forest-fire comparison · Baumeister, Zhang & Vohs (2004) and Kardes (1993), narrative and
counterargument · Godes & Mayzlin, Chevalier & Mayzlin, Trusov et al., Bughin et al., the
word-of-mouth effectiveness figures.

### 4d. The counts, both reported as required

- **Measured by Berger himself: 14 formal studies + 3 informal demonstrations = 17.**
- **Measured by someone else and reported by Berger: 21 distinct studies or instruments** (more if
  the Introduction's compressed effectiveness citations are counted individually).

So roughly **45% of the identifiable measurement in this book is Berger's own**. That is
extraordinary for this corpus and it is why the live `heath-made-to-stick-introduction` note — that
its source "reports measurement constantly, almost none of it their own" — does **not** apply here.
The hazard in this book runs the other way: because so much genuinely is his, it is easy to assume
all of it is, and several of the most quotable figures in the book (the 7% online figure, the sale
sign result, the anti-drug backfire, the Rule of 100, the 70% rumour decay) belong to other people.

## 5. Separating what was measured from what was asserted

`empirical_within_source`: **19 objects**. `controlled_comparison`: **13 objects** — of which 9 are
Berger's own manipulated designs and 4 describe genuine minimal pairs run by others (the cockroach
study, the Petrified Forest signs, the catalogue experiment, the rumour chains). `anecdotal`: **21
objects**. `outcome_claimed`: **10 objects** — the recounted business cases. `historical_claim`: 14.
`culturally_bounded`: 6. `source_hedges`: 6 objects. `source_concedes_difficulty`: 1.

**A vivid opening story never inherits the evidential weight of the study that follows it.** Each
chapter opens with a business narrative — a secret bar, a theme park, a blender, a wristband, a
corn-shucking video, a Trojan Horse — and in every case the narrative object carries `anecdotal`
and, where a figure is reported, `outcome_claimed`, while the study object beside it carries
`empirical_within_source`. `sk_ctg_0005` (the blender) and `sk_ctg_0018` (the BzzAgent null) are the
clearest instance of the pair.

194 caveats were written, 180 of them `extractor_observed`. That ratio is itself the finding: this
book states more confidently than its underlying designs support, and almost every correction is
ours rather than the author's.

## 6. Hazards handled

**Popular-science compression.** Recorded per object rather than generally. Where Berger hedges, the
object carries `source_uncertainty: source_hedges` — six do, including his own definition of "viral"
(`sk_ctg_0006`), the influentials refutation whose endnote is far weaker than its body text
(`sk_ctg_0003`), the narrow-audience claim which has no evidence at all (`sk_ctg_0048`), and the
advertising-placement speculation which he states entirely in "should" and "may" (`sk_ctg_0032`).
Where he does not hedge but the claim rests on a single study, or on correlational field data
narrated as though causal, that is said in an `extractor_observed` caveat — as on `sk_ctg_0011`,
`sk_ctg_0022`, `sk_ctg_0032`, `sk_ctg_0036` and `sk_ctg_0052`. **His confidence has not been
imported.**

**Replication status is NOT VERIFIED and is out of scope.** Nothing here asserts whether any finding
has since held up. Several cited works were 2011–2012 working papers at the time of writing; that is
recorded as a fact about the source, not as a judgement.

**Period-bounding.** 14 objects carry `historical_claim` and 6 `culturally_bounded`. The platform
environment (Foursquare mayorships, Rue La La, the pre-algorithmic Twitter timeline, the *New York
Times* Most E-Mailed list as a scarce ranking surface) and the examples (minivans, soccer moms, the
McRib, American campus drinking) are of their period and place.

**Nothing translated into model instructions.** No `creative_ir` binding and no `production`
binding. The two remedies whose only executor is `physical_production` — self-advertising product
design and behavioural residue — are recorded in the source's frame and **left unbound**, per
SCHEMA-CONTRACT §5.1 and SPEC-05 rule 6. No remedy anywhere carries `generative_respecification`.
No inference about model capability appears in any file.

**`figure_semantic_binding_lost` is NOT recorded.** The book contains two charts, of daily searches
for a song and of daily mentions of a cereal, but in both cases the text states the pattern in words
— weekly spikes on Fridays; a rise from 5 a.m., a peak between 7.30 and 8, a fall by 11, shifting
later at weekends — so no meaning is carried by a figure alone. No object claims `visually_demonstrated`.

## 7. Mandatory self-check — results

1. **Every YAML parses.** All five YAML files load under `yaml.safe_load`. Re-verified after every
   append. ✅

2. **Page assertion, mechanical, over the whole lane rather than a spot-check.** 119 objects
   inspected — all 54 SourceKnowledge, all 5 SourceConceptSystems, all 60 Q&A items, which is more
   than the required 20. Assertions: every `page_start` is `null`; every `page_end` is `null`; no
   `provenance.locator`, `provenance.chapter`, `provenance.section` or `qa.source_locator` matches
   `\bpp?\.\s*\d`. A second scan looked for any non-null `page_start:` / `page_end:` line in the raw
   text of both files. **Failures: 0. Nothing had to be fixed.** ✅

3. **`empirical_within_source` count and verification: 19 objects.** Each was checked back against
   the ledger in §4 and against the book's own attribution. 16 rest on formal studies Berger
   conducted or co-authored; 3 rest on informal demonstrations he ran himself
   (`sk_ctg_0001`, `sk_ctg_0009`, `sk_ctg_0035`), each carrying an explicit caveat saying so.
   **No object carrying this characteristic rests on someone else's study.** The book's most
   quotable third-party findings — the 7% online figure, Tamir and Mitchell's reward study, the
   Zhang kidney result, Hornik's anti-drug evaluation, the Anderson and Simester sale-sign
   experiment, the Cialdini park signs, the Rule of 100, Allport and Postman's 70% — appear only in
   `extractor_observed` caveats and contribute nothing to any evidence field. ✅

4. **Application fraction, computed in code: 23 of 60 = 0.3833.** Threshold 1/3 = 0.3333. **Pass.**
   ✅

5. Additional checks run: no `informs` field; no Creative IR path; no product vocabulary; every
   evidence characteristic from the fixed list; every intra-source relation from the fixed list;
   every `source_interpretation` has a basis (there are none — all 54 objects are
   `explicit_source_claim`); every `mechanism.stated_by_source` present; every binding's refs
   resolve inside the lane; every `evaluation` binding has an `observation_unit`; every `governance`
   binding has a permitted `governance_consumer`; no `xs_` identifier; no `same_failure_family`; no
   `cross_source_supported` or `empirically_supported`; no `canonical_concept`; every Q&A item has
   all twelve required fields and a non-empty confounder list. **All pass.** The lane validator
   `validate_experimental.py` reports no error against this directory.

## 8. Observation-unit findings — the honest answer, and it is not uniform

The task asked whether `asset_set_over_time` is the honest unit and where a single asset cannot
carry the property at all. The answer split three ways, and the split is worth more than either
extreme would have been.

**A single asset genuinely CANNOT carry the property (2 bindings, `asset_set_over_time`).**
`bnd_ctg_004` is the clearest case in the lane: **trigger value is not in the artefact at all.** It
is a property of the relationship between the artefact and the environment its audience inhabits —
how often the cue occurs there, what else that cue means to those people, whether it fires where
they can act. No review of an asset can establish any of it, because none of the information is in
the asset. That binding is therefore written to do one thing only: record which cue the artefact is
betting on, so the bet is visible and checkable later. `bnd_ctg_002` is the same shape for a
different reason — the immediate/ongoing distinction only exists across time, and a single-window
measurement will produce a **confident wrong answer** rather than a noisy one.

**A single asset genuinely CAN carry the property (4 bindings, `whole_asset`).** Three real
exceptions. Whether the sponsor is detachable from the narrative (`bnd_ctg_001`) is an internal
structural property, checkable by one reader with no audience data — the retell test. Which emotion
an artefact evokes (`bnd_ctg_003`) is a property of the artefact, though **whether it will be shared
is emphatically not**, and that binding states its own ceiling. Whether an artefact depicts use, and
whether useful content is visible and bounded (`bnd_ctg_005`, `bnd_ctg_006`), are likewise
inspectable.

**Not an evaluation question at all (8 bindings).** Four `benchmark` bindings, which is where this
source fits best — his drivers generate minimal pairs cheaply and with a predicted direction, and
they diagnose the **judge** rather than the content. Four `governance` bindings, carrying the rules
this source is unusually good at supplying: examine failures alongside successes; do not treat a
named framework as a conjunction; prefer the extraction over the received summary when they
conflict; never reduce a behaviour by reporting its prevalence.

## 9. What was deliberately NOT extracted

- **Extended narrative case studies whose mechanism is stated elsewhere.** The Barclay Prime
  cheesesteak, the Blendtec origin story, the Please Don't Tell phone booth, the Rue La La
  turnaround, the Kit Kat revival, the Movember founding, the Livestrong decision, the Vietnamese
  nail salons, the Susan Boyle audition, the Ken Craig corn video. Each survives only as an
  `examples.positive` entry on the object stating its mechanism. None was given an object.
- **Chapter summaries and the Epilogue recap**, which restate the chapters in slogans. The one
  exception is where the Epilogue's summary language **contradicts** the Introduction footnote; that
  contradiction is recorded on `sk_ctg_0007` and as a `conflicts` entry inside `scs_ctg_001`.
- **Motivational framing** — "anyone can use it", "regular people with regular products", "the best
  part of the STEPPS framework".
- **Biography** — the author's childhood logic puzzles, his graduate-school cubicle, his fantasy
  football league except where the argument depends on it, his hiking trip, his own stock-picking.
- **The Readers Group Guide discussion questions and the Index.**
- The "poison parasite" technique, folded into `sk_ctg_0023` as an example rather than given its own
  object, because its mechanism is habitat growth applied to a rival's cue.

## 10. Tensions inside the book that were recorded rather than resolved

Four, all recorded as `contradicts` or `conflicts` relations or as caveats, none smoothed over.

1. **Remarkability against the interest null.** `sk_ctg_0011` reports remarkable brands discussed
   almost twice as often; `sk_ctg_0018` reports interest, novelty and surprise showing **no**
   relationship with word of mouth. Both are Berger's own. He never places them side by side, and
   his later resolution concerns *interest* rather than *remarkability*.
2. **Stories grow against stories shrink.** `sk_ctg_0012` has retelling amplify the remarkable;
   `sk_ctg_0054` has transmission chains lose ~70% of detail. Compatible in principle, unreconciled
   in the book.
3. **Make the private public against make the public private.** `sk_ctg_0037` and `sk_ctg_0040`
   give opposite instructions in one chapter, and the variable that selects between them — whether
   the true norm favours the desired behaviour — is visible in his two cases and never stated.
4. **The framework's own logical form.** The Introduction footnote says the six are relatively
   independent and not all required; the Epilogue says there is a recipe and that following the six
   will make any product contagious. The footnote is taken as the source's position and the summary
   recorded as him overstating himself.

## 11. Where the extraction was tempted to over-claim and did not

- **The three informal demonstrations.** Applying `empirical_within_source` to a classroom poll is
  defensible and could read as inflation. It was applied, because they *are* his own reported
  measurements, and each carries a caveat naming the informality — with the stricter alternative
  count (16) stated in §4b so a reviewer can adopt it.
- **`sk_ctg_0011` and `sk_ctg_0036`** are correlational and observational and are narrated causally
  by the source. The causal reading was **not** adopted; both carry caveats saying nothing was
  manipulated.
- **`sk_ctg_0022`, the polling-place study**, is the most impressive result in the book and it is
  observational — assignment was administrative, not researcher-controlled. The matched near-school
  comparison is recorded as a real design strength and explicitly **not** as random assignment.
- **`sk_ctg_0023`, the Boston Market experiment.** The +20% is a subgroup result. It would have been
  easy to record it as a general effect, as the book's phrasing invites; it is recorded as
  conditional.
- **`sk_ctg_0048`, narrow relevance.** No evidence of any kind supports this, and it is one of the
  book's most repeated ideas outside the book. It was kept — the mechanism is real content — and
  marked `source_hedges` with a caveat saying plainly that no study, citation or note supports it.
- **`sk_ctg_0052`, valuable virality.** The 50 million views and the ~25% sales fall are two facts
  placed side by side by the author. The causal implication was **not** recorded; the caveat says a
  year of falling sales has many possible causes.
- **The arousal-to-advertising-placement extension.** Berger's own text uses "should" and "may"
  throughout and reports no media test. The hedge is preserved in `sk_ctg_0032` and repeated in the
  Q&A item's confounders, rather than converted into a media-planning recommendation.
- **The Rule of 100.** The hundred-dollar threshold is arithmetic, not psychology. That observation
  is ours and is marked `extractor_observed`; it is not attributed to the source, who states the
  rule without qualification.
- **A tempting cross-source claim was declined.** The resemblance between this source's
  `remarkability` and the live Heath extraction's `unexpectedness` is close enough to invite a
  `potentially_equivalent_to`. They are not the same claim — Berger's runs through the *teller's*
  self-presentation and Heath's through *holding attention* — and no cross-lane relationship was
  written in any case, because the Heath term ids are not resolvable from here. It lives as prose in
  `PROVENANCE.md` §6 as an observation for review, not as a promotion.

## 12. Output

54 SourceKnowledge · 5 SourceConceptSystems · 14 OperationalBindings (6 evaluation, 4 benchmark,
4 governance; 0 creative_ir, 0 production) · 66 ontology terms (22 problems, 23 remedies, 17
properties, 4 entities), 15 relationships including 6 `distinct_from`, 7 source-specific concepts ·
60 Q&A pairs, 23 of them `requires_application: true` (38.3%).

All seven required files are present. No file outside
`canon/experimental/book-expansion-qa-v1/berger-contagious/` was created, edited or deleted, and
nothing was committed.
