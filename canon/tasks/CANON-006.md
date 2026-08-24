# Task CANON-006: Adjudicate and integrate the two deferred reserve sources

**TASK ID:** CANON-006  
**STATUS:** Controller-opened 25 Aug 2026, after CANON-005 made Audit Gate v0.2 authoritative.  
**TYPE:** bounded source-adjudication / integration task. No new source consumption.

## OBJECTIVE

Take the two source extractions that were deliberately left outside the frozen 16-book CANON-003/CANON-004 evidence set, recover only their completed source-specific work from the old lane branches, and adjudicate each under the now-authoritative Canon method.

The two reserves are:

1. Christopher Kenworthy, *Master Shots*, vol. 1, 2nd ed. — chapter 8, “Directing Attention” plus the bounded front/back matter consumed by the original worker.
2. Michael Ondaatje, *The Conversations: Walter Murch and the Art of Editing Film* — Third Conversation, complete.

The historical CANON-003 result remains **16 accepted books** forever. CANON-004’s method test remains **16 sources** forever. CANON-006 may bring the **current live Canon** to 17 or 18; it must not rewrite either historical result.

## AUTHORITATIVE CURRENT METHOD

Read first from current `main`:

- `canon/HANDOFF.md`
- `canon/audit/AUDIT-GATE-v0.2.md`
- `canon/knowledge/SPEC-03-source-knowledge.md`
- `canon/knowledge/SPEC-04-operational-bindings.md`
- `canon/knowledge/SPEC-05-knowledge-ontology.md`
- `canon/validation/validate_canon003_integrated.py`
- `canon/validation/validate_audit_gate_v02.py`
- `canon/findings/CANON-004-CONTROLLER-BRIEF.md`
- `canon/findings/CANON-005-CONTROLLER-BRIEF.md`
- `shared/COMMUNICATION-STANDARD.md`
- `coordination/RUNBOOK.md`

The accepted order is now:

1. source extraction stable;
2. source systems / ontology stable;
3. OperationalBindings stable;
4. fresh checkpoint committed;
5. Audit Gate record written against those exact source bytes;
6. Audit Gate validator passes;
7. only then may the source count as accepted downstream knowledge.

An unaudited, stale, or evidence-insufficient source can remain source evidence but cannot pass downstream promotion/use gates.

## VERIFIED LEGACY INPUTS

Do **not** assume the old lane branches are mergeable. They diverged substantially from modern `main` and contain other historical work.

### Reserve 11 — Master Shots

Legacy branch: `work/canon-003-rebalance-d`

Verified completed source-specific artifacts:

- `canon/knowledge/current/kenworthy-master-shots-ch8/`
- `canon/findings/CANON-003-book11-master-shots-findings.md`
- supporting completion evidence in `canon/findings/CANON-003-rebalance-lane-checkpoint.md`

Legacy checkpoint states book 11 is complete, validated and pushed; fresh checkpoint `2d3da5d`.

Recorded legacy counts:

- 20 SourceKnowledge objects
- 3 SourceConceptSystems
- 17 ontology terms
- 8 ontology relationships
- 3 concepts
- 6 OperationalBindings

Known source-integrity issue worth carrying into the new Audit Gate: the source text makes a colour-dependent “Color Guides” claim while the available book illustrations are greyscale, so the figure cannot discriminate the claim from its negation even though the file itself is intact.

### Reserve 12 — The Conversations

Legacy branch: `work/canon-003-b`

Verified completed source-specific artifacts:

- `canon/knowledge/current/ondaatje-conversations-ch3/`
- `canon/findings/CANON-003-book12-conversations-findings.md`
- supporting completion evidence in `canon/findings/CANON-003-lane-B-checkpoint.md`

Legacy checkpoint states book 12 is complete, validated and pushed; fresh extraction checkpoint `9e6f716`, comparison/findings checkpoint `7760953`.

Recorded legacy counts:

- 27 SourceKnowledge objects
- 3 SourceConceptSystems
- 16 ontology terms
- 6 OperationalBindings

Available representation was EPUB / `not_verified_page_level`.

Known source-shape issues worth carrying into the Audit Gate include caption-image binding loss and interview/testimony provenance.

**Critical lineage warning:** *The Conversations* is bibliographically authored by Ondaatje but substantially records Walter Murch’s speaking voice. The current live Canon already contains Murch’s *In the Blink of an Eye*. Distinct `source_id` or distinct bibliographic author **must not** be used to manufacture independent convergence between these sources.

## BRANCH DISCIPLINE

1. Start a fresh branch from current `origin/main`, preferably `work/canon-006-reserves`.
2. Do **not** merge either legacy branch.
3. Do **not** cherry-pick broad lane commits that contain unrelated source directories or stale shared files.
4. Recover only the exact source-specific artifacts required for these two reserves, plus source-specific finding material needed to preserve their audit trail.
5. Before importing, compare the final legacy source directory against the stated fresh checkpoint/history enough to establish that later lane work did not silently reinterpret the frozen extraction. Record what was checked.

If clean extraction of the source-specific artifacts is impossible without importing unrelated stale lane state, stop and explain rather than broad-merging.

## ADJUDICATION STEPS — RUN PER SOURCE

### A. Recover the frozen source record

Bring the source-specific knowledge directory onto the fresh current-main branch without changing claim meaning merely to fit modern expectations.

Preserve original ids where they do not collide.

Do not re-open or re-consume the original copyrighted source unless the committed legacy evidence is insufficient to perform the authoritative Audit Gate. If re-opening becomes necessary, stop and explain exactly why before doing it.

### B. Validate source-layer compatibility

