# Eval V1 correction pass — Controller Brief

**Task:** `eval/tasks/EVAL-V1-CORRECTION-PASS.md` (E-C1 – E-C9)
**Date:** 26 Aug 2026 · **Branch:** `work/eval-v1-overnight` · **Not merged to `main`.**
**Predecessor:** `eval/findings/EVAL-V1-OVERNIGHT-CONTROLLER-BRIEF.md` (E1–E5), unchanged.

> ## ₹0 spent · 0 paid calls · 0 generations · 0 empirical Registry entries · 0 instruments qualified
>
> E1–E5 were **not restarted**. This was a bounded hardening pass.

---

## 1 · Status of the nine corrections

| | Correction | Status |
|---|---|---|
| **E-C1** | Separate instrument readiness from material readiness | ✅ Done |
| **E-C2** | Complete E2 only from official evidence | ⚠️ **Re-tested; still unobtainable.** Roster now enumerated row by row, all 19 unresolved |
| **E-C3** | Repair the bank without increasing generation count | ✅ Done — 20/20 critical capabilities |
| **E-C4** | Separate experimental repeat from production retry | ✅ Done + tested |
| **E-C5** | Registry row homogeneity fail-closed | ✅ Done + tested |
| **E-C6** | Remove the synthetic escape hatch | ✅ Done + regression test |
| **E-C7** | Emit the canonical Resources storage handoff | ✅ Done + tested |
| **E-C8** | Explicit uncertainty representation | ✅ Done + tested |
| **E-C9** | Keep thresholds provisional | ✅ Done — made *checkable*, not just prose |

**All 11 verification suites pass. 0 failing.**

---

## 2 · E-C1 — the conflated scalar is gone

`measurability_status` split into two **independent** fields:

| Axis | Values | Distribution |
|---|---|---|
| `instrument_readiness` | can the mechanism be trusted? | 30 `blocked_pending_qualification`, 6 `deterministic_ready` |
| `benchmark_material_readiness` | do we hold the material? | 17 missing, 10 constructed_by_eval, 5 none-needed, 3 partial, 1 held |

Plus `production_envelope_note` — **prose, not a third score** — populated on 13
capabilities where neither axis captures the caveat.

**The case that proves why this was needed.** `audio_video_synchronisation` and
`edit_preservation` have mechanisms needing no calibration *and* no material to
run on. The old scalar had to call that either "measurable now" (false — there
is nothing to measure) or "blocked on instrument" (false — the instrument is
fine). **Each misreading sends the next decision the wrong way:** one wastes
qualification effort, the other buys material we may not need yet.

**Cross-stream agreement, not coincidence.** The material axis was populated
from Resources' own 36-row classification on their correction branch. Eval and
Resources now agree **row for row**: 10 / 5 / 1 / 3 / 17 — exactly the arithmetic
R-C1 requires them to preserve. One vocabulary adapter is recorded: their
`no_external_resource` is this contract's `no_external_stimulus_required`.

**A correction inside the correction.** The new validator immediately rejected my
own first pass: I had marked `audio_video_synchronisation` `deterministic_ready`
while it sits in a model-based family. On inspection the *offset arithmetic* is
deterministic but **locating the visual onset is not** in arbitrary content. It
is now `blocked_pending_qualification` with the split envelope recorded. The
conservative reading was the correct one.

**Only 5 of 36 are ready on both axes**, and every one is operational or
deterministic — none reports fidelity or creative quality.

---

## 3 · E-C2 — still blocked, and the half-open route has closed

Re-probed after GitHub access was restored. **The policy is unchanged**, and one
thing got worse:

| Check | Result |
|---|---|
| Official provider domains probed | 22 |
| Reachable | **1** (`cloud.google.com`) |
| Yielding a pricing table | **0** |
| Its model/pricing docs | **301 → `docs.cloud.google.com`, also blocked** |
| Web search usable as price evidence | **No** — reseller blogs and calculators |

So neither a price **nor an exact model identity** could be obtained by any
available means.

**All 19 roster slots are now enumerated individually** — 4 image / 5 video /
4 native-AV / 3 lip-sync / 3 TTS, every one `unresolved`, each pointing at
blocker `E2-BLOCK-01`. A slot is a **reserved position, not a candidate**: it
names no model, because naming one from memory is the invented certainty E-C2
forbids.

**A partially filled roster remains the intended outcome.** It simply could not
be reached, because *zero* slots could be evidenced rather than some. One
official pricing page fills one slot and leaves the other eighteen untouched —
this never had to be completed in one pass.

Human verification cost remains a **separate unresolved line**; no rate is approved.

---

## 4 · E-C3 — the bank repaired without growing

`two_speaker_turn_assignment_and_lip_sync` went **7 → 10**. Both cheap repairs
were ruled out, so three atomic slots were **reallocated**:

| | Atomic | Opportunities |
|---|---|---|
| `anatomy_hands` | 3 → 2 | 39 → 38 |
| `product_identity` | 2 → 1 | 38 → 37 |
| `spatial_relationship` | 2 → 1 | 32 → 31 |
| **`two_speaker…`** | **1 → 4** | **7 → 10** |

Donors are the three capabilities with the **largest margin** that still keep an
isolation probe. **No capability lost its atomic probe** — causal isolation is
the only reason the atomic tier exists.

The four two-speaker probes sit at **distinct ladder levels** (1, 2, 4, 5) and
every one has two visible speakers, so each can actually exhibit a wrong turn
assignment. **No fake opportunity was created.**

**Invariants held:** 100 items · 40 atomic + 60 compound · 10 scenario families
× 6 · **20/20 critical capabilities ≥10** · 1,266 measurements (12.7×) · fan-out
still contract-authorised.

**Cost, recorded not hidden:** three atomic *group* counts shift by one, and
`speech_lipsync_speaker` goes 6 → 9. The runbook froze those counts "unless E1
proves a material invalidity"; E-C3 supersedes that for these three slots by
explicit direction.

**A real hole found while testing this.** The bank validator checked modality
applicability only for *compound* items, so an **atomic** probe could have
claimed a capability its modality cannot exhibit — a fake opportunity of exactly
the kind the ≥10 target must never be padded with. Atomic items are now checked
on the same footing.

---

## 5 · E-C4 — repeat and retry are now different things

| | Meaning | Decided |
|---|---|---|
| **Repeat** | deliberate re-run to estimate reproducibility | **before** the run |
| **Retry** | later attempt caused by a failure or rejection | **after** seeing a result |

Separate fields (`repeat_index` / `repeat_of_attempt_id` vs
`retry_of_attempt_id` / `retry_reason`), separate counters
(`experimental_repeats`, `production_retries` — the old combined `retries` key is
gone), and separate cost lines.

**Why it mattered.** The conflation corrupted two numbers in opposite
directions: a repeat counted as a retry inflates the apparent failure rate; a
retry counted as a repeat **hides real production cost**, because only retries
belong to the chain CpAO divides by. The previous self-test literally passed
`retry_reason="reliability_repeat"` — the bug, in the test.

`retry_chain()` follows retries only. Refusals are enforced for: an attempt that
is both, a retry with no reason, and a repeat with `repeat_index` 0.

---

## 6 · E-C5 / E-C6 — the Registry boundary

**E-C5.** `write_registry_row()` now proves the measurements are **one coherent
cell** before aggregating: capability, instrument id/version/config-hash/
qualification state, provider, model, version, endpoint, workflow, lane,
observation unit — and that they match what the *caller asked for*, not merely
each other. A self-consistent row about the wrong thing is worse than none.

Declared conditions that contradict the trials are refused. The declared
`repeats_per_item` is **not trusted** over the attempts actually present — that
is how repeats become "independent items" and confidence gets overstated. And a
**production retry may not be pooled into a pass-rate cell**: a retry exists
because something failed, so pooling it biases the pass rate upward.

Verified refusals: two models, two capabilities, two instruments, contradictory
conditions, bad repeat counts, and a retry in a pass-rate cell.

**E-C6.** `allow_synthetic` is **deleted**. `grep` confirms zero occurrences in
the harness. The regression test inspects the function signature for *any*
override-shaped parameter, greps the source, and attacks the call with multiple
shapes — all refused, registry still empty.

---

## 7 · E-C7 — one storage contract, and it is Resources'

The harness now emits the canonical **four** records and keeps **no competing
persistent manifest** (the old `artifact-manifest.jsonl` is gone):

| Record | Verified behaviour |
|---|---|
| **Attempt** | Written because the call was *made*. **2 non-ok attempts survive with no artifact** — refusal and timeout both. |
| **Artifact** | 7 artifacts, 4 derived, **3 trials** — derived frames add no trial. |
| **Measurement** | 14 records, canonical observation units only. |
| **Acceptance** | **Empty.** Eval does not decide acceptance; inventing one manufactures the numerator of CpAO. |

**Reconciliation note for Resources.** Their correction branch is visible but
`resources/v1/EVAL-STORAGE-HANDOFF.md` is not published yet, so this targets the
contract exactly as stated in E-C7 / R-C2. Two adapters will be needed against
their *current* published schema, both of which their own R-C2 already fixes:

1. their present schema **merges attempt and artifact** into one `artifact_record`; R-C2 splits them, and this emits them split;
2. their present `observation_unit` enum lists `image | sampled_clip | whole_clip | asset_set`; R-C2 mandates the canonical vocabulary, and this emits **only** canonical values.

No competing schema was chosen silently.

---

## 8 · E-C8 / E-C9 — uncertainty and thresholds

