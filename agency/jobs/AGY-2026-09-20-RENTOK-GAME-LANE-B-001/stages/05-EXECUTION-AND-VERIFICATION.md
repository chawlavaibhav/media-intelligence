# Stage 5 — Execution and verification · AGY-2026-09-20-RENTOK-GAME-LANE-B-001 (lane B)

Author: lane-B producer session. Machine clock (`date -u`): 2026-09-20, dispatch 18:56:13Z → QA complete 19:18:28Z.
Authority: Controller message (Stage 5 authorised; cap USD 10.00 credits-only, 0 hidden retries, hard stop). Frozen package: `b585f11` (`plan.frozen_at_sha`).
Vocabulary: OBSERVED = measured/seen by this session; INFERRED = my reading; the LJ/HJ verdicts below are NOT issued here — they are listed for the independent inspector.

## Deliverable (OBSERVED)

| | |
|---|---|
| file | `gen/final/rentok-game-lane-b-9x16-30s.mp4` |
| sha256 | `d9d437d3a83411d6b1e0776f83edd974d6e807bb55953184c72f09f5a6b89df1` (`gen/final/SHA256SUMS.txt`) |
| ffprobe | 1080×1920, h264 High, yuv420p, 30/1 fps, 30.000 s, AAC-LC 48 kHz stereo 256 kbps, 3.79 Mbps overall, 14.2 MB, moov before mdat |
| companions | `gen/final/CONTACT-SHEET.png` (66 sampled frames, safe box drawn in yellow) · `gen/final/KEYFRAMES.png` (one frame per beat F1–F17, labelled with beat + timecode) · `qa/frames/*.png` (every sampled frame) |
| render determinism | two consecutive full renders produced the identical sha256 (OBSERVED) |

## Paid attempts — every call, failures included (`gen/ATTEMPTS.jsonl`, `gen/LEDGER.jsonl`)

| id | asset | route (cell) | pool | USD reserved | status | verdict | produced |
|---|---|---|---|---|---|---|---|
| att-001 | A8 V1 | sarvam-bulbul-v3 (AUD-TTS clean 6/6) | sarvam_credits | 0.000849 | ok | **accepted (final voice)** | `gen/voice/A_sarvam_V1.wav` 2.645 s |
| att-002 | A8 V2 | sarvam-bulbul-v3 | sarvam_credits | 0.000503 | ok | accepted | `A_sarvam_V2.wav` 2.219 s |
| att-003 | A8 V3 | sarvam-bulbul-v3 | sarvam_credits | 0.000880 | ok | accepted | `A_sarvam_V3.wav` 2.731 s |
| att-004 | A8b V1 | elevenlabs-v3-direct (AUD-TTS clean 4/6) | elevenlabs_credits | 0.0027 | ok | not_selected | `B_eleven_V1.mp3` 2.72 s |
| att-005 | A8b V2 | elevenlabs-v3-direct | elevenlabs_credits | 0.0016 | ok | not_selected | `B_eleven_V2.mp3` 2.00 s |
| att-006 | A8b V3 | elevenlabs-v3-direct | elevenlabs_credits | 0.0028 | **failed** http_401 `quota_exceeded` — the API key has a per-key quota of 1,000 credits with 11 left (the account shows 946/10,000 used): candidate B could not produce the longest line | failed | — |
| att-007…011 | QA transcripts A/B | gemini-3.1-flash-lite (job-local pin, `source/pins/`) | credits | 5 × 0.00245 (settled ≈ 0.00005 each) | ok | QA evidence | `qa/transcript_*.txt` |
| att-012 | A8c V1 | gemini-tts (job-local pin) | credits | 0.009607 (settled 0.002077) | ok | not_selected | `C_gemini_V1.wav` 3.16 s |
| att-013 | A8c V2 | gemini-tts | credits | 0.009604 | **failed** provider_refusal `PROHIBITED_CONTENT` on "RentOk mode: on." | failed | — |
| att-014 | A8c V3 | gemini-tts | credits | 0.009607 (settled 0.002117) | ok | not_selected (audition candidate on the longest line) | `C_gemini_V3.wav` 3.24 s |
| att-015 | QA transcript C V1 | gemini-3.1-flash-lite | credits | 0.00245 | ok | QA evidence | |
| att-016 | QA transcript C V2 | gemini-3.1-flash-lite | credits | 0.00245 | **failed** local_fault — my tool reserved before checking the input file existed (att-013 had been refused); nothing was sent; the reservation stays counted; tool fixed (`transcribe()` now checks the file first) | failed | — |
| att-017 | QA transcript C V3 | gemini-3.1-flash-lite | credits | 0.00245 | ok | QA evidence | |
| **att-018** | **A1 character sheet (micro-qualification)** | nano-banana-2 (IMG-CORE clean 7/8) | credits | 0.067 | ok | **PASS on the six-point card → FROZEN** sha256 `9bb97e3a…c270` | `gen/stills/A1_character_sheet_v1.png` |
| att-019…023 | A2 O1–O5 obstacle pairs | nano-banana-2 | credits | 5 × 0.067 | ok | accepted (producer; inspector re-checks) | `gen/stills/A2_O{1..5}_v1.png` |
| att-024 | A3 world plate | nano-banana-2 | credits | 0.067 | ok | accepted; no lettering seen | `gen/stills/A3_world_plate_v1.png` |
| att-025 | A6 music | lyria (MUS clean 4/4) | credits | 0.060 | ok | used (by-ear check reserved for the inspector) | `gen/audio/A6_lyria_v1.wav` 32.77 s |

