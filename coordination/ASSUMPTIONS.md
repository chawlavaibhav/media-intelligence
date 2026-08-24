# Assumptions and Falsification Register

**Date opened:** 23 Aug 2026 · **Purpose:** stop reasonable guesses from hardening into facts.

Several claims in this project have been repeated often enough to sound established. Some are.
Most are not. Each entry records what would have to happen for us to stop believing it.

**Status values**
`architectural_invariant` — decided, and we accept the cost of being wrong
`provisional_design` — chosen deliberately, expected to change
`hypothesis` — believed, untested
`empirical_finding` — we ran something and observed it

---

## 1a. The coupled SPEC-02 admission rule caused exclusion and distortion in the six-source sample

**Status:** empirical_finding (23 Aug 2026) — **scope: this sample only**

**What was observed.** Requiring every atom to name a Creative IR path produced two measurable
effects across six sources and 80 candidates:
- **Exclusion:** 19 items were demoted to notes for lack of a current consumer, 16 of which the
  re-audit judged to be genuine knowledge — including *Light: Science & Magic*'s central concept.
- **Distortion:** 2 bindings were manufactured to satisfy the rule (`entities.role` on `mb_004`,
  `relationships` on `mb_013`/`mb_016`), and product vocabulary appeared inside fields claiming to
  record the source (`mb_002`: "rank-1 element").
- **Inconsistency:** the same knowledge was classified unbindable in SPEC-02's own worked example
  and bound in extraction three days later.

**Limits of this finding.** Six sources, one extractor, one product schema, no independent
replication. It is evidence that *this rule* misbehaved on *this sample*. It is not evidence about
admission rules in general, and the re-audit's judgement that the 16 demoted items are "genuine
knowledge" is our judgement, not a measurement.

**Falsifier:** Re-extract one processed chapter under SPEC-02 with a different extractor. If the
exclusions and manufactured bindings do not recur, the effect was extractor behaviour rather than
the rule.

**Review trigger:** If a second extractor is ever used on the existing corpus.

---

## 1b. Separating Source Knowledge from Operational Bindings is the right response

**Status:** provisional_design — **not proven by 1a**

**Relationship to 1a.** 1a establishes that the coupled rule misbehaved. It does **not** establish
that this particular separation is the correct remedy, and the architecture must not be described
as empirically validated. A diagnosis is not a prescription.

**Alternatives not tested:** relaxing the admission rule while keeping one object; permitting an
`informs: []` atom with a documented reason; allowing bindings as optional annotations rather than
a separate layer. Any of these might have addressed 1a at lower cost.

**Supporting:** The re-audit represented all 81 candidates without forced fitting, recovered 16
demoted items, and dropped 2 manufactured bindings. That demonstrates the design is *sufficient*
for this corpus — not that it is necessary or minimal.

**Against:** One extra layer and an indirection, paid on every future extraction. No downstream
result has yet improved. The separation has never survived an actual SPEC-01 revision, which is
the scenario it exists for.

**Falsifier:** After fifty bindings, if none is ever revised while its source knowledge holds
constant, the separation is paying for nothing. Conversely, if bindings are routinely rewritten
while source objects stay stable, it is earning its cost.

**Review trigger:** First SPEC-01 revision after bindings exist.

---

## 2. Atoms are sufficient to represent creative expertise

**Status:** weakened — was an implicit invariant, now a hypothesis under doubt

**Against:** Molly Bang's `mb_008` contains a relationship inside its own principle text ("a
horizontal placed across verticals restores order") because there was nowhere else to put it.
`mb_002` and `mb_003` are a trade-off pair that is incoherent if either is retrieved alone.
Lupton's one-signal rule and redundancy rule contradict unless both are present with their scopes.

**Supporting:** Atoms retrieved fine in isolation for simple compositional facts — scale, contrast,
value against ground.

**Falsifier:** Retrieve atoms only, and separately atoms-plus-systems, for the same set of briefs.
If specification quality does not differ, systems are overhead.

