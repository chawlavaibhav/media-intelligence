# CANON-003 book 10 — Walter Murch, *In the Blink of an Eye*, pp.1–25

**Lane B** · branch `work/canon-003-b` · fresh checkpoint `72a6b31`, pushed before any comparison
material was opened.

**Source:** Walter Murch, *In the Blink of an Eye*, revised 2nd ed., Silman-James Press, 2001.
**Section:** printed pp.1–25, contiguous — seven consecutive named sections, containing the Rule of
Six in full.
**Output:** 39 SourceKnowledge objects · 4 SourceConceptSystems · 23 ontology terms ·
9 relationships · 3 concepts · 8 operational bindings. All validate.

---

## 1. What this source turned out to be

A transcribed lecture, and it behaves like one. Its own front matter says so: "a revised
transcription of a lecture on film editing given by Walter Murch in the mixing theater at Spectrum
Films, Sydney, Australia, in October 1988", revised in 1995 and again in 2001.

The consequences show up everywhere and were recorded rather than smoothed:

- **It argues by extended analogy, and the analogies carry weight rather than decorating it.** Human
  and chimpanzee DNA for why sequence matters. A beehive moved two inches, two yards or two miles for
  why intermediate change is the dangerous kind. Nuclear binding forces for how tightly the top three
  criteria cohere. Houdini for misdirection. A bumble-bee for the central mystery. In at least two
  cases — the DNA argument and the nuclear one — **the analogy is the entire support for the claim**.
  Nothing in the batch so far has had that evidence profile.
- **It hedges aloud.** "Slightly tongue-in-cheek, but not completely." "The general principle seems
  to be." "An ideal cut (for me)." These are a speaker's qualifications, and they are load-bearing.
- **It defers its own central question by thirty-three pages** (see §4).
- **It contains almost no measurement.** Two numbers the author says he computed (a 95-to-1 shooting
  ratio, 1.47 cuts per editor per day), one estimate ("probably fifteen" shadow splices), and six
  percentages he immediately qualifies as not-quite-serious.

## 2. The Rule of Six against the schema — the question the operator posed

The instruction was to represent Murch's priority ordering faithfully **using existing structures**,
and if the schema proved insufficient, to record that as evidence rather than invent a new structure.

**What was done.** `scs_murch_c003_001` uses SPEC-03's existing `priority_order` system type. Six
members carry `order` 1–6. `ordering.scheme` is `source_numbered` and `ordering.origin` is
`source_stated`, both of which are true — Murch numbers the list himself. The sacrifice procedure,
the masking asymmetry, the interval claim, the coupling claim and the applicability bound are all
members. Nothing was invented.

**Where it is insufficient.** `priority_order` records that emotion outranks story. It has no field
for **by how much**. Murch's percentages are not decoration:

| Rank | Criterion | Weight |
|---|---|---|
| 1 | Emotion | 51% |
| 2 | Story | 23% |
| 3 | Rhythm | 10% |
| 4 | Eye-trace | 7% |
| 5 | Two-dimensional plane of screen | 5% |
| 6 | Three-dimensional space of action | 4% |

51 against 49 for everything else combined. The gap from rank 2 to rank 3 (23 → 10) is larger than
the whole spread from rank 3 to rank 6 (10 → 4). **Read as a bare ordinal list, the Rule of Six
presents as six roughly comparable considerations in a preferred sequence — close to the opposite of
what it argues.** The numbers are preserved verbatim on the six criterion objects and on
`sk_murch_c003_0029`, readable by a person and invisible to anything mechanical. Recorded as
**LB-10**, not fixed.

**A prediction this batch made, and how it turned out.** `canon/experiments/CANON-CURRICULUM-V0.md`
selected this book with the words: *"Murch's Rule of Six is an explicit **weighted priority order** —
a `priority_order` SourceConceptSystem, the type we have never yet tested."*

The planning document called it a **weighted** priority order. The schema type is called
`priority_order` and has no weight. **The gap was sitting in the difference between those two phrases
and nobody noticed it until the type was used.** That is the most useful thing this book contributed:
not that the schema failed, but that a schema type can look adequate right up until a source exercises
the part of it that does not exist.

**Two markings preserved that are usually dropped.** The weights are "slightly tongue-in-cheek, but
not completely" — a double hedge the source puts on its own most-quoted numbers. And the whole list
is scoped: "An ideal cut **(for me)**". Both are in the system's `source_warns_against_isolated_use`
field. This framework is quoted impersonally almost everywhere it appears; the source does not state
it that way.

## 3. Historical comparison

