# First Empirical Tranche Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the project's first trustworthy empirical model evidence by qualifying the minimum text/geometry/logging measurement path and, only after qualification passes, running a 16-generation A-TEXT partial admission screen for IMG-01 and IMG-02.

**Architecture:** Keep the existing V1 harness and Resources persistence contracts authoritative. Add a narrow `eval/empirical-tranche-1/` execution package that builds qualification material, wraps real evaluator/generator APIs behind fail-closed budget guards, writes the canonical Attempt/Artifact/Measurement records through the existing harness, and stops at every gate before downstream spend. The package must be runnable in `--dry-run` mode with zero network calls and must refuse paid execution unless an explicit authorisation file names the exact spend ceiling.

**Tech Stack:** Python 3; existing `eval/v1/harness` models/persistence; YAML/JSONL; provider SDK/HTTP clients pinned at execution; pytest/unittest-style existing project tests; SHA-256 manifests.

**Spec:** `coordination/plans/2026-08-26-FIRST-EMPIRICAL-TRANCHE-PROPOSAL.md`

## Global Constraints

- No provider/model/evaluator call before explicit user approval of the Tranche-1 spend ceiling.
- Proposed consumed-API ceiling is exactly **USD 10.00**, excluding taxes; account pre-funding above that ceiling requires separate approval.
- No retries. Every paid provider/API call is one trial even if it refuses, errors or times out.
- Stage-Q model generations remain exactly 0.
- A-TEXT generation ceiling is exactly 16: IMG-01 = 8; IMG-02 = 8.
- V1 36-capability contract and V1 100-item bank remain byte-identical.
- Frozen Devanagari battery remains untouched.
- `transcribe` and `verdict` evaluator shapes remain separate; generated-output exactness uses `transcribe` as the primary measurement.
- Synthetic/dry-run measurements may never populate the empirical Registry.
- A-TEXT is partial evidence only; it may not promote an entire scientific slot.
- Customer-outcome CpAO may not be reported from this tranche.
- Current Veo planning uses per-generated-second billing; this tranche itself contains no Veo calls.

---

## File Structure

Create a focused execution package rather than modifying historical V1 artifacts:

- `eval/empirical-tranche-1/README.md` — exact execution contract, gate order and commands.
- `eval/empirical-tranche-1/config.yaml` — frozen candidate versions, budget ceiling, repeat counts, seed policy and item ids.
- `eval/empirical-tranche-1/authorization.example.yaml` — schema/example only; committed with `authorised: false` and zero secrets.
- `eval/empirical-tranche-1/budget_guard.py` — fail-closed cumulative spend guard.
- `eval/empirical-tranche-1/providers.py` — real provider adapters; imports/configuration do not make network calls.
- `eval/empirical-tranche-1/text_qualification/build_latin_pack.py` — deterministic 96-item Latin pack builder.
- `eval/empirical-tranche-1/text_qualification/latin-pack-v1.jsonl` — generated/frozen item manifest after build.
- `eval/empirical-tranche-1/text_qualification/latin-pack-v1.sha256` — manifest fingerprint.
- `eval/empirical-tranche-1/text_qualification/qualify_text.py` — progressive Devanagari-first qualification runner.
- `eval/empirical-tranche-1/atex/atex-items-v1.jsonl` — four fixed comparability items.
- `eval/empirical-tranche-1/atex/run_atex.py` — gated 16-generation runner.
- `eval/empirical-tranche-1/preflight.py` — Q1/Q7/persistence/dry-run gate.
- `eval/empirical-tranche-1/tests/` — budget, blind-payload, pack, persistence and no-network negative controls.
- `eval/runs/tranche-1/` — execution output root, created at run time; no fabricated empirical result committed in advance.

Modify only where necessary:

- `eval/v1/harness/adapters.py` — **do not add live adapters here**; keep it synthetic-only.
- `eval/v1/harness/harness.py` — modify only if a missing generic hook is proven by a failing test; otherwise consume it unchanged.
- `eval/registry/registry-v1.jsonl` — never hand-edit. Population, if any, must occur only through the existing qualified-instrument promotion path.

---

### Task 1: Freeze Tranche-1 Configuration and Authorization Gate

