# AGENT 12 — Craft Jury: verdicts on the actual media (cases 001, 002, 003)

Read-only. All media were extracted with `git show <ref>:<path>` (Cumin: de1f978; Upwork intro: work/pilot-upwork-intro-video-v4 @ f6ca66f) or read from disk (UPM = upwork-portfolio-media, non-git; UPT = upwork-portfolio-tiles @ f236c54). Frames were sampled with ffmpeg at 0 s, 1 s, 2 s, then every 2 s (plus targeted key frames) and LOOKED AT with the Read tool; audio was measured with ffprobe / silencedetect / astats / ebur128 and by re-running the job's own ffmpeg VO chain on the committed VO files. No provider was called, nothing was spent, nothing inside any repo was modified. Working files: `scratchpad/jury/{cumin,intro,portfolio}/`.

Labels: OBSERVED = seen in frames or measured; INFERENCE = derived from timeline/script files or re-derivation; HYPOTHESIS; UNKNOWN. Listening was not possible; every voice judgement is INFERENCE from the transcripts, the VO files' measured timing, and the human's recorded ear.

---

## 0. Artifacts judged (path + sha256)

### Case 003 — Cumin Co. chopsticks film (`de1f978`, `agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/`)

| Artifact | sha256 | Probe |
|---|---|---|
| gen/final/cuminco-chopsticks-9x16.mp4 (V1) | 097e428e5929f1bd10d71bc68479dcbe6e011803629b198b616858e17b205d9d | 1080x1920 24 fps 23.50 s, aac 48 k stereo |
| gen/final/cuminco-chopsticks-4x5.mp4 (V1) | 02a121d9cbc396e158507f8c5b6ccea7aa63cdbd07191c09bdfab0a76804e996 | 1080x1350 23.50 s |
| gen/final/cuminco-chopsticks-1x1.mp4 (V1) | d2b0673698827a760c58e1183dab28192c2054ad4a2f54a342b5ba15e67a9f47 | 1080x1080 23.50 s |
| gen/final/v2/cuminco-chopsticks-9x16.mp4 | adaeaa37e4c647a9ac24e986d8124ca6f86265172d23194019333db437693f8a | 22.875 s |
| gen/final/v2/cuminco-chopsticks-9x16-nomusic.mp4 | 28ea1d7b396e90779cdcf139f0fb5ae659a6e32341a3a24d0a6248d07dd00a4c | 22.875 s |
| gen/final/v2/cuminco-chopsticks-4x5.mp4 | a4ed805602e5d4b35c8721e66a22292b88413f8d093ce966ac3b0cde15c8e34a | 22.79 s |
| gen/final/v2/cuminco-chopsticks-1x1.mp4 | 4c9a4f2d95bd01986421d0832b03a7ae7fad3f54e93bf8383cd607dfbff39bb8 | 22.875 s |
| gen/final/v3/cuminco-chopsticks-9x16.mp4 | 85d7410e8bc52717b4630944a5c3664cddf54ba776d43a689cfa9e9e766e67ae | 25.583 s |
| gen/final/v3/cuminco-chopsticks-9x16-nomusic.mp4 | 199e8eb1e9169c18d1c08b023f680e9ab435c551bd3571957ec8f0f8533ff851 | 25.583 s |
| gen/final/v3/cuminco-chopsticks-4x5.mp4 | f2252fd0e2f0fd3be33d1d66bcc46e028178677774cf1f399010732630eea797 | 25.583 s |
| gen/final/v3/cuminco-chopsticks-1x1.mp4 | 6b19bc1a020b471e150d7fb7f2251619e2dbb8723ab1aac963c0c54bd27efc20 | 25.583 s |
| gen/clips/clip-1-r1.mp4 / clip-1-r2.mp4 | 09cbbf70770ff217978234edb3357629a27d5b0c8d74843d5b7fe9f7388c22ed / 6ebc713d7fbc5add33f2a914d56452b52e3c03437b081d80858835e546bb41f7 | 720x1280 24 fps 6.0 s, no audio |
| gen/clips/clip-2-r1.mp4 (= clip-2-accepted, same blob) | 706aa3cf445ac44c005da79673a4347fe4027567a7eba33e2a6e6cbe22a90ff5 | 6.0 s |
| gen/clips/clip-3-r1.mp4 / clip-4-r1.mp4 | a8b72333766cf56a5708a544ab4ece78a077c1cf011e89d7437cad259e9cecfc / 371f26d58edaecd7642b68e75ccf678585abc5c265e52d8580937f27354d0d06 | 6.0 s |
| gen/clips/clip-5-r1.mp4 / clip-5-r2.mp4 | cc11d9f63b28a7e73ad37d5dca9a3312e5a79d7f0b9be0f2e6c5fa90618e6007 / bb85d928a0c35959527106710dbd860282b063ce376b24fc7950459989b67ce2 | 6.0 s |
| gen/plates/plate-A-r1.png / plate-A-accepted.png | 4f1bfc20c16c94f4f1d348b6ca343cf79f10e8fa945e712196ff06456e32f025 / 9f4d17c39753d2d2efbdab0bc4c16c9576743f0cdf50848db2e1b2110790536e | 768x1376 |
| gen/plates/plate-B-accepted.png | c5c39a2db8a9b2b58616f448b21bc286a17eaeb29e1372fcce6f417eff6292a4 | |
| gen/plates/plate-H1-r1.png / plate-H1-accepted.png | ceddf47d01f44fef69875123a65b1f89cfc7e097ba0eae51d5bddb1613b7b446 / dcd267915401d9e384051c1ad3a6fe6e108f08cdca76f26a049e94725427edf1 | |
| gen/plates/plate-H2-accepted.png / plate-H3-accepted.png | 8b4f2776cbd000f2aa12f48e7cd2f35b149edc398b31beee1f94e1601fcaca63 / 234aeb9c0bd7154f70147565dc72b57f952062f70cbae92e172f890fcdcf87c7 | |
| gen/vo/final-b1..b6.wav | 6f0b7f56…, 18f8c3c0…, 2917d1ef…, 60dfb3a5…, f479ce69…, 2b3f0600… (full: 6f0b7f56ffd435582b5a512fddfee019033d819e3c031334fed9d5083ac5c488, 18f8c3c053ede567ba6d756e273f2ea7df68c5854d774f2e725989477ac2ed9c, 2917d1efae083d576747099fae0f2a0508c757b2fe20f81950a10b6e8233141c, 60dfb3a52f9de2398a5d57b0f7123148d1b3ab17d3f2b9ee5e5742993b29c170, f479ce6968451254c3e1814d621d848d890da7c1f02c5d8147142aee8cce188a, 2b3f06009084300f386ceb45f25dad14356d4160f30238b0e01a1512193b7549) | raw 6.48 / 5.16 / 5.24 / 4.88 / 5.36 / 5.76 s |
| gen/music/bed-r1.wav | d76e85ebde91e24a9e432cc79eb0b49f9953e93225ad9d517459a2113a6f809a | 32.77 s |
| qa/clips-1-5-r2-faces.png, qa/clip-2-r1-hand-zoom.png, qa/final-4x5-1x1-samples.png | 455cad011ecf6ae89a7e7974a1a2d28b4db66e4a9e11952f0478380bdedcffeb, d33ea5009c7a0905f0cfbcd49f50a8b08f43e7b71c2d9d56b2998811a8ca0a95, 341e0876ee56ee157c4b95d4365ad365828597e131d8760e6a6e80c52ab95b43 | |

