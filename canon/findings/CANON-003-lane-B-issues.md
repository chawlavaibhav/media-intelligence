# CANON-003 — Lane B issue file

**Lane B:** film / editing / unusual source form · branch `work/canon-003-b`
**Assigned books:** 9 *Grammar of the Edit* · 10 Murch *In the Blink of an Eye* ·
11 Kenworthy *Master Shots* · 12 Ondaatje *The Conversations*

This file replaces the shared batch issue ledger for the duration of parallel execution. Lane B does
not edit `CANON-003-batch-issue-ledger.md`, the synthesis, the Controller Brief or `canon/HANDOFF.md`.

**Isolation:** no other lane's new findings have been read. The existing batch ledger has not been
opened or used as a checklist of what to look for. Shared starting evidence is the task file, the
parallel amendment, the source inventory, the pre-parallel handover checkpoint, and the CANON-001/002
decisions that define the frozen method.

**Issue IDs** are `LB-nn` so they cannot collide with the pre-parallel `B-nn` series or another
lane's.

---

## Status

| Book | Status | Objects | Visual | Historical comparison |
|---|---|---|---|---|
| 9 — *Grammar of the Edit*, ch.3–5 | **complete** | 60 | verified page-level | pending — after checkpoint |
| 10 — *In the Blink of an Eye* | not started | — | — | — |
| 11 — *Master Shots* | not started | — | — | — |
| 12 — *The Conversations* | not started | — | — | — |

---

# Issues

## LB-01 — SPEC-03 cannot express that two things are siblings, alternatives, or orthogonal classifications

**Plain English.** When a source teaches two ideas that sit *beside* each other rather than one above
the other, the schema has nowhere to put the connection. SPEC-03 lets an extraction say that A is a
kind of B, that A depends on B, that A contradicts B, or that A and B trade off. It has no way to say
that A and B are two members of a set, two alternative methods for the same decision, or two
independent ways of classifying the same event.

**Where observed.** Book 9, *Grammar of the Edit*. **1 distinct book so far.**

**Status.** OBSERVED — the vocabulary is fixed in SPEC-03 and the gap is checkable against it.
The judgement that these particular thirteen connections have no honest home is INFERRED.

**Affected layer.** Source fidelity; systems.

**New or recurrence.** New in this batch as far as Lane B's evidence goes.

**What actually happened.** Thirteen connections were written during drafting using `related_to`,
which is **not** in SPEC-03's `intra_source_relations` vocabulary — it belongs to SPEC-05's ontology
layer. Mechanical validation caught all thirteen. Five were then remapped to an existing SPEC-03
relation that genuinely fits. The remaining eight, and their reverse directions, were **deleted**
rather than forced into a relation asserting more than the source supports. No relation type was
invented; the human-approval trigger was not touched.

**Connections lost, in full:**

| Between | What the source says | Why nothing fits |
|---|---|---|
| `0039` five edit categories ↔ `0024` four transitions | Two independent classifications of one event; the source's own review confirms it — "the combined edit is still just a cut, dissolve, or wipe at one transition" | Neither generalises the other; they do not conflict; they are orthogonal axes |
| `0009` the felt "beat" ↔ `0053` describe-the-shot-aloud | Two alternative methods for deciding one thing: how long a shot runs | Alternatives, not specialisations; the source never relates them |
| `0013` jump cut ↔ `0028` dissolve duration | A too-short dissolve can imitate a jump cut — a third cause of one named failure | Cause-to-named-failure, which the vocabulary has no term for |
| `0021` sound contradicting picture ↔ `0043` concept edit | One juxtaposition mechanism operating in two modalities | Shared mechanism across modalities; `same_mechanism` exists in SPEC-05, not SPEC-03 |
| `0018` continuity of position ↔ `0010` eye trace | The same frame-side logic, once as a constraint and once as a device | Same substrate, opposite use |
| `0027` cut usage ↔ `0022` split edit | The assemble edit described from two sides — "all cuts", "all butt-cuts" | Two descriptions of one practice |
| `0032` dissolves in news ↔ `0052` the MTV effect | The section's two explicitly dated claims about changing practice | A meta-grouping about evidence type, not about content |
| `0036` natural wipe ↔ `0045` combined edit | Both require pre-production planning and are unavailable to an editor working from arbitrary coverage | A shared precondition |

