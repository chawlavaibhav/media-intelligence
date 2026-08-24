# CANON-003 — Lane C issue file

**Lane C:** advertising / persuasion. Books 13 (Hopkins, *Scientific Advertising*), 14 (Heath &
Heath, *Made to Stick*), 15 (Sutherland, *Alchemy*).
**Branch:** `work/canon-003-c` · **Method:** frozen, per `canon/tasks/CANON-003.md` and the parallel
execution amendment. Nothing in this file has been applied. Every proposed fix is a proposal.

This file records issues found by Lane C only. Per the isolation rule it does not read other lanes'
new findings, and it is not written against the pre-parallel batch ledger as a checklist. Where an
issue looks like it may repeat something the pre-parallel handover checkpoint already reported, that
is said plainly and the pre-parallel item is treated as a possible earlier sighting, not as a
confirmed count.

**How to read the counts.** "Distinct books" means books *in this lane* showing the issue. Combining
lanes and the pre-parallel ledger into real recurrence counts is the integrator's job, not this
file's.

---

## Book 13 — Claude C. Hopkins, *Scientific Advertising*, ch.1–7

Fresh checkpoint: `1222919`. Historical comparison: **none exists** (see C-12).

---

### C-01 — The evidence vocabulary cannot tell "the source reported a measurement" apart from "the source said one was made"

**Status:** OBSERVED · **Layer:** source fidelity / evidence characteristics · **New in Lane C** ·
**Distinct books: 1**

**What it is.** SPEC-03 offers `empirical_within_source`, defined as "the source reports its own
measurement". Hopkins constantly says measurement happened — "we prove them by repeated tests", "the
mail order advertiser knows that waste by tests", "it has never failed to prove out so in any test we
know", "whenever we do we invariably find" — and almost never says what any test returned. Across
seven chapters the reported results amount to three unattributed cost-per-reply figures (85 cents,
$14.20, 41 cents), one before-and-after picture test, and one conversion rate (about nine in ten).
A described record of roughly 2,000 keyed headlines is mentioned and no result from it is given.

**Why it matters.** The vocabulary has one slot for two very different facts. Marking these claims
`empirical_within_source` would credit the book with evidence it did not supply. Leaving the
characteristic off records them as bare assertion and loses the fact that the source is
*claiming* an empirical basis, which is itself important information about the source.

**What was done instead, under the frozen method.** `empirical_within_source` was applied only where
a measurement result is actually reported. Every asserted-but-unreported measurement was written
into a caveat with `origin: extractor_observed`. Nothing was upgraded and nothing was dismissed.

**Practical consequence if unchanged.** The distinction survives in prose and nothing can count it.
A later question like "which of our sources claim to be evidence-based, and which of those actually
report evidence?" would have to be answered by re-reading every caveat by hand. That question is
directly relevant to how much weight a source should carry.

**PROPOSED — not applied.** A second characteristic alongside `empirical_within_source`, for
"the source asserts that measurement was performed but reports no result". This is a schema change
and a human approval trigger; it is recorded here only so the integrator can weigh it against the
other lanes.

---

### C-02 — A set of claims unified by one shared warrant has no honest `system_type`

**Status:** OBSERVED · **Layer:** systems (SPEC-03 SourceConceptSystem) · **New in Lane C** ·
**Distinct books: 1**

**What it is.** Chapter 4 issues a set of copy rules — small type, every line used, no borders, a
coupon, pictures that earn their space, tell the complete story, returns scale with filled space.
They do not interact with each other, they are not ordered, and none causes another. What holds them
together is that every one of them is justified by the same single argument: mail order advertising
is continuously measured, so whatever mail order advertisers do universally must have been selected
by results.

The available `system_type` values are `trade_off_set`, `priority_order`, `sequence`,
`decision_framework`, `causal_model`, `interacting_set`, `mutual_qualification`. None means "these
share one evidential warrant". `interacting_set` was used as the least assumptive available choice
and the mismatch was written into `system_level_uncertainty` rather than resolved.

**Why it matters.** The shared warrant is the most important property of this group. Every member is
exactly as sound as the warrant, and the warrant here is weak — it is an inference from observed
practice, not a reported comparison. Only one member (the incubator picture) carries an actual
before-and-after result.

**Practical consequence if unchanged.** Retrieving one prescription on its own detaches it from the
only thing supporting it, and the object looks like an independently established rule. That is
precisely the failure the system layer exists to prevent, and the layer currently cannot name it.

**PROPOSED — not applied.** A `shared_warrant_set` system type, or a `warrant` field on the system
that names what supports the members jointly. Schema change; approval trigger; recorded only.

---

### C-03 — A claim can be plainly stated, unhedged, and structurally impossible to disprove, and nothing records that

**Status:** OBSERVED · **Layer:** evidence · **New in Lane C** · **Distinct books: 1**

**What it is.** `source_uncertainty` records whether the source hedges. Three claims in this book do
not hedge at all and still cannot be tested:

- "Now the only uncertainties pertain to people and to products, not to methods." Any failure can be
  assigned to the product or the public, because method failure has been defined out of the
  available explanations.
- "Any studied attempt to sell, if apparent, creates corresponding resistance." Effective craft is
  by definition craft the reader did not notice, so any counter-example is reclassified rather than
  counted.
- "It has never failed to prove out so in any test we know." The qualifier confines the evidence to
  the author's own unreported records.

**Why it matters.** These read as the most confident claims in the book. Confidence and testability
point in opposite directions here, and the schema currently records only the first.

