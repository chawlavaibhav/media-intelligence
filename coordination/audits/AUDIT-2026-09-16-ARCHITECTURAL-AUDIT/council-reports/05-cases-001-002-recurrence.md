# AGENT 5 — Cases 001 (Upwork intro) and 002 (Upwork portfolio) forensics + recurrence audit 001→002→003

Read-only audit. MI main @ `3bb9a3c` (verified `git rev-parse HEAD`). Raw branches: `work/pilot-upwork-intro-video-v4` (head `f6ca66f`), `work/upwork-portfolio-samples-2026-09-15` (head `b4b77fa`), PR #103 `1de2b37`, Cumin job evidence `de1f978`. All times IST unless marked Z. Labels: OBSERVED / INFERENCE / HYPOTHESIS / UNKNOWN. Failure-chain codes K0–K15 as defined in the task.

Scratch media extracted for eyeballing: `scratchpad/audit/agents/media05/` (V3/V4/V4.1 films byte-identical to the case sha256s: V3 `ea81264d…`, V4.1 `d1a5edf8…`, both recomputed with `shasum -a 256`).

---

## 0. Findings ranked

1. **The runtime gates promoted from case 001 are a library, not a path.** `runtime/compositor/gates.py` (`344f517`, on main via PR #98 at 08:04:05 15 Sep) is called by nothing in `runtime/` except its tests (`grep -rn check_text_bounds|check_contrast|check_fit|check_geometry|check_disjoint runtime --include=*.py` → only `gates.py`, `tokens.py` docstring, tests). No production path on main imports it. The first production to import it was the Cumin job tool (`de1f978:agency/jobs/AGY-…/tools/compose.py:30-31`), i.e. a per-job script. "Promoted into the runtime" (CONTROL-STATE.md:196-199) is true of the code and false of any executable path. OBSERVED.
2. **Case 002 did not bypass a merged gate so much as never import any gate — including the pilot's own.** The batch was built on the branch whose head `f6ca66f` already carried `v4/tools/design4.py` (TextBox, `contrast_ratio`, `place_text`, `contain/native/declared_cover`, `write_reports`). The batch tools `compose_v4.py` (imports `adcomp` = the V2 rasteriser), `compose_pf.py`, `export_tiles.py`, `ad_9x16.py`, `nivaas*_build.py` import none of `design4`, `runtime.compositor` (grep of every tool at `b4b77fa`). Timeline: export folder born 07:52:24, PR #98 merged 08:04:05, first paid call 08:05:49. The case README's "bypassed the workflow … merged the same day" is literally true but the decisive bypass was of the same-branch gates written 9 hours earlier. OBSERVED (git log, grep). K12+K13.
3. **The "robotic voice" defect was known before case 001 and discounted by policy.** `eval/historical-priors/media-factory-v1/MEDIA-FACTORY-ROUTING-PRIOR.md:28`: "raw TTS sounds robotic without speech-rhythm rewrite + mix" (Sarvam bulbul:v3); `PROMPT-ENRICHMENT-EVIDENCE.md:34` records the fix. The pilot's `preprod/ROUTE-ANALYSIS.md:38` (branch @ `7629894`) lists that directory and states "**none is relied on below**"; Sarvam was chosen on RR-12 "6/6" whose Lab lines were 30, 70 and 34 characters (`eval/experiments/EVAL-040/runs/aud-tts-sarvam/artifacts/*.request.json`) and then used for ≈1,000 characters / 47.8 s. Recurred in case 003 (Sarvam 8/8 rejected by ear, RO-04). RR-12 on main still names Sarvam the default with no caveat. K1→K3→K4 (retrieved, in context, discarded) then K5/K8, then K13 twice.
4. **Contrast knowledge was in the pilot's own context and ignored (K4), not absent (K0).** `preprod/CANON-BRIEF.md` @ `7629894` line 174: text ≥ 4.5:1, "Text over image needs value contrast (sk_sam_c003_0021)", "reverse type and headlines over the picture are named failures (sk_ogx_0028)", grayscale check CA-D5. V3 drew "HUMAN-CHECKED" over the dal photo with its sub-line vanishing (eyeballed, `v3-t37.5.png`). The case's PROMOTION-QUEUE says "no new Canon need was proven" — correct, and it should have said the opposite: existing Canon was not consumed by the compositor.
5. **A rejected version's self-review seeded case 002's defects.** `v3/learning/PRODUCT-LEARNING-V3.md` @ `70f687e` §G: "Exact-text mechanism B … produced zero text defects across 23 deliverable files" and proposes "the Kora poster register, the Dhaba Hindi overlay" as template candidates. The Controller rejected V3 minutes later for clipped text and lost contrast. Nobody revoked the proposal; both treatments were exported unchanged as B1 tiles the next morning (HD-03/04/05/07). K7 → K13 → REJECTED_DESIGN_REUSE.
6. **Subject-obstruction ("text over subject") has now occurred in all three cases and is still not code.** 001 V3 (HUMAN-CHECKED over the dal), 002 HD-03/05/07/08/09/10, 003 HD-03 "text is coming on figures". Learning artefacts: 002 candidates TEXT_OVER_IMAGERY_CONDITIONAL / SUBJECT_AWARE_CROP_ANCHORING (never wired: `grep -i obstruct|margin|inset|hierarchy runtime/compositor` = 0 on main and on `1de2b37`), skill row CF2 (human eye), and the Cumin job's own `wall_obstruction` after V1 — third private implementation. On Cumin V1 the operator's CF2 row read "PASS on 9:16 (copy on empty wall, nothing over bowl/hands/faces)" (JOB.yaml:326) while the user saw text on figures — a human-checklist row self-assessed PASS (K11/K7).
7. **Promotion-queue IDs are recorded, not wired, except where a job script happened to import a module.** No case-001 ID string exists anywhere on main outside the case directory (`git grep -w` over main excluding `production-learning/` and `.claude/skills/` = 0 for all eight gate IDs and all candidates); the three 002 IDs appear only in the skill and `docs/media-agency-operator.md`; `REJECTED_DESIGN_REUSE` was renamed `DESIGN_REUSE_PROVENANCE` in the skill without a cross-reference. SERVICE_INTRO_TEMPLATE is not in `runtime/canon/templates.py`. COMPLEX_PRODUCTION_EVENT: trigger declared MET in 002, nothing built by 003.
8. **Human attention was spent at the wrong altitude.** Case 001: 9 human touches, all verdicts on fully assembled films; the two decisive inputs (V2 strategic correction, V3 "presenter = hard requirement" + compositor list) arrived after USD 8.08 and USD 3.28 respectively. Case 002: the Controller was the only QA (10 defects in 8 messages); the operator contributed no detection on B1. Case 003: 10–12 cycles (the case's own counts disagree), 5 of them voice rounds after the plates were drawn.
9. **Case 003 is the first case where learning demonstrably propagated — and it still failed.** JOB.yaml @ `de1f978` cites 001 RO-05 (line 98, 226), 002 CROSS_CLIP_VOICE_CONTINUITY (105), DESIGN_REUSE_PROVENANCE (108), micro-qualifies plates/clip/voice, runs per-geometry QA (CF2 FLAGGED on 4:5/1:1), keeps a packet and a cap. Every rejection landed on a dimension no gate measured (VO overlap, ad structure, mouths under VO). The pattern across three cases: gates measure what the previous case's Controller named; the next Controller names something else.

---

## 1. CASE 001 — UPWORK-INTRO-001

### 1.1 Timeline (mechanical; branch commit times recomputed with `git log --date=iso`)

| Version | Commit (branch) | Time | Verdict (verbatim summary, HUMAN-VERDICTS.yaml @3bb9a3c) | USD (reserved) | Dispatches |
|---|---|---|---|---|---|
| package 1 | session created | 15:02:14 (09:32:14Z) | — | | |
| V1 | `7629894` | 16:44:13 | `specific_repair` — "acceptable-but-not-great direction; commercially clear, strong sales logic"; feedback: video proof too small · too much phone/mockup framing · opening not visually exceptional · presenter blocks too long · creative range insufficient · 24h/4h undersold | 3.762 | 10 (shares a 12-line ledger with V2) |
| V2 | `7b39aeb` | 17:21:32 | `rebuild_direction` — "not great enough — competent, not extraordinary"; strategic correction after: images AND videos co-equal · one product becoming a campaign · work owns the majority of screen time | 4.320 | 2 |
| V3 | `70f687e` | 18:55:57 | `reject` — "assembly/compositor failure set; presenter missing became a hard requirement": text getting cut off · text colour disappearing against backgrounds · creatives/images being cropped · inconsistent card geometry · voice horribly robotic · pacing too rushed · direct-to-camera speaker missing → HARD REQUIREMENT | 3.2836 | 36 (3 Lyria failures) |
| V4 | `11d3e59` | 22:40:00 | `specific_repair` — "architecture finally worked"; defects: offer/code collision · "and it can't suck" lost · bubble persisted · not enough range proof · Express too weak | 4.0276 | 6 (2 Veo UNAVAILABLE) |
| V4.1 | `f6ca66f` | 22:56:19 | `accept` — "accepted for release" | 0 | 0 |

TTAO: 7:53:35 mechanical lower bound (session created → V4.1 mtime 22:55:50; ACCEPT minute unrecorded); Controller estimate "7–8 h". Total USD 15.39318 reserved across 54 dispatches (TIME-AND-COST.yaml); the pilot's own final report quoted 7.3112 (V3+V4 only). Generation wait 1:05:42 (latency sum) ≈ 14 %; unattributed review/packaging gaps 3:49:34 ≈ 48 %. Verdict evidence is chat-only (`evidence_class: chat_only_human_evidence`) — no verdict file exists on the branch; every pilot learning report ends "awaiting Controller judgment" (OBSERVED, `v3/learning/PRODUCT-LEARNING-V3.md` §H "24 is the Controller's call").

Human review cycles: 5 (one per assembled version). Human touches (see §5): 9.

### 1.2 Routes / tools used and their provenance

| Layer | What was used | Chosen from Registry/routing evidence? | Source |
|---|---|---|---|
| Stills | Nano Banana 2 (Gemini API) V1/V4; GPT Image 2 medium (fal) ×4, Seedream 5 Pro Edit ×6, FLUX.2 Pro ×1 V3 | Yes — `preprod/ROUTE-ANALYSIS.md` cites ROUTING-EVIDENCE-MAP cells and Registry latency/cost rows (lines 36-41, 85-86) | branch @7629894 |
| Video | Veo 3.1 Fast i2v + native speech (Vertex) V1/V4, extend V2; MiniMax H3 Max V1; Kling v3 Pro i2v ×5 V3; Wan 3.0 Prime planned fallback (never callable) | Partly — VID-I2V/VID-REF cells cited; **speaker route had no Registry cell** (SD-08) → ad hoc micro-qualification Omni vs Veo | ROUTE-ANALYSIS §; SPEAKER-QUALIFICATION.md @11d3e59 |
| TTS | Sarvam bulbul:v3 `aditya` ×16 (V3) | Yes — RR-12 "default voice route", evidence 6/6 on 30–70-char lines | ROUTING-EVIDENCE-MAP-v0.yaml:222-226 (main); request.json lengths OBSERVED |
| Music | Lyria-002 ×4 (3 × 5xx) | Yes (cell cited) | |
| Compositor | pilot scripts: `tools/film.py`, `film2.py`, `adcomp.py` (V1/V2); `v3/tools/compose.py` + `film3.py`; `v4/tools/design4.py` + `film4.py` — Pillow + hb-view + ffmpeg | No runtime component existed for composition; `canon/gate` is a baked-text/prompt gate, not a layout gate (`canon/gate/textscan.py`) | branch trees |
| Historical priors | `eval/historical-priors/media-factory-v1/` | Listed and explicitly not relied on: ROUTE-ANALYSIS.md:38 "**none is relied on below**" | OBSERVED |
| Canon | `preprod/CANON-BRIEF.md` (researcher output, 37 sources by id) + two compiled packs | Yes, by id; but consumed by the script writer, not by any compositor | @7629894 |

### 1.3 Failure chains (K-codes)

Eight-state test per chain: exists → retrieved → in context → understood → changed a decision → decision correct → survived production → QA detected.

**(a) Robotic long-form voice (V3, SD-05/RO-05).**
- Knowledge existed: **K1** — `eval/historical-priors/media-factory-v1/MEDIA-FACTORY-ROUTING-PRIOR.md:28` and `PROMPT-ENRICHMENT-EVIDENCE.md:34` (identical text in MFH `/media-factory-controller-handoff/`), confidence "Medium (Tier B)". Retrieved and in context: ROUTE-ANALYSIS.md:38 names the directory. Discarded by rule ("none is relied on") → **K4** (present, not used), by design of the evidence hierarchy (historical priors have no routing authority) → arguably **K6** (no owner for "prior says X, Lab says Y, which governs?").
- Reasoning: RR-12's 6/6 on ≤70-char lines extrapolated to 8 paragraphs → **K5/K8**.
- QA: `v3/tools/vo_check.py` = transcript match ("all 16 verbatim") → **K11** (measured presence, not delivery); the executor's self-check noted "the Controller should listen" → **K7** (self-review, deferred to human).
- Human: verdict came after full assembly (USD 3.28) → **K14**.
- Propagation: RO-05 recorded as directional, no Registry/routing change ("routing_authority: none"); RR-12 unchanged on main and on `1de2b37`. Case 003 re-hit it (RO-04, 8/8 rejected) → **K13** (see §3).
- Conflict to report: 001 SD-05 classes this as `pipeline_failure` (route choice), 003 RO-04 as a model observation "consistent with 001 RO-05", RR-12 as clean default. Three documents, three statuses; no reconciliation owner.

**(b) Creative architecture re-litigated V1→V2→V3 (SD-13; creative_direction ×8 in the root-cause histogram).**
- Knowledge: CANON-BRIEF @7629894 §"Presenter grammar" and the COMMERCIAL-BRIEF contradiction flag (ROUTE-ANALYSIS.md item 3: the profile says "Not on the menu: on-camera presenters" while the film leads with one) were in context before V1 → **K3/K4**. The Karl review (`plan/KARL-REVIEW-script-v3.md`, an AI persona reviewing the script "before any spend") is **K7** — no independent human challenge at the architecture level.
- Ownership: presenter yes (V1/V2) → no (V3) → hard requirement (V4); "phone/mockup framing" objected in V1 and V2. The Controller's own strategic correction after V2 changed the brief. → **K6** (architecture decision owned by nobody until V2) and **K14** (human approval at film level, never at storyboard/animatic level; script v5 was approved, the visual architecture never was).
- No gate can detect this; the case correctly does not propose one. The ACCEPTED-TEMPLATE is the only durable output; it is not in `runtime/canon/templates.py` (OBSERVED grep) → recorded only.

**(c) Proof size / presenter blocks / framing (V1, V2).** Same chain as (b): **K14 + K5**. Pacing rule "important still ≥ 3.3 s" exists only as `evidence_scope: this_accepted_template`.

**(d) Text clipping (V3, SD-01).**
- Knowledge: no structured layout rule anywhere (canon/knowledge/current: 1 file mentions "safe area"; `canon/gate` has no layout check; MFH: 0 hits for clipping/overflow) → **K0/K1**. `v3/tools/compose.py` `wrap2()` fits to `max_w` but measures nothing after drawing; no `textbbox`, no canvas assertion → **K10**. No post-draw geometry QA → **K11**. Executor self-check §H claims "all strings from the deck" (presence) → **K7**.
- Eyeballed: `v3-t33.5.png` (beat s12-exact, 32.9–36.4 s) shows the "FIRST ORDER" pill cut at the card's top edge; `v3-t8.png` shows the caption "FOUR IMAGE DIRECTIONS" running under the card. OBSERVED, consistent with the verdict "text getting cut off (brief card, statement)".
- Promotion: TEXT_BOUNDS_GATE → `gates.check_text_bounds` (wired as library; see §4).

**(e) Contrast (V3, SD-02).** Knowledge existed and was in context (CANON-BRIEF:174; PACK-product_appearance check line 413 "tonal contrast survives a grayscale check"; `canon/knowledge/current/w3c-wcag22-text-legibility/`, `ogilvy-beyond-ch2/source-knowledge.yaml:1447` sk_ogx_0028) → **K4** (the compositor author had the numbers and drew labels over photographs anyway) + **K11**. Eyeballed `v3-t37.5.png`: "HUMAN-CHECKED" over the dal photo, sub-line "Every file, before delivery" unreadable where it crosses the photo. OBSERVED.

**(f) Crops (V3, SD-03).** `compose.py:63 cover()` is the default fit with a fractional anchor → **K5/K10** (design default), **K11**. Canon CA-D6 ("aspect justified") is not a crop rule → K1 at best. My 9-frame sample did not isolate a destructively cropped creative (the 4:5 Aarohi card at t=8 is complete); the Controller's frame is UNKNOWN. The code default is OBSERVED.

**(g) Video-created lettering (V3 Kling B2, SD-06).** Knowledge existed: RR-11 / vid-ref "lettering appeared" (ROUTE-ANALYSIS.md:101) and the Canon post-draw detector "wired, never invoked" (`canon/gate/textscan.py:234`) → **K1/K3**; the still passed the scan, the clip was never scanned → **K11** (QA on the wrong artefact). Caught by the executor's eye; excluded. Promoted VIDEO_FRAME_TEXT_HYGIENE → `runtime/loop/frame_hygiene.py` + `driver.py:121 frame_sampler` — the only 001 gate wired into an executable path (the dry Alpha loop), which no real production has used; Cumin's D1 was a human-eye pass because Cloud Vision "is not authorised by default" (QA-CHECKLIST D1).

**(h) Route liquidity (SD-11).** fal balance was read at plan time (SHOT-MAP:10 "USD 3.35 available"; SPEND-RECORD-V3 "fal cash 3.23 at start") → knowledge in context; the plan still put Kling/Wan/H3 all on fal under an INR 2,000 cap → **K5** (cap ≠ liquidity) + **K6**. Promoted PROVIDER_POOL_AVAILABILITY → `runtime/execute/pools.py` (fail-closed in the dry bridge). Case 003's pool reading was "I attest all pools cover the cap" (JOB.yaml:69, 267) and ElevenLabs quota exhausted at 54 credits mid-job (003 RO-05) → the rule survives as text, the mechanism is not on the agency path (**K12-lite**).

**(i) Long TTAO.** 48 % of the clock is review/packaging gaps; three architectures; compositor without gates until V4 → **K14 + K6 + K15** (five full assemblies where a storyboard round would have carried V1→V2 information). TTAO adopted as KPI (PR #98 audit comment 19:19Z) and stamped by the skill's JOB-TEMPLATE (`ttao.*`) — the one candidate that became mechanism.

**Media-model failures reaching the Controller: 0** (case claim). INFERENCE: defensible under the case's definition, but it silently reclassifies "voice horribly robotic" as routing and "presenter quality degraded (chained extends)" as `model_generation` in REVISION-TRACE — an internal inconsistency in the same case.

---

## 2. CASE 002 — UPWORK-PORTFOLIO-002

### 2.1 Timeline and gates-in-existence

| Event | Time (15 Sep) | Source |
|---|---|---|
| pilot gates `design4.py` exist on the batch's base commit | 14 Sep 22:56 (`f6ca66f`) | branch |
| runtime gates on PR #98 branch | 14 Sep 23:34 (`344f517`), frame hygiene 23:49, pools 00:02 | `git log --follow` |
| Controller audit fixes on PR #98 | 07:46:47 (`fc806c3`) | |
| B1 export folder born | 07:52:24 | TIME-AND-COST (APFS birth) |
| B1 defects, 8 messages | 07:59–08:18 | HUMAN-VERDICTS |
| **PR #98 merged to main** | **08:04:05** (`17b347c`) | `git log --merges` |
| first paid call | 08:05:49 | ledger |
| tools + IronLeaf/GyaanBox commit | 08:16:09 (`662fba4`) | |
| B2 commit | 08:24:07 (`c3995c6`) | |
| N1 call / operator accept / Controller reject | 08:28:10 / 08:39 / 08:43–08:44:25 (`11c6eb7`) | |
| N2 calls / reject+skip / silent rebuild | 08:46–08:59:40 (`c969204`) | |
| handover (implicit accept of 9) | ~09:05 | chat only |
| archive commit | 12:31:25 (`b4b77fa`) | |
| case 002 on main | 12:41:23 (`4fdf085`), PR #100 merged 13:48:54 | |
| media-agency skill on main | PR #99 merged 14:21:27 | |

Which gates existed and why they did not run: `compose_v4.py` imports `adcomp` (V2) and `v3/plan/COPY-DECK-v3.yaml`; `compose_pf.py`, `export_tiles.py`, `ad_9x16.py`, `nivaas_build.py`, `nivaas2_build.py` import `compose_v4`/`compose_pf`. None imports `design4`, `runtime.compositor`, `frame_hygiene`, `pools`, `provider_errors` (OBSERVED, grep at `b4b77fa`). The B1 bytes are not on disk (export dir first committed at `b4b77fa`; `662fba4`/`c3995c6` trees contain 0 `portfolio-export` paths — OBSERVED), so the B1 defects are evidenced by the fix commits and the transcribed verdicts only; I verified the V3-lineage source treatments instead (below).

### 2.2 Failure chains

| Defect | Chain | Knowledge/gate that existed | Evidence I checked |
|---|---|---|---|
| Text clipping HD-01/02 | **K12 + K13** (same-branch `design4.place_text` bounds and runtime `check_text_bounds` both unused) + **K11**; HD-02 "fits but reads clipped" is a gate-scope gap → READABILITY_MARGIN candidate (never wired) | design4 @f6ca66f; gates.py @344f517 | `compose_v4.py:120` at `b4b77fa` now has `maxw = W - 2*m - int(W*0.05)  # never let a headline kiss the panel edge` — the fix lives only in the pilot tool |
| Low contrast HD-04 | **K12/K13** (CONTRAST_GATE existed twice) + REJECTED_DESIGN_REUSE: the V3 Kora poster was exported as-is | CANON-BRIEF contrast numbers; design4 `contrast_ratio` | `v3/gen/deliverables/kora-hook-1-16x9.png` @70f687e eyeballed: cream serif over a light beige wall — legible but low-contrast, matches "hard to read, unfinished" (OBSERVED, my eye) |
| Text over subject HD-03/05/07/08-10 | **K7 → K13 → K6**: `PRODUCT-LEARNING-V3.md` §G proposes "the Kora poster register, the Dhaba Hindi overlay" as templates from a version rejected minutes later; nobody revoked it; reused. No obstruction check existed anywhere (**K0** in code) while Canon named it (sk_ogx_0028, CANON-BRIEF:174) (**K4**) | | V3 film t=37.5 s shows the same class in the accepted-lineage's rejected version |
| Destructive crop HD-06 / HD-11 | `compose_v4.cover()` (line 63) is the V3 `cover()` verbatim; CROP_FIT_DECLARATION (contain default for product proof) existed in design4 and runtime → **K12/K13**; HD-11 operator-caught over three renders → K10 | | |
| Rejected design reuse | as above; **K6** — no provenance field existed on any asset until JOB-TEMPLATE `plan.assets[].reuse` (PR #99, after the fact) | | 003 JOB.yaml carries the field, all `null` (nothing reused) — untested in anger |
| Narration hole HD-13a | **K11** (`speaker_check.py` transcript-presence accept at 08:39; Controller reject 08:43) + **K13**: the same operator had written RO-05 ("all 16 verbatim on transcript; rejected by ear") ~10 h earlier and RO-02 (Veo extend chain degrades) and chose Veo t2v+extend again | RO-02, RO-05 (PR #98 branch, merged 08:04) | |
| Two narrator identities HD-13b | **K0** (no cross-clip check existed) + **K5** (per-clip acceptance assumed to compose); MFH HANDOFF:10 had named "no cross-asset consistency" as a known gap → K1 | | |
| Process PD-01..09 | **K12 + K14** (chat "go" as the only authority; no packet/cap/ledger split); PD-07 "the operator did not re-read main after PR #98 merged" — but main moved 12 min after the batch began; the operative failure is not re-reading one's own branch | | |

Tally in the case: 10 pipeline failures reached the Controller, 2 model (HD-13a/b, each with a QA component), 2 operator-caught. I agree with the classification except that HD-13b "native narration not identity-stable across generations" is model behaviour that the plan should have expected (K5), not a surprise.

---

## 3. RECURRENCE TABLE

"Learning artefact" = what was supposed to prevent the recurrence; K13 detail = written? promoted into what? read by the next job? enforced?

| Defect class | 001 | 002 | 003 (`1de2b37`) | Intermediate learning artefact | Why it did not prevent (K13 detail) |
|---|---|---|---|---|---|
| Text clipped / overflow | V3 SD-01 | HD-01, HD-02 | not reported | TEXT_BOUNDS_GATE → `gates.check_text_bounds` (PR #98) + pilot design4 | Written ✔, promoted to code ✔ (23:34 14 Sep), on main 08:04 ✔, **read by 002: no** (tools import adcomp), enforced: no path calls it. 003 imported it in its job tool → held |
| Contrast lost over imagery | V3 SD-02 | HD-04 | (V1 "contrast probed on 4 frames" SD-04 — gate ran, mis-sampled) | CONTRAST_GATE; Canon sk_wcag/sk_ogx in CANON-BRIEF | 002: not imported. 003: imported, but `luminance_samples` from 4 frames misread a gradient (K10) — gate present, sampling wrong |
| Text / UI over the subject | V3 (HUMAN-CHECKED over dal; SD-07 offer/code straddling the plate in V4) | HD-03/05/07/08/09/10 | **HD-03 "text is coming on figures"** (SD-04) | 002 candidates TEXT_OVER_IMAGERY_CONDITIONAL, SUBJECT_AWARE_CROP_ANCHORING; skill CF2 (human row) | Written ✔ (candidate); promoted only to a **human checklist row**; read by 003 ✔; enforced ✗ — the operator marked CF2 "PASS on 9:16" on V1 (JOB.yaml:326) and the user rejected. Third private implementation (`wall_obstruction`) now a 003 candidate. Not in runtime on main or PR #103 |
| Destructive / accidental crop | V3 SD-03 | HD-06, HD-11 | SD-09 (4:5/1:1 re-crop leaves no copy zone; bowl base cut ~55–115 px, CF2 REVIEW) | CROP_FIT_DECLARATION; 002 FORMAT_SPECIFIC_REVALIDATION | 002: not imported. 003: per-geometry QA ran and **flagged** it (state 8 reached) but the deliverable was still a re-crop (state 5 not reached) → new candidate GEOMETRY_NEEDS_ITS_OWN_PLATES |
| Robotic TTS voice | V3 SD-05 / RO-05 (Sarvam ×16) | — (no TTS; native Veo narration) | voice rounds 1–3 "all three are robotic" (Sarvam 8/8, ElevenLabs 6/6 rejected), 26 takes | MF prior (Tier B) → RO-05 directional → skill D10 "long narration not accepted on transcript alone" → JOB.yaml micro-qualification by ear | Written ✔ three times (MF 2026-08, 001, 003); promoted ✗ (RR-12 unchanged; MF fix "speech-rhythm rewrite" never entered MI); read by 003 ✔ (JOB.yaml:226 cites RO-05); enforced as "human ear first" ✔ — which is why it cost 5 rounds instead of a rejected film. VOICE_BY_EAR_FIRST (003) = SPEAKER_MICROQUALIFICATION (001, "keep as candidate") = MF "speaker chosen by human ear" (Jul-Aug) — the same pattern proposed three times |
| Speaker/presenter degradation across chained generations | V2 RO-02 (Veo extend drift) | N1 (Veo extend split narration, re-imagined scene) | — | RO-02 directional, routing_authority none | Written ✔; promoted ✗; read by the same operator ✗ (chose extend again next morning); 003 JOB.yaml:219 "case 002 RO-01 (no extend chains)" ✔ — propagated on the third job |
| Narration continuity / holes / overlap at joins | — | HD-13a (2.9-s hole), HD-13b (two voices) | **HD-07 VO overlap 0.92 s + overrun 0.94 s** (SD-08) | CROSS_CLIP_VOICE_CONTINUITY (skill D14, human ear on the assembly) | Written ✔, promoted to a human row ✔, read ✔ (JOB.yaml:105), enforced ✗ — V3 shipped with an overlap D14 should have caught (K11). Now `check_vo_schedule` (PR #103) — first deterministic audio gate |
| Video judged on still / lettering in frames | V3 SD-06 | — | — (7/7 Veo clips frame-sampled clean) | VIDEO_FRAME_TEXT_HYGIENE (loop) + skill D1 | Propagated as a human-eye frame pass; the Cloud Vision detector still "not authorised" |
| Pool liquidity ≠ cap | V3/V4 SD-11 | — | ElevenLabs quota exhausted at 54 credits mid-search (RO-05); pools attested not read | PROVIDER_POOL_AVAILABILITY (`pools.py`, dry bridge) + skill A7 | Written ✔, code ✔, on the agency path ✗ (A7 satisfied by "user attestation in chat") |
| Creative architecture unowned / "not an ad" | V1–V3 (three architectures) | — | V2 "does not look like an ad at all … canon had this knowledge" (SD-07, Canon gap) | 001 CANON-BRIEF had ABCD/Ogilvy closing rules by id (lines 185-187); `commercial_communication` pack uncompiled (C-10) | **K2/K3**: the knowledge reached 001 through a hand-written researcher brief, not through a pack; the agency path consumes packs only → the next job could not retrieve what the previous job had in context. Not a K13 of a case artefact; a Canon-delivery gap surfaced by 003 and reported, not fixed |
| Paid calls without packet/cap/ledger | — | PD-01..09 | conformant | PAID_PRODUCTION_PREFLIGHT (skill stage 8, JOB-TEMPLATE) | **Propagated and effective** — the one clean success; and the case still failed on quality |
| Offer/code hierarchy collision | V4 SD-07 | HD-08 (pill on seam cuts the plant — "accepted in context" reuse) | — | ELEMENT_DISJOINTNESS (boxes) — measures overlap, not read order (case's own note) | Gate scope gap acknowledged in 001; 002 hit the adjacent class (obstruction) |

Summary INFERENCE: of ten recurring classes, one (preflight) was prevented by propagation; three were *detected* by the propagated mechanism but still shipped or still cost rounds (format, voice-by-ear, per-geometry crop); six recurred because the artefact was a case file or a checklist row that no code path or independent reviewer enforced.

---

## 4. Promotion queues: proposed vs actually landed (recorded vs wired)

"Recorded" = the ID/rule exists in a case file, skill text or doc. "Wired-lib" = code + tests exist but nothing on a production path calls it. "Wired-path" = an executable path calls it. "Used" = a real production ran it.

| ID | Case | Proposed where | Landed (main `3bb9a3c` / PR #103 `1de2b37`) | Status |
|---|---|---|---|---|
| TEXT_BOUNDS_GATE, CONTRAST_GATE, CROP_FIT_DECLARATION, GEOMETRY_TOKENS, ELEMENT_DISJOINTNESS | 001 | `runtime/compositor/gates.py`, `tokens.py` | present (`344f517`, fixes `fc806c3`), 24 tests (28 on PR #103); ID strings appear nowhere outside the case dir; callers: none in runtime | **Wired-lib**; **Used** once, by Cumin's job tool import |
| VIDEO_FRAME_TEXT_HYGIENE | 001 | `runtime/loop/frame_hygiene.py`, `postdraw.py`, `driver.py` | present (`c6c39b8`), `driver.py:121` calls `frame_sampler` | **Wired-path** (dry Alpha loop); real productions used the human eye |
| PROVIDER_POOL_AVAILABILITY | 001 | `runtime/execute/pools.py`, `bridge.py` | present (`dcddedb`) | **Wired-path** (dry bridge); agency path uses attestation |
| TRANSIENT_ERROR_CLASSIFICATION | 001 | `provider_errors.py` | present; imported by Cumin `dispatch.py:35` | **Wired-lib + Used** |
| SPEAKER_MICROQUALIFICATION | 001 candidate ("KEEP AS CANDIDATE") | — | skill A9 / workflow §9 text; 003 applied it | Recorded in skill; re-proposed by 003 as VOICE_BY_EAR_FIRST |
| SERVICE_INTRO_TEMPLATE | 001 candidate | ACCEPTED-TEMPLATE.yaml | not in `runtime/canon/templates.py` (grep 0) | Recorded |
| TTAO_PRIMARY_KPI | 001 adopted | — | JOB-TEMPLATE `ttao.*` stamps; 003 recorded them | **Wired into the job record** |
| COMPLEX_PRODUCTION_EVENT | 001 deferred → 002 "trigger MET" | OUTCOME-EVENT-v2 | nothing on main or PR #103 | Recorded twice, not built |
| QA_COVERAGE_ENFORCEMENT, FORMAT_SPECIFIC_REVALIDATION, PAID_PRODUCTION_PREFLIGHT, CROSS_CLIP_VOICE_CONTINUITY | 002 promoted_now | media-agency workflow | SKILL.md, QA-CHECKLIST (C-final, D14), JOB-TEMPLATE (lines 148-150), `docs/media-agency-operator.md:120-122` | Recorded in skill (a prompt, enforced by the operator reading it); 003 followed them |
| REJECTED_DESIGN_REUSE | 002 promoted_now | workflow provenance | renamed **DESIGN_REUSE_PROVENANCE** in the skill; the case ID string appears nowhere outside the case | Recorded, ID drift |
| READABILITY_MARGIN, STACK_LEVEL_FIT, SUBJECT_AWARE_CROP_ANCHORING, SINGLE_VOICE_SOURCE, STILLS_FIRST, TEXT_OVER_IMAGERY_CONDITIONAL | 002 candidates | runtime/compositor (conditional) | none in runtime on main or PR #103 (`grep -i margin|inset|obstruct|hierarchy|stack` = 0); the 5 % margin exists only in `compose_v4.py` on the archival branch; QA-CHECKLIST CF2/CF5 carry them as human rows | Recorded |
| VO_SCHEDULE_GATE | 003 | `gates.check_vo_schedule` | on PR #103 (`1de2b37`, +35 lines, +4 tests) | Wired-lib (PR open) |
| WALL_OBSTRUCTION_GATE, VO_FIRST_TIMELINE, CLOSED_MOUTH_UNDER_VO, AD_STRUCTURE_MINIMUM, GEOMETRY_NEEDS_ITS_OWN_PLATES, VOICE_BY_EAR_FIRST, AUDIO_EDGE_TRIM_ONLY, ATTEMPT_ID_LOCK | 003 candidates | job tool / runtime later | job tool only | Recorded |

Distinguishing sentence: **eight 001 gates exist as code; zero of them sit on a path that a real production is obliged to traverse.** The skill converts that gap into an instruction ("run the existing runtime gates, never a weaker one-off version", SKILL.md §Every job 3) — which is exactly the instruction the 002 operator did not follow with the pilot's own gates.

---

## 5. Human attention accounting

Definition: a distinct moment where the human supplied information the system then acted on.

**Case 001 (9 touches, 5 verdict cycles).** (1) package 1 15:02 · (2) V1 verdict ~16:45 · (3) script v5 approval before V2 (REVISION-TRACE "script v5 approved") · (4) V2 verdict + strategic correction 17:21–17:57 · (5) V3 package 17:57 · (6) V3 verdict, somewhere in the 18:56–22:09 gap · (7) V4 package ~22:09 · (8) V4 verdict · (9) V4.1 accept after 22:56. Every verdict was on a fully assembled film; no human gate on the speaker (SPEAKER-QUALIFICATION was executor-scored 53/60 vs 45/60 and folded into the V4 verdict). **Decisive**: (4) — "work owns the majority of screen time" — and (6) — presenter = hard requirement + the four compositor classes. Together they define V4; (8) produced only USD-0 assembly repairs. Touches (1)–(3) produced the two lineages later discarded entirely (USD 8.08).

**Case 002 (≈8 touches, 5 cycles).** B1: 8 messages / 10 defects 07:59–08:18 (one review moment) · "go" tile 7 · N1 reject 08:43 · "go" stills · "go" motion · N2 reject + skip 08:58–09:02 · handover 09:05 · meta-verdict ("i suspect you didnt use the pipeline either properly"). **Decisive**: B1 — the Controller was the only detector; the operator contributed zero detections on B1 and two on B2. N1 reject overturned an operator accept given 4 min earlier. The meta-verdict is what turned a media case into a process case.

**Case 003 (10 per README/TIME-AND-COST `total_cycles`; enumeration gives 4 plate/clip gates + 4–5 voice rounds + 3 versions = 11–12 — internal conflict, UNKNOWN which is right).** Decisive: voice round 2–3 ("stick to english … why are we not using veo models with voice? … calm + cheerful") — direction the packet lacked; V2 ("does not look like an ad … canon had this knowledge") — the Canon-delivery gap; V3 ("voices overlapping") — the one promoted gate. Four of the human moments (plates, clip) confirmed things that were already fine; the expensive information came late.

Across the three cases the human's decisive information arrived after full assembly in 001 and 003, and after export in 002; no case had a human touch at storyboard/animatic altitude.

---

## 6. Conflicts between sources (reported, not harmonised)

- 001 README "54 paid dispatches" vs V3 PRODUCT-LEARNING "37 calls" for V3 vs V3 ledger 36 lines — the case reconciles to 36; the pilot doc is off by one.
- 002 README: "workflow … merged the same day (PR #98)" — merge 08:04:05, batch began 07:52:24 (12 min earlier); the same-branch `design4` gates are the ones actually skipped.
- 001 SD-05 (pipeline_failure) vs 001 REVISION-TRACE (`model_audio`) vs 003 RO-04 (model observation) vs RR-12 (clean default) for the same Sarvam behaviour.
- 003 human cycles: 10 stated, 11–12 enumerated.
- CONTROL-STATE.md:196-199 "deterministic gates promoted into the runtime" vs the call graph (library only).
- 001 PROMOTION-QUEUE "no new Canon need was proven" vs CANON-BRIEF:174 (contrast rules present and unconsumed) — not a Canon gap, a Canon-delivery gap; 003 makes the same point for `commercial_communication`.

## 7. Open questions / unknowns

- Whether the Controller's verdicts contain more than the transcriptions (chat only; screenshots for 002 not on disk). UNKNOWN.
- Which V3 frames the Controller meant by "creatives/images being cropped" — my sample did not isolate one (cover() default is code-verified).
- Whether any real production has ever executed `run_loop(frame_sampler=…)` or `pools.py` outside the dry battery — nothing on the three job branches suggests so. HYPOTHESIS: no.
- Whether the 002 candidate gates will be wired before the next tile/format job; the skill's CF2/CF5 rows are the only barrier today and they failed as self-assessed rows on Cumin V1.
- Whether a "learning propagates only through the operator reading case files at BOOTSTRAP" model (BOOTSTRAP.md:27) can scale past three cases — currently every promoted rule that is not code is a sentence in an 887-line skill bundle.
