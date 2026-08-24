# Task EVAL-005: Devanagari exactness checker qualification — design hardening

**TASK ID:** EVAL-005 *(Controller-assigned)*
**STATUS:** **Controller-authorised DESIGN HARDENING ONLY.** Not a run. No checker has been called,
qualified, ranked or entered anywhere.
**OPENED:** 25 Aug 2026 · **BRANCH:** `work/eval-005-controller-review`

**OBJECTIVE:** Fix the defects the Controller identified in the inherited `work/eval-005` proposal,
so that a Devanagari exactness checker-qualification battery exists whose blinding, rendering,
visibility screening, canonicalisation and statistics are all defensible — and prepare, without
executing, the human validation step it will eventually need.

**WHY WE ARE DOING THIS:** EVAL-004 was stopped because reading photographed signage is a weak
proxy for the failure that actually costs money: we ask a generator for a specific Hindi string, it
produces something subtly wrong, and the checker says *matches*. That false pass ships a broken
asset with a passing grade attached. The redesign proposed on `work/eval-005` had the right idea —
render the images ourselves, so ground truth needs no annotator — but four of its guarantees did
not hold in the code, and its headline statistic was computed over correlated trials. A
qualification battery whose own instruments are unverified would reproduce the exact error this
stream exists to prevent, one level up.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`.

---

## INPUTS

- `coordination/RUNBOOK.md`, `shared/COMMUNICATION-STANDARD.md`, `shared/AUTONOMY-POLICY.md`
- `eval/HANDOFF.md`, `eval/decisions/EVAL-004-STOP-2026-08-24.md`
- `eval/tasks/EVAL-003.md`, `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md`
- `eval/battery/INSTRUMENT-CALIBRATION-PLAN-V0.md`, `eval/battery/CAPABILITY-BATTERY-V0-DRAFT.md`
- `eval/scripts/check-vlm.mjs`, `eval/harness/`
- the whole inherited `work/eval-005` tree
- `eval/calibration/devanagari-v0/candidate-manifest.jsonl` — **as lexical items only**

## IN SCOPE

Design, local implementation and local testing only:

1. Remove target leakage from the `transcribe` checker shape, mechanically rather than in prose.
2. Pin shaping and rendering to the **same font asset**, and record enough provenance to audit it.
3. Gate mismatch visibility on the **final raster**, not on glyph sequences.
4. Make canonicalisation semantics true to their documentation.
5. Rebuild the statistical claim on **distinct base-word opportunities**, and recompute the
   sample-size requirement rather than inheriting it.
6. Correct the qualification/repeat rule and remove the false redundancy between gates.
7. Formalise this task; prepare the native-validation sheets **without executing them**; state
   precisely what Resources would need to supply.
8. Update Eval-owned handoff/findings so a fresh session does not re-derive the state.

## OUT OF SCOPE — and each is independently blocking

- **Any checker/model/API call.** No Qwen, Claude, GPT, Gemini, web OCR or external VLM.
- **Any image or video generation.**
- **Any human specialist time**, including the word-list validation this task prepares.
- **Any Capability Registry entry.**
- Resuming EVAL-004, or promoting its Reader-A pilot to ground truth.
- BSTD or the Marathi reserve — not consumed, and not to be consumed merely to raise item count.
- The Class B generated-glyph stress layer (`GENERATED-GLYPH-STRESS-LAYER.md`).
- Any change to approved battery dimensions, the observation-unit vocabulary, Registry
  architecture, Canon schemas, or Resources records.
- Editing `coordination/WORKSTREAM-STATUS.md` — a proposed replacement row is offered in the
  Controller Brief instead.
- Expanding the base word list from new external material.

## DELIVERABLES

| Path | What |
|---|---|
| `eval/tasks/EVAL-005.md` | this file |
| `eval/tasks/EVAL-005-CONTROLLER-BRIEF.md` | the review surface |
| `eval/tasks/EVAL-005-RESOURCES-REQUEST.md` | the precise cross-stream ask, if the pool is short |
| `eval/battery/devanagari-exactness/checker_input.py` | per-shape projections + blind check |
| `eval/battery/devanagari-exactness/devtext.py` | one pinned font asset; raster-level screen |
| `eval/battery/devanagari-exactness/build_items.py` | one-item-per-base construction + statistics |
| `eval/battery/devanagari-exactness/make_validation_sheets.py` | sheet generator |
| `eval/battery/devanagari-exactness/native-validation/` | prepared, blank sheets + plan |
| `eval/battery/devanagari-exactness/*.md` | corrected contract, metrics, taxonomy, README |
| `eval/findings/devanagari-exactness-design-findings.md` | updated findings |
| `eval/HANDOFF.md` | current state, EVAL-004 stop reflected |

## AUTONOMY MODE

**`autonomous` within the scope above.** Method is frozen (design/implement/test locally), inputs
are named, the budget is zero on every axis that could be spent, and the stop conditions below are
explicit. Anything that would require a call, a generation, a person or a Registry row is out of
scope and is a stop, not a judgement call.

## RESOURCE BUDGET

| | |
|---|---|
| API / model spend | **₹0.** No checker, VLM, OCR service or model of any kind is called. |
| Generation spend | **₹0.** No image or video model is called. |
| Human specialist time | **0 hours.** The validation sheets are prepared and left blank. |
| New data acquisition | **none.** No new external source is fetched. |
| Capability Registry entries | **0.** |
| BSTD / Marathi reserve | **untouched.** |
| Storage | negligible — the build directory is git-ignored and reproducible |

## APPROVED DEPENDENCIES

- EVAL-001 — Capability Battery V0 and the checker-calibration principle that a checker must earn
  trust on the specific task before its scores are believed. Unchanged by this task.
- EVAL-002 — evaluation plumbing; the identity rubric remains frozen and uncalibrated. Untouched.
- EVAL-003 — the Devanagari calibration pack. Its transcriptions are reused **as lexical items
  only**; its finding that source annotations are unsafe as ground truth stands and is respected,
  because the image is rendered from the string rather than described by it.
- The EVAL-004 stop decision, `eval/decisions/EVAL-004-STOP-2026-08-24.md`. Unchanged.

**Not depended on:** Resources PR #5 (IndicSTR12 / IIIT-ILST composition and recoverable crop
transcriptions) was **open, not merged**, when this task ran. No claim here rests on it. If it
merges, its records may change how many Hindi lexical items are available and should be re-checked
against `EVAL-005-RESOURCES-REQUEST.md`.

## STOP CONDITIONS

Beyond the eight in `shared/AUTONOMY-POLICY.md`, stop and return to the Controller if:

- fixing the rendering would require committing or licensing a font asset;
- no available local renderer can pin the exact font used for shaping;
- a defensible statistical bound cannot be supported without changing the approved evaluation
  architecture;
- the corrected sample-size requirement needs new external lexical material *(this fired — see
  `EVAL-005-RESOURCES-REQUEST.md`; it is reported, not resolved)*;
- a new evaluator or instrument is required;
- any external, API, model or human spend becomes necessary;
- a conflict is found with an approved EVAL-001/002/003 rule.

## HUMAN APPROVAL TRIGGERS

Each of these is a decision only the Controller can make, and each blocks a different thing:

1. **Approve or reject the hardened design.** Blocks everything downstream.
2. **Approve ~1.5 hours of one Hindi-competent reader** for the prepared sheets. Blocks the run.
3. **Approve the sourcing request to Resources** for ~31–37 more Hindi lexical items. Blocks the
   ≤5% bound, not the run itself — a run at 53 words is possible, it just carries a 7.8% bound.
4. **Approve a checker roster and API budget.** Blocks the run. No roster is selected here.
5. **Approve the proposed qualification thresholds** (0.95 repeat consistency, ≤10% false fail,
   ≤5% refusal). They are judgement calls with no empirical backing in this repository.
6. **Decide separately on the Class B generated-glyph layer.** Needs generation spend.

## ACCEPTANCE CRITERIA

This task is complete when **all** of the following hold, each verified by a committed test:

1. A `transcribe` checker payload contains no target, no ground-truth metadata, and no Devanagari
   character at all; a `verdict` payload contains the target and a prompt carrying it; injecting a
   target into a transcribe payload — as a field *or* inside the prompt — is detected.
2. Shaping and rendering demonstrably use the same pinned font **file** and face index; a missing
   font raises rather than falling back; no font binary is committed; provenance records the font
   SHA-256, the tool versions and every pixel-affecting setting.
3. A mismatch ships only if the NFC-canonical strings differ **and** the final PNG bytes differ.
   The known canonically-equivalent nukta pair is rejected; a pair whose glyph sequences differ but
   whose pixels are identical is rejected; a genuinely visible pair (सुबह / सुवह) is accepted.
4. `nfc()` performs NFC and nothing else; whitespace handling is a separately named, separately
   tested rule; the comparison predicate does not strip.
5. Every mismatch item sits on a distinct base word; `hard items == distinct hard base words`; the
   quoted bound is derived from that count; the epistemic limit ships with it.
6. The battery remains deterministic, 50/50 balanced, non-trivial to game, and covers all 20
   failure classes across all 5 groups.
7. No module in the battery references a network client, a URL or an API key.
8. The native-validation sheets exist, are blank, and carry stable ids.
9. The full test suite passes from a clean run, with commands, exit code and counts recorded in the
   Controller Brief.

**Status: all nine met.** `python3 test_devanagari_exactness.py` → exit 0, 121 checks across 37
tests. See `EVAL-005-CONTROLLER-BRIEF.md` for the recorded run and environment provenance.

## RESULT LOCATION

`eval/tasks/EVAL-005-CONTROLLER-BRIEF.md` on `work/eval-005-controller-review`.

## RELATIONSHIP TO THE INHERITED PROPOSAL

`work/eval-005` remains untouched and reviewable. Its `PROPOSED-TASK-SPEC.md` and
`PROPOSED-EVAL-005-CONTROLLER-BRIEF.md` are retained and marked superseded rather than deleted, so
the Controller can compare what was proposed against what was corrected. **This file is the
authoritative task record; where the two disagree, this one governs.**
