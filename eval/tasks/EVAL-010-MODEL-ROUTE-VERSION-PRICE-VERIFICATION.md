# EVAL-010 — Model Route / Version / Price Verification

**AUTONOMY:** autonomous  
**ENVIRONMENT:** Claude Web/cloud; GitHub + public web  
**BUDGET:** ₹0 external spend  
**BRANCH:** `work/eval-010-route-verification`

## Objective

Turn EVAL-008's candidate universe into an **execution-grade supply table** wherever current first-party/provider-authorised evidence permits.

This task verifies how selected model/workflow candidates can actually be called. It does **not** decide which models scientifically deserve Wave-1 admission.

## Read first

1. `PROJECT-MEMORY.md`
2. `coordination/CONTROL-STATE.md`
3. `coordination/decisions/CONTROLLER-FINAL-PRE-EXECUTION-FREEZE-2026-08-26.md`
4. `coordination/plans/2026-08-26-FINAL-PRE-EXECUTION-FREEZE-PROGRAM.md`
5. EVAL-008 research under `eval/model-access/2026-08-26/`
6. current model/API inventory and price template

## Core rule

**Model selection is upstream and independent.**

Do not add, remove or reprioritise candidates because they are easy/hard/cheap/expensive to access. Verify the candidate universe first. EVAL-009 separately decides the scientific Wave-1 roster.

The user's sourcing preference applies only after equivalent version/workflow identity is established:

`Frontier Clouds -> fal -> direct/other legitimate production API`

## Evidence standard

Execution-grade fields require one of:
- official model/provider documentation;
- provider-authorised API/catalogue/model page;
- official cloud marketplace/catalogue entry that identifies the exact model/version/workflow and billing unit.

Search-result snippets, blogs, leaderboard descriptions and reseller summaries are **leads only**. They may populate a leads/notes field but must not populate `verified_version`, `verified_price`, `verified_billing_unit` or `execution_ready_route`.

Unknown stays null.

## Work packages

### E10-A — Candidate identity verification

For every EVAL-008 Must/Should row verify or reject the exact claimed identity:
- canonical vendor/model name;
- exact current version or stable version identifier;
- whether the version is current, deprecated, preview, beta or scheduled for shutdown;
- whether the model name in EVAL-008 is a real public/API identity versus a benchmark/marketing/family label.

Do not silently substitute a sibling model.

Where EVAL-008 contains ambiguous identities (including but not limited to FLUX.2 [klein], LTX-2, Wan, Seedream, MiniMax/Hailuo, MAI image claims), resolve from primary evidence or keep unresolved.

### E10-B — Workflow/control verification

For each verified candidate/workflow record the supported production controls relevant to the project:
- t2i/t2v/i2v/edit/extend/compose/reference-conditioned/native AV/TTS/lip-sync/etc.;
- reference image/video/audio support and count limits;
- identity/character/product conditioning;
- masks/inpainting/edit controls;
- first/last frame controls;
- duration range/extensions;
- aspect/resolution;
- camera/motion controls;
- native audio and supported language claims where officially documented;
- seed/reproducibility controls;
- version pinning/floating aliases;
- rate/concurrency limits where public.

Record absent vs undocumented separately.

### E10-C — Frontier Clouds verification

Attempt to identify the exact service only from reliable public evidence. The user reports having credits there, but the exact provider identity is not established.

Do **not** guess.

If identified, verify every candidate version against its catalogue first.

If not identified:
- mark all Frontier cells `unresolved_service_identity`;
- preserve a ready-to-run candidate checklist;
- continue with fal/direct verification.

### E10-D — fal verification

For every candidate not execution-ready on Frontier Clouds, verify the exact equivalent selected version/workflow on fal.

Require exact model/endpoint identifiers where published.

Record wrapper limitations relative to direct vendor controls. A family-level match is not a version-pinned match.

### E10-E — direct/other route verification

For candidates not verified on preferred providers, identify the exact legitimate direct/other production route.

Record:
- API availability;
- account/enterprise/approval requirements;
- region restrictions where public;
- whether only a human UI exists rather than an automatable API;
- any material workflow difference that makes the route non-equivalent.

Do not propose bypasses or unofficial mirrors.

### E10-F — price verification

For every execution-ready route record:
- price;
- currency;
- billing unit;
- date verified;
- source;
- any resolution/duration/tier dependence;
- whether tax/credits are excluded;
- whether price is preview/introductory.

Do not normalise incompatible billing units by guesswork.

If a derived comparable cost is calculated, show the formula and preserve the source unit.

### E10-G — route-equivalence risk

Select a small number of high-value wrapper-vs-direct comparisons where the same nominal model may expose materially different controls/versioning.

Do not run models. Specify what later equivalence test would be required before evidence rows from two routes can be pooled.

### E10-H — budget inputs and user actions

Produce a machine-readable table containing only execution-grade verified values.

For every candidate return one of:
- `execution_ready_preferred_route`;
- `verified_fallback_only`;
- `identity_or_version_unresolved`;
- `route_unresolved`;
- `not_current_or_deprecated`.

Produce a concise user account/action checklist. Do not create accounts or accept terms.

If Frontier Clouds remains unidentified, clearly separate:
- nominal benchmark cost from verified routes;
- actual cash-outlay-after-credits, which remains unresolved.

## Controller corrections to EVAL-008

Do not use the reported ~99% Hindi/Bengali character-accuracy claim as verified unless a primary official source is found.

Treat every EVAL-008 price except independently reverified primary values as provisional.

A model being in EVAL-008 does not make it real/current/version-pinned. Verify identity first.

## Deliverables

Under `eval/pre-execution-freeze/model-supply/` create at minimum:
- `VERIFIED-MODEL-UNIVERSE.yaml`
- `VERIFIED-MODEL-UNIVERSE.md`
- `FRONTIER-CLOUDS-CHECKLIST.md`
- `FAL-VERIFIED-ROUTES.yaml`
- `DIRECT-VERIFIED-ROUTES.yaml`
- `WORKFLOW-CONTROL-MATRIX.yaml`
- `PRICE-VERIFICATION.yaml`
- `ROUTE-EQUIVALENCE-RISKS.md`
- `BUDGET-INPUTS.yaml`
- `ACCOUNT-ACTIONS.md`
- `EVAL-010-CONTROLLER-BRIEF.md`

## Mechanical gates

Fail if:
- selection rationale changes because of sourcing;
- a sibling/family model is silently substituted for the selected version;
- a search snippet populates an execution-grade version/price field;
- price has no billing unit/date/source;
- unavailable and undocumented are conflated;
- aggregator and direct routes are pooled despite material control/version differences;
- Frontier Clouds is guessed;
- a login/account/terms/payment action is performed;
- a partially verified supply table is described as complete.

## Restrictions

No API/model calls. No evaluator calls. No accounts, payments or terms acceptance. No Registry rows. No paid spend. No merge.

Commit and push the branch. Return the Controller brief and commit SHA only after the whole program is complete.
