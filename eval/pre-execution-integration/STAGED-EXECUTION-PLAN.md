# E11-E — Staged execution plan, in plain English

**Task:** EVAL-011 · **Date:** 26 Aug 2026
**Machine-readable record:** `STAGED-EXECUTION-PLAN.yaml`
**Nothing here authorises spend. ₹0 · no model/API/evaluator calls · no acquisition.**

---

## The correction this makes

EVAL-009 produced a number — **494 generations, 5,515 evaluator calls, 188 human review units** —
and that number started being read as "the first run".

It is not. It is the **full design ceiling** for Layers 1–3: what it would cost if every slot ran
its entire item set. A complete design is not automatically a sensible first bill.

This plan splits the work into four stages, so the Controller can authorise the smallest useful
experiment instead of the whole design.

| Stage | What it buys | Model generations |
|---|---|---:|
| **Q** — qualification | trustworthy instruments | **0** |
| **A** — admission screen | which routes deserve deeper spend | **90** |
| **B** — deeper benchmark | capability + condition envelopes, survivors only | **≤ 404** |
| **C** — end-to-end | accepted outcomes and the only real CpAO | 32 outcome attempts; generations formula-only |

`90 + 404 = 494`. The staging does not invent or lose a single generation — it decides *when* they
are spent and *whether* the later ones are spent at all.

## Stage Q — qualify the instruments first, at zero generation cost

**The project has never run a checker.** Every capability number is meaningless until the thing
producing it has been qualified. So Stage Q comes first.

**It needs zero model generations.** That is a design result, not a deferral: all seven evaluator
families can be qualified against material whose truth is known by construction or by capture. The
principle the task set — no generation spend merely to qualify an evaluator — turns out to cost
nothing to honour.

**Three families can be qualified with material already in the repository:**

- **Deterministic CV geometry** — the `cv-geometry` fixture pack, **102 items** (100 scoreable + 2
  negative controls), truth constructed by code, **zero human labels**. Unblocks 5 capabilities.
  Runnable today.
- **Devanagari OCR** — the frozen **96-item** exactness battery, labels known by construction.
  Unblocks the highest-value question on the roster. One caveat: the built items are git-ignored
  and the pinned font is not committed, so a fresh clone cannot rebuild it. That is a rebuild risk,
  not an acquisition cost.
- **Operational logging** — deterministic from run records, no material at all.

**One more can be built by Eval without any new Resources pack:** a Latin exact-text set, rendered
from known strings exactly as the Devanagari battery was. It must not mutate the frozen battery.

**The cheapest large unblock is the temporal family.** Nine capabilities unblock from **12 clean
clips**, because the truth is *injected* — a known freeze, a known identity swap, a known flip — so
no annotator is needed. Twelve clips, zero human labels, nine capabilities.

**Four families are genuinely blocked on Resources material.** The largest is the structured visual
VLM family: 12 capabilities, needing person and product references **with same-category decoys**.
The decoys are not optional. A known-non-match only means something against a plausible confusion —
an identity checker that can tell a shoe from a kettle has demonstrated nothing. A decoy-free
subset is not a cheaper version of this experiment; it is a different and useless one.

## Stage A — the admission screen, 90 generations

**One question per slot: does this route deserve deeper spend?**

Each slot runs only its **comparability core** — the shared items every slot in its lane runs —
at **full repeats of 2**. Image and video slots have a 4-item core, so 8 generations each; audio
slots have 3, so 6 each. Twelve core slots, **90 generations**, about 18% of the design ceiling.

**Repeats were deliberately not halved.** The Controller's instruction was explicit, and it is
sound: halving repeats to save money destroys the reliability evidence that is half the point of
running twice. Stage A saves by **deferring item breadth**, not by weakening the design.

**Before it runs, each slot must declare its seed policy.** Three eligible slots have no seed on
their verified route. Their repeats measure inherent variance; other slots can measure held-seed
repeatability. Those are different quantities and cannot share a threshold.

**What Stage A may report:** trial cost, reliability under a declared seed policy, latency, error
and refusal rates, and cost per benchmark pass.

**What it may not report: customer-outcome CpAO.** There are no accepted customer outcomes at this
stage, so the denominator does not exist.

## Stage B — deeper benchmark, survivors only, ≤ 404

Atomic and compound capability items plus sparse adaptive sweeps across **4 of the 13** condition
families. The naive two-level product of all 13 would be **8,192 cells**; that is the size of the
space we are deliberately not sweeping.

**The maximum is 404** — the design ceiling minus what Stage A already spent. The *expected* figure
is deliberately **null**, because it depends on how many slots survive Stage A, and we do not have
that result. The per-slot remainder table is published instead, so any survivor set can be summed
exactly the moment Stage A returns.

**No pass-rate saving is claimed.** Asserting an expected survivor count would be inventing
evidence, and the validator fails the package if anyone later fills that field in.

## Stage C — end-to-end outcomes, and the only place CpAO exists

This is where the VID-05 correction lands.

**Layers 1–3 cannot compute CpAO.** They produce no accepted customer outcomes, so there is no
denominator. VID-05 — the cost-knee question — may run generations in Stage A and B and report
trial cost and reliability there. **Its premium-versus-fast accepted-outcome verdict is a Stage C
output and may not be stated earlier.** Reporting cost-per-benchmark-pass as though it were CpAO is
the exact relabelling this correction forbids.

**Eval does not author customer briefs.** The Stage C pool is CANON-010's: the 30-item brief bank
plus the 10 runnable request-coverage items, 40 in total. RX-11 is representation-only and is
excluded.

Eight slots are reserved, and the selection rule **L4-SELECT-v1** is deterministic: cover all seven
requested-operation values, allocate the eighth slot to `generate` (the only operation with 30
candidates), and within an operation prefer Hindi, then Hinglish, then English, tie-breaking on
ascending id. Language is prioritised because Stage C is where a language failure stops being a
capability score and becomes a rejected outcome.

**The final ids are the Controller's to integrate.** The rule and its derived candidates are shown
so the choice is reproducible, not so Eval can make it.

**Outcome attempts are exact: 8 briefs × 2 recipes × 2 repeats = 32.** The *generation* count is
formula-only, because one outcome can consume many generations — a dialogue video may need an
image, a video, a TTS pass and a lip-sync transform — and the recipe depends on a Planner that does
not exist. Putting a number there would be inventing the Planner's behaviour.

## What a first authorisation could reasonably look like

**Stage Q + Stage A: zero generations to qualify the instruments, then 90 generations to decide
which routes deserve more.** That is 18% of the design ceiling, and it reduces scope by deferring
whole questions rather than by weakening any of them.

It is not costable yet — see `PRICE-READY-STAGED-FORECAST.yaml`. Eleven of the twelve Stage A slots
have no verified generation price, and no evaluator unit price is verified at all, which blocks
even Stage Q's total despite its generation line being a genuine zero.

## What this plan does not do

It does not authorise spend. It does not choose Stage C's final request ids. It does not claim a
Stage B survivor count. It does not invent a repeat-consistency threshold. And it does not treat
RES-004's 173 person-hour full-acquisition estimate as a prerequisite to anything — that figure is
a complete provisional plan under one sizing assumption, not a gate on the first paid model call.
