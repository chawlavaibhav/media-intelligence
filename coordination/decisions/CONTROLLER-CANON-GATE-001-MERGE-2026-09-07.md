# Controller — CANON-GATE-001 Merge Decision — 2026-09-07

**Status:** ACCEPTED FOR MERGE.
**Role:** Writer Controller.
**Target:** `work/canon-gate-001` at `daea2b0`, merged to `main` by merge commit (never squash or
rebase — the decision trail references commit SHAs).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md` and Rulings
1–12. This record is Ruling 13.

## Basis

Ruling 12 set the merge condition: a checker verdict of PASS or PASS WITH NON-BLOCKING NOTES with
the merge line — "Known PASS-over-unscanned-text paths found at HEAD not already ruled deferred" —
reading **none**. The ninth checker pass returned **PASS WITH NON-BLOCKING NOTES**, the merge line
**none**, and **no new class** on the deferred heading. Every Ruling 12 condition in scope survived
refutation; the after-prompts set reproduced under an independent derivation; the precedence was
enforced by the invariant alone under two ordering mutants; 84 packages, ten anchors, 243 gen3
rows, four hunt tables and the cross-battery in both directions moved only where the ruling said.

## Two corrections to the Controller's own record (checker S-01, S-02)

1. **Ruling 12 condition 2 was over-inclusive by four rows.** It listed 3a-4, 3a-6, 3a-8 and 3d-4
   among rows that "must now ERROR". Each carries only after-prompts-set headings, once each; the
   only rule that catches them is a schema-order or schema-content rule Ruling 12 did not
   authorise. The maker did not under-deliver; it pinned them as the documented boundary, which
   the checker confirmed as the correct reading. The four rows are R-01 residual by name.
2. **The R-01 residual register entry is amended.** It read "a known post-prompts heading *in
   schema order* with a quoted run under it". The refinements leave open "after-prompts-set
   headings, each once, in **any** order" — the checker's 3a-8 and E2 (all seven reversed) both
   pass unscanned. Same mechanism; closable only by the production blueprint schema. The register
   entry now reads: **R-01 residual — after-prompts-set headings, each at most once, in any order,
   with a quoted run or blockquote under one of them: that content is the section's prose by
   definition. First GATE-002 design item.**

## What merges

- `canon/gate/` — the compiled-doctrine gate: render-by-id registry of the 21 check lines, package
  parser, pre-dispatch and post-draw runners, stdlib container probes, text-scan interface with the
  Cloud Vision adapter wired and never invoked, CLI. Every check traces to a committed pack
  `check_id` or the pack limit line; every unmechanised line is reported, never counted.
- `tests/test_gate_*.py` — 274 gate tests; a 172-row regression battery that prints intended vs
  observed and exits non-zero on any mismatch; a no-silent-discard invariant over 92 sections.
- `canon/gate/GATE-BUILD-PLAN-v0.md` with Controller annotations for Rulings 9–12.
- Thirteen Controller decision records for this task.

The extractor's guarantee at merge, in one sentence: **every straight-quoted run and every
blockquote line inside `GENERATION_PROMPTS` is either scanned or the cause of an ERROR; curly
quotes, sub-floor runs, unbalanced runs, unknown headings, before-only headings and repeated
headings after the prompts all fail closed; the only unscanned content is prose outside any run
(P-06) and content under a genuine after-prompts schema heading (R-01 residual), both on the
GATE-002 register by name.**

## What this merge does not establish

A gate PASS establishes structure over the submitted bytes — not doctrine satisfaction, quality,
outcomes or adoption. Ten of the 21 doctrine check lines are mechanised partially and eleven not
at all; the gate says so on every run. **Whether Canon works remains reserved to the Controller**
(`CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`); nothing here bears on it.
The post-draw text scan is NOT_RUN in production until a separate spend authorisation invokes the
qualified detector.

## CANON-GATE-002 register at merge (opened, not authorised)

L-02..L-07, K-07..K-10, M-03..M-06, N-02..N-04, P-03..P-06, Q-02..Q-04, R-01 residual (as amended),
R-03..R-05, the digit-glued and lazy-continuation shapes, the F-02/F-03 vocabulary residuals, and
the root-cause item: replace free-prose prompt extraction with an unambiguous prompt boundary in
the production blueprint schema (Ruling 3) so extraction is a lookup, not a guess.

## After merge

Governor refresh of `PROJECT-MEMORY.md` and `coordination/CONTROL-STATE.md` (both say the gate is
designed, not built) with byte-for-byte snapshots under `history/`; `canon/HANDOFF.md` routed to
the Canon stream as stale since the PR #83 merge. No new task is authorised by this record.
