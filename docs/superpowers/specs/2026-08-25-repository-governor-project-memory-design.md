# Repository Governor + Project Memory Design

Date: 2026-08-25
Status: APPROVED
Scope: governance/control plane only

## 1. Problem

The repository's domain work is broadly intact, but its operational state has drifted across coordination files, stream handoffs, task briefs, external research artifacts, and long-lived chat context. Fresh sessions can currently encounter contradictory statements about what is active, complete, historical, or authoritative.

The reset must solve the recurrence mechanism, not just clean the present mess.

## 2. Core invariants

1. **GitHub is project memory. Chat is execution context only.**
2. A fresh competent agent with zero prior chat history must be able to reconstruct the authoritative project state from GitHub alone.
3. `PROJECT-MEMORY.md` is the canonical human-readable entry point for current project context.
4. Detailed domain artifacts remain authoritative for their own underlying facts; `PROJECT-MEMORY.md` summarizes and links rather than duplicating them exhaustively.
5. Accepted architectural and strategic decisions are represented as durable repository records, not inferred from chat.
6. Historical facts remain historical; later work must not rewrite earlier baselines to look as though they always reflected the current state.
7. The Governor detects contradictions and context drift continuously; workers continue their existing domain workflows.

## 3. Roles

### Controller

Owns strategic direction, architecture, task authorization, acceptance/rejection decisions, and final merge decisions.

### Canon / Eval / Resources workers

Continue their current workflows and ownership boundaries. This governance design does not make them maintain the master project memory and does not change their domain responsibilities.

### Repository Governor

A fifth, independent role. It is not a Canon/Eval/Resources worker and does not own project strategy.

Responsibilities:

- inspect GitHub after every meaningful task/PR for repository coherence;
- identify stale or contradictory current-state claims, broken paths, duplicated truth, unintended architectural/method changes, and operational documentation drift;
- maintain the curated rolling `PROJECT-MEMORY.md`;
- produce periodic repository-health audits covering documentation hygiene, code quality, context burden, obsolete artifacts/branches, duplicated state, and opportunities for mechanical validation;
- flag issues to the Controller and originating stream rather than silently fixing domain-owned artifacts.

The Governor may write only the governance/control layer unless the Controller explicitly authorizes otherwise.

## 4. PROJECT-MEMORY.md

`PROJECT-MEMORY.md` is a curated rolling synthesis, not an append-only diary.

It must be understandable to a reader with zero conversation history.

It should contain:

1. project thesis and success metric;
2. current high-level architecture and stream boundaries;
3. non-negotiable/frozen decisions that materially constrain current work;
4. current state of Canon, Eval, Resources, acquisition/external research, and major implementation objects;
5. important lessons/results already established;
6. current limitations, unresolved questions, and stop conditions;
7. active work and exact next gates;
8. concise historical milestones with links to deeper task/decision/findings records;
9. an authority map pointing to the deeper files that prove or define each major area;
10. verification/provenance qualifiers where material: merged repo fact, Controller-inspected, human-reviewed, agent-reported verification, external research snapshot, unresolved.

It must not contain:

- full task-by-task transcripts;
- long worker narratives already preserved elsewhere;
- copied source material;
- speculative recommendations presented as decisions;
- manually duplicated counts or hashes when they can instead be linked to or generated from authoritative artifacts;
- chat-only facts that have not been accepted into GitHub.

The Governor may compress old sections as the project grows, preserving meaning and links while reducing context burden.

## 5. Authority hierarchy

The intended relationship is:

- `PROJECT-MEMORY.md`: canonical narrative map of what is true now and why it matters;
- domain artifacts/specs/records: evidence and detailed authority for their own contents;
- decision records: durable authority for deliberate Controller decisions;
- historical tasks/findings: forensic evidence, not automatically current-state authority;
- chat/session memory: non-authoritative.

If `PROJECT-MEMORY.md` conflicts with underlying committed evidence, the contradiction is a governance defect that must be resolved. The document is not allowed to override evidence merely because it is the entry point.

## 6. Governor review cadence

### Per meaningful task/PR

The Governor performs a bounded integrity review focused on the change and collateral state drift.

Minimum questions:

