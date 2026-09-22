# PART 17 — TWO-WEEK RECOVERY PLAN

RECOMMENDATION. Written after the diagnosis (Parts 1–12), the decision tree (Part 14), the architecture (Part 15) and the experiments (Part 16). It is a plan for the Controller to authorise, not work this audit performs: nothing below has been started, no PR has been opened, no Controller state has been changed. Costs are provider ceilings; owner hours are estimates (INFERENCE from the three cases). The plan is sequenced so that USD-0 and reversible work comes first and every paid step is gated by the result before it.

## Principles

1. **No new knowledge, no new Lab, no new runtime before the loop is fixed.** The first week spends USD ≈ 6 and produces the instruments; the second week spends ≈ USD 65 and runs one real job through the new path.
2. **Everything reversible is a branch; everything irreversible is a Controller decision.** Three decisions are needed (D1–D3 below); the rest is skill and code on branches.
3. **Human minutes are the budget.** Target ≤ 6 owner-hours in week 1 (mostly judging) and ≤ 4 in week 2 (three pause points + release on one job).

## Week 1 — instruments and the loop (USD ≤ 6; owner ≈ 6 h)

| Day | Work | Owner | Output | Gate to next |
|---|---|---|---|---|
| 1 | **D1 (Controller decision):** record this audit's location and status; annotate `CONTROLLER-EVAL-037-CONCLUSION` as "preference recorded; judging uncommitted"; reword C-10 to "no *pack* without a decision; reading a gap domain is never forbidden"; retire WORKFLOW L118-119 by decision. Decide whether this audit folder is committed and where. | 30 min | one decision record | — |
| 1–2 | **E6 judge reliability** (Part 16): assemble the 15 artefacts (sha-listed in Part 6 §0); two non-author reviewers; blind order; accept/reject + defect class; compute κ. Draft the ~25-item rejection checklist *with* the judges from the 42 items (council 10 §4.2). | 2 h judging + 1 h checklist | `eval/experiments/E6/` κ + frozen checklist | κ ≥ 0.4 (else: rewrite checklist, re-run E6 on items before anything else) |
| 2 | **E0** Cumin brief → strong model, no repo context, 5 samples (USD < 1). | 0 | 5 packages scored | informs whether "proceed on the brief" alone caused DF-07 |
| 2–3 | **E4 + E5** (USD ≈ 5, no media): fresh-context replay of 8 artefacts with the checklist; gated re-assembly of Cumin V1–V3 from the committed components (`check_vo_schedule`, a subject-box obstruction gate written for the experiment, edge-trim audio) and 002 B1-lineage tiles under the runtime gates; blind A/B. | 2 h | flip rates; self-PASS lines overturned | NODE 1 answered |
| 3–4 | **Skill rewrite on a branch** (no merge): (a) progressive disclosure — SKILL.md ≤ 2 k tokens with stage files on demand; (b) creative stage first; (c) the twelve intake decisions as non-null fields with `asked | decided | derived`; (d) the ≤12-line structure checklist with cited ids and the 3–5 negative examples copied from Q&A with ids; (e) pause points P1/P2/P3 with binary questions; (f) `reviews[]` filled by a fresh-context checker session (the Karl/Ezra line deleted); (g) "CF-flagged ⇒ not a deliverable"; (h) REJECT ⇒ re-brief, not "repair that layer"; (i) fix the four instruction conflicts (PriceBook workaround, one-off gates, D1 PASS-by-eye, HITL trap 8); (j) PROFILE.md replaced by a one-page proven/unproven sheet; (k) MF priors P8/P10/P16/P7/P13/P18 as directional notes with `checked:` fields at the tier the operator reads. | 1 h review of the diff | `work/skill-v2` branch; token count before the brief ≤ 15 k | Controller review of the diff (not merge yet) |
| 4–5 | **Shared dispatcher + compositor on a branch** (no merge): consolidate `tools/dispatch.py` and `tools/compose.py` from the Cumin job into one importable module with tests; it calls the six existing gates + `check_vo_schedule`; adds subject-box obstruction (shared primitive for 002 SUBJECT_AWARE_CROP and 003 WALL_OBSTRUCTION), loudness/true-peak, narration-hole (`silencedetect`), per-geometry composition, ElevenLabs/fal balance reads, attempt-id lock. `check_case.py` gains: every `promoted_now` id must resolve to a caller; every re-derived candidate must cite its prior; a class-keyed cross-case index; K7/K13/K14 in the vocabulary. | 30 min review | `work/shared-assembler` branch; tests green | — |
| 5 | **D2 (Controller decision):** reconcile the three "creative architecture" diagnoses (001 / 002 / 003) into one ruling; decide NODE 5 (agency path is the product; `runtime/loop` frozen); decide the archive moves of Part 10 (bindings, ontology, context spec, `history/`, stale HANDOFFs, WORKSTREAM-STATUS, sealed media out of git) — moves, not deletions. | 30 min | one decision record | — |

