# 03 — What the earlier pipeline (Media Factory, July–August 2026) actually did

Experiment `RENTOK-CREATIVE-QUALITY-001`, Phase 1 (USD 0). Written 2026-09-21.

Everything in §1–§4 is **HISTORICAL EVIDENCE**: read from the files named, cited by path plus git sha (`media-factory` repo @ `57b2ccabcfddc161256ab6d45ea993204bf7dcdc`, the "spike" commit) or by sha256 for files outside git. §5 is this session's **RECONSTRUCTION** (INFERRED) of which of those practices the current media-agency pipeline keeps, weakens or lacks. §6 is an **OBSERVATION** on the pre-agency `rentok-ad` finals. Where a prompt, reference image, setting or iteration record is missing from the record, that is stated; nothing is filled in.

Freshness: every Media Factory verdict dates from 2026-07-19/20 (spike) and 2026-07-24 (gallery); the handoff pack itself warns the model landscape has moved since. Practices are cited as practices, not as current model capability.

---

## 1. Sources read (all read-only)

| Source | Identity | Used for |
|---|---|---|
| `media-factory/HANDOFF.md` | untracked in git; sha256 `01b832dc…` (2026-07-08) | the production post-mortem and principles |
| `media-factory/CLAUDE.md` | git `5c2d0f4d…` @ 57b2cca | the repo's hard rules (incl. the later-refuted no-model-text rule) |
| `media-factory/spike/brand.json` | git `ebc5f6a0…` | how the character was defined |
| `media-factory/spike/run.mjs` | git `dc729db5…` | reference sheet → reference-conditioned stills → talking takes; take strategy; spend cap |
| `media-factory/spike/grid.mjs` | git `7fc57cad…` | the review grid (contact sheet + pass/fail badges) |
| `media-factory/spike/out/scores.json` | git `0757de99…`; sha256 `8d928dac…` | 64 human pass/fail scores with notes |
| `media-factory/spike/film.mjs` | git `706ee9c5…` | clean plates from customer art; gentle-motion i2v prompts |
| `media-factory/spike/film2.mjs` | git `4395f34d…` | performed scenes, voice casting in-prompt, frame-chaining |
| `media-factory/spike/scene7.mjs` | git `b2e2b67b…`; sha256 `aa7e21c9…` | Wan vs Veo head-to-head from one plate |
| `media-factory/spike/lipsync.mjs` | git `813f1fff…` | the cheap talking-shot ladder |
| `media-factory/spike/assemble.py` | git `8414eb03…` | assembly: audio-led timing, fit video to audio, room tone, loudnorm |
| `media-factory/spike/gallery-video-gen.mjs`, `gallery-media-gen.mjs` | untracked; sha256 `c952e5b5…`, `85aaac8e…` | text-in-scene vs textless + composite comparison |
| handoff pack `media-factory-controller-handoff/` | `MEDIA-FACTORY-EMPIRICAL-FINDINGS.md` sha256 `59037aab…`; `PROMPT-ENRICHMENT-EVIDENCE.md` `f5cbf278…`; `MEDIA-FACTORY-ROUTING-PRIOR.md` `b326f885…`; `SOURCE-INDEX.md` `8e7daa6f…`; `contact-sheets/nano_all32_grid.jpg` `ac904bf6…`; `selected-media/stills/sheet_1.png` `8aad8926…` | the tiered findings, the five prompt-iteration pairs, the routing prior |
| this repo `eval/historical-priors/media-factory-v1/` | `PRIOR-INDEX.yaml` + copies of the four handoff documents | confirms the pack was imported as a prior |
| `rentok-ad/` (30 Aug 2026) | `assets/brief.md` sha256 `fb6bf460…`; `assets/prompts.json` `7826c84a…`; `ad_script.json` `274932ea…`; `RentOk_Owner_Ad_16x9_28s.mp4` `a1619923…`; `RentOk_PG_Ad_9x16.mp4` `0e06d5e4…`; `source-shots/shot_A/B/C.mp4` `993eaf3f…`, `42ef6e4b…`, `e3838bd2…` | the pre-agency RentOk ad: brief, prompts, finals |

Not read: `media-factory/.env` (by instruction); `data/adwisely.db` (PII; not needed).

---

## 2. What Media Factory did — practice by practice (HISTORICAL EVIDENCE)

### 2.1 How references were chosen and supplied