- Does the work leave GitHub internally coherent?
- Did any current-state document become stale?
- Did a historical baseline get mutated instead of superseded?
- Did the worker introduce an unauthorized architecture/method change?
- Do paths, hashes, counts, generated/materialized artifacts and documented state agree where mechanically checkable?
- Does `PROJECT-MEMORY.md` need a small update because project truth materially changed?

Governor verdict is constrained to:

- `PASS`
- `PASS WITH NON-BLOCKING NOTES`
- `BLOCK` with evidence-backed blocking inconsistencies

The Governor must not use routine integrity review as a pretext to redesign methodology.

### Periodic repository-health audit

Run weekly or after roughly 5-10 meaningful merged tasks, whichever comes first.

Audit scope includes:

- stale or contradictory operational docs;
- code quality and complexity drift;
- oversized context/handoff files;
- dead or obsolete documentation;
- stale branches and abandoned work markers;
- duplicate state representations;
- naming/terminology drift;
- test coverage/integrity gaps;
- opportunities to derive state mechanically rather than maintain it manually;
- whether `PROJECT-MEMORY.md` remains concise enough to bootstrap a fresh agent.

## 7. Write boundaries

The Governor reads the entire repository.

By default it may write:

- `PROJECT-MEMORY.md`
- `governance/**`
- explicit supersession/status markers in coordination documentation when included in an approved hygiene task

It does not directly modify Canon knowledge, Eval batteries/results, Resources datasets/manifests, domain implementation code, or methodology/specs owned by another stream solely because it found an inconsistency. Those issues are returned to the originating stream or Controller.

## 8. External research / ChatGPT Work

External research remains useful but is not automatically authoritative project state.

The Governor records it in `PROJECT-MEMORY.md` only with a clear status such as:

- external research snapshot;
- Controller-accepted input;
- unresolved;
- superseded.

If an external workbook/report conflicts with current GitHub truth, the Governor flags the conflict rather than treating the external artifact as a competing source of truth.

## 9. Fresh-session bootstrap

A fresh session should start from GitHub, not a pasted chat summary.

Controller bootstrap:

1. `PROJECT-MEMORY.md`
2. `coordination/PROJECT-CONTRACT.md`
3. relevant decision/current-state records as linked by the memory

Worker bootstrap:

1. `PROJECT-MEMORY.md`
2. `coordination/PROJECT-CONTRACT.md`
3. stream charter
4. assigned task

Governor bootstrap:

1. `PROJECT-MEMORY.md`
2. `governance/GOVERNOR-CONTRACT.md`
3. current `main`
4. task/PR under review

A session is allowed to persist for convenience, but no important project fact may depend on that persistence.

## 10. First cleanup / GOV-001 intent

The first Governor task is an unusually thorough repository hygiene and state-reconstruction pass against the frozen current `main`, not a routine review.

It must:

- reconstruct authoritative current state from committed GitHub evidence;
- create the first `PROJECT-MEMORY.md`;
- create `governance/GOVERNOR-CONTRACT.md` from this approved design;
- exhaustively audit all current operational/state documents for stale, contradictory, oversized, historical, ambiguous, or duplicated current-state claims;
- explicitly classify each audited operational/state document as current authority, supporting/current, historical, superseded, or requiring correction;
- add explicit supersession/current-status markers where necessary instead of reorganizing or deleting large portions of history;
- bring the central coordination layer forward so a fresh session cannot mistake old state for current state;
- preserve all domain evidence, historical baselines, task records, source knowledge, Eval artifacts, and Resources artifacts;
- avoid new Canon/Eval/Resources methodology or product architecture work;
- produce a dated governance audit report describing every material inconsistency found and how it was resolved, marked historical, or routed back to the owning stream/Controller.

The cleanup must prefer targeted corrections and clear authority markers over large-scale file moves or cosmetic repository reorganization.

## 11. Success criteria for the reset

The reset is successful when:

- a fresh agent can understand the project and current state from GitHub alone;
- `PROJECT-MEMORY.md` provides the concise canonical narrative context;
- stale historical documents cannot reasonably be mistaken for live operational truth;
- current Canon/Eval/Resources state is represented without contradictions;
- chat is unnecessary for project reconstruction;
- the Governor has a durable protocol for catching future state drift after tasks and during periodic audits;
- no domain work was silently rewritten during governance cleanup.
