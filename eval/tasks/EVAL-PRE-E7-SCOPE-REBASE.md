# EVAL — Pre-E7 Scope Rebase

**Owner:** Eval  
**Controller decision:** `coordination/decisions/CONTROLLER-PRE-E7-SCOPE-REBASE-2026-08-26.md`  
**Design:** `docs/superpowers/specs/2026-08-26-pre-e7-scope-rebase-design.md`

## Goal

Refreeze Eval so Registry evidence answers not only **what capability was measured**, but also **under what production envelope**, and so customer requirements can query evidence without choosing a provider or workflow prematurely.

## Read first

- `eval/v1/capability-contract.yaml`
- `eval/registry/SCHEMA-v1-draft.yaml`
- `eval/v1/bank/COVERAGE-REPORT.md`
- `eval/v1/MODEL-WORKFLOW-INVENTORY-2026-08-26.md`
- `canon/experiments/v1/brief-bank/briefs-source.yaml`
- Pre-E7 design above

## Deliverables

Create under `eval/pre-e7/` unless an existing V1 file is the authoritative owner:

1. `PRODUCTION-REQUIREMENT-PROFILE.md` + machine-readable schema.
2. `CONDITION-ENVELOPE-CONTRACT.yaml`.
3. `CAPABILITY-CONTRACT-v2.yaml` or a minimal versioned replacement generated from V1 after audit.
4. Registry schema revision that replaces unconstrained condition use with the frozen condition taxonomy while preserving historical compatibility.
5. E2 workflow-inventory revision adding production-operation fields.
6. Revised benchmark design and fresh cost/call forecast. Historical E7=204 / E8=520 remains recorded as superseded, not erased.
7. `PRE-E7-EVAL-CONTROLLER-BRIEF.md`.

## Production Requirement Profile requirements

Must remain provider/model/workflow agnostic.

A requirement record must distinguish:

- capability requirement;
- acceptance constraint;
- delivery condition;
- Planner decision;
- source operation/provenance;
- hard/soft/free strength;
- scope (entity/asset/shot/sequence/outcome/asset-set);
- resolved/unresolved/conflicted status.

It may not contain routing scores or provider choices.

## Condition / Envelope Contract

Freeze these condition families, splitting fields further only when necessary for unambiguous measurement:

1. delivery;
2. content load;
3. identity/reference load;
4. physical complexity;
5. cinematic complexity;
6. constraint load;
7. workflow mode;
8. sequence structure;
9. language/audio;
10. input quality;
11. decision provenance;
12. scale.

Do not create one synthetic complexity score.

Every new empirical Registry row must carry all applicable required condition fields or an explicit allowed null-state. Changing an evidence-relevant condition creates a different evidence cell/row.

## Capability v2 audit

Wait for or consume Canon's requirement ledger if available. If work proceeds in parallel, produce a provisional mapping and reconcile before completion.

For each candidate gap, prove one of:

- existing capability already covers it;
- existing capability + condition covers it;
- it is a Planner decision, acceptance constraint or operational variable;
- a genuinely new capability is required.

Candidate questions to inspect include exact spoken-script fidelity, camera/framing fidelity, cross-shot/cross-asset consistency, sequence/state continuity, technical visual integrity, pronunciation/intelligibility/voice consistency, and style-reference fidelity.

Do not target a preselected capability count.

## E2 amendment

For each officially evidenced endpoint/workflow, add where exposed:

- native duration range;
- t2v/i2v/edit/extension support;
- first/last-frame control;
- reference support type/count;
- masking/edit controls;
- character/product conditioning;
- native audio;
- aspect ratios/resolutions;
- camera controls;
- seed/reproducibility;
- version pinning;
- concurrency/rate constraints relevant to production;
- direct vs aggregator access.

Model family names from memory remain non-evidence. Current identity/access/pricing still require official sources.

## Benchmark redesign rules

Keep layered evidence:

1. evaluator qualification;
2. primitive atomic/compound baseline;
3. sparse production-envelope sweeps;
4. workflow-topology comparisons;
5. end-to-end customer outcomes.

Do not enumerate the cartesian product of conditions. Envelope sweeps should isolate one or a very small number of variables and seek failure boundaries.

The existing 100-item bank should be changed only when capability-v2 semantics or missing envelope coverage creates a concrete reason. Prefer metadata/condition enrichment and small reallocations over wholesale rebuild.

## Tests / fail-closed gates

Add validators proving:

- every capability id is unique and fully defined;
- every Registry condition key belongs to the frozen taxonomy;
- required condition values cannot silently disappear;
- Production Requirement Profile cannot contain provider/model/routing choices;
- benchmark items declare the condition values necessary to interpret their measurements;
- no synthetic fixture or unqualified instrument can promote to the Registry;
- revised cost forecast refuses to total unresolved official prices;
- superseded pre-rebase call counts are not accidentally presented as authorised.

## Stop conditions

Stop and escalate if:

- Canon's 30-brief audit reveals a requirement class that cannot be represented without changing Creative IR semantics;
- the rebase would require silently redefining historical empirical evidence;
- the proposed benchmark explodes combinatorially rather than remaining sparse/adaptive.

No paid calls. No Registry population. No merge. Commit and push isolated branch for Controller review.
