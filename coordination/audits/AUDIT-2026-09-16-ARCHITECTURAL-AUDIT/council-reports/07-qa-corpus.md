# Agent 7 — Question–Answer Corpus (CANON-014 Q&A banks)

Persona 56 (Q&A corpus specialist) with 53/54 (fine-tuning/distillation, SLM) consulted for §6(d).
READ-ONLY audit. MI main verified at `3bb9a3c3da484e43d4d54ae20543d1d246769ac6`.
All counts below were computed by commands shown in §A (appendix); prose figures from README/manifest are quoted only to compare against the computed ones.

---

## 0. Where the Q&A material lives (OBSERVED)

| Location | Ref | What | Items |
|---|---|---|---|
| `canon/qa/canon-014/` | main @ 3bb9a3c | 23 `*-qa-bank.yaml` + `QA-MANIFEST.json` + `README.md` + `validate_qa_corpus.py` (26 files) | **1,028** |
| `canon/experimental/book-expansion-qa-v1/<source>/qa-bank.yaml` | branch `work/canon-parallel-books-qa-experimental` @ 3c29c8d (NOT merged; 19 commits ahead of merge-base bf02dd1; 128 files, +134,743 lines) | 17 per-source dirs, each with qa-bank + SK/SCS/bindings/ontology + `grounding_audit.py` | **899** |
| `canon/experimental/canon-014-qa/*-qa-bank.yaml` | branch `claude/canon-014-expansion-admission-ntp0dl` @ 22656b9 (NOT merged) | 6 Indian-context banks, manifest `canon-014-v2` | **129** |
| Referenced by | `canon/knowledge/CANON-CORPUS-INDEX.yaml @ 3bb9a3c` lines 39–57 and 854–895 (fingerprint `qa_corpus`, 23 files, digest `1313c0ba…`) | | |
| Referenced by | `canon/candidates/canon-014/{airey,ries,samara,freeman}/audit-assessment-HOLD.yaml` field `qa_bank:` | 4 of the 5 remaining HOLD candidates point at their bank | |

Lineage (OBSERVED from `git log`): 899 items came from the experimental branch (author "Canon Experimental Worker", 2026-08-30 08:18–13:05 IST, 17 lanes), 129 from the ntp0dl branch (author "Claude (CANON-014)" / "Vaibhav Chawla", 2026-08-30). Both were consolidated on `work/canon-014-final-full-canon` (e281059 "integrate full grounded QA corpus", ffc6edc) and landed on main in a single commit `c6f8d91` (2026-08-30 18:43 IST, author chawlavaibhav, "CANON-014: integrate full Canon corpus"). `git log -- canon/qa` on main shows exactly one commit: the corpus has never been edited since landing. 899 + 129 = 1,028 ✔. The manifest's own vocabulary note confirms "two contributing lanes used two vocabularies" (`QA-MANIFEST.json` `answer_type_vocabulary_note`).

Generator (INFERENCE from commit authorship and bank headers): the questions and answers were written by Claude sessions running an extraction lane per source against a local text copy of each book; no human authored or reviewed any item (README: "No expert has reviewed them"). The experimental branch carries an *independent* `grounding_audit.py` that checks support quotations against the source text — that tool did not travel to main.

---

## 1. Exact counts (computed)

Command: `python3 canon/qa/canon-014/validate_qa_corpus.py` and the per-bank script in §A.1.

| Bank (main @ 3bb9a3c) | items | requires_application | bank `source_status` |
|---|---|---|---|
| hopkins-my-life-in-advertising | 80 | 38 | hold |
| sullivan-hey-whipple | 78 | 34 | hold |
| ogilvy-beyond-ch2 | 76 | 35 | hold |
| light-science-magic-beyond-ch3 | 62 | 31 | hold |
| berger-contagious | 60 | 20 | hold |
| freeman-photographers-eye-beyond-parts1-3 | 58 | 27 | hold |
| airey-logo-design-love | 57 | 30 | hold |
| hopkins-scientific-advertising-ch8-21 | 57 | 23 | hold |
| kahneman-sibony-sunstein-noise | 57 | 16 | hold |
| connor-irizarry-discussing-design | 51 | 17 | hold |
| ries-22-immutable-laws-branding | 50 | 25 | hold |
| samara-breaking-the-grid-ch2 | 46 | 23 | hold |
| w3c-wcag22-text-legibility | 41 | 17 | hold |
| godin-this-is-marketing | 37 | 12 | hold |
| carroll-read-this-photographs | 35 | 14 | hold |
| sontag-on-photography | 28 | 10 | hold |
| google-abcd-video-ads | 26 | 13 | hold |
| parameswaran-nawabs-nudes-noodles | 26 | 12 | accepted |
| dwyer-patel-cinema-india | 23 | 4 | accepted |
| bijapurkar-we-are-like-that-only | 21 | 3 | accepted |
| desai-mother-pious-lady | 21 | 5 | hold |
| jain-gods-in-the-bazaar | 21 | 3 | accepted |
| pandey-pandeymonium | 17 | 6 | accepted |
| **Total** | **1,028** | **418 (40.7%)** | 108 accepted / 920 hold *as labelled* |

