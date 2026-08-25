# Controller State

**Updated:** 26 Aug 2026 by Controller.

**Read `PROJECT-MEMORY.md` first.** Where its older freeze/task wording conflicts with this newer Controller state, this file and the underlying task/decision artifacts govern until the Governor refreshes memory.

## Global posture — planning only

**No domain execution task is currently authorised.**

`EVAL-006` is **PAUSED — DO NOT EXECUTE** as of 26 Aug 2026. Its previous autonomous checker/model/Registry bootstrap, including all API-spend authority, is withdrawn before execution. The current task file is the authoritative pause marker: `eval/tasks/EVAL-006.md`.

The Controller has required a complete end-to-end Eval master plan before any new Eval task is assigned. The planning pass may read repository evidence and public benchmark/model documentation, but it must not run checker/model APIs, generate media, create empirical Registry entries, or spend money.

Canon expansion, Resources expansion/acquisition, Production IR, Production Planner/routing implementation, and Canon-consumption/RAG/training remain on hold unless separately authorised.

## Architecture state

- Product goal remains an API-native media production intelligence layer optimising **Cost per Accepted Outcome**.
- Creative IR v0.1 is locked for experiment use; Production IR does not exist yet.
- Capability Battery V0 is approved measurement-design evidence, not an exhaustive production capability map and not model capability data.
- Capability Registry schema work exists, but **there are still zero empirical model/workflow entries**.
- Production Planner/routing does not exist.

## Canon

- Historical CANON-003/004 baseline: **16** sources, frozen.
- Live accepted Canon: **19** sources.
- CANON-008 is closed as a legitimate blocked-source adjudication; the Devanagari-structure gap remains explicit.
- No Canon task is open.

## Eval

Completed evidence remains intact:

- EVAL-001/002/003 closed and merged.
- EVAL-004 stopped; Reader A is exploratory only.
- EVAL-005 human validation complete; authoritative checker-qualification battery is **96 items: 48 match / 48 mismatch, 48 accepted base words, 33 hard opportunities, 20 failure classes across 5 groups**.
- Existing harness/plumbing and negative controls remain reusable.
- No checker is qualified, no generator has been benchmarked, and no empirical Capability Registry entry exists.

**Current Controller direction:** zoom out and redesign Eval end-to-end against the first commercial product scope. The plan must quantify the complete capability map, distinguish isolated probes from shared multi-measurement production scenarios, maximise valid measurements per generation, define resource/instrument/model-access requirements, define one-time generation reuse for later creative scoring, specify budgets and stop gates, and break execution into bounded measurable tasks. **Nothing is assigned until the Controller approves that plan.**

## Resources

- RES-001/002 are closed and merged.
- Current corpus: **34,786 items / 5.70 GB across 8 acquired sources; 4 blocked**.
- IndicSTR12 and IIIT-ILST are one source lineage for holdout purposes; BSTD is the genuine cross-lineage Devanagari reserve.
- No Resources task is open. Resources should receive only concrete requirements from the approved Eval master plan; no speculative acquisition is authorised.

## Current gate

1. Finish and review the complete Eval master plan.
2. Controller approves/amends/rejects the plan.
3. Only after approval: create the new bounded Eval task sequence and any exact Resources dependency tasks.
4. Before any paid run: verify actual configured API access, exact current model/version/endpoint and live pricing, produce a full cost forecast, and obtain the budget approval required by the approved plan.
