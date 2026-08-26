# E7-C — External audit of the current 36 capabilities

**Task:** EVAL-007 · **Date:** 26 Aug 2026 · **Spend:** ₹0

> **This task does NOT modify the authoritative capability contract.** Everything below is
> an audit finding for the Controller to integrate. No capability was added, removed or
> renamed, and no target count was aimed at.

Evidence: [`benchmark-source-register.yaml`](benchmark-source-register.yaml) · Contract audited: `eval/v1/capability-contract.yaml` @ `work/eval-v1-overnight`

## Summary

| Classification | Count |
|---|---:|
| Externally supported, well scoped | 15 |
| Supported — definition/unit needs refinement | 11 |
| Likely a condition, not a capability | 0 |
| Overlaps another capability | 0 |
| Product-important, weakly evidenced externally | 10 |
| **Total audited** | **36 / 36** |
| Candidate missing capabilities identified | 6 |

**The headline is not alarming and should not be dressed up as such.** Fifteen of 36 capabilities are well scoped against current external practice. Eleven need a definition or observation-unit refinement — most of them small. Ten are product-important with weak external evidence, which mostly means *nobody has built that benchmark*, not that we are wrong to want it.

### Two categories came back empty, and that is a finding

E7-C offered six classifications. **No capability was classified `likely a condition rather than a capability`, and none as `overlaps another capability`.** I did not skip these — I looked for both and did not find them:

- The pairs most likely to overlap are separated deliberately and correctly in the contract: `action_adherence` (did it happen) vs `motion_action_quality` (does it look plausible); `person_identity` at `asset_set_over_time` vs `person_stability_in_clip` at `sequence`. Different units, different failures.

- **One genuine subtlety:** `delivery_format_compliance` carries aspect ratio, resolution and duration — and those same three appear in E7-D as *conditions*. That is a real dual role, not a mistake: the requested format is a **condition** of every other measurement, and whether the model honoured it is a **capability**. Worth stating so the Planner never conflates them.

The empty categories are reported rather than filled. Forcing a capability into a category to make the audit look thorough would be the opposite of an audit.


---

## Capability-by-capability

### A constraint fidelity

**`object_count`** — Externally supported, well scoped

- *External evidence:* GenEval and T2I-CompBench both isolate counting as its own dimension judged by a detector (Mask2Former / UniDet). Our definition, unit and instrument family all match external practice.
- *Action:* None. Keep as is.

**`attribute_binding`** — Externally supported, well scoped

- *External evidence:* GenEval names colour attribution; T2I-CompBench devotes three of its six categories to attribute binding (colour, shape, texture) judged by BLIP-VQA. Both report it as a MAJOR current failure mode - GenEval quotes model scores of 0.00-0.35.
- *Action:* Consider whether shape and texture deserve to be distinguishable inside the failure vocabulary; external practice splits them and we do not.

**`spatial_relationship`** — Supported — definition/unit needs refinement

- *External evidence:* Strongly supported - both GenEval and T2I-CompBench test it, and GenEval reports position as the WORST dimension (0.03-0.15). BUT T2I-CompBench separates 2D-spatial from 3D-spatial and judges them differently.
- *Action:* REFINE. We merge 2D and 3D into one capability while our own contract already states depth ordering 'is NOT decidable from 2D boxes'. We documented the split and then did not make it. A 2D relation is deterministic from boxes; a depth relation is not. They are different instruments and probably different capabilities.

**`action_adherence`** — Externally supported, well scoped

- *External evidence:* VBench has human_action; VBench-2.0 adds motion order understanding and human interaction. Our sequence observation unit matches - an action is a temporal object.
- *Action:* None to the definition. See sequence/state continuity under missing capabilities.

**`delivery_format_compliance`** — Externally supported, well scoped

- *External evidence:* Not a research benchmark dimension because it is trivially deterministic - which is exactly why it is ours to keep. No external work needed to justify a file probe.
- *Action:* None. It is the cheapest true measurement we have.

### B text brand

**`exact_text_latin`** — Product-important, weakly evidenced externally

- *External evidence:* Compositional T2I benchmarks do not test exact glyph-level string rendering; they test objects, attributes, relations and counts. Text rendering is a known weakness discussed in the field but no reachable benchmark isolates exact-string fidelity as we define it.
- *Action:* Keep. Build our own pack, as already planned. Absence of an external benchmark is not evidence the capability does not matter - it means the instrument is ours to build.

