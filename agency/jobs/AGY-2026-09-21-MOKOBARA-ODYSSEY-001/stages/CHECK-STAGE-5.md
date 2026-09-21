# Independent Stage-5 check — `AGY-2026-09-21-MOKOBARA-ODYSSEY-001`

Checker: a fresh session that wrote none of the job. Scope: the producer's final `gen/final/mokobara-odyssey-9x16-30s.mp4` (sha256 `75d1fc8b…`), the ledgers, the prompts, the fetched brand sources. Spend: USD 0 (ffprobe/ffmpeg/python only, no model calls). No producer file was edited. Cited frames: `qa/checker/` (11 frames at 2 fps + one product-comparison sheet; all other extracted frames deleted for disk).

Timing note: the customer's own verdict (`HUMAN-VERDICT-V1.md`, 18:14Z) landed while this check was running. This check was made without it and is recorded as an independent read; §8 cross-references the two.

**Verdict: DELIVERABLE WITH DEFECTS** for presentation as a first pass. Details in §7.

Labels used below: OBSERVED = measured or seen in a cited frame; INFERRED = my reading of what was observed; CANNOT_DETERMINE = needs a human ear/eye or evidence that does not exist.

---

## 1. Re-measurement of the file and the money (all OBSERVED by code)

| Check | Producer claims | Re-measured | Result |
|---|---|---|---|
| Duration | 30.021 s | **30.021 s**, 720 video frames at 24 fps | PASS (29.5–30.5) |
| Geometry / codec | 1080×1920 H.264 High yuv420p 24 fps | same; SAR 1:1 | PASS |
| Audio | AAC-LC 48 kHz stereo 196 kbps | same, 195.6 kbps | PASS |
| sha256 vs `JOB.yaml` | `75d1fc8b…` | `75d1fc8b2d59368b7358017c342aaca183e1943e8cc27f6aec43e9bc572cf6a2` | PASS (identical) |
| Edit lists (box walk of `moov/trak/edts/elst`) | 0 | **0 `elst` boxes**; top-level order `ftyp, moov, free, mdat` (moov first) | PASS |
| Loudness / true peak (ebur128) | I = −13.3 LUFS, TP = −4.1 | **I = −13.3 LUFS, LRA 3.2 LU, TP = −4.1 dBTP** | PASS (−14 ± 1, TP ≤ −1) |
| Silence (−50 dB, ≥ 0.5 s) | — | none | PASS |
| Per-beat loudness | — | 0–3.5 s −15.6 · 3.5–7.5 −13.7 · 7.5–12.5 −13.6 · 12.5–20.5 −12.7 · 20.5–24.5 −12.0 · 24.5–28 −13.1 · end card −17.6 LUFS | level-safe; the film gets ~3 LU louder through the gag and packing, then drops on the end card — a sensible curve |
| Scene cuts (scdet) | cuts at 3.5 / 7.5 / 12.5 / 20.5 / 24.5 | exactly those five, **plus one at 1.54 s inside beat 1** (see §4) | the extra cut is in-model, not an assembly error |
| Black frames / freezes | — | no black frames; one freeze from 28.0 s = the static end card (expected) | PASS |
| End card in the file = composed `endcard.png` | strings byte-exact | frame at 29.0 s vs `gen/overlays/endcard.png`: PSNR 44.5 dB (compression-only difference) | PASS — the byte-exact strings reached the video |
| Wordmark = the site's asset | sha256 `c443658f…` | `source/mokobara/wordmark-white.svg` re-hashed = `c443658f…`; fetched from `mokobara.com/cdn/shop/files/Mokobara_SVG_White_Logo.svg` per `FETCH-LOG.txt`; **fresh rsvg-convert of that SVG is pixel-identical (PSNR ∞) to `gen/overlays/wordmark-600.png`** | PASS — never redrawn |
| Fetched sources | 13 files hashed | 13/13 match `SHA256SUMS.txt` (the file lists itself, which cannot match — not a defect) | PASS |

**Ledger** (`gen/LEDGER.jsonl`, 36 lines; `gen/ATTEMPTS.jsonl`, 18 lines):

