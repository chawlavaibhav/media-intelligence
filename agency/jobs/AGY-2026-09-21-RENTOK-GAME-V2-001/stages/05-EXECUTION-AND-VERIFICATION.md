# Stage 5 — Execution and verification (gate: DET checks as code on the delivered file; LJ items listed for an independent checker)

Job `AGY-2026-09-21-RENTOK-GAME-V2-001`. Deliverable: **`gen/final/rentok-game-v2-9x16-30s.mp4`** sha256 `0e76b7b1872317728cfbb08dc948e4c678452ef7d84a0eafd6ece0f89013d122` (33,028,692 bytes; 1080×1920, H.264 High 4:2:0 30 fps ≈ 8.6 Mbps, AAC-LC 48 kHz stereo 200 kbps, 30.016 s, moov first, **0 edit lists by box walk**, I = −14.0 LUFS, TP = −2.7 dBTP). Superseded round-1 candidate kept at `gen/final/v1/` (sha256 `1cc8c13d…`). Contact sheet `gen/final/CONTACT-SHEET.png`, keyframes `gen/final/KEYFRAMES.png` (one frame per beat + the hero frame 651), hashes in `gen/final/SHA256SUMS.txt`.

## 5.1 Order of work as executed (all UTC 2026-09-21; ledger `gen/LEDGER.jsonl`, attempts `gen/ATTEMPTS.jsonl`)

| Step | When | USD | Result |
|---|---|---|---|
| Job opened, standard read, source trees read | 11:25:07 | 0 | `ttao.job_start_utc` |
| Stages 1–2 carried over + re-verified; 61 files copied with blob-verified provenance | 11:31–11:35 | 0 | `PROVENANCE.md` |
| BOARD-v2 authored; `render_v2.py` written (C primitives over 30 s, board-driven) | 11:35–11:48 | 0 | `board.json`, `tools/render_v2.py` |
| Animatic v1 (900 frames, 1 m 49 s) → DET: 4 FAIL (animatic edit list; phone-drop over `INSTALL` 2 frames; tower corner + departing swarm under text; framing measured mid-ease / wrong stand-in) | 11:48–11:52 | 0 | fixed: scroll pauses (buried, down), obstacle carry-over, tower pivot at base centre, swarm fade-out, phone out of the panel's bottom edge, focus_t at the camera hold, per-pose framing targets |
| Animatic v2 → DET **26 PASS / 0 FAIL / 3 NOT_RUN** (audio ×2, human eye) | 11:55–11:58 | 0 | `qa/animatic-v2/DET-RESULTS.json`; feel judged beat by beat (Stage 3 Part E) |
| Stage 4 plan; prompt; Canon pre-gate PASS; prompt guard PASS; `planning_complete_utc` | 12:01:11 | 0 | |
| **att-001** V2-S1 pose sheet, nano-banana-2 (Gemini API, credits), 16:9 | 12:01:22 → 12:02:15 (53.6 s) | **0.067** | ok; sha256 `ad4dab13…`; consistency card PASS with one recorded miss (§5.3); frozen |
| SFX stem from the board's 53 audio cues; assembly with the per-beat bed processing | 12:03–12:07 | 0 | `gen/sfx-v2-stem.wav`, `tools/assemble_v2.py` |
| final-v1 render + mix → DET: TP −0.4 dBTP (FAIL) → limiter added → −3.1 / −15.5 → make-up gain → **−14.0 LUFS / −2.7 dBTP**; then 1 FAIL: F4 framing 0.202 < 0.21 | 12:05–12:09 | 0 | `gen/final/v1/` |
| Repair round 1 (own findings, USD 0): R-1 F4 camera ×1.4 → ×1.5 (two renders: 1.45 measured 0.209 by rounding); R-2 limiter + make-up gain (audio) | 12:11–12:15 | 0 | final-v3-audio |
| DET suite on the deliverable: **28 PASS / 0 FAIL / 1 NOT_RUN** (D1 human eye → done by the author on the 61 sampled frames: no stray lettering) | 12:15:45 | 0 | `qa/final-v3-audio/DET-RESULTS.json` |
| Container verified by box walk (0 elst, moov first); `qa_complete_utc` | 12:16:20 | 0 | |

Spend: **USD 0.067 reserved of the USD 3.00 cap** (1 paid call, 0 failed, 0 repairs, 0 hidden retries). Remaining USD 2.933.

## 5.2 DET results on the delivered file (`tools/qa_checks.py final-v3-audio --final`)