**Practical consequence if unchanged.** Each was captured in a caveat, so nothing is lost for a human
reader. But an unfalsifiable claim and a well-supported one are indistinguishable to anything that
reads the structured fields.

**PROPOSED — not applied.** An `extractor_observed` value on `source_uncertainty`, or a separate
testability note. Recorded only.

---

### C-04 — Evidence *for* the current design: a self-contradicting source was representable without strain

**Status:** OBSERVED · **Layer:** systems, source fidelity · **Evidence against an earlier concern** ·
**Distinct books: 1**

Hopkins contradicts himself three times inside seven chapters, and in each case the contradiction is
load-bearing rather than incidental:

1. Chapter 1 rules that cost per reply is **not** a final measure and that conclusions must rest on
   cost per customer. Chapter 4's headline evidence is stated entirely in cost per reply.
2. Chapter 1 rules that only some findings generalise beyond their product line. Chapter 4
   generalises mail order copy practice to all advertising without applying that test to any of it.
3. Chapter 1 says the traced-return method replaced the accumulation of unmeasured practitioner lore.
   Chapter 6 says most psychological methods are learned by noting down a winning method when you see
   one — which is that same accumulation.

All three were expressible with existing vocabulary: `contradicts` in `intra_source_relations` at
object level, and `conflicts` with `origin: extractor_inferred` at system level. Nothing had to be
invented and nothing had to be smoothed over.

**Why this is worth recording.** A source can be internally incoherent and still be worth extracting,
and this is the case where a schema is most tempted to tidy. It did not have to.

---

### C-05 — The relationship vocabulary was under-used again, and one needed relation does not exist at all

**Status:** OBSERVED · **Layer:** ontology · **Possible recurrence — see caution below** ·
**Distinct books in this lane: 1**

Two problems, one of which is new.

**(a) Under-use.** `keyed_advertising` and `traced_returns` stand in a clear
broader/narrower relation — one is the apparatus, the other the data it produces. `broader_than` and
`narrower_than` exist in the SPEC-05 vocabulary, but the Canon charter names only `related_to` and
`potentially_equivalent_to` as relations a worker may set locally. Rather than assume the authority,
`related_to` was used and the intended reading written into the note. The same happened for
`mental_impression` and `price_as_evidence_of_worth`, which look like one mechanism under two names.

*Caution on counting:* the pre-parallel handover checkpoint reports an item of the same shape from an
earlier book. This lane has not read that book's working files, and cannot confirm the two are the
same issue rather than two similar ones. It is recorded here as an independent observation; the
integrator should decide whether it is a recurrence.

**(b) New: there is no relation for opposition.** Hopkins sets `offer_service` directly against
`driving_people_to_the_stores` — the right and the wrong attitude to the same task, stated in the
same passage. `distinct_from` records "we checked and these are not the same", which is a different
and weaker statement than "the source presents these as opposites". `related_to` was used and the
opposition put in the note.

**Practical consequence if unchanged.** Two of the most useful things a source tells us — that A is
a special case of B, and that A is the opposite of B — are both stored as "connected somehow", with
the real content in free text.

**PROPOSED — not applied.** Either extend local authority to `broader_than`/`narrower_than`, which
needs no schema change, or add an opposition relation, which does. Recorded only.

---

### C-06 — Evidence *for* the current design: the V0 granularity rule held on an unusually claim-dense source

**Status:** OBSERVED · **Layer:** granularity · **Evidence for the frozen rule** ·
**Distinct books: 1**

24 printed pages produced 54 SourceKnowledge objects — roughly 2.2 per page, the densest in the
batch so far and about double the rate of the pre-parallel books. This is a property of the source,
not of the extractor: Hopkins writes in short declarative rules, most of which genuinely can be
retrieved, supported, contradicted or qualified on their own, which is exactly the V0 test.

No exception to the rule had to be invented. **One borderline case is recorded** rather than
resolved: `sk_hop_sa_0054` ("a definite statement takes no more room than a vague one") could
defensibly have been folded into the specificity claim it supports. It was kept separate because the
economic argument could hold or fail independently of the persuasive one. The caveat says so, in the
object.

**A related scope observation, offered to the integrator.** The batch's depth calibration is written
in chapter units — "one substantial chapter or equivalent span". Hopkins's chapters are 2–4 printed
pages, an order of magnitude smaller than the chapters in other batch books. A chapter is not a
stable unit of size across the library, and treating it as one would have produced a section too
small to expose this author's reasoning system. Seven chapters were taken instead, and the reason is
written into `PROVENANCE.md` rather than left implicit.

---

### C-07 — Visual loss did not recur, and the batch now has a genuine zero-risk control

**Status:** OBSERVED · **Layer:** visual completeness · **Evidence against an earlier concern** ·
**Distinct books: 1**

The visual pass rendered and inspected all 24 pages before any claim was written and found **zero**
figures, illustrations, tables, diagrams or reproduced advertisements. Every page is one column of
body text with a running header and a page number. For this source class, text extraction loses
nothing.

**Why a null result is worth writing down.** A visual pass that only ever reports loss cannot
distinguish "we lost the evidence" from "there was no visual evidence to lose". This book supplies
the second case cleanly, which makes the first case meaningful.