**Review trigger:** The A/B/C experiment, if it retrieves Canon at all.

---

## 3. SourceConceptSystems are required in addition to atoms

**Status:** hypothesis

**Supporting:** §2's evidence shows information was lost. Systems are the proposed fix.

**Against:** Untested. May be solvable more cheaply by intra-source relations on atoms alone —
SPEC-03 provides both, which is arguably redundant.

**Falsifier:** If every system that gets written turns out to be fully reconstructible from its
members' `intra_source_relations`, the object is unnecessary.

**Review trigger:** After five systems exist.

---

## 4. Book knowledge connects to empirical failure — restated after testing

**Status:** hypothesis, **partially supported**, and reworded because the original was too narrow

**Original wording:** *"A shared ontology improves joins between books and empirical failures."*

**Restated:** *Book knowledge connects to empirical failure through at least three distinct
channels — shared mechanism, violated requirement, and commercial consequence — and the ontology
serves only the first.*

**Supporting (FINDINGS-11, 20 recorded failures):** the join exists and is sometimes exact. A 2000
picture book explains a 2026 floating-logo artefact at mechanism level, well enough to imply the
repair. Book knowledge also correctly predicted an **observation unit**: *Grammar of the Shot* says
continuity breaks are invisible frame-by-frame, and the Wan clip's drifting misspelling was exactly
that.

**Against:** only 4 of 20 related at term level. Twice as many connected through the Creative IR
requirement or a commercial consequence — routes the ontology does not serve.

**⚠ Scope correction (DIRECTION-RESET-01).** FINDINGS-11's percentages — including "35% no useful
Canon relationship" — **are not a Canon coverage or quality score and must never be cited as one.**
That sample was dominated by infrastructure failures, provider API drift and diffusion artefacts,
none of which the Canon owns. The experiment tested knowledge representation, using failures as
material.

**Falsifier:** twenty *creative-craft* failures — not operational, not generator-artefact — where
the Canon relates to few of them at any channel.

**Review trigger:** when Empirical Memory holds enough craft-level failures to sample properly.

---

## 5. Parameterised failures are better than separate failures

**Status:** provisional_design

**Supporting:** The false-grouping cluster parameterises cleanly by cue across three sources.

**Against:** The too-many-signals cluster spans three altitudes with no clean parameter. One clean
case does not establish a rule, and SPEC-05 accordingly permits parameterisation without requiring
it.

**Falsifier:** If repairs selected at parent level are systematically wrong, parameterisation is
hiding what matters. (SPEC-05 pre-empts this with `children_are_authoritative`, which is itself
the untested part.)

**Review trigger:** First repair loop that selects from the ontology.

---

## 6a. Explicit Canon improves creative **planning**

**Status:** hypothesis — untested. The central product claim.

**Claim:** given the same reasoning model and the same structured procedure, retrieved Canon
produces a better Creative Spec than generic craft instructions. This is *latent knowledge versus
explicit structured knowledge*, not "books versus no books."

**Supporting:** nothing yet. **Against:** nothing yet. The Canon has never been given to a model.

**Falsifier:** Experiment A in [CANON-EXPERIMENT-V0](CANON-EXPERIMENT-V0.md). Arm B (schema +
generic checklist) versus Arm C (schema + retrieved Canon), matched for length and format, blind,
pre-registered. If C ties B, the structure did the work.

**Second falsifier, independent:** if C wins on quality but **explicit intent preservation drops**,
the result is a failure regardless of quality — a Canon that overrides customers is not shippable.

**Review trigger:** Experiment A.

---

## 6b. Explicit Canon improves creative **evaluation**

**Status:** hypothesis — untested, and tracked separately from 6a

**Why separate:** planning and evaluation are different tasks and could easily diverge. It is
entirely possible that Canon helps critique an existing asset while adding nothing to planning one,
or the reverse.

**Weak early signal:** FINDINGS-11 found one case where book knowledge named the correct
**observation unit** — a property of the evaluator, not of the asset. One case, not a result.

