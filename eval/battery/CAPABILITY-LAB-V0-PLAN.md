# Capability Lab V0 — research plan and schema

**Date:** 23 Aug 2026 · **Parallel workstream to the Canon. Independent of it.**

**Rule:** model capability is never inferred from craft literature. The Canon says *what
capabilities a job requires*. The Lab measures *which current workflows have them*. Only the
Registry may answer the second question.

This document defines the **research plan and the schema**. It deliberately does **not** invent a
supposedly exhaustive benchmark from first principles — that was named as a failure mode and the
battery must be derived from evidence.

---

## Where the battery comes from

Four inputs, in priority order. None alone is sufficient.

**1 · Published benchmarks — borrow methodology, don't reinvent.**
Established image and video generation benchmarks already decompose capability into tested
dimensions. Their **taxonomies and protocols** are the starting point; their scores are not our
answer, because they do not test our conditions. Candidates to review are listed in
[EVAL-CORPUS-PLAN](EVAL-CORPUS-PLAN.md).

**2 · Real production requirements.** Derived from Creative IR fields that carry hard constraints:
identity invariants, exact copy, script system, entity counts, relationships, temporal continuity,
duration, aspect ratio, spoken language.

**3 · Vendor claims — as an admission suite, never at face value.** When a model claims strength in
multilingual text, identity preservation or motion, that claim becomes a targeted test *first*.
Promising results escalate to deeper testing.

**4 · Observed production failures.** We already hold real ones: 10 human-scored failures in
`spike/out/scores.json`, the Devanagari corruption from Finding 01, and identity drift across a
character set. These become permanent regression cases — the layer that gets more valuable with
time, because they are ours and nobody else has them.

**Sequence:** review published taxonomies → intersect with our Creative IR requirements → add our
observed failures → cut to what V0 can afford.

---

## Dimensions to measure

Named because our IR requires them. **Not claimed exhaustive.**

| Dimension | Why it is on our list | Difficulty ladder |
|---|---|---|
| Exact text — Latin | `copy.headline.exactness` | word → line → paragraph → in-scene signage |
| **Exact text — Devanagari** | `audience.language`, our market | word → line → in-scene → in motion |
| Identity preservation — product | `entities.invariants` | frontal static → rotated → held → occluded → in motion |
| Identity preservation — person | `entities.invariants` | single frame → across prompts → across shots → across sessions |
| Reference conditioning | how identity is achieved at all | one ref → multiple refs → ref + style change |
| Composition control | `static.composition`, `creative.hierarchy` | placement → relations → depth → count + relations |
| Object count & relations | prompt adherence | 2 objects → 5 → counted + spatially related |
| Human-object interaction | `relationships` (holding, using) | touching → holding → manipulating → rotating |
| Temporal consistency | `video.continuity_requirements` | background → identity → text → lighting |
| Motion & physics | `video.temporal_structure` | camera move → subject walk → object motion → interaction |
| Speech & lip sync | `video.dialogue_intent` | English → Hindi → emotional → two-speaker |
| Logo & brand mark fidelity | `brand.logo.exactness` | flat placement → on surface → in perspective → in motion |
| Operational behaviour | routing inputs | cost · latency · failure rate · rate limits · moderation · reproducibility |

Two of these — Devanagari exactness and person identity across shots — are where **we already have
observed failures**, which makes them the cheapest to start with and the most load-bearing for the
product.

---

## Registry schema

```yaml
entry_id: cap_0031
vendor: fal
model: bytedance/seedream
version: v4.5
endpoint: text-to-image
workflow: single_call          # single_call | i2v | keyframe_chain | ref_conditioned | composite

dimension: exact_text_devanagari
difficulty_level: 2            # per that dimension's ladder
conditions:                    # what was held fixed
  resolution: 1600x900
  aspect_ratio: "16:9"
  script: devanagari
  string_length_words: 4

result:
  trials: 20
  passes: 3
  pass_rate: 0.15
  failure_types:               # observed, in the observer's words, per SPEC-05 Layer 1
    - {term: "character substitution", n: 12}
    - {term: "gibberish", n: 5}
  instrument: qwen3-vl-235b    # WHICH checker produced this verdict
  instrument_calibration_ref: FINDINGS-01
  human_verified_subset: 5

cost:
  usd_per_call: 0.03
  usd_per_pass: 0.20           # the number that actually matters
latency_p50_s: 14
reliability:
  api_error_rate: 0.02
  moderation_block_rate: 0.00

tested_date: 2026-08-23
sample_source: lab             # lab | production
production_observations: 0
freshness: current             # current | ageing | stale
```

**Three fields exist because of things we already learned.**

`instrument` and `instrument_calibration_ref` — Finding 01 showed one VLM scored 14/14 and another
produced six false passes on the same material. **A capability number without its instrument is
meaningless.**

`usd_per_pass` alongside `usd_per_call` — cost per accepted outcome is the objective, and a cheap
model that fails four times in five is not cheap.

`freshness` — confidence decays. A six-month-old entry for a model that has shipped two versions
is not evidence.

---

## V0 scope

**Three workflows**, chosen because we have prior observations on all three and their failure
profiles already look different:

| Workflow | Prior observation |
|---|---|
| nano-banana-pro (edit / ref-conditioned) | 7 failures in 32 — identity drift, wardrobe change, floating logo |
| seedream v4.5 | 3 failures in 32 — text corruption, prompt leakage, missing wordmark |
| Wan / Veo image-to-video | Devanagari corruption **that drifts within a single clip** |

**Four dimensions for V0**, not thirteen: exact text Devanagari, person identity across prompts,
composition placement and count, and operational cost/latency/reliability. Levels 1–3 only.

Rough shape: 3 workflows × 4 dimensions × 3 levels × 20 trials ≈ 720 generations. At observed
spike pricing (~$0.15 per nano edit) that is a real but bounded number, and it should be costed
before committing rather than assumed.

## Cadence

New serious model → admission suite. Promising → targeted deep tests. Before production routing →
full qualification. Monthly → regression on active models. Quarterly → full battery. Event-driven →
customer failure spike, suspected provider change, vendor announcement.

## What V0 must not do

Benchmark live during a customer request. Trust a vendor claim. Report a capability without naming
its instrument. Infer any capability from a book. Treat a published benchmark's score as our answer.

## Open questions for review

1. Which published taxonomies to adopt, and which to adapt — needs the corpus review first.
2. Devanagari ground truth requires a Hindi reader; Finding 01 flagged that neither prior reader
   was a native speaker.
3. Whether `usd_per_pass` should be the Registry's primary sort key.
4. How freshness decays — linear, by version count, or by observed drift.
