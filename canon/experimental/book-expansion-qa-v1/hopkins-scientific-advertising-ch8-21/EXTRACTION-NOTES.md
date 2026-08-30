# Extraction notes — Claude C. Hopkins, *Scientific Advertising* (1923), chapters 8–21

**EXPERIMENTAL — NOT LIVE CANON.** Lane `book-expansion-qa-v1`. Nothing in this directory is accepted
Canon, has been reviewed, or may be described as accepted. This lane is a **scope extension of a live
source with zero independence** — see §6.

---

## 1. Counts

| File | Objects |
|---|---|
| `source-knowledge.yaml` | **48** SourceKnowledge objects (`sk_sa8_0001`–`0048`) |
| `source-concept-systems.yaml` | **4** SourceConceptSystems |
| `operational-bindings.yaml` | **11** OperationalBindings (3 governance, 3 evaluation, 3 benchmark, 2 production) |
| `ontology-mappings.yaml` | **46** terms, **14** relationships, **6** concepts (5 source-specific, 1 canonical) |
| `qa-bank.yaml` | **57** Q&A items |

`requires_application: true` — **21 of 57 = 36.8 %** (contract minimum 1/3 = 19 items). Clears without
additions; **no items were added to reach the floor.**

Answer-type mix: application 15 · mechanism 9 · source_position 9 · boundary_condition 4 ·
comparison 4 · tradeoff 4 · repair 4 · factual 3 · failure_diagnosis 3 · concept_definition 2.
Difficulty: 37 medium, 18 hard, 2 easy.

Term kinds: 22 remedy · 19 problem · 5 property. Every remedy carries `executable_by`
(13 `human_edit`, 5 `unknown`, 4 `physical_production`). The four `physical_production` remedies —
store-routed sampling, the pre-announced dealer coupon, undated Sunday coupon insertion, and local
sample delivery — are **left untranslated**, as SPEC-05 rule 6 requires. They are 1923 physical trade
mechanics and there is no generative-media equivalent of mailing a grocer a proof sheet.

> **Three discrepancies in `PROVENANCE.md`, flagged for the reviewer and deliberately not corrected
> here.** That file was written before the bank and ontology were finished, and three of its figures
> are stale:
>
> | `PROVENANCE.md` says | True, verified mechanically in this pass |
> |---|---|
> | §7 "41 ontology terms" | **46 terms** |
> | §7 "54 Q&A pairs" | **57 Q&A items** |
> | §2 "Six objects carry such a caveat" (naming a live `sk_hop_sa_` id) | **18 objects** |
> | §7 "14 relationships (including 4 `distinct_from`)" | 14 relationships ✓, but **6** `distinct_from` |
>
> `PROVENANCE.md` was outside this pass's write scope, so the stale figures were left in place and are
> flagged rather than silently edited. Its §2 also points at "`EXTRACTION-NOTES.md` §5" for the list
> of extending objects and at "§3" and "§7" for the chapter-15 finding and the self-check; in this
> file those are **§9**, **§2** and **§11** respectively.

---

## 2. Resolving the chapter-15 question left open by the live chapters 1–7 extraction

The live `hopkins-scientific-advertising-ch1-7` `PROVENANCE.md` records an explicit unresolved gap:
chapter 15, "Test Campaigns", was not processed; chapter 1 forward-references it; and whether it
reports measurements chapters 1–7 do not was recorded as **NOT VERIFIED**. Chapter 15 (printed
pp. 47–50) falls inside this span, was read in full from the supplied extract, and was then re-read
directly from the PDF (pages 55–58) specifically to answer this question.

### 2.1 Does chapter 15 report measurement *results*?

**No. It does not, and the negative finding is firm.**

Chapter 15 specifies its procedure more fully than any other chapter in the book and then reports
**not one test campaign's return**. There is no cost per customer started, no repeat rate, no purchase
volume and no payback period, for any product, in any town, anywhere in the four pages.

A direct grep of the chapter's every numeral, run against the PDF rather than the extract, returns
exactly four money-or-percentage figures. Sorted by what they actually are:

| Figure | What it is | Is it a test's return? |
|---|---|---|
| `$3,000 to $5,000` | what a four-or-five-town test **costs to run** | No — an input |
| `about $1,000 each` | what the two coupon tests **cost to run** | No — an input |
| `91 per cent` | a **vote on a product form** by a few thousand women who had redeemed a coupon | No — a survey result from a side-use of the apparatus |
| `75 per cent` | cost-of-selling reduction of the **best of fifty plans over five years**, for one food advertiser | No — a cumulative programme outcome, not a test campaign's return |

The two dollar figures are the price of the instrument. The two percentages belong to side-uses
Hopkins himself introduces with "These test campaigns have **other** purposes." Neither is the
quantity the procedure exists to produce.

So the answer to the live gap is the *unwelcome* one: **chapter 15 behaves exactly like chapters 1–7.**
It asserts that measurement happens, specifies how, insists on its authority — "Go to the court of
last resort", "we know almost exactly", "we prove our undertaking absolutely safe" — and then withholds
the returns. `qa_sa8_0042` puts this question to the reader directly and `sk_sa8_0033` / `sk_sa8_0034`
carry it in the knowledge layer.

The sharpest form of the finding: the chapter's load-bearing inferential premise — **"We establish
averages on a small scale, and those averages always hold"** — is stated as an unqualified absolute,
with no mechanism, no conditions, and not one paired figure (predicted from a test, observed at scale)
anywhere in the book. **The strongest claim in Hopkins's measurement doctrine is the one he supports
least.** That is recorded in `sk_sa8_0034` and in `qa_sa8_0038`, and it is arguably a more useful
finding for Canon than a table of returns would have been.

