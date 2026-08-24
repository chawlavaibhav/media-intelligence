# Direction Reset 01 — What the Canon is responsible for

**Date:** 23 Aug 2026 · **Status:** correction of scope, not of architecture
**Nothing in FINDINGS-01 through 11 is deleted.** Specific conclusions are corrected below.

---

## The error

Recent work began evaluating the Creative Canon against responsibilities that were never its own.
FINDINGS-11 reported that 35% of a twenty-failure sample had "no useful Canon relationship" and
that routing showed "no evidence" of benefit. Both statements are true of what was measured. Both
were measured against the wrong subsystem.

Seven of those twenty failures were server restarts, storage paths, provider API drift and a
platform message limit. Several more were diffusion artefacts — prompt text leaking into pixels,
glyph substitution in Devanagari. **No craft literature from any century was ever supposed to
explain those.** Reporting their absence as a Canon result made a category error look like a
finding.

The separation below is the original one. It is being restored, not invented.

---

## Ownership

### The Creative Canon owns

Durable, explicit creative and media expertise. It answers:

- Given this objective, audience, message, product and medium, **what does a good outcome need to
  accomplish?**
- What principles, techniques, patterns, strategies and trade-offs are available for constructing it?
- How do hierarchy, composition, typography, colour, lighting, visual weight, product prominence,
  storytelling, cinematography, continuity, editing, pacing, persuasion, brand communication and
  emotional effect work — individually, and against each other?
- How should an incomplete customer instruction become a better creative plan **without overriding
  explicit intent?**
- Given an asset and its brief, **what should be inspected** to judge whether it is good *for that
  objective*?
- If an output is creatively weak, what is wrong at craft level and what creative change might fix it?

The working image: **cookbook + culinary school + tasting expertise.** Recipes, ingredients,
techniques, interactions, exceptions, and the trained judgement to assess a result.

**It does not know which oven in today's kitchen works best.**

### The Capability Lab owns

What today's models and workflows can actually do, measured. Which render exact text. Which
preserve identity. Which handle human-object interaction, temporal consistency, motion, Hindi
speech, reference conditioning. Failure rates, cost, latency, reliability. Which repairs work in
practice.

This changes monthly and is external to the Canon by construction. It produces the Capability
Registry.

### The Production Planner / Router owns

Choosing today's execution path. It reads the Creative IR's requirements and the Registry's
measured abilities, and picks a workflow at the lowest expected cost to an accepted outcome.

### Empirical Memory owns

What actually happened on real runs — this brief, this workflow, this failure, this repair, this
acceptance, this customer. Observer's own words preserved.

### Evaluation owns

Two separate instruments that must not be collapsed:

**A — Technical / hard fidelity.** Exact text matches, QR decodes, logo exactness, object count,
aspect ratio, product identity preserved. Deterministic or empirically validated instruments
wherever possible. Finding 01 is this side's founding result.

**B — Creative fitness.** Does the intended hierarchy actually work; is the product appropriately
prominent; does the composition communicate the intended relationship; is the emotional target
achieved; does typography support the message; does attention evolve correctly across a video; do
cuts and pacing support the story; does the ad communicate a clear proposition.

**The Canon should be especially valuable for B, and largely irrelevant to A.** One evaluator and
one knowledge source must not be asked to cover both.

---

## How they interact

```
CUSTOMER INPUT
     ↓
NORMALIZED REQUEST
     ↓
CREATIVE INTELLIGENCE + CANON
     ↓
CREATIVE IR          "this job needs strong identity fidelity, temporal
     ↓                continuity, exact end-card copy, this hierarchy,
     ↓                this emotional target"
     +
CAPABILITY REGISTRY  "these current workflows have measured ability to
     ↓                satisfy those requirements, at this cost"
PRODUCTION PLANNER / ROUTER
     ↓
EXECUTE → EVALUATE (A + B) → REPAIR
     ↓
EMPIRICAL MEMORY ──→ feeds Capability Lab and Customer Memory
```

**The Canon's role in routing, stated correctly:** it helps define **which capabilities the job
requires**. It must never claim to know **which current model has them**. Those are two different
sentences and only the second needs empirical data.

---

## Corrections to specific published conclusions

The originals stay on disk. These supersede them.

