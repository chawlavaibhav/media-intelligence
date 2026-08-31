# Canon retrieval — CANON-015

**What this is:** the code that decides which Canon knowledge a reasoning model sees when a
customer asks for a piece of media, and how that knowledge is packaged.

**Status:** built, tested, and **not accepted** as the production retrieval design. That is
a Controller decision. Deterministic tests passing is not the same as being right.

**Read next:** [`RETRIEVAL-CONTRACT-v0.1.md`](RETRIEVAL-CONTRACT-v0.1.md) for the
guarantees, [`evaluation/RESULTS-v0.1.md`](evaluation/RESULTS-v0.1.md) for the measured
before/after, and [`../findings/CANON-015-CONTROLLER-BRIEF.md`](../findings/CANON-015-CONTROLLER-BRIEF.md)
for what the Controller needs to decide.

---

## 1. The problem, in plain English

The project has a library of durable creative knowledge — 24 books and reports that have
passed the project's admission check, broken into 1,623 retrievable objects. EVAL-037 asked
whether showing that library to a reasoning model improves the media production package it
writes. The Controller's answer was: **yes, it helps, but the way we hand it over is not
mature** (`coordination/decisions/CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`).

"Not mature" turns out to mean four specific, measurable things. All four numbers below are
recomputed from the committed EVAL-037 transcripts, not quoted from a summary.

**It was too much.** In the healthiest lane — Sonnet under a controlled retrieval
allowance, the only lane that completed all 18 trials — a single trial saw a mean of
**66,966 bytes** of Canon, across three separate searches. In the unbounded lanes it was
catastrophic: the repaired Sonnet run completed 2 of 18 trials with 16 context overflows,
and a Gemma lane exposed roughly 1.13M tokens and failed all 18 on technical grounds.

**More than half of it was not accepted knowledge.** Of the 424 objects that lane received,
**53.5% were HOLD material** — knowledge the project has explicitly *not* admitted — and
**22.2% were Q&A items**, which the corpus itself labels "not benchmark ground truth, not
independent corroboration". Only **42.2%** was accepted, non-Q&A Canon. Every object stated
its own status honestly; the ranking simply handed held material to the model first,
because Q&A items are short and question-shaped and BM25 likes that. For the watch brief,
the first search of one trial returned **8 HOLD items out of 8**.

**It repeated itself.** A single search returned a mean of 4.5 of its 8 results from one
source, and in the worst case all 8 from one source. Nothing prevented two books the
project's own audit records describe as *not independent of each other* — the two *Grammar
of the...* companion volumes, or Walter Murch speaking in his own book and in Ondaatje's —
from both filling a bundle as if they were two witnesses.

**It arrived as raw records.** Each result was the whole stored object, ids, digests, schema
metadata and all, with no separation between the claim and the machinery around it, and no
framing of what a hedge or an unreviewed proposal meant.

One widely repeated reading needs correcting: the observation that the lane made 53
searches and only **1** detailed read was taken as evidence that models ignore the read
step. Reading EVAL-037's `canon_tools.py` shows why they did: `canon_search` already
returned each result's **complete stored object**, so a follow-up read was usually
redundant by construction. The models were not skipping a step they needed. The real
problems are the four above — cost, purity, redundancy and packaging — not a missing tool
call.

## 2. What this package does instead

```
customer request
   │
   ├─ 1. PLAN        pick at most 4 production questions from a fixed catalogue
   │                 (composition · lighting & material · product legibility ·
   │                  message structure · shot grammar · persuasion & memory ·
   │                  brand handling · cultural communication · failure prevention)
   │
   ├─ 2. RANK        BM25 *within each object kind*, over content fields only
   │
   ├─ 3. ALLOCATE    an explicit interleaved mix per question, not a hidden weight
   │
   ├─ 4. SPREAD      caps per source, per lineage group, per question; near-duplicate
   │                 and already-defined suppression
   │
   ├─ 5. PACKAGE     verbatim content + the epistemics that stop a hedge reading as a rule
   │
   └─→ ONE canon_context bundle: ≤12 items, ≤30,000 characters, accepted only
```

### 1. Plan — ask production questions, not the customer's words back

EVAL-037 searched paraphrases of the brief. The model wrote out its own knowledge needs
first, in prose, differently on every repetition of the same brief — three searches, three
new paraphrases, every time.