One closing claim of the chapter is unfalsifiable as constructed and is marked as such: "there are
today no advertising disasters piloted by men who know" — any disaster demonstrates the pilot did not
know.

### 2.2 What Hopkins specifies as the procedure

He does specify it, and precisely. Recorded in `sk_sa8_0033` and `qa_sa8_0037`:

- **Scale** — "four or five towns."
- **City selection** — "a few average towns." That is the whole of it. **He never says what makes a
  town average, never names a test city anywhere in chapters 8–21, and gives no selection rule.** This
  is the procedure's largest hole and it is load-bearing, because the extrapolation premise in §2.1
  depends entirely on the towns being representative.
- **Starting method** — a sample offer or a free package, "to get users started quickly."
- **Duration** — **not stated.** He gives *payback* periods (before the bills are due; or three
  months) but never a test length. The only temporal instruction is "Then we wait."
- **What is held constant** — **nothing is specified, and there is no comparison arm.** The chapter-15
  design is a single-arm absolute-level measurement, not a controlled comparison. Where Hopkins does
  describe holding something constant, it is in *other* chapters: the paired-town display test in
  chapter 16 ("Try one town in one way, one in another. Compare total sales"), the same-advertisement
  two-route sample comparison in chapter 13, and the twenty-five-letter cell test in chapter 19. This
  matters, and `t_sa8_0035 → t_sa8_0034 distinct_from` exists precisely to stop the two being merged.
- **What counts as a verdict** — a fixed question sequence: cost per customer started → do users buy
  the samples → will they continue → how much will they buy → how long until profit returns the cost
  of selling. The verdict is the payback answer, and it determines financing rather than go/no-go.

An irony worth recording: **the best-specified test in the whole span is not in chapter 15.** It is the
magazine publisher's letter test in chapter 19 (printed p. 57) — twenty-five letters, a thousand
prospects each, with an explicit abandonment branch if the plan appears unprofitable. That states arm
count and cell size, which chapter 15 never does, and it can kill a programme as well as rank
candidates. `qa_sa8_0049` is built on the comparison; `sk_sa8_0043` holds it.

### 2.3 Does it change the evidence picture the live extraction recorded for chapters 1–7?

**No. It confirms and extends it.** The live record's characterisation of Hopkins — a practitioner
asserting that measurement grounds his rules while systematically not printing what the measurements
returned — survives chapter 15 intact, and chapter 15 is the strongest possible test of it, being the
book's dedicated chapter on the subject and the one chapter 1 forward-references.

The live extraction's caution therefore stands **unchanged and unweakened**. Nothing here licenses
upgrading any live object's `evidence.characteristics`, and this lane does not touch the live record.

**A finding worth flagging to whoever reads this next, recorded as an observation and nothing more.**
The separately-extracted *My Life in Advertising* lane (`sk_mla_0020`) reports that Hopkins's 1927
memoir *does* supply the exact chain chapter 15 withholds — the Liquozone campaign in a dozen small
Illinois cities at 18 cents per inquiry, a deliberate thirty-day wait, 90 cents average sales per
inquirer, then a national reproduction at the same 18 cents and 91 cents per request. So the numbers
exist in Hopkins's corpus; they are simply **not in the book live Canon extracted, and not in the
chapter live Canon flagged.** See §6 for why this is emphatically not corroboration.

---

## 3. Method, and the interruption

### 3.1 Extraction (first pass)

1. Read printed pp. 25–64 end to end before extracting anything, then re-read chapter by chapter.
2. Extracted along mechanism · decision rule · trade-off · failure condition · boundary condition.
   Refused generic advice, motivational prose, the mill-wheel/waterfall/chess metaphors, and the
   chapter-21 peroration about the trade's moral improvement.
3. Diffed every candidate against the live chapters 1–7 objects **before** writing it, not after
   (§5).
4. Separated, at the point of writing each object, the three things Hopkins constantly blends:
   a measurement *asserted*, a result *reported*, and an outcome *claimed*. Where he asserts
   measurement and withholds the return, the caveat says **"measurement asserted, result withheld"**
   in those words, with `origin: extractor_observed`.

### 3.2 The interruption, and what this second pass did

**This lane was killed during its locator spot-check, immediately before writing these notes.** At the
point of interruption the five data files were complete and the `qa-bank.yaml` header recorded that
**22 of 57** items had been spot-checked line by line. The bank was therefore complete but only
partially verified, and the file said so.

This second pass did exactly two things and nothing else: it **completed the locator verification over
all 57 items** (§7), and it wrote this file. It did not re-extract, did not rewrite the four data
files, did not renumber, and did not add or remove Q&A items except as §7 records. The `qa-bank.yaml`
header now states that the pass is complete rather than partial.

---

## 4. Evidence origin across chapters 8–21 — assertion versus result

This is the central characteristic of the source and the thing most likely to be mishandled downstream.

`evidence.characteristics` across the 48 objects:

| Characteristic | Count |
|---|---|
| `explicitly_stated` | 48 |
| `mechanism_given` | 46 |
| `practitioner_assertion` | 45 |
| `argued` | 35 |
| `historical_claim` | 31 |
| `outcome_claimed` | 21 |
| `anecdotal` | 9 |
| `culturally_bounded` | 9 |
| **`empirical_within_source`** | **8** |
| `repeated_within_source` | 6 |
| `mechanism_absent` | 3 |
| `controlled_comparison` | 1 |

