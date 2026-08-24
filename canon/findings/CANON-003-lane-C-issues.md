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

## Lane C running tally after book 13

| | |
|---|---|
| Books complete | 1 of 3 |
| Books blocked | 0 |
| New issues raised | C-01, C-02, C-03, C-05(b), C-08, C-09, C-11 |
| Evidence *for* the frozen design | C-04 (contradiction representable), C-06 (granularity held), C-07 (visual loss did not recur), C-10 (binding ratio as predicted) |
| Possible recurrence of a pre-parallel item | C-05(a), flagged for the integrator to confirm or reject |
| Schema/method changes made | **none** |

## Book 14 — Chip Heath & Dan Heath, *Made to Stick*

Not started.

## Book 15 — Rory Sutherland, *Alchemy*

Not started.