**A second, separate observation that the loss taxonomy does not currently have a name for.**
Hopkins argues from specific advertisements — the Mead Cycle Company's, the incubator advertisement
with and without its silhouetted chickens, the brewer's copy, "Our net profit is 3 per cent" — and
tells the reader to look at them and note their headlines, type and use of space. **Not one is
reproduced anywhere in the book.** This is not digitisation loss and no better scan would repair it:
the 1923 reader was in exactly the same position. The two patterns are recorded separately in the
visual evidence ledger as `no_visual_layer` and `absent_in_source`.

**Practical consequence.** Recording "the evidence is missing" without recording "missing from the
source, or missing from our copy?" would put an unfixable gap and a fixable one in the same bucket.

---

### C-08 — OCR damage was clean, and *where* it fell was more diagnostic than how much

**Status:** OBSERVED · **Layer:** provenance / source integrity · **New in Lane C** ·
**Distinct books: 1**

The section's garbled-word rate is about 0.04% — three words in 8,202, all recoverable
(`Pll` for "I'll"). But the damage is not spread evenly. It is confined almost entirely to **italic
page-number footers**, which render as `ii`, `124`, `1)`, `ts)`, `ee`. Printed page 11's footer reads
"11" on the page and `ii` in the text layer. Body text, set in roman, is clean.

**Why it matters.** A single overall damage rate would have hidden this. The useful question turned
out to be *which typographic class* the OCR failed on, because that predicts what else is at risk —
here, any italic numeral, which is where page references and some emphasis live.

**Practical consequence.** Cheap and worth keeping: measure damage by where it clusters, not only by
how much there is.

---

### C-09 — The frozen visual pass has no step for verifying load-bearing numbers against the page

**Status:** OBSERVED · **Layer:** visual completeness / method · **New in Lane C** ·
**Distinct books: 1**

The visual pass as practised in this batch is about figures, demonstrations and layout. This book has
none of those, so a literal reading of the method would have marked the pass complete after
confirming there were no figures.

But this source's evidence **is** its numbers, and OCR of digits is precisely the failure that would
corrupt the extraction without leaving a trace: `$14.20` misread as `$14.20` is fine, misread as
`$1.20` is a silently wrong claim in a file that validates. So printed pages 11 and 23 were
re-rendered at high resolution and every load-bearing figure was read from the page against the text
layer. All matched.

This step was performed because it was obviously necessary, not because the method calls for it. It
is not a method change — it adds verification, changes no rule and altered no object — but the gap is
worth naming.

**PROPOSED — not applied.** Add to the visual pass: where a claim's support is a specific figure,
verify the figure against the rendered page. Recorded only.

---

### C-10 — Binding behaviour was as SPEC-04 predicts, and one binding used the layer in a way worth naming

**Status:** OBSERVED · **Layer:** bindings · **Evidence for the frozen design** ·
**Distinct books: 1**

54 objects produced 8 bindings — roughly one binding per seven objects. Most of this book is print
craft doctrine for a medium our schemas do not model (type size, space utilisation, coupons, mail
order economics), and those objects are correctly left unbound. Zero bindings is the normal state
and it behaved that way here without pressure.

**One binding is worth calling out as a shape.** `bnd_hop_sa_0006` does not fill or constrain a
Creative IR field. It **flags that one of the values in an existing field's list is contested by a
major source in the domain** — Hopkins denies that `awareness` or `brand_film` are legitimate
objectives at all ("It is not for general effect. It is not to keep your name before the people").
`role: [flags]` supports this and no schema change was needed. Recorded because it is a use of the
binding layer that carries disagreement rather than instruction, and disagreement between sources is
something the product will eventually have to hold.

---

### C-11 — A source that theorises its own persuasive technique creates a problem only the system layer catches

**Status:** OBSERVED (about the text) / INFERRED (about the consequence) · **Layer:** evidence
interpretation · **New in Lane C** · **Distinct books: 1**

Chapter 7 states that a definite figure makes the reader infer that tests were made — "Say that it
gives three and one-third times the light and people realize that you have made tests and
comparisons"; of a 78-second shave, "That was definite. It indicated actual tests."

The book is written to that rule. Its own authority rests on specific figures — 85 cents, $14.20,
41 cents, 250,000, nine times in ten, two thousand headlines, five to ten times, exactly 50 per cent
— supplied without the measurements behind them.

**This is an observation about the text, not an accusation.** Whether Hopkins's measurements were
made is **NOT VERIFIED** and cannot be settled from chapters 1–7.

**Where it is recorded, and why that matters.** No single object shows it. Each figure, read alone,
is an ordinary unattributed practitioner number. The pattern only exists across the whole extraction,
and it is written into `scs_hop_sa_005`'s `system_level_uncertainty`. A consumer that retrieves
objects individually and never reads the system would not see it.

**Practical consequence if unchanged.** The system layer is currently the only place a whole-source
epistemic property can live, and nothing guarantees a consumer reads it. That is an argument for the
system layer, and a warning about how it gets consumed.

---

### C-12 — No historical comparator exists for this book

**Status:** OBSERVED · **Layer:** provenance · **Distinct books: 1**

Searched after the fresh checkpoint was committed and pushed, per the sealing rule. The repository
contains no prior extraction, audit, findings file or superseded atom set for Hopkins. The only
mentions are planning references: `CANON-COVERAGE-MAP-V0.md` lists *Scientific Advertising* as an
owned but unprocessed source, `CANON-CURRICULUM-V0.md` explicitly defers it, and
`FINDINGS-02-molly-bang-pass1.md` names Hopkins as a candidate for a later book.

Recorded as **`no historical comparator`**. None was manufactured.

---

---

