# AGENT 15 — CANON DEFENDER / FAILURE-TO-CONSUME INVESTIGATOR (persona 77)

Brief: build the strongest evidence-based case that the production failures arose because Canon knowledge failed to REACH decisions (retrieval, compilation policy, context placement, form, ownership) rather than because the knowledge is weak or unnecessary — and that a strong LLM alone made, or would have made, the same mistakes. I do not issue the verdict. Section 5 steelmans the prosecution.

Repo state: MI `main @ 3bb9a3c` (verified `git rev-parse HEAD`); Cumin evidence `de1f978`; PR #103 `1de2b37`; pilot branch `work/pilot-upwork-intro-video-v4` (`7629894` = V1 commit, `f6ca66f` = head); EVAL-037 lane branches `work/eval-037-sonnet-no-canon`, `work/eval-037-sonnet-controlled-canon`; MF `/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-factory` @ `57b2cca` checkout. Read-only; nothing modified; no provider called. EVAL-037 packages were extracted with `git show` to `scratchpad/audit/agents/e037_15/{nc,cc}/` (18 + 18 files) for counting.

Labels: OBSERVED (read from committed bytes / computed by a shown command) · INFERENCE · HYPOTHESIS · UNKNOWN.

---

## 0. Spot-check of load-bearing citations from wave-1 reports

I re-verified these against the repo before leaning on them. 16 checked; 14 held exactly; 2 held with a line-number discrepancy.

| # | Claim (source report) | Where I checked | Result |
|---|---|---|---|
| 1 | C-10 forbids compiling the eight remaining packs "unless a real runtime failure demands one" (04, 06) | `coordination/CONTROL-STATE.md @ 3bb9a3c` L81, L95, L247 | HELD verbatim |
| 2 | `packs.py`: "a missing pack never blocks a job" — gap recorded, job continues (06) | `runtime/canon/packs.py @ 3bb9a3c` L11, L233, L248-294 (`gap_pack_ids`, `canon_gap=bool(gaps)`) | HELD |
| 3 | Gate hard-codes exactly two packs (06) | `canon/gate/doctrine.py @ 3bb9a3c` L33 `EXPECTED_DECISIONS = {"product_appearance": 10, "composition_and_attention": 11}`; L140-145 raise on any other pack_id | HELD |
| 4 | PA-D7 is NOT_MECHANISED, "remains a human / blueprint-model check" (06) | `canon/gate/predispatch.py @ 3bb9a3c` L39-41 | HELD |
| 5 | Skill §4: "Do not compile, paraphrase or invent a pack … record the gap … only if the production actually fails"; §5 "Canon constrains; it does not direct" (04, 06) | `.claude/skills/media-agency/PRODUCTION-WORKFLOW.md @ 3bb9a3c` L118-119, L123; SKILL.md blob `7e324b0` = `JOB.yaml skill_version` | HELD |
| 6 | BOOTSTRAP §2 prints only `decision_id | question` + `CHECK:` — never the DEFAULT text or conflict rules (06) | `.claude/skills/media-agency/BOOTSTRAP.md @ 3bb9a3c` §2 python one-liner | HELD |
| 7 | ABCD source carries "Brand early, often, and richly", "start … in the middle of the action, or open with a close-up", "Ask them to take action", "Use CTAs throughout … more direct as you go", "finish with the product" (04, 06, 10) | `canon/knowledge/current/google-abcd-video-ads/source-knowledge.yaml @ 711163e` L462, L667, L737, L803, L1291-1292, L1799-1801 | HELD (04 cites blob `4e3dc358`; `git cat-file -t` = blob; same file) |
| 8 | All ABCD operational bindings are `status: proposed` (04, 06) | `…/google-abcd-video-ads/operational-bindings.yaml`: 9 bindings, 9 × `status: proposed` | HELD |
| 9 | Cumin `canon:` block 10 selected / 2 injected / 8 missing incl. `commercial_communication`; `cta: none in-frame`; PA-D7 "pass"; `reviews: []` (04, 06, 11) | `de1f978:agency/jobs/AGY-…/JOB.yaml` L112-116, L48, L157, L173 | HELD |
| 10 | The string "ABCD" first enters the job record at `c0f849c`, after the human's V2 verdict (04) | `git log -S'ABCD' main..de1f978 -- agency` → `c0f849c` (15 Sep 23:18 IST), `de1f978` | HELD |
| 11 | `qa_abcd_0010` describes the Cumin V2 shape and is excluded from production by contract (06, 07) | `canon/qa/canon-014/google-abcd-video-ads-qa-bank.yaml` item text; `runtime/contracts/PRODUCTION-SPEC-v1.yaml` L69; `canon/context/CANON-CONTEXT-SPEC-v0.1.md` L134; `canon/packs/COMPILED-PACK-CONTRACT-v0.1.md` L172 | HELD (3 of the 4 named contracts checked) |
| 12 | EVAL-037 conclusion table: NO_CANON leads B03/B04, CONTROLLED_CANON leads B01/B06, ties B02/B05 (08, 10) | `eval/experiments/EVAL-037/CONCLUSION.md @ 3bb9a3c` L57-64 | HELD |
| 13 | EVAL-038: "The packs made weak models disciplined. They did not make them good" (06) | `canon/findings/PROPOSED-EVAL-038-CONCLUSION.md` L18-21 | HELD |
| 14 | Case 001 CANON-BRIEF carried ABCD/Ogilvy closing rules by id at "lines 185-187" (06 §3 recurrence table); contrast rules at "line 174" (05) | `7629894` and `f6ca66f` `:pilots/upwork-intro-video-2026-09-14/preprod/CANON-BRIEF.md` | HELD on content, **line numbers wrong**: brand-early/end-on-package row is L20, pacing/CTA/end-on-package is L65, contrast numbers are L52 (same in both revisions) |
| 15 | 001 ACCEPTED-TEMPLATE beat 10 is `human_cta` with a CTA card (04) | `production-learning/cases/UPWORK-INTRO-001/ACCEPTED-TEMPLATE.yaml` L22 | HELD |
| 16 | MF receptionist forced `cta`/`headline` into every brief; HANDOFF §5 "a photo with a banner stamped on it" (02) | `media-factory/packages/whatsapp/src/receptionist.ts` L31-36, L99-109; `media-factory/HANDOFF.md` L23-25 | HELD |

