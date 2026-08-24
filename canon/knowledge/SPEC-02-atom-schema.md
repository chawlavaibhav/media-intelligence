> ## ⚠ SUPERSEDED — retained as experimental evidence
>
> **Status:** superseded after the six-source probe, 23 Aug 2026. **Do not delete. Do not edit.**
> This file and the six probe outputs it produced are the evidence for why the architecture changed.
>
> **The assumption that failed:**
>
> > **Current product consumption is not a valid admission criterion for durable source knowledge.**
>
> This spec admitted knowledge by asking whether it informs a field in today's Creative IR
> (rule 1: *"No consumer, no atom"*). The probe showed that test fails in both directions —
> it excluded durable knowledge with no current consumer, and it admitted distortion, because
> an extractor required to find a binding will find one.
>
> The decisive evidence is in this file. Its own worked counter-example,
> `pointed_shapes_read_as_threatening`, is presented below as knowledge that informs nothing and
> belongs in human notes. The Molly Bang extraction three days later produced `mb_011` — the same
> knowledge, informing `creative.visual_language`. Same rule, opposite verdicts.
>
> **Replaced by:**
> - [SPEC-03](SPEC-03-source-knowledge.md) — durable source-faithful knowledge, no admission test
> - [SPEC-04](SPEC-04-operational-bindings.md) — how today's product can use it, versioned and separable
> - [SPEC-05](SPEC-05-knowledge-ontology.md) — mapping over preserved terminology, replacing the single registry
>
> **What survives from this spec:** two-pass extraction discipline, page-and-figure provenance,
> `knowledge_type` and evidence classification, the requirement that a diagnostic states an
> observation rather than an instrument, and the insistence that exceptions be recorded with
> their origin. See [FINDINGS-10](FINDINGS-10-source-vs-binding-reaudit.md).

# Spec 02 — Canon Atom Schema v0

**Date:** 23 Aug 2026 · **Derives from:** SPEC-01 Creative IR v0.1
**Purpose:** give book extraction a target that can be validated mechanically.

An atom does not answer *"what interesting thing did this book say?"*
It answers *"which Creative IR decisions can this knowledge improve?"*

---

## Schema

```yaml
atom_id: atom_0142
concept: visual_weight

# ── THE FILTER ──────────────────────────────────────────────
informs:                          # REQUIRED, non-empty, paths must resolve in SPEC-01
  - creative.hierarchy
  - static.composition

role:                             # what it lets the system DO
  - fills                         # helps choose a value for an IR field
  - diagnoses                     # gives an observable symptom
  - repairs                       # gives a corrective action
  # also: constrains, derives, flags

# ── THE KNOWLEDGE ───────────────────────────────────────────
principle: >
  Relative scale, contrast, position and isolation determine which element
  is perceived as most important, independent of its literal size.

mechanism: >
  Perceptual salience is comparative, not absolute. The eye resolves
  competing signals by relative difference within the frame.

applicability:
  media: [static, video_frame]
  when: "two or more elements compete for primary attention"
  exceptions:
    - "sequential reveal, where priority resolves over time rather than space"
  exceptions_status: source_supported    # source_supported | interpreter_proposed | not_identified

# ── OPERATIONAL HOOKS ───────────────────────────────────────
diagnostic: >
  Compare intended priority order against perceived dominance order.
                                  # states what to observe, never how to measure it

failure_modes:                    # registered terms only
  - wrong_element_dominates
  - competing_focal_points
proposed_failure_modes: []        # new terms awaiting registry promotion

repairs:                          # registered terms only
  - alter_relative_scale
  - alter_contrast
  - alter_position
proposed_repairs: []

# ── RETRIEVAL ───────────────────────────────────────────────
retrieval_keys:
  ir_fields: [creative.hierarchy, static.composition]
  media_types: [static]
  objective_classes: [any]

relationships:
  refines: [atom_0138]
  conflicts_with: []

# ── PROVENANCE ──────────────────────────────────────────────
source_ref:
  source_id: molly_bang_picture_this
  chapter: 3
  section: "Principle 4"
  page_start: 78
  page_end: 81
  figure_refs: [fig_3_12, fig_3_13]
  visual_context_required: true

source_support: text_and_visual   # text | visual | text_and_visual

knowledge_type: source_principle
evidence_class: established
confidence: 0.9
last_reviewed: 2026-08-23

status: operational               # operational | pending_vocabulary | human_notes
```

Page-and-figure provenance is not bureaucracy. *Picture This* argues largely **through images** —
an atom whose support is a figure rather than a sentence must be marked so, or we will later be
unable to tell whether we recorded what the book demonstrated or what we read into it. Chapter-level
provenance would be a regression against the auditability this whole architecture is built on.

We store references, not quotes. The requirement is to be able to go back and inspect, not to
reproduce the book.

---

## Validation rules

Mechanical. An extraction pipeline enforces every one without judgment:

1. `informs` is non-empty and every path resolves against SPEC-01. **No consumer, no atom.**
2. `role` is non-empty and drawn from the fixed set.
3. `failure_modes` / `repairs` contain registered terms only. New terms go to
   `proposed_*` and the atom becomes `status: pending_vocabulary`.
4. `knowledge_type` and `evidence_class` present, never blended.
5. `diagnostic` states an observation, not an instrument. Any atom naming a model, API or
   metric fails — that is Production IR's job and it changes as tools change.