Here that step is explicit. A **production question** names a knowledge need in the
customer's outcome and carries the vocabulary that finds it in Canon. The request selects
questions by whole-word cue match, so the same request always produces the same plan, and
the plan is printed in the bundle for a human to disagree with. A caller who knows better
can name the questions directly; what no caller can do is ask for an unbounded plan.

The boundary is enforced by test: a production question never names a model, a provider, a
price for a service, or a latency. That is capability routing, and it is a different
stream's question.

*(Word-boundary matching is not pedantry. An earlier substring version fired the lighting
question on the word "dia**log**ue", because "dialogue" contains "dial".)*

### 2 & 3. Rank within a kind, allocate across kinds

EVAL-037 ranked everything in one pool. That is not a fair comparison: an ontology term is
a one-line definition of about 20 tokens, a SourceKnowledge object is a claim with
mechanism, scope and caveats running past 250. BM25's length normalisation narrows the gap
but does not make the two scores mean the same thing, so a single pool quietly
over-selects the shortest objects.

So each kind gets its own index, and a score is only ever compared with scores of its own
kind. Because cross-kind scores are then not comparable, the mix is decided by an explicit
order rather than a hidden weight:

> claim → the relations between claims → how we might use it → a claim → …

Written out: `knowledge, concept_system, knowledge, binding, knowledge, visual_evidence,
ontology_concept, ontology_term`. Two questions override it — lighting promotes visual
evidence, because that is where the figure often carries an argument the prose does not;
failure prevention promotes bindings and problem terms.

The sequence is **interleaved on purpose**. Grouped by kind, a tight character budget spends
everything on the first kind in the list and the mix never happens.

One scope filter applies. SPEC-04 defines five binding target types, and two of them —
`governance` (how our ontology admits or refuses terms) and `benchmark` (how to build our
own test cases) — are about this project's machinery, not about making the customer's work.
That is **63 of 152 accepted bindings, 41% of the binding surface**, and a flat search
returns them anyway: EVAL-037 surfaced a binding about how to score an evaluator's feedback
as an answer to "what goes wrong in a premium watch photograph". They are excluded from a
production bundle. That is a scope decision, not a quality judgement, and it is
configurable.

### 4. Spread — stop one source, or one origin, filling the bundle

Four independent limits, all enforced before an item consumes any budget:

- **per source** — at most 3 items from one book (default);
- **per lineage group** — sources the Audit Gate records as *not independent of each other*
  share one cap. The dependence relations are imported from
  `canon/validation/validate_audit_gate_v02.py` rather than restated, so this can never
  drift from the promotion rule it borrows. Where two such sources are selected anyway,
  both carry a note saying their agreement is not corroboration;
- **near-duplicate** — two items sharing 60% of their combined vocabulary are one item;
- **already defined** — an ontology term whose parent claim is already in the bundle is a
  definition of something the reader already has.

Selection is **round-robin across questions**, so every question contributes its strongest
item before any question contributes its second, and a tight budget hurts all questions
equally rather than starving the last one.

### 5. Package — deliver the knowledge, not a pointer to it

Each item arrives as: the verbatim claim, the source's own words, the mechanism if the
source gave one, the scope the source claimed, the problems and remedies in the source's
language — and alongside it, separately, the epistemics: claim type, evidence
characteristics, both uncertainty fields, and every caveat **with its origin**.

That last distinction is the one a bundle would most easily destroy. `source_stated` means
the author limited their own claim. `extractor_observed` means this project noticed a
weakness the author never mentioned. Merging them into "notes" turns a hedge into a rule.

Operational bindings always disclose that they are unreviewed: 141 of the 152 accepted
bindings carry `status: proposed`, and every binding in a bundle says so and says it is
this project's proposal rather than the source's claim.

Nothing is paraphrased anywhere. Truncation touches prose only, never epistemics, and is
always marked.

## 3. Measured result

Six real customer briefs, the same six EVAL-037 used. USD 0; no model call, no media.

| | EVAL-037 observed | CANON-015 default |
|---|---|---|
| Retrieval operations per job | 3.0 | **1** |
| Context handed to the model | 66,966 bytes | **27,862 chars** (−58.4%) |
| Objects / items | 23.6 | 8.3 |
| Accepted-status purity | 46.5% (42.2% non-Q&A) | **100%** |
| Distinct sources | 8.9 | 6.7 (6.5 independent origins) |
| Redundancy (mean pairwise vocabulary overlap) | 0.153 *(replayed)* | **0.117** |
| Production questions answered | not asked | **100%** |
| Items delivered whole (no second call needed) | n/a | **96%** |

