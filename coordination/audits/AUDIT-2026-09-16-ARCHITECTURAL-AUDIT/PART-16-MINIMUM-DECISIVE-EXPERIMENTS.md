# PART 16 — MINIMUM DECISIVE EXPERIMENTS

The fewest experiments that distinguish the leading hypotheses (Part 12 §3) and drive the decision tree (Part 14). Designed by council 10 §6.2, extended by councils 11 §9, 14 §4.2 and 15 §5, adopted by the lead. All are RECOMMENDATION. None has been run; nothing here authorises spend — every arm requires a Controller spend authorisation under the existing cap discipline. No experiment merges anything, compiles a pack onto `main`, changes the Registry, or touches Controller state; experiment-only artefacts live under `eval/experiments/` on a branch.

## 0. Common substrate

- **Briefs (9):** the six EVAL-037 briefs (B01–B06, committed) + the three real briefs verbatim (Upwork intro paragraph + owner instruction; Nivaas tile; Cumin).
- **Rejection checklist (~25 distinct items):** derived from the 42 human rejection items across the three cases (council 10 §4.2), written *with* the judges in E6, binary and instance-level.
- **Judges:** two non-author reviewers by unanimity (the value-gate rule), position-balanced, blind to arm; the author-judge participates in E6 and, if κ ≥ 0.6, as one reviewer thereafter.
- **Outcome measure:** fraction of the known rejection reasons a plan/artefact pre-empts (checklist hit rate) + the value-gate's nine dimensions for plans; accept/reject + defect class for artefacts.
- **Model:** one strong reasoning model fixed throughout unless the arm varies it. Prices: ≈ USD 0.05–0.20 per reasoning package; media at case-pinned prices (image ≈ 0.07; 6-s Veo fast ≈ 0.60).
- **Order:** E6 → E0 → E4 / E5 (USD 0 media) → E1 → E3 → E2 → E7 → (later) plate ablation.

## 1. The set

| # | Question (hypotheses) | Arms | n | Cost ceiling | Outcome | Reading (→ Part 14 node) |
|---|---|---|---|---|---|---|
| **E6** Judge reliability (prerequisite) | Is the single judge a usable instrument? | 3 judges (author + 2 non-authors), blind, on the 15 versions/tiles from the three cases: accept/reject + defect class | 15 × 3 | ~2 h human, USD 0 | Fleiss/Cohen κ on accept/reject; agreement on defect class | κ < 0.4 → stop; write the checklist with the judges first (NODE 0) |
| **E0** Prior sufficiency (U4) | Does a strong model, given the Cumin brief verbatim and no repo context, propose product end card + brand from frame 1 unprompted? | one arm, ≥ 5 samples; score presence of hero/opening/CTA/end-card/brand-early | 5 | USD < 1 | count of samples with all four | ≥ 4/5 → the failure was the instruction set; ≤ 2/5 → a required question is necessary (NODE 1) |
| **E4** Role collapse (E, K7) | Does an independent reviewer catch what the producer self-passed? | replay the 3 Cumin versions + 5 case-002 B1-lineage tiles: (i) producer's own QA rows as recorded; (ii) a fresh session (no job context) given artefact + checklist; (iii) a second human | 8 × 3 | USD ≈ 5 (no media), ~2 h human | fraction of human-named defects flagged before presentation; self-PASS lines overturned | (ii) or (iii) ≥ 50 % of what (i) missed → fund the checker role before any Canon work (NODE 1) |
| **E5** Assembly-only replay (J) | Were Cumin's rejections assembly problems? | re-assemble V1–V3 from the same accepted components under `check_vo_schedule` + a subject-box obstruction gate + edge-trim audio; re-export 002 B1 tiles under the runtime gates; blind A/B originals vs replays | 6 pairs × 3 judges | USD 0 media, ~1 h human | per-defect flip rate on the 7 + 13 HD criteria; overall accept; also answers U10 (V3 with clean audio) | ≥ 5/7 flips → assembly dominates 003; structural items will not flip → those are E1's domain (NODE 1) |
| **E1** Context ladder (A, C, F, H) | Does *what* is in context matter, and does more hurt? | (a) no Canon; (b) oracle hand-picked compiled-form doctrine ≤ 2.5 k tokens; (c) same content as raw source excerpts ≈ 10 k; (d) union of all ten packs' sources ≈ 35 k+ | 9 × 3 reps × 4 = 108 packages | USD 25 | value-gate 9 dims + rejection-checklist hit rate | b > a & c ≈ a → form is the lever; d < b → overload; b ≈ a → knowledge not the bottleneck (NODE 2) |
| **E3** Short checklist (L, M/N) | Does a 40-line rejection-derived checklist match oracle Canon? Does its *source* matter? | (b) oracle vs (f) strong + checklist vs (g) strong + checklist + oracle; checklist built (m) from human rejections and (n) from Q&A/eval data | 9 × 3 × 3 = 81 (+ f_m/f_n) | USD 18 | same | f ≥ b → L; g > f → Canon adds beyond the checklist; f_m vs f_n → M/N (NODE 2) |
| **E2** Retrieval (B) | Does the trigger-table lookup lose what the oracle finds? | (b) oracle vs (e) `runtime.canon.lookup` output for the same NR with all ten packs compiled **for the experiment only** (branch, not merged) | 9 × 3 × 2 = 54 | USD 12 | same | e < b → lookup/compilation loses value; e ≈ b → policy was the only block (NODE 3) |
| **E7** Model sufficiency (D) | Does a strong reasoning model with oracle context beat a weak one with the same? | E1 arm (b) with strong vs weak reasoning model | 9 × 3 × 2 = 54 | USD 8 | same | strong+b ≫ weak+b and strong+a ≈ strong+b → D dominates (NODE 4) |
| **E8** Plate ablation (U9; later) | Did the PA-D lighting/finish vocabulary and the no-text clause cause the clean Cumin plates? | same five plate prompts minus PA-D vocabulary and the no-text clause, one draw each; blind pairwise vs the accepted plates | 5 pairs × 2 judges | USD ≈ 0.35 | lighting/finish/lettering defects appear or not | defects appear → the one Canon chain that reached state 7 is demonstrated; none → co-owned by baseline craft |