Experimental branch (computed over the archived tree): 17 banks, **899** items (identical per-bank counts to the 17 corresponding main banks). ntp0dl branch: 6 banks, **129**. Main = union; there is no Q&A on any branch that is not on main, and no main bank differs from its branch original except the added `source_status`/`corpus`/`calibration` header keys and the vocabulary merge (89 items carry `answer_type_as_written`).

Provenance fields (computed, §A.1): every one of 1,028 items has `qa_id, source_id, source_locator, question, answer, answer_type, difficulty, knowledge_type, requires_application, support, confounders, source_status`; 899 also carry `source_title` and `requires_application_canon013`; 1 carries `amended_by`.
- `support` is non-empty on **1,028/1,028**; it is usually a locator restatement plus an evidential note, and often (not always) a verbatim quotation.
- Page-level locators (`p.`/`pp.`/`page` in `source_locator`): **400/1,028 (38.9%)**. The rest are chapter/section/"spine N" locators (README: "page numbers only where the copy had authored pages").
- Size: q mean 31 words, answer mean 150 words (median 149; floor 35 enforced by validator); total q+a+support ≈ 222k words ≈ **300k tokens**.

**Validator state on main — CONFLICT (OBSERVED).** `QA-MANIFEST.json` says `checks_run.errors: 0` and the README says "108 items, 5 banks accepted / 920 items, 18 banks hold". Running the committed validator today prints **`23 banks, 1028 items, 26 errors`**: 13 banks "claim source_status 'hold' but its artifacts live in the accepted tree" and the same 13 have a `knowledge_dir` under `canon/candidates/canon-014/` that no longer has a `source-knowledge.yaml`. Cause: the DN-06 admission batch (commits 711163e, 3aac324, 095bca0, 18807b8 … 2026-09-01, all on main; ruling in `coordination/decisions/CONTROLLER-REP-07-ADMISSION-BATCH-2026-09-01.md`) moved 13 sources to `canon/knowledge/current/` and updated the corpus index totals (`CANON-CORPUS-INDEX.yaml` lines 49/57: accepted qa_items 796, hold 232) but **never touched the banks or the manifest**. The index is itself internally inconsistent: 13 source entries carry `epistemic_status: accepted` while their nested qa block still says `source_status: hold` (computed, §A.4). So three artefacts disagree on the same fact: banks+manifest (108/920), index totals (796/232), index per-source (contradictory). Actual state by where the source now lives: **796 items over 18 accepted sources; 232 items over 5 HOLD sources** (airey 57, ries 50, samara 46, freeman-beyond 58, desai 21).

---

## 2. Subject coverage

Domain mapping (by bank; `knowledge_type` counts from manifest reproduced by computation):

| Domain | Banks | Items |
|---|---|---|
| Advertising / commercial communication | hopkins ×2, ogilvy, sullivan, google-abcd, pandey, parameswaran | 360 |
| Branding / marketing strategy | ries, godin, berger | 147 |
| Design / typography / legibility | airey, samara, connor-irizarry, w3c-wcag | 195 |
| Photography / light | light-science-magic, freeman, carroll, sontag | 183 |
| Film / Indian visual culture | dwyer-patel, jain | 44 |
| Indian market / consumer | bijapurkar, desai | 42 |
| Behavioural / judgement | kahneman-noise | 57 |

`knowledge_type` top values: evaluation_diagnosis 127, advertising 123, brand_communication 99, creative_process 72, composition 67, persuasion 64 … short_form **6**, shot_design 12, lighting 14, production 9. There is **no** bank on editing/pacing, motion, voice performance, sound, or Devanagari/Indic typography (the last is a known gap in the Controller decision).