Also verified: `pack-triggers-v0.yaml` L44 (`commercial_communication: 4096` budget) and L90-92 (conditional on `advertising_acceptance_intent`); `KIND-NR-BINDING-v0.yaml` 8 kinds with `advertising_acceptance_intent: true`; `compile_pilot_packs.py` L491-503 hard-codes `PACKS = [product_appearance, composition_and_attention]` (909 lines; not generic over pack ids); `check_vo_schedule` on `1de2b37` has callers only in `gates.py` and its test.

---

## 1. Eight-state ladders per production failure

Ladder: (1) exists → (2) retrieved → (3) in context → (4) understood → (5) changed a decision → (6) decision correct → (7) survived production → (8) QA-detected. For each failure: the rung where it broke and the mechanism, with citations.

### 1.1 Tutorial-not-ad (Cumin V1/V2; HD-06 / DF-07)

| Rung | State | Evidence |
|---|---|---|
| 1 exists | ✔ | OBSERVED. ABCD `sk_abcd_0010` "Brand early, often, and richly" (L667); `concept_label: brand_shows_up_early_and_throughout` (L737); L1799 "Start with a mix of branding elements and finish with the product"; Hopkins `sk_hop_sa_0026` "A picture … must be a salesman in itself and earn the space it occupies" (`hopkins-scientific-advertising-ch1-7/source-knowledge.yaml` L1393). Also `qa_abcd_0010`. |
| 2 retrieved | ✘ **BROKE HERE** | OBSERVED. Trigger table fired `commercial_communication` (JOB.yaml L113); `packs_injected` excludes it (L114); listed in `missing_domains` (L115). Mechanism: **compile policy C-10** (CONTROL-STATE L81/L95: "The remaining eight packs are not compiled unless a real runtime failure demands one") + **`packs.py` continue-on-gap** (L11) + **hard-coded two-pack gate** (`doctrine.py` L33 — a third pack cannot even be loaded without a code change) + **compiler not generic** (`compile_pilot_packs.py` L491-503). |
| 3 in context | ✘ (by policy) | OBSERVED. **BOOTSTRAP §2** never lists `canon/knowledge/current/**`; **WORKFLOW §4** L118-119 instructs "Do not compile, paraphrase or invent a pack for a missing domain. Proceed on the brief and record the gap … only if the production actually fails for want of it" — reading the gap domain is policy-discouraged, and the gap is to be *recorded after the human sees the failure*. Q&A form (`qa_abcd_0010`) is **contractually excluded** (PRODUCTION-SPEC L69; CONTEXT-SPEC L134; PACK-CONTRACT L172). |
| 4–8 | unreachable | The one compiled advertising decision, PA-D7, reached rung 4 and failed at 5–6 (see 1.3). |
| Post-hoc proof that rungs 4–6 work when 2–3 are supplied | ✔ | OBSERVED. After the human's "canon had this knowledge", the operator read ABCD and at `c0f849c` (JOB.yaml L141, L347, L402) produced: persistent brand mark from frame 1 ("ABCD 'early and throughout'"), product end card, spoken close ("see and say"), Direction "cuminco.com" — at USD 0 composition + one TTS line (att-051). The V3 verdict names only VO overlap (HUMAN-VERDICTS V3 L50-53). INFERENCE: the operator model understands and applies the doctrine instantly once it is in context; the missing link was delivery, not comprehension. |

### 1.2 No opening / weak hook (HD-05)

- Rung 1 ✔ OBSERVED: `sk_abcd_0007` "start your ad in the middle of the action, or open with a close-up" (L462/503); `sk_abcd_0005` hook-and-sustain. Case 001 CANON-BRIEF L18-19 had already operationalised this ("Open tight and in progress; no establishing wide"; "A sound event synchronous with frame 1").
- Rung 2 ✘ **BROKE**: same pack, same policy. Additionally, the 001 lesson reached the Cumin operator only as *narrative* (BOOTSTRAP reads case READMEs/queues) — the opening verdicts ("opening not visually exceptional", "opening still not strong enough", 001 HUMAN-VERDICTS L19, L31) were never promoted to any field or rule (001 PROMOTION-QUEUE promotes only gates + SPEAKER_MICROQUALIFICATION). So rung 3 for the *case* knowledge was ✔ and rung 5 ✘ — a **form** failure (prose in a README vs a requirement).
- OBSERVED: the blueprint has a `hook` field (WORKFLOW §5 table) which the operator filled ("A noodle slips back into the bowl in the first second", JOB.yaml L123) while V1 beat 1 was a wide static two-shot (04 §A.3). INFERENCE: a field with no doctrine and no check behind it does not bind; the ABCD "close-up / mid-action" default would have contradicted the wide two-shot directly.

### 1.3 Weak product role (HD-04)

- Rung 1 ✔; rung 2 ✔ (PA-D7 injected, 04 §C(3)); rung 3 ✔ (BOOTSTRAP printed Q + CHECK); rung 4 ✔ (operator wrote a PA-D7 line in pack vocabulary, JOB.yaml L157).
- Rung 5–6 ✘ **BROKE**: `PA-D7: "pass — 'the bowl on a noodle night' sells at a glance; the hero image needs no copy"` — a **self-attested check line** with **no mechanical test** (`predispatch.py` L39-41 NOT_MECHANISED) and **no independent reviewer** (`reviews: []` L173; the "Karl disconfirmer / Ezra copy" personas named in WORKFLOW §5 do not exist anywhere in the repo — 04 §A.3, grep confirmed by 04).
- Form mechanism, OBSERVED: the operator never saw PA-D7's DEFAULT ("size imagery by importance to the sale, never decoration", PACK L714-715) by the documented path — BOOTSTRAP prints only Q and CHECK. The CHECK ("State in one line what the hero image sells at a glance; if that line needs the body copy, the image fails", L717-718) is a print-era Hopkins test (`[DATED|CULTURE-BOUND|MEDIUM-UNTESTED]` markers, L710) that a 2026 Reels film passes trivially with one sentence. INFERENCE: the compiled *form* (question + self-check) is the failing element here, not the underlying claim.
- Rung 8 ✘: no QA row asks "is the product the hero" (QA-CHECKLIST grep: only C5/CF2/CF5 mention cta/hero in a layout sense).

### 1.4 Weak close / no end card (HD-04/06)