**`exact_text_devanagari`** — Product-important, weakly evidenced externally

- *External evidence:* Same as Latin, and more so: no reachable benchmark covers generative Devanagari exactness. Our 96-item validated battery appears to be ahead of the reachable public state of practice for this specific judgement.
- *Action:* Keep. Note the standing envelope limit: the battery perturbs REAL characters and cannot produce malformed generated glyphs.

**`typography_legibility`** — Supported — definition/unit needs refinement

- *External evidence:* VBench's imaging_quality is adjacent but is general image quality, not legibility at delivery size. No external benchmark found for legibility as a delivery-size property.
- *Action:* REFINE. Legibility depends on DELIVERY SIZE, which is a CONDITION, not a property of the asset. Today the condition is buried in the definition. It should be an explicit condition so two legibility measurements are comparable only at the same declared size.

**`logo_wordmark_fidelity`** — Product-important, weakly evidenced externally

- *External evidence:* NO benchmark found on reachable surfaces for brand-mark fidelity under perspective or curvature. The external world does not appear to have solved this either.
- *Action:* Keep, and stop expecting an off-the-shelf instrument. Our contract already records required_but_no_calibrated_instrument; this audit confirms that is not an oversight.

**`packaging_brand_colour_fidelity`** — Supported — definition/unit needs refinement

- *External evidence:* Colour is heavily tested externally (GenEval colours, T2I-CompBench colour binding) but as CATEGORICAL colour ('is it red'), not as tolerance against a declared brand value.
- *Action:* REFINE. External colour evidence does NOT transfer: naming a colour and matching a brand specification within tolerance are different judgements. Ours is the harder one and needs its own tolerance, declared before any run.

### C identity references

**`person_identity`** — Supported — definition/unit needs refinement

- *External evidence:* Strongly supported: DreamBench's whole purpose, plus VBench subject_consistency and VBench-2.0's separate Human Identity and Human Clothes dimensions.
- *Action:* REFINE on TWO counts. (1) VBench-2.0 splits identity from CLOTHES; we fold wardrobe into person_identity, which means a right face in wrong wardrobe and a wrong face are the same verdict. (2) DreamBench's DINO metric 'may risk overfitting identity-irrelevant information' - external corroboration that decoys are mandatory.

**`product_identity`** — Externally supported, well scoped

- *External evidence:* DreamBench covers subject-driven object identity directly (21 of its 30 subjects are objects). Our asset_set_over_time unit matches its multi-generation protocol.
- *Action:* None to the definition. The decoy requirement (ADD-01) is now externally corroborated and should be treated as a hard precondition, not a nice-to-have.

**`reference_conditioning`** — Externally supported, well scoped

- *External evidence:* The entire subject-driven personalisation literature is about this mechanism. Keeping it separate from the identity OUTCOME is well founded - one is the mechanism, one is the result.
- *Action:* None.

**`edit_preservation`** — Externally supported, well scoped

- *External evidence:* Adjacent to instruction-guided editing evaluation. Our formulation - deterministic masked diff outside the declared edit region against OUR OWN input - is stronger than a similarity score because the input is ours.
- *Action:* None. This is one of our better-designed capabilities.

### D human physical realism

**`anatomy_hands`** — Supported — definition/unit needs refinement

- *External evidence:* VBench-2.0 names Human Anatomy as a dimension in its Human Fidelity group, so the property is externally recognised.
- *Action:* REFINE the NAME and scope. Ours says 'hands'; the external dimension is anatomy generally (limbs, joints, faces). Our own failure vocabulary already includes extra_limb, joint_inversion and facial_feature_misplaced - so the name is narrower than the capability and invites under-testing of everything that is not a hand.

**`human_object_contact`** — Product-important, weakly evidenced externally

- *External evidence:* VBench-2.0 has Human Interaction but that is human-human. No reachable benchmark isolates human-object contact plausibility.
- *Action:* Keep - it is commercially central (a person holding the product IS the shot). Accept that the instrument is ours to build and remains uncalibrated.

**`human_human_interaction`** — Externally supported, well scoped

- *External evidence:* VBench-2.0 names Human Interaction explicitly.
- *Action:* None.

