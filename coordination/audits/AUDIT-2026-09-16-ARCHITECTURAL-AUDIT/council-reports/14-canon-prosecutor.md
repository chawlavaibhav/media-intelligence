# AGENT 14 — CANON PROSECUTOR (persona 76: devil's advocate FOR deleting Canon)

Brief: build the strongest evidence-based case that Canon (37 accepted sources, 1,300 SourceKnowledge objects, 291 bindings, ontology, 1,028 Q&A items, 2 compiled packs, trigger table, gate) was unnecessary for the product objective, and that a strong current LLM + a short expert checklist + direct tools would have produced the same or better outcomes at lower CpAO/TTAO. I do not issue the verdict. Section 4 steelmans the defence.

Inputs: wave-1 reports 04, 05, 06, 07, 08, 10, 11, 13a and LEAD-NOTES. Repo refs: MI `main @ 3bb9a3c` (verified `git rev-parse HEAD`), Cumin evidence `de1f978`, PR #103 `1de2b37`, case-001 branch `work/pilot-upwork-intro-video-v4` (`7629894` V1, `f6ca66f` head), case-002 branch `b4b77fa`, EVAL-037 lane branches `work/eval-037-*`. Read-only; nothing modified; no provider called.

Labels: OBSERVED (read/computed from committed bytes by me), OBSERVED-A<n> (read by agent n, not re-verified by me), INFERENCE, HYPOTHESIS, UNKNOWN.

---

## 0. Spot-check of load-bearing citations (12 checked; 11 held, 1 held-with-conflict)

| # | Claim leaned on | Where | Result |
|---|---|---|---|
| 1 | Cumin blueprint decided `cta: none in-frame`, `offer_placement: none`, `reviews: []`, `PA-D7: "pass — 'the bowl on a noodle night' sells at a glance"`, and CF2 "PASS on 9:16 (copy on empty wall, nothing over bowl/hands/faces)" | `de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/JOB.yaml` L48, L124, L173, L157, L326 | **HELD** (OBSERVED) |
| 2 | Canon lookup: 10 packs selected, 2 injected, 8 `missing_domains` incl. `commercial_communication`; prefix 5,298 tokens, 21 check ids | same file L113–116 | **HELD** |
| 3 | ABCD "Brand early, often, and richly" / "Introduce your brand or product from the start" exists in accepted Canon | `canon/knowledge/current/google-abcd-video-ads/source-knowledge.yaml @ 3bb9a3c` sk_abcd_0010 (~L663–667), sk_abcd_0011 (~L734–740) | **HELD** |
| 4 | The string "ABCD" first enters the job record only after the human's V2 complaint | `git log -S'ABCD' main..de1f978` → first hit `c0f849c` 2026-09-15 23:18 IST (17:48Z) | **HELD** |
| 5 | C-10: "The remaining eight packs are not compiled unless a real runtime failure demands one" | `coordination/CONTROL-STATE.md @ 3bb9a3c` L81, L95, L247 | **HELD** |
| 6 | `packs.py`: "a missing pack never blocks a job"; skill §4: "Do not compile, paraphrase or invent a pack for a missing domain. Proceed on the brief"; "Canon constrains; it does not direct" | `runtime/canon/packs.py` L10–11; `.claude/skills/media-agency/PRODUCTION-WORKFLOW.md` L118–119, L123 | **HELD** |
| 7 | PA-D7 is the only compiled advertising decision; carries markers `[REASONED-hedged|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|SINGLE-ORIGIN]`; gate marks it NOT-MECHANISED | `canon/compilation/PACK-product_appearance-v0.yaml` L486–515, L710–715; `de1f978:…/prompts/packages/clip-1.gate.txt` | **HELD** |
| 8 | EVAL-038: Sonnet NO_CANON took 18/18 top-3 slots; 0/6 for weak+packs | `eval/experiments/EVAL-038/RESULTS.md` L12–13, L24 | **HELD** |
| 9 | EVAL-037 conclusion "Canon helps, but the current retrieval / consumption system is not mature"; per-brief table = 2 leads / 2 ties / 2 NO_CANON leads; no committed judging/verdict/blinding files on any `eval-037-*` ref | `eval/experiments/EVAL-037/CONCLUSION.md` L45–66, L147; `coordination/decisions/CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md` L13; ref scan (only two `media-inputs/*-JUDGMENT.md` inputs exist, no outputs) | **HELD** |
| 10 | EVAL-037 spend floor USD 8.372931; Gemma FULL_CANON `canon_used` 0/18, Haiku 3/18, Sonnet CONTROLLED 18/18 at 2.5× the NO_CANON lane cost | recomputed from each lane's `runs/<lane>/result.json` on `work/eval-037-<lane>`: 1.138812 + 2.861148 + 0.412806 + 3.228778 + 0.331358 + 0.400029 = 8.372931 | **HELD** (reproduces agent 8 exactly) |
| 11 | Human V2 verdict verbatim "did cannon say nothing about product positioning? … it does not look like ad at all. the opening is missing too. canon had this knowledge. how's that possible?" | `1de2b37:production-learning/cases/CUMINCO-CHOPSTICKS-003/HUMAN-VERDICTS.yaml` L42–43 | **HELD** |
| 12 | EVAL-038 spend | `CONTROL-STATE.md` L116 says USD 2.260122; my recount of `eval/experiments/EVAL-038/runs/spend-ledger.jsonl`: reserve 3.9611 / settle 2.0881 / settle_ambiguous 0.672 (settled total 2.7601) | **HELD-WITH-CONFLICT** — three figures for one experiment; none is a vendor bill |