### FINDINGS-11 — the results table

> "35% no useful Canon relationship"

**Corrected.** That figure counts infrastructure failures, provider API drift, a platform message
limit, tooling incapacity and diffusion artefacts. Those belong to the Capability Lab, Production
and operations. The correct reading of the same experiment is: **of the failures that were
creative-craft failures at all, the Canon related to most of them** — and it explained one at
mechanism level well enough to name the repair.

The table is retained as an architecture result. **It is not a Canon coverage score and must not
be cited as one.**

### FINDINGS-11 — routing

> "Routing — no evidence. Nothing in six books says which model to use."

**Corrected as a category error.** Nothing in the Canon should ever say which model to use. What
was actually tested was whether craft books name models, which they do not and should not. The
untested claim is the real one: *do Canon-derived requirements, combined with an empirical
Registry, improve routing?* Recorded as a hypothesis in the register; never examined.

### FINDINGS-11 — "the failures cluster where the books do not reach"

**Corrected.** The sample was drawn from whatever had been recorded, which was dominated by
generator artefacts and operations. It says where *that sample* sat, not where craft knowledge
reaches.

### FINDINGS-09 and FINDINGS-10 — "fields never covered"

> `delivery`, `acceptance`, `creative.hook`, `copy.cta`, `brand.logo`, `brand.mandatories`,
> `video.dialogue_intent` received nothing.

**Partially corrected.** Reported as though it revealed structure in the IR. It is largely a
sample artefact: six partial chapters, chosen to test the schema, not chosen for coverage. The
library contains untouched sources that plainly address several of them — `creative.hook` and
`copy.cta` are the explicit subject matter of *Hey Whipple, Squeeze This* and *Scientific
Advertising*.

The narrower claim survives: `delivery` specs and `acceptance` thresholds plausibly come from
customers and platforms rather than craft books. That remains a hypothesis, now testable against
the Coverage Map.

### FINDINGS-08 — "highest content, lowest yield"

**Reframed.** *Light: Science & Magic*'s low atom count was attributed to the source. It was
caused by the admission rule, since corrected — and by the fact that much of the book is
production knowledge, which is correct behaviour, not low yield.

### Assumption 14 — corpus representativeness

**Correction of scope.** Marked "weakened by the six-source probe." Six partial chapters cannot
weaken a claim about a forty-book library. Re-scoped in the register to what was actually
observed.

---

## What FINDINGS-11 did and did not establish

**Did establish**
- Creative knowledge and observed failures *can* connect, sometimes at mechanism level — Molly Bang
  explains a floating logo by the absence of a baseline.
- Connections occur at **different abstraction levels**: shared mechanism, violated requirement,
  commercial consequence. The ontology serves only the first.
- **Book knowledge can shape how we evaluate.** *Grammar of the Shot* says continuity breaks are
  invisible frame-by-frame; the Wan clip's drifting misspelling was exactly that, and Finding 01
  could only record it as incidental. This is the most transferable result in the file.
- Three concrete gaps in the ontology's relation vocabulary.
- Failure logging must permit multiple defects per output.

**Did not establish**
- Anything about Canon coverage, quality or usefulness.
- Anything about routing.
- Anything about the forty-book library.
- Anything about creative planning or creative evaluation — **neither has ever been tested.**

It was an experiment about knowledge representation that used failures as its material. It was
never an evaluation of creative expertise.

---

## What remains correct and is not reopened

1. Normalized Request and Creative IR remain separate.
2. Creative IR and Production IR remain separate.
3. Source Knowledge remains separate from Product Bindings.
4. Source claims preserve precise provenance.
5. SourceConceptSystems preserve knowledge that cannot safely be atomised.
6. Empirical and model behaviour remain separate from book knowledge.
7. Product bindings are versioned and replaceable.
8. Source terminology is preserved, never overwritten.
9. Evidence is factual characteristics, not invented decimals.
10. The evaluator itself must be calibrated and benchmarked.

**No further abstract schema expansion until real material breaks something.**

---

## Standing rule

> A missing relationship in processed material means **"not found in the currently processed
> material."** It never means "the Canon cannot know this."

Any future finding that reports a Canon limitation must state which subsystem owns the failure
before drawing a conclusion.
