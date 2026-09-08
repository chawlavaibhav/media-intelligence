# Media Factory — Empirical Findings (evidence-recovered)

Prepared 2026-08-28 for the Controller of `chawlavaibhav/media-intelligence`.
Source repo: `~/Vaibhav_Personal_Projects/media-factory` (read-only extraction; nothing modified or rescored).

**Evidence tiers used throughout:**
- **Tier A — Strongly evidenced:** surviving artifacts + a written human score or head-to-head comparison.
- **Tier B — Directional:** surviving artifacts + operator captions/judgments, but small n or no formal scoring.
- **Tier C — Operational anecdote:** recorded in project memory / handoffs; artifacts may survive but the specific judgment was never written into a scoreable ledger.

**Freshness warning (applies to everything below):** all model verdicts date from **2026-07-19/20** (spike) and **2026-07-24** (gallery). A later verified check (project memory `video-model-landscape-2026-08`, web-verified 2026-08-13) already shows the landscape moved: Veo 3.1 Fast became the *cheap* dialogue option ($0.10–0.15/s with native lip-sync), Seedance 2.0/2.5 became the *expensive* quality king, Kling 3.0 Turbo appeared as the volume tier. Every routing conclusion here is a **historical empirical prior**, not an August-2026 capability claim.

---

## A. Strongly evidenced findings

### A1. Character consistency via reference-conditioned edit works (the load-bearing bet)
- **Evidence:** 64 scored stills (`spike/out/scores.json`, `spike/out/review.html`, artifacts on disk), generated from one character turnaround sheet (`sheet_1.png`) + logo ref, 8 scenes × 4 takes × 2 models. Harness: `spike/run.mjs` (committed).
- **Sample:** n=64, all human-scored pass/fail with notes.
- **Result:** Seedream 4.5 edit **29/32 pass (90.6%)** at $0.04/img; Nano Banana Pro edit **25/32 pass (78.1%)** at $0.15/img. Takes-per-keeper 1.10 (Seedream) / 1.28 (Nano) — far better than the feared many-runs-per-keeper.
- **Conditions:** Pixar-style 3D character (Aight brand), 16:9, seeds fixed per take, same sheet as ref for every take.
- **Date/cost:** 2026-07-19; stills ledger $4.80 (nano) + $1.28 (seedream).
- **Stale risk:** model versions (nano-banana-pro, seedream v4.5) have likely been superseded; the *mechanism* (multi-angle ref sheet → edit endpoint) was independently corroborated as industry practice in the Aug-2026 landscape check.

### A2. Nano Banana Pro and Seedream 4.5 fail differently
- **Evidence:** the fail notes in `scores.json` (all 10 fails enumerated).
- **Nano fails (7):** identity/object drift — "two laptops", "face drift — younger, streak moved", "outfit changed to pants", "blazer color split", "logo floating mid-air", "bg logos mirrored", one occlusion. Zero pure-text failures on exact-headline scenes except one layout occlusion.
- **Seedream fails (3):** all text/layout — "text collides with head", "rendered hex codes from prompt" (leaked prompt content into the image), "wordmark missing". **Zero identity-drift failures.**
- **Reading:** Seedream held the character better; Nano held text/craft better. Different QA checks are needed per model.
- **Date:** 2026-07-19. Human-scored: yes.

### A3. In-scene generated text in STILLS was largely reliable (letter-perfect headlines happen)
- **Evidence:** the "sign" scene demanded the exact sentence "Get AI working for your business."; the "poster" scene demanded "your AI, right." — scores show nano_sign 3/4 "headline exact", nano_poster 4/4 "poster perfect", seedream_sign 2/4 exact, seedream_poster 3/4. Artifacts survive (see `selected-media/stills/`).
- **Contradicts** the repo's hard rule 5 ("NEVER ask a model to render logo/typography") — and `HANDOFF.md` §5 itself flags that rule as **obsolete** and names it the root cause of amateur-looking output.
- **Human-scored:** yes (subset of A1). Date 2026-07-19.

