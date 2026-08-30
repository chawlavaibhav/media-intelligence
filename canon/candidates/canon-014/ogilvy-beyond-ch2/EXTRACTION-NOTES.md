# EXTRACTION NOTES — `ogilvy-beyond-ch2`

**EXPERIMENTAL — NOT LIVE CANON.** Lane of the non-merge run `book-expansion-qa-v1`. Nothing here
is accepted Canon and nothing here may be described as accepted.

Source: David Ogilvy, *Ogilvy on Advertising* (1983), **the chapters beyond chapter 2**. Chapter 2
is already live Canon as `ogilvy-ch2-advertising-that-sells` and was not re-extracted. See
`PROVENANCE.md` for the scope-extension declaration, the chapter-by-chapter coverage statement and
the licence position.

---

## 1. Counts

| | |
|---|---|
| SourceKnowledge objects | **70** (`sk_ogx_0001`–`sk_ogx_0070`) |
| SourceConceptSystems | **3** |
| OperationalBindings | **15** |
| Ontology terms | **68** (28 problem, 24 remedy, 16 property) |
| Ontology relationships | **15** (10 within-lane, 5 cross-lane observations) |
| Ontology concepts | **5** (2 source-specific, 3 canonical) |
| Q&A items | **76** |
| Q&A `requires_application: true` | **27 — 35.5 %** |

All five YAML files parse under `yaml.safe_load`. All intra-source relation targets resolve. All
binding `source_knowledge_refs`, `source_system_refs` and ontology refs resolve inside this lane.

---

## 2. Method

1. Read `SCHEMA-CONTRACT.md`, the locator addendum, SPEC-03/04/05, and the completed
   `sullivan-hey-whipple` lane as the format target.
2. Read the **live** `ogilvy-ch2-advertising-that-sells/source-knowledge.yaml` in full — all 22
   objects — and its audit record `aud_ogilvy_ch2`, before touching the source text. This is the
   only way to avoid re-extracting a live span.
3. Established the chapter list **from the book's own contents page**, not from assumption: 20
   chapters plus front and back matter. Confirmed against the spine markers, which map
   `epub_c01_r1` through `epub_c20_r1` to spines 7 through 26.
4. Read the priority chapters in full: 7 (print), 8 (television), 12 (direct mail and direct
   response), 15 (research), then 9, 10, 11, 13, 14, 16, 17, 19, 20, and 1.
5. Read chapters 3, 4, 5 and 18 selectively, targeting reasoning about the work rather than
   business-of-agency material; read chapter 6 in full and extracted nothing from it.
6. Wrote `source-knowledge.yaml` incrementally in six appends of 12, 12, 6, 7, 6, 8, 9 and 5
   objects, parsing the file after each. The Q&A bank was written in four appends of 15, 15, 19 and
   6 items, parsing after each. **No single large write was attempted** — earlier lanes in this run
   died on them.

---

## 3. Hazard 1 — outcome claims without controls, and the sharper pattern behind them

This is the known signature of this source and it recurred exactly as expected. **Reported split:**

| Characteristic | Objects | Share of 70 |
|---|---|---|
| `outcome_claimed` | **14** | 20 % |
| `empirical_within_source` | **30** | 43 % |
| both on the same object | 3 | — |
| `controlled_comparison` | 4 | 6 % |
| `practitioner_assertion` | 70 | 100 % |
| `mechanism_given` | 52 | 74 % |
| `mechanism_absent` | 18 | 26 % |

**The 43 % figure is the finding, and it is a real difference from chapter 2.** The live chapter-2
extraction carries 4 `empirical_within_source` out of 22 (18 %) and 5 `outcome_claimed` (23 %).
The later chapters are far more numeric, because chapter 2 is doctrine and the later chapters are
craft built on commissioned readership research. Chapter 7 opens by naming its evidence base —
factor analyses from Gallup and Robinson, the Starch Readership Service, direct-response test
results and the author's own observation — and then gives numbers. That does not make the numbers
good; it makes them *reported results* rather than *asserted authority*, which is the distinction
`empirical_within_source` is for.