- **The character was defined once, in prose, with an expression.** `spike/brand.json` `character.description`: "Pixar-style 3D animated character: an Indian woman in her late 30s … round tortoiseshell glasses … deep forest-green blazer (hex #1B5E47) over a cream kurta (hex #F4EEE2). **Confident, calm, slightly wry expression.** High-end 3D animation film look, soft cinematic lighting."
- **A turnaround sheet was generated first, from that prose plus the logo as a reference image.** `run.mjs` `sheet`: "Character turnaround reference sheet, three views side by side (front view, three-quarter view, profile view) of the SAME character: ${CHAR} Standing neutral pose … plain light cream background … The Aight brand logo from the reference image printed small in the top-left corner". Two candidates (`seed: 1000 + i`); one chosen (`sheet_1.png`, surviving in the handoff pack).
- **Every scene still was then generated with the sheet AND the logo as reference images**, through an *edit* endpoint, not text-to-image: `stillInput()` → `image_urls: [sheetUrl, LOGO_URI]`; prompt prefix "Using the character reference sheet (first image) — the EXACT same character, same face, same glasses, same silver streak, same green blazer and cream kurta — render her ${sceneDesc}. ${CHAR} Brand palette: … Cinematic 3D animation film still, 16:9."
- **Video was generated from an accepted still**, with the still as the image input (`run.mjs video`, `film.mjs motion`, `scene7.mjs`, `lipsync.mjs idle`): the still is the identity anchor; the prompt restates "The 3D animated style, her face, glasses, outfit and the background stay exactly as in the input image."
- Result recorded (Tier A, `MEDIA-FACTORY-EMPIRICAL-FINDINGS.md` A1): 64 scored stills from one sheet, Seedream 4.5 edit 29/32 pass, Nano Banana Pro edit 25/32 pass; takes-per-keeper 1.10–1.28.

### 2.2 How shots were described

- **Scene descriptions carry action, framing and an emotional/expressive state.** `run.mjs` `SCENES`: "on an office balcony at golden hour holding a glass of cutting chai, **laughing warmly**, Indian city skyline behind, medium close shot"; "pointing at a simple rising line chart drawn on a whiteboard, three-quarter side angle, **engaged teaching expression**"; "arms crossed, **slight confident smile**, full body shot"; "walking down a data-center corridor between server racks, **low-angle cinematic shot**, cool blue-green lighting contrasting her green blazer".
- **Motion prompts describe small, specific, physically plausible movements with their cause**, not categories. `film.mjs` `SHOTS.s07`: "Steady rain falls. The red umbrella tilts slightly as she holds it over him. Rain drips off the umbrella edge. Puddle ripples at their feet. He looks down at her slowly." — then a style lock: "Keep the exact soft watercolor storybook illustration style of the input image. No style change, no new elements, no text. Camera static or drifting very slowly."
- **Performed scenes cast the voices in the prompt** (`film2.mjs`): `HER` = "a woman in her late twenties, LOW and warm, gentle, slightly husky, tender, NOT high-pitched, NOT shrill"; `HIS` = "deep, slow, quiet, weary, with love underneath the tiredness"; a shared `STYLE` block: "The scene is slow and deeply emotional — long pauses, gentle minimal movement, heavy with feeling, no hurry."
- The handoff pack's reading of what this was (`PROMPT-ENRICHMENT-EVIDENCE.md` §2): "Every surviving spike prompt … is a heavily crafted final prompt committed in source: character sheet references, palette hexes, exact-spelling demands, per-voice casting notes … style-lock clauses. These were authored in Claude Code sessions from the raw brand brief … The intermediate drafts were not preserved."

### 2.3 How image and video prompts were constructed — real ones, with paths