## Book 14 — Chip Heath & Dan Heath, *Made to Stick*, Introduction

Fresh checkpoint: `a699a49`. Historical comparison: **no prior extraction exists**; one prior
*prediction* about this book does exist and is compared in C-21.

---

### C-13 — The same evidence vocabulary fails again, in the opposite direction: there is no way to record cited external research

**Status:** OBSERVED · **Layer:** source fidelity / evidence characteristics · **New in Lane C, and
the mirror image of C-01** · **Distinct books showing the vocabulary gap: 2**

**What it is.** This book's support is overwhelmingly published research by named third parties:
Elizabeth Newton's 1990 Stanford doctoral study of tappers and listeners, with a design and figures
(120 songs, 3 identified, 2.5 per cent actual against 50 per cent predicted); Joel Best and Gerald
Horiuchi's study of every reported Halloween incident since 1958; a 1999 Israeli study classifying
200 award-winning advertisements against 200 matched non-award ones (89 per cent against 2 per
cent), and its follow-up three-arm training experiment with a blinded selector.

`empirical_within_source` is defined as "the source reports its **own** measurement". None of these
is the authors' own. The fixed list has no value for cited external research at all.

**Why this is the sharper half of the problem.** Book 13 and book 14 are the same vocabulary failing
in opposite directions:

| | what the source does | what the vocabulary records |
|---|---|---|
| Hopkins | claims measurement, reports almost none | risk of crediting evidence that was not supplied |
| Heath & Heath | reports measurement constantly, almost none of it their own | no way to credit evidence that *was* supplied |

**What was done, under the frozen method.** The characteristic was withheld from every third-party
study, and each study was recorded in full — researcher, design, comparison group, figures — in a
caveat marked `extractor_observed`.

**Practical consequence, and it is worse than C-01's.** This book's best-evidenced claims and its
bare assertions now carry similar characteristic sets. `sk_hea_mts_0023`, which rests on a published
controlled study, and `sk_hea_mts_0017`, which rests on "it's difficult... but it's easier", are not
cleanly separable by anything a machine reads. The extraction states this in the file header and in
`PROVENANCE.md` so it cannot be misread as the extractor having missed the evidence — but a
statement in prose is not a fix.

**PROPOSED — not applied.** A characteristic for "the source reports a named third party's
measurement", distinct both from the source's own measurement and from bare assertion. Schema
change; approval trigger; recorded only.

---

### C-14 — `source_warns_against_isolated_use: false` cannot tell silence from explicit permission

**Status:** OBSERVED · **Layer:** systems · **New in Lane C** · **Distinct books: 1**

**What it is.** The field is boolean. For this book the correct value is `false`, and that value is
misleading, because this source does not merely fail to warn against using its principles in
isolation — it explicitly licenses partial use: "you don't need all of these traits in order to be
great... And having all the traits doesn't guarantee greatness."

Three states exist and the field has two: the source warns against isolated use; the source is
silent; the source affirmatively permits it. The second and third both record as `false`.

**Why it matters.** This is a retrieval-governance fact. "The author said you may use one of these
alone" and "the author never addressed it" license completely different behaviour by anything that
retrieves a single member of the system.

**How it was handled.** The value stays `false` and the distinction is written into the system's
`system_level_uncertainty`, alongside a note in the binding that carries it
(`bnd_hea_mts_0006`, governance / rule_application).

**PROPOSED — not applied.** Make the field three-valued. Schema change; recorded only.

---

### C-15 — Two governing documents disagree about which relationship types a worker may set, and the conservative reading cost real fidelity

**Status:** OBSERVED · **Layer:** ontology / governance · **New in Lane C; sharpens C-05(a)** ·
**Distinct books in this lane showing relation under-use: 2**

**What it is.** The source states an identity outright: the tapper who cannot stop hearing the tune
**is** the Curse of Knowledge. The tapper/listener gap is that tendency observed under measurement,
not a separate phenomenon resembling it. The SPEC-05 relation for this is `same_mechanism`.

The two documents give different answers about whether this worker may set it:

- **SPEC-05's governance section** singles out only `same_failure_family` as requiring human review,
  which would permit `same_mechanism`.
- **The Canon charter** enumerates the relations a worker may choose locally and lists exactly two:
  `related_to` and `potentially_equivalent_to`.

The narrower reading was followed, so `related_to` was recorded and the intended relation written
into the note.

**Why this is worth escalating rather than filing quietly.** The cost is not hypothetical. A
source-stated identity is now recorded in the structured layer as an unspecified connection, and
`related_to` is the same value used elsewhere in this file for "the source mentions these together".
Across books 13 and 14 the same downgrade has now happened to `broader_than`/`narrower_than` four
times and to `same_mechanism` once, and in every case the real relation survives only in a prose
note.

**Practical consequence if unchanged.** The ontology layer's whole purpose is to make relationships
machine-readable so aggregation is possible later. Systematically downgrading to `related_to`
produces a graph where almost every edge means nothing in particular.

**PROPOSED — not applied.** Reconcile the two documents. The cheapest resolution needs no schema
change at all: state which relation types are a local decision. Recorded only.

---

### C-16 — Evidence *for* the current design, and the strongest in this lane: the system layer carried what no object could

**Status:** OBSERVED · **Layer:** systems · **Evidence for the frozen design** ·
**Distinct books: 1**

This book is the case SPEC-03's SourceConceptSystem was written for, and it worked.

