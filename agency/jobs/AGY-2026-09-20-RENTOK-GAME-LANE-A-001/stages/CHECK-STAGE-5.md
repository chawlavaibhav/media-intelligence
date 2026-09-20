# Checker verdict — Stage 5 (lane A) — independent verification of the delivered film

Job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001` · branch `work/agency-job-rentok-game-lane-a-001` · checked 2026-09-21 by a fresh session that wrote none of the producer's records.
Method: every number below was re-measured by this session with USD-0 tools (ffprobe, ffmpeg, Python/Pillow) on the delivered file; every picture judgment is from frames this session extracted itself (`qa/checker/`). No paid call was made; no producer file was edited.

**Communication check:** I will explain technical ideas in plain English, including what they mean, why they matter, and their practical consequence; use minimum sufficient wording without sacrificing understandability; separate evidence from inference; and never invent facts. I have read `shared/COMMUNICATION-STANDARD.md`.

Vocabulary: OBSERVED = measured by this session or seen in a frame this session extracted · INFERRED = this session's reading of what it observed · CANNOT_DETERMINE = the evidence available to this session does not settle it. Timecodes are seconds from the start of the film.

Evidence files (this session's own): `qa/checker/contact.png` (60 frames at 2 fps, labelled with timecodes) · `qa/checker/phone-size-360.png` (six frames scaled to 360 px wide, the size of a phone screen) · `qa/checker/cited/*.png` (the 12 individual frames cited below, named by timecode).

---

## VERDICT: DELIVERABLE WITH DEFECTS

Every A-item passes on the customer's requirement. Two defects are worth fixing before the blind presentation, both USD 0 (no new generation): the container carries edit lists that the lane's own spec row says it must not (a one-line re-mux), and the raised flag — the customer's "gets the flag" payoff — is hidden behind on-screen text for the last 0.4 s of the game (a layout change). The full defect list is in §6.

---

## 1. Re-measured, not trusted

### 1.1 The file

| Item | OBSERVED by this session | Producer's record | Agrees? |
|---|---|---|---|
| Path | `gen/final/rentok-game-lane-a-9x16-30s.mp4` | same | yes |
| sha256 | `6d418c10163e8af033cb3158173a5960d41a2ba4db061e3bdeb8dff039118168` | `JOB.yaml outcome.assets[0].sha256` identical | yes |
| Bytes | 33,301,406 | 33,301,406 | yes |
| Container | MP4 (`mov,mp4,m4a,3gp,3g2,mj2`); atom order `ftyp` (0) → `moov` (32) → `free` → `mdat` (32,584) — the index is at the front ("fast start") | "moov first" | yes |
| Video | H.264 High profile, 1080×1920, yuv420p (4:2:0), 30/1 fps constant, 900 frames, 30.000 s, ≈ 8.67 Mbit/s, 2 B-frames | same | yes |
| Audio | AAC-LC, 48 kHz, stereo, ≈ 201 kbit/s, 30.000 s | same | yes |
| Duration | 30.000 s (A7 window 29.5–30.5) | 30.000 | yes |
| **Edit lists** | **present: two `elst` atoms** (video: 1024 ticks at timescale 15360 = 0.067 s, the two-frame B-frame delay; audio: 1024 samples = 0.021 s, the AAC encoder's priming) | not checked by `tools/qa_checks.py`; Stage 2 §2.1 spec row says "no edit lists" (YouTube: "No Edit Lists (or the video might not get processed correctly)"; Meta: "should not contain edit lists") | **no — see defect D-1** |
| Contact sheet / keyframes sha256 | `295835b5…` / `df526312…` | identical | yes |

Plain English on the edit list: an "edit list" is a small instruction inside the MP4 that tells a player "start playing this track a fraction of a second in". ffmpeg writes one automatically when B-frames or AAC audio are used, which is why it is here. Both platforms' pages say not to include one because some processing pipelines mis-handle it. INFERRED: the practical risk is low — this is the default output of the most common encoder in the world — but the lane wrote "no edit lists" into its own spec, its deterministic check did not test for it, and the producer's "DET-A8 container PASS" is therefore incomplete. Not verified by upload (no upload was made).

### 1.2 Audio, measured on the delivered file

- `ebur128`: integrated −14.6 LUFS, true peak −2.0 dBTP, loudness range 5.1 LU — matches the producer's figures and the recorded target (−14 LUFS, ≤ −1 dBTP).
- `astats`: peak −1.96 dBFS, flat factor 0.0, peak count 2 — no clipping (a clipped file would show a flat factor above zero and many samples at the ceiling).
- `silencedetect` at −50 dB / 0.5 s: no silent gap anywhere in the 30 s.
- Momentary loudness sampled every second stays between −27 and −10 LUFS; the quietest second is 26.1 s (the beat before the flag fanfare), the loudest 27.1 s (fanfare + end-card hit). Nothing drops out.
- SFX timing (energy in the code-synthesised SFX stem, 120-ms windows): jump blip at 0.6 s (the renderer jumps at 0.6 s, the board text said 0.9 — picture and sound agree with each other), hits at 3.33 / 6.10 / 11.70 / 14.10 s (−12 to −14 dBFS), key-clicks from 15.9 s, power-up at 17.4 s, pew at 19.9 s, bursts at 20.37 / 21.57 / 23.97 / 25.17 s, tag at 22.77 s, flag fanfare at 26.6 s, end-card hit at 27.6 s. Every board event has a sound at its frame. Obstacle 3 (the fleeing tenant, 7.4–10.2 s) has no hit sound, consistent with "trips, no hit".

### 1.3 Frames

Extracted 60 frames at 2 fps plus the last frame (29.97 s) to `qa/checker/frames/` (deleted after inspection; the 12 cited frames are kept under `qa/checker/cited/`), built `qa/checker/contact.png`. Full-frame white flashes were located by average luma: 3–4 frames (0.10–0.13 s) at each of the four hits and 4 frames at the power-up (17.60–17.70 s) — five brief flashes in 30 s, never more than one per second.

### 1.4 Ledger and attempts (`gen/LEDGER.jsonl`, `gen/ATTEMPTS.jsonl`), reconciled by code

- Paid attempts: **8** (att-001 … att-008): 7 × Nano Banana 2 stills at USD 0.067 + 1 × Lyria music at USD 0.06.
- Reserved USD: **0.529** (sum of the eight reservation lines; the ledger's own running total ends at 0.529). Cumulative ≤ 10.00: **yes** (5.3 % of the cap; USD 9.471 unspent).
- Every attempt has a `reserved` line before its `ok` line — checked by line order and by UTC timestamp for all eight: **true**.
- Failed / refused attempts: **none** (all eight `status: ok`; no `failure_basis`).
- ATTEMPTS ⇄ LEDGER: the same eight ids on both sides; nothing in one file that is absent from the other.
- Record inconsistency (non-blocking): `ATTEMPTS.jsonl` still carries `verdict: pending` on all eight rows and `settled_usd: null`, while `JOB.yaml spend.attempts[].verdict` says `accepted`. The two mirrors disagree on a field that should be identical.
- The micro-qualification row `JOB.yaml plan.micro_qualifications[0]` has `frozen_asset: null` although the sheet's sha256 (`f1706052…`) is recorded on the attempt row and in Stage 5 §2; the "freeze the sheet (sha256 into plan.assets[])" step from Stage 4 §4.1 is not visible as written.

---

## 2. Customer-requirement compliance (A1–A11)

| # | Requirement | Verdict | Evidence (frames this session extracted) |
|---|---|---|---|
| A1 | Reads as an actual platform game, not a promo with game graphics | **PASS** (LJ) | OBSERVED across `contact.png` 0.0–27.5 s: a side-scrolling street with parallax, a running/jumping pixel character on a ground line, obstacles entering from the right, a HUD with a name and a five-segment health bar that empties (5→0 by 14.1 s) and refills in cyan (17.6–18.0 s), a "LEVEL 1" flash at 0–1.2 s, a cheat-code panel that pauses the world, a "POWER UP!" flash, projectiles, a flagpole and "LEVEL CLEAR!". The game runs for 27.6 of 30 s; the only non-game picture is the 2.4-s end card. INFERRED: no frame looks like a conventional ad with a game filter on it. |
| A2 | The player is recognisable as a PG owner | **PASS** (LJ) | OBSERVED `t01.0-open.png`, `t08.5-obst3-tenant.png`: HUD reads `PG OWNER` on every gameplay frame (828 frames in the layout log); the sprite is an adult Indian man, spectacles, blue-white checked shirt, dark trousers, sandals, a bunch of keys on the belt in every pose, a thick red account book under the arm in the idle pose and one of the two run poses. INFERRED: without the HUD label the props say "a man who manages something"; the label is what makes it "PG owner" — that is the design, and it is on screen throughout. |
| A3 | The five named problems are each identifiable | **PASS** (per-obstacle table below) | |
| A4 | An install-RentOK event is the central turning point | **PASS** (LJ) | OBSERVED: health hits 0 at 14.1 s; world desaturates to grey from 14.2 s; `GAME OVER?` flashes 14.2–14.7 s (`t14.5-gameover.png`); a dark panel with a cyan border appears at 15.5 s, `CHEAT CODE:` header, then `INSTALL` / `RENTOK APP` type in letter by letter 15.9–17.2 s; at 17.33 s a small blue phone item falls from the top of the panel, at 17.47 s it is at the owner's head (`t17.47-install-phone.png`), colour returns, a white flash at 17.6 s, health refills in cyan by 18.0 s. The event sits at 17.4 s (58 % of runtime) and the game visibly stops for it. |
| A5 | The character visibly acquires an enhanced ability | **PASS** (LJ) | OBSERVED from 17.47 s: a pulsing cyan outline around the owner on every later gameplay frame; `POWER UP!` 18.0–19.2 s; a phone icon beside the health bar from 18.0 s; a cyan projectile fired at 18.4 s and once per clear afterwards; health never drops again (immunity). Note: the projectile is a plain 26-px cyan square with a dark outline (`t21.40-hero.png`, zoomed at 1:1), not the "cyan tick mark" the board describes — a deviation, not a failure of A5. |
| A6 | Overcomes the obstacles with the new ability and reaches the flag | **PASS with defect D-2** (LJ) | OBSERVED: obstacles 1, 2, 4, 5 re-enter and burst under the projectile at 20.37 / 21.57 / 23.97 / 25.17 s (the "burst" is a 0.3-s scale-up-and-fade of the sprite — OBSERVED in `tools/render_game.py` and in the frames — not the pixel debris the board describes); obstacle 3 re-enters at 22.0 s, keeps running, a cyan tag attaches above its head at 22.77 s and travels with it out of frame (`t22.90-tenant-tagged.png`); five green chips land in the checklist (20.7 / 21.9 / 23.1 / 24.3 / 25.5 s). Flag: a grey pole with a RentOk-blue flag carrying a cyan tick enters at 25.6 s; the owner jumps at 26.2 s, is at the pole at 26.6 s; the flag rises 26.6–27.4 s (visible mid-rise at 26.8 and 27.0 s); `LEVEL CLEAR!` and confetti. **Defect:** from ≈ 27.2 s to the cut at 27.6 s the raised flag sits behind the `COMPLAINT TICKETS` chip row and the `LEVEL CLEAR!` band — only a sliver of blue shows (`t27.50-flag-hidden.png`). The flag is reached and seen rising, so A6 holds; its climax frame is obscured. |
| A7 | 30 s | **PASS** (DET) | 30.000 s by ffprobe (format and both streams). |
| A8 | 9:16, 1080×1920, H.264/AAC MP4, platform limits, critical text in the documented safe zones | **PASS on geometry/codec/duration/safe zones; spec deviation D-1 on edit lists** | DET: 1080×1920, H.264 High, 4:2:0, 30 fps constant, AAC-LC 48 kHz stereo, MP4 with the index first, 33.3 MB. Safe zones: re-checked every text/logo box in `gen/final-v3-audio-layout.jsonl` (900 frames) against (65,288)–(888,1248): **0 outside**. Visual (`contact.png`, all 60 frames): HUD row at y 296–377, labels at y ≈ 720, checklist y 400–666, panel and end-card text all inside the box; nothing critical in the top 14 % or bottom 35 % bands or the right 192-px band. Edit lists: see §1.1 and D-1. |
| A9 | Original Mario-inspired; no Nintendo character, artwork, music or asset | **PASS** (LJ + prompts) | OBSERVED sprite sheet `gen/raw/A1_owner_sheet_att001.png` (sha256 matches the ledger): no cap, no overalls, no moustache, no gloves, no red/blue colour scheme — an ordinary man in a checked shirt. Obstacles (`gen/raw/_obstacles_review.png`): paper wall + grey silhouette + bare `?`; chained money sack; man with suitcase and coin bag; book tower with calculator; red speech bubbles. Plate: a PG building with water tanks and a TV antenna, a lane, two clouds — no hills with eyes, no pipes, no blocks. Flag: plain grey pole, rectangular blue flag, no castle. Ground: packed earth with a stone kerb, no brick bond. HUD words: `PG OWNER`, `LEVEL 1`, `LEVEL CLEAR!` — no "WORLD 1-1", no "1-UP". All seven image prompts contain "Original design, not based on any existing video game character" and no Nintendo name. Music: Lyria generation from the prompt "Upbeat 8-bit chiptune instrumental … 140 bpm … no vocals" (OBSERVED in `ATTEMPTS.jsonl`), not a sampled track. **Closest resemblance found:** the money sack is brown with angry eyebrows — the same mood as a Goomba — but it is a tied sack wrapped in chain with a padlock, not a mushroom shape; INFERRED not a reproduction. Whether the generated melody happens to echo any Nintendo tune: CANNOT_DETERMINE by this session (no listening); its origin as a fresh generation with no reference audio is OBSERVED. |
| A10 | Communicates why RentOK is relevant to a PG owner | **proxy PASS** (HJ — the customer decides) | This session's one-line reading, without the deck: "RentOk is an app that, once installed, handles KYC, autopay rent, tracks dues, puts accounts on one dashboard and turns complaints into tickets — the five things this PG owner was losing to." That reading came from the chips (20.4–27.6 s) and the end card. |
| A11 | No unverified claim (guarantees, prevention, elimination) | **PASS** (DET + LJ) | Full string audit in §2.2: every on-screen string is either a copy-deck string, a typing fragment of one, or the raster wordmark. No `guarantee`, `100%`, `never`, `prevent`, `recover`, `eliminate`, `%` or outcome numeral anywhere. Visually: no "100 %" badge, no coin shower from the tenant, the tenant is tagged, not stopped. |

### 2.1 A3 — per-obstacle

| # | Customer's problem | Frame | How it is identifiable before the label | Genuine PG-management problem? | Verdict |
|---|---|---|---|---|---|
| 1 | tenant verification | `t03.0-obst1-verification.png` (3.0 s) | a leaning stack of blank white papers/folders with a grey faceless silhouette peeking from behind and a large `?` above; label `TENANT VERIFICATION` 2.2–4.6 s; the owner runs into it, white flash, health 5→4 at 3.3 s | yes — "who is this person and is their paperwork real" | PASS |
| 2 | collecting rent | `t06.0-obst2-rent.png` (6.0 s) | a brown money sack tied at the neck, wrapped in chain with a padlock, angry face, hopping; label `COLLECTING RENT` 5.0–7.4 s; hit at 6.1 s, health 4→3 | yes — rent that will not come out | PASS |
| 3 | tenants leaving without paying | `t08.5-obst3-tenant.png` (8.5 s) | a young man in a hoodie sprinting right with a rolling suitcase and a bulging coin bag, exiting frame right while the owner stands with his register; label `LEFT WITHOUT PAYING` 7.8–10.2 s; health 3→2 at 8.6 s | yes | PASS — note the sprite is small (≈ 170 px tall at 1080, ≈ 55 px at phone size) and sits at the right edge, partly under the YouTube right band; it is a moving sprite, not critical text, so this is a readability note, not a safe-zone failure |
| 4 | no place to do reconciliation | `t11.0-obst4-reconciliation.png` (11.0 s) | a toppling tower of bound ledgers with loose sheets flying and a pocket calculator on top (display blank, keys blank at 1:1); label `NO RECONCILIATION` 10.6–12.6 s; crash at 11.7 s, health 2→1 (bar turns yellow) | yes — accounts in a heap | PASS |
| 5 | solving complaints | `t13.5-obst5-complaints.png` (13.5 s) | a cluster of five red speech bubbles with frowning eyes, one carrying `!`, motion lines; label `COMPLAINTS` 13.0–15.0 s; hit at 14.1 s, health 1→0 | yes | PASS |

All five also re-enter in the clearing run (19.6–25.6 s) with a 0.4-s recall of the same label and are cleared to a chip that names a site-supported feature (§3).

### 2.2 A11 — every on-screen string, read from frames and from the layout log

Strings this session could read confidently in the frames: `PG OWNER` · health glyphs `▮▮▮▮▮` … `▯▯▯▯▯` · `LEVEL 1` · `TENANT VERIFICATION` · `COLLECTING RENT` · `LEFT WITHOUT PAYING` · `NO RECONCILIATION` · `COMPLAINTS` · `GAME OVER?` · `CHEAT CODE:` · `INSTALL` · `RENTOK APP` (and the typing fragments `I`, `IN`, `INS`, `INST`, `INSTA`, `INSTAL`, `R`, `RE`, `REN`, `RENT`, `RENTO`, `RENTOK`, `RENTOK A`, `RENTOK AP` — 15.9–17.2 s) · `POWER UP!` · `✓ DIGITAL KYC` · `✓ AUTOPAY` · `✓ DUES TRACKED LIVE` · `✓ ONE DASHBOARD` · `✓ COMPLAINT TICKETS` · `LEVEL CLEAR!` · `RENTOK.COM` · the raster wordmark `RentOk` with the baked-in tagline `India's renting superapp` (legible at 700 px on the end card; at the 150-px HUD chip the tagline is a yellow smear, `RentOk` legible even at phone size — checked at 360 px, magnified).

Against `stages/02-STRUCTURE.md` §2.4: the five chip strings are on the permitted list byte-for-byte; every other string is HUD furniture, a problem label, or the cheat/CTA line — none describes a RentOk capability. Forbidden-substring scan by this session over the layout log's 40 distinct strings: 0 hits (the typing fragment `RENT` is a prefix of `RENTOK`, not "rent recovery"). Strings not readable confidently: none. One string sits outside the permitted list: the tagline `India's renting superapp` inside the brand's own logo file — declared in `copy-deck.json raster_marks`, fetched from the customer-named site, and not a guarantee/outcome claim; INFERRED acceptable, flagged for the Controller's awareness because the permitted list does not contain it.

---

## 3. Factual accuracy (D) — each depicted capability against the site line the producer relied on

Checked by grep in `source/rentok-snapshot/*.txt` (the frozen snapshot; the Gate 1–4 checker already verified the hashes).

| Depiction (what the picture + chip say) | Chip | Site line relied on | Within it? |
|---|---|---|---|
| The paperwork wall bursts → `✓ DIGITAL KYC` | CHIP_1 | home.txt:99 "Digital KYC & Verify or Reject Tenant's Documents & Govt. IDs" | yes — a paperwork problem answered by digital KYC; no turnaround time, no "no bad tenants" |
| The locked rent sack bursts → `✓ AUTOPAY` | CHIP_2 | home.txt:19–20 "Autopay / Collect rent automatically every month"; autopay.txt:4–5 | yes — the feature name only; the picture does not show money arriving or a "100 %" |
| The fleeing tenant is tagged and keeps running → `✓ DUES TRACKED LIVE` | CHIP_3 | autopay.txt:104–107 "Rent Not Paid … Tenants Not Paid", :136 "Pending Dues"; home.txt:104 real-time filled/vacant/under-notice | yes — OBSERVED at 22.77–23.2 s the tenant is never stopped or turned back; a marker attaches and travels with him. This is tracking, which is what the site offers, and it is the frame the Gate 3 checker reopened (3-A) — closed correctly |
| The ledger tower bursts → `✓ ONE DASHBOARD` | CHIP_4 | autopay.txt:95 "No more Excel sheets … Everything in one dashboard." | yes — the board promised the tower "is blasted into one neat stack/screen"; OBSERVED it scales up and fades like the others (no neat stack is drawn; the renderer has one burst routine for obstacles 1, 2, 4, 5). The chip still holds; the picture is weaker than the board's version (see D-6) |
| The red ticket swarm bursts → `✓ COMPLAINT TICKETS` | CHIP_5 | complaint-management.txt:10 "Tenants raise tickets from their app. Complaints auto-appear on your dashboard. Track, assign, and resolve" | yes — the board said "ticks turn each red bubble green"; OBSERVED the swarm scales up and fades like the others (no red-to-green recolour in the renderer or the frames at 25.0–25.6 s). Chip holds |
| End card `INSTALL / RENTOK APP / RENTOK.COM` | CTA | the site's own CTA is "Get the app" (home.txt:140); the URL is the customer-named source | a call to action, not a claim |
| Tagline `India's renting superapp` (raster) | — | the brand's own logo asset (Stage 2d, sha256 `1ff7dcf5…`) | the brand's self-description, not authored by this job |

No depiction exceeds its source. Nothing implies rent is guaranteed, tenants are prevented from leaving, or all problems vanish; the `GAME OVER?` question mark and the tenant's continued exit are the two places the film could have over-promised and did not.

---

## 4. Production quality (C)

- **Generated lettering:** none. OBSERVED at 1:1 on the sprite sheet, five obstacle sprites and the plate: the only symbols are the requested `?` and `!`; the calculator display and keys are blank; the building faces carry no boards or writing. The sheet cut-out is clean (border keyability 99.96 % in `owner_cutout.json`; no green fringe visible at 1080 in the cited frames).
- **Brand mark:** the raster wordmark is legible at the HUD chip (150 px) and the end card (700 px); at phone size the chip's `RentOk` still resolves, the tagline does not (a yellow line, not garbled letters). On the end card the logo file's own rounded blue card is a slightly lighter blue than the #0038FF background, so a faint rectangle is visible around the wordmark (`t29.97-endcard.png`) — a small seam, not an error.
- **Safe zone:** all text inside the documented box (0 of 4,113 boxes outside, re-checked). The end card is centred on the safe box, not the canvas, so the whole stack sits ≈ 50 px left of the frame's centre — visible as a slight left bias; by design (Stage 3 NOTE 6).
- **Animation/timing:** scroll, jumps, knock-backs, bursts and chip flights land on the board's timecodes (events file agrees with the SFX stem and the frames). Hit flashes are full-frame semi-transparent white for 0.1 s each (the board said a flash on the character); five in 30 s, never more than one per second. The pole is drawn in front of the owner, so at 26.6–27.6 s he runs on the spot behind it (F10 keeps the run pose after arrival) — cosmetic.
- **Audio:** present, level-safe (−14.6 LUFS, −2.0 dBTP), no clipping, no gaps, every event has its cue. Melody originality by ear: CANNOT_DETERMINE (see A9).
- **Character continuity:** one bitmap per pose for all 30 s; the powered state is the same sprite with a cyan outline, so the face, shirt, keys and sandals are identical before and after. One flicker: the red register is present in idle and run-A and absent in run-B, so during every run it appears and disappears at the run cycle rate (8 pose changes per second). Visible on `contact.png` (compare 21.0 vs 21.5 s). Cosmetic; the customer may read it as a glitch.
- **The lower 40 % of the frame** (below the ground line at y 1180) is a flat ochre lane with a few dots — OBSERVED on every gameplay frame, and heavy at phone size (`phone-size-360.png`). The producer recorded it (Stage 5 §7). It is the price of keeping every critical element inside the platform safe box; the band is not empty by accident, but it is empty.
- **Micro-qualification of the character sheet (att-001) — this session's look, which is the one that counts:** OBSERVED on `gen/raw/A1_owner_sheet_att001.png` (sha256 verified against the ledger) — (1) four poses, one person: same face, spectacles, hair, shirt pattern, trousers, sandals in all four; (2) keys on the belt in all four poses; the red account book in idle, run-A and jump, hidden in run-B — visible at the 260-px in-film height (`t01.0-open.png`, `t08.5-obst3-tenant.png`); (3) no lettering anywhere on the sheet; (4) flat #00FF00 background, keyable (the cut-outs carry no green); (5) no Nintendo cue. **Verdict: PASS on all five plan criteria.** `checker_inspected` may now be set true, with the run-B book absence recorded as the one known limitation of the sheet.

---

## 5. Creative quality (B) — observations, not a verdict

- **Does it read as a platform game?** Yes — a scrolling street, a runner, a health bar that drains, a pause-and-cheat panel, projectiles, a flag. INFERRED, as the Gate 3 checker warned: the first half is an auto-runner in which the owner loses to every obstacle on cue (three jumps in 30 s); the "game" is more scripted than played, but the furniture is all there and coherent.
- **Readable at phone size?** (`phone-size-360.png`, six frames at 360 px wide) The HUD, obstacle labels, cheat code, `POWER UP!`, `LEVEL CLEAR!` and the end card read clearly. The chips are small (green 42-px caps → ≈ 14 px at 360 wide) but legible; the fleeing tenant, the phone item (a blue rectangle ≈ 20 px tall at phone size, on screen ≈ 0.3 s) and the cyan projectile (a dot) are at the edge of legibility. The five obstacle sprites read well.
- **Install → power-up → clearing, without sound:** intelligible. The chain is: health empties → grey world + `GAME OVER?` → panel types `INSTALL RENTOK APP` → colour and health return, `POWER UP!`, cyan glow → each old obstacle re-enters and bursts, a green feature name lands → flag → `INSTALL RENTOK APP` again. The weakest link is the phone item: it falls for ≈ 0.3 s and vanishes in the flash, so "app installed" is carried by the typed words and the HUD phone icon rather than by the owner holding a phone (the events file says "phone in hand"; OBSERVED he never holds it — he keeps the red register). The clearing run at 1.2 s per obstacle is fast but each obstacle is a shape already seen, so it tracks.
- **Does the commercial message land?** The chips say what the app does in five feature names, and the same install line opens and closes the second half. Whether a PG owner is moved by it is the customer's call.

---

## 6. Failure classification — every defect, its earliest stage and its one repair

Stage key: 1 intent · 2 structure · 3 creative · 4 selection · 5 execution. "Recorded" = the producer already wrote it down; "found" = new in this check.

| id | Defect | Found/recorded | Earliest stage | One repair at that layer | USD |
|---|---|---|---|---|---|
| **D-1** | MP4 carries two edit lists; the lane's spec row (Stage 2 §2.1) and both platforms say none | found | 5 (assembly) | re-mux without re-encoding: `ffmpeg -i final -c copy -movflags +faststart+negative_cts_offsets -use_editlist 0 out.mp4`, then re-walk the atoms to confirm no `elst`, re-run ffprobe + ebur128, update the sha256 in `JOB.yaml`. Add an `elst` check to `tools/qa_checks.py` so DET-A8 tests what the spec says | 0 |
| **D-2** | Raised flag hidden behind the checklist and `LEVEL CLEAR!` for the last ≈ 0.4 s of the game (27.2–27.6 s) | found | 3 (board: F10 says the checklist "stays visible (it is the proof)" and the flag "rises to the top", but both occupy y 540–666; Gate 3's 3-B fix moved only the flash) | one line on the board: fade the checklist out at 26.6 s (its proof is done; the end card follows), and keep the flag's top at y 540 — the flag then rises into clear facade. Re-render, re-run the gates | 0 |
| D-3 | Projectile is a plain cyan square; the board specifies a cyan tick mark ("gun sort of" reads as "shooting dots") | found | 5 | draw the projectile with the pixfont `✓` glyph (the flag already uses it) at the same 26 px | 0 |
| D-4 | The phone item vanishes in the power-up flash; the owner never holds it (events note says "phone in hand") | found | 5 | keep the phone item composited at the owner's hand for 0.6 s after the flash (or in the powered idle pose), and correct the events note | 0 |
| D-5 | Red register flickers on/off between run poses (present in run-A, absent in run-B) | recorded as "hidden by the body in run-B" (Stage 5 §2); the flicker consequence not recorded | 4/5 (the sheet's run-B pose; accepted at micro-qualification) | code-paste the book from run-A onto run-B at the cut-out stage (same pixels, offset to the arm), no new draw | 0 |
| D-6 | All four bursts are the same scale-up-and-fade; the board promised pixel debris, "one neat stack/screen" for the ledger tower and "red bubbles turn green" for the tickets | found | 5 | either implement the debris and the two special clears in the renderer or amend the board so record and film agree | 0 |
| D-7 | Lower 40 % of every gameplay frame is an empty ochre band | recorded (Stage 5 §7) | 2/3 (a consequence of composing only inside the safe box) | fill the band with non-critical world art (a nearer parallax layer: kerb, drain, a parked scooter, shadows) — allowed to be covered by platform UI, not allowed to be blank | 0 |
| D-8 | End-card wordmark shows the logo file's own slightly-lighter blue card as a faint rectangle on #0038FF | found | 5 | sample the raster's card colour for the end-card fill, or use the code-typed two-colour `RentOk` the producer already prepared | 0 |
| D-9 | Full-frame white hit flashes (the board said a flash on the character) | found | 5 | cosmetic; if changed, flash the sprite only | 0 |
| D-10 | Records: `ATTEMPTS.jsonl verdict: pending` vs `JOB.yaml verdict: accepted`; `frozen_asset: null` on the micro-qualification row; `checker_inspected: false` (now answered above) | found | 5 (records) | one pass over the two files; set `checker_inspected: true` citing this file | 0 |

None of these is a customer-requirement failure. D-1 and D-2 are the two that should be fixed before presentation; D-3, D-4 and D-5 are the ones a viewer is most likely to notice; the rest are record hygiene or taste.

---

## 7. Release-readiness for the blind customer evaluation

**DELIVERABLE WITH DEFECTS.** All eleven A-items pass on the customer's words (A10 pending the customer, as the contract says). The file is 30.000 s, 1080×1920, H.264/AAC, index-first, level-safe, every string inside the safe box, every claim inside its site line, nothing Nintendo. Defects to clear first, both USD 0 and both a few minutes: D-1 (re-mux to remove the edit lists so the file matches the lane's own spec) and D-2 (let the flag be seen at the top of the pole). If the Controller chooses to present as-is, the customer will see a film that meets the brief with a slightly buried flag moment.

---

## For the human Controller (plain English)

This is a 30-second vertical film that is itself a small, original, code-rendered side-scrolling game: a pixel-art PG owner (spectacles, checked shirt, keys on his belt, a red rent register) runs down an Indian PG lane into five obstacles named exactly as the customer named them — a wall of unverified paperwork, a padlocked rent sack, a tenant fleeing with a suitcase and a coin bag, a toppling tower of ledgers, a swarm of angry complaint tickets — losing one heart to each until "GAME OVER?". A cheat-code panel types "INSTALL RENTOK APP"; colour and health return, he glows cyan, and he re-runs the level shooting each obstacle away while a checklist stamps a real product feature per clear (Digital KYC, Autopay, Dues tracked live, One dashboard, Complaint tickets); the fleeing tenant is tagged and tracked, never stopped, which is exactly the honesty line the customer drew. He reaches a blue flag, "LEVEL CLEAR!", and the film ends on the RentOk wordmark and the same install line. With code I confirmed the file's identity (sha256 matches the job record), its geometry, codecs, duration and index position, that every one of 4,113 text placements sits inside the documented phone-safe box, that all 40 on-screen strings are permitted and contain no guarantee language, that the sound is at broadcast level with no clipping or gaps and every effect lands on its event, and that the money trail is clean: eight paid calls, USD 0.529 of a USD 10 cap, every reservation logged before its result, no failures, no hidden retries. With my own eyes on my own extracted frames I confirmed the five obstacles are recognisable before their labels, the character is one consistent person for 30 s, nothing on screen resembles a Nintendo asset, and the install moment visibly changes the game's state. Two things I found that the producer did not: the MP4 contains "edit lists" (a standard encoder artefact that the lane's own spec and both platforms say to avoid — a one-line re-mux fixes it), and the raised flag is hidden behind the feature checklist and the "LEVEL CLEAR!" band for the last 0.4 seconds of the game, so the customer's "gets the flag" moment is half-buried. The two things most likely to make a real customer reject it: (1) the "gun sort of power" reads as a small cyan dot and the app itself is a blue rectangle on screen for a third of a second — the transformation is told by words more than shown by picture, and the customer asked for it to be shown; (2) the bottom 40 % of every frame is an empty brown band and the sprites are small in the middle of a tall phone screen, which at Reels size can feel like a game viewed from too far away.

---

## USD-0 commands this session ran (all read-only except writes into `qa/checker/` and this file)

- `shasum -a 256` on the final MP4, contact sheet, keyframes, and the raw sprite sheet; compared with `JOB.yaml` and the ledger.
- `ffprobe` (streams, format, time bases, B-frames); a Python atom walk of the MP4 (`ftyp/moov/free/mdat` offsets; `elst` count and contents; `mdhd` timescales).
- `ffmpeg -vf fps=2` frame extraction; `-sseof` last frame; single-frame extraction at 17.20–17.87, 19.90–27.50 s; Pillow contact sheet and 360-px phone-size strip; 1:1 zooms of the projectile and the HUD chip.
- `ffmpeg -af ebur128=peak=true`, `astats`, `silencedetect`; per-second momentary loudness; `signalstats` YAVG per frame to locate white flashes; windowed RMS over `gen/sfx-stem.wav` at the board's event times.
- Python over `gen/final-v3-audio-layout.jsonl` (all strings, first/last times, safe-box containment) and over `gen/LEDGER.jsonl` / `gen/ATTEMPTS.jsonl` (ordering, sums, reconciliation).
- `grep` over `tools/render_game.py`, `tools/sfx.py`, `tools/assemble.py`, `gen/prompts/*`, `JOB.yaml`, `copy-deck.json`, `qa/final-v3-audio/DET-RESULTS.json`.
