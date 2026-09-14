# UPWORK-INTRO-V3-SHOWCASE — execution record and product learning

Status: FIRST PASS ASSEMBLED, awaiting Controller judgment (ACCEPT / SPECIFIC REPAIR / REJECT).
Run class: paid commercial showcase / product-learning production. Not Registry, Stage-A or Alpha-1 evidence. No sealed
evidence touched; nothing written to the Registry.

## A. Film
`assembly/v3/upwork-intro-v3.mp4` — 1920x1080, 30 fps, H.264 (CRF 16), AAC 256 kbps 48 kHz stereo, **59.87 s**, 19.4 MB.
Loudness −14.6 LUFS integrated, true peak −1.5 dBTP, LRA 6.4 LU (`assembly/v3/audio-report.json`).
Beat map (segment starts): `assembly/v3/timeline.json`. Deck check: 0 off-deck strings (every on-screen string comes from
`plan/COPY-DECK-v3.yaml`; timestamps/counters are mechanical).

## B. Spend (cumulative ledger `gen/LEDGER.jsonl`; pinned prices; cap INR 2,000 = USD 20.96)
- **Reserved at pinned prices: USD 3.2836 = INR 313.3** (15.7 % of the cap). 37 paid calls, 0 refused, 4 failed (Lyria ×3, none on fal).
- **fal actual (balance read before/after): USD 3.2315 → 0.2589 = USD 2.9726 billed** vs USD 3.0500 reserved on fal routes
  (GPT Image 2 metered slightly under the 0.053 projection). Vertex credits: 4 Lyria calls (USD 0.24 reserved; whether the
  three failed calls were billed is unknown — provider statement not reconciled). Sarvam: 16 calls ≈ INR 4.3.
- By route: Kling v3 Pro i2v 5 calls USD 2.352 · Seedream 5 Pro Edit 6 × 0.0675 = 0.405 · GPT Image 2 4 × 0.053 = 0.212 ·
  FLUX.2 Pro 1 × 0.03 · Lyria 4 × 0.06 = 0.24 · Sarvam 0.0446.
- The pass was sized by the **fal cash balance (USD 3.23 at start), not by the cap**. The cap was never approached.