**Files:**
- Create: `eval/empirical-tranche-1/config.yaml`
- Create: `eval/empirical-tranche-1/authorization.example.yaml`
- Create: `eval/empirical-tranche-1/budget_guard.py`
- Test: `eval/empirical-tranche-1/tests/test_budget_guard.py`

**Interfaces:**
- Consumes: explicit authorisation YAML supplied at execution time.
- Produces: `BudgetGuard(authorised_usd: Decimal, spent_usd: Decimal)` with `reserve(estimated_usd)` and `record(actual_usd)` methods that raise before a ceiling can be exceeded.

- [ ] **Step 1: Write failing budget-guard tests**

```python
from decimal import Decimal
import pytest
from eval.empirical_tranche_1.budget_guard import BudgetExceeded, BudgetGuard


def test_refuses_without_positive_authorisation():
    with pytest.raises(ValueError):
        BudgetGuard(authorised_usd=Decimal('0'), spent_usd=Decimal('0'))


def test_reserve_fails_before_crossing_ceiling():
    g = BudgetGuard(authorised_usd=Decimal('10.00'), spent_usd=Decimal('9.80'))
    with pytest.raises(BudgetExceeded):
        g.reserve(Decimal('0.21'))


def test_record_never_silently_exceeds_ceiling():
    g = BudgetGuard(authorised_usd=Decimal('10.00'), spent_usd=Decimal('9.90'))
    with pytest.raises(BudgetExceeded):
        g.record(Decimal('0.11'))
```

- [ ] **Step 2: Run the tests and verify RED**

```bash
pytest -q eval/empirical-tranche-1/tests/test_budget_guard.py
```

Expected: import/module failure because the guard does not exist yet.

- [ ] **Step 3: Implement the minimal fail-closed guard**

```python
from dataclasses import dataclass
from decimal import Decimal

class BudgetExceeded(RuntimeError):
    pass

@dataclass
class BudgetGuard:
    authorised_usd: Decimal
    spent_usd: Decimal = Decimal('0')

    def __post_init__(self):
        if self.authorised_usd <= 0:
            raise ValueError('positive explicit authorisation required')

    def reserve(self, estimated_usd: Decimal) -> None:
        if self.spent_usd + estimated_usd > self.authorised_usd:
            raise BudgetExceeded('next call could exceed authorised ceiling')

    def record(self, actual_usd: Decimal) -> None:
        if self.spent_usd + actual_usd > self.authorised_usd:
            raise BudgetExceeded('recorded spend exceeds authorised ceiling')
        self.spent_usd += actual_usd
```

- [ ] **Step 4: Freeze config values**

`config.yaml` must contain exactly:

```yaml
tranche_id: EMP-001
status: PREPARED_NOT_AUTHORISED
external_spend_ceiling_usd: 10.00
retries_authorised: 0
qualification:
  repeats_per_shape: 3
  devanagari_items: 96
  latin_items: 96
  shapes: [transcribe, verdict]
  judge_candidates:
    - provider: openai
      model_alias: gpt-5.4-mini
      snapshot_required: true
    - provider: google
      model_alias: gemini-3.5-flash-lite
      snapshot_or_exact_version_required: true
atex:
  seed_policy: unseeded
  repeats_per_item: 2
  items: [ATEXT-01, ATEXT-02, ATEXT-03, ATEXT-04]
  slots:
    IMG-01: {route: openai/gpt-image-2, provider_surface: fal, generations: 8}
    IMG-02: {route: fal-ai/ideogram/v3, provider_surface: fal, generations: 8}
```

`authorization.example.yaml` must remain:

```yaml
authorised: false
tranche_id: EMP-001
max_consumed_api_spend_usd: 0
approved_by: null
approved_at: null
```

- [ ] **Step 5: Run tests GREEN and commit**

```bash
pytest -q eval/empirical-tranche-1/tests/test_budget_guard.py
git add eval/empirical-tranche-1
git commit -m "eval: add EMP-001 authorisation and budget guard"
```

---

### Task 2: Build and Freeze the Separate Latin Qualification Pack

**Files:**
- Create: `eval/empirical-tranche-1/text_qualification/build_latin_pack.py`
- Create: `eval/empirical-tranche-1/text_qualification/latin-pack-v1.jsonl`
- Create: `eval/empirical-tranche-1/text_qualification/latin-pack-v1.sha256`
- Test: `eval/empirical-tranche-1/tests/test_latin_pack.py`

