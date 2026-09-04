# Stage A freeze package — September 2026 (EVAL-039A)

**Status:** FROZEN PROPOSAL, USD 0 spent, awaiting the Controller's acceptance and the separate spend record. Nothing here authorises a paid call. Authored by the Executor agent on 2026-09-05 from the committed packs, grammar and source pools only (base `cb92f1e` on `controller/capability-lab-direction-2026-09-05`); no provider, evaluator, OCR or LLM API call was made and no network was used.

## What this package is, in plain English

Before any money is spent on the model screen, every test item must exist the way a real Indian buyer would write it to a studio, be mapped to the frozen request grammar, and be produced under one frozen Canon-shaped production plan, so that comparing routes compares routes and nothing else. This directory is that item set: 35 customer-shaped cases, one frozen blueprint per case, a blind-judgeable acceptance contract per case, the routes and parameters each case runs on, the pre-registered elimination rules, the seed policy, the evaluator fan-out, the argument for why no case can be dropped or merged, and a call-count and cost table split by tranche and billing pool. The spend record the Controller writes in the morning names routes, counts and a cap from this package.

## Package map

| file | what it holds |
|---|---|
| `TEST-CASES.yaml` | the 35 case records (request, source, Normalized Request, capabilities, 13 condition families, reference assets, acceptance contract, blueprint ref + sha256, routes with parameters and billing quantities, downstream reuse, cut rank) — the EVAL-039B interlock file |
| `test-cases/<CASE-ID>.md` | human-readable twin of each record |
| `BLUEPRINTS/<CASE-ID>.blueprint.md` | the frozen production blueprint per case: packs selected by deterministic lookup, decisions cited by `PA-Dn` / `CA-Dn` with the pack's own DEFAULT text rendered by id, text handling, dispatch parameters, the `*-check` lines, and the single generation prompt every route receives |
| `ACCEPTANCE-CONTRACTS.md` | every contract in one place, with the E5 pre-checks |
| `COVERAGE-MATRIX.md` | routing questions → cases, roster questions, §C.3d items, core counts, TOPO arms, freshness items, operation coverage, language mix |
| `ELIMINATION-RULES.md` | E1–E5 byte-identical to plan §C.4, the survivor cap, the Seedance proportional rule |
| `SEED-POLICY.yaml` | per route: seed support (EVAL-010 evidence or `undocumented`), policy `unset` |
| `EVALUATOR-PLAN.yaml` | per case: T-DET / T-BENCH / T-HUMAN / T-SCREEN fan-out; only the 8 deterministic capabilities are Registry-eligible |
| `COST-TABLE.yaml` | route × case × arm rows, calls, indicative unit prices, pool, tranche; totals; evaluator rows; judging minutes |
| `IRREDUCIBILITY.md` | one paragraph per case and the fixed cut order |

## Counts

- Cases: **35** · blueprints: **35** (one per case; `VID-KNEE-01` carries the same production spec as `VID-T2V-04` under its own header).
- Calls: **1a = 186**, **1b = 112**, **total = 298**, plus **32 conditional** (SD3.5 Large 8, MAI-Image-2.6 8, Sora 2 8, Chirp 3 HD 2, Azure Neural TTS 2, Kling v3 elements 4) listed but outside the cap.
- Deviation from the task's fixed counts: none — the counts equal the task's fixed 186 / 112 / 298 + 32.
- Language mix (by the language the customer wrote in): en 15, hi 12, hg 8 → Hindi + Hinglish = 20/35 = 57 %.

| lane | en | hi | hg | total |
|---|---|---|---|---|
| IMG | 5 | 4 | 3 | 12 |
| VID | 7 | 5 | 3 | 15 |
| AUD | 2 | 2 | 2 | 6 |
| MUS | 1 | 1 | 0 | 2 |

- Fixtures (no source pool could supply the shape; each carries its reason in `source.adaptation`): IMG-CORE-04, VID-T2V-03, VID-I2V-04, AUD-LIP-01, AUD-LIP-02, AUD-LIP-03. Three are the policy-edge shape (the Media Factory Veo-refusal scene as still, text-to-video and animate); three are the lip-sync requests, because no pool item supplies a clip plus a voice file to be lip-synced — each consumes two real-demand items (its drive script and its plate).
- **4K is not a case.** 4K recorded as a Stage B COND-DELIVERY level only; round one runs 720p.

## How prices are treated (read this before the cost table)

`eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml` (EVAL-039B) was present when this package was written (the sibling landed it at 02:21 IST; it was absent at the first orientation read). Every route record names the roster record and variant it takes its price and pin from (`roster_route_key`), and `COST-TABLE.yaml` carries a `roster_cross_check` block that the build asserted against the roster's bytes. Each cost row carries a `price_status`:

- `pinned` — the unit price and pin path come from the named roster record (fetched bytes + sha256 in `price-pins-2026-09/PIN-INDEX.yaml`); regular price only, promotions never used;
- `unpinned` — the roster has no projectable price for that path (in the cap's scope: gpt-image-2 edit, pinned only as a token meter with no per-image table, 12 calls; Veo 3.1 Lite image-input, no pinned variant, 2 calls; among the conditionals: MAI-Image-2.6 unpublished, Chirp 3 HD, Kling elements); the line contributes 0, is summed under `unpinned_calls_excluded_from_cap`, and is outside the proposed cap.

Route-level facts (id, surface, pool, status, unit price, pin path, seed support, notes, credit alternatives, billing-quantity rules) live once per route in `route_catalogue` at the top of `TEST-CASES.yaml` and `COST-TABLE.yaml`; each case's `routes[]` row and each cost row carries the `route_key` into that catalogue.

Two roster facts changed this package after its first build: the second lip-sync route now has an id (`fal-ai/kling-video/lipsync/audio-to-video`, pinned), and Veo 3.1 **Fast** has a pinned reference-to-video variant, so VID-REF-* run on Fast (credits) rather than the full tier. The "cheapest pinned image-to-video route" resolves to MiniMax H3 Max i2v at 768p (0.08/s) for TOPO-03 arm C and the VID-2SPK-01 chain, because Veo Lite's image-input path is not pinned. Kling v3 bills 0.168/s with native audio on (0.112/s silent); the text-to-video core and the native dialogue arm use the audio-on price.

### Nominal projection (indicative, USD; Sarvam in INR)

| tranche | pool | calls | priced calls | unpinned calls | nominal USD |
|---|---|---|---|---|---|
| 1a | cash | 136 | 124 | 12 | 47.59 |
| 1a | credits | 50 | 50 | 0 | 25.5 |
| 1b | cash | 78 | 78 | 0 | 73.85 |
| 1b | credits | 24 | 22 | 2 | 15.51 |
| 1b | sarvam_credits | 10 | 10 | 0 | 0.01 |

Conditional (listed, outside the cap):

| tranche | pool | calls | priced calls | unpinned calls | nominal USD |
|---|---|---|---|---|---|
| 1a | credits | 24 | 16 | 8 | 5.44 |
| 1b | cash | 4 | 0 | 4 | 0.0 |
| 1b | credits | 4 | 2 | 2 | 0.0 |

- Nominal in-cap total: **USD 162.46** (1a ≈ 73.09, 1b ≈ 89.37); of which cash ≈ 121.44, GCP credits ≈ 41.01.
- Unpinned calls excluded from the cap: **14** on routes `gpt-image-2-edit`, `veo-3.1-lite-i2v`.
- Sarvam lines are inside the cap in INR: ≈ ₹0.92 (Sarvam's prepaid balance; shown as USD-equivalent 0.01 at the August display rate).
- Evaluator lines (nominal): ≈ USD 3.82 (Cloud Vision + VLM triage; ASR unpinned). Controller judging time: see `COST-TABLE.yaml` → `evaluator_rows` → `controller_blind_judging.minutes`.
- The task's INFERRED planning figure was ≈ USD 150–165 nominal with ≈ 45–55 credit-eligible; the pinned figure sits in that range. gpt-image-2 and FLUX.2 Pro (base, edit and the arm-C/chain plates) are carried as fal cash until deployed on Azure; once deployed those lines move from cash to Azure credits at the same list price. The 1a nominal is above the plan's ≈ USD 60 line — morning decision 8 (raise the 1a cap, or apply the cut order in `IRREDUCIBILITY.md`).

## Morning decisions for the Controller (recorded, never attempted)

The task's eleven human-approval triggers, with the state this package assumes:

1. Ratify this package and the counts (35 cases / 298 + 32 conditional) or apply the cut order in `IRREDUCIBILITY.md`.
2. Sarvam key — **confirmed present**: the Controller session stated it, EVAL-039B's overnight check first reported the value empty, and EVAL-039B's Tester corrected that as a measurement error (DEFECT-1, commit `a24b197`: a 36-character value; length check only). The roster now records Sarvam bulbul:v3 as `pinned` and this package runs AUD-TTS-* on Sarvam (Sarvam credits, ₹3 per 1,000 characters) and ElevenLabs v3 via fal (cash). No key value was read by this task.
3. Azure deployments for gpt-image-2 / FLUX.2 Pro (credits) — carried as fal cash here; whether Sora 2 / MAI-Image-2.6 join — listed conditional.
4. Bedrock access for SD3.5 Large — listed conditional.
5. Runway account for VID-04 — stays `deferred_no_account`.
6. Controller-supplied photos for IMG-EDIT-01/02, IMG-EXT-01, IMG-COMP-01, IMG-REF-*, VID-REF-* — every reference asset is specified with a rights rule (Controller-owned photo, Resources item with explicit rights, or constructed synthetic); bytes are not produced by this task. IMG-EDIT-02 and IMG-REF-01 propose a printed label on a Controller-owned pack/tin so the Devanagari strings are known.
7. Seedance 2.5 policy: 2 items × 2 repeats per lane (this package) vs the plan's 4 single draws.
8. 1a cap: raise above ≈ USD 60 or cut.
9. Lip-sync drive route: ElevenLabs v3 repeat 1 (frozen default) vs Sarvam.
10. Lyria id (`lyria-002` observed vs "Lyria 3" in the plan) — both music routes are unpinned and excluded from the cap until resolved.
11. Fourth image-core slot = the policy-edge scene (this package) vs the plan's flat-lay + Indian-market scene.

## Open questions the Executor met (answered by a recorded default, never asked)

- OQ-1 Veo reference-to-video tier: the roster pins a reference-to-video variant on the Fast tier (0.10/s, credits), so VID-REF-* use `veo-3.1-fast-generate-001`; the plan's tier-less "veo-3.1 reference-to-video" is read as Fast.
- OQ-2 Native audio on Kling v3 / H3 Max / Wan 3.0 for the speech items (VID-T2V-01, VID-2SPK-01): assumed on where the route exposes it; the capability is pinned by EVAL-039B; a silent output on a speech item is a reject under the contract, never an exclusion.
- OQ-3 Whether `veo-3.1-lite-generate-001` accepts an image input: the roster pins no Lite image-input variant, so the task-fixed TOPO-03 arm-A Veo Lite line is `unpinned` (2 calls outside the cap), and the "cheapest pinned i2v route" for arm C and the VID-2SPK-01 chain is H3 Max i2v-768p (0.08/s). If Lite does accept an image, the Controller may price it at 0.05/s and swap arm C / the chain to it — counts unchanged.
- OQ-4 The second lip-sync route is `fal-ai/kling-video/lipsync/audio-to-video` (the roster added it, pinned at 0.014 per input video second in 5-s increments; `fal-ai/latentsync` exists but is not pinned). A 6-s plate bills as 10 s.
- OQ-5 VID-2SPK-01 runs at 8 s (two turns and a pause), a system-derived duration recorded in the NR; the core's 6 s is not applied to the added-scope item.
- OQ-6 Arm C's textless base and the chain plate use `fal-ai/flux-2-pro` as "the cheapest pinned image route" by indicative price (USD 0.03); re-resolved against pins before dispatch, counts unchanged.
- OQ-7 AUD-TTS-02's brand name "Kaushal Setu" is a labelled fixture (the task asks for Indian brand names in the Hinglish script; the source names none).
- OQ-8 One lip-sync plate (the VID-I2V-02 accepted clip) is held constant across AUD-LIP-01/02/03 so the drive language is the only variable; the task named the plate only for AUD-LIP-01.
- OQ-9 Music lane: the task fixes 8 calls (2 briefs × 2 routes × 2); EVAL-039B's MD-7 defaults to 4 in its totals — this package carries 8. Lyria is priced at the roster's `lyria-002` reading (0.06 per clip, the "Lyria 2" row; "Lyria 3" at 0.04 is unreachable on the endpoint — contradiction 1 / morning decision 10); ElevenLabs music bills 0.60 per rounded-up minute.
- OQ-10 The baked-text scan (E5) uses Cloud Vision TEXT_DETECTION; whether it bills against GCP credits is unverified (survey §4).
- OQ-11 Omni Flash 1.1's longest supported duration (≤ 15 s) is not in the survey; VID-MS-01 records "longest supported ≤ 15 s".
- OQ-12 VID-REF-01 reads the localised buyer's request (three references, free camera) as `generate` with identity references; MKT-014's own reading of its one-image posting is `animate`. Recorded, not silently resolved.
- OQ-14 `nano-banana-pro/edit`: the roster records the fal edit route (0.15/image, cash) as the plan names it and notes the same model edits on Vertex for 0.134 on credits; this package follows the roster so the two deliverables agree, and flags that the credits-first rule would move it to Vertex — the Controller may switch (counts unchanged).
- OQ-15 `openai/gpt-image-2` on fal is pinned at 0.053 only at quality=medium (fal's default is high at 0.211): the harness must set quality=medium, or the 1a projection rises by ≈ USD 4.
- OQ-17 The sibling's roster was edited again after this package's first build (its Tester's Sarvam correction landed in the working tree, commit `a24b197`); the final build read the working-tree roster, and `COST-TABLE.yaml` → `roster_cross_check` records the values it matched. If the roster changes again before the spend record, rebuild the cost table from `TEST-CASES.yaml` with EVAL-039B's `project_costs.py --test-cases` rather than editing numbers by hand.
- OQ-16 The HOLD-id grep: the packs' own verbatim DEFAULT text contains the word "carries" (CA-D7) and the grammar's field name is `mandatories`; a substring grep for `ries` therefore hits pack bytes and a schema field, never a HOLD source id. The Tester should grep with word boundaries (`grep -w`), as the repo's `validate_compiled_pack.py` matches HOLD-lane tokens. The Executor removed "carries"/"hurries" from its own prose.
- OQ-13 The image core's fourth slot folds the Indian-market scene into the Hindi policy-edge item (contradiction 3); if the Controller prefers the plan's split, one case is swapped, counts unchanged.

## Contradictions the Executor met (beyond the Planner's ten, which were applied as resolved)

1. Rule 6 ("one blueprint per case, byte-identical across routes") against the three-arm cases (IMG-TEXT-*, VID-TOPO3-01) and the native/chain case (VID-2SPK-01), whose arms need different prompts by construction. Resolution: one blueprint file per case carries the arm variants (textless-plate prompt, i2v motion prompt, chain steps); the prompt is byte-identical across every route *within* an arm, and route differences live only in `routes[].params`.
2. Task §A.4 gives three `text_handling` values; edit/extend cases preserve supplied lettering and generate none. Resolution: `none` with a note that supplied strings are preserved under `mutation_intents`, never generated.
3. The trigger table injects `product_appearance` only when a product entity is present, so its lighting doctrine cannot be cited on person-only or illustration cases. Resolution: those blueprints carry light and mood as brief-only production parameters (section 2a), attributed to nothing in Canon; only `composition_and_attention` decisions are cited.
4. The pack limit "never generate Devanagari glyphs; composite text deterministically" against TOPO-02/03 arms A and B, which generate Devanagari by design. Resolution: the arms are the experiment the Controller asked for; the limit is rendered in every text blueprint, arm C is the doctrine-compliant arm, and IMG-COMP-01's headline is composited.
5. "TTS 20 incl. 2SPK drives" implies both dialogue lines on both TTS routes × 2 repeats = 8 calls; a single call cannot voice two speakers. Resolution: four line-specific TTS entries on VID-2SPK-01.
6. "Veo 3.1 fast + extend" is one trial in the multi-shot count but two API calls. Recorded on the row (`api_calls_per_trial: 2`); billed seconds 15.
7. BR-F02-HI states the strings printed on the tin; IMG-REF-01 makes the tin the referenced product, so the lettering is product identity reproduced from references, never generated (the pack limit). Recorded as an adaptation.
8. The marketplace bank's UK/US buyers are localised to Indian buyers (MKT-009, MKT-012, MKT-014) to satisfy the Controller's register rule; the demand shape is kept and the localisation is listed as an adaptation.

## Self-check

The Executor ran the Tester checklist F.1–F.9 on its own output before finishing (YAML parse, 35 ids, sha256 match, operation vocabulary, primary capability ids, 13 families, coverage checks 1–8 incl. the benchmark-vocabulary grep, cost totals, source ids, HOLD-id and pack-id scans, E1–E5 byte match, `git status` confined to this directory and the Executor report). That self-check is not the Tester's verdict.