### Justification for every `empirical_within_source`

The test applied throughout: **the source reports a measurement AND states what it returned.** A
result stated only as a direction still counts; a measurement invoked with no result does not.

| Object | The measurement and its supplied result |
|---|---|
| `sk_ogx_0004` | five times as many read the headline as the body copy; eighty per cent never read body copy |
| `sk_ogx_0005` | helpful information read by seventy-five per cent more people |
| `sk_ogx_0006` | advertisements with news recalled by twenty-two per cent more people |
| `sk_ogx_0008` | Starch: headlines over ten words get less readership; retail study: ten-word headlines sell more — two results, opposite directions |
| `sk_ogx_0010` | quotation marks raise recall twenty-eight per cent; blind headlines twenty per cent below average |
| `sk_ogx_0013` | Gallup, seventy campaigns with known sales results, no before-and-after campaign failed to increase sales |
| `sk_ogx_0014` | Come to Britain readership tripled after photographs replaced drawings |
| `sk_ogx_0018` | average magazine body-copy readership about five per cent |
| `sk_ogx_0025` | drop-initial +13 %; leading between paragraphs +12 % |
| `sk_ogx_0026` | six times as many read the average article as the average advertisement; four times as many read captions as body copy; fewer than one reader in twenty reads an advertisement |
| `sk_ogx_0027` | Starch: spreads average +28 % rating; financial advertisers +150 % |
| `sk_ogx_0028` | a charity that switched from reverse to black on white raised twice as much money; forty-seven reverse-set advertisements counted in one issue |
| `sk_ogx_0029` | headlines below the illustration read by ten per cent more people; fifty-nine per cent of magazine advertisements place them above |
| `sk_ogx_0030` | subway exposure twenty-one minutes; fifteen per cent of riders carry anything to read |
| `sk_ogx_0031` | people who register a brand-preference change buy three times more |
| `sk_ogx_0035` | agency studies found competitor-naming commercials less believable and more confusing — a direction supplied |
| `sk_ogx_0038` | fabric-softener pair: cartoon no effect on the trend, live action reversed it |
| `sk_ogx_0042` | two commercials identical but for voice-over, on-camera sold more; background music neither positive nor negative |
| `sk_ogx_0043` | Jacoby 1979: all twenty-five commercials miscomprehended, 19–40 % of viewers |
| `sk_ogx_0044` | Northwestern, 731 corporations, corporate advertising +2 % on share price |
| `sk_ogx_0046` | research found the software buyer's criteria were responsiveness, support, service and product, not size |
| `sk_ogx_0047` | copy over 350 words attracts more readers; body copy read by ~10 %; four-colour costs a third more and attracts twice the readers; captions read by twice as many |
| `sk_ogx_0048` | cost per salesman's call, letter, telephone call, advertisement contact; four buying influences; sixty per cent of specifiers; advertising twice as effective as an article in the same journal |
| `sk_ogx_0051` | three subscription terms tested, cheapest returned thirty-five per cent more net revenue at a forty per cent lower price; partial coin offer outsold the complete-collection offer |
| `sk_ogx_0057` | Norwegian campaign readership highest ever recorded; more than seventy per cent of parents read the second wave |
| `sk_ogx_0060` | Starch: benefit headlines read by four times more people |
| `sk_ogx_0063` | tracked attitude series improved, flattened, resumed after the change — direction supplied at each stage |
| `sk_ogx_0064` | same product in glass and cans, majority preferred glass; identical cheeses at two prices, dearer sold faster |
| `sk_ogx_0066` | repertory of four or five brands; almost never admitted after year one; users ignore advertising for brands they do not use |
| `sk_ogx_0067` | Reisz, 679 food brands, correlation between quality and price almost zero |