**Interfaces:**
- Produces exactly 96 deterministic records: 48 `match`, 48 `mismatch`, one mismatch opportunity per base string.
- Must not read/write any file under `eval/battery/devanagari-exactness/` except read-only comparison of its contract if needed.

- [ ] **Step 1: Write failing structural tests**

```python
import json
from pathlib import Path

PACK = Path('eval/empirical-tranche-1/text_qualification/latin-pack-v1.jsonl')

def rows():
    return [json.loads(x) for x in PACK.read_text().splitlines() if x.strip()]


def test_pack_is_exactly_96_balanced_items():
    r = rows()
    assert len(r) == 96
    assert sum(x['expected'] == 'match' for x in r) == 48
    assert sum(x['expected'] == 'mismatch' for x in r) == 48


def test_one_mismatch_per_base_string():
    mismatches = [x for x in rows() if x['expected'] == 'mismatch']
    assert len({x['base_id'] for x in mismatches}) == 48


def test_mismatch_classes_are_controlled():
    allowed = {'confusable_substitution','omission','insertion','transposition','case_diacritic','punctuation_digit_space'}
    assert {x['failure_class'] for x in rows() if x['expected'] == 'mismatch'} <= allowed
```

- [ ] **Step 2: Run RED**

```bash
pytest -q eval/empirical-tranche-1/tests/test_latin_pack.py
```

- [ ] **Step 3: Implement deterministic builder**

Use a fixed in-file list of 48 commercially ordinary targets including words, short phrases, prices and alphanumeric claims. Generate exactly one clean render and one controlled corruption per base target. The builder must sort by `item_id`, serialize UTF-8 JSON with stable key order, and write a SHA-256 fingerprint of the final JSONL bytes.

The builder must refuse to run if its output path resolves anywhere inside `eval/battery/devanagari-exactness/`.

- [ ] **Step 4: Build, inspect, run tests**

```bash
python eval/empirical-tranche-1/text_qualification/build_latin_pack.py
pytest -q eval/empirical-tranche-1/tests/test_latin_pack.py
sha256sum eval/empirical-tranche-1/text_qualification/latin-pack-v1.jsonl
```

- [ ] **Step 5: Perform perceptibility sanity review**

Create `eval/empirical-tranche-1/text_qualification/perceptibility-review.csv` with columns:

```text
item_id,visible_difference,usable_surface,reviewer_note
```

Every mismatch must receive `visible_difference=yes`; every item must receive `usable_surface=yes`. Any rejected item causes the builder source list to be corrected and the whole manifest rebuilt before fingerprint freeze. Do not replace only the reviewed row in-place.

- [ ] **Step 6: Commit**

```bash
git add eval/empirical-tranche-1/text_qualification eval/empirical-tranche-1/tests/test_latin_pack.py
git commit -m "eval: freeze EMP-001 Latin exact-text qualification pack"
```

---

### Task 3: Implement Zero-Spend Q1/Q7 and Persistence Preflight

**Files:**
- Create: `eval/empirical-tranche-1/preflight.py`
- Test: `eval/empirical-tranche-1/tests/test_preflight.py`
- Consume unchanged: `eval/v1/harness/harness.py`, `eval/v1/harness/run_selftest.py`

**Interfaces:**
- Produces `preflight-result.json` with explicit booleans for geometry fixtures, logging/persistence, Registry-zero check, dry-run no-network check and authorisation status.

- [ ] **Step 1: Write negative-control test that forbids network during preflight**

Patch `socket.socket.connect` to raise and verify `preflight.py --dry-run` still exits 0. Also assert `eval/registry/registry-v1.jsonl` remains byte-identical.

- [ ] **Step 2: Run existing full harness self-test**

```bash
python eval/v1/harness/run_selftest.py
bash eval/v1/harness/run_cross_branch_validation.sh
```

Any non-zero exit blocks EMP-001. Do not weaken an invariant to make the tranche run.

- [ ] **Step 3: Add Q1/Q7 checks**

The preflight must verify:

```python
assert geometry_fixture_count == 102
assert registry_empirical_row_count == 0
assert one_call_one_trial_contract is True
assert retries_authorised == 0
assert authorisation_file_is_false_or_missing is True  # during preparation
```

- [ ] **Step 4: Run GREEN and commit**