| Check | Status | Evidence |
|---|---|---|
| DET-A7 duration 29.5–30.5 | PASS | ffprobe duration 30.016 s |
| DET-A8 geometry/codec | PASS | 1080x1920 h264 High yuv420p 30/1 fps |
| DET-A8 container/size | PASS | mov,mp4,m4a,3gp,3g2,mj2 33.0 MB |
| DET-A8 moov first (faststart) | PASS | first 64 bytes contain moov: True |
| DET-A8 no edit lists (elst) | PASS | 0 elst atom(s) found by walking the moov/trak/edts boxes (D-1; Stage 2 §2.1) |
| DET-A8 audio aac 48k stereo | PASS | aac 48000 ch=2 br=199723 |
| C1 text bounds in safe box | PASS | 4019 boxes over 900 frames; failures 0 [] |
| C5 disjoint per frame | PASS | failures 0 [] |
| C2 contrast ≥ 4.5 (body) | PASS | min worst ratio 6.08; failures 0 [] |
| C6 exact copy byte-check | PASS | 0 mismatches [] |
| DET-A11 forbidden-claim scan | PASS | 40 distinct strings; hits [] |
| §D claims sourced | PASS | ['✓ DIGITAL KYC', '✓ AUTOPAY', '✓ DUES TRACKED LIVE', '✓ ONE DASHBOARD', '✓ COMPLAINT TICKETS'] |
| DET-A4 install event 10–20 s | PASS | install at [17.4] |
| DET-A6 five clears + flag | PASS | clears [1, 2, 3, 4, 5] chips 5 flag [26.6] |
| DET-A3 five obstacle labels rendered | PASS | each OBST_k present on its board frames (first and second half) |
| DET-A4 cheat strings at F7 | PASS | CHEAT_1/CHEAT_2 full strings logged inside F7 |
| DET-A5 powered only after 17.4 | PASS | layout-log powered flag vs 17.4 s |
| DET-A2 HUD_NAME on gameplay frames | PASS | HUD name box on every non-end-card frame |
| DET-A6 flag before end card | PASS | flag 26.6 < 27.6 |
| DET-A3 five hits before the install | PASS | hits at [3.3, 6.1, 8.6, 11.7, 14.1] |
| DET-A4 install at board install_event_t | PASS | install [17.4] vs board 17.4 |
| C5b graphic-vs-text disjoint | PASS | 0 sprite/text overlaps [] |
| FRAMING owner_frac >= target at focus_t | PASS | 0 beats below target [] |
| HERO frame in keyframes | PASS | hero frame 651 (t=21.7) |
| world fills the frame (camera >= 1.0) | PASS | every logged camera scale >= 1.0 — the world is never smaller than the frame |
| brand end card strings | PASS | CTA_1, CTA_2, URL, WORDMARK logged in F11 |
| 5.5 loudness −14 LUFS ±1.5, TP ≤ −1 | PASS | I=-14.0 LUFS, TP=-2.7 dBTP |
| D13 contact sheet + keyframes | PASS | 61 sampled frames at 2 fps under qa/final-v3-audio/frames |
| D1 frame text hygiene | NOT_RUN | human-eye pass over the sampled frames (Cloud Vision not authorised); recorded in 05-EXECUTION |

D1 (human eye, author): all 61 frames at 2 fps + 16 keyframes inspected on `gen/final/CONTACT-SHEET.png` / `KEYFRAMES.png` — the only letters anywhere are the code-set deck strings and the raster wordmark; no generated lettering (the new sheet has none; the reused stills were checked in Lane A). The independent checker should repeat this.

## 5.3 The paid draw, inspected (consistency card `qa/V2-S1-consistency-card.png`, `gen/assets/v2_cutout.json`)

- Keyable 99.95 %; 8 cells (the reach/trip run shared columns and was split by connected components — `merged_cells_split` in the json); standing cell 342 px (the C sheet's 344: same density, ≈ 60 % of the base sheet's).
- Identity vs the Lane A idle and the C brace: same man, spectacles, hair, checked shirt, dark trousers, sandals — PASS (eye).
- Keys 8/8 (gold-pixel count 459–1014 per cell). Red book 5/8 (2234 / 2247 / 1368 / 2423 / 2357 px); absent in cover, cheer, land (247 / 289 / 221 px) — the arms are on the head, up, or out; accepted.
- No lettering; not a Nintendo cue.
- **Recorded miss:** cell 1 "lookback" faces forward with raised eyebrows and an open mouth instead of looking over the shoulder. Used for 0.25 s (8.2–8.45) as "he hears the runner". Decision: no repair draw — a redraw regenerates all eight cells and risks the strong reach / running-fire / cheer / trip cells for a quarter-second pose; cost if wrong: the look-back reads as surprise, not as hearing someone behind — the tenant overtaking supplies that meaning.

## 5.4 Repairs (bounded round 1, USD 0) — classified

