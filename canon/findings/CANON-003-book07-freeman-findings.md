# CANON-003 book 7 — Michael Freeman, *The Photographer's Eye: A Graphic Guide*

**Lane:** A · **Fresh checkpoint:** `5f95755` · **Date:** 24 Aug 2026
**Section:** Parts 1–3 (*Framing*, *Placing*, *Dividing*), 24 cases, converted-PDF pages 12–70
**Method:** CANON-002-era frozen instrument. No schema, granularity, ontology or visual-pass change
was made. Two schema gaps were found and **recorded, not fixed.**

---

## 1. What this book is

A photography composition manual built as roughly eighty "cases". Each case is one photograph the
author made, with a first-person account of the decisions behind it and a set of graphic
deconstructions — diagrams laid over or beside the picture showing where the divisions fall and
where the eye goes.

The author states his method in the introduction, and it matters for everything below:

> "Words to a necessary minimum, with visuals carrying the story."

## 2. Result

34 SourceKnowledge objects · 5 SourceConceptSystems · 46 terms · 12 relations · 5 concepts ·
8 bindings. All validate.

**No historical comparator exists.** Searched after the checkpoint. There is no Freeman atom file
and no Freeman migration audit; the six historical extractions cover only the original probes.
Recorded as `no historical comparator`. Fourth such book in the batch.

## 3. Two provenance errors in the batch inventory, corrected here

Both were found by checking rather than assuming, and both are the sort of error that would have
propagated silently.

**The book is not the one that was selected.** The inventory lists this source as *The
Photographer's Eye* and describes it as overlapping Molly Bang's territory. The file's title page,
metadata and imprint all say *The Photographer's Eye: **A Graphic Guide***, Focal Press 2013 — and
the book opens by distinguishing itself from the earlier title: *"This book takes as it's starting
point my earlier The Photographer's Eye."* The filename has fused the two books' subtitles.

The domain selection survives: the photography quota asked for composition for photography and that
is what this is. The identification did not.

**The PDF is a calibre conversion, so it has no printed page — and this one is more dangerous than
the EPUB case in book 6.** The inventory placed this source in the class where "a visual pass can
recover the actual printed page." Rendering a page shows calibre's A4 reflow: running text with the
photographs dropped in beneath at whatever size the converter chose.

This was *proved*, using the book's own cross-references. The section contains five and **every one
points somewhere else in this copy** — the text cites SQUARE as page 22 when it is at page 29 and
page 22 is FRAME-FIT; it cites SYMMETRICAL as `page_52` when it is at page 61. One reference,
`page_52`, is a broken hyperlink anchor left in the running text as a literal string.

Two consequences. The numbers on these pages are the converter's, so every object in this
extraction carries `page_start: null` and a converted-PDF locator; citing them as printed pages
would have been a fabrication. And a reader — or a retrieval system — following a cross-reference
inside this copy silently lands on the wrong content.

**Why this is worse than book 6's EPUB.** There, no page exists at all and the limitation announces
itself. Here a page *can* be rendered, so a visual pass that reasons "it is a PDF, therefore I can
see the page" would record verified page-level completeness for a layout the author never made.
**The affordance is false rather than absent.**

## 4. The sharpest visual-loss test in the batch, because the author declares the loss in advance

Elsewhere in this batch, visual loss has had to be inferred by comparing what a figure shows against
what its caption says. Here the author states up front that the words are deliberately insufficient.
Any claim extracted from text alone is known to be partial before it is written — which makes this
the strongest available check on whether the frozen visual-pass method actually catches loss.

It caught three things, each a different kind.

**A diagram that measures what the text only asserts.** The prose says the three placement zones are
"approximate" and that any rule of thirds "can only be approximate". The accompanying diagram draws
all three zones with soft gradient edges, wide enough that adjacent zones visibly overlap. The word
is an adjective; the picture is a quantity. A text-only pass keeps the claim and loses the only
thing that makes it usable.

