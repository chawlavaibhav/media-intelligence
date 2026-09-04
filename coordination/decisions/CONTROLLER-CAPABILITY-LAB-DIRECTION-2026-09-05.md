# Controller — Capability Lab Direction: Empirical Model/Workflow Battery — 2026-09-05

**Status:** DRAFT — PENDING CONTROLLER RATIFICATION. Written by the Writer Controller session on
2026-09-05 from the human Controller's direction; it becomes a durable decision only when the
human Controller ratifies it and the carrying branch is merged. Until then
`coordination/CONTROL-STATE.md` governs.
**Role:** Writer Controller.
**Base `main`:** `599ff4af6a1f0684132303687e438877da47a004`.
**Plan adopted by this decision:** `coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md`.

## 1. Authority — the Controller's direction, in the Controller's words

> "I am now explicitly changing direction. My current direction is: I want to move into extensive
> empirical model/workflow testing. I am keen to run the battery properly and determine which
> current model/workflow works best for which use case and under which conditions. Treat this as
> a new Controller input requiring proper durable disposition before execution. Do not silently
> reinterpret or erase the prior decision. Supersede/amend it explicitly where necessary."

and, later in the same session: "have to start testing now. we may not necessarily go with the
proposed methodology."

Further Controller inputs in the same session (transcribed from a voice note; punctuation added):

> "You have access to AWS, GCP, and Azure … look for image and video models that we are looking
> to test, if they are available on cloud. If yes, then we will use them … against credits.
> Second, whatever test we have to do, form a plan, form a budget. fal, Gemini key, and Anthropic
> keys are there already. Third … when we are testing, we eventually want a weaker LLM plus
> weaker media model to beat the strongest media model plus strongest LLM combination. That's
> where the win is. So if we are saying … Gemini nano models are best at text rendering, and if
> you're able to produce text rendering via RGN, via one of the cheaper models, in a video,
> preferably I would go that way."

## 2. What this decision supersedes, amends, or preserves

| Prior record | Disposition |
|---|---|
| `CONTROLLER-PROGRAMME-RESET-MEDIA-FACTORY-PRIORS-2026-08-29.md`, immediate queue item 4 — *"Do not generate any new media before T2B unless the user explicitly changes direction"* | **SUPERSEDED.** The user has explicitly changed direction. T2B's programme-direction question was answered by `CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`. |
| Same record — *"The USD 25 T2 workflow/model screen remains declined and must not be revived under another name"* | **SUPERSEDED, stated plainly.** A model/workflow screen is now the programme's centre. It is not the August design revived by stealth: it is a route-comparison screen per scientific question with pre-registered elimination rules and tiered evidence, and the Controller reverses the earlier refusal knowingly. |
| Same record — T2A (EVAL-036) as prerequisite; T3 / T4 Canon media-propagation and cost-compression; T5 targeted freshness only | T2A **re-scoped** to a compact hashed import inside EVAL-039. T3 / T4 **deferred, not cancelled**. T5 **replaced** by the staged campaign. |
| Same record — historical prior ≠ Registry row; no generate-vs-deterministic dogma; the seven settled priors are not re-proven from zero | **PRESERVED verbatim.** |
| `CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`, `CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`, `CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md` | **PRESERVED.** The verdict on whether Canon works remains reserved to the Controller. The refuted substitution configuration stays closed. CANON-SHAPE-v1 remains the governing consumption shape; Canon's role is doctrine, compiled mechanical checks, and later templates — not the programme's centre. Battery evidence will show which missing packs are worth compiling. |
| `CONTROLLER-STOP-TEMPORAL-PREP-PRIORITISE-PRODUCT-PILOT-2026-08-28.md` | **PRESERVED**; its reopening condition ("automated temporal-evaluator qualification is again the objective") is met when Stage B needs temporal instruments, and is then reopened under a **new** task id, never by resurrecting EVAL-032/033. |
| `CONTROLLER-DIRECT-GEMINI-T1-ROUTE-REVISION-2026-08-28.md` | **PRESERVED** for Google models (direct Gemini API). Non-Google routes execute via fal. |
| `CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md` (admission must not be weakened to create a first row; benchmark-grade text metrics do not populate the Registry) | **PRESERVED without exception.** |
| CANON-GATE-001 authorisations and rulings 1–9 | **UNTOUCHED.** The gate merge proceeds in its own sequence; this decision waits for it before `CONTROL-STATE.md` is amended. |

