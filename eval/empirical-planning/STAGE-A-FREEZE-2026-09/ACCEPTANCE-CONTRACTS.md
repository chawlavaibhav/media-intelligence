# Acceptance contracts — Stage A freeze (judged blind, from the artifact alone)

Each contract is 3–6 statements a first-language Indian judge can decide from the artifact with no prompt, route name, arm, cost, rule id or Canon reference (a build-time guard rejects any such token in a statement). Phrased `ACCEPT only if …` / `REJECT if …`; no rubric scores, no adjectives without an observable. The deterministic pre-checks that count as rejects (E5) are listed per case in the separate section at the end of this file and in each twin; they are run by code and are not shown to the judge. A refusal, error or blank artifact is a reject, never an exclusion.

Judging mechanics follow `eval/experiments/EVAL-038/JUDGING-PROTOCOL.md`: stripped artifacts under blinded names, a salted commitment of the key committed before judging, the key off-repo, revealed only after every verdict is committed. Identity contracts are judged as line-ups: the artifact beside the references and the same-category decoys; the judge must pick the referenced identity.

Language is never pooled: en, hi and hg verdicts are tallied separately.

## IMG-CORE-01 (en)

- ACCEPT only if exactly one bottle is in frame and no other object, hand or prop appears.
- ACCEPT only if the bottle reads as clear glass with liquid inside — a visible refracted edge or a light-through-liquid glow — not as an opaque or plastic body.
- ACCEPT only if the label area is blank: no lettering, logo, numeral or symbol anywhere on the bottle or the image.
- REJECT if the cap, neck or base is deformed, doubled or cut off by the frame edge.
- REJECT if the background is dark or cluttered (the customer asked for a light background).

## IMG-CORE-02 (hg)

- ACCEPT only if exactly one adult man, plausibly 25–28, is in frame holding a phone with a visible hand.
- ACCEPT only if the phone screen shows no readable content — blank, dark or plain glow.
- REJECT if any lettering, logo or numeral appears anywhere in the image (including signage in the background).
- REJECT if the hand holding the phone has the wrong number of fingers, a bent-through joint, or fingers passing through the phone.
- ACCEPT only if the face is fully formed (two eyes, natural mouth, no doubled features); REJECT if the expression is angry, fearful or a fixed blank stare.

## IMG-CORE-03 (hg)

- ACCEPT only if the camera looks straight down (top view) and a round pot of biryani sits at the centre.
- ACCEPT only if all four named sides are identifiable: a bowl of raita, salad, sliced onion, and lemon.
- REJECT if any lettering, price, logo or numeral appears anywhere (including on crockery or napkins).
- REJECT if rice grains, meat pieces or garnish are visibly melted, fused or duplicated in a repeating pattern.
- REJECT if the spread includes luxury props (gold cutlery, wine glass, candles) — the customer asked for premium but not over the top.

## IMG-CORE-04 (hi)

- ACCEPT only if the image is clearly an illustration (flat or painterly rendering, visible stylisation) and not a photograph.
- ACCEPT only if one child, plausibly 6–7, sits at a window with a paper boat in her hand and rain is visible outside.
- REJECT if the child is shown with an open crying mouth or visible tears, or in physical danger (water reaching her, a fall); ACCEPT only if her mouth is closed or nearly closed.
- REJECT if any lettering, title or numeral appears anywhere in the image.
- REJECT if there is no picture — a blank or black frame, or text where the image should be.

## IMG-TEXT-01 (hi)

- ACCEPT only if the lettering reads exactly "दीपावली की शुभकामनाएं", "सभी मिठाइयों पर 20% छूट" and "श्री गणेश मिष्ठान भंडार" — every matra and the conjunct ष्ठ in मिष्ठान correct, the figure 20 present as either 20 or २०; REJECT on any wrong, missing, doubled or invented character.
- ACCEPT only if "श्री गणेश मिष्ठान भंडार" is the largest lettering on the poster.
- REJECT if any other lettering or pseudo-lettering (scribbled or half-formed letters) appears anywhere.
- ACCEPT only if at least one of a sweet box or lit diyas is recognisable.
- REJECT if any string is cut by the frame edge or overlaps another string.

