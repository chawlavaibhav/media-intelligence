# EVAL-039C — Executor report: harness adapters, deterministic instruments, Q1 geometry run

**Role:** Executor. **Branch / worktree:** `controller/capability-lab-direction-2026-09-05` in `media-intelligence-wt-controller`, base HEAD `c60d224` (nothing committed by the Executor). **Spend:** USD 0 / ₹0 — no provider call of any kind, no authenticated call, no queue submit, no token exchange. **Stop conditions hit:** none. **Status:** deliverables complete; 16 morning decisions listed (MD-C1…MD-C16); one honest negative finding (Q1 `object_count` disqualified on the overlap fixtures).

Conventions: **OBSERVED** = produced by a command or file on this checkout; **INFERRED** = the Executor's reading. Plain English first, detail after.

## 1. What was built (OBSERVED)

A previous, interrupted attempt had already written `surfaces.py`, `pricing.py`, `ledger.py`, `transports.py`, `store.py`, `casebook.py`, `dry_run.py`, the six adapters, the pinned schemas and six test files, but its suite was red (43 errors) and it stopped before instruments, Q1, the manifest and the report. This run kept that code, fixed it, and finished the tree.

`eval/harness-v2/` (7,394 lines of Python, stdlib + PyYAML only): `hv2_paths.py`, `surfaces.py` (47 keys = the COST-TABLE route catalogue, set equality tested), `pricing.py`, `ledger.py`, `store.py`, `transports.py`, `casebook.py`, `dry_run.py`, `battery_harness.py`, `adapters/{base,fal_queue,vertex_veo,vertex_gemini_image,vertex_omni,vertex_lyria,sarvam_tts}.py`, `instruments/{imageio,common,metrics,format_probe,masked_diff,brand_colour,av_offset,repeat_consistency,ledger_metrics,gate_wrapper,registry_gate}.py`, `instruments/PASS-CRITERIA-v0.yaml`, `q1/{detector,run_q1,check_record}.py`, `schemas/` (768 KB pinned: 24 fal OpenAPI JSONs + 10 gzipped vendor pages with sha256), `tests/test_*.py` (10 files) + `tests/RESULTS-2026-09.txt`, `DRY-RUN-MANIFEST-2026-09.yaml`, `README.md`, `ENVIRONMENT-2026-09.yaml`, `authorization.example.yaml`. Plus the three Q1 records under `eval/v1/instruments/qualification-records/` and one `.gitignore` line (§6).

Fixes made to the inherited code (each caught by a test): `hv2_paths` inserted paths in the wrong order so `import adapters` resolved to the frozen v1 module; `route_catalogue` moved to COST-TABLE at commit 0596aa2 (pointer string in TEST-CASES) — `casebook` now reads it there; `repeats: 0` rows (the VID-2SPK-01 chain, 8 rows) were counted as 1 call each (`0 or 1`); string constants in `ROUTE_PINS` (`"medium"`, `"720p"`, …) were parsed as resolver names — now explicit `Const()`; the Veo extend follow-up carried a caller-input placeholder so live dispatch refused it; the omni-long registry variant did not match the catalogue; pricing conflated price status with route status and quoted a token-metered price as projectable; Sarvam had no mapping for the literal `'hi-en (Hinglish)'`.

## 2. Tests (OBSERVED)