Three of these (`0014`, `0057`, `0063`) carry `outcome_claimed` **as well**, because the same
passage reports a measured readership figure and an unmeasured sales or behaviour outcome in one
breath. Both characteristics are on the object and the caveats separate them explicitly. That
splitting is the honest treatment and it is the single most common shape in this book: *readership
measured, effect attributed.*

### "Measurement asserted, result withheld"

The brief asked for this to be recorded precisely, and it is a **distinct** state from
`outcome_claimed` — the latter claims a result without controls, this one claims a measurement
without a result. Five clear instances, each recorded in the object's caveats in those words:

| Object | What is claimed, and what is missing |
|---|---|
| `sk_ogx_0023` | "In split-run tests, long copy invariably outsells short copy." No test, margin, product or source. **This is the load-bearing evidence for his entire long-copy position** — the nine listed successes are single-arm outcomes that cannot isolate copy length. |
| `sk_ogx_0032` | "the latest wave of factor-analysis reveals that humor can now sell." No result, sample or date, for a reversal of a position he had held for decades. |
| `sk_ogx_0039` | "Research has demonstrated that a shocking percentage of viewers … forget the name of your product." The percentage is never given. |
| `sk_ogx_0020` | Gallup "has found" that analogies are widely misunderstood. No study, sample or rate. |
| `sk_ogx_0009` | Gallup's "Brag and Boast" finding: no study, date or result. |

An `evidence_interpretation` governance binding (`bnd_ogx_012`) records the pattern, and an
ontology term (`t_ogx_0068`) names it. **No change to SPEC-03's fixed vocabulary is proposed** —
the lane records the pattern rather than trying to extend the enum.

### The book's own criticism of this fault, applied to a predecessor

`sk_ogx_0069` records Ogilvy quoting, approvingly, a criticism of Claude Hopkins: that he did not
always indicate "the boundaries between direct findings from experimentation and conclusions
arrived at by general observation and reasoning." That is exactly the fault of chapters 7 and 8,
where measured figures, withheld results and taste-based rules sit in the same numbered lists in
the same voice. He records it in a predecessor and does not apply it to himself. `qa_ogx_0065`
tests it.

---

## 4. Hazard 2 — `historical_claim` is pervasive and load-bearing

**27 of 70 objects (39 %) carry `historical_claim`.** This is 1983 describing print, television,
radio and direct mail of that era, and in many objects the media condition is not context around the
claim — it *is* the mechanism.

Cases where the 1983 media condition is the stated reason the rule holds:

- `sk_ogx_0011` — the headline must telegraph because it competes with **350 others** on a
  newspaper page.
- `sk_ogx_0030` — the subway card may carry long copy because the rider has **21 minutes** and
  **85 per cent carry nothing else to read**.
- `sk_ogx_0040` — the first frame decides, in **30 seconds**, inside **30,000 commercials a year**.
- `sk_ogx_0026` — editorial graphics outdraw advertising graphics because readers had been trained
  by the news magazines of that period to classify a page by its conventions.
- `sk_ogx_0028` — legibility follows familiarity, and familiarity is defined by the books,
  newspapers and magazines of that period.
- `sk_ogx_0014` — line drawings beat photographs where **1983 newspaper reproduction** destroys the
  photograph's realism.
- `sk_ogx_0047`, `sk_ogx_0048` — colour cost ratios, cost per sales call, and the fact that a
  printed trade journal is passed to about three further readers.
- `sk_ogx_0055`, `sk_ogx_0056` — twenty seconds of ordering information, and the dayparts and months
  of American television, both properties of 1983 ordering and broadcast infrastructure.

**Not one claim was modernised.** A `rule_application` governance binding (`bnd_ogx_013`) records
the lane's position: a rule whose stated mechanism is a media condition is retrieved with its
condition or not at all.

### Where I was tempted to modernise, and did not

Recorded honestly, because the temptation was real in each case:

