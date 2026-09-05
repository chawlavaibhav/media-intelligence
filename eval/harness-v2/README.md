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
| `ledger.py` | `BatteryRun / BatteryBudget / PoolStageBudget` = subclasses of EMP-001's ledger; EVERY ceiling / cap / INR sub-cap comes from `authorization.local.yaml` (the signed record's `machine_authorisation` block; gitignored, absent tonight) - no constant in code; the roster sha256 named there must equal the roster on disk; every open re-validates the file |
| `store.py` | sealed artifact store: `media/<trial>.<ext>` + `.request.json` (written **before** dispatch) + `.record.json` + `.attempt.json` + append-only manifest; never overwrites |
| `transports.py` | the **only** module that may open a socket (urllib) or run a network-capable subprocess (`gcloud` token, at dispatch only); plus the fakes the tests use |
| `casebook.py` | TEST-CASES rows × repeats with each case's blueprint prompt; route catalogue read from COST-TABLE (working tree or a git revision) |
| `adapters/` | `base` (one builder for dry-run and dispatch, the invariants), `fal_queue`, `vertex_veo`, `vertex_gemini_image`, `vertex_omni`, `vertex_lyria`, `sarvam_tts`; `NullAdapter` for the not-built surfaces |
| `dry_run.py` | renders body + price for every (case, route row, repeat) and reconciles against COST-TABLE line by line |
| `instruments/` | `imageio` (stdlib PNG codec + ffmpeg wrappers), `common`, `metrics`, `format_probe`, `masked_diff`, `brand_colour`, `av_offset`, `repeat_consistency`, `ledger_metrics`, `gate_wrapper`, `registry_gate`, `PASS-CRITERIA-v0.yaml` |
| `battery_harness.py` | `BatteryHarness(Harness)`: bytes-aware `generate()` / `measure()`; `write_registry_row` **inherited, never overridden** |
| `q1/` | `detector.py` (frozen method), `run_q1.py` (`--preregister`, then `--run`), `check_record.py` (schema checker) |
| `schemas/` | pinned fal OpenAPI JSON and vendor reference pages (gzipped) with sha256 — the only source of request-body shapes |
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

## The rules the code enforces (each is a test)

* construction opens no socket and reads no key; a key is read by **name** at dispatch and never enters a body,
  log, record or exception text;
* output-count parameters are pinned to 1; a field absent from the pinned schema is refused; `seed` is sent only
  under SEED-POLICY `held` (today: never);
* one `dispatch()` = one submit; polls, result reads and downloads are lifecycle steps of that trial; the poll loop
  is bounded and can never resubmit; 0 retries;
* the reservation is written **before** the first byte leaves; only a refusal raised by our own code before any send
  releases it; ANY other exception after the reservation persists an attempt and settles it as ambiguous, with
  credential values scrubbed from the record (Auditor AF-3);
* the dry-run body bytes are the bytes the (fake) transport receives — same builder, no second rendering;
* no adapter, unverified shape, conditional row, unpinned price or unsatisfied precondition ever dispatches;
* every instrument fails closed (`parse_failure`), reports a missing tool (`instrument_unavailable`), and returns
  `absent / criterion_not_frozen` until its threshold is frozen;
* only the eight deterministic capabilities, through a `deterministic` or `qualified` instrument, over
  non-synthetic measurements, can reach the frozen `write_registry_row` (the gate sits in front of it on every path). This task writes no row.

## What is NOT true yet

The live transports have never been exercised against a provider (zero-spend rule). The first authorised call is
the first proof of the real path. Every threshold in `PASS-CRITERIA-v0.yaml` is a proposal (MD-C1). Q1's
`attribute_binding` is `qualified: null` until the colour tolerance is approved (MD-C2), and its `object_count`
family is **disqualified** on the three overlapping-circle fixtures — the frozen 4-connected-component method merges
touching same-colour objects, which is exactly the trap the pack was built to catch.
