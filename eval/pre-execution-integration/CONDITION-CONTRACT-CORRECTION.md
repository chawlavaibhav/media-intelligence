# E11-A / E11-C — Condition contract correction

**Task:** EVAL-011 · **Date:** 26 Aug 2026 · **Branch:** `work/eval-011-pre-execution-integration`
**Scope:** bounded correction. No new research, no reopened decisions.
**₹0 spend · no model/API/evaluator calls · no acquisition · no Registry rows.**

---

## 1. What was actually wrong

EVAL-009's condition contract **declared 13 condition families and always had 13**. The error was
never the architecture — it was the count written next to it. Three places said twelve, and one
derived number was wrong as a consequence.

| Where | Said | Now says |
|---|---|---|
| `CONDITION-ENVELOPE-CONTRACT.yaml` → `sweep_policy.condition_families` | `12` | `13` |
| `CONDITION-ENVELOPE-CONTRACT.yaml` → `sweep_policy.why_not_cartesian` | "12 families … 4,096 cells" | "13 families … 8,192 cells" |
| `BENCHMARK-v2-WAVE1.md` line 45 | "4 of 12 … 4,096 cells" | "4 of 13 … 8,192 cells" |
| `EVAL-009-CONTROLLER-BRIEF.md` line 134 | "4 of 12 … All 12 … 4,096 cells" | "4 of 13 … All 13 … 8,192 cells" |

**No condition family was removed to recover the old number.** That was the explicit instruction
and it is the only correction that would have been cheap and wrong: deleting a family to make the
arithmetic agree would have silently narrowed what the benchmark can distinguish.

### Why 8,192 and not 4,096

Thirteen families at two levels each is `2^13 = 8,192` cells, before any capability or any model is
considered. The old figure `4,096` is `2^12` — it was simply the same mistake propagated into
arithmetic.

**This number is not a plan.** It exists to state the size of the space we are deliberately *not*
sweeping. A full sweep was never fundable and never will be. Recording a condition costs nothing;
sweeping one costs a run.

## 2. A second inconsistency found and fixed

While checking the count mechanically, a different mismatch surfaced inside the same file.

`sweep_policy.actively_swept_in_wave1` named **four** families — `COND-LOAD`, `COND-CONSTRAINT`,
`COND-LANGUAGE`, `COND-DELIVERY` — but only **three** carried a `swept_in_wave1: true` flag.
`COND-DELIVERY` had none. A machine counting swept families got 3; the prose said 4.

`COND-DELIVERY` now carries the flag. The sweep list was right and the family record was
incomplete — duration and delivery size sit inside `COND-DELIVERY`, and the benchmark's layer-3
sweep table already swept it with 4 items and 1 extra level.

## 3. Requested-operation vocabulary — consumed from CANON-010

EVAL-009 held this vocabulary as `provisional_vocabulary` with a note saying CANON-010 owns it and
Eval would adopt whatever Canon froze.

**Canon froze it, the seven machine ids matched exactly, and nothing was renamed.**

```
generate | edit | animate | restore | extend | compose | variants
```

Source: `canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml` →
`vocabularies.requested_operation.values`, on `work/canon-010-request-freeze`.

The field is no longer provisional. It now carries `vocabulary_owner: canon`,
`eval_may_extend: false` and the exact source path, so the ownership survives a future edit.

### Vocabulary is not coverage

`BENCHMARK-v2-WAVE1.yaml` previously had a single key `requested_operations_covered: [animate,
edit, generate, variants]`. Read quickly, that says the vocabulary is four values. It is not — it
was the list of operations **layer 2 exercises**. That key is now split into three:

- `requested_operation_vocabulary` — all **7**, from CANON-010, fixed;
- `requested_operations_exercised_in_layer2` — the **4** Wave 1 actually runs;
- `requested_operations_not_yet_exercised` — `compose`, `extend`, `restore`.

Those three unexercised operations are **not** a gap in the vocabulary. They are covered by
CANON-010's request-coverage extension and become live in Stage C, where the end-to-end pool
supplies one runnable item for each.

### The provenance rule is untouched

`requested_operation` is customer intent; `workflow_mode` is the production route we chose. Both
remain required on every row, both keep their `MUST NOT be populated from` hard rules in both
directions, and the validator still enforces it.

## 4. Seed availability is now a recorded condition — E11-C

EVAL-010 established from provider-authorised SDKs that **seed availability is a property of the
route, not of the model family**. Twelve verified routes expose a seed. Seven do not — including
OpenAI's image API on both generate and edit, fal's Kling v3 text-to-video, fal's
`veo3.1/reference-to-video`, and Sarvam TTS, which offers `temperature` instead.

So `COND-WORKFLOW` gains three fields — `seed_support`, `seed_policy`, `seed_value` — with closed
vocabularies:

| `seed_support` | meaning |
|---|---|
| `exposed` | the route accepts a caller-supplied seed |
| `absent_in_api` | the provider's own generated API surface enumerates its parameters and no seed is among them |
| `undocumented` | not determinable from any provider-authorised source |

`absent_in_api` and `undocumented` are deliberately different values. Conflating "the vendor's API
has no seed" with "we could not find out" would let an evidence gap masquerade as a model property.

| `seed_policy` | what the repeat group then measures |
|---|---|
| `held` | variance **under a held seed** |
| `varied` | variance across deliberately different seeds |
| `unset` | **inherent** variance, seed unavailable or not supplied |

### The rule that follows, and why it matters

**A repeat group under `held` and one under `unset` measure different quantities. They must not be
pooled, averaged, or compared against a single threshold.**

In plain terms: on a seeded route, running the same prompt twice with the same seed asks "is this
route deterministic?". On an unseeded route, the same two runs ask "how much does this model wander
when nothing is pinned?". Both are useful. They are not the same number, and a single
repeat-consistency figure computed across both would be meaningless.

The sharpest case is the one the product most needs. **AUD-01 (Sarvam) has no seed; AUD-02
(ElevenLabs) does.** Those two slots exist precisely to be compared on Hindi and Hinglish. Their
reliability figures are not like-for-like unless one convention is chosen and applied to both.

**No threshold is invented here.** The project's provisional `0.95` repeat-consistency figure
remains unqualified, exactly as the Controller decision states. This correction says only what the
number would have to mean before it could be used, and that one convention must be declared per
comparison before Stage A runs.

### Repeats are still not retries

Unchanged and restated because the seed work sits next to it: a **repeat** is a deliberate
experimental re-run decided before any result is seen, and gets its own trial id. A **retry** is
caused by a prior failure, belongs to the acceptance and CpAO chain, and must never be pooled into
a capability pass-rate cell.

## 5. What now fails mechanically

`CONDITION-ENVELOPE-CONTRACT.yaml` carries two new machine-checkable fields:

```yaml
condition_families_count: 13
two_level_naive_cells: 8192
```

`validators/validate_integration_package.py` recomputes both from the actual `condition_families`
list and fails on any mismatch, so the count cannot drift again silently. It also fails if the
swept-family flags and the sweep list disagree, if the operation vocabulary differs from
CANON-010's, if any live file claims 12 families or 4,096 cells, and if seeded and unseeded repeat
semantics are described as interchangeable. Negative fixtures prove each check actually fires.
