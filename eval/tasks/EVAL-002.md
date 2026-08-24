# Task EVAL-002: Calibration & benchmark readiness

**TASK ID:** EVAL-002

**OBJECTIVE:** Turn the Controller-approved EVAL-001 measurement design into a locally runnable, reviewable evaluation scaffold **without running any real model, calibrating any checker, spending money, or changing the approved battery**.

**WHY WE ARE DOING THIS:** EVAL-001 defined what we will measure and how a checker must earn trust before we use it. Several practical prerequisites still do not exist: the existing VLM-check script is machine-path-dependent, there is no common mock harness proving that an item can flow through evaluation and produce a traceable result, the identity-review rubric is not yet written, and the Hindi generation-test item set has not been designed. If we wait until Resources finishes, these plumbing gaps will delay the first real calibration/run.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`. Explain ideas, not just labels: what a thing is, why it matters, what evidence means in practice, what changes, and what remains uncertain. Briefly explain internal names when they matter to the human decision.

## INPUTS

Read these first:
- `coordination/PROJECT-CONTRACT.md`
- `shared/COMMUNICATION-STANDARD.md`
- `eval/CHARTER.md`
- `eval/HANDOFF.md`
- `eval/tasks/EVAL-001-CONTROLLER-BRIEF.md`
- `eval/battery/CAPABILITY-BATTERY-V0-DRAFT.md`
- `eval/battery/INSTRUMENT-CALIBRATION-PLAN-V0.md`
- `eval/battery/CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml` **as a proposal only; do not promote it**
- `eval/scripts/check-vlm.mjs`
- `shared/AUTONOMY-POLICY.md`

## IN SCOPE

### 1. Make the existing checker script portable

Repair `eval/scripts/check-vlm.mjs` so it no longer depends on a hard-coded path that exists only on one machine.

The purpose is simple: another machine/worktree should be able to point the script at an input file or directory explicitly and run it.

- Preserve the checker/evaluation meaning already present in the script.
- Add clear CLI/help/error behaviour where needed.
- Test only with local fabricated/mock inputs.
- If fixing portability would require changing what the checker actually judges, STOP and report that separately rather than silently changing evaluator behaviour.

### 2. Build a minimal common evaluation harness using synthetic fixtures

Create a small local harness proving the mechanics of an evaluation run without contacting any model/provider.

The harness must demonstrate, with fabricated fixtures only, that we can:
- load a test-item record;
- identify the battery dimension being tested;
- attach a simulated generation/output reference;
- attach a simulated checker/instrument result;
- record pass/fail plus multiple defect labels where applicable;
- distinguish independent item count from repeated attempts;
- record the observation unit (for example frame vs sequence);
- record instrument identity/version/state;
- record generation/evaluation/human-cost fields without inventing values — use explicit fixture values or `null`/`not_measured`;
- emit a machine-readable result plus a human-readable summary;
- keep a shared generation from being counted as two independent trials when the same output is scored on more than one dimension.

This is **plumbing validation**, not a benchmark. The fixtures must be visibly labelled synthetic/mock so nobody can later mistake them for empirical evidence.

### 3. Draft the identity-consistency human rubric

Create a review rubric for the approved `person_identity_across_prompts` test.

Plain-English purpose: before humans or an AI judge look at real generated people, we need written rules saying what must stay the same and what is allowed to vary. Otherwise reviewers can unconsciously change the standard after seeing the outputs.

The draft must include:
- how declared `invariants` are judged one by one;
- how `allowed_variation` prevents lighting/pose/style changes from being mislabelled as identity drift;
- pass/fail and diagnosis recording;
- how multiple simultaneous identity defects are recorded;
- examples using **fabricated descriptions only**, not new generated media;
- ambiguity/adjudication rules;
- what the rubric cannot decide reliably.

This rubric is a **draft for Controller review**, not frozen ground truth and not a calibrated instrument.

### 4. Design the Hindi/Devanagari generator-test item set structure

Create the design for the capability items previously called **M1b**.

Plain-English meaning: these are the prompts we will eventually give image/video generators to see whether they can **draw Hindi text correctly**. They are different from the public Devanagari images Resources may supply to test whether our checker can **read Hindi correctly**.

Design the structure and coverage plan only. Include:
- item fields needed for prompt, exact target string, context/placement, script, difficulty level and expected observable result;
- coverage categories already justified by EVAL-001, including joined-letter forms/conjuncts, vowel marks/matras, nukta where relevant, and the specific character-confusion families already observed;
- short vs longer strings and simple vs visually busier contexts where supported by the approved battery;
- how the Latin control items should be matched so we can tell a general text problem from a Hindi-specific problem;
- what must later be checked by a Hindi first-language reader;
- what may be sourced from existing permissible Hindi text rather than authored from scratch.

Do **not** populate the benchmark with unreviewed Hindi phrases and do not claim linguistic coverage is complete.

## OUT OF SCOPE

- no real image/video/audio generation;
- no external model/API calls, including free-tier calls;
- no checker calibration against real human ground truth;
- no Hindi-reader work or human-time spend;
- no model/vendor/workflow roster selection;
- no provider pricing research;
- no dataset acquisition or rights assessment — Resources owns that;
- no new battery dimension;
- no change to the seven approved V0 dimensions, their difficulty ladders, pass criteria or observation units;
- no change to the approved qualification-gate logic;
- no promotion/finalisation of the proposed Capability Registry cross-stream schema fields;
- no creative-quality evaluator design;
- no EVAL-003.

## DELIVERABLES

- updated `eval/scripts/check-vlm.mjs`
- `eval/harness/README.md` — what the local harness proves and explicitly does **not** prove
- `eval/harness/run-fixture.mjs` — local mock/synthetic execution path
- `eval/harness/fixtures/` — a minimal set of clearly synthetic fixture inputs/expected outputs sufficient to exercise the required mechanics
- `eval/rubrics/IDENTITY-CONSISTENCY-RUBRIC-V0-DRAFT.md`
- `eval/battery/M1B-DEVANAGARI-GENERATION-ITEM-DESIGN-V0.md`
- `eval/findings/EVAL-002-readiness-findings.md`
- `eval/tasks/EVAL-002-CONTROLLER-BRIEF.md`

If an equivalent small file layout is materially simpler, propose it in chat **before** substituting it; do not grow this into a framework.

## ACCEPTANCE CHECKS

Before reporting completion:

1. Run the checker-script help/argument path locally and show that no hard-coded machine path is required.
2. Run the harness on the synthetic fixtures and show that expected machine-readable outputs are produced.
3. Include at least one fixture with multiple defects and one fixture where one synthetic output is scored on two dimensions without being counted as two independent trials.
4. Confirm no network/model/provider call was made.
5. Confirm no real benchmark result was written anywhere.
6. Confirm the identity rubric and M1b design are labelled drafts and have not been treated as calibrated/approved evidence.

## AUTONOMY MODE

`autonomous`

The task is implementation/readiness work under the already approved EVAL-001 design. It is **not** permission to redesign that design.

## RESOURCE BUDGET

- sources/items: repository-local inputs only; no new external dataset/media acquisition
- storage: negligible; code, Markdown, JSON/YAML fixtures only
- API spend: ₹0 / $0
- generations/retries: zero real generations; local synthetic-fixture runs may be repeated as needed
- human specialist time: zero
- other: do not install a large new framework or introduce a service/database for this task

## APPROVED DEPENDENCIES

- EVAL-001 Controller-approved battery specification
- EVAL-001 Controller-approved calibration specification
- existing project communication/autonomy rules

The Capability Registry cross-stream schema remains proposed/deferred. Do not treat it as approved merely because the harness needs a local result format; keep any local harness format explicitly implementation-scoped and reversible.

## STOP CONDITIONS

STOP and write a Controller checkpoint if any of these occurs:
- portability repair requires changing checker judgement semantics;
- the approved battery cannot be represented without changing a dimension, ladder, pass criterion or observation unit;
- a new evaluator/instrument is needed;
- a new cross-stream schema/architecture decision becomes necessary;
- meaningful Hindi-language content must be invented or judged to continue;
- real media, external API access, dataset acquisition, paid spend or human specialist time becomes necessary;
- synthetic harness results expose a contradiction in the approved EVAL-001 design rather than a simple implementation bug;
- any normal `shared/AUTONOMY-POLICY.md` stop trigger fires.

## HUMAN APPROVAL TRIGGERS

Controller approval is required before:
- freezing the identity rubric;
- freezing/populating the final M1b Hindi item set;
- calibrating any checker;
- selecting models/workflows;
- spending human/API money;
- changing the battery or Registry architecture.

## RESULT LOCATION

Authoritative completion/review summary:
`eval/tasks/EVAL-002-CONTROLLER-BRIEF.md`

Explain the important result in chat as well: what became runnable, what is still only a draft, what failed/surprised you, and what this changes for the first future calibration. Commit and push `work/eval`, then STOP. Do not start EVAL-003.