### A4. Veo can refuse content that Wan performs (policy asymmetry)
- **Evidence:** `scene7.mjs` scheduled 2 Wan + 2 Veo generations of the same rain-scene dialogue beats from the same plate. Ledger (`costs.jsonl`) contains **only** `scene7/wan_b1`, `wan_b2`, `music` — no Veo charges; no Veo files on disk; `videos.html` caption: "Veo refused the scene entirely (content filter vs Battu's childlike design) — so this is Wan, the only engine that would perform it."
- **Sample:** n=2 refusals on one art style; consistent across both beats.
- **Implication recorded at the time:** premium tier ≠ available tier; per-brand policy pre-flight needed before promising Veo.
- **Date:** 2026-07-20. Cost: $0 charged for refusals.

### A5. SadTalker route rejected; LatentSync route accepted as the cheap talking shot
- **Evidence:** artifacts `vid_sadtalker.mp4` (256px face crop) vs `vid_latentsync*.mp4` (full-frame 12.8s talking shots); `videos.html` verdict captions; ledger $0.10 vs $0.07/shot.
- **Result:** SadTalker "works but outputs a tiny 256px face crop — not delivery quality" (hard fail). LatentSync (Seedance idle clip + TTS wav + mouth repaint) = "the current best ₹20 shot" with character+logo intact.
- **Human-scored:** operator verdicts written in the review page; user ear-verdict recorded (ishita > kavya).
- **Date:** 2026-07-19. Route cost ~₹16–25 vs Wan ₹42 vs Veo ₹105.

## B. Directional findings

### B1. Wan 2.5: strong cinematic/performed-scene engine; degrades small in-scene text in motion
- **Evidence:** talking takes `vid_wan_t0-2` (caption: "watch the laptop tagline decay"), Hinglish takes approved by user's ear at ₹42; rain-scene performance labeled "The verdict piece" and the Hindi retake "the candidate recipe for the whole film" (`videos.html`); frame strips `_wan0_strip.jpg`, `_wan12_strip.jpg`.
- **n:** ~10 kept Wan clips (14 billed). No per-take pass/fail ledger — hence directional.
- **Date:** 2026-07-19/20.

### B2. Voiceover route was serviceable for narrated/explainer work; voice was the named weak link
- **Evidence:** Sarvam bulbul:v3 four-speaker test + polish chain (artifacts `vo_*.wav`), ElevenLabs v3 acted test (`el_sarah_v3.mp3` — inline acting tags work), full ladder published on `videos.html`. Operator verdict recorded: Sarvam "not very good but not bad"; ishita chosen by ear over metric-picked kavya.
- **n:** 4 Sarvam speakers + 3 EL takes + 4 lip-synced composites. Not formally scored.
- **Date:** 2026-07-19.

### B3. Image-first (hero still → minimal i2v animation) is the high-keep-rate route
- **Evidence:** 12/12 surviving clean plates → 12 gentle-motion clips assembled into `pixels_to_dawn.mp4` (film v1); gallery pair `nano_chai-textless.png` → Veo push-in base → deterministic composite; production recipes are built exactly this way (`packages/recipes/src/*.ts`). Still-level keep rates are Tier-A (A1); clip-level acceptance is operator judgment.
- **Date:** 2026-07-20/24.

### B4. Deterministic compositing guarantees exact text — at an aesthetic price
- **Evidence:** surviving composite `aight_chai-composite.mp4` (sharp SVG Devanagari overlay on a textless Veo base — text pixel-sharp by construction) vs `wan_chai-sign.mp4` (model-generated Devanagari sign in motion, generated to demonstrate smearing). Production compositor code + legibility regression tests exist on branch `fix/legible-ad-composite`.
- **Counter-evidence in the record:** `HANDOFF.md` §5 states the composite-always rule is the main reason production output looked amateur ("a photo with a banner stamped on it").
- **No surviving production ad composites** — Render `/data` outputs were not preserved in the repo.

