# ACCEPTANCE CONTRACT V4

The Controller's contract (§25) verbatim governs; the executor's self-check adds the mechanical gates below. "Acceptable"
and "pretty good" are rejects. Required bar: "I would actively want this on the front of the Upwork profile."

## Speaker micro-qualification gate (§9) — before any other new media
Hard fails: robotic cadence; odd/non-Indian or distracting accent; waxy/etched skin; eye wander; unstable pupils;
lip/audio mismatch; weird teeth; changing facial structure; over-articulated mouth; fake smile; awkward gesture loop;
background morphing; stray text; visibly synthetic freeze-frame; line too fast; line read rather than spoken.
Scores /10: FACE NATURALNESS, EYE CONTACT, VOICE NATURALNESS, ACCENT/CREDIBILITY, DELIVERY/PACING, FRAME QUALITY.
Pass only if: no hard fail AND total ≥ 50/60 AND voice ≥ 8 AND face ≥ 8 AND eye contact ≥ 8. Evidence per candidate:
contact sheet at 1 s, extracted audio, transcript check. If no candidate passes: STOP, return candidates.

## Film — the twenty conditions (§25), each with its mechanical or human check
1–3 speaker: human (Controller) by ear and eye; executor pre-score recorded. 4 no clipped text: compositor asserts every
text box inside the safe area, else the render FAILS (`qa/layout-report.json`). 5 readability: compositor measures WCAG
contrast over the real pixels behind every wrapper text box; ≥ 4.5:1 body / ≥ 3:1 display, else FAIL
(`qa/contrast-report.json`). 6 one card radius (26 px) and one bubble shape: tokens only; `qa/layout-report.json` lists
every card and its radius. 7 no accidental crop: every portfolio creative is `contain`; the two native 16:9 assets are
shown at native size; `qa/crop-report.json` lists every placement with its fit mode and the fraction of the source shown
(must be 1.0 unless declared cover). 8 product drift: human on the A1/A3/B1 frames (V3 verdicts stand; re-checked on the
frames actually used). 9 stray lettering: frames of every generated video used are sampled at 0.5 s and inspected
(`qa/frame-scan.md`). 10 hierarchy demo: HOOK → OFFER → CTA shown sequentially, each ≥ 1.5 s. 11 pacing: no hero creative
< 3 s; video ≥ 6 s uninterrupted; no beat < 2 s (`assembly/timeline.json`). 12–13 images 18.5 s vs video 8 s + moving
bubble — both substantial. 14–20 human. Duration 52–56 s. Loudness −14 ± 1 LUFS, TP ≤ −1 dBTP, speaker intelligible,
speaker audio never time-stretched (`qa/audio-report.md`).
