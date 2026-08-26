# E7-F — Provisional call / cost forecast

**Task:** EVAL-007 · **Date:** 26 Aug 2026
**Status: STRUCTURE COMPUTED · PRICES UNRESOLVED · AUTHORISES NO SPEND**

Calculator: [`provisional_forecast.py`](provisional_forecast.py) — self-test **PASS**, run in session.

---

## One paragraph

The proposed benchmark-v2 wave would make **360 generation calls** and trigger roughly **3,960
evaluator calls**. What it would **cost is unknown**, because E7-B probed 22 official provider
documentation domains and evidenced **zero prices**. The forecast is therefore built as a calculator
with every price cell empty, and it **refuses to produce a total** rather than under-report a budget.

---

## Call counts — computed, and self-checked

| Tier | Items | Repeats | Trials |
|---|---:|---:|---:|
| 1 — atomic probes | 40 | 2 | **80** |
| 2 — compound scenarios | 60 | 2 | **120** |
| 3 — condition sweeps | 80 derived | 2 | **160** |
| **Total generations** | | | **360** |

**Tier 3 reuses tier-2 items rather than adding new ones**: 20 compound items × 4 swept conditions ×
1 additional level. That is the sparse-sweep decision from E7-D made concrete — a cartesian product
over all 11 conditions would be 2,048 cells before a model is considered.

⚠️ **No adaptive saving is claimed.** The adaptive rule (don't sweep the next level where the
previous already failed) will reduce this in practice, but by an amount that depends on results we do
not have. Claiming a saving now would be forecasting a discount on evidence that does not exist.
`adaptive_saving_assumed: 0.0`.

## Evaluator calls — again outnumbering generations

| Instrument | Calls |
|---|---:|
| Structured visual VLM | 1,080 |
| Text / OCR | 1,080 |
| ASR | 360 |
| Deterministic (local) | 1,440 |
| **Total** | **3,960** |

**~11 evaluator calls per generation.** That is the generate-once rule working, not an overrun — and
it is why evaluator cost is a separate top-level line and must never be folded into generation cost.

⚠️ The per-asset fan-out remains `ESTIMATE_NOT_MEASURED`, unchanged in status from E2.

---

## Why there are no prices

**E7-B probed 22 official provider documentation domains across all five lanes plus aggregators.
One was reachable; zero yielded a model id or a price.**

The single reachable domain (`cloud.google.com`) redirects its model and pricing documentation to
`docs.cloud.google.com`, which is blocked, and the two pages that do render return truncated
JavaScript-dependent content with no pricing table. Three separate Google pages were attempted.

**Prices were not written from memory, and not from search.** Search returns reseller blogs and cost
calculators — permitted as leads, forbidden as evidence. Model identities and prices in this market
change faster than the gap between the assistant's training cutoff and today.

**9 price cells remain unresolved** (5 generation lanes + 4 evaluator classes).

---

## The one external cost datapoint worth recording

DreamBench++ upgraded from DINO/CLIP-I to an MLLM judge for better human alignment, at a reported
**~20,000 judge API calls and >$400 per model evaluated**.

*(INDICATIVE — from a search summary, not a first-party page. Re-verify before it informs an approved
budget.)*

Even as an indicative figure it makes a structural point: **in the current field, upgrading an
evaluator to something humans agree with has a price comparable to the generation itself.** Our
family-3 (visual VLM) qualification is the most likely place for that cost to land, and it should be
budgeted as a real line rather than assumed cheap.

---

## Fail-closed behaviour, verified

```
python3 eval/research/pre-e7-macro/provisional_forecast.py --selftest
tier1 80 / tier2 120 / tier3 160 / total 360 ..................... OK
unresolved prices produce null totals, not 0 .................... OK
partially-resolved forecast refuses to total .................... OK
fully-resolved total 360.0 (expect 360.0) ....................... OK
SELFTEST PASS
```

A **partially** resolved forecast refuses to total. Filling in three of nine cells and reporting the
sum of those three would produce a number that looks like a budget and is a third of one.

---

## Three rules this forecast keeps

**Human verification is a separate line and is expected to dominate.** No approved rate exists, so it
stays null.

**Evaluator cost never hides inside generation cost.** Two lines, always.

**The zero-pass rule.** When an endpoint never passes, cost-per-pass is `null` — never infinity,
never a sentinel. *"Never observed to pass in N trials"* and *"expensive per pass"* are different
facts about the world.
