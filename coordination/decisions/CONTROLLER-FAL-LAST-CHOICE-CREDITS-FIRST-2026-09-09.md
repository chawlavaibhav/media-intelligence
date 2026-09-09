# Controller — fal is the last choice; GCP (Vertex or Gemini API) first, because fal costs cash — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.
**Sharpens:** plan §C.3a (credits-first) and `CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09.md`.

## Authority — the Controller's words

> **"vertex and gemini come from gcp. deicsion is fal is the last choice since it costs me money."**

## Decision

1. **Routing preference order at equal acceptance**: GCP first (Vertex or the Gemini Developer API — both draw on the
   Controller's GCP credits, so which of the two carries a Gemini call is a plumbing choice, not a cost choice), then
   other prepaid pools (Sarvam credits, ElevenLabs plan credits), and **fal last** — fal is cash. A fal route is chosen
   only where no GCP/credits route meets the contract, or where the Controller's blind acceptance is materially better.
2. **The routing map encodes this**: the fallback ranking within a question becomes acceptance first, then billing pool
   (credits before cash), then settled cost per trial. Recorded as rule RR-0 in `ROUTING-EVIDENCE-MAP-v0`.
3. **Testing order**: future pieces run the GCP routes first and fal routes only where the GCP routes leave the question
   open; caps are sized to the GCP rows plus the fal rows the Controller explicitly keeps.
4. The Gemini-key decision stands as written (Gemini-named models via the Gemini API), understood as GCP either way.

Not decided here: any spend.