**Practical consequence if unchanged.** The strongest structural fact about this book — that it
operates two independent taxonomies over the same events — survives only as prose inside two
`caveats` fields. Nothing can retrieve it, count it, or notice the same pattern in another source. A
later pass asking "which sources classify along more than one axis?" would get nothing.

**Proposed fix — PROPOSAL ONLY, not applied.** Consider one additional `intra_source_relations` value
covering non-hierarchical association, or permit SPEC-05's `related_to` inside SPEC-03 with a
required note. **Weigh against:** CANON-001 decision 3 deliberately granted `distinct_from` to the
ontology layer and *explicitly withheld it* from `intra_source_relations`, which suggests the
narrowness is intentional. The alternative reading is that a SourceConceptSystem is the correct home
for sibling structure and was underused here — though a system for every loose pair would be its own
distortion. One book is not enough to choose. Watch for recurrence in books 10–12.

---

## LB-02 — a source can name a framework as fixed and apply it as variable

**Plain English.** *Grammar of the Edit* announces six elements that make an edit good, repeats the
number throughout, and then applies a different subset almost every time it uses them — without ever
saying the set changes.

**Where observed.** Book 9. **1 distinct book.**

**Status.** OBSERVED for the individual departures; each is countable on a named page. INFERRED that
they form one pattern rather than several unrelated remarks.

**Affected layer.** Source fidelity; systems; Creative IR fit.

**The evidence, checkable.**

| Applied to | Elements walked through | Departure |
|---|---|---|
| The cut (pp.76–78) | all six | — |
| The dissolve (pp.80–82) | six, but continuity dropped and **time** added | silent |
| The wipe (pp.84–85) | six listed, composition and camera angle **explicitly waived** | stated |
| The fade (pp.86–87) | **four** — motivation, composition, sound, time | silent |
| Action edit (pp.88–90) | all six | — |
| Screen position edit (p.91) | "not every ... will address all six" | stated |
| Concept edit (p.94) | "The six elements need not be applied here" | stated |

Three departures are the source's own words. Four are silent, including an unannounced seventh
element — time — that appears for every transition possessing a duration and is never added to the
named list.

**Why it matters.** An extraction that recorded only the framing claim would hand the product a
six-item checklist the source does not itself apply. The failure is not that the source is careless:
elements drop out exactly where they are inapplicable, so the operative rule appears to be
*applicability*, not membership — but that rule is never written down, so an extractor either
notices the pattern or reports a rule the author does not hold.

**Practical consequence if unchanged.** Retrieving a named framework without its exceptions
misrepresents the source. Recorded as `scs_gote_c003_002` and bound as a `retrieval_governance`
binding (`bnd_gote_c003_0010`), so this book is handled. The general question — how often do sources
state a framework more rigidly than they use it — is open.

**Proposed fix — PROPOSAL ONLY.** None yet. The existing schema handled this case without strain: a
SourceConceptSystem of type `mutual_qualification` with `extractor_synthesis` origin carried it, and
a governance binding made the retrieval consequence explicit. This may be evidence **for** the
current design rather than against it. Watch whether books 10–12 produce frameworks that need the
same treatment.

---

## LB-03 — text printed inside artwork is lost silently, and no cheap check detects it

**Plain English.** Where a book prints words inside a diagram, those words vanish in text extraction,
and nothing in the extracted text shows that anything is missing.

**Where observed.** Book 9. **1 distinct book.**

**Status.** OBSERVED — verified by searching the whole book's extracted text.

**Affected layer.** Visual completeness; source fidelity.

**New or recurrence.** Related to the pre-batch hypothesis that visual evidence can disappear
entirely in plain text, but this is a **different mechanism**: not a lost picture, a lost *string*.