Conflict noted (OBSERVED): `JOB.yaml versions[V1].assets` records the V1 9:16 file as `0fa7df99…`, while the same file's QA row in JOB.yaml and the committed blob both hash to `097e428e…`. Either the versions entry is a transcription error or the file the human saw is not the committed one. UNKNOWN which.

### Case 001 — Upwork intro film (branch work/pilot-upwork-intro-video-v4 @ f6ca66f, `pilots/upwork-intro-video-2026-09-14/`)

| Artifact | sha256 | Probe |
|---|---|---|
| v4/assembly/v4.1/upwork-intro-v4.1.mp4 (ACCEPTED) | d1a5edf8836936eb7e27cec4350f4cce6f21f1d966778f7241544a2ad07e008a | 1920x1080 30 fps 57.13 s; I −14.9 LUFS, LRA 5.2 |
| v4/assembly/v4/upwork-intro-v4.mp4 | 09ed32c54d601f68bd31733dfc1749326d89c9e40a43ba89fc0e6a14d60a29fc | 55.30 s |
| v3/assembly/v3/upwork-intro-v3.mp4 | ea81264d4103faa346b8937b50da4f785d5351f08aefc1e9bceb8d5df0052e51 | 59.87 s |
| assembly/v2/upwork-intro-v2.mp4 | bdd4566eee1b494e802b055a212e6026c664761dad243f43fa01eb37d34915d5 | 59.13 s 24 fps |
| assembly/v1/upwork-intro-first-pass.mp4 | c073e9ab0cf67f5754be0fba6505483d375ea314353e4d691e31e468fda8f4bd | 56.33 s 24 fps |
| v4/gen/speaker/veo-r3.mp4 (speaker take) / still-accepted.png | 72a16bd735372f33a19eb73e35d42bbf76ad345de6c4f7815ef84fe5882f6a0a / e85e2ea171d43d9334fd894db9ef00e19256b9b6edc9be288ad35a44a99b51eb | 8.0 s with audio |
| v4/qa/contact-sheet-key-beats.jpg / contact-sheet-2s.jpg | 091f9927eb1152c13c2d7ae54ec855442361b4b9396d5de2302e8960b0c006a1 / 612b0f6cb53a9e575e18eda2084bfe377217f2162dc5a1a4da64faac3cc977eb | |

### Case 002 — Upwork portfolio (UPM on disk; UPT @ f236c54)

| Artifact | sha256 |
|---|---|
| UPM tile-01-aarohi-skin/aarohi-offer-cta-4x5.png | 3b1fc474236b0e32659b3fb2a4424013524d3370ce0c81e3d936bf3d90b07b57 |
| UPM tile-01-aarohi-skin/aarohi-offer-in-motion-9x16-11s.mp4 | 2b3de9fc3f5bcad45667c13da9ba11170d69ecf07d3431771bbd86756fe69cca |
| UPM tile-02-six-hooks-aarohi/hook-1-cta-4x5.png / hindi-offer-4x5.png | 372aa13e1a396af0b924dbd3c8fe4755959c64d8348441c80b6f9db2cc907264 / c99ff9379346d7bd523d83e1cfb553341227df508136bcb905a4e0e2aa0cc0c0 |
| UPM tile-03-kora-threads/kora-hook-1-16x9.png / kora-hook-1-1x1.png | 479e208481d16cc03713177a7519f80b513928c3a67eda3ec59bb88766e377ab / d6a09e2e501a5039bc66875789268fb703c63e5c767521d1c133d62327d5a536 |
| UPM tile-04-ironleaf-nutrition/ironleaf-offer-4x5.png | 333ebeb6704bb9b66fd331a8de773ad2a3bf1a105458e41cd913b302883b921f |
| UPM tile-05-dhaba-47-hindi/dhaba47-hindi-4x5.png / -1x1.png | 92aab4f11b4e9c7cf3d21e5e4e8973f2a3b80b49ae63e78c0e96a3e0757cb5f5 / 69c230cdcef4e1429946b48a03ff0dce6f7e08b6def5805ae597e46db31260a8 |
| UPM tile-06-gyaanbox-edtech/gyaanbox-offer-1x1.png / gyaanbox-offer-in-motion-9x16-12s.mp4 | c3a71b095947fcb4f5d0fb1027b4907c1d88e2b42574924b8c7d133c6e554984 / 517ab55298c85a9a5f77cc569422267cfc625e8bff9eb10eda3c76ecf69853ce |
| UPM tile-03-brewa-kettle/brewa-scene-1-kitchen-16x9.png | 1e9f7281b7fa54d680a90d1038f6c2ec4b6140456a1e1398dbde0ad7f994b433 |
| UPM tile-10-two-speaker-hindi/two-speaker-hindi-veo-3.1-fast-r1.mp4 | 1eddf1d551338666d416a1ffacabb236d7e26811c8d1b7631e684b55a5bc887f |
| UPM _rejected/tile-07-nivaas-homes-REJECTED-2026-09-15/nivaas-story-9x16-15s.mp4 | d501c1fb4f82fc17f440ca284e35beac5723a868d3f92590261adddd6decfa14 |
| UPT tile-01-aarohi-skin/cover-5x4.png | b6187886521e36b0b7cad9733feadc6a1baf94087525f7b675afea9283e2ddd6 |
| UPT tile-08-kora-threads/board-four-sizes.png | 7fdfca60abed9271b79d31f160c5fb5b4b0ef4c293d83c9a1e7def77f1943789 |
| UPT tile-04-dhaba-47-hindi/board-detail-hindi-panel.png | 0c557c5ae62056a28086301884d7fc20ac22178f2a57f31227a0f3cc05248ec7 |

