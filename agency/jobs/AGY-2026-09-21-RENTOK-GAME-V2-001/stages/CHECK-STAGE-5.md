# CHECK — Stage 5 independent verification (checker session, 2026-09-21)

Job `AGY-2026-09-21-RENTOK-GAME-V2-001` · deliverable `gen/final/rentok-game-v2-9x16-30s.mp4` · sha256 `0e76b7b1872317728cfbb08dc948e4c678452ef7d84a0eafd6ece0f89013d122` (re-hashed by me; matches `JOB.yaml outcome.assets[0]`).

I wrote none of this job. I read the frozen brief, the acceptance contract, the CQ-001 diagnosis §5–§6, Stages 1–5, `JOB.yaml`, the ledgers and the copy deck, then re-measured the file with my own commands and looked at my own frames. Labels: **OBSERVED** = I measured or saw it; **INFERRED** = my reading of what I saw; **CANNOT_DETERMINE** = I had no way to check. USD spent by this check: 0. No producer file was edited.

My evidence folder: `qa/checker/` — `CONTACT-SHEET.png` (my own 61 frames at 2 fps, `frames/f000..f060.png`), `PHONE-360.png` (eight frames at 360 px wide, the size a phone shows), `lj/01..15-*.png` (the fifteen cited frames and strips).

**Verdict first: DELIVERABLE WITH DEFECTS.** Every customer requirement A1–A11 passes; every deterministic measurement the producer reported I reproduced; the on-screen claims are supported by the site snapshot. The defects are production-quality (two occlusions of the hero at his best moments, visible pose "pops", small effects) and one creative gap (the effects and payoffs are modest at phone size). Nothing blocks presenting it; the customer's likely reaction is discussed in §7.

---

## 1. Re-measurement (DET) — all OBSERVED with my own commands

