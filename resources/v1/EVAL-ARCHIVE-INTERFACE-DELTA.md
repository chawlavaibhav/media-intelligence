# Eval archive interface delta — exact remaining failing fields

**Task:** RI-C5 of `resources/tasks/RESOURCES-EVAL-STORAGE-INTEGRATION-PASS.md`
**Status:** **`BLOCKED_WAITING_FOR_EVAL_INTERFACE`** — one defect class remaining, in the cost ledger only
**Date:** 26 Aug 2026 · Owner: Resources · **No Eval file was edited. The branch was read in a detached worktree.**

**Gate command:** `bash resources/v1/validators/validate_eval_archive.sh`

---

## Headline

Eval's integration correction landed during this pass. Measured against it:

| Eval ref | Violations |
|---|---:|
| `d91500e` (pre-integration, archive last written at `dfe3a5a`) | **125** |
| **`adac747`** "EVAL-Resources storage integration: EI-C1 through EI-C8" | **114** |

The raw counts hide the real progress, because the shape of the failure changed completely.

**At `adac747` the four core entity files — `attempts`, `artifacts`, `measurements`,
`acceptances` — validate cleanly.** Every one of the 114 remaining violations is a **cost-ledger
entry-schema** issue, and the arithmetic accounts for all of them exactly:

> **19 ledger entries × 6 failing checks each = 114.**

## What Eval now gets right

Everything that was wrong before is fixed:

| Was | Now |
|---|---|
| no `trial_id` on any row | `trial_id` present; `trial_id == attempt_id`, satisfying one-call-one-trial (RI-C1) |
| `api_status: "refused"` | `status: "refusal"` — the frozen id (RI-C2) |
| `lane: "video"` | `lane: "image"` etc. from the frozen machine vocabulary (RI-C2) |
| no `prompt_hash`, `cost_ref`, `storage_class` | all present; `storage_class: C_irreproducible_empirical` |
| artifacts missing `trial_id`, `output_bytes`, `media_kind` | all present |
| measurements missing instrument version/config/qualification | all present |
| 1 measurement with both `result` and `absence_reason` | fixed |
| derived artifacts not modelled | **4 derived artifacts**, correctly inheriting parent trial and attempt |
| refusals/errors indistinguishable | **2 failed attempts preserved individually with their reasons** |

Fan-out is 7.00 measurements per artifact, 0 duplicate media copies, observation units canonical.

## Two naming collisions Resources absorbed, not Eval

Both are cosmetic — no content rule was relaxed to accept either, and doing so makes the validator
check *more*, not less, because it can now read the ledger at all:

| Eval emits | Contract said | Resolution |
|---|---|---|
| `cost-ledger.jsonl` | `cost_ledger.jsonl` | Both accepted. Canonical name unchanged; hyphen accepted as an alias. |
| `cost_ref` as the ledger entry's own id | `ledger_entry_id` | `cost_ref` accepted as an alias for the entry id. It names the same value attempts point at. |

**Cost-reference resolution now works end to end:** all 5 attempt `cost_ref`s and all 14 measurement
`evaluator_cost_ref`s resolve against the 19 ledger entries, and generation and evaluator costs are
already separate entries.

## The one remaining defect class

Every ledger entry is missing four required fields, which produces six failures per entry:

| Missing / invalid | Entries | Why it is required (RI-C4) |
|---|---:|---|
| `unit` | **19/19** | An amount without a unit is not a cost. `0.01` per call, per second and per image are three different numbers. |
| `recorded_at` | **19/19** | When the cost was recorded. Without it a ledger cannot be reconciled against a provider invoice later. |
| `basis` | **19/19** | Whether the figure is a billed amount, an API-reported amount, a modelled estimate, or synthetic. This is the field that stops a price-list guess being read as a bill. |
| `immutable` | **19/19** | The guarantee that the entry is never edited. A correction must be a new entry. |
| `basis` invalid (`None`) | 19/19 | Consequence of the above. |
| `immutable` not `true` | 19/19 | Consequence of the above. |

**Eval's intent is already right, and honest.** Each entry carries
`source: "SYNTHETIC_SELFTEST_LEDGER"` and the note *"Fabricated for harness self-tests. NOT a
provider price. No real rate has been obtained — see E2-BLOCK-01."* That is exactly the disclosure
the contract wants; it simply is not yet in the fields the contract names.

The mapping is small:

```
source: "SYNTHETIC_SELFTEST_LEDGER"   →   basis: "synthetic_test"  +  synthetic: true
(new)                                 →   unit: "call"
(new)                                 →   recorded_at: "<ISO-8601 UTC>"
(new)                                 →   immutable: true
```

`kind: "generation" | "evaluator"` is a useful extra and the contract does not object to it.

## One recommendation, not a violation

Synthetic entries carry `currency: "USD"` with amounts like `0.01` for calls that never happened.
The accompanying note disclaims it clearly, so this is **not** currently failing anything. But
`amount: 0.01, currency: USD` reads as a real dollar figure at a glance, and the contract's rule is
that a synthetic test may never carry a fabricated real-provider cost. Consider a non-currency test
code (the Resources dummy generator uses `XTS`, the ISO code reserved for testing) so the disclaimer
lives in the data rather than only in a note.

This is a suggestion for Eval to accept or reject. Resources does not set it as a gate.

## Closing the gate

```bash
bash resources/v1/validators/validate_eval_archive.sh
```

Exit 0 closes it. The contract stands as written — `EVAL-STORAGE-HANDOFF.md` §6 is the field-by-field
ledger specification, and negative controls `19`, `20` and `21` hold the resolution, reference-not-a-number
and immutability rules in place.
