# Canon — Handoff

**PURPOSE:** Build and test durable creative/media expertise consumable by a reasoning model.

**CURRENT STATE:** SPEC-01 (Creative IR) through SPEC-05 (Ontology) exist and are locked/frozen.
CANON-003 closed at **16 Controller-accepted books** and was merged to `main` via PR #4 — 505
SourceKnowledge objects, 54 SourceConceptSystems, 417 ontology terms, 53 concepts, 111 operational
bindings, under `knowledge/current/`. Its conclusion was that the three-layer architecture
(SourceKnowledge → source systems/ontology → OperationalBindings) should be **retained**, and that the
next revision should be one consolidated post-extraction Audit Gate.

CANON-004 designed and tested that gate against the 16-book corpus. **The Controller ADOPTED it on
25 Aug 2026** (`decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`, PR #6), and **CANON-005 has made
it authoritative**. Canon-consumption / RAG experiments remain paused until the Controller reopens
them.

**Audit Gate v0.2 — the active method and its paths:**

| What | Where |
|---|---|
| Normative procedure and schema | `canon/audit/AUDIT-GATE-v0.2.md` |
| Active records — exactly one per accepted source | `canon/audit/records/*.audit.yaml` (16), all `audit_record_version: v0.2` |
| Validator | `canon/validation/validate_audit_gate_v02.py` |
| Tests | `tests/test_validate_audit_gate_v02.py` |
| Experiment history — pointer only, nothing active | `canon/experiments/audit-gate-v0.2/README.md` |

**The gate blocks downstream consumption, not storage.** A source becomes accepted downstream
knowledge only after its extraction, systems/ontology and bindings are stable, its fresh checkpoint
is committed, its Audit Gate record is written against those exact bytes, and the Audit Gate
validator passes. **Until then — and again if its audit goes stale — it may not be used for
cross-source promotion, downstream product/application use, or Canon-consumption/retrieval.** It
remains in the repository as source evidence throughout; the gate governs use, not worth.

All **16** currently accepted books have an active, validating audit record.

**One adopted record version: `v0.2`.** The validator fails closed on anything else, including the
pre-adoption `v0.2-experimental`. There is no migration or version-negotiation machinery, and adding
a second version is a Controller decision, not something to build in advance.

**CURRENT APPROVED DECISIONS:** Audit Gate v0.2 adopted 25 Aug 2026 and authoritative; the only
authoritative spec it changed is SPEC-05 Governance rule 5. `deterministic_composition` and
`human_workflow` remain **audit application-fit vocabulary only** — neither is a SPEC-04 target type
or executor unless a later task separately establishes one. SPEC-01 v0.1 locked. SPEC-03/04/05 supersede SPEC-02 conceptually
(SPEC-02 retained as evidence). Direction reset restoring the Canon / Capability-Lab / Production
boundary accepted. CANON-003 stopped at 16 books by Controller decision
(`decisions/CANON-003-STOP-AT-16-2026-08-24.md`); Books 11 (*Master Shots*) and 12 (*The
Conversations*) are deferred reserves, not failures. *Thinking with Type* remains blocked on
structural column interleaving.

**LAST COMPLETED TASK:** `tasks/CANON-005.md` — applied the adopted Audit Gate. Amended SPEC-05
Governance rule 5 so independence for a `cross_source_concept` comes from the Audit Gate lineage
records rather than a count of distinct source ids; promoted the schema and the 16 records out of
`experiments/` into `canon/audit/`; documented the gate order authoritatively; repointed the
validator and tests. SPEC-01, SPEC-03 and SPEC-04 unchanged.

Preceding: `tasks/CANON-004.md` — designed and tested the gate, plus a Controller correction pass on
25 Aug (retain `deterministic_composition`; close the stale-audit hole with an enforced
`source_snapshot` content fingerprint; correct the independence test fixtures).

**CURRENT TASK / QUEUE:** none. CANON-005 is `needs_controller_review`. **Next work is
Controller-assigned only** — do not self-assign reserve-book integration, Canon expansion,
cross-source promotion, RAG/retrieval or Production IR.

**IMPORTANT OBSERVATIONS:**
- The old admission rule ("no IR consumer → discard") caused exclusion and distortion. Do not
  reintroduce that coupling. 44 objects across *Creativity, Inc.* and *Art & Fear* have zero Creative
  IR bindings and that is correct.
- Current source knowledge must stay source-faithful; product bindings are separate and optional.
- **Bindability is not evidence quality.** The corpus's best-binding source (*Building a StoryBrand*,
  4 Creative IR bindings from 18 objects) has its weakest support. Never rank by binding count.
- **A source id is not an independent origin.** *Grammar of the Shot* and *Grammar of the Edit* are
  companion volumes by the same authors and must not count as convergence. This is now enforced by
  SPEC-05 Governance rule 5 and by `independent_origins_ok()`, which fails closed. Independence is
  **pairwise** — a source blocked against its companion is still a good origin against everything
  else.
- **Validate with a committed instrument, not a session script.** The integration validator returns
  early on a YAML parse failure, which under-reported one book's term checks; that gap surfaced as 10
  real errors on `main` and was repaired in CANON-004.
- **An audit record is only valid for the exact bytes it audited.** If any of a book's five
  machine-consumed artifacts changes, that book's Audit Gate record fails as stale and must be
  re-run. There is deliberately no snapshot-refresh shortcut.
- **PyYAML is not installed system-wide on this machine.** Create a local `.venv` (self-ignoring) with
  `pyyaml` and `pytest` before running either validator.

**DEFERRED RESERVE SOURCES:** *Master Shots* and *The Conversations* remain reserve sources
**outside** the frozen 16-book CANON-003/004 method-test set. They were not ingested by CANON-004 or
CANON-005. They may be integrated later under the now-adopted method, which means each would need its
own fresh Audit Gate record before passing any downstream gate. That is a separate Controller-assigned
task.

**OPEN QUESTIONS:** Ontology naming convention. Runtime Canon consumption shape. Whether evidence
lineage and source lineage need joining (one source is not enough to say). Whether a different worker
writing an audit record produces the same record.

**DEPENDENCIES:** None. Routing work remains downstream of Eval's future Capability Registry.

**PROPOSED CROSS-STREAM CHANGES:** none filed. One observation the Controller may wish to forward to
Eval: a validator that aborts a unit on a parse error under-reports, and the shortfall is invisible in
its own output.

**NEXT APPROVED TASK:** none. Do not self-assign a source, an experiment or a spec edit. Wait for the
Controller's CANON-004 decision.
