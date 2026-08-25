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

## Two files, and why that separation is the design

**Artifacts** (what was produced) and **measurements** (what was observed about it) are separate.

One generated asset is scored by many capabilities. Storing a copy per metric would multiply cost,
break the "generate once, measure many" economy the whole benchmark design rests on, and make
pass-at-k uncountable — because nobody could tell a genuine repeat from a filing duplicate.

**Proven tonight, at scale.** A synthetic 1,000-artifact archive was generated and validated:

| | |
|---|---:|
| Artifacts | **1,000** |
| — succeeded | 966 |
| — refusal / error (retained) | 34 |
| Measurements | **5,796** |
| Distinct output hashes stored | 966 |
| **Duplicate media copies** | **0** |
| **Mean measurements per scored artifact** | **6.00** (min 5, max 7) |

**One generation, six measurements, stored once.** The ≥1,000-artifact capacity requirement is
demonstrated, not asserted. Everything in the fixture is synthetic — fictional vendor and model names
(`dummy-vendor-a`, `dummy-image-v0`), fixed timestamps, hashes derived from record ids. **No provider
was called and no money was spent.**

## Four rules that exist because omitting them loses evidence

**1. A refusal is evidence.** An artifact row is written when the call is *made*, not when it
succeeds. A refusal produced no bytes but still cost money and latency. The schema requires
`api_status != 'ok'` ⟹ `output_hash` is null, and `api_status == 'ok'` ⟹ it is not. Without this,
refusals silently vanish and reliability is overstated.

**2. Never fabricate a hash or a cost.** If bytes were not retained, `output_hash` is null and
`output_location` says so. `cost_ref` points at a recorded ledger line; a modelled estimate is
labelled as one. This is the same rule that stopped a full-archive hash being invented for
VideoGen-RewardBench, which was never downloaded.

**3. Frames of one clip are one trial.** `observation_unit` is mandatory on every measurement so a
sampled-frame observation can never be miscounted as an independent trial. This is the same
correlation trap the project has already paid for statistically.

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

A candidate is any artifact that was not accepted, or whose `api_status` was error/refusal/timeout,
or that carries a measurement the owning stream marks as a failure, or that arrives as a production
failure with complete provenance.

Resources supplies the bytes, the complete provenance, the lineage keys and the exact conditions.
Resources does **not** supply the failure label, its severity, or whether it is worth retesting.

**Contamination warning, recorded in the schema:** regression items are contaminated by construction
— somebody already studied them closely. That is fine for regression and disqualifying for
calibration, qualification or reserve use on anything sharing their lineage.

## Fail-closed, verified

**Seven negative controls executed tonight.** The validator distinguishes *couldn't check* (exit 2)
from *found a violation* (exit 1):

| Broken input | Exit | Detected |
|---|:--:|---|
| Empty artifacts file | 2 | refuses to validate an empty archive |
| Missing file | 2 | file not found |
| Refusal carrying an output hash | 1 | status/hash contradiction |
| Same output stored at two locations | 1 | duplicate media copy |
| Measurement referencing an absent artifact | 1 | dangling reference |
| One measurement per artifact (no reuse) | 1 | fan-out 1.00 — not reusing generations |
| Artifact missing its cost reference | 1 | cost must never be invented later |

## Not forecast tonight, deliberately

**No byte budget.** A forecast needs per-endpoint duration and resolution from Eval's E2 inventory,
which does not exist yet. Guessing one would encode a guess as a plan. The schema carries
`output_bytes` per artifact, so the forecast becomes a sum the moment E2 lands.

For scale: Eval's frozen caps are ≤204 admission-screen outputs and ≤520 deep-qualification outputs
= 724 before retries, plus ≤96 end-to-end trials. 1,000 is the right order of magnitude for the first
wave, and the schema imposes no structural limit beyond it.

**Operational rule for later:** ingest durably **as part of execution**, not as a tidy-up after
scoring. An output that is scored and then cleaned up has already been lost.
