# Controller EVAL-029 Review — Result Accepted; Seal Evidence Before Merge — 2026-08-28

## Status

**SCIENTIFIC RESULT ACCEPTED. BRANCH NOT YET MERGE-READY BECAUSE THE LIVE EVIDENCE IT DEPENDS ON IS STILL LOCAL/GITIGNORED. ONE ZERO-SPEND PERSISTENCE/SYNC PASS IS REQUIRED.**

Returned branch:
- `eval/eval-029-benchmark-grade-text-ocr`
- returned head: `438b5d3dd748e75782fdf417ea32329f48b13514`
- base at worker start: `28c8477a5f7c5fd7df1642bdc10a24cd1df439ce`

Current main includes the later GOV-005 Controller review.

## Accepted scientific result

Under the separate frozen `benchmark_text_ocr_v1` contract:

### Devanagari
Recomputed from the accepted Cloud Vision stored observations:
- false-pass rate: 0.1250;
- match false-fail rate: 0.0208;
- repeat consistency: 1.0;
- failure rate: 0.0;
- complete 288/288;
- `benchmark_qualified: true`;
- `strict_exactness_qualified: false`.

### Latin
Live EVAL-029 Cloud Vision screen:
- false-pass rate: 0.1042 (15 calls / 5 unique items);
- match false-fail rate: 0.0000;
- repeat consistency: 1.0;
- failure rate: 0.0;
- complete 288/288;
- `benchmark_qualified: true`;
- `strict_exactness_qualified: false`.

Incremental EVAL-029 spend:
- USD 0.4320.

Cumulative paid qualification spend:
- USD 1.7357905.

No fal/A-TEXT generation occurred.
Registry remains 0 rows.

This does not alter any historical strict zero-false-pass disposition.

## Why merge is paused

GOV-005 finding F-1 identified that completed live EMP-001 observations and cost evidence live under
gitignored `eval/runs/` and cannot be reconstructed from GitHub.

EVAL-029 currently repeats that problem:
- the branch adds the benchmark contract/code/tests/handoff;
- the actual completed EVAL-029 benchmark result is not in the branch diff;
- the historical Cloud Vision Devanagari source evidence used for recomputation is also local;
- `test_benchmark_text_ocr.py` hardcodes a machine-local `~/Vaibhav_Personal_Projects/.../emp-001-live/...` path.

A fresh clone therefore cannot reproduce the accepted qualification.

Do not merge until this task stops adding to the persistence debt.

## Required zero-spend correction

### 1. Sync current main

Integrate current `origin/main` into the EVAL-029 branch.
Do not overwrite newer Controller/Governor decisions.

### 2. Seal exact evidence bytes into Git

Create a bounded immutable evidence package, suggested root:

`eval/empirical-tranche-1/evidence/EMP-001/text-ocr/`

At minimum persist exact, unmodified copies of:

1. the accepted Cloud Vision Devanagari strict-run evidence used by EVAL-029 recomputation:
   - `qualification-live-cloudvision-ocr-v1.json`;

2. the completed EVAL-029 combined benchmark qualification result:
   - `benchmark-text-ocr-qualification.json`;

3. a minimal immutable cost/ledger excerpt containing every ledger entry/cost ref needed to trace:
   - the Cloud Vision Devanagari qualification evidence used by this result;
   - the 288 EVAL-029 Latin calls;
   - cumulative spend through EVAL-029.

Do not commit the mutable live ledger wholesale if a bounded referenced excerpt is sufficient.

### 3. Evidence manifest

Add a machine-readable manifest containing:
- evidence package id;
- EMP-001 run id;
- each persisted file path;
- SHA-256 of exact persisted bytes;
- source local runtime path as provenance metadata only;
- candidate/config identity;
- contract ids/hashes;
- call counts;
- cost refs / ledger-excerpt relation;
- incremental and cumulative spend;
- statement that secrets/auth headers are absent;
- immutable/sealed status.

The manifest itself must be fingerprinted.

### 4. No secret leakage

Before commit, mechanically scan the persisted evidence for:
- `FAL_KEY`;
- Google API keys;
- Anthropic/OpenAI keys;
- Authorization headers;
- bearer/key header values;
- environment dumps.

If any secret or credential is present, do not commit that raw file. Produce a deterministic
credential-redacted copy only if redaction can be proven not to alter observations, outcomes,
candidate identity, costs or scientific metrics; record the transformation explicitly.

### 5. Make tests portable

Replace the hardcoded home/worktree EVAL-029 test path with the committed evidence path.

A fresh clone must be able to:
- load the committed Devanagari evidence;
- recompute its benchmark metrics;
- reconcile its stored summary;
- load/recompute the EVAL-029 Latin benchmark result;
- verify the evidence manifest and hashes.

No test may require the original `emp-001-live` worktree merely to verify historical evidence.

### 6. Preserve live result exactly

Do NOT rerun:
- Cloud Vision;
- Devanagari;
- Latin;
- Gemini;
- Anthropic;
- Tesseract;
- fal.

External calls: 0.
Incremental spend for this correction: USD 0.

The persisted result must match the already-completed live result byte-for-byte wherever raw source
files are safe to commit.

## A-TEXT

EVAL-024 still has no sealed artifacts.
Keep the existing A-TEXT handoff prepared-only.
Do not generate or score anything in this correction.

## Merge gate

Return only after:
- current main integrated;
- committed evidence package exists;
- fresh/path-independent tests pass;
- preflight remains green;
- exact historical strict evidence/contracts unchanged;
- Registry remains 0;
- no secrets;
- worktree clean.

Push exact head.
Do not merge.
Return to Controller.
