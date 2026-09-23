# P1 v2 — founder's checklist

For Vaibhav, to check the P1 v2 build **before any money is spent or any live test is run**.
The builder fills the right-hand columns. For each item, open the evidence and ask the question in plain words.
Status: **Done / Partly / Not done**. Spec references (§) point to `P1-V2-BUILD-SPEC.md`.

**Filled in by the builder on 2026-09-23** — branch `claude/p1-v2-build`, draft PR
https://github.com/chawlavaibhav/media-intelligence/pull/109. Test file names below are under `product/tests/`.

> **Amendment 1 has been applied** (your decisions of 2026-09-23). See the **Amendment 1** section at the end. Where it
> differs from the summary and sections A–J below, the Amendment 1 section describes the product as it is now: nobody
> waits for you any more, and the kitchen learns by itself.

## Summary in plain words

**What works (in simulated mode, USD 0):**

- **The rejected film would be stopped before any spend.** Given the rejected Reel's order and photos, the new "pantry check" says the video model *cannot* do hands working zips. It pauses the job, offers the customer a still instead, and nothing is spent. Given v1's own plan, the recipe checker sends it back twice and then stops for you. This is also checked against the real 23-Sep records.
- **Every film shot now comes from one master plate.** The customer approves that "look of the film" once; each shot is built from it and from the end of the shot before. The production log proves this for every shot.
- **Only you can override.** The builder, scripts, the admin tool, the worker and ordinary staff are all refused, and each refusal is logged. Your overrides need a written reason, which appears on the release report.
- **Other controls hold:**
  - A checker's "no" now binds: retry once, then the chef re-plans, then you decide.
  - The riskiest shot goes first.
  - The big taster's "fix" redoes only the shots it names.
  - Old files are never overwritten.
- **The kitchen learns, but only with your approval.**
  - Every closed job (accepted, rejected or abandoned) writes lessons, and nothing changes until you approve one.
  - An approved equipment lesson changes the very next job's pantry check.
  - A second job for the same customer reuses their logo, colours, hands reference and master plate. Another customer sees none of it.
- **Full image and film journeys work through the web app**, with the customer and you each using your own pages.

**What doesn't meet the target, or isn't done:**

- **AI reasoning cost is well below v1 but misses your targets.** Estimated at the configured models' list prices:
  - A film is about **USD 0.38** against the **USD 0.30** target; v1 actually spent USD 2.33.
  - An image is about **USD 0.25** against the **USD 0.03** target; v1 spent USD 1.87.
  - The strongest model writing the recipe costs about USD 0.13 on its own, so the image target is out of reach with it. This needs your decision (question 1 below).
- **No judge is qualified yet.** The test set and harness are built, but qualification needs a live run you authorise. Until then the judges' "no" blocks and their "yes" waits for you, so every job currently asks you to confirm the recipe and to confirm at the final check.
- **The judges' test set is small on this machine.** 14 cases with known verdicts; the MOKO7 films and the older RentOK, Cuminco and Upwork media are not in the evidence repository.
- **Nothing has run against a real model.** Every behaviour is proven in simulation only. Live models may misjudge photos or actions in ways simulation cannot show; that is what the qualification run and the first live jobs will test.

## A. Ground rules held

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| A1 | Was anything paid for (any AI, picture, video or music call)? The answer must be no. | **Done** — nothing paid | Every run used the defaults `MI_PROVIDER_MODE=simulated` / `MI_REASONING_MODE=simulated` (`product/config.py`). No API keys exist in this environment. No `--live` command was run: `judges.py --live` was only run to prove it is refused without your session. |
| A2 | Was anything created or changed on Azure, Google Cloud or AWS? The answer must be no. | **Done** — nothing | No cloud command or credential was used; all work stayed in this repository and a local test folder. |
| A3 | Is the work on its own branch with a draft PR, not merged? | **Done** | Branch `claude/p1-v2-build`; draft PR #109, based on `claude/p1-v2-build-spec`, not merged. |
| A4 | Did the builder ever act as the operator (pick takes, override checks, release files)? The answer must be no. | **Done** — no | The only founder actions were made by the test founder account inside automated tests. The code refuses the builder: `test_v2_skeleton` `test_worker_script_operator_customer_and_builder_strings_are_refused_and_logged`. |

## B. Storage — "where is everything kept?" (§7)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| B1 | **Job file:** show me one job's complete record — order, every form, money, every file, checks, verdict. | **Done** | The operator job page `/ops/jobs/<id>` shows every form (order slip → lessons), trays, cost report, production log, ledger, AI calls, assets, gateway and events. Stored in `mi.sqlite3` + `media/<job>/`. Test: `test_v2_journeys` (the full film). |
| B2 | **Job file:** if a poster is redone, is the old version still there? (v1 lost it.) | **Done** | `test_v2_production` `test_a_recomposed_poster_is_a_new_file_and_the_first_cut_is_still_on_disk_unchanged`; the store refuses to reuse a path: `test_v2_storage` `WriteOnceFiles`. |
| B3 | **Customer shelf:** show me a customer's shelf — logo, fonts, colours, product photos with roles, characters, master plates. | **Done** | The customer page `/shelf`; code `product/shelf/`. Brand fonts are used by the sign painter: `test_v2_storage` `BrandFontsFromTheShelf`. |
| B4 | **Customer shelf:** does the customer approve each item once? Are old versions kept? | **Done** | `test_v2_storage` `test_items_are_proposed_approved_once_and_new_versions_keep_the_old`. |
| B5 | **Customer shelf:** can one customer ever see another customer's shelf? The answer must be no (show the test). | **Done** — no | `test_v2_storage` `test_another_account_can_never_read_or_decide_this_shelf`; through the web: `test_v2_founder_tools` (the rival sees nothing and gets 404); in a job: `test_v2_learning` `SecondJobReusesTheShelf` (nothing reaches the rival's waiter or chef). |
| B6 | **Kitchen library:** show me the four sections — cookbooks, failure diary, recipe library, equipment sheet. | **Done** | `/ops/library` (equipment sheet, recipe library, failure diary); cookbooks = Canon split into decision pages (`library.cookbook_pages`). Code `product/library/`. Test `test_v2_storage` `Library`. |
| B7 | **Equipment sheet:** does it say Veo "cannot" do hands working zips, with the evidence it came from? | **Done** | Row EQ-001 in `product/library/equipment_seed.yaml`: *cannot*, 16 samples, evidence EV-0923-FILM + ATLAS-B7. Test `test_the_equipment_sheet_says_veo_cannot_do_hands_working_zips_with_its_evidence`. |
| B8 | **Rulebook:** show me every worker's card (mission, vision, KRA) and the form schemas, with version numbers. | **Done** | `/ops/rulebook`; data in `product/rulebook/cards/*.yaml` and `product/rulebook/forms/*.yaml`. Test `test_v2_skeleton` `RulebookAndForms`. |
| B9 | **Lesson queue:** show me where lessons wait for my approval, and how I approve, edit or reject one. | **Done** | `/ops/lessons` (approve / approve with my edit / reject, with a reason). Test `test_v2_founder_tools` `test_the_founder_approves_edits_or_rejects_lessons_in_the_web_app_and_an_operator_cannot`. |

