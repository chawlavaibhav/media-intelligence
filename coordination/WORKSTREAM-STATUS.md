# Workstream Status

**Current snapshot:** 28 Aug 2026 — EMP-001 is **authorised and live**. The first paid tranche has
run; five exact-text checkers were tested and all five failed the strict zero-false-pass standard.
**Exact text is now a non-blocking measured capability**, so unrelated work is no longer held up by
it. Three lanes are open in parallel.

**Refreshed by the Repository Governor under GOV-005**
(`governance/reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md`), resynced against `main` at
`8990a7a` after the Controller's disposition
(`coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md`).

**Read `PROJECT-MEMORY.md` and `coordination/CONTROL-STATE.md` first.** `CONTROL-STATE.md` is the
current execution posture and **governs where this file and it differ**.

## Global posture

**Broad research and design are closed. Paid execution is authorised, bounded and in progress.**

The user approved EMP-001 at **USD 10 total consumed API spend**, with a **USD 6 text-judge
qualification sub-cap**, **zero retries** and no account pre-funding above the ceiling.
`coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md`.

**USD 1.3037905 has been consumed.** No image has been generated and no Registry row exists.

| Stream | Current state | Active approved work | Next gate |
|---|---|---|---|
| Canon | 19 live accepted sources; request grammar and coverage frozen; Canon value remains empirically unproven. User-supplied Upwork/Fiverr marketplace demand research committed as external research — **not** a Canon source. | **CANON-011** — marketplace-derived brief bank, USD 0 | Return the derived bank for Controller review. Live Canon stays 19 unless a source passes the Audit Gate. |
| Eval | Capability v2 44 = 43 active + 1 dormant; 13 condition families; 12 core + 2 reserve slots. **0 qualified instruments, 0 Registry rows** — now after testing five exact-text configurations, not before testing any. | **EVAL-029** — benchmark-grade text OCR, ≤ USD 0.432. **EVAL-024** — generate and seal the 16 A-TEXT images; behind a cleanup gate, USD 0 spent so far. | EVAL-029 recomputation, then the Cloud Vision Latin screen. |
| Resources | Topology v3 / CpAO v3 / four-pack structure frozen; historical v2.1 preserved. | No broad acquisition | Acquire or capture only material demanded by a separately approved later tranche. |
| Governor | GOV-005 resynced to current main, awaiting merge — **PASS WITH NON-BLOCKING NOTES**; one High finding (F-1, completed live evidence not sealed into GitHub) routed and unresolved. | none | No new Governor round scheduled. |

## What EMP-001 found

The tranche asked whether any available system can reliably tell that the text drawn in an image is
**exactly** the text requested. Five configurations were measured against the frozen 96-item
Devanagari battery:

| Candidate | Outcome |
|---|---|
| Anthropic `claude-haiku-4-5-20251001` | Disqualified |
| Anthropic `claude-sonnet-5` | Disqualified — 20 false passes across 7 unique items |
| Google `gemini-3.5-flash-lite` | Disqualified twice on two independent complete screens |
| Google Cloud Vision `TEXT_DETECTION`, no language hints | Disqualified — 18 false passes across 6 unique items, every one repeated 3/3 |
| Tesseract 5.5.3 with all six lexical dictionaries disabled (USD 0) | Disqualified — 3 false passes, but a 0.67 false-fail rate |

**The mechanism, in plain terms.** Modern recognisers use dictionary and language knowledge to
repair broken words. Shown a deliberately misspelled word, they return the correct one — which is
exactly the behaviour that ships a defect with a passing grade. Turning that knowledge off cut false
passes sharply but made the recogniser reject correct text instead. Routing by script removed
wrong-script errors but not false passes.

**The zero-false-pass gate was never relaxed.** That is what makes this a usable result.

**Consequences.** General-purpose multimodal LLMs are frozen as the primary exact-text judge family.
The Tesseract configuration line is **closed** — no further page-segmentation, engine-mode, language
or preprocessing sweeps without a new mechanism-level rationale.

## The 28 August course correction — exact text stops being a gate

`coordination/decisions/CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md`

