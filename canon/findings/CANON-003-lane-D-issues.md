# CANON-003 — Lane D issue file

**Lane D:** storytelling / creative process · **Branch:** `work/canon-003-d`
**Assigned books:** 16 Catmull *Creativity, Inc.* · 17 Bayles & Orland *Art & Fear* ·
18 Miller *Building a StoryBrand*

**What this file is.** New issues found by Lane D during fresh extraction, recorded in the lane's
own file because the shared batch ledger is locked during parallel execution. It is **not** a
synthesis and it does **not** count recurrence across lanes — only the final integrator can do
that, because only that session sees all four lanes.

**Isolation statement.** No other lane's new findings were read before or during these extractions.
The shared starting evidence used was: the communication standard, the CANON-003 task, the parallel
execution amendment, the source inventory, the pre-parallel handover checkpoint, and SPEC-01/03/04/05
themselves. The existing batch issue ledger was **not** opened, so nothing here was found by looking
for it.

**Counting rule used.** "Books" below means distinct books **within Lane D**. Where a hypothesis
from the handover checkpoint is relevant, it is named only to say whether Lane D's own evidence
supports or resists it — not to inherit its count.

---

## D-01 — The repair vocabulary cannot express a social or organisational action

**Status:** OBSERVED · **Layer:** ontology · **New in this batch (Lane D)** · **Books: 2**

**What it is.** SPEC-05 makes every remedy term declare `executable_by` — who or what could
actually carry the repair out. The permitted values are `physical_production`,
`generative_respecification`, `deterministic_composite`, `human_edit` and `unknown`. All four
substantive values describe changing an image, a video, or a physical camera-and-light setup.

Every remedy in Catmull ch.5 is a **social** action: change the word you use when asking for
feedback; give the reviewing group no power to mandate; convene a smaller group; keep a dominating
person out of the room; distil a session into one takeaway; phrase a note so the maker wants to act
on it.

**Why it matters.** Nine remedy terms therefore carry `unknown`. That is the honest value available
and it is also actively misleading: `unknown` reads as "we have not worked out how to execute this",
when the truth is "this vocabulary has no value for this kind of action". Anyone later counting
unresolved repairs across the Canon would misread nine representable, well-understood remedies as
gaps.

**Recurred in book 17.** *Art & Fear*'s remedies are the same kind of thing — share work in progress
with other makers, leave an unresolved thread in each piece, notice how the material actually
responds. Six more remedy terms recording `unknown`, in a completely different book by different
authors in a different decade. Two of two Lane D books.

**Consequence if unchanged.** Every process, management, teaching or creative-discipline source will
land the same way. The Canon will accumulate `unknown` repairs that are not unknown, and the field
stops carrying information precisely where the Canon is broadening beyond image-making.

**Proposed (not applied):** an additional `executable_by` value for actions performed by people
changing how they work rather than changing an artefact — a working name would be
`organisational_practice`. This is a proposal for the post-batch revision task only.

---

## D-02 — A claim quoted from a named third party inside a source has nowhere to be recorded

**Status:** OBSERVED · **Layer:** source fidelity · **New in this batch (Lane D)** · **Books: 2**

**What it is.** Several of the chapter's most useful claims are not the book's author speaking. The
two selection criteria for building your own review group, the definition of constructive criticism,
and the observation that a work must at some point stop being made for its maker are all **quoted by
Catmull from named colleagues**, and endorsed by being placed where they are.

SPEC-03 records `source_terms` (the words) and `provenance` (where in the book), but has no field
distinguishing *the author asserts this* from *the author quotes a named person asserting this,
approvingly*.

**Why it matters.** Those are different evidentiary situations. A practitioner assertion by the
book's author is one person's authority. A claim the author selected from someone else and endorsed
is arguably two people's — or arguably weaker, because the author did not commit to it in his own
voice. Neither reading is available to anything reading the Canon later, because the fact is not
recorded in a field.

**What I did instead.** Recorded the attribution in `caveats` with `origin: extractor_observed`.
That preserves the fact but files an authorship property as an observation of mine, which is the
wrong shelf.