## C. The workers — "who does what?" (§3, §5)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| C1 | Are there exactly the workers in the diagram: 7 AI workers, 5 code helpers, and 2 people? | **Done** | `product/rulebook/__init__.py` (`AI_WORKERS`, `CODE_WORKERS`, `PEOPLE`); modules in `product/stations/`. Test `test_every_worker_in_the_diagram_has_a_card...`. |
| C2 | Does every AI call include that worker's rulebook card, and record which version was used? | **Done** | `product/ai.py` puts the card first in every call and records `card_version` per call and on each form. Test `test_v2_learning` `test_every_call_records_its_card_version_and_an_approved_rulebook_lesson_bumps_it_for_the_next_job`. |
| C3 | Which model does each worker use, and where is that set? (It must be config, not hard-coded.) | **Done** | `product/config.py` `DEFAULT_WORKER_MODELS`, overridable by `MI_MODEL_<WORKER>`. Chef = Azure OpenAI gpt-5.6-sol; recipe checker, big taster and the small taster's escalation = Gemini 3.1 Pro; waiter, pantry checker, small taster and diary writer = Claude Haiku 4.5. Shown on `/ops/rulebook`. Test: no model name appears in any station file. |
| C4 | Are the chef and the judges (recipe checker, big taster) from different AI companies? | **Done** | `config.check_independence` refuses to start otherwise. Test `test_models_are_configuration_the_chef_and_judges_must_be_different_companies...`. |
| C5 | Is the change-taker merged into the waiter? | **Done** | The waiter writes both Understanding and Change request (`stations/waiter.py`, `cards/waiter.yaml`). |
| C6 | Does each worker fill exactly one form, checked against its schema? | **Done** | `ai.py` returns one form per call, validated (with one repair re-ask) and stamped; `orchestrator.put_form` validates again before storing. |

## D. The forms (§4)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| D1 | Is the customer's exact wording stored once and never edited? Does it reach **every** AI worker, including the small taster? | **Done** | Frozen and fingerprinted at submission; the order slip carries it; the waiter's copy is forced byte-equal. `test_v2_journeys`: all 7 AI workers carried the same fingerprint. Also `test_v2_front_of_house` `CustomersExactWordsReachEveryAiCall`. |
| D2 | Does the waiter label every photo's role (product view, detail, lifestyle, infographic, logo)? | **Done** | `test_the_waiter_labels_every_photo_and_flags_the_wrong_photo_note` → photo 1 product_view, 2 infographic, 3 lifestyle. |
| D3 | Does the waiter flag contradictions — for example a wrong photo label like the v1 film's? | **Done** | Same test. The v1 note said photo 2 was people; it is the open-pocket infographic, and this is flagged. I checked it against the real evidence photos. |
| D4 | **Feasibility form exists:** for each product part and each action, does it have a photo? Which route can make it — reliable, risky or cannot? | **Done** | `rulebook/forms/feasibility.yaml`, `stations/pantry.py`. Tests `test_v2_front_of_house`. |
| D5 | Does every shot in the recipe name its route, its action type and what it starts from (master plate or previous shot)? | **Done** | Required fields in `rulebook/forms/recipe.yaml`, enforced by the schema. |
| D6 | Can the recipe checker say "approve", "add steps" or "send back"? Does it predict whether the customer will accept? | **Done** | `rulebook/forms/recipe_check.yaml` (`verdict`, `predicted_acceptance`) plus code rules that force send_back. Tests `test_v2_kitchen`. |
| D7 | Does the small taster compare each shot with the previous one and with the master plate? | **Done** (simulated only) | It is given the master plate and the previous end frame, and its form has `matches_master_plate` / `matches_previous_plate`; a "no" on either rejects (`head_cook._usable`). How well a real model compares is untested until qualification. |
| D8 | Is there a Lessons form, and a Production log from the head cook? | **Done** | `forms/lessons.yaml`, `forms/code_forms.yaml` (production_log). Tests `test_v2_learning`, `test_v2_production` `ContinuityChain`. |