Cumin-relevant keyword search (regex over question+answer, §A.2 — counts are hits, many incidental): product role/hero 7; ad-vs-tutorial/demonstration 49 (almost all "demonstrate" in the reasoning sense); opening/hook/first-seconds 11; CTA/end card 10 (7 of them in google-abcd); brand mention/early 23; proposition/proof 28; voice/VO/narration 46 (mostly "brand voice"/"in his own voice"); text-over/safe area/legibility 55 (mostly WCAG contrast). **No item mentions "safe area", "safe zone", "tutorial", or "hero shot".** The only items that directly answer the Cumin-shaped questions (opening, brand-early, CTA placement, supers, packshot lighting) are concentrated in two banks: `google-abcd-video-ads` (26 items) and `ogilvy-beyond-ch2` ch.8 TV tips, plus `light-science-magic-beyond-ch3` for packshots. Both of the first two are now accepted sources (DN-06), although their banks still say hold.

### The 10 most Cumin-relevant pairs (verbatim, trimmed; `file:line` is the `- qa_id:` line on main @ 3bb9a3c)

1. **`google-abcd-video-ads-qa-bank.yaml:277` qa_abcd_0010** (application) — Q: "A 20-second ad for a new energy drink opens on a silent slow-motion product beauty shot, brings the logo up only at the very end, shows no people at all, and closes on a 'Buy now' end card. The brief is an awareness campaign. Judged strictly by this source, what is wrong with it — and what is not?" A: "Three of the four awareness instructions are missed. Attention for awareness is to be won with audio … and the opening is silent. Branding is to be 'front and center' and the brand arrives last … Connection is to 'Make the people core to the story', and there are no people … What is not wrong on this source's terms is the end card …"
2. **`google-abcd-video-ads-qa-bank.yaml:311` qa_abcd_0011** — Q: "A performance team wants to put the call to action in the first two seconds of an action-objective ad, to catch viewers who skip. What does this source's own guidance say about that placement?" A: "It says the opposite, and it is the source's only placement instruction anywhere. The action row's Direction cell reads 'Present the ask after the context is set' … the core Direction guidance says nothing about placement at all …"
3. **`google-abcd-video-ads-qa-bank.yaml:535` qa_abcd_0019** — Q: "An ad carries no brand presence at all until a five-second logo lockup at the end. Which parts of the source's Branding guidance does that miss?" A: "All three of them. 'Show up early and throughout' … 'Reinforce with audio' — no spoken brand mention … 'Draw on all your branding assets' — one asset type where the source names six (product shots, pack shots, in-situ branding, graphic elements, voice-overs, musical treatments) … the source quantifies none of the three."
4. **`google-abcd-video-ads-qa-bank.yaml:141` qa_abcd_0005** — Q: "You are adapting an ad built to this guidance for a feed placement that autoplays muted. Which of the source's guidelines lose their premise…?" A: "Every audio-dependent guideline loses its premise … As to what to do instead, the source says nothing at all."
5. **`google-abcd-video-ads-qa-bank.yaml:448` qa_abcd_0016** — Q: "The source's Attention principle asks for two distinct things. What are they…?" A: "Hooking attention and sustaining it … What it never gives is a duration — no page names a number of seconds for 'the start'."
6. **`ogilvy-beyond-ch2-qa-bank.yaml:2603` qa_ogx_0073** — Q: "A thirty-second script opens on eight seconds of wordless atmosphere, names the brand at twenty-two seconds, and carries a super whose wording paraphrases the voice-over. Give Ogilvy's three objections and say which two of his rules are competing for the same seconds." A: "…open with the fire … use the name within the first ten seconds … the super must carry exactly the same words as the soundtrack … The two rules competing for the same seconds are the visual surprise and the brand name …"
7. **`ogilvy-beyond-ch2-qa-bank.yaml:952` qa_ogx_0027** — Q: "A director defends a slow, atmospheric opening on the ground that it sets up a strong payoff twenty seconds in. Give Ogilvy's answer…" A: "…the maker knows great things are about to happen and the viewer does not — and the viewer will never find out, because she has left the room … stated for the thirty-second commercial in the broadcast environment of 1983."
8. **`ogilvy-beyond-ch2-qa-bank.yaml:915` qa_ogx_0026** — Q: "Ogilvy treats getting the brand remembered as work that has to be done deliberately … What is the failure he says is the default, and what does he prescribe?" A: "…a shocking percentage of viewers remember the commercial and forget the name of the product … use the name within the first ten seconds … commercials ending by showing the package change brand preference more effectively …" Support: "The shocking percentage is never given … measurement asserted, result withheld."
9. **`light-science-magic-beyond-ch3-qa-bank.yaml:1384` qa_lsmx_0039** — Q: "A packshot of a white ceramic diffuser on white shows clean separation and good detail, and the art director says it reads as 'product on grey' … What does this book say has happened, and what is the fix?" A: "The lighting has put the extreme on the wrong element … relight so the BACKGROUND carries the extreme and the subject sits just inside it — … between half a stop and one stop darker at its edges."
10. **`hopkins-scientific-advertising-ch8-21-qa-bank.yaml:1663` qa_sa8_0048** — Q: "You are advertising a wrinkle treatment. On Hopkins's rule, what goes in the picture, what goes in the call to action, and what exception does he allow?" A: "The picture shows the face as it will appear, not the wrinkles … The call to action assumes compliance: 'Send now for this sample', not 'Why do you neglect this offer?' …"