### `empirical_within_source` — the count is 8, and here is the justification for each

The rule applied, stated in `PROVENANCE.md` §8 and enforced object by object: **`empirical_within_source`
is used only where Hopkins reports what a measurement returned.** Not where he says a test was made.
Not where he says a thing was "proved". Not where he predicts what a test would show.

| Object | The returned quantity | Page |
|---|---|---|
| `sk_sa8_0010` | $20–$25 per tooth-brush-habit convert | 31 |
| `sk_sa8_0016` | 4 % used canned pork and beans; 96 % baked at home | 35 |
| `sk_sa8_0019` | 425 calories per pint (laboratory return) | 36 |
| `sk_sa8_0024` | 1,460,000 sample requests from one New York issue; one-fifth of coupons presented; 40 c–$1 added cost of charging a dime | 41 |
| `sk_sa8_0026` | 70 c per mailed inquiry vs 18–22 c presented at store, **same advertisement**; 70 % of inquiries by telephone | 42 |
| `sk_sa8_0028` | repeater check in certain territories: loss less than the cost of checking | 42 |
| `sk_sa8_0035` | 91 % voted for the new product form; tests cost ~$1,000 each | 49 |
| `sk_sa8_0036` | best of fifty plans reduced cost of selling 75 % over five years | 49 |

Eight of forty-eight, against **twenty-one** objects carrying `outcome_claimed`. That ratio is the
finding. Hopkins asserts measurement roughly two and a half times as often as he reports what one
returned.

**`controlled_comparison` is used exactly once**, on `sk_sa8_0026`, and the single use was argued
rather than assumed. It qualifies because Hopkins explicitly holds the advertisement constant — "**the
same ad** brings inquiries at from 18 cents to 22 cents each when the coupons are presented at a local
store" — varies one factor (the response route), and reports a cost on both arms. It is still one
unnamed line with no market, period, volume, or statement of whether the arms ran simultaneously, and
the object's caveats say so. **Chapter 15 receives no `controlled_comparison` mark**, which is the
whole of §2 restated in the schema.

Three cases where the temptation to award `empirical_within_source` was refused:

- **"Tests have proved them unappealing"** (p. 33, tooth-trouble headlines). Measurement asserted, no
  return, no margin, no advertiser. `outcome_claimed` only.
- **"the positive ad outpulls the other four to one"** (p. 55). The most quotable number in the span
  and it is not a reported comparison — it is a prediction about *the reader's* future results,
  explicitly conditioned: "**if you have our experience**." He reports no pair of advertisements and
  no returns. `qa_sa8_0047` is built entirely on the dropped conditional.
- **"This has been proved by many disappointments"** (p. 32, prevention appeals). Naming no
  disappointment.

### The audit pattern `source_evidence_never_printed`

**It applies to this span with full force, and it is not a digitisation loss.**

Printed pages 25–64 contain **zero** figures, plates, tables, diagrams or reproduced advertisements.
Every `source_support` value is `text`; every `provenance.inspected.figures` is empty; no object is
marked `visually_demonstrated`.

Yet Hopkins argues throughout from specific advertisements: Arrow Collar advertisements, mail order
advertisements, the Puffed Grains pictures of the grains, correspondence-school pictures of men in
high positions, Marmon's columns of copy, coupon advertisements carrying full-package offers, "before
and after taking" advertisements, and the positive/negative pair he says outpulls four to one. **Not
one is reproduced.** In chapter 9 he goes further and instructs the reader to *look at* mail order
advertisements to see how pictures are used — an instruction the book itself makes impossible to
follow.

The critical point for anyone auditing this lane: **a reader holding the 1923 first edition was in
exactly the position we are in.** The evidence was never printed. No better scan repairs it, no
re-acquisition of the source helps, and the caution name **`figure_semantic_binding_lost` is NOT
applicable** and is not used — nothing was lost, because nothing was ever there. `bnd_sa8_001` binds
this to `evidence_interpretation` governance so that a retrieval layer cannot serve a Hopkins claim as
though its evidence were merely un-digitised.

Locator format is **Case 1** of the addendum (PDF with a verified authored folio, printed = PDF − 8).
Neither `false_page_affordance` nor `no_authored_page` applies. The folio was checked against the
marker at eight independent points and agreed everywhere; **no page was found where the printed folio
disagreed with the marker.**

---

## 5. Chapter 9, "Art in Advertising" — recorded as a source position, not as a claim about images

Hopkins's chapter 9 position is that **pictures often cost rather than pay**, and it is recorded
faithfully because it is genuinely his, argued, and unusual. It must not be recorded as a durable
claim about images, and it is not.

**His argument, as he makes it** (`sk_sa8_0005`, `qa_sa8_0007`): pictures are expensive "not in the
cost of good art work alone, but **in the cost of space**", with one-third to one-half of a campaign
often staked on them. Because the picture is bought with paid space, its true cost is the selling
argument that space would otherwise have carried. That yields a single admission test: use a picture
only when it "form[s] a better selling argument than the same amount of space set in type."

**Where he says pictures do pay** (`sk_sa8_0006`, `qa_sa8_0008`) — and the chapter is routinely
miscited as simply anti-illustration, which is why this is extracted explicitly: apparel (Arrow
Collars — "men whom others envy, in surroundings which others covet"), correspondence schools, beauty
articles, and Puffed Grains, where pictures of the grains beat every figure drawing tried. The common
structure is that the picture depicts the condition the buyer wants to reach, so it is an argument made
pictorially. That is what lets it beat type on Hopkins's own test.