| Kind | Path | Prompt (verbatim) |
|---|---|---|
| Still, reference-conditioned | `spike/run.mjs` `stills` | "Using the character reference sheet (first image) — the EXACT same character, same face, same glasses, same silver streak, same green blazer and cream kurta — render her sitting at a tidy desk in a modern Indian office, a laptop with the Aight logo on its lid facing the camera, waving hello at the viewer, medium shot. [CHAR] Brand palette: cream #F4EEE2, ink #15120C, deep green #1B5E47. Cinematic 3D animation film still, 16:9." |
| Clean plate from customer art | `spike/film.mjs` `plates` | "Recreate this exact illustration as a clean full-bleed 16:9 cinematic frame in the identical soft watercolor storybook style: same characters, same composition, same colors, same lighting, same paper texture. REMOVE all text, captions, titles, speech bubbles and white page borders completely. Extend the artwork naturally to fill the whole widescreen frame. No text anywhere in the image." |
| i2v, gentle motion | `spike/film.mjs` `motion` (s04) | "The two keys sway very gently on their hooks. Steam rises in a thin curl from the red coffee cup. The small plant leaves tremble almost imperceptibly. Morning light slowly brightens. Keep the exact soft watercolor storybook illustration style of the input image. No style change, no new elements, no text. Camera static or drifting very slowly." |
| i2v, performed with dialogue | `spike/scene7.mjs` b1 | "[STYLE] The big soft white round character holds the red umbrella over the small girl in red; he is drenched, rain dripping off him. She looks up at him and says, lightly scolding but warm, a young woman's clear voice: 'You're getting wet, idiot.' He looks down at her and answers slowly, a deep soft tired male voice, almost breaking: 'Battu... why are you still here?' Gentle subtle movement, intimate, cinematic." |
| i2v, talking to camera | `spike/run.mjs` `video` | "The woman speaks directly to the camera, warm confident Indian-English accent, natural hand gestures, subtle head movement, office ambience. She says: '[line]' Lip sync matches the words. The 3D animated style, her face, glasses, outfit and the background stay exactly as in the input image." |
| i2v, idle for lip-sync | `spike/lipsync.mjs` `idle` | "The woman sits calmly facing the camera, subtle natural idle motion: gentle blinking, tiny head movements, shoulders relaxed, hands resting on the desk. Mouth stays closed, neutral pleasant expression. No talking. Static camera. Style, face, outfit and background stay exactly as in the input image." |

Settings that survive with them: seeds fixed per take (`5000 + take*37`; `seed: 77` / `21` / `7` / `4242`), durations (`'10'`, `'8s'`), resolutions (`720p`, `1K`), `generate_audio: true` on Veo, `camera_fixed: false` on Seedance. Missing from the record (stated in `SOURCE-INDEX.md`): generator scripts for the VO wavs and the s7 Hindi/dub retake prompts; no raw-vs-enriched pairs; no enrichment logs.

### 2.4 Was an accepted reference still established before video generation?

Yes, as a rule of the harness: `run.mjs video <stillUrl>` takes a still path; `film.mjs motion` refuses if the plate does not exist (`!existsSync(plate)` → error); `scene7.mjs` reads `out/film_s07_plate.png`; `lipsync.mjs` reads `out/nano_desk_t0.png` (a scored keeper: `scores.json` "keeper — logo on lid perfect"). Finding B3 of the handoff pack: "Image-first (hero still → minimal i2v animation) is the high-keep-rate route … 12/12 surviving clean plates → 12 gentle-motion clips".

### 2.5 How identity / continuity was held

- Across stills: the reference sheet + logo in every call (2.1), plus the character prose repeated in full in every prompt (`${CHAR}`).
- Into video: the accepted still as the image input + a style/identity lock sentence in the prompt (2.3).
- Across beats of one scene: **frame-chaining** (last frame of beat N → image input of beat N+1, `film2.mjs` `CHAIN`) — tried and recorded as failing ("generational decay — 'photocopy of photocopy' — plus per-clip voice changes → chaining banned", finding C1, memory-recorded Tier C; the artifacts `f2_s02_b1/b2.mp4` survive).
- Across a short film: identity held per scene from its own plate; voice consistency across clips "unsolved" (C1).

### 2.6 How candidates were inspected and selected

