# Independent blind evaluation — RENTOK-CREATIVE-QUALITY-001

Evaluator: a fresh Claude Opus 5 session that did not write, direct, prompt, render or check any clip. Date: 2026-09-21. Cost: USD 0.

**What I was allowed to see:** `06-EVALUATION-PROTOCOL.md`, `00-EXPERIMENT-CONTRACT.md` §1–§2, `shared/COMMUNICATION-STANDARD.md`, and the packet (`clip-1.mp4` … `clip-4.mp4`, their 10-fps contact sheets, `README-FOR-EVALUATOR.md`, `SEAL.txt`). No customer-brief file was present in `treatments/A-baseline/frozen-inputs/` (only `board.json`, `copy-deck.json`, `PROVENANCE.md`, which look like treatment inputs; I did not open them). The mandatory requirements were taken from the protocol's R1–R8 table. I did not open any treatment folder, ledger, mapping file, files 01–05 or git history.

**What I could not do:** I cannot hear. Every statement about sound below comes from measurements (loudness over time, spectrograms, a speech-band check) — not from listening. Audio scores are marked *provisional* and need a human ear.

**Method:** SHA-256 of every clip matched `SEAL.txt`. Each clip was probed with `ffprobe` and an MP4 box walk; frames were extracted at 10 fps (and at 30 fps around the moments that mattered) and viewed at full size and at phone width (360 px). Frame `fNNN` below means the frame at NN/10 seconds (e.g. `f050` = 5.0 s). Cited frames are in `evaluation/frames/clip-N/`; composite views are in `evaluation/frames/composites/`; spectrograms in `evaluation/frames/audio/`.

Terms used: **OBSERVED** = I saw or measured it; **INFERRED** = my reading of what I saw; **PROVISIONAL** = scored from measurement only because I cannot hear.

---

## 0. Same-event check (before any scoring)

Event list from the protocol: confront complaints → hit, GAME OVER? → cheat code entered, RentOk installed → visible power → power used on the document wall, wall cleared → product chip lands.

| Clip | Events present, in order | OBSERVED timeline (seconds) |
|---|---|---|
| clip-1 | Yes, all seven | run at complaints 0.0–0.9 · hit and kneel, grey wash, GAME OVER? 1.0–1.4 · phone falls from the sky into his hand while the cheat code types 1.1–2.6 · burst and POWER UP 2.9–4.3 · run 4.4–4.9 · TENANT VERIFICATION wall 4.9 · lightning beam hits it 5.0–6.0 · wall breaks into paper, smoke, fire 5.2–6.8 · ✓ DIGITAL KYC chip from 5.4 to end |
| clip-2 | Yes, all seven, plus an extra "COLLECTING RENT" label at the very end | complaints 0.0–0.2 · white damage flash 0.2 · GAME OVER? 0.6–0.8, grey from 0.8 · cheat box slides up 1.1–1.5, types to 3.6 · full-frame white flash 3.7 · colour returns, cyan outline, phone icon 3.8 · POWER UP 4.0–5.2 · TENANT VERIFICATION 5.7 · run, tiny ✓ projectile 6.0–6.4 · paper stack slices and fades 6.4–6.7 · chip 6.4–6.9 · COLLECTING RENT 6.9 |
| clip-3 | Yes, all seven | same structure and timing as clip-2 (flash 0.1, GAME OVER? 0.5–0.7, box 1.0–3.6, flash 3.7, POWER UP 4.0–5.2, TENANT VERIFICATION 5.6, projectile 6.0–6.3, stack fades 6.3–6.6, chip 6.4–6.8) |
| clip-4 | Yes, all seven | complaints 0.0 · knocked backwards with an impact star, book flies 0.1–0.4 · GAME OVER? 0.5–0.7, scene dims · on hands and knees looking up at the code 0.6–3.3 · box 1.0–3.5 · stands with phone 3.4 · white flash 3.6 · POWER UP 4.0–5.2 · TENANT VERIFICATION 5.6 · wind-up 5.8, throw 6.1, tiny ✓ projectile · stack flashes white, slices and fades 6.4–6.7 · chip 6.4–6.7 (gone before the end) |

No clip is missing an event. Order is correct in all four. The four clips are the same length within 0.1 s (6.83–6.87 s of picture).

