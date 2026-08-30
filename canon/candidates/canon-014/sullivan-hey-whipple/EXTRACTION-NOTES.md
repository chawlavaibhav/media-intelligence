# EXTRACTION NOTES — sullivan-hey-whipple

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon and nothing here may
be described as accepted. This is one lane of a non-merge Canon expansion probe. No cross-source
promotion was performed, no `xs_` identifier was created, and no live Canon file was read for
anything other than the overlap check recorded in `PROVENANCE.md`.

---

## 1. Method

1. Read `SCHEMA-CONTRACT.md`, `SCHEMA-CONTRACT-ADDENDUM-LOCATORS.md` (Case 3), SPEC-03, SPEC-04 and
   SPEC-05 before touching the source.
2. Read the completed sibling lane `w3c-wcag22-text-legibility` as the format and quality target,
   and adopted its wrapped YAML shape (`source_id:` plus a single named top-level list per file).
3. Read the live `ogilvy-ch2-advertising-that-sells` extraction — concept labels and claim openings —
   **before** extracting, so that its knowledge would not be restated here as new and so that genuine
   disagreement could be spotted. Read the live `hopkins-scientific-advertising-ch1-7` concept labels
   for the same reason. Neither file was modified.
4. Read the source itself: front matter and Chapters 1–9, 11, 15 and 16 in full, plus one section of
   Chapter 12. Chapters 10, 13, 14 and 17 were read only as headings. See `PROVENANCE.md` §2 —
   **this is a partial extraction of the work and is recorded as one.**
5. Continued an earlier interrupted attempt rather than restarting: the first ten SourceKnowledge
   objects (`sk_whip_0001`–`sk_whip_0010`) and `PROVENANCE.md` survived from that attempt, were
   re-read, judged sound, and kept. Numbering continued from `sk_whip_0011`.
6. Wrote every file incrementally, in appended chunks, and re-parsed after each chunk. The two
   previous attempts at this lane died mid-write on single very large writes; no write in this run
   exceeded roughly a dozen objects.
7. Ran the mechanical self-checks in §6 and fixed what they caught before finishing.

## 2. Locators — audit pattern `no_authored_page`

**This source is an EPUB, reflowable, and has no authored page numbers.** Record the audit pattern
**`no_authored_page`** against this lane. It is not a defect in the extraction: the format has no
page and this is unfixable in this copy.

- `provenance.page_start` and `provenance.page_end` are `null` in **all 70** SourceKnowledge objects
  and **all 7** SourceConceptSystems. Asserted mechanically; see §6.
- Every locator is chapter number + chapter title + the source's own section heading, with the spine
  marker as a secondary file-position aid, e.g.
  `Ch. 6 'The Virtues of Simplicity', section 'Make sure the fuse on your idea isn't too long or too short' (spine 19)`.
- No `p.`-style, `pp.`-style, PDF-page or folio reference appears in any locator anywhere in the
  lane. Asserted mechanically; see §6.
- The EPUB's navigation document contains a `Pages` list enumerating roman iii–xviii and arabic
  1–393, inherited from the print edition. The extracted text carries **no inline page-break
  anchors**, so no sentence in this copy can be tied to any of those numbers. They exist in the file
  and are unusable. None was used and none was reconstructed by interpolation. This is worth naming
  as a near-miss `false_page_affordance`: the file looks as though it has authored pages and does
  not.
- The book's own text cross-references chapters, never pages, so the addendum's
  unresolvable-page-reference case did not arise.

## 3. Hazards, and what was done about each

### 3.1 Practitioner assertion dominates — the count, reported

Across all 70 objects:

| characteristic | count |
|---|---|
| `explicitly_stated` | 70 |
| `practitioner_assertion` | **70** |
| `mechanism_given` | 59 |
| `argued` | 22 |
| `anecdotal` | 19 |
| `repeated_within_source` | 18 |
| `visually_demonstrated` | 11 |
| `historical_claim` | 7 |
| `culturally_bounded` | 6 |
| `mechanism_absent` | 5 |
| `outcome_claimed` | 3 |
| `empirical_within_source` | **0** |
| `controlled_comparison` | **0** |

