---
name: media-agency-sync
description: Use when accepted (or rejected/abandoned) Media Agency jobs exist whose learning has not yet been integrated into Media Intelligence — "sync the agency jobs", "integrate the learning from job X", "open the production-learning PR", or when a job branch shows learning_status pending_sync. Also use to list which agency jobs are still awaiting sync.
---

# Media Agency Sync — job branches → one reviewed production-learning PR

**Overview.** Completed agency jobs live on `work/agency-job-*` branches with a
`LEARNING-PACKET.yaml`. This skill distils those packets into `production-learning/cases/` on a
**new integration branch cut from `origin/main`**, classifies every learning into one of five
classes, adds only explicitly justified deterministic engineering changes with tests, opens a PR,
and marks the jobs `synced`. It never merges, never touches Canon / Registry / routing files /
Controller state, and never merges a raw job branch anywhere.

## 1. Find the jobs (USD 0)

```bash
git fetch origin
git branch -r --list 'origin/work/agency-job-*'
for b in $(git branch -r --list 'origin/work/agency-job-*' | sed 's/^ *//'); do
  id=${b#origin/work/agency-job-}
  git show "$b:agency/jobs/$id/JOB.yaml" 2>/dev/null | python3 -c '
import sys,yaml; d=yaml.safe_load(sys.stdin) or {}
print("'"$id"'", d.get("production_status"), d.get("learning_status"), d.get("production_base_sha","")[:7], d.get("class"))'
done
```

Candidates: `production_status ∈ {accepted, rejected, abandoned}` AND `learning_status ==
pending_sync`. A job still `open`, or without a packet, is skipped and named in the report. The
packet is the `learning_packet` section of `JOB.yaml` or a separate `LEARNING-PACKET.yaml` beside
it — either is valid. Read them from the branch with `git show`; never check the job branch out
over the integration branch.

## 2. Cut the integration branch from main

```bash
git status --short                                   # must be empty
git checkout -b work/agency-sync-<YYYY-MM-DD> origin/main
```

## 3. Classify every learning item — exactly one class each

| Class | Meaning | Where it goes |
|---|---|---|
| **1 PROMOTE — DETERMINISTIC SYSTEM** | a QA / compositor / orchestration / ledger defect that should be code, a gate, or a regression test | `SYSTEM-DEFECTS.yaml` (`promoted_as`) + `PROMOTION-QUEUE.yaml promoted_now` + the code/test change on this branch, each justified by the defect id it closes |
| **2 CANDIDATE PATTERN** | workflow / template behaviour that worked but needs more evidence | `PROMOTION-QUEUE.yaml candidate_patterns` with a stated promotion condition; template structure → `ACCEPTED-TEMPLATE.yaml` with `evidence_scope: this_accepted_template` |
| **3 DIRECTIONAL MODEL OBSERVATION** | production evidence about a route; no Registry authority | `ROUTE-OBSERVATIONS.yaml` rows: `evidence_class: directional_production_observation`, `routing_authority: none`, exact n |
| **4 CANON GAP CANDIDATE** | a real failure exposed missing creative/production knowledge | `PROMOTION-QUEUE.yaml canon_gap_candidates` + the PR text; **report only — no pack compiled, no source added** |
| **5 JOB-SPECIFIC / NO PROMOTION** | true only of this job | stays in the job branch; listed under `not_promoted` |

Tests for the classification: a class-1 item must name a deterministic check that would have
caught it and a file where that check lives; if it cannot, it is class 2. A class-3 item with a
human verdict attached is still class 3 — human acceptance never enters the Registry. Anything
that would change a routing rule, a Registry row, a compiled pack or a Controller decision is
written as a **proposal** in the PR text, never as a file change to those trees.

## 4. Write the case(s)

One `production-learning/cases/<CASE-ID>/` per job (or per closely related batch), with the
file set: `README.md`, `OUTCOME.yaml`, `HUMAN-VERDICTS.yaml`, `REVISION-TRACE.yaml`,
`TIME-AND-COST.yaml`, `SYSTEM-DEFECTS.yaml`, `ROUTE-OBSERVATIONS.yaml`, `PROMOTION-QUEUE.yaml`,
`EVIDENCE-MAP.md` (every claim → path @ job-branch commit + sha256), and `ACCEPTED-TEMPLATE.yaml`
**only when** the job produced a reusable structure. The validator checks structure and honesty,
never the outcome — write the truth:

- `OUTCOME.yaml`: `final_outcome: accepted | rejected | abandoned`; accepted → `final_asset`
  {path, commit, 64-hex sha256}, `accepted_version`, `accepted_by`; rejected/abandoned →
  `final_outcome_reason`. `source_main_sha` (= the job's `production_base_sha`), `job_branch`,
  `job_commit`, `evidence_source: {ref, dir}` (the job branch and `agency/jobs/<id>`),
  `not_evidence_for: [Capability Registry, Canon effectiveness, …]`, `two_conclusions` with the
  case's own values (quality and efficiency stated separately — MET_BASELINE, UNDERPERFORMED,
  NOT_APPLICABLE, whatever is true), and `template_status: reusable_candidate | job_specific | none`.
  Do not manufacture a template to satisfy anything; `none` is a valid, common answer.
