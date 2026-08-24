# Task CANON-004: Post-Extraction Audit Gate v0.2

**TASK ID:** CANON-004  
**STATUS:** Controller-opened 24 Aug 2026; design/test task only. Authoritative SPEC-03/04/05 changes are **not** pre-authorized.

## OBJECTIVE

Turn CANON-003's 16-book synthesis into one concrete, minimal method revision proposal: a **Post-Extraction Audit Gate** that runs after source knowledge is stable and before cross-source promotion or downstream product use.

The task must design the gate, exercise it against the already-integrated 16-book CANON-003 corpus using repository evidence, and determine the minimum schema/method changes actually required. It must not acquire or consume new books to make the design look stronger.

## WHY NOW

CANON-003 produced a clear pattern: the core separation between SourceKnowledge, source systems/ontology and OperationalBindings worked, but the source-first method stopped forcing several useful second-order questions.

The synthesis identified four questions that need a mandatory structured pass after source freeze:

1. What did the source representation make unavailable or misleading?
2. Where did the evidence/claim actually originate?
3. What, if anything, can the current product use without distorting the source?
4. Are apparently agreeing sources genuinely independent?

CANON-004 exists to formalise that second look without reintroducing the old mistake of forcing product bindings into source truth.

## AUTHORITATIVE INPUTS

Read first:

- `canon/findings/CANON-003-multi-source-synthesis.md`
- `canon/findings/CANON-003-CONTROLLER-BRIEF.md`
- `canon/findings/CANON-003-INTEGRATION-VALIDATION.md`
- `canon/findings/CANON-003-batch-issue-ledger.md`
- lane checkpoints/issues integrated under `canon/findings/`
- current `SPEC-03`, `SPEC-04`, `SPEC-05`
- `shared/COMMUNICATION-STANDARD.md`

The 16 integrated CANON-003 knowledge directories are the test corpus. Their source claims are treated as frozen evidence; CANON-004 must not silently reinterpret or rewrite them.

## CORE DESIGN CONSTRAINT

The Audit Gate is a **post-extraction layer**, not a new excuse to contaminate SourceKnowledge with product policy.

Order must remain:

1. source extraction becomes stable;
2. source systems/ontology become stable;
3. source record is frozen for the audit;
4. Audit Gate runs;
5. only then may cross-source promotion, product/application decisions or later Canon-consumption work use the audited record.

An audit is allowed to conclude:

- `no current binding`;
- `independence not established`;
- `visual/page evidence structurally unavailable`;
- `evidence origin unresolved`;
- `technology contingency uncertain`.

Those are valid results, not failures to be filled with guesses.

## REQUIRED AUDIT OUTPUTS

### A. Source / visual integrity

The proposal must distinguish the failure shapes CANON-003 actually observed rather than collapsing them into one risk score. At minimum test whether it can represent:

- authored page available;
- no authored page / reflowed source;
- converted or false-page representation;
- headings or text carried only as image/SVG artwork;
- figure-contained text absent from text extraction;
- colour or another required visual dimension destroyed by the copy;
- figure inspected but claim still underdetermined;
- figure self-contained such that loss of page layout is immaterial;
- inspected source with no claim-bearing visual argument.

The output should describe representation and consequence. Do **not** turn it into a generic numeric visual-quality score unless evidence demonstrates one is useful.

### B. Evidence and claim origin

The proposal must make the following distinguishable and machine-readable without treating them as a credibility ranking:

- author's/source's own reported measurement;
- named or attributable third-party study/evidence reported by the source;
- source claims measurement/testing but supplies no result adequate to inspect;
- mixed own + third-party evidence within one source/object context;
- source author states a claim directly;
- source quotes or reports a third party approvingly;
- unresolved origin where the source does not allow a stronger statement.

The design must show how this relates to, rather than duplicates, existing evidence characteristics such as `empirical_within_source`.

### C. Application / product-fit audit

After source freeze, explicitly ask whether knowledge informs any current consumer:

- Creative IR;
- future Production IR / physical production;
- evaluation;
- governance;
- benchmark design;
- deterministic composition or other already-defined executor classes.

This audit **must not require a binding**. `no current binding` is valid and must remain distinguishable from `not audited`.

The task should demonstrate that the useful attention from the old mandatory-binding workflow can be recovered without returning to one-binding-per-object behaviour.

### D. Source lineage / independence

The proposal must represent enough lineage to stop source-id count from masquerading as independent convergence.

At minimum exercise:

- two different books by the same authors / companion series (*Grammar of the Shot* + *Grammar of the Edit*);
- a genuinely separate source agreeing on a related concept (e.g. Murch vs the Grammar books where applicable);
- derivative/reported evidence where one source is relaying another origin;
- unknown lineage.

The design must state what counts as an independent origin for cross-source promotion and what does not. It should not automatically merge or promote concepts merely because independence is established.

