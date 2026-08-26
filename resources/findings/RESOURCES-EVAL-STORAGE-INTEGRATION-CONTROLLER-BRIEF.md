# Resources–Eval storage integration pass — Controller Brief

**Task:** `resources/tasks/RESOURCES-EVAL-STORAGE-INTEGRATION-PASS.md` (RI-C1 … RI-C5)
**Date:** 26 Aug 2026 · **Branch:** `work/resources-v1-overnight` · **Not merged to `main`**
**Status:** RI-C1 … RI-C4 **complete**. RI-C5 **`BLOCKED_WAITING_FOR_EVAL_INTERFACE`** — one defect class left.
**Spend:** ₹0 / $0 · no acquisition, no paid API call, no raw-corpus access, **no Eval file edited**.

---

## 1. The bottom line

**Resources' side is done. The wire is one field-set away from closing.**

The gate is not "our validator passes on our own generator" — it is "**a corrected Eval harness
archive validates with the Resources validator at exit 0**". Eval pushed their integration correction
(`adac747`) while this pass was running, so this brief measures the real thing, twice:

| Eval ref | Violations | Shape |
|---|---:|---|
| `d91500e` (pre-integration; archive last written at `dfe3a5a`) | **125** | every entity, every row |
| **`adac747`** "EVAL-Resources storage integration: EI-C1 through EI-C8" | **114** | **cost ledger only** |

The raw counts understate the progress, because the *shape* changed completely.

> **At `adac747`, `attempts`, `artifacts`, `measurements` and `acceptances` all validate cleanly.
> All 114 remaining violations are cost-ledger entry-schema, and the arithmetic accounts for every
> one: 19 ledger entries × 6 failing checks = 114.**

**Four ledger fields close the gate:** `unit`, `recorded_at`, `basis`, `immutable`. Eval's intent is
already correct and honest — every entry says *"Fabricated for harness self-tests. NOT a provider
price."* — it is simply not yet in the fields the contract names. Exact mapping in
`resources/v1/EVAL-ARCHIVE-INTERFACE-DELTA.md`.

**The validator was not weakened.** Nothing was relaxed to make Eval's archive pass.

## 2. What was corrected on the Resources side

| ID | Controller decision | Status | Enforcement |
|---|---|---|---|
| **RI-C1** | One call = one trial | **done** | `attempt_id` ↔ `trial_id` one-to-one, enforced; controls `13`, `14` |
| **RI-C2** | Freeze machine vocabularies | **done** | lane + status membership checks; controls `15`, `16` |
| **RI-C3** | Absence vocabulary; attempt failures ≠ measurement absences | **done** | canonical set + two forbidden classes; controls `17`, `18` |
| **RI-C4** | Required fields + explicit cost provenance | **done** | cost-ledger contract, reference resolution; controls `19`, `20`, `21` |
| **RI-C5** | Prove the real cross-branch interface | **blocked** | `validate_eval_archive.sh`; see §1 |

### RI-C1 — trial semantics

The permissive phrase that `trial_id` *"groups the attempts belonging to one experimental trial"* is
**removed**. A trial is now the call itself: every attempt maps to exactly one `trial_id` and no two
attempts may share one. A repeat is a **new trial** linked by `repeat_of_attempt_id`; a retry is a
**new trial** linked by `retry_of_attempt_id`; derived artifacts inherit the producing attempt's trial
and are the only thing in the contract that adds artifacts without adding trials. `trial_id ==
attempt_id` is accepted, and Eval has adopted exactly that.

Why it matters: if two calls could share a trial, every per-trial count would silently depend on how
many calls happened to be filed under it.

### RI-C2 — frozen machine vocabularies

`lane` ∈ `image · general_video · native_av · lipsync · tts`.
`status` ∈ `ok · error · refusal · timeout · cancelled`.

These are machine ids, not display names, and the two near-misses that were actually in Eval's
pre-integration archive — **`refused`** (not `refusal`) and **`video`** (not `general_video`) — are
rejected by name with a message that says what to use instead. Both look harmless to a reader and
break every join that groups by them. The provider's own wording belongs in `error_detail`, verbatim,
where it is evidence rather than a status.

