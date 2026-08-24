# CANON-003 book 1 — Grammar of the Shot ch.4: extraction findings

**Date:** 24 Aug 2026 · **Checkpoint:** `b9f18be` · **Domain:** filmmaking / continuity
**Section:** the complete chapter 4, printed pp.93–112 · **Visual completeness:** verified page-level

---

## 1. What this book is, and why it stresses the method differently

Chapter 4 teaches how to shoot so that footage can later be cut together. Its distinctive property is
that it is **geometric**: one imaginary line, traced from where the actors are looking, generates most
of the chapter's rules. Where the camera may stand, how far it must move between shots, and where the
matching shot of the other character goes are all consequences of that single line.

That makes it a different test from the first two books. Molly Bang argues from association and
feeling. Robin Williams argues from what you see on a page. These authors argue from a plan drawing.

**Result: the method handled it, and the granularity rule needed no exceptions.** 17 knowledge
objects, 3 groupings, 16 vocabulary terms, 8 bindings. All four files pass the schema checks.

## 2. The chapter's most important claim, and why it matters beyond film

The authors state that placing the camera on the wrong side of the line produces a shot that is
**perfectly fine on its own**, and that the mistake only appears once the shots are cut together —
adding that most filmmakers do not notice it until the edit.

The figure makes this directly visible: the erroneous close-up is an unremarkable, well-composed
image. Nothing is wrong with it. The fault exists only in its relationship to the shot before it.

**Why it matters for this project.** Any checking process that looks at frames one at a time will
pass a scene containing this defect. Not because it is subtle, but because there is nothing in any
single frame to find. I grouped four further claims with the same property — jump cuts, mismatched
over-the-shoulder pairs, broken eye-lines, reversed screen direction — into a system on that basis.

**What remains uncertain.** That grouping is mine, not the authors'. They state the invisibility only
for the crossed line. If the grouping is wrong, each member still stands on its own.

## 3. A third distinct kind of visual dependence

The batch is now tracking how visual evidence gets lost. This source shows a third pattern.

| Book | How the figures matter | What text extraction loses |
|---|---|---|
| Bang (CANON-001) | Figures corroborate claims the prose already makes | Little; the prose carries the argument |
| Williams (CANON-002) | The evidence *is* the spacing | Everything; the demonstration becomes two identical lists |
| **Grammar of the Shot** | Figures map a camera position to the image it produces | The correspondence between the two halves |

Here the text names every figure and says what it shows, so a text-only reader knows what they are
missing — unlike Williams, where the loss was silent. But the actual teaching device is a **paired
representation**: an overhead plan of where the camera stands, set beside the resulting frame. Neither
half carries the knowledge alone.

## 4. Comparison with the sealed historical work

Opened only after checkpoint `b9f18be`. **Nothing was altered afterwards.**

**Found by both — 11 of the historical 13.** Frame edges as directional references, screen direction,
lines of attention, the axis and the 180 degree rule, invisibility until assembly, the 30 degree rule,
reciprocating imagery, outside-in progression, eye-line match, continuity across takes, and shooting
coverage to give the editor choices.

**Found only by the fresh pass — 5 objects.** The most consequential is the authors' statement that
**"there are very few absolutes"** among their own guidelines and that a creative reason is sufficient
warrant to break any of them. The historical pass has no counterpart for this. It is not a rule among
the others; it governs how all of them should be applied. The others are: shots composing into scenes
and acts, the requirement that material shot months apart read as one moment, the general obligation
to present a physically consistent world, and the persistence of screen position when the other
character leaves frame.

**Found only historically — 2.** A separate object for minimising take count on cost grounds, which I
folded into the coverage object as a caveat; and a restatement of shot-type roles from chapter 1,
which the historical audit itself flags as having incomplete attribution.

### Where the historical work was better

**It made a Creative IR binding I missed, and it was right to.** The audit binds lines of attention
and eye-line match to SPEC-01's `relationships` field, on the grounds that a sight line *is* one
entity looking at another — which is SPEC-01's own worked example of that field. I bound sight lines
only to continuity requirements and never considered `relationships`.

The audit goes further and contrasts it with the Molly Bang case, where the same field was bound
**wrongly** because perceptual colour grouping is not an entity-to-entity relation. So the historical
work distinguished a correct use of the field from an incorrect one, and I missed the correct one.

**This is the second consecutive book where the historical pass caught a product-schema fit point the
fresh pass walked past.** In CANON-002 it was that `creative.hierarchy` cannot express a definite
ending. Here it is an available and well-justified binding. Two books is a pattern worth naming, and
it is logged.

**Its evaluation bookkeeping is finer than mine.** The audit assigns a viewing unit to each claim
separately — six claims, six units, none at frame level. I grouped the same material into three
bindings. Mine is coarser and loses per-claim precision. Theirs is the better record.

### Where the two passes independently agreed

Both concluded that this source's value lies in evaluation and that **none of it can be checked one
frame at a time.** The audit reached that by tallying viewing units and finding zero at frame level.
I reached it by grouping claims that share the no-single-frame-signature property. Different routes,
same structural conclusion. That convergence is worth more than either result alone.

## 5. Recurrences confirmed against earlier books

- **The historical binding layer over-binds.** Bang 21 bindings for 19 objects; Williams 12 for 14;
  Grammar of the Shot 13 for 13. Roughly one Creative IR binding per object every time. The fresh
  passes produce 5, 2 and 2. **Three books.** This is now the most consistently reproduced difference
  in the batch.
- **The fresh method finds governance material the historical passes did not.** Williams: none
  historically, one fresh. Grammar of the Shot: none historically, one fresh. In both cases it came
  from the author stating how their own rules should be applied. **Two books.**

## 6. Uncertain / not verified

- Whether the no-single-frame-signature grouping is a real class or my construction. **Not established.**
- Whether 30 degrees is the threshold at which two views become perceptibly different. The figure
  shows five views differ; it never shows a smaller interval. **Not established by the source.**
- Whether any of these continuity requirements can be expressed to a generative video model. Outside
  Canon's remit and not asserted.
- The claim that audiences react unfavourably to mismatched framing, "perhaps just on a subconscious
  level", is asserted without evidence and no figure can support it.