## E. The flow and the send-backs (§6)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| E1 | **The backpack test:** fed the v1 film order and photos, does the pantry check block "hands pulling zips" before any spend? | **Done** | `test_hands_zipping_the_bag_is_cannot_and_the_job_pauses_for_the_customer_with_an_alternative_at_usd_0`, and on the verbatim evidence `OnTheVerbatimEvidence`. v1's own recipe: `test_the_rejected_films_recipe_is_sent_back_by_code_for_every_mechanism_shot...`. |
| E2 | With no photo of the inside, does the job pause and ask the customer for one? | **Done** | `test_an_order_needing_the_front_pocket_open_with_no_photo_of_it_asks_the_customer_for_one` (it continues once the photo arrives). |
| E3 | If the recipe checker says "send back", does it go to the chef, with a limit of 2 rounds? | **Done** | `test_after_two_send_backs_only_the_founder_can_override...`; the table in `product/flow.py` `SEND_BACKS`. |
| E4 | If a shot fails twice, does it go back to the chef to re-plan, instead of a third identical try? | **Done** | `test_a_risky_shot_rejected_twice_goes_to_the_chef_then_stops...`; a third identical request is refused by the dispatcher: `NoThirdIdenticalRetry`. |
| E5 | **Big taster "no":** "fix" redoes only the broken shots, "fail" goes back to the chef, and after 2 rounds it stops and asks me. | **Done** | `test_fix_redoes_only_the_named_shot_and_a_second_fail_stops_for_the_founder...`. |
| E6 | Is the riskiest shot made first, and does the job stop if it fails? | **Done** | Same risky-shot test: no other shot was paid for. Check `process:riskiest_first` on the delivered file. |
| E7 | Is every film shot built from the master plate and the shot before? Show the production log. | **Done** | `test_every_shot_is_built_from_the_master_plate_or_the_previous_shots_end_frame`; production log on `/ops/jobs/<id>`. |
| E8 | **Only I can override:** show the test where the builder, a script and the admin tool all try to override and are refused. | **Done** | `test_v2_skeleton` `OnlyTheFounderCanOverride` (worker id, "operator:claude…", script, admin CLI, operator and customer sessions, a forged proof, environment flags); station level: `test_v2_production`; web: `test_v2_founder_tools`, `test_web`. |
| E9 | When I override, is my reason saved and shown? | **Done** | `test_the_founder_can_override_with_a_reason_that_is_stored_and_shown_in_the_gateway_report`; overrides listed on the job page and in the gateway report. |
| E10 | Does a customer change go to the waiter, and then only to the affected station? | **Done** | `stations/changes.py`; `test_e2e` `test_submit_direct...` (only shot 2 + film redone), `test_copy_change_rerenders_only_text_bearing_nodes` (no paid redraw), `test_concept_change_goes_back...` (chef + new quote). |

## F. Retrieval — "does the chef read only what it needs?" (§8)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| F1 | Does the librarian build a tray, rather than sending all 25,000 words of cookbook? What is the cap for each worker? | **Done** | Caps: chef 6,000, recipe checker 4,000, pantry checker 1,500 tokens (`library/librarian.py`). The backpack job's chef tray was 3,121 tokens. Test `test_v2_kitchen` `TraysAreCapped...`. |
| F2 | Does the tray include past failures that match the planned shots? Show one example. | **Done** | FD-0923-02 (continuity drift) is on the chef's tray for the backpack job. Same test. |
| F3 | Does the tray include similar past recipes with their outcomes? | **Done** | RL-0923-FILM (the rejected reel, "Outcome REJECTED") on the same tray. |
| F4 | Is the tray logged, so I can see what the chef knew for any job? | **Done** | Artifact `tray:<worker>` plus `tray_ids` on each AI call; shown on the job page. |

## G. Learning (§7.5, §4.11)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| G1 | Does every finished job — accepted, rejected or abandoned — produce lessons? | **Done** | `test_accepted_rejected_and_abandoned_jobs_each_produce_lessons_and_nothing_is_applied_until_approved`. |
| G2 | Is nothing changed until I approve it? | **Done** | Same test; `test_lessons_wait_and_only_an_approved_one_changes_its_store`. |
| G3 | After I approve an equipment-sheet lesson, does the next job actually use it? (Show the test.) | **Done** | `test_an_approved_equipment_lesson_is_used_by_the_next_jobs_pantry_check` (risky → cannot, cited on the next job). |
| G4 | Does a second job for the same customer reuse their shelf (character, master plate, logo)? | **Done** | `test_the_second_film_for_the_same_customer_reuses_their_logo_character_and_master_plate...` (no new purchase for master or character). |

## H. Cost (§9.4)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| H1 | What is the estimated AI reasoning cost of a simulated image job, per worker? (Target ≤ USD 0.03, about ₹3.) | **Partly — reported; target missed** | About **USD 0.25**: chef 0.132, big taster 0.045, recipe checker 0.036, small taster 0.011, waiter 0.011, diary 0.008, pantry 0.008. v1 actually spent USD 1.87. See open question 1. |
| H2 | And for a simulated film job? (Target ≤ USD 0.30, about ₹25.) | **Partly — reported; target missed** | About **USD 0.38**: chef 0.155, big taster 0.061, small taster 0.056 (7 checks), recipe checker 0.049, waiter 0.027, pantry 0.023, diary 0.008. v1 actually spent USD 2.33. Test `test_v2_founder_tools` `CostReport` (it checks the report is correct and flags the miss; it does not pretend the target is met). |
| H3 | Does the quote show the reasoning cost, and does the ledger record actual cost per worker? | **Done** (live actuals not yet exercised) | The quote has `reasoning_line_usd`, shown to the customer as "Planning and checking (AI reasoning, estimated)". Every call is recorded per worker, estimated in simulation. In a live run the ledger's settled cost appears next to it (`cost.reasoning_report`). |
| H4 | Is a decision-model slot (such as Jev) available for yes/no workers, without being required? | **Partly** | The setting exists (`MI_MODEL_DECISION`) and is tested; no worker is routed to it yet, because no decision-only adapter exists. |

## I. Judges' qualification (§10)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| I1 | Is there a test set of old cases with my known verdicts, for all three judges? | **Partly** | `product/qualification/JUDGE-CASES.yaml`: recipe checker 2, small taster 9 (7 known-bad, 2 known-good), big taster 5 (MOKO7 v1/v2 unavailable on this machine). RentOK, Cuminco and Upwork media are not in the evidence repo, so they are not included yet. |
| I2 | What are the pass marks, and do I agree with them? | **Partly — needs your decision** | `product/qualification/PASS-MARKS.yaml`, the spec's proposals, status `proposed_not_confirmed_by_founder`. Nothing can qualify until you change it to `confirmed_by_founder`. |
| I3 | Until a judge passes, does its "no" still block, and does its "yes" still need me to confirm? | **Done** | `test_until_qualified_a_judges_no_blocks_and_its_yes_needs_the_founder`; recipe checker yes → "confirm recipe"; big and small taster yes → confirmation rows at the door. |
| I4 | Can the harness run live only with my separate authorisation? | **Done** | `test_a_live_run_is_refused_without_the_founders_own_session`. |

