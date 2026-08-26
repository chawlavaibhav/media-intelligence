# Benchmark v2 — Wave 1 (PROPOSED, NOT FROZEN)

**Task:** EVAL-009 / E9-E · **Date:** 26 Aug 2026 · **Spend:** ₹0

> **The V1 100-item bank is preserved byte-identical** at `eval/v1/bank/master-bank-v1.jsonl` as a historical baseline. It is not rewritten, not migrated and not deleted.

## Shape

| Layer | Purpose | Items |
|---|---|---:|
| 1 — atomic probes | causal isolation, one capability each | **64** |
| 2 — compound scenarios | realistic co-occurrence **with prerequisite graphs** | **30** |
| 3 — sparse adaptive sweeps | condition dependence, reusing layer-2 items | +25 instances |
| 4 — end-to-end outcomes | accepted-outcome evidence | **reserved, parameterised** |
| **Base items** | | **94** |
| **Item instances** (incl. sweeps) | | **119** |

## Crossed by requested operation

The benchmark covers **materially different request operations**, not just generate-from-nothing:

| Requested operation | Compound items |
|---|---:|
| `animate` | 3 |
| `edit` | 5 |
| `generate` | 19 |
| `variants` | 3 |

`requested_operation` is **customer-side**; `workflow_mode` is the route we chose. Both are recorded and neither may be populated from the other.

## Layer 4 is reserved, not invented

**8 slots** are held for end-to-end briefs, × 2 recipes × 2 repeats.

**Eval does not author customer briefs.** CANON-010 freezes the Media Request Grammar and the request-coverage extension. Until then these are SLOTS with a declared operation mix, not items. Eval authoring its own customer briefs is precisely how a benchmark starts defining the product instead of the other way round.

Because layer 4 is parameterised, **CpAO is not computable in Wave 1** — there are no accepted outcomes to divide by. That is stated rather than papered over.

## Why this is not a cartesian product

Two mechanisms, both deliberate:

**1 · Slot-targeted item sets.** Each roster slot runs the atomic items for *its own* declared capabilities, the compound scenarios its workflow mode can serve, a small shared comparability core, and its share of the sweeps. Running every item on every slot would nearly double the wave and buy redundant evidence — the first draft of this design did exactly that and was cut from 943 generations to 494.

**2 · Sparse adaptive sweeps.** 4 of 12 condition families are swept, on subsets. 12 families at two levels each would be 4,096 cells before a capability or model is considered.

- **Stop rule:** Stop expanding a sweep axis after two consecutive failing levels on the same item.

- **Expansion rule:** Expand an axis only where a level PASSED and the next level is materially harder.

- **Adaptive rule:** Sweep the next level only where the previous did NOT already fail. No saving is claimed in the forecast.

## Repeats vs retries

A repeat is a DELIBERATE experimental re-run to estimate reliability, decided before any result is seen. It gets its own trial id and NEVER counts as an independent base item. A RETRY is caused by a prior failure, belongs to the acceptance/CpAO chain, and must never be pooled into a capability pass-rate cell.

## Wave-1 counts

| | |
|---|---:|
| Core roster slots | 12 |
| **Generations** | **494** |
| **Evaluator calls** | **5,515** |
| Human review units | 188.0 |
| Reserve slots (not in totals) | 2 |

Evaluator calls outnumber generations about **11:1** — generate-once working as intended, and the reason evaluator cost is a separate top-level line.

**Retries are excluded and must be predeclared.** Discovering a retry allowance mid-run is a budget change, not an adjustment.