Also viewed as mosaics: every accepted static in tiles 01/02/03-kora/03-brewa/04/05/06 of UPM, the nine UPT covers, eight UPT boards, and the four `_rejected` Nivaas statics. Media are committed for cases 003 and 001 (not gitignored); case 002 media live only on disk (UPM is non-git; UPT is a local git repo).

---

## 1. CASE 003 — Cumin Co. "Bottom stick, still." (V1 → V2 → V3, all REJECTED by the human)

### 1.1 What is actually on screen (OBSERVED, V3 9:16 master, 25.6 s)

| Master t | Beat | Frame content | Copy |
|---|---|---|---|
| 0.0–3.0 | 1 (clip-1-r2 3.0–6.0) | Static two-shot: she lifts noodles from her pink bowl toward her mouth; he holds one chopstick in a fist over his mint bowl; both look down. Nobody fumbles, no noodle escapes. Brand mark "Cumin Co." absent at t=0.0, fades in by 0.3 s, top-RIGHT (box x 823–984) although compose.py's comment says top-left. | none |
| 3.0–8.5 | 2 (clip-2) | Macro, her hand holds both sticks over the pink bowl; sticks cross at the tips; 5.5 s in which essentially nothing moves. | "1 / The bottom stick stays still." top-left, wall |
| 8.5–13.5 | 3 (clip-3 0.5–5.5) | Her hand lifts a bundle of noodles high, drops; hand exits frame with a blurred sleeve at the very end of the clip (5.9 s; cut before it). | "2 / The top stick does all the work." |
| 13.5–17.5 | 4 (clip-4 0.0–4.0) | His hand, mint bowl: a single noodle strand lifts, sticks go progressively vertical into the bowl (the "standing chopsticks" the brief forbids is reached at clip t≈5 s, cut at 4.0; at 3–4 s the sticks are already stabbing downward). | "3 / Pinch and release." |
| 17.5–21.0 | 5 (clip-5-r2 1.0–4.5) | Two-shot: she laughs with her mouth WIDE open from 17.5 to ≈18.8 s (frames at 17.6/18.0/18.4/18.8 verified) under the VO line "It takes a few tries…"; he eats with a wooden SPOON; her chopsticks lie across the rim, his on the table — not in the rim notch. | none |
| 21.0–25.6 | 6 end card | Cream ground; stacked type "Ramen night at home. / 15 cm Ceramic Ramen Bowl / Cumin Co. / cuminco.com" above the brand's lifestyle photograph (different bowl finish with the embossed "cumin co." mark, different kitchen, stir-fried noodles not ramen), slow zoompan; bottom ≈25 % of the 9:16 frame empty. | four lines |

### 1.2 Audio (measured)

- V3 VO chain re-run on the committed files (edge trim −50 dB, atempo 1.10): b1 5.32 s, b2 4.12, b3 3.99, b4 3.56, b5 3.98, b6 4.54. With the hand-set starts 0.3 / 4.7 / 9.1 / 13.6 / 17.7 / 22.0: **b1 ends 5.62 → overlaps b2 by 0.92 s; b6 ends 26.54 → overruns the 25.6-s film by 0.94 s.** Matches DF-08 exactly. Confirmed independently on `v3/…-9x16-nomusic.mp4`: speech is continuous from 3.49 s to 8.81 s (no gap between b1 and b2) and the last silence starts at 25.21 s (b6 is cut off by `-shortest`).
- **V1 had the same class of defect and it was never diagnosed (INFERENCE, re-derivation):** V1 chain (internal silenceremove −45 dB + atempo 1.05) gives b1 = 4.33 s from 0.3 → ends 4.63 s, b2 starts 4.0 → **0.63 s overlap in V1 as well**. DF-02 attributes V1's "random audio" only to internal-silence removal and loudnorm pumping. V2 hid the overlap only because b1 was dropped; V3 restored b1 with the same hand-set start table and the overlap returned. The per-second RMS of the V1 mix swings between −14 and −37 dB (V3: −13 to −32 with a smoother contour), consistent with the pumping DF-02 describes.
- Music bed: −30 LUFS, side-chain 4:1 (declared). Not audible to me; the V3 loudness contour shows no −35 dB holes, so the ducking is at least not pumping as V1 did.
- Voice character (INFERENCE from ATTEMPTS.jsonl att-043…051): Gemini TTS "Leda", directed as "bubbly, bright, high-energy happiness held at a soft volume". The brief asked for "a very calm empathetic voice". The direction text contradicts the brief's register; the human never rejected on voice character in this job, but never accepted it either.

