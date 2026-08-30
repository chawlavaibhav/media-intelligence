# EXTRACTION NOTES — Seth Godin, *This Is Marketing*

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon and nothing here may
be described as accepted.

---

## 1. Counts

| | |
|---|---|
| SourceKnowledge objects | **29** |
| SourceConceptSystems | **3** |
| OperationalBindings | **5** (3 evaluation · 2 benchmark · 0 creative_ir · 0 production · 0 governance) |
| Ontology terms | **39** (20 problem · 10 remedy · 9 property) |
| Ontology concepts | **6** (4 source_specific · 2 canonical) |
| Q&A items | **37** |
| Q&A with `requires_application: true` | **13 — 35.1%** |

Source size: **328,396 characters** across 34 spine documents, twenty-three chapters plus an
author's note and a worksheet. Twenty-nine objects from twenty-three chapters — see §3 for why that
is the honest number rather than a shortfall.

## 2. Method

Read the whole book once, then a second pass with one question held against every candidate: what
would it mean for this to be false. That test is the whole method for this source, and §4 explains
why.

The unit of extraction is the section heading, not the chapter. Godin prints a heading every few
hundred words, so a twenty-three chapter book contains several hundred labelled units. Locators
therefore name chapter, chapter title and section heading, which is a genuinely fine locator with no
page involved.

## 3. The real idea count is lower than the page count

Godin restates heavily and the brief warned about it. Three ideas — "who's it for? what's it for?",
the smallest viable market, and "people like us do things like this" — appear in a dozen or more
places each, in the author's note, the executive summary, the chapter that introduces them, several
later chapters and the worksheet.

**Each was extracted once**, at the place where the mechanism is actually given rather than where
the phrase first appears, and the other appearances are recorded as `repeated_within_source` on the
evidence characteristics and nowhere else. Concretely:

- "Who's it for? What's it for?" appears in Chs. 2, 3, 4, 5, 13, 14, 16 and the worksheet. One
  object: `sk_god_0002`, anchored in Ch. 4 where the two failure modes are named.
- The smallest viable market has its own chapter and a second chapter named after it (Chs. 4 and 8).
  One object: `sk_god_0003`, anchored where the mass-means-average mechanism is stated.
- "People like us do things like this" appears from Ch. 2 onward and has its own chapter. One
  object: `sk_god_0015`.

Twenty-nine objects from a book of this length is therefore a refusal rate, not thin reading. §7
lists what was refused.

## 4. The aphorism problem, and how every object was tested

This is the central hazard for this source and it is different in kind from a figure problem or a
pagination problem. Godin writes in sentences that are memorable and assert nothing:

> *"Low price is the last refuge of a marketer who has run out of generous ideas."*
> *"Ideas that spread, win."*
> *"Culture beats strategy—so much that culture is strategy."*
> *"If they remark on it, then it's remarkable."*

The first three are slogans. The fourth is a definition disguised as a criterion. Recording any of
them as a claim would produce an object that cannot be wrong, which is the specific failure mode the
brief named.

**The test applied to every candidate: what would it mean for this to be false?** Where the answer
was "nothing", the candidate was refused. Where a maxim sits on top of a real claim, the claim was
recorded and the maxim was quoted in `source_terms` as the source's phrasing — never as the claim.
`sk_god_0029` is the worked case: "low price is the last refuge" is quoted as a source term, and the
claim recorded underneath it is the falsifiable one — that cheapness promises no change, and that
lowering a price lowers trust rather than raising it.

**Where the circularity could not be removed, it is recorded rather than hidden.** `sk_god_0026`
carries an `extractor_observed` caveat stating that "if they remark on it, then it's remarkable" is
definitional and therefore unfalsifiable as stated, and `bnd_god_003` says the binding can check for
a stated reason for the sharer and can never predict that sharing will occur. Two other objects
carry the same kind of note: `sk_god_0015` on "everyone always acts in accordance with their internal
narratives", which no behaviour can contradict, and `sk_god_0019` on the tension/fear test, whose
criterion is the maker's own feeling.

**`answer_type: source_position` is used where it is honest.** Three Q&A items are typed that way,
and a large share of the objects concern what Godin holds rather than how the world is; every one of
the 29 objects carries `practitioner_assertion`.

## 5. The one number in the book — why no `empirical_within_source`

