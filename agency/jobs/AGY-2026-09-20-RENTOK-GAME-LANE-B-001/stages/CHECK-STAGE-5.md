# Independent Stage-5 check · AGY-2026-09-20-RENTOK-GAME-LANE-B-001 (lane B)

Checker: a fresh session that wrote none of this lane's files. Machine clock (`date -u`): 2026-09-20 ~19:30Z. Worked only inside this worktree; no paid call; no producer file edited. My own measurements and frames live in `qa/checker/` (contact sheet `contact.png` at 2 fps with the Meta safe box drawn in yellow; the 12 frames I cite as `frames/fNNN.png` where NNN × 0.5 s = the timecode; two evidence crops).

Vocabulary: **OBSERVED** = I measured it with a command or saw it in a frame I extracted myself; **INFERRED** = my reading of what I observed. Where I could not check something (I cannot listen to audio), I say so instead of guessing.

---

## 1. Re-measured, not trusted

### The delivered file (OBSERVED, `ffprobe` + `shasum` run by me)

| what | measured | producer's record | match |
|---|---|---|---|
| sha256 | `d9d437d3a83411d6b1e0776f83edd974d6e807bb55953184c72f09f5a6b89df1` | `JOB.yaml outcome.assets[0].sha256` identical; `gen/final/SHA256SUMS.txt` identical | yes |
| size | 14,200,299 bytes | 14,200,299 | yes |
| container | `mov,mp4` brand `isom` / `isomiso2avc1mp41`; `moov` atom at byte 40, before `mdat` (fast-start) | "moov before mdat" | yes |
| video | H.264 High, yuv420p, 1080×1920, 30/1 fps, 900 frames, 30.000 s, 3.51 Mbps | same | yes |
| audio | AAC-LC, 48 kHz, stereo, 264 kbps, 30.000 s | "AAC-LC 48 kHz stereo 256 kbps" | yes (264 vs 256 is the encoder's actual vs. requested rate) |
| duration (A7) | 30.000 s | 30.000 s | **A7 PASS** (tolerance 29.5–30.5) |
| loudness (`ebur128`, my run) | I = −14.4 LUFS, LRA 4.4 LU, true peak −2.2 dBTP | I −14.4 / TP −2.2 | yes |
| clipping (`astats`) | peak −2.2 dBFS, flat factor 0.0 (no flattened/clipped runs) | — | no clipping |
| silence (`silencedetect`, −40 dB, ≥ 0.3 s) | none found in 0–30 s | — | no dead audio |

Plain meaning: the file the producer describes is the file on disk, byte for byte; it is a normal 30-second vertical MP4 that phones and the three platforms play; its sound level sits where social platforms expect it and never distorts.

### Ledger and attempts (OBSERVED, `gen/LEDGER.jsonl` 50 lines, `gen/ATTEMPTS.jsonl` 25 lines, parsed by my own script)

- **25 attempts** in `ATTEMPTS.jsonl`; **25 distinct attempt ids** in the ledger; the two id sets are identical — nothing in one file is missing from the other.
- **Every attempt has exactly one `reserved` line and exactly one settle line, and the reservation comes first** (checked by line position for all 25).
- **Reserved USD sums to 0.58675** in both files; the ledger's running `cumulative_reserved_usd` re-adds correctly at every line; `cap_usd` is 10.00 on every line; **cumulative ≤ 10.00 throughout** (5.9 % of the cap).
- Failed / refused / local-fault attempts (3): `att-006` ElevenLabs V3 — HTTP 401 `quota_exceeded` (the API key's own 1,000-credit quota had 11 left); `att-013` Gemini TTS V2 "RentOk mode: on." — provider refusal `PROHIBITED_CONTENT`; `att-016` transcript of the refused C-V2 — `local_fault`, reserved then stopped locally because the input file did not exist (USD 0 billed; reservation kept, as the rules require). All three carry their reservation and remain counted. No hidden retry: no attempt id appears twice and no route is re-sent with the same request.
- **Every artefact hash in `ATTEMPTS.jsonl` re-hashes to the file on disk** (22 files checked: 3 Sarvam WAVs, 2 ElevenLabs MP3s, 2 Gemini WAVs, 7 transcripts, 7 stills, 1 Lyria WAV) — the recorded outputs are the outputs.
- The 25 calls split as: 3 Sarvam TTS (att-001..003), 3 ElevenLabs TTS (att-004..006, one failed), 3 Gemini TTS (att-012..014, one refused), 7 Gemini transcription checks (att-007..011, 015..017, one local fault), 7 Nano Banana 2 stills (att-018..024), 1 Lyria music (att-025). Each is on the ledger with its own line pair.
- **Selected voice is one source — verified by code, not by trust.** I converted the three Sarvam takes and the final film's audio to 16 kHz mono and ran a spectral (log-spectrum) correlation search ±0.6 s around the producer's claimed start times. Best matches: `A_sarvam_V1.wav` at **11.90 s** (correlation 0.85), `A_sarvam_V2.wav` at **14.70 s** (0.70), `A_sarvam_V3.wav` at **26.70 s** (0.69). The Gemini candidate `C_gemini_V3.wav` scores only 0.36 at its best offset, i.e. it is not in the mix. Same test for the music bed: the film's 2–8 s stretch matches `gen/audio/A6_lyria_v1.wav` at a 2.0 s offset (0.75) — the bed is the Lyria draw. `tools/mix_audio.py` line 64–67 loads `A_sarvam_*.wav` only (OBSERVED in code).
- One record discrepancy (INFERRED as a bookkeeping slip, not a spend issue): every successful line in `ATTEMPTS.jsonl` still says `"verdict": "pending"`, while `JOB.yaml spend.attempts[]` says `accepted` / `not_selected` / `qa_evidence` for the same ids. The two files disagree on the verdict field only.
- The producer's DET checks are real code (OBSERVED: `tools/qa_checks.py` defines `c_container`, `c_safezone_disjoint`, `c_copy_claims`, `c_prompts`, `c_frames`, `c_loudness`, `c_vo`; `text_render.py`, `keying.py`, `render_film.py`, `sfx_synth.py`, `mix_audio.py` exist; the planned `pixelate.py` does not exist as a file — the retro look is instead produced inside `render_film.py` by composing the world at 360×640 and scaling ×3 nearest-neighbour, line 4 and 355). The gate-1–4 checker's NOTE 11 asked for exactly this verification: done.

---

## 2. Customer-requirement compliance (A1–A11)

Frames cited are mine (`qa/checker/frames/`, 2 fps; "fNNN" = NNN × 0.5 s) plus the producer's `gen/final/KEYFRAMES.png` where noted.

| # | Verdict | What I relied on |
|---|---|---|
| **A1** "a Mario game … not a promotional video with gaming graphics placed over it" (LJ; customer decides HJ) | **PASS (LJ)** | f000–f019: a side-scrolling street, a running player sprite, one obstacle at a time entering from the right, a HUD (three hearts that empty one by one — 3 at f000, 2 at f007, 1 at f019 — `LEVEL 1`, a six-digit score that counts up 000128 → 010000, a `RENTOK MODE` slot), a `CONTINUE?` freeze at f022, a typed cheat code at f024–f028, a flag on a pole at f052–f054 and `LEVEL COMPLETE`. The game frame runs 0.0–27.8 s; the end card is 2.2 s. Observations that go to the customer's judgement, not to this verdict: there are no ledges or gaps — the player only runs and jumps into obstacles, so it reads as an endless-runner level rather than a platformer with platforms; and the lower 33 % of every game frame (rows 1256–1896 of 1920, measured as uniform-colour rows) is a flat drawn road with a dashed line, with the game confined to the middle band — see §5. |
| **A2** "the player is basically a PG owner" | **PASS** | f000, f004: a man in an ochre checked half-sleeve shirt, dark trousers, chappals, glasses pushed up, a red cloth register under the arm, a ring of keys at the belt, and a floating tag `PG OWNER` over his head from 0.0 s. INFERRED: at phone size the keys read as a small dark/purple blob (see §4), so the tag and the register do the identifying; the tag alone would already satisfy the customer's sentence. |
| **A3** the five named problems each identifiable | **PASS** (per-obstacle lines below) | f004, f007 (via contact sheet), f011 (contact), f016, f019 |
| **A4** cheat code = install RentOK, central turning point | **PASS** | f022 `CONTINUE?` freeze with one heart left at 10.5–11.8 s; f024–f028 `CHEAT CODE: INSTALL RENTOK` typed letter by letter (f024 shows `CHEAT CODE:`, f025 `INSTAL_`, f026–f028 the full string), 11.8–14.6 s; f030 `INSTALLING...` with a phone; f033 `RENTOK MODE: ON`, hearts refilled to three, sky turned brand blue, HUD slot lit. The install sits at 11.8–16.0 s of a 30 s film — the middle. The VO speaks the same words (`transcript_A_sarvam_V1/V2`). |
| **A5** "gun sort of power/immunity" — a visibly enhanced ability | **PASS** | f033 (16.5 s): phone held up, a cyan glow ring round the character (the immunity); f035 (17.5 s): a cyan beam from the phone hitting the obstacle (the "gun"). The customer's brief allowed the system to design the power-up; it is a phone-beam, not a firearm (the lane's decision D6). Observation for §5: the beam is a thin line and its `OK` tip is tiny. |
| **A6** overcomes all obstacles and gets the flag | **PASS** | Five hits, five transformations, in the same order as the problems: f035 ID-card gets a face and a tick (`TENANT: VERIFIED`), f038–f039 calendar turns blue with a tick (`AUTOPAY: ON`), f042 ghost pinned with a tag (`DUES VISIBLE`), f045 paper ball becomes a stacked report (`REPORTS: DONE`), f049 handsets become three ticked tickets (`TICKETS RESOLVED`); f052 jump to the flag pole with fireworks; f053–f054 flag lowered, `LEVEL COMPLETE`, score jumps to 010000. INFERRED: the customer wrote "kills all the obstacles"; the lane deliberately converts rather than destroys them (documented at Stage 2/3 to avoid a recovery claim). The customer may or may not accept "converted" as "killed" — a taste item for the blind evaluation, not a compliance miss, because each obstacle visibly stops being a threat and the flag is reached. |
| **A7** 30 s | **PASS (DET)** | 30.000 s by my ffprobe. |
| **A8** Reels/Shorts fit; critical text inside the documented safe zone | **PASS (DET + LJ)** | Container/geometry above. Safe zone: on my contact sheet the yellow box (x 65–1015, y 269–1248 — the Meta guidance the lane documented at Stage 2 §2.2) contains every HUD element, every label, every card, the cheat bar, the name tag, the `LEVEL COMPLETE` banner and the end card on all 60 frames; measured on f058 the end-card text/button pixels span y 608–1237 and x 154–924 (inside). The bottom 35 % carries only the drawn road — nothing a platform overlay could hide. |
| **A9** original, no Nintendo asset in picture or sound | **PASS (picture) · CANNOT_DETERMINE by ear (sound); provenance verified by code** | Picture: I looked at all seven generated stills and all 60 frames. Character: no cap, no moustache, no overalls, no gloves, no letter initial. World: Indian low-rise facades, water tanks, a dish, a scooter, a tree; no ?-blocks, bricks, pipes, mushrooms, turtles, castle, or striped flag ball. Obstacles are an ID card, a flip calendar, a sheet ghost with a suitcase, a paper ball, three winged handsets — none resembles a Nintendo enemy. The flag is a plain pole with a rectangular blue RentOk flag. The pixel fireworks at f052–f054 are a generic end-of-level trope, as the gate-1–4 checker already said. Sound: I cannot listen. What code establishes: the bed is the Lyria draw generated for this job (spectral match above); the effects are synthesised by `tools/sfx_synth.py` (twelve WAVs in `gen/audio/sfx/`); nothing in the mix comes from any external recording. Whether the Lyria draw accidentally quotes a known melody needs a human ear — I record that as not checked by me. |
| **A10** why RentOK is relevant to a PG owner | **HJ — observation only** | Muted read (frames only): a PG owner is beaten by five labelled PG problems; installing RentOk turns each into a product status the site lists; the closing line is `PG OWNER? LEVEL UP.` + `Get the app`. The relevance is carried by the five problem labels and five status cards — all readable without sound. |
| **A11** no unverified claim | **PASS (DET + LJ)** | See the string scan below. |

### A3 per-obstacle

| obstacle | frame / time | how it is identifiable | maps to a genuine PG problem? |
|---|---|---|---|
| O1 tenant verification | f004 (2.0 s) | a walking white ID card with a blank grey head-silhouette photo; label `UNVERIFIED TENANT` on a dark plate above it | yes — an unverified tenant is the customer's first named problem; the card-with-no-face is a direct picture of it |
| O2 collecting rent | f007 (3.5 s, contact sheet) | a red flip-calendar creature (two rings on top) with angry brows and fists; label `RENT NOT PAID` | yes — the calendar says "due date"; the label says the problem. INFERRED: without the label the red block is only loosely a calendar |
| O3 tenants leaving without paying | f011 (5.5 s, contact) | a sheet ghost carrying a suitcase and a rolled mattress, i.e. a tenant who has "vanished" with his belongings; label `LEFT WITHOUT PAYING` | yes — the customer's third problem verbatim in spirit |
| O4 no place to do reconciliation | f016 (8.0 s) | a rolling ball of receipts, ledger strips and bank slips with angry eyes; label `ACCOUNTS MESS` | yes — "accounts mess" is a fair plain-English label for "no place to do reconciliation"; the customer's own phrase is not used, which the customer may notice |
| O5 solving complaints | f019 (9.5 s) | three red old-style telephone handsets with wings and angry eyes swarming; label `COMPLAINT CALLS` | yes — the site itself says complaints arrive "on calls, WhatsApp" (cm L15, cited by the producer) |

All five are on screen for ~1.84 s each with the label visible ~1.54 s (`gen/render/TIMELINE.json`, F2–F6).

### A11 — every on-screen string I could read, against `stages/02-STRUCTURE.md` permitted claims and the forbidden list

Read confidently on frames: `PG OWNER` · `LEVEL 1` · `RENTOK MODE: OFF` · score digits (`000128` … `010000`) · `UNVERIFIED TENANT` · `RENT NOT PAID` · `LEFT WITHOUT PAYING` · `ACCOUNTS MESS` · `COMPLAINT CALLS` · `CONTINUE?` · `CHEAT CODE:` / `INSTAL_` / `CHEAT CODE: INSTALL RENTOK` · `INSTALLING...` · `RENTOK MODE: ON` (banner and HUD) · `TENANT: VERIFIED` · `AUTOPAY: ON` · `DUES VISIBLE` · `REPORTS: DONE` · `TICKETS RESOLVED` · `LEVEL COMPLETE` · `PG OWNER? LEVEL UP.` · `RentOk` + `India's renting superapp` (wordmark, end card and on the flag) · `Get the app`.
VO (the 7 transcripts under `qa/`, and the deck lines): "cheat code install rent okay" / "Rent OK mode on." / "Level complete. Get the app." — the transcriber spells the brand as it is pronounced.

- My own scan of all of the above against the Stage 2 forbidden list (guarantee, never, always, 100 %, zero/no/all/every problem(s), no more, can't/won't leave, prevent, recover(y), insur-, claim, instant(ly) verif-, safe/trusted tenants, any %, "faster", rupee amounts, Eqaro, Mario/Nintendo names, tool/model names): **zero hits** (OBSERVED). "superapp" contains "super" — it is the customer's own wordmark tagline, not the Nintendo word; not a hit.
- Product-state strings used: `TENANT: VERIFIED` (PC1d), `AUTOPAY: ON` (PC2a), `DUES VISIBLE` (PC3a), `REPORTS: DONE` (PC4a), `TICKETS RESOLVED` (PC5a+PC5c), `Get the app` (PC6a), `India's renting superapp` (PC6b), `INSTALL RENTOK` (PC7). All are rows of the permitted table. No other product statement appears.
- Implied-claim frames (the producer flagged 17.8 / 21.0 / 24.2 s; I looked at f035 17.5 s, f042 21.0 s, f049 24.5 s):
  - **`TENANT: VERIFIED` after one beam hit (f035).** The string is the site's own status value (tv L70 "Verified", re-read by me in the frozen snapshot). The instantaneous change is game-time compression, not a statement about speed; no word on screen or in voice says "instant". The lane's own Stage 2 table lists "instant verification" as unsupported — this is an in-lane caution, not one of the three things the customer forbade. I judge it does not state or imply a guarantee. Note it for the Controller as the frame most likely to be misread.
  - **`DUES VISIBLE` (f042).** The ghost keeps drifting away (it is still on screen, faded, moving up-right) — the film deliberately shows "you can see what he owes", not "you get it back". Correct. One small ambiguity: the price tag pinned to the ghost carries a **green tick**, which a viewer could read as "paid/settled". The text says otherwise; I record it as a minor implied-claim risk rather than a failure.
  - **`TICKETS RESOLVED` (f049).** Site: "Complaints Resolved" (cm L24), "marks the ticket as resolved" (cm L76), "Resolved status shown in Tenant App" (cm L83) — all re-read by me. The card shows the site's status; it does not say the app resolves complaints by itself, and no voice line says so. Within the permitted row.
- Strings I could **not** read confidently: the small `OK` glyph at the tip of the beam (f035, ~20 px tall, cyan on cyan) and the tagline on the in-game flag (f052–f054, the wordmark scaled to ~120 px wide). Neither is a claim; both are decorative.

**A11: PASS.** No forbidden word; every product string is a permitted row; the three flagged frames stay inside "the app shows this status".

---

## 3. Factual accuracy (D)

I re-verified the snapshot first: `shasum -c source/rentok-snapshot/SHA256SUMS.txt` → all four HTML files OK (OBSERVED). Then I re-read every cited line in the `.txt` extracts.

| depicted capability | producer's citation | what the line actually says (re-read) | stays within it? |
|---|---|---|---|
| `TENANT: VERIFIED` — an unverified tenant becomes a verified one | tenant-verification.txt L59–60, L66–70 | "Tenant Verification Status / Real-time verification tracking for all tenants"; a status table with values "Completed", "Verified" | yes — the card shows a status value the site displays; the film does not say how fast |
| `AUTOPAY: ON` — rent collection switched on | home.txt L19–20; autopay.txt L4–5, L9 | "Autopay / Collect rent automatically every month"; "Rent Collection. Now Fully Automatic."; "money moves to your account automatically" | yes — the card names the feature's on-state; no amount, no success rate, no "always" |
| `DUES VISIBLE` — the leaving tenant is tagged, not stopped | autopay.txt L116–117, L136; home.txt L92 | columns "Rent Amount / Dues", "Pending Dues"; "Excel Reports of Dues …" | yes — visibility of dues only; the ghost still leaves; the Eqaro guarantee block is correctly absent |
| `REPORTS: DONE` — the paper ball becomes a neat stacked report | home.txt L90 | "✅ Accounting Done ✅ Reports Done +7 more reports" | yes — the card is nearly the site's own phrase |
| `TICKETS RESOLVED` — three handsets become three ticked tickets | complaint-management.txt L24, L61–62, L71–76, L83 | "Complaints Resolved"; "submits a complaint ticket directly from the app"; "Ticket auto-appears on dashboard / Auto-assigned to team member"; "marks the ticket as resolved"; "Resolved status shown in Tenant App" | yes — the site's own resolved status; the film does not claim the app fixes the issue itself |
| `Get the app` (CTA, spoken and on screen) | home.txt L140 | "Get the app" | yes, verbatim |
| `India's renting superapp` (wordmark) | S-LOGO; tv L154 | the customer's own logo file (`source/brand/rentok-new-logo.webp`, hash recorded) | yes — customer asset, composited unchanged |
| the app icon on the phone (a white house pictogram on brand blue) | Stage 2 §2.4(d) "App icon: ORIGINATE — no icon file in the snapshot; an original in-game icon" | recorded decision, not a claim | within the record; **fidelity risk**: it is not RentOk's real icon (the snapshot has none), and a real customer may notice — see §7 |

Nothing depicted goes beyond its cited line. No percentage, price, timing promise or third-party guarantee appears anywhere (OBSERVED on all 60 frames and in all transcripts).

---

## 4. Production quality (C)

**Generated lettering.** All seven stills inspected at source resolution (`gen/stills/`): no letters, digits, labels or watermarks on the character sheet, the four other obstacle pairs or the world plate (no shop signs, no nameplate — the gate-1–4 REOPEN 1 was resolved by deleting the nameplate, and the plate indeed has none). **O4 tangle:** the papers carry short horizontal ruled strokes (the "greeked text" look of a drawn document). I zoomed the frame at 3× (f016, region 280–620 × 840–1160) and the source still: they are parallel lines of even weight with no letterforms, no word shapes, no digits. **My verdict: not lettering; acceptable.** At frame scale they read as "printed paper", which is what the obstacle needs.

**Brand mark legibility.** End card (f058): the wordmark is ~590 px wide on a 1080 frame, white/cyan on blue, and the tagline is legible; the `Get the app` button is a white pill with blue text, ~510 px wide. Both are clear at a 360 px phone render (§5). The wordmark's own rounded-rectangle background is a slightly different blue from the end-card blue, so a faint panel edge is visible round the logo (the producer recorded this; confirmed). On the in-game flag the wordmark is ~120 px wide: `RentOk` readable, the tagline not — acceptable for a flag.

**Text in the safe zone.** Confirmed visually on all 60 frames (yellow box on `contact.png`) and by pixel extents on the end card (y 608–1237). PASS.

**Animation, timing and layering — defects I found (none of these are in the producer's R1–R5 list):**

1. **Phone graphic rides over the `PG OWNER` name tag (14.9–15.3 s).** OBSERVED on f030 (15.0 s) and the crop `qa/checker/crop_14.5-15.5s_phone-over-name-tag.png`: as the phone rises into the frame during `INSTALLING...`, its top overlaps the tag and hides most of the final `R` (the tag reads roughly `PG OWNE▮`). The producer's `disjoint` check covers *text* regions only, so a non-text graphic crossing a text plate was not caught. Small, but it is the brand-moment frame.
2. **Flag pole drawn in front of the character during `LEVEL COMPLETE` (26.6–27.8 s).** OBSERVED on f054 (27.0 s) and the crop `crop_26.3-27.5s_flagpole-over-character.png`: after the flag slide the white pole runs vertically through the character's hand, torso and leg, and the lowered flag sits over the parked scooter. This is a layer-order slip (pole should be behind the player, or the player should stop short of the pole). It is on screen for 1.2 s at the film's celebratory beat.
3. **Voice line V2 starts 1.2 s before its words appear.** OBSERVED from `gen/render/LAYOUT.json` (C11 `INSTALLING...` on screen 14.60–15.87 s; C12 `RENTOK MODE: ON` banner first at 15.90 s) and my audio match (V2 "RentOk mode: on" begins 14.70 s). So the announcer says "mode on" while the screen still says "installing". The lane's own rule (Stage 3 §3.8, on-screen = spoken) is met in *words* but not in *time*. The producer's `vo schedule` gate checks overlap and film end, not this alignment.
4. **The red register (and at the flag, the phone) vanish in the jump, hurt, cornered and celebration poses.** OBSERVED on the character sheet `gen/stills/A1_character_sheet_v1.png`: cells 5 (jump), 6 (hurt) and 7 (hands-up) have the keys but **no register**; in the film the register therefore disappears at every jump (f004 2.0 s, 8.0 s, f052 26.0 s), throughout the freeze/cheat beats (f022, f027; 10.4–14.6 s) and on `LEVEL COMPLETE` (f054), then reappears when he runs. The producer's micro-qualification card, item 1, states "every cell carries every identifier" — that is not what the sheet shows (see the micro-qualification verdict below). At phone size this is subtle; on a large screen it is a continuity blink.
5. **The same hands-raised pose is used for defeat (`CONTINUE?`, f022) and for victory (`LEVEL COMPLETE`, f054).** OBSERVED. INFERRED: a viewer who registered "hands up = cornered" at 10.4 s sees the identical pose at 26.6 s under a victory banner; it reads as celebration because of the banner and fireworks, but the pose set is one short.
6. **Facial expression does not change while losing hearts.** The four run cells and the jump cell smile; only the brief hurt pose grimaces. During F2–F6 the owner is mostly smiling into the obstacles (f007, f011, f019). A tone observation; the hearts and knock-backs carry the "losing" information.
7. **Near-silence gaps around the install beat.** From my 100 ms level profile: 10.8–11.9 s sits at −40 to −50 dBFS (music dropped for the freeze; only heartbeat blips at 11.2/11.4 s and then V1), and **14.1–14.7 s sits at −45 to −55 dBFS** — a 0.6 s hole between V1 ending (14.55 s) and V2 starting (14.70 s), before the music returns at ~15.3 s. The freeze drop-out is designed (Stage 3 audio direction); the 0.6 s hole between the two announcer lines is INFERRED to be a by-product of the timeline stretch (F8/F9 grew to fit the measured VO). In a Reel a half-second of near-silence can feel like the sound cut out. Not clipping, not a fault of level — a pacing question.

**Producer-recorded items, re-checked:**
- Keying fringe on the keys: confirmed (f000 at 2× shows a small magenta/purple smear at the belt where the key ring is; at 1× the keys are a dark blob). The winged handsets (f019) also show a faint purple outline. Neither is visible as "magenta" at phone size; the keys just stop being keys.
- Run cycle: the four run cells on the sheet differ only in arm angle by a few degrees (OBSERVED on the sheet); I cannot judge motion from stills — the producer's statement that running reads via bob/tilt plus scroll is left as their observation.
- After-world recolour: sky and road turn brand blue at 16.0 s; the facades keep their warm colours (OBSERVED, f033 onward). It reads as "same street, different sky" — acceptable and arguably better for continuity.
- Wordmark panel edge on the end card: confirmed, faint.
- R1–R5: `TICKETS RESOLVED` fits inside the box (f049), the CTA bottom is 1237 ≤ 1248, the name tag stays at ground level during jumps (f004), the cheat bar clears the tag (f027) — the repairs hold in the delivered file.

**Audio defects checked by code:** none — no clipping, no silence ≥ 0.3 s at −40 dB, true peak −2.2 dBTP, VO lines do not overlap each other (V1 ends 14.55, V2 starts 14.70; V3 ends 29.43 before the 29.8 s film end), music present under the VO (ducked, not muted, at 12–14.5 s: −22.6 dBFS mean vs −21.9 before). For each of the eleven events in `gen/render/CONTACT_EVENTS.json` I looked for a level jump within ±0.3 s (50 ms windows): the five struggle contacts have a 7–17 dB rise within 0.1 s of the recorded time (2.40, 4.30, 6.15, 7.75→peak 8.00, 9.85 s; the O4 paper-ball hit is the softest at 6.7 dB — a rustle), the flag capture rises 15.6 dB at exactly 25.90 s, and the five beam hits each have a 9–18 dB rise **0.25 s before** the recorded transform time (17.40, 19.05, 20.65, 22.25, 23.85 s) — INFERRED: the beam sound fires when the beam is launched and the obstacle changes a quarter-second later, which is consistent across all five and reads as intended, not as a sync error. An effect fires on every hit.

### Micro-qualification of the nine-pose character sheet — my verdict against the six-point card (Stage 4 §4.4)

| # | card item | my finding (OBSERVED on `gen/stills/A1_character_sheet_v1.png`, sha256 re-hashed = frozen value) | verdict |
|---|---|---|---|
| 1 | one identity across all nine cells, listing face, hair, glasses, shirt, trousers, chappals, key ring, red register | face, hair, glasses, shirt, trousers, chappals and key ring are constant in all nine; **the red register is present in 6 of 9 cells and absent in jump, hurt and hands-up** | PASS on identity; **the card's "every cell carries every identifier" is inaccurate** — a prop, not an identity, is missing in three cells |
| 2 | no cap, moustache, overalls, gloves | none in any cell | PASS |
| 3 | no lettering/digits/grid/watermark | none; phone screens plain blue | PASS |
| 4 | flat solid magenta, keyable | uniform magenta, no gradient or shadow | PASS |
| 5 | side view, full body, same proportions | consistent three-quarter side view facing right in all nine | PASS |
| 6 | pose set complete | run ×4 (near-identical), jump, hurt, hands-up, powered-run ×2 | PASS with the producer's own note on the run cells |

**Checker verdict on the micro-qualification: PASS for its purpose (identity, IP, keying, no text — the gated items).** The producer's card overstates item 1; the cost of that overstatement is defect 4 above (a disappearing register), which is real but minor. Had the card been read strictly, the repair allowance (one re-draw, USD 0.067) would have been spent here or the register composited by code.

---

## 5. Creative quality (B) — observations, not a verdict

- **Does it read as a platform game?** Yes as a genre signal: side-scroll, hearts, level label, score, one enemy at a time, a freeze-and-continue, a flag pole, chiptune bed. What is missing from the platformer vocabulary is platforms: the level is one flat pavement; the character's two jumps land on the same ground. A viewer is more likely to say "runner game" than "Mario-type game". The gate-1–4 checker's NOTE 6 (one ledge or gap) was not adopted.
- **Frame use.** Because the world plate was drawn at 16:9 (1376×768) and scaled to the 1080 width, the drawn street occupies roughly rows 640–1250 of the 1920-tall frame; the top ~30 % is sky with the HUD and the bottom ~33 % (rows 1256–1896, measured) is a flat synthetic road with a dashed centre line and nothing on it. At phone size (my 360 px render of f007/f027/f035/f052) the eye reads a wide-screen game letterboxed into a vertical phone. Stage 3 §3.11 promised "a tall PG building facade filling the height (sky above, street below)"; the delivered frame is a three-storey facade in the middle third. Everything critical is inside the safe zone, so nothing is *lost*, but a third of the screen is doing nothing for 27.8 s.
- **Readable at phone size?** Labels (60 px caps), cards (72 px condensed) and the HUD are clearly legible at 360 px wide. The character is about 1/7 of the frame height and readable as a man in an orange shirt; the obstacles read as shapes plus label. The beam is a one-pixel-ish cyan line at 360 px — visible, not emphatic; the `OK` glyph disappears entirely. The keys are a dot.
- **Install → power-up → clearing without sound?** Yes. The chain is carried by: hearts emptying → `CONTINUE?` → the cheat bar typing itself → a phone with an app icon and `INSTALLING...` → `RENTOK MODE: ON`, hearts refilled, sky blue, glow → five beam hits each with a card → flag → `LEVEL COMPLETE` → end card. Every step has a visual. The one soft link is *why* the beam hits produce those cards: the cards are statuses, and a first-time viewer has to infer "the app did this".
- **Does the voice help or hurt?** I cannot hear it; from the record: three short lines (2.6 / 2.2 / 2.7 s), same Sarvam voice, verbatim to the screen, at −14 LUFS with the bed ducked 6 dB. Structurally it helps (the brand name is spoken three times; the CTA is spoken). The V2 timing slip (defect 3) is the one place it could hurt, and the producer's audition compared A vs C only on paper — the ear check remains open.
- **Tone.** Smiling owner, cute enemies, warm palette: friendly rather than tense. The "losing" half (0–10.4 s) is not visibly stressful; the transformation is therefore a relief of *labels*, not of a character in trouble. The customer asked for "problems the owner faces"; a stressed owner would sell the install harder. Taste, not compliance.

---

## 6. Failure classification

| defect | found by | earliest stage affected | one repair at that layer |
|---|---|---|---|
| D-1 phone over the name tag, 14.9–15.3 s | checker | 5 execution (compositor) | extend `check_disjoint` to non-text critical graphics (phone, beam, flag) or start the phone rise 60 px lower; USD 0 re-render |
| D-2 flag pole drawn over the character, 26.6–27.8 s | checker | 5 execution (layer order) | draw the pole behind the player layer, or stop the player 40 px left of the pole; USD 0 |
| D-3 V2 spoken 1.2 s before its on-screen words | checker | 5 execution (timeline derivation) | start V2 at 15.9 s (it ends 18.1 s, overlapping the first card by 0.4 s) **or** show `RENTOK MODE: ON` at 14.7 s and shorten `INSTALLING...` to 0.1 s of the phone rise; USD 0 |
| D-4 register missing in three poses (card item 1 overstated) | checker | 5 execution (micro-qualification judgement); the card itself (Stage 4) was right | composite a code-drawn register on the three cells, or accept and correct the card's wording; a re-draw would be USD 0.067 |
| D-5 lower third of every game frame is empty road; frame reads letterboxed | checker | 4 selection (world plate specified as 16:9, so it cannot fill 9:16; Stage 3 promised a height-filling facade) | at Stage 4: specify the plate at 9:16 or a two-row facade (one nb2 draw, USD 0.067); at Stage 5 only a code patch is possible (a foreground pavement layer with kerb, drain, parked objects) |
| D-6 same hands-up pose for defeat and victory | checker | 3 creative (pose list) → 4 (sheet spec) | add a distinct "arms-up cheer" cell to the sheet spec; USD 0.067 re-draw or accept |
| D-7 0.6 s near-silence between V1 and V2 | checker | 5 execution (mix) | let the bed re-enter at 14.5 s instead of 15.3 s, or a heartbeat blip in the gap; USD 0 |
| D-8 `ATTEMPTS.jsonl` verdicts all `pending` | checker | 5 execution (record hygiene) | write the JOB.yaml verdicts back into the attempts file; USD 0 |
| O4 scribble marks | producer (recorded) | — | none needed (not lettering) |
| run cycle relies on bob/tilt | producer (recorded) | 5 (micro-qualification accepted it) | re-draw of the four run cells, USD 0.067, only if a human viewer finds the run stiff |
| keying fringe on keys | producer (recorded) | 5 (keying) | 1 px more erosion on the key region, or a code-drawn key ring; USD 0 |
| wordmark panel edge on end card | producer (recorded) | 5 (compositor) | match the panel blue to the end-card blue or drop the panel; USD 0 |
| app icon is an invented pictogram | producer (recorded as a Stage 2 decision) | 2 structure | ask the customer for the real icon at delivery, or draw a plain phone screen with the wordmark instead; USD 0 |
| beam and `OK` glyph faint at phone size | checker (observation) | 3 creative (power-up design) | thicker beam with a glow and a larger `OK`; USD 0 |
| no platforms in a "platform game" | checker (observation; gate-1–4 NOTE 6) | 3 creative | one ledge and one gap in F2–F6; USD 0 in code |

No defect traces to Stage 1 (intent) or to the customer's inputs. No defect requires a paid call to fix; D-5 and D-6 would if fixed properly.

---

## 7. Verdict on release-readiness for the blind customer evaluation

**DELIVERABLE WITH DEFECTS.**

- Every A-item is PASS or an HJ item the customer judges: A1 PASS (LJ), A2 PASS, A3 PASS (5/5), A4 PASS, A5 PASS, A6 PASS, A7 PASS (DET), A8 PASS (DET + LJ), A9 PASS on picture / sound not checkable by me (provenance verified), A10 HJ, A11 PASS (DET + LJ). The file is in spec. No A-item fails deterministically.
- Defects to declare with the delivery (all visible to a careful viewer, none changes what the film says): **D-1** the phone hiding part of `PG OWNER` at 15 s; **D-2** the flag pole drawn through the character at 26.6–27.8 s; **D-3** the "RentOk mode on" voice arriving 1.2 s before the words; **D-4** the register that blinks out in jump/freeze poses; **D-5** the empty lower third of the frame (a layout choice a customer will see as "the game only uses half my screen"); **D-7** the half-second sound hole at 14.1–14.7 s. All are USD 0 re-renders except D-5, which is a plate decision.
- I did not soften anything: no A-item is failed by these, and I did not find any string, picture or sound that makes a forbidden claim or reproduces a Nintendo asset.

---

## For the Controller (plain English)

This is a 30-second vertical cartoon that plays like a small retro game: a smiling PG owner in an orange checked shirt, keys on his belt and a red rent register under his arm, runs along an Indian street and is knocked back by five monsters that are his five real problems (an unverified tenant, unpaid rent, a tenant who left owing money, a mess of accounts, complaint calls); he runs out of hearts, a `CONTINUE?` screen appears, the cheat code `INSTALL RENTOK` types itself, a phone rises into his hand, the sky turns RentOk blue, and he runs back through the level turning each monster into a status the RentOk website really lists (verified, autopay on, dues visible, reports done, tickets resolved), grabs a RentOk flag, and the film ends on the logo with "Get the app". With code I confirmed: the file is exactly the one the producer recorded (same hash), 30.000 s, 1080×1920, H.264/AAC, fast-start, loud enough for social and never distorting; all 25 paid calls are on the ledger in the right order, USD 0.587 of the USD 10 cap, three failures honestly counted; the three announcer lines in the mix are the Sarvam takes and the music is the Lyria draw, both matched by signal analysis; every product statement on screen is a row of the permitted list and every cited website line says what the producer says it says. With my eyes I confirmed the five problems, the cheat code, the power-up, the five clears and the flag, and found no Nintendo look-alike anywhere; I could not listen to the sound, so whether the music accidentally hums a famous tune is the one thing no one has checked by ear. I also found six small execution slips the producer did not record: the phone briefly covers part of the `PG OWNER` tag, the flag pole is drawn through the hero at the end, one voice line arrives a second early, the register vanishes when he jumps, there is a half-second of near-silence mid-film, and the bottom third of every game frame is an empty grey road because the street was drawn as a wide picture and dropped into a tall frame. The two things most likely to make a real customer reject it: **(1) it looks like a wide-screen game letterboxed into a phone — a third of the screen is empty road and there are no platforms to jump on, so "Mario game" may feel like "runner with labels"; (2) the obstacles are converted into tidy status cards rather than "killed", and the owner smiles all the way through, so the customer's "problems → cheat code → blast them all" story arrives as calm and friendly rather than dramatic.** Neither breaks a requirement; both are what a customer who wrote "kills all the obstacles" will notice first.

---

# Re-verification after repair round 1 (producer commit `40ff61c`)

Same checker session, same rules: USD 0, no producer file edited, my own measurements only. Evidence in `qa/checker/round1/` (fresh 2 fps contact sheet `contact.png` with the safe box drawn; the frames I relied on as `tNN.N.png` = seconds; four comparison crops). The first-round folder `qa/checker/` still refers to v1, now kept by the producer at `gen/final/v1/`.

## 1. Re-measured (OBSERVED)

| what | measured by me | producer / JOB.yaml | match |
|---|---|---|---|
| sha256 of `gen/final/rentok-game-lane-b-9x16-30s.mp4` | `40cf2f40bf50c88d04afebb98ea91f6896a83aac8ad4fbdc010b0e289eb42c78` | `JOB.yaml outcome.assets[0]` and `final_geometry` both carry this hash; v1 hash recorded under `superseded_v1` | yes |
| duration / geometry / codecs | 30.000 s, 1080×1920, H.264 High yuv420p 30 fps 900 frames, AAC-LC 48 kHz stereo, 15,284,419 bytes | same | yes; A7 still PASS |
| loudness (`ebur128`) | I −14.3 LUFS, LRA 4.7 LU, true peak −1.8 dBTP | I −14.3 / TP −1.8 | yes; no clipping (flat factor 0), no silence ≥ 0.3 s at −40 dB |
| VO positions (spectral match of the three Sarvam takes against the new mix) | V1 at **11.90 s**, V2 at **15.90 s**, V3 at **26.70 s** | V1 11.9–14.545 · V2 15.9–18.119 · V3 26.7–29.431 | yes — V2 moved from 14.70 to 15.90 s exactly |
| ledger | `LEDGER.jsonl` byte-identical to the file I audited (git diff `ac794da..40ff61c` touches `ATTEMPTS.jsonl` only); 25 attempts, reserved sum 0.58675, cumulative 0.58675 | "spend unchanged, no paid call" | yes |
| `ATTEMPTS.jsonl` | 25 rows; the only field that changed is `verdict`; now accepted 11 / qa_evidence 7 / not_selected 4 / failed 3, **0 pending** | "0 pending" | yes |

## 2. Per-defect result

| # | defect (round 1) | result | what I relied on |
|---|---|---|---|
| D-1 | phone graphic over the `PG OWNER` tag at ~15 s | **FIXED** | `t15.0.png`, crop `crop_15.0-16.0s_…`: the phone now rises ~110 px to the right of the tag; clear gap; at 15.9/16.0 s the phone is in the raised hand. The producer's `disjoint` check now includes graphics (`G-*` boxes in `LAYOUT.json`) — OBSERVED in `tools/qa_checks.py` |
| D-2 | flag pole drawn through the character, 26.6–27.8 s | **FIXED** | `t26.6.png`, `t27.2.png`, crop `crop_26.6-27.6s_…`: the pole stands well to the right of the player (≈160 px clear), pole and flag are behind him, and the hold is a small hop in the jump cell rather than the hands-up pose (which also closes my D-6 note). New minor observation below (N-1) |
| D-3 | V2 spoken at 14.7 s, words shown at 15.9 s | **FIXED** | audio match: V2 begins 15.90 s; `t15.9.png`: the `RENTOK MODE: ON` banner and the lit HUD slot are on screen in the same frame. Consequence the producer declared: V2 now ends 18.12 s, ~0.4 s over the first beam hit (17.7 s) — one card appears while the announcer finishes "on"; no line overlaps another line |
| D-4 | red register absent in jump / hurt / cornered poses | **FIXED** | `t8.0.png` (jump into the paper ball), `t11.0.png` (cornered under `CONTINUE?`), `t27.2.png` (celebration hop), crop `crop_2.0-11.0s_…`: a red register now sits at the hip/under the arm in every pose. In the hands-up pose it hangs at the left hip while the arm is raised — plausible, slightly stiff. `qa/A1-microqual-card.md` item 1 corrected (OBSERVED) |
| D-5 | lower third of every game frame an empty road | **PARTIAL (by a stated design limit)** | `contact.png`, `t8.0.png`, `t21.0.png`, crop `crop_24.0s_…lower-band`: the band y ≈ 1240–1560 is now a foreground pavement that scrolls faster than the street (near-parallax) with planters/bushes, bollards, storm drains and the plate's own scooter; the road with lane dashes fills y ≈ 1560–1900. Measured: near-uniform-colour rows in the lower part fell from 640 (33 % of the frame, v1) to ~344 (18 %) on a warm frame. It no longer reads as a wide game letterboxed into a phone; it reads as a street with a deep foreground sidewalk. What remains: about a third of the picture below the action is scenery with no play in it, because the producer chose to keep the player's feet inside the Meta safe box (y ≤ 1248). That reasoning is sound for Reels; a customer viewing on a large screen will still see a lot of pavement. Recorded as PARTIAL, not as a failure |
| D-6 (audio) | 0.6 s near-silence between V1 and V2 | **PARTIAL** | my 100 ms level profile on the new mix: 14.2–14.5 s still sits at −44 … −50 dBFS (0.3–0.4 s, inside V1's own tail after its last word), then −31/−30 at 14.6–14.7 s as the bed re-enters at 0.55 gain, then −14 at 14.8 s (the hum), −38 at 15.1 s for one window, and full level from 15.5 s. The producer's stated test ("no window below −40 dBFS between 14.5 and 15.9 s") holds (min −38). The hole shrank from ~0.6 s to ~0.35 s and moved earlier; it is the voice file's own silent tail over a fully ducked bed. Audible? I cannot listen; by the numbers it is now a breath, not a drop-out |
| D-8 | `ATTEMPTS.jsonl` verdicts pending | **FIXED** | 0 pending, ledger untouched (table above) |
| D-9 (producer-found) | beam 8 px under the tag at 23.9–24.1 s | **FIXED** | `t24.0.png`, crop `crop_24.0s_beam-tag…`: the beam leaves the phone ≈ 40 px below the tag's bottom edge, clear of it |
| note | green tick on the drifting ghost's tag | **FIXED** | `t21.0.png`: the tag now carries a cyan ring-with-dot marker (a "tracked" symbol), not a tick; `DUES VISIBLE` unchanged |

**New observations introduced by the repair (none blocks delivery):**
- **N-1 The player no longer touches the flag pole.** Because he stops 160 px short (to keep the pole behind and clear of him), the flag slides down on its own as he lands (`contact.png` f052–f053, 26.0–26.5 s; `t26.6.png`). Genre convention is that the player grabs the pole; a viewer may read "he reached the flag" rather than "he got the flag". The customer's sentence "gets the flag" is still met in substance (level ends at the flag with `LEVEL COMPLETE`), so A6 stays PASS.
- **N-2 V2 runs 0.4 s into the first card** (declared by the producer; measured 18.12 vs 17.7 s). Harmless in words (`TENANT: VERIFIED` is a different line, unspoken); slightly busy in sound.
- **N-3 The foreground band is sparse**: on most frames it shows one planter or a pair of bollards over ~320 px of flat pavement; nothing in it occludes the player, obstacles, labels or cards (checked on all 60 contact frames — the band starts ~90 px below the ground line). No text ever enters it.
- I checked the round-1 A-items that could have moved: hearts, HUD, labels, cheat bar, cards, end card all unchanged in wording and position; safe box still contains every critical element on all 60 frames (yellow box on `round1/contact.png`); A11 strings unchanged (the only new pixels are the pavement props and the ghost marker, neither carries text).

## 3. Verdict (updated)

**DELIVERABLE.** Every A-item is PASS or an HJ item; the six execution slips I reported are fixed or reduced to design-level residue that I would not call a defect (a deep sidewalk kept for the safe zone; a 0.35 s breath between two voice lines). No new defect was introduced. Sound remains unheard by anyone — the one open check.

**The two most likely customer-rejection reasons now:** (1) **"Not Mario enough"** — the level is a flat run with hits and a hop; no platforms, no pit, no stomp, and the obstacles are *converted* into status cards rather than "killed" — a customer who wrote "runs and kills all the obstacles" may find the transformation too polite; (2) **tone** — the owner smiles through every hit and the world is warm and cute, so the "problems" half never feels like trouble; the install reads as a nice upgrade rather than a rescue, which weakens the reason to get the app. Both are creative judgements (Stage 3), not compliance misses, and both are what the blind evaluation exists to test.
