# Controller — Gemini models run on the Gemini API key, not Vertex — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.

## Authority — the Controller's words

> **"geminni models from gemini key only"**

## Decision (Writer Controller's reading, to be corrected by the Controller if too narrow or too wide)

1. Every **Gemini-named** model — Gemini image (route `nano-banana-2`, model gemini-3.1-flash-image; `nano-banana-pro`
   and `nano-banana-pro-edit`), Gemini Omni (`gemini-omni-1.1-flash*`), and any Gemini used as a judge (the vision
   screening instrument) — is called through the **Gemini Developer API** (`generativelanguage.googleapis.com`) with the
   key named `GOOGLE_API_KEY` in `~/.mi-keys` (name only; value never printed), billed to that key's account.
2. Veo, Lyria and Imagen are Google models but not Gemini-named; they **stay on Vertex** (service account, credits)
   unless the Controller says otherwise.
3. Effect on the running text-to-video lane: the Gemini Omni draws already dispatched on Vertex before this decision are
   valid evidence of the same model and are kept; from the next run onward Omni dispatches on the Gemini API. The
   surfaces registry gains Gemini-API entries (`surface: gemini_api`, `billing_pool: gemini_key`) and the package rows are
   re-pointed when the adapters land; pricing from the pinned Gemini API pricing page.
4. No spend is implied by this record; each later run keeps its own spend record.