- Rung 1 ✔: L1799 "finish with the product"; Ogilvy `sk_ogx_0039` "end on the package" (CANON-BRIEF L65, L121); 001 ACCEPTED-TEMPLATE beat 10 `human_cta` (L22).
- Rung 2 ✘ **BROKE** for ABCD/Ogilvy (uncompiled pack). Rung 3 ✔ / rung 5 ✘ for the 001 template (mandated reading, prose, no rule) — **form + ownership**: the template's `status: accepted_once` is "not a Canon rule" by its own header (L3), so nothing obliged the next job to end on the product.
- OBSERVED: `cta_placement: "brand line 'Cumin Co.' bottom-centre of the end beat … no other CTA"` (L127) is a *placement of a placement*, decided by the operator alone at 13:27Z, never surfaced as a question.

### 1.5 CTA weakness (`cta: none in-frame`, L48)

- Rung 1 ✔: `sk_abcd_0019/0020/0021` "Ask them to take action … be more direct as you go … reinforce onscreen CTA with voice-over" (L1291-1292, L1801); StoryBrand `sk_sb_c003_0011`; MF receptionist forced a `cta` field on every brief (receptionist.ts L33-36).
- Rung 2 ✘ **BROKE** (same pack). Rung 3 for the *skill*: the skill treats CTA as an exact-text typesetting mechanism (JOB-TEMPLATE L38 `mandatory_text` roles; L40 `cta: null`; L83 `cta_placement: null`) with **no rule that it be non-null** — the field exists, the requirement does not. **Ownership**: no persona, no gate, no human question owns "does this ad ask for anything".

### 1.6 Text over subject (V1 "text is coming on figures"; DF-04; 001 V3; 002 HD-03/05/07-10)

- Rung 1 — partial. OBSERVED: no Canon SK names copy-over-subject as a rule (06 §4: regex over 1,300 objects, 0 hits); adjacent: `sk_ogx_0028` "headlines over the picture are named failures" (CANON-BRIEF L52), `sk_abcd_0008` "avoid competing elements", CA-D1. MF prior: `campaign.ts` L14 reserved "the upper-right two-thirds … kept open for a caption" and MFH audit Theme 1 "placement assumes empty space … collides with product/faces" (02 L158).
- Rung 3 ✔ (CF2 row mandated; 002 candidates read; `product_placement: "never obstructed by text"` in the blueprint). Rung 5–8 ✘ **BROKE at self-attestation + no gate**: `CF2: "PASS on 9:16 (copy on empty wall, nothing over bowl/hands/faces)"` (JOB.yaml L326) written by the author against a 4-frame contrast probe with no obstruction test (DF-04, L345); the human rejected the same file. 002's `TEXT_OVER_IMAGERY_CONDITIONAL` had a promotion condition ("an obstruction check exists in the compositor") that nobody owned (10 §2.1).
- Honest note: this is a **content-thin** rung-1 in Canon proper; the *delivery* failure is of the 002 learning and the MF prior (02 §, 05 §3), not of a doctrine pack. It still supports the thesis in its weaker form: knowledge in the repo (MF, 002) did not reach the compositor.

### 1.7 Robotic voice (001 V3; 003 rounds 1–3)

- Rung 1 ✔ OBSERVED (in the repo, not in Canon): MFH `MEDIA-FACTORY-ROUTING-PRIOR.md` L28-29 "raw TTS sounds robotic without speech-rhythm rewrite + mix"; "EL western voices … rejected by ear even in English (el_sarah_v3.mp3)"; 001 RO-05. Canon: 0 sources on audio (`modality_base_packs.audio: []`).
- Rung 2/3 ✘ **BROKE by design**: `runtime/route/evidence.py` reads only the taint register (08 §5: `grep -rn historical runtime/` → 0); the routing map's `historical_prior` tier is `no_row_for_this_route_family` for Sarvam (08 §3.1); the pilot's ROUTE-ANALYSIS states "none is relied on below" (05 §1.2). **MF priors unread by routing code.**
- Rung 3 ✔ / 5 ✘ for the 001 case learning: JOB.yaml cites RO-05 and still dispatched Sarvam ×8 and ElevenLabs Sarah (`EXAVITQu4vr4xnSDxMaL`) first — the exact voice MF recorded as rejected (04 §C(7)). Mechanism: RO-05 is `routing_authority: none` **by rule** (sync skill class 3), so it can never change route rank — a representation that forbids the knowledge from binding.

### 1.8 VO overlap (V3, DF-08)

- Rung 1: not in Canon (K0 for Canon; universal craft). The analogue existed as code (`check_text_bounds`, `check_disjoint`) and doctrine ("text overflow fails closed").
- Rung 5 ✘: the blueprint stored VO `t:` as hand-set plan values before any VO existed (04 §C(8)); nothing measured a wav. Rung 8 ✘: D14 "pending human ear" when V3 was presented (10 §2.5).
- This failure is engineering, not Canon; I do not claim it for the defence. Noted for completeness: the promoted fix (`check_vo_schedule`) has no caller on `1de2b37`, i.e. the same "exists but does not reach" pattern in code form.

### 1.9 Text clipping / contrast / crop (001 V3; 002 HD-01/02/04/06/11)

- Contrast, rung 1 ✔ / rung 3 ✔ / rung 5 ✘: CANON-BRIEF L52 had "Text ≥ 4.5:1 … reverse type and headlines over the picture are named failures … grayscale check (CA-D5)" *in the pilot's own context* before V1; the V3 compositor drew "HUMAN-CHECKED" over the dal photo (05 §1.3(e)). WCAG `sk_wcag_0001` 4.5:1 is in accepted Canon (`w3c-wcag22-text-legibility/source-knowledge.yaml` L26). **Form**: a number in a 22.7 KB prose brief written for the script author does not bind a compositor; the same number as `check_contrast` (14 Sep) held in Cumin (no contrast complaint in 003).
- Clipping: rung 1 ✘ in Canon (05: "1 file mentions safe area"); rung 1 ✔ in MF (P16 text overflow, 02 L187). Delivered as code after 001; **002 never imported it** (05 §2.1). Crop: CA-D6 is not a crop rule (K1 at best); 002 FORMAT_SPECIFIC_REVALIDATION reached rung 8 in Cumin (CF2 FLAGGED on 4:5/1:1, JOB.yaml L320-321, L327-328) and the flagged files were presented anyway — **ownership**: a flag "for the human" with no rule that a flagged file is not a candidate.

