# EVAL-039A — Executor report (Stage A test-case package)

**Role:** Executor (five-role pipeline). **Date:** 2026-09-05. **Base:** `cb92f1e` on `controller/capability-lab-direction-2026-09-05`, worktree `media-intelligence-wt-controller`. **Spend:** USD 0 — no provider, evaluator, OCR or LLM API call; no network. **Commits:** none (the Controller session commits). Nothing outside `eval/empirical-planning/STAGE-A-FREEZE-2026-09/` and this report was written.

## What was produced (OBSERVED)

`eval/empirical-planning/STAGE-A-FREEZE-2026-09/`: `README.md`, `TEST-CASES.yaml`, `test-cases/<35>.md`, `BLUEPRINTS/<35>.blueprint.md`, `COVERAGE-MATRIX.md`, `ACCEPTANCE-CONTRACTS.md`, `ELIMINATION-RULES.md`, `SEED-POLICY.yaml`, `EVALUATOR-PLAN.yaml`, `COST-TABLE.yaml`, `IRREDUCIBILITY.md` — 79 files, 1021 KB of actual bytes (≤ 1 MB budget; `du -sk` reports 1200 KB because of 4 KB block rounding over 79 small files).

- Cases **35**, blueprints **35** (author `executor_agent`, sha256 recorded per case and verified; `gate_pre: not_available_on_base` — `canon/gate/` is absent from the base).
- Calls **1a = 186**, **1b = 112**, **total = 298**, **conditional = 32** — equal to the task's fixed counts; no deviation.
- Language mix: en 15 / hi 12 / hg 8 (Hindi + Hinglish 20/35 = 57 %); per lane IMG 5/4/3, VID 7/5/3, AUD 2/2/2, MUS 1/1/0.
- Fixtures **6**: IMG-CORE-04, VID-T2V-03, VID-I2V-04 (the Media Factory Veo-refusal shape as still / text-to-video / animate — no pool holds it) and AUD-LIP-01/02/03 (no pool item supplies a clip plus a voice file to lip-sync; each consumes two real-demand items). Every other case cites a real pool id with every adaptation listed.
- Operation coverage: generate, edit, animate, extend, compose; `restore` and `variants` omitted with stated reasons (COVERAGE-MATRIX §7).

## Cost table (pinned by route key from EVAL-039B's roster; OBSERVED from `COST-TABLE.yaml`)

| tranche | pool | calls | priced | unpinned | nominal USD |
|---|---|---|---|---|---|
| 1a | cash | 136 | 124 | 12 | 47.59 |
| 1a | credits | 50 | 50 | 0 | 25.5 |
| 1b | cash | 78 | 78 | 0 | 73.85 |
| 1b | credits | 24 | 22 | 2 | 15.51 |
| 1b | sarvam_credits | 10 | 10 | 0 | 0.01 |

Conditional (listed, outside the cap):

| tranche | pool | calls | priced | unpinned | nominal USD |
|---|---|---|---|---|---|
| 1a | credits | 24 | 16 | 8 | 5.44 |
| 1b | cash | 4 | 0 | 4 | 0.0 |
| 1b | credits | 4 | 2 | 2 | 0.0 |

- In-cap nominal **USD 162.46** (1a 73.09, 1b 89.37); cash 121.44, GCP credits 41.01, Sarvam ₹0.92. Unpinned and excluded: 14 calls (gpt-image-2-edit, veo-3.1-lite-i2v). Conditional nominal 5.44. Evaluators ≈ USD 3.82 (Cloud Vision + VLM triage; ASR unpinned).

| evaluator row | calls | nominal USD | minutes |
|---|---|---|---|
| cloud-vision-text-detection | 562 | 0.84 |  |
| asr-vs-script | 56 | None |  |
| vlm-triage | 298 | 2.98 |  |
| controller_blind_judging | 302 | None | 101 |