1. **"Open with the fire" and the first-frame rule (`sk_ogx_0040`).** This reads like a
   ready-made claim about short-form video openings, and translating it would have been one
   sentence's work. It was not translated. The claim is stated for a thirty-second broadcast slot
   inside a specific viewing environment, and its supporting reasoning — that the viewer has left
   the room — is about a household television, not a scrolling feed. A separate lane covers modern
   platform guidance; any resemblance is an **observation only** and no claim is transferred. The
   binding `bnd_ogx_004` says so in its `limits`.
2. **The subway card's exposure-duration reasoning (`sk_ogx_0030`).** The general principle —
   dwell time and the absence of competing matter set how much can be read — is genuinely
   attractive as a modern media rule. Ogilvy states it for one transit system in one era and never
   generalises it. Neither did I. It is recorded as his reasoning about that case, and `qa_ogx_0074`
   makes the reader notice that it is scoped.
3. **Miscomprehension at a 19 per cent floor (`sk_ogx_0043`).** It is tempting to state this as a
   general fact about audiences. It is a 1979 study of twenty-five American television commercials
   and is recorded as that.
4. **`sk_ogx_0026`, editorial graphics.** The modern reading — "native advertising works" — is
   sitting right there. It was refused. His mechanism is a learned signal produced by a specific
   historical relationship between two sets of print conventions, and that relationship is what the
   claim depends on.
5. **`sk_ogx_0060`, the repertory of brands.** The temptation here ran the other way: to treat a
   1983 academic finding about packaged goods as a settled law of marketing. It is recorded as a
   finding he reports, conditionally, from two named academics, with no study design or dates.

---

## 5. Hazard 3 — `culturally_bounded`

**8 objects carry `culturally_bounded`.** In every case the material is recorded as *what this
source held in 1983*, never sanitised into neutral modern advice and never extracted as actionable
guidance.

- `sk_ogx_0018`, `sk_ogx_0019`, `sk_ogx_0016` — the assumption that the reader of food, soap and
  household advertising is a housewife runs through the whole print chapter. The chapter's own
  opening quotation is about formulae for "advertisements which grab a woman's attention". The
  objects state the assumption as the source's framing.
- `sk_ogx_0007` — his examples of headline words that flag a narrow audience are "asthma,
  bedwetters, women over thirty-five". Recorded as his wording, not endorsed as a way to describe
  an audience.
- `sk_ogx_0040` — the television viewer is "she" throughout, consistent with the period's
  assumption about who watches daytime television.
- `sk_ogx_0047` — "babies, beagles and bosoms", his own phrase for irrelevant decoration in a
  technical advertisement.
- `sk_ogx_0067` — "the consumer is not a moron, she is your wife", quoted by him from his own
  earlier work.
- `sk_ogx_0045`, `sk_ogx_0068` — the national stereotypes he reports research finding (Americans
  believing the British polite and aloof and the French rude and dirty), and chapter 17's extended
  characterisations of advertising and audiences in a dozen countries, including passages on India
  and Kenya written from the position of a visiting principal. **Chapter 17 produced exactly one
  object**, on the testing procedure for transferring a campaign, and the caveats state plainly
  that the surrounding national material is recorded as what the source wrote and is not extracted
  as guidance about any market.

Chapter 3's section "Women in advertising", which opens by refusing to write "spokesperson" or
"chairperson", was read and **deliberately not extracted**: it is agency staffing, which the lane's
brief refuses, and extracting it would have meant either sanitising it or recording an opinion about
hiring as knowledge about advertising. It is named here so the decision is visible.

---

## 6. Hazard 4 — `figure_semantic_binding_lost`

**Caution name: `figure_semantic_binding_lost`.** It applies to this lane and it applies hard.