## J. Tests and reproducibility (§11, §14)

| # | Question to ask | Status | Evidence |
|---|---|---|---|
| J1 | Do all 16 required tests exist and pass? Show the output. | **Done** | Mapping below. Full run: see "Final test run" at the end of this file. |
| J2 | Do the old v1 tests still pass? If any were removed, which ones, and why? | **Done** | None removed. All 54 are kept and pass (2 are skipped only because historical media is not on this machine); 18 were updated. See "v1 tests changed" below. |
| J3 | Do full simulated image and film journeys work through the web app, end to end? | **Done** | `test_v2_journeys` (the rejected film's order → accepted film, with a change request; a two-format poster), plus `python3 -m product.smoke` → PASS media engine, PASS dry image + film jobs, PASS backup and restore. |
| J4 | What are the exact commands to reproduce everything from a fresh checkout? | **Done** | `product/README.md` "Reproduce from a fresh checkout" (Linux also needs `ffmpeg`, `fonts-noto-core`, `librsvg2-bin`). |
| J5 | What did the builder change from the spec, and why? | **Done** | "Spec changes and interpretations" below. |
| J6 | What questions are still open for me? | **Done** | "Open questions" below. |

---

## The 16 required tests (§11) → where they are

| § 11 | Test (file · test) |
|---|---|
| 1 | `test_v2_front_of_house` · `test_hands_zipping_the_bag_is_cannot...`, `OnTheVerbatimEvidence`; `test_v2_kitchen` · `test_the_rejected_films_recipe_is_sent_back...`, `test_the_recipe_checkers_model_cannot_approve_a_cannot_action...` |
| 2 | `test_v2_front_of_house` · `test_an_order_needing_the_front_pocket_open_with_no_photo_of_it...` |
| 3 | `test_v2_skeleton` · `test_worker_script_operator_customer_and_builder_strings_are_refused_and_logged`, `test_a_waiver_written_by_anyone_but_the_founder...`, `test_the_admin_cli_has_no_override_command...`; `test_v2_production` (take choice, big taster, release); `test_v2_founder_tools` (web) |
| 4 | `test_v2_skeleton` · `test_the_founder_can_override_with_a_reason_that_is_stored_and_shown_in_the_gateway_report`; `test_v2_production` |
| 5 | `test_v2_production` · `test_every_shot_is_built_from_the_master_plate_or_the_previous_shots_end_frame` |
| 6 | `test_v2_skeleton` · `NoThirdIdenticalRetry` (2 tests) |
| 7 | `test_v2_production` · `test_fix_redoes_only_the_named_shot_and_a_second_fail_stops_for_the_founder...` |
| 8 | `test_v2_storage` · `WriteOnceFiles`; `test_v2_production` · `test_a_recomposed_poster_is_a_new_file...` |
| 9 | `test_v2_learning` · `test_accepted_rejected_and_abandoned_jobs_each_produce_lessons...` |
| 10 | `test_v2_learning` · `test_an_approved_equipment_lesson_is_used_by_the_next_jobs_pantry_check` |
| 11 | `test_v2_journeys` (all 7 workers) · `test_v2_front_of_house` · `CustomersExactWordsReachEveryAiCall` |
| 12 | `test_v2_kitchen` · `test_the_chef_gets_a_capped_tray...` |
| 13 | `test_v2_storage` · `CustomerShelf`; `test_v2_learning` · `SecondJobReusesTheShelf` |
| 14 | `test_v2_skeleton` · `test_a_card_change_is_a_new_version...`; `test_v2_learning` · `test_every_call_records_its_card_version...` |
| 15 | `test_v2_founder_tools` · `CostReport` (reports per worker; the film is over the budget and is flagged — see H2) |
| 16 | the v1 suite: `test_dispatch`, `test_store`, `test_verify`, `test_e2e`, `test_web` (see below) |

## v1 tests changed (none removed)

- **Kept as they were** (36): all of `test_dispatch` and `test_store`, most of `test_verify`, and `test_e2e` `Isolation`.
- **Same purpose, v2 steps added** (14). The new steps are:
  - the pantry checker's alternative for "zipped shut" is accepted;
  - you confirm the unqualified recipe checker;
  - the customer approves the master plate;
  - you confirm or waive at the door, instead of a name string.

  Film tests use the backpack order so the recipe includes video-model shots. The node names changed (`clip_bN` → `shot_N`, `still_bN` → `frame_N`), and so did the artifact names (`intent` → `understanding`, `direction` → `recipe`). The 14 tests are:
  - `test_e2e`: FilmJourney ×3, ImageJourney, Clarification, Refusal, BudgetExhaustion, ProviderFailureInjection ×2, WorkerCrash, Learning, EveryApplicableControl;
  - `test_verify`: `test_a_waiver_does_not_discharge_the_listen...`;
  - `test_web`: `test_customer_can_submit_approve...`.
- **Purpose kept, behaviour changed by the spec** (4):
  - `test_verify` `test_missing_required_check_blocks_and_a_waiver_with_a_name_unblocks`: a name alone no longer unblocks; your waiver does.
  - `test_e2e` `WorldTruthBeforeSpend`: v1's direction reviewer is replaced by the recipe checker, and only you can override (v1: any named operator).
  - `test_e2e` `PersonPicksWhen…` → `FounderPicksWhenTheTasterRejectsEverything`: only you can pick a take (v1: any person, in practice the builder).
  - `test_web` `test_operator_pages_render_and_the_operator_can_waive_and_release`: now shows the operator refused and you doing it.
- **Two real bugs the v1 tests caught, now fixed:**
  - The automatic retry after a provider outage crashed.
  - A clip paid for just before a worker crash was not reused.

## Spec changes and interpretations (please confirm)

1. **A risky shot starts from the master plate.** §6.3 says make the riskiest shot first; §5 says every shot is built from the previous shot. Both can't hold for a risky shot in the middle of a film, so a risky shot must start from the master plate (the recipe checker enforces this). "Risky first" is a gate, not a picture dependency, so redoing a risky shot doesn't redo shots that only waited for it.
2. **"Never a third identical request"** counts requests the generator actually answered, including content refusals. It does not count outages (5xx errors, timeouts): resending after an outage isn't asking the model to try the same thing again, and counting it would kill jobs during provider outages.
3. **The small taster's "no":** each output gets 2 attempts in total (the retry adds the taster's notes as a correction). Then the chef re-plans that shot once; if that re-plan changes nothing, code falls back to a still with gentle motion. Then you decide. A master plate or poster plate has no shot to re-plan, so after 2 rejections it goes straight to you.
4. **Who approves the master plate:** §6.1 says "founder/customer", so either may. The customer's approval also puts it on their shelf as approved.
5. **Unqualified judges' "yes":**
   - Recipe checker: you confirm before the customer sees the plan (every job, until it qualifies).
   - Small taster: production continues, and you confirm at the door ("small_taster_confirmed").
   - Big taster: its "pass" rows stay unverified until you confirm.