- The roster was absent at first orientation and present (02:21 IST) when the package was built; every priced line names its roster record/variant and `COST-TABLE.yaml → roster_cross_check` was asserted against the roster at build time. The roster's Tester correction of the Sarvam key (DEFECT-1, commit `a24b197`) was read from the working tree and applied: Sarvam is `pinned` and inside the cap.
- INFERRED: the 1a nominal (≈ 73) exceeds the plan's ≈ 60 line — morning decision 8.

## Open questions (all recorded in `README.md`, none asked)

Morning decisions 1–11 from the task with the state assumed (2 = Sarvam confirmed present after the sibling's correction; 3/4/5/10 unchanged), plus OQ-1…OQ-17: Veo Fast ref2v tier (pinned, used); Kling/H3/Wan native audio on speech items; Veo Lite image-input unpinned (arm A keeps it, 2 calls outside the cap; arm C and the 2SPK chain use H3 Max i2v-768p, the cheapest pinned i2v); second lipsync route = Kling lipsync (pinned); VID-2SPK-01 at 8 s; arm-C base route FLUX.2 Pro on fal; the AUD-TTS-02 brand-name fixture; one lipsync plate held constant; music count 8 vs MD-7's 4; Cloud Vision billing pool; Omni Flash ≤ 15-s ceiling; VID-REF-01 read as generate-with-references; the image core's fourth slot; `nano-banana-pro/edit` on fal per the roster vs Vertex credits; gpt-image-2 quality=medium; the HOLD-id grep needs word boundaries (the packs' own verbatim text contains "carries"; the grammar field `mandatories`); the roster may change again before the spend record.

## Contradictions met (beyond the Planner's ten, which were applied as resolved)

Eight, listed in `README.md` §Contradictions: multi-arm cases vs "one prompt per case" (arm variants inside one blueprint; identical within an arm); `text_handling` for edit cases that preserve supplied lettering; `product_appearance` not triggered on person-only / illustration cases (light stated brief-only, not Canon); the pack limit against generating Devanagari vs TOPO-02/03 arms A/B (the experiment the Controller asked for; arm C is the compliant arm); "TTS 20 incl. 2SPK drives" → four line-specific TTS entries; Veo fast + extend = one trial, two API calls; BR-F02-HI's strings become referenced-tin identity in IMG-REF-01; marketplace buyers localised to India.

## Self-check (Tester checklist F.1–F.9 run on my own output — not the Tester's verdict)

