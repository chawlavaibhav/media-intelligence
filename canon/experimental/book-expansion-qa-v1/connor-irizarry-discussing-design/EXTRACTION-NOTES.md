# Extraction notes — Adam Connor & Aaron Irizarry, *Discussing Design*

**EXPERIMENTAL — NOT LIVE CANON.** A lane of the non-merge `book-expansion-qa-v1` expansion.
Nothing in this directory is accepted Canon and nothing here may be described as accepted.

---

## 1. What was extracted, and the counts

| Artifact | Count |
|---|---|
| SourceKnowledge objects | **55** |
| SourceConceptSystems | **6** |
| OperationalBindings | **12** (11 `governance`, 1 `evaluation`) |
| Ontology terms | **76** (27 problems, 28 remedies, 15 properties, 6 entities) |
| Ontology relationships | 16 |
| Ontology concepts | 9 (all `source_specific_concept`; no `canonical_concept`, no `xs_`) |
| Q&A items | **51** |
| Q&A `requires_application: true` | **20 — 39.2%** |

The brief's target was 35–55 SourceKnowledge objects and 45–65 Q&A pairs. Both are inside range.
The knowledge count is at the top of its band because the book is unusually dense in the exact
material this project lacks; a first pass produced 66 candidate objects and eleven were consolidated
or dropped (see §6).

## 2. Locators — Case 1, verified

The supplied text declares `printed page = PDF page - 18 (folio agreement on 178 pages)`. The
previous attempt verified the offset on seven rendered pages; this pass rendered three more —
PDF 51 → folio `33`, PDF 77 → folio `59`, PDF 81 → folio `63` — all agreeing. **Ten for ten. No
page was found where the printed folio disagrees with the marker.** `PROVENANCE.md` carries the
full table.

The real printed span was enumerated mechanically from the marker set: **positive printed pages
1–187, 182 of them, with 20, 76, 142, 174 and 180 absent** (blank versos before chapter and
section openings). Front matter carries negative marker numbers because the folio there is roman;
**nothing in this extraction cites a negative or roman-numbered page.** Index pages (181–187) are
not cited. Every locator falls inside printed 1–179.

## 3. Self-check results

All five checks below were run in code, not by eye. The script is reproduced in the shell history
of this session; each result is stated here with its number.

**1. Every YAML parses.** All five files load under `yaml.safe_load`. ✅

**2. Locator span assertion.** Only numbers following a `p.`/`pp.` marker were treated as pages, as
the shared validator does. **103 page numbers appear across the 51 Q&A locators. All 103 are inside
the real span and none names one of the five absent pages.** The 55 SourceKnowledge
`provenance.page_start`/`page_end` values and the 6 SourceConceptSystem ones were checked the same
way: **all inside the span.** ✅

**Spot-checks: 47 items were checked against the cited page** — a distinctive phrase from each
answer was normalised and searched in the text of the pages that item cites. **47 of 47 confirmed.**
One (`qa_disc_0029`) initially reported a miss, which turned out to be an error in the checking
script rather than in the locator: the phrase "focus your presentation on what isn't obvious or
can't be seen easily" is on printed p. 122, and the item's locator already reads `printed pp.
121-122`; the first script searched only the first page of each range. Re-run over the full cited
range, it confirms.

**Locators corrected: zero.** No Q&A locator, and no `provenance` page range, required a change.

**3. Application fraction.** Computed in code: **20 / 51 = 0.3922**, which is ≥ 1/3. ✅

**4. Prohibitions.**
- No `xs_` concept and no `cross_source_concept`: verified by scan. ✅
- No Creative-IR path or product vocabulary in SourceKnowledge: the strings `creative.`,
  `entities.`, `production_ir`, `normalized_request`, `Capability Registry` and `rank-1 element`
  appear in none of the five files. ✅
- No `human_workflow` target type: it appears nowhere. All 12 bindings use `governance` or
  `evaluation`, both SPEC-04 target types. ✅
