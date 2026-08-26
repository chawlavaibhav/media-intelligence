# E5 — Generate-once evaluation harness

**Status: IMPLEMENTED AND EXECUTED IN THIS CLOUD SESSION.**
**95/95** verification checks pass, and the emitted archive passes **Resources'
own validator, cross-branch, exit 0** — see
[`VERIFICATION-LOG.md`](VERIFICATION-LOG.md).
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
| **Trial** | **One provider call.** Corrected in EI-C2. |
| **Artifact** | Bytes from an attempt. An attempt may produce none. |
| **Measurement** | One evaluator's verdict about one artifact, for one capability. |

> **One call is one trial, however many evaluators inspect its bytes.**

**Why the trial moved (EI-C2).** It used to be the root *asset*. That meant a
call producing nothing had no trial at all, so a refusal silently left the
denominator. Anchoring the trial to the **call** keeps every refused, errored
and timed-out call countable — which is what reliability and cost both need.
Every repeat and every retry is its own trial; derived media adds artifacts,
never trials.

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
| 3b | **Experimental repeats and production retries are separate** (E-C4) | A repeat counted as a retry inflates the failure rate; a retry counted as a repeat hides real CpAO cost |
| 4 | Frames keep the parent trial id | Inflating trial counts by sampling |
| 5 | Every Registry row names an exact instrument configuration | A number without its judge |
| 6 | Absence distinguishes five reasons | "Could not measure" reading as "passed" |
| 7 | Generation, transform and evaluator costs stay separate | Hiding a third of true cost |
| 8 | No routing score or weight is computed | Eval doing the Planner's job |
| 9 | Registry starts and stays empty of empirical rows | Fake evidence |
| 10 | **A Registry row is ONE coherent cell** (E-C5) | An average across two models or two instruments that describes nothing |
| 11 | **No synthetic promotion bypass exists** (E-C6) | Dummy data becoming evidence via a call option |
| 12 | **The canonical four-record handoff is Resources'** (E-C7) | Two competing persistent schemas |

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
| `run_selftest.py` | The required demonstrations + harness negative controls |
| `out-selftest/` | `attempts` / `artifacts` / `measurements` / `acceptances` + derived views |

## Cross-branch validation (EI-C8)

```bash
bash eval/v1/harness/run_cross_branch_validation.sh
```

Runs **Resources' own** `check_empirical_archive.py` from a worktree of their
branch against the archive this harness emits. The validator is invoked, never
copied — a local copy would drift, and Eval would then be proving compliance
against a stale snapshot of somebody else's contract.

Exit **0** valid · **1** schema violation · **2** could not check. *"I found no
problem"* and *"I could not look"* never share an exit code.

## Storage handoff (E-C7 / EI-C1–C5)

Resources owns the durable storage contract; Eval owns measurement semantics.
The harness emits the canonical **four** records and keeps **no competing
persistent manifest**:

| Record | Rule |
|---|---|
| **Attempt** | Written because the call was *made*. Refusals, errors and timeouts survive as their own records **with no artifact**. |
| **Artifact** | Bytes from an attempt. Derived frames point to their parent and add **no** trial. |
| **Measurement** | Many per artifact. Canonical observation units only. |
| **Acceptance** | **Always empty here.** Eval does not decide acceptance; inventing one would manufacture the numerator of CpAO. |

## Relationship to the existing harness

`eval/harness/run-fixture.mjs` (EVAL-002) is **not modified**. It remains valid
and its `--selftest` still pins the historical checker-judgement equivalence.
This is a new, additive component for the V1 programme; no prior evidence is
touched or invalidated.
