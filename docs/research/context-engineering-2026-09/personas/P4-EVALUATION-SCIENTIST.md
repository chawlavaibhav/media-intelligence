# Persona 4: The Evaluation Scientist

*One of six persona reviews run on 2026-09-25 over `MEDIA-HISTORY.md` ([00]–[08]) and `../CONTEXT-SOLUTION.md`. Model
output, preserved in substance. Synthesis: `../MASTER-PLAN.md`.*

## 1. Diagnosis

**R1. Decisions were made from one output, on a process where each draw varies a lot.** About 175 decisions, at least 25 reversed, 30 rulings in the last 36 hours, chef card v1→v13 in 26 hours [05][07]. Most reversals followed a single rejected output [00 §5.8]. After one reject, the 95% interval for the true acceptance rate runs from 0% to 97.5%. The record shows how much draws vary:
- EVAL-038 replayed Sonnet's frozen prompts byte for byte and got worse media [03].
- Veo fails at people performing 7 times in 14 (EQ-014, 95% CI 23–77%) [05].
- The P1 inspector rejected 15 of 16 Veo takes [04].
- The keep rate is about 1 clip in 3–4 [05].

Odds multiply across the shots of a film: if each shot works 70% of the time, all four work only 24% of the time. "This film was bad" mostly measured luck, and each redesign chased noise. Tests also changed many things at once: Mokobara v3 changed packs, deep reading, forms, gates, code-built prompts and the three-session split together, so nothing could be attributed.

**R2. There was no control arm until 24 September, and when one appeared it won.** "LLM enrichment beats raw prompting" was never tested as a controlled A/B [02]. The first comparisons were accidental (iPhone Duo, Ascend), and direct Veo won both [05]. Two out of two (CI 16–100%) is thin, but it is the only head-to-head evidence, and it points one way.

**R3. What got measured was never checked against the real target.**
- **Plans instead of media.** EVAL-037, EVAL-038 and the three blind rounds judged plans. The best-scoring board produced the rejected v3 film ("a good plan is not a good film") [04][06].
- **Compliance instead of value.** Code checks passed both accepted and rejected work: 13/13 on PILOT-001 ("still garbage"), 9/9 on the rejected v3, 28/28 on the accepted RentOK V2 [02][04]. A check that passes both cannot predict acceptance; it is hygiene, not quality. The stage forms passed first time with all six defects inside. Claude-as-customer approved Aight Studio "because it followed the brief" [05].
- **The brief set was the opposite of real demand.** CANON-009 found 0 of 30 briefs tested editing a photo or animating an image (the two commonest real requests), while 28 of 30 tested exact text [02].

**R4. Judges were asked the wrong question, with the wrong inputs, on too few items, against a label nobody had defined.**
- **Wrong question.** Every judge gave an absolute accept/reject, but the founder's "accept" tolerates defects: RentOK V2 was accepted with 10 known defects. A judge told to find defects flags accepted work too, hence "stricter than the founder". Holistic VLM "which is better?" is the least reliable format known (49% in GenAI-Arena).
- **Wrong inputs.** In the judge trial only Gemini got video with sound; the others judged contact sheets, which cannot show a slideshow or a robotic voice.
- **Too few items:**

  | Judge | Result | 95% CI |
  |---|---|---|
  | Best taster in the trial | 12 of 16 correct | 48–93% |
  | P1 reviewer | found 1 of 6 known defects | 0.4–64% |
  | Vision judge | 66% agreement (kappa 0.33) | — |

- **Label never defined.** The founder: "it's very difficult to tell what accepted and rejected mean for me" (24 Sep). His own consistency was never measured (he reversed M1/M2 after the reveal; "accept. not good"). No judge can agree with the founder more than he agrees with himself, and nobody knew that ceiling.
- **Text checkers were a separate case, correctly diagnosed.** Readers "repair" misspellings, so code-set text was the right fix.

**R5. There was no regression suite, so every fix was local.** 39 repeating modes: 27 with no machine behind the fix, 8 back despite code, 4 prevented [04]. Each fix was tested only on the job that exposed it:
- the recipe checker stopped unsafe shots and produced slideshows (13 of 14 drafts sent back);
- chef v4's "use people" fix put Meera in all three films;
- the kitchen was changed nine times mid-order.