**Why this is contingent on 1923 printing economics and not a durable claim about images.** The whole
argument is an arithmetic over a cost structure that no longer obtains:

- Space was priced by **area**, so a picture and a column of type were substitutes competing for the
  same purchased rectangle. The trade-off *is* the argument; remove it and nothing remains.
- Reproduction was **halftone and line engraving**, and drawings — up to $2,000 each — were the
  expensive artefact. Every art example in the chapter is a drawing or an engraving.
- Colour carried an unstated **printing premium**, which is why his colour verdict (`sk_sa8_0008`,
  `qa_sa8_0010`) is a *cost* finding — "Do color pictures pay better…? Not generally" — and not a
  claim about colour perception. His exception, food dishes and oranges, works on a stated principle:
  colour "comes close to placing the products on actual exhibition."

Every object in the chapter-9 group therefore carries `historical_claim`, and `culturally_bounded`
where the content is period taste (the fool's cap, the salesman in conspicuous clothes, "people do not
patronize a clown"). `qa_sa8_0007`, `qa_sa8_0010` and `qa_sa8_0057` each state the contingency inside
the answer, and `qa_sa8_0007`'s third confounder names the exact over-generalisation to avoid:
"Treating this as a general claim about images rather than an arithmetic over a specific cost
structure." **Nothing in this lane says anything about whether images work.**

The chapter also contradicts itself and the contradiction is preserved rather than resolved
(`sk_sa8_0009`, `qa_sa8_0011`): art is "a study of paramount importance" on p. 28 and the whole class
of art questions is "minor questions … mere economies" on p. 30, two pages apart, never reconciled. A
reconciliation is available — the stake is in the *space*, a basic decision, while execution quality is
a minor one — but **Hopkins does not state it, so it is offered as the extractor's and attributed to
nobody.**

Two further chapter-9 positions where he explicitly withholds a verdict, and the withholding is
preserved (`qa_sa8_0012`): fine versus ordinary art work ("The question is one of small moment.
Certainly good art pays as well as mediocre"), and picture repetition, where he offers only a
probability derived from his new-customers-only premise rather than from any test.

---

## 6. Observations for cross-source review (NOT promotions)

### 6.1 Zero independence against the live source — the binding constraint

**This lane is a scope extension of `hopkins-scientific-advertising-ch1-7`, which is live accepted
Canon. It is the same work: same author, same 1923 volume, same continuous argument, chapters 8–21
following chapters 1–7 without a break.**

```yaml
scope_extension_of: hopkins-scientific-advertising-ch1-7
independence: none — same work
```

The consequence, stated as plainly as it can be:

> **Agreement between chapters 8–21 and chapters 1–7 must NEVER be counted as cross-source
> convergence.** Under SPEC-05 §Governance 5 the dependence here is stronger than `shared_author` —
> it is the *same volume*. Any promotion that treated the two spans as two agreeing sources would
> report one man's single book as corroborated by itself.

This span agrees with the live span constantly and at length — on complete-story copy, on
cost-per-customer as the only measure, on keyed returns, on samples, on the picture-must-earn-its-space
rule. **Every one of those agreements is worth exactly zero as corroboration.** They are one author
restating himself later in the same book, which is what books do.

Where the extension is genuinely additive it is marked: **eighteen** objects carry a caveat naming the
live `sk_hop_sa_` id they extend, depend on, are distinct from, or are consistent with — counted
mechanically in this pass. **Six** ontology
relationships point at live terms (`t_hop_sa_*`) — two `distinct_from`, two `related_to`, one
`narrower_than`, one `broader_than` — and every one of them is labelled **"OBSERVATION against live
Canon, not a promotion"** in its note. All six use only the relations the contract permits across
lanes; nothing stronger than an observation was written.

**No `xs_` cross-source concept exists in this lane, and none may be created here.** The one canonical
concept, `cc_sa8_measurement_level_errors`, carries `asserts_equivalence: false` and
`purpose: retrieval_and_aggregation`, and groups terms from **this lane only**. No
`same_failure_family` relation is used anywhere.

### 6.2 The *My Life in Advertising* relationship — an observation, and also `shared_author`

The separately-extracted `hopkins-my-life-in-advertising` lane covers Hopkins's 1927 memoir. Its own
`PROVENANCE.md` already records `shared_author` dependence against live Canon and states that this
lane's output must not be treated as agreement with it. That is correct and it is restated here from
this side.

**It is the same man.** Agreement between *My Life in Advertising* and *Scientific Advertising*
chapters 8–21 is **also not an independent origin** — it is one practitioner's testimony given twice,
four years apart, about his own career. Two books by one author are one origin.

This matters more than usual here, because the doctrinal overlap is not incidental — it is nearly
total. Comparing concept labels across the two lanes, at least a dozen pairs state the same doctrine:

| chapters 8–21 | *My Life in Advertising* |
|---|---|
| `sk_sa8_0001` one reading decides, carry the whole case | `sk_mla_0030` every ad must carry the whole case, reading is not serial |
| `sk_sa8_0010` / `0011` habit change is unaffordable; ride a trend | `sk_mla_0042` paid advertising cannot create a habit, only direct one |
| `sk_sa8_0024` any charge multiplies acquisition cost | `sk_mla_0044` charging anything for a trial multiplies the cost |
| `sk_sa8_0027` sample released only through a gate of earned interest | `sk_mla_0026` a sample must be earned by an act of interest |
| `sk_sa8_0031` pre-announced full-package coupon forces distribution | `sk_mla_0025` pre-announcing a redeemable coupon forces distribution |
| `sk_sa8_0034` small-scale averages asserted always to hold | `sk_mla_0021` a cheap local test predicts the national market |
| `sk_sa8_0035` product-form decision reversed by a $1,000 test | `sk_mla_0045` a product change must be tested on existing users |
| `sk_sa8_0042` show the condition desired, never the defect | `sk_mla_0049` appeal to a reward, never to prevention or penalty |
| `sk_sa8_0046` a name is display space and must earn it | `sk_mla_0032` the name should carry the claim, it is always displayed |
| `sk_sa8_0009` art quality is a minor economy | `sk_mla_0058` expensive art and colour recorded as an open question |

**Ten near-identical doctrines across two "sources" that are one man.** A naive convergence detector
would read this as overwhelming corroboration. It is nothing of the kind, and this table exists so that
the trap is documented rather than discovered later.

**No cross-lane ontology relationship to any `t_mla_` term was written**, deliberately: the parallel
lane's term ids are not stably resolvable from here, and anything stronger than prose belongs in a
`CROSS-SOURCE-OBSERVATIONS.md`, not in a relationship edge.

The one asymmetry genuinely worth a reviewer's attention, recorded in §2.3 and repeated here as an
observation only: **`sk_mla_0020` supplies the Liquozone measurement chain that chapter 15 withholds**
— 18 c per inquiry across a dozen Illinois cities, a thirty-day wait, 90 c average sales per inquirer,
then the national reproduction at the same 18 c and 91 c. That is precisely the cost-per-customer /
sale-per-customer / payback triple chapter 15 describes the procedure for and never reports. It does
**not** corroborate chapter 15. It is the same author supplying, in a memoir, the returns his manual
omitted — and it is uncontrolled, retrospective, and reported by the man whose reputation rests on it.
Treat it as a finding about the corpus's shape, never as evidence for the doctrine.

---

## 7. The locator verification pass — results

**Performed in full in the second pass. Every one of the 57 items was checked. This is not a
spot-check and not an extrapolation from a sample.**

### Procedure applied to each of the 57 items

1. Parsed the printed page number(s) out of `source_locator`.
2. Asserted every page falls inside **printed pp. 25–64**.
3. Re-read that page in the page-marked source and confirmed it **actually supports the answer** —
   not merely that the topic appears there, but that the sentences the `support` field quotes and the
   claims the `answer` makes are on the cited page.
4. Checked the answer attributes to Hopkins only what Hopkins claims, and that extractor observations
   are marked as the extractor's.
5. Checked the item is not answerable from generic common sense with no exposure to Hopkins.

The full source text of chapters 8–21 was re-read end to end for this pass, and chapter 15 and the
chapter 6/7 boundary of the **live** span were additionally re-read directly from the PDF.

### Results

| | Count |
|---|---|
| Items **checked** | **57** (all) |
| Items **corrected** | **7** |
| Items **deleted** | **0** |
| Items **added** | **0** |

**Locator range check: PASS.** All 57 `source_locator` values parse, and every printed page cited
falls inside 25–64. **Zero out-of-range locators; zero unparseable locators.** No item cited printed
65+ (the 2009 reprint's Gann/Nightingale "Recommended Readings" back matter), which was the specific
failure mode this check exists to catch.

**Support check: PASS on all 57.** Every cited page was re-read and confirmed to carry the quoted
sentences and support the answer. No item required its answer corrected, and no item was found whose
source did not support it at all — hence zero deletions.

### The seven corrections, in full

| # | Item | Correction |
|---|---|---|
| 1 | `qa_sa8_0032` | Locator narrowed **pp. 42-43 → p. 42**. Every element of the answer — "Only one sample to a home", "adults only", undated Sunday insertion, the repeater check, "repeaters form a small percentage" — is on printed p. 42. The p. 43 half of the range was unearned and violated the addendum's specificity rule. `support` relabelled to match. |
| 2 | `qa_sa8_0035` | Locator widened **p. 45 → pp. 45-46**. The answer asserts distribution attained "without a single salesman"; that sentence is on p. 46 ("many advertisers get national distribution without employing a single salesman"), not p. 45. `support` now names the p. 46 sentence explicitly. |
| 3 | `qa_sa8_0054` | `support` mis-attributed the five-dollar-offer sentence to p. 62 alone. It **straddles the page break**: "End an ad with an offer to pay" closes p. 62 and "five dollars to anyone who writes you that he read the ad through" opens p. 63. The locator (pp. 62-63) was already right; the support label was not. Corrected. |
| 4 | `qa_sa8_0028` | Confounder said "his **chapter 7** tactic of inviting comparison". It is **chapter 6**. Verified two ways: the live extraction places `sk_hop_sa_0044 inviting_comparison_defeats_substitution_where_warning_against_it_fails` in chapter 6, and re-reading PDF pages 25–32 confirms the substitution passage ("An advertiser suffered much from substitution…") sits under the *Psychology* running head, before chapter 7 begins. Corrected to chapter 6. |
| 5 | `qa_sa8_0008` | `knowledge_type` **`photography` → `composition`**. Chapter 9 concerns drawings and engravings — it prices art at "$2,000 per drawing" and contrasts "figure drawings" with the Puffed Grains pictures. Nothing in printed pp. 25–64 is about photography. The tag was a mis-file that would have mis-routed retrieval; `composition` matches the three sibling chapter-9 items (`0007`, `0009`, `0057`). |
| 6 | `qa_sa8_0022` | Confounder asserted this quantity "**directly contradicts**" chapter 15. Softened to "sits in tension with", and the reconciliation named. Hopkins never states a contradiction, and one is available (assume the test towns are average) — asserting a flat contradiction attributed to him a self-refutation he does not make. Contract §7 rule 6. |
| 7 | `qa_sa8_0038` | Same correction, same reason: "contradicts his own chapter 11 instruction" → "sits in tension with", with the note that he never raises the tension and never says which towns count as average. |

The `qa-bank.yaml` header comment, which recorded the interrupted state ("Twenty-two were
spot-checked"), was rewritten to state that the pass is complete and that no item is unverified.

### Other cross-references into the live chapters 1–7 span — all checked, all correct

Four further confounders reference the live span by chapter. Each was verified against the live
`source-knowledge.yaml`; **only #4 above was wrong.**

- `qa_sa8_0029` "chapter 6 … the maker should buy the sample at retail" → `sk_hop_sa_0045`, chapter 6 ✓
- `qa_sa8_0025` and `qa_sa8_0056` "chapter 6 claim that people judge value by stated price" →
  `sk_hop_sa_0040`, chapter 6 ✓
- `qa_sa8_0027` "chapter 7 process-fact tactic" → `sk_hop_sa_0053`, chapter 7 ✓
- `qa_sa8_0034` "chapter 1 town-by-town measurement method" → `sk_hop_sa_0004`, chapter 1 ✓

### Common-sense answerability — checked, nothing cut

Every item was tested against contract §7 rule 4. None was cut, because each turns on something
specific to Hopkins: a reported figure ($20–$25, 4 %/96 %, 70 c vs 18–22 c, 91 %, 75 %, 425 calories),
an exact phrase whose wording is the point ("a **seeming** advantage"; "if you have our experience"),
a position that runs *against* the modern default (address only the unconverted; never charge for a
sample; a coupon-redeemer survey as a product decision), or an internal tension a reader must have the
text to see.

The two `easy` items were examined hardest, since low difficulty is where triviality hides:

- `qa_sa8_0013` requires the $20–$25 figure and both of Hopkins's two reasons for it. Not recoverable
  without the text. **Kept.**
- `qa_sa8_0048` looks like generic positive-framing advice, but the modern default is the *opposite*
  (problem-agitate-solve), and the item additionally requires the call-to-action rule ("Send now"
  versus "Why do you neglect this offer?") and the "before and after taking" exception. It
  discriminates. **Kept.**

---

## 8. What was deliberately not extracted

- **Chapters 1–7 / printed pp. 1–24.** Live Canon. Read for the diff in §6 and §7; **not re-extracted,
  and no object here duplicates one.** See §9.
- **Printed pp. 65–68.** Blank leaves, and printed p. 67 is the 2009 Snowball/BN reprint's
  "Recommended Readings" page — W. D. Gann stock-trading titles, Earl Nightingale, a publisher URL.
  **This is reprint matter, not Hopkins, and not the book.** Excluded entirely, and the locator range
  check in §7 exists partly to prove nothing leaked from it.
- **The extended metaphors.** The mill-wheel and turbine (ch. 21), advertising as war and as chess
  (ch. 12), the waterfall going to waste (ch. 12). Rhetoric carrying no reusable mechanism.
- **The chapter-21 peroration** on the trade's coming moral improvement — "Bunk has lost its power",
  "we shall be prouder of it when we are judged on merit". Period professional self-image; the
  chapter's one extractable device, the five-dollar readership offer, is `sk_sa8_0048`.
- **The distribution methods Hopkins himself declines to discuss.** He states twice on p. 44 that
  scores of methods exist and that most "apply to lines too few to be worthy of discussion in a book
  like this". Extracting a taxonomy he explicitly withheld would have manufactured content.
- **The named brands as brand knowledge.** Marmon, Palmolive, Puffed Grains, Vaseline, Jell-O, Kodak,
  Cream of Wheat, Toasted Corn Flakes, Horlick's and the rest appear only where they carry a
  mechanism. Every one is outcome-selected and read backwards, and the Q&A items say so —
  `qa_sa8_0028` on Vaseline and `qa_sa8_0035` on Palmolive both name the selection problem in their
  confounders.
- **Biography.** Chapter 11's "This writer has just completed an enormous amount of reading…" is
  extracted for the *method* (`sk_sa8_0015`), not for the career.

---

## 9. Duplication check against the live chapters 1–7 extraction

**Confirmation: no chapters 1–7 knowledge was duplicated.**

All 48 `concept_label` values in this lane were diffed against all 54 in
`canon/knowledge/current/hopkins-scientific-advertising-ch1-7/source-knowledge.yaml`, mechanically by
string similarity and then by hand on semantics. **No exact duplicate exists.** Highest lexical
similarity across the whole 48 × 54 matrix is 0.53, and both of those pairs are false positives on
shared function words.

### The near-duplicates that were kept, and why

**One genuine semantic near-duplicate was kept, deliberately:**

- `sk_sa8_0005` `a_picture_is_bought_with_space_so_it_must_outsell_the_same_space_set_in_type`
  vs live `sk_hop_sa_0026` `a_picture_must_earn_the_space_it_occupies` (chapter 4).

  **Reason for keeping.** The live object is Hopkins's *rule*, stated in one line in the mail-order
  chapter. The chapter-9 object is the same rule with the **argument, the cost structure, the
  magnitude and the admission test** attached — the one-third-to-one-half stake, space rather than
  artwork as the real cost, and the explicit comparison against "the same amount of space set in
  type", none of which is in chapter 4. It is the author supplying, five chapters later, the reasoning
  under his own earlier assertion. `sk_sa8_0005`'s caveats state **"EXTENDS the live object
  `sk_hop_sa_0026`"** and name it, so the dependence is machine-visible and no future consolidation
  can mistake the two for independent statements. Deleting it would have discarded the mechanism to
  avoid restating a rule.

Two further pairs were examined and **kept as distinct** on genuine grounds:

- `sk_sa8_0046` (a *name* is display space and must earn it) resembles `sk_hop_sa_0026` and
  `sk_sa8_0005` structurally, but the element is different and — worth noting — **Hopkins never draws
  the parallel himself.** `qa_sa8_0052` says so explicitly: "It is the same argument he makes about
  pictures in chapter 9 … applied to a different element, **though he does not draw the parallel
  himself.**" The connection is the extractor's and is marked as the extractor's.
- `sk_sa8_0002` (claims are qualified by headline testing, then **all** of them run permanently)
  against live `sk_hop_sa_0034` (`run_many_appeals_in_parallel_because_a_weaker_appeal_can_still_pay`,
  chapter 5). Superficially the same doctrine, actually the opposite arrangement: chapter 5 runs
  several appeals as several *parallel advertisements*; chapter 8 makes them **co-resident in one**.
  `qa_sa8_0003`'s third confounder exists precisely to hold this distinction open.

**Eighteen** objects carry an explicit caveat naming the live `sk_hop_sa_` id they extend, depend on,
are distinct from, or are merely consistent with — including three `distinct_from`-style negative findings
recorded rather than discarded (`sk_sa8_0019` vs `sk_hop_sa_0011`; `sk_sa8_0034` vs `sk_hop_sa_0004`;
the near-neighbour note against `sk_hop_sa_0029`). Without those, the same false merges get proposed
again in six months.

---

## 10. Hazards and known limits

**The word "scientific" is the source's, not ours.** Hopkins describes his practice as scientific,
exact, proved and law-governed. Those descriptions are recorded as **his claims**, and each object's
`evidence.characteristics` record what he actually supplies. Nothing was upgraded to look better;
nothing was dismissed to look sceptical. `bnd_sa8_001` and `bnd_sa8_002` exist to keep this distinction
enforceable downstream.

**Almost everything here is contingent on 1923 trade structure.** Thirty-one of forty-eight objects
carry `historical_claim`. Bought circulation with unavoidable waste, area-priced space, halftone
engraving, postage classes, retail consignment, coupon redemption at a grocer's counter, the telephone
as a novel response route. The doctrines that survive the change of surface are the *reasoning*
patterns — cost per customer, feasibility screening before commitment, measuring at the level where a
gain and a reallocation differ — not the mechanics.

**Two `production` bindings, both correctly constrained.** `bnd_sa8_010` and `bnd_sa8_011` carry
`status: production_candidate` and `target_path: null`, per binding rule 1. **No physical-production
advice was rewritten as a generative-media instruction anywhere in this lane**, and the four
`physical_production` remedy terms are left deliberately unbound.

**No `creative_ir` binding exists.** SPEC-01 was not supplied to this lane; guessing a path would have
produced a binding resolving to nothing.

**No binding uses `cross_source_supported` or `empirically_supported`.** Both are forbidden in this
task and neither would have been honest: there is no authorised cross-source promotion here and no
Empirical Memory reference attached to anything.

**Nothing here is evidence about model capability.** It is a 1923 trade manual.

---

## 11. Self-check results

1. **All six files parse** (`yaml.safe_load` on the five YAML files; this file is Markdown). Confirmed.
2. **Q&A schema conformance — PASS on all 57.** Every item carries exactly the twelve contract keys,
   no more and no fewer. All 57 `qa_id` values unique. All 57 `source_id` values are
   `hopkins-scientific-advertising-ch8-21`. Every `answer_type`, `difficulty` and `knowledge_type` is
   drawn from the contract's fixed vocabulary. Every `question`, `answer`, `support`, `source_locator`
   and `source_title` is non-empty, and a scan for `TODO` / placeholder text returns nothing. Every
   `confounders` list is non-empty with no empty strings. Every `requires_application` is a boolean.
3. **Locator verification — complete, 57/57.** See §7. Zero out-of-range, zero unsupported, 7
   corrected, 0 deleted.
4. **`requires_application`: 21/57 = 0.368**, above the 1/3 floor of 19. **No items were added** to
   reach it.
5. **SourceKnowledge provenance pages — PASS.** All 48 objects have non-null `page_start` and
   `page_end`, and every one falls inside printed 25–64. Checked mechanically.
6. **Evidence vocabulary — PASS.** Every `evidence.characteristics` list is non-empty and drawn from
   the fixed list; `source_uncertainty` and `extraction_uncertainty` from their enums.
   `extraction_uncertainty: ocr_degraded` is used on **zero** objects, which was verified rather than
   assumed (`PROVENANCE.md` §4: body text clean throughout; OCR failure confined to italic page-number
   footers).
7. **Bindings — PASS.** All 11 resolve inside this lane. All 3 `evaluation` bindings carry an
   `observation_unit`. All 3 `governance` bindings carry a consumer from the permitted list
   (`evidence_interpretation` ×2, `conflict_resolution` ×1). Both `production` bindings carry
   `production_candidate` and `target_path: null`. No binding uses `cross_source_supported` or
   `empirically_supported`. `evidence_basis` split: 8 `derived_from_source`, 3 `extractor_inference`.
8. **Ontology — PASS.** 46 terms, 14 relationships, 6 concepts. Every `kind: remedy` term carries
   `executable_by`. **No `xs_` concept exists.** **No `same_failure_family` relation is used.** The
   single canonical concept carries `asserts_equivalence: false` and
   `purpose: retrieval_and_aggregation`. **Six** `distinct_from` relations record resemblances examined
   and rejected (four intra-lane, two against live Canon terms). The **six** relationships pointing at
   live `t_hop_sa_` terms use only permitted relations and are labelled as observations.
   **No relationship references any `t_mla_` term.**
9. **Systems — PARTIAL PASS; one defect found and left for the reviewer.** All 4 carry
   `system_type_origin`, and **all four** — not three — have
   `whole_system_claim.origin: extractor_synthesis` with a non-null `interpretation_basis`, so the
   §4 origin-marking requirement is met throughout.
   **Defect: `scs_sa8_002` (`the_feasibility_screen_applied_before_a_campaign_exists`) is missing
   `evidence.system_level_uncertainty`.** The contract's §4 template requires it — "state plainly how
   much of this system is OURS rather than the source's" — and the other three systems carry it. This
   matters for `scs_sa8_002` specifically, because its `system_type_origin` is `extractor_inferred`:
   the feasibility screen is a decision framework **assembled by the extractor** from nine chapter-10
   and chapter-11 objects, and Hopkins nowhere presents these as one procedure. That is exactly the
   fact the missing field exists to record. **Not fixed here**, because `source-concept-systems.yaml`
   was outside this pass's write scope; flagged so it is corrected rather than lost.
10. **Write boundary — PASS.** This pass wrote **only** `qa-bank.yaml` and `EXTRACTION-NOTES.md`,
    both inside this lane directory. Nothing under `canon/knowledge/current/**` or `canon/audit/**`
    was created, edited or deleted — the live chapters 1–7 files and the live ontology were **read
    only**, for the diff in §9 and the chapter cross-reference check in §7. Nothing was committed.

---

## 12. Where I was tempted to over-claim, and did not

1. **The chapter-15 answer itself.** This lane exists largely to close a live gap, and there is
   obvious pull toward returning something positive — "yes, chapter 15 supplies the measurements".
   The 91 % and 75 % figures are *right there* and could have been presented as test-campaign returns
   with very little strain. They are not. One is a coupon-redeemer vote on a product form; the other
   is the winner of a fifty-plan five-year search reported as if it were a method's effect. **The
   finding is negative and it is stated as negative**, in §2 and in `qa_sa8_0042`, which asks the
   question directly and answers "No."

2. **`empirical_within_source` on chapter 15.** The chapter has more numerals than any other in the
   span, and tagging it would have made the lane's evidence profile look far stronger. Every figure in
   it is either the *cost of running* the instrument or belongs to a side-use. Chapter 15's two core
   objects (`sk_sa8_0033`, `sk_sa8_0034`) carry **no** `empirical_within_source`. The count stayed at
   8.

3. **`controlled_comparison` beyond the single legitimate use.** Chapter 16's paired-town display test
   and chapter 19's twenty-five-letter cell test are both *described* as designs and are genuinely
   good ones — but Hopkins reports no result from either. Marking a described-but-unreported design as
   a controlled comparison would have confused a method with an outcome. Used **once**, on
   `sk_sa8_0026`, where he holds the advertisement constant and reports a cost on both arms.

4. **The four-to-one figure.** The most quotable number in the span and the one most likely to be
   wanted downstream. Presenting it as a measured result would have been the single most useful
   over-claim available. The conditional is his — "**if you have our experience**" — and
   `qa_sa8_0047` is built entirely on the fact that the conditional is routinely dropped in
   quotation.

5. **Resolving the chapter-9 contradiction on Hopkins's behalf.** A clean reconciliation exists and I
   can state it. Stating it *as his* would have tidied the record and falsified it. `qa_sa8_0011`
   gives both halves, says the source does nothing about it, offers the reconciliation, and attributes
   it to nobody.

6. **Calling the tensions "contradictions".** Two confounders (`qa_sa8_0022`, `qa_sa8_0038`) asserted
   that Hopkins "directly contradicts" himself between chapters 11 and 15. He is in tension; a
   reconciliation is available; he never states either. **Both were corrected in this pass** — items 6
   and 7 in §7 — because a self-refutation he does not make is still something attributed to him that
   he did not claim.

7. **Reading `source_evidence_never_printed` as a digitisation defect.** It would have been easy, and
   more comfortable, to record the missing advertisements as a scan limitation with
   `figure_semantic_binding_lost` and an implied "a better copy would fix this". **Nothing was lost.**
   The 1923 first edition printed no advertisements either. The caution name is **not** used, and §4
   says why in terms that cannot be softened later.

8. **Treating the *My Life in Advertising* Liquozone numbers as closing the gap.** They are the exact
   quantities chapter 15 withholds, and it is genuinely tempting to write that the corpus now has
   Hopkins's measurement chain corroborated across two sources. It has one man saying it twice.
   Recorded in §2.3 and §6.2 as an observation with the `shared_author` dependence stated in both
   places, and **no relationship edge was written to any `t_mla_` term.**

9. **Chapter 9 as a durable claim about images.** "Pictures often cost rather than pay" is a striking
   line and would be a valuable corpus entry if it were about images. It is arithmetic over
   area-priced space and halftone engraving. Recorded as a source position, `historical_claim` on
   every object in the group, with the contingency stated inside three separate Q&A answers.
