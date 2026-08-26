# Whole-outcome CpAO contract v3

**Task:** R4-D · **Date:** 26 Aug 2026 · **Engine:** `validators/recompute_cpao_v3.py`
**Controls:** `validators/run_cpao_controls_v3.sh` — **executed, 13/13 as declared**
**Controller basis:** integration decision §4.2

---

## Two required views

| View | Contents | Role |
|---|---|---|
| **API/tool CpAO** | `api_tool` costs only | **diagnostic** |
| **Fully-loaded CpAO** | `api_tool` + `local_compute` + `human_required` | **PRIMARY BUSINESS METRIC** |

> **CpAO = total distinct cost in the accepted outcome's provenance ÷ accepted outcomes**

The denominator is **outcomes**, never trials, units or shots.

**Worked example** (`v3-valid-outcome.yaml`, one accepted 3-shot branded video):

| Class | Cost |
|---|---:|
| `api_tool` — 7 provider calls incl. 1 error + 1 refusal, plus 2 evaluator calls | **50.00** |
| `local_compute` — overlay (shared, counted once) + concat + mix | **1.50** |
| `human_required` — review | **20.00** |
| **fully-loaded** | **71.50** |

**API/tool CpAO 50.00 · fully-loaded CpAO 71.50.** The gap is the point: a system optimised on the
diagnostic number alone would happily trade 20.00 of human review for 5.00 of API spend and report an
improvement.

## Cost classes

`api_tool` · `local_compute` · `human_required` · `human_optional`

**`human_optional` is recorded and excluded from both views.** Only human time **required in the
operational path** is loaded, per the Controller decision. Discretionary review is kept in the ledger
so the choice can be revisited without re-running anything.

**An unclassified cost is a refusal, not a default.** A cost with no class cannot be placed in either
view, so neither number can be honestly produced.

## The attribution rule

> **A cost attaches to the step or attempt that INCURRED it, never to the edge that CONSUMED it.**

Production provenance is a **DAG, not a tree**. A logo composited into three shots is visited three
times by a recursive walk. The engine collects the **set of distinct `ledger_entry_id`s** reachable
from the accepted outcome and sums each **exactly once**.

In the worked example the overlay entry is referenced by **two** steps and the logo artifact is consumed
by **two** composites; both are counted once. A naive walk would report **71.75** instead of 71.50.

## The revision journey, and where it stops

Rejected revisions **belong to the accepted outcome's cost** when they are part of the same journey:

| Fixture | Charged | API/tool | Fully-loaded |
|---|---|---:|---:|
| `revision-journey-included` | rejected v1 **+** accepted v2 | 20.00 | **30.00** |
| `scope-change-cuts-journey` | accepted v2 **only** | 10.00 | **15.00** |

**The two fixtures are identical except for one flag** — `scope_change_boundary: true` on v1 — and the
difference is exactly the earlier journey's cost.

**Why include revisions by default:** excluding them systematically understates the cost of briefs
needing a second pass, which are precisely the briefs that matter commercially.

**Why the boundary exists:** when a customer *materially changes the brief*, the earlier work belongs
to a different journey. Charging it forward would make a scope change look like a production failure.

## When the engine refuses

**It refuses to emit a number rather than emit a wrong one**, because a wrong CpAO gets quoted.

| Control | Condition | Why |
|---|---|---|
| `nc-unresolvable-cost-ref` | cost ref does not resolve | a missing cost is not a zero cost |
| `nc-ledger-without-amount` | no amount | a blank is not zero |
| `nc-mutable-ledger-entry` | `immutable != true` | a changeable cost is not evidence |
| `nc-unclassified-cost` | no `cost_class` | cannot be placed in either view |
| `nc-mixed-currency` | two currencies | no exchange rate is ever invented |
| `nc-no-accepted-outcome` | nothing accepted | CpAO is **undefined**, not zero |
| `nc-accepted-without-final-artifact` | accepted, no deliverable | cannot accept nothing |
| `nc-final-artifact-outside-provenance` | delivered artifact not in its own provenance | total would not describe what shipped |
| `nc-revision-chain-cycle` | outcome supersedes itself | the journey would never terminate |
| `nc-local-step-with-attempt` | local step carrying a provider attempt | a fabricated trial corrupts any per-trial view |

**Exit codes:** `0` computed and matched · `1` computed but disagreed · `2` could not read input ·
`3` **refused** (what negative controls expect).

**Three positive fixtures exist deliberately.** An engine that refuses everything would pass all ten
negatives and be useless.

## What this contract does not decide

- **What counts as "required" human time.** Resources records the class; the operational definition is
  the Controller's.
- **Any threshold.** No CpAO target, no acceptable range. Eval and the Controller own that.
- **Model or provider selection.** Nothing here ranks anything.
