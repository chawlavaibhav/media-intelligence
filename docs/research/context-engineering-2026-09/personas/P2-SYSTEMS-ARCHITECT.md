# Persona 2: The ML Systems Architect

*One of six persona reviews run on 2026-09-25 over the complete project history (`MEDIA-HISTORY.md`, cited as [00]–[08]) and
`../CONTEXT-SOLUTION.md`. Model output, reviewed and preserved verbatim in substance. Synthesis: `../MASTER-PLAN.md`.*

## 1. Diagnosis: five mechanical root causes

**RC1. Films were made in pieces too small, so failures multiplied.**
- **Rejected films were cut into many short, separate clips.** P1's Reel asked Veo for eight 3–4-second beats of hand choreography, each started from its own separately made still: 81 attempts, the inspector rejected 15 of 16 Veo takes, and the bag turned from blue to yellow [04 §5.3]. The kitchen's standard film was still → 2–4 s clip → sound muted → words added by code. The builder's own verdict: "chopping kills the life" [05 §15.4].
- **Ascend shows the cost.** 16 takes rejected, 12 repairs, 7 flagged takes kept anyway, and a cloned shopkeeper. Each shot started from the previous shot's last frame, so remaking shot 2 forced shots 3 and 4 to be remade too (F33). That is the same frame-chaining banned on 20 July as a "photocopy of a photocopy" [01 §4.6].
- **Both direct-Veo films did the opposite:** a few whole 8-second scenes (four on Ascend) with their own sound, and one fixed description of the main character repeated word for word [05 §15.3].
- **The arithmetic.** If a film needs k separate clips to all succeed, its chance is roughly the product of the clips' chances. At measured rates (Veo Fast image-to-video 5/8; Veo with people 7 of 14 failed, EQ-014), eight beats almost never works and three sometimes does.
- **Nothing tied one shot to the next.** The failure atlas has 12 such rows across 6 jobs (bucket B3), yet July had already measured a method that works: editing every picture from one character sheet, which Seedream held 29 times out of 32 [01].

**RC2. The pipeline replaced the direct prompt instead of competing with it, and nothing was regression-tested.**
- No production run ever included "the same brief sent straight to the model". The founder found out the kitchen lost only by opening a separate session, twice [05 §7.3, §15.3].
- With no fixed set of test briefs, every change was judged on one live order. The chef card went from v1 to v13 in 26 hours; nine fixes landed mid-order; there were 30 rulings in 36 hours and more than 25 reversals overall [05 §14][07].
- The one knowledge test judged written plans, not finished media (RC-4 of the Mokobara v3 root-cause analysis [04 §4.5]).
- "Every fix breaks something" is not bad luck. It is what a system does when it has no baseline and no regression suite.

**RC3. Checks could only make things safer, and the checkers were never qualified.**
- **Checks could only take things away.** The recipe checker sent back 13 of 14 drafts. Then `safe_replan` and `force_still` swapped moving shots for stills, a keyword rule turned "unfold" into "cannot", and 11 hard-coded send-back routes did the rest. Result: "a presentation not a video" [05 §7.6].
- **The judges holding those vetoes had failed their tests:**
  - the P1 model reviewer found 1 of 6 known defects;
  - in the judge trial, GPT-5.6 Sol passed 0 of 7 pieces the founder had accepted;
  - Gemini called Apple's own product photos "AI artifacts";
  - the gatekeeper was wrong on 2 of its 4 notes [04][05 §4, §11.4].
- **Overriding the checks was no better.** When the builder overrode them, it shipped takes the inspector had rejected [04 §5.3].
- Veto and override are the same mistake: there was never a choice among several candidates, only "accept this one or make it worse".
- No check measured what mattered. Nothing asked "does it move?" or "would the buyer pay?" [05 §7.6, §11.5].