### 1.10 Summary table

| Failure | Rung broke | Mechanism (cite) |
|---|---|---|
| Tutorial-not-ad | 2 | C-10 (CONTROL-STATE L81/L95); `packs.py` L11; `doctrine.py` L33; WORKFLOW L118-119; Q&A excluded (PRODUCTION-SPEC L69) |
| No opening | 2 (ABCD) / 5 (001 lesson) | same + 001 verdicts never promoted beyond README prose |
| Product role | 5–6 | PA-D7 self-attested (JOB.yaml L157); NOT_MECHANISED (predispatch L39); `reviews: []` (L173); DEFAULT not printed (BOOTSTRAP §2) |
| Weak close | 2 / 5 | same pack; ACCEPTED-TEMPLATE `not_a_canon_rule` |
| CTA | 2 / 3 | JOB-TEMPLATE `cta: null` with no non-null rule; "Canon constrains; it does not direct" (WORKFLOW L123) |
| Text over subject | 5/8 | CF2 self-PASS (L326); 002 candidate condition unowned; MF prior unread |
| Robotic voice | 2/3 | `evidence.py` reads Lab only; `historical_prior` unjoined; RO-05 `routing_authority: none` by rule |
| VO overlap | — | engineering (not claimed) |
| Contrast/clip/crop | 5 (contrast) / 2 (clip) / 8→5 (crop) | prose brief ≠ compositor input; gates library-only until a job script imports them; flagged files presented |

OBSERVED overall: of nine failure classes, seven have rung-1 knowledge somewhere in the repo (Canon, case files, or MF), and in every one of those seven the break is at rung 2, 3, or 5 — a delivery, form, or ownership rung — never at rung 1 being wrong.

---

## 2. Does a strong LLM WITHOUT Canon make the same mistakes? (honest reading)

### 2.1 EVAL-037 Sonnet NO_CANON vs CONTROLLED_CANON — computed from the packages

Method: extracted all 18 + 18 Sonnet packages; regex counts over the two advertising video briefs (B01 RentOK 30-s vertical ad; B04 skincare 25-s UGC). B05 is a non-advertising café scene and is excluded.

| Package | CTA mentions | "end card" | logo/wordmark | brand-early phrase |
|---|---|---|---|---|
| NO_CANON B01-R1 / R2 / R3 | 10 / 5 / 6 | 1 / 1 / 3 | 7 / 5 / 4 | 0 / 0 / 0 |
| NO_CANON B04-R1 / R2 / R3 | 5 / 5 / 6 | 2 / 4 / 1 | 2 / 4 / 2 | 0 / 0 / 0 |
| CONTROLLED B01-R1 / R2 / R3 | 6 / 5 / 3 | 6 / 2 / 0 | 5 / 3 / 3 | 1 / 0 / 0 |
| CONTROLLED B04-R1 / R2 / R3 | 3 / 7 / 4 | 0 / 5 / 1 | 3 / 5 / 1 | 0 / 0 / 0 |

**Against my case (OBSERVED, must be stated plainly):** every NO_CANON package on both ad briefs has a hook block in the first 3 s, a CTA block, and a logo/brand close. E.g. `nc/E037-sonnet-no-canon-B01-R1.txt` L14 "Hook (0–3s) … pattern-interrupt", L18 "CTA (26–30s): Logo, tagline, one clear action line + trust stat", L71 "End card: music resolves … logo lands". `nc/…B04-R1.txt` L13-17 "Hook … Brand recall + soft CTA: product name spoken + on-screen text", L49 "Shot 5 — CTA / PACKSHOT (0:22–0:25)". A strong LLM given a brief that *says* "commercially strong vertical video ad" produces the ad spine unaided. The Controller's own table has NO_CANON leading B03/B04 and tying B02/B05 (CONCLUSION.md L57-64).

**For my case (OBSERVED):**
1. *Brand-early is exactly where NO_CANON and CONTROLLED differ.* In all three NO_CANON B01 packages the brand first appears at the "turn" (14–18 s) and the logo only in the 26–30 s close (`nc/B01-R1` L16-18; `R2` L17-18; `R3` L17-18, L42). CONTROLLED B01-R1 L99 states the change and attributes it: *"google-abcd-video-ads (HOLD): informed the 'jump in' fast cold-open structure … and introducing/maintaining the brand from the match-cut onward rather than only at the very end."* CONTROLLED B01-R2 L24 places "the single strongest branding beat" at 11–13 s. That is the ABCD "early and throughout" rule reaching rung 5 (decision changed) with the model naming the source — on the brief the Controller's blind table scores CONTROLLED_CANON as the leader (B01).
2. *CTA placement.* CONTROLLED B04-R2 L88-89 cites `qa_abcd_0011` "to place the CTA after context is established rather than front-loaded, and to pair the spoken brand mention with the on-screen product/logo" — the ABCD "more direct as you go" / "see and say" rule at rung 5. (Honesty: B04 was judged a NO_CANON lead overall; the *structural* items were adopted, the package lost on other dimensions — 07 §5.)
3. *The Cumin brief is not an EVAL-037 brief.* The EVAL-037 briefs say "commercially strong … video ad" / "performance-oriented UGC video … one clear purchase reason". The Cumin brief says "make a video on how to hold chopsticks … step 1, step 2, step 3 … the boy fails but they still happily eat" — over-specified on tutorial mechanics, silent on product role/CTA (JOB.yaml L25; LEAD-NOTES). The frontier operator executed it literally (`cta: none`, brand line last beat). INFERENCE: the strong-LLM prior is *brief-dominated*; when the brief is a tutorial, the prior yields a tutorial. Canon-as-requirement is precisely the thing that would override a mis-framed brief; Canon-as-optional-doctrine ("constrains; does not direct") cannot.
4. *The skill actively suppressed the prior.* WORKFLOW L118-119 "Proceed on the brief"; L123 "Canon constrains; it does not direct"; SKILL.md L133 red flag "Regenerate everything → classify the defect; repair that layer only". A model told to proceed on the brief and repair only the named layer will not re-frame a tutorial into an ad on its own initiative. OBSERVED that the same operator, once told, re-framed in one pass (1.1 last row).

