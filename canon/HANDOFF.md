# Canon — Handoff

**PURPOSE:** Build and test durable creative/media expertise consumable by a reasoning model.

**CURRENT STATE:** SPEC-01 (Creative IR) through SPEC-05 (Ontology) exist and are locked/frozen.
CANON-003 closed at **16 Controller-accepted books** and was merged to `main` via PR #4 — 505
SourceKnowledge objects, 54 SourceConceptSystems, 417 ontology terms, 53 concepts, 111 operational
bindings, under `knowledge/current/`. Its conclusion was that the three-layer architecture
(SourceKnowledge → source systems/ontology → OperationalBindings) should be **retained**, and that the
next revision should be one consolidated post-extraction Audit Gate.

CANON-004 has designed and tested that gate against the 16-book corpus. It is complete and awaiting a
Controller decision. Canon-consumption / RAG experiments remain paused until the Controller reopens
them.

**CURRENT APPROVED DECISIONS:** SPEC-01 v0.1 locked. SPEC-03/04/05 supersede SPEC-02 conceptually
(SPEC-02 retained as evidence). Direction reset restoring the Canon / Capability-Lab / Production
boundary accepted. CANON-003 stopped at 16 books by Controller decision
(`decisions/CANON-003-STOP-AT-16-2026-08-24.md`); Books 11 (*Master Shots*) and 12 (*The
Conversations*) are deferred reserves, not failures. *Thinking with Type* remains blocked on
structural column interleaving.

**LAST COMPLETED TASK:** `tasks/CANON-004.md` — Post-Extraction Audit Gate v0.2, plus a Controller
correction pass on 25 Aug (retain `deterministic_composition`; close the stale-audit hole with an
enforced `source_snapshot` content fingerprint; correct the independence test fixtures; sync with
`main` at `8e99785`). Deliverables:
`findings/CANON-004-audit-gate-design.md`, `findings/CANON-004-CONTROLLER-BRIEF.md`,
`experiments/audit-gate-v0.2/` (candidate schema + 16 records), `validation/validate_audit_gate_v02.py`,
`tests/test_validate_audit_gate_v02.py`.

**CURRENT TASK / QUEUE:** none. CANON-004 is `needs_controller_review`. The Controller must choose
ADOPT / ADOPT WITH REDUCTION / REVISE AND RETEST / REJECT. On an adopt, a small follow-on task applies
the single SPEC-05 rule and the procedure step — CANON-004 deliberately does not apply them.

**IMPORTANT OBSERVATIONS:**
- The old admission rule ("no IR consumer → discard") caused exclusion and distortion. Do not
  reintroduce that coupling. 44 objects across *Creativity, Inc.* and *Art & Fear* have zero Creative
  IR bindings and that is correct.
- Current source knowledge must stay source-faithful; product bindings are separate and optional.
- **Bindability is not evidence quality.** The corpus's best-binding source (*Building a StoryBrand*,
  4 Creative IR bindings from 18 objects) has its weakest support. Never rank by binding count.
- **A source id is not an independent origin.** *Grammar of the Shot* and *Grammar of the Edit* are
  companion volumes by the same authors and must not count as convergence.
- **Validate with a committed instrument, not a session script.** The integration validator returns
  early on a YAML parse failure, which under-reported one book's term checks; that gap surfaced as 10
  real errors on `main` and was repaired in CANON-004.
- **An audit record is only valid for the exact bytes it audited.** If any of a book's five
  machine-consumed artifacts changes, that book's Audit Gate record fails as stale and must be
  re-run. There is deliberately no snapshot-refresh shortcut.
- **PyYAML is not installed system-wide on this machine.** Create a local `.venv` (self-ignoring) with
  `pyyaml` and `pytest` before running either validator.

**OPEN QUESTIONS:** Ontology naming convention. Runtime Canon consumption shape. Whether evidence
lineage and source lineage need joining (one source is not enough to say). Whether a different worker
writing an audit record produces the same record.

**DEPENDENCIES:** None. Routing work remains downstream of Eval's future Capability Registry.

**PROPOSED CROSS-STREAM CHANGES:** none filed. One observation the Controller may wish to forward to
Eval: a validator that aborts a unit on a parse error under-reports, and the shortfall is invisible in
its own output.

**NEXT APPROVED TASK:** none. Do not self-assign a source, an experiment or a spec edit. Wait for the
Controller's CANON-004 decision.