**RC4. Money and context went to deliberation, not to more attempts.**
- **Reasoning dominated cost.** On the only accepted P1 output (the poster), US$1.87 of US$2.28 was reasoning [04].
- **The planners were overloaded:**
  - the director read about 25,000 tokens of Canon at high reasoning, 4–10 minutes a round;
  - the chef card was 2,272 words;
  - 20 of the 26 items on the chef's reading tray were failure notes, so it wrote defensively [05 §7.2, §14];
  - Kimi wrote about 95,000 words over 15 checks on Ascend.
- **The context that mattered was missing.** The order sheet did not include the customer's own words [04 §5.4]. Mokobara v3's facts stage held 16 facts, none about the bag's physical build, so the plan invented a side zip the real bag does not have [04 §4.5].
- **Reading did not change the writing.** The chef cited the Canon's "feeling first" page and still wrote a feature list [05 §7.2].
- Meanwhile generation, the only step that makes pixels, ran one attempt per shot until something failed.

**RC5. The product was built on the customer, and the automated path had no judge.**
- P1 v1 went live the morning after it was built, and the kitchen was rebuilt while the founder was ordering from it.
- The menu had no genre gate, though July and the Lab had already measured what fails: lip-sync 0/5, a brand-new product drawn by the model 0/6, hands on zips 15 of 16 attempts failed, and robotic voice on long text-to-speech reads.
- The founder then ruled himself out of running jobs (24 Sep). Claude, standing in as the customer, approved Aight Studio "because it followed the brief" [05 §11.5]. The automated studio had no trusted judge at all.

## 2. Keep and kill

**Keep (each one demonstrably worked):**
- Exact text and logo set by code, and the Typeset engine. Hindi in motion: 4/4 by code against 0/4 when video models wrote it [03].
- Real product photos as references. Never ask a model to draw a product it has never seen (EQ-015: 0 of 6).
- Still picture first when the product must be exact.
- Character consistency by editing from one character sheet (29 of 32).
- Whole 8-second scenes, written in the video model's own style by one author. This is what the two direct-Veo sessions did.
- Code checks on the finished file:
  - voice-over schedule and overlap;
  - loudness and peak level;
  - text inside safe areas and clear of the hero;
  - MP4 edit list;
  - no black frames.

  These are measurements; none of them ever made a film lifeless.
- The spend ledger (money reserved before each call, collision-proof attempt ids, spending limits that carry across raised limits), and the P1 SQLite job store.
- The chat front page. The customer sees the plan and the stills before any video money is spent.
- Blind judging packets with sealed labels. The 76 items the founder has already judged, as a calibration set for any automatic judge. Exact binomial bounds (Clopper–Pearson) on equipment ratings.
- A wider menu. Research on 26 Aug (CANON-009) found real demand is mostly "edit my photo" and "animate my image". The Lab showed Seedream 5 Pro edits 10/12 accepted, and Kling and Wan image-to-video 8/8 each.

**Kill:**
- The kitchen as a staff of AI roles steered by prose cards: waiter, chef, head cook, gatekeeper, diary writer, lenses, personas, and advisors acting as design authority.
- Any AI judge with a veto, and any automatic fallback from a moving shot to a still.
- Canon packs, failure notes and recent recipes on the writer's reading tray.
- Code that assembles prompts from form fields or rewrites prompt strings. Three live failures came from exactly this: F10 (product name left in prompts, every shot refused), F15 (the word "the" painted into a frame) and F27 ("Mousi Kitchen" refused three times).
- Chopping films into 2–4-second beats, and chaining shots from last frames.
- Budget pauses every dollar (F29). Quote one price up front.
- Changing the system while an order is running.
- A premium planner model at up to about US$4 a recipe (GPT-6 Astra).

## 3. The solution: a finishing and selection layer around one direct author

**Principle.** The pipeline never replaces the direct prompt. It wraps the best direct method we have seen, one strong author writing whole scenes in the model's own language, with what that method cannot do:
- the product shown truly;
- exact text and logo;
- voice timing and clean audio;
- a choice among several candidates.

