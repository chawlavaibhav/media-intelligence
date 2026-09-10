# eval/harness-v2 — Stage A battery plumbing (EVAL-039C)

**What this is, in plain English.** Before a single paid call is made for the Stage A battery (EVAL-040), three
things have to exist as tested code rather than as good intentions:

1. **Adapters** that can render the exact request each of the 288 Tranche-1 calls would send, price it from the
   pinned roster, and — only when a Controller-signed authorisation file exists — send that same body exactly once
   through a reservation-first ledger. Tonight they render and price; nothing is sent (`DRY-RUN-MANIFEST-2026-09.yaml`).
2. **Deterministic instruments** for the eight capabilities the evaluator plan calls `yes_deterministic`, each failing
   closed on bad input and each returning *absent / criterion_not_frozen* until the Controller freezes its threshold
   in `instruments/PASS-CRITERIA-v0.yaml` (MD-C1). No Registry row can be built on an unapproved number.
3. **Q1**, the geometry qualification run over the 102-item synthetic pack, at USD 0, pre-registered first
   (`eval/v1/instruments/qualification-records/`).

Nothing in this package edits `eval/empirical-tranche-1/`, `eval/pilot-substrate/` or `eval/v1/harness/`; it imports
them read-only (`hv2_paths.py`) and subclasses what it needs. The protected baselines still hash true.

## Map