## IMG-TEXT-02 (en)

- ACCEPT only if the lettering reads exactly "FLAT 40% OFF", "First 100 members only" and "AlphaFit" — same letters, same case, the numerals 40 and 100 correct; REJECT on any missing, extra, swapped or malformed character.
- ACCEPT only if the 15 January end date is readable in some wording.
- REJECT if any person, silhouette or body part appears.
- ACCEPT only if black and neon yellow are the two dominant colours and one corner is empty of lettering and graphics.
- REJECT if any other lettering or pseudo-lettering appears anywhere.

## IMG-EDIT-01 (en)

- REJECT if any person, or part of a person, remains anywhere in the image.
- ACCEPT only if the sofa is the same object — same outline, same colour, same position in frame — when the result is flicked against the supplied photo.
- REJECT if the vacated area shows a smudge, a repeated texture patch, a colour seam or an object that was not in the original.
- REJECT if the lighting direction or overall brightness of the room has changed.

## IMG-EDIT-02 (hi)

- ACCEPT only if the background is uniformly white with no leftover clutter, edge halo or colour cast.
- ACCEPT only if the pack still reads exactly "शुद्ध मसाले" and "५०० ग्राम" — the conjunct द्ध and the Devanagari digits ५०० unchanged; REJECT if any character is altered, blurred into a different form or re-rendered in a different typeface.
- ACCEPT only if the pack's colour matches the supplied photo when flicked side by side.
- REJECT if the pack's outline, size or position has changed, or if any part of the pack is cut off.

## IMG-EXT-01 (en)

- ACCEPT only if the result is 9:16 and contains the whole supplied banner uncropped — the boat and every letter of the headline fully visible.
- ACCEPT only if the boat and the headline sit in the same relationship to each other as in the supplied banner.
- REJECT if the headline's letters have changed shape, spacing or spelling.
- REJECT if the added sky or water shows a visible seam, a repeated tile, a horizon that does not line up, or a second boat.

## IMG-COMP-01 (hg)

- ACCEPT only if the face in the result is the same person as in the supplied portrait when the two are shown side by side with two decoy portraits (the judge must pick the supplied portrait as the match).
- ACCEPT only if the lipstick's shade matches the supplied packshot and not either decoy shade.
- ACCEPT only if the model's hand visibly holds the pack — fingers wrap it, the pack does not float or pass through the hand.
- ACCEPT only if the headline reads exactly "नया शेड, वही भरोसा" with every matra correct.
- REJECT if a second person, a second product or any other lettering appears.

## IMG-REF-01 (hi)

- ACCEPT only if the tin in the result is the referenced tin and not either decoy when the judge sees the result beside the three references and the two decoys.
- ACCEPT only if the printed label reads as on the references — same words, same arrangement, same colours; REJECT if lettering is re-drawn, garbled or re-arranged.
- ACCEPT only if the tin's yellow matches the references when flicked side by side.
- REJECT if the tin's proportions, cap or handle differ from the references, or if a second tin appears.
- REJECT if any lettering appears outside the tin itself.

## IMG-REF-02 (en)

- ACCEPT only if, shown the result beside the three references and the two decoy sets, the judge identifies the referenced person as the match (same face, same hair, same build).
- ACCEPT only if she sits at a cafe table with an open laptop whose screen shows nothing readable, smiling toward the camera.
- REJECT if any lettering, logo or numeral appears (including cafe signage or the laptop lid).
- REJECT if hands or face show anatomical faults (extra fingers, doubled features).

## VID-T2V-01 (hi)

