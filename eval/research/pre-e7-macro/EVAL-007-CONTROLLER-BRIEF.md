# EVAL-007 — Controller Brief

**Task:** `eval/tasks/EVAL-007-CLOUD-EVAL-RESEARCH-PROGRAM.md` (E7-A – E7-F)
**Date:** 26 Aug 2026 · **Branch:** `work/eval-007-capability-workflow` · **Not merged.**

> ## ₹0 spent · 0 generation calls · 0 evaluator calls · 0 Registry rows · 0 instruments qualified
> The authoritative capability contract was **not modified**. No capability was added, removed or renamed.

---

## 1 · The five findings that change our thinking

**1 · Requirements in a real brief are dependent, and our fan-out is flat.**
Arena-T2I-Hard decomposes real user prompts into a DAG where *"If a parent isn't 'yes', its
descendants are skipped and counted as failed."* Our compound items score capabilities
independently — so if the product was never rendered, `logo_wordmark_fidelity`,
`packaging_brand_colour_fidelity` and `product_stability_in_clip` can all be scored **pass**. The
asset that most completely failed the brief returns the highest score. **The inflation is largest
exactly where the output is worst.** Fixable with prerequisite edges; no new capabilities needed.

**2 · Two metrics we would plausibly have adopted are contested.**
SyncNet's LSE-C/LSE-D are *the* lip-sync standard, yet comparative work finds *"only LSE-O displays
moderate effectiveness, casting doubt on their widespread application."* DINO — the identity
standard — *"may risk overfitting the identity-irrelevant information."* Adopting either because it
is standard would have gated production on a disputed instrument. It also **independently
corroborates ADD-01 (same-category decoys)**, which we requested before finding this evidence.

**3 · We measure single assets well and asset *relationships* poorly.**
Five of the eight capabilities E7-C told me to inspect are relational — camera fidelity, state
continuity, cross-asset identity, voice consistency, campaign consistency — and all five are missing
or under-specified. Our unit coverage shows it: **13 capabilities at `frame`, 1 at `shot_pair`.**
This is the most actionable structural finding in the audit.

**4 · Evaluator drift is now a design problem.**
GenEval2's paper is titled *"Addressing Benchmark Drift in Text-to-Image Evaluation."* HPSv2 states
its own v2.0 and v2.1 scores *"can not be directly compared."* Our Registry already pins instrument
version and config hash — this is external corroboration that the pin is load-bearing, and that
refresh triggers belong in the architecture from the start.

**5 · Making an evaluator agree with humans costs about what generation costs.**
DreamBench++'s MLLM-judge upgrade reportedly costs ~20,000 calls and >$400 per model evaluated
*(indicative — needs re-verification)*. Evaluator spend is a first-order budget line, and family 3
is where it will land.

---

## 2 · Evidence classification

### SOURCE-SUPPORTED — read from a first-party repository in this session

- GenEval's seven object-focused dimensions, judged by a detector (Mask2Former).
- GenEval2's 800 prompts indexed by `atom_count`; Soft-TIFA *"less likely to drift from human-alignment over time."*
- T2I-CompBench's six categories with **deliberately heterogeneous** judges, separating 2D from 3D spatial relations.
- VBench's 16 dimensions incl. `temporal_flickering`, `motion_smoothness`, `imaging_quality`; human-preference annotation claimed per dimension.
- VBench-2.0's 18 dimensions and its stated shift from *"superficial faithfulness"* to *"intrinsic faithfulness"*; Camera Motion, Motion Order Understanding, Human Identity/Clothes, Multi-View Consistency.
- Arena-T2I-Hard: 310 real arena prompts, dependency-aware DAG checklist.
- HPSv2: same-prompt-only comparability; v2.0/v2.1 not comparable.
- IndicVoices-R: 1,704 h, 10,496 speakers, 22 Indian languages, **CC-BY-4.0**.
- TTSDS: prosody / speaker identity / intelligibility / generic / environment.
- **E7-B environment evidence:** 22 official provider domains probed, 1 reachable, 0 yielding a price.

### INFERRED — my reasoning from that evidence, not stated by any source

