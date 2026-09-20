# RentOK game video — two-lane live experiment: EXPERIMENT CONTRACT

Opened: 2026-09-20 (IST evening) by the Media Intelligence Controller session (Claude Opus 5, local desktop), acting as **Writer Controller for this experiment's records only** — on the experiment branches below; `coordination/**`, `canon/**`, `eval/registry/**`, `eval/capability-map/**` and sealed evidence are never mutated by this experiment. Human Controller (release and spend authority): Vaibhav Chawla.

## 1. Operational state at opening (OBSERVED)

- `origin/main` = `4d919c9df6c9725a2f14c411771565bb09089876` (local `main` at `3bb9a3c`, one commit behind; the working tree of the main checkout carries the **untracked** `coordination/audits/AUDIT-2026-09-16-ARCHITECTURAL-AUDIT/` — left untouched; this experiment uses fresh worktrees so the `/media-agency` §0 clean-tree rule holds).
- No other session is executing on this programme (the audit session `local_d0f145a4…` is idle since 17:24Z; the Cumin experiment jobs A/B are closed — REJECT recorded, branches committed, not pushed).
- Implemented and reused as-is: `/media-agency` skill v1 (BOOTSTRAP, PRODUCTION-WORKFLOW, QA-CHECKLIST, JOB-TEMPLATE); the paid-dispatch mechanism proven on jobs 001/002/003 and the Cumin experiment (`agency/jobs/AGY-2026-09-20-CUMIN-EXP-B-FIVESTAGE-001/tools/dispatch.py` + `_common.py` on `work/agency-job-cumin-exp-b-fivestage @ 5c33173`: per-job append-only ledger, cap check before every request, `runtime.execute.provider_errors` classification, live PriceBook quotes); runtime gates (`runtime/compositor/gates.py`, `runtime/loop/frame_hygiene.py`, `canon/gate/run_gate.py`); the routing map + taint register (61 cells, regenerated 14 Sep); the two compiled Canon packs; accepted Canon (37 sources) readable by id under `canon/knowledge/current/**`; production-learning cases 001–002 on main (003 on PR #103).
- **Specified but not implemented as code:** Canon *interrogation* (Addendum A: "the system asks none, by design" — lanes interrogate Canon by reading accepted claims by id and recording what was retrieved); QUESTION-TEMPLATE v0.1 (a specification, "not yet wired into /media-agency" — applied by hand, as the Cumin Job B did); the Stage Controller / independent checker (realised here as separate fresh-context sessions).
- Pool balances: Google credits are **not machine-readable** by the project service account (Cloud Billing API disabled for `vertexaiproject-507518`; verified 2026-09-20). fal is excluded by instruction. Balances are therefore attested by the human Controller in the spend record, and every reservation is an upper bound.
- Spend authority at opening: **absent** (CONTROL-STATE §6: any new paid dispatch needs explicit approval in writing; `/media-agency` BOOTSTRAP §3: only a cap stated by the user in this session counts). Filled in §6 below when given.

## 2. Design

Two isolated production lanes from the same frozen customer brief (`01-CUSTOMER-BRIEF-FROZEN.md`), the same frozen product-source snapshot (`source/rentok-snapshot/`), the same frozen Canon (`origin/main @ 4d919c9`, `canon/knowledge/current/**` + the two compiled packs), the same routing evidence, the same acceptance contract (`03-ACCEPTANCE-CONTRACT.md`), the same budget.

| | Lane A — autonomous | Lane B — ChatGPT-directed |
|---|---|---|
| Creative starting point | brief + confirmed answers only | brief + confirmed answers + `02-CHATGPT-DIRECTION-LANE-B-ONLY.md` (a proposal to verify and refine, not a contract) |
| Job id | `AGY-2026-09-20-RENTOK-GAME-LANE-A-001` | `AGY-2026-09-20-RENTOK-GAME-LANE-B-001` |
| Branch / worktree | `work/agency-job-rentok-game-lane-a-001` / `../media-intelligence-rentok-lane-a` | `work/agency-job-rentok-game-lane-b-001` / `../media-intelligence-rentok-lane-b` |
| Sees the other lane | never, before its own production package is frozen | never, before its own production package is frozen |
| Sees the ChatGPT direction | **never** | yes |

The difference under test is the creative starting point. The experiment compares two complete creative-production approaches; it does not isolate Canon interrogation as a causal variable, and n = 1 customer job establishes no general winner.

## 3. Protocol per lane (five stages; QUESTION-TEMPLATE v0.1 applied by hand)

Producer session (one per lane, fresh context, sees only its own lane inputs) writes per stage: questions (only consequential ones), why each matters, class (DET/RSR/LJ/HJ/EMC) and priority, answer source, retrieved evidence, answer or `unresolved`, resulting decisions, assumptions, stage exit criteria. A **checker session** (fresh context, never the author) records a verdict at Gate 1 (intent contract preserves the customer's words), Gate 3 (creative package vs brief and question records; refuses to close without a numbered hero frame and every mandatory event on a numbered board frame), and Stage 5 (verification + failure classification to the earliest affected stage). Gate 2 and Gate 4 are checked by the same checker session as Gate 3 (structure ↔ contract ↔ evidence compatibility; riskiest capability tested first; every route priced from the live PriceBook with evidence status). Frozen creative package and frozen production plan are committed on the lane branch **before** any paid call.

Both lanes are told: the customer will not be asked further questions; the deliverable is produced by generative models and code (no live filming); no fal; no personal payment methods; credits pools only (Google Vertex/Gemini credits, ElevenLabs plan credits, Sarvam credits); exact/critical text composed by code by default (mechanism B) unless the lane records why in-model text is required and covers it with evidence; mandatory customer requirements verified by code where a check can be deterministic.

## 4. Isolation mechanics

- Separate worktrees, branches, job ids, ledgers, tools and QA folders. The Lane A worktree contains no copy of the ChatGPT direction; the Lane A producer's and checkers' prompts never contain or reference it. The Lane B worktree contains no Lane A file.
- The Controller reads both lanes but writes nothing into either lane's creative records.
- The blind packet (`05-BLIND-PACKET/`) carries `video-X.mp4` and `video-Y.mp4` with the lane→label mapping sealed in `05-BLIND-PACKET/MAPPING.sealed` (sha256 published; the mapping opened only after both verdicts are recorded verbatim).

## 5. Budget and spending control

- Equal caps per lane, credits only, no transfer between lanes, no hidden retry; every paid call (success, refusal, transient failure) is one ledger line reserved before the request leaves. Includes generation, retries, reference assets, micro-qualification draws, music, TTS. Rendering/assembly by code is USD 0.
- The earlier USD 5-per-lane Cumin experiment authorises nothing here.
- Recorded in §6 once given in writing by the human Controller; until then Stages 1–4 run at USD 0 and Stage 5 does not start.

## 6. Spend authorisation of record

RECORDED — `SPEND-AUTHORISATION.md`: USD 10.00 per lane, credits only, 0 hidden retries, Google credits pool attested funded by the human Controller (answers verbatim in that file).

## 7. Deliverables

A. two finished videos (one per lane, anonymised for the customer) · B. five-stage evidence per lane on its branch · C. production evidence (ledger, attempts, artifacts by sha256, tool versions, repairs, limitations) · D. blind packet · E. Controller comparison after verdicts (`06-CONTROLLER-COMPARISON.md`).

## 8. Blindness limitation recorded before presentation (2026-09-20T20:00Z)

During the run the Controller session reported per-lane facts to the human in chat (spend, attempt counts, the presence/absence of a voice, and that one lane's file measures 30.021 s). A human who remembers those messages could infer a video's lane from its duration, its file size or the presence of a voice-over. The packet therefore is blind as to labels and metadata, but not against the human's memory of this session's progress reports. Recorded here so the comparison does not overstate the blindness; the human is asked to judge on the acceptance contract, not on provenance.