## 2. Keep / kill

**Keep:**
- Blind founder judging with sealed mappings.
- Pre-registered decision rules applied literally (EVAL-038 "≥3 of 6"; C-3).
- Sealed, hashed evidence and the reserve-before-send ledger.
- **The labelled history, about 400 labels at US$0:**
  - 14 films and 62 images already judged (`mi-p1-evidence`, `1212814`);
  - 311 sealed Lab files with blind verdicts;
  - the 42 typeface picks.
- Code-set text, image-first, and measuring the rendered file (the atlas's largest bucket, B1, 62 rows).
- The founder's "use stats" ruling (Clopper-Pearson). Apply it to design decisions too.
- **CQ-001, the best experiment in the history:** one variable per treatment, ranked blind, and an independent rubric evaluator matched the founder's order (D>C>B>A).

**Kill:**
- Any overall accept/reject from a model used as a release gate.
- Claude-as-customer acceptance (zero evidence).
- Judging plans in place of media.
- Changing the pipeline while a job runs.
- Changing more than one thing per test.
- Design decisions on fewer than 6 outputs.
- Fixes that exist only as notes.
- "Qualified" flags with no report behind them.
- Blocking checks that turn motion into stills.

## 3. Solution: a permanent benchmark, with the founder's taste as data

### 3.1 Golden Brief Set v1 (GBS-1): 40 frozen, hashed briefs (30 dev, 10 vault)

| Class | Dev | Vault |
|---|---|---|
| Edit a supplied photo | 5 | 1 |
| Static ad with exact copy (Hindi/English) | 6 | 2 |
| Animate a supplied image (5–8 s) | 5 | 2 |
| 15-s product film, no speech | 5 | 2 |
| 15–30-s story/brand film with people | 5 | 2 |
| Voiced film (Hindi/Hinglish VO or dialogue) | 4 | 1 |

**Sources:** about 12 already-judged anchors (RentOK, Mokobara, Cumin, iPhone Duo, Ascend, Aight Studio, ramen, skateboard), the directors' 8 round-2 jobs, marketplace briefs and real requests (Rama). All in the customer's voice with real assets.

**Each brief carries:**
- the verbatim prompt and assets;
- a founder-set price anchor per class ("would I pay ₹X");
- 4–6 yes/no must-haves written before generation;
- a hard-fail list.

**Rotation:** 6 dev briefs a month are replaced with real requests. The vault runs at most monthly and is never used for debugging (the 26 Aug lesson).

**Visibility:** the pipeline sees only the prompt and assets, never the must-haves. The judge never sees arm names or plans. The builder sees totals and reason tags, never the vault.

### 3.2 Arms
- **D0, one direct prompt:** the customer's words and assets to the class's best model in one call (for film, one 8-s Veo clip with native sound). The golden-benchmark bar.
- **D1, one smart person with a chatbot:** one strong-LLM session, no repo, ≤15 minutes, writes the model prompts, one retake. Exactly what beat the kitchen twice; the honest bar, because any customer can do it.
- **V, the pipeline version under test.**

D0/D1 are generated once per vendor model version and reused. For every arm, record fully loaded CpAO and machine TpAO.

### 3.3 Judging protocol
Blind pair viewer, phone size, with sound, sides randomised, mapping sealed. Per pair the founder answers:
1. "Which would you rather pay for?" A clearly / A slightly / can't choose / B slightly / B clearly.
2. For each output: "Would you pay [anchor]?" Yes as-is / yes after one small fix / no.
3. If no, one reason from eight: wrong product or world; identity drift; artefact; text or layout; audio or voice; no motion or slideshow; not an ad or boring; off-brief.

About 90 s per film pair and 20 s per still pair. 10% of pairs are silent swapped repeats, which measure the founder's test–retest agreement: the ceiling for any judge.

### 3.4 What counts as a win (pre-registered)
W = wins ÷ (wins + losses), with ties reported separately. PR = pay rate ("yes as-is" or "yes after one small fix") with a 95% CI.

**A version becomes the default only if, on the 30 dev briefs:**
- **Against D1:** at least 20 of 30 non-tie pairs won (sign test p = 0.049; 89% power at a true 75% preference).
- **Against D0:** W ≥ 0.80 and PR(V) ≥ 2 × PR(D0). That is "much, much better", operationalised.
- **Pay rate:** PR(V) ≥ 60%.
- **Against the current default:** W ≥ 0.45, and no class loses 4 or more of its 5 briefs.
- **Cost and time:** CpAO and TpAO within the founder's per-class caps.
- **At milestones:** at least 7 of 10 vault wins against D1 (a sanity check).

**Power:** with one judge and 30 briefs, only large effects are visible: 70% preference has 73% power, 75% has 89%. A 55/45 improvement would need about 600 pairs. So make fewer, bigger changes until a qualified judge exists. Per-class results (n = 5) are warnings, not findings.

### 3.5 Judges earn authority by tier

| Tier | What it may do | What it must show |
|---|---|---|
| T0 | Log only | — |
| T1 (screen) | Rank inside a job; never release | ≥70% agreement with the founder on ≥80 held-out non-tie pairs; ≥85% side-swap consistency |
| T2 (gate) | One specific yes/no check may force a retake, never a downgrade to a still | When it fails an output, the founder agrees ≥90% of the time, on ≥30 labelled defects; recall reported |
| T3 (proxy) | Stand in for the founder on regression runs | Agreement ≥ the founder's test–retest minus 5 points, on ≥150 pairs |

- T3 is re-checked every 4 weeks on 20 fresh pairs, and after any model change.
- Required inputs: films with sound, the customer's words, the price anchor, the founder's question. Pairwise only.
- Calibration: pre-calibrate at US$0 on implied historical pairs (accepted beats rejected within a case). Each dev run adds 60–90 pairs, so T3 is realistic after about 3 runs.
- **Real buyers:** three SME owners judge 20 vault pairs at each milestone, to test whether the founder's taste matches his market.

### 3.6 Turning the failure atlas into checks
Each of the 39 repeating modes gets one of four dispositions:
- **(a) Code on the rendered file, US$0:**
  - overlap, bounds and contrast on every frame;
  - true peak ≤ −1 dBTP;
  - each VO line at most the shot length minus 0.4 s (Ascend put 23 s of speech into 15 s);
  - speech overlap, black frames, MP4 edit list;
  - **motion present**, measured as optical flow per shot ("nobody checked that the result moved").
- **(b) A narrow detector or yes/no vision question:** extra hands; identity drift (face and product similarity across shots); unrequested lettering; blank screens; each must-have present.
- **(c) Plan-time capability lookup with a measured success rate:** hand choreography (15/16 failed), a new product drawn from scratch (0/6).
- **(d) Taste:** no check; only the preference loop can handle it.

Of the 11 most repeated modes, 5 are (a), 2 are (b), 2 are (c) and 2 are (d).

**Rules for checks:**
- **Before it can block:** it qualifies on at least 10 positives and 30 negatives (atlas rows, historical media, EVAL-026's 13 defect injections), and when it fails an output the founder agrees at least 90% of the time.
- **Limits:** at most 12 blocking checks per class. A check firing on more than 30% of candidates is presumed too strict.
- **On failure:** retake or flag. The moment is never removed.
- **PREVENTED** only after 20 clean jobs in that class.
- **Voice gets its own cheap test:** 10 voices × 3 long scripts (≥20 s), judged pairwise, ranked with a Bradley–Terry fit.

### 3.7 Regression discipline
- Every pipeline version is hashed (cards, adapters, checks, models) and frozen while any customer job runs.
- One change per candidate (or one pre-declared bundle), with a written hypothesis.
- **Gate 1 (US$0):** tests, plus code checks replayed on stored assets.
- **Gate 2 (about US$15):** "smoke-6", one brief per class, T1-judged against the previous version. Stop if it loses 4 or more of 6.
- **Gate 3 (about US$110, about 50 founder minutes):** the full dev run, weekly, not per change.
- **Auto-revert** if W against the previous version is below 0.40.
- **A single bad production output opens a ticket and a brief candidate.** It never changes the design directly. This rule alone would have prevented most of the 25 reversals.

### 3.8 Measuring the Canon on screen (CANON-ABL-1)
**Arms:** V (with the Canon); V without the Canon (same models, recipes, seeds); V + 25 random claims (a volume control).

**Outcome:** founder pairwise verdicts on finished media, never plans.

**Stills first:** 30 still briefs × 2 seeds = 60 pairs, about US$20 and 25 founder minutes.

**Pre-registered rule.** The Canon stays in the generation path only if both hold:
- V beats V-without-Canon in at least 37 of 60 pairs (p = 0.046);
- V also beats the random-claims arm.

**Films** (14 briefs, about US$85) run only if stills show W ≥ 0.55.

**If it fails:** the Canon keeps its proven roles (copy and audience review, a source of checks) and leaves the planner prompt.

## 4. The first 14 days (founder time about 4–5 h; caps are proposals)

| Day | Step | Done when | Cap US$ |
|---|---|---|---|
| 1 | Draft 60 candidate briefs; the founder picks 40 and sets price anchors (30 min); hash them | 40 sealed briefs | 0 |
| 2 | Blind pair viewer (static local HTML) and label format; dry run on 10 historical pairs | 10 labels; seconds per pair measured | 0 |
| 3 | Relabel history: 60 pairs from the 14 films and 62 images, including 6 swapped repeats | ≥60 pairs + a test–retest estimate | 0 |
| 3–5 | Generate D0 and D1 on the 30 dev briefs, with no code changes | 60 sealed outputs, each with cost and time | 110 |
| 5 | Live kitchen (`11bfc5f`) on the 16 still and animate briefs only; its films already lost 2 of 2 | 16 outputs | 20 |
| 6 | Founder session 1 (about 70 min): D1 vs D0 (30 pairs), kitchen vs D1 (16 pairs) | Signed result with CIs. If D1 wins ≥12 of 16 non-tie pairs against the kitchen (p = 0.038), the kitchen stops being the default and D1 becomes the floor | 0 |
| 6–8 | Atlas → checks: a disposition per mode; build and qualify the (a) checks on history | Precision/recall report; table of mode → mechanism | 0 |
| 7–10 | Calibrate 3 pairwise judges (Gemini 3.1 Pro with video and sound, plus two others) on ≥120 founder pairs, both side orders | A tier per judge, with CIs | 25 |
| 9–12 | Candidate V1 through smoke-6, then the full dev run | 30 outputs with CpAO and TpAO | 15 + 110 |
| 12 | Founder session 2 (about 50 min): V1 vs D1 and V1 vs D0 | Ship-gate verdict under §3.4 | 0 |
| 13–14 | CANON-ABL-1 on stills; voice-casting test | Signed Canon-on-stills result; voice ranking | 20 + 5 |

**Totals:** caps about US$305; expected spend about US$250. Store media off the Mac (about 1–1.5 GB) and run one session at a time.

## 5. Bet and risk
**Bet:** the founder's blind pairwise labels become the project's currency. Ship/revert, routes, judge qualification and the Canon verdict are all computed from "which would you pay for" pairs on a fixed set with a permanent direct arm. T3 is realistic after about three runs, after which his taste can be applied without him judging every output.

**Risk:** the protocol breaks under pressure: one bad output, then a redesign within the hour. D1 may also win everything; that would be the answer, saying the value lies in finishing, selection and price, not the layer.

## 6. Disagreements with CONTEXT-SOLUTION.md
1. **A stills-first bake-off answers the wrong question.** Stills already work (Lab 55/75, GPT Image 2 11/12, P1 poster). Every whole-system rejection was a film, so films belong in the first benchmark.
2. **CQ-001 says prompts are not the bottleneck for film:** only 1 of 16 decisions was lost at the prompt, and the prompts-only arm matched baseline. The direct-Veo wins came from one writer, whole 8-s scenes and native sound. Compare whole pipelines on finished media, not prompt compilers.
3. **About 100 pairs per knowledge item is unaffordable with one judge.** Batch changes, or make no small changes until a T3 judge exists.
4. **PickScore/HPSv3 are trained on generic preference** and do not track "would an Indian SME pay"; nothing equivalent exists for video with sound. Keep them out of selection until calibrated.
5. **Best-of-N assumes a selector that can find the good candidate.** Ours could not. Selector accuracy, not N, is the binding term.
6. **A bandit needs volume;** there are about 20 judged jobs in 80 days. Use fixed recipes and explicit A/B tests.

**Agreed:** judge media, not plans; the direct arm is permanent; many narrow yes/no checks beat one overall verdict; lessons are evidence-backed deltas; no rule is promoted by argument.
