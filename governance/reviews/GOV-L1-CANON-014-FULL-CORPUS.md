# Governor Level-1 Review — CANON-014 Full Canon Corpus

**Review mode:** Level 1 — task / PR integrity review (`governance/GOVERNOR-CONTRACT.md` §3a).  
**Authorisation:** `coordination/decisions/CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md`.  
**Audited `main`:** `bf02dd1f31a9b1d0b790f4a2a09a68f3b39748fa`.  
**Branch reviewed:** `work/canon-014-final-full-canon` at
`bfd0fcd1926c991a5cd626d2e96bef56189a66ff` before this review artifact was added.  
**PR:** #68.  
**Date:** 30 Aug 2026.  
**Spend / provider calls:** none for this review.

A Governor verdict is only about repository coherence. It does not certify that the Canon
methodology is scientifically correct, that every source claim is true, or that the Q&A is a
benchmark. Domain correctness remains with Canon + Controller.

# Verdict: PASS WITH NON-BLOCKING NOTES

No repository-coherence defect was found that should block PR #68. The merge is coherent provided
the Controller uses PR #68 as the sole integration branch and does not merge donor PR #66 or #67
afterward.

## 1. Scope and branch shape — coherent

Mechanical comparison against current `main` at the reviewed head shows:

- **203 changed files** before this review artifact;
- **0 files changed under `eval/**` or `resources/**`;**
- **0 raw media/book binaries** added by the diff;
- the only non-Canon integration changes are the Writer Controller's:
  - `PROJECT-MEMORY.md`;
  - `coordination/CONTROL-STATE.md`;
  - `coordination/decisions/CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md`.
- the branch is **8 commits ahead / 0 behind** the audited `main` at the reviewed head.

The Controller-owned changes are integration bookkeeping, not a Canon worker crossing stream
boundaries. They make the state documents true at the moment PR #68 lands.

## 2. Accepted / HOLD separation — independently reproduced

From the branch tree, independently of the Markdown report:

- **24** direct source directories exist under `canon/knowledge/current/`;
- **18** direct source directories exist under `canon/candidates/canon-014/`;
- **24** Audit Gate records exist under `canon/audit/records/`;
- **0** source directory exists in both accepted and candidate trees;
- **0** accepted source lacks an Audit Gate record;
- **0** HOLD/candidate source has an Audit Gate record.

That is the central epistemic invariant of CANON-014 and it holds mechanically.

The review therefore reproduces the headline state:

> **24 accepted + 18 HOLD/candidate = 42 represented sources.**

This does not mean 42 accepted sources.

## 3. Q&A corpus — counts reproduced from the committed manifest

`canon/qa/canon-014/QA-MANIFEST.json` records:

- **23 banks**;
- **1,028 Q&A items**;
- **418 / 1,028 = 40.7%** marked as requiring application;
- **108** items from accepted sources;
- **920** items from HOLD sources;
- **5 accepted-source banks / 18 HOLD-source banks**.

The manifest explicitly labels the corpus grounded, ungraded and uncalibrated. Nothing in the
Controller integration decision or current-state refresh upgrades it to benchmark ground truth or
evidence that Canon improves outcomes.

## 4. Corpus fingerprints — experiment boundary remains explicit

`canon/knowledge/CANON-CORPUS-INDEX.yaml` preserves three separate top-level experimental
fingerprints:

- accepted Canon:
  `a9cee40fb433adc08ac98ba7c87e1ead790f60aa71d184327cc5e97f59ed7eb9`;
- full knowledge corpus:
  `cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60`;
- Q&A corpus:
  `1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd`.

`PROJECT-MEMORY.md`, `CONTROL-STATE.md` and the Controller integration decision now point future
experiments to the corpus index and require status-aware handling if HOLD material is exposed.