### 2.2 The Cumin operator IS a frontier model — and made the mistake

OBSERVED: `JOB.yaml` L12 `opened_by: "Vaibhav Chawla (operator: Claude, local desktop session)"`; skill blob `7e324b0`. The operator wrote 21 check lines in fluent pack vocabulary (L150-173), a coherent five-beat blueprint, and a 450-line dispatch tool — this is not a weak model. It still decided `cta: none in-frame`, `offer_placement: none`, brand line only in the last beat. INFERENCE: this is the single strongest data point that "a strong LLM alone" does not reliably supply ad structure when (a) the brief frames the job as a how-to, (b) the workflow says proceed on the brief, (c) nobody asks. The EVAL-037 NO_CANON packages and the Cumin blueprint were produced by the same model family; the variable that differs is the brief framing and the instruction set, not model strength.

### 2.3 MF receptionist era (July 2026)

OBSERVED: MF's receptionist (`receptionist.ts` L31-36, gpt-4o in production per MFH PROMPT-ENRICHMENT-EVIDENCE L16) *forced* the LLM to fill `headline` and `cta` for every brief — i.e. MF treated ad structure as a mandatory field, not as optional knowledge — and its `campaign.ts` L14 prompt put "{{brief.productVisual}} as the clear hero subject" with a reserved caption zone. Output still "looked amateur" because of the composite-always rule ("a photo with a banner stamped on it", HANDOFF L25) — a *mechanism* failure, not a knowledge failure. INFERENCE: MF is evidence that (i) a strong LLM needs the structure to be a *required field* to reliably emit it, and (ii) even with the fields filled, execution mechanisms decide whether the result reads as an ad. MI dropped MF's forced fields (JOB-TEMPLATE `cta: null`, no non-null rule) and re-derived them as the `AD_STRUCTURE_MINIMUM` candidate after the failure (02 L161: "Cumin's AD_STRUCTURE_MINIMUM candidate is MF's filled-brief idea").

### 2.4 Pilot V1/V2 (case 001)

OBSERVED: the pilot had a hand-written CANON-BRIEF in context (L20: "Seller mark in the opening beat and the last frame"; L65: "on-screen CTA paired with spoken CTA; end on the package"). V1 was judged "commercially clear, strong sales logic" (HUMAN-VERDICTS L14-16) and CONCEPT-v2 L43-45 has an end card + "Brand name once (end card)". The V1/V2 defects were *not* ad-structure defects — they were proof size, mockup framing, presenter length, range, opening strength (REVISION-TRACE L28-32). The accepted V4.1 ends on `human_cta` (beat 10). INFERENCE (confounded — different brief, different author): the one job where ABCD/Ogilvy closing rules were *in context before spend* did not fail on ad structure; the one job where they were policy-blocked did. n = 1 vs 1; direction consistent with the thesis; not proof.

### 2.5 Verdict on §2

INFERENCE: A strong LLM *without* Canon does supply hook/CTA/logo-close **when the brief asks for an ad**; it does **not** reliably supply brand-early-and-throughout (NO_CANON B01 ×3: brand at 14–18 s, logo at 26–30 s only), and it executes a tutorial brief as a tutorial (Cumin). The evidence therefore supports a narrower version of the defence: Canon content is redundant with the prior on the *coarse* spine, and additive on the *specific* rules (brand early, CTA-more-direct-as-you-go, see-and-say) — and it is additive only when it reaches context as something the model must answer to.

---

## 3. Is the specific Canon content RIGHT and production-relevant?

| Doctrine (path @ sha) | Cumin evidence that it is the right rule | Would it have changed the human verdict if enforced? |
|---|---|---|
| ABCD "Brand early, often, and richly" / `brand_shows_up_early_and_throughout` (`google-abcd…/source-knowledge.yaml @ 711163e` L667, L737) | Human V2: "the opening is missing too … does not look like ad at all"; V3 fix = "persistent brand mark from frame 1 (ABCD 'early and throughout')" (`c0f849c` JOB.yaml L347) | OBSERVED: the operator's V3 fix cites exactly this rule; V3's verdict names no structure defect. INFERENCE: yes for the "opening/brand" component. |
| ABCD "start in the middle of the action, or open with a close-up" (L462) | V1 beat 1 = wide static two-shot; 001 verdicts "opening not visually exceptional" ×2 | INFERENCE: a required close-up/mid-action open contradicts the plan on its face; the human named the opening in both jobs. |
| ABCD "Ask them to take action … more direct as you go" (L1291, L1801); "finish with the product" (L1799) | `cta: none`; human: "the closing shot should have cumin product and final caption" | OBSERVED: the V3 remedy (product end card + "cuminco.com" Direction) is this rule verbatim. |
| ABCD "See and say" (L803) | V3 spoken close added, cited "see and say" (L141) | OBSERVED: applied and not rejected. |
| Hopkins picture-as-salesman (`sk_hop_sa_0026`, L1393) compiled as PA-D7 | The rule is right (product must earn its space); its compiled CHECK is what failed | INFERENCE: right content, wrong form — see 1.3. |
| WCAG 4.5:1 (`w3c-wcag22…` L26) | 001 V3 "text colour disappearing"; as `check_contrast` code it held in 003 (no contrast complaint) | OBSERVED: same rule, two forms, two outcomes. |
| LSM packshot lighting (`light-science-magic-beyond-ch3`; `qa_lsmx_0039` white-on-white) | V3 end card was built from a borrowed brand photo whose world mismatched the film (12 C7) | INFERENCE: a packshot-lighting rule would have bound the end card; untested. |
| PA-D1..D6, D8..D10; CA-D1..D11 (compiled, injected) | 12-craft-jury: "Individually accepted plates (A, B, H1r2, H2, H3) are all good"; identity stable across V1–V3 (04 §A.3); 21 check lines rendered in pack vocabulary; plate prompts name "one soft window source camera-left … matte surfaces everywhere except the glaze (PA-D1)" (06 §3) | OBSERVED: where compiled doctrine reached context in question form, the plates held on exactly those dimensions. Nothing the human rejected was in the two compiled packs' scope. |
| `qa_abcd_0010` (Q&A, excluded) | Item describes "brings the logo up only at the very end … closes on a 'Buy now' end card … what is wrong — and what is not" — the Cumin V1/V2 shape, with scope discipline (what is *not* wrong) | INFERENCE: the most directly transferable negative example in the corpus for the "does this look like an ad?" judgement, and the one form four contracts forbid. |

