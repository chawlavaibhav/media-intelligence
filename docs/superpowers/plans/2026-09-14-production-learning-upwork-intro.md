# Production learning: Upwork intro pilot integration — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the V1→V4.1 Upwork-intro pilot into a durable production-learning case, push the raw evidence, add the deterministic runtime gates the run proved necessary, refresh the Governor, and open one auditable PR.

**Architecture:** New `production-learning/cases/<CASE>/` YAML package + `production-learning/tools/check_case.py` validator; new stdlib-only `runtime/compositor/` (tokens + gates); frame hygiene wired into `runtime/loop/postdraw.run` and `run_loop(frame_sampler=)`; pool liquidity and provider-error classification in `runtime/execute/`. Nothing touches `eval/`, the Registry, or Canon.

**Tech Stack:** Python 3 stdlib + PyYAML (the runtime's only dependency); `unittest` discovered with `python3 -m unittest discover -s runtime/tests -p 'test_*.py'`; git/gh.

## Global Constraints

- NO PAID MODEL CALLS. NO NEW MEDIA. NO RE-EDIT of V4.1 (`sha256 d1a5edf8836936eb7e27cec4350f4cce6f21f1d966778f7241544a2ad07e008a`).
- No Registry mutation (`eval/registry/` 575 rows), no Canon edit, no OUTCOME-EVENT-v1 edit, no Alpha-1 widening.
- Runtime code: stdlib + yaml only; tests offline; refusals by name (`runtime.errors.Refusal` style).
- Integration branch `work/production-learning-upwork-intro-001` from `origin/main`; the raw pilot branch `work/pilot-upwork-intro-video-v4` is pushed unrewritten and never merged.
- Never run two harness suites concurrently (8 GB Mac).
- Commit after each task; do not merge the PR.

---

### Task 1: Evidence inventory + raw branch durability

**Files:** Create `coordination/audits/UPWORK-INTRO-PILOT-EVIDENCE-INVENTORY-2026-09-14.md`.

- [ ] Step 1: From the pilot worktree, list tracked files (`git ls-files pilots`), ignored/untracked files (`git status --ignored --short`), commit hashes with times (`git log --format='%h %ci %s'`), sha256 of the five films, ledger totals per version.
- [ ] Step 2: Write the inventory table (item · class · path · commit/sha). Classes: FOUND / FOUND_BUT_UNTRACKED / MISSING / CHAT_ONLY_HUMAN_EVIDENCE / DUPLICATE. Human verdicts V1–V4.1 are CHAT_ONLY_HUMAN_EVIDENCE (the pilot learning docs say "awaiting Controller judgment").
- [ ] Step 3: `git push -u origin work/pilot-upwork-intro-video-v4` from the pilot worktree. If refused for size/policy: stop, record the blocking files, push manifests/hashes/reports on `archive/upwork-intro-pilot-evidence-2026-09-14` instead.
- [ ] Step 4: Verify `git ls-remote origin work/pilot-upwork-intro-video-v4` = `f6ca66f…`; record in the inventory.
- [ ] Step 5: Commit the inventory on the integration branch.

### Task 2: Production-learning package + revision trace

**Files:** Create `production-learning/README.md`, `production-learning/cases/UPWORK-INTRO-001/{README.md,OUTCOME.yaml,REVISION-TRACE.yaml,HUMAN-VERDICTS.yaml,SYSTEM-DEFECTS.yaml,ROUTE-OBSERVATIONS.yaml,EVIDENCE-MAP.md}`, `production-learning/tools/check_case.py`, test `runtime/tests/test_i_production_learning_case.py`.

**Interfaces:** `check_case.py --case production-learning/cases/UPWORK-INTRO-001 [--pilot-ref work/pilot-upwork-intro-video-v4]` exits 0 on PASS; `run(case_dir, pilot_ref=None) -> list[str]` returns problems.

- [ ] Step 1: Write the failing test: `check_case.run(CASE)` returns `[]`; a copy with `OUTCOME.yaml` `final_outcome: accepted` but no `final_asset.sha256` returns a problem naming the key.
- [ ] Step 2: Run → fails (module missing).
- [ ] Step 3: Write the YAML files from the inventory facts (spec §3) and the Controller's verdict text (spec §1, prompt §2). REVISION-TRACE root-cause classes limited to the eleven listed in the prompt.
- [ ] Step 4: Write `check_case.py`: parse YAML, required keys, root-cause vocabulary, evidence sha256 lines in EVIDENCE-MAP resolvable via `git cat-file -e <ref>:<path>` when `--pilot-ref` is given and the ref exists locally (skip with a note otherwise).
- [ ] Step 5: Run test → PASS. Commit.

### Task 3: TTAO + cost reconciliation

**Files:** Create `production-learning/cases/UPWORK-INTRO-001/TIME-AND-COST.yaml`, `production-learning/tools/reconcile_pilot_ledgers.py`; extend `check_case.py` to cross-check the YAML's cost totals against the ledgers when the pilot ref is available; test `runtime/tests/test_i_production_learning_case.py::CostReconciliation`.

- [ ] Step 1: Failing test: `reconcile_pilot_ledgers.totals(ledger_lines)` on three inline sample ledgers returns `{"reserved_usd": Decimal(...), "dispatches": n, "failed": k}` (exact figures from spec §3 are asserted against the real pilot ref only when present).
- [ ] Step 2: Implement `totals()` (sum `est_usd` over `status == "reserved"`; count non-ok statuses).
- [ ] Step 3: Write TIME-AND-COST.yaml with mechanical vs human-estimated sections, `null` + `reason` where unprovable, the two conclusions, and the TTAO Controller decision candidate.
- [ ] Step 4: Tests pass. Commit.

### Task 4: Compositor deterministic gates (A–E)

**Files:** Create `runtime/compositor/__init__.py`, `runtime/compositor/tokens.py`, `runtime/compositor/gates.py`; test `runtime/tests/test_i_compositor_gates.py`.

**Interfaces:**
```python
class LayoutRefused(Refusal)  # codes: TEXT_OUT_OF_CANVAS, TEXT_OUT_OF_CONTAINER, CONTRAST_BELOW_THRESHOLD,
                              # UNDECLARED_COVER_CROP, GEOMETRY_OFF_TOKEN, CRITICAL_REGIONS_OVERLAP, TOKEN_SOURCE_MISSING
Box = tuple[int,int,int,int]  # x0,y0,x1,y1 (x1,y1 exclusive)
check_text_bounds(box, container=None, canvas) -> dict
check_contrast(text_hex, luminance_samples, role="body", backing_hex=None, thresholds=DEFAULT) -> dict
check_fit(placement: dict) -> dict   # {"fit": "contain"|"native"|"cover", "declared_crop": {...}?}
check_geometry(cards: list[dict], tokens: DesignTokens) -> dict
check_disjoint(regions: dict[str, Box], critical=CRITICAL_REGIONS) -> dict
DesignTokens (frozen dataclass): card_radius, card_border_px, card_shadow, safe_x, safe_y, spacing, contrast_body=4.5, contrast_display=3.0, display_threshold_px=48
```
- [ ] Step 1: Failing tests (one per prompt §11 class): canvas overflow refused; container overflow refused; low contrast refused; same text with opaque backing passes; undeclared cover refused; declared cover passes; off-token radius refused; offer/CTA collision refused; disjoint regions pass.
- [ ] Step 2: Run → ImportError.
- [ ] Step 3: Implement tokens.py (DesignTokens + `from_mapping`) and gates.py (pure functions; WCAG relative luminance from hex; contrast against min/max sample luminance).
- [ ] Step 4: Tests pass. Commit.

### Task 5: Video-frame text hygiene (F)

**Files:** Create `runtime/loop/frame_hygiene.py`; modify `runtime/loop/postdraw.py` (`run(..., frames=None, source_still_scan=None)` adds the runtime row and forces NOT_RUN for video without frames), `runtime/loop/driver.py` (`run_loop(..., frame_sampler=None)`), `runtime/loop/synthetic.py` (`frames_for_spec`), `runtime/alpha/run.py` (`_post_draw_fixture` returns a frame sampler; scripted detector covers frame digests); tests `runtime/tests/test_i_frame_hygiene.py`; regenerate `runtime/battery/results/2026-09-14/` with `python3 -m runtime.alpha.battery`.

**Interfaces:** `frame_hygiene.assess(frame_detections: list[Detection], *, source_still_clean: bool|None, modality) -> dict` (a runtime row `RUNTIME-VIDEO-FRAME-TEXT`; status FAIL/PASS/NOT-RUN); `frame_sampler(attempt, artifact_bytes) -> list[bytes] | None`.

- [ ] Step 1: Failing tests: text in a sampled frame → row FAIL blocking; clean still + tainted frames → FAIL; no frames on video → postdraw verdict NOT_RUN (not PASS); driver with `frame_sampler` and scripted detector: still no_text, frame text → attempt `gate_post_verdict == "FAIL"`.
- [ ] Step 2: Run → fails.
- [ ] Step 3: Implement; wire; add synthetic frames to the alpha dry chain.
- [ ] Step 4: Tests pass; `python3 -m runtime.alpha.battery` → 14 runs, same final states as committed SUMMARY.yaml (B05 stays accepted with 3 synthetic frames scanned). Commit code + regenerated results.

### Task 6: Provider-pool liquidity (G) + transient error classification (H)

**Files:** Create `runtime/execute/pools.py`, `runtime/execute/provider_errors.py`; modify `runtime/execute/bridge.py` (`build(..., pools: PoolLiquidity|None=None)`; attempt fields `pool_liquidity`, `blocked_by_pool`; manifest `pool_liquidity` block); tests `runtime/tests/test_i_pools_and_errors.py`.

**Interfaces:**
```python
PoolLiquidity.from_readings([{"pool": "fal_cash", "balance_usd": "0.26", "read_utc": "...", "source": "..."}])
PoolLiquidity.can_fund(pool, amount) -> (bool|None, reason)   # None = unknown
classify(*, http_status=None, grpc_code=None, message="", timed_out=False) -> ProviderErrorClass
ProviderErrorClass: {"failure_class": "infrastructure_transient"|"provider_refusal"|"unclassified", "counts_against_route_quality": False, "retry_eligible": bool, "basis": str}
failure_record(attempt, error_class) -> attempt-record dict fragment for OUTCOME-EVENT-v1 (`status: provider_error`, extra `failure_class` kept out of the frozen contract's field set — recorded in the loop result, not the event)
```
- [ ] Step 1: Failing tests: profile ceiling permits but pool balance 0.26 < expected → `would_dispatch False`, `blocked_by_pool True`, reason names the pool; unknown pool → not blocked, `pool_liquidity.status == "unknown"`; gRPC 14 → `infrastructure_transient`, never `model_quality_failure`; HTTP 503 → transient; HTTP 400 content filter → `provider_refusal`.
- [ ] Step 2: Run → fails.
- [ ] Step 3: Implement.
- [ ] Step 4: Tests pass; full `runtime/tests` suite green. Commit.

### Task 7: Accepted template + promotion queue

**Files:** Create `production-learning/cases/UPWORK-INTRO-001/ACCEPTED-TEMPLATE.yaml`, `PROMOTION-QUEUE.yaml`; extend `check_case.py` required files + `evidence_scope: this_accepted_template` on every pacing value.

- [ ] Step 1: Failing test: check_case flags a template pacing value without `evidence_scope`.
- [ ] Step 2: Write both YAMLs (ten-beat structure; pacing observations from `v4/assembly/v4.1/timeline.json`; queue sections PROMOTED NOW / CANDIDATE PATTERNS / DIRECTIONAL ONLY / NOT PROMOTED).
- [ ] Step 3: Tests pass. Commit.

### Task 8: Governor update + verification

**Files:** Modify `coordination/CONTROL-STATE.md`, `PROJECT-MEMORY.md`; create `coordination/audits/UPWORK-INTRO-PRODUCTION-LEARNING-INTEGRATION-2026-09-14.md`.

- [ ] Step 1: Add the "first human-accepted real commercial showcase asset" section (prompt §19 bullets) to CONTROL-STATE §1/§5/§6 and PROJECT-MEMORY §5/§6; state plainly it does not prove commercial advantage.
- [ ] Step 2: Run: runtime suite; canon gate tests; `eval/registry/validate_registry.py`; `verify_sealed_evidence.py --against origin/main`; `build_taint_register.py --check`; `check_case.py`; `runtime.alpha.battery`; V4.1 sha256 on the pushed ref; `git diff --stat origin/main -- eval/registry canon` empty; secret scan (`grep -rE "sk-|AIza|fal_|key" ` over the diff), `authorization.local.yaml` absent.
- [ ] Step 3: Write the audit doc with exact outputs. Commit.

### Task 9: Push + PR

- [ ] Step 1: `git push -u origin work/production-learning-upwork-intro-001`.
- [ ] Step 2: `gh pr create --base main --title "Production learning: ingest accepted Upwork intro pilot and harden runtime QA"` with the four-section body (OBSERVED FACT / HUMAN JUDGMENT / DIRECTIONAL MODEL LEARNING / PROMOTED DETERMINISTIC SYSTEM CHANGE). Do not merge.
