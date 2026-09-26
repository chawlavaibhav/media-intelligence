# Persona 6: The Red-Team Skeptic

*One of six persona reviews run on 2026-09-25 over `MEDIA-HISTORY.md` ([00]–[08]), the Mokobara accepted template and
`../CONTEXT-SOLUTION.md`. Model output, preserved in substance. Synthesis: `../MASTER-PLAN.md`.*

## 0. Verdict first
- **The intelligence-layer bet (cheap LLM + Canon or cards beats one strong model) has failed every hard test as a creative layer:**
  - EVAL-038: 0 of 6;
  - E2: Sonnet *without* the Canon ranked above Sonnet with it;
  - Mokobara v3, with all ten packs: rejected;
  - one Claude session writing Veo prompts beat the kitchen twice.

  The only positive results were plans judged as plans, or deterministic assembly (code-set text 4/4 against 0/4). It is falsified as a creative layer, not as a finishing layer.
- **"Much, much better than one direct prompt" is reachable only on things the model cannot do by itself.** On ideas and raw visual quality a pipeline can at best tie, because the best creative engine found is a frontier LLM, and the customer can use it directly.
- **So the product that can pass is the same strong author the direct prompt uses, plus deterministic finishing and customer choice.** Nothing else goes in until it wins a blind test.

## 1. Diagnosis

**RC1. The baseline was never defined.**
- Both "direct" wins were a one-author pipeline (**B1**): a Claude session wrote the script and prompts, used Apple's real photo and retook a shot.
- Raw words to Veo (**B0**) were never tested.
- Consumer apps already work like B1: Veo's rewriter "can't be disabled"; OpenAI returns a `revised_prompt`.
- The real competitor is B1: about US$5 and 6 minutes for Ascend, against the kitchen's US$9.44 and 1 h 6 min.

**RC2. The pipeline removed the author's taste and added nothing the model could not do.**
- **Mokobara v3:** three sessions shared the writing, and 5 of 6 defects were in the plan before spend.
- **iPhone Duo:** the chef cited "feeling first" and wrote a feature list; the checker returned 13 of 14 drafts; `safe_replan` and `force_still` turned motion into zooms.
- **Chopping:** "Chopping kills the life".
- **CQ-001:** only 1 of 16 creative decisions was lost at the prompt step.
- Cumin 003 shows that one author is necessary but not sufficient.

**RC3. Yesterday's model limits were written into the rules, so the pipeline fell behind the models.**
- Veo Fast and Omni made two-speaker Hindi dialogue 2/2 on 9 Sep, yet the cards said "the video model never speaks" and scenes were muted. The direct Ascend film used Veo's own speech and won.
- Value that patches a model's weakness loses worth with every release. Value from what no model can know (exact copy, real product, logo, formats, facts) does not.

**RC4. Only one person can judge, and he also writes the briefs.**
- No automatic judge qualified: kappa 0.33; the best trial judge passed 4 of 7 accepted pieces; the P1 reviewer found 1 of 6 known defects.
- Blinding leaked: the founder saw RentOK's progress in chat, reversed a blind EVAL-038 verdict after the reveal, and Claude-as-customer approved Aight Studio.
- There were 8 accepted deliverables in 80 days and 25+ reversals, mostly after a single rejected output. Every "fix" was fitted to noise.

**RC5. The product pointed away from real demand.**
- CANON-009: edits and animations are the commonest requests, and 0 of 30 briefs tested them.
- No paying customer; Rama's first job failed.
- Multi-scene film became the centre of the work, though the automated pipeline never had one accepted.

## 2. Where a pipeline can and cannot beat one direct prompt

| Lever | Evidence | Durable? |
|---|---|---|
| Exact copy and logo by code | Hindi in motion: code 4/4 vs model 0/4; Veo turned the Apple logo black | Yes for video and exact copy; shrinking for stills (NB2 and GPT Image 2 wrote Devanagari 4/4) |
| Real product pixels | New product drawn from scratch 0/6 (EQ-015); references held the Mokobara bag's colour | Yes |
| Format pack (recomposed, not cropped) | Text cut off wherever a format went unchecked | Yes |
| Timed Indian-language voice, chosen by ear | The most repeated failure (9 jobs), including the direct film | Partly |
| Cheap revision (re-assembly, or one element) | Upwork V4.1 accepted after a US$0 assembly-only repair; RentOK repairs free | Yes |
| Claims checked against the customer's own site | The direct Ascend session flagged "60 min vs 4 h" | Yes |
| Several candidates, customer picks | Practitioners keep about 1 clip in 3–4 | Yes, but it costs money; no automatic selector |
| Brand memory across jobs | "Knowledge died with the job" | Yes; the only asset that compounds |
| The idea and the taste | EVAL-038, E2, E8 ("none of them is knowledge") | **No:** the same LLM is available directly |
| Motion physics, hands, lip-sync | People in Veo: 7 of 14 takes failed; lip-sync 0/5 | **No:** bound by the model |
| Continuity between shots | 7 jobs, never fixed | Unproven |