Mechanically validate the recovered directory against the current SPEC-03/04/05 constraints.

The historical `validate_canon003_integrated.py` is specifically a validator for the frozen 16-book CANON-003 set. **Do not change its 16-entry `ACCEPTED_BOOK_DIRS` merely to make the new live corpus fit.** Its historical output must remain stable.

For the two new directories, use the committed validation logic to check their individual files and mechanically check id uniqueness against the whole current live corpus.

If current tooling cannot mechanically prove the live-corpus invariants without a scratchpad-only script, add the smallest committed **live-corpus validator/wrapper** needed for future post-CANON-003 sources. Do not rewrite the historical CANON-003 validator’s meaning.

### C. Freeze and Audit Gate each source

After the recovered source record is stable and committed, create one authoritative `audit_record_version: v0.2` record under:

`canon/audit/records/`

Populate all five adopted Audit Gate areas from committed evidence:

1. representation integrity;
2. evidence / claim origin;
3. application fit across all seven consumers;
4. lineage / pairwise independence;
5. technology contingency.

Compute the authoritative `source_snapshot` only after the source directory is frozen.

Do not refresh or invent snapshot values merely to make validation pass.

### D. Lineage must be truthful

For *Master Shots*, assess actual relationships to existing film/cinematography sources; shared domain or conventional Hollywood grammar alone does not prove dependence.

For *The Conversations*, explicitly test its relationship to `murch-blink-p1-25`.

The current Audit Gate relation vocabulary is:

- `shared_author`
- `same_series`
- `companion_volume`
- `derivative_of`
- `cites_source`
- `shares_publisher_only`
- `no_known_relation`

Do **not** misuse one of those labels to hide a different relationship. In particular, do not call Murch a bibliographic author if the source does not support that, and do not call one source `derivative_of` the other unless that is actually what the evidence says.

If the known “same speaking practitioner / different bibliographic author” relationship cannot be represented truthfully by Audit Gate v0.2, that is a **method-compatibility finding**. Do not silently mark the two sources independent and do not unilaterally change the authoritative Audit Gate vocabulary or SPEC-05.

In that case:

- integrate neither source as accepted downstream knowledge merely to hit 18;
- preserve any safely recovered source evidence on the working branch if useful;
- file a precise Controller proposal for the minimum method amendment required, including validator/test consequences;
- stop for Controller decision.

A count of 17 is better than a dishonest 18; a blocked source is a valid adjudication result.

### E. Historical boundaries

Do not edit the historical claims that:

- CANON-003 stopped at 16;
- CANON-004 was tested against 16;
- CANON-005 promoted 16 existing audits.

Instead distinguish:

- **historical method-test corpus:** 16;
- **current live accepted Canon after CANON-006:** whatever number actually passes the authoritative gate.

## FINDINGS / STATUS OUTPUT

Create:

- `canon/findings/CANON-006-CONTROLLER-BRIEF.md`

It must report per reserve:

- exact legacy source branch and frozen artifact imported;
- whether the source files were changed, and why;
- final SourceKnowledge / systems / terms / relationships / concepts / bindings counts;
- current-source mechanical validation result;
- Audit Gate result and active audit-record path;
- representation-integrity findings;
- evidence-origin findings of note;
- application-fit summary;
- pairwise lineage verdicts, especially Conversations ↔ Murch;
- technology-contingency result;
- accepted-downstream / source-evidence-only / blocked verdict;
- exact live Canon count after the task.

Update `canon/HANDOFF.md` only with facts actually established by this task.

Do not rewrite CANON-003 or CANON-004 synthesis documents to include the reserves.

## VERIFICATION

Before returning, run fresh from the final branch head:

1. historical 16-source validator — it must still pass unchanged:
   `python canon/validation/validate_canon003_integrated.py --root .`
2. authoritative Audit Gate validator:
   `python canon/validation/validate_audit_gate_v02.py --root .`
3. full relevant tests:
   `python -m pytest tests/ -q`
4. committed live-corpus validation, if one is added or already exists.

Mechanically confirm:

- no whole legacy lane branch was merged;
- no unrelated legacy source directory was imported;
- no historical 16-source decision/synthesis was rewritten;
- every accepted live source has exactly one active v0.2 Audit Gate record;
- no accepted audit is stale;
- ids are unique across the live corpus;
- no source book/page/image was committed;
- no GitHub Actions workflow was added;
- no model/API/generation spend occurred.

Report actual commands, exit codes and final corpus counts. Do not rely on a previous lane’s old “validated” statement as fresh verification.

## NON-GOALS

CANON-006 does not:

- consume any newly discovered Work source;
- start the 22-source expansion portfolio;
- acquire source material;
- build RAG/retrieval;
- run Canon-vs-vanilla experiments;
- build Production IR;
- create cross-source concepts;
- change Creative IR;
- modify Eval or Resources files;
- spend on models/APIs;
- reopen the source-selection research.

## STOP CONDITIONS

Return to Controller before broadening scope if:

- either recovered legacy source does not actually represent a complete/frozen extraction;
- either source requires re-opening copyrighted material to establish audit truth;
- current SPEC-03/04/05 validation exposes a substantive meaning conflict rather than a mechanical legacy-format correction;
- The Conversations ↔ Murch lineage cannot be represented truthfully in Audit Gate v0.2;
- accepting a reserve would require changing an authoritative spec or Audit Gate controlled vocabulary;
- a whole stale lane branch would need to be merged;
- source ids materially collide with current live ids.

## DELIVERABLE

Open one PR against current `main`, preferably from `work/canon-006-reserves`.

Return the Controller Brief and stop. Do not self-assign Wave 1 or any new Canon source.