One imperfect capability had been holding the whole benchmark hostage: nothing could be measured
about any model until an exact-Hindi-text checker reached zero false passes, a bar nothing could
clear. The Controller separated two jobs that had been treated as one.

| Job | Question | Standard | Status |
|---|---|---|---|
| Strict exactness certification | "Can I promise the customer this text is exactly right?" | zero mismatch false passes | **Nothing has passed.** All five results above stand, unrewritten. |
| Benchmark-grade text OCR | "Which generation route handles text better?" | known, bounded error | New contract `benchmark_text_ocr_v1` |

`benchmark_text_ocr_v1`: false-pass ≤ **0.15**, false-fail ≤ **0.10**, repeat consistency ≥ **0.95**,
execution failure ≤ **0.05**, 3 repeats, blind transcription only, retries 0, **no human review**.

`benchmark_qualified` and `strict_exactness_qualified` stay explicitly distinct, and any metric
carries its evaluator's measured error rate and contract id.

**Cloud Vision, both statements true at once:** its Devanagari numbers (false-pass 0.125, false-fail
0.0208, consistency 1.0, zero empties, zero infrastructure failures) **fail** the strict screen and
**meet** the benchmark thresholds. Different questions, different answers.

**What follows:**

- **EVAL-028 is cancelled and must not be executed.** `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md`.
- **No mandatory human-in-the-loop step exists in the production API architecture.**
- **Exact-text imperfection blocks nothing else.** Any Stage-A slot may proceed once the instruments
  that measurement needs are ready.
- **The strict results are preserved as valid research** under `strict_exactness_certification`.

## Active lanes

**EVAL-029 — benchmark-grade text OCR.** `eval/tasks/EVAL-029-BENCHMARK-GRADE-TEXT-OCR.md`. Build
`benchmark_text_ocr_v1`; **recompute** (not rerun) the existing Cloud Vision Devanagari evidence
against it, mechanically from stored observations, and stop and return if it disagrees; then, only if
that passes, run the missing Latin screen — 288 calls, retries 0, reservation **USD 0.432**, on the
existing ledger, no language hints. If both scripts pass, Cloud Vision is **benchmark-qualified** for
comparison, still not strict-certified. If EVAL-024's sealed artifacts exist, score those exact
images without humans or regeneration. **Registry text rows stay blocked** pending Controller review.

> **Check before spending:** the recomputation step needs stored per-trial observations that are
> **not on `main`** (GOV-005 F-1). If they are not reachable locally, that step cannot be performed
> as written.

**EVAL-024 — A-TEXT generation-only, returned at USD 0, behind a cleanup gate.**
`coordination/decisions/CONTROLLER-EVAL-024-READINESS-CLEANUP-AND-LIVE-2026-08-28.md`

`FAL_KEY` was unavailable and the runner correctly treated that as a **pre-dispatch** failure, so no
provider call and no spend occurred. The design is accepted in principle. Before live dispatch:

1. sync the branch to current `main`;
2. restore `preflight-result.json` and `perceptibility-mechanical.json` byte-for-byte from `main`;
3. stop writing non-PNG bytes to `.png` paths — detect media type from the returned bytes, preserve
   and hash the raw bytes, never transcode for a convenient extension;
4. restore the pinned Tesseract traineddata so the full suite is green again.

If `FAL_KEY` is present after cleanup, the 16 generations may run from that exact pushed head on the
existing ledger. If not, stop pre-dispatch and return. Committing the 16 sealed image bytes is a
**bounded EMP-001 exception**, not a general policy for generated media.

**CANON-011 — marketplace-derived brief bank, USD 0.** Turn the committed Upwork/Fiverr research into
provenance-preserving benchmark briefs. Upwork buyer jobs may be used as customer-intent briefs;
**Fiverr seller gigs may not** — a seller's package is not a customer's request.

**Authority chains, settled 28 Aug 2026** (GOV-005 F-4 resolved):
`coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md`