**Verified in code: 0 of 29 objects carry `empirical_within_source`.** The brief expected zero and
asked for a justification of any use. There is one candidate and it was refused.

In the VisionSpring case (`sk_god_0011`) Godin reports that about a third of the people who came to
the table bought glasses, that he changed one thing, and that the change doubled the proportion
sold. That is a number, produced by him, in a situation he ran. Under a loose reading of
"the source reports its own measurement" it would qualify.

It was typed `outcome_claimed` and `anecdotal` instead, for reasons that are worth stating because
this is the closest call in the lane:

1. There is no comparison group. The two frames ran on different people at different times on the
   same afternoon, in the order he happened to try them.
2. There are no counts. "About a third" and "doubled" are the entire reported data.
3. There is no instrument. He was standing at a table forming an impression, and says so.
4. The explanation — that shopping is a risk affordable only to people for whom being wrong is not
   costly — is his interpretation constructed afterwards, not a hypothesis he set out to test.

`outcome_claimed` in the SPEC-03 vocabulary is exactly this: a result is claimed without controls.
`empirical_within_source` would have imported a rate into the corpus that the source does not have.
The object's caveat says so explicitly and adds that the result must not be used as a rate — which
matters especially here, since the point of the case is that the marketer's assumptions do not
transfer, and treating the number as transferable would contradict the claim it supports.

Two other objects carry `outcome_claimed` on the same basis: `sk_god_0009` (a reported fifty-per-cent
sales fall, unsourced, single case) and `sk_god_0027` (open and response rates from a company Godin
founded in the 1990s, reported by him, unaudited).

## 6. Adjacency to the live neighbour — Miller, *Building a StoryBrand*

The brief required reading `canon/knowledge/current/miller-storybrand-sb7` first so that Godin is
not recorded restating it. **This is recorded here as prose only.** No relationship, equivalence or
agreement between the two is asserted anywhere in this lane's YAML, and no ontology relationship
points at a live term. It is an observation about what to extract, not a claim about the world.

**What the live Miller extraction holds:** message *structure* — survival relevance, processing
cost, story structure as a comprehension aid, a seven-element framework, three levels of problem
with the internal one driving purchase, hero and guide, a message that names something the customer
wants, the grunt test, the BrandScript, comprehension speed beating product superiority.

**What was refused here because Miller already holds it in stronger form:** Godin's material on
telling a story well. He writes about stories constantly, but his story chapters are largely
exhortation, and his one structured treatment — the borrowed ten things good stories do, and the
story-of-self/us/now sequence he credits to Marshall Ganz — is either another author's framework or
generic. Extracting it would have added a thinner statement of what the corpus has.

**What Godin genuinely adds, and why the two are not the same book:** Miller answers *how a message
should be built*; Godin answers *who it is for and whether it should be built at all*. His
distinctive contribution is audience selection and exclusion (`sk_god_0001`–`sk_god_0007`), the
status and belonging machinery underneath choice (`scs_god_001`), the tension mechanism and its fear
boundary, positioning as a commitment that constrains later action, and the direct/brand separation.
None of that is message structure.

**One place the two look closest and are not.** Miller holds that a message must name something the
customer wants; Godin holds that performance and appeal come apart, so what the customer wants is
frequently not the thing the product does (`sk_god_0012`). Adjacent, and not the same claim. Recorded
here so the resemblance is not proposed again as a merge, and deliberately **not** recorded as a
`distinct_from` relationship, since that would be a cross-lane assertion against live Canon which
this task does not authorise.

## 7. What was deliberately not extracted

**Refused as exhortation and manifesto** — the whole author's note ("marketing is change", "how tall
is your sunflower", "it's not going to market itself"); Ch. 1's "you're not a cigar-smoking fat cat"
and "it's time"; Ch. 12's "perhaps you've seen the shift"; the whole of Ch. 22 ("the tyranny of
perfect", "the magic of good enough", "Help!"); and Ch. 23's closing address to the reader.

**Refused as ethics rather than mechanism** — Ch. 23's "Is marketing evil?". It is the one place
Godin addresses the moral status of the method, and it belongs in a discussion of whether to admit
this source at all rather than in a knowledge object. Recorded here as a deliberate omission, not an
oversight.