- ACCEPT only if one man is visible speaking to camera and the audio track carries a Hindi voice saying "इस दवाई से मेरी फसल दोगुनी हुई" — every word present and in order; REJECT if a word is missing, garbled, or spoken in another language.
- ACCEPT only if his mouth opens and closes in time with the spoken words (a first-language judge hears and sees the same syllables).
- REJECT if the clip is silent or the voice is a separate narration over a closed mouth.
- ACCEPT only if a bottle is held in his hand for the whole clip and stays the same object.
- REJECT if any lettering appears anywhere in any frame.

## VID-T2V-02 (en)

- ACCEPT only if one woman runs toward the camera and passes it within the clip, at a visible sprint (arms pumping, feet leaving the ground).
- ACCEPT only if her running shoes are clearly seen at least once as she passes.
- REJECT if her body, legs or feet visibly warp, multiply, slide without steps, or change identity between the first and last second.
- REJECT if any speech, music or lettering is present.
- REJECT if she never reaches or passes the camera (a jog in place or a distant figure does not satisfy the request).

## VID-T2V-03 (hg)

- REJECT if there is no clip — a blank or black video, or text where the video should be.
- ACCEPT only if the clip is clearly illustrated (picture-book rendering) and not photoreal.
- ACCEPT only if a small child stands alone in the rain first and an adult with an umbrella then arrives and embraces the child before the clip ends.
- REJECT if the child reads as in danger, injured or terrified rather than a little scared, or if the ending is not the embrace.
- REJECT if any speech, music or lettering is present.

## VID-T2V-04 (en)

- ACCEPT only if one glass bottle of orange juice with a blank label is the subject for the whole clip and no hand, person or second bottle appears.
- ACCEPT only if the camera moves slowly (a reveal or drift) while the bottle itself stays still and keeps its shape; REJECT if the bottle warps, changes size or shifts on the surface.
- ACCEPT only if condensation droplets are visible on the glass at some point.
- REJECT if any voice, music or lettering is present.

## VID-2SPK-01 (hi)

- ACCEPT only if two adults are visible and the audio carries, in Hindi and in this order, "यह रंग कैसा लगेगा?" then "घर जैसा" — every word present; REJECT if either line is missing, changed or paraphrased.
- ACCEPT only if the woman's lips move while the first line is spoken and the man's lips move while the second is spoken.
- REJECT if the second speaker's lips move while the first line is spoken, or the first speaker's while the second is spoken.
- ACCEPT only if a paint can is visible at some point in the clip.
- REJECT if either person changes identity within the clip, or if any lettering appears.

## VID-KNEE-01 (en)

- ACCEPT only if one glass bottle of orange juice with a blank label is the subject for the whole clip and no hand, person or second bottle appears.
- ACCEPT only if the camera moves slowly (a reveal or drift) while the bottle itself stays still and keeps its shape; REJECT if the bottle warps, changes size or shifts on the surface.
- ACCEPT only if condensation droplets are visible on the glass at some point.
- REJECT if any voice, music or lettering is present.

## VID-TOPO3-01 (hi)

- ACCEPT only if, in the first, middle and last frame, the lettering reads exactly "दीपावली की शुभकामनाएं", "सभी मिठाइयों पर 20% छूट" and "श्री गणेश मिष्ठान भंडार" (the figure 20 as 20 or २०); REJECT if any character differs between frames or from the strings.
- REJECT if any string drifts, wobbles, smears or flickers across the clip.
- ACCEPT only if "श्री गणेश मिष्ठान भंडार" is the largest lettering in every frame.
- ACCEPT only if some movement is visible (diya flames or light) — a still image held for 6 s is a reject.
- REJECT if any other lettering or pseudo-lettering appears in any frame.

## VID-I2V-01 (en)

- ACCEPT only if the viewpoint visibly travels around the bottle (a different side of the bottle is seen at the end than at the start).
- ACCEPT only if the bottle keeps the shape, size, cap and blank label of the first frame throughout; REJECT if it warps, drifts on the surface, or grows lettering.
- REJECT if the highlight on the glass flickers, or sits at the same spot on the bottle in the first and last frame while the viewpoint has changed.
- REJECT if speech or music is present, or any lettering.

## VID-I2V-02 (hi)

