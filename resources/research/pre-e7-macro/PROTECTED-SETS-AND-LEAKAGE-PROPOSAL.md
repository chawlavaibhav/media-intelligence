# Protected sets and leakage — proposal for the next program

**Task:** R3-C of `resources/tasks/RES-003-CLOUD-EVIDENCE-PROGRAM.md`
**Date:** 26 Aug 2026 · **Status:** PROPOSED — not an approved decision
**Builds on:** the accepted V1 allocation contract (`resources/v1/RESOURCE-ALLOCATION-SPEC.md`)
**Machine-checkable form:** the existing `check_allocation_leakage.py` already implements the
three-level check and the indeterminate outcome; this proposal adds **role 1** and **request-space
lineage**, which it does not yet cover.

---

## Why this needs to change now

The V1 contract has five roles — development, calibration, qualification, reserve, regression — and
three independence levels: byte, content, source lineage. It was designed for **media**.

The next program introduces something it does not model: **request-space data used to learn what to
build**. Canon will derive a request taxonomy from real user prompts. Eval will author benchmark
items. If those two activities draw on the same lineage, the benchmark tests the taxonomy on its own
ancestors and the result means nothing — and **no existing check would notice**, because prompts are
text and the existing levels reason about media.

R3-A found this is not hypothetical. **Arena-T2I-Hard's 310 prompts are sampled from the same public
arena pool as the LMArena open data.** Discovery on one and holdout on the other is circular today.

## The five roles

Roles are **allocations inside a named experiment at a named version**, never permanent properties of
data. That principle is unchanged and load-bearing.

| # | Role | What it is | Protected? | Contaminates |
|---|---|---|:--:|---|
| **1** | `request_discovery` | Data used to *learn the taxonomy* — what people ask for, what recurs | no | **everything downstream sharing its lineage** |
| **2** | `benchmark_construction` | Examples used to author or tune benchmark tasks | no | active benchmark + holdout, on shared lineage |
| **3** | `evaluator_calibration` | Material used to set an instrument's operating point | no | qualification of that instrument |
| **4** | `active_benchmark` | Material used to score current models | no | the holdout, on shared lineage |
| **5** | `final_holdout` | Untouched reserve, incl. regression reserve | **yes** | — |

**Role 1 is new and it is the one that matters most.** It sits *upstream of the benchmark's
existence*, so its contamination reach is the widest in the system. Anything that shares lineage with
the discovery set cannot honestly serve as evidence that the resulting design generalises.

`regression` from the V1 contract folds in as a **subtype of role 5** with a standing caveat: a
regression item is contaminated by construction — somebody already studied it closely — so it is valid
as a regression stimulus and disqualified for calibration, qualification or holdout on anything
sharing its lineage.

## Four independence levels — three inherited, one new

| Level | Catches | Status |
|---|---|---|
| **byte** | the same file twice | inherited, implemented |
| **content** | crops, re-encodes, transforms of shared material | inherited, implemented |
| **source lineage** | same collection/lab/platform ancestry, no byte or content overlap | inherited, implemented |
| **request lineage** | **the same underlying request population** | **NEW — proposed** |

### Why the three existing levels are not enough

The project already paid for the byte/content distinction: on the CVIT pair, **byte dedup reports
12.4% overlap where content lineage reports 99.1%**, and a hash-clean split was demonstrably
**100% contaminated**. That lesson generalises but the mechanism does not: **prompts share no bytes,
no parent photograph, and no lab.** Two prompts drawn from the same arena pool in the same quarter are
non-independent for taxonomy purposes and *every existing level reports them clean*.

### Request lineage, defined

Two request-space items share a **request lineage** when they come from the same underlying request
population: the same platform, community or interface, over an overlapping period, collected by the
same or a derivative method.

Registered groups from R3-A:

| Request lineage | Members | Consequence |
|---|---|---|
| `lin_lmarena` | LMArena open data · **Arena-T2I-Hard** | never discovery *and* holdout in one experiment |
| `lin_pika_discord` | VidProM · TIP-I2V | one lineage — same authors, same Discord, same method |
| `lin_diffusiondb` | DiffusionDB · **our ImageRewardDB** | we already hold part of this lineage |