The book reproduces advertisements that carry its argument, and in this EPUB they are gone. **39
placeholders** reading "Click here for hi-res image" or "Click here for hi-res image and text"
stand where reproductions were — 6 in the print chapter, 1 in the television chapter, the rest
spread through chapters 9 to 19. The television chapter is doubly affected: the source himself opens
it by saying it is impossible to show commercials on the pages of a book and that all he can do is
reproduce storyboards, and those storyboards are also absent.

**14 objects carry `extraction_uncertainty: figure_not_inspected`.** No visual claim is
reconstructed from text anywhere in this lane. The specific claims that a reader should not treat
as visually grounded:

| Object | What cannot be checked |
|---|---|
| `sk_ogx_0012` | what "story appeal" actually looks like — the Hathaway advertisement is a placeholder |
| `sk_ogx_0013` | the before-and-after form; only the caption for a plant-treatment advertisement survives |
| `sk_ogx_0015` | the finished-dish rule; the "Beautiful but dumb" example was not seen |
| `sk_ogx_0026` | the editorial-style advertisements offered as the demonstration of the whole argument |
| `sk_ogx_0028` | the all-capitals advertisement he says he gave up trying to read |
| `sk_ogx_0029` | **his two "perfect layouts"** — known only from his description of their word counts and proportions. This is the sharpest loss in the lane: a layout claim whose evidence is a layout. |
| `sk_ogx_0041` | the storyboards for every television craft point |
| `sk_ogx_0005`, `0023`, `0030`, `0044`, `0045`, `0046`, `0057` | the reproduced advertisements each rests on |

### A finding that qualifies the live chapter-2 audit

The live audit record classified this loss as `announced_loss_placeholder` with
`recoverability: recoverable_not_attempted`, and noted that captions survive and are substantive.
This lane found something the audit did not record: **the book's own Appendix (spine 30, "Hi-res
images and related text") carries roughly 300 lines of recovered advertisement text and 40 "Click
here to return to the text" links.** The full body copy of the Rolls-Royce advertisement, the
Volkswagen "Think small" copy and others are present in the same file.

So the **copy** of many reproduced advertisements is recoverable *within this copy*; the **layout,
typography, image and their relation to one another** are not. For a book whose print chapter argues
that layout and typography are where advertisements are won and lost, that is precisely the wrong
half to recover. Recorded in `PROVENANCE.md` §7. **The live audit record was not modified** — this
lane is read-only against `canon/audit/**`.

The book's own internal page cross-references ("see this page") render as that phrase with no
target. They are **unresolvable in this copy** and were not resolved by guessing.

---

## 7. Hazard 5 — production advice is parked, not translated

Two `production` bindings, both `status: production_candidate`, both `target_path: null`:

- `bnd_ogx_014` — typographic settings: drop-initial, leading, point size, column measure, type
  colour. **Physical print production for the presses and paper of 1983.** No generative equivalent
  is asserted.
- `bnd_ogx_015` — direct mail production variables (piece size, print colours, personalisation,
  enclosures, brochure) and direct-response television ordering mechanics. **Physical production and
  1983 postal and telephone ordering infrastructure.** Not translated.

In the ontology, **10 remedy terms carry `executable_by: physical_production`** and are not
translated into any other frame. A further **6 carry `unknown`** — the split run, the control, the
international test, inquiry analysis, attitude tracking and the sensitise-then-solicit sequence.
Those are measurement and media procedures with no production form at all, and forcing them into
`physical_production` or `generative_respecification` would have misdescribed them. `unknown` is the
honest value and it is used deliberately.

**Nothing in this lane infers any model capability.** A 1983 book is not evidence about what any
generative system can do, and no binding, term or Q&A item says otherwise.

---

## 8. Bindings — what was made and what was refused

**No `creative_ir` bindings.** Not one. The contract permits them only where a real SPEC-01 path can
be named with justification, and this lane's knowledge is diagnostic questions about finished
assets, physical print settings, or measurement procedures. None of those is a field in a creative
specification. Manufacturing a path here would be the exact distortion SPEC-03 exists to prevent —
the `mb_004` failure recorded in SPEC-03's own preamble.

