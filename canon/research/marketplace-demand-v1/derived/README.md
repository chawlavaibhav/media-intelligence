# Marketplace-derived benchmark cases — CANON-011

**Status:** proposed worker output. Not frozen, not merged, not an approved benchmark.
**Spend:** USD 0 · **External calls:** 0 · **Model generations:** 0

Eighteen benchmark cases derived from individual **Upwork buyer job postings** in the committed
marketplace research one directory up. Each carries the full chain the Controller decision
requires — source job, source-faithful customer brief, Normalized Request, acceptance contract,
route-neutral generation brief, prompt-ready envelope — and stops deliberately before any
provider-specific prompt, because that step needs a Production IR the project has not built.

**Start with [`COVERAGE-REPORT.md`](COVERAGE-REPORT.md).** It has the headline findings, every
computed figure and what this does and does not claim.

## The rule these files are built on

A requirement belongs to the customer only if the customer said it, or it follows directly from
what they said. Everything the benchmark adds to make a case repeatable — a script, a product, an
aspect ratio, a language, a list of what counts as "the same person" — is an **experiment
fixture** and is labelled as one. `validators/validate_marketplace_bank.py` fails closed if that
line is crossed, and `validators/test_negative_fixtures.py` proves each of its gates actually
fires by breaking the bank 28 different ways and requiring a rejection each time.

**Fiverr gigs are seller offerings and are never customer briefs.** They informed five commercial
conventions, all recorded and all used only to shape fixtures.

## Files

| File | What it is |
|---|---|
| `marketplace-brief-bank-v1.yaml` | The 18 cases. **Source of truth — edit this one.** |
| `marketplace-prompt-ready-bank-v1.yaml` | Generated envelope view. Do not hand-edit. |
| `COVERAGE-REPORT.md` | Findings, distributions, gaps, Stage-C candidates. |
| `SOURCE-DISCREPANCIES.md` | Four cleaned-vs-raw Fiverr disagreements, recorded not reconciled. |
| `coverage-measurement.json` | Every number in the coverage report. |
| `measure_coverage.py` | Computes it. |
| `build_prompt_ready_bank.py` | Regenerates the envelope bank. |
| `validators/validate_marketplace_bank.py` | Fourteen gates. |
| `validators/test_negative_fixtures.py` | 28 negative controls. |

## Running the checks

PyYAML is required and **is not installed system-wide on this machine** — the Canon handoff
already records this. Create a local virtual environment with `pyyaml`, then, from the repository
root:

```
python3 canon/research/marketplace-demand-v1/derived/validators/validate_marketplace_bank.py
python3 canon/research/marketplace-demand-v1/derived/validators/test_negative_fixtures.py
python3 canon/research/marketplace-demand-v1/derived/measure_coverage.py
python3 canon/research/marketplace-demand-v1/derived/build_prompt_ready_bank.py
```

If you change the brief bank, regenerate the envelope bank and rerun both validators — the
validator fails if the two banks have drifted apart.

## What this does not touch

The 30 authored briefs, the 11-item request-coverage extension, Capability Contract v1 or v2, the
100-item Eval bank and the Capability Registry are all **unmodified**. This is an additional
evidence-backed request source and a candidate Stage-C pool, not a replacement for anything.