F.1 parse PASS · F.2 35 ids / all fields / twins / sha256 PASS · F.3 operations, forbidden route values, primary ids, 13 families PASS · F.4 coverage B.2 1–8 incl. vocabulary grep PASS · F.5 totals 186/112/298 + 32, pools, surfaces PASS · F.6 source ids (no MKT-015/016/RX-11) PASS · F.7 decision ids ⊆ PA-D1..10 ∪ CA-D1..11, HOLD ids word-scan PASS (substring `ries` hits only the pack's own "carries" and "Stories") · F.8 E1–E5 byte-identical + survivor cap PASS · F.9 `git status`: my writes are only `STAGE-A-FREEZE-2026-09/` and this report; the sibling EVAL-039B's files show as modified in the working tree by its own pipeline, not by me. Defects found and fixed during the self-check: a no-in-image-text check line on audio blueprints; an unbounded HOLD substring grep; the storage budget (formatting overhead, trimmed).

## Stop conditions

None hit. `validate_compiled_pack.py` PASS on both packs before authoring. No case was `blocked`.

## Reproducibility

The package was emitted by a generator kept in the session scratchpad (`gen039a/`: `routes.py`, `common.py`, `cases_img.py`, `cases_vid.py`, `cases_aud.py`, `build.py`, `readme.py`), deliberately not committed so `git status` stays confined to the deliverable; the Controller may ask for it to be added under `eval/empirical-planning/STAGE-A-FREEZE-2026-09/tools/` as a separate task.

## Corrections after Tester (2026-09-05, USD 0, no network, no commits)

Tester report: `eval/tasks/EVAL-039A-TESTER-REPORT.md` — FAIL on DEFECT-1, risk O1, observations O2/O3, reproducibility note G. Files changed: `TEST-CASES.yaml`, `COST-TABLE.yaml`, `EVALUATOR-PLAN.yaml`, `IRREDUCIBILITY.md`, `README.md`, new `tools/` (generator + README). Blueprints and case twins are byte-unchanged, so every recorded sha256 still holds.

1. **DEFECT-1 fixed.** Every case carries `cut_order_rank`: an integer = the lowest-numbered cut item that touches it, with `cut_order_items[]` naming each item and its scope (route line / arm / whole case) — VID-MS-01 → 1; VID-REF-01 → 2; VID-REF-02 → 2 (items 2, 5); VID-I2V-01..04 → 3 (02/03 also item 6); VID-MS-02 → 4; VID-2SPK-01 → 7; MUS-02 → 8; VID-KNEE-01 → 9; VID-T2V-01..04 → 10 — or `never_cut` with `never_cut_reason` (core item / Hindi-Hinglish item / TOPO-02/03 arms A and C) on the other 20; the rule is stated once as `cut_order_rule` and `IRREDUCIBILITY.md` lists item → cases.
2. **O1 applied.** Repriced against the roster as committed: `eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml` sha256 `99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46`, last changed in `3434b37`, branch HEAD at build `f6b743b`, working tree = HEAD — recorded in `COST-TABLE.yaml → priced_against_roster`. `sync-lipsync-v3` is now `unpinned` (its exact endpoint carries no price; the 0.1333/s string belongs to the sibling image-to-video endpoint): its 12 calls (AUD-LIP-01/02/03 × 2 and the VID-2SPK-01 chain × 2 — the Tester's estimate of 8 counted only the three AUD cases) moved to `unpinned_calls_excluded_from_cap` (14 → 22). `flux-2-pro-edit` is priced 0.045 = pinned base 0.03 + pinned 0.015 addon for one 1-MP reference, declared as `roster_base_price` / `addon` so the build-time cross-check compares the base.
3. **Restated totals (OBSERVED from the rebuilt `COST-TABLE.yaml`):** in-cap nominal **USD 155.71** (1a 73.27, 1b 82.44); cash 114.69, GCP credits 41.01, Sarvam ₹0.92; calls unchanged 186 / 112 / 298 + 32.

| tranche | pool | calls | priced | unpinned | nominal USD |
|---|---|---|---|---|---|
| 1a | cash | 136 | 124 | 12 | 47.77 |
| 1a | credits | 50 | 50 | 0 | 25.5 |
| 1b | cash | 78 | 70 | 8 | 66.92 |
| 1b | credits | 24 | 22 | 2 | 15.51 |
| 1b | sarvam_credits | 10 | 10 | 0 | 0.01 |

4. **O2 reconciled.** `gpt-image-2` and `flux-2-pro` are `route_status: pinned` on their fal fallback records (the roster's `fallback.route_status: pinned`); `route_catalogue.priced_surface` states that the priced surface is fal and that the Azure credit surfaces remain `needs_controller_enablement`.
5. **O3 fixed.** README OQ-16 describes the fifth HOLD-lane id without printing the bare token, so a word-bounded scan of every .md/.yaml in the package is clean.
6. **Reproducibility.** The generator is committed under `tools/` (`build.py`, `routes.py`, `common.py`, `cases_*.py`, `readme.py`, `README.md`); it resolves the repo root from its own location and rebuilds the package deterministically from committed inputs. The Tester reproduced 79/79 files byte-identical before these changes; after them, a rebuild from `tools/` changed exactly the files listed above (`git diff --name-only`), blueprints and twins byte-identical to the committed package; `__pycache__` is removed after each build and is not part of the deliverable.
7. **Self-check re-run:** F.1–F.9, the DEFECT-1 rank check, `priced_against_roster` sha256 = `shasum -a 256` of the roster, in-cap sum = row sum with no sync-lipsync row counted, whole-package word-bounded HOLD scan over every .md/.yaml, storage (package files 1023 KB ≤ 1 MB; `tools/` adds 376 KB) — all PASS. Not the Tester's verdict.
