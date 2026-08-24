# Local evaluation harness — synthetic fixtures only

**Task:** EVAL-002 · **Status: plumbing validation. Not a benchmark. Not evidence about any model.**

---

## What this is, in plain terms

Before we ever run a real test against a real image generator, we want to know that the *machinery*
works: that a test item can go in one end, be judged, and come out the other end as a result we can
read, aggregate and trust the counting of.

This harness does exactly that, using **fabricated data**. Nothing here contacts a model. Nothing
here looks at a real generated image. Every input was typed by hand for the purpose of exercising
the pipeline.

Think of it as testing a weighing machine with a known 1 kg block before you weigh anything that
matters. It tells you the scale works. It tells you nothing about the thing you eventually weigh.

---

## What it proves

Running `node eval/harness/run-fixture.mjs --all --check` demonstrates that we can:

| Mechanic | Why it matters |
|---|---|
| Load a test item and identify which battery dimension it belongs to | without this, a result cannot be filed against the thing it measured |
| Attach a reference to the generated output being judged | traceability — a number must point back at the artifact it came from |
| Attach a checker result, with the checker's identity, version and trust state | a pass rate is a joint claim about the model *and* the checker; the checker must be named |
| Record pass/fail **plus several defects on one output** | one bad image can be wrong in more than one way; recording only the most obvious defect systematically undercounts |
| Distinguish independent items from repeated attempts | two attempts at one prompt are not two independent tests; confidence must be computed on items |
| Record the observation unit | some defects only exist across frames; a frame-level checker cannot see them at all |
| Treat a many-frame clip as **one** observation | six frames from one clip are one test, not six |
| Carry cost fields without inventing values | every cost is an explicit fixture number or an explicit "not measured" |
| Keep one generation scored on two dimensions from becoming two independent trials | otherwise sharing a generation to save money silently inflates the sample |
| Quarantine a run that fails its own integrity checks | a run with a counting error may not present *any* result as usable |
| Emit both a machine-readable file and a human-readable summary | one for later processing, one for a person to sanity-check |

The text-scoring path calls the **real** judgement function exported by
`eval/scripts/check-vlm.mjs` — not a copy of it — so the harness exercises production code.

---

## What it does NOT prove

- **Nothing about any model's capability.** No generation happened.
- **Nothing about any checker's accuracy.** No calibration happened. The mock checker's verdicts
  were written by hand.
- **Nothing about cost.** The money figures in the fixtures are invented placeholders, clearly
  labelled as such.
- **Nothing about Hindi.** Where Devanagari appears, it is *reused* from strings already recorded in
  `eval/runs/finding-01-devanagari-check/`. No new Hindi content was authored, and no linguistic
  judgement was made.
- **It does not validate the battery design.** It validates that the design can be *represented*.

**The result files in `out/` carry `SYNTHETIC_RESULT: true` and a warning. They must never be copied
into the Capability Registry.**

---

## The result format is implementation-scoped and reversible

The harness writes a local JSON shape so it has something to aggregate. **This is not a schema
decision.** The Capability Registry schema in `eval/battery/CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml`
remains a proposal, and its cross-stream fields remain deferred by the Controller. Nothing here
promotes it. If the Registry format changes, this harness changes with it.

---

## Usage

```
node eval/harness/run-fixture.mjs --all --check       # positive fixtures; exits 0 when clean
node eval/harness/run-fixture.mjs --negative          # negative controls; exits 0 when correctly rejected
node eval/harness/run-fixture.mjs --fixture <f.json>  # one fixture
node eval/harness/run-fixture.mjs --help
```

`--check` compares against the stored `.expected.json` beside each fixture and fails on drift, so an
accidental change to the counting rules is caught rather than silently absorbed.

### The negative controls matter

`fixtures/negative/` contains fixtures that are **deliberately wrong** — one counts a generation as
two independent trials and uses an invalid observation unit; another declares an instrument state
that is not in the approved vocabulary. The harness is expected to reject **each** of them.

This exists because **a check that never fails proves nothing.** Running `--negative` confirms the
guards actually fire rather than merely staying quiet.

**Each fixture is verified individually** (corrected 24 Aug 2026). An earlier version passed when any
error was raised anywhere in the run — which, with two or more negative fixtures, would pass even if
one had been silently *accepted*, because the other's errors covered for it. `--negative` now
requires every fixture to be rejected, and to raise the specific `expected_error_codes` it declares,
so a fixture rejected for the wrong reason also fails.

`--selftest` is regression coverage for that check itself. It pins four cases, including the exact
bug (one fixture rejected, another silently accepted → must FAIL) and an empty suite (→ must FAIL,
since deleting the fixtures should not read as success).

---

## Files

```
run-fixture.mjs                the harness
fixtures/*.json                synthetic inputs
fixtures/*.expected.json       expected aggregates — regression guard for the harness itself
fixtures/negative/             deliberately invalid fixtures the harness must reject
out/                           generated results (synthetic, labelled, safe to delete)
```