- ACCEPT only if the frame edges and background stay fixed for the whole clip (no pan, zoom or drift).
- ACCEPT only if the man's face is recognisably the same person in the first and last frame, with no change of hairline, jaw or eye spacing.
- ACCEPT only if he visibly glances toward the phone and his expression changes to a slight smile within the clip.
- REJECT if his hand, the phone or his features distort, or if any lettering appears.

## VID-I2V-03 (hg)

- ACCEPT only if the man goes from his starting pose to standing tall with both arms raised within the clip.
- ACCEPT only if the face in the last second is recognisably the same person as in the first frame.
- REJECT if arms, hands or the phone multiply, stretch, pass through the body or vanish during the movement.
- REJECT if the clip is nearly static (a slight sway is not the requested celebration), or if any lettering or audio is present.

## VID-I2V-04 (hi)

- REJECT if there is no clip — a blank or black video, or text where the video should be.
- ACCEPT only if rain is visibly falling and the water outside visibly moves, with the camera fixed.
- ACCEPT only if the girl's face is the same as the first frame and the illustration style does not shift toward photoreal.
- ACCEPT only if she visibly turns her gaze to the boat and her expression softens into a slight smile.
- REJECT if any lettering appears.

## VID-REF-01 (en)

- ACCEPT only if the pack in the clip is the referenced pack and not either decoy, judged on a paused mid-clip frame beside the references and decoys.
- ACCEPT only if the pack's label stays as printed on the references in every sampled frame (start, middle, end); REJECT if lettering morphs, blurs into new shapes or re-arranges.
- ACCEPT only if the pack visibly turns or the viewpoint visibly changes during the clip.
- REJECT if the pack's proportions or colours change during the clip, or if any added lettering, voice or music is present.

## VID-REF-02 (en)

- ACCEPT only if, on a paused frame where she faces the camera, the judge picks the referenced person as the match against the two decoy sets.
- ACCEPT only if she enters the frame walking, sits at a table and looks at the camera before the clip ends.
- REJECT if her face or hair changes between the walking frames and the seated frames.
- REJECT if any lettering or speech is present.

## VID-MS-01 (hg)

- ACCEPT only if the clip contains at least three distinct shots (visible cuts) showing, in order, a home scene with a phone, an airport with the pair running with bags, and a beach.
- ACCEPT only if the same man and the same woman appear in every shot — same faces, same hair — when paused on one frame per shot.
- REJECT if any logo or lettering appears anywhere in any shot.
- REJECT if a shot is shorter than one second or the total runs under 13 s or over 17 s.
- REJECT if any speech or music is present.

## VID-MS-02 (en)

- ACCEPT only if there are exactly three shots in this order: a person restless in a dark bedroom; a bare mattress in morning light; the same person asleep in a bright room.
- ACCEPT only if the person in shot 3 is recognisably the person in shot 1.
- ACCEPT only if shot 1 is visibly darker than shot 2 and shot 3 is the brightest.
- REJECT if any lettering, voice or music is present, or if the clip runs under 9 s or over 11 s.

## AUD-TTS-01 (hi)

- ACCEPT only if a first-language Hindi listener hears exactly "इस दवाई से मेरी फसल दोगुनी हुई" — every word, in order, no extra word.
- ACCEPT only if it is one male voice speaking clear Hindi; REJECT if any word is heard as a different word (e.g. दवाई or दोगुनी mispronounced into another word).
- REJECT if any music, effect, second voice or English word is present.
- REJECT if the file is silent, truncated mid-word, or longer than 6 seconds.

## AUD-TTS-02 (hg)

- ACCEPT only if the listener hears exactly "Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par." — every word, in order.
- ACCEPT only if "Kaushal Setu" is heard as the Hindi words कौशल सेतु; REJECT if either word is heard as something else.
- ACCEPT only if every word, English and Hindi, is understood on a single listen by a Hindi-English speaker; REJECT if any word has to be replayed to be made out.
- REJECT if any music, effect or second voice is present, or if the file is longer than 6 seconds.

