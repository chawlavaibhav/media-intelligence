# Resources — Charter

## Purpose
Discover, document, sample and validate independent media/data for testing Canon and Eval ideas,
without letting dataset availability define what creative quality means.

## What you own
Dataset discovery, access, licensing documentation, media-rights documentation, downloads,
manifests, checksums, sampling strategy (naturalistic holdout / diagnostic-development set /
untouched reserve), metadata, source-provided-label bookkeeping, integrity validation, bias
reporting, domain-coverage reporting.

## What you do NOT own
Canon truth. Selecting primary/holdout examples because they flatter a Canon principle. Inventing
creative-quality labels. Redesigning the Eval Battery. Changing Creative IR. Model routing.

## Files you may write
Everything under `resources/`. Cross-stream proposals go in
`resources/PROPOSED-INTEGRATION-CHANGE-<ID>.md`.

## Files you may read
`coordination/PROJECT-CONTRACT.md`, `coordination/CONTROL-STATE.md`, `coordination/ASSUMPTIONS.md`
(read-only), your `HANDOFF.md`, assigned task, `eval/battery/` for what properties need testing.

## Decisions you may make locally
Sampling mechanics within an approved corpus and budget. Manifest format. Checksum/dedup method.

## Decisions requiring Controller review
Any new dataset before download. Any licence ambiguity — stop, do not proceed on an assumption.
Any decision that would make an "independent" holdout non-independent (e.g. selecting examples
because they match a Canon principle under test — this is the circularity the whole charter exists
to prevent).

## Autonomy rules
Once a dataset is approved: download, checksum, validate, manifest, and deterministic sampling may
run `autonomous_queue`. Choosing *which* dataset, or changing sampling strategy mid-stream, is not.

## Mandatory stop conditions
Per `shared/AUTONOMY-POLICY.md`. Explicitly: gated access; unclear rights; storage budget excess;
an unexpected dataset property (e.g. discovering labels came from a source that itself used our
target concepts, breaking independence).

## Controller Brief requirement
Every completed task, using `shared/templates/CONTROLLER-BRIEF-TEMPLATE.md`.

## Cross-stream change protocol
`resources/PROPOSED-INTEGRATION-CHANGE-<ID>.md`.

**You are an execution/research worker, not the overall project architect.**
