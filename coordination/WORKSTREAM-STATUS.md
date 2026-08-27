# Workstream Status

**Current snapshot:** 28 Aug 2026 — **the five parallel domain lanes have settled and merged, and no
domain lane is currently open.** EMP-001's paid work is complete: text-judge qualification ran, 16
A-TEXT images were generated and sealed, and those exact images were scored. **Exact text is a
non-blocking measured capability**, and the Capability Registry still holds **0 rows** by deliberate
Controller decision.

**Refreshed by the Repository Governor under GOV-006**
(`governance/reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`), against `main` at
`91984f50b294f11aefc7065f5ad11f9e0d3e2b9a`. The previous refresh was GOV-005 at `8990a7a`; its
figures were correct when written and are superseded here, not erased.

**Read `PROJECT-MEMORY.md` and `coordination/CONTROL-STATE.md` first.** `CONTROL-STATE.md` is the
current execution posture and **governs where this file and it differ**.

## Global posture

**Broad research and design are closed. EMP-001's authorised paid work has been executed and
integrated.**

The user approved EMP-001 at **USD 10 total consumed API spend**, with a **USD 6 text-judge
qualification sub-cap**, **zero retries** and no account pre-funding above the ceiling.
`coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md`.

**Recorded spend:** cumulative **USD 2.6397905** through the EVAL-024 generation tranche, plus a
separately recorded **USD 0.024** for EVAL-030's evaluator calls. **16 images have been generated and
scored. No Registry row exists** — and none should, because `benchmark_qualified` is intentionally
weaker than the Registry's admission bar. *(No committed artifact states a consolidated total that
includes the EVAL-030 figure — GOV-006 finding G6-02.)*

