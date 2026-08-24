# CANON-003 book 12 — Ondaatje, *The Conversations*, Third Conversation

**Lane B** · branch `work/canon-003-b` · fresh checkpoint `9e6f716`, pushed before any comparison
material was opened.

**Source:** Michael Ondaatje, *The Conversations: Walter Murch and the Art of Editing Film*, Knopf,
2002.
**Section:** the Third Conversation, complete — the source's own unit: one meeting, one place, one
day, seven named sections.
**Output:** 27 SourceKnowledge objects · 3 SourceConceptSystems · 16 ontology terms ·
8 relationships · 3 concepts · 6 operational bindings. All validate.

---

## 1. What an interview turned out to be, as an instrument

This was the batch's deliberate test of an unusual source shape, and the shape asserted itself in
every layer.

**It has four voices, not one.** Ondaatje's third-person editorial frame; the `O:`/`M:` dialogue; an
inset ~400-word first-person account from the producer Rick Schmidlin; and photograph captions that
sometimes carry substantive content. Register determines who is making a claim, and the schema has no
field for it (**LB-15**).

**It does not name things.** Sixteen terms from 13,774 words, against 48 from book 9's 15,911. A
textbook coins *action edit*, *natural wipe*, *sound bridge*, because naming is how a textbook
teaches. A conversation reaches for a figure of speech instead — *the hat*, *the wrong echo*, *the
lucky accident*, dialogue as *the moon* and effects as *the stars*. Most of book 12's terms are vivid
phrases rather than maintained vocabulary, and each is marked accordingly via `verbatim`.

**It does not build frameworks.** Three systems, and only one — the "hat" metaphor, which Murch names
as a metaphor and then extends to the camera himself — is the speaker's own grouping. The other two
are marked largely `extractor_inferred` and labelled explicitly as hypotheses about the source,
because things said one after another in a conversation are not thereby a set.

**Much of it is testimony, not doctrine.** Long stretches are film history, biography and production
gossip and yield no object at all. Where Murch describes what he did on one film without asserting it
generalises, the act is recorded as an *example* inside a claim he actually makes — never promoted
into a principle he did not state. Six bindings against 27 objects follows from this and is correct.

**It hedges, and the hedges are load-bearing.** Preserved rather than tidied: *"I don't know whether
love is the right word. Understand, sympathize, perhaps."* — where the correction **is** the claim,
Murch declining the interviewer's framing. And *"Curiously, I wasn't consciously aware of this when I
was working on the film"* — a maker's admission that his most striking claim about his own work is a
post-hoc reconstruction, which he volunteers rather than conceals.

## 2. Historical comparison

**No historical *Conversations* or Ondaatje extraction exists in this repository.** Verified by
filename search and content search on author and title. All hits outside this lane's own files are
planning documents — the parallel amendment and the coverage map — containing no extracted claim.

Recorded as **`no historical comparator`**. This is the **fifth** such book in the batch, after
Albers, Vignelli, book 9 and book 10.

That number now matters. Five of twelve books have no comparator, and all three of Lane B's do. The
batch's strongest recurring signal — that older extractions catch Creative IR fit the fresh ones miss
— is untestable on a growing share of the sample, and **untestable on this entire lane**. The miss
rate for books 9, 10 and 12 is unknown, not zero.

## 3. The finding this book was selected to produce, and a sharper one it produced instead

The inventory selected *The Conversations* for its "interview transcript — an unusual form". It
delivered that: **LB-15** through **LB-18** are all consequences of the form.

But the sharper result is **LB-20**, and it was not anticipated.

*In the Blink of an Eye* is by Walter Murch. *The Conversations* is by Michael Ondaatje. Different
authors, different publishers, different years — and both are Walter Murch talking about editing.
Two items were extracted independently from both:

- **The Egyptian-painting argument.** In book 10 it is a footnote: each part of the body drawn from
  its most characteristic angle, combined in one figure, with the speculation that "in some remote
  future, our films … will look just as comic and twisted". In book 12 it is a full passage ending
  "five hundred years from now, when people see films from our era, they'll seem 'Egyptian' in a
  strange way."
