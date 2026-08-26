# EVAL-011 — Controller Brief

**Task:** EVAL-011 — Pre-Execution Integration Correction
**Date:** 26 Aug 2026 · **Autonomy:** autonomous · **Branch:** `work/eval-011-pre-execution-integration`

**Status: COMPLETE.** One bounded correction pass, as scoped. No new research round.
**₹0 spend · 0 model/API calls · 0 evaluator calls · no acquisition · no accounts · no Registry rows · no merge.**

> **Communication check:** I will explain technical ideas in plain English, including what they
> mean, why they matter, and their practical consequence; use minimum sufficient wording without
> sacrificing understandability; separate evidence from inference; and never invent facts.
> I have read `shared/COMMUNICATION-STANDARD.md`.

---

## 1. What was corrected

Four things were wrong or ambiguous across the four freeze branches. All four are now fixed and
mechanically enforced.

**The condition count.** EVAL-009's contract always declared **13** families; three places said 12
and one derived figure said 4,096. It now says **13 families / 8,192 two-level cells** everywhere.
**No family was removed to recover the old number** — that was the cheap wrong fix and it was
refused. A second, separate inconsistency surfaced while checking: the sweep policy named four
swept families but only three carried the flag. `COND-DELIVERY` now carries it.

**The operation vocabulary.** EVAL-009 held it as *provisional pending CANON-010*. Canon froze it;
the seven machine ids matched exactly, so nothing was renamed. The field now records
`vocabulary_owner: canon` and `eval_may_extend: false`. The benchmark's single ambiguous key
`requested_operations_covered: [4 values]` — which read as though the vocabulary itself were four
values — is split into **vocabulary (7, fixed)**, **exercised in layer 2 (4)**, and **not yet
exercised (`compose`, `extend`, `restore`)**. Those three are not a gap; they become live in Stage C.

**The CpAO contradiction.** VID-05 asked about accepted outcomes while the same package said
Layers 1–3 cannot compute CpAO. Both are now true and staged: Layers 1–3 may report trial cost,
reliability, latency, errors, refusals and cost-per-benchmark-pass, and are **forbidden** from
reporting customer-outcome CpAO. VID-05's cost-knee **conclusion** executes in Stage C only.

**Reproducibility semantics.** Seed availability is now a recorded production condition on
`COND-WORKFLOW`, with `absent_in_api` and `undocumented` kept as *different* values so an evidence
gap cannot masquerade as a model property. A repeat group under a held seed and one with no seed
measure different quantities and **may not be pooled, averaged, or compared against one threshold**.
No new threshold was invented; the provisional `0.95` remains unqualified exactly as your decision
states.

## 2. The staged answer

`494` was being read as the first paid run. It is the **full Layers-1–3 design ceiling**.

| Stage | Purpose | Model generations | Class |
|---|---|---:|---|
| **Q** | qualify instruments | **0** | first-tranche candidate |
| **A** | admission screen, 12 core slots | **90** | first-tranche candidate |
| **B** | deeper capability + sparse envelope, survivors only | **≤ 404** | adaptive/conditional |
| **C** | end-to-end outcomes and CpAO | 32 outcome attempts | attempts exact; generations formula-only |

`90 + 404 = 494`. Nothing was invented or lost — the staging decides *when* generations are spent
and whether the later ones are spent at all.

**Stage Q costs zero generations, and that is a result rather than a deferral.** All seven evaluator
families can be qualified from constructed or captured truth. Three can be qualified from material
already in the repository: the **102-item** CV-geometry pack, the frozen **96-item** Devanagari
battery, and operational logging. A Latin exact-text set can be built by Eval with no new Resources
pack. And the cheapest large unblock in the whole programme is the temporal family — **nine
capabilities from twelve clean clips with zero human labels**, because the defect is injected and
therefore known by construction.

**Stage A keeps repeats at 2.** Your instruction was explicit and it was followed: scope was reduced
by deferring item breadth, never by halving repeats.

**Stage B publishes a maximum and refuses to publish an expectation.** The expected figure depends
on a Stage A survivor set we do not have; the per-slot remainder table lets any survivor subset be
summed exactly once it exists. Claiming a pass-rate saving would be inventing evidence, and the
validator now fails the package if anyone fills that field in.

## 3. Slots against supply — 12 of 14 resolved, 0 deleted

