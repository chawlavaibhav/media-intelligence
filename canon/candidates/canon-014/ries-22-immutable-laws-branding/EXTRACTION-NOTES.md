# EXTRACTION NOTES — `ries-22-immutable-laws-branding`

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon. It has not been
reviewed by the Controller, has passed no Audit Gate, and must never be described as accepted.

Companion to `PROVENANCE.md`, which carries source identity, page mapping, span, access basis,
overlap and the evidential character of the source. This file carries method, hazards, refusals,
cross-source observations and self-check results.

---

## 1. Method

Read the Introduction (printed pp. ix–xvi) and all twenty-two chapters (printed pp. 3–110) in full
from the page-marked text, chapter by chapter, before writing anything. Structure was taken from the
book's own contents list (printed pp. v–vi), which gives the starting page of each law and made the
chapter boundaries exact rather than inferred.

Extraction unit: **one object per distinct claim, not one object per chapter.** Several chapters
carry more than one thing worth recording — the Law of Expansion carries the law itself, the
short/long-term trade-off, the weak-competition clause and the teeter-totter argument, and each is a
separate object because each can be true or false independently. Two chapters (Shape, Colour) were
compressed relative to their length because much of their content is restatement.

Order of writing: `source-knowledge.yaml` first and complete, then `source-concept-systems.yaml`
(which can only be written once the members exist), then `ontology-mappings.yaml`, then
`operational-bindings.yaml` (which references both the knowledge and the ontology), then
`qa-bank.yaml`. Every file was written incrementally in chunks of ten to thirteen objects and parsed
after each chunk, following the brief's instruction after earlier attempts in this run died on large
single writes.

`PROVENANCE.md` was inherited from a previous attempt in this run. It was read in full, checked
against the source, and **kept**. Its page-mapping verification table, its account of the book's
evidential character and its §7 analysis of the four rejected `empirical_within_source` candidates
were all confirmed against the text and are sound. Two additions were made: the mechanical
re-verification of the folio offset across all 256 markers, and a pointer to the self-check results
below. Its stated counts (49 knowledge objects, 3 systems, 9 bindings, 50 Q&A items) were treated as
targets and all four were met exactly.

---

## 2. What the authors claim about how the twenty-two laws relate

This was a specific instruction in the lane brief, so the answer is set out here in full. It is
recorded in `scs_r22_001` and in `sk_r22_0049`.

**They never claim the laws are independent, orthogonal, ranked, or applied in sequence.** No such
statement appears anywhere in the span. The numbering is presentational; only once is a law given an
ordinal, when the Law of Expansion is called "the first law of branding" (printed p. 91).

**What they do claim, in their own words:**

| Claim | Where |
|---|---|
| The laws apply universally, "equally to the Internet as they do in the real world" | printed p. xiv |
| Laws are inputs to other laws — "the best way to build a quality perception in the mind is by following the laws of branding. Take the law of contraction" | p. 35 |
| One law is derived from another — the Law of the Category opens by restating the Law of Contraction and pushing it further | p. 39 |
| Laws are invoked by name inside other chapters — "the law of expansion suggests the opposite" | p. 56 |
| One pair has an explicit temporal order — "First publicity, then advertising is the general rule" | p. 19 |
| One law is an exception to the others — "the law of change is the biggest exception to the laws of branding" | p. 101 |
| The laws are immutable but brands are not | p. 105 |
| What "the laws seem to suggest" is true, and then departed from | p. 77 |
| Chapters cross-refer forward by number for the reader | p. 60 → ch. 15 |

So the set is presented as **an interconnected body of mutually qualifying practitioner advice in
which at least one member overrides the rest**, and simultaneously asserted as universal. Those two
framings are never reconciled.

**The classification as `mutual_qualification`, and the conflicts listed below, are OURS**, and are
marked as extractor synthesis at every structural level of `scs_r22_001`. The authors nowhere say
their laws conflict.

### Tensions between laws — recorded, not resolved