**Evidence.** `WRONG SIDE OF LINE`, typeset inside Figure 5.5's third diagram, occurs **zero** times
in the extracted text of the section and zero times in the extracted text of the whole 225-page book.
`THE LINE`, inside Figure 5.3, likewise. The first label is what tells a reader which of the three
diagrams is the error case.

**Why it matters, and how it differs from what the batch has already seen.** Book 5's buried section
was caught by a contents page — an independent index of what should be present. **There is no
equivalent index for text inside artwork.** A contents page lists sections; nothing lists the words
drawn into figures. Detection required rendering and reading the pages, which is the expensive method
the batch is trying to characterise the need for.

**Practical consequence if unchanged.** For diagram-heavy sources, text-only extraction loses
polarity markers — the labels that say *this one is the error* — while leaving the surrounding prose
apparently intact and confident. This is the profile that produces confidently wrong extraction.

**Proposed fix — PROPOSAL ONLY.** Where a PDF is native, a cheap partial detector may exist: compare
the count of text objects inside figure bounding boxes against the extracted stream. Not attempted
here; it would be a method change.

---

## LB-04 — a source's own cross-reference can be wrong, and only a visual pass reveals it

**Plain English.** The book points the reader at the wrong figure. Nothing in the text could tell you.

**Where observed.** Book 9. **1 distinct book.**

**Status.** OBSERVED.

**Affected layer.** Source fidelity; provenance.

**Evidence.** Printed page 61 ends a paragraph about the sound bridge with "(see Figure 3.4E and F)".
Figure 3.4 is on page 64, has three panels A–C, and shows camera-angle similarity. The train-whistle
sound bridge the sentence describes is Figure 3.2E and F, on the same page as the sentence. Verified
by rendering both pages and counting panels.

**Why it matters.** An extractor working from text alone sees a claim with a figure reference
attached and has every reason to trust it. Attaching the sound-bridge claim to Figure 3.4 would have
recorded the source as demonstrating something it does not. The error is small and harmless in the
book; the class is not.

**Practical consequence if unchanged.** `provenance.figure_refs` inherits the source's errors
silently. The field records what the source *says* supports a claim, and there is no marking to
distinguish a verified figure reference from a copied one. This extraction cites Figure 3.2E–F —
what the source actually shows — and records the misdirection as a caveat.

**Proposed fix — PROPOSAL ONLY.** None. Recorded so that if a second source in this batch shows a
broken internal reference, the pair becomes evidence that `figure_refs` needs a verification marking.

---

## LB-05 — visual loss is not uniform, and a text-redundant figure can be identified by its reason

**Plain English.** Not every figure is lost in text. One in this book survives completely, and it
survives for a statable reason.

**Where observed.** Book 9. **1 distinct book.** Logged as **evidence against** treating visual loss
as a uniform property of figure-bearing sources.

**Status.** OBSERVED.

**Affected layer.** Visual completeness.

**Evidence.** Figure 5.2 draws a house on a hillside, chimney smoke, a man walking up the path, a
setting sun. The prose beside it reads: "There is a house in the hills, there is smoke coming out of
the chimney, a man is walking to the house, it is evening because the sun is setting. Cut!" Every
element is enumerated, because the method being taught **is** describing the shot aloud. The figure
is fully recoverable from text.

**Why it matters.** The batch's working picture is that figure-bearing sources lose information to
text extraction, with severity tracking detectability. This is a case where the loss is **zero**, and
the reason is structural rather than lucky: where a source's pedagogy requires the picture to be
described in words, the description is in the text. That is a predictable property, not an accident.

**Practical consequence.** A blanket rule that figure-bearing sources need a visual pass would be
correct but imprecise. Some figures are provably safe. Whether this generalises is unknown from one
instance.

---

## LB-06 — an enumerative source produces a high object count without any granularity exception

**Plain English.** This book listed things constantly, so it produced many more objects than earlier
books — without needing any new rule.

**Where observed.** Book 9. **1 distinct book.**

**Status.** OBSERVED.

**Affected layer.** Granularity.

**New or recurrence.** Bears on the open CANON-003 question of whether the V0 granularity rule
remains usable across source shapes.