**Total reserved USD 0.58675 of the USD 10.00 cap (5.9 %); 25 attempts, 3 failed (1 quota, 1 provider refusal, 1 local fault), 0 hidden retries, 0 repairs needing a paid call.** Pools: Google credits 0.5744 (stills 0.469 + music 0.06 + TTS/transcripts 0.045), Sarvam ≈ 0.0022, ElevenLabs 0.0071 (plan credits). Settled figures exist only where the provider returned usage (Gemini); every other line is an upper bound (Controller note: Google balances are not machine-readable).

Pool readings at dispatch: Google credits `attested_by_human` (Controller, 18:44Z) · ElevenLabs `GET /v1/user/subscription` at 18:55:57Z: tier free, 946 of 10,000 characters used (OBSERVED) — but the API key carries its own 1,000-credit quota, discovered by att-006 · Sarvam: attested (no endpoint known; UNKNOWN balance).

## Order of work as executed (matches Stage 4 §4.10)

1. Cap + pool readings recorded → 2. voice audition (A, B, C; transcripts) → 3. **A1 sheet micro-qualification → PASS → frozen** (card: `qa/A1-microqual-card.md`) → 4. obstacles → 5. world plate → 6. Lyria → 7. code (keying → sprites → render → SFX → mix → mux) → 8. QA bundle → repairs R1–R4 (below) → 9. this record.

## Voice audition (3.10) — result

