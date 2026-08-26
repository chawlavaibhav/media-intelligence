# EMP-001 — first empirical tranche execution package

**Status:** PREPARED, **NOT AUTHORISED**. Zero external spend. Zero provider/model/evaluator calls.

Nothing in this directory has ever contacted a provider. Running everything documented below
costs **USD 0 / INR 0** and makes **0** external calls.

---

## The gate order

Money can only be spent by passing every gate, in this order. Each one is enforced mechanically
and each one has a test that confirms it refuses.

| # | Gate | Enforced by |
|---|---|---|
| 0 | Preflight green — geometry, persistence, Registry-zero, baselines | `preflight.py` |
| 1 | An explicit authorisation file naming EMP-001 and its exact ceiling | `budget_guard.open_guard` |
| 2 | A text judge qualified on **both** scripts the A-TEXT items span | `atex/run_atex.py` |
| 3 | A budget reservation that succeeds **before** dispatch | `budget_guard.BudgetGuard.reserve` |
| 4 | A per-route ceiling of 8 generations, not raisable at runtime | `atex/run_atex.py` |

A failed gate stops downstream spend automatically. Retries authorised: **0**.

## Commands (all zero-spend)

```bash
# preflight: Q1 geometry, Q7 persistence, Registry-zero, baselines, authorisation gate
python3 eval/empirical-tranche-1/preflight.py --dry-run

# progressive text-judge qualification, simulated against deterministic local fakes
python3 eval/empirical-tranche-1/text_qualification/qualify_text.py --dry-run

# the gated 16-generation A-TEXT screen, simulated
python3 eval/empirical-tranche-1/atex/run_atex.py --dry-run

# the tests
python3 -m pytest -q eval/empirical-tranche-1/tests

# inherited V1 verification
python3 eval/v1/harness/run_selftest.py
bash   eval/v1/harness/run_cross_branch_validation.sh
```

### Rebuilding the derived material

Both are gitignored build products, reproducible from committed code plus a pinned font.

```bash
# the Latin pack images + the mechanical perceptibility record
python3 eval/empirical-tranche-1/text_qualification/render_latin_pack.py

# the 96-item Devanagari validated view — note the --out-dir OUTSIDE the battery
cd eval/battery/devanagari-exactness
python3 build_items.py --total 120 \
  --out-dir ../../empirical-tranche-1/text_qualification/build/devanagari
python3 apply_human_validation.py \
  --from-build ../../empirical-tranche-1/text_qualification/build/devanagari \
  --out-dir    ../../empirical-tranche-1/text_qualification/build/devanagari/validated
```

The frozen Devanagari battery is **read and never written to**. Its rebuilt `items.jsonl` hashes
to the `battery_identity` recorded in the human-validation record, which is how the materialised
view is proved to be the one the reviewer actually validated.

## Secrets

No key, token or credential belongs in any committed file. Provider credentials are read from the
environment **at dispatch time only**, never at import or construction:

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`

`authorization.local.yaml` is gitignored and must never be committed. The committed
`authorization.example.yaml` carries `authorised: false` and a zero ceiling.

## What a dry run is not

Every dry-run result is marked `synthetic: true` and `may_populate_registry: false`. A dry run
proves the harness executes and stops where it should. It says **nothing** about any real model,
and the Capability Registry refuses its evidence — see `attempt_registry_write_with_dry_run_evidence`,
which exercises the real harness boundary rather than asserting the rule in prose.

## Layout

| Path | What it is |
|---|---|
| `config.yaml` | frozen versions, ceiling, repeats, seed policy, item ids |
| `authorization.example.yaml` | schema only, `authorised: false`, zero secrets |
| `budget_guard.py` | fail-closed authorisation gate + cumulative spend guard |
| `providers.py` | judge request builders/parsers; fail-closed dispatch |
| `preflight.py` | Q1/Q7/Registry/baseline/authorisation preflight |
| `protected-baselines.sha256` | pre-EMP-001 fingerprints of every protected artifact |
| `text_qualification/` | Latin pack builder, renderer, perceptibility, qualification runner |
| `atex/` | four frozen items, their contract, the gated runner |
| `tests/` | budget, pack, perceptibility, preflight, blind-payload, gate-order controls |
| `VERIFICATION-PRE-SPEND.md` | fresh command output from the pre-spend gate |
| `EVAL-012-ZERO-SPEND-READINESS.md` | the readiness verdict returned to the Controller |