6. **The big taster's "fix" and "fail" act automatically, as §6.2 says.** This spends money on an unqualified judge's word; v1 had switched this off after a repair ran its budget to the cap. v2 limits it to the named shots, 2 rounds and the budget cap. See open question 4.
7. **After a "fail" at the plan stage, the new recipe goes back through your confirmation and the customer's approval** (the plan changed). Unchanged shots are reused, not bought again.
8. **Any action the pantry check says "cannot" pauses the job for the customer**, with an alternative. The customer's accepted alternative is always treated as a still (decided by code, not the model).
9. **Roles:** exactly one founder (`admin init-founder`, refused if a founder exists). "Operator" staff can view and pause only; every decision is yours. The admin tool has no override command. The limit: anyone who can write to the database file directly could still forge records, which is why the database must stay on your machine or VM.
10. **Per-worker call caps** are shown on the cards; they are enforced through the send-back limits, not a separate counter.
11. **Test fixtures:** the 23-Sep order and photo descriptions are paraphrased and no customer images are copied into this public repository. The same tests also run on the verbatim records when the private evidence repo is checked out alongside.
12. **Lessons targeting a form (schema)** are recorded when you approve them, but a builder applies them; they are not changed automatically.
13. **Other small changes:**
    - `media.py`: the simulated test pictures now also work with ffmpeg 6.
    - The state name `operator_hold` is kept for your final check.
    - The old orchestrator reference copy was deleted; it is still in git history.

## Open questions for you

1. **Reasoning cost targets.** With the strongest model writing every recipe, images cost about USD 0.25 and films about USD 0.38 in reasoning. Do you want to raise the targets, use a cheaper recipe model for images (e.g. set `MI_MODEL_CHEF` per job type — not built yet), or accept this for now?
2. **Pass marks:** do you confirm the proposals in `PASS-MARKS.yaml`, or change them?
3. **Your time per job:** until the recipe checker and the tasters qualify, every job waits for you twice: once to confirm the recipe, once at the final check. Is that acceptable for the beta?
4. **Automatic big-taster repairs:** should the unqualified big taster's "fix" spend money automatically on the named shots (the spec, and what's built), or should it wait for you, as in v1?
5. **Default models:** chef GPT-5.6 Sol (Azure); judges Gemini 3.1 Pro; cheap workers Claude Haiku 4.5. Keep these?
6. **More qualification cases:** can the MOKO7 v1/v2 films and the RentOK, Cuminco and Upwork final media be added to the evidence repo, so the judges' test set is larger than 14 cases?
7. **The old v1 orchestrator reference file**, deleted in the phase 5 commit: restore it, or leave it in history?

## Final test run

On commit `5f3c404` (branch `claude/p1-v2-build`), Linux cloud container, Python 3.11, ffmpeg 6.1, simulated mode, USD 0:

```
$ PYTHONPATH=. python3 -m unittest discover -s product/tests -t .
Ran 105 tests in 1530.144s
OK (skipped=2)
```

- 105 = 51 new v2 tests + the 54 v1 tests.
- The 2 skipped are v1 tests that need historical Mokobara media that is not on this machine.
- The checks on the verbatim 23-September evidence ran, because the private evidence repo was checked out alongside.

```
$ PYTHONPATH=. python3 -m product.smoke
PASS  media engine on this host
PASS  dry image + film jobs through the product
PASS  backup and restore
```

## Amendment 1

`coordination/p1-v2/P1-V2-AMENDMENT-1.md` (spec branch commit `963d791`), applied on 2026-09-23. Same rules as before:
simulated mode only, USD 0, no cloud changes, nothing merged, tests first, the builder never the operator.
New tests: `test_v2_amendment1.py` (20 tests). Older tests that assumed you had to confirm or release were changed to the
new rules (listed at the end of this section); none was removed.

### In plain words

**What works now (simulated, USD 0):**

- **Nobody waits for you.** Every place a job used to stop for you now goes to the system first, then to the customer:
  - The customer sees the plan with "Our reviewer found no problems with this plan."
  - If the reviewer sends the plan back twice, the system swaps the problem shots for the safest alternative (a still with gentle camera motion) and checks once more. If the reviewer still objects, the customer reads the objections in plain words and chooses: go ahead, change the brief, or stop. Nothing has been spent on production at that point.
  - A risky shot that fails after its re-plan becomes a still. The preview tells the customer.
  - The big taster's "fix" is repaired automatically, only the named shots, inside the budget the customer approved, at most 2 rounds. It never spends past that budget: if the money runs out, the job pauses and asks the customer.
  - If the big taster still says no, the customer sees the film with the reviewer's report and decides: accept as is, ask for changes, or reject.
  - A **measured** failure (code checking the exact file, e.g. a wrong letter in your exact text) still never ships. It is repaired automatically; if it still fails, the customer is told what failed and chooses to stop or pay for one more attempt.
  - While the judges are unqualified, the customer's own look at the preview is the final check. Their acceptance is recorded against every check the judges could not settle.
  - Your override powers are all still there, still yours alone, and never required. The "hold every cut for me before the customer sees it" switch still exists but is now **off** by default.