**Specific risk:** a knowledge-loaded evaluator may invent violations of principles it has just
read. False-criticism rate is measured separately in Experiment B for this reason.

**Falsifier:** Experiment B. If C finds no more real issues than B, or finds more real issues at
the cost of proportionally more false ones, Canon does not improve evaluation.

**Review trigger:** Experiment B, after A.

---

## 7. Runtime RAG is the best way to consume Canon

**Status:** hypothesis — and never examined

**Supporting:** Assumed throughout because retrieval is the obvious mechanism.

**Against:** Alternatives were never compared: compiling Canon into checks, compiling it into a
fixed planner prompt, or using it only offline to generate benchmark cases. SPEC-05's
`children_are_authoritative` and SPEC-03's systems both imply retrieval must return *sets*, not
nearest neighbours, which most retrieval designs do badly.

**Falsifier:** Compare retrieval against a fixed compiled checklist of the same knowledge. If the
checklist matches or wins, RAG is unnecessary complexity.

**Review trigger:** Before any vector database is built. **No retrieval infrastructure should be
built until this is tested.**

---

## 8. Explicit Canon improves a frontier model beyond its latent knowledge

**Status:** hypothesis

**Against:** Molly Bang and Robin Williams are foundational, widely summarised texts. A frontier
model very likely holds their content already. The first Canon is therefore built from the
material where marginal lift should be *smallest*.

**Supporting:** Auditability, consistency and versioning are claimed benefits independent of lift.
Those are real but are not what this claim asserts.

**Falsifier:** Arm C versus Arm B on material the model already knows. A tie here does not kill the
Canon thesis outright — it relocates it to knowledge models lack, which points at Empirical Memory
and at specialist professional sources rather than at classics.

**Review trigger:** A/B/C experiment.

---

## 9. Explicit Canon lets a cheaper or open model approach frontier performance

**Status:** hypothesis — untested and downstream of §6 and §8

**Falsifier:** Same Canon, same schema, open model versus frontier. Only meaningful once §6 has a
positive result.

**Review trigger:** After §6 resolves.

---

## 10. Creative IR generalises beyond short-form advertising

**Status:** hypothesis — with early counter-evidence

**Against:** Across six sources, `delivery` and `acceptance` received **zero** bindings, and
`creative.hook` received zero including from Ogilvy. Multi-asset campaigns are explicitly excluded
in SPEC-01 v0.1. The IR was designed against short commercial assets and has only ever been tested
against them.

**Supporting:** `entities` and `relationships` were independently confirmed by sources from 1983
and 2009 with no knowledge of our schema — that is real evidence for those two fields.

**Falsifier:** Hand-specify a long-form explainer, a product demo and a brand film in the IR. Count
fields that cannot express what is needed.

**Review trigger:** Any request beyond short-form.

---

## 11. Empirical Memory will improve routing and repair over time

**Status:** hypothesis

**Supporting:** Structurally plausible; Finding 01 shows failure data is collectable cheaply.

**Against:** Depends entirely on §4. Without a working join, Empirical Memory is a log, not
knowledge. It also assumes failures recur across customers and model versions — untested, and
models change monthly.

**Falsifier:** After one hundred logged runs, test whether prior failures predict later ones for
the same task family. If they do not, the memory is a record and not a routing input.

**Review trigger:** One hundred logged production runs.

---

## 12. Cost per Accepted Outcome is an adequate primary objective

**Status:** provisional_design

**Against:** It is only defined if "accepted" is defined, and that is still open (SPEC-01 splits
user success criteria from a derived acceptance contract, but no acceptance contract has ever been
run). It also omits the intelligence layer's own cost, which on cheap generations could exceed the
generation itself.

**Falsifier:** If measured CpAO improves while human satisfaction or campaign outcome does not, the
metric is measuring the wrong thing.

**Review trigger:** First end-to-end run with a human accepter.

---

## 13. Human acceptance correlates sufficiently with commercial outcome