End of week 1: κ known; NODE 1 answered; skill-v2 and shared-assembler branches reviewed; three decisions recorded. Spend ≤ USD 6. If E4 < 50 % *and* E5 does not flip, stop here and run E1/E3 before touching the skill further.

## Week 2 — one real job through the new path, and the knowledge question (USD ≤ 65; owner ≈ 4 h)

| Day | Work | Owner | Output | Gate |
|---|---|---|---|---|
| 6–7 | **E1 + E3** (USD ≈ 43): context ladder and short checklist on the 9 briefs; two reviewers by unanimity; pre-registered; oracle contexts hashed before generation; packages stripped of treatment disclosure. | 2 h judging | NODE 2 answered | decides whether any pack is compiled and in what form |
| 7 | **D3 (Controller decision):** on E1/E3 — Canon as provenance library (default) or compile `commercial_communication` in checklist form (only if g > f by unanimity). Merge skill-v2 and shared-assembler if week-1 review passed. | 30 min | decision + two merges | — |
| 8 | (If NODE 2 said knowledge matters) **E2** (USD ≈ 12) with ten packs compiled on the experiment branch only; **E7** (USD ≈ 8). Otherwise skip both. | 1 h | NODE 3/4 | — |
| 8–10 | **One real job** through the new path — the Cumin brief re-run from the verbatim brief is the natural choice (accepted plates and voice already exist at USD 0; the human's rejection criteria are known): P1 (completed brief + checker answers + cap), P3 (voice: Leda + two candidates on the longest line, before plates), P2 (six-frame board from plates with measured VO), then clips via the shared dispatcher, assembly via the shared compositor, release. Cap USD 8 as before. Record human minutes. | 3 pause points ≈ 20 min + release | one job record on the new template; TTAO and human minutes measured | accept/reject by the owner and one non-author reviewer |
| 10 | **Sync** through the amended `check_case.py`; the first case where "promoted" must mean "has a caller". | 15 min | case 004 | — |
| 10 | **E8 plate ablation** (USD ≈ 0.35) if E1 left U9 open. | 15 min | — | — |
| 10 | **Closing note** to the Controller: what the tree decided; what remains open (Part 13 R-items that need a paid order: R15–R19). | — | — | — |

## Not in the plan (deliberately)

- Compiling the eight packs (pending D3).
- Any Capability Lab spend.
- Any runtime-loop work (NODE 5 frozen).
- Q&A retrieval, grading beyond the five copied items, or any training.
- Governance refreshes, snapshots, or a new PROJECT-MEMORY; the archive moves in D2 are the only state work.
- Changing the Upwork profile (out of scope for this audit; council 03's contradictions are listed for the owner).

## Success test at day 10

| Measure | Now (three cases) | Target |
|---|---|---|
| Defects found by the human vs by gates/checker before presentation | 46 vs 3 | ≥ half found before the human sees a version |
| Human decision points per job | 13 / 11 / 15 | ≤ 5 (P1, P2, P3, release, one veto) |
| Proposition / product role / CTA / end card approved before spend | never | at P1, on every job |
| Timeline fixed before VO | 003 yes | never |
| CF-flagged file delivered | 003 ×3 | never |
| Promoted gate with no caller | 6 + 1 | 0 |
| Tokens before the brief | 60–80 k | ≤ 15 k |
| Owner hours per job | 1–8 | ≤ 1.7 (break-even, council 11 §7) |

If the re-run Cumin job is accepted by the owner and the non-author reviewer at ≤ 1.7 owner-hours, the architecture in Part 15 is supported at n = 1 and the next step is a second, different job class (a static offer ad from a real product photo — the class the profile sells first). If it is rejected on a dimension the checklist covered, the checker or the checklist failed and E4's reading was wrong. If it is rejected on a dimension the checklist did not cover, that dimension joins the checklist and the case index — which is the loop working.