Additional citation I added and verified (the single most important one for this brief): the case-001 `CANON-BRIEF.md @ 7629894` (`pilots/upwork-intro-video-2026-09-14/preprod/`, 121 lines, 3,065 words) line 20: "`sk_abcd_0010, sk_abcd_0011, sk_ogx_0039 | Brand early and throughout; name within ten seconds; end on the package; attribution fails by default | Seller mark in the opening beat and the last frame`", line 18 "Open tight and in progress; no establishing wide", line 65 "on-screen CTA paired with spoken CTA (sk_abcd_0021); end on the package (sk_ogx_0039)". OBSERVED. This brief was committed in the same commit as V1 (`7629894`, 16:44 IST 14 Sep) — i.e. the knowledge was in the executor's context before V1 was built.

Visual check (OBSERVED, my eyes on `scratchpad/audit/agents/c003/media/qa_final-9x16-contact.png`, 24 frames at 1 s): plates are clean (no stray lettering anywhere), one window light camera-left throughout, glossy glaze / matte linen as declared, both characters identity-stable t=0–3 and t=18–23; the bowl is large in the macro beats t=4–17 (lower half of frame) but unbranded and unmarked; first brand mark appears at t=18 s as a small red "Cumin Co." wordmark; the opening t=0–3 is a wide two-shot with the bowls at table scale; no packshot/end card.

---

## 1. Charges

### Charge 1 — In three real productions, no Canon-derived decision is demonstrably the cause of an accepted outcome, and every rejection landed on a dimension Canon did not touch.

Evidence:
- OBSERVED: case 001 `PROMOTION-QUEUE.yaml @ 3bb9a3c` L84: "no new Canon need was proven by this pilot: the failures were creative architecture, orchestration, compositor correctness, audio route choice and QA timing". Case 002 `PROMOTION-QUEUE.yaml` L91–92: "NO_CANON_CHANGE … not missing Canon knowledge". Case 001 `HUMAN-VERDICTS.yaml`: zero occurrences of "canon" (grep count 0). The accepting/rejecting human never referred to Canon until the third job, and then only to say it had not appeared.
- OBSERVED: across the three cases, 3 of 46 defects that reached the human were media-model failures and 43 were pipeline/compositor/direction (agent 11 §1.4, from the three `SYSTEM-DEFECTS.yaml`); every fix that eliminated a defect class was a deterministic gate (`runtime/compositor/gates.py` etc.), none a Canon rule (agent 10 §1.4; agent 5 §4).
- OBSERVED: the case-001 executor's own list "Canon knowledge that materially changed decisions" (`f6ca66f:…/learning/PRODUCTION-MAP-AND-LEARNING.md` L49–57) names 14 sk_ ids. It is self-reported (K7), not tied to any verdict, and several items are things any competent brief does (no superlatives, disclose once, end on the package). The one item tied to a human rejection — `sk_ogx_0028 + sk_alb_c003_0005 (no caps, no reverse type over picture → supers on cream tabs)` — was applied in V4 *after* V3 was rejected for exactly that defect, although the same rule sat in `CANON-BRIEF.md` L52/L92/L118 before V1. The knowledge did not prevent the failure; it was cited afterwards as the rationale for the fix the human had demanded.
- INFERENCE: the eight-state chain reaches "changed a decision" (state 5) only for prompt vocabulary (lighting/finish/no-text) and reaches "decision correct / survived / QA detected" for nothing the human judged.

Strongest single citation: `production-learning/cases/UPWORK-INTRO-001/PROMOTION-QUEUE.yaml @ 3bb9a3c` L84.

### Charge 2 — Where Canon was fully in the loop (Cumin), it produced false assurance rather than direction: 21 check lines, 20 self-marked "pass", and the human rejected on the one line that was a commercial judgment.

Evidence:
- OBSERVED: `JOB.yaml @ de1f978` L150–174: PA-D1…D10 and CA-D1…D11 all `pass` except CA-D4 `n-a`; `deviations: []`; `reviews: []`. PA-D7 "pass — … the hero image needs no copy" on a film with no product hero, no brand before t=18 s, no end card (visual check above). CA-D2 "the upper third stays clear for text" and CA-D1 "text lands after the action settles" — the human's V1 verdict was "the text is coming on figures" (INFERENCE: at least three of the twenty passes were contradicted by the first human look).
- OBSERVED: the pre-dispatch gate (`clip-1.gate.txt`) reports "11 doctrine check lines NOT mechanised … This establishes structure over the prompt/artifact bytes — not doctrine satisfaction, quality, outcomes, or adoption." The gate says of itself that it does not test what the human rejects on.
- OBSERVED-A6/A10: PA-D7 is `NOT_MECHANISED` in both gates; the only compiled advertising decision cites 1926 print doctrine (sk_hop_sa_0026/0035) with a `MEDIUM-UNTESTED` marker.
- INFERENCE: a compiled `commercial_communication` pack consumed the same way would have added a 22nd self-marked pass (agents 4 and 6 reach the same hypothesis independently). The external literature agrees that same-model self-critique without an external signal does not correct (agent 13a E1–E4).

Strongest single citation: `de1f978:…/JOB.yaml` L157 next to `HUMAN-VERDICTS.yaml @ 1de2b37` L42–43.

### Charge 3 — The Cumin "Canon gap" is not a knowledge gap: the missing rule is in every frontier model's prior, was hand-delivered to the previous job, and was policy-forbidden from being paraphrased.

