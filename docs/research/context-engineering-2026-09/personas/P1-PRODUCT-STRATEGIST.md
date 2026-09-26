# Persona 1: The Product Strategist

*One of six persona reviews run on 2026-09-25 over `MEDIA-HISTORY.md` ([00]–[08]), CANON-009, CANON-011 / marketplace
demand research, the 16 Sep architectural audit, and `../CONTEXT-SOLUTION.md`. Model output, preserved in substance.
Synthesis: `../MASTER-PLAN.md`.*

**The short answer:** in 80 days and about US$340, the project never gave a finished asset to someone who could pay, for
a job they had actually asked for. It tuned the pipeline against one judge, on briefs he wrote himself, in the hardest
media class. Most of the other problems follow from that.

## 1. Diagnosis

**RC1. No customer in the loop.** The founder was the designer, the customer and the only judge at once.
- Every brief after August was the founder's own or Claude-as-customer [00 §5.9]. The three overnight films were "accepted" only by Claude.
- One outside beta user (Rama), invited at 15:24 on launch day; "rama work failed" at 15:31, because the page was a form. The ~50 beta files for judge qualification never happened.
- Upwork: the profile went live 15 Sep with 150 Connects and a US$1,000 month-one target; no order is recorded.
- Accepted spec films were never sent to the brands (C-8).
- The whole learning signal was about 76 judged pieces from one person, although his own ruling is "taste is not a rule".

**RC2. The demand evidence was collected, then ignored. The testing ground became the hardest class.**
- **CANON-009 (26 Aug):**
  - editing a supplied photo had 82,976 real requests in one dataset and **0 of 30** briefs;
  - animating a supplied image had 1.70M+ requests and **0 of 30** briefs;
  - exact text had 28 of 30 briefs and no evidence that anyone asks for it.
- **CANON-011:** 18 real paid Upwork jobs. Exact text 1/18; customer supplies an asset 16/18; something must stay the same across outputs 13/18; more than one deliverable 10/18.
- The founder's Upwork research ranked catalogue work at US$30–45 per approved video as the top job type.
- The Lab had already measured these jobs as the easy ones:
  - stills: NB2 and GPT Image 2 each 11/12, about US$0.06–0.07 per accepted image;
  - photo edits: Seedream 10/12;
  - image-to-video: Kling 8/8, Wan 8/8.
- Yet from 14 Sep almost every job was a from-scratch film with people, hands, voice and Hindi. That is where models fail most (voice in about 9 jobs, drift in 7, slideshow in 6) and where one strong prompt already won (2 of 2).
- So the product was aimed where the layer had least to add and most to break.

**RC3. The "intelligence layer" was never defined as something a buyer can see.**
- It was defined as the founder's picture of a creative process: 37 books and 1,300 claims, five forms, a 17-role kitchen.
- Three moat theories were stated and each disproved: the router (6 Aug), cheap model plus Canon (0/6), cheap-beats-strong on films (25 Sep).
- What won was visible and mechanical: text by code 4/4 against 0/4; real product photos (Veo turned the Apple logo black; a new phone drawn from scratch 0/6); a still first, then animated.
- The layer cost more than the media: on the only accepted poster, planning was US$1.87 of US$2.28.

**RC4. No fixed test set, so decisions followed single examples.**
- At least 25 reversals, 30 rulings in 36 hours, chef card v1→v13 in 26 hours, nine fixes mid-order.
- Checking swung from maker–checker always → one checker → gatekeeper fired.

**RC5. The wrong cost was optimised.**
- The ledger counted model dollars, but the binding costs are owner time and acceptance rate.
- The 16 Sep audit:
  - model spend is 1–7% of the Upwork price;
  - the owner spends 1–8 hours a job;
  - at 10 jobs a month the business loses about US$440;
  - break-even needs ≤1.7 owner-hours a job.
- Time to acceptance: Upwork intro 7 h 54 m; Mokobara 10 h 24 m; Ascend 1 h 06 m in the kitchen against 6 minutes direct.
- Only US$33.6 of about US$340 produced accepted work. No price was ever tested with a buyer.

## 2. Keep / kill