### B5. Prompt/voice direction iteration visibly changed outcomes on the same plate (n=3 versions)
- **Evidence:** three surviving versions of the same rain scene from the identical plate: `s7_preview.mp4` (native EN voices) → `s7_dub_preview.mp4` (external acted audio; dub) → `s7_hindi_preview.mp4` (Hindi + heavy in-prompt voice direction; labeled the candidate recipe). See PROMPT-ENRICHMENT-EVIDENCE.md.
- Directional: operator-judged sequence, no blind comparison.

## C. Operational anecdotes (memory/handoff-recorded; not independently scoreable from surviving artifacts)

These are recorded in project memory (`media-factory-project.md`, sections dated 2026-07-19/20) and referenced by the spike commit message ("Findings recorded in the project memory"). Artifacts survive for most, but the specific judgments were never written into a scoreable file:

- **C1. Multi-turn dialogue laws (guddu film test, ~₹1,050 burnt):** >2 speaker turns per 10s Wan clip → lips desync + lines bleed into the wrong character; frame-chaining beats → generational decay ("photocopy of photocopy") + per-clip voice changes → chaining banned; voice consistency across Wan clips unsolved. Artifacts survive (`f2_s02_b1.mp4` → chained `f2_s02_b2.mp4`) but the desync/decay judgments are memory-recorded.
- **C2. Wan `audio_url` is a soundtrack slot, not a lip-sync driver** — the dub attempt (`s7_wan_dub_b1.mp4`, survives) was out of sync.
- **C3. Actual fal bill vs ledger:** dashboard-checked spike bill $22.38 including ~₹500 of ghost clips (14 Wan billed vs 5 kept, polling bug). The on-disk ledger totals $35.28 because it over-counts retried attempts. Neither number is authoritative alone.
- **C4. User ear-approvals (2026-07-19):** Wan Hinglish ₹42 and Seedance b-roll ₹35 both pass; budget-tier benchmark video ~₹850–1,150 validated vs the RentOk/Flow ₹250 benchmark.
- **C5. Production quality arc (V0–V2):** business-name-in-image-prompt bug and its fix (productVisual), GPT Image 2 swap, white-on-white legibility failure and the adaptive-contrast fix — all recorded in memory/commits; no scored output corpus survives.
- **C6. ElevenLabs western accent rejected by user's ear even in English** (guddu dub).

---

