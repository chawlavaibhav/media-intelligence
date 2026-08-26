# Eval ↔ Resources storage integration — Controller Brief

**Task:** `eval/tasks/EVAL-RESOURCES-STORAGE-INTEGRATION-PASS.md` (EI-C1 – EI-C8)
**Date:** 26 Aug 2026 · **Branch:** `work/eval-v1-overnight` · **Not merged to `main`.**
**Predecessors:** overnight brief (E1–E5) and correction brief (E-C1–E-C9), both unchanged.

> ## ₹0 spent · 0 paid calls · 0 generations · 0 empirical Registry entries · 0 instruments qualified

---

## 1 · The completion gate, up front

> **Eval dummy generation → canonical JSONL handoff → Resources `check_empirical_archive.py` → exit 0.**

```
$ bash eval/v1/harness/run_cross_branch_validation.sh
Resources ref   : origin/work/resources-v1-overnight
Resources SHA   : e974c813b6550c1dee1c1794b9c2da65481587e8
Schema version  : version: v2
Validator sha256: b6dda9239fab12cb…

attempts:              5
  ok:                  3
  failed/refused:      2  (each preserved individually with its reason)
artifacts:             7
  derived:             4  (inherit parent trial/attempt; never independent trials)
measurements:          14
acceptances:           0
distinct output hashes: 7
duplicate media copies: 0
MEAN MEASUREMENTS PER ARTIFACT: 7.00  (min 1 / max 13)
capability ids covered: 13
observation units used: ['frame']

[PASS] every failed/refused attempt is preserved individually with its reason
[PASS] status 'ok' <=> exactly one artifact; any other status <=> none
[PASS] repeats and retries are distinct; no repeat appears in a retry chain
[PASS] observation units use the canonical vocabulary verbatim
[PASS] derived artifacts inherit their parent's trial and attempt
[PASS] no output is stored more than once
[PASS] every attempt carries a cost reference
[PASS] fan-out 7.00 measurements per artifact — one generation, many measurements

RESULT: PASS — Eval's emission satisfies the Resources v2 contract (exit 0)
```

**The validator is invoked from a worktree of the Resources branch, never copied
into Eval.** A local copy would drift, and Eval would then be proving compliance
against a stale snapshot of somebody else's contract.

---

## 2 · Status of the eight corrections

| | Correction | Status |
|---|---|---|
| **EI-C1** | Conform exactly to Resources v2 | ✅ Validated cross-branch |
| **EI-C2** | Trial semantics: one call = one trial | ✅ `trial_id == attempt_id`, 1:1 by construction |
| **EI-C3** | Required attempt provenance | ✅ incl. `prompt_hash`, `cost_ref`, canonical status, lane ids |
| **EI-C4** | Artifact fields | ✅ incl. `media_kind`, `output_bytes`, derivation contract |
| **EI-C5** | Flat measurement fields + absence semantics | ✅ |
| **EI-C6** | Fix operational cost accounting | ✅ + regression with a costed refusal |
| **EI-C7** | Tighten Registry repeat/measurement structure | ✅ 4 required controls + 1 guard |
| **EI-C8** | Cross-branch validation | ✅ **exit 0** |

**11 Eval suites + the cross-branch gate. 0 failing.** Harness self-test **95/95**.

---

## 3 · EI-C2 — the trial moved, and that was the point

The trial used to be the root **asset**. So a call that produced nothing had **no
trial at all** — a refusal silently left the denominator. Reliability and cost
both then read better than reality, in exactly the cases where they should read
worse.

The trial is now the **call**. `trial_id == attempt_id`, so the one-to-one
mapping is true by construction rather than asserted. Every repeat and every
retry is its own trial; derived media inherits its parent's trial *and* attempt
and never becomes an independent one.

**One divergence from Resources' example, deliberate and compatible.** Their
committed baseline fixture shares a trial across a repeat (`A-OK` and
`A-REFUSED` both on `T1`). EI-C2 mandates the stricter rule — a repeat gets its
own trial — and their validator accepts both, since it only enforces that an
artifact's trial matches its attempt's. Worth them knowing the streams differ in
strictness here even though nothing breaks.