- **Several takes per scene, side by side, scored by a human with a note.** `run.mjs stills`: `for (let take = 0; take < 4; take++)` × 8 scenes × 2 models = 64. `grid.mjs` builds `review.html`: "scenes as rows, takes as columns, one section per model", the sheet at the top, a PASS/fail badge with the note on each cell. `scores.json`: `{"nano_desk_t3.png": {"pass": false, "note": "two laptops"}}`. The handoff pack recomputed keep rates and cost-per-accepted from it (Seedream USD 0.044/accepted vs Nano USD 0.192/accepted).
- **Head-to-head from one plate** (`scene7.mjs`): 2 Wan + 2 Veo on identical prompts and the same plate; Veo refused both; verdict captions on `videos.html`.
- **Iteration on the same plate** (`PROMPT-ENRICHMENT-EVIDENCE.md` P1–P5): three versions of the rain scene from one plate; "direction judged materially better" (P1); "richer prompt ≠ better when it exceeds model grammar" (P5).
- The take strategy the pack *derived* afterwards (`MEDIA-FACTORY-ROUTING-PRIOR.md`): "Generate-1, judge, retry-on-fail … ~90% pass rate makes N=3 wasteful" — while `HANDOFF.md` §5 lists among the baked-in limits "byte-identical reproducibility (blocks generate-many-and-pick-best, which is how good creative is actually made)". Both statements are in the record; they are not reconciled there.
- **Contact sheets of the film** (`_film_plates.jpg`, `_veo0_strip.jpg`, `_wan0_strip.jpg`, `_st_strip.jpg`…): frame strips per clip for inspection.

### 2.7 How assembly / editing was done (`spike/assemble.py`)

- **Audio-led timing.** Per shot, the dialogue/VO wavs are laid out first with fixed gaps (`GAP_DLG 0.45`, `GAP_VO 0.75`, `LEAD 0.9`, `TAIL 1.1`) into a shot audio track; the **video is then fitted to the audio** — trimmed if longer, slowed (≤ 2×, `setpts`) and tail-padded (`tpad … clone`) if shorter — with 0.5-s video fades and 0.3/0.4-s audio fades.
- **End card** from the customer's own title page, 4.5 s with slow fades.
- **Concat, room tone, loudness.** Concat by demuxer; a pink-noise room tone (`anoisesrc … amplitude=0.0035`, low-passed at 500 Hz) mixed under everything; `loudnorm=I=-16:TP=-1.5`.
- No colour work, no cut-on-action logic, no per-shot camera; the edit is a sequence of fitted shots.

### 2.8 The principles the pipeline wrote down for itself (`HANDOFF.md` §5, §11 — verbatim)

- "This one rule [never let a model render the logo/typography] forces every output to be **a photo with a banner stamped on it** instead of a single designed composition. It is the main reason output looks amateur, and no amount of overlay polish fixes it."
- "Other baked-in limits, same class: one hero → one clip; 5s gentle motion only; cheapest models; byte-identical reproducibility (blocks generate-many-and-pick-best, which is how good creative is actually made)."
- "Determinism belongs on the **business** layer (cost, brand accuracy, delivery, audit) — **not** the creative layer, where exploration and selection produce quality."
- "'Deterministic' must mean *encoded expert judgment that adapts to the situation*, not hardcoded constants. Most defects found were constants masquerading as rules."

---

## 3. The pre-agency RentOk ad (30 Aug 2026) — how it was directed (HISTORICAL EVIDENCE)

`rentok-ad/assets/brief.md` is the brief given to a writer/model for the three Veo prompts; `assets/prompts.json` holds the three prompts used for the 16:9 film (hero "Ramesh"); `ad_script.json` holds a four-scene script (hero "Vikram") whose captions match the 9:16 film's on-screen text (OBSERVED on frames: "Register mein sab gol maal", "Leakage, KYC miss, khaali bed"). UNKNOWN from the folder: which prompts generated the 9:16 film's shots, and whether either film was formally accepted (the task brief calls them accepted; no verdict file exists in `rentok-ad/`).

What the brief demanded of each prompt (verbatim, `assets/brief.md`):

- Canon applied as **binding constraints on the creative**, per beat: "MURCH … EMOTION outranks story, rhythm and geometry COMBINED. **Specify the intended feeling PER BEAT**, not once for the film"; "consecutive shots must differ a LOT in scale, light and sound — never a little"; "HEATH … They must arrive as ONE dramatised siege experienced by ONE named man. The viewer should feel five, not count five"; "ONDAATJE … the siege beat must be nearly WORDLESS and let noise do the work; the voice arrives only when the noise drops out"; "KENWORTHY: … Camera movement needs a visible cause in the scene"; "ALTON / FREEMAN: the subject must separate tonally from its background; the light on a face must agree with the light source visible in frame".
- A **fixed emotional structure**: "SHOT A (0-8s) THE SIEGE. Emotional target: besieged, cornered, outnumbered. Near-wordless. / SHOT B … THE COST. Emotional target: the quiet sinking … MUST be a hard visual/sonic break from A / SHOT C … THE TURN. Emotional target: lightness, command, a man back in his own business."
- A **prompt order**: "Specify in this order: shot size and lens, subject and wardrobe, action with a clear beginning and end inside 8 seconds, camera move WITH ITS VISIBLE CAUSE, lighting naming the practical source visible in frame, tonal separation of subject from background, colour treatment, and the audio bed (diegetic sound first, then any voice)."
- **Identity by repetition**: "State his description identically, word for word, in all three prompts so the model holds him."
- **Text suppression**: every prompt ends "No on-screen text, no captions, no subtitles, no signage, no logos, no readable writing anywhere in frame."; "A phone may appear but its screen must be described as glowing light only."

