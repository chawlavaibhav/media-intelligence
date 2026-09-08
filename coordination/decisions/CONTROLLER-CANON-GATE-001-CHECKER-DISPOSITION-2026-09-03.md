# Controller — CANON-GATE-001 Checker Disposition — 2026-09-03

**Status:** APPROVED CONTROLLER RULINGS; a bounded fix pass is authorised before merge.
**Role:** Writer Controller.
**Applies to:** `work/canon-gate-001` at `47efc09` (maker's seven commits) and the checker's report
on it (verdict: PASS WITH NON-BLOCKING NOTES, fourteen findings F-01..F-14).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md`;
`CONTROLLER-CANON-GATE-001-PLAN-RULINGS-2026-09-03.md`.

The checker put two matters to the Controller. The Controller answered each by selecting one of the
stated options; the selections are recorded here as chosen, nothing added.

## Ruling 4 — integrity rows block (checker F-01)

Controller selected: **"Block."**

Ruling 2's sentence "the blocking set — the only rows that can turn the verdict to FAIL — is …"
answered plan §G Q2, which concerned **declaration-presence partials only**. It did not, and was
not intended to, demote the plan's `INFRA` rows, which were blocking under the plan's v0 rule and
are the evidence-chain checks the Governor contract names ("break the evidence chain"). Ruling 2
is amended accordingly:

- **Blocking set:** `LIMIT-TEXT`; every `DISPATCH-*`; every `INFRA-*`
  (`INFRA-CONTAINER`, `INFRA-VIDEO-TRACK`, `INFRA-RECORD-SHA`); `CA-D2-check` clause 2; any
  `ERROR`.
- **Non-blocking (report only):** the declaration-presence partials named in Ruling 2, unchanged.
- An artifact whose sha256 does not match its `record.json`, or that carries no video track under
  a video dispatch, exits 1.

## Ruling 5 — scope of the pre-merge fix pass (checker F-01..F-14)

Controller selected: **"Fix everything, then merge."**

One bounded fix pass by the maker, re-verified by the checker, before the Controller merges. All
fourteen findings are in scope. Binding conditions on the pass:

1. **Vocabulary changes are Controller-visible or they do not happen.** Every change to a
   constant in `canon/gate/vocab.py` is recorded in that module's `CHANGELOG` with the finding id
   and the fixture phrase that motivated it. Every adversarial phrasing the checker reported under
   F-02 (false FAIL), F-03 (false PASS), F-04, F-05 and F-07 becomes a committed test fixture
   asserting the intended outcome — so the tuning is pinned, not guessed.
2. **The committed EVAL-038 fixtures remain the anchor.** After tuning, the four real packages
   and six real artifacts must produce the verdicts in the plan §F table as amended by Rulings 2
   and 4. If narrowing a bare term (F-05: `balance`, `key`, `fill`, `side`, `front`, `window`,
   `behind`, bare `°`) flips Sonnet B01's CA-D5 back to FAIL (non-blocking), that is the plan's
   original expectation restored: remove the `expectedFailure` guard and assert the plan's value.
3. **Boundaries unchanged.** All seven boundaries of the parent authorisation and the
   render-by-id requirement stand. No paid call; the Cloud Vision adapter stays un-invoked. The
   maker does not touch the plan file or any `coordination/` file; the Controller amends those.
4. **Where a finding is a stated limitation of a header-only probe (F-09) or of frame-based
   video scanning (F-08), the fix is to make the limitation visible in the report** (frames
   scanned vs duration; an mdat declared to-EOF on a short file), not to pretend to a capability
   stdlib does not have.
5. **F-06 (paraphrased clause in quotation marks):** quote the verbatim pack fragments; never
   render non-verbatim text inside quotation marks attributed to a pack.
6. **The in-test fixture copy of Haiku B01 shot 6 (checker §6) is replaced by the committed file
   read in place**, per plan §F.
7. **The suite must contain a test that exercises each INFRA row's effect on the verdict**, not
   only its status — the gap through which F-01 passed unremarked.

## Sequence to merge

maker fix pass → checker re-verification (same adversarial method, plus a diff review of every
vocabulary change against its recorded fixture) → Controller merge decision. No agent approves its
own work; the Controller does not implement.

## Not authorised by this decision

Any spend, provider call or media generation; any change under `eval/`, `canon/compilation/`,
`canon/knowledge/`, `canon/audit/`, `canon/packs/`; any conclusion about whether Canon works;
merge to `main` — a separate Controller act after the checker reports.
