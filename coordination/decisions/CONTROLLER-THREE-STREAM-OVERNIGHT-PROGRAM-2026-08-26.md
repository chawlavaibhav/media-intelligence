# Controller decision — coordinated Canon / Eval / Resources overnight program

**Date:** 26 Aug 2026  
**Status:** APPROVED FOR USER ASSIGNMENT

## Decision

The prior task-by-task direction is replaced, for future work, by one coordinated V1 program across Canon, Eval and Resources.

The authoritative planning documents are:

- `coordination/plans/2026-08-26-THREE-STREAM-OVERNIGHT-PROGRAM.md`
- `coordination/plans/2026-08-26-CLOUD-SESSION-BOOTSTRAP.md`
- `canon/tasks/CANON-V1-OVERNIGHT-PROGRAM.md`
- `eval/tasks/EVAL-V1-OVERNIGHT-PROGRAM.md`
- `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md`

The user intends to assign the three stream runbooks independently. **A stream may begin only when the user explicitly assigns that stream's runbook.** Once assigned, the worker may execute every work package marked `RUN TONIGHT` autonomously within the runbook's boundaries and stop conditions.

## Cloud-session execution interpretation

The intended overnight workers are **fresh cloud/browser sessions with zero prior chat context and no access to the user's laptop**. `coordination/plans/2026-08-26-CLOUD-SESSION-BOOTSTRAP.md` is the authoritative execution interpretation for this environment.

Workers must not assume access to laptop-only raw media, Downloads, local books/archives, local environment variables/API keys, or prior hidden/chat context. If a runbook instruction presumes a local code runner or laptop payload that is not available in the cloud session, the worker must complete all independent design/research work, label runtime/raw-byte verification honestly as unavailable in that session, and must not claim it reran checks it could only cite from committed repository evidence.

Before editing, every fresh worker must read the bootstrap sequence and post the required startup acknowledgement explaining: its role, end-state, quantified starting state, tonight's work, prohibitions, cloud constraints and morning deliverable. **It then continues immediately without waiting for a reply.**

Specific consequences:

- **Canon C1–C4** are expected to be substantially cloud-executable from committed Canon evidence plus public web research; local book/PDF access is not required because no ingestion is authorised tonight.
- **Eval E1–E4** are cloud-executable; **E5** may be implemented/tested only to the extent the cloud session actually exposes a code runner. Laptop credentials are `not_visible_to_cloud_session`, not evidence that the user has no credentials.
- **Resources** may rebaseline the 34,786-item corpus from committed manifests/reports/source records but may not claim to re-decode/re-hash the git-ignored 5.70 GB raw corpus in cloud. R5 views are logical manifests over committed evidence, not proof that raw payloads are present in the cloud session.

## EVAL-006 disposition

`EVAL-006` remains **PAUSED — DO NOT EXECUTE**. Its historical file remains intact. Its previous checker/model/Registry bootstrap and ₹16,000 spend authority are withdrawn and are not revived by this decision.

The new Eval program supersedes its execution approach. No paid Eval empirical task is authorised by the overnight program.

## Overnight financial/access boundary

All three overnight tranches are **₹0 external API/source spend**.

Not authorised tonight:

- paid model/checker/generation calls;
- any empirical Capability Registry score;
- purchases, subscriptions or course enrolment;
- login/account creation, gated-source access, click-through terms or forms;
- materially new Resources acquisition;
- new Canon ingestion;
- invented human judgement;
- Production IR or Planner/routing implementation;
- merge to `main` by a domain worker.

## Parallelism and ownership

Workers use isolated branches:

- Canon: `work/canon-v1-overnight`
- Eval: `work/eval-v1-overnight`
- Resources: `work/resources-v1-overnight`

Shared ownership rules:

- Canon owns the 30-underlying-brief commercial bank.
- Eval owns the 36-capability measurement contract and 100-base-item capability bank.
- Resources owns evidence/reference packs, role allocation, rights/integrity/lineage and empirical artifact preservation.
- Eval's later 12 end-to-end production briefs must be selected from Canon's 30-bank after integration; Eval must not create a competing commercial brief bank.
- Canon and Eval share one Resources commercial-creative bank for later creative-evaluator/Canon-critique work.

## Morning gate

No paid empirical run, source ingestion, or materially new acquisition begins automatically when an overnight worker finishes.

Morning Controller review must reconcile the three branches, verify the interfaces, and explicitly authorize the next empirical/acquisition/ingestion tranche.