The six principles are, individually, ordinary. The source says so itself: "many of the principles
have a commonsense ring to them... It's not as though there's a powerful constituency for
overcomplicated, lifeless prose." An extraction that produced six rules — be simple, be unexpected,
be concrete — would have been faithful at the object level and would have thrown away everything the
book contributes.

What is not commonsense lives entirely above the objects, and all of it was recordable:

- the six are **one checklist**, run against an idea you already have, and the source demonstrates
  the procedure twice;
- they are explicitly **not a formula** — not necessary, not sufficient;
- all six are aimed at **one named obstacle**, and that obstacle is why obvious advice is not
  followed;
- the whole thing is warranted by a **separate argument** that stickiness is learnable at all, which
  the source never assembles in one place.

Three systems hold this. Two carry `whole_system_claim.origin: source_explicit` — the source built
them, not us — which is rarer in this batch than `extractor_synthesis` and is worth noting on its
own.

**The counterfactual is the point.** Without the system layer this extraction would have been six
banal rules plus twenty-two supporting observations, and would have read as a weak source. With it,
the framework survives as a framework.

---

### C-17 — The V0 granularity rule needed a judgement call at a framework member, and held without a new rule

**Status:** OBSERVED · **Layer:** granularity · **Evidence for the frozen rule, with a caveat** ·
**Distinct books in this lane needing a recorded granularity judgement: 2**

**The tension.** Strictly applied, V0 says split when a claim can be retrieved, supported,
contradicted or qualified independently. Several principles contain sub-claims that pass that test —
surprise seizes attention but decays while curiosity gaps hold interest; hard numbers are often the
wrong instrument for belief; people feel for individuals rather than abstractions. Splitting them
would have produced ten or more objects where the framework has six members, and the checklist would
no longer map onto the extraction.

**How it was resolved without inventing a rule.** Each principle is one object, because the
principle is the unit the checklist operates on. Sub-claims that carry their own distinct mechanism
*and* their own support are separate objects related by `specialises` to their principle, and the
system's membership lists the six principles only. Both the V0 test and the framework survive.

**Why it is recorded rather than presented as settled.** The choice of which sub-claims cleared the
bar was a judgement. Four did. Others — for instance the Golden Rule as an exemplar of simplicity —
were treated as illustration and not split, per V0's instruction not to split for another example.
A different extractor could defensibly have drawn that line one object either way.

---

### C-18 — An EPUB-sourced book is structurally less locatable, and the batch's books are therefore not equally citable

**Status:** OBSERVED · **Layer:** provenance · **New in Lane C** · **Distinct books: 1**

Every object in this book has `page_start: null` and `page_end: null` and locates itself by section
heading. This is not an omission — an EPUB reflows, so there is no page and no printed page number
to cite. Nor could the text be checked against a print edition, as this lane's book 13 was, because
no print copy is available locally.

**Why it matters beyond tidiness.** The batch now contains books whose claims can be checked against
a specific printed page and books whose claims can only be located to a named section of several
thousand words. Anything that later cites Canon knowledge back to a source will find the two classes
are not equally verifiable, and nothing in the schema currently records which class an object
belongs to — `provenance.locator` is free text.

**Mitigation used here.** The section headings in this file are real text, present in the text layer,
and there are fourteen of them across the section, so locators are as fine-grained as the source
allows. That is stated in `PROVENANCE.md` rather than left to be discovered.

---

### C-19 — A new visual pattern: the section's own title exists only as a picture

**Status:** OBSERVED · **Layer:** visual completeness · **New in Lane C** · **Distinct books: 1**

The word "INTRODUCTION" is a 238×39 JPEG with no alt text. So are all six chapter titles: this EPUB
sets its top-level headings as images of words, as a house convention. A text-only extraction of the
file produces a section with no title on it.

**Severity: low, and the reason is worth keeping.** Nothing is corrupted, no sentence is lost, and
the fourteen sub-headings *inside* the section are real text and extract perfectly. Only the label of
the top-level unit is affected, and a visual pass recovers it completely by opening one image.

**Named as `heading_as_image` in the visual evidence ledger.** The pre-parallel handover checkpoint
reports an item of a similar shape from an earlier book — a graphic disturbing where a named section
appeared in the text layer. This lane has not read that book's working files and does not assert the
two are the same issue. Flagged for the integrator.

**Cheap check that caught it.** Enumerating every image in the package and opening each distinct one
takes minutes and is what distinguished "this book has no figures" from "this book has no figures
and one of its headings is a figure".

---

### C-20 — Source shape predicts binding yield, which is information about the product schema rather than about Canon

**Status:** OBSERVED (the counts) / INFERRED (the cause) · **Layer:** bindings ·
**Distinct books: 2, within this lane**

| Book | Objects | Bindings | Rate |
|---|---|---|---|
| 13 — Hopkins | 54 | 8 | one per ~7 |
| 14 — Heath & Heath | 28 | 9 | one per ~3 |

**Inferred cause.** Hopkins is largely print-medium craft — type size, space utilisation, coupons,
mail-order economics — for a medium our schemas do not model, so most objects correctly stay unbound.
Made to Stick is about designing a message for an audience, which is what a Creative IR is for, so
its claims land on fields that already exist: proposition, hook, emotional target, hierarchy.

**Why record it.** A low binding rate has been read in this batch as evidence that SPEC-04 is
behaving correctly, which it is. This adds that the rate is also a property of the source's subject
matter, so binding counts across books measure the schema's coverage of a domain and not the quality
of an extraction. Comparing them without that in mind would produce a wrong conclusion.

