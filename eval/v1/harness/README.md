# E5 — Generate-once evaluation harness

**Status: IMPLEMENTED AND EXECUTED IN THIS CLOUD SESSION.**
38/38 verification checks pass — see [`VERIFICATION-LOG.md`](VERIFICATION-LOG.md).
**0 network calls · 0 model calls · ₹0 spend · 0 Registry rows.**

---

## What it is for

One sentence: **so that a later paid wave never regenerates an asset merely
because a second evaluator wants to look at it.**

```
frozen item manifest
    → ONE generation/transform call
    → immutable output artifact + provenance
    → evaluator fan-out by eligible capability
    → measurements (many per asset)
    → failure co-occurrence
    → operational metrics
    → Registry rows (only from qualified instruments)
```

## The vocabulary that carries the design

| Term | Meaning |
|---|---|
| **Item** | A frozen benchmark specification from the E4 bank. Not media. |
| **Attempt** | One call to a provider. Every call is a new attempt, always. |
| **Asset** | One artifact from one attempt. **This is the trial.** |
| **Measurement** | One evaluator's verdict about one asset, for one capability. |

> **One asset is one trial, however many evaluators inspect it.**

Twelve measurements of one asset are twelve measurements of **one** trial. Frames
sampled from a clip carry their parent's trial id and add **no** trials. Repeats
measure reliability and are never base items. Getting this wrong silently
multiplies apparent confidence — the most expensive statistical error available
to this project, and one it has already made twice.

## The nine invariants, and what each prevents

| # | Invariant | Prevents |
|---|---|---|
| 1 | Exactly one provenance record per asset | An asset whose origin is ambiguous |
| 2 | Many measurements may point at one asset | Regenerating per metric |
| 3 | A retry is a new attempt, never a replacement | Silently overwriting evidence |
| 4 | Frames keep the parent trial id | Inflating trial counts by sampling |
| 5 | Every Registry row names an exact instrument configuration | A number without its judge |
| 6 | Absence distinguishes five reasons | "Could not measure" reading as "passed" |
| 7 | Generation, transform and evaluator costs stay separate | Hiding a third of true cost |
| 8 | No routing score or weight is computed | Eval doing the Planner's job |
| 9 | Registry starts and stays empty of empirical rows | Fake evidence |

## It fails closed

A prior harness defect in this project was *a run that raised integrity errors
and still exited successfully*. So every violation raises `HarnessError` and the
caller cannot proceed. Verified refusals include:

- regenerating an item+config that already has an asset;
- writing a Registry row from an unqualified instrument;
- writing a Registry row from **synthetic** measurements — even when the
  instrument *is* qualified;
- writing a Registry row from an empty measurement set (*an empty check is not a
  passing check*);
- an `absent` verdict with no machine-readable reason;
- a verdict outside the permitted vocabulary;
- scoring a capability outside the item's declared fan-out;
- using an instrument outside its qualified judgement family.

## Measured in the self-test

| Observation | Value |
|---|---|
| Evaluators scoring one video asset | **4 instruments, 12 measurements, 1 generation** |
| Measurements per trial asset | **12.0×** |
| 4 sampled frames added | **0 new trials** (6 assets, 2 trials) |
| Registry rows produced | **0** |
| Paid calls | **0** |

## Files

| File | Purpose |
|---|---|
| `models.py` | Provenance, Measurement, RegistryRow; absence reasons; qualification statuses |
| `harness.py` | The orchestrator and every invariant check |
| `adapters.py` | Dummy generators and evaluators, including deliberately broken ones |
| `run_selftest.py` | The six required demonstrations + harness negative controls |
| `out-selftest/` | Artifact manifest, measurements, operational metrics, co-occurrence |

## Relationship to the existing harness

`eval/harness/run-fixture.mjs` (EVAL-002) is **not modified**. It remains valid
and its `--selftest` still pins the historical checker-judgement equivalence.
This is a new, additive component for the V1 programme; no prior evidence is
touched or invalidated.
