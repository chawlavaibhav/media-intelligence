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
