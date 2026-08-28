# Governor Level-1 Review — CANON-012 and CANON-013 (pre-pilot tranche)

**Review mode:** Level 1 — task/PR integrity review (`governance/GOVERNOR-CONTRACT.md` §3a). Two
independent reviews in one file; each carries its own verdict.
**Authorisation:** `coordination/decisions/CONTROLLER-CANON-012-CORRECTION-ACCEPTANCE-2026-08-28.md`
(CANON-012 "eligible for the required bounded Level-1 Repository Governor review") and
`coordination/decisions/CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md` (CANON-013 "may proceed
to bounded Level-1 Governor review"), reflected in `coordination/CONTROL-STATE.md` Next gate items
1–2. This is **not** GOV-007 — GOV-007 (a broader reconciliation task) remains explicitly
unauthorised; the file is named without a GOV task number for that reason.
**Audited `main`:** `d164f49f6959b546c431cb47c3d8f5dec752dedd` — "controller: reflect final RES-007
correction", 28 Aug 2026.
**Branches reviewed:**
- `work/canon-012-aight-ir-seed` at `1ad0b7dd68954b2b6abaaa77db0b523f09321948`
- `work/canon-013-marketplace-triage` at `03f321cbe7b8fca78342a21f6642a999c01ef6b3`

**Date:** 28 Aug 2026 · **Spend:** USD 0. No model, provider or paid API call; no generation.

**What these verdicts are.** A Governor verdict speaks only to repository coherence: scope,
authority honesty, current-state consistency, historical integrity, and mechanically checkable
paths/counts. It is **not** a judgement that the Creative IR is creatively good, that CANON-012's
schema reading is methodologically ideal, that CANON-013's split is strategically best, or that the
Controller's acceptances were wise. Those are Controller/domain questions
(`governance/GOVERNOR-CONTRACT.md` §0, §3).

---

## REVIEW A — CANON-012 (`work/canon-012-aight-ir-seed`)

# Verdict: PASS WITH NON-BLOCKING NOTES

No repository-coherence defect found in scope. Two low-severity notes recorded below; neither would
mislead a fresh session about live project state or corrupt evidence.

### A.1 Scope / ownership — clean

Mechanically verified from the diff against the branch's merge base with `main` (`2995b442`):

- The branch adds exactly **three new files**, all under `canon/experiments/pilot-001/` — precisely
  the three deliverable paths the task file names. **No existing file is modified anywhere.**
- Therefore, mechanically: no frozen schema or grammar was touched
  (`canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml` and
  `canon/knowledge/SPEC-01-creative-ir.md` are byte-identical to `main`); no cross-stream file
  changed; no coordination/eval/resources file changed.
- No provider, model or Production-IR decision appears in the deliverables. The Creative IR is
  model-independent; where instruments are mentioned (AC-01/02 verification notes) the text states
  existing project facts about evaluator status and explicitly leaves instrument selection to
  Production IR.

### A.2 Authority — the branch agrees with the Controller correction decisions

Checked claim-by-claim against `CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md` (the four
required corrections) and `CONTROLLER-CANON-012-CORRECTION-ACCEPTANCE-2026-08-28.md` (which accepts
the correction commit `1ad0b7d` — the exact commit reviewed here):

1. **Conformance stated honestly.** The IR file header, `meta.spec_conformance`, and the Controller
   Brief all state: semantically complete/usable, **not strictly conformant to SPEC-01 as written**,
   because `confidence: not_assigned` is used where SPEC-01 requires numeric 0.0–1.0 (the F5
   conflict with the no-invented-confidence rule). Verified against SPEC-01 itself, which does
   require `confidence: 0.0–1.0` on derived/system_decided fields.
2. **F4 narrowed.** The overclaim ("exact price copy has no first-class IR slot") is explicitly
   withdrawn in the brief and the IR's copy-section comment. The narrowed finding matches the
   Controller's wording. Verified against SPEC-01: `copy.headline/body/cta` with `exactness` exists;
   `mandatories[]` explicitly permits price.
3. **No blinding claim survives.** Every remaining occurrence of "blind" in the three files (7
   occurrences) is a negation or a description of the removed claim; the deliverables state
   blinding is NOT required for PILOT-001 and belongs to the later architecture experiment, with
   freeze-before-generation and the explicit human acceptance record kept.
4. **Instance workarounds stay local.** `fixture: true`, `required_external_assets` and
   `confidence: not_assigned` are each explicitly marked, in both YAML files and the brief, as
   instance-level workarounds — not schema extensions, not frozen vocabulary, not precedent.

### A.3 Current-state consistency — merging makes nothing false

- The branch touches no current-state document, so it can stale nothing by edit; checked instead
  whether its *content* contradicts current state. It does not: `PROJECT-MEMORY.md`,
  `CONTROL-STATE.md` (CANON-012 row, PILOT-001 gate list) and the Canon-state navigation all remain
  true with these files merged.
- **The missing Aight wordmark remains visible as a PILOT-001 input gate everywhere:** in
  `CONTROL-STATE.md` ("a usable Aight asset package"), in the acceptance decision, and prominently
  in all three branch files (AC-03 `blocked`, `required_external_assets` status MISSING,
  "DECISIONS NEEDED" item 1). Nothing in the branch claims the asset exists.
- Mechanically confirmed **no Aight brand asset is committed** on `main` (the only path matching
  "aight" is the CANON-012 task file itself) — so the branch's "does not exist in this repository"
  claims are true, and there is no false claim of a committed wordmark.

### A.4 Historical integrity — clean

- Additions only; no historical file rewritten.
- The first-pass correction history is represented honestly: the brief's "CORRECTION PASS" section
  names what was wrong (overclaimed F4, false blinding claim, unqualified conformance claim), says
  the first-pass wording should not be taken at face value where it conflicts, and preserves the
  two-commit history on the branch (`0b8cd29` first pass, `1ad0b7d` correction) rather than
  squashing it away.
- No schema is retrospectively presented as having supported the workarounds: the grammar and
  SPEC-01 are unmodified, and the instance files repeatedly state the vocabularies **cannot**
  express fixture provenance / missing-asset registration — the opposite of retroactive support.

### A.5 Paths / references — resolve

All referenced files verified present on `main`: the grammar, SPEC-01, the task file, both
Controller decisions. Quoted anchors spot-checked: the grammar's `meta.status:
PROPOSED_READY_FOR_FREEZE` token exists as quoted (and the stale-header caveat is correctly cited
to CONTROL-STATE); SPEC-01 is v0.1 "Architecture locked" as cited. The two commercial strings are
byte-exact in every occurrence, including U+20B9 ("Image ₹9" ×8, "Video ₹99" ×8 across the two
YAML files' requirement-bearing positions).

### A.6 Branch state — behind `main`, no rebase required

The branch is based on `2995b442`, 10 commits behind audited `main`. The entire `main` delta since
the branch point is Controller decision records plus `CONTROL-STATE.md` updates — including the very
decisions this branch's correction pass implements. `git merge-tree` confirms a **clean merge** onto
`d164f49`; no branch content is falsified by the delta. Requiring a rebase would be cosmetic; none
is required.

### A.7 Non-blocking notes (routed, severity Low)

- **A-N1 — "PILOT gate condition 1" numbering.** The NR (`required_external_assets`), the IR
  (`brand.logo.asset` note) and the brief refer to the missing wordmark as "PILOT gate condition 1
  in CONTROL-STATE.md". `CONTROL-STATE.md` lists the PILOT-001 prerequisites in prose without
  numbered conditions (the asset package is one item among five). The gate itself is real and
  correctly described; only the "condition 1" citation form is imprecise. Self-correcting on
  contact with CONTROL-STATE. Owner: Canon (files), no action required before merge.
- **A-N2 — stale-numbering environment.** The same citation style interacts with the Next-gate
  numbering defect on `main` recorded in C-N2 below (a `main`-side defect, not this branch's).

**CANON-012 blocking findings: none.**

---

## REVIEW B — CANON-013 (`work/canon-013-marketplace-triage`)

# Verdict: PASS WITH NON-BLOCKING NOTES

No repository-coherence defect found in scope. One low-severity branch note and one `main`-side
defect recorded; neither would mislead a fresh session about live project state.

### B.1 Scope / ownership — clean

Mechanically verified from the diff against the merge base (`2995b442`):

- Exactly **three new files**, all under `canon/experiments/architecture-outcome-v1/` — precisely
  the task's three deliverable paths. No existing file modified.
- Therefore mechanically: the marketplace demand bank
  (`canon/research/marketplace-demand-v1/**`) is **byte-identical to `main`** — no buyer intent
  changed, bank not mutated; no fixture files created; no media generated (text-only additions,
  `spend_usd: 0`, `generations: 0` recorded in the triage meta).
- Route/model vocabulary is used only to *name* production dependencies; the triage header states
  this explicitly and no model selection or model-quality claim appears. Exactly 16 cases were
  analysed (see B.5).

### B.2 Authority / status — a fresh session cannot mistake the split for frozen

Checked every status/meta/narrative location in all three files:

- `proposed-brief-split.yaml`: file header "STATUS: PROPOSED. NOT FROZEN. The Controller freezes
  the final split"; `meta.status: PROPOSED_NOT_FROZEN`; the holdout-discipline preamble is
  conditional on "Once the Controller freezes a split"; the freeze checklist addresses the
  Controller as a future actor.
- `marketplace-feasibility-triage.yaml`: header "STATUS: PROPOSED WORKER OUTPUT. NOT FROZEN. NOT A
  CONTROLLER DECISION"; `meta.status: PROPOSED_WORKER_OUTPUT_NOT_FROZEN`; "Not an authorisation.
  The Controller freezes the split; this file … only propose[s]."
- `CANON-013-CONTROLLER-BRIEF.md`: "proposed here, not frozen"; decision needed from Controller is
  "freeze, amend or reject"; epistemic check states "the split is explicitly PROPOSED_NOT_FROZEN".

No location says or structurally implies the split is frozen. This matches the authoritative state
in `CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md` (triage accepted; split NOT frozen; no
further CANON-013 execution) and the `CONTROL-STATE.md` CANON-013 row. The brief's proposed
holdout-access rule is labelled as needing a Controller decision to become binding — a proposal,
not an enacted rule.

### B.3 Holdout integrity — provenance and status honest

- Development and proposed holdout are structurally separated; holdout cases are listed by id and
  coarse shape only, with the stated reason that development-focused workers need never open the
  holdout entries (which remain, correctly, only in the unchanged CANON-011 bank).
- The split file states the selection basis ("pre-generation feasibility + representativeness
  only") and `model_quality_information_used: none_exists_and_none_used` — consistent with the
  project's own state (zero qualified models; the only model-comparison evidence, the A-TEXT 7/16,
  is nowhere referenced as a selection input, verified by search of all three files).
- Whether these are the strategically best 8/8 is not judged here (Controller question).

### B.4 Current-state consistency — merging stales nothing

- No current-state document is touched. Content-checked: `PROJECT-MEMORY.md` (which does not
  discuss CANON-013 case-level detail), `CONTROL-STATE.md` (CANON-013 row: execution complete,
  split unfrozen — exactly what the files say), the marketplace-bank claims (18 cases / 16
  runnable / MKT-015 blocked-evidence-only — all restated consistently), and the
  architecture-experiment gate ("Before architecture-test media exists, freeze the
  representative-deliverable policy, development/holdout split and decision protocol" — the brief
  and split defer to precisely that gate) all remain true with the branch merged.

### B.5 Paths / counts — mechanically verified

| Check | Result |
|---|---|
| Bank cases with `runnable_now: true` on `main` | **16** (MKT-001…014, 017, 018); MKT-015 and MKT-016 are `false` |
| Triage entries | **16**, each runnable id exactly once, none duplicated, none omitted |
| MKT-015 / MKT-016 in triage | Only in `excluded_by_bank_itself`, with reasons matching the bank's own flags; **not** triaged, **not** in the split |
| Proposed split | development **8** + holdout **8**; union = the 16 runnable ids exactly, intersection empty |
| Burden classes | Triage per-case values (5 low / 7 medium / 4 high) match the brief's distribution and the split's balance audit exactly (dev 2/4/2, holdout 3/3/2) |
| Bank stability claim | "Nothing in `canon/research/marketplace-demand-v1/` changed between base `719c90f` and `2995b44`" — **verified true** by diff |
| Referenced paths | Bank, CANON-011 integration decision, revised-programme decision, task file — all resolve on `main` |

### B.6 Branch state — behind `main`, no rebase required

Same situation as CANON-012: based on `2995b442`, clean `git merge-tree` merge onto `d164f49`, and
the `main` delta (Controller decisions on CANON-012/EVAL-035/RES-007) touches nothing CANON-013
depends on or asserts. No rebase required.

### B.7 Non-blocking notes (routed, severity Low)

- **B-N1 — "gate 2 in CONTROL-STATE" is a stale pointer.** The brief's recommended-next-step says
  the split freeze is "gate 2 in CONTROL-STATE". That was exact at the branch's base
  (`2995b442`, where Next gate item 2 was "Review CANON-013 and freeze the … split"). On current
  `main` the gate list was rewritten and the split freeze now sits at the item reading "Before
  architecture-test media exists…". The underlying gate still exists and is unambiguous in
  substance; only the number moved after the branch was cut. Self-correcting on contact with
  current CONTROL-STATE. Owner: Canon (brief), no action required before merge.
- **C-N2 (main-side, not this branch's defect) — duplicate Next-gate numbering in
  `CONTROL-STATE.md`.** The current Next gate list on `main` is numbered 1, 2, 3, 4, 3, 4, 5, 6, 7
  — two items numbered 3 and two numbered 4 — making numeric gate citations ambiguous. Introduced
  by the post-`2995b44` Controller state edits, not by either reviewed branch. **Corrected in this
  Governor branch** as a factual/navigation current-state correction within the review's authorised
  scope (`GOVERNOR-CONTRACT.md` §2): the trailing five items renumbered 5–9, no wording changed.

**CANON-013 blocking findings: none.**

---

## Repository changes made by this review

Within Governor write boundaries only (`GOVERNOR-CONTRACT.md` §2); no Canon-owned file edited, no
branch merged, no domain task opened, no Controller decision changed:

1. This review artifact (`governance/reviews/GOV-L1-PREPILOT-CANON-012-CANON-013.md`).
2. `coordination/CONTROL-STATE.md` — renumbered the duplicated Next-gate items (C-N2); no wording
   or substantive content changed.
3. `PROJECT-MEMORY.md` — one navigation line: the authority-map row "Current Governor review" now
   points at this file (it pointed at GOV-006, which remains the last full reconciliation and the
   last memory content refresh; that header statement is unchanged and still true).

## Merge posture (advice to the Controller — the Governor does not merge)

Both branches are coherent as they stand and merge cleanly onto `d164f49`. **Neither branch
requires a coherence correction before merge.** The non-blocking notes need no pre-merge action.