| Stream | Current state | Active approved work | Next gate |
|---|---|---|---|
| Canon | 19 live accepted sources, unchanged. Request grammar and coverage frozen and **not reopened**. **CANON-011 merged:** 18 marketplace-derived buyer cases, 16 runnable without contacting the buyer — the preferred real-demand pool for Stage-C and compound sourcing. It is external research in `canon/research/`, **not** a Canon source, and did not change the count of 19. | **None.** | Live Canon stays 19 unless a source passes the Audit Gate. GG-01…GG-04 stay observations; the grammar reopens only if a selected case actually needs the missing representation. |
| Eval | Capability v2 44 = 43 active + 1 dormant; 13 condition families; 12 core + 2 reserve slots. **Cloud Vision `TEXT_DETECTION` is `benchmark_qualified` on Devanagari and Latin, and `strict_exactness_qualified: false`.** Its evidence is sealed in Git and recomputable from a fresh clone. **16 A-TEXT images generated, sealed and scored: 7/16 exact.** **EVAL-026 landed temporal machinery only — no temporal evaluator is qualified and no pass mark exists.** **0 Registry rows.** | **None.** | Registry text rows remain blocked; admission semantics must not be weakened to create a first row. Temporal qualification needs all four prerequisites below. |
| Resources | Corpus posture unchanged. **RES-005 merged:** 12 clips from 12 distinct works, 12/12 passing the cleanliness screen, rights limited to CC BY / CC BY-SA / CC0 / US-Gov public domain. Only a **representative 3/3** passed EVAL-026 ingest. Material is **`MAT-TEMPORAL-BASE`, not `PACK-AV-CLEAN`**. | **None.** | Full 12-clip ingest under a recorded execution condition, before any temporal qualification. No broad acquisition authorised. |
| Governor | **GOV-005 closed and merged** (PR #48, `c794694`); **GOV-006** is the current round — PASS WITH NON-BLOCKING NOTES. GOV-005's High finding **F-1 (live evidence not in GitHub) is resolved** for the text-OCR lane. | GOV-006, complete and pushed, not merged. | Seven GOV-006 findings routed to their owning streams. |

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

**Since then the Latin screen has also run** (false-pass 0.1042, false-fail 0.0000, consistency 1.0),
so Cloud Vision is `benchmark_qualified` on **both** scripts and still `strict_exactness_qualified:
false` on both. GOV-006 re-derived all six figures from the sealed observations.

**What follows:**

- **EVAL-028 is cancelled and must not be executed.** `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md`.
- **No mandatory human-in-the-loop step exists in the production API architecture.**
- **Exact-text imperfection blocks nothing else.** Any Stage-A slot may proceed once the instruments
  that measurement needs are ready.
- **The strict results are preserved as valid research** under `strict_exactness_certification`.

## Settled lanes — all merged, none active

**Every lane that was open at GOV-005 has returned, been accepted and been merged.** Nothing below is
work to do; it is the record of what was done. **Do not restart, re-run or regenerate any of it.**

**CANON-011 — marketplace-derived benchmark brief bank.** 18 cases derived from real Upwork buyer
postings, 16 of them runnable without contacting the buyer. Upwork buyer jobs are customer-intent
evidence; **Fiverr seller gigs are not**, and none was used as a case. `MKT-015` is retained only as
blocked market evidence and must not be promoted to a runnable Stage-C case without a new decision.
The four grammar gaps GG-01…GG-04 are **observed representation gaps, recorded and routed with no
change made** — the Media Request Grammar was not reopened and the 30 authored briefs are
byte-identical. USD 0.
`coordination/decisions/CONTROLLER-CANON-011-INTEGRATION-2026-08-28.md`

**EVAL-024 — A-TEXT generation, closed.** All 16 frozen coordinates generated and sealed as committed
bytes: 8 from fal `openai/gpt-image-2` and 8 from fal `fal-ai/ideogram/v3`, 1024×1024 PNG, unseeded,
0 retries, 0 missing coordinates, 0 evaluator calls. Generation spend **USD 0.904**; manifest
fingerprint `1e124343…`. **These exact bytes are durable evidence. Do not regenerate them.**
`coordination/decisions/CONTROLLER-EVAL-024-INTEGRATION-2026-08-28.md`

**EVAL-029 — benchmark-grade text OCR, with durable evidence.** Cloud Vision `TEXT_DETECTION`, no
language hints, is **`benchmark_qualified`** for Devanagari (false-pass 0.1250, false-fail 0.0208,
consistency 1.0) and Latin (false-pass 0.1042, false-fail 0.0000, consistency 1.0), and remains
**`strict_exactness_qualified: false`**. Incremental spend USD 0.4320.

The completed evidence is now **sealed into Git** under
`eval/empirical-tranche-1/evidence/EMP-001/text-ocr/` — the exact source observations, the completed
result, and a bounded cost/ledger excerpt, all hash-fingerprinted, with no machine-local path
required. **A fresh clone can recompute both scripts' metrics from committed bytes alone.** That
closes GOV-005's High finding **F-1** for this lane.
`coordination/decisions/CONTROLLER-EVAL-029-REVIEW-SEAL-EVIDENCE-BEFORE-MERGE-2026-08-28.md`

**EVAL-030 — the 16 sealed images scored, without regeneration.** The scorer consumed the exact
sealed hashes; nothing was regenerated.

| | Exact matches |
|---|---|
| GPT Image 2 | **6 / 8** (0.750) |
| Ideogram v3 | **1 / 8** (0.125) |
| **Overall** | **7 / 16** (0.4375) |
| Devanagari | 5 / 8 |
| Latin / Hinglish | 2 / 4 |
| Commercial claim with ₹ | 0 / 4 |

Evaluator spend **USD 0.024**; A-TEXT generation + evaluation **USD 0.928**.

**Read this correctly.** It is a **directional benchmark signal on a small slice**, not a production
certification and not a population rate. The sample is small, the evaluator's own error is non-zero
and is carried on every row, and the ₹ failures cannot be cleanly attributed to the generator versus
the OCR from this evidence alone. **The Registry stays at 0** — `benchmark_qualified` is deliberately
weaker than the Registry's `qualified`/`deterministic` admission bar, and **weakening admission to
create a first row is forbidden**.
`coordination/decisions/CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md`

**EVAL-026 — temporal qualification machinery only.** 13 deterministic perturbation types covering
all 9 frozen `temporal_video` capabilities: **7 with full injected-truth coverage**, and **2 —
`action_adherence` and `camera_framing_fidelity` — negative-direction-only**, because proving a
checker notices a destroyed action does not prove it can confirm a requested one. **No temporal
evaluator is qualified, no numeric pass mark exists, and none may be invented to let a run
conclude.** Constructed stand-in material can never qualify an instrument. USD 0.
`coordination/decisions/CONTROLLER-EVAL-026-INTEGRATION-2026-08-28.md`

**RES-005 — the real temporal perturbation base.** 12 clips from 12 distinct source works, all
free and legally acquired (CC BY, CC BY-SA, CC0 or US-Government public domain), **12/12 passing the
Resources cleanliness screen** with zero pre-existing freezes, black intervals or interlacing. USD 0.

**Two limits that must not be blurred:**

- **Only a representative 3/3 clips passed EVAL-026 ingest.** The full 12-clip ingest was attempted
  and **not completed** — per-frame materialisation exhausted local disk. **This is not 12/12
  ingest.**
- **This material is not `PACK-AV-CLEAN`** and satisfies no speech/audio pack obligation. Use the
  semantic role **`MAT-TEMPORAL-BASE`**; paths containing `MAT-AV-MIN` are historical names.

**The temporal content requirement is pack-level**, not a requirement that every clip contain a
person, a product and on-screen text at once. Current opportunity counts — **coverage counts, not
statistical-precision claims** — are: general freeze/reversal base 12, multi-shot 6, on-screen text 6,
product region 5, rendered-character identity 4, photographed-face identity 3. **Rendered-character
and photographed-face identity are separate populations and must not be pooled.**

**Before any real temporal checker qualification observation:** select the actual checker; complete
the full 12-clip ingest under a recorded execution condition; freeze Controller-approved numeric pass
marks *before* observations are run or inspected; and preserve human adjudication wherever the frozen
map says `model_based_plus_human`.
`coordination/decisions/CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md`

> **A-TEXT manual review is not project evidence.** Any human re-reading of the 16 images done outside
> GitHub is not durable truth, must not be recorded here, and must not produce a Registry row unless a
> later explicit Controller decision authorises it. The accepted result is the OCR-observed 7/16.

## Still blocked / not authorised

- **Mandatory human-in-the-loop exact-text review in the production API architecture.** Withdrawn
  28 Aug 2026; not to be reintroduced without a new decision.
- **Treating benchmark-grade OCR as a perfect exactness certifier.** It is a confidence signal with
  a measured error rate, never a guarantee.
- **Registry population from text metrics — now decided, and the answer is no.** The Controller
  reviewed the sealed EVAL-029 evidence and the actual A-TEXT scoring result and ruled the Registry
  **stays at 0 rows**, because `benchmark_qualified` is intentionally weaker than the Registry's
  `qualified`/`deterministic` admission bar. **Weakening admission to create a first row is
  forbidden.**
- **Any temporal checker qualification run.** No checker is selected, no pass mark exists, and the
  full 12-clip ingest is incomplete.
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
  five disqualified, and that result stands unrewritten;
- **qualified temporal-video evaluators: 0** — EVAL-026 delivered machinery, not a qualification, and
  no numeric pass mark exists;
- empirical Registry rows: **0** (mechanically verified at GOV-006: 0 data rows, validator passes);
- customer CpAO observations: **0** — Stage C only, and Stage C is not authorised;
- Production IR and Planner: **do not exist**.

No longer zero:

- **text evaluators holding `benchmark_qualified` status: 1.** Cloud Vision `TEXT_DETECTION`, no
  language hints, on **both** Devanagari and Latin — and still **not** strict-exactness qualified;
- **A-TEXT image generations: 16**, sealed as committed bytes and scored **7/16** exact;
- recorded consumed API spend: **USD 2.6397905** through EVAL-024, plus **USD 0.024** for EVAL-030,
  against a USD 10 ceiling;
- instrument configurations scientifically disqualified under the strict standard: **5**, with a
  mechanism finding attached;
- **real temporal base material: 12 clips**, 12/12 clean, rights-cleared.

> **How solid are those figures now?** Substantially more solid than at GOV-005. The completed
> EVAL-029, EVAL-024 and EVAL-030 evidence is **sealed into Git with fingerprinted manifests**, and
> GOV-006 independently re-derived the benchmark metrics, the 6/8 · 1/8 · 7/16 arithmetic, the sealed
> artifact hashes and the manifest fingerprint from committed bytes alone. **GOV-005 finding F-1 is
> resolved for the text-OCR lane.** The mutable live ledger remains local by design, and no single
> committed artifact states a cumulative total that includes EVAL-030's USD 0.024 (GOV-006 **G6-02**).

## Next gate

**There is no active domain lane.** Every lane open at GOV-005 has settled. The next tranche is the
Controller's to open, and **no worker may infer authorisation from any of the completed task files.**

What the settled state leaves genuinely open:

1. **Registry text rows stay blocked.** The Controller has reviewed both the sealed EVAL-029 evidence
   and the A-TEXT scoring result and ruled the Registry stays at **0**. Admission semantics must not
   be weakened to manufacture a first row.
2. **Temporal qualification is not authorised** — it needs a selected checker, the full 12-clip
   ingest, Controller-approved pass marks frozen *before* observations, and preserved human
   adjudication where the frozen map requires it.
3. **Prices remain incomplete** — 0 of 4 stages is price-complete and `Frontier Clouds` is still
   unidentified.
4. **HED-1 is undecided** — which human review time counts as required cost in fully-loaded CpAO.
5. **Any tranche beyond EMP-001 needs explicit user approval.**
6. **Stream-owned staleness routed by GOV-006** — `eval/HANDOFF.md` still claims ₹0 API spend and no
   checker run (**G6-05**, escalated); `resources/HANDOFF.md` still calls RES-005 unmerged
   (**G6-04**); `canon/HANDOFF.md` omits CANON-011 (**G6-06**); the temporal spec understates the
   human-adjudication requirement as four capabilities where the frozen map says five (**G6-01**).
   These are the streams' to fix; the Governor routed them rather than editing them.

**EVAL-028 is superseded and must not be executed.**
