# Decision Log

## 2026-08-23 · SPEC-02 superseded conceptually by SPEC-03/04/05

**Decision:** Split the single Canon Atom into three layers — durable source knowledge, replaceable
product bindings, and a terminology ontology. Retain SPEC-02 and all six probe outputs unchanged as
experimental evidence.

**The assumption that failed:**

> Current product consumption is not a valid admission criterion for durable source knowledge.

SPEC-02 rule 1 read *"No consumer, no atom."* Every piece of book knowledge had to name a Creative
IR path or be demoted to human notes.

**Why it failed — evidence from the six-source probe:**

1. **It excluded durable knowledge.** *Light: Science & Magic*'s family of angles, the organising
   concept of the book, was filed as a note because it describes where to place a physical light
   and Production IR does not exist. Nineteen items were discarded this way.

2. **It admitted distortion.** An extractor required to find a binding finds one. Molly Bang's
   "larger reads as stronger" was recorded as informing `entities.role`; her colour-grouping
   principle as informing `relationships`, which in SPEC-01 means entity-to-entity relations.
   Neither is her claim. Product vocabulary also leaked into source fields — `mb_002`'s diagnostic
   read *"Is the rank-1 element at or near centre."*

3. **The rule contradicted itself.** SPEC-02's own counter-example,
   `pointed_shapes_read_as_threatening`, was presented as unbindable. The extraction produced
   `mb_011`, bound to `creative.visual_language`. Same rule, opposite verdicts, three days apart.

**Two further assumptions failed alongside it:**

- *A single shared string vocabulary can be seeded from early sources.* Six sources produced 42
  failure terms and 47 repair terms with **zero exact reuse**. Seeding from book one would have
  forced five later sources to distort or fail. Replaced by SPEC-05's mapping layer.
- *Atoms alone are sufficient.* Three systems carry claims no member states; `mb_008` contains a
  cross-principle relationship inside its own principle text because there was nowhere else for it
  to go. SPEC-03 adds SourceConceptSystem.

**What changes**

- Source knowledge is durable and has no admission test. Zero bindings is a normal state.
- Bindings are ours, versioned against SPEC-01, and cheap to discard.
- Terminology is mapped, never merged. Canonical concepts are optional and their children stay
  authoritative for repair selection.
- Evidence is recorded as factual characteristics. Uncalibrated decimal confidence is removed.
- Physical-production repairs are preserved untranslated. Translation is Pass 2.

**What is explicitly unchanged**

SPEC-01 Creative IR v0.1. SPEC-02 and all six probe atom files. The two-pass extraction discipline,
page-and-figure provenance, and the observation-not-instrument rule for diagnostics all carry
forward.

**Cost of being wrong:** one extra layer and an indirection. Recorded as assumption 1 in
[ASSUMPTIONS-AND-FALSIFICATION.md](ASSUMPTIONS-AND-FALSIFICATION.md), with a falsifier: if after
fifty bindings none is ever revised while its source knowledge holds constant, the separation is
paying for nothing.

**Next review trigger:** first SPEC-01 revision after bindings exist.

---

## 2026-08-23 · Direction reset — Canon scope restored

**Decision:** Restore the original separation of responsibilities between the Creative Canon, the
Capability Lab, the Production Planner, Empirical Memory and Evaluation. No architecture is
reopened; no prior work is deleted.

**What went wrong.** Recent work began judging the Canon against responsibilities it never had.
FINDINGS-11 reported that 35% of a twenty-failure sample had "no useful Canon relationship" and
that routing showed "no evidence." Both were true of what was measured, and both were measured
against the wrong subsystem — seven of the twenty failures were server restarts, storage paths,
provider API drift and a platform message limit, and several more were diffusion artefacts. A
category error was published as a finding.

**The restored boundary:**

- **Canon** — durable creative and media expertise. What a good outcome must accomplish, what
  techniques and trade-offs exist, how to turn an incomplete instruction into a plan without
  overriding intent, what to inspect to judge fitness for objective, what is wrong at craft level.
  Cookbook, culinary school, tasting expertise. It does not know which oven works today.
- **Capability Lab** — what current models actually do, measured. Produces the Registry.
- **Production Planner** — chooses today's execution path from IR requirements plus Registry.
- **Empirical Memory** — what happened on real runs, in the observer's words.
- **Evaluation** — two instruments: technical hard-fidelity, and creative fitness. Canon serves
  the second and is largely irrelevant to the first.

**Routing, stated correctly:** the Canon helps define **which capabilities a job requires**. It
must never claim to know **which current model has them**.

**Conclusions corrected** (originals retained on disk): FINDINGS-11's results table and routing
verdict; FINDINGS-09/10's "fields never covered"; FINDINGS-08's "lowest yield" framing; assumption
14's "weakened" verdict.

**Standing rule adopted:** a missing relationship in processed material means *"not found in the
currently processed material."* It never means *"the Canon cannot know this."* Any future finding
reporting a Canon limitation must first state which subsystem owns the failure.

**Register changes:** entry 4 restated with three connection channels and a scope warning; entry 6
split into 6a planning and 6b evaluation; entry 14's weakening withdrawn as out of scope; entries
15 (routing via requirements plus Registry) and 16 (curriculum breadth) added. All remain
hypotheses.

**Work commissioned:** Coverage Map (52 domains), Canon V0 curriculum (11 sources with a
dimensional stopping criterion), Experiment A and B designs, Capability Lab V0 plan and Registry
schema, evaluation corpus research.

**Not done, deliberately:** no book ingested, no vector database, no fine-tuning, no full
Production IR, no schema expansion, no A/B/C run.

**Next review trigger:** approval of the Coverage Map and Curriculum before any source ingestion.
