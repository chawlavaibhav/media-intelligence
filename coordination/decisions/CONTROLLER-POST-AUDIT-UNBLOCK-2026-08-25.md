# Controller Decision — Post-audit unblock and Eval restart

**Date:** 25 Aug 2026
**Controller disposition:** APPROVED
**Baseline:** `main` at `7b2891278d32fbfa8e3ea7dc0d66f3192c1b7b69`

## Purpose

Resolve the three stream blockers after GOV-001 and re-scope the audit freeze so the project can begin empirical capability registration without reopening unrelated work.

## 1. Canon — close CANON-008 cleanly

**Decision:** choose CANON-008 option 4 for now: accept live Canon at **19** and leave the Devanagari-structure gap explicitly open.

The official Dalvi archive route exposes only a 3-page abstract and the full thesis is behind IIT Bombay authentication. No bypass, mirror or substitute identity is authorised. CANON-008 is therefore **closed as a legitimate acquisition-gate stop**, not failed and not resumed.

No replacement Devanagari source is authorised by this decision. If a legitimate full thesis or a separately approved replacement source becomes available later, it requires a new Canon task.

**Practical consequence:** one inaccessible source no longer blocks project progress. Canon remains at 19 live accepted sources, with the Devanagari-structure gap visible rather than papered over.

## 2. Resources — accept correction and hold on demand

**Decision:** accept the Resources correction in `resources/PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md` as the disposition of `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`.

The corrected composition figures, crop-label recoverability, and lineage conclusion are accepted: IndicSTR12 and IIIT-ILST are treated as **one source lineage** for holdout/independence purposes; BSTD remains the genuine cross-lineage reserve.

No further acquisition is authorised now. Resources stays closed and should source only against a concrete Eval requirement.

**Practical consequence:** Resources has no unresolved blocker. Its current 34,786-item corpus is available for approved internal research/evaluation tasks, subject to the recorded rights limits.

## 3. Eval — approve the checker qualification gates provisionally

The authoritative EVAL-005 battery remains the **96-item validated view**: 48 match / 48 mismatch, 48 accepted base words, 33 hard opportunities, 20 failure classes across 5 groups.

**Approved qualification gates for the first run:**

- **False passes:** zero. Any false pass is disqualifying.
- **False-fail rate:** at most 10% on clean match items.
- **Refusal rate:** at most 5%, reported separately.
- **Repeat consistency:** at least 0.95 across at least 3 full passes of the whole battery in both checker shapes.

The last three thresholds are **provisional usability thresholds**, not empirically established truths. They may be revised only by a later Controller decision using evidence from completed runs. The iid reference calculation remains a sizing aid only and is not a checker accuracy claim.

A screening pass may count as pass 1 of the three repeat passes **only if** model version, prompts, parameters, input bytes and scoring code are unchanged. Any experiment mutation makes it a separate run.

## 4. Checker roster and budget for EVAL-006

Approved checker candidates for the first qualification screen:

1. OpenAI **GPT-5.6 Luna**
2. Google **Gemini 3.7 Flash**
3. Anthropic **Claude Sonnet 5**
4. Alibaba **Qwen3-VL-32B-Instruct**

The worker must verify the exact API model identifier, availability and live pricing from official provider documentation immediately before the run. If a named candidate is unavailable, record it as unavailable and continue with the remaining approved candidates; **do not silently substitute another model**.

**Checker-qualification API budget:** maximum **₹4,000**. If the live-price forecast exceeds this cap, stop before spending and return to the Controller.

## 5. Capability Registry schema — approved for Eval measurement storage

`eval/battery/CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml` is approved as the basis for the first Eval Registry with this boundary:

- its measurement/provenance fields may be implemented and populated by Eval;
- the proposed cross-stream fields may be stored because they preserve evidence needed later;
- **no Production Planner or routing semantics are approved by this decision**. Storing `observation_unit`, `calibration_status`, failure co-occurrence, cost and freshness information does not yet define how a future Planner must weight them.

No scored Registry entry may be written from an uncalibrated instrument. `required_but_no_calibrated_instrument` remains a valid visible state rather than silently dropping a capability.

## 6. Audit freeze — re-scoped

The global audit freeze is **not fully lifted**. It is re-scoped as follows:

- **OPEN:** EVAL-006 only — checker qualification and bounded Capability Registry bootstrap under its task file and budget.
- **CLOSED/HOLD:** Canon expansion, Resources expansion, new acquisition, Production IR, Production Planner/routing implementation, Canon-consumption/RAG/training, and any Eval dimension/model/workflow not named in EVAL-006.

This is an explicit Controller re-scope of the GOV-001 audit freeze. Completion of EVAL-006 does not automatically authorise the next task.

## 7. What this decision does not claim

It does not claim the Capability Registry already exists; it exists only when EVAL-006 writes evidence-backed entries.

It does not claim the current Eval battery is exhaustive. The broader production capability families in `eval/battery/CAPABILITY-LAB-V0-PLAN.md` — including product identity, reference conditioning, human-object interaction, motion/physics, speech/lip-sync and two-speaker dialogue — remain future measurement work, not discarded scope.