**Evidence.** 60 SourceKnowledge objects from 55 printed pages — about **1.1 objects per page**,
against 0.85 for book 1 (17 objects, 20 pages). The source enumerates six elements, applies them to
four transitions, defines five edit categories and lists seven general practices, with each item
given its own heading, its own example and often its own figure.

**The rule held.** The V0 test — split when a claim can be retrieved, supported, contradicted or
qualified independently — was applied unchanged and needed **no invented exception**. Ambiguous cases
were resolved toward the least assumptive reading and recorded rather than resolved by new policy:

- *Split:* the disposal rule "a shot that adds no new information may not belong, however beautiful"
  was separated from the information rule it follows from, because it can be contradicted on its own.
- *Merged:* removing expected sound and substituting contradicting sound were kept as **one** object
  with two examples, because the source introduces both under a single sentence and gives them one
  mechanism. Splitting would have asserted a distinction the source does not make.
- *Merged:* the cut-away and the insert shot were kept as one SourceKnowledge object — same action,
  same stated mechanism, two names for two problems — while the ontology layer keeps **both source
  terms** related by `same_mechanism`, so no vocabulary was lost.
- *Folded:* "editing is creating" was folded into the closing rule about creativity overruling
  grammar rather than made its own object, because its substantive content restates the book's
  Introduction.

**Practical consequence.** Object counts across this batch are not comparable without knowing section
size and source shape. Stated explicitly in the file header and the provenance record so a reader
does not read 60 as a change in method or in quality.

---

## LB-07 — nearly every binding this source supports needs an observation unit larger than a frame

**Plain English.** This book is almost entirely about the relationship *between* shots, so almost
nothing it teaches can be checked by looking at a single image.

**Where observed.** Book 9. **1 distinct book** — but this is the recurrence of a concern SPEC-04
already records from the six-probe work, now met at full strength.

**Status.** OBSERVED.

**Affected layer.** Bindings; Creative IR fit.

**Evidence.** Of 11 operational bindings, 5 are evaluation bindings and **every one** required an
`observation_unit` of `shot_pair` or `sequence`. Not one claim in 60 supported a frame-level
evaluation binding.

**The sharpest case is `bnd_gote_c003_0004`.** The source claims a bad edit impairs the viewer's
absorption of information presented *after* it, because the mind stays occupied justifying the
anomaly. If true, the cost of a defective transition is not located at the transition, and an
evaluator that scores transitions independently and sums them would systematically misprice a
sequence. That is a constraint on how edit-level judgements may be **aggregated**, which
`observation_unit` alone does not express — the field says what a check must *see*, not how its
results may be *combined*.

**Practical consequence if unchanged.** SPEC-04's `observation_unit` handles "this check needs two
shots". It does not handle "this defect's cost appears elsewhere than where the defect is". Recorded
as a binding with `role: [constrains]` and an explicit status reason that the underlying claim is
unmeasured.

**Proposed fix — PROPOSAL ONLY.** None yet. The claim is a practitioner assertion with a stated
mechanism and no evidence, and should not drive a schema change on one source's say-so. Flagged
because if a second source in this batch makes a comparable downstream-cost claim, the pair is worth
attention.

---

## LB-08 — SPEC-01 has a continuity field and this batch has now found something to put in it

**Plain English.** The product schema reserved a slot for continuity requirements and left it empty.
This book fills it.

**Where observed.** Book 9. **1 distinct book.** Logged as **evidence for** the current design.

**Status.** OBSERVED.

**Affected layer.** Creative IR fit; bindings.

**Evidence.** `VideoCreativeExtension.continuity_requirements` exists in SPEC-01 v0.1 with no stated
contents. SPEC-01's own note says "the filmmaking and editing books will land almost entirely here".
This source supplies a four-way division — content, movement, position, sound — each naming what must
be held constant, which the field could take directly (`bnd_gote_c003_0006`).

**The caveat that matters.** The source addresses an editor choosing among footage that already
exists, and every one of its remedies assumes a pool of alternative coverage to cut away to. A
specification field describes material *before* it exists, and a generated single take has no
alternative coverage. The four divisions are a good shape for describing the requirement; whether
they are a good shape for *specifying* one is untested and is recorded as a limit on the binding.