**E-C8.** Every Registry cell must now carry `uncertainty.status` of either
`computed` — with named `method`, `computed_over` (**base items or
opportunities, never trials or frames**), `n_used`, written-out `assumptions`,
and a mandatory `independence_status` — or `not_computed` with a reason from a
closed list. `not_computed` is an **expected, honest** outcome:
`deterministic_gate_no_probability_model` is correct for a zero-false-pass
count, and `descriptive_only_result` is correct for every preference-shaped
capability. When independence is `NOT ESTABLISHED`,
`is_reference_calculation_only` is true and the figure may never be quoted as a
real-world error rate.

**E-C9.** Rather than restate "these are provisional" in prose, thresholds are
now **auditable**: `THRESHOLD-REGISTER.yaml` lists all 10 judgement calls with
value, status, empirical support, and what evidence would settle each.
`validate_thresholds.py` fails if anything is `approved` without an
`approval_ref`, if a provisional threshold claims empirical backing, or if a
`deliberately_not_set` row carries a value.

**Result: 0 approved. 4 proposed. 5 deliberately not set. 1 explicitly not a
threshold at all** (the 8.68% figure, listed precisely so it is never mistaken
for a gate — the real gate is a deterministic *count*: zero false passes).

---

## 9 · Verification — all freshly executed in this session

| Suite | Result |
|---|---|
| Capability contract validator | **PASS** — 36/36, scope unchanged |
| Contract negative controls | **PASS** — 20/20 rejected |
| Threshold register validator | **PASS** — 0 approved |
| Threshold negative controls | **PASS** — 7/7 rejected |
| Cost calculator self-test | **PASS** |
| CV fixture pack verify | **PASS** — 102/102 hash-identical |
| Bank build + validate | **PASS** — 100 items, 20/20 criticals |
| Bank negative controls | **PASS** — 12/12 rejected |
| Registry schema validator | **PASS** — empty, uncertainty present |
| Registry negative controls | **PASS** — 9/9 rejected |
| Harness self-test | **PASS** — **72/72** |

**11 suites, 0 failing. 48 negative controls plus 72 harness checks.**

Nothing is claimed as a runtime PASS that was not executed. The E2
official-evidence check *was* performed — it is the one that failed to obtain
evidence, and that outcome is recorded rather than papered over.

---

## 10 · Completion criteria

| # | Criterion | Met |
|---|---|:--:|
| 1 | 36/36 separate instrument from material readiness | ✅ |
| 2 | E2 officially evidenced **or explicitly unresolved row by row** | ✅ (19/19 unresolved) |
| 3 | Bank 100 = 40 + 60, all criticals ≥10 real opportunities | ✅ |
| 4 | Repeats and retries structurally separate and tested | ✅ |
| 5 | Registry aggregation rejects mixed cells | ✅ |
| 6 | Synthetic measurements have no promotion bypass | ✅ |
| 7 | Every failed/refused call survives as an attempt record | ✅ |
| 8 | Canonical Resources contract, not a competing schema | ✅ |
| 9 | Registry schema carries uncertainty method/status | ✅ |
| 10 | All applicable validators/controls freshly run | ✅ |
| 11 | This correction brief exists | ✅ |

---

## 11 · Evidence classification

### ✅ Verified in this session
Everything in §9. Both frozen EVAL-005 human-validation hashes were re-checked
earlier and matched; the battery is untouched by this pass.

### 📐 Designed, not runtime-verified
The six family qualification protocols; Registry schema v1 (**proposed, not in
force**); the evaluator fan-out estimate (`ESTIMATE_NOT_MEASURED`); every
threshold in the register.

### 📋 Previously committed, not re-run
The 96-item validated battery; the founding checker study (**explicitly
preliminary** — 14 images from 4 independent sources, right answers never
confirmed by a first-language reader); EVAL-004's stop; the CVIT lineage
overlap.

### 🚫 Blocked by environment
**E2 official pricing and model identity** — the only blocker, re-tested and
worse than before.

### ⏭️ Later-gated, deliberately untouched
E6–E10. **EVAL-006 remains paused**, not executed, resumed or reinterpreted.

---

## 12 · What still needs you

1. **The price lookup** — one hour with ordinary web access fills the roster and produces a real budget number. Everything around it is built and tested.
2. **Rule on the 4 proposed thresholds**, or defer them explicitly. A run that adopts them silently bakes a guess into every result.
3. **ADD-01 (same-category decoys)** before the reference packs are collected — retrofitting means recollecting.
4. **Note the E-C3 group-count shift** (three groups ±1) — authorised by E-C3, recorded here rather than made silently.
5. **Resources reconciliation** — two field-name adapters, both already covered by their own R-C2.

Nothing above authorises spend, and **no instrument may be described as
qualified** on the basis of this pass.
