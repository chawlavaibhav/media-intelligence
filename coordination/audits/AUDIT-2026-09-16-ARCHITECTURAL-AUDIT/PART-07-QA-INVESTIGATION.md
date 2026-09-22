# PART 7 — Q&A INVESTIGATION: what exists and what it is actually good for

Source: council report 07 (`council-reports/07-qa-corpus.md`, all counts recomputed by shown commands), cross-checked by councils 06 §6, 14 §Charge 5–7, 15 §4. Refs: MI `main @ 3bb9a3c`; branches `work/canon-parallel-books-qa-experimental @ 3c29c8d` and `claude/canon-014-expansion-admission-ntp0dl @ 22656b9` (both unmerged). Labels: OBSERVED / INFERENCE / HYPOTHESIS / UNKNOWN.

---

## 1. Where it lives and exact counts (OBSERVED)

| Location | Ref | Items |
|---|---|---|
| `canon/qa/canon-014/` — 23 `*-qa-bank.yaml` + `QA-MANIFEST.json` + `README.md` + `validate_qa_corpus.py` | main @ 3bb9a3c | **1,028** |
| `canon/experimental/book-expansion-qa-v1/<source>/qa-bank.yaml` (17 per-source dirs, each with its own `grounding_audit.py`) | branch `3c29c8d`, unmerged, +134,743 lines | 899 |
| `canon/experimental/canon-014-qa/*-qa-bank.yaml` (6 Indian-context banks) | branch `22656b9`, unmerged | 129 |

Lineage: 899 + 129 = 1,028; consolidated on `work/canon-014-final-full-canon` and landed on main in one commit `c6f8d91` (30 Aug 2026 18:43 IST, "CANON-014: integrate full Canon corpus"). `git log -- canon/qa` on main shows exactly one commit: **never edited since landing.** No Q&A exists on any branch that is not on main.

Provenance: the 899 were written by "Canon Experimental Worker" Claude lanes between 08:18 and 13:05 IST on 30 Aug (≈ 3 items/minute across parallel lanes); the 129 by "Claude (CANON-014)". No human authored or reviewed any item (README: "No expert has reviewed them"). The experimental branch's `grounding_audit.py` (checks that support quotations occur at the cited locator) did not travel to main; UNKNOWN whether it was ever run.

Fields: all 1,028 carry `qa_id, source_id, source_locator, question, answer, answer_type, difficulty, knowledge_type, requires_application, support, confounders, source_status`. `support` non-empty on 1,028/1,028; page-level locators on 400/1,028 (38.9 %); `requires_application` on 418 (40.7 %). Question mean 31 words; answer mean 150 words; total ≈ 222 k words ≈ 300 k tokens.

Per-bank sizes: hopkins-my-life 80 · sullivan 78 · ogilvy-beyond-ch2 76 · light-science-magic 62 · berger 60 · freeman 58 · airey 57 · hopkins-sa-ch8-21 57 · kahneman-noise 57 · connor-irizarry 51 · ries 50 · samara 46 · wcag 41 · godin 37 · carroll 35 · sontag 28 · google-abcd 26 · parameswaran 26 · dwyer-patel 23 · bijapurkar 21 · desai 21 · jain 21 · pandey 17.

**Validator conflict (OBSERVED).** `QA-MANIFEST.json` says `errors: 0`; README says "108 accepted / 920 hold". Running the committed validator today prints **`23 banks, 1028 items, 26 errors`**: 13 banks claim `hold` while their sources now live in the accepted tree (moved by the DN-06 admission batch on 1 Sep, `CONTROLLER-REP-07-ADMISSION-BATCH-2026-09-01.md`), and their `knowledge_dir` under `canon/candidates/` no longer holds a `source-knowledge.yaml`. `CANON-CORPUS-INDEX.yaml` totals say 796 accepted / 232 hold, while 13 of its per-source entries carry `epistemic_status: accepted` next to a nested `source_status: hold`. Three artefacts disagree on one fact. Actual state by where the source lives: **796 items over 18 accepted sources; 232 over 5 HOLD sources** (airey 57, ries 50, samara 46, freeman-beyond 58, desai 21). Ries was ruled retired in favour of Binet (DN-05) but its 50 items present its positions as ordinary "hold".

