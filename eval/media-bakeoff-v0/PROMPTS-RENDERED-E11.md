# Every prompt, rendered for E11 (F1_story_film)

Rendered by `render_prompts.py` from `TEST-FLOWS.md` + `canon_context.py`. This is exactly what each model receives.

## ARM A: LLM + media model

### A1 → writer

```
You are a skilled creative who makes ads with AI tools. A customer sent this request.

CUSTOMER REQUEST (verbatim):
make an ad for a indianised ramen bar. my girlfriedn has started- making ramen wih indiian fusiin)flavours)
ANSWERS: video, mousi kitchen, ramen tandoori, ramen cream and onion, ramen punjabi, ramen tadka and ramen afghani; no photos, make them yourself. home delivery on instagram; use a placeholder handle, gurgaon
PHOTOS ATTACHED: 0 reference image(s) of the product/customer assets.

Make this ad using Veo 3.1 Fast (8-second scenes with native audio; first frames by Nano Banana 2). Format: vertical 9:16, 15 seconds.
- For a still: write ONE image prompt (the photos will be attached as references).
- For an edit: write ONE edit instruction for the attached photo.
- For animate-my-image: write ONE image-to-video prompt for the attached still.
- For a film of 15 s: write one prompt per scene; each scene is one 8-second clip with its own sound.
  Include any spoken words in quotes. Say which scene is riskiest to generate.

Return JSON: {"prompts":[{"scene":1,"prompt":"...","duration_s":8}], "riskiest_scene":n, "notes":"..."}
```

### A3 → writer (pick, after generation)

```
Here is a contact sheet of the takes generated for this ad, labelled. Customer request (verbatim): make an ad for a indianised ramen bar. my girlfriedn has started- making ramen wih indiian fusiin)flavours)
Pick the take for each scene (or the one still) that best serves the request. Return JSON {"picks":{...}}. One line of reason each.
```

## ARM B: our pipeline

### B1 → understand model

```
Read this customer request and return JSON only.
REQUEST (verbatim): make an ad for a indianised ramen bar. my girlfriedn has started- making ramen wih indiian fusiin)flavours)  ANSWERS: video, mousi kitchen, ramen tandoori, ramen cream and onion, ramen punjabi, ramen tadka and ramen afghani; no photos, make them yourself. home delivery on instagram; use a placeholder handle, gurgaon  PHOTOS: none supplied
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

### B2 → writer

```
You are one senior creative director and writer making this whole ad yourself, start to finish.

CUSTOMER REQUEST (verbatim — the loudest thing here): make an ad for a indianised ramen bar. my girlfriedn has started- making ramen wih indiian fusiin)flavours)
ANSWERS: video, mousi kitchen, ramen tandoori, ramen cream and onion, ramen punjabi, ramen tadka and ramen afghani; no photos, make them yourself. home delivery on instagram; use a placeholder handle, gurgaon
UNDERSTANDING: {produced at run time by B1}
PHOTOS: none supplied — invent the food/product look yourself, and keep it identical across scenes by repeating one fixed description word for word.
MEDIA MODEL: Veo 3.1 Fast (8-second scenes with native audio; first frames by Nano Banana 2).  HOW THIS MODEL WANTS TO BE PROMPTED:
- **Veo 3.1:**
  - one 8-second scene per prompt: cinematography → subject → one action from start to end → setting → style and ambience;
  - the scene's own sound (ambience, effects), with spoken words in quotes, at most one short line;
  - keep it literal, because Veo rewrites prompts;
  - the same character description, word for word, in every scene;
  - image-to-video from a still: describe **motion and camera only**, and don't re-describe the image.

Do this in order:
1. IDEAS. Write 3 genuinely different ideas. Each = a human truth + one specific moment where this product matters
   + a one-line key-frame description. At most one may have no people. Pick the strongest and say why in one line.
2. TREATMENT. ≤150 words of plain prose for the chosen idea: what we see and hear, start to finish.
3. SCENES (films) / FRAME (stills). For each scene: the prompt written in this model's own style (the style notes above),
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

### B3 → lint message (only if code flags something)

```
These items need fixing before generation (code checks, not opinions): {list}. Return the corrected JSON only.
```