**Practical consequence.** A prediction SPEC-01 made about this source class turned out right. Worth
carrying to the synthesis as a positive result rather than an issue.

---

## Method-integrity note — an error I made, and how it was caught

Thirteen relations were drafted using a relation type SPEC-03 does not define (`related_to`, which
belongs to SPEC-05). This was **not** a deliberate schema extension; it was carelessness, reaching
for a vocabulary from an adjacent layer. It was caught by mechanical validation before the checkpoint
and resolved without inventing anything — five remapped, eight deleted.

Recording it for two reasons. First, honesty: the frozen method held here because a script enforced
it, not because I did. Second, it is evidence about the instrument — **mechanical validation caught a
fidelity error that reading would probably not have.** The drafted relations were individually
plausible and read naturally; only the fixed vocabulary check exposed them. That is an argument for
validating before every checkpoint rather than at the end of a book.

---

## LB-09 — two books by the same authors are not two independent origins, and nothing records that

*Added after book 9's fresh checkpoint `ddef98d`, from the post-checkpoint comparison. Marked as
post-checkpoint so it is not read as evidence the fresh pass produced.*

**Plain English.** SPEC-05 allows a claim that several sources describe the same thing, but only when
the sources are independent. *Grammar of the Shot* and *Grammar of the Edit* are by the same two
authors, in the same series, from the same publisher, a year apart, each referring to the other.
Agreement between them is one position stated twice. Nothing in the schema records that.

**Where observed.** Book 9 compared against book 1 (*Grammar of the Shot* ch.4, pre-parallel, shared
starting evidence). **1 distinct book pair.**

**Status.** OBSERVED — the shared authorship is on both title pages. The consequence for aggregation
is INFERRED, since no aggregation pass has run yet.

**Affected layer.** Ontology; cross-source synthesis.

**New or recurrence.** New. Related in spirit to the pre-parallel finding that the isolation rule had
a hole because the specs quote books the batch processes — both are cases of an assumed independence
that does not hold — but the mechanism is different: that one was contamination of the extractor,
this is contamination of the *evidence base*.

**The evidence.** Four terms now exist in two source files with near-identical meaning:

| Term | In book 1 | In book 9 |
|---|---|---|
| `axis_of_action` / `action_line` | `t_gos_*` | `t_gote_c003_0019` |
| `screen_direction` | `t_gos_*` | `t_gote_c003_0018` |
| `jump_cut` | `t_gos_*` | `t_gote_c003_0031` |
| `eye_line_match` / `eye_trace` | `t_gos_*` | `t_gote_c003_0021` |

Both books also independently state that their own rules are defeasible by creative intent — book 1
as "very few absolutes ... a creative reason is sufficient warrant", book 9 as "effective creativity
overrules grammar". Under a naive count that is two sources agreeing on a meta-position about craft
rules. It is one authorial position, restated.

**Why it matters.** SPEC-05's `cross_source_concept` is the only concept kind that makes a claim
about the world, and the only one requiring two or more independent origins. It is the join the whole
architecture is built to support. Its guard is a count of `origin_ref` values, and `origin_ref` is a
source identifier. **Two source identifiers can share an author, a publisher, a series, and a
decade.** A promotion rule that counts distinct `origin_ref`s would pass this pair.

**Practical consequence if unchanged.** The first `cross_source_concept` this corpus produces could
be built on a same-author pair and presented as convergent evidence. Because
`children_are_authoritative` is load-bearing, the children would still carry the right detail — but
the parent would assert an agreement that does not exist, and the count at the parent is exactly what
an aggregation layer would report.

**Proposed fix — PROPOSAL ONLY, not applied.** An independence check before promoting to
`cross_source_concept`, drawing on author and publisher rather than source id alone. **Weigh against:**
this is one pair, it was found by hand, and the batch has not yet attempted a single cross-source
promotion, so the failure is predicted rather than observed. It may also be cheaper to handle at the
promotion review — SPEC-05 already requires human review to promote `potentially_equivalent_to` to
`same_failure_family`, so a reviewer might catch it without a schema change.