**`empirical_within_source` is used zero times, and so is `controlled_comparison`.** That is the
finding, not an omission. This book contains no measurement its author made or reports in a form
that could support a threshold. The three `outcome_claimed` objects are the closest it comes, and
each attaches to a figure relayed second-hand: sales volumes for the campaign the book is named
after (`sk_whip_0042`), a share price fourteen years apart (`sk_whip_0035`), and a return-on-spend
ratio reported by an agency about its own work (`sk_whip_0070`). None is a controlled attribution
and each object says so.

**Strong opinion was not allowed to become universal truth.** In the Q&A bank, `source_position` is
the second most common answer type (13 of 78, 17%) and is used wherever an item is about what
Sullivan holds rather than about how the world is — the puns prohibition, the exclamation point, the
focus-group refusal, the effectiveness argument, the "art direction is where brand building happens"
claim, the Volvo reading. Every `support` field names whether the answer rests on a stated claim, a
reported anecdote, or an opinion.

Caveat origins across the lane: **45 `source_stated`, 119 `extractor_observed`.** The imbalance is
deliberate. Sullivan hedges himself less often than the material warrants, so most of the epistemic
qualification in this lane is ours and is marked as ours.

### 3.2 Award-show survivorship

**His examples are a selected sample of celebrated work and he does not correct for it.** Nearly
every campaign named in this book is a One Show, D&AD or Cannes winner or an acknowledged classic;
the book's own account of the author's education is a month spent reading award annuals, which his
first creative director called the graduate school of advertising. There is no case anywhere in the
extracted span of a campaign that used one of his recommended moves and failed.

This is recorded in `PROVENANCE.md`, in the header comment of `source-knowledge.yaml`, in the header
comment of `qa-bank.yaml`, and in `origin: extractor_observed` caveats on every object whose claim
rests on such an example — including `sk_whip_0008` (the sentence architectures), `sk_whip_0011`
(conflict), `sk_whip_0013` (deprivation), `sk_whip_0017` (the hundred lines), `sk_whip_0065` (Rong)
and `sk_whip_0070` (branded content). Two Q&A items (`qa_whip_0062`, `qa_whip_0063`) make the
survivorship itself the subject.

### 3.3 This is about advertising made by humans for paid media

Nothing in this lane is translated into a model instruction and nothing here is evidence about
generative capability. Stated in the header comment of every YAML file. Two ontology remedies carry
`executable_by: physical_production` (`t_whip_0038` Do > Invite > Capture > Share, `t_whip_0039` use
the environment as the visual); per SPEC-05 rule 6 neither is translated into a generative
instruction and neither is bound to anything. The two `target_type: production` bindings
(`bnd_whip_010`, `bnd_whip_011`) carry `status: production_candidate` and `target_path: null`, and
both rationales state explicitly that what is being recorded is a way of organising human working
time, not a generative operation.

### 3.4 `figure_semantic_binding_lost`

**Record the caution `figure_semantic_binding_lost` against this lane.** The book reproduces
advertisements whose images carry the argument, and the extracted text does not contain them. In
several places Sullivan describes an advertisement only by the effect it produces — "you lean into
the ad because you know something's going on", "words don't do this spot justice" — so the claim and
the artefact cannot be separated.

- **30 of 70 objects** carry `extraction_uncertainty: figure_not_inspected`.
- **33 of 70 objects** name specific `figure_refs`; `inspected.figures` is `[]` in every object,
  because no figure was inspected anywhere in this lane.
- 28 objects carry `source_support: text_and_visual`.
- The objects most affected are the whole of Part D (which element carries the idea): `sk_whip_0043`,
  `sk_whip_0044`, `sk_whip_0047`, `sk_whip_0048` and `sk_whip_0052` all rest on what a reproduced
  advertisement does, taken on the source's word. `scs_whip_006`'s
  `system_level_uncertainty` states this as a material limitation of the whole system.

### 3.5 Technology-contingent material