---

## 2. Subject coverage (OBSERVED)

| Domain | Banks | Items |
|---|---|---|
| Advertising / commercial communication | hopkins ×2, ogilvy, sullivan, google-abcd, pandey, parameswaran | 360 |
| Branding / marketing strategy | ries, godin, berger | 147 |
| Design / typography / legibility | airey, samara, connor-irizarry, wcag | 195 |
| Photography / light | light-science-magic, freeman, carroll, sontag | 183 |
| Film / Indian visual culture | dwyer-patel, jain | 44 |
| Indian market / consumer | bijapurkar, desai | 42 |
| Behavioural / judgement | kahneman-noise | 57 |

`knowledge_type` top values: evaluation_diagnosis 127, advertising 123, brand_communication 99, creative_process 72, composition 67, persuasion 64 … short_form **6**, shot_design 12, lighting 14, production 9. **No bank on editing/pacing, motion, voice performance, sound, or Devanagari/Indic typography.** No item mentions "safe area", "safe zone", "tutorial" or "hero shot".

Cumin-relevant keyword hits (regex over question+answer; many incidental): product role/hero 7; opening/hook 11; CTA/end card 10 (7 in google-abcd); brand mention/early 23; proposition/proof 28; voice/VO 46 (mostly "brand voice"); text-over/legibility 55 (mostly WCAG contrast). The items that directly answer Cumin-shaped questions are concentrated in `google-abcd-video-ads` (26), `ogilvy-beyond-ch2` ch. 8 TV tips, and `light-science-magic-beyond-ch3` packshots — **≈ 15 items of 1,028 (1.5 %)**.

The ten most Cumin-relevant pairs (trimmed; `file:line` = the `- qa_id:` line on main):
1. `google-abcd-video-ads-qa-bank.yaml:277` **qa_abcd_0010** — a 20-s ad "opens on a silent slow-motion product beauty shot, brings the logo up only at the very end, shows no people at all, and closes on a 'Buy now' end card … what is wrong with it — and what is not?" → three of four awareness instructions missed; the end card is not wrong on this source's terms. (This describes the Cumin V1/V2 shape almost verbatim.)
2. `:311` **qa_abcd_0011** — CTA in the first two seconds? → "It says the opposite … 'Present the ask after the context is set'."
3. `:535` **qa_abcd_0019** — no brand presence until a five-second lockup at the end → misses "show up early and throughout", "reinforce with audio", "draw on all branding assets".
4. `:141` qa_abcd_0005 — muted feed placement: every audio-dependent guideline loses its premise; the source says nothing about what to do instead.
5. `:448` qa_abcd_0016 — hook vs sustain; no duration is ever named.
6. `ogilvy-beyond-ch2-qa-bank.yaml:2603` **qa_ogx_0073** — eight seconds of wordless atmosphere, brand named at 22 s, super paraphrases VO → three objections; "the visual surprise and the brand name compete for the same seconds".
7. `:952` qa_ogx_0027 — slow atmospheric opening: "the viewer will never find out, because she has left the room" (1983 broadcast context stated).
8. `:915` qa_ogx_0026 — "use the name within the first ten seconds … ending by showing the package".
9. `light-science-magic-beyond-ch3-qa-bank.yaml:1384` **qa_lsmx_0039** — white ceramic on white reads as "product on grey": relight so the background carries the extreme.
10. `hopkins-scientific-advertising-ch8-21-qa-bank.yaml:1663` qa_sa8_0048 — picture shows the face as it will appear; CTA assumes compliance.

---

## 3. Quality (20-item sample, `random.seed(20260916)`; INFERENCE on grades)