| Type | Count | Observation units used |
|---|---|---|
| `evaluation` | 9 | `whole_asset` ×5, `sequence` ×1, `shot` ×1, `asset_set_over_time` ×2 |
| `benchmark` | 2 | — |
| `governance` | 2 | consumers: `evidence_interpretation`, `rule_application` |
| `production` | 2 | both `production_candidate`, both `target_path: null` |
| `creative_ir` | **0** | — |

Every evaluation binding carries an `observation_unit`, and three of them use a unit larger than the
asset for a reason: the interchangeable-slogan test (`bnd_ogx_006`) needs the competitor lines the
slogan sits among; the who-was-this-made-to-please diagnosis (`bnd_ogx_009`) needs a body of work;
the super-versus-soundtrack check (`bnd_ogx_005`) needs picture and audio of the same shot together.

Two bindings carry `evidence_basis: extractor_inference` rather than `derived_from_source`, because
they rest on groupings that are ours: `bnd_ogx_008` (the displacement family) and `bnd_ogx_009`
(intended-audience diagnosis). Neither `cross_source_supported` nor `empirically_supported` is used
anywhere in the lane.

**Refused governance bindings.** Two candidates were dropped for having no named consumer: a
proposed binding about how agencies should be structured for craft knowledge to survive
(`sk_ogx_0003` implies it, and it fits none of the six permitted consumers), and one about how to
weight a source's self-reported successes. The permitted-consumer list is the guard against a junk
drawer and it was allowed to do its job.

---

## 9. Concept systems — three, and one refused

- `scs_ogx_001` **the print readership cascade** — `causal_model`, `extractor_inferred`. Members are
  well supported individually; the claim that they form one model is ours, and the source states the
  derivation for only two of six members.
- `scs_ogx_002` **the measurable branches and what measurement costs** — `decision_framework`,
  `extractor_inferred`. Every member is a plain claim of his; the **assembly is entirely ours**, and
  the assembly is the value: his own presentation splits the endorsement of measurement from its
  three costs across three chapters, so any single chapter read alone yields a stronger position
  than the book supports. `source_warns_against_isolated_use: true`, pointing at `sk_ogx_0052`.
- `scs_ogx_003` **displacement of the product by a borrowed element** — `interacting_set`, fully
  `extractor_inferred`. Recorded with high `system_level_uncertainty` and a note that a reviewer
  could reasonably drop one of its four members.

**Refused:** the sixteen television "tips". They look like a system and are not one — an unordered
list of unrelated findings sharing only a medium. Asserting a structure over them would have been
inventing one. They stay as separate objects.

---

## 10. What was deliberately not extracted

- **All of chapter 6**, the open letter to a client choosing an agency: how to pick an agency, what
  to pay it, contract length, conflict-of-interest policy. Business of agency, refused.
- **Chapters 4 and 5** almost entirely — running an agency, agency profit and compensation, winning
  clients, house advertising. One passage in chapter 4 on written principles was read and refused as
  management rather than craft.
- **Chapter 3** except the *Researchers* section. Careers, salaries, hiring, education, social
  status, and the "Women in advertising" section (see §5).
- **Chapter 18** except the Hopkins section. It is six biographies; two objects were taken, both for
  reasoning about evidence rather than for biography.
- **Chapter 20** entirely: thirteen one-line predictions. Extracting a 1983 forecast as knowledge
  would be recording a prediction as a finding.
- **Chapter 17's national characterisations** — extended commentary on advertising and audiences in
  a dozen countries. One object taken, on the testing procedure; the rest recorded in a caveat as
  what the source wrote (see §5).
- Throughout: self-promotion, client anecdote with no mechanism, name-dropping, autobiography, and
  every rule already recorded in the live chapter-2 material.
- Two chapter-16 claims that were extractable and were dropped for budget when the object count
  reached 70: that new products fail more often for not being new enough than for being too new,
  and that companies which did not cut advertising in recession achieved greater profit increases.
  Both are real; both are recorded here as **known omissions**, not as absences.