**A counterfactual reduced to its conclusion.** For the classical-division case the author
manipulated his own photograph so the tonal boundaries fell on the Golden Section, showed that it
fails, then showed the tone-equalised version that would work — plus an exploded rendering
separating the frame's three depth planes. In text all of that survives as one sentence: *"It
doesn't work well, and the bright sky over-dominates."* That is the conclusion with the experiment
deleted.

**A demonstration that performs itself.** The reveal case claims *"it takes the eye a moment to slip
down to the corner to notice it."* Looking at the photograph, that is exactly what happens — the
bright mausoleums take the attention and the tiny white figure has to be hunted for. The evidence is
the delay in the viewer's own looking.

That third one is a category this batch has not previously had to describe. The other losses have
been losses of *information* — a colour, a section, a set of labels. This is the loss of an
*experience that constitutes the evidence*. Text can report that the effect exists. It cannot
produce it, and no fidelity of description would.

**A fourth observation, about pipelines rather than this book.** Text density is a poor proxy for
content here. Case pages carry 150–280 words; the pages following them carry 4–65 and are almost
entirely image. Any triage that sampled or weighted by text volume would discard exactly the pages
this book puts its argument on — and such triage is an obvious efficiency for a large ingestion.

## 5. The object count: a clean test of the concern raised after book 6

After book 6 this lane logged a worry (LA-01) that per-book object counts might be measuring
chapter length rather than source richness. Book 7 tests it almost perfectly, because the section
sizes nearly match:

| | Book 6 — Samara | Book 7 — Freeman |
|---|---|---|
| Section | 57 printed pages | 59 converted pages |
| Words | 14,737 | 5,748 |
| Objects | **79** | **34** |
| Objects per page | 1.4 | 0.6 |

Same lane, same frozen method, same week, near-identical page counts — and 2.3× fewer objects.

**So source shape is the dominant term and section size is a real but secondary confound.** Books
cannot be compared on raw counts, but the differences between them are not artefacts of how long a
chapter happened to be. That is a more useful conclusion than either "counts are comparable" or
"counts are meaningless", and it took two books under one method to reach.

The V0 granularity rule decided every case again, on a third distinct source shape — a book of
worked cases where the claim is thin and the example is thick, the reverse of the rule-dense manual.

## 6. Two schema gaps found. Neither was fixed.

**`creative.hierarchy` cannot express a traversal — a recurrence of a CANON-002 hypothesis.**
CANON-003 explicitly carried forward the concern that `creative.hierarchy` may not express a
definite traversal or end, and asked that recurrences be watched for. This source produces three,
independently:

- the two shot, where *"the attention plays ping-pong between the two subjects"* — it goes, returns,
  and goes again;
- the reveal, where attention lands on one place, lingers, wanders, and discovers a second;
- the eccentric division, where the eye arrives at the one sharp element and is then sent to the
  real subject.

`creative.hierarchy` is a ranked list. It can record that the actor outranks the actress. It cannot
record that the eye is meant to go there and come back, which is the entire content of the claim.

Recorded as `bnd_fre_c003_0005`, a binding that asserts a gap rather than a use. Nothing was added.
One honest qualification: two of the three claims are borrowed from cinema by the author's own
account, so this may be a still-image schema meeting a moving-image idea rather than a defect.

**`observation_unit` cannot express this source's own condition.** SPEC-04 requires evaluation
bindings to name the unit of observation, with values `frame · shot · shot_pair · sequence ·
whole_asset · asset_set_over_time`. Every one of those describes **how many assets are observed.**

This source states a condition of a different kind. Whether a figure included to give scale
registers at all depends on the **print size** — one of the author's two versions *"works under one
condition: It has to be printed big."* The same file passes or fails depending on how large it is
reproduced. No available value expresses that. `whole_asset` is recorded as the nearest available
value and is explicitly marked inaccurate in the binding's limits.

This is new. It is not that the vocabulary lacks a value; it is that the vocabulary is indexed on
the wrong dimension for this class of claim.

## 7. A repair profile that is the exact inverse of book 6

Ten of this source's twelve repairs are physical camera actions — thin a bright framing element,
wait for the transit, oppose two elements at the frame's extremes, pan level and overlap by half,
shoot head-on, build the set, focus at ƒ/1.4. `executable_by: [physical_production]`, no generative
equivalent, parked as `production_candidate` and **explicitly not translated.**