The later chapters add digital, social and branded-content material. Everything platform-specific is
labelled and none of it is presented as durable:

- `sk_whip_0070` carries `historical_claim` and `culturally_bounded`, and its first caveat states
  that every named platform, feature, format limit and content-scheduling vocabulary is contingent
  on the commercial platforms of the writing period. Sullivan footnotes one of his own terms
  (*stock* and *flow*) as dating from about 2011 and no longer in wide use — his own concession, and
  it is quoted.
- `qa_whip_0077` is built entirely around separating what survives from what is dated, and names
  three classes of contingent material.
- `sk_whip_0026` carries `historical_claim` because its distraction argument is contingent on the
  device culture of its period, not a claim about the medium of writing as such.
- `sk_whip_0066` records Sullivan's own warning that viral is a result rather than a strategy, which
  bounds the talkability material against being read as a distribution plan; `qa_whip_0066` puts the
  same point to a reader.

## 4. What was deliberately not extracted

Refused wholesale, per the lane brief:

- **War stories with no reusable principle.** The Whipple assassination anecdote, the actor mobbed
  at a restaurant, the blue-flyswatter client — the last of these is kept only as a `counter`
  example illustrating that clients' reasons often defy analysis, not as knowledge.
- **Agency-life colour.** Feet on the desk, talking about movies, the project manager, the pig-washing
  metaphor as a metaphor, the "Ad God" morning after an award. The one substantive claim inside the
  pig-washing passage — that inspiration's arrival time is what makes creative scheduling hard — is
  extracted; the metaphor is not.
- **Industry gossip and the history of agencies.** The Creative Revolution narrative, the personnel
  of Doyle Dane Bernbach, the positioning wars. Kept only where a claim is load-bearing for
  `sk_whip_0042`'s argument.
- **Career and portfolio advice.** The whole of Chapter 17 (portfolio construction, website,
  interviewing) and the hiring anecdotes in Chapter 1.
- **Motivational passages.** Chapter 18 in full; the "fear and arrogance" passage; the closing pages
  of Chapter 15 on not taking the work too seriously; "learn to enjoy the process".
- **Award-show example lists with no mechanism.** Long runs of admired campaigns in Chapters 9, 10,
  11 and 12 that are named and praised without a stated reason.
- **Personal-conduct advice** with no bearing on the work: expense reports, punctuality, office
  politics, "don't drink or do drugs".
- **Chapter 14** (television craft) and the un-read parts of Chapters 10, 12 and 13 — not refused on
  principle, simply outside the span this run covered. Recorded as unread rather than as absent.

Also refused as a category: **the voice**. Sullivan writes in a comic, profane, digressive register.
The reasoning is extracted and the joke is not — except where the tone carries an actual claim, in
which case the claim is extracted and the joke discarded. Examples: that an exclamation point makes
a brand sound desperate (`sk_whip_0033`); that a certain kind of invented-name advertisement is an
irritating kind of fake (`sk_whip_0034`); that the reader is not out looking for clarity
(`sk_whip_0005`).

## 5. Observations for cross-source review (NOT promotions)

**None of what follows is a promotion, a cross-source concept, or a claim of agreement or
disagreement between Canon sources.** These are observations recorded as prose for a future
Controller review, exactly as the schema contract requires. No `xs_` identifier exists in this lane,
no cross-lane relationship was written into `ontology-mappings.yaml`, and no SourceKnowledge object
knows that any other source exists.

The Canon's live advertising knowledge is Ogilvy (1983) and Hopkins (1923), both from the reason-why
tradition. Sullivan writes from the creative-department tradition. **The disagreement is not
resolved here and must not be resolved by anyone reading this file alone.**

### 5.1 Where Sullivan appears to disagree, and it looks genuine