The prompt that resulted (`assets/prompts.json` A, verbatim, 190 words): "Medium shot, 35mm lens, handheld. Ramesh, a stocky Indian man of 48 with greying stubble, wearing a slightly wrinkled sky-blue half-sleeve cotton shirt untucked over grey trousers, a cheap analog wristwatch, and rubber slippers stands in the cramped reception corridor of his PG hostel, a thick worn paper rent-register open on a plastic table before him. Action: three tenants close in from different sides at once, one waving a crumpled electricity bill, one thrusting a phone toward his face, one tapping his shoulder repeatedly; Ramesh's head snaps from one to the other, his hand hovering uselessly over the register, and by the eighth second he freezes, boxed in, the register slipping shut under someone's elbow. Camera move: a fast handheld whip-pan follows Ramesh's own head-turns as he pivots between tenants, motivated entirely by his movement, ending on a tight push-in on his trapped face. Lighting: harsh flat fluorescent tube-light overhead, the visible practical source, flattening the corridor. Tonal separation: his pale sky-blue shirt cuts against the dull beige corridor wall behind him. Colour: desaturated, slightly cool, institutional. Audio: overlapping indistinct tenant chatter, an unanswered mobile phone ringing, rubber slippers slapping tile, a ceiling fan. No music, no narrator, no voice-over, no scripted dialogue. No on-screen text, no captions, no subtitles, no signage, no logos, no readable writing anywhere in frame."

INFERRED: this is the same *kind* of object as Lane A's asset prompts (ordered, concrete, exclusions at the end) — but it carries an emotional target, an action with a beginning and an end, a motivated camera, a lighting mood and a sound bed. Lane A's prompts carry a costume, a pose list and a style block. The difference is not craft; it is *what the plan asked the prompt to carry*.

---

## 4. Keep / lost table — Media Factory and rentok-ad practices vs the current media-agency pipeline (RECONSTRUCTION, INFERRED)

Skill files cited: `.claude/skills/media-agency/SKILL.md`, `PRODUCTION-WORKFLOW.md`, `QA-CHECKLIST.md` (this worktree @ c88c0d5). Lane A record cited from `01`.