`python3 -m unittest discover -s eval/harness-v2/tests -v` → **Ran 123 tests, OK, 0 skipped** (captured in `eval/harness-v2/tests/RESULTS-2026-09.txt`). ffmpeg/ffprobe 8.1.2 were present, so no ffmpeg test was skipped. Every test runs under `NoNetworkTestCase`: `socket.socket.connect`, `socket.create_connection` and `urllib.request.urlopen` raise, every provider key name is stripped from the environment, and the key loader is pointed at a throw-away file (`test_live_call_would_hit_the_guard` proves the guard is real). Task §5 cases (a)–(n) map to: (a) `ConstructionTest`, (b) `KeyLeakTest` (canary via env and via a fake key file; never on disk, never in an attempt or exception), (c) `OrderingTest` (reservation open and `request.json` on disk at every send), (d)/(e) `PriceAndCapTest`, (f) `FailureModesTest` (timeout, provider error, content-policy refusal, poll exhaustion, poll failure, download failure, Veo operation error and safety filter — each one submit, one attempt, one conservative settlement, no release, no resubmit), (g) `BodyEqualityTest` over 13 routes (fal t2i/t2v/i2v/ref2v/edit/tts/lipsync/music, Veo, Gemini image, Omni, Lyria, Sarvam) plus the two-call extend, (h) `RefuseLiveRenderDryTest` + `ManifestTest.test_unpinned_and_enablement_keys_never_dispatch` (all 9 keys), (i) `ParameterRefusalTest`, (j) `StoreTest` + `StoreThroughAdapterTest`, (k) `test_imageio.py` + `test_instruments.py` (33 tests: identical/perturbed images, 120-ms shifted click train → lag 120 ± 10, corrupt PNG → `parse_failure`, missing ffmpeg → `instrument_unavailable`), (l) `test_registry_gate.py` (`BatteryHarness.write_registry_row is Harness.write_registry_row`; refusals for a non-deterministic capability, a provisional instrument and a synthetic measurement), (m) `AuthorisationTest` (no live ledger from the committed state), (n) `SurfaceRegistryTest`. Extra: `test_dry_run.py` mechanises Tester checks 2, 3, 4 and 8; `test_q1.py` covers the detector, the record checker and the pre-registration guard.

## 3. Dry-run manifest (OBSERVED)

`eval/harness-v2/DRY-RUN-MANIFEST-2026-09.yaml`, generated from the committed HEAD `c60d2244…` (TEST-CASES sha256 `2681066e…`, COST-TABLE `51e28596…`), roster sha256 `99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46` (= `COST-TABLE.priced_against_roster`), roster last commit `3434b370c3ca4002ec014f9fa58f418806aeeb16`. Header states it is planning evidence, not a spend authorisation.

