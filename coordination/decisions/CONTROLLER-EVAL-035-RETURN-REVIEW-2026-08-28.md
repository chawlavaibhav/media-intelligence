# Controller — EVAL-035 Return Review — 2026-08-28

## Status
**CORRECTION REQUIRED. WRITER CONTROLLER DISPOSITION.**

Reviewed:
- current main: `8d1be57d9a7734f442fcf98eef4da1321ed1c9f2`
- branch: `work/eval-035-video-route`
- branch work is one task commit based on `2995b442...`; current main has advanced by two Controller commits.

The route choice itself is accepted for the T1 substrate: **fal `fal-ai/veo3.1`, standard text-to-video, 720p, native audio**. This is infrastructure selection only, not model qualification.

No paid call is authorised by this decision.

## What is accepted from the first pass

The implementation correctly establishes:
- one injected fal queue transport;
- binary artifact persistence with SHA-256 and byte count;
- async submit/poll/result/download as one generation trial;
- no client-side retry;
- `X-Fal-No-Retry` to disable fal queue retries;
- `auto_fix: false` to prevent silent prompt rewriting;
- conservative post-dispatch accounting;
- zero network access in tests;
- a thin pilot-callable interface.

The current official fal docs independently confirm:
- queue retries are enabled by default and may reach 10 total attempts;
- `X-Fal-No-Retry` disables them;
- model fallbacks are a separate default-enabled mechanism;
- `x-app-fal-disable-fallback: true` disables fallback routing;
- Veo 3.1 `auto_fix` defaults true;
- `fal-ai/veo3.1` currently supports 4s/6s/8s and 9:16.

## Required correction 1 — disable provider model fallbacks

Current `_headers()` sends `X-Fal-No-Retry` but not `x-app-fal-disable-fallback`.

fal's official reliability/platform-header documentation states model fallbacks are enabled by default for supported models and can reroute a request to an equivalent alternative endpoint.

That violates EVAL-035's requirement for exact route/model identity and would make the persisted route claim potentially false.

Correction:
- every submit MUST also send `x-app-fal-disable-fallback: true`;
- add a test that fails if either retry suppression or fallback suppression is absent;
- document the two mechanisms separately.

## Required correction 2 — make spend authority mechanically real

Current `pilot_authorisation.py` verifies only that `decision_ref` points to an existing file under `coordination/decisions/`. Its own test demonstrates that a local authorisation file referencing the currently non-authorising pre-pilot decision can open a live `BudgetGuard`.

The docstring says decision existence is necessary, not sufficient and a future runner must inspect content manually. That is not an acceptable live-dispatch gate.

Correction:
- `open_pilot_guard` must remain mechanically closed unless the referenced committed Controller decision **explicitly authorises PILOT-001 and the exact cap/retry policy in a machine-verifiable form**;
- the current non-authorising decision must mechanically fail;
- do not infer approval from an existing decision path, account balance, credits, or a locally edited YAML file;
- no actual spend-authorisation decision exists yet, so the corrected committed state must still fail closed today.

A narrow deterministic authorisation-record format may be introduced within this pilot substrate if needed, but no spend may become enabled until a future Controller decision, after explicit user approval, supplies the matching authority.

## Required correction 3 — align attempt provenance with corrected RES-007 production records

The current EVAL-035 attempt object uses convenient local names such as:
- `prompt_sha256`
- `route`
- `model_family`
- `workflow_mode`
- `api_status`

It does not currently emit the complete production-attempt provenance RES-007 is being corrected to require.

EVAL-035 must emit or provide a deterministic adapter for the production-attempt fields needed at the pilot integration boundary, including:
- provider
- model_id
- model_version
- endpoint
- workflow
- prompt_hash
- config_hash
- config_location
- reference_asset_hashes
- requested_at
- completed_at
- lane
- repeat_index / repeat_of_attempt_id
- retry_of_attempt_id / retry_reason
- status
- cost_ref
- storage_class

Production attempts do not fabricate `eval_item_id`, per the RES-007 Controller correction.

Do not duplicate Resources' writer. The goal is a lossless, explicit handoff shape so PILOT-001 does not need ad-hoc field translation after the call.

## Required correction 4 — branch/scope hygiene

- Rebase/update the task branch onto current `main` before final review.
- Remove the top-level `.gitignore` modification from the Eval worker branch; stream workers should not modify the repository root for a task-local runtime file.
- If an ignore rule is needed, place a task-local `.gitignore` under `eval/pilot-substrate/`.
- No remote `rescue/res-007-duplicate-from-eval-035` branch exists, so no Controller cleanup action is required for that local rescue ref.

## Required correction 5 — do not require a throwaway paid smoke generation

The worker recommended a separate 4-second real dispatch before the real pilot generation.

Controller disposition: **do not create a separate paid smoke-test tranche by default.**

The first authorised provider call should be a real PILOT-001 production unit/shot chosen so that an early transport failure is still useful pilot evidence. If later execution-time verification reveals a reason a dedicated smoke call is necessary, bring that decision back with its incremental cost before spending.

## Tests / review gate

The correction must add/retain tests proving:
- retry suppression header present;
- fallback suppression header present;
- `auto_fix=false`;
- current non-authorising decision cannot open a live pilot guard;
- future machine-verifiable authority is required;
- complete production-attempt provenance can be handed to RES-007;
- binary artifact handling remains intact;
- no network by default;
- no retry/resubmit on ambiguous failure.

After correction, EVAL-035 is eligible for bounded Level-1 Governor review.

## Spend posture

USD 0 remains authorised for EVAL-035.
Real generations: 0.
PILOT-001 paid execution remains unauthorised.
