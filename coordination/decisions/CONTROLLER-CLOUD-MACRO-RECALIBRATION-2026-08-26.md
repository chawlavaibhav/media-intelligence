# Controller Decision — Cloud Macro Recalibration

**Date:** 26 Aug 2026  
**Status:** APPROVED  
**Environment:** fresh Claude Web/cloud sessions; no laptop access assumed

## Decision

The previously assigned Pre-E7 stream packets are **superseded before execution**:

- `canon/tasks/CANON-PRE-E7-SCOPE-AUDIT.md`
- `eval/tasks/EVAL-PRE-E7-SCOPE-REBASE.md`
- `resources/tasks/RESOURCES-PRE-E7-SCOPE-REBASE.md`

Do not execute their branches as the active program.

Their core architectural finding remains accepted: capability evidence needs explicit production conditions, and customer outcomes may contain many production steps/calls/artifacts. What is superseded is the method of discovering scope primarily by auditing the Controller-authored 30-brief bank.

## Why the plan changed

The project needs to understand recurring **media-generation request patterns** before refreezing its benchmark. Public evidence now provides a much stronger discovery surface than 30 synthetic briefs:

- DiffusionDB: 1.8M unique real-user text-to-image prompts — https://aclanthology.org/2023.acl-long.51/
- VidProM: 1.67M unique real-user text-to-video prompts — https://arxiv.org/abs/2403.06098
- TIP-I2V: 1.70M unique user-provided text+image prompts for image-to-video — https://openaccess.thecvf.com/content/ICCV2025/html/Wang_TIP-I2V_A_Million-Scale_Real_Text_and_Image_Prompt_Dataset_for_ICCV_2025_paper.html
- Arena Image categories derived after analysing 4M+ user prompts, including Product/Branding/Commercial Design and Text Rendering — https://arena.ai/blog/image-arena-improvements
- Artificial Analysis explicitly separates real-world use cases from model capabilities and refreshes prompts over time — https://artificialanalysis.ai/image/methodology
- GenEval 2 documents benchmark drift and the need for continual benchmark audits — https://arxiv.org/abs/2512.16853

These sources do not by themselves define our product. They establish that request-space research and use-case/capability separation are feasible and that static benchmarks age.

## New discovery order

1. **Observed request space** — recurring structures in real media-generation usage.
2. **Technical capability/failure space** — what generation/evaluation research and current workflows show can vary or fail.
3. **Evidence/supply space** — what independent material, lineage, rights and persistence are needed to measure those things honestly.
4. **Controller integration** — only then freeze request grammar, capability v2, conditions, outcome topology, benchmark design and acquisition plan.
5. **Empirical execution later** — evaluator qualification, targeted resource acquisition, Canon value gate and paid model benchmarking require a new Controller authorization after integration.

## What remains accepted

- Product goal: API-native media production intelligence optimising Cost per Accepted Outcome.
- Normalized Request != Creative IR != future Production IR.
- Canon knowledge != empirical model capability.
- Current 19-source Canon remains accepted.
- Current 36 Eval capabilities and 100-item bank remain useful **baselines**, not final scope proof.
- Six evaluator-family architecture remains a baseline.
- Generate once / measure many.
- One provider/API/transform call = one trial.
- Repeat != retry.
- Resources V2.1 attempt/artifact/measurement/cost persistence remains accepted.
- Registry stores evidence, not routing scores.
- EVAL-006 remains PAUSED — DO NOT EXECUTE.

## Cloud-session restrictions

Across all three new programs:

- ₹0 external spend;
- no generator/checker/evaluator API calls;
- no empirical Registry entries;
- no source ingestion into Canon;
- no materially new dataset/media acquisition;
- no login, account creation, payment, click-through terms or access-control bypass;
- no assumption of laptop files, raw git-ignored corpus, local API keys or Downloads;
- public web research and small public metadata/document inspection are allowed;
- code may be run only if the cloud session actually provides a runner; otherwise mark runtime verification honestly;
- workers may research and **propose** architecture/schema changes but may not unilaterally freeze cross-stream architecture.

## Active macro programs

- Canon: `canon/tasks/CANON-009-CLOUD-SCOPE-PROGRAM.md`
- Eval: `eval/tasks/EVAL-007-CLOUD-EVAL-RESEARCH-PROGRAM.md`
- Resources: `resources/tasks/RES-003-CLOUD-EVIDENCE-PROGRAM.md`
- Shared program: `coordination/plans/2026-08-26-CLOUD-MACRO-SCOPE-AND-READINESS-PROGRAM.md`

All three terminate at one Controller integration gate. No later paid/execution queue is pre-authorized.
