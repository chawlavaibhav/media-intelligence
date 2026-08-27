# Controller RES-005 Integration and Temporal Material Resolution — 2026-08-28

## Status

**RES-005 ACCEPTED AND MERGED. TEMPORAL MATERIAL CONTRACT RESOLVED AT PACK LEVEL.**

Integration:
- PR #54
- merge commit `3a49464448f1fb4d49ea59b7325c57eb750f5716`

## Accepted acquisition result

RES-005 provides a bounded real-footage base for EVAL-026 temporal perturbation work:

- 12 clips from 12 distinct source works;
- zero acquisition/API/model spend;
- rights routes recorded and limited to CC BY, CC BY-SA, CC0, or US-Government public-domain material;
- 12/12 pass the Resources cleanliness screen;
- 0 pre-existing freeze runs, black-frame intervals, or detected interlacing in the frozen clip windows;
- representative 3/3 clips passed EVAL-026 real-clip ingest;
- the attempted full 12-clip ingest was NOT completed because rebuildable per-frame PNG expansion exhausted local disk;
- raw media remains transient/git-ignored; hashes, provenance, retrieval scripts, measurements and lineage are committed.

The full 12-clip ingest therefore remains a zero-spend execution prerequisite before any real checker qualification run. It must be done in batches or with an explicitly recorded normalisation/downscale condition rather than silently changing the material.

## Controller correction made before merge

The worker brief originally overstated two things and was corrected on the branch before integration:

1. it said all 12 clips had been accepted by Eval ingest; evidence supports only a representative 3/3;
2. it implied temporal checker qualification would necessarily require no API spend and would produce the project's first qualified evaluator family. No checker has been selected, no pass mark exists yet, and qualification is contingent on passing the precommitted gate.

## Material-contract resolution

The family-4 content requirement is **PACK-LEVEL**, not a requirement that every clip contain a person + product + on-screen text simultaneously.

Reason:

- `RESOURCE-REQUESTS.yaml` expresses one pack request and includes the inherently pack-level condition `>=2 clips that cut between shots`;
- the perturbation protocol consumes different source features for different defect types;
- requiring every clip to contain every feature does not increase truth quality for freeze, motion, text, product, identity or shot-continuity perturbations; it only makes acquisition artificially commercial-ad-shaped;
- the scientifically relevant quantity is the number of independent usable base clips **per perturbation type**, which family 4 already requires to be reported separately and never pooled into one headline accuracy number.

The stricter phrase in `clips.example.json` and EVAL-026's precondition text was an accidental tightening in a paraphrase/example. It is corrected by this decision.

## Accepted RES-005 pack-level coverage

Current measured opportunities include:

- general freeze / reversal base: 12 clips;
- multi-shot source material: 6 clips;
- on-screen-text mutation base: 6 clips;
- product-region substitution base: 5 clips;
- rendered-character identity base: 4 clips;
- photographed-face identity base: 3 clips.

Rendered-character and photographed-face identity evidence must remain separated. They are not interchangeable populations.

These counts are coverage counts, not claims of statistical precision. The family-4 gate remains per perturbation type.

## PACK-AV-CLEAN boundary

RES-005 material is **not PACK-AV-CLEAN** and does not satisfy any speech/audio pack obligation.

For temporal Stage-Q qualification, PACK-AV-CLEAN is **permitted but not required** as a supply route. Any rights-cleared, clean real footage meeting the temporal pack-level coverage contract may serve.

PACK-AV-CLEAN itself remains unchanged for its speech/audio consumers: consent, verified transcripts, turn boundaries, language balance and other requirements are not weakened by this decision.

Use the semantic role name **MAT-TEMPORAL-BASE** going forward. Existing RES-005 paths/identifiers containing `MAT-AV-MIN` remain historical artifact names and do not need migration.

## What is now unblocked — and what is not

Resolved:
- bounded acquisition of a real temporal perturbation base;
- pack-level content interpretation;
- supply route independent of PACK-AV-CLEAN.

Still required before any real temporal checker qualification observations:
1. select the actual candidate checker/instrument;
2. complete full 12-clip ingest under a recorded execution condition;
3. freeze Controller-approved numeric pass marks before observations are run or inspected;
4. preserve separately required human adjudication for capabilities whose frozen map says `model_based_plus_human`.

No temporal evaluator is qualified by RES-005.
No Registry row is authorised.
No qualification run is authorised by this decision.