Runner-up for text legibility: `w3c-wcag22-text-legibility-qa-bank.yaml:863` qa_wcag_0025 (which of four on-page texts carry a contrast requirement — wordmark exempt, image-of-text in scope) and `:192` qa_wcag_0006 (relative-luminance weights; two colours differing only in blue barely differ in contrast).

INFERENCE: the ABCD and Ogilvy items are the only ones in the corpus that read like the questions a producer asks about a 15–20 s product film (brand-early, hook, CTA placement, super = VO). They are ~15 items out of 1,028 (≈1.5%).

---

## 3. Quality sampling (20 items, seed 20260916)

Sampling command (§A.3): load all 1,028 items in sorted bank order, `random.seed(20260916); random.sample(items, 20)`. Full dump at `agents/07-sample20.txt`. Grades are my judgement (INFERENCE), scale: G = grounded (locator + support present / page-level), S = specificity (would it change a production decision: H/M/L), R = correctness risk (L/M/H), P = "a question a professional remembers to ask" (Y / partial / N), Kind = RC (reading comprehension about the source) / SC (scenario-costumed comprehension: a case is posed but the ask is "what does the book say") / IC (intent-completion: a check a practitioner would run).

| # | qa_id | G | S | R | P | Kind |
|---|---|---|---|---|---|---|
| 1 | qa_ctg_0031 (Berger laptop logo) | ch+section; support notes "NO outcome measurement" | L | L | N | RC |
| 2 | qa_nnn_0025 (J&N no-product poster) | plate ref `images/00008.jpg`; support "inspected at 566 px" | M | M (answer is a description of one plate) | partial | SC |
| 3 | qa_pex_0058 (Freeman duration in a still) | converted-PDF page | L | L | N | RC |
| 4 | qa_disc_0050 (feedback sandwich) | printed pp.153–154 | L | L | N | RC |
| 5 | qa_ppm_0015 (five-second criterion) | "Ch. 7; operational-bindings" | M | M — answer is about *this project's record* (binding `bnd_ppm_0003`), not the book | partial | RC (self-referential) |
| 6 | qa_sa8_0026 (impregnable fields) | printed p.38 + quote | L | L | N | RC |
| 7 | qa_snt_0016 (Sontag two decays) | essay + passage | L | L | N | SC |
| 8 | qa_wcag_0039 (disabled button contrast) | normative SC refs | H (UI) / M (ads) | L | Y | IC |
| 9 | qa_sa8_0029 (charge a dime for the sample) | printed p.41 + quote | M | M (1920s figures) | partial | SC |
| 10 | qa_sa8_0041 (test-campaign "two problems he does not raise") | printed p.49 + quote | L | M — half the answer is extractor opinion presented as content | N | RC+critique |
| 11 | qa_god_0029 (shareable asset) | ch+sections | M | L | partial | SC |
| 12 | qa_snt_0012 (photography beautifies) | essay + Benjamin quote | L | L | N | RC |
| 13 | qa_nse_0004 (matter of judgment) | ch.4 | L | L | N | RC |
| 14 | qa_whip_0020 ("patterns are campaigns") | ch+section | M | L | partial | RC |
| 15 | qa_sgb_0009 (Samara readability) | ch+section | L | L | N | RC |
| 16 | qa_sgb_0019 (narrative constructs) | ch+section | L | L | N | RC |
| 17 | qa_r22_0045 (gin brand launching vodka) | printed pp.97–98 | M | **H** — Ries is a HOLD source the Controller ruled to retire in favour of Binet (DN-05: "Rule for Binet — retire ries"), yet the answer is stated as advice | partial | SC |
| 18 | qa_dpci_0017 (Mohabbatein publicity timeline) | printed pp.179–180 | L (for ads) | L | N | RC |
| 19 | qa_wcag_0006 (relative luminance weights) | glossary, normative | H | L | Y | IC |
| 20 | qa_ctg_0038 (Livestrong wristband) | ch+section | L | L | partial | SC |

Distribution: grounded 20/20 (page-level 7/20; corpus-wide 400/1,028). Specificity H 2, M 6, L 12. Correctness risk L 14, M 5, H 1. Professional-question Y 2, partial 8, N 10. Kind: RC 12, SC 6, IC 2.