## 3. Decisions

1. **Programme centre.** After CANON-GATE-001 lands, the programme is centred on the Capability
   Lab: a staged empirical battery whose output is a **conditional routing map**, not a
   leaderboard. The staged grammar (Stage Q → A → B → C; one call = one trial; repeat ≠ retry;
   generate once, score every eligible dimension; sparse sweeps; Registry only from qualified or
   deterministic instruments) is reused unchanged.
2. **Structural amendment to the roster.** Scientific slots remain *questions*. Stage A screens
   **several current routes per question** on the same frozen comparability core, because the
   objective is *which route under which condition*, not *is one route viable*. Stage B keeps the
   August depth on at most three survivors per question. Elimination rules are pre-registered in
   the freeze package before the first paid call and are not changed mid-run.
3. **Roster refresh is mandatory before spend.** No August candidate identity, endpoint, or price
   is assumed current. EVAL-039 pins every id and price with fetched bytes and a date; promotional
   prices are recorded but never used for CpAO.
4. **Three evidence tiers, kept apart.** *Deterministic* and *qualified* instruments may write
   Registry rows. *Benchmark-qualified* instruments (Cloud Vision text OCR; ASR against known
   scripts) and *blind human acceptance* produce product evidence with stated error or n.
   *Unqualified machine judges* produce triage only, labelled `screened_not_qualified`.
   *Historical priors* stay freshness-flagged. An unqualified evaluator never prevents
   generation; it only prevents a Registry claim from that dimension.
5. **Capability Map ⊇ Registry.** A tiered `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml` is
   the product asset the Planner reads; the Registry remains its strict subset and its admission
   bar is unchanged.
6. **Spend is authorised one tranche at a time**, each by its own record naming exact models,
   call counts, and a hard maximum consumed spend, with 0 retries and execution-time
   route/price verification — the same discipline as EMP-001 and EVAL-038. Proposed ceilings:
   Tranche 1 (Stage A) USD 175 split 1a ≈ 60 / 1b ≈ 115; Tranche 2 (Stage B) USD 250; Tranche 3
   (Stage C) USD 150. **None is authorised by this decision.**
7. **Production IR and Planner v0** are extracted from Stage C's accepted recipes and from the
   Capability Map, not designed in the abstract first.
8. **Canon in this campaign:** the compiled-doctrine gate runs as a zero-cost structural post-draw
   check on every trial and its agreement with human acceptance is *recorded as observation*.
   No worker draws a verdict on Canon from it.
9. **Provider surface — cloud credits first.** Where a candidate model is available on AWS
   Bedrock, Vertex AI or Azure AI Foundry and billable against that cloud's credits, the battery
   runs it there; otherwise on fal; Google models on the direct Gemini API or Vertex. The surface
   is part of the Registry row. Cash and credits are ledgered separately; tranche caps are
   USD-equivalent ceilings across both pools. The read-only survey
   `eval/empirical-planning/CLOUD-MODEL-AVAILABILITY-2026-09-05.md` is the input; EVAL-039 records the
   chosen surface per route. Accounts are the Controller's; workers create nothing.
10. **Headline hypothesis H-CHEAP** (plan §C.3b): a cheap stack plus the intelligence layer beats
    the frontier stack on accepted-outcome rate at lower CpAO. Stage C's two recipes are cheap
    stack + intelligence layer vs frontier stack. The cheap exact-text topologies TOPO-02 /
    TOPO-03 (text by a cheap image route → cheap image-to-video, vs premium native, vs
    deterministic composite) are in Tranche 1, not deferred. This does not reopen EVAL-038 and
    implies no verdict on Canon.

## 3a. Execution method and two design rules (Controller, 5 Sep, later in the session)

Controller's words: *"spin off agents — planner who writes tasks, execution who executes it, tester,
auditor and approver. Before anything is spent, one of the first tasks is to look at the test
holistically and write down the model test cases really well. Prompts should look like customer
prompts. Also, all productions must use Canon knowledge."*

