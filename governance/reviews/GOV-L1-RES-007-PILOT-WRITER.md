# Governor Level-1 Review — RES-007 (pilot outcome writer)

**Review mode:** Level 1 — task/PR integrity review (`governance/GOVERNOR-CONTRACT.md` §3a).
**Authorisation:** `coordination/decisions/CONTROLLER-RES-007-FINAL-ACCEPTANCE-2026-08-28.md`
("RES-007 now requires a bounded Level-1 Repository Governor review before merge"), reflected in
`coordination/CONTROL-STATE.md` Next gate item 2. This is **not** GOV-007 — GOV-007 (a broader
reconciliation task) remains explicitly unauthorised; the file is named without a GOV task number
for that reason.
**Audited `main`:** `ec3ccf6a304d4abce221824f3c0e73b8aa3e548e` — "controller: update pre-pilot
integration state", 28 Aug 2026.
**Branch reviewed:** `work/res-007-pilot-writer` at
`b760ab0f4e864b88f88a7f8a26ad487de62845ac` — the exact Controller-accepted head, verified against
the SHA named in the final acceptance decision.
**Date:** 28 Aug 2026 · **Spend:** USD 0. No model, provider or paid API call; no generation.

**What this verdict is.** A Governor verdict speaks only to repository coherence: scope, authority
honesty, current-state consistency, historical integrity, and mechanically checkable paths, counts
and controls. It is **not** a judgement that the Resources methodology is strategically optimal,
that the v3 topology is well designed, or that the Controller's acceptance was wise. Those are
Controller/domain questions (`governance/GOVERNOR-CONTRACT.md` §0, §3). Per the Controller's
review instructions, this review does not reopen the accepted `eval_item_id` override, the G12
scope, the writer design, or production-attempt semantics.

---

# Verdict: PASS WITH NON-BLOCKING NOTES

No blocking repository-coherence defect found in scope. All four worker-reported control figures
were **independently rerun in this review's environment and reproduced exactly**. One low-severity
note recorded below; it would not mislead a fresh session about live project state or corrupt
evidence. **RES-007 requires no correction before Controller merge.**

---

## A. Branch purity and ownership — clean

Mechanically verified from the complete diff `d164f49f..b760ab0f` (the merge base with `main` is
`d164f49f6959b546c431cb47c3d8f5dec752dedd`, exactly the SHA the final acceptance names as the
rebase base):

- **Three commits, all RES-007:** the original writer pass, the Review-1 G12 provenance
  correction, and the Review-2 value-invariant correction. No unrelated worker commits.
- **61 files, all under `resources/`** — the writer, its tests, the synthetic journeys, the G12
  fixtures, the two v3 contract documents, the v3 validator and the control runner, plus
  `resources/tasks/RES-007-CONTROLLER-BRIEF.md`. The Resources charter grants "everything under
  `resources/`", and the two Controller correction decisions explicitly authorise the contract and
  validator edits.
- **Nothing outside `resources/` is touched.** Verified by path-scoped diff: no Eval or Canon
  file, no Controller decision, no coordination, governance or shared file.
- **No generated local/runtime state committed.** The committed `.bin` files and journey YAMLs are
  the task's declared deliverable ("synthetic example output produced by tests"), regenerated
  deterministically by test t18 — not caches or scratch state. No `__pycache__`, `.pyc` or
  workspace files appear in the diff.
- **No paid evidence fabricated.** The synthetic journey's cost ledger holds 9 entries, every one
  marked `synthetic: true`, all in the test currency XTS, provider `dummy-vendor`. Verified by
  reading the committed archive, not the brief.

## B. Controller-authority consistency — clean

The branch implements `CONTROLLER-RES-007-FINAL-ACCEPTANCE-2026-08-28.md` without contradicting
it. Each accepted mechanic was verified in the durable artifacts (validator code, contract text,
fixtures, committed journeys), not just in the brief:

| Accepted mechanic | Where verified |
|---|---|
| Production attempt → no fabricated `eval_item_id`; forbidden if supplied | validator G12 (refuses non-null on `production`); writer refuses at record time; positive journey omits the key entirely; `nc-G12i` |
| Benchmark/eval attempt → `eval_item_id` required | validator + writer; `nc-G12h`; positive fixture `v3-valid-benchmark-attempt` |
| Lane vocabulary mechanically enforced | validator/writer `VALID_LANE` matches the frozen v2.1 vocabulary verbatim (`resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` line 232 — even the `nc-G12k` bad value `video` is one of v2.1's own `not_allowed_examples`) |
| Exact storage class | must equal `C_irreproducible_empirical`, matching v2.1; `nc-G12l` |
| `repeat_index` integer ≥ 0, boolean rejected | explicit `isinstance(…, bool)` exclusion in both; `nc-G12m/n/o` |
| Genuine SHA-256 hashes | 64-lowercase-hex regex in both; `nc-G12p/q/r`; committed journeys carry real hashlib digests (see F) |
| Repeat/retry references resolve | validator resolves in-archive; writer resolves at record time; `nc-G12s/t` |
| UTC timestamp semantics | ISO-8601 UTC check in both; null `completed_at` preserved as "never completed" (the journey's timeout attempt exercises it); `nc-G12u/v` |
| Failed/refused/timed-out attempts retained | G10 + writer refusal of failures without `error_detail`; the accepted journey retains a refusal and a timeout as individual rows |
| One call = one attempt = one trial | G1 + writer trial-id uniqueness |
| Local/human work creates no fake provider attempt | G2 both sides; tests t03/t08/t10 |
| HED-1 remains unresolved | writer records `human_required` and `human_optional` and decides nothing; CpAO engine untouched; brief states HED-1 open |

None of these decisions was reopened by this review.

## C. Validator/writer agreement — mechanically agree within the corrected G12 scope

Both `OutcomeWriter.record_attempt` and the G12 section of `validate_topology_v3.py` were read
line-by-line and compared across every item the Controller listed: attempt kind, lane, storage
class, repeat index, prompt/config/reference hashes, requested/completed timestamps, retry reason,
repeat/retry references, and `eval_item_id`. **No case was found where the writer emits something
the validator rejects, or the validator accepts something the writer contract explicitly forbids,
within the corrected G12 scope.** Test t24 additionally seeds each of the 13 Review-2 violations
into a written archive and proves the frozen validator rejects each — the durable archive is
protected even if the writer is bypassed.

Two deliberate, safe asymmetries, recorded so nobody mistakes them for drift:

- The validator accepts an unquoted YAML timestamp already parsed to a UTC-offset datetime; the
  writer only emits quoted strings. The writer is strictly narrower — everything it emits, the
  validator accepts.
- The writer refuses unknown extra attempt fields (only v2.1's `seed`/`settings`/`latency_ms` pass
  through); the validator does not police unknown extras. That is outside the Review-2 scope and
  the brief says so explicitly rather than claiming it.

## D. Control integrity — all four reported figures independently rerun and reproduced

Rerun in this review's environment (Python 3.14, PyYAML present) from the branch head checkout,
not quoted from the brief:

| Control | Worker-reported | Governor rerun |
|---|---|---|
| Writer tests (`test_pilot_journey.py`) | 24/24 | **24/24 — PASS** |
| Lineage controls (`run_lineage_controls.sh`) | 41/41 | **41/41 — PASS** (2 positives + 39 negatives, matching the fixture inventory: 17 G1–G11, 9 G12 presence, 13 G12 value) |
| CpAO controls (`run_cpao_controls_v3.sh`) | 13/13 | **13/13 — PASS** |
| Synthetic fully-loaded CpAO (`recompute_cpao_v3.py`) | 42.00 XTS | **42.00 XTS — PASS** (API/tool view 26.50 XTS; shared ledger entry counted once; `human_optional` excluded from both views) |

Nothing is reported here as `NOT RUN`; the environment permitted full execution.

## E. Negative-control quality — controls fail for their own invariant

The runner itself now enforces this (each G12 control declares `# EXPECT-SUBSTRING:` and the
runner matches the failure message against it). Independently spot-checked by running the
validator directly on five controls covering the Controller's minimum list — unknown lane
(`nc-G12k`), boolean repeat index (`nc-G12o`), malformed prompt hash (`nc-G12p`, the 64-p
pseudo-hash), dangling retry reference (`nc-G12t`), malformed timestamp (`nc-G12u`). **Each
produced exactly one gate violation, on exactly the declared invariant** — no control passes by
accidentally breaking an unrelated field.

## F. Historical integrity — intact

- **v2.1 historical artifacts unrewritten:** path-scoped diff over `resources/v1/` is empty. G12
  applies only to `schema_era: v3`; the validator routes `v2.1`/`pre_v3` archives away from G12
  and G9 still rejects backfilled v3 context.
- **The first-pass defect is honestly documented:** the brief states the first pass "shipped a
  real contract/validator mismatch and failed to fire the task's stop condition."
- **The second-pass overclaim is honestly documented:** the brief states the second pass
  "overclaimed" and names the exact false claim (validator PASS ≠ full written-contract
  conformance) with concrete examples of what still slipped through.
- **The final pass does not pretend the defects never happened:** the lineage contract preserves
  the original "18/18 as declared" record and layers the correction history on top with authority
  citations; the final conformance claim is explicitly narrowed to "mechanically explicit"
  invariants with a stated exclusion list.
- Committed evidence is genuine: every artifact `output_hash`/`output_bytes` in the accepted
  synthetic journey was recomputed from the committed `.bin` bytes in this review — all five
  match.

## G. CpAO boundary — untouched

`CPAO-CONTRACT-v3.md`, `recompute_cpao_v3.py` and the CpAO fixtures do not appear in the diff at
all (path-scoped diff empty). Numerator, denominator and human-cost treatment are therefore
unchanged by construction; the 13 CpAO controls still pass; the writer's docstrings and the brief
both state HED-1 is a Controller decision the writer does not make. **HED-1 remains unresolved.**

## H. Current-main coherence — merges cleanly; nothing stale

- `git merge --no-commit` of `b760ab0f` into `main` at `ec3ccf6a` completes with **no conflicts**
  (verified, then aborted — the Governor does not merge).
- `main` has advanced 7 commits past the branch's base (`d164f49f`): the CANON-012/013 Governor
  review and integration, the RES-007 acceptance decision itself, the EVAL-035 correction
  requirement, and the CONTROL-STATE update. None touches a path the branch touches and none
  contradicts any branch statement. The brief's cross-stream note about EVAL-035 needing to
  surface lane/hash/timestamp formats is consistent with the still-active EVAL-035 correction.
- **No rebase is needed.** The branch's base is the exact SHA the acceptance decision reviewed;
  demanding a rebase onto `ec3ccf6a` would be cosmetic, which the Governor contract forbids
  requiring.

---

## Non-blocking notes (routed, not edited — Resources-owned files)

**N1 (Low · Resources · routed).** The gate table in
`resources/pre-execution-freeze/LINEAGE-CONTRACT-v3.md` still lists G12's fixture column as
`nc-G12a…i` — the Review-1 set. After Review-2 there are 22 G12 fixtures (`nc-G12a…v`). The
correction header a few lines above the table already states the current 41-control inventory, so
a fresh reader is not misled about live state, and the control runner is the mechanical authority
in any case. Worth folding into any future Resources edit of that file; no correction required
before merge.

**Observation (not a defect).** The brief's STATUS line says "returning for Controller review
(then Level-1 Governor review if accepted)". That was true when written; the acceptance decision
now on `main` supersedes it as the current status, exactly per the "newer durable Controller
decisions govern over stale prose" rule. Expected sequencing, nothing to fix.

---

## Completion summary

| Item | Value |
|---|---|
| Review mode | Level 1 |
| `main` SHA reviewed | `ec3ccf6a304d4abce221824f3c0e73b8aa3e548e` |
| RES-007 branch SHA | `b760ab0f4e864b88f88a7f8a26ad487de62845ac` (matches the acceptance decision) |
| Verdict | **PASS WITH NON-BLOCKING NOTES** |
| Blocking findings | None |
| Non-blocking notes | N1 (stale G12 fixture list in the lineage-contract gate table; Low) |
| Tests independently rerun | Writer 24/24 · lineage 41/41 · CpAO 13/13 · fully-loaded CpAO 42.00 XTS — all reproduced |
| Writer/validator mechanical agreement | Yes, within the corrected G12 scope |
| v2.1 historical integrity | Intact — `resources/v1/` untouched; defect history honestly preserved |
| HED-1 | Untouched and unresolved |
| Correction required before Controller merge | **No** |

The Controller may merge `work/res-007-pilot-writer` at `b760ab0f` when ready. The Governor does
not merge.
