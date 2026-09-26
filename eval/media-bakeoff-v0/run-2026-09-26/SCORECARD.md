# Bake-off scorecard

Pairs judged: 43 of 45; no preference given: E03 B vs A (repeat), E10 B vs A
Rulings: side-check pairs excluded from A's would-pay; ties count against the per-class rule.

| comparison | wins | losses | ties | win rate (non-tie) | sign-test p |
|---|---|---|---|---|---|
| C vs A | 4 | 7 | 1 | 36% | 0.887 |
| B vs A | 4 | 5 | 2 | 44% | 0.746 |
| C vs B | 4 | 6 | 2 | 40% | 0.828 |
| A_MAI vs A | 3 | 1 | 1 | 75% | 0.312 |

| arm | would pay | mean cost/round US$ (comparable) | mean machine time s (includes queue waits) | top 'no' reasons |
|---|---|---|---|---|
| A | 11/23 (48%) | 4.01 | 331 | Identity drift ×4, Off-brief ×4, Audio or voice ×2 |
| A_MAI | – | 0.20 | 339 |  |
| B | 14/24 (58%) | 5.02 | 587 | Audio or voice ×3, Identity drift ×2, Not an ad / boring ×2 |
| C | 9/24 (38%) | 4.81 | 730 | Off-brief ×4, Not an ad / boring ×3, Artefact (hands, morph) ×3 |

Founder consistency on swapped repeats: 33%

## By class (wins / losses / ties)

- **C vs A:** F1_story_film 1/3/0; M1_animate 1/0/1; M2_product_film 0/1/0; S1_product_ad 1/3/0; S2_edit 1/0/0
- **B vs A:** F1_story_film 2/1/0; M1_animate 0/1/1; M2_product_film 0/0/1; S1_product_ad 1/3/0; S2_edit 1/0/0
- **C vs B:** F1_story_film 1/3/0; M1_animate 1/1/0; M2_product_film 0/0/1; S1_product_ad 2/1/1; S2_edit 0/1/0
- **A_MAI vs A:** S1_product_ad 2/1/1; S2_edit 1/0/0

## Pre-registered decisions (START-HERE.md §5, TEST-FLOWS.md §6)

- F1_story_film: B vs A 2/1 (ties 0) -> ship the pipeline
- M1_animate: B vs A 0/1 (ties 1) -> ship A + our finishing
- M2_product_film: B vs A 0/0 (ties 1) -> ship A + our finishing
- S1_product_ad: B vs A 1/3 (ties 0) -> ship A + our finishing
- S2_edit: B vs A 1/0 (ties 0) -> ship the pipeline
- Golden benchmark via B: B vs A 4/5 (ties 2), would-pay B 58% vs A 48% -> does not clearly beat LLM+model
- Golden benchmark via C: C vs A 4/7 (ties 1), would-pay C 38% vs A 48% -> does not clearly beat LLM+model
- Canon: C vs B 4/6 (ties 2) -> NOT in writer context
- Side check, image model: MAI-Image-2.6 vs Nano Banana 2 (same prompts) 3/1 (ties 1) -> MAI preferred (directional, n small)
- Side check would-pay (not used in the main benchmark): A 4/5, A_MAI 5/5
- Cost rule: B mean US$5.02 per round vs A US$4.01 (1.25x; rule <= 1.5x) -> within
- Cost rule: C mean US$4.81 per round vs A US$4.01 (1.20x; rule <= 1.5x) -> within