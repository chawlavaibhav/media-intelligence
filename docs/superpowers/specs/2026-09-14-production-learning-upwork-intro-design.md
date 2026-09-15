# Production learning: ingest the accepted Upwork intro pilot — design

**Date:** 2026-09-14 · **Branch:** `work/production-learning-upwork-intro-001` (from `origin/main` `3edbb78`)
**Class:** integration of a completed, human-accepted commercial showcase pilot into durable product
learning + the deterministic runtime improvements the run proved necessary. **USD 0.** No media, no
model calls, no re-edit of the accepted V4.1 (`sha256 d1a5edf8…e008a`, byte-unchanged).

## 1. What is being integrated

The pilot `pilots/upwork-intro-video-2026-09-14/` lives on the unpushed local branch
`work/pilot-upwork-intro-video-v4` (worktree `media-intelligence-worktrees/pilot-upwork-intro`). Five
assembled films exist locally: V1 `7629894`, V2 `7b39aeb`, V3 `70f687e`, V4 `11d3e59`, V4.1 `f6ca66f`
(all verified in local git; all on the same branch, merge-base with main `fcc99ce`). The Controller
accepted V4.1 in chat. The reported hashes match local git.

Two conclusions are recorded **separately and never blended**:

- **A. Final quality: SUCCESS** (V4.1 human-accepted, first real commercial showcase asset).
- **B. Pipeline efficiency / time-to-accepted-outcome: UNDERPERFORMED** (≈7–8 h human-estimated;
  mechanical corroboration: first pilot session created 15:02 IST → V4.1 file 22:55:50 IST = 7 h 54 m).

## 2. Deliverables

