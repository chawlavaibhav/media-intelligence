# Workstream Status

**Current snapshot:** 26 Aug 2026 — final pre-execution tranche returned; GOV-004 review active.
**Refreshed by:** Repository Governor, task GOV-004, against `main` at `74d6b0da0239013269f73804164a92f80c7f1d55`.

**Read `PROJECT-MEMORY.md` and `coordination/CONTROL-STATE.md` first.** Detailed historical snapshots remain in Git history; this file is current-state only.

## Global posture

**No domain programme is running.** All four pre-execution programmes have returned, the Controller has issued a joint integration disposition, and one bounded Eval correction (EVAL-011) has completed. **No paid model/evaluator work is authorised.**

| Stream | Current state | Active approved work | Next gate |
|---|---|---|---|
| Canon | 19 live accepted sources; original 30-brief bank byte-identical; CANON-009 merged. **CANON-010 returned, unmerged.** | none | Controller merge, then the request contract is frozen. |
| Eval | V1 36-capability and 100-item baselines byte-identical; **0 empirical Registry rows; 0 qualified instruments**; EVAL-007 merged. **EVAL-010 and EVAL-011 returned, unmerged.** EVAL-009 is superseded worker output. EVAL-008 remains candidate-universe research, not a paid roster. | none | Controller merge, then Capability v2 / benchmark v2 / staged execution are frozen and a tranche is priced. |
| Resources | RES-003 merged; v2.1 historical persistence preserved. **RES-004 returned, unmerged.** | none | Controller merge, then topology v3, CpAO v3 and pack requirements are frozen. |
| Governor | GOV-003 merged with **PASS WITH NON-BLOCKING NOTES**. | **GOV-004** final pre-execution coherence review | Verdict returns to the Controller; then merge and priced-tranche planning. |

## Branches returned and awaiting Controller merge

| Package | Branch | Commit |
|---|---|---|
| CANON-010 request contract and coverage freeze | `work/canon-010-request-freeze` | `3cf2979` |
| EVAL-011 corrected Eval freeze proposal (**the live one**) | `work/eval-011-pre-execution-integration` | `e300999` |
| RES-004 production evidence and persistence readiness | `work/res-004-production-readiness` | `2dc4796` |
| EVAL-010 model route / version / price verification | `work/eval-010-route-verification` | `8a8fc09` |

`work/eval-009-measurement-freeze` @ `718ba01` is **historical worker output**. EVAL-011 carries the corrected live files and is what should be merged.

**Merge note:** the EVAL-011 branch is three commits behind `main` and conflicts with it on `coordination/CONTROL-STATE.md`. `main`'s version is the newer Controller-authored one and is the correct side to keep.

## Active task and branch

- `governance/tasks/GOV-004.md` → `work/gov-004-final-pre-execution-review`

Authoritative program:
- `coordination/plans/2026-08-26-FINAL-PRE-EXECUTION-FREEZE-PROGRAM.md`

Authoritative decisions:
- `coordination/decisions/CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md` — **the current joint disposition**
- `coordination/decisions/CONTROLLER-FINAL-PRE-EXECUTION-FREEZE-2026-08-26.md`
- `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md`

## Durable facts that must remain distinct

- Historical CANON-003 baseline: **16** accepted books. Do not rewrite it to today's live count.
- Live Canon: **19** accepted sources / 19 active Audit Gate records.
- Original EVAL-005 build: 106 items; authoritative validated view: **96** items. Preserve both meanings.
- V1 capability contract: **36** dimensions; V1 bank: **100** items. These remain historical/baseline artifacts and stay byte-identical; the proposed **v2 target is 44 = 43 active + 1 dormant** and does not overwrite them.
- Condition architecture: **13 families**, a naive two-level product of **8,192** cells. The earlier "12 families / 4,096" figures were an error corrected by EVAL-011 — do not restore them.
- Staged execution: **Q = 0** model generations, **A = 90**, **B ≤ 404**, **A+B design ceiling 494**; **Stage C = 32 outcome attempts**, counted separately. None of these is an approved budget.
- Capability Registry: **0 current empirical model/workflow rows**.
- One provider/API/transform call = one trial.
- EVAL-004 remains stopped.
- `EVAL-006` remains **PAUSED — DO NOT EXECUTE**.

## Model research posture

EVAL-008 proved selection-before-sourcing ordering and is useful as a candidate universe, but does not authorise any model run.

EVAL-010 has since verified supply as **partial evidence**: 2 of 26 candidate rows are execution-ready (identity + route + billing unit + price all verified), 19 more have verified identity and route but **no verified price**. That is an evidence gap, not proof that models are unavailable. Price completeness across the four staged stages is **0 of 4**, and `Frontier Clouds` service identity remains unresolved, so cash outlay after credits cannot be computed.

Current Controller rule:
- the scientific roster is **12 core + 2 reserve question slots**, chosen by differentiated product-relevant information value;
- EVAL-010 verifies exact versions/routes/prices separately;
- route preference for equivalent versions is `Frontier Clouds credits -> fal -> direct/other`;
- access/credits do not decide scientific admission;
- non-primary version/price/availability claims remain provisional;
- the worker-side claim that “Frontier Clouds” means GCP+AWS+Azure is not a Controller decision on record and must not be assumed without confirmation/verification.

## Still blocked / not authorised

- no model generation calls;
- no evaluator/checker API calls;
- no empirical Registry population;
- no controlled-pack acquisition;
- no account funding / terms acceptance;
- no Production IR/Planner implementation;
- historical E7/E8 execution remains superseded/blocked;
- no paid benchmark budget exists.

## Final pre-paid-run gate

The four programmes have returned and been jointly dispositioned. GOV-004 is the bounded Governor review. After it returns, the Controller merges the accepted branches and then produces a **separately priced** first empirical tranche for explicit approval.

**Figures that are not budgets and must not be treated as approved:** 494 generations, 5,515 evaluator calls, 188 human review units, 173 pack-acquisition person-hours, and the provisional controlled-pack entity totals.

There is no further broad research round scheduled.