**`motion_action_quality`** — Externally supported, well scoped

- *External evidence:* VBench covers motion_smoothness and dynamic_degree; VBench-2.0 adds Motion Rationality. Our descriptive_only routing is well judged - the external dimension is a quality judgement, not a pass/fail gate.
- *Action:* None. Note VBench separates SMOOTHNESS from AMOUNT of motion (dynamic_degree): a frozen video scores perfectly on smoothness. Our failure vocabulary should keep frame_freeze prominent for exactly that reason.

**`physics_material_appearance`** — Supported — definition/unit needs refinement

- *External evidence:* VBench-2.0 has a whole Physics group (mechanics, thermotics, material, multi-view consistency), so the property is real and current.
- *Action:* REFINE scope DOWNWARD, deliberately. Their group is a research frontier. Our product needs commercial plausibility for 6-20s media, not physical correctness. Adopting their dimensions would import scope we cannot act on - but MULTI-VIEW CONSISTENCY is worth extracting, see missing capabilities.

### E temporal continuity

**`person_stability_in_clip`** — Externally supported, well scoped

- *External evidence:* VBench subject_consistency is exactly this; VBench-2.0 adds Instance Preservation.
- *Action:* None.

**`product_stability_in_clip`** — Externally supported, well scoped

- *External evidence:* Same external support as person stability, applied to objects.
- *Action:* None.

**`text_logo_stability_in_clip`** — Product-important, weakly evidenced externally

- *External evidence:* VBench has temporal_flickering and subject_consistency but nothing specific to rendered TEXT mutating across frames. This is a failure we have OBSERVED in our own prior evidence.
- *Action:* Keep. Our own observed-failure evidence is stronger here than anything external, and this is a legitimate case of leading rather than following.

**`multi_shot_spatial_continuity`** — Supported — definition/unit needs refinement

- *External evidence:* VBench-2.0's Multi-View Consistency and Motion Order Understanding both address cross-view and cross-time coherence, and go beyond what we cover.
- *Action:* REFINE - our name and definition are too narrow. 'Spatial' continuity captures screen direction and geometry. It does NOT capture STATE continuity (the box is open in shot 2 because it was opened in shot 1) or ORDER. Our own difficulty ladder already has a product-state example at level 5, so the capability is being asked to carry something its name excludes.

### F speech audio

**`spoken_language_correctness`** — Supported — definition/unit needs refinement

- *External evidence:* TTS evaluation measures intelligibility via ASR word error rate and speaker similarity via ASV. IndicVoices-R provides an Indic-specific benchmark surface (22 languages, CC-BY-4.0).
- *Action:* REFINE - this capability currently merges TWO judgements that the external field keeps apart: WORD correctness (machine-comparable via ASR) and PRONUNCIATION acceptability (needs a first-language listener). A robust ASR normalises a mispronunciation into the correct word, so one instrument cannot answer both.

**`single_speaker_lip_sync`** — Supported — definition/unit needs refinement

- *External evidence:* Externally standard (LSE-C/LSE-D) BUT the standard metrics are contested: comparative work reports only LSE-O shows moderate effectiveness.
- *Action:* REFINE the INSTRUMENT expectation, not the capability. The capability is right; the obvious off-the-shelf metric is not trustworthy as a gate. Budget for building/qualifying rather than adopting.

**`two_speaker_turn_assignment_and_lip_sync`** — Product-important, weakly evidenced externally

- *External evidence:* Talking-head evaluation is overwhelmingly single-speaker. No reachable benchmark covers turn assignment across two visible speakers.
- *Action:* Keep. Turn boundaries remain the field that makes wrong assignment machine-detectable.

**`emotional_prosodic_fit`** — Supported — definition/unit needs refinement

- *External evidence:* TTSDS evaluates prosody (pitch, speaking rate) as a measurable factor against reference speech, which is more tractable than our current framing.
- *Action:* REFINE toward DISCRIMINATION, which we already proposed: can the requested register be told apart and correctly identified. TTSDS shows prosody has measurable correlates, so this need not be purely preference-shaped.

**`audio_video_synchronisation`** — Externally supported, well scoped

- *External evidence:* Distinct from lip-sync in the literature (global A/V offset vs viseme correspondence), which matches our separation.
- *Action:* None. Our split of global offset from mouth-shape correspondence matches external practice.