**Totals:** ≈ USD 70 of API/media (E1 25 + E3 18 + E2 12 + E7 8 + E4 5 + E0 1 + E8 0.35) plus ≈ 5–7 h of human judging; every arm reuses committed briefs and accepted components; no new route qualification; no Registry effect. This is inside the 28-Aug head review's "USD 30–60, blinded, on 8 real briefs" envelope that was never run.

## 2. Pre-registration (write before running; commit on the experiment branch)

- Decision rules per arm as in the table; unanimity of the two non-author reviewers; position balance stratified per brief.
- The checklist text, frozen after E6, with the judges' signatures.
- The oracle contexts for E1(b) hand-picked *before* any package is generated and hashed.
- Treatment blindness: packages must not self-disclose treatment (the EVAL-037 defect at package line 98); strip any "Canon knowledge used" section before judging.
- Spend authorisation per experiment; the ledger governs; vendor statements read at the end (the reconciliation gap of Part 13 R3 is not repeated).

## 3. What each result changes (summary; full branches in Part 14)

| Result | Consequence |
|---|---|
| E6 κ < 0.4 | no other verdict-based number in the programme is interpretable; the checklist is written first |
| E4 ≥ 50 % and E5 ≥ 5/7 | Part 15 as written; Canon work deferred |
| E1 b ≈ a and E3 f ≥ b | Canon = provenance library; no pack compilation; Prosecutor's charges 3, 7 stand |
| E1 b > a, c ≈ a, d < b and E3 g > f | compile `commercial_communication` in checklist form under a decision; Defender's §3 stands |
| E2 e < b | job-time assembly replaces the pack lookup |
| E7 strong ≫ weak | the Lab's reasoning half reopens; media routes stay closed |
| E8 defects appear | keep the four typed lighting fields as Canon-derived; else as baseline craft |

## 4. What is deliberately not proposed

- No new Capability Lab cells: nothing the Lab measures predicts acceptance (Part 12 cause 8); the acceptance-critical capabilities need judges, not format probes.
- No fine-tuning: no labels; Part 8 D1/D2/D12.
- No retrieval build over the 7 MB corpus before E1/E2: the relevant material fits in context; near-miss chunks hurt.
- No new personas without a checklist: Part 8 E1–E5.
- No experiment whose outcome is the author-judge alone.