(B6 pick = the same as A3.)

## ARM C: LLM + Canon + our pipeline

### C0 → librarian (the full label index is appended)

```
You are the librarian for an ad-making AI. Below is an index of 1,300 short claims from advertising, film, design,
photography and Indian-marketing books (one per line: id | topic).

CUSTOMER REQUEST (verbatim): make an ad for a indianised ramen bar. my girlfriedn has started- making ramen wih indiian fusiin)flavours)
ANSWERS: video, mousi kitchen, ramen tandoori, ramen cream and onion, ramen punjabi, ramen tadka and ramen afghani; no photos, make them yourself. home delivery on instagram; use a placeholder handle, gurgaon
CLASS: F1_story_film

Pick AT MOST 10 claim ids whose full text would most change a real decision for THIS ad (idea, story, humour, brand
presence, short-form hook, shots/edit, character, showing the product, on-screen text, Indian audience).
Prefer specific over generic; skip anything the writer surely knows. Return JSON {"ids":[...], "why":{"id":"<=10 words"}}.

INDEX:
… (the 1,300-line label index follows — canon/shape-v1/LABEL-INDEX.md)
```

**Librarian picks used below:** sk_ctg_0013, sk_whip_0011, sk_abcd_0007, sk_conv_c003_0018, sk_ogx_0041, sk_mla_0018, sk_nnn_0019, sk_abcd_0017, sk_abcd_0010, sk_abcd_0021

### C2 → writer (the B2 prompt with the Canon block inserted — the complete prompt)