**Recurred in book 17, more strongly.** *Art & Fear* builds a substantial part of its argument from
other people's words: a piano teacher's reply, quotations from Joan Didion, Stanley Kunitz and Ben
Shahn, Charles Eames on where his energy went, Durrell's construction stakes, Forster on the
Malabar Caves — plus an epigraph from a named person at the head of every chapter. The rendered page
sets the epigraph apart in italic; the text layer loses the distinction entirely. Two of two Lane D
books, and the second is the heavier case because the borrowed material carries more of the
argument.

**Consequence if unchanged.** Interview- and reportage-shaped sources will systematically lose the
question "whose claim is this?". Lane B's *The Conversations* is an interview transcript, so this
may matter more there than here — that is a **prediction, not a finding**, and only the integrator
can check it.

**Proposed (not applied):** a `claim_attribution` field on SourceKnowledge distinguishing
`source_author`, `source_quotes_named_third_party` and `source_quotes_unnamed`.

---

## D-03 — A source with no visual argument at all, and a one-pixel trap in the visual pass

**Status:** OBSERVED · **Layer:** visual completeness · **New in this batch (Lane D)** ·
**Books: 1**

**What it is.** Catmull ch.5 contains exactly one image reference. Measured, it is **525 × 1
pixels** — a decorative horizontal rule repeated under all 28 chapter titles. The book's 21 real
images sit in a separate photo insert and are captioned biographical photographs. Nothing in the
book supports a claim visually.

**Why it matters, in two directions.**

1. **A visual pass that counts figure references rather than inspecting them gets this wrong.** It
   would report one figure in the chapter and then either hunt for an argument that does not exist,
   or mark the chapter visually incomplete for never having inspected a horizontal line. One pixel
   of height separated a correct reading from a wrong one. Measuring every image, not counting
   references, is what caught it.
2. **The visual-completeness vocabulary has no value for "there is nothing to see".** The batch so
   far uses `verified_page_level`, `blocked_visual_validation` and `not_verified`. None of those
   fits a source that argues entirely in prose. I recorded `verified_figure_level` and explained
   precisely what it covers, because saying `not_verified` would imply a gap where there is none,
   and `verified_page_level` would claim an inspection an EPUB cannot support.

**Consequence if unchanged.** Sources with no visual argument will be recorded either as
suspiciously unverified or as verified in a way that overstates what was checked. Both distort a
later reading of which parts of the Canon rest on inspected evidence.

**Proposed (not applied):** a visual-completeness value meaning "inspected; the source makes no
visual argument", distinct from both "verified" and "blocked".

---

## D-04 — Process knowledge has structure the source never made explicit in any form

**Status:** INFERRED · **Layer:** systems · **New in this batch (Lane D)** · **Books: 1**

**What it is.** The chapter describes a repeating loop — review a crude full-length stand-in for the
film, at a cadence of three to six months, with stated preconditions and stated failure modes — and
never draws it, tabulates it, or numbers its steps. The structure exists in the reasoning and
nowhere on the page.

**Why it matters.** Both SourceConceptSystems in this extraction therefore carry
`whole_system_claim.origin: extractor_synthesis`, and their `system_level_uncertainty` says plainly
that a different reader could reconstruct the same chapter as a flat list of good practices rather
than as an interacting mechanism. The schema handled this correctly — origin marking at every
structural level is exactly the machinery for it — but it means **for this source class the systems
layer is doing more inventing than reporting**, and that is a property of the source shape, not a
defect in the extraction.

**Contrast worth recording.** In the visual-design books the risk is losing structure the source
*showed*. Here there is no structure to lose and none to find; it has to be built. Those are
opposite failure modes and they need different safeguards.

**Consequence if unchanged.** None immediately — the origin fields make the situation visible. The
risk is a later reader treating a system's existence as source evidence when it is a hypothesis. The
fields say otherwise, but only if read.

---

## D-05 — Counter-evidence: the extraction did not need Creative IR bindings, and did not invent any

**Status:** OBSERVED · **Layer:** bindings · **Evidence *for* the current design** · **Books: 1**

**What it is.** Twenty-one SourceKnowledge objects produced **zero** Creative IR bindings. The
chapter never discusses what a creative asset should contain, so there was nothing to fill. Five
bindings exist against evaluation, governance, benchmark and one parked production candidate.