### G commercial creative

**`proposition_objective_fit`** — Product-important, weakly evidenced externally

- *External evidence:* HPSv2 and preference models measure general human preference, NOT whether a stated commercial proposition was conveyed. No external benchmark found for brief satisfaction.
- *Action:* Keep as descriptive_only. HPSv2's own limits - same-prompt comparison only - are external evidence that preference cannot gate.

**`hierarchy_product_as_hero`** — Product-important, weakly evidenced externally

- *External evidence:* No external benchmark found. Canon owns the craft definition.
- *Action:* Keep, descriptive_only. Partially instrumentable (relative area, centrality, contrast of the declared hero region) and those computable components should be recorded separately from the judgement.

**`composition_brand_register`** — Product-important, weakly evidenced externally

- *External evidence:* VBench's aesthetic_quality is the nearest external analogue and is a LEARNED TASTE PROXY trained on community preference - explicitly not brand register.
- *Action:* Keep, descriptive_only. Do NOT adopt an aesthetic predictor as a proxy; it would answer a different question confidently.

**`hook_pacing_temporal_hierarchy`** — Product-important, weakly evidenced externally

- *External evidence:* VBench has temporal_style; VBench-2.0 has Complex Plot. Neither is advertising pacing.
- *Action:* Keep, descriptive_only. Structural correlates (shot boundary timings, first product appearance, first text appearance) are computable and reproducible even though the judgement is not.

### H operational

**`reliability_pass_at_k`** — Externally supported, well scoped

- *External evidence:* Standard practice across generative evaluation. Our rule that confidence is computed on independent base items is the part most often got wrong elsewhere.
- *Action:* None.

**`cost_and_cpao`** — Externally supported, well scoped

- *External evidence:* Externally corroborated in an unexpected way: DreamBench++ reports its MLLM-judge upgrade costs roughly 20,000 API calls and >$400 per model evaluated. EVALUATOR cost is a first-order budget line in the field, not just in our model.
- *Action:* None to the definition. Treat the DreamBench++ figure as INDICATIVE pending re-verification.

**`latency_errors_refusals`** — Externally supported, well scoped

- *External evidence:* Operational, not a research dimension. Ours to own.
- *Action:* None.

**`reproducibility_repairability`** — Supported — definition/unit needs refinement

- *External evidence:* Seed/reproducibility control is an interface property providers expose or do not. Repair has no external benchmark.
- *Action:* REFINE - this merges two things with different natures. Repeat agreement is measurable now. REPAIR requires a repair loop that does not exist, and repair attempts are additional generations. They are already flagged in our own envelope note; the audit confirms the split is real.


---

## Candidate missing capabilities

Each was reached from external evidence, not from a wish list. **None is proposed for adoption in this task** — they are candidates for the Controller's integration decision, and several may resolve as refinements of existing capabilities rather than new ones.

| Candidate | Strength | Basis |
|---|---|---|
| `camera_framing_instruction_fidelity` | **STRONG** | VBench-2.0 names Camera Motion as its own controllable dimension. Providers expose camera/motion controls as first-class API parameters. Our 36 has NO… |
| `sequence_state_continuity` | **STRONG** | VBench-2.0's Motion Order Understanding. Our multi_shot_spatial_continuity covers geometry and screen direction, not whether ordered state changes per… |
| `technical_visual_integrity` | **STRONG** | VBench measures temporal_flickering and imaging_quality; these are TRANSIENT CORRUPTION properties - flicker, warping, sudden softness - that are not… |
| `cross_asset_identity_consistency` | **MODERATE** | Our person_identity uses asset_set_over_time so it is arguably covered, but VBench-2.0 separates identity from clothes, and campaign work needs N asse… |
| `style_reference_fidelity` | **MODERATE** | VBench has appearance_style and temporal_style. Providers expose style-reference inputs. We have reference_conditioning (mechanism) and composition_br… |
| `pronunciation_intelligibility_as_distinct_from_word_correctness` | **STRONG** | TTS evaluation separates ASR-WER intelligibility from speaker similarity and prosody. Our spoken_language_correctness merges word correctness with pro… |

### `camera_framing_instruction_fidelity`