---

### C-21 — No prior extraction exists, but a prior *prediction* does, and it was half right

**Status:** OBSERVED · **Layer:** provenance / planning · **Distinct books: 1**

Searched after the fresh checkpoint was pushed and committed. There is **no prior extraction, audit,
findings file or superseded atom set** for this book. Recorded as `no historical comparator`; none
was manufactured.

But `canon/experiments/CANON-CURRICULUM-V0.md` contains a prediction made about this book before
anyone had read it for extraction:

> the SUCCESs framework is unusually operational — six named attributes with diagnostics, which
> maps almost directly onto evaluation dimensions

Comparing that against the fresh pass, after the checkpoint:

- **Right on direction.** The framework did bind more readily than anything else in this lane — nine
  bindings from twenty-eight objects, including a whole-asset evaluation binding built directly on
  the checklist. "Unusually operational" is fair.
- **Overstated on substance.** "Six named attributes **with diagnostics**" is not what the source
  supplies. The Introduction gives six *questions* and no test for answering any of them. Every
  answer in the source's own worked example is the authors' judgement. And the source states
  explicitly that the traits are neither necessary nor sufficient, which rules out the scoring
  behaviour "maps almost directly onto evaluation dimensions" implies.

**Why this is worth logging.** The coverage map and curriculum carry confidence ratings — this
book's domain is rated "strong" — that were assigned from reputation rather than from extraction.
This is the first case in this lane where one could be checked, and it was directionally right and
materially overstated. That is a caution about reading those ratings as findings, not a defect in
them; they were written as planning documents.

---

## Book 15 — Rory Sutherland, *Alchemy*, Introduction

Fresh checkpoint: `f992d69`. Historical comparison: **no prior extraction exists** (see C-30).

---

### C-22 — `source_uncertainty` finally carried real load, and the pattern across the lane is the opposite of what you would expect

**Status:** OBSERVED · **Layer:** evidence · **Evidence for the frozen design** ·
**Distinct books compared: 3**

In books 13 and 14 almost every object recorded `source_uncertainty: none`. It would have been easy
to read that as a dead field. It is not. In this book it carries `source_concedes_difficulty`,
`source_hedges` and `source_asks_open_question` across a substantial share of objects, because this
author repeatedly says he does not know:

- of the strongest result in his own field experiment: *"I'll be honest with you – I have no idea
  why this should be."*
- of his own worked design example: *"We could find out"*, *"We don't know yet."*
- of the extension of his own thesis: *"I strongly suspect."*

**The cross-book pattern is worth stating plainly, because it is counterintuitive.** Ranked by how
confident the prose sounds, the lane runs Hopkins → Heath & Heath → Sutherland. Ranked by how much
evidence is actually supplied, it runs roughly the other way. And ranked by how often the author
admits ignorance, it is Sutherland by a wide margin — the source that presents itself as a
provocation rather than as science.

**Why this matters for the field.** `source_uncertainty` measures the author's stated confidence,
not the strength of the support. Those two are not correlated in this lane, and may be inversely
related. Anything that later weights knowledge should not treat a hedge as a weakness signal.

---

### C-23 — The cited-external-research gap recurs for the third time, in all three books of this lane

**Status:** OBSERVED · **Layer:** source fidelity / evidence characteristics ·
**Recurrence of C-13** · **Distinct books: 3 of 3**

This source cites Trivers and Kurzban on self-deception, Parker and Bollinger at Duke on the
appendix with an effect size, and a 1996 Heritage Institute survey on religious practice. As in book
14, `empirical_within_source` — "the source reports its **own** measurement" — does not apply, and
the fixed list has no value for cited external research, so each was recorded in an
`extractor_observed` caveat.

**Every book in this lane hit the same gap, in a different way each time:**

| Book | What the source does | Why the vocabulary fails |
|---|---|---|
| 13 — Hopkins | asserts measurement, reports almost none | risks crediting evidence never supplied |
| 14 — Heath & Heath | reports measurement constantly, almost none of it his own | cannot credit evidence that was supplied |
| 15 — Sutherland | mixes his own field test with cited third-party research | needs both values in the same source, and has one |

Book 15 is the sharpest of the three, because within a single extraction the same characteristic is
correctly applied to the author's own envelope experiment and correctly withheld from the Duke
appendix research — so the file itself contains the distinction the vocabulary cannot express.

**Practical consequence.** Three books in one domain, three failures, one field. Whether this is a
domain artefact or general is precisely what the other lanes decide. Within Lane C it is the single
strongest recurring signal.

---

### C-24 — The first figure in this lane that actually argues, and almost all of its content is only in the figure

**Status:** OBSERVED · **Layer:** visual completeness · **New in Lane C** · **Distinct books: 1**

Books 13 and 14 had no figures at all — 24 rendered pages and a whole EPUB, nothing shown rather
than said. It would have been reasonable, after two such results, to treat a visual pass on an
advertising/persuasion source as a formality.

This book has two figures and one of them is the thesis. A two-axis chart runs FAILS↔WORKS against
MAKES SENSE↔SEEMS WEIRD with roughly two dozen items placed in the quadrants. The prose beside it
names only the top-right quadrant and one item, the bicycle. **Every other placement exists solely
in the image** — Marxism, flossing, economies of scale, management consultancy and economics in
makes-sense-and-fails; placebos, marketing, heuristics, evolution, constitutional monarchy and Red
Bull in seems-weird-and-works. Several of these are the strongest claims on the page, and they are
made by position on a chart rather than by argument.