- `same_failure_family` is not used. ✅
- Every `kind: remedy` term carries `executable_by`; **28 of 28**. Values used: `human_edit` (26)
  and `unknown` (2). Neither `generative_respecification` nor `physical_production` is assigned to
  any remedy. ✅
- Enum conformance: every Q&A `answer_type`, `difficulty` and `knowledge_type` is from the fixed
  vocabulary; every `confounders` list is non-empty; every required field present; no duplicate
  `qa_id`. ✅
- Every binding `source_knowledge_refs`, `source_system_refs`, `failure_ontology_refs` and
  `repair_ontology_refs` resolves inside this lane; every SourceConceptSystem `sk_ref` resolves;
  every `intra_source_relations` target resolves. ✅
- No `cross_source_supported` or `empirically_supported` `evidence_basis`. ✅

**5. Q&A mix.** mechanism 13 · application 11 · concept_definition 6 · failure_diagnosis 5 ·
boundary_condition 4 · repair 4 · comparison 3 · source_position 2 · tradeoff 2 · factual 1.
Difficulty: 34 medium, 12 hard, 5 easy. This is heavier on mechanism and lighter on plain facts
than the contract's suggested mix, which reflects the source: it is almost entirely mechanism and
almost devoid of facts, and forcing a factual quota would have meant inventing trivia.

---

## 4. Hazards, as required

### 4.1 Practitioner methodology, not measured findings — with the count

**`empirical_within_source` is used ZERO times across 55 objects.** That is not a shortfall; it is
the finding. The book reports **no measurement of its own**: no study, no experiment, no count, no
controlled comparison of outcomes appears anywhere in it. Its single footnote is a dictionary
definition of "collaborate" (printed p. 48). Every claim is `practitioner_assertion`, `argued`,
`anecdotal`, or some combination, and 54 of the 55 objects carry `mechanism_given` because the
authors do reliably explain *why* they think something works — they simply never show that it does.

Four passages come close enough to sound empirical and none of them is:

- **"very few people are able to answer, and those who do rarely answer with the same objectives"**
  (printed p. 56). Reported from consulting experience with no sample, count or method. It is the
  most empirical-sounding sentence in the book and it is recorded in `sk_disc_0022` as an
  `extractor_observed` caveat saying exactly that.
