# CREATIVE BLUEPRINT V4 — Controller-frozen creative, executed with the two accepted Canon packs

Creative direction, positioning, script line, four movements and the second-by-second edit are FROZEN by the Controller
package (§5–§11). This blueprint records how that package is executed: design tokens, per-beat layout, the Canon check
lines (product_appearance PA-D1…D10, composition_and_attention CA-D1…D11) answered pass/fix, and DOCTRINE_DEVIATIONS.
Nothing here re-opens the direction.

## 1. Design tokens (single source: `tools/tokens.py`; the compositor refuses hard-coded radii/margins/colours)

| token | value | token | value |
|---|---|---|---|
| canvas_width × canvas_height | 1920 × 1080 @ 30 fps | safe_x / safe_y | 120 / 90 px |
| card_radius | 26 px (every wrapper card) | bubble_shape / bubble_size | rounded-square, radius 26 (same system) / 200 px |
| card_border | 1 px #111111 @ 14 % | card_shadow | blur 28, offset y 14, black @ 22 % |
| wrapper_bg | #F3EFE7 | wrapper_fg | #111111 |
| muted_fg | #5F5A54 (5.9:1 on bg) | accent | #FF5A3C — marks, rules, highlight rings only; never running text |
| h1_size / h2_size | 112 / 64 px | body_size / small_size | 40 / 32 px |
| spacing_xs / sm / md / lg | 12 / 24 / 48 / 96 px | font | Helvetica Neue (Bold / Medium / Regular), hb-view rasterised; Kohinoor Devanagari only inside the Hindi creative |

Text rules (hard): measured bounding box must sit inside the safe area or the layout FAILS (no silent clip); no wrapper
text < 32 px; no main claim < 48 px; CTA ≥ 64 px. Contrast: wrapper text only on wrapper_bg or on a solid tab of
wrapper_bg at ≥ 94 % opacity; measured ≥ 4.5:1 (body) / ≥ 3:1 (display) by the compositor's WCAG check over the actual
pixels behind each text box. Creative fit: `contain` for every portrait/deliverable; `cover` only for the two 16:9 native
assets (Brewa B1 scene 1920×1080, Aarohi A1/A3 clips 1920×1080) which are shown at native size — zero crop.

## 2. Speaker (Movement 1) — art direction for the anchor still and the native-speech clip

Fictional Indian creative professional, woman, mid-thirties; not Vaibhav, never named. Chest-up medium close, direct eye
contact, camera at eye level, 50 mm look, subject centred-high with breathing room on both sides (so a 200 px rounded
square crop on the face works later). Contemporary creative-studio interior: warm plaster wall, one out-of-focus shelf
with paper/ceramic objects, a plant edge, wooden surface — subtle depth, no beige empty wall. Wardrobe: plain charcoal
crew-neck knit, no jewellery, no logos, no print. Face: natural skin texture, normal teeth, restrained expression.
Absolutely no readable text anywhere (no monitors, signs, books with titles, wall type).

Canon — product_appearance applied to the person/scene (the pack scopes to products; person-skin doctrine is a declared
pack limit, so PA lines are applied as lighting discipline only):
- PA-D1 finishes declared: skin = diffuse with one small direct highlight kept (sk_lsmx_0051 qualification — not removed);
  knit = matte; wall = matte plaster; shelf objects = matte ceramic. PASS by declaration in the prompt.
- PA-D2/D3: one large soft source (a window camera-left), one highlight family, soft shadow edge → prompt says "one large
  soft window light from camera-left". PASS.