OBSERVED (ranking by demand): `PROPOSED-demand-weighted-pack-priority-v1.md` ranks `commercial_communication` P2, demanded by 53/54 briefs; the two compiled packs are the two lowest-demand packs (06 §7). The programme compiled the packs least likely to be tested by a real job.

INFERENCE on "would have changed the human verdict": the human's own V2 words are the doctrine's headings ("product positioning", "closing shot … product and final caption", "opening"). The V3 remedy applied the doctrine and the V3 rejection is on a different axis (VO overlap). That is as close to a within-job A/B as the record allows: same operator, same plates, same voice; structure absent → "not an ad"; structure applied → rejected for audio. UNKNOWN whether the human would have *accepted* V3's structure had audio been clean ("not at all happy with it" is global).

---

## 4. Consumption-mechanism diagnosis — which would have been sufficient to change Cumin V1?

Ranked from most to least likely sufficient, with reasoning and the 13a external evidence where it applies. "Sufficient" = the V1 blueprint at 13:27Z would have carried brand-early, product hero, product end card, and a Direction.

**1. (e) Human sign-off on proposition / product role / CTA before any spend — most likely sufficient.**
OBSERVED: the human already held the doctrine ("did cannon say nothing about product positioning?"), answered four questions at 13:28Z in one message, and approved the V3 structure fix in one word ("go ahead fix it"). The only structural question asked (spoon vs fist) was answered. INFERENCE: a fifth question — "This is framed as a how-to. Product hero? Brand from frame 1? End card with cuminco.com?" — would have been answered before USD 0 was spent. 13a F1.5 (Gawande): checklists work as 5–9 "killer items" at a defined pause point; F1.3 (Urbach): a mandated checklist not enforced in the workflow shows a null effect — the 13:28Z start-of-job summary *is* the pause point and already exists. Cost: zero code; one skill edit. Weakness: this does not scale past a human who knows advertising; it is the right first step, not the end state.

**2. (b) A ≤12-line ad-structure checklist enforced at a pause point before copy freeze — likely sufficient, and the mechanism the literature supports.**
13a F2.1-F2.7 (TICK, CheckEval, Chain-of-Verification, Constitutional AI): the measured behaviour change comes from *binary instance-level questions the model must answer*, ideally answered without seeing the draft's own rationale; F2.8 (IFScale) says keep it short; A2.3 says phrase positively ("brand mark present by t=1 s?" not "don't hide the brand"). OBSERVED that the operator answers questions it is asked (21 check lines rendered; intake questions answered). INFERENCE: "Is the product the hero of frame 1 and the last frame? y/n" is far harder to self-pass than PA-D7's "state in one line what the hero image sells". This is the `AD_STRUCTURE_MINIMUM` candidate (1de2b37 PROMOTION-QUEUE L35-41) — correct instinct, wrongly framed as a stop-gap "until commercial_communication is compiled". Weakness: self-attestation remains (13a E1/E4); pair with (e) or (d).

**3. (c) Showing `qa_abcd_0010` (the negative example) to the operator — probably sufficient for *this* brief, not general.**
13a B3.3/B3.4 (LEAP, RICP): principles anchored to a retrieved *similar mistake* change reasoning decisions where abstract prefixes do not; B3.2: case-based reasoning is the default. OBSERVED: the item is a near-description of V1/V2 and includes what is *not* wrong (scope discipline). OBSERVED that CONTROLLED_CANON B04-R2 cited a sibling item (`qa_abcd_0011`) and adopted its CTA placement (rung 5). Weaknesses: only ~15 of 1,028 items are production-shaped (07 §2); four contracts forbid the corpus; 688 items mislabelled `hold`; naive retrieval over-selects Q&A (07 §5). A hand-picked 5-item negative-example set per pack is cheap; a retrieval path is not.

**4. (d) An independent critic pass — necessary for the *product-role* rung, not sufficient alone.**
13a E1/E3/E4: same-model prompted self-critique does not correct and can degrade; D2.3/D2.4: judges favour their own generations; separation helps when the critic has *different information or a programmatic gate*. OBSERVED: `reviews: []`; the named personas do not exist; 46 of 49 defects across three cases were found by the human (11 §5). INFERENCE: a fresh-context session given only the blueprint + the 12-line checklist (no job transcript) would have flagged `cta: none` and "no product hero" — but only if it has the checklist (form) to judge against; a persona with the same 8,035-word skill and no checklist would likely have produced a 22nd "pass". Rank below (b) because (d) without (b) has nothing to enforce.

**5. (a) Compiling `commercial_communication` in the current pack form — least likely sufficient.**
OBSERVED: the current form is Q + DEFAULT + self-CHECK, of which BOOTSTRAP prints only Q + CHECK; the one advertising decision in that form (PA-D7) was self-passed on the very dimension rejected; EVAL-038 found the packs "made weak models disciplined … did not make them good" (L18-21); gate cannot load a third pack without editing `doctrine.py` L33; compiler hard-codes two packs (L491-503). 13a A1.7: adherence decays with instruction count (a third pack adds ~10 more imperatives to 21). INFERENCE: a compiled pack would have raised the *prior probability* that the operator wrote "brand from frame 1" into the blueprint (the 06 §7 hypothesis of a 22nd pass is plausible but not certain — CONTROLLED_CANON B01 shows the model *does* adopt "early and throughout" when the source is in context), but with self-attested CHECKs and no reviewer it is the weakest of the five. Its value is as the *source* for (b): the 12 lines should be compiled from ABCD ids so provenance survives.

Combined recommendation (clearly marked as recommendation): (b) rendered from ABCD ids, shown to the human at the existing 13:28Z pause (e), with the check answered by a fresh-context session (d). (c) as a 3–5-item appendix per pack. (a) later, in a checklist-shaped form rather than the current questions-with-defaults form.

---

## 5. Best evidence AGAINST my case (steelman) and what would refute me

