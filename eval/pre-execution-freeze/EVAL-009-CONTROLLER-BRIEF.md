# EVAL-009 — Controller Brief

**Task:** `eval/tasks/EVAL-009-MEASUREMENT-AND-BENCHMARK-FREEZE.md` (E9-A – E9-H)
**Date:** 26 Aug 2026 · **Branch:** `work/eval-009-measurement-freeze` · **Not merged.**

> ## ₹0 · 0 model calls · 0 evaluator calls · 0 Registry rows · 0 instruments qualified
> **V1 is preserved byte-identical:** the 36-capability contract and the 100-item bank are unmodified, and a mechanical gate proves it.

**All 10 mechanical gates PASS. 17 negative fixtures rejected. 6 aggregation semantics proven.**

---

## 1 · Capability Contract v2 — 36 → 44

| | |
|---|---:|
| V1 | **36** |
| V2 total | **44** |
| — active | 43 |
| — dormant | 1 (`repairability`) |

`36 + 4 splits + 4 added = 44`. 22 unchanged · 9 refined · 1 renamed.

**The count is an output, not a target.** V2 is *generated* from V1 by declared dispositions — the build aborts if any V1 id lacks one, so a capability cannot vanish silently.

### The four splits

| V1 | → V2 | Because |
|---|---|---|
| `spatial_relationship` | `_2d` + `_depth` | V1's own contract said depth *"is NOT decidable from 2D boxes"* — the split was documented and never made |
| `spoken_language_correctness` | `spoken_script_correctness` + `pronunciation_intelligibility` | The founding Devanagari trap in a new medium: a robust ASR **normalises a mispronunciation into the correct word** |
| `person_identity` | `person_identity` + `wardrobe_invariant_fidelity` | Right face/wrong wardrobe is usually repairable by re-prompt; wrong face needs a new reference. One verdict cannot carry both |
| `reproducibility_repairability` | `reproducibility` + `repairability` **(dormant)** | Repeat agreement is measurable now; repair needs a loop that does not exist |

### The four additions — each passed the admission bar

> A new capability is admitted **only** where existing capability + condition + observation scope cannot represent the failure cleanly.

