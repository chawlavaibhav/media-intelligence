# Controller Review — EVAL-012 / EMP-001 zero-spend readiness

**Date:** 26 Aug 2026  
**Reviewed worker branch:** `work/eval-012-emp-001-zero-spend` @ `d092be097cbc143cb1a5ad51ea5dc819a9a57486`  
**Controller verdict:** **BLOCKED — bounded implementation correction only**

## What is accepted

The zero-spend implementation work is useful and should be preserved:

- 162 EMP-001 tests were reported green by the worker;
- inherited V1 harness self-test reported 107/107;
- Resources cross-branch validation reported PASS;
- dry-run network isolation, Registry-zero protection, protected-baseline hashes and the 16-generation ceiling were exercised;
- the 96-item Latin pack was built separately and the human perceptibility sheet was honestly left unfilled rather than fabricated;
- external calls/spend remained 0.

The Controller could not independently rerun the worker suite because the Controller runtime cannot resolve GitHub from the local container. Therefore the execution counts above remain worker-run evidence. The Controller did independently inspect the returned code paths.

## Why `READY_FOR_SPEND_APPROVAL` is rejected

The branch is dry-run ready, but the positive paid execution path required by the existing implementation plan is not yet wired. Approving spend now would still require implementation changes before the first legitimate call.

### B1 — live qualification orchestration is absent

`eval/empirical-tranche-1/text_qualification/qualify_text.py` opens the authorisation guard under `--live` and then unconditionally raises that live qualification is not implemented.

The real `OpenAITextJudge` / `GeminiTextJudge` scaffolding therefore never participates in the qualification protocol. Only `FakeCandidate` does.

**Owner:** Eval  
**Smallest correction:** implement a positive live orchestration function that can be exercised entirely with injected fake transports before any real call. CLI execution must still require explicit authorisation.

### B2 — A-TEXT live generation path is absent

`eval/empirical-tranche-1/atex/run_atex.py --live` always refuses. The core runner accepts an injected generator, but no route-specific fal generation adapter is implemented for the frozen IMG-01 and IMG-02 routes.

This misses Task 7 Step 2 of the authoritative implementation plan.

**Owner:** Eval  
**Smallest correction:** implement the two frozen fal route adapters behind injected transports and budget/authorisation gates, without making a provider call.

### B3 — A-TEXT measurement path is dry-run-specific even when `dry_run=False`

The A-TEXT runner always:

- calls `_fake_transcribe(...)` rather than the qualified text judge;
- writes measurements with `synthetic: true`;
- returns the run with `synthetic: true` regardless of the `dry_run` argument.

A real paid result would therefore be mislabeled and would not be measured by the qualified instrument the experiment is supposed to establish.

**Owner:** Eval  
**Smallest correction:** real/non-dry-run execution must call the supplied qualified judge's blind `transcribe` path, set `synthetic` from the actual execution mode, and preserve the partial-evidence / no-full-slot-promotion boundary.

### B4 — missing positive live-path controls

The suite strongly proves refusal/dry-run behavior but does not prove the inverse path:

> valid authorisation + fake live transport + sufficient budget -> exactly one dispatch -> non-synthetic persisted evidence.

That positive control is required for both qualification and A-TEXT before money is approved.

**Owner:** Eval  
**Smallest correction:** add positive fake-live tests and negative twins for invalid auth, budget exhaustion, retry count and synthetic/empirical labeling.

### B5 — Google REST authentication semantics are not provider-correct

`providers.HttpTransport` sends `Authorization: Bearer <key>` for every provider while the branch expects `GOOGLE_API_KEY`. For the Gemini API key route, Google documents `x-goog-api-key` authentication. Provider-specific request transport/auth must be explicit before the first real call.

This is not a scientific change and does not alter the chosen judge candidate.

**Owner:** Eval  
**Smallest correction:** split transport/auth behavior by provider and test the emitted headers with fake HTTP transport; continue to read secrets only at dispatch time.

## What is NOT reopened

Do not change:

- EMP-001 scientific scope;
- the USD 10 proposed ceiling;
- 0 retries;
- 96 Devanagari + 96 Latin qualification shape;
- 3 repeats per shape;
- four frozen A-TEXT strings;
- IMG-01 / IMG-02 scientific questions;
- the 16-generation maximum;
- provisional qualification gates;
- V1/Devanagari protected baselines;
- Stage-C-only customer CpAO rule.

The outstanding human perceptibility review remains a separate zero-spend prerequisite for the Latin leg. It is not the reason for this implementation block.

## Correction route

Open one bounded zero-spend correction on top of the returned worker head:

- task: `eval/tasks/EVAL-013-EMP-001-LIVE-PATH-CORRECTION.md`
- branch: `work/eval-013-emp-001-live-path-correction`
- external calls/spend: **0**

After EVAL-013 returns, the Controller will re-review. Only a genuine positive fake-live path plus fresh green verification can advance EMP-001 to explicit user spend approval.
