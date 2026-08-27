# Controller EVAL-024 Readiness Review — Cleanup, Sync, Then Live Generation — 2026-08-28

## Status

**IMPLEMENTATION ACCEPTED IN PRINCIPLE. DO NOT MERGE OR DISPATCH FROM RETURNED HEAD `e4e4d39` YET. PERFORM ONE BOUNDED INTEGRATION CLEANUP, THEN LIVE GENERATION MAY RUN FROM THE EXACT CLEANED/PUSHED HEAD IF `FAL_KEY` IS PRESENT.**

Returned branch:
- `work/eval-024-parallel-atext-generation-only`
- returned head: `e4e4d39`
- base: historical `b4af1a1`
- live calls: 0
- spend in this lane: USD 0

## What is accepted

The Controller review accepts the core generation-only design:

- exactly 16 frozen coordinates;
- GPT Image 2 + Ideogram v3 routes unchanged;
- retries 0;
- persistent EMP-001 ledger;
- generation-only path constructs/calls no evaluator;
- artifacts are hashed and sealed for later scoring;
- manifest carries `scored: false`;
- scoring fields are refused;
- missing/ambiguous calls are persisted under existing one-call-one-trial semantics;
- Registry remains untouched;
- fake-live projection preserves the existing USD 1.3037905 qualification spend and reaches USD
  2.2077905 cumulative at nominal generation rates.

The missing `FAL_KEY` was correctly treated as pre-dispatch and no live call/spend occurred.

## Required cleanup before live dispatch

### 1. Sync to current main

The returned branch is behind current main and must incorporate all current Controller decisions,
including:
- EVAL-025 integration;
- exact-text non-blocking course correction;
- EVAL-029 task state.

Merge/rebase current `origin/main` into the EVAL-024 branch before any live dispatch.

Do not modify EVAL-029 or other active-lane domain work while resolving.

### 2. Restore unrelated generated evidence files

The branch incidentally rewrote:
- `eval/empirical-tranche-1/preflight-result.json`;
- `eval/empirical-tranche-1/text_qualification/perceptibility-mechanical.json`.

These are not EVAL-024 outputs.

Restore both byte-for-byte to current `origin/main` before the final EVAL-024 commit.

The preflight-result difference includes machine/worktree absolute paths; the perceptibility file was
re-serialized/reordered. Neither belongs in this PR.

Final EVAL-024 diff should contain only its generation-only implementation/tests plus actual sealed
live artifacts/manifest after live execution.

### 3. Do not lie about artifact media type

Current implementation writes every successful returned blob to a `.png` path even when the bytes
are not PNG.

Before live:
- determine media type from returned bytes (at minimum PNG/JPEG/WebP);
- use a matching extension or a content-neutral filename;
- record actual media type;
- record dimensions where safely parseable;
- preserve raw returned bytes unchanged;
- hash the raw returned bytes.

Do not transcode or normalize the image after retrieval merely to make the extension convenient.

### 4. Restore full local test prerequisites

The 9 full-suite failures were caused by missing gitignored pinned Tesseract traineddata, not by
EVAL-024.

Before final live dispatch:
- materialize/reuse the exact already-pinned official traineddata with the accepted hashes;
- do not change Tesseract configuration/evidence;
- rerun the full affected EMP-001 suite and require green;
- preflight must remain green.

This is environment restoration, not reopening the Tesseract research line.

## Live execution authority

After the cleanup commit is pushed and tests/preflight are green:

If `FAL_KEY` is available in the worker's environment:
- run EVAL-024 live immediately from that exact pushed/tested head;
- use the existing live EMP-001 run/ledger containing USD 1.3037905 prior qualification spend;
- do not create a new ledger/run id;
- no evaluator calls;
- no scoring;
- no retries;
- no regeneration;
- no account prefunding.

If `FAL_KEY` is still unavailable:
- stop pre-dispatch and return the cleaned/pushed head;
- do not ask for the key in chat;
- no spend.

## Artifact persistence

For this bounded 16-image tranche, committing the sealed image bytes to the repo is accepted so the
later evaluator can consume exact durable bytes.

This is a bounded exception for EMP-001 evidence and must not be generalized into storing all future
generated media directly in Git.

## Final return

Report:
- exact cleaned/pushed HEAD;
- current-main integration base;
- final diff paths;
- full tests + preflight;
- proof the two unrelated generated files match current main byte-for-byte;
- media-type/extension behavior tests;
- if live executed: all 16 coordinate dispositions, hashes, dimensions/media types, provider request
  ids, incremental/cumulative spend, manifest fingerprint, evaluator calls 0, Registry unchanged;
- if not executed: exact pre-dispatch blocker only.

Do not merge.
