# Bake-off v1: test design, flows, Canon shape and exact prompts

**Status:** for founder approval. Nothing runs until he says GO. This file supersedes `PROMPTS.md`, and
`HANDOFF.md` points here.

**Founder's ruling, 26 Sep:** drop "customer words straight to the media model". Anyone making media runs the request
through a strong LLM first, so the baseline is **LLM + media model**. That leaves three arms.

| Arm | Name | In one line |
|---|---|---|
| **A** | LLM + media model | A strong LLM turns the brief into media prompts, and the media model makes the output. What anyone can do with ChatGPT or Claude today |
| **B** | Our pipeline | Understand → one writer with ideas, per-model style guides and structured scenes → lint → generate with takes → measurement checks → code finishing → pick |
| **C** | LLM + Canon + our pipeline | B, plus the reshaped Canon in the writer's context, a Canon lookup, and an after-writing checklist pass |

**The only differences between arms:**
- **A → B:** the pipeline.
- **B → C:** the Canon.

**Kept identical across all arms:**
- the briefs, reference photos and answers;
- the writer LLM (the same model and settings);
- the media model per class;
- the seeds, where the API allows.

---

## 1. Shared settings

**Writer LLM (all arms):** Claude Sonnet 5.
- The gap card measured *Claude's* knowledge gaps, so a Claude writer is the fair test of the Canon.
- If the founder picks GPT-5.6 Sol instead, arm C still runs, but the gap card is then an unmeasured proxy. Log this.

**Understand step (B and C):** GPT-5.6 Luna (Azure); fallback Gemini Flash.

**Librarian (C only):** the writer model, one call.

**Media models.** Google and Azure only; no fal. The same model for every arm within a class.

| Class | Primary | Fallback |
|---|---|---|
| S1 product ad still | Nano Banana 2 (`gemini-3.1-flash-image`) with reference photos | GPT Image 2 (Azure) |
| S2 edit my photo | Nano Banana 2 edit | GPT Image 2 edit (Azure) |
| M1 animate my image | Veo 3.1 Fast image-to-video | Veo 3.1 |
| M2 product film, no people | Veo 3.1 Fast image-to-video from stills | Veo 3.1 |
| F1 story film with people | Veo 3.1 Fast, 8-s scenes with native audio | Veo 3.1 |
| Music (B and C only, if the writer asks) | Lyria (Vertex) | none |

**Draw budget, so that arms differ by method, not by luck:**

| | A | B | C |
|---|---|---|---|
| Stills (S1, S2) | 4 draws | 4 draws | 4 draws |
| Animate (M1) | 2 takes | 2 takes | 2 takes |
| Films: takes per scene | 1 take per scene + 1 retake of the scene the LLM thinks is riskiest | 1 take per scene + 1 retake of the riskiest scene | same as B |
| Who picks the shown candidate | the same writer LLM, from a contact sheet | the writer, from a contact sheet | same as B |

A, B and C get **the same number of media calls** per brief, and the same kind of pick. So B or C winning over A means the method worked, not that it got more tries.

**Finishing:** A gets none. It is shown exactly as the LLM plus the media model made it: whatever text the model drew, and no logo overlay. B and C get code finishing. **This difference is part of what is being tested,** because it is part of what the pipeline adds.

---

## 2. Arm A: LLM + media model

```
brief (verbatim + answers + photos)
  → [A1] writer LLM: write the media prompts            (1 call)
  → [A2] media model: generate (draw budget above)
  → [A3] writer LLM: pick the best take per scene / the best still from a contact sheet (1 call)
  → (films) concatenate the scenes in the order the LLM gave; no other editing
  → OUTPUT
```

**A1 prompt (writer):**
```
You are a skilled creative who makes ads with AI tools. A customer sent this request.

CUSTOMER REQUEST (verbatim):
{brief_verbatim}
{answers_if_any}
PHOTOS ATTACHED: {n} reference image(s) of the product/customer assets.

Make this ad using {media_model_name}. {format_line}
- For a still: write ONE image prompt (the photos will be attached as references).
- For an edit: write ONE edit instruction for the attached photo.
- For animate-my-image: write ONE image-to-video prompt for the attached still.
- For a film of {duration} s: write one prompt per scene; each scene is one {scene_len}-second clip with its own sound.
  Include any spoken words in quotes. Say which scene is riskiest to generate.

Return JSON: {"prompts":[{"scene":1,"prompt":"...","duration_s":8}], "riskiest_scene":n, "notes":"..."}
```