**No historical Murch extraction exists in this repository.** Verified by filename search and by
content search on the author, the title and "rule of six". Three hits, all planning documents with no
extracted claim: the parallel-execution amendment, the coverage map, and the curriculum document
quoted above. `FINDINGS-02` names the book once, as a suggestion for which book to do second.

Recorded as **`no historical comparator`**. Fourth such book in the batch, after Albers, Vignelli and
book 9.

**The miss rate for this book is unknown, not zero.** With four of ten books now lacking a
comparator, the batch's strongest recurring signal — that older extractions catch Creative IR fit the
fresh ones miss — is untestable on an increasing share of the sample.

## 4. Two source-shape findings that will matter for book 12

**The deferred question.** On printed page 9 Murch poses the book's central question — why do cuts
work — and says "We will get back to this mystery in a few moments". He returns to it on pp.58–64,
via John Huston's remark about blinking, which is the passage the book is named for. Any
normally-sized window on this source captures the question without the answer.

It is recorded as the source's **own open question**, with the location of the answer named in a
caveat, and nothing from pp.58–64 imported. The field `source_asks_open_question` was not sufficient
on its own: it describes a source's uncertainty, and using it for a question the source does in fact
resolve later would misrepresent it. The caveat carries the correction.

**Why this matters for what comes next.** Book 12 in this lane is *The Conversations*, an interview
transcript — a source form even less locally complete than a lecture. This is worth carrying into
that extraction as a known hazard rather than rediscovering it. Recorded as **LB-14**.

## 5. The comparison this lane can now make: books 9 and 10

Two books, same subject, same lane, same batch, opposite in almost every respect that matters to the
method.

| | Book 9 — *Grammar of the Edit* | Book 10 — *In the Blink of an Eye* |
|---|---|---|
| Form | introductory textbook | transcribed lecture |
| Figures in section | 23 | **0** |
| Visual loss | total; 2 in-graphic labels lost silently | **none** |
| Evidence profile | enumeration + demonstration | analogy + practitioner assertion |
| Objects per printed page | 1.1 | 1.6 |
| Bindings: evaluation vs governance | 5 evaluation, 1 governance | 1 evaluation, **5 governance** |
| Teaches | checkable relations between shots | how to weigh considerations |

**The binding split is the substantive result.** Book 9 produced mostly evaluation bindings because
it teaches properties two shots do or do not have. Book 10 produced mostly governance bindings
because what it teaches is *how to trade one consideration against another* — which is a question
about how our own conflict resolution and evidence interpretation should work, not about a property
of an asset. Both are film-editing books about when to cut.

That has a direct consequence for the batch's ninth synthesis question, on which source knowledge
repeatedly fails to bind to product schemas. On this evidence the answer depends less on the domain
than on whether the source states **properties** or **priorities**. Properties bind to evaluation.
Priorities bind to governance, or to nothing.

**Recorded as LB-13:** visual dependence follows the author's mode of argument, not the subject. A
triage rule of the form "filmmaking books need a visual pass" would be wrong in both directions here.

## 6. A cross-source candidate, flagged and not acted on

Murch's `eye_trace` and the `eye trace` term extracted from *Grammar of the Edit* in this same lane
name closely similar things — the location and movement of the audience's focus of interest within
the frame, and the viewer's gaze crossing the frame at a cut.

Unlike the *Grammar of the Shot* / *Grammar of the Edit* pair in **LB-09**, these are **genuinely
independent origins**: different authors, different publishers, no relationship between the books.
That makes them a legitimate candidate for a `cross_source_concept` under SPEC-05's
two-independent-origins rule — possibly the first real one this corpus has produced.

**No such concept was created.** Both ontology files are source-local, cross-source aggregation is
the integrator's work under the parallel amendment, and SPEC-05 requires review before a claim of
agreement is made. Flagged here so the integrator has it.

The pair with LB-09 is the useful thing: one same-author pair that would pass a naive independence
check and should not, and one genuinely independent pair that should. Both were found inside a single
lane, in four books.

## 7. Evidence for the current design

- **`priority_order` was the right type and it held.** It failed only on the interval, and it failed
  visibly — the insufficiency is stated in `system_level_uncertainty` where a reader will meet it.
- **`executable_by` did its job by admitting ignorance.** Murch's remedy for a director's distorted
  judgement is a two-week absence, which is not an operation on material at all. `unknown` is honest
  and the gap is legible, which is exactly what SPEC-05 says the field is for — though it flattens a
  real distinction (**LB-11**).
- **The V0 granularity rule held again**, on a source that ranks and enumerates, with no invented
  exception. The six criteria were split into six objects because each is independently
  contradictable and because splitting is what lets the `priority_order` system carry real members.
- **Layer separation held.** Zero product vocabulary in the source layer; 8 bindings against 39
  objects.