**Why it matters.** This is the first book in the batch whose subject has no contact at all with the
product's asset schema, and it produced real knowledge without any pressure to invent a consumer.
Under the superseded SPEC-02 rule — every atom must name a Creative IR field — this chapter would
have yielded either nothing or twenty invented bindings. Recorded as evidence *for* the SPEC-03 /
SPEC-04 split rather than as a problem.

**Note on the handover checkpoint's B-14 hypothesis** (that older extractions kept noticing
product-schema fit the fresh ones missed): Lane D cannot test it here, because **no historical
comparator exists for this book**. Not evidence either way.

---

## D-06 — Counter-evidence: `broader_than` was usable without any authority problem

**Status:** OBSERVED · **Layer:** ontology · **Evidence against an earlier concern** · **Books: 1**

**What it is.** The handover checkpoint records that an earlier worker wanted `broader_than` /
`narrower_than` twice and downgraded both to `related_to` rather than assume the authority to assert
a subsumption. In this extraction one relation genuinely needed it — constructive criticism as the
source's quoted director defines it is a stricter thing than the source's own definition of a good
note, so every good note is not necessarily constructive in that sense — and `broader_than` was used
with `confidence_basis: extractor_judgement` and a note explaining the reasoning.

**Why it matters.** It suggests the earlier downgrade was a **worker-caution effect rather than a
schema deficiency**: the relation type exists, is defined, and was usable once the reasoning was
written down beside it. Whether that holds elsewhere is for the integrator to judge across lanes.

---

## D-07 — A source may declare its foundations as chosen assumptions rather than as findings

**Status:** OBSERVED · **Layer:** source fidelity / Creative IR fit · **New in this batch (Lane D)**
· **Books: 1**

**What it is.** *Art & Fear* rejects the view that art rests on innate talent with the sentence that
it is fatalistic **even if it is true**, then adopts four premises under its own heading "A Few
Assumptions", stating that it chose them because they place responsibility in the maker's hands.

**Why it matters.** Every other claim the Canon holds is a candidate for being right or wrong — a
physical mechanism, a practitioner's report, a claim about how viewers respond. A premise adopted
for its effect on the person holding it is not that kind of claim and cannot be refuted by evidence
the way a factual one can. Anything that later weighs Canon sources against each other needs to see
the difference, or it will either dismiss the source for lacking evidence it never claimed, or
credit it with evidence it never offered.

**What the schema did and did not do.** It recorded the situation faithfully: the caveats say
`origin: source_stated` that these are offered as assumptions, and the system's whole-system claim
is `source_explicit` with the source's own stated purpose. What it does not do is mark the
**category** — `claim_type` reads `explicit_source_claim` here exactly as it does for a claim about
polarised light. The distinction survives only in prose a reader has to notice.

**Consequence if unchanged.** Sources of craft philosophy, teaching and creative discipline will be
weighed as though they had made factual claims and failed to support them, when in fact they made a
different kind of claim and were explicit about it.

**Proposed (not applied):** a `claim_type` value such as `declared_working_assumption`, or a flag
alongside it. Post-batch revision task only.

---

## D-08 — The most quotable claim in a source is often the one that binds least honestly

**Status:** INFERRED · **Layer:** bindings · **New in this batch (Lane D)** · **Books: 1**

**What it is.** *Art & Fear*'s best-known line is that vision is always ahead of execution *and it
should be*. It reads like a ready-made rule for an evaluator scoring how closely a produced asset
matches its brief: do not treat every residual gap as a defect.

I refused the binding and recorded the refusal in the bindings file. The source's claim is about a
human maker whose own skill lags their own conception, and its stated reason the gap should persist
is that the gap pulls the maker forward. A model generating from a specification has no conception
of its own, and nothing is pulled forward. The resemblance is verbal.

**Why it matters.** Building it would have taken our own tolerance decision — how much brief-drift
we accept — and dressed it in a source's authority. That is precisely the distortion the SPEC-03 /
SPEC-04 split exists to prevent, and it arrived in its most persuasive form: a famous sentence, a
plausible mapping, and a real product question waiting for an answer.