- PA-D4: fictional source named (window, left); no contradicting shadow. Checked on the still post-draw.
- PA-D5: warm mid-tone skin against a lighter warm wall, separated by tone (grayscale check post-draw). PASS/FIX post-draw.
- PA-D6: key level declared "daylight interior, soft, mid-key". PASS.
- PA-D7: what the image sells at a glance: "a calm professional looking at me" — needs no copy. PASS.
- PA-D8: no glass/dark glossy objects in frame by design. PASS.
- PA-D9: hero angle = frontal (eye contact is the brief's forcing clause). DEVIATION recorded (§5).
- PA-D10: deviations listed in §5. PASS.

Speech: the frozen line, natural pause after "So the bar went up.", conversational, understated, Indian English.
Camera static; restrained head movement; hands out of frame or resting.

## 3. Edit (Movements 2–4) — per beat, with the CA check lines

| t | beat | 1st / 2nd / 3rd read (CA-D1) | zone (CA-D2) | edge (CA-D3) | fit | device (CA-D7/D11) |
|---|---|---|---|---|---|---|
| 0.0–9.0 | Speaker full screen | eyes / mouth / room | centre (scene points inward: sole statement) | fit-with-gap | native 16:9 | stillness; no supers |
| 9.0–12.0 | Handoff: speaker → bubble (0.6 s scale), statement S1–S3 | statement / bubble / — | statement left zone; bubble bottom-left | fit-with-gap | — | one controlled scale |
| 12.0–18.0 | Proof 1: Aarohi master 4:5 contain, wrapper S4/S5 left | the ad / wrapper line / bubble | ad right zone | fit-with-gap (safe area) | contain | cut; stillness |
| 18.0–24.0 | Proof 2: craft ad contain; then HOOK → OFFER → CTA sequential spotlight | highlighted element / its label / rest of ad | ad right zone, labels left | fit-with-gap | contain | one attention device per beat: spotlight (blocking), no arrows |
| 24.0–30.0 | Proof 3: Brewa packshot contain (2.5 s) → B1 scene native 16:9; S9/S10 + S11 on a tab | product / line / bubble | packshot left zone → kettle centre | fit-with-gap | contain → native (no crop) | cut; new information = the scene |
| 30.0–38.0 | Proof 4: A1 hero clip 5.0 s + A3 clip 3.0 s, full screen; S12 tab first 2.5 s | the product / motion / — | native composition | native | native (no crop) | one cut, motivated by the new scene |
| 38.0–44.5 | Proof 5: master 4:5 → 4 formats row → 6 hooks grid → Hindi card; S16/S17 + S13/S14/S15 | approved layout / the reveal / labels | layout left zone, reveals right | fit-with-gap | contain (thumbnails whole) | staged reveals; bubble fades at 43.5 |
| 44.5–49.5 | Speed: STANDARD / 24 HOURS (2.6 s) → 4-HOUR EXPRESS + S21 (2.4 s) | the number / label / — | centre-left | — | — | cut |
| 49.5–54.5 | CTA: A1 still contain-anchored right, bubble back, S22 / S23 / S24, Adwisely once | CTA / anchor creative / bubble | CTA left zone | fit-with-gap | contain | stillness; single fade out |

CA-D5 balance: each beat is declared balanced (tone + size weighed: dark ad panel vs light ground offset by the copy
column). CA-D6 aspect: 16:9 master is the platform frame (pack LIMIT: no accepted source treats fixed feed frames —
stated, not forced). CA-D8: no cut sacrifices emotion or story for eye-trace. CA-D9: one speaker, one side; no line
crossing. CA-D10: every hold ≥ 3 s on a hero creative, ≥ 6 s on the video (describable content sets the hold; the fast
norm is the ambient pace we refuse). CA-D11: the only camera move is inside the generated clips (native dolly/push).

Music: V3 Lyria `music-r4` (accepted) re-edited: enters under the speaker's last word, low; lifts at 12.0; steady; out on
the final fade. No narration after the speaker. SFX: two soft ticks (handoff, spotlight steps) at most.

## 4. Deterministic assets (code; no model writes a word)
- Craft ad "YOUR NIGHT ROUTINE, SIMPLIFIED." / pill "15% OFF FIRST ORDER" / "CODE AAROHI15" / button "SHOP NOW" /
  "T&Cs apply" / mark "AAROHI SKIN" on the V3 A2 vanity plate (accepted), 4:5 — the Ledge layout with a CTA button.
- Reuse: V3 master statics (4 sizes), 6 hooks, Hindi 4:5, Brewa packshot + B1 scene, A1/A3 clips (`../v3/gen/**`).

## 5. DOCTRINE_DEVIATIONS
- PA-D9 (hero angle = most surfaces): overridden by the brief clause "direct eye contact / speaker looking into camera" —
  frontal is the only admissible angle.
- CA-D2 (off-centre default): the speaker is centred because the brief needs a symmetrical face crop for the bubble and
  the scene points inward (CF-08, centre allowed when the subject is the sole statement).
- CA-D6: 16:9 chosen by the platform (Upwork player), acknowledged as the pack's declared limit, not a Canon claim.
