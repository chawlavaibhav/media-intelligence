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

## Public data with no stated licence
Licence silence is **not** automatically a rejection.

For an already-approved source, Resources may download or scrape publicly accessible, ungated data
for **internal research and evaluation only** when all of these hold:

- no login, paywall, click-through agreement, API key or access-control bypass is required;
- no explicit licence or site term prohibits the intended automated access/download or internal use;
- the source, URL, access date, known terms and the fact that rights are **not stated / not verified**
  are recorded accurately;
- the material is not redistributed, shipped to customers, used as training data, or treated as
  cleared production content;
- scraping is rate-limited and does not evade technical blocks or anti-bot controls.

This policy is permission to **acquire for bounded internal evaluation**, not a claim that copyright
or commercial-use rights exist. If a later use needs redistribution, training, customer delivery or
production use, rights must be reviewed again.

## Decisions requiring Controller review
Any materially new dataset family before download. Any explicit licence/terms conflict, gated access,
or legal ambiguity not covered by the public-data rule above. Any decision that would make an
"independent" holdout non-independent (for example selecting examples because they match a Canon
principle under test).

## Autonomy rules
Once a dataset is approved: download, checksum, validate, manifest, and deterministic sampling may
run `autonomous_queue`. Choosing *which* dataset, or changing sampling strategy mid-stream, is not.

## Mandatory stop conditions
Per `shared/AUTONOMY-POLICY.md`. Explicitly: gated access; explicit licence/terms conflict; storage
budget excess; an unexpected dataset property that breaks independence. **Absence of a stated
licence alone is not a stop** for public, ungated, internal-only acquisition under the rule above.

## Controller Brief requirement
Every completed task, using `shared/templates/CONTROLLER-BRIEF-TEMPLATE.md`.

## Cross-stream change protocol
`resources/PROPOSED-INTEGRATION-CHANGE-<ID>.md`.

**You are an execution/research worker, not the overall project architect.**