The same queries replayed through EVAL-037's own `canon_tools.py` against today's corpus
give 66,708 bytes at 46.5% accepted — within 0.4% of what was observed. The difference is
the interface, not corpus drift. The redundancy row is measured on that replay, because the
committed transcripts record what came back but the evaluation set stores only each
object's identity, not its full text.

`compact` halves it again: mean 13,722 characters.

**What these numbers are not.** None of them says the retrieved knowledge is the *right*
knowledge. Nothing in this repository labels a Canon object relevant to a brief, and
inventing such labels would manufacture a ground truth.
[`evaluation/HUMAN-REVIEW-RUBRIC.md`](evaluation/HUMAN-REVIEW-RUBRIC.md) exists because
relevance needs a person, and six ready-to-read bundles are committed under
`evaluation/bundles/` for exactly that.

## 4. How it differs from EVAL-037's `canon_tools.py`

| | EVAL-037 `canon_tools.py` | CANON-015 `canon/retrieval/` |
|---|---|---|
| Surface | accepted + HOLD + Q&A, status stamped on each object | accepted only; HOLD/Q&A need an explicit diagnostic reason and mark the bundle non-production |
| Tools | `canon_catalog`, `canon_search`, `canon_read` | `canon_context`, `canon_detail` — no free-text search |
| Budgets | none by design (`limit` optional, default unbounded) | nine required bounds; `None` is rejected, not read as "no limit" |
| Query | the model's paraphrase of the brief | production questions from a fixed catalogue, plus the request's discriminative words |
| Index text | every string leaf **including dictionary keys** | declared content fields only |
| Ranking | one BM25 pool over all kinds | BM25 per kind, explicit interleaved allocation across kinds |
| Diversity | none | per source, per lineage group, near-duplicate, already-defined |
| Bindings | all 152, `governance` and `benchmark` included | 89 in production scope; the other 63 excluded |
| Framing | the raw stored object | verbatim content + epistemics, with a legend |
| Second call | expected | reported unnecessary for 96% of items |

EVAL-037's module is untouched and stays as experiment evidence. This package does not
import it except in the evaluation, where it is imported read-only to replay the old
behaviour as a control.

## 5. Layout

```
canon/retrieval/
  budgets.py      the nine bounds; refuses None and any non-positive value
  corpus.py       read-only accepted-Canon loader; typed items; lineage groups; fingerprint
  questions.py    the nine production questions, their cues and their search vocabulary
  plan.py         request -> bounded, inspectable retrieval plan
  rank.py         per-kind BM25, interleaved allocation, spread enforcement
  bundle.py       assembly, character budgeting, epistemics-preserving rendering
  tools.py        canon_context / canon_detail schemas and dispatch
  cli.py          inspect one bundle from the command line
  evaluation/     the offline evaluation, its inputs, its outputs and the human rubric
tests/test_canon_retrieval.py
```

## 6. Running it

```bash
# a readable summary of one bundle
python3 -m canon.retrieval.cli --request "premium 4:5 hero image of a mechanical watch …"

# the exact payload a model would receive
python3 -m canon.retrieval.cli --brief brief.txt --size compact --json

# the deterministic tests (50 tests, ~11s, no network)
python3 -m pytest tests/test_canon_retrieval.py -q

# the offline evaluation (USD 0, no model call)
python3 canon/retrieval/evaluation/run_offline_eval.py
```

`pyyaml` and `pytest` are the only requirements; `canon/HANDOFF.md` notes they are not
installed system-wide and suggests a local virtualenv.

## 7. Known limitations

1. **Lexical retrieval crosses media boundaries.** For the still-image watch brief, a claim
   from a film-editing book about moving the eye across a frame ranks first for the
   composition question. It is not nonsense — it is about composition — but it comes from a
   source whose own stated domain is `film_editing`. The bundle reports every selected
   source's stated domain so this is visible, and deliberately does not filter on it,
   because no mapping from a source's domain to a delivery medium exists in the corpus and
   inventing one would be this project's judgement rather than the source's.
2. **Cue matching is keyword matching.** It is deterministic and inspectable, which is why
   it was chosen, but a brief that describes a problem without using any cue word gets a
   thinner plan.
3. **Question coverage is not relevance.** A question "covered" only means at least one
   item was returned for it.
4. **Six briefs.** They are real and were used by EVAL-037, but they are six.
5. **No outcome evidence.** Nothing here shows an effect on accepted-outcome rate or Cost
   per Accepted Outcome. That needs a controlled model experiment, which CANON-015 is not
   authorised to run.