---

## 11. Self-check results

### 11.1 Every YAML parses
`source-knowledge.yaml`, `source-concept-systems.yaml`, `operational-bindings.yaml`,
`ontology-mappings.yaml` and `qa-bank.yaml` all load under `yaml.safe_load`. **Pass.**

### 11.2 No locator carries a page number; every page field is null
Asserted mechanically, not by eye:

- 70 SourceKnowledge objects and 3 concept systems: `page_start` and `page_end` both `null`.
  **0 violations.**
- `provenance.chapter` and `provenance.section` scanned for `\bpp?\.\s*\d`. **0 matches.**
- 76 Q&A `source_locator` values scanned for `\bpp?\.\s*\d` and for `page \d`. **0 matches, 0
  empty locators.**

**Result: 0 failures, 0 fixes required.**

### 11.3 Spot-check against the cited chapter — run over all 70, not a sample of 25
For each object, at least one `source_terms` entry was located verbatim inside the chapter the
object cites, after Unicode and punctuation normalisation, using an eight-word sliding window.

**Result: 70 of 70 located. 0 failures. 0 corrections required.** The required threshold was 25; the
check was automatable so it was run over the whole set.

### 11.4 No chapter-2 knowledge duplicated
Concept labels were diffed mechanically against the live
`ogilvy-ch2-advertising-that-sells/source-knowledge.yaml` (22 labels) using both token Jaccard and
`SequenceMatcher`.