| id | Found on | Observed | Class | Repair | Result |
|---|---|---|---|---|---|
| A-1 | animatic v1 | animatic (video-only) carried an edit list | infrastructure (encode) | `-use_editlist 0 +negative_cts_offsets` on the render encode too | 0 elst |
| A-2 | animatic v1 | phone drop overlapped the `INSTALL` backing for 2 frames | compositor | the phone emerges from the panel's bottom edge (screen y 860) | C5 0 |
| A-3 | animatic v1 | toppling tower's far corner rose into the label zone (2 frames); departing swarm passed under the HUD | compositor | pivot at the base centre (max rise 28 px); swarm fades out by 15.45 s (state `leaving`) | C5b 0 |
| A-4 | animatic v1 | framing measured mid-ease; the `cover` stand-in double-shrunk | records / compositor | `focus_t` at the camera hold; per-pose targets with notes; stand-in fixed | FRAMING PASS |
| A-5 | animatic v1 (feel) | fallen tower and hovering swarm slid off him with the scroll | creative_direction (the world must stop when he is down) | scroll pauses 11.7–12.35 and 14.1–18.0; obstacles persist into the next beat until off-screen | judged on animatic v2 |
| R-1 | final-v1 | F4 owner 0.202 < 0.21 (drawn reach pose 6 % shorter than the stand-in) | creative_direction (camera) | F4 camera ×1.4 → ×1.5 (1.45 gave 0.209) | 0.22 PASS |
| R-2 | final-v1 | TP −0.4 dBTP after AAC (denser SFX than Lane A) | audio | `alimiter` −6 dBFS after loudnorm + 1.5 dB make-up | −14.0 LUFS / −2.7 dBTP |

## 5.5 LJ items for the independent checker (timecodes; judge on the delivered file, not the records)

| # | Item | Where |
|---|---|---|
| LJ-1 | The hit lands on all five obstacles: freeze, white silhouette, star, knock-back, dust; the HUD segment blinks | 3.3, 6.1, 8.6, 11.7, 14.1 |
| LJ-2 | Each obstacle has its own motion before contact: wall leans in with sheets fluttering (2.6–3.3), sack hops with dust (4.7–6.1), tenant overtakes from behind with speed lines and coins (7.75–8.6), tower wobbles then topples (10.5–11.7), swarm lunges (13.9–14.1) | those windows |
| LJ-3 | "Half-buried": the tower lies ON him and the world stops (11.7–12.35); he crawls out (12.3–12.6) | 11.7–12.6 |
| LJ-4 | The low point is cold and the swarm hangs over him, still red; GAME OVER? and COMPLAINTS both readable | 14.1–15.0 |
| LJ-5 | The phone drops OUT of the cheat panel into his raised hand; the flash comes from the phone; the world is brighter after than before | 17.2–17.7 |
| LJ-6 | Kneeling owner and the catching hand sit below the panel (Treatment C's limitation 5 closed) | 15.5–17.4 |
| LJ-7 | The tick projectile (42 px) is visible at phone size; the muzzle flash reads | 18.4, 19.9, 21.1, 22.3, 23.5, 24.7 |
| LJ-8 | Five distinct payoffs: paper burst / coin fountain / tag that follows the runner (he is not stopped) / dashboard card / red→green flips with pops; five chips pop onto the checklist | 20.35, 21.55, 22.75, 23.95, 25.15 |
| LJ-9 | Hero frame 651 (21.70 s): powered owner + coin burst inside the shockwave, chip in flight — sells the idea with no copy | 21.70 |
| LJ-10 | Flag: brace, jump, cheer, flag rising to the pole top under LEVEL CLEAR!, confetti, checklist gone by 27.0 | 26.1–27.6 |
| LJ-11 | Pose swaps between the base run poses and the two sheets: any visible pixel-size change at phone width? (C's finding: not visible; INFERRED) | every pose swap, e.g. 3.2→3.3, 14.0→14.1, 17.35 |
| LJ-12 | The "lookback" pose (§5.3): does "surprised, facing forward" read as hearing the runner? | 8.2–8.45 |
| LJ-13 | Camera pushes (×1.5–1.6) on NEAREST resampling: does the enlarged pixel art look intended (chunkier) or degraded? | 3.3–4.4, 6.1–7.1, 8.4–9.6, 11.65–12.6, 14.05–19.7, 26.55–27.6 |
| LJ-14 | Audio: the hits have weight (thump), the bed goes cold after 14.1, near-silence before the flash, "level 2" after it; no clicks at the 17.6 concat | sound-on pass |
| LJ-15 | Safe zones on a phone (CF4) and the world filling the frame at every zoom (no black, no letterbox) | whole film |
| LJ-16 | IP (A9): the star / ring / coins / confetti / "?" / ▮▯ health are plain generic shapes | whole film |

## 5.6 What the renderer still could not do (documented, not weakened)

1. Secondary motion on the body (keys, shirt, hair on impact) — rigid bitmaps; only more drawn frames or a video model.
2. True physical contact — the tower is drawn over him and the swarm over him; overlap + hit-stop + shake stand in for contact.
3. Continuous facial change — discrete drawn states only (18 states now, still discrete).
4. Parallax depth on the camera push — crop-and-scale enlarges plate and sprite alike.
5. Squash-and-stretch — not attempted on the character (the sack gets a 1-frame 6 % squash, the limit before the pixel grid breaks).
6. Pixel density mismatch — both sheets are ≈ 60 % of the base sheet's density (INFERRED not visible at phone size; LJ-11).
7. The run cycle is still two frames (Lane A's runA/runB) — a four-frame cycle would need a sheet.
8. The "lookback" pose is not a look-back (§5.3).

Not a verdict. Written by the producer session.