**Loss pattern, named `named_loss_with_unstated_content`.** The text points at the figure, so the
absence is announced and an extractor would not miss it silently. What a text-only pass produces is
the claim with none of the content that makes it contentful.

**The finding is really about the method, not the book.** The mandatory visual pass earned its cost
here precisely because the two preceding books in the same lane and the same domain had returned
nothing. A pass that is skipped once a source class "looks textual" would have missed this.

---

### C-25 — An internal inconsistency in a source is indistinguishable from extraction damage until you check

**Status:** OBSERVED · **Layer:** provenance / source integrity · **New in Lane C** ·
**Distinct books: 1**

The section headed **"The Four S-es"** says *"There are **five** main reasons... and they
conveniently all begin with the letter S"* and then lists **four** items, one of which begins with P.
Heading, count and list all disagree.

Read from a text extraction alone, this looks exactly like a dropped item.

**What was done.** The section was read in the raw source file — it is 78 words — and its single
footnote was resolved, reading *"Except for the one that begins with a P."* Nothing is missing. The
inconsistency is in the published text and has **not** been silently repaired; the object records the
source's wording, the discrepancy, and the fact that completeness was verified.

**The generalisable point.** Any enumerative or numeric mismatch — a heading that says four, a
sentence that says five, a list of four — must be treated as an integrity question before it can be
attributed to the author. The check is cheap. Attributing an author's error to our extraction, or
our loss to the author, are both silent corruptions of the record, and they look identical from the
text alone.

---

### C-26 — Evidence *for* the current design: an avowedly anti-rational source went in without distortion

**Status:** OBSERVED · **Layer:** source fidelity, systems · **Evidence for the frozen design** ·
**Distinct books: 1**

This was the hardest test of the frozen schema in the lane, and the schema passed.

The source declares itself *"a provocation, and only accidentally a work of philosophy"*. It argues
that things can work without a known reason, that requiring a rationale before trying something is
itself the failure mode, and that the opposite of a good idea can be a good idea. A schema with any
field that rewarded rigour, or that required a mechanism, or that assumed a source's claims resolve
into non-contradictory rules, would have had to either exclude this material or dress it up.

Nothing had to be excluded and nothing had to be dressed up:

- `mechanism.stated_by_source: false` is a normal value, so claims with no mechanism were recorded
  as claims with no mechanism.
- `evidence.characteristics` are factual descriptions rather than a quality score, so a page of
  `practitioner_assertion` and `anecdotal` reads as a description of the source rather than as a
  verdict on it.
- `source_uncertainty` had somewhere to put the author's repeated admissions of ignorance.
- `whole_system_claim.origin: extractor_synthesis` with a required `interpretation_basis` was
  exactly the instrument needed for the hardest judgement in the extraction — see below.

**The hardest judgement, and why the schema made it recordable.** A source like this invites being
summarised into a method: six things to do differently. Doing that silently would convert a book that
explicitly declines to offer a recipe into one that offers a recipe. The instructions are genuinely
there and genuinely useful, so discarding them would also be wrong. They were recorded as a system
whose whole-system claim is marked `extractor_synthesis`, with the source's refusal written into the
interpretation basis. The usefulness is preserved and the authorship of the structure is visible.

**Also recorded rather than smoothed: this source contradicts itself three times inside the processed
section** — it warns against reasoning from hindsight and then reconstructs an election in hindsight;
it argues that universal claims about human affairs are doomed and then makes two; it rejects
self-report as evidence and then explains its own behaviour by introspection. All three were
expressible with existing vocabulary. See C-29.

---

### C-27 — The lane's first `distinct_from` that the source itself asserts

**Status:** OBSERVED · **Layer:** ontology · **Evidence for the frozen design** ·
**Distinct books: 1**

Every `distinct_from` recorded in books 13 and 14 was our judgement — a similarity examined and
rejected. This one is the author's. Sutherland introduces a hyphen specifically to hold two things
apart: **nonsense** is behaviour that genuinely serves nothing; **non-sense** is behaviour that is
useful or effective while defying conventional logic. The whole argument of the section depends on
their being different.

**Why it is worth recording separately.** The two terms differ by one punctuation mark. Any
normalisation that stripped punctuation, or any near-synonym merge based on string similarity, would
collapse them into one and destroy the distinction the source built. SPEC-05's rule that a term is
never edited to fit a concept is what protects this, and this is the clearest instance in the lane of
that rule doing real work.

It also demonstrates that `confidence_basis: source_stated` is meaningful on a `distinct_from`, which
none of the earlier instances showed.

---

### C-28 — Source shape predicts which *layer* a source binds to, not only how much it binds

**Status:** OBSERVED (the counts) / INFERRED (the cause) · **Layer:** bindings ·
**Extends C-20** · **Distinct books: 3**

| Book | Objects | Bindings | Creative IR | Evaluation | Governance | Benchmark |
|---|---|---|---|---|---|---|
| 13 — Hopkins | 54 | 8 | 2 | 2 | 3 | 1 |
| 14 — Heath & Heath | 28 | 9 | 4 | 1 | 3 | 1 |
| 15 — Sutherland | 32 | 7 | 1 | 2 | 3 | 1 |

Three books, one domain, three distinct profiles. Made to Stick is about designing a message, so it
lands on Creative IR fields that already exist. Hopkins is largely print craft for a medium the
schema does not model, so it lands mostly elsewhere. Alchemy is about *how to think about* problems
rather than about any artefact, so six of its seven bindings are governance or evaluation and only
one touches a Creative IR field.

