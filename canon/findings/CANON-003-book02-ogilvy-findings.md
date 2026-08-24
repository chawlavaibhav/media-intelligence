# CANON-003 book 2 — Ogilvy ch.2: extraction findings

**Date:** 24 Aug 2026 · **Checkpoint:** `b904278` · **Domain:** advertising / persuasion
**Section:** the complete chapter 2 · **Visual completeness:** `blocked_visual_validation`

---

## 1. Why this book stresses the method differently

The three books before this one argue from things you can look at — a picture, a page, a camera plan.
Ogilvy argues almost entirely from **assertion and anecdote about commercial outcomes**. He reports
that one advertisement sold 19½ times as much as another, that a beer campaign reduced consumption,
that Mercedes sales went from 10,000 to 40,000 cars a year. Almost none of it is replicated,
controlled, or sourced.

The evidence profile makes the contrast concrete:

| | Bang | Williams | Grammar of the Shot | **Ogilvy** |
|---|---|---|---|---|
| Objects resting on practitioner assertion | 22/55 | — | 6/17 | **20/22** |
| Anecdotal | 5/55 | — | 0/17 | **14/22** |
| Outcome claimed | 0/55 | 0/31 | 0/17 | **5/22** |
| Controlled comparison | 9/55 | — | 3/17 | **0/22** |
| Visually demonstrated | 26/55 | 23/31 | 12/17 | **0/22** |

**The schema handled it, and handled it well.** The evidence-characteristics vocabulary has terms for
exactly this — `outcome_claimed`, `anecdotal`, `practitioner_assertion` — so the weakness is recorded
inside each object rather than hidden. Nothing had to be forced or excluded.

**Why that matters practically.** This is the first source in the batch whose claims are almost all
about *whether something sells*, which is the closest any Canon source has come to the project's own
Cost per Accepted Outcome question. It is also the least evidenced. Recording both facts in the same
object is precisely what SPEC-03 was built to do.

## 2. A fourth pattern of visual loss, and a ranking

The visual pass was **blocked** — see §5. But what is missing is measurable from the text: six
explicit placeholders reading "Click here for hi-res image" sit where reproductions of actual
advertisements were. Those advertisements are Ogilvy's primary evidence. The captions survive.

Four books now show four distinct patterns, and they differ in **detectability**, not quantity:

| Book | Pattern | Can a text-only reader tell? |
|---|---|---|
| Williams | **Silent** — two demonstration lists become identical | No. Nothing marks the loss |
| Grammar of the Shot | **Named** — every figure numbered and captioned | Yes, precisely |
| Ogilvy | **Announced** — literal "click here" placeholders | Yes, unmissably |
| Bang | **Minimal** — prose carries the argument | Little is lost |

**The practical consequence:** severity is not about how much is missing. It is about whether the
extractor can tell. Silent loss is the only one that produces confident, wrong extraction.

## 3. Comparison with the sealed historical work

Opened only after checkpoint `b904278`. **Nothing altered afterwards.**

**Found by both — 12 of the historical 13.**

**Found only by the fresh pass — 10 objects, and they are not marginal.** They include the chapter's
entire final third:

- the claim that the industry has a **structural incentive not to test** whether advertising works;
- the charge that the field **fails to codify** what it learns, with the reverse-type example and the
  history of Gallup's abandoned readership research;
- the argument for **copying direct response** because it alone attributes sales to advertisements;
- the attack on the **cult of creativity**, including "if it doesn't sell, it isn't creative";
- the **image-not-product** evidence — the distilled water experiment and the whiskey demonstration;
- the 19½-fold performance gap that anchors the chapter's whole argument;
- the **thirty-year durability** test.

The sections headed *Pursuit of knowledge*, *The lessons of direct response* and *The cult of
'creativity'* produced **nothing at all** in the historical pass.

**INFERRED:** the historical extraction appears to have stopped, or narrowed, after *Repeat your
winners*. Whether that was truncation, a scope judgement that institutional criticism was not craft
knowledge, or something else is **not established** from the audit alone.

