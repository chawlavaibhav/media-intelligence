# Automation Roadmap

## Level A — Human/Controller required
Architecture changes. Interpreting a central hypothesis's result. Approving a curriculum or new
benchmark dimension. Accepting uncertain legal/licence terms. Material budget changes.

## Level B — Claude autonomous execution (once the relevant protocol is frozen and approved)
Approved book/chapter batches (Canon). Approved dataset downloads (Resources). Approved benchmark
runs against an approved model list (Eval). Validation and reporting in all three.

## Level C — scripted, deterministic, repeated
Provenance/schema validation, coverage report generation (Canon) — see `canon/scripts/`.
Download, checksum, manifest, dedup (Resources) — see `resources/scripts/`.
Battery execution, exact-text scoring, cost aggregation (Eval) — see `eval/scripts/`.
Scripts are versioned; a worker should not manually repeat deterministic work a tested script
already does consistently.

## Level D — scheduled/event-driven (later, not now)
Periodic Capability Registry refresh. Corpus integrity re-checks. Benchmark rerun triggered by an
approved model-version update. **Not implemented. No recurring paid workload exists or should be
created without explicit Controller approval.**

## What exists today
`eval/scripts/check-vlm.mjs` — the one working script in the repo, used for the Devanagari checker
calibration. Everything else in `*/scripts/` is empty, awaiting first approved deterministic task.
