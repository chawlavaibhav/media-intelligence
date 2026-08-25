# E2 — Pre-run cost forecast

**Task:** E2 · **Date:** 26 Aug 2026 · **Branch:** `work/eval-v1-overnight`
**Status: STRUCTURE COMPLETE · PRICES UNRESOLVED · AUTHORISES NO SPEND**

---

## The one-paragraph version

We now know **exactly how many paid calls the first two empirical waves would
make** — 204 for the admission screen and 520 for deep qualification, plus about
**8,000 evaluator calls** riding on top of those same outputs. What we could
**not** obtain in this cloud session is **what any of them cost**, because this
session's network policy blocks essentially every official provider pricing
page. Rather than guess, the forecast has been built as a calculator with every
price cell empty. Fill in the prices and it produces the totals immediately.

**No money has been spent and none is authorised by this document.**

---

## What is settled, and what is not

| | State |
|---|---|
| How many generation calls each wave makes | ✅ **Settled** — 204 and 520, verified against the runbook's own hard maxima |
| How many evaluator calls those trigger | ✅ **Computed** — but the per-asset fan-out is Eval's **estimate**, not a measurement |
| What each call costs | ❌ **Unresolved** — 9 price cells empty |
| Human verification cost | ❌ **Unresolved** — and expected to be the largest line |
| Total forecast | ❌ **Cannot be produced** without the above |

---

## Verified call counts

These are arithmetic over the Controller's frozen caps, and the calculator
checks its own totals against the maxima stated in the runbook.

### Admission screen (E7) — every endpoint gets the same shallow screen

| Lane | Endpoints (max) | Items each | Outputs |
|---|---:|---:|---:|
| Image | 4 | 12 | 48 |
| General video | 5 | 12 | 60 |
| Native audio-video | 4 | 12 | 48 |
| Lip-sync | 3 | 8 | 24 |
| TTS | 3 | 8 | 24 |
| **Total** | **19** | | **204** |

### Deep qualification (E8) — only the top ≤2 per lane

| Lane | Workflows | Items | Repeats | Outputs |
|---|---:|---:|---:|---:|
| Image | 2 | 40 | 2 | 160 |
| General video | 2 | 30 | 2 | 120 |
| Native audio-video | 2 | 36 | 2 | 144 |
| Lip-sync | 2 | 12 | 2 | 48 |
| TTS | 2 | 12 | 2 | 48 |
| **Total** | | | | **520** |

**Retries are not in these numbers.** They are budgeted separately and must be
predeclared. Discovering a retry allowance mid-run is a budget change and a
money stop, not an adjustment.

---

## The number that will surprise you: evaluator calls exceed generations ~8:1

| Wave | Generations | VLM calls | OCR calls | ASR calls | Local/deterministic |
|---|---:|---:|---:|---:|---:|
| Admission | 204 | 492 | 696 | 24 | 792 |
| Deep qualification | 520 | 1,320 | 1,744 | 48 | 2,016 |

**This is the generate-once rule working, not a problem.** One generated asset
is inspected by several evaluators, so evaluator volume *should* exceed
generation volume — that is precisely how we avoid regenerating the same asset
once per metric. Video multiplies it further because text-stability checks
transcribe several sampled frames from a single clip.

**But it has a hard consequence for budgeting:** evaluator cost is not a
rounding error and must never be folded into generation cost. At roughly one
rupee per vision-model check — the figure recorded in our own prior findings —
evaluation can exceed a third of the true cost of observing a cheap generation.
The forecast keeps the two lines apart for exactly this reason.

⚠️ The per-asset fan-out counts are an **Eval design estimate**, labelled
`ESTIMATE_NOT_MEASURED`. They will firm up once E4's fan-out map and E5's
harness are exercised.

---

## Why there are no prices in this document

E2's research rule is that **official provider documentation only** establishes
model identity, availability and price; secondary sources are leads and never
final evidence. This session cannot reach those pages.

- **22** official provider domains probed → **1** reachable (`cloud.google.com`)
- That one returns HTTP 200 but its pricing tables are JavaScript-rendered;
  two fetch attempts returned **no extractable pricing table**
- Web search works, but returned **reseller blogs and cost calculators** — the
  exact category the rule excludes

**The tempting shortcut was rejected deliberately.** Prices could have been
written from the assistant's training data. They were not, and here is the
concrete reason rather than a principle: a search lead indicated that legacy
`veo-3.0-generate-001` endpoints were shut down on **30 June 2026** — *after*
the assistant's May 2026 training cutoff. In this market, remembered prices and
even remembered model *identities* go stale faster than the gap between that
cutoff and today. A remembered price inside a document that gates a real budget
decision is invented evidence, however plausible it looks.

---

## How to finish this in under an hour

All the design work around the prices is done. What remains is a lookup.

1. Copy `eval/v1/prices-TEMPLATE.yaml` to `eval/v1/prices-<date>.yaml`.
2. Fill each cell from the **official** pricing page, recording `source_url`,
   `read_date`, `model_api_id` and `billing_unit`. Normalise to one unit per
   lane (per image, per clip, per transformation, per read).
3. Add the human-verification line — hours × rate, including first-language
   reader time.
4. Run:

```bash
python3 eval/v1/cost_forecast.py --prices eval/v1/prices-<date>.yaml
```

The calculator **fails closed**: an unresolved cell yields `null`, never `0`,
and it refuses to total a partially-resolved forecast rather than quietly
under-reporting a budget. Both behaviours are covered by its self-test.

```bash
python3 eval/v1/cost_forecast.py --selftest   # run in this session: PASS
```

---

## Three rules the forecast enforces, carried from prior evidence

**Human checking, not API spend, is likely to dominate.** Our original cost
model omitted it entirely. It is a separate top-level line here. Any ratio
quoted before we have measured it is an illustrative scenario, not a finding.

**Evaluator cost is not hidden inside generation cost.** Two separate lines,
always.

**The zero-pass rule.** When an endpoint never passes, cost-per-pass is `null`
— never infinity, never a large sentinel — and the cell cost goes into a
lower-bound field. *"Never observed to pass in N trials"* and *"expensive per
pass"* are different facts about the world, and a router must be able to tell
them apart.