**Unknown request lineage is INDETERMINATE, never independent.** This is the accepted R-C4 rule
carried across unchanged: two different `lin_unknown::` keys are not evidence of two different
lineages, and the validator already returns **exit 3 — independence not established** rather than
certifying.

## The anti-circularity rules

These are the operative output of this package.

**C1 — Discovery contaminates its whole lineage.** If a lineage supplies `request_discovery`, no
member of that lineage may serve `final_holdout` in the same experiment. Directly blocks
Canon-discovers-on-arena → Eval-holds-out-on-Arena-T2I-Hard.

**C2 — A rephrase is not an independent item.** Paraphrasing, translating, templating or
LLM-rewriting a discovery-set request produces a **descendant**, not a new item. It inherits the
parent's request lineage. Testing on rephrases of the discovery set and calling it generalisation is
the specific failure this package exists to prevent.

**C3 — A derived taxonomy carries its parent's lineage.** If a request grammar is learned from
lineage L, benchmark items *authored to instantiate that grammar* inherit L for holdout purposes.
Authorship does not launder ancestry. **This is the strictest rule here and the most likely to be
argued about** — see the open question below.

**C4 — Time is not independence.** A later sample from the same platform is the same lineage. Arena
prompts from Q2 2026 are not independent of arena prompts from Q1 2026.

**C5 — One lineage, one role, one experiment.** Inherited from V1 and unchanged.

**C6 — Freezing is one-way.** A holdout anyone has inspected is no longer a holdout. Inherited.

## What a clean split would look like

Illustrative only — Resources does not assign roles until an experiment names them, and every view
still carries `protected_role: unassigned_pending_eval_experiment_split`.

| Role | Candidate | Why it works |
|---|---|---|
| `request_discovery` | LMArena open data (`lin_lmarena`) | CC-BY-4.0, commercial use permitted, multi-model |
| `benchmark_construction` | authored items + GenEval/T2I-CompBench structures | Eval-authored; deterministic fixtures add no lineage |
| `evaluator_calibration` | CVIT Devanagari lineage; frozen 96-item battery | already held; one pool, one role |
| `active_benchmark` | Eval-generated outputs | generated by us, no external lineage |
| `final_holdout` | **BSTD** (`lin_bhashini_iitj`) + a frozen slice of the future commercial bank | genuinely independent of everything above |

**The cost of this split, stated plainly:** adopting LMArena for discovery **spends Arena-T2I-Hard as
a holdout**. That is a real loss — it is a well-constructed external benchmark — and it is the
unavoidable price of using its parent pool for discovery. Eval and the Controller should make that
trade knowingly rather than discover it after the fact.

## Implementation

The existing validator already does most of this. What it needs:

1. **`request_discovery` added** to the role vocabulary, as a non-protected role whose lineage
   contaminates protected roles.
2. **A `request_lineage` level** alongside byte/content/source, sharing the same
   already-implemented indeterminate machinery.
3. **A `derived_from_request_lineage` field** on authored benchmark items, so C2 and C3 are
   mechanically checkable rather than remembered.
4. **The lineage registry extended** with the three request-space groups above.

Points 1, 2 and 4 are small changes to `lineage_keys.py` and `check_allocation_leakage.py`. Point 3
requires Eval to emit one field on authored items, which is a cross-stream interface item for the
integration gate — not something Resources may decide alone.

## Open question for the Controller

**How strictly should C3 apply?** Under the strict reading, *any* benchmark item authored to
instantiate a grammar learned from lineage L inherits L, which makes a truly independent holdout
expensive — it must come from a lineage untouched by discovery. Under a looser reading, an authored
item that no longer resembles any specific discovery item is independent, which is defensible and much
harder to check mechanically.

**Resources' position: adopt the strict reading initially**, because it is checkable and because the
looser reading's boundary ("no longer resembles") is exactly the kind of judgement that erodes under
schedule pressure. **This is a recommendation, not a decision.** Where the line sits determines
whether the project can ever claim a generalisation result, so it is the Controller's to draw.

## What this proposal does not do

- It does **not** assign any role to any material. Roles belong to a named experiment; none exists.
- It does **not** decide what Canon's taxonomy is or what Eval measures.
- It does **not** claim that passing these checks proves independence. Absence of a detected collision
  is not proof, and the validator prints exactly that on every clean run.
