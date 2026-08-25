# E4 — Master benchmark bank: coverage report

> **GENERATED FILE — do not hand-edit.** Source: `master-bank-v1.jsonl`.  
> Rebuild: `python3 eval/v1/bank/build_bank.py --build`  
> Validate: `python3 eval/v1/bank/build_bank.py --validate`

**Task:** E4 · **Date:** 26 Aug 2026 · **Status: DESIGN ONLY — 0 items generated, 0 spend.**

## The headline: this bank pays for itself 12.7 times over

| | |
|---|---:|
| Base items (generations) | **100** |
| Atomic / compound | 40 / 60 |
| Capabilities covered | **36 / 36** |
| Total valid measurements | **1,266** |
| **Measurements per generated asset** | **12.7×** |

That multiplier **is** the generate-once rule expressed as a number. Scoring these 100 assets one-metric-per-generation would need **1,266 generations** instead of **100**. At any plausible price that is the difference between a fundable programme and an unfundable one.

It is also why evaluator calls outnumber generations roughly 8:1 in the E2 forecast — that is the intended economics, not an overrun.

## Atomic 40 — causal isolation

Atomic items test **one capability with nothing else in the frame**, so a failure has one candidate cause. They still free-ride the zero-cost operational and delivery checks on the same asset — there is no reason not to.

| Group | Items | Capabilities isolated |
|---|---:|---|
| exact text | 10 | `exact_text_latin`×5, `exact_text_devanagari`×5 |
| count attribute spatial | 6 | `object_count`×2, `attribute_binding`×2, `spatial_relationship`×2 |
| identity reference preservation | 6 | `person_identity`×2, `product_identity`×2, `reference_conditioning`×1, `edit_preservation`×1 |
| anatomy human object | 6 | `anatomy_hands`×3, `human_object_contact`×2, `human_human_interaction`×1 |
| motion camera physics | 6 | `motion_action_quality`×2, `action_adherence`×2, `physics_material_appearance`×2 |
| speech lipsync speaker | 6 | `spoken_language_correctness`×2, `single_speaker_lip_sync`×2, `two_speaker_turn_assignment_and_lip_sync`×1, `audio_video_synchronisation`×1 |
| **Total** | **40** | |

## Compound 60 — one generation, many measurements

Ten commercial scenario families × six difficulty tiers. **Each item's fan-out is derived from the capability contract**, not asserted here: a capability appears only if the contract lists that scenario in its `compound_reuse` *and* the capability applies to that modality. A still image is never allowed to claim a temporal measurement.

| Scenario family | Modality | Items | Fan-out | Measurements |
|---|---|---:|---:|---:|
| Typography-led commercial image | `image` | 6 | **14** | 84 |
| Product packshot | `image` | 6 | **19** | 114 |
| Person + product static ad | `image` | 6 | **22** | 132 |
| Reference-based campaign edit | `editing` | 6 | **10** | 60 |
| Product-hero video, external VO or no speech | `video` | 6 | **16** | 96 |
| Actor + product, external VO, no visible dialogue | `video` | 6 | **15** | 90 |
| One visible speaker | `native_av` | 6 | **13** | 78 |
| Two-person dialogue | `native_av` | 6 | **15** | 90 |
| Product handoff / action sequence | `video` | 6 | **16** | 96 |
| Multi-shot branded ad, 6-20 seconds | `video` | 6 | **31** | 186 |

**Read the fan-out column as value per generation.** A multi-shot branded ad is the most expensive asset to generate and returns the most measurements; a packshot is cheap and returns fewer. Both are needed — the cheap ones isolate, the expensive ones integrate.

## Coverage of the 20 critical capabilities

Target: **≥10 distinct base-item opportunities** each.

| Capability | Atomic | Compound | **Total** | ≥10? |
|---|---:|---:|---:|:--:|
| `exact_text_devanagari` | 5 | 24 | **29** | ✅ |
| `exact_text_latin` | 5 | 24 | **29** | ✅ |
| `logo_wordmark_fidelity` | 0 | 30 | **30** | ✅ |
| `person_identity` | 2 | 30 | **32** | ✅ |
| `product_identity` | 2 | 36 | **38** | ✅ |
| `reference_conditioning` | 1 | 24 | **25** | ✅ |
| `object_count` | 2 | 24 | **26** | ✅ |
| `attribute_binding` | 2 | 24 | **26** | ✅ |
| `spatial_relationship` | 2 | 30 | **32** | ✅ |
| `anatomy_hands` | 3 | 36 | **39** | ✅ |
| `human_object_contact` | 2 | 24 | **26** | ✅ |
| `person_stability_in_clip` | 0 | 30 | **30** | ✅ |
| `product_stability_in_clip` | 0 | 24 | **24** | ✅ |
| `text_logo_stability_in_clip` | 0 | 18 | **18** | ✅ |
| `multi_shot_spatial_continuity` | 0 | 18 | **18** | ✅ |
| `spoken_language_correctness` | 2 | 12 | **14** | ✅ |
| `single_speaker_lip_sync` | 2 | 12 | **14** | ✅ |
| `two_speaker_turn_assignment_and_lip_sync` | 1 | 6 | **7** | ⚠️ |
| `audio_video_synchronisation` | 1 | 24 | **25** | ✅ |
| `delivery_format_compliance` | 40 | 60 | **100** | ✅ |

