# V3 asset inventory for V4 (§13) — classified before any new showcase media

| V3 asset | V3 verdict | V4 class | V4 use |
|---|---|---|---|
| `gen/stills/a0-accepted.png` Aarohi packshot 4:5 | accept | KEEP | source photo reference (bundle/CTA anchor if needed) |
| `gen/stills/a1-accepted.png` Aarohi hero still 16:9 | accept | KEEP_WITH_NEW_COMPOSITION | plate of the master static; CTA anchor |
| `gen/stills/a2-accepted.png` Aarohi vanity 4:5 | accept | KEEP_WITH_NEW_COMPOSITION | plate of the Proof-2 craft ad (new deterministic layout with SHOP NOW) |
| `gen/stills/a3-accepted.png` Aarohi festive 16:9 | accept (note) | KEEP | source of the A3 motion only |
| `gen/video/a1-accepted.mp4` Kling hero 5.04 s | accept | KEEP | Proof 4, full screen, native 1920x1080 |
| `gen/video/a3-accepted.mp4` Kling festive 4.04 s | accept (petals note) | KEEP | Proof 4 second shot, first 3.0 s |
| `gen/video/a2-accepted.mp4` Kling vanity 4:5 | accept | NOT_NEEDED | (no 4:5 motion slot in V4) |
| `gen/stills/brewa0-accepted.png` kettle packshot | accept | KEEP | Proof 3 source (contain) |
| `gen/stills/b1-accepted.png` kettle kitchen 16:9 | accept | KEEP | Proof 3 result (native, no crop) |
| `gen/video/b1-accepted.mp4` Kling kettle | accept | NOT_NEEDED | V4 Proof 3 is a still→still transformation; motion is Proof 4's job |
| `gen/stills/b2-*.png`, `b3-*.png`, `gen/video/b2-r1.mp4` | b2/b3 stills accept; b2 clip reject | NOT_NEEDED / REJECT | not used |
| `gen/stills/kora-accepted.png`, Kora hooks | accept | NOT_NEEDED | V4 has no Kora slot (Proof 5 is Aarohi-only by the package) |
| `gen/stills/dhaba-accepted.png`, Dhaba 4:5/WA | accept (r2) | NOT_NEEDED | Hindi proof in V4 is the Aarohi Hindi card |
| `gen/deliverables/aarohi-master-{4x5,1x1,9x16,wa}.png` | code | KEEP | Proof 1 (4x5), Proof 5 formats, CTA anchor |
| `gen/deliverables/aarohi-hook-{1..6}-4x5.png` | code | KEEP | Proof 5 hooks |
| `gen/deliverables/aarohi-hindi-4x5.png` | code | KEEP | Proof 5 Hindi |
| `gen/deliverables/aarohi-video-ad-9x16.mp4` | code | NOT_NEEDED | (no vertical-ad slot; avoids a phone frame) |
| `gen/audio/music-r4.wav` Lyria 2 32.8 s | accept | KEEP_WITH_NEW_COMPOSITION | re-edited: enters under the speaker's last word, one loop with crossfade |
| `gen/audio/vo-*.wav` Sarvam narration | Controller: robotic | REJECT | no narration in V4 |
| V3 assembly / layout / tools (`film3.py`, `compose.py` wrapper parts) | Controller: reject | REJECT as a template | rebuilt (`design4.py`, `film4.py`); `adcomp.text` (hb-view rasteriser) reused as a library |