- `TIME-AND-COST.yaml`: one mechanical clock (`time_to_accepted_outcome_mechanical`, or
  `time_to_outcome_mechanical` for a job that did not accept) with its `source`, or
  `{value: null, reason}` when not provable; a human estimate only if one was given (labelled,
  non-numeric); `cost.total_known_provider_cost_usd` as a number or `{value: null, reason}`;
  `cost.cost_per_accepted_outcome` for accepted jobs (incomplete numerator → `missing_components`),
  `{value: null, reason}` otherwise; `counts.paid_generation_attempts` and `counts.human_review_cycles`;
  `product_conclusion.final_quality` and `.pipeline_efficiency` stated separately.

Validate against the job's **immutable commit** and directory — never a branch name, which can
move (the pilot branch gained six commits and USD 4.66 of ledger after its accepted V4.1):

```bash
JOB_COMMIT=$(git rev-parse origin/work/agency-job-<id>)        # the exact sha; also written to OUTCOME.job_commit
python3 production-learning/tools/check_case.py --case production-learning/cases/<CASE-ID> \
    --source-ref "$JOB_COMMIT" --source-dir agency/jobs/<id>
```

The branch name stays in `OUTCOME.job_branch` as provenance metadata; `final_asset.commit` and
`evidence_source.ref` carry the sha. The validator then reads the accepted asset's bytes at that
commit and requires the sha256 to match `OUTCOME.final_asset.sha256` and a hashed row in
`EVIDENCE-MAP.md`; a ref that does not resolve locally is a FAIL, not a note — fetch the job
branch first (`git fetch origin work/agency-job-<id>`). Never report a case as validated on a
structural-only (no `--source-ref`) run. (`--pilot-ref` / `--pilot-dir` remain as aliases for the
pilot-era case.) A FAIL is a defect in the case, not in the validator: fix the case. If the
validator genuinely cannot express an honest value, that is a class-1 engineering change on this
branch with a test — never a false value.
Update `production-learning/README.md`'s case list. Do **not** edit `PROJECT-MEMORY.md` or
`coordination/CONTROL-STATE.md` — note in the PR that a Governor refresh may be wanted.

## 5. Engineering changes — only class 1, only with tests

Each change: the defect id, the gate/test it adds, in the existing module
(`runtime/compositor/`, `runtime/loop/`, `runtime/execute/`), with a regression test under
`runtime/tests/`. Run the suite before the PR:

```bash
python3 -m unittest discover -s runtime/tests -p 'test_*.py' 2>&1 | tail -3
```

No refactors, no new subsystems, no "while I'm here".

## 6. Open the PR — never merge

Commit the case(s) and changes; push `work/agency-sync-<date>`; open a PR to `main` titled
`Production learning: <CASE-IDs> — <one line>` whose body lists, per job: base sha, verdict,
CpAO, TTAO, cycles/versions; the five-class table; every proposal that needs a Controller
decision (Canon gap, routing, Registry, policy); and the raw job branch names. Do not merge.

## 7. Mark the jobs synced — on their own branches

For each job integrated, on its job branch (`git worktree add` a throwaway, or `git checkout` after
the integration branch is pushed and clean) change exactly four fields of `JOB.yaml` and nothing
else: `learning_status: synced`, `sync.integration_branch`, `sync.integration_pr`, and
`sync.case_id`; commit (`sync: <CASE-ID> integrated via <PR>`) and push. `sync.merge_commit` is
filled later by whoever notices the merge. A job whose packet had only class-5 items gets
`learning_status: no_promotion` and no case. Never touch ledgers, verdicts or assets on the job branch.

## 8. Report

`SYNC REPORT` — jobs found / integrated / skipped (why), the five-class table, PR URL, the
proposals awaiting a decision. Plain English; one screen.

## Red flags

| Thought | Reality |
|---|---|
| "I'll just merge the job branch, it has everything" | Raw evidence stays archival. Only the distilled case and justified code enter the integration branch. |
| "The model clearly works — add the routing rule" | Class 3. Propose in the PR text; never edit `eval/capability-map/**`. |
| "This is obviously a Canon rule now" | Class 4 at most: report the gap. Compiling a pack is a Canon-stream decision. |
| "Update CONTROL-STATE so it's current" | Not yours. Note it for the Governor in the PR. |
| "It worked once, make it the standard workflow" | Class 2 with a promotion condition (the pilot's rule: ≥ 2 more successes). |