### RI-C3 — absence vocabulary

Canonical V1 set: `not_applicable · not_measured · instrument_unavailable · parse_failure ·
human_adjudication_pending · other`.

Two things are explicitly **not** absences:

- **A provider refusal/error/timeout.** It already has a first-class attempt row. Recording it again
  as a measurement absence double-counts it and makes the reliability picture depend on how many
  capabilities happened to be listed for the item. When a call fails there is no artifact, so there is
  nothing to have measured.
- **`instrument_unqualified`.** An unqualified instrument may still emit an observational result;
  it simply cannot create a Registry score. Emit the result with
  `instrument_qualification_ref: required_but_no_calibrated_instrument`. Turning it into an absence
  discards a real observation and understates how much was measured.

### RI-C4 — cost provenance

`cost_ref` and `evaluator_cost_ref` are **references**, not numbers. Inline numbers are rejected.
Minimal ledger entry: `ledger_entry_id`, `amount`, `currency`, `unit`, `recorded_at`, `basis`
(`provider_invoice | provider_api_response | published_price_estimate | synthetic_test`),
`immutable: true`. Synthetic tests use `basis: synthetic_test` with `synthetic: true` and **never a
fabricated real-provider cost**.

Why a reference: a number next to an attempt can be silently recomputed, rounded, or re-derived from
a price list that has since changed. **The legacy `media-factory` ledger is exactly that failure** —
July-2026 list prices hardcoded in the script, not billed amounts, and its own comment records that
it over-counted failed video attempts. Useful history; not a cost record.

## 3. Two naming collisions Resources absorbed

Both cosmetic. Accepting them makes the validator check **more**, not less — it can now read Eval's
ledger at all, and every content rule then applies to it:

| Eval emits | Contract said | Resolution |
|---|---|---|
| `cost-ledger.jsonl` | `cost_ledger.jsonl` | both accepted; canonical name unchanged |
| `cost_ref` as the entry's own id | `ledger_entry_id` | accepted as an alias — same value |

Cost-reference resolution now works end to end against Eval's real data: all **5** attempt `cost_ref`s
and all **14** measurement `evaluator_cost_ref`s resolve against their **19** ledger entries, with
generation and evaluator costs already recorded as separate entries.

## 4. Commands run, and their results

All executed in this session from a clean state (`resources/v1/build/` deleted first).

```
bash resources/v1/validators/run_all.sh                        → exit 0, ALL RESOURCES CHECKS PASSED
bash resources/v1/validators/validate_eval_archive.sh          → exit 1, 114 violations (the gate)
python3 resources/v1/validators/run_archive_negative_controls.py → 22/22 as declared
```

| Suite | Result |
|---|---|
| Requirements matrix vs YAML source of truth | 36/36 capabilities, 6/6 families, 48 rows |
| Corpus rebaseline from the committed manifest | **46 pass, 0 fail, 1 warn** |
| Views rebuild vs committed fingerprints | 9/9 byte-identical |
| Allocation leakage, clean split | exit 0 |
| `DUMMY-02` content leak / `DUMMY-03` byte-level contrast | correctly 1 / correctly 0 |
| R-C4 lineage negative controls | 4/4 as declared |
| Empirical archive, 1,000 attempts + ledger | exit 0, fan-out 6.00, 0 duplicate copies |
| **Archive negative controls** | **22/22 as declared, each failing for its declared reason** |
| **RI-C5 cross-branch gate** | **exit 1 — BLOCKED_WAITING_FOR_EVAL_INTERFACE** |

The cross-branch gate is **reported but not folded into** `run_all.sh`'s exit code. The Resources
suite verifies the Resources contract; whether Eval has yet emitted it is Eval's work, and mixing the
two would make our own suite unreadable. The gate's own exit code is what this brief records.

## 5. Required negative controls — all seven, plus the positive halves

