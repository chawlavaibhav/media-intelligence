# Prompt-Enrichment Evidence

Question investigated: **does any surviving evidence show `raw brief → Claude/LLM → enriched prompt → media model → artifact`, and is there a raw-vs-enriched paired comparison?**

## Headline answer

- **No controlled raw-vs-enriched A/B exists anywhere in the surviving record.** Claim 7 ("Claude enrichment before Wan materially improved output") is **NOT RECOVERABLE** as a proven effect.
- **No runtime enrichment logs survive.** Neither the spike harness nor production logged LLM inputs/outputs for prompt construction. The production DB (`data/adwisely.db`, tables `customers/orders/sessions`) may hold receptionist-era briefs but contains customer PII and was not extracted (access also blocked by the session's permission policy); it postdates and does not cover the Wan experiments anyway.
- What *does* survive is of two kinds, both real but weaker than an A/B:

## 1. The enrichment *pipeline* existed in production code (mechanism, not outcomes)

Chain (fully recoverable from code, no outputs preserved):

1. **Raw customer message** (WhatsApp) →
2. **LLM "creative director"** — `packages/whatsapp/src/receptionist.ts` `converse()`: system prompt instructs the model to convert a chat into `productVisual` (photographer's description, never the shop name), a tightened 3–7-word `headline`, `occasion`, `category`, `cta`. LLM = OpenAI `gpt-4o-mini`→`gpt-4o` in production (`llm.ts` `llmFromEnv` prefers OpenAI; an Anthropic client exists as fallback — so production enrichment was **not** actually Claude) →
3. **Category craft templates** — `packages/whatsapp/src/categories.ts` fills `scene`/`cta`/`style` per business type →
4. **Recipe prompt template** — `packages/recipes/src/{static-ad,video-ad,campaign}.ts`: `"Editorial commercial advertising photograph of {{brief.productVisual}} … {{brief.scene}} … no text, no lettering, no logos"` →
5. **Media model** (GPT Image 2 hero → PixVerse animate).

Recorded (memory, Tier C) as the fix that took output from "generic wrong sweets" to a "payable" kaju-katli ad — but the before/after artifacts were not preserved.

## 2. The spike's "enrichment" was Claude-in-the-loop *authoring*, not a runtime step

Every surviving spike prompt (`run.mjs`, `film.mjs`, `film2.mjs`, `scene7.mjs`) is a heavily crafted final prompt committed in source: character sheet references, palette hexes, exact-spelling demands, per-voice casting notes ("LOW and warm, NOT shrill"), style-lock clauses. These were authored in Claude Code sessions from the raw brand brief (`spike/brand.json`, `spike/guddu/` pages) — the working-style memory `script-before-pixels` records the discipline ("prove understanding, perfect the words at ₹0, then generate"). The intermediate drafts were not preserved; only the final prompts and their artifacts survive.

## Closest surviving *pairs* (directional, operator-judged — not controlled A/Bs)

| # | Same input | Version 1 | Version 2 | What changed in the prompt | Operator verdict (videos.html) |
|---|---|---|---|---|---|
| P1 | `film_s07_plate.png` (rain scene) | `s7_preview.mp4` — Wan, English dialogue, basic voice cues | `s7_hindi_preview.mp4` — Wan, Hindi lines + heavy voice direction ("directed low and heavy"), ages in prompt | Language + explicit voice/age direction | v1 = "the verdict piece"; v3 = "the candidate recipe for the whole film" — direction judged materially better |
| P2 | `film_s07_plate.png` | `s7_preview.mp4` (native Wan voices) | `s7_dub_preview.mp4` (ElevenLabs acted audio, Wan performing *to* the track) | Moved voice out of the prompt into an audio track | Dub out of sync (memory law: audio_url ≠ lipsync driver) — prompt-native voices won |
| P3 | chai-stall gallery scene | `nano_chai-headline.png` (prompt demands in-scene Devanagari headline) | `nano_chai-textless.png` (prompt demands *no* text) → composite | Text-in-prompt vs textless+overlay | Built as the website's own comparison; textless+composite is the one shipped as "the Aight way" |
| P4 | Sarvam VO script | first-attempt VO ("robotic") | speech-rhythm rewrite + speaker test + polish (`vo_kavya_mix`, `vo_ishita_mix`) | Script rewritten for the ear (short phrases, questions, ellipses) | Recorded as the fix for robotic TTS (memory Tier C; artifacts survive) |
| P5 | film v1 vs v2 on same plates | `film_sNN.mp4` — ambient-motion prompts, no dialogue | `f2_sNN_bN.mp4` — performed multi-turn dialogue prompts | Minimal motion prompt vs performed-scene prompt | v2 multi-turn broke (desync/decay laws) — richer prompt ≠ better when it exceeds model grammar |

**Reading for media-intelligence:** treat "LLM enrichment helps" as *plausible and directionally supported* (P1, P4, and the production mechanism were all kept after iteration), but **unproven** — no same-seed raw-vs-enriched generation pair exists. P5 is the counterweight: enrichment beyond the model's performable grammar actively hurt. If the effect matters to the new project, it needs a fresh controlled experiment; nothing here answers it.

## Where each item lives
- Production chain: `media-factory/packages/whatsapp/src/{receptionist,llm,categories}.ts`, `media-factory/packages/recipes/src/*.ts` (copies of the recipes' prompt templates are embedded in EVIDENCE-MANIFEST.json rows' source references; scripts copied under `source-copies/`).
- Pairs P1/P2: `selected-media/videos/s7_preview.mp4`, `s7_hindi_preview.mp4`, `s7_dub_preview.mp4`.
- Pair P3: `selected-media/gallery/`.
- Pair P4: `selected-media/voices/`.
- Pair P5: `selected-media/videos/film_s07.mp4` vs `f2_s02_b1.mp4`/`f2_s02_b2.mp4`.