1. **NO_CANON packages already contain the ad spine.** OBSERVED (§2.1): every Sonnet NO_CANON package on an ad brief has hook 0–3 s, CTA, logo close. The Controller's blind table gives NO_CANON the lead on 2/6 and ties on 2/6. EVAL-038: weak+packs 0/6 vs strong alone. Prosecution reading: the knowledge is in the prior; Canon's delivery problem is moot because there is nothing to deliver.
   *Defence reply:* brand-early is absent in NO_CANON B01 ×3 and present-with-attribution in CONTROLLED B01; the Cumin operator (same model family) omitted the spine under a tutorial brief; the prior is brief-dominated. *Refutation condition:* run the Cumin brief verbatim through a strong model with no repo context, ≥5 samples; if ≥4/5 propose a product end card and brand-from-frame-1 unprompted, my §2.3–2.5 claim is wrong and the failure is purely the skill's "proceed on the brief" instruction (still a consumption failure, but of the *prior*, not of Canon).

2. **The failure is ownership/self-review, not retrieval — a compiled pack would have been self-passed like PA-D7.** OBSERVED: PA-D7 reached rung 4 and failed at 5; 21/21 lines self-marked pass; `reviews: []`. Prosecution reading: rung 2 is a red herring; the system would have failed at rung 5 anyway.
   *Defence reply:* I agree the pack *form* is weak (§4 rank 5) — but that is itself a consumption failure (form), and the V3 evidence shows the operator applies the doctrine correctly the moment it is in context as a requirement. *Refutation condition:* replay the Cumin blueprint step with a compiled `commercial_communication` pack injected (experiment-only compile, not merged); if the operator still writes `cta: none` and self-passes, form/ownership dominates and (a) is worthless — my ranking already predicts this, so it would not overturn §4, only §1.1's emphasis on rung 2.

3. **Two of the six Cumin failures have no Canon knowledge at all** (text-over-subject, voice casting; 06 §4 regex over 1,300 SK objects: 0 hits), and the audio modality has zero sources. Prosecution reading: the corpus is mis-shaped for the failures that actually recur.
   *Defence reply:* conceded for Canon proper; both had rung-1 knowledge elsewhere in the repo (MF priors, 002 candidates) that also failed to reach decisions — the consumption thesis holds at repo level, not at Canon level. *Refutation condition:* none needed; this bounds the claim.

4. **Case 001 and 002 both declared "no new Canon need" / "not missing Canon knowledge"** (001 PROMOTION-QUEUE L84; 002 NO_CANON_CHANGE). Prosecution reading: two of three operators, closer to the work, judged Canon irrelevant.
   *Defence reply:* 001 had ABCD/Ogilvy in context via CANON-BRIEF and did not fail on structure — consistent with "Canon reached, no gap"; 002 bypassed everything. The three diagnoses were never reconciled (10 §8). *Refutation condition:* if the pilot's own record shows the CANON-BRIEF was written *after* the concept (i.e. it did not inform V1), my §2.4 inference fails. UNKNOWN — commit ordering within `7629894` not checked.

5. **Human verdicts map to contract criteria only 7% strictly** (10 §4.3) and the human's register ("does not look like an ad", "competent, not extraordinary") is not decidable from doctrine. Prosecution reading: no checklist can capture the acceptance criterion; the bottleneck is taste.
   *Defence reply:* the V2 verdict decomposes into three ABCD headings; the V3 fix satisfied them; the residual rejection was mechanical (overlap). Taste rejections in 001 (V2 "not extraordinary") are real and outside Canon's scope — but Cumin's were not. *Refutation condition:* a second reviewer scoring V3-with-clean-audio as "still not an ad" would show the doctrine is insufficient for acceptance even when applied.

6. **Budget-matched memory/skill modules can be net-negative** (13a B2.5, C2.3): more context, more instructions, more decay. Prosecution: adding a pack or a checklist adds tokens to an already 75–85k-token bootstrap (11 §2.3).
   *Defence reply:* §4 ranks the short checklist at the pause point above the pack for exactly this reason; the 21 existing check lines could be cut, not added to.

---

## 6. Minimal changes that would let existing Canon knowledge reach decisions (not a redesign)

Costs are my estimates (INFERENCE), in operator-hours and USD 0 provider spend unless stated. Ordered by leverage per cost.