---

## 4 · EI-C5 — two things were *removed*, and the removals are the correction

`generation_failed` and `refused` are gone from the absence vocabulary. A
provider refusal, error or timeout is a property of the **attempt** and lives on
the attempt row with its verbatim `error_detail`. Recording it again as a
measurement absence double-counted one fact and made a failed *call* look like a
failed *measurement*. The harness now **refuses** to measure a failed attempt.

`instrument_unqualified` is gone too, and this one is subtler. An unqualified
instrument still **saw** the artifact and produced a real observation. That
observation is evidence and must be stored — it simply may not be reported as a
capability score. So the result is stored normally carrying
`instrument_qualification_ref: required_but_no_calibrated_instrument`, and the
Registry boundary keeps it out of scores. Calling it an absence would have
thrown away a genuine observation.

---

## 5 · EI-C6 — the cost bug, and why the test was blind to it

`operational_metrics()` summed generation cost over **produced artifacts**. Every
refused, errored and timed-out call therefore contributed **zero** — understating
cost precisely where reliability is worst, which is the worst place to
understate it.

Totals are now computed over **attempts**. Verified with a costed failure:

| | |
|---|---:|
| 1 ok call | 1.00 |
| 1 refusal | 0.75 |
| 1 error | 0.50 |
| **Total (correct)** | **2.25** |
| Old artifact-based total | 1.00 |

**The self-test could not have caught this before**, because the dummy failure
adapters hardcoded `cost_generation: 0.0`. The bug and the test were blind in
the same place. The adapters now charge `unit_price` on failure, which is also
the truthful behaviour — a refused call still consumes latency and may still be
billed.

`cost_in_retry_chains` is **renamed**, because it claimed more than it computed:
it summed only the retry attempts, not the originating attempt, so it was never
a chain cost and could never have become CpAO. It is now
`cost_of_retry_attempts`, with `complete_retry_chain_cost: null` and
`cpao_computable: false` — **no acceptance exists**, so no complete chain cost is
claimed. `accepted_chain_cost()` provides the correct calculation for when one
does.

---

## 6 · EI-C7 — and a bug it exposed in my own earlier work

Four required controls, all passing:

| Control | Refused because |
|---|---|
| declared 2 repeats, 1 observed | observed trial structure ≠ declared |
| two measurements of one trial | one trial is one observation |
| one item with fewer repeats than another | per-item structure must be uniform |
| a retry inside the repeat cell | a retry exists because something failed |

Repeat counts are **derived from provenance**, never trusted from the caller.
`observed_max <= declared` was too weak: declaring 2 repeats while observing 1
passed silently, and the row then claimed a structure it did not have.

**The bug this surfaced.** My E-C5 homogeneity work included `config_hash` as a
cell key. But a Registry cell aggregates over **many base items**, each with its
own prompt and therefore its own config hash — so **no multi-item cell could ever
have been written**. It only appeared once EI-C7 forced multi-item cells to be
built. `config_hash` is out; the **instrument** config hash still must match,
because the evaluator has to be identical even though the prompts are not.

The balance invariant (`trials == n_items × repeats_per_item`) is retained as a
belt-and-braces guard and documented as such — given the per-item and duplicate
checks it is not independently reachable, and the brief says so rather than
implying a fifth independent control.

---

## 7 · Answers to Resources' three open items

They asked; these are Eval's answers.

1. **Lane vocabulary — confirmed.** `image | general_video | native_av | lipsync | tts`. The harness **rejects** any other value at generation time, so a local synonym cannot reach persistence.
2. **`absence_reason` coverage.** Eval emits the EI-C5 set: `not_applicable | not_measured | instrument_unavailable | parse_failure | human_adjudication_pending | other`. **One-word discrepancy to reconcile:** their handoff doc lists five and omits `not_measured`; EI-C5 includes it. Their validator does not enforce the vocabulary, so nothing breaks either way — but the docs should agree. `not_measured` earns its place: *applicable, simply not run this time* is a real and common state, distinct from *no instrument existed*.
3. **Byte budget.** Every artifact now carries `output_bytes`, so the forecast becomes a sum the moment E2 lands. It still cannot be forecast now, for the same reason E2 is blocked.

