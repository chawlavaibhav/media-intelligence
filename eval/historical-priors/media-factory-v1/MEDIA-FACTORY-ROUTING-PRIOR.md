# Media Factory — Routing Prior

> **Status: historical empirical prior — requires a targeted freshness check before any production use.**
> Learned 2026-07-19/20 (spike + guddu film test) and 2026-07-24 (gallery), on the model versions of that moment
> (nano-banana-pro/edit, seedream v4.5/edit, veo3.1/fast, wan-25-preview, seedance v1 lite, latentsync, sadtalker,
> sarvam bulbul:v3, elevenlabs multilingual v2 / v3, lyria2 — all via fal.ai except Sarvam/ElevenLabs direct).
> A verified 2026-08-13 landscape check already invalidates parts of the price column (Veo Fast now cheap with native
> lip-sync; Seedance 2.x now the expensive quality tier; Kling 3.0 Turbo new volume tier). **Do not read any row as an
> August-2026 capability claim.**

There was **no automated router in code**. The registry (`packages/providers/src/registry.ts`) is an id-lookup; model
selection was env vars (`FAL_IMAGE_ENDPOINT`, `FAL_VIDEO_ENDPOINT`, …) plus adapter capability descriptors
(`supportsSeed`, `acceptsImageInput`, `maxDurationSec`, `nativeAudio`). The table below is the **human-learned policy**
reconstructed from surviving evidence only.

| Requirement / condition | Preferred historical workflow | Avoided workflow | Why | Evidence | Confidence | Freshness risk |
|---|---|---|---|---|---|---|
| On-brand character stills at volume | Ref-sheet-conditioned edit on **Seedream 4.5 edit** ($0.04) | Unconditioned t2i; nano for volume | 90.6% pass, $0.044/accepted, zero identity-drift fails | scores.json + costs.jsonl (n=64 scored) | High (Tier A) | High — seedream version superseded |
| Stills where exact in-scene text/craft matters | **Nano Banana Pro edit** ($0.15) | Seedream for text-critical | Nano's fails were identity, not text; seedream rendered hex codes / dropped wordmarks | scores.json fail notes | Medium-High (Tier A, n=16 text scenes) | High |
| Guaranteed-exact text/logo (contracts, prices, Devanagari) | Textless base + **deterministic composite** (sharp/ffmpeg overlay) | Model-rendered text **in motion** | In-motion text decays/smears (Wan tagline decay; wan_chai-sign built to show it); composite is exact by construction | videos.html caption; gallery pair wan_chai-sign.mp4 vs aight_chai-composite.mp4 | Medium (Tier B) | Medium — stills already reliable in 2026-07; video text may be too by now |
| Hero talking shot, text-light, EN/Hinglish | **Wan 2.5 i2v** native speech (₹42/10s) | Veo by default (₹105/8s) | User-ear-approved at ₹42; Veo demoted to fallback (its only measured edge: in-scene text stays crisp) | videos.html takes; memory C4 | Medium (Tier B/C) | **Very high — Veo pricing/lip-sync changed by Aug 2026** |
| Budget talking shot (narration class) | **LatentSync route**: Seedance idle + TTS wav + LatentSync (₹16–25) | SadTalker (₹10) | Full-frame, character+logo intact, "best ₹20 shot"; SadTalker = 256px crop, reject | artifacts + videos.html verdicts | High for the reject; Medium for the accept (ear-judgment on lips pending) | High |
| Silent b-roll | **Seedance v1 lite** (~₹35/clip) | Wan/Veo for b-roll | Cheap, style-preserving, user-approved by ear | vid_seedance_t1 + idle_seedance; memory C4 | Medium (Tier B/C) | High — Seedance pricing inverted since |
| Narration-over-b-roll vs lips-on-camera | Ration lips-on-camera; Seedance+Sarvam ≈ ₹10 vs Wan ₹42 per shot | Talking heads everywhere | 4× cost difference at equal narrative value | memory (cost-push findings, Tier C); unit prices corroborated by ledger | Medium (Tier C economics on Tier A prices) | Medium |
| Emotional/childlike/stylized art performance | **Wan** (performed the rain scene) | **Veo** — content-filter refusal risk | Veo refused the childlike character design in an emotional scene, both beats, $0 charged | costs.jsonl absence + videos.html caption | High (n=2, consistent) | Medium — policy models change; per-brand pre-flight still the right control |
| Two-person dialogue, single beat, ≤2 turns | Wan i2v from a crisp plate, Hindi + heavy in-prompt voice direction, ages specified | — | Rain scene judged "perfect" / candidate film recipe | s7_hindi_preview.mp4 + videos.html | Medium (Tier B, n=1 scene ×3 iterations) | High |
| Multi-turn dialogue film (>2 turns / chained beats) | **REFUSE or re-scope at intake** | Wan multi-turn; frame-chaining; Wan audio_url as lipsync driver | Lips desync + line bleed; generational decay + per-clip voice drift; dub out of sync | f2_* artifacts + memory C1/C2 (Tier C laws, artifacts survive) | Medium (Tier C) | High — untested on 2026-08 models |
| Indic VO, cheap | Sarvam bulbul:v3, speaker chosen by human ear, + polish chain (loudnorm/room tone) | Auto-picking voice by metric | Ear beat RMS metric (ishita > kavya); raw TTS sounds robotic without speech-rhythm rewrite + mix | vo_* artifacts, videos.html, memory | Medium (Tier B) | Medium |
| Directed/acted VO | ElevenLabs v3 with inline acting tags | EL western voices for Hindi-accent work | v3 acting tags work; western accent rejected by ear even in English | el_sarah_v3.mp3; memory C6 | Medium (Tier B/C) | Medium |
| Take strategy | Generate-1, judge, retry-on-fail | N=3 spray by default | ~90% pass rate makes N=3 wasteful; takes-per-keeper 1.1–1.3 | derived from scores.json; memory cost-push | High (derived from Tier A) | Medium |
| Customer-art ingestion | nano-banana edit clean-plate (de-text + extend to 16:9) | regenerating art from scratch | 12/13 plate keepers, style preserved | film_*_plate.png artifacts (+ memory for the 12/13 count) | Medium (artifacts Tier B, count Tier C) | Medium |
| Production one-shot ads (V2 era) | GPT Image 2 hero ($0.04) + deterministic composite + PixVerse 540p animate | FLUX.2 for Indian-product world knowledge | FLUX invented wrong products; GPT Image 2 "payable" (live-verified) | HANDOFF.md §3; memory C5 (Tier C; no scored corpus survives) | Low-Medium | High |

## What must be freshness-checked before reuse (explicit list)
1. Veo 3.1 Fast price + lip-sync latency + content-policy behavior (the demotion to fallback is likely obsolete).
2. Seedance 2.x cost/quality position (was cheap b-roll; now premium).
3. Whether current video models hold small in-scene text in motion (the composite-always rule for video may be dying the same death the stills rule died).
4. Multi-turn dialogue + voice consistency on current models (the guddu laws are 5+ weeks old and model generations moved).
5. LatentSync-class mouth repaint quality vs current native lip-sync pricing.
