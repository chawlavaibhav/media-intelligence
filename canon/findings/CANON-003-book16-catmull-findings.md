# CANON-003 book 16 — Creativity, Inc. ch.5: extraction findings

**Date:** 24 Aug 2026 · **Lane:** D · **Checkpoint:** `b7f0d47` · **Domain:** creative process /
organisational craft
**Section:** chapter 5, "Honesty and Candor", complete · **Visual completeness:**
`verified_figure_level` — the chapter has no figures
**Counts:** 21 SourceKnowledge objects · 2 SourceConceptSystems · 23 terms · 10 relations ·
3 concepts · 5 operational bindings · **0 Creative IR bindings**

---

## 1. What kind of source this is, and why that matters for the test

Every book in this batch so far has been about making a thing — a page, a photograph, a shot, an
advertisement. This one is about **how a group of people criticises a thing while it is being
made**. It has no pictures, no measurements, no controlled comparison, and no case where its
method failed. What it has is a named mechanism, stated preconditions, stated failure modes, and
incidents from one company recounted by that company's president.

That is a genuinely different knowledge shape, and the task assigned it deliberately. The question
this book answers is not "does the method survive another book?" but "does the method survive a
book whose subject is not the artefact at all?"

**It survived, with one clean break and one strain.** Both are recorded below and in the Lane D
issue file.

## 2. The clean result: zero Creative IR bindings, and that is correct

The Creative IR (SPEC-01) is our internal description of a single advertising asset — what is in
it, who is in it, what the copy says, how the brand appears. **Nothing in this chapter fills any
of that.** The chapter never discusses what an asset should contain.

Under the old SPEC-02 rule, an extractor had to name a Creative IR field for every atom to admit
it. Applied here, that rule would have produced either an empty extraction — throwing away a
chapter of usable knowledge about criticism — or twenty invented bindings. The split between
SPEC-03 (what the source teaches) and SPEC-04 (what we can do with it) is what makes "twenty-one
objects, zero Creative IR bindings" a normal outcome instead of a failure.

**Practical meaning:** this is the first book in the batch that produces real knowledge with no
contact whatsoever with the product's asset schema, and it did so without any pressure to invent
one. That is evidence for the layer split, and it is stronger evidence than a book that binds
easily would have been.

The five bindings it does have all concern *evaluators* — the automated critics our product
builds — and one parked production candidate. The most useful is described next.

## 3. The most valuable single claim: a correct alarm can carry a wrong diagnosis

The source recounts a scene in *The Incredibles* where reviewers said the dialogue made a husband
seem to be bullying his wife, and told the director to rewrite it. The director judged the
dialogue right, looked further, and found the real cause: one character was drawn far larger than
the other, so a disagreement between equals read on screen as a big man menacing a small woman. He
redrew her at matching size, changed no words, and the same reviewers asked which lines he had
rewritten.

**Why this matters to us specifically.** We build evaluators that will report a defect and a
suspected cause in the same breath. This source says, from experience, that those two outputs have
different reliabilities: the detection that something is wrong was correct, and the account of why
was wrong, and the wrong account was *still useful* because it made the maker search. The
consequence for design is that an evaluator's alarm and its explanation should carry separate
confidence, and no automatic repair should ever be triggered by the explanation alone.

**What remains uncertain:** the source gives no way to tell in advance which part of a critique to
trust, and the evidence is one recounted incident from an interested party. This supports
separating the two signals. It does not say how to weight either.

## 4. The strain: the repair vocabulary cannot express a social action

SPEC-05 requires every remedy term to declare `executable_by` — who or what could carry the repair
out. The permitted values are `physical_production`, `generative_respecification`,
`deterministic_composite`, `human_edit` and `unknown`. Every one of them describes changing an
image, a video or a physical setup.

Every remedy in this chapter is a **social** action: change the word you use when asking for
feedback; give the reviewing group no authority; shrink the room; keep a dominating person out;
distil the session into one takeaway; phrase the note so the maker wants to act on it.