---

## Part (i) — Mandatory customer requirements (PASS / FAIL / CANNOT_DETERMINE)

| # | Requirement | clip-1 | clip-2 | clip-3 | clip-4 |
|---|---|---|---|---|---|
| R1 | PG owner recognisable (spectacles, checked shirt, keys, red register) | **PASS** — f007, f040; keys at belt visible in `composites/c1-faces.jpg` | **PASS** — f001, f047 (`composites/c2-faces.jpg`) | **PASS** — f000, f061 (`composites/misc-zoom.jpg`) | **PASS** — f000, f034 (`composites/c4-faces.jpg`) |
| R2 | Obstacles recognisable from the picture before the label | **PASS** — red angry speech-bubbles with "!" read as complaints (f007). Second obstacle: a white sheet mass enters at f049 as the label appears; it reads as paperwork mainly while it breaks into sheets (f056–f068). Marginal on the second obstacle. | **PASS** — angry bubbles f001; stacked paper bundles with a "?" f060–f063 read as paperwork before the label needs reading | **PASS** — f000; tall paper stack f058–f062 | **PASS** — f000–f004; paper stack f058–f063 |
| R3 | Install/activation is a distinct visible event that changes the scene | **PASS** — a phone drops from the sky and is caught (f013–f025), the cheat box types, the grey world returns to colour, a burst follows (f029–f030) | **PASS** — typed cheat code, full-frame white flash, grey → colour (f016–f040) | **PASS** — same as clip-2 (f015–f040) | **PASS** — typed code, he rises and holds the phone up (f034), white flash (f036), colour returns |
| R4 | A change on the character after the install (not only a HUD colour) | **PASS** — cyan aura and sparks on his body, phone held aloft (f036, f040) | **PASS (marginal)** — a thin cyan outline around the sprite and a small floating phone icon beside him (f040, f047); nothing else on the character changes | **PASS (marginal)** — same as clip-2 (f040, f048) | **PASS** — cyan outline plus a new stance holding the phone up (f034, f040, f047) |
| R5 | Powered action (he does something with the power) | **PASS** — fires a lightning beam from his hand (f050–f056) | **PASS (marginal)** — a ✓ tick the size of a fingernail flies from him while he runs (f061–f063; `composites/c2-contact-30fps.jpg`). At phone width it is invisible (`composites/phone-wall.jpg`). | **PASS (marginal)** — same as clip-2 (f060–f062) | **PASS** — a wind-up pose (f058) and a throw pose (f061) launch the tick; the pose sells the action even though the projectile is tiny |
| R6 | Physical interaction: the power contacts the obstacle and the obstacle responds | **PASS** — beam hits, wall cracks, burns, throws sheets and smoke (f053–f068) | **PASS (marginal)** — the tick reaches the stack at 6.4 s and the stack slices into vertical strips and fades out (`composites/c2-wall-zoom.jpg`, f064–f065). It is a dissolve with a few drifting sheets, not a break. | **PASS (marginal)** — same as clip-2 (f062–f064) | **PASS** — the stack flashes white on contact (f064, `composites/c4-extra.jpg`), sheets fly off the top, then it slices and fades (f066) |
| R7 | Clear payoff (chip / status) | **PASS** — "✓ DIGITAL KYC" on screen ≈ 1.5 s (5.4 s to end); appears while the wall is still breaking | **PASS** — chip ≈ 0.6 s (6.4–6.9), rises to the HUD | **PASS** — chip ≈ 0.5 s (6.4–6.8) | **PASS** — chip ≈ 0.4 s (6.4–6.7) and it is gone before the clip ends (f068 has no chip) |
| R8 | Reads as an actual platform game, not a film with a HUD on top | **PASS** — side-on world, HUD, hearts bar that empties and refills, ground plane. Caveat: the character and effects are soft and painterly while the HUD and background are crisp pixel art, so the picture reads as two styles composited together (see `composites/c1-wall-zoom.jpg`) | **PASS** — one coherent pixel-art game look | **PASS** — one coherent pixel-art game look | **PASS** — one coherent pixel-art game look |