Book 6, processed three days' work earlier in this same lane, produced the opposite: nine of
fourteen repairs were deterministic geometric operations a layout engine could execute exactly.

**Neither profile required a vocabulary addition.** The `executable_by` field was introduced to make
the physical-versus-generative gap visible, and it has now cleanly expressed both poles plus the
deterministic middle. That is evidence for the current design, from two consecutive books that could
hardly be less alike.

## 8. Contradictions in the source, recorded not resolved

| The source says | And also says |
|---|---|
| Rules for placement "take all the fun and imagination out of it" | …then supplies a three-zone scheme, a named classical proportion, and a numeric aspect ratio |
| Classical division is "all about satisfying the eye rather than challenging it" | Four pages later: it is better to divide so the eye "doesn't rest anywhere for long", which makes the image "more energetic" |
| Cropping later to make a frame-fit work "wouldn't really be the point" | Four sections later, argues for cropping a finished 3:2 image to square |
| A square signifies deliberate rigour and severity, chosen rarely | …and became common in photography because the film happened to be that shape |
| A flat frontal viewpoint is valuable because it isolates deliberate diagonals | The adjacent case concedes shooting a rectilinear subject squarely shows "no great imagination" |

All five sit as `extractor_observed` caveats on objects and as `origin: extractor_inferred` conflicts
in the systems — visibly ours, not presented as something the author noticed. The schema absorbed
them without strain, as it did book 6's six.

## 9. The most speculative thing in this extraction, marked as such

`scs_fre_c003_004` groups five cases the source treats as entirely unrelated — off-stage reference,
the almost-touching gap, the reveal, the eccentric division, and the scale figure — on the claim
that all five work by the **same mechanism: a delay in the viewer.** Not by anything visible in the
frame, but by the interval before something is found or resolved.

The evidence is that every one of the source's own explanations reduces to a duration: *"for a
moment it makes the image more engaging"*, *"the eye lingers long enough to start to wander"*, *"it
takes the eye a moment to slip down to the corner"*, *"the eye then wanders elsewhere"*, *"too small
and the point would be wasted."*

If the inference holds, it identifies one failure mode governing five apparently unrelated
techniques — the withheld element must be hidden enough to produce the delay and findable enough
that the viewer does not leave first — and the source states the two halves of that bound in two
different chapters without connecting them.

It is entirely `extractor_synthesis`, marked with the strongest uncertainty note in either book, and
every member stands alone if it is rejected. Recorded because a fully inferred system is a
hypothesis about a source, and SPEC-03 says that is legitimate provided it is visible.

## 10. A flag for the integrator — not acted on

The pre-batch `CANON-CURRICULUM-V0.md` names Freeman as the source expected to produce the project's
first `cross_source_concept`, on the grounds that if Bang and Freeman agree about visual weight from
different media, that agreement is real.

**This lane cannot test that** and did not try. Cross-source work needs two origins and this lane is
deliberately isolated; SPEC-05 also requires that a `cross_source_concept` be a reviewed claim about
the world rather than a convenience. Recording only that the opportunity now exists — Molly Bang's
extraction is in the repository and this one is beside it — and that the curriculum predicted it in
advance, which makes it a prediction worth checking rather than a merge worth assuming.

Note also that the curriculum's entry describes the *other* Freeman book, so whether the prediction
survives the identity correction in §3 is itself an open question.

## 11. What remains uncertain

- Whether the `creative.hierarchy` traversal gap is a schema defect or a still/moving mismatch. Two
  of the three instances are cinema devices by the author's own account.
- Whether the `observation_unit` gap recurs. It arose from one claim about print size; a second
  instance in a different domain would make it structural rather than particular.
- Whether the delay-mechanism system in §9 is real or is a pattern found because it was looked for.
  Nothing in this extraction can settle that, and it is marked accordingly.
- Whether losing "the page" costs anything for this book *in practice*. The graphic deconstructions
  all survived. What is gone is their composition with the photographs — which matters for a book
  whose method is exactly that, but the extraction was not blocked anywhere by it.