**Consequence if unchanged.** None to the schema; the split worked. The risk is to extractors: an
aphoristic source offers many such sentences, and the pressure to bind is strongest exactly where
the source is most memorable. Recorded so the integrator can check whether other lanes refused
anything, or whether refusals are going unrecorded because nothing asks for them.

**Proposed (not applied):** nothing in the schema. Possibly a convention that considered-and-refused
bindings are recorded, since SPEC-05 already establishes that negative findings are written down.

---

## D-09 — A title-string search is only as good as the other document's punctuation

**Status:** OBSERVED · **Layer:** provenance / method integrity · **New in this batch (Lane D)** ·
**Books: 1**

**What it is.** My first post-checkpoint search for historical material on book 16 used the string
"creativity, inc", with the comma the book's own title carries. `CANON-CURRICULUM-V0.md` writes it
"Creativity Inc" without one, so the search missed it and I recorded "no comparator" in the lane
checkpoint. The re-run, prompted by book 17's search surfacing the same file, found it.

**Why it matters.** The sealed-until-checkpoint rule depends on a search that actually finds what
exists. A missed comparator does not corrupt the fresh extraction — the discipline held, and the
extraction was already committed and pushed — but it produces a false "no historical material"
record, which is a claim about the repository that was not true.

**Consequence if unchanged.** Books get recorded as having no comparator when one exists, and the
integrator's count of compared-versus-uncompared books is wrong in a direction that is invisible.

**What I did:** corrected the book 16 findings and the lane checkpoint, and searched book 17 on
author surnames as well as title strings. **Recommended for other lanes:** search on author surname,
on distinctive concept words, and on the title with and without punctuation.

---

## D-10 — Counter-evidence: when a source really does declare a system, the origin fields say so

**Status:** OBSERVED · **Layer:** systems · **Evidence *for* the current design** · **Books: 1**

**What it is.** Both of book 16's concept systems carry `extractor_synthesis` on their whole-system
claims, because Catmull never assembles his conditions into a mechanism. Two of book 17's three
carry `source_explicit`, because Bayles and Orland do: "A Few Assumptions" is the source's own
heading with its own membership, order and stated purpose, and the three inevitabilities — vision,
uncertainty, knowledge of materials — are named together in one sentence and then given a subsection
each.

**Why it matters.** The origin-marking machinery is the main defence against a system being read as
source evidence when it is our hypothesis. Two books in the same domain, days apart, produced
opposite readings on that field without any adjustment to the method. That is evidence the field
discriminates rather than defaulting.

---

## D-11 — Two books, different material, near-identical evidence profile

**Status:** INFERRED · **Layer:** other (evidence characteristics) · **New in this batch (Lane D)**
· **Books: 2**

**What it is.** Book 16 is a 2014 organisational memoir by a studio president. Book 17 is a 1993
philosophical essay by a painter and a photographer. Their evidence profiles are almost the same:
every object `explicitly_stated` and `practitioner_assertion`, roughly two thirds carrying a stated
mechanism, and **zero** controlled comparison, zero visual demonstration, zero outcome claims in
either. The main difference is that *Art & Fear* argues more (13 of 23 against 9 of 21), which fits
a book trying to change what the reader believes rather than describe a mechanism already running.

**Why it matters.** It suggests evidence profile may track the **domain** — what kind of knowledge
this is — rather than the individual book. If that holds across lanes it is useful: it means the
profile is a real signal about a source class and not an artefact of one author's habits. If it does
not hold, this is a coincidence between two books.

**Status is INFERRED deliberately.** One lane, two books, both hand-classified by the same extractor
on the same day — which is itself a possible explanation for the similarity. Only the integrator,
comparing across lanes and extractors, can tell the two apart.

---

## Book status — Lane D

| Book | Status | Checkpoint | Historical comparator |
|---|---|---|---|
| 16 — Catmull, *Creativity, Inc.* ch.5 | **complete, validated** | `b7f0d47` | no extraction comparator; a pre-batch curriculum judgement exists and converged — see D-09 |
| 17 — Bayles & Orland, *Art & Fear* pp.1–21 | **complete, validated** | `75e4da1` | no extraction comparator; same curriculum judgement, converged |
| 18 — Miller, *Building a StoryBrand* | not started | — | — |