**A3 prompt (pick):**
```
Here is a contact sheet of the takes generated for this ad, labelled. Customer request (verbatim): {brief_verbatim}
Pick the take for each scene (or the one still) that best serves the request. Return JSON {"picks":{...}}. One line of reason each.
```

---

## 3. Arm B: our pipeline (no Canon)

```
brief (verbatim + answers + photos)
  → [B1] understand (cheap LLM)        → class, format, exact copy, language, facts with sources, ≤2 questions,
                                          refuse/rescope
  → [B2] writer: 3 ideas → pick 1 → treatment → scenes (JSON)            (1 call)
  → [B3] lint (code): flags only → back to the writer ONCE if any flag    (≤1 extra call)
  → [B4] generate (draw budget above; the first frame is a still where the class needs one)
  → [B5] measurement checks (code): exact copy absent from pixels, OCR stray text, black frames, motion present,
          audio overlap/loudness, aspect/duration → a failure = one retake of that asset (inside the draw budget)
  → [B6] writer picks takes from the contact sheet (same pick prompt as A3)
  → [B7] finishing (code): exact copy + logo + end card + format + music bed (if asked) + voice timing check
  → OUTPUT
```

In the bake-off there is no customer to answer questions. The briefs already carry the customer's answers, and B1's
questions are logged, not asked.

**B1 prompt (understand):**
```
Read this customer request and return JSON only.
REQUEST (verbatim): {brief_verbatim}  ANSWERS: {answers}  PHOTOS: {photo_descriptions_or_count}
Return:
{"class": one of [S1_product_ad, S2_edit, M1_animate, M2_product_film, F1_story_film],
 "format": {"aspect":"9:16|1:1|4:5|16:9","duration_s":n},
 "exact_copy": [strings that must appear exactly, e.g. brand name, offer, CTA, handle],
 "language": "...",
 "facts": [{"fact":"...","source":"customer words|photo|website"}],
 "questions": [at most 2, only facts only the customer knows],
 "refuse_or_rescope": null or "one sentence" (use the list below)}
Refuse/rescope list: back-and-forth dialogue drama; lip-sync onto existing footage; >30 s films needing shots to match;
real/celebrity likeness; drawing a product we have no photo of (rescope: use the photo); hands operating small product
parts (rescope: show before/after).
```

**B2 prompt (writer):** the core of the pipeline.
```
You are one senior creative director and writer making this whole ad yourself, start to finish.

CUSTOMER REQUEST (verbatim — the loudest thing here): {brief_verbatim}
ANSWERS: {answers}
UNDERSTANDING: {B1 json}
PHOTOS: attached as references. The product must look exactly like them; never describe it at length.
MEDIA MODEL: {media_model_name}.  HOW THIS MODEL WANTS TO BE PROMPTED:
{style_guide_for_class}          ← one page, section 5 below

Do this in order:
1. IDEAS. Write 3 genuinely different ideas. Each = a human truth + one specific moment where this product matters
   + a one-line key-frame description. At most one may have no people. Pick the strongest and say why in one line.
2. TREATMENT. ≤150 words of plain prose for the chosen idea: what we see and hear, start to finish.
3. SCENES (films) / FRAME (stills). For each scene: the prompt written in this model's own style (section 5 rules),
   duration, which reference photos to attach, at most one spoken line in quotes (≤ 2.5 words per second of the scene,
   minus 0.4 s), and any ON-SCREEN COPY — copy is added by code afterwards, so NEVER ask the model to draw text, logos
   or brand names. Mark the riskiest scene.
4. FINISH NOTES. Where the copy/logo/end card go, and whether a music bed is wanted (one line of mood if yes).

Return JSON:
{"ideas":[{"truth":"","moment":"","key_frame":""}x3], "chosen":0, "why":"",
 "treatment":"",
 "scenes":[{"n":1,"prompt":"","duration_s":8,"references":["photo1"],"spoken":"" ,"on_screen_copy":[],"first_frame_still_prompt":""}],
 "riskiest_scene":n, "finish":{"copy_placement":"","end_card":"","music":""}}
```