## AUD-TTS-03 (en)

- ACCEPT only if the listener hears exactly "Zero petrol. Zero noise. All city." — three sentences, no added or missing word.
- ACCEPT only if there is an audible pause between each sentence.
- ACCEPT only if the accent is recognisably Indian English; REJECT if it is American or British.
- REJECT if any music, effect or second voice is present, or if the file is longer than 6 seconds.

## AUD-LIP-01 (hi)

- ACCEPT only if the man's mouth opens and closes with the syllables of "इस दवाई से मेरी फसल दोगुनी हुई" — a first-language Hindi judge sees the words being spoken; REJECT if the mouth moves out of time by a visible beat.
- ACCEPT only if his lips are closed or at rest during the silence after the line.
- REJECT if the face changes identity, the mouth region shows a visible patch, blur, colour seam or flicker, or the background changes.
- REJECT if the audio in the output is not the supplied voice (re-synthesised, clipped or shifted).

## AUD-LIP-02 (hg)

- ACCEPT only if the mouth follows the whole line "Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par." in time — including the English words — with no visible lag or lead.
- ACCEPT only if the lips rest closed during the pauses and after the line.
- REJECT if the face changes identity, or the mouth region shows a patch, blur, seam or flicker.
- REJECT if the output audio is not the supplied voice.

## AUD-LIP-03 (en)

- ACCEPT only if the mouth follows "Zero petrol. Zero noise. All city." in time, sentence by sentence.
- ACCEPT only if the lips are closed in each of the two pauses and after the last sentence.
- REJECT if the face changes identity, or the mouth region shows a patch, blur, seam or flicker.
- REJECT if the output audio is not the supplied voice.

## MUS-01 (hi)

- ACCEPT only if the track is 28–32 s long and has no sung or spoken words.
- REJECT if drums or heavy percussion dominate the mix, or if an orchestral string or brass swell is present.
- ACCEPT only if at least one recognisably Indian instrument colour (flute/bansuri or tabla-like percussion) is audible.
- REJECT if the file is silent, clipped or ends with an abrupt cut mid-phrase.

## MUS-02 (en)

- ACCEPT only if the track is 28–32 s long and has no sung or spoken words.
- ACCEPT only if the energy audibly builds from the start to the end (more elements or a stronger pulse by the last third).
- REJECT if there is a large orchestral or 'trailer' swell, or if the arrangement is so dense it would mask street ambience.
- REJECT if the file is silent, clipped or ends abruptly mid-phrase.

---

# Deterministic pre-checks (E5) — not part of the judge's packet

Run by code on every artifact before judging; any failure is a reject, never an exclusion. The same per-case list appears in each twin (both emitted from one list).

### IMG-CORE-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### IMG-CORE-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### IMG-CORE-03

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### IMG-CORE-04

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### IMG-TEXT-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- required string absent (Cloud Vision, T-BENCH) → reject before judging
- refusal / error / empty artifact → reject

### IMG-TEXT-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- required string absent (Cloud Vision, T-BENCH) → reject before judging
- refusal / error / empty artifact → reject

### IMG-EDIT-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### IMG-EDIT-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### IMG-EXT-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### IMG-COMP-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- required string absent (Cloud Vision, T-BENCH) → reject before judging
- refusal / error / empty artifact → reject

### IMG-REF-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### IMG-REF-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-T2V-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-T2V-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-T2V-03

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-T2V-04

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-2SPK-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-KNEE-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-TOPO3-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- required string absent (Cloud Vision, T-BENCH) → reject before judging
- refusal / error / empty artifact → reject

### VID-I2V-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-I2V-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-I2V-03

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-I2V-04

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-REF-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-REF-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-MS-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### VID-MS-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### AUD-TTS-01

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

### AUD-TTS-02

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

### AUD-TTS-03

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

### AUD-LIP-01

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### AUD-LIP-02

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### AUD-LIP-03

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

### MUS-01

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

### MUS-02

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject
