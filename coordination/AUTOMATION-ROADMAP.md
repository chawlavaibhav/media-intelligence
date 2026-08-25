# Automation Roadmap

**Updated:** 25 Aug 2026 by Repository Governor, task GOV-001.

The A/B/C/D levels below are a durable policy and are unchanged. Only the "What exists today"
inventory was stale and has been corrected against the repository.

## Level A — Human/Controller required
Architecture changes. Interpreting a central hypothesis's result. Approving a curriculum or new
benchmark dimension. Accepting uncertain legal/licence terms. Material budget changes.

## Level B — Claude autonomous execution (once the relevant protocol is frozen and approved)
Approved book/chapter batches (Canon). Approved dataset downloads (Resources). Approved benchmark
runs against an approved model list (Eval). Validation and reporting in all three.

## Level C — scripted, deterministic, repeated
Provenance/schema validation and audit-gate validation (Canon) — `canon/validation/`, tested by
`tests/`. Download, checksum, manifest, dedup, report generation (Resources) — `resources/scripts/`.
Battery construction, blind-payload checks and harness self-test (Eval) — `eval/harness/`,
`eval/scripts/`, `eval/battery/devanagari-exactness/`.
Scripts are versioned; a worker should not manually repeat deterministic work a tested script
already does consistently.

## Level D — scheduled/event-driven (later, not now)
Periodic Capability Registry refresh. Corpus integrity re-checks. Benchmark rerun triggered by an
approved model-version update. **Not implemented. No recurring paid workload exists or should be
created without explicit Controller approval.**

## What exists today

> **Correction notice.** This section previously said `eval/scripts/check-vlm.mjs` was "the one
> working script in the repo" and that everything else in `*/scripts/` was empty, and it pointed at
> a `canon/scripts/` directory that does not exist. Substantial tooling has been built since.
> Verified against `main` at `00ea9b06` on 25 Aug 2026.

**Canon** — `canon/validation/validate_audit_gate_v02.py` (the live gate validator; 19 records, 0
errors) and `canon/validation/validate_canon003_integrated.py` (**historical** instrument for the
frozen 16-book corpus — its meaning must never change). Both covered by `tests/`, which runs 65
tests plus 93 subtests. There is **no `canon/scripts/` directory.**

**Eval** — `eval/scripts/check-vlm.mjs` (portable, supports per-item targets, `--dry-run` needs no
API key), `eval/harness/run-fixture.mjs` (`--selftest` passes, including negative-control fixtures),
and the Devanagari exactness battery under `eval/battery/devanagari-exactness/` with its own 43-test
suite.

**Resources** — 14 scripts under `resources/scripts/`: per-source fetchers, `validate_and_manifest.py`,
`build_reports.py`, `build_source_registry.py`, `verify_devanagari_composition.py`, `guard.sh`,
`remote_zip.py`.

**Two known limits on reproducibility from a fresh clone**, both deliberate consequences of keeping
large or proprietary payloads out of Git, and both recorded so nobody mistakes them for breakage:

1. `resources/scripts/verify_devanagari_composition.py` and `build_reports.py` read the git-ignored
   raw corpus. On a clone without it, the verifier fails (correctly) and `build_reports.py`
   **silently regenerates a degraded report and exits 0** — see the routed finding in
   `governance/audits/2026-08-25-initial-repository-hygiene-audit.md`. Do not commit its output from
   a machine that lacks the corpus.
2. The Devanagari battery's built items are git-ignored and its pinned font is a proprietary system
   asset that is not committed. The build is fingerprinted by SHA-256 so a rebuild can be checked,
   but it cannot be reconstructed on a machine without that font.