## The 12 claims — verdicts

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | Wan worked for most general/cinematic cases but not certain talking-to-camera cases | **PARTIALLY_SUPPORTED** | Cinematic strength: `s7_*` + `f2_*` artifacts + videos.html verdicts (Tier B). The recorded talking-camera weaknesses are specific: small in-scene text decays (`vid_wan_t0` caption) and multi-turn dialogue desyncs (Tier C, artifacts survive). Single-turn talking-to-camera actually *passed* the user's ear at ₹42 — so "not certain talking cases" is right, but narrower than remembered. |
| 2 | Voiceover was reliable for a significant class of jobs | **PARTIALLY_SUPPORTED** | Full voice ladder survives (`vo_*`, `el_*`, latentsync composites, videos.html). Narrated/explainer class validated by user approval (Tier B/C); but the record also says voice was "the weak link" and Sarvam "not very good but not bad". |
| 3 | Generated text was unreliable | **PARTIALLY_SUPPORTED** (and partly CONTRADICTED) | In **stills**, contradicted: scored letter-perfect headlines/logos (A3); HANDOFF.md declares the no-model-text rule obsolete. In **video motion**, supported: Wan "tagline decay" caption + the gallery `wan_chai-sign.mp4` built to demonstrate smearing. Treat as: stills-reliable (2026-07 models), in-motion-unreliable. |
| 4 | Deterministic compositing solved text/logo reliability | **PARTIALLY_SUPPORTED** | Mechanism + one surviving composite artifact (B4) + legibility test suite. But no production composited-ad corpus survives, and HANDOFF.md records the aesthetic cost of composite-always. |
| 5 | Lip-sync worked under some workflows but not others | **SUPPORTED** | Differential outcomes with artifacts: LatentSync route accepted, SadTalker rejected (256px), Wan audio_url dub out-of-sync (C2), Veo/Wan native lip-sync in talking takes (A5, B1). |
| 6 | Two-person dialogue had no satisfactory route at the time | **PARTIALLY_SUPPORTED** | **Multi-turn** two-person dialogue: supported — the guddu laws (C1) + surviving chained-beat artifacts; drama genre was to be declined at intake. **Single-beat ≤2-turn** dialogue: contradicted — the Hindi rain scene on Wan was judged "perfect" / "the candidate recipe" (`s7_hindi_preview.mp4` survives). |
| 7 | Claude prompt enrichment before Wan materially improved output vs raw prompts | **NOT RECOVERABLE** | No paired raw-vs-enriched generations exist; no enrichment logs survive. All surviving media prompts are already-crafted finals inside committed scripts. Closest surviving evidence is the same-plate prompt-iteration sequence (B5) — directional only. See PROMPT-ENRICHMENT-EVIDENCE.md. |
| 8 | A working model-routing strategy existed, selecting workflows by task/capability/cost | **PARTIALLY_SUPPORTED** | No automated router exists anywhere in the code (registry is id-lookup only; model choice = env vars). What existed: capability descriptors on adapters, env-selectable endpoints, and a **human-learned routing policy** with explicit price/quality tiers (videos.html ladder; memory: "Veo demoted to fallback-only", "ration lips-on-camera", genre gate at intake). See MEDIA-FACTORY-ROUTING-PRIOR.md. |
| 9 | Image-first hero generation + minimal i2v animation produced strong accepted outputs | **SUPPORTED** | A1 keep-rates on ref-driven stills (Tier A) + B3 pipelines + production recipes built on exactly this shape + Aug-2026 landscape note corroborating keyframe-first keep-rates. Clip-level acceptance is operator-judged rather than ledger-scored — noted. |
| 10 | Character/brand consistency experiments produced the reported scored results | **SUPPORTED** | Recomputed from `scores.json`: nano 25/32 (78.1%), seedream 29/32 (90.6%), takes-per-keeper 1.10–1.28 — matches the remembered "78% / 91% / 1.1–1.3" exactly. |
| 11 | Nano Banana and Seedream had different characteristic failure profiles | **SUPPORTED** | A2: nano = identity/object drift + logo hallucination; seedream = text/layout (incl. rendering hex codes from the prompt); zero seedream identity fails. |
| 12 | Verified economics / cost-per-accepted / route cost comparisons | **PARTIALLY_SUPPORTED** | Unit prices per artifact in `costs.jsonl` + PRICES map; route ladder in ₹ published on videos.html; dashboard-verified spike bill $22.38 (C3). Cost-per-accepted was never computed historically; derived now from A1: **seedream $0.044/accepted still vs nano $0.192/accepted** — 4.4× cheaper per keeper. Ledger has known over/under-counting (retries, ghost clips, Sarvam/EL not logged). |

## Major contradictions between remembered conclusions and surviving evidence

1. **CLAUDE.md hard rule 5 ("never let a model render logo/text") vs the scored spike record.** The rule is still written as non-negotiable in the repo's CLAUDE.md, while scores.json shows letter-perfect in-scene headlines/logos and HANDOFF.md names the rule as the root cause of amateur output. Any new project inheriting CLAUDE.md verbatim inherits a refuted rule.
2. **"No satisfactory two-person-dialogue route" is over-broad as remembered.** The surviving record splits it: single-beat ≤2-turn dialogue on Wan was judged the candidate film recipe; only multi-turn and chained dialogue failed.
3. **"A model-routing strategy existed" suggests code; the code contains none.** Routing lived in humans + env vars + a published price ladder. If media-intelligence expects to inherit a router, there is nothing to inherit beyond the policy table in MEDIA-FACTORY-ROUTING-PRIOR.md.
4. **Metric-vs-ear disagreement:** RMS-dynamics picked kavya as the most expressive voice; the user's ear picked ishita. Recorded lesson: voice choice must be a human/brand decision, never auto-picked.
5. **Ledger vs bill:** $35.28 (ledger) vs $22.38 (dashboard, spike period) — neither is a clean spend record; treat all cost totals as bounded estimates.
