# Stage 5 — Execution and verification

Job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001` · executed 2026-09-20/21 (UTC) after the checker's Gate 1–4 verdict (`3d824e4`), the closed reopened items (`0405feb`) and the freeze (`1c3448b`, recorded as `plan.frozen_at_sha`).
Spend authority: USD 10.00 for this lane, credits only, 0 hidden retries, hard stop (JOB.yaml `spend.cap`). Google credits pool: attested by the human Controller 2026-09-20T18:44Z (machine reading impossible — Cloud Billing API disabled on the project).

Vocabulary: OBSERVED = measured or seen by this session · INFERRED = this session's reading · PROPOSED = not yet judged by anyone else. Every LJ/HJ item below is **for an independent inspector**; this session issues no LJ/HJ verdict.

---

## 1. Deliverable (OBSERVED)

| Item | Value |
|---|---|
| File | `gen/final/rentok-game-lane-a-9x16-30s.mp4` |
| sha256 | `6d418c10163e8af033cb3158173a5960d41a2ba4db061e3bdeb8dff039118168` |
| ffprobe | 1080×1920, h264 High, yuv420p, 30/1 fps, 30.000 s, 33,301,406 bytes; audio aac 48 kHz stereo ≈ 200 kbps; moov first |
| Contact sheet (61 frames at 2 fps + last frame) | `gen/final/CONTACT-SHEET.png` (sha256 `295835b5…`) |
| Key frames (one per storyboard beat + hero) | `gen/final/KEYFRAMES.png` (sha256 `df526312…`) |
| Sampled frames | `qa/final-v3-audio/frames/f*.png` (every 0.5 s) |
| Composition inputs | `board.json`, `copy-deck.json`, `tools/render_game.py` (DesignTokens), `gen/assets/*.png` (cut-outs of att-001…att-007), `gen/raw/A10_music_att-008.wav`, `gen/sfx-stem.wav`, `source/rentok-brand/rentok-new-logo.webp` |
| Producing renders | video `gen/final-v3.mp4` (code), audio mix `gen/audio-mix.wav` (two-pass loudnorm), mux `gen/final-v3-audio.mp4` = the deliverable |

## 2. Paid attempts — every call, all through `tools/dispatch.py` (OBSERVED from `gen/ATTEMPTS.jsonl` / `gen/LEDGER.jsonl`)

| id | asset | route (cell) | USD reserved | status | latency | produced | verdict (producer, pending inspector) |
|---|---|---|---|---|---|---|---|
| att-001 | A1 owner sprite sheet (21:9) | IMG-CORE/nano-banana-2 | 0.067 | ok | 12.8 s | `gen/raw/A1_owner_sheet_att001.png` sha `f1706052…` | **micro-qualification passed on the plan's five criteria** (below); frozen; used |
| att-002 | A2 document wall | nano-banana-2 | 0.067 | ok | 9.2 s | `A2_obst_wall_att-002.png` `1e52476b…` | used (obst_1) |
| att-003 | A3 padlocked sack | nano-banana-2 | 0.067 | ok | 10.6 s | `A3_obst_sack_att-003.png` `7d56cfdc…` | used (obst_2) |
| att-004 | A4 fleeing tenant | nano-banana-2 | 0.067 | ok | 11.1 s | `A4_obst_tenant_att-004.png` `5165b2d6…` | used (obst_3) |
| att-005 | A5 ledger tower | nano-banana-2 | 0.067 | ok | 10.9 s | `A5_obst_tower_att-005.png` `19550e25…` | used (obst_4); calculator display and keys checked blank (zoom) |
| att-006 | A6 ticket swarm | nano-banana-2 | 0.067 | ok | 9.8 s | `A6_obst_swarm_att-006.png` `e9c5ef00…` | used (obst_5); one "!" symbol by design |
| att-007 | A7 background plate (9:16) | nano-banana-2 | 0.067 | ok | 9.6 s | `A7_plate_att-007.png` `04b0615f…` | used (plate); no lettering seen; lane edge measured at y 1602 after fit |
| att-008 | A10 music bed | MUS/lyria+native | 0.060 | ok | 29.3 s | `A10_music_att-008.wav` `8be3e70e…` (32.77 s, pcm 48 kHz stereo) | used, trimmed to 30.0 s |
| **Total** | 8 calls, 8 ok, 0 failed, 0 refused, 0 repairs | | **0.529** | | | | |

Reserved USD 0.529 of the USD 10.00 cap (5.3 %); remaining USD 9.471. Every first draw was accepted by this session; the plan's repair round (USD 0.328) and customer-repair reserve (USD 0.201) are unspent. Dispatch start 2026-09-20T19:03:11Z; last artifact 19:0x (att-008).

Micro-qualification of att-001 against the Stage 4 criteria (OBSERVED by this session; the checker's own look is still owed — `checker_inspected: false` until then): (1) four poses read as one person — same face, spectacles, shirt, keys, sandals; (2) keys on the belt visible in all four poses, the red account book in three (hidden by the body in run-B) at the final 260-px height; (3) no lettering; (4) border keyability 99.96 % (`gen/assets/owner_cutout.json`), four poses found by the sheet splitter; (5) no Nintendo cue (no cap, overalls, moustache, gloves). Fallback (single pose + code bob) not needed.

## 3. Deterministic checks — run by `tools/qa_checks.py final-v3-audio --final` (OBSERVED; JSON at `qa/final-v3-audio/DET-RESULTS.json`)

| Check | Status | Evidence |
|---|---|---|
| DET-A7 duration 29.5–30.5 | PASS | ffprobe duration 30.000 s |
| DET-A8 geometry/codec | PASS | 1080x1920 h264 High yuv420p 30/1 fps |
| DET-A8 container/size | PASS | mov,mp4 33.3 MB (< 4 GB) |
| DET-A8 moov first (faststart) | PASS | first 64 bytes contain moov |
| DET-A8 audio aac 48k stereo | PASS | aac 48000 ch=2 ≈ 201 kbps |
| C1 text bounds in safe box (runtime `check_text_bounds`, container (65,288)–(888,1248)) | PASS | 4,113 text/logo boxes over 900 frames; 0 outside |
| C5 disjoint per frame (runtime `check_disjoint`, all boxes critical) | PASS | 0 overlaps in 900 frames |
| C2 contrast ≥ 4.5 body (runtime `check_contrast`; opaque backing hex, or real pixels for the end card) | PASS | minimum worst ratio 6.08 |
| C6 exact copy byte-check (every logged string == `copy-deck.json` value) | PASS | 0 mismatches |
| DET-A11 forbidden-claim scan (deck + every rendered string) | PASS | 40 distinct strings, 0 hits |
| §D claims sourced (`claims_source_map`) | PASS | five chips mapped to Stage 2b lines |
| DET-A4 install event inside 10–20 s | PASS | 17.4 s |
| DET-A4 cheat strings on F7 | PASS | CHEAT_1 / CHEAT_2 full strings logged 15.8–17.2 s |
| DET-A5 powered state only after 17.4 s | PASS | per-frame flag |
| DET-A3 five obstacle labels rendered on their frames | PASS | first half and clearing run |
| DET-A6 five clears + flag | PASS | clears [1,2,3,4,5], five chips, flag 26.6 s |
| DET-A6 flag before end card | PASS | 26.6 < 27.6 |
| DET-A2 HUD_NAME on every gameplay frame | PASS | 840 gameplay frames |
| Brand end-card strings + wordmark | PASS | CTA_1, CTA_2, URL, WORDMARK logged in F11 |
| 5.5 loudness (ffmpeg ebur128 on the delivered file) | PASS | I = −14.6 LUFS, true peak −2.0 dBTP, LRA 5.1 LU |
| D13 contact sheet + keyframes | PASS | 61 sampled frames at 2 fps |
| D1 frame text hygiene (detector) | NOT_RUN | Cloud Vision not authorised; human-eye pass in §4 |
| DET-A9 prompt guard | PASS | all seven prompts passed `_prompt_guard` (no IP word, no deck string, no-lettering clause) and `canon/gate/run_gate.py pre` (LIMIT-TEXT PASS ×7, 0 non-blocking FAILs; reports `gen/prompts/*.gate.json`) |

Pre-dispatch (A1–A10 of QA-CHECKLIST): A1 gate PASS ×7 · A2 check lines rendered (Stage 3 A3) · A3 no critical string in any prompt (guard) · A4 routes clean/True only · A5 prices live (`dispatch.py quotes`) · A6 cap USD 10 written · A7 pool attested by human (not read) · A8 consent n-a (no supplied person) · A9 micro-qualification done before dependents · A10 TTAO stamps present.

## 4. Human-eye frame text hygiene (D1) — this session's pass, for the inspector to repeat

OBSERVED on all 61 sampled frames (`CONTACT-SHEET.png`) and the 15 key frames: the only lettering is code-set (HUD, labels, panel, chips, flashes, CTA, URL) plus the raster wordmark (HUD chip 150 px, phone screen 56 px, end card 700 px). The generated sprites carry one "?" (document wall) and one "!" (ticket swarm), both requested symbols, no letters or digits; the calculator display and keys are blank (zoomed); the plate has no boards or signs. No stray marks seen. This is not the paid detector and is recorded as a human-eye pass by the author; the independent inspector should repeat it (§6).

## 5. Repairs (all USD 0, all at the compositor / cut-out layer; no generation repeated)

| id | Found by | Class | What changed |
|---|---|---|---|
| R1 | animatic v1 look | compositor | ground line 1130 → 1180 (more play height; still inside the safe box) |
| R2a | C5 disjoint gate on animatic v1 (171 frames) | compositor | checklist chip backing pad 10 → 4, row pitch 48 → 54 — chips no longer overlap each other; column bottom 666 < label zone 710 |
| R2b | C1 bounds gate on animatic v1 (33 frames) | compositor | cheat panel no longer slides out through the bottom of the safe box; it fades in place with its text hidden after 2.6 s |
| R2c | C1 bounds gate on animatic v2 (29 frames) | compositor | chip flight start clamped inside the safe box |
| R3 | final-v1 look (green pockets between the tenant's legs; the model's dark-green ground shadows kept as sprite) | cut-out | key-out by colour as well as connectivity; darkened chroma green treated as background; one-pass green-fringe erosion |
| R4 | final-v2 look (sprites read small at phone size) | compositor | owner 220 → 260 px, obstacles ×1.15; labels/HUD unaffected (gates re-run: PASS) |
| R5 | 5.5 loudness on final-v2 (true peak −0.4 / −0.3 dBTP after AAC) | audio | AAC overshoots square-wave SFX by ≈ 2 dB; pre-encode true-peak target −4 dBTP → delivered −2.0 dBTP at −14.6 LUFS |

Animatic v1 (`gen/animatic-v1.mp4`) and its failing DET run (`qa/animatic-v1/DET-RESULTS.json`) are kept as the attempt of record that produced R2; final-v1/v2 are kept as the attempts that produced R3/R4/R5.

## 6. Items for the independent inspector (LJ) and the customer (HJ) — timecodes

| Item | Look at | What must be true |
|---|---|---|
| A1 platform game (LJ + HJ) | KEYFRAMES F1–F10; contact sheet 0.0–27.5 | side-scrolling level, running/jumping player, obstacles, HUD with health, flag; the game is the film |
| A2 PG owner (LJ + HJ) | F1 (0.90 s), hero 21.40 s; `gen/assets/owner_idle.png` | HUD `PG OWNER`; keys on the belt and the red account book visible at 260 px; spectacles, checked shirt, sandals |
| A3 five obstacles (LJ, per obstacle) | F2 3.20 · F3 6.00 · F4 8.80 · F5 11.40 · F6 13.80 | each picture reads before its label: paper wall + silhouette + "?"; padlocked sack; fleeing tenant with suitcase and coin bag; ledger tower with calculator; angry ticket swarm |
| A4 turning point (LJ + HJ) | 14.2–18.0 s (GAME OVER? → panel → typed code → phone → refill) | the game visibly stops and changes state; the install is the cause |
| A5 enhanced ability (LJ + HJ) | 18.0–19.6 s | cyan aura, a fired tick, phone icon in the HUD |
| A6 clears + flag (LJ + HJ) | 19.6–27.6 s; F9.3 at 22.6 s specifically | five obstacles cleared by projectiles; obstacle 3 is **tagged and keeps running** (never stopped); flag grabbed at 26.6 s, `LEVEL CLEAR!` |
| A8 safe zones (LJ) | any frame; the DET run proves the boxes | no critical text under the Reels/Shorts UI bands |
| A9 IP (LJ) | sprites in `gen/assets/`, plate, the SFX/motifs (`tools/sfx.py`) | Stage 2c do/don't table holds; no Nintendo melody (the power-up and fanfare motifs are five/six-note originals) |
| A10 relevance (HJ) | 19.6–30.0 s | the chips and the end card say what RentOk does |
| A11 no guarantee (LJ) | all strings (DET passed); pictures | no "100 %", no "never", no visual guarantee |
| B creative quality (HJ) | whole film with sound | clearing-run tempo (1.2 s per obstacle), the 0.4-s label flashes, the weight of the empty lane in the lower 40 % (a consequence of the safe box) |
| C production quality (LJ) | contact sheet; audio | no stray lettering; sound level-safe; SFX timed to the events |
| D14 voice continuity | n-a | no narration |

## 7. Limitations and unresolved items (honest)

- The pool balance was attested, not read (Cloud Billing API disabled); every reservation is an upper bound; no billing/quota error occurred.
- `checker_inspected` on the micro-qualification stays `false` until the independent inspector records a look at att-001.
- Frame text hygiene is a human-eye pass (the paid detector is not authorised).
- The lower ≈ 40 % of the frame (below the ground line at y 1180) is a plain lane: it sits under the platforms' UI bands and was kept plain by design; an inspector may judge it visually heavy.
- The wordmark chip at 150 px carries the brand's own tagline at ≈ 6 px, unreadable by design (Stage 3 D-2); if judged as garbled lettering, swap to the code-typed two-colour `RentOk` (USD 0).
- No voice (Stage 3 D-1); sound-on brand recall relies on the typed name and the end card.
- Sarvam / ElevenLabs pools were not touched and not read.

## 8. TTAO stamps (OBSERVED, `date -u`)

`job_start_utc` 2026-09-20T18:11:42Z · `planning_complete_utc` 18:37:56Z · `dispatch_start_utc` 19:03:11Z · `dispatch_end_utc` / `artifact_received_utc` 19:07Z (att-008) · `qa_complete_utc` 2026-09-20T19:16:02Z → elapsed job_start → qa_complete = **1 h 04 m 20 s**. Human review not yet requested (the Controller presents to the customer blind).

Written by the producer session (lane A). Not a verdict.

---

## 9. Repair round 1 (Controller-authorised after the independent Stage-5 checker's DELIVERABLE WITH DEFECTS, `stages/CHECK-STAGE-5.md` @ `e12613f`) — USD 0, no new generation

New deliverable (OBSERVED): `gen/final/rentok-game-lane-a-9x16-30s.mp4` · sha256 `5769ffa7232e6bb1427ce1f0db7396fedd12e9af58dc7feb5d61f140d20b0ab9` · 33,341,051 bytes · 30.021 s (the AAC priming is no longer trimmed by an edit list; inside A7's 29.5–30.5) · 0 `elst` atoms · −14.6 LUFS, −2.0 dBTP. Previous file kept as `gen/final/v1/rentok-game-lane-a-9x16-30s.mp4` @ `6d418c10…`; the intermediate before the D-7 addendum is `gen/final-v4-audio.mp4` @ `bcf125ca…`. Spend unchanged: USD 0.529 (8 calls).

| Defect | Layer | Fix | Check result |
|---|---|---|---|
| D-1 edit lists (mandatory) | assembly (mux) | `-use_editlist 0 -movflags +faststart+negative_cts_offsets` (stream copy); new DET check `DET-A8 no edit lists (elst)` walks the moov/trak/edts box tree (`tools/qa_checks.py count_atoms`) — it reports 2 on the v1 file and 0 on the new one | PASS (0 elst); duration 30.021 s PASS; loudness PASS |
| D-2 flag hidden 27.2–27.6 s (mandatory) | board F10 + compositor | board decision reopened: the checklist fades out 26.6–27.0 s (`board.json` F10 `repair_of: D-2`; `03-CREATIVE.md` Part D); the pole is drawn behind the owner and he takes the idle pose at the pole | C1/C5 gates PASS over 900 frames; frame 27.40 s (`qa/repair-round-1/t27.40.png`): flag at the top, clear facade behind it |
| D-3 projectile | compositor | pixfont `✓` glyph at scale 4 with a dark shadow (`draw_tick`) | frames 18.55 / 20.45 s show the tick |
| D-4 phone not held | compositor | the phone stays composited in the owner's raised hand from 17.6 s through the power-up beat to 19.6 s (idle pose); the test tick fires from the phone; events note corrected | frames 17.80 / 18.55 s |
| D-5 register flicker | cut-out | the run-A book patch composited **behind** the run-B pose (arm stays in front); original kept as `gen/assets/owner_runB_orig.png` | book visible in all run frames (contact sheet 21.0 vs 21.5 s) |
| D-6 generic bursts | compositor | per-obstacle clears as the board says: tile debris with gravity (wall, sack), the ledger tower becomes one neat dashboard card that shrinks toward the checklist, the red tickets recolour to brand green then fade; obstacle 3 unchanged (tagged) | frames 20.45 / 21.65 / 24.05 / 25.25 s |
| D-7 empty lower band (addendum) | compositor (world art; safe box frozen) | slab kerb with yellow dashes, two wheel tracks, drain grate, manhole, parked-scooter silhouette as a 1.3× nearer parallax layer, depth shading toward the bottom — non-critical, may be covered by platform UI | all gates PASS; frame 21.40 s (`qa/repair-round-1/t21.40-d7-lane.png`) |
| D-8 end-card seam | compositor | end-card fill sampled from the logo file's own card colour (#0239FF) | frame 29.90 s: no rectangle |
| D-9 full-frame flashes | compositor | hit flash on the character silhouette only (`flash_sprite`) | frame 03.35 s |
| D-10 records | records | `gen/ATTEMPTS.jsonl` verdicts set to accepted with a dated note (ledger untouched); `plan.micro_qualifications[0]` frozen_asset sha + `checker_inspected: true` citing CHECK-STAGE-5.md §4 | `JOB.yaml` valid YAML |

Not done: nothing in the round was infeasible at USD 0. The D-2 board change is the only reopened creative decision; everything else is execution.

Full DET suite on the new file (`qa/final-v5-audio/DET-RESULTS.json`): **23 checks, 0 FAIL, 1 NOT_RUN** (the paid text detector; the author's human-eye pass was repeated on the new contact sheet and the nine repair frames under `qa/repair-round-1/` — no lettering beyond the code-set strings, the wordmark, `?` and `!`). `ttao.qa_complete_utc` re-stamped 2026-09-20T19:44:03Z (job_start → qa_complete = 1 h 32 m 21 s, including both checker turnarounds).

For the inspector, the frames that changed: 03.35 (sprite flash) · 17.80 / 18.55 (phone in hand, tick) · 20.45 / 21.65 (debris) · 24.05 (dashboard card) · 25.25 (green tickets) · 27.40 (flag clear, checklist gone) · 29.90 (end card) · 21.40 (lower band). Duration is now 30.021 s, not 30.000 s, because no edit list trims the encoder priming — the customer-facing tolerance is 29.5–30.5.