**Keep:**
- Code-set copy and logos, Typeset, and the production code checks (PR #98).
- Real product photo as reference: drawn labels are right only about 29% of the time.
- Still first, then animate; motion-only prompts for image-to-video.
- The chat studio shell (invites, job DB, ledger, deploy).
- Blind judging, sealed evidence, CpAO and TpAO; the Lab's measured results.
- Rules: the customer owns the budget; the founder is never inside a running job; the July intake rule (ask only for facts only the customer knows; the machine makes creative choices; work out specs yourself).
- The CANON-011 briefs, the Upwork/Fiverr demand research and the D2C prospect list.

**Kill:**
- The multi-role kitchen and rewriting cards as the improvement method.
- The Canon in the running pipeline, and any new Canon work for 30 days.
- Overall-verdict AI judges that block release (the best judge in the trial passed only 4 of 7 accepted pieces).
- Voiced story films as a paid product until they beat A1.
- Worst-case reservations (Ascend paused for budget five times; ramen reserved US$18.92 for calls that cost US$0.81).
- Spec ads never sent; unsupervised overnight builds; changing the product while a customer uses it.
- The WhatsApp small-shop bot: Meta now offers free AI ad creation inside WhatsApp Business in India.

## 3. The solution

**Customer:** D2C and e-commerce brands, and the freelancers and agencies who make their ads. This matches the founder's 16 Aug target list and the Upwork buyers who pay per approved asset.

**The job, in the customer's words:** "Here is my product and what I want. Give me on-brand creative in every format I need, with my exact words in English or Hindi, showing my *real* product, in minutes. Charge me only for what I approve, and remember my brand next time."

**Why not call Veo or Nano Banana directly?** A direct prompt:
- redraws the product;
- garbles Indian-language text;
- forgets the brand between sessions;
- gives one output in one format;
- leaves all the checking to you.

Each of these is measurable against a direct prompt on the same brief. Creative quality comes from a strong model, several candidates and the buyer's own pick, not from pasting book knowledge into prompts.

**Media classes.** The chat accepts every request; a class is sold only once it passes the benchmark.

| Class | Demand | Measured success | Where the layer beats direct | Decision |
|---|---|---|---|---|
| S1 product ad still from the real photo, exact copy, 4 formats | 16/18 jobs supply assets; the P1 poster | NB2/GPT Image 2 11/12; text by code 4/4 | Real product, exact copy, formats, brand kit | Launch day 7 if it passes |
| S2 edit my photo | 82,976 requests; 0/30 briefs | Seedream edit 10/12 | "Change only X", before/after, formats | Launch with S1 |
| M1 animate my image (5–8 s, no speech) | 1.70M+ requests; one real Upwork job | Kling 8/8, Wan 8/8, Veo Fast 5/8 | Motion-only prompts, 2 takes, code text, music | Beta day 9 |
| M2 short product film from approved stills | Upwork catalogue at US$30–45 a video | Mokobara v2 accepted at US$7.86 | Approved stills keep shots consistent | Head-to-head test after M1 |
| F voiced film with people and a story | Mostly the founder's briefs | Voice failed ~9 jobs; lip-sync 0/5; direct won 2/2 | None shown yet | Free and labelled "draft"; one LLM session writing whole 8-s Veo scenes with native sound; every order becomes feedback data |

**Pipeline:**
1. **Chat intake (cheap LLM).** The verbatim words, files and brand references in; operation / class / formats / exact copy / language / missing facts out. At most 2 questions, only for facts only the customer knows.
2. **Brand shelf (code).** Logos, fonts, colours, product photos, facts from the product page, and past approvals and rejections, passed as references, never pasted into prompts as text.
3. **Director (one strong LLM, one pass).** A plan of ≤150 words and ≤6 must-haves per shot. No Canon. ≤US$0.05 a job.
4. **Adapter.** Prompts in each model's style: 30–80 words for stills; motion only for image-to-video; no "don't do X" sentences.
5. **Generate.** Stills: 4 candidates plus 1 from the A1 baseline, mixed in without a label. Clips: 2 takes from the picked still.
6. **Hard checks (code and detectors only).** Stray text, product matches the reference, hand count, safe margins, contrast, exact copy, speech fits the clip. One silent retry on failure; no AI verdict on overall quality.
7. **Customer picks** from 2–4 candidates: accept, "change only X", or reject with a reason. The pick is the quality label ("machine makes stuff with the help of the user").
8. **Compose (code).** Copy, logo, every format.
9. **Ledger.** Per class: CpAO counting every call, TpAO, and how often buyers pick the A1 candidate.

**Decision rules:**
- **Fixed test set:** 30 frozen, hashed briefs, at least 20 from real demand with real product assets. S1 10, S2 5, M1 8, M2 5, F 2.
- **Arms:** A0 (the customer's raw words to the model); A1 (one strong LLM writes the prompt in one pass); P (the pipeline).
- **A class ships when, judged blind:**
  - P is accepted at least 20 points more often than A1;
  - at least 70% pass "would I pay?" from the founder **and** from at least 2 outside buyers;
  - cost and time are within target.
- **Targets:**

  | Class | CpAO | Time |
  |---|---|---|
  | S1 (per concept, 4 formats) | ≤US$0.60 | first preview ≤3 min, delivered ≤10 min |
  | S2 | ≤US$0.30 | — |
  | M1 (per 8-s clip) | ≤US$2 | ≤15 min |
  | M2 | ≤US$8 | ≤45 min |

- LLM spend stays at or below 20% of media spend.
- **If P doesn't beat A1 for a class:** ship A1 plus the mechanical layer for that class and delete the director. No stage stays unless it wins head-to-head.
- **Change control:** nothing changes after a single rejection. Changes are batched and released at most every 48 hours; every release re-runs the capped test set and must not lower any class's acceptance.
- **Pricing hypotheses:** pay per approved concept; S1 at ₹299 against ₹799, M1 at ₹999 against ₹1,999; price at least 10× CpAO.

**The moat, honestly: none today.** Every candidate needs customers first:
1. **The brand shelf:** a customer's second job comes out better and faster than their first.
2. **Buyer picks:** they tune recipes and judges to buyers' taste ("the ledger is the business").
3. **Exact Indian-language text.**
4. **Pay per accepted outcome.**

## 4. The first 14 days (about US$120 plus the existing server)

| # | Days | Step | Done when | Cap US$ |
|---|---|---|---|---|
| 1 | 1 | One-page founder ruling: classes, three arms, ship/kill rules, caps, change control. Stop kitchen film orders | Signed | 0 |
| 2 | 1–2 | Fixed set from 6 real people (Rama, the ramen bar, 4 more), usable CANON-011 briefs, real products of 8 prospect brands | 30 briefs frozen, each with the customer's own "acceptable" line | 0 |
| 3 | 2–3 | Baseline S1/S2: A0 against A1 (15 briefs × 2 arms × 2 draws), judged blind | Acceptance rate, cost, time per arm | 10 |
| 4 | 3–6 | Pipeline v0 for stills, reusing P1's DB, compositor, Typeset, ledger and chat; no new roles; build on the Azure server or in cloud sessions | One S1 job end to end live in ≤10 min for ≤US$0.60 | 10 |
| 5 | 6–7 | Stills test: P against A1 on 15 held-out briefs, plus P without the director and P without the checks | Ship/no-ship S1 and S2 | 20 |
| 6 | 7–9 | M1: 8 briefs × {A1, P} × 2 takes | Acceptance table; ship or not | 30 |
| 7 | 8–13 | Real buyers: free S1 packs for 10 prospect brands from their own photos, plus a paid offer; 5–8 Upwork bids on pay-per-approved jobs (not the research's sample proposals: they claim a six-person team); onboard 5 small businesses | ≥3 outside buyers have judged 10+ assets; ≥1 paid order of any size | 25 + ~12 Connects |
| 8 | 11–13 | Brand-shelf test: a second job for 3 repeat customers | Acceptance and time, job 1 vs job 2 | 10 |
| 9 | 14 | Scorecard | Published | 0 |

## 5. Bet and risk
**Bet:** for product creative, a thin layer (real product, exact words, brand memory, 4 candidates, buyer picks) beats both A0 and A1 by at least 20 points of acceptance at under US$1 per accepted outcome.

**Risk:** the founder judges the plan by the next film he dislikes and redesigns mid-sprint; the signed change-control rule is the only defence. A close second is that free tools (Meta's WhatsApp ad maker, Google's Pomelli) may already be good enough; step 7 finds out.

## 6. Disagreements with CONTEXT-SOLUTION.md
1. **It answers the wrong first question** (how knowledge reaches the model, instead of which job for which customer). Weight the brief set toward real buyer demand and outside judges.
2. **Its direct baseline is too weak.** Add A1, the one-session LLM writer: it beat us twice, and any buyer can do it with ChatGPT or Gemini.
3. **Too much machinery for zero customers** (a router, preference scorers, a 30-check registry, Canon migration). Let the buyer pick until there are 500+ buyer labels.
4. **The buyer should pick, not the machine.** It is quicker to build, creates labels, and fits "taste is not a rule".
5. **The Canon is a sunk cost for 30 days.** The blind rounds were won on structure ("none of them is knowledge").