```bash
pytest -q eval/empirical-tranche-1/tests/test_preflight.py
python eval/empirical-tranche-1/preflight.py --dry-run
git add eval/empirical-tranche-1/preflight.py eval/empirical-tranche-1/tests/test_preflight.py
git commit -m "eval: add zero-spend EMP-001 preflight"
```

---

### Task 4: Add Real Judge Adapters Without Polluting Synthetic Harness Adapters

**Files:**
- Create: `eval/empirical-tranche-1/providers.py`
- Test: `eval/empirical-tranche-1/tests/test_provider_adapters.py`
- Do not modify: `eval/v1/harness/adapters.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class EvaluatorResponse:
    text: str
    input_tokens: int | None
    output_tokens: int | None
    billed_usd: Decimal | None
    provider_request_id: str | None

class TextJudge:
    def transcribe(self, image_bytes: bytes) -> EvaluatorResponse: ...
    def verdict(self, image_bytes: bytes, target: str) -> EvaluatorResponse: ...
```

- [ ] **Step 1: Write tests for no-call-on-construction and target blindness**

`OpenAITextJudge(...)` and `GeminiTextJudge(...)` constructors must not call the network. The serialized `transcribe` payload must contain neither the target string nor any Devanagari characters copied from the target. The `verdict` payload must contain the target exactly once in the declared field.

- [ ] **Step 2: Implement provider request builders**

Pin exact model versions at execution. Store the alias and resolved version in every call record. Return token/cost metadata when providers expose it; otherwise calculate a provisional cost from the provider's published rate and replace it with invoice/billing evidence when available.

Never put API keys in committed files; read only from environment variables named in `README.md`.

- [ ] **Step 3: Add fake transport tests**

Use an injected transport that returns deterministic provider-shaped JSON. Verify provider request ids, token fields, refusal/error mapping and cost records are preserved.

- [ ] **Step 4: Run GREEN and commit**

```bash
pytest -q eval/empirical-tranche-1/tests/test_provider_adapters.py
git add eval/empirical-tranche-1/providers.py eval/empirical-tranche-1/tests/test_provider_adapters.py
git commit -m "eval: add fail-closed EMP-001 judge adapters"
```

---

### Task 5: Implement Progressive Devanagari-First Text Qualification

**Files:**
- Create: `eval/empirical-tranche-1/text_qualification/qualify_text.py`
- Create: `eval/empirical-tranche-1/text_qualification/qualification-contract-v1.yaml`
- Test: `eval/empirical-tranche-1/tests/test_text_qualification.py`

**Interfaces:**
- Reads frozen Devanagari 96-item validated view and Latin 96-item manifest.
- Runs exactly 3 passes × 2 shapes per item per candidate.
- Stops a candidate before Latin if it fails Devanagari.
- Produces candidate-level result with `qualified_scope`, false-pass, false-fail, refusal and repeat-consistency fields.

- [ ] **Step 1: Freeze the bounded qualification contract**

```yaml
repeats_per_shape: 3
mismatch_false_pass_max: 0
match_false_fail_rate_max: 0.10
refusal_rate_max: 0.05
repeat_consistency_min: 0.95
primary_generated_output_shape: transcribe
qualified_scope_excludes:
  - malformed_generated_glyphs
```

Mark every threshold `status: PROVISIONAL_FIRST_RUN_GATE`, not universal truth.

- [ ] **Step 2: Write progressive-stop tests**

A fake candidate with one Devanagari false pass must receive exactly 576 Devanagari calls and **0 Latin calls**. A candidate passing Devanagari may receive 576 Latin calls. A budget guard refusal must stop before the next API call.

- [ ] **Step 3: Implement scorer**

Exactness comparison must be code-level Unicode comparison after only the explicitly frozen normalization rules. Do not let the judge decide string equality after transcription.

- [ ] **Step 4: Dry-run with fake transports**

```bash
pytest -q eval/empirical-tranche-1/tests/test_text_qualification.py
python eval/empirical-tranche-1/text_qualification/qualify_text.py --dry-run
```

Expected: complete synthetic protocol simulation; 0 network calls; 0 Registry rows.

- [ ] **Step 5: Commit**

```bash
git add eval/empirical-tranche-1/text_qualification eval/empirical-tranche-1/tests/test_text_qualification.py
git commit -m "eval: implement progressive EMP-001 text qualification"
```