---

## 8 · Verification — all freshly executed

| Suite | Result |
|---|---|
| Capability contract validator | **PASS** 36/36 |
| Contract negative controls | **PASS** 20/20 |
| Threshold register + controls | **PASS** 0 approved, 7/7 |
| Cost calculator self-test | **PASS** |
| CV fixture pack verify | **PASS** 102/102 |
| Bank build + validate | **PASS** 100 items, 20/20 criticals |
| Bank negative controls | **PASS** 12/12 |
| Registry schema + controls | **PASS** empty, 9/9 |
| Harness self-test | **PASS** **95/95** |
| **Resources cross-branch validator** | **PASS — exit 0** |

Commands are in §1 and in `eval/v1/harness/VERIFICATION-LOG.md`. Nothing is
claimed as a runtime PASS that was not executed.

---

## 9 · E2 remains separate and still blocked

Unchanged and explicitly out of scope for this pass. No model id or price was
invented. All 19 roster slots remain enumerated as unresolved. **The storage
contract is merge-ready without E2** — that was the point of separating them.

---

## 10 · What still needs you

1. **The E2 price lookup** — unchanged, one hour with ordinary web access.
2. **The `not_measured` reconciliation** with Resources (§7.2) — a one-word docs alignment, no code impact.
3. **Note the trial-strictness divergence** (§3) so both streams know Eval is stricter than the Resources example.
4. **Rule on the 4 proposed thresholds**, or defer explicitly.
5. **ADD-01 same-category decoys** before reference packs are collected.

Nothing here authorises spend, and **no instrument may be described as
qualified**.

---

# Final v2.1 ledger closure

**Task:** `eval/tasks/EVAL-RESOURCES-LEDGER-MICROFIX.md` · **Date:** 26 Aug 2026
**₹0 spent · 0 paid calls · 0 Registry entries · 0 instruments qualified · not merged.**

## What this was

A **branch-order race, not a new defect.** Eval `adac747` validated cleanly against Resources
`e974c81` (schema v2). Resources then tightened the cost-ledger contract in `db54e97` (schema
**v2.1**) and re-validated Eval's existing archive against the newer rules.

All four core entity files — attempts, artifacts, measurements, acceptances — still validated
cleanly. Every remaining violation was in the synthetic cost ledger.

## SHAs

| | |
|---|---|
| Previous Eval SHA | `adac747` |
| Resources SHA validated against | `db54e972a8a0d593e3c3455f630641906e7a58f6` |
| Resources schema version | **v2.1** |
| Required minimum | `db54e972a8a0d593e3c3455f630641906e7a58f6` ✅ met exactly |

## RED — test written first, and it failed for the predicted reason

The self-test was extended **before** `_ledger_line()` was touched, asserting the v2.1 minimum
ledger contract. It failed, and the failure reproduced Resources' arithmetic exactly:

```text
DEMO 8 — cost ledger satisfies the Resources v2.1 minimum contract
  [PASS] cost ledger file is emitted
  [PASS] cost ledger is non-empty                     19 entries
  [FAIL] every ledger entry carries the v2.1 required fields
         19 entries; missing counts: {'unit': 19, 'recorded_at': 19,
                                      'basis': 19, 'immutable': 19}
  [FAIL] synthetic entries declare basis 'synthetic_test'
         19 entries with basis ['None']
  [FAIL] synthetic entries declare synthetic: true     19 entries not marked synthetic
  [FAIL] every ledger entry declares immutable: true   19 entries not marked immutable
  ...
RESULT: 103/107 checks passed        (exit 1)
```

**4 failing checks over 19 entries → 4 missing fields + 2 consequent invalidities = Resources'
reported 19 × 6 = 114 violations.** The RED test reproduced their count independently before any
fix was written, which is the point of writing it first.

