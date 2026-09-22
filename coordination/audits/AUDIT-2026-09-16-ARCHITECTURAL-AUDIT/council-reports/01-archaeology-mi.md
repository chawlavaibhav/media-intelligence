# AGENT 1 — Project Archaeology: chawlavaibhav/media-intelligence (MI)

**Scope.** Reconstruct MI from first commit `2cf4988` (2026-08-24 12:44 IST) to `main` `3bb9a3c` (2026-09-15 14:38 IST), plus the unmerged production/sync branches through 2026-09-16, using git history and decision records as primary evidence. PROJECT-MEMORY.md and CONTROL-STATE.md were treated as maps and checked against git.

**Read-only.** Nothing in any repo or worktree was modified. All counts below were computed with the commands shown.

**Labels:** OBSERVED (verified in bytes/git), INFERENCE (derived), HYPOTHESIS, UNKNOWN.

---

## 0. Global numbers (computed)

| Measure | Value | Command / source |
|---|---|---|
| HEAD of main | `3bb9a3c3da484e43d4d54ae20543d1d246769ac6` | `git rev-parse HEAD` |
| Total commits on main | **899** | `git rev-list --count main` |
| Span | 24 Aug 12:44 → 15 Sep 14:38 IST = **22.1 days**; 19 calendar days with commits | `git log --format=%ad` |
| Commits per day | **40.7 / elapsed day**; 47.3 / active day | 899 ÷ 22.08 |
| Busiest days | 28 Aug 147 · 27 Aug 142 · 24 Aug 105 · 26 Aug 105 · 1 Sep 77 · 9 Sep 77 | per-day histogram |
| Files on main | 5,288 | `git ls-tree -r --name-only main \| wc -l` |
| Markdown files on main | **799** | `… \| grep -c '\.md$'` |
| Prose words in those .md files | **1,109,283** | `git ls-tree -r --name-only main \| grep '\.md$' \| xargs cat \| wc -w` |
| Controller decision records | **117** files in `coordination/decisions/` (116 `CONTROLLER-*` + 1 `DRAFT-…-SUPERSEDED`) + 2 `canon/decisions/` + 1 `eval/decisions/` = **120** | `ls … \| wc -l` |
| `coordination/DECISION-LOG.md` index rows | 51 (curated index only; ~44 % of records) | `grep -c '^|'` |
| Governor reviews | **8** in `governance/reviews/` (GOV-003…006 full; GOV-L1 ×4) + 1 GOV-001 hygiene audit. **Zero Governor reviews after 30 Aug**; five "Governor refresh" commits since (`c98f9a0`, `fa9b806`, `c771fef`, `2551bd9`, `d11a394`) | `ls governance/reviews` |
| Distinct task IDs | **71** well-formed IDs in file names (CANON-001…014, EVAL-001…041 incl. 039A/B/C, RES-001…007, GOV-001…006, REP-07, PILOT-001, EMP-001; excluding placeholder `CANON-00X`); 73 in prose (adds GOV-007, never authorised, and two stray tokens). Not counted: CANON-GATE-001, REP-01…06, RR-1…16, C-1…C-18, AGY-… job ids | `grep -oE '(CANON\|EVAL\|RES\|GOV\|REP\|PILOT\|EMP)-[0-9]{3}[A-Z]?' \| sort -u` |
| PRs | 103 opened; **85 merged**, 6 closed unmerged, **12 open** (#23, #37, #71–#76, #78–#80 EVAL-037 lanes, #84 CANON-015, #94 audit brief, #103 Cumin sync) | `gh pr list --state all` |
| Registry rows | **575** data rows (+6 non-JSON header lines in the jsonl); validator PASS | `python3 eval/registry/validate_registry.py` |
| Live Canon | **37** audit-gate records, 0 errors | `python3 canon/validation/validate_audit_gate_v02.py` |
| Q&A corpus | 23 banks, **1,028** items | yaml count over `canon/qa/canon-014/*-qa-bank.yaml` |
| Routing map | 61 cells: 36 `clean_observed`, 25 `directional_only`, 17 eliminated | `eval/capability-map/TAINT-REGISTER-v1.yaml` |
| Runtime | 97 .py files, 38 test files, 481 `def test_`, 15 dry-battery runs, **0 provider calls by `runtime/alpha` on main** | `find runtime -name '*.py'`; `ls runtime/battery/results/2026-09-14` |
| Git worktrees | 44 | `git worktree list \| wc -l` |

**Total recorded provider spend, all eras (lower bound):** ≈ **USD 162** — EMP-001 2.664 + PILOT-001 1.60 + EVAL-037 ≥ 8.37 (no consolidated total exists) + EVAL-038 2.260 + Capability Lab 122.241 + Upwork intro 15.393 + portfolio 4.660 + Cumin 5.091. Vendor statements have never been reconciled (CONTROL-STATE §6, C-2). Human-accepted deliverables against that spend: **10** (one 57-s film, nine portfolio tiles), all produced by pilot scripts, none by the runtime.

---

## 1. Era chronology

Era boundaries are from author-dates in `git log --reverse`; commit counts per era were computed by a script over those dates (`scratchpad/audit/work/gitdates.txt`). Day numbers count from day 0 = 24 Aug.

### E0 — Foundation: thesis, PROJECT-CONTRACT, three workstreams (24 Aug, day 0) — 105 commits, USD 0

- **Question:** Can an "API-native media production intelligence layer" be built by three parallel workstreams (Canon / Eval / Resources) under a human Controller, with Cost per Accepted Outcome (CpAO) as the metric?
- **Built:** `coordination/PROJECT-CONTRACT.md @ 2cf4988` (edited only 4 times since; last `97d822d` 28 Aug): product goal, the flow `CUSTOMER INPUT → NORMALIZED REQUEST → CREATIVE IR → PRODUCTION PLANNING/ROUTING ← CAPABILITY REGISTRY → tools → EVALUATION → REPAIR → ACCEPTED OUTCOME → EMPIRICAL MEMORY`, 13 "major separations", "The Controller merges". Same day: communication standard (7 doc commits), CANON-001/002/003 (16-book extraction, PR #4), EVAL-001/002/003 (capability battery V0, Devanagari calibration pack, PR #3), RES-001/002 (corpus pilot, PR #2), EVAL-004 (two-reader Hindi reference).
- **Tested:** CANON-003 stress-extracted 18 books, stopped at 16 (`canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md`). EVAL-004 single-reader pilot, 54 items.
- **Evidence:** 16 usable books integrated (`canon/findings/CANON-003-multi-source-synthesis.md @ dc64ff8`). EVAL-004 stopped after Reader A — "no Reader B and no two-reader reference" (`eval/decisions/EVAL-004-STOP-2026-08-24.md`).
- **Controller decision:** "stop CANON-003 extraction at 16 usable books" (`d462070`); "stop EVAL-004 after single-reader pilot" (`885801a`).
- **Later production used:** the Contract's *vocabulary* (NR, Creative IR, Registry, CpAO) survives in every later document and in the `/media-agency` skill; the Controller-merges rule survives.
- **Abandoned / never consumed:** Creative IR as a runtime object (see §3); EVAL-004 two-reader reference; "Production IR — does not exist yet" stayed true for 17 days.

### E1 — Audit Gate v0.2, Canon 16→19, Repository Governor (25 Aug, day 1) — 17 commits, USD 0

- **Question:** How is a book admitted to Canon (CANON-004/005)? Who keeps the repository coherent (GOV-001)?
- **Built:** Audit Gate v0.2 (`canon/audit/AUDIT-GATE-v0.2.md`, PRs #6/#7); CANON-006/007 reserve sources (PR #9/#10, live 19); CANON-008 stopped at acquisition (PR #13, "archive exposes a 3-page abstract, not the thesis"); EVAL-005 96-item validated view (PR #12); Governor design spec `docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md`, GOV-001 hygiene reset (PR #16).
- **Evidence:** GOV-001 audit verified Canon 19/19, battery hashes, corpus manifest (`governance/audits/2026-08-25-initial-repository-hygiene-audit.md`).
- **Controller decision:** `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`; `CONTROLLER-POST-AUDIT-UNBLOCK-2026-08-25.md` (authorised EVAL-006 registry bootstrap and GOV-002 — both later paused/superseded).
- **Later production used:** Audit Gate v0.2 is still the admission method (37 records validate today). The Governor role persisted as a *refresh* function.
- **Abandoned:** EVAL-006 paused within a day (`CONTROLLER-PAUSE-EVAL-006-PENDING-MASTER-PLAN-2026-08-26.md`), spend authority withdrawn, never resumed; GOV-002 "assigned but never executed; superseded" (`governance/status/2026-08-26-GOV-002-SUPERSEDED.md`).

### E2 — V1 overnight → macro reset → pre-execution freeze (25 Aug 20:00 – 26 Aug 22:30, days 1–2) — 124 commits, USD 0

- **Question:** What should be measured, on what briefs, with what persistence — before spending the first dollar?
- **Built:** V1 overnight (C1–C4, E1–E5, R1–R5; PRs #17–#19): 30-brief bank, 36-capability contract, 100-item Eval bank, persistence v2.1, "generate-once harness + empty Registry interface". Then CANON-009 request-space research + Media Request Grammar (PR #20), EVAL-007 (PR #24), RES-003 (PR #25), EVAL-008 model roster (PR #23 — **still OPEN**, superseded by EVAL-010). Then the freeze: CANON-010 (7 operation values; PR #27), EVAL-009→EVAL-011 (44 = 43+1 capabilities, 13 condition families, Q=0·A=90·B≤404·C=32; PRs #30/#31), RES-004 (topology v3, CpAO v3; PR #28), EVAL-010 (26 rows, 2 execution-ready; PR #29). GOV-003, GOV-004 reviews.
- **Evidence (the consequential one):** CANON-009 found the 30-brief bank inverted against real demand — `edit a supplied asset` 82,976 real requests / 0 briefs; `animate a supplied image` 1.70 M+ / 0 briefs; exact in-image text 28/30 briefs with no real-user frequency figure (`history/GOVERNANCE-2026-08.md` §"macro reset"; reproduced in GOV-003).
- **Controller decision:** `CONTROLLER-CLOUD-MACRO-RECALIBRATION-2026-08-26.md` — "the benchmark was becoming the specification"; `CONTROLLER-PRE-EXECUTION-CLOSURE-2026-08-26.md` froze the v2 contracts.
- **Later production used:** CANON-010's Normalized Request vocabulary is the `nr.*` block in the `/media-agency` skill (`PRODUCTION-WORKFLOW.md:44-52`, `:102`) and in the Cumin JOB.yaml; the persistence rule "one call = one trial, failed calls kept" survives in every ledger since.
- **Abandoned / never consumed:** the 30 briefs (used only in EVAL-037/038 as 6 of them), the 100-item bank (never scored), the 90-generation Stage A (never run as designed — Stage A ran 8–10 Sep on a different 35-case package), Stage B and Stage C (never), EVAL-008 roster (open PR), the "494 generations · 5,515 evaluator calls · 188 human units" ceiling (never approved). The v2 contracts still carry `NOT IN FORCE` headers (GOV-005 F-6).

### E3 — EMP-001: first paid tranche, exact-text evaluator hunt, A-TEXT (26 Aug 22:30 – 28 Aug 03:12, days 2–4) — 235 commits (the densest era), USD 2.66

- **Question:** Can any evaluator certify exact text (Devanagari/Latin) so that a Registry row can be admitted? Then: which of two image routes renders exact text?
- **Built:** EVAL-012…016 execution stack (five Controller review loops before spend: live-path defects, budget continuity, ambiguous dispatch, human-review gate); EVAL-017/018/019 judge roster switched OpenAI → Anthropic → Sonnet 5 (PRs #40–#42); EVAL-020/021 contract v2; EVAL-022/023/025 OCR family (PRs #45–#47); EVAL-024 sealed A-TEXT generation (PR #50); EVAL-029 benchmark-grade OCR (PR #51); EVAL-030 scoring (PR #53); EVAL-026 temporal machinery (PR #52); RES-005 12 clips (PR #54); CANON-011 marketplace brief bank (PR #49); GOV-005, GOV-006.
- **Tested:** five judge configurations for strict exactness; 16 images (4 strings × 2 repeats × 2 routes).
- **Evidence:** all five strict-exactness candidates **disqualified**; Cloud Vision `TEXT_DETECTION` benchmark-qualified only (false-pass 0.125 Devanagari / 0.104 Latin); A-TEXT **7/16 exact** — GPT Image 2 6/8, Ideogram v3 1/8, ₹-sign claims 0/4 (`eval/empirical-tranche-1/evidence/EMP-001/atex-scoring/atex-benchmark-scoring-v1.json`; `CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md`). Mechanism finding: recognisers repair misspellings on purpose; Tesseract with dictionaries off → false passes 3 but false-fail 0.67 (`history/EMP-001.md`). Spend USD 2.6397905 through EVAL-024 + 0.024 (ceiling USD 10; `CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md`).
- **Controller decision (quoted):** "Do **not** populate the Capability Registry from EVAL-030 … weakening Registry admission semantics merely to create a first row would destroy the meaning of the Registry. Registry remains 0 rows." And the course-correction `CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md`: exact text becomes non-blocking; EVAL-028 (two-human gate) cancelled.
- **Later production used:** the *conclusion* that exact text must be composed by code (mechanism B) became Alpha-1's definition (C-7) and every production since (pilot "exact text by code" `70f687e`; Cumin `route: code`). The spend-ledger / cap / 0-retry discipline persisted into harness-v2 and the agency job ledger.
- **Abandoned / never consumed:** Cloud Vision as a production text checker (wired into the gate on 7 Sep, **never invoked**); the 16 A-TEXT images and 7/16 (never re-used in routing — RR-2's in-scene text evidence came from the Lab instead); EVAL-026's 13 perturbation types and RES-005's 12 clips (no temporal evaluator ever qualified; EVAL-031 stopped, EVAL-032/033 stopped, EVAL-034 cancelled, RES-006 deferred — `CONTROLLER-STOP-TEMPORAL-PREP-PRIORITISE-PRODUCT-PILOT-2026-08-28.md`); GOV-007 never authorised.

### E4 — Context migration, pre-pilot tranche, PILOT-001 (T1) (28 Aug, day 4) — 68 commits, USD 1.60

- **Question:** Can the project produce one real accepted outcome end-to-end (Aight vertical slice)? Also: can the memory documents be made readable (the two local 28-Aug reviews said PROJECT-MEMORY had grown 44 KB → 105 KB in two days and that "no Creative IR instance has ever been created — not one").
- **Built:** context-architecture migration (PR #56: `history/`, `shared/CONTEXT-SUFFICIENCY-POLICY.md`, `verify/VALIDATOR-INDEX.yaml`); CANON-012 Aight NR + Creative IR seed (PR #58 — the **only** Creative IR instance ever authored: `canon/experiments/pilot-001/aight-creative-ir.yaml`), CANON-013 marketplace triage (PR #59: all 16 runnable cases are video, most need speech), EVAL-035 direct-Gemini video substrate (PR #61), RES-007 pilot outcome writer (PR #60); PILOT-001 frozen, USD 2 cap.
- **Tested:** two Veo 3.1 fast text-to-video candidates (USD 0.80 each), 13/13 hard checks PASS both times.
- **Evidence:** both rejected by the human ("still garbage"); H1 modern/premium FAIL, H6 publishable FAIL; **CpAO undefined — USD 1.60 / 0 accepted** (`CONTROLLER-PILOT-001-CANDIDATE-2-REJECTION-AND-T1-CLOSURE-2026-08-28.md`). Evidence branch `work/pilot-001-aight-execution` merged (`7830f8a`).
- **Controller decision (quoted):** "PILOT-001 / T1 IS CLOSED AS AN HONEST, FULLY-EVIDENCED FAILED VERTICAL SLICE. NO REPAIR REMAINS. NO FURTHER PILOT-001 PROVIDER CALL IS AUTHORISED, EVER." Root cause: "text-to-video from descriptive words, with no concrete product hero and no pre-approved visual". Proposed USD 25 T2 screen declined (`1aea9b9`).
- **Later production used:** the root-cause lesson — image-first, hero still, then minimal motion — is exactly the recipe of EVAL-040's accepted cells and the Cumin plan (plates → i2v). The compact PROJECT-MEMORY format survived.
- **Abandoned:** the Aight Creative IR (zero references in `runtime/`: `grep -ric creative_ir runtime --include=*.py` = 0); EVAL-035's Gemini substrate and RES-007's writer (superseded by harness-v2 on 5 Sep); the programme plan T2–T8 v1 (`coordination/plans/2026-08-28-PROGRAMME-PLAN-T2-T8-v1.md`), superseded next day.

### E5 — Media Factory priors reset, CANON-014 full corpus, EVAL-037 Canon value (29–31 Aug, days 5–7) — 13 commits on main; lane work on 14 unmerged branches; EVAL-037 spend ≥ USD 8.37 (no consolidated total)

- **Question:** (a) Does the predecessor project's evidence change what must be re-proven? (b) Does the same reasoning model do better with Canon than without (T2B)?
- **Built:** `CONTROLLER-PROGRAMME-RESET-MEDIA-FACTORY-PRIORS-2026-08-29.md` (T2–T8 v2); EVAL-036 authorised (USD 0 import); CANON-014 (PR #69: 24 accepted / 18 HOLD / 1,028 Q&A; three donor PRs #66–#68 closed unmerged); EVAL-037 frozen substrate (PR #70: 6 briefs × 4 models × 2 conditions × 3 reps = 144 trials); nine lane PRs (#71–#80, **nine still OPEN**), one repair merged (#77), conclusion merged (#81). Parallel experimental Q&A expansion on `work/canon-parallel-books-qa-experimental` (17 sources, 128 files, 134,743 insertions, **unmerged**).
- **Evidence:** the 144-trial matrix "did not complete symmetrically": Gemma FULL_CANON used Canon **0/18**; unbounded Sonnet FULL_CANON completed **2/18** (16 context overflows); Gemma mandatory-unbounded **18/18 technical failures** (~1.13 M tokens exposed); Sonnet CONTROLLED_CANON 18/18, 53 searches, **1 Canon read in the whole lane** (`eval/experiments/EVAL-037/CONCLUSION.md @ 5b95da1`). Blind judging placed Sonnet NO_CANON and Sonnet CONTROLLED_CANON at the top, CONTROLLED leading B01/B06. Recorded lane costs: sonnet-no 1.1388, haiku-no 0.3314, haiku-full 0.4000, sonnet-full 0.4128 (1 trial) + repair 3.2288 (2 trials), sonnet-controlled 2.8611, gemma `null` (price never established) — PR bodies #71–#80; "actual lane spend is higher".
- **Controller decision (quoted):** "**Canon helps, but the current Canon retrieval / consumption system is not mature.** … accepts a programme-direction result, not a universal quantified treatment effect … Do not rerun failed lanes to improve symmetry" (`CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`). Reset decision: "zero Registry-qualified workflows = zero empirical workflow knowledge. That was false."
- **Later production used:** the reset's seven "settled priors" (image-first → I2V, condition-specific routing, deterministic composition for exact text, provider policy pre-flight) are the shape of the Capability Lab package and of all three real productions. The reset's "prompt enrichment — crucial unresolved question" became EVAL-037/038.
- **Abandoned / bypassed:** T3 (Canon → media propagation) and T4 (cost compression) "deferred, not cancelled" on 5 Sep and never run; T5 replaced; T7 holdout never; the EVAL-036 task as written was never executed — a 5-file hashed import (`eval/historical-priors/media-factory-v1/PRIOR-INDEX.yaml`, 5 rows, imported 5 Sep inside EVAL-039B `fc1f8cd`) stands in for it; the 64 scored stills / 67 human rows / 206 artifacts exist only as manifest references. The MF prior is pointed to by 3 routing-map cells (`ROUTING-EVIDENCE-MAP-v0.yaml:74,475,666,829`) and cited by no production (grep of `production-learning/`, `.claude/skills/`, pilot and Cumin branches: 0 hits). The optional/unbounded retrieval interface was retired.

### E6 — REP-07 admission (24→37), EVAL-038 substitution test, CANON-SHAPE-v1 (31 Aug – 3 Sep 13:30, days 7–10) — 82 commits, USD 2.26

- **Question:** Can a weak model + two compiled Canon packs match a strong model alone (the CpAO lever)? What *is* Canon's consumption shape?
- **Built:** REP-01…06 repair tranche + two compiled packs (`canon/compilation/PACK-product_appearance-v0.yaml`, `PACK-composition_and_attention-v0.yaml`); REP-07 13 inspections → DN-06 admission of 13 sources (PR #85); EVAL-038 substrate, blinded judging, media generation (PR #86); `canon/CANON-SHAPE-v1.md`; PR #83 merged 3 Sep (`599ff4a`).
- **Tested:** Haiku+packs ×2 reps and Gemma+packs vs committed Sonnet NO_CANON over 6 briefs; B06 image pair and B01 video pair executed to real media (2 images USD 0.067 each on gemini-3.1-flash-image, 2 videos USD 0.40 each on veo-3.1-lite); replay pair USD 0.467.
- **Evidence:** substitution **REFUTED 0/6** — Sonnet NO_CANON took all **18/18 top-3 slots** blind; the cheap arm cost more per package (USD 0.072 vs 0.063); spend USD 2.260122 of 10 (`eval/experiments/EVAL-038/RESULTS.md`). Post-reveal: the pack-guided image won B06; both videos failed on baked-in text — the defect the packs guard against; packs retro-forbid both PILOT-001 candidates (`canon/findings/EVAL-038-RETRO-TEST-PILOT-001.md`).
- **Controller decision (quoted):** "The tested substitution configuration is closed … Do not rerun this configuration." And: "**i don't want you to conclude this any further... It's my call eventually to decide whether it works or not.**" (`CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`). Shape adopted with "**Let's stick with that**" (`CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md`); forced-consumption receipts retired.
- **Later production used:** the two packs are injected by the `/media-agency` skill and were injected in the Cumin job ("2 packs injected, 8 gaps", `86ec183`); the shape's pipeline (pack lookup → blueprint → gate → cheapest route → post-draw gate → human) is the skill's stage list.
- **Abandoned / never consumed:** the reserved verdict has never been taken; the "acceptance-rate run (the cheapest decisive measurement)" was never commissioned; CANON-015 bounded retrieval (PR #84 OPEN); `canon/context/CANON-CONTEXT-SPEC-v0.1.md` superseded by pack injection; 8 of 10 packs never compiled (C-10) — the Cumin job hit the uncompiled `commercial_communication` pack (PR #103 class 4). Media from EVAL-038 is "product learning only".

### E7 — CANON-GATE-001 (13 rulings, 9 checker passes) and the Capability Lab direction / EVAL-039 (3–8 Sep 11:00, days 10–15) — 69 commits, USD 0

- **Question:** Can the two packs' 21 check lines be mechanised as a fail-closed gate? Then, from 5 Sep: "I want to move into extensive empirical model/workflow testing."
- **Built:** `canon/gate/` (PR #88: 274 tests, 172-row regression battery, Cloud Vision adapter "wired and never invoked"); 13 Controller records for one task (11 checker dispositions, 5 of them BLOCK); five days on one gate. From 5 Sep, on a Controller-draft branch: EVAL-039A 35 customer-shaped Stage-A cases + 35 blueprints, EVAL-039B Sept-2026 roster + 36 price pins + MF import, EVAL-039C harness-v2 (six adapters, ledger, sealed store, 123 tests) — each with executor/tester/auditor/approver reports (PR #87 merged 8 Sep after ratification).
- **Evidence:** gate mechanises 10 of 21 lines partially, 11 not at all; on fixtures it fails both EVAL-038 videos on the sentences that caused the baked text (`CONTROLLER-CANON-GATE-001-MERGE-2026-09-07.md`). EVAL-039A/B/C: 11/11, 176, 123 mechanical checks pass.
- **Controller decision (quoted):** gate: "A gate PASS establishes structure over the submitted bytes — not doctrine satisfaction, quality, outcomes or adoption." Direction: "**Go for it. Approved now**" (8 Sep), superseding the reset's "do not generate any new media before T2B" and the declined USD 25 screen — "SUPERSEDED, stated plainly" (`CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` §2). Controller voice-note goal: "we eventually want a weaker LLM plus weaker media model to beat the strongest … combination. That's where the win is."
- **Later production used:** harness-v2's adapters, price pins and ledger are what the pilot scripts and the Cumin dispatch tool call; `runtime/route/price.py` (PR #102) normalises against the same roster. The gate: wrapped by `runtime/loop` (14 Sep); Cumin commit `42fab25` says its 10 prompts were "gated" (INFERENCE that `canon.gate` ran; the pilot and portfolio used their own triage tooling).
- **Abandoned / never consumed:** CANON-GATE-002 register (opened, not a task); the gate's post-draw text scan (NOT_RUN in every real production); the maker/checker five-role pipeline was not repeated after 5 Sep.

### E8 — Capability Lab EVAL-040…043 and the 10-Sep audits (8 Sep 11:00 – 10 Sep, days 15–17) — 120 commits, USD 122.24

- **Question:** Which current model/workflow wins which Stage-A case, cheap-first?
- **Built/ran:** Image Round 1 (76 + 8 redo trials, 66 sealed, USD 4.66 + 0.51; composite arm 4/4), half two (21 stand-ins, USD 1.61), video pieces 1–5 (knee, multi-shot, i2v, reference, two-speaker), speech (Sarvam 6/6, ElevenLabs Hindi 2/2 English 2/2 Hinglish 0/2), music (Lyria 4/4), lipsync (0/5), text-to-video core (36/40 sealed, USD 28.29; Gemini Omni 8/8, Kling audio 2/6 eliminated), Wan 2.2 contender (11/16), vision-judge qualification (206 calls, USD 3.16). PRs #90–#93. Registry 167 → 282 → 459 → 485 → 566 → **575** rows (`84a64e9`). Audit closeout `850003f` (nine repairs, taint register, four tools); audit brief PR #94 (OPEN); runtime v0 contracts + PC-03A/PC-03B lanes (`743a5d7`…`e57bb36`, 10 Sep).
- **Evidence:** 35/35 cases dispatched and blind-judged by one person; 311 sealed media; RR-1…RR-16; ledger **USD 119.085109 + 3.156153 judge = 122.241262** counted against caps, USD 10.1145 produced nothing; **two cap crossings** (10.364 vs 9.96; 11.840 vs 11.53) and a 19-vs-16 call breach (`coordination/audits/AUDIT-2026-09-10-SPEND-RECONCILIATION.md`). Vision judge **not qualified**: agreement 66 %, kappa 0.33, false-accept 22 % (`64141f7`). Auditor A: the project "crossed the line from research architecture into a real empirical capability system" (`AUDIT-2026-09-10-REPORT-A.md` §1).
- **Controller decisions:** eight spend records 8–10 Sep (`CONTROLLER-SPEND-AUTHORISATION-*`), `CONTROLLER-INSTRUMENT-THRESHOLDS-FROZEN-2026-09-09.md`, ElevenLabs-direct, fal-last-choice, Gemini-key rulings.
- **Later production used (OBSERVED):** the routes the Lab cleared are the ones the three real productions drew — Veo 3.1 fast i2v, Nano Banana 2, Kling, Lyria, Sarvam, ElevenLabs; the Cumin JOB.yaml cites map cells verbatim ("IMG-CORE/nano-banana-2 … clean_observed 7/8", "VID-I2V/veo-3.1-fast-i2v clean_observed", RR-8/RR-12/RR-13); the Upwork pilot branch references the map in 2 files. The Registry jsonl itself is read only through `runtime/route/evidence.py` (used by Cumin's `build_router`).
- **Abandoned / never consumed:** RR-16 withdrawn; 17 eliminated cells, 3 needing clean reruns (C-15, unauthorised); the vision judge; Seedance/premium sweep deferred; Group-3 items C-12…C-18 never authorised; 524 of 575 rows rest on a single base item and are "reference calculations, not statistics"; **no Registry row has ever been created or changed by a real production** (cases 001/002 and PR #103 all say `routing_authority: none`).

### E9 — 14-Sep rulings C-1…C-11, runtime Alpha-1 vertical slice (11–14 Sep 15:05, days 18–21; 3 idle days 11–13 Sep) — 41 commits, USD 0

- **Question:** How is the Lab's human evidence to be counted, and what is the smallest complete production path?
- **Built:** six decision records materialising fifteen rulings (`ae5ba7d`); taint register regenerated (36 clean / 25 directional / 17 eliminated); `runtime/` on main (PR #95/#96): contracts PRODUCTION-JOB-v1 … TEMPLATE-v0, intake, spec compiler with Canon lookup, Canon Injection v1, router, execution bridge (dry), gates over `canon.gate`, bounded repair, acceptance states, OUTCOME-EVENT-v1, template library, `python3 -m runtime.alpha.cli`; 14-run dry battery; Governor refresh PR #97.
- **Evidence:** every run dry; `spend_authority.status: none` on every profile; 26 of 61 cells auto-routable by `alpha_human_release`.
- **Controller decision (quoted):** C-7 "Freeze Alpha 1 to: one STATIC COMMERCIAL AD WITH EXACT OVERLAY COPY, optionally followed by: one SHORT MOTION VERSION DERIVED ONLY FROM THE ACCEPTED STILL … Exclude … talking heads; lip-sync; native speech; multi-shot stories; generated in-scene exact text." C-9 "Stop widening the Capability Lab." C-10 "Authorise USD-0 implementation of: Canon Injection v1; template / empirical-memory integration. Do NOT compile the remaining eight packs unless a real runtime failure later demands one." C-6b "STRICT interpretation … RR-16 therefore cannot remain clean." Rider: "adopting the Alpha policy is NOT spend authorisation."
- **Later production used:** `runtime.compositor.gates`, `DesignTokens`, `runtime.route.cli.build_router`, `runtime.execute.provider_errors`, `runtime.errors.Refusal` — imported by the Cumin job tools (`git grep '^from runtime' origin/work/agency-job-cuminco-chopsticks-001 -- agency`). `runtime/route/price.py` fixed by PR #102 after the Cumin job found character-metered pricing wrong ("PR #102 fix verified 13:23Z" in JOB.yaml).
- **Bypassed:** **the Alpha-1 family itself.** All three real productions since (speaking presenter multi-shot film; portfolio tiles with narration; spec video ad with VO) are *excluded* by C-7; `runtime/alpha` has run for no real job. OUTCOME-EVENT-v1 "cannot represent a five-version, nine-route, assembly-repaired production honestly" (case 001). The "next gate: first paid Alpha-1 run" (CONTROL-STATE §9) has not happened; instead paid work happened outside it three times.

### E10 — d2c prospecting, Upwork intro pilot, production-learning case 001 (14 Sep 11:16 – 15 Sep 08:04, days 21–22) — 16 commits on main + 5 on the raw branch; USD 15.39

- **Question:** Can the project's routes and compositing discipline produce one real commercial asset the human accepts?
- **Built:** `coordination/commercial/d2c-prospecting` (two runs; Cumin Co. top of run 02, `42e3ecc`); raw pilot branch `work/pilot-upwork-intro-video-v4` (5 commits, 213 files, never merged; V1 USD 3.76 → V2 8.08 cumulative → V3 3.28 → V4 → V4.1 accepted, `f6ca66f`); PR #98 (`production-learning/cases/UPWORK-INTRO-001/`, compositor gates, frame hygiene, pool liquidity, transient-error classification; 467 runtime tests; Controller audit fixed three blockers `fc806c3`).
- **Evidence:** V4.1 accepted 14 Sep; **USD 15.39318** across 54 dispatches (V1/V2 8.082 discarded entirely; cost of discarded attempts ≥ USD 9.32); **TTAO 7 h 54 m** mechanical lower bound; "**zero media-model failures reached the Controller** — every defect was compositor / orchestration / creative direction / QA timing / route choice" (`SYSTEM-DEFECTS.yaml`). Pilot branch: **0 imports of `runtime`** (`git grep` over `pilots/`), 1 file naming a Canon pack, 2 naming the routing map.
- **Controller decisions:** TTAO adopted as primary KPI alongside CpAO; speaker micro-qualification stays candidate; COMPLEX-PRODUCTION-EVENT "deferred until after the second complex real production" (PR #98 audit comment, recorded in CONTROL-STATE §5E).
- **Later production used:** the compositor gates promoted from this case were imported by the Cumin tool; the accepted template `service_intro_with_portfolio_proof` — never reused (Cumin: `template_status: none`).
- **Bypassed:** Alpha-1, `runtime/alpha`, Canon Injection v1, OUTCOME-EVENT-v1, the gate's text detector.

### E11 — Portfolio batch (case 002), generic validator, Media Agency Operator v1, pricing fix (15 Sep 08:30 – 14:38, day 22) — 9 commits, USD 4.66

- **Question:** Can more showcase media be made quickly (portfolio), and can the workflow be packaged so a session *must* follow it (`/media-agency`)?
- **Built:** raw branch `work/upwork-portfolio-samples-2026-09-15` (12 commits, unmerged); PR #100 (`UPWORK-PORTFOLIO-002`); PR #101 generic `check_case.py`; PR #99 `.claude/skills/media-agency/` (SKILL, BOOTSTRAP, PRODUCTION-WORKFLOW, QA-CHECKLIST, JOB-TEMPLATE) + `media-agency-sync`, `docs/media-agency-operator.md` (8 files, +1,179 lines); PR #102 `runtime/route/price.py` character-metered units.
- **Evidence:** 9 tiles accepted, 1 skipped after 2 rejections; USD 4.6596, **USD 3.526 (75.7 %) on rejected/skipped**; chat figure "USD 3.9" was wrong; **process NON-CONFORMANT** — "the batch bypassed the Media Intelligence workflow that had been built and merged the same day (PR #98): no pre-spend packet, copy invented during execution, paid calls straight after a chat 'go' … pilot scripts instead of the runtime / media-agency path, no spend amendment"; **all four V3 failure classes from case 001 came back on the first tile export** (`UPWORK-PORTFOLIO-002/README.md @ 4fdf085`).
- **Controller decision:** "Good final media can coexist with a non-conformant production process … evidence for enforcing the workflow" (case README, Controller 15 Sep). No `coordination/decisions/` record exists for this spend.
- **Later production used:** PR #99's skill was used for the very next job (Cumin) — the first job to follow the workflow.
- **Bypassed:** the whole system, by the project's own account; CONTROL-STATE's "Nothing paid is authorised" was not amended.

### E12 — Cumin Co. job (first `/media-agency` job) and PR #103 sync (15 Sep 18:48 – 16 Sep 09:51, days 22–23) — 0 commits on main; 12 on the job branch, 1 on the sync branch; USD 5.09, 0 accepted

- **Question:** Does the packaged workflow produce an accepted spec ad for a prospect surfaced by d2c prospecting?
- **Built:** `agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/` on `work/agency-job-cuminco-chopsticks-001` @ `de1f978` (immutable evidence; 1,403 files, 50,221 insertions): JOB.yaml with `production_base_sha: 3bb9a3c`, TTAO clock, NR, Canon lookup (2 packs, 8 gaps), 21-check-line blueprint, live-priced routes with map cells, USD 8 in-session cap, dispatch tool with ledger + classifier, micro-qualification with human gates, compose.py through `runtime.compositor.gates`. PR #103 (`work/agency-sync-2026-09-16` @ `1de2b37`, 12 files, +639): case CUMINCO-CHOPSTICKS-003, promotes `check_vo_schedule` (DF-08) with tests, 8 candidate patterns, Canon-gap proposal.
- **Evidence:** V1/V2/V3 all **REJECTED** (mix/mouths/text placement; "no ad structure"; "the voices are overlapping … reject completely"); 50 paid attempts, 47 ok, **USD 5.0907 reserved**, CpAO n/a; component-level accepts (plates, clip-2, voice Leda); fal excluded (balance USD 0.147); ElevenLabs exhausted at 54 credits; `check_case.py` PASS 0 problems (PR #103 body).
- **Controller decision:** none yet on main. PR #103 asks: is this the "real runtime failure" that justifies compiling `commercial_communication` under C-10? (The knowledge exists in accepted Canon `google-abcd-video-ads` but is uncompiled.)
- **Consumed:** NR (CANON-010), 2 packs, gate (INFERENCE), routing map cells and price pins, runtime compositor gates / router / error classes, production-learning cases 001/002 as directional notes (RO-04/05/06/09/10), d2c prospecting output. **Not consumed:** `runtime/alpha` (class excluded by C-7), OUTCOME-EVENT-v1, template library, the 8 uncompiled packs, the Q&A corpus, MF priors, the Registry's deterministic rows as a decision input beyond what the map summarises.
- **Note on the caller's premise:** the branch head is `1aea4d2` (one sync commit after `de1f978`) — consistent with the preamble.

---

## 2. Stale or contradicted claims in PROJECT-MEMORY.md / CONTROL-STATE.md on main (`3bb9a3c`)

Both files were last written at `fc806c3` (15 Sep 07:46 IST) — *before* PRs #98, #101, #100, #99, #102 merged (08:04–14:38 IST). Consequences, all OBSERVED:

| # | Claim on main | Git reality | Severity |
|---|---|---|---|
| 1 | PROJECT-MEMORY:9 "PR #98 open from `work/production-learning-upwork-intro-001`"; §6 "Remaining: merge #98"; CONTROL-STATE:9 "PR #98 open, not merged"; §9(e) "merge PR #98" | PR #98 merged 15 Sep 02:34Z, commit `17b347c` | stale |
| 2 | CONTROL-STATE:11,42 "`main` = `bf92c53`" | main = `3bb9a3c`, six merge commits later (`17b347c`, `3ea8cbc`, `0849957`, `b4a0e5e`, `3bb9a3c`) | stale |
| 3 | No mention of PR #99 (Media Agency Operator v1), the `/media-agency` and `/media-agency-sync` skills, or `docs/media-agency-operator.md` | merged `b4a0e5e`; the skill's BOOTSTRAP tells every session to read PROJECT-MEMORY §1/§2/§5/§7 — which does not know the skill exists | contradiction of the "authority map" §9 |
| 4 | No mention of PR #100 / `production-learning/cases/UPWORK-PORTFOLIO-002` or its USD 4.66; §5 "one human-accepted real commercial showcase asset" | 10 accepted deliverables (1 film + 9 tiles); merged `0849957` | stale count |
| 5 | No mention of PR #101 (generic case validator) or PR #102 (pricing fix) | both merged | stale |
| 6 | CONTROL-STATE §6 spend-of-record table and "Any new paid dispatch — Not authorised"; §8 "any paid or network provider call by the runtime" blocked | Paid dispatch happened twice after the table was written under in-chat caps with no `coordination/decisions/` record: portfolio batch USD 4.66 (case 002 says "no spend amendment") and Cumin job USD 5.09 (cap recorded only in the job's JOB.yaml). Runtime *modules* dispatched paid calls via the Cumin job tool (branch), though `runtime/alpha` on main still has never called a provider | contradiction (spend of record incomplete by ≈ USD 9.75) |
| 7 | CONTROL-STATE §5E / PROJECT-MEMORY §6: "COMPLEX-PRODUCTION-EVENT deferred until after the second complex real production" | the second (case 002) and third (Cumin) complex productions exist; trigger reached, not revisited | stale rule |
| 8 | PROJECT-MEMORY §5 "8 of the 10 compiled packs … none is compiled without a real runtime failure — C-10" | PR #103 proposes the first such failure (`commercial_communication`); undecided | open, not yet stale |
| 9 | `coordination/WORKSTREAM-STATUS.md:18,161` "the Capability Registry still holds **0 rows**"; `eval/HANDOFF.md:33,105` "₹0 API … 0 Registry entries … No Capability Registry exists" (last touched 25 Aug `eaedc33`) | 575 rows; USD ≈ 162 spent. Both files self-declare stale in their headers/notes; PROJECT-MEMORY §7 trap 1 already warns | acknowledged stale, never rewritten |
| 10 | PROJECT-MEMORY §2 "list `coordination/decisions/` directly … DECISION-LOG is a curated index only" | DECISION-LOG indexes 51 of 117 records | consistent with its own caveat |
| 11 | CONTROL-STATE:55 "PR #94 … still open and untouched" | true | — |
| 12 | Both files: "Registry 575", "37 sources / 1,300 objects", "36 clean / 25 directional / 17 eliminated", "USD 122.241262", "USD 15.39318" | all recomputed and match | correct |

An untracked, empty directory `coordination/audits/AUDIT-2026-09-16-ARCHITECTURAL-AUDIT` exists on disk (not ignored, 0 tracked files) — presumably this audit's own placeholder; not evidence.

---

## 3. Designed but never instantiated (on main)

| Design | Where designed | Status / evidence |
|---|---|---|
| **Creative IR** as a runtime object | PROJECT-CONTRACT 24 Aug; Creative IR v0.1 accepted 26 Aug | One hand-authored instance ever (`canon/experiments/pilot-001/aight-creative-ir.yaml`, CANON-012). `grep -ric creative_ir runtime --include=*.py` = **0**. PRODUCTION-SPEC-v1 took its place; the 28-Aug reviewer's "no Creative IR instance has ever been created" is still true for machine-made instances. |
| Production Planner as "requirements (Canon) + Registry (Eval)" | PROJECT-CONTRACT separation 11 | Exists as `runtime/route` since 14 Sep, dry only; used for one rejected job via a job tool. |
| Stage A (90 gens) / Stage B (≤404) / Stage C (32 outcome attempts) | EVAL-011, 26 Aug | Stage A never run as designed (replaced by the 35-case EVAL-039A package); B and C never (C-17/C-18 unauthorised). |
| 30-brief bank, 100-item Eval bank, 36→44 capability contract, 13 condition families | V1 overnight, 26 Aug | 6 briefs reused in EVAL-037/038; the rest never scored. |
| Temporal evaluator qualification (13 perturbation types, 12 clips) | EVAL-026, RES-005, EVAL-031…033 | No evaluator qualified; pass mark `DOES_NOT_EXIST`; EVAL-031 stopped, 032/033 stopped, 034 cancelled, RES-006 deferred. |
| Strict-exactness text evaluator / Registry population from text metrics | EVAL-009…030 | 5 tested, 5 disqualified; Registry admission from text metrics ruled out. |
| EVAL-036 Media Factory prior import (as a task) | reset 29 Aug | Never executed as written; 5-file hashed import inside EVAL-039B (5 Sep). T3/T4/T7/T8 of the reset plan never run. |
| CANON-015 bounded retrieval; CANON-CONTEXT-SPEC v0.1; INJECTION-CONTRACT-v0 receipts | 31 Aug – 1 Sep | PR #84 OPEN; receipts retired 1 Sep; superseded by pack injection. |
| 8 of 10 compiled packs | COMPILED-DOCTRINE-SPEC v0 | Forbidden without a real runtime failure (C-10); first candidate failure raised by PR #103. |
| Acceptance-rate run ("cheapest decisive measurement of the reserved question") | EVAL-038 disposition, CANON-SHAPE §7 | Never commissioned; the Canon verdict remains reserved 15 days later. |
| Vision judge in the release path | Capability Lab | Not qualified (kappa 0.33); C-8 makes humans the release authority. |
| Post-draw text detection by the gate's Cloud Vision adapter | CANON-GATE-001 | Wired 7 Sep, never invoked. |
| Twelve-condition T8 public-release gate | C-11 | 0 of 12 met. |
| First paid Alpha-1 run; live transport behind `ExecutionBridge.run()` | CONTROL-STATE §9 | Not built; `dispatch_mode: live` refuses. |
| COMPLEX-PRODUCTION-EVENT / OUTCOME-EVENT-v2 | case 001 | Design candidate; trigger ("after the second complex run") passed. |
| EVAL-006, EVAL-008 (PR #23), EVAL-028, GOV-002, GOV-007, PILOT-001 T2 screen | various | Paused / open / cancelled / superseded / not authorised / declined. |

## 4. Instantiated but never consumed by a real production

| Artifact | Evidence of non-consumption |
|---|---|
| **Capability Registry, 575 deterministic rows** | Read by the runtime router (`runtime/route/evidence.py`) which the Cumin job invoked — but no production cites a Registry row; every production cites *map cells* and RR rules. No row has ever been created or changed by a real production (`routing_authority: none` in cases 001/002/003). 524 rows rest on one base item. |
| 16 sealed A-TEXT images, 7/16 result; Cloud Vision benchmark qualification | Never used in any production QA (pilot used its own frame triage; runtime frame hygiene — detector identity UNKNOWN). |
| EVAL-037 packages (6 lanes, 14 branches) and EVAL-038 media | Product learning only; the retrieval interface they tested was retired. |
| Media Factory historical prior (5 files) | Pointed to by 3 map cells; cited by no case, skill, or job (grep = 0). |
| CANON-014 Q&A corpus (1,028 items) and the 17-source experimental Q&A branch (134,743 lines, unmerged) | Retrieved once in an EVAL-037 supplemental lane (PR #79 "Q&A 42"); never in production; the branch is unmerged. |
| 13 admitted REP-07 sources / 37-source Canon beyond the 2 packs | Only what the two packs compile is injected; the Cumin gap register lists 8 gaps; `google-abcd-video-ads` knowledge existed and was not reachable (PR #103). |
| CANON-011 18 marketplace cases | "Preferred pool for Stage-C selection" — Stage C never; `runtime/tools/brief_from_marketplace_case.py` exists; dry battery references marketplace briefs 3× (dry). Real jobs came from d2c prospecting instead. |
| `runtime/alpha` one-command chain, Alpha-1 policy profile, Canon Injection v1, template library, OUTCOME-EVENT-v1 store | 15 dry battery runs; zero real jobs (all three real productions are outside the Alpha-1 family by C-7). The one accepted template (`service_intro_with_portfolio_proof`) was never matched again. |
| Governor review machinery (Level-1 / full reviews) | No review since 30 Aug; only state refreshes. |
| Audit brief PR #94; EVAL-037 lane PRs #71–#80; CANON-015 PR #84 | Open, untouched. |

---

## 5. Findings ranked

1. **Every accepted outcome was produced by bypassing the system built to produce it.** 10 accepted deliverables, USD ≈ 25 of production spend, 0 runs of `runtime/alpha`; the pilot imported no runtime module; the portfolio batch was declared non-conformant by the Controller the same day the workflow merged; the first workflow-conformant job (Cumin) was rejected three times. OBSERVED (`git grep` on the branches; case READMEs; PR #103).
2. **Alpha-1 as frozen (C-7) excludes every real job the Controller has actually wanted.** All three productions are speech/multi-shot. The runtime's next gate ("first paid Alpha-1 run") is 2 days old and has been overtaken by three paid non-Alpha productions. OBSERVED/INFERENCE.
3. **Spend of record is incomplete and the "nothing paid is authorised" line is contradicted twice** (USD 4.66 + 5.09 under chat caps with no decision record). The mechanical cap machinery (harness ledger, C-6a lineage) was not the path those spends took. OBSERVED.
4. **The Capability Lab (USD 122, 76 % of all spend) is consumed through a 61-cell summary, not through the 575-row Registry**; and the deterministic rows have never been changed by production feedback. The Registry's stated purpose ("so that later, when a customer job arrives, the system can pick a model") is served by RR rules and human-judged cells. OBSERVED.
5. **The central Canon question is still reserved and un-measured after EVAL-037 (≥ USD 8.4), EVAL-038 (USD 2.26), CANON-GATE-001 (5 days, 13 rulings), REP-07 (24→37 sources).** The only production signal is negative-by-omission: the Cumin job's rejection on "no ad structure" traces to an uncompiled pack whose source knowledge was admitted on 1 Sep. OBSERVED (PR #103 class 4).
6. **Both memory files are stale on the day they matter most**: they predate five merges including the operator skill that instructs every session to read them. The Governor has issued no *review* since 30 Aug; refreshes lag merges by hours-to-days. OBSERVED.
7. **Recurrent design → supersede cycle without execution:** V1 bank → macro reset (1 day); T2–T8 v1 → v2 (1 day); reset v2 → Capability Lab direction (7 days, "SUPERSEDED, stated plainly"); Lab → stop-widening (6 days); Alpha-1 → three non-Alpha productions (1 day). Design artefacts persist (799 .md, 1.11 M words, 120 decision records in 22 days); execution artefacts that survive into production are few: the ledger discipline, the compositor gates, the two packs, the map cells, the CANON-010 NR vocabulary. INFERENCE from the chronology.
8. **The 28-Aug reviews' diagnoses were largely acted on** (compact memory, pilot-first, video routes, runtime thin slice) but their warning about process mass was not: prose words grew from ~612 k (28 Aug, per the head review) to 1.11 M; decision records 58 → 120; and the per-session mandated reading now includes the operator BOOTSTRAP on top of the memory files. OBSERVED counts.
9. **Evidence hygiene is genuinely strong** — sealed bytes re-hash, validators pass, spend crossings were recorded rather than annulled, negative results are kept. This is the project's most durable asset and should be preserved in any redesign. OBSERVED.
10. **Lane evidence for EVAL-037 lives on nine open PRs**, so main carries the conclusion but not the trials; the era looks like 13 commits when it was hundreds of trials. OBSERVED.

## 6. Open questions / unknowns

- **EVAL-037 total spend** — no consolidated figure exists anywhere; lane costs are partial and Gemma's price was never established. UNKNOWN beyond the ≥ USD 8.37 lower bound.
- **Did `canon.gate` actually run in the Cumin job?** Commit `42fab25` says prompts were "gated"; I did not execute or trace the job tool. INFERENCE.
- **Which text detector does `runtime/loop/frame_hygiene.py` use in real productions** (the gate's Cloud Vision adapter is "never invoked" per CONTROL-STATE; PR #98 mentions a memoised detector)? UNKNOWN.
- **Vendor-billed cost** for every era — never reconciled (C-2); all figures are ledger reservations at pinned prices.
- **Whether the Controller intends Alpha-1 to remain frozen** given that all real demand (prospecting, Upwork, Cumin) is outside it — no decision on main since 14 Sep. UNKNOWN.
- **PR #103's Canon question** (compile `commercial_communication` under C-10) — undecided.
- **Human review time / HED-1** is uncosted in every CpAO figure (PILOT-001 line, cases 001–003).
- The two prior 28-Aug reviews exist only locally (not in git); their influence on the 28-Aug decisions is INFERENCE from timing (`dd23a4a` "prioritise real product test" 28 Aug 03:12 IST precedes the reviews' stated `main = a89af60`).