---

### Task 6: Freeze the Four A-TEXT Comparability Items and Stop Rule

**Files:**
- Create: `eval/empirical-tranche-1/atex/atex-items-v1.jsonl`
- Create: `eval/empirical-tranche-1/atex/ATEXT-CONTRACT.md`
- Test: `eval/empirical-tranche-1/tests/test_atex_manifest.py`

**Interfaces:**
- Exactly four frozen prompt/target items, each run twice per slot.
- Primary score is blind transcription + code exact comparison.

- [ ] **Step 1: Freeze these exact targets**

```text
ATEXT-01: शुभ दीपावली
ATEXT-02: आज की डील
ATEXT-03: Aaj ki Deal
ATEXT-04: SAVE 20% • ₹999
```

Each prompt must request a plain 1:1 poster with the target as the **only textual content**, no logo, no product/reference identity and no extra copy. This deliberately isolates text rather than pretending to measure creative quality.

- [ ] **Step 2: Freeze repeat/seed semantics**

Both IMG-01 and IMG-02 use **unseeded repeats** for A-TEXT, even if one route exposes a seed. This makes the first comparison an inherent-variance comparison. Do not later pool it with held-seed evidence.

- [ ] **Step 3: Freeze the hard elimination rule**

A route is eligible for immediate **text-specific deeper-spend stop** if it records **zero exact matches across all scoreable Devanagari/Hinglish A-TEXT opportunities**. State the conclusion only as a result on this frozen screen, not as a universal model incapability.

Any non-zero result is **not promotion**. Full Stage-A survival still requires the rest of the slot's qualified instrument families.

- [ ] **Step 4: Test manifest invariants**

```python
assert len(items) == 4
assert len({x['item_id'] for x in items}) == 4
assert all(x['operation'] == 'generate' for x in items)
assert all(x['extra_text_forbidden'] is True for x in items)
```

- [ ] **Step 5: Commit**

```bash
git add eval/empirical-tranche-1/atex eval/empirical-tranche-1/tests/test_atex_manifest.py
git commit -m "eval: freeze EMP-001 A-TEXT comparability core"
```

---

### Task 7: Implement Gated IMG-01 / IMG-02 Generation Runner

**Files:**
- Create: `eval/empirical-tranche-1/atex/run_atex.py`
- Test: `eval/empirical-tranche-1/tests/test_run_atex.py`

**Interfaces:**
- Consumes only a qualified text-judge record, a positive explicit authorisation file and four frozen A-TEXT items.
- Emits canonical Attempts/Artifacts/Measurements; maximum 16 generation trials.

- [ ] **Step 1: Write gate-order tests**

Verify no generator adapter is invoked when:

1. authorisation is missing/false;
2. no text judge is qualified;
3. preflight is not green;
4. budget guard cannot reserve the next call;
5. a route would exceed its declared 8-generation maximum.

- [ ] **Step 2: Implement generation adapters**

Use exact routes frozen in `config.yaml`:

```text
IMG-01 -> fal openai/gpt-image-2, 1024x1024 medium
IMG-02 -> fal fal-ai/ideogram/v3, BALANCED
```

Each call must create the Attempt record **before** parsing whether an artifact exists. Refusal/error/timeout must remain persisted with no retry.

- [ ] **Step 3: Evaluate generated outputs**

For each artifact:

1. run the qualified judge in `transcribe` shape;
2. compare transcription to target in code;
3. optionally run `verdict` only as a diagnostic measurement if the remaining budget allows it under the frozen evaluator budget allocation;
4. never let `verdict` override a primary transcription mismatch.

- [ ] **Step 4: Verify 16-call maximum with fake adapters**

```bash
pytest -q eval/empirical-tranche-1/tests/test_run_atex.py
python eval/empirical-tranche-1/atex/run_atex.py --dry-run
```

Dry run must emit synthetic records and leave Registry unchanged.

- [ ] **Step 5: Commit**

```bash
git add eval/empirical-tranche-1/atex/run_atex.py eval/empirical-tranche-1/tests/test_run_atex.py
git commit -m "eval: add gated EMP-001 A-TEXT runner"
```

---

### Task 8: Full Zero-Spend Verification Before Requesting/Consuming Money

