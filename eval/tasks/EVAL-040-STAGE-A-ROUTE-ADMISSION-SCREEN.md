# Task EVAL-040: Stage A — route admission screen (Tranche 1a / 1b)

**TASK ID:** EVAL-040
**STATUS:** DRAFT — **PENDING SPEND AUTHORISATION.** May not execute until (a) `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` is ratified, (b) EVAL-039's freeze package is accepted by the Controller, and (c) a separate Controller spend record names the exact routes, call counts and hard cap, recorded verbatim before the first paid call (the EVAL-038 / DN-07 pattern).
**OBJECTIVE:** For every scientific question in the plan, learn which current routes deserve deeper spend — and write the first deterministic Registry rows and Capability Map v0 — from ≈ 250 generations judged blind against pre-registered rules.
**WHY WE ARE DOING THIS:** The product must answer "for requirement X under conditions Y, which route, what fallback, what cost, what failure modes". Stage A is the smallest experiment that turns a stale roster into a ranked, condition-tagged survivor set without spending on routes that fail the basics.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`.

## CONTEXT CONTRACT

**Inherits `shared/CONTEXT-SUFFICIENCY-POLICY.md`.**

### BASE STATE
- **BASE MAIN SHA:** the `main` that carries EVAL-039's merged freeze package (to be filled at authorisation).
- **ACCEPTED DEPENDENCY SHA(s):** the freeze package fingerprint from EVAL-039; the spend record.

### REQUIRED ORIENTATION
Default bootstrap; `coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md` §C–§F; the spend record.

### TASK-SPECIFIC CONTEXT
- `eval/empirical-planning/STAGE-A-FREEZE-2026-09/` — items, acceptance contracts, elimination rules E1–E5, seed policy, evaluator plan, judging protocol, cost table. **Byte-frozen; any change is a new task.**
- `eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml` and the price pins.
- `eval/v1/harness/harness.py`, `eval/registry/SCHEMA-v1-draft.yaml` — Registry writer and row shape (`n_items`, `repeats_per_item`, `uncertainty`, `absence_reason` mandatory).
- `eval/experiments/EVAL-038/JUDGING-PROTOCOL.md`, `tools/strip_blind.py` — blind-judging precedent.
- `canon/gate/run_gate.py` — `post` mode as a zero-cost structural check per artifact (observation only).

### EVIDENCE HANDLING LEVEL
`row_level_evidence` — every trial is a committed record: request, response metadata, artifact bytes (sealed pattern), ledger entry, instrument outputs.

### CONTEXT INSUFFICIENCY
If a route's live price at dispatch differs from the pin, or the ledger cannot reserve, **refuse the dispatch** and report; never proceed on an estimate.

**IN SCOPE:**
1. **Tranche 1a** — image core (6 routes × 4 items × 2), exact-text set (4 routes), edit-preservation set (4 routes), reference set product/person (4 routes); text-to-video core (6 routes, Seedance 2.5 at 4 gens) including the Hindi native-dialogue item, the high-motion item and the policy-edge item; VID-05 cost-knee tiers. ≈ 164 generations.
2. **Blind Controller acceptance of 1a** → selection of the shared hero still for 1b.
3. **Tranche 1b** — image-to-video (5 routes), reference-to-video (2–3 routes), multi-shot (3 routes), TTS (2 routes × 3 scripts × 2), lipsync (2 routes × 3 × 2, plates and drives reused from 1a/1b outputs). ≈ 82 generations.
4. Evaluator fan-out per the frozen plan: deterministic instruments on every trial; Cloud Vision on text items; ASR-vs-script on TTS/dialogue; `run_gate.py post` on every artifact (structure only); VLM triage labelled `screened_not_qualified`.
5. Apply E1–E5 mechanically; publish the survivor table per question.
6. **Registry rows** — only from `deterministic` instruments, written by the harness: `latency_errors_refusals`, `delivery_format_compliance`, `cost_and_cpao` (trial cost; CpAO `absence_reason: not_applicable`), `reproducibility`, `reliability_pass_at_k` where a deterministic criterion exists, `edit_preservation` on IMG-03 items; `uncertainty.status: computed`, `independence_status: NOT ESTABLISHED`, `n_items` explicit.
7. **Capability Map v0** — `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml`: every route × question × condition cell with tier, n, date, price pin, refusal rate, failure modes (observer's own words), and fallback.
8. Sealed evidence + spend ledger committed; Controller Brief with OBSERVED / INFERRED separated and the Stage B candidate survivor list.

**OUT OF SCOPE:** Stage B items or sweeps; any Stage C outcome attempt; any CpAO claim; any Registry row from a benchmark-grade, human, or screened instrument; any conclusion on Canon; retries; changing an item, route or rule after the first paid call; Runway (no account) unless the Controller opens one.

**AUTONOMY MODE:** autonomous within the spend record; the judging steps are the Controller's.

**RESOURCE BUDGET:**
- API spend: **hard cap to be set by the spend record** (plan proposes USD 175: 1a ≤ 60, 1b ≤ 115); 0 retries; reservation-before-send; execution-time price verification against the pin; stop at cap without exception.
- generations: ≈ 246 (exact count from the freeze package); evaluator calls per the frozen plan.
- Controller time: ≈ 2.5 h blind acceptance.

**APPROVED DEPENDENCIES:** EVAL-039 merged and accepted; the spend record; CANON-GATE-001 merged.

**STOP CONDITIONS:** cap reached; price mismatch at dispatch; ledger reservation failure; a provider refusal pattern that suggests a policy block on the account (report, do not probe); any instrument raising a harness invariant error.

**HUMAN APPROVAL TRIGGERS:** the spend record itself; hero-still selection after 1a; any proposal to add a route mid-run (refused — new task).

**RESULT LOCATION:** `eval/experiments/EVAL-040/` (runs, media, ledger, judging), `eval/registry/registry-v1.jsonl` (appended by harness only), `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml`, `eval/tasks/EVAL-040-CONTROLLER-BRIEF.md`, branch `work/eval-040-stage-a`.