**19 of 20 critical capabilities meet the target.**

### The one that does not, and why it was not padded

**`two_speaker_turn_assignment_and_lip_sync` — 7 opportunities, not 10.**

- **Exact denominator:** 7 = 1 atomic + 6 compound.
- **Why it cannot reach 10:** it is only meaningful where two visible speakers exchange turns, which requires a modality of `lipsync` or `native_av`. 1 scenario family qualifies (`two_person_dialogue`), giving 6 compound opportunities at six items each.
- **Listed but excluded by modality:** `multi_shot_branded_ad` is modality `video`. The contract permits the reuse, but the scenario as defined has no visible on-camera dialogue, so the capability cannot be exhibited. **This is a real design choice worth the Controller's attention:** if a multi-shot branded ad should contain on-camera dialogue, its modality should be `native_av`, which would raise this capability to 13 opportunities and change nothing else. Left as-is tonight because changing a scenario's modality alters the frozen compound-60 design.
- **What was deliberately not done:** adding two-speaker items to scenarios that do not have two visible speakers. That would manufacture opportunities that cannot exhibit the failure, inflating the denominator while measuring nothing. The runbook requires recording the real denominator instead, and that is what this row does.
- **If the Controller wants 10:** the honest route is to widen the two-person dialogue family from 6 items to 10, which is a scope change to the frozen 60 and therefore a Controller decision, not a worker one.

## Full coverage, all 36

| Capability | Opportunities | Critical |
|---|---:|:--:|
| `delivery_format_compliance` | 100 | ● |
| `reliability_pass_at_k` | 100 |  |
| `cost_and_cpao` | 100 |  |
| `latency_errors_refusals` | 100 |  |
| `reproducibility_repairability` | 100 |  |
| `anatomy_hands` | 39 | ● |
| `product_identity` | 38 | ● |
| `spatial_relationship` | 32 | ● |
| `person_identity` | 32 | ● |
| `logo_wordmark_fidelity` | 30 | ● |
| `person_stability_in_clip` | 30 | ● |
| `proposition_objective_fit` | 30 |  |
| `hierarchy_product_as_hero` | 30 |  |
| `composition_brand_register` | 30 |  |
| `exact_text_latin` | 29 | ● |
| `exact_text_devanagari` | 29 | ● |
| `object_count` | 26 | ● |
| `attribute_binding` | 26 | ● |
| `action_adherence` | 26 |  |
| `human_object_contact` | 26 | ● |
| `motion_action_quality` | 26 |  |
| `physics_material_appearance` | 26 |  |
| `reference_conditioning` | 25 | ● |
| `audio_video_synchronisation` | 25 | ● |
| `packaging_brand_colour_fidelity` | 24 |  |
| `product_stability_in_clip` | 24 | ● |
| `hook_pacing_temporal_hierarchy` | 24 |  |
| `edit_preservation` | 19 |  |
| `human_human_interaction` | 19 |  |
| `typography_legibility` | 18 |  |
| `text_logo_stability_in_clip` | 18 | ● |
| `multi_shot_spatial_continuity` | 18 | ● |
| `spoken_language_correctness` | 14 | ● |
| `single_speaker_lip_sync` | 14 | ● |
| `emotional_prosodic_fit` | 12 |  |
| `two_speaker_turn_assignment_and_lip_sync` | 7 | ● |

**Capabilities with zero opportunities: 0** — none. Every one of the 36 is exercised by at least one base item.

## Rules this bank enforces

**Repeats are never base items.** Repeats measure reliability. Two repeats of 50 items is not 100 items, and confidence is computed on base items only.

**Reuse never creates independent trials.** One asset scored by twelve instruments is twelve measurements of **one** trial. Frames sampled from one clip carry the parent trial id.

**The later 12 end-to-end production briefs are NOT in this bank.** They must be selected from Canon's accepted 30-brief bank after integration. These 60 compound items are *capability benchmark scenarios* under controlled conditions — deliberately not customer briefs, and Eval must not author competing ones.