The direct output is always one of the candidates, so in the customer's own judgement we cannot deliver worse than direct; we can only cost more, and that extra cost is what we optimise. This holds only while a trusted person makes the final pick (see §5).

**The stages, and what each one sees:**

| Stage | Who | Sees (and nothing else) | Budget |
|---|---|---|---|
| Intake | cheap LLM (Luna class) | the customer's words exactly as typed, the list of uploads, a summary of the customer's saved file | ≤3k tokens, <US$0.005 |
| Writer | one strong LLM, one call (+1 retry if the checker finds problems) | the exact words; the job details; up to 1k tokens of facts, each with its source; 1–4 product or customer images; a recipe card (≤400 tokens); a one-page style guide for each model it will write for (≤600 tokens); a craft card for this kind of job (≤15 lines, distilled once from the Canon); a short list of what the last 8 jobs used (casting, music, structure; ≤300 tokens) | ≤8k tokens in, ≤60 s, ≤US$0.10 |
| Prompt checker | code | the writer's structured output | US$0 |
| Generators | image and video models | only the prompt and the reference images. Stills 30–80 words; whole scenes 60–120 words; animating a still: motion only, ≤40 words | per recipe |
| Pre-ranker | cheap vision model | each candidate plus ≤6 yes/no questions taken from the job details | ≤US$0.005 per candidate |
| Finisher | code | the chosen media, the copy, the logo, the voice audio | US$0 |
| Pick | the customer | at most 3 images, or 2 cuts of a film (finished and raw) | — |
| Ledger | code | everything, append-only; never loaded into any model's context | — |

**The first menu of recipes:**
- **R1: static ad or poster.** Text set by code; two formats.
- **R2: edit my photo.**
- **R3: animate my image.** One 8-second clip from the customer's still, motion-only prompt, two takes.
- **R4: scene film of 15–30 seconds.**
  - Built from 2–4 whole 8-second scenes (made from text, or from an approved first frame).
  - Two takes of every scene with a person in it.
  - Real product photos for up to 25% of the runtime; music from Lyria.
- **R5: motion graphics rendered by code** (the RentOK type).

A **genre gate** at intake declines or rescopes, with a plain reason:
- drama with several speakers;
- lip-sync;
- a product with no photos;
- long on-screen dialogue.

**Voice options:**
- **V0: no voice.** This is the default.
- **V1: narrator.** Text-to-speech auditions using the actual script lines, not 70-character test lines. The customer picks a voice by ear in the chat before any video is bought. Each line is measured and must be at least 0.4 s shorter than its shot; the picture is cut to fit the audio.
- **V2: speech inside the scene.** At most two short lines per 8-second scene, only on routes the Lab passed for two-speaker Hindi (Veo Fast 2/2, Omni 2/2). The customer hears it in the raw cut.
- **No lip-sync added afterwards** (0/5 in the Lab).

**Continuity:**
- **A saved file for each customer:** product photos, physical facts with their sources, and looks already approved. It carries over from job to job; losing it was root cause RC-5 of Mokobara v3 ("that knowledge died with the job").
- **One approved master picture per character,** shown in the storyboard.
- **Every scene with that person** starts from an edit of the master picture, plus one fixed description sentence repeated word for word.
- **At most 4 joins per film, and no chaining.**
- **A trained per-customer model (LoRA)** only for repeat customers with at least 3 jobs.

**Checks.**

*Hard checks.* These block delivery. A failure is fixed by code or by remaking that one asset, never by swapping motion for a still:
- exact copy;
- format and duration;
- voice lines fit their shots and do not overlap;
- loudness −14 LUFS and true peak ≤ −1 dBTP;
- no black frames;
- text clear of the hero;
- a motion budget: at least 70% of a film's runtime must be generated video. This is the missing slideshow check.

*Soft signals.* These only rank candidates:
- the ≤6 yes/no questions;
- how closely faces and products match their references.

An automatic ranker gets power to release only after it agrees with the founder at least 80% of the time on held-out pairs taken from the 76 items he has judged plus beta labels.