**A note on how this was found.** It surfaced because the batch's own selection policy deliberately
chose a companion volume for source-shape diversity. The selection rule that made the corpus broader
also introduced the dependency, and the two facts arrived together.

---

## Correction to the inventory's expectation for book 9

The source inventory selected *Grammar of the Edit* as a test of "whether two books by the same
authors produce near-duplicate knowledge". **They do not.** The overlap is about 13% — eight of sixty
objects — and where the two books share a concept, the shooting book states it as a camera action and
the editing book as a selection constraint on footage that already exists. The 30-degree rule is the
clearest instance: "move the camera at least 30 degrees" against "place shots more than 30 degrees
apart".

That is a more useful result than the near-duplication the inventory anticipated, and it changes the
question. The risk from a companion volume is not redundant knowledge; it is **false independence**,
which is LB-09.

---

# Book 10 — *In the Blink of an Eye* (issues LB-10 onward)

*Written before book 10's fresh checkpoint. LB-09 above was added after book 9's checkpoint and is
marked as such; everything from LB-10 to LB-14 is pre-checkpoint for book 10.*

## LB-10 — SPEC-03 can record that a list is ranked, but not by how much

**Plain English.** Murch's Rule of Six is not just an order, it is an order with sizes. He puts
numbers on the six criteria — 51%, 23%, 10%, 7%, 5%, 4% — and the numbers say something the order
alone does not: the first item is worth more than the other five put together. The schema can store
the order. It has nowhere to put the sizes.

**Where observed.** Book 10, *In the Blink of an Eye*. **1 distinct book.**

**Status.** OBSERVED. `priority_order` and `members[].order` are the only ordering structures SPEC-03
defines, and neither takes a magnitude. Checkable against the spec.

**Affected layer.** Systems; source fidelity.

**This is the case the operator asked to be tested.** The instruction was that Murch's priority
ordering be represented faithfully using existing structures, and that if the schema proved
insufficient this be recorded as evidence rather than met by inventing a new structure. That is what
was done. `scs_murch_c003_001` uses the existing `priority_order` type, with six members carrying
`order` 1–6, `ordering.scheme: source_numbered` and `origin: source_stated`. Nothing was invented.

**What is lost.** The percentages are cardinal, not ordinal, and they carry two things the ranking
cannot:

1. **Emotion outweighs everything else combined.** 51 against 23+10+7+5+4 = 49. The choice of 51 is
   the smallest whole percentage constituting a majority, which is almost certainly deliberate. The
   source states the consequence in words as well: "the top of the list — emotion — is worth more
   than all five of the things underneath it."
2. **The gaps are wildly uneven.** The distance from rank 2 to rank 3 (23 → 10) is larger than the
   entire spread from rank 3 to rank 6 (10 → 4). Ranks 3, 4, 5 and 6 are nearly a flat cluster.

Read as `order: 1, 2, 3, 4, 5, 6`, the Rule of Six presents as six roughly comparable considerations
in a preferred sequence. **That is close to the opposite of the argument.** The whole point is that
the list is top-heavy.

**Where the numbers actually live.** Verbatim inside `sk_murch_c003_0020` through `0025`, one per
criterion, and in `sk_murch_c003_0029`, which records the source's own gloss on what they mean. They
are readable by a person and invisible to anything mechanical.

**A second, smaller insufficiency in the same system.** The source claims its ordering is
*perceptual* as well as *preferential* — satisfying a higher item tends to obscure failures of lower
ones, and not the reverse (`sk_murch_c003_0028`). That is a property OF the ordering, but
`internal_structure.ordering` has only `scheme` and `origin`, so the claim is carried as an ordinary
member of the system alongside the criteria it describes.

**Practical consequence if unchanged.** Any consumer reading the system mechanically gets a rank
order and silently loses the weighting. For a framework whose entire content is that one item
dominates, that is a material distortion. It is also the specific way this could go wrong quietly:
the object validates, reads sensibly, and misrepresents the source.

