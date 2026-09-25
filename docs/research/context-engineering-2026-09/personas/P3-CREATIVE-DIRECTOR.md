# Persona 3: The Creative Director / Commercial Filmmaker

*One of six persona reviews run on 2026-09-25 over `MEDIA-HISTORY.md` ([00]–[08]), the CQ-001 Media Factory evidence file,
the Mokobara accepted template, and `../CONTEXT-SOLUTION.md`. Model output, preserved in substance. Synthesis: `../MASTER-PLAN.md`.*

## 1. Diagnosis

In one sentence: **the project built a factory for correctness and then asked it for feeling.** Every automated film was put together from parts that had each passed a check. Nobody was responsible for the one thing a buyer pays for: an idea that makes you feel something about the product.

**RC1. There is no idea. The machine makes lists.**
- The iPhone Duo chef cited "feeling first" (CD-D7) and "want, obstacle, stakes" (CC-D5), then wrote six product photos with spec lines [05 §7.2].
- Aight Studio v10 was "a list of steps, not an idea": three people staring at a screen.
- In the Ascend kitchen film, "better life" was written on screen and never shown.
- The direct-Veo films had *moments*: a man in his sixties pulls a small phone from his kurta pocket and opens it like a book, and his wife leans in and laughs; a daughter's report card stands for "a better life" [05 §7.3, §15.3].
- All eight director personas picked the tea seller's one extra biscuit as the best idea of the night [05 §9.3]. It was the only piece with a human truth in it.
- No stage owned the idea. Claude-as-customer approved Aight Studio "because it followed the brief".

**RC2. It chops performance into pieces, so nothing moves.**
- "Chopping kills the life": still → 2–4 s clip → sound muted → words by code [05 §15.4].
- A slowly zooming still counted as a video shot. The equipment sheet marked any moving person "risky". Every fallback (`safe_replan`, `force_still`) turned motion into a still. Nobody checked that the film moved. The recipe checker sent back 13 of 14 drafts.
- Hence "a presentation not a video", in six jobs. This is the July Guddu mistake repeated ("I routed a drama like an explainer").
- CQ-001: the pipeline "inherited Media Factory's controls and not its creative loop". Lost along the way: character expression, an emotional target per beat, takes compared side by side, reworking the direction.

**RC3. The author was split up and blindfolded.**
- Mokobara v2 was accepted because one author held "the brief, the photographs and the myth in view at the moment of writing the words".
- v3 split that across three sessions and five forms. Five of its six defects were written into the plan before any spend, and every form still passed.
- The kitchen repeated this: the chef wrote into about 20 form fields, `prompts.py` rebuilt prompts from those fragments, and 20 of 26 tray items were failure notes. Nobody writes with heart while reading last week's accident reports.
- Ascend had 23 s of speech in 15 s of film because whoever wrote the words never heard them against the cut.

**RC4. Taste became rules, and the one person with taste was taken out.**
- The checks measured faithfulness, never life.
- Taste pushed in through written instructions became a template: all three overnight films starred "Meera", used the same soft piano and had the same shape.
- The automatic taste picker agreed with the founder on 5 of 15 pairs, then 10 of 15. His ruling: "you cant make it a rule".
- No automatic judge ever qualified, and the founder then ruled himself out of running jobs.
- Media Factory's practice of comparing four takes side by side, which is how directors actually use taste, was dropped.

**RC5. It offers everything, so it keeps failing where the models are weak, above all on voice.**
- Voice was robotic, wrong-accented or overlapping in about nine jobs:
  - voices were chosen on lines of 70 characters or fewer, then used for 48 s of narration;
  - scripts were written for the eye, not the ear;
  - nobody listened to the delivered audio;
  - on-screen text repeated the VO.
- The Canon has no audio source at all.
- The same pattern with hands on zips, a new phone drawn from scratch (0/6) and multi-turn dialogue.
- "Genre picks the route" (July): the genre gate was planned and never built.

**Why the direct prompt wins.** The "direct" arm was not the customer's raw words. It was one Claude session writing a story for Veo in Veo's own unit (one 8-s scene), with no review rounds. That is a director without bureaucracy, and it is the real bar.