6. `exceptions` field present with an `exceptions_status`. **Empty is legitimate.**
7. `source_ref` resolves to a page range. `source_support` present.
8. An atom failing 1 or 2 is not rejected — it is written with `status: human_notes`.

### On rule 6

The motivation is real: unconditional design commandments are how a Canon becomes prescriptive,
which is the leading diagnosis if C loses to B in the experiment.

But *requiring* an exception would make the model manufacture one. So the field must exist and
be honest about where it came from:

```yaml
exceptions: []
exceptions_status: not_identified          # the source states no limits
```
```yaml
exceptions: ["..."]
exceptions_status: source_supported        # the book states the limit
```
```yaml
exceptions: ["..."]
exceptions_status: interpreter_proposed    # our inference — flagged as ours
```

An atom with `not_identified` is a signal to watch, not a validation failure.

---

## Controlled vocabularies

`failure_modes` and `repairs` are shared taxonomies, not free text. Left as free text, forty
books produce four hundred near-synonyms — no failure counts, no repair success rates, no
benchmark families.

**Extraction proposes → registry reviews → registry promotes → atom becomes operational.**

The pending lane exists so the extractor never has to choose between forcing a genuinely new
idea into the nearest existing term and failing validation. Both outcomes are worse than
`pending_vocabulary`.

These taxonomies are also the join between the two knowledge stores:

```
CREATIVE CANON  →  failure_mode: wrong_element_dominates  ←  EMPIRICAL MEMORY
    (books say it can happen)                        (this model, this generation, it did)
```

Books predict failure modes. Real generations count them. They only meet if they use the same
words, which is why the vocabulary is registry-controlled from the first chapter.

---

## Knowledge type — never blended

Per master thesis §9. Each atom is exactly one:

| Type | Meaning |
|---|---|
| `source_principle` | A book, paper or expert explicitly supports it |
| `cross_source_synthesis` | Inferred by comparing multiple sources |
| `generative_media_hypothesis` | What a creative principle implies for AI generation |
| `empirical_generator_observation` | Observed in controlled model tests |
| `human_preference_observation` | What human evaluators preferred |
| `customer_specific_observation` | What one customer approved or rejected |
| `commercial_outcome_evidence` | What campaign performance indicates |

Books produce the first three. The last four come from Empirical Memory and never enter the
Canon through the book pipeline.

## Evidence class

Per §10: `established` · `supported_extrapolation` · `hypothesis`. A confident sentence in a
well-written book is `established` only for what the book actually demonstrates — never for its
extension to generated media.

---

## Extraction procedure — two passes, enforced

The knowledge-type separation must be procedural, not just declarative. A single extraction call
will slide from "Molly Bang demonstrates X" to "therefore AI advertising should Y" inside one
paragraph, and the join will be invisible afterwards.

```
PASS 1 — source only
  input:  chapter text + figures
  output: human notes  +  source_principle atoms
  rule:   no reference to generation, models, prompts, or advertising
          that the source does not itself make

        ↓  human review and approval

PASS 2 — implication
  input:  APPROVED source atoms only (not the chapter)
  output: generative_media_hypothesis atoms
  rule:   every one must cite the source atom it derives from
```

Pass 2 never sees the raw chapter. It can only build on what Pass 1 established and a human
accepted.

---

## Worked counter-example

Molly Bang on the emotional reading of pointed shapes — genuinely interesting, fails the filter:

```yaml
concept: pointed_shapes_read_as_threatening
informs: []                 # ← no IR field consumes this
status: human_notes
```

Not deleted. It sits in the human learning layer. If `creative.visual_language` later gains an
emotional-register field, it gets promoted with a real `informs` path.

That is the difference between an encyclopedia and an operational Canon: **the encyclopedia
keeps everything at the same status.**

## Two outputs per source

Per §32, each book produces both, and they are not the same document:

- **Human learning layer** — summaries, concepts, examples, mental models. For us.
- **Machine knowledge layer** — atoms conforming to this schema. For the system.

The second is not a compression of the first. An atom reading like a good summary sentence has
usually failed rule 5 or rule 6.

---

## Required output of the first chapter run

The review is **not** "are these atoms well written?" The run must produce:

```
1. Every candidate idea found in the chapter — including discarded ones
2. The status each received:  operational | pending_vocabulary | human_notes
3. For operational atoms: the informs path(s) it landed on
4. Every proposed vocabulary term, with the atom that proposed it
5. Every place the extractor was uncertain, and about what
6. Counts
```

A healthy result looks something like:

```
34 candidate ideas
 8 operational
 6 pending_vocabulary
20 human_notes
```

The result that should worry us is `34 ideas → 33 operational`, because it means the extractor
found a way to shoehorn everything into the product rather than testing the filter.

---

## Open questions

1. Atom granularity — one atom per principle, or per principle-plus-context? Chapter one
   settles this faster than argument will.
2. Whether `mechanism` earns its place or is human-notes material.
3. How `conflicts_with` resolves at runtime — likely a Production Canon concern.
4. Retrieval strategy: `informs`-path lookup alone, or embedding search filtered by path.

## Next

**One chapter. Not the book.** Three things are being tested simultaneously: whether the IR has
somewhere legitimate for this knowledge to go, whether this book is operational for the product
at all, and whether the atom schema preserves knowledge without distorting it.