No clip fails a mandatory item outright. Clips 2 and 3 pass R4–R6 only marginally: their powered action is a projectile so small that at phone width the wall appears to dissolve on its own, which is exactly what R6 says must not happen. I have recorded these as marginal passes rather than fails because at full size the contact is verifiable frame by frame.

---

## Part (ii) — Creative-quality scores (1–5, protocol anchors; no half points)

| Criterion | clip-1 | clip-2 | clip-3 | clip-4 |
|---|---|---|---|---|
| Q1 Prompt adherence | **3** | **2** | **2** | **3** |
| Q2 Visual quality | **3** | **3** | **3** | **3** |
| Q3 Character expressiveness | **4** | **2** | **2** | **4** |
| Q4 Motion quality | **4** | **2** | **2** | **3** |
| Q5 Environmental richness | **3** | **3** | **3** | **3** |
| Q6 Gameplay readability | **4** | **2** | **2** | **3** |
| Q7 Audiovisual impact (PROVISIONAL) | **4** | **2** | **2** | **3** |
| Q8 Commercial suitability | **4** | **2** | **2** | **3** |

### What I saw, one sentence per score

**clip-1**
- Q1 = 3: every event is present and in order, but the finished cheat code "INSTALL RENTOK APP" is on screen for exactly one frame (1/30 s) before the box clears (`composites/c1-typing-end2.jpg`), the chip appears at 5.4 s while the wall is still standing, and for a few frames the dropped red register lies on the ground while he also holds one (f029–f030).
- Q2 = 3: the burst, beam, fire, smoke and flying sheets are attractive and have depth, but the character is drawn soft and wobbly, the complaint bubbles smear into a red blob at the hit (f011–f013, `composites/c1-extra.jpg`), and the crisp pixel HUD sits on a painterly picture — a careful viewer notices.
- Q3 = 4: he runs, crumples with a grimace (f013), shouts with an arm raised as the phone falls (f022), stands calm and lit (f040), leans into the beam (f050) and jogs out with a slight smile (f068) — pose and face both carry each beat.
- Q4 = 4: the hit stops him and drops him, the falling phone gives the install anticipation and a catch, the burst throws the bubbles skyward, the beam has recoil in his stance and the wall answers with chunks, fire and smoke; not a 5 because the body wobbles and the cheat-code timing is off.
- Q5 = 3: two-layer world (facade and road) with sky, greys at defeat and returns to colour at the power-up, water tanks appear as it scrolls; no people, traffic or life.
- Q6 = 4: obstacle, hit, life bar emptying, power, a fired beam, a broken wall and a refilled bar all read as rules with cause and effect; there is ground and distance but no jumping, and the phone-from-the-sky feels like a cut-scene rather than play.
- Q7 = 4 (PROVISIONAL): measured levels rise sharply at the hit (1.0 s), tick during typing, burst at the power-up (3.0 s), fall to their quietest just before the beam (4.75 s) and peak at the wall strike (5.0 s, the loudest moment in any clip); loudness range 7.7 LU means real dynamics; broadband noise bursts on the spectrogram line up with the impacts (`audio/spectrogram-clip-1.jpg`); whether the music fits I cannot say.
- Q8 = 4: the problem visibly hurts, the install is the turning point, the power is enjoyable and the chip is legible for 1.5 s; not a paid-Reel-ready 5 because of the one-frame cheat code and the smearing.

**clip-2**
- Q1 = 2: all events present, but the powered action (the tick) is barely legible even at full size and invisible at phone width, and an extra "COLLECTING RENT" label intrudes at the end (f069).
- Q2 = 3: clean, crisp pixel art with the richest street of the four (wires, transformer, water tanks, shutters, tree, a cart), but the character is a sprite standing still on a background for 3.5 s.
- Q3 = 2: one frowning face throughout; the only visible change is standing → running (`composites/c2-faces.jpg`); the hit is a white flash with no change of pose.
- Q4 = 2: hit = flash, install = flash, power = an outline, the tick slides at constant speed and the stack fades; bodies rigid, motion linear.
- Q5 = 3: a detailed backdrop with layers, and the world goes grey at the defeat and warm at the power-up.
- Q6 = 2: HUD and scrolling are there, but he stands and things happen to him on cue for the first four seconds; the run-and-tick is the only thing he does.
- Q7 = 2 (PROVISIONAL): a chip-tune-style continuous bed with regular pulses during the typing, a rising arpeggio at the flash and down-sweeps at 4.6 s and 6.0 s — cues are on the events (`audio/spectrogram-clip-2.jpg`) — but loudness range is 2.9 LU and the level does not drop at the defeat, i.e. the music runs flat through the story.
- Q8 = 2: the install reads as a colour change plus a label; the problem does not visibly hurt (he never falls) and the chip is up for 0.6 s.