| Measure | Result |
|---|---|
| Grounded (locator + support) | 20/20 (page-level 7/20; corpus-wide 38.9 %) |
| Specificity (would change a production decision) | H 2 · M 6 · L 12 |
| Correctness risk | L 14 · M 5 · **H 1** (qa_r22_0045 — a retired source's position stated as advice) |
| "A question a professional remembers to ask" | Y 2 · partial 8 · N 10 |
| Kind | reading-comprehension 12 · scenario-costumed comprehension 6 · genuine practitioner check 2 |

Corpus-wide proxies agree: **86.4 % (888/1,028) of questions name the author, "the source", "this book" or "the authors"**; 32.5 % open with a scenario. Best property: answers are careful about what the source does *not* say, and the `confounders` field (present on all items) names the plausible wrong answer. Weakness for production: the question is almost always *about the author* ("What does Hopkins say…"), and `requires_application` by the manifest's own definition still means "what follows from the source", not "what does a producer check". Sample #5 (qa_ppm_0015) answers about *this project's binding record*, not the book; #10 presents extractor-authored "problems he does not raise" as content.

**Verdict on "questions a professional remembers to ask" (OBSERVED counts + INFERENCE):** the corpus encodes "what does this book say (about this case)", not intent completion. The exception is concentrated where the source is normative or procedural (google-abcd, WCAG, light-science-magic) — there the two coincide.

---

## 4. Authority (OBSERVED)

- **Never admitted into production authority, by design.** README: "Outside [the Audit Gate], deliberately … No Audit Gate record covers any file in this directory." `AUDIT-GATE-v0.2.md` does not mention Q&A.
- Controller decision `CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md` (PR #69): "1,028 grounded, ungraded, uncalibrated Q&A items retained … This merge does not enable HOLD/candidate retrieval in ordinary runtime … A future experiment may deliberately expose the full status-aware corpus and Q&A, but must record the exact fingerprints used."
- Two fingerprints exist for the same 23 files: `CANON-CORPUS-INDEX.yaml` `qa_corpus` digest `1313c0ba…` (matches EVAL-037's execution contract) vs `QA-MANIFEST.json combined_digest 25ac8bbc…` (different algorithm; Governor note G14-N1).
- **Four contracts forbid Q&A on the production surface:** `canon/context/CANON-CONTEXT-SPEC-v0.1.md` R4 ("Q&A banks must not appear"); `canon/context/canon-context-schema-v0.1.yaml:84`; `runtime/contracts/PRODUCTION-SPEC-v1.yaml:69` ("No HOLD material, no Q&A corpus, no free-form retrieval"); `canon/packs/COMPILED-PACK-CONTRACT-v0.1.md:54,172,192` ("HOLD/QA ids fail validation").

Answer: **experimental companion asset; not authoritative; never admitted; explicitly excluded by four contracts.**

---

## 5. Consumption today (OBSERVED, with proof)

- `runtime/canon/packs.py` docstring: "no HOLD material; no Q&A corpus"; the only files it reads are `pack-triggers-v0.yaml` and `canon/compilation/PACK-*-v0.yaml` (line 158). **There is no code path from a Normalized Request to `canon/qa/`.**
- Regression test `runtime/tests/test_canon_lookup.py:66-69` `test_no_hold_material_can_reach_the_payload` asserts `"canon/qa/"` is absent from the payload — the runtime is unit-tested to *exclude* it.
- `compile_pilot_packs.py` reads `source-knowledge.yaml` only (line 550).
- `.claude/skills/media-agency/**`: zero references to `canon/qa` or qa-bank. Cumin `JOB.yaml:111-116` records a pack-path lookup only.
- **The only reader:** `eval/experiments/EVAL-037/tools/canon_tools.py` (BM25 search + `canon_read` over accepted + HOLD + Q&A, FULL_CANON lanes only) — a frozen, completed experiment. Unmerged CANON-015 (`8115400`) built an accepted-only retriever precisely to exclude Q&A/HOLD; its brief reports that of 424 objects EVAL-037's unbounded lane exposed, **HOLD Q&A = 94 (22.2 %) and accepted Q&A = 18 (4.2 %)**: "Q&A items are short and question-shaped and the lexical ranker rewards that."

Eight-state ladder: exists ✔ → retrieved ✔ (EVAL-037 FULL_CANON lanes; haiku 33 hits, sonnet-full-canon-repair 461, gemma 21) → in context ✔ → referenced ✔ (`work/eval-037-sonnet-controlled-canon … B04-R2.txt:89` cites `qa_abcd_0011` "to place the CTA after context is established"; `B03-R1.txt:67` cites `qa_whip_0032`) → changed a decision: **model-reported only** → correct: UNKNOWN (B04 was judged a NO_CANON lead; the one trial that cited an ABCD Q&A item did not beat the no-Canon arm) → survived production: never in a job → QA: n/a.

**Answer: consumed by nothing today.**

---

## 6. Five uses evaluated (baseline facts: 1,028 pairs ≈ 300 k tokens; 0 graded; 86 % author-referential; 13 banks mislabelled; ries retired; 232 items over HOLD sources)

| Use | Fit | Evidence for | Evidence against | Cost | Verdict |
|---|---|---|---|---|---|
| **(a) Retrieval context for creative reasoning** | **No** (corpus-wide); narrow yes for ~15 items | ABCD/Ogilvy/LSM items are decision-shaped and pre-hedged; `qa_abcd_0010` is a worked negative example of the exact Cumin V1/V2 shape; LEAP/RICP literature (Part 8) shows mistake-anchored principles move decisions where abstract prefixes do not | EVAL-037: lexical retrieval over-selects Q&A (26.4 % of exposed objects); unbounded Sonnet overflowed 16/18; four contracts forbid it; answers duplicate SK doctrine in a chattier form; 232 items over HOLD/retired sources; near-miss chunks are harmful (Cuconasu 2024, Chroma 2025) | USD-trivial per request; governance cost = a Controller ruling reversing R4 / PRODUCTION-SPEC §canon / pack contract | Do not open retrieval over the corpus. Hand-copy 3–5 items per pack (start `qa_abcd_0010/0019/0011`, `qa_ogx_0073`, `qa_lsmx_0039`) into a negative-example appendix with source ids; that is "copied, id-cited items", not "Q&A retrieval" — needs a one-line Controller note |
| **(b) Dynamic checklist / "questions an expert asks"** | **Partially, after transformation** | `failure_diagnosis` (81), `repair` (45), `boundary_condition` (93) and the universal `confounders` field are raw material; 334 scenario items could be inverted into "have you decided X?" | The questions are the examiner's, not the expert's (sample 12/20 RC, 2/20 IC); the 21 check ids already occupy the checklist role and come from bindings, not Q&A; ethnographies (jain, dwyer-patel, sontag) yield almost nothing | one LLM rewrite pass ≈ 0.6 M tokens (single-digit USD) + 1–2 days human review + a schema | Useful only as *seed material* for the ≤12-line ad-structure checklist recommended in Parts 15/17; not as a runtime asset |
| **(c) Independent critic / judge prompts** | **Yes for 2–3 domains** | the answer style ("judged strictly by this source, what is wrong — and what is not") is a rubric-bound judge's output; `qa_abcd_0010/0019/0011` could seed an ABCD-compliance judge for 9:16 product films today; hedging reduces over-claiming | 0 items graded → a judge inherits extractor opinions (#10, #17); needs a fresh-context reader, not the author (Part 8 E1–E4) | low: 5–15 items per domain; no training | **Best-shaped use.** ABCD video structure, WCAG legibility, LSM packshot lighting. Feeds experiment E4 (Part 16) |
| **(d) Fine-tuning / distillation / SLM** | **No** | 1,028 pairs is enough for LoRA/SFT *format* adaptation of a 1–8B model | each fact occurs once (no paraphrase augmentation → poor recall; Ovadia 2023, Gekhman 2024 in Part 8); already a Claude distillation set, never human-checked; no train/dev/test split; no held-out metric; `difficulty` authored not empirical; licence status of 13/17 sources unverified; target task (production reasoning) ≠ the task the pairs teach (book recall) | compute trivial; the cost is building the evaluation that does not exist | Not supported |
| **(e) Evaluation benchmark** | **Yes, with a grading pass** | unique ids, locator, support, confounders — nearest thing in the repo to a benchmark; the most valuable variant is a **retrieval benchmark** ("does the retriever return the right source/locator?") which needs no answer grading; CANON-015 built the harness (`8115400:canon/retrieval/evaluation/`) | nothing has been answered; no baseline, inter-rater agreement or calibration; stale `source_status` labels would report the wrong split | grade a stratified 200-item subset ≈ 10 h human (or LLM-judge vs `support` with spot-checks); fix labels first | Supported as a *Canon extraction* benchmark, not as a production benchmark |

What the material itself suggests (INFERENCE): (1) run `grounding_audit.py` from the experimental branch to turn "grounded" from asserted into measured (minutes of compute; needs source texts, not committed); (2) conflict mining — `qa_ogx_0073`, `qa_abcd_0005`, the ries/Binet tension are exactly the cross-source conflicts CONTEXT-SPEC wants and could feed `CROSS-SOURCE-RELATIONSHIPS.yaml`; (3) regression tests for packs — test a compiled pack's check ids against the ~15 production-shaped ABCD/Ogilvy items.

---

## 7. Answers to the commission's Q&A questions

| Question | Answer |
|---|---|
| Exact count(s) | 1,028 on main (23 banks); 899 + 129 on two unmerged branches (identical to main); no other Q&A anywhere |
| Provenance | Claude extraction lanes, 30 Aug 2026, ~5 h; no human authorship or review; grounding tool not carried to main |
| Subject coverage | advertising 360, branding 147, design/legibility 195, photography 183, Indian culture/market 86, judgement 57; none on editing, motion, voice, sound, Indic typography |
| Quality | grounded 100 % (page-level 39 %); long, hedged, careful about source limits; low specificity (12/20 L); 1/20 high correctness risk (retired source) |
| Grounded in accepted sources? | 796/1,028 by source location today; the banks' own labels say 108 (stale since DN-06); validator reports 26 errors vs a manifest that says 0 |
| Admitted into production authority? | No, by design; four contracts forbid it |
| Consumed by current production? | No; runtime tested to exclude it; skill never names it |
| Can the current retrieval system query it? | No — there is no retrieval system on main; `packs.py` is a table lookup over two compiled files. The only reader was the sealed EVAL-037 BM25 tool |
| Do they encode "questions a professional remembers to ask"? | Mostly no: 86.4 % author-referential; 2/20 genuine practitioner checks; yes in google-abcd / WCAG / LSM |
| Overlap with the missing intent-completion problem? | Thin: ~15 items describe the ad-structure judgement Cumin failed on (brand-early, hook, CTA placement, super = VO, packshot on white); nothing on product-role-as-hero as a question, voice register, or copy-over-subject |

**Red-team Q7 — are Q&A pairs a potentially superior interface for LLM consumption?** INFERENCE: as a *form*, yes for one narrow purpose — a worked negative example with scope discipline (`qa_abcd_0010`) is the most directly transferable representation in the corpus for "does this look like an ad?", and the external literature (Part 8 B3.3/B3.4) supports mistake-anchored principles over abstract doctrine. As a *corpus*, no: it is a reading-comprehension set over books, 1.5 % production-shaped, ungraded, mislabelled, forbidden by four contracts, and over-selected by naive lexical retrieval. Hypotheses M ("Q&A better substrate than packs") and N ("Q&A useful only as evaluation/training data") are both partly right: M for ≤ 15 hand-picked items as critic seeds and negative examples; N for the remainder as an extraction/retrieval benchmark. Neither supports opening Q&A retrieval in production. The decisive test is E3 in Part 16 (checklist built from Q&A items vs from human rejection transcripts).

## Open questions / unknowns
- UNKNOWN whether any Q&A item has been answered by a model or human outside EVAL-037.
- UNKNOWN whether `grounding_audit.py` was ever run and with what result.
- UNKNOWN licence status of 13 of the 17 experimental sources (only Hopkins ×2, WCAG, Google ABCD have a stated open basis in `SOURCE-STATUS.csv`).
- UNKNOWN why DN-06 updated index totals but not banks/manifest (likely oversight).
- Not resolved: overlap between the 21 compiled check ids and any Q&A items.