- **The kitchen learns by itself.**
  - "More careful" lessons apply at once.
  - "Bolder" lessons wait until 2 accepted jobs support them.
  - A customer's taste goes on that customer's shelf only.
  - Rulebook changes apply, the next 5 jobs are watched, and the change is rolled back automatically if results get worse.
  - Anything about money, budgets, overrides or safety is never applied; it waits for you.
  - A weekly digest page (`/ops/digest`) shows what was learned, from which job, before → after, with an **Undo** button on each.
- **Images use a cheaper chef.** The recipe for an image now costs about USD 0.05 instead of 0.13. A set of 3 images meets your USD 0.08-per-image target.
- **The judges have a much bigger test set:**
  - Your 76 old verdicts: 14 films and 62 images, each file checked against its fingerprint.
  - 6 old plans for the recipe checker.
  - The report now shows agreement on accepted and not-accepted work separately. In the simulated run, an "always yes" judge scores 100% on accepted work and 0% on rejected work, so it cannot sneak through.

**What still misses or isn't done:**

- **Film reasoning cost:** about **USD 0.37** against USD 0.30 (not met).
- **Image reasoning cost:**
  - A single image is about USD 0.16 (not met).
  - A set of 2 is about 0.084 each (just over).
  - A set of 3 is about 0.059 each (met).
- **No judge is qualified.** The live qualification run has not been run, as you asked.
- **"Money, overrides, safety" lessons are recognised by their words** (budget, USD, cost, spend, cap, override, waive, safety, …). Wording that avoids those words would not be caught; the Undo button is the backstop.
- **Picking a take** (a founder override) has nothing to act on any more, because the kitchen now keeps the best take itself and flags it to the customer. Your other overrides all still work.

### §1 Cost