11. **Five-role pipeline for every campaign task**: Planner (writes the task and acceptance
    criteria; writes no deliverable), Executor (produces the deliverable; changes no scope),
    Tester (runs validators and checks the deliverable against the task's acceptance criteria),
    Auditor (adversarial review against doctrine, contracts and evidence rules; reports, does not
    fix), Approver (PASS / PASS WITH NOTES / BLOCK on the merge line). Roles run in sequence with
    separate contexts; no role approves its own work; the human Controller reviews between the
    Planner and the Executor and before merge. Agents run one at a time on this machine.
12. **Test cases are customer-shaped.** Every Stage A item is written the way a real buyer writes
    to a studio — WhatsApp or email register, Hindi / Hinglish / English as the market dictates,
    with the customer's own constraints and attachments — and is mapped to a Normalized Request
    under the CANON-010 grammar. Benchmark-style prompts ("isolated probe for capability X") are
    not admissible as items.
13. **All productions use Canon.** For each test case one production blueprint is authored under
    `canon/CANON-SHAPE-v1.md` §4 (deterministic pack lookup, compiled packs as the doctrine, check
    lines applied before dispatch) and **frozen**; then every candidate route executes that same
    blueprint. The blueprint is held constant across routes so the comparison remains a comparison
    of routes. The blueprint author (model or agent) is recorded on each case. This measures
    routes under Canon-shaped production; it still draws no verdict on Canon.
14. **First pipeline task**: the holistic Stage A test-case package (EVAL-039A), at USD 0 provider
    spend, before any spend authorisation is written.

## 4. Authorised by this decision (USD 0)

- **EVAL-039** — September-2026 roster, price and route-liveness refresh; compact Media Factory
  prior import; harness adapters for fal video/audio/lipsync; Stage A freeze package (items,
  acceptance contracts, seed policy, elimination rules, evaluator plan, exact cost); Q1
  deterministic-geometry qualification run; the deterministic instruments listed in the plan.
  Network fetches for pinning are authorised; **no paid provider call of any kind**.
- **EVAL-040** exists as a task file in status *PENDING SPEND AUTHORISATION* so that the freeze
  package has a named home; it may not execute until a separate spend record is written.

## 5. Not authorised by this decision

Any paid call, generation, or evaluator spend; any Registry row from anything other than a
`deterministic`/`qualified` instrument; any weakening of admission; Production IR or Planner
implementation; compilation of further packs; any conclusion about whether Canon works; any
change to `coordination/CONTROL-STATE.md` before the CANON-GATE-001 merge lands; any edit to the
gate branch or its files.

## 6. Controller actions requested (human only)

1. Ratify or amend this decision and the plan (methodology is open).
2. Say whether a Sarvam AI key already exists (AUD-01) and whether a Runway account should be
   opened (VID-04) — the Controller pre-creates accounts; nothing is created by workers.
3. Decide whether Stage C's second recipe is the CANON-SHAPE-v1 blueprint + gate path (doubling as
   the reserved acceptance-rate measurement) or a plain second topology.
4. HED-1 before Stage C's fully-loaded CpAO.

## 7. Overnight execution mode (Controller, 5 Sep, ~01:45 IST)

Controller's words: *"complete the tasks. I don't authorise spends till I give approval. Just create
plans, build access, projections and everything. Will approve in the morning. Build async. Don't
destroy anything. Will not be available to resolve queries for 5–6 hours."*

Binding for every agent in this window: USD 0 provider spend of any kind; no deletion, overwrite of
committed evidence, or force-push; reversible access steps only (requesting Bedrock model access,
enabling a Vertex API) and each one logged; anything needing the Controller (Ashva Azure sign-in,
deployments, spend) is written down as a morning decision, never attempted. The Writer Controller
session reviews between roles in the human's absence; the human ratifies in the morning.

### 7a. Cloud accounts and fresh resources (Controller, 5 Sep, ~01:50 IST)

Controller's words: *"getaight tenant in azure, yes, yes. can you rather create fresh resources in
all three clouds — where the APIs are kept. it will save polluting existing projects."*

Read as: Azure = the getaight subscription `b832f4a1-…` (not Ashva); AWS account `528730633804` and
GCP project `vertexaiproject-507518` confirmed as the credit-bearing accounts. Workers may create
**new, isolated, zero-standing-cost** resources dedicated to this battery — an Azure resource group +
AI Services resource with pay-as-you-go model deployments; a dedicated AWS IAM identity scoped to
Bedrock with its own key; a dedicated GCP service account (or a new project if the credentials and
billing link allow it unambiguously) — and store their keys under `~/.mi-battery-keys/` (mode 600)
without ever printing a value. Nothing existing is modified or deleted; the Wherehouse subscription
`d3ee8dc2-…` is never touched. Every creation is logged with the exact command.