| Item | Producer said | I measured | Result |
|---|---|---|---|
| Duration (A7, 29.5–30.5) | 30.016 s | container 30.016 s; video stream 30.000 s = 900 frames; audio 30.016 s | PASS |
| Geometry / codec (A8) | 1080×1920 H.264 High 30 fps, AAC-LC 48 kHz stereo | `ffprobe`: 1080×1920, h264 High yuv420p, 30/1 fps, 8.60 Mbps; aac LC 48000 Hz 2 ch 200 kbps; 33,028,692 bytes | PASS |
| Edit lists (A8) | 0 by box walk | my own MP4 box walk: top-level `ftyp, moov, free, mdat`; `elst` count **0**; moov before mdat (fast-start) | PASS |
| sha256 vs `JOB.yaml` | 0e76b7b1… / de2887bb… / 54f48b50… | identical for the MP4, `CONTACT-SHEET.png`, `KEYFRAMES.png`; `gen/final/SHA256SUMS.txt` agrees | PASS |
| Loudness / true peak (contract 2.6) | I −14.0 LUFS, TP −2.7 dBTP | `ebur128=peak=true`: I = **−14.0 LUFS**, LRA 4.8 LU, true peak **−2.7 dBFS** | PASS (limit ≤ −1 dBTP) |
| Silence gaps | near-silence 17.3–17.6 by design | `silencedetect −50 dB/0.3 s`: none. `−35 dB/0.2 s`: one, **17.347–17.624 s (0.277 s)** — the designed held breath before the flash. First 0.3 s peak −4.6 dBFS, last second −9.1 dBFS: audio present start to end | PASS |
| Audio shape (a partial stand-in for the ear check, LJ-14) | hits thump; cold after 14.1; brighter after the flash | half-second RMS profile: a peak on every hit (−1.1 to −2.0 dBFS in the mono sum at 3.3 / 6.1 / 8.6 / 11.7 / 14.1 / 17.6 / 20.35 / 21.55 / 22.75 / 23.95 / 25.15 / 26.6); spectral centre of gravity falls to **200 Hz at 14 s** (the darkest second of the film) and rises to 1.4–2.7 kHz after 17.6; whole-frame brightness (Y average) 105 before the flash → 136 after | consistent with the design; hearing it: CANNOT_DETERMINE |
| Ledger | 1 attempt, USD 0.067 of 3.00 | `LEDGER.jsonl` 2 rows / `ATTEMPTS.jsonl` 1 row, same attempt id; reserved sum **0.067 ≤ 3.00**; reserve stamp 12:01:22.360176Z precedes the ok stamp 12:02:15.974972Z and the attempt's own start 12:01:22.360414Z; `settled_usd` null (never settled — consistent with `JOB.yaml total_settled_usd: null`); raw sheet re-hashed `ad4dab13…` = attempt record, 705,990 bytes = ledger note; the prompt contains none of mario / nintendo / luigi / mushroom / rentok / install / guarantee | PASS |
| Safe zone (A8, my own code over the layout log) | C1 4019 boxes, 0 outside | 4019 text/logo backing boxes; **0 outside (65,288)–(888,1248)**; overall extent (67,296)–(888,1229); text-vs-text overlaps 0 | PASS |
| Graphic-vs-text (C5b, my own code) | 0 | 2 raw intersections: 17.37 owner vs the dropping phone (a graphic, by design) and 20.37 the bursting wall vs the chip that pops out of it (one frame; the producer's gate excludes `burst`/`leaving` states, and the reason is sound) | agrees with the producer's 0 |
| Black bands / letterbox (LJ-15) | world fills the frame | all 61 frames: no near-black band on any edge | PASS |
| Log ↔ film | — | the sack's hop (top edge 795 ↔ 923 px), the flag's rise (y 1191 → 857) and the pose list in the log match what I see on the frames at those times (INFERRED: the log is the film's record, not a plan) | consistent |

Note on the producer's Stage 3 table: it says the F2 camera is "back by 4.4"; the log shows the pull-out running 4.4 → 4.9 s (1.6 → 1.0). A records mismatch, not a film defect. Also the flash is **two** white frames (528–529), not one — invisible as a difference.

## 2. Customer requirements A1–A11

| # | Status | Evidence (frame / time) |
|---|---|---|
| A1 platform game, not a promo with game graphics | **PASS** (OBSERVED) | side-scrolling street, HUD name + health segments, LEVEL 1 (0–1.2 s), labelled obstacles, cheat panel, checklist, LEVEL CLEAR!, pole and flag; nothing in 0–27.6 s is a non-game shot. `lj/01`, `lj/07`, `lj/14` |
| A2 recognisable as a PG owner | **PASS** | "PG OWNER" on the HUD every gameplay frame; keys on the belt and a red account book in every non-trip pose; PG-building street. `lj/03` |
| A3 the five problems, each identifiable | **PASS** — see per-obstacle table below | |
| A4 install-RentOK cheat code is the turning point | **PASS** | panel "CHEAT CODE:" 15.5 s, typed "INSTALL RENTOK APP" 15.9–17.2, phone out of the panel 17.2–17.4, flash 17.6; nothing before it helps him, everything after it does. `lj/08` |
| A5 visibly enhanced ability | **PASS** | aura outline, cyan shirt/health, phone in hand, POWER UP! 18.0–19.2, muzzle flash + tick projectile at 18.4 and at each clear. `lj/09`, `lj/10` |
| A6 overcomes the obstacles with it, reaches the flag | **PASS with a caveat** | wall bursts 20.4, sack bursts 21.55, tenant tagged 22.9 (he keeps running away — the Lane A decision that "kills the obstacle" must not become "prevents tenants leaving"), tower → dashboard 24.1, swarm colour-flips and fades 25.2–25.6; flag reached 26.6, at the pole top 27.4. Caveat: obstacle 3 is not visibly stopped and obstacle 5's payoff reads weakly (§5). `lj/11`–`lj/14` |
| A7 duration | **PASS** | §1 |
| A8 platform format + safe zone | **PASS** | §1; at 360 px every string is readable except the tagline inside the wordmark raster (part of the brand mark, not job copy). `PHONE-360.png` |
| A9 no Nintendo reproduction | **PASS** (OBSERVED on picture; music CANNOT_DETERMINE by ear) | owner: spectacles, checked shirt, sandals, no cap/overalls/moustache-signature; power-up is a phone; obstacles are a paper wall, a padlocked sack, a runner with a suitcase, a ledger tower, angry speech bubbles; no ? blocks, pipes, mushrooms, castle; health bar is ▮▯ segments; flag is a plain pole with a blue tick flag. The closest cue is the floating "?" over the document wall (a thought bubble, not a block) and an end-of-level flagpole, which the customer asked for. Music: the bed is a Lyria draw (Lane A att-008), not a Nintendo file; melodic resemblance not checkable here |
| A10 why RentOK matters to a PG owner | HJ — the customer decides | the five problems → the install → five green capability chips → flag; the muted read carries it (INFERRED) |
| A11 no unverified claim | **PASS** | my own scan of all **42 distinct on-screen strings** (27 deck strings + 15 typing partials, every partial a prefix of a deck string) against guarantee / 100 % / never / no more / zero / prevent / recover / eliminate / all-every problem / always / any % / free / best / #1 / instant / Nintendo words: **0 hits**. The only mixed-case brand spelling is the raster wordmark ("RentOk", the site's spelling) |

**A3 per obstacle**

| Obstacle | Frame | Identifiable as | Genuine PG problem? |
|---|---|---|---|
| 1 wall of documents with a grey figure and a "?" | `lj/01` (3.3 s), `lj/10` | TENANT VERIFICATION — an unknown tenant behind a pile of papers | yes (site: "Digital KYC & Verify or Reject Tenant's Documents", home.txt:99) |
| 2 padlocked, chained, angry money sack that hops | `frames/f011` (5.5 s), `lj/11` | COLLECTING RENT — money you cannot get at | yes (autopay.txt:4–5 "Rent Collection. Now Fully Automatic.") |
| 3 tenant sprinting past from behind with a suitcase and a bag of coins | `lj/04`, `lj/05` | LEFT WITHOUT PAYING — he leaves, the owner falls | yes (autopay.txt:104–107 "Rent Not Paid / Tenants Not Paid") |
| 4 tower of ledgers + calculator + loose sheets that topples | `lj/06` | NO RECONCILIATION — the books fall on him | yes (autopay.txt:95 "No more Excel sheets… one dashboard") |
| 5 swarm of angry red speech bubbles | `lj/07` | COMPLAINTS | yes (complaint-management.txt:10 "Tenants raise tickets… Complaints auto-appear") |

Every label is on screen with its obstacle (log: OBST_1 2.2 s…, OBST_5 13.0 s…, and the recall flash on each clear).

## 3. Factual accuracy (D) — each depiction vs its cited site line

Snapshot integrity: `source/rentok-snapshot/SHA256SUMS.txt` verifies (4 HTML files OK). Wordmark raster re-hashed `1ff7dcf5…` = the brand file.

| On screen | Cited line (re-read by me) | Verdict |
|---|---|---|
| ✓ DIGITAL KYC | home.txt:99 "Digital KYC & Verify or Reject Tenant's Documents & Govt. IDs" | SOURCE-SUPPORTED, word for word |
| ✓ AUTOPAY | home.txt:19–20 "Autopay / Collect rent automatically every month"; autopay.txt:4–5 | SOURCE-SUPPORTED |
| ✓ DUES TRACKED LIVE | autopay.txt:104–107 (dashboard counters "Rent Not Paid", "Tenants Not Paid"), :136 "Pending Dues"; home.txt:104 "Real-time update of filled, vacant…" (rooms, not dues) | "dues tracked": SOURCE-SUPPORTED. "live": the cited home.txt:104 is about occupancy; the stronger line is **autopay.txt:216 "Real-time dashboard and notifications"**, present in the snapshot but not cited by the deck. Supported; the citation could be tightened |
| ✓ ONE DASHBOARD | autopay.txt:95 "Everything in one dashboard." | SOURCE-SUPPORTED, word for word |
| ✓ COMPLAINT TICKETS | complaint-management.txt:10 "Tenants raise tickets from their app. Complaints auto-appear on your dashboard." | SOURCE-SUPPORTED |
| "India's renting superapp" (inside the raster) | tenant-verification.txt:154 | the brand's own tagline; SOURCE-SUPPORTED |
| Phone screen and HUD icon show the wordmark | brand file | the product is shown as a phone app, which is what the site sells |

No depiction promises rent recovery, retained tenants or zero problems. The tenant clear (tagged, not stopped) is the film's own way of staying inside A11.

## 4. Production quality (C) — OBSERVED

**Passes:** no stray or garbled lettering on any of my 61 frames or on the five obstacle sprites at zoom (calculator display blank, ledger spines plain, documents blank, no currency sign on the sack); brand mark legible in the HUD chip at 360 px and on the end card; all critical text inside the safe box; audio present and level-safe; the LEVEL CLEAR! label blinks on/off by design (log: on 26.6–26.73, 27.0–27.23, 27.5–27.57); the camera pushes on NEAREST resampling look like deliberately chunkier pixel art, not degradation (LJ-13); the world fills the frame at every zoom (LJ-15).

**Defects and observations (new unless marked "producer-recorded"):**

| id | What I saw | Where | Severity |
|---|---|---|---|
| N1 | **The flag rises through the owner.** The flag is drawn in front of him and passes over his legs, then his torso, for 26.53–27.37 s (26 frames) while he cheers; the pole is drawn behind him, the flag in front. The C5b gate covers graphic-vs-text only, so no gate could catch this | `lj/14` (26.6, 26.9, 27.2) | medium — the triumph beat is the hero half-hidden by a blue rectangle |
| N2 | **The phone hides his face during the wind-up.** 18.20–18.37 s (6 frames) the raised phone sits exactly over his head; the face returns at 18.4 with the fire pose | `lj/09` | medium — 0.2 s, but at "rising confidence" |
| N3 | **Kneel → stand in one frame.** 17.37 kneeling (`cornered_up`, 381 px tall) → 17.40 standing with the phone (`catch`, 444 px): no rise, no intermediate. A pop at the gift moment | `lj/08` | medium |
| N4 | **Dazed pose clipped at the left frame edge** 3.77–4.23 s: the book and left arm are cut by x = 0 (owner box reaches −52 px). Also the document wall is drawn over his right side while he is dazed | `lj/02` (left panel) | low |
| N5 | **Pixel-density and proportion jump at every base-run → sheet-pose swap** (producer-recorded as LJ-11, "INFERRED not visible at phone size"). Native 1080: clearly visible — the run poses are soft, finer-grained and leaner; the sheet poses are crisp, coarser blocks and stockier with a larger head. At 360 px the block-size difference mostly disappears, but the **proportion change still reads** as a small "pop" (3.13→3.20, 13.90→14.00, 17.3→17.4). Some 150 swaps in the film | `lj/03` | low–medium (cumulative) |
| N6 | **Green key fringe** on the new sheet's cut-outs: 194 green-tinted pixels around the trip pose (arm edge, the dizzy puffs), 153 around dazed, 36–52 around brace/lookback/cover; 0–2 on the C-sheet kneeling poses. A 1-px halo at native size; invisible at 360 px | `lj/15` (4× zoom) | low |
| N7 | **Tenant sprite is a different drawing style** (smooth-shaded illustration, soft edges) from the pixel-art owner and other obstacles (reused Lane A asset) | `lj/04` | low |
| N8 | **Cheat panel enters as an empty black box** rising over the owner's head 15.0–15.5 s, covering him for ~3 frames, before any text appears at 15.5 | `frames/f030` (15.0) | low (reads as game UI) |
| N9 | **End card: the wordmark raster's own gradient backing is faintly visible** against the card blue (card (1,55,253); raster box (1,54,250) → (0,40,231), a rounded rectangle 136–817 px wide) | `frames/f058` | very low |
| P1 | "Lookback" pose faces forward, surprised (producer-recorded, V2-D4). At 8.2 s he stands still, eyebrows up, the tenant right behind him. It reads as "startled", and because the runner is visibly behind him the meaning survives; it does not read as hearing/looking back | `lj/05` | low |
| P2 | Rigid bitmaps: no secondary motion, no squash-and-stretch on the character, two-frame run cycle, contact stood in by overlap (producer-recorded §5.6) — see §5 | | — (limitation) |

Occlusion check (flag, tag, phone): flag — N1; phone — N2; the ledger tag over the runner — not occluded, but tiny (§5). The dropping phone never crosses the INSTALL text (repair A-2 holds).

## 5. Creative-quality target (B) — observations scored 1–5

Target (CQ-001 §5–§6, the customer's words): "a modern, polished platform game with expressive characters, rich environments, fluid movement, satisfying interactions and exciting power-up effects". Comparison with the accepted v1 film: **not compared** — I did not open the other worktree, as instructed.

| Dimension | Score | One sentence |
|---|---|---|
| Character expressiveness | **3** | Eighteen drawn states give real faces — shocked at the wall, eyes-shut dazed, sprawled with crooked spectacles, kneeling and looking up, a fierce grin firing, a wide-mouth cheer — but every change is a hard swap between rigid cut-outs, so he expresses in snapshots, not in motion. |
| Motion quality (anticipation, hit-stop, follow-through) | **3** | Anticipation is there on every hit (brace/crouch before each), the hit-stop with white silhouette and star lands on all five, knock-back, dazed and crawl-out give some follow-through; there is no squash-and-stretch, no secondary motion, a two-frame run, and the kneel→stand pop (N3). |
| Environmental richness | **2** | One repeating building plate and an empty street from 0 to 27.6 s; the pushes enlarge the same wall; no parallax, no street life, no props beyond the obstacles; only the cold grade at 14–17.6 s changes the world's mood. |
| Gameplay readability at phone size | **4** | At 360 px the HUD, labels, obstacles, the low point and the cheat code all read; what does not read is the projectile (a ~14-px dot) and the tenant payoff. `PHONE-360.png` |
| Impact / power-up excitement | **2** | The gift and flash (phone out of the panel, held breath, white frame, cyan health refill, aura) are the film's best moment; after it, the muzzle flash is a small sparkle, the tick is a dot with a faint trail, the shockwave ring is thin, and the bursts are speckle — modest at 1080, faint on a phone. |
| Five distinct obstacle motions | **4** | All five are present and different: wall leans in with sheets fluttering (subtle), sack hops with squash (reads), tenant overtakes from behind with speed lines and coins (reads best), tower wobbles then topples onto him (reads), swarm lunges (reads, short). |
| Five distinct payoffs | **3** | Read: paper burst (1), coin fountain (2, a yellow smudge at phone size), dashboard card (4, the clearest). Do not read: the ledger tag on the runner (3 — a 60-px card over a man who simply keeps running away), the swarm flip (5 — red → olive (142,113,35 mean), faces still frowning, then fade; reads as "muddied", not "solved"). `lj/12`, `lj/13` |
| Overall "polished platform game" feel | **3** | It is unmistakably a game and the story spine is clean and paced; it looks like a well-made 16-bit fan game built from cut-outs rather than a modern polished one — the customer's own bar. |

## 6. Failure classification

| Defect | Producer-recorded? | Earliest stage | The one repair (all USD 0 unless stated) |
|---|---|---|---|
| N1 flag through the owner | new | 3 (board: flag draw order / pole position) | draw the flag behind the owner, or place the pole 200 px ahead so the flag rises beside him |
| N2 phone over the face at wind-up | new | 5 (compositor: phone anchor on `windup`) | anchor the phone at shoulder height / draw it behind the head for 18.2–18.4 |
| N3 kneel→stand pop | new | 3 (board: no transition between `cornered_up` and `catch`) | 3–4 frames of rise using `brace` as the mid pose, or ease the y of the catch pose from the kneel height |
| N4 dazed clipped at the edge | new | 5 (camera cx during the F2 push) | shift the push centre +60 px; assert owner box x0 ≥ 0 in the FRAMING gate |
| N5 density/proportion jump at swaps | recorded (LJ-11, as "not visible at phone size" — INFERRED by the producer; I find the proportion pop visible) | 4 (reuse decision R4 accepted 60 % density) | quantise the base run poses to the sheets' pixel grid (nearest, same block size) so all 19 states share one density; the proportion change needs a run pose drawn on the sheet style (USD 0.067) |
| N6 key fringe | new | 5 (`cutout.py` key threshold) | 1-px alpha erosion + despill on the V2 and C cut-outs |
| N7 tenant sprite style | new (accepted in Lane A) | 4 (reuse R2) | leave, or redraw the tenant in the pixel style (USD 0.067) |
| N8 empty panel rise | new | 3 (panel entry) | fade the panel in at its final position, or show "CHEAT CODE:" during the rise |
| N9 raster backing on the end card | new | 5 (compositor) | set the card to the raster's own gradient, or key the raster's backing |
| P1 lookback faces forward | recorded (V2-D4) | 4 (a 0.25-s pose put on a paid sheet with no fallback) | drop the pose: hold `brace` facing the runner for 8.2–8.45 |
| Weak payoffs (tag, swarm) | partly recorded (Stage 3 specifies them; the execution is small) | 3 (payoff scale and the swarm's end state) | tag ≥ 120 px with the chip popping off the runner; swarm to a clean green with the faces changed (a 1-cell "resolved bubble" still, USD 0.067) or a fast fade instead of a hue shift |
| Small projectile / muzzle flash | new | 3 (impact spec: tick 42 px) | tick ≥ 90 px with a thicker trail; muzzle flash ≥ 120 px for 2 frames |
| Records: "back by 4.4" vs 4.9; "one white frame" vs two | new | 3 (table) | correct the table |

## 7. Verdict and plain-English summary

**DELIVERABLE WITH DEFECTS** for presentation to the customer.

What the film is: a 30-second, 9:16 pixel-art platform game. A PG owner (keys on his belt, account book under his arm) runs down a street of PG buildings and is knocked down by five labelled problems — a wall of unverified documents, a padlocked rent sack, a tenant who sprints off with a suitcase, a toppling tower of ledgers, and a swarm of angry complaints — until the health bar is empty and the world goes cold under "GAME OVER?". A cheat panel types INSTALL RENTOK APP, a phone drops out of it into his hand, the screen flashes, he glows and fires ticks from the phone, clears the five problems (each clear adds a green capability chip: Digital KYC, Autopay, Dues tracked live, One dashboard, Complaint tickets), reaches the flag under LEVEL CLEAR!, and the end card says INSTALL RENTOK APP / RENTOK.COM.

What I verified by code: the file is exactly what the job record says (hashes match), it is 30.016 s, 1080×1920, H.264/AAC, fast-start with no edit lists, −14.0 LUFS and −2.7 dBTP, no silence except the designed 0.28-s breath before the flash, every one of 4,019 text boxes inside the safe zone, no forbidden claim among 42 on-screen strings, every capability chip supported by a line of the frozen RentOk site, one paid call of USD 0.067 against a USD 3.00 cap with the reservation written before the call.

What I saw: a coherent, readable game with a real low point and a real turning point; the fall sequence (the sprawled trip, the tower on him, the cold kneel under the complaints) is the strongest stretch. Against that, the hero is half-hidden by the flag as he cheers and by his own phone as he winds up; he stands up from kneeling in a single frame; every pose swap between the old run poses and the new sheets pops in size and grain; and the "power" — the thing the customer explicitly asked to be exciting — is a small dot fired from a phone, with two of the five payoffs (the tenant tag, the swarm flip) that a phone viewer will not read as "problem solved".

The two things most likely to make this customer say "technically correct but below the desired creative standard" again (INFERRED from his CQ-001 words — "good in drama", "better pixelated" — and the target text):
1. **The character still moves like cut-outs, not like a game character.** The eighteen faces are good, but he pops between them; the rise from his knees and the pixel-size jumps at each swap are exactly the "not fluid" the customer will feel without being able to name it. A video-model pass on the two hero beats, or at least drawn transition frames and one pixel grid for all poses, is the repair.
2. **The power-up and the clears are small.** After the flash — which works — the projectile, muzzle flash, shockwave and bursts are modest at 1080 and near-invisible on a phone, and the last two payoffs read as "the tenant leaves anyway" and "the complaints turn brown". The customer asked for "exciting power-up effects"; this delivers correct ones. Scale the effects up and give obstacles 3 and 5 a visible end state before showing it.

Not checked by me: sound by ear (LJ-14) and the melody's originality — both CANNOT_DETERMINE from this session; the waveform and spectrum are consistent with the design. Not compared: the accepted v1 film.

Written by the checker session. Not the customer's verdict.