| Lane | Governing | Historical, preserved, not governing |
|---|---|---|
| EVAL-024 | `CONTROLLER-EVAL-024-READINESS-CLEANUP-AND-LIVE-2026-08-28.md` → `CONTROLLER-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md` → `eval/tasks/EVAL-024-PARALLEL-ATEXT-GENERATION-ONLY.md` | `CONTROLLER-EMP-001-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md`; `eval/tasks/EVAL-024-ATEXT-GENERATION-ONLY.md` |
| CANON-011 | `CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PREP-2026-08-27.md` → `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-BANK.md` → `canon/research/marketplace-demand-v1/README.md` | `CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PROMPT-PREP-2026-08-27.md`; `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-PROMPT-BANK.md` |


## Still blocked / not authorised

- **Mandatory human-in-the-loop exact-text review in the production API architecture.** Withdrawn
  28 Aug 2026; not to be reintroduced without a new decision.
- **Treating benchmark-grade OCR as a perfect exactness certifier.** It is a confidence signal with
  a measured error rate, never a guarantee.
- Registry population from text metrics until the benchmark-grade handoff is reviewed.
- Further Tesseract or OCR configuration sweeps without a new mechanism-level rationale.
- Broad Stage-B and Stage-C execution without their own instrument readiness.
- Broad controlled-pack acquisition.
- Production IR / Planner implementation before sufficient empirical capability evidence exists.
- **EVAL-006 remains PAUSED — DO NOT EXECUTE.** Its spend authority was withdrawn.
- Historical E7 paid admission and E8 deep qualification.
- The Canon value gate remains unrun.

**No worker may infer authorisation from an old task file.** Where a task file and a current
Controller decision disagree, the decision wins.

## Important pricing correction — still in force

Execution budgeting for current Veo 3.1 / Lite routes is **per generated second**. The old
per-complete-video implication is withdrawn for execution planning.
`coordination/decisions/CONTROLLER-VEO-PRICING-UNIT-CORRECTION-2026-08-26.md`.

The full 90-generation Stage-A generation-side planning estimate is approximately **USD 52.01 + up
to ₹4.50 Sarvam**, roughly **₹4,967** at the reference FX rate, before evaluator, human, tax and
resource costs. **It remains unapproved** — the USD 10 approval covers EMP-001 only.

## The empirical floor

Still zero:

- qualified models or workflows: **0**;
- qualified subjective or perceptual evaluator families: **0**;
- exact-text evaluators qualified under the **strict** zero-false-pass standard: **0** — five tested,
  five disqualified;
- text evaluators holding **`benchmark_qualified`** status: **0** — Cloud Vision meets the benchmark
  thresholds on Devanagari, but its Latin screen has not been run;
- empirical Registry rows: **0** (mechanically verified);
- A-TEXT image generations: **0**;
- customer CpAO observations: **0**.

No longer zero:

- consumed API spend: **USD 1.3037905** of a USD 10 ceiling;
- live evaluator calls: roughly **2,500**, plus about 1,150 zero-cost local Tesseract executions;
- instrument configurations scientifically disqualified: **5**, with a mechanism finding attached.

> **How solid are those spend and result figures?** `eval/runs/` is git-ignored and no per-trial
> record, ledger or qualification result from any live run is committed. They exist only inside
> Controller decision records and cannot be recomputed from GitHub. GOV-005 finding **F-1**, routed
> to Eval and the Controller, **unresolved**.

## Next gate

**Exact text is no longer a programme-wide blocker.** The next moves, in order of leverage:

1. **EVAL-029** — recompute the Cloud Vision Devanagari evidence against the benchmark contract,
   then run the Latin screen if it passes.
2. **Seal the completed EMP-001 evidence into GitHub (F-1).** Accepted as High by the Controller and
   still unresolved. EVAL-029's first step already depends on it.
3. **EVAL-024 cleanup**, so 16 sealed images exist for a benchmark-qualified evaluator to score.
4. **Open Eval corrections for F-2, F-6, F-7 and F-8** — the stale handoff, the regenerated
   `NOT IN FORCE` status fields, machine-absolute preflight paths, and the hand-maintained
   prior-spend default.

**EVAL-028 is superseded and must not be executed.**