## C. Real clock (`gen/CLOCK.json`, recorded mechanically)
- Brief complete (A0 packshot accepted, colours + offer frozen): **2026-09-14 18:13:59 IST**
- Aarohi bundle complete on disk (4 sizes, 6 hooks, Hindi, 9:16 video ad): **18:40:52 IST**
- **Elapsed: 0 h 26 m 52 s.** Inside four hours; the speed-proof criterion holds. Shown verbatim on the DELIVERED beat.
  (Clock excludes Brewa/Kora/Dhaba work and the intro's own assembly, which are not part of the sample order.)

## D. Asset table
`gen/ASSET-TABLE.md` (generated from `gen/ASSETS.jsonl`, which holds prompt, reference, provider/model/surface, pinned price,
start/end, latency, result, human verdict, failure reason, repair/fallback per asset).

Summary: stills 10 draws / 9 accepted / 1 rejected (FLUX Dhaba) / 1 fallback accepted (GPT Image 2 Dhaba). Video 5 draws /
4 accepted / 1 rejected (Kling B2). Audio: VO 16 calls all verbatim on transcript check (`tools/vo_check.py`, triage tier,
not evidence); music 4 calls, 3 failed, 1 accepted.

## E. Deviations from the frozen package (what the executor had to change, and why)
1. **Video slots not animated: B3 (Brewa evening) and Kora motion (optional).** Cause: fal cash balance USD 3.23 at start;
   every frozen video route (Kling / Wan / H3) bills to that pool. The pass covered A1, A2, A3, B1 on Kling; B2 was run
   from the unspent fallback reserve and rejected (see G). B3 and Kora appear as stills in the film. Cost to complete
   after a fal top-up: ≈ USD 0.45 each on Kling at 4 s; still inside the cap.
2. **Music prompt rewritten after 3 route failures.** The frozen Lyria prompt returned HTTP 503 then 500 ("try a different
   prompt") on the identical send and once more on a shortened variant. A neutral rewrite of the same musical description
   (no "advertising / DTC creative studio / 58-second"; framed as a "design-studio showreel", 30 s) succeeded on the first
   try. Lyria 2 returns ~32.8 s; the 58-s bed is that track looped with two 3-s crossfades (deterministic), ducked under VO.
3. **Aarohi scenes at mixed aspects.** A1 and A3 were generated 16:9 so they can own the full 1920x1080 frame (§16 demands
   full-screen hero/motion shots); A2 at 4:5 as the static/9:16 source. The 9:16 video ad is the approved Ledge 9:16 layout
   with the three clips cover-fitted into its plate region, offer text composed in post.
4. **VO takes.** Sarvam bulbul:v3 at pace 1.0 read at ~130 wpm; a second set at pace 1.08 was generated (16 calls total,
   ≈ INR 4.3). The chosen mix (`plan/VO-TAKES.json`) averages ≈ 139 wpm; speech totals 47.8 s inside 59.9 s. Sarvam
   output is not deterministic across calls (pace 1.08 produced longer reads on two paragraphs).
5. **"→" glyph.** Helvetica Neue via hb-view has no U+2192; arrows in labels are drawn deterministically.
6. **GPT Image 2 sizes.** 1024x1280 (4:5) and 1536x864 (16:9) at quality=medium instead of the 1024-long-side pin, to keep
   packshots usable at 1080p; metered cost stayed at/below the 0.053 projection.
7. **Seedream image sizes.** Explicit 1920x1080 / 1280x1600 (inside the ≤ 1536² price tier) instead of `auto_1K`, for
   full-frame use.

## F. Failures and repairs (kept individually; nothing silently regenerated)
- `dhaba-r1` FLUX.2 Pro — **rejected**: a second rice bowl and no clean upper-left copy space. This is the REAL rejected
  output shown for 0.5 s in the QA beat (two accent rings on the rice bowls, "REJECTED · REDRAWN"), then the accepted
  GPT Image 2 redraw (`dhaba-r2-gpt`) — the package's named fallback, one call.
- `music-r1/r2/r3` Lyria — 503 / 500 / 500; `music-r4-neutralprompt` accepted.
- `vid-b2-r1` Kling — **rejected**: kettle preserved, but the model widened the framing vs the still and sharpened the far
  shopfronts; letter-shaped signage and a metro-style sign become visible in the last second. Illegible, but it reads as
  stray lettering at full screen. No fallback affordable (Wan 4 s = 0.56 > 0.26 fal remaining). B2 stays a still.
- Accepted-with-note: `a3-r1` (diya beside, not behind; lighter world than briefed), `vid-a3-r1` (extra petals scatter),
  `b2-r1` still (far shopfront sign blurred and illegible).

## G. Product learning (proposals only — no Registry mutation, no self-authorised project change)
**WHAT THE FROZEN PLAN GOT RIGHT.** Packshot-first then Seedream 5 Pro Edit with the packshot as the supplied reference:
9/9 product-fidelity edits accepted on the first draw (bottle and kettle geometry, colour, mark, cap/handle all held; no
added labels). Kling v3 Pro i2v on those stills: 4/5 accepted first draw, every one with the product intact. Exact-text
mechanism B (code composes every string on textless plates) produced zero text defects across 23 deliverable files
including Devanagari. The freeze→static and static→motion beats work as designed. GPT Image 2 medium was enough for
three premium packshots/base visuals (3/3). The one-draw-then-judge discipline held: 37 calls, USD 3.28.

**WHAT THE EXECUTOR HAD TO CHANGE FOR API/TECHNICAL REASONS.** See E: pool sizing (fal cash), Lyria prompt wording,
aspect choices per slot, arrow glyph, explicit sizes.

**WHAT ROUTE FAILED.** Lyria 2 on the frozen prompt (3/3 failed; wording-sensitive — "advertising"/"creative studio"/"58-second"
are the suspects; unproven). FLUX.2 Pro on a seven-element flat-lay with a negative-space instruction (1/1 failed on count
+ framing; GPT Image 2 fallback 1/1). Kling v3 Pro on a scene with a city-street background (1/1 rejected for
background-signage lettering; the model also drifted the framing wider than the still).

**WHAT VISUAL DEFECT WAS NOT PREDICTED.** (a) I2V "sharpening" of far-background signage into letter shapes on a plate
whose still had only blurred signs — the still passed the text scan, the clip did not. (b) I2V framing drift (zoom-out)
on a lateral-drift prompt. (c) Petal multiplication on the festive push-in ("one or two petals" became a scatter).
(d) Seedream ignoring "well behind the product" for the diya and the "dark burgundy" world (kept the packshot's light wall).

**WHAT SHOULD CHANGE IN MEDIA INTELLIGENCE LATER (proposals, not authorised).**
1. Post-draw text scan must run on video last/mid frames, not only on the source still (the Cloud Vision adapter exists
   and has never been invoked on a real artifact — this run shows why it matters).
2. Pool-aware planning: the router should read live pool balances (fal cash / credits / Sarvam) before a plan is frozen;
   here the cap was 6× the binding constraint.
3. A Lyria prompt-hygiene note in the music lane (commercial wording triggers refusals; describe the music, not the use).
4. Route note for I2V on plates with legible-world backgrounds (streets, shops): prefer stills with no signage, or crop.
5. Sarvam TTS non-determinism across calls: pick takes by measured wpm; a deterministic-seed field does not exist.
6. Template candidates from this run: the Ledge (4:5/1:1/9:16/WA + hooks + Hindi), the Kora poster register, the Dhaba
   Hindi overlay, and the 9:16 "Ledge in motion" ad — all code, all reusable.

## H. Self-check against §20 (Controller judges by eye and ear)
1–3 hero is paid Kling footage full-screen; static ads by 5 s; video ads by 18–25 s. 4 images get 6.0–17 s and own the
frame. 5 full-screen generated outputs: A1 hero, A3, B1, Kora ×2, plus the 9:16 ad at full height. 6 both transitions
present. 7 geometry held (see verdicts). 8 no stray lettering in the film (B2 clip excluded). 9–10 all strings from the
deck, Devanagari via Kohinoor. 11 four worlds. 13 no presenter. 14 no internal terminology on screen or in VO. 15
disclosure on the brief card and the first work frames. 16 no performance claim. 17 "Adwisely" once in VO (and as the
wordmark twice on screen). 18–19 STANDARD 24 HOURS before 4-HOUR EXPRESS, express marked paid add-on. 20 CTA card + line.
22 elapsed 0 h 26 m 52 s, mechanical. 23 captions on every beat. 24 is the Controller's call.

Known limits for judgment: the VO accent read by the triage transcript model flips between "American" and "mild Indian"
(the Lab's human judge accepted `aditya` for Indian English; the Controller should listen); Kora has no motion; Brewa
has one motion shot; the music bed is a looped 32.8-s track.
