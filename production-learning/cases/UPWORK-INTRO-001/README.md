# UPWORK-INTRO-001 — production-learning case

**What it is.** The first human-accepted real commercial showcase asset produced with this project's
routes and compositing discipline: a 57-s Upwork profile introduction film (V4.1, accepted by the
Controller on 14 Sep 2026). Five assembled versions, five human review cycles, 54 paid dispatches,
USD 15.39 reserved, ≈ 7 h 54 m wall clock (mechanical lower bound; Controller estimate 7–8 h).

**Two conclusions, kept apart.** Final quality: **SUCCESS**. Pipeline efficiency / time to accepted
outcome: **UNDERPERFORMED**. This case is the baseline for the next comparable production.

| File | Answers |
|---|---|
| `OUTCOME.yaml` | what was accepted, by whom, the exact asset (sha256), what it is not evidence for |
| `HUMAN-VERDICTS.yaml` | the Controller's verdict and feedback per version (chat-only evidence, transcribed) |
| `REVISION-TRACE.yaml` | V1 → V2 → V3 → V4 → V4.1: input, generation, verdict, defects with root-cause class, repair requested/made/succeeded, cost, elapsed |
| `TIME-AND-COST.yaml` | TTAO (mechanical vs human estimate, never mixed), generation wait, repair time, counts, spend by lineage and pool, CpAO lower bound, FULL CpAO proposal, the TTAO-as-KPI decision candidate |
| `SYSTEM-DEFECTS.yaml` | which failures were media-model failures and which were pipeline/orchestration/infrastructure — the big lesson (0 model failures reached the Controller) |
| `ROUTE-OBSERVATIONS.yaml` | per-model observations from this one job; `directional_production_observation`, `routing_authority: none` |
| `ACCEPTED-TEMPLATE.yaml` | the ten-beat `service_intro_with_portfolio_proof` structure and its observed pacing, all `evidence_scope: this_accepted_template` |
| `PROMOTION-QUEUE.yaml` | promoted now (eight deterministic gates) · candidate patterns · directional only · not promoted |
| `EVIDENCE-MAP.md` | every claim → path @ commit + sha256 on the raw pilot branch |

**Validate:** `python3 production-learning/tools/check_case.py --case production-learning/cases/UPWORK-INTRO-001
--pilot-ref work/pilot-upwork-intro-video-v4` (the ref check is skipped with a note when the branch is not
present locally). Ledger figures: `python3 production-learning/tools/reconcile_pilot_ledgers.py`.

**Raw evidence.** Branch `work/pilot-upwork-intro-video-v4` (V4.1 = `f6ca66f`), never merged to `main`;
inventory in `coordination/audits/UPWORK-INTRO-PILOT-EVIDENCE-INVENTORY-2026-09-14.md`.

## OUTCOME-EVENT-v1 mapping gap (documented, not fixed)

`runtime/contracts/OUTCOME-EVENT-v1.yaml` records one job → one spec → attempts on one primary route
(+ one fallback) → one acceptance, written by the runtime loop. This pilot was executed by pilot scripts
outside the runtime and is 5 assembled versions × ~25 generated assets × 9 routes × 3 billing pools, with
USD-0 assembly repairs (V4.1), a speaker qualification that is itself a mini-acceptance, sealed-media reuse
at USD 0, and five human verdicts. Fields v1 cannot carry honestly: `route` (one identity), `attempts[].slot`
(primary | fallback), `repairs[].incremental_cost_usd` for edit-only repairs, `acceptance` (one decision),
`template_candidate` (one template from five versions), `dry_run` semantics for externally executed work.
Forcing it in would fabricate structure. v1 is **not mutated**; it stays valid for the narrow Alpha chain.
A `COMPLEX-PRODUCTION-EVENT` / `OUTCOME-EVENT-v2` is queued as a design candidate in `PROMOTION-QUEUE.yaml`
(condition: a second complex real production). This directory is the durable record meanwhile.