| # | Item | Status | Evidence |
|---|---|---|---|
| 1.1 | Film target stays ≤ USD 0.30 | **Done** (target kept and reported; the estimate does **not** meet it) | `cost.BUDGET`; `cost.reasoning_report` shows `targets` and `within_budget`. Backpack film estimate at quote time: USD 0.3695. Largest parts: chef 0.155, big taster 0.062, recipe checker 0.049, small taster 0.046. |
| 1.2 | Image target ≤ USD 0.08 (per image) | **Done** (target changed and reported; met only for sets of 3+) | Estimates at quote time: 1 image **0.159**; set of 2 **0.084 per image**; set of 3 **0.059 per image** (met). Test: `test_v2_amendment1.ImageCost.test_the_report_shows_both_targets_and_the_quote_shares_reasoning_across_the_image_set`. |
| 1.3 | Image jobs use a cheaper chef, `MI_MODEL_CHEF_IMAGE`, default a mid-tier model from the film chef's company | **Done** | `config.DEFAULT_WORKER_MODELS["chef_image"] = azure_openai:gpt-5.6-terra` (the film chef is `gpt-5.6-sol`, same company). The independence check covers both chefs, so a judge-company image chef is refused. The chef station passes `model_key="chef_image"` for images. Image chef estimate USD 0.047 (was 0.132). Test: `ImageCost.test_image_jobs_use_the_image_chef_and_films_the_strongest_both_configurable_and_independent_of_the_judges`. |
| 1.4 | One recipe → a set of images; the quote shows the reasoning cost shared across the set | **Done** | The set is one image per requested format (the product's existing "set"). The quote carries `images_in_set` and `reasoning_per_image_usd`. Extra variants of the *same* format are not offered; that would be a new feature. |
| 1.5 | The cost report shows both targets and whether they are met | **Done** | Report fields `targets` {film 0.30, image 0.08}, `target_measured` (per film / per image), `per_image_usd`, `within_budget`. Shown on the operator job page ("AI reasoning cost"). The quote carries `reasoning_targets` and `reasoning_within_target`. |

### §2 Judges tested on old jobs

| # | Item | Status | Evidence |
|---|---|---|---|
| 2.1 | Add the CASES.yaml cases (films and images) to `JUDGE-CASES.yaml` for the big taster, read from the evidence repo | **Done** | 76 cases `BT-H-*` (14 films, 62 images) generated from `historical/CASES.yaml` @ `1212814`. Each is read from `<evidence repo>/historical/…` and used **only if its SHA-256 matches** (`judges.Evidence.historical`). All 76 were available and matched on this machine. The earlier agency-folder MOKO7 cases were replaced by the same two films, now hash-verified. Total big-taster set: 79. |
| 2.2 | Verdict mapping accept → pass; specific_repair → fix; rebuild_direction / reject → fail | **Done** | Each case stores `founder_verdict` and `known_judge_verdict`. Test: `JudgesOnOldJobs.test_the_big_taster_set_holds_the_14_films_and_62_images_with_the_verdict_mapping_and_pass_marks_are_confirmed`. |
| 2.3 | A recipe-checker case for each old job whose plan is on its job branch, with the job's final verdict; list the jobs whose plan is missing | **Done** | 6 cases `RC-H-*`, read with `git show origin/work/<branch>:<path>`: MOKOBARA-ODYSSEY-007 (accept), RENTOK-GAME-A-004 (accept), RENTOK-GAME-B-005 (accept), RENTOK-GAME-V2-006 (accept), UPWORK-INTRO-001 (accept, final V4.1), CUMINCO-CHOPSTICKS-003 (reject; its only plan on the branch is its prompt file). **Missing:** UPWORK-PORTFOLIO-002 (the portfolio tiles, including the rejected Nivaas tile): no plan was kept on any branch (`recipe_checker_missing` in `JUDGE-CASES.yaml`). |
| 2.4 | Report agreement separately for accepted and not-accepted cases | **Done** | `agreement_accepted`, `agreement_not_accepted`, `agreement_balanced`, plus films vs images for the big taster. The pass marks apply to **each group separately** (my reading; please confirm). Simulated run (USD 0), big taster: 79 available, accepted 64 → 1.0, not accepted 15 → 0.0. Recipe checker: 8 available, 6 → 1.0, 2 → 0.0. Test: `JudgesOnOldJobs.test_the_harness_scores_accepted_and_not_accepted_separately_verifies_hashes_and_still_never_qualifies_simulated`; a wrong fingerprint makes a case unavailable, never judged (`test_a_file_whose_hash_does_not_match_is_unavailable_never_judged`). |
| 2.5 | Mark `PASS-MARKS.yaml` `confirmed_by_founder: 2026-09-23` | **Done** | `status: confirmed_by_founder`, `confirmed_by_founder: 2026-09-23`. |
| 2.6 | The live qualification run stays not run | **Done** (not run) | No live flag was used; `spent_usd` 0.000000 in every harness run. Every judge still reports `qualified: false` (simulated). |

### §3 Nobody waits for the founder

| # | Where the job used to wait | Now | Status | Evidence |
|---|---|---|---|---|
| 3.1 | Plan confirmation after the recipe checker | **Customer.** An unqualified checker's approve shows as "Our reviewer found no problems with this plan." Its send_back still sends back. | **Done** | `chef.after_approved_recipe` (the `plan_note` artifact, shown on the plan card). Tests: `NobodyWaitsForTheFounder.test_an_unqualified_recipe_checkers_approve_goes_straight_to_the_customer_as_our_reviewer_found_no_problems`; `test_v2_kitchen.RecipeRoundsAndTheCustomer`. |
| 3.2 | Recipe checker sends back twice | **System, then customer.** The system swaps the problem shots for the pantry checker's safest alternative (FILM-A still) and re-checks once (`SB-RECIPE-SAFE`). If it is still sent back, the customer sees the objections in plain words and chooses go ahead / change the brief / stop (USD 0 spent). | **Done** | `chef.safe_replan`, `chef.objections_to_customer`; approving needs `accept_objections` (a tick-box on the plan card). Test: `…test_after_two_send_backs_the_system_replans_with_safe_alternatives_and_the_customer_decides_if_it_still_fails`. Also `test_v2_kitchen` (the v1 recipe → the safe re-plan) and `test_e2e.WorldTruthBeforeSpend` (objections → customer, nothing paid). |
| 3.3 | Riskiest shot fails after its re-plan | **System.** The shot switches to FILM-A; the preview notes it; the job continues. If even the still is rejected, the best take is kept, flagged and noted. | **Done** | `chef.force_still`, `head_cook._keep_flagged`. Tests: `…test_a_risky_shot_that_fails_after_its_replan_becomes_a_still_with_code_motion_and_the_preview_says_so`; `test_v2_production.RiskiestShotFirstAndOnlyTheFounderPicksATake`; `test_e2e.TheTasterRejectsEverything`. |
| 3.4 | Master plate approval | **Customer**, unchanged | **Done** | `head_cook.approve_master`; `test_v2_founder_tools` (customer approves the master in the web app), `test_v2_journeys`. |
| 3.5 | Big taster says fix | **System.** Automatic repair of the named shots, within the approved budget, at most 2 rounds | **Done** | `tasters._send_back` (`SB-BIG-FIX`). The budget is enforced by the ledger: out of money → `paused_budget` (the customer's decision), never spend beyond it. Test: `…test_big_taster_fix_repairs_automatically_within_the_approved_budget_and_never_spends_beyond_it` (2 rounds, only shot 2 and what is built from it; a second job whose budget covers only the first cut stops at the cap). |
| 3.6 | Big taster says fail, or repairs used up | **Customer**: sees the film with the plain report; accept as is / changes (priced) / reject | **Done** | `tasters._to_customer` (the `review_report` artifact + a note on the preview). On acceptance, the customer's "accept as is" is recorded against the failed judgement rows. Tests: `…test_a_big_taster_fail_after_its_round_goes_to_the_customer_who_may_accept_as_is`; `test_v2_production.BigTasterSendBacks`. |
| 3.7 | Unqualified big taster says pass | **Customer**: the preview is the final check | **Done** | `tasters.present`, `tasters.accept` (writes `customer:<email>` rows). `verify.gateway` now splits **measured** checks (block) from **judgement** checks (the customer settles them). Tests: `test_v2_founder_tools.JudgesQualification.test_until_qualified_a_judges_no_blocks_and_its_yes_goes_to_the_customers_preview`; `test_v2_journeys`. |
| 3.8 | Door guard block from a measured FAIL | **System**: still blocks, routed to repair; if it cannot be fixed within budget, the customer is told what failed and chooses stop or paid rework | **Done** | `tasters.measured_repair`, `customer_decision`, `decide`; a new customer state `needs_customer_decision`. Test: `…test_a_measured_fail_never_ships_it_goes_to_repair_then_the_customer_chooses_to_stop_or_pay_for_a_rework` (2 automatic repairs → decision → paid rework → still failing → decision → stop). |
| 3.9 | Founder overrides stay available, founder-only, never required | **Partly** | Still founder-only, refused and logged for everyone else: override the recipe checker, override the big taster, waive, confirm, resume, release, close, decide/undo lessons, and the hold before preview (now off by default: `MI_HOLD_BEFORE_PREVIEW=0`). **Picking a take** can no longer happen, because no output ever waits for a pick. |
| 3.10 | Test: no job ever enters a founder-only wait unless a founder chose to intervene | **Done** | `…test_no_simulated_journey_ever_enters_a_founder_only_wait` (an image and a film, end to end). Every §3 test also asserts no `paused_for_founder` / `operator_hold` state. The web journeys assert it too. The send-back table no longer names the founder anywhere (`test_v2_skeleton`). A crash (`failed`) is still a founder state, but the customer can now close a failed job themselves. |
| 3.11 | Test: automatic repair never exceeds the approved budget | **Done** | See 3.5. |

Two bugs were found and fixed on the way. Both had been hidden before because, in dry runs, you waived every open check at the door:

- A second plan approval moved the "budget authorised at" time. Pictures paid under the first approval then looked unauthorised. Now the first approval counts.
- Automatic repairs and customer changes looked like rule breaks to the "take selection" and "riskiest shot first" checks. Redraws after a repair or change are now marked as repairs.

### §4 Learning is automated

| # | Lesson kind | Rule | Status | Evidence |
|---|---|---|---|---|
| 4.1 | More careful (equipment → risky/cannot, a failure-diary entry, a stricter check) | Applied automatically, immediately | **Done** | `lessons.LessonQueue.classify/_process`. Tests: `LearningIsAutomated.test_a_more_careful_lesson_applies_immediately_and_the_founder_can_undo_it_exactly`; `test_v2_learning` (the next job's pantry check uses it; undo brings the old verdict back). |
| 4.2 | Bolder (equipment → reliable, a check relaxed) | Applied automatically once ≥ 2 accepted jobs support it | **Done** | Support is counted by accepted jobs proposing the same change. A change to a judge's rulebook card is treated as possibly relaxing a check (code cannot tell looser wording from stricter), so it waits too. Tests: `test_a_bolder_lesson_waits_for_two_accepted_jobs`, `test_a_change_to_a_judges_card_may_relax_a_check_so_it_waits_for_two_accepted_jobs_then_is_watched`. |
| 4.3 | One customer's taste or brand fact | On that customer's shelf only; never global | **Done** | Test: `test_one_customers_taste_goes_on_that_customers_shelf_only`. |
| 4.4 | Rulebook card / KRA wording | A new card version; the next 5 jobs watched against the previous 5; automatic rollback if acceptance drops or blocking checks rise; the rollback recorded | **Done** | `LessonQueue.review_watches` (run after every closed job); `Rulebook.restore` writes the rollback as a new version with the old content and the reason. Test: `test_a_rulebook_change_applies_is_watched_for_five_jobs_and_rolls_back_on_a_drop` (a simulated drop). |
| 4.5 | Money limits, budgets, spend caps, who may override, safety rules | Never automatic; founder only | **Done** (by wording, see the limit above) | Card/equipment lessons whose wording mentions money, spend, caps, overrides, waivers, permissions, safety or the founder, plus any form (schema) change, are `founder_only`. Tests: `test_a_money_or_override_lesson_is_never_applied_automatically`; `test_v2_storage.LessonQueueApplies`; `test_v2_founder_tools` (you decide one in the web app; an operator cannot). |
| 4.6 | Every applied lesson logged with the job, the evidence and before/after | | **Done** | The lesson row (`applied_json` before/after, `evidence_json`, `decision_note`) and a `lesson_applied` event on the job. `test_v2_learning` checks this on real closed jobs. |
| 4.7 | A weekly digest page for the founder, with undo per item; undo restores the previous version and records who undid it | | **Done** | `/ops/digest` (linked from `/ops`). Sections: waiting for you / applied / waiting for support / rolled back / undone. Undo is founder-only (operators get 403). Undo writes the previous content back as a new version (card, equipment row), removes an added library/diary entry, or withdraws a shelf item. It records `undone_by`, the reason and a `lesson_undone` event. Tests: `test_the_weekly_digest_lists_what_was_learned_from_which_job_with_an_undo_button`; `test_v2_founder_tools` (undo in the web app). |

### §5 Models

| # | Item | Status | Evidence |
|---|---|---|---|
| 5.1 | Leave the model configuration as is | **Done** | Unchanged except the new image-chef slot required by §1. |
| 5.2 | Add the open-items line | **Done** | Below. |

### §6 Housekeeping

| # | Item | Status | Evidence |
|---|---|---|---|
| 6.1 | `deploy/RUNBOOK-P1.md`: the founder account is created and held only by the founder; builders and scripts never create it or store its password | **Done** | The runbook now tells **the founder** to run `init-founder` and says no builder, operator, AI agent or script may run it, receive the link or hold the password. The old `init-operator` step and the operator-waiver instructions were replaced to match amendment 1. Test: `RunbookFounderAccount`. |
| 6.2 | The independent re-run (105 tests OK, 1 skipped, commit 4359d5a) is noted | **Done** | Noted here, with thanks. |

### Open items

- live runs will fail at the first cheap-worker call until a valid Anthropic key is supplied or those workers are pointed at another provider (`MI_MODEL_<WORKER>`)
- Your earlier questions 1–4 and 6 are answered by the amendment. Question 5 (default models) is settled by §5. Question 7 (the deleted v1 reference file) is still open.
- Please confirm that the pass marks apply to accepted and not-accepted cases separately (2.4).

### Older tests changed for amendment 1 (none removed)

Every test that expected you to confirm a recipe, pick a take or release a cut now expects the new owner (the system or
the customer). Where a test is about your own intervention (the hold before preview, waivers, the listen that cannot
be waived) it switches the hold on first (`test_web.test_operator_pages_render_and_the_operator_can_waive_and_release`).
Files: `test_v2_kitchen`, `test_v2_production`, `test_v2_learning`, `test_v2_founder_tools`, `test_v2_journeys`,
`test_v2_storage`, `test_v2_skeleton`, `test_e2e`, `test_web`, and the helpers `support.py` and `fixtures_v2.py`.

### Final test run (amendment 1)

On commit `faacdfd` plus this checklist (branch `claude/p1-v2-build`), Linux cloud container, Python 3.11, ffmpeg 6.1,
simulated mode, USD 0, with the private evidence repo at `1212814` and the old job branches fetched:

```
$ PYTHONPATH=. python3 -m unittest discover -s product/tests -t .
Ran 125 tests in 2038.003s
OK (skipped=2)

$ PYTHONPATH=. python3 -m product.smoke
PASS  media engine on this host
PASS  dry image + film jobs through the product      (both accepted, USD 0.134 / 0.194 simulated)
PASS  backup and restore

$ PYTHONPATH=. python3 -m product.qualification.judges
big taster 79 available (64 accepted / 15 not), recipe checker 8 available (6 / 2); spent USD 0.000000; nothing qualified
```

- 125 = the earlier 105 + 20 new amendment tests. The 2 skipped are the same v1 tests as before; they need
  historical Mokobara media in a folder layout this machine doesn't have.