**Why it surfaced:** VBench-2.0 names Camera Motion as its own controllable dimension. Providers expose camera/motion controls as first-class API parameters. Our 36 has NO capability for whether a requested camera move or framing was delivered.

**Strength of the case:** STRONG - external benchmark dimension AND an API surface. If a workflow accepts a camera instruction, whether it honoured it is measurable and routing-relevant.

### `sequence_state_continuity`

**Why it surfaced:** VBench-2.0's Motion Order Understanding. Our multi_shot_spatial_continuity covers geometry and screen direction, not whether ordered state changes persist (opened box stays open).

**Strength of the case:** STRONG - and our own difficulty ladder already smuggles a state-continuity example into a capability whose name excludes it.

### `technical_visual_integrity`

**Why it surfaced:** VBench measures temporal_flickering and imaging_quality; these are TRANSIENT CORRUPTION properties - flicker, warping, sudden softness - that are not identity drift, not motion quality and not anatomy. Our 36 has no home for them.

**Strength of the case:** STRONG - three of VBench's sixteen dimensions are in this space, and a customer notices flicker immediately.

### `cross_asset_identity_consistency`

**Why it surfaced:** Our person_identity uses asset_set_over_time so it is arguably covered, but VBench-2.0 separates identity from clothes, and campaign work needs N assets to look like ONE campaign.

**Strength of the case:** MODERATE - may be a refinement of person_identity plus a genuinely new campaign-level capability rather than one new dimension. No external benchmark found for campaign consistency.

### `style_reference_fidelity`

**Why it surfaced:** VBench has appearance_style and temporal_style. Providers expose style-reference inputs. We have reference_conditioning (mechanism) and composition_brand_register (judgement) but nothing for whether a supplied STYLE reference was followed.

**Strength of the case:** MODERATE - externally recognised and commercially real for campaign look, but overlaps our existing reference_conditioning and should not be added without resolving that overlap.

### `pronunciation_intelligibility_as_distinct_from_word_correctness`

**Why it surfaced:** TTS evaluation separates ASR-WER intelligibility from speaker similarity and prosody. Our spoken_language_correctness merges word correctness with pronunciation acceptability.

**Strength of the case:** STRONG - and it is the same trap as the founding Devanagari failure in a different medium: a robust ASR silently corrects a mispronunciation exactly as a vision checker silently corrected a misspelling.


---

## The eight questions E7-C required me to inspect explicitly

| Question | Finding |
|---|---|
| Exact spoken-script/content fidelity | **Merged today.** `spoken_language_correctness` carries both word correctness and pronunciation acceptability. External TTS practice keeps them apart (ASR-WER vs listener judgement). Splitting is the single clearest refinement in this audit. |
| Camera/framing instruction fidelity | **Missing.** VBench-2.0 names Camera Motion; providers expose camera controls as API parameters. We have no capability for it. |
| Cross-shot / cross-asset identity consistency | **Partly covered.** `person_identity` uses `asset_set_over_time`. But VBench-2.0 separates identity from *clothes*, and campaign-level consistency has no home. |
| Sequence/state continuity beyond left-right | **Missing.** VBench-2.0's Motion Order Understanding. Our own level-5 ladder example already assumes state continuity under a capability whose name is *spatial*. |
| Technical visual integrity (flicker, corruption, warping, softness) | **Missing.** Three of VBench's sixteen dimensions live here. Nothing in our 36 does. |
| Pronunciation / intelligibility / voice consistency | **Partly missing.** Intelligibility is inside `spoken_language_correctness`; **voice consistency across assets has no capability at all** — the audio analogue of person identity. |
| Style-reference fidelity | **Candidate, with an overlap to resolve.** VBench has appearance/temporal style. Overlaps `reference_conditioning`; should not be added until that boundary is decided. |
| Campaign/variant consistency | **Missing, and no external benchmark exists.** Commercially real — N assets must read as one campaign — but we would be building the instrument with no external precedent. |

**One observation across all eight.** Five of the eight point at the same structural gap: **we measure single assets well and asset *relationships* poorly.** Camera fidelity, state continuity, cross-asset identity, voice consistency and campaign consistency are all relational. Our strongest unit coverage is `frame` (13 capabilities); our weakest is `shot_pair` (1). That imbalance is the most actionable finding in this audit.