Evidence:
- OBSERVED: `CANON-BRIEF.md @ 7629894` L18/L20/L65 carried "open tight … no establishing wide", "Seller mark in the opening beat and the last frame", "end on the package", "on-screen CTA paired with spoken CTA" — by id — into case 001. Case 001's opening was then rejected twice ("opening not visually exceptional enough" V1; "opening still not strong enough" V2, `HUMAN-VERDICTS.yaml` L19/L31). Knowledge in context (state 3) did not yield an accepted opening.
- OBSERVED: `PRODUCTION-WORKFLOW.md` L118–119 forbids paraphrasing an uncompiled domain; C-10 forbids compiling it; `packs.py` continues silently on the gap. The cheapest possible fix — one sentence: "an ad opens on the product and ends on a packshot with a CTA" — was the one thing the programme's rules prohibited the operator from writing down.
- OBSERVED: skill creative guidance is one sentence in `SKILL.md` L12–13 ("A technically perfect picture can still be a bad ad; you own the advertising craft") plus the §5 field table; agent 4 counts creative content at ≈ 4.6 % of the 8,035-word skill.
- INFERENCE: the operator (a frontier LLM) does not need 4,096 tokens of compiled Hopkins/ABCD to know an ad has a hero, an opening and a CTA; it needed to be *asked* the question before the deck was frozen, and nobody (human or skill) asked. The human approved five strings and a spend cap at 13:28Z (K14).

Strongest single citation: `7629894:pilots/upwork-intro-video-2026-09-14/preprod/CANON-BRIEF.md` L20 alongside `production-learning/cases/UPWORK-INTRO-001/HUMAN-VERDICTS.yaml` L19, L31.

### Charge 4 — Canon's only controlled tests are one clean negative, one unjudged tie, and one never-run design; no experiment ever compared strong+Canon vs strong-alone on media a human accepts.

Evidence:
- OBSERVED: EVAL-038 `RESULTS.md` L12–13: Sonnet NO_CANON 18/18 top-3; 0/6 under the pre-registered rule. Weak+packs also cost more per package (USD 0.072 vs 0.063, OBSERVED-A8).
- OBSERVED: EVAL-037 `CONCLUSION.md` table: CONTROLLED_CANON leads B01, B06; ties B02, B05; NO_CANON leads B03, B04 — at 2.5× the token cost (2.861148 vs 1.138812, recomputed). No judging files, verdicts or blinding key are committed on any of the 12 `eval-037-*` refs; package line 98 of the Canon-condition packages self-discloses treatment (OBSERVED-A8). The Controller's decision text (`CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md` L13–15) records "Canon helps" and then stops discovery — a preference recorded as a conclusion.
- OBSERVED: `canon/experiments/v1/value-gate/PROTOCOL.md` L4: "PACKAGE ONLY. NOT EXECUTED. 0 of 24 planning outputs generated." The one design that isolates Canon from length-matched generic craft (`FRESH_CONTROL_SESSION_REQUIRED`) never ran. `CONTROL-STATE.md` L85 calls CANON-012 "merged and closed".
- OBSERVED: `PROPOSED-EVAL-038-CONCLUSION.md` L18–21: "the treatment packages lost on creative substance — thin copy, no dialogue … The packs made weak models disciplined. They did not make them good."
- INFERENCE: after ≈ USD 10.6–12.3 and two experiments, the programme holds exactly one decision-grade number about Canon, and it is negative.

Strongest single citation: `eval/experiments/EVAL-038/RESULTS.md` L12–13.

### Charge 5 — The programme built a library, not a tool: 92 % of Canon is unreachable by any production path by design, and the reachable 8 % is the lowest-demand slice.