1. **Whether selling is a sufficient criterion.** Live `ogilvy-ch2` holds
   `selling_not_style_is_the_criterion_for_a_good_advertisement`; live `hopkins-ch1-7` holds
   `the_only_purpose_of_advertising_is_to_make_sales` and
   `advertising_is_multiplied_salesmanship_and_is_judged_by_salesmans_standards`. `sk_whip_0042` is
   the direct denial of sufficiency: the campaign the book is named after sold enormously and
   Sullivan holds it should not be applauded for it. **This is the sharpest disagreement in the lane
   and it is the book's founding argument.** One complication worth an Audit Gate's attention:
   Sullivan makes the argument by quoting **Norman Berry, a creative director at Ogilvy's own
   agency**, so this is not cleanly a between-house disagreement. A second: `sk_whip_0042`'s
   caveats record that Sullivan never defends the step his argument needs — that the creative route
   reaches the same commercial destination.

2. **Whether a clever headline is an asset or a defect.** Live `hopkins-ch1-7` holds
   `a_blind_or_clever_headline_attracts_the_wrong_readers_and_hides_the_offer_from_the_right_ones`.
   `sk_whip_0005`, `sk_whip_0007` and `sk_whip_0008` are a sustained argument that wit is the
   mechanism by which an idea registers and persists. These are contradictory as stated. Note
   before anyone resolves them: Hopkins is writing about keyed mail-order advertisements where the
   headline's job is to select respondents, and Sullivan about advertising encountered by someone
   who did not seek it out. **That is a difference in problem, not necessarily in finding**, and no
   one should record either as refuted by the other.

3. **Whether copy should be cut.** Live `hopkins-ch1-7` holds
   `brevity_should_not_be_imposed_because_only_interested_people_read` and
   `telling_the_complete_story_sells_more`. `sk_whip_0056` prescribes cutting a finished piece by a
   third; `sk_whip_0003` treats every added element as diluting the rest. Again these are
   contradictory as stated, and again the media differ. Complicating both: `sk_whip_0045` records
   Sullivan endorsing long copy and claiming that its visible weight adds gravitas whether or not it
   is read — which is closer to Hopkins than to Sullivan's own reduction argument, and which he does
   not reconcile.

4. **Whether the practitioner's judgement can be trusted.** Live `hopkins-ch1-7` holds
   `the_advertising_mans_own_judgment_errs_about_nine_times_in_ten` and
   `principles_are_established_by_keyed_returns_and_repeated_comparison`; live `ogilvy-ch2` holds
   `copy_direct_response_because_it_measures` and
   `the_industry_avoids_testing_whether_advertising_sells`. `sk_whip_0039` and `sk_whip_0068` reject
   the testing of creative work outright. This is a **methodological** disagreement and is the one
   with the most at stake for any future consolidation. Recorded here without adjudication, but with
   two things flagged: Sullivan's own line — research to generate ideas, not to judge them — is
   narrower than his rhetoric, and he is not disinterested, which he does not raise.

5. **Where big ideas come from.** Live `ogilvy-ch2` holds
   `big_ideas_come_from_an_informed_unconscious` and reports fewer than one campaign in a hundred
   containing one. `sk_whip_0017`, `sk_whip_0018` and `sk_whip_0021` describe a volume-and-discard
   process. These are **less opposed than they look** — `sk_whip_0021` explicitly endorses an
   incubation model — and the real difference is where the emphasis falls, on the wait or on the
   throughput. Anyone reading this as a clean disagreement is over-reading.

6. **What makes an idea durable.** Live `ogilvy-ch2` holds
   `durability_over_decades_is_the_test_of_a_big_idea` (could it run thirty years). `sk_whip_0009`
   makes productivity a function of a rule set's richness instead. Different criteria for a
   related property, not obviously contradictory.

### 5.2 Where a careless reader would manufacture a disagreement, and should not

7. **"Make the product the hero" versus "the brand is not the hero".** Live `ogilvy-ch2` holds
   `make_the_product_the_hero`; `sk_whip_0015` states that the brand is not the hero, the customer
   is. **These are not in conflict.** Ogilvy is talking about what to feature; Sullivan is assigning
   a narrative role within a borrowed story template. Flagged so that nobody records a contradiction
   that is not there.

8. **Superlatives.** Live `hopkins-ch1-7` holds
   `generalities_and_superlatives_leave_no_impression_and_discredit_the_rest`; `sk_whip_0040`
   records Sullivan's preference for an absolute over a comparative. **Also not in conflict**:
   Hopkins objects to unsupported superlatives and Sullivan requires the absolute to be true —
   "it's not often the product you're working on is, in fact, the best, but when it is, set up camp
   there". A consolidator matching on the surface word "superlative" would get this wrong.

9. **Committees.** Live `ogilvy-ch2` holds `campaigns_made_by_committee_achieve_nothing`;
   `sk_whip_0068` records Sullivan's claim that permission research grinds ideas into vanilla or
   nonsense. These **agree**, and that is exactly why it is recorded here rather than acted on:
   apparent cross-source agreement between a 1983 practitioner and a 2022 practitioner in the same
   industry is weak evidence, and manufacturing corroboration from it is forbidden in this task.

### 5.3 Relation to the separately-extracted Google ABCD lane

Observation only, and deliberately thin. `sk_whip_0001` and `sk_whip_0060` make comprehension speed
a function of how long the viewer dwells with the medium, and `sk_whip_0074`'s underlying claim is
that attention is earned rather than owed. Those are adjacent in subject to platform-specific
short-form guidance. **They are not evidence for it and it is not evidence for them.** Sullivan's
material is a practitioner's account of human-made work for paid and earned media, his own
platform-specific claims are dated and labelled as such (§3.5), and the ABCD lane's material has a
different origin, a different evidentiary basis and a different unit of analysis. No relationship
was written, and the two lanes' term identifiers are not resolvable from each other in any case.

## 6. Self-check results

All checks were run in code against the written files, not asserted.

**1. Every YAML parses.**

| file | parses | contents |
|---|---|---|
| `source-knowledge.yaml` | yes | 70 SourceKnowledge objects |
| `source-concept-systems.yaml` | yes | 7 SourceConceptSystems |
| `operational-bindings.yaml` | yes | 12 OperationalBindings |
| `ontology-mappings.yaml` | yes | 58 terms, 24 relationships, 8 concepts |
| `qa-bank.yaml` | yes | 78 Q&A items |

**2. No locator contains a page number; every `page_start`/`page_end` is null.** Asserted
mechanically:

- Objects with a non-null `page_start` or `page_end`, across SourceKnowledge and
  SourceConceptSystems: **0 of 77**.
- Locator strings matching any of `\bp\.\s*\d`, `\bpp\.\s*\d`, `\bpages?\s+\d`, `folio`,
  `PDF page`, `printed page`: **0 of 78** Q&A locators, and **0** provenance strings.
- Every numeral appearing in a Q&A locator was checked for its context; all resolve to a chapter
  number, a spine number, a figure number, or a number belonging to the source's own section
  heading (`write 100`, `180˚`, `25 seconds`). None is a page.
- Spine numbers used across the lane: 9, 11, 13, 15, 17, 19, 21, 23, 25, 29, 31, 37, 39 — all inside
  the file's real range of 2–50.

**Spot-check against the source, far beyond the required 25.** Every quoted section heading in
`qa-bank.yaml`, `source-knowledge.yaml` and `source-concept-systems.yaml` was checked to occur
inside the spine document its locator cites, by normalised substring match against the extracted
text: **211 checked, 211 passed, 0 failed.** All 15 distinct chapter titles cited across the lane
were checked to occur in the source text: **15 of 15 found.**

**Locators corrected: 2.** Both were caught by the check and both were real.

- The exclamation-point section heading had been cited with an ellipsis
  (`Never, ever … use exclamation points anywhere, ever`), which is a legitimate elision but is not
  findable by search. Replaced in both files with the source's full heading,
  `Never, ever, not even once, or even just a little bit, ever use exclamation points anywhere, ever`.
- The Rong section heading used the degree sign `°` where the source uses the ring above `˚`
  (U+02DA). Corrected to the source's character in both files.

A third discrepancy was found and **not** corrected, because the source text is wrong and the
locator is right: the plain-text conversion joined the Chapter 1 title across a line break as
`A BRIEF HISTORYOF WHY EVERYBODYHATES ADVERTISING`. The locators use the correct title. Recorded in
`PROVENANCE.md` §5 so that a future reader grepping the extracted text is not misled.

**3. Application fraction, computed in code.**

```
items = 78
requires_application: true = 31
fraction = 31 / 78 = 0.3974
required >= 1/3 (0.3333) — PASS
```

Answer-type mix: application 15 (19%), source_position 13 (17%), mechanism 11 (14%),
boundary_condition 10 (13%), repair 7 (9%), comparison 7 (9%), concept_definition 5 (6%),
failure_diagnosis 4 (5%), tradeoff 3 (4%), factual 3 (4%). Against the contract's target mix, this
lane is light on definitions and facts and heavy on source_position and boundary conditions. That is
a property of the source: it is a book of arguments and prohibitions, not of definitions, and it has
almost no facts that are not the author's opinion. Diagnosis plus application is 19 of 78 (24%) and
boundaries plus exceptions is 10 of 78 (13%), both close to target.

Difficulty: easy 15, medium 50, hard 13.

**4. Prohibitions.**

- No `xs_` concept exists anywhere in the lane. Checked.
- No `same_failure_family` relationship exists. Checked.
- No Creative-IR path, no `creative.*` or `entities.*` path, no product vocabulary, no decimal
  confidence value, and no `status` field gating on product usefulness appears in any
  SourceKnowledge object. Checked by string scan; the one hit was the word "creative" followed by a
  sentence-ending full stop in prose, which is not a path.
- Every `kind: remedy` term carries a non-null `executable_by` from the permitted list: **25 of 25
  remedy terms**. Checked. Values: 23 `human_edit`, 2 `physical_production`.
- Every non-remedy term carries `executable_by: null`. Checked.
- `target_type: creative_ir` appears zero times. `target_type: governance` appears zero times
  (nothing in this source addresses any permitted governance consumer).
- Both `target_type: production` bindings carry `status: production_candidate` and
  `target_path: null`. Checked.
- Every `target_type: evaluation` binding carries an `observation_unit` from the permitted list.
  Checked, 9 of 9.
- `evidence_basis` is `derived_from_source` (7) or `extractor_inference` (5). Neither
  `cross_source_supported` nor `empirically_supported` appears anywhere except in the
  `operational-bindings.yaml` header comment stating that they do not. Checked. Likewise `xs_` and
  `same_failure_family` appear only in the `ontology-mappings.yaml` header comment forbidding them.
- Binding target types: 9 `evaluation`, 2 `production`, 1 `benchmark`, 0 `creative_ir`,
  0 `governance`. Observation units used: `whole_asset` 6, `asset_set_over_time` 2, `sequence` 1.
- Ontology term kinds: 16 problem, 25 remedy, 12 property, 5 entity.
- System types: 3 `sequence`, 1 `causal_model`, 1 `mutual_qualification`, 1 `decision_framework`,
  1 `interacting_set`.
- Every `source_knowledge_refs`, `source_system_refs`, `failure_ontology_refs` and
  `repair_ontology_refs` entry resolves inside this lane. Checked, 0 unresolved.
- Every `intra_source_relations` target resolves to an object or a system in this lane. Checked,
  0 unresolved.
- Every `member_of_system` relation declared on an object is matched by a corresponding entry in
  that system's `members`, and vice versa, with no orphans in either direction. Checked; one
  mismatch was found (`sk_whip_0041` belongs to two systems and declared only one) and fixed.
- All 7 `whole_system_claim` entries carry `origin: extractor_synthesis`, and all 7 carry a non-null
  `interpretation_basis`. Checked. None claims `source_explicit`: even where Sullivan states an
  ordering himself (the platform sequence, the copy-finishing sequence), the *whole-system* claim
  built on top of it is ours, and is marked as ours. Every `members[].membership_origin` and every
  `internal_structure.ordering.origin` is likewise marked at its own level.
