# Resource requirements matrix — what Canon and Eval actually need from Resources

**Task:** R1 of `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md`
**Date:** 26 Aug 2026 · **Branch:** `work/resources-v1-overnight` · **Status:** complete, cloud-verified

**Source of truth:** `resource-requirements.yaml`. `RESOURCE-REQUIREMENTS-MATRIX.csv` is derived from it
by `validators/build_requirements_matrix.py` and cannot drift; this document explains it.

---

## In one paragraph

Before tonight, "what does Resources need to get?" was answered source by source. This matrix answers it
requirement by requirement. Every one of Eval's 36 capability dimensions, all 6 evaluator families, Canon's
three experiment rows, Eval's benchmark-bank and end-to-end rows, and the regression archive now have an
explicit disposition: does it need media from outside the project, does Eval build it, is what we already
hold enough, or does it need no media at all? **48 rows, no unknowns.** The headline is uncomfortable and
worth stating plainly: **of 36 capabilities, exactly one is fully served by material we already hold.**

---

## What the matrix found

### 1. Only one capability is currently covered

| Capability state | count of 36 | meaning |
|---|---:|---|
| `available` | **1** | Existing material is sufficient. This is `exact_text_devanagari` only. |
| `constructed_by_eval` | **10** | Eval builds the stimulus itself. Resources supplies nothing and should not be asked to. |
| `no_external_resource` | **5** | Measured from the model's own outputs and telemetry. No media at all. |
| `partial` | **3** | Existing material covers part of it; a named remainder is missing. |
| `missing` | **17** | Nothing we hold serves it. |

Read the good news honestly: **15 of 36 capabilities (10 + 5) need nothing from Resources ever.** That is a
real result — it stops a third of the capability map from generating acquisition work. The bad news is the
17 `missing` rows, and they are not scattered. They cluster into four packs.

### 2. Four packs unblock almost everything missing

Counting how many missing/blocked/partial rows each pack appears in:

| Pack | rows it unblocks | target | state |
|---|---:|---|---|
| `PACK-PRODUCT-REF` | **11** | ≥48 images = 12 products × ≥4 views | missing |
| `PACK-PERSON-REF` | **8** | ≥32 images = 8 identities × ≥4 views | missing |
| `PACK-AV-CLEAN` | **7** | 36 clips = 24 single + 12 two-speaker, with transcripts | missing |
| `PACK-COMMERCIAL` | **7** | 80 assets = 40 static + 40 video; 60 active + 20 reserve | missing |

**This is the single most useful number in tonight's work.** Four acquisitions, not seventeen. The product
reference pack alone touches eleven rows — product identity, packaging colour, logo fidelity, reference
conditioning, edit preservation, in-clip product and text stability, the structured-VLM evaluator family,
the compound benchmark bank and the end-to-end production benchmark.

### 3. Where the gaps are concentrated

| Capability group | missing | note |
|---|---:|---|
| F. Speech / audio | **5 of 5** | Completely uncovered. The corpus contains **zero audio**. |
| G. Commercial / creative | **4 of 4** | Completely uncovered. No commercial creative bank exists. |
| C. Identity & references | **4 of 4** | Completely uncovered. Both reference packs missing. |
| E. Temporal / continuity | 3 of 4 | The fourth is partial: perturbation bases exist, content does not. |
| B. Text & brand | 1 of 5 | The best-covered group, because of the Devanagari work. |
| A. Constraint fidelity | 0 of 5 | All deterministic or telemetry-based. |
| D. Human & physical realism | 0 of 5 | All measured on Eval's own generations. |
| H. Operational | 0 of 4 | All telemetry-based. |

Three whole groups are at zero coverage. That is the picture the Controller needs before approving any budget.

### 4. Three evaluator families are blocked, one is fine, two are workable

- **Family 1 (text/OCR) — `available`.** The only instrument family with sufficient material today: the
  existing Devanagari reading pools plus the frozen 96-item exactness battery.
- **Family 2 (deterministic CV geometry) — `constructed_by_eval`.** Needs ≥100 synthetic known-answer
  fixtures. Resources supplies nothing. Recorded explicitly so this is not mistaken for a gap.
- **Family 4 (temporal/video) — `partial`, and partially unblockable now.** Discontinuity, text-instability
  and continuity perturbations can be built on clips we already hold. Identity-drift cases cannot.