- **`camera_framing_fidelity`** — action_adherence asks whether the SUBJECT did what was asked. A camera instruction is about the OBSERVER, not the subject: a push-in can be absent while the subject action is perfect, and no existing …
- **`sequence_state_continuity`** — multi_shot_spatial_continuity covers geometry and screen direction. State continuity is ORDERED and causal - the box is open in shot 2 BECAUSE it was opened in shot 1 - and a spatially perfect pair ca…
- **`technical_visual_integrity`** — Flicker, transient corruption, warping and sudden softness are not identity drift (the subject is still the same person), not motion quality (the motion may be smooth) and not anatomy (the body is cor…
- **`voice_identity_consistency`** — The audio analogue of person_identity, and genuinely absent. spoken_script_correctness checks WHAT was said; pronunciation_intelligibility checks HOW clearly; emotional_prosodic_fit checks register. N…

### Three concepts REJECTED under the same bar

- **`style_reference_fidelity`** — RESOLVED INTO reference_conditioning with reference_type=style. The failure is identical in kind - the supplied reference did not control the output - and only the reference type d…
- **`cross_asset_person_or_product_identity`** — RESOLVED BY OBSERVATION SCOPE. person_identity and product_identity already use asset_set_over_time. Cross-asset is a SCOPE of the same capability, not a different failure. Control…
- **`campaign_variant_set_consistency`** — DEFERRED AS AN OUTCOME-LEVEL CONCEPT, not a capability. It is a property of a DELIVERABLE SET against an acceptance basis, which lives at outcome acceptance rather than per-asset m…

The bar is only credible if it sometimes says no. It did, three times.

---

## 2 · Dependency-aware scoring — the inflation this removes

`blocked_by_prerequisite_failure` is frozen with **`outcome_acceptance: unsatisfied`**.

**The motivating case, proven by fixture:** product absent → logo and brand-colour blocked.

| | Old flat fan-out | V2 dependency-aware |
|---|---|---|
| logo fidelity | **pass** (nothing wrong was visible) | `blocked_by_prerequisite_failure` |
| brand colour | **pass** | `blocked_by_prerequisite_failure` |
| reported score | **0.67** | diagnostic 0.0 |
| outcome | *looked acceptable* | **UNSATISFIED** |

A completely failed asset scored **0.67** and would have out-ranked a near-perfect asset with one real defect. **The inflation was largest exactly where the output was worst.**

The requirement was **not waived** by its ancestor failing — the customer still asked for the logo to be right. That is why it is `unsatisfied`, not `not_applicable`.

---

## 3 · Scientific Wave-1 roster — 12 core + 2 reserve

From **53** EVAL-008 candidates.

| Admission rationales using… | Count |
|---|---:|
| access / credits / availability | **0** |
| leaderboard rank alone | **0** |
| an unverified vendor claim | **0** |

### Rows are slots, not model names

A row is its **question**. A named candidate is a guess at an *instrument*. If EVAL-010 finds one unavailable or mispriced, **the slot survives and an equivalent fills it** — naming models as the unit of science would let a sourcing failure silently delete an empirical question.

| Slot | Question | Tier |
|---|---|---|
| `IMG-01` | Is generated exact Devanagari/Hinglish text viable AT ALL from a frontier general image model, … | core |
| `IMG-02` | Does a typography/text-specialist model outperform a frontier generalist on non-Latin script ex… | core |
| `IMG-03` | Does instruction-driven editing preserve everything it was not asked to change?… | core |
| `IMG-04` | Does a reference-conditioned model hold person AND product identity across a multi-asset set, a… | core |
| `IMG-05` | Does owning the step on open weights change CpAO enough to matter?… | reserve |
| `IMG-06` | Can type be emitted as editable vector output, so a text defect is REPAIRABLE without regenerat… | reserve |
| `VID-01` | Can a frontier video model hold rendered text and logo STABLE across a clip, and produce usable… | core |
| `VID-02` | Does state and identity continuity survive across CUTS, not just within a shot?… | core |
| `VID-03` | Can supplied reference images control identity in generated VIDEO?… | core |
| `VID-04` | Can EXISTING customer footage be edited rather than regenerated?… | core |
| `VID-05` | Where is the cost knee - does the premium tier buy enough additional ACCEPTED outcomes to justi… | core |
| `AUD-01` | Does an India-focused voice model pronounce Hindi, Hinglish code-mixing and Indian brand names … | core |
| `AUD-02` | Does a global frontier voice model match a specialist on Hindi/Hinglish?… | core |
| `AUD-03` | Is TTS + lip-sync a viable production route for Hindi dialogue video, as an alternative to nati… | core |

### The ~99% Hindi/Bengali claim

**Verification attempted:** Direct fetch of the vendor announcement page (EGRESS_BLOCKED) plus a targeted web search for primary evidence and evaluation methodology.

**Result: `NO_PRIMARY_EVIDENCE_FOUND`.** Reseller product pages, a Medium post and marketing summaries. The search itself concluded the results were "primarily marketing claims and general descriptions rather than detailed peer-reviewed primary source documentation of the evaluation methodology".

**Disposition:** not load-bearing anywhere. Instead **converted into the hypothesis IMG-01 tests** — a marketing number becomes a falsifiable prediction rather than a reason to believe.

### Other challenges upheld

- **CHALLENGE-02** — Leaderboard/Elo evidence (gpt-image-2 T2I arena #1 ~1370; reve-2.1 #2 ~1306): INSUFFICIENT ALONE, per Controller. Arena Elo measures aggregate human preference on community prompts - HPSv2 states preference comparison is "only m…
- **CHALLENGE-03** — Vendor geography / training lineage as a differentiator (H_lineage_acceptance): DEMOTED. 'Different national/vendor lineage' is not a concrete failure hypothesis. It was RE-SPECIFIED into something testable and kept only in that f…
- **CHALLENGE-04** — H_clean_rights (marey-realism, licensed-data-only training): DEMOTED OUT OF WAVE 1. Rights-clean training is a procurement/legal property, not a capability our benchmark measures. It would change a purchasing de…
- **CHALLENGE-05** — H_conversational_loop (gemini-omni-flash): DEMOTED TO RESERVE. Multi-turn is explicitly recognised by the Controller as real but NOT solved, with no request-history schema frozen and no block o…
- **CHALLENGE-06** — 27 EVAL-008 entries carrying no hypothesis at all: NOT ADMITTED. Superseded versions and unhypothesised entries were excluded by the admission rule automatically - a row with no question cannot earn a …
- **CHALLENGE-07** — Composite-route arms treated as model rows: RESTRUCTURED. 'Generate image without type, then composite type locally' and 'TTS + lip-sync instead of native AV' are WORKFLOW TOPOLOGY arms, not mod…

---

## 4 · Benchmark v2 Wave 1 and call counts

| | |
|---|---:|
| Base items | **94** (L1 64 + L2 30) |
| Sweep instances | +25 |
| **Generations** | **494** |
| **Evaluator calls** | **5,515** |
| Human review units | 188.0 |
| Requested operations covered | `animate`, `edit`, `generate`, `variants` |

**Not a cartesian product**, by two mechanisms. Slot-targeted item sets: each slot runs only the items bearing on *its* question plus a shared comparability core — the first draft ran everything on everything and was **cut from 943 to 494 generations**. And sparse sweeps: 4 of 13 condition families, on subsets. All 13 at two levels would be **8,192 cells**.

**Layer 4 (end-to-end) is reserved, not invented.** Eval does not author customer briefs — that is how a benchmark starts defining the product instead of the reverse. **Consequence: CpAO is not computable in Wave 1**, because there are no accepted outcomes to divide by.

**Prices are all null.** EVAL-010 owns them; the forecast refuses to total.

**5 reduction levers** are offered with what each *loses*. Recommended if budget forces a cut: defer whole questions (L3, L4), never halve repeats (L1) — that corrupts every remaining number instead.

---

## 5 · Evaluator blockers

**0 instruments qualified.** Of 43 active capabilities:

| Wave-1 measurability | Count |
|---|---:|
| `yes_after_qualification_pack_exists` | 4 |
| `blocked_needs_qualification_material_and_human_reference` | 24 |
| `blocked_needs_qualification` | 7 |
| `yes_deterministic` | 8 |

### The five blockers

- **No qualification pack for the visual VLM family (family 3)** — blocks 12 capabilities. Largest single blocker. Needs person/product reference packs WITH same-category decoys - without decoys the qualification cannot detect permissiveness at all.
- **No AV material of any kind** — blocks 7 capabilities. The project holds no audio. Nothing in family 5 can be qualified or measured.
- **No clean base clips for temporal perturbation** — blocks 9 capabilities. Truth can be INJECTED (known freeze, known identity swap, known flip) so this needs ZERO human labels - only clean clips. Cheapest large unblock available.
- **No Latin exact-text pack** — blocks 1 capabilities. Must be built separately and must NOT mutate the frozen Devanagari battery.
- **No fresh independent reviewer panel for family 6** — blocks 4 capabilities. Public/source preference labels are never our creative truth. Also needs KNOWN-CLEAN assets to measure false criticism.

**Cheapest large unblock:** temporal (9 capabilities) needs **zero human labels** — truth is *injected* (known freeze, known identity swap, known flip). It needs only clean clips.

**Two standard instruments are contested and must not be adopted unexamined:** SyncNet LSE-C/LSE-D for lip-sync, and DINO/CLIP-I for identity (*"may risk overfitting the identity-irrelevant information"*).

---

## 6 · Unresolved Controller decisions

| # | Decision | Consequence if deferred |
|---|---|---|
| 1 | **Freeze Capability Contract v2 (44)?** | Wave 1 cannot be built against a contract that is still a proposal |
| 2 | **Approve the 12-slot core roster, or cut it?** | Any cut must preserve the omitted hypotheses in the record, per your trade-off rule |
| 3 | **Which reduction lever, if budget forces one?** | Defaulting to halving repeats would silently destroy all reliability evidence |
| 4 | **Approve reserve promotion triggers?** | IMG-06 (vector type) promotes only if IMG-01 *and* IMG-02 fail — that rule needs to be live before the wave, not after |
| 5 | **CANON-010 reconciliation** on `requested_operation` vocabulary | Eval's provisional vocabulary is a placeholder; Canon owns request grammar |
| 6 | **Accept that CpAO is not computable in Wave 1?** | Layer 4 depends on Canon's brief bank; pretending otherwise would manufacture the numerator |
| 7 | **Resource packs**: person/product **with same-category decoys**, clean clips, AV material | Without decoys the identity qualification cannot detect permissiveness at all |

---

## 7 · Verification

| Check | Result |
|---|---|
| 10 mechanical gates | **PASS** |
| Negative fixtures | **17/17 rejected** |
| E9-B aggregation semantics | **6/6 hold** |
| V1 36-capability contract modified | **No** |
| V1 100-item bank modified | **No** (100 items, byte-identical) |
| Instruments qualified | **0** |
| Prices populated | **0** |

**Evidence classification.** *SOURCE-SUPPORTED:* Controller decisions, the V1 artifacts, EVAL-007's first-party benchmark register, EVAL-008's candidate universe. *INFERRED:* the slot-targeted design, the redundancy judgements, evaluator fan-out (`ESTIMATE_NOT_MEASURED`). *PROPOSED:* everything in this package — v2, the roster, the benchmark. *UNKNOWN:* every price, every model identity/version, and whether any candidate passes anything.