### 1.3 Persona verdicts — Cumin V3 (the last presented) with V1/V2 deltas

| Persona | Verdict | Single most important reason |
|---|---|---|
| Cold Viewer (Reels, sound on or off) | REJECT | First 1–3 s is a still-ish two-shot of two people looking down at bowls; the promised hook ("a noodle slips back into the bowl in the first second") is not in the picture. Nothing invites a second second. V1's first frame is worse: the man slurping with a puckered grimace (OBSERVED `sheets/v1-t0-faces.png`). |
| Target customer (urban Indian young adult) | ACCEPT-WITH-FIXES | Warm, aspirational, product-adjacent; but "how to hold chopsticks" is read as instruction, and the demonstration is not clearer than the blog it came from. |
| Distracted mobile viewer (muted) | ACCEPT-WITH-FIXES | Muted test genuinely passes: three step lines + macro hands read without sound. But beat 2 is 5.5 s of a hand not moving — dead time on a feed. |
| Persuasion / attention specialist | REJECT | Attention order is text → hand → bowl; the bowl is never the object of a cue. There is no moment engineered to make the viewer want the bowl. |
| Communication strategist | REJECT (V1/V2), ACCEPT-WITH-FIXES (V3) | V1/V2 have no proposition, no brand early, no end. V3 adds mark + end card + spoken close, but the end card is a slide, not a payoff. |
| Advertising strategist | REJECT | Is it an ad? V3 yes, formally (brand early, product end card, Direction "cuminco.com"). Proposition: none stated — "Ramen night at home" is a mood, not a reason. Hook → proposition → proof → payoff → action: hook missing, proposition missing, proof = grip demo (of chopsticks, not the bowl), payoff = laugh + spoon, action = URL. **Product Storytelling test: FAILS.** Replace the Kairi/Rosé bowls with any plain pastel bowl and nothing in the story changes; the one product argument the blueprint named (chopsticks resting in the rim notch) is not in any frame (`sheets/v3-t20-notch.png`: sticks lie across the rim / on the table). |
| Direct-response specialist | REJECT | No offer, no reason to click, URL only in the last 4.6 s in 38-px type. Acceptable for a spec film; unacceptable as "an ad". |
| Copywriter | ACCEPT-WITH-FIXES | Hook line (none), headlines (three verbatim blog fragments — good, distinct jobs), proof (none in words), brand line, CTA (URL): the deck has no hook and no proposition line. VO "Pinch… and… nearly." is the best line and it is buried under a mouth-open laugh. |
| Brand strategist | ACCEPT-WITH-FIXES | Register (warm, unhurried, oat/mint/rosé) is right for the brand; the end card's brand photo breaks the film's own world (different bowl finish, different kitchen, different dish). |
| Product storytelling director | REJECT | Product is scenery; feature (rim notch) not shown; embossed mark hidden by design (turned away) in every generated frame, visible only in the borrowed photograph. |
| Story / narrative designer | REJECT | The brief's story (he fumbles → she shows → he fails → they eat anyway) is not on screen: beat 1 shows HER eating, beat 4 shows a single strand lifted cleanly, beat 5 shows him eating with a spoon (which reads as "gave up", but the failure it pays off never happened). |
| Indian-market creative specialist | ACCEPT-WITH-FIXES | Casting, wardrobe, table are plausible urban-Indian; Indian-English VO direction is right; "bubbly/high-energy" direction is wrong for "calm, empathetic"; a Hindi/Hinglish option was tested (mq-hi-*) and dropped without a recorded reason. |
| Art director / graphic designer | ACCEPT (9:16) / REJECT (4:5, 1:1) | 9:16: copy sits on wall, hierarchy numeral→line→mark is clean, Charter + Avenir Next pairing is tasteful. 4:5 and 1:1: every step line is on an opaque card that overlaps the chopsticks and the hand (`sheets/v3-4x5-t5.png`, `sheets/v3-1x1.png` t=4–6), i.e. exactly the V1 complaint "the text is coming on figures", now with a card. The brand mark is omitted in beats 2–4 (4:5) and 1–5 (1:1) so "early and throughout" is false in two of three deliverables. |
| Typography specialist | ACCEPT-WITH-FIXES | Line breaks fine; end-card stack has four sizes/two faces/two colours in 300 px — over-articulated; numerals at 44 px are near-invisible on mobile. |
| Compositor | ACCEPT-WITH-FIXES | Gates did their job (0 clipping, contrast on pixels, exact strings byte-checked). But the mark fades in over 0.35 s so frame 0 has no mark; comment says top-left, render is top-right — the code and its narration disagree. |
| Product photographer | ACCEPT-WITH-FIXES | Bowl reproduction from the packshot is good (shape, ridges, glaze); the embossed mark is deliberately hidden after plate-A-r1 garbled it ("cumin ca."), so the product is identifiable only by colour. Plate-H1-r1 had pale generic chopsticks (rejected correctly; r2 dark acacia). |
| Cinematographer | ACCEPT-WITH-FIXES | One soft window key, consistent oat/wood palette, matched two-shots. Macro inserts are static locked-off; nothing motivates the cut from two-shot to macro (no look, no hand entering). |
| Editor | REJECT | Cuts are on VO starts, not on action; beat 2 is 5.5 s of stillness; beat 5 cuts in on an open-mouth laugh; end card is a 4.6-s hold on a still. Total 25.6 s vs the 18-s plan — 42 % over. |
| Motion designer | ACCEPT-WITH-FIXES | Alpha fades 0.35 s in / 0.3 s out are fine; end-card zoompan 1.00→1.04 reads as a slideshow. |
| Storyboard artist | REJECT (process) | No storyboard exists as an artifact. The blueprint text ("first_read", "attention_order") is a storyboard in prose; five of the seven story defects below would have been visible on a six-panel board drawn from the accepted plates before any clip was generated. |
| Film director | REJECT | The film has no event. The one directable moment (the miss) was never staged; the i2v prompts ask for "one cue" per macro but the model returned clean lifts. |
| Voice / casting director | ACCEPT-WITH-FIXES (INFERENCE) | Casting a young Indian woman "explaining something she loves" is right; direction "bubbly, high-energy" contradicts the brief's "calm, empathetic". |
| Dialogue / VO editor | REJECT (measured) | b1→b2 overlap 0.92 s; b6 overrun 0.94 s; same class of overlap existed in V1 (0.63 s) undiagnosed. |
| Music supervisor | ACCEPT-WITH-FIXES (INFERENCE) | Lyria bed at −30 LUFS ducked 4:1 is a sane spec; a no-music variant was shipped, which signals the operator was unsure the bed helped. |
| Sound designer | REJECT (V1), ACCEPT-WITH-FIXES (V3) | V1 mix pumps (−14 → −37 dB per-second RMS); V3 contour steady; no room tone, no foley (chopstick on ceramic would be the one sound that sells the product). |
| Post-production supervisor | REJECT | Individually accepted plates (A, B, H1r2, H2, H3) are all good; the clips generated from them are individually acceptable; the assembly is not, because acceptance happened per asset and never on a timeline: overlap, open mouth under VO, card-over-subject, end-card world mismatch are all assembly-level. |
| Delivery / format | 9:16 ACCEPT-WITH-FIXES; 4:5 REJECT; 1:1 REJECT | 4:5 and 1:1 are declared crops with cards over the subject and no brand mark — the QA JSON flags every one of these as a CF2 deviation "recorded for the human", and they were delivered anyway. |