| Path | What it does |
|---|---|
| `hv2_paths.py` | read-only import paths to the frozen packages (harness-v2 first, so its `adapters/` package shadows the frozen `adapters.py`) |
| `surfaces.py` | `SurfaceRegistry`: the 47 route keys → adapter, surface, model id, endpoint, pinned schema, price pin, pool, credential **name**, `shape_status` |
| `pricing.py` | roster + COST-TABLE reader; execution-time price check (re-reads the roster every time; refuses drift, promos, unpinned or non-projectable prices, unknown quantity rules) |
| `ledger.py` | `BatteryRun / BatteryBudget / PoolStageBudget` = subclasses of EMP-001's ledger; EVERY ceiling / cap / INR sub-cap comes from `authorization.local.yaml` (the signed record's `machine_authorisation` block; gitignored, absent tonight) - no constant in code; the roster sha256 named there must equal the roster on disk; every open re-validates the file. 2026-09-10 (Auditor AF-4 / AF-5): **one authorisation = one cap across every run that used it** - spend recorded by sibling runs (same `authorisation_sha256` in their `run.json`, under this ledger root or a sibling `<out>/ledger` root) is pooled into the ceiling, the 1a / 1b caps and the INR / credits sub-caps, a new run under a consumed cap is refused at `BatteryRun.create` naming those runs and the combined total, and an unreadable sibling refuses rather than counting zero; the OPTIONAL `max_paid_calls` field caps the NUMBER of paid calls over the same pooled set (absent = no call limit, said in words by `authorisation_status`) |
| `store.py` | sealed artifact store: `media/<trial>.<ext>` + `.request.json` (written **before** dispatch) + `.record.json` + `.attempt.json` + append-only manifest; never overwrites |
| `transports.py` | the **only** module that may open a socket (urllib) or run a network-capable subprocess (`gcloud` token, at dispatch only); plus the fakes the tests use |
| `casebook.py` | TEST-CASES rows × repeats with each case's blueprint prompt; route catalogue read from COST-TABLE (working tree or a git revision) |
| `adapters/` | `base` (one builder for dry-run and dispatch, the invariants), `fal_queue`, `vertex_veo`, `vertex_gemini_image`, `vertex_omni`, `gemini_api_image` + `gemini_api_omni` (2026-09-09, CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY: the Gemini-named routes `nano-banana-2` / `nano-banana-pro` / `nano-banana-pro-edit` / `gemini-omni-1.1-flash*` run on generativelanguage.googleapis.com with the key NAMED `GOOGLE_API_KEY`, pool `credits` "GCP credits via the Gemini API key"; image = the Vertex generateContent body byte for byte, Omni = the Interactions API body; pins in `price-pins-2026-09/gemini-api/`, shapes in `schemas/gemini_api/`), `vertex_lyria`, `sarvam_tts`, `elevenlabs_direct` (2026-09-09: ElevenLabs on the user's own account, `tts` + `music`, mp3 bytes back, billed in PLAN CREDITS - pool `elevenlabs_credits`, 0 USD cash, credits recorded natively from the pinned pricing page, capped by the optional `elevenlabs_cap_credits`; routes `elevenlabs-v3-direct` / `elevenlabs-music-direct` are `surfaces.EXTENSION_ROUTES`, outside the freeze catalogue); `NullAdapter` for the not-built surfaces |
| `dry_run.py` | renders body + price for every (case, route row, repeat) and reconciles against COST-TABLE line by line; EVAL-041 part 2: takes the input resolver (`inputs_for`) so input rows render with their sealed bytes, refuses `input_unresolved:<role>` otherwise, reports `roster_implied_usd` / `cost_table_unit_price` / `price_basis` and honours `accept_roster_price` on multi-reference FLUX edit rows |
| `inputs.py` | EVAL-041 part 2: the input resolver - a committed `INPUTS.yaml` maps (case, arm, role) -> a sealed artifact (`fixture:<run>:<id>` or `<run>:<trial>[:<suffix>]`); bytes are loaded from the sealed store, sha256-verified, and handed to the adapter as a data URI (fal) or bytes (Vertex); decoy fixtures refuse; templates `INPUTS.half2.template.yaml` / `INPUTS.topo3.template.yaml` |
| `fixtures.py` | EVAL-041 part 2: `run_live.py fixtures` - plans (`FIXTURE-PLAN.yaml` + sha) and executes STAND-IN-SPEC.yaml: generations, derived views (parent fixture through the resolver), code overlays (USD 0); every output sealed as a `constructed_synthetic` fixture record under `<out>/artifacts/fixtures/`; same ledger, caps, 0 retries, resumability |
| `composite.py` | TOPO-02 arm C overlay (exact strings by code); `--video` (EVAL-041 part 2) overlays every frame of a sealed clip via ffmpeg and re-encodes at the source fps, sealed with suffix `composite` |
| `instruments/` | `imageio` (stdlib PNG codec + ffmpeg wrappers), `common`, `metrics`, `format_probe`, `masked_diff`, `brand_colour`, `av_offset`, `repeat_consistency`, `ledger_metrics`, `gate_wrapper`, `registry_gate`, `PASS-CRITERIA-v0.yaml` |
| `battery_harness.py` | `BatteryHarness(Harness)`: bytes-aware `generate()` / `measure()`; `write_registry_row` **inherited, never overridden** |
| `registry_rows.py` | EVAL-041: the first Registry rows from sealed run records under the FROZEN criteria (`--run OUT:RUN_ID ... [--write]`); every row through `BatteryHarness.registry_row_for`; infra faults excluded, refusals counted; dry by default |
| `evidence_map.py` | EVAL-041: `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml` - the tiered product asset (deterministic rows / human blind acceptance / screened / historical prior) per (question, route); human tiers never `registry: true`; 2026-09-09: the `screened_not_qualified` tier is filled from a `SCREEN-RESULTS.yaml` beside a RESULTS.yaml (agreement with the Controller, n, config hash; status `qualified` only under a binding QUALIFICATION-REPORT; registry stays false) |
| `instruments/vlm_screen.py` | 2026-09-09: the VLM screen - one artifact + the case's acceptance_contract -> per-line pass / fail / cannot_judge + an overall derived in code by the Controller's rule; Gemini Developer API (`GeminiApiTransport`, key NAMED `GOOGLE_API_KEY`, never Vertex - CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09); strict JSON, temperature 0; video = 3 sampled frames, audio = cannot_judge at USD 0; `screened_not_qualified`, refused by registry_gate; prompt + model id + `SCREEN-QUALIFICATION-CRITERIA-v0.yaml` sha in config_hash |
| `qualify_screen.py` | 2026-09-09: qualification runner - every Controller-judged trial through the screen, compared with the blind verdict: agreement, Cohen's kappa, per-question / per-route confusion, disagreements with the Controller's note, `qualification_verdict` against `instruments/SCREEN-QUALIFICATION-CRITERIA-v0.yaml` (UNFROZEN: the verdict stays `screened_not_qualified`, `would_verdict` recorded); `--dry-run` prints calls / frames and "price not pinned" (no number) until a Gemini API price pin exists; a live run refuses without `--auth` carrying `screen_cap_usd` > 0 AND the pin, reserves every call against the cap |
| `q1/` | `detector.py` (frozen method), `run_q1.py` (`--preregister`, then `--run`), `check_record.py` (schema checker) |
| `schemas/` | pinned fal OpenAPI JSON and vendor reference pages (gzipped) with sha256 — the only source of request-body shapes; `schemas/elevenlabs/` holds extracts over the raw pages pinned under `eval/empirical-planning/price-pins-2026-09/elevenlabs-direct/` |
| `tests/` | `unittest`, stdlib only; every test runs with sockets and `urlopen` monkeypatched to raise and every key name stripped from the environment |
| `ENVIRONMENT-2026-09.yaml` | what is installed (names only); nothing was installed |
| `authorization.example.yaml` | the schema of the authorisation file; `authorised: false`; a live ledger cannot be opened from the committed state (a test proves it) |

## How to run

```bash
# every test (fake transports only; no socket, no key, no queue submit)
python3 -m unittest discover -s eval/harness-v2/tests -v

# the dry-run manifest, from the committed HEAD (nothing is sent)
python3 eval/harness-v2/dry_run.py --git-rev HEAD --out eval/harness-v2/DRY-RUN-MANIFEST-2026-09.yaml

# Q1 (already run; a second run needs a new record id - the runner refuses to overwrite)
python3 eval/harness-v2/q1/run_q1.py --preregister    # once, BEFORE any run
python3 eval/harness-v2/q1/run_q1.py --run
python3 eval/harness-v2/q1/check_record.py eval/v1/instruments/qualification-records/Q1-deterministic-cv-geometry-2026-09.yaml
```

```bash
# EVAL-041 part 2: stand-in fixtures (dry plan first), image half two with resolved inputs, VID-TOPO3-01 (plates, then video rows)
python3 eval/harness-v2/run_live.py fixtures --dry --spec eval/experiments/EVAL-040/fixtures/STAND-IN-SPEC.yaml --run-id half2-fixtures \
    --out eval/experiments/EVAL-040/runs/half2-fixtures --auth eval/harness-v2/authorization.half2.local.yaml       # USD 0: FIXTURE-PLAN.yaml + total
python3 eval/harness-v2/run_live.py fixtures --spec ... --run-id half2-fixtures --out ... --auth ...                     # LIVE, resumable
python3 eval/harness-v2/run_live.py plan --run-id half2 --cases IMG-EDIT-01,IMG-EDIT-02,IMG-EXT-01,IMG-COMP-01,IMG-REF-01,IMG-REF-02 \
    --tranche 1a --inputs INPUTS.yaml [--accept-roster-price] --out <dir> --auth eval/harness-v2/authorization.half2.local.yaml
python3 eval/harness-v2/run_live.py plan --run-id topo3-video --cases VID-TOPO3-01 --tranche 1a,1b --inputs INPUTS.yaml --out <dir> --auth ...video1...
python3 eval/harness-v2/composite.py --video --run-id topo3-video --out <dir> --spec <VIDEO-COMPOSITE-SPEC.yaml>   # USD 0, arm C clips

# EVAL-041: Registry rows from Image Round 1's sealed records (dry first; --write appends through the harness writer)
python3 eval/harness-v2/registry_rows.py --run eval/experiments/EVAL-040/runs/img-r1:img-r1 \
    --run eval/experiments/EVAL-040/runs/img-r1-redo:img-r1-redo --run eval/experiments/EVAL-040/runs/img-r1-composite:img-r1-composite [--write]
python3 eval/harness-v2/evidence_map.py --results eval/experiments/EVAL-040/runs/img-r1/RESULTS.yaml \
    --composite-results eval/experiments/EVAL-040/runs/img-r1-composite/RESULTS.yaml
```

## The rules the code enforces (each is a test)

* construction opens no socket and reads no key; a key is read by **name** at dispatch and never enters a body,
  log, record or exception text;
* output-count parameters are pinned to 1; a field absent from the pinned schema is refused; `seed` is sent only
  under SEED-POLICY `held` (today: never);
* one `dispatch()` = one submit; polls, result reads and downloads are lifecycle steps of that trial; the poll loop
  is bounded and can never resubmit; 0 retries;
* a signed authorisation is ONE cap however many runs use it: the ceiling, the tranche caps and (when the record
  names `max_paid_calls`) the number of paid calls are checked over this run PLUS every sibling run that recorded the
  same authorisation sha256; a sibling whose `run.json` or ledger cannot be read refuses the run rather than counting zero;
* the reservation is written **before** the first byte leaves; only a refusal raised by our own code before any send
  releases it; ANY other exception after the reservation persists an attempt and settles it as ambiguous, with
  credential values scrubbed from the record (Auditor AF-3);
* the dry-run body bytes are the bytes the (fake) transport receives — same builder, no second rendering;
* no adapter, unverified shape, conditional row, unpinned price or unsatisfied precondition ever dispatches;
* every instrument fails closed (`parse_failure`), reports a missing tool (`instrument_unavailable`), and returns
  `absent / criterion_not_frozen` until its threshold is frozen;
* only the eight deterministic capabilities, through a `deterministic` or `qualified` instrument, over
  non-synthetic measurements, can reach the frozen `write_registry_row` (the gate sits in front of it on every path). This task writes no row;
* (EVAL-041 part 2) an input reaches an adapter only through `inputs.py` from a sealed, sha256-verified artifact named in a committed
  `INPUTS.yaml`; the plan's body sha256 is computed WITH the input bytes; execute refuses a changed inputs file, a swapped input or a
  changed body; a decoy fixture never resolves; a placeholder that nobody resolved keeps the row at `would_dispatch: false`
  (`input_unresolved:<role>`).

## What is NOT true yet

The live transports have never been exercised against a provider (zero-spend rule). The first authorised call is
the first proof of the real path. Every threshold in `PASS-CRITERIA-v0.yaml` is a proposal (MD-C1). Q1's
`attribute_binding` is `qualified: null` until the colour tolerance is approved (MD-C2), and its `object_count`
family is **disqualified** on the three overlapping-circle fixtures — the frozen 4-connected-component method merges
touching same-colour objects, which is exactly the trap the pack was built to catch.
