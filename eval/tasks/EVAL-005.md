# Task EVAL-005: Devanagari exactness checker qualification — design hardening

**TASK ID:** EVAL-005 *(Controller-assigned)*
**STATUS:** **Controller-authorised DESIGN HARDENING ONLY — task closed and merged.** During this
task no checker/model/API qualification run and no human validation occurred; only deterministic
local construction, rendering and test verification were run.

> **Superseded on current state, 25 Aug 2026:** human validation has since been performed and is
> complete — 98 of 98 answered, 5 of 53 base words rejected, 10 items excluded, authoritative
> battery now 96 items. This file records the design-hardening task as it was; it is not the
> current state. See
> [`../battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md`](../battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md).
> **Checker qualification has still not started.**
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
3. Gate mismatch visibility on the **decoded pixel raster** — not on glyph sequences, and not on
   encoded PNG bytes.
4. Make canonicalisation semantics true to their documentation.
5. Rebuild the sizing claim on **distinct base-word opportunities**, recompute the target rather
   than inheriting it, and state plainly that distinct words do **not** establish iid or
   exchangeable trials.
6. Correct the qualification/repeat rule and remove the false redundancy between gates.
7. Formalise this task; prepare the native-validation sheets **without executing them**; state
   precisely what Resources would need to supply.
8. Update Eval-owned handoff/findings so a fresh session does not re-derive the state.

**Second Controller review pass (same task, same branch)** added three bounded corrections:

9. Compare **decoded pixels**, not encoded PNG bytes — and keep the two hashes distinct in name and
   purpose.
10. Remove every claim that distinct base words make the opportunities "statistically independent";
    keep zero-false-passes as the deterministic gate and the Clopper-Pearson figure as an explicitly
    labelled iid **reference** calculation.
11. Reflect merged Resources state (PR #5) and reorder the Resources ask so the first step is a
    check of existing local material rather than any acquisition.

**Third Controller review pass — merge gate** added three bounded corrections:

12. Make the PNG decoder **fail closed** on any feature it does not faithfully decode — transparency
    above all — by narrowing and stating its supported contract, not by growing a general-purpose
    PNG library.
13. Remove wording that turns the iid reference calculation into a demonstrated bound on a checker.
14. Replace "nothing has been run" with the precise statement of what has and has not happened.

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
| `eval/battery/devanagari-exactness/devtext.py` | one pinned font asset; pixel-level screen |
| `eval/battery/devanagari-exactness/pngraster.py` | stdlib PNG decoder with an explicit, narrow, fail-closed contract; pixel fingerprint vs file hash |
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

**Resources PR #5 is merged**, and `origin/main` was merged into this branch before final
verification. Its records establish that **3,924 of 3,925 single-word crops are
transcription-resolvable** (IndicSTR12 2,711/2,711; IIIT-ILST 1,213/1,214), and that IndicSTR12 and
IIIT-ILST remain **one evaluation lineage** — with BSTD the only genuine cross-lineage reserve.

Two things follow, and the second is easy to get wrong:

- The battery's base words are unaffected: it still builds from the 53 distinct Hindi strings in the
  EVAL-003 candidate manifest, reused **as lexical items only**.
- Those merged records establish that **recoverable labels exist**, not that the lexical strings are
  in git. The raw strings may still live only in the git-ignored Resources corpus, so how many
  *distinct* Hindi words they yield is **unknown** — which is why
  `EVAL-005-RESOURCES-REQUEST.md` asks Resources to check existing local material first rather than
  acquire anything.

## STOP CONDITIONS

Beyond the eight in `shared/AUTONOMY-POLICY.md`, stop and return to the Controller if:

- fixing the rendering would require committing or licensing a font asset;
- no available local renderer can pin the exact font used for shaping;
- a defensible sizing calculation cannot be supported without changing the approved evaluation
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
   sub-5% iid reference figure, not the run itself — a run at 53 words is possible, it just reports
   the figure at 37 opportunities (7.8%).
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
3. A mismatch ships only if the NFC-canonical strings differ **and** the **decoded pixels** differ
   — dimensions plus RGBA8 pixel data, not encoded PNG bytes. The known canonically-equivalent nukta
   pair is rejected; a pair whose glyph sequences differ but whose pixels are identical is rejected;
   three encodings of one picture are shown to have three file hashes and one pixel fingerprint and
   are treated as visually identical; a genuinely visible pair (सुबह / सुवह) is accepted; the decoder
   raises rather than guessing on anything it cannot decode.
4. `nfc()` performs NFC and nothing else; whitespace handling is a separately named, separately
   tested rule; the comparison predicate does not strip.
5. Every mismatch item sits on a distinct base word; `hard items == distinct hard base words`; the
   quoted figure is derived from that count; every machine-readable statistical field names its iid
   assumption; `independence_status` records **NOT ESTABLISHED**; and no EVAL-005 file asserts the
   opportunities are "statistically independent".
6. The battery remains deterministic, 50/50 balanced, non-trivial to game, and covers all 20
   failure classes across all 5 groups.
7. No module in the battery references a network client, a URL or an API key.
8. The native-validation sheets exist, are blank, and carry stable ids.
9. The full test suite passes from a clean run, with commands, exit code and counts recorded in the
   Controller Brief.

**Status: all nine met, after three review passes.** `python3 test_devanagari_exactness.py` → exit 0,
**165 checks across 43 tests**. Criterion 3 additionally requires that the PNG decoder fail closed on
any feature it does not faithfully decode — transparency in particular is applied correctly or the
file is refused, never ignored. See `EVAL-005-CONTROLLER-BRIEF.md` for the recorded run and
environment provenance.

## RESULT LOCATION

`eval/tasks/EVAL-005-CONTROLLER-BRIEF.md` on `work/eval-005-controller-review`.

## RELATIONSHIP TO THE INHERITED PROPOSAL

`work/eval-005` remains untouched and reviewable. Its `PROPOSED-TASK-SPEC.md` and
`PROPOSED-EVAL-005-CONTROLLER-BRIEF.md` are retained and marked superseded rather than deleted, so
the Controller can compare what was proposed against what was corrected. **This file is the
authoritative task record; where the two disagree, this one governs.**