**Proposed fix — PROPOSAL ONLY, not applied.** An optional `weight` or `interval_note` on
`members[]`, populated only where a source states one. **Weigh against:** exactly one book in ten so
far has supplied numeric weights, and this source hedges its own — "slightly tongue-in-cheek, but not
completely". A field that is empty for nine books out of ten and marked not-quite-serious in the
tenth is thin justification for changing a frozen schema. The alternative, which costs nothing, is to
require that a `priority_order` system's `system_level_uncertainty` state explicitly what the
ordering does *not* capture — which is what was done here.

---

## LB-11 — a remedy that acts on a person, not on material, has no `executable_by` value

**Plain English.** SPEC-05 asks, for every repair, how it could be carried out — by a camera, by
regenerating, by compositing, by a human editing. Murch's remedy for a director's distorted judgement
is: send him to the Alps for two weeks. None of the four answers fits.

**Where observed.** Book 10. **1 distinct book.**

**Status.** OBSERVED.

**Affected layer.** Ontology; bindings.

**Evidence.** `t_murch_c003_0020`, the two-week barrier between shooting and editing, is recorded
with `executable_by: [unknown]`. SPEC-05's vocabulary is `physical_production`,
`generative_respecification`, `deterministic_composite`, `human_edit`, `unknown` — every positive
value describes an operation performed on *material*. This remedy is a scheduling and organisational
practice performed on a *person*, to change the state they are in when they later judge the material.

**Why it matters, and why it is more than a vocabulary gap.** SPEC-05 introduced `executable_by`
precisely so that a repair with no generative equivalent would be *visible* rather than silently
bridged, and it works: `unknown` is honest and the gap is legible. But it flattens a real
distinction. A repair marked `unknown` because nobody has worked out how to do it is a different
thing from a repair marked `unknown` because it is not the kind of thing this field is about. Two
other Murch remedies sit near the same edge — the paper dolls beside the editing screen, and "see
only what's on the screen", both recorded as `human_edit` because a human does act on the material,
though what they really change is the *conditions of judgement*.

**Practical consequence if unchanged.** A class of practitioner knowledge — how to put yourself in a
state where you judge well — collapses into `unknown` and becomes indistinguishable from
untranslatable physical technique. Given that book 10 produced five governance bindings out of eight,
against one out of eleven for book 9, this class may not be marginal.

**Proposed fix — PROPOSAL ONLY.** None yet. One book. Worth watching in books 11 and 12, and in the
creative-process books Lane D is processing, which are likely to be dense in exactly this kind of
knowledge.

---

## LB-12 — a scanned two-page spread interleaves like a two-column page, and the damage is removable

**Plain English.** This book's PDF puts two printed pages on every sheet. Extracted naively, the text
reads straight across both pages and splices two unrelated arguments together — the same failure that
blocked Lupton. Cropping each sheet in half before extracting removes it completely.

**Where observed.** Book 10. **1 distinct book.**

**Status.** OBSERVED. Both extractions were produced and compared.

**Affected layer.** Source fidelity; provenance.

**New or recurrence.** A **recurrence of the interleaving failure mode**, with a materially different
outcome.

**Evidence.** Naive full-page extraction of spread 15 produced: `"and over here we have the Mona
Lisa, and, by the"` (left page) → `"I classes is what I'm going to call three-dimensional"` (right
page) → `"way, look at these floor tiles ... " If you are on a tour,"` (left page). Cropped
extraction of the same spread produces two clean single-column pages.

**Why this matters for the batch.** The distinction it draws is between a *file* that is corrupt and
an *extraction* that is. Interleaving here was an artifact of asking a tool to read a landscape sheet
as one column; the underlying artifact was intact, and respecting its geometry recovered it exactly.
No character was altered and nothing was inferred — both extractions contain the same words in a
different order.

**Deliberate limit on this finding.** This lane has **not** examined the Lupton anchor and is
**not** claiming its block was avoidable. Lupton was blocked on a pre-extracted repository text file,
which is a different situation from having the original artifact in hand. The claim here is only the
narrow one: **"interleaved" describes an output, and is not by itself a verdict on a source.** Whether
that bears on any other blocked book is for the integrator to consider, not this lane.

