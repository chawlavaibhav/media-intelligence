# EVAL-039A — Tester report (Stage A test-case package)

**Role:** Tester (five-role pipeline). **Date:** 2026-09-05. **Tested commit:** `97b237f` (Executor output) in worktree `media-intelligence-wt-controller`; the package on disk is byte-identical to that commit. **Spend:** USD 0 — no provider, evaluator, OCR or LLM call; no network. No file edited; no sub-agent. Checker script kept in the session scratchpad (`check039a.py`); commands below are what it ran, outputs trimmed. Sibling EVAL-039B's pipeline was live in the same worktree during testing (HEAD moved to `3201b1b`; 9 of its files modified, uncommitted) — see O1/O8.

## Checklist F.1–F.9 and Controller additions A–G

| id | command (trimmed) | result | verdict |
|---|---|---|---|
| F.1 | `python3 -c 'import yaml,sys; yaml.safe_load(open(f))'` × TEST-CASES / SEED-POLICY / EVALUATOR-PLAN / COST-TABLE | all 4 parse (pyyaml 6.0.3) | PASS |
| F.2 | script: ids vs §B.1; §A.1 fields; `BLUEPRINTS/` + `test-cases/` exist; `sha256(file) == blueprint_sha256` | 35 ids, unique, set == §B.1; every §A.1 field present on 35/35 (`cut_order_rank` is null on 28 — DEFECT-1); 35 blueprints + 35 twins exist; 35/35 sha256 match; twins carry the request verbatim, source id, "real demand" paragraph | PASS |
| F.3 | script over `nr`, `capabilities`, `conditions` | ops = generate 24 / edit 2 / animate 4 / extend 1 / compose 4 (all in the seven); 0 forbidden route values (`inpaint … segment_and_composite`) in any NR field; 35 primaries ∈ 43 active contract ids, `repairability` never primary; 13 families on 35/35; `who_chose_workflow_mode: benchmark_fixed` on 35/35; repeats = 2 on every route | PASS |
| F.4.1 | parse COVERAGE-MATRIX §1 | 17 rows (16 plan §C.1 rows + VID-04); every row names a case or `deferred_no_account`; the load-sweep row says "Stage B sweeps" (O4) | PASS |
| F.4.2 | grep | VID-MS-01 15 s; VID-2SPK-01 native + chain; MUS-01/02 × 2 routes × 2; 4K sentence verbatim in README and matrix | PASS |
| F.4.3 | script from YAML `language` | image 4 / t2v 4 / i2v 4 / TTS 3 / lipsync 3; each core ≥ 1 hi/hg; policy-edge IMG-CORE-04 / VID-T2V-03 / VID-I2V-04, TTS+lipsync waived and stated; high-motion VID-T2V-02 / VID-I2V-03 | PASS |
| F.4.4 | matrix §5 | TOPO-02 (both text cases) and TOPO-03 list arms A/B/C with routes and counts | PASS |
| F.4.5 | matrix §6 | freshness 1→VID-I2V-04/VID-T2V-03, 2→every Seedance line, 3→VID-TOPO3-01, 4→VID-2SPK-01, 5→AUD-LIP-* | PASS |
| F.4.6 | YAML ops vs matrix §7 | generate/edit/animate/extend/compose covered; `restore`, `variants` absent with stated reasons | PASS |
| F.4.7 | script | en 15 / hi 12 / hg 8; by lane IMG 5/4/3, VID 7/5/3, AUD 2/2/2, MUS 1/1/0 = counts block; hi+hg 20/35 = 57 % ≥ 40 % | PASS |
| F.4.8 | word-bounded grep of 35 `customer_request.text` for `probe|capability|benchmark|isolated|level 1|condition` | 0 hits | PASS |
| F.5 | script over COST-TABLE `rows` (165) + `route_catalogue` (47) | every row has `billing_pool` + `price_status`; every catalogue `route_id` carries a `plan_ref` to §C.3/§C.3c/§C.3d and the 6 conditionals are flagged; surfaces agree with survey §6 (ElevenLabs v3 on fal per plan §C.3 — O7); row sums 1a 186 / 1b 112 / total 298 / conditional 32; totals block == row sums per tranche × pool | PASS |
| F.6 | script vs the four pools | 29 real sources (MKT-009/012/014; BR-F01…F10; RX-01/02/05/06/07/08; B0n unused) + 6 fixtures; 0 mentions of MKT-015 / MKT-016 / RX-11 anywhere in records | PASS |
| F.7 | script: PA/CA ids in 70 blueprint + twin files vs the two packs; `**DEFAULT (<pack>)**` quotes | 0 unknown ids (packs hold PA-D1..10, CA-D1..11 + `-check`); DEFAULT text quoted only from the two compiled packs; audio cells carry the trigger file's `coverage_gap_notice` verbatim and no `*-check` line (AUD-TTS-*, MUS-*) | PASS |
| F.8 | 5 plan §C.4 `- E1…E5 — ` lines byte-searched in ELIMINATION-RULES.md | 5/5 present byte-identical; survivor cap "at most 3"; Seedance proportional rule stated | PASS |
| F.9 | `git diff --name-status 97b237f~1 97b237f` | 80 lines, all `A`, all under `STAGE-A-FREEZE-2026-09/` + the Executor report; no M/D; `git status --porcelain -- <039A paths>` = 0 (O8 for the sibling's files) | PASS |
| A | `grep -rwiE '(desai|airey|freeman-beyond|samara-ch2|ries)'` blueprints + test-cases; unknown-id script | 0 hits in the 70 files; 0 unknown `PA-D`/`CA-D`/`*-check` ids. Whole-package scan: 1 hit, README.md:109 — the word `ries` named as the grep token itself (O3) | PASS |
| B | script | `routes[]` carry no per-route blueprint field; each case has one `blueprint_ref` = `BLUEPRINTS/<id>.blueprint.md`; header `case_id`, `held_constant_across_routes: true`, `author: executor_agent` in 35/35; sha256 35/35 | PASS |
| C | script: catalogue `unit_price` vs roster `regular_price` via `roster_route_key` (record / variant / fallback) | roster at `97b237f` and at HEAD: 0 mismatches > 0.0001 on 41 pinned lines; 6 unpinned lines carry no price. In-cap totals 186 / 112 / 298, conditional 32; unpinned 14 calls (gpt-image-2-edit 12, veo-3.1-lite-i2v 2) have `line_usd: null`, `counted_in_cap: false`, in-cap sum 162.46 = `nominal_usd_in_cap`. **Working-tree roster (uncommitted 039B edit): `sync-lipsync-v3` now `unpinned`, price null → 1 mismatch (O1)** | PASS |
| D | word-bounded grep for the B.2 list + `capability|route|model|arm|Canon|pack|condition family|repeat` | 7 hits, all customer-sense: "model" = the person in the photo (IMG-COMP-01 ×3, AUD-LIP-01), "pack" = the product pack (IMG-COMP-01, VID-REF-01 ×2). 0 hits on the other tells | PASS |
| E | script | hi+hg = 20/35 = 57 %; Devanagari present in 12/12 `language: hi` texts; 3 hg texts also contain Devanagari strings (IMG-COMP-01, AUD-TTS-02, AUD-LIP-02 — product/script strings, as typed) | PASS |
| F | `git status --porcelain`; `git diff --name-status HEAD~1` | at start: clean, HEAD = 97b237f, diff = 80 `A`. During testing HEAD became `3201b1b` (039B Auditor report) and 8 M + 1 ?? appeared, all 039B files; 039A paths untouched | PASS |
| G | rebuilt from the scratchpad generator (`gen039a/build.py`, OUT and ROSTER_PATH patched to scratch copies; roster = `97b237f` version) then `diff -rq` | 79 files, byte-identical to the committed package; the build asserts (fail-closed) against the live working-tree roster because of O1. Generator not committed — note, not a FAIL | NOTE |

## Defects

1. **DEFECT-1 (minor, consistency).** `TEST-CASES.yaml` `cut_order_rank` is `null` on 28 of 35 cases (e.g. lines 272, 2466, 2673, 2866, 3056 = VID-T2V-01..04; 3684, 3847, 4025, 4204 = VID-I2V-01..04) although `IRREDUCIBILITY.md:160` states the rank "names the case whose line the numbered cut removes" for items 1, 2, 3, 5, 6, 9, 10 — items 3, 6, 10 (Wan / Seedance on VID-I2V-*, Wan on VID-T2V-*) therefore have no case carrying their rank, and VID-REF-02 (line 4684) carries 2 but is also item 5. §A.1 asks for an integer rank on every case. Fix is a field-value pass in one file (plus, if the Executor prefers, an explicit `never_cut` marker for the 28); counts and blueprints unaffected.

## Observations (not defects; for the Auditor / Approver)

- **O1 Roster drift, live.** EVAL-039B's uncommitted working-tree edit un-pins `sync-lipsync-v3` (0.1333/s → null; commit `3201b1b` AF-1). If it lands as-is, 4 COST-TABLE rows / 8 calls / USD 6.93 (AUD-LIP-01/02/03, VID-2SPK-01 chain) move from in-cap to `unpinned_calls_excluded_from_cap` (14 → 22) and `nominal_usd_in_cap` falls to ≈ 155.53. README OQ-17 already prescribes regenerating rather than hand-editing; the spend record must name which roster version it prices against.
- **O2** `route_catalogue` marks `gpt-image-2` and `flux-2-pro` `route_status: unpinned` while `price_status: pinned` (fal fallback, which the roster records as `pinned`); the intended reading (credit surface unpinned, cash fallback priced) is stated in the `note` field but the two status fields read against each other.
- **O3** README.md:109 contains the bare token `ries` while explaining the grep — not a HOLD citation.
- **O4** COVERAGE-MATRIX.md:24 (load-sweep row) lists no Stage A case; plan §C.1 assigns that row to Stage B and the row says so.
- **O5** IMG-CORE-03's contract uses "premium" but ties it to an observable (a named list of luxury props to reject); Auditor's call under §A.3.
- **O6** `reference_assets[]` on VID-I2V-*/AUD-LIP-* carry `status: specified (bytes exist only after 1a/1b acceptance)` — a qualified `specified`, consistent with §A.1.
- **O7** ElevenLabs v3 surface is `fal` (plan §C.3, §C.3c, task §B.1) where survey §6 says "direct"; the plan governs.
- **O8** The 9 working-tree changes seen at the end of testing are all EVAL-039B files (ACCESS-LOG, COST-PROJECTION-*, MORNING-DECISIONS, ROSTER-REFRESH, PIN-INDEX, project_costs.py, af1-sync-lipsync-v3-refetch.json); none under the 039A deliverable or its report.

## Overall verdict

**FAIL (1 defect — minor: `cut_order_rank` inconsistent with IRREDUCIBILITY.md; every mechanical check F.1–F.9 and additions A–G otherwise PASS; package rebuilds byte-identical from the generator.)**