| # | Historical practice (source) | In the skill/workflow? | In Lane A? | Status |
|---|---|---|---|---|
| 1 | **Character defined with an expression and a personality** (`brand.json`: "Confident, calm, slightly wry expression") | No field for expression/personality in `JOB-TEMPLATE.yaml` or the Stage-3 template lines (3.1–3.13 are proposition, hero frame, copy, brand, CTA, audio, typography) | No — costume and props only (01 §4, §6) | **LOST** |
| 2 | **Turnaround/reference sheet first, then every still conditioned on it through an edit endpoint** (`run.mjs`) | Partly: `reference_assets[]` roles exist for *supplied* assets; RR-4 makes Seedream edit the default for *supplied photos*; nothing makes a generated sheet the reference for dependents | Sheet generated, then **not used as a reference** for the five obstacles ("A2–A6: text prompt only … optionally A1's accepted sheet as a single style reference … done only if the first text-only obstacle draw mismatches"; Stage 4 §4.7) | **WEAKENED** — kept for supplied assets, dropped for generated ones |
| 3 | **Emotional target per beat, stated before the prompt** (`rentok-ad/assets/brief.md`; `film2.mjs` STYLE) | No: the board schema (`BOARD-v1`) has `beat`, `strings`, `mandatory`; no `feeling`/`emotional_target` field | No — the board is events + strings (01 §4a) | **LOST** |
| 4 | **Prompt order: shot/lens → subject → action with start and end → camera with cause → lighting with practical → tonal separation → colour → audio bed** (`rentok-ad/assets/brief.md`) | Partly: the vendor style (consistent order, concrete nouns, exclusions) is present in the gate and in Lane A's prompts; no rule asks for an *action arc*, a *camera cause* or a *lighting mood* | Style block present; no action arc, no mood beyond "daylight from the upper left" | **WEAKENED** (n/a for stills in part; fully lost for any video prompt because none was written) |
| 5 | **Identity held by repeating the full description word-for-word in every prompt** (`run.mjs` `${CHAR}`; `rentok-ad` rule) | Not a rule; identity is handled by *reuse of one bitmap* or *reference image* | Kept by construction — one sheet, one bitmap for 30 s (stronger than MF's for stills) | **KEPT (by a different mechanism)** |
| 6 | **Accepted hero still before any video** (`run.mjs`, `film.mjs`, finding B3) | Yes — `PRODUCTION-WORKFLOW.md` §6 "motion from an accepted still"; RR-6/RR-8 | n/a (no video); Cumin case applied it (Veo i2v 7/7 clean from plates) | **KEPT** |
| 7 | **Several takes per scene, side by side, human-scored with a note; keep rates computed** (`run.mjs` 4 takes, `grid.mjs`, `scores.json`) | Partly: **one** draw + micro-qualification + freeze (`PRODUCTION-WORKFLOW.md` §7); contact sheets of the *assembly* (`QA-CHECKLIST.md` D13); the routing prior itself says "Generate-1, judge, retry-on-fail" | One draw per asset, 8/8 accepted first time, no comparison across takes | **LOST as comparison; KEPT as verdict-per-draw** (and MF's own record is split on which is right — 2.6) |
| 8 | **Head-to-head on one plate across models** (`scene7.mjs`) | Yes, at the evaluation layer (EVAL-040 routing map), not at job time | n/a | **KEPT (moved to eval)** |
| 9 | **Iterate direction on the same plate and judge the sequence** (P1–P5) | No job-time loop for creative iteration; repair rounds are defect-driven (`qa.defects[]`) | Repair round 1 fixed 10 defects at USD 0 — all *fidelity to the board*, none *direction* | **LOST** for direction; kept for defects |
| 10 | **Style-lock / identity-lock sentence on every i2v prompt** (`film.mjs`, `run.mjs video`) | Implicit in RR-6/RR-8 and in Cumin's prompts ("Static camera, no camera movement … No text, no lettering, no logos") | n/a | **KEPT (by example, not by rule)** |
| 11 | **Frame-chaining banned; ≤ 2 dialogue turns per clip** (C1, C2) | Consistent: `veo-3.1-fast-extend` is `manual_only`; VID-2SPK cells directional | n/a | **KEPT** |
| 12 | **Audio-led assembly: lay the voice track first, fit the picture to it; room tone; loudnorm** (`assemble.py`) | Partly: `VO_SCHEDULE_GATE` promoted from the Cumin case; "VO-first timeline" is a *candidate*; loudnorm present | Picture-led (no voice); loudnorm present | **PARTLY KEPT** |
| 13 | **Let the model draw in-scene text where the model can** (finding A3; `HANDOFF.md` §5 calls the no-model-text rule "obsolete" and "the main reason output looks amateur") | No: RR-1/RR-6 keep exact text by code; IMG-TEXT cells exist (nano-banana-2 4/4) but "code-set on a textless plate" is the default | All 26 strings by code; the phone screen is a rectangle with a raster | **DELIBERATELY NOT KEPT** — a recorded contradiction between MF's post-mortem and the current default; not wrong for HUD labels, arguably wrong for the phone screen and cheat panel (INFERRED) |
| 14 | **"Determinism on the business layer, not the creative layer, where exploration and selection produce quality"** (`HANDOFF.md` §11) | The skill puts determinism on cost/records/QA (business) *and*, for this job class, on the picture itself (`CODE_RENDERED_GAME_FILM` candidate pattern) | The creative layer *was* the deterministic layer | **LOST for this job class** — the very thing MF warned against, chosen for its guarantees (01 §5) |
| 15 | **Per-brand policy pre-flight before promising a premium video model** (A4: Veo refused both beats) | Refusals are counted as attempts; no pre-flight | n/a | **PARTLY KEPT** (counted, not pre-flighted) |
| 16 | **Contact sheets / frame strips of every clip** (`_veo0_strip.jpg` etc.) | Yes — D13, keyframes | Yes — `gen/final/CONTACT-SHEET.png`, `KEYFRAMES.png` | **KEPT** |
| 17 | **Voice chosen by human ear, never by metric** (B2, contradiction 4) | Yes — Cumin and Lane B auditions; "voice-by-ear-first" candidate | n/a | **KEPT** |

Reading (INFERRED): of the practices that bear on *creative quality* — 1, 2, 3, 4, 7, 9, 13, 14 — the current pipeline keeps none intact. Of the practices that bear on *reliability* — 5, 6, 8, 10, 11, 12, 15, 16, 17 — it keeps or improves nearly all. The pipeline inherited Media Factory's controls and not its creative loop. That is consistent with what 02 found: presence and correctness are excellent; feel was never loaded.

Two of the "lost" items were never in Media Factory either, strictly: an emotional-target-per-beat field (3) and the five-part prompt order (4) are from the **rentok-ad brief** (30 Aug), which post-dates Media Factory and pre-dates the agency skill; they are the nearest thing in the record to a "stronger" RentOk direction and they were not carried into the skill.

---

## 5. The `rentok-ad` finals — what makes them read as "stronger" (OBSERVATION)

Frames extracted by this session to `evidence/frames-rentok-ad/` (7 per film at 2/6/10/14/18/22/26 s; 640-px and 360-px reductions). Files: `RentOk_Owner_Ad_16x9_28s.mp4` (1920×1080, 28.0 s) and `RentOk_PG_Ad_9x16.mp4` (1080×1920, 35.6 s).

OBSERVED on the frames:

- **Human scale.** In the 16:9 film the hero's face occupies roughly 25–45 % of frame height in Shot B and the close of Shot A; in the 9:16 film the hero fills 40–70 % of frame width in most frames. Lane A's owner is 13.5 % of frame height.
- **A face that changes.** Shot A: eyes darting, mouth tight, three tenants pressing in (t02, t06). Shot B: head in hand under a single lamp (t14). Shot C: relaxed, smiling toward the skyline (t18, t22). The 9:16 film: rubbing the temple in the dark (t02), a frown over cash (t10), a satisfied smile on a sofa (t18), a proud walk down a lit corridor (t26).
- **Lighting that changes with the beat.** Flat fluorescent → one warm desk lamp against black → golden morning; the 9:16 film moves from amber-and-blue night to bright daylight to golden hour. These match the brief's "MUST be a hard visual/sonic break" and Canon `sk_alt_c003_0022` (drama lighting "fluctuates across the film … gay sequences lit brightly, sad scenes lower").
- **A camera with a cause.** Whip-pan on head turns; push-in as he sinks; tilt up steam. (INFERRED from the prompts and consistent with the frames; motion itself not verifiable on stills.)
- **Physical crowding as the obstacle.** The five problems arrive as people and paper around one man (Heath: "feel five, not count five"), not as five labelled sprites.
- **Minimal composited text.** One short line per beat (16:9: "Rent in 5 days. Automatically."; 9:16: caption plates), the logo and one proof line on the end card. The picture carries the story; the text annotates it.

INFERRED, stated as an observation not a verdict: what reads as "stronger" is (i) the viewer is *close* to a *face* that *changes*, (ii) light and sound change with the emotional beat, (iii) the obstacle is physical and crowds the hero, (iv) the picture, not the label, carries the meaning. None of these four depends on photorealism; all four are absent from both RentOk game films (02 rows 1, 3, 6, 9) and all four are things the rentok-ad brief *asked for in writing* before any prompt was written.

Caveats: the game brief is a different form (a game, not a drama) and the customer asked for it; a game film cannot copy a live-action grammar. What it can copy is the *direction discipline* — a stated feeling per beat, a framing objective, an action with a start and an end, a light/sound change at the turn — which is method-independent.

---

## 6. Things the record does not contain (UNKNOWN — stated, not filled)

- Any raw-vs-enriched prompt pair, or any enrichment log (handoff pack: "No controlled raw-vs-enriched A/B exists anywhere").
- The prompts for the 9:16 `rentok-ad` film's generated shots (only `ad_script.json`'s `veo_prompt` fields exist; whether they were sent verbatim is not recorded).
- Acceptance records for either `rentok-ad` final.
- The intermediate drafts behind any Media Factory prompt.
- Any Media Factory attempt at a game-style or code-rendered film (none exists; the nearest is the deterministic composite over a Veo base, `aight_chai-composite.mp4`).