**Files:**
- Create: `eval/empirical-tranche-1/VERIFICATION-PRE-SPEND.md`
- Modify only after evidence exists: `eval/empirical-tranche-1/README.md`

**Interfaces:**
- Produces a single pre-spend gate record. No provider secrets or live responses committed.

- [ ] **Step 1: Run all EMP-001 tests**

```bash
pytest -q eval/empirical-tranche-1/tests
```

Required: 0 failures.

- [ ] **Step 2: Run inherited harness verification**

```bash
python eval/v1/harness/run_selftest.py
bash eval/v1/harness/run_cross_branch_validation.sh
```

Required: both exit 0.

- [ ] **Step 3: Run tranche dry-run with network disabled**

```bash
python eval/empirical-tranche-1/preflight.py --dry-run
python eval/empirical-tranche-1/text_qualification/qualify_text.py --dry-run
python eval/empirical-tranche-1/atex/run_atex.py --dry-run
```

Required: 0 live calls, 0 empirical Registry rows, 0 budget consumed.

- [ ] **Step 4: Verify protected baselines byte-for-byte**

Compare V1 capability contract, V1 100-item bank and frozen Devanagari validation artifacts against their pre-EMP-001 SHAs. Any difference is a hard block.

- [ ] **Step 5: Write verification record and commit**

Record exact commands, exits and hashes in `VERIFICATION-PRE-SPEND.md`. Do not write “passed” from expectation; copy the fresh outputs.

```bash
git add eval/empirical-tranche-1/VERIFICATION-PRE-SPEND.md eval/empirical-tranche-1/README.md
git commit -m "eval: verify EMP-001 pre-spend gate"
```

---

### Task 9: Paid Execution — ONLY AFTER EXPLICIT USER APPROVAL

**Files:**
- Runtime-only authorisation file: `eval/empirical-tranche-1/authorization.local.yaml` (gitignored)
- Runtime outputs: `eval/runs/tranche-1/<run-id>/`
- Registry: through harness promotion only, never manual edit.

**Interfaces:**
- Consumes explicit approval for `max_consumed_api_spend_usd: 10.00`.
- Produces qualification evidence first; image generation only if qualification succeeds.

- [ ] **Step 1: Materialise local authorisation from the user's exact approval**

```yaml
authorised: true
tranche_id: EMP-001
max_consumed_api_spend_usd: 10.00
retries_authorised: 0
```

Do not infer approval from “continue,” prior research budgets, existing credits or account balances.

- [ ] **Step 2: Run Q2a Devanagari qualification**

Both checker candidates start. A candidate failing the frozen gate stops before Latin.

- [ ] **Step 3: Run Q2b Latin for Q2a survivors only**

If no candidate survives both scripts, stop EMP-001. Run zero image generations.

- [ ] **Step 4: Run A-TEXT only with a qualified judge**

Run IMG-01 and IMG-02, maximum 8 calls each, no retries.

- [ ] **Step 5: Close the run**

Persist final actual spend, route/version ids, trial counts, refusals/errors/timeouts, exact-match observations and qualification scope. Do not compute customer CpAO.

- [ ] **Step 6: Verify evidence before any Controller conclusion**

Run Resources archive validator and Eval integrity checks against the actual run archive. Only after fresh green verification may the Controller decide whether either route deserves deeper Stage-B text spend.

---

## Self-Review Against the Spec

- **Spend boundary:** implemented as a fail-closed $10 ceiling; no account pre-funding permission is implied.
- **Progressive qualification:** Devanagari first, Latin only for survivors.
- **No research-loop regression:** only the minimum missing Latin pack is built; AV/identity/commercial packs are deferred.
- **Measurement validity:** judge is qualified before generated output is scored; blind transcription is primary.
- **Partial-evidence boundary:** A-TEXT cannot promote a full slot.
- **Persistence:** one provider call = one trial; refusals/errors remain evidence; no retries.
- **Historical protection:** V1 baselines and Devanagari battery stay unchanged.
- **CpAO:** not computed here.
- **No placeholders:** every implementation task names concrete files, commands, interfaces and gates.

## Execution Handoff

This plan is ready for implementation, but **Task 9 remains blocked on explicit user spend approval**. Tasks 1–8 are zero-spend implementation/preflight work and may be executed before that approval.
