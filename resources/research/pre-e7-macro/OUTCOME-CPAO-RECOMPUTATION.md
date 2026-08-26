# Whole-outcome CpAO — fail-closed recomputation contract

**Task:** R3-E of `resources/tasks/RES-003-CLOUD-EVIDENCE-PROGRAM.md`
**Date:** 26 Aug 2026 · **Status:** PROPOSED, with a working implementation
**Engine:** `validators/recompute_outcome_cpao.py` · **Controls:** `validators/run_cpao_controls.sh`
**Result:** **9/9 controls behaved as declared** — 1 known-answer computation, 8 required refusals

---

## What CpAO is, at outcome level

> **CpAO = total cost of every distinct cost entry in an accepted outcome's provenance closure ÷
> number of accepted outcomes**

The denominator is **outcomes**, not trials, not units, not shots. Eight accepted shots inside one
rejected film are **zero accepted outcomes**.

## The problem this solves: production provenance is a DAG, not a tree

One generated logo gets composited into three shots. A recursive walk of the provenance tree visits
that logo once per path and **charges its cost three times**.

The fixture demonstrates it with real arithmetic. `art-logo` is generated once (6.00) and consumed by
two composites; `LED-LOCAL-OVERLAY` is referenced by two steps:

| | Total |
|---|---:|
| **Correct (distinct-entry) recomputation** | **45.25 XTS** |
| Naive tree walk, double-counting the shared logo | 51.25 XTS |
| **Overstatement** | **+13.3%** |

**The fix is structural, not arithmetic:** cost attaches to the **step or attempt that incurred it**,
never to the edge that consumed it. The engine collects the **set** of distinct `ledger_entry_id`s
reachable from the outcome and sums each **exactly once**. Two independent instances of the dedup
fire in the single fixture.

## What is counted

The known-answer fixture is one accepted 3-shot branded video. Hand-computed, then reproduced by the
engine:

| Component | Cost | Note |
|---|---:|---|
| shot 1 generation | 10.00 | |
| shot 2, attempt 1 — **ERROR** | 4.00 | **a failed attempt still cost money** |
| shot 2, retry — ok | 10.00 | retry is a new trial, linked backward |
| **logo generation — SHARED by 2 shots** | **6.00** | **counted once** |
| shot 3 generation | 10.00 | |
| **refused attempt** | 1.00 | **cost and latency spent, no bytes produced** |
| local concat (recorded compute) | 0.50 | local step, no provider call |
| local overlay (shared by 2 steps) | 0.00 | free, but the entry exists |
| evaluator measurements, 3 × 0.25 | 0.75 | separate from generation cost |
| human review | 3.00 | |
| **TOTAL** | **45.25** | 12 distinct ledger entries |
| **Accepted outcomes** | **1** | |
| **CpAO** | **45.25** | |

**Failed, refused and retried attempts are all in the total.** They are what the outcome actually cost.
A CpAO that silently drops them measures the cost of the *successful path*, which no customer ever
pays for on its own.

**A note on the fixture's own history:** the engine's first run disagreed with the fixture's declared
`distinct_cost_entries_counted`. The engine was right and **my hand-count was wrong** — I had collapsed
three separate evaluator entries into one. The fixture expectation was corrected; the total (45.25)
never changed. That is what a known-answer fixture is for, and it is recorded rather than quietly
fixed.

## When the engine refuses

**It refuses to emit a number rather than emit a wrong one.** A wrong CpAO is worse than no CpAO,
because a wrong one gets quoted.

**Eight refusal conditions, each with an executed negative control:**

| Control | Condition | Why refusing is right |
|---|---|---|
| `nc-01` | `cost_ref` does not resolve | A missing cost is not a zero cost |
| `nc-02` | ledger entry is mutable | A cost that can change afterwards is not evidence |
| `nc-03` | **no accepted outcome** | CpAO is **undefined** — not zero, not infinity. Reporting 0 would make the worst run look free |
| `nc-04` | mixed currencies | No exchange rate is ever invented to produce a tidy number |
| `nc-05` | delivered artifact not in its own provenance | The total would not describe what was delivered |
| `nc-06` | local transform with no recipe | The composition is unreproducible, so the outcome is not auditable |
| `nc-07` | `provider_call` step with no attempt | The call either happened and has a row, or it is not a provider call |
| `nc-08` | ledger entry with no amount | Treating a blank as zero is how a real cost disappears |

**Exit codes:** `0` computed and matched · `1` computed but disagreed · `2` could not read the input ·
`3` **refused, as a negative control expected**. A refusal is a distinct outcome from a failure to run.

**Control `00` exists for a reason.** A refusal engine that refuses everything would pass all eight
negative controls and be useless. The happy-path fixture is what proves the engine can still produce
a number when the evidence supports one.

## What this does not decide

Three questions determine what CpAO *means*, and none is Resources' to answer. **The schema records
the underlying facts either way, so the Controller can decide later without re-running anything.**

**OQ-1 — Is human review time counted?** Counting it measures the true cost to the business; excluding
it measures the API cost of the production route. Both defensible, different numbers. The fixture
includes a human cost so both are computable.

**OQ-2 — Does a rejected revision's cost count toward the accepted one?** If a customer rejects v1 and
accepts v2, the honest cost of the accepted outcome probably includes v1. Excluding revisions
systematically understates the cost of hard briefs. The topology persists the `supersedes` link so
either rule is computable.

**OQ-3 — Is an outcome with an unreproducible local step still auditable?** Proposed: mark it
`reproducibility_status: partial` rather than silently treating it as fully reproducible.

## Dependency on R3-D

This engine assumes the R3-D topology (`job → outcome → set → unit → step → attempt → artifact`,
with multi-parent artifact lineage). **Both are proposals.** Until the Controller integrates them,
`resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` **v2.1 remains authoritative**, and v2.1 cannot
express an outcome — which is precisely why whole-outcome CpAO is not computable under it today.

## Reproducing this

```bash
python3 resources/research/pre-e7-macro/validators/recompute_outcome_cpao.py \
        resources/research/pre-e7-macro/fixtures/cpao/outcome-happy.yaml
bash resources/research/pre-e7-macro/validators/run_cpao_controls.sh
```

Every value in every fixture is synthetic: fictional provider, `basis: synthetic_test`, currency
**XTS** (the ISO code reserved for testing, so no figure here can be mistaken for a real amount).
**No provider was called and no money was spent.**
