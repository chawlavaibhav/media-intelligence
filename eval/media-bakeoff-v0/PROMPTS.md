# Media bake-off v0: the exact prompts for every arm

**One writer model for every arm.** B1, P and P+Canon use the same model, set once in `HANDOFF.md`. Otherwise a win
could be the model, not the method. Temperature and settings are the default and identical across arms.

The four arms differ **only** as described below. Everything else is identical across arms:
- the media model per class;
- the reference photos;
- the number of draws;
- the finishing code;
- the seeds, where the API allows.

---

## Media model per class (pinned; the same model for every arm within a class)

**Only Google (Gemini API / Vertex) and Azure (Aight subscription) keys are used. fal is not available.** If a primary
route fails, use the fallback for **all** arms of that class and log it. Never use Azure subscription `d3ee8dc2`
(Wherehouse).

| Class | Primary | Fallback | Evidence / note |
|---|---|---|---|
| S1 product ad still | Nano Banana 2 (`gemini-3.1-flash-image`, Gemini API, with the product reference image) | GPT Image 2 (Azure) | NB2 11/12, GPT Image 2 11/12 accepted blind; the P1 poster |
| S2 edit my photo | Nano Banana 2 edit (Gemini API, "change only X, keep everything else the same") | GPT Image 2 edit (Azure) | Seedream (fal) was the Lab's best edit route and is unavailable; NB2 edit is the substitute (weaker evidence) |
| M1 animate my image | Veo 3.1 Fast image-to-video (Gemini API / Vertex), motion-only prompt | Veo 3.1 (standard) image-to-video | Kling/Wan (fal) unavailable; Veo Fast i2v was 5/8 in the Lab, so expect this class to be harder |
| M2 product film, no people | Veo 3.1 Fast image-to-video from approved stills, 8-s scenes | Veo 3.1 (standard) | Mokobara v2 path |
| F1 story film with people | Veo 3.1 Fast, 8-s scenes **with native audio** (text-to-video, or image-to-video from an approved first frame) | Veo 3.1 (standard) | Both direct-Veo wins; Mokobara v2. Two-speaker Hindi: Veo Fast 2/2 in the Lab |
| Music bed (P only, if the writer asks) | Lyria (Vertex) | none | Lab |

**Text models:**
- **Writer:** the model named in the kick-off. Claude Sonnet 5, via `ANTHROPIC_API_KEY` or Claude on Vertex, or else GPT-5.6 Sol on Azure. Use the same model for B1 and P.
- **Understand step:** GPT-5.6 Luna (Azure); fallback Gemini Flash.

Text, logo and end cards are always composed by code in P, never drawn by a model. B0 and B1 get no code finishing:
they are the direct baselines.

## B0: direct (no writer)

Send the customer's verbatim words (plus any answers) **as the prompt**, with the reference photos, to the class's
media model. The vendor's own prompt rewriter stays at its default. Stills get 4 draws; clips get 2.

---

## B1: smart writer, no pipeline

A fresh session of the writer model, with no repo and no files except the brief and the photos:

> You are making this ad for a real customer. Here is their request, word for word, and their photos.
> Write the prompts yourself for {media model}: {stills: one image prompt} / {film: one prompt per 8-second scene,
> with the scene's own sound and at most one short spoken line; 2–3 scenes for 15 s}. Then stop.
> [brief verbatim + answers] [photos]

One draw per prompt, the same as the direct-Veo sessions that beat the kitchen. **For fairness, B1 stills also get
4 draws** of its single prompt. (E09 and E10 reuse the existing direct-Veo films as their B1.)

---

## P: Author + Finish + Choose, without the Canon

**Step 1: Understand** (cheap model, ≤3k tokens). Output JSON: `class`, `format`, `exact_copy[]`, `language`,
`facts[]` (each with a source), `questions[]` (≤2, facts only the customer knows), `refuse_or_rescope` (from
the refusal list in `docs/research/context-engineering-2026-09/MASTER-PLAN.md` §4.2).

**Step 2: Write** (writer model, one call):

> You are one senior creative director and writer, making this whole ad yourself.
> Customer's words (verbatim): … Facts (with sources): … Photos: … Format: …
> How {media model} wants to be prompted: {one-page model style guide, below}.
> For films and hero stills: first give 3 different ideas (a human truth + one moment + a key-frame description).
> Pick the strongest yourself. In the bake-off the pick is automatic; in production the customer picks.
> Then write a ≤150-word treatment, and then, per scene: the prompt in the model's own style, the duration,
> the references to attach, at most one spoken line, and any on-screen copy (copy is added by code later — never ask the model to draw it).
> Output JSON.

**Step 3: Lint** (code, flags only, returned once): stills 30–80 words; video scenes ≤120 words; animate-a-still
prompts describe motion only; no exact-copy or brand strings in image prompts; spoken lines ≤ (scene length − 0.4 s)
at 2.5 words/s.

**Step 4: Generate.** Stills: 4 candidates. Films: whole scenes with native sound, and 2 takes of the riskiest scene
only. Never replace a scene with a still.

**Step 5: Checks** (code; block only on measurements): exact copy and text bounds, OCR for stray lettering, black
frames, audio overlap and loudness, motion present, aspect and duration. On failure, retake that asset once.

**Step 6: Finish** (code): copy, logo, end card, formats, music. **Step 7:** keep all candidates. In the bake-off the
judge sees the best one, chosen by the writer from a contact sheet. The pick rule is the same for P and P+Canon.

---

## P+Canon: the same as P, plus Canon shape v1 in the writer's context (PHASE 2, later; do not run in phase 1)

This is the **only** difference from P, and it applies to steps 2 and 2b:

- **Step 2 context adds:**
  - `canon/shape-v1/REQUIRED-DECISIONS.yaml`: the writer fills these fields after its prose treatment;
  - `canon/shape-v1/GAP-CARD.md`: only the knowledge the Q&A test showed the model lacks;
  - `canon/shape-v1/EXAMPLES.md` + the two accepted templates it points to.
- **Step 2b (new):** after the draft, the same writer answers `canon/shape-v1/AFTER-WRITING-CHECKLIST.yaml` YES or NO,
  quoting its own evidence for each. It revises or keeps each NO with a one-line reason. It never deletes a moment
  and never downgrades motion.
- **Optional lookup:** the writer may name ≤10 claim IDs from `canon/shape-v1/LABEL-INDEX.md` to read in full.
  Log which ones it reads.

**Budget check:** the Canon context must stay under about 4 pages (≈3k tokens), not the old 25k packs. Log the
token count per job.

---

## One-page model style guides (the writer reads these; code never rewrites prompts)

- **Stills** (Nano Banana / GPT Image / Seedream / FLUX):
  - write the subject, then the action, then the setting, then the style, in 30–80 words;
  - state the use ("an Instagram product ad photo of …");
  - use positive phrasing ("clean unmarked surfaces"), not "no X";
  - the product's identity comes from the reference photo; say "the exact product from the reference image" and do not describe it at length.
- **Veo 3.x (text or image to video):**
  - one 8-second scene per prompt: cinematography, subject, one action from start to end, context, style and ambience;
  - the scene's own sound; at most one line in quotes;
  - Google rewrites prompts, so keep them literal.
- **Image-to-video** (Veo i2v / Kling / Wan / Seedance): describe **motion and camera only**, and do not re-describe the image.