| # | Change | Rung fixed | Mechanism | Est. cost |
|---|---|---|---|---|
| 1 | Add 5–9 **ad-structure questions** to the start-of-job summary the human already answers at intake (WORKFLOW §8 / JOB-TEMPLATE): product hero in first and last frame? brand mark by t=1 s? Direction line? spoken brand mention? end card source? Render each from an ABCD/Ogilvy/Hopkins sk_ id so provenance survives. Phrase positively. Block dispatch until answered. | 2→5 for §1.1, 1.2, 1.4, 1.5 | 13a F1.5, F2.1-F2.7; MF's forced `cta`/`headline` fields | 1–2 h skill edit (JOB-TEMPLATE + WORKFLOW §5/§8 + QA-CHECKLIST) |
| 2 | Make `blueprint.cta`, `cta_placement`, `product_placement` **non-null required** with a "none" value requiring a stated brief clause (same shape as `deviations`). | 5 | closes the `cta: null` hole (JOB-TEMPLATE L40, L83) | 30 min |
| 3 | **Delete WORKFLOW L118-119** ("Do not compile, paraphrase … record the gap only if the production actually fails") and replace with: "For each `missing_domain`, read the domain's top-N accepted SK claims (list below) before the blueprint; cite ids in `learning_applied`." Keep C-10's "do not compile" for the *pack* artefact; stop forbidding the *reading*. | 2–3 | removes the policy block; BOOTSTRAP already has the read-list pattern | 1 h + a per-domain id list (~10 ids per gap domain, 8 domains: 2–3 h once) |
| 4 | **Fresh-context check pass**: before the human sees the summary, spawn a subagent with only (brief, blueprint, the #1 questions) — no job transcript, no skill — and record its answers in `blueprint.reviews[]`. Disagreements go to the human. | 5–6 (self-attestation) | 13a E1/E4, D2.3; `reviews: []` today; personas named in §5 do not exist | 2 h skill edit; ~USD 0.05–0.20 per job |
| 5 | Print the pack **DEFAULT** lines (not just Q + CHECK) in the BOOTSTRAP one-liner, and cut the 21 check lines to the ≤10 that are not already mechanised, so the DEFAULT text fits. | 3–4 for the compiled packs | BOOTSTRAP §2 prints 4,520 chars without DEFAULTs (06 §3) | 30 min |
| 6 | Append a **negative-example appendix** to each pack / to the #1 questions: 3–5 hand-picked Q&A items rewritten as "a film that does X fails Y" (start with `qa_abcd_0010`, `0019`, `0011`, `qa_ogx_0073`, `qa_lsmx_0039`). Do not open Q&A retrieval; copy the five items into the skill with source ids. | 3–5 | 13a B3.3/B3.4 (mistake-anchored principles) | 1–2 h; needs a one-line Controller note that copied, id-cited items are not "Q&A retrieval" under PRODUCTION-SPEC L69 |
| 7 | **Flagged ≠ candidate**: a CF-row FLAGGED/REVIEW file is not presented as a deliverable; it is listed under "not delivered, why". | 8→5 for crops | JOB.yaml L320-321, L327-328 presented flagged files three times | 15 min skill edit |
| 8 | **Join MF priors to the routing map**: for the 9 cells with `historical_prior.row_exists`, and for Sarvam/ElevenLabs specifically, add a `directional_notes` line the operator's route step must quote (WORKFLOW §7 already says "directional production notes as tie-breakers"). | 2–3 for voice | `evidence.py` reads Lab only; RO-05 `routing_authority: none` | 1–2 h YAML edit; no runtime change |
| 9 | Promote the 001 opening verdicts and the 001/003 close-on-product pattern from README prose into the #1 question list (they are the same rules as ABCD; cite both the case and the sk id). | 5 | case learning is prose read once per session (10 §1.3) | included in #1 |
| 10 | (Later, USD 0) Compile `commercial_communication` **in checklist form** — decision ids whose CHECK is a binary, artifact-level question — and generalise `compile_pilot_packs.py` PACKS list + `doctrine.py` EXPECTED_DECISIONS. Only after #1–#4 have run on ≥2 jobs. | 2 | C-10's "real runtime failure" has now occurred (LEARNING-PACKET L230-235) | 1–2 days; requires a Controller decision |

Not proposed: retrieval over the 7 MB corpus (13a B2.1/B2.4: near-miss chunks hurt; the relevant ABCD material is ~30 claims), fine-tuning (13a D1), new personas without a checklist (13a E1/E4), or any new pack in the present Q + self-CHECK form.

---

## Findings ranked

1. **Rung 2 broke by policy, not by accident.** `commercial_communication` fired on the Cumin NR and was not injected because C-10 forbids compiling it, `packs.py` continues on a gap, the gate hard-codes two packs, the compiler hard-codes two packs, and WORKFLOW §4 tells the operator not to read the gap domain until after a human rejection. OBSERVED at five separate points in the code and policy (§0 #1-6).
2. **When the same doctrine did reach the same operator, it changed the decision correctly in one pass.** `c0f849c`: brand mark from frame 1, product end card, spoken close, Direction — each cited to ABCD — at USD 0 + one TTS line; V3 rejected on audio only. OBSERVED. This is the strongest single piece of evidence that the knowledge is right and the delivery was the failure.
3. **The strong-LLM prior is brief-dominated, not doctrine-equivalent.** NO_CANON Sonnet supplies hook/CTA/logo-close on "make an ad" briefs but places the brand at 14–18 s and the logo at 26–30 s in all three B01 packages; CONTROLLED_CANON B01 moves the brand to the match-cut and names ABCD as the reason. The Cumin operator (Claude) executed a tutorial brief as a tutorial. OBSERVED (computed over 12 packages + JOB.yaml). INFERENCE: Canon is redundant on the coarse spine and additive on the specific rules the human actually rejected on.
4. **The one compiled advertising decision failed at rung 5 through form and ownership**: PA-D7's DEFAULT was never printed to the operator, its CHECK is a one-line self-attestation, it is NOT_MECHANISED, and `reviews: []`. OBSERVED. A third pack in the same form would most likely have added a 22nd pass — which is why §4 ranks compilation last and a pause-point checklist plus a fresh-context check first.
5. **Case 001 is the natural control**: ABCD/Ogilvy closing rules were in the pilot's context via CANON-BRIEF (L20, L65) before V1; V1 was "commercially clear, strong sales logic" and V4.1 ends on a CTA card; the pilot's failures were elsewhere. OBSERVED; INFERENCE on causation (confounded by brief and author).
6. **MF already knew the fix in July**: forced `headline`/`cta` fields on every brief and a hero-product prompt with a reserved copy zone. MI dropped the forced fields and re-derived them as `AD_STRUCTURE_MINIMUM` after paying for the lesson. OBSERVED.
7. **Two of the six Cumin failures have no Canon content** (text-over-subject, voice); the consumption thesis holds for them only at repo level (MF priors, 002 candidates unread by code). OBSERVED; conceded.
8. **The literature supports the ranking**: short binary checklists at an enforced pause point, answered by something other than the author, are the only intervention with positive evidence in both human-factors and LLM studies (13a F1/F2, E1-E4); declarative doctrine in a prefix has no comparable measured effect. OBSERVED in 13a; not independently verifiable here.

## Open questions / unknowns

- UNKNOWN: whether a strong model given the Cumin brief verbatim and *no* repo context proposes a product end card / brand-from-frame-1 unprompted (the decisive test for §2.5; ≥5 samples, USD < 1).
- UNKNOWN: whether the operator opened `PACK-*.yaml` and read PA-D7's DEFAULT (not recorded; the documented path does not print it).
- UNKNOWN: whether the human would have accepted V3's structure with clean audio ("not at all happy with it" is global).
- UNKNOWN: commit-order inside `7629894` — was CANON-BRIEF written before the V1 concept? If after, §2.4 weakens.
- UNKNOWN: the EVAL-037 blind judges and verdict files (08 §1.3: none committed); the B01 "CONTROLLED leads" signal rests on an uncommitted judgement.
- Conflict to record: agents 05/06 cite CANON-BRIEF lines 174 / 185-187; the content is at L52 / L20+L65 in both `7629894` and `f6ca66f`. Content held; line refs did not.
- Conflict to record: 04 labels the tutorial failure K6/K7/K14 "not K0/K2"; 06 labels it a compile-policy (rung-2) failure; 10 labels it K2/K3 mis-diagnosed as K0. All three agree it is not K0 (knowledge absent). My reading: rung 2 by policy, with rung 5 (form/ownership) as the failure that would have followed had rung 2 been fixed in the current pack form.