| # | Required proof | Control | Result |
|:--:|---|---|:--:|
| 1 | two attempts sharing one trial id are rejected | `13-two-attempts-sharing-one-trial` | **PASS** |
| 2 | a repeat and a retry each get their own trial | `14-repeat-and-retry-each-get-their-own-trial` (expects **pass**) | **PASS** |
| 3 | `refused` rejected, `refusal` accepted | `15-status-refused-not-refusal` | **PASS** |
| 4 | provider failure cannot be only a measurement absence | `17-provider-failure-as-a-measurement-absence` | **PASS** |
| 5 | `instrument_unqualified` rejected as an absence | `18-instrument-unqualified-as-an-absence` | **PASS** |
| 6 | unresolvable `cost_ref` rejected | `19-cost-ref-that-does-not-resolve` (+ `20` inline number, `21` mutable entry) | **PASS** |
| 7 | the corrected Eval archive validates cleanly | `validate_eval_archive.sh` | **NOT YET — 114** |

Plus `16-lane-display-name-not-machine-id` for the other RI-C2 near-miss. Total archive suite: **22
controls, 22 as declared**, of which two are deliberately *positive* — a suite with no passing case
would be satisfied by a validator that rejects everything. The runner asserts each failure **names its
declared rule**, so a control failing for the wrong reason does not count as passing.

## 6. Unresolved items

1. **The gate itself.** Four ledger fields (`unit`, `recorded_at`, `basis`, `immutable`) on 19
   entries. Everything else in Eval's archive validates.
2. **One recommendation, not a gate.** Eval's synthetic ledger entries carry `currency: "USD"` with
   amounts like `0.01` for calls that never happened. The note disclaims it clearly, so nothing fails
   — but it reads as a real dollar figure at a glance. Consider `XTS`, the ISO code reserved for
   testing, as the Resources dummy generator uses. **Eval's call to accept or reject.**
3. **Carried forward, unchanged by this pass:** the raw 5.70 GB corpus is absent from this session and
   no media file was opened; the BSTD **351-vs-364** discrepancy remains open and uncorrected; GOV-001
   R3 (`build_reports.py` exits 0 on a degraded report) remains untouched and the script was
   deliberately not run.

## 7. Files changed

**Modified:** `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` (v2 → v2.1) ·
`resources/v1/EVAL-STORAGE-HANDOFF.md` · `resources/v1/EMPIRICAL-ARCHIVE.md` ·
`resources/v1/fixtures/empirical-archive-negative-controls/CASES.yaml` (13 → 22 cases) ·
`validators/check_empirical_archive.py`, `make_dummy_archive.py`,
`run_archive_negative_controls.py`, `run_all.sh` ·
`resources/findings/RESOURCES-V1-CORRECTION-CONTROLLER-BRIEF.md` (annotated, not rewritten)

**Added:** `resources/v1/EVAL-ARCHIVE-INTERFACE-DELTA.md` ·
`resources/v1/validators/validate_eval_archive.sh` · this brief

**Not touched:** any file under `eval/` or `canon/`. The Eval branch was read in a **detached,
throwaway worktree** and never written to.

## 8. Compliance statement

- **0** Eval or Canon files edited or written. **0** cross-stream files modified.
- **0** acquisitions, downloads, logins, forms, terms acceptances, purchases. **₹0 / $0** spent.
- **0** paid API calls. **0** media files opened from the raw corpus.
- **0** validator rules weakened to accommodate a failing archive.
- **0** persistence models added — the one canonical contract was tightened, not forked.
- **0** Canon/Eval semantic redesign: capability ids, instrument semantics and thresholds remain Eval's.
- **0** protected roles assigned. **0** later tasks started.
- **Not merged to `main`.**

## 9. Completion criteria

| Criterion | Met |
|---|:--:|
| RI-C1 trial semantics enforced, permissive prose removed | ✅ |
| RI-C2 exact lane and status vocabularies frozen | ✅ |
| RI-C3 absence vocabulary adopted; attempt failures excluded | ✅ |
| RI-C4 required fields kept; cost-ledger contract added | ✅ |
| RI-C5 corrected Eval archive validates at exit 0 | ❌ **BLOCKED** — 114 violations, ledger only |
| All seven required negative controls present and passing | ✅ (7 of 7; #7 is the gate itself) |
| Exact failing fields recorded rather than the validator weakened | ✅ |
| This brief written; committed and pushed; not merged | ✅ |