- **"less than five percent of a team's utilization"** (printed p. 82, Russ Unger's sidebar). A
  cost estimate for a practice, not a measured effect of it — and a different practitioner's.
- **"more than 70 people in attendance"** (printed p. 105). An anecdote's headcount.
- **"research that it doesn't work"** on the feedback sandwich (printed p. 153). **No citation is
  given, and the book contains no references section, no endnotes and no bibliography.** This is
  flagged inside `sk_disc_0051` and inside the `support` field of `qa_disc_0050`, because an
  uncited appeal to research is exactly the thing a downstream reader would otherwise inherit as
  established.

The same applies to the book's central cognitive premise — that the brain does not consciously
think analytically and creatively at once (printed pp. 11 and 113). It is asserted without
citation, it carries the weight of the rule against problem solving and of the divergent/convergent
structure, and it is labelled in `sk_disc_0007` as the authors' working model rather than as an
established finding.

### 4.2 The extrapolation is ours and lives only in bindings

*Discussing Design* is about synchronous conversation between people about interface work. Its unit
is a sentence said by one person to another in a room; its remedies are acts people perform; its
diagnostics assume the speaker is present and can be asked a follow-up question. Applying any of it
to an automated evaluation pipeline is **our** extrapolation.

It appears **only** in `operational-bindings.yaml`, and **all twelve bindings carry
`evidence_basis: extractor_inference`.** Not one is `derived_from_source`, because in no case is the
target the source's own target — a judgement was made that calling any of these "derived" would
overstate the fit. Each `applicability.limits` states the specific gap for that binding rather than
repeating a boilerplate. Nothing of this kind appears inside any SourceKnowledge `claim`.

Large parts of the source are **deliberately left unbound**, and the binding file says so at the
top: everything about feelings, defensiveness, culture, trust and morale; the session mechanics that
govern how a meeting is run; and the process-shape material about how an organisation schedules
work. Zero bindings would have been a legitimate outcome. Twelve were written because twelve
knowledge objects here are about how a judgement is formed, recorded, weighted and disputed, which
is what the permitted governance consumers cover.

**Governance consumers used:** `evidence_interpretation` (6), `conflict_resolution` (2),
`rule_application` (2), `taxonomy_governance` (1). The single non-governance binding
(`bnd_disc_006`) is `evaluation` with `observation_unit: asset_set_over_time`, because the source's
too-much-critique cues are properties of a series of revisions rather than of any single artifact.

### 4.3 Remedies act on people

All 28 `kind: remedy` terms carry `executable_by: human_edit` — every remedy in this book is
something a person does in a conversation — except two that carry `unknown`:

- `t_disc_0054 establish_product_focused_intent` — the source names the required intent on both
  sides and then says only "ensure that you're going in with the right intent". There is no
  procedure.
- `t_disc_0055 make_the_process_allow_iteration` — a required state of the organisation with no
  executable route to it beyond practising and accepting incremental change.

Marking those two `unknown` rather than `human_edit` is deliberate. They are the two places where
the book prescribes an outcome and not an action, and flattening them into `human_edit` would have
made the ontology look more operational than the source is.

### 4.4 Figures — `figure_semantic_binding_lost`

Four pages were rendered at 110 dpi and read directly, chosen because a claim depended on them:

| PDF page | Printed | Figure | What the figure carries that the prose does not |
|---|---|---|---|
| 51 | 33 | Figure 2-1 | The four questions as an **ordered downward arrow flow**. The prose enumerates them; the sequencing is visual. `sk_disc_0015` is `source_support: text_and_visual` with `inspected.figures: [Figure 2-1]`. |
| 77 | 59 | Figure 3-3 | An example persona — its actual sectioning (Consumption / Sharing / Learning behaviours, plus an "In Fred's words" block). The prose says only "half-page, succinct". |
| 81 | 63 | Figure 3-5 | Example goals, all numeric and percentage-shaped. Stronger than the prose. |
| 81 | 63 | Figure 3-6 | **The important one.** Example principles written as *first-person user constraints with a reason attached* — "Be where I am. Don't be just another place I have to go log into…". The prose says principles should be "somewhat specific" and gives no form. Recovering this changed `sk_disc_0024` and `qa_disc_0010`. |

**`figure_semantic_binding_lost` is recorded here for four figures that were NOT rendered and whose
content the prose does not carry.** The three objects that touch them are marked
`extraction_uncertainty: figure_not_inspected`:

- **Figure 5-3** (printed p. 120) — a reproduced critique-notification email. The specific wording
  of a good pre-send message exists only in the image. `sk_disc_0038` is marked; no claim in this
  extraction depends on the wording, and `qa_disc_0028` deliberately describes the handling
  procedure rather than the email's text.
- **Figure 5-4** (printed p. 123) — the improved user-perspective presentation framing. The prose
  states the rule; the demonstration of what it looks like is only in the figure. `sk_disc_0039`
  is marked.
- **Figures 6-2 and 6-3** (printed pp. 154–155) — a bad feedback sandwich contrasted with a
  balanced discussion. The prose describes the failure in general terms; the actual contrasting
  wording is only in the images. `sk_disc_0051` is marked.
- **Figure 6-1** (printed p. 152) — framing questions on the design rather than the designer.
  `sk_disc_0050` is marked.

Figure 3-4 (an example scenario, printed p. 60) is in the same category but no object depends on
its content, so it is noted here and nowhere else.

### 4.5 Sidebars are other people's assertions

Six named practitioners contribute signed sidebars: Kevin M. Hoffman with Chris Cashdollar
(printed pp. 31–32), Kim Goodwin (61–62), Veronica Erb (73–74), Russ Unger (80–82), Jeff Gothelf
(88–90) and Brad Nunnally (125–126). Two of them carry material strong enough to be their own
objects — `sk_disc_0025` (Goodwin) and `sk_disc_0047` (Nunnally) — and **both say in an
`extractor_observed` caveat that this is a different practitioner's assertion carried inside this
book, not the authors'.** The corresponding Q&A items (`qa_disc_0012`, `qa_disc_0039`) name the
contributor in the question or the answer and list mis-attribution to Connor & Irizarry as a
confounder. Hoffman/Cashdollar and Erb are cited only inside caveats on the authors' own objects,
attributed. Unger's and Gothelf's sidebars produced no object (see §6).

---

## 5. Where I was tempted to over-claim, and did not

Recorded because the brief asked for it, and because each of these was a live decision rather than
a hypothetical.

1. **The three elements as a validity test.** The strongest temptation in this extraction. It is
   very easy to slide from "a finding that names the element, the objective and the why is usable"
   to "…is more likely to be correct". The source never says that and offers nothing that would
   support it. `bnd_disc_001` says so explicitly in its own rationale — "it does not make the
   complete ones correct" — and the `applicability.limits` adds that treating a rejected finding as
   false rather than as under-specified would go beyond both the source and the binding.

2. **A saturation threshold for review loops.** `sk_disc_0028` gives four cues for too much
   critique. Turning three of them into an inspectable property of a revision series was already a
   stretch; attaching a number to it would have been invention. `bnd_disc_006` states that nothing
   in the source supports a specific threshold and that none should be attributed to it. The fourth
   cue — critique used for validation — is a motive, is not observable here, and is **excluded from
   the binding** rather than approximated.

3. **The "more often the answer should be 'no'" heuristic as a metric.** It is the sharpest
   reusable idea in the book and it is dimensionless: the source gives no rate, and no test at all
   for the opposite failure of an over-narrow criterion. `bnd_disc_005` reports the rate and the
   source's direction of concern and explicitly refuses to derive a threshold.

4. **The four prioritisation considerations.** These look like a method and they are labelled by
   the authors themselves "(As Adam says, this is completely unscientific.)" They are recorded in
   `sk_disc_0046` because they are what the source says, but **`bnd_disc_010` binds only the
   record-the-declination step and states in its limits that the agreement heuristic has no
   protection against amplifying a shared blind spot and should not be adopted on this source's
   authority.**

5. **The cognitive premise.** It would have been easy to write "the brain cannot analyse and
   generate simultaneously" as a claim. It is written as *the authors' working model*, with an
   `extractor_observed` caveat in `sk_disc_0007` and again in `sk_disc_0035`, because it is asserted
   without citation and carries more of the book's structure than any other single sentence.

6. **The uncited "research" on the feedback sandwich.** Repeating "research shows the sandwich
   doesn't work" would have laundered an uncited claim into an apparent finding. `sk_disc_0051` and
   `qa_disc_0050` both state that no reference is given and that the book has no bibliography.

7. **Kim Goodwin's belief condition as the authors' own.** It qualifies their argument and is
   arguably better than it. Attributing it to them would have made the book look more careful than
   it is. It is attributed to her throughout.

8. **Generalising "when not to use Design Studio".** The five conditions transfer well beyond that
   one methodology, and I wanted them to be the authors' general boundary conditions. They are not
   — they are written about one named technique. `sk_disc_0031` carries an `extractor_observed`
   caveat saying the generalisation is ours.

9. **An `evaluation` binding on the three elements.** Tempting, because it would have looked more
   operational. But `evaluation` requires an `observation_unit`, and the unit here is a *judgement*,
   not an asset, a frame or a shot. Forcing `whole_asset` would have been a false fit, so it is a
   `governance` binding with `evidence_interpretation` instead. Only one binding in this lane has a
   genuine observation unit.

---

## 6. What was deliberately not extracted

Per the brief's refusals — organisational anecdote with no mechanism, meeting logistics, tool
recommendations, culture exhortation — the following were read and left out:

- **Remote-working tooling** (printed pp. 71–74): video chat, screen sharing, BoardThing,
  StormBoard, document cameras, iPevo. Tool recommendations of 2015, no transferable mechanism. The
  one general claim — "collaboration is a mindset, not a by-product of co-location" — is
  exhortation.
- **Veronica Erb's sidebar** (73–74) on remote work eroding self-confidence. Genuinely interesting
  and genuinely about people's psychology; no mechanism about judgement. It survives only as a
  caveat inside `sk_disc_0050`.
- **Russ Unger's "Continuous Critique" sidebar** (80–82) — a 12-week cadence of one-on-ones, group
  sessions and all-team meetings. Scheduling logistics.
- **Jeff Gothelf's Lean/Agile sidebar** (88–90). Its usable content ("one designer tasked with
  everything cannot seek out critique") is an organisational staffing observation.
- **The Design Studio recipe** (97–101): three charrettes, 6-up paper, black markers, red and green
  pens, painters tape, eight minutes then three then four-to-five. Supplies and timings. The two
  parts that carry mechanism were kept elsewhere: the boundary conditions (`sk_disc_0031`) and the
  divergent-then-critique-then-convergent structure (`sk_disc_0030`).
- **The Mini Creative Brief** (64–65) as an object. It is a container for the foundation rather
  than a claim about judgement; it survives as ontology term `t_disc_0053` only.
- **Practising critique, finding advocates, starting with a colleague over coffee** (69–71, 170–172)
  and most of Chapter 7, which restates earlier chapters. Chapter 7 is cited nowhere in the Q&A
  except as corroboration for the three-form taxonomy.
- **Acknowledgments, foreword, the downloadable cheat sheet, the index.**

Eleven candidate knowledge objects from a first pass were consolidated rather than dropped —
selfish and untimely critique into one object, "everyone is a critic" merged with the quiet-participant
diagnostic, the four session rules kept but the strengths/quota material folded into two objects.
`scs_disc_003` notes the one place where this consolidation makes the extraction's shape differ
from the source's: the book names **four** characteristics of bad critique and this lane carries
them in **three** objects.

---

## 7. Audit patterns

- **`figure_semantic_binding_lost`** — recorded, §4.4, for Figures 5-3, 5-4, 6-1, 6-2 and 6-3.
  Four figures that *were* rendered are recorded as inspected and their objects upgraded to
  `source_support: text_and_visual`.
- **`false_page_affordance`** — **not applicable.** The folio is real and was verified on ten
  pages.
- **`no_authored_page`** — not applicable. This is a paginated PDF, Case 1.
- **Unresolvable internal cross-reference** — not applicable here. The book cross-references by
  chapter ("see Chapter 5"), not by page, so no reference was left dangling. One cross-reference is
  simply wrong in the source: printed p. 69 sends the reader to "Chapter 4 for a more in-depth
  explanation of the rules for critique", but the rules are in Chapter 5. Noted, not corrected in
  any locator, and no object depends on it.
- **Uncited appeal to external research** — no vocabulary term exists for this in the audit set, so
  it is named here in prose: printed p. 153, the sandwich-method claim. The book has no references
  section of any kind.

## 8. Cross-source

**No cross-source concept, no cross-lane ontology relationship, and no independence claim.** The one
resemblance a reviewer should look at — Catmull's "good note" against this book's three elements,
and the fact that this book cites Pixar's Dailies at printed p. 83 — is recorded as prose in
`PROVENANCE.md` under "Observations for cross-source review (NOT promotions)" and nowhere else. It
is an observation. Neither source is evidence for the other.
