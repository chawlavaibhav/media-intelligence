# Round two of stills - sizing note (plan only) - 2026-09-09

**Status:** PLAN. No call, no spend, no authorisation implied. Sources: `eval/experiments/EVAL-040/runs/img-r1/RESULTS.yaml`,
`runs/half2/RESULTS.yaml`, the IMG cells of `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml` (generated 2026-09-09 13:38Z),
unit prices from `STAGE-A-FREEZE-2026-09/COST-TABLE.yaml` `route_catalogue.unit_price`, INR at 95.4 per USD (the rate given).

## 1. What round one left standing

"Survivor" = a (route, question) cell the map does not mark `eliminated` under ELIMINATION-RULES E1/E2 (E2: accepts <= floor(0.25 n)).
Round-one n is 2-8 trials per cell over 1-4 items; every 95 % Clopper-Pearson interval is 0.52-0.97 wide, so round one ranks, it does not measure.

| Question | Survivors (accepts/trials, USD per call) | Eliminated in round one |
|---|---|---|
| IMG-CORE | flux-2-pro 5/8 (0.03), gpt-image-2 7/8 (0.053), nano-banana-2 7/8 (0.067), nano-banana-pro 4/8 (0.134), qwen-image-3 7/8 (0.04), seedream-5-pro 6/8 (0.0675) | none |
| IMG-TEXT | flux-2-pro + code overlay 4/4 (0.03 plate + USD 0), gpt-image-2 4/4 (0.053), nano-banana-2 4/4 (0.067), nano-banana-pro 4/4 (0.134); qwen-image-3 2/4 (0.04), recraft-v4 2/4 (0.04), seedream-5-pro 2/4 (0.0675) | flux-2-pro native text 1/4 |
| IMG-EDIT | flux-2-pro-edit 3/4 (0.045), seedream-5-pro-edit 2/4 (0.0675) | nano-banana-pro-edit 1/4 |
| IMG-EXT | seedream-5-pro-edit 2/2 (0.0675) | flux-2-pro-edit 0/2, nano-banana-pro-edit 0/2 |
| IMG-REF | seedream-5-pro-edit 4/4 (0.0675) | flux-2-pro-edit 0/4, nano-banana-pro-edit 1/4 |
| IMG-COMP | flux-2-pro-edit 1/2 (0.045), nano-banana-pro-edit 1/2 (0.15), seedream-5-pro-edit 2/2 (0.0675) | none (n = 2 decides nothing) |

Routing rule RR-3 already says avoid seedream / recraft / flux for Devanagari: recraft-v4 and seedream-5-pro failed only the Hindi case
(IMG-TEXT-01 0/2 each) and passed English (IMG-TEXT-02 2/2 each); qwen-image-3 split 1/2 on each. Round two keeps all three on the English case only.

## 2. The n that measures

Target: a 95 % Clopper-Pearson interval narrower than +-15 points, i.e. total width < 0.30 (exact binomial, `registry_gate.clopper_pearson`).

| True rate p | n = 24 | n = 32 | n = 40 | n = 48 |
|---|---|---|---|---|
| 0.50 (worst case) | 0.42 | 0.36 | 0.32 | **0.295** |
| 0.75 | 0.37 | 0.32 | **0.285** | 0.26 |
| 0.875 (the 7/8 routes) | **0.297** | 0.26 | 0.23 | 0.21 |

So **n = 48 trials per (route, question)** guarantees the target whatever the rate; **n = 24** already meets it for a route that
really sits near 7/8, and n = 40 for one near 3/4. That is the cheap-first shape: 24 first, top up only where the interval is still wide.

Two caveats the interval does not remove. (a) The Registry computes uncertainty over base ITEMS, not trials, and independence is NOT
ESTABLISHED: 24 trials as 4 items x 6 repeats measure four briefs, not "the route". Round two should reach its n mostly through NEW
items (target 8 items x 3 repeats = 24; 12 x 4 = 48), which needs 4-8 new blueprints per question written and frozen before any call.
(b) The intervals are on the Controller's blind verdicts; the VLM screen (qualify_screen.py) is `screened_not_qualified` and cannot
substitute for the judging load: the 444 blind verdicts of stage 1 are the real cost of this round.

## 3. Cost at the pinned unit prices

| Stage | What | Calls | USD | INR (95.4) |
|---|---|---|---|---|
| 1 | n = 24 on every survivor: IMG-CORE 6 routes (9.40), IMG-TEXT 4 routes (6.82) + 3 routes x 12 English-only (1.77), IMG-EDIT 2 (2.70), IMG-EXT 1 (1.62), IMG-REF 1 (1.62), IMG-COMP 3 (6.30) | 444 | **30.22** | **2,883** |
| 2 | top-up +24 only where stage 1 is likely to leave width > 0.30 (rates near 0.5-0.75): IMG-CORE flux / nano-banana-pro / seedream (5.56), IMG-EDIT both (2.70), IMG-COMP all three (6.30) | 192 | 14.56 | 1,389 |
| 1+2 | | 636 | **44.78** | **4,272** |
| ref | n = 48 on everything (no staging; the 3 English-only routes stay at 24) | 888 | 60.44 | 5,766 |

Not in the table: input fixtures (already sealed, USD 0), the code overlay (USD 0), Sarvam / video (not this round), and the VLM
screen (its Gemini API price is not pinned; the runner prints "price not pinned" and refuses to run).

Price basis flags. nano-banana-2 / nano-banana-pro prices are the Vertex pins in COST-TABLE; by the 2026-09-09 decision they now run
on the Gemini Developer API, whose pricing page is not yet pinned - re-price the Nano Banana calls (96 in stage 1, 120 with stage 2) once
it is. gpt-image-2 / flux-2-pro are fal cash prices (Azure credits only if the Controller deploys them).

## 4. Recommendation

**Cheap-first cap: USD 45 (INR 4,293)**, released in two pieces: **USD 30 (INR 2,862) for stage 1**, the remaining USD 15 for stage 2
only after the stage-1 intervals are read. Order inside stage 1: the 0.03-0.04 routes first (flux, qwen, recraft), then gpt-image-2 /
seedream, the Nano Banana pair last (on the GOOGLE_API_KEY account per the 2026-09-09 decision; price unpinned until the page is).
Stop rule per cell: once its interval is narrower than 0.30, stop.
Preconditions before the first call: new blueprints frozen in TEST-CASES (item count, not repeats, is what moves the Registry interval);
the Gemini API price pinned for the Nano Banana rows; an `authorization.*.local.yaml` with these caps signed by the Controller.