- **Exact label collisions: 0.**
- Highest similarity pairs on inspection are **string artefacts** of long snake_case labels sharing
  function words (e.g. `sk_ogx_0059` against `sk_ogl_c003_0003` at ratio 0.53 — "the consistency
  that produces the results…" against "the industry avoids testing…", conceptually unrelated).
  **Conceptual duplicates: 0.**

**Near-duplicates deliberately kept, with reasons.** Eight objects touch chapter-2 ground and each
names the live object it builds on inside its own caveats:

| Kept | Live object | Why it is not a duplicate |
|---|---|---|
| `sk_ogx_0012` | `sk_ogl_c003_0019` | Chapter 2 records Rudolph's story-appeal finding **only inside a caveat**, as an example of research the field abandoned. Chapter 7 states it as an **operative craft rule with a dose-response form** — the more injected, the more people look. Different claim about the same finding. |
| `sk_ogx_0003` | `sk_ogl_c003_0019` | Chapter 2 attributes the field's failure to a wilful refusal to learn. Chapter 3 supplies a **mechanism**: no retrieval system plus personnel turnover. Cause, not restatement. |
| `sk_ogx_0049` | `sk_ogl_c003_0020` | Chapter 2 argues you should follow direct response **because** it measures. Chapter 12 says **why the measurement is possible** — a property of the distribution channel, not of the advertising. |
| `sk_ogx_0054` | `sk_ogl_c003_0020` | Chapter 2 makes an argument about whom to imitate. Chapter 12 gives the **specific print craft used inside** direct response, including two exceptions to his own reverse-type rule. |
| `sk_ogx_0056` | `sk_ogl_c003_0017` | **The qualification** — see §12. |
| `sk_ogx_0063` | `sk_ogl_c003_0017` | Chapter 2 says measure at intervals and stop when it wears out. Chapter 15 says **what the measurement looks like when it says stop**: the tracked series flattens. |
| `sk_ogx_0044`, `sk_ogx_0059` | `sk_ogl_c003_0007` | Chapter 2 says project the same image year after year and names only internal forces that erode it. Chapter 9 says what consistency must **consist of** to work; chapter 14 names what it **costs** externally. |
| `sk_ogx_0065` | `sk_ogl_c003_0012` | A genuine **repetition** — the limit that research cannot predict a campaign's long-run value appears in both. Kept because it appears in the chapter devoted to praising research, which is where it carries most weight, and the caveat says it is a repetition. |

### 11.5 Application fraction, computed in code
```
items 76   requires_application True: 27   =  35.5 %
```
**Threshold is one third (33.3 %). Pass.** The first draft came in at 30.0 % (21 of 70) and six
further application items were written rather than relabelling existing ones, because relabelling a
recall question as an application question would be a lie about the bank.

Answer-type distribution: application 25, mechanism 11, source_position 9, boundary_condition 8,
comparison 7, factual 6, failure_diagnosis 5, tradeoff 4, repair 1.
Difficulty: medium 40, hard 22, easy 8.

### 11.6 SPEC-03 purity
Scanned every SourceKnowledge object for an `informs` field, a Creative IR path
(`creative.*` / `entities.*` / `production_ir.*` / `normalized_request.*`), and the registered
product vocabulary. **0 violations.** No decimal confidence value appears anywhere in the lane.

### 11.7 Ontology and binding integrity
- All 15 relationship types are from the permitted vocabulary. **`same_failure_family` is not used**
  — it requires human review under SPEC-05 governance.
- **No `xs_` cross-source concept was created.** Forbidden in this task.
- Both canonical concepts carry `asserts_equivalence: false` and
  `purpose: retrieval_and_aggregation`.
- All 24 remedy terms carry `executable_by` from the permitted list.
- All binding refs resolve; every evaluation binding has an `observation_unit`; both governance
  bindings name a permitted consumer; both production bindings are `production_candidate` with
  `target_path: null`; no binding uses `cross_source_supported` or `empirically_supported`.

---

## 12. The place a later chapter qualifies chapter 2 — stated once more, because it matters

`sk_ogx_0056` against the live `sk_ogl_c003_0017`, on repetition:

- **Chapter 2, live Canon:** readership does not decline across at least four repetitions in the
  same magazine; the audience is a moving parade; repeat a winner until it stops selling.
- **Chapter 12, this lane:** "When you advertise repeatedly in the same magazine, response rates
  almost always drop." Some magazines carry six profitable insertions a year, others twelve.

**One author. One book. Two measures — readership and orders.** He never sets them side by side and
never makes the reconciliation, which is available in his own material. The object records the
qualification and states explicitly that it must never be presented as two sources disagreeing.
`qa_ogx_0047` puts this to the reader directly, and its confounders name the specific error:
*"presenting the two as evidence that the field disagrees about wear-out; both are Ogilvy."*

Two further intra-source tensions are recorded the same way, both flagged by the author himself:

- **`sk_ogx_0055` against `sk_ogx_0059`** — direct-response demonstrations should promise several
  benefits, which he notes in his own parenthesis "runs counter to the Procter & Gamble formula" he
  praises two chapters later. The reconciliation — different objectives, closing a sale versus
  owning an association — is available and he does not state it.
- **`sk_ogx_0031` against `sk_ogx_0006` and `sk_ogx_0010`** — the television chapter rejects recall
  as having no correlation with purchasing, while several of the print chapter's central findings
  are recall findings. This is the sharpest unreconciled inconsistency in the book, and he never
  raises it.

---

## 13. What a reviewer should look at first

1. **§3, the evidence split.** 43 % `empirical_within_source` is high for this author and the
   justification table is there to be attacked object by object. Two are borderline —
   `sk_ogx_0035` and `sk_ogx_0063` supply a *direction* rather than a number, and a reviewer may
   reasonably demote both.
2. **`scs_ogx_003`.** Entirely our hypothesis. It may be wrong.
3. **`bnd_ogx_008` and `bnd_ogx_009`,** the two `extractor_inference` bindings.
4. **§6, the appendix finding,** which qualifies a completed audit record this lane could not and
   did not modify.
5. **The unread portions of chapters 3, 4 and 5** — the only place this extraction is knowingly
   incomplete rather than deliberately selective.