The brief flagged the expansion/contraction pair specifically. Six tensions were found and all six
are recorded in `scs_r22_001.internal_structure.conflicts`:

1. **Domination against the share ceiling.** Law 2's five-step pattern names "dominate the category"
   as the ultimate objective of any branding programme and cites Microsoft at 95 per cent, Intel at
   80 and Coca-Cola at 70 approvingly (pp. 10–11). Law 8 says a leading brand's rightful share is
   never more than 50 per cent (p. 42) and Law 11 gives about 50 per cent as the researched upper
   limit (p. 60). Coca-Cola carries two different figures in the two passages with no comment. This
   is the sharpest conflict in the book and it is never addressed.
2. **Narrowing against stocking in depth.** *Inside the expansion/contraction pair itself.* Law 1
   and Law 2 are the same claim stated negatively and positively — but Law 2's own programme has the
   brand contract what it is about (step 1) while expanding what it carries (step 2: ten thousand
   toys against a department store's three thousand) and how much of the category it takes (step 5).
   The book never says where narrowing stops and depth begins. This is the tension the brief
   expected and it is real, though it sits *within* the pair rather than *between* its two halves.
3. **Smother against welcome.** Law 4 tells a leader to use massive advertising to smother
   competitors and make them pay through the nose (p. 21). Law 11 tells the dominant brand to
   welcome competitors because they build the category (p. 56). Both are stated as laws.
4. **Never change against change carefully.** Law 19: markets may change but brands should not, ever
   (p. 97). Law 20 opens by saying nothing in branding is absolute (p. 101). The authors present
   this as a stated exception rather than a conflict, but supply no criterion for identifying which
   of Law 20's three situations a brand is in.
5. **One brand against a family.** Laws 2 and 22 point to a single narrowly focused brand; Law 15
   concedes that the laws seem to require exactly that, agrees it is true, and licenses a second,
   third and fourth (p. 77) — again with no test for when the "time and place" has come.
6. **The word against the visual.** Two of the twenty-two laws are given to logotype and colour,
   while both chapters argue that the visual is secondary and the meaning lies in the word (pp.
   84–85).

A seventh, softer tension is worth a reviewer's eye and is recorded on `sk_r22_0023`: Law 6 tells a
brand in a tiny market never to forget leadership and not to be duped into selling the benefits of
the category (p. 32), while Law 8 tells a leading brand to promote the category rather than the
brand (p. 39). The chapters address slightly different situations, but the instructions point
opposite ways and the book does not distinguish them.

**None of these was resolved.** Where two laws point in opposite directions both are recorded, and
`bnd_r22_007` (governance, `conflict_resolution`) exists specifically so that a downstream consumer
retrieving one side must retrieve the other.

---

## 3. Hazards

### 3.1 "Immutable law" is rhetoric, not a finding — the primary hazard of this lane

The word "law" in this book carries no evidential weight beyond the authors' assertion. Two
practising positioning consultants are writing about their own clients and about companies whose
outcomes were already known. **Every law-bearing object carries `practitioner_assertion`**; most
carry `anecdotal` and `outcome_claimed`; every object resting on named companies carries
`historical_claim`. The hazard is stated in the header comment of every YAML file in this directory,
in `PROVENANCE.md` §6, in the dedicated object `sk_r22_0049`, and in a governance binding
(`bnd_r22_008`, `evidence_interpretation`) whose entire purpose is to stop the word "law" doing
weighting work downstream.

**Where we were tempted to grant "law" more weight than the evidence supports, and did not.** Four
places, recorded honestly:

- **The Law of Extensions felt true.** Cannibalisation is a familiar and plausible mechanism, and
  the "wrong end of the ruler" diagnostic is genuinely sharp. The temptation was to write the object
  with `argued` and `mechanism_given` and let it stand as a finding. It does carry those, but it
  also carries `anecdotal` and `outcome_claimed`, and the caveat states that the beer case has no
  comparison group and that the authors themselves concede on p. 52 that the regular-to-light shift
  was a real market movement — which is the alternative explanation they do not separate.
- **The Consumer Reports passage (p. 35) was the one real candidate for
  `empirical_within_source`.** The authors line up quality rank against sales rank themselves and
  report three pairs. It was rejected. See §5.
- **"Our research indicates that 50 percent is about the upper limit" (p. 60)** was tempting to
  treat as a reported measurement because it uses the word "research". Research is invoked, not
  reported: no method, no sample, no categories, no date. Rejected, and the object
  (`sk_r22_0036`) says so in a caveat.
- **The Law of the Generic's sound-processing mechanism** is an elegant argument and reads as
  cognitive science. It is not: the only supporting figure is an uncited nine-to-one ratio of
  listening time to reading time, which is about media consumption and not about how names are
  retrieved. The caveat on `sk_r22_0037` says this.

### 3.2 Survivorship and hindsight are unmanaged in the source

Cases are chosen after outcomes were known. Successes are read back as compliance with the laws
(Starbucks, Subway, Toys "R" Us, FedEx, Volvo, Absolut, DeWalt, L'eggs, Olive Garden, Wrigley, Time
Inc.); failures as violation (Chevrolet, American Express, Levi Strauss, Crest, Miller Regular,
Bayer Select, Arch Deluxe, Holiday Inn Crowne Plaza, Boston Chicken, Atari, Newton, Little Caesars).

The counter-examples the laws most need are almost entirely absent: **no focused brand that failed
appears anywhere in the span**, and the extended brands that succeeded are each re-labelled rather
than counted —

| Counter-example | How it is disposed of | Page |
|---|---|---|
| Diet Coke | competitor had already line-extended | 7 |
| General Electric | all its competitors are equally weak | 36 |
| Vaseline Intensive Care | customers misread the descriptor as a name; "sometimes a company gets lucky" | 66 |
| Marquis by Waterford | conceded a big success, predicted to erode the parent later | 74 |
| Burned-out brands still trading | competitors are equally line-extended | 109 |

Four of those five are the same move, which this lane named `the_weak_competition_clause`
(`t_r22_0061`) so that a reader has a handle for the pattern. **No base rate is given anywhere in
the span**: the reader is never told how many focused brands were launched, how many extensions were
launched, or what proportion of each survived. No causal claim in this book is supported by a
controlled comparison. This is stated in `PROVENANCE.md` §6, in every YAML header, and as an
`extractor_observed` caveat on each affected object.

### 3.3 Strong practitioner opinion must not become universal truth

This was flagged in the brief as the easiest place in the run to breach the rule, and it is. The
book's prose is declarative, confident and quotable, and paraphrasing it faithfully produces
sentences that read like findings. Three defences were applied:

- Every `claim` field is written as *what the authors hold*, with the subject present — "the authors
  say", "they claim", "on their account". No claim field states a market fact in this project's own
  voice.
- `answer_type: source_position` is used for **eight** Q&A items, all of the ones that are about
  what these authors hold rather than about how markets are, and the `support` field of every one of
  the fifty items states what kind of claim the answer rests on.
- The distinction between the source's material and this lane's reading is marked in every object
  where both appear. `caveats[].origin` separates `source_stated` from `extractor_observed`
  throughout; `scs_r22_001`'s conflicts are marked as ours; `scs_r22_003`'s unifying test is marked
  as ours and explicitly not attributable to Ries & Ries.

### 3.4 `historical_claim` is pervasive

Every company example in this span is pre-2002 and the copy is a 2002 combined edition of a 1998
book. **No example anywhere in this directory has been updated with what happened afterwards.** That
was a deliberate refusal, not an oversight: this lane has no source for later events, and supplying
them from memory would be invention. It bites hardest on the Law of Mortality, where the authors
make a live forecast about Kodak and digital photography (pp. 106–108) — the forecast is recorded as
a forecast of its moment and its outcome is not stated. The Q&A bank's header says so, and
`qa_r22_0048`'s confounder list names "answering with what actually happened afterwards" as a wrong
answer.

The Internet material in the Introduction (pp. xiii–xvi) is the same case and is treated the same
way: the dotcom examples are recorded as the authors' post-hoc attributions of their period.

### 3.5 Subject boundary — brands and markets, not generative media

This book is about brand portfolios. It contains nothing about generative media and **no inference
about any model's capability has been drawn from it anywhere in this directory.** No `creative_ir`
binding exists (SPEC-01 was not supplied to this lane, and nothing here belongs in a creative IR
regardless). No production binding exists — the source describes no physical production act. No
remedy in `ontology-mappings.yaml` carries `generative_respecification` or `physical_production`;
every remedy is `human_edit` (a concrete organisational act) or `unknown` (a desired state in a
customer's mind with no stated procedure). Where the operational bindings reach at all toward
anything this project would run, the reach is marked `extractor_inference` and the
`applicability.limits` field says plainly that it is ours.

### 3.6 `figure_semantic_binding_lost`

**Recorded.** The copyright page advertises that this edition "combines *The 22 Immutable Laws of
Branding* and *The 11 Immutable Laws of Internet Branding* with added illustrations and text." No
figure survives in this PDF's text layer and **none was inspected**. Two chapters carry arguments
that are visual in character and are nonetheless conveyed entirely in prose in this copy:

- **Ch. 16, the Law of Shape** — a logotype proportion of roughly 2.25 units wide to 1 high, a
  comparison of Shell's wordless mark with Mobil's wordmark, and a claim about the Arby's
  cowboy-hat logo. The reader cannot see any of the marks.
- **Ch. 17, the Law of Color** — an argument about specific colours (Coca-Cola red, Tiffany blue,
  Burger King's yellow-and-orange, Hertz yellow / Avis red / National green) in a text file with no
  colour in it.

Every object in this lane is `source_support: text`; nothing claims `visual` or `text_and_visual`.
`sk_r22_0042` and `sk_r22_0043` carry `extraction_uncertainty: figure_not_inspected`. Whether the
illustrations would have added anything the prose does not is unknown and is not guessed at.

### 3.7 Locator hazards specific to this copy

- **Case 1** (verified authored folio). Printed page = PDF page − 17, and this lane re-verified it
  mechanically across all 256 markers as well as by eye on six rendered pages (`PROVENANCE.md` §2).
  Zero violations.
- **Chapter-opening pages are not a folio disagreement.** On a chapter opener the running head
  carries the *chapter number* and the folio is printed at the foot. Checked on printed pp. 13, 49
  and 83. Reading the head as a folio would have produced badly wrong locators.
- **Front matter carries roman folios (ix–xvi) which the marker file renders as negative integers
  (−7 … 0).** A negative integer is not an authored page. All three Introduction Q&A items cite the
  **roman** folio and contain no numeral at all, and the four Introduction knowledge objects set
  `page_start`/`page_end` to `null` with the roman range in `provenance.section`. Verified
  mechanically in §5 — those three items are the only ones with no page numeral, exactly as
  intended.

---

## 4. What was deliberately not extracted, and why

**Out of scope by the brief.** *The 11 Immutable Laws of Internet Branding* (printed pp. 111–230) is
bound into the same volume and was not extracted. It is a separate, later, and heavily period-bound
work, and the lane brief scopes this extraction to the 22 named laws. It is available-but-unextracted
material, not a gap. Nothing in this directory draws on it. Where the Introduction refers to its laws
by number (pp. xiv–xv), those references are recorded as part of the Introduction's method
(`sk_r22_0004`) and the Internet laws themselves are not defined anywhere here.

**Refused per the schema contract's extraction stance:**

- **Company-example lists carrying no mechanism.** The book contains many. The twenty-one "firsts"
  (pp. 14–15), the ten beer-leadership categories (pp. 32–33), the sixteen General/Standard/American
  corporate names (p. 61), the ten Nature's-something supplement brands (p. 63), the country-of-origin
  stereotype pairs (p. 92), the five brand-colour associations (p. 87). Each is compressed into a
  single `examples` entry on the object whose mechanism it illustrates, and none became an object.
- **Cross-chapter repetition.** The Law of Expansion is restated in whole or part in at least six
  later chapters. Chapter 22 is very largely a restatement of chapters 1 and 5. Restatements were
  folded into the original object with `repeated_within_source` rather than duplicated; `sk_r22_0048`
  exists only for the closing definitions and the survival caveat, and its caveat says so.
- **Polemical restatement.** "East Asia has a branding problem" (p. 48), "Hyundai makes everything
  except money" (p. 47), "the Nursing Home for Dying Brands" (p. 106), "it's like introducing New
  God" (p. 69). These are rhetorical closings, not claims. The East Asia one is the exception: it is
  recorded inside `sk_r22_0030` **because it shows how far the authors extend the law**, with a
  caveat saying the book does not support it.
- **The mistranslation anecdotes** (p. 96 — the Pepsi, Perdue and Coors slogans in Chinese and
  Spanish). Widely circulated marketing stories reproduced without any source. Recorded as a caveat
  on `sk_r22_0044` saying they carry no argumentative weight; this lane did not attempt to verify
  them and no object rests on them.
- **Biography and self-promotion.** The authors' client anecdotes were extracted only where a
  mechanism is stated (Act, Datastream, Maxion, Lotus Notes, the Swatch car); the surrounding
  narrative was not.
- **"You are a brand"** (p. xii), offered as personal-success advice. Recorded as a caveat on
  `sk_r22_0001` as outside anything the book examines; no object rests on it.

**Left unbound although extracted.** Most of this source has no honest binding target, and
`operational-bindings.yaml` names the four groups explicitly in its header: the growth-strategy
apparatus, the market-structure claims, the advertising and publicity economics, and every claim
about what customers believe. Per SCHEMA-CONTRACT §5.9 zero bindings would have been legitimate;
nine were written because nine objects concern either a checkable textual property of a name or
position, or how a body of conflicting practitioner advice should be held.

**A note on the advertising economics specifically.** They were left unbound partly because this
project holds a live source that reaches materially different conclusions about the same question.
Binding either side would be adjudicating a disagreement that this lane has no authority to
adjudicate. Leaving both recorded and neither bound is the correct output. See §6.

---

## 5. Self-check results

All four mandatory checks were run in code against the written files and the marker source.

### 5.1 Every YAML parses

All five YAML files parse under `yaml.safe_load`. Additionally checked mechanically:

| File | Result |
|---|---|
| `source-knowledge.yaml` | 49 objects, 49 unique ids; all 17 required keys present on every object; every `evidence.characteristics` value in the fixed vocabulary; every `source_uncertainty` and `extraction_uncertainty` in its vocabulary; every `intra_source_relations[].relation` in its vocabulary; **0 dangling `intra_source_relations` targets**; no `source_interpretation` claim with a null `interpretation_basis` |
| `source-concept-systems.yaml` | 3 systems; every `system_type` and origin marker valid; every `whole_system_claim` with `origin: extractor_synthesis` carries a non-null `interpretation_basis`; every member `sk_ref` resolves; every system carries `system_level_uncertainty` |
| `ontology-mappings.yaml` | 61 terms, 61 unique ids, 20 relationships, 9 concepts; every `kind: remedy` carries a valid `executable_by`; every relationship endpoint resolves; every concept child term resolves; **no `xs_` concept created**; **`same_failure_family` used zero times** |
| `operational-bindings.yaml` | 9 bindings (3 benchmark, 3 evaluation, 3 governance); every evaluation binding carries a valid `observation_unit`; every governance binding carries a permitted `governance_consumer`; every `target_path` null; no `creative_ir` and no `production` binding; every `source_knowledge_refs` / `source_system_refs` / ontology ref resolves; **`cross_source_supported` and `empirically_supported` used zero times** |
| `qa-bank.yaml` | 50 items, 50 unique ids; all 12 required keys present; every `answer_type`, `difficulty` and `knowledge_type` in the fixed vocabulary; `requires_application` boolean on every item; **`confounders` non-empty on every item**; no placeholder or `TODO` answers |

### 5.2 Locator assertion — every Q&A page inside the real span

Asserted mechanically. The real printed span was established from the marker file itself rather than
assumed: the file carries 256 markers, of which the positive printed folios run **1–240**. The lane's
extracted span is printed **3–110** (chapters 1–22) plus the roman-folio Introduction.

Digits were extracted only where they follow a `p.` / `pp.` marker, so chapter numbers, percentages
and dates elsewhere in a locator string cannot be mistaken for pages.

```
real printed span present in file: (1, 240)  | lane extracted span: (3, 110)
marker rows violating printed = pdf-17: 0        (all 256 markers checked)
QA locators: 87 page numerals across 50 items — ALL inside (1, 240). failures: 0
                                              — and all inside (3, 110). failures: 0
items citing roman front matter only (no numeral): qa_r22_0001, qa_r22_0002, qa_r22_0003
source-knowledge provenance pages outside extracted span: []
concept-system provenance pages outside extracted span: []
```

**Failures: 0. Fixes required: 0.**

**Spot-checks: 34 items** (the brief required ≥20). Each probed the actual page text for a
distinctive string the answer depends on — the epigram, the named case, or the quoted phrase.
**33 passed outright. The single flag was a false positive and was investigated rather than
patched:** `qa_r22_0005` cites printed pp. 5–6 for the teeter-totter passage, and the probe looked
for the plural on p. 6. The plural is the last line of p. 5 and the singular occurs twice on p. 6 —
the passage genuinely spans the break, so `pp. 5-6` is correct and no change was made. **Net: 34/34
verified, 0 locators corrected.**

### 5.3 `empirical_within_source` — count and justification

**ZERO. No object in this lane carries `empirical_within_source`.**

This is a finding about the source, not a gap in the extraction. The characteristic is reserved for
a measurement the source itself made and reported. Every quantitative statement in this span falls
into one of four categories, none of which qualifies. The four are set out case by case in
`PROVENANCE.md` §7; in summary:

1. **Third-party figures reported second-hand** — Kroger scanner data on 23,000 store items (p. 49);
   US vs Japanese and Korean top-100 profit margins (pp. 46–47); "a widely publicized study of
   twenty-five leading brands . . . in the year 1923" with no author, title or method (p. 32);
   Consumer Reports rankings (p. 35); wine consumption per head across four countries (p. 58).
   Someone else's data, provenance and method unstated.
2. **Market-share before/after pairs** — American Express 27→18 per cent, Levi's 31→19, Crest 36→25
   (pp. 4–5); Bayer Select's $26 million in a $2.5 billion market (p. 54). Two numbers each, no
   comparison group, no period alignment, no test of the asserted cause — and in the Bayer case the
   authors themselves say the decline predated the launch.
3. **Research invoked but not reported** — "our research indicates that 50 percent is about the
   upper limit" (p. 60); "years of observation have led us to this conclusion" (p. 35). No method,
   no sample, no data.
4. **Illustrative counts** — 45 per cent of national flags dominated by red (p. 86); 90 per cent of
   new grocery products are line extensions (p. 49); nine times as much listening as reading
   (p. 63). Uncited descriptive figures decorating arguments they do not test.

**The nearest miss, examined specifically and rejected:** the Consumer Reports small-car comparison
(p. 35), where the authors themselves line up quality rank against sales rank and report three
pairs. Rejected because the ranking is undated and unnamed beyond "recent"; the source of the sales
ranking is not given; three of sixteen ranked brands are reported and they are the three that make
the point; and no statistic is computed. It is recorded as `outcome_claimed` + `anecdotal` on
`sk_r22_0024` with an `extractor_observed` caveat saying exactly this, and `qa_r22_0020` asks about
it directly.

**Zero is the honest characterisation of a book that calls its contents immutable law.**

### 5.4 Application fraction

Computed in code over `qa-bank.yaml`:

```
requires_application: 19 / 50 = 0.38   (>= 1/3 required: PASS)
```

Answer-type distribution, against the contract's target mix:

| Type | n | Contract target |
|---|---|---|
| definitions / facts (`concept_definition`, `factual`) | 5 | ~20 % → 10 |
| mechanisms (`mechanism`, `repair`) | 10 | ~25 % → 12–13 |
| comparisons / trade-offs (`comparison`, `tradeoff`) | 6 | ~20 % → 10 |
| diagnosis / application (`application`, `failure_diagnosis`) | 16 | ~20 % → 10 |
| boundaries / exceptions (`boundary_condition`) | 5 | ~15 % → 7–8 |
| `source_position` | 8 | not in the target mix |

The mix is deliberately skewed away from the target in two places and the reasons are recorded here
rather than hidden. **Definitions are under-weight** because this source defines very little: it
asserts. **`source_position` is over-weight at eight items** because the contract's rule 7 requires
that answer type wherever an item is about what a source holds rather than about how the world is,
and with a source whose entire content is unmeasured practitioner assertion, that is the honest type
for every item that examines a claim's standing. Difficulty runs medium-heavy (1 easy, 35 medium,
14 hard); nothing here is easy to answer from general knowledge, which is the contract's rule 4.

---

## 6. Observations for cross-source review (NOT promotions)

**Read this section as a set of unadjudicated observations. Nothing here was resolved, no side was
softened, and no cross-source concept, term relationship or binding was created. Every one of these
requires Controller review and Audit-Gate lineage records that do not exist.**

The live Canon source this book most directly contradicts is
`canon/knowledge/current/binet-field-effectiveness-in-context-ch1` — Les Binet and Peter Field's
IPA-Databank analysis, which this lane read in full before extracting, as the brief instructed. The
two are **independent origins**: different authors, different traditions, no shared material, no
overlap. What follows is disagreement between independent sources, which is the most valuable thing
a Canon can hold, and it is recorded so that it can be held.

### 6.1 The role of advertising — the sharpest contradiction

- **Ries & Ries:** advertising cannot build a new brand at all; publicity does that (pp. 13–17). For
  an established leader, advertising is a defence budget and insurance against loss, explicitly *not*
  an investment expected to pay dividends, and they concede in the same chapter that it "may not pay
  for itself" (pp. 18–21). Its value is deterrence: making a competitor pay through the nose.
- **Binet & Field:** advertising efficiency and return are the units of analysis. ESOV Efficiency is
  reported at 0.73 in high-consideration categories against 0.60 in low; ROMI at 430 per cent
  against 418 per cent; optimum brand-to-activation budget splits are derived from a fitted curve
  and run from 61:39 to 74:26 depending on context.
- **The contradiction is not merely about numbers, it is about the kind of thing advertising is.**
  One source treats it as an expense that buys no growth; the other treats it as the investment that
  produces measured business effects. **Not resolved. Neither softened.**

### 6.2 What drives growth

- **Ries & Ries:** growth comes from narrowing focus, creating and owning a category, and expanding
  the category or the geography — never from broadening the brand's appeal. "Can a successful brand
  appeal to everybody? No" (p. ix); broadening the base and widening the appeal are named as the
  forces that undermine the brand.
- **Binet & Field:** penetration is always the main driver of growth in every context examined, the
  share of campaigns reporting very large penetration effects exceeds those reporting very large
  loyalty effects in every consideration context, and loyalty-first strategies are judged doomed to
  fail.
- **A frame mismatch must be stated so that a reviewer does not over-read the contradiction.**
  Ries's "narrow" is about *product and attribute scope*; Binet & Field's "penetration" is about
  *number of buyers*. Narrowing what a brand stands for and reaching more buyers are not strictly
  the same axis, and it is possible to do both. But Ries & Ries explicitly reject "widening the
  appeal" as a growth route and cap a brand's reasonable share at about half a market (pp. 42, 60),
  which is a real disagreement with a penetration-first prescription and not merely a terminological
  one. **Recorded as an observation with the mismatch flagged. Not adjudicated.**

### 6.3 Universality of the rules themselves

- **Ries & Ries:** the laws are immutable and apply equally everywhere, including to the Internet
  (p. xiv) and to any category whatever including commodities (p. xiii).
- **Binet & Field:** the report explicitly declines to be read as a set of universal rules, tells
  readers not to assume general learning applies automatically in all situations, and instructs them
  to flex the rules and take only what fits their context. Its whole subject is how best practice is
  *modified* by category context — consideration level, rational versus emotional decision-making,
  online research intensity.
- This is a disagreement about **what marketing knowledge is**, and it is arguably deeper than any
  disagreement about a particular tactic. **Not resolved.**

### 6.4 Whether category context changes the answer

- **Ries & Ries:** the same laws hold in every category; you can build a brand in any category as
  long as you follow them.
- **Binet & Field:** consideration is "the master context variable"; brand building is harder where
  decisions are rational and easier where they are emotional; optimum budget allocation shifts
  materially with context; efficiency moves in opposite directions as rational versus emotional
  consideration rises.
- **Not resolved.**

### 6.5 Evidential standard

Recorded because a reviewer comparing the two sources will need it. Ries & Ries: selected corporate
anecdote, zero measurement of their own, no base rates, no comparison groups, counter-examples
re-labelled rather than counted. Binet & Field: several hundred IPA Databank cases, quantified effect
sizes, fitted curves — **and stated limitations of their own**, including that the sample is drawn
from awards entries and biased toward successful campaigns, that every effectiveness magnitude is a
case author's own grading, that activation spend is under-reported, and that the optimum-split curve
broke down in some subsamples and was restored by removing a group.

**This asymmetry is recorded, not used to dismiss either source.** A source that reports its own
limitations is not thereby correct, and a source that reports none is not thereby wrong.
Practitioner assertion is a real category of knowledge and this is an articulate instance of it. The
observation for a reviewer is only that the two sources cannot be weighed as though they were the
same kind of claim.

### 6.6 Where they may not disagree — also not adjudicated

Ries & Ries prescribe a high price plus a "code word" that lets the buyer justify a prestige purchase
on other grounds (p. 27), and hold that rational argument about product superiority is discounted
("that's what they all say", p. 20). Binet & Field report that reducing price sensitivity by rational
persuasion almost never works and that emotional engagement is the route to a price premium. These
may be pointing at the same thing from two traditions, or may not be — Ries & Ries offer no notion of
emotional engagement and their mechanism is social signalling rather than affect. **This lane did not
decide, and deliberately did not record it as agreement.** Manufacturing cross-source agreement is
forbidden by the schema contract for the same reason as manufacturing disagreement.

### 6.7 What was done with all of this

Nothing beyond recording it here. Specifically:

- **No `xs_` cross-source concept** was created (SPEC-05 forbids it in this task).
- **No cross-lane or cross-source term relationship** was written in `ontology-mappings.yaml`; its
  header says why.
- **No binding carries `cross_source_supported`.**
- **No knowledge object references any other source.** A SourceKnowledge object cannot know it is
  contradicted any more than it can know it is corroborated.
- **The advertising-economics objects were left unbound**, precisely because binding either side
  would adjudicate this disagreement.
- `bnd_r22_007`'s `applicability.limits` states explicitly that its conflict-resolution rule covers
  conflicts *within* this source only, and that anything between sources requires Controller review.

---

## 7. Audit patterns recorded

| Pattern | Applies? | Note |
|---|---|---|
| `figure_semantic_binding_lost` | **yes** | §3.6 — Laws of Shape and Colour argue visually in a copy with no inspectable figures |
| `false_page_affordance` | no | Case 1 applies; the folio is real and was verified mechanically across all 256 markers and by eye on six rendered pages |
| `no_authored_page` | no | this is a PDF with authored folios, not a reflowable EPUB |
| unresolvable internal cross-reference | no | the book cross-refers by chapter number and name, never by page, so every internal reference resolves in this copy |