**clip-3**
- Q1 = 2: as clip-2 (tick barely legible), without the extra end label.
- Q2 = 3: clean and consistent, but a plainer backdrop than clip-2 and the smallest sprite of the four, so less to look at.
- Q3 = 2: one face, standing → running only (`composites/misc-zoom.jpg`).
- Q4 = 2: as clip-2 — flashes mark events, nothing has weight.
- Q5 = 3: apartment blocks, sky gap, road with a cart; grey at defeat, colour at power-up.
- Q6 = 2: as clip-2 — the character does not seem to play.
- Q7 = 2 (PROVISIONAL): the audio track is byte-identical to clip-2's (same decoded checksum), so the same reading applies.
- Q8 = 2: as clip-2; the small sprite makes the product moment even easier to miss.

**clip-4**
- Q1 = 3: every event has its own moment (knock-down, kneel, code, rise, flash, wind-up, throw, hit-flash, chip), with two small intrusions: the cheat box slides up over the character for a few frames (f012) and a translucent ghost of the box hangs over the scene after the flash (f037, `composites/c4-extra.jpg`).
- Q2 = 3: crisp, consistent pixel art with an impact star, a hit-flash on the wall and paper flying; the box ghost and the overlap are the only blemishes.
- Q3 = 4: neutral run (f000), shock with arms up and mouth open as he is thrown (f004), worried on hands and knees looking up at the code (f009, f020), content as he studies the phone (f034), determined in the wind-up (f058) — face and pose at every beat; the states cut rather than flow, so not a 5.
- Q4 = 3: the hit lands (knock-back, dropped book, impact star), the throw has a wind-up, the wall flashes on contact; but the projectile slides at constant speed and the wall fades rather than breaks.
- Q5 = 3: same backdrop as clip-3; the world dims rather than greys at the defeat and brightens after.
- Q6 = 3: obstacle, hit, power, throw, contact and clear read as rules you could play; the projectile is too small for a player to "feel" it and there are no jumps.
- Q7 = 3 (PROVISIONAL): the same effect set as clips 2/3 (typing pulses, rising arpeggio, down-sweeps) but with near-silences before the box (1.5 s) and before the flash (3.25 s) and a strong broadband hit at the knock-down (0.0–0.75 s), so the level does move with the story (`audio/spectrogram-clip-4.jpg`); there is no continuous bed in the first half.
- Q8 = 3: the problem hurts and the fix relieves, the install is the clear turning point; the chip lasts 0.4 s and disappears before the end, and the power is hard to see at phone width.

### Rank on creative quality (recorded separately from the scores)

1. **clip-1** — the only clip where the power visibly does something: the beam-into-exploding-wall beat is the most watchable second in the packet.
2. **clip-4** — the only clip whose character actually acts (thrown, kneels, looks up, winds up), which makes the story land despite thin effects.
3. **clip-2** — the richest street, but the owner stands still for half the clip and the power is a label.
4. **clip-3** — the same beat as clip-2 with a smaller sprite and a plainer street, so even less to read.

### Rank on "would a customer who wants a modern, polished platform-game feel accept this beat"

1. **clip-1** — closest on feel (impact, particles, light, a life bar that reacts), but I would expect a customer to ask for the smeared hit and the soft character to be cleaned up before accepting; it is polished in effect, not in drawing.
2. **clip-4** — closest on craft coherence (one crisp style, real character animation), but the power beat is too small to satisfy; a customer would ask "where is the power?".
3. **clip-2** — a customer would read this as a nicely drawn scene in which nothing much happens.
4. **clip-3** — as clip-2, smaller.