**Refused as career and self-help advice** — "authenticity versus emotional labor", "the authentic,
vulnerable hero", "your freedom", "marketing to the most important person", and the closing material
on the story you tell yourself. Real content, wrong layer: it is about the practitioner, not about
the work.

**Refused as repeated aphorism** — the executive summary in Ch. 2, which restates fifteen claims made
elsewhere in one page, and the "things marketers know" list beside it. Both are indexes to the book,
not sources of claims.

**Refused as anecdote with no mechanism** — the Penguin Magic, Be More Chill, Stack Overflow,
Trident Booksellers and Robin Hood Foundation case studies. Each is well told and each supports a
claim already stated elsewhere; none contains a mechanism the surrounding chapter does not.

**Refused as another author's framework** — the ten things good stories do (credited to Bernadette
Jiwa), the story of self / us / now (credited to Marshall Ganz), the thirteen rules and their
inversion (Saul Alinsky), the hype cycle (Gartner), the thousand true fans (Kevin Kelly), the long
tail (Chris Anderson). Where these frameworks are load-bearing for one of Godin's own claims they
appear inside its object with the attribution recorded in the caveats — the chasm inside
`sk_god_0024`, the true-fans idea inside `sk_god_0003`. They are not extracted as knowledge of this
source.

**Refused as period-bound business detail with no principle** — the funnel arithmetic worked in
stamps and clicks; the SEO discussion; the reading list; the logo advice; the long-tail T-shirt
example.

**Considered and refused on scope — one case worth naming.** Ch. 16's "And what about free?" is a
genuine mechanism: free is a different category of transaction rather than a lower price, because
like dividing by zero it scales to infinity, and the resolution is free ideas paired with expensive
expressions of them. It was not extracted because it is a business-model claim rather than an
audience-and-change claim, and the brief scopes this lane to the latter. This is the closest call in
§7 and is flagged rather than buried.

## 8. Bindings — why so few, and the categories examined and refused

Five bindings from twenty-nine objects.

**No `creative_ir`.** None attempted. Nothing about a Creative IR path is inferred from a trade book
about positioning, and the task forbids it.

**No `production`.** There is no production act in this book. Godin's remedies are decisions and
postures — choose these people, claim these two axes, refuse to measure this, keep the promise. The
two that come closest to an act are commercial (buy or do not buy the ads) and design-directional
(send a signal that resembles one already trusted), and neither is an act performed on an asset.
This is why the ontology's remedy terms carry `[human_edit]` rather than `[physical_production]` —
the opposite of the Carroll lane in this run, and for a real reason.

**No `governance` — examined and refused.** The nearest candidate is `sk_god_0013`, better is not a
single scale, which resembles `evidence_interpretation` until you notice that it is a claim about
how buyers rank offerings, not about how this project weighs evidence. A second candidate,
`sk_god_0015`'s instruction to define "us" before anything else, resembles `taxonomy_governance` and
is not: it governs an audience definition, not the admission of terms into an ontology. Under
SPEC-04's guard against a junk drawer, a candidate fitting none of the six permitted consumers is
not a governance binding, so both are left unbound.

**Two benchmarks, and one of them is unusual.** `bnd_god_005` is the only place in this lane group
where a source generates a genuine minimal pair by construction: the same offering placed at
opposite extremes of the same two axes, with Godin's own worked case being two music teachers in one
neighbourhood differing only in claimed position. `bnd_god_001` binds the worksheet and the promise
template, which specify a brief directly.

**No model capability is inferred from this source anywhere.**

## 9. Hazards, and how each was handled

**Strong opinion must not become universal truth.** All 29 objects carry `practitioner_assertion`
and none carries a characteristic implying measurement. Three Q&A items are typed
`source_position`, and the objects that carry Godin's most confident claims — the primacy of status, the case against
price competition, empathy as theft, the status of "better" — all carry `practitioner_assertion` and
an `extractor_observed` caveat separating the argument from the rhetoric.

**`historical_claim` where the examples are of their period.** Twelve of 29 objects carry it. The
period-bound material includes: the named social platforms and the sharecropper argument; the 2018
online advertising duopoly and its share of global spend; the CPM figures; a specific ride-hailing
company's early posture; a music-streaming playlist's subscriber counts; a workplace-tool launch; a
department-store episode of the early 2010s; the Yellow Pages and Yelp comparison; and the camera
of the retail environment generally. In every case the caveat separates the structural claim, which
may survive, from the example, which will not.