- The flat-fan-out inflation argument (from Arena-T2I-Hard's DAG plus our own item schema).
- That our `spatial_relationship` should split 2D from depth (from T2I-CompBench, plus our contract's own note).
- That relational capabilities are systematically under-covered (from unit distribution vs the audit).
- That families 2 and 4 are the cheapest to qualify because their truth is constructible.
- 8 of 11 condition rows — marked `inferred_*` in the map, not measured by us.

### PROPOSED — decisions for you, not made here

- Prerequisite edges on compound items *(no capability change; no new generations)*.
- A four-tier benchmark: atomic / compound / sparse condition sweeps / reserved end-to-end.
- Sweeping **4** of 11 conditions actively; recording the other 7.
- Six candidate missing capabilities — **three strong** (camera fidelity, sequence/state continuity, technical visual integrity), **two moderate**, **one overlapping**.
- Eleven capability refinements.

### UNKNOWN — and not filled in

- **Every current model identity, price, limit and feature.** Zero rows evidenced.
- Whether drift is linear in duration, or in anything.
- Whether any external metric would pass our qualification — none was run.
- The real evaluator fan-out (`ESTIMATE_NOT_MEASURED`).
- Contamination/train-test overlap in any benchmark — unassessable without the papers.
- **The entire request axis.** That is Canon's, and I did not guess it.

---

## 3 · Which current assumptions look strong, and which weak

| Strong | Weak |
|---|---|
| **Six evaluator families** — external practice routes judges per property exactly as we do | **`spatial_relationship` merges 2D and depth** — our own contract already said depth isn't box-decidable |
| **Atomic isolation** — GenEval/T2I-CompBench built the same way | **`spoken_language_correctness` merges word correctness and pronunciation** — the founding trap in a new medium |
| **Family G descriptive-only** — HPSv2's own limits prove preference can't gate | **`anatomy_hands` is named narrower than it is** — its vocabulary already covers limbs and faces |
| **Instrument version pinning** — HPSv2 says versions aren't comparable | **`multi_shot_spatial_continuity` is too narrow** — its own level-5 example assumes state continuity |
| **Devanagari exactness battery** — appears ahead of reachable public practice | **Flat measurement fan-out** — over-reports on the worst assets |
| **Generate-once** — ~11 evaluator calls per generation | **No technical-integrity capability** — 3 of VBench's 16 dimensions live in that gap |

---

## 4 · Conditions that clearly matter

**Best evidenced (recommended for active sweep):** entity count (GenEval2 indexes by it), constraint
load (Arena-T2I-Hard's prompts are hard *because* constraints stack), language/script (IndicVoices-R
exists because Indic speech needs its own material), duration (cumulative drift).

**Recorded but not swept:** shot count, reference quality, resolution/aspect, motion load, workflow
mode, input quality, campaign scale.

**Two structural notes.** 11 conditions at two levels is 2,048 cells before a model is considered —
a cartesian product is not fundable and never will be. And **workflow mode sits on the
condition/Planner line**: when *we* choose I2V it is a Planner decision; when the customer supplies
a starting image it is a condition. The same field means different things depending on who chose it.

---

## 5 · What remains unresolved

1. **E7-B in full** — 22 candidates probed, 0 evidenced. Blocks only the cost forecast's price cells.
2. **Request axis** — Canon's, deliberately untouched.
3. **Three literature gaps** — no benchmark found for brand-mark fidelity under perspective, campaign/variant consistency, or exact spoken-script fidelity in code-mixed speech. If we want them, **we build the instrument**.
4. **Two evidence rows need re-verification** before informing a budget or a gate: the DreamBench++ cost figure and the SyncNet comparative ranking. Both came from search summaries, not first-party pages.
5. **arxiv, HuggingFace, OpenReview blocked** — no peer-reviewed paper was read. Every row is a README, which states what authors *claim*, not what a method section establishes.

---

## 6 · What you must decide at integration

| # | Decision | Cost if deferred |
|---|---|---|
| 1 | **Adopt prerequisite edges?** | Every compound score stays inflated on exactly the worst assets. *No capability change, no new generations — the cheapest high-value fix here.* |
| 2 | **Split `spatial_relationship` into 2D and depth?** | One capability keeps carrying two judgements with different instruments |
| 3 | **Split word correctness from pronunciation?** | A robust ASR keeps hiding mispronunciations |
| 4 | **Adopt any of the 3 strong missing capabilities?** | Camera fidelity, state continuity and technical integrity stay unmeasured while models are marketed on them |
| 5 | **Approve E7-B's completion elsewhere** | No budget number is possible |
| 6 | **Confirm Eval must not author the request axis** | Risk of re-running the failure this reset corrected |

**Recommended order:** #1 first (cheap, structural, no scope change), then #3 and #2 (both are
splits of things we already measure), then #4 after Canon's request evidence lands — because whether
camera fidelity matters depends on whether customers ask for camera moves, and that is not my
question to answer.

---

## 7 · Verification

| Check | Result |
|---|---|
| Research-output validator | **PASS** — 9/9 deliverables, 36/36 capabilities, 0 endpoints admitted |
| Provisional forecast self-test | **PASS** — counts correct; refuses to total a partial forecast |
| Negative control on the validator | **PASS** — a deliberately inserted over-claim was caught |
| Capability contract modified | **No** |
| Another stream's files edited | **No** |

*One defect found and fixed in my own tooling: the over-claim check initially matched
"instrument is qualified" inside the negation "**No** instrument is qualified", flagging exactly the
documents being careful. It now reads the sentence, and was negative-controlled to confirm it still
catches a real assertion.*