Observations (INFERENCE): answers are long (150 words), hedged, and unusually careful about what the source does *not* say — that is the corpus's best property. Their weakness for production use is that the question is almost always *about the author* ("What does Hopkins say…"): a computed **86.4% (888/1,028)** of questions name the author, "the source", "this book" or "the authors"; **32.5% (334)** open with a scenario ("A team…", "You are…"). The `confounders` field (present on all 1,028) is the most benchmark-shaped element: it names the plausible wrong answer.

---

## 4. Authority status (OBSERVED)

- **Never admitted into production authority, by design.** README: "Where it sits relative to the Audit Gate — Outside it, deliberately … No Audit Gate record covers any file in this directory." `grep -rl qa-bank canon/audit/records` → only `hopkins-my-life-in-advertising.audit.yaml:312` mentions "Q&A confounders" in passing. `AUDIT-GATE-v0.2.md` does not mention Q&A at all.
- Controller decision `coordination/decisions/CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md` (ACCEPTED FOR MERGE, PR #69): "1,028 grounded, ungraded, uncalibrated Q&A items retained under canon/qa/canon-014/ … This merge does not enable HOLD/candidate retrieval in ordinary runtime … A future experiment may deliberately expose the full status-aware corpus and Q&A, but must record the exact fingerprints used." Governor L1 review (`governance/reviews/GOV-L1-CANON-014-FULL-CORPUS.md`) PASS with non-blocking note G14-N1: the manifest's own digest algorithm differs from the index's.
- `canon/knowledge/CANON-CORPUS-INDEX.yaml` references all 23 banks under `fingerprints.qa_corpus` (digest `1313c0ba…`, matching EVAL-037's `EXECUTION-CONTRACT.md:47`). The manifest's `corpus_fingerprint.combined_digest` (`25ac8bbc…`) is a *different* algorithm — two fingerprints for the same 23 files.
- Status labels per the gate today: 18 of the 23 sources are accepted (Audit Gate records promoted by DN-06), 5 remain HOLD (`ries` explicitly retired by DN-05 but still resident in candidates). The banks' own labels are stale (§1). Per the corpus's own rule ("a held source must never be presented as accepted") the current mislabel is in the *safe* direction, but the reverse hazard exists for `ries`: its bank presents a retired source's positions as ordinary "hold".
- Explicit contracts forbidding Q&A in the production surface: `canon/context/CANON-CONTEXT-SPEC-v0.1.md` R4 ("Q&A banks (canon/qa/) must not appear"); `canon/context/canon-context-schema-v0.1.yaml:84` forbidden list; `runtime/contracts/PRODUCTION-SPEC-v1.yaml:69` ("No HOLD material, no Q&A corpus, no free-form retrieval"); `canon/packs/COMPILED-PACK-CONTRACT-v0.1.md:54,172,192` ("HOLD/QA ids fail validation").

Answer: **experimental companion asset; not authoritative; never admitted; explicitly excluded from the production surface by four contracts.**

---

## 5. Consumption today (OBSERVED, with proof)

- **Runtime (`runtime/canon/packs.py`)**: the docstring states "no HOLD material; no Q&A corpus" and the only files it reads are `canon/packs/pack-triggers-v0.yaml` and `canon/compilation/PACK-*-v0.yaml` (line 158 `self.compilation_dir.glob("PACK-*-v0.yaml")`). The injectable check is `corpus_digest == fingerprints.accepted_canon.combined_digest`, which does not include the `qa_corpus` fingerprint. **It cannot query the Q&A banks** — there is no code path from a Normalized Request to `canon/qa/`. Regression test: `runtime/tests/test_canon_lookup.py:66-69` `test_no_hold_material_can_reach_the_payload` asserts `"canon/qa/"` is absent from the payload.
- **Pack compiler (`canon/compilation/compile_pilot_packs.py`)** reads `source-knowledge.yaml` (line 550) — no reference to Q&A. Only two pilot packs exist (`composition_and_attention`, `product_appearance`).
- **media-agency skill (`.claude/skills/media-agency/`)**: zero references to `canon/qa` or qa-bank (grep). The Cumin job record (`work/agency-job-cuminco-chopsticks-001 : agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/JOB.yaml:111-116`) records `canon.prefix_sha256` from `runtime.canon.lookup` ("5298 tokens, 21 check ids") — pack path only; no Q&A.
- **Tests**: only the negative assertion above.
- **Code that DOES read the banks**: `eval/experiments/EVAL-037/tools/canon_tools.py:122,161,232,269,393,470` (BM25 search + `canon_read` over accepted + HOLD + Q&A, exposed only in FULL_CANON) and `tools/runner.py:117` (fingerprints the 23 banks). Lanes `sol/haiku/sonnet/gemma-full-canon.yaml` list `corpus.roots.qa: canon/qa/canon-014`. This is the **only** consumer and it is a frozen, completed experiment (2026-08-30), not runtime.
- Unmerged: CANON-015 (`8115400`, branch `claude/canon-retrieval-maturity-lwwaey`) built an accepted-only retriever precisely to exclude Q&A/HOLD; its brief (`8115400:canon/findings/CANON-015-CONTROLLER-BRIEF.md:77-78`) reports that of 424 objects EVAL-037's unbounded lane exposed, **HOLD Q&A = 94 (22.2%) and accepted Q&A = 18 (4.2%)** — "Q&A items are short and question-shaped and the lexical ranker rewards that." Its "Production questions answered" eval set is a set of *questions* built by `build_eval_set.py`, not from the Q&A banks (line 146).

Eight-state ladder, what can be proven: knowledge exists (yes, 1,028 items) → was retrieved (yes, EVAL-037 FULL_CANON lanes: computed hits for `qa-bank.yaml`/qa ids in run artefacts — haiku-full-canon 33 hits/22 files, sonnet-full-canon-repair 461/21, gemma-full-canon 21/21, from `git grep` on those branches) → entered context (yes for those lanes) → model referenced it (yes: `work/eval-037-sonnet-controlled-canon : runs/sonnet-controlled-canon/packages/E037SCC-sonnet-B04-R2.txt:89` cites `qa_abcd_0011` "used to structure the hook-then-sustain opening"; `B03-R1.txt:67` cites `qa_whip_0032`) → changed a decision (**model-reported only**; not verified) → decision correct (UNKNOWN — `EVAL-037/CONCLUSION.md:62` records B04 skincare video as "Sonnet NO_CANON lead", i.e. the one trial that cited an ABCD Q&A item did not beat the no-Canon arm) → survived production (no: never in a production job) → QA detected failure (n/a).

**Answer: consumed by nothing today. Proof: packs.py reads only compiled PACK files; test asserts `canon/qa/` absent; four contracts forbid it; the sole reader is a sealed experiment.**

---

## 6. Evaluation of uses

Baseline facts for costing: 1,028 pairs ≈ 300k tokens; answers ~150 words; 0 graded; 86% author-referential; 13 banks mislabelled; `ries` retired; 5 sources still HOLD (232 items); 18 accepted (796 items).

**(a) Retrieval context for creative reasoning at decision time.**
Pros: the ABCD/Ogilvy/LSM items are genuinely decision-shaped and already hedged ("the source gives no duration"). Cons (evidence): (i) EVAL-037 showed lexical retrieval over-selects Q&A (26.4% of exposed objects) and the unbounded Sonnet lane overflowed 16/18 (`CONCLUSION.md:83`); (ii) four contracts forbid Q&A in the production surface and `packs.py` has no path to it; (iii) answers describe *what a book says*, which the compiled packs already carry as doctrine with check ids — injecting Q&A duplicates SK content in a chattier form; (iv) 232 items are over HOLD/retired sources. Cost: per-request ~2–3k tokens if 10 items injected (USD-trivial), but the governance cost is a Controller ruling reversing R4/PRODUCTION-SPEC §canon plus a compiled-pack contract change. Shaped for it: **no** (only ~15 items are production-question-shaped).

**(b) Dynamic checklist / "questions an expert asks" for intent completion.**
Pros: `failure_diagnosis` (81), `repair` (45), `boundary_condition` (93) and the universal `confounders` field are the raw material for checks; the SC-type questions (334) could be inverted into "have you decided X?" prompts. Cons: the questions are not the expert's questions — they are the examiner's questions about the expert's book (sample: 12/20 RC, 2/20 IC). A transformation pass is required (rewrite each into a production-facing check, drop the author reference, attach the pack check id); the 21 check ids already injected for Cumin come from operational bindings, not Q&A, so the checklist role is already occupied by a governed artefact. Cost: one LLM rewrite pass ≈ 1,028 × ~600 tokens ≈ 0.6M tokens (single-digit USD on a Sonnet-class model), plus human review of the output (the real cost, ~1–2 days), plus a schema. Shaped for it: **partially** (after transformation), and only for the ~20 banks that are practitioner texts; the ethnographies (jain, dwyer-patel, sontag) yield almost nothing.

**(c) Independent critic / judge prompts.**
Pros: the answer style ("judged strictly by this source, what is wrong — and what is not") is exactly a rubric-bound judge's output; qa_abcd_0010/0019/0011 could seed an "ABCD compliance judge" for 9:16 product films today. The corpus's habit of stating the source's limits reduces over-claiming. Cons: 0 items graded, so a judge seeded from them inherits extractor opinions (sample #10 presents extractor-authored "problems he does not raise" as content; #17 a retired source). Cost: low — a judge prompt per domain built from 5–15 items; no training. Shaped for it: **yes for 2–3 domains** (ABCD video, WCAG legibility, LSM packshot lighting); not corpus-wide.

**(d) Fine-tuning / distillation / SLM training.**
Persona 53/54 view. 1,028 pairs (≈300k tokens) is enough for a LoRA/SFT *format and style* adaptation of a 1–8B model (typical instruction-tuning sets of 1k–10k examples do that), and it is *already* a distillation set: every answer was written by a frontier Claude session from the source text (commit authors "Canon Experimental Worker", "Claude (CANON-014)"), never by a human. It is **not** enough for knowledge injection: each fact occurs once, with no paraphrase augmentation; SFT on single-exposure facts yields poor recall (general ML knowledge — INFERENCE, not measured here). Further blockers: no train/dev/test split; no graded answers so no held-out metric; `difficulty` is authored not empirical; 13 stale status labels; licence of the underlying copies "not independently verified" (experimental README §2), with public-domain/openly-licensed status established only for Hopkins ×2, WCAG, Google ABCD (`SOURCE-STATUS.csv`). Cost: compute trivial (an 8B LoRA epoch is ~1 GPU-hour); the cost is building the evaluation that would tell you whether it did anything — which does not exist. Shaped for it: **no**, and the target task (creative production reasoning) is not the task the pairs teach (book recall).

**(e) Evaluation benchmark ("does the agent know X").**
The README forbids calling it a benchmark and is right: nothing has been answered, so there is no baseline, no inter-rater agreement, no calibration. But it is the nearest thing in the repo to one: unique ids, locator, support, confounders. To become one: grade a stratified subset (e.g. 200 items; human at ~3 min/item ≈ 10 h; or LLM-judge against `support` with human spot-check), split by source status, and freeze. The most valuable variant is a **retrieval benchmark**: "given this question, does the retriever return the right source/locator?" — that needs no answer grading and CANON-015 already built the harness (`8115400:canon/retrieval/evaluation/`). Shaped for it: **yes, with a grading pass**; the mislabelled `source_status` must be fixed first or the benchmark reports the wrong split.

**(f) What the material itself suggests.**
1. *Extraction QA*: the corpus was built as a check on extraction ("if the extraction has understood a source, a question about that source should be answerable from it"). The experimental branch's `grounding_audit.py` (verifies support quotations occur at the cited locator) is the right tool and never reached main; running it would upgrade "grounded" from asserted to measured. Cost: minutes of compute; needs the source texts (not committed).
2. *Conflict mining*: items like qa_ogx_0073 (two Ogilvy rules competing for the first ten seconds), qa_abcd_0005 (guidance loses its premise on muted feeds) and the accepted-vs-retired `ries`/Binet tension are exactly the cross-source conflicts the CONTEXT-SPEC wants resolved; they could feed `CROSS-SOURCE-RELATIONSHIPS.yaml`.
3. *Regression tests for packs*: a compiled pack's check ids could be tested against the 15 production-shaped ABCD/Ogilvy items to see whether the pack encodes what the Q&A says the source says.

---

## 7. Intent-completion vs reading comprehension

From the 20-item sample: **reading comprehension 12 (60%), scenario-costumed comprehension 6 (30%), genuine practitioner checks 2 (10%)**. Corpus-level proxies agree: 86.4% of questions name the author/source; `requires_application` is 40.7% but by the manifest's own criterion it means "puts a case not in the source on the table and asks what follows [from the source]" — still a question about the source. **The corpus encodes "what does this book say (about this case)", not "what does a professional remember to ask".** The exception is concentrated in google-abcd, WCAG and light-science-magic (normative or procedural sources), where the two coincide.

---

## Findings ranked

1. **Consumed by nothing in production; explicitly forbidden by four contracts; only reader is the sealed EVAL-037 FULL_CANON experiment.** (`runtime/canon/packs.py` docstring & line 158; `runtime/tests/test_canon_lookup.py:66-69`; `canon/context/CANON-CONTEXT-SPEC-v0.1.md` R4; `runtime/contracts/PRODUCTION-SPEC-v1.yaml:69`; `canon/packs/COMPILED-PACK-CONTRACT-v0.1.md:54`.) OBSERVED.
2. **The corpus is stale and self-contradictory since DN-06 (2026-09-01):** the committed validator reports 26 errors on main (manifest says 0); banks say 108/920 accepted/hold, index totals say 796/232, index per-source entries contradict themselves for 13 sources. Nothing has edited `canon/qa` since c6f8d91. OBSERVED (computed).
3. **It is a reading-comprehension corpus over books, not an intent-completion corpus:** 86.4% author-referential questions; sample 12 RC / 6 SC / 2 IC. Only ~15 items (google-abcd, ogilvy ch.8, LSM ch.9) answer Cumin-shaped questions (brand-early, hook, CTA placement, super = VO, packshot on white). OBSERVED counts + INFERENCE on kinds.
4. **EVAL-037 shows what happens if it is retrieved naively:** Q&A was 26.4% of exposed objects because the lexical ranker rewards question-shaped text; Sonnet-controlled cited `qa_abcd_0011` in B04 and that brief was won by NO_CANON. Retrieval → context → reference is proven; decision change and correctness are not. OBSERVED/UNKNOWN.
5. **Best-shaped uses are narrow:** (c) domain judge prompts for ABCD/WCAG/packshot lighting, (e) a retrieval benchmark after a grading pass, (f) running `grounding_audit.py` from the experimental branch to turn "grounded" into a measurement. Fine-tuning/SLM use is not supported by 1,028 single-exposure, ungraded, licence-unverified pairs. INFERENCE.
6. **Provenance is honest but thin:** 100% have locator+support; only 38.9% have page-level locators; answers were written by Claude lanes on 2026-08-30 in ~5 hours for 899 items (≈3 items/minute across parallel lanes), with no human review; the experimental branch's independent grounding audit tool was not carried to main. OBSERVED.
7. **Hazard item:** `ries-22-immutable-laws-branding-qa-bank.yaml` (50 items) presents positions of a source the Controller ruled to retire in favour of Binet (DN-05) as ordinary "hold" content; any future exposure must exclude it. OBSERVED ruling / INFERENCE hazard.

## Open questions / unknowns

- UNKNOWN: whether any Q&A item has ever been answered by any model or human outside EVAL-037 (none found on main; trial branches not exhaustively read).
- UNKNOWN: whether `grounding_audit.py` was ever run and with what result — the experimental README claims lane self-checks; no committed audit output was found.
- UNKNOWN: licence status of 13 of the 17 experimental sources (only Hopkins ×2, WCAG, Google ABCD have a stated public-domain/open basis in `SOURCE-STATUS.csv`); relevant to any training use.
- UNKNOWN: why DN-06 updated the index totals but not the banks/manifest — no decision text addresses the Q&A labels; likely oversight (INFERENCE).
- Not resolved: which Q&A items, if any, the compiled packs' 21 check ids for Cumin overlap with; a pack-vs-Q&A consistency check was out of scope.

---

## A. Appendix — commands run

A.1 Counts/fields: `python3 canon/qa/canon-014/validate_qa_corpus.py`; per-bank loop with `yaml.safe_load` counting `qa_items`, `requires_application`, field presence, `source_locator` matching `p.|pp.|page`, non-empty `support`.
A.2 Keyword search: regex over `question + answer` per item for the eight Cumin groups; output `agents/07-keyword-hits.txt` (245 lines).
A.3 Sample: `random.seed(20260916); random.sample(items, 20)`; output `agents/07-sample20.txt`.
A.4 Index contradictions: for each `sources[]` entry, compare `epistemic_status` with any nested dict carrying `qa_items` and `source_status` → 13 contradictions.
A.5 Branches: `git log --format='%h %ad %an %s' --date=iso main..work/canon-parallel-books-qa-experimental`; `git ls-tree -r --name-only <branch> | grep -i qa`; `git diff main...<branch> --stat`; `git archive <branch> canon/experimental/book-expansion-qa-v1 | tar -x -C <scratch>`; `git merge-base --is-ancestor`.
A.6 Consumers: `grep -rn -E 'canon/qa|qa-bank|qa_bank|QA-MANIFEST' --include='*.py' --include='*.md' --include='*.yaml' --include='*.json' .` (excluding .git and canon/qa); `git grep -c -E 'qa-bank\.yaml|"qa_[a-z0-9]+_[0-9]{4}"' <eval-037 branch> -- eval/experiments/EVAL-037/runs`.
A.7 Decisions: `grep -rn -i -E "Q&A|qa corpus|canon/qa|qa bank" coordination/decisions/*.md governance/reviews/*.md`; `git log --all --grep='CANON-014'`, `--grep='Q&A' --grep='qa bank' --grep='qa-bank'`.
