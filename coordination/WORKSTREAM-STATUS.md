# Workstream Status

**Current snapshot:** 28 Aug 2026 — EMP-001 is **authorised and live**. The first paid tranche has
run; five exact-text checkers were tested and all five were disqualified. Three zero-to-low-spend
lanes are open in parallel.

**Refreshed by the Repository Governor under GOV-005**
(`governance/reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md`), against `main` at `0e24d6a`. The
previous snapshot said spend approval was pending and no paid call was authorised; both were false.

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
| Canon | 19 live accepted sources; request grammar and coverage frozen; Canon value remains empirically unproven. User-supplied Upwork/Fiverr marketplace demand research committed as external research — **not** a Canon source. | **CANON-011** — marketplace-derived brief and prompt bank, USD 0 | Return the derived bank for Controller review. Live Canon stays 19 unless a source passes the Audit Gate. |
| Eval | Capability v2 44 = 43 active + 1 dormant; 13 condition families; 12 core + 2 reserve slots. **0 qualified instruments, 0 Registry rows** — now after testing five exact-text configurations, not before testing any. | **EVAL-028** — prepare the fail-closed human-confirmed composite, USD 0, no human time. **EVAL-024** — generate and seal the 16 A-TEXT images, scoring not authorised. | Controller review of the prepared composite, then a separate decision on human review time. |
| Resources | Topology v3 / CpAO v3 / four-pack structure frozen; historical v2.1 preserved. | No broad acquisition | Acquire or capture only material demanded by a separately approved later tranche. |
| Governor | GOV-005 merged pending — **PASS WITH NON-BLOCKING NOTES**; one High finding (F-1, live evidence not committed) routed and unresolved. | none | No new Governor round scheduled. |

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

## Active lanes

**EVAL-028 — human-confirmed exact-text composite, preparation only.** An automated stage (Cloud
Vision preferred, for stability and low false-fail rate) may only **reject**; anything it would pass
goes to two independent blind human readers who never see the target, the OCR output or each other's
answer. Any disagreement or ambiguity **fails closed**. No human time is consumed and no API call is
made by this task. Cloud Vision being preferred does not make it qualified.

**EVAL-024 — A-TEXT generation-only.** Generate and seal the 16 frozen images (4 strings × 2 repeats
× 2 routes) now, in parallel with evaluator work. **Scoring, interpreting or promoting them is not
authorised.** This reverses the original ordering deliberately; it does not relax the scientific
gate. Branch `origin/work/eval-024-parallel-atext-generation-only` holds the orchestrator and tests;
no generation result is committed.

**CANON-011 — marketplace-derived brief and prompt bank, USD 0.** Turn the committed Upwork/Fiverr
research into provenance-preserving benchmark briefs. Upwork buyer jobs may be used as customer-intent
briefs; **Fiverr seller gigs may not** — a seller's package is not a customer's request.

> **Open ambiguity, routed to the Controller (GOV-005 finding F-4).** EVAL-024 and CANON-011 each
> have **two** authorising Controller decisions and **two** task files, with no supersession marker
> on either pair. Which governs is undecided.

## Still blocked / not authorised

- A-TEXT scoring or evaluation until a qualified evaluator covers the required scripts and its
  handoff is accepted.
- Registry population from any current unqualified instrument.
- Further paid text-judge candidate sweeps without a new Controller decision.
- The full 90-generation Stage A; Stages B and C.
- Broad controlled-pack acquisition.
- Production IR / Planner implementation.
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
- qualified exact-text evaluators: **0** — five tested, five disqualified;
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

**Controller review of the prepared EVAL-028 composite**, then a separate decision on whether to
spend human review time on it. Alongside that, the Controller has four open questions from GOV-005:
whether completed qualification results get sealed into `main` (F-1); which EVAL-024 and CANON-011
authorisations govern (F-4); whether `eval/HANDOFF.md` is refreshed (F-2); and whether the decision
index and the stale `NOT IN FORCE` status fields are normalised (F-5, F-6).
