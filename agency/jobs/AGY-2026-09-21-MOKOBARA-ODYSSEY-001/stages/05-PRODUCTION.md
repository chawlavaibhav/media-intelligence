# Stage 5 — Production (what was made, what it cost, what the code checked, what a human must judge)

Job `AGY-2026-09-21-MOKOBARA-ODYSSEY-001`. Final: `gen/final/mokobara-odyssey-9x16-30s.mp4` (sha256 `75d1fc8b…`, 30.02 s, 1080×1920, H.264 High, 24 fps, AAC 48 kHz stereo, 33.9 MB). Status: **pending_human_review** — only the customer accepts (C-8).

## 1. What happened, in order

| Step | Result | Evidence |
|---|---|---|
| Hero still (protagonist + bag from 2 product photos as references) | strong first draw; a tiny wordmark-like mark copied from the reference onto the strap band → painted out by code | `gen/stills/hero.png`, `hero-clean.png`, `hero-clean.edit.json` |
| Micro-qualification: beat-4 still → beat-4 clip (8 s) | **PASS with note** — identity, bag likeness, no lettering, cinematic look hold; the gag reads through the impossible paddle; arm not visibly to the shoulder, no second arm | `qa/b4/MICRO-QUAL.md`, `qa/b4/contact.jpg` |
| Beat stills 1, 2, 3, 5, 6 (hero still + product photo as references) | all accepted first draw; the photograph is a generated, unnamed woman; no writing anywhere | `gen/stills/b*.png` |
| Beat clips 1, 2, 3, 5, 6 (Veo i2v, native audio) | 2, 3, 6 accepted first draw; **1 FAIL** (the bag lies at his feet before he finds it — story break); **5 FAIL** (one coconut in, zip closed with everything else left) | `qa/b*/contact.jpg` |
| Music bed (Lyria) | first call refused by the provider (HTTP 500 "Could not generate audio… different prompt" — the known Lane A wording pattern), counted USD 0.06; one re-send with neutral wording succeeded | att-014, att-015 |
| Re-takes, one recorded change each | beat 1 take 2: empty shore — PASS on story, shirt drifted to sleeved (flag); beat 5 take 2: fish, rope, flare go in, coconuts + gourd stay out — accepted for the first pass (flag); beat 4 take 2 (the reserve): **both arms in the bag**, then the paddle — used | `gen/RETAKES.md`, `qa/*-take2/contact.jpg` |
| Assembly | trims per the board; hard cuts; 0.6-s crossfade into the code end card; wordmark super 5.0–7.5 s; native ambience −4 dB + Lyria bed from 7.5 s at −9 dB; two-pass loudnorm + limiter; mux with no edit lists + faststart | `tools/assemble.py`, `gen/assemble-report.json` |
| QA by code | 16 DET checks PASS, 1 FLAG (OCR on texture), 1 NOT_RUN (ear) — below | `tools/qa_checks.py`, `qa/final/qa-results.json`, `qa/final/contact.jpg`, `qa/final/keyframe-beat*.jpg`, 60 frames at 2 fps |

Environmental note: the machine's disk hit 169 MB free during QA (not this job — `gen/` is 81 MB); intermediates were deleted and frame samples switched to JPEG. Anything larger (a 16:9 pass, 1080p clips) will need disk freed first.

## 2. Spend — every paid attempt (USD, credits; reserved = counted)

| Attempt | Asset | Route | USD | Status |
|---|---|---|---|---|
| att-001 | hero still | nano-banana-2 | 0.067 | ok |
| att-002 | beat-4 still | nano-banana-2 | 0.067 | ok |
| att-003 | beat-4 clip 8 s (micro-qual) | veo-3.1-fast-i2v | 0.800 | ok (PASS with note) |
| att-004..008 | beat stills 1, 2, 3, 5, 6 | nano-banana-2 | 5 × 0.067 = 0.335 | ok |
| att-009 | beat 1 clip 4 s | veo-3.1-fast-i2v | 0.400 | ok — rejected (story break) |
| att-010 | beat 2 clip 4 s | veo-3.1-fast-i2v | 0.400 | ok — used |
| att-011 | beat 3 clip 6 s | veo-3.1-fast-i2v | 0.600 | ok — used |
| att-012 | beat 5 clip 4 s | veo-3.1-fast-i2v | 0.400 | ok — rejected (items left out) |
| att-013 | beat 6 clip 4 s | veo-3.1-fast-i2v | 0.400 | ok — used |
| att-014 | music bed | lyria | 0.060 | **provider error HTTP 500** (counted) |
| att-015 | music bed (neutral wording) | lyria | 0.060 | ok — used |
| att-016 | beat 1 take 2 (repair) | veo-3.1-fast-i2v | 0.400 | ok — used |
| att-017 | beat 5 take 2, 6 s (repair) | veo-3.1-fast-i2v | 0.600 | ok — used |
| att-018 | beat 4 take 2 (repair, reserve) | veo-3.1-fast-i2v | 0.800 | ok — used (take 1 kept as alternative) |
| **Total** | 18 attempts, 1 failed | | **5.389 of 12.00** | remaining 6.611 |

Ledger `gen/LEDGER.jsonl` (reserve line before every request, settle after); attempts `gen/ATTEMPTS.jsonl` (prompt, params, reference sha256, latency, artifact sha256). Pool reading: human attestation only (SPEND-AUTHORISATION.md).

## 3. DET results (code; `qa/final/qa-results.json`)

PASS: duration 30.021 s · 1080×1920 H.264 High yuv420p 24 fps · MP4 33.9 MB · moov first · 0 edit lists (box walk) · AAC 48 kHz stereo 196 kbps · loudness I = −13.3 LUFS, TP = −4.1 dBTP · copy deck byte-exact (`Transit Backpack · 30L` / `Room for the long way home.` / `mokobara.com`) · wordmark = the site's SVG (sha256 `c443658f…`) · all 6 text/logo boxes inside (65,288)–(888,1248) via `runtime/compositor/gates.check_text_bounds` · claim scan clean · 60 frames at 2 fps + contact sheet · 7 keyframes (one per beat) · every attempt reserved-then-settled · cap not exceeded.
FLAG: frame text hygiene by local `tesseract` — 40 of 56 generated frames return tokens, which on inspection are texture (the tally marks at 0–3.5 s, pebbles, sea); the wordmark super (5.0–7.5 s) is the only intended lettering before the end card. Human eye to confirm.
NOT_RUN: generated speech in the native audio — human ear.

## 4. LJ items for the independent checker (timecodes in the final file)

| # | Judge | Where | What to look for |
|---|---|---|---|
| LJ-1 | Identity continuity | 1.5–3.5 s vs 3.5–28 s | beat 1's man wears a sleeved, buttoned shirt; beats 2–6 the sleeveless torn shirt of the hero still (beat 2 shows a chest tear). Face/hair/beard/bracelet hold throughout. Acceptable for a first pass? |
| LJ-2 | Bag likeness | keyframes 5.5 s, 16.5 s, 22.5 s, 26.2 s vs `source/mokobara/The_Transit_Backpack_30L_Private_Island_1.jpg` | navy matte body, yellow lining, black pulls, straps, proportions; NO lettering on the lower front |
| LJ-3 | The gag | 12.5–20.5 s | one arm to the shoulder ~13–15 s, both arms in ~15–17 s, the paddle 18–20.5 s; deadpan, no mugging. Alternative take at `gen/clips/b4.mp4` (arm + longer paddle reveal) |
| LJ-4 | Packing | 20.5–24.5 s | fish, rope and flare go in; coconuts and the gourd remain on the pebbles at the zip — does it read as "he packed", or as "he left the food"? |
| LJ-5 | IP resemblance | whole film | generic island, no named props, no film's grading/poster look, no volleyball, nobody identifiable; the photo (8–12.5 s) is a generated unnamed woman |
| LJ-6 | Audio by ear | whole file | native ambience 0–28 s (wind, surf, zip, rustle); the bed enters at 7.5 s; **any speech or singing is a defect** (prompts forbade it) |
| LJ-7 | Text hygiene by eye | 0–27.4 s | the OCR-flagged frames; confirm no readable lettering except the super at 5.0–7.5 s |
| LJ-8 | The open | 0–3.5 s | do the scratches read as years (tally marks), and does the pull-back reveal land? |
| LJ-9 | The close | 27.4–30 s | crossfade into the end card; wordmark, product line, tagline, CTA legible on a phone |

## 5. Not realised in this first pass

- Beat 4 does not show the arms to the shoulder as far as the board wanted; take 2 has both arms in, take 1 the better paddle reveal — the customer may prefer either.
- Beat 5 is not "everything goes in".
- Beat 1's costume drift.
- No 16:9 version (Stage 1 decision); no spoken line (Stage 1 decision).