- 18 attempts, each with a *reserve* line strictly before its *settle* line (timestamps checked): PASS.
- Sum reserved **USD 5.389**, cumulative column re-added line by line with no drift, cap 12.00, remaining 6.611: PASS (producer's 5.389 confirmed).
- Failures counted: exactly one non-ok settle, att-014 `http_500` (Lyria: "Could not generate audio… different prompt"), charged 0.06: PASS. The re-send att-015 used a neutral wording (`music-v2.txt`) — one recorded change.
- ATTEMPTS ↔ LEDGER: same 18 ids, same USD per attempt; **every artifact sha256 in ATTEMPTS re-hashed from disk and matched (17/17; att-014 has no artifact, correct)**: PASS.
- Every prompt file in `gen/prompts/*.txt` appears verbatim inside the sent prompt in ATTEMPTS; both negative-prompt files appear verbatim in the sent `negativePrompt` parameter (the beat-1 take-2 variant only on att-016): PASS.

**IP / claim grep of every prompt actually sent (prompt + parameters, 18 attempts) and every prompt file:** searched for Odysseus, Odyssey, Ulysses, Penelope, Telemachus, Ithaca, Calypso, Homer, Nolan, Universal, Cast Away/Castaway, Wilson, Hanks, FedEx, Crusoe, Damon, Zendaya, Lupita, Holland, Pattinson, Hathaway, Theron, Bardem, Fiennes, Chuck Noland, volleyball, Life of Pi, Survivor, The Martian, Blue Lagoon — **zero hits**. Claim words (indestructible, waterproof, water-resistant, lifetime, guarantee, warranty, best-selling, #1, TSA, airline, durable, survive, premium, luxury) — zero hits; the only match was "strongest colours" in `b5-still.txt`, which is about colour, not the product. Every clip prompt carries "no lettering, no logo" and the negative prompt includes `brand name, logo, watermark, text`. The product photos were sent only as *reference images* (their sha256 recorded per attempt) and do not appear in the film. PASS.

Two OBSERVED facts the producer did not state in Stage 5: the six Veo clips are **720×1280** and were upscaled to 1080×1920 at assembly — this is the main source of the "soft" look, not a stitch error; and per `gen/assemble-report.json` the trims are 3.5 / 4.0 / 5.0 / 8.0 / 4.0 / 3.5 s — beats 1 and 6 use 3.5 s of their 4-s clips, beat 3 uses 5 of 6, beat 5 uses 4 of 6, beat 4 uses all 8.

---

## 2. Customer requirements (from the frozen brief; frames in `qa/checker/`)

| # | The customer's words | Result | What I saw |
|---|---|---|---|
| R1 | "the proatagonist had mokbara bags" — reads as **his** bag | **PASS (INFERRED)** | 3.5–7.5 s the navy bag lies half-buried at the tideline; he crouches, hands on it (`f012-05.5s`). Nothing in beat 2 alone says it is *his* rather than *a* bag; what makes it his is the wife's photo inside at 8.0 s (`f017-08.0s`). The ownership reads through beats 2+3 together, not beat 2 alone. |
| R2 | found it "on the island where he was kept for years" | **PASS on "years"; "kept" not shown** | Years: OBSERVED — a rock face covered in hundreds of tally marks with a hand scratching one more (`f003-01.0s`), long grey-streaked hair and beard, torn clothes. "Kept" (held by someone) is not depicted and the Controller's Stage-1 reading treated it as "stranded"; a castaway, not a captive. If the customer meant captivity, nothing in the film shows it. |
| R3 | "in that bag he founds her wives photo" | **PASS** | 7.5–12.5 s: over-shoulder, bright yellow lining, a small creased photo of a smiling woman in a yellow kurta, held, then set on the lining while he looks to sea (`f017-08.0s`). The woman is generated and unnamed (no real person). That she is his *wife* is inferred by the viewer — there is no ring, no caption; the placement (a photo carried for years) carries it. |
| R4 | "a lot of stuff that he could use to go back" | **PASS** | Rope, coconuts, dried fish, gourd, orange flare on the pebbles, and the paddle from the bag (`f040-19.5s`, `f046-22.5s`). |
| R5 | "he packs food and stuff and goes back" | **PARTIAL — two FAILs** | (a) Packing 20.5–24.5 s: fish, rope and flare go in; **the zip closes with two coconuts and the gourd still on the pebbles** (`f049-24.0s`) — the *food* is exactly what stays out. Producer-recorded (DF-2, "partial"). (b) Going back 24.5–28 s: he stands knee-deep beside the raft, bag on his back, bends and picks the paddle off the raft, and holds it (`f055-27.0s`). **He never boards or pushes off** in the 3.5 s used, nor in the unused 0.5 s of `gen/clips/b6.mp4`. It reads as "about to go", not "goes". NEW (not in the producer's defect list; Stage 5 §1 describes the beat as if realised). |
| R6 | "would be funny that he could keep his arms in the bag and food and so much stuff" | **PARTIAL** | 12.5–17.5 s: both hands are inside the open bag, but at **wrist-to-forearm depth**, the way anyone rummages in a backpack (`f030-14.5s`, `f034-16.5s`, and a 2-fps sweep of the whole beat). At no sampled frame does an arm go in past the elbow, let alone to the shoulder; there is no chin-on-the-rim. What lands is the second half: a stick emerges and becomes a full wooden paddle far longer than the bag (`f040-19.5s`) — that reveal reads clearly and is the film's joke. The customer's *named* gag (arms swallowed) is not on screen. Producer-recorded in Stage 5 §5 ("does not show the arms to the shoulder"), but the same document's LJ-3 line ("one arm to the shoulder ~13–15 s, both arms in ~15–17 s") overstates what the take contains. |
| R7 | "lets make an ad with mokobara" | **PASS** | Brand early: the code wordmark super at 5.0–7.5 s over the moment he finds the bag (`f012-05.5s`), the bag itself in frame from 3.5 s to 28 s. Clear close: navy end card 28–30 s with wordmark · `Transit Backpack · 30L` · `Room for the long way home.` · `mokobara.com` (`f058-28.5s`), legible at phone size. |
| R8 | "odysey movie angel" + "Avoid getting copyright violoations from odysssey" | **PASS on exposure; note on shape** | Prompts: no myth or film name (§1). Frames: no volleyball, no branded package, no named ship, no title-card style, no Greek/bronze-age dressing, no identifiable actor's face (the man is a generated Indian face). The elements used — tally marks, beard, a photo of the woman waiting, a driftwood raft with a paddle, dawn — are generic castaway tropes shared by many works, not protectable expression (INFERRED; not legal advice). Shape note: what is on screen is a *castaway* story; the specifically Odyssey-shaped element (a man held away from home, the wife waiting) survives only as the tally marks + the photo. A viewer is likelier to think "castaway film" than "Odyssey". That is not a copyright problem; it is a reading the customer may or may not want. |

---

## 3. Brand / product fidelity

Comparison sheet: `qa/checker/bag-vs-product-5.5-16.5-22.5-26.0s.jpg` (top row: `…Private_Island_1.jpg`, `…Private_Island_6.jpg`, film 5.5 s; bottom: 16.5 s, 22.5 s, 26.0 s).

- **Shape and colour (OBSERVED):** deep navy matte body, slim rectangular silhouette with a rounded top section, black padded straps, small top grab handle, bright yellow lining, plain tonal rectangular patch low on the front, black zip pulls — all present at 5.5, 16.5 and 26.0 s. The navy is a close match to the product photo; the yellow lining is the same sunshine yellow. Proportions against the man and the coconuts read as a ~45–50 cm pack, consistent with 48 × 31 × 16 cm on the page.
- **Where the likeness bends (OBSERVED):** (i) at 16.5 s the whole top opens as one hinged lid showing the lining — the real bag's main opening is a zip; it reads as "the bag, opened", not wrong, but it is not the product's mechanism; (ii) at 22.5 s the front pocket hangs open **downwards** to the pebbles with lining showing (`f046-22.5s`) — the product's front pocket zips at the top; a Mokobara employee would notice; (iii) 7.5–12.5 s the lower-left of the open lining shows an irregular hanging flap that can read as a **tear** (this is what the customer later called "slightly torn"); a torn bag is the wrong signal for the product.
- **Lettering on the bag:** the lower-front patch is plain in every checked frame at full resolution (5.5, 16.5, 19.5, 22.5 s). The two stills' copied wordmark marks were painted out before dispatch (`*.edit.json`); nothing came back in the video. PASS.
- **Wordmark and strings:** wordmark = the site's own SVG, pixel-identical rasterisation (§1). On-screen strings are exactly `Transit Backpack · 30L` (title "Transit Backpack" + "Capacity: 30L" from `transit-backpack.json`), `Room for the long way home.`, `mokobara.com`. The tagline is original: the site's lines are "The Joy Is in the Details", "Every street, every airport, every work desk", "out doing what it does best", "make your carry the easiest part of your journey" — no overlap in words or construction. It claims only room (30L is on the page). PASS.
- **Generated lettering anywhere (the OCR FLAG):** I looked at all 60 frames at 2 fps and at full resolution on the textured areas the OCR fired on (tally marks 0–3.5 s, pebbles, sea), plus the photo, the flare, the shirt and the raft. **No readable lettering exists** except the wordmark super (5.0–7.5 s) and the end card. The OCR tokens ("fiat", "Wars", "PULA"…) are scratches and pebbles. Producer's FLAG resolved: PASS.
- Fonts: Avenir Next, a system face; the brand's typeface is not verified anywhere in the fetched pages (Stage 2 (d)). The end card is clean but generic — the customer later said the font "could be better".

---

## 4. Production quality

**Identity of the man across the six clips (OBSERVED):** same type throughout — lean Indian man, long hair, full beard, cord bracelet, torn green shirt, cut-off khakis, barefoot. Drifts: (a) **beat 1 (1.5–3.5 s) wears a long-sleeved, buttoned shirt with rolled cuffs; beats 2–6 wear the sleeveless torn shirt** (`f005-02.0s` vs `f012-05.5s`) — producer-recorded DF-4; (b) beat 1's beard is jet-black and fuller, beats 3–4 show a grey-streaked beard (`f030-14.5s`) — mild, INFERRED as the same character aged by lighting/grade, but a careful viewer sees two beards; (c) the cord bracelet sits on the **right** wrist in beats 2, 4 and 5 while the anchor text says left — minor, new. The face itself holds well from beat 2 onward.

**Beat 1 — the open (NEW defect):** the board asks for one continuous pull-back from the hand to the small man before the marked rock. What was generated: 0–1.5 s ECU of the hand and marks, then a **hard in-model cut at 1.54 s** (scdet's largest score, 27.5) to a **static full-length portrait of the man looking straight into the lens** for 2 s, on an empty shore with a blown-white sky and **no marked rock in view**. The scale reveal ("how long he has been here") is not made by the camera; the years live only in the ECU. The frontal stare reads as a lookbook photo, not a survival film. The producer's LJ-8 asks the checker whether "the pull-back reveal lands" without recording that no pull-back exists.

**Bag identity across clips:** §3 — consistent colour and silhouette; opening mechanism and the front pocket differ between beats 4 and 5.

**Seams (OBSERVED):** hard cuts at 3.5, 7.5, 12.5, 20.5, 24.5 s; each new shot is a different setup, so there is no jump-cut feel. The 0.6-s crossfade at 27.4–28.0 s into the end card is smooth. No black or duplicate frames. Audio at the cuts: at 3.5 s and 7.5 s the incoming clip's native ambience is ~15–20 dB quieter for the first ~40 ms then recovers (a faint "hole"); at 12.5, 20.5, 24.5 s the level is continuous. No clicks (max sample step at every cut is below the file's own 99.9th-percentile step). INFERRED: the two 40-ms dips are at or below audibility on phone speakers; a human ear should confirm.

**Continuity between beats 4–6 (NEW):** the paddle comes out of the bag at 18–20.5 s; in beat 5 it is nowhere (not on the pebbles, not going into the bag); in beat 6 it is **already lying on the raft** before he picks it up (`f055-27.0s`). Where the paddle went between 20.5 and 24.5 s is unexplained. (The customer independently noticed this.)

**The gag's readability:** both arms clearly *in* the bag — yes, at forearm depth; **to the shoulder — no**; the paddle reveal — yes, clean, with a good beat of "stick… longer… oh, a paddle" over 18.0–20.5 s. The 5 s of ordinary rummaging before it (12.5–17.5 s) is the weak stretch: nothing impossible happens, so the disbelief is not built before the paddle. The producer's alternative take `gen/clips/b4.mp4` (att-003) is recorded as having one arm deeper and a longer paddle reveal; not re-judged here.

**Packing:** fish, rope, flare in; two coconuts and the gourd out at the zip (§2 R5).

**The dawn push-off:** not a push-off (§2 R5). The dawn itself is good — the first warm band on the horizon, rim light on the raft, the navy bag on his back against the gold.

**Audio:** native ambience (wind, surf, fabric, zip) is present under every beat; the Lyria bed enters at 7.5 s and the level curve is sensible (§1). **Speech or singing in the native audio: CANNOT_DETERMINE by code** (no local recogniser; the prompts and negative prompt forbid speech; the producer heard none). True peak −4.1 dBTP everywhere — safe, with room to spare.

**Resolution:** 720p sources upscaled to 1080p — the whole film is slightly soft on close inspection (the "Veo softening"); on a phone feed this is unlikely to be noticed, on a desktop it is.

---

## 5. Creative quality (observations, 1–5)

| Aspect | Score | Why |
|---|---|---|
| Cinematic look | 4 | The stills are genuinely handsome: grey pebble shore, the one navy object, the yellow flash when the bag opens. Loses a point for the flat white-sky portrait in beat 1 and the 720p softness. |
| Beat 1 — endurance | 3 | The tally-mark ECU is the right first image and says "years" without a word. The static stare-at-camera that follows says nothing. |
| Beat 2 — recognition | 4 | Colour is the hit, as designed; the crouch and brushing hands are quiet and right. The super over his shoulder reads like a caption, which is fine for the brand-early rule. |
| Beat 3 — the reason | 4 | The best image in the film: a small photo on a field of yellow. Holding three seconds on his profile looking to sea is a little long but emotionally correct. |
| Beat 4 — disbelief → laugh | 3 | The paddle lands. The disbelief before it does not, because the arms never do anything impossible. |
| Beat 5 — momentum | 3 | Good pace and good props; the coconuts left behind undercut "it takes everything". |
| Beat 6 — hope | 3 | Beautiful light, correct composition; but he is standing still holding a paddle, so the film ends on intent, not departure. |
| Beat 7 — home | 4 | Clean navy card, the real wordmark, three lines, legible. Generic type. |
| Comic timing of beat 4 | 3 | 5 s set-up / 2.5 s payoff is the wrong ratio; the payoff itself is well built (stick → blade → he regards it). |
| Brand integration | 4 | The bag is the object every beat turns on and never looks like a product shot; the super and end card carry the name without shouting. |
| Would a D2C brand run this | 3 | As a first pass to show the customer: yes, it is coherent, on-brand and funny in one place. As a paid placement: not yet — the arms gag, the packing leftovers, the non-departure and the beat-1 costume would each draw a note from a brand manager. |

---

## 6. Failure classification (earliest stage, one repair each)

| # | Defect | Producer-recorded? | Earliest stage | One repair |
|---|---|---|---|---|
| D1 | Arms never go in past the forearm; the named gag is carried by the paddle only | Recorded in Stage 5 §5, understated in LJ-3 | Stage 4 (route): image-to-video from a still whose first frame shows normal rummaging cannot be pushed to "arm to the shoulder" by text alone | Generate a beat-4 **still** that already shows one arm buried to the shoulder (nano-banana-2, USD 0.067, inspect), then i2v from it (USD 0.80); or accept the paddle-only gag and re-cut the beat to 2 s set-up / 4 s payoff at USD 0 |
| D2 | Zip closes with coconuts + gourd outside | Recorded (DF-2 partial) | Stage 5 (generation) | Beat-5 still with the pebbles already **empty** and the bag visibly full, then i2v of only the zip closing (USD 0.47); or trim beat 5 at USD 0 to end before the leftovers are legible |
| D3 | No push-off: he stands by the raft for 3.5 s | **New** | Stage 5 (generation) — the 4-s clip did not reach the action; Stage 3 asked for wade + board + two strokes in 3.5 s, too much for the length | Beat-6 still with him already kneeling **on** the raft, paddle in hand, one stroke in 4 s (USD 0.47); or buy 6 s and use the last 3.5 |
| D4 | Beat 1: in-model hard cut to a static frontal portrait; no pull-back; marked rock absent from the wide; long-sleeved shirt | Costume recorded (DF-4); the cut and the missing move **new** | Stage 5 (generation) — take 2's one change fixed the bag-on-shore story break and introduced the shirt and the portrait | Beat-1 still that is *already* the wide (small man, marked rock, empty shore, sleeveless), then i2v of a slow push-in; keep the ECU as a separate 1.5-s cut (USD ~0.47) |
| D5 | Paddle continuity: out of the bag at 20 s, absent in beat 5, already on the raft in beat 6 | **New** | Stage 3 (board): the board never says where the paddle goes between beats 4 and 6 | Board line "paddle goes into the bag last, before the zip" + beat-5 re-take; or beat-6 re-take with the paddle drawn from the bag on his back |
| D6 | Bag geometry: lid-opening at 16.5 s; front pocket hanging open downward at 22.5 s; lining flap that reads as a tear at 7.5–12.5 s | **New** (the tear is also in the customer's verdict) | Stage 5 (still generation) — the stills fixed these first frames | Re-draw the beat-3 and beat-5 stills with the product photo `…Private_Island_6.jpg` as the *opening* reference and "no torn fabric" in the prompt (USD 0.134), then i2v |
| D7 | Beard/hair shade and bracelet-wrist drift between clips | New, minor | Stage 5 | Accept for a first pass; a re-draw of any beat still should paste the hero still as reference (already done) and add "beard salt-and-pepper" to the anchor text |
| D8 | 720p sources, soft at 1080p | New, informational | Stage 4 (route chose 720p) | 1080p Veo output if the price allows; otherwise accept for phone feeds |
| D9 | 40-ms ambience dips at the 3.5 s and 7.5 s cuts | New, minor | Stage 5 (assembly) | 60-ms audio crossfade at each hard cut, USD 0 |

Nothing in the ledger, the prompts, the container or the brand strings needs repair.

---

## 7. Verdict

**DELIVERABLE WITH DEFECTS** — fit to present to the customer as a first pass, not fit to run as a paid ad without one more round.

In plain English: this is a 30-second vertical film in which a bearded man who has plainly been alone on a grey island for years finds a navy Mokobara backpack at the water's edge, opens it to a bright yellow lining and a photo of the woman he is going back to, reaches inside and pulls out — among rope, food and a flare — a wooden paddle far longer than the bag, packs, and stands at dawn beside a driftwood raft with the bag on his back before the film closes on the Mokobara wordmark, "Transit Backpack · 30L", "Room for the long way home." and mokobara.com.

What I verified with code: the file is exactly what the producer says it is (30.021 s, 1080×1920, H.264/AAC, hash identical, no edit lists, loudness −13.3 LUFS and true peak −4.1); all 18 paid attempts are reserved before settled, total USD 5.389 of 12.00, one Lyria HTTP 500 counted honestly, every artifact hash on disk matches the ledger; not one prompt sent contains a Homer, film, actor or prop name; the wordmark is the site's own SVG pixel for pixel; the three on-screen strings are byte-exact and inside the fetched page's facts; there is no generated lettering anywhere in the picture.

What I saw: a handsome, on-brand, coherent film whose joke lands once (the paddle) and whose story has three soft spots — the arms never disappear into the bag the way the customer described, the coconuts are left on the beach when the zip closes, and he never actually leaves. Plus a costume change and a static camera in the first three seconds. As far as it is measurable, the sound is level-safe and continuous; whether any stray voice is in the native ambience needs a human ear.

The two things most likely to make the customer ask for a change: **(1) the gag** — "keep his arms in the bag" is the customer's own sentence and it is not on screen; and **(2) the ending** — food left on the beach and a man who does not push off, so the "holds everything, and he goes home" promise is not closed.

---

## 8. Cross-reference with the customer's verdict (arrived during this check)

`HUMAN-VERDICT-V1.md` (18:14Z) classes v1 as SPECIFIC REPAIR with five items. Overlap with this check: the torn-looking bag in beat 3 = D6; the paddle "looked weird coming out of the bag" = D1's beat (the customer reads the reveal as odd where I read it as the one working joke — his reading governs); the paddle already on the raft = D5; "use mokobara logo/name properly" and "font style could be better" are brand-presence and typography notes this check scored 4 for legibility but flagged as generic. The customer did **not** raise the arms depth, the coconuts or the non-departure (D1–D3), which remain this checker's independent findings for the repair round. Both reads agree the film is presentable and needs one targeted round, not a re-shoot.