**Non-blocking note G14-N1 — secondary Q&A checksum vocabulary.**  
`QA-MANIFEST.json` also contains an internal `corpus_fingerprint.combined_digest`
(`25ac8bbc173d1593eae562d93802bd7bdbb0212a36b4a3cdf4279363878148c8`) produced by a different
algorithm (`sha256-of-sorted-bankname-and-content`). The index's Q&A fingerprint uses
`sha256-of-sorted-path-and-content` and is the fingerprint the experiment-facing corpus index
declares. These are different checksums, not contradictory bytes, but the shared word
“corpus_fingerprint” could confuse a future reader. **For experiments, use the index fingerprint
`1313c0…` unless a later decision explicitly says otherwise.** Severity: Low; no merge block.

## 5. Current-state coherence — corrected before merge

Without integration bookkeeping, merging PR #68 would have left `PROJECT-MEMORY.md` saying
“19 live accepted sources”. The Writer Controller corrected that on this branch before this review.

The reviewed branch now records coherently:

- **24 accepted sources**;
- **18 durable HOLD/candidates**;
- **1,028 Q&A items**;
- ordinary runtime retrieval remains accepted-only;
- any experiment exposing HOLD/Q&A must freeze exact fingerprints and preserve source status;
- CANON-014 is independent of T2A/T2B authorisation and does not itself authorise model/provider
  calls.

The 29-Aug Media Factory programme reset remains the active programme authority. CANON-014 does not
silently reopen, cancel or replace it.

## 6. Historical / architectural integrity — clean in scope

The branch:

- does not add Capability Registry rows;
- does not create Production IR / Planner;
- does not modify Eval or Resources;
- does not enable ordinary runtime retrieval of candidate/HOLD material;
- does not commit raw source books;
- does not merge the prior experimental package wholesale;
- retains HOLD sources as a separate state rather than relabelling them accepted.

The Controller decision explicitly states that candidate retrieval, model experiments, visual-pass
programmes and provider spend are **not authorised by this merge**.

## 7. Validation evidence — what was and was not independently rerun

The CANON-014 branch reports:

- Audit Gate: **24 records, 0 errors**;
- live schema validator: **24 dirs, 3 errors**, all pre-existing in
  `sutherland-alchemy-introduction`;
- candidate schema validator: **18 dirs, 0 errors**;
- Q&A validator: **23 banks / 1,028 items / 0 errors**;
- pytest subset: **179 passed / 113 subtests**, with
  `tests/test_request_freeze_gates.py` excluded because of the known CANON-010 collection defect.

This Governor session did **not** execute those Python test suites through a runtime, so those exact
test-run figures remain **worker-reported**. It independently reproduced the branch-tree
accepted/HOLD/audit separation and the Q&A counts above.

**Non-blocking note G14-N2 — pre-existing Sutherland schema defects.**  
Three accepted concept systems in `sutherland-alchemy-introduction` still lack provenance. The
defect predates CANON-014, is explicitly carried in the Controller decision, and was not hidden or
rewritten here. It needs its own Canon reopening/audit decision. Severity: Medium; routed, not a
CANON-014 merge block.

**Non-blocking note G14-N3 — full pytest collection defect.**  
The branch documents that `tests/test_request_freeze_gates.py` hardcodes a container path and
executes its runner at module scope, aborting normal pytest collection. The Controller decision
carries this forward as a separate owning fix. Severity: Medium; pre-existing, not a CANON-014 merge
block.

## 8. Merge posture

**Governor advice: merge PR #68.**

PR #68 is the sole integration surface for CANON-014. PR #66 and PR #67 are donor history and must
not be merged afterward.

After merge, the durable state is:

- CANON-014 closed;
- 24 accepted Canon sources;
- 18 HOLD/candidate sources;
- 1,028 grounded/ungraded/uncalibrated Q&A items;
- ordinary runtime candidate retrieval still disabled;
- future Canon experiments must name the exact corpus fingerprint(s) they expose.

**Blocking findings: none.**