```
You are one senior creative director and writer making this whole ad yourself, start to finish.

CUSTOMER REQUEST (verbatim — the loudest thing here): make an ad for a indianised ramen bar. my girlfriedn has started- making ramen wih indiian fusiin)flavours)
ANSWERS: video, mousi kitchen, ramen tandoori, ramen cream and onion, ramen punjabi, ramen tadka and ramen afghani; no photos, make them yourself. home delivery on instagram; use a placeholder handle, gurgaon
UNDERSTANDING: {produced at run time by B1}
PHOTOS: none supplied — invent the food/product look yourself, and keep it identical across scenes by repeating one fixed description word for word.
MEDIA MODEL: Veo 3.1 Fast (8-second scenes with native audio; first frames by Nano Banana 2).  HOW THIS MODEL WANTS TO BE PROMPTED:
- **Veo 3.1:**
  - one 8-second scene per prompt: cinematography → subject → one action from start to end → setting → style and ambience;
  - the scene's own sound (ambience, effects), with spoken words in quotes, at most one short line;
  - keep it literal, because Veo rewrites prompts;
  - the same character description, word for word, in every scene;
  - image-to-video from a still: describe **motion and camera only**, and don't re-describe the image.

CRAFT NOTES FROM OUR LIBRARY (use them as a sharp colleague's notes — they never override the customer's words, and
you may depart from any with a one-line reason):

A. WHAT THE MODEL USUALLY DOESN'T KNOW (gap card):
# Gap card: what the writer does not know by default

These are the rules a strong writer model got wrong or left out when answering from memory. Each one changes a concrete decision on an Indian SME or D2C ad.

## Indian audience
1. Draw deities with soft, unmuscled bodies and tranquil faces, eyes looking straight out at the viewer, and iconography correct for the region (e.g. Lakshmi standing in the north, seated in the south). Avoid an angry, muscular Ram, which has carried political connotations since the late 1980s. (Jain; jgb_0003, jgb_0016, jgb_0013, jgb_0021, jgb_0004)
2. For pan-India reach, let the image carry the message with minimal text, because choosing a language cuts the audience. Plan one brand core with regional nuance, as if the regions were separate countries. (Dwyer/Patel, Pandey; dpci_0012, dpci_0022, ppm_0007)
3. Tie discretionary buys to an occasion. Sell wedding and festival spends on social return (face, status), and everyday buys on paisa-vasool value. A small free extra makes the purchase feel complete, even for affluent buyers. (Desai; dmpl_0004, dmpl_0017, dmpl_0003)
4. Never frame a value variant as stripped-down or last year's model, and never pitch "saves money" to budget buyers, which hurts pride. Show it as what discerning people choose, and frame EMI as the convenience richer people use. (Bijapurkar, Hopkins; rbwl_0020, mla_0055, mla_0054)
5. Position a modern product as taking over the chore while keeping the valued tradition. Where most people still make it at home, sell against home-made rather than against rival brands. (Bijapurkar, Hopkins; rbwl_0012, sa8_0021)
6. Status only exists once others register it, so show the product being noticed. With mass audiences, visible popularity is itself the appeal. (Desai, Jain; dmpl_0012, jgb_0011)
7. Own an everyday Hindi word, set in Devanagari, in a real small-town setting, or let one familiar Indian scene make the claim with no headline. Avoid descriptors every rival already claims ("fair", "pure"). (Parameswaran, Desai; nnn_0017, nnn_0013, dmpl_0008)
8. Show kids choosing only kid-targeted, low-value goods; in shared household goods show their veto. Lead with the gain rather than safety or prevention unless the ad first builds the cause-and-effect link. (Parameswaran, Desai, Hopkins; nnn_0008, dmpl_0013, sa8_0017)

## Idea & copy
9. Before writing, fix who the ad is for and what change it seeks, and restate a solution-brief as a problem with conflict. One ad covers one specific need, so split full-range briefs. (Godin, Sullivan; god_0007, whip_0010, whip_0072)
10. The hook does the selling: it calls out the buyer and carries the brand and promise. If it needs explaining, it fails. No exclamation marks. (Hopkins, Ogilvy, Sullivan, Carroll; mla_0073, ogx_0001, whip_0037, whip_0038, crl_0030)
11. Cut defensive reassurances ("made with real…") and asterisked prices. Test each claim against "yeah, right?" (add proof) and "so what?" (tie it to a real want). Never promise above what the product delivers. (Sullivan, Hopkins; whip_0034, whip_0042, mla_0008)
12. Drop striking images that upstage the claim, and drop obvious clichés (Taj, Eiffel). The idea should fit in one sentence, and the room's enthusiasm is not proof it is big. (Hopkins, Airey, Sullivan; sa8_0009, logo_0009, logo_0016, whip_0008)

## Proof & persuasion
13. Take the risk off the buyer. Have the guarantee come from the local seller the buyer knows, keep samples truly free (token charges kill response), and lead offers with the cheapest entry point. (Hopkins, Ogilvy, Godin; mla_0024, mla_0023, sa8_0029, ogx_0041, god_0011)
14. Cast real, unpolished customers, and have the interviewer challenge the product so they defend it. Don't add a celebrity just to pass pre-tests. (Ogilvy, Parameswaran; ogx_0021, nnn_0011)
15. Never publicise how many people do the bad habit you oppose; sell through "people like us do this". Anchor the product to a frequent everyday cue (chai time) at the moment the viewer can act. (Berger, Godin; ctg_0035, ctg_0036, ctg_0021, ctg_0022, ctg_0020, god_0017, god_0018)
16. Give the lowest-friction response route (WhatsApp or call beats a form), add a dated inducement against delay, and name local stockists in the ad. (Hopkins; sa8_0030, sa8_0051, mla_0063)

## Picture & composition
17. Reflective packs:
    - On glass, use one large, dim highlight.
    - Side-light cylinders with a black card on the opposite side.
    - Kill label sheen by raising the light or with a gobo no larger than the label.
    - On metal, add black cards for the edge reflections. A dark table turns a tin's front face black, so put a light surface under it.

    (Light Science & Magic; lsmx_0026, lsmx_0055, lsmx_0035, lsmx_0005, lsmx_0033)
18. Keep a contact shadow under cut-out products, or they float. Shoot flat products on white over a translucent, backlit base instead of trying to shade them. (Light Science & Magic; lsmx_0059, lsmx_0044)
19. A small, saturated subject can sit near a corner of a muted frame. Point the model's gaze at the product, freeze motion at the apex, and stack 9:16 frames up toward one peak. Pastel means brighter, not desaturated. (Freeman; pex_0041, pex_0015, pex_0045, pex_0006, pex_0018)
20. Indian popular and devotional imagery expects high saturation, strong contrast and glowing highlights, but retro filmi-poster styling now reads as dated to urban audiences. (Jain, Dwyer/Patel; jgb_0002, dpci_0018)

## Film, layout & type
21. Cut the film to its objective:
    - Awareness: open with sound, show the brand early and throughout, and put people at the centre.
    - Conversion: make the product the hero and set the context before the ask.
    - Full funnel: escalate the CTAs as the film runs.

    Set the key sung or spoken word on screen so the film works with the sound off. (Google ABCD, Parameswaran; abcd_0010, abcd_0008, abcd_0025, abcd_0011, abcd_0012, nnn_0019)
22. Text over a photo:
    - Check contrast against the least-contrasting patch of the image.
    - A thick outline acts as the background, so measure the letters against the outline.
    - Avoid hairline fonts for small supers.
    - Choose the brand name's typeface for legibility over mood.

    (WCAG, Ries; wcag_0035, wcag_0012, wcag_0033, r22_0039)
23. Posters and statics: one visual shock, the promise shown in the picture, huge type, the brand readable at a distance, pure colours, and at most three elements. (Ogilvy; ogx_0015)

## Brand & review
24. Before critique, agree the objective, then collect independent judgements on a short rubric. Ask whose approval the ad is built to win. Take client impressions, not prescriptions. (Connor/Irizarry, Kahneman, Ogilvy, Airey; disc_0008, disc_0007, nse_0026, nse_0057, ogx_0067, logo_0017)
25. Own one attribute nobody else owns and stay narrow. A challenger takes the colour opposite the leader. Keep a working campaign running after the team is bored with it. (Ries, Godin; r22_0014, r22_0016, r22_0041, god_0031)

B. CLAIMS THE LIBRARIAN PULLED FOR THIS BRIEF:
[sk_ctg_0013] remarkability is produced by violating a category expectation or by leaving a question open (berger-contagious) — The source gives two constructive routes to remarkability rather than treating it as a property a thing either has or lacks. The first is breaking an expectation the audience already holds about the category — the surprise is manufactured out of the norm, so any category with a strong norm can supply one. The second is unresolved mystery or controversy, which produces discussion because people consult others to settle the question, and disagreement generates further discussion.
[sk_whip_0011] an idea without a conflict has no story to run on (sullivan-hey-whipple) — Sullivan holds that a brand story requires an opposing force, and that most briefs remove it. The common brief describes life after purchase — a world with no cavities, no breakdowns, no overdrafts — which he says cuts to the end of the movie and short-circuits the structure that makes a story hold attention. His stated diagnosis of an uninspiring brief is that it states a solution rather than a problem, and he says creativity happens in response to a problem, so a brief phrased as a solution gives the maker nothing to respond to. He offers a headline test for the same point: nobody reads "Area Bank Not Robbed", not because the reader is bad but because attention tunes out an unchanged status quo.
[sk_abcd_0007] open in the middle of the action or on a close up (google-abcd-video-ads) — The source names two concrete opening constructions for an ad — beginning in the middle of the action, and opening on a close-up — and offers bold imagery at the start as a third means. It presents them as examples of many possible ways to earn engagement immediately, not as a required opening.
[sk_conv_c003_0018] dwelling on the minutiae of a craft produces identification (ondaatje-conversations-ch3) — Murch's claim that audiences are fascinated by process, and that deliberately dwelling on the minutiae of a character's work draws the viewer into that character's life and produces identification with them. It also serves clarity, since the character's work was hard to understand by its nature.
[sk_ogx_0041] show the product in use and in motion and repeat one visual device over years (ogilvy-beyond-ch2) — Showing the product in use pays, and where possible the end-result of using it — how a nappy keeps a baby dry, how pistons look after fifty thousand miles. For food the more appetising it looks the more it sells, and food in motion is said to look particularly appetising: chocolate sauce in the act of being poured, syrup over pancakes. Close-ups pay when the product is the hero of the commercial. Over a longer horizon he names mnemonics, a visual device repeated over a long period, which he says can increase brand identification and remind people of the promise.
[sk_mla_0018] attach the product to a named person and borrow that persons voice (hopkins-my-life-in-advertising) — The source claims that naming and featuring an individual is one of its most reliable devices, and that a person can be made famous far more easily than a firm. It reports three uses of it. Featuring an unknown chief engineer by name gave a mid-priced car a distinction against a better-known and handsomer rival at the same price. Making a designer sign the advertisements borrowed his existing reputation and let the copy be written to characterise him. And writing an entire selling book in the name and voice of an independent practical user — a chicken raiser who cared more for serving than for selling — produced a catalogue that read unlike the five or six identical ones the same prospect had requested. It states that a person featured this way is unknown at the start, that advertising makes him prominent, and that his name then becomes an exclusive feature of great value.
[sk_nnn_0019] vernacular appropriation carried by script and setting together (parameswaran-nawabs-nudes-noodles) — The "Thanda matlab Coca-Cola" execution reproduced here works by two simultaneous vernacular moves that the plate makes visible: the setting is an ordinary small-town Indian street — whitewashed wall, stacked red crates, a squatting child, a dog, a leaning pole — photographed without styling, and the line "Thanda matlab" is set in Devanagari alongside the Latin Coca-Cola logotype. The appropriation is of a Hindi word AND of the script it is written in, in a setting that is neither aspirational nor aspirationally lit.
[sk_abcd_0017] focus the message and avoid doing too much (google-abcd-video-ads) — The source names doing too much in a single ad as a fault in its own right and prescribes keeping both the messaging and the language focused and simple. It places this instruction inside Connection, not inside Attention or Direction — on the source's arrangement, an overloaded ad fails to connect.
[sk_abcd_0010] branding early often and richly (google-abcd-video-ads) — The source's branding principle has three separate dimensions in one line: when the brand first appears (early), how often it recurs (often), and how many different kinds of branding element carry it (richly). The third is the one that distinguishes this from a simple frequency instruction — the source asks for variety of asset, not just repetition.
[sk_abcd_0021] supercharge ctas by pairing onscreen cta with voice over (google-abcd-video-ads) — An on-screen call to action is to be paired with a voice-over saying the same thing, so that the next step is carried by both channels. The stated purpose is clarity of the next step rather than added emphasis.

C. WHAT GOOD LOOKED LIKE (one accepted piece; learn the level, do not copy its story, casting, setting or music):
Mokobara castaway film v2 — founder: "excellent. pass" (accepted).
Skeleton: open on the problem (a state that says time) → the product found (colour is the hit; brand super) → the reason (a human object inside the product) → the reveal (the product's exaggerated capability, one locked shot) → momentum (using the product) → resolution (leaving, the product worn) → brand close
Direction layer: per beat: feeling (one or two words + one line), framing (shot, lens, camera, what is in frame), impact (what makes the beat land; sound), and the Canon claim ids the beat rests on — board.json beats[].feeling / .framing / .impact / .canon; a hero_frame declared (beat 4)
Beats:
- 1. years_the_problem_state (0.0–3.5 s) feeling: endurance — he has been here a very long time. ECU of a hand scratching one more tally mark into rock covered in marks (take 2, 1.5 s) → wide: the small man side-on at the marked rock, sleeveless, empty shore (take 3, 2.0 s); the pull-back the board asked for became a cut
- 2. product_found_colour_is_the_hit (3.5–7.5 s) feeling: recognition — the first colour in a grey world. low at the tideline, the navy bag half-buried in grey pebbles; he crouches, brushes sand; brand super (the site's black logo, 420 px) 5.0–7.5 s on the sky
- 3. the_reason_object_inside (7.5–13.0 s) feeling: the reason — why he will go back. over-shoulder unzip → yellow lining → a small creased photo of a smiling woman (generated, unnamed); music enters; the bag intact (take 2)
- 4. the_reveal_exaggerated_capability (13.0–21.0 s) feeling: disbelief, then a laugh — the bag holds an absurd amount. locked medium, bag centre: both hands in (forearm depth — not to the shoulder), a stick emerges and becomes a paddle far longer than the bag, pulled straight (take 1); HERO FRAME declared here
- 5. momentum_using_the_product (21.0–24.2 s) feeling: momentum — a plan. close on hands: the last coconut in, the zip closes, he lifts the full bag out of frame; the pebbles empty (take 4)
- 6. resolution_leaving_product_worn (24.2–28.0 s) feeling: hope — the way back. wide at dawn: kneeling on the raft afloat, paddle in both hands from the first frame, two strokes, the raft glides toward the gold horizon, the bag on his back (take 2)
- 7. brand_close_end_card (28.0–30.0 s) feeling: home — the brand as the destination. navy end card (colour sampled from the product photo): the site's white wordmark SVG at 700 px · TRANSIT BACKPACK · 30L · Room for the long way home. · mokobara.com; 0.6-s crossfade in from 27.4 s

ADDITIONAL OUTPUT — fill after your treatment:
"decisions": {D1_idea, D2_conflict, D3_roles, D4_opening, D5_brand, D6_ask_and_end, D7_product_truth, D8_deviations} — each: D1_idea: The idea in one sentence — a specific moment in which this product matters. Not a feature list.; D2_conflict: What stands in the way (the problem, obstacle or tension) before the product enters?; D3_roles: Who is the hero (the customer/person) and what role does the brand play (the guide/enabler)?; D4_opening: The first 2 seconds: what is on screen? (mid-action, a close-up, or a bold image — say which); D5_brand: When is the brand/product first seen (second), where does it recur, and through which kinds of asset (product shot, pack, logo, spoken name, sound)?; D6_ask_and_end: What should the viewer do next, how is it carried (picture / voice / text), and what is the final frame? (default: end on the product); D7_product_truth: Every product fact the film shows or implies, each with its source (customer photo, product page, customer answer). Nothing else may be shown.; D8_deviations: Anything in the brief you are changing or not doing, and why (model limit, format, legal).
and per scene (S1_feeling, S2_first_frame, S3_one_action, S4_new_information, S5_impact): S1_feeling: The one emotion the viewer should feel here.; S2_first_frame: The opening picture of the scene — it must already contain the idea of the scene (not an ordinary state the motion has to rescue).; S3_one_action: The ONE action from start to end in this scene, and how long it takes.; S4_new_information: What the viewer learns here that they did not know before; why we leave the previous scene now.; S5_impact: How the scene lands (the payoff), and is it big enough to read on a phone?

Do this in order:
1. IDEAS. Write 3 genuinely different ideas. Each = a human truth + one specific moment where this product matters
   + a one-line key-frame description. At most one may have no people. Pick the strongest and say why in one line.
2. TREATMENT. ≤150 words of plain prose for the chosen idea: what we see and hear, start to finish.
3. SCENES (films) / FRAME (stills). For each scene: the prompt written in this model's own style (the style notes above),
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

### C2b → the same writer, after its draft

```
Here is your draft (JSON) for this ad and the customer's request (verbatim). Answer each question YES or NO,
quoting the line of your draft that proves it. For every NO, either revise the draft or keep it with a one-line reason
(e.g. "the customer asked for no logo"). You may NOT delete a scene's moment or replace motion with a still to satisfy
a question. Return the full revised JSON plus "checklist":[{"id","answer","evidence","action"}].

C01. Can you say the idea in one sentence, and would it be wrong for any other product?
C02. Is there a real obstacle or tension before the product appears (not just life after purchase)?
C03. Is the customer the hero and the brand the guide/enabler (not the brand bragging)?
C04. Would the first 2 seconds stop a thumb — mid-action, a close-up, or a bold image?
C05. Is the brand or product seen early, again later, and through more than one kind of asset — so a viewer could not credit a competitor?
C06. Does the film make the viewer FEEL something, and is each scene's feeling stated and shown (not a feature list)?
C07. Is the product the hero of at least one scene — shown doing the thing that matters?
C08. Does every scene add new information, and is every cut motivated?
C09. Is every must-have from the brief SHOWN on screen in a specific scene (not only written in text or voice)?
C10. Does each scene ask for only one action the video model can do in that time?
C11. Will the payoff and the product read clearly on a phone screen (size, time on screen)?
C12. Is the next step clear and carried by picture, voice or text — and does it end on the product?
C13. Is it written for one typical buyer in THIS market (who, where, what they worry about)?
C14. Does anything shown or said go beyond the product facts you listed (D7)?
C15. Is this different from the last pieces we made (casting, music, setting, structure)?
```
