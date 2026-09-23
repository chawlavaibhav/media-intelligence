# P1 v2 — founder's checklist

For Vaibhav, to check the P1 v2 build **before any money is spent or any live test is run**.
The builder fills the right-hand columns. For each item, open the evidence and ask the question in plain words.
Status: **Done / Partly / Not done**. Spec references (§) point to `P1-V2-BUILD-SPEC.md`.

---

## A. Ground rules held

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| A1 | Was anything paid for (any AI, picture, video or music call)? The answer must be no. | | |
| A2 | Was anything created or changed on Azure, Google Cloud or AWS? The answer must be no. | | |
| A3 | Is the work on its own branch with a draft PR, not merged? | | |
| A4 | Did the builder ever act as the operator (pick takes, override checks, release files)? The answer must be no. | | |

## B. Storage — "where is everything kept?" (§7)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| B1 | **Job file:** show me one job's complete record — order, every form, money, every file, checks, verdict. | | |
| B2 | **Job file:** if a poster is redone, is the old version still there? (v1 lost it.) | | |
| B3 | **Customer shelf:** show me a customer's shelf — logo, fonts, colours, product photos with roles, characters, master plates. | | |
| B4 | **Customer shelf:** does the customer approve each item once? Are old versions kept? | | |
| B5 | **Customer shelf:** can one customer ever see another customer's shelf? The answer must be no (show the test). | | |
| B6 | **Kitchen library:** show me the four sections — cookbooks, failure diary, recipe library, equipment sheet. | | |
| B7 | **Equipment sheet:** does it say Veo "cannot" do hands working zips, with the evidence it came from? | | |
| B8 | **Rulebook:** show me every worker's card (mission, vision, KRA) and the form schemas, with version numbers. | | |
| B9 | **Lesson queue:** show me where lessons wait for my approval, and how I approve, edit or reject one. | | |

## C. The workers — "who does what?" (§3, §5)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| C1 | Are there exactly the workers in the diagram: 7 AI workers, 5 code helpers, and 2 people? | | |
| C2 | Does every AI call include that worker's rulebook card, and record which version was used? | | |
| C3 | Which model does each worker use, and where is that set? (It must be config, not hard-coded.) | | |
| C4 | Are the chef and the judges (recipe checker, big taster) from different AI companies? | | |
| C5 | Is the change-taker merged into the waiter? | | |
| C6 | Does each worker fill exactly one form, checked against its schema? | | |

## D. The forms (§4)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| D1 | Is the customer's exact wording stored once and never edited? Does it reach **every** AI worker, including the small taster? | | |
| D2 | Does the waiter label every photo's role (product view, detail, lifestyle, infographic, logo)? | | |
| D3 | Does the waiter flag contradictions — for example a wrong photo label like the v1 film's? | | |
| D4 | **Feasibility form exists:** for each product part and each action, does it have a photo? Which route can make it — reliable, risky or cannot? | | |
| D5 | Does every shot in the recipe name its route, its action type and what it starts from (master plate or previous shot)? | | |
| D6 | Can the recipe checker say "approve", "add steps" or "send back"? Does it predict whether the customer will accept? | | |
| D7 | Does the small taster compare each shot with the previous one and with the master plate? | | |
| D8 | Is there a Lessons form, and a Production log from the head cook? | | |

## E. The flow and the send-backs (§6)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| E1 | **The backpack test:** fed the v1 film order and photos, does the pantry check block "hands pulling zips" before any spend? | | |
| E2 | With no photo of the inside, does the job pause and ask the customer for one? | | |
| E3 | If the recipe checker says "send back", does it go to the chef, with a limit of 2 rounds? | | |
| E4 | If a shot fails twice, does it go back to the chef to re-plan, instead of a third identical try? | | |
| E5 | **Big taster "no":** "fix" redoes only the broken shots, "fail" goes back to the chef, and after 2 rounds it stops and asks me. | | |
| E6 | Is the riskiest shot made first, and does the job stop if it fails? | | |
| E7 | Is every film shot built from the master plate and the shot before? Show the production log. | | |
| E8 | **Only I can override:** show the test where the builder, a script and the admin tool all try to override and are refused. | | |
| E9 | When I override, is my reason saved and shown? | | |
| E10 | Does a customer change go to the waiter, and then only to the affected station? | | |

## F. Retrieval — "does the chef read only what it needs?" (§8)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| F1 | Does the librarian build a tray, rather than sending all 25,000 words of cookbook? What is the cap for each worker? | | |
| F2 | Does the tray include past failures that match the planned shots? Show one example. | | |
| F3 | Does the tray include similar past recipes with their outcomes? | | |
| F4 | Is the tray logged, so I can see what the chef knew for any job? | | |

## G. Learning (§7.5, §4.11)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| G1 | Does every finished job — accepted, rejected or abandoned — produce lessons? | | |
| G2 | Is nothing changed until I approve it? | | |
| G3 | After I approve an equipment-sheet lesson, does the next job actually use it? (Show the test.) | | |
| G4 | Does a second job for the same customer reuse their shelf (character, master plate, logo)? | | |

## H. Cost (§9.4)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| H1 | What is the estimated AI reasoning cost of a simulated image job, per worker? (Target ≤ USD 0.03, about ₹3.) | | |
| H2 | And for a simulated film job? (Target ≤ USD 0.30, about ₹25.) | | |
| H3 | Does the quote show the reasoning cost, and does the ledger record actual cost per worker? | | |
| H4 | Is a decision-model slot (such as Jev) available for yes/no workers, without being required? | | |

## I. Judges' qualification (§10)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| I1 | Is there a test set of old cases with my known verdicts, for all three judges? | | |
| I2 | What are the pass marks, and do I agree with them? | | |
| I3 | Until a judge passes, does its "no" still block, and does its "yes" still need me to confirm? | | |
| I4 | Can the harness run live only with my separate authorisation? | | |

## J. Tests and reproducibility (§11, §14)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| J1 | Do all 16 required tests exist and pass? Show the output. | | |
| J2 | Do the old v1 tests still pass? If any were removed, which ones, and why? | | |
| J3 | Do full simulated image and film journeys work through the web app, end to end? | | |
| J4 | What are the exact commands to reproduce everything from a fresh checkout? | | |
| J5 | What did the builder change from the spec, and why? | | |
| J6 | What questions are still open for me? | | |

---

**Only when every item is Done, or explained, do we authorise money for live tests** — starting with the judges'
qualification, then one image job, then one film job, each with its own spend record.