**B3 lint:** code checks the writer's JSON and returns it **once**. Code never edits a prompt.
- **Word budgets:** stills 30–80 words; video scenes ≤120 words; animate prompts ≤40 words.
- **Animate prompts** describe motion and camera only: no re-description of the image.
- **No exact-copy strings or brand names** inside image or video prompts.
- **Spoken lines fit the scene.**
- **No "no X" sentences:** rephrase positively.

**The lint message returned to the writer:**
```
These items need fixing before generation (code checks, not opinions): {list}. Return the corrected JSON only.
```

---

## 4. Arm C: LLM + Canon + our pipeline

It is **identical to B**, plus three additions: C0 (the Canon lookup), extra context in C2, and C2b (the checklist pass).

```
brief
  → [B1] understand (same as B)
  → [C0] LIBRARIAN (Canon lookup): the writer model reads the label index, picks ≤10 claim ids for THIS brief
          → code fetches those claims' full text                                      (1 call)
  → [C2] writer = B2 prompt + CANON BLOCK (below)                                      (1 call)
  → [C2b] CHECKLIST PASS: the same writer answers 15 yes/no questions on its own draft, revises  (1 call)
  → [B3]–[B7] exactly as B
  → OUTPUT
```

### 4.1 The Canon shape used (all in `canon/shape-v1/`; the 1,300-claim library is unchanged)

| Piece | What it is | How C uses it | Size |
|---|---|---|---|
| 1. Required decisions | 8 decisions (idea in one sentence, conflict, hero and brand roles, the first 2 s, brand moments, the ask and the ending, product facts with sources, declared deviations), plus 5 per scene (feeling, first frame containing the idea, one action, new information, impact at phone size) | Added to the C2 output JSON: the writer must fill them | about 640 words |
| 2. Gap card | 25 rules the Q&A test showed Claude does **not** know by itself: Indian audience (8), idea and copy (4), proof and persuasion (4), picture (4), film and type (3), brand (2) | Always in the C2 context | about 1,180 words |
| 3. After-writing checklist | 15 yes/no questions built from the claims producers reused on 3+ jobs and the writer-side failure-atlas modes | The C2b pass. It **never blocks** and never deletes a moment | about 620 words |
| 4. Label index | 1,300 lines, `sk_id \| topic` | Read **only** by the librarian (C0), never by the writer | about 25k tokens, in C0 only |
| 5. Examples | Accepted work with the founder's verdict | The C2 context gets **one** example matching the class, as an excerpt (films: the Mokobara v2 skeleton, direction layer and structure, ≤800 words). Stills: none yet (no accepted still template exists) | ≤800 words |

**Total Canon in the writer's context:** about 6k tokens (pieces 1, 2 and 5, plus ≤10 looked-up claims). The old packs were 25k.

### 4.2 Canon lookup (C0, the "librarian")

This uses the method that won the retrieval test: an LLM scanning a compact index. Keyword and embedding search scored
near random on this corpus.

```
You are the librarian for an ad-making AI. Below is an index of 1,300 short claims from advertising, film, design,
photography and Indian-marketing books (one per line: id | topic).

CUSTOMER REQUEST (verbatim): {brief_verbatim}
CLASS: {class}

Pick AT MOST 10 claim ids whose full text would most change a real decision for THIS ad (idea, story, humour, brand
presence, short-form hook, shots/edit, character, showing the product, on-screen text, Indian audience).
Prefer specific over generic; skip anything the writer surely knows. Return JSON {"ids":[...], "why":{"id":"≤10 words"}}.

INDEX:
{LABEL-INDEX.md}
```

Code then fetches each chosen claim's `claim` text (plus its `concept_label` and source) from
`canon/knowledge/current/*/source-knowledge.yaml` and passes them to C2. It logs the IDs chosen and the tokens used.

### 4.3 C2: the B2 prompt with the Canon block inserted after STYLE GUIDE