**Why it matters.** A low Creative IR binding count has a plausible-sounding reading — that a source
is not very useful — which is wrong. Alchemy binds least to Creative IR and produced the lane's most
directly applicable governance content: how to weigh a claim with no mechanism, how to treat two
sources recommending opposite things, and what a human evaluator can and cannot learn by asking
people. Binding counts measure schema coverage of a subject, and reading them as source quality would
invert the answer.

---

### C-29 — Sources in this domain contradict themselves inside a single processed section, routinely, and the schema records it

**Status:** OBSERVED · **Layer:** systems, source fidelity · **Evidence for the frozen design** ·
**Distinct books: 3 of 3**

| Book | Self-contradictions recorded within the processed section |
|---|---|
| 13 — Hopkins | 3 (its own measurement rule; its own generalisation rule; its own method of discovery) |
| 14 — Heath & Heath | 2 (simplicity against concreteness; unexpectedness against credibility) |
| 15 — Sutherland | 3 (hindsight; universal claims; self-report) |

Eight contradictions across three books, every one expressible with existing vocabulary —
`contradicts` in `intra_source_relations` at object level, `conflicts` with an origin marker at system
level. Nothing had to be invented and nothing had to be smoothed over.

**Two observations.** First, this is strong evidence *for* the current design: the moment a schema is
most tempted to tidy is when a source disagrees with itself, and this one does not. Second, it is a
source-shape finding in its own right — commercial and practitioner sources appear to contradict
themselves within a few thousand words as a matter of course, which means any consumer retrieving
two objects from the same book cannot assume they are consistent.

---

### C-30 — No historical comparator exists for this book either

**Status:** OBSERVED · **Layer:** provenance · **Distinct books: 1**

Searched after the fresh checkpoint was committed and pushed. No prior extraction, audit, findings
file or superseded atom set exists for *Alchemy*. The only mentions are planning references:
`CANON-CURRICULUM-V0.md` lists it among titles explicitly deferred for V0, and
`CANON-COVERAGE-MAP-V0.md` cites it as an owned but unprocessed source for audience understanding,
persuasion and emotional target.

Recorded as **`no historical comparator`**. None was manufactured.

**All three books in Lane C have no historical comparator.** This is worth flagging for the
integrator: the pre-parallel books 1–3 each had one and the comparison produced the batch's strongest
signal to date. Lane C contributes no evidence on that question at all, in either direction.

## Lane C final tally — all three assigned books complete

| | |
|---|---|
| Books complete | **3 of 3** — Hopkins, Heath & Heath, Sutherland |
| Books blocked | 0 |
| Books with a historical comparator | **0 of 3** |
| Total objects | 114 SourceKnowledge · 11 systems · 81 terms · 29 relationships · 10 concepts · 24 bindings |
| Issues raised | C-01 to C-30 |
| Schema/method changes made | **none** |

### Recurrence within Lane C, counted by distinct books

| Issue | Books | What it is |
|---|---|---|
| **Evidence-characteristic gap** (C-01, C-13, C-23) | **3 of 3** | one field, `empirical_within_source`, cannot record claimed-but-unreported measurement, cited external research, or a source that does both |
| **Relation-type under-use** (C-05a, C-15) | **3 of 3** | `broader_than` / `narrower_than` / `same_mechanism` all downgraded to `related_to`; SPEC-05 governance and the Canon charter disagree about which a worker may set |
| **Self-contradiction inside one section** (C-29) | **3 of 3** | eight instances, all expressible — evidence *for* the design |
| **A recorded granularity judgement** (C-06, C-17) | 2 of 3 | V0 held both times without a new rule, but needed a judgement call and it is written down |
| **Binding profile varies by source shape** (C-20, C-28) | 3 of 3 | rate *and* target layer both track the source's subject, not its quality |

### Issues that appeared once and did not recur

C-02 (no `system_type` for a shared-warrant set), C-03 (unfalsifiable-but-unhedged claims), C-08
(OCR damage clustering by typographic class), C-09 (no numeric verification step in the visual pass),
C-14 (`source_warns_against_isolated_use` cannot tell silence from permission), C-18 (EPUB books are
less locatable), C-19 and C-24 (two different figure-related patterns), C-25 (source error versus
extraction damage). Each is one book. None should be read as a pattern on this evidence.

### Evidence *for* the frozen design, gathered

C-04, C-06, C-07, C-10, C-16, C-17, C-22, C-26, C-27, C-29. The strongest are C-16 — Made to Stick's
whole contribution lives above its individual claims and the system layer held all of it — and C-26 —
an avowedly anti-rational source went in without anything being excluded or dressed up.

### The one finding this lane would put in front of the Controller

**One SPEC-03 field broke in all three books, in three different ways.**
`empirical_within_source` means "the source reports its own measurement", and the fixed
characteristic list has no neighbour for anything else. Hopkins claims measurement and supplies
almost none. Heath & Heath supply it constantly and almost none is theirs. Sutherland does both
inside one book, so a single extraction contains the distinction the vocabulary cannot express.

All three were handled by writing the truth into prose caveats. That is faithful and completely
unaggregatable: nothing can later count how many sources claim an empirical basis, how many supply
one, and how many are relying on someone else's.

Whether this is general or an artefact of one domain is exactly what the other three lanes settle.
Lane C asserts the pattern within advertising and persuasion, and asserts nothing beyond it.