Counts: 320 rows = **288 non-conditional (1a 192 / 1b 96) + 32 conditional** — equal to COST-TABLE `totals.calls` (Controller note 6; the task file's 298/186/112 and 155.71 are superseded and recorded as such). `would_dispatch: true` 260; false 60; unpinned calls 20 (= COST-TABLE `unpinned_calls_excluded_from_cap`). Every `would_dispatch: true` row is price pinned, route pinned, shape verified (tested).

| tranche / pool | calls | manifest | COST-TABLE | delta | closed by |
|---|---:|---:|---:|---:|---|
| 1a cash | 142 | 50.30 | 50.15 | +0.15 | flux-2-pro-edit multi-reference addon (MD-C10) |
| 1a credits | 50 | 25.50 | 25.50 | 0.00 | — |
| 1b cash | 66 | 65.30 | 65.30 | 0.00 | — |
| 1b credits | 24 | 14.49 | 15.51 | −1.02 | omni-long 15 s vs the pinned 10-s page cap (MD-C11), −1.0136; residual −0.01 = 4-decimal rounding |
| 1b sarvam_credits | 6 | ₹0.80 (USD-equiv 0.0084) | ₹0.80 / USD 0.01 | −0.01 | rounding |
| **in cap** | **288** | **155.59** (+ ₹0.80) | **156.46** | **−0.87** | explained −0.86, residual −0.00, `all_pools_closed: true` |

Conditional pools reconcile within 0.01 (1a credits 5.44 = 5.44). Four explained lines only: IMG-COMP-01 / IMG-REF-01 / IMG-REF-02 flux-2-pro-edit (+0.03 / +0.06 / +0.06) and VID-MS-01 gemini-omni-1.1-flash-long (−1.0136). INFERRED: both deltas are genuine planning questions, not code defects — see MD-C10 / MD-C11.

Shape status: 41 keys `verified` (pinned fal OpenAPI, pinned Vertex/Sarvam pages, or the live-proven Gemini image body); **1 `unverified`**: `kling-v3-elements` (fal returns "OpenAPI schema not available" for `fal-ai/kling-video/v3/pro/elements`; renders a marker body, refuses dispatch; conditional and unpinned anyway); **5 `not_built`**: `sd3.5-large`, `mai-image-2.6`, `sora-2`, `chirp-3-hd-hi-in`, `azure-neural-tts-hi-in` (registry entries with `adapter: none`; the Azure three carry `dispatch_preconditions: [subscription == b832f4a1-…]`).

## 4. Instruments (OBSERVED)

All seven are `harness.Instrument` objects built by `instruments/common.build_instrument`; the criteria file sha256, the thresholds, the frozen flag, the colour space and the ffmpeg/ffprobe version lines are inside `config` and therefore inside `config_hash` (tested: freezing a threshold changes the identity). Fail-closed: `parse_failure` on any unparseable input, `instrument_unavailable` when ffmpeg/ffprobe is missing. **Every entry in `PASS-CRITERIA-v0.yaml` is `frozen: false`, `status: proposed`** (gate_wrapper: `observation_only_never_a_row`), so every instrument returns `absent / other / criterion_not_frozen` and keeps its measurement plus `would_verdict` as an observation.

| instrument | capabilities | proposed threshold | source |
|---|---|---|---|
| `format_probe` | delivery_format_compliance, reliability_pass_at_k | aspect ±1 %; duration ±0.5 s; audio present iff `audio: on`; resolution class = declared | Planner proposal |
| `masked_diff` | edit_preservation | MAE ≤ 8/255 outside the mask; SSIM ≥ 0.90 (8×8 non-overlapping windows, K1 0.01, K2 0.03) | Planner proposal; Wang 2004 (external, verified: false) |
| `brand_colour` | packaging_brand_colour_fidelity | ΔE*ab (CIE76, CIELAB D65) ≤ 5 | Planner proposal; "ΔE≈2.3 JND" not verified |
| `audio_track_offset_vs_drive` (`av_offset`) | audio_video_synchronisation — **partial claim** | \|lag\| ≤ 80 ms; peak correlation ≥ 0.5 else "no alignment" (absent) | Planner proposal; ITU-R BT.1359-1 not verified |
| `repeat_consistency` | reproducibility | unseeded: same probed format (structural); held-seed: dHash Hamming ≤ 4; groups never pooled | Planner proposal |
| `ledger_metrics` | latency_errors_refusals, cost_and_cpao | pass = status ok; pass = settled ≤ reserved; CpAO absent / not_applicable | task §3 ("no threshold needed") — kept unfrozen anyway (MD-C15) |
| `gate_wrapper` | none | observation only; `provisional`, `registry_writable` False | plan §D |

On this checkout `gate_wrapper.run_post` returns `{status: not_available_on_base, base: c60d224…}` (OBSERVED; `canon/gate/run_gate.py` exists only on `work/canon-gate-001`, read for the CLI contract: `post --artifact --dispatch --modality [--frames DIR] [--json PATH]`).

`registry_gate` reads the 8 ids from `EVALUATOR-PLAN.yaml`; `BatteryHarness.registry_row_for` = gate → **inherited** `write_registry_row` → `attach_uncertainty` (`computed`, `clopper_pearson_95` by bisection, `computed_over: base_items`, `independence_status: NOT ESTABLISHED`, `is_reference_calculation_only: true`). **No Registry row and no data row under `eval/registry/` was written**; `validate_registry.py` → 0 rows, PASS.

## 5. Q1 — geometry qualification run (OBSERVED)

Pre-registration `Q1-…-PREREGISTRATION.yaml` (sha256 `e7edee8c1cbcd5b4d86452af513539d3942141e0007376636799ad09da87c038`, quoted in the result) was written **before** the run by `run_q1.py --preregister`; `--run` refuses without it and refuses if the detector's `configuration_hash` (`70ea60d8…`) differs. R_q = 3; T_rgb = 30 (Euclidean sRGB, hash-covered); gates cited to `FAMILY-2-DETERMINISTIC-CV.md#Gate`; pack hash over the 102 image sha256s; manifest sha256 = the protected baseline before and after; `build_cv_fixtures.py --verify` PASS before and after; 306 observations in the JSONL; elapsed **20.5 s** (< 10 min); spend 0.

| family | n | agreement (all 3 passes) | status | qualified | why |
|---|---:|---|---|---|---|
| object_count | 30 (+ blank) | 27/30 | **disqualified** | false | cv-0024/25/26 (the three OVERLAPPING same-colour circle fixtures) detected as 1 component each — the frozen 4-connected-component method merges touching objects, the trap the pack was built to catch; a failure, recorded as informative |
| spatial_relationship_2d | 40 | 40/40 | qualified | true | exact agreement, R_q = 3 |
| size_aspect | 15 | 15/15 | qualified | true | exact agreement, R_q = 3 |
| attribute_binding | 15 | 15/15 | provisional | **null** | the colour judgement rests on T_rgb, which FAMILY-2 says needs Controller approval — none exists |

Negative controls: blank → 0 objects ✔; corrupt → `ProbeError` (fail closed) ✔; repeat consistency 1.0 everywhere. Supplementary (gates nothing): object_count agreement on the non-count categories 72/75 (the three misses are the same merge behaviour, not present there — INFERRED: multi-object fixtures where shapes touch). Every record carries `registry_use_permitted: false`, `controller_ratification_required: MD-C2`, and the narrow domain "flat-colour synthetic renders on white, 640×480 — no transfer to photographic outputs". `check_record.py` → every schema field present in every record.

## 6. Deviations from the task file and things the Controller should know

1. Task figures: the manifest uses the Controller's 192/96/288 + 32 and 156.46 (note 6); the task file's 298/155.71 are recorded as superseded in the header.
2. `eval/runs/` was already gitignored (line 39), contrary to the task text; no change needed. **`.gitignore` was changed once**: `eval/harness-v2/authorization.local.yaml` added (the task's design assumes it is ignored; it was not) — MD-C13.
3. `ledger.py` overrides `reserve` / `record` beyond the task's whitelist (create/open/_check/remaining_usd/authorised_usd) only to REQUIRE `billing_pool`, `currency`, `amount_native`, `amount_usd_equiv` on every row before delegating to the inherited method; nothing frozen is edited — MD-C14.
4. `ledger_metrics` is `frozen: false` although the task said no threshold is needed, because note 4's blanket rule wins — MD-C15.
5. `store.py` is a new module: `pilot-substrate/artifact_store.py` names files by attempt id, maps only video types and has no request/record/manifest trio, so it could not be subclassed into the EVAL-024 pattern.
6. `imageio.py` and `gate_wrapper.py` (and `casebook`/`dry_run` for `git show`) run **local** subprocesses (ffmpeg/ffprobe/git/the gate); `transports.py` remains the only module importing urllib — Tester check 2 output: `transports.py`, `tests/_support.py`, `tests/test_transports.py`, `tests/test_adapters.py`.
7. Pinned schema/doc bytes were fetched by the earlier attempt on 2026-09-04 (URLs and sha256 in `schemas/fal/FETCH-LOG.txt` and `schemas/*/SCHEMA-INDEX.yaml`); no fetch of any kind was made tonight.
8. The live transports (`FalQueueTransport`, `VertexTransport`, `SarvamTransport`, `GcloudServiceAccountTokenSource`) have never touched a provider; the first authorised call is the first proof of the real path.
9. `~/.mi-battery-keys/gcp-mi-battery-sa.json` does not exist (OBSERVED, name check only), so the default Vertex credential NAME is `~/.aight-litellm-keys/vertex-sa.json` (MD-C3).

## 7. Morning decisions (none attempted; recorded for the Controller)

- **MD-C1** freeze or amend every threshold in `PASS-CRITERIA-v0.yaml` (set `frozen: true`, `status: frozen`, ruling ref). Until then no instrument yields pass/fail.
- **MD-C2** approve T_rgb = 30 for Q1 attribute binding; ratify Registry use of the two `qualified` Q1 families; decide whether `object_count` gets a new task (an overlap-splitting detector, e.g. distance-transform peaks) or stays disqualified.
- **MD-C3** Vertex credential file: default `~/.aight-litellm-keys/vertex-sa.json` (mi-battery file absent tonight).
- **MD-C4** ffmpeg/ffprobe 8.1.2 relied on; no numpy/PIL installed; confirm.
- **MD-C5** accept the free unauthenticated schema/page fetches (2026-09-04) as the body-shape source.
- **MD-C6** accept `audio_track_offset_vs_drive` as a partial claim for `audio_video_synchronisation`, or withdraw that Registry claim from Stage A.
- **MD-C7** Lyria id `lyria-002` (30-s WAV, `sample_count: 1`).
- **MD-C8** `quality: medium` pin for `openai/gpt-image-2` (body refuses without it; tested).
- **MD-C9** the 20 unpinned calls (`gpt-image-2-edit` 12, `sync-lipsync-v3` 6, `veo-3.1-lite-i2v` 2) stay outside the cap and refuse dispatch.
- **MD-C10 (new)** `flux-2-pro-edit` with 2–3 references: roster-implied 0.060 / 0.075 per call vs COST-TABLE 0.045 (IMG-COMP-01, IMG-REF-01/02; 6 calls, +USD 0.15). The price check refuses dispatch until the rule is pinned.
- **MD-C11 (new)** VID-MS-01 `gemini-omni-1.1-flash-long`: the pinned Vertex page caps Omni Flash at 10 s; COST-TABLE bills 15 s; the body renders 10 s (2 calls, −USD 1.01). Choose 10 s, drop the row, or name another surface.
- **MD-C12 (new)** confirm the fal image size policy (`SIZE_A` long side 1024 exact aspect; `SIZE_SEEDREAM` short side 1024) recorded on every manifest row.
- **MD-C13 (new)** ratify the `.gitignore` line for `eval/harness-v2/authorization.local.yaml`.
- **MD-C14 (new)** ratify the `reserve`/`record` overrides in `ledger.py` (deviation 3).
- **MD-C15 (new)** ratify keeping `ledger_metrics` unfrozen (deviation 4).
- **MD-C16 (new)** Sarvam `language_code` for the Hinglish case AUD-TTS-02 is sent as `hi-IN` (code-mixed Hindi); confirm, or name the code the Controller wants.

## 8. Tester checklist, self-run (OBSERVED)

1. `python3 -m unittest discover -s eval/harness-v2/tests -v` → 123 tests OK, 0 skipped — **PASS**.
2. `grep -rnE "urllib|http\.client|socket|requests" eval/harness-v2 --include='*.py' -l` → `transports.py`, `tests/_support.py`, `tests/test_transports.py`, `tests/test_adapters.py` — **PASS** (tests are the monkeypatching ones).
3. key-pattern grep over `eval/harness-v2`, the Q1 records and this report → no hits — **PASS** (ENVIRONMENT and this report carry names only).
4. manifest: 288 / 32 (192 / 96); every pool within 0.01 or closed by explained lines; in-cap 155.59 vs 156.46 closed (residual −0.00); every `would_dispatch: true` row pinned/pinned/verified — **PASS** (`test_dry_run.py`).
5. Q1: pre-registration sha256 quoted; `check_record.py` PASS; `registry_use_permitted: false` ×4; `build_cv_fixtures.py --verify` PASS after the run; `shasum -a 256 -c protected-baselines.sha256` all OK — **PASS**.
6. `validate_registry.py` → 0 rows, PASS; `git status --porcelain` = ` M .gitignore`, `?? eval/harness-v2/`, `?? eval/v1/instruments/qualification-records/` (+ this report); `git diff --stat` on every other path empty — **PASS**.
7. `PASS-CRITERIA-v0.yaml`: 7 entries, all `frozen: false`, each with a `source` — **PASS** (`CriteriaFileTest`).
8. every catalogue key resolves in `SurfaceRegistry` (set equality); the three unpinned keys and the five `needs_controller_enablement` keys plus `kling-v3-elements` refuse live dispatch — **PASS** (`RefuseLiveRenderDryTest`, `ManifestTest`).