- **`planarity`** — a named criterion of the Rule of Six in book 10, and `planarity_of_the_face`
  applied to lens choice in book 12.

**Why this is worse than LB-09.** There, two books shared authors, publisher and series; a reviewer
might catch it from the title page. Here **the author field itself differs**. `dc:creator` is
"Michael Ondaatje", and no metadata field anywhere records that the book consists largely of another
man's words. This pair would pass any independence check built on author, publisher or source id —
and SPEC-05's `cross_source_concept`, the only concept kind that makes a claim about the world, is
guarded by exactly such a count.

### Disclosed contamination

I recognised the Egyptian argument **on sight** while reading book 12's source, because I had
extracted it from book 10 earlier in this lane.

Nothing was imported. `sk_conv_c003_0027` is written from the wording in front of me, which is
substantially longer and differently developed than book 10's footnote, and the recognition is
disclosed on the object itself as an extractor-observed caveat.

But an extraction cannot claim an independence it does not have. This is the same class of hole the
batch already logged when the specs were found to quote books the batch processes: **assigning two
books by or about one person to a single lane means the second extraction is performed by someone who
has read the first.** The batch's own curriculum document anticipated the topical overlap — "Overlaps:
Grammar of the Shot (continuity), Conversations" — but read it as subject-matter redundancy, not as
an independence or contamination problem.

### The set of three is the useful output

Lane B has now produced three cases of the same question, from three books:

| Pair | Independent? | Would a naive check say so? |
|---|---|---|
| *Grammar of the Shot* / *Grammar of the Edit* (LB-09) | **No** — same authors, publisher, series | Yes, wrongly |
| *In the Blink of an Eye* / *The Conversations* (LB-20) | **No** — same speaking voice, different author field | Yes, wrongly, and no metadata would catch it |
| Murch's `eye_trace` / *Grammar of the Edit*'s `eye trace` | **Yes** — unrelated authors and publishers | Yes, correctly |

Two false positives and one true positive, all found by hand, inside one lane of three books. No
cross-source concept was created for any of them; all are flagged for the integrator.

## 4. What this source gives the product

Six bindings, split two evaluation, two governance, two Creative IR. The most useful are the two that
do not depend on the film industry at all:

- **`bnd_conv_c003_0001`** — dialogue and sound effects compete for one pool of attention, so
  specifying dialogue intent implicitly specifies what the rest of the soundtrack can carry.
  "You pay attention to the stars on nights when there is no moon."
- **`bnd_conv_c003_0005`** — a documented case of a source's *stated* reason for an instruction not
  being its real one, because the writer was addressing a hostile reader. Directly relevant to how
  the Canon records source rationales, and the reason this extraction keeps a source's stated reason
  and any interpretation of it as separate records.

**LB-19** generalises across the lane: book 9 states *properties* and binds to evaluation; book 10
states *priorities* and binds to governance; book 12 states *testimony* and mostly binds to nothing.
Same domain, three profiles. Bearing on synthesis question 9: knowledge that fails to bind because it
was never general is **the schema working, not failing.**

## 5. Evidence for the current design

- **The frozen method absorbed a fourth source shape without modification.** Interview transcript,
  after textbook, lecture and companion volume. No schema change, no invented relation, no new term
  kind.
- **`origin` marking at every structural level is what made the difference legible.** Two of three
  systems are fully `extractor_inferred` and say so. Without that field the same objects would read
  as reports of a framework the source does not have.
- **The V0 granularity rule held a fourth time**, with no invented exception, on a source where the
  main temptation was the opposite of book 9's: not over-splitting an enumeration, but manufacturing
  principles out of anecdote. The guard used was to ask whether the source asserts generality, and to
  record the specific act as an example when it does not.
- **Zero bindings being normal turned out to matter.** SPEC-04 says an unbound object is healthy, and
  this is the book that needed it — 21 of 27 objects are unbound.