```
CRAFT NOTES FROM OUR LIBRARY (use them as a sharp colleague's notes — they never override the customer's words, and
you may depart from any with a one-line reason):

A. WHAT THE MODEL USUALLY DOESN'T KNOW (gap card):
{GAP-CARD.md body}

B. CLAIMS THE LIBRARIAN PULLED FOR THIS BRIEF:
{≤10 claims: [id] topic — claim text}

C. WHAT GOOD LOOKED LIKE (one accepted piece; learn the level, do not copy its story, casting, setting or music):
{example excerpt}

ADDITIONAL OUTPUT — fill after your treatment:
"decisions": {REQUIRED-DECISIONS fields: D1_idea, D2_conflict, D3_roles, D4_opening, D5_brand, D6_ask_and_end,
              D7_product_truth, D8_deviations},
and per scene: "feeling", "first_frame", "one_action", "new_information", "impact".
```

### 4.4 C2b: the checklist pass (one call, the same writer)

```
Here is your draft (JSON) for this ad and the customer's request (verbatim). Answer each question YES or NO,
quoting the line of your draft that proves it. For every NO, either revise the draft or keep it with a one-line reason
(e.g. "the customer asked for no logo"). You may NOT delete a scene's moment or replace motion with a still to satisfy
a question. Return the full revised JSON plus "checklist":[{"id","answer","evidence","action"}].

{AFTER-WRITING-CHECKLIST.yaml questions C01–C15}
```

---

## 5. Model style guides (the one page the writer reads in B and C)

A does **not** get these: it is the plain LLM baseline.

- **Stills** (Nano Banana 2 / GPT Image 2):
  - subject → action → setting → style, in 30–80 words;
  - state the use ("an Instagram product ad photo of …");
  - positive phrasing ("clean, unmarked surfaces"), not "no X";
  - the product comes from the reference photo: "the exact product shown in the reference image", not a long description;
  - leave a calm area where the copy will go, and name where it is.
- **Edit:** "Change only {X}. Keep everything else exactly the same: the product, its colours, its label, the framing."
- **Veo 3.1:**
  - one 8-second scene per prompt: cinematography → subject → one action from start to end → setting → style and ambience;
  - the scene's own sound (ambience, effects), with spoken words in quotes, at most one short line;
  - keep it literal, because Veo rewrites prompts;
  - the same character description, word for word, in every scene;
  - image-to-video from a still: describe **motion and camera only**, and don't re-describe the image.

---

## 6. What the founder judges, and the pre-registered rules

**Pairs per exam brief** (12 briefs):
- B vs A;
- C vs B;
- C vs A.

That is 36 pairs plus about 4 swapped repeats, around 35 minutes: blind, sides randomised, phone-size, with sound.

**Per pair:** which would you rather pay for (5-point scale); "would you pay the anchor price?" for each; and a one-tap reason if no.

**Decisions (fixed now, before any output exists):**

| Question | Rule |
|---|---|
| Does the pipeline beat LLM + model? (the golden benchmark) | **B vs A:** a class ships the pipeline if B wins ≥ 2/3 of that class's pairs. Otherwise that class ships "A + our finishing". Overall, the pipeline "beats direct" only if the better of B or C wins ≥ 8 of 12 against A **and** its would-pay rate is ≥ 20 points above A's |
| Does the Canon help? | **C vs B:** keep the Canon in the writer's context only if C wins more pairs than it loses **and** at least 7 of 12. That earns a 30-brief confirmation run. Otherwise the Canon stays out of the writer's context |
| Cost and time | Record CpAO and TpAO per arm. The pipeline's cost per round should be ≤ 1.5 × A's |

With 12 briefs these are **directional** screens for large effects, not proof.

---

## 7. Cost (estimate; confirmed against the price book before spending)

| Part | Rough cost |
|---|---|
| Practice (T1–T4, B and C) | about $8 |
| Stills-type exam (E01–E07) × 3 arms | about $20 (the animations on Veo are the main cost) |
| Films (E08–E12) × 3 arms | about $45 (about 3 scenes + 1 retake × 3 arms × 5 films) |
| LLM calls (writer, librarian, checklist, understand, picks) | about $4 |
| **Total** | **about $77. Proposed cap $85**, released per step |

A is generated fresh with the same writer for all 12 briefs. The older direct-Veo films were made by a different
session and model, so they are kept only as reference.
