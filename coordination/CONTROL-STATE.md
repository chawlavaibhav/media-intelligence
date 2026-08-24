# Control State

**Purpose:** enough to bootstrap a fresh Controller conversation without replaying history.
**Not a diary** — see `coordination/DECISION-LOG.md` for that.

## Product thesis
An intelligence layer above image/video/audio models, optimizing Cost per Accepted Outcome by
combining explicit creative knowledge (Canon) with empirically measured current capability
(Capability Lab) to plan, route, generate, evaluate and repair. See `PROJECT-CONTRACT.md`.

## Current accepted architecture
Normalized Request → Creative IR (Canon-informed) → Production IR (does not exist yet) + Capability
Registry (does not exist yet) → Planner → Execute → Evaluate (technical + creative) → Repair →
Empirical Memory. Object-level separations are locked — see `PROJECT-CONTRACT.md` §Major
separations. **Not to be reopened without an approved integration task.**

## Workstream boundaries
Canon = durable creative expertise. Eval/Capability Lab = measurement design + empirical current-
model behaviour. Resources = independent media/data. Full definitions: each stream's `CHARTER.md`.

## Current central hypotheses (see `coordination/ASSUMPTIONS.md` for full register, 21 entries)
- **6a/6b — untested, load-bearing.** Does explicit Canon improve creative planning (6a) and
  creative evaluation (6b), versus the same model with generic structure only?
- **15 — untested, blocked on Eval.** Do Canon-derived requirements improve routing when combined
  with an empirical Capability Registry?
- **4 — partially supported.** Book knowledge connects to empirical failure through shared
  mechanism, violated requirement, or commercial consequence — not one uniform channel.
- **1b — provisional design, not proven.** Separating Source Knowledge from Operational Bindings
  is the right response to 1a (an empirical finding, narrowly scoped to the six-source sample).

## Current versions
- Creative IR: **SPEC-01 v0.1**, locked for first experiment.
- Source Knowledge schema: **SPEC-03 v0** (supersedes SPEC-02, retained as historical evidence).
- Operational Bindings: **SPEC-04 v0**.
- Knowledge Ontology: **SPEC-05 v0**.
- Canon curriculum: **V0 proposed, 11 sources, not yet approved for ingestion** —
  `canon/experiments/CANON-CURRICULUM-V0.md`.
- Capability Registry schema: proposed, not built — `eval/battery/CAPABILITY-LAB-V0-PLAN.md`.
- Eval Battery: not designed.
- Corpus: not sourced — `resources/corpus/CORPUS-SOURCING-PLAN.md` is a research plan only.

## Canon status
Six sources partially processed (Molly Bang, Williams, Lupton, Grammar of the Shot, Ogilvy, Light:
Science & Magic) — **representation-architecture probes, not a representative Canon sample; see
`canon/findings/DIRECTION-RESET-01-CANON-ROLE.md`.** Re-audited under SPEC-03/04/05 in
`canon/knowledge/migration/`. Coverage Map (52 domains) and V0 Curriculum (11 sources) proposed,
awaiting Controller approval before any further ingestion. No book has been processed under the
current (SPEC-03/04/05) schema yet — the six probes predate it and were re-audited, not rerun.

## Eval status
One completed piece of work: Devanagari VLM-checker calibration (`eval/findings/
FINDINGS-01-can-we-check.md`) — qwen3-vl scored 14/14, claude-sonnet-4.5 produced 6 false passes on
the same material. Established that an uncalibrated checker is worse than none. No battery
designed, no Capability Registry exists, no model benchmarking beyond that one calibration test.

## Resources status
No dataset downloaded. Two small existing pools: 64 human-scored generations
(`resources/corpus/finding-01-samples/` is the 14-sample checker set; the larger 64-image scored
set remains in the `media-factory` repo's `spike/` directory, not yet copied here). Candidate
external datasets researched, not accessed — `resources/corpus/CORPUS-SOURCING-PLAN.md`, all
licences marked unverified.

## Cross-stream dependencies
Eval's Capability Registry blocks hypothesis 15 (routing). Canon's Curriculum approval blocks
Experiment A/B. Resources' corpus work blocks Experiment B's need for independent evaluation media
and blocks a proper Capability Lab battery. All three currently blocked on Controller review of
this setup and of `canon/experiments/CANON-COVERAGE-MAP-V0.md` +
`canon/experiments/CANON-CURRICULUM-V0.md`.

## Current approved milestones
None yet approved under this operating model. Prior work (six probes, re-audit, direction reset)
was approved under the previous single-thread mode and stands as historical evidence.

## Blockers requiring human input
1. Approve or amend the Canon V0 Curriculum (11 sources) before any ingestion resumes.
2. Approve or amend the Coverage Map's domain priorities.
3. Decide whether to build a proprietary Devanagari text-rendering benchmark (no public one found
   — `resources/corpus/CORPUS-SOURCING-PLAN.md` §D).
4. Assign/approve first tasks per stream (see Phase 7 report for suggestions — not started).

## Next integration checkpoint
After Canon runs Experiment A (planning) and reports results, Controller reviews before Experiment
B (evaluation) or any Capability Lab spend is approved.
