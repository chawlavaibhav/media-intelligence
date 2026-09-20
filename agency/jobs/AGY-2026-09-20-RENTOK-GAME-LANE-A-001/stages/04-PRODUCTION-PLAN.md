# Stage 4 — Production selection (gate: riskiest element tested first; every route has evidence or a test; balances read)

Job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001`. Template lines 4.1–4.10. Prices are live PriceBook quotes (`tools/dispatch.py quotes`, USD 0); cell status and `production_use_allowed` from `stages/evidence/routing-table.txt`. **No paid call has been made; `CAP_USD = 0.0`.**

---

## 4.0 Production approach in three lines

1. The film is a 2-D side-scroller **rendered by code** (Pillow frames → ffmpeg): level, scrolling, jumps, hits, projectiles, health bar, checklist, cheat panel, flag, end card, every exact string — deterministic timing, byte-exact text, one character bitmap for all 30 s.
2. Generative models supply only **textless stills**: one PG-owner sprite sheet, five obstacle sprites, one background plate (Nano Banana 2, credits) — cut out by code and animated by code; the powered state is a code recolour + aura of the same sprite, so identity cannot drift.
3. Audio: one original music bed (Lyria, credits) trimmed by code + code-synthesised SFX; no voice.

Why not generative video: the brief needs (a) one character identical across 30 s, (b) readable in-game text on every frame, (c) obstacles physically hit by projectiles at exact times, (d) 30.0 s exactly. Every video route in the table is 4–15 s per clip, identity across clips is a directional risk (case 002 RO-02; case 001 RO-02 extend drift), and in-motion text is the defect the packs guard against (EVAL-038, RR-6). Code satisfies all four at USD 0 per re-render.

## 4.1 Highest generative risk — from evidence, not the author's label

| Rank | Element | Risk (with source id) | Why it is ranked here |
|---|---|---|---|
| **1** | PG-owner sprite sheet (4 poses on one flat background) | Nano Banana 2 drew paper-like text marks once despite "no readable text" (case 001 RO-04, n=2, 1 clean); no evidence anywhere for multi-pose sprite-sheet consistency or for a keyable flat background (GAP → `test`) | every frame depends on it; a wrong character = creative-direction repair (Stage 1 D3, the one high-cost assumption) |
| 2 | Background plate (PG street / facade) | street scenes invite signage: RO-04 (nb2 environmental text), RO-06 (a video route sharpened blurred signage into letters; directional, different route), EVAL-038 (both videos failed on baked-in text) | a letter-shaped mark anywhere fails D1/CF3; fallback exists (code-drawn plate) |
| 3 | Five obstacle sprites | picture must say the problem before the label does; no identity requirement; risk is misreading, not drift (no case id — reasoning) | one repair each is priced; LJ per obstacle |
| 4 | Music bed | Lyria returned 503/500/500 on a wording-heavy prompt, succeeded on a neutral rewrite (RO-09, SD-10, n=4); tracks ≈ 32.8 s (RR-13) | neutral wording; trim by code; a refusal is `infrastructure_transient`, counted |
| 5 | Code animation feel (pacing) | a pipeline risk, not generative: case 001 SD-13 "creative architecture re-litigated across versions" | mitigated by a **USD-0 animatic** (grey placeholder sprites, full 30 s) rendered and checker-inspected BEFORE any paid draw |

**Micro-qualification (`plan.micro_qualifications[0]`)**: one draw of the sprite sheet (USD 0.067), cut out by code, placed at final size (220 px) on the animatic frame, checker-inspected against: four poses read as one person; keys + register visible at 220 px; no lettering; background keyable (≥ 98 % of border pixels within tolerance of the flat colour); not a Nintendo silhouette (Stage 2c). Verdict → freeze the sheet (sha256 into `plan.assets[]`) → then dependents. Fallback if the sheet fails twice: best single pose + code bob for the run cycle (recorded).

## 4.2 Assets, routes, evidence, price, pool

| id | Asset | Method | Depends on | Route (cell) | Status / use / accepts | Unit price (live) | Draws planned (+repair) | Reason tied to this plan |
|---|---|---|---|---|---|---|---|---|
| A0 | Animatic (grey boxes, full 30 s, all strings) | code | board.json, copy-deck.json | code | — | 0 | — | proves timing, text placement, safe zones and the muted test at USD 0 before any spend |
| A1 | PG-owner sprite sheet (idle, run A, run B, jump; 1:1) | AI still → code cut-out | — | IMG-CORE / nano-banana-2 | clean_observed / True / 7/8 | 0.067 per_image | 1 (+1) | riskiest; identity over 30 s comes from reusing one bitmap |
| A1p | Powered owner (cyan palette shift + aura) | code | A1 | code | — | 0 | — | identity guaranteed; the visible change is deterministic |
| A2–A6 | Obstacle sprites ×5 (document wall; padlocked sack; fleeing tenant; ledger tower; ticket swarm), each 1:1 on flat green | AI still → code cut-out | A1 (style match by prompt, same palette words) | IMG-CORE / nano-banana-2 | clean_observed / True / 7/8 | 0.067 | 5 (+2) | five distinct pictures at 250 px; a wrong read is repaired singly |
| A7 | Background plate 9:16 (sky, PG facade, rooftops, lane; no ground tiles; no signs) | AI still (code fallback) | — | IMG-CORE / nano-banana-2 (9:16) | clean_observed / True / 7/8 | 0.067 | 1 (+1) | parallax layer; fallback = code gradient + block facade. Cell choice (checker NOTE 8): the more specific VID-TOPO3/nano-banana-2+A2_nb_plate_9x16 is directional/manual_only and describes a still-to-video topology this plan does not use; the general clean IMG-CORE cell plus case 002 RO-04 (1/1 clean 9:16 plate, same surface) is the evidence used |
| A8 | Ground tiles, flagpole + flag, phone item, tick projectile, hit flash, confetti, panel, chips, HUD | code (pixel primitives + pixfont) | — | code | — | 0 | — | exact geometry and brand colours; no lettering risk |
| A9 | Wordmark placements (HUD chip, phone screen, end card) | code composite of the fetched raster | `source/rentok-brand/rentok-new-logo.webp` @ sha256 1ff7dcf5… | code | — | 0 | — | brand fidelity (Stage 2d); mechanism B |
| A10 | Music bed 30 s | generative audio → code trim + loudness | — | MUS / lyria+native | clean_observed / True / 4/4 | 0.06 per_clip | 1 (+1) | original audio (Meta "no licensed music"); chiptune character by prompt |
| A11 | SFX set (jump, hit, key-click, power-up, pew, burst, ding, fanfare, end hit) | code (ffmpeg `aevalsrc`/`sine` synthesis) | — | code | — | 0 | — | no licensed sample; exact timing from board.json |
| A12 | Assembly: 900 frames → H.264 MP4 + AAC mix | code (ffmpeg) | A0–A11 | code | — | 0 | — | Stage 2.1 encode row |
| A13 | Deliverable `RENTOK-GAME-LANE-A-001_9x16_1080x1920.mp4` | — | A12 | — | — | — | — | the one delivered geometry (`plan.deliverables[0]`) |

Fallback cells: none needed on a `False` cell; if Nano Banana 2 refuses or is unavailable (infrastructure_transient), the declared fallback is **IMG-CORE / nano-banana-pro** (clean_observed, True, 4/8, USD 0.134, credits) — used only on the Controller's OK because it doubles the unit price; otherwise wait and re-attempt as a new counted attempt. No `manual_only` and no `False` cell is used. Surface note: the map lists nano-banana-2 on `vertex`; this job calls the Gemini API endpoint as cases 001/002 did (RO-04 in both), same Google credits pool — recorded, not hidden.

`plan.assets[].reuse`: null for every asset (nothing carried in from earlier work; DESIGN_REUSE_PROVENANCE G1–G4 satisfied by absence).

## 4.3 Known failures per route (directional; routing_authority none)

- nano-banana-2: environmental lettering despite a no-text clause (case 001 RO-04 r1); clean when paper/notes/posters were explicitly forbidden (RO-04 r2); GyaanBox plate 1/1 clean with "upper half clear" (case 002 RO-04). → Every prompt forbids "signs, boards, posters, papers with writing, letters, numbers, logos"; every still is frame-scanned by eye + the gate's post-draw path; a plate with letter-like marks is painted over by code or replaced by the code plate.
- lyria: 3 provider errors on wording naming "advertising / creative studio / 58-second" (RO-09); neutral prompt succeeded first time; 32.8 s output (RR-13). → Prompt: "upbeat 8-bit chiptune instrumental, bright square-wave lead, driving bass, 140 bpm, playful, loop-friendly" — no brand, no ad words; trim to 30.0 s with a 0.4 s fade.
- code compositor: the four V3 failure classes (clipped text, lost contrast, accidental crops, elements over the subject — case 001 SD-01..04, recurring in case 002 HD-01..10 when gates were bypassed). → the runtime gates run on every rendered text box (4.4).

## 4.4 Text, logo, UI generated? — No. Everything composited

`plan.composite[]` = every string in `copy-deck.json` (rendered by `tools/pixfont.py`, byte-exact by construction), the wordmark raster (three placements), the phone screen, the HUD, the panel, the chips, the flag. Generation prompts carry the LIMIT-TEXT clause and are grepped for every critical deck string and for the Nintendo names (`tools/dispatch.py _prompt_guard`, proven to refuse at USD 0). Deviation from the generic "hb-view + Pillow" shaping: Latin capitals in a code bitmap font need no shaping engine; the exact-copy check is a string comparison against the deck plus glyph coverage (`pixfont.py coverage`: none missing).

## 4.5 / 4.6 Voice

`plan.voice.source_count = 0` — no voice (Stage 3 D-1). 4.6 (VO durations before shot durations) is n-a; shot durations come from `board.json` and are exact by construction.

## 4.7 References

A1 (sprite sheet): no reference image — text prompt only (an IMG-CORE draw, the clean cell). A2–A6: text prompt only, sharing the palette and outline words of A1's prompt; **optionally** A1's accepted sheet as a single style reference — that would make the call an unregistered reference use on this route (the kit's note), so it is done only if the first text-only obstacle draw mismatches the style, and then recorded as a micro-qualification with its own checker look. A7: text only. ≤ 1 reference per call in every case.

## 4.8 Pool balances — read, not attested

**RESOLVED 2026-09-21 by human attestation (checker 4-B / Controller message).** A machine reading is not available: the project service account cannot call Cloud Billing (the API is disabled on vertexaiproject-507518 — verified by the Controller session). The human Controller attested "Yes, credits are funded — proceed" (Controller session AskUserQuestion, 2026-09-20T18:44Z); recorded in `JOB.yaml spend.pool_readings` as `attested_by_human`. Assumption recorded: both credentials the tool uses (the Gemini API key for Nano Banana 2; the Vertex service account for Lyria) draw on the same Google credits pool, as in the Cumin experiment ledgers — cost if wrong: a call could bill a different account or hit a quota; rule: any billing/quota error → stop and report, never retry on another surface. Every reservation is an upper bound. Original text follows for the record: The Controller named the pools (Google Vertex/Gemini credits; ElevenLabs; Sarvam) as existing, but a reading (balance value, read_utc, source) did not exist in this job at Stage 4. The plan touches one pool: Google credits (nb2 + Lyria, ≈ USD 0.53–1.06). Under PROVIDER_POOL_AVAILABILITY (case 001 SD-11) no dispatch happens on an unread pool. Request to the Controller, to travel with the written cap: the current Google Cloud credits balance for `vertexaiproject-507518` (console reading with UTC), or authorisation for a `gcloud billing` read from this session. `spend.pool_readings` stays empty until then.

## 4.9 Expected spend vs the provisional cap (USD 10.00, unconfirmed)

| Line | Draws | Unit | USD |
|---|---|---|---|
| A1 sprite sheet — micro-qualification | 1 | 0.067 | 0.067 |
| A2–A6 obstacles | 5 | 0.067 | 0.335 |
| A7 plate | 1 | 0.067 | 0.067 |
| A10 music | 1 | 0.060 | 0.060 |
| **Base plan (no failures)** | | | **0.529** |
| Repair round: A1 ×1, obstacles ×2, plate ×1, music ×1 | 5 | — | 0.328 |
| **Base + one repair round** | | | **0.857** |
| Customer SPECIFIC-REPAIR reserve (3 stills) | 3 | 0.067 | 0.201 |
| **Planned ceiling** | 16 calls | | **1.058** |

10.6 % of the provisional USD 10.00; 0 hidden retries; every failed call counts. Infrastructure failures (5xx/UNAVAILABLE) reserve at full price and are re-sent only as new counted attempts inside the ceiling.

If the confirmed cap is lower: ≤ USD 1.00 → drop the customer-repair reserve (0.857); ≤ USD 0.60 → plate by code, obstacles get one shared repair (0.529 → 0.596 max); ≤ USD 0.30 → sprite sheet + music + two obstacles generative, three obstacles by code pixel art (≈ 0.26); USD 0 → a fully code-drawn film (all sprites as pixel primitives) — deliverable, weaker character.

## 4.10 Order of work

1. USD 0: A0 animatic rendered from board.json (grey sprites, all strings, HUD, panel, chips, end card) → contact sheet → checker look at timing, safe zones, readability.
2. USD 0: pre-dispatch checks (A1–A10 of QA-CHECKLIST) — `canon/gate/run_gate.py pre` over the package + the seven prompts; prompt guard; cap recorded; pool reading recorded.
3. Paid, after the written cap: A1 sprite sheet → cut-out → checker verdict → freeze.
4. A2–A6 obstacles (one call each, inspected each) → A7 plate → A10 music.
5. Engine render with real sprites → SFX → assembly → post-draw QA (below) → contact sheet → human release surface.

## 4.11 Text rendering, audio, assembly — the exact tools to be written (Stage 5)

| Tool | Does |
|---|---|
| `tools/pixfont.py` (exists) | bitmap font; audition; glyph coverage |
| `tools/prompts.py` | the seven generation prompts as data (gate-conformant; guarded) |
| `tools/cutout.py` | keys the flat background → RGBA; checks border keyability ≥ 98 %; adds/validates the 2-px outline; grayscale separation (PA-D5) |
| `tools/render_game.py` | the engine: reads board.json + copy-deck.json; draws 900 frames at 1080×1920; writes `gen/layout-log.jsonl` (every text/logo box per frame) |
| `tools/sfx.py` | ffmpeg-synthesised SFX at the board's timestamps → one stereo stem |
| `tools/assemble.py` | music trim/fade, SFX mix, loudness to −14 LUFS / −1 dBTP (`loudnorm`), H.264 High 4:2:0 30 fps ≈ 9 Mbps + AAC-LC 48 kHz 192 kbps, `+faststart` |
| `tools/qa_checks.py` | DET: ffprobe geometry/codec/duration/moov; safe-box check over `layout-log.jsonl` (via `runtime.compositor.gates.check_text_bounds` with the safe box as container); contrast over real pixels (`check_contrast`) per string; exact-copy byte check deck ↔ layout log; forbidden-claims scan; frame sampling every 1.0 s + at cuts → `qa/` contact sheet; `runtime/loop/frame_hygiene.assess` over the human-eye frame verdicts |

## 4.12 QA plan — every acceptance-contract item → a named check

| Item | Check (name · class · tool/judge) |
|---|---|
| A1 platform game | `LJ-A1` · checker on the contact sheet (level, player, obstacles, HUD, flag; game is the film) · HJ customer |
| A2 PG owner | `LJ-A2` · checker names the cues at F1 and F9.2 · `DET-A2` HUD_NAME in layout log on every gameplay frame |
| A3 five obstacles | `DET-A3` · OBST_1..5 byte-present in the layout log at F2–F6 and F9.1–F9.5 · `LJ-A3` per-obstacle checklist (picture reads without the label) |
| A4 install = turning point | `DET-A4` · board.json `install_event_t` = 17.4 s within 10–20 s; CHEAT_1/CHEAT_2 boxes present at F7 · `LJ-A4` visible state change (desaturate → colour, health refill) |
| A5 enhanced ability | `DET-A5` · powered sprite (A1p) appears in frames ≥ 17.4 s only; POWERUP string at F8 · `LJ-A5` aura + projectile visible and used |
| A6 obstacles overcome + flag | `DET-A6` · five burst events and five chips logged; flag reached at 26.6 s before the end card · `LJ-A6` counts five clears, sees the flag |
| A7 duration | `DET-A7` · ffprobe duration ∈ [29.5, 30.5] |
| A8 platform spec + safe zones | `DET-A8` · ffprobe 1080×1920, h264 High, yuv420p, 30 fps, aac 48 kHz stereo, mp4, moov first, size < 4 GB; every layout-log box inside (65,288)–(888,1248) · `LJ-A8/CF4` on the final file |
| A9 original IP | `LJ-A9` · Stage 2c table over sprites, plate, sounds · `DET-A9` prompt-guard log (no Nintendo word ever sent) |
| A10 relevance | `HJ-A10` customer · proxy `LJ-A10` checker's one-line reading of what RentOk does, without the deck |
| A11 no unverified claim | `DET-A11` · forbidden-substring scan over every deck string and every layout-log string · `LJ-A11` no visual guarantee cue (no 100 %, no "never") |
| §C production quality | C1–C8 on every text box (bounds, contrast ≥ 4.5:1 or backing, geometry tokens, disjointness); D1 frame text hygiene on 31+ sampled frames (human eye; Cloud Vision not authorised); D12 delivered vs declared; D13 contact sheet; loudness measured |
| §D factual accuracy | `claims_source_map` in copy-deck.json → Stage 2b lines |

## Stage 4 exit criteria — self-assessment (the checker issues the gate verdict)

| Criterion | Self-assessment |
|---|---|
| Riskiest element identified from evidence and tested first | Met — 4.1 rank 1 with RO-04 + GAP; micro-qualification defined; animatic at USD 0 before it |
| Every route has evidence status, `production_use_allowed`, live price, pool | Met — 4.2; only clean/True cells; fallback named with the condition for its use |
| Known failures listed with ids | Met — 4.3 |
| No generated text/logo/UI; voice count | Met — 4.4, 4.5 |
| Pool balance read | Met by human attestation 2026-09-21 (4.8); machine reading impossible (Cloud Billing API disabled) |
| Expected spend vs cap with a repair round; cuts if lower | Met — 4.9 |
| Order of work | Met — 4.10 |
| Tools adapted, fal removed, CAP_USD 0.0, refusals proven | Met — `tools/dispatch.py`, `tools/_common.py` (USD 0 tests above) |

Written by the producer session (lane A). Not a verdict.
