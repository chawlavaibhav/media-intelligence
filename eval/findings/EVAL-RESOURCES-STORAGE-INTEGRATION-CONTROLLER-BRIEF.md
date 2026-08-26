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
