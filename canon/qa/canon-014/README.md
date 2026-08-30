# CANON-014 grounded Q&A corpus

**1,028 questions and answers across 23 sources.** One bank per source, plus
`QA-MANIFEST.json` (all counts, recomputed mechanically) and `validate_qa_corpus.py`.

## What this is, in plain English

For every book the Canon has extracted, this is a set of questions about what that book actually
says, each with a written answer, the place in the book it came from, and a quotation supporting it.

It exists so that a claim like *"the Canon knows what this book teaches"* can be checked rather than
asserted. A question is a concrete, inspectable form of a knowledge claim: if the extraction has
understood a source, a question about that source should be answerable from it.

## What this is **not** — and this matters more than what it is

- **It is not benchmark ground truth.** Nobody has established that these answers are correct.
- **It is not human-calibrated truth.** No expert has reviewed them.
- **It is not model-evaluation evidence.** No human and no model has answered a single item, so
  nothing here reports how well anything performs.
- **It is not proof that Canon improves outcomes.** That would need an experiment this corpus does
  not constitute and cannot substitute for.

The three words on every bank — **grounded, ungraded, uncalibrated** — say it exactly. *Grounded*:
every item traces to one source, with a locator and a supporting quotation. *Ungraded*: nobody has
answered any of it. *Uncalibrated*: the `difficulty` label is an author's judgement, never checked
against an observed answer, and must never be reported as an empirical property.

## Where it sits relative to the Audit Gate

**Outside it, deliberately.** What establishes whether a source is faithfully represented is the
source artifacts and the audit written against their exact bytes. Questions written *about* those
artifacts are a companion asset, and folding them into the snapshot would let a well-written question
look like evidence about a source. No Audit Gate record covers any file in this directory.

## `source_status`: accepted vs hold

Every bank and every item carries one, and it describes **the source, not the answer**.

| | |
|---|---|
| `accepted` | The source is live Canon under `canon/knowledge/current/`. **108 items, 5 banks.** |
| `hold` | The source is a durable candidate under `canon/candidates/canon-014/`. **920 items, 18 banks.** |

**Held knowledge is kept, not discarded, and stays visibly held.** A source can be held because
nobody has yet inspected its figures, or because its only available copy is a bad translation, or
because its independence from a source already in Canon is unresolved. None of that makes what it
says about itself less useful to read — it makes it unsafe to treat as established. So the Q&A
survives and carries the flag.

**The status never changes the wording of a source-derived answer.** An answer describing what a
held book says is written exactly as it would be if that book were accepted. Anything else would
make the corpus a record of our confidence rather than of the source.

## Traceability

Each item carries: a unique `qa_id`; the `source_id` matching its source's own artifacts; a
`source_locator` (chapter, section or essay — page numbers only where the copy had authored pages);
the `question`; the `answer`; a `support` quotation; `answer_type`; `difficulty`; `knowledge_type`;
`requires_application`; `source_status`; and `confounders`, which records the plausible wrong answer
the item is built to separate from the right one. Each bank names its `knowledge_dir`, so any item
can be traced from question to the source artifacts it came from.

## No application-question quota

An earlier rule required a third of every bank to be "application" questions — ones putting a new
case to the source rather than asking what it says. **That rule is gone**, because it was a
construction target rather than a property of sources: banks clustered just above the threshold and
none ever fell below it, which is what a quota does to a distribution rather than what sources do.

The observed rate across the corpus is **40.7%**, and it varies widely by source. A practitioner's
account of campaigns they ran supports many transfer questions; an ethnography or an art history
supports few, because most of what those books establish is what *was* the case, not a principle to
carry somewhere new. Both are correct outcomes. **The observed rate is a measurement, never a
target.**

## Checking it

```bash
python3 canon/qa/canon-014/validate_qa_corpus.py
```

It checks structure and traceability only — that ids are unique, no question is asked twice, every
required field is present, controlled values are valid, and **no bank claims `accepted` for a source
whose artifacts sit in the candidate tree**. It says nothing about whether an answer is right, and
it cannot: nobody has answered any of them.