Rule: ≥ 2 candidates on the longest line (V3 "Level complete. Get the app.") at final pace, before dependent assets; one voice source. Completed: **A (Sarvam bulbul:v3 `aditya`) all three lines; C (Gemini TTS `Puck`) V1 and V3 (V2 refused); B (ElevenLabs `Daniel`) V1 and V2 only (V3 quota failure).** Transcripts (Gemini 3.1 Flash-Lite, QA only): A: "cheat code install rent okay" / "Rent OK mode on." / "Level complete. Get the app." · B: same for V1/V2 · C: "Cheat code install rent okay." / "Level complete. Get the app." — every take is verbatim on transcript ("rent okay" is the transcriber's spelling of the spoken brand name). Measured durations: A 2.645 / 2.219 / 2.731 s; C 3.16 / 3.24 s; B 2.72 / 2.00 s.
**Chosen: A (Sarvam)** — the only candidate that completed all three lines; on the longest line it is 0.5 s shorter than C, which matters for the F16–F17 slot. The by-ear comparison A vs C on V3 (`gen/voice/A_sarvam_V3.wav` vs `C_gemini_V3.wav`) is reserved for the inspector (this session cannot listen); if the inspector prefers C, V2 would still have to come from A (C refused it) — which would break the single-source rule, so A stays unless the inspector rejects it outright.

## Timeline derived from the measured VO (4.6)

The frozen board's F8 (1.8 s) and F9 (1.6 s) were shorter than V1 (2.645 s) and V2 (2.219 s). Per the frozen rule (Stage 4 §4.5/4.6: the slot grows, adjacent holds shrink by code, no label hold below 1.2 s): F8 = 2.8 s, F9 = 2.4 s; F2–F6 = 1.84 s each (labels visible 1.54 s), F10–F14 = 1.6 s each (cards visible 1.2 s: 0.9 s in their beat + 0.3 s into the next); F1 1.2, F7 1.4, F15 1.6, F16 1.2, F17 2.2 → **30.0 s** (`gen/render/TIMELINE.json`). VO starts: V1 11.9 s, V2 14.7 s, V3 26.7 s (ends 29.431 s).

## DET checks — outputs (`qa/QA-RUN-final.txt`, `qa/QA-REPORT.json`; every check is real code in `tools/qa_checks.py`, `tools/text_render.py`, `tools/mix_audio.py`)

```
container: PASS dur=30.000s 1080x1920 h264 High yuv420p 30/1 aac 48000 2 bitrate 3786746   (+ moov_before_mdat True, size < 4 GB)
safezone: PASS 4974 placements; 0 failures        (every critical text box inside x 65–1015, y 269–1248 on every frame; right-edge rule)
disjoint: PASS 900 frames; 0 failures             (runtime check_disjoint over every frame's critical regions, min gap 12 px)
copy byte-exact: PASS 20 strings; worst contrast 6.927   (every rendered plate's lines == copy deck; runtime check_contrast ≥ 3.0 display / 4.5 body on the opaque backing; check_geometry PASS on the one token source)
claims/forbidden: PASS [] []                       (forbidden list over deck + VO lines + 7 transcripts: no hit; every product-state string is in spec.permitted_claims)
prompts: PASS []                                   (no Nintendo word, no deck string in any of the 3 generation prompts; guard_prompt also refused at dispatch)
vo schedule: PASS  V1 11.9–14.545, V2 14.7–16.919, V3 26.7–29.431; film end 29.8; min gap 0.1   (check_vo_schedule, measured durations)
loudness: PASS I=-14.4 LUFS TP=-2.2 dBTP LRA=4.4  (ffmpeg ebur128 on the final file; target I −14 ±1, TP ≤ −1 — our own target)
frames: 66 sampled (0.0, every 0.5 s, ±0.2 s around the three cuts, 29.9) → CONTACT-SHEET.png; KEYFRAMES.png (17)
```

Mapping to the acceptance contract: A7 → container PASS · A8 DET half → container + safezone PASS · A3 DET half → copy PASS (C04–C08 byte-exact on F2–F6) · A4 DET half → copy PASS (C10 on F8, 11.8–14.6 s) · A11 DET half → claims PASS · A9 DET half → prompts PASS · 5.4 → vo schedule PASS · 5.5 → loudness PASS · 5.1/5.2 → copy + contrast/bounds/disjoint PASS. Text-hygiene detector (Cloud Vision): **NOT_RUN** (not authorised) — the human-eye pass below is the release check.

## Repairs (bounded; all at the compositor/audio layer; no paid call)

| id | failed check | class | repair | result |
|---|---|---|---|---|
| R1 | safezone: `TICKETS RESOLVED` at cap 72 Bold was 1031 px wide (x 24–1055); `Get the app` plate bottom 1249 > 1248; disjoint: label plate 10 px from the name tag; score plate 3 px into `LEVEL 1` | compositor | cards set in Condensed Bold (all five, one look); CTA centre 1180 → 1165; labels 700 → 688; score 378 → 396 | safezone PASS; disjoint 834 → 83 failures |
| R2 | loudness: TP +0.6 dBTP after loudnorm (dynamic mode; +4.8 dB gain needed) | audio | true-peak limiter after loudnorm | TP +0.3 (AAC overshoot) |
| R2b | loudness: AAC encoding overshot the WAV's −1.6 dBTP by 1.9 dB | audio | limiter to −3.6 dBTP on the WAV; AAC 256 kbps | **I −14.4, TP −2.2 PASS** |
| R3 | disjoint: the name tag rode up with the jump into the label plate (F2, F5) | compositor | tag fixed at the ground position | 83 → 63 (then 20 distinct) |
| R4 | disjoint: two-line cheat bar bottom 812 vs tag top 804 | compositor | cheat bar centre 700 → 665 | 1 artefact left |
| R5 | disjoint: a duplicate layout record of the same HUD box at 27.767 s (QA-tool artefact from a redundant render call) | infrastructure (tool) | removed the redundant call; QA dedupes identical records | **0 failures** |
| Recorded deviations from the deck's declared sizes (not repairs to strings): C18 96 → 76 cap Condensed; C19 84 → 64 cap Condensed; C13–C17 Bold → Condensed Bold — the 950-px safe width binds; strings unchanged. |

## For the independent inspector — LJ items, with where to look (this session issues no verdict here)

| item | look at | what must be true |
|---|---|---|
| A1 platform game | KEYFRAMES F1–F16; play 0–27.8 s | side-scroll level, player, obstacles, HUD (hearts / LEVEL 1 / score / RENTOK MODE slot), flag; game frame runs 27.8 of 30 s (OBSERVED from the timeline) |
| A2 PG owner | F1 (0.0–1.2 s), `qa/frames/t000.50.png` at phone scale | keys at the belt, red register under the arm, ochre checked shirt, glasses on the head, HUD tag `PG OWNER` |
| A3 five obstacles | F2 2.12 s · F3 3.96 s · F4 5.80 s · F5 7.64 s · F6 9.48 s | blank-ID creature / red calendar / sheet ghost with suitcase / paper tangle / three winged handsets, each with its label |
| A4 cheat code = turning point | F7 11.10 s (`CONTINUE?`) → F8 13.20 s → F9 15.80 s | freeze, typed code, phone + `INSTALLING...` → `RENTOK MODE: ON`, hearts refill, world turns blue |
| A5 enhanced ability | F9 15.8–17.0 s; F10 17.8 s | phone raised, cyan shield glow, cyan OK beam |
| A6 all overcome + flag | F10–F14 (17.8, 19.4, 21.0, 22.6, 24.2 s) · F15 25.8 s · F16 27.2 s | five beam hits → five product-state cards; flag grabbed and slid; `LEVEL COMPLETE` |
| A8 safe zones (visual) | CONTACT-SHEET.png (yellow box) | no critical text outside the box; nothing important in the bottom 35 % |
| A9 original | A1–A3 stills; every frame; **by ear**: `gen/audio/A6_lyria_v1.wav` and `gen/audio/sfx/*.wav` | no plumber cues, no ?-blocks/pipes/mushrooms; no Nintendo melody or coin/jump/1-up/power-up jingle; the F15 fireworks are a generic trope |
| A10 relevance | muted viewing | one-sentence statement after a sound-off pass |
| A11 implied claims | F10 17.8 s (`TENANT: VERIFIED` after one hit) · F12 21.0 s (ghost tagged, drifts on) · F14 24.2 s (`TICKETS RESOLVED`) | nothing states or implies guaranteed recovery, prevented leaving, or elimination of all problems; the cards show the site's own status values |
| D1 frame text hygiene | `qa/frames/*.png` (66) | no lettering other than the code-set strings; note the O4 tangle's scribble marks (`A2_O4`) — lines, not letters (producer reading; inspector decides) |
| D3 identity | KEYFRAMES | one man throughout (single sheet) |
| D10/D14 voice | `A_sarvam_V1/V2/V3.wav` on the assembly at 11.9 / 14.7 / 26.7 s | verbatim (transcripts PASS), one source, arcade-announcer register, no hole; compare V3 with `C_gemini_V3.wav` |
| D11 mix | 10.4–17.0 s (drop-out and return), 26.7–29.4 s | music ducks under the announcer; SFX on every contact; nothing clips (TP −2.2) |
| C production quality | whole film | run cycle relies on bob/tilt (the four run cells differ little — recorded on the A1 card); keying fringe on the keys; wordmark panel edge on the end card |

HJ (customer, blind): A1, A2, A4, A5, A6, A10 — via the Controller.

## Unresolved limitations (honest list)

1. The by-ear checks (voice register, music/SFX originality, mix balance) are not done by this session; they are the inspector's.
2. The run cycle: the model's four run poses differ only slightly, so running reads through the code bob/tilt and the scroll — a producer-observed weakness, not re-drawn (the gated items passed; a re-draw would be USD 0.067 if the inspector asks).
3. The "after" world keeps the warm facade colours with a blue sky/road; a fuller recolour was not attempted (the plate's wall colours are part of its identity; changing them risks a muddy look) — judgement call, recorded.
4. ElevenLabs' per-key quota (1,000 credits) is smaller than the account's plan (10,000); the balance read did not reveal it. Recorded as a pool-reading limitation.
5. Gemini TTS refused "RentOk mode: on." as PROHIBITED_CONTENT (n = 1, no reason given) — a directional observation only.
6. Sarvam balance UNKNOWN (no endpoint known); Google balances not machine-readable (Controller); every ledger line is an upper bound; vendor statements not reconciled.
7. The O4 tangle sprite carries scribble-like lines on the papers (asked for blank paper); they are not legible letters at 1024 px or on screen (producer reading) — the inspector decides whether that counts as stray lettering.

TTAO so far (mechanical): job_start 18:12:53Z → qa_complete 19:18:28Z = **1 h 05 m 35 s**; human decision pending.
