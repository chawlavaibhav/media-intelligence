# EVAL-003 — Devanagari calibration readiness findings

**Date:** 24 Aug 2026 · **Status:** readiness complete, not yet run  
**API/model spend:** ₹0 / $0 · **Human specialist time:** 0 hours · **Generators run:** 0 · **Capability results written:** 0

This file is the **authoritative current-state findings summary** for EVAL-003 after the Controller correction, finalization, and documentation-consistency passes. Earlier versions remain available in Git history; they contain the superseded zero-Hindi pack, single-reader protocol, browser-crop approach, and other correction history. Do not treat those historical states as current instructions.

---

## 1 · The two CVIT releases are one source lineage for calibration purposes

Resources contains two related Devanagari-signage releases, IndicSTR12 and IIIT-ILST. Of the **176 IIIT-ILST image+annotation records available locally, 173 are byte-identical to an IndicSTR12 photograph**, leaving only 3 unique labelled IIIT-ILST records in that locally usable subset.

**Consequence:** these releases must not be counted as two independent sources. The committed Hindi-primary pack attributes each selected shared photograph deterministically to one record, but that attribution is provenance bookkeeping, not evidence of independent origin. **BSTD remains the only genuinely separate Devanagari lineage reserve and is untouched.**

---

## 2 · Source annotations are not project ground truth

On the **173 byte-identical shared photographs**, the two releases' text regions were matched geometrically at IoU ≥ 0.5 with a strict one-to-one greedy matcher. Results:

| Measure | Result |
|---|---:|
| Regions matched | **1,082** |
| Identical transcription | **725 (67.0%)** |
| Different transcription | **357 (33.0%)** |
| Different pairs that match after mechanically deleting virama, nukta, anusvara and chandrabindu | **64 / 357** |

This is **cross-dataset annotation disagreement between two releases from the same source lineage**. It is **not** human inter-annotator agreement, **not** a measure of human reading ability, and **not** an accuracy ceiling or evaluator threshold.

The supported conclusion is narrower and important: **dataset transcriptions are unsafe to promote directly to project ground truth.** EVAL-003 therefore constructs its own reference from two independent blind human readings.

The one-to-one matcher is not justified merely by the real corpus having zero contested partners. `build-candidate-pool.py --self-test` contains the adversarial case the corpus lacks: two A-regions both prefer one B-region, and the corrected matcher permits that B-region to be used only once.

---

## 3 · The acquired material is full-scene photography, not pre-cropped words

The locally acquired IndicSTR12 material consists of **full scene photographs containing multiple annotated text regions**, not one pre-cropped word per image. The same broad task shape applies to IIIT-ILST.

Only **551 of 4,476 acquired CVIT images** have a locally usable paired annotation in the material available to EVAL-003:

- IndicSTR12: **375** locally paired image+annotation records
- IIIT-ILST: **176** locally paired image+annotation records

This is a downstream planning fact, not an acquisition error. The Eval→Resources correction proposal records the distinction between media acquired and locally paired records, plus the two valid overlap denominators: 173/1,390 for the full IIIT-ILST acquisition and 173/176 for the locally paired subset.

Because a scene can contain many text regions, EVAL-003 deterministically chooses **one region per photograph** and materialises that region as the unit shown to both readers and future checkers.

---

## 4 · Committed primary V0 pack: 173 eligible Hindi photographs → 54 selected

**Controller-approved committed configuration:**

`--overlap-policy admit-once --language-filter hindi --target-n 54`

| Step | Records |
|---|---:|
| Labelled source records | 551 |
| Remove second copies of 173 shared hashes under `admit-once` | −173 |
| Remove same-source duplicate records | −3 |
| Remove records outside the Hindi language filter | −202 |
| **Eligible Hindi photographs** | **173** |
| **Selected** | **54** |

All **54 selected items are Hindi-labelled and have 54 distinct photograph hashes**. One photograph is one item; no shared photograph is counted twice.

Every Hindi-labelled photograph in this local CVIT material is one of the shared photographs. That is why the earlier `exclude` configuration produced **0 Hindi**. That configuration is superseded and must not be used to regenerate the committed V0 pack.

The script retains `exclude` as generic machinery, but the committed V0 reproduction command must explicitly pass `admit-once`, `hindi`, and `54`. The authoritative reproduction instructions live in `eval/calibration/devanagari-v0/README.md`.

---

## 5 · Difficulty/coverage profile of the committed 54-Hindi pack