- Every evidence characteristic, `source_uncertainty`, `extraction_uncertainty`, relation, role,
  observation unit, answer type, difficulty and knowledge type is drawn from its fixed vocabulary.
  Checked. One violation was found during writing (an invented characteristic
  `technology_contingent_not_in_vocabulary` on `sk_whip_0026`) and corrected to `historical_claim`.
- No Q&A item has an empty or placeholder answer, and no `confounders` list is empty. Checked.

## 7. Where the extraction was tempted to over-claim and did not

Recorded because it is the part of this work that a reader cannot check.

1. **The book's founding argument.** `sk_whip_0042` could have been written as "creative advertising
   is as effective as reason-why advertising and more decent". Sullivan does say the creative route
   "leads to the same place — enduring brands and market leadership". He never supports it, and the
   book contains no comparison of outcomes between the two schools anywhere. The object records the
   claim as his position, and a caveat names the undefended step as the least defended in the
   argument. `qa_whip_0062` makes it the subject of a question rather than burying it.

2. **The dopamine explanation.** `sk_whip_0007` could have been recorded as a neurological mechanism
   for why wit works. Sullivan cites a general NIH item about how the brain evaluates whether a
   mental task is worth the effort and connects it to advertising comprehension himself. The cited
   research is not about advertising. The object records the gloss as his and says so.

3. **The five-to-forty-percent range.** It is quoted from another book and reads like a
   specification. It is a figure of speech, nothing in the source operationalises it, and the
   caveat says exactly that. No binding uses it.

4. **`empirical_within_source`.** There was a real temptation to use it for the Charmin sales
   figures, the share price, and the return-on-spend ratio, all of which look like measurements.
   None is a measurement the source made, and none has a method attached. The characteristic is used
   **zero times** and `outcome_claimed` is used instead, three times.

5. **The two-second outdoor test as a threshold.** `bnd_whip_005` could have been a benchmark with a
   pass mark. There is no sample, no protocol, no scoring and no baseline; the seven-word figure is
   reported as something that has been said rather than measured. The binding proposes a repeatable
   exercise producing a comparable observation, and its limits say explicitly that its results are
   not evidence about effectiveness.

6. **The talkability tests as effectiveness tests.** Chapter 9 reads as though "will people talk
   about it" and "would the press cover it" were criteria for whether advertising works.
   `sk_whip_0066` records that they measure attention, that this is not the criterion `sk_whip_0042`
   proposed in place of sales, and that the chapter reads as though they were the same thing.
   `bnd_whip_007` binds only the *ordering* of the checks, not a score.

7. **The "obedient idea".** It is a genuinely useful diagnosis and it is also unfalsifiable as
   stated. `sk_whip_0038` and `qa_whip_0041` both carry the observation that no check distinguishes
   an inert idea from one the reviewer dislikes, and that the diagnosis sits inside a chapter urging
   provocation.

8. **The process chapters as a method.** `scs_whip_004` unifies sixteen objects from four chapters
   into one working cycle. Sullivan presents no process — he presents advice under headings, and
   says explicitly that whatever process a reader arrives at is their own. The system's
   `system_level_uncertainty` states in plain words that this is the most extractor-assembled system
   in the lane, and `bnd_whip_010` repeats it.

9. **Cross-source resolution.** Several of the tensions in §5 have obvious resolutions — media
   differ, eras differ, problems differ. Two of them are noted as *possible* explanations precisely
   so that nobody mistakes the note for the finding. **None was resolved.** No cross-source concept,
   no cross-lane relationship, no `xs_` identifier, and no claim of corroboration was created.

10. **Independence.** `PROVENANCE.md` records that Sullivan cites Ogilvy directly, quotes Ogilvy's
    own creative directors, and quotes an Ogilvy-published book in three separate chapters. It would
    have been easy to assert independent origin on the strength of different author, publisher,
    decade and tradition. The file states instead that this lane does not adjudicate independence,
    that independence is established from Audit Gate lineage records which do not exist for this
    source, and that the Fowler dependency is heavier than a citation and should be examined rather
    than assumed away.