**Determinism and records.**
- The writer returns strict JSON:
  - a treatment of ≤150 words;
  - per scene: prompt, duration, source (generate or photo), references, voice line, on-screen copy;
  - the facts it used, with sources.
- Code checks it against:
  - word budgets;
  - positive phrasing;
  - no quoted brand or copy strings in prompts;
  - motion-only prompts when animating a still;
  - voice timing.
- Violations go back to the writer once. **Code never edits a prompt.**
- Every call's inputs, seed, model version and cost are stored, so any job can be replayed.

**Economics.**
- Cost per accepted outcome = cost of one round ÷ chance the round is accepted. If the customer looks at N candidates, the chance is about 1 − (1 − p)^N.
- **Targets to verify (these are not measured claims):**

  | | Target per round | Reference point |
  |---|---|---|
  | Static ad | ≤US$0.50, ≤3 min machine time | P1 poster: US$2.28, 1 h 34 m |
  | 15-second film | ≤US$8, ≤20 min | 3 scenes × 8 s × US$0.15/s (Veo Fast with sound [01]) × 2 takes ≈ US$7.20, plus about US$0.40 for writer and first frames |
  | Reasoning share | ≤10% of job cost | poster: 82% |

- **A film round costs about what the kitchen spent (US$9.44).** The gain has to come from a higher chance of acceptance and from 20 minutes instead of 66.
- **Human waiting time is recorded separately.** On RentOK v2, 4 hours of the 5 h 09 m was the founder's reply time [04].
- **Caching:**
  - prompt caching for the writer's fixed opening text;
  - reuse of the customer's saved file and approved master pictures;
  - de-duplication keyed on prompt, seed and model, so retries after refusals are not blocked (the overnight problem).

**Learning.**
- Raw records are never put on a model's reading tray.
- A lesson changes a recipe, a model style guide, a craft card or a hard check, and only after it wins on the test briefs.
- Each recipe's acceptance rate is tracked with a running estimate.
- Automatic routing between recipes starts only once an option has at least 30 judged jobs. The direct option always keeps at least 10% of traffic.

## 4. The first 14 days (about US$140 in total; the founder sets each cap before any spend)

| Day | Step | Done when | US$ cap |
|---|---|---|---|
| 1 | Freeze. No live-studio changes. Pick 12 test briefs (6 image or edit, 6 film), using the founder's exact words from Mokobara, RentOK, iPhone Duo, Ascend, ramen, Aight Studio, Cumin and skateboard, plus 4 of the most common real request types. **Write the decision rules down before spending anything.** | Briefs and rules saved with hashes; founder spends 15 minutes signing off | 0 |
| 2 | Baselines. **A0** = the customer's words straight to the model. **A1** = one strong model writing the model prompts in one pass, the S-ASCEND-VEO method. Reuse the two existing direct-Veo films. | 4 new film briefs + 6 image briefs sealed | 30 |
| 3–6 | Build pipeline v0. Keep new code to about 1,500 lines on the P1 job store, providers, Typeset and checks. No kitchen code. | 1 image brief and 1 film brief run end to end, replayable; reasoning ≤10% of cost | 5 (smoke tests) |
| 7–8 | Run the pipeline on all 12 briefs. Keep the raw cut and the finished cut of each film. | 12 jobs sealed; cost and time per job in the ledger | 55 |
| 9 | Founder's blind sitting: A0, A1, pipeline raw, pipeline finished, all shuffled. | For each: accept, "would pay", rank, and a one-line reason; about 75 minutes | 0 |
| 10 | Read the results against the rules written on day 1. The comparisons separate three effects: A1 vs A0 = the strong author; raw vs A1 = the recipe and craft card; finished vs raw = the finishing layer. | A decision for each class | 0 |
| 11–12 | One change at a time on the worst failure. Re-run only the briefs it affects. | No worse on 5 of 6 in that class | 20 |
| 13 | 3–5 real beta customers (Rama and friends, not the founder, not Claude). The customer picks. | At least 3 delivered, with the customer's own verdict | 30 |
| 14 | Freeze v0 as the baseline. The 12 briefs become the paid regression suite for every future change. | A one-page result for the founder; decide whether to switch the live studio | 0 |