Twelve of fourteen slots now have an exact version verified from a provider-authorised source. Two
do not: **IMG-04** (fal carries Seedream v5/**lite**, not v5/**pro**) and **AUD-03** (fal's highest
lip-sync is `sync-lipsync/v2/pro`, not Sync-3). **Both slots were retained and no sibling was
substituted.** One slot — **VID-05** — is fully execution-ready.

Three supply findings change *how* slots run, not *whether* they run:

- **AUD-02 must run direct.** fal's ElevenLabs wrapper omits `seed`, the pronunciation-dictionary
  locators and the previous/next-text continuity controls. The pronunciation dictionary is the
  mechanism the AUD-01 vs AUD-02 comparison turns on, so a fal measurement cannot test it.
- **AUD-01 and AUD-02 are not like-for-like yet.** ElevenLabs has a seed; Sarvam has `temperature`
  and none. One convention must be chosen before Stage A, or the most product-relevant comparison
  on the roster yields two numbers that cannot sit beside each other.
- **One EVAL-009 open question closed:** Veo 3.1 *does* expose first/last-frame and extend controls
  — Google's own SDK carries `last_frame`, typed reference images and four video mask modes.

**One finding is uncomfortable and is reported rather than acted on.** The only image model with a
fully verified price — Nano Banana 2 at $0.067 per generated 1K image — is **not on the roster**. It
genuinely answers IMG-01's question, so it is recorded as an equivalent candidate. **It was not
added**, because adding a model on the grounds that it is the one we can price is exactly the
substitution the independence rule exists to prevent.

## 4. Price readiness — 0 of 4 stages complete

No stage can be totalled. The blockers, in order of how much they unblock:

1. **Evaluator unit prices.** EVAL-010 verified none, and several instruments are themselves model
   APIs. This blocks every stage — including Stage Q, whose generation line is a genuine zero but
   whose total is still unknown.
2. **Generation prices for 11 of 12 Stage A slots.**
3. **Frontier Clouds identity** — still unresolved, still not guessed. Nominal cost can be frozen
   without it; **cash outlay after credits cannot**, and the two are kept strictly apart.
4. **HED-1** — which human review time counts as *required* in fully-loaded CpAO.

Exactly one line is priced: Stage A / VID-05, `8 × USD 0.05 = USD 0.40` on the Google Cloud 720p
video+audio count route. Your two price clarifications are applied and guarded by the validator:
Nano Banana 2's figure means **per one generated 1K-resolution image, not per thousand images**, and
Veo 3.1 Lite's `$0.05` is **that route's** 720p video+audio count price and is not generalised to
fal's or Runway's Veo routes.

## 5. Verification

Two validators run clean, and the new one is proven rather than assumed.

- `validators/validate_integration_package.py` — **13 gates, all pass.** It recomputes the family
  count and cell count from the contract itself, so the 12/13 drift cannot return silently.
- `validators/test_negative_fixtures.py` — **16 negative fixtures, all caught.** Each breaks exactly
  one gate. Among them: declaring 12 families, restoring 4,096, *deleting a family to recover the
  old count*, drifting the operation vocabulary, collapsing the customer/planner provenance line,
  letting Stage A claim CpAO, staging VID-05's CpAO early, pooling seeded with unseeded repeats,
  deleting a slot for sourcing reasons, substituting a sibling, totalling a partial stage, guessing
  cash outlay, making the 173 hours mandatory, breaking the count reconciliation, spending
  generations in Stage Q, and inventing a pass-rate saving.
- The V1 immutability gate was **live-fire tested**: a tampered `eval/v1/capability-contract.yaml`
  was detected, then reverted. V1 artifacts are byte-identical.
- EVAL-009's own validator still passes all 10 of its gates after the corrections, and the
  regenerated forecast still produces 494 / 5,515 / 188 — the ceiling is unchanged, only relabelled.

The original EVAL-009 branch is untouched; corrections live here.

## 6. Decisions still needed before Governor review

None of these blocks the coherence review itself; all block a priced tranche.

| id | Decision | Why it matters |
|---|---|---|
| **SUP-3** | Which seed convention governs the Indic voice comparison? | **Must be settled before Stage A runs**, or AUD-01 vs AUD-02 is not like-for-like |
| **SUP-2** | IMG-04 and AUD-03: accept a documented version difference, defer, or wait for catalogue access? | Two retained slots cannot execute until this is answered |
| **SUP-1** | Recraft v3 as named, or v4 where `text-to-vector` is first-class? | The slot exists *because of* vector output |
| **SUP-4** | Add Nano Banana 2 to IMG-01? | It is the only priced image model; adding it is a scope call, not a sourcing one |
| **HED-1** | Which human review time is *required* in fully-loaded CpAO? | Blocks every Stage C cost figure |
| **L4 ids** | Integrate rule L4-SELECT-v1 into final Stage C request ids | Eval produced the deterministic rule; Eval must not choose the briefs |
| **R multiplier** | Whether a pack must both calibrate and qualify | RES-004 flags this as the largest cost lever; staged acquisition may satisfy independence more cheaply than doubling |

## 7. What remains true and unchanged

No model is qualified. **No instrument has ever been run.** No Capability Registry row exists. No
budget is approved. The 173 person-hour acquisition estimate is not a prerequisite to anything, and
this task treated it as what it is — a full provisional plan under one sizing assumption.

Knowing exactly what to call, in what version, under what conditions, and in what order to spend,
still is not the same as being able to measure. Stage Q is where that changes, and it is the only
stage that can start with material the project already holds.