## SUPPORTING PROCEDURAL CHECKS

The same Audit Gate proposal must also include:

### Technology contingency for older technical sources

For sources where age/technology is relevant, explicitly ask whether a claim is:

- durable mechanism/principle;
- technology-contingent;
- historical convention/culturally bounded;
- uncertain.

Reuse existing vocabulary where it already works. Add schema only where representation is genuinely impossible.

### Mechanical acceptance

Use the committed CANON integration validator as the starting point. Any new experimental audit representation must have a committed validator/test fixture before being treated as viable.

Do not create an auto-running notification-heavy GitHub Actions workflow for this task. Validation can run in a controlled environment; the validator/tests themselves must be committed.

## TEST METHOD

Use the existing 16-book corpus only.

1. Inventory each known CANON-003 issue against the four audit areas.
2. Draft the smallest candidate audit representation.
3. Create experimental audit records under a clearly non-authoritative path, e.g. `canon/experiments/audit-gate-v0.2/`.
4. Apply the candidate to all 16 accepted sources **from existing repository evidence**. Re-open source books only if a repository record is insufficient to test the representation; record that need rather than inventing an answer.
5. Mechanically validate the experimental records.
6. Report where the candidate is expressive, redundant, ambiguous or too burdensome.
7. Revise the candidate only from cross-corpus evidence, not one awkward source.
8. Produce one final proposal and Controller decision brief.

This is a method-design experiment, not a new extraction batch.

## FIXED NON-GOALS

CANON-004 does **not**:

- consume new books or finish deferred Books 11–12;
- acquire copyrighted sources;
- change Creative IR / SPEC-01;
- build Production IR;
- run RAG/Canon-consumption experiments;
- run image/video model benchmarks;
- revisit the stopped Devanagari calibration;
- automatically create cross-source canonical concepts;
- score authors or books for truth/quality;
- translate physical-production knowledge into generative prompts;
- rewrite the 16 accepted SourceKnowledge corpora for cosmetic consistency;
- apply authoritative SPEC-03/04/05 changes without a final Controller decision.

## DELIVERABLES

Required:

- `canon/findings/CANON-004-audit-gate-design.md`
- experimental 16-source audit records under `canon/experiments/audit-gate-v0.2/`
- committed validator + tests for the candidate audit representation
- `canon/findings/CANON-004-CONTROLLER-BRIEF.md`

The design document must include:

- candidate data model;
- field-by-field rationale tied to CANON-003 observations;
- examples from materially different source shapes;
- burden/complexity assessment;
- rejected alternatives;
- exact proposed authoritative changes, if any, to SPEC-03/04/05 or the extraction procedure;
- migration consequence for the existing 16-book corpus;
- unresolved questions.

## ACCEPTANCE CRITERIA

CANON-004 is complete only when:

1. all 16 accepted CANON-003 sources have an experimental Audit Gate record or an explicit evidence-insufficient result;
2. each of the four required audit areas has been exercised across more than one materially different source shape;
3. same-author companion books cannot accidentally count as independent convergence under the candidate design;
4. own measurement, third-party evidence, claimed measurement-without-result and mixed evidence are structurally distinguishable;
5. `no current binding` is structurally distinct from `not audited`;
6. known visual/source-format failures from CANON-003 can be represented without one generic risk bucket;
7. older-source technology contingency can be asked/recorded without forcing a new vocabulary where existing fields suffice;
8. committed mechanical tests pass for the candidate representation;
9. the proposal identifies the **minimum** authoritative method/schema revision supported by the 16-book evidence;
10. SPEC-03/04/05 remain unchanged until the final Controller decision explicitly authorizes the revision.

## RESOURCE BUDGET

- new source acquisition: none;
- paid APIs/model generation: none;
- human review: Controller review only; no new external reader panel;
- test corpus: existing 16 accepted CANON-003 sources;
- copyrighted page/image commits: none.

## STOP / ESCALATION CONDITIONS

Return to Controller before implementation if:

- the Audit Gate requires modifying SourceKnowledge semantics rather than post-extraction metadata;
- the candidate requires changing SPEC-01 / Creative IR;
- a proposed field acts as a hidden credibility score;
- testing shows the four audits cannot live coherently in one post-extraction layer;
- more than a small minority of the 16 sources require re-opening original books just to populate the gate;
- the proposal would require broad migration/reinterpretation of accepted source claims rather than additive audit metadata.

## FINAL DECISION EXPECTED

At completion, the Controller must choose one of:

- **ADOPT** — authorize the minimal v0.2 method/spec revision;
- **ADOPT WITH REDUCTION** — keep only the parts that earned their complexity;
- **REVISE AND RETEST** — candidate still fails across materially different sources;
- **REJECT** — current method is preferable and CANON-003 issues should remain local caveats.

No authoritative schema change occurs merely because CANON-004 was opened.