- **Families 3 (structured VLM), 5 (speech/AV) and 6 (creative/commercial) — `blocked`**, each on a pack
  that does not exist.

**Why this matters more than it looks.** The project's founding result is that a capability number without a
qualified checker is not a measurement. Three of six instrument families cannot be qualified at all right
now, so any capability that depends on them cannot produce a trustworthy number regardless of which model
is tested or how much is spent on generation.

### 5. Two anti-duplication findings

**One commercial bank, not two.** Eval's creative/commercial evaluator family (`REQ-INS-06`) and Canon's
Experiment B (`REQ-CAN-03`) both need real commercial creative. The plans already say to share; the matrix
makes it structural by pointing both rows at the same 60 active assets. Acquiring two banks would double
the cost *and* make the two results non-comparable.

**One product pack serves five distinct measurements.** Product identity, packaging colour, reference
conditioning, edit preservation and in-clip product stability are five different questions asked of the
same physical objects. Five packs would multiply cost and destroy comparability across the answers.

### 6. Rows that create a Resources obligation without needing any media

Four operational capabilities (`reliability_pass_at_k`, `cost_and_cpao`, `latency_errors_refusals`,
`reproducibility_repairability`) need no media — but they are storage class **C**, irreproducible empirical
output. They are only measurable if the output bytes, the cost reference, the accept/reject outcome and the
exact provider/model/version survive together. **Cost per Accepted Outcome — the project's primary metric —
is recomputable only if Resources' archive holds all four next to each other.** That is why R3/R8's
`EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` is a requirement of the metric, not filing tidiness.

One consequence worth stating: a **refusal produces no output bytes but is still evidence**. The schema
therefore permits a record with a null output hash and a populated API status. Without that, refusals would
silently vanish and reliability would be overstated.

---

## Boundaries Resources held while writing this

- **Counts and capability ids are Eval's**, taken verbatim. Where Resources thinks a target is wrong it is
  written into `resources_note`, never silently changed. (Example: `REQ-CAP-04` `action_adherence` has no
  deterministic checker, so its instrument depends on two blocked families — flagged, not altered.)
- **No creative labels.** For the commercial bank, Resources supplies descriptive axes only — category,
  media type, market/language, duration, platform. Never "this ad is good." Selecting assets by whether
  Canon predicts they are good is precisely the circularity this stream exists to prevent.
- **No thresholds.** Resources supplies clips and known offsets for lip-sync; the millisecond tolerance is
  Eval's to derive from evidence.
- **Source labels stay observations.** Every row using a distributor's labels records them as that
  distributor's observations, not project ground truth.

## How this was verified tonight

`python3 resources/v1/validators/build_requirements_matrix.py` — **executed in this cloud session**, exit 0:

```
[PASS] 36/36 capability rows present
[PASS] 6/6 evaluator-family rows present
[PASS] 48 total requirement rows, all with a state and a reason
```

It also cross-checks that every referenced pack exists and that every pack's `serves` list points at real
requirement ids, so the matrix cannot reference a pack nobody defined.

**Negative controls, also executed tonight** — the tool was run against deliberately broken inputs, because
the project has already paid for the lesson that a check which passes on nothing is not a check:

| Broken input | Result |
|---|---|
| Source YAML missing | `[FAIL]` exit 2, no CSV written |
| Source YAML empty | `[FAIL]` exit 2, no CSV written |
| Source truncated to 3 rows | `[FAIL]` exit 2, no CSV written |
| One capability row deleted (35 of 36) | `[FAIL]` exit 2, no CSV written |

All four fail closed and write nothing. This matters because GOV-001 found an existing Resources script
(`build_reports.py`) that produced a degraded artifact and still exited 0 when its input was absent. **That
defect is untouched here** — fixing it needs a Controller-assigned task — but every new tool in
`resources/v1/` is built to the opposite standard.

## What this does not establish

- It does **not** approve any acquisition. A `missing` row says a named consumer needs something; whether to
  get it is the Controller's call.
- It does **not** claim the four packs are obtainable. R4 researches routes; several have real rights,
  consent or access problems.
- It does **not** verify that existing material is *fit* beyond what committed evidence records. The raw
  media is not available in this cloud session.
