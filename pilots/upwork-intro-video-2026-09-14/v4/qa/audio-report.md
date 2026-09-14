# Audio report — V4 master `assembly/v4/upwork-intro-v4.mp4`

- Speaker: `gen/speaker/speaker-accepted.mp4` (Veo 3.1 Fast native audio), used 0.000–7.750 s, **no time-stretch, no pitch change**; speech span 0.46–7.40 s.
- Transcript (triage model, `qa/speaker/veo-r3-transcript.json`): "Everyone can make AI ads now. So the bar went up. You need more creative, faster." — verbatim to the permitted short form; pause after "So the bar went up." = 0.76 s (waveform); ~99 wpm; accent Indian English; naturalness 9/10; defects [].
- Music: V3 Lyria `music-r4.wav` (accepted), enters at 7.0 s under the last word, one 3-s crossfade loop, bed compressed (4:1) and side-chain ducked under speech, out over the final 2.4 s. No narration after the speaker.
- SFX: one soft air at the handoff, five ticks (three hierarchy steps, two speed cards). Nothing else.
- Loudness (ffmpeg ebur128 on the encoded master): **I:         -14.9 LUFS**, **Peak:       -2.0 dBFS** (true peak), LRA:         5.4 LU. Gain applied 9.7 dB before a true-peak limiter at −2.4 dBFS; AAC 256 kbps adds ≈ +1 dB overshoot, hence the −2 dBTP ceiling. No clipping (sample peak −2.24 dBFS).
- Target was "roughly −14 LUFS": measured −14.9 LUFS. Speech is normalised to −15 LUFS on its own; the bed sits ≈ 9 LU under it while she speaks.
