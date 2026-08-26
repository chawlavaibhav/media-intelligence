# RESOURCES-V1-CORRECTION-PASS

**Status:** AUTHORIZED correction pass on `work/resources-v1-overnight` only.  
**Purpose:** close the Controller review loop on the overnight Resources V1 work before merge.  
**Spend:** ₹0. No acquisition, purchase, login, email, consent action, or raw-laptop-corpus access is authorized.

## Zoom-out

Resources is the evidence-supply and evidence-preservation layer. It does **not** decide Canon truth, evaluator semantics, thresholds, creative labels, or routing. It must make sure Canon and Eval have the right material, with stated rights/lineage/protected-set roles, and it must preserve irreproducible paid outputs so later measurements and CpAO remain auditable.

The overnight work is substantively accepted. Do **not** redesign R1–R5/R8. This pass is a bounded correction of four Controller findings plus one cross-stream interface decision.

## Controller decisions you must implement

### R-C1 — Correct the misleading 15/36 headline

Current prose says that 15/36 capabilities "need nothing from Resources, ever." Replace that claim everywhere it appears with the precise meaning:

> **15/36 require no capability-specific external stimulus pack; some still inherit evaluator-calibration dependencies.**

Do not change the underlying 36-row classification merely to fit the wording. Preserve the exact arithmetic:
- 1 available
- 10 constructed_by_eval
- 5 no_external_resource
- 3 partial
- 17 missing
= 36.

### R-C2 — Make Resources the canonical persistent empirical-storage contract

Controller decision: **Resources owns the durable attempt/artifact/measurement/acceptance storage contract. Eval owns measurement semantics.**

Refactor `EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` (rename only if truly necessary; prefer stability) so the canonical persistent model is explicitly:

1. **Attempt** — one provider/API/transform call, recorded whether it succeeds, errors, times out, or is refused. Every attempt has stable id, item id, provider/model/version/endpoint/workflow/lane, request/config provenance, timing, cost reference, repeat/retry metadata, and status.
2. **Artifact** — bytes produced by an attempt, when any. Derived frames/assets point to their parent artifact/trial and do not become independent trials.
3. **Measurement** — many per artifact/trial, owned semantically by Eval, preserving the exact canonical capability id, instrument/version/config, observation unit, result/absence reason, defects, evaluator cost and timestamp.
4. **Acceptance** — production acceptance/rejection and retry chain; Resources stores it but never decides it.

The persistent schema must preserve failed/refused attempts individually; aggregate reliability counters are not enough.

**Observation-unit rule:** do not invent a Resources-specific vocabulary. Store the Canon/Eval canonical vocabulary verbatim:
`frame | shot | shot_pair | sequence | whole_asset | asset_set_over_time`.
If a derived-media description is needed, add a separate derivation field; do not redefine observation units as `image`, `sampled_clip`, `whole_clip`, etc.

**Repeat vs retry:** the storage contract must distinguish them:
- `repeat_index` / `repeat_of` (or equivalent) = deliberate experimental reliability repeat;
- `retry_of_attempt_id` / retry reason = production/repair attempt caused by a prior failure.
They must never be interchangeable, because only retries belong to an accepted-outcome retry chain.

Publish a short `resources/v1/EVAL-STORAGE-HANDOFF.md` stating the exact field contract Eval must emit. Do not implement Eval code.

### R-C3 — Remove deterministic generated Git bloat

The large R5 views and the 1,000-artifact synthetic scale archive are deterministic proof artifacts, not irreplaceable evidence.

Keep in Git:
- generators/builders;
- schemas;
- validators;
- expected counts and deterministic fingerprints/hashes;
- small representative fixtures and deliberate negative controls;
- human-readable reports.

Do **not** keep tens of thousands of rebuildable JSONL rows merely because they were generated once.

Refactor validation so large views and the scale dummy archive are generated into a temporary/build directory, validated, and removed or git-ignored. The validator must prove determinism using counts + content hashes/fingerprints.

Irreplaceable future paid model outputs remain Class C and must be retained durably; this correction must not weaken that rule.

### R-C4 — Unknown source lineage must fail closed

At `source_lineage` protection level, an unknown lineage must mean **independence not established**, not "a unique new lineage because the source id differs."

Add negative controls proving:
- two known independent lineages may pass;
- a known dependent lineage fails;
- an unknown lineage in a protected comparison returns an explicit indeterminate/could-not-establish-independence result and cannot be certified clean.

Keep the existing distinction between "problem found" and "could not check."

### R-C5 — Integrate accepted Eval resource refinements without creating more acquisition families

The project still has four controlled missing packs. Fold the following requirements into those packs rather than creating separate acquisitions:

- **Product pack:** ≥48 images = 12 products × ≥4 controlled views. Design products so same-category non-match decoys exist; record declared brand-colour reference values where applicable; include curved/angled/logo-on-surface difficulty coverage where feasible.
- **Person pack:** ≥32 images = 8 identities × ≥4 views. The identities themselves must support known-match and known-non-match/decoy comparisons. No public-face scraping.
- **AV pack:** 36 clips = 24 single-speaker + 12 two-speaker, with transcripts and explicit turn boundaries. Reuse ≥12 clean clips from this pack for deterministic temporal perturbation qualification rather than creating a fifth pack, if scientifically valid.
- **Commercial pack:** 80 assets = 60 active + 20 reserve. Resources supplies candidates/rights/provenance only. Eval/humans may later establish a ≥15 known-clean subset for false-criticism calibration; Resources must not author that label.

Do not acquire any of these in this pass.

## Required verification

Run the full Resources V1 validator suite from a clean branch state. Add new negative controls for R-C4 and for the canonical storage schema where practical. Verify the large generated view/archive files are no longer required as committed inputs.

If the cloud environment cannot execute a test, say so explicitly; do not claim PASS.

## Completion criteria

This correction pass is complete only when:

1. the 15/36 wording is precise everywhere;
2. one canonical attempt/artifact/measurement/acceptance storage contract exists under Resources;
3. observation units match the canonical vocabulary exactly;
4. repeats and retries are separate concepts;
5. failed/refused attempts survive individually;
6. deterministic large generated artifacts are removed from Git and rebuilt by validation;
7. unknown lineage cannot be certified independent;
8. the four missing packs incorporate the accepted Eval refinements without scope explosion;
9. the full validator suite/negative controls are freshly run where the environment permits;
10. a correction brief is written at `resources/findings/RESOURCES-V1-CORRECTION-CONTROLLER-BRIEF.md` with exact files changed, tests run, residual blockers, and a statement that no acquisition/spend occurred.

Do not merge to `main`. Commit the correction pass on the existing Resources branch and push it.