**Practical consequence if unchanged.** A source could be blocked as corrupt when the corruption
belongs to the extraction command. Given that the batch has blocked four books and treats blocking as
final, the cost of that error is a book.

**Proposed fix — PROPOSAL ONLY.** Before recording `blocked_source_integrity` for interleaving,
check whether the page geometry explains it — landscape aspect, spread layout, multi-column setting —
and if so re-extract respecting it. This is arguably not a method change at all but ordinary care in
reading a file.

---

## LB-13 — visual dependence is set by the author's mode of argument, not by the domain

**Plain English.** Two books in this lane teach the same subject. One is unreadable without its
pictures; the other has none. Knowing the subject tells you nothing about the risk.

**Where observed.** Books 9 and 10. **2 distinct books, same domain.** Logged as **evidence against**
treating visual-loss risk as a property of a source's field.

**Status.** OBSERVED.

**Affected layer.** Visual completeness.

**Evidence.**

| | Book 9 — *Grammar of the Edit* | Book 10 — *In the Blink of an Eye* |
|---|---|---|
| Subject | when and why to cut | when and why to cut |
| Pages processed | 55 | 25 |
| Figures | 23 | **0** |
| Controlled comparisons in figures | 3 | 0 |
| Recoverable from text alone | no | **entirely** |
| Text baked into artwork | 2 labels lost silently | none |

Both are film-editing books. Both were selected into the same lane for the same domain quota. The
visual-loss risk is total in one and zero in the other, and the difference is what kind of writer
each is: one demonstrates and one argues.

**Why it matters.** A selection or triage rule of the form "photography and filmmaking books need a
visual pass, process books do not" would be wrong in both directions. The batch's inventory already
classifies sources by whether page renders are available; this suggests that is the wrong axis on its
own, because availability does not tell you whether anything would be found.

**Practical consequence.** Visual-pass cost cannot be predicted from a book's subject before opening
it. A cheap early signal does exist and cost nothing here: counting figure references in the
extracted text. Book 10's section contains none, which was confirmed by rendering and reading.

---

## LB-14 — a transcribed lecture can defer its own central question past any reasonable window

**Plain English.** Murch asks the book's main question on page 9 and answers it on page 58. Any
extraction of a normal-sized section will therefore capture the question without the answer.

**Where observed.** Book 10. **1 distinct book.**

**Status.** OBSERVED.

**Affected layer.** Source fidelity; granularity.

**Evidence.** Printed page 9: "the central fact of all this is that cuts do work. But the question
still remains: Why? ... We will get back to this mystery in a few moments." The answer — John
Huston's remark about blinking, which the book is named after — arrives at printed pages 58–64,
thirty-three pages later.

**How the extraction handled it.** `sk_murch_c003_0005` records the question with
`source_uncertainty: source_asks_open_question` and a caveat naming where the answer lies. It is not
recorded as unanswered, and nothing from pp.58–64 was imported. The provenance record states the
boundary.

**Why it matters beyond this book.** The batch's per-book procedure asks for "a coherent
representative section large enough to expose the author's reasoning system", which implicitly
assumes an argument is locally complete. A textbook chapter usually is. **A transcribed lecture is
not organised that way** — a speaker can raise something, digress for fifty minutes, and return. The
same will likely be true of book 12, *The Conversations*, which is an interview transcript, and this
is worth carrying forward into that extraction.

**Practical consequence if unchanged.** A windowed extraction of a discursive source can record a
question as open when the source answers it elsewhere. `source_asks_open_question` is a field about
the SOURCE's uncertainty, and using it for a claim the source does in fact resolve later would be a
misrepresentation — which is why the caveat naming the location was necessary here and why the field
alone was not sufficient.

**Proposed fix — PROPOSAL ONLY.** None. The existing fields handled it once a caveat carried the
location. Recorded so that if book 12 forces the same manoeuvre, the pair becomes evidence that
discursive sources need an explicit convention rather than an ad-hoc caveat.