**`culturally_bounded` where the claim is about one culture.** Five objects, including the whole
"people like us" apparatus, the crickets-and-beef illustration, the affiliation-versus-dominion
material and the claim that modern urban and internet culture runs on affiliation.

**Survivorship.** Named on `sk_god_0003` and made into a Q&A item (`qa_god_0035`) that requires the
reader to state it: every case supporting the smallest viable market is a survivor, and projects
that narrowed and stayed small cannot appear in a book of this kind.

**Godin's own failure case was kept.** `sk_god_0024` records the HugDug project he reports failing,
with his own diagnosis. It is the single most useful piece of evidence in the book precisely because
it is the only case selected on something other than success.

## 10. Internal tensions preserved, not resolved

1. **The tension mechanism against its own fear boundary.** `sk_god_0019` fences the method against
   coercion and fear; `sk_god_0020`'s strongest case is a workplace tool that spread because people
   not using it were being talked about behind their backs and excluded from projects. Recorded as a
   `conflicts` entry in `scs_god_001` and as a caveat on the object.
2. **Choose the audience first, but do not ask them.** `sk_god_0001` requires selecting the audience
   before building; `sk_god_0012` says the crowd invents nothing and people are terrible at
   inventing ways to address their wants. Recorded as a `source_stated` caveat on `sk_god_0001`.
3. **Typecast them, and treat them as individuals.** `sk_god_0008` carries both of Godin's
   statements, unreconciled, as he leaves them.
4. **Serve the smallest viable market, whose wants are the opposite of the mass market's.** Recorded
   as the trade-off in `scs_god_003` and made into a Q&A item (`qa_god_0034`) that also requires the
   reader to name what he does not resolve — that offerings without a network effect have no bridge.

## 11. Self-check results

1. **All five YAML files parse** under `yaml.safe_load`.
2. **No page number anywhere.** 29/29 objects have `page_start` and `page_end` null; 37/37 Q&A
   locators contain no `p.`/`pp.`/`page N` construction; asserted in code by regex over every
   locator string. 0 failures, 0 fixes required. Audit pattern `no_authored_page` recorded.
   Unlike the Carroll lane in this run, this file carries **no** `false_page_affordance` — the book
   contains no internal page cross-references at all.
3. **Every reference resolves.** All `source_knowledge_refs`, `source_system_refs`,
   `failure_ontology_refs`, `repair_ontology_refs`, `members[].sk_ref`, `children_terms`,
   `relationships[].from/to` and every `intra_source_relations[].target` checked in code. 0 dangling.
4. **`requires_application` = 13/37 = 35.1%**, computed in code. Required minimum one third: **met.**
   The first draft came in at 31.4%, below the floor. It was corrected by **adding two genuinely
   applied items** (`qa_god_0036`, the "why are they right" exercise; `qa_god_0037`, the method
   applied to a single-person internal audience) rather than by relabelling existing items, which
   would have been the dishonest fix.
5. **Every `kind: remedy` term carries `executable_by`.** Checked in code: 0 missing. None carries
   `generative_respecification`.
6. **No `xs_` concept and no `same_failure_family` relation** created.
7. **No `empirical_within_source`** on any object. Checked in code: 0. The one candidate is
   documented in §5.
8. **Honest count, not target count.** The range was 20–35 objects and 25–40 Q&A. This lane sits at
   29 and 37 — mid-range on objects despite the book being three and a half times the length of the
   Carroll source in this run, which is the point: the idea count is lower than the page count, and
   §3 and §7 are the evidence.

## 12. Write boundary

Every file written by this lane is inside
`canon/experimental/book-expansion-qa-v1/godin-this-is-marketing/`. The `PROVENANCE.md` found in
this directory from an earlier attempt was **read, checked against the source and kept**: its
fingerprints, sizes, spine counts and character count all verify, and its overlap and access
sections are sound. It was amended in one place only — §3, to state precisely which later chapters
contributed to objects anchored earlier, so the span is neither overstated nor understated. Nothing
under `canon/knowledge/current/**`, `canon/audit/**`, `coordination/**` or any SPEC file was
created, edited or deleted. Nothing was committed.