**Status:** hypothesis — assumed everywhere, examined nowhere

**Against:** The corpus itself warns against this. Ogilvy's whole opening argument is that
professionally admired advertising routinely fails to sell, and cites cases where advertised
groups bought *less*. Our entire evaluation design rests on human preference.

**Falsifier:** Any campaign-outcome data at all, compared against acceptance decisions.

**Review trigger:** First customer with measurable campaign outcomes. Likely far off — which is
exactly why it should be recorded now.

---

## 14. The library is representative enough to bootstrap the Canon

**Status:** hypothesis — **previous "weakened" verdict withdrawn as out of scope**

**Withdrawal.** This entry previously read "weakened by the six-source probe," citing uneven field
coverage. **Six partial chapters, chosen to test the schema rather than for coverage, cannot
weaken a claim about a forty-book library.** Per DIRECTION-RESET-01, absence in processed material
means "not found in what we processed," never "the Canon cannot know this." Several fields reported
as uncovered — `creative.hook`, `copy.cta` — are the explicit subject of library titles that were
never opened.

**What the Coverage Map actually establishes** (a real finding, correctly scoped): across 52 mapped
domains, the library gives strong or medium coverage of 37. It is strong where craft is old and
stable — composition, typography, lighting, shot grammar, advertising strategy.

**Against, and this is the real weakness:** it is thin exactly where the first product lives. Four
domains rated critical are **absent from the entire library**: short-form feed-native grammar,
Devanagari and Indic typography, Indian cultural and market context, and modern effectiveness
evidence. Three of those cannot be fixed by buying books.

**Falsifier:** run Experiment A on briefs in the absent domains — a Hindi festival Reel, a
feed-native hook — and compare uplift against briefs in well-covered domains. If uplift is near
zero where coverage is absent, the library's shape is the binding constraint.

**Review trigger:** after Experiment A, split by domain coverage.

---

## 15. Canon-derived requirements improve routing when combined with an empirical Registry

**Status:** hypothesis — **never tested, and previously judged against the wrong subsystem**

**Correction.** FINDINGS-11 reported "routing — no evidence, nothing in six books says which model
to use." That was a category error. Nothing in the Canon should ever name a model. The Canon's
routing contribution is **defining which capabilities a job requires**; the Registry supplies which
workflow has them.

**Claim:** a Creative IR carrying Canon-informed requirements — identity fidelity strictness,
temporal continuity, exact-copy constraints, script system, interaction complexity — routes better
than a brief alone, given the same Registry.

**Falsifier:** same briefs, same Registry, routing from a Canon-informed IR versus from raw brief
features. Compare pass rate and cost per accepted outcome.

**Review trigger:** requires a Capability Registry, which does not exist. Blocked on
[CAPABILITY-LAB-V0-PLAN](CAPABILITY-LAB-V0-PLAN.md).

---

## 16. The Canon V0 curriculum provides enough breadth to test 6a and 6b

**Status:** hypothesis

**Claim:** eleven sources selected by the Coverage Map give enough coverage that Experiments A and
B measure the Canon rather than measuring its gaps.

**Supporting:** the curriculum's stopping criterion is dimensional, not volumetric — every judging
dimension backed by two independent sources, cross-source concepts in three areas, at least one
recorded disagreement.

**Against:** the four critical absent domains remain absent after V0 by deliberate choice, and
several planned briefs will fall into them.

**Falsifier:** if Experiment A shows near-zero uplift and the retrieval logs show relevant Canon
was rarely found, the failure is curriculum breadth rather than the Canon thesis. Distinguishing
these requires logging what was retrieved for every brief — **and that logging must be built into
Experiment A from the start**, or the two causes become indistinguishable afterwards.

**Review trigger:** Experiment A retrieval logs.

---

## Register discipline

Anything that starts being repeated as settled gets an entry here first. An entry may only move to
`empirical_finding` when the falsifier named in it has actually been run — not when it merely feels
established.