**One deliberate divergence.** The historical pass classified "big ideas come from the informed
unconscious" as **human-learning-only** — that is, outside Canon. I extracted it as SourceKnowledge.
Under SPEC-03 there is no usefulness test, and it is plainly something the source teaches. Mine is the
schema-correct treatment, and this is a small example of the old admission habit surviving into the
migration.

### Where the historical work was better, again

**It found Creative IR bindings I did not.** The audit binds Ogilvy's material to `message.proposition`,
`message.support`, `audience.who`, `audience.context`, `intent.objective`, `brand.type`, `entities` and
`creative.hierarchy`. I produced two Creative IR bindings. `message.proposition` in particular is
obviously right for a chapter about what to say and why, and I never considered it.

**This is the third consecutive book in which the historical pass caught a product-schema fit point
the fresh pass missed.** Williams: `creative.hierarchy` cannot express an ending. Grammar of the Shot:
sight lines belong in `relationships`. Ogilvy: the whole `message.*` family. Three books is no longer
a coincidence.

**It connected a source claim to our own assumptions register and I did not.** The audit observes that
`advertising_can_reduce_sales` is direct counter-evidence to **assumption 13** — that human acceptance
correlates sufficiently with commercial outcome — because Ogilvy's opening argument is that admired
advertising routinely fails to sell.

I extracted that claim, and the stronger version of it, and I built an evaluation binding warning that
scoring style measures the wrong thing. So I reached the same substance. **I did not connect it to the
register.** That is the same weakness as the binding misses, in a different place: the fresh method is
good at reading sources and poor at relating what it reads back to the project's own framework.

### Where the two passes independently agreed

Both built a **working-procedure sequence** from the chapter's ordered headings, with almost the same
membership and order — study the product, research the audience, decide position, decide image, test
the idea. Both built a **parity trade-off**: where a differentiating fact exists build on it, where
products are genuinely alike do not claim superiority at all. Neither pass saw the other's work.

## 4. Recurrences now confirmed across books

- **Historical over-binding: 4 books.** Bang 21 bindings/19 objects, Williams 12/14, Grammar of the
  Shot 13/13, Ogilvy 14/13. Fresh: 5/55, 2/31, 2/17, 2/22.
- **Fresh method finds governance the historical passes missed: 3 books.** Ogilvy yields an
  `evidence_interpretation` binding — this chapter is a worked case of how to weigh a source that
  argues from uncontrolled outcome claims while itself explaining why its field produces such claims.
- **Historical catches product-schema fit the fresh pass misses: 3 books.**
- **Distinct visual-loss patterns: 4 books, 4 patterns.**

## 5. The batch-level blocker

**The local book library became unreadable partway through this book.** It was readable earlier in this
same session — that is how Phase 0 verified all four anchors and how book 1's pages were rendered. It
is now refused at the filesystem level for the entire directory.

**This is an access problem, not corruption.** The books are intact. The only workaround available to
me would be bypassing the sandbox, which is an access-control bypass and a stop-gate action under the
autonomy policy, so I did not take it.

**Consequence for the batch, stated plainly:** the repository holds six chapter texts. Two are already
processed, one (Lupton) is blocked on corruption, and one is book 1. That leaves exactly **one** more
processable source — Light: Science & Magic — before the batch runs out of reachable material at book
3 of a required 15.

Ogilvy was completed anyway because its provenance had already been verified while access existed, and
because CANON-003's own visual policy says to mark visual completeness as blocked and continue rather
than abandon the book. That policy covers one book losing its figures. It does not cover the library
becoming unreachable.

## 6. Uncertain / not verified

- Why the historical pass produced nothing from the chapter's final third. **Not established.**
- Whether Ogilvy's outcome figures are true. None is checkable from the text and the source names no
  study for any of them.
- Whether practices proven in direct response transfer to brand advertising. The source argues they
  should; it presents no test, and its own argument implies the test is not run.
- Whether the "measurement argument" system I built is the chapter's spine or my construction. Two of
  its five links are source-stated; three are mine.
