# E7-F — Benchmark v2 proposal (PROPOSED, NOT FROZEN)

**Task:** EVAL-007 · **Date:** 26 Aug 2026 · **Spend:** ₹0

> **This proposes; it does not freeze.** The Controller must integrate it with Canon's request-space
> findings and Resources' constraints before anything here becomes a design. Nothing in it modifies
> the authoritative capability contract or the existing 100-item bank.

---

## The one change that matters most

**Requirements in a real brief are dependent, and our fan-out is flat.**

Arena-T2I-Hard decomposes each real user prompt into a **DAG of yes/no questions** and checks them in
BFS order — *"If a parent isn't 'yes', its descendants are skipped and counted as failed."*

Our compound items declare a **flat `measurement_fanout`**. On a real brief that fails in a specific
direction: if the product was never rendered, then `logo_wordmark_fidelity`,
`packaging_brand_colour_fidelity` and `product_stability_in_clip` have nothing to be wrong about — and
a flat fan-out can score all three as **pass**. The asset that most completely failed the brief
returns the *highest* score.

**The inflation is largest exactly where the output is worst.**

### Proposed change — prerequisite edges, not new capabilities

Add to each compound item a `prerequisites` map: capability → the capability that must pass first.

```yaml
measurement_fanout: [product_identity, logo_wordmark_fidelity, packaging_brand_colour_fidelity]
prerequisites:
  logo_wordmark_fidelity: product_identity
  packaging_brand_colour_fidelity: product_identity
```

When a prerequisite fails, dependents are recorded **`not_applicable`** — not pass, not fail. We
already have that absence reason and the Resources contract already stores it. **This is a change to
the bank's item schema and the harness fan-out, not to the 36 capabilities.** It is the cheapest
high-value change in this proposal.

---

## Two axes, deliberately separate

E7-F requires request coverage and technical coverage to be separate. They answer different questions
and neither substitutes for the other:

| Axis | Question | Owner | Status |
|---|---|---|---|
| **Request coverage** | Do we test what customers actually ask for? | **Canon** (CANON-009) | Not yet available |
| **Technical coverage** | Do we test every capability under the conditions that move it? | **Eval** | This document |

**Eval must not invent the request axis.** A benchmark dimension is not market demand — VBench
measuring `aesthetic_quality` says nothing about whether anyone asks for it. Until Canon's findings
land, the request axis stays empty rather than being filled with our own guesses.

---

## Proposed four-tier structure

The current bank has two tiers (40 atomic + 60 compound). The evidence supports **four**, because the
existing compound tier is being asked to do three incompatible jobs at once.

### Tier 1 — Atomic probes · *keep unchanged*

Causal isolation. One capability, nothing else in frame. **No change proposed.** External practice
(GenEval, T2I-CompBench) is built the same way, and when a compound item fails, the atomic result is
the only thing that says why.

### Tier 2 — Compound production scenarios · *add prerequisite edges*

Realistic co-occurrence. **Keep the 10 scenario families × 6.** Add the DAG above. This is the tier
that currently over-reports.

### Tier 3 — Condition sweeps · *new, sparse and adaptive*

E7-D identifies **11 conditions**. Two levels each is 2,048 cells before a model is considered — a
cartesian product is not fundable and never will be.

**Sweep only four**, on the strongest evidence, and only on items that already exist:

| Condition | Why swept | Sweep |
|---|---|---|
| Duration | Drift is cumulative; short clips flatter every stability capability | short / long |
| Entity count | GenEval2 indexes by `atom_count` explicitly | low / high |
| Constraint load | Arena-T2I-Hard's prompts are hard *because* constraints stack | low / high |
| Language & script | English does not transfer to Hindi; Hinglish is hardest and most commercial | en / hi / hinglish |

The other seven are **recorded as declared conditions on every measurement, not swept**. Recording a
condition costs nothing; sweeping one costs a run.

**Adaptive rule:** sweep the *next* level only where the previous level did not already fail. Spending
a full sweep establishing that a workflow which fails at 6 seconds also fails at 20 buys nothing.

### Tier 4 — End-to-end customer outcomes · *reserved, not designed here*

Deliberately left empty. These must come from **Canon's accepted brief bank** after integration. Eval
authoring its own customer briefs is precisely how a benchmark starts defining the product instead of
the other way round — the failure this macro reset exists to correct.

---

## Workflow topology comparison

E7-F asks for materially different topologies compared for the same outcome. The clearest case:

> **"Founder talking to camera, 15 seconds"** can be produced as
> **(a)** native audio-video in one call, or
> **(b)** silent video + TTS + lip-sync transform.

These have different costs, different failure surfaces and different *applicable capability sets* —
in (a) sync is a property of one trial; in (b) it is a property of a transform over our own inputs,
which makes parts of it deterministically checkable.

**This is a Planner decision, not a customer request** (E7-D, PD-01). The benchmark should measure
both routes to the same declared outcome so the Planner later has evidence to choose between them.
**Eval does not choose.**

---

## Refresh and audit triggers

GenEval2 exists partly to address benchmark drift; HPSv2 says its own two versions are not
comparable. Drift is a design requirement, not maintenance.

| Trigger | Action |
|---|---|
| Provider model/version change | Re-measure affected Registry rows |
| **Evaluator version change** | **Re-qualify. Prior rows become non-comparable, not merely old** |
| Benchmark item leakage/contamination suspected | Rotate the affected items; retain a sealed holdout |
| Scheduled interval | Re-run active regression |
| Production failure spike | Add a permanent regression case |
| Canon request-space update | Re-check request-axis coverage |

**No decay formula is proposed.** Inventing one would encode a guess about drift rates we have never
measured. Triggers are auditable; a formula would only look precise.

---

## Recommended changes to the existing 100-item bank

Only where evidence shows a concrete gap. **The bank is a good baseline and most of it should stand.**

| # | Change | Evidence | Cost |
|---|---|---|---|
| 1 | **Add prerequisite edges to compound items** | Arena-T2I-Hard DAG | Schema + harness; no new generations |
| 2 | **Split `spatial_relationship` measurement into 2D and depth** | T2I-CompBench separates them; our own contract says depth is not decidable from boxes | Instrument routing; possibly a capability split (Controller's call) |
| 3 | **Add technical-integrity measurement to existing video items** | 3 of VBench's 16 dimensions; nothing in our 36 covers flicker/warping | Needs a capability decision first |
| 4 | **Record motion load alongside motion quality** | VBench separates `dynamic_degree` from `motion_smoothness` | Free — a recorded condition |
| 5 | **Split word correctness from pronunciation in speech items** | External TTS practice; ASR normalises mispronunciations | Two results per item, not two generations |
| 6 | **Add camera-instruction items** | VBench-2.0 Camera Motion; providers expose the control | Needs a capability decision first |

**Items 1 and 4 need no Controller capability decision and no new generations.** They are the ones to
do first.

---

## What this proposal deliberately does not do

- Does **not** add, rename or remove any of the 36 capabilities.
- Does **not** set a target item count for v2. The current 100 is a baseline; the right number falls
  out of integration, not out of this document.
- Does **not** author customer briefs.
- Does **not** adopt any external benchmark's taxonomy wholesale — VBench-2.0's physics group is
  explicitly *rejected* as scope we cannot act on.
- Does **not** propose a threshold. Zero remain approved.