None of the four substantive values applies, so nine remedy terms carry `unknown`. **`unknown` is
the honest value and it is also misleading**, because it reads as "we have not worked out how to
execute this" when the truth is "this vocabulary has no value for this kind of action". A later
reader counting unknowns across the Canon would conclude these repairs are unresolved rather than
unrepresentable.

The method is frozen, so nothing was added. Recorded as Lane D issue **D-01**.

## 5. Two smaller observations

**A quotation inside a source has no place to live.** Several of the chapter's most quotable claims
are not the author's: the two selection criteria for building your own review group, the definition
of constructive criticism, and the observation that a film must at some point stop being made for
its maker are all quoted by Catmull from named colleagues. SPEC-03 has `source_terms` and
`provenance`, but no field distinguishing *the book's author asserts this* from *the book quotes a
named third party asserting this, approvingly*. I recorded the attribution in `caveats` with
`origin: extractor_observed`, which works but files an authorship fact as an observation of mine.
Lane D issue **D-02**.

**The source contradicts itself and the schema handled it.** The chapter prizes feedback from
practised peers with deep craft understanding, then closes by telling the reader that rank and role
are irrelevant — janitor, intern or lieutenant — provided the person makes you think smarter and
produces solutions quickly. It also states that directors reject notes from non-filmmakers while
conceding that outsiders often see more clearly. Both tensions are the source's own and neither is
resolved by it. `contradicts` relations and a `conflicts` entry on the system recorded them without
requiring a resolution, which is the right behaviour: the extraction should not tidy up an
inconsistency the author left in place.

## 6. The visual pass returned nothing, and the nothing is informative

All 33 images in the file were measured. Chapter 5 references exactly one image: a **525 × 1 pixel**
decorative rule that sits under all 28 chapter titles. Twenty-one images sit in a separate photo
insert and are captioned biographical photographs — Catmull as a toddler, the Emeryville building.
None supports a claim.

**The point worth carrying forward:** a visual pass that counted figure *references* without
measuring them would have reported "one figure in this chapter" and then either hunted for an
argument that does not exist or marked the chapter visually incomplete for never inspecting a
horizontal line. One pixel of height is what separated a correct reading from a wrong one.

And the opposite of the Williams problem appears here. In the visual-design books, the argument
lives in pictures that plain text destroys. Here there was never anything outside the sentences:
the chapter describes a production loop with a cadence, an artefact and an ordering, entirely in
prose. Nothing was lost — but nothing was *given* either, which is why both concept systems in this
extraction carry `extractor_synthesis` on their whole-system claims rather than reporting a
structure the source declared.

## 7. Evidence profile

| Characteristic | Objects (of 21) |
|---|---|
| `explicitly_stated` | 21 |
| `practitioner_assertion` | 21 |
| `mechanism_given` | 13 |
| `argued` | 9 |
| `anecdotal` | 4 |
| `mechanism_absent` | 6 |
| `repeated_within_source` | 2 |
| `historical_claim` | 2 |
| `empirical_within_source` | 1 |
| `controlled_comparison` | **0** |
| `visually_demonstrated` | **0** |
| `outcome_claimed` | **0** |

Plain-English reading: **every claim in this chapter is asserted by a practitioner, and about two
thirds of them come with an explanation of why they work.** Nothing is demonstrated, nothing is
measured, and — worth noting given the genre — nothing claims a business outcome. Catmull does not
say "candor made us $X"; he says candor is how the films get made. That is a milder evidentiary
posture than Ogilvy's, and it is recorded rather than assumed.

The single `empirical_within_source` is the production arithmetic: about twelve thousand storyboard
drawings per 90-minute reel, with story teams commonly making ten times that. It is a count from
inside the source's own operation, not a study.

## 8. Historical comparison

**No historical comparator exists.** Searched after the fresh checkpoint `b7f0d47` was committed
and pushed. The only files in the repository mentioning this book are the parallel-execution
amendment and the source inventory, both of which merely assign it. Recorded as `no historical
comparator` rather than manufacturing one. This is the third such book in the batch, after Albers
and Vignelli.