## GREEN — the minimal change

One function, `_ledger_line()` in `eval/v1/harness/harness.py`:

```python
"unit": "call",
"recorded_at": self._synthetic_timestamp(),   # deterministic ISO-8601 UTC
"basis": "synthetic_test",
"synthetic": True,
"immutable": True,
```

plus a small `_synthetic_timestamp()` helper: a **fixed base date plus the harness clock tick**.
Never wall-clock — the handoff must stay byte-identical across runs, and a real timestamp would put
nondeterministic drift into the very file whose reproducibility is under test. **Confirmed
byte-stable across consecutive runs.**

The existing disclaimer is unchanged and now sits in contract-named fields rather than only in prose:
`basis: synthetic_test`, `synthetic: true`, `source: SYNTHETIC_SELFTEST_LEDGER`, and the note
*"Fabricated for harness self-tests. NOT a provider price. No real rate has been obtained — see
E2-BLOCK-01."* **No real-provider cost source was invented.**

Nothing else was touched. Attempts, artifacts, measurements and acceptances were already conformant
and were not modified.

## Self-test result

```text
python3 eval/v1/harness/run_selftest.py
RESULT: 107/107 checks passed        (exit 0)
```

## Cross-branch gate — the completion criterion

```text
bash eval/v1/harness/run_cross_branch_validation.sh

cost-ledger entries:   19
trials:                5  (one call = one trial)

[PASS] one call = one trial: every attempt_id maps to a unique trial_id
[PASS] lane and status use the frozen machine vocabularies
[PASS] every cost_ref resolves to an immutable cost-ledger entry
[PASS] no provider failure is laundered into a measurement absence
[PASS] every failed/refused attempt is preserved individually with its reason
[PASS] status 'ok' <=> exactly one artifact; any other status <=> none
[PASS] repeats and retries are distinct; no repeat appears in a retry chain
[PASS] observation units use the canonical vocabulary verbatim
[PASS] derived artifacts inherit their parent's trial and attempt
[PASS] no output is stored more than once
[PASS] every attempt carries a cost reference
[PASS] fan-out 7.00 measurements per artifact

check_empirical_archive.py EXIT = 0
```

**Violations by category, counted from the validator's own output:**

| Category | Violations |
|---|---:|
| attempts | **0** |
| artifacts | **0** |
| measurements | **0** |
| acceptances | **0** |
| cost ledger | **0** |
| **Total `[FAIL]` lines** | **0** |

The validator was invoked from a detached worktree of the Resources branch. It was **not copied into
Eval and not weakened**.

## All prior suites re-run

11 Eval suites, **0 failing**: capability contract (36/36) and its 20 controls; threshold register
(0 approved) and its 7 controls; cost calculator self-test; CV fixture pack (102/102); bank (100
items, 20/20 criticals) and its 12 controls; Registry schema and its 9 controls; harness self-test
(107/107).

## One recommendation put back to you

Resources noted — as a **suggestion, not a gate** — that synthetic entries carrying
`currency: "USD"` with amounts like `0.01` "read as a real dollar figure at a glance", and
suggested the ISO test code `XTS`.

**I left currency unchanged**, because the micro-fix task states `USD` is not a merge blocker and
directs switching to `XTS` only if already supported by the self-test — it is not; currency was
previously unasserted — and not to broaden the task.

**My recommendation is to accept it later.** The disclaimer would then live in the data rather than
beside it, which is the same principle that motivated `basis` and `immutable`. It is a one-line
change plus a self-test assertion, and it belongs in whichever pass next touches the ledger — not
smuggled into a micro-fix.

## Final state

| | |
|---|---|
| Eval commit | `d48d46c` |
| Branch | `work/eval-v1-overnight` — **not merged** |
| Cross-branch gate | **exit 0**, zero violations in all five categories |
| Spend | ₹0 · 0 paid calls · 0 Registry entries · 0 instruments qualified |