Evidence (OBSERVED-A6 unless marked):
- 104/1,300 SK objects (8.0 %), 44.6 KB / 7.07 MB (0.63 %), 10/37 sources, 11/56 domains reachable via the two compiled packs. `commercial_communication` (15 sources, 555 SK, demanded by 53/54 briefs in Canon's own priority doc) is uncompiled; the two compiled packs are demanded by 15/54.
- Bindings: 291, 266 `proposed`, 249 with no `target_path`, none reviewed since 28 Aug (the 28-Aug review's 127/89 reproduces at `e6474dc`). Ontology: 0/422 relationships cross a source. `canon/context/**`: no code consumer. Q&A: consumed by nothing (`runtime/tests/test_canon_lookup.py` L66–69 asserts `canon/qa/` is absent from the payload — OBSERVED by me); four contracts forbid it; validator on main reports 26 errors against a manifest that says 0 (OBSERVED-A7).
- OBSERVED (me): `canon/knowledge/current/**` = 1,292,342 words; `canon/**/*.md` = 384,591 words; findings/candidates/experiments/research markdown = 256,803 words; the two packs that reach an operator = 8,854 words. Ratio corpus : operator-reaching ≈ 146 : 1.
- OBSERVED (me): the gate cannot even load a third pack without a code change (`doctrine.py EXPECTED_DECISIONS` hard-codes the two — OBSERVED-A6).

Strongest single citation: `runtime/tests/test_canon_lookup.py @ 3bb9a3c` L66–69 (the runtime is tested to *exclude* most of Canon) together with `de1f978:…/JOB.yaml` L113–115.

### Charge 6 — Two of the six Cumin failures have no Canon knowledge at all, and the fixes for all six were gates or a question, never a book.

Evidence: OBSERVED-A6 regex over all 1,300 SK and 1,191 terms: 0 hits for text-over-subject obstruction; 0 hits for voice casting/register; audio modality has zero sources (`modality_base_packs.audio: []`). The remedies that actually landed: `check_vo_schedule` (35 lines, PR #103), `wall_obstruction()` (job tool), `AD_STRUCTURE_MINIMUM` (blueprint fields shown to the human). OBSERVED (me): case 003 `PROMOTION-QUEUE.yaml @ 1de2b37` L66–70 files the Canon item as "report only".
INFERENCE: even the ad-structure remedy the project proposes is a checklist question, not a compiled pack — the project's own fix for the "Canon gap" does not use Canon.

Strongest single citation: agent 6 §4 table (regex, 0 hits) — not re-run by me; OBSERVED-A6.

### Charge 7 — The compiled-pack form was designed for a weak model that never used it and is consumed by a strong model as boxes to tick.

Evidence:
- OBSERVED (me): Gemma FULL_CANON `canon_used` 0/18; Haiku 3/18; Sonnet CONTROLLED 18/18 only because the lane forced it. The pack contract (`INJECTION-CONTRACT-v0.md`, questions-with-defaults + CHECK) was shaped by EVAL-037's weak-model failure (`packs.py` L10 "that produced EVAL-037's 0/18").
- OBSERVED-A6: the documented operator path prints only `decision_id | question` + `CHECK` (4,520 chars); the 6,185 chars of DEFAULT text and 28 conflict rules are never printed by any BOOTSTRAP/WORKFLOW command. Whether the operator opened the YAML is unrecorded.
- OBSERVED-A13a: no published study shows declarative doctrine in a prefix changing downstream decisions; the measured effects come from binary instance-level questions answered by something other than the author (TICK, CoVe, RLCF) — and IFScale shows adherence decays with instruction count with early-item bias. Twenty-one imperative check lines plus 28 conflict rules is the shape the literature predicts will be ticked, not obeyed.

Strongest single citation: `runtime/canon/packs.py @ 3bb9a3c` L10–11 plus lane `result.json` `canon_used` counts.

### Charge 8 — The Canon governance loop is self-sealing: the rule that gates compilation is the failure it waits for, and the first real failure produced another "report", not knowledge in a job.

Evidence: OBSERVED: C-10 (`CONTROL-STATE.md` L81/L95/L247) → skill §4 "record the gap only if the production actually fails for want of it" → Cumin fails → `LEARNING-PACKET.yaml` records the gap → PR #103 "Controller decision under C-10" → no decision as of `1de2b37`. OBSERVED (me): 20 Controller decision records are named for Canon/EVAL-037/038/admission (13,593 words); 65 of 117 decision bodies mention Canon. INFERENCE: the programme's Canon throughput is decisions about Canon, not Canon in jobs.

Strongest single citation: `coordination/CONTROL-STATE.md @ 3bb9a3c` L81 and `1de2b37:production-learning/cases/CUMINCO-CHOPSTICKS-003/PROMOTION-QUEUE.yaml` L66–70.

### Charge 9 — The cost was real and measurable; the value is not.

See §3. Summary: 164 non-merge commits (18 % of 899) on 15 of 23 days, 56 of the repo's 135 commit-hour buckets (41 % of all hours in which anything was committed had a Canon commit), 345,441 lines inserted under `canon/`+`runtime/canon/`, 77 Canon/EVAL-037/038 branches, 30.4 MB tracked, 5,320 lines of Canon code, ≈ USD 10.6–12.3 of provider spend, 1.29 M words of knowledge — against zero accepted outcomes attributable to Canon and one job rejected while the human asked where Canon was.

---

## 2. The counterfactual: strong LLM, no Canon, short expert checklist, direct tools

Method: for each brief I write the professional completion a current frontier model produces from the verbatim brief plus a ~40-line ad-craft checklist (the kind the 28-Aug review proposed as arm B′), then mark each actual human rejection AVOIDED / SAME / PARTIAL. I am the model in question; that is a limitation (INFERENCE throughout, HYPOTHESIS where the claim is about production behaviour I cannot observe).

### 2.1 Cumin Co. chopsticks (brief verbatim `de1f978:…/JOB.yaml brief.verbatim`)

Baseline completion (INFERENCE — what a strong LLM writes unprompted when asked "turn this into an ad"):

- **What it sells**: the Cumin Co. 15 cm Ceramic Ramen Bowl (the blog's product); proposition "noodle night at home, done properly"; the chopstick lesson is the *device*, the bowl is the *hero*.
- **Structure (18 s, 9:16)**: 0–2 s close-up hook: chopsticks drop into the bowl's rim notch, steam, brand mark on from frame 1. 2–12 s three macro beats (her hand teaches, his fails), bowl filling the lower half, 3–5-word supers on the wall. 12–15 s payoff: he grabs the spoon parked in the notch, both laugh. 15–18 s packshot end card from the brand's own photograph, product name, "Cumin Co.", "cuminco.com"; VO says the brand name.
- **Voice**: one calm Indian-English female narrator; cast by ear on the *longest line at final pace* before any picture is drawn; picture cut to the measured VO.
- **Text**: supers never over hands/bowl/faces; 4:5 and 1:1 re-framed, not cropped.
- **Muted test**: brand and product readable in the first and last 2 s without sound.
- **Questions to the customer** (before freezing anything): which product is the hero; may the embossed mark appear; spoon vs chopsticks ending; on-camera speech or VO; Hindi; spend cap.

Against the seven human rejection items (HD-01…07 @ `1de2b37`):

| Human rejection | Baseline | Why |
|---|---|---|
| HD-06 "does not look like an ad at all" | **AVOIDED** | the completion opens on the product, brands from frame 1, ends on a packshot — the operator's blueprint said `cta: none in-frame` and no brand before beat 5 (OBSERVED L48, L127) |
| HD-05 "the opening is missing" | **AVOIDED at plan level**, PARTIAL at pixels | the plan says close-up hook; whether Veo delivers a usable first second is a draw question (V1's clip-1 window was chosen by excluding defects) |
| HD-04 closing shot / end card | **AVOIDED** | end card from the brand photo is in the baseline plan; the operator added it only in V3 after the human asked |
| HD-03 text on figures | **SAME** | a plan clause ("never over hands") does not enforce itself; without an obstruction gate the compositor produces the same defect (case 002 HD-03/05/07 had the same clause in Canon and shipped it) |
| HD-01 "random audio" (silenceremove inside lines) | **SAME** | engineering |
| HD-02 lips moving under VO | **PARTIAL** | the baseline's "closed mouths, nobody speaks" prompt clause is standard i2v craft (case 001 RO-01 / 002 RO-02 already recorded it); a strong LLM adds it reflexively, but Veo may still animate mouths |
| HD-07 voices overlapping | **PARTIAL** | "VO first, cut to measured durations" is in the baseline plan; but without `check_vo_schedule` a hand-set timeline can still overlap — the baseline avoids the *cause* (timeline before VO), not the *class* |
| Voice: 5 rounds / 26 takes | **PARTIAL** | the baseline still auditions; but it would not spend 8 takes on ElevenLabs Western voices (RO-05 and MFH row both said no Indian voice) nor 8 on Sarvam raw reads (RO-05); it would start with 2–3 candidates on the longest line |

Honest scoring: 3 avoided (all three are the V2 structural rejections — the ones the human explicitly attributed to Canon), 2 same (engineering), 3 partial. The baseline would still have produced a V1 with audio and text-placement defects; it would not have produced a tutorial with no brand and no close.

What Canon actually contributed (OBSERVED from plates/frames): declared finishes, one window source, no lettering, hold lengths — all held. What a baseline writes for the same plates: "one soft window light from camera-left, glossy glaze, matte linen, no text, no logos" — the same sentence. HYPOTHESIS: the plate quality is not distinguishable between arms; an ablation (same prompts minus the PA-D vocabulary) is the only way to know.

### 2.2 Upwork intro film (brief: `UP/PROFILE.md` v2 paragraph + owner instruction "fully AI-made, a character speaking to camera, crazy good because it IS the demo")

Baseline completion (INFERENCE): 60 s, 16:9; open on a finished ad full-screen within 3 s while the first sentence is spoken; AI presenter disclosed once, bookends only, ≤ 20 s total; body = brief arrives → words approved → ad builds → four sizes → six hooks + Hindi flip → the QA catch (a wrong digit fixed on screen) → clips in motion → close with the two windows (24 h / 4 h) and an end card; every proof ≥ 3 s full-frame; supers word-identical to speech, never over the work; contrast ≥ 4.5:1 on panels, not over photos; one voice source; presenter anchored on one still, no extend chains; end on the offer card. Questions: face or no face (conflicts with the live "not on the menu" line), brand spoken/shown, hosting, may the film's own ads be generated.

Against the human rejections (HUMAN-VERDICTS @ 3bb9a3c):

| Human rejection | Baseline | Why |
|---|---|---|
| V1 proof too small / phone-mockup framing / opening not exceptional / presenter blocks too long | **PARTIAL** | the baseline's "proof full-frame ≥ 3 s, presenter ≤ 20 s" avoids two; "opening not exceptional" is taste the Controller articulated only after seeing V1 and V2 — SAME |
| V2 "images AND videos co-equal … work owns the majority of screen time" | **SAME** | this was a strategic correction supplied by the human; neither Canon nor a baseline had it (CANON-BRIEF L104 lists it under "Canon knowledge missing") |
| V3 text cut off / contrast lost / crops / card geometry | **SAME** | compositor engineering; Canon had the 4.5:1 rule in context (CANON-BRIEF L52) and it was drawn over the dal anyway (agent 5 §1.3e); a baseline plan says the same thing and is equally unenforced without gates |
| V3 voice horribly robotic (Sarvam 48 s) | **AVOIDED (likely)** | a baseline reads the MFH prior ("raw TTS sounds robotic without speech-rhythm rewrite") if given it, or simply auditions a long read before assembling; the pilot chose Sarvam on a 6/6 Lab cell over ≤ 70-char lines and disclaimed the prior (`ROUTE-ANALYSIS.md` "none is relied on") — a routing-policy failure, not knowledge |
| V3 presenter missing → hard requirement | **SAME** | the human reversed himself (V1/V2 had one; V3 removed it; V4 required it) |
| V4 offer/code collision, "can't suck" lost, bubble persisted | **SAME** | assembly |

Honest scoring: 1 avoided, 2 partial, the rest same. Canon is cited in no verdict; the accepted V4.1 is the Controller's V2/V3 corrections executed with gates written after V3. The 22.7 KB CANON-BRIEF and the 22 Canon citations in `CREATIVE-BLUEPRINT-V4.md` (OBSERVED, L35–85) are decoration on a film whose shape the human dictated. INFERENCE: on this job Canon is neutral; TTAO (7 h 54 m) was driven by three architectures and five full assemblies, which a storyboard-level human gate (not Canon) would have shortened.

### 2.3 Portfolio tile 03 — Kora (`production-learning/cases/UPWORK-PORTFOLIO-002/HUMAN-VERDICTS.yaml` HD-03, HD-04)

Rejections: "headline placed over the figure/garment once the 16:9 poster is cropped" and "cream type over the beige wall: hard to read, unfinished". Fix (`662fba4`): square/vertical formats put the picture over a solid oxblood panel; 16:9 editorial split.

Baseline completion (INFERENCE): a four-size set is four compositions, not one crop — picture in a panel, type on a solid panel, headline never crossing the figure; contrast 4.5:1 minimum; cream-on-beige fails by inspection; re-validate each export. This is exactly the fix that shipped nine hours later.

Against the rejections: **AVOIDED at plan level** (the baseline would not have exported a cropped 16:9 poster as a 1:1), **SAME at execution risk** — case 002 had no plan at all (PD-01) and imported none of the same-branch gates; a baseline with the same `compose_v4.py cover()` default and no gate could produce the same tile if it skipped its own plan. The point for the prosecution: Canon *had* this knowledge (`sk_ogx_0028`, `sk_sam_c003_0021`, in `CANON-BRIEF.md` L52, L92) in the previous day's context and it made no difference, because nothing turned it into a gate. Whether the rule comes from Ogilvy or from a frontier prior is irrelevant to whether it is enforced.

### 2.4 Where the no-Canon baseline would have made the same mistakes (stated plainly)

All engineering/measurement failures: text over figures at the pixel level, VO overlap, audio mix, mouths under VO, clipped text, lost contrast at pixels, crop defaults, attempt-id collision, pool exhaustion. All human-taste reversals: "not extraordinary", presenter in/out, "co-equal". None of these is a knowledge failure and none is where Canon could have helped; the prosecution does not claim the baseline is better here, only that Canon was not better either.

---

## 3. Cost accounting of the Canon programme vs demonstrated production value

### 3.1 Costs (OBSERVED unless marked; commands in the working notes above)

| Item | Value | Method |
|---|---|---|
| Non-merge commits touching `canon/`, `runtime/canon/`, EVAL-037, EVAL-038 | **164** of 899 (18 %) | `git rev-list --count --no-merges HEAD -- <paths>` |
| Calendar days with such commits | **15** of 23 (24 Aug – 14 Sep) | `git log --format=%ad --date=short … | sort -u` |
| Distinct commit-hour buckets with a Canon commit | **56** of the repo's 135 (41 %) | `--date=format:'%Y-%m-%d %H' | sort -u` (proxy for sessions; overlaps other work) |
| Lines inserted / deleted under `canon/` + `runtime/canon/` | **+345,441 / −7,131** | `git log --no-merges --shortstat` |
| Tracked bytes under `canon/` | **30.4 MB** (12.7 MB YAML) | `git ls-files -z canon | xargs -0 stat` |
| Words: `canon/knowledge/current/**` | **1,292,342** | `wc -w` |
| Words: `canon/**/*.md` | **384,591** | `wc -w` |
| Words: findings + candidates + experiments + research markdown | **256,803** | `wc -w` |
| Words: Q&A corpus (q+a+support) | ≈ 222,000 (OBSERVED-A7) | |
| Words that reach an operator (2 packs) | **8,854** | `wc -w canon/compilation/PACK-*` |
| Canon code (runtime/canon, canon/gate, compilation tool) | **5,320 lines** | `wc -l` |
| Controller decision records named CANON / EVAL-037 / EVAL-038 / REP-07 / admission | **20** of 117; **13,593** of 77,131 words (18 %) | `ls`, `wc -w` |
| Decision bodies mentioning Canon | **65** of 117 | `grep -l -i canon` |
| Branches (local + remote) named canon / eval-037 / eval-038 | **77** | `git branch -a | grep -c` |
| Provider USD, EVAL-037 (floor; Gemma unpriced) | **8.372931** | six lane `result.json` (recomputed) |
| Provider USD, EVAL-038 | **2.260122** (record) / 2.7601 settled / 3.9611 reserved (my recount) | conflict reported |
| Provider USD, CANON-001…014, CANON-GATE-001, value gate | **0** recorded (value gate never executed) | `PROTOCOL.md` L4 |
| **Direct Canon provider spend** | **≈ USD 10.6–12.3** (≈ 7–8 % of the programme's ≈ USD 155 provider total) | |
| LLM/session cost of extraction (1,300 SK, 1,028 Q&A written by Claude lanes in ~5 h on 30 Aug), compilation, bindings, ontology | **UNKNOWN** (subscription-metered; not recorded) | agent 7 §0 |
| Operator overhead per job attributable to Canon | 5,298 tokens prefix + reading CANON-SHAPE §4–5 (9.5 KB) + trigger table (9.8 KB) + the BOOTSTRAP print (4.5 KB) + rendering 21 check lines + 10 gate runs | `JOB.yaml` L116; BOOTSTRAP §2 |

The dollar cost is small. The cost that matters is that the Canon stream owned ~18 % of commits, ~18 % of decision prose and — by Canon's own inventory — produced 1.29 M words of knowledge of which 8.9 k words can reach a job. INFERENCE: this is the "process mass" the 28-Aug reviews warned about, concentrated in one workstream.

### 3.2 Demonstrated production value

Which Canon-derived decision demonstrably changed an outcome for the better in the three jobs?

| Candidate | State reached | Verdict |
|---|---|---|
| Cumin plate prompts carry PA-D1/PA-D4 vocabulary ("one soft window light camera-left", "glaze glossy … linen matte") and the pack-limit no-text clause ("No text, no lettering, no logos, no printed matter") — `de1f978:…/prompts/packages/plate-A.package.md` L24–25, L37, L52, L59 | exists → retrieved → in context → understood → changed the prompt → plates accepted (H2/H3/B first draw; A on r2 for a product-fidelity reason unrelated to Canon) → survived to V3 → no human complaint on lighting/lettering | **The only chain that reaches state 7.** But (a) the no-text clause is co-owned by the Lab's mechanism B (RR-6, IMG-TEXT, `SKILL.md` "exact text composed by code") and by `QA-CHECKLIST` B1, so it is not uniquely Canon; (b) "one window light, no text" is baseline prompt craft; (c) no ablation exists. OBSERVED that it held; UNKNOWN whether Canon caused it. |
| Case 001 `PRODUCTION-MAP §4` 14 sk_ ids "materially changed decisions" | self-reported; not tied to any verdict; one (sk_ogx_0028) applied only after the human rejected V3 for the defect it names | **Not demonstrated** (K7) |
| Case 001 CANON-BRIEF "open tight, seller mark in the opening beat, end on the package" | in context before V1; opening rejected V1 and V2 | **Negative**: knowledge in context, decision not changed |
| Cumin PA-D7 | in context, "pass", human rejected on that dimension | **Negative** |
| Cumin CA-D10 hold lengths (≥ 3.3 s) | carried from case 001 template, not from Canon (`evidence_scope: this_accepted_template`) | not Canon |
| Cumin product fidelity (DF-01 embossed mark caught at plate-A r1) | `QA-CHECKLIST` B2 cites `PROFILE.md delivery checklist 1–3`, not a pack | not Canon |
| EVAL-038 B06 image: haiku+packs beat sonnet-no-canon after reveal | n = 1 pair, 1 reviewer who revised post-reveal; the replay of the same prompts was worse than all four originals (draw variance) | **Not decision-grade** |

Check ids self-marked pass in Cumin (OBSERVED, `JOB.yaml` L150–174): PA-D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, CA-D1, D2, D3, D5, D6, D7, D8, D9, D10, D11 = 20 pass; CA-D4 n-a. Contradicted by the first human look: PA-D7 (directly), CA-D1 and CA-D2 (INFERENCE via "text is coming on figures"). Mechanised by the gate: 9 partial literal-clause tests; 11 NOT-MECHANISED (gate.txt). Independent review of any line: none (`reviews: []`; the personas named in workflow §5 do not exist — OBSERVED-A4).

### 3.3 The ledger in one line

INFERENCE: ~18 % of a 23-day programme's commits and decisions, 1.29 M words, five and a half thousand lines of code and ≈ USD 11 bought: two packs whose lighting vocabulary held on one job's plates (cause unproven), one negative experiment, one unjudged tie, one unrun design, and a rejected job in which the human asked why the knowledge he had paid for was absent.

---

## 4. The best evidence against this case (steelman), and what would refute me

### 4.1 Strongest points for the defence

1. **EVAL-037 is not a loss.** OBSERVED: Sonnet CONTROLLED_CANON led two briefs (B01 RentOK video, B06 watch image) and tied two; NO_CANON led two. On a per-brief reading that is 4/6 ≥ for Canon. The judging was described as four independent blind streams; the absence of committed verdict files is a provenance gap, not proof the judging did not happen. Rebuttal: uncommitted, treatment self-disclosed in the packages, 53 % HOLD material consumed, 2.5× cost for a tie; agent 8's verdict "inconclusive on value" stands, but "inconclusive" is not "negative".
2. **EVAL-038 answered a different question.** It tested *substitution* (weak + 2 packs vs strong alone), and refuted it. It never ran strong + packs vs strong alone — the cell that would test the prosecution's own claim (agent 10 §6.1). The prosecution's headline number does not measure the thing the prosecution asserts.
3. **Where Canon was injected, it held.** OBSERVED (my visual check): the Cumin plates are clean, lit consistently, unlettered, identity-stable across 24 frames and three versions. The two injected domains (lighting, composition) drew zero human complaints across three versions; the eight uninjected domains include the one that failed. The pattern "injected → fine, uninjected → rejected" is at least as consistent with "compile the rest" as with "delete it".
4. **The retro-test shows the compiled checks bite where they apply.** OBSERVED: `canon/findings/EVAL-038-RETRO-TEST-PILOT-001.md` L29–59: both rejected PILOT-001 candidates fail PA-D7 outright ("nothing in frame sells anything"; "the sale lives entirely in the later text overlays"), and PA-D1/PA-D4/CA-D1/CA-D2 would have forced fixes before dispatch. A heroless plate is exactly the class of failure a frontier model produced unprompted; the check catches it *when answered honestly*.
5. **The human wants it.** OBSERVED: the V3 rejection ends "we need to do the diagnosis now. tranfer the info to canon". The product owner's stated remedy is more Canon, not less; a prosecution that deletes what the customer asked for must show the customer is wrong about his own product.
6. **Provenance and Indian context are not in a frontier prior.** OBSERVED-A7: Bijapurkar, Pandey, Parameswaran, Jain, Desai, Dwyer-Patel are accepted sources with ids and locators; a frontier model's recall of Indian advertising practice is thin and uncitable. Canon gives a stable house doctrine that survives model swaps (agent 13a C1.12 Memp: procedural memory migrates to weaker models) and can be audited when a client asks "why".
7. **n = 3, one unblinded judge who authored the briefs.** Nothing in production learning can prove Canon useless any more than useful (agent 10 §6.1). The 28-Aug head review said the value is "an open empirical question"; the honest state after three jobs is *still open*, not *closed against*.
8. **The cheap parts of Canon are cheap.** Direct spend ≈ USD 11; the packs are 8.9 k words; the per-job prefix is 5.3 k tokens. Deleting Canon saves little money; the expensive parts (extraction sessions) are sunk.

### 4.2 What would refute the prosecution

- E1/E3 from agent 10 §6.2 run honestly: on the 6 EVAL-037 + 3 real briefs, strong model + oracle compiled Canon (≤ 2.5 k tokens) beats strong model + a 40-line rejection-derived checklist under two blind non-author reviewers by unanimity, on the fraction of the ~25 known human rejection reasons pre-empted. If Canon-oracle > checklist by a margin the reviewers agree on, Charge 3 and Charge 7 fall.
- A real job in which a Canon check line rendered by a *non-author* (or mechanised) blocked a defect the human would have rejected, before spend. One instance would move Canon from state 5 to state 8 for the first time.
- An ablation of the Cumin plates: same prompts minus PA-D vocabulary and the no-text clause, judged blind by the same human. If lighting/lettering defects appear, §3.2 row 1 becomes demonstrated value.
- A compiled `commercial_communication` pack consumed under an independent reviewer that changes a V1 blueprint (product hero, opening, CTA) on a job where the operator's first draft lacked them. That would show the pack form can direct, not only constrain.
- Evidence that the Indian-context sources changed a decision a frontier prior got wrong (e.g. a Hindi copy register, a festival cue) and the human accepted it.

---

## 5. What I would preserve even under prosecution

| Keep | Evidence it earned its place | Form to keep it in |
|---|---|---|
| The pack-limit clause "never generate Devanagari glyphs; composite text deterministically" and its production form "No text, no lettering, no logos, no printed matter anywhere in the image" | OBSERVED: zero exact-text defects and zero stray-lettering defects across three cases (`LIMIT-TEXT` PASS ×10 in Cumin; Cumin frames clean on my visual check; agent 11 §2.4) | as a hard prompt-template line + the existing LIMIT-TEXT gate; co-owned with the Lab's mechanism B — keep regardless of Canon's fate |
| PA-D1 / PA-D2 / PA-D4 / PA-D5 lighting-and-finish vocabulary (declared finish per object; one nameable source; grayscale separation) | OBSERVED: Cumin plates lit consistently, identity stable, no relight needed across V1–V3; the retro-test shows the same lines would have forced fixes on PILOT-001's atmospheric prompts | as four typed prompt fields (`surface_finish_per_key_object`, `implied_light_source`, …) — the job record already carries them; drop the pack wrapper and markers |
| CA-D1 / CA-D2 "name the 1st/2nd/3rd read; state the placement zone" | OBSERVED: rendered in every Cumin package; the attention-order field is a good forcing question even though the self-answers were wrong | as two blueprint questions answered *before the human sees the blueprint* |
| The ≈ 15 production-shaped ABCD/Ogilvy items (sk_abcd_0005–0007, 0010–0013, 0019–0021, 0026; sk_ogx_0026/0027/0039/0073; Q&A `qa_abcd_0010`, `qa_abcd_0011`, `qa_abcd_0019`) | OBSERVED-A7: `qa_abcd_0010` describes the Cumin V2 structure almost verbatim and gives the three misses; these are the only Cumin-shaped items in 1,028 | as a **≤ 12-line ad-structure pause-point checklist** (hero named; brand by beat 1; opening on product or problem; CTA present; end on the product; super = VO) answered by a non-author before the deck freezes — i.e. the project's own `AD_STRUCTURE_MINIMUM`, made unconditional |
| WCAG numbers (sk_wcag_0001/0021: 4.5:1, 3:1 large) | already constants in `runtime/compositor/gates.py check_contrast` | keep in code; the source citation is a comment |
| Provenance discipline (ids, locators, `support`, `confounders`) and the Audit Gate record format | it made this audit possible; the 28-Aug figures reproduced exactly at `e6474dc` | as a library convention, not a runtime dependency |
| The Indian-context sources as *reading* | UNKNOWN value; plausibly the only content a frontier prior lacks | keep the extractions on disk; no runtime path until a job demonstrates need |

What I would delete or freeze (not a recommendation to the lead — the prosecution's proposed remedy): the runtime injection path (`packs.py` payload, prefix, trigger table as a *mechanism*), the 291 bindings, the ontology, `canon/context/**`, the Q&A corpus as a runtime asset, the 21-line check-rendering ritual and its gate, and C-10's compile-on-failure rule. Replace with the checklist above, an independent reviewer for the blueprint, and the deterministic gates that already exist.

---

## Findings ranked

1. **No Canon-derived decision demonstrably caused an accepted outcome in three jobs; every rejection landed where Canon was absent or self-marked.** OBSERVED (`PROMOTION-QUEUE` 001 L84, 002 L91–92; Cumin `JOB.yaml` L157 vs `HUMAN-VERDICTS` L42–43).
2. **The same ABCD knowledge Cumin lacked was in case 001's context by id (CANON-BRIEF L18/L20/L65) and the opening was rejected twice.** Knowledge in context ≠ decision changed. OBSERVED.
3. **The only controlled evidence is one clean negative (EVAL-038 0/6, 18/18), one unjudged tie at 2.5× cost (EVAL-037), and one unrun design (value gate, 0/24).** No experiment compared strong+Canon vs strong-alone on accepted media. OBSERVED.
4. **92 % of Canon is unreachable by design; the runtime is unit-tested to exclude the Q&A corpus; the compiled 8 % is Canon's own lowest-demand slice.** OBSERVED / OBSERVED-A6.
5. **Canon's cost is ~18 % of commits and decision prose, 1.29 M words, 345 k inserted lines, ≈ USD 11; its per-job footprint is a 5.3 k-token prefix plus a 21-line self-attestation ritual.** OBSERVED.
6. **The policy loop was self-sealing** (C-10 → skill §4 "do not paraphrase" → gap recorded after human rejection → "report only"). OBSERVED.
7. **What held (lighting/finish/no-text prompt lines) is co-owned by the Lab and by baseline craft; no ablation exists.** OBSERVED that it held; UNKNOWN that Canon caused it.
8. **The defence's best exhibits are real:** injected domains drew no complaints; the retro-test shows PA-D7 bites when answered honestly; EVAL-037 per-brief 4/6 ≥; the owner asked for more Canon. None reaches decision grade.

## Open questions / unknowns

- UNKNOWN: whether the Cumin operator opened `PACK-*.yaml` DEFAULT text or only the BOOTSTRAP print; not recorded.
- UNKNOWN: EVAL-037 judging — who, where, how blinded; the conclusion rests on uncommitted verdicts.
- UNKNOWN: LLM/session cost of the Canon extraction, compilation, bindings, ontology and Q&A lanes — the dominant real cost, unrecorded.
- UNKNOWN: whether the Cumin plates would have been worse without the PA-D vocabulary (no ablation).
- UNKNOWN: which of the three EVAL-038 spend figures (2.26 / 2.76 / 3.96) a vendor billed.
- CONFLICT (not harmonised): case 001 says "no new Canon need was proven"; case 003 says the same failure class is "a Canon gap"; case 002 says "not missing Canon knowledge". Three diagnoses of one failure family.
- Method limits: my counterfactual completions are written by a frontier model about frontier-model behaviour (INFERENCE); commit-hour buckets over-count Canon effort where sessions interleaved; agent-6/7 regex counts were not re-run by me (marked OBSERVED-A6/A7).