### 1.4 Comparison with the recorded human verdicts (JOB.yaml versions[])

- V1 "crapy. the video has got some random audio. her lips are omving. the text is coming on figures. all messed up" — **I agree** on all four; I add that the first frame (man slurping, grimace) kills the hook, and that a b1→b2 overlap was already present.
- V2 "did cannon say nothing about product positioning? the closing shot should have cumin product and final caption. it does not look like ad at all. the opening is missing too." — **I agree**, and would go further: the opening is not just missing a brand mark, it is missing the event the brief asked for.
- V3 "this is still bad. the voices are overlapping. not at all happy with it. reject completely." — **I agree** on the overlap (measured); I disagree with the implicit framing in LEARNING-PACKET that DF-08 is a new defect: the VO start table was hand-set from an 18-s plan in V1 and never re-derived after the read came in long; the overlap is a V1 defect that V2 masked.
- MQ1 plate "r2" — **I agree** (H1-r1 chopsticks were pale and generic; r2 dark acacia).
- Where I am harsher than the human: the human never said "this does not tell the story I asked for"; the film would still fail the brief with the audio fixed.

### 1.5 Defect detectability (feeds the human-review-point analysis)

| # | Defect | Where visible | Detectable from a single frame / storyboard before spend? |
|---|---|---|---|
| C1 | No hook event in beat 1 (nobody fumbles; she eats) | plate-A-accepted.png already shows her lifting noodles, him passive | **YES — on the accepted plate**, before clip-1 was generated (twice). |
| C2 | Beat 4 does not show a miss; sticks go vertical (forbidden) | clip-4 frames 3–5 s | On the plate H3: NO (plate is a clean grip). On the first clip contact sheet: YES. Storyboard would have specified the miss. |
| C3 | Rim-notch payoff absent | plate-B-accepted.png: sticks across the rim / on table | **YES — on the accepted plate** (the blueprint's own "proof" image was never drawn). |
| C4 | Mouth open under VO (V1 clip-1/5; V3 beat 5 17.5–18.8 s) | clip frames | Per clip: YES from the contact sheet (qa/clips-1-5-r2-faces.png shows clip-5-r2 mouth open at 1.0/1.5 s — the chosen in-point). Only after assembly: whether it lands under a VO start. |
| C5 | VO overlap / overrun | none — timeline only | Before assembly YES, by arithmetic (start table + trimmed durations) — a VO_SCHEDULE gate, no frames needed. |
| C6 | Cards over chopsticks in 4:5 / 1:1 | one frame per beat per geometry | YES — the QA JSON already flagged it (CF2); it needed a human to read the flag, not a new detector. |
| C7 | End-card world mismatch (borrowed photo ≠ film's bowl/kitchen) | one frame | YES — from the end-card composite alone. |
| C8 | Beat 2 dead time (5.5 s static) | clip-2 contact sheet | YES — seven identical frames on the contact sheet. |
| C9 | Product Storytelling failure (generic bowl would do) | blueprint + plates | YES — from the storyboard/plate set; no clip needed. |
| C10 | Voice register vs brief ("bubbly" vs "calm") | prompt text | YES — from the TTS direction string before generation. |
| C11 | V1 mix pumping | audio only | Only after mix; measurable (per-second RMS) without listening. |
| C12 | Brand mark missing at frame 0 (fade-in) | frame 0 | YES — first frame. |

Eight of twelve were visible on plates, a storyboard, or a prompt string before any clip credit was spent.

---

## 2. CASE 001 — Upwork intro film (V1, V2 specific-repair/rebuild; V3 reject; V4 specific repair; V4.1 ACCEPT)

### 2.1 What is on screen (OBSERVED, v4.1, 57.1 s, 16:9)

0–8.5 s full-frame generated speaker (Veo 3.1 native speech, 0.46–7.40 s: "Everyone can make AI ads now. So the bar went up. You need more creative, faster."); 8.5 s handoff to a 200-px rounded-square speaker bubble; typographic cards "AND IT CAN'T SUCK." / "MORE CREATIVE. FASTER. WITHOUT LOWERING THE BAR."; proof 1 Aarohi 4:5 ad + "GREAT IMAGES AREN'T ENOUGH. THEY HAVE TO WORK AS ADS."; proof 2 the craft ad with HOOK → OFFER → CTA spotlight rings; proof 3 kettle packshot "SAME PRODUCT." → two kitchen scenes "NEW SCENE. Shape. Colour. Details held."; proof 4 "AND THEN IT MOVES." bottle dolly + diya clip; Kora 16:9 2.8 s; proof 5 "ONE DIRECTION. MORE TO TEST." master + 4 formats + 6 hooks + Hindi; speed cards "STANDARD 24 HOURS" / "4-HOUR EXPRESS eligible smaller packs · paid add-on"; CTA "SEND YOUR PRODUCT LINK + OFFER. GET A STRAIGHT PRICE FOR THE FIRST TEST PACK." + Adwisely wordmark + bubble. Audio: one speech span, music from 7.0 s, seven SFX ticks; integrated −14.9 LUFS, TP −1.9, LRA 5.2 (my ebur128 agrees with `audio-measure.json`).

### 2.2 Persona verdicts — v4.1 (accepted)

| Persona | Verdict | Reason |
|---|---|---|
| Cold Viewer (Upwork profile, likely muted autoplay) | ACCEPT-WITH-FIXES | First 3 s: a credible woman looking at me and talking. Muted, there is no super under her for 8.5 s, so a silent viewer gets nothing until "AND IT CAN'T SUCK." at 9.5 s. |
| Target customer (DTC founder browsing Upwork) | ACCEPT | Proposition is legible in 12 s; proof is the actual work at full size; price mechanism ("straight price for a first test pack") is honest. |
| Distracted mobile viewer | ACCEPT-WITH-FIXES | Type-only cards are big enough; the 6-hook grid and the 4-format row are thumbnails that are unreadable at player size (the 6 hooks are ≈120 px tall in a 1080 frame). |
| Persuasion / attention | ACCEPT | Speaker → statement → proof → offer → CTA is the right order; the spotlight beat (HOOK / OFFER / CTA rings) is the strongest 6 s of the film. |
| Communication strategist | ACCEPT | "And it can't suck" is the film's one memorable sentence and it is restored in v4.1 (V4 lost it — human noted). |
| Advertising strategist / Direct-response | ACCEPT-WITH-FIXES | Hook (speaker) → proposition (can't suck / faster) → proof (ads, scenes, motion, range) → payoff (24 h / 4 h) → action (send link). Speed is asserted by type, not demonstrated — known limit recorded in SCRIPT-v4-FROZEN ("Karl's 'speed is asserted, not demonstrated' stands"). |
| Copywriter | ACCEPT | Hook / headline / proof labels / brand line / CTA each do one job; "GET A STRAIGHT PRICE FOR THE FIRST TEST PACK" is good direct-response copy. |
| Brand strategist | ACCEPT-WITH-FIXES | Cream + Helvetica Neue + orange rule is coherent; "Adwisely" wordmark appears once, small, in Didot — the film's identity is its typography more than its name. |
| Product storytelling | ACCEPT | The demonstrated product (an ad set) is the story; substituting a generic asset would change it. Passes. |
| Story / narrative | ACCEPT-WITH-FIXES | Four movements land; the Kora beat (2.8 s) is a non-sequitur insert added to satisfy "creative range" — it reads as a cutaway. |
| Indian-market specialist | ACCEPT | Indian-English speaker, Hindi creative shown (Devanagari correctly shaped in the Aarohi and Dhaba tiles), ₹ prices. |
| Art director / graphic designer | ACCEPT-WITH-FIXES | Consistent 26-px radius, tokens enforced (V3's "square + rounded" mess is gone). Large empty cream fields on the speed cards look like slides, not film. |
| Typography | ACCEPT | Hierarchy consistent; smallest running text is the 32-px legal line; nothing clipped (layout-report gate). |
| Compositor | ACCEPT | Zero clipped text, contrast on real pixels, contain-fit for every creative; the V4 offer/code pill collision (visible in my v4 t=20/22 key frames: "15% OFF FIRST ORDER" and "CODE AAROHI15" side by side over the headline) is fixed in v4.1 (pill below the headline). |
| Product photographer | ACCEPT-WITH-FIXES | Bottle and kettle constant across scenes; the A3 diya clip shows a large orange flame burst beside the serum bottle at ≈36 s (`sheets/v4.1-wide.png` row 6 col 4) that reads as fire, not a lamp. |
| Cinematographer / editor / motion | ACCEPT-WITH-FIXES | Cuts are motivated by new information; holds ≥3 s; the bubble is a good continuity device. The speaker take has one frame family (t≈4 s) with bared teeth/tight jaw that reads slightly synthetic; the human accepted by ear and eye. |
| Voice / casting / VO editor | ACCEPT (INFERENCE) | One 7-s native take, transcript verbatim, pause 0.76 s, ~99 wpm; no VO elsewhere, so no continuity risk. |
| Music supervisor / sound designer | ACCEPT-WITH-FIXES (INFERENCE) | Music enters under the last word; 7 ticks; loudness on target. 48 s of a 57-s film are music-only with reading — acceptable on Upwork, thin as film. |
| Post-production supervisor | ACCEPT | This is the one case where assembly-level QA existed (layout, contrast, crop, frame-scan, audio reports) and the assembled film matches its reports. |
| Delivery / format | ACCEPT | Single 16:9 deliverable; no geometry variants claimed. |

Earlier versions (OBSERVED on frames): V1/V2 — presenter with small white lower-third supers (≈28-px text in a 1080 frame), phone mock-ups, "Glass skin in three weeks" Aarohi ad; V1 t≈40 s shows a ghost-doubled caption from a crossfade; V2 t≈44 s presenter frame is soft/unstable (the "presenter quality degraded later" the human recorded). V3 — no presenter; tiny grey labels ("1/4 FOUR IMAGE DIRECTIONS", "SIX HOOKS" partly hidden behind a card at t≈16 s, "VIDEO AD · 16:9" in muted colour over the diya image at t≈30 s, "HUMAN-CHECKED" over the Dhaba creative at t≈44 s, a faded "…WORLD" ghost at the Kora card's bottom-left at t≈36 s); square and rounded cards mixed; narrated VO (Sarvam, 8 lines, VO-SCRIPT.txt). Every item in the human's V3 list is visible on my frames.

### 2.3 Comparison with HUMAN-VERDICTS.yaml (case 001)

- V1 specific_repair, V2 rebuild_direction, V3 reject, V4 specific_repair, V4.1 accept — **I agree with every step**, and with the V4 feedback in detail (offer/code collision visible at t=20–22 s; "and it can't suck" absent in V4; bubble persists through proofs; Express card is plain type in both V4 and V4.1).
- Where I am stricter: V4.1's Express treatment is still a type card — "strengthened" is a small change; and the diya flame at 36 s should have been a product-context flag.
- Where I am more lenient: the V3 VO — I cannot hear "horribly robotic"; the transcripts passed 16/16, so this is a purely ear-level rejection that no metric in the repo predicts.

### 2.4 Detectability (case 001)

| Defect | Single frame / storyboard? |
|---|---|
| V3 text clipped / colour vanishing / crop / mixed radii | YES — every one is a single-frame defect; the V4 compositor gates (layout, contrast, crop reports) are the codification. |
| V3 robotic voice | NO frame; only ear. No proxy in the repo. |
| V3 pacing too rushed | Timeline arithmetic (beats < 2 s) — YES before render. |
| V4 offer/code pill collision | YES — single frame of the craft ad. |
| V4 lost "and it can't suck" | Script diff — YES before render. |
| Speaker naturalness | Contact sheet catches teeth/jaw frames; final call is ear. |
| Diya flame | YES — clip contact sheet (frames-a3-05s.jpg existed and was passed). |

---

## 3. CASE 002 — Upwork portfolio tiles (B1 specific_repair → B2/B3 accept; Nivaas N1/N2 reject → skipped)

### 3.1 What is on disk (OBSERVED)

Nine accepted tiles: one layout system (photo top, solid panel bottom, pill / Didot or Helvetica headline / code / button / legal / wordmark) applied to Aarohi (serum), IronLeaf (protein), GyaanBox (edtech), Dhaba 47 (Hindi), Kora (editorial split 16:9, panel-under-picture for 1:1/4:5/9:16); Brewa kettle three scenes; presenter takes; two-speaker Hindi clips. The UPT build (covers 1250x1000 cream, Didot headline, tag chips, "Demonstration · invented brand" label) is what was published.

### 3.2 Persona verdicts (the published set)

| Persona | Verdict | Reason |
|---|---|---|
| Cold viewer (Upwork gallery scroll) | ACCEPT | Covers are legible at thumbnail size; one visual system across nine tiles reads as a studio, not a scrapbook. |
| Target customer (DTC brand buying ad sets) | ACCEPT-WITH-FIXES | The pitch is "exact text, four sizes, fast" — demonstrated. Creative range is not: the same amber bottle appears in ~30 of the files; "six hooks" = six headlines on one photo. |
| Advertising strategist | ACCEPT-WITH-FIXES | Every offer tile has hook/offer/code/CTA/legal; Kora and Brewa tiles are not ads (no offer, no CTA) and the README says so honestly. |
| Direct-response | ACCEPT | Pill + code + button + T&Cs on Aarohi, IronLeaf, GyaanBox, Dhaba; the Hindi Aarohi variant has no button (README flags it). |
| Copywriter | ACCEPT-WITH-FIXES | Lines are competent and safe ("YOUR NIGHT ROUTINE, SIMPLIFIED."); Didot all-caps for a protein tub is a category mismatch. |
| Brand strategist | ACCEPT-WITH-FIXES | Five invented brands share one panel system and two fonts — it is Adwisely's system, not five brands; fine for a portfolio, wrong as "custom per brand" proof. |
| Indian-market specialist | ACCEPT | Devanagari shaping correct in every Hindi file I zoomed (आज की दावत, कोड DHABA20, ऑर्डर करें, नियम लागू, पहले ऑर्डर पर); ₹ formatting correct; Hindi CTA button present on Dhaba, absent on Aarohi Hindi. |
| Art director / graphic designer | ACCEPT | B2 files: no text on photo, no edge touch, panel geometry consistent — every one of HD-01…HD-10 is fixed in the files I looked at. |
| Typography | ACCEPT-WITH-FIXES | Kora 16:9 hook lines are ≈24 px on a 1920 frame — too small for a social/hero 16:9; the Kora 9:16 headline is also small relative to the panel. |
| Compositor | ACCEPT-WITH-FIXES | Dhaba 9:16 still crops the dal bowl at the top-right edge (edge crop of a flat-lay is normal, but HD-06 says "dal bowl cut at the right edge — fixed"; it is still cut at the top). IronLeaf packshot sits on a flat band with a visible tonal step against the photo ground in 1:1. |
| Product photographer | ACCEPT | Kettle identical across three scenes and the packshot (the Brewa tile's whole claim, and it holds). |
| Motion | ACCEPT-WITH-FIXES | Aarohi 11-s and GyaanBox 12-s "in motion" clips are three stills crossfaded under a panel whose text builds in; not motion in any ad sense. Text stays exact (their claim). |
| Voice / VO editor (Nivaas, rejected) | REJECT (INFERENCE + measured) | nivaas-story-9x16-15s.mp4: silences 6.63–8.15 s (1.5 s hole mid-narration), 10.16–11.37, 13.16–15.02; 720p soft exterior pan. The human's "voice not continuous, images scrappy" is consistent with the measurement. |
| Post-production supervisor | ACCEPT | Deterministic build (tools/build.py, MANIFEST.json with sha256) — the one case where "what was published" is byte-reproducible. |
| Delivery / format | ACCEPT-WITH-FIXES | Every size variant works independently; Kora 9:16 is the weakest (small type, large empty oxblood). |

### 3.3 Comparison with HUMAN-VERDICTS.yaml (case 002)

- B1 specific_repair (HD-01…HD-10) — I cannot see B1 (not on disk); the B2 files on disk show every flagged defect fixed. **Agree** with B2/B3 implicit accept.
- N1/N2 reject — **agree** (measured hole; soft 720p).
- Controller meta-verdict "you didn't use the pipeline properly" — supported by the fact that the defects HD-01…HD-10 are all single-frame geometry defects a compositor gate would have caught; the operator caught two more (HD-11/12) only while fixing.
- Where I am harsher: "six hooks" and "creative range" — the portfolio shows one photo per brand; a buyer will notice.

### 3.4 Detectability (case 002)

All thirteen human-flagged defects except HD-13 (voice continuity) are single-frame defects (clip, edge touch, text over subject, banner over photo, poor colour combination, shrunken Hindi headline). HD-13a (narration hole) is measurable from the audio track without listening (silencedetect); HD-13b (two voices) is ear-only.

---

## 4. Findings ranked

1. **(Cumin, OBSERVED/measured) The rejected V3's fatal defect — VO overlap — was a V1 defect that the V1 diagnosis missed.** Re-running the committed V1 chain gives b1 = 4.33 s from 0.3 s vs b2 at 4.0 s (0.63-s overlap); DF-02 blames silence removal and loudnorm only. V2 dropped b1, V3 restored it with the same hand-set starts. A start-table + trimmed-duration arithmetic gate (no listening, no frames) would have caught V1, V3 and the b6 overrun. `de1f978:…/tools/compose.py` (V3 lines 63–79), `8a5927a:…/tools/compose.py` (V1 lines 62–70), JOB.yaml DF-02/DF-08.
2. **(Cumin, OBSERVED) The film fails the brief's story on the accepted plates, before any clip was bought.** plate-A-accepted shows her eating, not him fumbling; plate-B-accepted shows sticks across the rim, not in the notch the blueprint calls "the blog's own product argument"; clip-4 shows a clean single-strand lift then vertical sticks (the forbidden etiquette). Product Storytelling test fails: a generic bowl changes nothing. The human never articulated this; the human's V2 verdict ("does not look like an ad") is the symptom.
3. **(Cumin, OBSERVED) 4:5 and 1:1 deliverables reproduce the V1 complaint ("text on figures") as opaque cards over the chopsticks, and the compositor's own QA JSON says so** (nine CF2 deviations in 4x5.qa.json, eleven in 1x1.qa.json, each "recorded for the human"). The flags were written and not read; brand mark omitted in beats 2–4 (4:5) and 1–5 (1:1).
4. **(Cumin, OBSERVED) "Lips moving" survived the r2 repair into V3 beat 5**: clip-5-r2's chosen in-point (1.0 s) is inside an open-mouth laugh that lasts to ≈2.5 s (qa/clips-1-5-r2-faces.png shows it; the compose comment claims "mouth closes at ~1.2 s"), and VO b5 starts 0.2 s after the cut.
5. **(All three cases, OBSERVED)** Of 12 Cumin defects, 8 were visible on a plate, a contact sheet, a prompt string, or by timeline arithmetic before assembly; of the case-001 V3/V4 defects, all but "robotic voice" were single-frame or script-diff; of case-002's 13, 12 were single-frame. The ear-only defects (Sarvam robotic, Nivaas two voices, Cumin voice register) are the residual class no artifact in the repo predicts.
6. **(Case 001, OBSERVED)** v4.1 is the only film of the three where assembly-level QA artifacts exist (layout/contrast/crop/frame-scan/audio reports) and the frames match them. It deserves its accept; residual craft fixes: 8.5 s of silent-viewer blindness before the first super, unreadable thumbnail grids, a slide-like Express card, a diya flame that reads as fire.
7. **(Case 002, OBSERVED)** The published tiles are clean and consistent; the honest weaknesses are creative range (one photo per brand), Kora type size, and "in motion" clips that are crossfaded stills.
8. **(Cumin, OBSERVED) Record inconsistencies:** V1 9:16 hash in `versions[]` (0fa7df99…) ≠ committed/QA hash (097e428e…); compose.py comment says brand mark top-left, render is top-right; comment says beat-5 mouth closes at 1.2 s, frames say ≈2.5 s.
9. **(Cumin, INFERENCE)** TTS direction "bubbly, bright, high-energy" contradicts the brief's "very calm empathetic voice"; no human verdict on voice character was ever recorded (JOB.yaml `human_ear_verdict: null`).
10. **(Cumin, OBSERVED)** No storyboard artifact exists in any of the three jobs; case 001 v4 has the closest thing (CREATIVE-BLUEPRINT-V4 per-beat table) and is the accepted one.

## 5. Open questions / unknowns

- UNKNOWN: whether the V1 file the human watched is the committed blob (hash mismatch in JOB.yaml versions[]).
- UNKNOWN: the audible quality of any VO (Leda, Sarvam, Nivaas) — all voice verdicts here are inference from timing and transcripts.
- UNKNOWN: whether the Cumin human saw the 4:5 / 1:1 files or judged only the 9:16 (verdict text mentions no geometry).
- UNKNOWN: case-002 B1 files (not on disk) — the pre-fix defects are taken from HUMAN-VERDICTS.yaml, not seen.
- HYPOTHESIS: the Cumin story defects were invisible to the operator because acceptance gates were per-asset (plate → clip) and the story was only ever checked as prose; a six-frame board built from the accepted plates would have shown a woman eating, a clean lift, and sticks on the table.