These figures were recomputed on the **current committed 54**, not carried over from the superseded pack:

| Property | Committed 54-Hindi pack |
|---|---:|
| Region area | **864 → 182,700 px²**, median 9,372 |
| Region share of frame | **0.11% → 37.1%**, median 3.5% |
| Annotated regions in source photo | **1 → 28**, median 3 |
| Transcription length | **3 → 12 characters**, median 6 |
| Contains conjunct | **20 / 54** |
| Contains vowel sign | **53 / 54** |
| Contains nukta | **1 / 54** |

The 12 strata are deterministic spread proxies, **not a validated difficulty scale**. Blur and contrast are still unmeasured. Nukta coverage is effectively absent, so this pack cannot support a strong claim about nukta handling.

---

## 6 · Reviewer and checker see the exact same crop bytes

`materialise-crops.py` writes one canonical PNG crop per selected item. The reviewer interface and future checker input reference **the same materialised files**, with crop hashes recorded and checked across all 54 items.

Crop geometry has an explicit synthetic self-test. That test caught a real `sips` edge case at origin coordinates; the implementation includes the verified workaround and refuses normal materialisation if the geometry self-test fails.

The review pack is mechanically blinded: readers see the crop and item ID, **not** dataset transcription, expected answer, or model output.

---

## 7 · Human reference protocol: two independent Hindi-competent readers

The future reference is built by **two independent blind Hindi-competent readers**.

Each reader separately transcribes exactly what is visibly drawn and can mark an item `cannot read` or `ambiguous`. They do not see dataset labels or one another's answers before both passes are frozen.

- **Exact reader agreement** becomes the high-confidence reference for the strict calibration gate.
- **Reader disagreement** is not silently resolved in either reader's favour; the item is excluded from the strict gate or handled in a separate recorded adjudication step.
- Neither reader alone becomes ground truth.

After both reader passes are frozen and a reference exists, **either reader may perform the later altered-target validity check**. That check cannot edit or replace the frozen reference; doubt means the altered item is dropped. No third reader is required by this protocol.

Estimated human time remains approximately **3.5–4.5 hours total across two readers**, including the later short altered-target check.

Human review has **not** started and still requires Controller approval.

---

## 8 · Checker plumbing is ready without changing judgement semantics

`check-vlm.mjs` now supports per-item targets while preserving the existing scoring predicate. Historical regression evidence:

- **27 / 27 stored historical checker cases re-scored**
- **0 judgement mismatches**
- malformed per-item fixtures are rejected rather than silently skipped

No checker has been qualified by EVAL-003 yet. The checker roster and any API/model spend remain separate Controller decisions.

---

## 9 · What EVAL-003 establishes—and what it does not

EVAL-003 establishes **readiness to perform a checker-calibration study** on a bounded Hindi-primary real-photo pack. It does not establish that any checker is trustworthy, because no checker has yet been run on the human-derived references.

It also does not establish:

- human reading accuracy in general;
- a 67% or 73% evaluator ceiling;
- transfer from photographed signage to generated Devanagari text;
- transfer from Hindi to Marathi;
- cross-source transfer, because BSTD remains untouched;
- a final capability benchmark or Capability Registry value.

The primary V0 result, once run, will speak specifically to **reading Hindi text from these photographed signage crops under this protocol**. Marathi stress testing is deferred and would require Marathi-competent readers and separate reporting.

---

## 10 · Scope and stop state

No human review, API/model call, generator run, EVAL-004 work, Registry work, or new data acquisition was performed in EVAL-003 readiness.

BSTD remains the held-out independent lineage reserve and was not opened/selected for this task.

The outstanding Controller decisions are now operational spend/next-stage decisions:

1. whether to authorize approximately 3.5–4.5 hours across two Hindi-competent readers;
2. which checker models/tools to qualify and what API spend to authorize;
3. whether/when to action the Eval→Resources factual correction proposal.

For implementation details and the correction trail, see:

- `eval/calibration/devanagari-v0/README.md`
- `eval/calibration/devanagari-v0/HUMAN-REVIEW-GUIDE.md`
- `eval/calibration/devanagari-v0/CALIBRATION-RUN-PLAN-V0.md`
- `eval/calibration/devanagari-v0/annotator-disagreement.json`
- `eval/calibration/devanagari-v0/PROPOSED-V0-COMPOSITION.md` (decision record)
- `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md`
- Git history of this findings file for superseded intermediate states
