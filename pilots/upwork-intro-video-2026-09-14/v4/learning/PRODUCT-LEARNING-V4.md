# PRODUCT LEARNING — V4 (commercial showcase pilot; recommendations only, nothing promoted)

## A. Creative-direction failures carried from V3 (Controller-identified) and how V4 answers them
- No point of view → a speaker with one frozen line opens the film (Veo 3.1 Fast native speech, qualified before any other spend).
- Work shown too fast to absorb → nine beats, none under 3.3 s; hero video 8 s uninterrupted; statics 6 s each; 55.3 s total.
- Wall-to-wall narration → speech only in the first 7.75 s; music and six restrained sound events after.
- "Nice generation, where is the advertising thinking?" → Proof 2 (hook → offer → CTA spotlight on a real layout) and Proof 5 (one direction → formats/hooks/Hindi).

## B. Assembly / compositor failures in V3 and the V4 fix (all now deterministic gates, not habits)
- Text clipped (brief card, statement) → `design4.place_text` measures the ink box and raises `LayoutError` outside the safe area; the statement size is chosen by measurement (112 → 96 px) instead of clipping. Caught live twice during the V4 build.
- Text lost on backgrounds (labels over photos, dimmed ground) → wrapper text only on wrapper_bg or a ≥ 94 % tab; WCAG contrast measured over the real pixels behind every box; the gate caught a real collision ("4 FORMATS" over "ONE DIRECTION.") that the eye would have missed at speed.
- Creatives cropped (cover-fit statics, edge-to-edge cards) → `contain`/`native` only; 22 placements, 0 unintended crops; the two declared covers (bubble face, ad-internal plate) are logged with reasons.
- Mixed square/rounded geometry (intake card) → one `card()` with radius 26 on every wrapper card and the bubble; report lists radii used = [26].
- Arrow glyph tofu → no arrows in V4 copy.
- Bundle overflow / hidden mark behind the bubble → measured placement; mark placed relative to the bubble.

## C. Media-model observations (single run; not Registry evidence)
- Nano Banana 2 drew blurred handwriting-like sheets into a "creative studio" scene despite "no readable text" — the prompt must forbid paper/notes/posters explicitly; second draw clean.
- Veo 3.1 Fast i2v + native speech from the same still: framing drifted slightly wider than the still; identity, room and eye contact held; a hand entered the frame edge briefly despite "hands out of frame".
- Gemini Omni 1.1 Flash i2v + native speech: identity and room held; framing widened; script not verbatim (inserted a word) and a synthetic timbre.
- Vertex Veo returned gRPC 14 UNAVAILABLE twice in a row, then succeeded 100 s later: transient, not a request fault.

## D. Audio-model observations
- Sarvam bulbul:v3 narration was rejected by the Controller as robotic (V3) — long narration exposes the cadence that short lines hide; the Lab's 6/6 was on ≤ 70-character lines.
- Veo's native speech on a 22-word line at 8 s reads at ~99 wpm with a natural pause; the full 26-word line would not fit 8 s at that pace — the package's short form was necessary, not optional.
- Omni's native speech at 10 s read at ~108 wpm but was not verbatim.
- Loudness: AAC at 256 kbps adds ≈ 1 dB true-peak overshoot over a limited PCM master; a −2.4 dBFS limiter ceiling is needed for a −1 dBTP delivery.

## E. Capability / evidence gaps exposed
- No Registry or map cell for single-speaker English native speech from an anchored still on Veo/Omni (the Lab's VID-2SPK cells are Hindi dialogue); the pilot now holds two draws (1/1 Veo, 0/1 Omni) — product learning only.
- No evidence on Omni script fidelity; one insertion in one draw is a signal worth a designed test, not a conclusion.
- Provider availability is not part of any route's evidence; a route can be "clean" and unavailable.

## F. Pipeline / system defects and recommendations (for the Controller; none adopted here)
1. **Speaker micro-qualification as a reusable pattern — recommend YES.** One anchor still, one draw per candidate route, contact sheet + audio extraction + transcript + a scored gate before any dependent spend. Cost here USD 4.03 to reach one accepted 8-s speaker; the alternative (building the film first) is what V3 did.
2. **Provider-balance awareness in planning — recommend YES.** V3's cap was 6× the real constraint (fal cash); V4's Wan fallback was structurally dead (USD 0.26). The route plan should carry a live pool read and mark fallbacks callable/not.
3. **Video-frame text scanning in post-draw QA — recommend YES.** V3's B2 clip failed on frames from a clean still; V4 scanned every used clip. The gate's Cloud Vision adapter exists and has never run on a real artifact — this is the first honest use case.
4. **Layout overflow / contrast / crop checks as compositor gates — recommend YES.** In V4 they are functions that raise; the three reports (`qa/layout-report.json`, `contrast-report.json`, `crop-report.json`) are produced by the same code that draws. Two real defects were caught by the gates during the build that the contact sheets did not show.
5. Transient provider errors should be retried under a small, pre-declared allowance (Addendum 1 pattern) rather than counted as route failures.

## G. Spend
Cumulative reserved USD 7.3112 = INR 697.6 of INR 2,000 (V3 3.2836 + V4 4.0276). V4 media actually returned: 2 stills (Gemini API credits), 1 Omni clip, 1 Veo clip (Vertex credits); two Veo operations failed at the provider and are counted conservatively. No fal spend in V4.