The gap between clip-1 and clip-4 is narrower on this second ranking than on the first: clip-1 wins on feel, clip-4 on finish, and neither would be accepted as-is (INFERRED from the customer's own words in the contract §1 — "technically functional but creatively poor" describes clips 2 and 3 well).

---

## Part (iii) — Technical constraints (measured)

| Check | clip-1 | clip-2 | clip-3 | clip-4 |
|---|---|---|---|---|
| Geometry / codecs | 1080×1920, H.264 + AAC 48 kHz stereo | same | same | same |
| Frame rate | 30 fps, 205 frames | 30 fps, 206 frames | 30 fps nominal; average rate 29.93 (timestamps slightly uneven), 205 frames | 30 fps, 205 frames |
| Duration (picture / container) | 6.83 s / 6.89 s | 6.87 s / 6.93 s | 6.85 s / 6.88 s | 6.83 s / 6.88 s — all inside 5.0–8.0 s |
| Container | ftyp-moov-free-mdat (moov first), no edit lists, only generic encoder tags | same | same | same |
| Loudness (integrated) | −13.8 LUFS ✓ | −13.3 LUFS ✓ | −13.3 LUFS ✓ | −15.1 LUFS ✓ |
| True peak | **−0.2 dBTP — over the −1 dBTP limit** | −2.1 dBTP ✓ | −2.1 dBTP ✓ | −2.5 dBTP ✓ |
| Loudness range | 7.7 LU | 2.9 LU | 2.9 LU | 2.9 LU |
| Silence ≥ 0.3 s below −40 dB | none | none | none | none (brief dips to −43 dB at 1.5 s and −41 dB at 3.25 s, each < 0.3 s) |

**Text and the safe box (65,288)–(888,1248):** OBSERVED from frames (±5 px). The "PG OWNER" HUD text starts at about x 72, y 295 — inside, with 7 px to spare at the top. The RentOk badge's right edge sits at about x 888 — on the boundary. The cheat-code box spans about x 105–849. Labels (COMPLAINTS, GAME OVER?, POWER UP!, TENANT VERIFICATION, ✓ DIGITAL KYC, COLLECTING RENT) and the box text all sit inside. Same layout in all four clips (`composites/hud-all.jpg`).

**Lettering that is not clean composed text:** none found. Clip-1's broken wall, smoke and paper carry no pseudo-writing (`composites/c1-wall-zoom.jpg`); the phone in his hand shows a plain glowing screen. The paper stacks in clips 2–4 are blank. The only small text is "RentOk / India's renting superapp" inside the badge and a tiny "RentOk" on the floating phone icon.

**Anything resembling a Nintendo asset:** no characters, blocks, coins, pipes or mushrooms. Two generic motifs to note for the checker: a floating "?" glyph over the paper stack in clips 2–4 (a plain question mark, not a block), and a segmented hearts/health bar. Neither looks like a Nintendo drawing to me.

**On-screen or audible claims:** the badge tagline "India's renting superapp" appears in every frame of every clip — a positioning claim, not a guarantee, but it should be on the permitted-string list. On-screen strings observed: PG OWNER · COMPLAINTS · GAME OVER? · CHEAT CODE: INSTALL RENTOK APP (typed letter by letter) · POWER UP! · TENANT VERIFICATION · ✓ DIGITAL KYC · COLLECTING RENT (clip-2 only). Audible claims: no speech-like pattern appears in any spectrogram (speech shows as sweeping stacks of harmonics over 100–300 ms syllables; none of the three distinct tracks has this — they show steady tones, regular pulses, chirp sweeps and broadband bursts). The speech-band (300–3400 Hz) level sits within 1 dB of the full-band level in clip-2/3 at 1.75–3.75 s and in clip-4 at 1.75–3.0 s; that is the typing-pulse section and is consistent with square-wave beeps, not voice, but **a human should listen to those two stretches to be sure**.

---

## Part (iv) — Observations that might identify a production method

Written after the scores above; the scores were not changed after writing this section.

1. **Clips 2 and 3 carry byte-identical audio** (same decoded MD5 at 16 kHz mono; identical loudness, peak and noise-floor figures to the last decimal). Clip-4's spectrogram shows the same effect set — the same regular typing pulses at ~1.6 kHz and ~4.8 kHz, the same rising arpeggio, the same down-sweeps — but with gaps and without the continuous bed. INFERRED: clips 2, 3 and 4 share one sound-generation method with different mixes; clip-1's audio is unrelated (broadband, no chip-tune pulses, a tonal low bed at the start).
2. **Clips 2, 3 and 4 share one timing skeleton** (box slides up at 1.0–1.5 s, flash at 3.6–3.7 s, POWER UP 4.0–5.2 s, wall 5.9–6.7 s), the same HUD, the same cheat box, the same label styling, the same crisp sprite-swap animation (a handful of fixed poses, linear movement, a floating phone icon, a slice-and-fade wall). Clip-3 and clip-4 share a backdrop; clip-2 has a different, richer backdrop; clip-4 has a larger pose set (knock-back, kneel, look-up, hold-phone, wind-up, throw). INFERRED: the same code-driven compositor with different assets and, in clip-4, more poses.
3. **Clip-1 looks generated by a video model with the HUD composited on top.** Evidence OBSERVED: the character deforms continuously rather than swapping poses; the complaint bubbles melt into a smear at the hit and re-form crisp afterwards; smoke, fire and paper have soft, photographic-looking texture; background water tanks appear at the end; the picture is soft while the HUD, labels and cheat box are pixel-sharp and identical to the other clips'. The cheat box in clip-1 also has its own timing (types from 1.5 s, clears at 2.6 s) unlike the shared skeleton.
4. **What I was told before scoring:** the packet README says two clips have code-made sound and one keeps a video model's own soundtrack, and the contract §2 names "AI stills + code animation" and a "video-model prompt" as production kinds. So I knew such categories existed. I did not know which clip was which; the identification above is my inference from the media. Whether that foreknowledge coloured the scores is for the reader to judge — the scores were written against the anchors with frame references before this section.
5. Container metadata was stripped to generic ffmpeg tags in all four; nothing in the files identified a treatment.

---

## Part (v) — For the customer, in plain English

Of the four, **clip-1** comes closest to a modern, polished platform-game beat, because it is the only one where the power you install actually *does* something you can see and feel: the owner gets knocked to his knees, a phone drops into his hand as the cheat code types, he lights up, and then he fires a beam that smashes the paperwork wall into flying sheets and smoke while his life bar refills. That is the sequence a player would want to repeat. What it still lacks is finish: the owner is drawn soft and slightly wobbly, the complaint bubbles smear into a red blob at the moment of impact, and the completed cheat code "INSTALL RENTOK APP" is visible for one thirtieth of a second — a viewer never gets to read it. **Clip-4** is the cleanest drawing and the only other clip where the owner visibly reacts (thrown backwards, kneeling, looking up at the code, winding up a throw), but its "power" is a projectile the size of a fingernail and the wall fades away rather than breaking, so the payoff feels like a label rather than a win. The single most visible difference between the strongest and weakest clip is this: in clip-1 the owner fires a beam and the wall explodes; in clip-3 the owner stands still, a flash happens, and a small paper stack quietly fades out while he jogs on the spot.

---

## Appendix — audio measurements used

Levels are RMS per 0.25 s window, full band vs. 300–3400 Hz speech band, from the decoded track (16 kHz mono).

- clip-1: quiet start (−32 dB) → hit at 1.0 s (−17) → typing ticks (−23 to −34) → power-up at 3.0 s (−13.5) → quietest at 4.75 s (−33) → wall strike at 5.0–5.5 s (−7.6, the loudest moment in the packet) → decay to −39 at the end. Speech band stays 5–10 dB below full band throughout (broadband effects, not voice).
- clip-2 = clip-3: −15 dB at the start, dip to −31 at 1.5 s, steady −12 to −18 through the typing (speech band within 1 dB of full band — square-wave beeps), −32 at 5.0 s, −17 to −22 to the end.
- clip-4: −12 to −15 at the knock-down, near-silence at 1.5 s (−44), −18 during the typing, near-silence at 3.25 s (−41), −18 at the flash, −25 to −37 through the power section, −16 to −24 at the throw and hit.

Spectrograms: `evaluation/frames/audio/spectrogram-clip-{1,2,4}.jpg` (clip-3's is identical to clip-2's).