## 2. Keep / kill

**Keep:**
- Exact text, logos (the brand's own files, checked by hash) and end cards set by code; Hindi in motion 4/4 this way vs 0/4 when models wrote it; the text-bounds and contrast checks.
- Real product photos, as references and as insert shots.
- A still first wherever the product must stay the same. When a still is animated, that first frame *is* the direction ("the remedy each time was a different still, not a better sentence").
- Feeling, framing and impact per beat: +7 blind for US$0.067.
- A product-facts file per customer, carried from job to job.
- Buying the riskiest shot first; showing the plan and stills before spend.
- Speech timing: each line ≤ its shot minus 0.4 s, at about 2.5 words a second.
- The record of the last 8 pieces made, used to stop repeats.
- Blind founder judging, and the chat front door.

**Kill:**
- The kitchen stations and their 2,000-word cards.
- Any form or code step between the author's words and the model's prompt.
- Every fallback that swaps a shot for a zooming still.
- Muting the scene's own sound by default.
- Canon packs and failure notes in the author's context.
- Overall-verdict model judges that block delivery.
- Claude approving its own work as the customer.
- TTS narration as the default.
- Rebuilding mid-order, and redesigning after one rejection.

## 3. The solution: one director, three ideas you can see, scenes in the model's own unit, finished by code

### 3.1 What creative intelligence is, and where it lives
Five decisions, in order:
1. **Idea:** one true, specific moment in which the product matters.
2. **World:** who, where, what hour, which objects, true to the audience and product.
3. **Performance:** a face that changes; an action with a start and an end.
4. **Motion:** a camera that moves for a reason; shots that differ a lot.
5. **Sound:** the room, the sounds of the scene, music or silence, a voice that belongs to a person.

It lives in **two places only**:
- **One strong author** makes all five decisions at one sitting, with the photos and facts in view.
- **Selection:** someone with taste chooses between options they can see.

Code, checks and the Canon serve those two and never overrule them.

### 3.2 The flow (one flow for all formats; only the unit changes)

| Stage | Who | Sees | Produces | Cost |
|---|---|---|---|---|
| 0 Intake | cheap model | exact words, uploads, saved customer assets | one format from the menu (or one question); a product-facts file; any scope change stated in one sentence before spend | ≤US$0.02 |
| 1 Ideas | strongest writing model (the "director") | order, facts file, photos, the format's one-page card, the last 8 pieces, 2 example films | **3 ideas** differing in premise and casting (one may have no people), each a human truth + a moment + a key frame rendered as a still | ~US$0.45, ≤4 min |
| 2 Pick | customer | the 3 key frames | the chosen idea; if "you choose" or 10 min of silence, the director picks | US$0 |
| 3 Treatment | same director, same context | the pick and any edits | one page in the video model's own terms. For Veo: an 8-s scene; who, where, light and lens; one action from start to end; a camera move with its cause; the scene's own sound; at most one quoted line. Plus on-screen words and a sound plan | ~US$0.30 |
| 3b Critique | a different strong model | the treatment + a Canon critique card (≤15 questions) | ≤5 notes, each accepted or rejected in one line by the director. **Never blocks** | ~US$0.10 |
| 3c Hard checks | code | treatment + facts file | product details match the facts; exact words; allowed claims; speech fits the shots; nothing the format "cannot" do | US$0 |
| 4 Production | code + director | the treatment | stills first where identity matters; 2–3 takes of the hero scene; a contact sheet; the director picks takes. A scene that fails twice is **rewritten or cut, never swapped for a still**. Native sound kept; words added by code | 15-s film ≤US$5 |
| 5 Customer | customer | parts as made, then the film with sound | accept / specific repair (back to the director) / reject | — |
| 6 Learning | offline | verdicts | accepted and rejected work into an example library with the customer's reasons; facts saved; a format card changes only after a win on the fixed briefs | — |

**Targets:** a still ≤US$0.25 per accepted outcome including reasoning; a 15-s film ≤US$6 and ≤30 min from pick to first cut (direct-Veo Ascend: about US$5 and 6 minutes).

### 3.3 The format menu
A format is Higgsfield's preset idea at the right level. It fixes *how* the piece is produced (unit, route, sound, finishing), never the idea, casting, music or look.

**Offer now:**
1. **Product hero still or poster.** P1 poster accepted; 9 portfolio tiles accepted; images 55/75 in blind judging.
2. **Edit my photo.** The most common real request; Seedream edit passed 10/12.
3. **Offer or festive banner set with exact Hindi.** Picture plus code-set text: 4/4.
4. **Animate my still.** Kling 8/8, Wan 8/8.
5. **Product film with no people.** Needs the premium model and re-draws.
6. **One-moment story film, 15–20 s.** 2–3 native Veo scenes, an insert from a real product photo, an end card. This is how both direct-Veo wins and Mokobara v2 were made.
7. **Drawn explainer rendered by code.** The RentOK films, US$0.07–0.53.
8. **One presenter speaking to camera.** Upwork intro V4.1; Veo's own speech qualified 53/60.

**Change the scope before spending:**
- Hands working a product → show the before and after.
- A new product → real photos only (0/6 drawn from scratch).
- Narration → on-screen words plus one line spoken inside the scene.

**Refuse for now:**
- Drama with back-and-forth dialogue.
- Films over 30 s that depend on shots matching.
- Lip-sync onto existing footage (0/5).
- Real people or celebrity likenesses.
- Claim-heavy categories without a customer claim sheet.

### 3.4 Sound and voice
- **The default is no narration.** Keep native scene sound; one music track or deliberate silence; at most one short line per scene, spoken by the video model. Two-speaker Hindi dialogue passed 6/6 in the Lab.
- **Narration returns only as a cast brand voice:** auditioned on the full real script, chosen by a human ear, saved with the customer's assets, timed to the cut, never repeating the on-screen words.
- **Every file gets a human listen at preview,** plus measured checks on fit, overlap and loudness.

### 3.5 Taste without rules
Taste comes in through four things:
1. **The strongest writing model is the author.**
2. **Examples, not rules:** accepted *and* rejected films with the founder's words, rotated, with an instruction not to copy them.
3. **Choice:** the customer picks the idea; the director picks takes.
4. **Critique questions** the author may overrule with a reason.

The only hard rules are facts: product truth, exact words, the law, what the format can do, technical specs, and no repeat of casting, name, music or shape within the last 8 pieces.

### 3.6 What the Canon is for
- **Good for:**
  - better-informed plans (the no-Canon plan came last in all nine blind rankings);
  - a vocabulary for critique (sell, not merely entertain; one dominant idea; brand early; end on the pack);
  - copy, numbers and the Indian reader.
- **Cannot:**
  - produce an idea;
  - know the product or today's models;
  - help with sound, vertical 9:16 or motion design (its own declared gaps);
  - on two jobs the right advice was cited and then not followed.
- **So:** compile it into the critique card (≤15 questions) and a copy reviewer. The director may read up to about 10 full claims on request. Nothing is loaded by default.

### 3.7 Measurement and decision rules
**12 fixed briefs from the history, in the customer's own words:**
- Stills: Mokobara poster, Jaipur sweet-shop Diwali poster, Dhaba 47 offer, one photo edit.
- Product: animate the Mokobara poster, the condensation bottle, the Cumin chopsticks, earbuds with no people.
- Story: iPhone Duo for the over-50s, Ascend Foods for kirana shops, the Mousi Kitchen ramen bar, the Aight tea seller.

**Three arms per brief,** with the same models, photos and finishing by code: raw direct; author direct (one session writing for the model, no pipeline; the bar); pipeline.

**Scorecard:** a blind ranking; "Would I pay for this?"; "Say the idea in one sentence" (if the founder can't, there isn't one).

**Decision rules:**
- **A format ships** when the pipeline beats author-direct on at least 3 of 4 briefs, would-pay holds on at least 3 of 4, and CpAO is at most 1.5× author-direct.
- **Otherwise** that format runs the author-direct method plus finishing by code. That is still a product.
- **Any change** to the director prompt, a format card or a check re-runs that format's briefs and must not lose a brief it previously won.

## 4. The first 14 days (every paid step needs a written cap; everything in sequence on the one Mac)

| Day | Step | Done when | US$ |
|---|---|---|---|
| 1 | Freeze kitchen and studio code; write the 12 briefs and the scorecard | Founder signs | 0 |
| 2 | Format menu v0: 8 one-page cards + refusal list | Founder approves or strikes each ("would I sell this?") | 0 |
| 3 | Director prompt (≤1,200 words), critique card, facts template, five-step script; dry run on 3 briefs | Ideas → treatment runs without errors | ~1 |
| 4 | **Idea round:** 12 briefs × (3 director key frames + 1 author-direct key frame) | Founder picks blind. If author-direct wins 7+ of 12, rework the director before any film spend | ≤6 |
| 5–6 | Stills: 4 briefs × 3 arms × 2 candidates | Ranked, with would-pay; still formats decided | ≤8 |
| 7–8 | Films part 1: iPhone Duo and Ascend (the two we lost), pipeline vs author-direct | Ranked. If the pipeline loses both, stop; films use the author-direct method | ≤20 |
| 9–10 | Films part 2: ramen bar, Aight tea seller, one product film | Film formats decided | ≤25 |
| 11 | Voice: 3 full scripts × 4 routes (Sarvam, ElevenLabs v3, Azure, video-model speech), judged blind by ear | One route passes 3/3, or narration stays off | ≤3 |
| 12 | One page per format: ship pipeline / ship author-direct / refuse, with measured acceptance, cost and time | Founder signs | 0 |
| 13 | Put the winning path behind the chat; take the kitchen stations off the live path | 12 briefs dry-run through the studio | 0 |
| 14 | Three outside users (Rama + 2), each owning their budget | ≥2 of 3 accept and ≥1 would pay; reasons recorded either way | ≤15 |

**Total:** about US$78, released step by step. **Founder judging time:** about 3 hours.

## 5. Bet and risk
**Bet:** put taste at the cheapest decision point: **three ideas the customer can see as key frames**. Then one author writes whole scenes in the model's own unit. A chosen idea, made as a performance rather than assembled from parts, is what a direct prompt does not give and what a buyer pays for.

**Risk:** someone adds a rule after the next bad film. If "no change without a win on the test briefs" does not hold, the director becomes the kitchen within two weeks. A smaller risk is Veo's limits on Indian faces and voices; rescoping answers that.

## 6. Disagreements with CONTEXT-SOLUTION.md
1. **The main cause is direction, not prompt writing.** CQ-001 lost only 1 of 16 creative decisions at the prompt step; rewriting prompts alone matched baseline, while better direction scored +7. The winning direct-Veo prompts were not 30-word captions: they carried a style line, a full character description and dialogue, and won on story and on using Veo's own unit. Cleaner prompts make a slideshow cleaner, not alive.
2. **A structured plan plus a code compiler is one more form between author and model.** That is Mokobara v3 and `prompts.py`. Keep per-model writing notes as a page the author reads, plus a linter that only flags.
3. **Canon rules as post-generation checks:** yes for facts, exact words, law and technical specs; no for creative doctrine. Checks flattened the films (13/14 drafts sent back; a film failed for "no brand mark" when the customer asked for no logo).
4. **PickScore/HPSv3 to pick takes** will choose polished but generic work, which is what "AI slop" means now. Use them only to throw out broken takes.
5. **Stills-first testing:** stills already work; test films in week one, with stop rules.
6. **"Direct" must include the author-direct arm,** because that is what beat us twice.

**Agreed:** knowledge stays out of generation prompts; identity from references, not descriptions; motion-only prompts for animating a still; no "no X" sentences; lessons as counted changes to specific rules or cards; knowledge must win a paired test before promotion. But its 30-day plan is mostly infrastructure: building before proving, again.