**Decision rules, set on day 1.** The pipeline ships for a class only if all of these hold:
- the founder says "would pay" on at least 4 of 6 briefs;
- the pipeline ranks at least as high as A1 on at least 4 of 6;
- a round costs no more than 1.5 × A1;
- machine time is at most 5 minutes for images and 25 minutes for films.

If A1 beats the pipeline on 4 of 6, strip the pipeline back to A1 plus text and logo finishing. If nothing gets "would pay" on 3 of 6 films, stop selling open films and keep only R3 and R5.

Six briefs per class is a screen for large effects, not statistical proof. The kitchen's losses were large.

## 5. The one bet and the one risk

**The bet:** don't try to make the pipeline smarter than the model. Make it the layer that finishes and chooses around one direct author. Keep the direct candidate forever, put tokens into more candidates rather than more deliberation, and let only measurements block delivery. That is the one design where "beats direct" holds by construction rather than by hope.

**The risk: nobody qualified to pick the winner.** The guarantee holds only if a trusted person picks the candidate.
- No automatic judge has ever qualified here.
- The founder is the only proven eye, and he has ruled himself out of running jobs.
- If real customers won't pick, or pick badly, the pipeline falls back to an unqualified ranker, which is RC3 again.

The mitigation is labelling: every customer pick becomes a label, aimed at about 100 pairs before any ranker gets release power. If customers refuse to choose, this plan loses its main advantage.

## 6. Where I disagree with CONTEXT-SOLUTION.md

1. **Code-compiled prompts.** It proposes turning the plan into prompts by code, through templates for each model. Our own evidence says code-assembled prompts hurt:
   - Mokobara v3's prompts were built by code from the plan, and it was rejected;
   - the kitchen's `prompts.py` built prompts from small form fields;
   - F10, F15 and F27 were all string-handling bugs.

   The prompts that won were written in one pass by an LLM. Keep the budgets and the one-page style guides; let the LLM write the prompt, and let code only check it.
2. **The wrong baseline.** Its "direct arm" is the customer's words plus references. What actually beat us twice was a strong LLM writing Veo prompts in one pass. We need both baselines, and that second one is the harder bar.
3. **It misses the main cause for films.** Its diagnosis is prompt length, negative phrasing and constraint count. Those are real, but CQ-001 found that prompt wording was not the bottleneck (1 of 16 creative decisions was lost at the prompt step [04 §4.2]). For films the first cause is how finely the film is chopped (RC1), and its 30-day plan starts with stills only.
4. **Automatic selection.** Its route relies on a preference model plus an AI vision judge. Our data says no automatic ranker is trustworthy on our briefs yet (66% agreement, 1 of 6, 0 of 7). Such rankers may shortlist candidates; they should not choose until they qualify.
5. **"What we are not doing wrong."** It lists "binding checker verdicts" and "a deterministic prompt builder" as correct. Verdicts from unqualified judges that could block work are what produced the slideshows. Only measured checks may block.
6. **Canon work first.** Sorting the Canon into six types and building a registry of about 30 checks in month one risks rebuilding the machinery of checks that made films lifeless. Keep hard checks to about 10, all measurements, and only one craft card per class of job, which must beat having no card on media.
7. **The router bandit.** It is right in principle, but with under 30 judged jobs per option it would only be fitting noise. Start with a fixed menu and running estimates.

**Agreed:**
- knowledge stays out of the generator's prompt;
- stills of 80 words or fewer, phrased positively;
- motion-only prompts when animating a still;
- spend on candidates, not words;
- the direct candidate is permanent;
- changes promoted only after paired tests;
- lessons stored as specific changes, never as a growing pile of prose.
