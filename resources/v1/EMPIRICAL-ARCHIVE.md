# Empirical artifact archive — storage class C

**Task:** R8 (tonight's schema tranche) of `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md`
**Date:** 26 Aug 2026 · **Schema:** `EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml`
**Validator:** `validators/check_empirical_archive.py` — executed tonight, exit 0

---

## The problem this solves

When Eval starts paying for generations, each output is **irreproducible**. Providers drift, versions
retire, and the same prompt with the same seed stops returning the same bytes. If an output is
deleted after scoring, every measurement derived from it becomes unverifiable — nobody can re-check
it, re-annotate it for a second defect, or use it as a regression case.

**This has already happened to this project.** The legacy `media-factory` spike gitignored its
generated media with the comment *"expensive to make, wrong to store in git… regenerable from the
scripts here."* They were not regenerable. The 64 human judgements survived only because someone
whitelisted `scores.json`; **the 64 images did not.** Those failures can no longer be re-annotated,
which is exactly what the Eval master plan now asks for.

## Four entities, and why the split is the design

**Attempt · Artifact · Measurement · Acceptance.** Four persistent entities, four JSONL files.

```
attempt ──▶ artifact (0 or 1) ──▶ measurement (many)
   │                          └──▶ artifact (derived: frames, transcodes)
   └──▶ acceptance (0 or 1, per trial)
```

**Attempt and artifact are separate, and v1 got this wrong.** The **call** and the **bytes** are
different facts. A call always happened, always cost money and latency, and is always evidence; bytes
may not exist. v1 stored both in one row, so a refused call became an artifact-shaped hole with a
null hash. Now a refusal is a first-class attempt row with no artifact, and a sampled frame is a
derived *artifact* rather than a second *attempt*.

**One artifact is scored by many capabilities.** Storing a copy per metric would multiply cost, break
the generate-once/measure-many economy the benchmark design rests on, and make pass-at-k uncountable
— nobody could tell a genuine repeat from a filing duplicate.

**Proven at scale, from a clean state.** A synthetic 1,000-attempt archive is generated into
`build/` and validated:

| | |
|---|---:|
| Attempts | **1,000** |
| — succeeded | 966 |
| — refused / errored, each preserved individually with its reason | 34 |
| Artifacts | **1,126** (966 direct + 160 derived frames) |
| Measurements | **5,796** |
| Acceptances | 250 |
| **Duplicate media copies** | **0** |
| **Mean measurements per artifact** | **6.00** (min 5, max 7) |

Everything in the fixture is synthetic — fictional vendor and model names (`dummy-vendor-a`,
`dummy-image-v0`), fixed timestamps, hashes derived from record ids. **No provider was called and no
money was spent.** Under R-C3 the archive is a build product: the generator and the expected shape
are committed, the 3.7 MB of generated rows are not.

## Two vocabularies Resources stores but does not own

**Observation units are canonical and verbatim:**

```
frame | shot | shot_pair | sequence | whole_asset | asset_set_over_time
```

v1 used a Resources-invented set — `image`, `sampled_clip`, `whole_clip`. Those are now **explicitly
rejected** by the validator. A local synonym silently breaks comparability between two measurements
that should be comparable. Where derived media needs describing, that belongs in
`artifact.derivation`, not in the observation unit.

**Capability ids are Eval's**, stored exactly as Eval defines them. Resources never renames,
abbreviates, normalises or maps them.

## Repeat is not retry

| | `repeat_index` | `retry_of_attempt_id` |
|---|---|---|
| What it is | A **deliberate experimental repeat**, planned before any result is seen | A **repair attempt caused by a prior failure or rejection** |
| Measures | Reliability (`pass_at_k`) | Getting to an acceptable outcome |
| In a retry chain | **Never** | **Always** |

**Why the distinction is load-bearing.** CpAO divides the cost of a retry chain by accepted outcomes.
Count repeats as retries and **every CpAO figure is inflated by the experimental design itself**.
Count retries as repeats and `pass_at_k` is computed over attempts that were not independent draws.
Both errors are silent, and neither is recoverable after the fact.

## Four rules that exist because omitting them loses evidence

**1. Every failed attempt survives individually.** An *attempt* row is written when the call is
*made*, not when it succeeds. A refusal produced no bytes but still cost money and latency, so it is
a first-class row carrying the provider's verbatim `error_detail` and no artifact. **Aggregate
reliability counters are explicitly not sufficient** — a count of "5 refusals" cannot say which items
were refused, what they cost, or whether the pattern is systematic. The validator rejects a summary
that disagrees with the rows.

**2. Never fabricate a hash or a cost.** An artifact exists only where bytes exist, and its
`output_hash` is never null — an artifact *is* its bytes. If bytes were not retained there is no
artifact row and the attempt records why. `cost_ref` points at a recorded ledger line; a modelled
estimate is labelled as one. This is the same rule that stopped a full-archive hash being invented
for VideoGen-RewardBench, which was never downloaded.

**3. Frames of one clip are one trial.** A sampled frame is a **derived artifact** that inherits its
parent's `trial_id` and `attempt_id`; it never gets its own. Ten frames from one clip are ten
artifacts of one trial, and letting each claim a trial would inflate every downstream sample size by
an order of magnitude. This is the same correlation trap the project has already paid for
statistically.

**4. Retention is not conditional on the result.** Deleting rejected outputs after scoring destroys
the denominator of Cost per Accepted Outcome.

## Cost per Accepted Outcome only works if the archive works

CpAO = total cost of every attempt in a retry chain ÷ accepted outcomes. It is recomputable **only**
if the cost reference, the acceptance decision, the retry chain and the output bytes all survive
together. That is why the `acceptance_record` sits in a Resources schema. **Resources records the
decision; it never makes it** — `decided_by` is never Resources.

Evaluator cost is recorded separately from generation cost, so neither can hide inside the other.

## How a production failure becomes a regression candidate

**Resources identifies candidates mechanically. Eval decides what a failure means.**

A candidate is any trial whose acceptance record says `accepted: false`, any attempt whose `status`
was error/refusal/timeout, any artifact carrying a measurement the owning stream marks as a failure,
or any production failure ingested with complete provenance.

Resources supplies the bytes, the complete provenance, the lineage keys and the exact conditions.
Resources does **not** supply the failure label, its severity, or whether it is worth retesting.

**Contamination warning, recorded in the schema:** regression items are contaminated by construction
— somebody already studied them closely. That is fine for regression and disqualifying for
calibration, qualification or reserve use on anything sharing their lineage.

## Fail-closed, verified

**Twenty-two committed negative controls**, each breaking (or deliberately satisfying) exactly one rule, run by
`validators/run_archive_negative_controls.py`. The runner asserts both the expected outcome **and**
that the failure names the right rule — a case that fails for the wrong reason is not a passing
negative control.

| Control | Breaks |
|---|---|
| `00-baseline-valid` | nothing — proves the others fail for their stated reason |
| `01-observation-unit-v1-coinage` | uses `whole_clip` instead of the canonical vocabulary |
| `02-refusal-carrying-an-artifact` | a call that produced nothing owns bytes |
| `03-failure-without-a-recorded-reason` | a refusal with no `error_detail` |
| `04-aggregate-counter-replaces-preserved-rows` | a summary claiming 5 refusals over 1 row |
| `05-reliability-repeat-inside-a-retry-chain` | a repeat counted as a retry |
| `06-derived-artifact-claiming-its-own-trial` | a frame becoming an independent trial |
| `07-same-output-stored-twice` | one hash at two locations |
| `08-measurement-with-both-result-and-absence` | incoherent measurement |
| `09-measurement-referencing-a-missing-artifact` | a score with nothing behind it |
| `10-no-fan-out` | one measurement per artifact — no reuse |
| `11-attempt-without-a-cost-reference` | cost reconstructable later |
| `12-acceptance-decided-by-resources` | Resources deciding acceptance |
| `13-two-attempts-sharing-one-trial` | RI-C1: a trial grouping two calls |
| `14-repeat-and-retry-each-get-their-own-trial` | nothing — the positive half of RI-C1 |
| `15-status-refused-not-refusal` | RI-C2: a near-miss status id |
| `16-lane-display-name-not-machine-id` | RI-C2: `video` instead of `general_video` |
| `17-provider-failure-as-a-measurement-absence` | RI-C3: laundering an attempt failure |
| `18-instrument-unqualified-as-an-absence` | RI-C3: discarding a real observation |
| `19-cost-ref-that-does-not-resolve` | RI-C4: unresolvable cost reference |
| `20-inline-cost-instead-of-a-ledger-reference` | RI-C4: cost as a number |
| `21-mutable-cost-ledger-entry` | RI-C4: an editable ledger |

**22/22 behaved as declared.** Two are deliberately *positive* — a suite with no passing case would
be satisfied by a validator that rejects everything. The validator separates *could not check* (exit 2) from *found a
violation* (exit 1): missing directory, missing file and empty file all produce exit 2, never a
cheerful zero.

## Not forecast tonight, deliberately

**No byte budget.** A forecast needs per-endpoint duration and resolution from Eval's E2 inventory,
which does not exist yet. Guessing one would encode a guess as a plan. The schema carries
`output_bytes` per artifact, so the forecast becomes a sum the moment E2 lands.

For scale: Eval's frozen caps are ≤204 admission-screen outputs and ≤520 deep-qualification outputs
= 724 before retries, plus ≤96 end-to-end trials. 1,000 is the right order of magnitude for the first
wave, and the schema imposes no structural limit beyond it.

**Operational rule for later:** ingest durably **as part of execution**, not as a tidy-up after
scoring. An output that is scored and then cleaned up has already been lost.
