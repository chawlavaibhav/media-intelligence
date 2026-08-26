# v2.1 → v3 compatibility and migration semantics

**Task:** R4-B · **Date:** 26 Aug 2026 · **Branch:** `work/res-004-production-readiness`
**Authoritative for pre-v3 archives:** `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` (v2.1)
**Forward contract:** `OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml`
**Enforced by:** `validators/validate_topology_v3.py` gate **G9**, negative control `nc-G9-historical-backfill.yaml`

---

## The one rule everything else follows from

> **v2.1 archives are historical truth. v3 does not migrate them, rewrite them, or reinterpret them.
> A v3 reader ingests a v2.1 archive without mutating a single source record.**

v3 is a **forward** contract for records written from now on. There is no migration script and there
should never be one, because every migration of this kind is an opportunity to invent provenance that
was never recorded — which is the exact failure this whole contract exists to prevent.

## What v2.1 recorded, and what it did not

v2.1 models `attempt → artifact → measurement`, plus acceptance. It is complete and correct **for what
it covers**. What it never recorded, because the concepts did not exist:

| v3 concept | Present in v2.1? |
|---|---|
| `job` / customer request | **no** |
| `outcome` / customer deliverable | **no** |
| `sequence_or_asset_set` | **no** |
| `production_unit` | **no** |
| `production_step` | **no** |
| local deterministic steps | **no** — they had nowhere to live |
| ordered multi-parent artifact lineage | **no** — a single optional parent only |
| customer-level acceptance | **no** — acceptance was trial-level |
| cost classification (api/local/human) | **no** |
| request lineage | **no** |

## The null state: `not_recorded_pre_v3`

Every v3 field with no v2.1 counterpart takes the explicit sentinel **`not_recorded_pre_v3`** — never
`null` silently, never a guess, never a default that reads as a real value.

```yaml
# A v2.1 attempt read by a v3 reader
attempt_id: att-abc123          # from the source record, unchanged
trial_id:   trial-abc123        # from the source record, unchanged
step_id:    not_recorded_pre_v3 # v2.1 had no production steps
outcome_id: not_recorded_pre_v3 # v2.1 had no outcomes
```

**Why a sentinel rather than null:** `null` is ambiguous — it can mean "recorded as absent" or "never
recorded at all", and those are different facts. A reader that cannot tell them apart will eventually
treat one as the other.

## Four prohibitions, each mechanically enforced

**1. No invented outcome or job context.** A pre-v3 archive must not acquire jobs, outcomes, sets or
units. Gate **G9** fails an archive declaring `schema_era: v2.1` while asserting any of them.

**2. No historical trial acceptance promoted to customer-outcome acceptance.** v2.1 acceptance rows
are **trial-level and diagnostic**. They map to `unit_acceptance`, never to `outcome_acceptance` — **no
v2.1 archive ever recorded whether a customer accepted anything.** Promoting them would fabricate a
CpAO denominator out of internal pass/fail judgements and make historical work look commercially
validated when it was not.

**3. No historical record mutated.** A v3 reader may *project* a v2.1 record into v3 shape in memory.
It may not write that projection back. The source archive is append-only and immutable.

**4. No historical CpAO.** Whole-outcome CpAO over v2.1 data is **not computable and must not be
reported**, because v2.1 has no outcomes, no cost classification and no customer acceptance. The
correct answer is `not_computable_pre_v3`, not a number derived from trial-level acceptance.

## What v3 preserves from v2.1, unchanged

The trial-level evidence layer is **identical**. v3 adds levels above `attempt`; it changes nothing at
or below it:

- one provider/API/transform call = one trial;
- `attempt` and `artifact` remain separate entities;
- failed, refused, timed-out and cancelled attempts persist individually with verbatim reasons;
- `repeat_index` ≠ `retry_of_attempt_id`;
- frozen machine vocabularies for `status` and `lane`;
- canonical observation units; capability ids stored verbatim; measurements Eval-owned;
- costs reference immutable ledger entries.

**A v2.1 artifact's `derived_from_artifact_id` is exactly a v3 single-element `parents` list** with
`role: source` and `position: null`. Legacy readers keep working and legacy archives need no rewriting.

## How a v3 reader should ingest a v2.1 archive

1. Read it with the **v2.1** validator (`resources/v1/validators/check_empirical_archive.py`). It is
   still the correct tool for those bytes and it still passes.
2. Project into v3 shape **in memory only**, filling every absent field with `not_recorded_pre_v3`.
3. Mark the projection `schema_era: v2.1` so gate G9 keeps it honest.
4. Map v2.1 acceptance to `unit_acceptance`. **Never** to `outcome_acceptance`.
5. Report whole-outcome CpAO as `not_computable_pre_v3`.
6. **Write nothing back.**

## Mixed archives

A single archive must not mix eras. If a production run spans the transition, write **two archives** —
one `v2.1`, one `v3` — and relate them by reference rather than merging them. A merged archive would
have to answer "was this row recorded or inferred?" for every field, and no schema can answer that
after the fact.

## Verification

`nc-G9-historical-backfill.yaml` takes the fully valid v3 archive and changes exactly one thing —
`schema_era: v2.1` — and the validator rejects it under G9 with a message naming the correct state.
**Executed: 18/18 lineage controls behaved as declared.**