| # | Artifact | Purpose |
|---|---|---|
| D1 | `coordination/audits/UPWORK-INTRO-PILOT-EVIDENCE-INVENTORY-2026-09-14.md` | every expected evidence item classified FOUND / FOUND_BUT_UNTRACKED / MISSING / CHAT_ONLY_HUMAN_EVIDENCE / DUPLICATE with path + commit |
| D2 | raw pilot branch pushed to origin **unmerged**, history unrewritten (385 MB tracked, largest file 31 MB — under GitHub's 100 MB limit; no LFS in this repo) | GitHub durability of raw evidence |
| D3 | `production-learning/cases/UPWORK-INTRO-001/` — README, OUTCOME, REVISION-TRACE, TIME-AND-COST, ROUTE-OBSERVATIONS, SYSTEM-DEFECTS, HUMAN-VERDICTS, ACCEPTED-TEMPLATE, PROMOTION-QUEUE, EVIDENCE-MAP | the durable learning package (new canonical location — the repo has no existing production-learning store; `runtime/store/outcomes/` holds OUTCOME-EVENT-v1 which cannot represent this pilot, see §6) |
| D4 | `production-learning/tools/check_case.py` | validator: YAML parses, required keys present, every evidence sha256/path in EVIDENCE-MAP resolves against the pilot ref, TIME-AND-COST figures recompute from the ledgers |
| D5 | `runtime/compositor/` — `tokens.py`, `gates.py` (+ tests) | deterministic gates A–E (bounds, contrast, fit declaration, geometry tokens, disjointness), stdlib only |
| D6 | `runtime/loop/frame_hygiene.py` + `postdraw.run(frames=…)` + `run_loop(frame_sampler=…)` + synthetic frames in the dry alpha chain (+ tests, battery regenerated) | gate F: a video's text verdict comes only from sampled frames; a clean source still never transfers; no frames → NOT_RUN, never PASS |
| D7 | `runtime/execute/pools.py` (pool liquidity in `ExecutionBridge.build`) and `runtime/execute/provider_errors.py` (transient-error classification) (+ tests) | gates G and H |
| D8 | Governor update: `coordination/CONTROL-STATE.md`, `PROJECT-MEMORY.md` | state of record |
| D9 | `coordination/audits/UPWORK-INTRO-PRODUCTION-LEARNING-INTEGRATION-2026-09-14.md` | verification results |
| D10 | PR to `main`, title `Production learning: ingest accepted Upwork intro pilot and harden runtime QA`, not merged | audit |

## 3. Evidence facts established in the inventory pass (inputs to D3)

**Spend (reserved at pinned prices, every `reserved` ledger line incl. failed calls):**
V1+V2 ledger `gen/LEDGER.jsonl` 12 dispatches USD 8.082 (V1 3.76 + V2 4.32; cap INR 3,000);
V3 ledger 36 dispatches USD 3.2836 (3 Lyria failures included; cap INR 2,000 — a new lineage);
V4 ledger 6 dispatches USD 4.0276 (2 Veo UNAVAILABLE included). V4.1 USD 0.
**The reported USD 7.31 is V3+V4 only** (`known_v3_to_v4_1_provider_cost`). Verified pilot provider
cost across all lineages = **USD 15.3932** (lower bound of full CpAO numerator: excludes ~12 triage
transcript calls on Gemini credits < USD 0.10, ElevenLabs free-tier isolation, and unreconciled vendor
statements; Lyria failed calls may or may not have billed).

**Mechanical time (UTC ledgers, file mtimes, session metadata, git commit times, all consistent):**
session 1 created 09:32:14Z (15:02 IST); first plan artifact 15:39 IST; first paid call 10:40:29Z
(16:10 IST); V1 film 16:42 IST, commit 16:44; V2 film 17:20, commit 17:21; session 2 created 12:27:53Z
(17:57 IST); V3 brief-complete 18:13:59 (CLOCK.json), V3 film 18:48, commit 18:55; V4 planning files
22:09–22:13; V4 paid calls 22:12–22:24; V4 film 22:38, commit 22:40; V4.1 film 22:55:50, commit 22:56.
**Discrepancy recorded:** `v4/plan/SPEND-AMENDMENT-V4.md` self-labels "~19:40 IST" and "19:58 IST";
the ledger UTC and the file mtimes both say 22:12–22:17 IST — the document's clock labels are wrong by
≈2.5 h and are superseded by the mechanical record.

**Human-review/idle gaps that no mechanical source attributes:** V2 commit 17:21 → session 2 created
17:57 (36 min); V3 commit 18:55 → V4 planning 22:09 (3 h 14 m). Together ≈ 3 h 50 m of the 7 h 54 m.

## 4. Deterministic gates promoted (D5–D7) — engineering requirements, not model opinions

| Gate | Surface | Fail-closed behaviour |
|---|---|---|
| A text bounds | `runtime/compositor/gates.py: check_text_bounds(box, container, canvas)` | box outside canvas or container → `LayoutRefused(TEXT_OUT_OF_CANVAS / TEXT_OUT_OF_CONTAINER)` |
| B contrast | `check_contrast(text_hex, luminance_samples, role, backing=None)` | worst-case WCAG ratio below threshold and no opaque backing declared → `CONTRAST_BELOW_THRESHOLD`; opaque backing → ratio computed against the backing colour |
| C crop/fit | `check_fit(placement)` | default `contain`; `cover` without `declared_crop` (box + reason) → `UNDECLARED_COVER_CROP` |
| D tokens | `tokens.py: DesignTokens` frozen dataclass; `card_geometry(tokens)`; `check_geometry(cards, tokens)` | a wrapper card whose radius/border/shadow differ from the token set → `GEOMETRY_OFF_TOKEN` |
| E disjointness | `check_disjoint(regions)` over critical regions (offer, code, cta, legal, headline) | any overlapping pair → `CRITICAL_REGIONS_OVERLAP` |
| F frame hygiene | `runtime/loop/frame_hygiene.py: assess(source_still, frame_detections)`; wired in `runtime/loop/postdraw.run` for video modality | text in any sampled frame → FAIL regardless of the source still; no frames → NOT_RUN (verdict NOT_RUN, never PASS) |
| G pool liquidity | `runtime/execute/pools.py: PoolLiquidity`; `ExecutionBridge.build(..., pools=)` | attempt whose pool balance < expected cost → `would_dispatch False`, `blocked_by_pool True`; unknown balance → recorded `pool_liquidity: unknown`, no silent pass either way — a manifest-level `pool_liquidity` block says which pools were read |
| H transient classification | `runtime/execute/provider_errors.py: classify(...)` | gRPC 14 UNAVAILABLE / HTTP 429/500/502/503/504 / timeout → `infrastructure_transient`, `counts_against_route_quality: False`; HTTP 400 content filter → `provider_refusal`; anything else → `unclassified` (never `model_quality_failure` by default — that class is only ever assigned by a gate or a human verdict) |

All gates are pure stdlib (the runtime imports nothing beyond stdlib + yaml); pixel reading stays with
the caller (the pilot used Pillow). Tests are `unittest`, under `runtime/tests/`, offline.

## 5. What is NOT done

- No Capability Registry row created/modified (575 rows unchanged). Model observations (Veo 3.1 Fast
  accepted 1/1, Omni 1.1 Flash rejected 1/1, NB2 redraw, Kling B2 signage, Lyria prompt refusals,
  Sarvam long-read cadence) go to ROUTE-OBSERVATIONS.yaml as `directional_production_observation`,
  `routing_authority: none`.
- No Canon pack compiled or edited; accepted Canon untouched. Recorded: no new Canon source/domain was
  proven necessary — the failures were creative architecture, orchestration, compositor correctness,
  audio route choice, QA timing.
- OUTCOME-EVENT-v1 is not mutated (§6). No OUTCOME-EVENT-v2 is written; a design candidate is queued.
- TTAO is proposed, not made policy. Speaker micro-qualification is a candidate pattern.
- Alpha-1 scope is not widened; the pilot's job family (speaking presenter, multi-shot) stays excluded.

## 6. OUTCOME-EVENT-v1 mapping gap (documented, not fixed)

v1 records one job → one spec → attempts on one primary route (+ fallback) → one acceptance. The pilot is
5 assembled versions × ~25 assets × 9 routes × 3 billing pools, with assembly repairs at USD 0, a speaker
qualification that is itself a mini-acceptance, sealed-media reuse at USD 0, and execution outside the
runtime (pilot scripts, not `runtime/alpha`). Fields that cannot be represented honestly: `route`
(single), `attempts[].slot` (primary|fallback), `repairs[].incremental_cost_usd` for edit-only repairs,
`acceptance` (one decision; the pilot had five), `template_candidate` (one template from five versions).
Candidate: COMPLEX-PRODUCTION-EVENT (or OUTCOME-EVENT-v2) — queued in PROMOTION-QUEUE, condition:
a second complex real production.