## 3. Keep / kill

**Keep:**
- Code-set text and the compositor gates (PR #98); image first, then animate; real photos for new products.
- The VO schedule check; blind judging; caps and ledgers.
- The chat front door, with uploads first-class.
- The customer sees the treatment before any spend (this stopped iPhone v3 at US$0.27).
- The CANON-011 briefs and the CANON-013 hold-out split.
- Sarvam for short lines; Lyria with neutral wording.

**Kill:**
- Canon injection into any runtime prompt; the cards arms race.
- LLM gatekeepers and tasters in the release path; still-with-zoom fallbacks; chopping into muted 2–4 s clips.
- Model limits written as rules in the author's card; authorship split across sessions.
- Budget reservations that pause jobs; the builder acting as the customer; mid-order changes.
- Widening the Lab.
- H-CHEAP as a goal: a strong-LLM script costs about US$0.25, so saving on the author is a false economy.

## 4. Solution: "same author, better finish", judged by a fixed exam

### 4.1 The exam, built before any product code
**30 frozen, hashed briefs:**
- **Tuning (6):** from CANON-013's dev half; used for development only, and only on the product.
- **Non-film exam (18):** 6 static ads with exact Hindi/English offer copy; 6 ads from supplied product photos; 4 "animate this image" clips of 6–8 s; 2 format packs.
- **Film exam (6):** Ascend, iPhone Duo, Mokobara, Cumin, ramen, and one from CANON-011.
- The exam includes CANON-013's 8 hold-out cases and at least 3 briefs from real business owners.

**Arms:**
- **B0:** the customer's raw words and assets to the best single model, vendor rewriter on.
- **B1:** a fresh session of the same strong LLM the product uses, told "make this ad; write the prompts; one draw each".
- **P:** the product.
- For stills, B1 and P each get N = 4 draws; for clips, N = 2. This separates finishing value from re-roll value.

**Judges:** the founder plus at least 3 paid outsiders who buy marketing, blind and in random order. Record rank; accept, near-miss or reject; and "would you pay US$60 (static) / US$180 (film)?".

### 4.2 The product P, thin by design
1. **Chat.** The customer's words kept verbatim, plus photos, logo and site URL. A cheap LLM fills at most 10 fields and asks at most 2 questions.
2. **Author.** One strong-LLM call (the same model as B1).
   - **Inputs:** the fields, the photos, a house card of ≤400 words, and a "today's equipment" sheet held as data.
   - **Output:** a treatment plus prompts in each model's own style.
   - **Not included:** no Canon packs, no forms, no reviewer.
   - **Before any spend,** the customer approves or edits the treatment and price.
3. **Generate.**
   - Stills: 4 candidates with product references; the customer picks.
   - Films: whole 8-s scenes with the model's own sound when people speak; 2 candidates for the riskiest scene only.
   - A scene is never replaced by a still.
4. **Finish (code).**
   - Exact copy, logo and end card, recomposed for each format; music.
   - Claims checked against the customer's facts.
   - Each VO line measured and sent back to the author if longer than the shot minus 0.4 s; the customer picks from 3 voice samples.
5. **Checks.** Only measurable faults can block: text bounds and contrast, overlapping audio, aspect ratio, black frames, stray lettering by OCR, and an optical-flow motion check. No LLM verdict can stop a release.
6. **Revision.** "Change X" re-assembles, or regenerates only that element.
7. **Brand shelf.** Facts, photos, logo and accepted outputs stored by ID and reused on the next job.

**Targets:**
- Static ads and "animate this": CpAO ≤US$2 and ≤3× B1; TpAO ≤15 minutes of machine time.
- Films: CpAO ≤US$15; TpAO ≤45 minutes.
- At catalogue prices, cost is not the constraint; acceptance is.

### 4.3 Decision rules
- **Non-film classes pass only if all three hold:**
  - the founder prefers P over B1 on at least 13 of 18 (p ≈ 0.048);
  - a majority of the outsiders agree on at least 12 of 18;
  - P gets would-pay on at least 50%, and at least 20 points more than B1.
- **Films (directional, n = 6):**
  - P wins at least 5 of 6 with at least 3 would-pay: films enter the product.
  - P wins exactly 4: one more cycle on new briefs.
  - P wins 3 or fewer: films stay a handmade service.
- **Change control:** batched; never during an order; each change names the brief it fixes and must re-pass the tuning set; re-tests use new briefs, never the failed exam.

## 5. The first 14 days

| Day | Step | Done when | Cap US$ |
|---|---|---|---|
| 1 | Freeze kitchen deploys; one-page exam spec; founder signs caps | Signed | 0 |
| 1–2 | Assemble and hash the 30 briefs and assets | Frozen | 0 |
| 2 | Recruit 3 outside judges; book days 7 and 12 | Fixed | ~40 in fees |
| 3 | B0 and B1 on the 18 non-film briefs, via API scripts on the Azure VM (not the 8 GB Mac, not the Max quota) | Frozen, with cost and time | 15 |
| 3–5 | P v0, reusing `runtime/compositor`, the VO check and the chat shell; add the motion check and format recomposition | 6 tuning briefs run with no human touch | 10 |
| 6 | P on the 18 briefs | Frozen; any human touch counts as a failure | 15 |
| 7 | Judging session 1 | Verdicts scored by script | 0 |
| 8 | Gate G1: pass → open to 3 outside owners; fail → one fix cycle on 6 fresh briefs | Pass/fail per class | 10 |
| 8–10 | Films: B0, B1, P on the 6 film briefs | 18 film outputs | 110 |
| 11 | Revision test: one change on each of 6 outputs, P vs a B1 re-roll | Cost and time logged | 10 |
| 12 | Judging session 2 | Recorded | 0 |
| 13 | Scorecard per class and arm; Gate G2 for films | Signed | 0 |
| 14 | Offer passed classes to 5 real prospects at catalogue price | Paid, declined with a reason, or no reply in 72 h | 0 |

Model spend: cap about US$170, expected about US$120. About 5 builder-days and 4 founder-hours.

## 6. Kill criteria
- **K1:** non-film classes fail twice (the exam, then new briefs). Stop building the pipeline for them; sell "B1 + hand finishing" as a service, or stop.
- **K2:** films win 3 of 6 or fewer. Make no automated films. When a new video model ships, re-run B1 first: if B1 alone reaches would-pay on 4 of 6, the model does the job without us.
- **K3:** B0 reaches would-pay on 50% or more of a class. That class is a commodity; do not build for it.
- **K4:** outsiders disagree with the founder on more than 40% of briefs. Freeze design changes until at least 10 outside judges have rated.
- **K5 (day 45):** no paid order of at least US$50, and no 3 written "I would pay" statements from non-friends. Stop product work.
- **K6:** a change shipped without the tuning re-run, or during an order, is reverted; a stage that exceeds its cap stops.

## 7. Bet and risk
**Bet:** the same frontier author as the direct prompt, plus deterministic finishing (real pixels, exact copy, timed Indian voice, every format, fact checks, cheap revisions, customer choice). By construction it ties direct on the idea and beats it on the deliverable.

**Risk: the goalpost.** If "much, much better" is judged on creativity alone, by one person who also writes the briefs, no plan can pass. If the founder will not accept "an equal idea, a better-finished deliverable, and outsiders who pay", stop now rather than spend another US$300.

## 8. Disagreements with CONTEXT-SOLUTION.md
1. **Our own wins contradict its main diagnosis.**
   - Accepted Mokobara v2 pasted "four verbatim anchor blocks … unchanged into every still and clip prompt" and used a negative prompt (`ACCEPTED-TEMPLATE.yaml`).
   - The winning direct Ascend film repeated the style line and character description and said "No on-screen text, no subtitles".
   - CQ-001: 1 of 16 decisions lost at the prompt.
   - GenEval 2 and DetailMaster measure single-image attribute accuracy, not whether an ad sells.
   - Prompt hygiene is secondary; authorship, production method and stale model limits are primary.
2. **Its bake-off has no B1 arm.** We could win it and still lose to the ChatGPT and Gemini apps.
3. **It relies on judges we do not have** (PickScore/HPSv3 predict generic aesthetics). Until there are 100+ labels, the customer selects.
4. **Its statistical gate needs thousands of judgements** (100 pairs per item, a 100–300 brief set, a bandit). A 30-brief exam with a hold-out is what we can afford.
5. **The Canon migration is more knowledge engineering with no finished-media evidence.** Compile a check only after a failure has recurred on at least 3 jobs and code can detect it.
6. **§6 (AGENTS.md and hooks) is sound hygiene** but off the path to the golden benchmark.

**Agreed:** a permanent direct arm; references over paragraphs; text by code; motion-only image-to-video prompts (as a hypothesis to test); promotion only on grounded feedback, stored as deltas.
