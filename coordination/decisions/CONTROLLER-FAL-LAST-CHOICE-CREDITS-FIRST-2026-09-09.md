# Controller — surface choice in testing: a model available on both fal and GCP is called on GCP (Gemini key / Vertex); fal only for models that exist nowhere else — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.
**Sharpens:** plan §C.3a (credits-first) and `CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09.md`.

## Authority — the Controller's words

> **"vertex and gemini come from gcp. deicsion is fal is the last choice since it costs me money."**

The Writer Controller first read this as a routing preference between different models; the Controller corrected it:

> **"no, i mean in testing. if you want to use a model, and the model exists on fal and geminni key. we use it from gemini key. this way"**

## Decision

1. **Surface choice per model, in testing.** When the same model is offered both on fal and on GCP (the Gemini
   Developer API key or Vertex — both the Controller's GCP credits), the harness calls it on **GCP**. fal is used only
   for models that exist on no GCP surface (today: Kling, Wan, MiniMax, Seedream, FLUX, Qwen, Recraft, the lipsync
   routes). This is about where a given model is called, not about which model is preferred.
2. **Today's package already complies**: Veo, Gemini image, Gemini Omni and Lyria run on Vertex / the Gemini key; no
   Google model is called through fal. The rule is now explicit for every future route pin: before a fal pin is made,
   check the GCP surfaces first and pin there if the model exists.
3. Model preference between different models stays what the blind verdicts say (the routing map); cost is a tie-break
   only, as before.

Not decided here: any spend.
