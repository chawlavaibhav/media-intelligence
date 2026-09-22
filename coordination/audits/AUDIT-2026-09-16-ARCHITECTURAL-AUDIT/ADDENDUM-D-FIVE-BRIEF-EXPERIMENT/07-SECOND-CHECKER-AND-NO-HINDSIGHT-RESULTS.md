# Addendum D — Second checker (different model tier) and no-hindsight producer: results

Date: 2026-09-20. Controller item 2 ("run a second checker and a no-hindsight producer on the two EVAL-037 briefs"). Three agents: a Claude Opus checker on the original `02-checker-input.md` (all five briefs, ten plans); a Claude Sonnet producer with **no project history** given only `05-producer-input-no-hindsight.md` (the template + the two briefs + the claim list); a Claude Sonnet checker on `06-checker-input-v2-no-hindsight.md` (the rubric plus the two new lines: verification method per requirement, and line 12 judged against evidence rather than the plan's label). All verbatim outputs are preserved in this file's appendix sections. Labels: OBSERVED / INFERENCE / UNKNOWN.

## 1. Second checker vs first checker (OBSERVED)

| Brief | First checker (Sonnet): existing · five-stage | Second checker (Opus): existing · five-stage | Direction agrees? |
|---|---|---|---|
| B1 Cumin | 4/8 · 5/12 vs 7/8 · 12/12 | 5/8 · 4/12 vs 7/8 · 12/12 | yes |
| B2 Nivaas | 3 · 3 vs 8 · 9 | 3 · 3 vs 7 · 9 | yes |
| B3 Upwork intro | 6 · 3 vs 7 · 8 | 4 · 3 vs 5 · 9 | yes |
| B4 RentOK | 3 · 3 vs 7 · 9 | 3 · 4 vs 6 · 8 | yes |
| B5 Skincare | 4 · 6 vs 8 · 8 | 5 · 7 vs 6 · 8 | yes |
| Totals | 20/40 · 20/60 vs 37/40 · 46/60 | 20/40 · 21/60 vs 31/40 · 46/60 | yes |

B-line (structure) agreement between the two checkers: 111 of 120 lines identical (92.5 %). Every disagreement is on a line where one checker read a plan more strictly; none flips a plan from majority-YES to majority-NO. A-line agreement is lower (the Opus checker is harsher on A4 for the five-stage plans: it scored 0 on B3's five-stage plan for "STANDARD 24 HOURS", "six hooks" and "straight price", which come from the pilot's profile context and were not in the checker file's permitted facts — a fair reading of the file, and a real gap: the five-stage plan carried facts from outside the frozen inputs without saying so).

Things the second checker caught that the first did not (OBSERVED):
- B5 existing plan: "it calms my breakouts" is an efficacy claim the brief forbids. Neither the producer nor the first checker flagged it. This is the class of error that reaches a customer as a policy rejection.
- B3 existing plan: the mandated on-screen clock at the brief's arrival and the elapsed time in large type are absent from the beat sheet.
- B4 five-stage plan: the structural rules (two shots in 5 s, on-screen person beats VO, logos in context beat overlays) were asserted without a source in the checker file — because the producer paraphrased Canon and external claims without ids in the plan text. Correct reading; a sourcing discipline failure by the producer.
- B1 both plans: neither mentions the USD 8 cap in its spend plan (the five-stage plan discusses cost in Addendum B but not in the checker text).

INFERENCE: two checkers of different tiers agree on direction for all five briefs and on 92 % of structure lines; a second checker adds catches of its own (three material ones above). The Controller's requirement that the checker be a *separate execution context with the original evidence* holds up; making it *two* contexts costs one extra call and caught an efficacy claim.

## 2. No-hindsight producer (OBSERVED)

Scores (checker v2, 14 lines, 8 points):

| Brief | No-hindsight five-stage plan | For comparison: existing plan (checker 1, 12-line scale) | Hindsight five-stage plan (checker 1) |
|---|---|---|---|
| B4 RentOK | A 6/8 · B 8/14 | A 3/8 · B 3/12 | A 7/8 · B 9/12 |
| B5 Skincare | A 6/8 · B 7/14 | A 4/8 · B 6/12 | A 8/8 · B 8/12 |

On the twelve lines shared with the original rubric: the no-hindsight B4 plan scored 8/12 (existing 3/12; hindsight 9/12); the no-hindsight B5 plan 7/12 (existing 6/12; hindsight 8/12). The two added lines (13 verification methods; 14 every fact sourced) were both NO for both plans.

What the no-hindsight producer got right without project history (from the template alone): intent contract with flagged asks and defaults (A1 = 2 on both); mid-action opening; brand within 10 s with id cited; ask on card and spoken; close on product; mandatory events on numbered frames; supers = VO; copy zones off hands/faces; VO measured before timings (B4); riskiest-shot-first with a hands/UI composite (B4).

What it got wrong or missed:
- **Line 12 on B5**: it declared faces-speaking the highest risk and then, because the brief implies a real creator, chose to *film* the presenter and test only a generated product cutaway first. The checker (with the evidence) marked NO: the shot tested first contained no risk element. The producer solved the risk by leaving the generative pipeline — a legitimate answer for an agency, not for this system, and the template did not say "the deliverable is generated". Template defect, logged.
- **Line 13 (verification per requirement)**: both plans listed verifications but not one per mandatory item ("no invented statistic", "exactly one purchase reason" had no stated check). The template asks for it at 1.4; the producer wrote the requirement column and not the method column. Template needs the method column mandatory, not implied.
- **Line 14 (every fact sourced)**: "Reels default muted" and "faces speaking is a known generative risk" were asserted without a source — the second was in the producer's input as general knowledge without an id. A sourcing discipline failure in the *input*, not only the producer.
- **Line 9 (voice cast by ear on a full line before visuals)**: stated as "cast once" without the audition step, on both.
- **Line 7 (the selling frame)**: missed on both — the same gap the hindsight producer had on four of five. Now missed by two producers of different kinds; the template line 3.2 exists, so the failure is enforcement: the Stage Controller must refuse to close Stage 3 without a numbered hero frame.
- A2 = 1 on both: the plans asked the right questions and then proceeded with defaults while listing the same items as unresolved — the checker read that as "not resolved before spend". Fair. The template should distinguish "asked, default recorded, proceed permitted" from "asked, blocks".

INFERENCE: without hindsight and with only the template, the mechanism recovers most of the structural gain (B-lines: 8/12 and 7/12 vs the existing plans' 3/12 and 6/12) and loses about one line per brief against the hindsight producer. The lines it loses are the ones the template states but does not *enforce*: the numbered hero frame, the verification column, the audition step. That is the same finding as §3a of `04-RECONCILIATION.md`, now from an independent producer: **the reusable layer must be enforced by the Stage Controller, not left to the producer's reading of the template.**

## 3. Template changes implied (RECOMMENDATION, to fold into `QUESTION-TEMPLATE-v0.md` → v0.1)

1. Stage 1 line 1.4: the verification-method column is mandatory per mandatory item; a row without one blocks Gate 1.
2. Stage 1: add "the deliverable is produced by generative models; any element that would be solved by live filming must instead be solved by references, composition, or a test" — otherwise a producer will correctly choose to film.
3. Stage 1: separate "ask — blocks" from "ask — default recorded, proceed permitted at this cost tier"; the checker should score A2 on the former only.
4. Stage 3 line 3.2: Gate 3 refuses to close without a numbered hero frame.
5. Stage 3 line 3.10: the audition step (≥ 2 candidates, longest line, final pace) is the answer format, not a suggestion.
6. Stage 2 line 2.6 and every "known risk" statement: must carry a source id or "fetch"; the producer input must give ids for the risk list (it did not).
7. Checker rubric: keep lines 13 and 14; give the checker the risk-evidence list for line 12 (it worked: the B5 NO was correct).

## Appendix A — Second checker (Opus) verbatim

(see agent output recorded in the session log; scores per brief: B1 X 5/8 4/12 · Y 7/8 12/12; B2 X 3/8 3/12 · Y 7/8 9/12; B3 X 5/8 9/12 · Y 4/8 3/12; B4 X 3/8 4/12 · Y 6/8 8/12; B5 X 6/8 8/12 · Y 5/8 7/12; mapping as in `03-CHECKER-OUTPUT.md`. Full line-by-line text preserved below.)

### B1 — Plan X
A1 1 · A2 2 · A3 2 · A4 0 ("pool balance attestation" no source; asks for a cap already given; "Meta feed" widens the channel). B1 YES · B2 NO · B3 NO · B4 YES · B5 NO · B6 YES · B7 NO · B8 NO · B9 NO (voice after first plates and grip clip) · B10 NO · B11 NO · B12 YES. C1: voice provider; ending; whether the 16 photographs are used at all; crop anchors; route; music; brand mark on screen; casting; cost vs cap. C2: pool attestation; cap as open; "Meta feed"; "Reels UI band" rule unsourced.
### B1 — Plan Y
A1 2 · A2 2 · A3 2 · A4 1 ("cuminco.com" invented; embossed mark presumed). B1–B12 all YES. C1: exact durations pending voice; embossed mark; spoon; product name/URL inclusion; which voice; where the laugh two-shot sits; music; cost vs cap never mentioned. C2: cuminco.com; embossed mark as an existing asset.
### B2 — Plan X
A1 1 · A2 0 · A3 1 · A4 1 (RERA). B1 NO · B2 NO · B3 YES · B4 YES · B5 NO · B6 NO · B7 NO · B8 NO · B9 NO · B10 NO · B11 YES · B12 NO. C1: shot contents; who the people are; static layouts; WhatsApp still never mentioned; voice pace; which attempt is the deliverable; card animation; music; transcript-fail path. C2: RERA.
### B2 — Plan Y
A1 2 · A2 2 · A3 2 · A4 1 ("RERA details on request" still implies registration). B1 YES · B2 YES · B3 YES · B4 YES · B5 NO · B6 YES · B7 NO · B8 YES · B9 YES · B10 NO · B11 YES · B12 YES. C1: static layouts and WA still composition; shot look beyond golden hour/window; Veo vs Kling; legal line replace vs omit; voice provider; music; absolute durations. C2: "RERA details on request"; the structural assertions "brand early, home as hero, ask at close" unsourced.
### B3 — Plan X
A1 2 · A2 2 · A3 1 · A4 0 ("STANDARD 24 HOURS", "six hooks", "straight price for the first test pack" outside permitted facts). B1 NO · B2 NO · B3 YES · B4 YES · B5 YES · B6 YES · B7 NO · B8 YES · B9 YES · B10 YES · B11 YES · B12 YES. C1: presenter ruling; hosting; cap; script; tile-to-frame mapping; Hindi line; elapsed-time figure; two variants' content; music. C2: the three items above; "not Sarvam for a 48-s read"; Upwork rule correctly marked fetch.
### B3 — Plan Y
A1 1 · A2 1 · A3 2 · A4 0 ("Adwisely", "Standard delivery, twenty-four hours", "Order 09:00–19:00 IST, Mon–Sat", "Six hooks. Same afternoon.", "reference-person route 0/2"). B1 NO · B2 NO · B3 YES · B4 YES · B5 NO · B6 YES · B7 NO · B8 NO · B9 NO · B10 NO · B11 NO · B12 NO. C1: presenter ruling; script not frozen; phone footage matching; AI presenter voice; music; tiles for 12–38 s; the on-screen clock and elapsed time the brief demands (absent); Hindi flip verification; 55 s vs 60 s. C2: the five items above; the Upwork rule from an unfetched summary.
### B4 — Plan X
A1 1 · A2 1 · A3 1 · A4 0 ("Apni property, apne control mein" invented brand line; assumes real app footage obtainable). B1 NO · B2 NO · B3 YES · B4 YES · B5 YES · B6 YES · B7 NO · B8 NO · B9 NO · B10 NO · B11 NO · B12 NO. C1: VO at all and its text; who delivers the CTA; real screenshots/logo source; CTA wording; whether shots 8–10 stay generative; music; safe zones; order; Hinglish approval. C2: invented brand line; assumed assets; UI strings "Rent Collected ✅ / Autopay Active"; "RentOK" vs "RentOk".
### B4 — Plan Y
A1 2 · A2 2 · A3 1 (no durations, no written labels, no voice script) · A4 1 (placement rules asserted without source). B1 NO (app appears at F5–F6, only a corner mark in F1) · B2 YES · B3 YES · B4 YES · B5 YES · B6 YES · B7 NO · B8 NO · B9 YES · B10 NO · B11 YES · B12 YES. C1: durations; Hinglish labels; which ask; real screenshots vs mock UI; native vs VO; music; composited signage method. C2: the placement rules without source.
### B5 — Plan X
A1 2 · A2 2 · A3 1 (no durations, "[brand]", one spoken line) · A4 1 (effectiveness claims about creator content unsourced). B1 YES · B2 YES · B3 YES · B4 YES · B5 YES · B6 YES · B7 NO · B8 NO · B9 NO · B10 NO · B11 YES · B12 YES. C1: brand name; spoken lines; durations; native take vs VO; Hindi phrase; label design; music; end-text wording. C2: "no Sarvam"; "the one previously accepted presenter route"; the creator-content effectiveness claims.
### B5 — Plan Y
A1 1 (three attributes as "one reason"; "it calms my breakouts" edges into efficacy) · A2 1 · A3 2 · A4 1 ("it calms my breakouts"). B1 YES · B2 YES · B3 YES · B4 YES · B5 YES · B6 YES · B7 NO · B8 NO · B9 NO · B10 NO · B11 YES · B12 NO. C1: how identity is held across five shots (requirement without method); native vs dubbed and how lip sync is achieved; production order; any acceptance/verification step (absent); whether "calms my breakouts" survives; label asset; macro insert source. C2: "it calms my breakouts"; assumed synced lip movement and identical actress/wardrobe/lighting/bottle without a means.

## Appendix B — No-hindsight producer (Sonnet) verbatim

The two plans are reproduced in full inside `06-checker-input-v2-no-hindsight.md` under "Plan Z" (they were pasted there unchanged for the checker).

## Appendix C — Checker v2 (Sonnet) verbatim

### B4 — Plan Z
A1 2 · A2 1 · A3 2 · A4 1 ("Reels default muted" unsourced). B1 NO (frame 1 "no brand") · B2 NO (named ≤ 10 s, not ≤ 5 s) · B3 YES · B4 YES · B5 YES · B6 YES · B7 NO · B8 YES · B9 NO · B10 YES · B11 YES · B12 YES (hands/UI composite tested first) · B13 NO ("no invented statistic", "CTA explicit and singular" have no stated check) · B14 NO. C1: platform/spec; CTA action; deadline/cap/approver; brand assets; language mix; spelling. C2: "Reels default muted".
### B5 — Plan Z
A1 2 · A2 1 · A3 2 · A4 1 ("faces speaking is a known generative risk" unsourced). B1 YES · B2 NO (no brand name exists yet) · B3 YES · B4 YES · B5 YES · B6 YES · B7 NO · B8 NO (timings measured during assembly after capture) · B9 NO · B10 YES · B11 YES · B12 NO (the shot tested first, a product-only cutaway, contains no listed risk element) · B13 NO · B14 NO. C1: platform/spec; brand/pack approval; lead reason; casting source; language; CTA wording; deadline/cap/approver. C2: the generative-risk claim without source.
Tally: B4 A=6/8 B=8/14 · B5 A=6/8 B=7/14.
